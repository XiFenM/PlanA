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
- **授权边界**：前台仍为 W1，下述 vLLM revision 1 的文字练习已经收口。用户于 2026-09-14 确认保存 C++／Linux 基线、更新当前 Claim-evidence 矩阵，并接受 [Conv3D Case Card 正式练习 revision 1](#w1-conv3d-case-card-practice-20260914)。该练习只授权契约列明的记录与最终忠实投影，不直接改写 `CV.md`、既有项目事实或 `self-introduction.md`，不启动 W2–W4、新 Benchmark、环境安装、Kernel 实现或其他实践。
- **待做实践引用**：[W1-P1：运行路径选择与最小输出契约验证](#w1-p1-runtime-output-validation)、[W1-P2：C++／Linux 基线实践验证](#w1-p2-cpp-linux-validation)。两项均未启动，用户于 2026-09-15 确认暂缓；延期不取消原有证据要求，也不要求重复已通过的概念题。
- **W1 补充基线**：[C++／Linux 概念与书面校准](#w1-cpp-linux-baseline-20260914)已由用户确认收束，实践待验证；不构成整个 Lesson 的 `final_mastery`。
- **W1 Claim 审计**：[当前 Claim-evidence 矩阵](#w1-claim-evidence-matrix-20260914)已覆盖 19 条高风险表述，只裁决可用口径与补证边界，不直接修改外部文稿。
- **W1 Case Card 练习**：[Conv3D Case Card revision 1](#w1-conv3d-case-card-practice-20260914)已完成 A1–A6 的草稿验收，[Case Card v1](../面试准备/自我准备/projects.md#project1-conv3d-case-card-v1)已保存；不新增或改写本 Lesson 的三个目标，也不代表 W1 整体完成。
- **W1 反压补充**：[反压分层与立即重试变式](#plana-jd-w1-20260915-backpressure)已通过概念检查，与既有 DP／DPLB／TP 证据共同覆盖对应书面验收项；不声称实现或实测了端到端反压。
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

<a id="w1-cpp-linux-baseline-20260914"></a>

### W1 补充基线：C++／Linux 概念与书面校准

- **确认日期与结论**：2026-09-14，用户确认“C++／Linux 基线概念与书面校准完成，实践待验证”。本节对应[冲刺计划 W1 的基线任务](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#62-主任务)，不新增 Lesson，也不关闭 W1 或覆盖历史诊断。
- **证据形式**：本次对话中的短代码判断、推导、局部补差及三个综合情境；没有本轮编译运行、sanitizer、库加载或服务配置实测。未提供实际学习时长，不推算工时。
- **来源范围**：C++ 采用 [C++17 草案 N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf) 的生命周期、初始化、虚函数与删除规则；ELF 采用 [gABI 4.3 DRAFT](https://gabi.xinuos.com/elf/01-intro.html) 的 Section、Segment 与符号表约定。工具行为参考 [readelf](https://sourceware.org/binutils/docs/binutils/readelf.html)、[ldd](https://man7.org/linux/man-pages/man1/ldd.1.html)、[进程 maps](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html) 和 [环境继承](https://man7.org/linux/man-pages/man7/environ.7.html)；在线资料核验截至 2026-09-14，不代替未来实践环境的版本记录。

**基线缺口表**

本表的 🟩 只表示相应范围的书面判断通过，🟨 表示仅有讲解或仍缺实践证据，不等同于整体岗位能力评级。

| 范围 | 当前结论 | 最小证据与边界 |
|---|---|---|
| RAII、借用、移动与对象生命周期 | 🟩 书面通过 | 正确判断借用指针不延长生命周期、移动只转移管理权、`reset()` 不销毁管理对象，以及静态管理对象不保证动态资源一直存活；综合题 1 正确得到 7，由 `keeper` 经虚析构清理，返回整数仍有效。按值返回的理由经导师补准为独立副本，不要求数值不能来自对象成员。 |
| 静态／动态类型、overload／override／name hiding | 🟩 书面通过 | 能按名字查找、重载选择、虚派发分阶段判断；包含 `using Base::f` 与显式限定调用的综合题得到 2、10、1。显式限定不取消覆盖关系，只影响本次调用。 |
| 多态销毁与未定义行为 | 🟩 补差后通过 | 区分默认删除器通过 `Derived*` 与无虚析构的 `Base*` 删除派生对象；曾将 UB 展开成确定的“只析构基类并泄漏成员”，经讲解后在无额外资源的变式中仍正确判定 UB，不再保证具体析构序列。 |
| 编译／链接、声明／定义与符号身份 | 🟩 书面通过 | 能定位漏传目标文件的链接失败，拒绝用重复声明替代定义；识别 `add(int,int)` 与 `add(double,double)` 不能在链接时重新重载匹配。将定义合入一个源文件不等于取消最终链接，此措辞已补准。 |
| ELF 与存储期 | 🟩 补差后通过 | 区分 Section／Segment、`.data`／`.bss`、作用域／存储期；正确计算 `p_filesz=4 KiB`、`p_memsz=12 KiB` 的 8 KiB 零初始化尾部，以及零数组扩容只增加题设段的 `p_memsz` 2 MiB。综合题 2 漏写 `calls`，且把普通局部变量的理由简化为“局部”；补差变式 `static int local=5` 正确说明局部作用域、静态存储期、通常在 `.data`。 |
| 动态库搜索与证据链 | 🟩 核心书面诊断通过 | 区分构建时 `-L` 与运行时查找、缺库与缺符号；综合题 3 依据目标进程出错前的 maps 快照认定实际映射 A，不以当前终端 ldd 的 B 结果替代，正确解释 `UND` 不是可用定义，并提出启动新进程核查实际映射。 |
| C++17 保证的拷贝消除与可选 NRVO | 🟨 讲解补充 | 已回答用户关于返回 `unique_ptr` 的追问；没有单独完成返回值消除规则的独立变式或编译验证，不扩大为已验证的全部 copy／move 能力。 |
| 编译、sanitizer、ELF／动态库实测与服务启动配置 | 🟨 实践待验证 | 仅阅读示意代码、命令和模拟证据。环境变量继承、配置落实到真实服务启动入口、实际触发原故障调用由导师补充，未完成独立实操验证；见 [W1-P2](#w1-p2-cpp-linux-validation)。 |

**补差与判断边界**

- ELF 初讲时前置术语引入过快；按用户反馈补全“源码 → 目标文件 → 链接 → 装载 → 执行”的背景后继续，不把用户当时缺少前置说明记作已教授内容的错题。
- “新开终端会继承当前终端设置”“只确认进程启动就足够”不作为本轮已独立通过的部署能力。导师补充了父子进程环境传递、正式启动入口和触发 `compute(int)` 的验证要求，未把这些此前未展开的前提追加为书面阻塞项。
- 本轮已暴露的书面概念差距经补差收口；🟨 项仍保留原证据边界。线程同步、memory ordering、完整 ABI、并发生命周期程序以及现场编码未在本轮验证；不据此把诊断报告中的整个 C++／Linux 风险清零。

<a id="w1-claim-evidence-matrix-20260914"></a>

### W1 当前 Claim-evidence 矩阵

- **审计日期与范围**：2026-09-14；核对 [CV](../面试准备/自我准备/CV.md)、[项目档案](../面试准备/自我准备/projects.md)、[自我介绍](../面试准备/自我准备/self-introduction.md)、[2026-08-29 诊断旧表](../面试准备/自我准备/AMD-AI框架开发工程师胜任力诊断-2026-08-29.md#13-简历-claim-审计)及截至当日的 W1 evidence。旧诊断保持历史快照，不回写当前结论。
- **状态定义**：`已证明` 表示当前证据足以支持本表给出的有界口径；`需降级` 表示存在相关证据，但现有措辞、范围或数字超出证据；`待补证` 表示当前不应把该强表述作为能力事实。
- **证据层级**：固定 revision 源码只裁决对应实现理解；用户确认的项目口述可支持历史经历叙述，但不冒充 commit、Trace 或 Benchmark 的独立审计。性能数字只有在 Workload、绝对基线、方法和正确性同时闭环后才升级。

| ID | 当前强 Claim 与来源 | 裁决 | 当前证据与边界 | 当前可用口径／关闭条件 |
|---|---|---|---|---|
| `CL01` | [CV“深入理解 vLLM 模型执行、调度、KV Cache 与 PagedAttention”](../面试准备/自我准备/CV.md#推理框架与模型部署) | 需降级 | Pass A–E、12 文件 source map、KV 账本和独立文字变式已通过；实现证据固定于 `vLLM v0.26.0@568afb3`、V1／MRV1，不包含 Attention Kernel 算法、设备运行和性能实证。 | “能够基于 `vLLM v0.26.0` 源码解释 V1 请求执行、Scheduler／KV block 生命周期及 Prefix Cache 与 PagedAttention 的职责边界。” |
| `CL02` | [自我介绍“对 vLLM 执行链、调度、KV Cache、Chunked Prefill 比较熟悉”](../面试准备/自我准备/self-introduction.md) | 需降级 | 固定 `vLLM v0.26.0@568afb3` 范围内，独立主链复述以及调度／token 记账、取消／抢占、InputBatch／slot mapping 和 KV 账本的迁移检查已通过；Chunked Prefill 目前只有一次范围纠正，尚无无提示变式。 | 改为“比较熟悉 `vLLM V1` 的请求执行链、调度与 KV Cache”；Chunked Prefill 经独立复核后再并入口径。 |
| `CL03` | [CV“vLLM／PyTorch 源码级二次开发，完成多类模型四阶段适配”](../面试准备/自我准备/CV.md#工作经历) | 需降级 | [项目一口述](../面试准备/自我准备/projects.md#project1-oral-baseline-20260902)支持主要负责 Qwen2.5-VL、Qwen3-VL、ERNIE 4.5-VL 的框架层接入、精度对齐和性能优化；Qwen3-Omni、Llama、DeepSeek 及“各模型都完整覆盖四阶段”缺少同等粒度证据，生产项目也没有固定 commit／patch 审计。 | “主要负责 Qwen2.5-VL、Qwen3-VL、ERNIE 4.5-VL 的框架接入、精度对齐和性能优化。” |
| `CL04` | [CV“熟悉 SGLang 的 RadixAttention、结构化输出与调度”](../面试准备/自我准备/CV.md#推理框架与模型部署) | 待补证 | Lesson 虽固定 `SGLang v0.5.17@2948168` 教学基线，但尚未完成对应源码 map、学习者独立解释或 patch；固定版本和后续计划本身不构成能力 evidence。 | 当前从简历删除；完成固定版本窄对照并通过独立解释后，再决定是否写“了解”。 |
| `CL05` | [CV“掌握 Continuous Batching、Chunked Prefill、Prefix Cache”](../面试准备/自我准备/CV.md#推理框架与模型部署) | 需降级 | 固定 `vLLM v0.26.0@568afb3` 范围内，Prefix Cache 的 KV 账本、hash／refcount／reuse 和 PagedAttention 职责辨析已有独立证据；Chunked Prefill 只有补差后的预算拆分边界，Continuous Batching 尚无直接独立验收。 | 当前只写“能够基于固定源码解释 Prefix Cache 的命中、引用和复用边界”；Chunked Prefill 与 Continuous Batching 分别补独立变式后再加入。 |
| `CL06` | [CV“掌握 Speculative Decoding、PD 分离、量化和多模态推理”](../面试准备/自我准备/CV.md#推理框架与模型部署) | 需降级 | 多模态部署有项目口述支持；Speculative Decoding 在当前练习中明确排除，PD 状态机／性能模型尚无独立验收证据，量化也缺少当前可审查工件。 | 当前只保留“有多模态模型推理适配与部署经验”；Speculative Decoding、PD 分离和量化从能力口径删除，分别补证后再加入。 |
| `CL07` | [CV“熟悉 Qwen／Llama／DeepSeek／Ernie 及 MHA／MQA／GQA／MLA／MoE／MTP”](../面试准备/自我准备/CV.md#推理框架与模型部署) | 需降级 | 有若干模型适配历史口述，但当前 W1 并未分别验收每个模型和结构；名词列表不能代替对 shape、数据流和适配点的独立解释。 | 只保留有具体职责证据的 Qwen2.5-VL、Qwen3-VL、ERNIE 4.5-VL 项目经验；结构名词串当前删除，后续按 shape、数据流和适配点逐项补回。 |
| `CL08` | [CV“理解 Tensor、Storage、Stride、Dispatcher、Autograd、Caching Allocator 和 PrivateUse1”](../面试准备/自我准备/CV.md#pytorch-与分布式系统) | 需降级 | 项目口述支持 Tensor／Storage／Layout、PyTorch 算子接口、数据拷贝和后端调试经验；本轮未验收 Autograd、Allocator、PrivateUse1 及本人自定义算子注册／实现的完整调用链。 | “具备 PyTorch 算子接口、数据拷贝和 Tensor／Storage／Layout 问题的框架级调试经验”；其他 Internals 与自定义算子实现逐项补证。 |
| `CL09` | [CV“熟悉 DeepSpeed、Megatron-LM、FSDP 及 ZeRO／TP／SP／PP／EP”](../面试准备/自我准备/CV.md#pytorch-与分布式系统) | 需降级 | [项目四](../面试准备/自我准备/projects.md#project4-oral-baseline-20260903)支持参与 DeepSpeed ZeRO-3、Megatron-LM TP 与通信后端适配；两框架交付范围、实际并行组合、Loss 对齐和代码边界未核，FSDP 无直接证据。 | “参与 DeepSpeed ZeRO-3、Megatron-LM Tensor Parallel 与通信后端适配，处理 Padding、Collective 与 Stream 语义问题”；FSDP 当前删除，待补证后再加入。 |
| `CL10` | [CV“理解 Ring／Tree AllReduce、ReduceScatter、AllGather，具备自研通信后端经验”](../面试准备/自我准备/CV.md#pytorch-与分布式系统) | 需降级 | 项目四和 TP 子组变式支持通信接口、分组、精度、同步及性能定位经验；未单独验收 Ring／Tree 算法、通信量和多拓扑选择。 | “具备自研通信后端的接口适配、分组正确性、同步语义和多卡性能定位经验”；Ring／Tree 另行补证。 |
| `CL11` | [CV“具备 Kernel 开发调优经验，熟悉 Triton／TileLang 及 FlashAttention”](../面试准备/自我准备/CV.md#高性能计算与工程能力) | 需降级 | Conv3D 和 blocked Col-major 只支持框架侧 Shape／Layout 分析、Kernel 接入及协同调优；内部 Kernel 由算子同事实现。无本人 Triton／TileLang／FlashAttention 概念验收、实现、正确性或 profiler 工件。 | “具备 Kernel 接入、真实 Shape／Layout 分析和与算子团队协同调优经验”；Triton、TileLang、FlashAttention 当前删除，待独立证据后再加入。 |
| `CL12` | [CV“擅长以 Profile、算子对比、控制变量和 Replay 定位性能及精度问题”](../面试准备/自我准备/CV.md#个人概述) | 已证明 | Conv3D、ECG、异步 H2D 和训练通信四个项目口述均给出该方法的具体用法和 ownership；这是用户确认的历史经历证据，不是本轮重跑 Trace 的结果。 | 可保留方法型表述，不把任一单次现象扩张为已证明的底层机制或所有 workload 通用。 |
| `CL13` | [CV“能够使用 Roofline 方法拆解端到端瓶颈”](../面试准备/自我准备/CV.md#高性能计算与工程能力) | 需降级 | ECG 口述支持低并发 GEMM 的 FLOPs、最低 Bytes 和 AI 初步推导；读写次数、cache reuse、设备屋脊点、实测带宽和效率未闭环。 | “做过低并发 GEMM 的 Roofline 初步估算，用于判断权重访存可能占主导”；完成可复算全链后再升级。 |
| `CL14` | [CV“能够使用 Nsight Systems／Compute，并建立可重复 Benchmark”](../面试准备/自我准备/CV.md#高性能计算与工程能力) | 待补证 | 通用 Profile／Trace 有历史项目支持，但 Nsight 只见 CV 自述，没有版本、命令、Trace／counter 解读或可复现工件。 | 当前口径只保留“使用框架 Profile／Trace 和控制变量分析 Host、算子、拷贝、通信与 Layout 瓶颈”；Nsight 待真实 capture 补证。 |
| `CL15` | [CV“熟练使用 C／C++、Linux”](../面试准备/自我准备/CV.md#高性能计算与工程能力) | 需降级 | [C++／Linux 基线](#w1-cpp-linux-baseline-20260914)支持 RAII、多态、编译链接、ELF 和动态库诊断的书面理解；编译、sanitizer、真实库加载、线程／memory ordering、ABI 和现场编码尚未实践验证。 | “熟练使用 Python、Linux、Git 和 Bash；具备 PyTorch 扩展与通信适配层的 C++ 修改和调试经验”；不把书面基线升级为“熟练 C++ 系统开发”。 |
| `CL16` | [CV／自我介绍“Qwen3-VL Conv3D 使 TTFT 下降 40%”](../面试准备/自我准备/projects.md#project1-oral-baseline-20260902) | 需降级 | 口述支持 `OOM → 小通道 Padding → 模型侧布局重构 → 算子协作 → 两级验证`；模型是 Qwen2.5-VL-32B 还是 Qwen3-VL、具体性能幅度、绝对耗时、Profile 分母和布局／Kernel 收益拆分均未统一。 | 暂撤下百分比与冲突模型名；只说“完成模型侧布局重构并协同算子优化，消除已观察到的 OOM，显著降低 Conv3D 开销和 TTFT”。 |
| `CL17` | [CV“ECG 从 40 秒以上降至 10–15 秒”](../面试准备/自我准备/projects.md#project2-oral-baseline-20260902) | 需降级 | 项目口述支持分阶段优化并达到客户时延目标；当前起止范围、Transformers／vLLM 边界、输入／输出长度、并发、预热、统计和单项消融未统一。 | 对外先不写精确起止数字，改为“经过 Host 路径、小 Shape 计算和权重布局优化，显著降低端到端时延并达到客户验收目标”。 |
| `CL18` | [自我介绍“Col-major 使三类模型少并发吞吐提升约 20%”](../面试准备/自我准备/self-introduction.md) | 待补证 | 只见自我介绍中的同源数字；项目二只支持 ECG 的权重预排布与访存判断，不支持 Llama-3-70B、Qwen2.5、Qwen3 三模型和 `20%` 口径。 | 暂删模型列表和百分比；可改为“在低并发小 Batch 场景中，通过加载期权重预排布改善 Matmul 访存效率”。 |
| `CL19` | [CV／自我介绍“vLLM V1 异步 H2D／D2D 异常目前根因闭环中”](../面试准备/自我准备/projects.md#project3-oral-baseline-20260902) | 已证明 | 新项目基线已覆盖旧状态：按用户口述，根因为 `CPU Padding 完成 → H2D 提交 → 设备拷贝完成 → 消费` 依赖不完整，已修复；168 条请求×5 轮，共 840 次在当前请求集中未再观察到原异常。本表不采用已撤回 diff，也不扩张为全部 Runtime 实现归属或所有 workload 零故障。 | 当前文稿的“根因闭环中”已滞后；可改为“定位两阶段 Host 准备与异步 H2D 间的依赖缺口，通过统一异步任务标记与等待机制完成修复；修复后在现场 168 条请求×5 轮回归范围内未再复现”。 |

**矩阵结果**：`已证明` 2 条，`需降级` 14 条，`待补证` 3 条，共 19 条。这一结果完成 W1 的当前 Claim 审计门，但不代表原文稿已经改写，也不代表其他 W1 任务完成。后续修订外部文稿时以本表为当前裁决入口，项目事实和数字仍回到各项目的待核字段关闭。

<a id="w1-conv3d-case-card-practice-20260914"></a>

### W1 正式练习：Conv3D Case Card v1

- **练习 ID／revision**：`plana-jd-w1-conv3d-case-card-20260914`／`1`。
- **digest**：`sha256:1a3a5859a2ed220310f6c4fb5305b7c26450e2275477d74a1d3ee1a12ca62660`。
- **接受事件**：[`plana-jd-w1-20260914-conv3d-case-card-accepted`](#plana-jd-w1-20260914-conv3d-case-card-accepted)，绑定上述 revision 与 digest。
- **运行范围**：W1 附属独立正式练习；`conceptual` 与 `practical` 为 required，`empirical` 为 not-required。不把 `w1-conv3d-case-card` 静默加入现有 vLLM Lesson 的 required objective。
- **规范化契约**：以下对象是已接受契约的持久投影。digest 只覆盖 `id`、`targets`、`task`、`deliverables`、`acceptance`、`scope` 与 `optional`；递归按 key 排序、保留数组顺序并采用 UTF-8 紧凑 JSON 计算。

```json
{
  "id": "plana-jd-w1-conv3d-case-card-20260914",
  "targets": [
    {
      "objective_id": "w1-conv3d-case-card",
      "missing_dimensions": ["conceptual", "practical"],
      "evidence_gap": "现有项目口述与 CL16 只支持有界叙述，尚无一张由学习者独立组织、字段齐全且可审计的 Conv3D Case Card；模型、Workload、Shape 和性能数字仍有待核项。"
    }
  ],
  "task": "基于项目一 2026-09-02 口述基线、W1 Case Card 模板与 CL16，独立完成 Conv3D Case Card v1；覆盖 F1–F6，并将每项标为“项目口述”“原始记录已核”或“待核”，不得补造未知事实或性能数字。",
  "deliverables": [
    {
      "artifact": "dialogue:plana-jd-w1-conv3d-case-card-v1",
      "outcome": "学习者在对话中提交并修订完整卡片核心内容，覆盖 Claim 与范围、问题与基线、机制与反证、修改与 ownership、正确性与性能验证、结果归因与限制。"
    },
    {
      "artifact": "面试准备/自我准备/projects.md#project1-conv3d-case-card-v1",
      "outcome": "全部 required acceptance 通过后，Agent 将学习者已确认内容忠实投影为受管 Markdown section；只规范结构和明显笔误，不补造事实、数字或 ownership。"
    }
  ],
  "acceptance": [
    {
      "id": "A1",
      "criterion": "F1–F6 关键字段齐全；每个事实有来源标签，未知项写明“待核”、原因和可执行关闭动作，不静默选定冲突模型或 40% 数字。",
      "evidence_method": "按 W1 Case Card 模板与项目一待核字段逐项 rubric review。"
    },
    {
      "id": "A2",
      "criterion": "机制链明确连接逻辑 Shape、物理 Layout/Stride、对齐与 Padding、实际 Bytes/搬运以及 OOM/时延；区分 Padding、Workspace 和 Kernel 性能。实际参数缺失时允许使用符号公式，但必须标出补数条件。",
      "evidence_method": "对卡片机制链做可复算性检查；不要求本轮取得新的原始数据。"
    },
    {
      "id": "A3",
      "criterion": "至少列出一个竞争解释，并说明哪个控制变量、Trace 或对照能够支持或否定当前布局假设。",
      "evidence_method": "检查假设—证据—反证链是否可证伪。"
    },
    {
      "id": "A4",
      "criterion": "正确性验证与性能验证分开；包含单算子和端到端两层契约，明确 reference、误差/输出判据、Workload 可比条件和测量边界；缺失值保持待核。",
      "evidence_method": "按验证契约 rubric 检查，不运行新 Benchmark。"
    },
    {
      "id": "A5",
      "criterion": "清楚区分“我负责／我参与／他人负责”，不把 Conv3D Kernel 内部实现归给本人；最终对外口径不强于 CL16。",
      "evidence_method": "与项目一口述基线的个人职责边界及 CL16 交叉核对。"
    },
    {
      "id": "A6",
      "criterion": "学习者能够解释一个关键验证选择，并在 Review 后无实质提示完成一个表面不同但机制相同的条件变式。",
      "evidence_method": "对话解释与一次无提示小型变式。"
    }
  ],
  "scope": {
    "learner_owned": [
      {
        "artifact": "dialogue:plana-jd-w1-conv3d-case-card-v1",
        "operations": ["create", "modify"]
      }
    ],
    "agent_owned": [
      {
        "artifact": "推理框架/EP-PD自研芯片适配设计与验证包.md#w1-conv3d-case-card-practice-20260914",
        "operations": ["read", "create", "modify", "record"]
      },
      {
        "artifact": "面试准备/自我准备/projects.md#project1-conv3d-case-card-v1",
        "operations": ["read", "create", "modify", "record"]
      },
      {
        "artifact": "计划/学习断点.md",
        "operations": ["read", "modify", "record"]
      },
      {
        "artifact": "计划/高级AI框架开发工程师-八周证据冲刺计划.md#64-验收门",
        "operations": ["read", "modify", "record"]
      }
    ],
    "read_only": [
      {
        "artifact": "计划/高级AI框架开发工程师-八周证据冲刺计划.md#44-case-card-模板",
        "operations": ["read"]
      },
      {
        "artifact": "计划/高级AI框架开发工程师-八周证据冲刺计划.md#62-主任务",
        "operations": ["read"]
      },
      {
        "artifact": "面试准备/自我准备/projects.md#project1-oral-baseline-20260902",
        "operations": ["read"]
      },
      {
        "artifact": "推理框架/EP-PD自研芯片适配设计与验证包.md#w1-claim-evidence-matrix-20260914",
        "operations": ["read"]
      },
      {
        "artifact": "面试准备/自我准备/CV.md",
        "operations": ["read"]
      },
      {
        "artifact": "面试准备/自我准备/self-introduction.md",
        "operations": ["read"]
      },
      {
        "artifact": "面试准备/自我准备/AMD-AI框架开发工程师胜任力诊断-2026-08-29.md#72-优化案例必须升级为可审计-case-card",
        "operations": ["read"]
      }
    ],
    "excluded": [
      {
        "artifact": "projects.md 中现有项目事实与待核字段、CV、自我介绍和旧诊断的改写；目标 Case Card section 之外的新文稿",
        "operations": []
      },
      {
        "artifact": "未跟踪内容、公司代码、内部 API、未公开硬件参数、原始日志、已撤回 diff 或未经确认可披露的信息",
        "operations": []
      },
      {
        "artifact": "新 Benchmark/Profile/counter、环境安装、Kernel 实现或调优、W1-P1/P2、Roofline、其他 Case Card、W2–W4",
        "operations": []
      },
      {
        "artifact": "W1 整体完成、Lesson final mastery 或 CL16 证据等级升级",
        "operations": []
      }
    ]
  },
  "optional": []
}
```

- **当前 Review 状态**：A1–A6 在已接受 revision 1 的草稿范围内通过，正式练习已结束；[Case Card v1](../面试准备/自我准备/projects.md#project1-conv3d-case-card-v1)由学习者对话核心内容忠实整理后保存。图片性能的 10 例均值、视频单次测量、未覆盖的视频模型级精度及原始资料缺口均明确保留；未确认可披露的数值没有写入项目正文。项目经历继续按用户口述／自核层使用，不升级为原始 commit、Issue、脚本或运行结果的独立审计，不写 Lesson final mastery。
- **F1 当前可保留输入**：用户确认所列 Qwen2.5-VL／Qwen3-VL 全部规格均适用两组单算子 Shape，并提供框架版本、BF16、Conv3D 配置及单并发历史信息；实际模型级验证仅按 F5 所述范围记录。本人负责问题定位、复现提取、模型调用重构和权重布局调整，与算子同事协作完成方案；观察到的资源和性能改善保留适用条件。项目事实的工作稿投影现见上述 Case Card，原始记录与数字缺口不因保存而关闭。

- **布局定位与算量证据**：学习者说明原始 Host 输入为二维展平张量；H2D 准备阶段先补齐二维末维，再传入设备，框架侧保留逻辑尺寸。随后设备侧 view 拆分逻辑维度并复用原存储；通道重排由后端算子生成新的存储时，才出现小通道末维的高比例补齐。具体内部参数留在学习者对话工件，当前只记录上述机制边界。学习者独立给出图片输入的逻辑／补齐字节公式；导师纠正了提前取整导致的倍数误差，并根据后续补充区分“相对逻辑输入”与“相对既有设备输入”两个分母。以上属于口述与纸面推导，不是分配器实测或 OOM 峰值证据。
- **术语核对**：后端所称 `reshape` 暂按用户报告的“通道重排并生成新存储”理解，不仅凭内部名称判错；标准 PyTorch 的 [view](https://docs.pytorch.org/docs/2.11/generated/torch.Tensor.view.html)、[reshape](https://docs.pytorch.org/docs/2.11/generated/torch.reshape.html) 和 [permute](https://docs.pytorch.org/docs/2.11/generated/torch.permute.html) 语义只作公开接口说明，不裁决历史自研实现。实际 stride、物理描述和连续性标记尚未提供，不从逻辑 Shape 自动推出。
- **首维与并发边界**：学习者将首维解释为预处理产生的视觉分块数，区分图片空间切分、视频时间／空间切分与请求级单并发；原始图片已无法恢复，所举二维网格仅为可能解释。以 [Transformers v4.51.3 的 Qwen2-VL 预处理源码](https://github.com/huggingface/transformers/blob/v4.51.3/src/transformers/models/qwen2_vl/image_processing_qwen2_vl.py#L256-L280)作概念对照，单视觉项的首维为 `grid_t × grid_h × grid_w`，网格取决于预处理后的尺寸与时间分组；该源码不证明历史自研版本的实际网格。导师补准：多个请求的视觉数据合入同一次调用时才可按所合并的分块数累加，服务并发增加本身不决定每次 Conv3D 的首维。
- **剩余快照待核字段**：原始媒体及具体网格因素材缺失无法唯一恢复，当前只保留已报告的算子输入规模；实际 stride、存储观测、连续性标记及 accumulation dtype 尚无原记录，分别以对应后端的张量描述、分配记录与算子配置为后续核对来源，缺失时不填入推测值。F5 已由用户补充输入／权重采用 BF16，比较前是否另有 dtype 转换仍待核。按 revision 1 允许未知项留待核的约定，这些状态不升级为本轮找回素材或新跑实验的要求。
- **F2／F3 排查证据（2026-09-15 补充）**：学习者明确首次 OOM 出现在 Qwen2.5-VL-32B 的视频输入；Python 调用栈指向 PyTorch Conv3D，复现并打印输入后获得视频单例的算子 Shape。学习者依据该自研算子库的输入连续化要求提出 Padding 膨胀假设，检查算子处理逻辑后发现通道末置重排；随后将重排从 Conv3D 内部外提，在单例中使用 PyTorch 显存 snapshot 检查，观察到重排后显存跃升。该链支持将显存膨胀定位到重排与补齐阶段；“连续化会补齐”只描述该后端行为。此处保存用户对历史观察的报告，未读取原始代码或快照，也不把原始首次故障推广为全部模型均曾 OOM。
- **当前证据边界**：布局账本可预测重排输出的容量，但不能替代快照中的实测峰值、失败分配字节与同时存活对象记录。Workspace、其他存储和生命周期的叠加贡献、单算子时延与优化因素的独立贡献仍待核。TTFT 只保留各模型和样本组的近似口述结果；图片均值与视频单次测量分别标注，不能从 OOM 用例构造有限时延基线。后续可用脱敏记录核对这些字段，当前不要求新跑实验。
- **F4 输入与权重方案**：学习者说明优化后沿用二维输入的 H2D 路径，保持 `C×T×H×W` 合并维，并向专用 Conv3D 算子传入四个逻辑维度的标量参数；权重也在初始化时保留为 `(out_channels, C×T×H×W)`。调用侧取消了输入与权重的通道末置物化，因而避免产生对应的大规模补齐缓冲。算子内部是否在 SRAM 中再次补齐及如何计算，学习者明确不掌握，继续保留算子团队的实现边界。
- **展平映射检查**：学习者独立给出零起始索引 `k=c×T×H×W+t×H×W+h×W+w`，并正确用整除和取模可逆说明无元素丢失；输入与权重采用同一映射时，可保持相同卷积窗口内的元素乘积配对。当前证据支持逻辑映射，不证明专用算子实装、物理 Padding 处理或 BF16 数值正确性；完整卷积语义仍须结合实际配置和 F5 对照确认。
- **F5 正确性参考与判据**：用户明确专用算子与 CPU Conv3D 的 golden reference 对照，原设备算子接入时也曾与 CPU 参考对照，并未做新旧设备实现直接互比。用户报告采用测试套件默认 `rtol=0.1、atol=0.05`；当前可记录为在该容差内通过 CPU 参考检查，不能表述为逐元素严格相等或新旧实现必然在相同容差内彼此接近。导师将此前“与原始 Conv3D 一致”的问法修正为“对共同 CPU 参考验证”，不追加直接互比要求。
- **F5 数据与输出对齐**：学习者说明在 CPU 上用 `torch.randn` 准备同一份 BF16 输入和权重，先执行 CPU Conv3D 参考计算，再将输入及权重的卷积维度按共同次序展平并 H2D，调用专用算子。当前具体恢复的是视频 Shape 单例；在所述卷积核、步长和无 Padding 配置下，CPU 输出为 `(N,out_channels,1,1,1)`，专用算子输出为 `(N,out_channels)`。仅 squeeze CPU 输出最后三个单例维后按既定容差比较，保留 N 与输出通道轴。该叙述支持同份数据和输出映射的单算子验证，不自动证明整模型正确性。
- **F5 模型级回归**：用户报告从 `vision-arena-bench-v0.1` 随机抽取 10 个含图片的测例，在 Qwen2.5-VL-32B 上设置 `temperature=0`、随机种子 `1234`，记录专用 Conv3D 接入后的模型输出，并与模型采用 CPU Conv3D 参考路径时的输出逐 Token 比较，10 例输出 Token 序列完全一致。当前只据此描述这组图片测例的回归结果；实际模型权重 revision、样本标识及其余运行配置未恢复，不外推到全部型号或全量数据集。[官方数据集页](https://huggingface.co/datasets/lmarena-ai/vision-arena-bench-v0.1)仅核对名称与资料入口，不证明历史样本选择或运行结果；本轮未下载数据或执行评测。
- **F6 已知覆盖限制**：用户明确没有做视频输入的模型级回归。视频 Shape 的随机张量单算子测试与上述图片模型级测试分别保留适用范围；不把单算子通过、首次视频 OOM 的定位或配置确定性扩展为视频端到端正确性。此项作为已知限制记录，按当前草稿契约不自动增加视频实验或扩大样本量的要求。
- **F6 性能结果分组**：用户明确视频性能计时来自可正常运行的 3B 模型，只有同一随手选取视频的一次请求；32B 视频 OOM，没有对应的优化前 TTFT；32B 图片记录的是数据集中 10 个测例的平均 TTFT。用户确认前后使用相同输入与运行配置，报告优化后图片均值及视频单次观测的上界，具体原始数值未恢复。三组分别保留，不能用 3B 视频代替 32B 视频基线，也不把图片均值上界改成每条请求的上界。近似耗时保留在本次学习者口述中，正式卡片中的数字待测量和披露口径确认后再写入；不计算跨模型或跨输入的收益。
- **F6 计时与统计方法**：客户端从请求发送计时，到收到第一个生成 Token 结束；请求前确认模型初始化完成、API 服务可用，模型加载和预热不计入所报 TTFT。图片组是 10 个不同测例各一次请求的算术平均；视频组仅一个样本、一次请求，不称 10 例平均。此前将“10 例平均”统一用于两组的解读已由用户后续澄清修正；当前没有同一测例重复运行的波动或分位数证据。
- **样本对应关系**：固定单算子图片／视频 Shape 来自用户另外随手选择的媒体，不在 `vision-arena-bench-v0.1` 内，不作为该数据集 10 个图片测例共有的 Shape。3B 视频性能使用的仍是随手选择的同一个视频。原始媒体、数据集抽样标识与各样例网格尚未恢复，按待核保留。
- **输出分配边界**：用户解释二维返回旨在避免输出末维 Padding；新接口的二维输出形状已明确，但旧设备输出的物理布局、实际分配和节省量尚未提供，输出侧显存收益暂不写成已核结果。
- **容差解释与待核边界**：若当时采用标准 [PyTorch assert_close](https://docs.pytorch.org/docs/2.11/testing.html#torch.testing.assert_close) 或等价比较，对于有限实数元素，误差界为 `abs(actual-reference) <= atol + rtol×abs(reference)`；这是接口说明，尚未核对历史脚本的具体比较函数。比较前是否转换 dtype、实际误差、随机种子、完整输入集合和回归次数仍待核；不把套件默认阈值等同于实测误差，也不因本轮检查而自动收紧历史验收阈值。

<a id="w1-conv3d-case-card-findings"></a>

#### 当前 findings

| ID | 映射 | 严重度 | owner | 状态 | Evidence（建立／复核） | 下一动作 |
|---|---|---|---|---|---|---|
| `conv3d-F01-case-scope` | A1、A5 | major | learner | closed | 建立：初稿缺少 Claim 句，多个模型规格未与案例关联。复核：用户确认两组 Shape 适用于所列全部规格，并自行提交问题定位、复现提取、模型调用重构、算子协作及定性结果的 Claim；没有填入未核百分比，也没有宣称独立实现 Kernel。结果按相应已验证输入与测试范围理解；仅关闭范围与表述缺口，不等于性能实证或 A1／A5 全部通过。 | — |
| `conv3d-F02-layout-snapshot` | A1、A2、A4 | major | learner | closed | 建立：逻辑维、物理对齐维和分配位置混写。复核：学习者已说明 Host 二维输入补齐、设备侧 view 复用与通道重排生成大张量的顺序，并区分视觉分块数与请求级并发；原图和具体网格明确未知，其余快照字段已列待核与核对来源。导师补准了算量舍入与并发累加条件；本次仅关闭草稿的布局表述歧义，独立变式及 A2／A4 整体证据仍须按原契约验收。 | — |
| `conv3d-F03-provenance` | A1 | minor | learner | open | `vLLM 0.9.3` 尚未绑定内部 fork 的实际 commit；当前来源锚点是泛称，末列“关闭”只表示状态，不能让复核者重新定位证据或区分已关闭／待关闭。 | 把已核项写成“已关闭：依据可重新定位的脱敏记录，无后续动作”；将实际 commit 或其他未确认字段标为“待核”并给出具体核验动作。 |

<a id="w1-conv3d-case-card-transfer-1"></a>

#### A6 独立变式：布局容量与另一种分配来源

- **状态与边界**：已作答并通过，沿用 revision 1 的 A2／A3／A6；以下全部是教学假设，不是项目设备参数。
- **题设**：BF16，`N=1024、C=8、T=2、H=W=8`；每个新分配张量的最内层连续数据段按 256 Bytes 向上补齐。方案甲分配二维输入 `(N,C×T×H×W)`；方案乙物化通道末置输入 `(N,T,H,W,C)`。只计算每个方案的单个输入缓冲，不计其他分配。
- **交付 1**：独立计算两种方案各占多少 MiB，以及方案乙相对于甲的存储量倍数。
- **交付 2**：若同步后的快照显示，进入卷积计算后还新增了一块无法由上述输入缓冲解释的显存，提出另一种可能来源，并说明用什么检查区分它与输入 Padding。
- **复核证据**：学习者独立算出甲 2 MiB、乙 32 MiB、乙为甲的 16 倍，正确处理 BF16 字节与对齐；提出输出 Tensor 分配的竞争解释，并建议在输出分配前后添加显存快照检查。该方法能够区分分配阶段，满足当前变式的计算与可证伪判断要求。
- **非阻塞补准**：乙的物理 Shape 应为 `(1024,2,8,8,128)`，提交中交换了 T／H 次序，但乘积和容量正确，不要求重复整题。输出是否补齐仍由真实物理内层维与分配规则决定，不能仅从逻辑尾维为 1 推定。

#### 本次练习验收

| 验收项 | 最小证据 | 判断 |
|---|---|---|
| A1：字段与来源 | Case Card 覆盖 F1–F6；口述、自核与待核分开，缺口均给出核验方式 | 通过 |
| A2：机制与算量 | H2D／view／通道重排分开，输入与权重共同索引可逆；A6 独立算出两种输入容量和倍数 | 通过 |
| A3：可证伪性 | 项目中外提重排检查快照；A6 提出输出分配的替代解释及分配前后对照 | 通过 |
| A4：验证契约 | 同份 BF16 数据对 CPU 参考、输出 squeeze 和容差；模型级图片 Token 对照与视频未覆盖；TTFT 分组、计时和统计边界明确 | 通过 |
| A5：职责与口径 | 模型调用和权重处理由本人负责，Kernel 内部归算子团队；性能数值与贡献拆分保持待核，未升级 CL16 | 通过 |
| A6：解释与独立迁移 | 学习者解释 CPU／专用输出对齐，并无实质提示完成新参数的容量计算和另一分配来源判断 | 通过 |

- **帮助与独立性**：导师提供了字段释义、口径收窄、舍入与单位、统计范围等补准；学习者提供项目核心叙述并完成共同展平映射、验证解释及最后的独立变式。Agent 只将已提交内容整理为授权章节，未代做核心推导、代码或历史实验。
- **关闭范围**：本次独立练习的 conceptual／practical 草稿证据充分，empirical 为 not-required；required blocking／major 开放数为 0，`conv3d-F03-provenance` 保留为非阻塞 minor。只有 W1 Case Card 草稿门完成，历史实证与披露缺口、整个 W1 和 Lesson mastery 均不随之关闭。

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

#### `plana-jd-w1-20260914-cpp-linux-baseline`

- **日期**：2026-09-14（用户确认收束日）。
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`；归入 W1 附属基线任务，不改既有 vLLM 目标或历史契约。
- **覆盖范围**：C++ 所有权与多态、ELF／存储期、编译链接与动态库诊断。
- **已完成动作**：完成三个书面综合情境及必要局部补差；用户确认保存基线结论和待实践项。记录 [基线缺口表](#w1-cpp-linux-baseline-20260914)，登记 [W1-P2](#w1-p2-cpp-linux-validation)。
- **开放问题**：独立编译、sanitizer、真实 ELF／库加载、服务启动环境配置仍待验证；RVO／NRVO 保留为讲解补充。
- **证据边界**：本次只是概念与书面校准收束，不是实践契约接受、实际测试通过或整个 W1 的关闭；未写入 `final_mastery`，未估算学习时长。

#### `plana-jd-w1-20260914-claim-evidence-matrix`

- **日期**：2026-09-14。
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`；归入 W1 Claim 校准任务，不改动原 vLLM 三目标。
- **覆盖范围**：当前 `CV.md`、`projects.md`、`self-introduction.md` 的高风险能力与性能表述，以 2026-08-29 诊断旧表为历史 seed，吸收 W1 新增书面／源码 evidence 和项目口述更新。
- **已完成动作**：完成 [19 条当前 Claim 矩阵](#w1-claim-evidence-matrix-20260914)；裁决为已证明 2 条、需降级 14 条、待补证 3 条，每条都有当前可用口径或关闭条件。
- **证据边界**：本次没有改写简历、项目档案或自我介绍；项目性能和历史事实仍为用户口述层，未使用已撤回 diff，未冒充为原始 Benchmark、Trace 或 commit 审计。不写 `final_mastery`，不标记 W1 整体完成。

#### `plana-jd-w1-20260914-conv3d-case-card-accepted`

- **日期**：2026-09-14。
- **Session topic**：W1 Conv3D Case Card v1；这是附属独立正式练习，不新增现有 vLLM Lesson 的 required objective。
- **覆盖范围**：项目一口述基线、W1 Case Card 模板与 Claim 矩阵 `CL16` 的有界材料组织。
- **已完成动作**：用户明确接受 [练习 `plana-jd-w1-conv3d-case-card-20260914` revision 1](#w1-conv3d-case-card-practice-20260914)，绑定 digest `sha256:1a3a5859a2ed220310f6c4fb5305b7c26450e2275477d74a1d3ee1a12ca62660`；契约列明学习者核心内容、Agent 记录路径、A1–A6 与排除范围。
- **开放问题**：学习者尚未提交 F1–F6 核心内容；模型版本、Workload、Shape、性能数字和原始实证继续保持待核。
- **证据边界**：接受契约只启动练习，不证明卡片通过，不创建项目正文，不升级 `CL16`，不标记 W1 或 Lesson 完成；未提供学习时长。

#### `plana-jd-w1-20260914-conv3d-case-card-f1-review`

- **日期**：2026-09-14。
- **Session topic**：W1 Conv3D Case Card v1 的 F1“Claim 与范围”首版 Review。
- **覆盖范围**：模型与版本、框架版本、候选 Conv3D Shape／dtype、请求并发及 512 B 对齐环境叙述。
- **已完成动作**：学习者提交 F1 首版；按 revision 1 的 A1／A2／A5 Review，保留用户确认的历史输入边界并打开 [3 个稳定 findings](#w1-conv3d-case-card-findings)，其中 2 个 major、1 个 minor。
- **开放问题**：具体案例与模型规格尚未绑定；逻辑／物理 Layout、请求 Batch／算子 N 和对齐作用层级未拆开；实际 fork commit 与可重定位来源锚点仍待补准。
- **证据边界**：本段不复制学习者原表，不把用户自核来源冒充 Agent 独立审计，不创建项目 Case Card 正文，不确认任何性能数字，不记录学习时长。

#### `plana-jd-w1-20260915-conv3d-diagnosis`

- **日期**：2026-09-15（补充排查过程的会话日期，并非项目故障日期）。
- **Session topic**：Conv3D Case Card 的故障定位、接口重构与正确性回归。
- **覆盖范围**：F2 故障与基线、F3 局部对照、F4 接口与元素映射、F5 正确性回归，以及 F6 性能分组与计时统计方法。
- **已完成动作**：学习者完成 F1–F6 核心内容和 A6 独立变式，A1–A6 按既定草稿范围通过；忠实整理并保存 [Case Card v1](../面试准备/自我准备/projects.md#project1-conv3d-case-card-v1)，完成 W1 对应的 Case Card 验收项。
- **开放问题**：实际误差、样本标识、精确耗时、峰值、失败分配及分项收益保留待核，视频模型级精度仍未覆盖。
- **marker**：`practice-closed`。
- **证据边界**：完成的是草稿组织与独立解释练习；本轮没有执行模型、读取内部代码或核验原始 snapshot，未升级 CL16，未关闭 W1 或写入 Lesson final mastery，未记录未提供的学习时长。

#### `plana-jd-w1-20260915-backpressure`

- **日期**：2026-09-15。
- **Lesson 引用**：`plana-jd-w1-vllm-execution-boundaries`；补齐 W1 既有反压分层要求。
- **来源与边界**：[Reactive Streams](https://www.reactive-streams.org/)用于解释下游容量反馈与有界缓冲；固定提交的 [Scheduler 准入限制](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L617-L622)只裁决本地 Token／运行槽位限制，不据此推定 API 准入或端到端反压已经实现。
- **学习者证据**：在运行请求限额但入口无限接收的情境中，正确指出压力积在 Scheduler waiting，尚未反馈到前端与客户端；提出等待队列限容、EngineCore 通知前端暂停提交、满载时入口拒绝与容量恢复后重新接收的方案。在客户端立即重试的变式中，正确指出前端仍会承压，需要客户端减少并发并等待后重试。
- **导师补准**：区分后端到前端的反压与入口过载拒绝；前端是否逐请求查询 EngineCore 取决于反馈实现，频繁重试不必然产生查询。该补充不增加新的实现要求。
- **验收结论**：反压概念检查及轻量设计通过，与既有 DP／DPLB 路由和 TP 边界证据合并，完成相应 W1 书面验收；同步请求主链、12 文件索引、协议字段边界和 KV 账本的既有通过记录，不重复验收。
- **后续边界**：W1-P1／P2 仍未启动，未运行负载测试，未修改旧练习契约，未写入 Lesson final mastery，也未记录未提供的学习时长。

<a id="plana-jd-w1-20260915-wrap-up"></a>

#### `plana-jd-w1-20260915-wrap-up`

- **日期与用户要求**：2026-09-15，暂缓 W1 最后两项实践，保存学习断点，整理结构化学习记录与可追溯日志，制作复习卡，同步进度并提交 Git；不推送远端。
- **学习进展**：vLLM 主链、文字复述与变式、C++／Linux 概念基线、19 条 Claim 审计、Conv3D Case Card v1 及反压补充均已完成各自的概念或材料验收。W1 保持 `synthesis`，P1／P2 未启动，不写入 `final_mastery`，不进入 W2。
- **结构化记录**：[C++／Linux 基线](log/2026-09-14-cpp-linux-baseline.md)、[Conv3D 案例证据与反压](log/2026-09-15-conv3d-claim-backpressure.md)。覆盖选定的 210 条可见消息；使用稳定消息 ID 回溯来源，不把导师补充、用户澄清或课堂模拟改写为用户错误或实操证据。
- **复习资料**：[C++／Linux](cards/w1-cpp-linux-baseline.md) 11 张、[Conv3D 证据与反压](cards/conv3d-evidence-backpressure.md) 12 张；对应模板 XLSX 与受管清单均由制卡工具生成。最终 Review 将两份日志中的措辞补准／导师问法纠正改标为“要点”；用户确认后更新卡片来源哈希，问答、ID 和 XLSX 均未改变。两组同请求复核均得到 `operation=no-op`、`would_write=false`，无来源依赖或表格漂移。排除 3 项与旧卡语义重复的候选；只保留可公开的通用机制与证据边界，不制入未确认可披露的项目参数、性能数字或待实践项。未上传墨墨。
- **可追溯可见文本归档**：用户于 2026-09-15 确认按已展示方案保存，已在本机私有目录新建两份 `final` 归档，共 210 条可见消息。重新预览确认选定消息 ID 及其绑定文本均未变化；续段 source SHA 因范围外追加而更新，归档中的元数据记录了保存时的 source SHA。保留所选专有叙述，仅作私存，不代表获准公开披露。

  - 前段：`sl-4f6dbf518ca0461b8f84b8883809211e`，174 条；正文校验值 `visible_content_sha256=76be38d12e103967719218f16fc83980ebf343a66f17fd2c2fa676902f154075`。
  - 续段：`sl-3a8ed1c8e6054d64bee8cf2864d64e4f`，36 条；正文校验值 `visible_content_sha256=05a1da78924b21ebe8c09ef86b2f80fce5e84b35dfb42fde6b13fd0100ab083f`。
  - 两份均保留助手可见过程更新，排除工具事件、推理内容、客户端注入及附件正文；按已确认方案启用凭据和个人标识的可复现脱敏规则，本次替换数为 0，不声称已经匿名化。归档正文与私有路径不进入 Git，源对话未修改。

- **提交授权与范围**：用户再次确认更新来源校验信息并提交；本次范围为相关进度、既有本轮案例与验收增量、两份结构化记录及两组卡片，已提交为 `8ebb655`。本事件随后补记已确认的私有归档回执，不修改结构化记录、卡片或学习状态，不纳入既有未跟踪的 `temp.md`。
- **状态投影与工时**：同步唯一 Checkpoint、临时冲刺计划、README、全局及相关模块进度；未提供本段真实学习时长，不新增工时或课程完成率。不改写主计划、历史周报和旧验收契约。

<a id="plana-study-log-paired-migration-20260915"></a>

#### `plana-study-log-paired-migration-20260915`

- **授权与当前规则**：2026-09-15，用户要求在中央 `.agent-skills` 中改为仓库内导出，并将 PlanA 的三份外置归档迁入，与结构化记录一一对应；不处理 programming-lab。下方是当前原文位置，前一事件和结构化记录头部的“私有归档”及旧 ID 保留为生成时的历史来源，不再表示当前存放位置。
- **配对方式**：结构化文件保持 `推理框架/log/`，原文使用同级 `推理框架/log-raw/` 中的同名文件；原文元数据绑定结构化路径并含相对回链。三份既有结构化文件逐字节不变，避免改变已受管卡片的来源哈希；没有另行改写文章、卡片、学习状态或其他历史日志。

| 结构化记录 | 当前可追溯对话 | 消息数 | 新归档 ID |
|---|---|---:|---|
| [vLLM 全会话复盘](log/2026-09-08-vllm-full-session-review.md) | [同名原文](log-raw/2026-09-08-vllm-full-session-review.md) | 324 | `sl-0eec17119ac5482d9e252bca982279ac` |
| [C++／Linux 基线](log/2026-09-14-cpp-linux-baseline.md) | [同名原文](log-raw/2026-09-14-cpp-linux-baseline.md) | 90 | `sl-df9352532bc9402a9d8e03244e68c95f` |
| [Conv3D 证据与反压](log/2026-09-15-conv3d-claim-backpressure.md) | [同名原文](log-raw/2026-09-15-conv3d-claim-backpressure.md) | 120 | `sl-53e52b881e4d497da2c1bd65b270e8f3` |

- **迁移来源与内容守恒**：旧 `sl-22e6e0a4514b45e3aa993aa12959fc91` 的 324 条对应第一组；旧 `sl-4f6dbf518ca0461b8f84b8883809211e` 按明确边界拆为 90 条与 84 条，后者与旧 `sl-3a8ed1c8e6054d64bee8cf2864d64e4f` 的 36 条拼为第三组。534 个消息 ID 恰好保留一次，角色、时间、phase、正文及原始换行不变；各旧归档的完整元数据、全文 SHA 与分段来源保存在新归档的迁移字段中。
- **校验与披露边界**：三组均通过 `verify-pairs`，新归档均为 `final`；旧文件只在新文件验证完成后移除。迁入仓库是本次明确授权的本地操作，不代表允许公开；本轮不自动 stage、commit 或 push 原文，凭据防护继续有效。
- **落地结果**：三份旧外置归档已移除，新归档保留的消息与来源元数据可逐字节重建旧文件。中央 Skill 已按用户追加授权本地提交为 `dc4631f`，219 项测试与 79 个子测试通过，并完成 PlanA 的技能分发与 `--check` 校验；没有修改 programming-lab 的文件或技能视图。PlanA 的原文、存储说明、迁移回执及子模块指针更新均未暂存、未提交，未推送远端。

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
- **安排**：用户于 2026-09-15 确认暂缓，替代先前暂记的 2026-09-12～2026-09-13 周末安排；恢复时再确认时段，不新增截止日期、自动执行或提醒。
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

<a id="w1-p2-cpp-linux-validation"></a>

#### W1-P2：C++／Linux 基线实践验证

- **状态**：⬜ 待启动；2026-09-14 仅登记候选验证范围，尚未接受正式实践契约、创建实现／测试文件或执行本项测试。
- **目的与依据**：为[基线缺口表](#w1-cpp-linux-baseline-20260914)补实际操作证据；书面通过不自动转成实践通过，也不重复整套概念题。
- **安排**：用户于 2026-09-15 确认暂缓；沿用周末集中实践的偏好，具体日期和范围待明确启动时确认，不新增固定时长、截止日期或自动提醒。

**候选验证内容（启动时选择最低充分范围，不自动叠加为全部必做）**

1. **C++ 生命周期**：用最小 C++17 程序验证已学过的借用、移动、`reset()` 或多态销毁边界，记录编译器告警与 sanitizer／等价工具的适用范围；不把未报告错误当成不存在 UB 的证明。
2. **编译链接与 ELF**：用隔离的目标文件、可执行文件和共享库，核查声明／定义、符号匹配、Section／Segment、`p_filesz`／`p_memsz`；对照预期与实际工具输出，不用课堂模拟数据充当实测。
3. **动态库来源与调用验证**：使用自建可信测试库复现缺库或缺符号，区分 ELF 依赖、当前环境解析与目标 PID 映射；修正实际启动入口后，用新进程的 maps 和原故障函数调用结果共同验证。新开终端不等于继承旧终端环境；只启动成功不等于目标调用已覆盖。

**启动与证据边界**

- 启动前按正式实践流程确认目的、交付、通过标准、文件归属及允许的环境操作；导师准备最小验收工具，学习者保留核心实现和解释任务。
- 另记真实 OS、编译器、标准库、binutils 与所选检查工具版本，不沿用历史 Windows／GPU 配置推断当前环境。不把源码／手册核验记录当作本地工具实测。
- 当前不安装依赖、不修改系统级库搜索配置、不替换真实业务库或重启生产服务；不对不可信二进制执行 `ldd`。未来测试以隔离目录和自建库为范围，具体权限仍在启动时确认。
- W2 的并发生命周期练习仍是后续候选，不因本项登记提前启动；口头要求继续由 W4 及后续 Mock 承接。

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
