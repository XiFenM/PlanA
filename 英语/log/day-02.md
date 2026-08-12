# 学习日志 · Day 02 — 2026-05-27 周三

> 记录性质：`legacy-derived` 学习记录。内容来自历史 AI 教练对话，主要记录当时主动表达受阻、工程沟通纠错和可复用表达。
> 来源限制：旧文件没有保留可核验的 provider、会话或消息边界；下列原表达和场景沿用历史记录，本次迁移不补造来源标识，也不把 AI 示例当成学习者原话或掌握证据。
> 交接边界：只有用户明确要求时，才把已核验条目交给 `memo-cards` 预览；整理日志、制卡和 Markji 导入互不自动触发。

## 主动表达受阻：解释复习流程

当时想法较多，不知道怎样用英语表达，先切换为中文说明。这次语言切换本身是过程证据：需要的是更小的表达支架，而不是默认获得完整翻译。

- [要点] 怎样表达“把这些想法用英语说出来”？——`put these ideas in English`；`put ... in English` 比较口语化。
- [要点] 怎样表达“我设想中的流程”？——`the workflow I have in mind`；`have in mind` 表示心里已有的设想。
- [要点] 怎样表达“值得记忆的东西”？——`something worth memorizing`；`worth` 后接动名词。
- [要点] 怎样表达“随手记下”？——`jot it down`；它比 `write it down` 更突出快速、非正式地记一笔。

### 历史可选 shadowing 参考

下面是旧记录保留的 AI 生成范本，只可在用户需要时作为跟读参考；它不是学习者原话、会话边界证据或掌握证据：

> I've got a lot of ideas here and I'm not sure how to **put** them **in English**, so let me explain in Chinese first. Here's the workflow I **have in mind**: ① **Spot the issue** — while I'm studying, I come across something **worth memorizing** that isn't just a plain vocab word. ② **Jot it down** — I (or you, the AI coach) log it in that day's notes, in loose, natural language rather than in a strict card format.

## 复现 benchmark 结果 / 找现成工具

- [纠错] 场景：表达“在四个 benchmark 上复现结果”。我写“reproduce the result of four datasets” → 正确：`reproduce results on four benchmarks`。原因：该历史场景讨论的是 benchmark，常用搭配是 `results on a benchmark`，多个结果和对象也应使用复数。
- [要点] 怎样简洁询问“有没有现成工具可以跑这些 benchmark”？——`I'm not sure if there are off-the-shelf tools I can use to run these benchmarks.` 原来的 `software packages or libraries` 可以理解，但 `off-the-shelf tools` 更集中地表达“现成可用”，不是单纯语法纠错。
- [要点] 怎样自然地请对方推荐工具？——`Can you point me to any tools that would work?`；`point someone to ...` 是工程协作中常见的请求表达。
- [要点] `off-the-shelf` 与什么概念相对？——它表示现成的、开箱即用的工具或方案，常与 `in-house` 对照，例如 `We built it in-house rather than using an off-the-shelf tool.`

## 带新人上手 CUDA / C++

- [纠错] 场景：表达“一个刚毕业的同事”。我写“fresh graduated colleague” → 正确：`a new-grad colleague` 或 `a colleague who just graduated`。原因：`fresh graduated` 不是英语中的正常搭配。
- [纠错] 场景：表达“他们懂一些基础，但不系统、不扎实”。我写“they know some basics, but not systematic and solid” → 正确：`They know some basics, but their foundation isn't solid` 或 `... but their knowledge isn't structured.` 原因：原句后半段缺少被形容的名词或完整谓语，含义关系不清。
- [要点] 怎样表达“给他们设计一条系统学习路径”？——`I want to put together a structured learning path for them.` 原来的 `give a systematic learning path for them` 能猜到含义，但 `put together` 更准确地表示设计和组织材料。
- [要点] 怎样表达“让新人快速达到可工作的理解程度”？——`get someone up to speed on ...`，也可说 `ramp someone up on ...`，例如 `get a new grad up to speed on CUDA and C++`。

## 口语中的随口确认

- [要点] 怎样随口确认“其他的都是免费的吧”？——轻松对话中可说 `The rest are free, right?` 或 `Everything else is free, right?`。历史原句 `Others are free, aren't they?` 在指代清楚时也合乎语法；前者只是更适合当时想要的随口确认语气，不能把 tag question 一概判为错误。
- [要点] 工程沟通中怎样用 `right?` 做低成本确认？——把它放在陈述句末，例如 `The KV cache lives in HBM, right?`。它便于对方直接确认或纠正，但在需要正式或精确确认时仍应完整提问。
