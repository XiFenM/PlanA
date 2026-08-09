# 深入学习理解 vLLM 第 1 节：从仓库地图到进程与组件边界

> 学习阶段：vLLM 源码系统学习 Pass A–B
> 固定版本：vLLM `v0.26.0 @ 568afb3a13806beb53bb2e6bd518269357b237c0`
> 本文是基于固定版本源码形成的个人理解，可能存在遗漏。版本敏感的实现结论均限定在该 commit。

## 资料来源

本阶段没有从某一个函数开始追调用链，而是先使用官方设计文档和固定版本源码建立整体地图：

- [V1 架构总览](../references/vllm/docs/design/arch_overview.md)
- [V1 使用与设计说明](../references/vllm/docs/usage/v1_guide.md)
- [Model Runner V2 设计文档](../references/vllm/docs/design/model_runner_v2.md)
- [V1 引擎源码](../references/vllm/vllm/v1)
- [模型执行相关源码](../references/vllm/vllm/model_executor)
- [EP/PD 自研芯片适配设计与验证包](../EP-PD自研芯片适配设计与验证包.md)

需要特别注意：`arch_overview.md` 的部分内容仍混有旧式 `LLMEngine/AsyncLLMEngine` 表述。本文讨论在线 V1 主路径时，以 `AsyncLLM + EngineCore` 的固定源码为准。

## 先猜再学

### 当前状态背景

我有一些 vLLM 适配经验，但主要了解适配过程中实际修改过的部分。这种经验能让我识别 Worker、ModelRunner、KV Cache 或 device kernel 等局部概念，却不足以解释它们为什么位于当前目录、属于哪个进程，以及不同组件之间如何协作。

最初直接讨论自研芯片适配时，我给出的直觉链路是：

```text
OpenAI-compatible 请求入口
→ HTTP 服务接收
→ KV Cache 等资源调度
→ 模型运行调度
→ 模型代码执行
→ device kernel
```

我进一步猜测：

- HTTP 服务层保持不变；
- 资源调度需要 adapter；
- ModelRunner 位于核心路径，因此可能需要 `core patch`；
- device kernel 需要替换；
- 模型代码是否修改取决于具体实现。

这套猜测混合了三种不同问题：

1. 源码放在哪个目录；
2. 运行时经过哪些组件和进程；
3. 芯片适配时哪些接口需要修改。

如果缺少前两层地图，直接给第三层结论只能变成一张需要背诵的适配清单。因此本阶段先封存最终适配判断，按下面的顺序重新学习：

```text
仓库地图
→ 进程与组件
→ 请求生命周期
→ 单步模型执行
→ 扩展机制
→ 最后回看原始猜想
```

本文只收口前两步。

### 期望回答的问题

- vLLM 仓库有哪些主要部分，分别承担什么职责？
- `vllm/v1/` 中的 `engine`、`core`、`executor`、`worker` 如何分工？
- 逻辑组件、OS 进程和 TP/PP/DP 并行策略之间是什么关系？
- 为什么单纯增加进程不等于启用模型并行？
- 一个 API Server 能否连接多个 EngineCore？
- Worker 与 ModelRunner 为什么还需要拆成两层？
- 请求执行到一半后，为什么不能因为另一个 EngineCore 空闲就直接迁移？

## 学习过程

### 1. 源码目录结构不等于运行时调用层次

vLLM 顶层仓库可以先压缩成四类：

| 区域 | 主要作用 | 第一遍阅读策略 |
|---|---|---|
| `vllm/` | Python 产品代码与主要运行时 | 主读 |
| `csrc/`、`cmake/`、Rust 目录 | 原生算子、绑定与构建 | 沿调用链下钻时再读 |
| `tests/`、`benchmarks/` | 正确性、契约与性能验证 | 每学完一层选择对应测试 |
| `docs/`、`examples/` | 设计说明与使用入口 | 用于建立地图，不代替源码 |

这个分类解决了第一个误区：看到大量 CUDA/C++ 文件，不代表应该从 `csrc/` 开始阅读。更可靠的顺序是：

