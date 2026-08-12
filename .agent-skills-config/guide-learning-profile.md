# `guide-learning`：PlanA 配置层

本文只保存中央 `guide-learning` 在 PlanA 中运行时需要的仓库事实：状态路径、单写者、
实际时长归属和领域透镜。教学微循环、检查、练习、Review、mastery、暂停与恢复行为均由中央
Skill 定义，不在本仓库复制。

## 1. 状态路径

| 逻辑职责 | PlanA 位置 | 路径规则 |
| --- | --- | --- |
| 长期 Program | [`计划/主计划.md`](../计划/主计划.md) | 保存长期目标、范围、候选 Lesson 与总预算；专项计划只引用它 |
| 临时 Program | `计划/` 下由用户明确启动的专项计划 | 只保存该专项的目标、范围、候选 Lesson、预算与返回引用 |
| Lesson evidence ledger | 当前 Checkpoint 所引用的设计包、实验包或稳定 Lesson 章节 | 保存 Lesson 目标、来源、阶段、finding、evidence 与经确认的 mastery |
| Lesson Session event | 当前 Lesson evidence ledger | 与对应 Lesson evidence 保持同一活动 owner |
| 独立 Session event | 实际任务所属模块已有的记录位置 | 沿用模块已经存在的记录位置 |
| 实际时长 | 实际任务所属模块的 `进度.md` | 只记录用户提供或确认的值 |
| Checkpoint | [`计划/学习断点.md`](../计划/学习断点.md) | 唯一可覆盖恢复游标；当前 Program 与 Lesson 均从这里的引用发现 |
| 派生 dashboard | [`计划/进度总表.md`](../计划/进度总表.md) | 周日或经批准的周期触点更新，不反向裁决活动状态 |
| 稳定课程与资料范围 | 各模块 `学习指引.md` | 只在获准的资料治理触点修改，不保存当前游标或 Lesson evidence |

JSON 的 `record_mappings` 只登记当前已确认的活动 Program、Lesson、Session event 与 Checkpoint owner，
作为受管写入的机械上限。它不保存状态正文，也不构成推进或写入授权；普通节点推进不改配置。只有用户
确认切换活动 owner 时，才在同一迁移事务中更新对应 mapping 并重新 materialize。

当前活动 Lesson 属于推理框架，因此公共配置只把 `推理框架/进度.md` 暴露为实际时长与模块进度事实；
切换到其他模块时，应随 owner 切换把对应模块的 `进度.md` 映射为 `progress-source`，不读取派生总表代替它。

## 2. 单写者与时长归属

| 事实 | 唯一活动 owner |
| --- | --- |
| 长期目标、范围与总预算 | `计划/主计划.md` |
| 专项目标、范围、专项预算与候选 Lesson | 相应专项计划 |
| Lesson 阶段、finding、evidence 与 final mastery | 当前 Lesson evidence ledger |
| 当前语义位置、唯一下一动作、前进门槛与返回点 | `计划/学习断点.md` |
| 用户确认的实际学习时长 | 实际任务所属模块的 `进度.md` |
| 全局完成度与周期汇总 | `计划/进度总表.md`，仅作为派生视图 |

专项按实际学习内容归账，不建立第二套累计时长：

- vLLM、推理服务、调度、KV cache 与 PD 分离归 [`推理框架/进度.md`](../推理框架/进度.md)；
- PyTorch Dispatcher、custom op、后端接入归 [`PyTorch/进度.md`](../PyTorch/进度.md)；
- collective、P2P、RDMA 与通信数据面归 [`训练框架与分布式/进度.md`](../训练框架与分布式/进度.md)；
- 其他任务归实际所属模块的 `进度.md`。

计划时长与预计投入不是实际时长；实际时长的唯一原始来源是用户确认后写入的模块 `进度.md`。

## 3. PlanA 领域透镜

只在有助于当前节点时，从以下透镜中选择最相关的一项或少数几项，不要求每次全部展开：

- **PyTorch**：Dispatcher、算子 schema、fake/meta、设备与 stream 语义、PrivateUse1 和后端接入；
- **vLLM**：请求生命周期、EngineCore／Scheduler／Worker／ModelRunner 所有权和扩展边界；
- **KV cache 与 PD**：逻辑到物理 block 映射、producer／consumer ownership、传输、ready、cleanup 与失败语义；
- **通信**：collective、P2P／RDMA、内存注册、同步、拓扑与故障边界；
- **自研芯片适配**：框架不变量、设备能力槽位、adapter 边界、正确性证据和性能归因。

自研芯片映射只使用用户已提供或获准公开的能力事实；未披露接口、拓扑、性能数据和内部实现保持
未知，不用 CUDA、ROCm 或其他平台的能力替代。

## 4. 配置边界

- 本文件只提供静态仓库事实，不保存教学步骤或当前状态正文。
- W18/W26/W32 是只读 legacy 资源报告；新的静态目录、动态 registry 与课程 slot 由 `resource-planning` 独立拥有，不进入教学状态。

## 5. 文章产物适配

- 学习文章沿用模块内现有系列目录，不为通用规范创建第二棵文章树；当前受管目标是
  `PyTorch/深入学习理解PyTorch/` 与 `推理框架/深入学习理解vLLM/`。
- 主要语言为中文，使用同伴式技术解释：展示问题、理解变化和证据边界，不采用讲台式命令口吻。
- 领域内容优先连接实际工程、源码所有权、版本锚点、可复核数字、反例与面试迁移；只有已有证据时
  才连接过往经验，不杜撰经历、实验或公司内部事实。
- vLLM 系列只有已跟踪 Markdown，继续采用 `sequence-topic`，编号以该 collection 的现有序列为准。
- PyTorch 系列目录混有图像与绘图证据，不把整个目录授权为可读知识 collection；新文章采用
  `yyyy-mm-dd-topic`，只把用户本轮明确选择的来源与目标纳入写入事务。既有 `0-Index.md` 与
  `1-Internal-Overview.md` 保持历史命名，不为统一文件名而改写。
