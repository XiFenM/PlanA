# 学习日志 · Day 06 — 2026-08-10 周一

> 记录性质：`legacy-derived` 表达记录。来源说明仅保留为“AI 教练对话（Codex，讨论 vLLM 请求规范化与进程边界）”；接管前文件没有可核验的学习者原句、会话 ID 或稳定消息边界，因此以下内容只代表历史提炼结果，不作为原话或完整过程证据，本次迁移不补造来源标识。
> 交接边界：这些表达只有在用户明确要求、并经定向复核后，才可作为 `memo-cards` 的主动产出候选；不能据此生成纠错卡，也不会自动接管现有 legacy 卡片。

- [要点] 怎样表达“将 API 请求归一化为统一的引擎请求”？——`normalize an API request into a canonical engine request`。
  - 场景：讨论跨层边界时把协议对象转换为稳定的内部表示。
  - 为什么：`normalize A into B` 适合强调多个外部表示收敛到一个统一内部表示；如果只是一般类型转换、不强调规范化，宜用 `convert`、`map` 或 `translate`。
- [要点] 怎样表达“某项状态仍由 API server 进程持有或负责”？——`remain owned by the API server process`。
  - 场景：区分连接与流式响应状态的所有权，以及跨进程传递的内部请求。
  - 为什么：`remain owned by` 强调所有权或生命周期责任没有随边界转移，不只是对象物理上“待在”某处。
