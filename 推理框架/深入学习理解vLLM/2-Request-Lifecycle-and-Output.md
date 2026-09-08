本文围绕一次 vLLM 请求，说明三个问题：`output_kind` 如何组织调用方可见的输出；请求结束后，调度侧、前端和 ModelRunner 分别清理什么；如何将这些机制串成从接收请求到返回结果的完整表述。

## 来源与讨论范围

本文承接[仓库地图与进程架构](1-Repository-and-Process-Architecture.md)，以 vLLM `v0.26.0 @ 568afb3a13806beb53bb2e6bd518269357b237c0` 的源码为实现依据。正文中的上游链接均固定到该提交，不随本地源码子模块的当前 checkout 改变。

主场景限定为：

- V1 引擎、MRV1、一个 API Server，`DP=TP=PP=1`、`backend=uni`。
- 服务已经就绪，模型权重和物理 KV pool 已经初始化。
- 普通纯文本 Chat Completion，`n=1`，非流式输入，不使用投机解码，没有前缀缓存命中。
- 以 `stream=true`、最终达到 `max_tokens` 为主线，再对照非流式输出、stop string 和断连分支。

本文不展开多模态执行、PD 传输、多卡通信或具体 Attention Kernel 的内部算法。KV 延期回收只用于说明安全边界，不将某条同步路径推广为所有异步配置的统一时序。内容为源码理解与讲述材料，不代表设备运行或性能实测结论。

## output_kind 与两层输出

### RequestOutput 的交付形式

EngineCore 向前端返回的内部结果，与前端交给调用方的 `RequestOutput`，是两层不同的输出。`output_kind` 主要规定后者包含多少生成内容，以及是否交付中间结果。

假设生成内容依次增加 `A`、`B`、`C`，暂不考虑缓冲和聚合：

| output_kind | 交付语义 | 调用方依次收到的内容 |
|---|---|---|
| `CUMULATIVE` | 每次提供截至当前的累计结果 | `A` → `AB` → `ABC` |
| `DELTA` | 每次只提供新增内容 | `A` → `B` → `C` |
| `FINAL_ONLY` | 不交付中间结果，结束时提供完整结果 | 结束时收到 `ABC` |

