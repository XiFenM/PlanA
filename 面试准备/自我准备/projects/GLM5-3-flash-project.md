## 项目：GLM-5.3-Flash 模型适配与优化（已完成）

> 事实依据：此前整理时引用的《GLM-5.3-Flash 推理适配项目总结》、本人 2026-11-02 的问答补充，以及 2026-11-09、2026-11-10 合并的适配细节材料；沿用旧档案中未被新材料替代的实践细节。项目已完成，由云服务团队正式生产上线。
> 来源可用性说明（2026-11-10）：原链接所指的 `GLM-5.3-flash-project-summary.md` 当前不在本目录中，不能当作本仓库内可打开的独立证据。保留本档案已经记录的本人确认及来源归属，不补造总结文件；原始代码、日志和评测索引尚未在本次整理中重新核验。
> 补充材料中的源码定位使用原工程内相对路径，行号沿用材料记录，不是本仓库链接；上游布局描述限于项目当时参考的 GLM5 路径，不泛化为所有 vLLM／CUDA 版本。
> 本档案整理项目经历、职责和结果口径；下方【待补充／待核验】用于完善复现与面试材料，不改变已交付状态。
> 对外统一使用“自研 AI 加速芯片”，不写内部代号、内部仓库名或内部算子编号。

### 项目概览

| 字段 | 当前信息 |
|---|---|
| 开发与交付时间 | 2026-09-01 至 2026-10-27；截至 2026-11-02 已确认生产上线，实际首次上线日期本人不掌握 |
| 角色 | AI 框架开发工程师；独立负责本模型在既有 vLLM 硬件插件中的适配开发、插件侧性能优化、排障与发布验证 |
| 模型与部署 | GLM-5.3-Flash-Mix，AWQ 4-bit 权重、BF16 激活，单机 8 卡（自研 AI 加速芯片），TP=8，`block_size=256`。单机配置由本人于 2026-11-20 确认 |
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

两次 OOM 分别来自分组计费模型与物理页 Padding，修复位置不同。混合 cache 包含 11 个 full MLA 主 cache、11 个 KPool index cache、11 个 KPool tail cache，以及 34 个 KDA／Mamba 状态 cache。TP=8 时，每个 rank、每层 KDA 的一个状态 block 包含：

| 状态 | 形状 | dtype | 每 block 字节数 |
|---|---|---|---:|
| 因果短卷积滑窗 `conv_state` | `[3, 3072]` | BF16 | 18,432 B |
| delta-rule 递推矩阵 `recurrent_state` | `[8, 128, 128]` | FP32 | 524,288 B |
| 合计 | 两种状态打包 | — | 542,720 B，约 0.518 MiB |

当时未扩大的 MLA 页为 256 KiB（0.25 MiB），小于 KDA 的真实状态页。

##### 第一次：分组与逐层分配的计费口径不一致

启动在申请 Mamba cache 时触发 `Tried to allocate 674 MiB`，材料同时记录 `GPU KV cache size: 45,409 tokens`。上游 `_get_kv_cache_groups_glm5_next` 将 34 层 KDA 合为一个 Mamba 组，按共享页布局核算，并设置 `page_size_padded = MLA page`；移植时沿用了 256 KiB 的 MLA 页假设。目标 runner 却为每个 KDA 层独立申请 raw byte-page tensor，实际需要 34 份 `num_blocks × 542,720 B`。

这使规划器的共享页成本模型与 worker 的逐层分配不一致，材料记录 `num_blocks` 高估一度约 6.5 倍。仅降低 `gpu_memory_utilization` 不能修正 cache 拓扑和计费口径。

我在 `patch/patch_kv_cache_utils.py` 中增加模型专用分组，并同步修正每 block 字节统计：

```text
1 个 full MLA 组
1 个 KPool index 组
1 个 KPool tail 组
34 个 KDA 各自独立的 MambaSpec 组
```

每层 KDA 使用真实页大小 `542,720 B`，设置 `page_size_padded=None`；其余 attention cache 仍通过 `UniformTypeKVCacheSpecs` 合并。分组后按实际逐层 allocation 求和，使容量核算与分配使用同一成本模型。

