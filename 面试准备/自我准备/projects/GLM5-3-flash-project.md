## 项目：GLM-5.3-Flash 模型适配与优化（已完成）

> 事实依据：[GLM-5.3-Flash 推理适配项目总结](GLM-5.3-flash-project-summary.md)及本人 2026-11-02 的问答补充；沿用旧档案中未被新材料替代的实践细节。项目已完成，由云服务团队正式生产上线。
> 本档案整理项目经历、职责和结果口径；原始代码、测试日志与评测报告仍由总结中的证据索引指向，本次未重新运行验证。下方【待补充／待核验】用于完善复现与面试材料，不改变已交付状态。
> 对外统一使用“自研 AI 加速芯片”，不写内部代号、内部仓库名或内部算子编号。

### 项目概览

| 字段 | 当前信息 |
|---|---|
| 开发与交付时间 | 2026-09-01 至 2026-10-27；截至 2026-11-02 已确认生产上线，实际首次上线日期本人不掌握 |
| 角色 | AI 框架开发工程师；独立负责本模型在既有 vLLM 硬件插件中的适配开发、插件侧性能优化、排障与发布验证 |
| 模型与部署 | GLM-5.3-Flash-Mix，AWQ 4-bit 权重、BF16 激活，8 卡自研 AI 加速芯片、TP=8、`block_size=256` |
| 最终软件基线 | vLLM `0.30.1rc0`、PyTorch `2.5.0` 芯片后端、自研 vLLM 插件与 AOT 算子库；模型 revision、插件及后端发布标识待补充 |
| 发布执行路径 | 文本推理、V1 runner、`FULL_DECODE_ONLY`；decode 使用 graph，prefill／chunked prefill 使用 eager |
| 发布范围之外 | MTP、多模态、FP8、V2 runner、计算与通信重叠；MoE router 仍使用 BF16 logits |
| 交付与精度结果 | 云服务团队正式生产上线；OpenCompass 单轮、每题一次生成的 AIME26 结果为 30/30，与团队在 8 卡 H100 上运行同一模型的准确率一致 |
| 验收目标 | AIME 数据集准确率与 CUDA 机器测试一致；单请求输出 token 间隔低于 70 ms |
| 工具 | Python、C++、`py-spy`、PyTorch／vLLM profiler、芯片 profiler、隔离微基准、`pytest` |

旧稿中的 vLLM `0.28.1rc0`、仅 eager、端到端精度未验证及项目进行中等描述，已由本次总结的发布基线和交付结果替代。

### 项目背景与结构

项目需要将 GLM-5.3-Flash 的文本推理能力接入自研芯片并交付云服务。项目开始时，上游实现依赖 Triton、TileLang 和 `torch.compile`，目标平台无法直接使用这些执行路径。我的工作从模型语义、权重和状态缓存接入开始，建立可验证的 native 路径，再逐步接入芯片融合算子、优化 Host／Device 执行并完成 decode graph 适配。

模型约有 321B 总参数、18B 激活参数，45 层按 `[KDA×3 + 稀疏 MLA]×11 + KDA` 排列。主要适配对象如下；模型声明的 1,048,576-token 上下文上限与本次部署容量分别记录。

| 结构 | 本项目处理的适配问题 |
|---|---|
| 34 层 KDA | 同时维护 conv state 与 recurrent state；prefill、decode、状态迁移和 graph padding 使用不同调用条件 |
| 11 层 KPool／NoPE 稀疏 MLA | 每 4 个 token 形成 pooled key，完成池级选择、token 索引展开及尾池处理；512 维 latent、`qk_rope_head_dim=0` 需要独立于旧 576 维布局的路径 |
| 四路 mHC 残差 | 对齐残差混合、20 轮 Sinkhorn 与 RMSNorm 语义，接入 pre、post、fused post+pre |
| 42 层 AWQ MoE | 288 个路由专家取 Top-8，另有共享专家；处理权重打包、`qzeros` 布局和 `swiglu_limit=10` |
| 混合缓存 | MLA、KPool index、KPool tail 和 KDA 状态不能直接共用同一页大小与分组假设 |

本人不掌握最终服务的具体业务场景和实际首次上线日期，按未知记录。项目验收目标已明确为 AIME 准确率与 CUDA 对照一致，以及单请求输出 token 间隔低于 70 ms。

### 职责与协作边界

