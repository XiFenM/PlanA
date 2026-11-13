#!/usr/bin/env python3
"""W4-U2 本地 completions 客户端；仅标准库，不读取凭据或代理环境变量。

所有时间来自客户端 time.monotonic()，单位为秒。raw ITL 是相邻非空 text
事件的间隔，不能当作逐 token ITL。request_once 的非流式模式只用于正确性。
"""
from __future__ import annotations

import codecs
from concurrent.futures import ThreadPoolExecutor
import hashlib
import http.client
import json
import math
from pathlib import Path
import socket
import threading
import time
from urllib.parse import urlsplit


SEED = 20261112
SCHEMA_VERSION = 1
MAX_RESPONSE_BYTES = 64 * 1024 * 1024
CONTROLLED_FIELDS = {
    "model", "prompt", "max_tokens", "stream", "stream_options", "temperature",
    "ignore_eos", "seed", "return_token_ids", "n", "best_of", "echo",
}


def _positive_int(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} 必须是正整数")


def _endpoint(base_url):
    url = urlsplit(base_url)
    if (url.scheme != "http" or url.hostname != "127.0.0.1"
            or url.username is not None or url.password is not None
            or url.query or url.fragment):
        raise ValueError("仅允许无凭据、无查询参数的 http://127.0.0.1 本地服务")
    if url.path.rstrip("/") not in ("", "/v1", "/v1/completions"):
        raise ValueError("base_url 路径必须为空、/v1 或 /v1/completions")
    return url.hostname, url.port or 80, "/v1/completions"


def _timeout_value(timeout):
    if type(timeout) not in (int, float) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout 必须是有限正数，单位秒")
    return float(timeout)


