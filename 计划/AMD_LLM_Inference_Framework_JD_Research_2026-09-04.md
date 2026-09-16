# AMD 大模型推理框架工程师：JD 深度研究与面试准备手册

> 研究日期：2026-09-14<br>
> 文档用途：岗位判断、投递定位、技术复习、面试准备、开源贡献、与招聘方沟通<br>
> 研究对象：用户提供的“AMD 大模型推理框架工程师”非正式内推截图<br>
> 个人化依据：已知的 PyTorch 分布式、ProcessGroupDLCCL、集合通信、vLLM custom allreduce、CUDA IPC、CUDA 算子及性能调试经历

---

## 版本更新记录

| 版本日期 | 更新性质 | 主要内容 |
|---|---|---|
| 2026-09-14 | 例行更新：岗位、代码里程碑与贡献清单纠正 | 上海 6 条既有岗位仍可申请；新增收录 09-10 发布的 San Jose GPU Fleet Management 岗位 Req 92051（Hybrid、无签证赞助，不能视为中国远程机会）。InferaSim、MORI UMBP 重构/EP v2 preview、AIC emulation 与 vLLM 弹性 EP 修复已合入。MORI #626 已有 #653 合并修复，移出待认领；AIC #150 关闭但未合并，功能由 #154 合入；SGLang timeout/abort 已有 #38164/#38704/#38961 等推进，纠正“空白新提案”定位。更新第 19 节优先三项、验证限制和来源 S52–S64。 |
| 2026-09-07 | 外部贡献专题增补与事实修正 | 新增第 19 节：Infera、MORI、AIC、SGLang/vLLM upstream 的贡献规则、10 个具体参与切口、硬件门槛、重复任务排除和两周路线。补充核验确认 AIC #139/#151 于 09-06 合并，**纠正上一版本“项目侧本期未发现实质变化”的结论**。另将 Infera #88、MORI #507/#557 等 Open issue 与实际 PR 进度交叉对照；这些较早合入属于本期新核验证据，不称作本周新发布。 |
| 2026-09-07 | 例行监测更新 | **当时记录：岗位侧有新增发现，项目侧未发现实质变化；后者已由同日专题增补纠正，见上行。** 新增核验 5 条此前未收入手册的上海官方相邻岗位：Req 87545、89395、89498、89499、89500；复核既有 Req 89398 仍开放。上述岗位均早于 2026-09-04 发布，因此应理解为“本期新发现”，不能表述为“本周新发布”。Infera、MORI、AIC 及三份 roadmap 未发现 9 月 4 日后的已确认里程碑变化。 |
| 2026-09-04 | 初版 | 完成截图 JD 复原、AMD 分布式推理项目地图、证据分级、个人匹配分析、学习路线、面试题纲与来源索引。 |

### 本期检查范围与结论

- **比较基线：** 完整读取 2026-09-07 版手册（含同日贡献专题纠正），本次检查截至 2026-09-14。历史发布日期和历史结论保留，不把旧条目的首次收录称为本周发布。
- **岗位范围与结果：** 检索 AMD Careers 中国、remote 及推理/通信/Rust 关键词，逐页复核上海 Req 89398、89500、89499、89395、89498、87545 的正文和 Apply 入口；6 条均仍开放，未发现这些岗位关闭或重新开放的证据。新增 Req 92051 为美国 San Jose、Hybrid、无签证赞助。本次未确认新的中国/可从中国远程申请岗位，亦未识别截图的 exact Req；这不是对全部 AMD 招聘的穷尽声明。[S20]–[S25][S52]
- **项目范围：** Infera、MORI、AIC、ATOM/ATOMesh 主分支提交与重点 PR；SGLang/vLLM 定向检索；AMD/ROCm 官方文章与三份 roadmap。读取 Infera/MORI/AIC 全部开放 PR 列表（分别 11/45/6 条）；大型 upstream 按相关关键词筛选，未逐条审计所有 PR。旧候选结合当前源码、评论、作者、assignee 和合并记录判断，不只读搜索摘要。
- **本期实质变化：** Infera 增加 InferaSim 和 worker/NATS 失败处理；MORI 增加 UMBP 后端/传输抽象、EP v2 跨节点 preview 与回绕修复；AIC emulation 经 #154 合入，版本组合升级，但仍明确不推荐生产负载；ATOM 增加 CPP/DCP KV 传输能力；vLLM 合入 DP 组 AITER AG/RS、KV connector 兼容及弹性 EP 死锁修复。详情及验证边界见 3.7。[S53]–[S61]
- **开源参与纠正：** MORI #626 仍 Open 但已指派 QizhouZhang97，#653 于 09-11 合并，现为学习案例；AIC #150 关闭且未合并，#154 承接合入；SGLang pending timeout/abort 不再作为无人推进的新提案。当前首选为 Infera #36、MORI #632 协作补测、SGLang #38164 等既有工作的限定评审，详情见第 19 节。[S30][S36][S53][S58][S63]
- **验证与权限约束：** 本研究未运行项目测试、未使用 AMD GPU/RDMA、未发布 Issue/评论/PR。合入、作者测试报告和本研究独立验证分开记录。SGLang MI355X 分离推理定时夜测因节点不可用暂停，手动入口仍在；不能预设维护者马上能提供硬件。[S61]
- **日期口径：** GitHub 事件默认 UTC；岗位发布日期取官方 `JobPosting.datePosted`。Apply 入口只证明检查当时可申请，不保证后续状态；结构化 `validThrough` 不视作招聘方承诺的截止日期。

---

## 0. 最终结论

### 0.1 是否值得申请

**值得，而且建议尽快申请。**

这不是普通的“模型适配工程师”或单机推理算子岗位，而是位于以下四层交界处的核心系统岗位：

1. 集群级推理调度与路由控制面；
2. 全局、分层、跨节点的 KV Cache 控制面与数据面；
3. vLLM / SGLang 推理运行时；
4. ROCm、MORI、RCCL、AITER 等 GPU 通信与算子栈。

按目前已知经历估算：

| 方向 | 当前匹配度 | 判断 |
|---|---:|---|
| C++ / GPU 通信 / KV 数据面 | 约 75% | 最适合的切入点 |
| vLLM / SGLang 运行时集成 | 约 65%–70% | 架构基础较好，需要补真实上游代码 |
| Rust 集群调度与路由控制面 | 约 55%–60% | 主要短板是 Rust async 工程经验 |
| 综合匹配 | 约 65%–75% | Stretch role，但主干经历高度相关 |

这些百分比不是雇主评分，而是为了辅助准备优先级。

### 0.2 对岗位归属的判断

最稳妥的表述是：

> 该岗位很可能来自 AMD 分布式推理产品族，覆盖 Infera / ATOMesh 类编排控制面，以及 MORI-IO、MORI-EP、MORI-UMBP 类通信与 KV 数据面；公开信息不足以证明它只属于某一个项目或某一条具体汇报线。

公开技术中，与 JD 最接近的证据包括：

- AMD 与 Moonshot AI 的 SGLang + MoRI + UMBP + AITER 联合推理栈。[S1]
- AMD ROCm Infera 的 KV-aware routing、P/D disaggregation、KV tiering、SLA planner 与 Rust router。[S2][S3][S4]
- MORI 的 KV 传输、MoE 专家并行通信、分层全局 KV，以及 2026 H2 roadmap。[S5][S6][S7][S8]
- ROCm AIC 的分布式共享 KV Cache 分层方案，但它是独立的 early-access 路线，不能与 UMBP 混为同一项目。[S9]
- ATOMesh 的 Rust 分布式网关、P/D 路由、健康检查、重试与 cache-aware scheduling。[S10]

### 0.3 最重要的不确定性

原始材料是带小红书水印的内推截图，而不是 AMD Careers 正式页面。截图没有提供：

- Req ID；
- 工作地点；
- 职级；
- 年限要求；
- 薪酬；
- 正式投递链接；
- 明确的项目和汇报线。

因此：

- 可以高置信判断技术方向；
- 可以中高置信判断它属于 AMD 分布式推理产品族；
- 不能断言 exact requisition、地点、级别或唯一项目归属。

### 0.4 本文的证据分级

| 等级 | 含义 | 本文示例 |
|---|---|---|
| A：已确认事实 | AMD 官方文章、官方文档、公开代码或上游合入记录可直接验证 | Infera 有 Rust router；MORI 分为 IO、EP、UMBP；AIC 标为 early-access |
| B：强关联推断 | JD 与多个公开 roadmap 高度对应，但没有 exact Req 证明 | 岗位大概率服务于 Infera / ATOMesh + MORI / UMBP 产品族 |
| C：待招聘方确认 | 公开材料不足，不能自行补全 | Req ID、地点、职级、汇报线、Rust/C++ 比例 |

阅读本文时，应把“公开项目具备某项能力”和“该岗位一定属于某个项目”严格区分。

---

## 1. 如何使用这份文档

### 1.1 十分钟快速复习

只看以下部分：

1. 第 0 节“最终结论”；
2. 第 3 节“岗位所处的 AMD 技术栈”；
3. 第 8 节“个人匹配度与投递定位”；
4. 第 12 节“一页式速记卡”。

### 1.2 面试前一小时

重点复习：

- 第 4 节：分布式调度；
- 第 5 节：全局 KV Cache；
- 第 6 节：路由、自愈与 MoE；
- 第 10 节：高频面试题；
- 第 11 节：六条生产级 invariant。

### 1.3 系统准备

按照第 9 节的四周路线执行，并把每周产出补充回本文档。准备公开贡献时先读第 19 节，按当前任务状态和硬件条件选择切口。

---

## 2. 原始 JD 复原

### 2.1 岗位名称

**大模型推理框架工程师**

### 2.2 内推帖摘要

AMD 推理框架组扩招，工作方向包括：

- 分布式调度；
- 全局 KV 缓存；
- 推理路由底层底座；
- vLLM / SGLang 开发。

帖子特别强调“有相关开发经验欢迎私聊，PR 砸过来”，这通常意味着：

1. 团队重视可验证的上游贡献；
2. 面试可能会直接讨论源码、PR、benchmark 和设计权衡；
3. 仅有概念性学习可能不足，需要展示实际代码或问题定位能力。

### 2.3 工作内容

1. 负责分布式调度模块开发，落地 Prefill / Decode 分离调度、拓扑调度、SLO 自适应扩缩容和 MoE 负载均衡。
2. 开发全局 KV 缓存体系，实现跨节点寻址、多级冷热迁移、缓存复用与会话隔离。
3. 实现分布式推理路由，支持 KV 亲和调度、会话黏滞、故障自愈和 MoE 专家分发。
4. 适配 ROCm 硬件，对接通信层与算子库，进行吞吐、时延和显存性能调优。

### 2.4 任职要求

1. 熟悉分布式系统和 GPU 推理运行时；了解 ROCm / HIP 者优先。
2. 精通 LLM 推理架构，理解 P/D 分离、KV Cache、TP / EP / MoE 并行逻辑。
3. 熟练 Rust / C++；有 vLLM / SGLang 源码开发、优化经验者优先。
4. 有大规模 GPU 集群推理框架落地经验，可独立完成模块开发和性能调优。

### 2.5 从措辞推断出的隐含要求

“可独立完成模块”“大规模 GPU 集群”“精通”说明其面试标准大概率偏资深 IC，而不是初级框架适配岗位。

同时，JD 同时出现 Rust、C++、全局路由、KV、通信和算子，可能有两种组织方式：

- 一个较宽的 senior / staff 型岗位；
- 一组相邻 headcount 共用一份对外画像，入职后分别进入控制面或数据面。

必须向招聘方确认主战场。

---

## 3. 岗位所处的 AMD 技术栈

### 3.1 总体架构

~~~mermaid
flowchart TD
    A["API / Gateway<br/>OpenAI-compatible"] --> B["集群控制面<br/>Infera / ATOMesh"]
    B --> C["推理引擎<br/>vLLM / SGLang / ATOM"]
    C --> D["通信与全局状态<br/>MORI-IO / EP / UMBP"]
    D --> E["ROCm GPU 底层<br/>HIP / RCCL / AITER / CK"]
~~~

各层责任不能混淆：

| 层 | 核心职责 | 典型语言 | 与 JD 的对应 |
|---|---|---|---|
| Gateway / 集群控制面 | 请求路由、worker registry、健康状态、P/D 配对、SLO、扩缩容 | Rust、Python | 分布式调度、路由、自愈 |
| 推理引擎 | continuous batching、token scheduler、KV block 管理、模型执行 | Python、C++、HIP | vLLM / SGLang 源码开发 |
| KV / 通信数据面 | RDMA/XGMI KV 传输、全局索引、分层存储、MoE dispatch/combine | C++、HIP、Python binding | 全局 KV、P/D、MoE |
| 算子与通用通信 | attention、GEMM、FusedMoE、collective、stream/event | HIP C++、Triton、CK | 吞吐、时延、显存优化 |

### 3.2 Infera：最直接的集群编排映射

Infera 是 AMD 面向大规模部署的分布式推理 reference solution，位于多个推理引擎实例之上，主要解决单实例引擎无法解决的 fleet-level orchestration 问题。[S2][S3]

公开能力包括：

- 一个入口代理多个 vLLM、SGLang 或 ATOM 实例；
- KV-aware routing；
- Prefill / Decode disaggregation；
- KV-cache tiering；
- 基于 etcd 或 Kubernetes 的 worker discovery；
- worker heartbeat、drain 和故障处理；
- SLA planner；
- Python 控制面与高性能 Rust router。

它的重要定位是：

> vLLM / SGLang 解决“一个 engine instance 内如何执行”；Infera 解决“许多 engine instances 之间如何协调”。

Infera 的初始公开定位为 v0.1 reference solution。官方 roadmap 仍列出真正的 SLO-aware scheduling、load-driven autoscaling、运行时 P/D 角色切换、cluster-wide KV pool、distributed prefill cache 和 wide EP 等工作；不能用早期版本号概括不断变化的 main，也不能把 roadmap 未勾选等同于所有相关模块都未实现。[S4]

这与 JD 的关系非常关键：**岗位很可能不是维护一个已经完全成熟的系统，而是在建设下一阶段能力。**

2026-09-07 补充核验：#88 虽仍 Open，但 Rust router 的相关 NATS request/KV event 与 Kubernetes discovery 工作已由 #113 在 2026-08-12 合并。应以当前代码和 PR 为准，不能将该 Open issue 解读为功能仍未实现；这一合并也不等于整份 roadmap 已完成。[S32]

2026-09-14 更新：#138 已于 09-10 合入 InferaSim，增加容量/延迟投影和离散事件仿真；这不是实际集群的负载驱动自动扩缩。#162 于 09-09 合入 engine death 与 NATS 恢复处理，其中 FILE 存储故障后回退 MEMORY 带来持久性边界，不能写成完整高可用保证。[S56][S57]

### 3.3 ATOMesh：高度相邻的 Rust 路由项目

ATOMesh 是 AMD 公开的分布式推理 gateway / control plane，相邻能力包括：

