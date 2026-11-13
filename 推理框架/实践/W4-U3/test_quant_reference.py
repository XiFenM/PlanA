"""stdlib 合成已知样例；GPU 检查须显式 W4U3_RUN_GPU_TESTS=1。"""

import importlib.util
import json
import math
import os
from pathlib import Path
import struct
import tempfile
import types
import unittest
from unittest import mock

import quant_reference as qr


def write_safetensors(path, header, payload=b""):
    encoded = json.dumps(header).encode()
    path.write_bytes(struct.pack("<Q", len(encoded)) + encoded + payload)


class IndependentUnpackTests(unittest.TestCase):
    def test_known_awq_permutation_and_signed_word(self):
        self.assertEqual(qr.unpack_awq_word(0x76543210), (0, 4, 1, 5, 2, 6, 3, 7))
        self.assertEqual(qr.unpack_awq_word(0xFEDCBA98 - (1 << 32)), (8, 12, 9, 13, 10, 14, 11, 15))
        self.assertEqual(qr.unpack_awq_word(-1), (15,) * 8)

    def test_reject_non_word_and_bad_layout(self):
        for word in (True, 1.0, -(1 << 31) - 1, 1 << 32):
            with self.subTest(word=word), self.assertRaises(ValueError):
                qr.unpack_awq_word(word)
        good = {"qweight": [128, 2], "qzeros": [1, 2], "scales": [1, 16]}
        qr.validate_projection_layout(good, 128, 16, 128)
        for k, n, group in ((127, 16, 128), (128, 15, 128), (128, 16, 0)):
            with self.subTest(dimensions=(k, n, group)), self.assertRaises(qr.ReferenceFailure):
                qr.validate_projection_layout(good, k, n, group)
        with self.assertRaises(qr.ReferenceFailure):
            qr.validate_projection_layout({**good, "qzeros": [2, 1]}, 128, 16, 128)


