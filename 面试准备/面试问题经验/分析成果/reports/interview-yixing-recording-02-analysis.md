# 奕行智能第二次面试最终分析报告

- 记录 ID：`interview-yixing-recording-02`
- 公司：奕行智能
- 轮次：第二次面试（来自用户标识）
- 面试日期：未知；源文件没有可用的创建日期证据
- 原片时长：`44:14.033`
- 有效问答：前约 5 分钟为设备调试，正式问答约 39 分钟
- 主来源：`work/managed/interview-video-analysis/incoming/奕行智能-2.mkv`
- 分析底稿：`outputs/managed/interview-video-analysis/analysis/understand-yixing-recording-02-20260829.audio.md`
- 技术审计：`outputs/managed/interview-video-analysis/analysis/interview-yixing-recording-02.audio-evidence-audit.md`
- 一面有限背景：`outputs/managed/interview-video-analysis/reports/interview-yixing-notes-01-analysis.md`
- 报告日期：2026-08-29

## 证据边界

本报告基于 Gemini 3.7 Flash 对完整 44 分钟音频的结构化理解结果，不是人工逐字稿。Qwen3-ASR-Flash 的完整转写首次因请求体大小、缩小音频后的显式重试因录音时长被上游拒绝，均未生成转写文本。因此本报告没有独立 ASR 交叉验证，所有时间点只能用于近似导航，所有内容均按“回答概述”处理，不当作逐字引语。

说话人身份按问答语义推定，没有做声纹识别；专有名词、数字和硬件内部名仍需回听。本文只评价本场呈现出的回答，不作录用、职级或人格判断，也不把“本场没有观察到”写成“不会”。

## 综合结论

这轮面试的考察主线是：你是否不仅做过模型接入，还能把 **硬件结构、框架/runtime、分布式通信、算子供数、性能模型和疑难问题定位** 串成一条可推导、可验证的工程链路。

现有证据支持以下结论：

- 你的回答呈现出较具体的国产 AI 芯片适配与问题定位经历。异步 Padding 数据竞争案例能够讲清“概率性现象—强制同步缩小范围—Host/Device 依赖缺失—根因”，是本轮最强的能力证据。
- 权重 blocked layout 是第二个高价值案例。你能把硬件对齐、跨步访问、加载期预排布和矩阵单元供数连接起来，也明确了与算子团队的协作边界。
- 精度问题排查较成熟：能够从 logits/采样、逐层或二分 dump、CPU/reference 对照和 collective 边界组织排查，而不是只说“换精度试试”。
- 最大短板出现在理论推导和架构边界。DeepSeek 的 TP/EP 通信、机内/机间链路、MatMul Roofline 等问题中，你多次从 profile 现象出发，配置、shape、分片轴和公式没有先说清，面试官需要继续缩小或澄清问题。
- C++、底层算子独立实现和当前 vLLM 核心架构在本轮没有充分证据。你说明了 pybind11 和插件接口，也讨论了向量/矩阵单元，但没有现场代码或完整 operator dispatcher/runtime 设计。
- 结尾的反问与岗位方向相关，但主要停留在“用什么框架、是不是自研云端芯片”。如果还有后续轮次，应该把反问升级到职责边界、当前最大性能瓶颈和入职后的首个交付。

一句话概括：**你的工程排障和硬件感知优化是可信的强项；下一步最需要把“我在 profile 里看到了什么”升级为“在给定配置下，我先验推导应该发生什么，再用 profile 验证”。**

## 面试流程与表现总览

