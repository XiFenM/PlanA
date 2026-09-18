"""P1 验收工具。A1 源码表、A4 事前预测与解释由导师单独 Review。

正式运行前先在对话或 分析.md 提交预测。默认只验收 include_stop_str_in_output=False；
独立变式阶段可设 P1_INCLUDE_STOP=1，改变文本保留规则，其他条件不变。

从 PlanA 根目录：
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
    推理框架/实践/W1-P1/test_contract.py
"""

import importlib.util
import os
from pathlib import Path
import sys
from types import ModuleType

import pytest

from harness import make_case
from vllm.sampling_params import RequestOutputKind, SamplingParams
from vllm.v1.engine import EngineCoreOutput, FinishReason


def test_fixture_and_observer_baseline():
    """核验缓存、真实处理器与观察器；使用普通 LENGTH 结束，不执行目标 stop 场景。"""
    case = make_case()
    assert len(case.chunks) == 2
    assert case.stop_string not in case.tokenizer.decode(case.chunks[0])
    assert case.stop_string in case.tokenizer.decode(sum(case.chunks, []))
    params = SamplingParams(output_kind=RequestOutputKind.FINAL_ONLY, max_tokens=64)
    case.processor.add_request(case.make_request(params), case.prompt)
    assert case.processor.get_num_unfinished_requests() == 1
    ids = case.tokenizer.encode("Hello.", add_special_tokens=False)
    result = case.processor.process_outputs([EngineCoreOutput(
        request_id=case.request_id, new_token_ids=ids, finish_reason=FinishReason.LENGTH,
    )])
    assert len(result.request_outputs) == 1
    completion = result.request_outputs[0].outputs[0]
    assert completion.text == "Hello."
    assert completion.finish_reason == "length"
    assert result.reqs_to_abort == []
    assert case.processor.get_num_unfinished_requests() == 0
    assert case.processor.calls[0]["request_outputs"][0]["outputs"][0]["text"] == "Hello."
    assert case.processor.calls[0]["registered_internal_ids"] == []


@pytest.fixture(scope="module")
def executed_case():
    path = Path(__file__).with_name("scenario.py")
    if not path.exists():
        pytest.skip("学习者尚未提交 scenario.py；跳过不表示 A2/A3 通过")
    # 提供包上下文，支持学习者使用同目录的 .harness 相对导入。
    package_name = "plana_w1_p1"
    package = ModuleType(package_name)
    package.__path__ = [str(path.parent)]
    sys.modules[package_name] = package
    sys.modules[f"{package_name}.harness"] = sys.modules[make_case.__module__]
    spec = importlib.util.spec_from_file_location(f"{package_name}.scenario", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert callable(getattr(module, "run_case", None)), "请提供 run_case(case) 函数"
    case = make_case(include_stop_str_in_output=os.getenv("P1_INCLUDE_STOP") == "1")
    module.run_case(case)
    return case


def test_a2_real_request_and_two_core_outputs(executed_case):
    case = executed_case
    registrations = case.processor.registrations
    assert len(registrations) == 1, "只注册一个请求"
    request = registrations[0]
    assert request["request_id"] == case.request_id
    assert request["external_req_id"] == case.external_req_id
    assert request["output_kind"] == "FINAL_ONLY"
    assert request["stop"] == [case.stop_string]
    assert request["min_tokens"] == 0
    assert request["max_tokens"] > sum(map(len, case.chunks))
    assert request["include_stop_str_in_output"] == case.include_stop_str_in_output
    assert len(case.processor.calls) == 3, "两次正式输出，再提交一次迟到输出"
    for call, token_ids in zip(case.processor.calls, [*case.chunks, case.late_ids]):
        assert call["engine_core_outputs"] == [{
            "request_id": case.request_id, "new_token_ids": token_ids, "finished": False,
        }]


def test_a3_output_stop_abort_cleanup_and_late_output(executed_case):
    case = executed_case
    assert len(case.processor.calls) == 3
    before, stopped, late = case.processor.calls
    assert before["request_outputs"] == []
    assert before["reqs_to_abort"] == []
    assert before["unfinished"] == 1
    assert before["registered_internal_ids"] == [case.request_id]
    assert len(stopped["request_outputs"]) == 1
    output = stopped["request_outputs"][0]
    assert output["request_id"] == case.external_req_id
    assert output["finished"] is True
    assert len(output["outputs"]) == 1
    completion = output["outputs"][0]
    expected = case.generated_text.split(case.stop_string, 1)[0]
    if case.include_stop_str_in_output:
        expected += case.stop_string
    assert completion["text"] == expected
    assert completion["finish_reason"] == "stop"
    assert completion["stop_reason"] == case.stop_string
    assert stopped["reqs_to_abort"] == [case.request_id]
    assert stopped["unfinished"] == 0
    assert stopped["registered_internal_ids"] == []
    assert late["request_outputs"] == []
    assert late["reqs_to_abort"] == []
    assert late["unfinished"] == 0
    assert late["registered_internal_ids"] == []