```text
Python 调用位置
→ Backend / CustomOp
→ Python kernel wrapper
→ csrc 或其他 device kernel
```

否则只能看到很多孤立 kernel，无法判断谁在什么条件下调用它们。

#### `vllm/` 包的三圈地图

`vllm/` 下的目录很多，但第一遍不需要逐个记忆，可以先分成三圈：

```text
vllm/
├─ 运行主干
│  ├─ entrypoints/
│  ├─ v1/
│  └─ model_executor/
│
├─ 横切能力
│  ├─ config/
│  ├─ platforms/ + plugins/
│  ├─ distributed/
│  └─ compilation/ + kernels/ + ir/
│
└─ 功能支线
   ├─ inputs/ + renderers/ + tokenizers/
   ├─ multimodal/ + lora/
   ├─ parser/ + reasoning/ + tool_parsers/
   └─ logging_utils/ + tracing/ + profiler/
```

运行主干可以先记成三句话：

```text
entrypoints：谁来请求
v1：这一轮该做什么
model_executor：具体计算什么
```

横切能力不是一条从前到后的调用链，而是被主干各处使用：

- `config/` 管理模型、缓存、并行、调度、量化和编译配置；
- `platforms/` 与 `plugins/` 识别设备并加载外部平台；
- `distributed/` 提供 TP、PP、DP 及通信能力；
- `compilation/`、`kernels/`、`ir/` 承担编译与性能实现。

输入、多模态、LoRA、工具解析和可观测性等目录属于功能支线。它们很重要，但不是第一遍理解主架构的前置条件。

#### 两组容易混淆的名字

第一组：

```text
vllm/engine/
vllm/v1/engine/
```

前者更多承载参数、公共协议和兼容表面；当前 V1 引擎主体位于后者。看到 `engine` 目录时，不能只凭名字判断它就是当前核心实现。

第二组：

```text
vllm/v1/executor/
vllm/model_executor/
```

- `vllm/v1/executor/` 决定工作发到哪里执行，例如 `uni`、`mp` 或 Ray；
- `vllm/model_executor/` 定义具体执行什么，包括模型、层、权重加载、量化和算子。

一个偏执行拓扑，一个偏模型计算内容。

源码定位题验证了这张地图：

| 要找的内容 | 第一站 |
|---|---|
| `vllm serve` 入口 | `entrypoints/` |
| 下一轮调度哪些 token | `v1/core/` |
| 模型或并行 Linear | `model_executor/` |
| CUDA/ROCm 等平台识别 | `platforms/` |
| TP collective | `distributed/` |
| 高性能 kernel | `kernels/` 或 `csrc/` |

这一步的价值不是背目录名，而是遇到问题时能先把搜索范围缩到正确区域。

### 2. `vllm/v1/` 的四个主要所有者

继续展开 `vllm/v1/`，可以得到四个主要职责区域：

| 目录 | 主要职责 |
|---|---|
| `engine/` | 异步请求生命周期、Engine Core client、IPC 与引擎总协调 |
| `core/` | 请求队列、调度策略和逻辑资源状态 |
| `executor/` | 执行拓扑、RPC 和任务下发 |
| `worker/` | 具体设备、rank、模型权重、物理缓存与模型执行 |

#### `engine/`：让引擎持续运转

这里包含 `async_llm.py`、`core_client.py`、`core.py`、输入输出处理器等内容，主要回答：

> 引擎如何启动、接收请求、连接内部组件，并持续执行一轮轮工作？

其中还有一个命名陷阱：

```text
vllm/v1/engine/core.py
vllm/v1/core/
```

前者定义 `EngineCore` 这一总协调组件；后者存放 Scheduler、KV Cache Manager 等调度算法和逻辑状态。可以暂时理解为：

```text
EngineCore：总控室
v1/core：总控室里的调度与逻辑资源管理部门
```

#### `core/`：决定这一轮算什么

