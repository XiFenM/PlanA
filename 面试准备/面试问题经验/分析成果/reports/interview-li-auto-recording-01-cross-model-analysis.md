# 理想汽车面试复盘 · Qwen 与 Hydrogen 对照版

**最值得准备的一道追问出现在约 17:42。** 你已经讲了卷积尾状态、递推矩阵和两类缓存池，面试官仍请你用几句话重新说明原有方案的问题、你改了什么、取得什么收益。你接下来给出的解释清楚得多：在分配时就形成算子所需的布局，可以省掉计算前的形状整理和连续化。录音里缺少的是能把这个改动与收益连起来的一组同条件数据。把后面这段回答提前，是这场面试最具体的改进机会。[回到 L074–L078](../transcripts/interview-li-auto-recording-01.local-indexed.md#l074)

这场面试从模型部署的实际数字开始，沿着线性注意力缓存追到插件改动，再用一个 4096-token 的算例检查你对 PagedAttention 的理解。末段是你主动补充的 Conv3D OOM 案例和对端云推理分工的反问。你能解释具体实现中的内存约束，尤其是历史状态、分块增长、设备末维对齐。面试官反复要求补全的是**测量对象、比较基线和本人改动的边界**。

- 记录 ID `interview-li-auto-recording-01`。报告日期 2026-11-19，公司名来自用户指定的文件。面试轮次、正式 JD、简历原文和结果未确认。
- 原视频长 41:02.666，音轨内容 41:02.613。本次提供给 Gemini 的完整 MP3 与 Qwen 的九个分片来自同一份归一化 PCM。Hydrogen 独立理解完整音频，未收到 Qwen 转写或旧报告。另有两套本地语音识别结果用于精确定位短音频窗口。[Qwen 转写索引](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md) · [Hydrogen 独立底稿](../analysis/understand-li-auto-hydrogen-stream-20261119.audio.md) · [本地时间索引](../transcripts/interview-li-auto-recording-01.local-indexed.md)
- 本文按 15 组问答组织，Hydrogen 将相同对话归为六个主题和两项反问。30 个对照点覆盖 21 项语义一致、4 项证据不足、2 项文字分歧、2 项候选补充，以及 1 项经用户校正的专名。[逐项对照](../analysis/interview-li-auto-recording-01.qwen-hydrogen-comparison.md) · [原文引用及字符区间](../analysis/interview-li-auto-recording-01.qwen-hydrogen-comparison.json)
- **用户校正**　反问环节提到的主力框架是 **SGLang**。Qwen 在 P034 写成 Hugging Face，Hydrogen 写成 SGLang，你在复盘中明确确认了这个名称。正文采用你的校正；P034 原样保留，便于追溯。
- 12 个抽样画面主要是会议窗口与本地笔记，技术答题依据来自对话。公司内部实现与性能仍属于现场自述。[画面核查](../analysis/interview-li-auto-recording-01.visual-evidence.md) · [技术核查与演算](../analysis/interview-li-auto-recording-01.technical-audit.md)

## 两路材料使哪些判断更清楚

| 核查项 | 对照与采用的结论 |
| --- | --- |
| 单请求 decode 与 prefill | 两路都保留了面试官专门确认 decode 的问答，16–17 tokens/s 的口径清楚。64K 约 70 s、128K 约 150–160 s 可以作条件换算。32K 的“3……28 秒”多路都带停顿，28 s 仍是候选读法。 |
| KDA 缓存的 dtype | 前段分别说明两种状态时，Qwen P012–P013、Hydrogen 与本地 L066–L067 支持“卷积尾部 FP32、递推矩阵 BF16”。后段畅谈未来 FP8 时，Qwen P020 又写成 FP16/FP32，本地 L102 更接近 BF16/FP32。初次分项说明的证据较清楚；后段原词和插件实际 dtype 需分开核实。 |
| 形状、层数和类名 | 对递推矩阵，Qwen 多次写成 `8×18×18`，Hydrogen 写成 `8×128×128`。官方配置的 64 heads、head dimension 128 说明后一组数字在特定分片条件下有可能，但不能证明当场原话或实际 TP。本模型配置有 **34 个 KDA 层**，上游配置也不能证明团队为全部状态分配了怎样的池。`Map Cache` / `MambaCache group` 只作类名候选。 |
| 页数与复用 | Qwen 和 Hydrogen 都记下先说“16 块”又提到“17 块”。结合本地原声窗口，初版中形似“116/117”的转写不宜照录成答题失误。数学边界明确，现场有没有特指额外预留仍待核实。 |
| Conv3D 的倍率 | Qwen 与 Hydrogen 都支持末维 **3→128** 这个重述。它支持特定张量在指定物理布局下的膨胀，当前没有端到端峰值数据。Hydrogen 举的完整五维 patch 示例和片上重构方式属于复盘建议，未作为你的现场实现或已验证成果。 |
| 端云与团队介绍 | “成本约官方的两到三折”属于面试官介绍其云端项目，比较基准未展开。可确认现有框架、社区回馈和多客户适配这些话题。对方提及的主力框架按你的校正写作 SGLang；中间部分技术简称及对方云端示例的型号仍不确定。 |

## 逐题复盘

| 原片窗口 | 面试官的问题与追问 | 你的实际回答、能支持的判断及待补证处 |
| --- | --- | --- |
| [Q1 · 03:17–05:11](../transcripts/interview-li-auto-recording-01.local-indexed.md#l015) · [P002](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p002) | 在哪家公司？公司、团队多大，组里负责什么？ | 先确认问的是公司还是组，再给出整公司约 200–300 人、团队约十人或略少的估计。组内做自研芯片上的训练/推理框架开发和模型适配。面试官介绍本场先聊背景与项目，再问框架问题，最后反问。 |
| [Q2 · 05:11–06:54](../transcripts/interview-li-auto-recording-01.local-indexed.md#l022) · [P003](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p003) | 你具体做什么，部署过哪个模型，性能到什么水平？ | 自述负责 PyTorch 与 vLLM 相关接入和推理优化，用 profiler、shape 分析和测试定位瓶颈，在框架侧改动，与算子同事合作。代表项目是 GLM-5.3-Flash 插件接入，第一次报单请求生成速率，后面又确认一次。模型名称按本场读音、后续 KDA 讨论整理。 |
| [Q3 · 06:54–09:27](../transcripts/interview-li-auto-recording-01.local-indexed.md#l029) · [P005](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p005) | 自研卡是否量产？单卡显存、算力、带宽多少？为什么带宽是范围，指哪条链路？ | 回答单卡 64 GB、已量产，峰值算力约 200 TFLOP/s，实际场景量级约 120–130。带宽先报实测约 800–1000 G，追问后补标称峰值 1.6 T，并说明指单卡显存到计算单元。你区分出了实测与标称；下次可一开始就给方向、单位、精度和测试负载。 |
| [Q4 · 09:27–11:23](../transcripts/interview-li-auto-recording-01.local-indexed.md#l040) · [P007](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p007) | 16–17 tokens/s 是 decode 吗？prefill 多快？和业界、硬件预期相比如何？ | 明确是**单请求 decode**。prefill 用多档上下文报耗时，面试官改问输入 tokens/s，你说明主要看时延、吞吐可以换算。你认为相对其他国产芯片表现偏低，但符合本代硬件和当时优化阶段的预期。没有同模型、精度、并发和卡数一致的对照，行业比较只能作为现场判断。 |
| [Q5 · 11:23–14:25](../transcripts/interview-li-auto-recording-01.local-indexed.md#l048) · [P010](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p010) | 模型里哪里用卷积？卷积和线性注意力是一回事吗？ | 你先讲 KDA 带来的缓存适配，再明确是一维因果卷积、窗口约四个 token，并澄清卷积是 KDA 的一个组成步骤。这是可保留的澄清。讲解时直接以当前位置 t 举例，能消除口语“从前往后看”带来的方向歧义。 |
| [Q6 · 14:25–16:33](../transcripts/interview-li-auto-recording-01.local-indexed.md#l061) · [P013](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p013) | 整个 KDA 能否简要概括？两类历史状态分别保存什么？ | 你提到 Q/K/V 的处理、递推状态 S、前一状态参与下一步，并从这里引出卷积缓存和递推矩阵。完整音频底稿与转写中，首次逐项说明都指向卷积尾部保留最近 3 个历史位置、FP32，递推矩阵对应 heads、K/V 维度、BF16。后续泛称有识别差异。这是本场口述，实际布局和 dtype 仍需插件配置。简述时可再讲清楚本步读什么、更新什么、输出什么。 |
| [Q7 · 16:33–20:58](../transcripts/interview-li-auto-recording-01.local-indexed.md#l069) · [P015](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p015) | 原有缓存池哪里慢？拆成什么形状？int8 是模型精度还是池的存储类型？是否只改配置即可？ | 你描述固定版本用一块平铺的字节存储承载不同状态，目标算子需要特定 dtype、shape 和连续布局；在你的后端，切分后整理数据耗时。方案是分配时拆成两类池，使算子直接消费。面试官要求概括后，你把“省掉算子前的转换”说了出来，并回答要改代码。尚待补充的是哪一步实际触发拷贝、省掉多少次/多少微秒，以及端到端改善。 |
| [Q8 · 20:58–24:19](../transcripts/interview-li-auto-recording-01.local-indexed.md#l087) · [P019](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p019) | 自定义部分具体实现了什么？常用模型为什么还要做这项适配？vLLM 是哪个版本？ | 回答大部分已有管理功能可复用，改的是分配阶段的两种状态、shape/dtype 和容量计算。团队固定上游版本开发硬件插件，频繁升级会带来集成冲突。两路都听到最后反复确认的 `v0.30.1`，对方提到另一个较新版本；Hydrogen 给出 `MambaCache` 的候选类名，Qwen 写成 `Map Cache`。版本与具体类以当时的提交和插件实现为准。面试官继续指出跑通还需要验证性能。 |
| [Q9 · 24:19–25:57](../transcripts/interview-li-auto-recording-01.local-indexed.md#l101) · [P022](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p022) | 还有哪些优化空间？为什么尚未支持 MTP、低精度缓存？你负责框架还是算子？ | 你提出 MTP 和尝试 FP8 缓存；补充自研硬件算子有开发周期，简历所述时间点尚未支持，面试时部分工作在推进。你明确自己的重心在框架。进一步答题时可对每项功能列出已接入的框架路径、仍需的 kernel 和正确性测试；录音不足以确认已经上线或得到收益。 |
| [Q10 · 25:57–28:00](../transcripts/interview-li-auto-recording-01.local-indexed.md#l108) · [P023](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p023) | 用插件接入时要改主框架吗？除了 modeling，还有哪些改动？ | 你举出用融合算子替换模型执行路径片段的场景，解释固定版本中有时需动主仓；其余尽量通过平台插件、自定义 worker、model runner、分配逻辑完成。一个具体文件或调用点就能进一步说明“主仓一处、插件一处、算子团队一处”各自负责的工作。 |
| [Q11 · 28:00–30:15](../transcripts/interview-li-auto-recording-01.local-indexed.md#l116) · [P025](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p025) | PagedAttention 的逻辑块和物理块如何组织？为什么节省空间？ | 你提到 KV 分块、block table、按 sequence 查物理块，单请求可以使用离散物理块。面试官因此进一步指定 4096 个 token，要求把“节省空间”讲成实例。这里已经有核心机制，缺的是把地址、容量与增量分配放在同一个例子里。 |
| [Q12 · 30:15–33:45](../transcripts/interview-li-auto-recording-01.local-indexed.md#l125) · [P027](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p027) | 输入 4096，分块前后各分多少？下一步如何扩容？page/block table 里面是什么？ | 你假设 block size=256，对比按最大生成长度预留连续区与尾块满后再增块，补充不同请求可按块复用共同前缀。结尾说清每个请求有对应的一组物理块号。口述块数有重复。Qwen、Hydrogen 与本地 Paraformer 均支持十六/十七的读法；仅凭 SenseVoice 的“116/117”不能判为算错。下文给出可以当场算清的边界。 |
| [Q13 · 33:45–37:44](../transcripts/interview-li-auto-recording-01.local-indexed.md#l139) · [P032](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p032) | 还有什么优化案例？Conv3D 省多少显存？只 pad 最后一维，怎么会到四十几倍？改在什么框架？ | 你主动讲到多模态 32B 模型适配时的 OOM，解释移通道到末维，再触发设备对齐；做法是展平多个尾部维度，让算子根据原元信息解释逻辑形状。追问中重述通道从 3 补到 128，最后把主要改动定位在 PyTorch 侧。Qwen 与 Hydrogen 都给出 Qwen3 32B VL 一类模型名候选。例子支持相关 tensor 的膨胀机制；实际 checkpoint、新物理 shape、整体峰值与 OOM 回归均缺少实现记录。 |
| [Q14 · 37:44–39:38](../transcripts/interview-li-auto-recording-01.local-indexed.md#l156) · [P033](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p033) | 你反问，理想也做云端大规模推理吗？端云工作的重点有什么不同？ | 对方按语义说明端侧交付和云端训练/推理都有，举部署开源模型的例子，提到“官方成本的两到三折”和社区贡献，也谈到端侧小 batch、融合与减少数据搬运。该成本数字属于面试官介绍，没有明确比较基线，不能计入你的项目履历。 |
| [Q15 · 39:38–41:02](../transcripts/interview-li-auto-recording-01.local-indexed.md#l164) · [P034](../transcripts/interview-li-auto-recording-01.qwen-asr-indexed.md#p034) | 你继续问主要用现有框架还是自研。 | 对方谈到基于已有框架做改动、适合的改动回贡献给社区、芯片客户有不同框架需求。你已确认**主力框架为 SGLang**。对方还表示支持 vLLM，提到客户需求与社区回馈；这部分属于面试官的口头介绍。最后表示团队会横向讨论并通知进展。 |

## 三个下次可以现场算给对方看的答案

**1. 把 prefill 和 decode 各放进一行数据。** 你已经能报出 16–17 个生成 token/s。换成单请求稳态步时约 59–63 ms/输出 token。对 64K 输入，若 K=1024、70 秒确是完整 prefill 耗时，则 `65,536 / 70 ≈ 936` 输入 tokens/s。对 128K、150–160 秒，同样假设下是约 **819–874** 输入 tokens/s。32K 那一行的两份转写不清楚，先回听再填。这样可以直接回答“多少 tokens/s”，同时给对方能复算的时延和计时区间。[回听性能原声](../../../../work/managed/interview-video-analysis/derived/li-auto-20261119-review-clips/prefill.mp3)

**2. 用 4096→4097 画出 block table。** 每块 256 个 token，4096 正好占满 16 块。第 4096 个 token 在逻辑块 15、偏移 255；下一个要写 KV 的位置落到逻辑块 16、偏移 0，这时申请第 17 块。物理块可以是 `[31, 8, …, 52]` 这样的离散块号。再解释最大长度预留、尾块浪费、跨请求共享分别受哪些条件影响。你当场已说出按需增长，这个边界算例能让听者马上跟上。[回听分页算例](../../../../work/managed/interview-video-analysis/derived/li-auto-20261119-review-clips/page-boundary.mp3)

**3. 给“42.7 倍”加上对象。** 如果末维只有 3 个有效元素，硬件每行都按 128 个元素物化，且其余维度、元素宽度不变，这个张量旧物理占用相对理想紧凑占用是 `128÷3≈42.7`。新布局还可能有尾部对齐，且权重、其他激活、workspace 会共同决定进程峰值。现场可以先给这道算术，再拿同输入的旧/新物理字节数和端到端峰值说明实际收益。[回听原声](../../../../work/managed/interview-video-analysis/derived/li-auto-20261119-review-clips/conv3d-ratio.mp3) · [技术核查中的带对齐算例](../analysis/interview-li-auto-recording-01.technical-audit.md)

## 下次面试前的准备顺序

| 优先级 | 做什么 | 完成标准 |
| --- | --- | --- |
| P0 | 把缓存池项目压缩成一段 45 秒开场，再准备技术细节 | 先说固定版本与目标后端的约束，再说旧布局触发哪种整理、本人改了哪层分配。用同负载 trace 补上前后 copy 次数/耗时。暂缺的收益数字直接标待测。用一张表解释卷积历史、递推矩阵、槽位、每 rank 的 shape、dtype 和 stride。 |
| P0 | 重建一张模型性能对照表 | 列出模型 revision、精度、卡数、并行度、batch、输入/输出长度、warm-up 和计时边界。每个长度同时给 prefill 秒数与输入 tok/s，decode 给输出 tok/s 与步时。解释 16–17 tok/s 是最终配置成绩，归因到拆池需独立对照。 |
| P0 | 为 Conv3D OOM 准备一张按字节计算的内存账 | 给出原逻辑 5D、通道后置布局、对齐粒度及单位、新物理布局、每一步字节数。用同一输入核对输出正确性与峰值显存；将 tensor 占用倍率和整模型实测结果分别填入。 |
| P1 | 白板练习 PagedAttention | 在 90 秒内画出请求、逻辑块、物理块、偏移；演示 4095、4096、4097 三种长度的块数与最后位置。增加第二个请求，只共享已满足匹配条件的前缀块。 |
| P1 | 准备一个“插件需要改主仓吗”的真实例子 | 用一个融合算子画出原、新调用链，注明 worker/model runner、modeling、kernel 分别由谁维护。列出上游版本更新后需回归的接口与测试；MTP/FP8 分别标明简历时期和现在的状态。 |

**缓存池项目可以用这段话起头**（建议表达，数字留待实测）：“我们在固定版本的 vLLM 插件上接 GLM-5.3-Flash。旧路径从统一的字节池切出两种状态，在我们的后端还要整理成算子能直接读的布局。我改了分配逻辑，按卷积历史和递推矩阵各自的 shape、dtype 建池。验证时，我会在同样的输入和并行配置下对比整理操作的次数、耗时及 decode 速率。16–17 tokens/s 是当前配置的单请求结果，拆池本身贡献多少，需要前后两组数。”

如果只做一件事，先补缓存池改造的同条件测量。这能同时回答本场最反复的三个追问：原来哪里慢、你改了什么、改完值多少。

## 回听与证据边界

共保留六段原声。除上文三段外，值得优先核实的还有[状态精度 15:33–16:21](../../../../work/managed/interview-video-analysis/derived/li-auto-20261119-review-clips/cache-dtype.mp3)、[状态形状 18:56–19:31](../../../../work/managed/interview-video-analysis/derived/li-auto-20261119-review-clips/shape.mp3)。另外保留了[已确认 SGLang 的反问原段 39:38–40:26](../../../../work/managed/interview-video-analysis/derived/li-auto-20261119-review-clips/team-framework.mp3)。[片段与原片位置清单](../../../../work/managed/interview-video-analysis/derived/li-auto-20261119-review-clips/clip-index.json)

两套本地 ASR 对同一段音频独立解码，也可能共同听错。英文简称、数字连读和短句交叠尤为明显。169 段覆盖全部采样点，保证的是输入连续；可见屏幕和转写均不能代替实机日志或人工逐句回听。

本轮经明确授权，通过 ZenMux 进行了 9 次 Qwen 中文分片转写、1 次 Hydrogen 完整音频流式理解。Qwen 共返回 11,042 个原始 UTF-16 单元，分为 P001–P035；9 份文本均可无损还原。第 3 片（09:59.600–14:59.400）的 MP3 容器时长为 299.880 s，响应计量 271 s。第 9 片（39:58.400–41:02.613）为 64.296 s，响应计量 46 s。这两项未通过 ±5 s 门禁，其余七片通过。第 3 片仍有卷积与 KDA 追问，第 9 片包含社区、vLLM 兼容及告别；计量差值既不能指出漏了哪句话，也不能证明逐字覆盖。两段另有本地时间窗口可供复听。

九份 Qwen 原始文本均已落盘，但服务端未提供可用请求 ID，其追踪状态保留为 `unknown`。Hydrogen 正常以 `stop` 和约定结束标记收尾，真实回执 `d6ed9b9efae74f05acbf34d44c7d5cb1`。本版沿用采样位置定位，Hydrogen 自估秒点只作辅助导航，没有人工逐字定稿或正式岗位评分。