- **我负责**：模型注册与绑定、权重映射、native 执行路径、混合 KV 分组与容量核算、状态拆池和迁移；算子需求、调用契约、验收及插件接入；Profile 与插件侧优化、Graph metadata 和 padding 修复、NaN 排障、warmup 后 null block 清零的代码修复、定向回归及交付文档。
- **我与同事协作**：给算子团队提供复现、接口及验收条件，跟进融合算子缺陷；向 PyTorch 后端提交 strided copy 问题；与运行时／通信团队拆分 allreduce 的等待和通信耗时。
- **其他团队负责**：融合 Kernel 的实现与 Kernel 性能优化；芯片 Runtime、驱动、集合通信库和编译器后端的实现；云服务团队负责正式生产部署并提供 AIME26 结果反馈。
- **既有团队基础**：插件平台框架、以往模型适配和算子基础设施，不作为本人在本项目中新建的成果。
- **关键修改分工（2026-11-02 本人确认）**：KDA 高地址换算和 KPool 长上下文问题由我定位，算子同事修改代码并优化，我再验收问题是否消失及性能结果；warmup 后清零 null block 由我完成定位、代码修复和验收。

### 关键行动

#### 1. 建立模型路径与权重映射

我在插件中接入 KDA、KPool、mHC 和 512 维 NoPE 稀疏 MLA，处理模型与 inner model 的独立命名空间，补齐 `gate_up`、`fused_qkv_a`、`wk_weights`、`in_proj_qkvbfg_a` 等打包映射，避免继承旧模型映射后误量化 Dense 层。

编写 safetensors header／index 静态审计脚本，核对 111,346 个权重 key 的映射与跳过规则；其中 889 个 MTP key 因本次不启用 MTP 被明确跳过。审计记录无 missing、unexpected 或重复目标，不能据此表述为所有 checkpoint 结构均已启用。

适配阶段先以 CPU FP32 参考和 native 实现检查语义，再逐项验收融合算子。旧档案已记录的 KPool“逐 head 点积 → ReLU → 按 head 加权”及稀疏 MLA 的 `1/sqrt(256)` scale 修正继续保留。

#### 2. 修复混合 KV cache 的两次 OOM

第一次 OOM 来自分组、容量核算与实际分配不一致：上游将 34 层 KDA 合为一组，假设 KDA 状态页可以装入 MLA 页，但目标平台按层独立分配，且实际 KDA 页更大，导致 `num_blocks` 高估。我将 KDA 拆成每层独立 spec，并分别处理 MLA、KPool index 和 KPool tail，按真实页大小计费。

第二次 OOM 来自平台层沿用共享页布局的额外 Padding。核对实际访问范围后，去掉这部分不必要的补齐，使核算与分配使用一致的页容量。旧档案中的 CPU 分组／核算／分配单测，以及真机容量由 45,409 提升至 148,762 tokens 的结果继续保留，显存利用率为 0.85。

总结另给出后续配置的单请求预算：`B(L)=69+2×ceil(L/256)`，其中 L 为请求长度，69 对应 34 层 KDA 各 2 个状态 block 和 1 个 tail block。相应的容量推导与实际验证长度见“容量与长上下文”。

#### 3. 状态拆池消除非连续搬运开销

早期服务能够执行，但同一短 prompt 下，prefill 单步 Host 耗时约 179 s，decode 单步约 120 s。通过 `py-spy`、模型内 Profile 和隔离微基准，我定位到 conv state 与 recurrent state 打包在同一字节页后形成非连续 view；目标后端对这类访问退化为 Host 逐元素搬运，开销与整个 Storage 大小相关。

我将两种状态拆成独立连续池，保持总字节数及 block ID 语义，适配清零、runner 绑定和状态迁移。该阶段通过 21 项单测和真机对照；在相同短 prompt 的插桩测量中，prefill 单步 Host 耗时降至约 5.7 s，decode 降至约 2.6 s。适配期保留回退开关，发布期的代码清理另见第 8 项。

隔离微基准中，只搬运 8 页／约 4 MiB 时，`index_select + clone` 的连续池与页内 view 耗时为 0.181 ms／579.7 ms，`index_copy_` 为 1.544 ms／1,873.0 ms。这些结果支持布局路径的归因，不能换算成端到端吞吐提升倍数。

#### 4. 验收并接入融合算子