CPU 离线闭环记录为 `num_blocks=1509`、每 block 合计约 `20.734 MiB`，即 `1509 × 20.734 MiB ≈ 30.55 GiB`，对应可用 KV 空间约 `30.56 GiB`。`tests/test_glm5_kv_grouping_dlc.py` 覆盖“分组 → num_blocks → 每层实际字节”的完整链路。

这里保留原日志中的 45,409 tokens，但不沿用补充材料的 `45,409 = 177 × 256`：该乘积实际为 45,312，不能据此反推当时的物理 block 数。离线 1,509 blocks、后续 Padding 排查中的 771 blocks 和真机 token 容量来自不同阶段，不合并为同一配置。

##### 第二次：独立分配仍沿用共享页 Padding

分组修复后启动仍然 OOM，日志显示真实 `page_size_bytes=542,720 B`，但 `page_size_padded=786,432 B`，即被补到 0.75 MiB。原因是平台层仍调用 `_align_hybrid_block_size`：为让共享页容纳 Mamba 状态，先增大 attention block size，再把 Mamba 页补齐到相同的 attention 页大小。

目标 runner 已经逐层独立分配，MLA 与 KDA 不共享 backing storage；`bind_kv_cache` 只读取 conv／recurrent 的真实内容，Padding 尾部不参与计算。因此这层补齐只会占用额外显存。按材料给出的页大小和 771 blocks 重新计算：

```text
每个 KDA block 多分配 = 786,432 − 542,720 = 243,712 B = 238 KiB
34 层 × 771 blocks × 243,712 B ≈ 5.95 GiB
```

补充材料中的“约 230 KiB／5.7 GiB”与上述输入不一致，改按算式保留约 5.95 GiB；这只是目标平台该次逐层分配的额外容量估算，不用于推算上游共享池的总开销。

我在平台 `update_block_size_for_backend` 中继续解析 backend 首选 block size，但跳过 `_align_hybrid_block_size`，保持 `mamba_page_size_padded=None`；同时让 `patch/patch_kv_cache_interface.py` 中 Mamba 的 `page_size_bytes_padded` 返回真实 `page_size_bytes`，防止后续核算再次引入 Padding。

修复后记录为 `page_size_padded=None`、真实页大小 `542,720 B`，34 层 KDA 全部分配成功。早期启动日志中的 45,409 tokens 来自有误的容量核算。修复后，在显存利用率 0.85 下，启动日志报告 148,762 tokens。排错时也排除了仅降低显存利用率、启用目标 allocator 不支持的 `expandable_segments:True`，或继续调整已经确定的状态形状等方向。

##### 上游共享页布局成立的前提

补充材料记录的 NVIDIA GLM5 路径通过 `allocate_kv_cache` 申请统一的 `int8` backing buffer，再用 `as_strided` 为不同层与 cache group 建立 view。`KVCacheTensor` 的关键约束是：**同一个全局 block ID 在同一时刻只由一个 cache group 拥有**。因此，不同 group 的 view 可以映射重叠地址，而同一时刻实际使用这些字节的 group 仍然唯一。

例如，block 17 分给 MLA 组时按 MLA 页解释，回收后分给 KDA 组时按状态页解释；同一个请求的 MLA cache 与 KDA state 使用不同的全局 block ID。材料中的 `bytes_per_block` 只计 MLA 与 KPool index，Mamba 和 tail 使用重叠 view，前提正是物理分配与 block 所有权共同遵守这套布局。

为让共享槽位容纳不同类型，平台先增大 MLA 页到足以容纳 KDA，再将 KDA 补齐到相同大小。对应的约束检查是 `mamba.real_page_size_bytes <= mla_page`；在该例中，MLA 页从 256 KiB 扩到 786,432 B 后，真实 542,720 B 的 KDA 状态才可放入。Padding 换来统一页池、跨类型 block 复用，并为调度、prefix cache 和 KV transfer 提供统一布局。

