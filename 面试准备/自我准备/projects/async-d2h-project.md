## DLC 异步 D2H 实现与 vLLM 异步调度验证

- **时间**：2026-10-20 至 2026-11-02（目标 commit 的 author date 至本轮验证日期）
- **角色**：PyTorch 侧异步 D2H 实现作者 / DLC 运行时路径与 vLLM 调度适配分析
- **技术栈**：`PyTorch 2.5.0` DLC fork、`vLLM` V1、`vllm-cl`、DLC runtime（C/C++）、Python
- **涉及模型**：DLC 异步 D2H 通用机制；本轮端到端验证使用 Qwen3-32B、BF16、单机 TP4。
- **验证结论**：PyTorch 目标构建的 A/B/C 回归通过；Qwen3-32B 的 A/B 请求均成功完成。本轮 8 并发吞吐中位数提升约 3.0%，单并发下降约 8.2%，效果具有负载边界，详见[验证结果](#async-d2h-validation-20261102)。

### 项目背景

DLC 后端的 `tensor.to("cpu", non_blocking=True)` 长期并不真正异步。旧实现虽然把拷贝放在独立 stream 上，但 PyTorch 侧仍走同步 staging：先把 DLC 物理 padded storage 拷到 pinned CPU 临时区，再由 CPU `unpack`，最后 `copy_` 到用户输出。DLC runtime 还会对非 pinned 或非 512B 对齐的 D2H 强制 `isAsync=false`，所以 worker 主线程实际会卡在 D2H 的提交与完成上。

vLLM 的异步调度已经用 `AsyncScheduler`、独立 copy stream 和 event 做了“先调度下一批、后取上一批输出”的框架，但 DLC 后端的同步 D2H 把这层重叠能力吃掉了。目标分支 `fix/async-d2h-layout-kernel-1028` 在满足条件时使用异步 DMA，让采样 token 的回传能够先提交、后等待，为 worker 继续准备和提交下一批工作提供条件。实际重叠与端到端收益受调度和设备能力约束。

本项目以三个问题为主线：

1. PyTorch 侧具体如何把 D2H 做成真异步；
2. vLLM/vllm-cl 的实际 D2H 点位在哪里，下一批输入如何在没有 CPU token 的情况下准备好；
3. 这项优化可能带来什么收益，以及哪些路径仍然不受益。

### 职责

- **负责**：PyTorch DLC 后端异步 D2H 的方案实现、代码落地与回归测试，包括 padded pinned 输出、PyTorch 侧对 compat 算子和转 CPU 布局算子的调用与接口衔接、async DMA 提交、stream/host allocation 生命周期保护，以及 O2/O3 开关和回退路径。
- **参与**：DLC runtime 异步条件分析；vLLM/vllm-cl 实际 D2H 点位映射；`_prepare_inputs` 中上一 step GPU token 到下一 step 输入的依赖分析；收益与验证方案设计。本轮完成了 PyTorch 回归及 Qwen3-32B 的同构建 A/B 测试。
- **其他团队负责**：compat 算子与转 CPU 布局算子由算子团队负责；vLLM-cl 生产接入、DLC runtime/driver 的独立实现、生产端到端性能验收和对外发布口径。

### 关键行动

#### 1. 框架接入与机制实现

主要分为两个阶段步骤：

1. 实现异步 D2H fast path、512B padded pinned 输出，并接入算子团队提供的 device-side layout kernel。
2. 把异步 D2H 和 padded pinned 输出收紧到 `O3`；`O3` 仍为默认；把原先只在 O3 的 H2D copy-kernel 路径下沉到 O2；移除 device tensor keepalive；目标 tip 同时包含 `input_format(src)` 的 source-stride 修复。

**一次 `.to("cpu", non_blocking=True)` 的实际调用链：**

```text
to("cpu", non_blocking=True)
  -> _to_copy()
  -> 分配 padded pinned CPU output
  -> r.copy_(self, non_blocking=True)
  -> copy_through_cpu()
  -> handle_d2h_copy()
  -> try_device_layout_async_d2h()
  -> 调用算子团队的 compat/layout kernels
  -> synMemCopyAsync(D2H, padded_bytes)
  -> return（不等待 DMA 完成）
```

**1.1 输出先变成 padded pinned storage**

`pytorch/aten/src/ATen/native/TensorConversions.cpp:343` 只在 DLC、`non_blocking=True` 且 O3 时把 CPU 输出标记为 pinned。
`TensorConversions.cpp:354` 的 `empty_padded_dlc_d2h_output()` 会：

- 计算 `padded_bytes = ceil(logical_bytes / 512) * 512`；
- 分配 `at::empty({padded_numel}, pinned_memory=true)`；
- 用 `set_` 把逻辑 shape/stride 设回原来的 `self.sizes()/self.strides()`。

因此 `int32 [N,1]` 这类采样结果逻辑上仍是 `[N,1]`，但底层 storage 至少有 512B。DMA 按 padded bytes 写，不会越过分配边界；用户侧 `.tolist()` 只看到逻辑元素。

**1.2 只有满足条件才进入异步 fast path**

`pytorch/aten/src/ATen/native/dlc/Copy_cpu.h:787` 的 `can_use_device_layout_async_d2h()` 要求：

- source 是 DLC、连续、`storage_offset()==0`；
- destination 是 CPU、连续、非 view、唯一持有；
- destination 由 DLC CachingHostAllocator 分配；
- `dst.storage().nbytes() == aligned_d2h_bytes(src)`；
- dtype 在支持列表中；
- 未设置 `DLC_DISABLE_DEVICE_D2H_LAYOUT=1`。

不满足时，`Copy_cpu.h:958` 回退到旧的同步 `dlc_tensor_to_cpu_storage()` + CPU unpack。

**1.3 把 CPU unpack 搬到芯片上**

`Copy_cpu.h:818` 的 `try_device_layout_async_d2h()` 由 PyTorch 侧编排，具体 kernel 由算子团队提供：

1. `flat_view = src.reshape(-1)`，检查 `is_contiguous_dlc(flat_view)`；
2. 如果物理布局不是一行，调用算子团队提供的 compat 类算子（如 `custom_strided_get*`）压缩成一行；
3. 8/16/64-bit 再调用算子团队提供的 `custom_convert_to_cpu_layout_*` 转成 CPU 自然字节序；32-bit 已同序，不需要转换。

大于 16384 个元素时分块 compact，避免 strided-get 的输入窗口问题。`Copy_cpu.h:853` 使用 `kernel.input_format(src)` 而不是 `flat_view`，因为 `reshape` 只是 metadata view，不能消除物理 padding；`[N,1]` 这类采样结果正好需要原始 strides。

**1.4 最终只发一次对齐的 async DMA**

`Copy_cpu.h:920` 调用 `custom_device_memcpy(host, device, padded_bytes, D2H, stream, true)`。
`Copy_cpu.h:150` 在 `non_blocking=true` 时走 `synMemCopyAsync`，不会调用 `dlcStreamSynchronize`；旧路径传 `non_blocking=false`，是 `dlcMemcpyAsync` 后立即同步。

**1.5 runtime 为什么以前强制同步**

`DLCSynapse/synapse_core/synapse_state.cpp:1812` 计算：

```cpp
useRegularMemOrD2hMisaligned =
    (!isPinnedHugepageMem && !isDmabufMem && !dmaMappedIndex) ||
    (dmaSize != logicalSize && !toDevice);
```

只要 host 不是 pinned/DMA-mapped，或 D2H 的 `dmaSize != logicalSize`，runtime 就在 `:1820` 设置 `isAsync=false`，分配临时 host buffer，同步完成后再拷回用户 buffer。
新路径把 destination 变成 pinned，并把 DMA 大小变成 512B 整数倍，才真正满足 runtime 的 async 条件。

**1.6 生命周期保护**

函数返回后，`src`、`flat`、`dma_source` 这些局部 Tensor 可能被释放，但 DMA 还在队列里。`Copy_cpu.h:930` 对它们逐个调用 `DLCCachingAllocator::recordStream()`；host destination 则在 `:941` 通过 `CachingHostAllocator_recordEvent()` 记录到同一个 stream，防止 pinned buffer 被 allocator 提前回收。

因此 PyTorch 侧只保证“提交异步、完成有序”；调用方必须像 vLLM 一样等 event 或同步 stream，不能 `.to()` 后立刻读数据。

**1.7 O3 开关**

`pytorch/c10/dlc/DLCConstants.h:16` 统一解析 `DLC_SYN_COPY_ASYNC`：

- 未设置或未知值：O3；
- `O0/O1/O2`：不会启用异步 D2H；
- O3：开启 padded pinned 输出和异步 D2H。

该环境变量在每个进程内静态读取一次，必须在进程启动前设置。

#### 2. 精度对齐与数据正确性

正确性回归以 D2H 拷贝语义为对象；本轮 Qwen3 请求测试与性能数据不替代模型数值精度或生成内容一致性验证。

**2.1 逻辑 shape/stride 与物理 storage 分离**

在上述 fast path 及已测 contract 范围内，输出保留逻辑 shape/stride，额外 padding 位于 storage 尾部，逻辑元素数量和顺序不变。非连续输入、slice 和共享 destination 按适用条件回退；不将此结论推广为任意带间隙 stride 都可按逻辑元素数直接分配。

**2.2 布局转换的正确性**

旧路径由 CPU `unpack_dlc_transfer()` 完成 DLC padded layout 到普通 CPU layout 的转换。新路径由 PyTorch 侧调用算子团队提供的 compat/转 CPU 布局算子完成同样职责：

- 32-bit：DLC 物理元素顺序与 CPU 自然顺序一致，只做 compact；
- 8/16/64-bit：compact 后再做 `custom_convert_to_cpu_layout_*`；
- 大输入：分块 compact，避免单次 strided-get 窗口越界；
- 没有对应 compact kernel 的 dtype/形状：回退同步路径。

**2.3 已知风险点**

- `flat_view` 不能代替 `src` 作为 strided-get 的输入 descriptor；否则 padded `[N,1]/[N,4]` 可能拿到错误的一行 metadata，甚至挂住设备队列。
- 目标分支 tip 已用 `kernel.input_format(src)` 修复。
- destination 必须是唯一持有的 padded storage；共享大 buffer 的 slice/view 会被拒绝，防止对齐 DMA 覆盖逻辑尾部之外的数据。

**2.4 测试覆盖**

`pytorch/test/dlc_async_d2h_copy.py` 覆盖：

- `.to()` 返回后 event 仍 pending；
- padded pinned output；
- 连续、非连续、切片、转置；
- 不同 dtype/尾长度；
- 大输入分块；
- 多次 queued copy 的生命周期；
- source/flatten/layout temporary 提前释放；
- stream 依赖、Python dispatch、fallback error、H2D、DLC-to-DLC、autograd。

`test/dlc_async_d2h_copy.py:92` 的 `check_copy_is_deferred_to_event()` 是异步事件测试入口。本轮结合受控积压、提交耗时和完成后数据校验判断异步契约；单次 event pending 不能单独证明异步路径或实际计算重叠。A/B/C 的通过与跳过项见[验证结果](#async-d2h-validation-20261102)。

#### 3. vLLM/vllm-cl 异步调度适配分析

**3.1 实际生产路径是 vllm-cl 的 `DLCModelRunner`**

`vllm-cl/vllm_cl/worker/dlc_worker.py:301` 在非 V2 时选择 `DLCModelRunnerV1`。上游 `vllm/v1/worker/gpu_model_runner.py` 只是同构参考，不是 DLC 实际执行路径。

**3.2 AsyncScheduler 本身不做 D2H**

`vllm/v1/core/sched/async_scheduler.py:39` 只维护 `num_output_placeholders`，让下一批可以在上一批真实 token 还没回 CPU 时先调度。D2H 发生在 worker 的 `AsyncGPUModelRunnerOutput`。

**3.3 实际 D2H 点位**

`vllm-cl/vllm_cl/worker/dlc_model_runner.py:276` 记录 default stream，`:277` 切到 `async_output_copy_stream`，`:279` 发起：

```python
self.sampled_token_ids_cpu = self._sampled_token_ids.to(
    "cpu", non_blocking=True
)
```

`:282` 到 `:286` 再处理 logprobs，`:287` 记录 `async_copy_ready_event`。`:294` 的 `get_output()` 在异步输出线程里等 event，`:301` 之后才 `.tolist()` 或做 rejection parse。

**3.4 下一批输入不需要 CPU token**

async decode 时，`_bookkeeping_sync` 把 `sampler_output.sampled_token_ids` 直接留在 GPU，并赋给 `input_batch.prev_sampled_token_ids`，见 `dlc_model_runner.py:3553` 和 `:3557`。
下一 step 的 `_prepare_inputs()` 在 `:1867` 开始，先准备 CPU 侧调度元数据，再调用 `_prepare_input_ids()`：

- 没有 `prev_sampled_token_ids`：prefill/新请求，`input_ids.cpu` 整体 H2D；
- 有 `prev_sampled_token_ids`：对 batch 中与上一批共有的 decode 请求，直接把 GPU 上的 sampled token 填入 `input_ids.gpu`；
- batch 顺序不变时用直接 slice copy，见 `:1778`；
- batch 重排或混合新请求时用 `scatter_`，见 `:1792`；
- speculative decoding 再 scatter draft tokens，见 `:1800`。

因此普通 decode 的下一步模型输入是 `prev_sampled_token_ids`，不是 CPU 上的 `.tolist()` 结果。CPU 只提供 positions、query_start_loc、slot mapping、seq_len 等调度元数据。

**3.5 主线程与异步输出线程**

- worker 主线程：`sample_tokens()` 返回 `AsyncGPUModelRunnerOutput` 后，通过 `vllm/v1/executor/multiproc_executor.py:1000` 把对象放进 `async_output_queue`，随后回到 `:1027` 的 worker RPC 循环，继续执行下一批 `execute_model`。
- 异步输出线程：在 `:1010` 的 `async_output_busy_loop()` 中调用 `:981` 的 `get_output()`，等待 event，做 `.tolist()`/parse，再把 `ModelRunnerOutput` 放进 response MQ。
- EngineCore：V1 且 `pp=1` 时 `max_concurrent_batches=2`，见 `vllm/config/vllm.py:589`；`step_with_batch_queue()` 可以先提交下一批，等 batch queue 满后才在 `vllm/v1/engine/core.py:743` 的 `future.result()` 上等上一批输出。

**3.6 调用关系中的重叠机会与限制**

从源码依赖关系看，以下工作具有重叠机会；这里描述机制允许的调度关系，不代表本轮逐项测得设备并行：

- 下一 step 的 `_prepare_inputs()`：positions、query_start_loc、slot mapping、block table、pinned H2D metadata；
- 下一 step 的 GPU 前向：模型计算、集合通信和 sampling；
- 异步输出线程里的 event 等待、`.tolist()`、输出解析；
- EngineCore 的下一批调度、请求管理和 aborts 处理；
- 多批在飞时，更后面批次的计算。

不能或只能部分重叠：

- 当前 step 的 `scheduler.update_from_output()` 仍要等 D2H 完成，因为要用真实 sampled token 更新请求状态和 KV cache；
- 结构化输出需要上一步真实 token 计算 grammar bitmask 时，下一步 sampling 会被推迟，见 `vllm/v1/engine/core.py:721`；
- repetition penalty、bad words 等依赖 output token ids 的 logits processor，可能通过 `vllm/v1/worker/gpu_input_batch.py:1042` 等 event；
- speculative decoding 的 draft token/valid count 预分配 `copy_` 路径不满足新 fast path；
- 在本次 vllm-cl 配置中，`--enforce-eager` 会关闭 async scheduling；缺少该调度时，不能据此验证其与下一批工作的重叠。O2 或 `DLC_DISABLE_DEVICE_D2H_LAYOUT=1` 会停用新的 D2H fast path。
- 本轮有效配置为 `mode=none + cudagraph_mode=NONE`，未设置 `--enforce-eager`，日志确认 async scheduling 开启。该配置关系仅对应本次框架版本，不把 eager 一概等同于禁止异步拷贝。

#### 4. 性能分析

**4.1 旧路径的真实成本**

旧路径的成本不只是 DMA 字节数，而是：

- runtime 对非 pinned/非对齐 D2H 强制同步；
- 临时 host buffer 分配；
- DMA 完成等待；
- CPU layout unpack；
- 再从 staging `copy_` 到用户输出。

对小 token id 来说，固定开销占主导，所以即使 payload 只有 512B，也可能出现明显 host stall。

**4.2 新路径的收益来源**

- 去掉了 CPU unpack 和额外 `copy_`；
- 调用算子团队提供的 compat/布局算子完成 compact/layout；
- 用 padded pinned output 满足 runtime 的 async 条件；
- D2H 提交后 worker 主线程即可继续下一批；
- event 等待转移到异步输出线程，为其与下一批工作重叠提供条件；本轮 trace 摘要确认了等待的线程归属，未单独证明设备 DMA 与 compute 的时间区间重叠。

**4.3 收益模型与边界**

可以用下面的模型理解收益：

```text
Host 提交路径的潜在耗时减少
  ≈ 旧同步 staging 固定开销 × 每 step D2H 次数
  - 新增 compact/layout kernel 开销
  - 新增 event/allocator 管理开销
```

实际收益取决于：

- 旧同步 D2H 的固定开销；
- 每 step 是否只有采样结果，还是还带 logprobs；
- 是否有下一批可以立即提交；
- DLC runtime 是否允许 copy stream 与计算 stream 真正并行；
- batch queue 是否能在 D2H 完成前保持非空。

上述模型用于组织开销分析，不能直接预测端到端加速比。如果旧同步开销很小，或者没有下一批可提交，等待仍可能落到关键路径。本轮 Qwen3-32B A/B 已观察到不同并发下的正、负结果，按下方固定测试条件记录，不据此推定所有负载都获益。

<a id="async-d2h-validation-20261102"></a>

### 验证结果（2026-11-02）

以下保存本轮测试的环境、命令、通过与跳过项、完整数据表及原始产物位置。`work-tests/...` 均相对于测试机的 `/root/workspace`，不是 PlanA 仓库内的路径。

#### 1. 版本、环境与命令

##### 1.1 实际版本

| 组件 | 版本 / 标识 |
|---|---|
| PyTorch | `2.5.0` |
| PyTorch git version | `20feb31a48655add23935ce6e5a56cae2986251e` |
| PyTorch 路径 | `/root/workspace/pytorch/torch/__init__.py` |
| vLLM | `0.2.8.dev17944+g0058d0d39` |
| vLLM checkout | `0058d0d392e0555d1e92feb2fc599a1d661afeb2`，`fp8-kvcache-main` |
| vllm-cl | `0.1.dev173+ga3cf83b67.d20261102` |
| vllm-cl checkout | `a3cf83b67dcfd2c05843c02caca494b81366bde8`，`fp8-kvcache-main` |
| 驱动 | `Driver Version_v26.0.8` |
| DLC 设备 | 8 张，`/dev/cltech0..7` |
| Qwen3 模型 | `/data/models/Qwen3-32B`，BF16，TP4 |

环境快照位于：

- `work-tests/async-d2h/results/full-20261102/A/env.json`
- `work-tests/async-d2h/results/full-20261102/B/env.json`
- `work-tests/async-d2h/results/full-20261102/C/env.json`

##### 1.2 A/B/C 配置

| 组别 | `DLC_SYN_COPY_ASYNC` | `DLC_DISABLE_DEVICE_D2H_LAYOUT` | 用途 |
|---|---:|---:|---|
| A | `O3` | `1` | 同构建的同步回退路径 |
| B | `O3` | unset | 新异步 D2H 路径 |
| C | `O2` | unset | 可选整体策略对照 |

A/B 固定同一目标构建和 O3，仅切换 D2H fast path；C 组用于整体策略对照。A 组故意走 fallback，因此现有测试中“`.to()` 后 event 仍 pending”的断言由 wrapper 跳过；其余数据、布局、生命周期测试照常执行。

##### 1.3 执行命令

PyTorch A/B/C 全套：

```bash
cd /root/workspace
/root/workspace/.venv/bin/python work-tests/async-d2h/run_ab_suite.py \
  --python /root/workspace/.venv/bin/python \
  --run-name full-20261102 \
  --groups A,B,C \
  --repeats 10
```

Qwen3-32B vLLM A/B：

```bash
cd /root/workspace
TEST_GROUPS="A B" \
REPEATS=3 \
NUM_PROMPTS=8 \
CONCURRENCIES="1 8" \
INPUT_LEN=512 \
OUTPUT_LEN=128 \
RUN_NAME=qwen3-32b-full-20261102 \
  ./work-tests/async-d2h/run_qwen3_32b_ab.sh
```

Qwen3 服务配置：

```text
--tensor-parallel-size 4
--max-model-len 4096
--max-num-batched-tokens 4096
--max-num-seqs 8
--block-size 256
--dtype bfloat16
--compilation-config '{"mode":"none","cudagraph_mode":"NONE"}'
```

不加 `--enforce-eager`。该配置下服务日志明确出现：

```text
Asynchronous scheduling is enabled.
```

##### 1.4 Qwen3 graph 模式说明

历史 FP8 Qwen3 实验使用 `--enforce-eager`，这会让 vllm-cl 关闭 async scheduling，因此不能用于 D2H 重叠验证。

本次有效测试使用 `mode=none + cudagraph_mode=NONE`、保持非 eager。`FULL_DECODE_ONLY` 测试中，记录的失败发生在 Qwen3 fused-QKV patch 与 graph/compile 路径的接口分派处：当前 vllm-cl 的 `patch_qwen3.py` 落到标准 `RotaryEmbedding.forward_native()`，该接口不接受 `qkv=` 参数。因此该配置未计入本轮有效结果。

#### 2. 通过、失败与跳过清单

##### 2.1 PyTorch A/B/C

| 组别 | 现有 `dlc_async_d2h_copy.py` | 补充测试 | 微基准 | 结果 |
|---|---|---|---|---:|
| A fallback | PASS，跳过 2 个 deferred-event 断言 | 6/6 PASS | PASS | 通过 |
| B async | PASS | 6/6 PASS | PASS | 通过 |
| C O2 | PASS，跳过 event-pending 检查 | 4/4 PASS | PASS | 通过 |

A 组跳过项：

```text
SKIP deferred D2H raw_dma: fallback mode intentionally completes synchronously
SKIP deferred D2H flattened_Nx1: fallback mode intentionally completes synchronously
```

C 组跳过项：

```text
SKIP event-pending checks: async D2H requires O3
```

补充测试覆盖：

- 基础 shape/dtype/storage contract；
- slice/transpose fallback；
- 16M int32 控制积压；
- device allocation lifetime；
- pinned host allocation lifetime；
- 非默认 stream 依赖。

没有失败项。

##### 2.2 Qwen3-32B vLLM

| 组别 | 并发 | 轮数 | 每轮 prompts | completed | failed | 状态 |
|---|---:|---:|---:|---:|---:|---|
| A | 1 | 3 | 8 | 24 | 0 | PASS |
| A | 8 | 3 | 8 | 24 | 0 | PASS |
| B | 1 | 3 | 8 | 24 | 0 | PASS |
| B | 8 | 3 | 8 | 24 | 0 | PASS |

服务在 benchmark 结束后由 SIGTERM 关闭；日志末尾的 `EngineDeadError` 是关闭路径噪声，不是请求失败。所有 `vllm bench serve` 返回码为 0。

#### 3. 异步提交与生命周期记录

##### 3.1 控制积压

16M int32 单次 D2H，A/B 各一次控制积压记录：

| 组别 | submit | event wait | 返回时 pending |
|---|---:|---:|---|
| A fallback | 5.973679 ms | 0.084697 ms | true |
| B async | 0.053039 ms | 4.738049 ms | true |

两组的 `pending` 都为 true，不能单独据此区分同步回退与异步路径。结合调用路径与完成后校验，A 的 submit 包含同步 staging 开销，B 则更早返回并在 event wait 侧等待完成。这组记录支持受测路径的异步提交契约；5.973679 → 0.053039 ms 是该次控制积压中的 Host 提交耗时变化，不是 DMA 传输或端到端加速倍数。

##### 3.2 设备与 Host 生命周期

补充测试 A/B 各运行 32 轮：

- A：device lifetime PASS；host lifetime PASS；pinned pointer reuse 32 次。
- B：device lifetime PASS；host lifetime PASS；pinned pointer reuse 32 次。
- 所有轮次均无旧 DMA 覆盖新 pinned buffer，也没有提前释放导致的错误。

#### 4. A/B 微基准

输入为 `[N,1]` int32，每组 warmup 3 次、重复 10 次；时间为中位数。

| N | A submit | A wait | B submit | B wait | C submit | C wait |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.055 | 0.001 | 0.039 | 0.012 | 0.053 | 0.001 |
| 128 | 0.056 | 0.001 | 0.083 | 0.002 | 0.054 | 0.001 |
| 129 | 0.056 | 0.001 | 0.084 | 0.003 | 0.054 | 0.001 |
| 257 | 0.062 | 0.001 | 0.083 | 0.002 | 0.054 | 0.001 |
| 1024 | 0.096 | 0.005 | 0.085 | 0.002 | 0.099 | 0.008 |
| 16384 | 0.737 | 0.009 | 0.083 | 0.047 | 0.751 | 0.009 |
| 16385 | 0.738 | 0.009 | 0.253 | 0.106 | 0.738 | 0.009 |
| 65536 | 2.550 | 0.002 | 0.761 | 0.865 | 2.559 | 0.003 |

单位：ms。原始值：

- `work-tests/async-d2h/results/full-20261102/A/micro.json`
- `work-tests/async-d2h/results/full-20261102/A/micro.csv`
- `work-tests/async-d2h/results/full-20261102/B/micro.json`
- `work-tests/async-d2h/results/full-20261102/B/micro.csv`
- `work-tests/async-d2h/results/full-20261102/C/micro.json`
- `work-tests/async-d2h/results/full-20261102/C/micro.csv`

小拷贝的 `pending_at_return` 没有稳定区分度，不应据此单独判断路径；submit 耗时和大拷贝控制积压更有解释力。

#### 5. Qwen3-32B 端到端 A/B

##### 5.1 请求口径

- 输入/输出：512 / 128 tokens
- prompts：8
- 并发：1 和 8
- 轮数：3
- 每组每个并发：24 个成功请求，0 个失败
- `vllm bench serve` 使用 `openai-chat`、`temperature=0`、`ignore-eos`、固定 seed
- 服务端：TP4、BF16、no-graph、非 eager、async scheduling enabled

##### 5.2 3 轮中位数

| 并发 | 组别 | TTFT p50 | TTFT p95 | TTFT p99 | TPOT p50 | TPOT p95 | TPOT p99 | Output tok/s |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | A fallback | 48.57 | 52.55 | 53.23 | 37.33 | 37.94 | 38.09 | 26.71 |
| 1 | B async | 47.87 | 55.80 | 57.38 | 40.70 | 44.60 | 45.90 | 24.53 |
| 8 | A fallback | 154.81 | 155.26 | 155.35 | 39.76 | 39.82 | 39.85 | 196.69 |
| 8 | B async | 153.33 | 154.03 | 154.20 | 38.62 | 38.69 | 38.71 | 202.60 |

单位为 ms；吞吐为 3 轮 output throughput 的中位数。

##### 5.3 解释

- 8 并发：B 组 output throughput 中位数由 196.69 升至 202.60 tok/s，约 `+3.0%`；TPOT p50 由 39.76 降至 38.62 ms，约 `-2.9%`。这是本轮小样本下的正向观测。
- 1 并发：B 组 output throughput 中位数由 26.71 降至 24.53 tok/s，约 `-8.2%`；TPOT p50 由 37.33 增至 40.70 ms，约 `+9.0%`。本轮出现性能回退，原因尚未确定；固定开销或运行波动只能作为可能解释。
- 本次每组每档只有 3 轮，并发 8 每轮也只有 8 个 prompts，主要对应一波请求。现有汇总未列逐轮波动，不支持稳定的持续负载收益；小样本的 p95/p99 保留为本次统计值，不解释为可靠的生产尾延迟。
- 所有请求成功证明链路完成。记录未给出 A/B 输出 token 序列或文本的一致性结果，因此不据此声明模型级精度或生成内容一致。TPOT 保留原指标名称，不改称逐 token ITL。

原始数据：

- `work-tests/async-d2h/results/qwen3-32b-full-20261102/vllm_A/`
- `work-tests/async-d2h/results/qwen3-32b-full-20261102/vllm_B/`

#### 6. 代表性时间线

##### 6.1 Trace 文件

A/B 均采集 short trace（32 input / 8 output、单请求），并复制到结果目录：

- `work-tests/async-d2h/results/qwen3-32b-trace-a-v2-20261102/traces/`
- `work-tests/async-d2h/results/qwen3-32b-trace-b-v2-20261102/traces/`

所有 rank0-3 和 frontend trace 均通过 `gzip -t`。采集时使用：

```json
{
  "profiler": "torch",
  "torch_profiler_with_stack": false
}
```

上一版带 stack 的 profiler run 在 `/stop_profile` 阶段超时，trace 不完整，已由 v2 替代。

##### 6.2 rank0 事件摘要

| 事件 | A fallback | B async |
|---|---:|---:|
| `aten::_to_copy` 次数 | 48 | 48 |
| `aten::_to_copy` 总时长 | 20.520 ms | 2.738 ms |
| `aten::_to_copy` 最大单次 | 6.261 ms | 0.099 ms |
| `synMemCopyAsync` 次数 | 108 | 108 |
| `synMemCopyAsync` 总时长 | 1.694 ms | 1.918 ms |
| `dlcEventSynchronize` 次数 | 36 | 36 |
| `dlcEventSynchronize` 总时长 | 0.206 ms | 656.509 ms |
| `dlcEventSynchronize` 最大单次 | 0.053 ms | 99.610 ms |

##### 6.3 时间线解释

A 组的 `aten::_to_copy` 在 worker 线程上承担了更大的同步成本，最大单次约 6.26 ms；B 组同一事件的提交路径降到最大约 0.10 ms。

根据测试时的 trace 整理，B 组较长的 `dlcEventSynchronize` 位于 async output 线程，单次最长约 99.6 ms；A 的 event 等待较小，与其同步 staging 在 `_to_copy` 内等待的源码行为一致。

该摘要支持主机调用路径耗时下降和完成等待的线程归属。它没有逐 step 的区间对应，不能单凭聚合时长证明下一批工作已与等待重叠，也不能证明设备 DMA 与 compute 真正并行。`synMemCopyAsync` 的统计是 API 调用时长，不是 DMA 持续时间；跨线程累计 event wait 也不等于请求关键路径耗时。Profiler 会改变时间，因此这些绝对值仅用于本次机制分析，不作为端到端性能数字。

#### 7. 本轮结论与适用边界

- PyTorch `20feb31a48…` 目标构建的现有 D2H 回归、补充测试与微基准均通过；A/C 按同步路径跳过不适用的 deferred-event 断言，无失败项。该结果覆盖本轮列明的输入与路径，不保证所有形状、dtype 或并发交错。
- 受控积压与生命周期测试支持新路径的提前返回、完成后数据正确，以及设备和 Host 分配在本轮复用压力下未提前回收。它们不替代生产规模的长期稳定性结论。
- Qwen3-32B 在 BF16、单机 TP4、no-graph、async scheduling 开启的条件下完成 A/B 请求测试。设备环境有 8 张卡，本次模型使用 TP4，不能写成 8 卡 TP8 测试。
- 端到端结果同时保留并发 8 的初步正向信号和单并发的回退；未确定回退原因，未证明稳定的跨负载收益。当前记录未包含生成内容一致性对照、逐轮波动或持续负载结果。
- Trace 的聚合摘要支持等待线程迁移，不升级为已证明逐 step 实际重叠或设备 DMA/compute 并行。Qwen3 graph/compile 不兼容路径和带 stack 的不完整 trace 均不计入有效结果。

### 面试深挖点

1. **为什么旧的 `non_blocking=True` 实际上不是异步？**
   关键在 DLC runtime：非 pinned/非 512B 对齐 D2H 会设置 `isAsync=false`；旧 PyTorch 路径又走 CPU staging + unpack，并没有真正满足异步条件。

2. **为什么必须把输出 padding 到 512B？**
   runtime 把 `dmaSize != logicalSize` 视为 misaligned D2H，会分配临时 buffer 并强制同步。padding 后 DMA 大小与分配边界都对齐，才能保持 `isAsync=true`。

3. **为什么还要 device-side layout kernel？**
   DLC 物理 storage 可能按 padded row 存放，不能直接把逻辑 tensor 当连续 buffer 拷给 CPU；必须先 compact，并对 8/16/64-bit 做 CPU 字节序转换。这些 compat/转 CPU 布局算子由算子团队提供，PyTorch 侧负责调用、布局约定和生命周期衔接。

4. **异步后如何防止 source/host buffer 被提前释放？**
   设备侧用 `DLCCachingAllocator::recordStream()`，host 侧用 `CachingHostAllocator_recordEvent()`；调用方再用 event 等待完成。

5. **为什么 vLLM 下一批模型输入不需要 CPU token？**
   普通 decode 的下一步输入就是上一步 sampled token，而它已经在 GPU 的 `prev_sampled_token_ids` 中；`_prepare_input_ids()` 在 GPU 上直接 copy/scatter 到 `input_ids.gpu`，CPU 只提供调度元数据。

### 面试叙述

#### 当前叙述

DLC 推理里，异步调度的目标本来是让 worker 在上一批采样结果还没回 CPU 时继续跑下一批。但旧 DLC 后端即使传 `non_blocking=True`，D2H 仍会因为 host 非 pinned、尺寸未 512B 对齐而走 runtime 的同步 staging，worker 主线程实际上被卡住。

我负责 PyTorch 侧异步 D2H 的实现：通过 padded pinned output、调用算子团队提供的 compat/转 CPU 布局算子、`synMemCopyAsync`，以及 `recordStream`/host event 生命周期保护，把 D2H 变成真正提交后返回；同时把异步级别收到 O3，并保留不满足条件时的同步回退。vLLM-cl 侧实际点位在 `DLCModelRunner` 的 `AsyncGPUModelRunnerOutput`，不是上游 `gpu_model_runner`。普通 decode 的下一批输入直接取 GPU 上的 `prev_sampled_token_ids`，CPU 上的 token 回读只为 response、请求状态和部分采样约束服务。

实现中需要处理两个边界：一是 pinned 与传输对齐决定 runtime 是否保留异步语义；二是下游等待必须覆盖完成事件，而设备和 Host 分配在此之前都不能被提前复用。我还沿 vLLM 实际调用链确认，普通 decode 的下一步 token 可以保留在设备侧，因此 CPU 回传与下一批准备之间存在解除阻塞的空间。

在目标 PyTorch 构建上，A/B/C 回归、设备与 Host 生命周期测试均通过。同构建 O3 下只切换 D2H 路径后，16M int32 控制积压中的 Host 提交耗时由约 5.97 ms 降至 0.053 ms，完成等待留在后续 event 侧。Qwen3-32B、BF16、TP4 的有限请求测试全部成功；三轮中位数显示，并发 8 吞吐约提升 3.0%，单并发约下降 8.2%。我保留这个负结果，不把本轮观测表述成稳定的生产加速。

#### 个人职责与协作边界

- **我负责（作者）**：PyTorch DLC 后端异步 D2H 的方案、PyTorch 侧编排/实现、测试和回退策略；DLC runtime 异步条件分析；vLLM/vllm-cl 点位映射与收益评估。
- **与同事共同完成**：与 vLLM/vllm-cl 同事确认实际调度点位和生产接入方式；与 runtime/性能同事分析多 stream DMA 与 compute 的并行条件。本轮聚合 trace 未单独证明设备并行。
- **其他团队负责**：compat 算子与转 CPU 布局算子由算子团队负责；vLLM-cl 生产接入、DLC runtime/driver 的独立实现、生产端到端性能验收和对外发布口径。
- **当前不能扩张的表述**：
  - 不能声称“所有 D2H 都已异步化”，预分配 slice 的 `copy_`、structured output、spec draft metadata 仍有同步点；
  - 不能把上游 `vllm` 的 `gpu_model_runner` 当成 DLC 生产路径；
  - 不能声称 D2H 已从关键路径消失，`scheduler.update_from_output()` 仍然要等 event；
  - A/B 结果只按本轮模型、配置、请求规模和统计口径使用，不能宣称跨负载固定提升，也不能省略单并发回退；
  - 请求成功不等于 A/B 输出内容一致；Host 调用时长下降不等于 DMA 加速或已经证明设备计算重叠；
  - 不能把 compat 算子或转 CPU 布局算子说成 PyTorch 侧实现。

#### 验证结果与适用范围

| 字段 | 本轮事实 | 适用范围 |
|---|---|---|
| 构建与版本 | 已运行 PyTorch `20feb31a48655add23935ce6e5a56cae2986251e`，完整框架与环境标识见验证结果 | 取代此前仅在 merge base `9049914` 环境分析的状态 |
| 代表性改动 | `313fc47c31` 与 `20feb31a48` 为本人实现的 PyTorch 侧异步 D2H；目标构建回归通过 | 本人负责框架侧编排、内存与同步契约，compat/layout kernels 由算子团队实现 |
| 数据与生命周期 | A/B/C 回归通过，A/B 设备与 Host 生命周期压力测试各 32 轮通过 | 限于已测 contract；不扩张为所有输入或长期稳定性保证 |
| vLLM 请求结果 | Qwen3-32B、BF16、TP4，每组每并发 24 个请求成功、0 失败 | 已验证请求链路完成；A/B 生成内容一致性未在记录中呈现 |
| 性能口径 | 并发 8 吞吐中位数约 +3.0%，单并发约 -8.2%；微基准与 trace 单独记录 | 有限样本观测，保留负结果；未证明持续负载收益或设备级重叠 |
| 对外披露 | 框架机制与个人职责可讲，内部路径、接口与具体性能数据保留在本档案 | 本次整理不扩大已有对外披露范围，具体数字仍受原项目披露约束 |

### 附录：关键代码索引

| 文件 | 作用 |
|---|---|
| `pytorch/aten/src/ATen/native/TensorConversions.cpp:343` | DLC O3 padded pinned 输出入口 |
| `pytorch/aten/src/ATen/native/TensorConversions.cpp:354` | 512B padded pinned allocation |
| `pytorch/aten/src/ATen/native/dlc/Copy_cpu.h:787` | 异步 D2H eligibility |
| `pytorch/aten/src/ATen/native/dlc/Copy_cpu.h:818` | device compaction/layout + DMA fast path |
| `pytorch/aten/src/ATen/native/dlc/Copy_cpu.h:930` | device allocation stream lifetime |
| `pytorch/aten/src/ATen/native/dlc/Copy_cpu.h:941` | pinned host allocation event |
| `pytorch/c10/dlc/DLCConstants.h:16` | `DLC_SYN_COPY_ASYNC` O0–O3 解析 |
| `DLCSynapse/synapse_core/synapse_state.cpp:1812` | runtime 判定 misaligned/unpinned D2H 并强制同步 |
| `vllm-cl/vllm_cl/worker/dlc_model_runner.py:276` | 实际 D2H copy stream 起点 |
| `vllm-cl/vllm_cl/worker/dlc_model_runner.py:279` | sampled token id `.to("cpu", non_blocking=True)` |
| `vllm-cl/vllm_cl/worker/dlc_model_runner.py:295` | 异步输出线程等待 event |
| `vllm-cl/vllm_cl/worker/dlc_model_runner.py:3557` | 上一 step sampled token 缓存在 GPU |
| `vllm-cl/vllm_cl/worker/dlc_model_runner.py:1693` | `_prepare_input_ids()` |
| `vllm-cl/vllm_cl/worker/dlc_model_runner.py:1778` | 下一 step 直接 copy `prev_sampled_token_ids` |
| `vllm-cl/vllm_cl/worker/dlc_model_runner.py:1792` | batch 重排时 scatter sampled token |
| `vllm/config/vllm.py:589` | V1 async scheduling 的 `max_concurrent_batches=2` |
| `vllm/v1/executor/multiproc_executor.py:1010` | worker 异步输出线程 |
