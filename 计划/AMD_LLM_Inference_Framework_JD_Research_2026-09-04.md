# AMD 大模型推理框架工程师：JD 深度研究与面试准备手册

> 研究日期：2026-11-09<br>
> 文档用途：岗位判断、投递定位、技术复习、面试准备、开源贡献、与招聘方沟通<br>
> 研究对象：用户提供的“AMD 大模型推理框架工程师”非正式内推截图<br>
> 个人化依据：自研芯片 ProcessGroupDLCCL 适配及执行流调整；PyTorch C++ Extension、集合通信、vLLM custom allreduce 接入既有通信算子、CUDA 算子与性能调试。本期任务说明新增列出 CUDA IPC；在缺少具体实现范围前，本手册只把它作为待梳理经历，不自动扩写为独立设计过 IPC transport 或通信 kernel。LMCache 重新适配处于计划阶段；学习、推断与个人已完成成果严格分开。

---

## 版本更新记录

| 版本日期 | 更新性质 | 主要内容 |
|---|---|---|
| 2026-11-09 | 第 11 版：新增上海 Req 96120/96121、四项目 release 与 P/D/KV 生命周期更新 | 完整读取第 10 版 2,662 行、284,569 字节。岗位侧从 AMD 官方 Careers 新确认上海 **AI Framework and Performance Experts(vLLM)（Req 96120）** 与 **AI Software Development Eng.（Req 96121）**；两页均为 existing vacancy，官方 `datePosted` 未稳定取得，故记录为“本期新确认开放”而非“本周新发布”。94065、89635、89393、89499 等仍可从官方页面/索引取得，未确认中国 remote、重新开放或正式关闭。项目侧：Infera v0.3.3、MoRI v1.2.5、ATOM v0.1.9 已发布；LMCache 出现 ROCm 7.2.4/torch 2.10 的 v0.5.7rc4 变体和 11-08 nightly，均按 RC/夜版处理。SGLang #49156 已把 Mooncake KV registration 失败改为启动失败；MORI #915 非合并关闭并由 #907 的完整 WR quiescence 方向承接；ATOM #3068–#3070、vLLM #66008/#66268 与 SGLang #49205 仍为有作者推进的 Open/Draft，不写成 release 能力。第 19 节更新正式上游、贡献规则草案、CPU/AMD GPU/多卡/RDMA 边界与首选三项；未发布 issue、评论或 PR。 |
| 2026-11-02 | 第 10 版：新增上海岗位、Infera release、MoRI EPv2 与可模拟数据面 | 完整读取第 9 版 2,539 行、260,538 字节。岗位侧从 AMD 官方 Careers 新确认上海 **AI framework Eng.（Req 94065）**、**GPU Kernel Performance Engineer（Req 96117）**，并补录 **AI Optimization Engineer（Req 89635）**；三者官方页面均显示 existing vacancy，但官方发布日期未稳定取得，故写作“本期新确认/新发现”，不冒充“本周新发布”。94063、89393、89499、92012 等仍可检索；未确认中国 remote、重新开放或正式关闭。项目侧：Infera v0.3.1/v0.3.2 已发布，#210/#214 及一组 projector/UMBP 模型进入 main；MORI #823/#831/#836/#843/#851/#862/#866/#867 等合入，新增无 GPU/NIC 的 IO/UMBP 模拟入口；vLLM #61361 MoRI EPv2 与 #63142/#63628 已合入，#61109/#61119/#64428 仍在评审；ATOM 最新 release 仍 v0.1.8，#2634 RFC/#2630 Draft 未推进，出现 P/D/前缀缓存/cudagraph 新问题；AIC 主要是 CI、wheel、benchmark 增量。第 19 节据此把首选三项调整为 MORI 模拟回归、W7900 HIP 证据包、自研芯片 LMCache 闭环；未发布 issue、评论或 PR。 |
| 2026-10-26 | 第 9 版：新增上海 Req 94063、Q4 roadmap 与分层 KV/故障语义更新 | 完整读取第 8 版 2,417 行。AMD 官方 Careers 索引新增上海 AI Framework Engineer **Req 94063**，当前可检索；官方 `datePosted` 未稳定取得，不把第三方首次发现时间冒充发布日期，也不把它视为 89499 的重开或替代。既有 89393、89398、89499、92012、89497 仍可从官方索引取得；其它旧 Req 搜索缺失不推断关闭。项目侧：ATOM v0.1.8 发布；Infera #198/#209 入 main，而 #210/#214 仍 Open，且 v0.3.1 尚未形成公开 release；SGLang 新增 2026 Q4 AMD roadmap，UMBP、MoRI-EP v2、MI45x P/D 仍是目标而非已交付能力；MORI #788/#821/#838 等入 main，#823/#825/#831/#836 仍由既有作者推进；vLLM #61361/#63142/#63628、ATOM #2634/#2630 均为在研。10-20 AMD megakernel 文章的可用/preview/planned 矩阵及个人 fork 边界已补入。第 19 节刷新贡献机会与首选三项，未对外发布任何内容。 |
| 2026-10-19 | 第 8 版：例行核验、release 基线与 KV 生命周期更新 | 完整读取第 7 版 2,201 行。未确认本周新发布、重开或正式关闭的中国/中国可远程目标工程岗；92012 当前官方索引标题明确为 Senior AI Model Quantization Engineer，不能确定改名日期；补充美国产品岗 87223 为相邻旁证而非技术投递主线，91704 的 remote 仍限定欧洲列明国家。LMCache v0.5.6 于 10-14 UTC 发布，确认包含 #5157；补记安全公告与 ABI/架构边界。MORI #711/#718/#731、ATOM #2464、SGLang #43719/#43723 已合并；ATOM #2459 非合并关闭，MORI #621 早在 09-30 已合并，本期纠正遗漏。Infera #185/#186 已入 main，但 #203 仅合入开发分支；MORI 新增本地读 hold、SSD 分段暂存与 demotion retry，vLLM 增加受限 hybrid WRITE/DSpark 和 communicator 退出清理。第 19 节逐项刷新状态、作者、日期、门槛及首选三项；ROCTX 补测仍由既有作者推进。新增 gfx1100 RDNA GEMM 进阶阅读，不扩大七天必做范围。 |
| 2026-10-12 | 第 7 版：例行核验、完成语义落地与外部贡献重排 | 完整比较第 6 版。岗位侧未发现新的中国或可从中国远程申请 exact Req；92727、89393、89398、89499、87545、92012、78999 等仍可从 AMD 官方职位页/索引取得正文，89764 仍可检索但继续是美国 Hybrid 且无签证赞助；未重获同等证据的旧 Req 保留最后确认状态，不把搜索缺失写成关闭。项目侧：LMCache #5157 于 10-08 合并，纠正旧版“仍 Open”；Infera #183、MORI #716/#729、ATOM #2518、LMCache #5565/#5611、AIC #177 均已合并，分别补强指标联邦、peer failure、VMM/RDMA 释放、MP lookup 锁生命周期、ROCm/SGLang 设备抽象与 CPU emulation 趋势发布。新增核验 vLLM #61109/#61119 与 SGLang #43719/#43723：均为已有作者推进的 Open/Draft 工作，不当作新手空白题。第 19 节据此把首选三项收敛为可独立完成的 W7900/HIP 证据包、LMCache 设备后端闭环和 MORI 故障语义评审式学习。 |
| 2026-10-05 | 第 6 版：例行核验、岗位线索转实证与分层 KV 双路线 | 完整比较第 5 版。官方职位正文重新可检索：确认上海 92727 与 San Jose 89764 为 existing vacancy；89393、89398、89499、87545、92012 也再次出现可申请正文，旧岗位未能逐条取得同等证据的仍保留最后确认状态。Infera 当前 README 已公开 v0.1.1 镜像、Anthropic API、drain/rollout 实测与 AIC tiering 组合，但仍明确没有 autoscaler；MORI #717/#718、Infera #179、ATOM #2459/#2464 均在评审，不写成已发布能力。第 19 节更新 Infera issue 创建限制、AIC #177/#178 状态，并将 LMCache/ATOM 分层 KV 方案纳入学习主线。 |
| 2026-09-28 | 第 5 版：例行核验、生命周期进展与 W7900 准备路线 | 完整比较第 4 版。岗位正文/API 本期访问受限，13 条旧岗位保留 09-21 最后确认状态；92727、91704、89764 仅列新检索线索，不计已确认新发布/开放。Infera roadmap 09-24 更新，#173/#176 已合并；MORI #656/#709 合并、#711 在评审；ATOM #2167/#2339 补强源块保留与保存依赖，#2351 修复 ATOMesh 负载统计；SGLang #40645/#41023/#41402 已合并且 MoRI 不在默认 ACK 延迟释放范围。加入 W7900 本地/实机分离路线、LMCache #5075 补测与贡献权限新快照。 |
| 2026-09-21 | 第 4 版：例行核验、状态纠正与 LMCache 准备主线 | 官方 API 补充中国相邻职位；89498 当前地点为北京，纠正旧表“全在上海”；89395 多次 404 且搜索无结果，列为页面下架/申请不可用待确认，不推断招满。MORI #665/#652 合并；AIC #147 非合并关闭，#166 准确率门禁合入；ATOM #2315 回滚涉及 PD/卸载的 #2154。LMCache #4957 迁移设备目录，#5157 仍 Open 且已有批准。撤回无依据匹配百分比及 CUDA IPC/通信 kernel 实做表述，将自研芯片 LMCache 适配设为准备主线。详见 3.8、5.8、8、15、19。 |
| 2026-09-14 | 例行更新：岗位、代码里程碑与贡献清单纠正 | 上海 6 条既有岗位仍可申请；新增收录 09-10 发布的 San Jose GPU Fleet Management 岗位 Req 92051（Hybrid、无签证赞助，不能视为中国远程机会）。InferaSim、MORI UMBP 重构/EP v2 preview、AIC emulation 与 vLLM 弹性 EP 修复已合入。MORI #626 已有 #653 合并修复，移出待认领；AIC #150 关闭但未合并，功能由 #154 合入；SGLang timeout/abort 已有 #38164/#38704/#38961 等推进，纠正“空白新提案”定位。更新第 19 节优先三项、验证限制和来源 S52–S64。 |
| 2026-09-07 | 外部贡献专题增补与事实修正 | 新增第 19 节：Infera、MORI、AIC、SGLang/vLLM upstream 的贡献规则、10 个具体参与切口、硬件门槛、重复任务排除和两周路线。补充核验确认 AIC #139/#151 于 09-06 合并，**纠正上一版本“项目侧本期未发现实质变化”的结论**。另将 Infera #88、MORI #507/#557 等 Open issue 与实际 PR 进度交叉对照；这些较早合入属于本期新核验证据，不称作本周新发布。 |
| 2026-09-07 | 例行监测更新 | **当时记录：岗位侧有新增发现，项目侧未发现实质变化；后者已由同日专题增补纠正，见上行。** 新增核验 5 条此前未收入手册的上海官方相邻岗位：Req 87545、89395、89498、89499、89500；复核既有 Req 89398 仍开放。上述岗位均早于 2026-09-04 发布，因此应理解为“本期新发现”，不能表述为“本周新发布”。Infera、MORI、AIC 及三份 roadmap 未发现 9 月 4 日后的已确认里程碑变化。 |
| 2026-09-04 | 初版 | 完成截图 JD 复原、AMD 分布式推理项目地图、证据分级、个人匹配分析、学习路线、面试题纲与来源索引。 |

### 本期检查范围与结论

- **本期比较基线：** 完整读取 2026-11-02 第 10 版（2,662 行、284,569 字节），检查截至 2026-11-09（北京时间）；GitHub 日期采用 UTC。当前结论以 **3.15、8.12、15.10、19.18** 为准，旧台账均为历史快照。
- **岗位：** AMD 官方 Careers 本期新确认上海 **AI Framework and Performance Experts(vLLM)（Req 96120）** 与 **AI Software Development Eng.（Req 96121）**；两者均为独立 Req、页面显示 existing vacancy，但官方发布日期仍待确认。94065、89635、89393、89499 等仍可取得官方正文或索引；96117 沿用 11-02 最后确认，不以本期搜索缺失推断关闭。本期未确认中国 remote、重新开放或正式关闭。[S189][S190]
- **已发布变化：** Infera v0.3.3（11-02）、MoRI v1.2.5（11-06）、ATOM v0.1.9（11-02）形成新 release 基线；LMCache v0.5.7rc4 ROCm 变体与 `nightly-rocm` 更新提供更明确的 ROCm/torch/架构组合，但 RC 与 nightly 都不是稳定生产承诺。[S191][S193][S199][S209][S210]
- **上游状态：** SGLang #49156 已合入并让 Mooncake registration 失败在启动时显式失败；MORI #915 非合并关闭，完整 WR quiescence 方向由仍 Open 的 #907 推进；ATOM #3068–#3070、vLLM #66008/#66268、SGLang #49205、LMCache #6401/#6411/#6421 均仍有作者推进，不能从作者 benchmark 或 Draft 推成 release/生产能力。[S194][S195][S201]–[S207][S212]–[S214]
- **成熟度边界：** Infera #233 的 SGLang/ROCm 10.3 预览纠正了 disaggregated decode 兼容性，但验证仍是特定 MI355X/镜像且残留有限错误；LMCache #6358 已合入 VMM shared-KV sleep mode，现有证据来自 H200/CUDA，不代表 ROCm 已验证。AIC 本期是 CI/夜版 benchmark 调整，没有确认新的数据面里程碑。[S192][S211][S215]
- **个人准备：** 96120 将 distributed runtime、TP/PP/EP、KV、RCCL/RDMA、AITER/HIPBLAS-LT 与 upstream 写在同一职位里，成为最直接第一优先；96121 更偏框架与 kernel 联调。个人叙事继续以 ProcessGroupDLCCL、C++ Extension、集合通信、custom allreduce 调用链和性能定位为事实核心；CUDA IPC 仍需按实际句柄、映射、ownership 与异常回收范围校准。首选准备为 MORI 模拟/完成语义证据包 → W7900 HIP/ROCTX → KV 生命周期与 custom-allreduce 源码评审包。[S189][S190][S194][S198][S206][S207]
- **执行与证据边界：** 本次未运行 GPU/CPU 项目测试、未连接 W7900、未申请职位、未发布 issue/评论/PR。作者 benchmark、CI、main、release、preview 和本研究独立复现继续分开；未经用户授权不对外写入。

#### 上期检查摘要（2026-10-19，历史）

- 当期未确认新的中国/中国可远程目标工程 Req；92012 标题明确为模型量化，91704 remote 仍限欧洲列明国家。
- LMCache v0.5.6、MORI #711/#718/#731、ATOM #2464、SGLang #43719/#43723 等状态已按合并字段纠正；Infera #203 只入开发分支。
- 准备主线为 W7900 生命周期证据包、自研芯片 LMCache 闭环与故障完成语义；ROCTX #5075 是已有作者补测，不是空白任务。

#### 上期检查摘要（2026-10-12，历史）

- **比较基线：** 完整读取 2026-10-05 第 6 版，共 2,073 行。检查截至 2026-10-12（北京时间）；GitHub 日期采用 UTC。历史快照继续保留，当前判断以 3.11、15.6、19.14 为准。
- **岗位：** 搜索 AMD 官方 Careers 的中国、美国相邻与 remote 方向。未发现新的中国或可从中国远程申请 exact Req，也未确认重新开放或正式关闭。92727、89393、89398、89499、87545、92012、78999 仍能从官方页面/索引取得正文；89764 仍可检索，但仍是 San Jose Hybrid 且无签证赞助。89500、89498 等本期未重获同等强度正文，不据搜索缺失推断关闭。[S122]
- **项目：** LMCache #5157 已于 10-08 合并；Infera #183、MORI #716/#729、ATOM #2518、LMCache #5565/#5611、AIC #177 也已合并。它们把“同步正确对象、peer failure、VMM 注册释放、异步 lookup 锁回收、HIP 错误清理、设备能力判断、CPU emulation 趋势发布”从讨论推进到主分实现；仍不等于所有 connector、拓扑和错误路径已生产验证。[S123]–[S128][S133]
- **在研路线：** Infera #179、MORI #711/#717/#718/#731、AIC #183、ATOM #2459/#2464、LMCache #5075/#5133、vLLM #61109/#61119、SGLang #43719/#43723 均有现成作者且仍 Open/Draft；其中 #5075 当前 19/29 checks、无 reviewer，适合 W7900 ROCTX 补测，但不是待从零实现；#731 是故障注入基础设施，不是已经解决所有 RDMA hang；vLLM/SGLang 新 PR 更适合作为通信与失败语义学习案例。[S129]–[S135]
- **个人化：** 准备主线继续是“W7900 HIP 数据通路 → 自研芯片 LMCache 闭环 → 通信故障/完成语义”。新合入内容为面试提供了更直接的源码案例：`enqueue != complete`、liveness 不能恒真、deregister 后仍可能泄漏、lookup 结果未消费也必须释放锁。
- **验证边界：** 本次未连接 W7900、未运行项目测试、未申请职位、未对外发布 issue/评论/PR。作者报告、CI、合并记录、release 与独立生产验证继续分开；官方搜索结果能证明页面当前可检索/申请时才写“开放”，发布日期缺失则明确待确认。

---

## 0. 最终结论

### 0.1 是否值得申请

**值得，而且建议尽快申请。**

这不是普通的“模型适配工程师”或单机推理算子岗位，而是位于以下四层交界处的核心系统岗位：

1. 集群级推理调度与路由控制面；
2. 全局、分层、跨节点的 KV Cache 控制面与数据面；
3. vLLM / SGLang 推理运行时；
4. ROCm、MORI、RCCL、AITER 等 GPU 通信与算子栈。

按用户最新澄清，改用证据强弱而非无依据百分比：

| 方向 | 当前可证明的基础 | 尚缺的证据 |
|---|---|---|
| PyTorch / vLLM 通信接口集成 | ProcessGroupDLCCL 适配、执行流调整；custom allreduce 直接接入既有通信算子 | 应补可展示的调用链、同步契约、正确性回归与真实性能对照 |
| KV Cache connector / 卸载 | 与已有框架适配有可迁移交集；计划重新适配 LMCache | 尚无本次适配完成、真实命中、异步正确性或端到端收益的结果 |
| MORI-EP / RDMA / GPU 通信 kernel | 已有集合通信上层集成背景，可以学习接口和完成语义 | 不等于实现过 EP dispatch/combine、RDMA transport 或 IPC；用户明确没有 CUDA IPC 经历 |
| Rust / 集群控制面 | 本手册提供架构与源码学习路线 | 生产 Rust、SLO 自适应调度、大规模在线集群经验未证实 |

**撤回旧版 55%–75% 等匹配估计。** 能否达到具体级别还需年限、学历、独立负责范围和测量结果，不能用项目关键词替代。建议以“推理框架与通信后端集成”申请匹配级别，资深全栈/EP kernel 岗位视作冲刺，不包装成现成专家。


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

**2026-09-28 当前状态补充：** #173/#176 与 09-24 roadmap 已确认基础缩放/安全 rollout 和 P/D lifecycle 加固，负载驱动策略与 runtime 角色切换仍未交付。详见 3.9；上面的早期状态不能解读为今天仍无安全 rollout。[S90]

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
- 09-14 历史基线为 ROCm 7.14.1、vLLM 0.28.0、LMCache 0.5.4、NIXL 1.4.1。**09-21 当前 README 为 vLLM 0.29.0、LMCache 0.5.5、AITER 0.1.22.post1**，PyTorch release/2.13 与 AITER 明确 source build，旧 wheel/source 描述问题已修正。#166 新增 accuracy gate；#168 拆分构建层。版本与测试更新不改变 preview 性质。[S9][S58][S69][S70]
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

### 3.7 上期技术变化台账（2026-09-07 至 2026-09-14，历史快照）

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

### 3.8 上期技术变化台账（2026-09-14 至 2026-09-21，历史快照）

以下合并日期均为 UTC；代码能力只对所述路径成立。测试数字与性能描述来自作者报告，本研究未独立复现。

| 项目 / 事件 | 已确认变化 | 成熟度与岗位准备影响 |
|---|---|---|
| Infera #171，09-16 合并 | 测得的 serving anchor 可用于不同并行宽度；修正 prefill 曲线外推；P/D 搜索与仿真按两个池分别计费，并计入 KV handoff | 是容量模拟和推荐改进，不是线上 autoscaler。README 仍明确没有 scaling controller；不要把模拟预测当 GPU 实测。[S66] |
| Infera #148，09-16 合并 | 兼容矩阵新增 ROCm 10.1 条目 | 具体引擎/镜像组合逐项查矩阵，不能理解为所有路径已完成生产验证。[Infera #148](https://github.com/AMD-AGI/Infera/pull/148) |
| MORI #665，09-14 合并 | 统一 warmup 与正式计时的 tensor 引用寿命，避免 allocator 新分配污染 combine 测量 | 已解决学习案例，撤下“待评审优化”。作者在 2×8 MI308X 测量；CPU 只能解释引用/分配模型。[S64] |
| MORI #652，09-20 合并 | AllGather SDMA 增加 graph-capture 路径；完成 generation 移到 device 推导，并增强跨 GPU 可见性；新增 replay 测试 | 不是移除 sync 就能获得 overlap：回放计数与 system-scope 顺序也是契约。适合作为执行流适配的进阶学习，不是用户已有 IPC/kernel 经验。[S67] |
| MORI #662，09-17 合并 | 增加 GEMM + CCO SDMA allreduce 融合，提供支持条件与构造自检 | 专门形状/硬件/构建选项下的能力；`BUILD_CCO_SDMA=ON` 很重要。不能泛化为替代 RCCL 的完整通用实现。[S86] |
| MORI #679 → #687，09-17 合入、09-18 回滚 | UMBP 匿名 DRAM tier 的 transparent hugepage 提示被回滚 | 当前不能把 #679 记为持续可用优化；回滚正文未说明充分原因，不推断性能或正确性根因。[S68] |
| AIC #147 → #166，09-16 关闭旧 PR、09-17 合并新方案 | 差分 lm_eval/gsm8k、基线负对照、tier 命中计数、重启后复测进入代码与 CI 工作流 | 撤回“accuracy 尚未接入 CI”的当前描述；旧评论保留为历史。测试门禁增加不等于任意 KV 逐字节一致性或生产认证。[S69] |
| AIC #160/#168，09-15/09-18 合并 | README 同步 PyTorch/AITER 来源；构建拆为 base/vLLM/LMCache；当前 README 为 vLLM 0.29.0、LMCache 0.5.5、AITER 0.1.22.post1 | 旧“修 README 的 wheel/source 矛盾”不再作为空白任务。`docker/Dockerfile` 当前仍存在，不能照 #168 早期正文断言已经删除。整体仍明示不推荐生产负载。[S70][S88] |
| ATOM #2223，09-15 合并 | 修复多 rank completion 轮询丢失；新增默认关闭的 pinned async copy 与 block-ID 批量准备控制 | 作者单独打开 async copy 的那组反而更慢；组合收益来自限定模型/8×MI355X/单次各组实验。非常适合学习“异步≠必然更快”，不照搬收益数字。[S71] |
| ATOM #2284，09-20 合并 | vLLM 插件侧精确保护仍被 save 读取的 blocks，释放其余 request blocks；修复特定 index dtype/投机形状问题 | source-safe completion 身份尚未完整跨 worker→scheduler 传递。作者拒绝把不满足 cache value gate 的对照解释为 throughput 胜利；不能描述成已完成提前回收闭环。[S72] |
| ATOM #2154 → #2315，09-18 合入、09-20 回滚 | Kimi-K3 P/D 等更改因 V4 DPA + draft hang 整体回滚，连带撤回部分 listener readiness 与 async save fencing | **风险提示：** 回滚后的完整 GPU 验证仍待完成；不能继续把撤回功能列为 main 当前支持，也不能推断所有 PD 都失效。[S73] |
| vLLM #57160，09-18 合并 | ROCm native CPU KV offload 改用每 rank 私有 pinned tensor，绕开共享 mmap 整段注册问题 | 不再享有该共享区复制 KV 去重；属于 vLLM native backend，不是 LMCache 修复。为自研芯片选内存模型提供对照。[S74] |
| vLLM #51052，09-20 合并 | MoRIIO READ 搬运 hybrid attention + Mamba/KDA recurrent state，并等待所有 transfer status | 限等 P/D TP、READ、无 speculation；Hybrid WRITE、异构 TP、请求级 HMA recovery 不在范围。作者实机验证不能扩成全模型保证。[S75] |
| SGLang #39763/#39910，09-16/09-17 合并 | MORI intranode grid 按设备 CU 数限制；允许 MORI + DSpark + DP attention 的特定静态 verify 路径 | 前者 full serving 验证在 PR 中仍标进行中；后者是门禁放行及特定模型/MI355X 报告，不代表所有 EP/DSpark 组合。[S76][S87] |
| LMCache #4957，09-19 合并 | 内置 device 实现迁至 `lmcache/v1/platform/devices/<backend>/`，测试与设计文档同步迁移 | 重新适配应固定 commit，并以当前设备目录和插件接口为准，不继续沿旧 MUSA 目录照搬。[S77][S79] |

**官方文章本期检查：** ROCm 官方 Atom feed 有 09-14 至 09-17 新文；重点完整读取 09-17 MLPerf v6.1 技术详解与 09-15 Thread Trace Part 1。前者说明 SGLang/MORI-EP 的 shared-expert 融合、按 token 负载调度和 phase 对齐，说明框架调度与通信性能确实关联；它是指定基准栈的报告，不证明截图组织归属，也不使 AIC 自动达到相同成熟度。后者可加入 ROCm 性能诊断学习清单。旧 08-24 长上下文文章本期复查，不称为本周新文。[S81][S82]

**本期判断：** 项目关联仍属强关联推断，未得到截图 exact Req。准备优先级从“直接写 EP/RDMA kernel”调整为“框架接口 → KV 正确性与缓存价值测量 → 有证据的异步优化”，与用户真实经历和 LMCache 重启计划更接近。

---

### 3.9 本期技术变化台账（2026-09-21 至 2026-09-28）

下表事实来自 PR 合并字段、正文及重点当前源码；作者的实验不作为本研究独立复现。仍在评审的方案单列。

| 项目 / 事件（UTC） | 已确认事实与当前能力 | 验证边界、岗位与准备影响 |
|---|---|---|
| **Infera #173 / #176；09-23 / 09-24 合并** | P/D 注册前的 KV probe、启动等待与退出/取消链路加强；worker 增加注册后的 readiness，默认有相应探针的 Deployment 先起新副本，再退旧副本 | #173 正文仍是未填写模板，因此能力判断另外核对文件和 09-24 roadmap。#176 作者报告 live 1P1D 91 次采样未出现任一角色 Ready 数为零；这不证明所有拓扑零中断。无额外 GPU 会停在 Pending，旧 worker 继续服务；skipReadinessProbe 与多节点 LWS 有不同边界。[S90] |
| **Infera roadmap #9；09-24 更新** | 将 P/D reliability 标为 shipped/hardening，API/ratio/replica scaling + 安全 rollout 标为 delivered/hardening；#174/#175/#177 模拟成本修正仍在 review | **负载驱动策略、运行时 P/D 角色切换、32+ GPU 实例、组合 L3+L4、多 worker 共享 prefill cache、SLO/goodput 仍是后续工作。** 不再笼统说“扩缩容全未实现”，也不将 rollout 当自动弹性。[S90] |
| **MORI #656；09-24 合并** | distributed ranged read 增加可选 scratch sharding，以注册区域基址+偏移描述源/目的来减少碎片计划，批量获取注册锁，并细分计时 | sharding 默认关闭；作者是同主机两个服务 + NIC loopback，不是两台机器；优化首次远端读不等于整负载相同比例加速，累计计时要差分取稳态。适合学习“搬运慢可能是锁与 plan 构造”。[S91] |
| **MORI #709；09-24 合并** | EPv2 wide barrier 改为最后到达块清零，避免其他块错过短暂的 gridDim.x 值后永久等待 | PR 中 EP128 多节点与 EP8 回归仍未勾选；合并不证明完成这些验证。W7900 单卡不能承担原场景验收。[S92] |
| **MORI #711；09-24 创建、09-27 更新，Open** | 已有作者 yoqiu-amd 提交 SDMA device-post 两类死锁补丁：多队列发布与 commit snapshot；正文报告 gfx942/gfx950 并发测量 | 非待认领白纸；队列跨 communicator 共享的语义值得阅读。底层可见性机理在正文也有作者未确认部分，不将推测写成硬件规范。适合作为后续多卡评审，非本周 W7900 必做。[S93] |
| **ATOM #2167；09-22 合并** | send/save completion 分别上报，由 scheduler-side `should_defer_free()` 决定源块保留；增加 `source_blocks_released` 清理并考虑 TP/PP 聚合、超时与请求 ID 复用 | 当前 MultiConnector 限至多一个 producer/send 和一个 offload；不能由此推出任意嵌套 connector 完成身份都已解决。旧版“完成/回收尚未打通”的笼统表述应收窄到具体路径。[S94] |
| **ATOM #2339；09-25 合并** | dense LMCache save 把 producer event 传至实际 pack stream，正常路径用 stream wait；失败保存的 frontier 与重试也作处理 | current main 的 connector 已见 producer event wait。作者实机报告涉及 MI350X/LMCache 0.4.5 与特定 head；GPU smoke 早于最终 rebase，最终 head 另有 CPU 检查。仅确认 dense 保存依赖重新引入，**不称 #2154 回滚的全部 K3 P/D 功能已恢复**。[S95] |
| **ATOM #2268 / #2305；09-23 合并** | vLLM plugin 增加 K3 MLA+KDA 联合命中/状态恢复路径；共享 dense offload scheduler memoize 同一 sequence/HBM frontier 的 lookup，避免 KV 满时每步重复哈希 | #2268 针对 pin 的 vLLM 0.28，要求 align、chunk 对齐和 recompute 策略；作者每性能点 n=1、未声称准确率评估。#2305 不覆盖另一个 DSV4 scheduler。不能说“线性状态不再需要缓存管理”。[S96] |
| **ATOMesh #2351；09-22 合并** | streaming P/D 在 dispatch 前占用负载；P 响应结束释放 P，D 保留到输出结束/断开，并修正双派发失败取消 | 作者验证为 CPU HTTP/Rust 测试，未重测 GPU throughput；是负载记账修复，不是已量化吞吐提升。是更适合无卡阅读的 Rust 生命周期案例。[S97] |
| **SGLang #40645 / #41023 / #41402；09-22 / 09-24 / 09-27 合并** | 保留 drain ACK；默认启用支持 backend 的 decode 延迟释放；ACK 扇出到同 room 所有 decode peers，先 arm tracker 再发送 ABORT，并保留 teardown 前快照 | 当前只 Mooncake/NIXL 等 opt-in 路径；**MoRI/fake 不启用这条延迟释放路径**。30s timeout 是保留上限，不能凭到期推出远端写入必定停止。#38961 所列多目标 ACK/部分跟踪问题已有新合入，不再原样认领；其它 shared failure/source ownership 仍逐项核对。[S98] |
| **vLLM #58098 / #58566；09-23 / 09-25 合并** | ROCm 增加受限 BF16 AsyncTP fusion；skinny GEMM 把 `.contiguous()` 移到真正使用它的分支 | 前者含双卡数值/模型作者报告，限制 BF16 与显式 sequence-parallel 阈值；后者 main 已见改动。小拷贝移除数字来自特定 K3/8×MI355X workload，不外推 W7900 端到端收益。[S99] |
| **AIC #176/#173；09-22/09-25 合并；#177/#178 仍 Open** | 构建可读取 LMCache PR manifest；SPUR CI 要求至少申请一块 GPU；新增评审中 CPU emulate 报表和 gfx1250 VM/compose 测试方案 | 读取 PR head 的镜像不等于采用稳定发布。#178 仍有上游 blocker、多个验收项未勾选；QEMU/emulation 不是真实 GPU 性能。README 仍 early-access、不推荐 production。[S100] |

**Roadmap 与归属：** MORI #348 最后更新时间仍 06-15；SGLang AMD #35003 仍 08-18。主分支持续前进，旧 roadmap 的“planned”不能覆盖已有实现。新增 Infera/ATOM/SGLang 生命周期代码强化截图与分布式推理技术族的 **B 级强关联推断**；exact Req、汇报线与实际负责模块仍是 **C 级待招聘方确认**。

**官方文章 / 文档本期变化：**

- 09-21 Hyperloom 文章，09-24 有正文更新：公开跨 vLLM/SGLang/xDiT 的测量—优化—复验流程。其收益数字是官方特定实验报告，不是岗位归属证明或用户可复现承诺。对你最有价值的是固定 workload、端到端重测和保留负结果的方法。[S101]
- 09-22 Kimi-K3 三框架 benchmark 文章：**实际测量日为 07-29**，8×MI350X，各引擎 day-0 配置未归一、每点单次且无准确率评估；不能称本周性能榜或 W7900 可复现方案。[S102]
- 09-22 ATT profiling Part 6：介绍 rocprofv3/Compute Viewer，文档列 Radeon gfx11 支持；云镜像、驱动和 profiler 权限仍须实测。先完成 HIP/kernel/copy 时间线，再按需要做 ATT，不强制本周升级驱动。[S103]
- 09-25 UltraQuant：官方报告 MI355X 上 4-bit KV 的特定负载收益，文末明确 vLLM upstreaming 和 fused multi-token decode 仍是后续方向；不称 upstream 默认可用。此次 sweep 没有 KV offload，不能拿它证明 LMCache 收益。[S104]

