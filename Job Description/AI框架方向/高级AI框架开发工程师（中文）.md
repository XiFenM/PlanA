# 岗位介绍（THE ROLE）

你将在推动**高性能大语言模型（LLM）推理服务**方面发挥关键作用，通过优化 GPU 网络通信、推理基础设施、GPU Kernel，以及单机和多机环境下的分布式执行策略，提升大模型推理系统的整体性能。

**岗位：** 软件工程师 / 系统工程师<br>
**团队：** GPU Networking & Inference Infrastructure Team<br>
**所属方向：** ROCm System Software — Communication Primitives（通信原语）

---

# 项目介绍（About the Project）

**MORI（Modular RDMA Interface）** 是一个开源框架，为 AMD GPU 上的大规模 LLM 推理提供高性能 GPU 通信能力。

它为以下场景提供 **RDMA + GPU Direct 网络通信层**：

- MoE（Mixture of Experts，混合专家模型）的 **Expert Parallelism，专家并行**
- SGLang 和 vLLM 中的 **Prefill / Decode 解耦**
- 高性能分布式推理中的 GPU 间数据传输

此外，MORI 还通过 **MORI-UMBP（Unified Memory & Bandwidth Pool，统一内存与带宽池）** 提供 KV Cache 的管理与存储能力。

MORI 在 **SemiAnalysis InferenceX v2** 测评中取得了业界领先（State-of-the-Art）的结果。

---

# 你将负责的工作（What You'll Work On）

## 1. 推理框架集成（Inference Framework Integration）

负责将 MORI 的通信原语完整集成到 **SGLang 和 vLLM** 中，包括：

- Python Operator API
- 在 MoE Forward 中集成 **MORI-EP dispatch / combine**
- 在 KV Cache 传输流水线中集成 **MORI-IO**

你将负责从底层通信组件一直到推理框架上层 API 的端到端集成。

---

## 2. MORI-UMBP

将**分层式 KV Cache 存储（Tiered KVCache Storage）**以及**分布式 Key-Value 访问能力**集成到 LLM 推理服务系统中。

这可能涉及：

- GPU HBM
- CPU 内存
- 远程内存 / 远程节点

等不同层级之间的 KV Cache 管理和访问。

---

## 3. Prefill / Decode 解耦（PD Disaggregation）

将 **MORI-IO** 集成到 Prefill / Decode 路径中，通过 **GPU Direct RDMA** 实现高吞吐量的 KV Cache 数据传输。

目标是在 Prefill 节点和 Decode 节点之间高效传递 KV Cache，从而实现解耦式 LLM Serving。

---

## 4. Expert Parallelism（EP，专家并行）

负责将 **MORI-EP** 集成、提交并长期维护在 SGLang 和 vLLM 中。

工作范围包括：

- Scheduling 调度
- Routing 专家路由
- EPLB（Expert Parallel Load Balancing，专家并行负载均衡）

并支持诸如 **DeepSeek V3** 这样的 MoE 模型，在 **8～64 张 GPU** 环境下运行。

---

## 5. MORI-SHMEM

负责集成和维护 MORI 的**对称内存运行时（Symmetric Memory Runtime）**。

该 Runtime 是整个 MORI 系统的基础设施，负责：

- 对称 GPU 内存分配
- RDMA Transport 初始化
  - InfiniBand（IB）
  - AINIC
  - Broadcom Thor2
- P2P / XGMI 地址转换
- 为 GPU Kernel 管理 Device-side State
- 通过 **MORI-IR bitcode** 为 GPU Kernel 提供底层运行时能力

---

## 6. 性能 Benchmark（Performance Benchmarking）

设计并执行端到端 LLM 推理性能测试。

关注指标包括：

- **Throughput：吞吐量**
- **TTFT（Time To First Token）：首 Token 延迟**
- **ITL（Inter-Token Latency）：Token 间延迟**

测试场景包括：

- Expert Parallelism
- Prefill / Decode Disaggregation
- 不同 GPU 数量和多机配置

并根据 Profiling 数据持续定位性能瓶颈和推动优化。