`core/` 维护 waiting/running 请求、token budget 和逻辑 KV blocks，主要回答：

> 当前有哪些请求？这一轮谁可以运行多少 token？逻辑 KV blocks 如何分配、复用和释放？

这里的 KV 管理首先是逻辑账本，不等于直接写 GPU 上的 KV tensor。

#### `executor/`：决定发到哪里执行

Executor 在 `uniproc`、`multiproc`、Ray 等执行方式之间提供统一接口，主要回答：

> Scheduler 已经给出本轮计划，应该通过什么拓扑把它交给一个或多个 Worker？

Executor 不重新决定本轮运行哪些请求；那仍然是 Scheduler 的职责。

#### `worker/`：在具体设备上执行

Worker 管理设备、rank、显存和模型执行入口，主要回答：

> 在这个 rank、这张设备上，本轮计划如何真正变成模型计算？

这四层拆开后，不同变化可以尽量局部化：

- 请求协议或 IPC 改变，主要影响 `engine/`；
- 调度算法改变，主要影响 `core/`；
- 执行拓扑改变，主要影响 `executor/`；
- 设备、显存和模型执行改变，主要影响 `worker/`。

### 3. 组件、进程和并行策略是三个维度

一开始我把“切换多进程”和“开启模型并行”放在了一起，认为多进程会自然让 Worker 增加通信算子。这个说法缺少条件。

需要分开的三个维度是：

| 维度 | 回答的问题 | 示例 |
|---|---|---|
| 逻辑组件 | 谁负责什么？ | EngineCore、Scheduler、Executor、Worker |
| 进程布局 | 组件在哪里运行、如何通信？ | `uni`、`mp`、Ray |
| 并行策略 | 请求或模型怎样拆分？ | DP、TP、PP |

关键结论是：

> 多进程解决“组件放在哪里、怎样调用”；TP/PP 解决“模型计算怎样跨设备拆分”。

#### 常规单卡在线路径

即使 `TP=PP=DP=1`，常规在线 V1 路径也不是整个服务只有一个进程：

```text
进程 A
└─ API Server + AsyncLLM
          │ ZMQ
          ▼
进程 B
├─ EngineCore
├─ Scheduler
├─ UniProcExecutor
├─ Worker
└─ ModelRunner
          │
          ▼
        GPU 0
```

这里的 `uni` 只表示 Worker 与 EngineCore 位于同一个进程，不表示 API Server 和 EngineCore 也在同一个进程。

这种隔离对应两种不同节奏：

- HTTP、tokenization、连接和流式输出具有较大抖动；
- EngineCore 需要稳定执行 `schedule → execute → update` 热循环。

#### 单卡显式使用 `mp`

当 `TP=PP=1` 时，也可以显式选择 `mp`：

```text
进程 A：API Server + AsyncLLM
             │
进程 B：EngineCore + Scheduler + MultiprocExecutor
             │ IPC
进程 C：Worker + ModelRunner + 完整模型
             │
           GPU 0
```

此时：

- 模型不分片；
- 不需要跨 rank collective；
- Executor 与 Worker 之间增加 IPC；
- CUDA context、模型加载和设备资源生命周期移动到 Worker 子进程。

因此，日志中只出现一个 `VllmWorker-0`，不能据此断定启用了 TP。它也可能只是单卡显式使用 `mp`。

#### `mp + TP>1`

当 TP 从 1 增大时，进程拓扑和模型语义才同时发生变化：

- Executor 创建多个 Worker/rank；
- 每个 Worker 加载自己的权重 shard；
- 模型层引入 AllReduce、AllGather 等 collective；
- 每个 ModelRunner 消费相应 rank 的设备和并行上下文。

默认配置中，多 rank 经常会自动选择 `mp`，所以二者看起来总是一起出现；但这是默认策略，不是架构上的同义关系。

#### 多 API 进程

`api_server_count` 是另一个正交维度。多个 API 进程可以共同服务同一个 EngineCore 和模型实例，用于扩展 HTTP、tokenization 和输入输出处理能力，不改变模型 world size，也不产生权重分片。

