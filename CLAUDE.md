# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Not a code project. This is an Obsidian-backed personal knowledge vault used by an AI Infra engineer (PyTorch PrivateUse1 backend + custom NCCL on a non-NV accelerator) for a 5-month / 20-week interview sprint plus long-term notes. All content is Chinese Markdown; English is preserved for proper nouns (FlashAttention, PagedAttention, etc.). There is no build system, no tests, and no code to run — your work is reading, writing, and editing Markdown.

The README (`README.md`) is the canonical entry point and source-of-truth for the resource subscription list (`§5`). When the README and a module's `学习指引.md §长期订阅` disagree, README wins.

## The 8 study modules

Each lives in its own top-level dir (Chinese names) and **always contains exactly two anchor files**:

- `学习指引.md` — stable curriculum: graded resource list (🟥 必读 / 🟨 选读 / 🟩 背景), long-term subscriptions, self-test bank. Edited only at month-end review.
- `进度.md` — progress tracker: 📊 summary table + per-section rows. Updated daily, every 0.5h of study.

Modules: `推理框架/` `Pytorch/` `训练框架与分布式/` `并行计算编程/` `模型理论/` `Leetcode/` `编译器/` `TPUs/`. Module dirs may also accumulate ad-hoc `.md` files (paper notes, retros, kernel demos) over time — that's expected; only the two anchor files are mandatory.

## The 计划/ control plane

`计划/` is the planning hub and contains files you should treat as load-bearing:

- `主计划.md` — 20-week schedule + weekly cadence (32.5h/week). **Never modify** during routine work; quarterly-level edits only.
- `进度总表.md` — global dashboard (Gantt + module rollup + checkpoints). Updated weekly on Sunday.
- `周更流程.md` — SOP for the weekly resource update. See below.
- `月底晋级评审.md` — SOP for the month-end promotion review. See below.
- `周报/YYYY-Wxx.md` — one per ISO week. Append-only history; never edited after the next week starts (except for status annotations during month-end review).

## The two SOPs you will be asked to run

These are the two recurring tasks the user invokes by saying "请严格按 `计划/X.md` 的规范…". Read the SOP file first — they are precise and have hard rules.

### Weekly resource update — `计划/周更流程.md`

- Trigger phrase: "请严格按 `计划/周更流程.md` 的规范，为本周执行一次全板块资料周更。"
- Output: **one** new file `计划/周报/YYYY-Wxx.md` (use `date +"%G-W%V"` for the week number).
- Approach: spawn 2–3 `general-purpose` agents in parallel (split modules per §4 Step 2), each does WebFetch on subscription sources + WebSearch on arXiv keywords for the trailing 7 days, returns candidates in the §5 single-entry format. Main Claude dedupes against existing `学习指引.md` files and historical 周报, then writes the report and lists 3–5 §晋级候选 at the end.
- **Hard rule**: this flow **must not** touch any `学习指引.md` or `进度.md`. Promotion is human-decided at month-end.

### Month-end promotion review — `计划/月底晋级评审.md`

- Trigger phrase: "请严格按 `计划/月底晋级评审.md` 的规范，对本月（YYYY-MM）做一次晋级评审。"
- Input: only the §晋级候选 sections of this month's 周报 — **do not** re-search the web in this flow.
- Each candidate scored on the 5-question rubric (§3); ≥3 yes ⇒ promote.
- Edit set per promotion: target `{module}/学习指引.md` (insert with letter-suffix IDs like `19a`, never renumber existing rows), top-of-file `## Changelog` (one line), `{module}/进度.md` if the promoted item is 🟥, the source 周报 (append `> **状态**：✅/❌/⏸ …` annotation), and `计划/进度总表.md` 月度复盘日志 (one summary line). **Never edit** `主计划.md`, `周更流程.md`, `月底晋级评审.md`, or non-current 周报.
- Replacements (e.g. EAGLE-2 → EAGLE-3): keep the old ID position with a `（替代自 …，YYYY-MM-DD）` annotation. Never delete old entries.

## Conventions to preserve

- **Resource grading and status icons**: 🟥/🟨/🟩 (priority) and ⬜/🟡/✅/⏭/🔖 (status). Don't introduce new symbols; the README §4 table is the registry.
- **ID stability**: numeric IDs in `学习指引.md` are referenced by `进度.md` and 周报 cross-links. Insert with `19a`, `19b` suffixes; never renumber.
- **Cross-references use relative paths** (e.g. `[../面试准备/projects.md]`) so the Obsidian graph stays intact. Preserve them when moving files.
- **Date format**: convert relative dates to absolute (`本周日` → `2026-05-10`) when writing into files that will be re-read months later. Today's date is available in the harness context.
- **CJK filenames**: many files have Chinese names with no ASCII fallback. When using Bash, quote them (`"Job Description"`, `"训练框架与分布式"`).
- **`.obsidian/`** is the vault config; don't edit it. `.gitignore` already excludes the workspace state files inside it.

## Things to avoid

- Don't auto-promote weekly-report items to `学习指引.md` — that breaks the SOP separation.
- Don't reformat or "tidy" stable curriculum files; their layout (especially the per-section tables in `进度.md`) is referenced by the SOPs.
- Don't create planning/decision/summary `.md` files unless the user explicitly asks — work from conversation context. The repo already has its own structure for retros (per-module dirs) and weekly reports (`周报/`).
- Don't add English translations alongside Chinese content unless asked.
