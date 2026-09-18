"""导师维护的 P1 辅助工具；不包含学习者的 run_case 实现。

从 PlanA 根目录运行：
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python 推理框架/实践/W1-P1/harness.py fixture
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python 推理框架/实践/W1-P1/harness.py config
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python 推理框架/实践/W1-P1/harness.py attention

scenario.py 的接口为 run_case(case: Case) -> None。
学习者负责构造 SamplingParams、注册请求并提交两次输出与一次迟到输出。
调用自动记录到 case.processor.calls；不要手填观察结果。
"""

import argparse
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

REPO = Path(__file__).resolve().parents[3]
ENVIRONMENT = REPO.parent / "plana-w1-env/environment.json"
SOURCE_REVISION = "568afb3a13806beb53bb2e6bd518269357b237c0"


@lru_cache(maxsize=1)
def environment():
    data = json.loads(ENVIRONMENT.read_text())
    assert data["source"]["revision"] == SOURCE_REVISION
    return data


@lru_cache(maxsize=1)
def load_tokenizer():
    from transformers import AutoTokenizer

    info = environment()["tokenizer"]
    path = Path(info["path"])
    for name, expected in info["files"].items():
        actual = hashlib.sha256((path / name).read_bytes()).hexdigest()
        assert actual == expected["sha256"], f"tokenizer 文件变化：{name}"
    return AutoTokenizer.from_pretrained(
        path, local_files_only=True, trust_remote_code=False
    )


from vllm.sampling_params import SamplingParams
from vllm.v1.engine import EngineCoreOutput, EngineCoreRequest
from vllm.v1.engine.output_processor import OutputProcessor


class ObservedOutputProcessor(OutputProcessor):
    """执行上游真实方法，只增加输入、返回值和状态的观察。"""

    def __init__(self, tokenizer):
        super().__init__(tokenizer, log_stats=False)
        self.registrations = []
        self.calls = []

    def add_request(self, request, prompt, *args, **kwargs):
        result = super().add_request(request, prompt, *args, **kwargs)
        params = request.sampling_params
        self.registrations.append({
            "request_id": request.request_id,
            "external_req_id": request.external_req_id,
            "output_kind": params.output_kind.name,
            "stop": list(params.stop),
            "min_tokens": params.min_tokens,
            "max_tokens": params.max_tokens,
            "include_stop_str_in_output": params.include_stop_str_in_output,
        })
        return result

    def process_outputs(self, outputs, *args, **kwargs):
        outputs = list(outputs)
        observed_input = [{
            "request_id": item.request_id,
            "new_token_ids": list(item.new_token_ids),
            "finished": item.finished,
        } for item in outputs]
        result = super().process_outputs(outputs, *args, **kwargs)
        self.calls.append({
            "engine_core_outputs": observed_input,
            "request_outputs": [{
                "request_id": item.request_id,
                "finished": item.finished,
                "outputs": [{
                    "text": completion.text,
                    "token_ids": list(completion.token_ids),
                    "finish_reason": completion.finish_reason,
                    "stop_reason": completion.stop_reason,
                } for completion in item.outputs],
            } for item in result.request_outputs],
            "reqs_to_abort": list(result.reqs_to_abort),
            "unfinished": self.get_num_unfinished_requests(),
            "registered_internal_ids": sorted(self.request_states),
        })
        return result


@dataclass
class Case:
    tokenizer: object
    processor: ObservedOutputProcessor
    prompt: str
    prompt_ids: list[int]
    generated_text: str
    stop_string: str
    chunks: tuple[list[int], list[int]]
    late_ids: list[int]
    include_stop_str_in_output: bool = False
    request_id: str = "p1-internal"
    external_req_id: str = "p1-public"

    def make_request(self, sampling_params: SamplingParams) -> EngineCoreRequest:
        """填充无关的请求字段；采样与输出参数由学习者提供。"""
        return EngineCoreRequest(
            request_id=self.request_id,
            external_req_id=self.external_req_id,
            prompt_token_ids=list(self.prompt_ids),
            mm_features=None,
            arrival_time=0.0,
            lora_request=None,
            cache_salt=None,
            data_parallel_rank=None,
            sampling_params=sampling_params,
            pooling_params=None,
        )

    def make_output(self, token_ids: list[int]) -> EngineCoreOutput:
        """构造 Core 尚未判停的一次输出；不自动提交给处理器。"""
        return EngineCoreOutput(
            request_id=self.request_id,
            new_token_ids=list(token_ids),
            finish_reason=None,
        )


