#!/usr/bin/env python3
"""W4-U3-P1：单个真实 AWQ 投影的独立 GPU FP32 实现参考。

不加载模型，不访问网络，不把无 GPU 环境回退成 CPU 推理。可在无 torch
的机器上 import reference_policy()、检查 safetensors 元数据及运行 stdlib 测试。
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import inspect
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from compatibility import PROFILES, profile_for_version


PROJECTION = "model.layers.0.self_attn.q_proj"
AWQ_SHIFTS = (0, 16, 4, 20, 8, 24, 12, 28)
REFERENCE_POLICY = {
    "schema_version": 1,
    "fixture": {
        "repository": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
        "expected_revision": "3ecffa0ceb27851800f45519bab9c457a04405e1",
        "projection": PROJECTION,
        "batch_rows": [1, 256],
        "seed": 20261113,
        "input": "GPU standard normal FP32, then cast to service params dtype",
        "bias": "include checkpoint projection bias when present",
        "production": "vLLM 0.26.0 / 0.33.0 AutoAWQLinearMethod.apply (dense fallback)",
        "source_commits": {v:p["source_commit"] for v,p in PROFILES.items()},
        "reference": "independent AWQ unpack, cast scales and input, GPU FP32 matmul",
        "cpu_compute_fallback": False,
        "reference_tf32": False,
    },
    "metrics": {
        "relative_l2": "norm(actual-reference)/max(norm(reference),1e-12)",
        "max_abs_limit": "atol + max_abs_rms_factor * RMS(reference)",
        "require_finite": True,
    },
    "tolerances": {
        "float16": {"relative_l2": 0.01, "atol": 0.001, "max_abs_rms_factor": 0.05},
        "bfloat16": {"relative_l2": 0.04, "atol": 0.001, "max_abs_rms_factor": 0.20},
    },
    "rationale": (
        "Predeclared implementation-consistency gates for a fixed random fixture; "
        "BF16 has a wider rounding/accumulation allowance. The RMS-scaled maximum "
        "error gate also checks isolated errors without dividing by near-zero "
        "reference elements. These are engineering gates, not worst-case error "
        "bounds, task-quality criteria, or tolerances fitted after execution."
    ),
    "limits": [
        "One projection and two shapes do not validate a whole model or all inputs.",
        "Reference uses the quantized checkpoint, not original BF16 weights.",
        "Checkpoint origin/revision must also be verified by the outer manifest.",
        "This explicitly exercises dense fallback, not automatic whole-model kernel choice.",
    ],
}


def reference_policy() -> dict:
    return copy.deepcopy(REFERENCE_POLICY)


class ReferenceFailure(Exception):
    def __init__(self, message: str, *, status="error", kind="input", stage="input"):
        super().__init__(message)
        self.status, self.kind, self.stage = status, kind, stage


def unpack_awq_word(word: int) -> tuple[int, ...]:
    """独立解释一个 signed/unsigned 32-bit 存储字，不调用生产解量化。"""
    if isinstance(word, bool) or not isinstance(word, int):
        raise ValueError("packed word must be an integer")
    if not -(1 << 31) <= word < (1 << 32):
        raise ValueError("packed word is outside 32-bit storage")
    return tuple((word >> shift) & 15 for shift in AWQ_SHIFTS)


def validate_projection_layout(shapes: dict, k: int, n: int, group_size: int) -> None:
    if k <= 0 or n <= 0 or group_size <= 0 or k % group_size or n % 8:
        raise ReferenceFailure("K/group and N/8 must be positive integral dimensions")
    expected = {
        "qweight": [k, n // 8],
        "qzeros": [k // group_size, n // 8],
        "scales": [k // group_size, n],
    }
    if "bias" in shapes:
        expected["bias"] = [n]
    for name, shape in expected.items():
        if shapes.get(name) != shape:
            raise ReferenceFailure(f"{name}: expected {shape}, got {shapes.get(name)}")


def evaluate_metrics(metrics: dict, dtype: str) -> dict:
    limits = REFERENCE_POLICY["tolerances"][dtype]
    if not metrics.get("finite", False):
        return {"passed": False, "reason": "nonfinite_output", "limits": dict(limits)}
    numbers = [metrics.get(k) for k in ("relative_l2", "max_abs_error", "reference_rms")]
    if any(not isinstance(v, (float, int)) or not math.isfinite(v) or v < 0 for v in numbers):
        return {"passed": False, "reason": "invalid_metrics", "limits": dict(limits)}
    maximum = limits["atol"] + limits["max_abs_rms_factor"] * metrics["reference_rms"]
    checks = {
        "relative_l2": metrics["relative_l2"] <= limits["relative_l2"],
        "max_abs_error": metrics["max_abs_error"] <= maximum,
    }
    return {"passed": all(checks.values()), "checks": checks,
            "limits": {**limits, "max_abs_error": maximum}}


def summarize_cases(cases: list[dict], dtype_name: str) -> dict:
    # Never let an earlier compatibility exception hide a later numeric or
    # resource failure and thereby authorize an inappropriate dtype retry.
    failures = [case for case in cases if case["status"] != "passed"]
    failure = next((case for case in failures if case["status"] == "numerical_failure"), None)
    failure = failure or next((case for case in failures if case.get("failure_kind") != "compatibility"), None)
    failure = failure or next(iter(failures), None)
    if failure:
        return {"status": failure["status"], "failure_kind": failure.get("failure_kind"),
                "fp16_retry_eligible": dtype_name == "bfloat16" and all(
                    case["status"] == "unsupported" and case.get("failure_kind") == "compatibility"
                    for case in failures)}
    if [case.get("m") for case in cases] != REFERENCE_POLICY["fixture"]["batch_rows"]:
        return {"status": "error", "failure_kind": "internal", "fp16_retry_eligible": False,
                "message": "missing expected M=1 or M=256 case"}
    return {"status": "passed", "failure_kind": None, "fp16_retry_eligible": False}


def _read_header(path: Path) -> tuple[dict, int]:
    """只读 safetensors header；拒绝截断或不合理大小，未读 tensor payload。"""
    with path.open("rb") as stream:
        raw = stream.read(8)
        if len(raw) != 8:
            raise ReferenceFailure(f"truncated safetensors header: {path.name}")
        size = struct.unpack("<Q", raw)[0]
        if not 2 <= size <= 16 * 1024 * 1024:
            raise ReferenceFailure(f"invalid safetensors header length: {size}")
        raw = stream.read(size)
    if len(raw) != size:
        raise ReferenceFailure(f"truncated safetensors metadata: {path.name}")
    header = json.loads(raw)
    if not isinstance(header, dict):
        raise ReferenceFailure("safetensors metadata must be a mapping")
    return header, 8 + size


def locate_projection(model_dir: Path) -> dict:
    """允许读取各 shard 的 header，但只返回此投影的 tensor data 范围。"""
    model_dir = model_dir.resolve()
    names = {f"{PROJECTION}.{suffix}": suffix for suffix in ("qweight", "qzeros", "scales", "bias")}
    index = model_dir / "model.safetensors.index.json"
    if index.exists():
        weight_map = json.loads(index.read_text())["weight_map"]
        paths = {model_dir / weight_map[name] for name in names if name in weight_map}
    else:
        paths = set(model_dir.glob("*.safetensors"))
    found = {}
    byte_sizes = {"I32": 4, "F16": 2, "BF16": 2, "F32": 4}
    for path in sorted(paths):
        path = path.resolve()
        if not path.is_relative_to(model_dir):
            # HF snapshots normally symlink blobs outside snapshots; allow those
            # direct files, but never accept an index path that escapes model_dir.
            named = [p for p in paths if p.resolve() == path]
            if not all(p.absolute().is_relative_to(model_dir) and ".." not in p.parts for p in named):
                raise ReferenceFailure("index shard path escapes model directory")
        header, data_start = _read_header(path)
        payload_size = path.stat().st_size - data_start
        for full_name, suffix in names.items():
            if full_name not in header:
                continue
            if suffix in found:
                raise ReferenceFailure(f"duplicate projection tensor: {full_name}")
            info = header[full_name]
            dtype, shape, offsets = info.get("dtype"), info.get("shape"), info.get("data_offsets")
            if (dtype not in byte_sizes or not isinstance(shape, list)
                    or any(type(dim) is not int or dim <= 0 for dim in shape)
                    or not isinstance(offsets, list) or len(offsets) != 2
                    or any(type(x) is not int for x in offsets)
                    or not 0 <= offsets[0] <= offsets[1] <= payload_size
                    or offsets[1] - offsets[0] != math.prod(shape) * byte_sizes[dtype]):
                raise ReferenceFailure(f"invalid tensor metadata: {full_name}")
            expected_dtype = {"I32"} if suffix in ("qweight", "qzeros") else {"F16", "BF16", "F32"}
            if dtype not in expected_dtype:
                raise ReferenceFailure(f"unexpected storage dtype for {full_name}: {dtype}")
            found[suffix] = {"name": full_name, "file": str(path), "shape": shape,
                             "storage_dtype": dtype, "data_offsets": offsets,
                             "data_start": data_start}
    missing = {"qweight", "qzeros", "scales"} - found.keys()
    if missing:
        raise ReferenceFailure(f"checkpoint missing projection tensors: {sorted(missing)}")
    return found


def _payload_sha256(info: dict) -> str:
    digest = hashlib.sha256()
    remaining = info["data_offsets"][1] - info["data_offsets"][0]
    with open(info["file"], "rb") as stream:
        stream.seek(info["data_start"] + info["data_offsets"][0])
        while remaining:
            chunk = stream.read(min(remaining, 1024 * 1024))
            if not chunk:
                raise ReferenceFailure("tensor payload truncated while hashing")
            digest.update(chunk)
            remaining -= len(chunk)
    return digest.hexdigest()


def independent_awq_weight(torch, qweight, qzeros, scales, group_size: int):
    """只在 GPU 上独立 unpack，返回实际 params dtype scales 所定义的 FP32 W。"""
    if not all(t.device.type == "cuda" for t in (qweight, qzeros, scales)):
        raise ReferenceFailure("independent reference requires GPU tensors", status="unsupported", kind="compatibility")
    k, n = qweight.shape[0], qweight.shape[1] * 8
    validate_projection_layout({"qweight": list(qweight.shape), "qzeros": list(qzeros.shape),
                                "scales": list(scales.shape)}, k, n, group_size)
    shifts = torch.tensor(AWQ_SHIFTS, dtype=torch.int64, device=qweight.device)
    values = ((qweight.to(torch.int64).unsqueeze(-1) >> shifts) & 15).reshape(k, n)
    zeros = ((qzeros.to(torch.int64).unsqueeze(-1) >> shifts) & 15).reshape(k // group_size, n)
    groups = torch.arange(k, device=qweight.device) // group_size
    return (values.float() - zeros[groups].float()) * scales[groups].float()


@contextmanager
def _record_production_ops(module, events: list):
    targets = [(module.ops, "awq_gemm"), (module.ops, "awq_dequantize"), (module.torch, "matmul")]
    originals = [(obj, name, getattr(obj, name)) for obj, name in targets]
    for obj, name, original in originals:
        def wrapped(*args, _name=name, _original=original, **kwargs):
            events.append({"op": _name, "tensor_shapes": [list(a.shape) for a in args if hasattr(a, "shape")]})
            return _original(*args, **kwargs)
        setattr(obj, name, wrapped)
    try:
        yield
    finally:
        for obj, name, original in originals:
            setattr(obj, name, original)


@contextmanager
def _fp32_reference_math(torch):
    old_tf32 = torch.backends.cuda.matmul.allow_tf32
    old_precision = torch.get_float32_matmul_precision()
    torch.set_float32_matmul_precision("highest")
    torch.backends.cuda.matmul.allow_tf32 = False
    try:
        yield
    finally:
        torch.set_float32_matmul_precision(old_precision)
        torch.backends.cuda.matmul.allow_tf32 = old_tf32


def _error_record(exc: Exception, stage: str, *, production=False) -> dict:
    if isinstance(exc, ReferenceFailure):
        return {"status": exc.status, "failure_kind": exc.kind, "stage": exc.stage,
                "exception_type": type(exc).__name__, "message": str(exc)}
    message = str(exc)
    if "out of memory" in message.lower() or type(exc).__name__ == "OutOfMemoryError":
        status, kind = "unsupported", "resource"
    elif "device-side assert" in message.lower() or "illegal memory access" in message.lower():
        status, kind = "error", "device_execution"
    elif isinstance(exc, ImportError):
        status, kind = "unsupported", "environment"
    elif (production and not isinstance(exc, (AttributeError, AssertionError))
          and (isinstance(exc, (RuntimeError, NotImplementedError)) or type(exc).__module__.startswith("triton"))
          and re.search(r"out_dtype\s*=\s*bfloat16\s+is unsupported|"
                        r"unsupported (?:dtype|data type|scalar type)|"
                        r"not implemented for [\"']?(?:bfloat16|bf16|half|float16)|"
                        r"(?:bfloat16|bf16|float16|fp16) (?:is |are )?not supported|"
                        r"does not support (?:bfloat16|bf16|float16|fp16)", message.lower())):
        # A generic runtime/compiler error may be a bug, not dtype support.
        # Stop on unknown diagnostics; never use an exception class alone to retry.
        status, kind = "unsupported", "compatibility"
    elif stage in ("gpu_preflight", "dependencies"):
        status, kind = "unsupported", "environment"
    else:
        status, kind = "error", "input" if stage == "checkpoint" else "internal"
    return {"status": status, "failure_kind": kind, "stage": stage,
            "exception_type": f"{type(exc).__module__}.{type(exc).__name__}", "message": message}


def _case(torch, module, method, layer, weight_fp32, bias, m: int, dtype_name: str) -> dict:
    result = {"m": m, "k": int(weight_fp32.shape[0]), "n": int(weight_fp32.shape[1]),
              "expected_ops": ["awq_gemm"] if m == 1 else ["awq_dequantize", "matmul"],
              "observed_ops": [], "dtype": dtype_name}
    generator = torch.Generator(device=weight_fp32.device).manual_seed(REFERENCE_POLICY["fixture"]["seed"])
    x = torch.randn((m, weight_fp32.shape[0]), generator=generator,
                    device=weight_fp32.device, dtype=torch.float32).to(layer.scales.dtype)
    with _fp32_reference_math(torch):
        reference = torch.matmul(x.float(), weight_fp32)
        if bias is not None:
            reference.add_(bias.float())
        torch.cuda.synchronize()
    try:
        with _record_production_ops(module, result["observed_ops"]):
            actual = method.apply(layer, x, bias)
            torch.cuda.synchronize()
    except Exception as exc:
        result.update(_error_record(exc, "production_apply", production=True))
        return result
    if [event["op"] for event in result["observed_ops"]] != result["expected_ops"]:
        result.update(status="unsupported", failure_kind="configuration", stage="path_evidence",
                      message="Observed apply path differs from the predeclared fixture")
        return result
    result["actual_dtype"] = str(actual.dtype)
    if actual.dtype != layer.scales.dtype or actual.device != x.device:
        result.update(status="numerical_failure", failure_kind="numerical",
                      reason="output_dtype_or_device_mismatch", actual_device=str(actual.device))
        return result
    if tuple(actual.shape) != tuple(reference.shape):
        result.update(status="numerical_failure", failure_kind="numerical", reason="output_shape_mismatch",
                      actual_shape=list(actual.shape), reference_shape=list(reference.shape))
        return result
    finite = bool(torch.isfinite(actual).all().item() and torch.isfinite(reference).all().item())
    metrics = {"finite": finite}
    if finite:
        delta = actual.float() - reference
        reference_norm = torch.linalg.vector_norm(reference).item()
        metrics.update(relative_l2=torch.linalg.vector_norm(delta).item() / max(reference_norm, 1e-12),
                       max_abs_error=delta.abs().max().item(),
                       mean_abs_error=delta.abs().mean().item(),
                       reference_rms=reference_norm / math.sqrt(reference.numel()),
                       reference_max_abs=reference.abs().max().item())
        nonfinite_metrics = [key for key, value in metrics.items()
                             if isinstance(value, float) and not math.isfinite(value)]
        if nonfinite_metrics:
            metrics["finite"] = False
            metrics["nonfinite_metrics"] = nonfinite_metrics
            for key in nonfinite_metrics:
                metrics[key] = None
    result["metrics"] = metrics
    result["acceptance"] = evaluate_metrics(metrics, dtype_name)
    result["status"] = "passed" if result["acceptance"]["passed"] else "numerical_failure"
    result["failure_kind"] = None if result["status"] == "passed" else "numerical"
    return result


def run_reference(model_dir: Path, dtype_name: str) -> dict:
    report = {"schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(),
              "status": "error", "failure_kind": "internal", "dtype": dtype_name,
              "fp16_retry_eligible": False, "policy": reference_policy(), "cases": [],
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    stage = "gpu_preflight"
    try:
        try:
            torch = importlib.import_module("torch")
        except ImportError as exc:
            raise ReferenceFailure("PyTorch unavailable; no CPU fallback", status="unsupported", kind="environment", stage=stage) from exc
        if not torch.cuda.is_available():
            raise ReferenceFailure("CUDA/ROCm GPU unavailable; no CPU fallback", status="unsupported", kind="environment", stage=stage)
        device = torch.device("cuda", torch.cuda.current_device())
        report["environment"] = {"torch": torch.__version__, "hip": torch.version.hip,
                                 "cuda": torch.version.cuda, "gpu": torch.cuda.get_device_name(device),
                                 "device": str(device)}
        stage = "dependencies"
        try:
            vllm = importlib.import_module("vllm")
            safetensors = importlib.import_module("safetensors")
            module = importlib.import_module("vllm.model_executor.layers.quantization.auto_awq")
        except (ImportError, OSError) as exc:
            raise ReferenceFailure(str(exc), status="unsupported", kind="environment", stage=stage) from exc
        try:
            vllm_profile = profile_for_version(vllm.__version__)
        except ValueError as exc:
            raise ReferenceFailure(str(exc),status="unsupported",kind="environment",stage=stage) from exc
        if not module.current_platform.is_cuda_alike():
            raise ReferenceFailure("vLLM platform is not CUDA/ROCm", status="unsupported", kind="environment", stage=stage)
        module.current_platform.verify_quantization("auto_awq")
        if module.envs.VLLM_BATCH_INVARIANT:
            raise ReferenceFailure("batch-invariant mode prevents the M=1 fused path", status="unsupported", kind="configuration", stage=stage)
        report["environment"].update(vllm=vllm.__version__, vllm_profile=vllm_profile, platform=str(module.current_platform.device_name),
                                     triton_awq=bool(module.envs.VLLM_USE_TRITON_AWQ),
                                     batch_invariant=bool(module.envs.VLLM_BATCH_INVARIANT),
                                     apply_source_sha256=hashlib.sha256(inspect.getsource(module.AutoAWQLinearMethod.apply).encode()).hexdigest())
        stage = "checkpoint"
        config_bytes = (model_dir / "config.json").read_bytes()
        config = json.loads(config_bytes)
        quant = config.get("quantization_config", {})
        if (config.get("model_type") != "qwen2" or quant.get("quant_method") != "awq"
                or quant.get("bits") != 4 or quant.get("group_size") != 128
                or quant.get("zero_point") is not True or str(quant.get("version", "")).lower() != "gemm"):
            raise ReferenceFailure("fixture requires Qwen2 AWQ GEMM, bits=4, group_size=128, zero_point=true")
        k = int(config["hidden_size"])
        n = int(config.get("head_dim", k // config["num_attention_heads"])) * config["num_attention_heads"]
        if k != 1536 or n != 1536:
            raise ReferenceFailure("fixture requires the Qwen2.5-1.5B q_proj dimensions K=N=1536")
        metadata = locate_projection(model_dir)
        validate_projection_layout({name: info["shape"] for name, info in metadata.items()}, k, n, 128)
        report["checkpoint"] = {"model_dir": str(model_dir.resolve()), "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
                                "config_torch_dtype": config.get("torch_dtype"), "quantization_config": quant,
                                "revision_verified": False, "tensors": metadata}
        tensors = {}
        for name, info in metadata.items():
            info["payload_sha256"] = _payload_sha256(info)
            with safetensors.safe_open(info["file"], framework="pt", device="cpu") as handle:
                tensors[name] = handle.get_tensor(info["name"])
        stage = "weight_preparation"
        dtype = getattr(torch, dtype_name)
        method = module.AutoAWQLinearMethod(module.AutoAWQConfig.from_config(quant))
        with torch.inference_mode(), torch.device(device):
            layer = torch.nn.Module()
            # create_weights uses BasevLLMParameter and requires a live TP group.
            # Header validation above checks the TP=1 checkpoint layout; register
            # just this projection, then use the actual production post-load hook
            # (0.33 inherits the no-op hook; 0.26 re-registers ordinary Parameters).
            for name in ("qweight", "qzeros", "scales"):
                param_dtype = dtype if name == "scales" else torch.int32
                layer.register_parameter(name, torch.nn.Parameter(
                    tensors[name].to(device=device, dtype=param_dtype), requires_grad=False))
            bias = tensors["bias"].to(device=device, dtype=dtype) if "bias" in tensors else None
            del tensors
            method.process_weights_after_loading(layer)
            report["runtime_parameters"] = {name: {"shape": list(getattr(layer, name).shape), "dtype": str(getattr(layer, name).dtype)}
                                            for name in ("qweight", "qzeros", "scales")}
            report["runtime_parameters"]["bias"] = None if bias is None else {"shape": list(bias.shape), "dtype": str(bias.dtype)}
            if not torch.isfinite(layer.scales).all().item() or (bias is not None and not torch.isfinite(bias).all().item()):
                raise ReferenceFailure("checkpoint scales/bias become nonfinite at requested params dtype")
            stage = "reference"
            weight_fp32 = independent_awq_weight(torch, layer.qweight, layer.qzeros, layer.scales, 128)
            for m in REFERENCE_POLICY["fixture"]["batch_rows"]:
                case = _case(torch, module, method, layer, weight_fp32, bias, m, dtype_name)
                report["cases"].append(case)
                if case.get("failure_kind") in ("resource", "device_execution", "internal"):
                    break
        report.update(summarize_cases(report["cases"], dtype_name))
    except Exception as exc:
        report.update(_error_record(exc, stage))
    return report


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        tmp = Path(stream.name)
        stream.write(serialized)
    try:
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--dtype", choices=("bfloat16", "float16"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = run_reference(args.model_dir, args.dtype)
    write_report(args.output, report)
    print(json.dumps({"status": report["status"], "failure_kind": report["failure_kind"],
                      "output": str(args.output)}, ensure_ascii=False))
    return {"passed": 0, "numerical_failure": 2, "unsupported": 3, "error": 4}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())
