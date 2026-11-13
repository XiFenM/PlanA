"""W4-U2 独立正确性校验测试；不下载模型，不产生 GPU 实测证据。

运行：PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s <本目录> -v
可选 tiny Qwen2 测试只在 torch 与 transformers 已安装时运行。
"""

from __future__ import annotations

import copy
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import correctness  # noqa: E402


def record(request_id="case-0", generated=3):
    return {
        "request_id": request_id,
        "prompt_token_ids": [1, 2, 3],
        "token_ids": [4] * generated,
        "token_logprobs": [-0.3] * generated,
    }


def score_fake_logits(logits, candidate, server_offset=0.0):
    # 用小词表的显式分布构造独立参考，不依赖实现中的张量/索引逻辑。
    normalizer = math.log(sum(math.exp(value) for value in logits))
    reference = [value - normalizer for value in logits]
    top1 = max(range(len(logits)), key=logits.__getitem__)
    return correctness.score_reference_position(
        token_id=candidate,
        server_logprob=reference[candidate] + server_offset,
        reference_logprob=reference[candidate],
        reference_top1_id=top1,
        reference_top1_logprob=reference[top1],
    )


class RecordValidationTests(unittest.TestCase):
    def test_normalized_copy_preserves_original_records(self):
        records = [record()]
        before = copy.deepcopy(records)
        actual = correctness.validate_records(records, 10)
        self.assertEqual(records, before)
        self.assertEqual(actual, before)
        self.assertIsNot(actual[0]["token_ids"], records[0]["token_ids"])

    def test_empty_batch_and_missing_arrays_fail(self):
        for invalid in ([], None, {}, "not records"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                correctness.validate_records(invalid, 10)
        for field in ("prompt_token_ids", "token_ids", "token_logprobs"):
            for replacement in ([], None, ""):
                candidate = record()
                candidate[field] = replacement
                with self.subTest(field=field, replacement=replacement):
                    with self.assertRaises(ValueError):
                        correctness.validate_records([candidate], 10)

    def test_ids_must_be_in_vocabulary_and_not_bool_or_float(self):
        for field in ("prompt_token_ids", "token_ids"):
            for value in (-1, 10, True, 1.5, "4", None):
                candidate = record()
                candidate[field][0] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    correctness.validate_records([candidate], 10)

    def test_vocab_boundaries_are_valid(self):
        candidate = record()
        candidate["prompt_token_ids"] = [0, 9]
        candidate["token_ids"] = [9, 0, 9]
        self.assertEqual(correctness.validate_records([candidate], 10), [candidate])

    def test_nonfinite_positive_and_missing_logprobs_fail(self):
        for value in (float("nan"), float("inf"), -float("inf"), 0.01, None, True, "-1"):
            candidate = record()
            candidate["token_logprobs"][0] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                correctness.validate_records([candidate], 10)

    def test_logprob_length_and_fixed_generation_length_fail(self):
        candidate = record()
        candidate["token_logprobs"].pop()
        with self.assertRaisesRegex(ValueError, "长度不一致"):
            correctness.validate_records([candidate], 10)
        with self.assertRaisesRegex(ValueError, "恰好生成 8"):
            correctness.validate_records([record()], 10, expected_generated_tokens=8)

    def test_invalid_or_duplicate_request_ids_fail(self):
        for request_id in (None, "", " ", 123):
            with self.subTest(request_id=request_id), self.assertRaises(ValueError):
                correctness.validate_records([record(request_id)], 10)
        with self.assertRaisesRegex(ValueError, "重复"):
            correctness.validate_records([record(), record()], 10)


class PredictionPositionTests(unittest.TestCase):
    def test_first_token_is_predicted_by_last_prompt_position(self):
        self.assertEqual(correctness.prediction_positions(4, 3), [3, 4, 5])
        # 输入 [p0,p1,p2,p3,g0,g1]；g2 由最后输入 g1 对应的位置 5 预测。
        self.assertEqual(correctness.prediction_positions(1, 1), [0])
        self.assertEqual(correctness.prediction_positions(1, 8), list(range(8)))

    def test_zero_negative_and_boolean_lengths_fail(self):
        for length in (0, -1, True, 2.0):
            with self.subTest(length=length), self.assertRaises(ValueError):
                correctness.prediction_positions(length, 2)
            with self.subTest(length=length), self.assertRaises(ValueError):
                correctness.prediction_positions(2, length)


class PositionScoringTests(unittest.TestCase):
    def test_exact_greedy_with_matching_probabilities_passes(self):
        score = score_fake_logits([0.0, 2.0, -2.0], 1)
        self.assertTrue(score["passed"])
        self.assertTrue(score["exact_top1_match"])
        self.assertEqual(score["greedy_logprob_gap"], 0)

    def test_near_tie_may_differ_but_wrong_token_fails(self):
        near_tie = score_fake_logits([0.0, 0.09, -2.0], 0)
        self.assertTrue(near_tie["passed"])
        self.assertFalse(near_tie["exact_top1_match"])
        wrong = score_fake_logits([0.0, 2.0, -2.0], 0)
        self.assertTrue(wrong["probability_passed"])
        self.assertFalse(wrong["greedy_passed"])
        self.assertFalse(wrong["passed"])

    def test_correct_token_with_wrong_probability_fails(self):
        score = score_fake_logits([0.0, 2.0], 1, server_offset=-0.251)
        self.assertTrue(score["greedy_passed"])
        self.assertFalse(score["probability_passed"])
        self.assertFalse(score["passed"])

    def test_thresholds_are_inclusive_and_independent(self):
        def evaluate(gap, difference):
            return correctness.score_reference_position(
                token_id=0, server_logprob=-1.0 - difference,
                reference_logprob=-1.0, reference_top1_id=1,
                reference_top1_logprob=-1.0 + gap,
            )

        self.assertTrue(evaluate(0.10, 0.25)["passed"])
        self.assertFalse(evaluate(0.100001, 0.25)["passed"])
        self.assertFalse(evaluate(0.10, 0.250001)["passed"])
        # 另一种十进制表示在 binary float 中产生略大于 0.1 的差值。
        boundary = correctness.score_reference_position(
            token_id=0, server_logprob=-1.1, reference_logprob=-1.1,
            reference_top1_id=1, reference_top1_logprob=-1.0,
        )
        self.assertTrue(boundary["passed"])

    def test_reference_nan_or_inconsistent_top1_fails(self):
        kwargs = dict(
            token_id=0, server_logprob=-1.0, reference_logprob=-1.0,
            reference_top1_id=1, reference_top1_logprob=-0.9,
        )
        for field in ("server_logprob", "reference_logprob", "reference_top1_logprob"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                correctness.score_reference_position(**{**kwargs, field: float("nan")})
        with self.assertRaises(ValueError):
            correctness.score_reference_position(**{**kwargs, "reference_top1_logprob": -1.2})
        with self.assertRaises(ValueError):
            correctness.score_reference_position(**{**kwargs, "reference_top1_id": 0})

    def test_one_bad_position_cannot_be_hidden_in_average(self):
        good = score_fake_logits([2.0, 0.0], 0)
        bad = score_fake_logits([2.0, 0.0], 1)
        cases = [{"passed": False, "positions": [good] * 99 + [bad]}]
        result = correctness._summarize(cases, 1)
        self.assertEqual(result["failed_cases"], 1)
        self.assertEqual(result["failed_positions"], 1)
        self.assertEqual(result["max_greedy_logprob_gap"], 2.0)


def fake_tensor(*, dtype="float32", device="cpu", mkldnn=False):
    return SimpleNamespace(
        device=SimpleNamespace(type=device), dtype=dtype, is_floating_point=lambda: True,
        is_mkldnn=mkldnn,
    )


class CpuBackendContractTests(unittest.TestCase):
    def runtime(self, mkldnn):
        linear_type = type("Linear", (), {})
        torch = SimpleNamespace(
            float32="float32", nn=SimpleNamespace(Linear=linear_type),
            backends=SimpleNamespace(mkldnn=mkldnn),
        )
        model = SimpleNamespace(
            modules=lambda: iter([linear_type()]),
            named_parameters=lambda: iter([("weight", fake_tensor())]),
            named_buffers=lambda: iter([]),
        )
        return model, torch

    def test_unavailable_onednn_is_explicit_dense_fallback(self):
        for available, enabled in ((False, True), (True, False)):
            with self.subTest(available=available, enabled=enabled):
                model, torch = self.runtime(SimpleNamespace(is_available=lambda: available, enabled=enabled))
                info = correctness.configure_cpu_reference_backend(model, torch)
                self.assertEqual(info["backend"], "torch_dense_cpu_fp32")
                self.assertEqual(info["linear_count"], 1)
                self.assertEqual(info["converted_linear_count"], 0)
                self.assertIsNone(info["mkldnn_matmul_fp32_precision"])
                self.assertEqual(info["backend_fallback_reason"], "mkldnn_unavailable_or_disabled")

    def test_missing_precision_control_keeps_dense_without_converting(self):
        model, torch = self.runtime(SimpleNamespace(is_available=lambda: True, enabled=True, matmul=object()))
        converter = mock.Mock()
        with mock.patch.dict(sys.modules, {"torch.utils.mkldnn": SimpleNamespace(MkldnnLinear=converter)}):
            info = correctness.configure_cpu_reference_backend(model, torch)
        converter.assert_not_called()
        self.assertEqual(info["backend"], "torch_dense_cpu_fp32")
        self.assertIn("unavailable", info["backend_fallback_reason"])

    def test_failed_ieee_readback_cannot_enable_onednn(self):
        class RefusesIeee:
            @property
            def fp32_precision(self):
                return "bf16"

            @fp32_precision.setter
            def fp32_precision(self, value):
                pass

        model, torch = self.runtime(SimpleNamespace(is_available=lambda: True, enabled=True, matmul=RefusesIeee()))
        converter = mock.Mock()
        with mock.patch.dict(sys.modules, {"torch.utils.mkldnn": SimpleNamespace(MkldnnLinear=converter)}):
            with self.assertRaisesRegex(ValueError, "ieee"):
                correctness.configure_cpu_reference_backend(model, torch)
        converter.assert_not_called()

    def test_parameter_and_buffer_checks_include_mkldnn_weights(self):
        model, torch = self.runtime(None)
        for kind in ("parameters", "buffers"):
            for bad in (fake_tensor(dtype="bfloat16", mkldnn=True), fake_tensor(device="cuda")):
                model.named_parameters = lambda: iter([])
                model.named_buffers = lambda: iter([])
                setattr(model, f"named_{kind}", lambda: iter([("weight", bad)]))
                with self.subTest(kind=kind, dtype=bad.dtype, device=bad.device.type):
                    with self.assertRaisesRegex(ValueError, "CPU|FP32"):
                        correctness._validate_cpu_reference_tensors(model, torch)
        model.named_parameters = lambda: iter([("embedding", fake_tensor())])
        model.named_buffers = lambda: iter([("linear.weight", fake_tensor(mkldnn=True))])
        self.assertEqual(correctness._validate_cpu_reference_tensors(model, torch), {
            "parameter_tensors": 1, "buffer_tensors": 1, "mkldnn_buffer_tensors": 1,
        })


class EvaluationGateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.model_dir = Path(self.temporary.name) / "model"
        self.model_dir.mkdir()
        self.output_path = Path(self.temporary.name) / "report.json"
        self.config = {
            "architectures": ["Qwen2ForCausalLM"], "model_type": "qwen2", "vocab_size": 10,
        }
        self.write_config()

    def write_config(self):
        (self.model_dir / "config.json").write_text(json.dumps(self.config), encoding="utf-8")

    def fake_runtime(self):
        torch = SimpleNamespace(
            __version__="fake-test-only", float32="float32",
            set_num_threads=mock.Mock(), get_num_interop_threads=lambda: 1,
            nn=SimpleNamespace(Linear=type("Linear", (), {})),
            backends=SimpleNamespace(mkldnn=SimpleNamespace(is_available=lambda: False)),
        )
        model_type = type("Qwen2ForCausalLM", (), {})
        model = model_type()
        model.config = SimpleNamespace(model_type="qwen2", vocab_size=10, _attn_implementation="eager")
        model.model = object()
        model.lm_head = object()
        model.eval = mock.Mock()
        model.named_parameters = lambda: iter([("weight", fake_tensor())])
        model.named_buffers = lambda: iter([])
        model.modules = lambda: iter([model])
        loader = mock.Mock(return_value=model)
        transformers = SimpleNamespace(
            __version__="fake-test-only", AutoModelForCausalLM=SimpleNamespace(from_pretrained=loader)
        )
        return {"torch": torch, "transformers": transformers}, loader

    def test_invalid_batch_saves_error_and_does_not_load_reference(self):
        with mock.patch.object(correctness, "_evaluate_case") as evaluate:
            with self.assertRaises(correctness.CorrectnessError) as caught:
                correctness.evaluate_records(self.model_dir, [], self.output_path)
        evaluate.assert_not_called()
        saved = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(saved, caught.exception.report)
        self.assertFalse(saved["passed"])
        self.assertEqual(saved["status"], "error")
        self.assertEqual(saved["error"]["phase"], "records")
        self.assertEqual(saved["summary"]["evaluated_positions"], 0)

    def test_architecture_and_thread_limits_fail_closed(self):
        self.config["architectures"] = ["OtherForCausalLM"]
        self.write_config()
        with self.assertRaises(correctness.CorrectnessError):
            correctness.evaluate_records(self.model_dir, [record(generated=8)], self.output_path)
        for threads in (0, 9, True):
            with self.subTest(threads=threads), self.assertRaises(correctness.CorrectnessError):
                correctness.evaluate_records(
                    self.model_dir, [record(generated=8)],
                    self.output_path.with_name(f"threads-{threads}.json"), threads=threads,
                )

    def test_existing_report_is_rejected_before_validation_without_modification(self):
        original = b'{"passed": true, "prior_evidence": true}\n'
        self.output_path.write_bytes(original)
        with mock.patch.object(correctness, "validate_records") as validate:
            with self.assertRaises(FileExistsError):
                correctness.evaluate_records(self.model_dir, [], self.output_path)
        validate.assert_not_called()
        self.assertEqual(self.output_path.read_bytes(), original)

    def test_dangling_symlink_is_also_existing_output(self):
        missing = self.output_path.with_name("missing.json")
        self.output_path.symlink_to(missing)
        with self.assertRaises(FileExistsError):
            correctness.evaluate_records(self.model_dir, [], self.output_path)
        self.assertTrue(self.output_path.is_symlink())
        self.assertFalse(missing.exists())

    def test_atomic_publication_does_not_replace_concurrent_output(self):
        self.output_path.write_text("prior evidence", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            correctness._write_report(self.output_path, {"new": "report"})
        self.assertEqual(self.output_path.read_text(encoding="utf-8"), "prior evidence")
        self.assertEqual(list(self.output_path.parent.glob(".report.json.*.tmp")), [])

    def test_persistence_failure_does_not_hide_original_validation_error(self):
        with mock.patch.object(correctness, "_write_report", side_effect=OSError("disk full")):
            with self.assertRaises(correctness.CorrectnessError) as caught:
                correctness.evaluate_records(self.model_dir, [], self.output_path)
        failure = caught.exception
        self.assertIsInstance(failure.__cause__, ValueError)
        self.assertEqual(failure.report["error"]["phase"], "records")
        self.assertIn("非空列表", failure.report["error"]["message"])
        self.assertEqual(failure.report["persistence_error"]["message"], "disk full")
        self.assertIn("报告保存也失败", str(failure))

    def test_persistence_failure_blocks_even_successful_reference(self):
        modules, _ = self.fake_runtime()
        good = score_fake_logits([2.0, 0.0], 0)
        case = {"request_id": "a", "passed": True, "positions": [good] * 8}
        with mock.patch.dict(sys.modules, modules), mock.patch.object(
            correctness, "_evaluate_case", return_value=case
        ), mock.patch.object(correctness, "_write_report", side_effect=OSError("disk full")):
            with self.assertRaises(correctness.CorrectnessError) as caught:
                correctness.evaluate_records(self.model_dir, [record("a", 8)], self.output_path)
        result = caught.exception.report
        self.assertFalse(result["passed"])
        self.assertEqual(result["status"], "error")
        self.assertTrue(result["reference_evaluation_passed"])
        self.assertEqual(result["error"]["phase"], "report_write")

    def test_persistence_failure_keeps_numeric_failure_details(self):
        modules, _ = self.fake_runtime()
        bad = score_fake_logits([2.0, 0.0], 1)
        case = {"request_id": "a", "passed": False, "positions": [bad] * 8}
        with mock.patch.dict(sys.modules, modules), mock.patch.object(
            correctness, "_evaluate_case", return_value=case
        ), mock.patch.object(correctness, "_write_report", side_effect=OSError("disk full")):
            with self.assertRaises(correctness.CorrectnessError) as caught:
                correctness.evaluate_records(self.model_dir, [record("a", 8)], self.output_path)
        result = caught.exception.report
        self.assertFalse(result["passed"])
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["summary"]["failed_positions"], 8)
        self.assertIn("校验未通过", str(caught.exception))
        self.assertIn("报告保存也失败", str(caught.exception))

    def test_nonfinite_input_error_report_is_valid_json(self):
        candidate = record(generated=8)
        candidate["token_logprobs"][0] = float("nan")
        with self.assertRaises(correctness.CorrectnessError):
            correctness.evaluate_records(self.model_dir, [candidate], self.output_path)
        self.assertNotIn("NaN", self.output_path.read_text(encoding="utf-8"))

    def test_success_uses_local_fp32_eager_and_preserves_fixed_thresholds(self):
        modules, loader = self.fake_runtime()
        good = score_fake_logits([2.0, 0.0], 0)
        cases = [
            {"request_id": "a", "passed": True, "positions": [good] * 8},
            {"request_id": "b", "passed": True, "positions": [good] * 8},
        ]
        with mock.patch.dict(sys.modules, modules), mock.patch.object(
            correctness, "_evaluate_case", side_effect=cases
        ) as evaluate, mock.patch("builtins.print") as output:
            result = correctness.evaluate_records(
                self.model_dir, [record("a", 8), record("b", 8)], self.output_path
            )
        output.assert_not_called()
        self.assertTrue(result["passed"])
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["summary"]["evaluated_positions"], 16)
        self.assertEqual([call.args[2]["request_id"] for call in evaluate.call_args_list], ["a", "b"])
        self.assertFalse(result["reference"]["performance_measurement"])
        self.assertEqual(result["reference"]["backend"], "torch_dense_cpu_fp32")
        self.assertIn("backend_fallback_reason", result["reference"])
        self.assertEqual(result["reference"]["tensor_validation"]["parameter_tensors"], 1)
        self.assertEqual(result["thresholds"]["logprob_abs_diff_max_nats"], 0.25)
        self.assertEqual(result["thresholds"]["greedy_logprob_gap_max_nats"], 0.10)
        loader.assert_called_once_with(
            str(self.model_dir.resolve()), local_files_only=True, trust_remote_code=False,
            torch_dtype="float32", attn_implementation="eager",
        )
        self.assertEqual(json.loads(self.output_path.read_text(encoding="utf-8")), result)

    def test_optional_progress_flushes_stages_without_token_data(self):
        modules, _ = self.fake_runtime()
        good = score_fake_logits([2.0, 0.0], 0)
        case = {"request_id": "a", "passed": True, "positions": [good] * 8}
        with mock.patch.dict(sys.modules, modules), mock.patch.object(
            correctness, "_evaluate_case", return_value=case
        ), mock.patch("builtins.print") as output:
            correctness.evaluate_records(
                self.model_dir, [record("a", 8)], self.output_path, progress=True
            )
        events = []
        for call in output.call_args_list:
            self.assertEqual(call.kwargs, {"flush": True})
            message = call.args[0]
            self.assertTrue(message.startswith("W4_REFERENCE "))
            fields = json.loads(message[len("W4_REFERENCE "):])
            self.assertFalse({"prompt_token_ids", "token_ids", "positions", "token_logprobs"}.intersection(fields))
            events.append(fields["event"])
        self.assertEqual(events, [
            "reference_load_started", "reference_load_completed", "reference_backend_configured",
            "reference_case_started", "reference_case_completed",
            "reference_report_saving", "reference_report_saved",
        ])

    def test_bad_position_saves_failed_report_and_raises(self):
        modules, _ = self.fake_runtime()
        good = score_fake_logits([2.0, 0.0], 0)
        bad = score_fake_logits([2.0, 0.0], 1)
        case = {"request_id": "a", "passed": False, "positions": [good] * 7 + [bad]}
        with mock.patch.dict(sys.modules, modules), mock.patch.object(
            correctness, "_evaluate_case", return_value=case
        ), self.assertRaises(correctness.CorrectnessError) as caught:
            correctness.evaluate_records(self.model_dir, [record("a", 8)], self.output_path)
        result = caught.exception.report
        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["passed"])
        self.assertEqual(result["summary"]["failed_positions"], 1)
        self.assertEqual(json.loads(self.output_path.read_text(encoding="utf-8")), result)


