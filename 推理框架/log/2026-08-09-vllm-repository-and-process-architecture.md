# 学习记录 · 2026-08-09 — vLLM 仓库地图、进程拓扑与组件边界

> 来源：AI 会话 Codex:019fe49d（04:21–14:12 技术学习段）· 模块：推理框架 · 关联产出：[从仓库地图到进程与组件边界](../深入学习理解vLLM/1-Repository-and-Process-Architecture.md)
> 版本锚点：vLLM `v0.26.0 @ 568afb3a13806beb53bb2e6bd518269357b237c0`；以下源码判断只适用于该固定版本，另有明确说明时除外。
> legacy 边界：本次只把既有结构化记录适配到当前格式；沿用上方旧会话标识及当时记录的时间／语义范围，未重新提取源会话，也未新建或补造稳定消息边界、session ID 或 archive ID。
> 记录职责：只保留学习过程中的理解、纠错、高价值问题和遗留；稳定知识以关联文章为准，本记录不承担 Lesson 状态或 mastery。

## 学习过程

- [纠错] 最初怎样把 Scheduler 的一次决策拆成了两层？——场景：第一次凭经验画 request → kernel 链路。我说“KV Cache 等资源调度 → 模型运行调度”，把二者当成前后两个 scheduler；正确表述是 Scheduler 在同一次决策中选择请求和 token、分配逻辑 KV blocks，并产出 `SchedulerOutput`，物理 KV tensor、slot mapping 和实际执行再由 Worker/ModelRunner 等执行层处理。原因：资源选择与设备执行分别属于调度输出和执行落地，后者不是第二个 scheduler。
- [要点] 本轮完成了仓库地图压缩；稳定目录分类与“目录地图不等于运行时调用栈”的结论统一见关联文章 §学习过程 1。
- [要点] 六项“源码问题应从哪个目录开始”的定位题全部答对；完整定位表由关联文章 §学习过程 1 维护。
- [要点] `engine/core/executor/worker` 四项所有权映射全部答对；完整职责边界由关联文章 §学习过程 2 维护。
- [纠错] 为什么“多进程会让 Worker 多一些通信算子”缺少条件？——场景：讨论从单进程切到多进程时哪些目录变化最大。我说“对 worker 部分也会有变化，因为多进程并行会多一些通信算子”；正确表述是 `uni/mp/Ray` 回答组件放在哪里、如何调用，TP/PP 才回答模型怎样跨设备切分。只改变 Worker 的进程位置时，不必新增模型分片或跨 rank collective。原因：执行拓扑与模型并行是两个正交维度，不能由“多了进程”直接推出“多了 collective”。
- [纠错] “单纯增加进程不会影响 Worker”为什么又过于绝对？——场景：理解 `uni/mp` 与 TP 不同后，我把结论推得太远。单卡切到 `mp` 虽不改变模型分片和 collective，却会改变 Worker 的进程位置、Executor↔Worker IPC，以及 CUDA context、模型加载和资源生命周期的归属；更准确的是“不改变 Worker 的模型并行语义”。原因：模型并行语义不变，不等于进程位置、通信边界与资源生命周期不变。
- [纠错] 内部 DP 为什么不是“把一个 EngineCore 变成多进程”？——场景：我提出“把 EngineCore 变成多进程，由一个 API 给多个后台 engine 分流”。更准确的说法是启动多个独立 EngineCore，每个拥有自己的 Scheduler、请求队列、逻辑 KV 状态和模型副本，再由 API 进程中的 `DPLBAsyncMPClient` 为新请求选择目标。原因：各 DP rank 拥有独立的调度与模型状态，前端是在多个状态所有者之间路由新请求，而不是把一个状态所有者拆成多个进程。
- [要点] “为什么执行中的请求不能直接迁移”这一题中，我先正确指出原 EngineCore 持有调度与 KV 相关状态；补验随后揭示我的状态清单仍不完整。完整状态面与迁移边界见关联文章 §学习过程 4。
- [转折] AI 最初统一表述“每个 EngineCore 在 step 前后上报 waiting/running”；源码核对后，固定 `v0.26.0` 中实时 `_maybe_publish_request_counts()` 链只出现在 MoE 使用的 `DPEngineCoreProc`，dense DP 的普通 `EngineCoreProc` 未找到等价发布链。这个证据把理解从“两条路径都有相同实时反馈”收窄为“当前只证明 MoE 路径存在该实现”，不能继续外推。
- [要点] DP 多 EngineCore 场景的五项状态所有权映射全部答对；完整映射由关联文章 §学习过程 5 维护。
- [纠错] `DPCoordinator` 位于哪个进程？——场景：在 `API=1, DP=2, TP=1, backend=uni` 的进程题中，我说“DPCoordinator 在 EngineCore 进程上”，并据此算出 3 个进程。正确答案是它作为所有 DP ranks 的对等汇总点运行在独立进程中，因此共有 1 个 API、1 个 Coordinator 和 2 个 EngineCore，共 4 个主要进程。原因：Coordinator 是跨 DP ranks 的对等汇总角色，固定版本由独立进程承载，不隶属于某一个 EngineCore。
- [要点] `DP=2` 切到 `backend=mp` 的进程数补验回答正确；推导与组件归属由关联文章 §学习过程 5 维护。
- [高价值问题] 我追问“ModelRunner 是否只负责调用模型 forward”，把关注点从一次调用扩展到 Worker 与 ModelRunner 的资源生命周期和设备热路径所有权；完整职责边界见关联文章 §学习过程 6。
- [要点] MRV1→MRV2 补验中的五项职责判断全部正确；完整差异与不变项由关联文章 §学习过程 6 维护。
- [转折] AI 讲解时使用了“`GPUWorker` 外壳”这一概念简称；源码核对后，固定 `v0.26.0` 的 `gpu_worker.py` 中实际类名是 `Worker`。同时，“初始化归 Worker”只覆盖 device、rank、distributed/NCCL 等环境，ModelRunner 仍初始化并持有自己的 batch、tensor、KV 和 graph 状态。这个核对把概念称呼收窄为版本中的实际符号与所有权边界。

## 遗留

- [遗留] 对比最新 `main`、检索已有 issue/PR、确认 maintainer 预期并构造 dense `DP=2` 最小复现，判断 internal DP 实时计数差异是实现遗漏、文档未说明限制，还是已经在新版本修复。（已挂账：关联文章 §实践、`EP-PD自研芯片适配设计与验证包.md` §6.1）
- [遗留] 最初的自研芯片五层适配猜想及 `adapter/core patch/替换` 分类尚未完成理解验收，需在 Pass C–E 后重新作答，不能把导师预核对当作已掌握结论。（已挂账：关联文章 §后续预告、`计划/学习断点.md`）
- [遗留] DP/TP 多卡进程图、请求迁移和 dense 统计链当前只有固定源码证据，没有本地多卡运行验证。（已挂账：关联文章 §实践）