---

# 任职要求（Qualifications）

## 必须具备（Required）

### 1. 熟悉至少一种主流 LLM 推理框架

例如：

- SGLang
- vLLM
- TensorRT-LLM
- 或类似系统

需要深入理解其中的核心模块，例如：

- Scheduler 调度器
- Attention Backend
- KV Cache Manager
- Distributed Execution Engine 分布式执行引擎

---

### 2. 深入理解 LLM Serving

需要熟悉：

- MoE Expert Parallelism
- Prefill / Decode Disaggregation
- KV Cache Reuse
- Tensor Parallelism（TP，张量并行）
- Pipeline Parallelism（PP，流水线并行）
- Sequence Parallelism（SP，序列并行）

---

### 3. 扎实的 C++ 和 Python 能力

能够熟练在以下技术混合的代码库中开发：

- C++
- HIP
- Python
- PyTorch Custom Operator / Extension

---

### 4. 大型开源项目贡献经验

具备参与大型开源项目的经验，包括：

- 向上游提交 PR
- Code Review
- 与其他团队 / Maintainer 协作
- 推动功能合并进入上游项目

---

# 加分项（Nice to Have）

## RDMA

了解 RDMA 核心概念，例如：

- Verbs API
- Queue Pair（QP）
- Completion Queue（CQ）
- Memory Registration
- GPUDirect Async / IBGDA

---

## 集合通信

熟悉以下集合通信库：

- NCCL
- RCCL
- MPI

以及它们如何集成到大型分布式计算 / 推理系统中。

---

## GPU 集群网络拓扑

理解 GPU Cluster 的通信拓扑，例如：

### 节点内部：

- XGMI
- NVLink

### 节点之间：

- InfiniBand
- RoCE

并理解这些拓扑如何影响 **MoE All-to-All** 等通信模式的性能。

---

## NIC 生态

熟悉不同厂商的高速网络设备和用户态驱动生态，例如：

- NVIDIA / Mellanox ConnectX
- AMD Pollara / AINIC
- Broadcom Thor2

---

## 性能分析工具

有网络瓶颈型 workload 的 profiling 经验，例如使用：

- rocprofv3
- Perfetto
- ibstat
- perfquery

---

## AMD GPU / ROCm

具备以下经验之一：

- ROCm
- hipcc
- AMD GPU Architecture

---

# 这个岗位的独特之处（What Makes This Role Unique）

你将负责连接两个关键世界：

**底层 GPU 网络通信基础设施 MORI**

与

**运行万亿参数级模型的上层 LLM 推理框架**

之间的桥梁。

MORI-EP 和 MORI-IO 已经被合入 **SGLang 和 vLLM**，因此你开发的功能会直接进入：

- 开源社区
- 实际生产环境

团队本身拥有非常深入的：

- RDMA
- GPU Kernel

技术积累，因此你可以主要专注于**推理系统层面的性能影响**，同时向真正构建这些底层网络组件的工程师学习 GPU 网络通信技术。

你的工作会同时涉及：

- GPU Kernel
- Inference Runtime
- 分布式执行策略
- 单机多 GPU 系统
- 多机多 GPU 系统

---

这个岗位高度聚焦于 **LLM Inference Stack**，包括：

- vLLM
- SGLang
- 内部推理平台

你将在以下几个领域的交叉点上工作：

**模型架构 × GPU Kernel × 编译器 × 分布式系统**

并与：

- AMD 内部 GPU Library 团队
- 上游开源社区

紧密合作，交付达到生产级标准的性能优化。

你的工作将直接影响 AMD GPU 上最先进 LLM 的：

- 吞吐量（Throughput）
- 延迟（Latency）
- 扩展能力（Scalability）
- 成本效率（Cost Efficiency）

---

# 我们希望你是这样的人（THE PERSON）

你是一名具有深厚 LLM 领域知识的**资深系统工程师**。

你喜欢深入底层系统进行开发，同时又能保持对整个端到端 LLM 推理系统的理解。

你能够熟练分析：