| 近似时间 | 考察主题 | 本场表现 | 复盘判断 |
| --- | --- | --- | --- |
| `00:00–04:55` | 设备调试 | 有键盘、移动和准备阶段声音 | 不计入技术表现；下次提前完成会议与音频检查 |
| `约 04:55` | 自我介绍 | 按框架适配、性能/问题定位、客户与测评支持分块介绍 | 结构清楚，但覆盖过宽，容易引来每一项的深挖 |
| `08:05–14:45` | 芯片架构、存储层次、layout、C++/Python 接口 | 按候选人自述说明专用大核、片上显式存储、1024 字节对齐和 pybind11 | 有一线经验信号；GPU 映射和 PyTorch 注册链路不够严格 |
| `14:45–23:05` | DeepSeek、TP/EP、collective、机内/机间通信 | 按音频理解结果中的疑似 32 卡部署自述，结合 profile 讲多种通信 | 有实际接触信号；并行配置和通信归属表达反复 |
| `23:05–30:20` | 权重 layout、MatMul、Roofline | blocked layout 案例完整；理论上限回答偏 profiler | 案例强，定量性能模型弱 |
| `30:20–34:35` | Coding Agent | 有具体幻觉案例，知道人工审阅与自动测试门禁 | 工具使用有边界意识 |
| `34:35–40:55` | 精度异常、概率性并发 Bug | 打桩对比方法清楚；异步 Padding race 案例完整 | 本轮最强段落，需补准确数字和最终修复 |
| `40:55–44:14` | 换工作原因与反问 | 希望提高核心研发占比；询问对方框架和芯片方向 | 动机可理解；表达可更正向，反问可更深入 |

## 逐题重点复盘

### 1. 自我介绍：完整，但应把“最强证据”前置

你把经历分为框架/模型适配、性能调优与问题定位、客户/测评支持，逻辑是清楚的。风险在于一口气列出多种模型、vLLM、PyTorch、C++、Python、算子优化和测评，很容易让后续每个主题都被按专家深度追问。

更好的组织是先给定位，再给两个最强案例，最后说明业务范围：

> 我目前主要做国产 AI 芯片上的大模型推理框架适配与性能问题定位，技术栈以 vLLM、PyTorch 插件、Python/C++ 为主。最有代表性的两件事，一是把静态权重按硬件访问粒度做 blocked layout 预排布，改善 MatMul 的供数效率；二是定位过一个只在并发下出现的异步 Padding 数据竞争。除此之外，我也负责模型接入、精度回归和外部测评交付。接下来我希望把工作重心进一步放到框架/runtime 的核心研发上。

其中模型名、收益和个人 ownership 只加入已回听确认的内容。

### 2. 硬件架构与 GPU 映射：先讲属性，再讲类比

你将自研芯片描述为更接近 NPU/TPU 的少量大核和脉动阵列，并提到 HBM、片上 Buffer、显式搬运和 1024 字节对齐。这些都是候选人现场自述；如果回听确认，能够比只讲上层 Python 接口更好地体现硬件适配经验。

不足是把片上 Buffer 直接等同 Shared Memory，容易被继续追问。更稳妥的说法是：

> 如果只做功能类比，它更接近软件显式管理的片上 scratchpad，而不是硬件自动管理的 cache。与 GPU Shared Memory 的共同点是都需要软件安排搬运和复用；但容量、可见范围、bank 组织、DMA 路径和执行单元绑定关系不同，所以不是一一对应。我们这个芯片的具体层次是【回听后填写正式名称】。

如果说“没有 L1/L2”，要限定为该具体芯片或编程模型，不要泛化到所有 NPU。

### 3. C++ 到 PyTorch：pybind11 只是链路的一层

你回答 pybind11 是合理起点，但面试官如果关心“PyTorch 插件怎么适配新设备”，还期待 operator schema、dispatcher/backend key、runtime、stream/device guard 和 kernel 的层次。

下次可以先澄清问题：

> 如果是把普通 C++ API 暴露到 Python，pybind11 就可以完成绑定；如果是注册 PyTorch 自定义算子，还要定义 schema，让 dispatcher 按 backend key 找到自研设备实现，再进入 runtime/stream 和设备 kernel。我在这个链路里主要负责【模块/目录】，与算子团队的接口是【输入输出/stream/错误码】。

这样既回答原理，也不会把没有做过的底层实现包装成个人工作。

### 4. DeepSeek 与分布式通信：本场最需要技术校准的题

