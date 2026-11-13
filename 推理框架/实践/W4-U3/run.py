#!/usr/bin/env python3
"""W4-U3-P1: paired GPU BF16 / official AWQ deployment comparison.

No dependency installation, full-model CPU reference, or automatic cloud access.
Preparation is separate from prediction-gated GPU checks and measurements.
"""
from __future__ import annotations
import argparse
import contextlib
import datetime as dt
import hashlib
import http.client
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import random
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
from compatibility import profile_for_version, missing_cli_flags

ROOT = Path(__file__).resolve().parent
REVISION = "2026-11-13.5"
SEED = 20261112  # preserve the U2 performance workload
BUDGET = 2048
VARIANTS = ("bf16", "awq")
ORDER = ("bf16", "awq", "awq", "bf16", "bf16", "awq")
CONCURRENCY = 8
REQUEST_COUNT = 48
MAX_MODEL_LEN = 4096
OUTPUT_TOKENS = 128
SERVER_MODEL_NAME = "w4-u3-qwen"
SOURCE_FILES = (
    "run.py", "client.py", "configuration.py", "quality.py", "quant_reference.py", "memory.py", "compatibility.py",
    "test_driver.py", "test_client.py", "test_configuration.py", "test_quality.py",
    "test_quant_reference.py", "test_memory.py", "test_compatibility.py", "test_download.py", "models_manifest.json", "source_provenance.json", "README.md",
)
SAFE_DEVICE_ENV = ("HIP_VISIBLE_DEVICES", "ROCR_VISIBLE_DEVICES", "CUDA_VISIBLE_DEVICES")

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

def gpu_identity(info):
    return [{k: device.get(k) for k in ("index", "name", "total_memory_bytes", "gcn_arch", "uuid", "pci_bus_id")}
            for device in info.get("torch_probe", {}).get("devices", [])]

def inspect_environment(folder):
    from memory import normalize_bdf
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
    for device in info.get("torch_probe", {}).get("devices", []):
        original = device.get("pci_bus_id")
        device["pci_bus_id"] = normalize_bdf(original)
        if device["pci_bus_id"] is None:
            device["pci_bus_id_error"] = "HIP PCI address unavailable or unrecognized; memory attribution remains unverified"
    if shutil.which("rocm-smi"):
        write_json(folder / "rocm_smi.json", run_capture(["rocm-smi"], timeout=30))
    if packages.get("vllm"):
        help_result = run_capture([sys.executable, "-m", "vllm.entrypoints.cli.main", "serve", "--help=all"], timeout=120)
        help_text = help_result.get("stdout", "")
        info["cli_help_ok"] = help_result.get("returncode") == 0
        try:
            info["vllm_profile"] = profile_for_version(packages["vllm"])
            info["missing_flags"] = missing_cli_flags(help_text,packages["vllm"])
        except ValueError as exc:
            info["vllm_profile"] = None
            info["profile_error"] = str(exc)
            info["missing_flags"] = []
        write_json(folder / "cli_help.json", help_result)
    info["reasons"] = environment_reasons(info)
    info["passed"] = not info["reasons"]
    write_json(folder / "environment.json", info)
    return info

def verify_model(model_dir, manifest=None):
    manifest = manifest or read_json(ROOT / "models_manifest.json")["models"]["bf16"]
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

def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

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

def renamed_requests(requests, prefix, *, count=None, output_tokens=None):
    return [{**r, "request_id": f"{prefix}-{r['request_id']}",
             "max_tokens": output_tokens if output_tokens is not None else r["max_tokens"]}
            for r in (requests[:count] if count is not None else requests)]

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


TORCH_PROBE = r'''
import ctypes, json, torch
r = {'torch_version': str(torch.__version__), 'torch_git': getattr(torch.version,'git_version',None),
     'hip_build': torch.version.hip, 'cuda_build': torch.version.cuda,
     'gpu_available': torch.cuda.is_available(), 'device_count': torch.cuda.device_count(), 'devices': []}
for i in range(r['device_count']):
    p = torch.cuda.get_device_properties(i)
    free,total = torch.cuda.mem_get_info(i)
    d = {'index':i, 'name':p.name, 'total_memory_bytes':p.total_memory,
         'free_memory_bytes':free, 'reported_total_bytes':total,
         'gcn_arch':getattr(p,'gcnArchName',None),
         'uuid':str(p.uuid) if getattr(p,'uuid',None) is not None else None, 'pci_bus_id':None}
    try:
        hip = ctypes.CDLL('libamdhip64.so')
        fn = hip.hipDeviceGetPCIBusId
        fn.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        fn.restype = ctypes.c_int
        buf = ctypes.create_string_buffer(64)
        if fn(buf, len(buf), i) == 0:
            d['pci_bus_id'] = buf.value.decode('ascii')
    except (OSError, AttributeError, UnicodeError):
        pass
    r['devices'].append(d)
if r['gpu_available']:
    torch.backends.cuda.matmul.allow_tf32 = False
    r['bf16_supported'] = bool(torch.cuda.is_bf16_supported())
    for dtype in (torch.bfloat16, torch.float16, torch.float32):
        x = torch.ones((2,2), device='cuda', dtype=dtype)
        r[str(dtype).split('.')[-1]+'_smoke_passed'] = bool(torch.equal(x @ x, torch.full_like(x,2.)))
    r['bf16_smoke_passed'] = r['bfloat16_smoke_passed']
print('W4_ENV_JSON='+json.dumps(r))
'''


