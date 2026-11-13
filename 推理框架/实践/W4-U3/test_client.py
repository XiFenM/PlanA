"""W4-U3 客户端合同测试：本机假服务与构造样本，不是 GPU/vLLM 性能实测。"""
from __future__ import annotations

import contextlib
import copy
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import client  # noqa: E402


def request(request_id="r0", max_tokens=4):
    return {"request_id": request_id, "prompt_token_ids": [10, 11], "max_tokens": max_tokens}


def event(payload, *, multiline=False):
    text = json.dumps(payload, ensure_ascii=False)
    if multiline:
        left, right = text.split(",", 1)
        return ("data: " + left + ",\r\ndata: " + right + "\r\n\r\n").encode("utf-8")
    return ("data: " + text + "\n\n").encode("utf-8")


def completion(text, ids, finish=None):
    return {"id": "cmpl-mock", "choices": [
        {"index": 0, "text": text, "token_ids": ids, "finish_reason": finish,
         "logprobs": {"tokens": ["token_id:" + str(x) for x in ids],
                      "token_logprobs": [-0.2] * len(ids),
                      "top_logprobs": [{"token_id:" + str(x): -0.2} for x in ids]}}
    ]}


def stream_chunks(*, usage=True, finish="length", done=True, usage_count=4):
    chunks = [event(completion("", [20])),
              event(completion("甲", [21, 22]), multiline=True),
              event(completion("乙", [23], finish))]
    if usage:
        chunks.append(event({"id": "cmpl-mock", "choices": [],
                             "usage": {"prompt_tokens": 2, "completion_tokens": usage_count,
                                       "total_tokens": 2 + usage_count}}))
    if done:
        chunks.append(b"data: [DONE]\n\n")
    return chunks


@contextlib.contextmanager
def local_service(responder):
    """每次用独立 127.0.0.1 端口，server 线程不能生成任何 GPU 证据。"""
    state = {"received": [], "active": 0, "max_active": 0, "lock": threading.Lock()}

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            pass

        def do_POST(self):
            raw = self.rfile.read(int(self.headers["Content-Length"]))
            payload = json.loads(raw)
            with state["lock"]:
                state["received"].append({"path": self.path, "body": payload,
                                           "raw": raw, "headers": dict(self.headers)})
                state["active"] += 1
                state["max_active"] = max(state["max_active"], state["active"])
            try:
                responder(self, payload, state)
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                with state["lock"]:
                    state["active"] -= 1
                self.close_connection = True

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", state
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def send_stream(handler, chunks, *, fragment=False, pause=0):
    handler.send_response(200)
    handler.send_header("Content-Type", "text/event-stream; charset=utf-8")
    handler.send_header("x-request-id", "mock-server-request")
    handler.send_header("Connection", "close")
    handler.end_headers()
    for chunk in chunks:
        if pause:
            time.sleep(pause)
        if fragment:
            for offset in range(0, len(chunk), 3):
                handler.wfile.write(chunk[offset:offset + 3])
                handler.wfile.flush()
        else:
            handler.wfile.write(chunk)
            handler.wfile.flush()


def errors(record):
    return {e["code"] for e in record["errors"]}


class SSEDecoderTests(unittest.TestCase):
    def test_byte_fragmentation_utf8_bom_multiline_crlf_and_comments(self):
        wire = (b"\xef\xbb\xbf: keepalive\r\nid: ignored\r\nevent: update\r\n"
                + event({"id": "中文", "choices": []}, multiline=True)
                + b": another comment\n\ndata: [DONE]\n\n")
        decoder = client.SSEDecoder()
        actual = []
        for byte in wire:
            actual.extend(decoder.feed(bytes([byte])))
        actual.extend(decoder.feed(b"", final=True))
        self.assertEqual(actual[0][0], "update")
        self.assertEqual(json.loads(actual[0][1]), {"id": "中文", "choices": []})
        self.assertEqual(actual[1], ("message", "[DONE]"))
        self.assertEqual(len(actual), 2)

    def test_lone_cr_and_eof_do_not_invent_final_event(self):
        decoder = client.SSEDecoder()
        self.assertEqual(decoder.feed(b"data: one\r\rdata: incomplete", final=True),
                         [("message", "one")])

    def test_invalid_utf8_is_explicit_error(self):
        with self.assertRaises(UnicodeDecodeError):
            client.SSEDecoder().feed(b"data: \xff\n\n", final=True)