音频理解结果显示你提到 DeepSeek-V3、32 卡、单卡 64 GB，并能从 profile 识别 AllReduce、All-to-All 和 AllGather。这是一条有价值的实际部署证据，但数字与型号仍需回听。

问题出在解释顺序。TP 和 EP 不是“二选一的两个阶段”这么简单：TP 决定一个线性层/张量怎样切分，EP 决定 expert 怎样分布；MoE 的 token dispatch/combine 常涉及两次 All-to-All，而 expert 内部如果再做 TP，仍可能出现 ReduceScatter/AllReduce。最终 logits 是否 AllGather也取决于 vocab parallel 和采样实现。

下次直接按下面的框架回答：

> 我先固定当时的并行配置，避免把两套实验混在一起。最初是【TP=32、EP=1，待回听确认】，因此 dense attention 和 expert MLP 的具体投影按 TP 分片，在 row-parallel 输出位置出现归约类 collective。后来实验是【TP=?、EP=?】，Router 后 token 要按 expert 所在 rank 做 dispatch All-to-All，expert 计算后再 combine All-to-All；expert 内部是否还有 TP collective 取决于它的分片配置。Profile 里同时出现两类通信不矛盾，但我会按 parallel group 和调用栈确认它们分别属于哪一层。

回答时至少画两张图：dense attention/MLP 的 TP shape，以及 routed expert 的 `route → dispatch → expert → combine`。

### 5. 机内与机间通信：把语义、拓扑和链路分层

你抓住了机间链路通常具有更高启动延迟和更复杂网络路径，但“机内走 RDMA、机间走 IB”如果确是原话，技术层次不够准确：IB 是网络体系，RDMA 是能力/访问语义，机间也常通过 IB/RoCE 使用 RDMA。

建议回答：

> collective 的数学语义可以相同，但 rank 跨不跨节点会改变拓扑和底层 transport。机内可能走 PCIe、NVLink 或厂商 fabric；机间走 NIC 和交换网络，例如 IB/RoCE。性能差异来自链路带宽、启动延迟、NIC/协议开销、NUMA 路径和拥塞。我会用不同 message size 的带宽/时延曲线，再结合 topology-aware trace 判断瓶颈。

### 6. Blocked weight layout：本轮第二强案例

音频理解结果记录了一条完整的候选人自述优化链：MatMul 在目标 workload 上受供数影响 → 原始行主序/跨步访问不适配硬件 → 在模型加载阶段把静态权重按 1024 字节 block 预排布 → 稳态 kernel 直接消费新 layout。你还说明了与算子团队协作而不是独立完成全部底层实现，这个边界是加分项。

现在缺的是可审计数字和准确归因。下次用下面这组字段讲：

1. workload：`M/N/K`、batch、dtype、模型层；
2. 原地址模式：tile、stride、对齐和哪一级存储低效；
3. 证据：有效带宽、矩阵单元利用率、stall/counter；
4. 新 layout：地址公式或一张 4×4 block 示意图；
5. ownership：你负责权重预处理、框架接入和验证，算子团队负责什么；
6. 结果：kernel/单层/端到端的前后绝对值与相对提升；
7. 代价：加载时间、额外存储、多 shape 兼容和精度回归。

在没有 counter 前，把“HBM bank conflict”说成“跨步访问与硬件 transaction/片上供数不匹配”更稳妥。

### 7. Roofline：先算理论下界，再打开 profiler

你现场主要回答“抓 profile，看热点、气泡、H2D/D2H 和异常小算子”。这是好的工程排查流程，但面试官已经把题目缩小为单个 MatMul 的理论性能，期待的是先验估算。

可以直接这样答：

> 对 `A[M,K] × B[K,N]`，计算量约为 `2MNK FLOPs`。我会按 dtype、tile 复用和 C 的读写方式估算最小数据移动量，再算 arithmetic intensity。Roofline 上界是 `min(Peak FLOPS, AI × Bandwidth)`，理论耗时下界是计算时间与访存时间下界的较大者。然后再看实测 achieved FLOPS、有效带宽、矩阵单元利用率、occupancy、同步和 launch gap，判断离理论上界的差距来自供数、并行度还是调度。