def environment_reasons(info):
    reasons = []
    packages = info.get("packages", {})
    try:
        profile_for_version(packages.get("vllm") or "")
    except ValueError as exc:
        reasons.append(str(exc)+"；本包不自动安装或升级")
    for name in ("torch", "transformers", "huggingface_hub", "safetensors"):
        if not packages.get(name):
            reasons.append(f"镜像缺少 {name}")
    gpu = info.get("torch_probe") or {}
    if not gpu.get("hip_build"):
        reasons.append("未确认 PyTorch ROCm/HIP 构建")
    if not gpu.get("gpu_available") or gpu.get("device_count") != 1:
        reasons.append("需要当前容器只暴露一张已分配 GPU；不转为 CPU 推理")
    for name in ("bf16_supported", "bf16_smoke_passed", "float16_smoke_passed", "float32_smoke_passed"):
        if not gpu.get(name):
            reasons.append(f"GPU 功能检查未通过：{name}")
    devices = gpu.get("devices") or []
    if devices and devices[0].get("total_memory_bytes", 0) < 12 * 1024**3:
        reasons.append("GPU 显存低于本包保守预检门槛 12 GiB")
    if info.get("disk_free_bytes", 0) < 16 * 1024**3:
        reasons.append("当前文件系统可用空间低于 16 GiB")
    if not info.get("cli_help_ok"):
        reasons.append("vLLM CLI 检查失败")
    if info.get("missing_flags"):
        reasons.append("CLI 缺少所需参数：" + ", ".join(info["missing_flags"]))
    return reasons


def model_manifests():
    return read_json(ROOT / "models_manifest.json")["models"]


def method(vllm_version="0.26.0"):
    from quant_reference import reference_policy
    manifests = model_manifests()
    profile = profile_for_version(vllm_version)
    return {
        "contract": "W4-U3-P1", "contract_version": 1, "package_revision": REVISION,
        "models": {k:{"model_id":v["model_id"], "revision":v["revision"]} for k,v in manifests.items()},
        "vllm_target": profile["version"], "vllm_profile":profile,
        "source_boundary": read_json(ROOT / "models_manifest.json")["source_boundary"],
        "precision": {"bf16":"bfloat16", "awq_preference":["bfloat16","float16"],
                      "fallback":"only a reported compatibility failure; never after numerical failure",
                      "reference":"one projection, independent unpack + GPU FP32; no CPU model"},
        "reference": reference_policy(), "seed":SEED, "budget":BUDGET, "run_order":list(ORDER),
        "requests_per_round":REQUEST_COUNT, "prompt_lengths":[256,3072], "output_tokens":OUTPUT_TOKENS,
        "prompt_mix":"alternating short/long, 24 each; fixed token IDs reused for both variants",
        "ignore_eos":True, "concurrency":CONCURRENCY,
        "arrival":"finite-pool closed-loop, all 48 requests enqueued at batch start",
        "max_model_len":MAX_MODEL_LEN, "max_num_seqs":16, "tensor_parallel_size":1,
        "block_size":16, "kv_cache_dtype":"auto", "gpu_memory_utilization":0.70,
        "kv_cache_memory_bytes":None, "enforce_eager":True, "async_scheduling":False,
        "prefix_caching":False, "chunked_prefill":True,
        "warmup":"first 8 performance prompts, 32 output tokens, on every fresh service",
        "quality":{"cases":32,"labels":"deterministic constructed records, independent of both models",
                   "max_tokens":32,"ignore_eos":False,"scoring":"strip only; exact match; truncation is incorrect",
                   "when":"once per variant before timing", "score_gate":None,
                   "scope":"small sanity task set; no general quality or production non-inferiority claim"},
        "round_smoke":"one fixed 32-token prompt, 8 output tokens and finite logprobs before/after timing; not an independent reference",
        "memory":{"interval_seconds":1.0,"scope":"external device sampling around the clean request batch",
                  "peak":"maximum observed sample, not exact instantaneous peak; other processes may contribute",
                  "separate_fields":["loader-reported model memory","KV capacity","sampled device memory"]},
        "profiler":False,"full_model_cpu_reference":False,
        "statistics":"per-round distributions; medians/ranges of round statistics; P99 exploratory",
        "decision":"valid evidence and explanation, no required speedup or quality improvement",
        "network":"HTTP loopback; no public serving endpoint", "run_deadline_minutes":80,
        "estimated_download_bytes":sum(f["bytes"] for m in manifests.values() for f in m["files"]),
    }