- 请求、worker 与 backend 协调；
- P/D 路由；
- cache-aware policy；
- worker warmup、健康检查和失败摘除；
- retry、circuit breaker、rate limiting；
- Prometheus 可观测性；
- Rust async 数据面；
- 对 ATOM、vLLM、SGLang 的适配方向。[S10][S11]

ATOMesh 与 Infera 在公开职责上有明显重叠，但没有足够证据证明二者是同一项目、重命名关系或替代关系。面试中宜称为：

> AMD 分布式推理编排产品族中的相邻项目。

### 3.4 MORI：通信与分布式 KV 数据面

MORI 是 AMD 面向大规模 LLM 推理的模块化 RDMA + GPU 框架。[S5]

#### MORI-IO

用于 P/D 分离和跨节点 KV 数据传输：

- RDMA、XGMI、TCP backend；
- GPU memory registration；
- one-sided read / write；
- batch transfer；
- session 建立与复用；
- 异步 completion；
- C++ / Python API。[S6]

#### MORI-EP

用于 MoE expert parallelism：

- token dispatch / combine；
- 单节点 XGMI；
- 跨节点 RDMA；
- throughput、low-latency、async 等不同模式；
- 与 vLLM / SGLang MoE 路径集成。[S7]

#### MORI-UMBP

用于全局、分层 KV：

- GPU HBM、主机 DRAM、远端内存和 SSD；
- 全局 block index；
- RouteGet / RoutePut；
- master / peer 元数据与事件；
- heartbeat、lease、eviction；
- placement、复制、迁移和容错方向。[S8]

MORI 2026 H2 roadmap 继续推进：

- 多级 KV；
- SSD / SPDK / GDS；
- scheduler-aware KV；
- cluster fault tolerance；
- multi-tenant；
- vLLM / SGLang upstream；
- elastic EP / EPLB。[S5]

这些条目与截图中的“冷热迁移、会话隔离、故障自愈、MoE 负载均衡”高度对应。

2026-09-14 更新：UMBP #540 已合入后端与传输解耦，#644 合入 ranged-get handle 复用；EP #625 已合入跨节点 v2，但标题仍明确标注 preview。旧 H2 roadmap 的计划措辞与当前代码有时间差，须按子功能判断。接口抽象已存在，不等于任意存储介质、共享文件系统元数据或集群容错全部就绪。[S54][S55]

### 3.5 AMD Infinity Context：另一条全局 KV 路线

AIC 是 AMD 公开的 disaggregated KV-cache inference stack，组合 vLLM、LMCache、NIXL 和存储组件，覆盖：

- GPU VRAM；
- CPU DRAM；
- local NVMe；
- NFS over RDMA；
- 大规模共享 KV 层。[S9]

需要特别注意：

- AIC 与 MORI-UMBP 解决相邻问题，但不是同一项目；
- AIC 公开仓库明确标注 early-access technology preview；
- 2026-09-14 的 README 基线为 ROCm 7.14.1、vLLM 0.28.0、LMCache 0.5.4、NIXL 1.4.1；替代 09-07 记录的 7.14 / 0.27.1 / 0.5.4 / 1.3.2 组合。Dockerfile 实际从源码构建 PyTorch release/2.13、torchvision 和 AITER；README 对 AITER wheel 的描述有滞后，部署应核对可执行构建步骤及 commit。版本升级不是生产成熟度证明。[S9][S58]
- #150 于 09-09 关闭但未合并，作者明确由 #154 承接；#154 同日合入 CPU emulation 与更新后的本地栈。不能再把 emulation 写成仅存在于未合并 #150，也不能把模拟 profile 当成真实 GPU 性能。[S58]
- 不应在简历或面试里把 roadmap / preview 描述成成熟生产能力。

### 3.6 AITER、CK 与 RCCL

AITER 提供面向 AMD GPU 推理的高性能算子和集成，包括：

- MHA / MLA；
- PagedAttention；
- Fused MoE；
- GEMM；
- RMSNorm；
- RoPE + KV Cache；
- 多种量化与融合路径。[S12]

Composable Kernel 是 HIP C++ 的 kernel / tile 编程层；RCCL 则负责常见 collective 和 P2P 通信。[S13][S14]

它们与岗位的关系是“性能协同对象”，而非该 JD 唯一主战场：

- TP / PP collective：RCCL 或 MORI-CCL；
- P/D KV 点对点传输：MORI-IO；
- MoE 稀疏 dispatch/combine：MORI-EP；
- 分层全局 KV：MORI-UMBP 或 AIC 类方案；
- attention / GEMM / MoE kernel：AITER / CK / Triton / HIP。

---

### 3.7 本期技术变化台账（2026-09-07 至 2026-09-14）

下表“合入”指公开主分支合并事实；测试结果若来自 PR 正文，均为作者报告。本研究没有独立执行这些测试。

| 项目 / 日期（UTC） | 已确认的变化 | 当前能力与验证限制 | 对岗位判断和准备的影响 |
|---|---|---|---|
| Infera #138，09-10 | 新增 `infera/projection/`：解析投影、离散事件仿真、P/D 配比、KV/权重占用与基于锚点的通信成本；main 有对应 README | 默认路径无需 GPU；采集真实锚点仍需设备。当前 README 对 `--profiling-mode simulate` 指出 Origami 依赖 ROCm/HIP，缺失时相应用例会 skip，不能照 PR 的“152 CPU tests”推定任意机器完整通过。仿真不是实测，也不是在线 autoscaler | 可用于练习 TTFT/TPOT、TP/EP/PP、暴露通信时间的容量推导；与你的集合通信经历有映射，但须补误差模型与校准意识。[S56] |
| Infera #162，09-09 | engine 子进程异常导致 worker 非零退出；区分空 prefill/decode 池；JetStream FILE 错误 10077 后重建为 MEMORY | PR test plan 尚未勾选，不称“已完整验证”。内存回退可恢复发布，但不能保留原有持久性假设 | 面试解释进程存活、服务可用、KV 索引新鲜度与持久性是四个不同指标。[S57] |
| MORI #540，09-07；#644、#650，09-11 / 09-09 | UMBP 用 `MediumBackend` 管内存与描述符、`TransferEngine` 管字节搬运；按源/目的组合选路径；ranged-get 复用 key handle；hipFile 改为可选动态加载 | #540 作者仅报告非 integration 测试；跨节点 smoke 需要真实 fabric，未在该验证中运行。缺 hipFile 的 host-staged 回退不等价于零拷贝；共享介质控制面仍有边界 | 很贴合 C++ Extension、注册内存、transfer status 生命周期；优先读 ownership、staging、错误返回契约。[S55] |
| MORI #625，09-11 | `[preview]` EP v2 internode 经 CCO/GDA 合入，包含 `auto/v2/v2_ll` 选择与 flush/空 chunk 等正确性处理 | internode 为 HIP 路径、wave64；特定量化配置拒绝。作者有双节点 MI308X/MI355X 测试，但不是所有 NIC/shape 验证；不能用单机模拟双节点。GPU-free region 测试只覆盖模型层。PR 的早期“待做 soak”段与后来勾选项有文字不同步，不据此推演完整生产覆盖 | 不再说“EP v2 全部尚未实现”；仍需学习 preview 的兼容与验证边界，尤其通信/张量生命周期。[S54] |
| MORI #653，09-11 | #626 对应 serial-number / CQ 完成计数修复合入；main 新增 `AtomicMaxSerial` 与回绕测试 | Issue 仍 Open、09-09 已指派 QizhouZhang97；状态滞后不能继续认领同题修复。#645 的优化于 #661 撤回，不能只看首次合并 | 作为 ProcessGroup Work / 完成条件 / 模序号比较的学习案例，不作为自己已完成成果。[S53][S55] |
| AIC #154，09-09；#145，09-10；#158，09-12 | emulation 与版本组合更新；attention 构建兼容修正；cliff benchmark 增加 `kvbench` 客户端 arm | emulation 不编译真实 GPU kernel；RX9070XT 局部作者验证不能外推 Instinct 集群。kvbench 的缺失 vLLM 指标应留空而非记 0；main 仍 early-access、明确不推荐生产 | C++ Extension ABI、Docker 构建和 benchmark 语义有可贡献空间；适合没有 AMD 卡时准备小范围提案。[S58][S59] |
| ATOM #2121，09-10；#2165，09-09 | P-CPP / D-DCP 的 MLA 与 DSA index-cache 传输；producer/consumer 布局映射、GPU gather staging、fence 与 bounded pool；API 增加 TTFT/流式 ITL histogram | 合入特定布局与路径，不代表任意 P/D shape 自动兼容。PR 的单测与特定模型验证不等于生产容量承诺 | 与 CUDA IPC、buffer 生命周期、layout/stride、RDMA 完成事件高度相关，优于只背网关名词。[S60] |
| vLLM #56610，09-12 | ROCm elastic EP 将 standby/joining communicator warmup 延至 scheduler 暂停后的 commit，避免和正在服务的 collective 顺序交错 | 作者在 4×MI300X 报告回归测试；修复已合入，不是当前待认领。CUDA 未观察到同一症状不等于 NCCL 保证任意跨组顺序 | 本周最高优先级面试学习案例：能把 ProcessGroup、跨 rank 顺序、动态成员与服务状态机串起来。[S61] |
| vLLM #48247，09-11；#53695，09-10 | AITER 自定义 AG/RS 用于 uniform batch 的 DP group；ROCM_AITER_UNIFIED_ATTN 启用 KV connector 兼容 | 前者不改变 TP/EP collectives，mixed batch 仍走 NCCL/RCCL；后者作者验证特定 MI300X/MoRI/NIXL 组合，不是所有布局、拓扑承诺 | 面试必须明确哪个 process group、哪个 communicator、哪种 batch/布局，不能将所有“custom collective”都说成 TP allreduce。[S61] |
| SGLang #38672，09-10；#39044，09-11 | UMBP 测试改用真实张量视图，修正 MagicMock 接口不匹配；MI355X P/D scheduled nightly 因节点不可用暂停，保留手动入口 | 前者只修改 fixture，非运行时性能改进；后者是验证资源变化，非功能下线。本次 main 仍注释 schedule | 补测先明确硬件可用性，不把无测试/跳过测试解释成通过或功能失效。[S61] |
| AMD ROCm 博客，09-08 | 介绍 SGLang 在加载时将 NVFP4 按层转为 Quark MXFP4，使用 MI350X/MI355X 原生 MXFP4 路径 | 一次性权重转换与每批 activation 量化不同；官方测试数据只覆盖所列模型/配置，不推论任意模型无精度损失 | 作为量化兼容补充阅读，优先级低于通信正确性、KV 生命周期和实测能力。[S62] |

**Roadmap 核验：** Infera #9、MORI #348、SGLang AMD #35003 本次所见更新时间分别为 08-25、06-15、08-18，没有本周 roadmap 文本更新的证据；但上述主分支已有实质合入。更新应以“已实现的子路径 + 剩余规划”表述，不把旧 roadmap 当完整现状。[S4][S5][S15]

**组织归属仍属 B/C 级：** 更多共同集成证明技术栈交集在扩大，不证明 Infera、ATOMesh、UMBP、AIC 归属同一经理，也不证明它们就是截图岗位的直接工作仓库。

---

## 4. 技术专题一：分布式调度

### 4.1 集群调度与 vLLM 本地调度的区别

vLLM 单实例 token scheduler 主要决定：

- 当前 iteration 运行哪些 requests；
- 每个 request 分配多少 token budget；
- 是否 preempt；
- 如何分配本地 KV blocks；
- continuous batching 如何推进。

本 JD 的集群调度在它之上，决定：

- 请求进入哪个模型 deployment；
- 使用 aggregated serving 还是 P/D disaggregation；
- 选择哪个 Prefill worker；
- 选择哪个 Decode worker；
- 是否利用已有 prefix KV；
- KV 从哪里加载、往哪里迁移；
- worker 是否应该扩容、缩容或 drain。

### 4.2 P/D 分离的基本路径

~~~mermaid
sequenceDiagram
    participant G as Global Router
    participant P as Prefill Worker
    participant K as Global KV / Transfer
    participant D as Decode Worker
    G->>G: 估算缓存、队列、拓扑和 SLO
    G->>D: 预留 decode capacity / KV blocks
    G->>P: 发送 prompt 与 D 元数据
    P->>K: 复用或生成 prompt KV
    K->>D: RDMA/XGMI 传输 KV
    D-->>G: 流式返回 tokens
~~~

为什么要先确认 Decode 容量：

如果 Prefill 已经完成大量计算，却发现 Decode 无法接收，系统会浪费整次 prefill 和 KV 构造成本。

### 4.3 一个实用的调度代价模型

对候选 Prefill worker \(p\) 和 Decode worker \(d\)，TTFT 可近似分解为：

\[
T_{\mathrm{TTFT}}(p,d)
= Q_p
+ C_{\mathrm{prefill}}(\mathrm{uncached\ tokens})
+ T_{\mathrm{KV}}(p,d)
+ Q_d
+ C_{\mathrm{first\ decode}}
\]

实际调度器还要考虑：

- prefix 命中长度；
- prompt 长度和预测输出长度；
- P/D queue；
- HBM 可用量；
- worker health；
- GPU / NIC / NUMA / rack 拓扑；
- P/D、TP、EP 通信是否争用相同 NIC；
- failure probability；
- TTFT / TPOT 联合 SLO。

因此，不应把该岗位理解为简单的 least-connections 或 shortest-queue 负载均衡。

### 4.4 Prefill 与 Decode 的资源差异

| 阶段 | 主要特征 | 典型瓶颈 | 调度重点 |
|---|---|---|---|
| Prefill | 一次处理大量 prompt tokens | 算力、attention/GEMM、长上下文 | chunking、prefix reuse、计算吞吐 |
| Decode | 每步生成少量 token | HBM bandwidth、launch、同步、尾延迟 | batch 动态性、TPOT、KV 容量 |

P/D pool 的比例不能长期固定。合理扩缩容至少需要：

- arrival rate；
- input / output token 分布；
- TTFT / TPOT 目标；
- cache hit；
- worker warmup；
- 模型加载、communicator 建立；
- graph capture；
- RDMA memory registration；
- hysteresis 与 cooldown，避免振荡。

### 4.5 拓扑调度

优先级通常是：

1. 同一 GPU / 已存在目标 KV；
2. 同一 xGMI domain；
3. 同一 host；
4. 同一高速网络域；
5. 跨 rack / 较慢链路。

但“最近”不一定“最快”，因为还要考虑：

- 源节点是否成为 hot key；
- NIC 是否拥塞；
- Decode 是否有足够 HBM；
- P/D 传输是否与 TP/EP collective 争用；
- 重算是否比远端传输更便宜。

### 4.6 扩缩容状态机

一个 production-grade scale-down 应遵循：

~~~mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Draining: 停止接收新请求
    Draining --> Migrating: 迁移或放弃可恢复状态
    Migrating --> Deregistered: 回收 lease / 注销 worker
    Deregistered --> [*]
~~~

不能直接删除 Pod，因为仍可能存在：