不要背固定 bytes 公式；先说明数据是否能在片上复用、权重是否常驻和 C 是否读改写。

### 8. 精度异常与并发 Race：本轮最强案例

精度排查部分的路径是成熟的：特殊 token/乱码先检查 logits 和采样，再逐层或二分 dump，与 CPU/reference 比较，并把 collective 边界作为重点。补上 seed、dtype、误差度量和首个分歧层后，就会更完整。

并发案例尤其值得包装成一个两分钟 STAR，但必须区分“强制同步用于定位”和“最终修复”：

> **S**：相同输入单次运行正常，高并发压力下概率性输出乱码。  
> **T**：判断是数值误差、内存踩踏还是异步时序问题，并构造稳定复现。  
> **A**：先记录错误率和输入；逐步把异步阶段串行化，发现强制同步后问题消失；继续检查 Host Padding 与 H2D 的生产者—消费者关系，定位到 Padding 尚未完成，设备侧就可能消费数据。最终用【回听后填写：event/future/队列依赖等】建立 happens-before，并恢复异步流水。  
> **R**：加入并发、不同 batch/shape 与长时间压力回归；填写修复后错误率、吞吐和延迟。  
> **L**：Host 侧异步任务不能假设会被 Device Stream 自动排序，跨执行域依赖必须显式表达。

音频理解结果给出的“125 次约 30 次异常”暂不进入正式话术，回听确认后再填。

### 9. Coding Agent：案例具体，回答还可以更工程化

你能举出 Agent 把其他 NPU 代码库中的接口误搬到自研插件的具体幻觉，而不是笼统说“AI 有时不准”，这一点很好。人工 review 加 CI 也是正确门禁。

下一次再补三点：只给最小必要上下文；要求 Agent 引用仓库内真实 API/测试；把生成改动放在小 diff 中，先编译和单测，再跑硬件回归。工具名和底层模型代际不是重点，工程闭环才是重点。

### 10. 换工作原因与反问

希望减少支持/运维占比、回到核心框架研发，是合理动机。正式表达可以更聚焦未来：

> 目前的工作让我积累了从模型接入到客户现场问题闭环的完整经验。我下一步希望把更高比例的时间投入框架/runtime 的长期建设，尤其是调度、内存与硬件协同优化；所以我在看职责边界更清晰、能持续沉淀核心模块的机会。

结尾除了问技术栈，还应问：

- 这个岗位入职 90 天最希望我独立负责哪个模块？
- 当前主要瓶颈更偏 scheduler/KV cache、runtime、通信还是算子库？
- 框架、编译器、runtime 与算子团队的接口和 ownership 怎样划分？
- 性能验收主要看 TTFT、TPOT、吞吐、P99、显存还是集群成本？

## 能力画像

| 维度 | 本轮候选人自述支持 | 尚未验证 |
| --- | --- | --- |
| 硬件感知与异构适配 | 较强；能从对齐、片上存储和搬运解释软件改造 | 内部架构名和部分映射需回听 |
| 性能优化 | 较强；blocked layout、profiler、H2D/D2H 与气泡分析有实际案例 | 完整 benchmark、counter 和理论上界推导 |
| Debugging | 强；精度二分和异步 race 案例完整 | 自动化最小化、长期回归数据 |
| 分布式推理 | 有实际接触，理论表达中等 | TP+EP 的 shape/collective 白板推导与通信建模 |
| vLLM/PyTorch 框架 | 有插件和模型接入经验 | 当前核心 scheduler/KV manager/worker/backend 的系统掌握 |
| C++/算子 | 有接口与协作经验 | 现场代码、独立 kernel/runtime 实现、并发与内存安全 |
| 工程工具 | 能把 Coding Agent 放进 review/test 闭环 | 量化效率和更完整自动化门禁 |
| 沟通 | 具体案例清楚、边界诚实 | 理论题需先限定配置和抽象层，减少边答边修正 |

