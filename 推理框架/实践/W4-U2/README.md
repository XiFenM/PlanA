# W4-U2：单卡服务的调度预算对照

本包执行用户于 2026-11-12 接受的 [W4-U2-P1 约定](../../../计划/八周冲刺进度/历史记录/W4-学习验收记录.md#w4-u2-p1)。Agent 维护方法与脚本，学习者负责事前预测、运行和结果解释。只比较一个 BF16 小模型的两档预算，另采一个短 trace。包修订为 `2026-11-12.3`；约定仍为版本 1。已完成的设备测量使用 `.2`，`.3` 只修正 trace 派生索引，旧测量不重跑。

## 1. 启动 Radeon Cloud 实例

在已提供截图的控制台选择：

- 类型：**Notebook**；规格：**1 GPU**。
- 镜像：`ai-academy_in_radeon-cloud:vllm-openai-rocm-v0.26.0`，使用不带额外后缀的这一项。
- 自动销毁：可保留截图中的 **2 小时**作为首个窗口。准备与运行时间取决于实际下载和设备情况，不保证完整实验必在该窗口结束。
- 页面提供持久 `/workspace` 时选用它；没有该选项则使用临时工作区，并及时下载返回包。销毁实例会删除临时工作区。

截图中的 `16 核 · 55GB` 是实例规格，不能据此认定 GPU 显存。先由脚本记录实际 GPU、显存、PyTorch/HIP 和 vLLM 构建。平台镜像名不是已经通过兼容性检查的证明。

实例就绪后打开 JupyterLab，将 `W4-U2-packet-20261112.3.zip` 上传到 `/workspace`，打开 Terminal：

```bash
cd /workspace
python3 -m zipfile -e W4-U2-packet-20261112.3.zip .
cd W4-U2
python3 run.py preflight
```

如果 JupyterLab 默认目录不是 `/workspace`，先在 Terminal 执行 `pwd`，把命令中的目录替换为 ZIP 实际上传的位置。所有 Python 文件与 `model_manifest.json` 应留在同一个 `W4-U2` 目录中。

**先把终端打印的“返回包”下载并发回对话。**这一步不下载模型，不启动 vLLM 服务，也不测性能；只进行环境查询和一个无计时的 2×2 BF16 功能检查。没有 GPU、版本不符或 CLI 缺少所需参数时，脚本保存原因后退出，不转为 CPU 性能测试，不自动安装软件。

包内要求 Linux、Python 3.10+、vLLM `0.26.0`（允许同版本构建后缀）、可用的 ROCm PyTorch/BF16，以及已安装的 Transformers、Hugging Face Hub、safetensors。保守预检要求至少 12 GiB GPU 显存和 12 GiB 可用磁盘空间；CPU FP32 参考建议有至少 16 GiB 可用主机内存。不要把预检门槛当成显存占用实测。

## 2. 核对环境后准备固定输入

环境核对通过后，在同一目录运行：

```bash
python3 run.py prepare
```

此命令会：重新检查环境；下载固定 revision 的公开模型；核对权重 SHA256 及配置／tokenizer 的 Git blob hash；生成并保存固定 token IDs。没有大规模 GPU 运行，也没有性能结果。

模型为 `Qwen/Qwen2.5-1.5B-Instruct`，revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`。权重文件为 3,087,467,144 bytes，约 3.09 GB；tokenizer 等文件另占少量空间。下载缓存留在 `cache/`，返回包不会包含模型权重。首次下载会占用实例运行时间。

如果平台已挂载**同一 revision** 的完整模型，可以改用 `python3 run.py prepare --model-dir /实际模型目录`；仍会逐文件验证。脚本不安装或升级 PyTorch、vLLM、驱动或系统工具。下载失败时返回失败包，不要自行把 revision 换成 `main`。镜像已设置 `HF_ENDPOINT` 时会沿用它，但仍验证固定内容的哈希。

每次 `prepare` 新建 `runs/case-时间-随机号/`，不会覆盖旧目录。`current_run.json` 只是最近一次成功准备的路径指针。

## 3. 事前预测与正式运行

查看下面的固定方法后，先在对话中提交自己的预测：预算变化可能如何影响 TTFT、ITL 和吞吐，依据是什么，哪些观察会推翻你的判断。包内不预填答案；预测不符合实测不算练习失败，关键是能解释支持、反证和未知。

把已提交的预测原文保存为 UTF-8 的 `prediction.txt`，再运行：

```bash
python3 run.py run --prediction-file prediction.txt
```

脚本会在正式运行前保存预测原文、时间与源码快照，随后自动组织服务启停、独立正确性、预热、六轮测量和单独的短 trace。主实验循环设 80 分钟截止，网络请求、排队任务、服务启动和参考计算共享剩余时间；清理进程、导出 trace 与压缩结果需要额外收尾时间。不要因此将云端自动销毁窗口卡在最后一秒。

每轮完成后都会打印一个返回 ZIP，结束或失败时还会再生成包含最新状态的完整 ZIP。保留最后一份完整包即可交回；较早的包是同一次运行的阶段快照。数据仍在实例里时，也可以手工重新打包：

```bash
python3 run.py pack
```

在 JupyterLab 文件栏进入 `W4-U2/exports/`，对终端指定的 ZIP 选择 Download，再上传回对话。自动销毁不会替你下载文件。完成保存后按平台界面结束实例；脚本只关闭自己启动的 vLLM 进程，不管理云账户或销毁实例。

## 4. 固定实验方法

| 项目 | 本包设置与原因 |
| --- | --- |
| 服务模型 | 固定 revision 的 Qwen2.5-1.5B-Instruct，BF16，TP=1；同一张卡和同一软件环境 |
| 唯一主要变量 | `max_num_batched_tokens` 为 **512 / 2048**；读取实际 `VllmConfig`，核对另一调度额度为相同值或按源码继承 |
| 执行条件 | `max_model_len=4096`，`max_num_seqs=16`，GPU memory utilization 0.70；启用 Chunked Prefill，关闭 prefix caching、异步调度和 speculative decoding |
| eager | 两档都 `enforce_eager=True`，避免本练习引入 graph capture 与编译覆盖差异；结论仅限该 eager/synchronous 条件，不代替生产最优配置 |
| 输入 | 48 条固定合成技术文本；tokenizer 只运行一次，短／长 prompt 精确为 256／3072 token，交替排列各 24 条；每轮复用同一份 token IDs |
| 输出 | 每请求 128 个 token，temperature=0，固定 seed，ignore_eos=True；返回 token IDs 与 usage 交叉核对。保留特殊 token 文本，输出内容用于受控执行，不是模型能力评测 |
| 负载 | 全部请求在轮次开始进入客户端队列，上限 8 个同时在途，完成后补位；这是有限请求池的 closed-loop 饱和测试，不冒充固定外部到达率 |
| 预热 | 每次新服务启动后，先执行固定前 8 条 prompt、每条输出 32 token；预热不计入正式指标 |
| 重复与顺序 | **512 → 2048 → 2048 → 512 → 512 → 2048**，各三轮；每轮重新启动同一模型服务，避免只比较先后各一组，但不能据此声称完全消除热状态漂移 |
| 正确性位置 | 每轮计时前后校验 4 个固定输入，长度为 32／128／768／3072 token，各生成 8 token。验证与参考计算不计时 |
| profiler | 六轮性能测量不配置 profiler；之后另起服务，用预算 2048 的 4 条短输出请求采集一次 Torch Profiler CPU＋GPU trace |
| 网络范围 | 客户端和服务在同一实例，通过 `127.0.0.1` 访问；不经过公网 Model API 网关，结果不覆盖互联网传输体验 |

服务的实际配置在启动后从该版本的本地管理接口读取，只保存模型、调度、缓存等白名单字段。原始管理响应中的环境信息不会落盘。服务只绑定 loopback；没有开放外部 API、替换模型权重或修改 vLLM 调度源码。

## 5. 独立正确性与性能统计

正确性参考使用 **同一权重的 Transformers CPU FP32/eager 实现**。对服务器实际生成的 token 前缀进行 teacher forcing，逐个位置计算概率：实际 token 的 logprob 绝对差不超过 **0.25 nats**，相对于参考 top-1 的 logprob 差不超过 **0.10 nats**。两项都要逐位置通过；后者容纳 BF16 的近似平局，不用“请求返回成功”替代数值验证。

修订 `.2` 优先使用镜像已有的 oneDNN 执行 CPU Linear，并显式设置、回读 IEEE FP32。只转换线性层的存储／执行形式，eager attention、权重数值、输入和阈值不变；同时检查参数与 buffers 均在 CPU、浮点值均为 FP32。没有可用的 oneDNN 路径时，保留并记录 dense 后端，不隐式降低精度。实际 Radeon Cloud 镜像的 dense CPU 路径使原参考超时，这属于参考执行方式的适配问题，不是 GPU 服务或学习者理解失败。

控制台会显示模型加载、每个参考输入及保存报告的进度；长输入处理时每 30 秒显示心跳。完整输出即时保存在每轮 `validation_before/reference.log` 或 `validation_after/reference.log`，超时也保留。参考计算期间 vLLM 的 Running／Waiting 为 0 是正常现象，服务在等待 CPU 参考完成；参考时间不进入服务性能统计。

上述阈值在结果出现前固定，是本练习小型数值一致性检查，不代表模型总体质量或所有输入正确。若同一输入和完整生成前缀没有变化，后续验证可复用已经独立计算的 FP32 概率；仍重新核对服务器概率，前缀改变时重新运行参考。报告保留参考来源和哈希。失败会停止有效性能汇总，不自动放宽阈值。

逐请求原始记录包括请求 ID／顺序、输入长度、发送前队列等待、发送起点、非空输出消息的接收时刻、生成 token IDs、usage、结束原因及错误。统计使用同一个客户端单调时钟：

- TTFT：从实际发送起点到首个非空输出消息，不含此前客户端队列等待。
- E2EL：从发送起点到最后一个非空输出消息，不含 usage 尾包与连接收尾。
- TPOT：首末非空输出消息间的时间，除以实际生成 token 数减一。
- raw ITL：相邻非空输出消息间隔；一个消息可能包含多个 token，因此不是逐 token 间隔。
- 输出吞吐：成功请求的实际生成 token 总数，除以该轮从开始到全部请求退出的完整窗口；窗口包含客户端排队与收尾。

失败和超时请求不会从原始文件消失。P99 明确标为**探索性观察**，每轮请求级样本只有 48 个；三轮的统计量分别保留，再给出轮次统计量的中位数与范围，不把这些数值改称合并全部样本的分位数。范围不是置信区间，也不据它作生产 SLO 承诺。

结果解释先结合预测检查方向、跨轮波动和可比条件。可能支持预测、与预测相反，或证据不足；没有必须达到的加速百分比。

## 6. 短 trace 的解释边界

短采集打开 shape、内存记录与细粒度 CPU scope，关闭 stack 收集，输出 gzip trace。开始／停止接口返回 HTTP 200 不代表 GPU 捕获成功：脚本还要求找到 GPU kernel 事件和 worker 的 `execute_context_…_generation_…` 批次标注。

批次标注可以显示 prefill／decode 请求数与每批调度 token 数。它**没有逐请求 ID 映射**；并发情况下不能据此自动声称某个 kernel 属于某条 HTTP 请求。客户端时钟、trace 时钟与 Host scope 的结束也不能直接当作同一设备完成边界。请求、批次与必要依赖的可关联范围在实际返回后逐项核对。

`.3` 的索引按原始 `cat` 分开 Host scope 与 `gpu_user_annotation`：`batches` 只计带实际 token 的 Host execute scope，GPU 同名范围放在 `gpu_batch_ranges`，零 token Host scope 另存。旧 `.2` 索引只匹配名称，可能将同一批次的 Host／GPU 范围重复计数，并把 GPU duration 误标为 Host duration；原始 trace 可重新分类，干净计时不受影响。

单卡没有 collective 时如实记录。未出现 allocator/copy 等事件时，应先检查采集覆盖与窗口，不把“未看见”写成“不存在”。若只有 CPU trace 或 profiler 不支持，干净性能文件仍保留，状态为采集不完整，返回完整包后再处理，不先重跑全部 benchmark。

## 7. 返回包与失败处理

| 文件／目录 | 用途 |
| --- | --- |
| `source/`、`source_manifest.json` | 本次实际脚本快照及 SHA256 |
| `method.json`、`prediction.json` | 事前固定方法与学习者预测 |
| `environment_*`、`model_*verification.json` | 实例与软件信息、固定模型的文件身份 |
| `inputs.json` | 全部固定输入 token IDs、请求顺序与生成条件 |
| `round-*/command.json`、`effective_config.json`、`server.log` | 实际启动方式、生效配置与服务日志 |
| `round-*/validation_*` | 独立参考、重复校验及原始正确性响应 |
| `round-*/requests.jsonl`、`summary.json` | 逐请求观测与每轮统计 |
| `performance.json` | 六轮干净性能比较；不是 GPU trace 的耗时汇总 |
| `profile-budget-2048/` | 单独采集记录、原始 trace 与批次索引 |
| `failure_*.json`、`status.json` | 失败原因与最后完成的阶段 |
| `ARCHIVE_SHA256.json` | 返回 ZIP 内文件哈希；不包含模型权重 |

出现异常后返回现有 ZIP 与终端提示即可，不先升级依赖、放宽阈值或改调度参数。每个准备目录只运行一次；重跑时重新 `prepare`，会复用已验证的下载缓存并创建新结果目录，旧结果保留。

## 8. 本机验证与来源

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

标准库测试覆盖流式协议、总截止时间、失败记录、指标独立复算、正确性评分、配置白名单、哈希、防覆盖、打包及模拟运行流程。没有安装 PyTorch／Transformers 的机器会明确跳过 tiny Qwen2 数值测试；模拟服务与模拟 trace 不属于设备实证。真实模型加载、ROCm 执行和 GPU trace 的验证仍由云实例完成。

`.2` 修复在用户的现有实例上进行了针对性验证：相同四个输入、32 个生成位置均满足原判据，oneDNN Linear 配合原 eager attention 的 CPU 参考约用时 331 秒；这是参考计算诊断，不是服务性能结果。旧的失败运行保留；升级后用缓存模型重新 `prepare` 创建新目录，继续使用已给出的预测，不覆盖旧 case 或将失败尝试合并进正式六轮。

接口核验基于 vLLM `v0.26.0`（commit `568afb3a13806beb53bb2e6bd518269357b237c0`），不把课程讲解使用的另一固定 commit 当作这个镜像的实际构建：

- [CLI 参数](https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/engine/arg_utils.py)：本版本使用 `--no-enable-log-requests`，没有旧的 `--disable-log-requests`。
- [流式 token IDs 与 usage](https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/entrypoints/openai/completion/serving.py#L403-L487)、[请求协议](https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/entrypoints/openai/completion/protocol.py)：使用显式 token IDs，核对输入输出 usage。
- [实际服务配置](https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/entrypoints/serve/dev/server_info/api_router.py)、[Profiler 配置](https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/config/profiler.py)。
- [worker 批次标注](https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/v1/worker/gpu_worker.py#L967-L1076)、[worker CPU/GPU profiler](https://github.com/vllm-project/vllm/blob/v0.26.0/vllm/v1/worker/gpu_worker.py#L1180-L1231)。
- [实际 Torch 构建的 oneDNN Linear](https://github.com/pytorch/pytorch/blob/d0c8b1f364ecacff4dd8bc06a645d0fb9324cd37/torch/utils/mkldnn.py#L1-L30)：参考侧 dense 输入／输出与 FP32 线性层适配，不改变服务端 BF16 后端。
- [模型固定配置](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/989aa7980e4cf806f80c7fef2b1adb7bc71aa306/config.json)、[平台镜像用途](https://github.com/AMD-AIM/radeon-cloud-docs/blob/13778f8a87cf88c065207e717e4a7152225f1ce8/src/content/docs/guides/images.md#L76-L82)。