HAS_REFERENCE_RUNTIME = all(
    importlib.util.find_spec(package) is not None for package in ("torch", "transformers")
)


@unittest.skipUnless(importlib.util.find_spec("torch") is not None, "未安装 torch；不下载依赖")
class OneDnnLinearSemanticTests(unittest.TestCase):
    def test_only_linear_layers_change_and_fp32_outputs_match_dense(self):
        import torch

        torch.set_num_threads(1)
        torch.manual_seed(79)
        model = torch.nn.Sequential(
            torch.nn.Linear(16, 24), torch.nn.LayerNorm(24), torch.nn.SiLU(),
            torch.nn.Linear(24, 12, bias=False),
        ).float().eval()
        unchanged_layer = model[1]
        inputs = torch.randn(2, 7, 16, dtype=torch.float32)
        with torch.inference_mode():
            dense = model(inputs)
        info = correctness.configure_cpu_reference_backend(model, torch)
        if info["backend"] != "onednn_linear_cpu_fp32":
            self.skipTest(info["backend_fallback_reason"])
        self.assertIs(model[1], unchanged_layer)
        self.assertEqual(info["linear_count"], 2)
        self.assertEqual(info["converted_linear_count"], 2)
        self.assertEqual(info["mkldnn_matmul_fp32_precision"], "ieee")
        self.assertGreater(info["tensor_validation"]["mkldnn_buffer_tensors"], 0)
        self.assertTrue(all(t.dtype == torch.float32 for t in model.buffers() if t.is_floating_point()))
        with torch.inference_mode():
            converted = model(inputs)
        torch.testing.assert_close(converted, dense, rtol=1e-5, atol=1e-6)