### 4. 一个前端连接多个 EngineCore

我随后提出了一个很自然的问题：能否由一个 API 前端连接多个后台 EngineCore，再按照负载为新请求分流？

原生 vLLM 已通过 Data Parallel 内部负载均衡提供这一结构。准确说法不是“把一个 EngineCore 变成多进程”，而是：

> 启动多个相互独立的 EngineCore，每个持有自己的 Scheduler、请求队列、逻辑 KV 状态和模型副本，再由前端 client 为新请求选择目标。

```text
API Server + AsyncLLM
└─ DPLBAsyncMPClient
   ├─ EngineCore 0
   │  ├─ Scheduler 0
   │  └─ Worker 组 0 / 模型副本 0
   └─ EngineCore 1
      ├─ Scheduler 1
      └─ Worker 组 1 / 模型副本 1

独立 DPCoordinator
└─ 汇总各 EngineCore 的 DP 状态并反馈给前端
```

分流位于 API 进程中的 `DPLBAsyncMPClient`，而不是 OpenAI HTTP route。这样 HTTP 协议层不必知道后面有多少 EngineCore。

固定版本中的选择公式为：

$$
score = 4 \times waiting + running
$$

新请求选择得分最低的 EngineCore。前端在等待下一次统计快照期间，还会乐观增加目标 EngineCore 的本地 waiting 计数，并轮转同分时的扫描起点，以减少突发请求集中到同一个实例。

这个启发式只看加权请求数量，不直接考虑：

- prompt token 数；
- 预计生成长度；
- GPU utilization；
- 剩余 KV blocks；
- prefix cache 是否命中。

因此它是轻量的近似负载均衡，而不是精确的工作量或 cache-locality 路由。

#### 为什么执行中的请求不能直接迁移

新请求会在进入 EngineCore 前完成分流。一旦开始执行，其状态分散在多个所有者中：

| 所有者 | 与请求迁移相关的状态 |
|---|---|
| EngineCore / Scheduler | waiting/running 归属、token 进度、调度状态、逻辑 KV block IDs |
| Worker / ModelRunner | 物理 KV tensor、block table、持久 batch 和采样状态 |
| AsyncLLM / CoreClient | 输出 collector、`request_id → EngineCore` 路由与 abort 目标 |

因此，另一个 EngineCore 后来变空闲，也不能只转发 request id 就接手执行。

如果在新 EngineCore 上重新执行 prefill，可以重新构建 KV，但这属于重算或重启，不是无损的执行中迁移。真正的 live migration 至少需要迁移或重建调度状态、token 进度、逻辑到物理 block 映射、KV 内容、采样状态和输出路由。

#### 固定版本中的文档与源码落差

这一节还发现了一个值得继续验证的现象：

- 官方文档把 internal DP 描述为依据各 EngineCore 的 running/waiting 队列进行负载均衡；
- `v0.26.0` 中，实时 `_maybe_publish_request_counts()` 路径只出现在 MoE 使用的 `DPEngineCoreProc`；
- dense DP 使用普通 `EngineCoreProc`，固定源码中尚未找到等价的实时计数发布链。

因此，目前只能得出限定结论：

- MoE internal DP 存在完整的实时队列反馈链；
- dense internal DP 仍会执行前端选择逻辑，但不能直接声称拥有相同的实时后端压力反馈；
- dense 路径更可能依赖前端的 optimistic waiting 和轮转，但其真实行为仍需复现。

这只是一个上游实践候选，尚未证明是 bug。后续需要对比最新 `main`、检索已有 issue/PR、确认 maintainer 的设计意图，并构造最小复现后，才能判断应修改代码、测试还是文档。

源码锚点：

- `vllm/v1/engine/core_client.py:1380–1447`
- `vllm/v1/engine/coordinator.py:23–56`
- `vllm/v1/engine/core.py:1287–1299`
- `vllm/v1/engine/core.py:1844–1860`

### 5. DP 场景中的组件所有权与进程布局

