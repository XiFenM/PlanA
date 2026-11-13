#!/usr/bin/env python3
"""质量输入、严格评分与失败保留的标准库测试；不加载模型或访问网络。"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import patch

import quality


class MockTokenizer:
    def __init__(self, offset=0):
        self.offset = offset
        self.calls = []

    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt, return_dict=False):
        self.calls.append((deepcopy(messages), tokenize, add_generation_prompt, return_dict))
        data = json.dumps(messages, ensure_ascii=False, sort_keys=True).encode()
        ids = [1 + self.offset] + list(hashlib.sha256(data).digest())
        return {"input_ids": ids, "attention_mask": [1] * len(ids)} if return_dict else ids


class NewDefaultTokenizer(MockTokenizer):
    """模拟新版默认返回 BatchEncoding 的 Mapping 接口，不依赖 transformers。"""

    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt, return_dict=True):
        return super().apply_chat_template(
            messages, tokenize=tokenize, add_generation_prompt=add_generation_prompt,
            return_dict=return_dict,
        )


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.bundle = quality.build_quality_inputs(MockTokenizer())

    def run_quality(self, folder, answers=None, failures=(), deadline=None, truncated=(), wrong_ids=()):
        expected = {x["request_id"]: x["expected_answer"] for x in self.bundle["items"]}
        overrides = answers or {}
        requests = []

        def respond(base_url, model, request, *, timeout, stream):
            requests.append(deepcopy(request))
            self.assertFalse(stream)
            self.assertGreater(timeout, 0)
            request_id = request["request_id"]
            if request_id in failures:
                raise RuntimeError("synthetic network failure")
            return {"request_id": "mismatched-response-id" if request_id in wrong_ids else request_id, "success": True,
                    "text": overrides.get(request_id, expected[request_id]),
                    "finish_reason": "length" if request_id in truncated else "stop",
                    "actual_output_tokens": 32 if request_id in truncated else 4, "error": None}

        with patch.dict(sys.modules, {"client": types.SimpleNamespace(request_once=respond)}):
            result = quality.evaluate_quality(
                "http://127.0.0.1:8000", "test-model", self.bundle, folder,
                time.monotonic() + 10 if deadline is None else deadline,
            )
        return result, requests

    def test_deterministic_unique_rules_and_labels_independent_of_tokenizer(self):
        other_tokenizer = MockTokenizer(offset=400)
        other = quality.build_quality_inputs(other_tokenizer)
        self.assertEqual(self.bundle, quality.build_quality_inputs(MockTokenizer()))
        self.assertEqual(32, len({x["request_id"] for x in self.bundle["items"]}))
        self.assertEqual(32, len({x["messages"][1]["content"] for x in self.bundle["items"]}))
        self.assertEqual([x["expected_answer"] for x in self.bundle["items"]],
                         [x["expected_answer"] for x in other["items"]])
        self.assertNotEqual(self.bundle["input_sha256"], other["input_sha256"])
        for item in self.bundle["items"]:
            source = item["label_source"]
            selected = next(x for x in source["records"] if x["编号"] == source["target_id"])
            self.assertEqual(selected[source["target_field"]], item["expected_answer"])
            self.assertEqual(4, len(source["records"]))
        self.assertEqual(16, sum(x["category"] == "field_extraction" for x in self.bundle["items"]))
        self.assertTrue(all(tokenize and generation and return_dict is False
                            for _, tokenize, generation, return_dict in other_tokenizer.calls))

    def test_new_mapping_default_preserves_legacy_inputs_with_explicit_false(self):
        messages = self.bundle["items"][0]["messages"]
        default_result = NewDefaultTokenizer().apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True,
        )
        self.assertIsInstance(default_result, dict)
        self.assertEqual(self.bundle["items"][0]["prompt_token_ids"], default_result["input_ids"])
        tokenizer = NewDefaultTokenizer()
        result = quality.build_quality_inputs(tokenizer)
        self.assertEqual(self.bundle, result)
        self.assertEqual(32, len(tokenizer.calls))
        self.assertTrue(all(call[3] is False for call in tokenizer.calls))
        self.assertEqual("bf5b1c62418a637f92485e5381dd30ceded7b009beea655ffa837abe688b410a",
                         result["input_sha256"])

    def test_invalid_tokenizer_results_are_not_flattened_or_coerced(self):
        for returned in ([], [[1, 2]], [True], [1, -1], {"input_ids": [1, 2]}):
            with self.subTest(returned=returned):
                tokenizer = types.SimpleNamespace(apply_chat_template=lambda *args, **kwargs: returned)
                with self.assertRaisesRegex(ValueError, "token ID"):
                    quality.build_quality_inputs(tokenizer)

    def test_parser_only_strips_outer_whitespace(self):
        self.assertTrue(quality.exact_match(" \nHUB-123\t", "HUB-123"))
        for output in ('"HUB-123"', "答案：HUB-123", "HUB-123。", "hub-123", "HUB -123", "```HUB-123```", ""):
            with self.subTest(output=output):
                self.assertFalse(quality.exact_match(output, "HUB-123"))
        with self.assertRaises(ValueError):
            quality.exact_match(None, "HUB-123")

    def test_natural_eos_request_and_raw_outputs_persist(self):
        item = self.bundle["items"][0]
        raw = " \n" + item["expected_answer"] + "\t"
        with tempfile.TemporaryDirectory() as directory:
            report, requests = self.run_quality(directory, {item["request_id"]: raw})
            self.assertEqual("complete", report["status"])
            self.assertEqual(32, report["correct_count"])
            self.assertEqual(32, len(requests))
            self.assertTrue(all(x["ignore_eos"] is False and x["max_tokens"] == 32 for x in requests))
            self.assertTrue(all(x["skip_special_tokens"] is True for x in requests))
            self.assertEqual(raw, report["items"][0]["raw_output"])
            records = [json.loads(line) for line in (Path(directory) / "quality_raw.jsonl").read_text().splitlines()]
            self.assertEqual(32, len(records))
            self.assertEqual(raw, records[0]["record"]["text"])
            self.assertEqual(report, json.loads((Path(directory) / "quality_report.json").read_text()))

    def test_failure_and_deadline_do_not_drop_tasks(self):
        failed_id = self.bundle["items"][0]["request_id"]
        with tempfile.TemporaryDirectory() as directory:
            report, _ = self.run_quality(directory, failures={failed_id})
            self.assertEqual("incomplete", report["status"])
            self.assertFalse(report["valid_for_quality_comparison"])
            self.assertEqual(31, report["correct_count"])
            self.assertEqual(32, len(report["items"]))
            self.assertIn("synthetic network failure", report["items"][0]["error"])
        with tempfile.TemporaryDirectory() as directory:
            report, requests = self.run_quality(directory, deadline=time.monotonic() - 1)
            self.assertFalse(requests)
            self.assertEqual(32, report["failed_requests"])
            self.assertEqual(32, len((Path(directory) / "quality_raw.jsonl").read_text().splitlines()))

    def test_labels_or_tokens_cannot_be_silently_changed(self):
        for change in ("label", "tokens", "duplicate"):
            bundle = deepcopy(self.bundle)
            if change == "label":
                bundle["items"][0]["expected_answer"] = "BF16 fabricated answer"
            elif change == "tokens":
                bundle["items"][0]["prompt_token_ids"][0] += 1
            else:
                bundle["items"][1] = deepcopy(bundle["items"][0])
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                with patch.dict(sys.modules, {"client": types.SimpleNamespace(request_once=lambda *a, **k: None)}):
                    with self.assertRaises(ValueError):
                        quality.evaluate_quality("http://127.0.0.1:8000", "model", bundle, directory, time.monotonic() + 10)
                self.assertFalse(list(Path(directory).iterdir()))

    def test_comparison_aligns_by_id_and_separates_changes(self):
        first, second = [x["request_id"] for x in self.bundle["items"][:2]]
        with tempfile.TemporaryDirectory() as directory:
            bf16, _ = self.run_quality(Path(directory) / "bf16", {second: "wrong"})
            awq, _ = self.run_quality(Path(directory) / "awq", {first: "wrong"})
            awq["items"].reverse()
            result = quality.compare_quality(bf16, awq)
            self.assertEqual([first], [x["request_id"] for x in result["regressions"]])
            self.assertEqual([second], [x["request_id"] for x in result["improvements"]])
            self.assertEqual(0, result["accuracy_percentage_point_change"])
            awq["items"][0]["expected_answer"] = "changed label"
            with self.assertRaises(ValueError):
                quality.compare_quality(bf16, awq)

    def test_failed_pair_is_not_a_quality_regression(self):
        failed_id = self.bundle["items"][0]["request_id"]
        with tempfile.TemporaryDirectory() as directory:
            bf16, _ = self.run_quality(Path(directory) / "bf16")
            awq, _ = self.run_quality(Path(directory) / "awq", failures={failed_id})
            result = quality.compare_quality(bf16, awq)
            self.assertEqual([failed_id], result["failed_pairs"])
            self.assertFalse(result["regressions"])
            self.assertFalse(result["valid_for_quality_comparison"])

    def test_truncation_is_incorrect_without_becoming_protocol_failure(self):
        first = self.bundle["items"][0]["request_id"]
        with tempfile.TemporaryDirectory() as directory:
            bf16, _ = self.run_quality(Path(directory) / "bf16")
            awq, _ = self.run_quality(Path(directory) / "awq", truncated={first})
            self.assertTrue(awq["valid_for_quality_comparison"])
            self.assertEqual(31, awq["correct_count"])
            self.assertEqual(1, awq["length_limit_count"])
            result = quality.compare_quality(bf16, awq)
            self.assertEqual([first], [x["request_id"] for x in result["regressions"]])

    def test_misaligned_response_and_edited_score_are_rejected(self):
        first = self.bundle["items"][0]["request_id"]
        with tempfile.TemporaryDirectory() as directory:
            bf16, _ = self.run_quality(Path(directory) / "bf16")
            awq, _ = self.run_quality(Path(directory) / "wrong-id", wrong_ids={first})
            self.assertEqual(1, awq["failed_requests"])
            self.assertIn("request_id", awq["items"][0]["error"])
            awq = deepcopy(bf16)
            awq["items"][0]["correct"] = False
            with self.assertRaises(ValueError):
                quality.compare_quality(bf16, awq)

    def test_all_wrong_answers_are_complete_without_score_gate(self):
        answers = {x["request_id"]: "wrong" for x in self.bundle["items"]}
        with tempfile.TemporaryDirectory() as directory:
            report, _ = self.run_quality(directory, answers)
            self.assertEqual("complete", report["status"])
            self.assertTrue(report["valid_for_quality_comparison"])
            self.assertEqual(0, report["accuracy"])

    def test_repeated_run_does_not_overwrite_results(self):
        with tempfile.TemporaryDirectory() as directory:
            report, _ = self.run_quality(directory)
            before = (Path(directory) / "quality_report.json").read_bytes()
            with self.assertRaises(FileExistsError):
                self.run_quality(directory)
            self.assertEqual(before, (Path(directory) / "quality_report.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
