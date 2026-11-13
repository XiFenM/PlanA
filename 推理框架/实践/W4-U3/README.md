# W4-U3：BF16 与官方 AWQ 的 GPU 部署对照

本包执行 2026-11-13 接受的 [W4-U3-P1 版本 1](../../../计划/八周冲刺进度/历史记录/W4-学习验收记录.md#w4-u3-p1)。包版本为 `2026-11-13.5`：保留版本、缓存及聊天模板适配，并识别目标环境已观测的明确BF16 out_dtype不支持诊断。模型、负载、数值门槛与分工不变。Agent 维护方法与脚本，学习者负责事前预测、在自己的新 GPU 实例运行及结果解释。

**本次没有完整模型 CPU 推理、CPU 性能对照或整模型 CPU FP32 参考。**只有一个真实量化投影的独立 GPU FP32 参考；CPU 用于文件校验、请求发送、评分及汇总。没有 GPU 时停止，不回退到 CPU 模型。

## 1. 新实例先预检

原 U2 实例已释放。使用单张已分配 AMD GPU 的 Linux 环境；本包明确支持已核验的 **vLLM 0.26.0／0.33.0**（允许各自构建后缀）和 ROCm PyTorch，不自动接受其他版本。2026-11-13 返回的新实例实际为 `0.33.0+rocm72`；按实际构建选择对应 CLI 参数与来源版本，不需降级环境。镜像名字不替代兼容性检查，脚本不租用实例、不安装依赖、不连接旧 SSH 端点。

`.1` 预检的两个 CLI 报错来自帮助文本检查：0.33 将旧 `--no-enable-*` 别名隐藏但仍接受，现改用其可见的 `--disable-prefix-caching` 与 `--disable-log-requests`。准备阶段会把实际选中的版本分支写入 `method.json`，每轮命令和局部参考也记录它。0.26 教学材料和旧测量保持原版本归属。

保守预检要求一张可见 GPU、至少 12 GiB 显存、16 GiB 可用磁盘，以及镜像中已有 Transformers、Hugging Face Hub 和 safetensors。2×2 的 BF16／FP16／FP32 GPU 功能检查不计时，不是性能结果。实际 AWQ 支持留到预测保存后的局部参考与模型启动阶段。

把 `W4-U3-packet-20261113.5.zip` 上传到 JupyterLab 工作目录，在 Terminal 中运行：

```bash
cd /workspace
python3 -m zipfile -e W4-U3-packet-20261113.5.zip .
cd W4-U3
python3 run.py preflight
```

如果上传目录不是 `/workspace`，先用 `pwd` 确认并替换第一行。**先下载终端打印的返回 ZIP 并发回对话。**此步不下载模型、不启动完整服务、不做正式计时。预检失败也会留下原因与返回包。

## 2. 准备固定模型与输入

环境核对后执行（已返回预检或下载失败包的同一实例，可更新包后直接执行；此命令仍先重新预检，通过后才下载）：

```bash
python3 run.py prepare
```

两份发布物固定在：

| 角色 | 模型与 revision |
| --- | --- |
| BF16 基线 | `Qwen/Qwen2.5-1.5B-Instruct@989aa7980e4cf806f80c7fef2b1adb7bc71aa306` |
| AWQ 候选 | `Qwen/Qwen2.5-1.5B-Instruct-AWQ@3ecffa0ceb27851800f45519bab9c457a04405e1` |

下载总量约 4.73 GB；固定 SHA256／Git blob hash 见 `models_manifest.json`。脚本使用公开访问、不请求 Hugging Face token，并验证每个文件；已配置的 HTTPS `HF_ENDPOINT` 可沿用，但不能改变固定内容的校验。缓存和权重不会放进返回包。

`.3` 先检查缓存中的实际内容；已有完整且通过固定哈希的文件不再向下载站发起该文件请求。两份模型的 LICENSE 与四个 tokenizer 文件在 manifest 中完全相同，可在复验实际源文件、复制到临时文件并再次校验后复用；不按文件名猜测兼容性。只请求仍缺失或校验不符的文件，已知坏文件会强制重下载，不能用Hub的旧本地元数据替代内容验证。

对429、500／502／503／504或明确网络超时最多尝试3次，中间等待2秒和4秒；每次重新确认还缺哪些文件。403／404、磁盘错误、最终哈希失败直接保留失败。SDK单次下载自身的耗时不由这两个等待时间限定。脚本不切换 `HF_ENDPOINT`，并把下载尝试写入 `*_acquisition.jsonl`。失败后再次 `prepare` 会保留旧case，继续使用同一个缓存。

已有对应 revision 的完整模型目录时，可以使用 `prepare --bf16-dir /path/to/base --awq-dir /path/to/awq`，仍逐文件核验。没有路径的一侧按固定 revision 下载。

准备阶段检查结构、tokenizer 和 chat template 一致，生成固定性能 token IDs 与32条质量任务，不进行完整模型推理。每次新建 `runs/case-.../`；成功后 `current_run.json` 指向该目录，旧目录不覆盖。

聊天模板调用显式使用 `return_dict=False`，取一维整数token列表；不会把Transformers5.20默认返回的BatchEncoding对象误作列表。该参数只明确返回容器，模板、题目、标签和评分规则不变。

**来源边界**：官方 AWQ model card 指向原模型仓库，但没有量化底座的确切 commit／权重哈希。两边结构与 tokenizer 一致，仍不能证明来自相同原始权重 revision。本包比较两份固定发布物的部署表现，不把结果称为已证同源的纯权重量化单变量收益。

## 3. 先给预测，再运行

先在对话里给出你对权重／KV 容量、TTFT、ITL、吞吐及小任务质量变化的预测、依据和反证条件。预测不符合结果也可以完成练习；关键是结果前有可检验的判断，结果后能解释证据。

把自己的预测原文保存为 UTF-8 的 `prediction.txt`，运行：

```bash
python3 run.py run --prediction-file prediction.txt
```

脚本先保存预测，再执行 GPU 局部参考、两模型质量评测与六轮干净计时。包内不提供预测答案，不预填该文件。一次准备目录只启动一次正式运行；需要重跑时重新 `prepare`，复用已核验的缓存并保留旧结果。

主 GPU 流程共享80分钟截止时间；环境查询、校验、进程清理与打包另需时间。服务启动单次最多600秒，局部参考每种 dtype 最多360秒，请求也有总期限。运行中每轮落盘并打印阶段返回包，失败时保留现有日志和原始记录。

完成或停止后，下载终端打印的最后一份完整 ZIP。也可执行 `python3 run.py pack` 对已有结果打包。包内不会替你下载返回 ZIP，也不管理云实例的自动销毁。先保存结果，再按平台操作结束实例。

## 4. 固定比较方法

| 项目 | 设定及口径 |
| --- | --- |
| GPU／软件 | 同一次运行的同一可见 AMD GPU与同一vLLM构建；显式选择0.26.0或0.33.0分支，准备后软件或设备身份改变即停止 |
| BF16 服务 | 明确 `dtype=bfloat16`，未量化 |
| AWQ 服务 | 4-bit、group128、zero point、GEMM 格式；先检查 BF16，只有明确的生产路径兼容性异常才尝试 FP16。数值失败、OOM、缺依赖或超时不授权 dtype 后备 |
| dtype 差异 | 若选 FP16，单独报告激活／相关执行类型变化，不将其隐藏成只改权重位数 |
| 调度／缓存 | token预算2048、max_num_seqs16、max_model_len4096、TP/PP1、block size16、utilization0.70，KV dtype为auto；Chunked Prefill开启，prefix caching和异步调度关闭 |
| eager | 两边都 enforce_eager；不加 profiler，不进行图捕获／参数扫描 |
| 性能输入 | 48条固定合成技术文本，256／3072输入token各24条、交替排列；两模型共用同一份token IDs |
| 性能输出 | 每请求128token，temperature0、ignore_eos=True，核对token IDs与usage；它们是受控工作量，不用于任务质量判断 |
| 负载 | 48请求同时进入客户端队列、并发上限8、完成后补位；有限请求池，不是固定外部到达率 |
| 顺序 | BF16 → AWQ → AWQ → BF16 → BF16 → AWQ，每轮重新启动服务，各三轮 |
| 预热 | 每次服务启动后先跑固定前8条prompt、各32输出token，不计入正式指标 |
| 短检查 | 每轮前后一个固定32token输入、生成8token并检查协议与有限logprob；它不是独立参考 |
| 网络 | 同一实例内的 `127.0.0.1`，不覆盖公网网关与互联网时延 |

在结果出现前，`method.json`、输入文件、包源码及哈希均冻结。脚本会读取实际服务配置的白名单投影，核对模型路径、量化方式、dtype、调度、缓存与 profiler 状态；不保存包含环境变量的原始 `/server_info` 响应。

### GPU 局部独立参考

只读取 AWQ checkpoint 的 `model.layers.0.self_attn.q_proj`：qweight、qzeros、scales及存在时的bias。独立位解包恢复数值，不调用生产反量化函数作为参考；输入和 scales 按实际服务 dtype 转换，再用 GPU FP32 matmul 计算参考，禁用 TF32。没有完整模型 CPU 加载。

生产侧调用真实 vLLM `AutoAWQLinearMethod.process_weights_after_loading/apply`，固定 M=1与256，记录实际算子调用与shape/dtype，分别覆盖该普通 dense fallback 的两条分支。0.33 的 post-load 继承基类空操作，手工注册的普通 Parameter 仍适用；两个已核版本的 apply 与 AWQ Triton 数值路径一致。它不证明完整服务所有层、所有形状或其他 kernel 正确。

事前固定门槛如下；全部结果还须有限，shape/dtype符合预期：

| dtype | 相对 L2 误差 | 最大绝对误差 |
| --- | --- | --- |
| FP16 | ≤0.01 | ≤0.001 + 0.05 × 参考 RMS |
| BF16 | ≤0.04 | ≤0.001 + 0.20 × 参考 RMS |

相对 L2 为误差范数除以参考范数（分母下限1e-12）。这是固定正态输入、同一量化权重下的工程一致性门槛，BF16留出较宽舍入／累加余量；不是数学最坏界、量化质量门槛，也不在看到结果后调整。它们与 U2 的 logprob 容差无关。检查未通过先停止计时，保留失败，而非放宽阈值。

目标镜像已在BF16的M=1分支报告 `out_dtype=bfloat16 is unsupported`。`.5`将这一明确编译诊断识别为兼容性受限，从而允许约定内的FP16尝试；它没有修改Triton kernel或任何误差阈值。FP16仍须独立通过两种shape的原定数值门槛，原BF16失败记录保留。

### 32条固定任务

字段提取和短事实定位各16条，带干扰项。答案由构造记录直接给出，独立于两模型；准备时保存题目、标签、chat template生成的token IDs和哈希。每个模型在正式计时前各评测一次；temperature0、最多32输出token、自然EOS。只去掉输出首尾空白后做exact match，截断算该题错误。

逐题原始输出、得分、BF16正确而AWQ错误的题目以及反向变化均保留。传输／协议失败会阻断性能比较；任务得分低或下降则是需要解释的有效结果，不要求量化优于基线。这是32条小任务的观察，不作生产质量、统计显著性或整体模型能力保证。

## 5. 指标与显存

复用U2的流式观测方法，按原始时戳重算：TTFT从实际发送到首个非空消息，排除客户端发送前等待；E2EL到最后非空消息；TPOT用首末消息间隔除以输出token数减一；raw ITL是非空消息之间的间隔，不自动当成逐token间隔。输出吞吐使用完整请求窗口，包括排队和收尾。

逐轮保存绝对值、统计量与原始请求；再给三轮统计量的中位数及范围，不把它们改称合并样本分位数。P99只作探索，范围不是置信区间，没有必须达到的加速百分比。

显存分三种口径保存：

- **模型加载占用**：vLLM日志报告的内存变化，保留原文和GiB精度，不伪装逐张量精确字节数。
- **KV容量**：启动日志和实际配置中的池容量／块数，不是当前活跃请求使用量。
- **设备采样**：正式请求窗口附近每秒读一次AMD sysfs，必要时用已有rocm-smi；采样器不创建HIP context。按短预检返回的PCI BDF关联逻辑GPU，不能关联时明确留缺口，不取“第一张卡”或跨卡求和。

采样最大值可能遗漏瞬时峰值，也可能包含同卡其他进程；不等于worker的allocator峰值。保存采样间隔、有效／失败样本和最大间隙。设备映射、采样或加载／KV日志不完整时，保留有效性能文件，状态为 `measured_memory_incomplete`，返回码2；不要因此先把六轮全部重跑。

## 6. 返回包与本机验证

关键文件包括 `source/`及源码哈希、`method.json`、`prediction.json`、两个模型的校验结果、`pair_verification.json`、性能／质量输入、`gpu_reference/`、两份质量报告、六个`round-*`目录及 `performance.json`。每轮保留命令、生效配置、服务日志、原始请求和显存报告；失败另有 `failure_*.json`、`status.json`。返回ZIP附条目SHA256，不含权重、缓存或旧ZIP。

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

标准库测试覆盖协议、固定输入、标签评分、独立解包的已知值、失败分类、配置投影、dtype后备限制、显存映射与采样、预测顺序及失败保存。可选GPU测试没有满足依赖时明确跳过。本地假服务和模拟流程不作为GPU实测；真实镜像加载、Triton编译及模型运行仍须在新实例验证。

通用代码从只读U2包派生，来源文件SHA256保存在 `source_provenance.json`，包运行时不依赖U2目录。量化路径固定参考 [vLLM 0.26／568afb3a](https://github.com/vllm-project/vllm/blob/568afb3a13806beb53bb2e6bd518269357b237c0/vllm/model_executor/layers/quantization/auto_awq.py#L858-L960)与[vLLM 0.33／4ba787ec](https://github.com/vllm-project/vllm/blob/4ba787ec9959e566d3b587a796dff07673324da5/vllm/model_executor/layers/quantization/auto_awq.py#L803-L911)；[0.33 CLI别名实现](https://github.com/vllm-project/vllm/blob/4ba787ec9959e566d3b587a796dff07673324da5/vllm/utils/argparse_utils.py#L120-L179)。模型来源见[官方AWQ固定配置](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-AWQ/blob/3ecffa0ceb27851800f45519bab9c457a04405e1/config.json)与[model card](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-AWQ/blob/3ecffa0ceb27851800f45519bab9c457a04405e1/README.md)。
