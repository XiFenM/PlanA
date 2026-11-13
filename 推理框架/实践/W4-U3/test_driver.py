"""Standard-library contract tests. Mock orchestration is not GPU evidence."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
from unittest import mock
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parent))
import run
import client
import quality
import memory


def environment():
    return {"passed":True,"reasons":[],"packages":{"vllm":"0.26.0+test","torch":"test"},
            "device_visibility":{},"torch_probe":{"devices":[{"index":0,"name":"mock-only",
            "total_memory_bytes":48*1024**3,"gcn_arch":"gfx1100","uuid":"test","pci_bus_id":"0000:03:00.0"}]}}


def memory_record():
    return {"status":"ok","scope":"matched_pci_bdf","runtime_device_mapping_confirmed":True,
            "thread_stopped":True,"devices":[{"pci_bdf":"0000:03:00.0","valid_samples":3,
            "sampled_max_used_bytes":100,"total_bytes_values":[1024]}]}


def measured_summary():
    result={"failure_count":0,"request_count":48,"output_tokens_per_second":100.0}
    for name in ("request_ttft_ms","request_tpot_ms","request_e2el_ms","pooled_raw_itl_ms"):
        result[name]={"p50":1.0,"p99":2.0}
    return result


class DriverTests(unittest.TestCase):
    def test_pinned_manifests_and_tokenizer_identity(self):
        models=run.model_manifests()
        self.assertEqual(set(models),{"bf16","awq"})
        self.assertEqual(models["awq"]["revision"],"3ecffa0ceb27851800f45519bab9c457a04405e1")
        for m in models.values():
            self.assertEqual(len(m["revision"]),40)
            weights=[f for f in m["files"] if f["name"].endswith(".safetensors")]
            self.assertTrue(weights)
            self.assertTrue(all(len(w["sha256"])==64 for w in weights))
        for name in ("tokenizer.json","tokenizer_config.json","merges.txt","vocab.json"):
            hashes=[next(f["git_blob_sha1"] for f in m["files"] if f["name"]==name) for m in models.values()]
            self.assertEqual(hashes[0],hashes[1])

    def test_model_same_size_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"data"
            p.write_bytes(b"abc")
            manifest={"model_id":"test","revision":"fixed","files":[{"name":"data","bytes":3,
                         "git_blob_sha1":hashlib.sha1(b"blob 3\0abc").hexdigest()}]}
            self.assertTrue(run.verify_model(td,manifest)["files"][0]["verified"])
            p.write_bytes(b"abd")
            with self.assertRaises(run.ExperimentError):run.verify_model(td,manifest)

    def test_server_commands_hold_workload_and_measurement_conditions(self):
        b=run.server_command("/base","bf16","bfloat16",1234)
        q=run.server_command("/quant","awq","bfloat16",1234)
        self.assertEqual(q[-2:],["--quantization","awq"])
        differences=[(a,z) for a,z in zip(b,q[:-2]) if a!=z]
        self.assertEqual(differences,[("/base","/quant")])
        self.assertNotIn("--profiler-config",q)
        self.assertEqual(q[q.index("--host")+1],"127.0.0.1")
        self.assertEqual(q[q.index("--max-num-batched-tokens")+1],"2048")
        with self.assertRaises(run.ExperimentError):run.server_command("/base","bf16","float16",1234)

    def test_missing_gpu_has_no_cpu_fallback_and_method_records_reference(self):
        reasons=run.environment_reasons({"packages":{"vllm":"0.26.0"}})
        self.assertTrue(any("GPU" in r for r in reasons))
        method=run.method()
        self.assertIs(method["full_model_cpu_reference"],False)
        self.assertIs(method["profiler"],False)
        self.assertEqual(method["reference"]["fixture"]["batch_rows"],[1,256])

    def test_reference_timeout_keeps_log(self):
        with tempfile.TemporaryDirectory() as td:
            log=Path(td)/"reference.log"
            result=run.run_reference_logged([sys.executable,"-u","-c",
                    "import time;print('partial output');time.sleep(5)"],log,0.15)
            self.assertTrue(result["timeout"])
            self.assertIn("partial output",log.read_text())
            self.assertLess(result["elapsed_seconds"],3)

    def test_dtype_fallback_only_for_explicit_compatibility(self):
        for status,kind,eligible,retries in (("numerical_failure","numerical",False,False),
                ("unsupported","resource",False,False),("unsupported","compatibility",True,True)):
            with self.subTest(status=status,kind=kind),tempfile.TemporaryDirectory() as td:
                calls=[]
                def fake(command,log_path,timeout):
                    calls.append(command)
                    report=({"status":status,"failure_kind":kind,"fp16_retry_eligible":eligible} if len(calls)==1
                            else {"status":"passed","failure_kind":None})
                    run.write_json(command[-1],report)
                    return {"returncode":0 if report["status"]=="passed" else 3,"timeout":False}
                with mock.patch.object(run,"run_reference_logged",side_effect=fake):
                    if retries:
                        selected=run.select_awq_dtype(Path("/model"),Path(td)/"ref",time.monotonic()+10)
                        self.assertEqual(selected["dtype"],"float16")
                        self.assertEqual(len(calls),2)
                    else:
                        with self.assertRaises(run.ExperimentError):
                            run.select_awq_dtype(Path("/model"),Path(td)/"ref",time.monotonic()+10)
                        self.assertEqual(len(calls),1)

    def test_memory_incomplete_not_misrepresented(self):
        row={"memory":memory_record(),"server_memory":{"model_loading_gib":2.,"kv_capacity_tokens":100}}
        self.assertTrue(run.memory_evidence_complete(row,"00000000:03:00.0"))
        for field,value in (("status","partial"),("thread_stopped",False),("scope","all_devices_unmapped")):
            changed=copy.deepcopy(row);changed["memory"][field]=value
            self.assertFalse(run.memory_evidence_complete(changed,"0000:03:00.0"))
        self.assertFalse(run.memory_evidence_complete(row,"0000:04:00.0"))

    def test_archive_excludes_weights_and_preserves_prior_evidence(self):
        with tempfile.TemporaryDirectory() as td,mock.patch.object(run,"ROOT",Path(td)):
            case=Path(td)/"runs"/"case";case.mkdir(parents=True)
            run.write_json(case/"raw.json",{"value":1})
            with self.assertRaises(FileExistsError):run.write_json(case/"raw.json",{"value":2})
            (case/"model.safetensors").write_bytes(b"fake")
            (case/"escape").symlink_to(case/"raw.json")
            z=run.pack_case(case)
            with zipfile.ZipFile(z) as archive:
                self.assertEqual(set(archive.namelist()),{"case/raw.json","case/ARCHIVE_SHA256.json"})

    def test_round_medians_keep_variants_and_raw_statistics(self):
        rounds=[{"round_id":str(i),"variant":v,"summary":measured_summary()} for i,v in enumerate(run.ORDER)]
        result=run.compare_rounds(rounds)
        self.assertEqual(result["by_variant"]["awq"]["round_count"],3)
        self.assertEqual(result["relative_change_percent_of_round_medians"]["output_tokens_per_second"],0)
        self.assertIn("exploratory",result["p99_status"])

    def _mock_run(self,root,memory_ok=True,fail_round=None,vllm_version="0.26.0+test"):
        real_root=run.ROOT
        env=environment()
        env["packages"]["vllm"]=vllm_version
        for name in run.SOURCE_FILES:shutil.copyfile(real_root/name,root/name)
        case=root/"runs"/"mock-case";case.mkdir(parents=True)
        with mock.patch.object(run,"ROOT",root):
            run.capture_sources(case)
            requests=[{"request_id":str(i),"prompt_token_ids":[1,2],"max_tokens":128} for i in range(48)]
            for name,value in {"method.json":run.method(vllm_version),"inputs.json":{"requests":requests,"smoke":{}},
                    "quality_inputs.json":{"items":[]},"model_locations.json":{"bf16":"/base","awq":"/quant"},
                    "pair_verification.json":{}}.items():run.write_json(case/name,value)
            run.write_json(case/"prepared_data_manifest.json",{n:run.sha256_file(case/n) for n in run.SEALED_FILES})
            run.write_json(case/"environment_prepare"/"environment.json",env)
            run.save_status(case,"prepared")
            prediction=root/"prediction.txt"
            original="这是学习者的预测原文：权重读取可能减少，但执行成本与服务性能需要实际验证。\n"
            prediction.write_text(original)
            stages=[]
            def inspect(folder):
                self.assertEqual(run.read_json(case/"prediction.json")["text"],original)
                folder.mkdir(parents=True)
                run.write_json(folder/"environment.json",env);return env
            def reference(*args):
                stages.append("reference")
                self.assertTrue((case/"prediction.json").exists())
                return {"dtype":"bfloat16","activation_dtype_matches_bf16":True}
            @contextmanager
            def serve(path,variant,dtype,folder,deadline,**kwargs):
                self.assertEqual(kwargs["vllm_version"],vllm_version)
                folder.mkdir(parents=True)
                stages.append(folder.name)
                run.write_json(folder/"server_memory.json",{"model_loading_gib":2.,"kv_capacity_tokens":100})
                yield "http://127.0.0.1:1"
            def batch(*args,**kwargs):
                if fail_round and f"round-{fail_round:02d}" in str(args[4]) and kwargs["phase"]=="measure":
                    raise RuntimeError("mock intentional failure")
                return measured_summary()
            class Sampler:
                def __init__(self,*args,**kwargs):pass
                def start(self):pass
                def stop(self):
                    r=memory_record()
                    if not memory_ok:r["status"]="unavailable"
                    return r
            with mock.patch.object(run,"inspect_environment",side_effect=inspect),mock.patch.object(run,"verify_model",return_value={}), \
                 mock.patch.object(run,"select_awq_dtype",side_effect=reference),mock.patch.object(run,"serve",side_effect=serve), \
                 mock.patch.object(run,"smoke"),mock.patch.object(run,"pack_case",return_value=root/"mock.zip"), \
                 mock.patch.object(client,"run_batch",side_effect=batch),mock.patch.object(memory,"MemorySampler",Sampler), \
                 mock.patch.object(quality,"evaluate_quality",return_value={"valid_for_quality_comparison":True,"accuracy":0}), \
                 mock.patch.object(quality,"compare_quality",return_value={"score_is_mock":True}):
                result=run.run_command(argparse.Namespace(case=str(case),prediction_file=str(prediction)))
            return result,case,stages

    def test_prediction_precedes_all_checks_and_quality_zero_does_not_block_timing(self):
        with tempfile.TemporaryDirectory() as td:
            code,case,stages=self._mock_run(Path(td))
            self.assertEqual(code,0)
            self.assertEqual(stages[0],"reference")
            perf=run.read_json(case/"performance.json")
            self.assertEqual([r["variant"] for r in perf["rounds"]],list(run.ORDER))
            self.assertEqual(run.read_json(case/"status.json")["phase"],"measured")

    def test_v033_profile_survives_prepared_guard_and_all_service_runs(self):
        with tempfile.TemporaryDirectory() as td:
            code,case,stages=self._mock_run(Path(td),vllm_version="0.33.0+rocm72")
            self.assertEqual(code,0)
            self.assertEqual(run.read_json(case/"method.json")["vllm_target"],"0.33.0")
            self.assertEqual(len([s for s in stages if s.startswith("round-")]),6)

    def test_missing_memory_preserves_valid_performance(self):
        with tempfile.TemporaryDirectory() as td:
            code,case,_=self._mock_run(Path(td),memory_ok=False)
            self.assertEqual(code,2)
            status=run.read_json(case/"status.json")
            self.assertEqual(status["phase"],"measured_memory_incomplete")
            self.assertTrue(status["performance_valid"])
            self.assertTrue((case/"performance.json").exists())

    def test_mid_run_failure_does_not_create_full_comparison(self):
        with tempfile.TemporaryDirectory() as td:
            code,case,_=self._mock_run(Path(td),fail_round=3)
            self.assertEqual(code,2)
            self.assertFalse((case/"performance.json").exists())
            self.assertEqual(run.read_json(case/"failure_run.json")["completed_rounds"],2)


if __name__=="__main__":unittest.main()
