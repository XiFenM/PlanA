"""用本地 HF Transformers CPU FP32 参考校验 vLLM 的短生成结果。

本模块不下载权重；调用方负责 pinned snapshot 与文件哈希核验。
HTTP 成功、非空文本或 CPU 参考耗时均不是本模块的正确性/性能证据。
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
import tempfile
from typing import Any


MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MODEL_REVISION = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
EXPECTED_GENERATED_TOKENS = 8
MAX_LOGPROB_ABS_DIFF = 0.25
MAX_GREEDY_LOGPROB_GAP = 0.10
BOUNDARY_EPSILON = 1e-12


class CorrectnessError(RuntimeError):
    """校验未通过或报告未保存；保存失败时 report 保留原错误和 persistence_error。"""

    def __init__(self, message: str, report: dict[str, Any]):
        super().__init__(message)
        self.report = report


def _positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} 必须是正整数")
    return value


def _logprob(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} 必须是有限数值")
    result = float(value)
    if not math.isfinite(result) or result > 0:
        raise ValueError(f"{name} 必须是有限且不大于 0 的 log probability")
    return result


def prediction_positions(prompt_length: int, generated_length: int) -> list[int]:
    """第 j 个生成 token 由 prompt_length - 1 + j 位置的 hidden state 预测。"""
    _positive_int(prompt_length, "prompt_length")
    _positive_int(generated_length, "generated_length")
    return list(range(prompt_length - 1, prompt_length + generated_length - 1))


def validate_records(
    records: Any,
    vocab_size: int,
    *,
    expected_generated_tokens: int | None = None,
) -> list[dict[str, Any]]:
    """在模型执行前验证完整批次，返回副本，不修改 HTTP 原始记录。"""
    _positive_int(vocab_size, "vocab_size")
    if expected_generated_tokens is not None:
        _positive_int(expected_generated_tokens, "expected_generated_tokens")
    if not isinstance(records, list) or not records:
        raise ValueError("records 必须是非空列表")
    normalized = []
    request_ids: set[str] = set()
    for case_index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"records[{case_index}] 必须是对象")
        request_id = record.get("request_id")
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError(f"records[{case_index}].request_id 必须是非空字符串")
        if request_id in request_ids:
            raise ValueError(f"request_id 重复: {request_id}")
        request_ids.add(request_id)
        clean: dict[str, Any] = {"request_id": request_id}
        for field in ("prompt_token_ids", "token_ids"):
            values = record.get(field)
            if not isinstance(values, list) or not values:
                raise ValueError(f"{request_id}.{field} 必须是非空列表")
            for index, token_id in enumerate(values):
                if (
                    isinstance(token_id, bool)
                    or not isinstance(token_id, int)
                    or not 0 <= token_id < vocab_size
                ):
                    raise ValueError(
                        f"{request_id}.{field}[{index}] 必须是 [0, {vocab_size}) 内整数"
                    )
            clean[field] = list(values)
        token_logprobs = record.get("token_logprobs")
        if not isinstance(token_logprobs, list):
            raise ValueError(f"{request_id}.token_logprobs 必须是列表")
        if len(token_logprobs) != len(clean["token_ids"]):
            raise ValueError(f"{request_id} 的 token_ids 与 token_logprobs 长度不一致")
        if (
            expected_generated_tokens is not None
            and len(clean["token_ids"]) != expected_generated_tokens
        ):
            raise ValueError(f"{request_id} 必须恰好生成 {expected_generated_tokens} 个 token")
        clean["token_logprobs"] = [
            _logprob(value, f"{request_id}.token_logprobs[{index}]")
            for index, value in enumerate(token_logprobs)
        ]
        normalized.append(clean)
    return normalized


def _within_limit(value: float, limit: float) -> bool:
    # 只消除二进制浮点在十进制边界上的舍入误差，不放宽数值误差预算。
    return value <= limit or math.isclose(value, limit, rel_tol=0, abs_tol=BOUNDARY_EPSILON)


def score_reference_position(
    *,
    token_id: int,
    server_logprob: float,
    reference_logprob: float,
    reference_top1_id: int,
    reference_top1_logprob: float,
) -> dict[str, Any]:
    """分别检查概率一致性与贪心选择；不同 token 仅在近似平局时允许通过。"""
    for name, value in (("token_id", token_id), ("reference_top1_id", reference_top1_id)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} 必须是非负整数")
    server_logprob = _logprob(server_logprob, "server_logprob")
    reference_logprob = _logprob(reference_logprob, "reference_logprob")
    reference_top1_logprob = _logprob(reference_top1_logprob, "reference_top1_logprob")
    gap = reference_top1_logprob - reference_logprob
    if gap < 0:
        raise ValueError("reference_top1_logprob 不能小于候选 token 的参考 logprob")
    if token_id == reference_top1_id and gap != 0:
        raise ValueError("相同参考 token 的 logprob 必须相等")
    abs_diff = abs(server_logprob - reference_logprob)
    probability_passed = _within_limit(abs_diff, MAX_LOGPROB_ABS_DIFF)
    greedy_passed = _within_limit(gap, MAX_GREEDY_LOGPROB_GAP)
    return {
        "token_id": token_id,
        "server_logprob": server_logprob,
        "reference_logprob": reference_logprob,
        "reference_top1_id": reference_top1_id,
        "reference_top1_logprob": reference_top1_logprob,
        "logprob_abs_diff": abs_diff,
        "greedy_logprob_gap": gap,
        "exact_top1_match": token_id == reference_top1_id,
        "probability_passed": probability_passed,
        "greedy_passed": greedy_passed,
        "passed": probability_passed and greedy_passed,
    }


def _validate_cpu_reference_tensors(model: Any, torch: Any) -> dict[str, int]:
    """oneDNN 线性层把权重放入 buffers，因此不能只检查 parameters。"""
    counts = {"parameter_tensors": 0, "buffer_tensors": 0, "mkldnn_buffer_tensors": 0}
    for kind, tensors in (
        ("parameter", model.named_parameters()), ("buffer", model.named_buffers())
    ):
        for name, tensor in tensors:
            if (
                tensor.device.type != "cpu"
                or (tensor.is_floating_point() and tensor.dtype != torch.float32)
            ):
                raise ValueError(f"参考模型 {kind} {name} 必须位于 CPU，浮点张量必须为 FP32")
            counts[f"{kind}_tensors"] += 1
            if kind == "buffer" and getattr(tensor, "is_mkldnn", False):
                counts["mkldnn_buffer_tensors"] += 1
    return counts


def configure_cpu_reference_backend(model: Any, torch: Any) -> dict[str, Any]:
    """只将 nn.Linear 转为 oneDNN FP32，保留 Qwen2 eager attention 与其他层。

    缺少 oneDNN 或 IEEE FP32 控制时保留 dense 实现并记录原因；开始替换后若失败
    则向上抛错，避免将部分转换的模型描述为 dense。此函数不改变任何评分阈值。
    """
    _validate_cpu_reference_tensors(model, torch)
    linear_count = sum(isinstance(module, torch.nn.Linear) for module in model.modules())
    info: dict[str, Any] = {
        "backend": "torch_dense_cpu_fp32",
        "linear_count": linear_count,
        "converted_linear_count": 0,
        "mkldnn_matmul_fp32_precision": None,
        "backend_fallback_reason": None,
    }
    mkldnn = getattr(torch.backends, "mkldnn", None)
    if mkldnn is None or not mkldnn.is_available() or not mkldnn.enabled:
        info["backend_fallback_reason"] = "mkldnn_unavailable_or_disabled"
        info["tensor_validation"] = _validate_cpu_reference_tensors(model, torch)
        return info
    try:
        from torch.utils.mkldnn import MkldnnLinear
        # 不用 BF16/TF32 内部运算来加速 FP32 参考。先检查 API，避免创建无效属性。
        getattr(mkldnn.matmul, "fp32_precision")
        mkldnn.matmul.fp32_precision = "ieee"
        precision = mkldnn.matmul.fp32_precision
    except (ImportError, AttributeError, RuntimeError) as error:
        info["backend_fallback_reason"] = f"ieee_mkldnn_linear_unavailable: {type(error).__name__}"
        info["tensor_validation"] = _validate_cpu_reference_tensors(model, torch)
        return info
    if precision != "ieee":
        raise ValueError("oneDNN matmul 的 FP32 设置未保持 ieee，禁止运行参考")
    info["mkldnn_matmul_fp32_precision"] = precision
    if linear_count == 0:
        info["backend_fallback_reason"] = "no_linear_layers"
        info["tensor_validation"] = _validate_cpu_reference_tensors(model, torch)
        return info

    converted = 0

    def replace_children(parent: Any) -> None:
        nonlocal converted
        for name, child in list(parent.named_children()):
            if isinstance(child, torch.nn.Linear):
                setattr(parent, name, MkldnnLinear(child, dtype=torch.float32))
                converted += 1
            else:
                replace_children(child)

    with torch.inference_mode():
        replace_children(model)
    if converted != linear_count:
        raise ValueError("oneDNN 线性层替换数量不匹配")
    model.eval()
    info.update(backend="onednn_linear_cpu_fp32", converted_linear_count=converted)
    info["tensor_validation"] = _validate_cpu_reference_tensors(model, torch)
    return info


def _progress(enabled: bool, event: str, **fields: Any) -> None:
    if enabled:
        try:
            print("W4_REFERENCE " + json.dumps({"event": event, **fields}, ensure_ascii=False), flush=True)
        except OSError:
            pass  # 进度输出失效不能掩盖原错误或阻止保存正确性报告。


def _evaluate_case(model: Any, torch: Any, record: dict[str, Any]) -> dict[str, Any]:
    prompt = record["prompt_token_ids"]
    generated = record["token_ids"]
    positions = prediction_positions(len(prompt), len(generated))
    # Teacher forcing 使用服务器实际生成的前缀；最后一个待预测 token 不进入输入。
    input_ids = torch.tensor([prompt + generated[:-1]], dtype=torch.long, device="cpu")
    with torch.inference_mode():
        output = model.model(
            input_ids=input_ids,
            use_cache=False,
            output_hidden_states=False,
            return_dict=True,
        )
        # 仅对最后 G 个 hidden states 投影到词表，避免完整 prompt 的 [L, V] logits。
        hidden = output.last_hidden_state[:, positions[0] : positions[-1] + 1, :]
        if hidden.shape[1] != len(generated):
            raise ValueError("参考 hidden-state 位置数量不匹配")
        logits = model.lm_head(hidden).float()
        if logits.shape != (1, len(generated), model.config.vocab_size):
            raise ValueError("参考 logits 形状不匹配")
        if not torch.isfinite(logits).all().item():
            raise ValueError("参考 logits 含非有限值")
        logprobs = torch.log_softmax(logits, dim=-1)[0]
        top1_ids = logprobs.argmax(dim=-1)
        case_positions = []
        for index, token_id in enumerate(generated):
            top1_id = int(top1_ids[index].item())
            score = score_reference_position(
                token_id=token_id,
                server_logprob=record["token_logprobs"][index],
                reference_logprob=float(logprobs[index, token_id].item()),
                reference_top1_id=top1_id,
                reference_top1_logprob=float(logprobs[index, top1_id].item()),
            )
            case_positions.append(
                {"generated_index": index, "input_position": positions[index], **score}
            )
    return {
        "request_id": record["request_id"],
        "prompt_token_ids": list(prompt),
        "token_ids": list(generated),
        "prompt_tokens": len(prompt),
        "generated_tokens": len(generated),
        "passed": all(position["passed"] for position in case_positions),
        "positions": case_positions,
    }


def _summarize(cases: list[dict[str, Any]], expected_cases: int) -> dict[str, Any]:
    positions = [position for case in cases for position in case["positions"]]
    return {
        "expected_cases": expected_cases,
        "evaluated_cases": len(cases),
        "passed_cases": sum(case["passed"] for case in cases),
        "failed_cases": sum(not case["passed"] for case in cases),
        "evaluated_positions": len(positions),
        "failed_positions": sum(not position["passed"] for position in positions),
        "max_logprob_abs_diff": max(
            (position["logprob_abs_diff"] for position in positions), default=None
        ),
        "max_greedy_logprob_gap": max(
            (position["greedy_logprob_gap"] for position in positions), default=None
        ),
    }


def _write_report(output_path: str | Path, report: dict[str, Any]) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.",
            suffix=".tmp", delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
            json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        # 同目录的完整临时文件以 hard link 原子发布；目标存在时绝不替换。
        # 入口检查只提供早期报错，此操作仍防止检查之后的竞争写入。
        os.link(temporary_path, path)
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass  # 临时文件清理不能掩盖序列化、发布或原始校验错误。


def _persist_report(
    output_path: str | Path, report: dict[str, Any], *, progress: bool = False
) -> Exception | None:
    """保留持久化错误供调用方附加，避免覆盖原始校验失败原因。"""
    _progress(progress, "reference_report_saving", status=report["status"])
    try:
        _write_report(output_path, report)
    except Exception as error:
        report["persistence_error"] = {"type": type(error).__name__, "message": str(error)}
        _progress(progress, "reference_report_save_failed", error_type=type(error).__name__)
        return error
    _progress(progress, "reference_report_saved", status=report["status"])
    return None


def evaluate_records(
    model_path: str | Path,
    records: list[dict[str, Any]],
    output_path: str | Path,
    *,
    threads: int = 8,
    progress: bool = False,
) -> dict[str, Any]:
    """成功时返回已保存报告；未通过时尝试保存报告，再抛出 CorrectnessError。

    依赖延迟导入，纯数据/评分测试无需安装 torch 或 transformers。只允许本地
    Qwen2ForCausalLM；固定短输出与阈值不可通过调用参数放宽。CPU 运行不计时。
    已有 output_path（包括悬空符号链接）在入口抛出 FileExistsError，绝不覆盖。
    progress=True 时只输出阶段、样本序号与长度，不输出 prompt、生成内容或权重。
    """
    if os.path.lexists(output_path):
        raise FileExistsError(f"正确性报告已存在，拒绝覆盖: {output_path}")
    expected_cases = len(records) if isinstance(records, list) else 0
    report: dict[str, Any] = {
        "schema_version": 1,
        "status": "error",
        "passed": False,
        "expected_model_id": MODEL_ID,
        "expected_model_revision": MODEL_REVISION,
        "model_path": str(model_path),
        "weight_identity_scope": "调用方负责 pinned snapshot 与权重文件哈希核验",
        "reference": {
            "implementation": "HF Transformers Qwen2ForCausalLM",
            "device": "cpu",
            "dtype": "float32",
            "attention": "eager",
            "conditioning": "teacher forcing on actual server-generated prefix",
            "use_cache": False,
            "performance_measurement": False,
        },
        "thresholds": {
            "logprob_abs_diff_max_nats": MAX_LOGPROB_ABS_DIFF,
            "greedy_logprob_gap_max_nats": MAX_GREEDY_LOGPROB_GAP,
            "boundary_roundoff_epsilon": BOUNDARY_EPSILON,
            "all_positions_must_pass": True,
            "generated_tokens_per_case": EXPECTED_GENERATED_TOKENS,
        },
        "cases": [],
    }
    phase = "model_contract"
    try:
        if type(progress) is not bool:
            raise ValueError("progress 必须是 bool")
        _positive_int(threads, "threads")
        if threads > 8:
            raise ValueError("CPU 参考最多使用 8 个线程")
        local_path = Path(model_path).resolve()
        if not local_path.is_dir():
            raise ValueError("model_path 必须是已经下载并验证的本地模型目录")
        config = json.loads((local_path / "config.json").read_text(encoding="utf-8"))
        if (
            config.get("model_type") != "qwen2"
            or config.get("architectures") != ["Qwen2ForCausalLM"]
        ):
            raise ValueError("参考仅支持 Qwen2ForCausalLM / qwen2 架构")
        vocab_size = _positive_int(config.get("vocab_size"), "config.vocab_size")
        phase = "records"
        clean_records = validate_records(
            records, vocab_size, expected_generated_tokens=EXPECTED_GENERATED_TOKENS
        )
        phase = "reference_load"
        _progress(progress, "reference_load_started", device="cpu", dtype="float32")
        import torch
        import transformers
        from transformers import AutoModelForCausalLM

        torch.set_num_threads(threads)
        if torch.get_num_interop_threads() != 1:
            # 并行工作已开始时 PyTorch 会拒绝修改；此时失败，不静默突破资源上限。
            torch.set_num_interop_threads(1)
        report["reference"].update(
            threads=threads, interop_threads=torch.get_num_interop_threads(),
            torch_version=torch.__version__, transformers_version=transformers.__version__,
        )
        model = AutoModelForCausalLM.from_pretrained(
            str(local_path), local_files_only=True, trust_remote_code=False,
            torch_dtype=torch.float32, attn_implementation="eager",
        )
        model.eval()
        _progress(progress, "reference_load_completed")
        if (
            type(model).__name__ != "Qwen2ForCausalLM"
            or model.config.model_type != "qwen2"
            or model.config.vocab_size != vocab_size
            or model.config._attn_implementation != "eager"
            or not hasattr(model, "model")
            or not hasattr(model, "lm_head")
        ):
            raise ValueError("已加载参考模型与固定架构/配置不一致")
        phase = "reference_backend"
        backend = configure_cpu_reference_backend(model, torch)
        report["reference"].update(backend)
        _progress(progress, "reference_backend_configured", **backend)
        phase = "reference_evaluation"
        for index, record in enumerate(clean_records):
            _progress(
                progress, "reference_case_started", case_index=index, cases=len(clean_records),
                prompt_tokens=len(record["prompt_token_ids"]), generated_tokens=len(record["token_ids"]),
            )
            result = _evaluate_case(model, torch, record)
            report["cases"].append(result)
            _progress(progress, "reference_case_completed", case_index=index, passed=result["passed"])
        report["passed"] = all(case["passed"] for case in report["cases"])
        report["status"] = "passed" if report["passed"] else "failed"
    except Exception as error:
        report["error"] = {
            "phase": phase, "type": type(error).__name__, "message": str(error)
        }
        report["summary"] = _summarize(report["cases"], expected_cases)
        _progress(progress, "reference_failed", phase=phase, error_type=type(error).__name__)
        persistence_error = _persist_report(output_path, report, progress=progress)
        message = f"独立正确性校验无法完成 ({phase}): {error}"
        if persistence_error is not None:
            message += f"；报告保存也失败: {persistence_error}"
        raise CorrectnessError(message, report) from error
    report["summary"] = _summarize(report["cases"], expected_cases)
    persistence_error = _persist_report(output_path, report, progress=progress)
    if not report["passed"]:
        message = "独立正确性校验未通过；禁止继续 benchmark"
        if persistence_error is not None:
            message += f"；报告保存也失败: {persistence_error}"
        raise CorrectnessError(message, report) from persistence_error
    if persistence_error is not None:
        report.update(status="error", passed=False, reference_evaluation_passed=True)
        report["error"] = {"phase": "report_write", **report["persistence_error"]}
        raise CorrectnessError(
            f"参考结果通过，但报告保存失败；禁止继续 benchmark: {persistence_error}", report
        ) from persistence_error
    return report