理解多 EngineCore 后，组件状态可以进一步明确：

| 组件 | 主要职责 | 不负责 |
|---|---|---|
| API Server / `AsyncLLM` | 输入输出语义、输出处理、流式 collector、Core client | token 级调度、模型 forward |
| `DPLBAsyncMPClient` | 为新请求选择 EngineCore，保存负载快照和请求路由 | Scheduler 队列、KV 内容 |
| `DPCoordinator` | 汇总 DP rank 状态和协调信息 | 选择具体请求、持有请求 KV |
| EngineCore / Scheduler | 请求生命周期、token 进度、waiting/running、逻辑 KV blocks | 模型权重、物理 KV tensor |
| Executor | 隔离执行拓扑与 RPC | 决定本轮调度哪些请求 |
| Worker / ModelRunner | 设备、模型权重、物理 KV、模型执行与采样 | OpenAI 协议、HTTP 连接 |

我最初正确判断了 `DPCoordinator` 的统计汇总职责，却把它错误地放进了某个 EngineCore 进程。

以以下配置为例：

```text
API server count = 1
DP = 2
TP = 1
backend = uni
```

忽略 supervisor 和监控辅助进程后，主要进程为：

```text
进程 1：API Server + AsyncLLM + DPLBAsyncMPClient
进程 2：DPCoordinator
进程 3：EngineCore 0 + Scheduler 0 + UniProcExecutor 0
        + Worker 0 + ModelRunner 0
进程 4：EngineCore 1 + Scheduler 1 + UniProcExecutor 1
        + Worker 1 + ModelRunner 1
```

总数是 4，而不是我最初判断的 3。

`DPCoordinator` 是所有 DP ranks 的对等汇总点，因此由独立进程承载，而不是归属于其中某一个 EngineCore。

如果只把 backend 改为 `mp`：

- 两个 EngineCore 进程仍然存在；
- Scheduler 和 MultiprocExecutor 留在对应 EngineCore 进程；
- 每个 EngineCore 新增一个 Worker 子进程；
- ModelRunner、模型权重和物理 KV tensor 随 Worker 移动。

因此主要进程数从 4 增加到 6。

### 6. Worker 与 ModelRunner 不是“外层调用和一次 forward”

我最初把 ModelRunner 简化成了“处理模型 forward 的对象”。继续查看源码后，这个描述明显不够。

固定 `v0.26.0` 中，`gpu_worker.py` 内的实际类名是 `Worker`，不是 `GPUWorker`。

二者更准确的边界是：

> Worker 管“在哪个设备/rank、以什么生命周期运行”；ModelRunner 管“这一轮在该设备上具体怎样运行”。

| 阶段 | Worker | ModelRunner |
|---|---|---|
| 设备初始化 | 选择 device，初始化 rank、distributed/NCCL、seed 和显存环境 | 在设备环境就绪后建立执行状态 |
| 模型加载 | 提供生命周期入口和 allocator、memory pool 等外围上下文 | 实际创建、加载并持有模型及相关组件 |
| KV Cache | 探测显存预算、协调 cache 初始化时机和生命周期 | 分配并持有物理 KV tensor，维护 block table 与 slot mapping |
| 每个 engine step | 接收 Executor 调用，处理设备和 PP 通信外壳 | 将 `SchedulerOutput` 转换成 batch、tensor 和 attention metadata |
| 模型执行 | 提供外层调用、同步检查和资源控制 | 选择 eager/compile/CUDA Graph，执行模型并处理采样 |
| 运维 | health、sleep/wake、profile、权重更新和资源清理入口 | 实现与模型、图、KV 和执行状态直接相关的具体操作 |

ModelRunner 不只是调用一次 `model.forward()`，还可能负责：

- 维护请求和持久 `InputBatch`；
- 更新 block table 与 slot mapping；
- 准备 positions、attention metadata、LoRA 和多模态输入；
- 选择 eager、compile 或 CUDA Graph；
- 计算 logits；
- sampling、speculative decoding 和 structured output；
- 更新设备侧请求和采样状态。

