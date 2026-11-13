#!/usr/bin/env python3
"""W4-U1：固定合同的 MatMul 测量；无 GPU 时只检查方法，不生成性能结果。"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import platform
import re
import statistics
import subprocess
import sys
import uuid


CONTRACT = {
    "id": "w4-u1-p1", "version": 1,
    "ms": [128, 256], "k": 5120, "n": 25600, "seed": 20261110,
    "warmup": 20, "rounds": 5, "calls_per_sample": 20,
    "storage_dtype": "bfloat16", "relative_l2_limit": 0.01,
    "max_abs_relative_limit": 0.01, "max_abs_floor": 0.001,
}
TIMING_SCOPE = "20 次预分配 torch.mm 的设备事件区间摊销时间；可包含设备等待 Host 提交的间隙"
PACKAGE_FILES = ("harness.py", "test_harness.py", "README.md")
PACKAGE_REVISION = "2026-11-10.2"
TORCH_213_COMMIT = "cf30153c4c131c8164ee7798e5022d810682e2cb"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, payload):
    # 先序列化，避免 NaN 或不可序列化对象留下半个结果文件。
    text = json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    with Path(path).open("x", encoding="utf-8") as stream:
        stream.write(text)


def new_run_dir(root, prefix):
    if not re.fullmatch(r"[a-z][a-z0-9-]*", prefix):
        raise ValueError("非法运行目录前缀")
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = root / f"{prefix}-{stamp}-{uuid.uuid4().hex[:8]}"
    target.mkdir(exist_ok=False)
    return target


def workload(m, k=5120, n=25600):
    if any(isinstance(x, bool) or not isinstance(x, int) or x <= 0 for x in (m, k, n)):
        raise ValueError("M/K/N 必须为正整数")
    a, b, c = 2 * m * k, 2 * k * n, 2 * m * n
    f, q = 2 * m * n * k, a + b + c
    return {"flops": f, "a_bytes": a, "b_bytes": b, "c_bytes": c,
            "q0_bytes": q, "ai0_flop_per_byte": f / q}


def round_order(index):
    if isinstance(index, bool) or not isinstance(index, int) or index < 0:
        raise ValueError("轮序必须是非负整数")
    return (128, 256) if index % 2 == 0 else (256, 128)


def correctness_metrics(actual, reference, torch_module):
    t = torch_module
    if tuple(actual.shape) != tuple(reference.shape) or actual.numel() == 0:
        raise ValueError("正确性检查要求相同的非空 shape")
    # 在 CPU 上用 double 汇总误差，不改变 FP32 参考矩阵乘的计算精度。
    a = actual.detach().to(device="cpu", dtype=t.float64)
    r = reference.detach().to(device="cpu", dtype=t.float64)
    finite = bool(t.isfinite(a).all().item() and t.isfinite(r).all().item())
    result = {"finite": finite, "relative_l2": None, "max_abs_error": None,
              "max_abs_reference": None, "max_abs_limit": None, "passed": False}
    if not finite:
        return result
    d = a - r
    error_norm = t.linalg.vector_norm(d).item()
    ref_norm = t.linalg.vector_norm(r).item()
    relative = error_norm / ref_norm if ref_norm else (0.0 if error_norm == 0 else None)
    max_error, max_reference = d.abs().max().item(), r.abs().max().item()
    limit = CONTRACT["max_abs_relative_limit"] * max_reference + CONTRACT["max_abs_floor"]
    result.update(relative_l2=relative, max_abs_error=max_error,
                  max_abs_reference=max_reference, max_abs_limit=limit,
                  passed=(relative is not None and relative <= CONTRACT["relative_l2_limit"]
                          and max_error <= limit))
    return result


def prepare_inputs(torch_module, device, m=256, k=5120, n=25600, seed=20261110):
    t = torch_module
    if m < 2 or m % 2:
        raise ValueError("最大 M 必须是正偶数")
    workload(m, k, n)
    rng = t.Generator(device="cpu").manual_seed(seed)
    a_cpu = (t.randn((m, k), generator=rng, dtype=t.float32) / math.sqrt(k)).to(t.bfloat16)
    b_cpu = t.randn((k, n), generator=rng, dtype=t.float32).to(t.bfloat16)
    a, b = a_cpu.to(device), b_cpu.to(device)
    outputs = {rows: t.empty((rows, n), dtype=t.bfloat16, device=device)
               for rows in (m // 2, m)}
    return a, b, outputs


def measure_one(torch_module, a, b, out, calls=20):
    if isinstance(calls, bool) or not isinstance(calls, int) or calls <= 0:
        raise ValueError("调用次数必须是正整数")
    t = torch_module
    start, end = t.cuda.Event(enable_timing=True), t.cuda.Event(enable_timing=True)
    t.cuda.synchronize()
    start.record()
    for _ in range(calls):
        t.mm(a, b, out=out)
    end.record()
    end.synchronize()
    total = float(start.elapsed_time(end))
    if not math.isfinite(total) or total <= 0:
        raise ValueError("设备事件时间必须为有限正值")
    return {"total_ms": total, "calls": calls, "mean_ms": total / calls}


def summarize(samples):
    if len(samples) != CONTRACT["rounds"] * len(CONTRACT["ms"]):
        raise ValueError("需要两个 shape 各五轮的完整样本")
    seen = set()
    for s in samples:
        if not isinstance(s, dict) or not {"round", "order", "m", "calls", "total_ms", "mean_ms"} <= s.keys():
            raise ValueError("样本字段缺失")
        rnd, m, calls = s["round"], s["m"], s["calls"]
        if (isinstance(rnd, bool) or not isinstance(rnd, int) or rnd not in range(5)
                or isinstance(m, bool) or not isinstance(m, int) or m not in CONTRACT["ms"]
                or isinstance(calls, bool) or not isinstance(calls, int) or calls != 20):
            raise ValueError("样本不符合固定轮数、shape 或调用次数")
        if (rnd, m) in seen:
            raise ValueError("重复的轮序与 shape")
        seen.add((rnd, m))
        if type(s["order"]) is not int or s["order"] != round_order(rnd).index(m):
            raise ValueError("shape 顺序与合同不一致")
        for key in ("total_ms", "mean_ms"):
            if type(s[key]) not in (int, float) or not math.isfinite(s[key]) or s[key] <= 0:
                raise ValueError("样本时间必须为有限正值")
        if not math.isclose(s["total_ms"] / calls, s["mean_ms"], rel_tol=1e-9):
            raise ValueError("总时间与摊销时间不一致")
    by_m = {}
    for m in CONTRACT["ms"]:
        values = [s["mean_ms"] for s in samples if s["m"] == m]
        median = statistics.median(values)
        w = workload(m)
        by_m[str(m)] = {**w, "mean_ms_median": median,
                       "mean_ms_min": min(values), "mean_ms_max": max(values),
                       "useful_tflops": w["flops"] / (median * 1e9),
                       "q0_effective_gb_s": w["q0_bytes"] / (median * 1e6),
                       "q_actual_bytes": None,
                       "q0_is_model_budget": True}
    return {"by_m": by_m, "sample_count": len(samples), "samples_per_shape": 5,
            "timing_scope": TIMING_SCOPE,
            "interpretation": "不同 M 的工作量不同；本表不是同任务优化加速比。Q₀/t 为模型值。"}


def command_snapshot(args):
    try:
        p = subprocess.run(args, text=True, capture_output=True, timeout=15, check=False)
        return {"command": args, "returncode": p.returncode,
                "stdout": p.stdout[:16000], "stderr": p.stderr[:4000]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"command": args, "unavailable": str(exc)}


def precision_source(version, git_version):
    """只放行已核验的版本；新构建按返回的精确源码识别。"""
    if re.fullmatch(r"2\.9\.\d+(?:\+[A-Za-z0-9.]+)?", str(version)):
        ref = "v2.9.0"
    elif (re.fullmatch(r"2\.13\.0(?:\+[A-Za-z0-9.]+)?", str(version))
          and git_version == TORCH_213_COMMIT):
        ref = TORCH_213_COMMIT
    else:
        return None
    return f"https://github.com/pytorch/pytorch/blob/{ref}/aten/src/ATen/cuda/CUDABlas.cpp"


def configure_precision(t):
    # 使用已核验的新 FP32 设置，绝不混设旧 allow_tf32。
    t.backends.fp32_precision = "ieee"
    t.backends.cuda.matmul.fp32_precision = "ieee"
    t.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = False
    settings = {
        "global_fp32_precision": t.backends.fp32_precision,
        "matmul_fp32_precision": t.backends.cuda.matmul.fp32_precision,
        "allow_bf16_reduced_precision_reduction":
            t.backends.cuda.matmul.allow_bf16_reduced_precision_reduction,
        "evidence": f"PyTorch {t.__version__} CUDA 配置与 FP32 compute 合同；未检查底层指令",
    }
    if (settings["global_fp32_precision"] != "ieee"
            or settings["matmul_fp32_precision"] != "ieee"
            or settings["allow_bf16_reduced_precision_reduction"] is not False):
        raise RuntimeError("精度设置回读不一致")
    return settings


def collect_environment(device_index):
    env = {"schema_version": 1, "created_at": utc_now(), "status": "blocked", "errors": [],
           "python": sys.version, "os": platform.platform(), "machine": platform.machine(),
           "cpu": platform.processor(), "cpu_count": os.cpu_count(),
           "device_index": device_index, "contract": CONTRACT,
           "precision": None, "device": None,
           "environment_overrides": {key: os.environ.get(key) for key in
               ("CUDA_VISIBLE_DEVICES", "HIP_VISIBLE_DEVICES", "ROCR_VISIBLE_DEVICES",
                "NVIDIA_TF32_OVERRIDE", "TORCH_ALLOW_TF32_CUBLAS_OVERRIDE",
                "TORCH_BLAS_PREFER_CUBLASLT", "TORCH_BLAS_PREFER_HIPBLASLT",
                "CUBLAS_WORKSPACE_CONFIG")}}
    try:
        t = importlib.import_module("torch")
    except (ImportError, OSError) as exc:
        env["errors"].append(f"PyTorch 无法导入：{exc}；使用已有的 GPU PyTorch 镜像后重新检查。")
        return env, None
    env.update(torch_version=t.__version__, torch_git_version=t.version.git_version,
               cuda_runtime=t.version.cuda, hip_runtime=t.version.hip,
               torch_build_config=t.__config__.show())
    env["package_revision"] = PACKAGE_REVISION
    env["precision_source"] = precision_source(t.__version__, t.version.git_version)
    try:
        env["blas_library_preference"] = str(t.backends.cuda.preferred_blas_library())
    except (AttributeError, RuntimeError):
        env["blas_library_preference"] = None
    env["cuda_available"] = bool(t.cuda.is_available())
    if not env["cuda_available"]:
        env["errors"].append("没有可用的 GPU 后端；不会转为 CPU 计时。")
        return env, t
    env["device_count"] = t.cuda.device_count()
    if device_index < 0 or device_index >= env["device_count"]:
        env["errors"].append("所选 GPU 编号不存在。")
        return env, t
    try:
        t.cuda.set_device(device_index)
        props = t.cuda.get_device_properties(device_index)
        free_bytes, total_bytes = t.cuda.mem_get_info(device_index)
        env["device"] = {"name": props.name, "capability": list(t.cuda.get_device_capability()),
                         "total_memory_bytes": props.total_memory, "free_memory_bytes": free_bytes,
                         "visible_total_memory_bytes": total_bytes,
                         "multiprocessor_count": props.multi_processor_count,
                         "gcn_arch_name": getattr(props, "gcnArchName", None),
                         "uuid": str(getattr(props, "uuid", "unknown"))}
        if t.version.hip:
            env["driver_snapshot"] = command_snapshot(["rocm-smi", "--showdriverversion", "--showproductname"])
            env["errors"].append("已采集 ROCm 信息；本包首版尚未核验该架构与 BLAS 精度路径，请返回环境文件。")
        else:
            env["driver_snapshot"] = command_snapshot([
                "nvidia-smi", "--query-gpu=index,name,uuid,driver_version,memory.total,pstate,clocks.sm,clocks.mem",
                "--format=csv,noheader"])
            if props.major < 8 or not t.cuda.is_bf16_supported(including_emulation=False):
                env["errors"].append("设备未通过原生 BF16 条件检查（CUDA compute capability ≥8）。")
        if env["precision_source"] is None:
            env["errors"].append("该 PyTorch 版本／构建的精度路径尚未核验；已支持 2.9.x 正式版及已核验的 2.13.0 构建，请先返回环境信息。")
        if free_bytes < 2 * 1024**3:
            env["errors"].append("可用显存不足 2 GiB，先释放其他任务占用。")
        if os.environ.get("NVIDIA_TF32_OVERRIDE") == "1":
            env["errors"].append("NVIDIA_TF32_OVERRIDE=1 可能覆盖参考计算精度；须先移除。")
        if os.environ.get("TORCH_ALLOW_TF32_CUBLAS_OVERRIDE") == "1":
            env["errors"].append("TORCH_ALLOW_TF32_CUBLAS_OVERRIDE=1 会强制 TF32；须先移除。")
        if not env["errors"]:
            env["precision"] = configure_precision(t)
            env["status"] = "ready_for_prediction"
    except (RuntimeError, AttributeError, TypeError) as exc:
        env["errors"].append(f"设备或精度条件无法确认：{exc}")
    return env, t


def snapshot_sources(run_dir):
    source_dir = run_dir / "source"
    source_dir.mkdir()
    hashes = {}
    for name in PACKAGE_FILES:
        p = Path(__file__).resolve().parent / name
        if not p.is_file():
            raise RuntimeError(f"测试包文件缺失：{name}")
        data = p.read_bytes()
        with (source_dir / name).open("xb") as dest:
            dest.write(data)
        hashes[name] = hashlib.sha256(data).hexdigest()
    git = command_snapshot(["git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "HEAD"])
    write_json(run_dir / "manifest.json", {
        "created_at": utc_now(), "argv": sys.argv, "contract": CONTRACT,
        "package_revision": PACKAGE_REVISION,
        "source_sha256": hashes, "git_head": git.get("stdout", "").strip() or None,
        "source_authority": "本次 source 快照与 SHA256；工作区可能有未提交修改，不以 git HEAD 代替实际脚本",
    })


def execute_measurement(t, run_dir):
    with t.inference_mode():
        a, b, outputs = prepare_inputs(t, t.device("cuda", t.cuda.current_device()))
        tensor_metadata = {"a_shape": list(a.shape), "b_shape": list(b.shape),
                           "a_stride": list(a.stride()), "b_stride": list(b.stride()),
                           "dtype": str(a.dtype), "layout": "contiguous row-major",
                           "input_policy": "fixed CPU generator; A128 is A256[:128]; shared B",
                           "cache_policy": "预热后反复使用同一组输入输出，不清空缓存"}
        write_json(run_dir / "inputs.json", tensor_metadata)
        refs, before = {}, {}
        b32 = b.float()
        for m in CONTRACT["ms"]:
            # IEEE FP32 参考从实际 BF16 值构造；转换、参考与误差汇总全部在计时外。
            reference = t.mm(a[:m].float(), b32)
            t.mm(a[:m], b, out=outputs[m])
            before[str(m)] = correctness_metrics(outputs[m], reference, t)
            refs[m] = reference.cpu()
            del reference
        del b32
        write_json(run_dir / "correctness_before.json", before)
        if not all(item["passed"] for item in before.values()):
            raise RuntimeError("正确性检查未通过；未进行正式计时，请返回误差结果。")
        for m in CONTRACT["ms"]:
            for _ in range(CONTRACT["warmup"]):
                t.mm(a[:m], b, out=outputs[m])
        t.cuda.synchronize()
        samples = []
        fields = ["round", "order", "m", "calls", "total_ms", "mean_ms"]
        with (run_dir / "samples.csv").open("x", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            stream.flush()
            for rnd in range(CONTRACT["rounds"]):
                for order, m in enumerate(round_order(rnd)):
                    result = measure_one(t, a[:m], b, outputs[m], CONTRACT["calls_per_sample"])
                    sample = {"round": rnd, "order": order, "m": m, **result}
                    samples.append(sample)
                    writer.writerow(sample)
                    stream.flush()
        after = {str(m): correctness_metrics(outputs[m], refs[m], t) for m in CONTRACT["ms"]}
        write_json(run_dir / "correctness_after.json", after)
        if not all(item["passed"] for item in after.values()):
            raise RuntimeError("计时后正确性检查未通过；保留原始时间，但不生成有效性能结论。")
        summary = summarize(samples)
        summary.update(status="measured", result_type="真实设备事件计时及派生值",
                       resource_peak_flops_s=None, resource_bandwidth_bytes_s=None,
                       roofline_model_ratio=None,
                       resource_note="设备能力与单位由 Agent 按实际设备和计算模式核对后对照；不自动猜峰值。")
        write_json(run_dir / "summary.json", summary)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "run"):
        child = sub.add_parser(name, help="只采集环境" if name == "preflight" else "在提交预测后运行固定实验")
        child.add_argument("--device", type=int, default=0 if name == "preflight" else None,
                           required=name == "run",
                           help="可见 GPU 编号；正式运行必须明确选择与环境检查相同的卡")
        child.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent / "runs")
        if name == "run":
            child.add_argument("--prediction", required=True, help="测量前在对话中提交的原文；保留预测及成立条件")
    args = parser.parse_args(argv)
    if args.command == "run" and not args.prediction.strip():
        parser.error("--prediction 不能为空；先完成事前预测")
    run_dir = new_run_dir(args.output_root, args.command)
    try:
        snapshot_sources(run_dir)
        if args.command == "run":
            write_json(run_dir / "prediction.json", {"created_at": utc_now(), "text": args.prediction.strip(),
                       "note": "在该运行采样前保存；独立性由对话评阅，不由脚本判断。"})
        env, t = collect_environment(args.device)
        write_json(run_dir / "environment.json", env)
        if env["status"] != "ready_for_prediction":
            print("环境检查未通过；已保存信息，不进行正式计时。")
            for error in env["errors"]:
                print("- " + error)
            write_json(run_dir / "status.json", {"status": "blocked", "finished_at": utc_now(), "errors": env["errors"]})
            print(f"结果目录：{run_dir}")
            return 2
        if args.command == "preflight":
            write_json(run_dir / "status.json", {"status": "ready_for_prediction", "finished_at": utc_now()})
            print("环境检查通过；尚未测量。请返回 environment.json 并提交事前预测。")
        else:
            execute_measurement(t, run_dir)
            write_json(run_dir / "status.json", {"status": "measured", "finished_at": utc_now()})
            print("固定实验完成；请返回整个结果目录。性能解释与结课由后续评阅决定。")
        print(f"结果目录：{run_dir}")
        return 0
    except Exception as exc:
        write_json(run_dir / "failure.json", {"status": "failed", "finished_at": utc_now(),
                   "error_type": type(exc).__name__, "error": str(exc),
                   "note": "保留已有原始结果；不要修改文件伪装通过。"})
        print(f"运行停止：{exc}\n结果目录：{run_dir}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
