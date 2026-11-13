"""CPU/stdlib tests only. Mocked orchestration is never GPU evidence."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
import sys
from unittest import mock
import zipfile

import run


class DriverTests(unittest.TestCase):
    def test_pinned_model_manifest_is_complete_and_not_a_mutable_branch(self):
        model = run.read_json(run.ROOT / "model_manifest.json")
        self.assertEqual(len(model["revision"]), 40)
        self.assertEqual(model["revision"], run.MODEL_REVISION)
        weights = [f for f in model["files"] if f["name"].endswith(".safetensors")]
        self.assertEqual(len(weights), 1)
        self.assertEqual(weights[0]["bytes"], 3087467144)
        self.assertEqual(len(weights[0]["sha256"]), 64)

    def test_verification_rejects_same_size_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_bytes(b"abc")
            manifest = {"model_id": "test", "revision": "fixed", "files": [
                {"name": "config.json", "bytes": 3, "git_blob_sha1": hashlib.sha1(b"blob 3\0abc").hexdigest()}]}
            self.assertTrue(run.verify_model(tmp, manifest)["files"][0]["verified"])
            path.write_bytes(b"abd")
            with self.assertRaises(run.ExperimentError):
                run.verify_model(tmp, manifest)

    def test_write_json_preserves_raw_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "raw.json"
            run.write_json(path, {"before": 1})
            with self.assertRaises(FileExistsError):
                run.write_json(path, {"after": 2})
            self.assertEqual(run.read_json(path), {"before": 1})

    def test_server_pair_changes_only_budget(self):
        a = run.server_command("/model", 512, 8123)
        b = run.server_command("/model", 2048, 8123)
        differences = [(x, y) for x, y in zip(a, b) if x != y]
        self.assertEqual(differences, [("512", "2048")])
        self.assertEqual(a[a.index("--host") + 1], "127.0.0.1")
        self.assertNotIn("--profiler-config", a)
        trace = run.server_command("/model", 2048, 8123, "/trace")
        config = json.loads(trace[trace.index("--profiler-config") + 1])
        self.assertEqual(config["profiler"], "torch")
        self.assertTrue(config["torch_profiler_with_memory"])

    def test_missing_gpu_does_not_fall_back_to_cpu_benchmark(self):
        reasons = run.environment_reasons({"packages": {"vllm": "0.26.0"}, "disk_free_bytes": 20 * 1024**3})
        self.assertTrue(any("ROCm" in r for r in reasons))
        self.assertTrue(any("GPU" in r for r in reasons))

    def test_total_time_budget(self):
        with mock.patch.object(run.time, "monotonic", return_value=10):
            self.assertEqual(run.time_left(15, 180), 5)
            with self.assertRaises(run.ExperimentError):
                run.time_left(9, 180)

    def test_child_commands_have_package_working_directory(self):
        with mock.patch.object(run.subprocess, "run") as child:
            child.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            run.run_capture(["python", "-c", "pass"])
            self.assertEqual(child.call_args.kwargs["cwd"], run.ROOT)

    def test_reference_timeout_preserves_partial_progress_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "reference.log"
            command = [sys.executable, "-u", "-c",
                       "import time; print('W4_REFERENCE loading',flush=True); time.sleep(10)"]
            result = run.run_reference_logged(command, log, timeout=0.2)
            self.assertEqual(result["error"], "timeout")
            self.assertIsNone(result["returncode"])
            self.assertIn("W4_REFERENCE loading", log.read_text())
            self.assertLess(result["elapsed_seconds"], 3)

    def test_reference_completion_retains_stderr_and_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "reference.log"
            command = [sys.executable, "-u", "-c",
                       "import sys; print('W4_REFERENCE complete'); print('detail',file=sys.stderr); sys.exit(3)"]
            result = run.run_reference_logged(command, log, timeout=3)
            self.assertEqual(result["returncode"], 3)
            self.assertNotIn("error", result)
            self.assertIn("detail", log.read_text())

    def test_control_http_ignores_proxy_and_rejects_redirect(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/redirect":
                    self.send_response(302)
                    self.send_header("Location", "http://example.invalid/")
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"ok": true}')
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}"
            with mock.patch.dict(run.os.environ, {"HTTP_PROXY": "http://127.0.0.1:1", "NO_PROXY": ""}):
                self.assertEqual(run.http_json(url, "/"), {"ok": True})
                with self.assertRaises(run.ExperimentError):
                    run.http_json(url, "/redirect")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_cpu_only_trace_never_passes_as_gpu_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = [{"cat": "cpu_op", "name": "execute_context_1(512)_generation_2(2)",
                       "ph": "X", "ts": 1, "dur": 2, "pid": 3, "tid": 4}]
            path = Path(tmp) / "test.json.gz"
            with gzip.open(path, "wt") as f:
                json.dump({"traceEvents": events}, f)
            self.assertFalse(run.analyze_traces(tmp)["passed"])
            events.append({"cat": "kernel", "name": "hip_kernel", "ph": "X", "dur": 5})
            with gzip.open(path, "wt") as f:
                json.dump({"traceEvents": events}, f)
            result = run.analyze_traces(tmp)
            self.assertTrue(result["passed"])
            self.assertEqual(result["batches"][0]["scheduled_tokens"], 514)
            self.assertIsNone(result["request_kernel_mapping"])

    def test_gpu_annotation_is_not_a_second_host_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            name = "execute_context_1(2047)_generation_1(1)"
            events = [
                {"cat": "user_annotation", "name": name, "ph": "X", "dur": 10, "args": {"External id": 7}},
                {"cat": "gpu_user_annotation", "name": name, "ph": "X", "dur": 100, "args": {"External id": 7}},
                {"cat": "user_annotation", "name": "execute_context_0(0)_generation_0(0)", "ph": "X", "dur": 1},
                {"cat": "kernel", "name": "gpu_kernel", "ph": "X", "dur": 90},
            ]
            (Path(tmp) / "trace.json").write_text(json.dumps({"traceEvents": events}))
            result = run.analyze_traces(tmp)
            self.assertEqual(len(result["batches"]), 1)
            self.assertEqual(len(result["gpu_batch_ranges"]), 1)
            self.assertEqual(len(result["empty_host_ranges"]), 1)
            self.assertEqual(result["batches"][0]["host_scope_dur_us"], 10)
            self.assertEqual(result["gpu_batch_ranges"][0]["gpu_annotation_dur_us"], 100)
            self.assertNotIn("host_scope_dur_us", result["gpu_batch_ranges"][0])
            self.assertEqual(result["batches"][0]["external_id"], result["gpu_batch_ranges"][0]["external_id"])

    def test_gpu_range_and_empty_host_cannot_establish_a_real_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = [
                {"cat": "gpu_user_annotation", "name": "execute_context_1(256)_generation_0(0)", "ph": "X"},
                {"cat": "user_annotation", "name": "execute_context_0(0)_generation_0(0)", "ph": "X"},
                {"cat": "kernel", "name": "kernel", "ph": "X"},
            ]
            (Path(tmp) / "trace.json").write_text(json.dumps({"traceEvents": events}))
            self.assertFalse(run.analyze_traces(tmp)["passed"])

    def test_archive_excludes_weights_symlinks_and_prior_archives(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(run, "ROOT", Path(tmp)):
            case = Path(tmp) / "runs" / "test"
            case.mkdir(parents=True)
            (case / "failure.json").write_text('{"failed":true}')
            (case / "model.safetensors").write_bytes(b"weights")
            (case / "old.zip").write_bytes(b"old")
            (case / "linked.txt").symlink_to(case / "failure.json")
            archive = run.pack_case(case)
            with zipfile.ZipFile(archive) as z:
                self.assertEqual(set(z.namelist()), {"test/failure.json", "test/ARCHIVE_SHA256.json"})

    def test_reference_reuse_requires_identical_conditioning(self):
        record = {"request_id": "r", "prompt_token_ids": [1], "token_ids": [2] * 8,
                  "token_logprobs": [-0.2] * 8}
        baseline = {"cases": [{**record, "positions": [
            {"reference_logprob": -0.2, "reference_top1_id": 2, "reference_top1_logprob": -0.2}
            for _ in range(8)]}]}
        self.assertTrue(run.reuse_reference([record], baseline)["passed"])
        changed = {**record, "prompt_token_ids": [9]}
        self.assertIsNone(run.reuse_reference([changed], baseline))
        bad = {**record, "token_logprobs": [-2.0] * 8}
        self.assertFalse(run.reuse_reference([bad], baseline)["passed"])

    def test_round_percentiles_are_not_mislabelled_as_pooled(self):
        rounds = []
        for i, budget in enumerate(run.ORDER):
            result = {"output_tokens_per_second": 10.0 + i}
            for name in ("request_ttft_ms", "request_tpot_ms", "request_e2el_ms", "pooled_raw_itl_ms"):
                result[name] = {"p50": 20.0 + i, "p99": 100.0 + i}
            rounds.append({"round_id": str(i), "budget": budget, "summary": result})
        result = run.compare_rounds(rounds)
        self.assertEqual(result["by_budget"]["512"]["round_count"], 3)
        self.assertIn("median_of_round_statistics", result["by_budget"]["512"]["request_tpot_ms.p99"])
        self.assertIn("not established", result["p99_status"])

    def test_orchestration_smoke_uses_mock_data_only(self):
        # Exercises all six rounds plus the separate trace with temporary mock files.
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(run, "ROOT", Path(tmp)):
            root = Path(tmp)
            case = root / "runs" / "mock-not-gpu-evidence"
            case.mkdir(parents=True)
            req = {"request_id": "x", "prompt_token_ids": [1], "max_tokens": 128}
            run.write_json(case / "inputs.json", {"requests": [req] * 48, "correctness": []})
            run.write_json(case / "status.json", {"phase": "prepared", "input_sha256": run.sha256_file(case / "inputs.json")})
            run.write_json(case / "model_location.json", {"path": "/mock-model"})
            env = {"passed": True, "packages": {"vllm": "0.26.0"}, "device_visibility": {}}
            run.write_json(case / "environment_prepare" / "environment.json", env)
            prediction = root / "prediction.txt"
            prediction.write_text("Mock test input only. This is not a learner prediction or GPU evidence.")
            calls = []
            @contextmanager
            def fake_serve(model, budget, folder, *, profile=False, deadline=None):
                folder.mkdir()
                calls.append((budget, profile))
                yield "http://127.0.0.1:1"
            def fake_batch(url, model, requests, concurrency, output_path, **kwargs):
                Path(output_path).write_text('{"mock": true}\n')
                result = {"failure_count": 0, "output_tokens_per_second": 10.0}
                for name in ("request_ttft_ms", "request_tpot_ms", "request_e2el_ms", "pooled_raw_itl_ms"):
                    result[name] = {"p50": 1.0, "p99": 2.0}
                return result
            args = argparse.Namespace(case=str(case), prediction_file=str(prediction))
            with mock.patch.object(run, "check_source_identity"), \
                 mock.patch.object(run, "inspect_environment", return_value=env), \
                 mock.patch.object(run, "verify_model", return_value={"mock": True}), \
                 mock.patch.object(run, "serve", fake_serve), \
                 mock.patch.object(run, "validate_outputs", return_value=({}, Path("mock-reference"))), \
                 mock.patch("client.run_batch", side_effect=fake_batch), \
                 mock.patch.object(run, "http_json", return_value={"http_status": 200}), \
                 mock.patch.object(run, "analyze_traces", return_value={"passed": True, "mock": True}):
                self.assertEqual(run.run_command(args), 0)
            self.assertEqual(calls, [(b, False) for b in run.ORDER] + [(2048, True)])
            self.assertEqual(run.read_json(case / "status.json")["phase"], "measured")
            self.assertEqual(len(run.read_json(case / "performance.json")["rounds"]), 6)
            self.assertTrue((case / "prediction.json").exists())
            with self.assertRaises(run.ExperimentError):
                run.run_command(args)


if __name__ == "__main__":
    unittest.main()
