# 地平线 AI 推理框架开发工程师面试自我复盘

> 录像：2026-08-13，39:38
> 分析用途：候选人本人复盘
> 报告状态：候选版，等待按关键片段人工复核
> 岗位校准：部分校准（未提供正式 JD、职级、简历和内部评分表）

## 1. 先说结论

这场面试中，你最有说服力的不是“会使用 PyTorch／vLLM”，而是能把自研 ASIC 的约束转化为模型转换、运行时、算子和数据布局层面的工程方案。矩阵权重离线重排、多模态中间张量对齐膨胀、KV Cache 布局和低精度归约，都是与推理框架岗位高度相关的案例。

本场最明确、最值得优先修复的问题，是 **22:55–24:30 的 Padding 讨论没有先限定语境**。稠密 prompt batch 的左右 Padding、自回归 token 向右追加、Paged KV Cache 的 slot／block-table 管理是三件不同的事。回答一开始落在“左还是右”的结论上，随后出现迟疑和反复。可靠结论是“术语边界和现场推演方式需要加强”，不能仅凭非逐字摘要断言你的实现逻辑错误。

第二个问题是多个案例“方案讲得好，证明契约讲得不够完整”。例如 10%–20% 的提升、`C=3 → 256` 的中间张量膨胀、MTP／Chunked Prefill 的收益，都缺少 workload、shape、dtype、硬件状态、绝对值、统计口径、正确性阈值和适用边界。面试官容易因此相信你做过，但仍无法判断你能否稳定复现和迁移。

第三个问题不是已经证实的能力缺陷，而是 **本场证据空白**：C++ 系统工程、完整编译器 IR／pass／codegen、量化算法侧校准与搜索、CI／性能回归、车端确定性约束都没有被直接充分考察。下一阶段应同时“补能力”和“补可展示证据”，但不要把“本场未观察”误写成“你不会”。

一句话画像：**本场出现了较强的算子、运行时、异构适配和性能排查信号；主要短板是歧义题的抽象推演、技术术语的精确边界，以及项目结果的量化证明。**

## 2. 证据边界

- 远端模型处理了完整视频，但原始 12 条证据的时间并集约为全片的 **44.44%**；“看过全片”不等于“每个说话轮次都有证据”。
- 所有证据都是非逐字摘要。时间点可用于回片，不能把摘要加引号当作你的原话。
- 自动补出的 `ev-13` 至 `ev-18` 只是主题索引，不是重新听到的独立提问证据，本报告不把它们用于能力判定。
- `ev-8` 混合了面试官提问与候选人回答；`ev-12` 位于双方交替发言的反问段。两者的说话人归属均需人工复核。
- 以下“强／较强／局部／未观察”描述的是本场证据强度，不是岗位等级或录用评分。

详细 QA 见 [证据与技术 QA](../analysis/run-20260823-01.evidence-qa.md)。

## 3. 本场真正展示出来的优势

### 3.1 数据布局与软硬件协同：本场最强案例

在 10:15–12:00，你描述了矩阵切块访问的效率问题，把权重布局转换前置到模型加载阶段，并给出 10%–20% 的性能收益。[ev-4]

这个案例的价值在于因果链比较完整：

`访问模式问题 → 离线权重预排布 → 避免运行时转换 → 性能收益`

需要修正的是归因精度。非连续 global/HBM 访问、cache-line 浪费、partition/channel 冲突和片上 shared-memory/LDS bank conflict 不是同一个概念。若原片确实使用了 “HBM Bank Conflict”，下次应补出具体 memory level、地址到 bank 的映射、lane/stride 和硬件计数器；否则更稳妥地称为“与硬件存储组织相关的 stride／layout 访问低效”。

把该案例升级为面试王牌，还需要补一张基准卡：代表性 M/N/K、dtype、batch、硬件频率、warm-up、重复次数、p50/p95、正确性容差和不适用的动态 shape。

### 3.2 多模态 OOM／TTFT 排查：跨层定位能力强

在 15:00–17:30，你从多模态视觉 Encoder 的 OOM／TTFT 症状，定位到 `C=3` 在特定硬件约束下被补到 256，并通过维度合并／算子重排规避无效存储。[ev-6]