#### KV Cache 为什么是两层协作

KV Cache 不能简单归给 Worker 或 ModelRunner 中的某一方：

- Worker 决定有多少显存可供 KV 使用、何时初始化和销毁，并提供设备与资源生命周期；
- ModelRunner 决定具体 tensor 布局，分配并持有物理 KV tensor，建立 block table/slot mapping，并在 attention 中使用它们。

#### 通信也不是全部归 Worker

- Worker 初始化 distributed process groups，并在外层显式处理 Pipeline Parallel intermediate tensor 的收发；
- Tensor Parallel 的 AllReduce、AllGather 等 collective 通常发生在模型层和 distributed primitives 中；
- ModelRunner 也会读取和消费 DP、PP、TP 等 rank 状态。

所以这里不是“Worker 完全不计算、ModelRunner 完全不理解分布式”，而是所有权和热路径职责不同。

#### MRV1 切换到 MRV2 不改变进程拓扑

MRV1/MRV2 是 Worker 内部执行实现的选择。切换到 MRV2 后：

- Worker 仍处于原来的进程；
- ModelRunner 仍是 Worker 内对象；
- API、EngineCore、Executor 和 Worker 的进程拓扑不需要改变；
- 变化集中在持久 batch、输入准备、图执行和采样等设备内执行算法。

源码锚点：

- `vllm/v1/worker/gpu_worker.py:297–416`
- `vllm/v1/worker/gpu_worker.py:1087–1175`
- `vllm/v1/worker/gpu/model_runner.py:1151–1391`
- `vllm/v1/worker/gpu/model_runner.py:1395–1535`

## 读后回顾

### 当前已经能够回答的问题

现在面对 vLLM 源码问题，我可以先判断它属于哪一层：

- 用户入口和协议：`entrypoints/`
- 请求生命周期与 IPC：`v1/engine/`
- 调度和逻辑 KV：`v1/core/`
- 执行拓扑：`v1/executor/`
- 设备和运行入口：`v1/worker/`
- 模型、层与算子：`model_executor/`
- 设备识别和插件：`platforms/`、`plugins/`
- 通信：`distributed/`
- kernel：`kernels/` 或 `csrc/`

我也可以把以下概念分开：

```text
逻辑组件 ≠ OS 进程 ≠ 并行策略
uni/mp ≠ TP/PP
Worker process 数量 ≠ 模型分片数量
多个 EngineCore ≠ 一个 EngineCore 内多 Worker
```

### 与最初直觉相比

几个最重要的变化是：

1. 多进程不必然意味着模型分片或 collective。
2. `uni` 只描述 EngineCore 与 Worker 的放置关系，不代表整个在线服务是单进程。
3. 一个 API 前端可以通过内部 DP client 连接多个独立 EngineCore。
4. `DPCoordinator` 是独立进程，而不是某个 EngineCore 的内部对象。
5. ModelRunner 远不止一次模型 forward，它拥有设备内推理热路径的大部分状态和算法。
6. 请求迁移困难不是单纯“缺 KV Cache”，而是多个组件共同持有请求状态。

不过，最初的五层适配图和 `adapter/core patch/替换` 分类仍然没有正式收口。这是有意保留的：只有完成请求生命周期、单步模型执行和扩展机制后，才有足够依据重新判断。

## 实践

### 固定可复查源码

本阶段已将以下源码作为 shallow Git submodule 固定：

| 项目 | 版本 |
|---|---|
| vLLM | `v0.26.0 @ 568afb3a` |
| SGLang | `v0.5.17 @ 29481685` |
| PyTorch | `v2.11.0 @ 70d99e99` |

PyTorch 版本服从 vLLM `v0.26.0` 的依赖基线，不与独立更新的 PyTorch 稳定版混用。

### 当前证据边界

本阶段主要完成固定源码审查，还没有完成：

- 多卡 TP/DP 实际运行；
- dense DP 计数链最小复现；
- vLLM 与 PyTorch 固定组合的环境安装验证；
- attention backend 和 device kernel 的真实调用链验证。