我对 18 项候选需求进行覆盖核查，形成 12 条首轮提交；后续验收并接入 KDA 短卷积、chunk prefill、recurrent decode、gated RMSNorm、state gather／scatter，KPool 更新／压缩、select／top-k／expand、slot mapping，以及 512 维 NoPE 稀疏 MLA 和 mHC 融合路径。

验收中发现并推动处理长序列卡死、wrapper 整池搬运、Kernel 未按 stride 读取、ATen scalar 打包错误、PAD 槽语义和状态布局不一致等问题。对 mHC 曾出现的“native 与 fused 两侧都回退，数值比较仍通过”，我加入调用计数断言，确认测试实际命中融合路径。

我将 KPool 的历史长上下文瓶颈定位到 select／top-k 融合算子的扫描与并行效率，由算子同事修改和优化代码，再由我验收问题是否消失及性能情况。算子级时延改善与整模结果分别记录，不将其全部归为插件代码的独立收益；单请求长上下文的具体测量配置仍待补齐。

#### 5. 减少 Host／Device 往返与下发次数

我结合 Profile、拷贝事件及隔离实验识别 Host 开销，并实施 metadata H2D 合并、pinned／device buffer 常驻、静态参数加载期预物化，以及 KPool 阻塞 D2H 消除。对设备侧 view 物化逐项检查，结合融合算子减少下发次数。

总结中的 profiled decode 对照记录：view 物化由 204 次／步降到 0，Kernel 下发由 3,888 次降到 1,982 次，设备空洞由 389.5 ms 降至 29.1 ms，原约 223 ms／步的长阻塞 D2H 被消除，未再出现大于 0.5 ms 的该类阻塞项。这些是带 Profile 的流水线指标，不能替代干净服务计时。

与运行时／通信团队拆分后，allreduce 的主要开销来自等待其他 rank 到达。屏障到达偏斜累计由 220.5 ms 降至 90.4 ms，尚未达到不高于 20 ms 的优化目标；计算与通信重叠未纳入本次发布。

#### 6. 完成 decode Graph 与 Padding 修复

最终使用 `FULL_DECODE_ONLY`，启动捕获 35 张 decode graph，最大 capture size 为 256；prefill 与 chunked prefill 继续使用 eager。

首次 8 并发验证时，实际 6 个 decode token 被放入大小为 8 的 graph bucket。输入补到了 8 行，但 `query_start_loc` 的尾部边界仍为 6，模型侧还截断了 metadata，造成输入行数与序列边界不一致。我在 metadata 构造阶段为尾部 PAD token 配置 NULL state 槽及完整边界，并让 KDA 传递完整的持久 `cu_seqlens` buffer。

修复后，总结报告 1／2／8／16／24／32 并发的 Graph 矩阵通过。相同 prompt、`temperature=0`、32-token 输出的 graph／eager 对照逐字一致。

单请求与并发收益按各自测例保留，见下表；64 并发测例中 graph 没有获得收益。replay cache 又在另一组测例中降低了 gap，不能将不同输入长度的最低数字组合成一个服务指标。

#### 7. 定位两个 NaN 根因并分别完成修复

服务曾在健康检查和请求均返回 HTTP 200 时输出连续感叹号，hidden states／logits 含 NaN。我通过 sentinel、首个异常层检查、地址阈值实验及高地址占位对照，将问题拆为两个独立根因。

| 根因 | 证据与修复 | 验证及归属边界 |
|---|---|---|
| KDA state pool 地址换算回绕 | 目标路径以 32 位进行地址单位换算，超过 16 GiB 后回绕，gather 未正确写入；将 metadata、word offset、地址转换和 gather／scatter 共用 copy 路径统一为 64 位 | 我负责定位问题，算子同事修改代码，我再进行功能与性能验收；补充高地址 gather／scatter 回归 |
| sparse MLA null block 被 warmup 污染 | 修复前一根因后，首个 NaN 从 layer 0 移到 layer 3；dummy warmup 以全 0 slot mapping 将 NaN 写入 null block 0，无效 top-k 索引读取该块并在 mask 前进入计算 | 我完成定位、代码修复和验收：在全部 dummy／warmup 完成后、服务 ready 前再次清零 null block，服务级请求恢复正常 |

总结中的 dummy run 改用 `PAD_SLOT_ID(-1)`／scratch block、读取端提前清理无效索引属于后续加固建议，不计为本次已实现。HTTP 成功、单元测试通过和模型正确性分别验证，不能互相替代。