这段能体现从模型结构、框架表示到 Kernel 约束的跨层排查能力。`256 / 3 ≈ 85.3` 在“channel 元素被真实物化到 256”这一语境下算术成立，但不能写成“256 字节对齐”，也不能外推成整体模型显存膨胀 85 倍。需要回片确认：

- 256 的单位是 channel 元素、字节还是其他 tile 约束；
- 哪个中间 tensor 被物化；
- 峰值内存和 TTFT 的绝对前后值；
- 动态分辨率、batch 和不同视觉 Encoder 下的适用边界；
- 维度合并后如何做 shape／stride 语义与数值回归。

### 3.3 Runtime 与 KV Cache：有真实改造信号

在 07:25–09:00 和 25:10–26:25，你讨论了 PagedAttention／Block Table、特定后端的 Block Size 约束，以及结合向量寄存器消费方式调整 K/V Cache 排布。[ev-3、ev-9]

这些内容比只讲 PagedAttention 概念更接近实际 Runtime 工作。不过应把术语讲准：vLLM 的 `block_size` 单位是每个 KV block 的 token 数；不同版本和后端限制不同。若 256 准确，需要给出实际 vLLM 版本和自研后端，不能把它说成通用默认值。更精确的链路是：

`Scheduler 做 admission／预算 → KVCacheManager 分配 block／slot → block table 维护逻辑到物理映射 → ModelRunner／Attention backend 消费元数据`

K/V 交错存储也是硬件专属方案，不天然优于分开存储。下次要说明 DMA／vector load 为什么能利用同一 transaction、QK 与 PV 两阶段如何消费，以及参考实现如何比对。

### 3.4 数值稳定性：有实践，解释还可更精确

13:00–13:55 的 TP 数值核验和 32:00–34:00 的 RMSNorm 低精度处理，说明你关注分布式切分后的正确性和敏感算子的高精度归约。[ev-5、ev-11]

“使用 FP32 做平方、均方归约和 `rsqrt`，再转回低精度”是合理方案。若原片与摘要一致，需纠正两处表述：RMSNorm 计算 mean-square，不是去均值后的 variance；FP16 的动态范围较小，平方／归约更易溢出，而 BF16 与 FP32 具有相同指数位宽，主要问题通常是尾数较短导致的舍入和归约误差。

### 3.5 熟悉项目的叙述结构较好

在布局和多模态案例中，你基本能按“症状／瓶颈—根因—修改—收益”展开。[ev-4、ev-6] 这是一项直接可复用的面试能力。问题在于遇到语境歧义或超出熟悉实现的问题时，结构会退化为边想边给结论。[ev-8]

改进目标不是“显得更自信”，而是让回答更可验证：先定义语境、单位、shape 和不变量；再推导；最后才给结论。

## 4. 能力证据重新分级

| 岗位维度 | 本场证据 | 复盘结论 |
|---|---|---|
| Runtime / KV Cache | 较强 | 有分块、调度和布局案例；需复核 block 单位、版本与逻辑／物理映射术语。[ev-3、ev-7、ev-9] |
| Operator / Fusion | 强 | 布局重排、视觉算子处理、MoE 融合均有案例；operator 与 single kernel 的边界要说清。[ev-4、ev-6、ev-10] |
| Performance | 较强 | 能讲瓶颈与方案；benchmark 契约、绝对指标和 tail latency 不完整。[ev-4、ev-6、ev-7] |
| Heterogeneous adaptation | 较强 | 多条案例直接围绕自研 ASIC 约束和软件改造；不能外推为完整车端 BPU 能力。[ev-1、ev-3、ev-4、ev-6、ev-9] |
| Debugging / numerical | 中等至较强 | 有 OOM、通信一致性和 RMSNorm 案例；逐层工具链细节仍需回片。[ev-5、ev-6、ev-11] |
| ML deployment | 中等至较强 | 有模型转换、vLLM 与多模态适配；具体模型清单和服务化范围不作外推。[ev-1、ev-2、ev-6] |
| Quantization | 局部 | 推理侧格式处理与低精度算子有证据；PTQ/QAT、observer、scale 和校准能力未评估。[ev-2、ev-11] |
| Compiler | 局部 | 有图／布局变换信号；IR、shape/type inference、pass、codegen、静态内存规划未评估。[ev-2、ev-4、ev-6] |
| Python | 局部 | 有 PyTorch／vLLM 工作背景；代码设计与工程质量未直接考察。[ev-1、ev-2] |
| C++ | 未观察 | 没有 RAII、所有权、并发、构建、ABI 或代码设计证据。 |
| Quality engineering | 局部 | 有正确性／精度核验信号；CI、性能回归、兼容和发布未观察。[ev-5、ev-11] |
| Technical communication | 分化 | 熟悉案例结构清楚；Padding 歧义题中没有先限定语境，表述反复。[ev-4、ev-6、ev-8] |

