---
archive_type: "study-log-visible-dialogue"
schema_version: 1
archive_id: "sl-f3fa9c63ec634cda9ce09db28725dd5a"
status: "final"
title: "W4a 单元一 · RadixAttention 与前缀缓存 · 可追溯可见文本对话"
provider: "codex"
project_name: "PlanA"
project_fingerprint: "c50d0de9b3ca"
source_session_id: "01a1f19b-aaaf-7800-9732-7f1c6b2dc2c8"
source_file: "study-log migration request"
start_message_id: "msg-5a15c1a1f15c088f2706"
end_message_id: "msg-bc65ad69a8744c23d85d"
message_count: 47
source_sha256: "1cbc3c0a379792426b53148ed208a9e3c011505fc3dd2d1169785ab26b9139d0"
visible_content_sha256: "f0ce10d6afe8a372d98272db04c29451cae14d96caab1c1e1c6b8ff2d2fadcbb"
target_precondition_sha256: null
first_message_at: "2026-11-23T02:08:02.775Z"
last_message_at: "2026-11-23T10:25:32.289Z"
created_at_utc: "2026-11-25T23:18:50.766849+00:00"
updated_at_utc: "2026-11-25T23:18:50.766849+00:00"
normalization: {"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"}
redaction: {"version":"study-log-redaction-v1","categories":["credential","personal"],"applications":[],"preserved_from_sources":true}
privacy_risks: {"categories":[],"counts":{}}
structured_record: "推理框架/log/2026-11-23-W4a-U1-RadixAttention与前缀缓存.md"
message_phases: [null,"commentary","final_answer",null,"commentary","final_answer",null,"commentary","commentary","final_answer",null,"commentary","final_answer",null,"commentary","commentary","final_answer",null,"commentary","commentary","final_answer",null,"commentary",null,"commentary","final_answer",null,"final_answer",null,"commentary","final_answer",null,"commentary","final_answer",null,"final_answer",null,"commentary","commentary","final_answer",null,"commentary","final_answer",null,"commentary","final_answer",null]
migration: {"schema":"study-log.migration/v1","preview_digest":"8562f721412bb8055515b9f6f670b5785619993069d44b1f2d80b47c1a0c4acf","request_sha256":"1cbc3c0a379792426b53148ed208a9e3c011505fc3dd2d1169785ab26b9139d0","segments":[{"source_id":"wa1-01","source_archive_id":"sl-097b021d6b384a50bd4f05d951f32f92","source_file":"/root/workspace/learning/PlanA/推理框架/log-raw/.sl-temp-0970553c78308edc-wa1-01.md","source_sha256":"1ad88721545fa6e7f37c65a360f37afbeae5310b2c9a37590e6db6d499209299","source_metadata":{"archive_type":"study-log-visible-dialogue","schema_version":1,"archive_id":"sl-097b021d6b384a50bd4f05d951f32f92","status":"final","title":"W4a 单元一 · RadixAttention 与前缀缓存 · 来源分段 1","provider":"codex","project_name":"PlanA","project_fingerprint":"c50d0de9b3ca","source_session_id":"01a1f19b-aaaf-7800-9732-7f1c6b2dc2c8","source_file":"rollout-2026-11-19T02-21-13-01a1f19b-aaaf-7800-9732-7f1c6b2dc2c8.jsonl","start_message_id":"msg-5a15c1a1f15c088f2706","end_message_id":"msg-341b0fcdbb7355ef384c","message_count":10,"source_sha256":"98b773f7a5d707c190a276013e01f1b76709438274cc13f0c509af8a0ca77eac","visible_content_sha256":"d9adf49eda6478ce20e6b5a48a2895d688991af6f22504cf23b8291d11337f6a","target_precondition_sha256":null,"first_message_at":"2026-11-23T02:08:02.775Z","last_message_at":"2026-11-23T02:54:24.292Z","created_at_utc":"2026-11-25T23:18:49.287106+00:00","updated_at_utc":"2026-11-25T23:18:49.287106+00:00","normalization":{"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"},"redaction":{"version":"study-log-redaction-v1","categories":["credential","personal"],"applications":[]},"privacy_risks":{"categories":[],"counts":{}},"structured_record":"推理框架/log/.sl-temp-0970553c78308edc-wa1-01.md","message_phases":[null,"commentary","final_answer",null,"commentary","final_answer",null,"commentary","commentary","final_answer"],"migration":null},"start_message_id":"msg-5a15c1a1f15c088f2706","end_message_id":"msg-341b0fcdbb7355ef384c","message_count":10,"visible_content_sha256":"d9adf49eda6478ce20e6b5a48a2895d688991af6f22504cf23b8291d11337f6a"},{"source_id":"wa1-02","source_archive_id":"sl-aa70cc56972c49b183fc323161d3b450","source_file":"/root/workspace/learning/PlanA/推理框架/log-raw/.sl-temp-0970553c78308edc-wa1-02.md","source_sha256":"33be060e516497db0c36cea08a21fbf50673b73f1452aa298abd15a7e1ecabcd","source_metadata":{"archive_type":"study-log-visible-dialogue","schema_version":1,"archive_id":"sl-aa70cc56972c49b183fc323161d3b450","status":"final","title":"W4a 单元一 · RadixAttention 与前缀缓存 · 来源分段 2","provider":"codex","project_name":"PlanA","project_fingerprint":"c50d0de9b3ca","source_session_id":"01a1f19b-aaaf-7800-9732-7f1c6b2dc2c8","source_file":"rollout-2026-11-19T02-21-13-01a1f19b-aaaf-7800-9732-7f1c6b2dc2c8.jsonl","start_message_id":"msg-42a621793bf43193f5f8","end_message_id":"msg-bc65ad69a8744c23d85d","message_count":37,"source_sha256":"98b773f7a5d707c190a276013e01f1b76709438274cc13f0c509af8a0ca77eac","visible_content_sha256":"3bc31de52cb931547253654a157535a9934cad80095e543b0fe61507db5669cd","target_precondition_sha256":null,"first_message_at":"2026-11-23T03:54:28.411Z","last_message_at":"2026-11-23T10:25:32.289Z","created_at_utc":"2026-11-25T23:18:49.736942+00:00","updated_at_utc":"2026-11-25T23:18:49.736942+00:00","normalization":{"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"},"redaction":{"version":"study-log-redaction-v1","categories":["credential","personal"],"applications":[]},"privacy_risks":{"categories":[],"counts":{}},"structured_record":"推理框架/log/.sl-temp-0970553c78308edc-wa1-02.md","message_phases":[null,"commentary","final_answer",null,"commentary","commentary","final_answer",null,"commentary","commentary","final_answer",null,"commentary",null,"commentary","final_answer",null,"final_answer",null,"commentary","final_answer",null,"commentary","final_answer",null,"final_answer",null,"commentary","commentary","final_answer",null,"commentary","final_answer",null,"commentary","final_answer",null],"migration":null},"start_message_id":"msg-42a621793bf43193f5f8","end_message_id":"msg-bc65ad69a8744c23d85d","message_count":37,"visible_content_sha256":"3bc31de52cb931547253654a157535a9934cad80095e543b0fe61507db5669cd"}]}
---