- in-flight generations；
- 未完成的 KV RDMA；
- session affinity；
- communicator；
- 被 pin 的 KV block；
- 尚未回收的 lease。

### 4.7 调度指标

必须同时观察：

- TTFT p50 / p95 / p99；
- TPOT、ITL 或 TBT p50 / p95 / p99；
- 联合 SLO attainment；
- goodput：满足 SLO 的有效请求或 token 产出；
- per-GPU goodput；
- P/D queue time；
- KV transfer latency / bandwidth / timeout；
- wasted prefill tokens；
- scale-out cold-start；
- scale convergence；
- request rejection / timeout；
- failure recovery time。

---

## 5. 技术专题二：全局 KV Cache

### 5.1 “全局 KV”到底比本地 KV 多了什么

本地 KV manager 通常只管理：

- 当前 engine instance；
- 本进程或本机 GPU；
- block allocation；
- prefix cache lookup；
- preemption 与 refcount。

全局 KV 系统还必须管理：

- block 在哪个节点、GPU、DRAM pool 或 SSD；
- 是否存在多个副本；
- 从哪里读取最划算；
- 何时迁移、淘汰和复制；
- worker 失败后如何恢复索引；
- 多租户之间如何隔离；
- metadata 的一致性和过期问题。

### 5.2 逻辑 key 不能只是 token hash

正确的逻辑 namespace 至少应覆盖：

~~~text
model_id / model_revision
tokenizer / tokenizer_revision
attention type and KV layout
KV dtype / block size
TP / PP partition and rank layout
LoRA / adapter identity
tenant or cache_salt
parent block hash
current token block hash
~~~

遗漏任意影响 KV 数值或布局的维度，都可能导致错误复用。

物理位置可以表示为：

~~~text
block_hash
  -> storage tier
  -> node / GPU rank
  -> segment / rkey
  -> offset / size
  -> version / lease / state
~~~

逻辑 key 与物理位置必须分离，否则无法安全迁移、复制和容灾。

### 5.3 GET 路径

1. 对 prompt 生成 chained block hash；
2. 查询最长可复用前缀；
3. 找出所有候选副本；
4. 比较 HBM、DRAM、SSD、远端网络和重算成本；
5. 在目标 worker 预留并 pin blocks；
6. 获取或复用 RDMA session、rkey 和地址；
7. 异步读取；
8. completion 后才允许 attention 使用；
9. 失败时切换副本或重算。

### 5.4 PUT 与迁移路径

1. 选择目标 tier 和节点；
2. 分配空间并建立传输；
3. 完成写入；
4. 校验 completion / checksum；
5. 原子发布 Stored 元数据；
6. 通过 KV event 更新全局索引；
7. lease / refcount 释放后才允许源 block 回收。

最重要的正确性规则是：

> 数据完成提交以后，位置才可以对外发布。

如果先发布地址、后异步写数据，其他请求可能读取到未完成数据，或读到已经被 allocator 复用的旧地址。

### 5.5 多级冷热迁移

典型层级：

~~~mermaid
flowchart LR
    A["GPU HBM<br/>最快、最贵"] --> B["本机 DRAM"]
    B --> C["远端 DRAM"]
    C --> D["NVMe / 共享存储<br/>最慢、容量最大"]
~~~

不能只按 LRU 淘汰。更合理的价值函数是：

\[
\mathrm{Value}
= P(\mathrm{future\ hit})
\times \mathrm{saved\ prefill\ time}
- \mathrm{transfer\ cost}
- \mathrm{storage\ cost}
\]

长 prefix 即使访问频率不高，也可能因为重算非常昂贵而值得保留。

### 5.6 会话复用与隔离

多轮对话通常希望：

- 下一轮尽可能回到已有 KV 的 worker；
- 或从全局 cache 快速恢复；
- Decode 新生成的 KV 异步写回；
- 下一轮只计算增量。

但必须区分：

- session stickiness：性能偏好；
- tenant namespace：安全和正确性边界。

session_id 本身不能承担权限隔离。实际系统还需要：

- tenant / org / user namespace；
- cache_salt；
- per-tenant quota；
- 带宽 QoS；
- 公平 eviction；
- 管理 API 权限；
- timing side-channel 防护。

### 5.7 全局 KV 指标

- reused token ratio，而不只是 request hit rate；
- HBM / local DRAM / remote DRAM / SSD 分层命中率；
- lookup latency；
- transfer latency 与带宽；
- load stall；
- saved prefill tokens / FLOPs / time；
- fallback recompute；
- eviction 与 replication amplification；
- hot-key source load；
- stale index / event lag；
- lease expiry；
- orphan blocks；
- checksum / corruption；
- per-tenant capacity 和 bandwidth。

---

## 6. 技术专题三：路由、故障自愈与 MoE

### 6.1 路由层级

~~~mermaid
flowchart TD
    A["API / Tenant"] --> B["Model Deployment"]
    B --> C["Global Router"]
    C --> D["P/D Pair 或 Worker Group"]
    D --> E["DP Rank"]
    E --> F["本地 Token Scheduler"]
~~~

一个较完整的 router score 可以包含：

\[
\mathrm{Score}
= \widehat{\mathrm{TTFT}}
+ \widehat{\mathrm{TPOT}}
+ C_{\mathrm{uncached\ prefill}}
+ C_{\mathrm{KV\ transfer}}
+ C_{\mathrm{topology}}
+ R_{\mathrm{failure}}
\]

### 6.2 KV affinity 与 session stickiness

| 机制 | 依据 | 优点 | 风险 |
|---|---|---|---|
| KV affinity | 实际 prefix block 命中 | 直接减少 prefill | 容易形成热点 |
| Session stickiness | session 到 worker 的软绑定 | 实现简单，多轮命中稳定 | worker 过载或故障时必须解除 |
| Least load | queue / active requests | 平衡短期负载 | 可能丢失大量 KV locality |

生产调度器通常需要在 locality 与 active work 之间动态权衡。

### 6.3 故障阶段决定恢复语义

#### 首 token 前失败

- 取消旧请求；
- 释放资源和 lease；
- 重新选择 worker；
- 从全局 KV 恢复或重算；
- 向客户端隐藏内部重试。

#### 已经流式输出后失败

需要额外保存：

- 已确认发送的 token 边界；
- sampling parameters；
- RNG state；
- logits processor state；
- 已生成 prefix；
- 可恢复的 KV 或重算输入。

严格 exactly-once streaming 很难，因为服务端未必知道客户端最后确认收到了哪个 token。

### 6.4 自愈要覆盖的故障

- worker 进程崩溃；
- GPU reset；
- NIC / RDMA session 失败；
- RCCL communicator error；
- 整节点掉线；
- router / index 重启；
- KV metadata 过期；
- 计划内 scale-down；
- 部分 transfer completion 丢失。

### 6.5 MoE 负载均衡的两层

#### 请求级 DP / cluster 调度

决定整条请求进入哪个 DP rank、pod 或 worker group，目标包括：

- 平衡 queue；
- 平衡 active KV；
- 减少同步 barrier 的尾部不均衡；
- 利用已有 prefix。

#### token 级 EP dispatch

模型 gate 为每个 token 选择 top-k experts，然后系统执行：

~~~mermaid
flowchart TD
    A["Hidden States"] --> B["Top-k Expert IDs / Weights"]
    B --> C["Histogram / Pack / Dispatch"]
    C --> D["Local Grouped GEMM"]
    D --> E["Combine / Restore Token Order"]
~~~

集群 router 不能替代模型 gate 决定单个 token 属于哪个 expert。控制面能做的是：

- expert replica placement；
- logical expert → physical slot 映射；
- 热点 expert 副本；
- 全 rank 映射版本广播；
- EPLB 统计与重新布局。

### 6.6 MoE 指标

- 每个 expert / rank 的 token 数；
- slowest rank / average rank time；
- dispatch / combine p50 / p99；
- RDMA / XGMI bandwidth；
- grouped GEMM utilization；
- barrier bubble；
- inter-node bytes；
- remap overhead；
- redundant expert HBM。

---

## 7. 技术专题四：ROCm、通信、算子与性能

### 7.1 从 CUDA 栈映射到 AMD 栈

| 已熟悉概念 | AMD 侧主要映射 | 需要补充 |
|---|---|---|
| CUDA Runtime | HIP Runtime | API 差异、stream/event、graph、allocator |
| NCCL | RCCL | ROCm 拓扑、channel、IB/RoCE 路径 |
| NVLink / NVSwitch | xGMI / Infinity Fabric | 拓扑、P2P 和带宽特征 |
| CUDA IPC | HIP IPC / ROCm memory sharing | handle、生命周期、同步 |
| CUDA kernels | HIP C++ / CK / Triton | wavefront、LDS、VGPR、MFMA |
| GPUDirect RDMA | ROCm RDMA / MORI | memory registration、rkey、CQ/QP |

### 7.2 三类通信不能混为一谈

| 场景 | 数据形态 | 典型方案 |
|---|---|---|
| TP / PP collective | dense tensor collective | RCCL / MORI-CCL |
| P/D KV transfer | 点对点、大块、带状态 | MORI-IO |
| MoE expert dispatch | 稀疏 all-to-all(v) | MORI-EP |
| 全局 KV tiering | block + metadata + storage | MORI-UMBP / AIC |

### 7.3 通信层真正的工程难点

- GPU / rank / NIC / NUMA 绑定；
- multi-rail striping；
- QP 和 connection 数量爆炸；
- CQ polling 与 completion；
- memory registration cache；
- GDR / DMA-BUF；
- 小消息 latency 与大消息 bandwidth 的不同路径；
- RoCE congestion 和 QoS；
- compute / communication overlap；
- 通信 kernel 占用 CU 对 GEMM 的反向影响；
- stream / event 完成前不得回收 buffer；
- communicator abort / recreate；
- graph capture 中的动态分配和隐式同步限制。

### 7.4 显存预算

稳态显存不能只统计 weights 和 KV：

\[
\mathrm{HBM}
= \mathrm{weights}
+ \mathrm{KV}
+ \mathrm{activations}
+ \mathrm{graph\ pools}
+ \mathrm{RDMA\ registered\ buffers}
+ \mathrm{staging}
+ \mathrm{fragmentation}
\]

P/D 传输期间，源 KV、目标 KV 和 staging buffer 可能同时存在。

### 7.5 性能分析指标

- end-to-end tokens/s/GPU；
- goodput；
- TTFT / TPOT p99；
- kernel time；
- launch gap；
- achieved FLOP/s；
- HBM bandwidth；
- arithmetic intensity；
- MFMA / CU occupancy；
- wave stall；
- VGPR / LDS；
- L2 hit；
- algorithm bandwidth / bus bandwidth；
- registration cache miss；
- overlap ratio；
- peak / steady HBM；
- fragmentation；
- correctness 与数值误差。

---

## 8. 个人匹配度与投递定位

### 8.1 当前最有竞争力的经历

#### ProcessGroupDLCCL 与集合通信

直接映射：

- 分布式框架与通信库的接口边界；
- collective 语义；
- async Work 生命周期；
- stream / event 同步；
- communicator 管理；
- 多 rank 一致性；
- 性能与正确性并行调试。

#### vLLM custom allreduce

CUDA IPC + barrier 的经验可以映射到：

- 跨进程 GPU buffer 共享；
- handle 和内存生命周期；
- barrier / event 正确性；
- 自定义通信快路径；
- size threshold；
- fallback；
- 故障和资源回收。

#### NCCL 源码

NCCL enqueue、collective 和同步路径的理解，可以迁移到：

- RCCL；
- MORI-CCL；
- MORI-IO 的异步 completion；
- 通信与计算 overlap；
- hang / timeout / use-after-free 定位。

#### CUDA kernel 与性能调试

有助于迁移至 HIP / AITER / CK：

- memory-bound 与 compute-bound 判断；
- launch overhead；
- occupancy；
- 数据布局；
- fusion；
- profiler 与 benchmark；
- 数值正确性。

#### 早期分布式数据平台经历

它不能替代 GPU serving 生产经验，但能辅助说明：

- 调度与任务状态；
- control plane；
- metadata；
- 监控；
- 故障处理；
- 系统化工程思维。

### 8.2 主要缺口

| 缺口 | 风险 | 优先补法 |
|---|---|---|
| Rust async 生产经验 | 若岗位主责 Infera / ATOMesh router，可能成为硬门槛 | Tokio、Axum/Tonic、Arc、channel、取消、背压、DashMap |
| ROCm / HIP / RCCL 实战 | 面试会问 AMD 平台细节 | 做 CUDA→HIP port；阅读 RCCL / AITER / MORI |
| SGLang 源码 | JD 明确点名 | 聚焦 HiCache、disaggregation、gateway、EP |
| vLLM / SGLang upstream PR | “PR 砸过来”是显著信号 | 先做测试、观测、文档或 policy 小 PR |
| 大规模在线推理集群 | senior 岗位可能追问真实规模与故障案例 | 用系统设计和已有分布式故障经验诚实补位 |
| 全局 KV 落地 | 当前以研究为主 | 做小型 metadata index / tiered cache prototype |

### 8.3 推荐的投递定位

最合适的定位：

> C++ / GPU 通信与推理数据面工程师，具备 PyTorch distributed、ProcessGroup、collective、CUDA IPC、vLLM 通信优化和 GPU 性能调试经验；希望进一步承担 MORI-IO / MORI-UMBP、vLLM / SGLang connector 与 ROCm 性能工作，并能补齐 Rust 控制面。

不建议把自己包装成：

- 已经完整落地过 production global KV cache；
- 已经维护过大规模 ROCm 集群；
- 精通 Rust async；
- vLLM / SGLang 核心 maintainer。

### 8.4 30 秒自我介绍主线

> 我目前主要做自研 AI 加速器上的 PyTorch 分布式和推理框架工作，包括 ProcessGroupDLCCL、collective、PyTorch C++ Extension，以及 vLLM custom allreduce。我在 CUDA IPC、barrier、stream/event 生命周期、通信正确性和性能定位方面有直接经验，也读过 NCCL 和 vLLM 的关键路径。这个岗位里，我与 MORI-IO、UMBP、vLLM/SGLang connector 及 C++ 数据面的匹配度最高；Rust 和 ROCm 是我当前重点补齐的部分。

### 8.5 三段必须准备好的项目故事

#### 故事 A：ProcessGroupDLCCL

回答框架：

1. 为什么需要新的 ProcessGroup；
2. PyTorch 上层语义如何映射到自研通信库；
3. Work、stream、event 和 completion 如何设计；
4. 遇到过什么 hang、timeout、内存或同步问题；
5. 如何验证多 rank 正确性；
6. 性能指标如何变化。

#### 故事 B：vLLM custom allreduce

回答框架：

1. 为什么默认路径不够；
2. CUDA IPC 如何建立共享；
3. barrier 如何保证内存可见性；
4. size threshold 为什么存在；
5. buffer 何时可以复用；
6. 故障和进程退出如何处理；
7. benchmark 和最终收益。

#### 故事 C：性能或随机异常定位

回答框架：

