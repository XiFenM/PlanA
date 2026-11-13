"""无 HIP context 的设备显存采样，以及 vLLM 启动日志的独立口径提取。

设备采样包含同卡其他进程，采样最大值可能遗漏瞬时峰值。启动日志里的
模型加载占用、KV 可用预算和 token 容量各有不同含义，不与采样值相加。
本模块只使用标准库；不会导入 torch、启动模型或初始化 GPU runtime。
"""

from __future__ import annotations

import datetime as dt
import json
import math
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path


SCHEMA_VERSION = 1
_COMMAND_TIMEOUT = 2.0
_ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_BDF = re.compile(r"(?:(?P<domain>[0-9a-fA-F]{4,8}):)?(?P<bus>[0-9a-fA-F]{2}):(?P<slot>[0-9a-fA-F]{2})\.(?P<fn>[0-7])")


def normalize_bdf(value):
    """规范化 HIP、sysfs 和 rocm-smi 的 PCI 地址；未知格式返回 None。"""
    match = _BDF.fullmatch(str(value).strip()) if value is not None else None
    if match is None:
        return None
    return (f"{int(match['domain'] or '0', 16):04x}:"
            f"{match['bus'].lower()}:{match['slot'].lower()}.{match['fn']}")


def _utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _bytes(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a byte count")
    if isinstance(value, int):
        result = value
    elif isinstance(value, str) and re.fullmatch(r"(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)", value.strip()):
        result = int(value.strip().replace(",", ""))
    else:
        raise ValueError("expected an integer byte count")
    if result < 0:
        raise ValueError("negative byte count")
    return result


def _validated_counter(device_id, pci_bdf, total, used):
    result = {"device_id": device_id, "pci_bdf": pci_bdf,
              "total_bytes": None, "used_bytes": None, "error": None}
    try:
        total, used = _bytes(total), _bytes(used)
        if total == 0 or used > total:
            raise ValueError("invalid VRAM counters: need 0 <= used <= total and total > 0")
        result.update(total_bytes=total, used_bytes=used)
    except (TypeError, ValueError) as exc:
        result["error"] = str(exc)
    return result


def discover_sysfs_devices(sysfs_root="/sys/class/drm"):
    """列出有 AMD vendor 标识的 card 节点，按物理 device 去重。"""
    devices, seen = [], set()
    for card in sorted(Path(sysfs_root).glob("card*")):
        if not re.fullmatch(r"card[0-9]+", card.name):
            continue
        device = card / "device"
        try:
            if int((device / "vendor").read_text().strip(), 16) != 0x1002:
                continue
            resolved = device.resolve(strict=True)
        except (OSError, ValueError):
            continue
        if str(resolved) in seen:
            continue
        seen.add(str(resolved))
        bdf = normalize_bdf(resolved.name)
        if bdf is None:
            try:
                for line in (device / "uevent").read_text().splitlines():
                    if line.startswith("PCI_SLOT_NAME="):
                        bdf = normalize_bdf(line.partition("=")[2])
            except OSError:
                pass
        devices.append({"device_id": card.name, "pci_bdf": bdf,
                        "device_path": str(resolved),
                        "has_vram_counters": all((device / name).is_file() for name in
                            ("mem_info_vram_total", "mem_info_vram_used"))})
    return devices


def _scope(devices, requested_bdf):
    if requested_bdf is not None:
        return "matched_pci_bdf"
    return "single_device_unmapped" if len(devices) == 1 else "all_devices_unmapped"


class _SysfsBackend:
    name = "amdgpu_sysfs"

    def __init__(self, devices, requested_bdf):
        self.devices = devices
        self.requested_bdf = requested_bdf

    def sample(self):
        results = []
        for device in self.devices:
            path = Path(device["device_path"])
            try:
                total = (path / "mem_info_vram_total").read_text().strip()
                used = (path / "mem_info_vram_used").read_text().strip()
                value = _validated_counter(device["device_id"], device["pci_bdf"], total, used)
            except OSError as exc:
                value = {"device_id": device["device_id"], "pci_bdf": device["pci_bdf"],
                         "total_bytes": None, "used_bytes": None,
                         "error": f"{type(exc).__name__}: {str(exc)[:240]}"}
            results.append(value)
        return {"devices": results, "scope": _scope(results, self.requested_bdf), "error": None}


def parse_rocm_smi_json(text, visible_bdf=None):
    """只接受 rocm-smi 明确标注 (B) 的 VRAM 字段，不猜测 MB/MiB 单位。"""
    requested_bdf = normalize_bdf(visible_bdf)
    if visible_bdf is not None and requested_bdf is None:
        raise ValueError("invalid visible_bdf")
    try:
        # 某些镜像会在 JSON 前打印只读查询的告警；不把告警当成指标。
        start = text.find("{")
        data = json.loads(text[start:]) if start >= 0 else None
        if not isinstance(data, dict):
            raise ValueError("rocm-smi did not return a JSON object")
    except (TypeError, ValueError) as exc:
        return {"devices": [], "scope": "unavailable", "error": f"invalid rocm-smi JSON: {exc}"}
    results = []
    for name, fields in sorted(data.items()):
        if not re.fullmatch(r"card[0-9]+", name) or not isinstance(fields, dict):
            continue
        bdf = normalize_bdf(fields.get("PCI Bus") or fields.get("PCI Bus ID"))
        if requested_bdf is not None and bdf != requested_bdf:
            continue
        value = _validated_counter(name, bdf, fields.get("VRAM Total Memory (B)"),
                                   fields.get("VRAM Total Used Memory (B)"))
        results.append(value)
    if not results:
        reason = "requested PCI BDF not found" if requested_bdf else "no recognized per-card VRAM byte fields"
        return {"devices": [], "scope": "unavailable", "error": reason}
    if requested_bdf is not None and len(results) > 1:
        return {"devices": results, "scope": "ambiguous_pci_bdf",
                "error": "multiple cards report the requested PCI BDF; not a unique runtime mapping"}
    return {"devices": results, "scope": _scope(results, requested_bdf), "error": None}


class _RocmSmiBackend:
    name = "rocm_smi_json"

    def __init__(self, binary, requested_bdf):
        self.binary = binary
        self.requested_bdf = requested_bdf

    def sample(self):
        command = [self.binary, "--showmeminfo", "vram", "--showbus", "--json"]
        try:
            result = subprocess.run(command, capture_output=True, text=True,
                                    timeout=_COMMAND_TIMEOUT, check=False)
            if result.returncode != 0:
                return {"devices": [], "scope": "unavailable",
                        "error": f"rocm-smi exit {result.returncode}: {result.stderr.strip()[:240]}"}
            return parse_rocm_smi_json(result.stdout, self.requested_bdf)
        except (OSError, subprocess.SubprocessError) as exc:
            return {"devices": [], "scope": "unavailable",
                    "error": f"rocm-smi query failed: {type(exc).__name__}: {str(exc)[:240]}"}


class _UnavailableBackend:
    name = "unavailable"

    def __init__(self, reason):
        self.reason = reason

    def sample(self):
        return {"devices": [], "scope": "unavailable", "error": self.reason}


def _select_backend(sysfs_root, requested_bdf):
    devices = discover_sysfs_devices(sysfs_root)
    selected = [d for d in devices if d["pci_bdf"] == requested_bdf] if requested_bdf else devices
    if selected and any(d["has_vram_counters"] for d in selected):
        return _SysfsBackend(selected, requested_bdf)
    binary = shutil.which("rocm-smi")
    if binary:
        return _RocmSmiBackend(binary, requested_bdf)
    reason = ("requested PCI BDF not exposed with AMD VRAM counters" if requested_bdf else
              "AMD sysfs VRAM counters not available")
    return _UnavailableBackend(reason + "; rocm-smi is not installed; no GPU runtime fallback")


class MemorySampler:
    """对一个明确时间窗口采样；同一 folder 的已有结果从不覆盖。

    start() 返回 self，stop() 幂等并返回 summary。context manager 的退出调用
    stop()，不吞掉主体异常。visible_bdf 应来自独立预检的逻辑设备映射；未提供时
    仅按物理设备逐个报告，不声称这些读数属于 vLLM 所用 GPU。
    """

    def __init__(self, folder, interval=1.0, *, visible_bdf=None, sysfs_root="/sys/class/drm"):
        if isinstance(interval, bool) or not isinstance(interval, (int, float)) or not math.isfinite(interval) or interval <= 0:
            raise ValueError("interval must be a finite positive number")
        self.folder = Path(folder)
        self.interval = float(interval)
        self.requested_bdf = normalize_bdf(visible_bdf)
        if visible_bdf is not None and self.requested_bdf is None:
            raise ValueError("invalid visible_bdf")
        self.sysfs_root = sysfs_root
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._thread = None
        self._summary = None
        self._rows = []
        self._worker_error = None

    def start(self):
        if self._thread is not None:
            raise RuntimeError("MemorySampler can only be started once")
        self.folder.mkdir(parents=True, exist_ok=True)
        self._sample_path = self.folder / "memory_samples.jsonl"
        self._summary_path = self.folder / "memory_summary.json"
        if self._sample_path.exists() or self._summary_path.exists():
            raise FileExistsError("memory sampling artifacts already exist")
        self._sample_path.touch(exist_ok=False)
        self._backend = _select_backend(self.sysfs_root, self.requested_bdf)
        self._started = time.monotonic()
        self._started_at = _utc_now()
        self._thread = threading.Thread(target=self._run, name="w4-u3-memory", daemon=True)
        self._thread.start()
        return self

    def _run(self):
        sequence, due = 0, self._started
        try:
            while not self._stop.is_set():
                begin = time.monotonic()
                row = self._backend.sample()
                end = time.monotonic()
                row.update(sequence=sequence, observed_at=_utc_now(),
                           elapsed_seconds=end - self._started,
                           query_duration_seconds=end - begin, backend=self._backend.name)
                # 超时 stop 返回之后，不再写入迟到的查询结果。
                with self._lock:
                    if self._stop.is_set():
                        break
                    with self._sample_path.open("a", encoding="utf-8") as stream:
                        stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                    self._rows.append(row)
                sequence += 1
                due = max(due + self.interval, end)
                self._stop.wait(max(0.0, due - time.monotonic()))
        except Exception as exc:
            with self._lock:
                self._worker_error = f"{type(exc).__name__}: {str(exc)[:300]}"

    def stop(self):
        if self._thread is None:
            raise RuntimeError("MemorySampler has not started")
        if self._summary is not None:
            return self._summary
        self._stop.set()
        self._thread.join(timeout=_COMMAND_TIMEOUT + 1.0)
        stopped = not self._thread.is_alive()
        with self._lock:
            rows, worker_error = list(self._rows), self._worker_error
        devices, errors, scopes = {}, [], set()
        for row in rows:
            if row["error"]:
                errors.append({"sequence": row["sequence"], "error": row["error"]})
            if row["devices"]:
                scopes.add(row["scope"])
            for device in row["devices"]:
                # 同一 BDF 也可能暴露多个设备/分区，绝不隐式合并这些读数。
                key = (device["pci_bdf"], device["device_id"])
                item = devices.setdefault(key, {"device_id": device["device_id"],
                    "pci_bdf": device["pci_bdf"], "valid_samples": 0, "failed_samples": 0,
                    "first_used_bytes": None, "last_used_bytes": None, "min_used_bytes": None,
                    "sampled_max_used_bytes": None, "total_bytes_values": []})
                if device["error"]:
                    item["failed_samples"] += 1
                    errors.append({"sequence": row["sequence"], "device_id": device["device_id"],
                                   "error": device["error"]})
                    continue
                used = device["used_bytes"]
                if item["valid_samples"] == 0:
                    item.update(first_used_bytes=used, min_used_bytes=used, sampled_max_used_bytes=used)
                item["valid_samples"] += 1
                item["last_used_bytes"] = used
                item["min_used_bytes"] = min(item["min_used_bytes"], used)
                item["sampled_max_used_bytes"] = max(item["sampled_max_used_bytes"], used)
                if device["total_bytes"] not in item["total_bytes_values"]:
                    item["total_bytes_values"].append(device["total_bytes"])
        valid = sum(d["valid_samples"] for d in devices.values())
        status = "ok" if valid else "unavailable"
        if valid and (errors or worker_error):
            status = "partial"
        if not stopped:
            status = "stop_timeout"
        scope = next(iter(scopes)) if len(scopes) == 1 else "mixed_or_unavailable"
        gaps = [b["elapsed_seconds"] - a["elapsed_seconds"] for a, b in zip(rows, rows[1:])]
        summary = {"schema_version": SCHEMA_VERSION, "status": status,
            "backend": self._backend.name, "scope": scope,
            "runtime_device_mapping_confirmed": scope == "matched_pci_bdf" and bool(valid),
            "requested_pci_bdf": self.requested_bdf, "started_at": self._started_at,
            "stopped_at": _utc_now(), "duration_seconds": time.monotonic() - self._started,
            "requested_interval_seconds": self.interval, "max_observed_sample_gap_seconds": max(gaps) if gaps else None,
            "sample_count": len(rows), "thread_stopped": stopped,
            "devices": list(devices.values()), "errors": errors,
            "worker_error": worker_error,
            "notes": ["设备 VRAM 读数包括同卡其他进程，不是服务进程独占内存。",
                      "sampled_max_used_bytes 是采样最大值，可能遗漏瞬时峰值；不等于 allocator 峰值。",
                      "未证明 runtime PCI 映射时按设备分别报告，不求和或冒充目标 GPU。",
                      "初始化权重占用、KV 预算及池容量由独立启动日志解释，不与此处读数混算。"]}
        with self._summary_path.open("x", encoding="utf-8") as stream:
            json.dump(summary, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
        self._summary = summary
        return summary

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.stop()
        except Exception:
            if exc_type is None:
                raise
        return False


def parse_server_memory(log_text):
    """提取日志实际声明的量；不从总预算反推实际使用量或 KV 块数。"""
    patterns = {
        "model_loading_gib": re.compile(r"Model loading took ([0-9]+(?:\.[0-9]+)?) GiB(?: memory)? and"),
        "kv_available_gib": re.compile(r"Available KV cache memory: ([0-9]+(?:\.[0-9]+)?) GiB"),
        "kv_capacity_tokens": re.compile(r"GPU KV cache size: ([0-9][0-9,]*) tokens"),
    }
    reports, values, invalid = [], {key: [] for key in patterns}, []
    for line_number, raw_line in enumerate(log_text.splitlines(), 1):
        line = _ANSI.sub("", raw_line)
        for key, pattern in patterns.items():
            match = pattern.search(line)
            if match is None:
                continue
            literal = match.group(1)
            try:
                value = _bytes(literal) if key.endswith("tokens") else float(literal)
                if not math.isfinite(value):
                    raise ValueError("non-finite value")
            except (TypeError, ValueError, OverflowError):
                invalid.append(f"{key}: invalid numeric log value on line {line_number}")
                continue
            values[key].append(value)
            reports.append({"kind": key, "value": value, "literal": literal,
                            "line_number": line_number, "log_line": line[:600]})
    result = {"schema_version": SCHEMA_VERSION, "source": "vllm_server_log", "reports": reports,
              "warnings": invalid, "notes": [
                  "model_loading_gib 是加载器报告的内存变化，不是逐张量精确字节数。",
                  "kv_available_gib 是启动时 KV 可用预算，不保证等于实际分配字节数。",
                  "kv_capacity_tokens 是池的容量，不是当前活跃请求使用量或实测并发能力。",
                  "GiB 数字经过日志格式化；保留原文精度，不伪造精确字节数。"]}
    for key, observed in values.items():
        distinct = set(observed)
        result[key] = next(iter(distinct)) if len(distinct) == 1 else None
        if not distinct:
            result["warnings"].append(f"{key}: no matching log entry")
        elif len(distinct) > 1:
            result["warnings"].append(f"{key}: conflicting log entries; no single value selected")
    return result