def model_file_matches(path, item):
    path=Path(path)
    if not path.is_file() or path.stat().st_size!=item["bytes"]:
        return False
    if "sha256" in item:
        return sha256_file(path)==item["sha256"]
    return git_blob_sha1(path)==item["git_blob_sha1"]


def transient_download_error(exc):
    seen=set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        status=getattr(getattr(exc,"response",None),"status_code",None)
        if isinstance(status,int):
            return status in (429,500,502,503,504)
        if isinstance(exc,TimeoutError) or type(exc).__name__ in ("ConnectTimeout","ReadTimeout","WriteTimeout","PoolTimeout","TimeoutException"):
            return True
        exc=exc.__cause__
    return False


def acquisition_event(path, **event):
    if path is None:
        return
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as out:
        out.write(json.dumps({"at":utc_now(),**event},ensure_ascii=False,allow_nan=False)+"\n")


def reuse_shared_model_files(variant, destination, manifests):
    """Reuse only byte-identical public artifacts, never filenames alone."""
    reused=[]
    for item in manifests[variant]["files"]:
        target=destination/item["name"]
        if model_file_matches(target,item):
            continue
        for other,manifest in manifests.items():
            if other==variant or item not in manifest["files"]:
                continue
            source=ROOT/"cache"/other/manifest["revision"]/item["name"]
            if not model_file_matches(source,item):
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            temporary=target.with_name(target.name+".reuse-"+uuid.uuid4().hex[:8])
            try:
                shutil.copyfile(source,temporary)
                if not model_file_matches(temporary,item):
                    raise ExperimentError("共享缓存复制后的哈希不符："+item["name"])
                os.replace(temporary,target)
            finally:
                temporary.unlink(missing_ok=True)
            reused.append(item["name"])
            break
    return reused


def obtain_model(variant, model_dir=None, *, audit_path=None):
    manifests=model_manifests()
    manifest = manifests[variant]
    if model_dir:
        path = Path(model_dir).expanduser().resolve()
        acquisition_event(audit_path,mode="supplied_directory",variant=variant)
    else:
        endpoint = urllib.parse.urlparse(os.environ.get("HF_ENDPOINT", "https://huggingface.co"))
        if (endpoint.scheme != "https" or not endpoint.hostname or endpoint.username or endpoint.password
                or endpoint.query or endpoint.fragment):
            raise ExperimentError("HF_ENDPOINT 必须是无凭据、无查询参数的 HTTPS 地址")
        path=(ROOT/"cache"/variant/manifest["revision"]).resolve()
        path.mkdir(parents=True,exist_ok=True)
        reused=reuse_shared_model_files(variant,path,manifests)
        acquisition_event(audit_path,mode="verified_shared_cache",variant=variant,files=reused)
        for attempt in range(1,4):
            pending=[f for f in manifest["files"] if not model_file_matches(path/f["name"],f)]
            if not pending:
                acquisition_event(audit_path,mode="verified_cache_complete",variant=variant)
                break
            from huggingface_hub import snapshot_download
            # A corrupt file can have valid Hub ETag metadata. Force redownload
            # for this pending subset rather than accepting that local metadata.
            force=any((path/f["name"]).exists() for f in pending)
            names=[f["name"] for f in pending]
            acquisition_event(audit_path,mode="download_attempt",variant=variant,attempt=attempt,
                              files=names,force_download=force,endpoint=endpoint.geturl())
            try:
                snapshot_download(repo_id=manifest["model_id"],revision=manifest["revision"],
                    allow_patterns=names,local_dir=str(path),max_workers=2,token=False,force_download=force,
                    endpoint=endpoint.geturl())
                acquisition_event(audit_path,mode="download_completed",variant=variant,attempt=attempt)
                break
            except Exception as exc:
                retryable=transient_download_error(exc)
                acquisition_event(audit_path,mode="download_error",variant=variant,attempt=attempt,
                                  exception_type=type(exc).__name__,message=str(exc),retryable=retryable)
                if not retryable or attempt==3:
                    raise
                delay=2**attempt
                print(f"    {variant} 下载遇到临时错误；{delay}秒后重试（最多3次，保留已校验文件）。",flush=True)
                time.sleep(delay)
    return path, verify_model(path, manifest)