1. 先区分数值错误、竞态、未同步、越界和未初始化；
2. 固定输入和随机性；
3. 单卡→多卡、单 stream→多 stream 缩小范围；
4. 对齐 reference；
5. 使用 profiler、sanitizer、日志和 checksum；
6. 找到 root cause；
7. 加回归测试。

---

### 8.6 本期个人化调整：先补能解释的工程证据

没有新增你的实做、实测或合并成果，故不调整 0.1 的启发式匹配比例。

1. **主线不变：C++ / 通信 / 推理数据面。** ProcessGroupDLCCL 与集合通信用于解释 vLLM #56610 的跨组 warmup 顺序；custom allreduce 与 CUDA IPC 用于对照 #48247 的 DP group、IPC 资源与 fallback，不能混用 TP/EP 概念。
2. **本周优先复习三份案例：** MORI #653 的 serial order 与完成条件；vLLM #56610 的 prepare/commit 状态机；ATOM #2121 的布局变换、staging buffer 与 RDMA fence。产出每份一页“旧问题—不变量—修复—验证—限制”，明确是源码学习，不是个人贡献。[S53][S60][S61]
3. **公开贡献优先做一条：** Infera #36 的行为兼容探测接口。后备选 MORI #632 的并发测试协作；SGLang lifecycle 先做既有 PR 的覆盖矩阵，不再从零提相同 timeout 修复。详见 19.11。
4. **新增补课：** AIC 的源码 PyTorch/AITER ABI 组合与你的 C++ Extension 经验直接相连；学习如何识别 README、Dockerfile 注释和实际 RUN 命令不一致，而不是假设“版本新就兼容”。InferaSim 用于容量推理训练，不能替代 HIP/多卡/RDMA 实操。[S56][S58]
5. **Rust 暂不升为唯一主线。** 新 Req 92051 更直接强调 production Rust 与 Fleet Manager，但地点和资格限制使它只适合组织/技术旁证；上海优先级仍是 89398、89500、89499。若以后确认你有美国工作资格，再单独评估该岗位，不预设可跨境 remote。[S52]

---

## 9. 四周准备路线

### 第 1 周：建立项目地图

- [ ] 阅读 Infera README、architecture、feature matrix 和 roadmap；
- [ ] 阅读 Infera Rust router 的 policy、pool、discovery、proxy、PD dispatch；
- [ ] 阅读 ATOMesh 的 cache-aware policy、worker registry 和 health/retry；
- [ ] 阅读 AMD × Moonshot 文章；
- [ ] 画出一次请求的控制流、KV 数据流和 MoE token 流。

产出：

- 一张完整架构图；
- 一页“组件—职责—语言—指标”表；
- 能在五分钟内解释 Infera、MORI 和 vLLM/SGLang 的边界。

### 第 2 周：MORI 与 ROCm

- [ ] 阅读 MORI-IO guide；
- [ ] 阅读 MORI-EP guide；
- [ ] 阅读 UMBP master control-plane design；
- [ ] 阅读 RCCL 基本通信模型；
- [ ] 阅读 AITER 的算子和 vLLM/SGLang integration；
- [ ] 总结 CUDA→HIP、NCCL→RCCL/MORI 的迁移点。

产出：

- P/D KV transfer 时序图；
- UMBP GET / PUT 状态机；
- 一份异步 buffer 生命周期 checklist。

### 第 3 周：Rust 与控制面

- [ ] ownership、borrow、Arc、Mutex/RwLock；
- [ ] Tokio task、channel、select、timeout；
- [ ] cancellation propagation；
- [ ] Axum HTTP；
- [ ] Tonic gRPC；
- [ ] DashMap / atomics；
- [ ] backpressure、rate limiting、retry、circuit breaker；
- [ ] PyO3 基础。

练习项目建议：

> 写一个简化的 Rust inference router：维护 worker registry、heartbeat、least-load 与 prefix-affinity policy，支持 drain、timeout 和 Prometheus metrics。

### 第 4 周：面试和公开产出

- [ ] 完成三个项目故事；
- [ ] 完成两个系统设计题；
- [ ] 准备 recruiter 问题；
- [ ] 尝试一个小型上游 PR；
- [ ] 更新简历项目描述；
- [ ] 做一次 60 分钟 mock interview。

低硬件门槛 PR 方向：

- router policy 单元测试；
- worker drain / retry 边界测试；
- cache-aware routing 的 observability；
- 文档和示例；
- mock worker；
- connector error handling；
- benchmark harness。

有 AMD GPU 时再考虑：

- HIP port；
- MORI-IO connector reproduction；
- P/D KV transfer benchmark；
- RCCL / MORI 对比；
- AITER operator benchmark。

---

## 10. 高频面试题纲

### 10.1 系统设计

1. 设计一个支持 P/D 分离的全局调度器。
2. 如何同时优化 TTFT、TPOT 与 goodput？
3. cache affinity 与 load balancing 冲突时如何决策？
4. 如何设计一个跨节点全局 KV index？
5. 如何比较远端拉取 KV 与重新 prefill 的成本？
6. 如何实现 HBM→DRAM→SSD 的冷热迁移？
7. 如何处理 worker failure 和 stale KV metadata？
8. scale-down 时如何保证不丢失 in-flight request？
9. 如何为多租户提供 cache isolation 与公平性？
10. 如何支持 wide EP、expert replication 与 EPLB？

### 10.2 C++ / 并发 / 通信

1. 异步 RDMA 已 enqueue 是否意味着 buffer 可以回收？
2. memory registration 生命周期如何管理？
3. CQ polling、callback 和 coroutine 各有什么权衡？
4. 如何避免 use-after-free 与 ABA？
5. communicator 出错后如何恢复？
6. 为什么 barrier 可能成为性能瓶颈？
7. 如何验证通信与计算 overlap？
8. 如何定位 collective hang？
9. small message latency 和 large message bandwidth 如何分别优化？
10. 如何设计 zero-copy connector？

### 10.3 Rust async

1. 为什么使用 Arc？何时还需要 Mutex / RwLock？
2. Tokio task 被取消时资源如何释放？
3. 如何设计 bounded channel 与 backpressure？
4. 如何实现 heartbeat 和 timeout？
5. retry 如何避免 retry storm？
6. 如何实现 drain 而不丢失 in-flight request？
7. DashMap 与单一 Mutex<HashMap> 的权衡是什么？
8. gRPC streaming 的取消如何向下游传播？

### 10.4 vLLM / SGLang

1. vLLM 本地 scheduler 与 global scheduler 的边界是什么？
2. KVConnector 的 scheduler-side 与 worker-side 分别做什么？
3. P/D disaggregation 时 KV block 如何匹配？
4. prefix cache key 为什么不能只含 token IDs？
5. vLLM V1 persistent batch 与异步 H2D 有什么关系？
6. SGLang HiCache 的 L1 / L2 / L3 语义是什么？
7. MoE dispatcher 与 EPLB 有什么区别？
8. graph capture 如何处理动态 batch / sequence？

### 10.5 ROCm / GPU 性能

1. HIP stream / event 与 CUDA 有哪些语义和实现差异？
2. RCCL、MORI-IO、MORI-EP 的边界是什么？
3. xGMI 与 RDMA 的拓扑代价如何进入调度？
4. graph capture 为什么限制动态分配和 communicator 创建？
5. 如何判断 attention / GEMM / KV copy 是 compute-bound 还是 memory-bound？
6. VGPR、LDS 和 occupancy 如何相互影响？
7. 如何发现 host sync？
8. 如何验证 kernel fusion 是否真正提升端到端 goodput？

---

## 11. 六条生产级正确性 invariant

以下六条很适合在系统设计面试中主动强调。

### 11.1 数据完成后才能发布位置

KV 写入或迁移完成以前，不能把目标地址标记为可读。

### 11.2 异步操作完成前不能复用 buffer

RDMA / HIP operation 已 enqueue 不等于完成；event、CQ completion、lease 和 refcount 必须形成一致的生命周期。

### 11.3 Cache key 必须覆盖所有语义维度

模型版本、tokenizer、KV layout、dtype、并行切分、adapter 和安全域任何一个不匹配，都不能复用。

### 11.4 Affinity 是性能偏好，不是正确性边界

session stickiness 失效时，请求仍应能通过全局 KV 或重算正确执行；tenant namespace 才是安全边界。

### 11.5 Scale-down 必须先 drain

停止接收新请求、完成或迁移状态、回收 lease、注销 worker 和 communicator，然后才能释放资源。

### 11.6 Expert 映射必须跨 rank 同版本

logical expert 到 physical slot 的更新必须在所有 rank 一致生效，且不能切断 in-flight microbatch。

---

## 12. 一页式速记卡

### 12.1 岗位一句话

> 在 vLLM / SGLang 之上做集群级推理编排，并把请求、会话、SLO 和 cache 语义落到 MORI / ROCm 的 KV、RDMA、MoE 和 GPU 数据面。

### 12.2 项目边界

- Infera / ATOMesh：集群控制面、Rust router；
- vLLM / SGLang / ATOM：engine runtime；
- MORI-IO：P/D KV transfer；
- MORI-EP：MoE dispatch / combine；
- MORI-UMBP：全局分层 KV；
- AIC：另一条 shared KV tiering 技术预览；
- RCCL：通用 collective；
- AITER / CK：算子与 HIP kernels。

### 12.3 三条核心公式

调度：

\[
TTFT = Q_p + C_{\mathrm{uncached}} + T_{\mathrm{KV}} + Q_d + C_{\mathrm{first\ decode}}
\]

缓存价值：

\[
Value = P(hit) \times saved\_prefill - transfer - storage
\]

显存：

\[
HBM = weights + KV + activations + graphs + RDMA\ buffers + staging + fragmentation
\]

### 12.4 必报指标

- TTFT；
- TPOT / ITL；
- SLO attainment；
- per-GPU goodput；
- KV reused token ratio；
- 分层命中率；
- transfer latency / bandwidth；
- queue；
- HBM；
- recovery time。

### 12.5 个人卖点

- ProcessGroupDLCCL；
- collectives；
- vLLM custom allreduce；
- CUDA IPC + barrier；
- NCCL source；
- PyTorch C++ Extension；
- kernel / profiler / sanitizer；
- 分布式系统工程基础。

### 12.6 首要短板

- Rust async；
- ROCm / HIP / RCCL hands-on；
- SGLang；
- 上游 PR；
- production-scale serving。

---

## 13. 向招聘方确认的问题

### 13.1 基本信息

1. 正式 Req ID 是什么？
2. 工作地点和 remote policy 是什么？
3. 对应职级和年限要求是什么？
4. 截图是否对应一个 headcount，还是多个相邻岗位？

### 13.2 技术归属

1. 主要归属 Infera / ATOMesh、MORI-UMBP、MORI-IO / EP，还是 vLLM / SGLang integration？
2. Rust 与 C++ / HIP 的工作比例是多少？
3. Rust 是入职硬门槛，还是可以入职后补齐？
4. 是否需要直接向 vLLM / SGLang upstream 提交 PR？

### 13.3 业务与交付

1. 入职前三个月最重要的 deliverable 是什么？
2. 当前哪些能力已经 production，哪些仍是 prototype / roadmap？
3. 集群规模、GPU 型号、NIC 和网络拓扑是什么？
4. 是否有客户 POC、benchmark deadline 或 on-call？
5. 成功指标更偏 TTFT、TPOT、goodput、KV hit 还是 availability？

---

## 14. 当前能力成熟度与岗位机会

| 能力 | 公开状态判断 | 岗位含义 |
|---|---|---|
| Infera KV-aware routing / P/D | 已有公开基础能力 | 需要完善策略、兼容性和生产可靠性 |
| Rust router | 已公开代码；#113 已合并 NATS/Kubernetes 相关路径，旧 Open issue 状态有滞后。[S32] | Rust 要求有直接来源，准备需读当前实现 |
| SLA planner / InferaSim | #138 已合入投影与仿真；不等于真实在线 resize。[S56] | 学成本模型、锚点误差与实际调度的边界 |
| Cluster-wide KV | 多条方案正在演进 | 全局索引、tiering、容错是核心增量 |
| MORI-IO | 已进入 vLLM / SGLang 集成 | 仍需兼容更多拓扑并强化错误路径 |
| MORI-EP | 已有 dispatch/combine；09-11 跨节点 EP v2 #625 以 preview 合入。[S54] | 兼容性、特定 NIC/shape 调优与实机回归仍重要 |
| MORI-UMBP | #540 后端/传输抽象、#644 ranged-get handle 复用已合入；共享介质/容错不能泛化。[S55] | descriptor、ownership、staging 和失败语义与经历高度相关 |
| AIC | 仍 early-access preview；ROCm 7.14.1 / vLLM 0.28.0 / LMCache 0.5.4 / NIXL 1.4.1；emulation 经 #154 合入，#150 关闭但未合并。[S58] | CPU 工具与 ABI 文档有局部机会，不代表生产栈成熟 |
| SGLang AMD CI | MI355X 分离推理定时夜测因节点不可用暂停，手动工作流保留。[S61] | 实机补测有资源门槛；不是代码能力下线 |
| MI45x / Helios | roadmap 重点 | 可能涉及新硬件 bring-up |

该岗位的吸引力：

- 处于 AMD 大规模推理竞争的关键路径；
- 系统深度高；
- 开源影响力强；
- 能连接调度、缓存、网络和 GPU；
- 有机会独立拥有核心模块。

主要风险：

- 范围宽；
- 需求和架构变化快；
- 生产可靠性与 benchmark 压力并存；
- 新硬件和上游版本带来持续适配；
- 岗位边界可能需要入职后才完全明确。

---

## 15. 相关官方岗位旁证

### 15.1 2026-09-14 已核验的上海岗位矩阵

以下 6 条岗位在 09-07 与 09-14 两次检查均显示 Apply 入口。本期逐页读取官方正文，未发现与手册相比的关键职责变化；不是对完整 HTML 的逐字差分。发布日期保留此前官方结构化字段记录；未见新的重新发布日期。职位开放不等于通过资格筛选，也不等于截图 exact requisition。[S20][S21][S22][S23][S24][S25]

