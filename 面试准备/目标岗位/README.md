# 上海 AI Infra 目标岗位

> 整理日期：2026-11-09。招聘信息核验日期：2026-11-09。
> 本目录保存已确认的候选范围，供后续制作针对性简历和准备面试使用。
> **核心重点目标：16 条岗位／渠道记录，含 13 条官网记录、3 条国内平台记录**，由用户于 2026-11-09 明确指定。国内记录尚未与官网 Req 建立对应关系，不能视为 16 个独立岗位或招聘名额。
> 当前保留 **12 条官方正文已核的扩展候选，另有 3 条待核线索**，见[扩展候选岗位（2026-11-09）](扩展候选岗位-2026-11-09.md)，均不进入核心重点目标。

## 1. 阅读入口与范围

- **核心重点目标、渠道与核验状态**：以本页为入口。
- **新增扩展候选**：见[扩展候选岗位（2026-11-09）](扩展候选岗位-2026-11-09.md)，同样按 A–G 分类。
- **如何选择项目、调整简历和准备面试**：见[简历与面试准备分类](简历与面试准备分类.md)。
- **个人经历基线**：[能力与经历总表](../自我准备/能力与经历总表.md)、[项目材料索引](../自我准备/projects/README.md)。[简历 W2 版本](../自我准备/过往简历/W2版本/简历-W2版本.md)保留为阶段成稿，不作为最新事实全集或通投成稿。
- **新增学习证据**：[W3 完成记录](../../计划/八周冲刺进度/W3.md)、[PD/KV Change Card](../自我准备/学习设计/ChangeCard-03-PD-KV-transport.md)。W3 的证明范围为机制理解、固定源码分析与方案／测试设计，不等于真实 RDMA 后端或生产 PD 系统已实施。

### 1.1 已确认的筛选条件

1. 地点包含上海；多地点岗位需在正式申请时选择或确认上海团队。
2. 自 2026-11-09 起，新增岗位不再限定外资，面向具有一定知名度的中大型企业及 AI 公司。以公开产品、业务、官方招聘主体及技术活动判断是否适合纳入，不虚构员工规模或把融资额当作岗位质量保证。原有 16 条记录保留为核心重点目标。
3. 主线为推理框架、模型与硬件后端集成、端到端推理性能；分布式 Runtime、ML 平台、客户技术及相邻岗位按下文分组。
4. 匹配判断依据约三年多软件开发、2024-06 起的加速器框架适配经历及仓库中的项目证据。推荐优先级不代表招聘方已经认可年限、职级或相关专业要求。