---

### 3.10 本期技术变化台账（2026-09-28 至 2026-10-05）

下表只写本次能够从官方仓库当前页面、release 或 PR 正文确认的内容。性能数字均为作者报告，未由本研究复现。

| 项目 / 事件（UTC） | 已确认事实与当前状态 | 成熟度、岗位与个人准备影响 |
|---|---|---|
| **Infera 当前 README / v0.1.1** | 当前公开镜像包含 vLLM、SGLang、ATOM、KVD 与 server 的 `v0.1.1` 标签；入口同时覆盖 OpenAI-compatible API 与 Anthropic Messages 转换；worker drain、Kubernetes operator、KV-aware routing、P/D 与 AIC tiering 已进入公开说明。README 同时明确 PyPI 包尚未发布、Rust router 尚未作为 wheel 交付，且没有 scaling controller | 说明控制面/路由/KV 分层的公开产品形态比早期 v0.1 更完整，但仍是 reference solution。`kubectl scale` 与安全 drain 不等于 SLO autoscaler；作者在 MI355X 的零失败样例不外推所有拓扑。[S112] |
| **Infera #179；10-01 创建，Open** | InferaSim 在评审中增加 PP stage host/scheduler 开销、token 返回路径与跨节点 NIC 边界成本；正文报告 MI355X 上多模型 PP ladder 校准，448 个 projection 单测通过 | 是模拟/容量规划准确性改进，不是运行时 PP 通信实现。适合面试解释“传输字节少并不代表 hop 便宜”，也再次说明 simulator 与真实执行必须分栏。[S113] |
| **MORI #717 / #718；09-30 创建，Open** | #717 计划让 H2D restore 的多段 batch 始终保留在 gather kernel，并把 D2H fallback 阈值分开；#718 计划让默认未绑定 DRAM tier 跨 NUMA 并行 prefault。两者均给出 8×MI355X 作者测量 | 与 LMCache/hip-kv-transfer-lab 高度相关：应分别测 plan/gather、copy 提交粒度、NUMA first-touch 和注册成本。它们尚未合并；W7900 单卡也不能复现 8 卡双路 NUMA 结论。[S114][S115] |
| **MORI #711；仍 Open** | 两类 CCO SDMA device-post 死锁补丁仍在等待评审；正文把 process-wide 共享 queue、multi-wave publish 与 commit snapshot 分开，并提供确定性 gate 复现和数据校验矩阵 | 继续作为完成语义/资源共享的进阶案例，而不是待从零认领的任务。对用户最可迁移的是“共享资源范围大于 communicator”与“完成/发布顺序是协议”，不是声称已有 SDMA kernel 经验。[S116] |
| **ATOM #2459；10-03 创建，Open** | 在 GLM-5.2 1P1D、prefill PP4/decode TP4+DCP4 场景中，方案 A 为每 NUMA node 一个 LMCache MP server，方案 B 为 in-process LMCache L1 + 跨节点 Mooncake Store L2；正文报告 HIP IPC 仅用于单机，跨节点回读走 RDMA | 这是“LMCache + 分层 L2”的在研方案，直接提示适配时要把进程边界、NUMA、L1/L2 ownership 和跨节点 transport 分开。作者性能数字依赖特定模型、并行配置、MI355X 与 agentic trace，不是通用收益。[S117] |
| **ATOM #2464；10-03 创建，Draft** | 另一方案绕过 LMCache：ATOM 自己 pack 256-token chunks，直接从 HBM `batch_put_from` 到 Mooncake Store，命中后 `batch_get_into` 回 HBM 并 unpack；正文将 staged、in-place、LMCache+Store 作作者对照 | 不能据此得出“LMCache 不再需要”。它只说明同一目标可有不同控制面/数据面拆分；比较必须覆盖功能范围、淘汰/一致性、可观测性、复用率和端到端 TTFT，而不只看 copy 带宽。[S118] |
| **AIC #177/#178 与 #181/#182；仍 Open** | #177 继续推进 CPU-only RocJITSU emulation 日报；#178 的 gfx1250 QEMU-KVM/compose 测试仍等待 code-owner review，且约 54GB 镜像超过标准 GHA runner 空间，PR trigger 被移除；#181/#182 继续调整本地/集群构建与 SPUR controller 地址 | emulation 可用于功能/回归，不是物理 GPU 性能。构建、CI 资源和镜像体积本身就是外部贡献门槛；不把“有 gfx1250 虚拟设备”写成真实 MI450 生产验证。[S119] |
| **ATOM v0.1.6 / ROCm 10.0** | 09-22 release 同时提供 ROCm 10.0 与 7.2 wheel；release 只说明构建组合，未列本期分层 KV 新 PR | 已发布基线与 main/feature branch 必须分开。做复现时固定 ATOM、AITER、PyTorch、ROCm 与 GPU arch，不能用 main 的 #2459/#2464 推断 v0.1.6 已包含它们。[S121] |

**本期判断：** 公开路线进一步收敛为两层：Infera 负责跨 engine 的路由、生命周期与容量决策；MORI/LMCache/Mooncake/ATOM connector 负责 KV 与通信数据通路。新 PR 强化了截图 JD 的技术相关性，但仍没有 exact Req 证据。对用户最有价值的准备不是追逐所有分支，而是用一个可复现实验讲清：布局、ownership、event 依赖、NUMA/pinned memory、批量 gather/scatter 与端到端收益之间的关系。

---

### 3.11 本期技术变化台账（2026-10-05 至 2026-10-12）

本节只把已经进入目标分支的改动写成“已实现”；Open/Draft PR 仍按评审中处理。性能和故障复现数字均为作者报告，未由本研究独立复测。

| 项目 / 事件（UTC） | 已确认事实与当前状态 | 成熟度、岗位与个人准备影响 |
|---|---|---|
| **Infera #183；10-10 合并** | `/metrics` 默认输出 TTFT/ITL/token histograms，并从 vLLM/SGLang worker 联邦 allowlist 指标；Python 与 Rust router 均覆盖。评审过程曾发现重复 metadata、PromQL、stream 完成、retry 归属与 scrape timeout 问题，最终以 8 commits 合入 | 可观测性从“看 router”推进到“一次 scrape 同时看 frontend 与 engine”。这为 SLO 调度提供数据基础，但不是 autoscaler 本身，也不能保证任意第三方 engine 指标都已兼容。[S123] |
| **MORI #716；10-10 合并** | `session.alive()` 不再在所有 backend 恒为 true；RDMA async event monitor 把 QP/port/device fatal 事件转为可消费的 peer failure，增加有界 pending queue 与查询/回调路径 | 直接补强 P/D 场景“慢 peer 与死 peer”的区分，但仍不等于自动 reconnect 或所有 lost-CQE 都能恢复。与用户 ProcessGroup 完成语义经验高度相关，适合面试讲 liveness、timeout 与 error propagation。[S124] |
| **MORI #729；10-09 合并** | VMM KV memory 改用 allocation handle 导出 DMA-BUF，避免 deregister/close 后仍持有 backing allocation；作者在 8×MI355X、Pollara AINIC、ROCm 7.2/10 上验证 sleep/wake 与内存释放 | 这是“API 成功返回但资源仍未真正释放”的典型生命周期问题。实现依赖 HIP runtime 版本差异及 POSIX FD handle type，不能外推普通 `hipMalloc`、其它 NIC 或 W7900。[S125] |
| **ATOM #2518；10-10 合并** | 修复 LMCache MP 中重复、未消费 async lookup 与 hit-count 被提前清理共同造成的 L1 read-lock 泄漏；prefetch 跳过不会消费 lookup 的请求，并由 lookup client 保存 async hit 以便 discard 释放锁 | 说明 cache correctness 不只包含数据字节，也包含 lookup/lease/lock 生命周期。最值得复用的测试模式是：负载停止后锁数归零、TTL 前可淘汰、异常路径明确由 TTL 兜底。[S126] |
| **LMCache #5157；10-08 合并** | engine-driven 同步跟随 KV tensor 的实际设备，CPU tensor 不再同步无关 accelerator；保留 async STORE event 与 staging lifetime，38 checks 通过 | 旧版“仍 Open”已失效。自研芯片适配应先基于含此修复的 commit/release，再检查对应 DeviceSpec 是否把同步落到真实设备；合并不能代替自研设备与 W7900 的验证。[S127] |
| **LMCache #5565 / #5611；10-09 / 10-10 合并** | #5565 在 host pin/unpin 失败后调用 `hipGetLastError` 清理 pending HIP error，避免下一 kernel 莫名失败；#5611 移除 SGLang unified MP connector 的硬编码 CUDA gate，改由 platform IPC/event/cache/transfer 能力决定 | 对新设备后端是实质利好：上层不再仅按 CUDA 名称判断，但 backend 能力必须真实实现和测试。错误清理也提醒：已经返回 false 的 runtime 调用仍可能污染线程的后续错误状态。[S128] |
| **MORI #731；10-09 创建，Open** | 为 MORI-IO verbs data path 增加可编译开关控制的 fault injector，模拟 post fail、CQE error/drop、QP error，以复现无限 RNR retry、lost CQE、被动端无通知等 hang；PR 明确“本身尚不改变行为” | 是很适合阅读和补测试矩阵的在研基础设施，但已有作者。W7900 单卡无法验证真实 RDMA；本地可审查 fault contract/超时不变量，之后需 NIC/多节点核对模拟症状与真实故障。[S129] |
| **AIC #183；10-05 创建，Open** | 用两台 QEMU/KVM VM 与 emulated Pensando ionic RDMA NIC 做 LMCache P2P KV-sharing E2E，断言第二实例 P2P load counter 增长；需要 `/dev/kvm`、Docker socket、约 3.5GB guest image，已有作者/assignee | 为“无物理 GPU/RDMA 的功能回归”提供现实入口，但 emulation 只证明协议/控制路径，不能证明 GPU-direct、真实 NIC 时序或性能。外部贡献更适合评审可重复性和失败诊断，而非重复实现。[S130] |
| **AIC #177 已合并；#178 仍 Open** | #177 于 10-05 20:07 UTC 合并 CPU-only RocJITSU 日常 sweep 与 GitHub Pages 历史趋势；#178 继续推进 gfx1250 QEMU/KVM GPU/compose 集成，但正文仍列上游 MES queue 限制，当前稳定 gate 主要验证编排路径 | #177 的数据是 emulator trend，不是物理 GPU benchmark；#178 即使 VM 中报告 gfx1250，也不能当作 MI450/Helios 生产验证。两项都有明确作者与 code-owner 路径。[S133] |
| **ATOM #2459 / #2464；仍 Draft / Open** | #2459 当前仍是 LMCache MP/NUMA L1 + Mooncake Store L2；#2464 当前为绕过 LMCache、直接 HBM↔Store 的 pack/get/put/unpack，已增加较完整失败路径与作者 benchmark | 两条路线仍未进入 release。比较重点继续是 owner、namespace、lease、发布时机、失败回收和端到端 TTFT，而非只比较 GB/s。[S131] |
| **LMCache #5075 / #5133；仍 Open** | #5075 的 ROCTX annotation 仍 3 commits、无 reviewer，当前页面显示 19/29 checks；#5133 的 padded MLA/BSV_BSS torch fallback 仍 Open，CPU regression 完整但 GPU runtime、stream 与 E2E 未验证 | #5075 仍是 W7900 低门槛补测候选；#5133 更适合做布局/stride 测试方法学习。两者都有作者，不能列为无人负责的新题。[S132] |
| **vLLM #61109 / #61119；10-11 Open / Draft** | #61109 为 2×4 XGMI-island 的 MI210 TP8 组合 CustomAllreduce 与 PyNccl，复用现有 kernel；#61119 将 AMD MiniMax-M3 FFN all-reduce 延后到下一层 normalization，作者报告单独改动性能基本中性、与 QuickReduce/融合 norm 组合后才有收益，且 GSM8K 有波动 | 与用户已有 vLLM custom allreduce 接入经验直接相关，但两项都有作者，且 MI210/特定模型数据不能外推其它拓扑。应学习 island communicator、graph capture、reduction ownership 与精度回归，不把作者 benchmark 当独立验证。[S134] |
| **SGLang #43719 / #43723；10-11 Open** | #43719 在 Mooncake send 非零返回或超时但写入可能仍在途时，对 room 做 poison，避免 Decode 释放并复用页面；当前 fallback 会让 Decode 最多等待约 30 秒。#43723 为 NIXL staging 启动补 `slot_layer_ids`，有 H100/NIXL 作者验证，但无单测且页面仍有 CI failure | #43719 是很强的“ACK、完成未知、buffer reuse”案例；但彻底修复仍需 Mooncake 区分失败与完成未知。#43723 暴露 connector 启动参数与测试覆盖缺口，不是 AMD GPU 验证。两项均更适合作为评审/学习而非抢占实现。[S135] |

**本期判断：** 技术演进从“新增 connector”进一步进入“可观测、故障传播、资源释放、锁/lease 回收和设备抽象”的生产化阶段。这与截图 JD 的关联仍属 B 级强推断，但对面试准备非常直接：应优先讲清楚一次异步操作从提交、完成、发布到资源复用的全链路，而不是只罗列 HIP/RDMA API。

---

### 3.12 当前技术变化台账（2026-10-12 至 2026-10-19）

本节以 10-19 的 REST 合并字段、目标分支、讨论及重点当前源码为准。**merged 到开发分支不等于已入 main，main 不等于已发布 wheel，作者模型测量不等于本研究独立复现。** 10-12 当天晚于上次检查的事件也属于本期增量。

| 项目 / 事件（UTC） | 已确认事实 | 当前边界与岗位准备影响 |
|---|---|---|
| **Infera #185 / #186；10-12 / 10-14 入 main** | Rust router 新增 opt-in Prefill 独立负载释放，以及独立的 P/D session bindings；main `session_affinity.rs` 有 generation、active lease、TTL 与容量限制 | #185 默认仍随 Decode 释放，completion 模式等待完整 body/terminal frame；它不改变物理 KV ownership。#186 状态局限单 Router 进程、重启丢失，不是集群会话存储或 tenant 隔离。作者有两节点功能验证，未报告新吞吐/延迟结论。[S137] |
| **Infera #192 / #197；10-13 / 10-14 入 main** | 启动超时/端口与 Mooncake preflight 加固；加入特定 ATOM nightly + GLM-5.2 DCP 示例 | preflight 增加 WRITE 的接收端字节验证，说明“注册成功”不能替代数据正确。示例依赖所列模型、镜像与 MI355X；不保证 W7900 可运行完整方案。[S137] |
| **Infera #198 Open；#203 10-17 merged 到开发分支** | #198 仍在评审：nightly 更新、ROCm pinned pool 与 eager DCP padding 修复；#203 的 base 是 `dev/yaoc/glm5.3-atom-20261013`，不是 main | API ancestry 显示 main 比 #203 merge commit 落后 12 commits（ahead=0、behind=12），不能把“ATOM P/D Rust router 已合并”直接写成 main/release 已交付。#198 的根因和测试是作者分支报告，不是所有 pinned memory 的普遍行为。[S138] |
| **MORI #711 / #731；10-13 / 10-12 入 main** | CCO 两类 SDMA device-post 死锁补丁、verbs fault injector 均已合并 | #711 评论撤回早期 L2/doorbell 单调性推断，最后由 ownership bit 与 drain mask 等修正；维护者表示后续 shared publish helper/剩余 SDMA 项由团队推进。#731 提供复现 seam，不等于 H1–H5 的 deadline/reconnect 全部解决。二者移为学习案例。[S139] |
| **MORI #718 / #756 / #761；10-13 入 main** | DRAM NUMA prefault、standalone 锁范围/分段 host registration、失败 fabric-handle probe 后清 HIP last-error | 在作者的大池/MI355X 场景中，USERPTR 页迁移可导致队列被逐出并放大查找等待；#756 的分块与锁收窄改善退化行为，不保证跨节点 MR 容量和 NIC 限制已解决。hugetlb 与 GTT 的作用须分开；不照抄环境变量到云镜像。[S140] |
| **MORI #741 / #774 / #762 / #763；10-15 / 10-15 / 10-16 / 10-16 入 main** | 默认 peer-local eviction、统一 incremental plan builder；本地大批 SSD get 分段暂存；本地读用 refcount hold 保护字节；可重试 demotion 与 dropped/retried 指标 | 本地 hold 不再靠固定时间到期判断完成；远端仍有 timed lease，不能外推安全。demotion retry 仍有预算与最终丢弃，不能称永不丢缓存。主机逻辑适合 CPU/模型审查，真实 GDS/RDMA/吞吐仍需对应硬件。[S141] |
| **ATOM #2464；10-13 入 main；#2459 10-12 非合并关闭** | dense `mooncake_store` 直连通路已合入，主分可见 Store taint marker；另一 LMCache MP+Store L2 实验分支关闭且 merged=false | #2464 不读 LMCache 对象，限制 dense/offload 侧 DCP；未知完成的 put 会让共享 Store 停止加载并要求重启，不是自动修复远端内存。CPU fake 测试与 GPU RDMA 往返是不同证据；不能据此否定 LMCache。#2459 的关闭原因未获明确解释，不推断已被完整替代。[S152] |
| **LMCache v0.5.6；10-14 22:21 UTC 发布** | release 明列 #5157、retrieve event wait、HIP copy-engine 与 MP 安全修复；commit compare 确认 #5157 为 tag 的祖先 | 是自研设备适配候选基线，需核对接口与 ABI；10-18 ROCm nightly 仍面向 gfx942/gfx950、ROCm 7.2 与其配套 torch，不是 W7900/gfx1100 现成保证。新发布不等于 AIC 已同步升级。[S142] |
| **SGLang #43719 / #43723；10-12 / 10-13 入 main** | Mooncake completion-unknown 时 poison drain ACK；NIXL staging 接受 `slot_layer_ids` | 纠正上期“仍 Open”；main Mooncake 代码可见 poison 路径。保守等待/timeout 不是远端写入已经停止的证明；NIXL 作者 H100 验证不冒充 AMD 验证。[S143] |
| **SGLang #40917 / #44968；10-18 入 main** | host pools 从 typed buffer info 构建；显式处理 scale/layout 与 packed draft，Mamba routing 与 host layout 共用 layer axis | main 有 `MHABufferInfo/MLABufferInfo` 及 scales。PR 包含局部拒绝不支持的 scale 格式、storage dtype 修复，但不改变所有物理格式；正文 AMD ROCm 10 CI 仍显示 failure，不能写全平台通过。面试可讲“payload 拷对不等于含 scales 的 KV 恢复正确”。[S143] |
| **vLLM #60544；10-17 入 main** | MoRIIO hybrid WRITE 扩展到 attention+Mamba/KDA 和 DSpark；当前使用指南已更新 | 等 TP、匹配布局、align、相同 draft；sliding-window WRITE 与其它 hybrid speculation 仍不支持。作者模型评估有波动且无性能对照，不当 bit-exact 或生产资格认证。旧 #51052 的 READ-only 限制不再是整个当前 connector 的状态。[S144] |
| **vLLM #58761 / #62241；10-18 / 10-19 入 main** | 默认 ROCm 构建/发布路径切到 10.0，保留 7.2 variant；external launcher 退出时清理 vLLM-owned model-parallel groups | 以当前代码/镜像 digest 验证实际发布内容，不能保证所有 latest 已重建；#62241 main 仅调用 `destroy_model_parallel()`，保留 launcher 可能拥有的 world/default group。是与 ProcessGroup 经历最直接的 ownership 案例，PR 验证项未全勾选，不能称退出异常全面消失。[S144] |

**本期官方文章/文档：**

- **10-16 RDNA FP16 GEMM 教程：** 作者在 W7800/gfx1100 等设备展示逐步 WMMA、LDS、寄存器与流水优化。适合 W7900 的第二阶段对照实验；文中 ROCm 10 与 FP16 accumulation 是固定条件，不能把其数字搬到 W7900，也不能用 ±1 输入精确匹配代替任意输入的误差验证。[S148]
- **10-14 GLM-5.3 MI300X recipe：** 比较 TP8 与 DP8+EP8，收益随长/短请求变化，依赖具体版本和两个 AITER 补丁。用来练习“通信拓扑、KV 显存与 workload 共同决定策略”，不是一张 W7900 的复现任务，也不证明 DP+EP 永远优于 TP。[S149]
- **Roadmap 纠正：** Infera #9 最后更新仍 09-24；MORI #348 仍 06-15；SGLang AMD #35003 当前 metadata 为 **10-02**，旧表沿用的 08-18 已过期。其文字新增/细化 MI45x、UMBP connector、MoRI-EP v2、FP8/MXFP4 attention/KV、CI 等目标，但仍是 WIP goals，不因出现型号或模型名就算交付。[S150]

**A/B/C 证据结论：** A 级事实是上述代码、合并目标与 release；B 级仍是截图与“路由/缓存/通信/引擎”产品族的关联，不能由提交活跃度推成组织汇报线；C 级仍包括 exact Req、实际模块、级别和远程雇佣资格。准备重点从“调用 API”进一步推进到 **谁拥有存储、何时完成、失败后谁还能读写、版本/布局是否兼容**。

---

### 3.13 当前技术变化台账（2026-10-19 至 2026-10-26）

本节以 10-26 的 GitHub PR/issue/release 字段、目标分支与 AMD 官方文章为准。**Open/Draft 不是已交付；合入 main 不是已发布；作者给出的 MI355X 数字不是本研究复现；官方文章链接个人 fork 也不自动把 fork 变成正式上游。**

| 项目 / 事件（UTC） | 已确认事实 | 当前边界与岗位准备影响 |
|---|---|---|
| **ATOM v0.1.8；10-19 发布** | release 提供 ROCm 10.0 / torch 2.11 与 ROCm 7.2.4 / torch 2.10 两组 wheel，固定 commit `daa4f1bb` | 这是可追溯 release 基线，不说明所有后续 ATOMesh/UMBP PR 已进入 0.1.8，也不保证 W7900/gfx1100 支持。[S154] |
| **Infera #198 / #209；10-19 / 10-23 入 main** | #198 将 ATOM nightly、GLM-5.2 4P4D、Rust router/ATOM PD 支持合入；#209 合入 ATOM/AITER patch、PD 路由和 Mooncake Store CPU tier 配方 | #198 的 ROCm pinned pool 修补比较了 USERPTR 注册与 `hipHostMalloc` GTT；#209 性能为作者 MI355X/特定镜像结果。公开 release 列表最新仍 v0.3.0，不能把 main 写成 v0.3.1 已发布。[S155][S156] |
| **Infera #210 Open；#213 合入其 feature branch；#214 Open** | #210 更新到 SGLang 0.5.22，加入 mixed/PD 示例和 decode request-count weight；#213 并非直接进 main，而是折入仍 Open 的 #210。#214 计划发布 `atom-nightly` image，并明确先前 v0.3.1 tag/release 在产物发布前撤回 | #210 已报告 custom all-reduce 在 DP-attention + decode graph 下出现乱码并暂时禁用，这是有作者的高硬件调试线索；#214 合入前仍需自行构建 nightly image，不能说 v0.3.1 已可用。[S157][S158] |
| **SGLang AMD Q4 roadmap #46462；10-25 创建** | 新 roadmap 把 Helios/MI45x、量化 All-to-All/Reduce、P/D、HiCache/UMBP/Mooncake/LMCache、MoRI-EP v2 与新 connector 列为 Q4 目标 | 这是最直接的岗位方向旁证，但词语是 goals；不能把“production-level reliability”目标改写成已经具备生产级可靠性。旧 #35003 保留历史，新判断以 Q4 roadmap 为准。[S159] |
| **SGLang RFC #46455；10-25 Open** | 草案定义 Mooncake/NIXL/Mori 共用 per-backend `Transport`；协议拥有 timeout/retry/staging，caller 保持 backing memory 有效，Transport 拥有 registration/专属 engine | 与用户 ProcessGroup/生命周期经验高度相关，适合做接口契约评审；但它是无 assignee、0 评论的 Draft-for-review issue，不能据此宣布维护者已接受外部实现 owner。[S160] |
| **MORI #788/#821/#838 等入 main** | #788 保护仍被 reader hold 的 SSD staging；#821 改进 MR 注册错误诊断并记录 ROCm 7.2 非 VMM retain crash；#838 让最后一个 reader drop 后归还 staging span并改 next-fit | 生命周期与诊断更成熟，但 #838 尚未给出端到端复测；#821 明确指出旧 HIP 路径仍可能在 fallback 前崩溃。适合面试讲 memlock、页表/translation entry、hold 与 reaper 的边界。[S161][S171][S172] |
| **MORI #823/#825/#831/#836 Open** | 分别推进排队请求预取、多 GPU DRAM→HBM restore、失败 QP 重建、notification/data 两部分完成语义；均已有作者，#831 还有 assignee | #825 需要 8×MI355X/PCIe peer，#831/#836 需要 RDMA fault injection；W7900 单卡无法完成核心复测。可做源码状态机/CPU mock 评审，不当作无人负责新任务。[S162][S173]–[S175] |
| **ATOM #2634 Open RFC；#2630 Draft** | #2634 提议把 MORI-UMBP 作为 ATOM HBM 之外的分层/分布式 KV tier；#2630 将 ATOMesh standalone 数据面从 Python 迁到 Rust 并直连 EngineCore | 两者直接对应截图 JD 的全局 KV 与 Rust 路由，但都处于设计/大 PR 阶段；#2630 base 不是 main，不能写成 ATOMesh 已完成 Rust 数据面替换。[S163][S170] |
| **vLLM #61361/#63142/#63628 Open** | #61361 增加 MoRI EPv2 backend 与受限 fallback；#63142 合并下降 block run 降低 Mooncake descriptor/WR；#63628 在 P2P NIXL descriptor 准备失败时回滚未发布注册 | 三者分别映射 EP、KV 传输粒度与失败 rollback。作者数据/测试是有效证据，但都尚未合入；尤其 #63628 的 `cleanup failure` 仍不能保证 native registration 消失。[S164][S176][S177] |
| **AIC #181 入 main；#187 Open** | #181 统一 buildx 并增加 gfx1250 VM test；#187 重新应用此前 CI 修复 | 本期未确认新的 AIC 数据面/产品能力；构建与 CI 改进不能写成 UMBP/分层 KV 已完成真实 GPU/RDMA 验证。[S166] |

**本期官方文章：** 10-20 AMD 发布 MI355X 低延迟推理文章。Qwen3.8-27B 已列 ATOM/SGLang/vLLM 可用，Qwen3.8-Flash-Next 仅 ATOM 可用，GPT-OSS-120B 仅 vLLM preview；其余组合仍 planned。文章测的是单张物理 MI355X、主要为单请求 decode，且部分资源当前链接 `proaditya/*`、`sangeeta0201/*` 个人仓库；本手册把它们列为官方披露的早期实现，不并入正式上游贡献清单。[S165]

**A/B/C 证据结论：** A 级新增事实是 Req 94063、上述 release/合并/开放状态与官方 roadmap/文章；B 级是这些技术活动与截图岗位族的强关联；C 级仍包括 exact Req、94063 的官方发布日期/内部级别、具体团队归属、remote 资格和用户尚未完成的 W7900/LMCache 实测。

---

### 3.14 当前技术变化台账（2026-10-26 至 2026-11-02）

本节以 11-02 的 GitHub API 字段、release、PR 正文和当前状态为准。**合并、release、作者实测、模拟验证和生产验证继续分开；stacked PR 的顶层性能不能自动归因给其中每个提交。**

| 项目 / 事件（UTC） | 已确认事实 | 当前边界与岗位准备影响 |
|---|---|---|
| **Infera v0.3.1 / v0.3.2；10-26 / 10-29 发布** | 公开 release 从 v0.3.0 推进到 v0.3.2；#210 的 SGLang 0.5.22/GLM-5.2 mixed+PD、#214 的 atom-nightly release 入口均已合入 | 纠正上期“v0.3.1 尚未发布”。release 可作为复现基线，但其中示例仍依赖所列镜像、模型和 MI355X，不等于 W7900 可运行完整 P/D 配方。[S180] |
| **Infera #215/#216/#217/#219/#225；10-30 入 main** | projector 新增 Agentic 长度/restore/DCP 计费、分离式 prefill DRAM tier 和 prefix cache、MoRI 47.9 GB/s/120 µs measured preset、UMBP node tier、TTFT host latency/decode clock 修正、SGLang EP dispatch 两种模型 | 这些是容量和性能投影模型，不是路由器真正执行了 UMBP 数据搬运；#217 明确 NIXL/Mooncake 默认参数仍未测。适合练习“模型假设—测量锚点—敏感性分析”，不能当作端到端吞吐证据。[S181] |
| **MORI #823/#831/#836；10-27 至 10-28 入 main** | queued request `BatchPrefetch`、失败 QP 替换、notification 与 data WR 两部分完成语义已合入 | 三者把“提前搬运、故障恢复、完成后才能复用 buffer”落成源码。#825 多 GPU restore 仍 Open，不能把单机预取外推为多卡带宽聚合已交付。[S182] |
| **MORI #851/#862/#867；10-29 至 10-31 入 main** | #851 可向 SGLang KV Indexer 报告共享 DRAM residency；#862 提供 UMBP 容量/传输模拟；#867 提供不需 GPU/NIC 的 RDMA/TCP/XGMI 模拟后端 | 这是本期最有用的外部参与变化：本地可跑真实 control flow、session/status/peer failure，而 payload 与硬件时序仍是模拟。#851 完整联动仍需 SGLang #46995，后者未合入。[S182][S185] |
| **MORI #843/#866；10-30 至 10-31 入 main** | gfx1250 EPv2 wide-EP/LL128 tuning 与 fused SDMA wait+put、engine-wait all-gather example 合入 | 作者数据来自指定架构/拓扑；#866 的 sharded KV prefix 例子适合学习 epoch、READY slot 和 engine wait，但 W7900 单卡不能验证 peer SDMA all-gather。[S183] |
| **MORI #825/#875/#884 仍 Open/Draft** | 多 GPU restore 未更新；#875 处理双 stream fused-receive 占满 CTA 导致跨 rank deadlock；#884 试图绕过 host scratch，直接在注册 GPU memory 与 peer tier 间 ranged I/O | 均有现成作者且依赖多 GPU/RDMA/MI355X 或 stacked 分支。可做 occupancy、stream 依赖与 registration 生命周期评审，不作为新手空白题。[S183] |
| **vLLM #61361/#63142/#63628 已合入** | MoRI EPv2 backend 10-31 合入；Mooncake descending block coalescing 10-26 合入；失败 P2P NIXL registration rollback 10-26 合入 | 三条已从“在研案例”升级为 main 学习基线，但最新 vLLM release 仍 v0.32.0（10-18），不能声称已随 release 交付。[S184] |
| **vLLM #61109/#61119/#64428 仍 Open/Draft** | MI200 XGMI-island custom allreduce、AMD MiniMax FFN deferred allreduce、MI355X QuickReduce MoE combine 均有作者推进 | 与用户 custom allreduce/集合通信高度相关；最适合比较 topology、defer point、quantized reduce 的 correctness boundary。作者性能数字不外推到自研芯片或 W7900。[S184] |
| **SGLang #46995 / #47309 Open/Draft** | #46995 与 MORI #851 配套共享 DRAM pool；#47309 stacked 在 #47180/#44322 上，组合 row-split indexer、AITER FP8 ASM sparse MLA 和 side-stream A2A pipeline | #46995 可用 CPU/fake indexer 检查 pool identity 与 fail-closed；#47309 的整套数字不能拆成单个改动收益，且依赖 MI355X/DCP4/特定模型。[S185] |
| **ATOM #2634/#2630 未推进；#2786/#2842/#2865/#2866 新增** | UMBP RFC 与 Rust data plane 仍 Open/Draft；新的工作覆盖 P/D 首 token/GC、state checkpoint null page、多模态 prefix-hit shape mismatch、Qwen3-Next cudagraph 非法访存 | ATOM release 最新仍 v0.1.8。新问题说明 KV 命中、状态 checkpoint、媒体 embedding 与 graph padding 之间仍有 correctness seam；issue 的复现和推断不是已合入修复。[S186] |
| **AIC #189/#190/#196/#198/#199 合入；#192/#193/#197/#201 Open** | 本期主要是 nightly wheel、构建/网络修补、latency report 与 AgentX benchmark 入口 | 可改善可安装性和回归可见性，但没有足够证据说明新的物理多节点共享 KV 数据面能力进入稳定 release。[S187] |

**A/B/C 证据结论：** A 级事实是上述 official release、合并字段和当前 PR/issue 状态；B 级是这些项目与岗位族、以及 94063/94065/96117 之间的职责映射；C 级仍包括 exact 截图 Req、官方发布日期、团队边界、内部生产采用程度和用户尚未完成的实测。

---

### 3.15 当前技术变化台账（2026-11-02 至 2026-11-09）

