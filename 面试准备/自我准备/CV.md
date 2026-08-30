# xxx

> 本文件是简历内容的唯一真源；`CV.html` 仅为可视化版本，不单独维护事实口径。

- **手机**：
- **邮箱**：
- **求职方向**：模型部署 / LLM 推理框架优化 / AI 框架性能优化

---

## 个人概述

- 具备 3 年以上软件开发经验，近 2 年专注国产非 CUDA 架构加速芯片上的大模型部署、推理框架适配和性能优化，长期工作在 `PyTorch`、`vLLM`、通信库与高性能算子的交叉层。
- 具备 `vLLM` 源码级二次开发经验，参与 Qwen、Llama、DeepSeek、Ernie 等模型及多模态、Omni 模型的端到端适配，能够从模型执行链路定位到算子、通信库和运行时。
- 擅长以 Profile、算子级对比、控制变量实验和 Replay 回归定位性能及精度问题，能够处理异步拷贝竞态、混合精度误差、内存排布、跨卡通信和硬件稳定性等复杂问题。
- 具备跨团队交付经验，可协同模型、算子、通信、运行时、硬件及云服务团队完成模型上线、客户支持和第三方测评。

## 专业技能

### 推理框架与模型部署

- **框架开发**：深入理解 `vLLM` 模型执行、调度、KV Cache 与 PagedAttention 等核心机制，具备 V0/V1 框架适配、模型接入、功能扩展、性能分析和稳定性调试经验；熟悉 `SGLang` 的 RadixAttention、结构化输出与调度机制。
- **推理优化**：掌握 Continuous Batching、Chunked Prefill、Prefix Cache、Speculative Decoding、PD 分离、量化和多模态推理等技术，能够围绕 TTFT、TPOT、吞吐、显存和并发扩展性设计优化方案。
- **模型架构**：熟悉 Qwen、Llama、DeepSeek、Ernie 等主流模型，以及 MHA/MQA/GQA/MLA、RoPE/M-RoPE、MoE、MTP 等关键结构；有图像、视频、语音等多模态模型部署经验。

### PyTorch 与分布式系统

- **PyTorch Internals**：理解 Tensor、Storage、Stride、Dispatcher、Autograd、Caching Allocator 和 `PrivateUse1` 后端接入机制，具备自定义算子注册、数据拷贝链路和框架级调试经验。
- **分布式训练与推理**：熟悉 `DeepSpeed`、`Megatron-LM`、FSDP 等框架，理解 ZeRO、Tensor Parallel、Sequence Parallel、Pipeline Parallel、Expert Parallel 等并行策略及其通信时序。
- **集合通信**：理解 Ring/Tree AllReduce、ReduceScatter、AllGather 等集合通信算法，具备自研通信后端的接口适配、精度排查、同步语义分析和多卡性能定位经验。

### 高性能计算与工程能力

- **算子开发**：具备自研加速芯片 Kernel 开发和调优经验，理解线程组织、存储层次、访存合并、Double Buffer、软件流水线、算子融合和数值稳定性；熟悉 `Triton`、`TileLang` tile级编程及 FlashAttention 实现原理。
- **性能分析**：能够使用框架 Profiler、Trace、Nsight Systems/Compute 和 Roofline 方法拆解端到端瓶颈，区分 Host 调度、计算、访存、通信与框架开销，并建立可重复的 Benchmark 和回归测试。
- **软件工程**：熟练使用 Python、C/C++、Linux、Git 和 Bash，具备跨仓库开发、CI 测试、问题复现、技术文档及客户交付环境建设经验。

## 工作经历

### 中昊芯英/上海泰则 | AI 框架开发工程师

*2024年06月 - 至今*

- **推理框架与模型适配**：负责 `vLLM`、`PyTorch` 在自研加速芯片上的适配和演进，完成 Qwen2.5/3-VL、Ernie4.5-VL、Qwen3-Omni、Llama、DeepSeek 等模型的功能接入、精度对齐、性能调优与部署支持，覆盖文本、图像、视频和语音链路。
- **多模态链路优化**：统一多模态 Fused Rotary Embedding 接口，推进 M-RoPE、tile级 Col-major Matmul等框架能力；通过异构调度、内存排布调整和算子融合减少 Host-Device 拷贝及非连续访存。
- **算子与端到端性能优化**：围绕 Conv3d、RoPE、Matmul、Attention 等热点开展 Profile、形状分析、调度调整和算子组协同；在 Qwen3-VL 链路完成 Conv3d 优化与验证，显著降低显存占用并使首 Token 延迟下降 **40%**。
- **客户模型部署**：负责 ECG 多模态模型的环境搭建、重复输出问题修复和端到端性能优化，通过 Col-major Matmul、热点算子优化与服务链路调整，将端到端推理耗时从 **40 秒以上降低至 10–15 秒**，并交付云服务部署。
- **复杂精度与稳定性调试**：针对 `vLLM V1` 异步 H2D/D2D 拷贝引发的低概率精度异常，建立全链路控制开关、统一 Replay、Copy/Consumer Trace、回读校验和分层控制变量实验，将随机问题逐步收敛至高风险拷贝与运行时可见性路径，目前根因闭环中。
- **分布式生态适配**：参与 `DeepSpeed ZeRO-3`、`Megatron-LM Tensor Parallel` 与自研通信库适配，定位并修复数据类型、Padding、ReduceScatter、AllGather、Broadcast、同步和流语义相关问题，将关键用例纳入 CI。
- **测评与跨团队交付**：对接支撑信通院国测、上海 AI Lab、绛溪实验室等外部测评，负责环境、流程、精度验证、性能分析和问题闭环；协同算子、通信、运行时、硬件、销售及云服务团队，将模型侧问题转化为可复现 Case 和可执行的优化需求。
- **工程沉淀**：建设 Profile Point、模型压测与异常分析工具，沉淀 Col-major Matmul 流程和模型压测文档；完成 Col-major Matmul 相关专利申请并获受理。

### 国药控股数字科技 | 助理架构师

*2023年04月 - 2024年04月（其中 2023年04月 - 2023年06月为实习）*

- 参与数据质量监控平台建设，打通数据入湖、质量规则、异常监控和可视化链路，并开发数据看板解析工具辅助指标血缘追踪与异常定位。

## 教育背景

### 复旦大学 | 硕士 | 应用统计（大数据学院）

*2021年09月 - 2023年06月*

- **研究方向**：图深度学习与强化学习智能体
- **相关课程**：机器学习及神经网络导论、数据挖掘、社交网络分析、时间序列分析
- **GPA**：3.5 / 4.0

### 上海大学 | 学士 | 数学与应用数学（理学院）

*2017年09月 - 2021年06月*

- **相关课程**：程序设计（C/C++）、数据结构与算法、概率论与数理统计
- **荣誉奖项**：学业优秀一等奖学金
- **GPA**：3.4 / 4.0