#### 8. 完成发布与交接

2026-10-23 清理 native／fallback、CPU 对比分发及诊断探针，统一生产执行路径；保留生产必需的 AWQ Host 布局逆变换与反量化辅助函数。发布定向回归为 `161 passed, 10 subtests passed`，并通过编译与静态检查；旧稿约 292 项属于早期测试范围，不与本次数量直接合并或比较。

2026-10-26 至 2026-10-27 完成 replay cache 复测、block numel 校验修复、发布基线与部署文档。云服务团队完成正式生产上线并反馈端到端评测结果。总结记录累计形成 50 余份设计、验证、排障及交付文档，40 余个探针脚本；名称与用途见总结的证据索引，原始路径不在本档案展开。

### 验证与量化结果

#### 功能、数值与交付

| 验证层级 | 已有结果 | 适用范围与待补条件 |
|---|---|---|
| 算子级数值对照 | 旧档案记录 KDA conv／decode state 一致、decode 输出误差不超过 1 个 BF16 ULP，KV 清零与 MLA cache 写入逐字节一致，mHC 融合与 native 误差不超过 `6.4e-5` | 各结果属于对应算子与测试阶段；不扩大为全模型逐位一致 |
| 请求与并发功能 | 服务、健康检查、模型列表、单请求与流式输出通过；8 并发完成 256 个输出 token；Graph 多档矩阵通过 | 各组矩阵的运行配置待补充 |
| Graph／eager 一致性 | 相同 prompt、`temperature=0`、32-token 输出逐字一致 | 不等同所有输入、长序列或 logits 全量一致 |
| 长上下文功能 | 3,610 prompt／8 output、16K／32K chunked prefill 有通过记录；131,072 长度在 eager／0.85 配置下验证 | 生产 `max-model-len`、实际输入长度和容量推导分别核对 |
| 发布回归 | `161 passed, 10 subtests passed`；高地址 gather／scatter 及 NaN 服务回归通过 | 不用单元测试数量代替端到端评测 |
| 端到端任务评测 | OpenCompass、每题一次生成、全数据集一轮、`temperature=0`；AIME26 30/30，与团队 8 卡 H100 对照准确率一致 | 使用 `gpt-6-astra` 作 LLM-as-judge 检查数学等价性；这是任务正确率对照，不是逐 Token／logits 对齐 |
| 生产交付 | 截至 2026-11-02 已由云服务团队正式生产上线 | 本人不掌握实际首次上线日期与业务场景；不推定线上运营和长期 SLA |

#### AIME26 评测口径

本人于 2026-11-02 确认：评测使用 OpenCompass，30 道题每题生成一次，整个数据集运行一轮，生成参数为 `temperature=0`。答案使用 LLM-as-judge 进行数学等价性检查，评估方为 `gpt-6-astra`，本次结果为 30/30。

“与官方一致”在本项目中具体指：团队在 8 卡 H100 的 CUDA 环境运行 GLM-5.3-Flash，同样得到 AIME26 30/30，两个平台的该项准确率一致。模型及量化 revision、输出长度上限、OpenCompass 版本和 judge 配置尚未补录，不由准确率相同推断逐 Token 或 logits 一致，也不扩张为其他评测集的结论。

#### 最终单请求性能

本人于 2026-11-02 确认以下同一组最终性能的测量条件与结果：

| 测量条件 | 已确认内容 |
|---|---|
| 并发 | 单请求，并发为 1 |
| 输入／输出长度 | 输入 128 token，输出 128 token |
| Graph | 开启 |
| replay cache | 开启 |
| 预热 | 0 次 |
| 正式测量与汇总 | 正式测量 3 次，三次取平均；下表保留本人提供的指标名称和统计口径 |

| 指标 | 统计口径 | 结果 |
|---|---|---:|
| 输出吞吐 | 平均值 | 17.12 tokens/s |
| 首 token 延迟（TTFT） | p50 | 243.89 ms |
| TPOT | p50 | 58.39 ms/token |

本组 TPOT p50 为 58.39 ms，低于性能目标中的 70 ms。引用时保留上述负载、测量方法与 p50 口径，不将其表述为每一个 token 间隔均低于 70 ms，也不将平均吞吐与 TPOT p50 互相换算。