本节以 11-09 的官方 release、PR/issue 字段、正文和当前状态为准。**release 只证明该 tag 的公开产物；合入 main 不等于已进入 release；Open/Draft 及作者 benchmark 不等于生产能力；RC/nightly/preview 均保持原等级。**

| 项目 / 事件（UTC） | 已确认事实 | 当前边界与岗位准备影响 |
|---|---|---|
| **Infera v0.3.3；11-02 发布** | 官方 release 提供 Python wheel 与源码包，正文为自动构建说明 | 可作为 v0.3.2 之后的新可追溯安装基线；release note 没有给出数据面能力清单，不能仅按版本号推断新增功能。[S191] |
| **Infera #233；11-05 合入** | 更新 SGLang 0.5.22 / ROCm 10.3 alpha nightly 预览，并记录 ROCm 10.2 + SGLang 0.5.21 的 disaggregated decode 长跑错误 | 这是兼容性矩阵和已知缺陷修正。验证集中于同节点 MI355X，仍有有限短答案异常，且没有 GSM8K/AgentX/多模态 Rust extension 的完整验证；因此只写 preview，不写成熟 P/D 生产能力。[S192] |
| **MoRI v1.2.5；11-06 发布** | 官方 release 汇总 105 commits：manylinux wheel/gRPC、EPv2 AsyncLL/LL128 与 EP16/32、GEMM+collective 融合、SDMA 2D/CCO、MORI-IO CXI/failed-QP/fault injection/simulation、UMBP SSD/NUMA/BatchPrefetch 与 SGLang Indexer 等 | 这是本期最重要的正式 release 基线；其中多项代码早于本周已在 main 出现，不能把 release 日期改写成全部功能本周才实现。硬件性能仍取决于 gfx125x、MI355X、NIC/拓扑和特定配置。[S193] |
| **MoRI #907 Open；#915 非合并关闭** | #907 要求失败状态直到所有可能触碰 buffer 的 WR 都已结束才可见；#915 的 quiescence API Draft 因与 #907 重叠于 11-06 关闭、未合入 | 纠正“Open/无 assignee 即无人推进”：#907 有明确作者和评审活动；#915 保留为历史设计案例，不再列作可认领任务。该线与用户通信完成语义最贴合。[S194][S195] |
| **MoRI #923/#929/#933 Open/Draft** | #923 增加 SDMA AllGather start/wait；#929 优化 UMBP per-key 扫描；#933 为 simulator 增加 host-posting/overlap 模式并报告 26 个 CPU 测试通过 | #933 可降低本地验证门槛，但仍有作者；其模拟证明控制流/状态机，不证明真实 GPU/NIC 时序。#923/#929 的核心收益需 gfx950/真实 UMBP 环境。[S196]–[S198] |
| **ATOM v0.1.9；11-02 发布** | 官方 release 提供 ROCm 10.0 与 ROCm 7.2.4 对应 wheel | 新的安装基线不等于 11-02 后的 P/D、DCP、LMCache stacked PR 已包含其中；复现需固定 wheel、torch、ROCm 和 commit。[S199] |
| **ATOM #3027；#3068–#3070 Open** | #3027 推进多模态 key、LMCache engine ID、chunk-grid checkpoint/deadline；#3068–#3070 是 PP→DCP×TP/MLA/LMCache 的 stacked 迁移与作者性能结果 | 都有明确作者，#3027 还有 assignee/评审；#3068–#3070 的结果依赖特定分支和硬件，且保留 MoRIIO PP/chunked-transfer 限制。作为 P/D 状态迁移学习案例，不写成 ATOM 0.1.9 能力。[S200]–[S203] |
| **ATOM #3088 Draft；11-07 创建** | 提议补充 CONTRIBUTING、review 流程和 area contacts | 在合入前，不能把草案内容当作 ATOM 当前正式贡献政策；它只说明项目正在补足外部参与入口。[S204] |
| **SGLang #49156；11-08 合入** | Mooncake KV registration 被拒绝时，进程启动显式失败，不再吞掉错误后以零质量继续服务 | 这是 main 上的实际 correctness 改进，但尚未据此确认进入哪个 release；适合作为 fail-fast/资源注册边界面试案例。[S205] |
| **SGLang #49205 Open；11-08 创建** | 为 MI450/gfx1250 的 AMD custom allreduce 增加 hierarchical `2shot_push`，作者在两台 MI455X 上报告 17%–31% 改善 | 与用户 custom allreduce 经历高度相关，但已有作者、硬件专用、尚未合入；适合比较拓扑分层、同步点和正确性，不作为空白贡献题或通用收益。[S206] |
| **vLLM #66008/#66268 Open/Draft** | #66008 为 MoRIIO READ lease 增加续期，避免 decode 等待超过 prefill 60 秒后的 silent wrong output；#66268 给出 MI355X、MoRI-IO、1P2D/12 GPU 的 MiniMax-M3.1 recipe | #66008 是直接的 KV 生命周期案例；#66268 仍依赖前置 PR且缺少完整准确率验证。两者均为作者推进中的在研材料，不是 vLLM release 能力。[S207][S208] |
| **LMCache v0.5.7rc4 ROCm 变体与 11-08 nightly** | RC 提供 ROCm 7.2/gfx942/gfx950 及 ROCm 7.2.4/torch 2.10 ABI 变体；nightly 为 `0.5.8.dev71+rocm7.2` | 标签虽为公开产物，名称仍明确是 RC/夜版；必须固定 torch/ROCm/arch/vLLM 镜像，不写作稳定生产 release。[S209][S210] |
| **LMCache #6358 已合入；#6401/#6411/#6421 Open/Draft** | #6358 支持 VMM shared-KV 的 vLLM sleep mode；#6401 RDMA write、#6411 peer DRAM→GPU borrowing、#6421 MP read lifetime 仍在评审 | #6358 现有证明是 H200/CUDA；后三项也主要是 H200/RoCE 或 CPU/unit 证据，均没有足够 AMD/ROCm 生产验证。生命周期设计可学习，硬件结论不可迁移。[S211]–[S214] |
| **AIC #202/#203 合入** | 分别固定安全 workflow action 与修复 nightly wheel benchmark job | 本期未确认 AIC 数据面或物理共享 KV 能力变化；CI/供应链改进不写成真实多节点验证。[S215] |

**A/B/C 证据结论：** A 级事实包括 96120/96121 的官方正文、上述 release 与 PR/issue 状态；B 级是它们与截图岗位族、用户通信/框架经验的强关联；C 级仍包括截图 exact requisition、两条新岗位的官方发布日期/级别/团队、国内远程资格、内部生产采用程度及用户尚未完成的 AMD 实机复现。

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
- 按 connector / 版本 / 保存策略保留可复用的新 KV；不是所有实现都在每个 decode step 卸载，也不是统一只在 eviction 时保存；
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

### 5.8 个人补差项目：重新适配自研芯片 LMCache

**10-19 当前覆盖说明：** v0.5.6（10-14 UTC 发布，tag `3e11e10`）已确认包含 #5157，且 release notes 包含 retrieve 前等待 event、ROCm direct copy-engine 等改动；建议把它作为新适配的候选基线，再核对公司框架/SDK 兼容性，而非直接在工作环境升级。10-13 安全公告指出 MP 不安全反序列化在 v0.5.6 修复，worker/server 应一起更新协议。不要将带补丁的 AIC 镜像仅凭 `0.5.5` 字符串判为有漏洞或已安全，需查实际 patch。新增验收：同 prompt 不同 KV dtype/scale 必须隔离；完整保存 payload 与 scale；CPU pool 的注册、页迁移与 copy 路径分开计时。#5133/#5615 仍是有作者的在研参考，不是已发布的通用保证。[S140][S142][S151]

**10-12 参考更新：** LMCache #5157 已于 10-08 合并，engine-driven 同步现在跟随 KV tensor 的实际设备；#5133 仍 Open、有作者。ATOM #2167/#2339 已合并 completion/retention 分离与 dense producer fencing，#2518 又补上 MP async lookup 的锁释放。七天 W7900 合成实验只铺垫本节，不算自研芯片适配完成。[S94][S95][S126][S127]

**当前状态：计划，未实现、未测量。** 同事过去观察到 decode 变慢，但旧版本、配置与 trace 已不可得，无法确认当时是不是逐步 decode D2H、全局同步、layout 重排或命中不足。不能替旧实验定根因。

1. **先选最小闭环。** 固定自研 PyTorch、vLLM、LMCache commit，单进程/单设备、一个常规 attention layout、一种 dtype、CPU cache tier；若采用当前 MP 接口，先按官方新设备指南显式选择 engine-driven，服务端也要接受该模式。该路线避免一开始实现设备 IPC，但不意味着零设备适配。[S79]
2. **先正确再异步。** 当前 engine-driven 源码仍保留同步边界；这是 baseline 的生命周期保障，不是已经实现的通信计算重叠。#5157 已把同步对象纠正为实际 KV tensor 设备，并跳过 CPU tensor 的无关 accelerator sync。不要再把该问题当未合并缺陷；适配时应固定包含此修复的版本，并验证自研 DeviceSpec/DeviceOps 是否提供等价语义。[S127]
3. **验证真实数据与布局。** block id 非连续、部分尾块、padding/stride、layer 顺序、dtype/scale、cache key/model namespace、TP rank 归属都要检查。#5133 提醒 torch fallback 对 padded MLA/BSV_BSS 仍有在研修复，且该 PR 的 raw GPU pointer 路径只限定 CUDA ABI；不能把 MUSA/HIP 当成自动兼容。[S80]
4. **分离两类收益。** 外部缓存保留/复用用于减少后续 prefill 或缓解 HBM 容量压力，不是让每次 decode 本身天然更快。必须记录外部 reused tokens、实际 D2H/H2D bytes、TTFT、TPOT/ITL、排队、完成数与错误率，不能仅看 LMCache 服务启动。
5. **实验矩阵。** 同模型同请求同资源：A 原引擎 APC；B LMCache 冷缓存；C LMCache 热缓存且 GPU 原缓存已被受控挤出；D 唯一前缀/无复用负对照。另跑多轮重复前缀、高并发容量压力。重启实验要写清谁重启、CPU cache server 是否保留、模型/权重/布局是否一致。
6. **异步优化独立验收。** producer event → D2H → CPU 可读 → store 提交；load 完成 → consumer forward；source block 与 pinned buffer 仅在实际不再被读写后释放。future 返回、RPC 成功、timeout 都不天然等于 device completion。先保守同步测出基线，再优化锁页内存、批量 block-ID、分块和 overlap。[S71][S72]

最小可交付不是“适配完成”四个字，而是：版本矩阵、数据路径图、字节级 roundtrip、错误注入/回收测试、一份含无收益情形的 A/B 报告。自研芯片结果可以证明工程能力，但不能标作 AMD GPU 验证。

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

| 对照学习概念（不等于个人实做） | AMD 侧主要映射 | 需要补充 |
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

### 8.1 当前最有竞争力的经历（以本人澄清为准）

- **ProcessGroupDLCCL：** 为自研芯片适配 PyTorch ProcessGroup，对照 NVIDIA 的 ProcessGroupNCCL，根据芯片特点调整执行流。可证明框架与通信后端的接口集成基础。
- **vLLM custom allreduce：** 为自研芯片建立更直接的调用路径，跳过原 PyTorch/DLCCL 层、调用已有通信算子。**没有编写该通信算子 kernel，也不能据此推断使用过 CUDA IPC。**
- PyTorch C++ Extension、集合通信与性能调试可作为相关知识/材料组织线索；具体负责内容、结果和 NCCL 源码研究深度，应由真实项目材料支持。本版不再擅自补出 communicator 设计、UAF 修复或 barrier 实现经历。
- 重新适配 LMCache 是用户计划，不是已完成经验；同事的旧适配也不是用户个人成果。

### 8.2 主要缺口

| 缺口 | 对目标岗位的影响 | 近期补法 |
|---|---|---|
| KV 存取、布局和 block 生命周期 | 直接关联 connector、全局 KV 和卸载 | 做 5.8 的真实设备闭环与回归 |
| EP dispatch/combine、RDMA transport | 与上层 allreduce 接口适配有明显距离 | 先读 MORI API/完成语义，用已有 PR 做对照；获得适当硬件后再复测 |
| ROCm / HIP 实机 | 自研芯片经验不能替代 AMD 平台验证 | 将通用接口结果与 AMD 待测项分列 |
| 大规模服务与系统性能 | 能跑通单测不足以满足资深 E2E 要求 | 固定 workload，报告缓存价值、端到端指标和失败场景 |
| Rust async / 路由 | 取决于实际团队分工 | 保留第二主线，先补取消、背压、状态机；不与 LMCache 项目同时铺开 |
| 上游协作 | 读代码不等于维护者认可或贡献合并 | 独立复现、说明范围，再讨论有新增价值的测试/修复 |

### 8.3 推荐的投递定位

> 推理框架与通信后端集成工程师：做过自研芯片的 ProcessGroupDLCCL 适配和执行流调整，以及 vLLM custom allreduce 对已有通信算子的直接接入；希望进一步承担 KV connector、异步存取和性能验证工作。

不包装成 EP kernel 作者、CUDA IPC 专家、成熟全局 KV 负责人或 AMD 集群 maintainer。匹配年限/职级尚需进一步事实，不用百分比遮盖证据缺口。

### 8.4 30 秒自我介绍主线

> 我主要做自研 AI 芯片与 PyTorch、vLLM 的通信接口适配。一个项目是 ProcessGroupDLCCL，根据芯片特点调整执行流；另一个是 vLLM custom allreduce，直接接入已有通信算子，减少中间调用层。我没有编写通信 kernel，也没有 CUDA IPC 实践。目前计划重新适配 LMCache，从 KV 数据正确性、设备同步和复用收益验证入手，补齐推理存储数据路径能力。

“减少调用层”不自动等于已有可量化收益；只有真实测量后才能加入数字。

### 8.5 三段必须准备好的项目故事

1. **ProcessGroupDLCCL（已做）：** 原调用流与修改后调用流；哪些是自己实现，哪些由芯片 SDK/通信库提供；同步边界为何要改；实际覆盖的 collective、rank 数与 dtype；能够提供的测试/性能证据。没做过的 failure recovery 不补写成经历。
2. **custom allreduce（已做）：** vLLM 入口如何选到自研 backend；参数、tensor/layout、device/stream 如何交接；直接调用和默认路径各自边界；若有 fallback/阈值则提供源码证据；对比测量要分 host overhead 与 device operator time。
3. **LMCache（准备中）：** 先写设计与验收，不使用完成时。完成后再填命中场景、同步/异步行为、错误与回收验证、是否真的优于基线，必要时诚实记录“没有收益”。

### 8.6 本期个人化调整：能力证据比 PR 数量重要

- 主线调整为“框架/通信后端集成 → KV Cache 存取与生命周期”，而非假定已有 GPU 通信底层深度。
- 首先在工作许可范围内做 LMCache 小闭环；涉及公司代码、SDK、日志和模型数据时，公开前必须获得相应授权并脱敏。
- 本期优先学习 ATOM #2223（异步 copy 单项可能变慢）、#2284（精确 block lease 与尚未贯通的 completion）、vLLM #57160（锁页内存方案的收益/代价）、LMCache #5157（实际设备同步）。阅读不等于自己的修复。[S71][S72][S74][S78]
- MORI #632 与 SGLang #38164 保留为补测/评审备选，已有作者，不抢同题实现。
- 旧版匹配百分比以及 30 秒介绍中的 IPC/barrier 直接经验已撤回；没有新增用户已提交或合并 PR 的事实。

---



### 8.7 10-05 个人准备的当前优先级

1. **把 W7900 资源转为可核验的 HIP 实验。** 现有路线图每天区分本地 A / 实机 B；本地约 16 小时、实机约 10 小时，另留排障余量。资源供应不连续时，本地学习继续、B 按依赖集中上机。没有用户提供日志/代码/数据之前，一律写“计划中”。（来源 S105）
2. **优先补三类证据：** producer→copy→consumer/reuse 依赖；CPU buffer 消费结束与 D2H 完成的差别；同步/异步/双缓冲的时间线和负收益解释。ATOM #2339 与 vLLM #58566 是本期最直接的源码对照。
3. **增加“数据通路方案对照”，不扩大项目数量。** 阅读 ATOM #2459/#2464 与 MORI #717 时，用同一张表比较 LMCache MP、LMCache L1+Store L2、直连 Mooncake Store、gather kernel/逐段 memcpy：谁拥有内存、何时可复用、跨进程/跨节点如何传输、失败如何回收、哪些指标可验证。只做分析，不宣称这些评审中方案已进入 release。
4. **开源协作首选收窄到可用硬件和权限。** LMCache #5075 的 ROCTX 补测仍适合单卡，但本期未能重新取得其最终状态，开始前必须再查；Infera 当前限制新 Issue 创建，#36 适合本地分析或先联系维护者，不预设能直接开新 issue。MORI-EP、RCCL 多卡和真实 RDMA继续标未验证。不要把 W7900 等同 MI355X 集群。
5. **投递定位维持框架/通信后端集成，新增两个备选方向。** 92727 可作为上海 kernel/性能方向备选，89764 可作为 Triton 通信岗位能力地图；前者要求 4+ 年并强调 kernel 深度，后者在美国且明确无签证赞助。两者都不改变“优先投中国框架集成岗位”的主线。

---

### 8.8 10-12 个人准备的当前优先级

1. **W7900 项目继续是第一优先，但验收应升级为生命周期证据包。** 除 KV roundtrip、双缓冲和 rocprof 时间线外，增加三类失败测试：producer event 缺失、host buffer 未消费即复用、异步 handle 未 wait 即释放。用 #5157/#2518 分别对应“同步对象”和“未消费结果仍需释放资源”。
2. **自研芯片 LMCache 适配基线前移。** 优先选择包含 #5157 的 LMCache commit；记录 platform 选择、actual device、current stream、pin/unpin 错误清理和 fallback layout。若遇到 padded MLA/BSV_BSS，再以仍 Open 的 #5133 为方法参考，不直接移植未验证的 CUDA raw-pointer 假设。
3. **把通信故障故事补成一页状态机。** 以 MORI #716/#731 为材料，区分：peer slow、peer dead、post fail、error CQE、missing CQE、passive receiver 无通知；为每类写出 timeout、buffer 可否复用、session 是否驱逐以及是否允许 retry。当前只做源码/设计证据，不宣称 RDMA 实测。
4. **面试中的 ROCm 例子优先用已合入的小而硬案例。** #5565 可以回答“错误返回后为何下一 kernel 仍失败”；#729 可以回答“deregister/close 为什么不等于 backing allocation 已释放”；#5611 可以回答“为什么设备支持不能靠 `cuda` 字符串判断”。
5. **投递顺序不因本周项目活跃度而改变。** 中国框架集成主线仍优先 87545/89393/89398/89499 等；92727 是 kernel/性能冲刺。没有新中国 remote 证据，也没有把美国 89764 变成现实投递主线。

---

### 8.9 10-19 个人准备与面试重点

1. **不增加同时开展的项目。** 第一项仍是 `hip-kv-transfer-lab`：版本清单、producer/copy/consumer 依赖、有限 buffer 池、同步/异步/双缓冲、时间线与负收益。CPU 模型、离线编译、W7900 实测分列；资源拿不到就继续本地部分，不推定已经完成七天计划。
2. **LMCache 候选基线更新为 v0.5.6。** 先核对公司版本与设备插件 API，再评估迁移；不自动升级。把安全配置/协议一致性与正确性一起纳入验收。vLLM 主分默认 ROCm 10.0 与 LMCache ROCm 7.2 nightly 不能只按包名拼接，要固定 torch、ROCm、arch、镜像 digest。[S142][S144]
3. **Day 4 加两项本地测试设计，不要求增加 GPU 时长。** ① payload 相同但 scale/dtype/layout 不同的对象不能同 key 命中；② local read 的 hold 必须覆盖实际 copy，timeout 只结束等待，不自动终止设备或远端操作。分别对照 SGLang buffer info、LMCache #5615、MORI #762。[S141][S143][S151]
4. **Day 5 增加双向并发负对照。** 测 H2D alone、D2H alone、两者并发、再叠计算；同时看各路变慢幅度与总时间。MORI #717 的新评论报告单 MI355X 的竞争，是他人的有限实验，不是 W7900 结果；本地先准备矩阵，卡可用再测。[S146]
5. **面试新增三条源码故事。** 退出清 communicator 但不越权销毁 launcher 的 world group（vLLM #62241）；按时间过期不等于读者不再使用（MORI #762）；复制 KV 需覆盖 scale 和层/草稿映射（SGLang #40917）。每条按“结论、源码、自己的证据、未验证边界”陈述，阅读不写成自己的修复。[S141][S143][S144]
6. **kernel 冲刺岗的进阶项。** 若主线闭环已完成，再从 10-16 RDNA GEMM 教程选 1–2 个阶段，在 W7900 做 shape sweep、误差、VGPR/LDS 与耗时对照。不要求七天重写八阶段，也不把 WMMA/RDNA 经验泛化为 CDNA/MFMA 或多卡通信经验。[S148]
7. **投递主线不变。** 中国框架集成方向优先，92727 为 kernel 冲刺；92012 是量化/模型工具相邻方向，用户最近的低精度概念学习有助于面试，但不能等同量化工具或训练实践。91704/87223 的 remote 不是中国雇佣资格证据；89764 仍作为长期通信编译器能力地图。[S136]

---

### 8.10 10-26 个人准备与投递优先级

1. **新增 94063 进入第一投递组。** 它把 C++/Linux、GPU kernel、vLLM/SGLang、HIP/CUDA/ASM 与多 GPU/多节点写在同一职位里，和用户的 ProcessGroupDLCCL、C++ Extension、集合通信、custom allreduce 接入及 CUDA 算子/性能调试形成直接交集。建议与 89393、87545 一起优先；89398/89499/92727 继续作为资深或 kernel 冲刺。官方发布日期、级别与团队仍待确认。[S153]
2. **简历证据不改写。** 可以写“适配 ProcessGroupDLCCL、调整执行流、把 vLLM custom allreduce 接入既有通信算子”；仍不能写“实现通信 kernel”“做过 CUDA IPC”或“完成 AMD 多机优化”。
3. **W7900 主线增加 host-memory 注册对照。** 在已有 pageable/pinned、H2D/D2H、双向并发矩阵上，加 `hipHostRegister` 与 `hipHostMalloc` 的分配/释放成本、首次触页、复用和失败清理；单机无法复现 RDMA MR、NUMA 大池或 MI355X USERPTR queue eviction，就明确留空。[S155][S161]
4. **把失败路径做成面试故事。** 以 vLLM #63628 解释“注册已创建但 descriptor 准备失败时为何必须 rollback”；以 MORI #836 解释“返回失败前仍有 data WR 在飞时为何 buffer 不能释放”；以 SGLang #46455 解释 protocol 与 transport 的 ownership 边界。三者先做源码/测试设计，不冒充本人修复。[S160][S162][S164]
5. **分布式 KV 学习顺序更新。** 先读 ATOM #2634 的 connector 生命周期，再对照 MORI #823 预取与 #825 多 GPU restore，最后回到自研芯片 LMCache 的最小 CPU tier。这样能区分调度 hint、逻辑对象、物理 tier、数据搬运和 completion，不把“有外部 cache”误说成 decode 必然加速。[S162][S163]
6. **megakernel 只作为第二阶段。** 官方文章适合学习 producer-consumer hand-off、持久 kernel、数据局部性和端到端 benchmark 边界；其 MI355X/低精度/特定 drafter 条件不能映射成 W7900 复现任务，也不能把个人 fork 代码当作已进入 ATOM/AITER 正式上游。[S165]

---

### 8.11 11-02 个人匹配、短板与投递定位

1. **94063 仍是最直接主线。** 它明确写 P/D、Large-EP、vLLM/SGLang 和多机多卡，最适合以 ProcessGroupDLCCL、集合通信接入、执行流与 custom allreduce 调用链切入。[S179]
2. **94065 是更资深的 framework/kernel 冲刺。** 职责覆盖 mentoring、强 GPU kernel、compiler 与大规模集群；用户的 C++/Extension/性能定位有交集，但目前缺 AMD/CDNA kernel 与公开 upstream 深度，不宜把它放在 94063 之前。[S179]
3. **96117 与 89635 是深 kernel/算子性能线。** 前者强调 vLLM/SGLang、FlashAttention/PagedAttention、量化和端到端瓶颈；后者强调 AITER、Triton LLIR/ASM、Gluon、roofline 与 MFU。二者能承接 CUDA 算子/低精度学习，但应以一个可复现 kernel 优化和 profiler 证据为投递前置，不把概念理解写成达到 50% MFU 的实绩。[S179]
4. **CUDA IPC 经历先做证据校准。** 本期任务把 CUDA IPC 列入个人经历；简历前需明确：是否调用过 `cudaIpcGetMemHandle/OpenMemHandle`、跨进程共享的是 tensor storage 还是通信库内部 buffer、谁拥有 close/free、进程退出/异常时如何回收、是否测过 P2P 可达性。若只是读源码或间接使用，改写为“理解/排查”，不要升级为独立实现 transport。
5. **新增本地可验证主线。** MORI #867/#862 让没有 AMD 多卡/RDMA 时也能验证 session、status、notification、peer failure、tier placement 和控制流；这比只读大型 PR 更容易形成“结论＋代码＋测试＋硬件边界”的证据包。[S182]
6. **面试新增四个追问。** （a）QP 进入 ERR 后为何 session cache 不能继续返回旧对象；（b）notification post 失败时为何不能立即发布失败；（c）P/D projector 中 measured link 与未测默认参数如何区分；（d）shared DRAM residency 如何避免一个 worker 的 cache spec 污染其他 worker。分别对应 #831、#836、Infera #217、MORI #851/SGLang #46995。[S181][S182][S185]
7. **准备优先级：** `MORI simulated IO/UMBP 回归` → `W7900 hip-kv-transfer-lab` → `自研芯片 LMCache 闭环` → `一个 Triton/HIP kernel 的 W7900 profile`。前两项为外部可展示，第三项注意公司授权/脱敏，第四项服务 96117/89635 冲刺。

---

### 8.12 11-09 个人匹配、短板与准备优先级

1. **96120 提升为最直接第一优先。** 职责把 production-grade 单机/分布式 runtime、vLLM/SGLang/llm-d、TP/PP/EP、MoE、KV、RCCL/RDMA、AITER/HIPBLAS-LT、FP8/FP4 与 upstream 贡献放在同一 Req，和 ProcessGroupDLCCL、PyTorch C++ Extension、集合通信、vLLM custom allreduce 调用链及性能定位形成最完整交集。[S189]
2. **96121 是框架—kernel 联调主线。** Paged/FlashAttention、量化、speculative decoding、compiler/graph pipeline 与 multi-GPU/multi-node 都有相关性；但投递时应把“调用/适配既有算子”和“独立设计 HIP/ASM kernel”分开，后者目前仍缺可公开的 AMD/CDNA 证据。[S190]
3. **第一组建议调整为 96120、94063、89393。** 96121、96117、94065、89499、89635 作为第二组，按 framework/kernel 深度选择；87545 保留历史候选。没有 official datePosted、级别或团队信息时，不用 Req 数字或第三方时间猜发布先后。
4. **CUDA IPC 继续单独校准。** 若实际做过 handle 导出/导入、P2P 可达性、close/free/异常退出回收，就整理成一页 ownership 状态机；若仅通过 NCCL/vLLM 间接使用或读源码，写作“理解与排查”，不写成自研 IPC transport。
5. **面试源码故事更新为三条。** 以 MoRI #907 讲“失败何时可见、buffer 何时可复用”；以 vLLM #66008 讲“READ lease 超时如何产生 silent wrong output”；以 SGLang #49205 讲“跨节点层次化 allreduce 的拓扑、同步和收益边界”。三条均注明是上游阅读/测试设计，不冒充本人提交。[S194][S207][S206]
6. **学习路线加入 ABI 与发布层级。** 对 Infera 0.3.3、MoRI 1.2.5、ATOM 0.1.9、LMCache RC/nightly 固定 tag、commit、ROCm、torch、arch 和镜像；面试时能解释“main 已合入、RC、nightly、preview、stable release”分别证明什么。[S191][S193][S199][S209][S210]
7. **本期准备顺序：** `MORI simulator + WR quiescence 状态机` → `W7900 hip-kv-transfer-lab + ROCTX` → `KV lease/registration + custom allreduce 评审包` → `一个 HIP/Triton kernel 的可复现实测`。第三项可在普通 CPU 上完成代码走查和测试设计；真实性能与 P/D/RDMA 结论留给匹配硬件。

---


## 9. 四周准备路线

**2026-09-28 执行顺序：** 先按现有七天 ROCm/HIP 路线打基础，再推进自研芯片 LMCache 闭环；下面四周知识地图保留，不要求并行完成。当前七天文件已包含自测与面试增补，本手册仅同步准备优先级。（来源 S105）

| 天 | 本地，不依赖 AMD GPU | 实机窗口任务 |
|---|---|---|
| 1 | 栈关系、环境脚本、torch.cuda/HIP 构建识别 | W7900/镜像核验、HIP/PyTorch smoke、profiler 探测 |
| 2 | kernel、CPU reference、边界与计时；审查熟悉的 CUDA reduction 移植假设 | 数值与 H2D/D2H baseline、pageable/pinned 对照 |
| 3 | stream/event 图、双缓冲状态模型、删除等待会破坏的契约 | 真正事件依赖与 buffer 复用压力测试 |
| 4 | KV block/handle/generation、CPU backend；追踪 current stream 和 tensor 生命周期 | 异物理块 roundtrip、有限池与 PyTorch 接入 |
| 5 | 实验矩阵、分析脚本、负对照；读 #2339/#58566 | 重叠时间线、计算干扰、总耗时与负收益解释 |
| 6 | 重读 LMCache #5075、依赖选择/异常/嵌套测试；RCCL 基础 | ROCTX marker + HIP kernel/copy trace；不要求完整大模型 |
| 7 | README、版本、证据表、面试口述与待验证项 | 最终 commit 必要回归；缺卡则顺延 |

上机可合并为 Day1–2、Day3–4、Day5–7 三个窗口。每个答案按“结论＋自己代码/数据＋适用边界”整理；自测重点为跨流依赖、通信返回后存储能否释放、HIP 移植验收、卸载拖慢 decode 的定位、实机验证顺序。单卡实验仍不能证明 RCCL 多卡完成语义或 LMCache 真实 E2E 瓶颈。详细十类面试题及六道项目追问见已更新路线图。（来源 S105）

**2026-09-21 优先级覆盖说明（历史）：** 以下项目地图、MORI/ROCm、Rust 资料保留为复习路线，不要求同时完成。实际主项目改为：第 1 周固定版本/设备接口与同步 baseline；第 2 周 KV roundtrip 和缓存命中闭环；第 3 周端到端 A/B 与生命周期故障测试；第 4 周整理报告、定位一个小而真实的改进，再决定是否提 PR。Rust router 练习延后或作为备用。所有复选框均表示待做，不能当完成记录。

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

- 已做：自研芯片 ProcessGroupDLCCL 适配与执行流调整；
- 已做：vLLM custom allreduce 直接接入已有通信算子，未编写该 kernel；
- 准备中：LMCache 设备适配、正确性与缓存价值测量；
- 没有 CUDA IPC 实践；NCCL 源码、C++ Extension、profiler/sanitizer 等具体深度仅按真实材料描述，不从关键词推断成果。

### 12.6 首要短板

- KV 数据布局、异步完成与 buffer 生命周期的实测闭环；
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

**10-19 当前覆盖说明：** Infera main 已有 opt-in P/D 独立负载释放与 session affinity，仍无 autoscaler；ATOM main 已有受限 dense `mooncake_store` 直连路径，#2459 非合并关闭；MORI main 已有局部 SSD/DRAM 生命周期加固，远端读与全部故障恢复不能由本地 hold 推定。vLLM #60544 已扩展 hybrid WRITE/DSpark，故旧表的“无 WRITE/投机”只适用于当时 #51052；SGLang host pool 抽象已更新但 AMD CI 并非全绿。AIC 仍明示 preview、不建议生产；LMCache 新基线见 5.8、3.12。[S137]–[S144]

**10-12 更新：** Infera 已合入 engine metrics federation；MORI 已合入 peer failure signal 与 VMM/DMA-BUF 释放修复；ATOM 已合入 LMCache MP lookup 锁回收；LMCache 已合入 actual-device sync、ROCm pending-error 清理与 SGLang MP 设备能力判断。它们表明公开栈正在从 feature bring-up 进入 observability、failure propagation 与 lifecycle hardening，但不能据此写成完整 production readiness。详见 3.11。[S123]–[S128]

**09-28 更新覆盖：** Infera 增加安全 rollout/P-D lifecycle，ATOM completion/retention 与 dense fencing 有新合入，SGLang 延迟释放仅对 opt-in 后端默认启用，AIC 仍 preview。详细当前边界见 3.9；下表带 09-21/09-14 日期的版本与 CI 描述保留历史，不冒充本周重新验证。

