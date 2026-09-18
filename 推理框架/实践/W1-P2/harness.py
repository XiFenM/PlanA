"""导师维护的 P2 构建、进程观察与证据工具。

在 PlanA 根目录使用 .venv/bin/python 调用本文件：
  harness.py build                 构建并记录环境
  harness.py observe B             观察指定运行环境，回车才调用 compute
  harness.py observe-launch B      观察学习者 launch.sh，B 为父进程库路径

启动脚本可读取 P2_APP、P2_LIB_A、P2_LIB_B 三个实验路径变量。
只需启动指定 app；stdin 中的 call 由本工具发送。
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import time
from contextlib import contextmanager

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BUILD = REPO.parent / "plana-w1-env/p2-build"
APP = BUILD / "app"
LIB_A = BUILD / "lib-a"
LIB_B = BUILD / "lib-b"
LIB_NAME = "libw1probe.so"
RESULTS = HERE / "results.json"
LAUNCH = HERE / "launch.sh"


def run(command, **kwargs):
    return subprocess.run(
        list(map(str, command)), check=True, text=True,
        capture_output=True, timeout=30, **kwargs
    ).stdout


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(key, value):
    results = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    results[key] = value
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")


def child_environment(library):
    env = os.environ.copy()
    # 固定本实验的装载条件，清除可能干扰诊断的父进程加载器变量。
    for key in ("LD_LIBRARY_PATH", "LD_PRELOAD", "LD_AUDIT", "LD_BIND_NOW"):
        env.pop(key, None)
    env.update({
        "LD_LIBRARY_PATH": str({"A": LIB_A, "B": LIB_B}[library]),
        "P2_APP": str(APP),
        "P2_LIB_A": str(LIB_A),
        "P2_LIB_B": str(LIB_B),
        "LC_ALL": "C",
    })
    return env


def build():
    LIB_A.mkdir(parents=True, exist_ok=True)
    LIB_B.mkdir(parents=True, exist_ok=True)
    fixture = HERE / "fixture"
    common = ["g++", "-std=c++17", "-O0", "-g", "-Wall", "-Wextra"]
    commands = []
    for variant, target in ((1, LIB_A), (2, LIB_B)):
        commands.append(common + [
            "-fPIC", "-shared", f"-DP2_VARIANT={variant}",
            str(fixture / "library.cpp"), f"-Wl,-soname,{LIB_NAME}",
            "-o", str(target / LIB_NAME),
        ])
    commands.append(common + [
        "-fplt", str(fixture / "driver.cpp"), f"-L{LIB_A}",
        "-lw1probe", "-Wl,-z,lazy", "-o", str(APP),
    ])
    for command in commands:
        run(command)
    artifacts = [APP, LIB_A / LIB_NAME, LIB_B / LIB_NAME]
    result = {
        "scope": "导师自建实验工件，编译成功不代表学习者实践通过",
        "os": run(["uname", "-srmo"]).strip(),
        "versions": {tool: run([tool, "--version"]).splitlines()[0]
                     for tool in ("g++", "ld", "readelf", "nm", "ldd")},
        "commands": commands,
        "source_sha256": {p.name: sha256(p) for p in sorted(fixture.iterdir())},
        "artifacts": {str(p): sha256(p) for p in artifacts},
        "binding": "函数调用采用 lazy binding；未写入 RPATH/RUNPATH",
    }
    record("build", result)
    return result


def read_ready(process):
    deadline = time.monotonic() + 8
    lines = []
    with selectors.DefaultSelector() as selector:
        selector.register(process.stdout, selectors.EVENT_READ)
        while time.monotonic() < deadline:
            events = selector.select(max(0, deadline - time.monotonic()))
            if not events:
                break
            line = process.stdout.readline()
            if not line:
                _, stderr = process.communicate(timeout=2)
                raise RuntimeError(f"未到达 READY：{''.join(lines)}{stderr}")
            lines.append(line)
            match = re.fullmatch(r"READY pid=(\d+)\n", line)
            if match:
                return int(match.group(1)), "".join(lines)
    raise TimeoutError("实验进程未在 8 秒内到达 READY")


@contextmanager
def started(command, environment):
    process = subprocess.Popen(
        list(map(str, command)), cwd=REPO, env=environment,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1, start_new_session=True,
    )
    try:
        pid, ready = read_ready(process)
        yield process, pid, ready
    finally:
        # 仅清理由本工具创建的独立进程组，包括启动脚本的子进程。
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)
        for stream in (process.stdin, process.stdout, process.stderr):
            stream.close()


def inspect_process(pid):
    executable = Path(f"/proc/{pid}/exe").resolve()
    assert executable == APP.resolve(), f"目标 PID 并非实验 app：{executable}"
    maps = Path(f"/proc/{pid}/maps").read_text().splitlines()
    library_lines = [line for line in maps if LIB_NAME in line]
    return {
        "pid": pid,
        "executable": str(executable),
        "library_maps_before_call": library_lines,
        "mapped_library_paths": sorted({line.split(maxsplit=5)[5]
                                        for line in library_lines}),
    }


def probe(library, *, learner=False, interactive=False):
    if not APP.is_file():
        raise RuntimeError("请先运行 harness.py build")
    env = child_environment(library)
    command = ["bash", LAUNCH] if learner else [APP]
    with started(command, env) as (process, pid, ready):
        snapshot = inspect_process(pid)
        if interactive:
            print(f"目标 app 的 PID：{pid}", flush=True)
            print("程序已到达 READY，尚未调用 compute。可在另一终端检查 /proc/PID/maps。",
                  flush=True)
            input("检查完成后回车，向程序发送 call：")
        stdout, stderr = process.communicate(input="call\n", timeout=8)
        observation = {
            "command": list(map(str, command)),
            "parent_library": library,
            "parent_LD_LIBRARY_PATH": env["LD_LIBRARY_PATH"],
            **snapshot,
            "stdout": ready + stdout,
            "stderr": stderr,
            "returncode": process.returncode,
            "app_sha256": sha256(APP),
            "launch_sha256": sha256(LAUNCH) if learner else None,
        }
    return observation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "observe", "observe-launch"])
    parser.add_argument("library", nargs="?", choices=["A", "B"], default="B")
    args = parser.parse_args()
    if args.action == "build":
        data = build()
        print(f"构建完成：{APP}；编译命令已记录到 results.json")
    else:
        learner = args.action == "observe-launch"
        data = probe(args.library, learner=learner, interactive=True)
        record("learner_observation" if learner else "diagnostic_observation", data)
        print(json.dumps(data, ensure_ascii=False, indent=2))