def verify_pair(paths):
    tokenizer_files = ("tokenizer.json","tokenizer_config.json","merges.txt","vocab.json")
    hashes = {n:{v:sha256_file(paths[v]/n) for v in VARIANTS} for n in tokenizer_files}
    if any(h["bf16"] != h["awq"] for h in hashes.values()):
        raise ExperimentError("两份发布物的 tokenizer / chat template 不一致")
    base = read_json(paths["bf16"] / "config.json")
    quant = read_json(paths["awq"] / "config.json")
    allowed = {"quantization_config","torch_dtype","transformers_version"}
    differences = sorted(k for k in set(base)|set(quant) if base.get(k)!=quant.get(k))
    if set(differences)-allowed:
        raise ExperimentError("模型结构存在未约定差异")
    q = quant.get("quantization_config",{})
    expected = {"bits":4,"group_size":128,"zero_point":True,"quant_method":"awq","version":"gemm"}
    if any(type(q.get(k)) is not type(v) or q.get(k)!=v for k,v in expected.items()):
        raise ExperimentError("AWQ 量化格式不符合已核定配置")
    return {"tokenizer_sha256":hashes,"config_differences":differences,
            "quantization_config":q,"identical_base_weight_revision_proven":False}


def build_inputs(tokenizer):
    words = ["memory","compute","request","queue","latency","token","stream","batch",
             "model","device","kernel","server","measure","cache","buffer","schedule"]
    def tokens(index, length):
        rng = random.Random(SEED+index)
        text = "Continue the following synthetic technical notes in English.\n"
        text += "\n".join(f"Note {j}: "+" ".join(rng.choice(words) for _ in range(16))+"." for j in range(260))
        ids = tokenizer.encode(text, add_special_tokens=False)
        if len(ids)<length:
            raise ExperimentError("合成输入不足指定长度")
        return ids[:length]
    requests = [{"request_id":f"work-{i:03d}","prompt_token_ids":tokens(i,256 if i%2==0 else 3072),
                 "max_tokens":OUTPUT_TOKENS,"extra_body":{"add_special_tokens":False,"skip_special_tokens":False}}
                for i in range(REQUEST_COUNT)]
    return {"schema_version":1,"seed":SEED,"requests":requests,
            "smoke":{"request_id":"round-smoke","prompt_token_ids":tokens(1000,32),"max_tokens":8,
                     "extra_body":{"logprobs":1,"add_special_tokens":False,"skip_special_tokens":False}}}


def server_command(model_path, variant, dtype, port, *, vllm_version="0.26.0"):
    if variant not in VARIANTS or dtype not in ("bfloat16","float16") or (variant=="bf16" and dtype!="bfloat16"):
        raise ExperimentError("未约定的模型／dtype")
    profile=profile_for_version(vllm_version)
    cmd = [sys.executable,"-m","vllm.entrypoints.cli.main","serve",str(model_path),
           "--served-model-name",SERVER_MODEL_NAME,"--host","127.0.0.1","--port",str(port),
           "--dtype",dtype,"--tensor-parallel-size","1","--pipeline-parallel-size","1",
           "--max-model-len",str(MAX_MODEL_LEN),"--max-num-seqs","16","--max-num-batched-tokens",str(BUDGET),
           "--gpu-memory-utilization","0.70","--block-size","16",
           "--enable-chunked-prefill",profile["disable_prefix_caching"],"--no-async-scheduling",
           "--enforce-eager","--generation-config","vllm","--seed",str(SEED),
           profile["disable_log_requests"],"--logprobs-mode","raw_logprobs"]
    if variant=="awq":
        cmd += ["--quantization","awq"]
    return cmd


