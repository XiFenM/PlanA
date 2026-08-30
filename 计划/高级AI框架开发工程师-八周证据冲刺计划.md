# 高级 AI 框架开发工程师 · 八周证据冲刺计划

> - 创建日期：2026-08-08
> - 最近审阅：2026-08-29（根据全部面试复盘、PlanA 实际断点和官方岗位样本重基线）
> - Program 状态：[见唯一状态区](#program-plana-jd-ai-framework-4w)；精确学习位置只由[唯一学习断点](学习断点.md)裁决
> - 目标岗位：[本地复合 JD](<../Job Description/AI框架方向/高级AI框架开发工程师.md>) / [市场岗位需求索引](<../Job Description/AI框架方向/市场岗位需求/README.md>)
> - 诊断依据：[AMD AI 框架开发工程师胜任力诊断](../面试准备/自我准备/AMD-AI框架开发工程师胜任力诊断-2026-08-29.md)
> - 周期：8 个有效周；另设 2 个条件机动周，不按连续日历自动推进
> - 预算：每个日历周目标 18h、上限 20h，包含专项、C++/算法、英语和 Mock；八个能力单元的基线预测为 144h
> - 重心：推理与性能约 55%，AMD/Kernel/通信约 20%，训练系统素养约 10%，工程/开源/表达约 15%

---

<a id="program-plana-jd-ai-framework-4w"></a>
## Program 状态（guide-learning）

- **Program ID**：`plana-jd-ai-framework-4w`。该 ID 为稳定历史标识，不因计划延长而更改。
- **状态**：`active`。
- **前台 Lesson**：[W1「vLLM 执行链与扩展边界」](../推理框架/EP-PD自研芯片适配设计与验证包.md#lesson-plana-jd-w1-vllm-execution-boundaries)。
- **Checkpoint**：[唯一学习断点](学习断点.md)。本文件不复制精确 Pass、题目或下一动作。
- **已授权范围**：W1。W2–W10 均为候选，不因出现在计划中而自动获得授权。
- **父 Program**：[主计划](主计划.md#program-plana-ai-infra-interview-20w)。
- **返回位置**：[启动前返回快照](#161-启动前返回快照)。
- **连续推进边界**：未授予。每周验收后由用户决定继续、暂停、调整或返回主线。

候选 Lessons：

| 顺序 | Lesson ID | 能力标题 | 状态 |
|---:|---|---|---|
| 1 | `plana-jd-w1-vllm-execution-boundaries` | vLLM 执行链与扩展边界 | active |
| 2 | `plana-jd-w2-moe-ep` | MoE EP、并行策略与通信量 | candidate |
| 3 | `plana-jd-w3-pd-kv-rdma` | PD、KV 生命周期与 RDMA | candidate |
| 4 | `plana-jd-w4-validation-interview` | 定量性能、案例证据与第一次面试闭环 | candidate |
| 5 | `plana-jd-w5-pytorch-cpp-runtime` | PyTorch custom op、C++ 与异步 runtime | candidate |
| 6 | `plana-jd-w6-amd-rocm-upstream` | ROCm/HIP/RCCL 迁移与上游工件 | candidate |
| 7 | `plana-jd-w7-training-systems-literacy` | 训练框架与分布式训练系统素养 | candidate |
| 8 | `plana-jd-w8-application-closure` | 证据打包、Mock 与分层投递 | candidate |
| 9 | `plana-jd-w9-hardware-or-critical-gap` | 硬件验证或唯一关键缺口 | conditional |
| 10 | `plana-jd-w10-upstream-or-repair` | 上游 review 或未过关项修复 | conditional |

本节是本专项唯一 Program control plane。Lesson ledger 保存目标、stage 和 evidence；Checkpoint 保存唯一恢复位置；模块 `进度.md` 保存实际资料和工时。本文件的周次、清单和岗位分析只负责规划，不反向伪造完成状态。

---

## 0. 2026-08-29 修订摘要

原计划的固定源码、Change Card、A/B/C 证据等级、benchmark 纪律和硬件分支继续保留。以下内容已经重基线：

1. **四周改为八个有效周 + 两周条件机动**：原 109h/四周的净投入与实际节奏不符，且英语、Leetcode 曾被放在预算外，真实负荷不可持续。
2. **MORI 从唯一中心改为拉伸组件**：近期主目标是 AMD 上海 `87545/78999` 一类通用框架岗位；MORI/EP/PD 继续保留，但不再吞噬 C++、Kernel、ROCm、benchmark、上游和训练素养。
3. **不重启 W1**：2026-08-09 已完成的 Pass A–B 继续有效，从当前 Checkpoint 恢复。
4. **以面试失分驱动 P0**：vLLM 主链、C++/Linux、Roofline、TP/EP 手推、数字和 ownership 校准必须在前两个有效周进入验收。
5. **项目材料已成型**：[代表项目档案](../面试准备/自我准备/projects.md)已有 3+1 个故事，不再沿用“尚无成型内容”的旧判断。
6. **删除未经现有材料支持的起点假设**：不再把“KV Cache +30%”“独立手写融合 Kernel”“通信多流改单流约 10 倍”预设为已验证事实。
7. **训练改为有界目标**：本轮做到一次训练 step、显存/通信账本和并行策略选择，不展开训练 Principal 全栈。

## 1. 使用规则

这是特定岗位的临时旁路计划，不替代[主计划](主计划.md)。

- 启动、暂停和恢复以用户指令和[唯一学习断点](学习断点.md)为准。
- 一个“有效周”由验收门决定，不由星期日或日历日期决定。中断后继续同一周，不把未过关内容标为完成。
- 每个能力单元最多展开一条主源码链、一个主要证据包增量、一个定量主题和一次 Mock；sequence、账本、测试和 Case Card 可以作为同一证据包的子产物，不等于同时开启多个项目。
- 阅读、实现、测试和复述使用同一源码时只记一次真实工时。
- 每周验收后先展示产物、未过项和下一周候选，再由用户决定是否授权。
- 生产经历、面试呈现、公开可复现证据和 PlanA 学习进度分别记录，不能相互替代。
- 自研芯片内容只保留可公开的抽象能力、接口语义和脱敏结论，不写公司代码、内部 API、未公开硬件参数或原始日志。
- 没有 AMD/RDMA 环境时完成 B 级源码、设计和测试证据；不得用模拟或类比冒充实测。
- 新增真实面试时，先把复盘结论映射到风险表；只有出现新的 P0 证据，才调整后续周次。

## 2. 目标岗位与准备梯度

### 2.1 近期主目标

| 岗位 | 准备定位 | 本轮重点 |
|---|---|---|
| AMD 上海 AI Framework Eng. `87545` | 当前有条件可投 | 多模态、vLLM/PyTorch、生产代码，以及多 GPU/多节点计算、内存、通信瓶颈诊断；补 C++、可复算案例和 ROCm 迁移边界 |
| AMD 上海 AI Framework Eng. `78999` | P0/P1 补强后的进阶主投 | Linux C++、GPU Kernel、PyTorch、训练/推理、多 GPU/多机、开源协作 |
| AMD 上海 AI Software Engineer `89398` | 专项拉伸；官方 5 年以上经验构成年限筛选风险 | Large-EP、PD、分布式推理、C++/Python、LLVM/ROCm；八周只能缩小技术差距 |

### 2.2 拉伸与训练参照

- AMD `88008/81040/80979` 和本地 MORI 复合 JD：分别定义 vLLM 性能、Kernel、端到端性能和网络专项的当前拉伸标准。
- AMD `76255` 的原页面已经失效，只保留为框架/runtime 架构的历史参照，不进入当前投递队列。
- AMD `78259`、NVIDIA Megatron Core：定义训练系统的知识边界，不作为本轮职级目标。
- NVIDIA 推理和 AWS Neuron：验证 vLLM/SGLang、C++、benchmark、分布式、非 CUDA 后端和 upstream 是跨厂商共同要求。

### 2.3 八周目标

八周结束时应具备：

1. 一次 vLLM 请求的固定源码主链，能从 API 讲到 scheduler、KV、model runner 和 backend/custom op。
2. MoE EP 与 PD/KV 的状态、shape、通信量、failure 和 hardware porting 设计。
3. 一个可复算的 Roofline/benchmark 案例和三张经过数字、单位、ownership 审计的 Case Card。
4. 一个 Python → Dispatcher → C++ → device/stream/allocator → Kernel/reference 的可运行或可审查工件。
5. 一张“现有自研后端 → ROCm/HIP/RCCL”的不等价迁移矩阵；有设备时再补 A 级运行和 trace。
6. 一个真实可公开评审的 upstream 工件，不以 merge 为硬条件。
7. 一次训练 step 的显存/通信账本和 DDP/FSDP/ZeRO、TP/PP/SP/CP/EP 决策表；推理侧另覆盖 DP/replica routing。
8. 两场推理 Mock、一场训练系统 Mock，以及按 `87545/78999/Senior` 分层的投递材料。

## 3. 当前起点

### 3.1 现有材料稳定支持的优势

- 非 CUDA 加速器上的 PyTorch/vLLM 适配和模型 bring-up。
- Qwen、ERNIE、Llama、DeepSeek 及多模态/Omni 链路。
- 从端到端异常收敛到 shape、layout、访存、通信或异步依赖的跨层 Debug。
- 项目档案和面试自述中的 Conv3D、RoPE、blocked/Col-major layout、AWQ、异步 H2D/D2D 等案例。
- DeepSpeed/Megatron 与自研通信接口的阶段性接触。
- 客户部署、外部测评和跨团队闭环。

### 3.2 诊断出的 P0/P1 缺口

| 优先级 | 缺口 | 关闭方式 |
|---|---|---|
| P0 | vLLM 当前主链不能稳定脱稿呈现 | 固定 commit source map + 15 分钟白板 + 两轮追问 |
| P0 | C++/Linux 基础直接失分 | 现场编码、ELF/linking、RAII/lifetime、并发与 sanitizer |
| P0 | 性能结论缺定量模型 | 一张完整 Roofline + 三张审计 Case Card |
| P0 | TP/EP 不先固定 shape/bytes | 5 个组合题覆盖 TP/PP/DP/SP/CP/EP，并推导通信时间下界 |
| P0 | CV claim、数字和 ownership 漂移 | claim-evidence 表逐项审计 |
| P1 | HIP/ROCm/RCCL 直接证据空白 | 迁移矩阵；有设备时 build/correctness/trace |
| P1 | MoE EP、PD/KV、RDMA 设计不稳 | worked example、状态机、failure matrix、通信量模型 |
| P1 | 独立 Kernel/custom op 证据弱 | 一个小型混合栈工件和 profiler 分析 |
| P1 | 无公开 upstream | issue/reproducer/test/doc/benchmark 任一真实工件 |
| P1 | 训练只见接触、缺系统表达 | training step、显存账本、并行决策和小型验证 |

### 3.3 已有学习状态

- W1 Lesson 已完成 Pass A–B 的材料和验收收口。
- 精确恢复位置只读取[唯一学习断点](学习断点.md)，不从本节猜测或重置。
- [EP/PD 适配设计与验证包](../推理框架/EP-PD自研芯片适配设计与验证包.md)继续作为 W1–W3 的 Lesson ledger 和专项设计工件。
- 模块进度表中的 0% 表示形式化学习尚未登记，不能抹去生产经验；生产经验也不能替代本轮验收。

## 4. 证据包与验收纪律

### 4.1 核心证据包

```text
AMD AI framework readiness pack
├── diagnosis-and-market/
│   ├── competency-diagnosis
│   └── role-cards
├── inference-source-maps/
│   ├── vllm-request-kv-runner
│   ├── moe-ep
│   └── pd-kv-rdma
├── porting/
│   ├── six-layer-adaptation-matrix
│   ├── self-developed-backend-to-rocm-map
│   └── change-cards
├── implementation/
│   └── pytorch-cpp-device-harness
├── performance/
│   ├── three-audited-case-cards
│   ├── roofline-and-benchmark-packet
│   └── correctness-performance-regression
├── training/
│   ├── one-step-memory-communication-ledger
│   └── parallelism-decision-table
├── upstream/
│   └── one-reviewable-artifact
└── interview/
    ├── claim-evidence-matrix
    ├── role-specific-stories
    └── mock-records
```

目录只是逻辑结构，不要求另建代码仓库。现有长文、模块笔记、GitHub 仓库或测试目录均可承载，关键是每项有唯一事实源和链接。

### 4.2 证据等级

| 等级 | 含义 | 允许声称 |
|---|---|---|
| A | 获准环境中的真实运行、代码、测试、trace 或 benchmark | 可说明固定版本和环境已验证；公开时仍需脱敏 |
| B | 固定 commit 的源码契约、现有测试追踪、reproducer 或精确 test design | 可证明理解和设计；不能声称已在目标硬件跑通 |
| C | 类比、理论模型或尚未核实的硬件假设 | 只能标为待验证，不能据此下实现或性能结论 |

### 4.3 Change Card 模板

每个关键改造点使用同一骨架：

```text
固定仓库 / commit / 文件 / 类 / 函数
→ 现有职责、输入输出和调用契约
→ 目标后端能力或缺口
→ 保持不变 / adapter / framework core patch / 替换
→ buffer / stream / device / ownership / lifetime
→ fallback、兼容性和错误传播
→ correctness 验证
→ 单芯片 / 多芯片 / 多节点性能验证
→ 证据等级、风险和仍待确认项
```

至少形成五张：

1. vLLM request/scheduler/KV 到目标 platform/backend。
2. Fused MoE 到 EP dispatch/combine。
3. `KVConnector` 到 PD/KV transport。
4. PyTorch custom op 到 C++/device Kernel。
5. collective/stream/allocator 到 ROCm/HIP/RCCL 或目标后端。

### 4.4 Case Card 模板

```text
问题与用户影响
→ 模型 / 版本 / shape / dtype / 并发 / 环境抽象
→ 基线绝对值和测量方法
→ 正确性契约
→ 假设、反证和控制变量
→ profile / trace / counter
→ 根因和个人负责边界
→ 修改位置与协作边界
→ 优化后绝对值、相对变化和波动
→ 回归、限制和未完成项
```

首批固定为 Conv3D、blocked/Col-major layout、`projects.md` 中 Qwen3-32B/vLLM V1 的低概率 H2D/D2D 异常。第三项必须明确“最终根因仍在闭环”。奕行二面的 Host Padding 竞态另作 F2 回听卡，两者关系未确认，不能互相补证。

## 5. 时间预算与周节奏

### 5.1 有效周与日历周容量

- 每个**日历周**目标 18h、硬上限 20h；其中 2h 保留为未分配缓冲，不因落后而追赶加时。
- 一个“有效周”实质上是一个能力单元，基线预测 18h；如果验收未过，可以跨到下一个日历周继续，实际累计工时允许超过预测，但每个日历周仍不得超过 20h，并先按 §18 缩减范围。
- 少于 12h 或能力门未过时，不自动进入下一个能力单元。
- 如果真实面试临近，允许临时切换到 §17 应急路径；结束后回到原 Checkpoint。
- 八个核心能力单元的基线预测为 144h，不是保证完成所需的硬预算。W9–W10 只有明确缺口、硬件窗口或 upstream review 才启用，各按 18h 预测。

### 5.2 每个日历周投入模板

| 类型 | 目标时长 | 规则 |
|---|---:|---|
| 主源码链与一手资料 | 6h | 只追一条端到端链，不横向扩读 |
| 主要工件/实现/测试 | 4h | 每周一个可展示增量 |
| 定量推导或 benchmark | 2h | 必须落到单位、公式、数据或可执行协议 |
| C++/算法 | 2h | 每周 3–5 题，至少一题与当前系统主题相连 |
| 英语与 Mock | 2h | 英文 5 分钟陈述或一次技术追问 |
| 未分配缓冲 | 2h | 只处理真实编译、环境、源码漂移或复测 |
| 合计 | 18h | 包含所有专项活动，不再把英语/Leetcode 隐藏在预算外 |

可使用 `5 × 2h + 周末 8h`，也可按工作实际重排。每次学习结束只记录：完成证据、精确续接点、一个下一动作。

### 5.3 每周统一验收门

一个主题只有同时满足以下五层才算过关：

1. **脱稿**：先给 2 分钟全景，再完成 10–15 分钟讲解。
2. **源码**：映射固定 commit 的真实类、函数、状态和测试。
3. **推导**：至少一个 shape/bytes/latency/memory worked example。
4. **证据**：一个可运行产物、reproducer、测试、trace、benchmark 或 B 级精确 test design。
5. **追问**：Mock 中能说明假设、ownership、fallback、限制和反例。

未过门时先修缺口，不通过增加阅读量掩盖。

---

> **候选 Lesson 边界**：下列 W1–W10 是规划展开。当前只有 W1 获得授权；后续内容不构成自动启动许可。

## 6. W1：恢复 vLLM 执行链与证据基线

### 6.1 本周目标

从当前 Checkpoint 继续，不重做 Pass A–B。把工作经验中的“做过 vLLM”转换为一次可追问的固定源码主链，并启动简历 claim 与 C++ P0 校准。

### 6.2 主任务

| 顺序 | 动作 | 产出 |
|---:|---|---|
| 1 | 从[唯一学习断点](学习断点.md)恢复 W1 问答 | Lesson ledger 中的实际问答证据 |
| 2 | 追 `request → processor → EngineCoreRequest → scheduler → KV manager → model runner → attention backend` | sequence diagram、8–12 个文件 source map |
| 3 | 说明 V1 与实际 model runner/backend/fallback，以及 DP replica routing/backpressure/DPLB 的选择边界 | 运行路径指纹；无环境时交源码决策树 |
| 4 | 完成 KV block、Prefix Cache、PagedAttention 的概念与生命周期对照 | 单位严格的 KV 小账本 |
| 5 | 审计 [CV](../面试准备/自我准备/CV.md)、[projects](../面试准备/自我准备/projects.md) 和[自我介绍](../面试准备/自我准备/self-introduction.md)中的“熟悉/掌握/深入理解” | claim-evidence 矩阵首版 |
| 6 | 做 C++/Linux 基线测试：RAII、override/name hiding、ELF、shared library、ownership | 红黄绿缺口表 |
| 7 | 将 Conv3D 案例写成第一张 Case Card | shape、基线、正确性、个人职责和待核数据 |

### 6.3 资料边界

- 主读固定版本 vLLM 与[推理框架学习指引](../推理框架/学习指引.md)对应章节。
- SGLang 只做一个边界对照，不追完整 scheduler。
- 不实现 FlashAttention，不开始 MORI，不重新做已通过的架构 Pass。

### 6.4 验收门

- [ ] 15 分钟脱稿讲清主链，两轮追问无需面试官补全全景。
- [ ] source map 只有真正进入链路的 8–12 个文件，不是目录罗列。
- [ ] `messages`、sampling 参数、stream/HTTP 状态等能说明留在哪一层以及原因。
- [ ] 能说明推理 DP、replica routing、backpressure 与 DPLB 分别在哪一层工作，以及它们与 TP 的区别。
- [ ] KV 账本统一 token、element、byte、block 和 address alignment。
- [ ] Claim 矩阵至少审计 10 条，标明“已证明/需降级/待补证”。
- [ ] C++ 基线已定位具体错误，不用“工作中主要写 Python”跳过。
- [ ] Conv3D Case Card 不再只有“TTFT -40%”，能说明 workload 和仍待核对字段。

## 7. W2：MoE EP、并行策略与 C++ 系统基础

### 7.1 本周目标

把 MoE 从名词转换为 token、expert、rank、buffer 和通信量；同时关闭 XG 暴露的 C++ 基础红灯。

### 7.2 主任务

1. 用一个小 tensor 手算 `router → top-k → token count/capacity → permutation → dispatch → grouped GEMM → combine`。
2. 追当前 vLLM Fused MoE 和一条 EP 接入路径；MORI/DeepEP 只用于接口对照。
3. 分别给出单卡多专家、单机多卡和跨机 EP 数据路径。
4. 计算 2 组 All-to-All 的 per-rank bytes，并在给定有效带宽后推导理想通信时间下界和负载倾斜影响。
5. 完成 5 个组合题，覆盖 TP/PP/DP/SP/CP/EP 的 shape/collective/routing 手推；至少 1 题必须包含推理 DP 的 replica routing 或 backpressure。
6. 写一个 producer-consumer/异步 buffer lifetime C++ 练习，使用 sanitizer 或等价工具验证。
7. 完成一个小型 MatMul Roofline，并为 blocked/Col-major layout、Qwen3-32B/vLLM V1 异常建立 Case Card 草稿；奕行 Host Padding 另作 F2 回听卡，完整数据审计留到 W4。

### 7.3 产出

- EP routing worked example。
- EP source/test map 和 Change Card。
- parallelism shape/bytes 题集。
- C++ lifetime 小程序、测试与错误复盘。
- 小型 MatMul Roofline、第二/第三张 Case Card 草稿。

### 7.4 验收门

- [ ] 不看稿恢复 token 原序并验证 send count 总量守恒。
- [ ] 能区分 EP、EPLB、专家冗余和 placement 的时间尺度与作用。
- [ ] 5 个并行组合题中至少 4 题无提示正确，六类并行均被覆盖，collective 由切分推导而非背诵。
- [ ] 推理 DP 不被误写成 tensor 切分；能解释 replica 级负载、queue/backpressure 和 DPLB 观测。
- [ ] C++ 练习能解释 ownership、happens-before、析构和错误复现。
- [ ] 小型 Roofline 的 FLOPs、Bytes、Arithmetic Intensity、可达性能上界和执行时间下界单位正确。
- [ ] layout 的 `10%–20%` / `20%–30%` 冲突及 race 的未闭环状态已列入待核字段，不提前给结论。

## 8. W3：PD、KV 生命周期与 RDMA

### 8.1 本周目标

讲清 prefill 生成的 KV 如何被 decode 安全接收、消费和释放，并把 RDMA 放在正确的网络和 runtime 层次。

### 8.2 主任务

1. 追固定版本 `KVConnector` 的 scheduler/worker 边界、metadata、load/save、ready 和 cleanup。
2. 画 PULL 与 PUSH 两种状态机，标出 ownership、ack、timeout、duplicate 和 process failure。
3. 计算普通 MHA/GQA 的 per-rank KV bytes，再写出 MLA/hybrid cache 不能直接套公式的原因。
4. 比较同 TP、异 TP 重分片、DCP/PCP 对 metadata 和 bytes 的影响；首版以 P/D 相同布局为基线。
5. 建立 MR、QP、CQ、WR、doorbell、CPU proxy/GPU initiated、IB/RoCE、GPUDirect 的数据路径。
6. 给出无 RDMA、仅 host staging、仅 collective 三种 fallback。
7. 完成 PD/KV Change Card、failure matrix 和一次 15 分钟系统设计 Mock。

### 8.3 验收门

- [ ] source map 指向真实 connector 字段和测试，不用自创 toy 协议代替。
- [ ] 状态机覆盖创建、传输、ready、消费、释放、超时、重复和进程退出。
- [ ] 能从 KV bytes 和假定有效带宽推导理想传输时间下界，并说明 metadata/padding/retry 开销。
- [ ] 能解释 PD 为什么可能改善 TTFT/ITL，又为什么不保证吞吐提升。
- [ ] RDMA 与 IB/RoCE 的层级关系正确，MR/QP/CQ 职责清楚。
- [ ] 无硬件时所有性能结果保持待验证，仍有可执行 test design。

## 9. W4：定量性能、案例证据与第一次面试闭环

### 9.1 本周目标

把“会 profile”升级为“能事前建模、事中测量、事后归因”，并让三个有明确证据边界的项目案例经得起数字、反证和 ownership 追问。

### 9.2 主任务

1. 将 W2 的小型 Roofline 升级为一个 MatMul 或 Conv3D 完整案例：`FLOPs → Bytes → Arithmetic Intensity → attainable performance upper bound / execution-time lower bound → measured efficiency`。
2. 设计端到端 benchmark packet：模型、版本、shape、dtype、并发、输入/输出长度、warm-up、重复、raw data、正确性。
3. 读一条 profiler trace，区分 Host、Kernel、copy、collective、allocator 和 idle。
4. 完成 Conv3D、layout、Qwen3-32B/vLLM V1 异常三张 Case Card；第三张必须保留未闭环项，并与奕行 Host Padding F2 回听卡分开。
5. 补 BF16/FP16/FP8、opmath dtype、AWQ/W4A16 的基础推导。
6. 做第一次综合推理 Mock：vLLM 主链 + 一个性能案例 + 一个分布式题。

### 9.3 验收门

- [ ] Roofline 所有单位可复算，明确读写假设和 cache reuse 假设。
- [ ] benchmark 同时报告绝对值和相对变化，不只写提升百分比。
- [ ] 三张 Case Card 都区分“我负责/我参与/他人负责”。
- [ ] 每个成功结论至少记录一个被否定假设或负结果。
- [ ] Mock 中先固定配置和单位，不再由面试官帮助收窄问题。
- [ ] 完成面向 `87545` 的投递门槛复核；满足 §13.1 时可以边投边学。

## 10. W5：PyTorch custom op、C++ 与异步 Runtime

### 10.1 本周目标

形成一个公开可审查的混合栈锚点，把已有 backend 和 race 经验连接到 Python、Dispatcher、C++、device、stream 和 allocator。

### 10.2 主任务

1. 追一个真实 op 的 `schema → dispatcher → fake/meta → C++ registration → backend dispatch → test`。
2. 实现或整理一个最小 custom op/harness；优先与 layout、copy 或异步 lifetime 相关，不另造无关项目。
3. 明确 DeviceGuard、stream/event、allocator、storage lifetime、error propagation 和 build/ABI。
4. 用 CPU reference 与可用设备 backend 做 correctness；有 profiler 时记录 trace。
5. 将 Qwen3-32B/vLLM V1 异步 H2D/D2D 案例映射到 producer-consumer、completion 和 buffer lifetime；奕行 Host Padding 只作对照，不合并根因。
6. 完成 C++ live coding：RAII 容器、线程同步、错误处理和最小测试。

### 10.3 验收门

- [ ] Python 到 backend 的每一层都有真实文件、函数和输入输出。
- [ ] harness 可运行，或在环境受限时有完整 build/test design 和阻塞说明。
- [ ] fake/meta、device guard、stream、allocator 和 lifetime 不再只列名词。
- [ ] correctness 包含 reference、边界 shape、dtype 和失败测试。
- [ ] 能解释同步操作为何可能掩盖 race，以及如何识别观察者效应。
- [ ] C++ 现场实现可以编译、运行并通过 sanitizer/等价检查。

## 11. W6：AMD ROCm/HIP/RCCL 迁移与上游工件

### 11.1 本周目标

把非 CUDA 后端经验转换成 AMD 可评审的迁移证据，并形成一个不依赖“必须 merge”的真实上游工件。

### 11.2 主任务

1. 建立六层迁移矩阵：serving framework、platform/plugin、PyTorch backend、Kernel、communication/runtime、hardware/profiler。
2. 对照 CUDA/现有自研后端与 ROCm 的 device、stream/event、allocator、graph、wavefront/LDS、build 和 error semantics。
3. 对照 NCCL/现有通信库与 RCCL 的 ordering、progress、buffer lifetime、topology 和错误处理。
4. 有 AMD 环境时跑一个 HIP/custom op correctness、一个 rocprof trace 和一个 RCCL smoke；无环境时只交 B 级固定源码和精确测试方案。
5. 选择一个真实 upstream 选题：issue、reproducer、test、doc/error handling patch 或 benchmark。
6. 提交前做最小复现、测试、兼容性和描述；是否对外提交由当时用户授权决定，本周核心只要求可评审工件。

### 11.3 验收门

- [ ] 迁移矩阵逐项区分等价、部分等价、不等价和待确认。
- [ ] 能解释 warp/wavefront、shared memory/LDS、CUDA/HIP build 和 profiler 的关键差异。
- [ ] 无 AMD 设备时没有任何“已跑通/已提升”措辞。
- [ ] upstream 工件绑定固定 commit、现有行为、缺口、reproducer/test 和预期结果。
- [ ] 工件本地自审通过；未 merge 或未提交不等于失败。
- [ ] 完成一次英文 5 分钟“non-CUDA backend experience → ROCm migration”陈述。

## 12. W7：训练框架与分布式训练系统素养

### 12.1 本周目标

训练方向达到 L2：能画、能算、能选择、能给验证方案；不追求训练 Principal 的实现深度。

### 12.2 主任务

1. 画一次训练 step：dataloader、forward、activation、backward、gradient sync、optimizer、checkpoint。
2. 对一个小 Transformer 计算参数、gradient、optimizer state、activation 和 temporary buffer 显存。
3. 比较 DDP、FSDP/ZeRO-3 的分片对象、通信时机、峰值显存和常见 failure。
4. 比较 TP、PP、SP/CP、EP 在训练中的 shape、collective、bubble 和通信计算重叠。
5. 解释 mixed precision、loss scaling、gradient accumulation、activation checkpointing。
6. 用单机可用环境做一个小型策略 sandbox，或在受限环境完成固定源码与精确实验设计。
7. 做一场训练系统素养 Mock，问题边界控制在本节。

### 12.3 验收门

- [ ] training step 的状态和 lifetime 完整，forward 与 backward 通信不混淆。
- [ ] 显存账本有明确模型规模、dtype、batch、sequence 和假设。
- [ ] 能解释何时选 DDP、FSDP/ZeRO、TP、PP、SP/CP、EP，以及它们如何组合。
- [ ] 能从 collective bytes 和假定有效带宽估算一步通信时间下界。
- [ ] 小型验证或 test design 有 correctness 和性能观察点。
- [ ] Mock 中没有把“接触过 DeepSpeed/Megatron”扩大成完整训练所有权。

## 13. W8：证据打包、Mock 与分层投递

### 13.1 `87545` 近期投递门槛

不必等待 W8 才投递。满足以下条件即可主动投递并继续补强：

- [ ] 简历、项目、自我介绍没有已知数字冲突和 ownership 扩大。
- [ ] 能脱稿讲清 vLLM 主链和一个多模态案例。
- [ ] 至少一个性能案例可以完整复算。
- [ ] C++ 基线没有明显红灯。
- [ ] 能用一个具体配置解释多 GPU/多节点场景中的计算、内存和通信瓶颈；缺少真实多节点数据时明确证据边界。

### 13.2 `78999` 进阶门槛

在上面基础上增加：

- [ ] 一个 C++/custom op/Kernel 可运行或可审查工件。
- [ ] 一份 ROCm/HIP/RCCL 迁移矩阵。
- [ ] 一组多 GPU shape/communication 推导。
- [ ] 一个真实可公开评审的 upstream 工件。

### 13.3 本周主任务

1. 整理 readiness pack 索引，逐项链接证据和未完成项。
2. 按 `87545`、`78999`、`89398/MORI` 分别生成一页 claim-evidence 对照。
3. 校准 [CV](../面试准备/自我准备/CV.md)、[projects](../面试准备/自我准备/projects.md) 和[自我介绍](../面试准备/自我准备/self-introduction.md)；实际修改前单独确认事实口径。
4. 做两场推理 Mock：一场框架/性能，一场分布式/AMD；W7 训练 Mock 计作第三场。
5. 每场记录：问题、原答、缺口类型、修正答、证据链接和是否通过复测。
6. 准备 5 分钟中文/英文项目陈述、三个 STAR、反问问题和未知问题处理模板。
7. 根据真实岗位状态形成投递队列，不把过期岗位当作当前机会。

### 13.4 最终验收

- [ ] readiness pack 的每项 claim 都能回到 A/B/C 证据。
- [ ] 两场推理 Mock 与一场训练 Mock 完成；P0 问题复测通过率达到 80% 以上。
- [ ] 三个 STAR 均能回答 workload、baseline、root cause、ownership、result、regression 和 limitation。
- [ ] 简历技能词与实际证据一致，SGLang、ROCm、FSDP、Triton、Roofline 等不再过度表述。
- [ ] 能明确说明当前适合 `87545`、补强后适合 `78999`、Senior/MORI 仍缺什么。
- [ ] 所有未完成项进入风险表，不通过模糊措辞伪装关闭。
- [ ] 用户决定：进入投递、启用机动周、返回主计划或开启长期能力建设。

## 14. W9–W10：条件机动周

机动周不是默认第九、第十周，只允许解决已经存在的阻塞或机会。

### 14.1 W9：硬件窗口或唯一关键缺口

二选一：

- 有 AMD/RDMA 环境：补一个 HIP/custom op、rocprof trace、RCCL/MORI correctness path。
- 无硬件但某个 P0/P1 未过：只修该缺口，例如 C++ live coding、EP 手推或 benchmark，不开新主题。

### 14.2 W10：上游 review 或面试修复

二选一：

- 处理 upstream review、补测试和兼容性；不另选第二个大题。
- 根据新增真实面试复盘修复一个反复失分主题，再完成复测。

### 14.3 禁止事项

- 不为了“用满十周”继续扩读。
- 不同时开启 AMD 实验、第二个 upstream 题和完整训练框架。
- 不把等待外部 review 的时间计为学习产出。

## 15. 性能与验证规范

### 15.1 每次实验或验证方案必须记录

- 日期与结果类型：真实实测 / 模拟 / 理论推导 / 尚未验证。
- 仓库、release/tag、完整 commit SHA、本地 patch。
- CPU、加速器、NIC、节点、进程和拓扑；自研硬件只记可披露抽象。
- OS、Python、PyTorch、vLLM/SGLang、SDK/runtime、通信库版本。
- 模型、dtype、量化方式、TP/PP/DP/EP 配置。
- prompt/output 长度、batch、并发和请求到达模型。
- warm-up、正式请求数、重复次数、随机种子。
- 命令、配置、raw CSV/JSON、trace、正确性判据和失败结果。

### 15.2 指标

| 层次 | 指标 |
|---|---|
| Serving | requests/s、input/output tokens/s、goodput |
| Request | TTFT、E2E、TPOT 的 p50；样本足够时才报告 p95/p99 |
| Token interval | raw ITL 数量、请求数和聚合方式 |
| KV | bytes/request、有效带宽、等待、失败/重算 |
| EP | dispatch/combine、通信占比、expert max/mean、负载 CV |
| Kernel | time、occupancy、register/LDS、cache、memory throughput、launch/sync |
| 稳定性 | 正确率、错误/超时、峰值内存、长稳波动 |

### 15.3 对照原则

- 每次只改变一个主要变量。
- baseline 与优化版固定模型、prompt、dtype、workload、seed、长度和并发。
- 至少一次 warm-up、三次正式运行；关键结论建议五次。
- request-level p95 建议至少约 200 个 post-warmup 请求，p99 建议约 1000 个；不足时标为探索性并报告样本数。
- raw ITL 与每请求 TPOT 不是同一统计样本，必须分别报告。
- 同时报告绝对值、相对变化和跨轮波动。
- 保留负结果、反证和未解释噪声。
- 小规模结果不直接外推到 64 卡，必须附通信量和拓扑模型。
- API 名称相似不代表 CUDA/ROCm/自研 runtime 的 ordering、progress、allocator 和 stream 语义相同。

## 16. 硬件分支与返回快照

### 16.1 启动前返回快照

本表保存 2026-08-09 启动时的历史返回 capsule，不裁决当前学习位置。

| 字段 | 启动时事实 |
|---|---|
| 启动日期 | 2026-08-09 |
| 启动前模块 | PyTorch |
| 启动前断点类型 | 阶段边界 |
| 已完成内容 | Ezyang《PyTorch Internals》全文读毕，累计 9.0h；遗留 Tensor Stride、调用链和扩展问题 |
| 产出文件 | [PyTorch Internals 笔记](../PyTorch/深入学习理解PyTorch/1-Internal-Overview.md) |
| 返回位置 | PyTorch 阶段边界；专项结束后由用户决定，不默认进入 Dispatcher |

### 16.2 当前环境基线

2026-08-09 启动时确认：CUDA、CPU 可用；单机多卡、RDMA 不可用；未明确的自研芯片与 AMD 环境按不可用处理。环境变化时只更新相应 Lesson 证据，不重写历史快照。

### 16.3 有 AMD GPU、RCCL 或 RDMA

- 先确认拓扑和版本，再跑官方 correctness/smoke。
- 只选一条路径做性能：HIP/custom op、RCCL collective、MORI-EP 或 MORI-IO，不同时优化四条。
- 使用当前版本官方帮助核对 rocprof 参数，保存命令、原始数据和 trace。
- AMD 结果不能直接外推到公司自研芯片；单独记录不等价语义。

### 16.4 只有 CUDA/CPU

- 用公开 vLLM/PyTorch 路径验证状态机、测试、C++ 和 profiler 方法。
- CUDA/NCCL 只是参考实现证据，ROCm/MORI 字段保持待验证。
- 允许做可移植 harness；不为了补 AMD 证明而编造结果。

### 16.5 只有公开源码或受限环境

- 固定 commit，追真实测试、PR 和接口文档，完成 B 级设计。
- EP/PD 提供精确 fixture、输入、断言、失败路径和 bring-up 顺序。
- 性能只交理论下限、公开结果审计和可执行协议，不填写目标芯片收益。

### 16.6 有获准的自研芯片环境

- 只记录可公开抽象能力和脱敏结论。
- 按 framework → backend → Kernel → communication/runtime → hardware/profiler 分层验证。
- 选择一个信息量最高的接口做 correctness/trace；不要求一次冲刺实现完整 EP/PD。
- 不把公司内部历史工作补记为本轮学习时间。

## 17. 十个学习日应急路径

真实面试窗口少于 14 天时，使用约 36–40h 的最小闭环：

| 日 | 主题 | 最小产出 |
|---|---|---|
| D1 | 当前 Checkpoint + vLLM 主链 | request/KV/runner 白板与 source map |
| D2 | C++/Linux 红灯 | RAII、object model、ELF/library、并发基础测试 |
| D3 | Roofline 与 benchmark | 一个可复算案例、正确性和绝对基线 |
| D4 | 并行策略手推 | 5 个组合题覆盖 TP/PP/DP/SP/CP/EP 的 shape/collective/bytes/routing |
| D5 | MoE EP | routing worked example、fallback、系统设计 |
| D6 | PD/KV/RDMA | 状态机、KV bytes、failure、网络层次 |
| D7 | PyTorch/ROCm 迁移 | custom op 主链、六层 porting matrix |
| D8 | 训练最低素养 | training step、显存账本、并行决策 |
| D9 | Claim 与案例 | CV claim 矩阵、三个 Case Card |
| D10 | Mock | 框架/性能与分布式两场复测 |

应急路径停止完整 MORI、编译器深潜、第二个上游选题和完整训练框架。面试结束后回到原 Checkpoint，不把应急阅读自动标成 Lesson 通过。

## 18. 范围控制与延期规则

进度落后时按以下顺序降级：

1. 停止第二框架、第二 upstream 题、完整 Kernel 和非必要硬件实验。
2. 保留 vLLM 主链、C++、定量案例、TP/EP 手推和 claim 审计。
3. MORI 只保留 EP/PD 接口、fallback 和 test design。
4. ROCm 无硬件时降为 B 级迁移矩阵，不追求 before/after。
5. 训练只保留 step、显存账本和并行决策。
6. 未过周门时延长当前有效周，不压缩测试或伪造完成。

本轮不展开：

- 完整 SGLang scheduler、完整 TensorRT-LLM 或多个 serving 框架并行精读。
- 完整 FlashAttention、MoE Mega Kernel、EP/PD toy serving。
- 完整 LLVM/MLIR/Inductor 编译器课程。
- 完整 RDMA verbs 工程和厂商 NIC 驱动细节。
- 完整 TorchTitan/Megatron、RLHF/PPO/GRPO。
- Kubernetes/Ray/AiBrix 控制面，除非目标岗位切换到推理平台基础设施。

## 19. 仓库事实源映射

### 19.1 学习与工时

- vLLM、KV、MoE、PD 记入[推理框架/进度.md](../推理框架/进度.md)。
- collective、RDMA 和训练策略按实际内容记入[训练框架与分布式/进度.md](../训练框架与分布式/进度.md)。
- Dispatcher、custom op、PrivateUse1、allocator 记入[PyTorch/进度.md](../PyTorch/进度.md)。
- HIP/Kernel/profiler 记入[并行计算编程/进度.md](../并行计算编程/进度.md)。
- 同一份源码、实验和工时只记一次；跨模块用链接，不重复累计。
- [进度总表](进度总表.md)是周期性派生视图，不反向裁决 Lesson 或 Checkpoint。

### 19.2 职业与市场材料

- 胜任力结论以[2026-08-29 诊断](../面试准备/自我准备/AMD-AI框架开发工程师胜任力诊断-2026-08-29.md)为基线。
- 面试现场证据来自[面试问题经验目录](../面试准备/面试问题经验/README.md)。
- 简历事实以[CV.md](../面试准备/自我准备/CV.md)为真源；HTML 不单独维护事实。
- 项目故事以[projects.md](../面试准备/自我准备/projects.md)为真源。
- 市场岗位以[市场岗位需求索引](<../Job Description/AI框架方向/市场岗位需求/README.md>)和企业官方页面为准；投递前重新核对状态。

### 19.3 状态边界

- Lesson ledger 保存目标、来源、stage、evidence 和真实验收。
- Checkpoint 只保存唯一恢复位置和一个下一动作。
- 本计划只保存候选顺序、预算、工件规格和 Program 级验收。
- 下一 Lesson 未授权时，不因计划列出周次而自动推进。

## 20. 完成清单

### 20.1 核心完成

- [ ] vLLM request/scheduler/KV/model runner/backend 主链与 8–12 文件 source map。
- [ ] KV 单位账本、Prefix Cache/PagedAttention 生命周期解释。
- [ ] 推理 DP/replica routing/backpressure/DPLB 的最小源码与验收说明。
- [ ] MoE routing worked example、EP 数据路径和通信量模型。
- [ ] PD/KV 状态机、failure matrix、KV bytes 与 RDMA/fallback 图。
- [ ] 三张审计 Case Card 和一张完整 Roofline/benchmark packet。
- [ ] C++ 系统基础通过现场编码和 sanitizer/等价验证。
- [ ] 一个 Python/C++/device custom op 或 runtime harness。
- [ ] 自研后端到 ROCm/HIP/RCCL 的六层迁移矩阵。
- [ ] 一个真实可公开评审的 upstream artifact。
- [ ] 一次 training step、显存/通信账本和并行策略表。
- [ ] Claim-evidence 矩阵、三层岗位投递材料、两场推理 Mock 和一场训练 Mock。
- [ ] 用户基于证据决定投递、机动周、返回主线或长期延伸。

### 20.2 条件验证

- [ ] 有 AMD 环境时完成一个 HIP/custom op correctness 和 rocprof trace。
- [ ] 有多卡/RDMA 时完成一个 RCCL/MORI correctness path。
- [ ] 有 A 级性能环境时只选一条路径做单变量 before/after。
- [ ] upstream 工件在获得单独授权后提交 issue/PR，并按 review 补充证据。

条件不满足时保持未勾选，不影响 B 级核心完成。

### 20.3 完成后返回

Program 关闭前读取 §16.1 历史返回快照和当前 Checkpoint，由用户选择：

1. 回到 PyTorch 阶段边界；
2. 继续 AMD 长期能力建设；
3. 根据真实 offer/面试反馈切换专项；
4. 返回主计划的其他模块。

计划不得自行替用户选择返回路径。
