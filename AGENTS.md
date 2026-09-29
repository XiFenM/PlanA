# Repository Guidelines

## What This Repo Is

这是面向 AI Infra 面试准备与长期学习的个人知识仓库，以中文 Markdown 为主，英文保留专有名词，例如 `FlashAttention`、`PagedAttention`、框架名、论文标题和 CLI/工具名。当前活动计划是八周证据冲刺，原 20 周计划冻结为长期候选排程。

`README.md` is the canonical human entry point. Its resource subscription list (`§5`) is a projection; `.agent-skills-config/resource-planning.json` owns machine source/query scope and the managed registry owns dynamic resource state.

仓库没有统一的应用构建或测试入口，但包含实践脚本、测试与上游源码；实践任务按对应目录和 Lesson 的约定运行。

## Project Structure

- `计划/` is the planning control plane: `主计划.md`, `进度总表.md`, `学习断点.md`, legacy reports in `计划/周报/`, and new managed resource state under `计划/资源治理/`. The two old SOP paths are retirement notices kept for historical links.
- `计划/八周冲刺进度/W1.md` through `W8.md` own the sprint's weekly completion, evidence, and remaining gaps. Detailed accepted contracts and stage history stay under `计划/八周冲刺进度/历史记录/`; technical artifacts stay in their module, and Claim-evidence / Case Card outputs stay in `面试准备/自我准备/`. The old EP-PD package path is a compatibility entry, not an active ledger.
- Core study modules live at the top level: `推理框架/`, `PyTorch/`, `训练框架与分布式/`, `并行计算编程/`, `模型理论/`, `Leetcode/`, `编译器/`, and `TPUs/`.
- 各核心模块保留 `学习指引.md` 与 `进度.md` 双锚文件，前者保存稳定课程，后者记录模块进度与用户确认的实际时长（归属规则见 `.agent-skills-config/guide-learning-profile.md` §2）。模块内可以另存专题 Markdown 笔记。
- `英语/` 保留 22 周长期听力与口语资料体系，当前投入服从活动计划。目录包含 `学习指引.md`、`进度.md`、`review-workflow.md` 及 `log/`、`cards/`、`references/`；中央 `english-coach` 拥有教学反馈行为，仓库不维护平行 prompt。
- `.agent-skills-config/guide-learning-profile.md` contains only PlanA's learner profile, state paths, single-writer ownership, duration attribution, domain lenses, and article adaptation. Central `guide-learning` owns teaching behavior.
- `面试准备/` holds interview materials. `Job Description/` stores role descriptions by direction.
- Assets should stay near the notes that reference them, for example `TPUs/pointwise-product.gif`.

## Common Commands

- `rg --files` lists repository content quickly.
- `git status --short` checks local changes before editing.
- `git diff --check` catches trailing whitespace and obvious patch formatting issues.
- `date +"%G-W%V"` returns the ISO week identifier used for weekly reports.

Quote CJK paths in shell commands, for example `"训练框架与分布式/进度.md"` or `"计划/资源治理/registry.json"`.

## Markdown Conventions

- Use Chinese Markdown for repository content.
- Preserve relative Markdown links so the vault remains portable.
- Preserve priority icons `🟥`, `🟨`, `🟩` and status icons `⬜`, `🟡`, `✅`, `⏭`, `🔖`. Do not introduce new status symbols unless the registry explicitly changes.
- Keep curriculum IDs stable. Insert new resources with suffixes such as `19a` or `19b`; never renumber existing rows.
- Convert relative dates to absolute dates when writing persistent notes, for example write `2026-05-10` instead of `本周日`.
- Do not add English translations alongside Chinese content unless explicitly asked.

## Planning Control Plane

- `计划/主计划.md` 是冻结的 20 周长期候选排程，32.5h/周属于历史预算，不裁决当前活动状态；日常工作不修改。
- [计划/高级AI框架开发工程师-八周证据冲刺计划.md](计划/高级AI框架开发工程师-八周证据冲刺计划.md) 拥有当前活动 Program 的目标、范围、预算与候选 Lesson；八个有效周不随日历自动推进。
- `计划/进度总表.md` 是全局派生视图，在周日或经批准的周期触点更新，不反向裁决活动状态，也不代替模块实际工时记录。
- `.agent-skills-config/resource-planning.json` is the static source/query, module, adapter, and storage fact source. `计划/资源治理/registry.json` becomes the sole dynamic resource fact source after the first confirmed refresh.
- `计划/周报/2026-W18.md`, `2026-W26.md`, and `2026-W32.md` are immutable legacy evidence. Never append status, rewrite links, infer cursors, or turn their Top lists into approved candidates.
- `计划/周更流程.md` and `计划/月底晋级评审.md` are retirement notices, not executable SOPs.
- `.agent-skills-config/guide-learning-profile.md` maps PlanA's learner profile, Program, Lesson, event, Checkpoint, duration, and domain facts without duplicating the central workflow. Record mappings are stable (the lesson mapping covers all of `计划/八周冲刺进度/`); the current lesson is pointed to only by `计划/学习断点.md`, so switching lessons never requires a config change.
- `计划/学习断点.md` is the single sparse Checkpoint. Overwrite it only at a semantic session boundary or durable recovery change.

