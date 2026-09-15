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
