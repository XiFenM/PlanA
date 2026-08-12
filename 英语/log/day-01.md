# 学习日志 · Day 01 — 2026-05-25 周一

> 记录性质：`legacy-derived` 学习记录。内容来自早期 AI 英语反馈，场景是在 blog-voice 项目中用英文讨论 verify / split-text 流程。
> 来源限制：原始 Anki Cloze 文件 `../anki-grammar-feedback-2026-05-25.tsv` 未随仓库存档，也没有保留可核验的 provider、会话或消息边界；下列原表达沿用历史记录，本次迁移不补造来源标识。
> 交接边界：本文件只保存历史学习过程。若要制成墨墨卡片，须由用户明确要求后再交给 `memo-cards` 预览和发布；不会因整理日志而自动制卡或导入。

## 冠词（a / the）

- [纠错] 场景：描述“在验证阶段，模型提出修复”。我写“in verifying phase” → 正确：`in the verifying phase`；工程语境中更常见 `in the verification phase`。原因：这里指流程中的特定单数阶段，不能省略限定词。
- [纠错] 场景：描述“如果这份转写里有错就修”。我写“fix the mistake in transcription” → 正确：`fix the mistake in the transcription`。原因：该语境指当时正在讨论的特定转写。
- [纠错] 场景：描述“可以直接 push 到 main 分支”。我写“push directly to main branch” → 正确：`push directly to main` 或 `push directly to the main branch`。原因：`main` 可直接作分支名；写完整的单数名词短语 `main branch` 时需要限定词。
- [纠错] 场景：描述 Issue #171。我写“Issue #171 is actually error” → 正确：`Issue #171 is actually an error`。原因：可数单数 `error` 需要冠词，且以元音音素开头时用 `an`。

## 动词形态 / 时态

- [纠错] 场景：描述“如果 LLM 认为有错，它就修”。我写“if LLM think there is a mistake” → 正确：`if the LLM thinks there is a mistake`。原因：单数第三人称主语在一般现在时使用 `thinks`；这里也需要限定具体的 LLM。
- [纠错] 场景：描述“句子被切成了两段”。我写“the sentence was splited” → 正确：`the sentence was split into two parts`。原因：`split` 的原形、过去式和过去分词相同，没有 `splited`。
- [纠错] 场景：描述一条通用规则“如果转写错了就修”。我写“fix it if it was wrong” → 正确：`fix it if it is wrong`。原因：在该通用规则语境中使用一般现在时；若明确回顾过去事件，`was` 才可能成立。

## 副词语序

- [要点] `actually` 在 be 动词附近怎样放更自然？——中性表达通常写 `Issue #171 is actually a splitting error`；`actually is` 也可以成立，但更像刻意强调“确实是”，不能一概判错。
- [要点] `directly` 必须放在实义动词后吗？——`to push directly to main` 节奏更中性；`to directly push to main` 也是合乎语法的 split infinitive，可用于强调“直接 push”，二者是语气差异而非正误差异。

## 单复数

- [纠错] 场景：描述“使用另外两个 reference”。我写“use the other two reference” → 正确：`use the other two references`。原因：`two` 后接复数名词。

## 介词

- [纠错] 场景：描述“我在 Fish Audio 网站上试了这些缩写”。我写“in the Fish Audio website” → 正确：`on the Fish Audio website`。原因：表达在网站或网页上进行操作时通常用 `on`。
- [要点] 怎样更自然地表达“重跑这句的 TTS”？——若 TTS 指生成操作，可说 `rerun TTS for this sentence` 或 `rerun TTS on this sentence`。原来的 `rerun the TTS of this sentence` 可以理解，但更像把 TTS 当作该句已有的输出，不是严格的语法错误。

## 选词

- [纠错] 场景：我想表达“这些词的读音都对了”，写成“I got the correct voice for all of them” → 正确：`I got the pronunciation right for all of them`；若强调 TTS 输出，也可说 `They were all pronounced correctly`。原因：`pronunciation` 指词怎么读，`voice` 指说话者或音色，原词会改变意思。
- [纠错] 场景：列举最后一点“最后，verifier 还应该修文本”。我使用 `At last` → 正确：使用 `Finally` 或 `Lastly`。原因：`Finally / Lastly` 标记列表末项；`At last` 通常表达久等之后“终于”的如释重负感。

## 拼写

- [纠错] 场景：项目讨论中拼写 `verifying`。我写“verifing” → 正确：`verifying`。原因：`verify` 变为 `-ing` 形式时是 `verifying`。
- [纠错] 场景：项目讨论中拼写 `reference`。我写“refernece” → 正确：`reference`。原因：历史记录中间字母顺序写反。
- [纠错] 场景：项目讨论中拼写 `repository`。我写“respository” → 正确：`repository`。原因：`repository` 中没有该处多出的 `s`。