## Central Agent Skills

The canonical Skill source is the pinned `.agent-skills` submodule. `.agent-skills.json` uses the version 2 consumer index to select six active Skills for both Codex and Claude; `.agent-skills-config/` contains Git-tracked public environment facts for all five learning Skills. `.agents/skills/` and `.claude/skills/` are ignored, materialized discovery views. Never edit either generated tree or copy a Skill back into this repository. Initialize and verify the pipeline with the commands documented in `README.md §2.2`.

Route work by intent:

- `guide-learning` — understanding-first teaching: depth ladder (mechanism → design rationale → real systems → boundaries → interview expression), checks that test understanding rather than computation, adaptive pacing, evidence-gap-driven practice, and three-place sparse state. PlanA facts and learner profile: `.agent-skills-config/guide-learning-profile.md`.
- `english-coach` — post-study English review and scoped turn-end English feedback. PlanA paths and handoffs: `英语/review-workflow.md`.
- `memo-cards` — managed Markdown plus one Markji XLSX per template, with optional official API upload, from English logs, technical Q&A, or structured study records. Per-batch soft targets apply to every new card.
- `study-log` — user-requested learning records inside the repository. Structured PlanA output stays under `{module}/log/` by default; a same-named visible-text archive under sibling `{module}/log-raw/` is produced only on explicit request. Raw content still needs privacy review and is not a card input; saving does not authorize Git stage, commit, push, or public disclosure. Existing hashed structured sources may remain unchanged during archive migration.
- `resource-planning` — managed research, light single-slot `adopt` edits of a module's `学习指引.md`, source refresh, claim-level evidence, candidate review, and exact slot-scoped curriculum edits. Configured scope is not network or write authorization. `adopt` previews one slot with `slot-edit` and applies after current confirmation; refresh and review prepare an exact transaction, obtain current confirmation, publish, then verify.
- `playwright-cli` — browser automation; it is a tool Skill, not part of the learning-state pipeline.

Cross-skill rules: broad resource governance stays with `resource-planning`; dialogue extraction stays with `study-log`; card generation stays with `memo-cards`. During English study, `english-coach` owns turn-end language feedback while `guide-learning` owns the learning flow. Articles, logs, cards, raw archives, and English review are explicit handoffs, never automatic wrap-up side effects.

Treat each generated `.agent-skills-context.json` as a materializer-owned locator and mechanical allowlist, not as action authorization. Public configuration never grants saving, overwriting, card generation, publishing, committing, or pushing. Configured log/card directories do not authorize scanning for inputs; a record the user names explicitly (including one study-log just produced) may be used whether or not it is Git-tracked, so never `git add` or re-materialize just to make a source usable.

## English Track Notes

原 20 周排程中的“英语每日 60–75 分钟、排除在总预算外”是冻结的历史口径；八周 Program 活动期间，英语投入计入[活动计划 §5](计划/高级AI框架开发工程师-八周证据冲刺计划.md#5-时间预算与周节奏)的每周预算。

英语音频教材由同级工具仓库 `../blog-voice` 生产。文章节奏、选题或听力音频生成在该工具仓库处理，以每 2–3 周一篇新 AI Infra 文章为基准。

## Validation

Validation is review-based:

- Inspect Markdown-sensitive changes after editing.
- Run `git diff --check`.
- Confirm links are relative.
- For resource work, verify exact transaction targets, old-report immutability, slot-scoped curriculum diffs, and registry-last publication.
- After changing Skill selection, run the central materializer and require `--check` to report current; do not compare or hand-maintain the two discovery trees.

## Commit And PR Guidance

Recent history uses short descriptive Chinese commits, plus occasional automated backup commits such as `vault backup: YYYY-MM-DD HH:MM:SS`. Prefer concise, specific summaries, for example `新增推理框架周报候选条目`.

Pull requests should state the purpose, list touched modules or SOPs, and call out any changed weekly report, curriculum, or progress tracker. Link related issues when available. Include screenshots only for visual assets or Markdown rendering changes where layout matters.

## Things To Avoid

- Do not reintroduce `.obsidian/`; Obsidian is no longer used for this vault.
- Do not switch branches in a shared checkout. Codex works in the sibling worktree `../PlanA-codex` on branch `codex`, while `../PlanA` stays on `main`; rebase `codex` onto `main` before starting, and ask the user to fast-forward `main` when the work is ready.
- Do not reformat or tidy stable curriculum files opportunistically.
- Do not auto-promote weekly-report items to `学习指引.md`.
- Do not create planning, decision, or summary Markdown files unless explicitly asked.
- Do not alter SOP files during routine execution.
- Do not move assets away from the notes that reference them.