结构化模型最初把 12 个维度全部标为 positive，这一结论不采纳。

## 5. 逐主题复盘

### 5.1 自我介绍（00:23–01:35）

现有摘要支持你介绍了教育和自研 ASIC 上 PyTorch／vLLM 适配背景。[ev-1] 由于没有逐字稿，无法判断时长分配和重点是否最佳。

建议固定成 90 秒：

1. 一句话定位：自研 AI 加速器上的推理框架与大模型部署工程师；
2. 两个最强证据：布局预排布性能案例 + 多模态 OOM／TTFT 案例；
3. 技术覆盖：模型转换、Runtime／KV Cache、算子、数值一致性；
4. 与目标岗位的连接：希望把异构推理经验迁移到端侧确定性部署问题。

### 5.2 模型部署、量化与 Paged KV（03:35–09:00）

优点：能把模型格式、算子适配和 KV 管理串成执行链路。[ev-2、ev-3]

需要回片核实一个潜在技术问题：摘要写成“遇到 FP4／FP8 权重，使用 AWQ 转为 W4A16／W8A16”。公开 AWQ 主路径是利用校准激活从高精度基准权重生成 INT4 weight-only 的 W4A16；W8A16 是通用 INT8 weight-only 格式，不应自然等同为 “AWQ 的 W8A16”。如果原意是“目标芯片不支持发布模型的 FP4／FP8，于是回到高精度权重重新量化”，应明确说出；若直接对已量化 checkpoint 二次量化，则需解释误差控制。

推荐追问：

- 输入权重的真实 dtype 是什么？INT4 与 FP4 如何区分？
- group size、scale 粒度、zero-point 和校准集如何选择？
- Block Size=256 的单位、vLLM 版本、自研后端与尾块碎片如何权衡？
- Prefix Cache 的引用计数、共享、抢占和回收如何实现？

### 5.3 Layout、TP 与多模态优化（10:15–17:30）

这是本场最有区分度的一组案例。[ev-4、ev-5、ev-6]

下一次回答不要停在“插入 AllReduce／AllGather”。标准 TP 中，QKV 和 MLP up/gate 常是 column-parallel，输出可继续保持分片；Attention O 和 MLP down 常是 row-parallel，需要对 partial sum 做 AllReduce，开启 sequence parallel 时可能使用 ReduceScatter。collective 由 tensor shape、分片轴和下游需要决定，不是每个 Linear 后固定插 AR+AG。

面试中建议直接画：

`QKV column-parallel → local attention → O row-parallel → partial sum collective`

`gate/up column-parallel → local activation → down row-parallel → partial sum collective`

同时标出每一步 tensor shape、每卡 bytes 和 dense reference 的 `allclose` 容差。

### 5.4 Prefill、Decode、MTP 与 Padding（20:35–26:25）

优点：能从 Prefill／Decode 的常见计算特征讲到调度和 KV 布局。[ev-7、ev-9]

需要加限定：Prefill 常偏 compute-bound、Decode 常偏 memory-bound 是工程启发式，会随 batch、context、模型和硬件改变；TP 还有通信代价。Chunked Prefill 是 token-budget 下协调 prefill 与 decode 的调度策略，不是 decode 算法。MTP 是带验证的 speculative decoding，需要模型有相应 head／草稿路径，收益取决于 acceptance length 和额外 verify 开销。

#### Padding 题的更好答法

“我先区分三个语境。第一，decoder-only 的稠密 prompt batch 通常用左 Padding，使每行最后一个位置都是真实 token，下一 token logits 的读取位置一致；第二，自回归生成的新 token 都沿时间轴追加在右侧；第三，vLLM continuous batching／PagedAttention 主要用 `seq_lens`、slot mapping 和 block table 管理有效 token，物理 KV 不一定存在传统的稠密左右 Padding。若问题指某个后端为 CUDA Graph 或 block table 做的 Padding，还需看该实现。无论哪种表示，我会检查有效长度、position id、attention mask、logits 读取位置和 KV 写入 slot 这五个不变量。”

