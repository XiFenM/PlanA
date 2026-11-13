"""Tiny local cache fixtures and mocked HTTP failures; no model download."""
from __future__ import annotations
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest import mock
import run


class HttpFailure(Exception):
    def __init__(self,status):
        super().__init__(f"mock HTTP {status}")
        self.response=types.SimpleNamespace(status_code=status)


def item(name,data):
    return {"name":name,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}


@contextmanager
def fixture(download):
    data={"LICENSE":b"shared public license", "base.bin":b"base weights fixture",
          "quant.bin":b"quant weights fixture", "config.json":b"fixed config"}
    models={"bf16":{"model_id":"test/base","revision":"base-fixed",
                     "files":[item(n,data[n]) for n in ("LICENSE","base.bin")]},
            "awq":{"model_id":"test/quant","revision":"quant-fixed",
                   "files":[item(n,data[n]) for n in ("LICENSE","config.json","quant.bin")]}}
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with mock.patch.object(run,"ROOT",root),mock.patch.object(run,"model_manifests",return_value=models), \
             mock.patch.dict("sys.modules",{"huggingface_hub":types.SimpleNamespace(snapshot_download=download)}), \
             mock.patch.dict(run.os.environ,{"HF_ENDPOINT":"https://mirror.example"}), \
             mock.patch.object(run.time,"sleep") as sleep:
            yield root,models,data,sleep


def put(root,variant,revision,name,data):
    p=root/"cache"/variant/revision/name
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    return p


class DownloadTests(unittest.TestCase):
    def test_complete_verified_cache_never_calls_hub(self):
        download=mock.Mock(side_effect=AssertionError("network must not be used"))
        with fixture(download) as (root,models,data,sleep):
            for f in models["bf16"]["files"]:put(root,"bf16","base-fixed",f["name"],data[f["name"]])
            path,report=run.obtain_model("bf16",audit_path=root/"acquisition.jsonl")
            self.assertEqual(len(report["files"]),2)
            self.assertTrue(path.is_dir());download.assert_not_called();sleep.assert_not_called()

    def test_shared_license_503_avoided_by_verified_copy(self):
        calls=[]
        def download(**kwargs):
            calls.append(kwargs)
            if "LICENSE" in kwargs["allow_patterns"]:raise HttpFailure(503)
            for name in kwargs["allow_patterns"]:(Path(kwargs["local_dir"])/name).write_bytes(data[name])
        with fixture(download) as (root,models,data,sleep):
            license_path=put(root,"bf16","base-fixed","LICENSE",data["LICENSE"])
            path,report=run.obtain_model("awq",audit_path=root/"acquisition.jsonl")
            self.assertEqual((path/"LICENSE").read_bytes(),data["LICENSE"])
            self.assertEqual(license_path.read_bytes(),data["LICENSE"])
            self.assertEqual(calls[0]["allow_patterns"],["config.json","quant.bin"])
            self.assertEqual(calls[0]["endpoint"],"https://mirror.example")
            self.assertFalse(calls[0]["token"])
            self.assertFalse(calls[0]["force_download"])
            self.assertEqual(len(report["files"]),3);sleep.assert_not_called()

    def test_corrupt_shared_source_not_reused_and_bad_target_forced(self):
        calls=[]
        def download(**kwargs):
            calls.append(kwargs)
            for name in kwargs["allow_patterns"]:(Path(kwargs["local_dir"])/name).write_bytes(data[name])
        with fixture(download) as (root,models,data,sleep):
            put(root,"bf16","base-fixed","LICENSE",b"x"*len(data["LICENSE"]))
            for name in ("LICENSE","config.json"):put(root,"awq","quant-fixed",name,data[name])
            put(root,"awq","quant-fixed","quant.bin",b"x"*len(data["quant.bin"]))
            _,report=run.obtain_model("awq")
            self.assertEqual(calls[0]["allow_patterns"],["quant.bin"])
            self.assertTrue(calls[0]["force_download"])
            self.assertEqual(len(report["files"]),3)
            # Now remove target license: corrupt counterpart must not be copied.
            (root/"cache/awq/quant-fixed/LICENSE").unlink()
            run.obtain_model("awq")
            self.assertEqual(calls[1]["allow_patterns"],["LICENSE"])

    def test_partial_download_503_retries_only_remaining_files(self):
        calls=[]
        def download(**kwargs):
            calls.append(kwargs)
            if len(calls)==1:
                (Path(kwargs["local_dir"])/"config.json").write_bytes(data["config.json"])
                raise HttpFailure(503)
            for name in kwargs["allow_patterns"]:(Path(kwargs["local_dir"])/name).write_bytes(data[name])
        with fixture(download) as (root,models,data,sleep):
            put(root,"bf16","base-fixed","LICENSE",data["LICENSE"])
            run.obtain_model("awq",audit_path=root/"acquisition.jsonl")
            self.assertEqual(calls[0]["allow_patterns"],["config.json","quant.bin"])
            self.assertEqual(calls[1]["allow_patterns"],["quant.bin"])
            sleep.assert_called_once_with(2)
            events=[json.loads(line) for line in (root/"acquisition.jsonl").read_text().splitlines()]
            self.assertTrue(any(e["mode"]=="download_error" and e["retryable"] for e in events))

    def test_retry_ceiling_and_nontransient_failure(self):
        for status,attempts in ((503,3),(403,1),(404,1)):
            download=mock.Mock(side_effect=HttpFailure(status))
            with self.subTest(status=status),fixture(download) as (root,models,data,sleep):
                with self.assertRaises(HttpFailure):run.obtain_model("awq")
                self.assertEqual(download.call_count,attempts)
                self.assertEqual(sleep.call_count,attempts-1)
        hard=HttpFailure(403);hard.__cause__=HttpFailure(503)
        self.assertFalse(run.transient_download_error(hard))
        self.assertFalse(run.transient_download_error(PermissionError("disk permission")))
        self.assertTrue(run.transient_download_error(TimeoutError()))

    def test_successful_http_with_wrong_bytes_fails_hash_without_retry(self):
        download=mock.Mock()
        def corrupt(**kwargs):
            for name in kwargs["allow_patterns"]:(Path(kwargs["local_dir"])/name).write_bytes(b"x"*len(data[name]))
        download.side_effect=corrupt
        with fixture(download) as (root,models,data,sleep):
            with self.assertRaises(run.ExperimentError):run.obtain_model("awq")
            self.assertEqual(download.call_count,1);sleep.assert_not_called()


if __name__=="__main__":unittest.main()