| 比较项 | 材料记录的上游共享页路径 | 本项目目标平台路径 |
|---|---|---|
| 物理分配 | 统一 backing buffer，group 间可建立重叠 view | 按层独立 allocation |
| 页大小约束 | 共享页须容纳各类状态，需要对齐／Padding | 按真实状态字节分配，无须为另一类 cache 补齐 |
| 非连续访问 | 对应 CUDA／Triton Kernel 在设备端按指针与 stride 寻址 | 当时后端的 `KernelDesc` 路径要求紧凑、无 storage offset 的输入；相关 view 触发物化／搬运 |

支持设备端 stride 并不意味着非连续访问没有性能成本，也不能由此推断目标硬件永远不能实现共享页；本次修复针对的是当时 runner、后端和算子接口的实际约束。分组计费、去掉无用 Padding、拆成连续状态池分别解决核算、容量和访问路径问题。

总结另给出后续配置的单请求预算：`B(L)=69+2×ceil(L/256)`，其中 L 为请求长度，69 对应 34 层 KDA 各 2 个状态 block 和 1 个 tail block。相应的容量推导与实际验证长度见“容量与长上下文”。

#### 3. 状态拆池消除非连续搬运开销

早期服务能够执行，但同一短 prompt 下，prefill 单步 Host 耗时约 179 s，decode 单步约 120 s。通过 `py-spy`、模型内 Profile 和隔离微基准，我定位到 conv state 与 recurrent state 打包在同一字节页后形成非连续 view；目标后端对这类访问退化为 Host 逐元素搬运，开销与整个 Storage 大小相关。

##### 为什么打包页会触发搬运退化

拆池前，本项目每层状态以 `int8 [P, 1, 1, 542720]` 存储，P 为状态 block 数。`MambaBase.bind_kv_cache` 按每页字节区间 `[0, 18432)` 和 `[18432, 542720)` 绑定 conv 与 recurrent。虽然页内各状态紧凑，但同一种状态跨 block 时要跳过整张打包页：

| 状态 | 形状 | 紧凑时 `stride(0)` | 打包页 view 的 `stride(0)` |
|---|---|---:|---:|
| conv | `[P, 3, 3072]`，BF16 | 9,216 | 271,360 |
| recurrent | `[P, 8, 128, 128]`，FP32 | 131,072 | 135,680 |

表中 stride 以各自 dtype 的元素数计，实际跨页距离都是 542,720 B。两个 view 均非连续，相关后端路径无法直接使用正常 DMA，转而由 Host 参与搬运。

隔离微基准从 1,168 个 block 中只访问 8 个、约 4 MiB 的 recurrent 数据；卷积也做了连续池／打包页 view 对照：

| 操作 | 连续池 | 打包页 view |
|---|---:|---:|
| `index_select + clone` | 0.181 ms | 579.7 ms |
| `index_copy_` | 1.544 ms | 1,873 ms |
| KDA conv prefill | 0.166 ms | 1,396 ms |
| KDA conv update | 0.259 ms | 1,339 ms |

模型内 Profile 同样显示：prefill 的 gather／scatter／conv 合计约占 96%，decode 的 conv update／recurrent 合计约占 96%，设备计算少而 8 个 worker 的 CPU 占用高。本次补充的 prefill `py-spy` 窗口中，gather／scatter 采样占比合计为 63.9%，卷积另占 35.2%，说明单独处理 gather／scatter 仍不能覆盖卷积路径；采样比例与上述 Profile 耗时比例分别记录，详见第 5 项。每层、每步临时调用 `.contiguous()` 也会保留物化成本，因此需要在分配阶段改变物理布局。

##### 拆池方式与接口适配

我通过 `get_state_shape()`／`get_state_dtype()` 获取各状态规格，为两类状态分别分配连续 tensor：

```text
conv_pool = BF16 [P, 3, 3072]       stride(0) = 9216
rec_pool  = FP32 [P, 8, 128, 128]   stride(0) = 131072

block b → conv_pool[b]
        → rec_pool[b]
```

