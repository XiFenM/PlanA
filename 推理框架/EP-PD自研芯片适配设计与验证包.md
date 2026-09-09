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
- **当前 stage**：`synthesis`。固定提交 `568afb3` 的 Pass A–E、KV 账本，以及整段独立文字复述、两轮变式与必要局部补差均已有通过证据；oral-F1／oral-F2／oral-F3 全部关闭，不再追加同类检查。根据用户 2026-09-08 确认的[口头验收新安排](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#53-每周统一验收门)，口头要求移交 W4 及后续 Mock，不再作为 W1 未完成项，也不记为已通过。页对齐与插件旁支保持原证据边界；W1 其余任务及整个 Lesson 尚未关闭，final mastery 未写入。
- **授权边界**：前台仍为 W1，下述 revision 1 的文字练习已经收口。用户当前只授权登记周末待做实践，不启动 W2–W4、新实践、环境安装、模型／tokenizer 下载或新的实现文件。
- **待做实践引用**：[W1-P1：运行路径选择与最小输出契约验证](#w1-p1-runtime-output-validation)。该项保持未完成，延期不取消 W1 原有证据要求；本轮可以先处理非实践材料，不为此重复已通过的概念题。
- **历史契约边界**：下述已完成练习的 revision、digest、原约定和文字证据保持不变；本次只调整后续口头验收的所属周次，不追溯改写历史，也不据此启动 W4。

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

旧记录没有逐目标保存用户确认的 `conceptual / practical / empirical` required 值。下述已接受练习只确认概念与独立表达的验收范围，不要求编码或设备实证；不据此改写整个 Lesson 的最终维度要求，进入 Lesson mastery gate 前仍须确认。当前没有 `final_mastery`。

- **核心工件**：本文件 [§0–§6](#0-范围版本与披露边界)。
- **最近结构化 evidence**：[Pass C-1 学习者流程图](深入学习理解vLLM/request_journey.drawio)。
- **Checkpoint 引用**：[唯一学习断点](../计划/学习断点.md)。

### 已接受练习：vLLM 整段独立讲解

- **练习 ID／revision**：`plana-jd-w1-vllm-oral-20260908`／`1`。
- **digest**：`sha256:22e19b50414d9f410b2dd1dbf22450f23b3b49ecff7f4dd6bf5c9d4604f3fe19`。
- **接受事件**：[`plana-jd-w1-20260908-oral-review`](#plana-jd-w1-20260908-oral-review)，绑定上述 revision 与 digest。用户在完整约定展示后直接提交讲解，按前轮“直接开始即接受”的约定生效。
- **本次维度**：补充三个既有目标的概念与独立表达证据；不要求独立编码或设备实证，不代替整个 Lesson 的最终维度确认或 W1 验收。
- **规范化契约**：以下只含 digest 所覆盖字段；计算时递归按 key 排序、保留数组顺序、UTF-8、JSON 紧凑分隔符。它是前轮公开约定的持久投影，不新增通过条件。

```json
{
  "id": "plana-jd-w1-vllm-oral-20260908",
  "targets": [
    {"objective_id":"w1-o1-repository-process-map","missing_dimensions":["conceptual"],"evidence_gap":"已有分段检查；本次补充独立整段表达中的进程与状态归属证据。"},
    {"objective_id":"w1-o2-request-lifecycle","missing_dimensions":["conceptual"],"evidence_gap":"独立组织单请求完整生命周期，并在两轮追问中解释关键边界。"},
    {"objective_id":"w1-o3-extension-boundaries","missing_dimensions":["conceptual"],"evidence_gap":"在本次讲解或已学过的边界变式中解释职责与接口，不把局部题通过外推为整段表达已通过。"}
  ],
  "task": "固定 vLLM v0.26.0@568afb3a13806beb53bb2e6bd518269357b237c0、V1/MRV1、一个API Server、DP=TP=PP=1、backend=uni；模型已加载、KV pool已初始化。讲解纯文本Chat Completion从接收至返回和资源回收；stream=true、无前缀命中、无投机解码，以max_tokens正常结束。覆盖请求与参数转换、组件职责、调度与KV、prefill/decode、ModelRunner输入与Attention、采样返回和清理；组织顺序由学习者决定。",
  "deliverables": [
    {"artifact":"dialogue:plana-jd-w1-vllm-oral-20260908","outcome":"学习者在对话中提交完整讲解并回答两轮追问。目标约15分钟、先约2分钟全景，不机械卡时；允许只看题设和范围清单，不查源码、旧图或笔记。文字提交只证明独立文字复述；实际口述时长须另有证据，自报时长标为自报。"}
  ],
  "acceptance": [
    {"id":"A1","criterion":"主链完整，没有需要导师补出的关键断点。","evidence_method":"独立讲解内容Review，非代码练习，不使用expected red。"},
    {"id":"A2","criterion":"进程、状态归属和跨边界载荷没有重大混淆。","evidence_method":"固定源码核验与讲解Review；不要求背源码行号，辅助函数名称小误记不单独否决。"},
    {"id":"A3","criterion":"区分调度与实际计算、输入token与新采样token、输出结束与各层资源清理。","evidence_method":"讲解和边界追问；仅修复实际差距，不要求重复已通过内容。"},
    {"id":"A4","criterion":"讲解后独立完成两轮已学过范围内的变式追问，涉及取消/抢占、batch/KV映射或适配边界。","evidence_method":"导师先听完，再追问；可自然求助，实质提示只影响对应范围，需一次无提示同构变式恢复独立证据。"}
  ],
  "scope": {"learner_owned":[{"artifact":"dialogue:plana-jd-w1-vllm-oral-20260908","operations":["create","modify"]}],"agent_owned":[{"artifact":"推理框架/EP-PD自研芯片适配设计与验证包.md#lesson-plana-jd-w1-vllm-execution-boundaries","operations":["read","modify","record"]},{"artifact":"计划/学习断点.md","operations":["read","modify","record"]}],"read_only":[{"artifact":"推理框架/references/vllm（固定提交568afb3a13806beb53bb2e6bd518269357b237c0）","operations":["read"]},{"artifact":"推理框架/深入学习理解vLLM/request_journey.drawio","operations":["read"]},{"artifact":"推理框架/深入学习理解vLLM/process_component_graph.drawio","operations":["read"]},{"artifact":"dialogue:本课程已引用的学习笔记","operations":["read"]}],"excluded":[{"artifact":"简历、项目稿、Program和其他未列明文件的修改；新文章、过程日志、卡片和原始对话归档","operations":[]},{"artifact":"启动初始化细节、Kernel内部算法、多卡通信实现、独立编码和设备实验；W1整体关闭与后续Lesson启动","operations":[]}]},
  "optional": []
}
```

#### 当前 Review

- **提交**：`dialogue:plana-jd-w1-vllm-oral-20260908`，2026-09-08 用户完整文字讲解；未改写原文，未提供口述时长，不计为已完成 15 分钟口头验收。
- **已有证据**：能够独立串起双进程、先注册后提交、waiting/running 资源调度、未完成 prefill 不对外输出、前后端输出链及正常结束时归还 KV 引用。第一轮补出了 Executor／Worker／ModelRunner 和 Scheduler 回写职责，并明确物理 KV pool 不在每次 forward 重新申请；第二轮在非流式提前命中 stop string 的新条件下正确判断可以返回最终响应、无需等待第 100 个输出 token，对外原因为 stop。
- **当前判断**：本次 A1–A4 在独立文字表达与变式范围内通过。R 结束而 S 继续的局部快照中，学习者正确说明最终输出仍可从 Collector 消费、InputBatch 移除 R 而保留 S 并维护映射，以及不能再次减少仍由 S 引用的 block 7 的计数。三项 findings 均关闭，停止补测；不把本次结论写成 15 分钟口头验收或整个 W1 通过。
- **帮助边界／material assistance**：导师给出过 Worker 初始化／每步执行、Runner 输入与映射维护、FINAL_ONLY 前端过滤，以及 KV 回收归属和前端消费者生命周期的局部讲解，并精确补充 ABORT 名称；影响 oral-F1／oral-F2／oral-F3 对应的 A2／A3，未代写核心讲解。oral-F2 已用第二轮非流式停止变式恢复本题范围的独立证据；oral-F1／oral-F3 已用 R／S 共享块与未消费最终输出的快照变式恢复对应证据，不抹去此前提示事实。
- **非阻塞表达建议**：开启 chunked prefill 只允许按预算拆分，不保证每个 prompt 都分为多个 chunk；最后一个 prefill chunk 与首个有效输出 token 的关系已有先前学习证据，不为本轮省略再加门槛。Runner 清理还包含自身 cached request state；此处作完整性补充。辅助函数／枚举名称及 `token budge` 等笔误不单独否决；grammar 为用户主动扩展，不追加为必考范围。

<a id="plana-jd-w1-oral-findings"></a>
#### 当前 findings

| ID | 映射 | 严重度 | owner | 状态 | Evidence | 下一动作 |
|---|---|---|---|---|---|---|
| `oral-F1` | A1、A2、A3 | major | learner | closed | 初始混淆物理池分配、Runner 状态与调度侧引用回收；2026-09-08 局部变式中，学习者正确说明从 InputBatch 移除 R、保留 S 并维护映射，拒绝再次扣减 block 7，指出会错误从 1 归零而归还。结合已补齐的执行闭环与 pool 预分配证据，本题范围复核通过。[Scheduler 回收](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L2224-L2239)、[Runner 更新](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_model_runner.py#L1179-L1193) | — |
| `oral-F2` | A2、A3 | major | learner | closed | 初始把 FINAL_ONLY 解释为 Core 完整生成后才发送；经前端过滤位置提示后，第二轮在 stream=false、前端提前命中 stop string、Core finished=false 的条件下，独立判断可最终返回且无需等待第 100 个 token，对外为 stop。本题范围的迁移证据通过，不外推其他输出路径。[前端输出过滤](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L273-L287) | — |
| `oral-F3` | A2、A3 | major | learner | closed | 初始把 RequestState 与 Collector 的清理绑定到 generate 消费之后；2026-09-08 局部变式给出 RequestState 已注销、最终输出仍在 Collector 的快照，学习者正确判断 generate 仍能取出并 yield 最终结果，消费者生命周期边界复核通过。终止控制方向已答对，ABORT 名称为导师精确补充，不以枚举背诵另设门。[输出处理与请求清理](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L676-L717) | — |

### Session event 索引

#### `plana-jd-w1-20260809-pass-ab`

- **日期**：2026-08-09
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：vLLM 仓库地图、进程边界、DP 路由与 Worker/ModelRunner 职责边界。
- **已完成动作**：完成 Pass A–B 的学习者问答验收并收束结果材料。
- **Evidence 引用**：[结果文章](深入学习理解vLLM/1-Repository-and-Process-Architecture.md)、[结构化过程记录](log/2026-08-09-vllm-repository-and-process-architecture.md)、[技术记忆卡](cards/vllm-repository-and-process-architecture.md)。
- **开放问题**：Pass C 的请求生命周期尚无学习者回答证据；精确恢复动作只见 Checkpoint。

#### `plana-jd-w1-20260904-pass-c1`

- **日期**：2026-09-04
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：普通 chat 请求从 OpenAI 协议对象到 `EngineCoreRequest` 的前端 lowering、注册顺序、IPC 边界与简化输出返回链。
- **已完成动作**：完成 Pass A–B 保持度复习；完成 Pass C-1 讲解、两轮学习者流程图 Review 和边界纠正。
- **Evidence 引用**：[学习者 Draw.io 流程图](深入学习理解vLLM/request_journey.drawio)、[导出 PNG](深入学习理解vLLM/request_journey.png)。
- **开放问题**：EngineCore 接收 ADD 后的请求转换、Scheduler admission 与后续 token 生命周期尚未开始；精确恢复动作只见 Checkpoint。

#### `plana-jd-w1-20260904-pass-c2-intake`

- **日期**：2026-09-04
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：`ADD` 请求在 EngineCore 内转换为可变 Request、登记到 `requests` 与 waiting／`skipped_waiting`，以及 structured-output grammar 的编译等待与逐 token 约束。
- **已完成动作**：通过普通请求 waiting 边界题与 structured-output 场景检查，能够区分请求状态、等待队列、Grammar bitmask 和事实语义边界。
- **开放问题**：waiting 请求如何通过 token budget 与 KV slots 检查进入 `RUNNING` 尚未验收；精确恢复动作只见 Checkpoint。

#### `plana-jd-w1-20260906-pass-c-synthesis`

- **日期**：2026-09-06
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：前端文本判停、Core abort 与 Scheduler preemption 的状态对照，以及普通流式 chat 请求从输入到正常结束的全链路综合表达。
- **已完成动作**：通过 `STOP / FINISHED_ABORTED / PREEMPTED` 对照与全链路复述；经补正区分 IPC 解码与内部 Request 构造，并通过跨 step 变式说明计算载荷与结束通知可以共存、最终输出不等待设备侧状态清理。补充明确普通结束时 KV blocks 已由 Scheduler 归还；导师完成 [12 文件源码索引](#pass-c-source-map)。
- **源码定位 evidence**：学习者准确定位 `AsyncLLM._add_request()` 的先注册后提交、`Scheduler._update_after_schedule()` 在 `schedule()` 返回前推进计算计数，以及 `OutputProcessor.process_outputs()` 返回待取消列表后由 `AsyncLLM._run_output_handler()` 中的 `output_handler()` 执行 `await engine_core.abort_requests_async(...)`；补正了前端已判停且 Core 未判停的外层条件。Pass C 验收完成。
- **后续边界**：Pass D 的执行侧状态、输入 tensor 构造与模型调用尚未验收；本记录只裁决 Pass C，不写整个 Lesson 的 final mastery。

#### `plana-jd-w1-20260906-pass-d-input-preparation`

- **日期**：2026-09-06
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：固定提交 `568afb3` 的 MRV1 `_update_states()`、`_prepare_inputs()` 与 `BlockTable.compute_slot_mapping()`。
- **已完成动作**：通过缓存请求与本步 batch 成员区分、抢占恢复时替换块表与普通继续时追加块表的检查；独立推导有效 `input_ids`、`positions`、`query_start_loc` 与 Token 总数；正确解释块映射变化不影响逻辑 Token 位置。槽位变式仅漏写另一请求的不变项，补正完整 batch 后通过。
- **证据边界**：本段为源码与纸面推导证据；未执行设备实验，未声称已掌握整个 Attention backend 或模型 forward。
- **开放问题**：Attention metadata 的 Query／KV 长度、因果可见范围及后续模型执行尚待验收。

#### `plana-jd-w1-20260906-pass-d-forward-output`

- **日期**：2026-09-06
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：MRV1 Attention metadata 与 ForwardContext、统一 Attention custom op 到 backend 的边界、隐藏状态选行与采样结果返回。
- **已完成动作**：通过 Query／KV 长度和因果隔离检查；解释静态模型资源与本步 metadata 的复用／更新；区分统一 op、具体 backend 与设备 kernel，并说明 KV 更新依赖的编译作用；正确推导生成 logits 的行号、输入与输出 Token 数，以及 `execute_model()` 返回 `None` 后经 `sample_tokens()` 取得结果。
- **开放问题**：控制面／执行面契约表与请求重排后的跨字段对应关系尚待综合验收；未据局部检查推断整个 Lesson 已完成。

#### `plana-jd-w1-20260907-pass-d-synthesis`

- **日期**：2026-09-07
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：控制面／执行面接口契约，以及同一步请求重排后的输入、Query 分段和 KV 映射。
- **已完成动作**：学习者提交四条边界的契约表，职责方向正确；独立给出正确的重排后 `input_ids`、`positions`、`query_start_loc` 和完整 `slot_mapping`。导师补充 Q/K/V、物理 KV tensor、显式输入与 ForwardContext、Scheduler 结果回写的职责。
- **验收结果**：通过。学习者在错误变式中正确指出新 K/V 写入槽位 36，但 D 的上下文被错误对应到第一行 `[7,6]`，能够区分正确写入与错误读取；`d3` 为题中 `d4` 的笔误。结合前面的独立重排计算，Pass D 综合验收完成。
- **Evidence 引用**：[控制面／执行面契约](#pass-d-execution-contract)。
- **后续边界**：平台扩展与适配层选择进入 Pass E，尚未验收；本段不写整个 Lesson 的 final mastery。

#### `plana-jd-w1-20260907-pass-e-platform-worker-ops`

- **日期**：2026-09-07
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：Platform 插件选择、Worker／Runner 的执行与资源契约、KV 物理布局、CustomOp OOT 注册与原生路径，以及设备 communicator 的 TP 分组语义。
- **已完成动作**：正确定位 `check_and_update_config()`／`worker_cls`；解释布局差异不必改变调度语义、页大小低报会高估容量，并补正为预算与真实布局不一致；区分注册底层 PyTorch 算子与通过 `register_oot`／`forward_oot` 接入模型路径，明确原生 PyTorch 组合不代表 CPU 执行。
- **通信检查 evidence**：正确推导两个 TP 子组的结果为 3、3、30、30，将错误的全 world 求和归因于分组契约；指出 TP=1 旁路和单组测试可能遗漏问题，补准为通信组恰好等于 world 时错误可能被掩盖。此为纸面推导，未声称完成多卡实测。
- **综合表达 evidence**：学习者正确对应 Worker／Runner、KV 布局、OOT 算子与 communicator 接入点，并指出题设差异不构成修改 EngineCore／Scheduler 的充分理由；识别私自回收仍 RUNNING 请求 KV 的契约破坏。导师补齐算子数学／tensor 契约及完整抢占生命周期，整理为 [六层适配矩阵](#pass-e-adaptation-matrix)。
- **最终复核结果**：通过。学习者将页大小误报归因于插件规格实现，将准确预算下的 KV pool 耗尽交由已有抢占／恢复机制处理；明确上述情况都不足以支持 core patch，需进一步证明现有扩展接口无法表达所需能力。Pass E 综合验收完成。
- **阶段证据边界**：至此 Pass A–E 的源码教学与对话验收完成；不标记整个 W1 完成，不声称具备本轮未进行的设备运行、实现或性能实证，也不将本段记为整个 Lesson 的 closure。

#### `plana-jd-w1-20260907-kv-unit-and-layout`

- **日期**：2026-09-07
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：单层 KV 的 Token／element／byte／block 计账，以及页跨度、搬运粒度、插件布局和页大小接口的区别。
- **已完成动作**：学习者正确计算 35 Token 对应的 3 blocks、105 KiB 有效数据、39 KiB 未用槽位容量与 48 KiB 页 padding，核对总占用为 192 KiB；结合用户提供的插件快照区分逻辑 tensor 大小与存储预算，并补充了用户向同事求证的 block size 设计理由。
- **Evidence 引用**：[按本轮授权保存的结构化学习记录](log/2026-09-07-kv-padding-block-size.md)。插件快照与同事转述只支持该记录标明的范围，不替代课程固定源码或设备实验。
- **开放问题**：在相同全注意力层和无共享假设下，将单层账本扩展到全模型及多个请求的计账尚待检查。

#### `plana-jd-w1-20260907-kv-ledger-synthesis`

- **日期**：2026-09-07
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：全模型／多请求 KV 计账、实际前缀共享与引用计数、零引用缓存块的可分配性、逐步增长的块需求，以及 Prefix Cache 与 PagedAttention 的职责区别。
- **已完成动作**：通过按请求分别取整、共享块按不同 pool block ID 去重、请求结束后的归还与保留、空闲块数为零但末块仍有槽位的检查；结合源码讲解区分前缀查询命中与正式引用，并澄清链式 hash、`cache_salt` 的复用边界和 decode 输入／新采样 token 的先后关系。
- **综合验收 evidence**：在 TP=1、32 个同规格全注意力层、每块 16 Token、每层页跨度 64 KiB、两请求各需保存 32 Token KV 且首块实际共享的教学题中，学习者独立算出开启／关闭 Prefix Cache 分别引用 3／4 个不同 pool block ID，占用 6／8 MiB；正确解释物理 pool 均为 20 MiB，不意味着前缀共享没有节省池内容量。综合检查通过，无需补测。
- **导师补充**：预分配按确定的 KV 预算与配置进行，并不保证满足所有未来请求；此措辞补充不记为学习者独立推导。空闲块类别的最终拆分还取决于出队顺序，未将原题缺失的顺序条件记为学习者错误。
- **源码锚点**：固定提交的 [BlockPool 引用与分配](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/block_pool.py#L647-L740)、[容量检查后建立引用](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/kv_cache_manager.py#L449-L486)。
- **证据边界**：本段为对话、纸面推导与源码核验证据，不代表设备运行、性能实证或整个 W1／Lesson 完成；未写入 final mastery，未新增文章、过程日志、卡片或学习时长。

#### `plana-jd-w1-20260908-oral-review`

- **日期**：2026-09-08
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：既定场景下单请求全生命周期的独立整段讲解与正式 Review。
- **已完成动作**：用户接受练习 `plana-jd-w1-vllm-oral-20260908` revision 1（digest `sha256:22e19b50414d9f410b2dd1dbf22450f23b3b49ecff7f4dd6bf5c9d4604f3fe19`），完成完整文字讲解、两轮变式与一个必要局部快照补差。非流式停止、前端消费者存续和 Runner／KV 所有权边界经迁移复核通过，oral-F1／oral-F2／oral-F3 全部关闭，本次 A1–A4 收口。
- **Evidence 引用**：本 Lesson 的“已接受练习”与[当前 findings](#plana-jd-w1-oral-findings)；核心提交保留在对话中，不另存原始全文。
- **marker**：`practice-closed`。
- **后续边界**：仅完成本次文字复述练习；未提供口述时长或设备实测证据，未完成整个 W1，不写 final mastery，也不自动启动下一项练习。

#### `plana-jd-w1-20260908-oral-deferral`

- **日期**：2026-09-08
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：用户明确调整正式口头验收的时间安排。
- **已完成动作**：按用户指令，将早期技术周的口头验收移交[冲刺计划 §5.3](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#53-每周统一验收门)与 W4 及后续 Mock；保留已完成文字复述、追问与源码证据，旧练习 revision 1 的规范化内容未变。
- **证据边界**：移交表示不再阻塞 W1 技术验收，不表示口头已通过、整个 W1 完成或后续 Lesson 已获启动授权；未执行运行路径验证或新测试。

#### `plana-jd-w1-20260908-practice-backlog`

- **日期**：2026-09-08
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：用户将运行路径与最小验证安排为周末集中处理的待做实践。
- **已完成动作**：在既有验证包中登记 [W1-P1](#w1-p1-runtime-output-validation) 的范围、候选验证点、材料与启动边界；更新恢复指针，当前不自动进入实践。
- **证据边界**：这只是待办登记，不是正式实践契约接受、测试执行或通过记录，不修改既有文字练习结果，也不标记 W1 完成。

#### `plana-jd-w1-20260909-kv-page-spec-review`

- **日期**：2026-09-09
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`
- **覆盖范围**：按用户请求快速复习上游 KV 页尾 padding 的规格配置、物理页字节数、原始存储块数与 Tensor stride，并准备通用场景卡片。
- **已完成动作**：在单层单组、普通未量化、B=16、本地 KV heads=8、K/V head 维度均为 96、BF16、仅页尾 padding、backend 真正支持对应 stride 的题设下，学习者正确回答 128 KiB 页跨度和 256 KiB 原始 buffer 对应 2 块、65536 个 BF16 元素的 block stride，逻辑 head_size 保持 96。
- **接口补充**：针对学习者的设置入口追问，说明上游 `page_size_padded` 是补齐后整页总字节数的配置字段，`page_size_bytes` 是无 setter 的派生属性；冻结规格通过构造参数或 `replace` 生成。普通页尾 padding view 分支依赖该配置是否非空，并要求 num-blocks-first 布局及 kernel 的真实 stride 支持。原始 int8 buffer 的字节容量与逻辑 view 的元素数分别使用。
- **一手来源锚点**：固定 `vLLM v0.26.0 @ 568afb3` 的 [AttentionSpec 字段与属性](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/kv_cache_interface.py#L175-L201)、[页尾 padding view](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu/attn_utils.py#L200-L253)、[MRV1 原始分配与块数解释](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_model_runner.py#L7238-L7344)、[容量规划](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/kv_cache_utils.py#L1344-L1419)。具体实现以这些固定源码为准。
- **证据边界**：本段记录轻量变式作答和接口讲解，不声称完成 kernel 适配、设备实测或整个 W1；原周末实践安排不变。自研 vllm-cl 的历史双字段方案归入工程实践案例，不作为上游接口限制或本组通用卡片的事实依据。

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

下表是本 Lesson 的**教学与历史 evidence 基线**。它固定本 Lesson 各 Pass 及相关永久链接所依据的 revision，不随父仓库当前 gitlink 更新。

| 角色 | Tag | Commit | 用途 |
|---|---|---|---|
| vLLM 主读 | [`v0.26.0`](https://github.com/vllm-project/vllm/releases/tag/v0.26.0) | [`568afb3`](https://github.com/vllm-project/vllm/commit/568afb3a13806beb53bb2e6bd518269357b237c0) | W1–W3 的执行链、EP/PD 与测试事实源 |
| PyTorch 兼容基线 | [`v2.11.0`](https://github.com/pytorch/pytorch/releases/tag/v2.11.0) | [`70d99e9`](https://github.com/pytorch/pytorch/commit/70d99e9) | vLLM v0.26.0 明确固定的默认 CUDA/CPU 依赖；2.13 只作增量阅读，不混入运行基线 |
| SGLang 窄对照 | [`v0.5.17`](https://github.com/sgl-project/sglang/releases/tag/v0.5.17) | [`2948168`](https://github.com/sgl-project/sglang/commit/29481685462732237d80d86076d6563e1f658102) | ATOM/MoE、PD 与控制面边界对照 |
| MORI 参考数据面 | [`v1.2.2`](https://github.com/ROCm/mori/releases/tag/v1.2.2) | [`dafdcfc`](https://github.com/ROCm/mori/commit/dafdcfcf1e27b0c981b90903ab198b90d29e6867) | SHMEM/IR、EP、IO、UMBP 契约审查 |

> 这些版本只建立可复查的源码基线，不代表四个组件已经在同一环境完成组合验证。若后续使用本地部署版本或更新快照，另建对照列，不覆盖本表。

#### 当前本地 comparison baseline（2026-08-30）

| 组件 | 本地路径 | 当前父仓库 Gitlink | 状态 |
|---|---|---|---|
| vLLM | [`references/vllm`](references/vllm) | `1dc464d42681d22f38caf1fdc1eb632dc4421c45` | 浅克隆、detached HEAD、上游 `main` 比较快照；不替代教学基线 |
| SGLang | [`references/sglang`](references/sglang) | `78fa921189e3a66c7278733940c60a1e6fe6e467` | 浅克隆、detached HEAD、上游 `main` 比较快照；不替代教学基线 |
| PyTorch | [`../PyTorch/references/pytorch`](../PyTorch/references/pytorch) | `460948b96a67002b7257ac4f3d6a192f70d61d27` | 浅克隆、detached HEAD、上游 `main` 比较快照；不替代教学基线 |

三项由仓库根目录 [`.gitmodules`](../.gitmodules) 登记，并建议后续 clone 时保持 shallow。当前快照只用于 old → new drift check；任何新增结论都必须同时标明 revision，不得混读后静默改写历史 evidence。当前父仓库 revision 的 depth-1 clone 不保证包含上表的旧教学 tag，通常通过固定 commit 链接复查，需要本地旧树时再按需 shallow fetch。MORI 当前仍使用固定远程源码链接，不在本轮本地 clone 范围内。

### 0.3 计划预算与实际工时边界

- Program 的计划预算与节奏只见[八周证据冲刺计划 §5](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#5-时间预算与周节奏)。
- 实际学习工时只按真实归属写入对应模块 `进度.md`；本 Lesson ledger、Session event 和 Checkpoint 不复制工时。
- 2026-08-09 的启动日期与返回 capsule 由临时 Program 保存；本文件不把计划可用时长冒充实际投入。

### 0.4 环境与能力 preflight

| 槽位 | 可用且获准 | 可公开粒度 | 当前处理 |
|---|---|---|---|
| 公开源码与官方文档 | 是 | 公开链接、commit、文件、类、函数 | W1 使用固定教学基线；当前 `main` 只作 revision 标注的漂移核对 |
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

> 下列固定源码预核对已用于 2026-09-04 的教学与两轮流程图 Review；Pass C-1 已形成学习者 evidence，但不代表 Pass C 后续节点已经完成。

本节只追请求进入 EngineCore 之前的前端路径，不提前展开 Scheduler 或模型执行：

`POST /v1/chat/completions` → `OpenAIServingChat._create_chat_completion()` → `render_chat_request()` → `EngineInput` + `SamplingParams` → `AsyncLLM.generate()/add_request()` → `InputProcessor.process_inputs()` → `EngineCoreRequest` → `EngineCoreClient.add_request_async()`。

- OpenAI 协议层：`messages`、tools、chat template、HTTP headers 与 `stream` 等先由 API serving 层解释；chat 内容被 render/tokenize 为 `EngineInput`，生成参数被归一化为 `SamplingParams`。
- EngineCore 输入契约：`InputProcessor` 生成的 `EngineCoreRequest` 携带 request id、prompt token IDs/embeds、多模态 features、sampling/pooling params、到达时间、LoRA、cache salt、priority、DP rank 与 trace headers；它不携带 FastAPI `Request` 或原始 OpenAI `messages`。
- 输出竞态防护：`AsyncLLM` 先在本进程创建 `RequestOutputCollector`，再把请求注册到 `OutputProcessor`，最后才通过 client 把 `EngineCoreRequest` 发往独立 EngineCore 进程。这样 EngineCore 即使很快返回，前端也已有接收该 request id 输出的位置。
- 流式边界：`request.stream` 一方面决定 API 层最终选择 SSE generator 还是一次性 JSON response，另一方面会被投影为 `SamplingParams.output_kind`（`DELTA` 或 `FINAL_ONLY`）并进入核心；但原始 `stream` 字段、FastAPI `Request` 和 HTTP 连接本身都留在前端。
- 设计动机：EngineCore 不理解 OpenAI chat schema、chat template 或 HTTP 生命周期，同一个 token 级核心因此可以复用于 chat、completion、离线调用等不同入口。
- 证据：[`/v1/chat/completions` 路由](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/api_router.py#L40-L61)；[chat render、参数归一化与 `AsyncLLM.generate`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/serving.py#L255-L384)；[`AsyncLLM` 先注册 collector 再跨进程发送](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L333-L412)；[`InputProcessor` 构造 `EngineCoreRequest`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/input_processor.py#L242-L385)。
- 验收结果（2026-09-04）：通过。学习者流程图正确区分 `ChatCompletionRequest`、`EngineInput`、`SamplingParams`、`EngineCoreRequest`、前端 Collector 与 SSE，并明确只有核心请求载荷跨 IPC；request ID 随机化按学习者选择不进入主图。客户端断连属于此前未教学的补充控制路径，不作为本节点通过条件。

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

<a id="pass-d-execution-contract"></a>
#### Pass D · 控制面／执行面契约

适用范围：`v0.26.0 @ 568afb3`，MRV1 普通单卡生成路径。以下由学习者综合表经源码 Review 补齐；验收证据见 [Pass D 综合表达记录](#plana-jd-w1-20260907-pass-d-synthesis)。

| 边界 | 主要传递内容 | 接收方职责 |
|---|---|---|
| Scheduler → Executor／Worker／ModelRunner | `SchedulerOutput`：新／已有请求、本步 Token 数、block IDs，以及结束／恢复等状态信息 | Executor 下发任务；Worker 处理设备／rank 外层调用；ModelRunner 更新本地缓存和 InputBatch，准备有效输入与 metadata |
| ModelRunner → 模型 | 显式传入 `input_ids`、`positions` 等 tensor；通过本次 `ForwardContext` 提供 Attention metadata 和 slot mapping | 执行模型前向，产生隐藏状态；本步 metadata 与可复用的模型层、物理 KV tensor 保持对应 |
| 通用 Attention → 具体 backend | Q/K/V、物理 KV tensor、metadata、输出缓冲；独立 KV 更新入口还接收 slot mapping | 按 backend 契约完成 KV 写入与 Attention 计算；两者可在分开的接口内实现，但要保持先写后读依赖 |
| 执行层 → EngineCore／Scheduler | `ModelRunnerOutput`：请求映射、有效采样 Token IDs、logprobs 等 | Scheduler 回写 Token 历史、检查停止条件并回收资源，组织 `EngineCoreOutputs` 交给前端处理 |

- **重排不变量**：有效输入的 `input_ids`、`positions`、`slot_mapping` 按 Token 一一对应；`query_start_loc` 按本步请求片段重新累计，block table 的行和请求级 metadata 跟随 batch 顺序。请求自己的 block ID 列表无需因单纯 batch 重排而改变。
- **读写区别**：slot mapping 指定新 K/V 的写入槽位，block table 定位请求上下文。一个映射正确或 tensor shape 合法，都不能替代跨字段的一致性。
- **采样返回**：模型前向返回隐藏状态，普通生成路径选取每个请求本步片段的最后一行计算 logits；Partial Prefill 的内部采样结果会被过滤。MRV1 `execute_model()` 返回 `None` 时，以 `sample_tokens()` 消费中间状态并取得最终执行输出。
- **固定源码入口**：[`_update_states / _prepare_inputs`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_model_runner.py#L1169)、[`get_attention_context / unified_attention_with_output`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/model_executor/layers/attention/attention.py#L731)、[`EngineCore.step`](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L576)。

<a id="pass-c-source-map"></a>
### 2.2 8–12 文件 source map

以下 12 个文件构成 Pass C 的教学定位索引，已按 `v0.26.0 @ 568afb3` 核验；索引由导师准备，学习者源码定位的验收 evidence 见 [Lesson 会话记录](#plana-jd-w1-20260906-pass-c-synthesis)。路径相对 `vllm/`，链接均指向固定提交。本地当前 checkout 仅作比较基线。

| 文件 | 优先定位的类／函数 | 在请求链中回答的问题 |
|---|---|---|
| [entrypoints/openai/chat_completion/serving.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/serving.py#L255) | `render_chat_request()`、`_create_chat_completion()`、`chat_completion_stream_generator()` | 组织 chat 渲染、调用采样参数转换和 `generate()`，按 `stream` 选择 SSE 或完整响应。 |
| [v1/engine/async_llm.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L280) | `add_request()`、`_add_request()`、`generate()`、`_run_output_handler()` | 创建 Collector、先注册请求再跨 IPC 提交；接收 Core 输出、消费 Collector，并转发前端 stop string 引发的 abort。 |
| [v1/engine/input_processor.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/input_processor.py#L242) | `InputProcessor.process_inputs()` | 校验并整理模型输入、采样参数，构造 `EngineCoreRequest`。 |
| [v1/engine/core_client.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core_client.py#L1121) | `AsyncMPClient.add_request_async()`、`abort_requests_async()`、`get_output_async()` | 跨进程发送 ADD / ABORT，接收 `EngineCoreOutputs`；传输层不承担调度与模型计算。 |
| [v1/engine/__init__.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/__init__.py#L88) | `EngineCoreRequest`、`EngineCoreOutput`、`EngineCoreOutputs` | 定义前端与 Core 之间的输入、单请求增量输出和批量输出契约；`finished` 由结束原因派生。 |
| [v1/engine/core.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L576) | `preprocess_add_request()`、`step()`、`abort_requests()` | 把已解码的核心输入转换为内部 Request；组织 `schedule → execute_model → update_from_output`，并接收终止控制。 |
| [v1/request.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/request.py#L59) | `Request.from_engine_core_request()`、`append_output_token_ids()`、`RequestStatus` | 持有可变请求状态、Token 历史和计算进度；区分队列位置与 `WAITING / RUNNING / PREEMPTED / FINISHED_*` 状态。 |
| [v1/core/sched/scheduler.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L425) | `schedule()`、`_update_after_schedule()`、`update_from_output()`、`finish_requests()` | 决定准入与本步计算量，维护在途记账，消费采样结果、处理终止和抢占，并生成设备侧清理通知。 |
| [v1/core/kv_cache_manager.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/kv_cache_manager.py#L283) | `get_computed_blocks()`、`allocate_slots()`、`free()` | 查询前缀命中、分配逻辑 KV slots/blocks、释放请求的块占用；不执行模型 forward。 |
| [v1/core/sched/output.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/output.py#L191) | `NewRequestData`、`CachedRequestData`、`SchedulerOutput` | 定义本步执行计划：新/已有请求、每请求计算量、block IDs，以及 `finished_req_ids` 等清理通知。 |
| [v1/outputs.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/outputs.py#L234) | `ModelRunnerOutput` | 定义执行侧返回 Scheduler 的结果：请求索引、采样 Token IDs、logprobs 等；区别于发给前端的 `EngineCoreOutput`。 |
| [v1/engine/output_processor.py](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L45) | `RequestOutputCollector`、`OutputProcessor.add_request()`、`process_outputs()` | 持有前端 RequestState，增量 detokenize、检查 stop string、组织 DELTA/累计输出、向 Collector 投递并清理前端状态。 |

阅读顺序：先识别跨边界载荷的字段，再找到构造／发送它的位置，最后找到消费／更新状态的位置。`SamplingParams.output_kind` 随核心请求携带，但 DELTA 的输出组织由前端 `OutputProcessor` 与 Collector 消费，不决定模型是否逐 Token 执行。

执行侧在 Pass C 保持黑盒，只读 `SchedulerOutput` 和 `ModelRunnerOutput` 两端契约；Worker、ModelRunner 的 batch/tensor 与 forward 内部实现留在 Pass D。

本地复查固定版本可使用：

```bash
git -C "推理框架/references/vllm" show 568afb3a13806beb53bb2e6bd518269357b237c0:vllm/v1/core/sched/scheduler.py
```

### 2.3 vLLM EP/PD 主图

### 2.4 SGLang/ATOM 边界对照

## 3. 适配设计

<a id="pass-e-adaptation-matrix"></a>
### 3.1 六层适配矩阵

本表对应 Pass E 的假想芯片综合题：请求／Token 调度语义不变，可通过既有接口表达设备运行时、KV padding、融合算子与 TP 子组通信差异。由学习者初稿经源码 Review 补齐，作为设计依据；不是该芯片已完成实现或运行验证的声明。

| 层次 | 本场景的处理方式与接入点 | 必须保留的契约 |
|---|---|---|
| HTTP／前端 | 保持协议处理不变 | 输入语义、流式输出和取消语义；进程放置不决定是否需要修改协议 |
| EngineCore／Scheduler | 保持普通请求生命周期与逻辑 KV 调度 | 请求状态、Token budget、逻辑块归属、抢占／恢复与结束清理相互一致 |
| Platform／Worker／ModelRunner | 平台插件通过 `check_and_update_config()` 设置 `parallel_config.worker_cls`；Worker 构造自定义 Runner，适配或替换设备执行实现 | 消费 `SchedulerOutput` 并返回约定结果；报告真实 KV 规格／可用内存并兑现分配方案；执行与采样的完成语义正确 |
| KV cache／Attention backend | 使用 `get_kv_cache_shape()`、`get_kv_cache_stride_order()`、`KVCacheSpec.page_size_bytes`，并适配实际分配及读写实现 | padding 后实际字节占用纳入预算；逻辑 Token、block table、slot mapping 与物理布局一致，读取遵守请求边界和注意力语义 |
| 普通算子 | 注册底层 PyTorch 算子；通过 `register_oot` 替换相应 vLLM 算子类，在 `forward_oot` 调用设备实现 | 保持数学语义、支持的 shape／dtype／device、输入修改／返回值及执行依赖契约；注册动作本身不是正确性契约 |
| 设备通信 | Platform 的 `get_device_communicator_cls()` 选择自定义 communicator | 正确绑定子组与 rank，保持 collective 数学语义、tensor 行为和后续消费所需的执行依赖 |

core patch 的论证应指出：需要的语义、现有字段／hook 能表达的范围，以及无法表达的信息或执行顺序。页大小漏报或已有抢占流程未被正确使用，首先属于实现／配置或契约遵守问题；不能仅凭换芯片、出现 OOM 或需要自定义 Runner 推断必须修改核心接口。

源码依据：[Worker 执行契约](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/worker_base.py#L142-L157)、[KV 页大小与 padding](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/kv_cache_interface.py#L175-L201)、[既有抢占路径](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L1212-L1234)。

### 3.2 既有经验迁移矩阵

### 3.3 C1–C5 Change Cards

## 4. 验证与证据

### 4.1 Correctness 与 failure matrix

### 4.2 分阶段 bring-up

### 4.3 Benchmark protocol

### 4.4 结果与待验证项

### 4.5 待做实践作业

<a id="w1-p1-runtime-output-validation"></a>

#### W1-P1：运行路径选择与最小输出契约验证

- **状态**：⬜ 待启动；当前只登记，尚未接受正式实践契约、准备执行环境或运行测试。
- **安排**：周末集中实践，暂按最近周末 **2026-09-12～2026-09-13** 记录；具体时段由用户启动时确认，可调整，不是硬截止日期，不自动执行或创建提醒。
- **目的**：将已经理解的 vLLM 请求链对应到明确配置与真实实现，并用一个小型验证检查已学过的输出契约。
- **版本与范围**：沿用 `vLLM v0.26.0 @ 568afb3a13806beb53bb2e6bd518269357b237c0`；普通文本、单请求场景。Executor 的 `backend=uni` 与 Attention backend 分别记录，不预设当前设备、模型或实际 backend。

**拟交付内容**

1. 一张“配置条件 → Worker／Runner／Attention backend 与相关 fallback → 源码依据 → 验证状态”的路径表。复核本文件 §1.3 的历史指纹，另行记录实践时的实际环境；不覆盖 2026-08-09 的历史观察，也不把历史 Windows／GPU 配置视为当前可用环境。
2. 一个最小用例的精确设计，包含输入构造、真实观察接口、断言、依赖条件与证明范围。有获准且兼容的环境时执行并保存结果；受限时采用原计划允许的 B 级设计路径，明确标注未运行。
3. 简短的结果与局限说明，区分源码推导、上游已有覆盖、本地执行结果和仍未验证的部分。完成判定以正式启动时确认的验收约定为准。

**候选验证点：FINAL_ONLY 与跨输出 stop string**

- 在前端 OutputProcessor 注册普通 `FINAL_ONLY` 请求，配置 stop string、`min_tokens=0` 和足够大的输出上限。
- 复用上游测试的构造方式，选定 tokenizer 与经核验的 token 序列，让 stop string 跨两次模拟 EngineCore 输出出现；命中时 Core 尚未判停。
- 检查 stop 出现前不交付中间 RequestOutput，命中后交付最终完整结果、生成对应的 `reqs_to_abort`，并注销前端 RequestState；迟到输出不重复交付。
- 该用例只验证前端输出过滤、文本判停和取消列表生成，不证明 HTTP／ZMQ 时序、Core 已执行取消或 GPU KV 已安全回收。

**参考材料与环境边界**

- [请求生命周期与输出处理](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md)。
- 固定版 [test_incremental_detokenization](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/tests/v1/engine/test_output_processor.py#L49-L141) 覆盖 DELTA／FINAL_ONLY；[test_stop_string](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/tests/v1/engine/test_output_processor.py#L761-L883) 当前使用 DELTA。可以参考二者设计交叉用例，不能声称现有测试已直接覆盖上述组合或本地已经通过。
- 现有 [测试 fixture](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/tests/v1/engine/conftest.py#L29-L45) 涉及 tokenizer 和 vLLM 配置；实践前核对兼容依赖与本地缓存，不承诺无需下载或当前环境直接可运行。
- 启动时再确认实现／验收文件的归属、允许的环境操作与通过标准；当前不安装依赖、不下载资源、不编写或执行测试，也不修改参考源码子模块。
- 本作业不扩展为完整服务部署、性能 benchmark、上游 patch 或口头验收；继续使用既有周预算，不另行记入未发生的学习时长。

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
- 2026-08-30 current `main` 静态预核对：在 `1dc464d42681d22f38caf1fdc1eb632dc4421c45` 中，internal/hybrid LB 会[启用统计发布](https://github.com/vllm-project/vllm/blob/1dc464d42681d22f38caf1fdc1eb632dc4421c45/vllm/v1/engine/core.py#L1080-L1087)；dense DP [仍走普通 `EngineCoreProc`](https://github.com/vllm-project/vllm/blob/1dc464d42681d22f38caf1fdc1eb632dc4421c45/vllm/v1/engine/core.py#L1327-L1336)，但其基类 busy loop 已在 step 前后[发布 running、waiting 与 KV 使用率](https://github.com/vllm-project/vllm/blob/1dc464d42681d22f38caf1fdc1eb632dc4421c45/vllm/v1/engine/core.py#L1410-L1435)，Coordinator 也会[消费这些统计](https://github.com/vllm-project/vllm/blob/1dc464d42681d22f38caf1fdc1eb632dc4421c45/vllm/v1/engine/coordinator.py#L369-L419)。因此旧提交中的静态缺口在当前快照已不能按原路径复现；尚未核对引入它的 issue/PR、专项回归测试和 dense `DP=2` 运行行为，不能据此写成“已修复”或关闭 U1。
- 待区分假设：① dense 发布链为实现遗漏，应补齐公共统计上报；②当前行为是有意设计，文档与配置注释需要说明限制；③该问题已在更新版本修复，固定 tag 只适合作为历史回归案例。
- 上游行动前置：
  - 🟡 对比最新 `main`：已完成 2026-08-30 静态预核对；动态行为、专项测试与变更来源仍待核验。
  - ⬜ 检索已有 issue、PR、讨论与 maintainer 设计意图，避免重复工作。
  - ⬜ 建立 dense `DP=2` 最小复现，观察 Coordinator 与 API client 收到的统计；当前单卡环境不能完成真实双副本测试。
  - ⬜ 先写能暴露缺口的测试，再决定修改代码还是文档。
- 最小贡献路径：
  1. 若为文档问题：明确 MoE 与 dense internal DP 在该版本的统计反馈差异。
  2. 若为代码问题：把请求计数发布抽到普通/DP EngineCore 可共享的窄接口，并避免把 MoE wave 语义错误带入 dense 路径。
  3. 无论哪条路径：补充 dense internal DP 的路由统计回归测试；必要时增加长短请求混合的分流验证。
- 完成定义：有固定版本最小复现、最新主线核验、已有讨论检索、失败测试或明确文档证据、maintainer 可审查的单一问题陈述；只有满足这些条件后才创建 issue 或提交 PR。
