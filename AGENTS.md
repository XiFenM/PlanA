# Repository Guidelines

## Project Structure & Module Organization

This repository is an Obsidian-backed Markdown knowledge vault for AI Infra interview preparation and long-term notes. `README.md` is the canonical entry point and owns the top-level resource subscription list.

- `计划/` is the planning hub: `主计划.md`, `进度总表.md`, `周更流程.md`, `月底晋级评审.md`, and weekly reports in `计划/周报/YYYY-Wxx.md`.
- Core study modules live at the top level: `推理框架/`, `训练框架与分布式/`, `并行计算编程/`, `Pytorch/`, `模型理论/`, `Leetcode/`, `编译器/`, and `TPUs/`.
- `英语/` is a parallel listening/speaking sub-track (22 weeks, like `Leetcode/`); it keeps the same two anchor files plus `review-workflow.md`, `ai-chat-prompt.md`, and `log/ cards/ references/`. Its audio material is produced by the sibling tool repo `../blog-voice`.
- Each module should keep two anchor files: `学习指引.md` for stable curriculum and `进度.md` for progress tracking.
- `面试准备/` holds interview materials. `Job Description/` stores role descriptions by direction. Assets should stay near the notes that reference them, for example `TPUs/pointwise-product.gif`.

## Build, Test, and Development Commands

There is no application build, dependency install, or automated test suite.

- `rg --files` lists repository content quickly.
- `git status --short` checks local changes before editing.
- `git diff --check` catches trailing whitespace and obvious patch formatting issues.
- `date +"%G-W%V"` returns the ISO week identifier used for weekly reports.

## Coding Style & Naming Conventions

Write repository content in Chinese Markdown; keep English for proper nouns such as `FlashAttention`, `PagedAttention`, and framework names. Use relative Markdown links so Obsidian graph links remain portable. Quote CJK paths in shell commands, for example `"训练框架与分布式/进度.md"`.

Preserve existing priority and status symbols: `🟥`, `🟨`, `🟩`, `⬜`, `🟡`, `✅`, `⏭`, and `🔖`. Do not introduce new status icons. Keep curriculum IDs stable; insert new IDs with suffixes such as `19a` rather than renumbering existing rows.

## Testing Guidelines

Validation is review-based. After edits, inspect rendered Markdown-sensitive changes, run `git diff --check`, and confirm links use relative paths. For SOP work, verify that only the allowed files changed.

## Commit & Pull Request Guidelines

Recent history uses short descriptive commits in Chinese, plus occasional automated backup commits like `vault backup: YYYY-MM-DD HH:MM:SS`. Prefer concise, specific summaries, for example `新增推理框架周报候选条目`.

Pull requests should state the purpose, list touched modules or SOPs, and call out any changed weekly report, curriculum, or progress tracker. Link related issues when available. Include screenshots only for visual assets or Markdown rendering changes where layout matters.

## Agent-Specific Instructions

Read the relevant SOP before running weekly updates or month-end promotion reviews. Do not edit `.obsidian/`, do not reformat stable curriculum files opportunistically, and do not create extra planning documents unless explicitly requested.
