# 理想汽车面试 · Qwen 与 Hydrogen 逐项对照

Qwen 只收到 9 片音频，Hydrogen 独立收到整条音轨与复盘提示词。本表将 Hydrogen 的 6 个主题和两项反问映射回报告的 15 组问题。P 编号定位 Qwen 原文，L 编号定位对应原片中的短音频窗口。摘录属于两模型输出，角色与技术判断还要结合上下文。

| 题号 | 核查项 | 两路结果 | 判断与定位 |
| --- | --- | --- | --- |
| Q1 | 背景与团队人数 | 语义一致 | 两方均有估计语气。团队约十人，不能与公司规模混用。 [P002](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p002) · [L020](../transcripts/interview-li-auto-recording-01.local-indexed.md#l020) |
| Q1 | 办公地 | 证据不足 | Hydrogen 提出城市解读并标注存疑，Qwen 紧接雇主名称，缺少具体地点回答，不新增城市信息。 [P001](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p001) · [L018](../transcripts/interview-li-auto-recording-01.local-indexed.md#l018) |
| Q2 | 本人和算子团队的分工 | 语义一致 | 保留框架侧接入和 profiling 工作，不把全部算子实现归给候选人。 [P003](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p003) · [L025](../transcripts/interview-li-auto-recording-01.local-indexed.md#l025) |
| Q2 | 模型名称与接入工作 | 语义一致 | 本场项目名称优先按清晰的 Qwen 拼写；后续 KDA 与固定配置相容。 [P004](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p004) · [L027](../transcripts/interview-li-auto-recording-01.local-indexed.md#l027) |
| Q3 | 峰值算力 | 语义一致 | 单卡 64 GB 和峰值约 200 TFLOP/s 是自述。120–130 的精度和实测范围需记录。 [P004](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p004) · [L033](../transcripts/interview-li-auto-recording-01.local-indexed.md#l033) |
| Q3 | 访存带宽方向 | 语义一致 | 800–1000 G 是回答中的实测范围，峰值另报 1.6 T。 [P005](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p005) · [L039](../transcripts/interview-li-auto-recording-01.local-indexed.md#l039) |
| Q4 | decode 口径 | 语义一致 | 两个模型均保存面试官的口径确认。这个指标属于整套配置。 [P005](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p005) · [L040](../transcripts/interview-li-auto-recording-01.local-indexed.md#l040) |
| Q4 | 32K prefill 时延 | 证据不足 | 28 秒是候选读法，328 秒也不是稳定识别。64K 和 128K 的条件换算可单独进行。 [P006](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p006) · [L041](../transcripts/interview-li-auto-recording-01.local-indexed.md#l041) |
| Q4 | 输入吞吐追问 | 语义一致 | 现场没有报换算后的输入 tok/s。936 及 819–874 均是复盘演算。 [P007](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p007) · [L043](../transcripts/interview-li-auto-recording-01.local-indexed.md#l043) |
| Q5 | 因果卷积是一个步骤 | 语义一致 | 现场主动区分卷积和完整 KDA。清楚定义当前与历史位置能避免方向歧义。 [P010](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p010) · [L060](../transcripts/interview-li-auto-recording-01.local-indexed.md#l060) |
| Q6 | 卷积尾状态和递推矩阵 | 语义一致 | 中间态及前后相依得到支持。衰减和 delta 更新可作为后续准备。 [P012](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p012) · [L064](../transcripts/interview-li-auto-recording-01.local-indexed.md#l064) |
| Q6 | 分别说明状态精度 | 语义一致 | 此处前一段卷积尾状态报 FP32，递推状态报 BF16。精度表述须按语境区分后面的泛指。 [P013](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p013) · [L067](../transcripts/interview-li-auto-recording-01.local-indexed.md#l067) |
| Q7 | 拆池为什么可能更快 | 语义一致 | 同条件拷贝量和端到端收益未提供。不要把一个 view 操作本身视为必然拷贝。 [P015](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p015) · [L078](../transcripts/interview-li-auto-recording-01.local-indexed.md#l078) |
| Q7 | 递推矩阵的数字 | 文字分歧 | Qwen 重复写 18，Hydrogen 给 128。本地另一次识别出混合的 128 与 18；公开配置只能说明 128 相容，实际 shape、TP 与槽位需核实。 [P014](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p014) · [L073](../transcripts/interview-li-auto-recording-01.local-indexed.md#l073) |
| Q7 | 面试官要求概括 | 语义一致 | 适合把问题、改动、可测收益放在项目开场，而非据此推断面试官对人的评价。 [P015](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p015) · [L075](../transcripts/interview-li-auto-recording-01.local-indexed.md#l075) |
| Q8 | 自定义类名 | 候选补充 | 复用既有管理逻辑、修改分配这件事两路相容；类名仍用源码核查，不能认定精确类和接口。 [P017](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p017) · [L087](../transcripts/interview-li-auto-recording-01.local-indexed.md#l087) |
| Q8 | 固定插件基线 | 语义一致 | 最后重复读数相容，仅作为团队当时自述版本，不把对方提到的 0.34 当作今天的最新版。 [P019](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p019) · [L095](../transcripts/interview-li-auto-recording-01.local-indexed.md#l095) |
| Q9 | 后续优化与项目时期 | 语义一致 | MTP 和尝试 FP8 都是讨论中的后续方向，现场不支持写作已上线收益。 [P022](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p022) · [L106](../transcripts/interview-li-auto-recording-01.local-indexed.md#l106) |
| Q9 | 后面重述的缓存精度 | 文字分歧 | 这里比较的是 Qwen 后段泛称与 Hydrogen 对前段说明的归纳。P013 与本地原窗支持前段 BF16；P020 的 FP16 与本地 L102 有差别，不能跨句静默统一。 [P020](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p020) · [L102](../transcripts/interview-li-auto-recording-01.local-indexed.md#l102) |
| Q10 | 主仓与插件边界 | 语义一致 | 融合算子替换 modeling 片段可能涉及主仓；worker/runner/分配尽量在插件。具体 commit 未查证。 [P023](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p023) · [L114](../transcripts/interview-li-auto-recording-01.local-indexed.md#l114) |
| Q11 | 块表与非连续存储 | 语义一致 | 已说出核心映射。块表在 GPU 上的具体表示形式是额外实现细节。 [P024](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p024) · [L117](../transcripts/interview-li-auto-recording-01.local-indexed.md#l117) |
| Q12 | 4096 与尾块 | 语义一致 | 两份相对长上下文材料都保留 16/17，并支持按需增长。整除时无需额外尾块；是否想表达预留尚未确认。 [P027](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p027) · [L129](../transcripts/interview-li-auto-recording-01.local-indexed.md#l129) |
| Q12 | 前缀共享 | 语义一致 | 可以把共同前缀的复用与渐进分配分开讲；实际共享取决于实现及匹配条件。 [P028](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p028) · [L133](../transcripts/interview-li-auto-recording-01.local-indexed.md#l133) |
| Q13 | Conv3D 项目与框架 | 候选补充 | 多模态 32B 项目和 PyTorch 侧布局修改有多处支持；模型全名及具体 revision 仍待确认。 [P030](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p030) · [L143](../transcripts/interview-li-auto-recording-01.local-indexed.md#l143) |
| Q13 | 末维 3→128 | 语义一致 | 用重述确认通道对齐。42.67 仅是在其余条件相同下旧物理张量与紧凑张量的倍率，整体峰值待测。 [P031](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p031) · [L151](../transcripts/interview-li-auto-recording-01.local-indexed.md#l151) |
| Q13 | 精确五维原貌 | 证据不足 | P031 后续明确恢复五维。Hydrogen 在建议中补的具体 patch shape 与片上操作不计为现场回答。 [P030](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p030) · [L143](../transcripts/interview-li-auto-recording-01.local-indexed.md#l143) |
| Q14 | 成本数字的归属 | 语义一致 | 这是对方云端工作举例；负载和成本基准未知，不写成个人成果或公司的公开承诺。 [P033](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p033) · [L160](../transcripts/interview-li-auto-recording-01.local-indexed.md#l160) |
| Q14 | 云端推理术语 | 证据不足 | 多 batch 与 MTP 得到支持。中间技术名在各路识别中差异大，“chunked prefill”仅作待核候选。 [P034](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p034) · [L163](../transcripts/interview-li-auto-recording-01.local-indexed.md#l163) |
| Q15 | 主要框架专名 | 用户校正 | 用户在本次复盘中明确确认“框架名是SGLang”。正文据此采用 SGLang；保留 Qwen 原始误识。此项确认仅用于该名称。 [P034](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p034) · [L164](../transcripts/interview-li-auto-recording-01.local-indexed.md#l164) |
| Q15 | 收尾表态 | 语义一致 | 支持对方会讨论后反馈。末片计量差异仍在，不以告别文字推断全片准确率或面试结果。 [P035](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p035) · [L167](../transcripts/interview-li-auto-recording-01.local-indexed.md#l167) |

**仍需回听**。Qwen P014/P016/P018 与 Hydrogen 的状态矩阵数字不同。Qwen P013 的 BF16 与 P020 后续泛称的 FP16 要按句分别核查。P034 的主力框架名已经用户确认为 SGLang，不再列入待回听项。

全部 60 条短引文及字符位置见[结构化证据](interview-li-auto-recording-01.qwen-hydrogen-comparison.json)。[Qwen 转写索引](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md) · [Hydrogen 原始底稿](understand-li-auto-hydrogen-stream-20261119.audio.md)。