@unittest.skipUnless(HAS_REFERENCE_RUNTIME, "未安装 torch/transformers；不下载依赖")
class TinyQwen2SemanticTests(unittest.TestCase):
    def test_hidden_slice_matches_independent_causal_prefix_predictions(self):
        import torch
        from transformers import Qwen2Config, Qwen2ForCausalLM

        torch.set_num_threads(1)
        torch.manual_seed(73)
        config = Qwen2Config(
            vocab_size=17, hidden_size=16, intermediate_size=32,
            num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=2,
            max_position_embeddings=64, bos_token_id=0, eos_token_id=1,
        )
        config._attn_implementation = "eager"
        model = Qwen2ForCausalLM(config).float().eval()
        candidate = {
            "request_id": "tiny-cpu-only", "prompt_token_ids": [2, 3, 4],
            "token_ids": [5, 6, 7], "token_logprobs": [],
        }
        reference_rows = []
        with torch.inference_mode():
            # 每次只提供已经出现的真实前缀，用完整 causal LM forward 的最后位置作独立对照。
            for index, token_id in enumerate(candidate["token_ids"]):
                prefix = candidate["prompt_token_ids"] + candidate["token_ids"][:index]
                logits = model(torch.tensor([prefix]), use_cache=False).logits[0, -1]
                logprobs = torch.log_softmax(logits, dim=-1)
                candidate["token_logprobs"].append(float(logprobs[token_id]))
                reference_rows.append(logprobs)
        result = correctness._evaluate_case(model, torch, candidate)
        self.assertEqual([row["input_position"] for row in result["positions"]], [2, 3, 4])
        for index, row in enumerate(result["positions"]):
            self.assertAlmostEqual(row["reference_logprob"], candidate["token_logprobs"][index], places=5)
            self.assertEqual(row["reference_top1_id"], int(reference_rows[index].argmax()))
            self.assertTrue(row["probability_passed"])

    def test_onednn_qwen2_matches_dense_teacher_forced_probabilities(self):
        import torch
        from transformers import Qwen2Config, Qwen2ForCausalLM

        torch.set_num_threads(1)
        torch.manual_seed(83)
        config = Qwen2Config(
            vocab_size=19, hidden_size=16, intermediate_size=32,
            num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=2,
            max_position_embeddings=64, bos_token_id=0, eos_token_id=1,
        )
        config._attn_implementation = "eager"
        model = Qwen2ForCausalLM(config).float().eval()
        prompt = [2, 3, 4, 5]
        generated = []
        server_logprobs = []
        with torch.inference_mode():
            # 用未转换的 CPU FP32 causal LM 生成可逐位置核对的贪心序列。
            for _ in range(8):
                logits = model(torch.tensor([prompt + generated]), use_cache=False).logits[0, -1]
                logprobs = torch.log_softmax(logits, dim=-1)
                token_id = int(logprobs.argmax())
                generated.append(token_id)
                server_logprobs.append(float(logprobs[token_id]))
        candidate = {
            "request_id": "tiny-onednn-cpu-only", "prompt_token_ids": prompt,
            "token_ids": generated, "token_logprobs": server_logprobs,
        }
        dense = correctness._evaluate_case(model, torch, candidate)
        original_attention = model.model.layers[0].self_attn
        info = correctness.configure_cpu_reference_backend(model, torch)
        if info["backend"] != "onednn_linear_cpu_fp32":
            self.skipTest(info["backend_fallback_reason"])
        self.assertEqual(model.config._attn_implementation, "eager")
        self.assertIs(model.model.layers[0].self_attn, original_attention)
        self.assertEqual(info["mkldnn_matmul_fp32_precision"], "ieee")
        converted = correctness._evaluate_case(model, torch, candidate)
        self.assertTrue(dense["passed"])
        self.assertTrue(converted["passed"])
        for expected, actual in zip(dense["positions"], converted["positions"]):
            self.assertEqual(actual["input_position"], expected["input_position"])
            self.assertEqual(actual["reference_top1_id"], expected["reference_top1_id"])
            self.assertAlmostEqual(actual["reference_logprob"], expected["reference_logprob"], places=5)
            self.assertAlmostEqual(actual["reference_top1_logprob"], expected["reference_top1_logprob"], places=5)


if __name__ == "__main__":
    unittest.main()
