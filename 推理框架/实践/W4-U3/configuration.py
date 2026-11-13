"""只投影并核验 W4-U3 的实际服务配置，不保存 /server_info 原始响应。

已核 vLLM v0.26.0 / v0.33.0 的 /server_info?config_format=json 返回 vllm_config 对象；
默认 config_format=text 返回的是 str(config)，并非可解析的 JSON。
本模块也接受已经 JSON 编码的配置字符串，但拒绝默认文本表示。

固定版本依据：
https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/entrypoints/serve/dev/server_info/api_router.py
https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/v1/core/sched/scheduler.py#L109-L115
https://github.com/vllm-project/vllm/blob/4ba787ec9959e566d3b587a796dff07673324da5/vllm/entrypoints/serve/dev/server_info/api_router.py#L43-L59
"""

from __future__ import annotations

from collections.abc import Mapping
import json
import math


# 逐字段复制，避免 config 中的 hf_token、环境变量或嵌套凭据进入记录。
_FIELDS = {
    "model": (
        "model_config",
        ("model", "dtype", "quantization", "max_model_len", "seed", "enforce_eager", "logprobs_mode"),
    ),
    "parallel": (
        "parallel_config",
        ("tensor_parallel_size", "pipeline_parallel_size"),
    ),
    "cache": (
        "cache_config",
        ("enable_prefix_caching", "gpu_memory_utilization", "cache_dtype", "block_size",
         "num_gpu_blocks", "num_cpu_blocks", "kv_cache_memory_bytes"),
    ),
    "scheduler": (
        "scheduler_config",
        (
            "max_num_batched_tokens",
            "max_num_scheduled_tokens",
            "max_num_seqs",
            "async_scheduling",
            "enable_chunked_prefill",
        ),
    ),
    "profiler": (
        "profiler_config",
        (
            "profiler",
            "torch_profiler_dir",
            "torch_profiler_use_gzip",
            "torch_profiler_with_stack",
            "torch_profiler_record_shapes",
            "torch_profiler_with_memory",
            "ignore_frontend",
            "detailed_trace_annotation",
        ),
    ),
    "compilation": (
        "compilation_config",
        ("mode", "cudagraph_mode", "backend"),
    ),
}


def _safe_scalar(value, field: str):
    """不递归复制对象，也不在错误消息中插入服务器返回的值。"""
    if value is not None and type(value) not in (str, int, float, bool):
        raise ValueError(f"配置字段 {field} 必须是 JSON 标量")
    if type(value) is float and not math.isfinite(value):
        raise ValueError(f"配置字段 {field} 必须是有限数值")
    return value


def project_runtime_config(response) -> dict:
    """从管理响应投影白名单；不改变原响应，不保留未知字段。

    缺失字段保持缺失，交给 validate_runtime_config 判定，不以默认值补齐。
    profiler.profiler 仅表示配置的类型，不表示 profiler 当前正在采集。
    """
    if not isinstance(response, Mapping) or "vllm_config" not in response:
        raise ValueError("管理响应缺少 vllm_config")
    config = response["vllm_config"]
    if isinstance(config, str):
        try:
            config = json.loads(config)
        except (ValueError, TypeError):
            raise ValueError("vllm_config 不是有效 JSON；请使用 config_format=json") from None
    if not isinstance(config, Mapping):
        raise ValueError("vllm_config 必须是 JSON 对象")

    projected = {}
    for output_group, (source_group, fields) in _FIELDS.items():
        source = config.get(source_group, {})
        if not isinstance(source, Mapping):
            raise ValueError(f"配置分组 {source_group} 必须是 JSON 对象")
        projected[output_group] = {
            field: _safe_scalar(source[field], f"{output_group}.{field}")
            for field in fields
            if field in source
        }
    if "speculative_config" in config:
        projected["speculative_enabled"] = config["speculative_config"] is not None
    return projected


