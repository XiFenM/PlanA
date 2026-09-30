# 代表项目档案

> 本目录用于沉淀面试项目故事，每个项目一个文件。项目内容按“项目背景—职责—关键行动—量化结果—面试深挖点”组织；涉及性能数据时，仅保留已确认可以对外披露的口径。

## 文件索引

| 文件 | 项目 |
|---|---|
| [multimodal-inference-project.md](multimodal-inference-project.md) | 项目一：多模态大模型推理框架适配与性能优化（含 Conv3D） |
| [ECG-project.md](ECG-project.md) | 项目二：ECG 多模态模型部署与端到端性能优化 |
| [vLLM-V1-async-H2D-project.md](vLLM-V1-async-H2D-project.md) | 项目三：vLLM V1 异步拷贝低概率精度异常专项 |
| [DeepSpeed-Megatron-project.md](DeepSpeed-Megatron-project.md) | 备选项目：DeepSpeed、Megatron-LM 与通信后端适配 |
| [GLM5-3-flash-project.md](GLM5-3-flash-project.md) | 新项目：GLM-5.3-Flash 推理适配（进行中） |
| [project-template.md](project-template.md) | 新项目模板：复制为 `<项目名>-project.md` 后填写，并在本表登记 |

<a id="project-overview-3-plus-1"></a>
## 3+1 项目总览

> 前四个项目（3 个主打 + 1 个备选）均已完成第一次无稿口述，但“口述完成”不等于事实和数字已经核验；GLM-5.3-Flash 是进行中的新项目，口述基线仍是待本人复述的初稿。下表只汇总面试定位、当前最强证据和最需要关闭的未知字段；具体事实继续由各项目正文及其“待核验字段”维护。

| 项目 | 面试定位 | 当前最强证据 | 首要未知字段 | 主要收口位置 |
|---|---|---|---|---|
| [多模态推理与 Conv3D](multimodal-inference-project.md#project1-oral-baseline-20260902) | 主打：非 CUDA 框架适配、跨层定位和物理布局 | 从 OOM 追到 channels-last 小末维 Padding，并完成模型侧布局重构、算子协作和两级验证 | 准确模型版本、显存账本、逻辑/物理布局契约、性能口径与收益拆分 | W1 建立 Case Card；W4 完整审计 |
| [ECG 与 blocked Col-major](ECG-project.md#project2-oral-baseline-20260902) | 主打：客户模型交付、Profile、Roofline 和权重预排布 | 经过 Host、融合和小 Shape 优化后，以 Roofline 判断继续处理权重访存，并在加载期完成布局预排布 | 实际运行栈、端到端 Workload、Roofline 读写假设、布局冲突层级和各项优化收益 | W2 形成草稿；W4 完成 Roofline 与 Case Card |
| [vLLM V1 异步 H2D](vLLM-V1-async-H2D-project.md#project3-oral-baseline-20260902) | 主打：低概率精度问题、控制变量和异步时序 | 从观察者效应和阻塞对照定位异步路径，说明 CPU Padding 到设备消费之间的依赖缺口，并完成现场请求集回归 | 准确版本与配置、首个分叉证据、修复前对照、底层修改 Ownership 与披露范围 | W4 完成 Case Card；W5 深化异步 Runtime 机制 |
| [DeepSpeed、Megatron-LM 与通信后端](DeepSpeed-Megatron-project.md#project4-oral-baseline-20260903) | 备选：分布式训练、通信语义和硬件感知调度 | 通过 Profile 发现多 Stream 没有形成有效 Overlap，反而拆分提交批次；以可回退的单 Stream 方案完成验证 | 两套训练框架的实际范围、并行配置、Loss 对齐、多 Collective 正确性和性能口径 | W7 完成训练证据与专项 Mock；W8 纳入最终叙述 |
| [GLM-5.3-Flash 推理适配](GLM5-3-flash-project.md) | 进行中：新模型结构的框架接入、混合 KV cache 与状态管理、Profile 驱动的插件侧优化 | 修正混合 KV cache 的分组与容量核算，解决两次 OOM；定位非连续状态页引发的 host 逐元素搬运并拆池，完成单测与真机对照 | 端到端精度对齐、统一条件下的最终性能、多并发与长序列稳定性、版本脱敏标识，以及本人复述确认 | 项目完成后按统一条件补测；计划周次未定 |

### 共性未知字段

- **版本与 Workload**：模型、框架提交、硬件抽象、Shape、数据类型、并发或并行配置。
- **量化口径**：绝对基线、相对变化、计时边界、预热、重复次数、统计方式和原始记录。
- **正确性**：参考实现、误差容差、Loss 或输出判据、边界输入、稳定性和回归范围。
- **因果证据**：初始假设、被否定的解释、控制变量，以及修改与结果之间的最小充分关系。
- **Ownership**：我负责、我参与、其他团队负责，以及代码、方案、验证和上线分别由谁完成。
- **披露边界**：客户信息、内部硬件能力、实现细节和性能数据是否能够用于简历或面试。
