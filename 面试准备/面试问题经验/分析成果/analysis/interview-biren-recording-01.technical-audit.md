# 壁仞科技面试记录：技术原理核查

核查日期：2026-11-17。记录 ID：`interview-biren-recording-01`。

这份文件区分录音中实际出现的说法、公开资料能验证的原理，以及仍需代码或测试补证的实现细节。现场证据来自 [Qwen ASR 原文索引](/root/workspace/learning/daily-work/outputs/managed/interview-video-analysis/transcripts/interview-biren-recording-01.qwen-asr-indexed.md)及[画面核查](/root/workspace/learning/daily-work/outputs/managed/interview-video-analysis/analysis/interview-biren-recording-01.visual-evidence.md)。ASR 片内没有逐句时间或可靠的自动说话人标签，以下引文均保留原始识别文字；P 编号用于定位文本，不代表完整对话轮次。

本次没有成功取得另一理解模型的正文，因此不称为双模型交叉验证。官方资料只能用于核查原理，不能替录音补写候选人没有讲出的答案，也不能证明自研后端的实际实现与性能。

## 优先结论

1. **`8×128×128` 有明确的配置解释，不能直接判错。** 官方 GLM-5.3-Flash 为 64 个 KDA heads，head dimension 为 128；结合现场后续确认的 TP8，每卡 8 个 heads 与该数字相容。现场薄弱处是当时未清晰说明轴名及分片条件。
2. **GLM-5.3-Flash 的文本 MLA 分支是 NoPE 变体。** 不应把 DeepSeek-V2 的解耦 RoPE 路径强加给这个模型。但录音中的“默认旋转位置编码在前面做好”也没有把两种模型明确区分，不能补写成现场已正确解释 NoPE。
3. **Q 不进入历史 KV cache，不等于 Q 不做低秩投影。** 具体 GLM-5.3-Flash 配置存在 `q_lora_rank=1536`；这比泛泛评价“MLA 一定压缩／一定不压缩 Q”更准确。
4. **“容量三倍”应按现场澄清写成核算错误纠正。** 不应继续宣传为独立的三倍内存优化，也不能从这次澄清推断诚信或人格。
5. **D2H 说明已经包含消费前等待。** 进一步需要澄清的是实际 API、内存生命周期、逻辑视图与物理接收空间，不应写成“完全没考虑同步”。

## 1. 模型名称与架构

