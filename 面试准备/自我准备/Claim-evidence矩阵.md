# Claim-evidence 矩阵

本文件保存面试主张的审计结果与可用口径；学习完成状态见 [W1 进度](../../计划/八周冲刺进度/W1.md)，原验收过程见 [W1 学习验收记录](../../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260914-claim-evidence-matrix)。

<a id="w1-claim-evidence-matrix-20260914"></a>

## W1 当前 Claim-evidence 矩阵

- **审计日期与范围**：2026-09-14；核对 [CV](CV.md)、[项目档案](projects.md)、[自我介绍](self-introduction.md)、[2026-08-29 诊断旧表](AMD-AI框架开发工程师胜任力诊断-2026-08-29.md#13-简历-claim-审计)及截至当日的 W1 evidence。旧诊断保持历史快照，不回写当前结论。
- **状态定义**：`已证明` 表示当前证据足以支持本表给出的有界口径；`需降级` 表示存在相关证据，但现有措辞、范围或数字超出证据；`待补证` 表示当前不应把该强表述作为能力事实。
- **证据层级**：固定 revision 源码只裁决对应实现理解；用户确认的项目口述可支持历史经历叙述，但不冒充 commit、Trace 或 Benchmark 的独立审计。性能数字只有在 Workload、绝对基线、方法和正确性同时闭环后才升级。

| ID | 当前强 Claim 与来源 | 裁决 | 当前证据与边界 | 当前可用口径／关闭条件 |
|---|---|---|---|---|
| `CL01` | [CV“深入理解 vLLM 模型执行、调度、KV Cache 与 PagedAttention”](CV.md#推理框架与模型部署) | 需降级 | Pass A–E、12 文件 source map、KV 账本和独立文字变式已通过；实现证据固定于 `vLLM v0.26.0@568afb3`、V1／MRV1，不包含 Attention Kernel 算法、设备运行和性能实证。 | “能够基于 `vLLM v0.26.0` 源码解释 V1 请求执行、Scheduler／KV block 生命周期及 Prefix Cache 与 PagedAttention 的职责边界。” |
| `CL02` | [自我介绍“对 vLLM 执行链、调度、KV Cache、Chunked Prefill 比较熟悉”](self-introduction.md) | 需降级 | 固定 `vLLM v0.26.0@568afb3` 范围内，独立主链复述以及调度／token 记账、取消／抢占、InputBatch／slot mapping 和 KV 账本的迁移检查已通过；Chunked Prefill 目前只有一次范围纠正，尚无无提示变式。 | 改为“比较熟悉 `vLLM V1` 的请求执行链、调度与 KV Cache”；Chunked Prefill 经独立复核后再并入口径。 |
| `CL03` | [CV“vLLM／PyTorch 源码级二次开发，完成多类模型四阶段适配”](CV.md#工作经历) | 需降级 | [项目一口述](projects.md#project1-oral-baseline-20260902)支持主要负责 Qwen2.5-VL、Qwen3-VL、ERNIE 4.5-VL 的框架层接入、精度对齐和性能优化；Qwen3-Omni、Llama、DeepSeek 及“各模型都完整覆盖四阶段”缺少同等粒度证据，生产项目也没有固定 commit／patch 审计。 | “主要负责 Qwen2.5-VL、Qwen3-VL、ERNIE 4.5-VL 的框架接入、精度对齐和性能优化。” |
| `CL04` | [CV“熟悉 SGLang 的 RadixAttention、结构化输出与调度”](CV.md#推理框架与模型部署) | 待补证 | Lesson 虽固定 `SGLang v0.5.17@2948168` 教学基线，但尚未完成对应源码 map、学习者独立解释或 patch；固定版本和后续计划本身不构成能力 evidence。 | 当前从简历删除；完成固定版本窄对照并通过独立解释后，再决定是否写“了解”。 |
| `CL05` | [CV“掌握 Continuous Batching、Chunked Prefill、Prefix Cache”](CV.md#推理框架与模型部署) | 需降级 | 固定 `vLLM v0.26.0@568afb3` 范围内，Prefix Cache 的 KV 账本、hash／refcount／reuse 和 PagedAttention 职责辨析已有独立证据；Chunked Prefill 只有补差后的预算拆分边界，Continuous Batching 尚无直接独立验收。 | 当前只写“能够基于固定源码解释 Prefix Cache 的命中、引用和复用边界”；Chunked Prefill 与 Continuous Batching 分别补独立变式后再加入。 |
| `CL06` | [CV“掌握 Speculative Decoding、PD 分离、量化和多模态推理”](CV.md#推理框架与模型部署) | 需降级 | 多模态部署有项目口述支持；Speculative Decoding 在当前练习中明确排除，PD 状态机／性能模型尚无独立验收证据，量化也缺少当前可审查工件。 | 当前只保留“有多模态模型推理适配与部署经验”；Speculative Decoding、PD 分离和量化从能力口径删除，分别补证后再加入。 |
| `CL07` | [CV“熟悉 Qwen／Llama／DeepSeek／Ernie 及 MHA／MQA／GQA／MLA／MoE／MTP”](CV.md#推理框架与模型部署) | 需降级 | 有若干模型适配历史口述，但当前 W1 并未分别验收每个模型和结构；名词列表不能代替对 shape、数据流和适配点的独立解释。 | 只保留有具体职责证据的 Qwen2.5-VL、Qwen3-VL、ERNIE 4.5-VL 项目经验；结构名词串当前删除，后续按 shape、数据流和适配点逐项补回。 |
| `CL08` | [CV“理解 Tensor、Storage、Stride、Dispatcher、Autograd、Caching Allocator 和 PrivateUse1”](CV.md#pytorch-与分布式系统) | 需降级 | 项目口述支持 Tensor／Storage／Layout、PyTorch 算子接口、数据拷贝和后端调试经验；本轮未验收 Autograd、Allocator、PrivateUse1 及本人自定义算子注册／实现的完整调用链。 | “具备 PyTorch 算子接口、数据拷贝和 Tensor／Storage／Layout 问题的框架级调试经验”；其他 Internals 与自定义算子实现逐项补证。 |
| `CL09` | [CV“熟悉 DeepSpeed、Megatron-LM、FSDP 及 ZeRO／TP／SP／PP／EP”](CV.md#pytorch-与分布式系统) | 需降级 | [项目四](projects.md#project4-oral-baseline-20260903)支持参与 DeepSpeed ZeRO-3、Megatron-LM TP 与通信后端适配；两框架交付范围、实际并行组合、Loss 对齐和代码边界未核，FSDP 无直接证据。 | “参与 DeepSpeed ZeRO-3、Megatron-LM Tensor Parallel 与通信后端适配，处理 Padding、Collective 与 Stream 语义问题”；FSDP 当前删除，待补证后再加入。 |
| `CL10` | [CV“理解 Ring／Tree AllReduce、ReduceScatter、AllGather，具备自研通信后端经验”](CV.md#pytorch-与分布式系统) | 需降级 | 项目四和 TP 子组变式支持通信接口、分组、精度、同步及性能定位经验；未单独验收 Ring／Tree 算法、通信量和多拓扑选择。 | “具备自研通信后端的接口适配、分组正确性、同步语义和多卡性能定位经验”；Ring／Tree 另行补证。 |
| `CL11` | [CV“具备 Kernel 开发调优经验，熟悉 Triton／TileLang 及 FlashAttention”](CV.md#高性能计算与工程能力) | 需降级 | Conv3D 和 blocked Col-major 只支持框架侧 Shape／Layout 分析、Kernel 接入及协同调优；内部 Kernel 由算子同事实现。无本人 Triton／TileLang／FlashAttention 概念验收、实现、正确性或 profiler 工件。 | “具备 Kernel 接入、真实 Shape／Layout 分析和与算子团队协同调优经验”；Triton、TileLang、FlashAttention 当前删除，待独立证据后再加入。 |
| `CL12` | [CV“擅长以 Profile、算子对比、控制变量和 Replay 定位性能及精度问题”](CV.md#个人概述) | 已证明 | Conv3D、ECG、异步 H2D 和训练通信四个项目口述均给出该方法的具体用法和 ownership；这是用户确认的历史经历证据，不是本轮重跑 Trace 的结果。 | 可保留方法型表述，不把任一单次现象扩张为已证明的底层机制或所有 workload 通用。 |
| `CL13` | [CV“能够使用 Roofline 方法拆解端到端瓶颈”](CV.md#高性能计算与工程能力) | 需降级 | ECG 口述支持低并发 GEMM 的 FLOPs、最低 Bytes 和 AI 初步推导；读写次数、cache reuse、设备屋脊点、实测带宽和效率未闭环。 | “做过低并发 GEMM 的 Roofline 初步估算，用于判断权重访存可能占主导”；完成可复算全链后再升级。 |
| `CL14` | [CV“能够使用 Nsight Systems／Compute，并建立可重复 Benchmark”](CV.md#高性能计算与工程能力) | 待补证 | 通用 Profile／Trace 有历史项目支持，但 Nsight 只见 CV 自述，没有版本、命令、Trace／counter 解读或可复现工件。 | 当前口径只保留“使用框架 Profile／Trace 和控制变量分析 Host、算子、拷贝、通信与 Layout 瓶颈”；Nsight 待真实 capture 补证。 |
| `CL15` | [CV“熟练使用 C／C++、Linux”](CV.md#高性能计算与工程能力) | 需降级 | [C++／Linux 基线](../../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-cpp-linux-baseline-20260914)支持 RAII、多态、编译链接、ELF 和动态库诊断的书面理解；编译、sanitizer、真实库加载、线程／memory ordering、ABI 和现场编码尚未实践验证。 | “熟练使用 Python、Linux、Git 和 Bash；具备 PyTorch 扩展与通信适配层的 C++ 修改和调试经验”；不把书面基线升级为“熟练 C++ 系统开发”。 |
| `CL16` | [CV／自我介绍“Qwen3-VL Conv3D 使 TTFT 下降 40%”](projects.md#project1-oral-baseline-20260902) | 需降级 | 口述支持 `OOM → 小通道 Padding → 模型侧布局重构 → 算子协作 → 两级验证`；模型是 Qwen2.5-VL-32B 还是 Qwen3-VL、具体性能幅度、绝对耗时、Profile 分母和布局／Kernel 收益拆分均未统一。 | 暂撤下百分比与冲突模型名；只说“完成模型侧布局重构并协同算子优化，消除已观察到的 OOM，显著降低 Conv3D 开销和 TTFT”。 |
| `CL17` | [CV“ECG 从 40 秒以上降至 10–15 秒”](projects.md#project2-oral-baseline-20260902) | 需降级 | 项目口述支持分阶段优化并达到客户时延目标；当前起止范围、Transformers／vLLM 边界、输入／输出长度、并发、预热、统计和单项消融未统一。 | 对外先不写精确起止数字，改为“经过 Host 路径、小 Shape 计算和权重布局优化，显著降低端到端时延并达到客户验收目标”。 |
| `CL18` | [自我介绍“Col-major 使三类模型少并发吞吐提升约 20%”](self-introduction.md) | 待补证 | 只见自我介绍中的同源数字；项目二只支持 ECG 的权重预排布与访存判断，不支持 Llama-3-70B、Qwen2.5、Qwen3 三模型和 `20%` 口径。 | 暂删模型列表和百分比；可改为“在低并发小 Batch 场景中，通过加载期权重预排布改善 Matmul 访存效率”。 |
| `CL19` | [CV／自我介绍“vLLM V1 异步 H2D／D2D 异常目前根因闭环中”](projects.md#project3-oral-baseline-20260902) | 已证明 | 新项目基线已覆盖旧状态：按用户口述，根因为 `CPU Padding 完成 → H2D 提交 → 设备拷贝完成 → 消费` 依赖不完整，已修复；168 条请求×5 轮，共 840 次在当前请求集中未再观察到原异常。本表不采用已撤回 diff，也不扩张为全部 Runtime 实现归属或所有 workload 零故障。 | 当前文稿的“根因闭环中”已滞后；可改为“定位两阶段 Host 准备与异步 H2D 间的依赖缺口，通过统一异步任务标记与等待机制完成修复；修复后在现场 168 条请求×5 轮回归范围内未再复现”。 |

**矩阵结果**：`已证明` 2 条，`需降级` 14 条，`待补证` 3 条，共 19 条。这一结果完成 W1 的当前 Claim 审计门，但不代表原文稿已经改写，也不代表其他 W1 任务完成。后续修订外部文稿时以本表为当前裁决入口，项目事实和数字仍回到各项目的待核字段关闭。

<a id="downgrade-restoration-evidence"></a>

## 后续处理：改写口径与恢复证据（2026-09-29）

- **用途**：W4 后开始投递前，据此修订 CV 与面试口径；CV 目前保持原样。上表 2026-09-14 的裁决不因本节改变，复审时再更新。
- **计划来源**：写明最可能产出证据的位置。“项目事实”只能由你依据真实项目记录补充确认，学习无法替代；“计划外”表示计划目前没有安排。
- **审计后进展**：2026-09-14 之后已经取得、复审时可以计入的相关证据；它们本身还不足以恢复原说法。

<a id="claim-wording-decisions-20260929"></a>

### 改写口径

以下说法不再追求恢复原文，改用新口径（用户 2026-09-29 决定）。

| ID | 新口径 | 依据与状态 |
|---|---|---|
| `CL03` | 主要负责 Qwen2.5-VL、Qwen3-VL、ERNIE 4.5-VL 与 GLM-5.3-flash 的框架接入、精度对齐和性能优化；删去 Qwen3-Omni、Llama、DeepSeek | 前三个模型见[项目一口述](projects.md#project1-oral-baseline-20260902)；GLM-5.3-flash 待按[项目模板](projects.md#project-glm-template)补充描述 |
| `CL09` | 技能行改为“理解 DP、TP、PP、SP、EP 等并行策略的切分与通信语义”，删去“熟悉 DeepSpeed、Megatron-LM、FSDP”；经历行改为“在自研芯片训练适配中，基于 DeepSpeed、Megatron-LM 的测试调试通信后端基础功能；定位多 Stream 通信的调度开销，并实现可回退的单 Stream 方案” | 依据[项目四口述](projects.md#project4-oral-baseline-20260903)与 W2 单元一；你已说明对训练框架本身只做了基于测试的基础功能调试；用户已确认该口径。ZeRO／FSDP 的理解在 W7 后再决定是否写入 |
| `CL11` | 具备 Triton kernel 编写与调优实践经验，包括 FlashAttention 式的 fused attention 前向实现；删去 TileLang | programming-lab Triton 01–06：本人实现 matmul、fused softmax 与 fused attention 前向，并做过 `GROUP_SIZE_M`、stages 等配置的受控对比实验 |
| `CL14` | 会使用 PyTorch、vLLM 框架 Profile／Trace 和控制变量分析 Host、算子、拷贝、通信与 Layout 瓶颈；删去 Nsight | 与 `CL12` 同源的项目口述 |
| `CL16` | 在 Qwen2.5-VL／Qwen3-VL 视觉 Encoder 的 Conv3D 上完成模型侧布局重构，并与算子同事协同优化；在 Qwen2.5-VL-32B 图片输入测试组中，算子 Profile 里 Conv3D 的 cycle 占比由约 95% 降至 0.03%，TTFT 从分钟级降到 5 秒以内 | [Conv3D Case Card](Conv3D-Case-Card.md) F4–F6；数字均来自 Qwen2.5-VL-32B 图片输入测试组。两个模型的 Conv3D 走同一优化路径，但权重形状不同，面试中不说“形状相同” |
| `CL17` | ECG 多模态模型端到端时延从 30–40 秒降至 20 秒以内，达到客户验收目标 | [项目二口述与测量条件](projects.md#project2-oral-baseline-20260902)：`Transformers` 运行栈，含图像预处理、从请求发出算到完整输出，生成上限 1024、平均约 700–800 token，优化前后都是 10 次平均、含首次运行（无预热编译） |

<a id="claim-restoration-evidence-20260929"></a>

### 恢复原说法所需证据

本行证据全部满足才恢复原说法；只满足一部分时，只把已证实的部分并入“当前可用口径”。

| ID | 恢复原说法所需证据 | 计划来源 | 审计后进展 |
|---|---|---|---|
| `CL01` | ① 约 15 分钟 vLLM 主链口述并经追问；② 一次真实运行的 trace 或日志，把 Scheduler 决策、KV block 分配／复用和抢占对应到可观测行为；③ PagedAttention 的 kernel 侧：说明 attention backend 如何通过 block table／slot mapping 读取分页 KV（到后端 metadata 与 kernel 接口层即可）。 | ① W4 Mock（§9.2-6）；② W4 trace 解读（§9.2-3）；③ W3（§8.2-8） | — |
| `CL02` | Chunked Prefill 的无提示独立变式：给定 token 预算和混合的 prefill／decode 请求，预测本步切分，并解释对 TTFT／ITL 的影响；自我介绍属口头材料，还需在 W4 Mock 中口述通过。 | W4（§9.2-7）；口述在 W4 Mock | — |
| `CL04` | 固定 SGLang 版本中，RadixAttention 的前缀匹配、引用计数与淘汰，结构化输出如何生成 token mask，调度如何形成批次并安排 prefill／decode，三部分各有一次独立解释或预测变式，并能与 vLLM 对照。 | W4a（§9A） | — |
| `CL05` | ① Continuous Batching 独立验收：基于固定源码说明请求如何逐步加入、退出批次，并完成一次预测变式；② Chunked Prefill 同 `CL02`；③ “掌握”还需一次受控 benchmark：调整调度参数（如 `max_num_batched_tokens`），报告 TTFT、ITL 与吞吐的绝对值、方法和取舍。 | ①② W4（§9.2-7）；③ W4 benchmark packet（§9.2-2） | — |
| `CL06` | 四项分别满足：PD 分离通过 W3 验收门；量化在 W4 的 dtype／AWQ／W4A16 推导之外，另有一份可审查工件（量化前后的精度与性能对照，或已确认的项目经历）；Speculative Decoding 讲清 draft／verify、接受率与加速比推导，给出固定源码的执行路径，并说明拒绝采样如何保持输出分布；多模态推理基于固定源码讲清 processor、encoder、embedding 合并与 M-RoPE 位置的链路，并与项目经历对应。 | PD：W3；量化推导：W4（工件计划外）；多模态：W4（§9.2-8）；Speculative Decoding：W4a（§9A） | — |
| `CL07` | 逐个结构讲清 shape、数据流和框架适配点。MoE：适配点指 vLLM／SGLang 的 MoE 层与 EP 通信后端如何接入。MHA／MQA／GQA：KV head 形状、每 rank KV 字节，以及 TP 下 KV head 的切分或复制。MLA：潜变量压缩的形状、KV 公式为何不同、后端支持情况。RoPE／M-RoPE：旋转公式和 M-RoPE 的时间／高／宽位置分解及实现位置。MTP：训练目标和推理时作为草稿的用法。每个模型家族再给一张基于公开 config 的结构差异表，标明哪些由你实际适配。若要写“在自研芯片上适配过 MoE 模型”，另需项目事实。 | MoE 适配点：W2 单元二；MHA／MQA／GQA／MLA 与模型差异表：W3（§8.2-3）；RoPE／M-RoPE：W4（§9.2-8）；MTP：W4a（§9A） | W2 单元一已验收 MoE 路由、放置与通信量（shape 与数据流） |
| `CL08` | 一个真实算子从 schema、dispatcher、fake／meta、C++ 注册、后端分发到测试的逐层文件与函数；allocator、storage 生命周期、device guard 和 stream 能讲清机制而非只列名词；本人的 custom op 注册与测试可运行；另需 Autograd（计算图、`autograd::Function`、backward engine 调度）与 PrivateUse1 后端注册路径的独立解释。 | W5（§10.2-1 含 PrivateUse1；§10.2-7 Autograd） | — |
| `CL10` | 独立推导 Ring AllReduce = ReduceScatter + AllGather、每 rank 通信量 `2(n−1)/n · S` 与 α–β 时间模型；说明 Tree 在小消息、大规模下的延迟优势和 Ring 的带宽优势；对照 NCCL 的 ring／tree 算法选择给出源码或文档锚点。 | W7（§12.2-8） | W2 单元一已验收“collective 由切分推导”（语义层），未涉及 Ring／Tree 算法 |
| `CL13` | 一个完整可复算案例：FLOPs、Bytes（写明读写次数与 cache reuse 假设）、AI、设备屋脊点、性能上界与时间下界、实测效率；再放回端到端链路，说明哪些算子受访存限制、哪些受计算限制及其占总时延的比例。 | W2 单元四（小型 Roofline）→ W4（§9.2-1 完整案例） | — |
| `CL15` | 异步缓冲区生命周期程序能讲清 ownership、happens-before 与析构，并经 sanitizer 或等价工具验证；现场实现 RAII 容器、线程同步、错误处理与测试，可编译运行并通过 sanitizer；能解释 memory ordering 与 ABI／构建问题。 | W2 单元三；W5（§10.2-3、§10.2-6） | W1 P2 已通过自建程序的 ELF／动态库诊断与启动修复实操 |