这三种语义直接对应 [`RequestOutputKind` 的定义](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/sampling_params.py#L182-L188)。它们让调用方可以选择维护累计快照、拼接增量，或只处理最终结果。

在 OpenAI Chat 接口中，前端将 `stream=true` 映射为 `DELTA`，将 `stream=false` 映射为 `FINAL_ONLY`，并分别选择 SSE 或完整 HTTP 响应。输出对象的组织方式与 HTTP 响应方式相互配合，但它们不是同一层协议。[参数转换](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/protocol.py#L690-L692)、[响应分支](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/entrypoints/openai/chat_completion/serving.py#L384-L407)

### FINAL_ONLY 不阻止 Core 返回中间结果

输出处理可以分成两段：

```text
EngineCore → EngineCoreOutput → 前端 OutputProcessor
                                      ↓
                          按 output_kind 组织 RequestOutput
                                      ↓
                          Collector → generate() → HTTP
```

在当前版本的普通生成路径中，Core 继续逐步执行模型并向前端传递结果。前端 OutputProcessor 接收这些结果后，更新文本和相关输出状态、检查 stop string，再决定是否产生调用方可见的 `RequestOutput`。

`FINAL_ONLY` 的过滤位于前端的 `RequestState.make_request_output()`：

```python
final_only = self.output_kind == RequestOutputKind.FINAL_ONLY

if not finished and final_only:
    return None
```

这里暂不产生的是交给 Collector 的中间 `RequestOutput`，不是禁止 EngineCore 生成或传回中间结果。stop string 检查发生在调用这一方法之前，所以非流式请求也可以在未达到 `max_tokens` 时由前端提前判停。[前端输出过滤](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L273-L310)、[先更新文本和判停再组织输出](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L649-L678)

`output_kind` 放在 `SamplingParams` 中，并可以随核心请求跨越 IPC，但字段传递到某个组件，不代表它的主要语义由该组件实现。不能据此认为 Core 根据 `FINAL_ONLY` 决定是否等待整个请求完成后再向前端发送结果。

### 输出对象与传输粒度

Collector 还会根据模式处理尚未被消费的结果。生产方快于消费方时，`DELTA` 结果可以合并，避免新增内容丢失；累计结果则按累计更新处理，不能把两份累计文本再次直接拼接。`stream_interval` 也可以影响交付粒度。因此，一个生成 token 并不必然对应一次调用方回调或一个 SSE 消息。[Collector 聚合](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L45-L76)、[输出内容选择](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L385-L404)

以上结论限定在本文的普通生成场景。流式输入和多个候选输出还存在额外的参数校验或聚合逻辑，不宜将其概括成 `output_kind` 在所有路径中都只影响一个函数。

## 请求结束后的清理

### 调度侧、前端和执行侧各自持有状态

请求结束涉及三类状态：调度侧管理请求与 KV 资源账本；前端管理输出处理和消费者；ModelRunner 管理本地请求缓存、InputBatch 和输入映射。即使在 `backend=uni` 下后端组件位于同一进程，也不能混淆这些职责。

对于正常达到 `max_tokens` 的请求，模型结果返回后，Scheduler 在更新请求状态时确认它已经结束。之后的职责与传递关系可以概括为：

```text
Scheduler 确认请求结束
├─ 调度侧资源处理：结束状态、队列移除、KV 引用回收
├─ 输出返回：带结束原因的 EngineCoreOutput → 前端
└─ 执行侧清理通知：后续 SchedulerOutput.finished_req_ids
                   → Executor → Worker → ModelRunner
```

这张图不表示三个分支同时完成，也不要求前端消费最终结果与 Runner 清理之间建立额外的等待关系。

### 调度侧回收 KV 引用

Scheduler 在处理模型输出时确认停止条件、设置结束状态，并完成请求队列和资源账本的处理。它通过 KVCacheManager／BlockPool 解除请求对 KV blocks 的引用，同时登记 `finished_req_ids`，随后由 EngineCore 将带有结束原因的输出传给前端。

共享块仍被其他请求引用时不能归还；引用归零的块才重新具备可分配资格。归还的是池内块的使用权，物理 KV pool 不会因此缩小，旧 KV 数据也不一定立即清除。开启前缀缓存时，零引用块仍可能保留缓存标识，直到重新命中或被淘汰。[BlockPool 的引用与空闲队列管理](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/block_pool.py#L647-L740)

正常结束时，相关模型执行结果已经收回，可以进行回收；异步执行期间发生取消时，如果仍有在途写入，实际回收需要遵守安全延期机制。不能仅凭前端已经结束，就判断相关块已经立即可以被其他请求覆盖。[Scheduler 回收与安全延期](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L2207-L2261)

### Runner 清理本地执行状态

结束 ID 会进入后续的 `SchedulerOutput.finished_req_ids`，经 Executor 和 Worker 传给 ModelRunner。ModelRunner 的 `_update_states()` 移除已结束请求的本地缓存状态和 InputBatch 成员，再根据剩余请求准备后续输入与映射。

ModelRunner 不再次扣减这些请求的 KV pool 引用计数。Executor 和 Worker 也不会接管 Scheduler 的资源账本。模型权重、设备环境和物理 KV pool 作为服务级资源继续保留。[结束 ID 的交接](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/core/sched/scheduler.py#L1158-L1162)、[Runner 状态清理](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_model_runner.py#L1179-L1193)

清理不必等待下一次真正的 forward。即使后续调度结果没有待计算 token，ModelRunner 也会先更新持久状态，再判断是否跳过模型计算。因此，不能把它理解成必须等待新请求到来后才清理旧请求。[零 token 调度的处理顺序](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/worker/gpu_model_runner.py#L4147-L4178)

### 前端注销状态与消费最终输出

前端处理最终结果的局部顺序是：

```text
最终 RequestOutput 放入 Collector
→ OutputProcessor 从请求表注销 RequestState 和相关 ID 映射
→ generate() 从 Collector 取出并 yield 最终输出
→ generate() 结束迭代，在 finally 中调用 Collector.close()
```

注销 RequestState 不等于强制销毁所有关联对象。`generate()` 仍然持有 Collector，因此可以取出已经投递的最终结果。这里的 `generate()` 消费并交付结果，不执行模型采样。

在该版本中，Collector 的 `close()` 主要处理可能关联的输入流任务，不应把它描述成强制销毁 Collector 或清空所有缓冲。对象的最终回收仍取决于引用生命周期。[最终输出与请求表清理](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L676-L717)、[generate 消费结果](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L573-L586)、[Collector 关闭行为](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L98-L106)

前端完成输出消费，与 ModelRunner 处理结束通知之间，没有必须等待对方完成的依赖。它们的实际先后可以交错；HTTP 已经返回但 Runner 尚未消费结束通知，并不单独证明资源泄漏。

### stop string 与断连分支

如果停止条件是前端 Detokenizer 才识别出的 stop string，前端形成对外的 `stop` 结果，并由 AsyncLLM 向 Core 发送 `ABORT`。Core 接到后按内部 `FINISHED_ABORTED` 处理，再进入调度侧的终止与回收路径，通过后续调度结果通知 Runner。用户可见的停止原因与 Core 内部取消状态不必使用相同名称。[前端判停与取消列表](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/output_processor.py#L649-L696)、[发送取消](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L685-L689)、[Core 处理取消](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L477-L483)

前端不需要等待 Core 再发送一份最终确认，才能结束响应。若客户端断连导致 `generate()` 被取消，也需要通过取消路径通知 Core，但不能期待已经断开的客户端收到最终 HTTP 响应。[生成器取消处理](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L588-L594)

## 请求全流程讲述稿

这里以一个已经完成初始化的 vLLM 服务为例。服务使用 V1 引擎和 MRV1，只有一个 API Server，配置为 `DP=TP=PP=1`、`backend=uni`。模型权重已经加载，物理 KV pool 已经按照预算完成分配。我们讨论一个普通的纯文本 Chat Completion 请求，不考虑投机解码，也没有前缀缓存命中。

在这个场景中，服务由两个主要进程组成。前端进程包含 API Server 和 AsyncLLM，负责协议处理、请求输入整理以及输出交付。后端进程包含 EngineCore、Scheduler、Executor、Worker 和 ModelRunner，负责请求调度与模型执行。虽然这些后端组件位于同一个进程中，但各自持有的状态和承担的职责仍然不同。

请求首先由 API Server 接收。前端根据 messages 等内容完成模板渲染和分词，准备 EngineInput；同时将温度、输出长度上限、停止条件等信息转换为 SamplingParams。`stream` 还会影响输出组织方式：流式请求使用 `DELTA`，非流式请求使用 `FINAL_ONLY`。随后，InputProcessor 校验并整理输入及参数，构造 EngineCoreRequest。这里应当区分模板渲染、分词和核心请求构造，不把它们混成一个动作。[Renderer 输入准备](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/renderers/base.py#L1084-L1108)、[核心请求构造](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/input_processor.py#L370-L384)

AsyncLLM 根据请求 ID 和输出模式创建 RequestOutputCollector，并向 OutputProcessor 注册该请求的前端状态。注册完成后，才通过 EngineCoreClient 使用 ZMQ IPC 将 EngineCoreRequest 发送到后端。这个顺序保证了后端开始返回结果时，前端已经具备接收和处理该请求输出的状态。[先注册后提交](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/async_llm.py#L391-L412)

EngineCore 收到并解码 EngineCoreRequest 后，将它转换为内部可变的 Request，交给 Scheduler 管理。新请求通常先进入 waiting 队列。此时，请求已经被调度器登记，但还没有因为进入队列就自动获得执行资格。若请求使用 structured output，还可能需要等待 grammar 准备完成；grammar 就绪后，也仍然需要通过普通的资源检查。

进入一个 engine step 时，Scheduler 通常先处理 running 请求，再尝试接纳 waiting 请求。它根据本步 token budget、KV 资源以及相关配置，决定哪些请求执行、每个请求处理多少输入 token，并通过 KVCacheManager 分配需要的 KV 槽位和 pool block IDs。资源满足后，请求才进入 running。这里分配的是池内块的使用权，不是在设备上为每个请求重新创建整套 KV tensor。

Scheduler 最后形成 SchedulerOutput，其中包含本步执行的请求、各请求的计算量、块分配信息，以及需要清理的已结束请求 ID 等内容。调度记录描述的是本步执行计划；调度阶段推进的计算计数，也不能直接当作设备已经完成计算的证明。

EngineCore 将 SchedulerOutput 交给 Executor 下发。在当前 `uni` 场景中，调用经 Worker 到达 ModelRunner。Worker 的设备初始化已经在服务启动时完成；每一步主要处理执行入口及相关设备执行包装，再调用 ModelRunner。

ModelRunner 根据调度结果更新本地请求状态和持久 InputBatch，处理新增、继续执行和结束的请求。随后，它准备本步有效的 `input_ids`、`positions`、请求片段边界、序列长度、block table 和 `slot_mapping` 等信息。物理 KV pool 保持不变，本步变化的是哪些请求使用哪些块，以及 token 如何映射到这些块中的槽位。

模型调用时，`input_ids`、`positions` 等作为显式输入传入，Attention 所需的运行时 metadata 和缓存访问相关信息则通过相应的 ForwardContext 等机制提供。Attention 按照配置的 backend 执行计算，写入本步新产生的 KV，并通过块映射读取该请求的历史 KV。不同请求即使被放进同一个 batch，也必须保持输入片段、位置和 KV 映射的一致性，不能互相读取对方的上下文。

模型 forward 得到 hidden states 后，普通生成路径使用每个请求本步片段末尾对应的结果计算 logits，并进行采样。如果开启 chunked prefill，较长的 prompt 可以按调度预算分多步计算；短 prompt 也可能一次完成。尚未完成 prompt 的片段可能参与批量采样，但其结果不会作为有效的新生成 token 对外返回。

完成 prompt 的最后一次 prefill 就能够产生第一个有效输出 token。下一次 decode 将这个已经采样出来的 token 作为输入，计算并写入它自己的 KV，再预测下一个 token。因此，decode 本轮处理的是已经知道 ID 的输入 token，而不是提前处理尚未采样出来的那个 token。

执行结果最终以 ModelRunnerOutput 等约定形式返回 EngineCore。在 MRV1 的相应路径中，`execute_model()` 可能先返回 `None`，再由 `sample_tokens()` 完成采样并取得输出；这不表示模型执行失败。随后，EngineCore 调用 Scheduler 的结果更新逻辑，回写请求的 token 历史、检查停止条件，并整理发往前端的 EngineCoreOutput。[单步执行与结果回写](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/v1/engine/core.py#L576-L606)

前端的后台输出处理任务持续接收 EngineCore 的结果。OutputProcessor 更新文本和相关输出状态，检查文本级停止条件，并根据 `output_kind` 组织 RequestOutput。流式请求通常交付增量结果，非流式请求则不交付中间 RequestOutput，直到请求结束才交付完整结果。非流式模式不会阻止 Core 向前端逐步返回内部结果，所以前端仍能及时识别 stop string。

需要交付的 RequestOutput 被放入 Collector，再由 `generate()` 取出并向上层 yield。这里的 `generate()` 是消费输出的异步生成器，不是在重新执行模型采样。API Server 对流式请求使用 SSE 返回，对非流式请求则在最终结果就绪后一次性返回完整响应。由于结果可能被聚合或暂存，不能要求一个模型 token 严格对应一个 SSE 消息。

如果请求达到 `max_tokens`，或者命中由 Core 处理的 EOS／stop token，Scheduler 会在处理模型结果时确认结束，更新请求状态，将其从调度队列移除，并解除它对 KV blocks 的引用。共享块只有在引用归零后才能重新分配，物理 KV pool 本身继续保留。EngineCore 同时整理带有结束原因的最终输出并发送给前端。

前端先将最终 RequestOutput 放入 Collector，再注销 OutputProcessor 中的 RequestState 和相关请求映射。`generate()` 仍然持有 Collector，因此可以取出并交付最终结果，随后结束迭代并执行 Collector 的关闭处理。注销 RequestState 与关闭 Collector 是两个动作，不要求把关联对象同时销毁。

执行侧的本地状态通过另一条路径清理。Scheduler 将结束请求的 ID 放入后续 SchedulerOutput，经 Executor 和 Worker 传给 ModelRunner。ModelRunner 移除该请求的本地缓存状态和 InputBatch 成员，其他请求继续按照调度结果执行。它不会再次扣减 KV pool 的引用计数，也不会重新创建或释放整个模型和缓存池。即使后续调度结果没有待计算 token，Runner 也可以先完成状态更新再跳过 forward；前端返回最终结果，不必等待这一步本地清理完成。

如果停止条件是前端 Detokenizer 才识别出的 stop string，前端会先形成对外的 `stop` 结果，并由 AsyncLLM 向 EngineCore 发送 `ABORT`。Core 再执行请求终止、KV 引用回收和 Runner 清理通知。若客户端断连导致生成任务取消，也需要把取消通知传给 Core，但这时不能再期待已经断开的客户端收到最终 HTTP 响应。对于取消时仍有在途设备操作的情况，KV 块回收还必须遵守安全时序，避免其他请求过早覆盖仍在使用的缓存。
