# EP/PD 自研芯片适配设计与验证包

> 启动日期：2026-08-09
> 所属临时 Program：[高级 AI 框架开发工程师八周证据冲刺](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#program-plana-jd-ai-framework-4w)
> 逻辑职责：下方 `Lesson 状态` 是当前 W1 Lesson 的唯一 ledger；其余章节是设计工件与历史 evidence，不拥有精确游标。
> 唯一恢复游标：[学习断点](../计划/学习断点.md)
> 证据边界：个人隐私敏感信息（如手机号）不公开，邮箱可公开；不记录公司代码、内部 API、未公开硬件参数、性能数据或原始日志。

<a id="lesson-plana-jd-w1-vllm-execution-boundaries"></a>
## Lesson 状态（guide-learning）

- **Lesson ID**：`plana-jd-w1-vllm-execution-boundaries`
- **能力标题**：vLLM 执行链与扩展边界。
- **Program 引用**：[临时 Program `plana-jd-ai-framework-4w`](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#program-plana-jd-ai-framework-4w)。
- **当前 stage**：`teaching`。Pass A–B 已形成学习者 evidence；Pass C-1 尚未产生学习者回答，不能据导师预核对外推掌握。
- **授权边界**：本节只迁移已经启动并位于前台的 W1 Lesson，不扩展到 W2–W4、optional 实现、正式练习或新的写入范围。

### 来源与版本锚点

| 来源 | 角色 | 版本锚点 | 本 Lesson 使用范围 |
|---|---|---|---|
| vLLM | teaching spine；实现事实权威 | `v0.26.0` / `568afb3a13806beb53bb2e6bd518269357b237c0` | 仓库地图、进程与组件、请求生命周期、执行和扩展边界 |
| 同 revision 的 vLLM 官方文档与测试 | 公开承诺与测试证据 | 同上 | 部署语义、已有 invariant、实现结论的交叉核验 |
| SGLang / MORI | 后续窄对照来源 | 见 [§0.2](#02-固定源码基线) | 只在 vLLM 主线建立后核对对应接入边界，不与 vLLM 等量展开 |

### 能力范围与 evidence 目标

| 目标 ID | 可观察目标 | 本 Lesson 的 evidence 目标 |
|---|---|---|
| `w1-o1-repository-process-map` | 独立解释仓库、进程边界和主要组件的状态所有权 | Pass A–B 的学习者回答、结果文章与源码锚点 |
| `w1-o2-request-lifecycle` | 把普通 chat 请求从 OpenAI 协议对象映射到 `EngineCoreRequest`，并说明不会跨越 IPC 的信息 | Pass C 的学习者映射、request sequence 与 8–12 文件 source map |
| `w1-o3-extension-boundaries` | 基于源码契约判断保持不变、adapter、core patch 与替换的边界 | 适配矩阵、Change Card 前置判断与可核验依据 |

旧记录没有逐目标保存用户确认的 `conceptual / practical / empirical` required 值；本次迁移不猜测、不补写。进入正式练习或 mastery gate 前必须另行确认这些维度。当前没有 `final_mastery`。

- **核心工件**：本文件 [§0–§6](#0-范围版本与披露边界)。
- **最近结构化 evidence**：[Pass A–B 阶段材料收口](#pass-ab--阶段材料收口已完成)。
- **Checkpoint 引用**：[唯一学习断点](../计划/学习断点.md)。

### Session event 索引

#### `plana-jd-w1-20260809-pass-ab`

- **日期**：2026-08-09
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：vLLM 仓库地图、进程边界、DP 路由与 Worker/ModelRunner 职责边界。
- **已完成动作**：完成 Pass A–B 的学习者问答验收并收束结果材料。
- **Evidence 引用**：[结果文章](深入学习理解vLLM/1-Repository-and-Process-Architecture.md)、[结构化过程记录](log/2026-08-09-vllm-repository-and-process-architecture.md)、[技术记忆卡](cards/vllm-repository-and-process-architecture.md)。
- **开放问题**：Pass C 的请求生命周期尚无学习者回答证据；精确恢复动作只见 Checkpoint。

---

> 以下章节保存设计工件、来源锚点和历史 evidence。章节内的历史推进记录不裁决当前 Lesson stage、唯一下一动作或 final mastery。

## 0. 范围、版本与披露边界

### 0.1 审查范围

- 主框架：vLLM，负责请求执行链、scheduler、KV Cache、model runner、attention backend 与 distributed executor 主线。
- 窄对照：SGLang，只核对 ATOM/MoE 注册、控制面差异和 ownership 边界。
- 参考数据面：MORI，只审查 SHMEM/IR、EP、IO、UMBP 的接口契约、buffer 生命周期与完成语义。
- PyTorch：服从 vLLM 的兼容基线，只追真实 op 的 schema → fake/meta → C++/设备注册 → DeviceGuard/stream → build/test 调用链。
- 非目标：不等量精读双框架，不自建完整 serving 系统，不预先启动 `mini-ep-pd-serving`。

### 0.2 固定源码基线

| 角色 | Tag | Commit | 用途 |
|---|---|---|---|
| vLLM 主读 | [`v0.26.0`](https://github.com/vllm-project/vllm/releases/tag/v0.26.0) | [`568afb3`](https://github.com/vllm-project/vllm/commit/568afb3a13806beb53bb2e6bd518269357b237c0) | W1–W3 的执行链、EP/PD 与测试事实源 |
| PyTorch 兼容基线 | [`v2.11.0`](https://github.com/pytorch/pytorch/releases/tag/v2.11.0) | [`70d99e9`](https://github.com/pytorch/pytorch/commit/70d99e9) | vLLM v0.26.0 明确固定的默认 CUDA/CPU 依赖；2.13 只作增量阅读，不混入运行基线 |
| SGLang 窄对照 | [`v0.5.17`](https://github.com/sgl-project/sglang/releases/tag/v0.5.17) | [`2948168`](https://github.com/sgl-project/sglang/commit/29481685462732237d80d86076d6563e1f658102) | ATOM/MoE、PD 与控制面边界对照 |
| MORI 参考数据面 | [`v1.2.2`](https://github.com/ROCm/mori/releases/tag/v1.2.2) | [`dafdcfc`](https://github.com/ROCm/mori/commit/dafdcfcf1e27b0c981b90903ab198b90d29e6867) | SHMEM/IR、EP、IO、UMBP 契约审查 |

> 这些版本只建立可复查的源码基线，不代表四个组件已经在同一环境完成组合验证。若后续使用本地部署版本，另建对照列，不覆盖本表。

#### 本地源码 submodules

| 组件 | 本地路径 | Gitlink commit | 状态 |
|---|---|---|---|
| vLLM | [`references/vllm`](references/vllm) | `568afb3a13806beb53bb2e6bd518269357b237c0` | 浅克隆、detached HEAD、固定 `v0.26.0` |
| SGLang | [`references/sglang`](references/sglang) | `29481685462732237d80d86076d6563e1f658102` | 浅克隆、detached HEAD、固定 `v0.5.17` |
| PyTorch | [`../PyTorch/references/pytorch`](../PyTorch/references/pytorch) | `70d99e998b4955e0049d13a98d77ae1b14db1f45` | 浅克隆、detached HEAD、固定 `v2.11.0`；submodule 内启用 `core.longpaths=true` |

三项由仓库根目录 [`.gitmodules`](../.gitmodules) 登记，并建议后续 clone 时保持 shallow。MORI 当前仍使用固定远程源码链接，不在本轮本地 clone 范围内。

### 0.3 计划预算与实际工时边界

- Program 的计划预算与节奏只见[八周证据冲刺计划 §5](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#5-时间预算与日常节奏)。
- 实际学习工时只按真实归属写入对应模块 `进度.md`；本 Lesson ledger、Session event 和 Checkpoint 不复制工时。
- 2026-08-09 的启动日期与返回 capsule 由临时 Program 保存；本文件不把计划可用时长冒充实际投入。

### 0.4 环境与能力 preflight

| 槽位 | 可用且获准 | 可公开粒度 | 当前处理 |
|---|---|---|---|
| 公开源码与官方文档 | 是 | 公开链接、commit、文件、类、函数 | 当前主分支 |
| 自研芯片环境 | 否（本轮） | 不适用 | 只做抽象能力槽位与公开源码设计，不推断内部能力 |
| AMD GPU / ROCm | 否（本轮） | 公开资料 | 仅审查公开实现，不声称 MORI/ROCm 实测 |
| CUDA GPU | 是，单卡 | 设备型号、driver、显存、算力等级、命令与脱敏结果 | 已完成宿主机只读指纹；框架运行仍待验证 |
| CPU 环境 | 是 | 工具链版本、命令与脱敏结果 | 可用于源码工具和轻量验证；不默认安装依赖 |
| 单机多卡 | 否 | 不适用 | 不声称多卡验证 |
| RDMA / 跨机环境 | 否 | 不适用 | 不声称通信实测 |

公开授权允许除个人隐私敏感信息外的内容进入工件，邮箱可公开；第三方或公司保密义务仍是更高优先级的硬边界。未明确的环境按不可用处理，后续如有变化再更新本表。

### 0.5 证据等级

- A：获准环境中的真实运行、测试、patch 或 trace；公开时仍需脱敏。
- B：固定 commit 的源码契约、上游测试追踪和精确 test design。
- C：类比、理论模型或尚未核实的硬件假设，只能标为待验证。

当前证据等级：宿主机基础环境指纹为 **A**；vLLM/PyTorch 框架运行尚未验证。固定源码审查从 **B/C** 起步，不能把 CUDA 可见外推为框架已跑通。

## 1. W1 D1：运行路径指纹与能力矩阵骨架

### 1.1 今日要解决的问题

一个请求怎样从 vLLM 控制面到达设备与通信层？迁移到自研芯片时，哪些边界保持不变，哪些需要 adapter、framework core patch 或替换？

### 1.2 2026-08-09 启动与 Pass A–B 历史记录

- 学习对象：上述固定源码基线。
- 今天解决的问题：完成启动配置与证据边界，并开始拆解 request → device kernel 的框架边界。
- 当前接口契约：导师已完成第一轮请求执行链源码核对；用户明确反馈尚缺 vLLM 仓库与整体架构心智模型，因此该链路暂不视为已掌握内容。
- 目标芯片能力或缺口：全部待确认。
- 决策：确认前走公开源码审查分支。
- 已完成：固定版本、建立工件位置、保存原主线返回点；完成第一轮“先猜再查”，核对请求入口、scheduler/KV、Worker/ModelRunner、attention/custom op 与 kernel 边界；把 vLLM、SGLang、PyTorch 作为浅克隆 submodules 固定到上述精确 commit。
- 证据：官方 release/tag 与固定 commit；用户确认的授权边界；当前宿主机的只读环境查询。
- 已确认：连续四周可用；今日主线 4h；Leetcode 与英语为额外时间；CUDA、CPU 可用且获准；单机多卡与 RDMA 不可用；未明确的自研芯片与 AMD 环境本轮按不可用处理。
- 仍不确定：可用的 Python/Linux 执行环境、PyTorch/vLLM 是否已经安装、固定组合能否运行、模型与实际 V1/MRV1/MRV2/attention backend/fallback 路径。
- 用户初始猜测：`HTTP 服务接收 → KV Cache 等资源调度 → 模型运行调度 → 模型代码执行 → device kernel`；初判 HTTP 保持不变、资源调度做 adapter、ModelRunner 做 core patch、kernel 替换，模型代码视情况适配。
- 导师第一轮纠偏（待后续回看）：遗漏了 `AsyncLLM / EngineCore` 跨进程边界；逻辑 KV 分配属于 scheduler 的一次调度，不是独立于“模型运行调度”的第二个 scheduler；模型 forward 与 device kernel 之间还存在 attention/custom op/backend 边界。
- 结果类型：宿主机基础环境已实测；第一轮源码结论为 B 级，但尚未通过用户理解验收；框架运行尚未验证。

### 1.3 运行路径指纹

| 项目 | 2026-08-09 只读结果 | 证据与限制 |
|---|---|---|
| 当前宿主机 | Windows / PowerShell | 当前 Codex 会话环境；尚未确认可用于 vLLM 的 Linux 环境 |
| CUDA GPU | `NVIDIA GeForce RTX 4070 Ti`，12282 MiB，compute capability `8.9` | `nvidia-smi --query-gpu=...` 实测；单卡 |
| NVIDIA driver | `610.74` | `nvidia-smi` 实测 |
| CUDA compiler | `nvcc 12.4.131` | `nvcc --version` 实测 |
| Python | 当前 shell 中 `python` 不在 `PATH` | 不代表机器没有其他 Python 环境；尚未搜索、安装或修改环境 |
| PyTorch / vLLM | 未验证 | 不从 GPU 可见或 `nvcc` 版本外推框架兼容性 |

本机 `nvcc 12.4` 与固定 PyTorch/vLLM 组合的二进制或源码构建方案是否兼容，必须在选定实际执行环境后单独验证。当前不安装依赖，也不记录设备 UUID。

### 1.4 目标芯片能力矩阵骨架

当前没有获准的自研芯片环境，能力槽位统一以“待确认”起步；后续只依据公开契约填写，不用 CUDA 能力替代目标芯片能力。

### 1.5 导师第一轮适配假设（暂缓验收）

> 本节来自固定源码的导师预核对，用于防止后续走读失焦；它不是用户当前已经理解或接受的结论。完成仓库地图、进程架构、请求生命周期和扩展边界学习后，再逐项回看并由用户自行纠正原始猜想。

| 边界 | 默认策略 | 第一轮依据 |
|---|---|---|
| HTTP / OpenAI API | 保持不变 | 协议、路由、流式返回不应感知设备类型 |
| `AsyncLLM` / `EngineCore` | 保持不变 | 前端与核心通过 client/进程边界解耦 |
| Scheduler 与逻辑 KV blocks | 保持不变 | 管理 request、token budget、抢占、前缀命中与逻辑 block 生命周期 |
| 设备发现、可用内存、物理 KV cache | adapter | 由 Platform/Worker 提供设备能力、cache spec 和物理分配 |
| Executor / Worker | adapter | OOT Platform 可以指定自定义 `worker_cls` 与 communicator |
| ModelRunner | 非 CUDA 语义时替换；CUDA-like 时优先 adapter | 可由自定义 Worker 承载，不必默认修改 Engine Core；缺少独立 `model_runner_cls` 插件点 |
| 模型定义 | 原则上保持不变 | 只在模型语义、量化或融合算子存在设备专属假设时做局部适配 |
| Attention / CustomOp | adapter，内部局部替换 | 平台可选择 attention backend，OOT custom op 可替换实现 |
| Device kernel | 替换 | 尽量保留 op schema 与调用契约，替换设备实现与注册胶水 |

`core patch` 是升级条件，不是默认起点：只有现有 `SchedulerOutput`、`KVCacheSpec`、`WorkerBase` 或 backend 契约无法表达目标芯片的内存、同步、完成或调度语义时，才提出窄范围上游修改。

## 2. 架构与 source map

### 2.0 系统学习顺序

1. **Pass A · 仓库地图**：区分产品入口、V1 引擎、模型执行、硬件后端与工程支撑；产出三级目录地图。
2. **Pass B · 进程与组件**：理解 API Server、Engine Core、Worker 的所有权与通信关系；产出进程图。
3. **Pass C · 请求生命周期**：只追一个普通 chat request，从输入处理到输出流；产出时序图与 8–12 文件 source map。
4. **Pass D · 单步模型执行**：理解 `SchedulerOutput → Worker → ModelRunner → Model → Attention/Op → Kernel`；产出控制面/执行面契约表。
5. **Pass E · 扩展与适配边界**：学习 Platform、Plugin、Worker、Backend、CustomOp、Distributed；再形成保持不变/adapter/core patch/替换矩阵。
6. **回看原始猜想**：由用户重新画图、解释偏差，并把纠偏写成自己的结论。

#### Pass A-1 · 仓库顶层分类（已通过）

```text
vLLM 仓库
├─ vllm/                  Python 产品与主要运行时
├─ csrc/ cmake/ rust/     原生实现与构建
├─ tests/ benchmarks/     正确性与性能验证
└─ docs/ examples/        设计说明与使用示例
```

- 检查题：把 `vllm/v1/engine/core.py`、`vllm/model_executor/`、`csrc/`、`tests/`、`benchmarks/`、`docs/` 分为 Python 运行时、原生实现/构建、验证评测/说明材料。
- 用户回答：Python 运行时为前两项；原生构建为 `csrc/`；其余三项为验证、评测与说明材料。
- 结果：全部正确。已建立“源码目录结构不等于运行时调用层次”的第一层认识。
- 历史推进结果：随后进入 Pass A-2，展开 `vllm/` 包的三圈地图；该步骤现已完成。

#### Pass A-2 · `vllm/` 包三圈地图（已通过）

```text
vllm/
├─ 运行主干：entrypoints/ + v1/ + model_executor/
├─ 横切能力：config/ + platforms/plugins/ + distributed/ + compilation/kernels/ir/
└─ 功能支线：输入、多模态、LoRA、解析器与可观测性
```

- 核心区别：`vllm/v1/executor/` 决定工作发到哪里执行；`vllm/model_executor/` 定义执行什么模型、层和算子。
- 定位题结果：用户正确把服务入口、token 调度、模型/Linear、平台识别、TP 通信与 kernel 分别定位到 `entrypoints/`、`v1/core/`、`model_executor/`、`platforms/`、`distributed/`、`kernels/` 或 `csrc/`。
- 结果：六项全部正确；已具备按职责缩小源码搜索范围的能力。
- 历史推进结果：随后进入 Pass A-3，展开 `vllm/v1/` 的四个主干目录；该步骤现已完成。

#### Pass A-3 · `vllm/v1/` 四个主干所有权（已通过）

| 目录 | 所有权 |
|---|---|
| `engine/` | 异步请求生命周期、Engine Core client、IPC 与引擎总协调 |
| `core/` | waiting/running 队列、调度策略与逻辑 KV blocks |
| `executor/` | `uni/mp/Ray` 等执行拓扑与任务下发 |
| `worker/` | 具体设备、rank、模型权重、物理缓存与 forward 执行 |

- 用户映射：四项全部正确。
- 用户推理：从单进程切换到多进程时，`engine/core` 应基本稳定，`executor` 变化最大；Worker 可能因通信算子而变化。
- 关键辨析：单纯把 Worker 从同进程调用改为跨进程 RPC，Worker 契约和 forward 语义理想情况下可以不变；只有同时把 `world_size` 从 1 扩到多 rank，并启用 TP/PP 等模型并行时，Worker 才需要权重分片、rank 初始化与 collective。**执行 backend（uni/mp）与并行策略（TP/PP/DP）是两个维度。**
- 结果：Pass A 三级仓库地图完成；进入 Pass B 的进程与组件架构。

#### Pass B-1 · 两条进程边界与三种部署布局（已通过）

- 用户已掌握：`uni → mp` 与 `TP=1 → TP>1` 不是同一个开关。单纯把单卡 Worker 搬到子进程，不需要模型分片，也不需要跨 rank collective。
- 新增辨析：vLLM 中至少有两条不同的进程边界。`AsyncLLM ↔ EngineCore` 属于 `engine/core client` 的前后端隔离；`Executor ↔ Worker` 才属于执行 backend 的 `uni/mp/Ray` 拓扑。笼统说“多进程主要改变 Executor”只对第二条边界成立。
- 布局 A（默认单卡在线）：API Server 与 `AsyncLLM` 在前端进程，`EngineCore + UniProcExecutor + Worker + ModelRunner` 在后端进程；已有 OS 跨进程通信，但 `TP=PP=DP=1`，无模型分片和跨 rank collective。
- 布局 B（原生显式单卡 `mp`）：当 `TP=PP=1` 且显式选择 `--distributed-executor-backend mp` 时，配置不会被覆盖为 `uni`；`MultiprocExecutor` 会创建一个 `WorkerProc`。此时比布局 A 再增加一条 Executor↔Worker IPC，但仍无模型分片和跨 rank collective。
- 布局 C（多 rank `mp + TP/PP`）：`world_size>1` 时默认倾向选择 `mp`，Executor 创建多个 Worker 进程；模型并行同时让 Worker/ModelRunner/模型层增加 rank、权重分片和 collective 语义。
- 另一个原生正交维度是 `--api-server-count N`：可在 `TP=PP=DP=1` 时扩展多个前端 API 进程，共享同一个 EngineCore/模型实例，用于扩展 HTTP、tokenization 与输入输出处理；它不进入模型 world size，也不新增模型分片。
- 证据：[`AsyncLLM` 创建异步多进程 Engine Core client](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L145-L153)；[`EngineCoreClient` 的 in-process 与 MP client 分类](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core_client.py#L71-L105)；[`ParallelConfig` 的默认 backend 选择](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/config/parallel.py#L883-L928)；[`MultiprocExecutor` 按 local world size 创建 Worker 子进程](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/executor/multiproc_executor.py#L158-L201)；[官方测试直接覆盖 `world_size=1` 的单 Worker `mp`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/tests/distributed/test_multiproc_executor.py#L23-L83)；[官方文档给出 4 API 进程 + 1 EngineCore 的例子](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/docs/configuration/optimization.md#L315-L331)。
- 验收结果：已通过。用户正确指出，仅看到 `MultiprocExecutor` 启动一个 `VllmWorker-0` 不能推断启用了 TP，也可能只是单卡显式选择 `mp`。

#### Pass B-2 · 一个前端连接多个 EngineCore（已通过）

- 用户问题：能否让一个 API 对应多个后台 EngineCore，并由 API server 根据各 EngineCore 的当前压力分流请求。
- 原生对应：这正是在线 **Data Parallel 内部负载均衡**。`data_parallel_size > 1` 且未启用 external LB 时，`EngineCoreClient.make_client` 返回 `DPLBAsyncMPClient`；每个 DP rank 对应独立 EngineCore、Scheduler、请求队列、逻辑/物理 KV 状态与模型副本。若再叠加 TP/PP，则每个 EngineCore 后面管理一组共同组成该副本的 Workers。
- 分流位置：不在 OpenAI HTTP route，而在 API/`AsyncLLM` 进程里的 Engine Core client 层。这样协议处理不感知 EngineCore 数量，路由发生在 `EngineCoreRequest` 发出之前。
- 压力采集（设计与 MoE 实现）：MoE 的 `DPEngineCoreProc` 在 GPU step 前后发布 Scheduler 的 `[waiting, running]` 请求数；`DPCoordinator` 汇总后约每 100 ms 广播给前端。
- 选择策略：`DPLBAsyncMPClient` 计算 `score = waiting * 4 + running`，选择最小分数；在下一次统计到来前先乐观增加本地 waiting 计数，并轮转同分起点，减少突发请求集中到同一 EngineCore。
- 请求归属：一个请求选中 EngineCore 后，其后续 decode、KV cache 和 Scheduler 状态都留在该 EngineCore；当前策略不做执行中的请求迁移。client 保存 `request_id → EngineCore`，以便把 abort 发回正确 EngineCore。
- 亲和性与限制：默认策略不看 prompt token 数、预计生成长度、GPU 利用率、空闲 KV blocks 或 prefix-cache 命中；官方文档也明确把 KV-cache-aware routing 列为未来可增强项。HTTP header `X-data-parallel-rank` 可显式指定 DP rank，为外部 router 做会话或前缀亲和提供入口，但默认不会自动保证跨 HTTP 请求的会话黏性。
- 固定版本落差：官方文档把 internal DP 统一描述为基于各 EngineCore 的 running/waiting 队列，但 `v0.26.0` 中 `_maybe_publish_request_counts()` 只存在于断言 MoE 模型的 `DPEngineCoreProc`；dense DP 会把每个 rank 当作 `DP=1` 的普通 `EngineCoreProc`，未找到等价的实时计数上报。因此：MoE internal DP 有完整的实时压力反馈链；dense internal DP 在该提交中主要依赖 API client 的本地 optimistic waiting 与轮转，不能笼统声称具有相同的实时 queue-aware 反馈。
- 证据：[`make_client` 选择内部 DP LB client](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core_client.py#L126-L132)；[`DPLBAsyncMPClient` 的打分与选择](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core_client.py#L1380-L1447)；[`DPCoordinator` 汇总 waiting/running](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/coordinator.py#L23-L56)；[MoE `DPEngineCoreProc` 在 step 前后发布计数](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L1844-L1860)；[dense DP 退回普通 `EngineCoreProc`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L1287-L1299)；[官方 DP 部署说明](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/docs/serving/data_parallel_deployment.md#L21-L77)。
- 本地限制：当前只获准单卡 CUDA，无法在本机实测多个完整 DP 副本；本节先做固定源码 B 级审查，不外推运行结果。
- 验收结果：已通过。用户正确计算 EngineCore 0 为 5、EngineCore 1 为 4，并选择 EngineCore 1；也正确指出，执行中请求不能仅因另一 Core 变空闲而迁移，因为原 Core 持有请求调度状态、逻辑 KV 映射和对应的物理 KV 内容。

#### Pass B-3 · 组件状态所有权（已通过）

| 组件 | 主要持有状态 | 不负责 |
|---|---|---|
| API Server / `AsyncLLM` | 输入输出语义、`OutputProcessor`、流式 collector、Core client | token 级调度、模型 forward |
| `DPLBAsyncMPClient` | EngineCore 负载快照、`request_id → EngineIdentity` 路由记录 | Scheduler 队列、KV cache 内容 |
| `DPCoordinator` | 各 EngineCore 的汇总计数、DP wave/running 控制状态 | 选择具体请求、持有请求或 KV |
| `EngineCore` / Scheduler | Request 生命周期、waiting/running、token 进度、逻辑 KV blocks 与调度决策 | 模型权重、物理 KV tensor |
| Executor / Worker / ModelRunner | 执行拓扑、设备/rank、模型权重或 shard、物理 KV tensor、持久 batch/block table、forward 与采样设备状态 | OpenAI 协议与用户流式连接 |

- 迁移含义：真正的 live migration 至少要迁移或重建 Scheduler/Request 状态、逻辑到物理 block 映射、已计算 KV 内容、Worker 侧持久 batch 状态以及前端输出/abort 路由。重新在新 EngineCore 做一次 prefill 可以重建 KV，但那属于重算/重启，不是无损迁移。
- 验收结果：五项全部正确。用户把请求分流、统计汇总、token/逻辑 KV 调度、物理 KV/forward、输出 collector/流式返回依次归给 `DPLBAsyncMPClient`、`DPCoordinator`、EngineCore/Scheduler、Worker/ModelRunner、API Server/AsyncLLM。

#### Pass B-4 · 完整进程图收口（已通过）

- 目标：在一张图中同时表达 frontend、DP routing/coordinator、每个 EngineCore 的独立调度状态，以及每个 EngineCore 内 `uni/mp` Executor 对 Worker 进程位置的影响。
- 用户回答正确部分：`DPLBAsyncMPClient` 在 API/AsyncLLM 进程；每个 `backend=uni` 的 EngineCore 进程内含 Scheduler、UniProcExecutor、Worker 与 ModelRunner；切换为 `mp` 后每个 EngineCore 各新增一个 Worker 子进程，Scheduler 与 MultiprocExecutor 仍留在原 EngineCore 进程。
- 唯一纠正：`DPCoordinator` 不是嵌在某个 EngineCore 内，而是由 `DPCoordinator` wrapper 通过 `multiprocessing.Process` 启动的独立 `VLLM_DP_Coordinator` 进程。它作为所有 DP ranks 的对等汇总点，不能归属于其中一个 EngineCore。
- 因此 `API server count=1, DP=2, TP=1, backend=uni` 忽略 supervisor/监控后的主要进程数为 4：一个 API/AsyncLLM、一个 DPCoordinator、两个各自内嵌 Worker 的 EngineCore。
- 证据：[`DPCoordinator` 显式创建独立进程](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/coordinator.py#L79-L125)；[`launch_core_engines` 启动并连接 Coordinator](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/utils.py#L1105-L1127)。
- 补验结果：已通过。用户确认 `backend=mp` 后共有 6 个主要 OS 进程，两个 ModelRunner 分别位于各自的 Worker 子进程。

#### Pass B-5 · Worker 与 ModelRunner 职责边界（已通过）

一句话边界：**Worker 是设备/rank 的生命周期、资源和通信外壳；ModelRunner 是设备内把 `SchedulerOutput` 变成 batch/tensor、模型执行与采样结果的推理运行时。** ModelRunner 不只是一次 `model.forward()` 调用。

| 阶段 | Worker 主要职责 | ModelRunner 主要职责 |
|---|---|---|
| 进程与设备初始化 | 持有 `rank/local_rank`，选择设备，初始化 distributed/NCCL、seed、显存快照与 workspace | 由 Worker 在设备就绪后构造；建立设备内执行所需的持久状态 |
| 模型加载 | 对 Executor 暴露统一 `load_model` 生命周期接口，设置 allocator/memory-pool/权重传输等外围上下文 | 实际创建并持有 `torch.nn.Module`、加载权重及模型相关执行组件 |
| KV cache | 探测可用显存、协调 cache 配置与初始化时机、初始化 KV transfer connector | 给出 cache spec，分配并持有物理 KV tensors，维护 block table/slot mapping 并在 attention 中使用 |
| 每个 engine step | 接收 Executor RPC；等待/发起 PP 边界通信；包裹 profiling/同步检查；调用 ModelRunner | 增删/更新持久 request state，构造 `InputBatch`、positions、block tables、slot mappings、attention metadata 与 LoRA/MM 输入 |
| 模型执行与输出 | 处理 rank 外壳和 PP intermediate tensors，转发执行结果 | 选择 eager/compile/CUDA Graph 路径，调用模型，计算 logits、采样/spec decode/structured output，并更新设备侧请求状态 |
| 运维能力 | health、sleep/wake、profile、LoRA/权重更新、资源清理等进程/设备级入口 | 实现其中与模型、cache、图和执行状态直接相关的具体操作 |

- 重要细节：Worker 经常“拥有 API、委托实现”。例如 `Worker.load_model()` 是生命周期入口，但实际调用 `model_runner.load_model()`；Worker 决定可分给 KV cache 多少显存并触发初始化，ModelRunner 决定具体 tensor 布局并持有它们。固定 v0.26.0 中 `gpu_worker.py` 内的实际类名是 `Worker`，不是 `GPUWorker`。
- 通信边界：Worker 初始化 distributed process groups，并在外层显式处理 Pipeline Parallel 的 intermediate tensor 收发；Tensor Parallel collective 通常发生在模型 forward 的层/算子与 distributed primitives 中，不能把所有通信都简单归为 Worker wrapper。
- 设计价值：相同 Worker 设备外壳可选择 MRV1 或 MRV2；`uni/mp/Ray` 改变 Executor/Worker 的放置和 RPC，不要求重写 ModelRunner 的 batch/forward 算法。
- 证据：[`WorkerBase` 的硬件与控制面抽象契约](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/worker_base.py#L39-L43)；[`Worker.init_device` 初始化设备/分布式并选择 ModelRunner](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_worker.py#L297-L416)；[`Worker.execute_model` 包裹 PP 通信后委托 ModelRunner](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_worker.py#L1087-L1175)；[MRV2 更新请求、准备输入并执行模型](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu/model_runner.py#L1151-L1391)；[MRV2 计算 logits 与采样](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu/model_runner.py#L1395-L1535)。
- 验收结果：五项判断全部正确。设备、rank、distributed/NCCL 初始化和 PP intermediate tensor 外层收发属于 Worker；`SchedulerOutput → InputBatch/block table/slot mapping`、图选择、模型执行与 sampling 属于 ModelRunner。MRV1/MRV2 是同一 Worker 生命周期外壳内的执行实现选择，不改变进程拓扑。
- 边界补充：模型加载与 KV cache 是“两层协作”而不是单方独占。Worker 提供生命周期入口、设备上下文、显存预算和初始化时机；ModelRunner 实际加载并持有模型，建立并持有物理 KV tensors、block table 与 attention 执行状态。

#### Pass A–B · 阶段材料收口（已完成）

- 结果型文章：[`深入学习理解vLLM/1-Repository-and-Process-Architecture.md`](深入学习理解vLLM/1-Repository-and-Process-Architecture.md)。
- 过程型记录：[`log/2026-08-09-vllm-repository-and-process-architecture.md`](log/2026-08-09-vllm-repository-and-process-architecture.md)。
- 技术记忆卡：[`cards/vllm-repository-and-process-architecture.md`](cards/vllm-repository-and-process-architecture.md)，共 25 张原子卡。
- 边界：以上材料只收录已通过的 Pass A–B；Pass C 的导师预讲不计入已掌握内容。

<a id="pass-c1-openai-to-engine-core-request"></a>
#### Pass C-1 · OpenAI 请求到 `EngineCoreRequest`

> 以下是导师为下一阶段准备的固定源码预核对。用户尚未完成 Pass C-1 的问答验收，不计入当前学习进度。

本节只追请求进入 EngineCore 之前的前端路径，不提前展开 Scheduler 或模型执行：

`POST /v1/chat/completions` → `OpenAIServingChat._create_chat_completion()` → `render_chat_request()` → `EngineInput` + `SamplingParams` → `AsyncLLM.generate()/add_request()` → `InputProcessor.process_inputs()` → `EngineCoreRequest` → `EngineCoreClient.add_request_async()`。

- OpenAI 协议层：`messages`、tools、chat template、HTTP headers 与 `stream` 等先由 API serving 层解释；chat 内容被 render/tokenize 为 `EngineInput`，生成参数被归一化为 `SamplingParams`。
- EngineCore 输入契约：`InputProcessor` 生成的 `EngineCoreRequest` 携带 request id、prompt token IDs/embeds、多模态 features、sampling/pooling params、到达时间、LoRA、cache salt、priority、DP rank 与 trace headers；它不携带 FastAPI `Request` 或原始 OpenAI `messages`。
- 输出竞态防护：`AsyncLLM` 先在本进程创建 `RequestOutputCollector`，再把请求注册到 `OutputProcessor`，最后才通过 client 把 `EngineCoreRequest` 发往独立 EngineCore 进程。这样 EngineCore 即使很快返回，前端也已有接收该 request id 输出的位置。
- 流式边界：`request.stream` 一方面决定 API 层最终选择 SSE generator 还是一次性 JSON response，另一方面会被投影为 `SamplingParams.output_kind`（`DELTA` 或 `FINAL_ONLY`）并进入核心；但原始 `stream` 字段、FastAPI `Request` 和 HTTP 连接本身都留在前端。
- 设计动机：EngineCore 不理解 OpenAI chat schema、chat template 或 HTTP 生命周期，同一个 token 级核心因此可以复用于 chat、completion、离线调用等不同入口。
- 证据：[`/v1/chat/completions` 路由](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/api_router.py#L40-L61)；[chat render、参数归一化与 `AsyncLLM.generate`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/serving.py#L255-L384)；[`AsyncLLM` 先注册 collector 再跨进程发送](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L333-L412)；[`InputProcessor` 构造 `EngineCoreRequest`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/input_processor.py#L242-L385)。
- 检查题（尚无学习者证据）：分别说明 `messages`、`temperature/top_p/max_tokens`、`stream=true + HTTP connection` 在跨入 EngineCore 前被放到哪里或留在哪里，并解释为什么不直接把 `ChatCompletionRequest` 发给 EngineCore。当前唯一执行动作仍只由 Checkpoint 保存。

### 2.1 vLLM request sequence

第一轮固定源码核对得到两条相连但不同层级的链：

```text
POST /v1/chat/completions
→ OpenAIServingChat
→ AsyncLLM
→ EngineCore（跨进程）
→ Scheduler.schedule + KVCacheManager 逻辑块分配
→ SchedulerOutput
→ Executor / Worker
→ ModelRunner
→ model forward / Attention
→ torch.ops.vllm.unified_* custom op
→ AttentionImpl backend
→ device kernel
```

关键事实：

- [API route](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/api_router.py#L53-L61) 进入 `OpenAIServingChat`，后者调用 [EngineClient.generate](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/serving.py#L363-L376)。
- `AsyncLLM` 把请求加入本进程的输出处理器，再通过 [EngineCore client](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L400-L413) 送入独立 Engine Core；因此这不是一条同步 Python call stack。
- [EngineCore.step](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L576-L606) 依次完成 `schedule → execute_model → update_from_output`。Scheduler 内部调用 [KVCacheManager](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L519-L526) 分配逻辑 blocks，但不直接写设备 KV tensor。
- `SchedulerOutput` 经 Executor/Worker 到达 [GPU ModelRunner](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_worker.py#L1085-L1159)；Runner 构造执行状态并调用模型 forward。
- [Attention.forward](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/model_executor/layers/attention/attention.py#L488-L582) 先进入 `torch.ops.vllm.unified_*` 编译图边界，再由注册实现调用 `AttentionImpl`。custom op 不是 device kernel 本身。
- vLLM 的 [OOT Platform 规范](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/docs/design/plugin_system.md#L100-L117) 要求平台指定 Worker、attention backend 与 communicator；因此自研芯片适配默认从这些扩展面开始。

### 2.2 8–12 文件 source map

### 2.3 vLLM EP/PD 主图

### 2.4 SGLang/ATOM 边界对照

## 3. 适配设计

### 3.1 六层适配矩阵

### 3.2 既有经验迁移矩阵

### 3.3 C1–C5 Change Cards

## 4. 验证与证据

### 4.1 Correctness 与 failure matrix

### 4.2 分阶段 bring-up

### 4.3 Benchmark protocol

### 4.4 结果与待验证项

## 5. Risk register

## 6. Upstream validation anchor

> W1 D5 在 source map 建立后选择唯一锚点。以下只登记候选，不代表已决定提交 issue 或 PR。

### 6.1 🔖 候选 U1：dense internal DP 实时队列统计链缺口

- 发现日期：2026-08-09。
- 固定基线：vLLM `v0.26.0`，commit `568afb3a13806beb53bb2e6bd518269357b237c0`。
- 用户意图：把该发现发展为一次可验证、可向上游贡献的开源实践；优先形成最小复现、回归测试与窄范围修复或文档澄清。
- 预期契约：[官方 DP 文档](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/docs/serving/data_parallel_deployment.md#L75-L77)称 internal DP 根据各 EngineCore 的 running/waiting 队列做负载均衡；[`VllmConfig.needs_dp_coordinator`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/config/vllm.py#L624-L645)也明确说 non-MoE internal/hybrid LB 启动 Coordinator 是为了收集并发布 queue stats。
- 实现观察：dense DP 在 [`run_engine_core`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L1287-L1299) 中退回普通 `EngineCoreProc`；实时 `_maybe_publish_request_counts()` 只位于断言 MoE 的 [`DPEngineCoreProc`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L1844-L1860) 及其 [busy loop](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L2002-L2043)。固定提交中未找到 dense 等价发布路径。
- 潜在影响：dense 的 [`DPLBAsyncMPClient`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core_client.py#L1413-L1447) 虽执行 `waiting * 4 + running`，但可能缺少来自后端的实时计数，更多依赖前端 optimistic waiting 与同分轮转；在长短请求混合或多 API client 下可能产生负载偏斜。此处仍是待复现假设，不写成已证实性能缺陷。
- 待区分假设：① dense 发布链为实现遗漏，应补齐公共统计上报；②当前行为是有意设计，文档与配置注释需要说明限制；③该问题已在更新版本修复，固定 tag 只适合作为历史回归案例。
- 上游行动前置：
  - ⬜ 对比届时最新 `main`，确认代码是否仍存在。
  - ⬜ 检索已有 issue、PR、讨论与 maintainer 设计意图，避免重复工作。
  - ⬜ 建立 dense `DP=2` 最小复现，观察 Coordinator 与 API client 收到的统计；当前单卡环境不能完成真实双副本测试。
  - ⬜ 先写能暴露缺口的测试，再决定修改代码还是文档。
- 最小贡献路径：
  1. 若为文档问题：明确 MoE 与 dense internal DP 在该版本的统计反馈差异。
  2. 若为代码问题：把请求计数发布抽到普通/DP EngineCore 可共享的窄接口，并避免把 MoE wave 语义错误带入 dense 路径。
  3. 无论哪条路径：补充 dense internal DP 的路由统计回归测试；必要时增加长短请求混合的分流验证。
- 完成定义：有固定版本最小复现、最新主线核验、已有讨论检索、失败测试或明确文档证据、maintainer 可审查的单一问题陈述；只有满足这些条件后才创建 issue 或提交 PR。
