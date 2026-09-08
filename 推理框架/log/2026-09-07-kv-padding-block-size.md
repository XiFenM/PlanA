# 学习记录 · 2026-09-07 · KV padding、页大小接口与 block size 选型

> 来源：codex:`01a0511a-d5ac-7211-a2c1-d86facc92a61` · `msg-c1a47e0c719f53f1d467` → `msg-076759558532b7b2eda2`，共 20 条可见消息。
> 提取时 source SHA-256：`0b5fb867577223f8153566f8b48af4e2aa01465bbb0de048f770811eae273f4b`。
> 关联：[vLLM 执行链与扩展边界](../EP-PD自研芯片适配设计与验证包.md#lesson-plana-jd-w1-vllm-execution-boundaries)。
> 源码快照：[本地 vllm-cl](../references/vllm-cl)，提交 `4fd99a4f21d720347c6dec54253504f8321c0437`；与课程上游 vLLM 的 `568afb3` 基线分开。
> 记录范围：讨论中的问题、理解变化、源码定位和同事反馈。保留机制与来源，不复制底层公司源码、内部地址或未提供的测量数据；本记录不承担课程状态或 mastery。

## 学习过程

- [高价值问题] “假设有一种芯片，其中全局内存与片上缓存之间的访存必须要是512Bytes对齐的……会不会导致需要设置特定的block size？”——先明确约束作用于搬运起点、长度、行跨度还是整页；搬运单元不能直接换算成逻辑 Token block 的大小。（用户：`msg-c1a47e0c719f53f1d467`）

- [转折] 用户进一步明确“kernel的搬运单元就是512Bytes”，随后提供自己参与适配的插件仓库。讨论由假想布局转为核对实际规格、逻辑 shape、容量预算和 kernel 调用。此前的 64 KiB 页跨度只是手算条件，不作为该芯片的默认要求。（用户：`msg-0002a243c712b9bd9a11`、`msg-d57aacd95873791f0d90`）

- [要点] 插件按什么粒度计算 KV padding？——普通 Attention 的新增页预算属性按 head 尾维补齐：BF16 按 256 元素、FP32 按 128 元素，均对应 512 B。普通分离 K/V 的预算包含两份对齐后的 head 行；它不是统一把整页向上补到 64 KiB。（源码：[页大小补丁](../references/vllm-cl/vllm_cl/patch/patch_kv_cache_interface.py)，`_page_size_bytes_padded()`）

- [要点] BF16、head size 128 为什么能减少 padding？——在 block size 256 的合并布局中，每个 Token、每个 KV head 的 K 和 V 各占 256 B，拼成一个 512 B 行。源码的 shape 分支及 CPU 参考写入均能证明前半段放 K、后半段放 V；相对于两份分别补齐的方案，可避免额外的行 padding。这里是存储公式推导，不是性能实测。（源码：[Attention 布局](../references/vllm-cl/vllm_cl/attention/attention.py)，`get_kv_cache_shape()`；[读写参考](../references/vllm-cl/vllm_cl/_custom_ops.py)，`reshape_and_cache_cpu()`）

- [高价值问题] 为什么另增 `page_size_bytes_padded`，而不直接覆盖 `page_size_bytes`？——当前插件用前者计算物理容量预算，Runner 仍用后者将 `numel() × itemsize` 的逻辑元素字节数换算为块数，再重建 shape。只替换属性会混用两种单位。（用户：`msg-bc26a3782f509762ab6b`；源码：[容量计算](../references/vllm-cl/vllm_cl/patch/patch_kv_cache_utils.py)，`_get_kv_cache_config_from_groups()`；[Runner](../references/vllm-cl/vllm_cl/worker/dlc_model_runner.py)，`_reshape_kv_cache_tensors()`）

- [转折] 用 BF16、8 个 KV heads、D=96、B=256 检查消费者：逻辑页为 768 KiB，padding 预算为 2 MiB；8 个 blocks 对应的逻辑 tensor 字节数为 6 MiB。用原字段反推得到 8，若只把分母改成 2 MiB 则得到 3，后续 reshape 不一致。用户最终复述：“确实可以直接覆盖原本的`page_size_bytes`，但在其他代码逻辑处需要进行对应的重构调整。”（助手推导：`msg-93a31dac3ca78f4935d8`；用户：`msg-58ca01b5bb4a617507cc`）

- [要点] 统一页大小接口是否可行？——原则上可以让标准属性报告真实存储字节数，同时明确逻辑 shape 和每组块数的来源，并联动调整分配、reshape、stride 等消费者。双字段解释了当前实现的依赖，不证明它是唯一设计；本次没有实施或验证该重构。

- [高价值问题] 源码能证明为什么选择 256 Token 吗？——当前代码能证明平台默认值、普通 Attention backend 的支持列表，以及 K/V 合并布局绑定 256；源码与所查本地历史没有给出完整的硬件选型论证。另一条旧 paged-attention 封装存在非 256 的通用分支，也不能据此推断当前活跃 backend 全路径兼容其他大小。（源码：[平台配置](../references/vllm-cl/vllm_cl/platform.py)、[Attention backend](../references/vllm-cl/vllm_cl/attention/attention.py)、[底层调用封装](../references/vllm-cl/csrc/attention.cpp)）

- [转折] 用户向同事询问后补充：“kernel内部实际上也可以兼容其他大小的block size。但由于硬件矩阵乘单元的特性，设为256的大小可以使得计算效率最高，减少每次矩阵乘所需的访存读取次数。所以目前只设了256。”这补充了源码没有说明的设计原因：当前选型是性能考虑，不能表述为硬件只能处理 256 Token。（来源：用户 2026-09-07 转述同事反馈，`msg-58ca01b5bb4a617507cc`）

- [要点] 面试中如何限定这条结论？——可以说明“根据同事对当前 kernel 的设计说明，256 的选择用于匹配矩阵乘单元、减少访存读取次数”。“效率最高”保留为反馈原话，不扩大成所有模型／负载下的实测最优，也不据此声称本人完成了该参数选型或性能验证。512 B 的搬运／对齐粒度与 256 Token 的计算分块大小分别说明。

## 证据区分

| 信息 | 证据来源 | 可以支持的范围 |
|---|---|---|
| 两种页大小的消费者、K/V 合并条件、普通 backend 支持列表 | 固定提交源码静态核对 | 当前实现的字段用途、布局和调用约束 |
| 768 KiB、2 MiB、6 MiB 等数字 | 给定 shape／dtype 条件的算术推导 | 该例的逻辑字节数与代码预算，非设备分配水位 |
| 其他 block size 可被底层 kernel 处理；选择 256 是矩阵乘／访存效率考虑 | 用户向同事求证后的转述 | 当前实现的设计理由，尚无本轮 benchmark 数据 |
| 全模型吞吐、不同 workload 下最优 block size | 本轮没有实证 | 不作结论 |

## 遗留

- [遗留] 具体 TensorStorage padding、DMA 次数和片上 tiling 未在这份插件源码中展开；若后续需要细化机制，需相关底层源码或可披露的接口说明。（去向：获准的设备实现核验）
- [遗留] 若要开放其他 block size，需联动核对支持列表、K/V 合并条件、页大小计账、读写 kernel 和正确性／性能对照。（去向：后续明确授权的实现或实验）