两池仍使用同一个 block ID，`num_blocks`、block table 与调度器的状态块生命周期不变；模型侧仍按 `conv_state, recurrent_state = self.kv_cache` 访问。每 block 合计仍为 542,720 B，拆池本身不减少状态字节数；第 2 项去除 Padding 才是容量修复。

实现采用 `MambaStatePool` 容器，它是 `list` 子类，用于容纳不同形状与 dtype 的 tensor。补充材料记录的发布实现按规格自动判断：各状态的每 block 字节数均满足 512 B 对齐才拆池；本模型 conv 为 `36 × 512 B`，recurrent 为 `1024 × 512 B`。不满足该条件时分配器回退打包页。早期设计曾使用拆池开关，不将其写成最终发布必须配置的选项。

| 实现定位（沿用材料中的行号） | 修改内容 |
|---|---|
| `worker/mamba_cache.py:51` | 分配独立状态池并封装为 `MambaStatePool` |
| `patch/patch_mamba_state_pool.py:55` | patch `MambaBase.bind_kv_cache`；识别容器后校验各状态的形状、dtype、block 数与 `is_contiguous()`，直接绑定为 tuple |
| `worker/dlc_model_runner.py:7206` | Mamba 分支调用拆池分配器；cache 清理、日志及 FP8 scale 初始化等通用代码兼容容器条目，不代表本模型已启用 FP8 |
| `patch/patch_kv_block_zeroer.py:119` | 遍历池内每个 tensor 清零，不再假设 cache 条目本身就是 Tensor |

##### 结果与后续优化的边界

该阶段通过 21 项单测和真机对照。在相同短 prompt 的模型内插桩中，Host 耗时记录如下；单步与单次调用分别列示，不能相加或混算：

| 测量项 | 拆池前 | 拆池后 | 单位 |
|---|---:|---:|---|
| prefill | 179,434 | 5,703 | ms／step |
| decode | 119,962 | 2,579 | ms／step |
| conv prefill | 1,941 | 0.40 | ms／call |
| conv update | 1,835 | 0.19 | ms／call |
| state gather | 729 | 44 | ms／call |
| state scatter | 2,444 | 36 | ms／call |

这些是布局归因实验与 Host 计时，不能换算成端到端吞吐提升倍数，也不与上面的隔离微基准逐项拼接。

拆池恢复了连续状态访问，但通用 `index_copy_` 在该阶段仍扫描整个 584 MiB recurrent pool（1,168 blocks），没有只搬运目标页。之后继续接入专用 state gather／scatter 按页搬运，并修复 HBM 16 GiB 以上的地址换算回绕；对应算子接入与协作分工见第 4、7 项。584 MiB 只指 recurrent pool，不包含 conv。发布期其他 native／fallback 清理见第 8 项。

#### 4. 验收并接入融合算子

我对 18 项候选需求进行覆盖核查，形成 12 条首轮提交；后续验收并接入 KDA 短卷积、chunk prefill、recurrent decode、gated RMSNorm、state gather／scatter，KPool 更新／压缩、select／top-k／expand、slot mapping，以及 512 维 NoPE 稀疏 MLA 和 mHC 融合路径。

验收中发现并推动处理长序列卡死、wrapper 整池搬运、Kernel 未按 stride 读取、ATen scalar 打包错误、PAD 槽语义和状态布局不一致等问题。对 mHC 曾出现的“native 与 fused 两侧都回退，数值比较仍通过”，我加入调用计数断言，确认测试实际命中融合路径。

我将 KPool 的历史长上下文瓶颈定位到 select／top-k 融合算子的扫描与并行效率，由算子同事修改和优化代码，再由我验收问题是否消失及性能情况。算子级时延改善与整模结果分别记录，不将其全部归为插件代码的独立收益；单请求长上下文的具体测量配置仍待补齐。

#### 5. 减少 Host／Device 往返与下发次数

我结合 Profile、拷贝事件及隔离实验识别 Host 开销，并实施 metadata H2D 合并、pinned／device buffer 常驻、静态参数加载期预物化，以及 KPool 阻塞 D2H 消除。对设备侧 view 物化逐项检查，结合融合算子减少下发次数。

