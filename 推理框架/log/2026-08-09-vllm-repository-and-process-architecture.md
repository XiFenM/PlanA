# 学习记录 · 2026-08-09 — vLLM 仓库地图、进程拓扑与组件边界

> 来源：AI 会话 Codex:019fe49d（04:21–14:12 技术学习段）· 模块：推理框架 · 关联产出：[从仓库地图到进程与组件边界](../深入学习理解vLLM/1-Repository-and-Process-Architecture.md)

## 问答与要点

- [纠错] 最初怎样把 Scheduler 的一次决策拆成了两层？——场景：第一次凭经验画 request → kernel 链路。我说“KV Cache 等资源调度 → 模型运行调度”，把二者当成前后两个 scheduler；正确表述是 Scheduler 在同一次决策中选择请求和 token、分配逻辑 KV blocks，并产出 `SchedulerOutput`，物理 KV tensor、slot mapping 和实际执行再由 Worker/ModelRunner 等执行层处理。
- [要点] 如何把 vLLM 仓库顶层压缩成四类？——`vllm/` 是 Python 产品与主要运行时；`csrc/`、`cmake/` 和 Rust 目录属于原生实现与构建；`tests/`、`benchmarks/` 负责验证和评测；`docs/`、`examples/` 提供说明与示例。目录地图不是运行时调用栈。（来源：关联文章 §学习过程 1）
- [要点] 面对源码问题时，如何选择第一站目录？——服务入口先去 `entrypoints/`，调度先去 `v1/core/`，模型和并行 Linear 先去 `model_executor/`，平台识别先去 `platforms/`，TP collective 先去 `distributed/`，具体 kernel 再去 `kernels/` 或 `csrc/`。这轮六项定位全部答对。（来源：关联文章 §学习过程 1）
- [要点] `vllm/v1/` 的 `engine/core/executor/worker` 分别拥有哪类职责？——`engine` 管异步请求、Core client、IPC 和总协调；`core` 管请求队列、调度和逻辑 KV；`executor` 隔离 `uni/mp/Ray` 执行拓扑；`worker` 管设备、rank、模型资源与执行入口。这轮四项所有权映射全部答对。（来源：关联文章 §学习过程 2）
- [纠错] 为什么“多进程会让 Worker 多一些通信算子”缺少条件？——场景：讨论从单进程切到多进程时哪些目录变化最大。我说“对 worker 部分也会有变化，因为多进程并行会多一些通信算子”；正确表述是 `uni/mp/Ray` 回答组件放在哪里、如何调用，TP/PP 才回答模型怎样跨设备切分。只改变 Worker 的进程位置时，不必新增模型分片或跨 rank collective。
- [纠错] “单纯增加进程不会影响 Worker”为什么又过于绝对？——场景：理解 `uni/mp` 与 TP 不同后，我把结论推得太远。单卡切到 `mp` 虽不改变模型分片和 collective，却会改变 Worker 的进程位置、Executor↔Worker IPC，以及 CUDA context、模型加载和资源生命周期的归属；更准确的是“不改变 Worker 的模型并行语义”。
- [要点] 原生 vLLM 哪些场景会增加进程但不启用模型并行？——常规单卡在线路径已经把 API/AsyncLLM 与 EngineCore 隔离；单卡可显式使用 `mp` 创建一个 Worker 子进程；还可以只增加 API Server 进程扩展 HTTP 和 tokenization。这些场景都不要求模型分片。（来源：关联文章 §学习过程 3）
- [要点] 只看到一个 `VllmWorker-0` 能否断定启用了 TP？——不能，因为 `TP=PP=1` 时显式选择 `mp` 也会创建一个 Worker 子进程。进程数量、Executor backend 与模型并行度是三个需要分别核对的维度。（来源：关联文章 §学习过程 3）
- [纠错] 内部 DP 为什么不是“把一个 EngineCore 变成多进程”？——场景：我提出“把 EngineCore 变成多进程，由一个 API 给多个后台 engine 分流”。更准确的说法是启动多个独立 EngineCore，每个拥有自己的 Scheduler、请求队列、逻辑 KV 状态和模型副本，再由 API 进程中的 `DPLBAsyncMPClient` 为新请求选择目标。
- [要点] 固定 v0.26.0 的内部 DP 如何给新请求选择 EngineCore？——客户端计算 `$score = 4 \times waiting + running$` 并选择最低分，还会在新快照到来前乐观增加本地 waiting，并轮转同分起点。它不直接查看 token 工作量、GPU 利用率、空闲 KV blocks 或 prefix-cache 命中。（来源：关联文章 §学习过程 4）
- [要点] 为什么执行中的请求不能直接迁移到另一个空闲 EngineCore？——我正确指出原 EngineCore 持有调度状态和 KV 相关状态；继续展开后，还需要包括 token 进度、逻辑 block 映射、Worker 侧物理 KV 与持久 batch、采样状态，以及前端输出和 abort 路由。重新 prefill 可以重建 KV，但属于重算而非无损迁移。（来源：关联文章 §学习过程 4）
- [纠错] AI 对 dense internal DP 实时压力反馈做过什么过度概括？——场景：AI 最初统一表述“每个 EngineCore 在 step 前后上报 waiting/running”。固定 `v0.26.0` 中，实时 `_maybe_publish_request_counts()` 链只在 MoE 使用的 `DPEngineCoreProc` 中；dense DP 使用普通 `EngineCoreProc`，未找到等价发布链，因此不能声称二者拥有相同的实时后端反馈。
- [要点] DP 多 EngineCore 场景中的状态所有权如何划分？——新请求选目标属于 `DPLBAsyncMPClient`，负载汇总属于 `DPCoordinator`，token 进度与逻辑 KV 属于 EngineCore/Scheduler，物理 KV 与模型执行属于 Worker/ModelRunner，输出 collector 与流式返回属于 API Server/AsyncLLM。这轮五项映射全部答对。（来源：关联文章 §学习过程 5）
- [纠错] `DPCoordinator` 位于哪个进程？——场景：在 `API=1, DP=2, TP=1, backend=uni` 的进程题中，我说“DPCoordinator 在 EngineCore 进程上”，并据此算出 3 个进程。正确答案是它作为所有 DP ranks 的对等汇总点运行在独立进程中，因此共有 1 个 API、1 个 Coordinator 和 2 个 EngineCore，共 4 个主要进程。
- [要点] 上述 DP=2 场景切换为 `backend=mp` 后有多少主要进程？——每个 EngineCore 各新增一个 Worker 子进程，总数从 4 增加到 6；Scheduler 和 MultiprocExecutor 留在 EngineCore 进程，ModelRunner、模型权重和物理 KV 跟随 Worker。补验时这一判断回答正确。（来源：关联文章 §学习过程 5）
- [纠错] ModelRunner 是否只负责调用模型 forward？——场景：我问“ModelRunner 只处理模型 forward，Worker 还处理别的吗”。正确边界是 Worker 拥有 device/rank/distributed 环境、进程与资源生命周期、显存预算和 PP 外层通信；ModelRunner 拥有持久 batch、输入 tensor、物理 KV、block table、slot mapping、attention metadata、图执行、模型调用和 sampling 等设备内热路径。
- [要点] KV Cache 为什么是 Worker 与 ModelRunner 的协作边界？——Worker 决定设备上下文、可用显存预算、初始化时机和生命周期；ModelRunner 实际分配并持有物理 KV tensor，维护 block table/slot mapping，并在 attention 中消费它们。模型加载也具有类似的“Worker 提供入口和上下文、ModelRunner 实际加载持有”结构。（来源：关联文章 §学习过程 6）
- [要点] 从 MRV1 切换到 MRV2 是否需要改变进程拓扑？——不需要。MRV1/MRV2 是同一 Worker 生命周期外壳内的执行实现选择，变化集中在设备内 batch、tensor、图执行和 sampling 算法；补验中的五项职责判断全部正确。（来源：关联文章 §学习过程 6）
- [纠错] 固定版本中的 GPU Worker 类究竟叫什么？——场景：AI 讲解时使用了“`GPUWorker` 外壳”这一简称。`v0.26.0` 的 `gpu_worker.py` 中实际类名是 `Worker`；同时，“初始化归 Worker”只限定 device、rank、distributed/NCCL 等环境，ModelRunner 仍会初始化自己的 batch、tensor、KV 和 graph 状态。

## 遗留问题

- [遗留] 对比最新 `main`、检索已有 issue/PR、确认 maintainer 预期并构造 dense `DP=2` 最小复现，判断 internal DP 实时计数差异是实现遗漏、文档未说明限制，还是已经在新版本修复。（已挂账：关联文章 §实践、`EP-PD自研芯片适配设计与验证包.md` §6.1）
- [遗留] 最初的自研芯片五层适配猜想及 `adapter/core patch/替换` 分类尚未完成理解验收，需在 Pass C–E 后重新作答，不能把导师预核对当作已掌握结论。（已挂账：关联文章 §后续预告、`计划/学习断点.md`）
- [遗留] DP/TP 多卡进程图、请求迁移和 dense 统计链当前只有固定源码证据，没有本地多卡运行验证。（已挂账：关联文章 §实践）
