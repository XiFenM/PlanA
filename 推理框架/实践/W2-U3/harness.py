#!/usr/bin/env python3
"""W2-U3-P1 的导师运行入口；只编译同目录的 test_slot.cpp 与 slot.hpp。

python3 harness.py --setup --list
python3 harness.py --case normal_producer_first --prediction "运行前的预测"
python3 harness.py --asan --case all --prediction "运行前的预测"

--setup 的记录仅用于导师搭建；其他运行也不会自动成为学习者实证。
ASan 检查本次执行中的内存错误，不证明不存在数据竞争或死锁。
故障 fixture 不属于本入口，须在学习者另行给出预测后处理。
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid


ROOT = Path(__file__).resolve().parent
CASE_TIMEOUT_SECONDS = 8
COMPILE_TIMEOUT_SECONDS = 60
SCHEMA = "plana.w2-u3.harness-results/v1"
CASE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\Z")
TODO_MARKER = re.compile(r"TODO:\s*SingleSlot::")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def kill_group(pid: int, sig: signal.Signals) -> None:
    try:
        os.killpg(pid, sig)
    except ProcessLookupError:
        pass


def execute(
    command: list[str],
    cwd: Path,
    timeout: int,
    log_path: Path,
    environment: dict[str, str] | None = None,
) -> dict:
    """每个命令使用自己的 session；超时/中断时清理整个进程组。"""
    started_at = utc_now()
    start = time.monotonic()
    child = None
    stdout = ""
    stderr = ""
    timed_out = False
    interrupted = False
    launch_error = None
    returncode = None
    try:
        child = subprocess.Popen(
            command,
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=True,
        )
        try:
            stdout, stderr = child.communicate(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            timed_out = isinstance(error, subprocess.TimeoutExpired)
            interrupted = isinstance(error, KeyboardInterrupt)
            kill_group(child.pid, signal.SIGTERM)
            try:
                stdout, stderr = child.communicate(timeout=0.25)
            except subprocess.TimeoutExpired:
                kill_group(child.pid, signal.SIGKILL)
                stdout, stderr = child.communicate()
        returncode = child.returncode
    except OSError as error:
        launch_error = f"{type(error).__name__}: {error}"
    finally:
        if child is not None:
            # 正常退出也不允许该例留下继承同一进程组的子进程。
            kill_group(child.pid, signal.SIGKILL)
            if child.poll() is None:
                child.wait()

    result = {
        "command": command,
        "command_display": shlex.join(command),
        "cwd": str(cwd),
        "started_at": started_at,
        "finished_at": utc_now(),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "timeout_seconds": timeout,
        "timed_out": timed_out,
        "interrupted": interrupted,
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
        "launch_error": launch_error,
        "environment_overrides": (
            {"ASAN_OPTIONS": environment["ASAN_OPTIONS"]}
            if environment is not None and "ASAN_OPTIONS" in environment
            else {}
        ),
        "log": str(log_path.relative_to(ROOT)),
    }
    log_path.write_text(
        json.dumps(
            {key: value for key, value in result.items() if key not in ("stdout", "stderr")},
            ensure_ascii=False,
            indent=2,
        )
        + "\n\n--- stdout ---\n"
        + stdout
        + "\n--- stderr ---\n"
        + stderr,
        encoding="utf-8",
    )
    return result


def classify(result: dict) -> str:
    if result["timed_out"]:
        return "timeout"
    if result["returncode"] != 0 and TODO_MARKER.search(
        result["stdout"] + "\n" + result["stderr"]
    ):
        return "unimplemented"
    if (
        result["returncode"] == 0
        and not result["launch_error"]
        and not result["interrupted"]
        and re.search(r"(?m)^PASS(?:\s|$)", result["stdout"])
        and not re.search(r"(?m)^FAIL(?:\s|$)", result["stdout"])
    ):
        return "passed"
    return "fail"


class Record:
    def __init__(self, args: argparse.Namespace):
        self.artifacts = ROOT / "artifacts"
        self.artifacts.mkdir(exist_ok=True)
        self.lock_file = (self.artifacts / ".results.lock.log").open("a")
        try:
            fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock_file.close()
            raise RuntimeError("本目录已有 harness 正在运行；请等它结束后再运行。")
        self.path = ROOT / "results.json"
        if self.path.exists():
            try:
                self.document = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise RuntimeError(f"现有 results.json 无法读取，未覆盖：{error}")
            if (
                not isinstance(self.document, dict)
                or self.document.get("schema") != SCHEMA
                or not isinstance(self.document.get("runs"), list)
            ):
                raise RuntimeError("现有 results.json 格式不匹配，未覆盖。")
        else:
            self.document = {"schema": SCHEMA, "runs": []}
        self.run_id = (
            datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
            + "-"
            + uuid.uuid4().hex[:8]
        )
        has_prediction = args.prediction is not None and bool(args.prediction.strip())
        if args.setup:
            evidence_status = "teacher_setup_not_learner_evidence"
        elif not has_prediction:
            evidence_status = "debug_run_missing_pre_run_prediction"
        else:
            evidence_status = "prediction_recorded_pending_human_review"
        self.run = {
            "run_id": self.run_id,
            "exercise": "W2-U3-P1",
            "contract_revision": 1,
            "started_at": utc_now(),
            "status": "pending",
            "requested_case": args.case,
            "list_only": args.list,
            "asan": args.asan,
            "setup": args.setup,
            "prediction": args.prediction,
            "prediction_recorded_at": utc_now() if args.prediction is not None else None,
            "evidence_status": evidence_status,
            "automatic_mastery_assessment": False,
            "evidence_limits": [
                "预测、运行和结果解释需由导师结合实际帮助范围评审；本脚本不自动认定实证。",
                "ASan 没有报错不证明所有线程交错都无数据竞争或死锁。",
                "每例超时只表示未在 hangguard 内完成收尾，不是性能门槛。",
            ],
            "tools": {"python": sys.version, "python_executable": sys.executable},
            "source_files": {},
            "available_cases": [],
            "cases": [],
            "exit_code": None,
        }
        self.document["runs"].append(self.run)
        self.document["latest_run_id"] = self.run_id
        # 在任何版本查询、编译或测试进程之前持久化预测原文。
        self.save()
        (self.artifacts / f"{self.run_id}-prediction.log").write_text(
            json.dumps(
                {
                    "run_id": self.run_id,
                    "setup": args.setup,
                    "prediction": args.prediction,
                    "recorded_at": self.run["prediction_recorded_at"],
                    "evidence_status": evidence_status,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def save(self) -> None:
        # 临时记录也留在已约定的 artifacts/*.log 范围；同文件系统原子替换。
        staging = self.artifacts / f".{self.run_id}-results-staging.log"
        with staging.open("w", encoding="utf-8") as stream:
            json.dump(self.document, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        staging.replace(self.path)

    def command(
        self,
        stage: str,
        command: list[str],
        cwd: Path,
        timeout: int,
        environment: dict[str, str] | None = None,
    ) -> dict:
        self.run["active_stage"] = stage
        self.save()
        return execute(
            command,
            cwd,
            timeout,
            self.artifacts / f"{self.run_id}-{stage}.log",
            environment,
        )

    def finish(self, status: str, exit_code: int, error: str | None = None) -> int:
        self.run["status"] = status
        self.run["exit_code"] = exit_code
        self.run["finished_at"] = utc_now()
        self.run.pop("active_stage", None)
        if error:
            self.run["error"] = error
        self.save()
        return exit_code

    def close(self) -> None:
        self.lock_file.close()


def command_ok(result: dict) -> bool:
    return (
        result["returncode"] == 0
        and not result["timed_out"]
        and not result["interrupted"]
        and result["launch_error"] is None
    )


def run(args: argparse.Namespace, record: Record) -> int:
    snapshots = {}
    for name in ("harness.py", "test_slot.cpp", "slot.hpp"):
        path = ROOT / name
        if not path.is_file():
            return record.finish("compile_error", 2, f"缺少同目录文件：{name}")
        snapshots[name] = path.read_bytes()
        record.run["source_files"][name] = {
            "path": str(path),
            "sha256": sha256(snapshots[name]),
            "bytes": len(snapshots[name]),
        }
    record.save()

    compiler = shutil.which("g++")
    if compiler is None:
        return record.finish("compile_error", 2, "没有找到 g++；未安装或下载工具。")
    version = record.command("compiler-version", [compiler, "--version"], ROOT, 8)
    record.run["tools"]["compiler_version"] = version
    record.save()
    if not command_ok(version):
        return record.finish(
            "compile_error", 130 if version["interrupted"] else 2, "无法查询编译器版本。"
        )
    numeric = record.command(
        "compiler-numeric-version", [compiler, "-dumpfullversion"], ROOT, 8
    )
    record.run["tools"]["compiler_numeric_version"] = numeric
    record.save()
    if not command_ok(numeric):
        return record.finish(
            "compile_error", 130 if numeric["interrupted"] else 2, "无法确认编译器版本。"
        )
    if not re.fullmatch(r"13\.3(?:\.\d+)?", numeric["stdout"].strip()):
        return record.finish(
            "compile_error",
            2,
            f"本练习固定 GCC 13.3，实际为 {numeric['stdout'].strip()!r}；未更换工具链。",
        )

    with tempfile.TemporaryDirectory(prefix="plana-w2-u3-", dir="/tmp") as temporary:
        build = Path(temporary)
        record.run["build_directory"] = str(build)
        # 编译精确的源码快照，避免编辑器在编译期间修改文件导致 SHA 与输入不符。
        for name in ("test_slot.cpp", "slot.hpp"):
            (build / name).write_bytes(snapshots[name])
        executable = build / "test_slot"
        command = [compiler, "-std=c++20", "-pthread", "-O1", "-g"]
        if args.asan:
            command.extend(["-fsanitize=address", "-fno-omit-frame-pointer"])
        command.extend([str(build / "test_slot.cpp"), "-o", str(executable)])
        compilation = record.command("compile", command, build, COMPILE_TIMEOUT_SECONDS)
        record.run["compilation"] = compilation
        record.save()
        if not command_ok(compilation):
            print("compile_error：请查看编译日志。", file=sys.stderr)
            return record.finish("compile_error", 130 if compilation["interrupted"] else 2)

        environment = os.environ.copy()
        if args.asan:
            environment["ASAN_OPTIONS"] = "detect_leaks=0"
        discovery = record.command(
            "list", [str(executable), "--list"], build, CASE_TIMEOUT_SECONDS, environment
        )
        record.run["discovery"] = discovery
        record.save()
        if not command_ok(discovery):
            return record.finish(
                "timeout" if discovery["timed_out"] else "fail",
                130 if discovery["interrupted"] else 2,
                "测试程序 --list 未正常完成；没有执行用例。",
            )
        names = [line.strip() for line in discovery["stdout"].splitlines() if line.strip()]
        if (
            not names
            or len(names) != len(set(names))
            or any(CASE_NAME.fullmatch(name) is None for name in names)
        ):
            return record.finish("fail", 2, "--list 必须逐行返回互不重复的有效用例名称。")
        record.run["available_cases"] = names
        record.save()
        if args.list:
            print("\n".join(names))
            return record.finish("listed", 0)
        if args.case != "all" and args.case not in names:
            return record.finish(
                "fail", 2, f"未知用例 {args.case!r}；有效名称见 --list 或使用 all。"
            )
        selected = names if args.case == "all" else [args.case]
        for index, name in enumerate(selected, 1):
            result = record.command(
                f"case-{index:02d}-{name}",
                [str(executable), "--case", name],
                build,
                CASE_TIMEOUT_SECONDS,
                environment,
            )
            result["name"] = name
            result["status"] = classify(result)
            if result["returncode"] == 2 or result["launch_error"]:
                result["failure_kind"] = "test_environment_or_argument_error"
            record.run["cases"].append(result)
            record.save()
            print(f"{name}: {result['status']}", flush=True)
            if result["interrupted"]:
                return record.finish("fail", 130, "运行被中断，已清理该例进程组。")

        statuses = {case["status"] for case in record.run["cases"]}
        status = next(
            (value for value in ("timeout", "fail", "unimplemented") if value in statuses),
            "passed",
        )
        environment_error = any(
            case.get("failure_kind") == "test_environment_or_argument_error"
            for case in record.run["cases"]
        )
        exit_code = 2 if environment_error else (0 if status == "passed" else 1)
        return record.finish(status, exit_code)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="all", help="单例名称或 all（默认）；名称由测试程序提供")
    parser.add_argument("--asan", action="store_true", help="使用 AddressSanitizer 构建和运行")
    parser.add_argument("--list", action="store_true", help="编译后列出用例，不执行用例")
    parser.add_argument("--prediction", help="原样记录运行前预测；未提供时记录为 null")
    parser.add_argument("--setup", action="store_true", help="导师搭建检查，不计学习者证据")
    args = parser.parse_args()
    if args.list and args.case != "all":
        parser.error("--list 与指定单例不能同时使用。")
    if os.name != "posix":
        print("本入口需要 POSIX 进程组；未安装或更换运行环境。", file=sys.stderr)
        return 2
    record = None
    try:
        record = Record(args)
        result = run(args, record)
        if record.run.get("error"):
            print(record.run["error"], file=sys.stderr)
        return result
    except KeyboardInterrupt:
        if record is not None:
            return record.finish("fail", 130, "运行被中断。")
        return 130
    except (OSError, RuntimeError) as error:
        print(f"harness error: {error}", file=sys.stderr)
        if record is not None:
            return record.finish("fail", 2, str(error))
        return 2
    finally:
        if record is not None:
            print(
                f"记录：{record.path}；run_id={record.run_id}；"
                f"{record.run['evidence_status']}",
                file=sys.stderr,
            )
            record.close()


if __name__ == "__main__":
    raise SystemExit(main())