因此进程图和组件结论属于固定源码证据，不应表述为当前单卡环境中的多卡实测结果。

### 上游实践候选

dense internal DP 的实时队列统计落差已登记为候选 U1。后续最小路径为：

1. 对比最新 `main`；
2. 检索已有 issue、PR 和讨论；
3. 确认 maintainer 预期；
4. 构造 dense `DP=2` 最小复现或失败测试；
5. 再决定修改代码、测试、文档或放弃该判断。

在完成这些步骤前，不把它写成已确认 bug。

## 下游透镜

### 过往经验

过去做 vLLM 适配时，我主要熟悉修改过的局部区域。这种经验适合解决“这个函数如何改”，却容易把局部执行路径误认为完整架构。

建立仓库地图后，既有经验可以重新定位：

- 修改设备初始化，应先判断是 Worker 生命周期还是 Platform 能力；
- 修改模型输入准备，应先判断是否属于 ModelRunner；
- 修改通信，需要区分 Executor IPC、PP 外层通信和模型层 TP collective；
- 修改 KV，需要区分 Scheduler 的逻辑 block 与 ModelRunner 持有的物理 KV tensor；
- 修改多副本服务，需要区分 API 进程数、DP EngineCore 数、Executor backend 和 TP world size。

### 面试问题 Q&A

#### 1. vLLM 中 `executor/` 与 `model_executor/` 有什么区别？

`vllm/v1/executor/` 负责执行拓扑和任务下发，例如 `uni`、`mp` 或 Ray；`vllm/model_executor/` 负责模型、层、权重、量化和算子，即具体执行什么。前者隔离放置与 RPC，后者承载模型计算内容。

#### 2. `vllm/v1/engine/core.py` 与 `vllm/v1/core/` 有什么区别？

`engine/core.py` 中的 EngineCore 是总协调组件，组织每轮 schedule、execute 和 update。`v1/core/` 存放 Scheduler、KV Cache Manager 等调度算法和逻辑资源状态。

#### 3. 为什么 `uni → mp` 不等于 `TP=1 → TP>1`？

`uni/mp` 决定 Worker 与 EngineCore 是直接调用还是跨进程调用；TP 决定模型权重和计算是否跨多个 rank 分片。单卡显式使用 `mp` 会增加 IPC，但不需要模型分片或跨 rank collective。

#### 4. 看到一个 `VllmWorker-0`，能否判断已经启用 TP？

不能。`TP=1` 时显式选择 `mp` 也会创建一个 Worker 子进程。需要同时查看 `tensor_parallel_size`、world size 和模型分片配置。

#### 5. 常规单卡在线服务为什么仍然是多进程？

API Server/AsyncLLM 与 EngineCore 通常通过独立进程和 IPC 隔离。这样 HTTP、tokenization 和流式连接的抖动不会干扰 EngineCore 稳定的迭代热循环。

#### 6. 一个 API Server 如何连接多个 EngineCore？

内部 DP 模式会启动多个独立 EngineCore，每个拥有自己的 Scheduler、KV 状态和模型副本。API 进程中的 `DPLBAsyncMPClient` 在请求进入 EngineCore 前选择目标实例。

#### 7. vLLM `v0.26.0` 的内部 DP 路由公式是什么？

前端计算 `$score = 4 \times waiting + running$`，选择分数最低的 EngineCore。它是加权请求计数，不直接考虑 token 工作量、GPU 利用率、剩余 KV blocks 或 prefix-cache locality。

#### 8. 为什么执行中的请求不能直接迁移到空闲 EngineCore？

原 EngineCore/Scheduler 持有 token 进度和逻辑 KV 映射，Worker/ModelRunner 持有物理 KV 和持久执行状态，前端还保存输出与 abort 路由。除非迁移或重建这些状态，否则新 EngineCore 无法继续等价的下一步执行。

#### 9. `DPCoordinator` 位于哪个进程？