# W4a 单元一 · RadixAttention 与前缀缓存 · 可追溯可见文本对话

> 此文件是规则化提取的“可追溯可见文本对话”，不是完整客户端 Session，也不代表已经匿名化。
> system、developer、reasoning、工具事件、客户端注入和附件正文默认不包含在内。

结构化学习记录：[查看记录](<../log/2026-11-23-W4a-U1-RadixAttention与前缀缓存.md>)

---

**001 · 用户** · `2026-11-23T02:08:02.775Z` · `msg-5a15c1a1f15c088f2706`

好的，那我们开始 W4a 吧。先看一下 SGLang 与推测解码这周要学哪些内容，具体怎么分单元？

---

**002 · 助手 / 过程更新** · `2026-11-23T02:08:07.503Z` · `msg-6621d5099e54ed6914f1`

我会先对照冲刺计划和上一周的学习断点，把 W4a 要掌握的内容、每个单元要回答的问题，以及它们和已有 vLLM 基础的关系排清楚。

---

**003 · 助手 / 正式回答** · `2026-11-23T02:14:02.883Z` · `msg-b430980f5976ba572639`

**W4a 已开始。建议分成五个单元：前三个学 SGLang 怎么处理请求，后两个学推测解码为什么可能更快，以及代码里怎样实现。** [W4a 学习路线与源码入口](/root/workspace/learning/PlanA/计划/八周冲刺进度/W4a.md:13)

前三个单元用同一个例子串起来。假设两个请求共用一段很长的系统提示词，各自问不同的问题，都要求用指定格式的 JSON 回答。我们依次看三件事：**哪些输入可以少算、哪个请求能先算、输出时哪些 token 可以选。**

