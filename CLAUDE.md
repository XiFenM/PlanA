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

## The 英语/ parallel track (listening + speaking)

`英语/` is a **22-week parallel sub-track** (like `Leetcode/`, it doesn't occupy mainline weeks — it's a daily 60–75 min block running the whole sprint, extending 2 weeks past it to W22). It uses the same two anchor files (`学习指引.md` stable plan + `进度.md` tracker), plus extra files specific to language practice:

- `学习指引.md` — the 5-phase plan: baseline-test SOP, daily time blocks, 4 practice SOPs (美剧 / 口语课 / AI Infra listening / mini-talk recording), Anki/Markji card templates, phase-by-phase detail, subscriptions.
- `进度.md` — weekly 打卡 table, monthly comparison, phase checkpoints, 偷懒红线, daily log.
- `review-workflow.md` — the 4-step spaced-repetition flow (踩坑 → daily log → 墨墨记忆卡 TSV). `ai-chat-prompt.md` — the AI-coach system prompt. `log/` (daily logs), `cards/` (Markji TSV cards), `references/` (podcast list, advice docs, Markji syntax).

**Audio teaching material is produced by the sibling tool repo `../blog-voice`** (a TTS CLI), not by this vault. The English plan is its downstream consumer. When the user mentions article cadence / topic selection / generating listening audio, that work happens in `../blog-voice` (`uv run blog-voice article ...`); anchor on "one new AI Infra article per 2–3 weeks".

## Skills（功能路由）

The recurring workflows live as skills under `.claude/skills/`. Each SKILL.md holds the operative rules (triggers, roles, persist contracts, hard rules) and points to its vault SOP doc for full detail — the vault docs stay the human-readable source of truth; the skills are the agent-facing layer. Route by trigger and invoke the skill:

| Trigger | Skill |
|---|---|
| `开始学习` / `继续学习` / `今天学什么` … until `收工` / `结束学习` | `study-companion` — daily study-execution loop: resume cursor, 讲→问→派→盯, three-stage persist, `/成文`. Controls: `/暂停 /继续 /卡住 /快 /状态 /成文` |
| 英语回顾 / "用英语回顾今天学的" (primary venue, post-study); or the user writes in English / technical discussion (ambient) | `english-coach` — 英语回顾 mock-dialogue over the day's study record, plus turn-end English feedback; persists to `英语/log/` and that day's cards. Controls: `/skip /deep /中文 /shadow /quiz` |
| 制卡 / "读 `英语/log/day-NN.md` … 整理成墨墨表格，写到 `英语/cards/day-NN.md`" / turning article 〔面试问题Q&A〕 or 学习记录 into cards | `memo-cards` — Markji table-import TSV; accepts English daily logs and technical Q&A material |
| 整理学习记录 / 提取对话记录 / 把今天的学习对话存档 | `study-log` — extract Claude Code transcripts (bundled script), filter the technical-learning turns, write a structured 学习记录 to `{module}/log/` (process-side material for `memo-cards`) |
| "请严格按 `计划/周更流程.md` 的规范，为本周执行一次全板块资料周更。" | `resource-planning` (周更 mode) |
| "请严格按 `计划/月底晋级评审.md` 的规范，对本月（YYYY-MM）做一次晋级评审。" | `resource-planning` (月底评审 mode) |

How the skills chain into the full study pipeline (each arrow is an explicit handoff written into the skills):

```
resource-planning(周更→周报晋级候选 →月底评审→学习指引) ──选定资料──▶ study-companion(断点续接→讲问派盯→收尾三Stage)
                                                                        │
                                              ┌─────────────────────────┼──────────────────────┐
                                              ▼                         ▼                      ▼
                                    文章 {module}/…/N-*.md    study-log → {module}/log/ ─▶ english-coach → 英语/log/
                                    （学习的结果，含面试Q&A）  （学习的过程，要点/纠错）   （「英语回顾」以学习记录为素材；常驻反馈为辅）
                                              └───────────┬─────────────┘                      │
                                                          ▼                                    ▼
                                              memo-cards → {module}/cards/          memo-cards → 英语/cards/
                                                          └────────── 墨墨导入，间隔重复复习 ──────┘
```

Two ambient rules that live here because they're cross-skill:

- **english-coach has two entry points**: the primary venue is the post-study 英语回顾 session (phrase-triggered, offered at study-companion wrap-up); the ambient turn-end feedback is retained opportunistically — load it whenever the turn is in English or is engineer-to-engineer technical content, but it stays off for pure-Chinese mechanical vault maintenance (weekly update, month-end review, card building, README/`进度.md` edits) — don't interrupt those with feedback.
- **Coexistence**: for English-track study or English messages during a study session, english-coach owns the turn-end feedback slot and study-companion only drives the session ritual — never both append feedback (English wins feedback, 陪学 wins the ritual).

## The 计划/ control plane

`计划/` is the planning hub and contains files you should treat as load-bearing:

- `主计划.md` — 20-week schedule + weekly cadence (32.5h/week). **Never modify** during routine work; quarterly-level edits only.
- `进度总表.md` — global dashboard (Gantt + module rollup + checkpoints). Updated weekly on Sunday.
- `周更流程.md` — SOP for the weekly resource update. Run via the `resource-planning` skill.
- `月底晋级评审.md` — SOP for the month-end promotion review. Run via the `resource-planning` skill.
- `周报/YYYY-Wxx.md` — one per ISO week. Append-only history; never edited after the next week starts (except for status annotations during month-end review).
- `陪学流程.md` — SOP for the daily AI study-companion workflow. Run via the `study-companion` skill.
- `文章模版.md` — the 8-part article template study sessions produce drafts against.
- `学习断点.md` — the single global "resume cursor" the companion reads at session start and overwrites at wrap-up; not SOP-referenced, so safe to overwrite freely.

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
