# W4a 学习验收记录

<a id="w4a-u1-prefix-check-20261123"></a>

### 单元一 · 前缀分叉后的 KV 复用（2026-11-23）

学习者在[检查 1](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-1)中独立判断 C 可以复用 A 的第 1–4 个位置，并解释了第 5 个 token 改变后，为何相同 ID、相同位置的后缀也要在新的上文中重新做前向。该变式通过，参考要点已放回原题。

随后沿 A、B 的例子讲到[保护引用与叶节点淘汰](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#node-3)。图中的槽位计数按 SGLang v0.5.17 设备端实现推演。[检查 2](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-2)已提出，待学习者说明两条请求先后结束时的回收条件。

<a id="w4a-u1-lifetime-check-20261123"></a>

### 单元一 · 保护引用与叶节点淘汰（2026-11-23）

学习者在[检查 2](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-2)中独立说明了 B 结束后 D 仍持有一份保护引用。D 也结束后，共享前缀还要等最后一个驻留子节点被淘汰才具备回收条件，是否继续回收取决于还缺多少槽位。引用与淘汰这一项目标通过。

<a id="w4a-u1-block-check-20261123"></a>

### 单元一 · 不同匹配粒度与块哈希（2026-11-23）

学习者在[检查 3](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-3)中独立判断了首次在第 20 个位置分叉时的复用边界。SGLang 每页 1 个 token 可复用前 19 个位置，vLLM 按 16 个 token 整块查找可复用前 16 个位置。学习者用第二块哈希的变化解释了第三块即使 ID 相同也无法单独命中。

学习者随后追问两种实现采用相同粒度时的区别。讲解页补上了[同粒度下的树、块哈希和回收方式](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#add-4-1)，并沿 A、B 的请求做了[单元串讲](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#synthesis)。

<a id="w4a-u1-routing-20261123"></a>

### 单元一 · 缓存命中与排队之间的取舍（2026-11-23）

学习者在[双实例综合题](../../../课程网页/八周计划/plana-jd-w4a-sglang-specdec.html#q-a1)中独立写明，甲排队后复用讲义的 2,048 个位置，乙可以立刻为整条输入做前向。学习者按排队代价与省下的前向时间选择实例，并提出向两台分别发同一请求、比较首个生成 token 的到达时间。这个新场景的书面技术验收通过。

反馈进一步明确，两条路径实际 prefill 耗时之差用于估算命中收益。复测时要分别记录客户端 TTFT，每轮恢复甲、乙各自的初始缓存和排队条件。

<a id="w4a-u1-final-mastery-20261123"></a>

**2026-11-23 最终结课结论。** 学习者确认 W4a 单元一「RadixAttention 与前缀缓存」结课，阶段登记为 `complete`。[前缀分叉](#w4a-u1-prefix-check-20261123)、[保护引用与淘汰](#w4a-u1-lifetime-check-20261123)、[两种索引的复用边界](#w4a-u1-block-check-20261123)和[缓存命中与排队取舍](#w4a-u1-routing-20261123)均已通过独立作答验收。

<a id="w4a-u2-opening-20261123"></a>

### 单元二 · 从运行批次追到本轮前向（2026-11-23）

学习者确认开始「SGLang 调度与组批」。[新讲解页](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#intro)先沿复习助手的一轮调度走完全流程，再对照 SGLang v0.5.17 的普通单卡循环，追 A 继续生成、B 分块读入提示词时的批次与输入位置。页面中的 token 数按源码和给定条件推演。[检查 1](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#q-1)已提出，待独立作答。

<a id="w4a-u2-admission-followup-20261125"></a>

**2026-11-25 请求名额与选批。** 学习者在检查 1 中认出了 prefill 优先的分支，但将仍在等待名额的 B 当作已经获准的请求。反馈沿准入和选批两步解释了这一轮为何由 A 做 decode。改用两个名额的[检查 2](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#q-2)复核独立判断。

<a id="w4a-u2-admission-check-20261125"></a>

**2026-11-25 准入复查通过。** 学习者在[两个名额的变式](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#q-2)中明确要核对 C 的请求是否结束、是否已退出运行批次并释放名额，据此判断 B 获准还是继续排队。反馈说明了 B 获准后先进入 prefill 批次，处理完提示词且还要生成时再并入运行批次。随后沿同一个长请求讲到[分块续算与混合组批](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#node-3)。

<a id="w4a-u2-mixed-output-followup-20261125"></a>

**2026-11-25 混合批次的输出归属。** 学习者在[检查 3](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#q-3)中识别出 A 的一枚 decode 输出，并提出查 `decoding_reqs` 核对 D 是否参与本轮。反馈区分了 B 轮前的输出长度和本轮处理最后一块后可能追加的首 token。[检查 4](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#q-4)用明确的输入区间复核这个时间点。

<a id="w4a-u2-mixed-output-check-20261125"></a>

**2026-11-25 输出归属复查通过。** 学习者在[检查 4](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#q-4)中根据第 800 位是提示词末尾，独立指出 B 的输出长度由 0 变为 1。A、D 各完成一步 decode，全批应追加 3 个 token，因此合计为 2 的日志与逐请求记录不符。

<a id="w4a-u2-comparison-gate-20261125"></a>

**2026-11-25 同负载调度对照通过。** 学习者在[综合题](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#q-a1)中解释，B 首次获准且只剩 500 个输入位置时，两边的 A 都生成 1 个 token。SGLang 的混合批次给 B 排入 496 个位置，vLLM 的分块 prefill 给 B 排入全部 500 个位置，B 只有在后一种配置中能于第一轮产出首 token。学习者提出在客户端比较 B 的 TTFT 和 A 的 ITL。此项按书面推演与测量方案验收，参考回答补充了两端的缓存初态和到达负载怎样对齐。

<a id="w4a-u2-final-mastery-20261125"></a>

**2026-11-25 最终结课结论。** 学习者补充讲解页后，确认 W4a 单元二「SGLang 调度与组批」结课，阶段登记为 `complete`。[请求准入与选批](#w4a-u2-admission-check-20261125)、[分块与混合批次的输出归属](#w4a-u2-mixed-output-check-20261125)和[同负载下两种调度器的取舍与验证方案](#w4a-u2-comparison-gate-20261125)均已通过验收。课后复习可直接查看[讲解页中的面试问题与口述回答](../../../课程网页/八周计划/plana-jd-w4a-sglang-scheduling.html#interview)。