这比直接回答“左”或“右”更准确，也能体现框架级推理能力。

### 5.5 MoE 与低精度数值（30:20–34:00）

把 Top-K／dispatch／GEMM／reduce 包装为 Fused MoE operator 以减少调度和中间存储，是合理方向。[ev-10] 但“一个 operator”和“一个设备 kernel”不是同一件事；公开实现通常分别融合 router、permute／dispatch、grouped GEMM 和 combine，expert parallel 还会引入跨设备通信。

下次应主动说明：是否包含 gate matmul／softmax、两次 GEMM+activation、token permutation、local expert 还是 expert parallel、动态 expert token 数如何 compact／pad，以及收益来自 launch、内存还是计算。

RMSNorm 部分则应明确 mean-square、FP32 opmath、FP16 动态范围和 BF16 尾数精度的区别。[ev-11]

### 5.6 反问（35:51–39:38）

该段是双方交替发言，当前 `ev-12` 无法可靠区分哪些是你的问题、哪些是面试官回答。因此本报告不把“2B–7B、编译器、C++ Runtime”等摘要当作你的能力证据。

下次可稳定准备三类问题：

- 团队当前最重要的是 latency、tail latency、功耗、内存还是部署周期？
- 新人前三个月更可能落在编译器、Runtime、算子还是模型适配的哪一层？
- 模拟器、板端 profiling 和业务回归在日常定位中分别占多大比重？

## 6. 暴露问题与优先级

| 优先级 | 问题 | 证据性质 | 修复方向 |
|---|---|---|---|
| P0 | Padding／位置／KV slot 的语境没有先拆开 | 高置信：回答段确有迟疑；是否答错仍需回片。[ev-8] | 用不等长序列逐步推导 mask、position、logits 位置、block table 和 slot。 |
| P0 | TP、RMSNorm、AWQ 等术语若按摘要字面理解不够精确 | 中置信：全部是非逐字摘要。[ev-2、ev-5、ev-11] | 回片确认原话；用 shape、dtype、单位和适用条件重写答案。 |
| P1 | 性能故事缺可复现测量契约 | 中高置信：摘要只给相对收益或定性结论。[ev-4、ev-6、ev-7] | 每个案例补 baseline、absolute/relative metric、正确性和边界。 |
| P1 | 量化算法、编译器、C++、质量工程缺直接展示 | 证据空白，不是已证实短板 | 做三个可展示的小项目，并准备设计取舍与测试证据。 |
| P2 | Linear／Hybrid Attention、端侧静态内存、MoE EP 等岗位相关主题未充分覆盖 | 学习与复测主题 | 在基础问题稳定后补齐，不把它们写成本场已暴露缺陷。 |

## 7. 学习路线

下面按每周约 10–12 小时设计。学习目标不是“读完资料”，而是产出可以在下一次面试中展示和复测的证据。

### 未来 2 周：修复现场推演与术语精度（约 20–24 小时）

#### A. Padding + KV 生命周期最小实验（6 小时）

练习：

- 用两个不同长度 prompt 比较 dense batch 的 left/right padding；打印 `input_ids`、`attention_mask`、`position_ids` 和最后位置 logits。
- 用 15／16／17 token 跨 block 边界，跟踪 `seq_lens`、`query_start_loc`、slot mapping、block table 和 decode 追加。
- 手算 block size 为 16／32／256 时的尾块浪费。

掌握标准：

- 3 分钟内区分“prompt batch 左 pad”“生成 token 向右追加”“block-table／执行后端的元数据 Padding”；
- 8 分钟内画出 3 个不等长请求的一次 prefill 和两次 decode；
- 能解释 `Scheduler → KVCacheManager → ModelRunner` 的数据流。

#### B. Tensor Parallel 通信账本（5 小时）

练习：为 `hidden=4096`、`FFN=11008`、`TP=4` 手算 QKV／O 和 gate-up／down 的分片 shape；记录每个 collective 的 shape 和 bytes，并与 dense 结果做逐层对比。