| 单元 | 具体学什么 |
|---|---|
| **1 · RadixAttention 与前缀缓存** | 第二个请求到达时，SGLang 怎样找到已经算过的最长前缀，复用对应的 KV？两个请求先后结束时，哪些缓存还能保留，哪些可以淘汰？最后和你熟悉的 vLLM 按块缓存前缀作对照。 |
| **2 · SGLang 调度与组批** | 已有请求正在 decode，这时又来了一条长提示词。沿一次真实调度看等待队列、KV 空间、token 预算和分块 prefill 怎样决定下一批跑什么。这里接上 W4：同一个决定，可能让新请求更早看到首字，也可能让已有请求更久才看到下一个 token。 |
| **3 · 结构化输出** | 假设 JSON 的某个字段只允许几个固定值。看框架怎样根据已经生成的内容算出合法 token，在采样前屏蔽其余候选，再随新 token 更新语法状态。性能上重点区分**首次编译规则的开销**和**每一步应用约束的开销**。 |
| **4 · 推测解码的正确性与收益** | 分两段学。先跟一轮短草稿，看目标模型怎样验证、遇到拒绝怎样补采样，以及为什么随机生成仍能保持目标模型的分布。再用“一轮花了多久、最终交付几个 token”推导加速比，解释为什么接受率高也可能变慢。[推测解码原始论文](https://proceedings.mlr.press/v202/leviathan23a.html) |
| **5 · 从推测解码源码到 DeepSeek MTP** | 沿 vLLM V1 的一条路径找到谁提出草稿、谁验证、接受结果怎样写回请求。再看 DeepSeek 的多 token 预测（MTP）：训练时各模块学习预测哪个未来位置，推理时怎样用它们生成草稿，以及它和独立小草稿模型各要付出什么成本。[DeepSeek-V3 技术报告 §2.2](https://arxiv.org/html/2412.19437v2#S2.SS2) |

**这周学到什么程度算完成？** SGLang 的三个机制，你都能指到固定版本的源码，并在换一个请求条件后预测行为。推测解码部分，你能讲清为什么保持分布、举出一个实际不会加速的反例，再沿代码说明 MTP 产生的候选怎样被验证。开头可以直接用本地源码和纸面推导推进。[整周验收标准](/root/workspace/learning/PlanA/计划/八周冲刺进度/W4a.md:25)

我们从单元一开始。第一个场景就是：**请求 A 已经算完一段长系统提示词。请求 B 带着相同提示词和一个新问题到来，SGLang 怎么知道它可以从哪里接着算？**

---

**004 · 用户** · `2026-11-23T02:22:01.912Z` · `msg-fe3e3a416bf8c949ef92`

最后一个单元到GLM5.3-flash的mtp吧。正好衔接上之前的项目。

---

**005 · 助手 / 过程更新** · `2026-11-23T02:22:07.952Z` · `msg-920e9c7e61b7a53e6d13`

我会把第五单元改成以 GLM-5.3-Flash 的 MTP 收尾，并核对项目里当时跳过了哪些权重、公开源码能接着追到哪一步。

---

**006 · 助手 / 正式回答** · `2026-11-23T02:27:56.898Z` · `msg-01437fbda2927b7fb883`

第五单元已改为 **「从权重加载到 GLM-5.3-Flash 的 MTP」**，并同步更新了冲刺计划。DeepSeek-V3 留作理解 MTP 训练目标的简短对照。[第五单元安排](/root/workspace/learning/PlanA/计划/八周冲刺进度/W4a.md:23)

这节课会从你亲手做过的权重审计讲起。你当时交付的文本推理版本未启用 MTP，因此加载时明确跳过了 **889 个 MTP 权重键**。到单元五，我们会从公开模型里选一条具体权重，追清三个问题：它在前向计算的哪一步用到？MTP 怎样用当前 token 的 embedding 和上一步的隐藏状态提出候选？目标模型验证后，哪些 token 可以提交给用户？[项目权重审计记录](/root/workspace/learning/PlanA/面试准备/自我准备/projects/GLM5-3-flash-project.md:55) · [vLLM 的 GLM MTP 实现](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/models/glm5next/common/mtp.py#L80)

---

**007 · 用户** · `2026-11-23T02:32:12.170Z` · `msg-6659bf48001f49fbeb97`

好的，那就按这五个单元来。我们开始 W4a 单元一吧，还是用讲解页，从两个请求共享同一段提示词的例子讲起。

---

**008 · 助手 / 过程更新** · `2026-11-23T02:32:17.648Z` · `msg-c2c76bd92df2a4d0ace7`

我会按这五个单元推进，先做单元一的讲解页。开场就用两个请求逐个对齐 token，看看第二个请求在哪个位置分叉，以及它能复用哪些已经算好的 KV。

---

**009 · 助手 / 过程更新** · `2026-11-23T02:41:13.487Z` · `msg-f91109f4505c5b7ca260`

我用 W4 实验里的同版 Qwen 分词器实际拆了两条消息。两条请求都以“请简答。”开头，第一处不同出现在第 13 个 token。图里会把前 12 个位置展开，让你看清为什么聊天模板里的角色标记也算进了共享前缀。

---

**010 · 助手 / 正式回答** · `2026-11-23T02:54:24.292Z` · `msg-341b0fcdbb7355ef384c`

**W4a 单元一「RadixAttention 与前缀缓存」已开课。** 导入和前两个节点约 7 分钟。[打开单元一讲解页](/root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html)

A 问“吞吐是什么？”，B 问“延迟是什么？”，系统提示词都是“请简答。”。先看图 1.1：按实际分词结果，两条输入的前 12 个 token 相同，第 13 个才分叉。再到图 2.1 切换“A 的 KV 仍在”和“缓存为空”，看看 B 从哪里开始做新的前向计算，以及它仍要读取哪些历史 KV。

**检查 1（迁移）**  
沿用图中的设置，缓存里只有 A 的路径。请求 C 与 A 等长，只有第 5 个位置的 token ID 不同。有人建议只重算第 5 个位置，后面继续用 A 的 KV。你会怎样划定 C 的复用边界？为什么？

---

**011 · 用户** · `2026-11-23T03:54:28.411Z` · `msg-42a621793bf43193f5f8`

检查题：我觉得 C 只能复用 A 前 4 个位置的 KV。从第 5 个位置开始，两条请求的前缀就不同了。后面的 token 即使 ID 和位置都相同，做注意力计算时看到的上文也变了，所以从第 5 个位置起都要重新做前向。

---

**012 · 助手 / 过程更新** · `2026-11-23T03:54:40.156Z` · `msg-6deb9d84918119eae27e`

你的边界划得对。C 可以复用前 4 个位置；从第 5 个位置起，上文已经分叉，后续各层的 KV 也可能随之改变。我会把这道题的参考要点补进讲解页，再沿同一个例子看 A 结束后，这些槽位什么时候才能回收。

---

**013 · 助手 / 正式回答** · `2026-11-23T04:04:44.578Z` · `msg-1458eba7454e117950e8`

**检查 1 通过。** C 可以复用 A 第 1–4 个位置的 KV，从第 5 个位置起重新做前向。你说清了原因：后面的 token 即使 ID 和位置相同，注意力能读到的上文已经改变，更深层的 K、V 也可能不同。

接着读节点 3「A 已经结束了，为什么 B 还能读到它的 KV？」，约 3 分钟。图 3.1 沿着同一批槽位，看 A 结束、B 开始使用共享前缀、显存吃紧时各发生了什么。[打开单元一讲解页](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#node-3>)

**检查 2（判断）**  
B 和 D 各持有一份共享前缀的引用。如果要腾出 KV 槽位，B 结束而 D 仍在生成时，能回收共享前缀吗？两者都结束后，若前缀下面还挂着一个驻留的后缀叶节点，又该先回收哪一段？为什么？

---

**014 · 用户** · `2026-11-23T04:04:47.616Z` · `msg-724e850015bd22fb4962`

本次课程学习有背景和引入缺陷。本单元是本次week的第一个单元，需要在讲解页中先阐明整个week的安排和学习项目。然后本单元刚开始，也要整体讲述一下全流程脉络，而不是直接进入了细节。比如本单元是**RadixAttention 与前缀缓存，那么讲解页中还应该先讲述RadixAttention的整体思想，然后再引入具体代码实践，提出实践中的细节问题，然后根据这些细节问题作为一个个学习节点进行细节上的学习。**

---

**015 · 助手 / 过程更新** · `2026-11-23T04:04:55.538Z` · `msg-cbd0234dd23407c5abbc`

我会把讲解页开头重新组织成三个层次：先看 W4a 五个单元怎样衔接，再用两个请求讲清 RadixAttention 的整体思想和完整流程，最后把流程中自然出现的问题对应到具体学习节点。

---

**016 · 助手 / 过程更新** · `2026-11-23T04:20:12.538Z` · `msg-a3071f05b5c2b5cb67c3`

原页虽然有一张路线图，但把“对照 vLLM”也画成了流程的一站，容易让人分不清服务实际做了什么、读源码时要比较什么。新版会分别呈现请求的运行流程和本单元的源码问题。

---

**017 · 助手 / 正式回答** · `2026-11-23T04:38:12.255Z` · `msg-3d866487db4750f4b1ed`

原页过早进入了 token 对齐和槽位索引，漏掉了两个更早的问题：W4a 整周要解决什么，以及 RadixAttention 为什么值得用。**我已重写单元一讲解页的开头。** [从新版周导览开始读](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#w4a-overview>)

现在按三个层次展开：

1. **先看整周。** 用两个学习项目串起五个单元：先追两条 SGLang 请求怎样复用前缀、进入批次并生成符合格式的回答，再追一轮推测解码，最后接回你的 GLM-5.3-Flash MTP 项目。
2. **再看单元全貌。** 从“A 已经算过共同开头，为什么 B 可以沿用”讲起，解释显存里的 KV 池存什么、前缀树索引什么，再完整走一遍 A 留下 KV、B 查找并取得引用、B 计算后缀、请求结束后槽位如何回收。
3. **最后进入代码。** 用 SGLang 的模拟缓存接口登记 A、查询 B，再从代码中引出每个节点的问题：输入在哪里分叉、查询返回什么、B 从哪里继续计算、谁还在使用缓存，以及 vLLM 按块查找时会有什么不同。

这个开篇顺序也写进了 [W4a 学习安排](/root/workspace/learning/PlanA/计划/八周冲刺进度/W4a.md:19)，后续单元会先把机制和流程讲完整，再进入实现细节。

---

**018 · 用户** · `2026-11-23T05:23:28.851Z` · `msg-0b710681751f0445d29a`

检查题：我觉得 B 结束时，共享前缀的引用数从 2 降到 1，D 还在用这段 KV，所以不能回收。等 D 也结束后，引用数虽然降到了 0，但前缀下面还有驻留的后缀叶节点。要腾出空间，应该先淘汰这个叶节点，否则后缀就失去了完整的前缀路径。如果还需要空间，而且共享前缀已经没有其他驻留子节点，这时才可以回收它。

---

**019 · 助手 / 过程更新** · `2026-11-23T05:23:40.418Z` · `msg-ec7bdf1ce9e5d25d8f54`

你把两个时刻都判断对了。尤其是“如果还需要空间”这句很重要：最后一个驻留子节点被删掉后，共享前缀才可能被选中，缓存仍然可以把它留给下一条请求。我会把这道题的参考要点补进讲解页，再用同一对请求对照 vLLM 的按块复用。

---

**020 · 助手 / 过程更新** · `2026-11-23T05:31:19.905Z` · `msg-59314966c2a4b5c3b6d9`

同一对请求放进三种配置后，差别就看得见了。前 12 个 token 都相同，SGLang 每页 1 个 token 时能复用这 12 个位置。把 SGLang 也改成每页 16 个，结果就和 vLLM 按 16 个 token 整块查找一样，第一页已经分叉，两边都得从头算。讲解页把这三行放在了一起。

---

**021 · 助手 / 正式回答** · `2026-11-23T05:32:05.068Z` · `msg-8615aed253427fee53ff`

**检查 2 通过。** B 结束时，引用数从 2 降到 1，D 做注意力计算还要读这段 KV。D 也结束后，引用数降到 0，但驻留的后缀仍依赖这条前缀路径。你说的“如果还需要空间”很准确：淘汰最后一个驻留子节点后，共享前缀才成为回收候选。如果槽位已经够用，它就可以留给下一条请求。

接下来沿同一对请求看一个区别：两条输入明明共享前 12 个 token，为什么一种配置能复用全部 12 个，另一种却要从头算？[单元一讲解页 · 节点 4，约 3 分钟](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#node-4>)

**检查 3**

两条新请求各有 49 个输入 token，只有第 20 个位置的 ID 不同。缓存里只有第一条请求留下的 KV。SGLang 每页 1 个 token，vLLM 每块 16 个 token，按整块查找。第二条请求在两边各能复用前多少个位置？第 33–48 个位置的 ID 都相同，vLLM 能单独复用这块 KV 吗？请用块哈希说明理由。

---

**022 · 用户** · `2026-11-23T05:53:40.881Z` · `msg-72d6feb01e33dee595d7`

检查题：我觉得 SGLang 可以复用前 19 个位置，因为每页只有一个 token，到第 20 个位置才分叉。vLLM 只能复用前 16 个位置，第 20 个 token 变了，第二块就不能命中。第 33–48 个位置虽然 ID 都相同，但第三块的哈希还取决于第二块的哈希，上文已经变了，所以第三块的 KV 也不能单独复用。

---

**023 · 助手 / 过程更新** · `2026-11-23T05:53:45.713Z` · `msg-9e883c4cc62a954d2fdf`

检查 3 通过。你把第 20 个位置的变化一直追到了第三块的哈希，这就解释了为什么第 33–48 个位置的 ID 全部相同，仍要重新计算。我会把这道题的参考回答补回讲解页，再沿 A、B 两条请求把单元一的流程串起来。

---

**024 · 用户** · `2026-11-23T05:55:07.701Z` · `msg-525688278c71a4b06094`

我有一个问题，既然vllm和sglang都可以设置每块/每页的token大小，从而做到细粒度的匹配命中，那二者的区别到底在哪呢？

---

**025 · 助手 / 过程更新** · `2026-11-23T05:55:31.500Z` · `msg-2d7981ce97ed68d44e72`

把匹配粒度设成一样，在同一段 KV 仍驻留的前提下，两边确实可以命中同样长的前缀。上一节的“12 对 0”说明的是粒度的影响。SGLang 和 vLLM 真正不同的地方，要看它们怎样记住这段前缀，以及请求结束后怎样回收它。我会把这个同粒度的对照补到节点 4。

---

**026 · 助手 / 正式回答** · `2026-11-23T06:02:07.423Z` · `msg-4473db0965cf4df80c4d`

**同样的命中粒度下，两者可以复用完全相同的 KV。** 你在检查题里答的 19 和 16 都对。现在只改一个条件，让 SGLang 也每页放 16 个 token。第 20 个位置发生分叉，两边就都只能复用前 16 个位置。区别要看它们**怎样找到这 16 个位置，以及之后怎样管理它们**。

- **SGLang 把共享关系存在一棵压缩前缀树里。** A 跑完时，连续三页可以合在一个树节点里。B 到来后，树发现只有第一页能共享，就在第一页末尾拆开节点。A、B 共用前面一段，后缀各走一条分支。拆开的是索引，显存里的 KV 留在原槽位。有了这棵树，调度器还可以沿分支统计哪些等待请求共享同一段上文。[SGLang 的查找与节点拆分](https://github.com/sgl-project/sglang/blob/29481685462732237d80d86076d6563e1f658102/python/sglang/srt/mem_cache/radix_cache.py#L648-L687)
- **vLLM 把上文编码进每个块的哈希。** B 用第一块的哈希查表，就能拿到 A 留下的物理块。到了第二块，token ID 变了，哈希随之改变，查找就在这里停下。就像你解释的，即使第三块的 ID 全都相同，它继承的第二块哈希也已经不同了。[vLLM 的前缀缓存设计](https://docs.vllm.ai/en/latest/design/prefix_caching/)

**回收时，这个区别尤其直观。** 假设两条请求都已结束，SGLang 选中的后缀叶节点恰好包含两页，就会一次归还 32 个位置。vLLM 按物理块维护引用和空闲队列，新请求只缺一块时，可以只取走一个 16-token 块。两边的命中长度一样，管理和回收 KV 的单位仍然可以不同。

我把这个同粒度的例子画进了讲解页，可以并排看同一对请求怎样形成树上的两条分支、哈希表里的两串键。[节点 4 补充 · 同样按 16 个 token 查找，区别在哪？](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#add-4-1>)

---

**027 · 用户** · `2026-11-23T07:16:14.841Z` · `msg-2bfd6e529ab371728ab8`

所以SGLang的命中匹配是通过树结构的查找进行的，而vLLM则将前文全部编码进每块的哈希，全部通过哈希查找。是吗？

---

**028 · 助手 / 正式回答** · `2026-11-23T07:16:49.383Z` · `msg-55ef2fd4945ae44f4b78`

对。**SGLang 沿前缀树匹配 token，vLLM 沿块哈希链查找缓存。**

- **SGLang** 从树根出发，用下一页的 token ID 在字典里找到子节点，再比较节点里保存的那一段 ID。共同上文就体现在两条请求走过的同一段树路径上。
- **vLLM** 把前一块的哈希、本块的 token ID 和附加信息一起算成新哈希。前一块的哈希已经包含了更早各块的信息，所以算第三块时，只要带上第二块的哈希，上文的变化就会传递过来。

你说的“全部通过哈希查找”，准确地说，是**用哈希定位每个已缓存的物理块**。在刚才按整块匹配的配置下，vLLM 仍要从第一块开始逐块查，遇到第一个未命中块就停。

---

**029 · 用户** · `2026-11-23T07:27:13.851Z` · `msg-173f3e6da62445053eaa`

明白，这是一个很重要的区别。然后第二个，空间不够用，要回收一部分时，SGLang优先回收叶子节点的缓存页。那么vLLM的优先回收逻辑是怎样的？vLLM先回收怎样的块呢？

---

**030 · 助手 / 过程更新** · `2026-11-23T07:27:46.705Z` · `msg-23c3a37bb6d375056e60`

vLLM 从空闲队列的头部取块。我会对照课上用的版本，核实哪些块排在队头，以及同一条请求的多个块一起释放时，前缀和后缀谁排在前面。

---

**031 · 助手 / 正式回答** · `2026-11-23T07:28:59.870Z` · `msg-387ed6d31a30bead0b90`

在课上这版 vLLM V1 里，**先用没有缓存哈希的空闲块；需要淘汰已经缓存的 KV 时，从空闲队列头部取最早闲下来、期间没有被再次命中的块。** 仍有请求引用的块继续保留。一个已缓存块的引用数降到 0 后，旧 KV 仍可命中，直到分配器取走该块、删除旧哈希。[vLLM 的块分配与空闲队列](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/block_pool.py#L647-L740)

**如果同一条请求同时释放多个已缓存块，后缀块先于前缀块进入队尾。** 道理和你刚才讲的哈希链有关。新请求想复用越靠后的块，需要相同的上文就越长。把靠前的块多留一会儿，其他请求还有机会复用它。[vLLM 的逆序释放逻辑](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/single_type_kv_cache_manager.py#L495-L503)

沿用每块 16 个 token 的例子。假设 A 有 49 个输入位置，B 仍在用 A 的第一块。A 结束前，空闲队列里只有一个更早闲下来的已缓存块 `X`。A 结束后，新请求取块的顺序是：

**只装了第 49 位的尾块 → X → A 的第 33–48 位 → A 的第 17–32 位。**

尾块还没填满，在整块查找的配置下没有缓存哈希，所以排最前。`X` 比 A 的两个完整后缀块更早闲下来，所以排在它们前面。第 1–16 位仍由 B 引用，根本不会进队列。

所以两边“先收后缀”的含义有个区别。**SGLang 用叶节点条件决定谁有资格被淘汰；vLLM 用空闲队列决定先取谁，同一请求一起释放时才体现出后缀优先。**

---

**032 · 用户** · `2026-11-23T07:52:15.804Z` · `msg-35354295f13fccb1ee79`

噢，所以vLLM是通过一个空闲队列来判断的，再叠加尾块优先的机制是吧。SGLang应该也有类似的尾块优先机制吧

---

**033 · 助手 / 过程更新** · `2026-11-23T07:52:48.603Z` · `msg-d59d8349ee640f3baa3e`

同一条树路径上，SGLang 确实会先回收后缀。我核对一下这版实现里，多条分支都能回收时，它怎样选出第一个叶节点。

---

**034 · 助手 / 正式回答** · `2026-11-23T07:53:36.737Z` · `msg-77169f32b4ef4be459a4`

对，**在同一条分支上，SGLang 确实会先回收后缀。** 两个框架的“尾部优先”发生在不同环节。

- **vLLM 用它安排入队顺序。** 同一条请求同时释放多个已缓存块时，后面的块先进入空闲队列。需要分配空间时，仍从整个队列的头部取块。
- **SGLang 用树结构决定谁有资格回收。** 只要前缀下面还有驻留的子节点，前缀就得留着。可以回收的是没有活跃引用的叶节点。如果有多个这样的叶节点，这版 SGLang 默认用 LRU，先选最久没被访问的那个，选中后把该节点里的页一起归还。[叶节点回收逻辑](https://github.com/sgl-project/sglang/blob/29481685462732237d80d86076d6563e1f658102/python/sglang/srt/mem_cache/radix_cache.py#L566-L585) · [LRU 如何排序](https://github.com/sgl-project/sglang/blob/29481685462732237d80d86076d6563e1f658102/python/sglang/srt/mem_cache/evict_policy.py#L16-L18)

比如共享前缀 `P` 下面有两个无人使用的叶节点，A 的后缀占两页，B 的后缀占一页。**如果 B 更久没被访问，就先回收 B 的一页。** 此时 A 还挂在 `P` 下面，所以 `P` 继续保留。如果这一页已经够用，回收就到此为止。

---

**035 · 用户** · `2026-11-23T08:23:27.891Z` · `msg-b6c95fec3a197f8cf93b`

所以SGLang的尾页也就在叶子结点上是吗？所以回收时就直接回收整个叶子结点？

---

**036 · 助手 / 正式回答** · `2026-11-23T08:24:09.059Z` · `msg-97bef11b8900b4c592ac`

是的，**SGLang 选中一个可淘汰的叶节点后，会归还它记录的全部 KV 槽位，再从树上删除这个节点。** 一个压缩节点可以包含多页。

“尾页在叶子上”说的是**这条缓存分支的末尾**。某条请求的末尾也可能落在内部节点。比如 A 用了两页，B 复用 A 的前缀后又接了两页，缓存树可以长成这样：

`根 → [第 1、2 页] → [第 3、4 页]`

第 2 页是 A 的尾页，但它所在的节点已经有了子节点。假设两条请求都已结束，此时只缺一页，SGLang 会选中右边的叶节点，把**第 3、4 页一起回收**。左边的节点这时才成为新的叶节点，空间已经够用，它就继续留在缓存里。

---

**037 · 用户** · `2026-11-23T08:27:46.427Z` · `msg-cd462591545b478d5351`

明白，很好，以上这些vLLM和SGLang关于查找匹配和回收再利用上的区别，在prefix cache方面，我觉得是我们所需要关注的，请把以上对比与分析添加到讲解页面中。

---

**038 · 助手 / 过程更新** · `2026-11-23T08:28:06.594Z` · `msg-e2fbab7351f6f43f8c57`

我会把这些区别整理到单元一节点 4 的现有对照里。查找部分沿用“第 20 个 token 分叉”的例子，回收部分补上 vLLM 的空闲队列顺序，以及 SGLang 里“请求的尾页落在内部节点”的例子，方便你复习时把两套机制对起来。

---

**039 · 助手 / 过程更新** · `2026-11-23T08:35:40.417Z` · `msg-b3dae9800ec5c23a2549`

节点 4 现在有一张对照表，可以顺着一次请求看完匹配、释放引用、再次命中和回收。表下还保留了两个具体例子，一个解释为什么只缺一页却会收回两页，另一个列出 vLLM 实际取块的顺序。

---

**040 · 助手 / 正式回答** · `2026-11-23T08:36:09.575Z` · `msg-cba2804fbc2b514d7ec6`

已补进 W4a 单元一讲解页的节点 4，复习时可以直接看这两处：

- **查找与命中**用第 20 个 token 分叉的例子，说明在相同粒度下，两边为什么能命中同样长的前缀，以及 SGLang 怎样沿树找到槽位、vLLM 怎样沿块哈希链找到物理块。[查看查找示意图](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#add-4-1>)
- **回收与再利用**把两种“尾部优先”放在一起对照。SGLang 先确定哪些叶节点可以回收，选中后整段归还。vLLM 从空闲队列头取块，同一请求同时释放多个缓存块时，后缀块先入队。表下还演示了引用归零后旧 KV 怎样再次命中。[查看对照表和两个回收例子](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#add-4-2>)

---

**041 · 用户** · `2026-11-23T09:13:28.443Z` · `msg-7efc44ddf8cc962b02bc`

接下来我们继续吧。

---

**042 · 助手 / 过程更新** · `2026-11-23T09:13:42.237Z` · `msg-5437c69c14d990080a13`

我们接着做单元一的综合口述。前面三道检查已经覆盖了前缀分叉、块哈希和回收顺序，这次换一个部署场景，请你判断缓存命中能不能让用户更早收到第一个 token。

---

**043 · 助手 / 正式回答** · `2026-11-23T09:17:19.517Z` · `msg-008902d7c156e8caaa31`

我们进入 W4a 单元一的综合口述。按面试时的口吻回答，讲一分钟左右，也可以直接写下来。[讲解页 · 综合题 1](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-a1>)

复习助手有甲、乙两台配置相同的单卡实例，模型都已预热，KV 缓存各自独立。一条流式请求的前 2,048 个 token 是讲义，末尾是用户的新问题。发给甲要排队，但轮到这条请求时，整段讲义的 KV 仍可复用。乙可以立刻处理，前缀缓存为空。

**为了让用户尽早收到第一个生成 token，你在什么条件下选甲，什么条件下选乙？** 请从两边各要算哪段输入讲起，再说说你会怎样验证自己的判断。

---

**044 · 用户** · `2026-11-23T09:25:13.715Z` · `msg-54c5b16e99f8024060c5`

对于甲，收到第一个token所需要的时间为排队时间 + 复用前2048个token的kv，计算末尾新问题输入的时间。对于乙，耗时则是需要从开头开始处理，要处理全部2048+末尾新问题所有token的时间。所以当排队时间短于处理前2048token的时间时，选用甲；当排队时间长于处理前2048token的时间时，选用乙。可以往甲和乙都发这条请求，看哪个服务先返回第一个生成token。

---

**045 · 助手 / 过程更新** · `2026-11-23T09:26:00.685Z` · `msg-050a835c8dcf09726e85`

这道综合题通过。你已经把甲的排队和两边各自要做的 prefill 算进去了。实际部署时，最可靠的分界线是“整条输入做 prefill”和“命中后只算新问题”这两次执行的耗时差。我会把这个口径和计时方法补到讲解页。

---

**046 · 助手 / 正式回答** · `2026-11-23T09:33:28.746Z` · `msg-937059fb9c285272a828`

**综合题通过。** 你的判断成立。假设采样和传输等其他耗时相近，甲的排队时间小于**乙处理完整输入的 prefill 耗时减去甲命中后处理新问题的 prefill 耗时**，就选甲。大于这个差值，就选乙。甲处理新问题时仍要读取讲义的 KV，所以用这两条路径的实际耗时差来估算收益，比单独计时那 2,048 个 token 更准确。

你提出向两台发送同一条请求，验证方法也对。客户端应分别从**各自发出请求**计到**收到第一个生成 token**，以毫秒比较 TTFT。复测时要恢复初始条件，尤其是乙跑过第一轮后已经缓存了讲义，下一轮要让它重新从空缓存开始。

前缀匹配、引用与回收、两种索引的对照，以及这道双实例取舍题都已通过。**W4a 单元一已达到结课条件，等你确认结课。** [讲解页 · 综合题参考口述](</root/workspace/learning/PlanA/课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-a1>)

---

**047 · 用户** · `2026-11-23T10:25:32.289Z` · `msg-bc65ad69a8744c23d85d`

好的，结课吧。接下来我们开始下一个单元。