class RequestTests(unittest.TestCase):
    def test_real_socket_stream_fragments_empty_text_usage_tail_and_token_ids(self):
        with local_service(lambda h, p, s: send_stream(h, stream_chunks(), fragment=True, pause=0.01)) as (url, state):
            record = client.request_once(url + "/v1", "mock-model", request(), timeout=2)
        self.assertTrue(record["success"], record["error"])
        self.assertEqual(record["text"], "甲乙")
        self.assertEqual(record["generated_token_ids"], [20, 21, 22, 23])
        self.assertEqual(record["actual_output_tokens"], 4)
        self.assertEqual(len(record["text_events"]), 2)
        self.assertEqual(record["text_events"][0]["token_ids"], [21, 22])
        self.assertEqual(len(record["stream_events"]), 4)
        self.assertEqual(record["server_request_id"], "mock-server-request")
        self.assertEqual(record["response_id"], "cmpl-mock")
        self.assertLess(record["last_text_monotonic_s"], record["stream_done_monotonic_s"])
        sent = state["received"][0]
        self.assertEqual(sent["path"], "/v1/completions")
        self.assertEqual(record["request_body_sha256"], hashlib.sha256(sent["raw"]).hexdigest())
        expected = {"model": "mock-model", "prompt": [10, 11], "max_tokens": 4,
                    "stream": True, "temperature": 0.0, "ignore_eos": True,
                    "seed": client.SEED, "return_token_ids": True, "n": 1, "echo": False,
                    "stream_options": {"include_usage": True}}
        self.assertEqual(sent["body"], expected)
        self.assertNotIn("Authorization", sent["headers"])
        self.assertIsNone(record["response_json"])
        self.assertEqual(record["logprobs"][1]["tokens"], ["token_id:21", "token_id:22"])

    def test_missing_usage_is_failure_even_with_exact_token_ids(self):
        with local_service(lambda h, p, s: send_stream(h, stream_chunks(usage=False))) as (url, _):
            record = client.request_once(url, "mock", request())
        self.assertFalse(record["success"])
        self.assertIn("missing_usage", errors(record))
        self.assertEqual(record["actual_output_tokens"], 4)

    def test_prompt_usage_must_match_the_exact_input_token_ids(self):
        for count, expected_code in ((None, "invalid_prompt_usage"), (-1, "invalid_prompt_usage"),
                                     (True, "invalid_prompt_usage"), (2.0, "invalid_prompt_usage"),
                                     (3, "prompt_token_mismatch")):
            payload = completion("甲乙", [20, 21, 22, 23], "length")
            payload["usage"] = {"completion_tokens": 4}
            if count is not None:
                payload["usage"]["prompt_tokens"] = count
            chunks = [event(payload), b"data: [DONE]\n\n"]
            with self.subTest(prompt_tokens=count):
                with local_service(lambda h, p, s: send_stream(h, chunks)) as (url, _):
                    record = client.request_once(url, "mock", request())
                self.assertFalse(record["success"])
                self.assertIn(expected_code, errors(record))
                self.assertEqual(record["actual_output_tokens"], 4)

    def test_unexpected_finish_and_inconsistent_usage_are_explicit(self):
        with local_service(lambda h, p, s: send_stream(h, stream_chunks(finish="stop", usage_count=9))) as (url, _):
            record = client.request_once(url, "mock", request())
        self.assertFalse(record["success"])
        self.assertTrue({"usage_token_mismatch", "unexpected_finish_reason"} <= errors(record))

    def test_missing_token_ids_does_not_guess_count_from_text_or_usage(self):
        chunks = [event({"choices": [{"text": "文字长度不等于token数", "finish_reason": "length"}],
                         "usage": {"completion_tokens": 4}}), b"data: [DONE]\n\n"]
        with local_service(lambda h, p, s: send_stream(h, chunks)) as (url, _):
            record = client.request_once(url, "mock", request())
        self.assertFalse(record["success"])
        self.assertIsNone(record["actual_output_tokens"])
        self.assertIn("missing_token_ids", errors(record))

    def test_http_failure_retains_status_and_body(self):
        def responder(h, p, s):
            body = b'{"error":{"message":"mock capacity error"}}'
            h.send_response(503)
            h.send_header("Content-Length", str(len(body)))
            h.send_header("Connection", "close")
            h.end_headers()
            h.wfile.write(body)
        with local_service(responder) as (url, _):
            record = client.request_once(url, "mock", request())
        self.assertFalse(record["success"])
        self.assertEqual(record["http_status"], 503)
        self.assertIn("http_error", errors(record))
        self.assertEqual(record["response_json"]["error"]["message"], "mock capacity error")

    def test_invalid_json_missing_done_and_server_sse_error(self):
        cases = [([b"data: {invalid}\n\n"], "transport_or_protocol_error"),
                 ([b'data: {"choices": [], "invalid": NaN}\n\n'], "transport_or_protocol_error"),
                 (stream_chunks(done=False), "missing_done"),
                 ([b'event: error\ndata: {"error":"mock failure"}\n\ndata: [DONE]\n\n'], "server_error")]
        for chunks, code in cases:
            with self.subTest(code=code):
                with local_service(lambda h, p, s: send_stream(h, chunks)) as (url, _):
                    record = client.request_once(url, "mock", request())
                self.assertFalse(record["success"])
                self.assertIn(code, errors(record))

    def test_nonstream_preserves_original_json_ids_and_logprobs_mapping(self):
        response = completion("甲乙", [20, 21, 22, 23], "length")
        response["usage"] = {"prompt_tokens": 2, "completion_tokens": 4, "total_tokens": 6}

        def responder(h, p, s):
            raw = json.dumps(response, ensure_ascii=False).encode("utf-8")
            h.send_response(200)
            h.send_header("Content-Type", "application/json")
            h.send_header("Content-Length", str(len(raw)))
            h.send_header("Connection", "close")
            h.end_headers()
            h.wfile.write(raw)
        req = request()
        req["extra_body"] = {"logprobs": 1, "return_tokens_as_token_ids": True}
        with local_service(responder) as (url, state):
            record = client.request_once(url, "mock", req, stream=False)
        self.assertTrue(record["success"], record["error"])
        self.assertEqual(record["response_json"], response)
        self.assertEqual(record["server_request_id"], "cmpl-mock")
        self.assertEqual(record["server_request_id_source"], "response.id")
        self.assertEqual(record["text_events"], [])
        self.assertIsNone(record["first_text_monotonic_s"])
        self.assertIsNotNone(record["response_received_monotonic_s"])
        self.assertFalse(state["received"][0]["body"]["stream"])
        self.assertNotIn("stream_options", state["received"][0]["body"])
        self.assertEqual(state["received"][0]["body"]["logprobs"], 1)

    def test_total_timeout_bounds_trickling_response_with_connection_close(self):
        def responder(h, p, s):
            send_stream(h, [b": keepalive\n\n"] * 100, pause=0.01)
        with local_service(responder) as (url, _):
            start = time.monotonic()
            record = client.request_once(url, "mock", request(), timeout=0.08)
            elapsed = time.monotonic() - start
        self.assertFalse(record["success"])
        self.assertIn("timeout", errors(record))
        self.assertLess(elapsed, 0.7, "不能让持续滴流无限刷新读超时")

    def test_rejects_remote_urls_and_contract_overrides_before_network(self):
        for url in ("https://127.0.0.1:8000", "http://localhost:8000", "http://example.com",
                    "http://user:pass@127.0.0.1:8000", "http://127.0.0.1:8000/?key=a"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                client.request_once(url, "mock", request())
        for override in ("stream", "prompt", "ignore_eos", "temperature", "return_token_ids", "seed"):
            req = request()
            req["extra_body"] = {override: None}
            with self.subTest(override=override), self.assertRaises(ValueError):
                client.request_once("http://127.0.0.1:1", "mock", req)
        for timeout in (0, -1, float("inf"), float("nan"), True):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                client.request_once("http://127.0.0.1:1", "mock", request(), timeout=timeout)


def raw_record(rid, *, enqueue, send, times, end, tokens, success=True):
    return {"request_id": rid, "request_index": int(rid[1:]), "stream": True,
            "enqueue_monotonic_s": enqueue, "send_start_monotonic_s": send,
            "end_monotonic_s": end, "success": success, "actual_output_tokens": tokens,
            "text_events": [{"time_monotonic_s": t, "text": "x"} for t in times],
            # 故意放入假的派生值，汇总必须重新计算。
            "ttft_ms": -999, "tpot_ms": -999, "raw_itl_ms": [-999]}


class SummaryTests(unittest.TestCase):
    def test_recompute_metrics_excludes_failed_tokens_but_keeps_whole_window(self):
        records = [raw_record("r0", enqueue=100, send=101, times=[102, 103, 112], end=114, tokens=5),
                   raw_record("r1", enqueue=100, send=102, times=[104, 105], end=113, tokens=3),
                   raw_record("r2", enqueue=100, send=104, times=[105, 119], end=120, tokens=100, success=False)]
        before = copy.deepcopy(records)
        summary = client.summarize(records, 100, 120)
        self.assertEqual(records, before)
        self.assertEqual(summary["success_count"], 2)
        self.assertEqual(summary["failure_count"], 1)
        self.assertEqual(summary["successful_output_tokens"], 8)
        self.assertEqual(summary["window_seconds"], 20)
        self.assertAlmostEqual(summary["output_tokens_per_second"], 0.4)
        self.assertEqual(summary["queue_wait_ms"]["count"], 3)
        self.assertAlmostEqual(summary["queue_wait_ms"]["mean"], 7000 / 3)
        self.assertEqual(summary["request_ttft_ms"]["p50"], 1500)
        self.assertEqual(summary["request_e2el_ms"]["p50"], 7000)
        self.assertEqual(summary["request_tpot_ms"]["p50"], 1500)
        self.assertEqual(summary["request_tpot_ms"]["p99"], 2480)
        self.assertEqual(summary["pooled_raw_itl_ms"]["count"], 3)
        self.assertEqual(summary["pooled_raw_itl_ms"]["p50"], 1000)
        self.assertAlmostEqual(summary["pooled_raw_itl_ms"]["p99"], 8840)
        self.assertNotEqual(summary["request_tpot_ms"]["p99"], summary["pooled_raw_itl_ms"]["p99"])
        failed = summary["per_request_metrics"][2]
        self.assertFalse(failed["success"])
        self.assertEqual(failed["raw_itl_ms"], [14000])
        self.assertTrue(summary["exploratory"])
        json.dumps(summary, allow_nan=False)

    def test_long_gap_survives_pooling_and_is_not_replaced_by_request_mean(self):
        times = [1.0]
        for gap in [0.001] * 98 + [0.501]:
            times.append(times[-1] + gap)
        r = raw_record("r0", enqueue=0, send=0, times=times, end=2, tokens=100)
        summary = client.summarize([r], 0, 2)
        pooled = summary["pooled_raw_itl_ms"]
        self.assertEqual(pooled["count"], 99)
        self.assertAlmostEqual(pooled["mean"], 599 / 99)
        self.assertAlmostEqual(pooled["p50"], 1)
        self.assertAlmostEqual(pooled["p99"], 11)
        self.assertAlmostEqual(pooled["max"], 501)
        self.assertAlmostEqual(summary["request_tpot_ms"]["p99"], 599 / 99)
        self.assertGreater(pooled["p99"], pooled["mean"])

    def test_one_token_and_single_text_chunk_do_not_fabricate_itl(self):
        records = [raw_record("r0", enqueue=0, send=0, times=[1], end=2, tokens=1),
                   raw_record("r1", enqueue=0, send=0, times=[1], end=2, tokens=10)]
        summary = client.summarize(records, 0, 3)
        self.assertIsNone(summary["per_request_metrics"][0]["tpot_ms"])
        self.assertEqual(summary["per_request_metrics"][1]["tpot_ms"], 0)
        self.assertEqual(summary["request_tpot_ms"]["count"], 1)
        self.assertEqual(summary["pooled_raw_itl_ms"]["count"], 0)
        self.assertIsNone(summary["pooled_raw_itl_ms"]["p99"])

    def test_all_failures_still_have_valid_zero_throughput_summary(self):
        r = raw_record("r0", enqueue=0, send=1, times=[], end=5, tokens=None, success=False)
        summary = client.summarize([r], 0, 5)
        self.assertEqual(summary["output_tokens_per_second"], 0)
        self.assertEqual(summary["request_ttft_ms"]["count"], 0)
        self.assertEqual(summary["queue_wait_ms"]["p50"], 1000)

    def test_summary_rejects_reversed_times_duplicate_ids_or_wrong_window(self):
        r = raw_record("r0", enqueue=0, send=1, times=[2, 3], end=4, tokens=2)
        for records, start, end in [([r], 0, 3), ([r], 4, 5), ([r, r], 0, 5), ([], 0, 5), ([r], 0, 0)]:
            with self.subTest(records=len(records), window=(start, end)), self.assertRaises(ValueError):
                client.summarize(records, start, end)
        r["text_events"].reverse()
        with self.assertRaises(ValueError):
            client.summarize([r], 0, 5)


class BatchTests(unittest.TestCase):
    def test_batch_deadline_stops_trickling_and_preserves_unsent_queue(self):
        def responder(h, p, s):
            send_stream(h, [b": keepalive\n\n"] * 100, pause=0.01)

        requests = [request(f"r{i}") for i in range(12)]
        with tempfile.TemporaryDirectory() as tmp, local_service(responder) as (url, state):
            output = Path(tmp) / "deadline.jsonl"
            start = time.monotonic()
            deadline = start + 0.10
            summary = client.run_batch(url, "mock", requests, 2, output,
                                       timeout=0.8, deadline_monotonic=deadline)
            elapsed = time.monotonic() - start
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
        self.assertLess(elapsed, 0.6, "总期限后不能再发送余下五波请求")
        self.assertEqual(len(state["received"]), 2)
        self.assertEqual(summary["failure_count"], 12)
        self.assertEqual(summary["success_count"], 0)
        self.assertEqual(summary["output_tokens_per_second"], 0)
        self.assertEqual(len(records), 12)
        self.assertEqual({r["request_index"] for r in records}, set(range(12)))
        self.assertTrue(all("batch_deadline_exceeded" in errors(r) for r in records))
        unsent = [r for r in records if not r["request_sent"]]
        self.assertEqual(len(unsent), 10)
        self.assertTrue(all(r["send_start_monotonic_s"] is None for r in unsent))
        self.assertTrue(all(r["http_status"] is None for r in unsent))
        self.assertTrue(all(r["text_events"] == [] for r in unsent))
        self.assertEqual(summary["queue_wait_ms"]["count"], 12)
        self.assertEqual(summary["batch_deadline_monotonic_s"], deadline)
        recomputed = client.summarize(records, summary["window_start_monotonic_s"],
                                     summary["window_end_monotonic_s"])
        for key in recomputed:
            self.assertEqual(summary[key], recomputed[key])

    def test_already_expired_batch_sends_nothing_and_still_records_every_request(self):
        with tempfile.TemporaryDirectory() as tmp, local_service(
                lambda h, p, s: send_stream(h, stream_chunks())) as (url, state):
            output = Path(tmp) / "expired.jsonl"
            summary = client.run_batch(url, "mock", [request("r0"), request("r1")], 2, output,
                                       deadline_monotonic=time.monotonic() - 1)
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(state["received"], [])
        self.assertEqual(summary["request_count"], 2)
        self.assertEqual(summary["failure_count"], 2)
        self.assertEqual(summary["request_ttft_ms"]["count"], 0)
        self.assertTrue(all(r["send_start_monotonic_s"] is None for r in records))
        self.assertTrue(all(r["request_sent"] is False for r in records))
        self.assertTrue(all(errors(r) == {"batch_deadline_exceeded"} for r in records))

    def test_finite_pool_keeps_failures_limits_concurrency_and_recomputes_jsonl(self):
        def responder(h, p, s):
            time.sleep(0.025)
            if p["prompt"][0] == 99:
                send_stream(h, stream_chunks(usage=False))
            else:
                send_stream(h, stream_chunks())
        requests = [request(f"r{i}") for i in range(7)]
        requests[3]["prompt_token_ids"][0] = 99
        with tempfile.TemporaryDirectory() as tmp, local_service(responder) as (url, state):
            output = Path(tmp) / "raw.jsonl"
            summary = client.run_batch(url, "mock", requests, 2, output, phase="mock-test")
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            recomputed = client.summarize(records, summary["window_start_monotonic_s"],
                                         summary["window_end_monotonic_s"])
            for key in recomputed:
                self.assertEqual(summary[key], recomputed[key])
            self.assertEqual(len(records), 7)
            self.assertEqual({r["request_index"] for r in records}, set(range(7)))
            self.assertEqual(len({r["enqueue_monotonic_s"] for r in records}), 1)
            self.assertTrue(all(r["phase"] == "mock-test" for r in records))
            self.assertEqual(summary["success_count"], 6)
            self.assertEqual(summary["failure_count"], 1)
            self.assertEqual(summary["successful_output_tokens"], 24)
            self.assertEqual(state["max_active"], 2)
            self.assertGreater(summary["queue_wait_ms"]["max"], 25)
            before = output.read_bytes()
            with self.assertRaises(FileExistsError):
                client.run_batch(url, "mock", requests, 2, output)
            self.assertEqual(output.read_bytes(), before)

    def test_each_completed_request_is_flushed_before_slow_request_finishes(self):
        release_slow = threading.Event()
        slow_arrived = threading.Event()

        def responder(h, p, s):
            if p["prompt"][0] == 99:
                slow_arrived.set()
                release_slow.wait(timeout=2)
            send_stream(h, stream_chunks())

        requests = [request("r0"), request("r1")]
        requests[1]["prompt_token_ids"][0] = 99
        with tempfile.TemporaryDirectory() as tmp, local_service(responder) as (url, _):
            output = Path(tmp) / "raw.jsonl"
            result = []
            runner = threading.Thread(target=lambda: result.append(client.run_batch(url, "mock", requests, 2, output)))
            runner.start()
            try:
                self.assertTrue(slow_arrived.wait(timeout=1))
                deadline = time.monotonic() + 1
                while time.monotonic() < deadline:
                    if output.exists() and output.stat().st_size:
                        break
                    time.sleep(0.005)
                rows = output.read_text(encoding="utf-8").splitlines()
                self.assertEqual(len(rows), 1)
                self.assertEqual(json.loads(rows[0])["request_id"], "r0")
                self.assertTrue(runner.is_alive())
            finally:
                release_slow.set()
                runner.join(timeout=3)
            self.assertFalse(runner.is_alive())
            self.assertEqual(result[0]["request_count"], 2)


class NaturalStopTests(unittest.TestCase):
    def test_quality_natural_stop_keeps_strict_usage_checks(self):
        def responder(handler,payload,state):
            body=completion("HUB-123",[20,21],"stop")
            body["usage"]={"prompt_tokens":2,"completion_tokens":2}
            data=json.dumps(body).encode()
            handler.send_response(200)
            handler.send_header("Content-Type","application/json")
            handler.send_header("Content-Length",str(len(data)))
            handler.end_headers()
            handler.wfile.write(data)
        with local_service(responder) as (url,state):
            natural={**request(),"ignore_eos":False,"skip_special_tokens":True,
                     "spaces_between_special_tokens":False}
            result=client.request_once(url,"m",natural,stream=False)
            self.assertTrue(result["success"])
            self.assertEqual(result["actual_output_tokens"],2)
            self.assertFalse(state["received"][0]["body"]["ignore_eos"])
            self.assertTrue(state["received"][0]["body"]["skip_special_tokens"])
            fixed=client.request_once(url,"m",request(),stream=False)
            self.assertFalse(fixed["success"])

    def test_natural_stop_options_require_booleans(self):
        for key in ("ignore_eos","skip_special_tokens","spaces_between_special_tokens"):
            with self.assertRaises(ValueError):
                client._body("m",{**request(),key:1},False)


if __name__ == "__main__":
    unittest.main()