#### 分阶段性能

| 阶段／测例 | 结果 | 计量边界 |
|---|---|---|
| 状态拆池对照 | prefill 约 179 s → 5.7 s；decode 约 120 s → 2.6 s | 相同短 prompt、插件插桩、Host 单步耗时 |
| 2026-10-10 服务基线 | 约 233 ms/token | 1,223-token prompt、无 profiler、eager；不能与其他输入的后续结果直接计算加速比 |
| 2026-10-22 干净 decode | 约 96.9 ms/token；p50 96.35 ms、p90 102.91 ms | 单请求、64 output、无 profiler／Kernel log；prompt 等完整配置待补 |
| 发布 smoke | 20 prompt／32 output 的单请求约 2.107 s；8 并发合计 256 output 用时 3.751 s，约 68.24 output tok/s | 单请求总时间与并发聚合输出吞吐分别记录，不能当成纯 decode 的倒数 |
| Profile 流水线 | profiled decode 步长 602.6 ms → 140.6 ms | 带 Profile 的执行路径对照；不能与干净服务数据混算 |

#### Graph 对照

| prompt／output | 并发 | Graph gap p50 | Eager gap p50 | Graph 吞吐 | Eager 吞吐 |
|---|---:|---:|---:|---:|---:|
| 49／96 tokens | 1 | 67.64 ms | 110.27 ms | 14.11 tok/s | 8.83 tok/s |
| 49／96 tokens | 8 | 103.49 ms | 112.86 ms | 65.38 tok/s | 59.95 tok/s |
| 49／64 tokens | 32 | 222.04 ms | 222.88 ms | 100.08 tok/s | 100.55 tok/s |
| 49／64 tokens | 64 | 277.89 ms | 263.59 ms | 92.10 tok/s | 99.12 tok/s |

gap 与吞吐沿用总结中的两个独立测量指标，精确计时窗口、预热、重复次数和聚合方式待补。按表中数值计算，64 并发的 gap 增加约 5.4%，吞吐下降约 7.1%；总结中“约 -5%”不再笼统用于吞吐。总结将此轮退化关联到 38 个实际请求落入 40 槽 bucket 的 Padding 开销，仍需与运行日志和调度计数对应。

replay cache 的另一组三档单并发对照中，`gap_p50` 由 63.78／74.42／80.13 ms 降到 57.58／67.61／72.31 ms，TTFT 变化小于 1%。各档输入／输出长度尚未列入本档案，暂不把该组最低 gap 与前表吞吐或其他 decode 数据组成统一性能结论。

#### 容量与长上下文

| 口径 | 总结中的结果 | 使用边界 |
|---|---|---|
| 模型声明上下文 | 1,048,576 tokens | 模型配置上限，不是本平台已验证的服务能力 |
| 早期修复后容量 | 显存利用率 0.85 时，启动日志 148,762 tokens | 早期分配与核算修复结果，不直接与后续 block 表比较 |
| 后续生产配置容量推导 | 0.80 下报告 1,411 blocks；按 `B(L)` 推得单请求 171,776 tokens | 理论容量且没有余量，不等同该长度已满足生产时延要求 |
| 更高显存预算外推 | 0.95 下约 1,883–1,891 blocks、约 232K tokens | 线性外推，未作为生产配置验证 |
| 已验证长序列 | 131,072，eager、显存利用率 0.85 | 不扩张到 graph、相同长度多并发或 1M；常规验证配置为 4096 |

总结 §6.3 还提供了 KPool 优化后的单请求整模长上下文数字。先保留为报告结果，测量来源、配置及统计方法需要补齐：

| 单请求输入／上下文 | TTFT：原 native → 优化后 | Decode |
|---|---|---|
| 4K | 24.7 s → 15.4 s | 101–102 ms/token；9.8–9.9 tok/s |
| 16K | 97.2 s → 62.8 s | 106–109 ms/token；9.2–9.4 tok/s |
| 32K | 194.7 s → 134.3 s | 115–121 ms/token；8.3–8.7 tok/s |
| 131K | 约 797 s → 589.7 s | 总结未提供该行 decode 数据 |

### 已完成项与后续边界