ASR 分片 002 / P004 识别为 `KTA`、`Sparse 的 MIA`、`Kimi K3`。官方 GLM-5.3-Flash 配置及框架实现支持 **KDA 与 sparse MLA / DSA 混合**。因此 KTA→KDA、MIA→MLA 是有公开技术背景支持的术语校对候选，但不应静默覆盖原始文本，也不能仅凭 ASR 拼写认定口述错误。[官方模型配置](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/46a050bec13002ad29ee795c16e61cf4fa3c4a9c/config.json)、[Transformers 模型文档](https://huggingface.co/docs/transformers/main/en/model_doc/glm5_next)

Kimi K3 本身确有官方模型与 KDA / Gated MLA 架构，不能按旧知识把这一名称自动纠正成 Kimi Linear。KDA 的原始原理可以参照 Kimi Linear 论文，但“借鉴哪个具体版本”的历史关系不能仅从这份 ASR 确认。[Kimi K3 官方仓库](https://github.com/MoonshotAI/Kimi-K3)、[Kimi Linear 论文](https://arxiv.org/abs/2510.26692)

## 2. KDA 的状态形状、卷积尾状态与精度

现场证据：分片 002 / P005：“递推矩阵需要是 8×128×128 我记得”；P007 随后的轴名说明不完整。分片 004 / P015 的问答则明确出现：“现在就相当于是你Attention、MOE都是TP8，是这个意思吗？对对对对对”。

官方配置是 64 heads、head dimension 128、短卷积 kernel size 4。当前 vLLM 的 KDA 状态形状计算将 heads 除以 TP。由此可推导，在相应分片约定下，单请求、单层、单 rank 的递推状态可以是：

```text
[H_local, D_k, D_v] = [64 / 8, 128, 128] = [8, 128, 128]
```

这是**配置相容性核查**，不是已经查验了用户自研插件的 tensor。实际实现可能交换最后两轴；因为本例两轴都是 128，只报尺寸无法证明轴语义。池外层还可能带 block / request 等维度。[vLLM KDA 实现](https://github.com/vllm-project/vllm/blob/main/vllm/models/glm5next/common/kda.py)、[状态形状计算](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/mamba/mamba_utils.py)

kernel size 4 对应保存 3 个历史位置这一思路成立，但“3×一个 head dim”没有交代全部投影通道。以当前 vLLM 的融合布局、TP8、未启用额外 speculative 槽位为例，卷积通道数为 `3×64×128/8=3072`，历史宽度为 3；布局可转置，启用推测解码还可能增加历史存储宽度。它和递推矩阵是两种状态，不能混成普通的逐 token K/V 列表。[同一状态形状计算](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/mamba/mamba_utils.py)

P005 的精度原文是“一部分是 FP16，一部分是那个 BF16”。当前上游 KDA recurrent state 的 auto 默认值为 FP32，也支持 BF16，conv state 则跟随模型／cache 配置。这与录音文字有差异，但可能来自 ASR、版本或自研实现。**没有插件源码及实际 tensor dtype，不判定现场一定说错。** 核查时应逐个记录 state 的逻辑 dtype、storage 字节数和 stride。[vLLM `kda_state_dtype`](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/mamba/mamba_utils.py)

## 3. 字节池、连续性与“拆池”

分片 002 / P005–P006 描述字节池与两个状态池的适配。应区分**原始存储采用 int8/byte 视图**和**模型计算使用 int8 精度**。一个 byte buffer 可以再按具体 dtype 与形状建立视图；`view(dtype)` 是存储重新解释，与数值类型转换不同。仅凭存在 byte buffer，不能得出框架默认把浮点状态量化成 int8 的结论。[PyTorch `Tensor.view`](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.view.html)

拆成独立、连续且对齐的状态池可以是合理的自研后端适配方案。但其收益需由实际 offset / stride、内核接口要求、是否触发 materialization/copy 以及 profiler 证明。本次没有这些源码或测量，不能把“性能会好很多”改写成已验证的具体加速倍数，也不能断言所有统一字节池必然慢。

## 4. MLA：latent、权重吸收与 RoPE 的适用范围

分片 003 / P010 的原文是：“把这个 latent 的 latent 给保存到我们的 cache 中”。这一说法抓住了 KV 共同低秩表示的核心。概念上可以先重建 K/V 再做注意力；优化推理则可以利用矩阵乘法结合律避免逐次显式重建。例如对内容分支：

```text
k_j = W_UK c_j
q_t^T k_j = (W_UK^T q_t)^T c_j
```

V 的上投影也可以与后续输出投影组织在一起。这是“能用朴素计算说明原理”和“已讲清优化推理路径”的区别；不能把录音中的重建式说明直接判为数学错误，也不能补写成现场已经推导了权重吸收。[DeepSeek-V2 §2.1.2 与附录 C](https://arxiv.org/html/2405.04434v5)

**带解耦 RoPE 的 DeepSeek-V2：** 历史缓存还需保存独立的位置 key 分量，不能只数内容 latent。旋转矩阵依赖位置，与一般投影矩阵不能随意交换，因此不能把 RoPE 无条件挪到投影前完成。[DeepSeek-V2 §2.1.3](https://arxiv.org/html/2405.04434v5)

**本场提及的 GLM-5.3-Flash：** 官方配置 `mla_use_nope=true`、`qk_rope_head_dim=0`，文本 MLA 分支不走上述位置分量。这并不意味着整个模型没有顺序信息，也不表示运行时只有 latent 一类存储；混合模型仍涉及 KDA 状态、稀疏检索索引及其他元数据。[官方配置](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/46a050bec13002ad29ee795c16e61cf4fa3c4a9c/config.json)、[vLLM MLA / indexer 实现](https://github.com/vllm-project/vllm/blob/main/vllm/models/glm5next/common/attention.py)

分片 003 / P011 的回答原文是：“我默认旋转位置编码在在前面就已经做好了”。这句话不足以说明采用哪种 MLA，通用表述需要修正为“先确认具体模型是否使用 RoPE，再展开对应分支”。但不能评价为“GLM-5.3-Flash 的实际实现必须补上 RoPE”。[00:15:25 现场笔记](/root/workspace/learning/daily-work/work/managed/interview-video-analysis/derived/interview-biren-recording-01.frame-15m25s.notes-crop.png)也只是简写，不能单凭未写缩放项或 mask 判断口头理解错误。

## 5. Q 不缓存与 Q 不压缩是两回事

分片 003 / P011：“Q 并没有，我记得并没有进行一个压缩”。历史自回归 cache 通常不保存过去的 Q，但这不排除当前 Q 采用低秩投影。GLM-5.3-Flash 的 `q_lora_rank=1536` 及实现中的 Q 下投影／归一化／上投影路径可直接核查。[官方配置](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/46a050bec13002ad29ee795c16e61cf4fa3c4a9c/config.json)、[vLLM Q 投影实现](https://github.com/vllm-project/vllm/blob/main/vllm/models/glm5next/common/attention.py)

也不应反向概括为所有 MLA 变体都压缩 Q；DeepSeek-V2-Lite 就是论文给出的不压缩 Q 的变体。这里适合指出**具体模型的 Q 投影路径没有讲准确**，而不是根据一条通用口号打分。[DeepSeek-V2 附录 B](https://arxiv.org/html/2405.04434v5)

## 6. TP / DP / EP 与峰值显存

分片 004 / P013–P015、分片 005 / P017–P018 给出了 TP8、TP4+DP2、dispatch/combine 及缓冲区的讨论。当前 vLLM 中，启用 EP 是独立配置；启用时 EP group size 为 TP×DP，attention 在各 DP group 内按 TP 分片。**TP4+DP2 本身并不必然意味着必须开启 EP。** 用户后端的支持组合仍需以实际实现为准。[vLLM EP 部署文档](https://docs.vllm.ai/en/latest/serving/expert_parallel_deployment/)

只比较相同数量 rank、相同 dtype、无额外副本的专家权重时，TP 和 EP 都可能达到约 `总专家权重/R` 的每卡存储。峰值还取决于 token 路由不均衡、dispatch/combine buffer、中间激活、graph pool 与算子 workspace。因此“EP 永远更占显存”或“只看权重可断言峰值一样”都过强。现场提到低延迟模式为最坏接收量预留 buffer，方向合理；“几百兆到一个 G”仍是当事人回忆值，本次没有参数与分配日志可复算。[vLLM EP 后端说明](https://docs.vllm.ai/en/latest/serving/expert_parallel_deployment/)

P019 把 torus、NVLink、IP 放在同一比较中，适合补充层次：torus 描述拓扑，NVLink 描述 GPU 互连技术，AllReduce / All-to-All 描述通信操作。TPU 的邻接连接也不是“任意两卡都有一条物理直连”。这些区分能帮助解释方案，但不能靠公开架构资料核实自研机器的坏链路情况或具体通信耗时。[Google TPU v4 拓扑说明](https://docs.cloud.google.com/tpu/docs/v4)、[NVIDIA NVLink 说明](https://www.nvidia.com/en-us/data-center/nvlink/)

## 7. 缓存容量与 Graph padding

分片 005 / P020 的澄清：“并并不是那个其实没有真正的扩大，只是之前把错误的结果给纠正了”。因此应将“约三倍”归为**适配后容量核算结果得到纠正**，不能直接当作物理容量三倍增长或同配置吞吐三倍提升。`148762 tokens` 与前面 P015 口述的“一一百一百一百七十几K左右”应分别保留来源，不能自动合并成同一测量口径。

分片 006 / P022 的明确说法是“对Token维度的Padding”，随后讨论小 batch 逐个捕获及更大 bucket 到 256。不能将其改写为“对完整上下文长度补齐”。固定形状及地址的 graph replay 可以使用多个 token-count buckets；这与历史 KV 的序列长度是不同维度。自研设备 graph 的具体能力未验证，CUDA/PyTorch 文档只作为相应机制的公开参照。[NVIDIA PyTorch Graph 说明](https://docs.nvidia.com/dl-cuda-graph/latest/torch-cuda-graph/torch-integration.html)

## 8. 异步 D2H：物理空间、逻辑视图与完成条件

分片 006 / P024–P025 及分片 007 / P027 描述先在 device 侧转换布局，再搬运对齐后的较大物理块；逻辑结果只有 5 个 int32。公开原理上，**物理分配／传输字节数**与**逻辑 tensor 的元素数**确实需要区分。将 layout 转换提前放到设备端，可以减少 CPU 后处理依赖，但是否真正与下一轮执行重叠仍需时间线证据。

P027 已出现“先要做，要要做 wait event”，并提到 stream 同步后再消费，不能写成未考虑数据就绪。工程验证还应区分设备端流依赖和 CPU 读取前的完成等待，以及源临时张量、host buffer 的生命周期；`record_stream` 或等效事件／保活机制是可核查点，不是唯一实现。[PyTorch 异步拷贝说明](https://docs.pytorch.org/tutorials/intermediate/pinmem_nonblock.html)、[PyTorch `record_stream`](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.record_stream.html)

P027 同时说“我们直接 view 成一个比较小的张量”。若这里泛指共享 storage 的逻辑视图，方向可以成立；若特指把 128 元素的同 dtype tensor 直接 `view(5)`，则元素数不匹配。实际代码应明确采用切片、`narrow` 或受控的 storage-backed view。这是需要补充 API 精度的地方，不能在没有代码时断言实现一定错误。[PyTorch `Tensor.view`](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.view.html)

## 9. FlashAttention-2 的回答边界

分片 007 / P028–P031 提到了不落完整中间矩阵、online softmax 的最大值与求和更新、Q tile 遍历 K/V tile，并说计算仍是“O O N 方的”。这些内容与精确 Attention 的 IO 优化及主导复杂度仍为二次的方向相符。FA2 还改进了线程块／warp 工作划分并减少非矩阵乘 FLOPs，因此“实际计算完全没有减少”不宜作为严格结论。现场要求的是简单讲设计思路，不应把未展开每个 kernel 细节等同于答错。[FlashAttention-2 原论文](https://arxiv.org/abs/2307.08691)

## 验证范围与仍未证明的事项

- 上述主要短引文已用字符串包含检查与各片原始 `.text` 核对；这验证引用忠实，不验证语音识别绝对准确。字母名、精度和数值单位仍需谨慎。
- 公开模型配置采用 HF revision `46a050bec13002ad29ee795c16e61cf4fa3c4a9c`；vLLM 与框架文档为 2026-11-17 读取的上游实现，不等同于用户当时使用的版本。
- 未取得自研插件代码、启动参数、张量 dump、性能时间线、内存峰值记录或端到端测试结果，不确认具体加速倍数、内存收益与部署效果。
- 第 009 片音频时长与响应 `usage.seconds` 不一致，仅能说明计量字段与媒体时长不同；不能从该字段单独推断必然漏转某段，也不能声称尾段已逐字覆盖。
- 本次核查只读取本地文本／图片和公开官方资料，没有发起新的计费模型请求。