| 优先级 | 职位名称 | 地点 | Req ID | 发布日期 | 2026-09-14 状态 | 与截图方向的关系 | 官方链接 |
|---|---|---:|---:|---:|---|---|---|
| P0 | AI Software Engineer | 上海 | 89398 | 2026-08-03 | 开放 | **最直接的分布式推理岗位旁证。** 明确写 P/D disaggregation、Large-EP、vLLM、SGLang、多机多卡、C++ / Python、ROCm / LLVM；要求 Master/PhD 与 5+ 年经验。 | [查看](https://careers.amd.com/careers-home/jobs/89398?lang=en-us) |
| P0 | AI Framework Engineer | 上海 | 89500 | 2026-08-26 | 开放 | 明确要求 vLLM 或 SGLang、Transformer / Attention / MoE / KV Cache、PagedAttention、continuous batching、多机通信瓶颈与开源贡献；CUDA / HIP / CK / Triton 为加分项。 | [查看](https://careers.amd.com/careers-home/jobs/89500?lang=en-us) |
| P0 / Stretch | AI Framework Engineer | 上海 | 89499 | 2026-08-26 | 开放 | 与 89500 基本同族，但措辞更偏 expert：大规模异构集群、Python/C++、LLVM/ROCm 与内核优化要求更强；适合作为资深档位投递。 | [查看](https://careers.amd.com/careers-home/jobs/89499?lang=en-us) |
| P1 | AI Software and GPU Kernel Development Eng. | 上海 | 89395 | 2026-08-07 | 开放 | 明确聚焦 SGLang、分布式推理并行、collective communication、HIP/CUDA、GPU kernel、图编译器与 upstream；更偏引擎和算子层。 | [查看](https://careers.amd.com/careers-home/jobs/89395?lang=en-us) |
| P1 | AI Framework Engineer | 上海 | 89498 | 2026-08-26 | 开放 | 3+ 年；偏 TensorFlow/PyTorch、GPU kernel、HIP/CUDA/ASM、scale-up/scale-out 和 compiler。与截图相邻，但没有明确写 Rust、全局 KV 或 P/D。 | [查看](https://careers.amd.com/careers-home/jobs/89498?lang=en-us) |
| P2 / 级别回退 | AI Framework Eng. | 上海 | 87545 | 2026-06-24 | 开放 | 官方明确称 early-career；涉及 vLLM/SGLang、KV Cache、MoE、multi-GPU / multi-node、async programming 和 upstream。技术关键词很贴近，但级别可能低于个人最佳定位。 | [查看](https://careers.amd.com/careers-home/jobs/87545?lang=en-us) |

### 15.2 本期变化应如何解读

**已确认事实：** 上述 6 条官方岗位仍可申请；本期另有以下新发布、首次收录条目。[S52]

| 职位名称 | 地点 / 工作方式 | Req ID | 发布日期 | 本期状态 | 官方链接 |
|---|---|---|---|---|---|
| Software Development Engineer — GPU Fleet Management & AI Infrastructure | San Jose, California, US；Hybrid | 92051 | 2026-09-10 16:18 UTC（北京时间 09-11） | 开放、新发布且新收录；明确不提供签证赞助 | [AMD Careers](https://careers.amd.com/careers-home/jobs/92051?lang=en-us) |

该岗位负责 GPU Fleet Manager 控制面、API、scheduler、inference gateway 与 CLI；重视 production Rust（也列 C++/Go）、Kubernetes/Kueue/JobSet、持久化协调、重试/幂等与多租户。vLLM/SGLang、ROCm/RCCL/collectives 是相关经验。它是很直接的“Rust 集群控制面”旁证，但不是中国远程岗位，不能替代上海投递清单，也不能认定属于 Infera 团队。

**本期分类汇总：** 新发布并收录 1 条（92051）；既有 6 条上海岗位持续开放；未确认关闭或重新开放；未确认 exact screenshot Req。此前 5 条上海职位的“新发现”保留在 09-07 版本记录，不重复记为本周新增。后续如关闭，保留表行及关闭核验日期，不删除。

**强关联推断：** 8 月集中发布的多个近似 Req 表明上海侧不是单一 headcount，而更像按级别或子方向拆分的一组 AI inference/framework 招聘。但官方页面未说明它们与截图团队、Infera、MORI 或 ATOMesh 的组织关系，因此不能将其写成已确认归属。

**待招聘方确认：** Req 89499 与 89500 的内部职级差异、截图所指 exact Req、是否允许中国境内远程、是否接受学历或年限等价替代、Rust 与 C++/HIP 的实际占比。

### 15.3 对个人投递定位与准备优先级的影响

1. **第一批：89398 + 89500。** 89398 与 P/D、Large-EP、通信和多机性能最直接；89500 对 vLLM/SGLang、KV、开源贡献与 C++ 的综合要求与现有经历最均衡。
2. **冲刺档：89499。** 用 ProcessGroupDLCCL、NCCL 源码、custom allreduce、故障定位和性能数据证明“expert”深度，避免仅罗列概念。
3. **引擎 / 内核备选：89395。** 如果目标更偏 SGLang runtime、collective 与 GPU kernel，这条比控制面岗位更贴近当前优势。
4. **级别校准：89498 / 87545。** 89498 是较宽的 3+ 年框架/内核岗；87545 明确 early-career。是否投递取决于个人年限、职级预期和招聘方是否支持同族 Req 调剂。
5. **准备顺序微调：** Rust 仍是截图岗位的重要短板，但当前官方可投岗位更明确地要求 Python/C++、SGLang/vLLM、HIP/CUDA、kernel 与多机性能。因此近期准备应先产出一个可展示的 vLLM/SGLang + ROCm/HIP 或通信性能证据，再并行补 Rust async 控制面。

这些岗位能证明上海存在高度相邻的技术招聘，但不能证明任何一条就是截图中的岗位，也不能证明截图岗位具有相同职级、年限或汇报线。

---

## 16. 术语表

| 术语 | 含义 |
|---|---|
| TTFT | Time To First Token，首 token 延迟 |
| TPOT | Time Per Output Token，平均输出 token 时间 |
| ITL / TBT | Inter-Token Latency / Time Between Tokens |
| Goodput | 满足指定 SLO 的有效吞吐 |
| P/D | Prefill / Decode 分离 |
| KV affinity | 按已有 prefix KV 位置选择 worker |
| Session stickiness | 同一会话优先回到原 worker |
| TP | Tensor Parallelism |
| PP | Pipeline Parallelism |
| DP | Data Parallelism |
| EP | Expert Parallelism |
| EPLB | Expert Parallel Load Balancing |
| RDMA | Remote Direct Memory Access |
| XGMI | AMD GPU 间高速互连 |
| RCCL | AMD ROCm 集合通信库 |
| AITER | AMD 面向 AI 推理的算子与优化库 |
| MORI-IO | MORI 的 KV / P2P 数据传输模块 |
| MORI-EP | MORI 的 MoE dispatch / combine 模块 |
| MORI-UMBP | MORI 的统一内存与带宽池 / 分层 KV 模块 |
| AIC | AMD Infinity Context，分布式共享 KV 技术栈 |
| HiCache | SGLang 的分层 KV Cache 机制 |
| KVConnector | vLLM 的外部 KV 传输接口 |

---

## 17. 来源索引

以下来源以 AMD 官方、ROCm 官方仓库、项目上游仓库和正式文档为主。研究日期为 2026-09-14；早期来源保留，新增证据注明本期日期，roadmap 和 main 可能继续变化。

1. **S1 — AMD × Moonshot：Rebuilding Agentic AI from First Principles for AMD GPU** — [打开来源](https://www.amd.com/en/developer/resources/technical-articles/2026/rebuilding-agentic-ai-for-amd-gpu.html)
2. **S2 — AMD ROCm Infera 官方介绍** — [打开来源](https://rocm.blogs.amd.com/software-tools-optimization/infera-di/README.html)
3. **S3 — AMD-AGI/Infera 仓库** — [打开来源](https://github.com/AMD-AGI/Infera)
4. **S4 — Infera 2026 Q3 Roadmap** — [打开来源](https://github.com/AMD-AGI/Infera/issues/9)
5. **S5 — ROCm/MORI 仓库与 2026 H2 Roadmap** — [仓库](https://github.com/ROCm/mori) · [Roadmap](https://github.com/ROCm/mori/issues/348)
6. **S6 — MORI-IO Guide** — [打开来源](https://github.com/ROCm/mori/blob/main/docs/MORI-IO-GUIDE.md)
7. **S7 — MORI-EP Guide** — [打开来源](https://github.com/ROCm/mori/blob/main/docs/MORI-EP-GUIDE.md)
8. **S8 — MORI-UMBP Master Control Plane Design** — [打开来源](https://github.com/ROCm/mori/blob/main/src/umbp/doc/design-master-control-plane.md)
9. **S9 — ROCm AMD Infinity Context** — [打开来源](https://github.com/ROCm/rocm-aic)
10. **S10 — ATOMesh 官方技术文章** — [打开来源](https://www.amd.com/en/developer/resources/technical-articles/2026/atomesh-unlocking-amd-hardware-for-scalable-llm-serving.html)
11. **S11 — ROCm/ATOM 与 ATOMesh** — [ATOM](https://github.com/ROCm/ATOM) · [ATOMesh](https://github.com/ROCm/ATOM/tree/main/atom/mesh)
12. **S12 — ROCm/AITER** — [打开来源](https://github.com/ROCm/aiter)
13. **S13 — Composable Kernel** — [打开来源](https://github.com/ROCm/rocm-libraries/tree/develop/projects/composablekernel)
14. **S14 — RCCL Documentation** — [打开来源](https://rocm.docs.amd.com/projects/rccl/en/latest/)
15. **S15 — SGLang AMD 2026 Q3 Roadmap** — [打开来源](https://github.com/sgl-project/sglang/issues/35003)
16. **S16 — SGLang HiCache Best Practices** — [打开来源](https://docs.sglang.io/docs/advanced_features/hicache_best_practices)
17. **S17 — SGLang P/D Disaggregation** — [打开来源](https://docs.sglang.io/docs/advanced_features/pd_disaggregation)
18. **S18 — vLLM Disaggregated Prefill** — [打开来源](https://docs.vllm.ai/en/latest/features/disagg_prefill/)
19. **S19 — vLLM NIXL KV Push Design** — [打开来源](https://docs.vllm.ai/en/latest/design/nixl_kv_push_connector/)
20. **S20 — AMD Careers 相邻岗位 Req 89398** — [打开来源](https://careers.amd.com/careers-home/jobs/89398?lang=en-us)
21. **S21 — AMD Careers 相邻岗位 Req 87545** — [打开来源](https://careers.amd.com/careers-home/jobs/87545?lang=en-us)
22. **S22 — AMD Careers 相邻岗位 Req 89395** — [打开来源](https://careers.amd.com/careers-home/jobs/89395?lang=en-us)
23. **S23 — AMD Careers 相邻岗位 Req 89498** — [打开来源](https://careers.amd.com/careers-home/jobs/89498?lang=en-us)
24. **S24 — AMD Careers 相邻岗位 Req 89499** — [打开来源](https://careers.amd.com/careers-home/jobs/89499?lang=en-us)
25. **S25 — AMD Careers 相邻岗位 Req 89500** — [打开来源](https://careers.amd.com/careers-home/jobs/89500?lang=en-us)
26. **S26 — Infera main 分支提交历史** — [打开来源](https://github.com/AMD-AGI/Infera/commits/main/)
27. **S27 — MORI main 分支提交历史** — [打开来源](https://github.com/ROCm/mori/commits/main/)
28. **S28 — ROCm AIC main 分支提交历史** — [打开来源](https://github.com/ROCm/rocm-aic/commits/main/)

### 外部贡献专题新增来源（2026-09-07 核验）

29. **S29 — Infera 贡献指南** — [指南](https://github.com/AMD-AGI/Infera/blob/main/CONTRIBUTING.md)
30. **S30 — Infera preflight 去重任务与当前实现** — [Issue #36](https://github.com/AMD-AGI/Infera/issues/36) · [netperf](https://github.com/AMD-AGI/Infera/blob/main/infera/tools/preflight/network/netperf.py) · [fabric](https://github.com/AMD-AGI/Infera/blob/main/infera/tools/preflight/network/fabric.py) · [mooncake_mode](https://github.com/AMD-AGI/Infera/blob/main/infera/tools/preflight/mooncake_mode.py)
31. **S31 — Infera 机内 KV 传输评估** — [Issue #46](https://github.com/AMD-AGI/Infera/issues/46)
32. **S32 — Infera Rust NATS issue 与实际合并状态** — [Issue #88](https://github.com/AMD-AGI/Infera/issues/88) · [PR #113](https://github.com/AMD-AGI/Infera/pull/113)
33. **S33 — Infera KV block 元数据与 renderer parity 已合并案例** — [PR #73](https://github.com/AMD-AGI/Infera/pull/73) · [PR #143](https://github.com/AMD-AGI/Infera/pull/143)
34. **S34 — MORI 与 ROCm 贡献规则** — [MORI README](https://github.com/ROCm/mori#contribution-guide) · [ROCm 通用指南](https://github.com/ROCm/legacy-rocm-build/blob/develop/CONTRIBUTING.md)
35. **S35 — MORI WQE 回绕报告与源码** — [Issue #626](https://github.com/ROCm/mori/issues/626) · [IBGDA kernels](https://github.com/ROCm/mori/blob/main/include/mori/shmem/shmem_ibgda_kernels.hpp)
36. **S36 — MORI CCO window 并发 PR 与未覆盖测试** — [PR #632](https://github.com/ROCm/mori/pull/632)
37. **S37 — MORI 连续异步 dispatch/combine 故障报告** — [Issue #342](https://github.com/ROCm/mori/issues/342)
38. **S38 — MORI 外部参与与重叠任务实例** — [Issue #507](https://github.com/ROCm/mori/issues/507) · [维护者回复](https://github.com/ROCm/mori/issues/507#issuecomment-5268237967) · [PR #621](https://github.com/ROCm/mori/pull/621) · [Moreh PR #92](https://github.com/ROCm/mori/pull/92)
39. **S39 — MORI async 与 SymmetricMemory 当前进展** — [RFC #572](https://github.com/ROCm/mori/issues/572) · [RFC #557](https://github.com/ROCm/mori/issues/557) · [PR #544](https://github.com/ROCm/mori/pull/544) · [PR #628](https://github.com/ROCm/mori/pull/628)
40. **S40 — AIC 贡献指南与仓库功能开关** — [CONTRIBUTING](https://github.com/ROCm/rocm-aic/blob/main/CONTRIBUTING.md) · [仓库 API](https://api.github.com/repos/ROCm/rocm-aic)
41. **S41 — AIC 日志任务与监控配置** — [Issue #118](https://github.com/ROCm/rocm-aic/issues/118) · [monitoring compose](https://github.com/ROCm/rocm-aic/blob/main/monitoring/docker-compose.monitoring.yml)
42. **S42 — AIC 已指派的 CI/benchmark 任务** — [Issue #115](https://github.com/ROCm/rocm-aic/issues/115) · [Issue #114](https://github.com/ROCm/rocm-aic/issues/114) · [Issue #110](https://github.com/ROCm/rocm-aic/issues/110)
43. **S43 — AIC 2026-09-06 已合并的低硬件门槛案例** — [Docker PR #151](https://github.com/ROCm/rocm-aic/pull/151) · [benchmark PR #139](https://github.com/ROCm/rocm-aic/pull/139) · [当前 CPU tests](https://github.com/ROCm/rocm-aic/blob/main/tests/test_run_cliff.py)
44. **S44 — AIC emulation 历史分支与 accuracy PR** — [PR #150](https://github.com/ROCm/rocm-aic/pull/150) · [PR #147](https://github.com/ROCm/rocm-aic/pull/147)。#150 的新状态与承接关系见 S58。
45. **S45 — SGLang 官方贡献入口与 sglang-amd fork 身份** — [贡献指南](https://docs.sglang.io/docs/developer_guide/contribution_guide) · [upstream](https://github.com/sgl-project/sglang) · [个人 fork](https://github.com/JohnQinAMD/sglang-amd)
46. **S46 — SGLang P/D bootstrap 报告和 CPU 验证 PR** — [Issue #33088](https://github.com/sgl-project/sglang/issues/33088) · [PR #33114](https://github.com/sgl-project/sglang/pull/33114)
47. **S47 — vLLM AITER allreduce 阈值契约** — [Issue #55344](https://github.com/vllm-project/vllm/issues/55344) · [PR #55347](https://github.com/vllm-project/vllm/pull/55347)
48. **S48 — SGLang host/device pointer 契约在研工作** — [PR #36966](https://github.com/sgl-project/sglang/pull/36966)
49. **S49 — vLLM allreduce 新版复测与已合并集成** — [Issue #53136](https://github.com/vllm-project/vllm/issues/53136) · [PR #46065](https://github.com/vllm-project/vllm/pull/46065)
50. **S50 — SGLang/MORI/AITER 跨层准确率定位历史** — [Issue #27194](https://github.com/sgl-project/sglang/issues/27194) · [AITER PR #4420](https://github.com/ROCm/aiter/pull/4420) · [AITER PR #4587](https://github.com/ROCm/aiter/pull/4587)
51. **S51 — vLLM 贡献要求与 CI 规则** — [贡献指南](https://docs.vllm.ai/en/latest/contributing/)

### 2026-09-14 新增与复核来源

52. **S52 — GPU Fleet Management 官方岗位** — [Req 92051](https://careers.amd.com/careers-home/jobs/92051?lang=en-us)。官方正文、Apply 与 JobPosting 元数据：09-10 发布、San Jose、Hybrid、无签证赞助。
53. **S53 — MORI #626 实际修复** — [#653](https://github.com/ROCm/mori/pull/653) · [Issue #626](https://github.com/ROCm/mori/issues/626) · [main serial atomics](https://github.com/ROCm/mori/blob/main/include/mori/core/transport/rdma/device_primitives.hpp) · [回绕测试](https://github.com/ROCm/mori/blob/main/tests/cpp/cco/test_gda_wraparound.cpp)。PR 创建 09-09、合并 09-11；作者 QizhouZhang97。
54. **S54 — MORI 跨节点 EP v2 preview** — [#625](https://github.com/ROCm/mori/pull/625)。09-11 合并；PR 正文含设备/NIC、wave64、量化限制、GPU-free 与双节点验证边界，未将作者报告当独立复现。
55. **S55 — MORI UMBP 与可靠性变化** — [#540](https://github.com/ROCm/mori/pull/540) · [#644](https://github.com/ROCm/mori/pull/644) · [#650](https://github.com/ROCm/mori/pull/650) · [被撤回的 #645](https://github.com/ROCm/mori/pull/645) · [revert #661](https://github.com/ROCm/mori/pull/661)。以 main 提交链判断有效变化。
56. **S56 — InferaSim** — [#138](https://github.com/AMD-AGI/Infera/pull/138) · [当前 README](https://github.com/AMD-AGI/Infera/blob/main/infera/projection/README.md)。09-10 合入；README 同时说明无 GPU 默认路径与 Origami/ROCm 模式限制。
57. **S57 — Infera worker/NATS 失败处理** — [#162](https://github.com/AMD-AGI/Infera/pull/162) · [当前 BaseEngine / EngineDeath](https://github.com/AMD-AGI/Infera/blob/main/infera/engine/base.py)。09-09 合入；PR test plan 未勾选，FILE→MEMORY 的持久性变化单独标注。
58. **S58 — AIC emulation、版本与 ABI** — [#150 关闭讨论](https://github.com/ROCm/rocm-aic/pull/150) · [承接 #154](https://github.com/ROCm/rocm-aic/pull/154) · [#145](https://github.com/ROCm/rocm-aic/pull/145) · [README](https://github.com/ROCm/rocm-aic/blob/main/README.md) · [Dockerfile](https://github.com/ROCm/rocm-aic/blob/main/docker/Dockerfile) · [accuracy #147](https://github.com/ROCm/rocm-aic/pull/147)。#154 创建 09-08、09-09 合并，作者/assignee sbates130272；#147 普通 CI 与 accuracy 触发语义须分开。
59. **S59 — AIC benchmark/监控** — [kvbench #158](https://github.com/ROCm/rocm-aic/pull/158) · [monitoring #159](https://github.com/ROCm/rocm-aic/pull/159) · [当前 cliff 客户端](https://github.com/ROCm/rocm-aic/blob/main/benchmarks/run_cliff.py)。不把缺失指标记成零，不重复已合入逻辑。
60. **S60 — ATOM/ATOMesh 本期变化** — [CPP/DCP KV #2121](https://github.com/ROCm/ATOM/pull/2121) · [TTFT/ITL #2165](https://github.com/ROCm/ATOM/pull/2165)。分别于 09-10 / 09-09 合并。
61. **S61 — upstream 实现与验证状态** — [vLLM elastic EP #56610](https://github.com/vllm-project/vllm/pull/56610) · [DP AG/RS #48247](https://github.com/vllm-project/vllm/pull/48247) · [KV connector #53695](https://github.com/vllm-project/vllm/pull/53695) · [SGLang UMBP fixture #38672](https://github.com/sgl-project/sglang/pull/38672) · [MI355X nightly 暂停 #39044](https://github.com/sgl-project/sglang/pull/39044) · [当前 workflow](https://github.com/sgl-project/sglang/blob/main/.github/workflows/nightly-amd-mi355x-disagg.yml)。
62. **S62 — AMD 官方 09-08 技术文章** — [NVFP4→Quark MXFP4 online requantization](https://rocm.blogs.amd.com/software-tools-optimization/nvfp4-to-mxfp4/README.html)。读取正文，不以标签页摘要作为技术结论。
63. **S63 — SGLang lifecycle 已有工作与评论** — [#38164](https://github.com/sgl-project/sglang/pull/38164) · [#38704](https://github.com/sgl-project/sglang/pull/38704) · [#38961 及维护者的重叠分析](https://github.com/sgl-project/sglang/pull/38961) · [当前 decode 源码](https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/disaggregation/decode.py)。#38164 创建 09-06、本期首次收录，不称本周新发布；#38704/#38961 为本周新 PR。
64. **S64 — MORI benchmark 生命周期评审机会** — [#665](https://github.com/ROCm/mori/pull/665) · [#659](https://github.com/ROCm/mori/pull/659) · [#660](https://github.com/ROCm/mori/pull/660) · [#664](https://github.com/ROCm/mori/pull/664)。#665 创建/更新 09-12，作者 jhchouuu；其它条目为开放列表中的相邻 tuning/bench 工作，不将标题当完整实现审计。

### 上游合入记录

- [vLLM MORI-IO](https://github.com/vllm-project/vllm/pull/29304)
- [vLLM MORI-EP](https://github.com/vllm-project/vllm/pull/28664)
- [SGLang MORI-IO](https://github.com/sgl-project/sglang/pull/14626)
- [SGLang MORI-EP](https://github.com/sgl-project/sglang/pull/17012)
- [SGLang UMBP / HiCache](https://github.com/sgl-project/sglang/pull/25377)

---

## 18. 后续维护建议

每次例行检查都保存同一文件的新版本，在文档开头更新研究日期与版本记录；没有实质变化时明确记录检查范围与日期，不以发现变化为执行条件。重点检查：

- [ ] 是否出现 exact Req ID；
- [ ] Infera roadmap 是否关闭或新增关键 issue；
- [ ] MORI H2 roadmap 的完成状态；
- [ ] UMBP 在 vLLM / SGLang 的 upstream 状态；
- [ ] AIC 是否从 preview 进入更稳定阶段；
- [ ] MI45x / Helios 支持状态；
- [ ] 是否出现新的 Rust / C++ 职责拆分；
- [ ] 个人是否新增 ROCm、Rust、SGLang 或公开 PR 证据；
- [ ] 面试反馈是否揭示真实团队边界；
- [ ] 第 19 节贡献候选的负责人、相关 PR、合并/关闭状态和当前源码是否变化；
- [ ] 是否存在 Issue 仍 Open 但工作已合并、或已有未关联 PR 的情况；
- [ ] 更新外部贡献首选三项、硬件门槛和个人实际进展，已解决任务保留历史。

建议把后续面试反馈按以下格式补充：

~~~text
日期：
面试轮次：
面试官方向：
重点问题：
回答不足：
新的岗位信息：
需要补习：
下一步行动：
~~~

---

## 19. 外部开发者参与 AMD 开源项目：入口、机会与执行路线

> 核验日期：2026-09-14。以下是公开贡献机会研究，未替用户发出评论、创建 Issue 或提交 PR，也未在 AMD 硬件上复现问题。Issue / PR 的日期默认使用 GitHub API 的 UTC 日期；状态是检查时快照。当前首选见 19.11；09-07 的机会判断已按实际合入和重叠工作同步纠正。

### 19.1 结论：可以参与，你的优势适合哪些贡献

**可以，而且你的 ProcessGroupDLCCL、C++ Extension、custom allreduce、CUDA IPC、NCCL 源码和并发故障定位经历，能直接用于通信正确性、框架接口和资源生命周期问题。** 不必先成为 Rust 专家或拥有大规模 AMD 集群，才开始贡献；但设备通信、HIP 地址可达性和性能结论仍需要匹配的实机验证。

这里把“能提 Issue / PR”拆成三件事：项目是否欢迎外部贡献、账号是否有相应操作权限、当前问题是否仍需要人做。公开仓库、Open 状态、没有 assignee，都不能单独回答全部三件事。

**已确认事实：** Infera、MORI、AIC 及 SGLang upstream 均有贡献说明；AIC 明确接受外部 fork PR。MORI PR #92 明确来自 Moreh Inc. 团队，并有维护者交流，但检查时仍未合并。AIC #151、#139 已于 2026-09-06 合并，两份 PR 均明确说明局部验证未使用 AMD GPU，证明硬件无关的构建或测试改进也能合入。[S29][S34][S38][S40][S43][S45]

**强关联推断：** 对你而言，小而完整的通信/框架工程贡献，比从零承接整个 scheduler、global KV pool 或 EP v2 更容易形成可信的面试证据。第一份贡献应优先追求“能复现、能解释、能验证”，之后再扩展范围。

**待维护者确认：** 任务是否已有内部 owner、是否接受拟议拆分、目标分支、兼容范围、能否协助运行 AMD CI。**待招聘方确认：** 某项贡献与截图岗位的实际团队关系，以及它在面试中的权重。贡献不能替代 exact Req 的核验，也不能保证面试或录用。

### 19.2 仓库入口与贡献门槛

| 项目 | 建议的正式入口 | 外部参与依据与流程 | 无 AMD GPU 时能先做什么 |
|---|---|---|---|
| Infera | [AMD-AGI/Infera](https://github.com/AMD-AGI/Infera) | fork 后向 main 提 PR；行为变更附测试；每个 commit 做 DCO sign-off；Python/Rust 有各自格式检查。[S29] | preflight 解析、配置、路由契约、取消和错误路径单测、文档与示例 |
| MORI | [ROCm/mori](https://github.com/ROCm/mori) | README 欢迎修复、功能、文档和反馈；允许 fork PR；使用 pre-commit；仓库自己的 main 与通用 ROCm 说明结合阅读。[S34] | 源码风险分析、队列边界模型、构建复现、宿主端测试；真实 HIP/RDMA 行为另验 |
| AIC | [ROCm/rocm-aic](https://github.com/ROCm/rocm-aic) | CONTRIBUTING 明确外部开发者使用 fork，PR 需 CI 通过及至少一位 code owner 批准。[S40] | Docker/构建、benchmark 客户端、配置、监控日志、CPU 测试；完整栈仍是 preview |
| SGLang 的 AMD 工作 | [sgl-project/sglang](https://github.com/sgl-project/sglang)，结合 AMD roadmap #35003 | upstream 贡献指南与 AMD roadmap 均支持社区参与；fork PR、pre-commit、回归测试；GPU CI 有维护者门禁。[S15][S45] | P/D bootstrap、scheduler 状态机、配置和错误传播单测 |
| vLLM 的 AMD 工作 | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 按 upstream 贡献指南提交，DCO、清楚的测试计划与结果；AMD CI 需对应权限。[S51] | communicator 选择条件、阈值/配置契约、CPU mock 与最小复现准备 |

**“sglang-amd”需要先辨明身份。** 本次找到的 [JohnQinAMD/sglang-amd](https://github.com/JohnQinAMD/sglang-amd) 是个人账号下的 upstream fork。名称含 AMD 不证明它是独立的官方贡献入口。没有维护者明确指向该 fork 时，默认在 upstream 查问题和提交贡献。[S45]

**文档意图与账号权限存在边界。** Infera 指南说非 AMD 人员成为仓库 collaborator 需要管理员批准；这与文档列出的 fork PR 流程是两回事。其示例邮箱也不能理解为必须有 AMD 邮箱。匿名页面曾显示 Infera/AIC 新建 Issue 受限提示，不能据此断言所有外部账号都被禁止，也不能保证用户登录后一定有权限。AIC 指南推荐 feature request 走 Discussions，但本次仓库 API 显示 Discussions 未开启；这一路径需要维护者澄清。实际权限不足时，使用项目当前允许的讨论入口，不尝试绕过限制。[S29][S40]

**09-14 权限复核：** Infera/AIC 贡献指南、MORI README 仍欢迎上述贡献流程；AIC `has_discussions=false`，个人 `JohnQinAMD/sglang-amd` 仍是 `sgl-project/sglang` 的 fork 且自身 Issues 未启用。SGLang 当前指南允许作者对自己的 PR 使用 `/rerun-failed-ci`，但加 CI 标签、完整/选择性运行仍有不同权限；这不等于能自行获取 AMD runner。新增 CPU CI 用例应遵守 `CustomTestCase`、`register_*_ci` 和脚本入口约定。MI355X P/D 夜测资源暂停需另行确认可运行性；本研究未测试用户账号权限。[S45][S61]

### 19.3 当前机会清单：先区分任务状态，再选切口

“未见重叠 PR”表示在本次公开正文、评论、相关 PR 列表和源码定向检查中未识别直接重复，仍可能遗漏未关联或内部工作；不是可立即独占认领的承诺。以下优先级针对你的经历与可复现性，属于研究建议。

| 优先级 / 类型 | 入口与日期 | 2026-09-14 状态 | 建议交付与硬件条件 |
|---|---|---|---|
| **P0，现有任务** | [Infera #36：RDMA preflight 探测去重](https://github.com/AMD-AGI/Infera/issues/36)；创建 07-29，更新 08-03 | Open，无 assignee；当前源码仍重复实现，未发现承接该抽取工作的 PR | 共享 GID/sysfs/netdev 探测函数，迁移调用点并保留单文件运行兼容。**核心可 CPU 单测**；真实 RoCE 验证另行安排。[S30] |
| **历史：已修复，不再认领** | [MORI #626](https://github.com/ROCm/mori/issues/626)；创建 09-01，更新 09-09；[#653](https://github.com/ROCm/mori/pull/653) 于 09-11 合并 | Issue 仍 Open，已指派 QizhouZhang97；其评论表示将复现。修复与回绕测试已在 main，不受 issue 状态滞后影响 | 学习 serial order、CQ 重建、完成计数；不重复修复或复制已有边界测试。CPU 只能检验模型，真实 IBGDA quiet/drain 仍需 AMD + RDMA。[S35][S53] |
| **P1，协作补测** | [MORI PR #632：CCO window 加锁](https://github.com/ROCm/mori/pull/632)；创建/更新 09-02 | Open，作者 jhchouuu 已提交修复；正文明确缺并发 register/deregister 测试 | 与作者讨论补充并发回归测试；主机模型可先分析，实际 collective/HIP VMM 路径通常需本机多 AMD GPU。**不重复写已有加锁修复。**[S36] |
| **P1，已有工作评审，非空白提案** | [SGLang #33114](https://github.com/sgl-project/sglang/pull/33114)（07-31）；[#38164](https://github.com/sgl-project/sglang/pull/38164)（创建 09-06，更新 09-08）；[#38704](https://github.com/sgl-project/sglang/pull/38704)（创建/更新 09-09） | 均 Open；作者分别 guptaishaan / ormandj / kflansburg。#38164 已有 preallocation timeout + CPU Gloo 测试；#38704 已有 admission abort/length-consensus 草案 | 先列跨 PR 责任/覆盖矩阵，只讨论剩余场景；不重做 timeout、取消或现有 66 测试。main 的 bootstrap 路径已演进，旧 patch/命令需 rebase。CPU 模型不验证真实 KV/RDMA。[S46][S63] |
| **P1，有卡时协作** | [vLLM #55344 / PR #55347](https://github.com/vllm-project/vllm/pull/55347)；创建/更新 09-04 | 均 Open，stefanskiasan 已提交 AITER AR 阈值/融合边界修复 | 评审 runtime cutoff、IPC pool 与编译范围的契约；先核对已有用例再补测试。CPU 验配置，**融合/fallback 正确性需 ROCm 多卡**。[S47] |
| P2，现有评估任务 | [Infera #46：机内 KV xGMI/remote-copy 评估](https://github.com/AMD-AGI/Infera/issues/46)；创建 07-30，更新 08-03 | Open，无 assignee；未见明确关联 PR | 做有限范围的两进程 KV transfer 对比报告。**需 AMD 多卡/xGMI**；不是从零重写已有下层传输库。[S31] |
| P2，现有问题复测 | [MORI #342：连续异步 dispatch/combine fault](https://github.com/ROCm/mori/issues/342)；创建/更新 05-30 | Open，无 assignee；没有直接修复关联，但 #92 已涉及重复调用测试 | 在当前 main 复跑后再定位，避免与 #92 重叠。原复现需 **4 块本机 ROCm GPU**，不必加载大模型。[S37][S38] |
| P2，AIC 工具侧任务 | [AIC #118：日志接入 telemetry harness](https://github.com/ROCm/rocm-aic/issues/118)；创建/更新 08-06 | Open，无 assignee、无评论；本次 PR 检查未见 Loki 实现 | 先商定最小日志接入、查询和验收范围；Docker 假服务可先验证，不要求 GPU。与底层通信的直接相关性低于前三项。[S41] |
| P2，AIC 历史与在研分开 | [#150](https://github.com/ROCm/rocm-aic/pull/150) 创建 09-03、09-09 关闭；[#154](https://github.com/ROCm/rocm-aic/pull/154) 09-09 合并；[#147](https://github.com/ROCm/rocm-aic/pull/147) 创建 08-31、更新 09-09 | #150 非合并关闭、sbates130272 指派；#154 承接。#147 Open、作者 john00003、有 9 条评论；作者 09-08 说明 accuracy 尚未接入对应 CI，仍在排查 | emulation 现为 main 学习入口；#147 的普通 Hardware CI pass 不证明 accuracy 已跑通。可讨论补测，但不把模型测试等同 KV 一致性证明。[S44][S58] |
| P2，深度评审 | [SGLang PR #36966：host/device pointer 契约](https://github.com/sgl-project/sglang/pull/36966)；创建 08-29，更新 08-31 | Open，Lzy17 已有实现，且存在前序 PR 依赖 | 评审注册、device alias、tensor view 与释放顺序；很贴合 IPC 经验。真实 GPU/RDMA 地址可达性需 AMD 多机，首 PR 不宜接整条依赖链。[S48] |
| P2，本周新 PR 的评审机会 | [MORI #665：warmup/timed tensor lifetime](https://github.com/ROCm/mori/pull/665)；创建/更新 09-12 | Open，作者 jhchouuu，无 assignee；已有实现与双节点实验；同题 #659/#660/#664 也在推进 | 评审 warmup 与计时循环的引用寿命、allocator segment 变化、paired runs。CPU 可解释 Python 引用次序，实际复现需 2×8 MI308X/相当配置与 RDMA；不是无人实现的优化。[S64] |
| P2，新提案，先核对范围 | [AIC #158](https://github.com/ROCm/rocm-aic/pull/158) 与 [构建源码](https://github.com/ROCm/rocm-aic/blob/main/docker/Dockerfile) | #158 已合并；当前 README 的 AITER wheel 描述与 Dockerfile source build 不一致。本次开放 PR 列表未见直接文档修正，但未公开工作仍未知 | 可先写 ABI 说明修正建议、kvbench 缺失指标/异常样本的覆盖矩阵；CPU 适合文档/解析测试。既有留空处理已实现，不能再“修复”一次。[S58][S59] |

### 19.4 首个贡献首选：Infera #36

它是一个边界清楚的维护任务。Issue 明确说这是代码重复和维护债，**没有宣称已发生运行故障**。当前 `netperf.py`、`fabric.py`、`mooncake_mode.py` 各有 GID 选择相关实现，接口返回值也不同。你可以用设备与网络排障经验做一份完整的工程改进。[S30]

**09-14 源码核验的重要补充：** 重复确实仍在，但不能照 Issue 的一句“相同策略”机械合并。`netperf._gid_index` / `fabric._roce_v2_gid` 在遍历遇到 global IPv6 时直接返回，并保留 link-local 作为末级 fallback；`mooncake_mode._routable_gid` 优先 IPv4-mapped、跳过 link-local，且枚举全部数字 GID 槽，而前两者扫描前 16 个。返回缺省值也不同。建议先将“共同读取机制”和“调用者策略”分层：首个 PR 保持各调用者原行为，策略统一另提讨论。这是当前代码差异，不是本研究已证明的运行故障。[S30]

建议先在本地形成以下交付，再带着具体方案参与讨论：

1. 列出调用点与返回契约，确定共享模块位置；不随意改变原有优先顺序。
2. 抽取设备枚举、netdev 映射和 RoCE-v2 GID 选择，保留需要单独拷入裸容器执行的 fallback import。
3. 用临时目录模拟 sysfs，用 mock 提供 `rdma link show` 输出；覆盖 IPv4-mapped 与 global IPv6 同时存在、各调用者不同的 link-local 策略、超过 16 个槽、无设备和文件缺失。先以旧实现为行为对照，不自行改变探测优先级。
4. 报告哪些测试已在 CPU 通过、哪些行为还需要真实 NIC 验证；如果发现原函数本来就有差异，先判断是契约差异还是缺陷，避免在“去重”里隐含改行为。

**简历价值：** 能证明你把通信环境知识转化成可维护接口与回归测试。它对底层性能深度的证明有限，因此适合作为进入项目的第一步，之后用 MORI 或 vLLM 通信问题形成第二个更强案例。

### 19.5 最贴合专业优势：MORI 完成语义与资源生命周期

**#626：已修复的学习案例，撤下待认领建议。** 09-09 已指派 QizhouZhang97；#653 于 09-11 合并，main 中可见 `AtomicMaxSerial`、CQ serial 重建及 `test_gda_wraparound.cpp`。上一版“无 assignee、未见同题 PR”已过期。现在适合对照修复前后学习，不能另发同题补丁，也不能声称自己发现或修复了该问题。[S35][S53]

学习材料可以列出 post、doorbell、done 的合法状态与模运算范围，对照已合并回归用例和 quiet/drain 的完成条件。尤其要写清“在途距离小于序号空间一半”等比较前提，不能把 signed 差值技巧机械替换到所有位置。CPU 模型、宿主线程模型、GPU 真实队列是三个不同的验证层级；新增测试必须证明没有与 #653 的现有覆盖重复。

**#632：已有修复明确缺测试，是很好的协作切口。** 作者描述 window 注册/注销与共享容器并发访问风险，并说明现有测试没有覆盖同一个 `ccoComm` 上的并发注册/注销。可讨论针对两线程、GC 释放、allocator 操作交错的测试，先保证各 rank 的 collective 调用顺序可控，避免测试本身制造无效协议。[S36]

09-14 复核：#632 仍 Open，创建/更新均 09-02，无 assignee、无讨论评论，但作者 jhchouuu 已提供补丁；当前 main 的 register 查表路径尚未包含该补丁的 lock。补测应同时分析“解锁后保存元素引用”的生命周期前提：rehash 不使引用失效，不等于允许对象被另一线程 erase/free。后者是需要确认 API 契约的评审问题，不在没有复现的情况下直接宣称新 UAF。

这与你处理 ProcessGroup Work、C++ 对象生命周期、IPC buffer 复用、barrier 和 UAF 的经历直接对应。使用 sanitizer 有价值，但宿主端 sanitizer 的通过不能证明 GPU 侧同步或远端写入正确。

**长期主线：MORI #572 的 async/shared-expert overlap。** 可以先贡献接口和完成语义分析，再讨论小范围实现；这是跨 MORI、vLLM、AITER 的工作，不能通过简单修改能力布尔值就宣称支持 overlap。与现有 #342、#92 的异步正确性问题一起看，更容易形成完整设计判断。[S39]

### 19.6 SGLang/vLLM：用已有经验进入 upstream

**没有 AMD 卡时，SGLang P/D 失败路径可从评审开始，但不能再当作空白任务。** #33114 仍 Open，作者的 CPU 节流测试不能视作当前 main 全部状态；main 已有 `_prefill_dp_rank_queries`、取消/预取等演进。更重要的是 #38164 已实现分配前超时与 rank consensus，#38704 已推进 admission abort 与长度共识，#38961 已推进 deferred KV release，不能重复提一份泛化 timeout/abort 修复。[S46][S63]

建议先写状态/覆盖表：连接失败、worker 未就绪、rank 未注册、请求已取消、整体超时、部分 rank 已终止，逐项对应 main 和现有 PR。#38164 已有两进程 CPU Gloo 超时共识测试；作者在 09-08 评论说明将重叠 admission 工作交回 #35645。#38961 的维护者 09-12 明确指出与 #37077 重叠，并区分“延迟回收”与“潜在内存破坏”，跨 backend/scheduler 行为需协调。先贡献独立评审、复测或维护者接受的遗漏用例，不重做已有测试套件；两进程 Gloo 也不证明 RDMA 已 quiesce。[S63]

本次元数据快照：#38164 创建 09-06、更新 09-08，Open 非 Draft，作者 ormandj、无 assignee、2 条讨论评论；#38704 创建/更新 09-09，Open Draft，作者 kflansburg、无 assignee、0 条讨论评论；#38961 创建 09-11、更新 09-12，Open Draft，作者 kflansburg、已指派 ShangmingCai、1 条详细维护者评论。后两者的 AST/fake/Gloo 验证各有依赖和范围限制，不能表述成完整 runtime/GPU/RDMA 回归通过。

**有 AMD 多卡时，vLLM AITER allreduce 更能展示你的已有深度。** #55347 涉及运行时 cutoff、IPC pool 和编译范围之间的一致性。先检查 PR 已覆盖的边界，再讨论新增用例；PR 后续提交已处理 0 值导致无效编译范围的问题，不能再列成无人修复漏洞。[S47]

另一个入口是 #53136 的新版复测。最新维护者回复认为已合并 #46065 的 AITER 路径应覆盖原问题，要求换新版验证。因此可贡献的是固定 commit/image、确认实际 communicator、将请求缩成 message-size sweep 后报告结果，不能把原“8–16 MiB 缺口”直接写成当前缺陷。[S49]

### 19.7 AIC：低硬件门槛存在，但应选择与目标相关的工作

AIC #151 是有参考价值的合入案例：用最小 Docker 构建场景验证 named build context 的默认行为，作者明确没有做完整 AMD 镜像验证。#139 则修正 benchmark 请求失败却返回成功的问题，使用局部 HTTP/单元测试。这说明**诚实限定验证范围的小修复也有价值**，而不是必须先跑起整个分层 KV 栈。[S43]

如果选择 #118，建议把目标限定为：给现有监控增加一条可运行的日志采集与查询路径，配套容器样例、配置校验和说明。这里的最小验收是能从模拟服务的一条错误日志追到查询结果；不要在首个 PR 同时重做完整观测平台。[S41]

以下条目已有人推进，应先讨论分工：#115 CI 脚本更新行为已指派 sbates130272 与 john00003；#114 NIXL benchmark/report、#110 八卡测试已指派 john00003。#115 涉及自托管 runner 对不可信 PR 代码的信任边界，不能以直接取消门禁来“修复”流程。[S42]

**纠正 #150 的旧状态：** #150 于 09-09 非合并关闭，关闭评论明确指向替代 #154；后者同日合并，emulation 已进入 main。现在可研究真实代码与 CPU smoke，而非继续评审旧分支是否应合入。其 profile 仍不是真实 GPU 测量。#147 仍 Open；09-08 作者明确 accuracy 测试未接入相应 CI，评论触发的是普通 CI，不能将普通 Hardware CI pass 当成 accuracy pass。更低层 KV checksum/一致性测试仍需先核对覆盖并与作者商量。[S44][S58]

本期可形成的新提案：README 写 AITER 使用 ROCm wheel，但 Dockerfile 的实际命令从 pinned ref 编译 AITER 以匹配源码 torch-2.13，适合做“文档/构建契约一致性”修正建议；#158 新增 kvbench 后，可分析不支持指标、请求失败与输出格式的测试覆盖。已有指标留空和异常处理不重复实现。#118 日志接入任务仍 Open、无 assignee/评论；09-10 的 #159 修改了监控网络，未来方案需基于新 main，不照旧 Compose 接线。[S58][S59]

### 19.8 历史与重叠工作：这些不应重复认领

| 条目 | 交叉核验结果 | 应采取的态度 |
|---|---|---|
| Infera #88，Rust NATS transport | Issue 仍 Open，但 #113 已于 2026-08-12 合并，加入相关 NATS/Kubernetes 路径。[S32] | 学代码或协助核对过期说明；不要从零重做 |
| MORI #626 / #653 | #626 仍 Open、已指派；#653 于 09-11 合并，main 有修复与测试。[S53] | 已解决的历史案例，不再列当前待认领 |
| AIC #150 / #154 | #150 于 09-09 Closed 且 `merged=false`；#154 同日合并承接 emulation。[S58] | 不把 Closed 当 merged，也不把已合入功能仍称 roadmap |
| SGLang #33114 与 lifecycle 新 PR | #38164/#38704/#38961 等已有作者；维护者指出 #37077 等重叠。[S63] | 旧“新提案”降为协作评审，保留历史纠正 |
| vLLM #56610 / #48247 / #53695 | 分别于 09-12 / 09-11 / 09-10 合并。[S61] | 弹性 EP 顺序、DP AG/RS、KV layout 的学习案例，非待修 bug |
| Infera KV block/renderer 边界 | #73 已于 08-02、#143 已于 09-04 合并相关修复和测试。[S33] | 用你对 block size/prefix cache 的理解寻找真正遗漏；不能重复已有 parity 用例 |
| MORI #507，接收索引 | 有维护者欢迎静态分析作者提 PR，但 #621 已于 08-31 提交同题修复，当前 Open Draft。[S38] | 适合独立复核、回归测试和硬件复测，不能重复提交同一行修复 |
| MORI #557，SymmetricMemory/CCO | #544 于 08-26、#628 于 09-02 已合并关键阶段。[S39] | 读当前代码及 remaining gaps，不照旧 RFC 认领整个项目 |
| MORI #92，Moreh 团队 EP 测试 | 有明确外部公司参与证据，但仍 Open。[S38] | 是协作实例，不是“已经合入”的成功案例 |
| SGLang #27194，MORI buffer/准确率 | 后续评论修正了早期根因判断，指向 AITER #4420/#4587 的修复。[S50] | 作为跨层定位案例，不列为当前无主 bug |
| AIC #139/#151 | 2026-09-06 已合并。[S43] | 学习贡献方式；本轮不再推荐相同修复 |

**维护原则：** Issue 状态、Development 栏、PR 标题、评论、合并时间和当前源码必须相互核对。Closed PR 也不等于 merged，需检查实际 merged 字段。别人声明的复现、性能或根因应注明来自报告者，本研究没有跑过的测试不能写成自己验证。

### 19.9 两周执行计划与贡献材料

不预设你已有 AMD 设备。建议只选一个主任务和一个后备，避免同时认领多个仓库的工作。

| 阶段 | 无 AMD GPU 的默认路线 | 如果已有 AMD 多卡 |
|---|---|---|
| 第 1–2 天 | 重查 Infera #36 的状态与 PR；阅读调用点、跑相关测试、写一页修改范围 | 同时确认 MORI #632 或 vLLM #55347 的分工与所需版本 |
| 第 3–5 天 | 完成局部 patch 和前后行为/回归证据；准备讨论或 PR 草稿 | 将原有故障缩成小脚本，记录 GPU/NIC/拓扑、实际 backend 与同步条件 |
| 第 6–8 天 | 根据维护者意见收窄范围，完成格式、测试和说明；无回复时继续本地验证，不重复催问 | 做正确性、边界尺寸、迭代次数、释放顺序等矩阵；保留失败日志 |
| 第 9–14 天 | 整理一页“问题—契约—方案—验证—限制”。第二条研究线选 MORI #653 已合并案例，或 #632 / SGLang #38164 的覆盖评审；对外发布须另获用户授权 | 增加必要性能对照与真实通信测试；同步记录回归和适用范围 |

上述时间是准备节奏，**不是合并时长承诺**。维护者响应、CI 和硬件验证可能延长周期。准备投递可同步推进，不必等 PR 合并后才申请。

进入项目时按最新贡献指南运行相关检查。Infera 明确区分 CPU 单测与 GPU E2E；SGLang 有 CPU unit suite。以下是指南中的入口示例，依赖安装和测试范围以当前仓库为准；本次研究未执行这些命令。[S29][S45]

```bash
# Infera：安装相应开发依赖后，在仓库目录运行
pytest -m "not slow and not integration"

# SGLang：安装相应开发依赖后，在仓库目录运行
python3 test/run_suite.py --hw cpu --suite base-a-test-cpu
```

外部 PR 的 AMD CI 可能需要维护者触发；没有触发权限、跳过测试和真正测试失败应分开记录。不要把 CPU 通过写成 GPU 通过，也不要预设社区一定免费提供机器。使用 AI 辅助时，遵守目标项目的披露与人工验证要求；最终提交者必须能解释并验证每一项改动。[S45][S51]

以下英文材料仅为可编辑草稿，未对外发送。使用时填写实际结果，不保留无依据的完成声明。

**确认任务范围：**

```text
I'm interested in contributing to this issue. I have experience with
PyTorch ProcessGroup backends, C++ extensions, and GPU communication.

I propose a small change covering [specific scope], with regression tests
for [cases]. I can validate [available environment]; [hardware-dependent
cases] would still need ROCm validation.

Is anyone already working on this scope, and would this split be useful?
```

**问题或 PR 的证据清单：**

```text
Problem / expected contract:
Repository commit and related issue/PR:
Environment and actual backend:
Minimal reproduction:
Observed result vs expected result:
Change and why it addresses the cause:
Tests actually run and results:
Not tested / remaining questions:
```

向招聘方展示时，分别标明“分析中 / 已提交 / 评审中 / 已合并”，记录自己负责的部分。一个高质量复现、一个有前后对照的测试或一个解决实际问题的小 PR，都是可讨论的工程证据；不能把尚在研究的 roadmap 写成已完成项目。

### 19.10 对投递与后续跟踪的影响

你的定位仍以 **C++ / 通信 / 推理数据面** 为主。Infera #36 提供低硬件门槛入口；MORI #632 和 vLLM AITER AR 可讨论协作验证，#626/#653 现为已合并学习案例；SGLang P/D 状态机先做既有工作的交叉评审，不能泛化为无人负责。没有新增你已经完成贡献的事实，因此不据此上调个人匹配度百分比，也不保证开源贡献带来面试、合并或录用。

后续每次例行更新应维护本节：新任务、负责人变化、关联 PR、合并/关闭、当前源码是否仍存在问题、硬件门槛、首选三项。已解决条目移入历史并保留链接；没有新增机会也更新核验日期。新增能力和过期 Issue 的纠正必须同步回正文成熟度判断，不能只在贡献清单里改状态。

### 19.11 当前首选三项与可交付范围（09-14）

这些是本地准备与待讨论的参与路线，不构成对外发布授权。优先级综合与你的匹配、任务边界和硬件可验证性，而非仓库热度。

| 排序 | 类型 / 推荐入口 | 本地最小交付 | 不应承诺或重复的内容 |
|---|---|---|---|
| 1 | **Infera #36：现有维护任务，先澄清兼容策略** | 三个 GID picker 的行为矩阵；sysfs 读取与选择策略的拆分方案；临时目录 + fake command 输出的 CPU 回归设计；保留单文件 fallback | 不把 global IPv6/IPv4-mapped/link-local 差异悄悄统一；不宣称修复了已复现生产故障；真实 NIC 验证另列。[S30] |
| 2 | **MORI #632：已有作者的并发补测/评审** | 画出同一 `ccoComm` 的注册、注销、allocator、GC 交错；列出锁保护对象、元素引用寿命与 collective 顺序；先确认允许哪些并发，再提出一个确有遗漏的测试 | 不重复作者加锁实现；无 AMD 多卡时只交契约/模型层材料，不声称真实 HIP VMM、跨 rank 或 sanitizer 全部通过。[S36] |
| 3 | **SGLang #38164 为主：已有 lifecycle 工作的覆盖评审** | 将 #33114/#38164/#38704/#38961 对应到等待、分配、传输、drain、回收；复核已有 CPU Gloo/状态机测试，对真正遗漏的一个场景提出建议 | timeout/abort 已有人实现且有测试，不能另起泛化修复。#38961 已指派 ShangmingCai，维护者要求与 #37077 协调；真实 RDMA drain 无法靠 CPU mocks 证明。[S63] |

**如希望更低风险的无卡备选：** AIC 的 README/Dockerfile ABI 说明一致性是具体新提案；对现有 kvbench 做覆盖分析也是可选项。二者与底层通信的直接相关性稍低，但交付边界更小。InferaSim 可以作为容量模型学习/测试提案入口，先核对当前测试和 Origami 依赖，不能把它包装成“无需硬件就验证 GPU 性能”。[S56][S58][S59]

**新工作来源与身份边界：** 本周 MORI #665、SGLang #38704/#38961 由公开账号提交；仅凭用户名、profile 或 AI 工具声明不能判断其是否 AMD 外部人员。仍以此前 MORI #92 明确披露 Moreh Inc. 的资料作为“外部组织参与”的实例，不推断上述新作者的雇佣身份，也不把未合并工作描述成成功合入。

**本期退出/保留规则：** #626 退出待认领，保留 #653 学习记录；#150 退出在研，保留 #154 承接关系；#33114 保留历史入口，但泛化 timeout 新提案改为已有 PR 协作；#36/#632 保留候选。本次没有代码提交、评论或硬件测试，因此所有“可交付”均为建议而非已完成成果。

**下期重点复核：** #632/#38164 是否合并及 scope 变化；#38961 与 #37077 的去重；#665 与其它 tuning PR 的关系；AIC #147 是否真正接入 accuracy CI；SGLang MI355X 定时夜测是否恢复；Infera #36 是否已有抽取 PR，以及 GID 策略是否经维护者统一。

---


## 结语

这份岗位最有价值的地方，是它恰好连接了两条看似分开的能力线：

- 早期的分布式平台、调度、状态和监控经验；
- 当前的 PyTorch distributed、GPU 通信、vLLM、CUDA IPC 和 kernel 性能工作。

真正需要补齐的不是“重新学习整个大模型推理”，而是把已有底层能力向两个方向延伸：

1. 向上延伸到 Rust 集群控制面、SLO、路由和可靠性；
2. 向 AMD 生态横向迁移到 ROCm、MORI、RCCL、AITER 和 SGLang。

因此，最合理的策略不是等到完全匹配再投，而是：

> 先以 C++ / 通信 / KV 数据面优势进入候选池，同时用 Rust、ROCm 和上游 PR 证明学习速度与方向一致性。

[S1]: https://www.amd.com/en/developer/resources/technical-articles/2026/rebuilding-agentic-ai-for-amd-gpu.html
[S2]: https://rocm.blogs.amd.com/software-tools-optimization/infera-di/README.html
[S3]: https://github.com/AMD-AGI/Infera
[S4]: https://github.com/AMD-AGI/Infera/issues/9
[S5]: https://github.com/ROCm/mori/issues/348
[S6]: https://github.com/ROCm/mori/blob/main/docs/MORI-IO-GUIDE.md
[S7]: https://github.com/ROCm/mori/blob/main/docs/MORI-EP-GUIDE.md
[S8]: https://github.com/ROCm/mori/blob/main/src/umbp/doc/design-master-control-plane.md
[S9]: https://github.com/ROCm/rocm-aic
[S10]: https://www.amd.com/en/developer/resources/technical-articles/2026/atomesh-unlocking-amd-hardware-for-scalable-llm-serving.html
[S11]: https://github.com/ROCm/ATOM/tree/main/atom/mesh
[S12]: https://github.com/ROCm/aiter
[S13]: https://github.com/ROCm/rocm-libraries/tree/develop/projects/composablekernel
[S14]: https://rocm.docs.amd.com/projects/rccl/en/latest/
[S15]: https://github.com/sgl-project/sglang/issues/35003
[S16]: https://docs.sglang.io/docs/advanced_features/hicache_best_practices
[S17]: https://docs.sglang.io/docs/advanced_features/pd_disaggregation
[S18]: https://docs.vllm.ai/en/latest/features/disagg_prefill/
[S19]: https://docs.vllm.ai/en/latest/design/nixl_kv_push_connector/
[S20]: https://careers.amd.com/careers-home/jobs/89398?lang=en-us

[S21]: https://careers.amd.com/careers-home/jobs/87545?lang=en-us
[S22]: https://careers.amd.com/careers-home/jobs/89395?lang=en-us
[S23]: https://careers.amd.com/careers-home/jobs/89498?lang=en-us
[S24]: https://careers.amd.com/careers-home/jobs/89499?lang=en-us
[S25]: https://careers.amd.com/careers-home/jobs/89500?lang=en-us
[S26]: https://github.com/AMD-AGI/Infera/commits/main/
[S27]: https://github.com/ROCm/mori/commits/main/
[S28]: https://github.com/ROCm/rocm-aic/commits/main/
[S29]: https://github.com/AMD-AGI/Infera/blob/main/CONTRIBUTING.md
[S30]: https://github.com/AMD-AGI/Infera/issues/36
[S31]: https://github.com/AMD-AGI/Infera/issues/46
[S32]: https://github.com/AMD-AGI/Infera/issues/88
[S33]: https://github.com/AMD-AGI/Infera/pull/73
[S34]: https://github.com/ROCm/mori#contribution-guide
[S35]: https://github.com/ROCm/mori/issues/626
[S36]: https://github.com/ROCm/mori/pull/632
[S37]: https://github.com/ROCm/mori/issues/342
[S38]: https://github.com/ROCm/mori/issues/507
[S39]: https://github.com/ROCm/mori/issues/572
[S40]: https://github.com/ROCm/rocm-aic/blob/main/CONTRIBUTING.md
[S41]: https://github.com/ROCm/rocm-aic/issues/118
[S42]: https://github.com/ROCm/rocm-aic/issues/115
[S43]: https://github.com/ROCm/rocm-aic/pull/151
[S44]: https://github.com/ROCm/rocm-aic/pull/150
[S45]: https://docs.sglang.io/docs/developer_guide/contribution_guide
[S46]: https://github.com/sgl-project/sglang/issues/33088
[S47]: https://github.com/vllm-project/vllm/issues/55344
[S48]: https://github.com/sgl-project/sglang/pull/36966
[S49]: https://github.com/vllm-project/vllm/issues/53136
[S50]: https://github.com/sgl-project/sglang/issues/27194
[S51]: https://docs.vllm.ai/en/latest/contributing/
[S52]: https://careers.amd.com/careers-home/jobs/92051?lang=en-us
[S53]: https://github.com/ROCm/mori/pull/653
[S54]: https://github.com/ROCm/mori/pull/625
[S55]: https://github.com/ROCm/mori/pull/540
[S56]: https://github.com/AMD-AGI/Infera/pull/138
[S57]: https://github.com/AMD-AGI/Infera/pull/162
[S58]: https://github.com/ROCm/rocm-aic/pull/154
[S59]: https://github.com/ROCm/rocm-aic/pull/158
[S60]: https://github.com/ROCm/ATOM/pull/2121
[S61]: https://github.com/vllm-project/vllm/pull/56610
[S62]: https://rocm.blogs.amd.com/software-tools-optimization/nvfp4-to-mxfp4/README.html
[S63]: https://github.com/sgl-project/sglang/pull/38164
[S64]: https://github.com/ROCm/mori/pull/665
