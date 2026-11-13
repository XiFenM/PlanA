#!/usr/bin/env python3
"""W4-U3 小型、固定标签任务质量检查；不加载 CPU 模型。

标准答案来自构造记录，不来自 BF16 输出。准确率只覆盖本文件的 32 道合成任务；
不作生产质量、统计显著性或量化 kernel 正确性结论。
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import time
from typing import Any


SCHEMA_VERSION = 1
DATASET_ID = "w4-u3-quality-v1"
SEED = 20261113
MAX_TOKENS = 32
SCORING_RULE = "exact match after str.strip(); no other normalization; length-truncated answers are incorrect"
GENERATION = {
    "temperature": 0.0, "max_tokens": MAX_TOKENS, "ignore_eos": False,
    "skip_special_tokens": True, "spaces_between_special_tokens": False,
}
SYSTEM_MESSAGE = (
    "你只根据用户提供的记录作答。只输出所问字段或事实的原值，"
    "不添加解释、标点、引号或标签。"
)


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _expected(source: dict[str, Any]) -> str:
    records = source["records"]
    selected = [record for record in records if record["编号"] == source["target_id"]]
    if len(selected) != 1:
        raise ValueError("标准答案源必须唯一定位一条记录")
    answer = selected[0][source["target_field"]]
    if not isinstance(answer, str) or not answer or answer != answer.strip():
        raise ValueError("构造标签必须是无首尾空白的非空字符串")
    return answer


def _item_identity(item: dict[str, Any]) -> dict[str, Any]:
    return {key: item[key] for key in (
        "request_id", "category", "label_source", "expected_answer", "messages",
        "prompt_token_ids", "prompt_sha256", "max_tokens",
    )}


def _dataset_hash(items: list[dict[str, Any]]) -> str:
    return _digest({"dataset_id": DATASET_ID, "seed": SEED,
                    "generation": GENERATION, "scoring_rule": SCORING_RULE, "items": items})


def build_quality_inputs(tokenizer: Any) -> dict[str, Any]:
    """准备阶段调用一次；返回可直接保存的输入、规则标签与内容哈希。"""
    rng = random.Random(SEED)
    items = []
    for category in ("field_extraction", "fact_lookup"):
        for index in range(16):
            if category == "field_extraction":
                records = [
                    {"编号": f"ORD-{index + 1:02d}-{j + 1}",
                     "目的仓": f"HUB-{rng.randrange(100, 1000)}",
                     "货物编号": f"ITEM-{rng.randrange(1000, 10000)}",
                     "负责人": rng.choice(("陈安", "林澄", "周禾", "沈宁", "许岚")),
                     "状态": rng.choice(("待出库", "运输中", "已签收", "待复核"))}
                    for j in range(4)
                ]
                target = records[rng.randrange(4)]
                field = ("目的仓", "货物编号", "负责人", "状态")[index % 4]
                question = (
                    "以下是四条独立订单记录：\n"
                    + json.dumps(records, ensure_ascii=False, indent=2)
                    + f"\n问题：编号为 {target['编号']} 的订单，其“{field}”字段的值是什么？"
                    + "只输出该字段的原值。"
                )
                prefix = "field"
            else:
                records = [
                    {"编号": f"项目{index + 1:02d}-{j + 1}",
                     "会议室": f"R{rng.randrange(100, 1000)}",
                     "材料柜": f"C{rng.randrange(100, 1000)}",
                     "联络码": f"K{rng.randrange(1000, 10000)}",
                     "开始时间": f"{rng.randrange(8, 18):02d}:{rng.choice((0, 15, 30, 45)):02d}"}
                    for j in range(4)
                ]
                target = records[rng.randrange(4)]
                field = ("会议室", "材料柜", "联络码", "开始时间")[index % 4]
                facts = [
                    f"{record['编号']}安排在{record['会议室']}举行，材料放在{record['材料柜']}，"
                    f"联络码是{record['联络码']}，开始时间为{record['开始时间']}。"
                    for record in records
                ]
                question = (
                    "请只依据下面的当日安排查找事实。各项目相互独立：\n"
                    + "\n".join(facts)
                    + f"\n问题：{target['编号']}的{field}是什么？只输出记录中的原值。"
                )
                prefix = "fact"
            source = {"records": records, "target_id": target["编号"], "target_field": field}
            messages = [{"role": "system", "content": SYSTEM_MESSAGE},
                        {"role": "user", "content": question}]
            ids = tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True, return_dict=False,
            )
            if not isinstance(ids, list) or not ids or any(type(x) is not int or x < 0 for x in ids):
                raise ValueError("apply_chat_template 必须返回非空、非负整数 token ID 列表")
            item = {
                "request_id": f"quality-{prefix}-{index + 1:02d}", "category": category,
                "label_source": source, "expected_answer": _expected(source),
                "messages": messages, "prompt_token_ids": list(ids),
                "prompt_sha256": _digest(ids), "max_tokens": MAX_TOKENS,
            }
            item["item_sha256"] = _digest(_item_identity(item))
            items.append(item)
    return {
        "schema_version": SCHEMA_VERSION, "dataset_id": DATASET_ID, "seed": SEED,
        "scoring_rule": SCORING_RULE, "generation": dict(GENERATION),
        "label_origin": "deterministic synthetic records; independent of model outputs",
        "scope": "32 synthetic extraction/lookup tasks; not a general or production quality estimate",
        "items": items, "input_sha256": _dataset_hash(items),
    }


def _validated_items(value: Any) -> list[dict[str, Any]]:
    bundle = value if isinstance(value, dict) else None
    items = bundle.get("items") if bundle is not None else value
    if not isinstance(items, list) or len(items) != 32:
        raise ValueError("任务集必须恰好包含 32 条任务")
    ids = []
    categories = Counter()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("任务必须是对象")
        try:
            request_id = item["request_id"]
            if not isinstance(request_id, str) or not request_id:
                raise ValueError("request_id 必须是非空字符串")
            ids.append(request_id)
            categories[item["category"]] += 1
            tokens = item["prompt_token_ids"]
            if not isinstance(tokens, list) or not tokens or any(type(x) is not int or x < 0 for x in tokens):
                raise ValueError("任务 token IDs 无效")
            if item["expected_answer"] != _expected(item["label_source"]):
                raise ValueError("标准答案与构造记录不符")
            if type(item["max_tokens"]) is not int or item["max_tokens"] != MAX_TOKENS:
                raise ValueError("任务输出上限必须为 32 token")
            if item["prompt_sha256"] != _digest(tokens) or item["item_sha256"] != _digest(_item_identity(item)):
                raise ValueError("任务输入或标签的哈希不符")
        except (KeyError, TypeError) as error:
            raise ValueError("任务字段不完整或类型错误") from error
    if len(set(ids)) != 32 or categories != Counter(field_extraction=16, fact_lookup=16):
        raise ValueError("任务 ID 必须唯一，两个类别必须各 16 条")
    if bundle is not None:
        if (bundle.get("dataset_id") != DATASET_ID or bundle.get("seed") != SEED
                or bundle.get("generation") != GENERATION or bundle.get("scoring_rule") != SCORING_RULE
                or bundle.get("input_sha256") != _dataset_hash(items)):
            raise ValueError("任务集元数据或总哈希不符")
    return items


def exact_match(raw_text: str, expected_answer: str) -> bool:
    """仅删除输出首尾空白；保留大小写、内部空白、引号、标点及解释文字。"""
    if not isinstance(raw_text, str) or not isinstance(expected_answer, str):
        raise ValueError("输出与标签都必须是字符串")
    return raw_text.strip() == expected_answer


def _write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def evaluate_quality(base_url: str, model: str, items: Any, folder: str | Path,
                     deadline: float) -> dict[str, Any]:
    """顺序发送 32 个非流式请求；deadline 为 time.monotonic() 的绝对期限。

    返回 quality_report.json 的内容。请求失败仍保留对应原始记录和题目；准确率
    分母固定为 32，但报告标记 incomplete，不能据失败请求得出质量退化结论。
    """
    from client import request_once

    selected = _validated_items(items)
    if not isinstance(model, str) or not model:
        raise ValueError("model 必须是非空字符串")
    if type(deadline) not in (int, float) or not math.isfinite(deadline):
        raise ValueError("deadline 必须是有限 monotonic 时刻")
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    input_hash = _dataset_hash(selected)
    _write_json(folder / "quality_inputs.json", {
        "schema_version": SCHEMA_VERSION, "dataset_id": DATASET_ID, "seed": SEED,
        "generation": dict(GENERATION), "scoring_rule": SCORING_RULE,
        "input_sha256": input_hash, "items": selected,
    })
    scored = []
    with (folder / "quality_raw.jsonl").open("x", encoding="utf-8") as raw_file:
        for item in selected:
            request = {
                "request_id": item["request_id"], "prompt_token_ids": item["prompt_token_ids"],
                "max_tokens": MAX_TOKENS, "ignore_eos": False,
                "skip_special_tokens": True, "spaces_between_special_tokens": False,
            }
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                record = {"request_id": item["request_id"], "success": False, "text": "",
                          "error": "quality deadline exceeded before request", "request_sent": False}
            else:
                try:
                    record = request_once(base_url, model, request, timeout=min(90.0, remaining), stream=False)
                except Exception as error:
                    record = {"request_id": item["request_id"], "success": False, "text": "",
                              "error": f"{type(error).__name__}: {error}"}
            if not isinstance(record, dict):
                record = {"request_id": item["request_id"], "success": False, "text": "",
                          "error": "client returned a non-object record"}
            # 原始 record 不改写；关联/格式错误另记在本层评分中。
            raw_file.write(json.dumps({"expected_request_id": item["request_id"], "record": record},
                                      ensure_ascii=False, allow_nan=False) + "\n")
            raw_file.flush()
            text = record.get("text")
            aligned = record.get("request_id") == item["request_id"]
            success = record.get("success") is True and isinstance(text, str) and aligned
            error = record.get("error")
            if not aligned:
                error = "response request_id does not match the submitted task"
            elif not isinstance(text, str):
                error = "response text is not a string"
            scored.append({
                "request_id": item["request_id"], "category": item["category"],
                "expected_answer": item["expected_answer"], "prompt_sha256": item["prompt_sha256"],
                "item_sha256": item["item_sha256"], "raw_output": text,
                "normalized_output": text.strip() if isinstance(text, str) else None,
                "transport_success": success,
                "correct": success and record.get("finish_reason") != "length" and exact_match(text, item["expected_answer"]),
                "finish_reason": record.get("finish_reason"), "error": error,
                "actual_output_tokens": record.get("actual_output_tokens"),
            })
    succeeded = sum(item["transport_success"] for item in scored)
    correct = sum(item["correct"] for item in scored)
    report = {
        "schema_version": SCHEMA_VERSION, "dataset_id": DATASET_ID, "model": model,
        "input_sha256": input_hash, "scoring_rule": SCORING_RULE, "generation": dict(GENERATION),
        "status": "complete" if succeeded == 32 else "incomplete",
        "valid_for_quality_comparison": succeeded == 32, "total": 32,
        "successful_requests": succeeded, "failed_requests": 32 - succeeded,
        "correct_count": correct, "accuracy": correct / 32,
        "accuracy_denominator": "all 32 tasks; request failures count as incorrect and mark report incomplete",
        "length_limit_count": sum(item["finish_reason"] == "length" for item in scored),
        "by_category": {
            category: {"total": 16, "correct_count": sum(x["correct"] for x in scored if x["category"] == category),
                       "accuracy": sum(x["correct"] for x in scored if x["category"] == category) / 16}
            for category in ("field_extraction", "fact_lookup")
        },
        "scope": "fixed synthetic tasks only; no production quality or statistical significance claim",
        "items": scored,
    }
    _write_json(folder / "quality_report.json", report)
    return report


def compare_quality(bf16: dict[str, Any], awq: dict[str, Any]) -> dict[str, Any]:
    """对齐同一任务集；失败请求单列，不冒充模型答案退化或改善。"""
    for report in (bf16, awq):
        if (report.get("dataset_id") != DATASET_ID or report.get("scoring_rule") != SCORING_RULE
                or report.get("generation") != GENERATION or len(report.get("items", [])) != 32):
            raise ValueError("质量报告的数据集、评分或生成规则不匹配")
    if bf16.get("input_sha256") != awq.get("input_sha256"):
        raise ValueError("BF16 与 AWQ 任务输入哈希不一致")
    before = {item["request_id"]: item for item in bf16["items"]}
    after = {item["request_id"]: item for item in awq["items"]}
    if len(before) != 32 or len(after) != 32 or before.keys() != after.keys():
        raise ValueError("质量报告任务 ID 缺失、重复或不一致")
    regressions, improvements, failed_pairs = [], [], []
    unchanged_correct = unchanged_incorrect = 0
    for request_id, left in before.items():
        right = after[request_id]
        if any(left.get(key) != right.get(key) for key in (
            "category", "expected_answer", "prompt_sha256", "item_sha256",
        )):
            raise ValueError(f"{request_id} 的题目或标签不一致")
        if not (left.get("transport_success") is True and right.get("transport_success") is True):
            failed_pairs.append(request_id)
            continue
        for item in (left, right):
            expected_score = item.get("finish_reason") != "length" and exact_match(item.get("raw_output"), item["expected_answer"])
            if item.get("correct") is not expected_score:
                raise ValueError(f"{request_id} 的评分与原始输出不一致")
        detail = {"request_id": request_id, "category": left["category"],
                  "expected_answer": left["expected_answer"],
                  "bf16_output": left["raw_output"], "awq_output": right["raw_output"]}
        if left["correct"] and not right["correct"]:
            regressions.append(detail)
        elif not left["correct"] and right["correct"]:
            improvements.append(detail)
        elif left["correct"]:
            unchanged_correct += 1
        else:
            unchanged_incorrect += 1
    bf16_correct = sum(x.get("transport_success") is True and x.get("correct") is True for x in before.values())
    awq_correct = sum(x.get("transport_success") is True and x.get("correct") is True for x in after.values())
    return {
        "schema_version": SCHEMA_VERSION, "dataset_id": DATASET_ID,
        "input_sha256": bf16["input_sha256"], "total": 32,
        "valid_for_quality_comparison": not failed_pairs,
        "bf16_correct_count": bf16_correct, "awq_correct_count": awq_correct,
        "bf16_accuracy": bf16_correct / 32, "awq_accuracy": awq_correct / 32,
        "accuracy_percentage_point_change": (awq_correct - bf16_correct) * 100 / 32,
        "regressions": regressions, "improvements": improvements,
        "unchanged_correct": unchanged_correct, "unchanged_incorrect": unchanged_incorrect,
        "failed_pairs": failed_pairs,
        "scope": "paired outcomes on 32 fixed synthetic tasks; failed pairs are not quality regressions",
    }
