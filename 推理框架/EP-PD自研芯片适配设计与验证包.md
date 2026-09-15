# 原设计与验证包：已拆分的兼容入口

本文件不再保存学习进度、技术正文或验收过程。当前内容分工如下：

| 内容 | 新位置 |
|---|---|
| W1 当前完成项、依据和缺项 | [W1 进度](../计划/八周冲刺进度/W1.md) |
| 请求链与接口知识 | [请求生命周期与输出处理](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md) |
| 设备适配知识 | [设备适配边界](深入学习理解vLLM/3-设备适配边界.md) |
| 固定源码与历史环境 | [W1 详细验收记录](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#02-固定源码基线) |
| 练习约定、详细验收和阶段变更历史 | [W1 学习验收记录](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md) |
| 面试主张审计 | [Claim-evidence 矩阵](../面试准备/自我准备/Claim-evidence矩阵.md) |
| 项目案例成果 | [Conv3D Case Card](../面试准备/自我准备/Conv3D-Case-Card.md) |

保留此入口，是为了不改写历史学习日志、原始对话和卡片的来源正文。旧 `:行号` 引用不再对应本页行号，请在 Git 提交 `54489e1` 中查看原完整文件；KV 页大小卡片的来源快照对应 `3edd31d71752c880a5cf2e7e8d95dd2c206d74ee`，SHA-256 为 `3d0c46acd756e1c2283c079e2b4912d0b27e0b5dc13dac85e0e51e66b7fb60d2`。本次未刷新卡片的历史来源，也不把本兼容页作为新知识材料。

## 旧锚点定位

| 旧锚点 | 对应位置 |
|---|---|
| <a id="eppd-自研芯片适配设计与验证包"></a>`eppd-自研芯片适配设计与验证包` | [查看](../计划/八周冲刺进度/W1.md#lesson-plana-jd-w1-vllm-execution-boundaries) |
| <a id="lesson-plana-jd-w1-vllm-execution-boundaries"></a>`lesson-plana-jd-w1-vllm-execution-boundaries` | [查看](../计划/八周冲刺进度/W1.md#lesson-plana-jd-w1-vllm-execution-boundaries) |
| <a id="lesson-状态guide-learning"></a>`lesson-状态guide-learning` | [查看](../计划/八周冲刺进度/W1.md#lesson-plana-jd-w1-vllm-execution-boundaries) |
| <a id="来源与版本锚点"></a>`来源与版本锚点` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#来源与版本锚点) |
| <a id="能力范围与-evidence-目标"></a>`能力范围与-evidence-目标` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#能力范围与-evidence-目标) |
| <a id="已接受练习vllm-整段独立讲解"></a>`已接受练习vllm-整段独立讲解` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#已接受练习vllm-整段独立讲解) |
| <a id="当前-review"></a>`当前-review` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#当前-review) |
| <a id="plana-jd-w1-oral-findings"></a>`plana-jd-w1-oral-findings` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-oral-findings) |
| <a id="当前-findings"></a>`当前-findings` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#当前-findings) |
| <a id="w1-cpp-linux-baseline-20260914"></a>`w1-cpp-linux-baseline-20260914` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-cpp-linux-baseline-20260914) |
| <a id="w1-补充基线clinux-概念与书面校准"></a>`w1-补充基线clinux-概念与书面校准` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-补充基线clinux-概念与书面校准) |
| <a id="w1-claim-evidence-matrix-20260914"></a>`w1-claim-evidence-matrix-20260914` | [查看](../面试准备/自我准备/Claim-evidence矩阵.md#w1-claim-evidence-matrix-20260914) |
| <a id="w1-当前-claim-evidence-矩阵"></a>`w1-当前-claim-evidence-矩阵` | [查看](../面试准备/自我准备/Claim-evidence矩阵.md#w1-claim-evidence-matrix-20260914) |
| <a id="w1-conv3d-case-card-practice-20260914"></a>`w1-conv3d-case-card-practice-20260914` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-conv3d-case-card-practice-20260914) |
| <a id="w1-正式练习conv3d-case-card-v1"></a>`w1-正式练习conv3d-case-card-v1` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-正式练习conv3d-case-card-v1) |
| <a id="w1-conv3d-case-card-findings"></a>`w1-conv3d-case-card-findings` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-conv3d-case-card-findings) |
| <a id="当前-findings-1"></a>`当前-findings-1` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#当前-findings-1) |
| <a id="w1-conv3d-case-card-transfer-1"></a>`w1-conv3d-case-card-transfer-1` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-conv3d-case-card-transfer-1) |
| <a id="a6-独立变式布局容量与另一种分配来源"></a>`a6-独立变式布局容量与另一种分配来源` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#a6-独立变式布局容量与另一种分配来源) |
| <a id="本次练习验收"></a>`本次练习验收` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#本次练习验收) |
| <a id="session-event-索引"></a>`session-event-索引` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#session-event-索引) |
| <a id="plana-jd-w1-20260809-pass-ab"></a>`plana-jd-w1-20260809-pass-ab` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260809-pass-ab) |
| <a id="plana-jd-w1-20260904-pass-c1"></a>`plana-jd-w1-20260904-pass-c1` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260904-pass-c1) |
| <a id="plana-jd-w1-20260904-pass-c2-intake"></a>`plana-jd-w1-20260904-pass-c2-intake` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260904-pass-c2-intake) |
| <a id="plana-jd-w1-20260906-pass-c-synthesis"></a>`plana-jd-w1-20260906-pass-c-synthesis` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260906-pass-c-synthesis) |
| <a id="plana-jd-w1-20260906-pass-d-input-preparation"></a>`plana-jd-w1-20260906-pass-d-input-preparation` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260906-pass-d-input-preparation) |
| <a id="plana-jd-w1-20260906-pass-d-forward-output"></a>`plana-jd-w1-20260906-pass-d-forward-output` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260906-pass-d-forward-output) |
| <a id="plana-jd-w1-20260907-pass-d-synthesis"></a>`plana-jd-w1-20260907-pass-d-synthesis` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260907-pass-d-synthesis) |
| <a id="plana-jd-w1-20260907-pass-e-platform-worker-ops"></a>`plana-jd-w1-20260907-pass-e-platform-worker-ops` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260907-pass-e-platform-worker-ops) |
| <a id="plana-jd-w1-20260907-kv-unit-and-layout"></a>`plana-jd-w1-20260907-kv-unit-and-layout` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260907-kv-unit-and-layout) |
| <a id="plana-jd-w1-20260907-kv-ledger-synthesis"></a>`plana-jd-w1-20260907-kv-ledger-synthesis` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260907-kv-ledger-synthesis) |
| <a id="plana-jd-w1-20260908-oral-review"></a>`plana-jd-w1-20260908-oral-review` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260908-oral-review) |
| <a id="plana-jd-w1-20260908-oral-deferral"></a>`plana-jd-w1-20260908-oral-deferral` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260908-oral-deferral) |
| <a id="plana-jd-w1-20260908-practice-backlog"></a>`plana-jd-w1-20260908-practice-backlog` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260908-practice-backlog) |
| <a id="plana-jd-w1-20260909-kv-page-spec-review"></a>`plana-jd-w1-20260909-kv-page-spec-review` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260909-kv-page-spec-review) |
| <a id="plana-jd-w1-20260914-cpp-linux-baseline"></a>`plana-jd-w1-20260914-cpp-linux-baseline` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260914-cpp-linux-baseline) |
| <a id="plana-jd-w1-20260914-claim-evidence-matrix"></a>`plana-jd-w1-20260914-claim-evidence-matrix` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260914-claim-evidence-matrix) |
| <a id="plana-jd-w1-20260914-conv3d-case-card-accepted"></a>`plana-jd-w1-20260914-conv3d-case-card-accepted` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260914-conv3d-case-card-accepted) |
| <a id="plana-jd-w1-20260914-conv3d-case-card-f1-review"></a>`plana-jd-w1-20260914-conv3d-case-card-f1-review` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260914-conv3d-case-card-f1-review) |
| <a id="plana-jd-w1-20260915-conv3d-diagnosis"></a>`plana-jd-w1-20260915-conv3d-diagnosis` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260915-conv3d-diagnosis) |
| <a id="plana-jd-w1-20260915-backpressure"></a>`plana-jd-w1-20260915-backpressure` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260915-backpressure) |
| <a id="plana-jd-w1-20260915-wrap-up"></a>`plana-jd-w1-20260915-wrap-up` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-jd-w1-20260915-wrap-up) |
| <a id="plana-study-log-paired-migration-20260915"></a>`plana-study-log-paired-migration-20260915` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#plana-study-log-paired-migration-20260915) |
| <a id="0-范围版本与披露边界"></a>`0-范围版本与披露边界` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#0-范围版本与披露边界) |
| <a id="01-审查范围"></a>`01-审查范围` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#01-审查范围) |
| <a id="02-固定源码基线"></a>`02-固定源码基线` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#02-固定源码基线) |
| <a id="当前本地-comparison-baseline2026-08-30"></a>`当前本地-comparison-baseline2026-08-30` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#当前本地-comparison-baseline2026-08-30) |
| <a id="03-计划预算与实际工时边界"></a>`03-计划预算与实际工时边界` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#03-计划预算与实际工时边界) |
| <a id="04-环境与能力-preflight"></a>`04-环境与能力-preflight` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#04-环境与能力-preflight) |
| <a id="05-证据等级"></a>`05-证据等级` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#05-证据等级) |
| <a id="1-w1-d1运行路径指纹与能力矩阵骨架"></a>`1-w1-d1运行路径指纹与能力矩阵骨架` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#1-w1-d1运行路径指纹与能力矩阵骨架) |
| <a id="11-今日要解决的问题"></a>`11-今日要解决的问题` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#11-今日要解决的问题) |
| <a id="12-2026-08-09-启动与-pass-ab-历史记录"></a>`12-2026-08-09-启动与-pass-ab-历史记录` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#12-2026-08-09-启动与-pass-ab-历史记录) |
| <a id="13-运行路径指纹"></a>`13-运行路径指纹` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#13-运行路径指纹) |
| <a id="14-目标芯片能力矩阵骨架"></a>`14-目标芯片能力矩阵骨架` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#14-目标芯片能力矩阵骨架) |
| <a id="15-导师第一轮适配假设暂缓验收"></a>`15-导师第一轮适配假设暂缓验收` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#15-导师第一轮适配假设暂缓验收) |
| <a id="2-架构与-source-map"></a>`2-架构与-source-map` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#request-execution-chain) |
| <a id="20-系统学习顺序"></a>`20-系统学习顺序` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#20-系统学习顺序) |
| <a id="pass-a-1--仓库顶层分类已通过"></a>`pass-a-1--仓库顶层分类已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-a-1--仓库顶层分类已通过) |
| <a id="pass-a-2--vllm-包三圈地图已通过"></a>`pass-a-2--vllm-包三圈地图已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-a-2--vllm-包三圈地图已通过) |
| <a id="pass-a-3--vllmv1-四个主干所有权已通过"></a>`pass-a-3--vllmv1-四个主干所有权已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-a-3--vllmv1-四个主干所有权已通过) |
| <a id="pass-b-1--两条进程边界与三种部署布局已通过"></a>`pass-b-1--两条进程边界与三种部署布局已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-b-1--两条进程边界与三种部署布局已通过) |
| <a id="pass-b-2--一个前端连接多个-enginecore已通过"></a>`pass-b-2--一个前端连接多个-enginecore已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-b-2--一个前端连接多个-enginecore已通过) |
| <a id="pass-b-3--组件状态所有权已通过"></a>`pass-b-3--组件状态所有权已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-b-3--组件状态所有权已通过) |
| <a id="pass-b-4--完整进程图收口已通过"></a>`pass-b-4--完整进程图收口已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-b-4--完整进程图收口已通过) |
| <a id="pass-b-5--worker-与-modelrunner-职责边界已通过"></a>`pass-b-5--worker-与-modelrunner-职责边界已通过` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-b-5--worker-与-modelrunner-职责边界已通过) |
| <a id="pass-ab--阶段材料收口已完成"></a>`pass-ab--阶段材料收口已完成` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#pass-ab--阶段材料收口已完成) |
| <a id="pass-c1-openai-to-engine-core-request"></a>`pass-c1-openai-to-engine-core-request` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#pass-c1-openai-to-engine-core-request) |
| <a id="pass-c-1--openai-请求到-enginecorerequest"></a>`pass-c-1--openai-请求到-enginecorerequest` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#pass-c1-openai-to-engine-core-request) |
| <a id="21-vllm-request-sequence"></a>`21-vllm-request-sequence` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#request-execution-chain) |
| <a id="pass-d-execution-contract"></a>`pass-d-execution-contract` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#pass-d-execution-contract) |
| <a id="pass-d--控制面执行面契约"></a>`pass-d--控制面执行面契约` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#pass-d-execution-contract) |
| <a id="pass-c-source-map"></a>`pass-c-source-map` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#pass-c-source-map) |
| <a id="22-812-文件-source-map"></a>`22-812-文件-source-map` | [查看](深入学习理解vLLM/2-Request-Lifecycle-and-Output.md#pass-c-source-map) |
| <a id="23-vllm-eppd-主图"></a>`23-vllm-eppd-主图` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#7-w2moe-ep并行策略与-c-系统基础) |
| <a id="24-sglangatom-边界对照"></a>`24-sglangatom-边界对照` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#63-资料边界) |
| <a id="3-适配设计"></a>`3-适配设计` | [查看](深入学习理解vLLM/3-设备适配边界.md#pass-e-adaptation-matrix) |
| <a id="pass-e-adaptation-matrix"></a>`pass-e-adaptation-matrix` | [查看](深入学习理解vLLM/3-设备适配边界.md#pass-e-adaptation-matrix) |
| <a id="31-六层适配矩阵"></a>`31-六层适配矩阵` | [查看](深入学习理解vLLM/3-设备适配边界.md#pass-e-adaptation-matrix) |
| <a id="32-既有经验迁移矩阵"></a>`32-既有经验迁移矩阵` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#11-w6amd-rocmhiprccl-迁移与上游工件) |
| <a id="33-c1c5-change-cards"></a>`33-c1c5-change-cards` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#43-change-card-模板) |
| <a id="4-验证与证据"></a>`4-验证与证据` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#9-w4定量性能案例证据与第一次面试闭环) |
| <a id="41-correctness-与-failure-matrix"></a>`41-correctness-与-failure-matrix` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#8-w3pdkv-生命周期与-rdma) |
| <a id="42-分阶段-bring-up"></a>`42-分阶段-bring-up` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#11-w6amd-rocmhiprccl-迁移与上游工件) |
| <a id="43-benchmark-protocol"></a>`43-benchmark-protocol` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#9-w4定量性能案例证据与第一次面试闭环) |
| <a id="44-结果与待验证项"></a>`44-结果与待验证项` | [查看](../计划/八周冲刺进度/W1.md#还缺哪些没完成) |
| <a id="45-待做实践作业"></a>`45-待做实践作业` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#45-待做实践作业) |
| <a id="w1-p1-runtime-output-validation"></a>`w1-p1-runtime-output-validation` | [查看](../计划/八周冲刺进度/W1.md#w1-p1-runtime-output-validation) |
| <a id="w1-p1运行路径选择与最小输出契约验证"></a>`w1-p1运行路径选择与最小输出契约验证` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-p1运行路径选择与最小输出契约验证) |
| <a id="w1-p2-cpp-linux-validation"></a>`w1-p2-cpp-linux-validation` | [查看](../计划/八周冲刺进度/W1.md#w1-p2-cpp-linux-validation) |
| <a id="w1-p2clinux-基线实践验证"></a>`w1-p2clinux-基线实践验证` | [查看](../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-p2clinux-基线实践验证) |
| <a id="5-risk-register"></a>`5-risk-register` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#32-诊断出的-p0p1-缺口) |
| <a id="6-upstream-validation-anchor"></a>`6-upstream-validation-anchor` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#upstream-u1-dense-dp) |
| <a id="61--候选-u1dense-internal-dp-实时队列统计链缺口"></a>`61--候选-u1dense-internal-dp-实时队列统计链缺口` | [查看](../计划/高级AI框架开发工程师-八周证据冲刺计划.md#upstream-u1-dense-dp) |
