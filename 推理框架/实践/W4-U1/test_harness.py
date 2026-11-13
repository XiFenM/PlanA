"""W4-U1 测量合同测试；不需要 GPU，不把本测试记为 GPU 实测。

运行：PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s <本目录> -v
真实张量检查需要 CPU 可用的 PyTorch；缺少依赖时明确跳过。
"""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest import mock


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

if importlib.util.find_spec("torch") is None:
    torch = None
else:
    import torch  # noqa: E402


def valid_samples():
    """两种 shape 的五个区间均值，刻意打乱大小以区分均值和中位数。"""
    means = {128: [1.0, 2.0, 3.0, 4.0, 20.0], 256: [5.0, 6.0, 7.0, 8.0, 30.0]}
    samples = []
    for index in range(5):
        shapes = (128, 256) if index % 2 == 0 else (256, 128)
        for order, m in enumerate(shapes):
            mean = means[m][index]
            samples.append(
                {
                    "round": index,
                    "order": order,
                    "m": m,
                    "calls": 20,
                    "total_ms": mean * 20,
                    "mean_ms": mean,
                }
            )
    return samples


class WorkloadContractTests(unittest.TestCase):
    def test_frozen_contract(self):
        expected = {
            "ms": [128, 256],
            "k": 5120,
            "n": 25600,
            "seed": 20261110,
            "warmup": 20,
            "rounds": 5,
            "calls_per_sample": 20,
        }
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(harness.CONTRACT[key], value)

    def test_small_rectangular_problem_has_three_bf16_tensors(self):
        actual = harness.workload(2, k=3, n=5)
        self.assertEqual(actual["flops"], 60)
        self.assertEqual(actual["a_bytes"], 12)
        self.assertEqual(actual["b_bytes"], 30)
        self.assertEqual(actual["c_bytes"], 20)
        self.assertEqual(actual["q0_bytes"], 62)
        self.assertAlmostEqual(actual["ai0_flop_per_byte"], 60 / 62)

    def test_changing_m_preserves_b_instead_of_doubling_all_traffic(self):
        small, large = harness.workload(128), harness.workload(256)
        self.assertEqual(small["flops"], 33_554_432_000)
        self.assertEqual(large["flops"], 67_108_864_000)
        self.assertEqual(small["q0_bytes"], 270_008_320)
        self.assertEqual(large["q0_bytes"], 277_872_640)
        self.assertEqual(large["b_bytes"], small["b_bytes"])
        self.assertEqual(large["a_bytes"], 2 * small["a_bytes"])
        self.assertEqual(large["c_bytes"], 2 * small["c_bytes"])
        self.assertLess(large["q0_bytes"], 2 * small["q0_bytes"])

    def test_round_order_alternates_without_adding_a_shape(self):
        self.assertEqual(
            [harness.round_order(i) for i in range(5)],
            [(128, 256), (256, 128), (128, 256), (256, 128), (128, 256)],
        )


