# 墨墨记忆卡 · vLLM 仓库与进程架构

> 素材：[阶段文章](../深入学习理解vLLM/1-Repository-and-Process-Architecture.md) + [学习记录](../log/2026-08-09-vllm-repository-and-process-architecture.md)。
> 卡型：技术Q&A卡，模板见 `.claude/skills/memo-cards/references/tech-qa-template.md`，列序 `问题 → 答案 → 锚点 → 来源`。
> 去重：文章〔面试问题 Q&A〕为主牌；学习记录只补文章未单独设问的要点与纠错过程，遗留问题不制卡。
> ⚠️ 首次使用：先在墨墨新建「vLLM 架构」牌组，把技术Q&A模板粘进「表格导入」左侧面板，再导入本表。

## 技术Q&A卡

```tsv
问题	答案	锚点	来源
vLLM 中 executor/ 与 model_executor/ 有什么区别？	vllm/v1/executor/ 负责执行拓扑和任务下发，例如 uni、mp 或 Ray；vllm/model_executor/ 负责模型、层、权重、量化和算子，即具体执行什么。前者隔离放置与 RPC，后者承载模型计算内容。	executor = topology；model_executor = computation	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q1
vllm/v1/engine/core.py 与 vllm/v1/core/ 有什么区别？	engine/core.py 中的 EngineCore 是总协调组件，组织每轮 schedule、execute 和 update；v1/core/ 存放 Scheduler、KV Cache Manager 等调度算法和逻辑资源状态。两者分别是总协调者与其调度资源部门。	EngineCore ≠ v1/core	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q2
为什么 uni → mp 不等于 TP=1 → TP>1？	uni/mp 决定 Worker 与 EngineCore 是直接调用还是跨进程调用；TP 决定模型权重和计算是否跨多个 rank 分片。单卡显式 mp 会增加 IPC，但不要求模型分片或跨 rank collective。	uni/mp = placement；TP = sharding	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q3
看到一个 VllmWorker-0，能否判断已经启用 TP？	不能。TP=1 时显式选择 mp 也会创建一个 Worker 子进程；必须同时查看 tensor_parallel_size、world size 和模型分片配置。	1 × VllmWorker-0 ≠ TP	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q4
常规单卡在线 vLLM 为什么仍然是多进程？	API Server/AsyncLLM 与 EngineCore 通常通过独立进程和 IPC 隔离。这样 HTTP、tokenization 和流式连接的抖动不会干扰 EngineCore 稳定的迭代热循环；uni 只表示 Worker 与 EngineCore 同进程。	frontend IPC isolates core hot loop	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q5
一个 API Server 如何连接多个 EngineCore？	内部 DP 会启动多个独立 EngineCore，每个拥有自己的 Scheduler、KV 状态和模型副本。API 进程中的 DPLBAsyncMPClient 在请求进入 EngineCore 前选择目标实例，HTTP route 不需要感知副本数量。	DPLBAsyncMPClient → N × EngineCore	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q6
vLLM v0.26.0 的内部 DP 路由公式是什么？	前端计算 score = 4 × waiting + running，并选择分数最低的 EngineCore。它是加权请求计数，不直接考虑 token 工作量、GPU 利用率、剩余 KV blocks 或 prefix-cache locality。	score = 4 × waiting + running	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q7
为什么执行中的请求不能直接迁移到空闲 EngineCore？	原 EngineCore/Scheduler 持有 token 进度和逻辑 KV 映射，Worker/ModelRunner 持有物理 KV 与持久执行状态，前端还保存输出和 abort 路由。除非迁移或重建这些状态，否则新 EngineCore 无法继续等价的下一步执行。	Scheduler state + physical KV + output route	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q8
DPCoordinator 位于哪个进程？	在本文讨论的 internal DP 场景中，它是独立 OS 进程，而不是 API 进程或任一 EngineCore 进程。它是多个 DP ranks 的对等协调和汇总点，不能归属于某个 rank。	DPCoordinator = independent process	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q9
Worker 与 ModelRunner 如何分工？	Worker 拥有设备、rank、distributed 环境和资源生命周期，并向 Executor 暴露进程级接口。ModelRunner 拥有设备内推理热路径，包括 batch/tensor、物理 KV、attention metadata、图执行、模型调用和采样状态。	Worker = lifecycle；ModelRunner = hot path	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q10
物理 KV Cache 属于 Worker 还是 ModelRunner？	两者协作。Worker 负责显存预算、初始化时机和生命周期编排；ModelRunner 实际分配并持有 KV tensor，维护 block table/slot mapping，并在模型执行中使用。	Worker budgets；Runner allocates and maps	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q11
从 MRV1 切换到 MRV2 是否需要改变进程拓扑？	不需要。MRV1/MRV2 是同一 Worker 外壳内的执行实现选择，主要改变设备内 batch、输入准备、图执行和采样算法，不改变 API、EngineCore、Executor、Worker 的进程关系。	MRV1/MRV2 ∈ Worker	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q12
dense internal DP 的实时负载反馈是否已经确认有 bug？	没有。固定 v0.26.0 中观察到文档描述与源码发布链可能存在落差，但尚未完成最新主线核对、多卡复现和上游讨论检索；当前只能登记为待验证的贡献候选。	source observation ≠ confirmed bug	../深入学习理解vLLM/1-Repository-and-Process-Architecture.md §下游透镜 Q13
如何把 vLLM 仓库顶层压缩成四类？	vllm/ 是 Python 产品与主要运行时；csrc/cmake/Rust 属于原生实现和构建；tests/benchmarks 负责验证与评测；docs/examples 提供设计说明和示例。目录地图不是运行时调用栈。	runtime / native / validation / docs	../log/2026-08-09-vllm-repository-and-process-architecture.md [要点] 仓库顶层
面对 vLLM 源码问题，如何选择第一站目录？	入口先去 entrypoints/，调度先去 v1/core/，模型与并行 Linear 先去 model_executor/，平台识别先去 platforms/。TP collective 先去 distributed/，具体 kernel 再去 kernels/ 或 csrc/。	entry → schedule → model → platform → comm → kernel	../log/2026-08-09-vllm-repository-and-process-architecture.md [要点] 目录定位
vllm/v1/ 的 engine、core、executor、worker 分别负责什么？	engine 管异步请求、Core client、IPC 和总协调；core 管请求队列、调度和逻辑 KV；executor 隔离 uni/mp/Ray 执行拓扑；worker 管设备、rank、模型资源和执行入口。	engine / core / executor / worker	../log/2026-08-09-vllm-repository-and-process-architecture.md [要点] V1 所有权
API=1、DP=2、TP=1 时，uni 与 mp 各有多少个主要进程？	backend=uni 时有 1 个 API、1 个独立 DPCoordinator、2 个各自内嵌 Worker 的 EngineCore，共 4 个。切到 mp 后每个 EngineCore 各新增一个 Worker 子进程，共 6 个；ModelRunner、权重和物理 KV 随 Worker 移动。	DP=2：uni 4 processes → mp 6 processes	../log/2026-08-09-vllm-repository-and-process-architecture.md [要点] DP 进程图
为什么“KV 资源调度 → 模型运行调度”不是两个前后 Scheduler？	我最初把二者画成两层；实际上 Scheduler 在同一次决策中选择请求和 token、分配逻辑 KV blocks，并产出 SchedulerOutput。物理 KV tensor、slot mapping 和实际执行才进入 Worker/ModelRunner 等执行层。	one schedule decision → SchedulerOutput	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] Scheduler 分层
为什么“切换多进程会让 Worker 增加通信算子”缺少条件？	我曾把进程布局与模型并行混在一起。uni/mp/Ray 只决定组件放置和调用方式；只有同时启用 TP/PP 时，Worker/模型层才需要 rank、权重分片和跨 rank collective。	process placement ≠ model parallel semantics	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] 多进程与通信
为什么“单纯增加进程不会影响 Worker”又过于绝对？	单卡切到 mp 不改变模型分片和 collective，却会改变 Worker 的进程位置、Executor↔Worker IPC，以及 CUDA context、模型加载和资源生命周期的归属。准确说法是“不改变 Worker 的模型并行语义”，而不是“完全不影响 Worker”。	same model semantics；different placement/lifecycle	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] Worker 影响
内部 DP 为什么不是“把一个 EngineCore 变成多进程”？	我最初这样描述，但原生结构实际是多个彼此独立的 EngineCore。每个实例拥有自己的 Scheduler、请求队列、逻辑 KV 状态和模型副本，再由 DPLBAsyncMPClient 为新请求选择目标。	N independent EngineCores，not one split Core	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] DP 表述
对 dense internal DP 的实时统计链，先前哪里概括过度？	AI 最初统一表述每个 EngineCore 都在 step 前后上报 waiting/running。固定 v0.26.0 中该实时发布链只出现在 MoE 的 DPEngineCoreProc，dense 使用普通 EngineCoreProc 且未找到等价路径，因此必须保留版本和待验证限定。	MoE live publisher；dense path unverified	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] dense DP
为什么把 DPCoordinator 放进某个 EngineCore 进程是错误的？	我最初根据它汇总 waiting/running 的职责，把它放进 EngineCore 并算成 3 个进程。它实际上是所有 DP ranks 的对等汇总点，运行在独立进程中；API=1、DP=2、uni 时应有 4 个主要进程。	peer coordinator cannot belong to one rank	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] Coordinator 归属
为什么“ModelRunner 只处理模型 forward”过度简化？	我最初把它理解成一次 forward 调用。ModelRunner 还维护持久 batch、输入 tensor、物理 KV、block table、slot mapping、attention metadata，并负责图选择、模型执行、sampling 和设备侧状态更新。	ModelRunner = prepare + execute + sample + state	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] ModelRunner
固定 v0.26.0 中 GPU Worker 的实际类名是什么？“初始化归 Worker”边界在哪？	gpu_worker.py 中实际类名是 Worker，不是 GPUWorker。设备、rank、distributed/NCCL 等环境初始化归 Worker；ModelRunner 仍会初始化自身的 batch、tensor、KV 和 graph 状态。	file gpu_worker.py；class Worker	../log/2026-08-09-vllm-repository-and-process-architecture.md [纠错] 类名与初始化
```
