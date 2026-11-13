# W4-U1：MatMul 模型与实测对照

本包执行已确认的 [W4-U1-P1 练习约定](../../../计划/八周冲刺进度/历史记录/W4-学习验收记录.md#w4-u1-p1)。只运行一个 MatMul 的两个 M 值；学习者负责事前预测、执行和事后解释，Agent 维护脚本与方法。模型来自[单元一课程页](../../../课程网页/八周计划/plana-jd-w4-validation-interview.html)，页面不作为实测证据。

## 1. 租用前选择环境

- 正式测量支持 **Linux、Python 3.10 或更新版本、已核验的 PyTorch CUDA 构建、原生 BF16 NVIDIA GPU（compute capability ≥8）**。已核验 PyTorch 2.9.x 正式版（源码基线 `v2.9.0`），以及用户返回的 **2.13.0、git `cf30153c4c131c8164ee7798e5022d810682e2cb`**；2.13.0 同时匹配版本和构建才能放行，不笼统放行后续 patch 或开发版。实际版本、源码依据和包修订号随运行保存。
- 本课可选 **单张 A100 40GB**，无需多卡或 80GB；优先使用已能运行 PyTorch 2.9.x 的镜像。A100 的 BF16 运算及 FP32 累加依据见 [NVIDIA Ampere 指南](https://docs.nvidia.com/cuda/ampere-tuning-guide/index.html#improved-tensor-core-operations)。这只是本课的运行选择，不改变后续单元的 AMD 取材安排。
- 建议独占一张卡；使用 MIG 或共享资源时，返回准确的分区和共享条件，不能套用完整物理卡的峰值。脚本检查至少 2 GiB 可用显存；主机建议至少 4 GiB 可用内存，用于固定输入生成和全输出误差检查。资源建议不代表已在某一租用实例验收。
- 不下载模型、不安装 profiler、不编译 kernel。本包仅依赖 Python 标准库与 PyTorch，所有输入为固定种子的合成数据。
- **ROCm、其他尚未核验的 PyTorch 构建先运行环境检查并返回信息。**脚本会保存环境后停止正式测量，原因是尚未核验该具体组合的精度路径，不能把 Python 开关的名称与回读值当成跨平台保证。

如镜像没有合适的 PyTorch，先返回版本与驱动信息，由 Agent 按 [PyTorch 官方历史版本说明](https://pytorch.org/get-started/previous-versions/#v290)确定安装命令；脚本不会自动安装或替换软件。

## 2. 第一步：只检查环境

把本目录的 `harness.py`、`test_harness.py`、`README.md` 一起复制到 GPU 机器的同一目录，然后在该目录执行：

```bash
python3 harness.py preflight
```

多卡机器用 `--device` 选择**当前进程可见**的独占卡编号，例如独占 GPU 1 时执行 `python3 harness.py preflight --device 1`。不要根据某一时刻频率较低就推断那张卡空闲或已分配给自己。成功时打印 `ready_for_prediction` 对应的中文提示，并给出新建的结果目录。此步骤不执行 MatMul，不采集性能。

返回该目录里的 `environment.json`，并说明是否独占、是否 MIG。环境未通过也返回这个文件，不需要先自行调试。缺少 PyTorch／GPU 时退出码为 2，不会偷偷转成 CPU 性能测试。

Agent 依据实际 GPU 型号／分区、软件与计算模式核对设备资源能力及模型前提后，你在对话中提交事前预测。预测内容是：M 从 128 变为 256 时，工作量、流量预算和耗时可能怎样变化；说明依据、成立条件，以及什么结果会推翻预测。这里不预写预测答案。

## 3. 第二步：预测之后运行

环境核对完成、预测已提交之后，再执行以下命令，把引号内容换成你自己的预测原文，并把 `--device` 的数字换成环境检查时选定的同一张卡。正式运行必须明确指定编号，以免多卡机器误用默认的 GPU 0：

```bash
python3 harness.py run --device 0 --prediction '在这里填入已提交的预测、依据及成立条件'
```

`--prediction` 只保存文字和时间，不判定学习者是否独立作答。包里没有预填答案。每次运行都会新建 `runs/run-<时间>-<随机标识>/`；已有目录和文件不会覆盖。

命令结束后返回**整个新生成的目录**。无论通过或失败，都保留原文件；若重跑，保留两次结果。无需写额外实验报告，后续在对话里解释数据即可。

## 4. 固定方法与指标含义

| 项目 | 本包采用的设置 |
| --- | --- |
| 数学任务 | `C=A@B`，M 为 128、256，K=5120，N=25600；无旧 C 读取、bias、激活、通信或量化 |
| 数据与布局 | 连续行主序 BF16 A/B/C；CPU 固定随机种子 20261110，A 的标准正态样本除以 √K 后转 BF16，B 的标准正态样本转 BF16；A128 是 A256 的前 128 行，共享同一个 B |
| 精度 | 新 `fp32_precision` 接口设置 IEEE FP32，禁用 CUDA BF16 reduced-precision reduction 并回读；不混用旧 `allow_tf32` 接口，不启用 autocast |
| 参考 | 从实际 BF16 值提升到 FP32，再在所选 GPU 上以 IEEE FP32 做全矩阵参考；引用的是计算设置与源码合同，不声明检查过底层所有指令 |
| 正确性 | 输出和参考都有限；`||C−Cref||₂/||Cref||₂ ≤ 0.01`，且全输出最大绝对误差 `≤ 0.01×max(abs(Cref))+0.001`；两项同时满足。零参考时，仅零误差满足相对项。误差在 CPU double 中汇总 |
| 验证位置 | 正式计时前后分别验证。准备、转换、参考计算、拷回和检查均在计时外；失败停止有效性能汇总 |
| 预热与缓存 | 两个 shape 各预热 20 次，重复使用预分配的输入输出；不清空缓存。这是预热后的重复调用条件，不是冷缓存测量 |
| 正式采样 | 5 轮，每轮每个 shape 连续调用 20 次；偶数轮先 128、奇数轮先 256，轮序为 0–4 |
| 完成边界 | 起止事件在同一当前 stream；计时前同步，结束后等待结束事件，再读毫秒。记录的是调用区间，可包含 Host 提交间隙 |
| 统计单位 | 每个 shape 有 5 个“20 次事件区间的平均时间”，统计这 5 个平均值的 median/min/max。不是 100 个独立样本，不报告 p95/p99 |

脚本输出有效工作量 F、各张量字节数、理想流量预算 Q₀、AI₀、有效吞吐 F/t，以及按 Q₀ 计算的有效带宽 Q₀/t。两种 M 的工作量不同，不把时间比命名为同任务优化加速比。GB/s 使用十进制 10⁹ B/s，TFLOP/s 使用 10¹² FLOP/s。

实际 HBM／设备 DRAM 流量 `q_actual_bytes` 保持 `null`。没有采集就不填 0，也不拿 Q₀ 替代。资源算力、带宽及对应 Roofline 比率也先保留 `null`，由 Agent 根据实际资源条件和可靠来源补充**解释**，不改写原始结果。

对照按事前预测判断“支持／否定／证据不足”：方向预测与五轮结果一致且变化超过本轮观测波动，才描述为本实验条件内支持；方向相反且超出波动则否定；范围重叠、环境不一致或条件无法核对则保留证据不足。min/max 是观测范围，不是置信区间。没有固定的加速百分比或 Roofline 达成率要求，也不要求故意制造异常。

## 5. 返回文件与失败处理

| 文件 | 用途 |
| --- | --- |
| `manifest.json`、`source/` | 固定合同、命令、实际三个源码文件及 SHA256；Git HEAD 只作辅助，不替代未提交工作区的真实源码 |
| `environment.json` | 系统、Python、PyTorch build/git 版本、runtime、可见设备、显存、精度设置及白名单环境覆盖项；设备查询失败也如实保存 |
| `prediction.json` | 正式采样之前保存的预测原文 |
| `inputs.json` | shape、stride、dtype 与复用条件；不保存大张量 |
| `correctness_before.json`、`correctness_after.json` | 两个 shape 的完整误差判据与通过情况 |
| `samples.csv` | 10 个原始区间：轮序、执行顺序、M、调用次数、总毫秒和摊销毫秒 |
| `summary.json` | 正确性通过后的统计与派生模型值；不表示机制归因或课程结课 |
| `status.json` 或 `failure.json` | 环境阻止、成功或执行失败；失败时已完成的原始采样保留 |

如果显存不足、精度设置无法核对、输出不正确或运行中断，返回已有文件和终端提示。Agent 先排查方法和环境；这不算学习者理解未通过。脚本不修改频率、功率、MIG、系统驱动或其他任务。

## 6. 测试包自检与证据边界

```bash
python3 -m unittest discover -s . -p 'test_harness.py' -v
```

标准库测试检查合同、采样顺序、统计、文件不覆盖、CLI 失败路径与环境限制。安装 PyTorch 时，还会运行小规模真实 CPU 张量的数值测试；没有 PyTorch 时明确跳过这些数值项。事件顺序测试使用测试替身，不生成 GPU 性能证据。

本机没有 GPU。打包前可完成代码检查、CPU 数值验证与失败路径检查；GPU 分配、BLAS 执行和事件时间的实机验证在租用环境上完成。CPU 验证不会写入 `runs/` 冒充本课实验。

## 7. 方法依据

核验日期：2026-11-10。以下是版本与接口依据，不是本课设备实测。

- [PyTorch 2.9 CUDA semantics](https://docs.pytorch.org/docs/2.9/notes/cuda.html)：FP32 精度选择、BF16 reduction 与异步完成／设备事件；新旧 TF32 控制不混用。
- [PyTorch 2.9 torch.mm](https://docs.pytorch.org/docs/2.9/generated/torch.mm.html)：矩阵乘和预分配 `out`。
- [PyTorch 2.9 CUDA 环境变量](https://docs.pytorch.org/docs/2.9/cuda_environment_variables.html)：脚本拒绝两个会强制 TF32 的覆盖项值为 1。
- [PyTorch v2.9.0 BF16 支持查询](https://github.com/pytorch/pytorch/blob/v2.9.0/torch/cuda/__init__.py#L185-L211)：CUDA 原生支持检查与 ROCm 分支的差异。
- [PyTorch v2.9.0 GEMM 入口](https://github.com/pytorch/pytorch/blob/v2.9.0/aten/src/ATen/cuda/CUDABlas.cpp#L1187-L1229)、[Lt 入口](https://github.com/pytorch/pytorch/blob/v2.9.0/aten/src/ATen/cuda/CUDABlas.cpp#L377-L434)：计算类型与 CUDA／ROCm reduction 控制差异。
- [PyTorch 2.13.0 精确构建的精度文档源码](https://github.com/pytorch/pytorch/blob/cf30153c4c131c8164ee7798e5022d810682e2cb/docs/source/notes/cuda.md)、[Python 设置接口](https://github.com/pytorch/pytorch/blob/cf30153c4c131c8164ee7798e5022d810682e2cb/torch/backends/cuda/__init__.py)、[GEMM 实现](https://github.com/pytorch/pytorch/blob/cf30153c4c131c8164ee7798e5022d810682e2cb/aten/src/ATen/cuda/CUDABlas.cpp#L1298-L1314)：本包使用的 IEEE 设置及布尔 `False` reduction 控制保持适用；2.13 增加的 split-K 控制不在本次改动范围。包修订 `2026-11-10.2` 仅适配运行环境与设备选择，学习约定仍为版本 1。
