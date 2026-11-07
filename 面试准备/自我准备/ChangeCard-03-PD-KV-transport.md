<a id="change-card-03-pd-kv"></a>

# Change Card 03：KVConnector 到 PD/KV transport（两分支学习设计）

> 本卡按[八周计划 §4.3](../../计划/高级AI框架开发工程师-八周证据冲刺计划.md#43-change-card-模板)问答共建。2026-11-07 确定两条条件分支：设备直传、双端 Host RDMA 中转；首版采用显式配置与启动校验，KV 加载失败安全收尾后采用 `fail`。
>
> 本卡是“若接入满足这些条件的目标平台，应如何设计”的方案，不作为已实施适配或性能成果。它不裁定用户其他项目的真实经历。证据为固定源码、机制推理与 B 级测试设计；实现、硬件正确性及性能均未在本卡中实测。

共同前提：目标平台的基础 prefill/decode 已可正确执行；P/D 使用同一模型、TP、cache 表示、dtype、布局与 block size；由 **D 侧 CPU 发起 PULL**。Host RDMA 可用是本卡的范围假设，需要在实际部署中验证。普通 Host TCP/socket 不纳入本卡；不由“云端数据中心”推定每个进程、容器或 backend 都已获得可用 RDMA 路径。

## 1. 固定仓库、文件与接入位置

vLLM commit：`d7ada3aace051fecec553c185225db2259c2ac6a`。下表是实现依据和候选改造入口，不代表已经修改代码；目标 NIXL native backend／驱动版本仍需另行锁定。

表内简写约定：`nixl/` 代表 `vllm/distributed/kv_transfer/kv_connector/v1/nixl/`；`kv_connector/` 代表 `vllm/distributed/kv_transfer/kv_connector/`；`v1/` 代表 `vllm/v1/`；`config/` 代表 `vllm/config/`。其他以 `vllm/` 开头的路径直接相对仓库根。

| 入口 | 固定位置 | 职责与适配判断 |
| --- | --- | --- |
| 平台声明 | `vllm/platforms/interface.py` L1410–1420：`get_nixl_supported_devices`、`get_nixl_memory_type`；`nixl/utils.py` L18–31 | 声明计算设备／transfer buffer 组合与内存类型；不是底层注册能力的实现 |
| 选择实际网络缓冲区 | `nixl/base_worker.py` L794–843、L1519–1527：`register_kv_caches` 的相关分支 | 直传选 `kv_caches`，中转选 `host_xfer_buffers` |
| 构造并注册 descriptor | 同文件 L1622–1630、L1870–1872 | 把实际区域、长度、memory type、device ID 交给 NIXL backend；需要真实注册与访问支持 |
| D 侧 PULL | `nixl/pull_worker.py` L554–567 | `make_prepped_xfer("READ", ...)`、提交与 handle 追踪；数据从 P 流向 D |
| Host 拷贝安装与分派 | `v1/worker/gpu_model_runner.py` L7081–7084；`kv_connector/utils.py` L207–241 | ModelRunner 安装 `copy_kv_blocks`，按方向分派到平台 copy 方法 |
| 保存与接收后处理 | `nixl/connector.py` L299–317；`nixl/base_worker.py` L2981–3037、L3191–3335 | P 的 Host 保存、D 的 H2D、完成／失败结果衔接 |
| 失败策略 | `config/kv_transfer.py` L88–92；`v1/core/sched/scheduler.py` L3432–3445、L2396–2408 | 首版选择 `fail`，不把失败 KV 当成功输入；清理前提由 worker／backend 保证 |
| 必要的外置扩展 | `kv_connector/factory.py` L95–121，`kv_connector_module_path` | 现有 hook 不足时可评估外置 connector／worker；不先断言一定要改 framework core |

表中简写按上述前缀展开。可从[本地固定源码](../../推理框架/references/vllm/)和[课程中的 source/test 说明](../../课程网页/八周计划/plana-jd-w3-failure-system-design.html#spine)定位。

## 2. 共用的职责、输入输出和调用契约

Scheduler 管理请求、缓存分配、交接 metadata 与调度等待；Worker 负责注册实际区域、提交／推进传输、衔接设备依赖并返回结果。两分支保持逻辑块到物理区域的映射、请求归属、成功可消费和安全释放的含义。

- **控制方向**：D 的 CPU 提交 PULL／READ。P 维护可读取的源状态、资源保留与相应通知／租约处理。
- **数据方向**：KV 字节从 P 到 D。CPU 发起与设备内存直传可以同时成立，不要求 GPU 直接敲 doorbell。
- **注册与就绪**：长期 cache／Host pool 可以预先注册；某次请求的 KV 是否已产生、哪些块可读取，是另一项条件，不能由 MR／descriptor 已存在推出。
- **结果接口**：结束结果与失败结果一并传递。`finished_recving` 不等于内容有效，要结合 `failed_recving`、必要后处理与消费依赖。
- **回收**：一次请求结束通常归还相应引用／块；不意味着立即注销整个共享 pool 的 MR。池和注册资源可以跨多次请求复用。

这里使用的是 READ，因此不要照搬此前 WRITE 主例的“源／目的描述”方向：D 的本地描述指向接收区；远端描述指向 P 的源区。按单次 verbs READ 的权限含义，P 源区需要允许远端读，D 接收区需要允许本地写。NIXL 在底层管理具体 key 和注册权限，vLLM 适配层不应自己伪造它们。

## 3. 两条条件分支与需要打通的能力

### A. 设备直传

```text
P 设备 KV → P RNIC → 网络 → D RNIC → D 设备 KV
                        D CPU 发起 PULL／READ
```

适配工作按依赖展开：

1. 核对目标设备分配能否被选定 NIXL backend 识别，device ID、地址范围和布局描述是否准确。若只有硬件／驱动具有直传能力，而当前 native backend 尚未支持，就需要补底层内存识别、导出／注册、访问与完成接口。
2. 在 platform adapter 声明实际支持的组合和 memory type；直传注册的应是实际设备 cache 区域。填写 `"VRAM"` 或扩充支持表，不会自动建立 RNIC 对目标显存的映射。
3. 把 P 的数据生产与网络读取连起来：远端读取获准开始前，源 KV 必须满足目标设备的可读条件。固定 `wait_for_save` 在直传分支没有执行通用设备同步，不能把函数名当作保证。
4. 把 D 的网络完成与设备消费连起来：明确 backend 的完成语义、设备可见性及消费 stream 的依赖；不把一个 handle 的 DONE 直接推广成任意 stream 可读。
5. 保留异常后的 handle、块与 peer 关联，按后端合同收尾。无法证明旧访问已停时，受影响区域不能回池或被重试覆盖。

固定 `_sync_device_after_direct_recv` 只在特定 ROCm＋Mamba、非 Host buffer 分支执行同步，并不是通用目标平台 hook。如果新设备需要不同的生产／接收同步，必须找出实际可插入的路径；可能需要外置 connector／worker 扩展，或补充核心接口，不能仅改配置。

### B. 双端 Host RDMA 中转

```text
P 设备 KV → D2H → P Host 源区 → Host RDMA → D Host 接收区 → H2D → D 设备 KV
                                  D CPU 发起 PULL／READ
```

1. 选择 Host transfer buffer，按 cache shape、dtype、stride 与块映射建立 Host pool。实际注册给网络后端的是 Host 区域；设备源／目标只参加本地拷贝，不因本次 Host RDMA 必须注册成 RDMA MR。
2. 实现或核对平台的 `swap_out_blocks_to_host` 与 `insert_blocks_to_device`，由 `copy_kv_blocks` 传入正确的块索引。不能把逻辑 block ID、物理块位置或 packed layout 再随意解释一次。
3. P 的 `wait_for_save` 在这一分支触发 `save_kv_to_host`。需要保证生产 → D2H → 网络读取的依赖，网络不得读取尚未准备好的 Host 副本。
4. D 成功完成网络接收后执行 H2D，再按设备／stream 合同允许消费；失败路径跳过成功加载后的拷贝／后处理。
5. 给 Host pool 设置容量和背压：没有安全可复用的槽时等待或拒绝新工作，不能覆盖旧网络／H2D 仍会读取的区域。

固定代码创建 CPU tensor 时没有显式 `pin_memory=True`。RDMA 注册为 RNIC 建立内存访问条件，不等于该 tensor 自动满足目标设备 runtime 的 pinned Host／异步拷贝要求。若目标 runtime 需要专门的 Host allocator 或注册 API，必须把它接入 pool 的分配与释放生命周期。

固定 CUDA copy 实现还包含索引 gather、`.to(device)`／`.cpu()` 与目标索引赋值，不能当作一条裸 memcpy。copy 回调返回后，后续计算仍需遵守平台与 stream 的顺序；`gpu_sync_allowed()` 只是调试许可，不执行同步。若改为异步 copy，必须显式接好 event／完成传播，不能让原本的 `None` 返回值偷偷改变含义。

## 4. 保持不变、adapter、底层后端与 core 扩展

| 层次 | 两分支共用 | 设备直传侧重点 | Host 中转侧重点 |
| --- | --- | --- | --- |
| 框架契约 | 请求／块映射、Scheduler／Worker 分工、完成与失败语义 | 网络完成后设备可消费 | H2D 及消费依赖纳入就绪含义 |
| Platform adapter | 设备类型、允许配置、已有平台入口 | memory type／设备 ID 声明；核对生产与消费 stream 合同 | 设备↔Host copy、索引与布局、必要的 Host allocator 接入 |
| NIXL／native transport | Host RDMA 和网络环境必须真正可用 | 目标显存识别、注册／导出、RNIC 访问和完成语义 | Host 注册与网络通路；不需要 RNIC 直接访问目标显存 |
| Connector／worker 扩展 | 已有接口表达不了目标平台需求时才增加 | 补足生产就绪、接收可见性或收尾的接入点 | 补足 pool 分配器、copy event 与终结结果的传播 |
| Framework core patch | 由具体缺口决定，不预设必需或完全不需 | 不能用支持表掩盖底层缺口 | 不能用返回值外观掩盖新增异步阶段 |

固定 NixlPullConnector 直接构造标准 worker，没有一个可以任意替换的通用 platform worker 工厂。采用外置 connector／worker 或增加 hook 时，要核对实例构造、metadata 与结果接口；基础 `get_transfer_results` 的 legacy 包装只带结束集合，不会自动补上完整失败传播。

## 5. Buffer、stream、ownership 与 lifetime

| 对象 | 直传分支的最低保留条件 | Host 中转分支的最低保留条件 |
| --- | --- | --- |
| P 设备源 KV | 网络已不再读取该区域；其他框架引用／协议保留也解除 | 设备→Host 复制链已不再读取该源区（含可能的 gather／临时拷贝）；实际释放仍看其他引用／保留策略 |
| P Host 源区 | 无此中转阶段 | 网络已不再读取 |
| D Host 接收区 | 无此中转阶段 | Host→设备复制链已不再读取该源区（含可能的 gather／临时拷贝） |
| D 设备目标 KV | 网络到设备的可见性及消费依赖满足后才能读；消费者／引用结束后回收 | H2D 与消费依赖满足后才能读；消费者／引用结束后回收 |
| handle、请求／尝试与块关联 | 失败不等于访问停止；保留到后端安全收尾，并使终结效果只生效一次 | 同左，且必须把新增 copy／中转槽依赖一起跟踪 |

注册资源的存活期与单请求引用分开：共享 pool 尚服务其他请求时，不能因某个 handle 完成就销毁注册或释放整池。软件代际可以拒绝迟到控制消息，但不能改写已经提交的旧 DMA 地址。

## 6. 选路、兼容性与错误传播

**已确定的首版策略。**显式配置 A 或 B，启动时检查该分支的实际条件；不满足则报错，说明缺失的是 backend、注册、拷贝还是同步能力。两分支作为受控配置分别验证，不在运行时静默切换，也不降级到本卡排除的 Host TCP/socket。

对已确认 KV 加载失败、旧访问按合同安全收尾后的请求，采用 `kv_load_failure_policy="fail"`。调度器错误结束请求；不把重算或重新传输加入首版自动恢复路径。失败期间的资源保护先于此业务策略：不能因为选择 fail，就立刻丢掉在途 handle 或归还仍被访问的块。

保留此前课程的异常约束：重复／迟到事件先核归属与是否已处理；新 peer 使用匹配身份的注册描述，旧本地资源按旧依赖清理；租约计时策略不单独证明旧访问停止。实际停止机制、不可恢复错误后的隔离／停用与资源上限需要在目标后端合同里明确；无法取得安全复用依据时，不能用更长 TTL 或强行 free 代替。

复用现有 NIXL 不等于这些安全要求已经全部得到证明。固定租约到期分支可以把请求加入 `done_sending`，但该分支没有核验远端旧访问已停止；目标后端若不能提供足够保证，还需评估租约、终结上报与回收接口的改造，不能只加平台声明就称整条故障路径安全。

固定版本的兼容边界也要进启动检查：Host staging 不支持 CSA-linear shared tensors，异构 block size 与 Host buffer 的组合也被拒绝；非 MLA 的初始化还有四维 cache 假设。本卡同 block size／同布局是首版范围，不外推所有 MLA、hybrid 或 packed cache 都自动支持。

## 7. Correctness 验证

完整故障矩阵及一个具体的 B 级受控用例见[PD/KV 故障矩阵与测试设计](../../推理框架/PD-KV故障矩阵与测试设计.md)。两分支在共用异常矩阵上各增加自己的数据路径检查：

- 共用：请求、尝试、块、peer／注册版本匹配；传输字节与预期状态一致；成功消费有明确依赖；失败不发布有效 KV；中间不提前复用，最终只归还一次且不残留。
- A：确认注册的确是目标设备区域、设备 ID 正确、P 生产就绪后才读；D 在 backend 完成与目标设备可见性条件满足后再消费。测试跨 stream 情形，不能只测试默认 stream。
- B：核对 D2H／RDMA／H2D 各自的实际缓冲区与块映射；让中转池吃紧，验证背压与四类缓冲区分别回收；若使用专门 pinned Host 内存，验证分配／注册／解除／释放配对。
- 两者分别覆盖空／尾块、部分片段、dtype／stride、容量边界及错误上报。特殊 cache 类型按该版本的真实支持条件另测，不因总字节相同就视为语义相同。

`test_kv_buffer_to_nixl_memory_types` mock 了 NixlWrapper，只检查 buffer 配置与 memory type；它不能证明真实设备内存已经注册或直传成功。软件状态测试、可控后端集成与真实设备验证分别声明范围；本卡没有执行这些测试。

## 8. 单设备、多设备与多节点性能验证设计

在 correctness 前提成立后，再比较两分支：

| 层次 | 保持一致的条件 | 观察量 |
| --- | --- | --- |
| 单设备 | 模型／KV 表示、片段大小、块选择及生产／消费边界 | D2H／H2D 时间、同步等待、Host pool 内存和临时分配；直传侧的生产／可见性衔接成本 |
| 多设备 | 相同 TP／布局、请求负载与拓扑记录 | 共享 RNIC／总线带宽、并发队列、CPU progress 占用、块池背压 |
| 多节点 | 同样的 payload、并发、计时起止与完成判据 | 注册／提交／网络／copy／消费等待分段，以及端到端 KV 交接、TTFT／ITL 和吞吐 |

无重叠基线先把各段开销分清；分块流水或重叠版本再用 trace 解释哪些阶段真实重叠、最慢阶段在哪里。不能把理论网络下界当成端到端实测，也不能仅因直传少了 Host 拷贝就预先断言它在所有负载下更快。没有设备结果时，这一节只是一套测量设计，不填写性能收益。

## 9. 证据等级、风险与待核验项

- **已确定的设计选择**：两分支学习推演；CPU 发起 PULL；同模型／TP／布局／block size；显式选路并启动校验；失败安全收尾后采用 fail；不纳入 Host TCP/socket。
- **实现依据**：本卡列出的固定 vLLM 路径、已有测试与接口结构。卡片中的目标平台工作清单属于方案设计，不声称已经做过代码修改。
- **必须落实到目标版本的能力**：native backend／驱动对设备或 Host 内存的注册访问；copy 与 stream 合同；生产就绪与接收可见性；查询、取消、释放和停止访问的保证；特殊 cache 支持及容量限制。
- **尚未取得的证据**：目标平台注册／数据正确性、故障恢复的真实设备行为、性能测量。已有 MoE／collective 项目事实不自动证明这些单边访问能力。
- **帮助归属**：两分支与首版策略由学习者选择；源码定位、接口边界和初稿整理由导师提供。资源依赖、重复事件、MR 归属及测试范围的理解依据另见[单元四账本](../../计划/八周冲刺进度/W3.md#lesson-plana-jd-w3-failure-system-design)。

## 固定来源入口

- [平台 hook](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/platforms/interface.py#L1410-L1420)、[设备支持组合](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/utils.py#L18-L31)。
- [实际注册与 memory type](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py#L1514-L1630)、[native 注册调用](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py#L1870-L1872)。
- [PULL 的 READ 提交](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/pull_worker.py#L554-L567)、[生产／保存 hook](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/connector.py#L299-L317)。
- [Host pool 与 copy callback](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py#L1280-L1333)、[D2H／H2D](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py#L2981-L3037)。
- [copy 分派](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/utils.py#L207-L241)、[CUDA 参考实现](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/platforms/cuda.py#L659-L680)、[ModelRunner 的调用与结果衔接](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/v1/worker/kv_connector_model_runner_mixin.py#L72-L100)。
- [接收后处理及特定同步分支](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py#L3191-L3344)、[Host buffer 的异构 block 限制](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py#L2780-L2787)。
- [外部 connector 加载](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/factory.py#L95-L121)、[legacy 完成包装](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/vllm/distributed/kv_transfer/kv_connector/v1/base.py#L416-L425)。
- [memory type 配置测试](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/tests/v1/kv_connector/unit/test_nixl_connector.py#L2996-L3040)、[恢复策略测试](https://github.com/vllm-project/vllm/blob/d7ada3aace051fecec553c185225db2259c2ac6a/tests/v1/kv_connector/unit/test_kv_load_failure_recovery.py#L38-L70)。