掌握标准：不看资料即可说明 column-parallel 输出何时保持 shard、row-parallel partial sum 何时用 AllReduce／ReduceScatter、AllGather 何时才必要。

#### C. RMSNorm 数值扫描（4 小时）

练习：实现低精度输入下的全低精度归约和 FP32-opmath 两个版本，扫描不同幅值与 hidden size，记录 Inf／NaN、max-abs 和 relative error。

掌握标准：准确解释 mean-square 与 variance、FP16 与 BF16 的指数／尾数和失效模式；能说明为什么 BF16 动态范围大仍常用 FP32 累加。

#### D. 六张工程案例卡（5–9 小时）

每张固定写：

`问题 → 基线环境 → 定位证据 → 根因 → 修改 → 正确性验证 → 性能数据 → 代价／边界`

至少覆盖布局、TP、多模态 OOM、Prefill／Decode、KV 布局、MoE／RMSNorm。每张必须含一个绝对指标、一个相对指标和一个正确性指标；数字不确定时回查真实记录，不能补造。

### 未来 1 个月：补三个可展示的直接证据（再投入约 30–40 小时）

#### A. 低比特量化实验（12 小时）

- 从 FP16／BF16 基准权重分别做 INT8 weight-only 和 AWQ INT4；不要把已量化 FP4／FP8 二次量化作为主路径。
- 比较 per-tensor、per-channel 或 per-group scale；设计校准集。
- 用逐层 activation diff／困惑度或任务准确率定位敏感层，做 mixed-precision exemption。

验收：能写清 W4A16／W8A16 中 W/A 的 dtype、scale 粒度与校准来源，并交付一份“首个发散层 → 修复策略 → 精度恢复”的实验报告。

#### B. 推理性能测量模板（8–10 小时）

- 固定模型、shape、dtype、batch、输入／输出长度、频率、warm-up 和重复次数。
- 同时记录 TTFT、ITL／TPOT、tok/s、p50/p95、峰值内存；条件允许时记录带宽、算力和功耗。
- 启停 Chunked Prefill；若模型原生支持 MTP，记录 acceptance rate／mean acceptance length 与额外验证开销。

验收：运行前能预测某个配置更偏 compute-bound 还是 memory-bound，并用测量解释预测是否成立；不再只报平均吞吐。

#### C. C++ Paged-KV 小项目（12–16 小时）

- 实现 block allocator、引用计数、prefix 共享、回收和简单抢占。
- 用 RAII 管理资源，加入并发安全、错误处理、单元测试和 sanitizer。
- 用 API 隔离 Scheduler 与 allocator。

验收：能解释所有权、锁粒度、复杂度、尾块浪费和 ABI 演进；用测试证明共享块不会被提前释放。

### 未来 3 个月：形成编译器—Runtime—端侧部署闭环（累计约 80–100 小时）

#### A. 小型图编译流水线

从 ONNX、`torch.export` 或自定义 IR 导入小模型，实现 shape/type inference、常量折叠、DCE、算子融合、layout／precision propagation、简单异构切分和静态内存复用。

验收：至少 20 个 pass／边界测试；可打印每个 pass 的 IR diff；优化前后数值在定义容差内；能量化峰值内存、算子数和 latency 变化。

#### B. Layout／Bank 实证与 MoE 分层融合

- 分开测 global coalescing、cache 行为与片上 bank conflict；用地址—bank 图和 profiler counter 解释，而不是只看 latency。
- 把 toy MoE 拆成 gate/top-k → permute/dispatch → grouped GEMM → activation → combine，逐步融合并统计 kernel 数、中间 buffer 和端到端收益。

验收：不会混用 uncoalesced access、cache miss 和 bank conflict；能明确 operator fusion 与 single-kernel、local MoE 与 expert parallel 的差异。

#### C. 端侧推理设计与地平线公开工具链

围绕一个有明确 deadline 的小模型，设计 CPU／BPU 切分、静态内存、零拷贝、算子融合、超时降级与可观测性。若具备公开 SDK／板卡，再完成模型转换、量化、运行和中间层差分；没有硬件时先交付设计文档和可验证的局部原型。

验收：给出 latency、峰值内存和带宽预算；每项设计说明收益、代价和失败模式；能在 20 分钟系统设计中完整讲清。

#### D. 每两周一次复测