class SummaryContractTests(unittest.TestCase):
    def test_medians_units_and_unmeasured_q_are_preserved(self):
        samples = valid_samples()
        before = copy.deepcopy(samples)
        result = harness.summarize(samples)
        self.assertEqual(samples, before, "汇总不能修改原始样本")
        self.assertEqual(result["sample_count"], 10)
        self.assertEqual(result["samples_per_shape"], 5)
        self.assertIsInstance(result["timing_scope"], str)
        self.assertTrue(result["timing_scope"].strip())
        self.assertEqual(set(result["by_m"]), {"128", "256"})
        for m, median, minimum, maximum in ((128, 3.0, 1.0, 20.0), (256, 7.0, 5.0, 30.0)):
            with self.subTest(m=m):
                row = result["by_m"][str(m)]
                self.assertEqual(row["mean_ms_median"], median)
                self.assertEqual(row["mean_ms_min"], minimum)
                self.assertEqual(row["mean_ms_max"], maximum)
                # 独立的已核工作量；毫秒转换为秒，TFLOP/s 与 GB/s 用十进制。
                flops, q0 = {
                    128: (33_554_432_000, 270_008_320),
                    256: (67_108_864_000, 277_872_640),
                }[m]
                self.assertAlmostEqual(row["useful_tflops"], flops / (median / 1000) / 1e12)
                self.assertAlmostEqual(row["q0_effective_gb_s"], q0 / (median / 1000) / 1e9)
                self.assertIsNone(row["q_actual_bytes"])
        json.dumps(result, allow_nan=False)

    def test_rejects_incomplete_and_duplicate_observations(self):
        whole = valid_samples()
        cases = {
            "empty": [],
            "one_sample_missing": whole[:-1],
            "one_shape_missing": [s for s in whole if s["m"] == 128],
            "duplicate_round_shape": whole[:-1] + [copy.deepcopy(whole[0])],
        }
        for name, samples in cases.items():
            with self.subTest(case=name), self.assertRaises(ValueError):
                harness.summarize(samples)

    def test_rejects_malformed_sample_metadata(self):
        changes = [
            ("m", 64),
            ("m", True),
            ("m", 128.0),
            ("round", -1),
            ("round", 5),
            ("round", 1.5),
            ("order", -1),
            ("order", 2),
            ("order", 1),  # 第一轮 M=128 必须先执行。
            ("order", 0.0),
            ("order", False),
            ("calls", 0),
            ("calls", 19),
            ("calls", 20.0),
            ("calls", 20.5),
            ("calls", True),
        ]
        for field, value in changes:
            samples = valid_samples()
            samples[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                harness.summarize(samples)
        samples = valid_samples()
        del samples[0]["total_ms"]
        with self.assertRaises(ValueError):
            harness.summarize(samples)

    def test_rejects_nonpositive_nonfinite_or_inconsistent_times(self):
        for field in ("total_ms", "mean_ms"):
            for value in (0.0, -1.0, math.nan, math.inf, -math.inf):
                samples = valid_samples()
                samples[0][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    harness.summarize(samples)
        samples = valid_samples()
        samples[0]["mean_ms"] = 2.0  # total=20、calls=20，不应被当成 2 ms。
        with self.assertRaises(ValueError):
            harness.summarize(samples)


class _FakeEvent:
    def __init__(self, owner, name):
        self.owner, self.name = owner, name

    def record(self, *args, **kwargs):
        self.owner.log.append(self.name + ".record")

    def synchronize(self):
        self.owner.log.append(self.name + ".synchronize")

    def elapsed_time(self, end):
        if self.name != "start" or end.name != "end":
            raise AssertionError("必须计算 start 到 end 的设备事件间隔")
        self.owner.log.append("start.elapsed_time")
        return self.owner.total_ms


class _FakeCuda:
    def __init__(self, owner):
        self.owner = owner
        self.event_count = 0

    def synchronize(self, *args, **kwargs):
        self.owner.log.append("device.synchronize")

    def Event(self, *, enable_timing=False, **kwargs):
        if not enable_timing:
            raise AssertionError("计时事件必须启用 timing")
        self.event_count += 1
        if self.event_count > 2:
            raise AssertionError("一个区间只需两个事件，不能改变采样单位")
        return _FakeEvent(self.owner, "start" if self.event_count == 1 else "end")

    def current_stream(self, *args, **kwargs):
        return None


class _FakeTorch:
    """只模拟可观察的设备计时协议，不模拟张量运算或性能。"""

    def __init__(self, total_ms=8.0):
        self.log = []
        self.total_ms = total_ms
        self.cuda = _FakeCuda(self)
        self.a = SimpleNamespace(device="cuda:0")
        self.b = SimpleNamespace(device="cuda:0")
        self.out = SimpleNamespace(device="cuda:0")

    def mm(self, a, b, *, out):
        if a is not self.a or b is not self.b or out is not self.out:
            raise AssertionError("区间内必须复用调用方提供的输入与输出")
        self.log.append("mm")
        return out

    @staticmethod
    def no_grad():
        return contextlib.nullcontext()

    @staticmethod
    def inference_mode():
        return contextlib.nullcontext()


class TimingContractTests(unittest.TestCase):
    def test_device_interval_is_synchronized_and_output_is_reused(self):
        fake = _FakeTorch(total_ms=8.0)
        result = harness.measure_one(fake, fake.a, fake.b, fake.out, calls=4)
        self.assertEqual(
            fake.log,
            ["device.synchronize", "start.record"]
            + ["mm"] * 4
            + ["end.record", "end.synchronize", "start.elapsed_time"],
        )
        self.assertEqual(result["total_ms"], 8.0)
        self.assertEqual(result["calls"], 4)
        self.assertEqual(result["mean_ms"], 2.0)

    def test_rejects_invalid_call_counts_before_device_work(self):
        for calls in (0, -1, 1.5, True, "20"):
            fake = _FakeTorch()
            with self.subTest(calls=calls), self.assertRaises((ValueError, TypeError)):
                harness.measure_one(fake, fake.a, fake.b, fake.out, calls=calls)
            self.assertNotIn("mm", fake.log)

    def test_rejects_unusable_event_measurements(self):
        for total in (0.0, -1.0, math.nan, math.inf, -math.inf):
            fake = _FakeTorch(total_ms=total)
            with self.subTest(total_ms=total), self.assertRaises(ValueError):
                harness.measure_one(fake, fake.a, fake.b, fake.out, calls=4)


class ArtifactContractTests(unittest.TestCase):
    def test_concurrent_runs_get_distinct_exclusive_directories(self):
        with tempfile.TemporaryDirectory(prefix="w4-u1-output-test-") as tmp:
            root = Path(tmp)
            with ThreadPoolExecutor(max_workers=6) as pool:
                paths = list(pool.map(lambda _: harness.new_run_dir(root, "preflight"), range(12)))
            self.assertEqual(len(set(paths)), 12)
            for path in paths:
                self.assertIsInstance(path, Path)
                self.assertTrue(path.is_dir())
                self.assertEqual(path.parent.resolve(), root.resolve())
                self.assertTrue(path.name.startswith("preflight"))

    def test_json_roundtrip_and_existing_result_is_never_overwritten(self):
        with tempfile.TemporaryDirectory(prefix="w4-u1-json-test-") as tmp:
            path = Path(tmp) / "result.json"
            payload = {"说明": "这是合同测试，不是 GPU 实测", "q_actual_bytes": None, "samples": [1, 2, 3]}
            harness.write_json(path, payload)
            before = path.read_bytes()
            self.assertEqual(json.loads(before), payload)
            with self.assertRaises(FileExistsError):
                harness.write_json(path, {"replacement": True})
            self.assertEqual(path.read_bytes(), before)

    def test_json_rejects_nonfinite_numbers(self):
        with tempfile.TemporaryDirectory(prefix="w4-u1-json-test-") as tmp:
            for index, value in enumerate((math.nan, math.inf, -math.inf)):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    harness.write_json(Path(tmp) / f"invalid-{index}.json", {"nested": [value]})


@unittest.skipIf(torch is None, "未安装 CPU 可用 PyTorch，跳过真实张量检查")
class NumericContractTests(unittest.TestCase):
    def tensor(self, values, dtype=None):
        return torch.tensor(values, dtype=dtype or torch.float64)

    def test_exact_output_and_small_rounding_error_pass(self):
        reference = self.tensor([[1.0, -2.0], [0.25, 3.0]])
        for actual in (reference.clone(), reference + 0.0005):
            with self.subTest(exact=torch.equal(actual, reference)):
                result = harness.correctness_metrics(actual, reference, torch)
                self.assertTrue(result["finite"])
                self.assertTrue(result["passed"])
                self.assertAlmostEqual(result["max_abs_reference"], 3.0)
                self.assertAlmostEqual(result["max_abs_limit"], 0.031)
                json.dumps(result, allow_nan=False)

    def test_wrong_output_fails(self):
        result = harness.correctness_metrics(torch.zeros(3, 4), torch.ones(3, 4), torch)
        self.assertTrue(result["finite"])
        self.assertFalse(result["passed"])
        self.assertAlmostEqual(result["relative_l2"], 1.0)

    def test_relative_l2_is_required_even_when_absolute_limit_passes(self):
        reference = torch.ones(100, dtype=torch.float64)
        result = harness.correctness_metrics(reference + 0.0105, reference, torch)
        self.assertLess(result["max_abs_error"], result["max_abs_limit"])
        self.assertGreater(result["relative_l2"], 0.01)
        self.assertFalse(result["passed"])

    def test_absolute_limit_is_required_even_when_relative_l2_passes(self):
        reference = torch.ones(1000, dtype=torch.float64)
        actual = reference.clone()
        actual[0] += 0.02
        result = harness.correctness_metrics(actual, reference, torch)
        self.assertLess(result["relative_l2"], 0.01)
        self.assertGreater(result["max_abs_error"], result["max_abs_limit"])
        self.assertFalse(result["passed"])

    def test_nonfinite_actual_or_reference_fails_and_remains_json_safe(self):
        for value in (math.nan, math.inf, -math.inf):
            for side in ("actual", "reference"):
                actual, reference = self.tensor([1.0, 2.0]), self.tensor([1.0, 2.0])
                (actual if side == "actual" else reference)[0] = value
                with self.subTest(value=value, side=side):
                    result = harness.correctness_metrics(actual, reference, torch)
                    self.assertFalse(result["finite"])
                    self.assertFalse(result["passed"])
                    json.dumps(result, allow_nan=False)

    def test_zero_reference_never_hides_nonzero_output(self):
        reference = torch.zeros(4, dtype=torch.float64)
        exact = harness.correctness_metrics(reference.clone(), reference, torch)
        self.assertTrue(exact["passed"])
        self.assertEqual(exact["relative_l2"], 0.0)
        wrong = harness.correctness_metrics(reference + 1e-6, reference, torch)
        self.assertTrue(wrong["finite"])
        self.assertFalse(wrong["passed"])
        json.dumps(wrong, allow_nan=False)

    def test_error_reduction_survives_float32_underflow_and_overflow(self):
        tiny = self.tensor([1e-30, -1e-30], dtype=torch.float32)
        result = harness.correctness_metrics(2 * tiny, tiny, torch)
        self.assertAlmostEqual(result["relative_l2"], 1.0)
        self.assertFalse(result["passed"])
        large = self.tensor([1e20, -1e20], dtype=torch.float32)
        result = harness.correctness_metrics(large * 1.005, large, torch)
        self.assertTrue(math.isfinite(result["relative_l2"]))
        self.assertAlmostEqual(result["relative_l2"], 0.005, places=5)
        self.assertTrue(result["passed"])

    def test_shape_mismatch_cannot_pass_by_broadcasting(self):
        actual = self.tensor([[1.0], [2.0]])
        reference = self.tensor([[1.0, 1.0], [2.0, 2.0]])
        with self.assertRaises(ValueError):
            harness.correctness_metrics(actual, reference, torch)

    def test_inputs_use_private_cpu_rng_bf16_and_preallocated_shapes(self):
        state_before = torch.random.get_rng_state().clone()
        a, b, outputs = harness.prepare_inputs(torch, "cpu", m=8, k=5, n=7, seed=17)
        self.assertTrue(torch.equal(torch.random.get_rng_state(), state_before))
        a2, b2, _ = harness.prepare_inputs(torch, "cpu", m=8, k=5, n=7, seed=17)
        self.assertTrue(torch.equal(a, a2))
        self.assertTrue(torch.equal(b, b2))
        self.assertEqual(tuple(a.shape), (8, 5))
        self.assertEqual(tuple(b.shape), (5, 7))
        self.assertEqual(set(outputs), {4, 8})
        for tensor in (a, b, *outputs.values()):
            self.assertEqual(tensor.dtype, torch.bfloat16)
            self.assertTrue(tensor.is_contiguous())
            self.assertFalse(tensor.requires_grad)
        self.assertEqual(tuple(outputs[4].shape), (4, 7))
        self.assertEqual(tuple(outputs[8].shape), (8, 7))
        self.assertNotEqual(outputs[4].data_ptr(), outputs[8].data_ptr())
        # 从相同 CPU 随机流独立恢复输入，检查先缩放、再转换 BF16 的顺序。
        generator = torch.Generator(device="cpu").manual_seed(17)
        expected_a = (torch.randn(8, 5, generator=generator, dtype=torch.float32) / math.sqrt(5)).to(torch.bfloat16)
        expected_b = torch.randn(5, 7, generator=generator, dtype=torch.float32).to(torch.bfloat16)
        self.assertTrue(torch.equal(a, expected_a))
        self.assertTrue(torch.equal(b, expected_b))
        self.assertTrue(a[:4].is_contiguous())
        self.assertEqual(a[:4].data_ptr(), a.data_ptr())

    def test_tiny_cpu_matmul_checks_every_output_against_promoted_inputs(self):
        a, b, outputs = harness.prepare_inputs(torch, "cpu", m=8, k=5, n=7, seed=17)
        for m, out in outputs.items():
            with self.subTest(m=m):
                pointer = out.data_ptr()
                torch.mm(a[:m], b, out=out)
                reference = torch.mm(a[:m].float(), b.float())
                result = harness.correctness_metrics(out, reference, torch)
                self.assertTrue(result["passed"], result)
                self.assertEqual(out.data_ptr(), pointer)


class _NewPrecisionSettings(SimpleNamespace):
    """一旦混用旧 TF32 API，测试立即失败，而非返回一个看似合理的值。"""

    def __getattribute__(self, name):
        if name == "allow_tf32":
            raise AssertionError("不能读取旧 allow_tf32 设置")
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == "allow_tf32":
            raise AssertionError("不能写入旧 allow_tf32 设置")
        super().__setattr__(name, value)


VERIFIED_213_GIT = "cf30153c4c131c8164ee7798e5022d810682e2cb"


class PrecisionSourceTests(unittest.TestCase):
    def test_stable_29_patch_builds_keep_the_existing_baseline(self):
        for version in ("2.9.0", "2.9.0+cu128", "2.9.1+cu128", "2.9.2+cpu"):
            with self.subTest(version=version):
                source = harness.precision_source(version, None)
                self.assertIsInstance(source, str)
                self.assertTrue(source.strip())

    def test_29_prerelease_and_development_builds_are_not_stable_releases(self):
        for version in ("2.9.0a0", "2.9.0a0+git123", "2.9.0.dev20261110", "2.9.0rc1"):
            with self.subTest(version=version):
                self.assertIsNone(harness.precision_source(version, VERIFIED_213_GIT))

    def test_exact_213_version_and_git_have_an_explicit_source(self):
        for version in ("2.13.0", "2.13.0+cu130"):
            with self.subTest(version=version):
                source = harness.precision_source(version, VERIFIED_213_GIT)
                self.assertIsInstance(source, str)
                self.assertTrue(source.strip())

    def test_213_cannot_be_authorized_by_the_version_label_alone(self):
        for git_version in (None, "", "Unknown", "0" * 40, VERIFIED_213_GIT[:-1]):
            with self.subTest(git_version=git_version):
                self.assertIsNone(harness.precision_source("2.13.0+cu130", git_version))

    def test_matching_git_does_not_authorize_other_213_versions(self):
        for version in ("2.13.1", "2.13.1+cu130", "2.13.0a0", "2.13.0rc1", "2.13.0.dev20261110"):
            with self.subTest(version=version):
                self.assertIsNone(harness.precision_source(version, VERIFIED_213_GIT))


def fake_environment_torch(
    *, version="2.9.0+cu128", git_version="SIMULATED-build-id",
    hip=None, capability=(8, 0), native_bf16=True,
):
    """仅为环境分流构造假设备；不能产生任何真实性能或硬件验证结论。"""
    matmul = _NewPrecisionSettings(
        fp32_precision="tf32", allow_bf16_reduced_precision_reduction=True
    )
    backends = _NewPrecisionSettings(
        fp32_precision="tf32", cuda=SimpleNamespace(matmul=matmul)
    )
    cuda = SimpleNamespace(
        is_available=lambda: True,
        device_count=lambda: 1,
        set_device=lambda index: None,
        get_device_properties=lambda index: SimpleNamespace(
            name="SIMULATED GPU — contract test only",
            major=capability[0],
            total_memory=8 * 1024**3,
            multi_processor_count=4,
            uuid="SIMULATED-UUID",
        ),
        mem_get_info=lambda index: (6 * 1024**3, 8 * 1024**3),
        get_device_capability=lambda: capability,
        is_bf16_supported=lambda *, including_emulation: native_bf16,
    )
    return SimpleNamespace(
        __version__=version,
        version=SimpleNamespace(
            git_version=git_version, cuda=None if hip else "12.8", hip=hip
        ),
        __config__=SimpleNamespace(show=lambda: "SIMULATED build metadata"),
        cuda=cuda,
        backends=backends,
        get_float32_matmul_precision=mock.Mock(
            side_effect=AssertionError("不能读取旧 get_float32_matmul_precision API")
        ),
        set_float32_matmul_precision=mock.Mock(
            side_effect=AssertionError("不能写入旧 set_float32_matmul_precision API")
        ),
    )


class EnvironmentContractTests(unittest.TestCase):
    def collect(self, fake, overrides=None):
        driver = {"returncode": 0, "stdout": "SIMULATED driver metadata", "stderr": ""}
        with (
            mock.patch.object(harness.importlib, "import_module", return_value=fake) as importer,
            mock.patch.object(harness, "command_snapshot", return_value=driver),
            mock.patch.dict(os.environ, overrides or {}, clear=True),
        ):
            environment, module = harness.collect_environment(0)
        importer.assert_called_once_with("torch")
        self.assertIs(module, fake)
        fake.get_float32_matmul_precision.assert_not_called()
        fake.set_float32_matmul_precision.assert_not_called()
        json.dumps(environment, allow_nan=False)
        return environment

    def assert_blocked(self, environment, reason=None):
        self.assertEqual(environment["status"], "blocked")
        self.assertIsNone(environment["precision"])
        self.assertTrue(environment["errors"])
        if reason is not None:
            self.assertIn(reason, " ".join(environment["errors"]))

    def test_qualified_fake_cuda_only_reaches_ready_for_prediction(self):
        fake = fake_environment_torch()
        environment = self.collect(fake)
        self.assertEqual(environment["status"], "ready_for_prediction")
        self.assertEqual(environment["errors"], [])
        self.assertEqual(environment["device"]["capability"], [8, 0])
        self.assertEqual(fake.backends.fp32_precision, "ieee")
        self.assertEqual(fake.backends.cuda.matmul.fp32_precision, "ieee")
        self.assertIs(fake.backends.cuda.matmul.allow_bf16_reduced_precision_reduction, False)
        self.assertEqual(
            environment["precision_source"],
            harness.precision_source(fake.__version__, fake.version.git_version),
        )
        self.assertTrue(environment["precision_source"])

    def test_verified_213_fake_reaches_ready_with_new_ieee_settings_and_source(self):
        fake = fake_environment_torch(version="2.13.0+cu130", git_version=VERIFIED_213_GIT)
        fake.version.cuda = "13.0"
        environment = self.collect(fake)
        self.assertEqual(environment["status"], "ready_for_prediction")
        self.assertEqual(environment["errors"], [])
        self.assertEqual(environment["torch_version"], "2.13.0+cu130")
        self.assertEqual(environment["torch_git_version"], VERIFIED_213_GIT)
        self.assertEqual(environment["precision_source"], harness.precision_source("2.13.0+cu130", VERIFIED_213_GIT))
        self.assertTrue(environment["precision_source"])
        self.assertEqual(environment["precision"]["global_fp32_precision"], "ieee")
        self.assertEqual(environment["precision"]["matmul_fp32_precision"], "ieee")
        self.assertIs(environment["precision"]["allow_bf16_reduced_precision_reduction"], False)

    def test_environment_uses_source_check_as_a_fail_closed_gate(self):
        fake = fake_environment_torch()
        with mock.patch.object(harness, "precision_source", return_value=None) as source:
            environment = self.collect(fake)
        source.assert_called_once_with(fake.__version__, fake.version.git_version)
        self.assert_blocked(environment)
        self.assertIsNone(environment["precision_source"])

    def test_unverified_213_or_prerelease_metadata_stays_blocked(self):
        cases = [
            ("2.13.0+cu130", None),
            ("2.13.0+cu130", "0" * 40),
            ("2.13.1+cu130", VERIFIED_213_GIT),
            ("2.13.0.dev20261110", VERIFIED_213_GIT),
            ("2.9.0a0", VERIFIED_213_GIT),
            ("2.9.0.dev20261110", VERIFIED_213_GIT),
            ("2.9.0rc1", VERIFIED_213_GIT),
        ]
        for version, git_version in cases:
            with self.subTest(version=version, git_version=git_version):
                environment = self.collect(fake_environment_torch(version=version, git_version=git_version))
                self.assert_blocked(environment)
                self.assertIsNone(environment["precision_source"])

    def test_rocm_is_recorded_but_cannot_enter_unverified_measurement(self):
        environment = self.collect(fake_environment_torch(hip="6.4.0"))
        self.assertEqual(environment["hip_runtime"], "6.4.0")
        self.assert_blocked(environment, "ROCm")

    def test_unverified_torch_versions_remain_blocked(self):
        for version in ("2.8.0+cu128", "2.10.0+cu128", "3.0.0"):
            with self.subTest(version=version):
                self.assert_blocked(self.collect(fake_environment_torch(version=version)))

    def test_either_tf32_override_blocks_the_reference_path(self):
        for name in ("NVIDIA_TF32_OVERRIDE", "TORCH_ALLOW_TF32_CUBLAS_OVERRIDE"):
            with self.subTest(variable=name):
                self.assert_blocked(self.collect(fake_environment_torch(), {name: "1"}), name)

    def test_old_capability_and_emulated_only_bf16_remain_blocked(self):
        for kwargs in ({"capability": (7, 5)}, {"native_bf16": False}):
            with self.subTest(condition=kwargs):
                self.assert_blocked(self.collect(fake_environment_torch(**kwargs)), "BF16")

    def test_precision_configuration_failure_does_not_become_ready(self):
        fake = fake_environment_torch()
        with mock.patch.object(harness, "configure_precision", side_effect=RuntimeError("test readback failed")):
            self.assert_blocked(self.collect(fake), "test readback failed")


class MissingTorchCliTests(unittest.TestCase):
    def run_without_torch(self, directory, *args):
        # 隔离导入，使这些检查在安装 PyTorch 的机器上同样测试缺依赖路径。
        blocker = directory / "import-blocker"
        blocker.mkdir(exist_ok=True)
        (blocker / "torch.py").write_text(
            'raise ModuleNotFoundError("No module named torch (test isolation)", name="torch")\n',
            encoding="utf-8",
        )
        env = os.environ.copy()
        env["PYTHONPATH"] = str(blocker)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, "-S", str(HERE / "harness.py"), *args],
            cwd=directory,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_help_does_not_require_torch(self):
        with tempfile.TemporaryDirectory(prefix="w4-u1-cli-test-") as tmp:
            result = self.run_without_torch(Path(tmp), "--help")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("preflight", result.stdout)
            self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_run_requires_an_explicit_device_before_creating_artifacts(self):
        with tempfile.TemporaryDirectory(prefix="w4-u1-cli-test-") as tmp:
            root = Path(tmp) / "results"
            result = self.run_without_torch(Path(tmp), "run", "--prediction", "test only",
                                            "--output-root", str(root))
            self.assertEqual(result.returncode, 2)
            self.assertIn("--device", result.stderr)
            self.assertFalse(root.exists())
            self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_preflight_records_a_clean_blocked_result_without_torch(self):
        with tempfile.TemporaryDirectory(prefix="w4-u1-cli-test-") as tmp:
            directory = Path(tmp)
            output = directory / "results"
            result = self.run_without_torch(directory, "preflight", "--output-root", str(output))
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stdout + result.stderr)
            artifacts = list(output.glob("preflight-*/environment.json"))
            self.assertEqual(len(artifacts), 1, result.stdout + result.stderr)
            payload = json.loads(artifacts[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "blocked")
            self.assertIsInstance(payload["errors"], list)
            self.assertTrue(payload["errors"])
            self.assertIn("torch", json.dumps(payload["errors"], ensure_ascii=False).lower())


if __name__ == "__main__":
    unittest.main()
