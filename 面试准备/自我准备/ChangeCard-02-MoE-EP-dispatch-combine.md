<a id="change-card-02-moe-ep"></a>

# Change Card 02：Fused MoE 到 EP dispatch/combine（问答成稿）

> 写法：按[八周计划 §4.3](../../计划/高级AI框架开发工程师-八周证据冲刺计划.md#43-change-card-模板)的九段骨架问答共建：导师逐段提问并给出选项，学习者选择、补充并提供芯片信息，导师据此成稿（[练习约定](../../计划/八周冲刺进度/历史记录/W2-学习验收记录.md#w2-u2-o4-practice-contract)）。
> 证据等级：B 级。框架源码以 vLLM `d7ada3a` 为准；各通信库的对照见[课程网页·综合横向对照表](../../课程网页/八周计划/plana-jd-w2-moe-ep-source.html#comparison)。芯片信息只记录可公开的抽象能力，具体型号与底层接口不写入。

## 1. 固定仓库 / commit / 文件 / 类 / 函数

vLLM `d7ada3aace`，路径相对 `vllm/` 包目录。参照已接入的 MoRI 后端（`mori_high_throughput`、`mori_low_latency`），新通信库记作 `<lib>`。本卡源码基线与团队实际版本的关系见第 9 段。

| 项 | 改动 | 位置 | 参照（`d7ada3a`） |
|---|---|---|---|
| A | 新增后端名，`--all2all-backend` 才能选到 | `config/parallel.py` 的 `All2AllBackend` | MoRI 的两个取值，`:51-52` |
| A′ | 新增 MoE 开关，工厂分支与 Experts 都读它 | `model_executor/layers/fused_moe/config.py`：`FusedMoEParallelConfig.use_<lib>_kernels`，以及 `FusedMoEConfig` 的同名转发 | `use_mori_kernels`，`:1087`、`:1556` |
| B | 新增 All2AllManager：创建通信库对象并按参数缓存，经 `get_handle(args)` 交出 | `distributed/device_communicators/all2all.py`；由设备通信器按后端名创建 | `MoriAll2AllManager`，`all2all.py:995`。CUDA/ROCm 的创建分支在 `cuda_communicator.py:203-274`；新平台由 `get_device_communicator_cls()`（`platforms/interface.py:1220`）指向自己的通信器，在那里创建 |
| C | 新增 P/F 子类：prepare 做量化与 dispatch，finalize 做 combine 并写回 `output` | `model_executor/layers/fused_moe/prepare_finalize/<lib>.py`，继承 `FusedMoEPrepareAndFinalizeModular` | `MoriPrepareAndFinalize`，`mori.py:15` |
| D | 工厂加分支：按量化配置定 dispatch 的 dtype 与 scale 尺寸，从 manager 取通信对象，构造 P/F | `model_executor/layers/fused_moe/all2all_utils.py` 的 `maybe_make_prepare_finalize`（`:182`）；各量化 oracle（`fused_moe/oracle/*.py`）都调用它 | MoRI 分支，`:329-386` |
| 视情况 | 输出是专家优先布局时，加入 batched 开关 | `fused_moe/config.py:1066` 的 `use_batched_activation_format` | oracle 在造 P/F 之前就按它挑 Experts（`oracle/unquantized.py:253-261`）；组装时断言两侧 `activation_format` 一致（`modular_kernel.py:1739-1747`）。这是 CUDA／ROCm 的路径；OOT 平台的未量化 oracle 不读它，见第 4 段 |
| 视情况 | 能接受序列并行切分的输入时，加入 SP 白名单 | `config/parallel.py:768` 的 `use_sequence_parallel_moe` | 白名单含 MoRI 的两个取值 |
| 视情况 | Experts 一侧配合：约定谁来量化、输入宽度；布局或元数据不被现有 Experts 支持时，才新写 Experts | `fused_moe/experts/` 与对应 oracle | AITER Experts 按 `use_mori_kernels` 决定是否自己量化（`experts/rocm_aiter_moe.py:484-490`）和 FP4 打包后的输入宽度（`:553-558`）；MoonEP 的 `[NvS, H]` 加 `cu_seqlens` 布局声明为 Standard，仍由 oracle 直接配专用的 `MoonEPExperts`（`oracle/unquantized.py:298-303`） |
| 不改 | MoE 层、MoE runner、模型 forward | `fused_moe/layer.py`、`fused_moe/runner/`、`models/` | 经 `FusedMoEKernel` 调用 P/F 与 Experts，并读取 `output_is_reduced()` 等性质（`runner/moe_runner.py:423-427`） |

上表展示一般接入位置；本卡首版正确性与性能方案采用未量化路径，量化相关位置只保留作后续接入参考。

“不改”的边界：runner 和个别模型里有按后端名写的名单或分支，新后端会落进保守或默认分支。功能上不必改，默认分支是否适用留到第 7 段验证。

- EPLB 开启时，只有白名单后端保留共享专家与路由专家的重叠，源码注释给出的理由是正确性问题（`runner/shared_experts.py:79-99`）。
- DeepSeek V3.2 的 AMD 路径只对 MoRI 改了 combine 之后的 TP 归约，其余后端走 `skip_final_all_reduce`（`models/deepseek_v32/amd/model.py:88-94`）；DeepSeek V4 的 AITER MegaMoE 只接受 MoRI（`models/deepseek_v4/amd/model.py:570-577`）。

> 本段问答（2026-10-28 第 1 轮）：学习者选 A–D；判断 E 不需要，理由是模型经 MoE runner 按配置调用通信库；F 不是必须，取决于输出布局是否被 Standard 或 BatchedExperts 两类 Experts 支持。六项判断均与源码一致。导师补充了 A′、三项“视情况”改动和“不改”的边界。

## 2. 现有职责、输入输出和调用契约

契约以 `FusedMoEPrepareAndFinalizeModular`（`model_executor/layers/fused_moe/modular_kernel.py:281`）为准。`FusedMoEKernel` 在初始化时组装一个 P/F 和一个 Experts，前向依次调用 prepare、Experts、finalize。

**prepare**：输入本卡 M 个 token 的激活 `a1 [M,H]`、路由 `topk_ids/topk_weights [M,K]`（全局专家 id）、`expert_map`、`apply_router_weight_on_input`、量化配置与 `defer_input_quant`；返回五元组（`:157-163`）。`apply_router_weight_on_input` 决定是否已经在专家计算之前施加路由权重，必须与 finalize 的加权责任一起处理，不能因采用未量化路径就忽略。

| 返回项 | 何时必填 | 作用与参照 |
|---|---|---|
| dispatch 后的激活 `a1q` | 总是 | Experts 的主输入 |
| `a1q_scale` | 已量化时 | 与 `a1q` 配套的 scale |
| `ExpertTokensMetadata` | 专家优先布局 | 行所在的槽位已说明是哪个专家，计数说明每槽几行有效：`BatchedTritonExperts` 断言它非空（`experts/fused_batched_moe.py:923`；`:672-674` 是 `NaiveBatchedExperts` 的对应检查），DeepEP LL 填每个本地专家的行数（`prepare_finalize/deepep_ll.py:334-338`）。Token 优先布局下可选：Triton Experts 不读它；MoRI 填的是收到的总行数，AITER 当作有效行数用（`mori.py:121-123`、`experts/rocm_aiter_moe.py:583-586`） |
| dispatch 后的 topk ids／weights | Token 行集合／顺序改变且后续仍需逐行路由时 | 每行要经过哪几个本卡专家靠 ids 判断，weights 供卡内加权。返回非 None 时 kernel 用它们替换原路由，否则沿用原值（`modular_kernel.py:1293-1297`）；Standard 布局的 NoDPEP 就可返回 None（`prepare_finalize/no_dp_ep.py:84`），不能仅凭布局判为必填。DeepEP HT 把库给的本地 id 转回全局 id，-1 改成别卡的专家（`deepep_ht.py:236-252`、`:280-286`）。DeepEP LL 的专家优先布局返回 None（`deepep_ll.py:338`） |

不在返回值里：

- 送回所需的第二类路由信息（来源卡、原位置）留在 P/F 对象或通信库里：DeepEP LL 按微批次存 `self.handles[ubatch]`（`deepep_ll.py:382-385`）；MoRI 由 op 内部保存，P/F 另存 dispatch 前的 `topk_ids`（`mori.py:107-111`）。
- 最终输出 `output` 由 kernel 分配（`modular_kernel.py:1514`），交给 finalize 就地写。P/F 能选择性提供的是另一块缓冲区，即 Experts 的输出：钩子 `allocate_fused_expert_output`（`:203`，调用处 `:1152`）。AgRs 在 Experts 已自行加权求和时，把 combine 的输入缓冲区交给 Experts 直接写（`naive_dp_ep.py:134-143`）。

**finalize**：输入 `output [M,H]`、Experts 输出、`topk_weights/topk_ids`（可能已被替换）、`apply_router_weight_on_input` 与 Experts 指定的 `weight_and_reduce_impl`；不返回值，结果就地写进 `output`（`modular_kernel.py:375-396`）。

- `output_is_reduced()` 只声明 finalize 的输出是否已经完成所需的跨 rank 归约（`modular_kernel.py:249-252`），不是“是否已做 top-k 加权／求和”的标志。为 False 时是否还要 all-reduce，由并行配置与 runner／模型路径决定：默认 late reduction 仅在非 SP、未启用 `skip_final_all_reduce`、TP 或 EP 大于 1 且结果尚未归约时执行（`runner/moe_runner.py:498-515`）。例如 NoDPEP 在单 rank 下返回 False，结果仍可完整且无需 all-reduce；新 P/F 必须按实际跨 rank 语义声明该值。
- 加权由谁做，看 Experts 的 `finalize_weight_and_reduce_impl()`（`modular_kernel.py:1427-1434`）：
  - Triton、AITER 返回 NoOP，表示 Experts 已在卡内对每行加权求和（`triton_moe.py:195-196`、`rocm_aiter_moe.py:536-537`）。MoRI 搭配 AITER，combine 不再传权重，结果从 op 的缓冲区复制进 `output`（`mori.py:147-152`）。
  - 返回 Delegate 的 Experts（例如 `BatchedTritonExperts`，`fused_batched_moe.py:861-863`）把决定交给 P/F：DeepEP HT 遇到 Delegate 时在 finalize 里改用 Contiguous，先加权再 combine（`deepep_ht.py:386-388`）；DeepEP LL 只接受 Delegate（`deepep_ll.py:378-400`）。但 Delegate 不表示权重此前一定未使用：DeepEP LL 在 `apply_router_weight_on_input=True` 时要求 top-k=1，prepare 先乘权重（`:278-284`），finalize 改传全 1（`:387-390`），避免再次加权。目标后端若不支持这种输入加权语义，应显式拒绝该配置，不能无条件把原权重交给 combine；本卡尚未确认该分支支持情况。

**其他声明**（`modular_kernel.py:217-277`）：`activation_format`、`topk_indices_dtype`（MoRI 要求 int32）、`max_num_tokens_per_rank`、`num_dispatchers`、`supports_async`、`supports_dbo`。不支持异步的 P/F，在 prepare 与 finalize 处断言 DBO 关闭或 `supports_dbo()` 为真（`:1236`、`:1425`）。

> 本段问答（2026-10-28 第 2 轮）：题 1 学习者认为 A 必需；B 必需，用来区分各行由哪个专家计算；C 可选，取决于 Experts 是否在卡内加权求和；D 不需要，因为 Experts 不需要原位置；E 可选，可由 Experts 或 prepare 分配。D 的判断与理由正确。B、C 的作用在 Token 优先布局下说反了：区分行与专家靠 C，B 只在专家优先布局里必需。E 不在 prepare 的返回值里；学习者描述的“由 Experts 或 P/F 分配”对应的是 Experts 的输出缓冲区。题 2 选 B、题 3 选 A，理由均正确。

## 3. 目标后端能力或缺口

芯片能力由学习者提供（2026-10-28；两段式通信、图模式与 combine 跳过加权的能力于 2026-10-29 补充确认），只记抽象能力。“对接入的推论”是导师按第 1、2 段的源码契约推出的设计含义，未经硬件验证。

| 方面 | 学习者提供的能力 | 对接入的推论 |
|---|---|---|
| dispatch 输出布局 | 专家优先：按本卡专家分槽，附每槽有效行数 | P/F 声明 `BatchedExperts`；prepare 返回激活与 scale、每个本地专家的行数，ids／weights 返回 None，finalize 因此收到原 `[M,K]` 路由；`max_num_tokens_per_rank()` 必须给出，批量 Experts 按它定尺寸（`oracle/unquantized.py:534-535`）。在 CUDA／ROCm 上，后端名还要加入 `use_batched_activation_format`（`fused_moe/config.py:1066`），oracle 才会挑批量 Experts；OOT 平台的未量化 oracle 不读它，见第 4 段 |
| 节点内传输 | 卡间可直接读写对端显存（学习者称节点内有 RDMA 能力） | — |
| 搬运者与两段式通信 | 节点内外的数据都由计算核心之外的引擎（DMA、网卡）搬运；学习者于 2026-10-29 与同事讨论后确认，芯片通信支持拆成“发起传输”和“确认接收完成”两段 | 分段能力允许在两段之间安排不依赖接收结果的计算，可参照 DeepEP LL 的 recv hook（vLLM 在 DBO 或异步时启用，`deepep_ll.py:383`）设计接入。完成依赖与缓冲区生命周期见第 5 段，具体异步 P/F 接入列第 9 段待验证；能否实际重叠及收益在第 8 段列验证方法。能力确认不等于已完成框架接入或性能验证 |
| 跨节点传输与发送量 | 只能由主机端发起：先交换每个专家的实际行数，主机拿到计数后按实际大小发送，中间有一次设备到主机的同步。节点内的传输不经主机 | 多节点部署时，每层 dispatch 都要等一次计数拷回，主机不能提前排后续 kernel；单节点部署没有这次同步。这就是节点 5 的“设备计数 → 拷回同步 → 精确分配”，只是槽位仍按上限固定，变的是发送量。多节点时主机端已有各专家的行数，可像 DeepEP HT 那样一并填进 `ExpertTokensMetadata` 的 CPU 计数（`deepep_ht.py:255-260`、`modular_kernel.py:110-123`）；单节点时要填，就得另加一次同步 |
| 图模式 | 学习者于 2026-10-29 确认：dispatch／combine 在单节点内支持图模式，跨节点不支持 | 平台适配应按实际部署是否跨节点区分：单节点可接入芯片图模式，跨节点选到本通信后端时关闭。现有跨节点路径包含设备计数拷回和主机按实际行数发起传输，不能把单节点支持外推到跨节点。vLLM 对 DeepEP HT 的关图规则（`config/compilation.py:1242-1258`）可作对照，但该规则按 DP>1 判断，不等同于本芯片的节点边界；具体配置与回归在第 6、7 段确定。此处记录用户确认的能力，不记为本轮录图／重放实测 |
| 完成语义 | 通信可放在独立的流上，并返回 event 供计算流等待 | — |
| 执行模型 | 同一时刻只运行一个 kernel、一个流；多个流由驱动切换着交替执行，通信 kernel 与计算 kernel 不能并行。惯常做法是全部放在同一个流上，避免切流开销；业务以单 batch 为主，几乎不用 micro-batch（2026-10-29 补充） | 当前串行基线按同步 P/F、`supports_async()` 与 `supports_dbo()` 返回 False、关闭 DBO 处理（`modular_kernel.py:1236`、`:1425`），共享专家也不走 kernel 内重叠（`:1714-1718`）。不能仅由单 kernel 执行推导出通信无法分段。非 CUDA 类平台不创建辅助流（`utils/torch_utils.py:860-869`），共享专家按顺序执行（`runner/shared_experts.py:101-122`）；第 8 段另设计“两段式通信＋共享专家计算”候选对照，具体异步 P/F 接入仍待验证。micro-batch／DBO 不作为本卡主要性能方案 |
| dispatch 精度 | 不支持低精度数据加 scale | 首版正确性与性能验证均采用未量化路径。后续启用量化时，可把量化挪到接收之后：prepare 自己量化，参照 DeepEP LL（`deepep_ll.py:203-214`）与 HT（`deepep_ht.py:262-278`）；或交给 `expects_unquantized_inputs` 为真的 Experts，`defer_input_quant` 取自它（`modular_kernel.py:535`、`:1252`）。具体 dtype、scale、通信字节与误差另行验证，不作为本版已实现能力 |
| combine 加权 | combine 可接收 topk 权重，在通信中完成加权求和；学习者于 2026-10-29 确认，也支持跳过加权，只做回传与求和 | 在 `apply_router_weight_on_input=False` 且 Experts 未加权、返回 Delegate 的分支，finalize 把原 `[M,K]` 权重交给 combine；若 Experts 已加权（返回 NoOP），则关闭 combine 加权。输入加权模式必须另按第 2 段处理或显式拒绝，不能由 Delegate 推断原权重仍应再乘。两侧布局、路由与归约契约仍须匹配，当前草案的 Experts 选择不因此自动改变 |
| 接收缓冲区 | 由库预先分配、反复使用；dispatch 返回新分配的输出张量，数据先在库缓冲区里整理成每个专家一段连续区再拷入，不是视图（第 5 轮学习者核对后更正）；固定容量、combine 输出归属及双缓冲见第 5 段 | 同 DeepEP LL：库缓冲区只在构造时分配一次（DeepEP `d4f41e4`，`csrc/legacy/buffer.hpp:268`），`packed_recv_x` 每次调用新建（`:1516`），接收阶段把各来源块的有效行集中到该专家那段的开头（`csrc/kernels/legacy/internode_ll.cu:408`、`:432-436`）。dispatch 接收与拷贝完成后，Experts 使用独立输出张量，不再读取内部接收区；代价是一次设备内拷贝和一块输出张量的显存，内部区何时可复用仍受通信顺序约束。MoRI 不同：返回句柄所持缓冲区上的视图（MoRI `2d4c3e2`，`python/mori/ops/dispatch_combine.py:992-997`、`:1361-1397`），vLLM 的 MoRI P/F 把视图原样交给 Experts（`mori.py:113-131`） |

> 本段问答（2026-10-28 第 3 轮）：学习者选专家优先布局，并指出 prepare 必须返回激活与 scale、每个专家的有效行数，没有列 ids／weights，判断正确；第 2 段 B、C 的混淆在这道迁移题中已纠正。传输、完成语义与执行模型均由学习者提供。
>
> 第 4 轮（2026-10-28）：学习者确认数据由计算核心之外的引擎搬运；跨节点先交换计数，主机按实际大小发送，中间有一次设备到主机同步；没在跨节点场景开过图模式，估计不能；dispatch 不支持低精度加 scale；combine 接收 topk 权重，在通信中加权求和；接收缓冲区归库所有，返回视图，下次调用覆盖（第 5 轮已更正，见下）。以上均为芯片事实；对图模式的估计与节点 5 的结论（只有按最坏情况分配才能进 CUDA graph）一致。学习者追问的“发出 → 算别的 → 确认收到”即 DeepEP LL 的 recv hook，已在对话中按 DeepEP `d4f41e4` 解释。
>
> 2026-10-29 审稿更正：“只有按最坏情况分配才能进 CUDA graph”是导师当时的过强结论。固定容量只是避免按本轮设备计数做主机分配的一种方法，既非一般必要条件，也不能单独保证可录图；缓存已知布局也可绕过该主机计数等待（DeepEP `d4f41e4`，`csrc/legacy/buffer.hpp:532-539`、`:571-598`）。这条窄事实不等于完整 HT 路径已经支持图模式；具体路径仍需满足主机依赖、地址／形状和通信实现的约束。
>
> 第 5 轮（2026-10-28）：学习者核对后更正两点：dispatch 返回的是新分配、整理成连续布局的输出张量，不是库缓冲区上的视图；只有跨节点用到主机，节点内不经主机。“跨节点传输与发送量”“图模式”“接收缓冲区”三行已按此改写。导师在对话中曾推断“主机按计数算出起点、直接写成连续布局，省掉整理”，与更正不符，已撤回。
>
> 第 6 轮（2026-10-29）：学习者选择 A，并确认已与同事讨论，芯片通信能力支持分成两段。该能力从未决项移入上表；未据此声称已实现 vLLM 异步接入、支持 DBO 或取得重叠收益。导师同时收窄“执行模型”行：关闭异步与 DBO 是当前草案的保守选择，不能从单 kernel 执行直接推导为硬件不支持两段式通信。
>
> 第 7 轮（2026-10-29）：学习者确认单节点内支持图模式、跨节点不支持，combine 支持跳过加权、只做回传与求和。本段原列的三项能力未决信息均已得到用户确认；同步改正“只能配 Delegate”的原推论，并把第 4 段关图条件收敛为跨节点部署。上述确认不作为本轮设备运行或框架接入证据。

## 4. 保持不变 / adapter / framework core patch / 替换

路线：留在 modular kernel 内。P/F 管通信，新写的 Experts 包装自有 grouped GEMM 算子，两侧按 `activation_format` 配对，组装时断言一致（`modular_kernel.py:1739-1747`）。团队做法由学习者提供：改动全部放在平台插件里，平台接口能覆盖的照常实现，必须改 vLLM 原代码的在插件里打 patch。下表的“归类”按 `d7ada3a` 判断。

| 改动 | 归类（`d7ada3a`） | 团队做法 | 依据 |
|---|---|---|---|
| 新后端名（第 1 段 A） | 由平台写入时是 adapter；要让 `--all2all-backend` 直接选到，才是 core patch | 插件内，不打 patch | `All2AllBackend` 是 Literal，构造 `ParallelConfig` 和生成命令行 choices 时都按它校验（`config/parallel.py:45-60`、`engine/arg_utils.py:1141-1145`）。`@config` 只设了 `extra="forbid"`，赋值不校验（`config/utils.py:71`），所以平台可以在 `check_and_update_config` 里按 `additional_config`（`config/vllm.py:425-428`）写入新名字 |
| P/F 子类（C） | adapter | 插件内 | 继承 `FusedMoEPrepareAndFinalizeModular` 的新类 |
| All2AllManager（B） | adapter | 插件内 | 平台通信器由 `get_device_communicator_cls()`（`platforms/interface.py:1220`）指定，在其中创建 |
| 跨节点部署关闭图模式 | adapter | 插件内 | 平台的 `check_and_update_config` 在 `config/vllm.py:2040` 调用，早于 DeepEP HT 的关图规则（`:2134` → `config/compilation.py:1242-1258`）。按第 3 段已确认的能力，选到本后端且实际跨节点时关闭；单节点接入平台支持的图模式，具体配置与验证在第 6、7 段确定 |
| 工厂分支（D）与 `use_<lib>_kernels`（A′） | 经 all-to-all 工厂分支组装时是 core patch | 插件内 patch | 仅在已进入 all-to-all 分支后，新名字未命中后端分支才返回 None（`all2all_utils.py:228`、`:453`），未量化 oracle 随后断言失败（`oracle/unquantized.py:527`）。若 `use_all2all_kernels=False`，工厂可能提前选 naive DP／EP 或 NoDPEP（`all2all_utils.py:195-223`），不能靠后端名字推断实际路径。在自有 MoE 方法里直接构造 P/F 和 `FusedMoEKernel` 可绕过工厂，但仍须匹配实际并行布局与通信组；其他工厂调用者包括各量化 oracle 和弹性 EP 重配（`eep_reconfigure.py:92`） |
| batched 开关（第 1 段“视情况”） | CUDA／ROCm 上是 core patch；OOT 平台的未量化路径不读它 | 插件内 patch | 读者是各 oracle 挑 Experts（`oracle/unquantized.py:258` 等）和弹性 EP 重配（`eep_reconfigure.py:73-75`）。OOT 平台的未量化 oracle 在读它之前就返回（`:231-232`）；`make_unquantized_moe_kernel` 构造 Experts 时看的是 P/F 的 `activation_format`（`:533-546`） |
| 自有 MoE 方法 | 替换，用 vLLM 给 OOT 平台留的注册点 | 未说明 | OOT 平台的未量化 oracle 返回 `(OOT, None)`，不挑 Experts（`oracle/unquantized.py:231-232`）；权重处理遇到 OOT 直接返回（`unquantized_fused_moe_method.py:227-232`）；默认的 `forward_oot` 转到 `forward_native`（`custom_op.py:167-170`），后者断言 kernel 已建好（`unquantized_fused_moe_method.py:303`）。所以平台要用 `@UnquantizedFusedMoEMethod.register_oot` 注册子类（`custom_op.py:326-340`），在其中组装 kernel。这就是新 Experts 的落点 |
| 新 Experts 类 | adapter | 插件内新写，复用自有算子 | 声明批量格式，构造参数接收 `max_num_tokens`、`num_dispatchers`（`oracle/unquantized.py:533-546`）；按第 3 段返回 Delegate；读设备端每个专家的行数，跳过空槽（参照 `experts/fused_batched_moe.py:345-363`） |
| 保持不变 | — | — | MoE 层、MoE runner、模型 forward、`FusedMoEKernel` 本身（第 1 段“不改”） |

**首版并行配置**：用户于审稿时确认 `TP=8、DP=4、EP 开启、SP 关闭`。本基线的 `use_all2all_kernels = use_ep and (dp_size > 1 or pcp_size > 1 or is_sequence_parallel)`（`fused_moe/config.py:1034-1038`），本配置由 `DP>1` 满足触发条件；不能推广成仅选择后端名即可触发所有组合。

PCP 未单独给出：以下以未开启 PCP（size=1）且沿用公开框架通信组构造为条件。原生 vLLM 在 EP 下将 TP×DP×PCP 的设备范围用于专家分布，MoE 配置中的专家 TP 变为 1，因此这里的 EP／dispatch 组为 32 ranks，而不是只取 DP 的 4；配置层面的 TP=8 仍用于相应非专家路径。该规则在 `d7ada3a` 的 `fused_moe/config.py:1106-1114`、`:1226-1244` 与 `v0.30.0` 的同文件 `:1121-1129`、`:1240-1258` 一致。若团队插件另行划分通信组，应以实际 manager 的 world size 核验，不能直接套用 32。

**OOT 子类的责任**：注册子类只是替换实现入口；子类仍需按目标设备完成权重处理，建立 `moe_quant_config`、P/F、Experts 与 kernel。默认 OOT 权重分支提前返回（`unquantized_fused_moe_method.py:227-232`），不会自动替插件完成这些工作；预处理权重路径也必须被插件正确接管，避免落到要求 `experts_cls` 非空的默认 `_init_moe_kernel`（`:200-218`）。

“团队做法”与“归类”有两处出入：第 1 项学习者归为插件内，按 `d7ada3a` 成立的前提是由平台写入，代价是命令行选不到；第 3、6 项团队打了 patch，按 `d7ada3a`，在 OOT 平台的自有 MoE 方法里自建 kernel 时可以不改。团队版本已由用户提供，见第 9 段；具体接口差异与团队 patch 尚未逐项核对，不能把这些出入直接归因为版本差异。

> 本段问答（2026-10-28 第 5 轮）：学习者选路线 A，理由是便于复用已有的专家计算 kernel；题 2 把 1、2、4、5 归为平台插件内正常实现，3、6 要在插件里 patch；题 3 选 B，用自有算子库并新写 Experts 类。2、3、4、5、6 的归类与源码一致；1 在“由平台写入”的前提下成立，导师预期的“改 Literal”只在要让命令行直接选到时才需要。导师补充了 OOT 平台上 Experts 的落点（注册自有 MoE 方法），以及按此组装时 3、6 可以不改。

## 5. buffer / stream / device / ownership / lifetime

先区分库内部的通信缓冲区与交给后续计算的张量。记本卡专家数为 `E`、每专家预设容量上限为 `C`、隐藏维度为 `H`，本卡原有 Token 数为 `M`。

| 对象 | 已确认的分配与归属 | 接入含义 |
|---|---|---|
| dispatch 输出 | 按用户确认的普通接口调用语义，每次新分配，按预设每专家容量分配，形状为 `[E,C,H]`；每轮有效行数单独给出 | 完成接收与拷贝后，Experts 读取独立输出；该张量仍须保留到最后一个消费者完成。图重放不会重新执行普通主机分配，跨 replay 的输出有效期另行约束，不能套用“每次新对象” |
| combine 输出 | 调用方提供输出张量，库直接写入 | P/F 把 vLLM 提供的 `[M,H]` `output` 交给库，finalize 无需再把库结果复制到 `output`。用户指出的参照已核对：vLLM `d7ada3a` 的 `prepare_finalize/deepep_ll.py:395-403` 使用 `out=output`；该调用同时是 `zero_copy=False`，所以直接写最终输出不等于整个通信过程无拷贝 |
| 库内部通信缓冲区 | 由库持有两份并轮换使用，相邻两次调用写不同的一份；调用方负责安排接收阶段，通过同流顺序或跨流 event 建立下一次调用前的复用依赖（2026-10-29 用户确认） | P/F 需把本次接收阶段及必要等待排在后续复用之前，不能只靠槽位轮换，也不能把 CPU 调用返回当成 GPU 完成。这里确认的是调用方责任；本芯片底层跨 rank 信号协议没有据此认定与 DeepEP 相同 |
| 完成 event | 消费流等待 event 后，dispatch 的接收／整理输出或 combine 的最终 `output` 已可读（2026-10-29 用户确认） | event 覆盖到输出可读，不能仅以发送已提交代替；同流保持顺序，跨流由消费者等待对应完成 event |
| 逆向路由 handle | 普通 dispatch 调用返回独立 handle，由调用方保留到该次 combine 完成（2026-10-29 用户确认） | P/F 将 handle 与对应调用配对；保持 handle 有效直到 combine 在设备上完成，不在 CPU 提交返回时提前释放或错配。图重放可能复用捕获时的 handle 对象与张量存储，必须验证其中动态路由数据随本轮更新 |

本段采用的依赖关系：dispatch 接收与整理完成 → Experts 读取独立输出 → Experts 结果就绪 → combine 回传并写入 `output` → 后续算子读取。内部通信区按已建立的跨调用依赖轮换复用；handle 保留至对应 combine 完成。独立 handle 解决调用间路由归属，不自动解除内部双缓冲的顺序约束。

**容量映射**：记每个发送 rank 的 Token 上限为 `T`、实际 dispatch 通信组大小为 `D`；用户确认采用 `C = T × D`。P/F 的 `max_num_tokens_per_rank()` 提供 `T`，`num_dispatchers()` 提供 `D`，Experts 据此分配 `[E,T×D,H]` 的容量，与库 `[E,C,H]` 对齐（`experts/fused_batched_moe.py:876-885`）。不能把 `C` 再作为 `T` 传入并重复乘 `D`。按第 4 段未启用 PCP、未自定义拆组的条件，`D=32`，即 `C=32T`。

这个上限的安全前提是每个发送 rank 的有效 Token 行数不超过 `T`，且该 rank 内每个有效 Token 行至多分配给同一物理专家一次；于是任一专家最多接收各 rank 的 `T` 行之和。SP 关闭时，同一逻辑 Token 可能在多个 TP rank 上复制发送，这些副本仍计入各发送 rank 的 T；不能把 `D×T` 当作不同逻辑 Token 的数量，也不能未经去重核验就除以 TP=8。需要验证配置容量、实际调用上限和有效路由满足这些条件，不能只凭初始化时保存了 `C=T×D` 就认为所有运行输入均安全。

**图重放边界**：vLLM `d7ada3a` 的 CUDA graph wrapper 在捕获时保存输出，replay 返回保存的输出（`compilation/cuda_graph.py:319-337`、`:347-362`）；DeepEP 的主机 `buffer_idx ^= 1` 也不会在每次设备图重放时重新执行。图模式需要核对捕获的槽位／清理顺序、持久地址、动态计数／路由更新，以及前一次结果消费完再重用的依赖。这里是公开实现给出的核验要求，不据此断言本芯片图模式的具体实现或安全性。

DeepEP LL 对照（`d4f41e4`，导师源码核验）：

- `csrc/legacy/buffer.hpp:1504-1505`、`:1644-1645` 在 dispatch 和 combine 中共用索引，直接取当前槽并 `^= 1`，没有按忙闲搜索槽位。
- `csrc/kernels/legacy/internode_ll.cu:286-295`、`:329-338` 与 `:776-785`、`:915-930` 保证本轮完成信号发出前，下一槽的本地信号区已清零；RECV 等待本轮各对端的 count／flag（`:379-407`、`:947-976`）。配合调用者的跨轮 stream／hook 顺序，这条因果链允许相邻轮使用不同槽，而不是保证任意时刻都有一个全局空闲槽。
- `return_recv_hook=True` 只先排 SEND，hook 再排 RECV（`buffer.hpp:1577-1592`、`:1696-1711`）；仅在 CPU 上拿到返回值或保存 hook 不构成完成。下一次 SEND 会清另一槽的信号，因此不能把两份缓冲区当成允许任意积压两个未收尾调用的队列。
- dispatch 的 `packed_recv_x` 独立分配（`buffer.hpp:1516`），combine 使用传入 `out`（`:1655-1663`）。Python 文档“返回张量复用两份 buffer”的笼统警告与此处普通输出分配不一致，输出归属按该 commit 的实际实现裁决；显式取得内部发送区视图的 zero-copy 路径另论。

> 本段问答（2026-10-29 第 8 轮）：学习者选择 1A、2C，并主动定位 vLLM 的 `out=output` 调用；补充芯片库内部两份缓冲区轮换。上述三项按用户提供的能力成稿。学习者随后追问 DeepEP LL 是否保证至少一份空闲；以上协议解释为导师核验，不记为学习者已经独立说明本芯片的复用保证。
>
> 第 9 轮（2026-10-29）：学习者确认选 A：调用方负责排好接收阶段，通过同流顺序或跨流 event 建立复用依赖。该责任已写入内部通信缓冲区一行；event 的完成范围和逆向路由元数据的生命周期仍待问答。
>
> 第 10 轮（2026-10-29）：学习者确认 1A、2A：等待完成 event 后输出已可读；dispatch 返回独立 handle，由调用方保留到 combine 完成。第 5 段的分配、归属与完成边界据此成稿；芯片底层协议和真实并发运行仍不作为已验证证据。

## 6. fallback、兼容性和错误传播

**初始化与兼容性策略**：本版不设计备用通信路径。库不可用，或配置经过既定适配后仍不满足支持条件，初始化时明确报错，说明未满足的条件，不静默切换其他通信后端。兼容性检查围绕前文已经选定的布局、容量、精度与加权分工；跨节点关闭图模式沿用第 3、4 段的适配规则，不改变通信后端。

**运行时错误的现状**：学习者确认，通信中的超时、设备错误等可能表现为任务／进程卡住或失败，需要通过外部日志或超时检测发现。当前没有据此确认库能向 P/F 提供可靠的异常、状态码或设备错误标志，因此本卡不把“P/F 捕获异常后即可恢复”写成已有能力。

**故障后的最小处置方案**：通过调试工具查看并记录 Python 调用栈和芯片卡住时的执行状态，停止继续使用受影响的执行实例并上报。恢复方式和重试条件保留为第 9 段的待确认项，不承诺自动恢复或在原通信状态上立即重试。超时检测本身不作为旧通信已经取消或内部缓冲区已经安全释放的证据；本方案也尚未定义整个 EP 通信组的协调停止／重建流程。

> 本段问答（2026-10-29 第 11 轮）：学习者选择 1A、2C：本版不设计备用路径，不满足条件就初始化报错；运行时任务／进程可能卡住或失败，依赖外部日志或超时检测。初始化策略作为本卡选定方案，运行错误表现作为用户提供的现状记录；尚未声称具有自动恢复能力。
>
> 第 12 轮（2026-10-29）：学习者选择最小处置方案，并补充记录 Python 调用栈与芯片卡住时的执行状态，再停止继续使用受影响实例并上报；恢复方式和重试条件留待确认。第 6 段据此成稿，未实际执行故障注入、调试采集或恢复验证。

## 7. correctness 验证

**首版范围**：只设计未量化路径的验证，同时覆盖通信契约与完整单层 MoE；量化路径列为第 9 段的待验证项。以下为待执行的 B 级测试设计，不记为已有运行结果。

**两层参考**：先固定路由、给 Token／专家结果设置可辨认标记，独立核对 dispatch 的专家分组与有效行数、combine 的还原顺序和加权结果；再固定同一组输入、专家权重与路由，用逐专家参考计算对照完整单层 MoE 输出，覆盖 P/F 与 Experts 的接口配合。具体小样例、参考程序和断言由导师在实际获准执行时维护，本卡不要求学习者另写测试代码。

| 覆盖项 | 判定内容 |
|---|---|
| 基础路由与结果还原 | 逐项对应 Token、专家与来源 rank，核对有效分配计数、无丢失／重复及原 Token 顺序；使用非均匀路由权重，避免等权重掩盖错误 |
| 空专家与负载倾斜 | 空槽不作为有效输入处理；专家负载不均时计数、数据和结果仍对应同一条逻辑路由 |
| 容量边界 | 先核对 `T`、`D`、`C` 与 workspace 的映射。可在既定调度与路由约束下证明永不超限，或提供写入前的安全超限检测；仅初始化配置合法不能证明所有数据分布安全。覆盖上限及超限，不能越界、误读 padding 或静默截断；具体机制未确认前，不声称该配置已可安全运行 |
| 路由权重与归约 | Experts 未加权、combine 加权，与 Experts 已加权、combine 只求和两条路径对照；单独覆盖 `apply_router_weight_on_input`，不支持的分支应显式拒绝，支持的分支按模型语义验证不重复施权。区分 top-k 求和与跨 rank 归约，并核对 TP／EP／SP 配置下 `output_is_reduced()` 与后续归约路径一致 |
| 连续调用与异步依赖 | 连续至少三次调用覆盖内部槽位再次复用；改变每轮数据与路由，检查无旧数据污染、handle 配对正确。比较同流顺序与跨流 event 等待路径，在等待输出可读后再核对结果 |
| 已选图模式边界 | 单节点同一 graph 连续重放并改变输入、路由与专家有效行数，逐次与普通执行对照；覆盖零 Token rank、不等长 rank、图档位／padding 边界，核对输出、handle 数据和捕获缓冲地址的复用。跨节点按既定配置关闭图模式；新分配与主机槽位轮换的普通调用语义不直接外推到 replay |

计数、路由映射与输出顺序精确核对；浮点结果采用与参考计算的 dtype 和归约方式相符、执行前明确的误差准则，不要求所有路径逐位相等，也不事后放宽容差。当前未运行上述测试，具体数值容差尚未确定。

> 本段问答（2026-10-29 第 13 轮）：学习者选择 1B、2A：通信契约和完整单层 MoE 都做对照验证；首版先验证未量化路径，量化路径列为待验证。导师据此整理参考层次、边界覆盖与判定方法，未生成或执行验收测试。

## 8. 单芯片 / 多芯片 / 多节点性能验证

**范围与候选**：prefill 和 decode 两类都设计代表负载，沿用第 7 段的未量化路径。用户业务主要采用单 batch，几乎不用 micro-batch，因此重叠主候选为同层共享专家计算；这里的单 batch 不等于单请求、单 Token 或 `batch_size=1`。micro-batch／DBO 不作为本卡主要性能方案。

**对照方法**：在同一硬件、模型／专家权重、输入、路由、专家放置及图模式下固定总工作量，对比串行基线与“dispatch 完成 → 路由专家计算 → 发起 combine → 执行不依赖其接收结果的共享专家计算 → 完成 combine 接收”的候选路径。两组都执行相同的共享专家工作，完整耗时包含最终结果合并及所需归约；不预设重叠一定更快。

**窗口的源码依据与审稿更正**：原稿把共享专家安排在 dispatch 的 SEND／RECV 之间，与“保持 `FusedMoEKernel` 不变”不一致。`d7ada3a` 的 `_prepare()` 在 `prepare_async()` 后直接处理 hook／receiver（`modular_kernel.py:1255-1291`）；共享专家实际在 `_finalize()` 中、`finalize_async()` 之后和接收 hook 之前调用（`:1435-1465`）。团队公开基线 `v0.30.0` 的同文件 `:1419-1448` 也是 combine 窗口。因此首个候选改为复用该 combine 插入点，具体异步 P/F 与 EPLB 适用性仍需接入验证。若以后选择 dispatch 窗口，则必须明确调整调度及共享专家恰好执行一次的责任，不能继续同时承诺 kernel 调度不改。

| 部署层级 | 主要观察内容 |
|---|---|
| 单芯片 | 建立本地准备／整理、共享专家与路由专家计算的耗时和显存基线；本通信后端的单 rank 模式是否可直接运行另行核对，不假定它等价于多 rank 通信 |
| 单节点多芯片 | 对照串行与共享专家重叠候选的完整 MoE 耗时，拆分 dispatch、共享专家、等待、路由专家和 combine；图模式开／关分别报告，不混为同一组对照 |
| 多节点 | 按既定能力关闭图模式，额外观察计数拷回与主机同步、跨节点传输和 rank 间负载差异；采用完整调用链及最慢 rank 的完成时间，不能只看局部最快值 |

prefill 与 decode 分别选定可追溯的模型配置，记录 Token 数、隐藏维度、top-k、专家数、每专家容量、rank 数与路由分布。prefill 关注完整处理时间和有效 Token 吞吐，decode 关注每步延迟与等待开销；不只凭 Token 数断言瓶颈。比较部署规模时说明固定的是全局工作量还是每 rank 工作量；逻辑专家分配数、实际通信载荷与设备内拷贝分别记录。

**计时纪律**：先通过所选正确性检查，再预热并重复测量，报告稳定耗时及波动；按输出可读的完成边界计时，不只量 CPU 函数返回。用平台可用的计时／trace 工具区分主机等待、设备计算和搬运，避免在拟重叠窗口额外插入会改变执行关系的同步。重叠收益以相同工作量的完整 MoE 耗时差判断，同时检查显存和等待开销。

以上只形成测法与待验证项；没有性能数字、实际 trace、带宽结论或硬件运行证据。尚不具备的部署环境保持待验证，不要求为本课补齐硬件。

> 本段问答（2026-10-29 第 14 轮）：学习者选择同时设计 prefill／decode 两类负载，并补充主要采用单 batch、几乎不用 micro-batch，因此以共享专家计算作为主要重叠候选。导师据此整理三类部署层级与串行对照方法；未运行 benchmark，也未将单 batch 解释为 batch size 等于 1。

## 9. 证据等级、风险和仍待确认项

**版本边界**：学习者于 2026-10-29 审稿时将团队版本更正为 `v0.30.0`。已通过官方仓库解析到公开提交 [`ced6857afa0ea7b2e3f0846a62e1394e90f15607`](https://github.com/vllm-project/vllm/tree/ced6857afa0ea7b2e3f0846a62e1394e90f15607)，并对 modular kernel、未量化 oracle／方法、并行配置及 DeepEP LL P/F 做窄对照。本卡主体的文件行号仍固定于教学源码 `d7ada3aace051fecec553c185225db2259c2ac6a`；团队内部 patch 与实际运行提交未读取，不能把公开 tag 对照当成生产代码审计。

| 窄对照项 | `v0.30.0` 的核验结果及边界 |
|---|---|
| 归约与输入加权 | `output_is_reduced` 同样表示跨 rank 归约；prepare／finalize 均含输入加权标志。DeepEP LL 输入加权后也在 combine 改传全 1（`prepare_finalize/deepep_ll.py:282-288`、`:392-394`） |
| 共享专家插入点 | `modular_kernel.py:1419-1448` 同样位于 combine SEND／RECV 之间，不能把 dispatch 窗口作为不改调度即可得到的默认行为 |
| P/F 辅助接口 | 此版本没有教学快照中的 `supports_dbo()` 与 `allocate_fused_expert_output()` 方法；第 2 段对这两个方法的描述只属于教学快照，不直接当成团队版本可用 API。`out=output` 的 combine 输出接口仍存在（`deepep_ll.py:399-407`） |
| 工厂与 OOT | `use_all2all_kernels` 条件一致（`fused_moe/config.py:1060-1063`）；OOT oracle 同样不提供 Experts，权重处理需由插件接管（`oracle/unquantized.py:219-220`、`unquantized_fused_moe_method.py:200-205`）。具体初始化签名和团队 patch 仍需按实际版本处理 |

**证据等级与来源**：本卡为 B 级问答共建设计与验证方案。固定版本源码用于裁决公开实现；芯片抽象能力与业务场景来自学习者说明；接入选择、测试范围和故障处置由学习者在问答中确定，正文与具体测法由导师整理。它不作为学习者独立写作、已完成代码适配、真实设备测试通过或取得性能收益的证据。DeepEP 双缓冲信号协议属于导师补充核验，保留原帮助归因。

| 落地前待确认／验证事项 | 当前边界 |
|---|---|
| 实际部署与版本差异 | 公开 `v0.30.0` 的上述窄对照已完成；用户已确认 TP=8、DP=4、EP 开启、SP 关闭及 `C=T×D`。团队内部 patch、PCP／自定义拆组是否改变实际 world size、输入加权分支的支持范围仍需按真实实现核验 |
| 共享专家重叠的具体接入 | 公开源码插入点已确定为 combine 窗口；异步 P/F 具体实现，以及第 1 段提到的 EPLB／后端名单限制在目标配置下是否适用仍待核验，不预设已有重叠收益 |
| 正确性运行结果 | 第 7 段已有两层对照设计，并补充输入加权、跨 rank 归约、容量映射和动态图重放用例；参考实现、具体 dtype／容差、超限保护与真实运行结果尚未验证。双缓冲、event 与 handle 的普通调用契约保持用户确认口径，图重放的存储有效期另作验证 |
| 三类部署的性能结果 | 第 8 段已有 prefill／decode、单 batch 共享专家对照方案；单 rank 路径适用性、各层级计时与 trace、显存及实际收益尚未验证 |
| 故障后的恢复与重试 | 已选最小诊断、停用实例与上报方案；整个 EP 组的协调停止、资源重建、安全复用与重试条件仍待确认 |
| 后续精度与执行模式 | 量化路径单列待验证；micro-batch／DBO 不作为本卡主要性能方案，不为覆盖这些模式额外增加本课任务 |

上述保留项描述实际落地前的未知与验证工作，不新增为本课必需硬件实验或结课门槛；本卡按既定九段问答共建范围交付，Lesson 是否结课由对应验收记录和用户确认裁决。

> 本段问答（2026-10-29 第 15 轮）：学习者选择 B，提供团队版本 tag `v0.30.1`。导师保留本卡 `d7ada3a` 的源码依据，将跨版本适用性与其余已约定的待验证项集中列出；没有读取团队内部代码、迁移教学基线或新增实测结论。
>
> 同日审稿补正：用户将版本更正为 `v0.30.0`，公开 tag 与上述窄范围已核验。导师修正了归约标志、输入加权分支、工厂前置条件、共享专家重叠窗口及图重放生命周期的过强／不完整表述，并补充 OOT 初始化责任和容量契约要求。这些是导师文稿与源码核验的修正，不归因于学习者答错；本次仍未开展硬件测试或读取团队内部实现。
>
> 审稿中的配置补充：用户明确 TP=8、DP=4、EP 开启、SP 关闭，容量采用 `C=T×D`。导师据公开源码说明该配置的 all-to-all 触发条件，以及未启用 PCP、未自定义拆组时 D=32 的条件性推导；实际运行组大小仍以团队配置和 manager 为准。

## 面试介绍（约两分钟）

我结合团队使用的 vLLM v0.30.0 和自研芯片的通信能力，梳理了一套 MoE 专家并行适配方案。目标配置是 TP=8、DP=4，开启 EP、不启用 SP，主要考虑单 batch 场景。

方案中，我选择沿用 vLLM 的 modular kernel，把通信适配放在 prepare／finalize 层，由 Experts 封装自有 grouped GEMM 等计算算子。prepare 负责按专家分发 Token，finalize 负责回传并恢复原 Token 顺序。这里需要明确路由权重由哪一层处理，避免重复加权，同时区分专家结果求和与跨 rank 归约。

我重点梳理了数据归属和异步依赖。dispatch 返回按容量上限分配的独立输出。方案中，combine 将直接写入 vLLM 提供的输出张量，使 finalize 无需再复制一次结果。库内部使用两份轮换缓冲区，由调用方通过同流顺序或跨流 event 建立复用依赖；每次 dispatch 的独立 handle 则保留到对应 combine 完成。图模式下的地址和数据复用需要单独验证。

性能方案优先考虑在 combine 的发送与接收之间执行共享专家计算，并与相同工作量的串行执行比较。验证先覆盖未量化路径，分别检查通信契约和完整单层 MoE 的正确性，再评估 prefill、decode 两类负载。目前形成的是接入与验证方案，实际性能收益需要通过测试确认。