题目固定覆盖 Padding／KV、TP shape、量化误差定位、图编译 pass、C++ Runtime、性能基准和端侧系统设计。每次录屏，要求：

- 先限定语境、单位、版本和后端；
- 画 shape 与数据流；
- 给瓶颈证据、方案、代价和验证指标；
- 不熟悉时明确边界，再用最小例子推导。

## 8. 下一次面试前的最小清单

1. 90 秒自我介绍，突出两个最强案例。
2. 六张带 benchmark 契约的工程案例卡。
3. 一张 dense batching 与 Paged KV 的对照图。
4. 一张标准 TP 的 shape／collective 图。
5. 一份量化误差定位实验报告。
6. 一个 C++ Paged-KV 或图编译可运行项目。
7. 三个围绕岗位实际约束的反问。

## 9. 建议复测题

1. 三个请求长度为 3、5、7。分别画 dense batch 和 continuous batching 的 mask、position、block table 与下一次 KV 写入位置。
2. `block_size=256` 时，尾块浪费、prefix 共享、抢占和硬件访存收益如何权衡？
3. 为 TP=4 的 QKV／O／gate-up／down 推导每卡 tensor shape 和 collective bytes。
4. 为什么 BF16 动态范围接近 FP32，RMSNorm 中仍常做 FP32 opmath？
5. 如果目标芯片不支持某个 FP4／FP8 checkpoint，你会从哪一版权重开始转换或重新量化，如何避免二次量化误差？
6. 如何证明 10%–20% 的布局收益来自预期的访存机制，而不是 cache、频率或测量波动？
7. Fused MoE 是一个图算子还是一个设备 kernel？expert parallel 后融合边界如何变化？
8. 一个 10 ms deadline 的端侧模型中，如何共同设计图切分、静态内存和零拷贝？

## 10. 官方学习资料

- [Hugging Face：decoder-only generation 与 Padding](https://huggingface.co/docs/transformers/v4.57.0/llm_tutorial)
- [vLLM：Engine Arguments（最新版，block size 单位为 token）](https://docs.vllm.ai/en/latest/configuration/engine_args/)
- [vLLM：PagedAttention](https://docs.vllm.ai/en/stable/design/paged_attention/)
- [vLLM：Optimization and Tuning](https://docs.vllm.ai/en/latest/configuration/optimization/)
- [vLLM：MTP speculative decoding](https://docs.vllm.ai/projects/speculators/en/latest/user_guide/algorithms/mtp/)
- [Megatron Core：Tensor Parallel Layers](https://docs.nvidia.com/megatron-core/developer-guide/0.15.0/apidocs/core/core.tensor_parallel.layers.html)
- [PyTorch：RMSNorm](https://docs.pytorch.org/docs/stable/generated/torch.nn.RMSNorm.html)
- [MIT Han Lab：AWQ](https://github.com/mit-han-lab/llm-awq)
- [ONNX Runtime：Quantization and debugging](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)
- [Megatron Core：MoE](https://docs.nvidia.com/megatron-core/developer-guide/nightly/user-guide/features/moe.html)
- [CUDA Best Practices：shared-memory banks 与 strided access](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-and-memory-banks)
- [地平线开发者文档](https://developer.horizon.auto/docs)
- [地平线／D-Robotics 模型示例库](https://github.com/D-Robotics/rdk_model_zoo)

## 11. 人工回片清单与限制

优先回看：07:25–09:00、10:15–12:00、13:00–13:55、15:00–17:30、20:35–22:15、22:55–24:30、25:10–26:25、30:20–34:00、35:51–39:38。每段要核对候选人原话、面试官提示、单位、版本、后端、shape 和指标。

本报告不判断录用结果，不推断面试官态度，不评价人格。由于没有正式 JD／职级锚点，也不提供“匹配度分数”。学习路线中的 C++、编译器、量化和端侧主题兼具补能力与补展示证据两种目的，不能倒推出这些能力当前一定缺失。

## 12. 处理记录

- 外部理解调用：1 次，`google/gemini-3.7-flash`，无重试。
- 输入：完整时长、低码率衍生视频；原片未覆盖或替换。
- 用量：231,001 tokens；费用明细仅保存在本地忽略区。
- 原始响应、响应元数据、规范化结果和 QA 均已分别保留。
- 报告未经发布或外发，当前仅位于本地工作仓库。