@contextlib.contextmanager
def serve(model_path, variant, dtype, folder, *, deadline, vllm_version):
    from configuration import project_runtime_config, validate_runtime_config
    from memory import parse_server_memory
    folder.mkdir(parents=True,exist_ok=False)
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    cmd = server_command(model_path,variant,dtype,port,vllm_version=vllm_version)
    overrides = {"VLLM_SERVER_DEV_MODE":"1","VLLM_CUSTOM_SCOPES_FOR_PROFILING":"0",
                 "HF_HUB_OFFLINE":"1","TRANSFORMERS_OFFLINE":"1","VLLM_USE_TRITON_AWQ":"1"}
    env = os.environ.copy()
    env.pop("VLLM_API_KEY",None)
    env.update(overrides)
    write_json(folder/"command.json",{"argv":cmd,"environment_overrides":overrides,"started_at":utc_now(),
               "variant":variant,"dtype":dtype,"vllm_profile":profile_for_version(vllm_version),
               "VLLM_API_KEY_in_child":"unset"})
    process = None
    try:
        with (folder/"server.log").open("x",encoding="utf-8") as log:
            process = subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,cwd=ROOT,start_new_session=True)
            startup = min(deadline,time.monotonic()+600)
            while time.monotonic()<startup:
                if process.poll() is not None:
                    raise ExperimentError(f"{variant} 服务启动失败，见 {folder.name}/server.log")
                try:
                    http_json(base_url,"/health",timeout=time_left(startup,2))
                    break
                except (OSError,ValueError,ExperimentError):
                    time.sleep(min(1,max(0,startup-time.monotonic())))
            else:
                raise ExperimentError("服务启动超过600秒或本轮总期限")
            projected = project_runtime_config(http_json(base_url,"/server_info?config_format=json",timeout=time_left(deadline,60)))
            write_json(folder/"effective_config.json",projected)
            errors = validate_runtime_config(projected,BUDGET,variant=variant,dtype=dtype)
            if Path(projected.get("model",{}).get("model","")).resolve()!=Path(model_path).resolve():
                errors.append("实际模型路径与已核对快照不符")
            if errors:
                raise ExperimentError("生效配置不符："+"; ".join(errors))
            print(f"    {variant}/{dtype} 服务就绪，预算2048，配置已核对。",flush=True)
            yield base_url
    finally:
        if process is not None:
            stop_process(process)
            write_json(folder/"process_exit.json",{"returncode":process.returncode,"stopped_at":utc_now()})
        log_path = folder/"server.log"
        if log_path.exists():
            write_json(folder/"server_memory.json",parse_server_memory(log_path.read_text(encoding="utf-8",errors="replace")))