##### 从总耗时定位到 Host 调用路径

判断从同一窗口的 Host／Device 时间线开始：Host 侧使用 PyTorch profiler、`py-spy` 和 Python 事件时间，Device 侧使用 Kernel log 的 `cycles/ops/bytes` 及 trace 的 busy／gap，检查单步 wall time 主要消耗在哪些区间。Host 工作、设备执行与等待可能重叠，因此不能简单相加，也不能直接把多个 Kernel 的 cycles 总和当成整步设备占用时间。

拆池前的现场记录为 8 个 worker 各占约 200% CPU，设备计算很少，而 prefill／decode 单步分别约 179 s／120 s。CPU 高和设备空闲提供排查方向，但尚不能排除同步、通信等待或设备侧停顿，仍需定位调用栈并做隔离对照。

对 TP0 worker 的 `py-spy` 采样命令为：

```bash
py-spy record --pid <Worker_TP0> \
  --duration 60 --rate 50 --format speedscope
```

prefill 窗口的叶子帧分布如下，函数名沿用材料中的诊断定位：

| Host 叶子帧 | 采样占比 |
|---|---:|
| `scatter_states_dlc` | 50.1% |
| `_prefill_new_op`／KDA conv prefill | 35.2% |
| `gather_initial_states_dlc` | 13.8% |

三项合计约 99.1%，说明采样集中在 KDA 状态搬运与卷积调用附近。叶子帧既可能在执行 Host 工作，也可能在等待设备；这些比例不等于各算子的设备耗时，更不能单独证明 Kernel 没有问题。

##### 用 profiler 区分下发、搬运与同步开销

2026-09-29 的 profiler 窗口记录：20-token prefill 单步约 11.975 s，伴随大量 Host 事件：

| 事件 | 次数 |
|---|---:|
| `synLaunchKernelQueue` | 32,287 |
| `synHostMalloc` | 32,504 |
| `driver.memcpy` | 33,487 |
| `aten::item + D2H`（材料中的组合统计项） | 5,607 |

trace 中还出现 `aten::copy_`、`copy_after_async`、`synMemCopyAsync`、`_local_scalar_dense`，以及在该路径中触发同步的 `torch.any`／`torch.equal` 校验。这些记录给出了减少逐调用下发、Host 分配、搬运和标量读回的具体目标；事件之间可能嵌套或关联，不将次数相加为独立操作总数。

同一补充材料另列出关闭 profiler 后，1,211-token 请求的 TTFT 约 13.8 s。它与 20-token、带 profiler 的单步计时具有不同输入、计时窗口和插桩条件，仅保留为阶段记录；不能由两者耗时接近直接断言固定成本支配，或推导开销与 token 数弱相关。

##### 用布局对照验证归因

为区分“Host 正在等待慢 Kernel”与“布局触发 Host 搬运”，我把 KDA gather／scatter 和卷积抽到隔离环境，以相同逻辑操作、相同数据对比连续池与打包页 view。第 3 项已列出完整微基准：连续池的相关调用处于亚毫秒至毫秒级，打包页 view 达到数百至上千毫秒，并伴随 Host staging，耗时与整个 Storage 大小相关。

这里控制的是输入布局和逻辑操作；布局本身可能改变后端分派、物化与搬运路径，不能称为底层执行的每一个 Kernel 都完全相同。进一步在模型与输入保持一致的对照中替换状态池布局，prefill／decode 的 Host 单步由约 179 s／120 s 降至 5.7 s／2.6 s，卷积单次调用也恢复到亚毫秒级。微基准、模型内 Profile 与拆池前后对照共同支持“非连续布局触发 Host fallback”的归因，具体计时见第 3 项。

##### 用设备空洞与队列批大小验证后续优化

后续 decode 的一组 Host／Device 对齐记录显示：Host 每步约 1,510 次 Kernel queue 下发，Device 侧约 3,924 个 Kernel，按这两个计数相除约为 2.60 个 Kernel／批；材料另记录典型批大小约 2.3–2.6。单批设备消费约 150 µs，提交线程等待 Host 主线程继续提供工作，队列批量较小，同时每步存在约 389.5 ms 的设备空洞。

