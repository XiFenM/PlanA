# Repository Guidelines

## What This Repo Is

This is not a code project. It is an Obsidian-backed personal knowledge vault for AI Infra interview preparation and long-term notes. Work here is mostly reading, writing, and editing Chinese Markdown. Keep English only for proper nouns such as `FlashAttention`, `PagedAttention`, framework names, paper titles, and CLI/tool names.

`README.md` is the canonical entry point and owns the top-level resource subscription list (`§5`). When `README.md` and a module's `学习指引.md §长期订阅` disagree, `README.md` wins.

There is no application build, dependency install, or automated test suite.

## Project Structure

- `计划/` is the planning control plane: `主计划.md`, `进度总表.md`, `周更流程.md`, `月底晋级评审.md`, `陪学流程.md`, `学习断点.md`, and weekly reports in `计划/周报/YYYY-Wxx.md`.
- Core study modules live at the top level: `推理框架/`, `Pytorch/`, `训练框架与分布式/`, `并行计算编程/`, `模型理论/`, `Leetcode/`, `编译器/`, and `TPUs/`.
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
- Preserve relative Markdown links so the Obsidian graph remains portable.
- Preserve priority icons `🟥`, `🟨`, `🟩` and status icons `⬜`, `🟡`, `✅`, `⏭`, `🔖`. Do not introduce new status symbols unless the registry explicitly changes.
- Keep curriculum IDs stable. Insert new resources with suffixes such as `19a` or `19b`; never renumber existing rows.
- Convert relative dates to absolute dates when writing persistent notes, for example write `2026-05-10` instead of `本周日`.
- Do not add English translations alongside Chinese content unless explicitly asked.

## Planning Control Plane

- `计划/主计划.md` is the 20-week schedule and weekly cadence. Do not modify it during routine work.
- `计划/进度总表.md` is the global dashboard. It is normally updated on Sunday or during approved SOP flows.
- `计划/周更流程.md` is the weekly resource update SOP.
- `计划/月底晋级评审.md` is the month-end promotion review SOP.
- `计划/周报/YYYY-Wxx.md` files are append-only history. Do not edit a past weekly report after the next week starts, except for status annotations during month-end review.
- `计划/陪学流程.md` defines the daily study-companion workflow.
- `计划/学习断点.md` is the global resume cursor. It is safe to overwrite only inside the study-companion workflow.

## Weekly Resource Update SOP

Trigger phrase: `请严格按 计划/周更流程.md 的规范，为本周执行一次全板块资料周更。`

When this is requested:

- Read `计划/周更流程.md` before acting.
- Create exactly one new weekly report: `计划/周报/YYYY-Wxx.md`, using `date +"%G-W%V"` for the ISO week.
- Research the trailing 7 days from subscription sources and arXiv keywords, then dedupe against existing `学习指引.md` files and historical weekly reports.
- End the report with 3-5 `晋级候选` entries.
- Do not touch any `学习指引.md` or `进度.md`. Weekly update only collects candidates; promotion happens at month end.

## Month-End Promotion Review SOP

Trigger phrase: `请严格按 计划/月底晋级评审.md 的规范，对本月（YYYY-MM）做一次晋级评审。`

When this is requested:

- Read `计划/月底晋级评审.md` before acting.
- Use only the `晋级候选` sections of that month's weekly reports. Do not re-search the web.
- Score each candidate with the SOP's 5-question rubric. Promote only items with at least 3 yes answers.
- For each promoted item, update the target `{module}/学习指引.md`, its top `## Changelog`, `{module}/进度.md` if the promoted item is `🟥`, the source weekly report status annotation, and one monthly summary line in `计划/进度总表.md`.
- Use letter-suffix IDs such as `19a`; never renumber existing rows.
- For replacements such as `EAGLE-2 -> EAGLE-3`, keep the old ID position and annotate it with `（替代自 ...，YYYY-MM-DD）`; never delete the old entry.
- Never edit `计划/主计划.md`, `计划/周更流程.md`, `计划/月底晋级评审.md`, or non-current weekly reports in this flow.

## English Track And Coach Mode

`英语/` is a daily 60-75 minute parallel track that extends to W22. Its audio material is produced by the sibling tool repo `../blog-voice`, not this vault. When work involves article cadence, topic selection, or generating listening audio, use `../blog-voice` and anchor on one new AI Infra article every 2-3 weeks.

For the standalone daily-card task, when asked to read `英语/log/day-NN.md` and build Markji cards:

- Read `英语/review-workflow.md` and `英语/cards/_templates.md` first.
- Follow `review-workflow.md` Step 3.
- Write the Markji table-import TSV to `英语/cards/day-NN.md`.
- Data rows stay plain text; styling lives in the templates.

English coach mode is active when the user writes in English or when the interaction is technical learning/discussion. It is not active for pure Chinese vault-maintenance or mechanical SOP commands unless the user explicitly asks for feedback.

When active:

- Answer first as a senior AI Infra technical peer.
- End with concise English feedback in the format defined by `英语/ai-chat-prompt.md`.
- If feedback is produced, also append it to today's `英语/log/day-NN.md`, then regenerate that day's `英语/cards/day-NN.md` from the full log.
- Read and follow `英语/review-workflow.md`, `英语/cards/_templates.md`, `英语/references/markji-content-syntax.md`, and `英语/references/markji-table-import.md` before generating cards.
- Skip persistence for `/skip`, `/shadow`, and `/quiz` ephemeral interactions.

## Study-Companion Mode

Study-companion mode is active from `开始学习` / `继续学习` / `今天学什么` until `收工` / `结束学习`. It is for mainline study modules, not weekly updates, month-end review, README maintenance, or pure card-building.

When active:

- Read `计划/陪学流程.md` and `计划/学习断点.md` first.
- Also read `计划/进度总表.md` and `计划/主计划.md §1` for cadence, read-only.
- Lead the user through the current article/topic with the loop `讲 -> 问 -> 派 -> 盯`, asking before explaining and producing learning artifacts such as restatements, examples, summaries, or self-tests.
- Stay faithful to the source order. Do not jump ahead or ask the user to draft the final article paragraph during micro-actions.
- Respect controls: `/暂停`, `/继续`, `/卡住`, `/快`, `/状态`, `/成文`.

On `收工`, follow the three-stage persistence contract:

- Stage A: update only the touched module's `进度.md` with used hours, allowed status icon, and an absolute-date log line. Show the diff and wait for user approval before writing. Sunday only, also append one line to `计划/进度总表.md`.
- Stage B: overwrite `计划/学习断点.md` with the current resume cursor and clear the pause snapshot.
- Stage C: the user drafts article prose from the learning artifacts; review it. `/成文` can run the full assemble-and-polish pass.

Hard boundaries in study-companion mode: never touch `计划/主计划.md`, `计划/周更流程.md`, `计划/月底晋级评审.md`, any `学习指引.md`, or `计划/周报/*`.

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

- Do not edit `.obsidian/`.
- Do not reformat or tidy stable curriculum files opportunistically.
- Do not auto-promote weekly-report items to `学习指引.md`.
- Do not create planning, decision, or summary Markdown files unless explicitly asked.
- Do not alter SOP files during routine execution.
- Do not move assets away from the notes that reference them.
