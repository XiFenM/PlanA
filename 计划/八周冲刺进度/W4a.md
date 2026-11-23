# W4a：SGLang 与推测解码

本周范围和验收依据见[八周冲刺计划 §9A](../高级AI框架开发工程师-八周证据冲刺计划.md#9a-w4asglang-与-speculative-decoding)，开周选材沿用[增强方案的 W4a 安排](../八周冲刺计划增强方案-AMD岗位.md#weekly-mapping)。

## 完成了什么

<a id="w4a-opening-20261123"></a>

2026-11-23 学习者开启 W4a，确认按下列五个单元推进。第五单元用自己的 GLM-5.3-Flash 项目衔接 MTP。同日开始[单元一](#w4a-u1-opening-20261123)，继续使用讲解页。

<a id="w4a-units-20261123"></a>

## 已确认的五个单元

前三个单元沿用同一批请求。两个请求共用一段长系统提示词，各自问不同的问题，都要求返回指定格式的 JSON。先追输入的 KV，再看两个请求怎样进批，最后看每一步输出怎样满足格式要求。第四单元用一段短草稿理解推测解码，第五单元回到 GLM-5.3-Flash，追一个 MTP 候选 token 怎样产生、怎样被验证。

| 单元 | 学习内容 | 面试时要能讲清的问题 |
| --- | --- | --- |
| 1 · [RadixAttention 与前缀缓存](#lesson-plana-jd-w4a-sglang-specdec) | 从第二个请求到达讲起。追 token 前缀匹配、已有 KV 的位置、仍需计算的后缀，以及节点引用计数与淘汰。与 vLLM 按块查找可复用前缀的方式对照。 | 两个请求共享一段提示词，第二个能省掉哪些计算？第一个请求结束后，谁还可能持有这段 KV，何时才能回收？ |
| 2 · SGLang 调度与组批 | 沿一步调度看等待队列、已有 decode 批次、KV 空间和 token 预算。追新请求的 prefill 如何获配，以及较长的输入如何分块推进，再与 vLLM 的同一场景对照。 | 已有请求正在出词，又来了一条长提示词。哪些工作能进入下一批？这会怎样影响新请求等首字和旧请求等下一个 token 的时间？ |
| 3 · 结构化输出 | 用一个带枚举字段的 JSON Schema，看语法如何编译、每条请求如何维护匹配状态、怎样在采样前屏蔽非法 token，以及采样后如何推进状态。分析首次编译与逐步应用 mask 各自的开销。 | 普通采样里分数最高的 token 此刻不符合语法，生成器怎样处理？多条请求复用同一套约束，可能省下哪部分工作？ |
| 4 · 推测解码的正确性与收益 | 先用短草稿走完一次提出、验证、接受或拒绝。分开讨论贪心解码与随机采样，推导草稿被拒绝后如何补采样以保持目标分布。再用每轮实际提交的 token 数、草稿成本和目标模型验证成本推导加速比。 | 一轮里前两个候选被接受，第三个被拒绝，最后能交付哪些 token？即使接受率高，在什么条件下仍会变慢？ |
| 5 · 从权重加载到 GLM-5.3-Flash 的 MTP | 从项目做权重映射时跳过的 MTP 权重入手。看公开实现如何组合 token 的 embedding 和上一步的隐藏状态，产生下一位置的候选，再追目标模型的验证、采样和请求状态更新。结合训练时预测的未来位置，比较 MTP 与独立草稿模型怎样提供候选。 | 当时交付的文本模型为什么可以跳过这些权重？如果启用 MTP，第一枚候选 token 从哪里来？候选被拒绝后，哪些结果能够提交？ |

<a id="w4a-unit-5-glm-mtp"></a>

### 单元五从项目里的哪一行开始

项目档案记载，当时在自研芯片上交付的是 GLM-5.3-Flash-Mix 文本推理路径，MTP 未启用。权重审计按规则跳过了 **889 个 MTP 权重键**。这是讲述自己做过的工作时可以引用的事实。[项目概览](../../面试准备/自我准备/projects/GLM5-3-flash-project.md#项目概览) · [权重映射与审计](../../面试准备/自我准备/projects/GLM5-3-flash-project.md#1-建立模型路径与权重映射)

项目的 vLLM 基线记为 `0.30.1rc0`，原权重的具体 revision 待核。课程选用公开的 `zai-org/GLM-5.3-Flash` 做源码对照。其固定配置列有 45 个主干层和 1 个 NextN 预测层。沿公开索引中的 `model.language_model.layers.45.eh_proj.weight`，可以在 vLLM 的 `load_weights` 中找到对应模块，再看它如何把归一化并拼接的 embedding 和隐藏状态投影回隐藏维度。最后接回第四单元的“提出草稿 → 目标模型验证 → 提交结果”。自研芯片启用 MTP 后的接受率和加速比留待实际测量。[公开配置](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/04c4e9e95c5da8862dced7e5056455116f83a7e0/config.json) · [同版公开权重索引](https://huggingface.co/zai-org/GLM-5.3-Flash/resolve/04c4e9e95c5da8862dced7e5056455116f83a7e0/model.safetensors.index.json)

## 凭什么算完成

- **SGLang 三个机制。** 前缀缓存、调度、结构化输出各对应固定版本的源码，各用一个新情境独立解释或预测。前缀缓存和调度还要在相同请求条件下说清与 vLLM 的实现差异和取舍。
- **推测解码的推导。** 能说明随机采样为何保持目标模型的输出分布，写清速度估算的假设，并举出接受率低或草稿太贵时无法获益的反例。
- **推测解码的实现。** 能从 GLM-5.3-Flash 的一条公开 MTP 权重追到草稿生成、目标模型验证和结果提交，说明 MTP 的训练目标与推理用途，以及它和独立草稿模型的差别。项目经历按已交付的范围陈述。

**本周与前课的连接。** 复用 [W3 的 KV 分页与生命周期](W3.md#w3-u2-final-mastery-20261106)和 [W4 单卡调度与 trace 判读](历史记录/W4-学习验收记录.md#w4-u2-final-mastery-20261112)。增强重点是把 W4 已测过的首 token 延迟、相邻输出间隔和吞吐放回新场景，判断某项改动可能省在哪一步。W4 的测量配置关闭了前缀缓存和推测解码。本周先用本地固定源码和纸面推导学习，实际性能结论随相应设备上的受控对照记录。开源贡献沿用此前的暂缓安排。

**随单元查阅的资料**

| 单元 | 固定来源 |
| --- | --- |
| 1–3 | SGLang v0.5.17（`2948168`）的 [RadixCache](https://github.com/sgl-project/sglang/blob/29481685462732237d80d86076d6563e1f658102/python/sglang/srt/mem_cache/radix_cache.py#L352)、[Scheduler](https://github.com/sgl-project/sglang/blob/29481685462732237d80d86076d6563e1f658102/python/sglang/srt/managers/scheduler.py#L2925)、[XGrammar 的 token 状态与 mask](https://github.com/sgl-project/sglang/blob/29481685462732237d80d86076d6563e1f658102/python/sglang/srt/constrained/xgrammar_backend.py#L92)。用 vLLM v0.26.0（`568afb3`）的[前缀块缓存](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/block_pool.py#L198)和[调度入口](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L425)对照。 |
| 4 | Leviathan 等人的[推测解码原始论文](https://proceedings.mlr.press/v202/leviathan23a.html)，用于随机接受、拒绝后的分布与速度模型。 |
| 5 | GLM 专题使用固定的公开 vLLM 提交 `d7ada3aace`。从 [MTP 权重加载](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/models/glm5next/common/mtp.py#L290)进入[预测层前向](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/models/glm5next/common/mtp.py#L80)和[草稿分数](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/models/glm5next/common/mtp.py#L176)。在同一提交追[候选生成](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/v1/worker/gpu_model_runner.py#L4743)、[使用目标模型 logits 验证采样](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/v1/worker/gpu_model_runner.py#L3454)与[请求状态更新](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/v1/core/sched/scheduler.py#L2110)。[DeepSeek-V3 技术报告 §2.2](https://arxiv.org/html/2412.19437v2#S2.SS2)作为 MTP 训练目标的原理对照。 |

<a id="lesson-plana-jd-w4a-sglang-specdec"></a>

### 单元一 · RadixAttention 与前缀缓存

- **Lesson ID** 为 `plana-jd-w4a-sglang-specdec`，单元一沿用本周原有候选标识。所属 Program 为[八周证据冲刺](../高级AI框架开发工程师-八周证据冲刺计划.md#program-plana-jd-ai-framework-4w)，阶段为 `teaching`。
- **讲解页**沿两个共享系统提示词的请求，串起输入、匹配、接续计算、引用与淘汰、vLLM 对照。[单元一讲解页](../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html)

| 目标 | 理解与源码依据 |
| --- | --- |
| `w4a-u1-o1-prefix` · 划定复用边界 | 对新请求独立判断哪些 token 位置能复用 KV，结合固定源码解释 token ID、已缓存槽位索引和本轮前向输入的关系。 |
| `w4a-u1-o2-lifetime` · 解释引用与淘汰 | 沿 SGLang 的引用计数和淘汰路径，在共享请求结束或显存吃紧时说明哪些位置仍受保护。 |
| `w4a-u1-o3-compare` · 比较前缀索引 | 对同一组请求和明确的分页条件，比较 SGLang 与 vLLM 的前缀复用粒度、代价与适用范围。 |

<a id="w4a-u1-opening-20261123"></a>

**2026-11-23 开课。** 已给出[两条请求的 token 对齐](../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#node-1)、[查到槽位后怎样计算后缀](../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#node-2)和[检查 1](../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-1)。用 W4 固定的 [Qwen 分词器与模板](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/989aa7980e4cf806f80c7fef2b1adb7bc71aa306)在 CPU 核得 A、B 分别有 21 和 20 个输入 token，前 12 个 ID 相同。缓存驻留与槽号属于教学设定，命中后的工作划分按 SGLang v0.5.17 源码推演。

## 还缺哪些没完成

单元一的理解判断随作答核对。其余单元按上表约定的范围验收。