def _body(model, request, stream):
    if not isinstance(model, str) or not model:
        raise ValueError("model 必须是非空字符串")
    if not isinstance(request, dict):
        raise ValueError("request 必须是字典")
    if not isinstance(request.get("request_id"), str) or not request["request_id"]:
        raise ValueError("request_id 必须是非空字符串")
    ids = request.get("prompt_token_ids")
    if not isinstance(ids, list) or not ids or any(type(x) is not int or x < 0 for x in ids):
        raise ValueError("prompt_token_ids 必须是非空、非负整数列表")
    _positive_int(request.get("max_tokens"), "max_tokens")
    if type(stream) is not bool:
        raise ValueError("stream 必须是 bool")
    extra = request.get("extra_body", {})
    if not isinstance(extra, dict) or any(not isinstance(k, str) for k in extra):
        raise ValueError("extra_body 必须是字符串键字典")
    if CONTROLLED_FIELDS.intersection(extra):
        raise ValueError("extra_body 不能覆盖固定协议字段")
    body = dict(extra)
    body.update(model=model, prompt=ids, max_tokens=request["max_tokens"],
                stream=stream, temperature=0.0, ignore_eos=True, seed=SEED,
                return_token_ids=True, n=1, echo=False)
    if stream:
        body["stream_options"] = {"include_usage": True}
    return json.dumps(body, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


class SSEDecoder:
    """增量 UTF-8/SSE 解析器，支持任意网络分片、CRLF 和多行 data。"""

    def __init__(self):
        self.decoder = codecs.getincrementaldecoder("utf-8-sig")("strict")
        self.buffer = ""
        self.data = []
        self.event = "message"

    def _line(self, line):
        if line == "":
            result = [(self.event, "\n".join(self.data))] if self.data else []
            self.data = []
            self.event = "message"
            return result
        if line.startswith(":"):
            return []
        field, separator, value = line.partition(":")
        if separator and value.startswith(" "):
            value = value[1:]
        if field == "data":
            self.data.append(value)
        elif field == "event":
            self.event = value or "message"
        return []

    def feed(self, chunk, final=False):
        self.buffer += self.decoder.decode(chunk, final=final)
        result = []
        while True:
            positions = [x for x in (self.buffer.find("\n"), self.buffer.find("\r")) if x >= 0]
            if not positions:
                break
            index = min(positions)
            # CR 与 LF 可能分别落在两次 read1 中。
            if self.buffer[index] == "\r" and index + 1 == len(self.buffer) and not final:
                break
            width = 2 if self.buffer[index:index + 2] == "\r\n" else 1
            line, self.buffer = self.buffer[:index], self.buffer[index + width:]
            result.extend(self._line(line))
        if final:
            if self.buffer:
                result.extend(self._line(self.buffer))
                self.buffer = ""
            # EOF 不隐含空行：未终止的 SSE 事件不能冒充已完整到达的消息。
        return result


def _error(record, code, message):
    if not any(item["code"] == code for item in record["errors"]):
        record["errors"].append({"code": code, "message": str(message)})


def _decode_json(raw):
    def reject_constant(value):
        raise ValueError(f"响应含非法 JSON 数值常量: {value}")
    return json.loads(raw, parse_constant=reject_constant)


def _new_record(model, request, index, enqueue, phase, stream, body):
    return {
        "schema_version": SCHEMA_VERSION, "request_id": request["request_id"],
        "request_index": index, "phase": phase, "model": model, "stream": stream,
        "prompt_tokens": len(request["prompt_token_ids"]), "max_tokens": request["max_tokens"],
        "request_body_sha256": hashlib.sha256(body).hexdigest(), "seed": SEED,
        "enqueue_monotonic_s": enqueue, "send_start_monotonic_s": None,
        "worker_start_monotonic_s": None, "request_sent": False,
        "first_text_monotonic_s": None, "last_text_monotonic_s": None,
        "stream_done_monotonic_s": None, "response_received_monotonic_s": None,
        "end_monotonic_s": None, "text_events": [], "stream_events": [],
        "text": "", "generated_token_ids": [], "token_ids_seen": False,
        "usage": None, "actual_output_tokens": None, "finish_reason": None,
        "logprobs": [], "response_json": None, "response_id": None,
        "server_request_id": None, "server_request_id_source": None,
        "http_status": None, "success": False, "error": None, "errors": [],
    }


def _consume_payload(record, payload, received, streaming):
    if not isinstance(payload, dict):
        raise ValueError("响应 JSON 必须是对象")
    if payload.get("error") is not None:
        _error(record, "server_error", json.dumps(payload["error"], ensure_ascii=False))
        return
    if payload.get("id") is not None:
        record["response_id"] = payload["id"]
        if record["server_request_id_source"] != "x-request-id":
            record["server_request_id"] = payload["id"]
            record["server_request_id_source"] = "response.id"
    if payload.get("usage") is not None:
        if record["usage"] is not None and record["usage"] != payload["usage"]:
            _error(record, "conflicting_usage", "收到互相矛盾的 usage")
        record["usage"] = payload["usage"]
    choices = payload.get("choices", [])
    if not isinstance(choices, list):
        raise ValueError("choices 必须是数组")
    for choice in choices:
        if not isinstance(choice, dict) or choice.get("index", 0) != 0:
            raise ValueError("仅支持 n=1 的 choice 0")
        if choice.get("finish_reason") is not None:
            if record["finish_reason"] not in (None, choice["finish_reason"]):
                _error(record, "conflicting_finish_reason", "finish_reason 发生变化")
            record["finish_reason"] = choice["finish_reason"]
        ids = choice.get("token_ids")
        if ids is not None:
            if not isinstance(ids, list) or any(type(x) is not int or x < 0 for x in ids):
                _error(record, "invalid_token_ids", "token_ids 必须是非负整数数组")
            else:
                record["token_ids_seen"] = True
                record["generated_token_ids"].extend(ids)
        if choice.get("logprobs") is not None:
            record["logprobs"].append(choice["logprobs"])
        text = choice.get("text", "")
        if not isinstance(text, str):
            raise ValueError("choice.text 必须是字符串")
        record["text"] += text
        if streaming and text != "":
            record["text_events"].append({"time_monotonic_s": received,
                                           "text": text, "token_ids": ids})
            if record["first_text_monotonic_s"] is None:
                record["first_text_monotonic_s"] = received
            record["last_text_monotonic_s"] = received


def _validate_response(record):
    if record["token_ids_seen"] and not any(x["code"] == "invalid_token_ids" for x in record["errors"]):
        record["actual_output_tokens"] = len(record["generated_token_ids"])
    else:
        _error(record, "missing_token_ids", "未获得可核对的生成 token IDs")
    usage = record["usage"]
    if not isinstance(usage, dict) or type(usage.get("completion_tokens")) is not int:
        _error(record, "missing_usage", "缺少包含 completion_tokens 整数的 usage")
    elif usage["completion_tokens"] < 0 or usage["completion_tokens"] != record["actual_output_tokens"]:
        _error(record, "usage_token_mismatch", "usage.completion_tokens 与生成 token IDs 数不一致")
    if isinstance(usage, dict):
        prompt_tokens = usage.get("prompt_tokens")
        if type(prompt_tokens) is not int or prompt_tokens < 0:
            _error(record, "invalid_prompt_usage", "usage.prompt_tokens 必须是非负整数")
        elif prompt_tokens != record["prompt_tokens"]:
            _error(record, "prompt_token_mismatch", "usage.prompt_tokens 与发送的 prompt token IDs 数不一致")
    if record["finish_reason"] != "length":
        _error(record, "unexpected_finish_reason", "固定长度合同要求 finish_reason=length")
    if record["actual_output_tokens"] != record["max_tokens"]:
        _error(record, "output_length_mismatch", "实际生成 token 数与 max_tokens 不一致")
    if record["stream"]:
        if record["stream_done_monotonic_s"] is None:
            _error(record, "missing_done", "未收到 SSE [DONE]")
        if not record["text_events"]:
            _error(record, "missing_text", "没有非空 text 事件，无法测量流式时延")


def _perform(base_url, model, request, *, timeout, stream, index, enqueue, phase, body,
             deadline_monotonic=None):
    host, port, path = _endpoint(base_url)
    record = _new_record(model, request, index, enqueue, phase, stream, body)
    record["worker_start_monotonic_s"] = time.monotonic()
    if deadline_monotonic is not None:
        record["batch_deadline_monotonic_s"] = deadline_monotonic
    # 所有已排队请求都产生记录；截止后不再建立连接或开启新一波请求。
    if deadline_monotonic is not None and time.monotonic() >= deadline_monotonic:
        _error(record, "batch_deadline_exceeded", "请求尚未发送，批次总期限已到")
        record["end_monotonic_s"] = time.monotonic()
        record["error"] = "batch_deadline_exceeded: 请求尚未发送，批次总期限已到"
        return record
    connection = http.client.HTTPConnection(host, port, timeout=timeout)
    expired = threading.Event()
    transport_socket = None
    response = None

    def expire():
        expired.set()
        # getresponse() 可把 Connection: close 的 socket 转交给 response，
        # 此后 connection.sock 为 None，仍需关闭实际传输以约束滴流响应。
        sock = transport_socket if transport_socket is not None else connection.sock
        if sock is not None:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

    record["send_start_monotonic_s"] = time.monotonic()
    request_deadline = record["send_start_monotonic_s"] + timeout
    deadline_limited = deadline_monotonic is not None and deadline_monotonic <= request_deadline
    if deadline_limited:
        request_deadline = deadline_monotonic
    effective_timeout = request_deadline - time.monotonic()
    if effective_timeout <= 0:
        record["send_start_monotonic_s"] = None
        _error(record, "batch_deadline_exceeded", "请求尚未发送，批次总期限已到")
        record["end_monotonic_s"] = time.monotonic()
        record["error"] = "batch_deadline_exceeded: 请求尚未发送，批次总期限已到"
        return record
    connection.timeout = effective_timeout
    record["effective_timeout_s"] = effective_timeout
    timer = threading.Timer(effective_timeout, expire)
    timer.daemon = True
    timer.start()
    try:
        connection.connect()
        transport_socket = connection.sock
        if expired.is_set() or time.monotonic() >= request_deadline:
            expired.set()
            raise TimeoutError("连接阶段达到请求期限")
        # HTTPConnection 不使用代理、认证配置或环境变量，不自动跟随重定向。
        record["request_sent"] = True
        connection.request("POST", path, body=body, headers={
            "Content-Type": "application/json", "Accept": "text/event-stream" if stream else "application/json",
            "Connection": "close",
        })
        response = connection.getresponse()
        record["http_status"] = response.status
        header_id = response.getheader("x-request-id")
        if header_id:
            record["server_request_id"] = header_id
            record["server_request_id_source"] = "x-request-id"
        if response.status != 200:
            error_bytes = response.read(1024 * 1024)
            try:
                record["response_json"] = _decode_json(error_bytes)
            except (ValueError, UnicodeDecodeError):
                record["response_error_text"] = error_bytes.decode("utf-8", errors="replace")
            _error(record, "http_error", f"HTTP {response.status}")
        elif stream:
            if "text/event-stream" not in (response.getheader("Content-Type") or "").lower():
                _error(record, "unexpected_content_type", "流式响应不是 text/event-stream")
            decoder = SSEDecoder()
            size = 0
            done = False
            while not done:
                chunk = response.read1(65536)
                received = time.monotonic()
                size += len(chunk)
                if size > MAX_RESPONSE_BYTES:
                    raise ValueError("响应超过字节上限")
                events = decoder.feed(chunk, final=not chunk)
                for event_type, data in events:
                    if data.strip() == "[DONE]":
                        record["stream_done_monotonic_s"] = received
                        done = True
                        break
                    payload = _decode_json(data)
                    record["stream_events"].append({"time_monotonic_s": received,
                                                     "event": event_type, "data": payload})
                    if event_type == "error":
                        _error(record, "server_error", json.dumps(payload, ensure_ascii=False))
                    _consume_payload(record, payload, received, True)
                if not chunk:
                    break
        else:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise ValueError("响应超过字节上限")
            record["response_received_monotonic_s"] = time.monotonic()
            payload = _decode_json(raw)
            record["response_json"] = payload
            _consume_payload(record, payload, record["response_received_monotonic_s"], False)
    except Exception as exc:
        code = "timeout" if expired.is_set() or isinstance(exc, TimeoutError) else "transport_or_protocol_error"
        _error(record, code, f"{type(exc).__name__}: {exc}")
    finally:
        timer.cancel()
        if time.monotonic() >= request_deadline:
            expired.set()
        if response is not None:
            response.close()
        connection.close()
        if expired.is_set():
            _error(record, "timeout", "请求超过端到端超时上限")
            if deadline_limited:
                _error(record, "batch_deadline_exceeded", "已发送请求达到批次总期限")
        _validate_response(record)
        record["end_monotonic_s"] = time.monotonic()
        record["success"] = not record["errors"] and record["http_status"] == 200
        record["error"] = "; ".join(f"{e['code']}: {e['message']}" for e in record["errors"]) or None
    return record


def request_once(base_url, model, request, *, timeout=180, stream=True):
    """执行一个请求；网络/协议失败返回失败 record，调用参数错误直接抛出。"""
    _endpoint(base_url)
    timeout = _timeout_value(timeout)
    body = _body(model, request, stream)
    return _perform(base_url, model, request, timeout=timeout, stream=stream,
                    index=0, enqueue=time.monotonic(), phase="single", body=body)


def _distribution(values):
    values = sorted(values)

    def percentile(q):
        if not values:
            return None
        position = (len(values) - 1) * q
        left = math.floor(position)
        right = math.ceil(position)
        return values[left] + (values[right] - values[left]) * (position - left)

    return {"count": len(values), "mean": math.fsum(values) / len(values) if values else None,
            "p50": percentile(0.5), "p99": percentile(0.99),
            "min": values[0] if values else None, "max": values[-1] if values else None}


def _finite(value, label):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{label} 必须是有限数值")
    return value


def summarize(records, window_start, window_end):
    """只从 raw records 重算；不信任任何缓存的 TTFT/TPOT/ITL 字段。

    时延分布仅收录成功流式请求；队列等待与完整窗口仍覆盖失败请求。
    P99 均为探索性观察：请求 TPOT 的 P99 与 pooled 消息间隔 P99 分列。
    """
    _finite(window_start, "window_start")
    _finite(window_end, "window_end")
    if window_end <= window_start:
        raise ValueError("完整批次窗口必须为正")
    records = list(records)
    if not records:
        raise ValueError("不能汇总空批次")
    ids = [r["request_id"] for r in records]
    if len(set(ids)) != len(ids):
        raise ValueError("批次 request_id 不能重复")
    per_request, pooled_itl, ttfts, tpots, e2els, queues = [], [], [], [], [], []
    success_count = 0
    successful_tokens = 0
    for r in records:
        enqueue = _finite(r["enqueue_monotonic_s"], "enqueue")
        sent = r["send_start_monotonic_s"]
        if sent is None:
            if r["success"] or r.get("request_sent", True):
                raise ValueError("只有明确未发送的失败请求可以缺少 send_start")
            queue_end = _finite(r["worker_start_monotonic_s"], "worker_start")
        else:
            sent = _finite(sent, "send_start")
            queue_end = sent
        end = _finite(r["end_monotonic_s"], "end")
        if not window_start <= enqueue <= queue_end <= end <= window_end:
            raise ValueError("请求时间不在批次窗口内，或时间顺序错误")
        if type(r["success"]) is not bool:
            raise ValueError("success 必须是 bool")
        queue_ms = (queue_end - enqueue) * 1000
        queues.append(queue_ms)
        times = [_finite(event["time_monotonic_s"], "text_event")
                 for event in r.get("text_events", []) if event.get("text", "") != ""]
        if (times and sent is None) or any(t < sent or t > end for t in times) or times != sorted(times):
            raise ValueError("text 事件时间顺序错误")
        itls = [(b - a) * 1000 for a, b in zip(times, times[1:])]
        token_count = r.get("actual_output_tokens")
        metric = {"request_id": r["request_id"], "request_index": r.get("request_index"),
                  "success": r["success"], "queue_wait_ms": queue_ms,
                  "request_sent": r.get("request_sent", sent is not None),
                  "actual_output_tokens": token_count, "nonempty_text_events": len(times),
                  "ttft_ms": None, "e2el_ms": None, "tpot_ms": None,
                  "raw_itl_ms": itls, "raw_itl_distribution_ms": _distribution(itls)}
        if r.get("stream", True) and times:
            metric["ttft_ms"] = (times[0] - sent) * 1000
            metric["e2el_ms"] = (times[-1] - sent) * 1000
            if type(token_count) is int and token_count > 1:
                metric["tpot_ms"] = (times[-1] - times[0]) * 1000 / (token_count - 1)
        if r["success"]:
            _positive_int(token_count, "成功请求的 actual_output_tokens")
            success_count += 1
            successful_tokens += token_count
            if r.get("stream", True):
                if not times:
                    raise ValueError("成功流式请求不能缺少非空 text 事件")
                ttfts.append(metric["ttft_ms"])
                e2els.append(metric["e2el_ms"])
                if metric["tpot_ms"] is not None:
                    tpots.append(metric["tpot_ms"])
                pooled_itl.extend(itls)
        per_request.append(metric)
    window = window_end - window_start
    return {
        "schema_version": SCHEMA_VERSION, "exploratory": True,
        "percentile_method": "linear interpolation: rank=(n-1)*q",
        "tail_caveat": "P99 为本轮探索性观察，样本量见 count；不能声称稳定尾延迟或用于 SLO 承诺。",
        "window_start_monotonic_s": window_start, "window_end_monotonic_s": window_end,
        "window_seconds": window, "request_count": len(records),
        "success_count": success_count, "failure_count": len(records) - success_count,
        "successful_output_tokens": successful_tokens,
        "output_tokens_per_second": successful_tokens / window,
        "request_ttft_ms": _distribution(ttfts), "request_tpot_ms": _distribution(tpots),
        "request_e2el_ms": _distribution(e2els), "queue_wait_ms": _distribution(queues),
        "pooled_raw_itl_ms": _distribution(pooled_itl), "per_request_metrics": per_request,
        "metric_definitions": {
            "window": "批次开始至所有请求退出；包括客户端排队、失败请求和尾部收尾",
            "latency_population": "成功流式请求；失败请求的部分观测仍保留在 per_request_metrics",
            "queue_wait": "send_start-enqueue；未发送的过期请求用 worker_start-enqueue；全部请求独立报告",
            "ttft": "首个非空 text 事件-send_start，不含客户端队列等待",
            "e2el": "最后非空 text 事件-send_start，不含 usage 尾包和 [DONE] 等待",
            "tpot": "(最后非空 text-首个非空 text)/(实际生成 token 数-1)，单 token 为 null",
            "raw_itl": "相邻非空 text 消息间隔，不等于逐 token ITL；pooled 汇集所有成功请求的消息间隔",
            "throughput": "仅成功请求的实际生成 token 数/完整批次窗口秒数",
        },
    }


def run_batch(base_url, model, requests, max_concurrency, output_path, *, timeout=180,
              phase="measure", deadline_monotonic=None):
    """有限请求池在窗口起点一并排队，固定 worker 连续补位；每个完成请求立即 flush。

    output_path 使用独占创建，调用者应为每批选择新文件。返回的 summary 可通过
    JSONL 中的 records 与返回的两个窗口端点独立复算；不向 JSONL 混写 summary。
    deadline_monotonic 是可选的绝对 monotonic 总期限；到期中断已发送请求，
    队列中尚未发送的请求立即写失败记录。最终落盘及线程清理可略晚于此期限。
    """
    _endpoint(base_url)
    timeout = _timeout_value(timeout)
    if deadline_monotonic is not None:
        _finite(deadline_monotonic, "deadline_monotonic")
    _positive_int(max_concurrency, "max_concurrency")
    if max_concurrency > 16:
        raise ValueError("并发上限为 16")
    requests = list(requests)
    if not requests:
        raise ValueError("请求池不能为空")
    if not isinstance(phase, str) or not phase:
        raise ValueError("phase 必须是非空字符串")
    bodies = [_body(model, r, True) for r in requests]
    if len({r["request_id"] for r in requests}) != len(requests):
        raise ValueError("批次 request_id 不能重复")
    lock = threading.Lock()
    records = []
    with Path(output_path).open("x", encoding="utf-8") as output:
        window_start = time.monotonic()

        def worker(index):
            record = _perform(base_url, model, requests[index], timeout=timeout, stream=True,
                              index=index, enqueue=window_start, phase=phase, body=bodies[index],
                              deadline_monotonic=deadline_monotonic)
            line = json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n"
            with lock:
                output.write(line)
                output.flush()
                records.append(record)

        with ThreadPoolExecutor(max_workers=max_concurrency, thread_name_prefix="w4-u2") as pool:
            futures = [pool.submit(worker, index) for index in range(len(requests))]
            for future in futures:
                future.result()
        window_end = time.monotonic()
    summary = summarize(records, window_start, window_end)
    summary.update(phase=phase, max_concurrency=max_concurrency,
                   load_model="finite-pool closed-loop; all requests enqueued at window start",
                   raw_records_path=str(output_path))
    if deadline_monotonic is not None:
        summary["batch_deadline_monotonic_s"] = deadline_monotonic
    return summary