- **已完成**：本次文本发布范围内的模型接入、混合缓存、融合链、decode graph、两个 NaN 根因处理、发布验证及云服务交付；AIME26 已有任务评测结果。
- **发布范围之外**：MTP、多模态、FP8、V2 runner、计算与通信重叠；不继续列为本次项目未完成项。
- **保留的技术取舍**：MoE router 使用 BF16 logits，可能影响临界专家选择；Graph 仅覆盖 uniform decode；更高并发可能因 bucket Padding 无收益；屏障等待仍有优化空间。
- **信息补录**：评测方法、H100 准确率对照、三处关键修改分工、验收目标及最终单请求的三项性能指标与测量条件已由本人确认；具体业务场景与首次上线日期按本人不掌握记录。后续按需补充可获得的历史对照配置、评测记录和发布标识。

### 面试深挖点

1. 混合缓存的分组、容量核算与实际分配怎样保持一致？两次 OOM 分别发生在哪一层，为什么两次修复不同？
2. 状态拆池为什么能同时影响 gather、scatter 和卷积？怎样用隔离实验区分布局开销与 Kernel 计算开销？
3. KPool 的逐 head 非线性与加权顺序为什么必须保留？算子接入怎样同时验证数值正确和真实路径命中？
4. Graph bucket 补齐输入后，metadata、状态槽和 buffer 生命周期为什么也要改变？什么条件下 graph 可能变慢？
5. NaN 的第一个出现位置如何帮助区分两个根因？低地址单测和 HTTP 200 为什么不足以证明模型正确？
6. 怎样解释 Host 单步、带 Profile 的步骤、token gap、TTFT 和端到端吞吐之间的差别？哪些收益属于本人插件改动，哪些属于算子协作？

### 口述基线（文稿已更新，待本人复述）

我负责将 GLM-5.3-Flash 接入 8 卡自研 AI 加速芯片的 vLLM 插件。它混合了线性注意力、稀疏 MLA、mHC 和 MoE，上游执行路径依赖目标平台无法直接使用的 Triton、TileLang 等能力。我负责插件内的模型、权重、缓存与执行接入，并提出融合算子需求，验收后接入；算子 Kernel 由算子团队实现。

最有代表性的问题是状态布局。conv state 和 recurrent state 放在同一页后形成非连续 view，目标后端退化为 Host 逐元素搬运。我通过 Profile 和隔离微基准定位后，将两种状态拆成连续池；相同短 prompt 下，prefill 和 decode 的 Host 单步耗时分别由约 179 秒、120 秒降到 5.7 秒、2.6 秒。

后续我继续合并 metadata 拷贝、减少阻塞读回，接入融合路径并完成 decode graph 的 metadata 与 Padding 适配。最终在单请求、输入与输出均为 128 token、Graph 和 replay cache 均开启的条件下，预热 0 次，正式测量 3 次后取平均：输出吞吐为 17.12 tokens/s，TTFT p50 为 243.89 ms，TPOT p50 为 58.39 ms，低于性能目标中的 70 ms。发布前我定位了 KDA 高地址换算回绕，由算子同事修改代码，我负责验收；warmup 污染 null block 的问题则由我完成定位、代码修复和验收。

项目开发与交付在 2026-10-27 完成，截至 2026-11-02 已由云服务团队正式生产上线。AIME26 使用 OpenCompass，每题生成一次、运行一轮、`temperature=0`，由 `gpt-6-astra` 检查答案的数学等价性，结果为 30/30，与团队在 8 卡 H100 上运行同一模型的准确率一致。当前交付范围为文本、AWQ 权重、BF16 激活、V1 runner 和 decode graph，MTP、多模态等扩展不包含在这次发布中。

### 待补充与待核验字段

| 优先项 | 仍需补充的信息 | 用途 |
|---|---|---|
| AIME26 评测记录 | 模型及量化 revision、OpenCompass 版本、输出长度上限、judge 配置与结果记录位置；本次问答已确认的生成次数、temperature、判分方式和 H100 对照不再列为缺项 | 固化单轮 30/30 的任务评测配置，不替代 logits 或逐 Token 数值对齐 |
| 发布记录 | 可获得的发布版本脱敏标识及实际生产配置；业务场景与首次上线日期本人不掌握，不再列为待补答项 | 固化发布基线；验收目标已明确 |
| 证据定位与表达 | 总结证据索引中的评测、Graph、NaN 和发布报告的可引用编号；本人复述后的事实与措辞修订 | 将当前材料用于后续简历和面试，不要求披露内部代码或路径 |
