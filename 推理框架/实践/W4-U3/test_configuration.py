"""使用模拟管理响应验证投影与实验配置；纯标准库，无 GPU 依赖。"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parent))
from configuration import project_runtime_config, validate_runtime_config


def response(budget=512, profile=False):
    return {
        "vllm_config": {
            "model_config": {
                "model": "/models/qwen-pinned",
                "dtype": "torch.bfloat16",
                "quantization": None,
                "max_model_len": 4096,
                "seed": 20261112,
                "enforce_eager": True,
                "logprobs_mode": "raw_logprobs",
            },
            "parallel_config": {
                "tensor_parallel_size": 1,
                "pipeline_parallel_size": 1,
            },
            "cache_config": {
                "enable_prefix_caching": False,
                "gpu_memory_utilization": 0.7,
                "cache_dtype": "auto",
                "block_size": 16,
                "kv_cache_memory_bytes": None,
            },
            "scheduler_config": {
                "max_num_batched_tokens": budget,
                "max_num_scheduled_tokens": None,
                "max_num_seqs": 16,
                "async_scheduling": False,
                "enable_chunked_prefill": True,
            },
            "speculative_config": None,
            "profiler_config": {
                "profiler": "torch" if profile else None,
                "torch_profiler_dir": "/runs/traces" if profile else "",
                "torch_profiler_use_gzip": True,
                "torch_profiler_with_stack": False,
                "torch_profiler_record_shapes": profile,
                "torch_profiler_with_memory": profile,
                "ignore_frontend": False,
                "detailed_trace_annotation": False,
            },
            "compilation_config": {"mode": 0, "cudagraph_mode": "NONE", "backend": ""},
        },
        "vllm_env": {"VLLM_API_KEY": "never-copy-this-secret"},
        "system_env": {"environment": "never-copy-this-secret"},
    }


class ProjectionTests(unittest.TestCase):
    def test_only_whitelisted_scalars_leave_response(self):
        source = response()
        for group in source["vllm_config"].values():
            if isinstance(group, dict):
                group["hf_token"] = "never-copy-this-secret"
                group["unknown"] = {"api_key": "never-copy-this-secret"}
        source["vllm_config"]["api_key"] = "never-copy-this-secret"
        before = copy.deepcopy(source)
        projected = project_runtime_config(source)
        serialized = json.dumps(projected)
        for forbidden in ("never-copy", "api_key", "hf_token", "vllm_env", "system_env"):
            self.assertNotIn(forbidden, serialized)
        self.assertEqual(source, before)
        self.assertEqual(validate_runtime_config(projected, 512), [])
        projected["model"]["seed"] = 0
        self.assertEqual(source["vllm_config"]["model_config"]["seed"], 20261112)

    def test_json_string_has_same_projection_as_object(self):
        source = response()
        expected = project_runtime_config(source)
        source["vllm_config"] = json.dumps(source["vllm_config"])
        self.assertEqual(project_runtime_config(source), expected)

    def test_default_text_and_invalid_shapes_are_rejected_without_echo(self):
        for source in (
            None, {}, {"vllm_config": None}, {"vllm_config": []},
            {"vllm_config": "VllmConfig(secret='do-not-echo')"},
            {"vllm_config": '"do-not-echo"'},
            {"vllm_config": {"model_config": "do-not-echo"}},
        ):
            with self.subTest(source=source):
                with self.assertRaises(ValueError) as raised:
                    project_runtime_config(source)
                self.assertNotIn("do-not-echo", str(raised.exception))

    def test_nested_secret_in_whitelisted_field_is_rejected(self):
        source = response()
        source["vllm_config"]["profiler_config"]["profiler"] = {
            "api_key": "do-not-echo"
        }
        with self.assertRaisesRegex(ValueError, "profiler.profiler") as raised:
            project_runtime_config(source)
        self.assertNotIn("do-not-echo", str(raised.exception))

    def test_speculative_details_are_reduced_to_boolean(self):
        source = response()
        source["vllm_config"]["speculative_config"] = {
            "model": "do-not-copy", "api_key": "do-not-copy"
        }
        projected = project_runtime_config(source)
        self.assertIs(projected["speculative_enabled"], True)
        self.assertNotIn("do-not-copy", json.dumps(projected))
        self.assertTrue(validate_runtime_config(projected, 512))


class RuntimeValidationTests(unittest.TestCase):
    def test_awq_dtype_and_quantization_are_checked_together(self):
        value = project_runtime_config(response(2048))
        value["model"].update(dtype="torch.float16", quantization="auto_awq")
        self.assertEqual(validate_runtime_config(value, 2048, variant="awq", dtype="float16"), [])
        self.assertTrue(validate_runtime_config(value, 2048, variant="awq", dtype="bfloat16"))
        self.assertTrue(validate_runtime_config(value, 2048, variant="bf16", dtype="float16"))
        value["model"]["quantization"] = None
        self.assertTrue(validate_runtime_config(value, 2048, variant="awq", dtype="float16"))

    def test_expected_budgets_dtypes_and_profiler_modes_pass(self):
        for budget in (512, 2048):
            for dtype in ("bfloat16", "torch.bfloat16"):
                for profile in (False, True):
                    for scheduled in (None, budget):
                        with self.subTest(budget=budget, dtype=dtype, profile=profile):
                            value = project_runtime_config(response(budget, profile))
                            value["model"]["dtype"] = dtype
                            value["scheduler"]["max_num_scheduled_tokens"] = scheduled
                            self.assertEqual(validate_runtime_config(value, budget, profile), [])

    def test_every_required_field_missing_fails(self):
        valid = project_runtime_config(response())
        groups = {
            "model": tuple(valid["model"]),
            "parallel": tuple(valid["parallel"]),
            "cache": tuple(valid["cache"]),
            "scheduler": tuple(valid["scheduler"]),
            "profiler": ("profiler",),
        }
        for group, fields in groups.items():
            for field in fields:
                with self.subTest(group=group, field=field):
                    value = copy.deepcopy(valid)
                    del value[group][field]
                    errors = validate_runtime_config(value, 512)
                    self.assertTrue(any(f"{group}.{field}" in error for error in errors))
        del valid["speculative_enabled"]
        self.assertTrue(validate_runtime_config(valid, 512))

    def test_projection_does_not_supply_missing_defaults(self):
        source = response()
        del source["vllm_config"]["speculative_config"]
        del source["vllm_config"]["scheduler_config"]["max_num_scheduled_tokens"]
        projected = project_runtime_config(source)
        self.assertNotIn("speculative_enabled", projected)
        self.assertNotIn("max_num_scheduled_tokens", projected["scheduler"])
        self.assertEqual(len(validate_runtime_config(projected, 512)), 2)

    def test_bad_values_reject_without_implicit_type_coercion(self):
        cases = (
            ("model", "model", (None, "", "   ", {})),
            ("model", "dtype", ("float16", "float32", None, {})),
            ("model", "max_model_len", (8192, "4096", 4096.0, None)),
            ("model", "seed", (0, "20261112", None)),
            ("model", "enforce_eager", (False, 1, "true", None)),
            ("model", "logprobs_mode", ("raw_logits", "processed_logprobs", None)),
            ("parallel", "tensor_parallel_size", (2, True, "1", None)),
            ("parallel", "pipeline_parallel_size", (2, True, "1", None)),
            ("cache", "enable_prefix_caching", (True, 0, "false", None)),
            ("cache", "gpu_memory_utilization", (0.9, True, "0.7", None, float("nan"), float("inf"))),
            ("scheduler", "max_num_batched_tokens", (2048, "512", 512.0, None)),
            ("scheduler", "max_num_scheduled_tokens", (256, "512", 512.0, False)),
            ("scheduler", "max_num_seqs", (8, "16", 16.0, None)),
            ("scheduler", "async_scheduling", (True, 0, "false", None)),
            ("scheduler", "enable_chunked_prefill", (False, 1, "true", None)),
            ("profiler", "profiler", ("torch", "cuda", False)),
        )
        for group, field, bad_values in cases:
            for bad in bad_values:
                with self.subTest(group=group, field=field, bad=bad):
                    value = project_runtime_config(response())
                    value[group][field] = bad
                    errors = validate_runtime_config(value, 512)
                    self.assertTrue(any(f"{group}.{field}" in error for error in errors))

    def test_invalid_speculative_flags_and_profile_mismatch_fail(self):
        for bad in (None, True, 0, "false", {}):
            value = project_runtime_config(response())
            value["speculative_enabled"] = bad
            self.assertTrue(validate_runtime_config(value, 512))
        self.assertTrue(validate_runtime_config(project_runtime_config(response()), 512, True))

    def test_profile_requires_shape_and_memory_capture(self):
        for field in ("torch_profiler_record_shapes", "torch_profiler_with_memory"):
            value = project_runtime_config(response(profile=True))
            self.assertIs(value["profiler"][field], True)
            value["profiler"][field] = False
            self.assertTrue(validate_runtime_config(value, 512, True))

    def test_bad_arguments_and_malformed_groups_return_errors(self):
        valid = project_runtime_config(response())
        for budget in (None, 0, -1, True, 512.0, "512"):
            self.assertTrue(validate_runtime_config(valid, budget))
        self.assertTrue(validate_runtime_config(valid, 512, "false"))
        self.assertTrue(validate_runtime_config(None, 512))
        for group in ("model", "parallel", "cache", "scheduler", "profiler"):
            for bad in (None, [], "not-an-object"):
                value = copy.deepcopy(valid)
                value[group] = bad
                self.assertTrue(validate_runtime_config(value, 512))


if __name__ == "__main__":
    unittest.main()
