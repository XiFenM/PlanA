# 开源贡献（调研、计划与成果回传）

本目录是 `PlanA` 内关于开源贡献的**计划与归档窗口**，不在这里克隆上游代码、搭建编译环境或存放实验产物；所有实际代码开发、上游拉取与环境构建统一在同级独立仓库 `../oss-contrib` 中完成。

## 1. 职责与双仓分工

| 位置 | 唯一权威源 | 放什么 | 不放什么 |
|---|---|---|---|
| `PlanA/开源贡献/调研报告/` | **`PlanA`** | 定期 GitHub 实时核验报告、候选 issue/roadmap 筛选、硬件与竞争边界、阶段工作计划 | 上游源码、构建产物、临时调试日志 |
| `../oss-contrib/plans/` | 同步副本（只读） | 从 `PlanA/开源贡献/调研报告/` 单向同步过去的调研与计划 | 不在 `oss-contrib` 直接修改计划正文 |
| `../oss-contrib/tasks/` | **`oss-contrib`** | 进行中任务的工作区（复现脚本、源码笔记、PR 草稿、验证记录） | 不反向拷回 `PlanA` |
| `../oss-contrib/summaries/` | **`oss-contrib`** | 已完成或阶段收口任务的正式总结（PR 链接、改动范围、实测环境、边界与面试复述点） | 过程草稿 |
| `PlanA/开源贡献/成果总结/` | 同步副本（只读） | 从 `../oss-contrib/summaries/` 单向同步回来的成果总结，供简历、复盘与面试取材 | 不在 `PlanA` 手改覆盖原总结 |

与 [八周冲刺计划增强方案-AMD岗位.md](../计划/八周冲刺计划增强方案-AMD岗位.md#early-contribution) 的关系：
- 本目录承接冲刺期内的开源调研、选题和成果汇总，复用每周既定的开源时段，不另建第二套工时体系。
- 实际学习/开源工时仍只在经本人确认后记入对应模块 `进度.md`；开源调研与计划不自动等同于已完成贡献。

## 2. 定期双仓流转流程

1. **在 `PlanA` 做定期调研核验**：结合最新目标岗位（[目标岗位入口](../面试准备/目标岗位/README.md)）与硬件条件，重新核验 GitHub 实时状态，在 `调研报告/` 新增一份 `YYYY-MM-DD-开源贡献调研与工作计划.md`。
2. **同步计划到 `oss-contrib`**：在 `../oss-contrib` 运行同步脚本把最新报告拉入 `plans/`：
   ```bash
   python3 scripts/sync_with_plana.py pull-plans --dry-run
   python3 scripts/sync_with_plana.py pull-plans
   ```
3. **在 `oss-contrib` 执行开发与验证**：拉取上游仓库到 `upstream/`、搭独立环境、写复现/修复/单测并提交 PR；完成后按 `summaries/_template.md` 写一份 `summaries/YYYY-MM-DD-<repo>-<topic>.md`。
4. **回传总结到 `PlanA`**：在 `../oss-contrib` 运行同步脚本将总结同步回本目录的 `成果总结/`：
   ```bash
   python3 scripts/sync_with_plana.py push-summaries --dry-run
   python3 scripts/sync_with_plana.py push-summaries
   ```

## 3. 调研报告索引

| 日期 | 报告 | 核心覆盖 | 状态 |
|---|---|---|---|
| 2026-11-26 | [2026-11-26 开源贡献调研与工作计划](调研报告/2026-11-26-开源贡献调研与工作计划.md) | 复核 2026-11-09 旧候选；覆盖 Qualcomm（AIMET / QEFF）、AMD（MORI / rocm-aic / ATOM / Infera）、LMCache、SGLang-Omni、Arm（ExecuTorch / 避坑） | 当前活动基线 |

## 4. 已回传成果总结

详见 [成果总结/README.md](成果总结/README.md)（当前 0 项，随 `../oss-contrib` 完成并同步后更新）。