这组记录指向 Host 供给不及时。3,924 是该观察窗口的设备 Kernel 数，下面 3,888 则来自优化对照的基线；两者不视为同一次采样或强行对齐。队列下发次数、设备 Kernel 数与 profiler 事件数也分别记录。

总结中的 profiled decode 对照记录：view 物化由 204 次／步降到 0，Kernel 下发由 3,888 次降到 1,982 次，设备空洞由 389.5 ms 降至 29.1 ms，原约 223 ms／步的长阻塞 D2H 被消除，未再出现大于 0.5 ms 的该类阻塞项。这些是带 Profile 的流水线指标，不能替代干净服务计时。

减少 view 物化、阻塞 D2H、下发次数并接入融合算子后，Host 工作量与设备空洞共同下降，支持后续优化方向；这是多项改动的组合结果，不能把全部收益归给其中某一项。完整证据链为“wall time 异常 → 调用栈与事件定位 → Device trace 对齐 → 隔离布局对照 → 模型内复测”，其中受控布局对照的因果证据强于单独的 CPU 占用率或 gap。

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

##### KDA 地址回绕：从首个异常张量到 gather 未写输出

服务的 `/health` 与推理请求均返回 HTTP 200，但输出稳定为重复的 `!` 类 token；hidden states／logits 中有大量 NaN，Inf 为 0，权重统计未发现 NaN／Inf。结合前向探针，我将排查重点移到模型执行与缓存数据路径；HTTP 成功和权重有限本身不证明 tokenizer、采样或权重映射完全正确。

逐层探针记录 layer 输入／输出、attention、MLP、MoE 的 NaN／Inf 数量、absmax、shape、dtype，以及所在的 warmup／prefill／decode 阶段。首个异常收敛到 layer 0 的 KDA chunk prefill `initial_state`。补充材料将该处形状记录为 `(1583, 8, 128, 128)`，并记录 head 5 的 16,384 个元素为 `0x7fc00000` qNaN，其他 head 留有旧状态位型。这更值得怀疑未写入或地址错误，尚不能单凭位型排除数值计算问题。

关键矛盾是：对应 state page 的 D2H 快照全零，CPU 侧 `has_initial_state=False`，mask 也显示 false，按调用契约 gather 应清零输出，但 `initial_state` 仍有 NaN 和旧值。因此开始检查 gather 是否真正覆盖了输出 buffer，而不只是重复清零源 state page。

最初在低 HBM 地址独立测试 gather，使用正常 mask、输出预填 NaN，并运行约 1 万次压力循环，均通过。这曾将排查方向引向 metadata H2D 生命周期、mask descriptor 和状态清零，但独立测试的内存布局不同于加载大量权重与 KV cache 后的服务进程，不能排除高地址缺陷。

我随后在真实模型进程中，对 layer 0 第一次 gather 做同调用 sentinel 对照：将受检输出预填为 `42`，分别使用原始 mask、克隆 mask、强制 bool false、int32 false 和 bool true。各组都得到：

```text
eq42 = 131072
returned_same_ptr = True
```

这证明该次受检输出的 131,072 个元素没有被覆盖，返回的也是原输出指针。这个计数等于单页的 `8 × 128 × 128`，不是前述 1,583 页状态几何的全量元素数；全量应为 207,486,976，不能把两处观测混成“整个状态池都未写”。单次探针张量与全量形状的具体切片关系仍需原日志核验。

Kernel 日志同时显示 launch 和 stream 正常、未被跳过，实际执行约 9,000–15,000 cycles。结合不同 mask 的结果，问题范围进一步缩小到已启动 Kernel 的有效读写路径；sentinel 本身证明的是目标输出未更新，地址回绕的判断由后续阈值实验与 ABI 审计完成。

##### HBM 地址阈值与目标 ABI 的对应关系

我通过占用 HBM 将 state 与输出放到不同地址段。材料记录的边界对照如下，GiB 为其使用的 HBM 偏移口径，不是把完整设备地址直接换算成容量：