## 与一面简记的有限关联

一面材料只有七条主题，没有完整问答、日期、说话人或现场表现，因此下面只是“主题是否在二面得到更多证据”，不是两轮评分比较。

| 一面简记主题 | 二面可关联内容 | 仍不能合并的部分 |
| --- | --- | --- |
| 框架上的特性适配、vLLM 如何适配 | 二面音频理解结果中的自我介绍、pybind11/PyTorch 插件、硬件对齐和权重预排布自述提供了更具体的适配实例 | 仍缺完整改动目录、版本、代码量、回归矩阵和长期 ownership |
| 融合判断中的 H2D/D2H 与 tensor 变换 | 二面在 profiler 和 layout 问题中再次讨论 H2D/D2H、非连续访问与预处理 | 一面那条简记的说话人未知，不能写成“你两轮都这样回答” |
| attention 融合粒度 | 二面提到向量 layout 转换和算子协作，但没有形成完整 attention fusion 回答 | 不能用二面的 MatMul layout 替代 attention 融合证据 |
| vLLM v0-v1-v2 | 二面提供了候选人有 vLLM 接入背景的自述 | 二面没有清楚考察或回答版本演进，原简记中的“v2”含义仍未知 |
| DeepSpeed 训练 | 二面重点是 DeepSeek 模型与分布式推理通信 | **DeepSpeed 与 DeepSeek 不是一回事**，不能因名称相似合并为同一证据 |
| 前沿模型研究 | 二面对 DeepSeek-V3/MoE 部署的自述可作为具体工程接触线索 | 没有证明系统的论文跟进、PoC 与工程决策流程 |

二面把一面简记中抽象的“框架适配”补成了两个较具体、仍待关键片段回听的案例，但没有消除 vLLM 版本演进、attention 融合和 DeepSpeed 训练的证据缺口。

## 优先改进清单

### P0：下一次技术面前必须补齐

1. **TP/EP/MoE 通信白板**：固定 `TP/EP/DP` 配置，画 tensor shape、parallel group、dispatch/combine 和每个 collective 的输入字节数。
2. **MatMul Roofline**：任选实际 `M/N/K/dtype`，完整算 FLOPs、最小 bytes、AI、算力/带宽上界、理论时间和实测差距。
3. **两个强案例补证据**：blocked layout 补 workload/counter/收益/代价；race case 补准确复现率、依赖图、最终修复和回归结果。
4. **人工回听四段**：`14:45–20:20`、`23:05–26:10`、`26:15–30:10`、`37:35–40:50`，先确认数字、术语和提示幅度。

### P1：岗位专项补强

1. 用一张图讲 PyTorch 自定义设备链路：Python/operator schema → dispatcher → backend implementation → runtime/stream → kernel。
2. 用实际代码版本梳理 vLLM 请求链路与自己的改动点，不再只列模型名和框架名。
3. 对机内/机间 collective 做 message-size sweep，能解释 transport、topology、算法和并行组四个层次。
4. 准备一套精度 Debug 模板：固定 seed/dtype → reference → 首个分歧层 → 误差阈值 → 自动回归。

### P2：现场表达

1. 大问题先给 30 秒全景图，再进入一个亲自做过的点；不要直接从 profiler 细节起步。
2. 每次先说清版本、硬件、batch/shape、并行配置和指标，避免被追问后再补语境。
3. 使用“我负责 / 我参与 / 算子团队负责”三分法说明 ownership。
4. 把换工作原因写成未来目标，准备至少三个与实际职责和验收指标相关的反问。

## 最后建议

这场不需要把所有问题都补成“标准答案”。最有效的准备是围绕两项已表现出的强能力做深：

1. 把 blocked layout 案例补成能被性能工程师复算的案例；
2. 把异步 Padding race 补成能被 runtime 工程师审查的依赖图和回归闭环。

再用 TP/EP 通信图和 Roofline 公式补上理论短板。这样你的整体叙事会从“做过很多适配与排障”升级为“能从硬件和执行模型推导问题，并给出可验证结果”。