| 能力 | 公开状态判断 | 岗位含义 |
|---|---|---|
| Infera KV-aware routing / P/D | 已有公开基础能力 | 需要完善策略、兼容性和生产可靠性 |
| Rust router | 已公开代码；#113 已合并 NATS/Kubernetes 相关路径，旧 Open issue 状态有滞后。[S32] | Rust 要求有直接来源，准备需读当前实现 |
| SLA planner / InferaSim | #138/#171 已合入投影、anchor 与 P/D 两池仿真；不等于真实在线 resize。[S56][S66] | 学成本模型、锚点误差与实际调度的边界 |
| Cluster-wide KV | 多条方案正在演进 | 全局索引、tiering、容错是核心增量 |
| MORI-IO | 已进入 vLLM/SGLang；#51052 新增受限 hybrid READ，不含 WRITE/异构TP/投机。[S75] | 仍需兼容更多拓扑并强化错误路径 |
| MORI-EP | 已有 dispatch/combine；09-11 跨节点 EP v2 #625 以 preview 合入。[S54] | 兼容性、特定 NIC/shape 调优与实机回归仍重要 |
| MORI-UMBP | #540/#644 已合入；本期 #679 hugepage 更改被 #687 回滚。[S55][S68] | descriptor、ownership、staging 和失败语义是待补能力，不视为已做过 |
| AIC | 仍 early-access preview；当前 vLLM 0.29.0 / LMCache 0.5.5；emulation #154、accuracy #166 均合入，旧 #147 非合并关闭。[S58][S69][S70] | 测试基础增强，不等于生产或全栈硬件认证；旧 ABI 文档提案撤下 |
| SGLang AMD CI | 09-21 源码仍注释掉 MI355X 分离推理 schedule，手动工作流保留；权限表本周有变更。[S61] | 实机补测有资源门槛；不是代码能力下线 |
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

### 15.1 2026-09-21 既有岗位复核（历史快照）

“开放”依据官方职位正文、`apply_url` 与官方检索可申请字段；没有进行申请提交。上期将 89498 记为上海，本期官方结构化地址和搜索 API 均为北京，应纠正；缺少旧页面完整快照，不能断言它本周搬迁。[S20]–[S25][S65]

