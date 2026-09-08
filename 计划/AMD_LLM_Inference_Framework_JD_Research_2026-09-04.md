# AMD 大模型推理框架工程师：JD 深度研究与面试准备手册

> 研究日期：2026-09-04<br>
> 文档用途：岗位判断、投递定位、技术复习、面试准备、与招聘方沟通<br>
> 研究对象：用户提供的“AMD 大模型推理框架工程师”非正式内推截图<br>
> 个人化依据：已知的 PyTorch 分布式、ProcessGroupDLCCL、集合通信、vLLM custom allreduce、CUDA IPC、CUDA 算子及性能调试经历

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

按照第 9 节的四周路线执行，并把每周产出补充回本文档。

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

Infera 当前公开版本仍是 v0.1。官方 roadmap 仍包含真正的 SLO-aware scheduling、load-driven autoscaling、运行时 P/D 角色切换、cluster-wide KV pool、distributed prefill cache 和 wide EP 等工作。[S4]

这与 JD 的关系非常关键：**岗位很可能不是维护一个已经完全成熟的系统，而是在建设下一阶段能力。**

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
| Rust router | 已公开代码 | Rust 要求有直接来源 |
| SLA planner | 可做容量建议，但不等于自动 resize | SLO 自适应扩缩仍有大量工作 |
| Cluster-wide KV | 多条方案正在演进 | 全局索引、tiering、容错是核心增量 |
| MORI-IO | 已进入 vLLM / SGLang 集成 | 仍需兼容更多拓扑并强化错误路径 |
| MORI-EP | 已有 dispatch/combine | EP v2、wide EP、EPLB 仍在演进 |
| MORI-UMBP | 新且活跃 | 最接近 JD 的新增工作 |
| AIC | early-access preview | 有探索价值，不能按成熟产品表述 |
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

AMD Careers 曾公开高度相邻的上海岗位 Req 89398，内容涉及：

- high-performance GPU communication；
- P/D disaggregation；
- Large-EP；
- vLLM / SGLang；
- 多 GPU / 多节点；
- C++ / Python；
- HIP / ROCm / LLVM。[S20]

它能证明上海存在高度相邻的技术招聘，但不能证明：

- 它就是截图中的岗位；
- 截图岗位位于上海；
- 截图岗位具有相同职级和年限要求。

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

以下来源以 AMD 官方、ROCm 官方仓库、项目上游仓库和正式文档为主。研究日期为 2026-09-04；roadmap 可能继续变化。

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

### 上游合入记录

- [vLLM MORI-IO](https://github.com/vllm-project/vllm/pull/29304)
- [vLLM MORI-EP](https://github.com/vllm-project/vllm/pull/28664)
- [SGLang MORI-IO](https://github.com/sgl-project/sglang/pull/14626)
- [SGLang MORI-EP](https://github.com/sgl-project/sglang/pull/17012)
- [SGLang UMBP / HiCache](https://github.com/sgl-project/sglang/pull/25377)

---

## 18. 后续维护建议

每次岗位或项目发生变化时，在文档开头更新研究日期，并重点检查：

- [ ] 是否出现 exact Req ID；
- [ ] Infera roadmap 是否关闭或新增关键 issue；
- [ ] MORI H2 roadmap 的完成状态；
- [ ] UMBP 在 vLLM / SGLang 的 upstream 状态；
- [ ] AIC 是否从 preview 进入更稳定阶段；
- [ ] MI45x / Helios 支持状态；
- [ ] 是否出现新的 Rust / C++ 职责拆分；
- [ ] 个人是否新增 ROCm、Rust、SGLang 或公开 PR 证据；
- [ ] 面试反馈是否揭示真实团队边界。

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