- Attention
- KV Cache
- Batching
- 并行策略
- GPU Kernel
- GPU 硬件特性

以及这些因素之间的映射和相互影响。

你能够适应具有较大不确定性的技术问题，独立确定技术方向，并持续交付**可量化的性能提升**。

同时，你不仅具有很强的工程执行能力，也能够与上游开源社区进行高质量协作，并始终保持较高的软件工程质量标准。

---

# 核心职责（KEY RESPONSIBILITIES）

## 1. 优化 LLM 推理框架

针对 AMD GPU，推动以下推理框架的性能优化：

- vLLM
- SGLang
- PyTorch

既包括 AMD 内部代码，也包括向开源上游提交优化。

---

## 2. 面向 LLM 的 GPU Kernel 开发

设计和优化 LLM 推理关键路径上的 GPU Kernel，包括：

- Attention
- GEMM
- KV Cache 操作
- MoE 相关组件
- Memory-bound Kernel

---

## 3. 大规模分布式 LLM 推理

设计、实现和调优多 GPU、多节点推理策略，包括：

- TP / PP / EP 混合并行
- Continuous Batching
- KV Cache Management
- Disaggregated Serving

目标是在大规模 GPU Cluster 上获得更好的性能和扩展性。

---

## 4. 模型与系统协同设计（Model-System Co-Design）

与模型团队和推理框架团队合作，使 LLM Architecture 与面向硬件的优化策略相匹配，从而提升真实生产环境中的推理效率。

---

## 5. 编译器与 Runtime 优化

利用编译器技术优化 GPU Kernel 和整个推理流水线，包括：

- LLVM
- ROCm
- Triton
- Graph Compiler

重点优化：

- Kernel Fusion
- Memory Access Pattern
- End-to-End Inference Pipeline

---

## 6. 端到端推理流水线优化

优化整个 LLM Serving Stack，包括：

- Model Execution Graph
- Runtime
- Scheduling
- Batching
- Deployment

而不仅仅关注某一个独立 Kernel 的性能。

---

## 7. 开源技术领导力（Open-Source Leadership）

与开源 Maintainer 深度合作：

- 向上游提交优化
- 参与和影响项目 Roadmap
- 推动优化进入主干
- 保证提交代码长期可维护

---

## 8. 工程卓越性（Engineering Excellence）

遵循高质量的软件工程实践，包括：

- 性能 Benchmark
- 测试
- Debugging
- Profiling
- 大规模系统可维护性

---

# 优先考虑的经验（PREFERRED EXPERIENCE）

## 1. 扎实的 LLM 知识

深入理解大语言模型推理，包括：

- Attention Mechanism
- KV Cache 行为
- Batching Strategy
- Latency / Throughput Trade-off

---

## 2. LLM 推理框架经验

具有实际使用和优化以下系统的经验：

- vLLM
- SGLang
- FasterTransformer
- 或其他类似推理系统

并具有明确的性能调优经验。

---

## 3. GPU Kernel 开发

具有深度学习 Workload 的 GPU Kernel 性能优化经验，尤其是 LLM 推理关键路径上的 Kernel。

---

## 4. 分布式推理系统

具有设计和调优多 GPU、多节点大规模推理系统的经验。

---

## 5. 开源贡献

在以下领域的大型开源项目中有实质性贡献记录：

- Machine Learning
- LLM
- 系统软件
- HPC

---

## 6. 编程与 Debug 能力

精通：

- Python
- C++

并具有丰富的：

- Performance Analysis
- Profiling
- Debugging

复杂系统的经验。

---

## 7. 高性能计算（HPC）

具有在**异构 GPU 集群**上运行和优化大规模 Workload 的经验。

---

## 8. 编译器与系统背景

具有扎实的编译器理论和工具基础，例如：

- LLVM
- ROCm
- Triton

并能够将这些技术应用于：

- ML Kernel 优化
- Runtime 优化
- 推理性能优化

---

# 学历要求（ACADEMIC CREDENTIALS）

计算机科学、计算机工程、电子工程或相关专业的：

- **硕士**
- 或 **博士**

学历。