def make_case(include_stop_str_in_output=False) -> Case:
    tokenizer = load_tokenizer()
    text, first_text, stop = "The river is quiet today.", "The river is", "is quiet"
    ids = tokenizer.encode(text, add_special_tokens=False)
    splits = [
        i for i in range(1, len(ids))
        if tokenizer.decode(ids[:i], skip_special_tokens=True) == first_text
    ]
    assert len(splits) == 1, "tokenizer 未提供预期的跨输出边界"
    split = splits[0]
    assert tokenizer.decode(ids, skip_special_tokens=True) == text
    assert text.index(stop) < len(first_text) < text.index(stop) + len(stop)
    prompt = "Write a sentence: "
    return Case(
        tokenizer=tokenizer,
        processor=ObservedOutputProcessor(tokenizer),
        prompt=prompt,
        prompt_ids=tokenizer.encode(prompt, add_special_tokens=False),
        generated_text=text,
        stop_string=stop,
        chunks=(ids[:split], ids[split:]),
        late_ids=tokenizer.encode(" later", add_special_tokens=False),
        include_stop_str_in_output=include_stop_str_in_output,
    )


def build_config():
    """只构造本练习配置；不会创建 Executor、Worker 或加载模型。"""
    from vllm.engine.arg_utils import EngineArgs

    local = environment()["tokenizer"]["path"]
    return EngineArgs(
        model=local, tokenizer=local,
        tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1,
        distributed_executor_backend="uni", enforce_eager=True,
        max_model_len=256, max_num_seqs=1,
    ).create_engine_config()


def inspect_config():
    from vllm.platforms import current_platform

    config = build_config()
    return {
        "scope": "配置构造实测；Worker、Runner 和 Attention kernel 均未执行",
        "executor_backend": config.parallel_config.distributed_executor_backend,
        "worker_cls": config.parallel_config.worker_cls,
        "use_v2_model_runner": config.use_v2_model_runner,
        "dtype": str(config.model_config.dtype),
        "head_size": config.model_config.get_head_size(),
        "num_attention_heads": config.model_config.hf_config.num_attention_heads,
        "kv_cache_dtype": config.cache_config.cache_dtype,
        "block_size": config.cache_config.block_size,
        "user_specified_block_size": config.cache_config.user_specified_block_size,
        "configured_attention_backend": str(config.attention_config.backend),
        "device_capability": str(current_platform.get_device_capability()),
    }


def inspect_attention():
    """实测本题的 CUDA 平台选择器；不构造 Attention 层或执行 kernel。"""
    import vllm.envs as envs
    from vllm.config import set_current_vllm_config
    from vllm.platforms import current_platform
    from vllm.v1.attention.selector import AttentionSelectorConfig

    config = build_config()
    model = config.model_config
    cache = config.cache_config
    assert model.hf_config.model_type == "qwen3"
    assert not model.hf_config.use_sliding_window
    assert config.attention_config.backend is None
    assert not config.attention_config.backend_per_kind
    assert config.kv_transfer_config is None
    selector = AttentionSelectorConfig(
        head_size=model.get_head_size(),
        dtype=model.dtype,
        kv_cache_dtype=cache.cache_dtype,
        block_size=cache.block_size if cache.user_specified_block_size else None,
        use_mla=model.use_mla,
        use_non_causal=config.attention_config.use_non_causal,
        use_batch_invariant=envs.VLLM_BATCH_INVARIANT,
        use_pcp=config.parallel_config.prefill_context_parallel_size > 1,
    )
    heads = model.get_num_attention_heads(config.parallel_config)
    capability = current_platform.get_device_capability()
    with set_current_vllm_config(config):
        valid, invalid = current_platform.get_valid_backends(
            capability, selector, num_heads=heads
        )
        selected_class = current_platform.get_attn_backend_cls(
            None, selector, num_heads=heads
        )
    inputs = selector._asdict()
    inputs["dtype"] = str(inputs["dtype"])
    return {
        "scope": "CUDA 平台候选校验与自动选择实测；未实例化 Worker/Runner，未执行 Attention kernel",
        "selector_inputs": inputs,
        "num_heads": heads,
        "device_capability": list(capability),
        "valid_candidates": [{
            "name": candidate.backend.name,
            "priority": candidate.priority,
        } for candidate in valid],
        "invalid_candidates": {
            backend.name: {"priority": priority, "reasons": reasons}
            for backend, (priority, reasons) in invalid.items()
        },
        "selected_class": selected_class,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["fixture", "config", "attention"])
    args = parser.parse_args()
    if args.action == "config":
        output = inspect_config()
    elif args.action == "attention":
        output = inspect_attention()
    else:
        case = make_case()
        output = {
            "scope": "仅检查输入文本与 token 划分，不运行目标输出场景",
            "prompt": case.prompt,
            "generated_text": case.generated_text,
            "stop_string": case.stop_string,
            "chunks": case.chunks,
            "chunk_texts": [case.tokenizer.decode(ids) for ids in case.chunks],
            "late_ids": case.late_ids,
        }
    print(json.dumps(output, ensure_ascii=False, indent=2))
