#!/usr/bin/env python3
"""W4-U2-P1: bounded, reproducible single-GPU serving experiment.

No dependencies are installed. `preflight` is read-only apart from its report.
`prepare` downloads only the pinned public model; `run` requires a prediction.
All GPU measurements must happen on the learner's actual ROCm instance.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import gzip
import hashlib
import http.client
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import random
import re
import shutil
import signal
import socket
import statistics
import subprocess
import sys
import time
import urllib.parse
import uuid
import zipfile

ROOT = Path(__file__).resolve().parent
REVISION = "2026-11-12.3"
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MODEL_REVISION = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
VLLM_TAG = "0.26.0"
SEED = 20261112
BUDGETS = (512, 2048)
ORDER = (512, 2048, 2048, 512, 512, 2048)
CONCURRENCY = 8
REQUEST_COUNT = 48
MAX_MODEL_LEN = 4096
OUTPUT_TOKENS = 128
SERVER_MODEL_NAME = "w4-u2-qwen-bf16"
SOURCE_FILES = (
    "run.py", "client.py", "correctness.py", "configuration.py",
    "test_driver.py", "test_client.py", "test_correctness.py",
    "test_configuration.py", "model_manifest.json", "README.md",
)
SAFE_DEVICE_ENV = ("HIP_VISIBLE_DEVICES", "ROCR_VISIBLE_DEVICES", "CUDA_VISIBLE_DEVICES")
REQUIRED_FLAGS = (
    "--max-num-batched-tokens", "--max-num-seqs", "--max-model-len",
    "--enable-chunked-prefill", "--no-enable-prefix-caching",
    "--no-async-scheduling", "--enforce-eager", "--profiler-config",
    "--generation-config", "--no-enable-log-requests", "--served-model-name",
    "--logprobs-mode",
)


class ExperimentError(RuntimeError):
    pass


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json(path, obj, *, replace=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if replace:
        temp = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex[:8])
        with temp.open("x", encoding="utf-8") as handle:
            handle.write(data)
        os.replace(temp, path)
    else:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(data)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path):
    path = Path(path)
    h = hashlib.sha1()
    h.update(f"blob {path.stat().st_size}\0".encode())
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def new_case(prefix):
    name = prefix + "-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    case = ROOT / "runs" / (name + "-" + uuid.uuid4().hex[:8])
    case.mkdir(parents=True, exist_ok=False)
    return case


def capture_sources(case):
    hashes = {}
    for name in SOURCE_FILES:
        source = ROOT / name
        if not source.is_file():
            raise ExperimentError(f"脚本包不完整：缺少 {name}")
        dest = case / "source" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        hashes[name] = sha256_file(dest)
    write_json(case / "source_manifest.json", {
        "package_revision": REVISION, "captured_at": utc_now(), "sha256": hashes,
    })


def check_source_identity(case):
    manifest = read_json(case / "source_manifest.json")
    for name, digest in manifest["sha256"].items():
        if name not in SOURCE_FILES or sha256_file(ROOT / name) != digest:
            raise ExperimentError("prepare 后脚本包发生变化；请重新 prepare，保留旧结果。")


def save_status(case, phase, **extra):
    write_json(case / "status.json", {"phase": phase, "updated_at": utc_now(), **extra}, replace=True)


def run_capture(command, timeout=90):
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return {"command": command, "returncode": p.returncode,
                "stdout": p.stdout[-500000:], "stderr": p.stderr[-30000:]}
    except subprocess.TimeoutExpired:
        return {"command": command, "returncode": None, "error": "timeout"}
    except OSError as exc:
        return {"command": command, "returncode": None, "error": str(exc)}


def run_reference_logged(command, log_path, timeout):
    """Keep partial diagnostics on timeout and show only concise reference progress."""
    log_path = Path(log_path)
    start = time.monotonic()
    deadline = start + timeout
    next_heartbeat = start + 30
    env = os.environ.copy()
    env.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"})
    timed_out = False
    with log_path.open("xb") as output:
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=output,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        try:
            with log_path.open("r", encoding="utf-8", errors="replace") as reader:
                while True:
                    for line in reader.readlines():
                        if line.startswith("W4_REFERENCE "):
                            print("    " + line.removeprefix("W4_REFERENCE ").rstrip(), flush=True)
                    if process.poll() is not None:
                        break
                    now = time.monotonic()
                    if now >= deadline:
                        timed_out = True
                        break
                    if now >= next_heartbeat:
                        print(f"    CPU FP32 参考仍在运行（{int(now-start)} 秒）；详情见 {log_path.name}", flush=True)
                        next_heartbeat = now + 30
                    time.sleep(min(0.5, max(0.01, deadline - now)))
        finally:
            stop_process(process)
    result = {"command": command, "returncode": None if timed_out else process.returncode,
              "log_file": str(log_path), "elapsed_seconds": time.monotonic() - start,
              "environment_overrides": {"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}}
    if timed_out:
        result["error"] = "timeout"
    return result


TORCH_PROBE = r'''
import json, torch
r = {'torch_version': str(torch.__version__), 'torch_git': getattr(torch.version,'git_version',None),
     'hip_build': torch.version.hip, 'cuda_build': torch.version.cuda,
     'gpu_available': torch.cuda.is_available(), 'device_count': torch.cuda.device_count(), 'devices': []}
for i in range(r['device_count']):
    p = torch.cuda.get_device_properties(i)
    free,total = torch.cuda.mem_get_info(i)
    r['devices'].append({'index':i, 'name':p.name, 'total_memory_bytes':p.total_memory,
        'free_memory_bytes':free, 'reported_total_bytes':total,
        'gcn_arch':getattr(p,'gcnArchName',None), 'multiprocessors':p.multi_processor_count,
        'uuid':str(p.uuid) if getattr(p,'uuid',None) is not None else None})
if r['gpu_available']:
    r['bf16_supported'] = bool(torch.cuda.is_bf16_supported())
    # Functional smoke only: no timer, no performance result.
    x=torch.ones((2,2),device='cuda',dtype=torch.bfloat16)
    r['bf16_smoke_passed'] = bool(torch.equal((x @ x).cpu(), torch.full((2,2),2.,dtype=torch.bfloat16)))
print('W4_ENV_JSON=' + json.dumps(r))
'''


def environment_reasons(info):
    reasons = []
    version = info.get("packages", {}).get("vllm") or ""
    if version.split("+")[0] != VLLM_TAG:
        reasons.append(f"需要已核验的 vLLM {VLLM_TAG}，实际为 {version or '未安装'}")
    for name in ("torch", "transformers", "huggingface_hub", "safetensors"):
        if not info.get("packages", {}).get(name):
            reasons.append(f"镜像缺少 {name}；脚本不会自动安装或替换它")
    gpu = info.get("torch_probe") or {}
    if not gpu.get("hip_build"):
        reasons.append("未确认 PyTorch ROCm/HIP 构建")
    if not gpu.get("gpu_available") or gpu.get("device_count") != 1:
        reasons.append("需要当前容器只暴露一张已分配 GPU")
    if not gpu.get("bf16_supported") or not gpu.get("bf16_smoke_passed"):
        reasons.append("BF16 功能检查未通过")
    devices = gpu.get("devices") or []
    if devices and devices[0].get("total_memory_bytes", 0) < 12 * 1024**3:
        reasons.append("GPU 显存不足本包保守预检门槛 12 GiB，需先缩小方案")
    if info.get("disk_free_bytes", 0) < 12 * 1024**3:
        reasons.append("当前文件系统可用空间少于 12 GiB")
    if not info.get("cli_help_ok"):
        reasons.append("vLLM CLI 检查失败")
    if info.get("missing_flags"):
        reasons.append("CLI 缺少已核验参数：" + ", ".join(info["missing_flags"]))
    return reasons


def gpu_identity(info):
    return [{k: device.get(k) for k in ("index", "name", "total_memory_bytes", "gcn_arch", "uuid")}
            for device in info.get("torch_probe", {}).get("devices", [])]


def inspect_environment(folder):
    folder.mkdir(parents=True, exist_ok=True)
    packages = {}
    for name in ("vllm", "torch", "transformers", "huggingface_hub", "safetensors", "tokenizers", "numpy"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    info = {"observed_at": utc_now(), "python": sys.version, "platform": platform.platform(),
            "packages": packages, "device_visibility": {k: os.environ.get(k) for k in SAFE_DEVICE_ENV},
            "disk_free_bytes": shutil.disk_usage(folder).free,
            "resource_ownership": "single-GPU cloud selection supplied by learner; not proven by free memory"}
    probe = run_capture([sys.executable, "-c", TORCH_PROBE], timeout=120)
    write_json(folder / "torch_probe_process.json", probe)
    prefix = "W4_ENV_JSON="
    for line in probe.get("stdout", "").splitlines():
        if line.startswith(prefix):
            info["torch_probe"] = json.loads(line[len(prefix):])
    if shutil.which("rocm-smi"):
        write_json(folder / "rocm_smi.json", run_capture(["rocm-smi"], timeout=30))
    if packages.get("vllm"):
        help_result = run_capture([sys.executable, "-m", "vllm.entrypoints.cli.main", "serve", "--help=all"], timeout=120)
        help_text = help_result.get("stdout", "")
        info["cli_help_ok"] = help_result.get("returncode") == 0
        info["missing_flags"] = [flag for flag in REQUIRED_FLAGS if flag not in help_text]
        write_json(folder / "cli_help.json", help_result)
    info["reasons"] = environment_reasons(info)
    info["passed"] = not info["reasons"]
    write_json(folder / "environment.json", info)
    return info


def method():
    return {
        "contract": "W4-U2-P1", "contract_version": 1, "package_revision": REVISION,
        "model_id": MODEL_ID, "model_revision": MODEL_REVISION, "vllm_target": VLLM_TAG,
        "precision": "BF16 service / independent Transformers CPU FP32 reference",
        "budgets": list(BUDGETS), "run_order": list(ORDER), "seed": SEED,
        "requests_per_round": REQUEST_COUNT, "prompt_lengths": [256, 3072],
        "prompt_mix": "alternating short/long, 24 each, identical ordered list each round",
        "max_output_tokens": OUTPUT_TOKENS, "ignore_eos": True, "skip_special_tokens": False,
        "arrival": "closed-loop finite queue, all requests enqueued at round start, max 8 in flight",
        "concurrency": CONCURRENCY, "max_num_seqs": 16, "max_model_len": MAX_MODEL_LEN,
        "gpu_memory_utilization": 0.70, "prefix_caching": False, "async_scheduling": False,
        "chunked_prefill": True, "enforce_eager": True, "tensor_parallel_size": 1,
        "warmup": "first 8 fixed prompts, 32 output tokens each, before each measured round",
        "correctness": {"cases": 4, "prompt_lengths": [32, 128, 768, 3072], "generated_tokens_each": 8,
                        "reference_logprob_abs_tolerance": 0.25, "greedy_gap_tolerance": 0.10,
                        "units": "natural-log probability", "positions": "all, not averaged",
                        "scope": "small deterministic numerical sanity set; not general model quality",
                        "cpu_linear_backend": "oneDNN IEEE FP32 when available, otherwise recorded dense backend; eager attention unchanged",
                        "when": "before and after each round; reuse verified FP32 probabilities only for identical token prefixes"},
        "trace": {"budget": 2048, "requests": 4, "max_output_tokens": 16,
                  "separate_process": True, "timings_excluded_from_performance": True,
                  "minimum": "valid exported trace containing GPU kernels and batch annotations",
                  "attribution_limit": "batch-level annotation; no automatic request-to-kernel attribution"},
        "statistics": "per-round raw request distributions and pooled message intervals; P99 exploratory",
        "comparison": "per-setting median/min/max of round statistics, not a pooled percentile",
        "decision": "no required speedup; conditions, direction, repeat variability and limits must be explained",
        "network_scope": "client and service on the same instance, HTTP loopback, excludes public cloud proxy",
        "estimated_download_bytes": 3087467144,
    }


def verify_model(model_dir, manifest=None):
    manifest = manifest or read_json(ROOT / "model_manifest.json")
    result = {"model_id": manifest["model_id"], "revision": manifest["revision"], "files": []}
    for item in manifest["files"]:
        path = Path(model_dir) / item["name"]
        if not path.is_file() or path.stat().st_size != item["bytes"]:
            raise ExperimentError(f"模型文件缺失或大小不符：{item['name']}")
        key = "sha256" if "sha256" in item else "git_blob_sha1"
        digest = sha256_file(path) if key == "sha256" else git_blob_sha1(path)
        if digest != item[key]:
            raise ExperimentError(f"固定模型文件哈希不符：{item['name']}")
        result["files"].append({**item, "verified": True})
    result["verified_at"] = utc_now()
    return result


def obtain_model(model_dir=None):
    manifest = read_json(ROOT / "model_manifest.json")
    if model_dir:
        path = Path(model_dir).expanduser().resolve()
    else:
        endpoint = os.environ.get("HF_ENDPOINT", "https://huggingface.co")
        parsed = urllib.parse.urlparse(endpoint)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ExperimentError("HF_ENDPOINT 必须为不含凭据或查询参数的 HTTPS 地址")
        from huggingface_hub import snapshot_download
        path = Path(snapshot_download(
            repo_id=MODEL_ID, revision=MODEL_REVISION,
            allow_patterns=[item["name"] for item in manifest["files"]],
            local_dir=str(ROOT / "cache" / MODEL_REVISION), max_workers=2, token=False,
        )).resolve()
    return path, verify_model(path, manifest)


def build_inputs(tokenizer):
    """Synthetic text, encoded once, then exact token slices; no remote dataset."""
    words = ["memory", "compute", "request", "queue", "latency", "token", "stream", "batch",
             "model", "device", "kernel", "server", "measure", "cache", "buffer", "schedule"]
    def tokens(index, length):
        rng = random.Random(SEED + index)
        text = "Continue the following synthetic technical notes in English.\n"
        text += "\n".join(
            f"Note {j}: " + " ".join(rng.choice(words) for _ in range(16)) + "."
            for j in range(260)
        )
        ids = tokenizer.encode(text, add_special_tokens=False)
        if len(ids) < length:
            raise ExperimentError("合成输入不足指定长度")
        return ids[:length]
    requests = []
    for i in range(REQUEST_COUNT):
        length = 256 if i % 2 == 0 else 3072
        requests.append({"request_id": f"work-{i:03d}", "prompt_token_ids": tokens(i, length),
                         "max_tokens": OUTPUT_TOKENS,
                         "extra_body": {"add_special_tokens": False, "skip_special_tokens": False}})
    correctness = [
        {"request_id": f"correct-{i}", "prompt_token_ids": tokens(1000 + i, length),
         "max_tokens": 8, "extra_body": {"logprobs": 5, "add_special_tokens": False,
                                         "skip_special_tokens": False}}
        for i, length in enumerate((32, 128, 768, 3072))
    ]
    return {"schema_version": 1, "model_revision": MODEL_REVISION, "seed": SEED,
            "requests": requests, "correctness": correctness}


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def server_command(model_path, budget, port, profile_dir=None):
    if budget not in BUDGETS:
        raise ExperimentError("未约定的预算")
    cmd = [sys.executable, "-m", "vllm.entrypoints.cli.main", "serve", str(model_path),
           "--served-model-name", SERVER_MODEL_NAME, "--host", "127.0.0.1", "--port", str(port),
           "--dtype", "bfloat16", "--tensor-parallel-size", "1", "--pipeline-parallel-size", "1",
           "--max-model-len", str(MAX_MODEL_LEN), "--max-num-seqs", "16",
           "--max-num-batched-tokens", str(budget), "--gpu-memory-utilization", "0.70",
           "--enable-chunked-prefill", "--no-enable-prefix-caching", "--no-async-scheduling",
           "--enforce-eager", "--generation-config", "vllm", "--seed", str(SEED),
           "--no-enable-log-requests", "--logprobs-mode", "raw_logprobs"]
    if profile_dir:
        cmd += ["--profiler-config", json.dumps({"profiler": "torch",
            "torch_profiler_dir": str(Path(profile_dir).resolve()),
            "torch_profiler_with_stack": False, "torch_profiler_use_gzip": True,
            "torch_profiler_record_shapes": True, "torch_profiler_with_memory": True})]
    return cmd


def http_json(base_url, endpoint, *, post=False, timeout=30):
    # Only this experiment's loopback server is addressed; no external publication.
    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme != "http" or parsed.hostname != "127.0.0.1":
        raise ExperimentError("服务控制仅允许 127.0.0.1")
    # http.client ignores proxy environment variables and never follows redirects.
    connection = http.client.HTTPConnection("127.0.0.1", parsed.port, timeout=timeout)
    try:
        connection.request("POST" if post else "GET", endpoint, body=b"" if post else None,
                           headers={"Connection": "close"})
        response = connection.getresponse()
        if response.status != 200:
            raise ExperimentError(f"本地服务控制接口 {endpoint.split('?')[0]} 返回 HTTP {response.status}")
        raw = response.read(8 * 1024 * 1024 + 1)
        if len(raw) > 8 * 1024 * 1024:
            raise ExperimentError("本地控制接口响应超出 8 MiB 限制")
        return json.loads(raw) if raw.strip() else {"http_status": response.status}
    finally:
        connection.close()


def time_left(deadline, cap):
    value = deadline - time.monotonic()
    if value <= 0:
        raise ExperimentError("正式运行达到 80 分钟控制界限；开始保存并清理本包进程")
    return min(value, cap)


def stop_process(process):
    # Also stop orphan workers if the parent exited unexpectedly.
    # Only the process group created by this harness, never unrelated services.
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGTERM)
    if process.poll() is None:
        try:
            process.wait(timeout=40)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)


@contextlib.contextmanager
def serve(model_path, budget, folder, *, profile=False, deadline=None):
    from configuration import project_runtime_config, validate_runtime_config
    folder.mkdir(parents=True, exist_ok=False)
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    cmd = server_command(model_path, budget, port, folder / "traces" if profile else None)
    env = os.environ.copy()
    env.pop("VLLM_API_KEY", None)  # This server is local-only and uses no external key.
    env.update({"VLLM_SERVER_DEV_MODE": "1", "VLLM_CUSTOM_SCOPES_FOR_PROFILING": "1" if profile else "0",
                "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"})
    write_json(folder / "command.json", {"argv": cmd, "environment_overrides": {
        k: env[k] for k in ("VLLM_SERVER_DEV_MODE", "VLLM_CUSTOM_SCOPES_FOR_PROFILING", "HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE")},
        "started_at": utc_now(), "profiler_run": profile, "VLLM_API_KEY_in_child": "unset"})
    with (folder / "server.log").open("x", encoding="utf-8") as log:
        process = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env, cwd=ROOT, start_new_session=True)
        try:
            startup_deadline = min(deadline or float("inf"), time.monotonic() + 600)
            while time.monotonic() < startup_deadline:
                if process.poll() is not None:
                    raise ExperimentError(f"vLLM 启动失败，见 {folder.name}/server.log")
                try:
                    http_json(base_url, "/health", timeout=time_left(startup_deadline, 2))
                    break
                except (OSError, ValueError, ExperimentError):
                    time.sleep(1)
            else:
                raise ExperimentError("vLLM 启动超时（600 秒）")
            # This response contains system_env; NEVER persist/print the response itself.
            projected = project_runtime_config(http_json(base_url, "/server_info?config_format=json",
                                                         timeout=time_left(deadline or startup_deadline, 90)))
            configured = projected.get("scheduler", {}).get("max_num_scheduled_tokens")
            projected["effective_scheduled_token_budget"] = (
                projected.get("scheduler", {}).get("max_num_batched_tokens") if configured is None else configured)
            write_json(folder / "effective_config.json", projected)
            errors = validate_runtime_config(projected, budget, profile=profile)
            if Path(projected.get("model", {}).get("model", "")).resolve() != Path(model_path).resolve():
                errors.append("服务实际模型路径与固定快照不一致")
            if errors:
                raise ExperimentError("生效配置不符：" + "; ".join(errors))
            print(f"    服务就绪，生效预算 {budget} 已核对。", flush=True)
            yield base_url
        finally:
            stop_process(process)
    write_json(folder / "process_exit.json", {"returncode": process.returncode, "stopped_at": utc_now()})


def correctness_records(base_url, requests, folder, *, deadline):
    from client import request_once
    records = []
    with (folder / "correctness_http.jsonl").open("x", encoding="utf-8") as log:
        for request in requests:
            record = request_once(base_url, SERVER_MODEL_NAME, request,
                                  timeout=time_left(deadline, 180), stream=False)
            log.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
            log.flush()
            if not record["success"]:
                raise ExperimentError("正确性请求失败，见 correctness_http.jsonl")
            choice = record["response_json"]["choices"][0]
            records.append({"request_id": request["request_id"],
                            "prompt_token_ids": request["prompt_token_ids"],
                            "token_ids": choice.get("token_ids"),
                            "token_logprobs": (choice.get("logprobs") or {}).get("token_logprobs")})
    write_json(folder / "correctness_inputs.json", records)
    return records


def check_reference(model_path, folder, *, deadline):
    # A separate CPU process releases all reference RAM on exit. No GPU timing here.
    code = ("import json,sys; from correctness import evaluate_records; "
            "evaluate_records(sys.argv[1],json.load(open(sys.argv[2])),sys.argv[3],threads=8,progress=True)")
    print("    启动独立 CPU FP32 参考（不计入服务性能时间）……", flush=True)
    result = run_reference_logged([sys.executable, "-u", "-c", code, str(model_path),
                          str(folder / "correctness_inputs.json"), str(folder / "correctness.json")],
                         folder / "reference.log",
                         timeout=time_left(deadline, 900))
    write_json(folder / "reference_process.json", result)
    if result.get("error") == "timeout":
        raise ExperimentError("CPU FP32 参考计算超时，尚未完成数值判断；reference.log 保留最后进度")
    if result.get("returncode") != 0:
        raise ExperimentError("独立 FP32 参考未完成或数值检查失败，详见 correctness.json 与 reference.log")
    return read_json(folder / "correctness.json")


def reuse_reference(records, baseline):
    """Use independently computed probabilities only when the entire prefix is identical."""
    from correctness import score_reference_position
    by_id = {case["request_id"]: case for case in baseline.get("cases", [])}
    if set(by_id) != {record["request_id"] for record in records}:
        return None
    cases = []
    for record in records:
        ref = by_id[record["request_id"]]
        if record["prompt_token_ids"] != ref["prompt_token_ids"] or record["token_ids"] != ref["token_ids"]:
            return None
        positions = []
        for index, (logprob, old) in enumerate(zip(record["token_logprobs"], ref["positions"])):
            score = score_reference_position(token_id=record["token_ids"][index], server_logprob=logprob,
                reference_logprob=old["reference_logprob"], reference_top1_id=old["reference_top1_id"],
                reference_top1_logprob=old["reference_top1_logprob"])
            positions.append({"generated_index": index, "input_position": len(record["prompt_token_ids"]) - 1 + index, **score})
        if len(positions) != 8 or len(record["token_logprobs"]) != 8:
            raise ExperimentError("复用参考的 token 数量不符")
        cases.append({**record, "positions": positions, "passed": all(p["passed"] for p in positions)})
    return {"passed": all(c["passed"] for c in cases), "cases": cases,
            "reference_reuse": "same prompt and generated prefixes; probabilities from independent CPU FP32 reference"}


def validate_outputs(base_url, requests, model_path, folder, baseline=None, *, deadline):
    folder.mkdir(exist_ok=False)
    records = correctness_records(base_url, requests, folder, deadline=deadline)
    reused = reuse_reference(records, baseline[0]) if baseline else None
    if reused is not None:
        reused["reference_source"] = str(baseline[1])
        reused["reference_source_sha256"] = sha256_file(baseline[1])
        write_json(folder / "correctness.json", reused)
        if not reused["passed"]:
            raise ExperimentError("重复正确性检查未通过；不继续有效性能汇总")
        print("    正确性通过：相同前缀复用独立 FP32 概率，已逐位置复核。", flush=True)
        return baseline
    report = check_reference(model_path, folder, deadline=deadline)
    return report, folder / "correctness.json"


def renamed_requests(requests, prefix, *, count=None, output_tokens=None):
    return [{**r, "request_id": f"{prefix}-{r['request_id']}",
             "max_tokens": output_tokens if output_tokens is not None else r["max_tokens"]}
            for r in (requests[:count] if count is not None else requests)]


def analyze_traces(trace_dir):
    reports = []
    all_batches = []
    all_gpu_ranges = []
    all_empty_host_ranges = []
    all_unclassified_ranges = []
    total_kernels = 0
    for path in sorted(Path(trace_dir).rglob("*")):
        if not path.is_file() or not (path.name.endswith(".json") or path.name.endswith(".json.gz")):
            continue
        opener = gzip.open if path.name.endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8") as handle:
            data = json.load(handle)
        events = data.get("traceEvents", [])
        cats = {}
        kernels = 0
        batches = []
        gpu_ranges = []
        empty_host_ranges = []
        unclassified_ranges = []
        for event in events:
            category = str(event.get("cat", ""))
            cats[category] = cats.get(category, 0) + 1
            if "kernel" in category.lower() and event.get("ph") == "X":
                kernels += 1
            match = re.fullmatch(r"execute_context_(\d+)\((\d+)\)_generation_(\d+)\((\d+)\)", str(event.get("name", "")))
            if match and event.get("ph") == "X":
                c, ct, d, dtokens = map(int, match.groups())
                row = {"trace_file": str(path.relative_to(trace_dir)), "pid": event.get("pid"),
                       "tid": event.get("tid"), "ts_us": event.get("ts"), "category": category,
                       "name": event.get("name"), "external_id": (event.get("args") or {}).get("External id"),
                       "context_requests": c, "context_tokens": ct, "decode_requests": d,
                       "decode_tokens": dtokens, "scheduled_tokens": ct + dtokens}
                if category in ("user_annotation", "cpu_op"):
                    row["host_scope_dur_us"] = event.get("dur")
                    (batches if ct + dtokens > 0 else empty_host_ranges).append(row)
                elif category == "gpu_user_annotation":
                    row["gpu_annotation_dur_us"] = event.get("dur")
                    gpu_ranges.append(row)
                else:
                    row["unclassified_dur_us"] = event.get("dur")
                    unclassified_ranges.append(row)
        total_kernels += kernels
        all_batches.extend(batches)
        all_gpu_ranges.extend(gpu_ranges)
        all_empty_host_ranges.extend(empty_host_ranges)
        all_unclassified_ranges.extend(unclassified_ranges)
        reports.append({"file": str(path.relative_to(trace_dir)), "bytes": path.stat().st_size,
                        "event_count": len(events), "categories": cats, "gpu_kernel_events": kernels,
                        "batch_annotations": len(batches), "gpu_batch_annotations": len(gpu_ranges),
                        "empty_host_annotations": len(empty_host_ranges),
                        "unclassified_batch_names": len(unclassified_ranges)})
    return {"schema_version": 2, "files": reports, "gpu_kernel_events": total_kernels, "batches": all_batches,
            "gpu_batch_ranges": all_gpu_ranges, "empty_host_ranges": all_empty_host_ranges,
            "unclassified_batch_ranges": all_unclassified_ranges,
            "passed": total_kernels > 0 and bool(all_batches),
            "scope": "batch-level only; host annotate duration is not GPU completion or client latency",
            "batch_count_definition": "non-empty Host execute scopes only; matching GPU annotations are separate ranges",
            "request_kernel_mapping": None, "absence_of_event_is_not_proof_of_absence": True}


def compare_rounds(rounds):
    # Keep per-round metrics. Do not average percentiles and label them pooled P99.
    comparisons = {}
    names = ("request_ttft_ms", "request_tpot_ms", "request_e2el_ms", "pooled_raw_itl_ms")
    for budget in BUDGETS:
        selected = [r for r in rounds if r["budget"] == budget]
        summary = {"round_count": len(selected), "round_ids": [r["round_id"] for r in selected]}
        for name in ("output_tokens_per_second",) + tuple(n + ".p50" for n in names) + tuple(n + ".p99" for n in names):
            if "." in name:
                base, key = name.split(".")
                vals = [r["summary"][base][key] for r in selected]
            else:
                vals = [r["summary"][name] for r in selected]
            vals = [v for v in vals if v is not None]
            summary[name] = {"values_by_round": vals, "median_of_round_statistics": statistics.median(vals) if vals else None,
                             "min": min(vals) if vals else None, "max": max(vals) if vals else None}
        comparisons[str(budget)] = summary
    changes = {}
    if all(comparisons[str(b)]["round_count"] == 3 for b in BUDGETS):
        for metric, values in comparisons[str(BUDGETS[0])].items():
            if not isinstance(values, dict):
                continue
            a = values["median_of_round_statistics"]
            b = comparisons[str(BUDGETS[1])][metric]["median_of_round_statistics"]
            changes[metric] = None if a in (None, 0) or b is None else (b / a - 1) * 100
    return {"by_budget": comparisons, "relative_change_percent_of_round_medians": changes,
            "p99_status": "exploratory; 48 request values per round, not established population stability",
            "range_status": "observed round min/max, not a confidence interval", "rounds": rounds}


def pack_case(case):
    """Copy only reports/source from a case; weights/cache never live in a case."""
    case = Path(case).resolve()
    exports = ROOT / "exports"
    exports.mkdir(exist_ok=True)
    output = exports / (case.name + "-" + uuid.uuid4().hex[:6] + ".zip")
    checksums = {}
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(case.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            if path.suffix in (".safetensors", ".bin", ".zip", ".pyc"):
                continue
            relative = path.relative_to(case).as_posix()
            checksums[relative] = sha256_file(path)
            archive.write(path, case.name + "/" + relative)
        archive.writestr(case.name + "/ARCHIVE_SHA256.json", json.dumps(checksums, indent=2))
    return output


def prepared_case(value=None):
    if value:
        path = Path(value).expanduser().resolve()
    else:
        pointer = read_json(ROOT / "current_run.json")
        path = (ROOT / pointer["relative_path"]).resolve()
    if not path.is_dir() or not path.is_relative_to((ROOT / "runs").resolve()):
        raise ExperimentError("--case 必须指向本包 runs/ 内的已有准备目录")
    return path


def preflight_command():
    case = new_case("preflight")
    capture_sources(case)
    info = inspect_environment(case / "environment")
    save_status(case, "preflight_passed" if info["passed"] else "preflight_blocked", reasons=info["reasons"])
    archive = pack_case(case)
    print("环境检查通过。" if info["passed"] else "环境检查未通过：" + "; ".join(info["reasons"]))
    print("返回包：", archive)
    return 0 if info["passed"] else 2


def prepare_command(args):
    case = new_case("case")
    capture_sources(case)
    write_json(case / "method.json", method())
    save_status(case, "preparing")
    try:
        info = inspect_environment(case / "environment_prepare")
        if not info["passed"]:
            raise ExperimentError("; ".join(info["reasons"]))
        print("环境通过；下载或核验固定模型（权重约 3.09 GB）……", flush=True)
        model_path, verification = obtain_model(args.model_dir)
        write_json(case / "model_verification.json", verification)
        write_json(case / "model_location.json", {"path": str(model_path), "model_id": MODEL_ID,
                                                   "revision": MODEL_REVISION})
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True, trust_remote_code=False)
        write_json(case / "inputs.json", build_inputs(tokenizer))
        save_status(case, "prepared", input_sha256=sha256_file(case / "inputs.json"))
        write_json(ROOT / "current_run.json", {"relative_path": str(case.relative_to(ROOT))}, replace=True)
        print("准备完成，尚未进行性能测量。结果目录：", case)
        print("先提交自己的事前预测，再使用 run --prediction-file 运行。")
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        write_json(case / "failure_prepare.json", {"type": type(exc).__name__, "message": str(exc), "at": utc_now()})
        save_status(case, "prepare_failed")
        print("准备停止：", str(exc), file=sys.stderr)
        return 2
    finally:
        print("返回包：", pack_case(case), flush=True)


def run_command(args):
    from client import run_batch
    case = prepared_case(args.case)
    if read_json(case / "status.json")["phase"] != "prepared":
        raise ExperimentError("只允许对 prepared 目录开始一次正式运行；重跑需重新 prepare")
    prediction_path = Path(args.prediction_file).expanduser()
    prediction = prediction_path.read_text(encoding="utf-8").strip()
    if len(prediction) < 20 or any(s in prediction for s in ("在这里填", "YOUR_PREDICTION", "TODO")):
        raise ExperimentError("请先写下自己的预测、依据与可推翻条件；不接受空白或占位文本")
    check_source_identity(case)
    inputs = read_json(case / "inputs.json")
    if sha256_file(case / "inputs.json") != read_json(case / "status.json")["input_sha256"]:
        raise ExperimentError("prepare 后输入文件发生变化")
    write_json(case / "prediction.json", {"text": prediction, "saved_at": utc_now(),
                                          "provenance": "learner-supplied text; independence reviewed in conversation"})
    save_status(case, "running")
    rounds = []
    try:
        info = inspect_environment(case / "environment_run")
        if not info["passed"]:
            raise ExperimentError("; ".join(info["reasons"]))
        before = read_json(case / "environment_prepare" / "environment.json")
        if info["packages"] != before["packages"] or info.get("device_visibility") != before.get("device_visibility"):
            raise ExperimentError("prepare 后软件或可见设备设置改变；请重新 prepare")
        if gpu_identity(info) != gpu_identity(before):
            raise ExperimentError("prepare 后可见 GPU 身份或规格改变；请重新 prepare")
        model_path = Path(read_json(case / "model_location.json")["path"])
        write_json(case / "model_reverification.json", verify_model(model_path))
        checked = {}
        deadline = time.monotonic() + 80 * 60
        for index, budget in enumerate(ORDER):
            if time.monotonic() > deadline:
                raise ExperimentError("本次运行达到 80 分钟控制界限；保留已完成结果")
            name = f"round-{index+1:02d}-budget-{budget}"
            folder = case / name
            print(f"[{index+1}/{len(ORDER)}] 预算 {budget}：启动、核验、预热、测量", flush=True)
            with serve(model_path, budget, folder, deadline=deadline) as base_url:
                checked[budget] = validate_outputs(base_url, inputs["correctness"], model_path,
                    folder / "validation_before", checked.get(budget), deadline=deadline)
                print("    开始预热：8 条请求。", flush=True)
                warm = run_batch(base_url, SERVER_MODEL_NAME,
                                 renamed_requests(inputs["requests"], name + "-warm", count=8, output_tokens=32),
                                 CONCURRENCY, folder / "warmup.jsonl", phase="warmup", deadline_monotonic=deadline)
                write_json(folder / "warmup_summary.json", warm)
                if warm["failure_count"]:
                    raise ExperimentError("预热请求失败，未进入正式计时")
                print("    开始正式计时：48 条请求，并发上限 8。", flush=True)
                summary = run_batch(base_url, SERVER_MODEL_NAME, renamed_requests(inputs["requests"], name),
                                    CONCURRENCY, folder / "requests.jsonl", phase="measure", deadline_monotonic=deadline)
                write_json(folder / "summary.json", summary)
                if summary["failure_count"]:
                    raise ExperimentError("正式请求有失败；保留数据，不生成有效性能比较")
                print("    本轮计时结束，进行末尾正确性检查。", flush=True)
                checked[budget] = validate_outputs(base_url, inputs["correctness"], model_path,
                    folder / "validation_after", checked[budget], deadline=deadline)
                rounds.append({"round_id": name, "budget": budget, "summary": summary})
            save_status(case, "running", finished_rounds=len(rounds))
            # Archive after every round, so an instance expiry needn't lose all evidence.
            archive = pack_case(case)
            print("本轮已保存：", archive, flush=True)
        write_json(case / "performance.json", compare_rounds(rounds))
        print("干净测量完成；开始单独的短 trace，trace 时延不纳入上面的结果。", flush=True)
        time_left(deadline, 1)
        folder = case / "profile-budget-2048"
        with serve(model_path, 2048, folder, profile=True, deadline=deadline) as base_url:
            warm = run_batch(base_url, SERVER_MODEL_NAME,
                             renamed_requests(inputs["requests"], "profile-warm", count=4, output_tokens=16),
                             4, folder / "warmup.jsonl", phase="profile_warmup", deadline_monotonic=deadline)
            if warm["failure_count"]:
                raise ExperimentError("trace 预热失败")
            write_json(folder / "capture_start.json", {"utc": utc_now(), "monotonic_s": time.monotonic(),
                "result": http_json(base_url, "/start_profile", post=True, timeout=time_left(deadline, 90))})
            try:
                profile = run_batch(base_url, SERVER_MODEL_NAME,
                                    renamed_requests(inputs["requests"], "profile", count=4, output_tokens=16),
                                    4, folder / "requests.jsonl", phase="profile", deadline_monotonic=deadline)
                write_json(folder / "client_observations_not_benchmark.json", profile)
            finally:
                write_json(folder / "capture_stop.json", {"utc": utc_now(), "monotonic_s": time.monotonic(),
                    "result": http_json(base_url, "/stop_profile", post=True, timeout=120)})
            if profile["failure_count"]:
                raise ExperimentError("trace 窗口存在失败请求")
        traces = analyze_traces(folder / "traces")
        write_json(folder / "trace_index.json", traces)
        if not traces["passed"]:
            save_status(case, "measured_trace_incomplete", performance_valid=True,
                        reason="未同时发现 GPU kernel 与批次标注；HTTP200 不等于成功采集")
            print("服务测量已保存，GPU trace 尚未验证成功，请返回完整包。", flush=True)
            return 2
        save_status(case, "measured", performance_valid=True, trace_captured=True,
                    learner_interpretation="pending", course_completion="not asserted")
        print("采集完成；请返回包并在对话里解释结果。", flush=True)
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        write_json(case / "failure_run.json", {"type": type(exc).__name__, "message": str(exc),
                                              "at": utc_now(), "completed_rounds": len(rounds)})
        save_status(case, "run_failed", completed_rounds=len(rounds),
                    performance_file_exists=(case / "performance.json").exists())
        print("运行停止：", str(exc), file=sys.stderr)
        return 2
    finally:
        print("返回包：", pack_case(case), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="W4-U2 单卡服务预算对照（不自动安装依赖）")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("preflight", help="仅检查环境并生成返回包，不下载模型")
    prepare = sub.add_parser("prepare", help="检查环境、下载/验证固定模型并生成固定输入")
    prepare.add_argument("--model-dir", help="可选：已有的同 revision 本地模型目录，仍逐文件验证")
    run = sub.add_parser("run", help="保存事前预测后执行正确性、干净计时和短 trace")
    run.add_argument("--case", help="已准备的 runs/ 目录；默认最近一次成功 prepare")
    run.add_argument("--prediction-file", required=True, help="你自己写的 UTF-8 预测文本")
    pack = sub.add_parser("pack", help="把已存在结果重新打包，不重跑、不改原始文件")
    pack.add_argument("--case", help="默认最近一次成功 prepare")
    args = parser.parse_args(argv)
    try:
        if args.command == "preflight":
            return preflight_command()
        if args.command == "prepare":
            return prepare_command(args)
        if args.command == "run":
            return run_command(args)
        print("返回包：", pack_case(prepared_case(args.case)))
        return 0
    except (ExperimentError, FileNotFoundError, ValueError, OSError) as exc:
        print("未执行：", str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
