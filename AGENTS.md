# Repository Guidelines

## What This Repo Is

This is not a code project. It is a Markdown personal knowledge vault for AI Infra interview preparation and long-term notes. Work here is mostly reading, writing, and editing Chinese Markdown. Keep English only for proper nouns such as `FlashAttention`, `PagedAttention`, framework names, paper titles, and CLI/tool names.

`README.md` is the canonical entry point and owns the top-level resource subscription list (`§5`). When `README.md` and a module's `学习指引.md §长期订阅` disagree, `README.md` wins.

There is no application build, dependency install, or automated test suite.

## Project Structure

- `计划/` is the planning control plane: `主计划.md`, `进度总表.md`, `周更流程.md`, `月底晋级评审.md`, `陪学流程.md`, `学习断点.md`, and weekly reports in `计划/周报/YYYY-Wxx.md`.
- Core study modules live at the top level: `推理框架/`, `PyTorch/`, `训练框架与分布式/`, `并行计算编程/`, `模型理论/`, `Leetcode/`, `编译器/`, and `TPUs/`.
- Each core module must keep two anchor files: `学习指引.md` for stable curriculum and `进度.md` for progress tracking. Extra ad-hoc Markdown notes in module directories are expected.
- `英语/` is a 22-week parallel listening/speaking sub-track. It has `学习指引.md`, `进度.md`, `review-workflow.md`, `ai-chat-prompt.md`, plus `log/`, `cards/`, and `references/`.
- `面试准备/` holds interview materials. `Job Description/` stores role descriptions by direction.
- Assets should stay near the notes that reference them, for example `TPUs/pointwise-product.gif`.

## Common Commands

- `rg --files` lists repository content quickly.
- `git status --short` checks local changes before editing.
- `git diff --check` catches trailing whitespace and obvious patch formatting issues.
- `date +"%G-W%V"` returns the ISO week identifier used for weekly reports.

Quote CJK paths in shell commands, for example `"训练框架与分布式/进度.md"` or `"计划/周更流程.md"`.

## Markdown Conventions

- Use Chinese Markdown for repository content.
- Preserve relative Markdown links so the vault remains portable.
- Preserve priority icons `🟥`, `🟨`, `🟩` and status icons `⬜`, `🟡`, `✅`, `⏭`, `🔖`. Do not introduce new status symbols unless the registry explicitly changes.
- Keep curriculum IDs stable. Insert new resources with suffixes such as `19a` or `19b`; never renumber existing rows.
- Convert relative dates to absolute dates when writing persistent notes, for example write `2026-05-10` instead of `本周日`.
- Do not add English translations alongside Chinese content unless explicitly asked.

## Planning Control Plane

- `计划/主计划.md` is the 20-week schedule and weekly cadence. Do not modify it during routine work.
- `计划/进度总表.md` is the global dashboard. It is normally updated on Sunday or during approved SOP flows.
- `计划/周更流程.md` is the weekly resource update SOP, run via `.claude/skills/resource-planning/SKILL.md`.
- `计划/月底晋级评审.md` is the month-end promotion review SOP, run via the same skill.
- `计划/周报/YYYY-Wxx.md` files are append-only history. Do not edit a past weekly report after the next week starts, except for status annotations during month-end review.
- `计划/陪学流程.md` defines the daily study-companion workflow, run via `.claude/skills/study-companion/SKILL.md`.
- `计划/学习断点.md` is the global resume cursor. It is safe to overwrite only inside the study-companion workflow.

## Recurring Workflows Are Skills

The five recurring workflows are defined under `.claude/skills/`; `.agents/skills/` is a complete discovery mirror. Treat `.claude/skills/` as canonical, update both trees together, and verify them with `diff -qr .claude/skills .agents/skills`. Each `SKILL.md` holds the operative rules (trigger, roles, persist contract, hard rules) and points to the vault SOP doc for full detail. If your tool does not auto-discover skills, read the relevant `SKILL.md` before acting:

- `.claude/skills/study-companion/SKILL.md` — daily study-execution loop. Active from `开始学习` / `继续学习` / `今天学什么` until `收工` / `结束学习`. Full SOP: `计划/陪学流程.md`.
- `.claude/skills/english-coach/SKILL.md` — two modes: the primary 英语回顾 post-study mock dialogue over the day's `{module}/log/` study record, and ambient turn-end English feedback during English or technical discussion; both persist to `英语/log/` and that day's cards. Full prompt: `英语/ai-chat-prompt.md`; flow: `英语/review-workflow.md`.
- `.claude/skills/memo-cards/SKILL.md` — Markji table-import TSV card building; accepts English daily logs (`英语/log/day-NN.md` → `英语/cards/day-NN.md`) and technical Q&A material (article 〔面试问题Q&A〕 or `{module}/log/` study records → `{module}/cards/`).
- `.claude/skills/study-log/SKILL.md` — extract Claude Code or Codex session transcripts via the bundled script, filter the technical-learning turns, and write a structured study record to `{module}/log/`.
- `.claude/skills/resource-planning/SKILL.md` — dual mode: weekly resource update (`计划/周更流程.md`) and month-end promotion review (`计划/月底晋级评审.md`).

Cross-skill rules: english-coach is scope-triggered (English or engineer-to-engineer content), and stays off for pure-Chinese mechanical vault maintenance; during study sessions in English, english-coach owns turn-end feedback while study-companion owns the session ritual — never both.

## English Track Notes

`英语/` is a daily 60-75 minute parallel track that extends to W22. Its audio material is produced by the sibling tool repo `../blog-voice`, not this vault. When work involves article cadence, topic selection, or generating listening audio, use `../blog-voice` and anchor on one new AI Infra article every 2-3 weeks.

## Validation

Validation is review-based:

- Inspect Markdown-sensitive changes after editing.
- Run `git diff --check`.
- Confirm links are relative.
- For SOP work, verify that only the files allowed by the SOP changed.

## Commit And PR Guidance

Recent history uses short descriptive Chinese commits, plus occasional automated backup commits such as `vault backup: YYYY-MM-DD HH:MM:SS`. Prefer concise, specific summaries, for example `新增推理框架周报候选条目`.

Pull requests should state the purpose, list touched modules or SOPs, and call out any changed weekly report, curriculum, or progress tracker. Link related issues when available. Include screenshots only for visual assets or Markdown rendering changes where layout matters.

## Things To Avoid

- Do not reintroduce `.obsidian/`; Obsidian is no longer used for this vault.
- Do not reformat or tidy stable curriculum files opportunistically.
- Do not auto-promote weekly-report items to `学习指引.md`.
- Do not create planning, decision, or summary Markdown files unless explicitly asked.
- Do not alter SOP files during routine execution.
- Do not move assets away from the notes that reference them.
