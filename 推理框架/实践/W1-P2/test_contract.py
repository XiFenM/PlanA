"""导师维护的 P2 验收。B1 预测、B2 诊断和 B4 解释另行 Review。

先提交运行前预测，再运行对应的诊断或学习者用例。
默认父进程库路径为 B；运行后变式使用 P2_PARENT_LIBRARY=A。

从 PlanA 根目录执行：
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
    推理框架/实践/W1-P2/test_contract.py
"""

import os

import pytest

from harness import APP, LAUNCH, LIB_A, LIB_B, LIB_NAME, child_environment, probe, record, run


def test_fixture_elf_and_symbols():
    """只检查导师 fixture 是否符合实验设计。"""
    dynamic = run(["readelf", "-d", APP])
    assert f"Shared library: [{LIB_NAME}]" in dynamic
    assert "(RPATH)" not in dynamic and "(RUNPATH)" not in dynamic
    assert "BIND_NOW" not in dynamic
    symbols_a = run(["nm", "-D", "--defined-only", "-C", LIB_A / LIB_NAME])
    symbols_b = run(["nm", "-D", "--defined-only", "-C", LIB_B / LIB_NAME])
    assert "compute(int)" in symbols_a and "compute(int)" not in symbols_b
    assert "compute(double)" in symbols_b
    for path in (LIB_A, LIB_B):
        assert f"Library soname: [{LIB_NAME}]" in run(["readelf", "-d", path / LIB_NAME])
    # 只对本次自建可信 app 使用 ldd，固定查询的进程环境。
    assert str(LIB_A / LIB_NAME) in run(["ldd", APP], env=child_environment("A"))
    assert str(LIB_B / LIB_NAME) in run(["ldd", APP], env=child_environment("B"))


def test_fixture_runtime_contrast():
    """导师预核验成功基线和可重复故障，不计为学习者 B1/B2 证据。"""
    good = probe("A")
    faulty = probe("B")
    assert good["returncode"] == 0
    assert "RESULT 14\n" in good["stdout"]
    assert good["mapped_library_paths"] == [str(LIB_A / LIB_NAME)]
    assert faulty["returncode"] != 0
    assert "symbol lookup error" in faulty["stderr"]
    assert "_Z7computei" in faulty["stderr"]
    assert "RESULT 14" not in faulty["stdout"]
    assert faulty["mapped_library_paths"] == [str(LIB_B / LIB_NAME)]
    record("fixture_preflight", {
        "owner": "agent", "status": "passed",
        "scope": "导师确认实验可用；不是学习者的预测、诊断或修复结果",
        "successful_call_verified": True, "repeatable_symbol_failure_verified": True,
    })


def test_b3_learner_launcher_selects_library_and_calls_compute():
    if not LAUNCH.exists():
        pytest.skip("学习者尚未提交 launch.sh；跳过不表示 P2 通过")
    parent_library = os.getenv("P2_PARENT_LIBRARY", "B")
    assert parent_library in ("A", "B")
    observation = probe(parent_library, learner=True)
    record(f"learner_run_parent_{parent_library}", {"status": "observed", **observation})
    assert observation["mapped_library_paths"] == [str(LIB_A / LIB_NAME)]
    assert observation["returncode"] == 0
    assert "RESULT 14\n" in observation["stdout"]
    assert observation["stderr"] == ""
    record(f"learner_run_parent_{parent_library}", {"status": "passed", **observation})