def run_reference_logged(command, log_path, timeout):
    start = time.monotonic()
    deadline = start+timeout
    heartbeat = start+30
    env = os.environ.copy()
    env.update({"HF_HUB_OFFLINE":"1","TRANSFORMERS_OFFLINE":"1","VLLM_USE_TRITON_AWQ":"1"})
    timed_out = False
    with Path(log_path).open("xb") as log:
        process = subprocess.Popen(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        try:
            while process.poll() is None:
                now=time.monotonic()
                if now>=deadline:
                    timed_out=True
                    break
                if now>=heartbeat:
                    print(f"    GPU 局部参考仍在运行（{int(now-start)}秒）；日志已实时保存。",flush=True)
                    heartbeat=now+30
                time.sleep(min(0.2,max(0.01,deadline-now)))
        finally:
            stop_process(process)
    return {"argv":command,"returncode":None if timed_out else process.returncode,"timeout":timed_out,
            "elapsed_seconds":time.monotonic()-start,"full_model_cpu_reference":False}


def select_awq_dtype(model_path, folder, deadline):
    folder.mkdir(parents=True,exist_ok=False)
    attempts=[]
    for dtype in ("bfloat16","float16"):
        out=folder/(dtype+".json")
        cmd=[sys.executable,"-u",str(ROOT/"quant_reference.py"),"--model-dir",str(model_path),"--dtype",dtype,"--output",str(out)]
        print(f"GPU 局部独立参考：{dtype}，M=1/256。",flush=True)
        process=run_reference_logged(cmd,folder/(dtype+".log"),time_left(deadline,360))
        write_json(folder/(dtype+"_process.json"),process)
        report=read_json(out) if out.exists() else {"status":"error","failure_kind":"internal"}
        attempts.append({"dtype":dtype,"status":report.get("status"),"failure_kind":report.get("failure_kind")})
        if process["returncode"]==0 and report.get("status")=="passed":
            result={"dtype":dtype,"attempts":attempts,"reference_report":out.name,
                    "activation_dtype_matches_bf16":dtype=="bfloat16",
                    "full_model_cpu_reference":False}
            write_json(folder/"selection.json",result)
            return result
        if (dtype=="bfloat16" and report.get("status")=="unsupported"
                and report.get("failure_kind")=="compatibility" and report.get("fp16_retry_eligible") is True
                and not process["timeout"]):
            print("BF16 路径报告兼容性限制，按事前约定尝试FP16；保留原失败。",flush=True)
            continue
        raise ExperimentError(f"AWQ {dtype} 局部参考未通过（{report.get('status')}）；停止性能测量，不放宽容差")
    raise ExperimentError("未找到本包支持的 AWQ 执行 dtype")


def smoke(base_url, request, folder, *, deadline):
    from client import request_once
    record=request_once(base_url,SERVER_MODEL_NAME,request,timeout=time_left(deadline,120),stream=False)
    write_json(folder,record)
    if not record["success"]:
        raise ExperimentError("短生成协议检查失败")
    probabilities=[v for block in record.get("logprobs",[]) for v in block.get("token_logprobs",[])]
    if len(probabilities)!=request["max_tokens"] or any(type(v) not in (float,int) or not math.isfinite(v) for v in probabilities):
        raise ExperimentError("短生成 logprob 缺失或存在非有限值")


def compare_rounds(rounds):
    comparisons={}
    metrics=("output_tokens_per_second",)+tuple(n+"."+q for n in
             ("request_ttft_ms","request_tpot_ms","request_e2el_ms","pooled_raw_itl_ms") for q in ("p50","p99"))
    for variant in VARIANTS:
        selected=[r for r in rounds if r["variant"]==variant]
        group={"round_count":len(selected),"round_ids":[r["round_id"] for r in selected]}
        for metric in metrics:
            parts=metric.split(".")
            vals=[r["summary"][parts[0]][parts[1]] if len(parts)==2 else r["summary"][parts[0]] for r in selected]
            vals=[v for v in vals if v is not None]
            group[metric]={"values_by_round":vals,"median_of_round_statistics":statistics.median(vals) if vals else None,
                           "min":min(vals) if vals else None,"max":max(vals) if vals else None}
        comparisons[variant]=group
    changes={}
    if all(comparisons[v]["round_count"]==3 for v in VARIANTS):
        for metric in metrics:
            b=comparisons["bf16"][metric]["median_of_round_statistics"]
            q=comparisons["awq"][metric]["median_of_round_statistics"]
            changes[metric]=None if b in (None,0) or q is None else (q/b-1)*100
    return {"by_variant":comparisons,"relative_change_percent_of_round_medians":changes,"rounds":rounds,
            "p99_status":"exploratory; not established population stability",
            "range_status":"observed min/max, not a confidence interval",
            "attribution":"fixed official deployments; exact common source weight revision not proven"}


def memory_evidence_complete(round_record, expected_bdf):
    from memory import normalize_bdf
    m=round_record.get("memory",{})
    devices=m.get("devices",[])
    if (m.get("status")!="ok" or m.get("thread_stopped") is not True
            or m.get("runtime_device_mapping_confirmed") is not True
            or m.get("scope")!="matched_pci_bdf" or len(devices)!=1):
        return False
    d=devices[0]
    totals=d.get("total_bytes_values",[])
    bdf=normalize_bdf(expected_bdf)
    if (not bdf or normalize_bdf(d.get("pci_bdf"))!=bdf or d.get("valid_samples",0)<1
            or d.get("sampled_max_used_bytes") is None or len(totals)!=1
            or type(totals[0]) is not int or totals[0]<=0):
        return False
    server=round_record.get("server_memory",{})
    return all(type(server.get(k)) in (int,float) and math.isfinite(server[k]) and server[k]>0
               for k in ("model_loading_gib","kv_capacity_tokens"))


SEALED_FILES=("method.json","inputs.json","quality_inputs.json","model_locations.json","pair_verification.json")


def preflight_command():
    case=new_case("preflight")
    try:
        capture_sources(case)
        info=inspect_environment(case/"environment")
        save_status(case,"preflight_passed" if info["passed"] else "preflight_blocked",reasons=info["reasons"])
        print("环境检查通过。" if info["passed"] else "环境检查未通过："+"; ".join(info["reasons"]))
        return 0 if info["passed"] else 2
    except (Exception,KeyboardInterrupt) as exc:
        write_json(case/"failure_preflight.json",{"type":type(exc).__name__,"message":str(exc)})
        save_status(case,"preflight_failed")
        return 2
    finally:
        print("返回包：",pack_case(case),flush=True)


def prepare_command(args):
    from quality import build_quality_inputs
    case=new_case("case")
    try:
        capture_sources(case)
        save_status(case,"preparing")
        info=inspect_environment(case/"environment_prepare")
        if not info["passed"]:
            raise ExperimentError("; ".join(info["reasons"]))
        write_json(case/"method.json",method(info["packages"]["vllm"]))
        paths={}
        for variant in VARIANTS:
            print(f"下载／校验固定 {variant} 发布物……",flush=True)
            paths[variant],verification=obtain_model(variant,getattr(args,variant+"_dir"),
                                                   audit_path=case/(variant+"_acquisition.jsonl"))
            write_json(case/(variant+"_verification.json"),verification)
        write_json(case/"pair_verification.json",verify_pair(paths))
        write_json(case/"model_locations.json",{v:str(p) for v,p in paths.items()})
        from transformers import AutoTokenizer
        tokenizer=AutoTokenizer.from_pretrained(str(paths["bf16"]),local_files_only=True,trust_remote_code=False)
        write_json(case/"inputs.json",build_inputs(tokenizer))
        write_json(case/"quality_inputs.json",build_quality_inputs(tokenizer))
        write_json(case/"prepared_data_manifest.json",{n:sha256_file(case/n) for n in SEALED_FILES})
        save_status(case,"prepared")
        write_json(ROOT/"current_run.json",{"relative_path":str(case.relative_to(ROOT))},replace=True)
        print("准备完成，尚未加载完整模型做推理。先给出预测，再执行run。",flush=True)
        return 0
    except (Exception,KeyboardInterrupt) as exc:
        write_json(case/"failure_prepare.json",{"type":type(exc).__name__,"message":str(exc),"at":utc_now()})
        save_status(case,"prepare_failed")
        print("准备停止：",str(exc),file=sys.stderr)
        return 2
    finally:
        print("返回包：",pack_case(case),flush=True)


def validate_prepared(case):
    if read_json(case/"status.json").get("phase")!="prepared":
        raise ExperimentError("只允许对prepared目录运行一次；重跑请重新prepare")
    check_source_identity(case)
    seals=read_json(case/"prepared_data_manifest.json")
    if set(seals)!=set(SEALED_FILES) or any(sha256_file(case/n)!=seals[n] for n in SEALED_FILES):
        raise ExperimentError("准备后的方法、输入或模型位置发生变化；请重新prepare")
    prepared_version=read_json(case/"environment_prepare"/"environment.json")["packages"]["vllm"]
    if read_json(case/"method.json")!=method(prepared_version):
        raise ExperimentError("固定方法与包内方法不一致")


def run_command(args):
    from client import run_batch
    from quality import evaluate_quality,compare_quality
    from memory import MemorySampler
    case=prepared_case(args.case)
    validate_prepared(case)
    prediction=Path(args.prediction_file).expanduser().read_text(encoding="utf-8")
    if len(prediction.strip())<20 or any(x in prediction for x in ("YOUR_PREDICTION","在这里填","TODO")):
        raise ExperimentError("请先提供自己的预测、依据及可推翻条件，不能使用占位文本")
    write_json(case/"run_started.json",{"at":utc_now()})
    write_json(case/"prediction.json",{"text":prediction,"saved_at":utc_now(),"provenance":"learner supplied; reviewed in conversation"})
    save_status(case,"running")
    rounds=[]
    try:
        inputs=read_json(case/"inputs.json")
        tasks=read_json(case/"quality_inputs.json")
        info=inspect_environment(case/"environment_run")
        if not info["passed"]:
            raise ExperimentError("; ".join(info["reasons"]))
        before=read_json(case/"environment_prepare"/"environment.json")
        if info["packages"]!=before["packages"] or info["device_visibility"]!=before["device_visibility"] or gpu_identity(info)!=gpu_identity(before):
            raise ExperimentError("prepare 后软件或GPU身份变化；请重新prepare")
        paths={v:Path(p) for v,p in read_json(case/"model_locations.json").items()}
        for v in VARIANTS:
            write_json(case/(v+"_reverification.json"),verify_model(paths[v],model_manifests()[v]))
        deadline=time.monotonic()+80*60
        choice=select_awq_dtype(paths["awq"],case/"gpu_reference",deadline)
        dtypes={"bf16":"bfloat16","awq":choice["dtype"]}
        write_json(case/"execution_choice.json",{**choice,"source_boundary":read_json(case/"method.json")["source_boundary"]})
        quality={}
        for variant in VARIANTS:
            folder=case/("validation-"+variant)
            print(f"{variant}：兼容性与32条固定任务，质量分数不当作性能门槛。",flush=True)
            with serve(paths[variant],variant,dtypes[variant],folder,deadline=deadline,
                       vllm_version=info["packages"]["vllm"]) as url:
                smoke(url,inputs["smoke"],folder/"generation_smoke.json",deadline=deadline)
                quality[variant]=evaluate_quality(url,SERVER_MODEL_NAME,tasks,folder/"quality",deadline)
                if not quality[variant]["valid_for_quality_comparison"]:
                    raise ExperimentError("质量请求的传输／协议不完整；不继续性能比较")
        write_json(case/"quality_comparison.json",compare_quality(quality["bf16"],quality["awq"]))
        bdf=info["torch_probe"]["devices"][0].get("pci_bus_id")
        for index,variant in enumerate(ORDER):
            time_left(deadline,1)
            name=f"round-{index+1:02d}-{variant}"
            folder=case/name
            print(f"[{index+1}/6] {variant}：启动、检查、预热、测量。",flush=True)
            with serve(paths[variant],variant,dtypes[variant],folder,deadline=deadline,
                       vllm_version=info["packages"]["vllm"]) as url:
                smoke(url,inputs["smoke"],folder/"smoke_before.json",deadline=deadline)
                warm=run_batch(url,SERVER_MODEL_NAME,renamed_requests(inputs["requests"],name+"-warm",count=8,output_tokens=32),
                               CONCURRENCY,folder/"warmup.jsonl",phase="warmup",deadline_monotonic=deadline)
                write_json(folder/"warmup_summary.json",warm)
                if warm["failure_count"]:
                    raise ExperimentError("预热失败")
                print("    正式计时：48条请求，完成后补位，并发8。",flush=True)
                sampler=MemorySampler(folder/"memory",interval=1.0,visible_bdf=bdf)
                sampler.start()
                try:
                    summary=run_batch(url,SERVER_MODEL_NAME,renamed_requests(inputs["requests"],name),CONCURRENCY,
                                      folder/"requests.jsonl",phase="measure",deadline_monotonic=deadline)
                finally:
                    memory_report=sampler.stop()
                write_json(folder/"summary.json",summary)
                if summary["failure_count"]:
                    raise ExperimentError("正式请求有失败；保留原始数据，不生成有效比较")
                smoke(url,inputs["smoke"],folder/"smoke_after.json",deadline=deadline)
            rounds.append({"round_id":name,"variant":variant,"dtype":dtypes[variant],"summary":summary,
                           "memory":memory_report,"server_memory":read_json(folder/"server_memory.json")})
            save_status(case,"running",finished_rounds=len(rounds))
            print("本轮返回包：",pack_case(case),flush=True)
        performance=compare_rounds(rounds)
        performance["execution_choice"]=choice
        memory_complete=all(memory_evidence_complete(r,bdf) for r in rounds)
        performance["memory_evidence_complete"]=memory_complete
        write_json(case/"performance.json",performance)
        save_status(case,"measured" if memory_complete else "measured_memory_incomplete",
                    performance_valid=True,quality_evaluated=True,memory_evidence_complete=memory_complete,
                    full_model_cpu_reference=False,learner_interpretation="pending",course_completion="not asserted")
        print("采集完成；请返回完整包并解释结果。" if memory_complete else
              "性能与质量已保存；显存映射／采样或启动日志证据不完整，请返回包，不先重跑全部测量。",flush=True)
        return 0 if memory_complete else 2
    except (Exception,KeyboardInterrupt) as exc:
        write_json(case/"failure_run.json",{"type":type(exc).__name__,"message":str(exc),"at":utc_now(),"completed_rounds":len(rounds)})
        save_status(case,"run_failed",completed_rounds=len(rounds),performance_file_exists=(case/"performance.json").exists())
        print("运行停止：",str(exc),file=sys.stderr)
        return 2
    finally:
        print("返回包：",pack_case(case),flush=True)


def main(argv=None):
    parser=argparse.ArgumentParser(description="W4-U3 GPU BF16/AWQ 部署对照；不安装依赖、不跑CPU模型")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("preflight",help="仅环境与2×2 GPU功能检查，不下载模型")
    prepare=sub.add_parser("prepare",help="下载／验证固定发布物并保存固定输入，无完整模型推理")
    prepare.add_argument("--bf16-dir")
    prepare.add_argument("--awq-dir")
    run=sub.add_parser("run",help="保存预测，再做GPU参考、质量及六轮计时")
    run.add_argument("--case")
    run.add_argument("--prediction-file",required=True)
    pack=sub.add_parser("pack",help="只打包已有结果")
    pack.add_argument("--case")
    args=parser.parse_args(argv)
    try:
        if args.command=="preflight":return preflight_command()
        if args.command=="prepare":return prepare_command(args)
        if args.command=="run":return run_command(args)
        print("返回包：",pack_case(prepared_case(args.case)))
        return 0
    except (ExperimentError,FileNotFoundError,ValueError,OSError) as exc:
        print("未执行：",str(exc),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