| 观察 | state 地址 | output 地址 | HBM 偏移与结果 |
|---|---|---|---|
| 正常样本 | `0x1000003cbc80200` | `0x1000003cbd80200` | 约 15.18 GiB，低于 16 GiB，gather 正常 |
| 失败样本 | `0x100000407800200` | `0x100000407900200` | 约 16.12 GiB，跨过阈值后失效；`true_eq7=0`、`true_eq42=131072` |
| 真实模型 | `0x100000898200200` | 材料未列出 | state 偏移约 34.38 GiB，落在已复现的高地址区间 |

材料另记录了占用 18 个 2 GiB dummy buffer 后复现 gather 未写输出的实验，占位总量为 36 GiB。它与下文修复后回归的“先占用 18 GiB”是两次不同实验。

随后审计 `attention/kda/kda_state_pool.h` 的地址换算。旧实现使用 `unsigned long` 接收和计算 word 地址，简化形式为：

```c
unsigned long dst_word =
    (unsigned long)dst->address * 32 + ...;
```

张量描述符中的 `address` 以 128 B 为单位，目标 word 地址以 4 B 为单位，因此需要乘以 32：

```text
word_addr = address_128B × 128 B / 4 B
          = address_128B × 32

目标编译器：__SIZEOF_LONG__ = 4，__SIZEOF_POINTER__ = 4
32 位 word 地址空间：2^32 words × 4 B/word = 16 GiB
```

目标 ABI 中 `unsigned long` 只有 32 位，乘法与地址中间值发生无符号回绕，丢失高位；边界恰好对应实验中的 16 GiB。这里判断的是设备编译目标的整数宽度，不能用 Host 系统的 `long` 或指针宽度替代。根因位于 gather／scatter 共用的地址换算，源 state 的内容全零也无法防止错误寻址。

##### 全链路 64 位修复与高地址回归

我提供复现与定位，算子同事修改共用地址路径，再由我验收。修复在乘法之前显式扩宽，示意如下：

```c
unsigned long long dst_word =
    (unsigned long long)dst->address * 32ULL + kda_word_offset(...);
```

修改覆盖 `KdaMetadataCache.block`、`kda_word_offset()`、`kda_load_word()`、`kda_page_index()`、`kda_copy_words()`，以及 `dst_word`、`src_word`、`src_relative` 等中间值；对齐掩码的 `127`／`~127` 也改为 `127ULL`／`~127ULL`。这样避免仅把最终接收变量改宽，而中间计算或掩码仍丢失高位。头文件同时供 gather 与 scatter 使用，两条方向一起修复，防止读路径恢复后写路径仍破坏错误地址。

高地址回归采用 `PAGES=1583`、`HEADS=8`、`DIM=128` 的生产几何，先占用 18 GiB HBM，将 state 和输出置于 16 GiB 以上，覆盖 gather true、gather false、PAD page、scatter，以及 sentinel 是否被正确覆盖。修复后记录：

```text
state = 0x100000490400200
out   = 0x1000004c1e00200
1 passed
```

这是一项定向高地址回归的结果，不与发布回归数量相加。真实服务复测中，layer 0–2 的 NaN 消失，首个 NaN 从 layer 0 后移到 layer 3；它与高地址回归共同支持第一处修复有效，同时暴露出下面独立的 sparse MLA null block 污染，不能把层号后移当成整模已正确。

##### null block 污染为什么会跨越 warmup 和正式请求

本路径保留物理 block 0 作为 `NULL_BLOCK_ID`，供 padding、无效索引及占位访问使用，并依赖其内容全零。它不属于正式请求，也不进入正常 block 分配／释放列表；这意味着请求不分配它，但计算仍可能读取它。

V1 启动的 `_dummy_run()` 预热 sampler 和模型路径，dummy batch 没有真实请求的 block table，`slot_mapping` 默认为全 0。cache 写入将其当成真实 slot；该次 dummy latent 含 NaN，于是 11 个相关 sparse MLA／indexer 层的 block 0 被污染。初始化的 `torch.zeros` 和最初的 KVBlockZeroer 都发生在 warmup 之前，不能保证 warmup 后仍为零。