| 职位名称 | 地点 | Req ID | 发布日期 | 当前状态 / 变化 | 方向与资格边界 | 官方链接 |
|---|---|---|---|---|---|---|
| AI Software Engineer | 上海 | 89398 | 2026-08-03 | 开放，未确认关键职责变化 | P/D、Large-EP、vLLM/SGLang；Master/PhD、5+ 年；技术最贴近但资深要求明显 | [查看](https://careers.amd.com/careers-home/jobs/89398?lang=en-us) |
| AI Framework Engineer | 上海 | 89500 | 2026-08-26 | 开放 | 框架、KV、continuous batching、性能与上游贡献；不等于已匹配所有要求 | [查看](https://careers.amd.com/careers-home/jobs/89500?lang=en-us) |
| AI Framework Engineer | 上海 | 89499 | 2026-08-26 | 开放 | 偏 expert 的框架/内核/异构集群要求；内部级别仍待确认 | [查看](https://careers.amd.com/careers-home/jobs/89499?lang=en-us) |
| AI Software and GPU Kernel Development Eng. | 上海（历史记录） | 89395 | 2026-08-07（历史记录） | **页面下架/申请不可用待确认**：09-21 多次 404，官方关键词 Req 搜索为 0，inference 中国结果未含此项；上次 09-14 记录开放 | 保留历史；不能确定关闭日期、招满或撤岗原因，也不以邻近 89393 替代其身份 | [历史链接](https://careers.amd.com/careers-home/jobs/89395?lang=en-us) |
| AI Framework Engineer | **北京** | 89498 | 2026-08-26 | 开放；纠正旧表地点 | 3+ 年，PyTorch/TF、kernel、性能、编译器；没有确认 Rust/全局 KV 主责 | [查看](https://careers.amd.com/careers-home/jobs/89498?lang=en-us) |
| AI Framework Eng. | 上海 | 87545 | 2026-06-24 | 开放 | early-career、本科；framework/model/KV。不能再无依据称“低于你的最佳级别” | [查看](https://careers.amd.com/careers-home/jobs/87545?lang=en-us) |
| Software Development Engineer — GPU Fleet Management & AI Infrastructure | San Jose，美国；Hybrid | 92051 | 2026-09-10 | 开放；旧记录保留，不重复算新增 | Rust/控制面；明确无签证赞助，不是中国远程机会 | [查看](https://careers.amd.com/careers-home/jobs/92051?lang=en-us) |

### 15.2 2026-09-21 新增收录与筛除记录（历史快照）

以下均读取官方职位正文，非仅搜索摘要。“新增收录”与“本周新发布”分开；日期为官方 datePosted 的 UTC 日期。

| 职位名称 | 地点 | Req ID | 发布日期 | 状态 / 收录性质 | 与本研究关系 | 官方链接 |
|---|---|---|---|---|---|---|
| Senior Software Development Engineer | 北京 | 92012 | **2026-09-16** | 开放，**本周新发布** | 模型量化、低精度、压缩、Python/C++ 工具、runtime/deployment；列 vLLM/SGLang，但不是已确认通信/KV 团队 | [查看](https://careers.amd.com/careers-home/jobs/92012?lang=en-us) |
| AI Software and GPU Kernel Development Eng. | 北京 | 89393 | 2026-08-11 | 开放，本期首次发现的旧岗位 | 明确 SGLang、HIP/Triton、分布式并行与 collective；和 89395 是不同 Req | [查看](https://careers.amd.com/careers-home/jobs/89393?lang=en-us) |
| Senior GPU Kernel Optimization Engineer | 北京 | 91145 | 2026-08-21 | 开放，本期首次发现的旧岗位 | 4+ 年，要求实际 kernel 开发、profiling、GEMM/Attention/MoE；仅接口适配不能替代此核心要求 | [查看](https://careers.amd.com/careers-home/jobs/91145?lang=en-us) |
| AI Framework Eng. | 上海 | 78999 | 2026-02-25 | 开放，本期首次发现的旧岗位 | 3+ 年；PyTorch/TF、kernel、多机多卡、Python/C++；较宽的框架相邻岗 | [查看](https://careers.amd.com/careers-home/jobs/78999?lang=en-us) |
| AI Framework Engineer | 上海 | 89497 | 2026-08-04 | 开放，本期首次发现的旧岗位 | Master、5+ 年、kernel 与 mentoring；资深档位，不作为默认最匹配 | [查看](https://careers.amd.com/careers-home/jobs/89497?lang=en-us) |
| Software Development Engineer — GPU Fleet Management & AI Infrastructure | San Jose，美国；Hybrid | 92050 | 2026-09-10 | 开放，本期首次发现；与 92051 分开记录 | 控制面、scheduler、inference gateway，production Rust 加分；无签证赞助，不是中国远程机会 | [查看](https://careers.amd.com/careers-home/jobs/92050?lang=en-us) |

**筛除而非遗漏：** 本周 09-18 发布的上海 Sys/Test Validation Engineer **92257** 正文实际是 Client Sensor Fusion Hub / APU / FW/BIOS/传感器验证，inference 只是加分项，不计为大模型推理框架岗位。[官方页面](https://careers.amd.com/careers-home/jobs/92257?lang=en-us) 中国检索中的 GPU compiler 87504 为相邻编译器方向，本期未纳入主候选。Rust 全球搜索也含安全/固件/商务等结果，不把关键词命中全部计为岗位新增。

**分类汇总：** 相关岗位本周新发布 1 条（92012）；补充旧岗位 5 条（89393、91145、78999、89497、92050）；旧清单 6 条仍开放（5 中国 + 1 美国）；1 条页面下架待确认（89395）；1 条地点纠正（89498）；未确认重新开放，未确认截图 exact Req。

**远程边界：** `location=remote` 官方 API 请求返回 422，不能由该请求得出“全球无远程岗位”。已读的 92050/92051 明确 Hybrid/美国；本期未核验到可从中国申请的新增远程机会。上述统计仅覆盖本次检索和阅读范围，不是 AMD 全球招聘总量。

**补充检索范围：** 使用 `country=China` 定向复查 MORI、Infera、vLLM、SGLang、HIP，分别返回 0、0、7、7、11 项；“remote inference”组合返回0。无项目名命中不代表 AMD 没有相关岗位。额外命中的商业销售、方案架构和编译器岗位不自动加入推理框架主表，也不据组合词零结果推断没有远程政策。

### 15.3 对个人投递定位与准备优先级的影响

1. **优先沟通 89500 与同族框架集成方向。** 两项真实适配经历有交集，但多机性能/模型与上游成果仍需补证据。
2. **按年限校准 87545、78999、89498。** 用户年限、学历和职级预期尚不完整，不预设 early-career 太低；89498 地点需按北京考虑。
3. **冲刺 89398 / 89499 / 89497。** 要求资深 E2E 或 kernel 深度，LMCache 项目可增加相关证据，但不能几周内等价补齐多年集群经验。
4. **89393 是引擎/内核方向备选；91145 更强依赖 kernel 实作。** 后者与用户“未写通信算子”的现实有明显差距，不因为同属通信/AI 就提升优先级。
5. **92012 作为量化/部署相邻方向了解；92050/92051 仅作组织技术旁证。** 未确认其与 Infera/MORI/AIC 汇报线，也未确认中国远程资格。

**仍待招聘方确认：** exact Req、内部级别、真实模块分工、是否接受同族岗位调剂、年限/学历等价替代与远程政策。公开开源能力与具体岗位归属分开判断。

---



### 15.4 2026-09-28 岗位复核：访问受限，分开记录事实与线索

**本期无法获得足够正文/申请证据来刷新状态。** 官方详情逐项读取多为 403，部分为无法访问；官方 `/api/jobs` 未成功返回。浏览器对 92727 也只显示 403。没有将错误消息当作职位关闭，也没有拿搜索抓取日期当发布日期。以下地点/发布日期来自已保存的 09-21 一手核验，**不是本周新确认**。[S89]

| 职位名称 | 地点（最后确认） | Req | 发布日（最后确认） | 09-28 状态与变化 | 官方链接 |
|---|---|---|---|---|---|
| AI Software Engineer | 上海 | 89398 | 2026-08-03 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/89398) |
| AI Framework Engineer | 上海 | 89500 | 2026-08-26 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/89500) |
| AI Framework Engineer | 上海 | 89499 | 2026-08-26 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/89499) |
| AI Software and GPU Kernel Development Eng. | 上海 | 89395 | 2026-08-07 | 保留 09-21 页面下架/申请不可用待确认；本期未证实恢复，也未证实正式关闭 | [历史官方](https://careers.amd.com/careers-home/jobs/89395) |
| AI Framework Engineer | 北京 | 89498 | 2026-08-26 | 待复核；保留北京更正 | [官方](https://careers.amd.com/careers-home/jobs/89498) |
| AI Framework Eng. | 上海 | 87545 | 2026-06-24 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/87545) |
| GPU Fleet Management & AI Infrastructure | San Jose / Hybrid | 92051 | 2026-09-10 | 待复核；历史无签证赞助，不作中国 remote | [官方](https://careers.amd.com/careers-home/jobs/92051) |
| Senior Software Development Engineer | 北京 | 92012 | 2026-09-16 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/92012) |
| AI Software and GPU Kernel Development Eng. | 北京 | 89393 | 2026-08-11 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/89393) |
| Senior GPU Kernel Optimization Engineer | 北京 | 91145 | 2026-08-21 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/91145) |
| AI Framework Eng. | 上海 | 78999 | 2026-02-25 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/78999) |
| AI Framework Engineer | 上海 | 89497 | 2026-08-04 | 待复核；09-21 开放 | [官方](https://careers.amd.com/careers-home/jobs/89497) |
| GPU Fleet Management & AI Infrastructure | San Jose / Hybrid | 92050 | 2026-09-10 | 待复核；历史无签证赞助，不作中国 remote | [官方](https://careers.amd.com/careers-home/jobs/92050) |

**新检索线索，尚不纳入已确认岗位变更统计：**

| 官方索引中的名称 | 索引地点 | Req | 发布日期 / 状态 | 线索价值与下一步 | 官方链接 |
|---|---|---|---|---|---|
| Senior GPU Kernel Optimization Engineer | 上海 | 92727 | 未取得 datePosted；实时开放待核实；09-28 首次收录线索 | 索引提到 GPU kernel + coding agents/benchmark/validation。只有取得正文后再确定资格与是否本周新发布；不能视为截图 exact Req | [官方](https://careers.amd.com/careers-home/jobs/92727) |
| Principal Agentic AI Performance Optimization Engineer | Gothenburg，瑞典 | 91704 | 未取得发布日期；实时开放待核实 | 索引出现可考虑 remote，但中国雇佣资格、地点限制、职级必须另核；不能列为已确认可中国远程申请 | [官方](https://careers.amd.com/careers-home/jobs/91704) |
| Sr. Software Engineer – AI Triton Communication | San Jose，美国 | 89764 | 未取得发布日期；实时开放待核实 | 原生 GPU 通信、Triton compiler/runtime 相邻线索；不是已确认中国岗位或 remote | [官方](https://careers.amd.com/careers-home/jobs/89764) |

**本期分类：** 已确认新发布 0、重新开放 0、正式关闭 0、关键职责变化 0，以上均表示“未能确认”，不表示实际数量为零；新增待核实线索 3。原 13 条保留历史。远程搜索另有美国产品/FAE/管理职位命中，未当作目标工程岗或中国 remote 机会。未取得截图 exact Req。[S89]

**对投递的影响：** 继续按 15.3 的框架集成定位准备材料；92727 等只是待核实备选。Hyperloom 和 kernel-agent 关键词同时出现只能作为技术方向关联，不能据此认定岗位隶属其团队。下一次优先恢复官方正文、datePosted 与申请入口核验。

---

### 15.5 2026-10-05 岗位复核：两条线索转为已确认开放

官方职位页面/索引本期重新返回了多条完整正文，并明确显示 `This posting is for an existing vacancy` 或 `Apply`。这足以确认检查时开放，不足以恢复官方页面没有稳定展示的首次发布日期。第三方转发时间不替代 AMD `datePosted`。[S110][S111]

| 职位名称 | 地点 | Req ID | 发布日期 | 10-05 状态 / 变化 | 与用户匹配及边界 | 官方链接 |
|---|---|---:|---|---|---|---|
| **Senior GPU Kernel Optimization Engineer** | 上海 | **92727** | **待官方确认** | **当前开放已确认；由 09-28 线索升级** | CUDA/HIP/Triton kernel、profiling、memory/occupancy/register/shared-memory；要求 4+ 年。用户有 CUDA 算子与性能调试证据，但仍需补 ROCm 实测和更完整 kernel 设计深度 | [官方](https://careers.amd.com/careers-home/jobs/92727) |
| **Sr. Software Engineer - AI Triton Communication** | San Jose，美国；Hybrid | **89764** | **待官方确认** | **当前开放已确认；由 09-28 线索升级** | Triton compiler/runtime 原生 collective、RMA、同步、GPU-initiated communication 与通信计算重叠，高度对应长期方向；但正文明确不提供签证赞助，不是中国远程机会 | [官方](https://careers.amd.com/careers-home/jobs/89764) |
| AI Framework and Performance Experts (vLLM, SGLang) | 北京 | 89393 | 2026-08-11（历史确认） | 当前开放再次确认 | SGLang、HIP/Triton、分布式与 collective；比纯 kernel 岗更接近“框架接口 + 性能”组合 | [官方](https://careers.amd.com/careers-home/jobs/89393) |
| AI Software Engineer | 上海 | 89398 | 2026-08-03（历史确认） | 当前开放再次确认 | 明确 P/D disaggregation、Large-EP、vLLM/SGLang；5+ 年与深 kernel/E2E 要求仍是冲刺边界 | [官方](https://careers.amd.com/careers-home/jobs/89398) |
| AI Framework Engineer | 上海 | 89499 | 2026-08-26（历史确认） | 当前开放再次确认 | vLLM/SGLang、MoE/KV/continuous batching、多机多卡和上游贡献；仍偏资深 | [官方](https://careers.amd.com/careers-home/jobs/89499) |
| AI Framework Eng. | 上海 | 87545 | 2026-06-24（历史确认） | 当前开放再次确认 | framework/model/KV、profiling 与通信优化；学历门槛较宽，具体级别需招聘方确认 | [官方](https://careers.amd.com/careers-home/jobs/87545) |
| Senior Software Development Engineer | 北京 | 92012 | 2026-09-16（历史确认） | 当前开放再次确认 | 量化、runtime/deployment、vLLM/SGLang 相邻；不是已确认 KV/通信主责 | [官方](https://careers.amd.com/careers-home/jobs/92012) |

**未升级或筛除：**

- 91704 已确认是 Gothenburg 的 Principal Agentic AI Performance Optimization Engineer，但正文没有把它变成中国可远程申请岗位；继续列相邻方向，不进入中国优先表。
- 89873/89874/91724 等 Rust、compiler、GPU systems 岗位位于 San Jose，说明 AMD 正在扩大 Rust 进入 GPU runtime/compiler 的范围，但不是截图 exact Req，也未确认可从中国远程申请。
- 89395 继续保留“页面下架/申请不可用待确认”的历史状态；本期没有足够一手证据说明重新开放或正式关闭原因。
- 其余旧 Req 未能逐条取得与上表相同强度的正文/申请证据，因此沿用 15.4 的最后确认状态，不把本期搜索缺失当作关闭。

**本期分类：** 新发布日期可确认 0；此前线索转“当前开放已确认”2 条（92727、89764）；旧岗位再次确认开放 5 条；重新开放 0；正式关闭 0；截图 exact Req 仍未确认。中国/可远程优先范围内，本期没有核实到新的中国远程岗位。

**投递顺序影响：** 中国主线仍优先 89500/87545/89393 等框架集成方向，89398/89499 为冲刺。92727 作为上海 kernel 备选，最需要一份可展示的 HIP/CUDA kernel 性能分析；89764 更像长期能力地图而非当前可落地投递目标。W7900 项目应产出时间线、数值正确性和负收益解释，而不只是“跑过 HIP”。

---

### 15.6 2026-10-12 岗位复核：无新增 exact Req，保留证据差异

本期继续优先使用 AMD 官方 Careers 页面/索引。直接页面在部分抓取路径返回 403，因此只把能够重新取得官方职位正文或明确 `apply today` 信号的条目写成“本期再次确认”；搜索缺失不自动等于关闭。[S122]

| 职位名称 | 地点 | Req ID | 发布日期 | 10-12 状态 / 变化 | 与用户匹配及边界 | 官方链接 |
|---|---|---:|---|---|---|---|
| Senior GPU Kernel Optimization Engineer | 上海 | **92727** | 待官方确认 | **当前开放再次确认** | kernel fusion、memory/occupancy、GEMM/Attention/MoE 与通信计算重叠；W7900 microbenchmark 可补证据，但 4+ 年与深 kernel 要求仍是冲刺边界 | [官方](https://careers.amd.com/careers-home/jobs/92727) |
| AI Framework and Performance Experts (vLLM, SGLang) | 北京 | **89393** | 2026-08-11（历史确认） | **官方正文再次取得** | SGLang、HIP/Triton、distributed parallelism 与 collective；最贴近“框架接口 + 性能”组合 | [官方](https://careers.amd.com/careers-home/jobs/89393) |
| AI Software Engineer | 上海 | **89398** | 2026-08-03（历史确认） | **当前开放再次确认** | P/D、Large-EP、vLLM/SGLang；5+ 年与 E2E 深度仍属冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89398) |
| AI Framework Engineer | 上海 | **89499** | 2026-08-26（历史确认） | **当前开放再次确认** | 框架、MoE/KV、continuous batching、多机多卡和 upstream；建议以 ProcessGroup + LMCache 证据切入 | [官方](https://careers.amd.com/careers-home/jobs/89499) |
| AI Framework Eng. | 上海 | **87545** | 2026-06-24（历史确认） | **官方正文仍可检索** | early-career、Python/C++、PyTorch/vLLM/SGLang；仍是中国主线中较现实的框架岗位 | [官方](https://careers.amd.com/careers-home/jobs/87545) |
| Senior Software Development Engineer / Senior AI Inference Engineer | 北京 | **92012** | 2026-09-16（历史确认） | **官方正文仍可检索；标题索引存在两种展示** | 模型压缩、低精度、runtime/deployment；相邻但不是已确认 KV/通信主责，标题差异需以申请页最终显示为准 | [官方](https://careers.amd.com/careers-home/jobs/92012) |
| AI Framework Eng. | 上海 | **78999** | 2026-02-25（历史确认） | **官方正文再次取得** | C++/Linux、framework/kernel、多机多卡；较宽的框架相邻岗 | [官方](https://careers.amd.com/careers-home/jobs/78999) |
| AI Framework Engineer | 上海 | **89497** | 2026-08-04（历史确认） | 官方正文仍可检索 | 5+ 年、GPU optimization 与 mentoring；资深冲刺，不作为默认最匹配 | [官方](https://careers.amd.com/careers-home/jobs/89497) |
| Sr. Software Engineer - AI Triton Communication | San Jose，美国；Hybrid | **89764** | 待官方确认 | 当前页面仍可检索；**仍无签证赞助** | 长期 Triton communication/RMA/synchronization 能力地图，不是中国 remote | [官方](https://careers.amd.com/careers-home/jobs/89764) |

**未确认变化：** 89500、89498、91145、92050、92051 等本期没有取得与上表同等强度的官方正文/申请信号，沿用最后确认状态；89395 继续保留“页面下架/申请不可用待确认”。没有证据证明它们在本周正式关闭、重新开放或改变地点。

**本期分类：** 新发布 0；重新开放 0；正式关闭 0；本期再次确认/重新取得官方正文 9 条；新的中国 remote 0；截图 exact requisition 仍未确认。

**对投递定位的影响：** 先准备可复用的一套证据，而不是为每个 Req 新建项目：`ProcessGroupDLCCL 调用链 + W7900 HIP 时间线 + LMCache 生命周期闭环` 可同时支撑 87545/89393/89398/89499；92727 另加 kernel roofline、occupancy 和边界尺寸数据。美国 89764 继续只做长期能力地图。

---

### 15.7 2026-10-19 岗位复核：标题明确化与远程范围纠正

**证据强度：** 逐条使用 AMD 官方索引中取得的职位正文，不仅靠结果标题/摘要；直接 Careers 详情/API 多处 403 或无法访问，未提交申请。因此本表用“官方索引仍含正文/Apply”，不把缓存索引当实时申请成功。日期保留历史一手核验；`datePosted` 本期未稳定取得，不能拿 crawl 日期当发布日期。[S136]

| 职位名称 | 地点 | Req ID | 发布日期 | 10-19 状态与本期变化 | 官方链接 |
|---|---|---:|---|---|---|
| AI Framework and Performance Experts (vLLM, SGLang) | 北京 | 89393 | 2026-08-11（历史） | 官方索引正文/Apply 仍在；无确认职责变化；框架与性能主线 | [官方](https://careers.amd.com/careers-home/jobs/89393) |
| AI Software Engineer | 上海 | 89398 | 2026-08-03（历史） | 正文/Apply 仍在；P/D、Large-EP 与 5+ 年要求仍明显 | [官方](https://careers.amd.com/careers-home/jobs/89398) |
| AI Framework Engineer | 上海 | 89499 | 2026-08-26（历史） | 正文/Apply 仍在；资深框架/E2E 方向，非截图 exact Req | [官方](https://careers.amd.com/careers-home/jobs/89499) |
| AI Framework Eng. | 上海 | 87545 | 2026-06-24（历史） | 正文/Apply 仍在；early-career/模型集成方向保留 | [官方](https://careers.amd.com/careers-home/jobs/87545) |
| AI Framework Eng. | 上海 | 78999 | 2026-02-25（历史） | 正文/Apply 仍在；3+ 年与多机多卡基础要求保留 | [官方](https://careers.amd.com/careers-home/jobs/78999) |
| AI Framework Engineer | 上海 | 89497 | 2026-08-04（历史） | 正文/Apply 仍在；5+ 年、mentoring，仍属资深冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89497) |
| Senior GPU Kernel Optimization Engineer | 上海 | 92727 | 待官方确认 | 官方正文仍可取得；4+ 年、kernel 与 coding-agent/验证方向，无确认新变化 | [官方](https://careers.amd.com/careers-home/jobs/92727) |
| **Senior AI Model Quantization Engineer** | 北京 | **92012** | 2026-09-16（历史） | **当前索引标题明确为模型量化**；仍列低精度/压缩、工具/API、训练与部署权衡。上期标题不一致的记录予以更新，但不能确定实际改名日或断言本周新增职责 | [官方](https://careers.amd.com/careers-home/jobs/92012) |
| AI Framework Engineer | 上海 | 89500 | 2026-08-26（历史） | 未重获同等正文/实时申请证据；保留 09-21 最后确认开放，不推定关闭 | [官方](https://careers.amd.com/careers-home/jobs/89500) |
| AI Framework Engineer | 北京 | 89498 | 2026-08-26（历史） | 本期状态待复核；保留北京，不恢复旧上海错误 | [官方](https://careers.amd.com/careers-home/jobs/89498) |
| Senior GPU Kernel Optimization Engineer | 北京 | 91145 | 2026-08-21（历史） | 本期状态待复核，不把搜索无结果当关闭 | [官方](https://careers.amd.com/careers-home/jobs/91145) |
| AI Software and GPU Kernel Development Eng. | 上海（历史） | 89395 | 2026-08-07（历史） | 保留 09-21 页面下架/申请不可用待确认；本期未确认恢复或正式关闭原因 | [历史官方](https://careers.amd.com/careers-home/jobs/89395) |
| Sr. Software Engineer – AI Triton Communication | San Jose，美国 | 89764 | 待官方确认 | 正文/Apply 仍在；明确无签证赞助；不当作中国 remote | [官方](https://careers.amd.com/careers-home/jobs/89764) |
| GPU Fleet Management & AI Infrastructure | San Jose，美国；历史 Hybrid | 92050 / 92051 | 2026-09-10（历史） | 两个独立 Req 均保留历史；本期未重获同等状态证据，不因共享标题混成同一岗位 | [92050](https://careers.amd.com/careers-home/jobs/92050) / [92051](https://careers.amd.com/careers-home/jobs/92051) |
| Principal Agentic AI Performance Optimization Engineer | Gothenburg 索引；正文列 Sweden/Finland/Germany/UK | 91704 | 待官方确认 | 正文/Apply 仍在；remote 只在所列国家办公地点之外可考虑，**未列中国**；不属于中国可远程机会 | [官方](https://careers.amd.com/careers-home/jobs/91704) |
| **Senior Product Manager – AI Inference Software** | Santa Clara 索引；正文 Bay Area/Austin/Remote | **87223** | 待官方确认 | **本期首次收录的相邻产品岗位**，不是本周新发布；无签证赞助、未确认中国 remote，职责偏产品与跨团队，不进入工程投递优先表 | [官方](https://careers.amd.com/careers-home/jobs/87223) |

**分类汇总：** 在本次范围内，已确认本周新发布目标工程岗 0、重新开放 0、正式关闭 0；这些是“未确认有变化”，不是 AMD 全球实际数量的保证。新发现相邻产品 Req 1（87223），既有标题展示明确化 1（92012）；9 条既有中国/美国工程岗重新取得官方索引正文，另 91704 复核欧洲 remote 限定。未取得截图 exact Req。

**检索与筛除记录：** 覆盖 vLLM/SGLang、ROCm/HIP、MORI/Infera、分布式推理、KV、MoE、Rust/C++ 与 remote；综合检索、Req 定向检索及新近页面检索交叉使用。部分强过滤检索返回无关结果，未据此推断零岗位。销售/固件/OpenBMC、产品管理和欧洲 agentic tooling 与目标工程岗分开；没有新一手证据时，不把“Remote”解释为全球任意雇佣。

**对定位的影响：** ProcessGroupDLCCL、已有算子接入、C++ Extension/性能分析仍是框架集成的可迁移基础；vLLM communicator 清理与 SGLang host layout 可作为面试源码案例，但不是用户已做成果。92012 若考虑投递，应额外补低精度方案/精度回归与模型工具证据；91704 和 87223 主要提供组织/能力旁证，不替代中国岗位。[S136][S143][S144]

---

### 15.8 2026-10-26 岗位复核：新增上海 Req 94063

**证据强度：** AMD 官方 Careers 索引当前给出 94063 的标题、上海地址、Engineering 分类和职位正文摘要；直接详情页仍可能 403。官方 `datePosted` 本期未稳定取得，因此发布日期写“待官方确认”。第三方页面称 10-23 首次发现，只用于说明检索时序，不进入 A 级发布日期结论。[S153]

| 职位名称 | 地点 | Req ID | 发布日期 | 10-26 状态 / 变化 | 与用户匹配及边界 | 官方链接 |
|---|---|---:|---|---|---|---|
| **AI Framework Engineer** | **上海** | **94063** | **待官方确认** | **本期新增确认：官方索引当前可检索** | C++/Linux、GPU kernel、vLLM/SGLang、HIP/CUDA/ASM、多 GPU/多节点；与框架通信接入和 CUDA 算子背景直接相关。仍需确认年限、级别、主责是 framework 还是 kernel，以及是否接受 ROCm 经验替代 | [官方](https://careers.amd.com/careers-home/jobs/94063) |
| AI Framework and Performance Experts (vLLM, SGLang) | 北京 | 89393 | 2026-08-11（历史） | 官方索引仍可取得 | 框架/性能主线；与 94063 为不同 Req，不能合并 | [官方](https://careers.amd.com/careers-home/jobs/89393) |
| AI Software Engineer | 上海 | 89398 | 2026-08-03（历史） | 官方索引仍可取得 | P/D、Large-EP，5+ 年要求仍属冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89398) |
| AI Framework Engineer | 上海 | 89499 | 2026-08-26（历史） | 官方索引仍可取得 | MoE/KV/continuous batching、多机多卡；不把新 94063 解释为其重开或替代 | [官方](https://careers.amd.com/careers-home/jobs/89499) |
| Senior AI Model Quantization Engineer | 北京 | 92012 | 2026-09-16（历史） | 官方索引仍可取得 | 量化/低精度/压缩相邻方向，不升级为 KV/通信主线 | [官方](https://careers.amd.com/careers-home/jobs/92012) |
| AI Framework Engineer | 上海 | 89497 | 2026-08-04（历史） | 官方索引仍可取得 | 5+ 年与 mentoring，资深冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89497) |

**状态保留：** 92727、87545、78999、89500、89498、91145、89764、92050/92051、91704 等本期未逐条取得与上表同等强度的官方正文；沿用各自最后确认状态，不把搜索缺失等同正式关闭。89395 继续保留“页面下架/申请不可用待确认”。本期未确认重新开放、正式关闭或新的中国可远程岗位。

**分类汇总：** 本期新增确认中国目标工程 Req 1（94063）；已确认重新开放 0；已确认正式关闭 0；旧中国 Req 再次取得官方索引 5；新中国 remote 0；截图 exact requisition 仍未确认。94063 是新的独立 Req，不因职位名相似就归并进 89499。

**投递顺序：** 第一组建议为 **94063、89393、87545**；第二组为 89398、89499、92727 等资深/深 kernel 冲刺；92012 作为量化相邻。投 94063 时，项目材料优先展示 `ProcessGroupDLCCL 调用链 + W7900 HIP 时间线 + 一个 kernel/传输性能定位案例`，并明确 AMD 实机验证范围。

---

### 15.9 2026-11-02 岗位复核：新增确认 94065、96117，补录 89635

**证据强度：** 下表标题、地点、Req、正文职责和“existing vacancy”来自 AMD 官方 Careers 页面/官方检索索引。页面未稳定暴露 `datePosted`，因此发布日期仍写待官方确认。第三方页面的“几天前发布”只作为发现线索，不进入事实列。[S179]

| 职位名称 | 地点 | Req ID | 发布日期 | 11-02 状态 / 变化 | 匹配度与准备边界 | 官方链接 |
|---|---|---:|---|---|---|---|
| **AI Framework Engineer** | 上海 | **94063** | 待官方确认 | 仍可检索，existing vacancy | **第一投递组。** P/D、Large-EP、vLLM/SGLang、多 GPU/多节点；最贴近 ProcessGroupDLCCL、集合通信和框架接入 | [官方](https://careers.amd.com/careers-home/jobs/94063) |
| **AI framework Eng.** | 上海 | **94065** | 待官方确认 | **本期新确认开放**；独立 Req | 强 kernel/framework、compiler、集群和 mentoring；比 94063 更资深，作为冲刺，不因名称相近并入 94063 | [官方](https://careers.amd.com/careers-home/jobs/94065) |
| **GPU Kernel Performance Engineer** | 上海 | **96117** | 待官方确认 | **本期新确认开放**；官方页面显示 existing vacancy | vLLM/SGLang、Attention/MoE/量化、kernel 和端到端 profiling；适合 CUDA 算子/性能调试延伸，但需要真实 HIP/Triton 优化证据 | [官方](https://careers.amd.com/careers-home/jobs/96117) |
| **AI Optimization Engineer** | 上海 | **89635** | 待官方确认 | **本期首次收录的既有 vacancy**，不声称本周发布 | AITER、Triton LLIR/ASM、Gluon、roofline、MFU；偏算子深度，作为 96117 相邻冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89635) |
| AI Framework and Performance Experts (vLLM, SGLang) | 北京 | 89393 | 2026-08-11（历史） | 官方页面仍可检索 | 第一投递组；SGLang/框架/性能，仍需核对级别 | [官方](https://careers.amd.com/careers-home/jobs/89393) |
| AI Framework Engineer | 上海 | 89499 | 2026-08-26（历史） | 官方页面仍可检索 | MoE/KV/continuous batching、多机多卡；资深冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89499) |
| Senior AI Model Quantization Engineer | 北京 | 92012 | 2026-09-16（历史） | 官方页面仍可检索，existing vacancy | 低精度/量化相邻，不替代分布式推理主线 | [官方](https://careers.amd.com/careers-home/jobs/92012) |

**状态保留：** 92727、87545、78999、89500、89498、91145、89764、92050/92051、91704 等沿用最后确认状态；本期未逐条取得同等强度证据的不据搜索缺失写成关闭。89395 继续保留“页面下架/申请不可用待确认”。未确认新中国 remote、重新开放或正式关闭。

**分类汇总：** 本期新确认开放的中国目标工程 Req 2（94065、96117）；本期首次补录但不确认新发布的既有 Req 1（89635）；再次确认开放 4（94063、89393、89499、92012）；重新开放 0；正式关闭 0；中国 remote 0；截图 exact requisition 仍未确认。

**投递顺序更新：** 第一组 **94063、89393、87545**；第二组 **96117、94065、89499、89398、92727、89635**，按 kernel 证据选择性冲刺；92012 为量化相邻。若一周内只能补一个材料，优先做“异步通信/搬运完成语义 + profiler 时间线”；若冲刺 96117/89635，再补一个 Triton/HIP kernel 的 roofline 与优化前后对照。

---

### 15.10 2026-11-09 岗位复核：新增确认 96120、96121

**证据强度：** 两条新增记录的职位名、地点、Req ID、职责和 existing vacancy 来自 AMD 官方 Careers 正文。官方页面未稳定暴露 `datePosted`，因此发布日期写“待官方确认”；第三方页面时间不进入事实列。其它岗位只有重新取得官方正文/索引或沿用明确的最后确认日期两种状态，不以搜索缺失判定关闭。[S189][S190]

| 职位名称 | 地点 | Req ID | 发布日期 | 11-09 状态 / 变化 | 匹配度与准备边界 | 官方链接 |
|---|---|---:|---|---|---|---|
| **AI Framework and Performance Experts(vLLM)** | 上海，中国 | **96120** | 待官方确认 | **本期新确认开放**；独立 Req，existing vacancy | **最直接第一优先。** production-grade distributed runtime、vLLM/SGLang/llm-d、TP/PP/EP、KV、RCCL/RDMA 与 upstream；最能承接 ProcessGroupDLCCL、集合通信、custom allreduce 接入和 C++ Extension | [官方](https://careers.amd.com/careers-home/jobs/96120?lang=en-us) |
| **AI Software Development Eng.** | 上海，中国 | **96121** | 待官方确认 | **本期新确认开放**；独立 Req，existing vacancy | 框架、Attention/量化/speculative decoding、compiler/graph 与多机多卡；匹配框架联调和性能定位，深 HIP/ASM kernel 证据仍需补 | [官方](https://careers.amd.com/careers-home/jobs/96121?lang=en-us) |
| AI Framework Engineer | 上海，中国 | 94063 | 待官方确认 | 沿用此前官方开放确认 | P/D、Large-EP、vLLM/SGLang；继续第一组 | [官方](https://careers.amd.com/careers-home/jobs/94063?lang=en-us) |
| AI framework Eng. | 上海，中国 | 94065 | 待官方确认 | 官方页面仍可取得 | 资深 framework/kernel/mentoring 冲刺 | [官方](https://careers.amd.com/careers-home/jobs/94065?lang=en-us) |
| GPU Kernel Performance Engineer | 上海，中国 | 96117 | 待官方确认 | 沿用 11-02 最后确认；本期未据搜索缺失判关闭 | 深 kernel、Attention/MoE/量化；需真实 HIP/Triton/profile 证据 | [官方](https://careers.amd.com/careers-home/jobs/96117?lang=en-us) |
| AI Optimization Engineer | 上海，中国 | 89635 | 待官方确认 | 官方页面仍可取得 | AITER/Triton/ASM/roofline；深算子冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89635?lang=en-us) |
| AI Framework and Performance Experts (vLLM, SGLang) | 北京，中国 | 89393 | 2026-08-11（历史） | 官方页面仍可取得 | 第一组；框架/性能，级别待确认 | [官方](https://careers.amd.com/careers-home/jobs/89393?lang=en-us) |
| AI Framework Engineer | 上海，中国 | 89499 | 2026-08-26（历史） | 官方页面仍可取得 | MoE/KV/continuous batching、多机多卡；资深冲刺 | [官方](https://careers.amd.com/careers-home/jobs/89499?lang=en-us) |

**状态保留：** 92012、92727、87545、78999、89500、89498、91145、89764、92050/92051、91704 等保留各自最后确认状态；89395 继续标为“页面下架/申请不可用待确认”。本期未确认已关闭、重新开放或可从中国远程申请的职位。96120/96121 是新的独立 Req，不等同截图 exact requisition，也不由相似标题推断组织归属。

**分类汇总：** 本期新确认开放的中国目标工程 Req 2（96120、96121）；重新开放 0；正式关闭 0；新中国 remote 0；官方发布日期待确认 2；截图 exact requisition 仍未确认。

**投递顺序更新：** 第一组 **96120、94063、89393**；第二组 **96121、96117、94065、89499、89635**，按 framework/kernel 证据选择；87545 与其它历史候选保留。96120 的材料首页应直接呈现 ProcessGroupDLCCL 调用链、集合通信完成语义、vLLM custom allreduce 接入位置、C++ Extension 边界和一次可复现性能定位；96121 再追加 Attention/量化/graph 或 kernel 证据。

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

以下来源以 AMD 官方、ROCm 官方仓库、项目上游仓库和正式文档为主。研究日期为 2026-11-09；早期来源保留为历史，新增证据注明本期日期，roadmap 和 main 可能继续变化。

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
64. **S64 — MORI benchmark 生命周期（现已合并学习案例）** — [#665](https://github.com/ROCm/mori/pull/665) · [#659](https://github.com/ROCm/mori/pull/659) · [#660](https://github.com/ROCm/mori/pull/660) · [#664](https://github.com/ROCm/mori/pull/664)。#665 创建09-12、09-14合并，作者jhchouuu；#660亦于09-17合并。其它条目只保留历史相关性，不以标题推断当前实现。


### 2026-09-21 新增与复核来源

65. **S65 — AMD Careers 官方检索 API** — [来源](https://careers.amd.com/api/jobs?keywords=inference&location=China&limit=100)。09-21：12项；正文与申请字段交叉核对，主表逐条保留官方链接。
66. **S66 — InferaSim width transport / P-D 两池仿真 #171** — [来源](https://github.com/AMD-AGI/Infera/pull/171)。09-16合并，读取正文和main提交。
67. **S67 — MORI SDMA AllGather graph capture #652** — [来源](https://github.com/ROCm/mori/pull/652)。09-20合并；核对device generation、可见性与replay测试。
68. **S68 — MORI 回滚 UMBP hugepage #687** — [来源](https://github.com/ROCm/mori/pull/687)。09-18合并，撤回#679。
69. **S69 — AIC differential accuracy gate #166** — [来源](https://github.com/ROCm/rocm-aic/pull/166)。09-17合并；并读旧#147评论、tests/accuracy/test_accuracy.py与self-hosted工作流。
70. **S70 — AIC build/版本拆分 #168** — [来源](https://github.com/ROCm/rocm-aic/pull/168)。09-18合并；当前README和docker/Dockerfile另行核对，不照搬旧PR中的删除声明。
71. **S71 — ATOM KV offload overhead #2223** — [来源](https://github.com/ROCm/ATOM/pull/2223)。09-15合并；作者报告单次各组实测、异步单项变慢与combined方案。
72. **S72 — ATOM plugin 精确 block leases #2284** — [来源](https://github.com/ROCm/ATOM/pull/2284)。09-20合并；保留未打通source-safe通知及无效throughput对照的限制。
73. **S73 — ATOM P-D 整体回滚 #2315** — [来源](https://github.com/ROCm/ATOM/pull/2315)。09-20合并；完整GPU回归仍待验证，fencing/readiness也被撤回。
74. **S74 — vLLM ROCm native CPU offload #57160** — [来源](https://github.com/vllm-project/vllm/pull/57160)。09-18合并；每rank私有pinned tensor，不是LMCache backend。
75. **S75 — vLLM MoRIIO hybrid READ #51052** — [来源](https://github.com/vllm-project/vllm/pull/51052)。09-20合并；等TP、无speculation等边界与作者实测分开记录。
76. **S76 — SGLang MORI + DSpark + DP #39910** — [来源](https://github.com/sgl-project/sglang/pull/39910)。09-17合并；静态verify等限制仍存在。
77. **S77 — LMCache device namespace 重构 #4957** — [来源](https://github.com/LMCache/LMCache/pull/4957)。09-19合并；当前platform/devices目录为适配基线。
78. **S78 — LMCache 实际KV设备同步 #5157（09-21 历史快照）** — [来源](https://github.com/LMCache/LMCache/pull/5157)。当时 Open/APPROVED；**已于 10-08 合并，v0.5.6 包含此修复**，当前结论见 S127/S142，不再列待认领。
79. **S79 — LMCache 新设备适配指南** — [来源](https://github.com/LMCache/LMCache/blob/dev/docs/source/developer_guide/extending_lmcache/adding_a_new_device_backend.rst)。09-21正文：in-tree/外部wheel，DeviceSpec/DeviceOps，engine-driven先行。
80. **S80 — LMCache padded MLA / BSV_BSS torch fallback #5133** — [来源](https://github.com/LMCache/LMCache/pull/5133)。09-16创建/更新，Open；作者限定raw pointer ABI，不声称全平台适配。
81. **S81 — AMD MLPerf Inference v6.1 技术详解** — [来源](https://rocm.blogs.amd.com/artificial-intelligence/mlperf-inf-v6.1/README.html)。09-17发布，正文来自ROCm/rocm-blogs官方源码；仅作指定benchmark栈的技术证据。
82. **S82 — Thread Trace Part 1: ROCprof Compute Viewer** — [来源](https://rocm.blogs.amd.com/software-tools-optimization/thread-trace/README.html)。09-15发布；完整取回官方文章源码，关注instruction trace与性能诊断。
83. **S83 — 北京 GPU/Framework 岗位 89393** — [来源](https://careers.amd.com/careers-home/jobs/89393?lang=en-us)。08-11发布，本期首次收录而非本周新发布。
84. **S84 — 北京模型优化岗位 92012** — [来源](https://careers.amd.com/careers-home/jobs/92012?lang=en-us)。09-16发布；量化/低精度/部署相邻方向。
85. **S85 — San Jose Fleet Manager 岗位 92050** — [来源](https://careers.amd.com/careers-home/jobs/92050?lang=en-us)。09-10发布，本期补充；Hybrid、无签证赞助。
86. **S86 — MORI CCO GEMM/AR 融合 #662** — [来源](https://github.com/ROCm/mori/pull/662)。09-17合并；特定形状、构建自检与SDMA条件。
87. **S87 — SGLang MORI intranode grid clamp #39763** — [来源](https://github.com/sgl-project/sglang/pull/39763)。09-16合并；full serving验证当时仍标进行中。
88. **S88 — AIC README PyTorch/AITER 同步 #160** — [来源](https://github.com/ROCm/rocm-aic/pull/160)。09-15合并；旧文档矛盾提案移入历史。

### 2026-09-28 新增与复核来源

89. **S89 — 岗位读取与新线索核验（09-28）** — [来源](https://careers.amd.com/careers-home/jobs/92727)。旧 13 条链接见15.4，另91704/89764；本期官方直读403/不可访问，搜索仅作线索，发布日期与实时状态留空。
90. **S90 — Infera 更新 roadmap 与安全 rollout** — [来源](https://github.com/AMD-AGI/Infera/issues/9)。09-24更新；PR #173(09-23 merged)、#176(09-24 merged)；当前readiness.py/builders.go另核。
91. **S91 — MORI distributed ranged read** — [来源](https://github.com/ROCm/mori/pull/656)。09-24 merged；核对pool_client.cpp；作者同主机NIC loopback，不是双机。
92. **S92 — MORI wide EP barrier** — [来源](https://github.com/ROCm/mori/pull/709)。09-24 merged；当前ep_intranode_kernel.hpp含last-arrival-reset；PR实机计划未勾选。
93. **S93 — MORI SDMA device-post 死锁在研补丁** — [来源](https://github.com/ROCm/mori/pull/711)。09-24创建、09-27更新、Open；有作者，未合并。
94. **S94 — ATOM completion 与源块保留分离** — [来源](https://github.com/ROCm/ATOM/pull/2167)。09-22 merged；核对chunked_scheduler.py中的source_blocks_released与should_defer_free。
95. **S95 — ATOM dense LMCache producer fence** — [来源](https://github.com/ROCm/ATOM/pull/2339)。09-25 merged；当前_block_gpu_connector.py已包含event→pack stream wait；实机结果的head范围见正文。
96. **S96 — ATOM hybrid offload 与 lookup memo** — [来源](https://github.com/ROCm/ATOM/pull/2268)。另#2305，两者09-23 merged；保留KDA joint hit和DSV4未覆盖边界。
97. **S97 — ATOMesh streaming P/D 负载** — [来源](https://github.com/ROCm/ATOM/pull/2351)。09-22 merged；作者CPU HTTP/Rust验证，无新增GPU throughput结论。
98. **S98 — SGLang drain ACK / 默认延迟释放 / fan-out** — [来源](https://github.com/sgl-project/sglang/pull/41402)。另#40645/#41023；09-22/24/27 merged；读#38961维护者评论与main common/conn.py，MoRI未opt-in。
99. **S99 — vLLM ROCm AsyncTP 与冗余拷贝** — [来源](https://github.com/vllm-project/vllm/pull/58098)。另#58566；09-23/25 merged，当前layers/utils.py复核；限制BF16/多卡与特定工作负载。
100. **S100 — AIC PR manifest 与 emulation review** — [来源](https://github.com/ROCm/rocm-aic/pull/176)。另#173/#177/#178；README仍preview；CONTRIBUTING和仓库权限字段再核。
101. **S101 — Hyperloom 官方技术文章** — [来源](https://rocm.blogs.amd.com/software-tools-optimization/hyperloom-optimization/README.html)。09-21发布、官方仓库09-24更新；闭环测量/复验的方法学，不作普遍收益保证。
102. **S102 — Kimi-K3 三框架 MAD benchmark** — [来源](https://rocm.blogs.amd.com/artificial-intelligence/kimi-k3-mad/README.html)。09-22文章，实际07-29测量；读取ROCm/rocm-blogs release正文及限制。
103. **S103 — ATT profiling guide Part6** — [来源](https://rocm.blogs.amd.com/software-tools-optimization/profiling-guide/att/README.html)。09-22文章、09-23修改；gfx11在文档支持范围，实例工具仍需核验。
104. **S104 — UltraQuant 4-bit KV** — [来源](https://rocm.blogs.amd.com/software-tools-optimization/ultraquant-kv4/README.html)。09-25文章；读取官方release正文，upstreaming/fused multi-token仍列未来工作。
105. **S105 — 用户当前七天路线图（09-24，第2版）** — ROCm_HIP_7_Day_W7900_Roadmap_2026-09-24.md；09-28读取当前文件目标/每日总表。用户提供W7900额度与可用性约束；不含实测完成证据。
106. **S106 — LMCache ROCTX 与 device-sync 候选** — [来源](https://github.com/LMCache/LMCache/pull/5075)。#5075仍Open；读取patch、dev utils.py、head b8085450... check-runs与评论；ROCm skipped。另#5157仍Open且有APPROVED。
107. **S107 — 贡献候选09-28状态复核** — [来源](https://github.com/AMD-AGI/Infera/issues/36)。19.12所列issue/PR REST元数据、重点comments/reviews及源码；#621变为非Draft且指派isytwu；个人sglang-amd仍fork。
108. **S108 — vLLM gfx1100 FP8 KV 补测候选** — [来源](https://github.com/vllm-project/vllm/pull/57126)。Open，assignee shen-shanshan，已有W7900D性能结果；不是待从零修复，也未合并。
109. **S109 — 当前 upstream 贡献与CI规则** — [来源](https://github.com/vllm-project/vllm/blob/main/docs/contributing/README.md)。并读SGLang contribution guide；记录6个Open PR上限、DCO/AI披露与CI授权/分支新鲜度要求，不代表用户实际权限。

### 2026-10-05 新增与复核来源

110. **S110 — AMD 中国岗位正文复核（10-05）** — [92727](https://careers.amd.com/careers-home/jobs/92727)、[89393](https://careers.amd.com/careers-home/jobs/89393)、[89398](https://careers.amd.com/careers-home/jobs/89398)、[89499](https://careers.amd.com/careers-home/jobs/89499)、[87545](https://careers.amd.com/careers-home/jobs/87545)、[92012](https://careers.amd.com/careers-home/jobs/92012)。官方页面/索引显示职位正文与 existing vacancy / Apply；未稳定取得的 datePosted 留待确认。
111. **S111 — AMD Triton 通信与相邻 Rust 岗位（10-05）** — [89764](https://careers.amd.com/careers-home/jobs/89764)。正文确认 San Jose、Hybrid、无签证赞助及 Triton native distributed communication 职责；89873/89874/91724 仅作相邻 Rust/compiler 方向，不当作中国 remote。
112. **S112 — Infera 当前公开能力与限制** — [来源](https://github.com/AMD-AGI/Infera)。当前 README 列 v0.1.1 镜像、OpenAI/Anthropic API、三引擎、AIC tiering、safe drain/rollout、Rust router 与 Kubernetes；同时明确 PyPI/Rust wheel 未交付、没有 scaling controller，并将 MI355X 数字标为作者测量。
113. **S113 — InferaSim PP 成本模型 #179** — [来源](https://github.com/AMD-AGI/Infera/pull/179)。10-01 创建、Open；PP hop host time、token return 与跨节点 NIC 成本，作者报告 448 projection tests 与 MI355X 校准。
114. **S114 — MORI UMBP restore gather #717** — [来源](https://github.com/ROCm/mori/pull/717)。09-30 创建、Open；H2D 多段 restore 保留 gather kernel，D2H 单独阈值；数据为作者 8×MI355X benchmark。
115. **S115 — MORI UMBP NUMA prefault #718** — [来源](https://github.com/ROCm/mori/pull/718)。09-30 创建、Open；未绑定 DRAM tier 跨 NUMA 并行 first-touch，作者报告双路 8×MI355X 注册/ready 时间。
116. **S116 — MORI CCO SDMA 死锁 #711 复核** — [来源](https://github.com/ROCm/mori/pull/711)。10-05 仍 Open、等待评审、无 assignee；正文给出 process-wide queue、两类死锁、gate 复现与验证矩阵。
117. **S117 — ATOM LMCache MP + Mooncake L2 #2459** — [来源](https://github.com/ROCm/ATOM/pull/2459)。10-03 创建、Open；每 NUMA LMCache MP server 与跨节点 Store L2 两种在研路径，作者 GLM-5.2/MI355X 数据不作通用保证。
118. **S118 — ATOM 直连 Mooncake Store #2464** — [来源](https://github.com/ROCm/ATOM/pull/2464)。10-03 创建、Draft；绕过 LMCache 的 pack/put/get/unpack 方案，与 #2459 作者对照；未进入 release。
119. **S119 — AIC emulation/VM 状态与门槛** — [#177](https://github.com/ROCm/rocm-aic/pull/177)、[#178](https://github.com/ROCm/rocm-aic/pull/178)。两者10-05仍Open；#178 仍等待 code-owner review，约54GB镜像使标准GHA pull_request lane被移除；#181/#182为后续构建/集群调整。
120. **S120 — 当前仓库贡献入口与限制** — [Infera Issues](https://github.com/AMD-AGI/Infera/issues)、[MORI PRs](https://github.com/ROCm/mori/pulls)、[AIC PRs](https://github.com/ROCm/rocm-aic/pulls)、[LMCache PRs](https://github.com/LMCache/LMCache/pulls)。10-05 快照；Infera 页面明确 issue creation restricted。列表状态只说明公开页面，不推断内部 ownership。
121. **S121 — ATOM v0.1.6 release** — [来源](https://github.com/ROCm/ATOM/releases/tag/v0.1.6)。09-22 发布，提供 ROCm 10.0 与 7.2 wheel；不包含 10-03 创建的 #2459/#2464。

### 2026-10-12 新增与复核来源

122. **S122 — AMD 岗位官方页/索引复核（10-12）** — [92727](https://careers.amd.com/careers-home/jobs/92727)、[89764](https://careers.amd.com/careers-home/jobs/89764)、[89393](https://careers.amd.com/careers-home/jobs/89393)、[89398](https://careers.amd.com/careers-home/jobs/89398)、[89499](https://careers.amd.com/careers-home/jobs/89499)、[87545](https://careers.amd.com/careers-home/jobs/87545)、[92012](https://careers.amd.com/careers-home/jobs/92012)、[78999](https://careers.amd.com/careers-home/jobs/78999)、[89497](https://careers.amd.com/careers-home/jobs/89497)。本期再次取得官方正文或申请索引；未稳定取得 `datePosted` 的条目继续标待确认，搜索缺失不作关闭证明。
123. **S123 — Infera metrics federation #183** — [来源](https://github.com/AMD-AGI/Infera/pull/183)。10-08 创建、10-10 合并；Python/Rust router 的 TTFT/ITL/token 指标与 engine metrics federation。合并不等于 autoscaling controller。
124. **S124 — MORI peer failure #716** — [来源](https://github.com/ROCm/mori/pull/716)。09-28 创建、10-10 合并；修正永远返回 true 的 liveness，暴露 QP/port/device fatal 事件。仍不覆盖全部 deadline/reconnect。
125. **S125 — MORI VMM DMA-BUF 生命周期 #729** — [来源](https://github.com/ROCm/mori/pull/729)。10-08 创建、10-09 合并；allocation handle 导出与 HIP 7.2/7.16 retain/release 差异，作者 8×MI355X/Pollara 验证。
126. **S126 — ATOM LMCache MP lookup 锁泄漏 #2518** — [来源](https://github.com/ROCm/ATOM/pull/2518)。10-10 创建并合并；未消费 async lookup、hit count ownership 与 L1 read-lock 回收。
127. **S127 — LMCache actual-device synchronization #5157** — [来源](https://github.com/LMCache/LMCache/pull/5157)。09-17 创建、10-08 合并；同步跟随 KV tensor device，CPU 跳过 accelerator sync，保留现有 async event/lifetime contract。
128. **S128 — LMCache ROCm/SGLang 设备抽象修复** — [#5565](https://github.com/LMCache/LMCache/pull/5565)、[#5611](https://github.com/LMCache/LMCache/pull/5611)。分别 10-09、10-10 合并；清理 pending HIP error，移除 unified MP 的硬编码 CUDA gate。
129. **S129 — MORI-IO fault injection #731** — [来源](https://github.com/ROCm/mori/pull/731)。10-09 创建、10-12 仍 Open；已有作者，提供 verbs seam 与 post/CQE/QP 故障注入，本 PR 明确尚不改变默认故障处理行为。
130. **S130 — AIC LMCache P2P emulated E2E #183** — [来源](https://github.com/ROCm/rocm-aic/pull/183)。10-05 创建、10-12 仍 Open；已有作者/assignee，以 QEMU/KVM 与 emulated ionic RDMA 验证 P2P load counter，不是物理 GPU/RDMA 性能证明。
131. **S131 — ATOM 分层 KV 两路线复核** — [#2459](https://github.com/ROCm/ATOM/pull/2459)、[#2464](https://github.com/ROCm/ATOM/pull/2464)。10-12 分别 Draft/Open；两者都有作者和特定 GLM-5.2/MI355X 数据，尚未进入 release。
132. **S132 — LMCache ROCTX 与 padded layout 状态** — [#5075](https://github.com/LMCache/LMCache/pull/5075)、[#5133](https://github.com/LMCache/LMCache/pull/5133)。10-12 均 Open；#5075 为 3 commits、无 reviewer、19/29 checks；#5133 CPU regression 完成，GPU runtime/stream/E2E 未验证。
133. **S133 — AIC RocJITSU emulation 状态** — [#177](https://github.com/ROCm/rocm-aic/pull/177)、[#178](https://github.com/ROCm/rocm-aic/pull/178)。#177 于 10-05 20:07 UTC 合并 CPU-only emulator sweep 与 Pages 历史发布；#178 在 10-12 仍 Open，QEMU/KVM gfx1250 compose gate 受上游 MES queue 限制，不是物理 GPU 性能验证。
134. **S134 — vLLM ROCm island all-reduce 与 deferred all-reduce** — [#61109](https://github.com/vllm-project/vllm/pull/61109)、[#61119](https://github.com/vllm-project/vllm/pull/61119)。10-11 创建，10-12 分别 Open/Draft；均已有作者。#61109 面向 2×4 XGMI-island MI210 TP8，#61119 面向 AMD MiniMax-M3 FFN reduction 延后；性能与精度数字为作者报告。
135. **S135 — SGLang Mooncake abort 与 NIXL staging** — [#43719](https://github.com/sgl-project/sglang/pull/43719)、[#43723](https://github.com/sgl-project/sglang/pull/43723)。10-11 创建、10-12 仍 Open；#43719 以 poison room 防止 completion-unknown 时过早复用 KV page，#43723 修正 staging `slot_layer_ids`，无单测且当前页面仍显示 CI failure。

### 2026-10-19 新增与复核来源

136. **S136 — AMD Careers 本期官方索引/正文与远程范围** — [来源](https://careers.amd.com/careers-home/jobs/92012)。10-19：92012 当前标题；89393/89398/89499/87545/78999/89497/92727/89764 正文；另 [91704](https://careers.amd.com/careers-home/jobs/91704)、[87223](https://careers.amd.com/careers-home/jobs/87223)。直接详情/API 部分 403，不冒充实时申请验证；发布日期历史沿用或待确认。
137. **S137 — Infera main 路由生命周期与 preflight** — [来源](https://github.com/AMD-AGI/Infera/pull/186)。另 [#185](https://github.com/AMD-AGI/Infera/pull/185)、[#192](https://github.com/AMD-AGI/Infera/pull/192)、[#197](https://github.com/AMD-AGI/Infera/pull/197)；元数据、正文、review 与 main session_affinity.rs 交叉核对，默认/opt-in 与物理 KV ownership 分开。
138. **S138 — Infera 开发分支与 nightly 在研变化** — [来源](https://github.com/AMD-AGI/Infera/pull/198)。[#203](https://github.com/AMD-AGI/Infera/pull/203) base=dev/yaoc/glm5.3-atom-20261013；比较其 merge commit 与 main，main 落后12 commits，不在 main 已交付能力中。
139. **S139 — MORI 已合并状态纠正** — [来源](https://github.com/ROCm/mori/pull/711)。另 [#731](https://github.com/ROCm/mori/pull/731)、[#621](https://github.com/ROCm/mori/pull/621)；分别10-13、10-12、09-30合入。#711 讨论纠正早期内存排序解释；#731 不保证全部故障恢复。
140. **S140 — MORI NUMA/USERPTR/错误清理** — [来源](https://github.com/ROCm/mori/pull/756)。另 [#718](https://github.com/ROCm/mori/pull/718)、[#761](https://github.com/ROCm/mori/pull/761)，均10-13合并；核对main standalone锁范围与host registration。作者硬件数据只对其配置成立。
141. **S141 — MORI eviction 与本地读 hold** — [来源](https://github.com/ROCm/mori/pull/762)。另 [#741](https://github.com/ROCm/mori/pull/741)、[#763](https://github.com/ROCm/mori/pull/763)、[#774](https://github.com/ROCm/mori/pull/774)；当前 [medium_backend.h](https://github.com/ROCm/mori/blob/main/src/umbp/include/umbp/distributed/peer/backend/medium_backend.h) 可见 ResolveReader/hold，远端 timed lease 另处理。
142. **S142 — LMCache v0.5.6、安全公告与 ROCm nightly** — [来源](https://github.com/LMCache/LMCache/releases/tag/v0.5.6)。10-14 22:21 UTC发布；[#5157 merge→tag compare](https://github.com/LMCache/LMCache/compare/f06af81699f1fb0cd2a15ceb6f959fc2682daca5...v0.5.6) ahead=37/behind=0；[GHSA](https://github.com/LMCache/LMCache/security/advisories/GHSA-w5f2-9q9c-ff4h) 10-13发布、标patched 0.5.6；[nightly-rocm](https://github.com/LMCache/LMCache/releases/tag/nightly-rocm) 10-18仍gfx942/gfx950、ROCm7.2/torch2.11。公告含历史段落，容器/示例安全补丁是否在特定tag以release notes与源码确认，不一概归入0.5.6。
143. **S143 — SGLang ACK、staging 与 host buffer info** — [来源](https://github.com/sgl-project/sglang/pull/40917)。另 [#44968](https://github.com/sgl-project/sglang/pull/44968)、[#43719](https://github.com/sgl-project/sglang/pull/43719)、[#43723](https://github.com/sgl-project/sglang/pull/43723)；读取正文与main device_pool_info.py、Mooncake conn.py；CPU/model作者结果与AMD CI failure分开。
144. **S144 — vLLM hybrid WRITE、ROCm 默认栈与退出清理** — [来源](https://github.com/vllm-project/vllm/pull/60544)。另 [#58761](https://github.com/vllm-project/vllm/pull/58761)、[#62241](https://github.com/vllm-project/vllm/pull/62241)；main moriio_connector_usage.md 与 uniproc_executor.py 核对，后者只销毁model parallel而非default/world group。
145. **S145 — 本期既有贡献候选元数据与验证限制** — [来源](https://github.com/LMCache/LMCache/pull/5075)。#5075 head b8085450 的28 check-runs为18 success/10 skipped，reviews=[]；读取patch与dev utils.py。另 #5133、Infera#179/#188/#198、MORI#632、AIC#178/#181/#183/#184、vLLM#57126/#61109/#61119、SGLang#38164 的创建/更新/作者/assignee/comments与重点讨论；明细链接见19.15。
146. **S146 — MORI 在研 gather/AsyncLL/远端生命周期** — [来源](https://github.com/ROCm/mori/pull/717)。10-14评论为单MI355X并发restore/store竞争报告；另 [#768](https://github.com/ROCm/mori/pull/768)、[#787](https://github.com/ROCm/mori/pull/787)、[#788](https://github.com/ROCm/mori/pull/788)。#787/#788为既有作者Draft；#791已非合并关闭，不把它当开放新题。
147. **S147 — 当前贡献指南与 CI 门禁** — [来源](https://github.com/ROCm/mori/pull/744)。[当前rerun workflow](https://github.com/ROCm/mori/blob/main/.github/workflows/ci-rerun.yml)要求write；并读Infera CONTRIBUTING、MORI README、AIC CONTRIBUTING、[vLLM指南](https://github.com/vllm-project/vllm/blob/main/docs/contributing/README.md)、[SGLang指南](https://docs.sglang.io/docs/developer_guide/contribution_guide)。本研究未触发CI/测试用户权限。
148. **S148 — RDNA FP16 GEMM 官方教程** — [来源](https://rocm.blogs.amd.com/software-tools-optimization/rdna-fp16-gemm/README.html)。10-16发布，W7800/gfx1100等、ROCm10、FP16 accumulation。作为W7900进阶方法，不移用作者数值、不保证任意输入精度。
149. **S149 — GLM-5.3 MI300X DP8+EP8 官方 recipe** — [来源](https://rocm.blogs.amd.com/artificial-intelligence/glm53-mi300x-vllm/README.html)。10-14发布，8×MI300X/ROCm7.2.3/vLLM0.28.0、两个AITER补丁；长/短负载结论不同，不作W7900部署计划。
150. **S150 — Roadmap 与仓库身份/入口当前快照** — [来源](https://github.com/sgl-project/sglang/issues/35003)。metadata更新10-02，纠正旧08-18；Infera#9仍09-24、MORI#348仍06-15。JohnQinAMD/sglang-amd仍fork、Issues关闭；AIC Discussions=false；Infera Issues本期未复现restricted提示，账号权限未实测。
151. **S151 — LMCache 在研 key/错误传播工作** — [来源](https://github.com/LMCache/LMCache/pull/5615)。另 [#5841](https://github.com/LMCache/LMCache/pull/5841)；均Open、有作者，前者有17条inline review、后者为CPU ZMQ错误回传工作。只列评审/测试方法，不称已发布修复。
152. **S152 — ATOM 两条 Store 路线的当前落点** — [来源](https://github.com/ROCm/ATOM/pull/2464)。10-13入main；[#2459](https://github.com/ROCm/ATOM/pull/2459)10-12非合并关闭。读多轮讨论、files与main [taint.py](https://github.com/ROCm/ATOM/blob/main/atom/kv_transfer/offload/mooncake_store/taint.py)。最新ATOM release v0.1.7发布10-08，早于#2464合并，不能声称该release含此功能。

### 2026-11-02 新增与复核来源

179. **S179 — AMD Careers 上海推理框架与 kernel 岗位** — [94063](https://careers.amd.com/careers-home/jobs/94063)、[94065](https://careers.amd.com/careers-home/jobs/94065)、[96117](https://careers.amd.com/careers-home/jobs/96117)、[89635](https://careers.amd.com/careers-home/jobs/89635)，以及 [89393](https://careers.amd.com/careers-home/jobs/89393)、[89499](https://careers.amd.com/careers-home/jobs/89499)、[92012](https://careers.amd.com/careers-home/jobs/92012)。11-02 官方页面/索引显示标题、地点、Req、正文和 existing vacancy；官方发布日期未稳定取得。
180. **S180 — Infera v0.3.1/v0.3.2 与 SGLang/ATOM release 基线** — [v0.3.1](https://github.com/AMD-AGI/Infera/releases/tag/v0.3.1)、[v0.3.2](https://github.com/AMD-AGI/Infera/releases/tag/v0.3.2)、[#210](https://github.com/AMD-AGI/Infera/pull/210)、[#214](https://github.com/AMD-AGI/Infera/pull/214)。分别 10-26/10-29 发布；#210/#214 已合入，纠正上期 Open/无 release 状态。
181. **S181 — Infera projector、MoRI/UMBP 与 P/D 估算** — [#215](https://github.com/AMD-AGI/Infera/pull/215)、[#216](https://github.com/AMD-AGI/Infera/pull/216)、[#217](https://github.com/AMD-AGI/Infera/pull/217)、[#219](https://github.com/AMD-AGI/Infera/pull/219)、[#225](https://github.com/AMD-AGI/Infera/pull/225)。均 10-30 合入；测量锚点、未测默认参数与真实数据面严格分开。
182. **S182 — MORI 预取、QP/完成语义与模拟后端** — [#823](https://github.com/ROCm/mori/pull/823)、[#831](https://github.com/ROCm/mori/pull/831)、[#836](https://github.com/ROCm/mori/pull/836)、[#851](https://github.com/ROCm/mori/pull/851)、[#862](https://github.com/ROCm/mori/pull/862)、[#867](https://github.com/ROCm/mori/pull/867)。均已合入；#862/#867 保留控制流但模拟 payload/硬件时序，不能当真实 RDMA 性能。
183. **S183 — MORI EP/SDMA 合入与在研多流/直连** — [#843](https://github.com/ROCm/mori/pull/843)、[#866](https://github.com/ROCm/mori/pull/866) 已合入；[#825](https://github.com/ROCm/mori/pull/825)、[#875](https://github.com/ROCm/mori/pull/875)、[#884](https://github.com/ROCm/mori/pull/884) 仍 Open/Draft、有作者。作者硬件数字不视为本研究复现。
184. **S184 — vLLM ROCm/MoRI/通信状态** — [#61361](https://github.com/vllm-project/vllm/pull/61361)、[#63142](https://github.com/vllm-project/vllm/pull/63142)、[#63628](https://github.com/vllm-project/vllm/pull/63628) 已合入；[#61109](https://github.com/vllm-project/vllm/pull/61109)、[#61119](https://github.com/vllm-project/vllm/pull/61119)、[#64428](https://github.com/vllm-project/vllm/pull/64428) 仍在评审。最新 release v0.32.0 早于这些合入。
185. **S185 — SGLang Transport、共享 DRAM 与 AMD DCP** — [#46455](https://github.com/sgl-project/sglang/issues/46455)、[#46462](https://github.com/sgl-project/sglang/issues/46462)、[#46995](https://github.com/sgl-project/sglang/pull/46995)、[#47309](https://github.com/sgl-project/sglang/pull/47309)。均 Open/Draft；#47309 stacked 在其它 PR 上，性能数字不可拆分归因。
186. **S186 — ATOM 分层 KV/Rust 与新 correctness seam** — [#2634](https://github.com/ROCm/ATOM/issues/2634)、[#2630](https://github.com/ROCm/ATOM/pull/2630)、[#2786](https://github.com/ROCm/ATOM/pull/2786)、[#2842](https://github.com/ROCm/ATOM/pull/2842)、[#2865](https://github.com/ROCm/ATOM/issues/2865)、[#2866](https://github.com/ROCm/ATOM/issues/2866)。最新 release 仍 [v0.1.8](https://github.com/ROCm/ATOM/releases/tag/v0.1.8)；issue 原因分析不是已合入修复。
187. **S187 — AIC nightly wheel、CI 与 benchmark 增量** — [#189](https://github.com/ROCm/rocm-aic/pull/189)、[#190](https://github.com/ROCm/rocm-aic/pull/190)、[#196](https://github.com/ROCm/rocm-aic/pull/196)、[#198](https://github.com/ROCm/rocm-aic/pull/198)、[#199](https://github.com/ROCm/rocm-aic/pull/199) 已合入；[#192](https://github.com/ROCm/rocm-aic/pull/192)、[#193](https://github.com/ROCm/rocm-aic/pull/193)、[#197](https://github.com/ROCm/rocm-aic/pull/197)、[#201](https://github.com/ROCm/rocm-aic/pull/201) Open。主要属于交付基础设施，不外推数据面成熟度。
188. **S188 — LMCache ROCm nightly 与生命周期在研** — [nightly-rocm](https://github.com/LMCache/LMCache/releases/tag/nightly-rocm) 11-01 仍为 ROCm 7.2、gfx942/gfx950；[#5075](https://github.com/LMCache/LMCache/pull/5075)、[#5133](https://github.com/LMCache/LMCache/pull/5133)、[#5615](https://github.com/LMCache/LMCache/pull/5615)、[#5841](https://github.com/LMCache/LMCache/pull/5841) 仍 Open 且近期无推进；[#6175](https://github.com/LMCache/LMCache/pull/6175) 为有作者的 stacked Draft，CUDA/RDMA 验证不能替代 ROCm/W7900。


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

> 核验日期：2026-11-02。以下是公开贡献机会研究，未替用户发出评论、创建 Issue 或提交 PR，也未在 AMD 硬件上复现问题。Issue / PR 日期默认使用 UTC；状态是检查时快照。**当前首选与动态状态见 19.17**；19.3–19.16 的带日期清单均保留历史，不能据旧 Open 状态认领任务。

### 19.1 结论：可以参与，你的优势适合哪些贡献

**可以。已确认的 ProcessGroupDLCCL、C++ Extension、集合通信与 custom allreduce 接入经验，为框架接口、设备同步与回归测试提供切入点；本期任务另列 CUDA IPC，但在具体范围梳理前，仍不能自动等同于独立实现通信 kernel、IPC transport 或 RDMA 完成语义。** 不必先成为 Rust 专家或拥有大规模 AMD 集群，才开始贡献；但设备通信、HIP 地址可达性和性能结论仍需要匹配的实机验证。

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

**09-14 权限复核（历史）：** Infera/AIC 贡献指南、MORI README 仍欢迎上述贡献流程；AIC `has_discussions=false`，个人 `JohnQinAMD/sglang-amd` 仍是 `sgl-project/sglang` 的 fork 且自身 Issues 未启用。SGLang 当前指南允许作者对自己的 PR 使用 `/rerun-failed-ci`，但加 CI 标签、完整/选择性运行仍有不同权限；这不等于能自行获取 AMD runner。新增 CPU CI 用例应遵守 `CustomTestCase`、`register_*_ci` 和脚本入口约定。MI355X P/D 夜测资源暂停需另行确认可运行性；本研究未测试用户账号权限。[S45][S61]

**09-21 权限复核：** Infera CONTRIBUTING 仍要求 DCO，外部 collaborator 需管理员批准，不代表 fork PR 必须先成为 collaborator；AIC 明确欢迎外部 fork，但 `has_discussions=false` 仍与指南的 feature-request 路径不一致。AIC accuracy 工作流使用 self-hosted runner/部署凭据，外部账号不能据此假定有免费机器。SGLang 本周 #40474 修改 CI 权限表，不能沿用旧授权名单判断当前用户权限；本研究没有测试该用户账号的发布权限。个人 JohnQinAMD/sglang-amd 仍是 upstream fork、Issues 未启用。MORI README 仍欢迎贡献并要求代码质量检查。[S29][S34][S40][S45]

### 19.3 09-21 机会清单（历史快照；09-28 更新见 19.12）

“未见同题 PR”只表示此次公开定向检查未发现，不保证没有未关联或内部工作。创建/更新日期均为 UTC；“评论”指 issue discussion，review 另述。

| 类型 / 优先级 | 入口；创建 → 更新 | 09-21 状态、归属与关联 | 最小交付 / 硬件门槛 |
|---|---|---|---|
| **P0，现有可讨论任务** | [Infera #36](https://github.com/AMD-AGI/Infera/issues/36)；07-29 → 08-03 | Open，无 assignee，0 评论；当前三处 GID picker 仍独立；定向 PR 检索未见承接去重 | 行为矩阵、共享读取层、sysfs fixture；CPU 可验策略兼容，真实 RoCE 另验。[S30] |
| **P1，已有作者补测** | [MORI #632](https://github.com/ROCm/mori/pull/632)；09-02 → 09-02 | Open，jhchouuu，无 assignee/评论；已提交锁补丁，main 查表仍未见该锁；正文承认缺并发测试 | 先确认 API 允许的并发，再补一个遗漏用例；主机模型不等于真实 HIP VMM/multi-rank。[S36] |
| **P1，已有作者评审** | [SGLang #38164](https://github.com/sgl-project/sglang/pull/38164)；09-06 → 09-08 | Open、非 Draft，ormandj，无 assignee，2 评论；已有 timeout + CPU Gloo 覆盖，与 #35645 去重 | 做覆盖矩阵与独立复测，不重写 timeout。CPU/Gloo 不证明真实 RDMA drain。[S63] |
| P1，相关上游学习/协作 | [LMCache #5157](https://github.com/LMCache/LMCache/pull/5157)；09-17 → 09-20 | Open，riversky0014，无 assignee、0 discussion；**09-17 hlin99 已 APPROVED**，尚未 merged | 对照实际 KV device 同步与 SHM/pickle 生命周期；作者 CPU + 2×4090 测试不是 AMD/自研芯片验证。不是无人认领，也不推断作者就是用户。[S78] |
| P1，有 AMD 卡再协作 | [vLLM #55347](https://github.com/vllm-project/vllm/pull/55347)；09-04 → 09-16 | Open，stefanskiasan，无 assignee；已有 0 值防护；09-16 bot 报 merge conflict | rebase 由作者推进；先评审编译 cutoff/runtime/fallback，ROCm 多卡再验证融合，不重写已有修复。[S47] |
| P2，已有草案 | [SGLang #38704](https://github.com/sgl-project/sglang/pull/38704)；09-09 → 09-15 | Open Draft，kflansburg，无 assignee、0 评论；admission abort/length consensus | 作者 38 测试/14 subtests 含两进程 Gloo；未验证完整 runtime、模型或 GPU/RDMA，不追加泛化“取消支持”。[S63] |
| P2，已有草案 | [SGLang #38961](https://github.com/sgl-project/sglang/pull/38961)；09-11 → 09-12 | Open Draft，kflansburg，assignee ShangmingCai，1 评论；与 #37077 重叠 | 看延迟回收与真实 source-safe；CPU fake 不能验证 RDMA quiescence。[S63] |
| P2，现有任务 | [Infera #46](https://github.com/AMD-AGI/Infera/issues/46)；07-30 → 08-03 | Open，无 assignee/评论 | intra-node KV 路径评估需 AMD 多卡/xGMI；当前不作无卡首选。[S31] |
| P2，既有问题复测 | [MORI #342](https://github.com/ROCm/mori/issues/342)；05-30 → 05-30 | Open，无 assignee/评论；#92 仍 Open（更新08-31），已有作者推进重复调用测试 | 原复现需4块本机ROCm GPU；复测当前代码后再判断缺陷是否仍在。[S37][S38] |
| P2，工具任务 | [AIC #118](https://github.com/ROCm/rocm-aic/issues/118)；08-06 → 08-06 | Open，无 assignee/评论；定向 Loki PR 搜索未见结果 | 日志采集/查询最小链路与CPU容器测试；不是底层通信成果。[S41] |
| P2，深度学习/评审 | [SGLang #36966](https://github.com/sgl-project/sglang/pull/36966)；08-29 → 08-31 | Open，Lzy17，无 assignee、0 评论，已有实现及前序依赖 | host/device pointer alias、注册与释放；补课而不是用户既有 IPC 经历；实机多卡/RDMA另验。[S48] |
| **历史，已合并** | [MORI #665](https://github.com/ROCm/mori/pull/665)；09-12 → **09-14** | 09-14 merged，jhchouuu，无 assignee；不再待认领 | 学习 allocator 污染 benchmark 的负对照；实测要求双节点。[S64] |
| **历史，已替代** | [AIC #147](https://github.com/ROCm/rocm-aic/pull/147)；08-31 → **09-16** | Closed、未 merged，john00003；09-16 维护者已说明 rebase/清理；后续 #166 于09-17 merged | 读新的 accuracy 源码/工作流；不继续补旧“未接 CI”问题。[S69] |
| **历史，已修正** | [AIC #160](https://github.com/ROCm/rocm-aic/pull/160)；09-14 → 09-15 | 09-15 merged；当前 README 明确 source build，后续 #168 更新版本/构建 | 撤下旧 README wheel/source 不一致提案；新问题先在新文件布局复现。[S70][S88] |
| 历史，issue 状态滞后 | [MORI #626 / #653](https://github.com/ROCm/mori/pull/653)；#626 09-01 → 09-09 | #626仍Open、QizhouZhang97已指派；#653于09-11merged修复 | 保留回绕/完成语义学习；不重复认领。[S53] |

相关新增学习入口：LMCache #5133（09-16 创建/更新、Open，已有作者补丁，非可认领白纸）与 ATOM #2223/#2284/#2315。详见 3.8、5.8；真实硬件与收益边界必须随源码案例一起记录。[S71]–[S73][S80]

### 19.4 历史低硬件候选：Infera #36（当前排序见 19.15）

它是一个边界清楚的维护任务。Issue 明确说这是代码重复和维护债，**没有宣称已发生运行故障**。当前 `netperf.py`、`fabric.py`、`mooncake_mode.py` 各有 GID 选择相关实现，接口返回值也不同。你可以从已有接口适配经验切入，补充网络探测知识后形成完整的工程改进。[S30]

**09-21 读取、09-28 再核源码：** 重复确实仍在，但不能照 Issue 的一句“相同策略”机械合并。`netperf._gid_index` / `fabric._roce_v2_gid` 在遍历遇到 global IPv6 时直接返回，并保留 link-local 作为末级 fallback；`mooncake_mode._routable_gid` 优先 IPv4-mapped、跳过 link-local，且枚举全部数字 GID 槽，而前两者扫描前 16 个。返回缺省值也不同。建议先将“共同读取机制”和“调用者策略”分层：首个 PR 保持各调用者原行为，策略统一另提讨论。这是当前代码差异，不是本研究已证明的运行故障。[S30]

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

09-21 复核：#632 仍 Open，创建/更新均 09-02，无 assignee、无讨论评论，但作者 jhchouuu 已提供补丁；当前 main 的 register 查表路径尚未包含该补丁的 lock。补测应同时分析“解锁后保存元素引用”的生命周期前提：rehash 不使引用失效，不等于允许对象被另一线程 erase/free。后者是需要确认 API 契约的评审问题，不在没有复现的情况下直接宣称新 UAF。

这可以从你的 ProcessGroup 接口与执行流适配经验向外延伸，但 Work 设计、IPC buffer、barrier 和 UAF 修复不能自动记为你已做过。使用 sanitizer 有价值，但宿主端 sanitizer 的通过不能证明 GPU 侧同步或远端写入正确。

**长期主线：MORI #572 的 async/shared-expert overlap。** 可以先贡献接口和完成语义分析，再讨论小范围实现；这是跨 MORI、vLLM、AITER 的工作，不能通过简单修改能力布尔值就宣称支持 overlap。与现有 #342、#92 的异步正确性问题一起看，更容易形成完整设计判断。[S39]

### 19.6 SGLang/vLLM：用已有经验进入 upstream

**没有 AMD 卡时，SGLang P/D 失败路径可从评审开始，但不能再当作空白任务。** #33114 仍 Open，作者的 CPU 节流测试不能视作当前 main 全部状态；main 已有 `_prefill_dp_rank_queries`、取消/预取等演进。更重要的是 #38164 已实现分配前超时与 rank consensus，#38704 已推进 admission abort 与长度共识，#38961 已推进 deferred KV release，不能重复提一份泛化 timeout/abort 修复。[S46][S63]

建议先写状态/覆盖表：连接失败、worker 未就绪、rank 未注册、请求已取消、整体超时、部分 rank 已终止，逐项对应 main 和现有 PR。#38164 已有两进程 CPU Gloo 超时共识测试；作者在 09-08 评论说明将重叠 admission 工作交回 #35645。#38961 的维护者 09-12 明确指出与 #37077 重叠，并区分“延迟回收”与“潜在内存破坏”，跨 backend/scheduler 行为需协调。先贡献独立评审、复测或维护者接受的遗漏用例，不重做已有测试套件；两进程 Gloo 也不证明 RDMA 已 quiesce。[S63]

本次元数据快照：#38164 创建 09-06、更新 09-08，Open 非 Draft，作者 ormandj、无 assignee、2 条讨论评论；#38704 创建 09-09、更新 09-15，Open Draft，作者 kflansburg、无 assignee、0 条讨论评论；#38961 创建 09-11、更新 09-12，Open Draft，作者 kflansburg、已指派 ShangmingCai、1 条详细维护者评论。后两者的 AST/fake/Gloo 验证各有依赖和范围限制，不能表述成完整 runtime/GPU/RDMA 回归通过。

**有 AMD 多卡时，vLLM AITER allreduce 可用于深化既有接口集成能力。** #55347 涉及运行时 cutoff、IPC pool 和编译范围之间的一致性。先检查 PR 已覆盖的边界，再讨论新增用例；PR 后续提交已处理 0 值导致无效编译范围的问题，不能再列成无人修复漏洞。[S47]

另一个入口是 #53136 的新版复测。最新维护者回复认为已合并 #46065 的 AITER 路径应覆盖原问题，要求换新版验证。因此可贡献的是固定 commit/image、确认实际 communicator、将请求缩成 message-size sweep 后报告结果，不能把原“8–16 MiB 缺口”直接写成当前缺陷。[S49]

**09-28 更新：** #40645/#41023/#41402 已合入 drain ACK 保留、默认开关与多目标 fan-out/先 arm 后发送；#38961 的部分审计点不再空缺。当前 MoRI 后端未 opt-in；不能将 Mooncake/NIXL 的保护外推 MoRI。#38164 本身仍 Open。详见 3.9 与 19.12。[S98]

### 19.7 AIC：低硬件门槛存在，但应选择与目标相关的工作

AIC #151 是有参考价值的合入案例：用最小 Docker 构建场景验证 named build context 的默认行为，作者明确没有做完整 AMD 镜像验证。#139 则修正 benchmark 请求失败却返回成功的问题，使用局部 HTTP/单元测试。这说明**诚实限定验证范围的小修复也有价值**，而不是必须先跑起整个分层 KV 栈。[S43]

如果选择 #118，建议把目标限定为：给现有监控增加一条可运行的日志采集与查询路径，配套容器样例、配置校验和说明。这里的最小验收是能从模拟服务的一条错误日志追到查询结果；不要在首个 PR 同时重做完整观测平台。[S41]

以下条目已有人推进，应先讨论分工：#115 CI 脚本更新行为已指派 sbates130272 与 john00003；#114 NIXL benchmark/report、#110 八卡测试已指派 john00003。#115 涉及自托管 runner 对不可信 PR 代码的信任边界，不能以直接取消门禁来“修复”流程。[S42]

**纠正 #150 的旧状态：** #150 于 09-09 非合并关闭，关闭评论明确指向替代 #154；后者同日合并，emulation 已进入 main。现在可研究真实代码与 CPU smoke，而非继续评审旧分支是否应合入。其 profile 仍不是真实 GPU 测量。#147 已于 09-16 非合并关闭；09-08 的“未接入 accuracy CI”只保留为历史，后续 #166 于 09-17 合并了新准确率测试与工作流。差分模型分数、tier 计数与重启测试比普通 smoke 更强，但依旧不是任意 KV 字节一致性证明。[S44][S58][S69]

**09-21 撤回旧新提案：** #160/#168 后 README 明确列 PyTorch/AITER source build，旧的 wheel/source 文档修复不再是空白机会。若想补构建或 kvbench 测试，应先核对新的 base/vLLM/LMCache Dockerfile 与现有 CPU smoke。#168 PR 正文曾说旧 Dockerfile 删除，但当前源码仍存在，说明不能只读 PR 摘要。本期不虚构新的待认领构建 bug。[S70][S88]

**可先本地学习的低硬件范围：** accuracy 配置/统计门槛、失败指标抓取、emulation/监控 CPU smoke。真实 tier hit、重启复用、GPU DMA 与吞吐依然需要完整栈。AIC 仍是 early-access technology preview；不推荐生产负载的声明没有因新增测试而撤销。


### 19.8 历史与重叠工作：这些不应重复认领

**本期新增历史条目：** MORI #665（09-14）、#652（09-20）已合并；AIC #147（09-16 关闭未合并）由 #166（09-17 合并）后续方案取代；#160（09-15）已覆盖旧版本说明修正。MORI #679 被 #687 回滚；ATOM #2154 被 #2315 回滚，不能继续按已启用能力复习。以下旧记录保留，其动态状态以 19.3 和本段为准。

| 条目 | 交叉核验结果 | 应采取的态度 |
|---|---|---|
| Infera #88，Rust NATS transport | Issue 仍 Open，但 #113 已于 2026-08-12 合并，加入相关 NATS/Kubernetes 路径。[S32] | 学代码或协助核对过期说明；不要从零重做 |
| MORI #626 / #653 | #626 仍 Open、已指派；#653 于 09-11 合并，main 有修复与测试。[S53] | 已解决的历史案例，不再列当前待认领 |
| AIC #150 / #154 | #150 于 09-09 Closed 且 `merged=false`；#154 同日合并承接 emulation。[S58] | 不把 Closed 当 merged，也不把已合入功能仍称 roadmap |
| SGLang #33114 与 lifecycle 新 PR | #38164/#38704/#38961 等已有作者；维护者指出 #37077 等重叠。[S63] | 旧“新提案”降为协作评审，保留历史纠正 |
| vLLM #56610 / #48247 / #53695 | 分别于 09-12 / 09-11 / 09-10 合并。[S61] | 弹性 EP 顺序、DP AG/RS、KV layout 的学习案例，非待修 bug |
| Infera KV block/renderer 边界 | #73 已于 08-02、#143 已于 09-04 合并相关修复和测试。[S33] | 用你对 block size/prefix cache 的理解寻找真正遗漏；不能重复已有 parity 用例 |
| MORI #507，接收索引 | 有维护者欢迎静态分析作者提 PR，但 #621 已于 08-31 提交同题修复，09-28 为 Open、非 Draft，已指派作者 isytwu，最后更新 09-23；并非无主任务。[S38][S107] | 适合独立复核、回归测试和硬件复测，不能重复提交同一行修复 |
| MORI #557，SymmetricMemory/CCO | #544 于 08-26、#628 于 09-02 已合并关键阶段。[S39] | 读当前代码及 remaining gaps，不照旧 RFC 认领整个项目 |
| MORI #92，Moreh 团队 EP 测试 | 有明确外部公司参与证据，但仍 Open。[S38] | 是协作实例，不是“已经合入”的成功案例 |
| SGLang #27194，MORI buffer/准确率 | 后续评论修正了早期根因判断，指向 AITER #4420/#4587 的修复。[S50] | 作为跨层定位案例，不列为当前无主 bug |
| AIC #139/#151 | 2026-09-06 已合并。[S43] | 学习贡献方式；本轮不再推荐相同修复 |

**维护原则：** Issue 状态、Development 栏、PR 标题、评论、合并时间和当前源码必须相互核对。Closed PR 也不等于 merged，需检查实际 merged 字段。别人声明的复现、性能或根因应注明来自报告者，本研究没有跑过的测试不能写成自己验证。

### 19.9 两周执行计划与贡献材料

**本期主线更新：** 用户已决定重新适配自研芯片 LMCache，优先用工作中可访问且获准使用的环境完成 5.8 最小闭环。以下 Infera 两周路线保留为低硬件备用，不要求同时推进，也不表示已联系维护者或已经获准对外发布。

09-28 已知你有按供应窗口使用 W7900 的云额度；这仍不包含多卡/RDMA保证。建议只选一个主任务和一个后备，避免同时推进多个仓库。

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
I'm interested in contributing to this issue. My experience includes
adapting a PyTorch ProcessGroup backend for a custom accelerator and
integrating existing communication operators into vLLM.

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

你的定位以 **推理框架与通信后端集成，向 KV 数据面延伸** 为主。Infera #36 提供低硬件门槛入口；MORI #632 和 vLLM AITER AR 可讨论协作验证，#626/#653 现为已合并学习案例；SGLang P/D 状态机先做既有工作的交叉评审，不能泛化为无人负责。没有新增你已经完成贡献的事实，且旧版匹配度百分比已撤回，也不保证开源贡献带来面试、合并或录用。

后续每次例行更新应维护本节：新任务、负责人变化、关联 PR、合并/关闭、当前源码是否仍存在问题、硬件门槛、首选三项。已解决条目移入历史并保留链接；没有新增机会也更新核验日期。新增能力和过期 Issue 的纠正必须同步回正文成熟度判断，不能只在贡献清单里改状态。

### 19.11 上期首选三项与可交付范围（09-21，历史）

下面是准备优先级，不是发布授权，也不是三个必须同时做的项目。

| 排序 | 入口与类型 | 最小交付 | 边界 |
|---|---|---|---|
| 1 | **自研芯片 LMCache 适配：本地项目；参考相关上游** | 固定版本、DeviceSpec/DeviceOps 或外部插件、engine-driven CPU tier、字节级 roundtrip、真实复用命中与冷/热/无复用 A/B | LMCache 是相关上游，不是 AMD 官方仓库；#5157/#5133 已有作者，不重复提修复。用户项目尚未开始产出结果。[S77]–[S80] |
| 2 | **Infera #36：现有可讨论维护任务** | 三个 GID picker 行为矩阵；共同读取机制与调用者策略分离；临时 sysfs + mock 命令测试，保留单文件 fallback | 当前仍存在重复，但不宣称生产 bug；没有实网则不声称 RoCE 验证。适合作为无设备条件下的首个公开贡献候选。[S30] |
| 3 | **SGLang #38164 及相邻生命周期 PR：既有作者协作** | main/PR 覆盖表；独立复跑现有 CPU Gloo，再提一个确有遗漏的场景；理解 source-safe/超时/取消的差别 | 不重做 #35645/#38704/#38961 的已有方案；完整 GPU/RDMA 与性能待验证。[S63] |

**若获得 AMD 多卡资源，可用 MORI #632 替换第 3 项：** 先明确同一 communicator 的合法并发 API 与 collective 顺序，后做主机/实机分层回归。#665/#652 作为已合并学习材料；vLLM #55347 先等作者解决当前冲突，再考虑协作，不据 Open 认定无人负责。

**为何改变上期排序：** 新近用户澄清显示最强证据是接口集成，而非 IPC/kernel；LMCache 工作机会能把相关能力变成实测成果，通常比同时学习三个全新仓库更容易完成闭环。是否最终公开依赖公司授权和维护者认可。

**身份与硬件：** 不由 GitHub 用户名、AI 工具声明或审批推断作者雇佣身份，也不将 riversky0014 等账号认作用户。没有确认免费 AMD/RDMA 机器、合并承诺、面试或录用结果。

**下一期复核：** #5157 是否真正合并及其 device-sync 变化；LMCache 设备目录/API 与用户选择版本；ATOM 回滚后 fencing/readiness 是否重新引入；Infera #36 是否承接；MORI #632/ SGLang #38164 是否合入及新增测试；AIC accuracy 真实运行证据与 preview 标记；89395 是否恢复/明确关闭、89498 地点，以及新岗位资格。

---



### 19.12 09-28 当前机会、贡献门槛与首选三项

#### 状态、关联与重复任务核验

日期为 UTC；无 assignee 记为“—”，PR 作者另列。本节为当前快照，覆盖 19.3 的动态状态。

| 入口 / 类型 | 创建 → 最后更新 | 状态 / 作者 / assignee / 讨论 | 当前可交付与限制 |
|---|---|---|---|
| **Infera #36，现有可讨论维护任务** | 07-29 → 08-03 | Open；dorado269；—；0 评论 | 09-28 仍见三个 GID 实现，定向 GID PR 搜索未发现去重承接。共享 sysfs 读取与策略保持测试可 CPU 验；真实 NIC/RoCE 另验。不是已证明运行 bug。[S30][S107] |
| **LMCache #5075，已有作者补测** | 09-11 → 09-25 | Open 非 Draft；jbelloncastro；—；无讨论/review | 当前补丁只有 utils.py；NVTX 优先，然后 ROCTX，再空装饰器。dev 仍为 NVTX-only；读取 head `b8085450...` 的 check-runs，ROCm build 为 skipped，普通 CPU CI 成功不能证明真实 marker。适合本地选择矩阵 + 单 W7900 trace。[S106] |
| MORI #632，已有作者评审/补测 | 09-02 → 09-02 | Open；jhchouuu；—；0 评论 | 当前 main WindowRegister 查表仍无本 PR 的 lock；正文承认缺同 comm 并发 register/deregister 复现。CPU 模型可讨论契约；真实 HIP VMM/跨 rank 仍需相应多卡，不能单 W7900 冒充。[S36][S107] |
| SGLang #38164，已有作者评审 | 09-06 → 09-08 | Open；ormandj；—；2 评论 | 去掉与 #35645 重叠的 admission 内容；可复核 CPU Gloo/状态机，但需按最新 main 重新比对；真实 RDMA 不在 CPU 测试内。[S63][S107] |
| SGLang #38961 / #37077，重叠中的方案 | 09-11 → 09-12 / 08-30 → 09-23 | 前者 Draft、kflansburg、ShangmingCai、1 评论；后者非 Draft、livingshade、ShangmingCai、0 评论 | #40645/#41402 已合入其中 ACK 保留、扇出与 arm 顺序相关子问题。先拆分“已合入 / 仍在方案 / 需共同契约”，不能把整套 deferred release 当新任务。[S98][S107] |
| SGLang #38704 / #36966 | 09-09 → 09-15 / 08-29 → 08-31 | 均 Open；分别 kflansburg(Draft)/Lzy17；无 assignee；0 评论 | admission abort、host/device alias 各有作者。可读 CPU 边界；后者实际 DMA/设备地址验证不可用 fake 代替。[S107] |
| vLLM #55347，已有作者修复 | 09-04 → 09-16 | Open；stefanskiasan；—；4 评论 | AITER cutoff/fusion 修复仍未合并，保留旧冲突记录；ROCm 多卡复测才能覆盖融合通信，不重做已有补丁。[S47][S107] |
| vLLM #57126，已有作者补测备选 | 09-16 → 09-17 | Open；zihaomu；shen-shanshan；0 评论 | 修 #56992，已提供 W7900D/gfx1100 性能报告和 6 个单测。明确有作者、有 assignee；不称修复已合并。现有报告没有 KV scale checkpoint 准确率证据；你的 W7900 复核放第二阶段。[S108] |
| LMCache #5157 / #5133 | 09-17 → 09-20 / 09-16 → 09-16 | 均 Open；riversky0014/plotarmordev；—；0 discussion；#5157 有 09-17 APPROVED | actual-device sync、padded layout 已有补丁；批准≠合并。保留为适配参考，不认领同题实现，不认定账号为用户。[S78][S80][S106] |
| AIC #118，现有可讨论工具任务 | 08-06 → 08-06 | Open；sbates130272；—；0 评论 | 定向 Loki PR 搜索 0；仅表示本次未找到承接，不保证内部没人做。模拟日志/容器可 CPU 验；全栈 tier 与生产观测另验。[S41][S107] |
| AIC #177/#178，已有作者推进 | 09-23 → 09-24 / 09-23 → 09-25 | 均 Open 非 Draft；Copilot/sbates130272；前者 assignee sbates130272+Copilot，后者 sbates130272 | #177 是 CPU emulate 结果发布；#178 是 VM/compose 栈，需 KVM、镜像/资源，仍有 upstream blocker 与未勾选测试。可评审报告边界，不当作已实现硬件验证。[S100] |
| MORI #621 / #92，既有作者任务 | 08-31 → 09-23 / 2025-10-23 → 2026-08-31 | 均 Open 非 Draft；isytwu/dongmin-ra；前者已指派 isytwu，后者—；评论0/3 | #621 不再是 Draft；#507 接收索引问题已有它推进。#92 外部团队例子仍未合并；不以身份/名称推断用户雇佣关系。[S107] |
| MORI #711，新在研修复 | 09-24 → 09-27 | Open 非 Draft；yoqiu-amd；—；0 评论/review | 已有实现与 gfx942/gfx950 作者报告；只推荐学习及后续硬件协作，不给你安排单卡复现多队列跨 GPU 死锁。[S93] |

**新增已解决学习案例：** Infera #176、MORI #656/#709、ATOM #2167/#2339/#2351、SGLang #40645/#41023/#41402、vLLM #58098/#58566 均已合并。应学习修复/验证方法或找明确遗漏；不重交同题修复。老的 MORI #626/#653、AIC #147→#166、#150→#154 等继续保留在历史。

#### 贡献规则与当前硬件边界

- **正式入口：** Infera 为 AMD-AGI/Infera；MORI/AIC/ATOM 为 ROCm 对应仓库；SGLang/vLLM 在各自 upstream。09-28 API 再确认 JohnQinAMD/sglang-amd 是 sgl-project/sglang 的个人 fork，自身 Issues 关闭。
- **Infera / MORI / AIC：** 当前贡献指南仍要求测试/格式；Infera 每 commit DCO；成为外部 collaborator 需管理员批准与 fork PR 不同。AIC 欢迎外部 fork、CI+code owner 审核；`has_discussions=false` 仍与指南的 feature-request 入口不一致。没有测试用户账号是否能创建 Issue，也没有承诺 CI/GPU 免费使用。
- **SGLang：** 当前指南强调保护具体行为/不变量的测试；作者可重跑自己的失败 CI，不自动拥有加 run-ci 标签或选择性 runner 权限；选择性 rerun 不构建 PR-local kernel wheel，涉及 AOT 改动须正常/full CI。评审补测须证明新覆盖，避免只镜像实现的测试。[S109]
- **vLLM：** 当前指南明确 DCO 与 AI 辅助披露/人工验证；无写权限外部贡献者当前上限为 6 个 Open PR。获批准或 ready 后作者可用 CI 命令；更早阶段需要 write/trusted 权限。run 默认要求与目标分支零落后；CI aggregate green 也要检查是否含 blocked 项。这里记录文档规则，未实测账号权限，也未调用任何 CI。[S109]
- **W7900：** 用户提供的 150 小时额度不是每日有卡保证；本计划只按一张卡安排基础 HIP、D2H/H2D、stream/event、可用时 ROCTX trace。不能满足 MORI-EP128、双节点 RDMA、RCCL TP4/TP8、MI355X/Instinct 专属 kernel 验收。CPU emulation 与实际设备结果分栏。

#### 首选三项与最小交付（准备顺序，不要求同时做）

| 排序 | 当前入口与类型 | 具体交付 | 证据与限制 |
|---|---|---|---|
| 1 | **hip-kv-transfer-lab：你的学习项目** | 按七天 A/B 路线完成版本清单、KV roundtrip、双缓冲生命周期、同步/异步 A/B、时间线及负收益说明；读 ATOM #2339 与 vLLM #58566 作对照 | 不是上游待认领 Issue；未取得代码/实测前只记计划。本地 CPU、离线编译、W7900 实测分开。随后延伸自研芯片 LMCache 5.8 |
| 2 | **LMCache #5075：已有作者的补测/评审机会** | 本地四组合（无库/仅NVTX/仅ROCTX/两者）及返回值、异常、嵌套调用；W7900 将 marker 与 kernel/copy 联合 trace 对齐；形成报告草稿 | 两库并存按现设计优先 NVTX，不自行改优先级；独立 decorator 验证不等于完整 LMCache 服务验收；有新缺陷再准备小 patch，不保证维护者接受 |
| 3 | **Infera #36：现有可讨论维护任务** | 三处行为矩阵、共享 sysfs 读取层、原策略保留、fixture/mocked command 回归、单文件 fallback 说明 | 本地 CPU 可完成主体；真实 RoCE/NIC 行为未验证。先确认最新承接情况，再经用户授权对外讨论/提交 |

**后备顺序：** SGLang #38164/生命周期覆盖表（CPU）；ATOMesh #2351 已合并 Rust/HTTP 学习案例；第二阶段 W7900 可复核 vLLM #57126；获得合适多卡之后再考虑 MORI #632/#711 或 vLLM #55347。AIC #118 仍可讨论，但与你的通信/KV 适配主线相关性较弱，不为凑 PR 分散精力。

**面试新增两题：** ① Infera worker `/health` 成功为什么不足以 retire 旧 pod？答题落到 KV probe、注册和 readiness。② 为什么 send 已完成，KV block 仍不能释放？用 ATOM #2167 解释各 connector 独立 retention，再用 #2339 解释 producer→pack 依赖。自己的 HIP 实验可给单卡证据，不能冒充这些项目的作者或生产部署者。

**下一期：** 恢复岗位正文/发布日期/申请核验；#5075 是否合并及真实 ROCTX 证据；#5157 是否合并；Infera #36/#174/#175/#177；MORI #632/#711/#707；AIC #177/#178；SGLang #38961/#37077 与新合入的剩余差异。持续维护，不以一次检查完成而停用；未经用户授权不发 issue/评论/PR。

---

### 19.13 10-05 当前机会、权限变化与首选三项

#### 本期状态纠正

- **Infera：** 官方 Issues 页面现在明确显示 `Issue creation is restricted in this repository`。公开贡献并不因此完全关闭，但“直接新建 issue”不能再作为默认动作；应优先在已有 issue/PR 上准备证据，或先通过维护者认可的渠道确认范围。#36 在本期官方列表的可见截面中没有足够元数据刷新，不能据页面截断判定关闭；开始前必须再次打开具体条目确认。[S120]
- **MORI：** #711 仍 Open 且已有作者/评审请求；#717/#718 由同一作者推进，均是完整实现加作者测量，不是待认领白纸。适合代码审查、实验方法学习或在获得等价硬件后独立复核，不应重复实现同题。[S114]–[S116]
- **AIC：** #177/#178 仍 Open；#178 的 54GB 镜像和被移除的普通 PR trigger 说明“能在本地/QEMU 运行”不等于“外部 PR 自动获得完整 CI”。#181/#182 继续由现有作者推进，不列新提案。[S119]
- **LMCache：** 本期当前 PR 列表显示 MP、L2、生命周期、trace context 与 tier-pressure benchmark 大量新工作；但未能从官方页面重新取得 #5075/#5157/#5133 的确定最终状态。因此它们不再作为无需复核即可执行的首选，开始补测前先确认是否已合并/关闭及 main 是否已有等价实现。[S120]
- **ATOM / LMCache / Mooncake：** #2459 与 #2464 分别代表“LMCache L1/MP + Store L2”和“ATOM 直连 Store”两条在研路径。已有作者、有具体模型与硬件数据；本期最合适的外部工作是形成架构/生命周期/测试覆盖对照，或在作者明确需要时补测，不是另起重复 connector。[S117][S118]

#### 10-05 首选三项与最小交付

| 排序 | 当前入口与类型 | 最小交付 | 可验证范围与限制 |
|---|---|---|---|
| 1 | **hip-kv-transfer-lab + 自研芯片 LMCache 小闭环** | 完成连续/分段 KV roundtrip、双缓冲 ownership、producer→copy→consumer 事件链、pageable/pinned、同步/异步/gather 对照；产出 CSV、时间线和失败用例 | 本地 CPU/离线编译、W7900 实机、自研芯片结果三栏分开；不把单卡数据写成 MI355X 多卡/RDMA 结论。可直接支撑 92727/89393 面试 |
| 2 | **ATOM #2459/#2464 + MORI #717：评审式学习** | 做一张统一对照表：内存 owner、进程/节点边界、pack/unpack、transport、发布/完成、失败回收、NUMA、测量口径；选择一个可在 W7900 缩小复现的 copy/gather 命题 | PR 均已有作者且未合并；不提交重复实现。W7900 能验证 HIP 搬运方法，不能验证 Mooncake RDMA、8×MI355X、双路 NUMA 或端到端 GLM-5.2 数据 |
| 3 | **Infera #36 或现有 PR 的 CPU 回归：需先确认权限和状态** | 若 #36 仍开放且维护者认可范围，完成 GID probe 行为矩阵与 mock/sysfs 测试；否则从 #179 的 projection 单测或现有 lifecycle PR 中选一个明确遗漏的 CPU 回归 | 新 Issue 创建受限；不要先写大 patch 再找入口。CPU 测试不能替代真实 RoCE、Kubernetes fleet 或 GPU E2E |

**后备：** LMCache #5075 只有在重新确认仍需真实 ROCTX 补测时，才恢复为 W7900 快速贡献；vLLM gfx1100 问题可作为第二周独立复核，但先检查上游当前状态和已有作者。MORI #711、#632 与 RCCL 多卡任务继续留在获得合适多卡/互联后。

#### 对求职准备的直接影响

1. **92727 的证据包：** 一个 HIP/CUDA kernel 或搬运 microbenchmark，包含正确性、边界尺寸、rocprof 时间线、带宽/occupancy 分析和负结果。
2. **89393/89398/89499 的证据包：** 一条从 Python/框架到 C++/device op 的调用路径，加上 stream/event、tensor storage 生命周期和多 rank 失败处理。
3. **89764 的长期能力包：** 读懂 Triton compiler/runtime 与 collective/RMA/synchronization 的接口边界；当前 ProcessGroupDLCCL 经验可证明集成能力，但不能包装成 Triton 原生通信实现。
4. **公开身份边界：** 继续准确标注“本地分析 / 独立复现 / 草稿 / 已提交 / 评审中 / 已合并”；未经用户明确授权不发布 issue、评论或 PR。

**下一期优先复核：** 92727/89764 的官方 datePosted 与持续可申请状态；89500/89498/89497/78999/92050/92051 的正文恢复；LMCache #5075/#5157/#5133 的最终状态；Infera #36 和 issue 权限；#179、MORI #711/#717/#718、ATOM #2459/#2464、AIC #177/#178 的合并/关闭及 main/release 落点。

---

### 19.14 10-12 当前机会、已解决案例与首选三项

#### 本期状态纠正

- **LMCache #5157：已合并，不再是贡献机会。** 10-08 合入 actual-device synchronization；后续工作是基于合入版本验证新设备后端，而不是重复提交同题修复。[S127]
- **LMCache #5075：仍可做有边界的 W7900 补测。** PR 仍 Open、无 reviewer，已有作者实现；可补真实 `rocprofv3 --marker-trace`、异常/嵌套 decorator 和两库选择行为。19/29 checks 不等于剩余 10 项全部失败，也不能保证维护者仍需要补测，开始前先留言范围仍需用户授权。[S132]
- **MORI #716/#729：已合并学习案例。** 前者建立 peer failure signal，后者修复 VMM DMA-BUF backing allocation 泄漏。它们很适合完善面试中的 failure/lifetime 故事，但不应再列待认领任务。[S124][S125]
- **MORI #731：已有作者的评审/测试机会。** fault injector 目前只让 hang 可确定复现，正文明确还没有修 H1–H5；CPU 可审 spec/parser/unit test，真实 verbs/NIC 与 chaos soak 需要 RDMA 环境。[S129]
- **AIC #183：已有作者/assignee的 emulation E2E。** 可讨论复现文档、失败诊断和 metric assertion；`/dev/kvm`、Docker socket、guest image 是现实门槛。不能把 QEMU ionic 测试写成 AMD GPU 或真实 RDMA 验证。[S130]
- **AIC #177：已合并；#178 仍由原作者推进。** #177 的 CPU emulator trend 可作 CI/报告设计参考，不再列待认领；#178 的 gfx1250 VM gate 仍受上游限制，也不是免费物理 GPU 验证入口。[S133]
- **ATOM #2518：已合并学习案例。** 它说明 Open/无 assignee 不是判断“无人负责”的充分条件，也说明未消费 lookup 仍会留下 read-lock/lease；外部新工作应找不同缺口。[S126]
- **Infera #183：已合并。** 指标联邦适合用来设计 CPU mock regression，但本期没有发现新的明确、低冲突 good-first issue；Infera 的 issue 创建限制仍应视为入口门槛。[S123]
- **vLLM #61109/#61119 与 SGLang #43719/#43723：已有作者的上游学习/评审案例。** #61109 最贴近用户的 custom allreduce 经历，可对照 island communicator、graph capture 与 correctness；#43719 最适合补强 ACK/timeout/buffer reuse 状态机。#61119/#43723 还显示“性能收益依赖组合优化”和“作者硬件验证不等于回归覆盖”。本期不把任何一项列成可直接认领的新题。[S134][S135]

#### 10-12 首选三项与最小交付

| 排序 | 当前入口与类型 | 最小交付 | 可验证范围与限制 |
|---|---|---|---|
| 1 | **hip-kv-transfer-lab：独立学习项目** | 完成 KV roundtrip、双缓冲、producer/copy/consumer event 链、pageable/pinned、同步/异步/批量对照；加入三类提前复用失败测试与 rocprof 时间线 | 本地 CPU/离线编译与 W7900 实测分栏。它能证明 HIP stream/event 与 buffer 生命周期能力，不能证明多卡 RCCL、RDMA 或 LMCache E2E |
| 2 | **自研芯片 LMCache 小闭环：工作内项目** | 固定含 #5157 的版本；验证 actual device、current stream、布局/stride、store/load/lookup/discard、有限 buffer 池与命中收益；输出正确性、失败注入和 A/B 数据 | 公司代码、SDK、日志和模型数据须遵守授权与脱敏；自研芯片结果不标作 ROCm。#5133 仅作未合并参考 |
| 3 | **LMCache #5075 或 MORI #731：二选一的评审式贡献** | 有稳定 W7900 时优先 #5075 的真实 ROCTX trace；若无 GPU/PR 已变化，则对 #731 做 fault contract、timeout invariant 与 unit-test coverage review，先形成私有报告 | 两项均已有作者，未经用户明确授权不发布评论/PR。#5075 独立 marker 测试不等于完整服务；#731 CPU review 不等于真实 NIC 故障恢复 |

#### 可交付证据与岗位映射

| 证据 | 可回答的面试追问 | 对应岗位 |
|---|---|---|
| event 链与提前复用失败测试 | enqueue、complete、publish、reuse 的区别；为何 `.cpu()` 会掩盖缺失同步 | 87545、89393、89398、89499 |
| #5157/#5565 的复现或源码说明 | actual device 如何选；已处理错误为何污染下一次 kernel | ROCm/HIP、PyTorch extension、LMCache connector |
| #716/#731 故障状态机 | peer slow/dead、CQE 丢失、timeout、session eviction 与 retry 如何分层 | MORI-IO、P/D、通信后端 |
| #2518 锁/lease 验证 | 请求取消或 lookup 未消费时资源如何释放；TTL 为什么只能兜底 | 全局 KV、缓存控制面 |
| kernel/copy 时间线与负收益分析 | 有 overlap 为什么整体仍不快；资源争用和提交粒度如何拆解 | 92727 与性能岗 |

**下一期优先复核：** 92727/89764 及中国主线 Req 的持续申请状态与 `datePosted`；89500/89498/91145 的官方正文；Infera #179、MORI #711/#717/#718/#731、AIC #178/#183、ATOM #2459/#2464、LMCache #5075/#5133、vLLM #61109/#61119、SGLang #43719/#43723 的合并/关闭与主分落点；LMCache 含 #5157 的首个可确认 release。继续只研究和准备，未经用户明确授权不发布 issue、评论或 PR。

---

### 19.15 10-19 当前贡献清单、门槛与首选三项

#### 已解决、非合并关闭与分支落点：先从候选中撤下

| 条目 | 本期核验事实 | 当前定位 |
|---|---|---|
| MORI #711 / #731 | 分别 10-13 / 10-12 合入 main；#711 末次维护者评论说明剩余相关事项团队继续推进 | 已合并学习案例；#731 的故障 seam 不等于全部 hang 修复，不重复提交 |
| MORI #718 | 10-13 入 main，NUMA prefault 已实现 | 不再列待评审优化；可复核适用边界，不照作者八卡数字认领收益 |
| **MORI #507 / #621** | issue #507 仍 Open，但 #621 **09-30 已合并**，作者/assignee isytwu | 纠正 19.8/19.12 的旧“仍在研”；是本期新核验旧合入，不是本周新发布 |
| ATOM #2459 | 10-12 关闭、merged=null，作者 Jasen2201、assignee ZhangLirong-amd | 非合并关闭历史实验；没有充分关闭原因，不擅自声称完整转入 #2464 |
| ATOM #2464 | 10-13 入 main，作者 Jasen2201、assignee JiaoliangYu；6 条讨论、50 条 inline review comments | 已合并 dense Store 案例；读最新失败/taint/预算处理，旧评审问题已有多轮修正 |
| SGLang #43719 / #43723 | 10-12 / 10-13 入 main；后者 assignee YAMY1234 | 已解决学习案例，撤下“Open 待补修”；NIXL 作者测试平台不是 AMD |
| Infera #185 / #186 / #192 | 已合入 main；分别覆盖 P 负载、会话与 preflight | CPU/Rust 测试方法可学，新增贡献须找具体遗漏，不重交现成功能 |
| Infera #203 | 10-17 merged，但目标为开发分支，不在当前 main 祖先链上 | feature-branch 已整合，不当作 main/release 或待从零实现 |
| LMCache #5157 | 10-08 合并且 v0.5.6 包含；#5075/#5133 则仍 Open | actual-device sync 不再认领；新设备后端自己验证 |
| vLLM #60544 / #62241 | 10-17 / 10-19 main 已合并 | hybrid WRITE 与退出清理学习案例，不以“未勾全测试”重新认领实现 |

本节日期为 UTC，读过元数据与重点讨论/源码。[S137]–[S145][S152]。“merge”只证明代码落点，不证明所有硬件/模型均通过。

#### 仍可讨论的具体工作（创建/更新日期为 2026 年 UTC）

下表 **讨论/inline** 是 API comments/review_comments 数量，不是批准人数。无 assignee 不等于无 owner；所有 PR 都已有作者。开始实际工作前仍须重查 head/base、同题 PR 与维护者分工。

| 入口 | 创建 → 更新 | 状态；作者；assignee | 讨论 / inline | 可交付范围与真实门槛 |
|---|---|---|---|---|
| [AMD-AGI/Infera #179](https://github.com/AMD-AGI/Infera/pull/179) | 10-01 → 10-08 | Open；araina-amd；— | 0 / 0 | 已有作者评审：PP 成本模型；CPU projection/误差分析，实机锚点另验 |
| [AMD-AGI/Infera #188](https://github.com/AMD-AGI/Infera/pull/188) | 10-09 → 10-16 | Open；llying-001；— | 0 / 8 | 已有作者评审：Decode demand/header 变化；与已合入 #186 去重，CPU 路由回归 |
| [AMD-AGI/Infera #198](https://github.com/AMD-AGI/Infera/pull/198) | 10-15 → 10-17 | Open；ChengYao-amd；— | 0 / 0 | 已有作者在研：pinned pool/DCP；CPU 可查 patch anchor，真实 KFD/多卡必须实测 |
| [ROCm/mori #632](https://github.com/ROCm/mori/pull/632) | 09-02 → 09-02 | Open；jhchouuu；— | 0 / 0 | 已有作者补测：同 comm window 并发；CPU 模型不等于 HIP VMM 多卡 |
| [ROCm/mori #717](https://github.com/ROCm/mori/pull/717) | 09-30 → 10-14 | Open；isytwu；isytwu | 1 / 0 | 已有作者补测：gather/copy 双向竞争；W7900 可缩小实验，不复刻 MI355X 数字 |
| [ROCm/mori #768](https://github.com/ROCm/mori/pull/768) | 10-14 → 10-16 | Open；yangyuhuiling；— | 4 / 26 | 已有作者评审：AsyncLL/跨节点；真实多卡/RDMA/特定架构，非单卡任务 |
| [ROCm/mori #787](https://github.com/ROCm/mori/pull/787) | 10-16 → 10-16 | Open / Draft；TianDi101；— | 0 / 0 | 已有作者 Draft：remote read 后验 key；叠在另一分支，CPU 协议模型不是 RDMA 验证 |
| [ROCm/mori #788](https://github.com/ROCm/mori/pull/788) | 10-16 → 10-16 | Open / Draft；TianDi101；— | 0 / 0 | 已有作者 Draft：Clear 保留本地 held spans；CPU 覆盖可分析，真实数据通路另验 |
| [ROCm/rocm-aic #178](https://github.com/ROCm/rocm-aic/pull/178) | 09-23 → 09-28 | Open；sbates130272；sbates130272 | 1 / 0 | 已有作者 VM/compose：需 KVM/镜像；不是物理 GPU 性能 |
| [ROCm/rocm-aic #181](https://github.com/ROCm/rocm-aic/pull/181) | 10-02 → 10-16 | Open；sbates130272；sbates130272 | 11 / 7 | 已有作者构建补测：有 gfx1151 与外部 gfx950 构建反馈，serve/缓存仍有讨论；非空白构建修复 |
| [ROCm/rocm-aic #183](https://github.com/ROCm/rocm-aic/pull/183) | 10-05 → 10-16 | Open；sbates130272；sbates130272 | 0 / 0 | 已有作者 emulated P2P：本地验证三项尚未勾选；KVM+Docker，不保证已可复现 |
| [ROCm/rocm-aic #184](https://github.com/ROCm/rocm-aic/pull/184) | 10-05 → 10-15 | Open；john00003；— | 36 / 4 | 已有作者 CI 加固：36 条讨论、4 条 inline；先看已做方案，自托管权限不可绕过 |
| [LMCache/LMCache #5075](https://github.com/LMCache/LMCache/pull/5075) | 09-11 → 09-25 | Open；jbelloncastro；— | 0 / 0 | 已有作者 ROCTX 补测：现 dev 仍 NVTX-only；本地选择矩阵+单卡 marker，不是完整服务 |
| [LMCache/LMCache #5133](https://github.com/LMCache/LMCache/pull/5133) | 09-16 → 09-16 | Open；plotarmordev；— | 0 / 0 | 已有作者 layout 修复：CPU 可学 stride/尾块；真实 GPU/stream 未验证 |
| [LMCache/LMCache #5615](https://github.com/LMCache/LMCache/pull/5615) | 10-10 → 10-18 | Open；wjinxu；— | 2 / 17 | 已有作者 namespace 修复：KV precision 隔离；CPU key/metadata 回归，真实复用另验 |
| [LMCache/LMCache #5841](https://github.com/LMCache/LMCache/pull/5841) | 10-18 → 10-19 | Open；Vivo50E；— | 0 / 0 | 已有作者异常回传：CPU ZMQ 最小复现/timeout 边界；非 GPU 数据面证明 |
| [vllm-project/vllm #57126](https://github.com/vllm-project/vllm/pull/57126) | 09-16 → 10-16 | Open；zihaomu；shen-shanshan | 10 / 2 | 已有作者且有 assignee：gfx1100 FP8 KV；可复核 W7900，非新题，先检查最新 head |
| [vllm-project/vllm #61109](https://github.com/vllm-project/vllm/pull/61109) | 10-11 → 10-18 | Open；omar-bahaa；— | 3 / 0 | 已有作者 island allreduce：10-12 bot 报冲突；需 8×MI210/拓扑，不是单卡补测 |
| [vllm-project/vllm #61119](https://github.com/vllm-project/vllm/pull/61119) | 10-11 → 10-11 | Open / Draft；akii96；— | 0 / 0 | 已有作者 Draft：deferred reduction；多卡/特定模型，先读 ownership 与准确率 |
| [sgl-project/sglang #38164](https://github.com/sgl-project/sglang/pull/38164) | 09-06 → 10-10 | Open；ormandj；— | 4 / 0 | 已有作者 timeout/consensus：CPU Gloo/生命周期评审；实际 RDMA drain 另验 |

另保留两个**可讨论而非承诺接受**的旧 issue：

- **Infera #36：** 07-29 创建、08-03 更新，Open、无 assignee、0 评论；当前 main 仍有三个 picker，定向 GID PR 搜索也命中 #192 等相邻工作，但未发现明确完成去重的承接。先产出各调用者策略差异与 sysfs fixture，不能把 issue 文字中的“同一策略”直接当源码事实。CPU 可验证读取/策略兼容，真实 RoCE 路径另验。
- **AIC #118：** 08-06 创建/更新，Open、无 assignee、0 评论；Loki PR 定向检索无结果，但 issue 正文本身偏工具讨论而非清晰验收规格。仅作监控备用，需要先确认维护者是否接受范围，不能等同官方悬赏或无人负责。

MORI #92 仍 Open（更新 08-31、3 评论），只证明有明确外部团队协作实例，不是合并成功承诺；JohnQinAMD/sglang-amd API 仍是 upstream fork、Issues 关闭。主贡献入口仍是 AMD-AGI/Infera、ROCm/mori、ROCm/rocm-aic、ROCm/ATOM 及 sgl-project/sglang、vllm-project/vllm、LMCache/LMCache 正式上游。[S145]–[S147][S150][S151]

#### 本期核验到的源码/讨论增量

- **#5075：** head `b8085450` 未变，review submissions 为 0；本次 check-runs API 返回 28 项，**18 success、10 skipped**（包括两项 ROCm build）。这与旧页面“19/29”口径不同，不将 skipped 解释为失败/通过。dev `lmcache/utils.py` 仍只有 NVTX 导入与空 fallback，补丁才增加 ROCTX；NVTX 优先的选择不可自行改写为“所有 ROCm 环境都自动走 ROCTX”。[S145]
- **#717：** 10-14 讨论新增单 MI355X 的并发 restore/store 退化报告。可先准备双向拷贝与计算竞争矩阵；这不是本研究复测，也不是作者尚未做的完整性能改进机会。若提出补测，明确要补哪种设备/shape/争用。[S146]
- **#2464：** 多轮 review 已处理 HBM 预算、Store taint 跨 worker 可见、失败范围等问题。main 有 taint marker；异步 scheduler lookup 等仍在作者列出的 follow-up，但没有核验到维护者接受新 owner 的证据，暂不立项重复 connector。[S152]
- **AIC #181/#183：** 前者已有构建与缓存行为反馈，后者 test plan 仍未勾选。功能设计、构建成功、serve 成功、真实 GPU/RDMA 与性能分别记，不因 QEMU/gfx1250 名字声称已验证新硬件。[S145]

#### 外部账号、CI 与本地资源边界

| 项目 | 当前公开规则与本期纠正 | 对用户的实际影响 |
|---|---|---|
| Infera | 贡献指南仍要求 fork→main、测试/格式及每 commit DCO；成为 collaborator 需管理员批准。**本期 Issues 页面未再复现旧 restricted 提示**，但没测试登录账号权限，不能据此宣布限制已解除 | 沿用允许的入口准备，不把历史限制说成已确认永久禁令，也不预设可发布 |
| MORI | README 欢迎贡献、pre-commit；#744 已入 main。fork PR 不走 rerun label，要用评论命令；当前 workflow 明确要求 admin/maintain/write | “支持 fork PR 重跑”不等于外部作者能自行触发 GPU CI；需维护者，未经授权不调用 |
| AIC | 外部 fork、CI 和至少一位 code owner 批准；metadata 仍 has_discussions=false，与指南 feature-request 入口有差异 | KVM、Docker socket、大镜像、自托管 SPUR 均有现实权限/资源门槛，不承诺免费 |
| SGLang upstream | 指南区分作者自己的失败 CI rerun、加标签/full CI、selective rerun 权限；selective 不构建 PR-local AOT kernel wheel | CPU/mock 与 AMD full CI 分列；没有 runner 不能将“未跑”记通过 |
| vLLM upstream | DCO、AI 辅助披露与人工验证；无 write 仍 6 Open PR 上限；CI 需权限/ready 或 approved，并检查目标分支新鲜度 | 不提交纯 agent/无意义 PR，不用 bypass/放宽门禁来解决资源不足 |
| W7900 与本地 | 用户仅提供单 W7900/按供应窗口的额度条件，没有新增已完成日志 | 本地先做测试设计/CPU 模型；单卡可验 HIP/ROCTX/copy，不能验 TP8、xGMI island、真正 RDMA、EP128 |

规则来自本期指南、workflow 与 repo metadata；未实测用户发布权限。维护者身份与 GitHub author_association 也不等于雇佣身份。[S147][S150]

#### 10-19 首选三项（准备顺序，不要求同时开展）

| 顺序 / 类型 | 最小可交付 | 验证边界 |
|---|---|---|
| **1．hip-kv-transfer-lab：独立学习项目** | KV roundtrip、异物理 block 恢复、event 链、buffer generation/复用、H2D/D2H 单向与双向并发对照；CSV、时间线、错误/负收益解释 | CPU、离线编译、W7900 三栏；故意删除等待的失败复现须有限循环/受控运行，不能以偶然没错证明安全。RDNA GEMM 只作完成主线后的进阶 |
| **2．自研芯片 LMCache：内部工程闭环** | 评估 v0.5.6 候选基线；actual-device/current-stream、dtype/scale/layout、key、lookup/discard/取消回收；冷/热/无复用 A/B 与真实命中证据 | 不自动升级工作环境；遵守公司公开授权与脱敏；没有用户实测前仍记计划，不冒充 ROCm/生产结果 |
| **3．LMCache #5075：已有作者补测；无卡则 Infera #36 CPU 维护分析** | #5075 做四种依赖选择、异常/嵌套、真实 marker+kernel/copy trace；#36 做策略差异/共享读取 fixture 与兼容草稿 | 二选一，先重查分工；#5075 独立装饰器不等于 LMCache E2E；#36 不宣称真实 RoCE 或生产 bug。先形成私有报告，发布需另获用户授权 |

**不再首选 #731 的原因：** 它已合并。现在最有价值的是学习 seam 及 hang→timeout→quiescence 契约，而不是再交实现。新 Draft #787/#788、AsyncLL #768、vLLM #61109 都已有作者且硬件/分支复杂度高，留作源码与评审学习；不为了新 issue 数量扩大主线。

**新提案状态：** 本期没有经过验证、维护者认可的全新无人负责技术题。对 #762 的 local/remote hold、#5615 的 precision key、#5841 的错误回传可以形成覆盖审查草稿；必须先证明遗漏、查同题并确认分工，不能将“我想到一个用例”写成已发现新 bug。

**下一期核验（历史计划）：** Careers 实时申请与 datePosted、92012 最终标题；Infera #198/#203 main 落点和 #188；MORI #717/#768/#787/#788；AIC #181/#183/#184；LMCache #5075/#5133/#5615/#5841 与稳定/ROCm wheel；vLLM #61109/#61119/#57126；SGLang AMD CI 与 host-pool scale 支持范围。

### 19.16 10-26 当前贡献清单、正式上游边界与首选三项

#### 状态变化与新入口

| 对象 | 10-26 核验状态 | 可参与方式与门槛 |
|---|---|---|
| **SGLang #46462 Q4 AMD roadmap** | 10-25 创建、Open、无 assignee、0 评论；正文明确欢迎贡献/反馈 | 它是 roadmap 汇总，不代表每个 bullet 无 owner。可用来选题和查关联 PR；发布实现前仍需定位具体 issue/owner/CI，不直接“认领 roadmap” [S159] |
| **SGLang #46455 per-backend Transport RFC** | 10-25 创建、Open、无 assignee、0 评论，正文标明 Draft for review | 与 ProcessGroupDLCCL/完成语义最贴合。CPU 可做接口状态机、fake transport、幂等 status/close/deregister 用例；真实 Mooncake/NIXL/Mori、peer quiescence、RDMA 需多节点。先做私有评审，维护者确认范围后再考虑代码 [S160] |
| **ATOM #2634 MORI-UMBP RFC** | 10-19 创建、Open、无 assignee、0 评论 | 架构阅读价值高；实现跨度含 scheduler、connector、packing、UMBP、RDMA，不是单人一周任务。可先画 ownership/状态机并列最小 local tier，但不把无 assignee 等同无人推进 [S163] |
| **MORI #839 SDMA 容器可见 GPU 编号** | 10-25 创建、Open、无 assignee、0 评论；issue 已给最小复现和 root-cause 分析 | 需要容器只暴露宿主部分 GPU、MORI main 和 SDMA；单 W7900 云实例未必能构造。若环境可控，可补稳定复现/单测 seam；否则只做代码审查，不声称修复 [S167] |
| **MORI #826 manylinux_2_28 wheels** | 10-21 创建、Open、无 assignee、1 评论 | 低 GPU 依赖、可验证 wheel tag/glibc/import，但与目标岗位数据面相关性较弱，列为包装/CI 备用，不挤占 HIP/KV 主线 [S168] |
| **MORI #811 RAS RFC** | 10-20 创建、Open，作者同时为 assignee，6 评论 | 已有 owner；适合学习 heartbeat、progress、QP root cause、flight recorder、framework hook，不应另起同题实现。与通信超时经历高度相关，可写状态机评审 [S169] |
| **LMCache #5075** | 仍 Open；09-25 后无更新时间；作者 jbelloncastro，无 assignee、0 评论/0 review | 仍可做 W7900 ROCTX 真实 trace 补测，但先问现有作者是否需要；独立 decorator 测试不等于 LMCache E2E [S145] |
| **MORI #823/#825/#831/#836、vLLM #61361/#63142/#63628、ATOM #2630/#2684** | 全部已有作者；部分有 assignee/reviewer，且核心验证分别要求 MI355X 多卡、RDMA、特定模型或大分支 | 作为补测/评审与面试源码案例，不当作空白题。CPU 可验证参数分组、状态机、rollback 和 mock；性能/正确性结论按硬件边界分开 [S162]–[S164][S170][S173]–[S178] |

#### 正式上游与个人 fork

- **正式主入口：** `AMD-AGI/Infera`、`ROCm/mori`、`ROCm/ATOM`、`ROCm/rocm-aic`、`sgl-project/sglang`、`vllm-project/vllm`、`LMCache/LMCache`。
- **10-20 megakernel 文章的临时资源：** 官方文章当前链接 `proaditya/ATOM`、`proaditya/aiter`、`sangeeta0201/fleet-chiplet-megakernel`。这些可以作为 AMD 官方披露的可复现实验资源，但仓库身份仍是个人账号；文章称后续迁移长期归宿，在迁移发生前不把它们列为正式上游任务入口。[S165]
- **Infera release 边界：** main 已含 #198/#209，但公开 release 最新仍 v0.3.0；#214 明确 v0.3.1 先前在未产生产物时撤回。贡献/复测需写 commit SHA 或 image digest，不能笼统写“v0.3.1”。[S155]–[S158]

#### 10-26 首选三项（准备顺序，不要求同时开展）

| 顺序 / 类型 | 最小可交付 | 验证边界 |
|---|---|---|
| **1．hip-kv-transfer-lab：W7900 证据包** | 保留 roundtrip/event/buffer generation/双向并发；新增 `hipHostRegister` vs `hipHostMalloc`、首次触页、复用与清理对照；CSV、rocprof 时间线、负收益解释 | 单卡只证明 HIP 与本机 copy/计算；不外推 MI355X USERPTR queue eviction、RDMA MR、NUMA 大池、TP/EP |
| **2．自研芯片 LMCache：内部闭环** | actual-device/current-stream、payload+scale/layout/key、lookup/discard/cancel、失败 rollback；冷/热/无复用 A/B | 不自动升级；遵守公司授权与脱敏；结果不冒充 ROCm、AMD GPU 或生产规模验证 |
| **3．SGLang #46455 私有接口评审；有 W7900 窗口时补 LMCache #5075 trace** | #46455 输出 protocol/transport ownership 表、PENDING→DONE/FAILED 单调性、deregister/close 前 quiescence 与 fake transport tests；#5075 输出 ROCTX marker+kernel/copy trace | 都先重查作者/维护者意愿；评审不等于实现，W7900 marker 不等于 LMCache E2E。未经用户明确授权不发评论/PR |

**不提升为首选：** MORI #839 虽有清晰 root cause，但需要特定 GPU 可见性容器；#826 易做但岗位相关性低；#811、#823/#825/#831/#836、#61361/#63142/#63628、#2630/#2684 均已有作者或重硬件依赖。Open、无 assignee、roadmap 欢迎贡献都不等同“无人负责”。

**下一期核验：** Req 94063 的官方 `datePosted`、级别和申请状态；旧 Req 92727/87545/78999 的正文恢复；Infera #210/#214 与 v0.3.1 release；SGLang #46462/#46455 的关联 PR/owner；ATOM #2634/#2630；MORI #823/#825/#831/#836/#839；AIC 是否出现非 CI 的数据面变化；LMCache #5075/#5133/#5615/#5841；vLLM #61361/#63142/#63628/#61109/#61119。继续例行更新，未经用户授权不发 issue、评论或 PR。

---

### 19.17 11-02 当前机会、已合并学习基线与首选三项

#### 状态纠正与正式上游边界

| 对象 | 11-02 核验状态 | 当前参与方式与边界 |
|---|---|---|
| **Infera #210/#214** | 均已合入；v0.3.1/v0.3.2 已发布 | 从“待补测机会”移为 release 学习基线。若复现必须固定 tag/image/model；不再按上期 Open 状态另起同题 [S180] |
| **Infera #222** | 10-28 创建，Open、已有作者、无 assignee | caller-supplied KV-event port 与 advertise 契约可做 CPU 配置/参数回归；先看作者是否需要补测，不另起重复实现 |
| **MORI #823/#831/#836/#843/#851/#862/#866/#867** | 已合入 main | 移为源码/测试学习基线；尤其 #862/#867 可在无 GPU/NIC 环境跑控制流。发现明确缺口前不把“给已合并功能补更多测试”写成维护者已请求任务 [S182][S183] |
| **MORI #825/#875/#884** | Open/Draft，均有作者；#884 stacked on #883/#856 | 适合评审 occupancy、buffer ownership、registration 和 ranged I/O；核心性能/正确性需多 GPU/RDMA。未经协调不接管同题 [S183] |
| **MORI #839** | issue 10-30 closed；修复 #841 已合入 | 从开放候选撤下，保留为“容器 GPU 可见编号与 sysfs/HSA node ID”学习案例，不再认领 [S167] |
| **SGLang #46455/#46462** | 仍 Open、无新增评论/assignee | RFC/roadmap 本身不等于无人负责。继续做私有 interface review；具体实现前找关联 PR/owner [S185] |
| **SGLang #46995** | Open，已有作者和 assignee；与 MORI #851 配套 | 可评审 shared pool identity、cache spec fail-closed、Indexer restart；完整联调需要双方版本，CPU mock 不能宣称真实 UMBP 性能 [S185] |
| **vLLM #61361/#63142/#63628** | 已合入 main；尚晚于 v0.32.0 release | 从开放候选撤下，作为 MoRI EPv2、descriptor 合并和 registration rollback 的面试源码案例 [S184] |
| **vLLM #61109/#61119/#64428** | Open/Draft，均有作者 | 适合结合 custom allreduce 做 topology/完成点/量化误差评审；MI210/MI355X 结果不能由 W7900 替代 [S184] |
| **ATOM #2634/#2630** | RFC/Draft 仍 Open，近期无推进 | 仍是 global KV/Rust 数据面的架构阅读，跨度过大，不提升为一周实现任务 [S186] |
| **AIC #192/#193/#197/#201** | Open，均有作者/部分有 assignee；本期重心为 benchmark、CI、wheel | CPU 可做 packaging/CLI/报告回归，岗位数据面相关性弱；不把 nightly wheel 等同生产 KV 验证 [S187] |
| **LMCache #5075/#5133/#5615/#5841** | 仍 Open，近期无推进，均有作者 | #5075 的 W7900 ROCTX trace 仍可做补测；先联系作者/维护者再对外。#5133/#5615/#5841 可做源码/CPU 测试设计，不能绕过真实 GPU/layout/MP 语义 [S188] |
| **LMCache #6175** | 10-29 创建、stacked Draft、已有作者 | 生命周期、read/write pin、process isolation/recovery 很贴合经验，但当前验证为 CUDA/RDMA；适合评审，不把它当 ROCm/W7900 任务 [S188] |

#### CPU、本地、W7900 与重硬件验证边界

| 范围 | 可可信交付 | 不能声称 |
|---|---|---|
| 普通 CPU / 本地 | MORI #867/#862 模拟 session/status/notification/peer failure/tier policy；Infera projector 单测；SGLang Indexer fake-pool；配置/错误路径测试 | 真实 RDMA 顺序、NIC/QP 恢复、GPU direct、带宽/延迟、MI355X/MI45x 兼容 |
| 单卡 W7900 | HIP stream/event、pinned/pageable、ROCTX、copy/compute overlap、单卡 kernel profile | CDNA/MI355X 性能、多卡 XGMI/UALink、RCCL/EP、P/D 跨节点、RDMA/GDS |
| 多卡/多节点/RDMA | QP replacement、two-part completion、UMBP peer tier、MoRI EPv2、shared pool E2E、SGLang DCP/A2A | 没有匹配拓扑和故障注入时，不把 mock/单次模型通过写成生产可靠性 |

#### 11-02 首选三项（按准备顺序，不要求同时开展）

| 顺序 / 类型 | 最小可交付 | 岗位映射与边界 |
|---|---|---|
| **1．MORI simulated-transport evidence pack** | 基于已合入 #867/#862 跑 CPU 场景：registration/session cache、success/failure status、notification、peer disconnect、size mismatch、tier placement；补一份状态机和测试报告 | 最贴合 ProcessGroupDLCCL、通信完成语义和 C++/Python 调用链；只证明模拟控制面/状态机，不证明真实 RDMA [S182] |
| **2．W7900 hip-kv-transfer-lab + ROCTX** | roundtrip、双 stream/event、buffer generation、`hipHostMalloc`/`hipHostRegister`、rocprof 时间线；若版本允许，复核 LMCache #5075 marker | 支撑 94063/89393，并为 96117 提供 profiler 证据；单卡 RDNA 结果不外推 CDNA/多卡。对外补测先确认作者意愿 [S179][S188] |
| **3．自研芯片 LMCache 生命周期闭环** | current device/stream、payload+scale+layout+key、lookup/discard/cancel、失败 rollback、冷/热/无复用 A/B；另写 CUDA IPC 实际范围卡片 | 把既有框架/通信经历转成 KV 数据路径证据；遵守公司授权与脱敏，不冒充 ROCm/AMD 生产验证 |

**未提升为首选：** #875/#884/#46995/#47309/#64428/#6175 均已有作者或依赖重硬件/stacked 分支；AIC 当前增量偏 CI/packaging；96117/89635 所需深 kernel 证据可以作为第四项，待前三项形成稳定交付后再做。

**下一期核验：** 94065/96117/89635 的官方 `datePosted`、级别和申请状态；94063/89393/89499/92012 是否仍开放；Infera #222 与下一 release；MORI #825/#875/#884、SGLang #46995/#47309、vLLM #61109/#61119/#64428、ATOM #2634/#2630/#2786/#2842/#2865/#2866、AIC #192/#193/#197/#201、LMCache #5075/#5133/#5615/#5841/#6175。继续例行更新，未经用户授权不发 issue、评论或 PR。

---

### 19.18 11-09 外部开发者参与：状态纠正、验证门槛与首选三项

#### 正式上游、fork 与贡献入口

- **正式上游入口不变：** `AMD-AGI/Infera`、`ROCm/mori`、`ROCm/ATOM`、`ROCm/rocm-aic`、`sgl-project/sglang`、`vllm-project/vllm`、`LMCache/LMCache`。AMD 文章引用的个人账号 fork 继续按个人 fork 处理，除非代码实际进入上述正式仓库。
- **ATOM 贡献规则仍需按当前仓库执行。** #3088 是 11-07 的 Draft，拟加入 CONTRIBUTING、review guide 与 area contacts；合入前不能把草案中的联系人或流程当作正式承诺。[S204]
- **Infera/AIC 的外部入口限制沿用已核验规则。** Infera 的 issue 创建权限与 AIC 的 feature request/Discussion 路径不因本期 PR 活跃度改变；不能假定外部账号可直接创建任意 issue 或获得 AMD CI/GPU。
- **CI 与硬件可得性不作承诺。** 上游接受外部 PR 不等于免费提供 MI355X/MI45x、多卡、RDMA、RoCE/CXI 或内部镜像；本地 CPU/W7900 证据必须明确硬件边界。

#### 本期对象逐项核验

| 对象 | 创建 / 更新 / 当前状态 | 作者、assignee、关联与当前源码 | 可参与方式与验证边界 |
|---|---|---|---|
| **Infera #229** | 11-02 创建，Open、非 Draft | 作者 `jiejingzhangamd`，无 assignee；补 PyPI router 使用文档 | 已有作者，适合文档审阅/复现，不是无人负责。CPU 可核对命令、配置与链接；不能证明 router/P/D 生产可靠性 |
| **Infera #232/#233** | #232 11-05 Open；#233 11-05 已合入 | #232 作者 `araina-amd`；#233 已进入 main，修正 ROCm/SGLang P/D 兼容矩阵 | #232 可读 prefill chunking/attention-DP；#233 移为已合并学习案例。真实 correctness 仍需指定 MI355X、模型、镜像和长跑，不用少量模型测试替代生产验证 [S192] |
| **MoRI #907** | 11-03 创建，11-06 更新，Open、非 Draft | 作者 `amirakb89`，无 assignee，有评论/评审；#915 因重叠关闭 | 最贴合通信完成语义。可在本地做 WR 生命周期状态机、mock completion/failure 测试设计；真实 CQ/QP、buffer DMA 与 failure injection 需 RDMA。未经协调不接管实现 [S194][S195] |
| **MoRI #923** | 11-06 创建，Open Draft | 有明确 AMD 作者；SDMA AllGather start/wait | 可评审 start/wait ownership 和 API；gfx950/多卡 peer SDMA 才能验证核心正确性/性能，不作为 CPU 独立交付 [S196] |
| **MoRI #929** | 11-06 创建，Open Draft | 作者 `TianDi101`，无 assignee；已有真实硬件结果推进 | 可做复杂度/扫描路径和测试矩阵评审；作者仍在推进，Open/无 assignee 不等于空白任务；UMBP 端到端收益需匹配硬件 [S197] |
| **MoRI #933** | 11-07 创建，Open、非 Draft | 作者 `ZhaiFeiyue`，无 assignee；源码/测试增加 `post_on_host` simulator 模式，作者报告 26 tests passed | CPU 可复现模拟后端、host-posting、per-segment overlap 和失败状态；适合补独立可重复性报告，但先等/问作者是否需要。模拟不证明真实 RDMA/XGMI/时序 [S198] |
| **ATOM #2997/#3027** | #2997 11-04 Open Draft；#3027 11-05 Open、非 Draft | 均有作者；#3027 有 assignee、评论和评审，处理 LMCache/multimodal/checkpoint/deadline | 作为 active work 学习 P/D handoff 与状态唯一性；可做 CPU 配置/metadata tests，不能把作者跑通或模型输出当多节点生产验证 [S200][S216] |
| **ATOM #3068–#3070** | 11-06 创建，全部 Open、非 Draft，stacked chain | 同一作者推进 PP→DCP×TP、MLA staging 与 LMCache state；正文给出作者性能数字和已知限制 | 适合画 producer fence、checkpoint、PP/DCP ownership；CPU 可审 metadata/state，核心性能/正确性需多 GPU。不得拆分 stacked 总收益到单个 PR，也不重复开同题 [S201]–[S203] |
| **ATOM #3088** | 11-07 创建，Open Draft | 作者 `zufayu`，无 assignee；尚未合入贡献指南 | 可审规则清晰度，但在合入前不宣称项目已有该政策或已建立外部 review SLA [S204] |
| **SGLang #49127/#49131** | 11-08 创建，分别 Open 非 Draft / Open Draft | 均有作者；一个补 external-cache linker metrics，一个传播 Mooncake registration failure | metrics 可做 CPU 单测/标签审查；registration 可做 failure-path 单测。真实 Mooncake/ROCm P/D 仍需跨进程/跨节点与 GPU；#49156 已合入同类 fail-fast 主线 [S205][S217][S218] |
| **SGLang #49205** | 11-08 创建，Open、非 Draft | 作者 `hubertlu-tw`，无 assignee；MI450/gfx1250 hierarchical `2shot_push`，有双节点 MI455X 作者 benchmark | 对用户 custom allreduce 经验最有学习价值；可做调用图、拓扑分层、同步/数值测试审阅。真实性能需要两节点 MI455X，已有作者，不作为可认领空白题 [S206] |
| **vLLM #66008** | 11-05 创建，Open Draft | 作者 `amirakb89`；MoRIIO READ lease renewal，已有 MI355X 1P1D 证据 | 可设计 fake clock/lease/state tests、评审 timeout 与 block reuse；silent wrong output 的真实复测仍需 P/D、MoRIIO 和 AMD GPU。先配合作者，不另起同题 [S207] |
| **vLLM #66268/#66339** | 11-07/11-08 创建，均 Open Draft | 前者是 1P2D MiniMax recipe并依赖前置 PR；后者是 MI355X NIXL PD accuracy mirror，受 UCX VMM 支持阻塞 | 作为补测/CI 设计案例；模型通过、synthetic rejection 或 mirror 不等于 accuracy/生产验证。需要多卡 MI355X、P/D、NIXL/UCX [S208][S219] |
| **LMCache #6329** | 11-05 创建，Open、非 Draft | 作者 `yhl-amd`，无 assignee；ROCm 7.2.4 / torch 2.10 nightly wheel for ATOM | CPU 可核 wheel metadata/import/ABI 描述，实际 gfx942/gfx950 与 vLLM/ATOM 组合需 AMD GPU；packaging 相关性低于数据面 [S220] |
| **LMCache #6358** | 11-06 已合入 | VMM shared-KV sleep mode 当前源码已在 main；证明基于 H200/CUDA | 移为已合并学习案例；可以审 borrow/restore/释放状态，不能把 CUDA H200 证明改写成 ROCm/W7900 已验证 [S211] |
| **LMCache #6401/#6411/#6421** | 11-06/11-07 创建，Open 或 Draft | 都有明确作者；分别为 RDMA write、peer DRAM→GPU borrowing、MP read lifetime；后两者 stacked/实验性 | 生命周期/通道 API 很相关，但证据主要来自 H200/RoCE、CPU/unit。可做私有设计评审和 fault matrix；AMD GPU/多卡/RDMA 是实际门槛，不抢占作者工作 [S212]–[S214] |
| **AIC #202/#203** | 11-03/11-07 已合入 | security action pin 与 nightly wheel benchmark job 修复已进 main | 作为 CI/供应链学习案例；本期没有可据此推断的 KV 数据面机会，也不把 nightly wheel 当生产能力 [S215] |

#### 已解决任务与事实纠正

- **MoRI #915：** 11-06 非合并关闭，因与 #907 重叠；保留历史设计价值，但从“可讨论开放任务”撤下。[S195]
- **SGLang #49156：** 已合入 main，Mooncake registration failure 现在 fail-fast；从候选实现移为源码学习基线，尚不声称进入稳定 release。[S205]
- **LMCache #6358：** 已合入 main；其 sleep/VMM shared-KV 功能目前只有 CUDA/H200 证据，不能同步改写为 AMD/ROCm 成熟能力。[S211]
- **Infera #233：** 已合入并修正预览配方；仍按 preview/特定矩阵处理，不能因合并消除其文档中明确列出的验证缺口。[S192]

#### CPU、W7900 与重硬件边界

| 范围 | 本期可可信交付 | 仍需的实际环境 |
|---|---|---|
| **普通 CPU** | MoRI simulator（含 #933 分支的 host-posting）、WR/lease/mock completion 状态机、Infera/ATOM/LMCache 配置与 metadata、wheel/ABI 检查、SGLang failure/metrics 单测设计 | 不能证明 GPU direct、真实 CQ/QP、RDMA ordering、XGMI、P/D 长跑、带宽与尾延迟 |
| **单卡 W7900** | HIP stream/event、host registration、copy/compute overlap、ROCTX/rocprof、单卡 kernel correctness/profile | 不能替代 CDNA/gfx942/gfx950/gfx1250、RCCL/EP、跨节点 P/D、VMM/RDMA/CXI/RoCE |
| **多卡/多节点/RDMA** | #907/#923/#66008/#66268/#66339、SGLang #49205、LMCache #6401/#6411 的核心正确性/性能 | 需要匹配 AMD GPU、拓扑、NIC/driver/ROCm/torch/vLLM/SGLang 组合和故障注入；单次模型输出不等于生产验证 |

#### 11-09 首选三项（准备与可交付，不等于上游 owner）

| 顺序 / 类型 | 最小可交付 | 参与定位与边界 |
|---|---|---|
| **1．MoRI simulator + WR quiescence evidence pack** | 基于 main #867/#862 跑 registration/session/status/failure；若 #933 可复现，再加 host-posting/per-segment overlap；用 #907/#915 画 `posted → in-flight → terminal → reusable` 状态机和负例 | 最贴合 ProcessGroupDLCCL、集合通信和完成语义。输出可先保持私有；模拟不证明 RDMA，#907/#933 都有作者，未经确认不提交同题实现 [S194][S195][S198] |
| **2．W7900 hip-kv-transfer-lab + ROCTX** | pageable/pinned/registered、stream/event、双向 copy、buffer generation、copy/compute overlap、负收益；固定 ROCm/torch/arch，输出 CSV、时间线和误差 | 支撑 96120/96121/94063；只证明单卡 RDNA/HIP。不得外推 MI355X、gfx1250、RCCL、P/D 或 RDMA |
| **3．KV 生命周期 + custom allreduce 源码评审包** | 用 vLLM #66008 写 lease/reuse 测试矩阵，用 SGLang #49156 写 fail-fast checklist，用 #49205 对照既有 vLLM custom allreduce 调用链，标出 topology、sync、ownership 与数值边界 | 可在 CPU/静态分析阶段完成，形成面试材料；上游 PR 均有作者，评审不等于贡献，作者 benchmark 不变成本人或通用硬件结果 [S205]–[S207] |

**新提案判断：** 本期没有确认一个“维护者尚未实现、无人推进、且适合直接认领”的高相关任务。#907、#929、#933、#3068–#3070、#49205、#66008、#6401/#6411/#6421 都已有作者；可做的是独立复现、补测设计、评审或在维护者明确需要后协作。未经用户明确授权，本手册不会发布 issue、评论或 PR，也不会承诺外部作者身份、免费硬件、合并或求职结果。

**下一期核验：** Req 96120/96121 的 official datePosted、级别、团队与申请状态；94063/94065/96117/89635/89393/89499；Infera #229/#232 与下一个 release；MoRI #907/#923/#929/#933；ATOM #2997/#3027/#3068–#3070/#3088；SGLang #49127/#49131/#49205 及 #49156 的 release 落点；vLLM #66008/#66268/#66339；LMCache #6329/#6401/#6411/#6421 与稳定 ROCm release；AIC 是否出现非 CI 的数据面增量。继续例行更新。

---


## 结语

你已经做过的框架适配不是“没有相关性”，但也不是 EP/RDMA/全局 KV 的完整经验。最合理的证明方式，是把真实的两项集成工作讲清楚，再完成一个可复现的 LMCache 数据路径项目。

> 用源码、测试、版本和端到端对照展示能力；阅读案例写成学习，计划写成计划，只有实际完成的工作写成成果。优先申请符合真实深度的框架集成岗位，再向 KV/通信数据面延伸。




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

[S65]: https://careers.amd.com/api/jobs?keywords=inference&location=China&limit=100
[S66]: https://github.com/AMD-AGI/Infera/pull/171
[S67]: https://github.com/ROCm/mori/pull/652
[S68]: https://github.com/ROCm/mori/pull/687
[S69]: https://github.com/ROCm/rocm-aic/pull/166
[S70]: https://github.com/ROCm/rocm-aic/pull/168
[S71]: https://github.com/ROCm/ATOM/pull/2223
[S72]: https://github.com/ROCm/ATOM/pull/2284
[S73]: https://github.com/ROCm/ATOM/pull/2315
[S74]: https://github.com/vllm-project/vllm/pull/57160
[S75]: https://github.com/vllm-project/vllm/pull/51052
[S76]: https://github.com/sgl-project/sglang/pull/39910
[S77]: https://github.com/LMCache/LMCache/pull/4957
[S78]: https://github.com/LMCache/LMCache/pull/5157
[S79]: https://github.com/LMCache/LMCache/blob/dev/docs/source/developer_guide/extending_lmcache/adding_a_new_device_backend.rst
[S80]: https://github.com/LMCache/LMCache/pull/5133
[S81]: https://rocm.blogs.amd.com/artificial-intelligence/mlperf-inf-v6.1/README.html
[S82]: https://rocm.blogs.amd.com/software-tools-optimization/thread-trace/README.html
[S83]: https://careers.amd.com/careers-home/jobs/89393?lang=en-us
[S84]: https://careers.amd.com/careers-home/jobs/92012?lang=en-us
[S85]: https://careers.amd.com/careers-home/jobs/92050?lang=en-us
[S86]: https://github.com/ROCm/mori/pull/662
[S87]: https://github.com/sgl-project/sglang/pull/39763
[S88]: https://github.com/ROCm/rocm-aic/pull/160

[S89]: https://careers.amd.com/careers-home/jobs/92727
[S90]: https://github.com/AMD-AGI/Infera/issues/9
[S91]: https://github.com/ROCm/mori/pull/656
[S92]: https://github.com/ROCm/mori/pull/709
[S93]: https://github.com/ROCm/mori/pull/711
[S94]: https://github.com/ROCm/ATOM/pull/2167
[S95]: https://github.com/ROCm/ATOM/pull/2339
[S96]: https://github.com/ROCm/ATOM/pull/2268
[S97]: https://github.com/ROCm/ATOM/pull/2351
[S98]: https://github.com/sgl-project/sglang/pull/41402
[S99]: https://github.com/vllm-project/vllm/pull/58098
[S100]: https://github.com/ROCm/rocm-aic/pull/176
[S101]: https://rocm.blogs.amd.com/software-tools-optimization/hyperloom-optimization/README.html
[S102]: https://rocm.blogs.amd.com/artificial-intelligence/kimi-k3-mad/README.html
[S103]: https://rocm.blogs.amd.com/software-tools-optimization/profiling-guide/att/README.html
[S104]: https://rocm.blogs.amd.com/software-tools-optimization/ultraquant-kv4/README.html
[S105]: ROCm_HIP_7_Day_W7900_Roadmap_2026-09-24.md
[S106]: https://github.com/LMCache/LMCache/pull/5075
[S107]: https://github.com/AMD-AGI/Infera/issues/36
[S108]: https://github.com/vllm-project/vllm/pull/57126
[S109]: https://github.com/vllm-project/vllm/blob/main/docs/contributing/README.md
[S110]: https://careers.amd.com/careers-home/jobs/92727
[S111]: https://careers.amd.com/careers-home/jobs/89764
[S112]: https://github.com/AMD-AGI/Infera
[S113]: https://github.com/AMD-AGI/Infera/pull/179
[S114]: https://github.com/ROCm/mori/pull/717
[S115]: https://github.com/ROCm/mori/pull/718
[S116]: https://github.com/ROCm/mori/pull/711
[S117]: https://github.com/ROCm/ATOM/pull/2459
[S118]: https://github.com/ROCm/ATOM/pull/2464
[S119]: https://github.com/ROCm/rocm-aic/pull/178
[S120]: https://github.com/AMD-AGI/Infera/issues
[S121]: https://github.com/ROCm/ATOM/releases/tag/v0.1.6
[S122]: https://careers.amd.com/careers-home/jobs/92727
[S123]: https://github.com/AMD-AGI/Infera/pull/183
[S124]: https://github.com/ROCm/mori/pull/716
[S125]: https://github.com/ROCm/mori/pull/729
[S126]: https://github.com/ROCm/ATOM/pull/2518
[S127]: https://github.com/LMCache/LMCache/pull/5157
[S128]: https://github.com/LMCache/LMCache/pull/5565
[S129]: https://github.com/ROCm/mori/pull/731
[S130]: https://github.com/ROCm/rocm-aic/pull/183
[S131]: https://github.com/ROCm/ATOM/pull/2459
[S132]: https://github.com/LMCache/LMCache/pull/5075
[S133]: https://github.com/ROCm/rocm-aic/pull/177
[S134]: https://github.com/vllm-project/vllm/pull/61109
[S135]: https://github.com/sgl-project/sglang/pull/43719
[S136]: https://careers.amd.com/careers-home/jobs/92012
[S137]: https://github.com/AMD-AGI/Infera/pull/186
[S138]: https://github.com/AMD-AGI/Infera/pull/198
[S139]: https://github.com/ROCm/mori/pull/711
[S140]: https://github.com/ROCm/mori/pull/756
[S141]: https://github.com/ROCm/mori/pull/762
[S142]: https://github.com/LMCache/LMCache/releases/tag/v0.5.6
[S143]: https://github.com/sgl-project/sglang/pull/40917
[S144]: https://github.com/vllm-project/vllm/pull/60544
[S145]: https://github.com/LMCache/LMCache/pull/5075
[S146]: https://github.com/ROCm/mori/pull/717
[S147]: https://github.com/ROCm/mori/pull/744
[S148]: https://rocm.blogs.amd.com/software-tools-optimization/rdna-fp16-gemm/README.html
[S149]: https://rocm.blogs.amd.com/artificial-intelligence/glm53-mi300x-vllm/README.html
[S150]: https://github.com/sgl-project/sglang/issues/35003
[S151]: https://github.com/LMCache/LMCache/pull/5615
[S152]: https://github.com/ROCm/ATOM/pull/2464
[S153]: https://careers.amd.com/careers-home/jobs/94063
[S154]: https://github.com/ROCm/ATOM/releases/tag/v0.1.8
[S155]: https://github.com/AMD-AGI/Infera/pull/198
[S156]: https://github.com/AMD-AGI/Infera/pull/209
[S157]: https://github.com/AMD-AGI/Infera/pull/210
[S158]: https://github.com/AMD-AGI/Infera/pull/214
[S159]: https://github.com/sgl-project/sglang/issues/46462
[S160]: https://github.com/sgl-project/sglang/issues/46455
[S161]: https://github.com/ROCm/mori/pull/821
[S162]: https://github.com/ROCm/mori/pull/823
[S163]: https://github.com/ROCm/ATOM/issues/2634
[S164]: https://github.com/vllm-project/vllm/pull/61361
[S165]: https://rocm.blogs.amd.com/software-tools-optimization/megakernel-intro/README.html
[S166]: https://github.com/ROCm/rocm-aic/pull/181
[S167]: https://github.com/ROCm/mori/issues/839
[S168]: https://github.com/ROCm/mori/issues/826
[S169]: https://github.com/ROCm/mori/issues/811
[S170]: https://github.com/ROCm/ATOM/pull/2630
[S171]: https://github.com/ROCm/mori/pull/788
[S172]: https://github.com/ROCm/mori/pull/838
[S173]: https://github.com/ROCm/mori/pull/825
[S174]: https://github.com/ROCm/mori/pull/831
[S175]: https://github.com/ROCm/mori/pull/836
[S176]: https://github.com/vllm-project/vllm/pull/63142
[S177]: https://github.com/vllm-project/vllm/pull/63628
[S178]: https://github.com/ROCm/ATOM/pull/2684
[S179]: https://careers.amd.com/careers-home/jobs/94065
[S180]: https://github.com/AMD-AGI/Infera/releases/tag/v0.3.2
[S181]: https://github.com/AMD-AGI/Infera/pull/217
[S182]: https://github.com/ROCm/mori/pull/867
[S183]: https://github.com/ROCm/mori/pull/875
[S184]: https://github.com/vllm-project/vllm/pull/61361
[S185]: https://github.com/sgl-project/sglang/pull/46995
[S186]: https://github.com/ROCm/ATOM/issues/2866
[S187]: https://github.com/ROCm/rocm-aic/pull/199
[S188]: https://github.com/LMCache/LMCache/releases/tag/nightly-rocm
[S189]: https://careers.amd.com/careers-home/jobs/96120?lang=en-us
[S190]: https://careers.amd.com/careers-home/jobs/96121?lang=en-us
[S191]: https://github.com/AMD-AGI/Infera/releases/tag/v0.3.3
[S192]: https://github.com/AMD-AGI/Infera/pull/233
[S193]: https://github.com/ROCm/mori/releases/tag/v1.2.5
[S194]: https://github.com/ROCm/mori/pull/907
[S195]: https://github.com/ROCm/mori/pull/915
[S196]: https://github.com/ROCm/mori/pull/923
[S197]: https://github.com/ROCm/mori/pull/929
[S198]: https://github.com/ROCm/mori/pull/933
[S199]: https://github.com/ROCm/ATOM/releases/tag/v0.1.9
[S200]: https://github.com/ROCm/ATOM/pull/3027
[S201]: https://github.com/ROCm/ATOM/pull/3068
[S202]: https://github.com/ROCm/ATOM/pull/3069
[S203]: https://github.com/ROCm/ATOM/pull/3070
[S204]: https://github.com/ROCm/ATOM/pull/3088
[S205]: https://github.com/sgl-project/sglang/pull/49156
[S206]: https://github.com/sgl-project/sglang/pull/49205
[S207]: https://github.com/vllm-project/vllm/pull/66008
[S208]: https://github.com/vllm-project/vllm/pull/66268
[S209]: https://github.com/LMCache/LMCache/releases/tag/v0.5.7rc4-rocm
[S210]: https://github.com/LMCache/LMCache/releases/tag/nightly-rocm
[S211]: https://github.com/LMCache/LMCache/pull/6358
[S212]: https://github.com/LMCache/LMCache/pull/6401
[S213]: https://github.com/LMCache/LMCache/pull/6411
[S214]: https://github.com/LMCache/LMCache/pull/6421
[S215]: https://github.com/ROCm/rocm-aic/pull/203
[S216]: https://github.com/ROCm/ATOM/pull/2997
[S217]: https://github.com/sgl-project/sglang/pull/49127
[S218]: https://github.com/sgl-project/sglang/pull/49131
[S219]: https://github.com/vllm-project/vllm/pull/66339
[S220]: https://github.com/LMCache/LMCache/pull/6329