class MetadataTests(unittest.TestCase):
    def test_select_only_projection_and_hash_only_its_range(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.safetensors"
            prefix = qr.PROJECTION
            header = {
                prefix + ".qweight": {"dtype": "I32", "shape": [1, 1], "data_offsets": [0, 4]},
                prefix + ".qzeros": {"dtype": "I32", "shape": [1, 1], "data_offsets": [4, 8]},
                prefix + ".scales": {"dtype": "F16", "shape": [1, 8], "data_offsets": [8, 24]},
                "unrelated.weight": {"dtype": "F16", "shape": [8], "data_offsets": [24, 40]},
            }
            write_safetensors(path, header, bytes(range(40)))
            found = qr.locate_projection(Path(directory))
            self.assertEqual(set(found), {"qweight", "qzeros", "scales"})
            self.assertEqual(qr._payload_sha256(found["qweight"]), qr.hashlib.sha256(bytes(range(4))).hexdigest())

    def test_missing_truncated_and_escaping_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            with self.assertRaises(qr.ReferenceFailure):
                qr.locate_projection(directory)
            path = directory / "model.safetensors"
            path.write_bytes(struct.pack("<Q", 400) + b"{}")
            with self.assertRaises(qr.ReferenceFailure):
                qr.locate_projection(directory)
            path.unlink()
            (directory / "model.safetensors.index.json").write_text(json.dumps({
                "weight_map": {qr.PROJECTION + ".qweight": "../outside.safetensors"}}))
            with self.assertRaises(qr.ReferenceFailure):
                qr.locate_projection(directory)


class OutcomeTests(unittest.TestCase):
    def test_both_error_gates_and_nonfinite(self):
        good = {"finite": True, "relative_l2": 0.005, "max_abs_error": 0.02, "reference_rms": 1.0}
        self.assertTrue(qr.evaluate_metrics(good, "float16")["passed"])
        self.assertFalse(qr.evaluate_metrics({**good, "relative_l2": 0.02}, "float16")["passed"])
        self.assertFalse(qr.evaluate_metrics({**good, "max_abs_error": 0.06}, "float16")["passed"])
        self.assertTrue(qr.evaluate_metrics({**good, "relative_l2": 0.02}, "bfloat16")["passed"])
        self.assertFalse(qr.evaluate_metrics({"finite": False}, "bfloat16")["passed"])
        self.assertFalse(qr.evaluate_metrics({**good, "relative_l2": math.nan}, "float16")["passed"])

    def test_policy_copy_does_not_mutate_acceptance(self):
        policy = qr.reference_policy()
        policy["tolerances"]["float16"]["relative_l2"] = 100
        self.assertEqual(qr.reference_policy()["tolerances"]["float16"]["relative_l2"], 0.01)

    def test_no_gpu_writes_unsupported_before_checkpoint_access(self):
        fake_torch = types.SimpleNamespace(cuda=types.SimpleNamespace(is_available=lambda: False))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            with mock.patch.object(qr.importlib, "import_module", return_value=fake_torch) as loader:
                rc = qr.main(["--model-dir", "/does/not/exist", "--dtype", "bfloat16", "--output", str(output)])
            result = json.loads(output.read_text())
            self.assertEqual(rc, 3)
            self.assertEqual(result["status"], "unsupported")
            self.assertEqual(result["stage"], "gpu_preflight")
            self.assertFalse(result["fp16_retry_eligible"])
            self.assertEqual(result["cases"], [])
            loader.assert_called_once_with("torch")

    def test_compatibility_and_oom_are_different(self):
        compatibility = qr._error_record(RuntimeError("unsupported dtype"), "production_apply", production=True)
        oom = qr._error_record(RuntimeError("HIP out of memory"), "production_apply", production=True)
        self.assertEqual(compatibility["failure_kind"], "compatibility")
        self.assertEqual(oom["failure_kind"], "resource")

    def test_missing_dependencies_and_unknown_runtime_errors_never_authorize_retry(self):
        for exc,kind in ((ImportError("missing optional backend"),"environment"),
                         (AttributeError("kernel API missing"),"internal"),
                         (AssertionError("shape mismatch"),"internal"),
                         (RuntimeError("unexpected compiler error"),"internal")):
            with self.subTest(exception=type(exc).__name__):
                record=qr._error_record(exc,"production_apply",production=True)
                self.assertEqual(record["failure_kind"],kind)
                summary=qr.summarize_cases([{"m":1,**record}],"bfloat16")
                self.assertFalse(summary["fp16_retry_eligible"])
        for message in ("not implemented for 'BFloat16'", "bf16 is not supported"):
            record=qr._error_record(RuntimeError(message),"production_apply",production=True)
            self.assertEqual(record["failure_kind"],"compatibility")

    def test_actual_bf16_triton_out_dtype_diagnostic_is_compatibility(self):
        CompilationError=type("CompilationError",(Exception,),{"__module__":"triton.compiler.errors"})
        exc=CompilationError("at 108:22:\naccumulator = tl.dot(a, b, accumulator, out_dtype=accumulator_dtype)\n"
                             "out_dtype=bfloat16 is unsupported. Please use out_dtype=float32/float16 and cast with `.to(tl.bfloat16)`")
        record=qr._error_record(exc,"production_apply",production=True)
        self.assertEqual(record["status"],"unsupported")
        self.assertEqual(record["failure_kind"],"compatibility")
        summary=qr.summarize_cases([{"m":1,**record},{"m":256,"status":"passed"}],"bfloat16")
        self.assertTrue(summary["fp16_retry_eligible"])

    def test_mixed_failures_never_grant_dtype_retry(self):
        compatibility = {"m": 1, "status": "unsupported", "failure_kind": "compatibility"}
        for status, kind in (("unsupported", "resource"), ("unsupported", "configuration"),
                             ("numerical_failure", "numerical")):
            summary = qr.summarize_cases([compatibility, {"m": 256, "status": status, "failure_kind": kind}], "bfloat16")
            self.assertEqual(summary["failure_kind"], kind)
            self.assertFalse(summary["fp16_retry_eligible"])
        self.assertTrue(qr.summarize_cases([compatibility], "bfloat16")["fp16_retry_eligible"])
        self.assertFalse(qr.summarize_cases([compatibility], "float16")["fp16_retry_eligible"])
        self.assertEqual(qr.summarize_cases([{"m": 1, "status": "passed"}], "float16")["status"], "error")

    def test_production_instrumentation_restores_functions_after_exception(self):
        def original(*args):
            return "called"
        module = types.SimpleNamespace(ops=types.SimpleNamespace(awq_gemm=original, awq_dequantize=original),
                                       torch=types.SimpleNamespace(matmul=original))
        events = []
        with self.assertRaises(RuntimeError):
            with qr._record_production_ops(module, events):
                self.assertEqual(module.ops.awq_gemm(), "called")
                raise RuntimeError("test")
        self.assertEqual([event["op"] for event in events], ["awq_gemm"])
        self.assertIs(module.ops.awq_gemm, original)
        self.assertIs(module.torch.matmul, original)


@unittest.skipUnless(os.environ.get("W4U3_RUN_GPU_TESTS") == "1" and importlib.util.find_spec("torch"),
                     "optional GPU reference test; requires explicit W4U3_RUN_GPU_TESTS=1 and torch")
class GPUReferenceTests(unittest.TestCase):
    def test_known_words_group_boundary_and_fp32_reference(self):
        import torch
        if not torch.cuda.is_available():
            self.skipTest("GPU unavailable; no CPU fallback")
        qweight = torch.tensor([[0x76543210], [0x76543210], [-1], [-1]], dtype=torch.int32, device="cuda")
        qzeros = torch.tensor([[0x11111111], [0x22222222]], dtype=torch.int32, device="cuda")
        scales = torch.tensor([[0.5] * 8, [2.0] * 8], dtype=torch.float16, device="cuda")
        actual = qr.independent_awq_weight(torch, qweight, qzeros, scales, 2)
        first = [-0.5, 1.5, 0.0, 2.0, 0.5, 2.5, 1.0, 3.0]
        expected = torch.tensor([first, first, [26.0] * 8, [26.0] * 8], device="cuda", dtype=torch.float32)
        torch.testing.assert_close(actual, expected, rtol=0, atol=0)
        self.assertEqual(actual.dtype, torch.float32)


if __name__ == "__main__":
    unittest.main()