全球 Arm 与 Arm China 继续分开记录；安谋科技官网将自身描述为独立运营的合资企业，不能由品牌推断雇佣主体、管理方式或待遇相同，见[公司介绍](https://www.armchina.com/brief?dataId=61)。

### 1.2 用户明确排除

- 算子与编译器作为主要职责的岗位：不再考虑此前列出的 NVIDIA AI and DL Kernel Libraries、AMD GPU Kernel Performance Engineer、Qualcomm AI Compiler & Kernel Engineer、Arm China AI DSL Compiler Engineer。
- Zenlayer、Rakuten／乐天创研：不进入当前候选或简历制作范围。
- 字节跳动、摩尔线程、寒武纪：用户于 2026-11-09 明确移出目标范围，后续不再作为新增候选；这不表示相关岗位下线。
- 排除上述岗位不意味着删除已有 Triton、布局和算子集成经验；它们仍可作为框架与性能能力的辅助证据。

### 1.3 核验口径

- **官网正文与申请状态已核**：读取官方招聘详情，并取得申请入口或公开招聘系统状态。只说明 2026-11-09 的公开发布情况，不保证内部 HC 未冻结。
- **官网正文已核**：取得官方 JD 和地点，但没有独立确认全部申请流程。
- **官网列表已核**：官方城市列表有完整 JD，详情页内容获取受限。
- **国内列表已核、详情受限**：猎聘／BOSS 的公开企业页或职位列表可见，具体职位页触发验证码或安全验证。用户已同意纳入考虑，分类仍属暂定。

国内平台的薪资只记录平台刊登范围，不推算最终年包，不转用于同公司的其他官网岗位。同名或相似标题不足以合并渠道记录。

### 1.4 目标层级与新增分类规则

- **核心重点目标**：本页现有 16 条渠道记录。该标记表示用户的关注与准备优先级，不提升招聘信息的证据等级，也不消除详情受限或年限差距。
- **扩展候选**：扩大范围发现的新增岗位。本轮全部使用这一层级；后续新增也默认如此，只有用户明确指定才调整为核心。
- **技术分类独立于目标层级**：核心和扩展岗位均使用既有 A–G；D 继续分 D1 模型服务、D2 ML 计算、D3 训练数据与工作流，E 区分客户性能优化与开发者生态。
- **每条记录只计入一个主分类**，可保留次方向；依据实际职责和交付对象分类，不按公司、职位名称或关键词机械判断。正文未取得时标为暂定，不强行归类。
- 新增记录至少保留公司与招聘主体、具体岗位／编号／来源、上海地点依据、社招与年限信号、主要职责、匹配与缺口、核验日期／状态及目标层级。岗位身份不足或地点冲突的线索单列待核，不冒充已确认机会。
- 本页分类表中的“主投”“定向冲刺”“技术相邻”等描述准备方式与技术匹配；它们不改变用户指定的核心／扩展层级。

## 2. 分类概览

| 分类 | 招聘主要关注点 | 核心记录数 | 扩展正文已核 | 扩展待核 | 当前准备定位 |
| --- | --- | ---: | ---: | ---: | --- |
| [A．框架、模型与硬件后端集成](#category-a) | 模型接入、执行正确性、接口和回归 | 4 | [2](扩展候选岗位-2026-11-09.md#category-a) | 0 | 主投 |
| [B．端到端推理性能与模型优化](#category-b) | 性能归因、内存与吞吐／延迟改善 | 3 | [3](扩展候选岗位-2026-11-09.md#category-b) | 1 | 主投；部分岗位有年限门槛 |
| [C．分布式推理与 Runtime](#category-c) | 跨设备执行、调度、KV 传输和可靠性 | 2 | [1](扩展候选岗位-2026-11-09.md#category-c) | 1 | 定向冲刺 |
| [D．ML／LLM 平台研发](#category-d) | 模型服务、计算资源或训练数据流程 | 3 | [5](扩展候选岗位-2026-11-09.md#category-d) | 1 | 平台方向，需区分子类与补齐能力 |
| [E．客户技术优化与开发者生态](#category-e) | 客户问题闭环、性能交付和技术表达 | 2 | [1](扩展候选岗位-2026-11-09.md#category-e) | 0 | 接受客户／生态协作时重点考虑 |
| [F．云资源效率与数据平台](#category-f) | 遥测、容量、利用率和成本分析 | 1 | [0](扩展候选岗位-2026-11-09.md#category-f) | 0 | 技术相邻方向 |
| [G．HPC 工作负载与系统性能](#category-g) | CPU／并行系统与客户计算负载优化 | 1 | [0](扩展候选岗位-2026-11-09.md#category-g) | 0 | 技术相邻方向 |
| 合计 | 每条仅按主分类计数 | 16 | 12 | 3 | 核心层级与技术匹配分开 |

<a id="category-a"></a>

## 3. A：框架、模型与硬件后端集成

| 公司／岗位与来源 | 目标层级 | 地点与经验信号 | 分类依据与匹配判断 | 2026-11-09 核验状态 |
| --- | --- | --- | --- | --- |
| **Arm China — AI Framework Software Engineer**；[官方 Moka](https://app.mokahr.com/apply/armchina/885#/job/bdb82f9f-c1ab-4864-a553-d2cf459d4f6b)；职位 ID `bdb82f9f-c1ab-4864-a553-d2cf459d4f6b` | 核心重点目标 | 上海徐汇／北京／深圳；正文未写明确年限 | PyTorch/vLLM/SGLang 定制硬件 backend、模型部署、并行、异步通信、量化与融合；非 CUDA 后端接入和正确性排障经历直接相关。Triton 是辅助加分项 | 官网正文与申请状态已核；Moka 状态为 `open` |
| **NVIDIA — AI Computing Development Engineer, TensorRT and TensorRT-LLM AIGV**；[官网](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/China-Shanghai/AI-Computing-Development-Engineer--TensorRT-and-TensorRT-LLM-AIGV_JR2018990)；`JR2018990` | 核心重点目标 | 上海，另含北京／深圳；2+ 年；硕士或以上／等效经验 | 推理软件开发与性能分析，Python 或 C/C++，接受 PyTorch/SGLang/vLLM 经验；A 为主、B 为辅。需要补准 TensorRT/TRT-LLM 机制，不把已有适配经验写成该栈实战 | 官网正文与申请状态已核；Workday `posted=true`、`canApply=true` |
| **AMD — 资深 AI 框架工程师**；[猎聘职位](https://m.liepin.com/job/1978582887.shtml)；平台 ID `1978582887` | 核心重点目标 | 上海浦东；3–5 年；统招本科；刊登 35–65K·13 薪 | 暂归 A，完整职责待核。不能断定对应 AMD 96121、94063 或 96120 | 国内列表已核、详情受限；[AMD 企业页](https://m.liepin.com/company/8788043/)列出该职位，并标注用人单位自主招聘；职位详情触发验证码 |
| **NVIDIA — AI Computing Development Engineer**；[BOSS 职位](https://www.zhipin.com/job_detail/a84307b9f2699c6c03B93Ni9FldQ.html)；平台 ID `a84307b9f2699c6c03B93Ni9FldQ` | 核心重点目标 | 上海张江；3–5 年；硕士；刊登 40–70K·13 薪 | 暂归 A，B 为可能的次方向。没有官方 Req 对应证据，不能直接合并到 JR2018990，也不能用平台年限或薪资覆盖官网条件 | 国内列表已核、详情受限；[BOSS 上海 NVidia 列表](https://www.zhipin.com/zhaopin/bb1f5e26e629253b1n163d68Ew~~/)可见标题、公司和条件；详情进入安全验证，具体招聘账户未核 |

<a id="category-b"></a>

## 4. B：端到端推理性能与模型优化

| 公司／岗位与来源 | 目标层级 | 地点与经验信号 | 分类依据与匹配判断 | 2026-11-09 核验状态 |
| --- | --- | --- | --- | --- |
| **AMD — AI Software Development Eng.**；[官网](https://careers.amd.com/careers-home/jobs/96121)；`96121` | 核心重点目标 | 上海；正文未写固定年限 | vLLM/SGLang、模型架构和量化、多 GPU／多节点计算／内存／通信优化、Python/C++、上游贡献；B 为主、A 为辅。Kernel 集成不等于独立算子岗位，继续保留；实际多节点和公开贡献证据仍需补齐 | 官网正文与申请入口已核；HTTP 200、有效 JobPosting，正文注明 existing vacancy |
| **Qualcomm — Performance & Modeling Engineer**；[官网](https://careers.qualcomm.com/careers/job/446721534307)；门户 ID `446721534307` | 核心重点目标 | 上海／广东；专项 Required 写明 5+ 年 Cloud AI／LLM deployment／AI infra | Cloud AI 上 LLM/MoE/多模态接入、精度、时延、吞吐、内存及扩展性；技术重合度高，年限为拉伸。通用学历条款不能抵消专项 5+ 年要求 | 官网正文已核；HTML 内 JobPosting 可读；未独立确认整个申请流程 |
| **AMD — Agentic AI Inference Engineer**；[BOSS 职位](https://m.zhipin.com/job_detail/d7a746024c3c23ca0nJy0tW5ElJQ.html)；平台 ID `d7a746024c3c23ca0nJy0tW5ElJQ` | 核心重点目标 | 上海张江；3–5 年；硕士；刊登 35–65K，未确认薪数 | 暂归 B，并保留 C 标签；列表提及 SGLang/vLLM 源码、模型、并行、调度与 KV cache。不能仅凭 Agentic 判定为 Agent 应用开发，也不能在详情未核时确认各项工作占比 | 国内列表已核、详情受限；[BOSS inference 列表](https://m.zhipin.com/zhaopin/244ab8270a7c493a1nN73NS_EA~~/)可见，详情进入安全验证；尚无官网 Req 对应关系 |

<a id="category-c"></a>

## 5. C：分布式推理与 Runtime

| 公司／岗位与来源 | 目标层级 | 地点与经验信号 | 分类依据与匹配判断 | 2026-11-09 核验状态 |
| --- | --- | --- | --- | --- |
| **AMD — AI Framework Engineer**；[官网](https://careers.amd.com/careers-home/jobs/94063)；`94063` | 核心重点目标 | 上海；正文未写固定年限，偏好实际分布式推理优化经验 | PD disaggregation、Large-EP、RL、vLLM/SGLang、多 GPU／多节点及 C++/Linux；重点准备具体功能接入、接口约束和性能取舍。W2/W3 有帮助，但学习设计不能替代设备实测 | 官网正文与申请入口已核；HTTP 200、有效 JobPosting，正文注明 existing vacancy |
| **AMD — AI Framework and Performance Experts(vLLM)**；[官网](https://careers.amd.com/careers-home/jobs/96120)；`96120` | 核心重点目标 | 上海；正文定位 senior member，未写固定年数 | 生产级单机／分布式 Runtime、TP/PP/EP、KV 与 Token 调度、RCCL/RDMA、上游及客户 PoC；相比 94063 更看重完整系统架构、可靠性和长期所有权，属于明显拉伸 | 官网正文与申请入口已核；HTTP 200、有效 JobPosting，正文注明 existing vacancy |

<a id="category-d"></a>

## 6. D：ML／LLM 平台研发

| 公司／岗位与来源 | 目标层级 | 地点与经验信号 | 子方向与匹配判断 | 2026-11-09 核验状态 |
| --- | --- | --- | --- | --- |
| **Cadence — Leader software engineer for jedai LLM-infra**；[官网](https://cadence.wd1.myworkdayjobs.com/External_Careers/job/SHANGHAI/Leader-software-engineer-for-jedai-LLM-infra_R50616)；`R50616` | 核心重点目标 | 上海；相关专业硕士 +3 年／本科 +5 年 | **D1 模型服务平台**：Python/C++、容器／微服务、分布式、性能和 SQL，涉及 LangChain/NIM/Spark 等工具；现有模型交付较可迁移。Leader 标题不直接解释为人员管理岗 | 官网正文与申请状态已核；Workday `posted=true`、`canApply=true` |
| **Optiver — Senior Machine Learning Engineer**；[官网](https://www.optiver.com/join-us/jobs/technology/shanghai/senior-machine-learning-engineer/)；官网 jobid `8371647002` | 核心重点目标 | 上海；未写硬性年限，但要求生产 ML Infrastructure 经验 | **D2 ML 计算平台**：CPU/GPU 集群效率、ML／仿真计算平台、profiling、容器、分布式训练与存储；性能工程可迁移，大规模集群与平台所有权为缺口 | 官网详情、上海列表和 Apply 入口已核 |
| **Unity — Senior Machine Learning Engineer, ML Infrastructure**；[官网](https://unitytech.wd1.myworkdayjobs.com/Unity/job/Shanghai-China/Machine-Learning-Engineer--ML-Infrastructure_JOBREQ-2616269-1)；`JOBREQ-2616269` | 核心重点目标 | 上海；未写具体年数，要求较深的平台经验与架构推动能力 | **D3 训练数据与 ML 工作流**：当前 JD 为 offline 平台，涉及 Ray Data/Train、PyTorch、Spark/Flink、Flyte/Airflow；不能套用第三方旧版 Online JD。训练数据管线和编排证据不足 | 官网正文与申请状态已核；Workday `posted=true`、`canApply=true` |

<a id="category-e"></a>

## 7. E：客户技术优化与开发者生态

| 公司／岗位与来源 | 目标层级 | 地点与经验信号 | 子方向与匹配判断 | 2026-11-09 核验状态 |
| --- | --- | --- | --- | --- |
| **NVIDIA — Developer Technology Engineer – AI**；[官网](https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/China-Shanghai/Developer-Technology-Engineer---AI_JR2026261)；`JR2026261` | 核心重点目标 | 上海，另含北京／深圳；2+ 年；硕博／相关专业 | **客户工作负载优化**：AI/HPC 加速、C/C++、软件设计、客户技术协作；客户部署、复现和跨团队排障经历相关。仍有编码与加速计算要求，不是纯售前或沟通岗 | 官网正文与申请状态已核；Workday `posted=true`、`canApply=true` |
| **Arm — Senior Developer-Relations Engineer (AI)**；[官网](https://careers.arm.com/job/shanghai/senior-developer-relations-engineer-ai/33099/100996071312)；`2026-17483` | 核心重点目标 | 上海／深圳；未写明确年限 | **开发者生态与技术表达**：端侧模型优化、runtime、全栈 profiling、Python/C++，以及技术指南、白皮书、demo、演讲与合作；需要确认愿意承担公开技术传播工作，并补真实内容成果 | 官网详情可读，Apply 入口可见 |

<a id="category-f"></a>

## 8. F：云资源效率与数据平台

| 公司／岗位与来源 | 目标层级 | 地点与经验信号 | 分类依据与匹配判断 | 2026-11-09 核验状态 |
| --- | --- | --- | --- | --- |
| **Microsoft — Software Engineer II／2, GPU COGS/Efficiency**；[申请入口](https://apply.careers.microsoft.com/careers/job/1970393557052841)；门户 ID `1970393557052841` | 核心重点目标 | 上海／苏州；3+ 年软件工程 | GPU 资源利用率、telemetry、成本模型、数据管线与可靠性；应突出数据质量平台和效率分析，不以模型或 GPU kernel 开发为主 | 官网列表已核；[官方上海城市页](https://careers.microsoft.com/v2/global/en/locations/shanghai.html)含完整 JD、地点和年限；详情地址只返回前端配置，不记为详情全文已核 |

<a id="category-g"></a>

## 9. G：HPC 工作负载与系统性能

| 公司／岗位与来源 | 目标层级 | 地点与经验信号 | 分类依据与匹配判断 | 2026-11-09 核验状态 |
| --- | --- | --- | --- | --- |
| **Intel — HPC and Financial Workload Optimization Engineer**；[官网](https://intel.wd1.myworkdayjobs.com/External/job/PRC-Shanghai/HPC-and-Financial-Workload-Optimization-Engineer_JR0288445)；`JR0288445` | 核心重点目标 | 上海；Experienced Hire，未写固定年限；接受数学等相关硕士 | C/C++、Python、Linux、MPI/OpenMP，HPC／金融计算与客户性能优化，SYCL/CUDA 加分；数学背景和性能分析可迁移，MPI/OpenMP 与 HPC 应用实操需要单独准备 | 官网正文与申请状态已核；Workday `posted=true`、`canApply=true` |

## 10. 渠道覆盖与去重

2026-11-09 的研究使用了公司官网、Workday／Moka 等公开招聘数据，以及 LinkedIn、猎聘、BOSS、前程无忧和招聘聚合站。国内平台仅覆盖公开可访问内容，没有登录后完整检索或招聘方确认；未命中不能解释为该公司没有岗位。

- 核心重点目标中的国内渠道仅包含用户指定的 **AMD 猎聘资深 AI 框架、AMD BOSS Agentic AI Inference、NVIDIA BOSS AI Computing**；后续国内渠道发现的岗位按扩展候选单独整理。
- 合并记录需要官方 Req、招聘者确认或足够明确的同岗位证据。当前不把国内三条直接对应到相似官网标题。
- 招聘品牌、岗位技术栈与实际雇主分别核对。“高通平台”“微软技术相关”不自动等于 Qualcomm 或 Microsoft 直招。
- 官网与平台年限冲突、地点变更、正文／列表不一致时保留差异，投递前复核，不能选择较宽松的一侧覆盖另一侧。

## 11. 历史记录与后续维护

- 本页保存 2026-11-09 的核验快照，不把相对更新日期或搜索抓取时间当作公司首次发布日期。
- 旧资料中的 AMD `87545`、`78999`、`89398` 在 2026-11-09 的官网详情返回 404，未列入上述 16 条记录；这不推断团队停止招聘，也不改写旧研究文档。
- 后续复核时记录具体日期、渠道与变化原因；只有岗位身份确定后才合并渠道，保留原入口及核验历史。
- 后续岗位继续归入 A–G，不因为扩大企业范围新增一套平行分类；核心层级只有在用户明确指定时调整。
- 简历制作按[分类文档](简历与面试准备分类.md)选择证据。岗位进入考虑范围不代表已投递、已联系招聘者或已经完成简历。