在讨论的 internal DP 场景中，它是独立进程，而不是 API 进程或任一 EngineCore 进程。它作为多个 DP ranks 的对等协调和汇总点，不能归属于其中某个 rank。

#### 10. Worker 与 ModelRunner 如何分工？

Worker 拥有设备、rank、distributed 环境和资源生命周期，并向 Executor 暴露进程级接口。ModelRunner 拥有设备内推理热路径，包括 batch/tensor、物理 KV、attention metadata、图执行、模型调用和采样状态。

#### 11. 物理 KV Cache 属于 Worker 还是 ModelRunner？

两者协作。Worker 负责显存预算、初始化时机和生命周期编排；ModelRunner 实际分配并持有 KV tensor，维护 block table/slot mapping，并在模型执行中使用。

#### 12. 从 MRV1 切换到 MRV2 是否需要改变进程拓扑？

不需要。MRV1/MRV2 是同一 Worker 外壳内的执行实现选择，主要改变设备内 batch、输入准备、图执行和采样算法，而不是 API、EngineCore、Executor、Worker 的进程关系。

#### 13. dense internal DP 的实时负载反馈是否已经确认有 bug？

没有。固定 `v0.26.0` 中观察到文档描述与源码发布链可能存在落差，但尚未完成最新主线核对、多卡复现和上游讨论检索。当前只能登记为待验证的贡献候选。

## 思维导图总结

```text
vLLM v0.26.0
├─ 仓库地图
│  ├─ vllm/：Python 运行时
│  ├─ csrc/cmake：原生实现与构建
│  ├─ tests/benchmarks：验证与评测
│  └─ docs/examples：说明与入口
│
├─ vllm/ 三圈
│  ├─ 运行主干：entrypoints / v1 / model_executor
│  ├─ 横切能力：config / platforms / distributed / compilation
│  └─ 功能支线：输入 / 多模态 / LoRA / parser / tracing
│
├─ v1 四层所有权
│  ├─ engine：生命周期、client、IPC、总协调
│  ├─ core：Scheduler、队列、逻辑 KV
│  ├─ executor：uni/mp/Ray、RPC、任务下发
│  └─ worker：设备、rank、物理资源与执行
│
├─ 三个独立维度
│  ├─ 逻辑组件
│  ├─ 进程布局：uni / mp / Ray
│  └─ 并行策略：DP / TP / PP
│
├─ 多 EngineCore
│  ├─ DPLBAsyncMPClient：选择目标
│  ├─ DPCoordinator：独立汇总进程
│  ├─ 每个 EngineCore：独立 Scheduler/KV/模型副本
│  └─ 请求执行中不直接迁移
│
└─ Worker / ModelRunner
   ├─ Worker：设备、rank、生命周期、PP 外壳
   ├─ ModelRunner：batch、tensor、KV、graph、forward、sampling
   └─ MRV1/MRV2：不改变进程拓扑
```

## 后续预告

### 依旧需要解决的问题

- 一个普通 `/v1/chat/completions` 请求如何变成 `EngineCoreRequest`？
- 请求和输出分别在哪些位置跨越进程边界？
- `SchedulerOutput` 如何变成 ModelRunner 的 batch、block table 和 attention metadata？
- 模型 forward 与 Attention backend、CustomOp、device kernel 之间如何连接？
- Platform、Worker、ModelRunner、Attention backend 和 communicator 分别提供哪些扩展面？
- 最初的“保持不变 / adapter / core patch / 替换”判断应如何正式修正？

### 下一阶段

Pass C 将只追一条普通 Chat Completions 请求，不展开多模态、LoRA、tool calling 或 speculative decoding 分支：

```text
OpenAI 请求
→ 前端协议处理
→ EngineCoreRequest
→ EngineCore / Scheduler
→ SchedulerOutput
→ 输出返回
```

在 Pass C、D、E 全部完成后，再回到最初的五层猜想，逐项说明哪些判断成立、哪些混淆了逻辑层次，以及真正的自研芯片适配边界在哪里。