正式请求使用 block 1 及之后的空间。block 0 不会出现在“本步新分配 block”列表中，常规清零与请求回收不会覆盖它；没有显式修复时，污染可持续到 worker 退出。

读取端的 top-k buffer 宽度为 2048，短上下文、causal mask、padding 或候选未填满都会留下无效项。补充材料定位到 `attention/sparse_attention/sparse_attention_kv_cache/sparse_attention_kv_cache_bf16.cpp:1821`：该路径将无效或越界索引映射到 0，有效索引保持原值。因此正式请求即使没有分配 block 0，仍会通过无效 top-k 项访问这块物理内存。

```text
KV cache 初始清零
    → dummy warmup：全 0 slot_mapping 将 NaN 写入 null block
    → 正式请求的无效 top-k 项映射到 block 0
    → gather NaN latent，在 score mask 前进入 QK 计算
    → 该故障路径中首个 sparse MLA 层出现 NaN
    → 后续残差传播，logits 含 NaN，输出连续感叹号
```

材料还记录过 405,248 行 cache 中仅一行 NaN 的情形，说明污染不需要覆盖整个 cache。这里能确认的是故障 Kernel 在 mask 前读入了 NaN，且后续 mask 没有隔离该路径的输出污染；不能泛化为“所有 QK 后的 mask 都必然失效”。安全覆写无效分数可以清除相应位置的 NaN，是否还有累加、归约或 value 读取污染需结合实际 Kernel 数据流判断。

##### 修复位置与执行顺序

我在全部 dummy／warmup 完成后、服务 ready 之前再次清零 block 0，并同步设备，材料定位为 `worker/dlc_worker.py:709`。对应调用顺序为：

```python
if hasattr(self.model_runner, "_zero_block_ids"):
    self.model_runner._zero_block_ids([0])

torch.dlc.synchronize()
```

清零位于 warmup 最后一次 cache 写入之后，并放在 `is_last_rank` 分支之外，使所有 TP／PP rank 都清理本 rank 的 cache。补充材料说明插入位置考虑了 V1 sampler dummy 与 V2 warmup 的收尾，但本项目发布验收范围仍为 V1，不据此扩张为 V2 已交付。

dummy run 改用 `PAD_SLOT_ID(-1)` 跳过写入、使用 scratch block、在 gather 后而 QK 前清零无效 latent，以及启动时断言 null block 全零，均属于后续加固建议，不计为本次已实现。HTTP 成功、单元测试通过和模型正确性分别验证，不能互相替代。

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

1. 混合缓存的分组、容量核算与实际分配怎样保持一致？两次 OOM 分别发生在哪一层，为什么两次修复不同？上游依靠哪些物理布局与 block 所有权前提支持共享页，为什么本次不能直接沿用？
2. 状态拆池为什么能同时影响 gather、scatter 和卷积？怎样用隔离实验区分布局开销与 Kernel 计算开销？如何在保持 block ID 语义和总字节数不变的情况下适配绑定、清零与迁移？
3. KPool 的逐 head 非线性与加权顺序为什么必须保留？算子接入怎样同时验证数值正确和真实路径命中？
4. Graph bucket 补齐输入后，metadata、状态槽和 buffer 生命周期为什么也要改变？什么条件下 graph 可能变慢？
5. NaN 的第一个出现位置如何帮助区分两个根因？怎样用 sentinel、地址阈值实验和目标 ABI 将 gather 未写输出收敛到 16 GiB 回绕，为什么只改最终变量类型不够？warmup 为什么能污染正式请求会读取的 null block，为什么必须在最后一次 warmup 写入后由所有 rank 清零？低地址单测和 HTTP 200 为什么不足以证明模型正确？
6. 怎样结合 Host 采样、profiler 事件、Device trace 和受控布局对照区分 Host 开销与等待慢 Kernel？怎样解释 Host 单步、带 Profile 的步骤、token gap、TTFT 和端到端吞吐之间的差别？哪些收益属于本人插件改动，哪些属于算子协作？

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