def validate_runtime_config(projected, budget, profile=False, *, variant="bf16", dtype="bfloat16") -> list[str]:
    """返回违反固定实验合同的字段；空列表表示通过。

    两个已核版本的 Scheduler 使用 max_num_scheduled_tokens；它为 None 时才继承
    max_num_batched_tokens。缺失该字段不等同于显式 None。
    模型路径的具体取值由调用方单独核对。
    """
    errors = []
    if type(budget) is not int or budget <= 0:
        return ["budget 必须是正整数"]
    if type(profile) is not bool:
        return ["profile 必须是布尔值"]
    if variant not in ("bf16", "awq") or dtype not in ("bfloat16", "float16"):
        return ["未约定的模型或 dtype"]
    if variant == "bf16" and dtype != "bfloat16":
        return ["BF16 基线不能改成 FP16"]
    if not isinstance(projected, Mapping):
        return ["投影配置必须是 JSON 对象"]

    missing = object()

    def read(group, field):
        source = projected.get(group)
        if not isinstance(source, Mapping) or field not in source:
            errors.append(f"缺少配置字段 {group}.{field}")
            return missing
        return source[field]

    def equal(group, field, expected):
        actual = read(group, field)
        if actual is missing:
            return
        if type(actual) is not type(expected) or actual != expected:
            errors.append(f"配置字段 {group}.{field} 不符合固定值 {expected!r}")

    model = read("model", "model")
    if model is not missing and (type(model) is not str or not model.strip()):
        errors.append("配置字段 model.model 必须是非空模型路径")
    observed_dtype = read("model", "dtype")
    if observed_dtype is not missing and (
        type(observed_dtype) is not str or observed_dtype not in (dtype, "torch." + dtype)
    ):
        errors.append("配置字段 model.dtype 与所选执行类型不符")
    quantization = read("model", "quantization")
    if quantization is not missing:
        if variant == "bf16" and quantization is not None:
            errors.append("BF16 基线不应启用量化")
        elif variant == "awq" and quantization not in ("awq", "auto_awq"):
            errors.append("AWQ 服务未确认普通 AutoAWQ 配置")
    equal("model", "max_model_len", 4096)
    equal("model", "seed", 20261112)
    equal("model", "enforce_eager", True)
    equal("model", "logprobs_mode", "raw_logprobs")
    equal("parallel", "tensor_parallel_size", 1)
    equal("parallel", "pipeline_parallel_size", 1)
    equal("cache", "enable_prefix_caching", False)
    equal("cache", "cache_dtype", "auto")
    equal("cache", "block_size", 16)
    equal("cache", "kv_cache_memory_bytes", None)
    memory = read("cache", "gpu_memory_utilization")
    if memory is not missing and (
        type(memory) not in (float, int)
        or not math.isfinite(memory)
        or not math.isclose(memory, 0.70, rel_tol=0.0, abs_tol=1e-12)
    ):
        errors.append("配置字段 cache.gpu_memory_utilization 必须是 0.70")
    equal("scheduler", "max_num_batched_tokens", budget)
    scheduled = read("scheduler", "max_num_scheduled_tokens")
    if scheduled is not missing and scheduled is not None and (
        type(scheduled) is not int or scheduled != budget
    ):
        errors.append("配置字段 scheduler.max_num_scheduled_tokens 必须为 None 或预算值")
    equal("scheduler", "max_num_seqs", 16)
    equal("scheduler", "async_scheduling", False)
    equal("scheduler", "enable_chunked_prefill", True)
    if "speculative_enabled" not in projected:
        errors.append("缺少配置字段 speculative_enabled")
    elif projected["speculative_enabled"] is not False:
        errors.append("配置字段 speculative_enabled 必须为 False")
    equal("profiler", "profiler", "torch" if profile else None)
    if profile:
        equal("profiler", "torch_profiler_record_shapes", True)
        equal("profiler", "torch_profiler_with_memory", True)
    return errors
