# Plan A

> 一份长期维护的 AI Infra 学习仓库。
>
> **当前阶段**：5 个月（20 周）面试冲刺。**长期定位**：作为我的二脑，沉淀资料、笔记、复盘、实战结果与新感悟。

---

## 1. 仓库定位

我是一名 AI Infra 框架开发工程师，主战场是**自研非 NV 加速芯片**的 PyTorch PrivateUse1 后端 + 改造过的 NCCL 通信库。这个仓库有两层用途：

- **冲刺层（W1–W20）**：5 个月内进入面试窗口，主攻**推理框架 > 训练框架 > 算子开发**三条路线，详见 [计划/主计划.md](计划/主计划.md)。
- **长期层（W20 之后）**：作为持续学习的根目录——周报会一直生成，新资料会沉淀到对应板块，自己的实践结果 / 复盘 / 论文笔记 / 工程踩坑都会进来。仓库会比"求职项目"活得长。

---

## 2. 仓库结构

```
PlanA/
├── README.md                       ← 本文件
├── 计划/                           ← 学习计划与进度的中枢
│   ├── 主计划.md                   ← 20 周排程总表 + 时间预算
│   ├── 周更流程.md                 ← 资料周报的 SOP
│   ├── 进度总表.md                 ← 全局 sprint 进度（甘特 + 模块汇总）
│   └── 周报/                       ← 每周一份，YYYY-Wxx.md
│       └── 2026-W18.md             ← 第一份（DeepSeek V4 周）
│
├── 推理框架/                       ← Track A 第一优先级
├── 训练框架与分布式/               ← Track A 第二优先级（含 §J GPU 通信子专题）
├── 并行计算编程/                   ← Track A 第三优先级（GPU 算子）
├── Pytorch/                        ← PyTorch Internals
├── 模型理论/                       ← Attention / MoE / 量化 / RL 后训练
├── Leetcode/                       ← 250 题，贯穿全程（并行子轨道）
├── 英语/                           ← 听力/口语训练，22 周贯穿全程（并行子轨道）
│   学习指引.md + 进度.md（同样的"稳定版/进度"双锚文件）
│   外加 review-workflow.md（墨墨复习流程）、ai-chat-prompt.md、log/ cards/ references/
│   音频教材由同级工具仓库 ../blog-voice 生产
├── 编译器/                         ← Track B（offer 后或 Track A 余力推进）
├── TPUs/                           ← Track B
│   每个板块目录恒定包含两份核心文件：
│     学习指引.md                   ← 稳定版资料清单（🟥/🟨/🟩 分级）+ 长期订阅
│     进度.md                       ← Sprint 进度子表（🟥 一行一条 + 🟨🟩 章节聚合）
│   随学习推进，会陆续追加：复盘博客 / 论文笔记 / kernel demo / 心得文档
│
├── 面试准备/                       ← STAR 故事、自我介绍、common_problems 题答
│   ├── CV-template.md
│   ├── self-introduction.md
│   ├── projects.md
│   └── common_problems.md
│
└── Job Description/                ← 目标岗位 JD 集合，按方向分类
    ├── AI框架方向/
    ├── 推理/算子/编译器/通信/集群优化/AI 应用/对外（共 7 个子方向）
```

---

## 3. 学习计划体系（四件套）

| 文件 | 作用 | 更新频率 |
|---|---|---|
| [计划/主计划.md](计划/主计划.md) | 20 周排程 + 每周节奏模板（32.5h/周）+ 5 篇博客产出物 | 季度级，不轻改 |
| [{板块}/学习指引.md](推理框架/学习指引.md) | 每板块的资料清单（🟥 必读 / 🟨 选读 / 🟩 背景）+ 长期订阅源 + 自测题库 | 月度晋级 |
| [{板块}/进度.md](推理框架/进度.md) | Sprint 进度表，每学 0.5h 就填一次"已用"列 | 每天 |
| [计划/进度总表.md](计划/进度总表.md) | 全局 dashboard，20 周甘特 + 8 个模块汇总 + checkpoint 自测 | 每周 |

**周报独立成线**：[计划/周更流程.md](计划/周更流程.md) 规定每周日新开会话扫订阅源 → 写 [计划/周报/](计划/周报/) → 月底人工"晋级"高分条目到稳定版 `学习指引.md`。

**两条全程并行子轨道**：[Leetcode/](Leetcode/) 和 [英语/](英语/) 都不占主线板块周次，而是每天用独立时间块推进、贯穿全程，各自同样用 `学习指引.md` + `进度.md` 双锚文件管理。英语轨 22 周（比冲刺多 2 周到 W22），其每日 60–75 min **不计入** 650h 主预算；音频教材由同级工具仓库 `../blog-voice` 生产。

---

## 4. 标记约定

| 资料分级 | 状态 | 含义 |
|---|---|---|
| 🟥 必读 | ⬜ 未开始 | |
| 🟨 选读 | 🟡 进行中 | |
| 🟩 背景 | ✅ 完成 | |
| ⭐ / ⭐⭐ 重要级 | ⏭ 跳过 | |
| 🆕 2025Q4-2026Q1 新增 | 🔖 订阅级（长期跟踪而非啃完）| |

---

## 5. 资料搜集来源

> 这是仓库知识流入的总入口。每个源都是**人工挑选的一线信息源**——不收营销软文、不收无信息增量的转载。
> 各板块 `学习指引.md §长期订阅` 是这里的子集投影；冲突以本节为准。

### 5.1 推理框架（每周必扫）

| 来源 | 链接 | 你能从这里拿到什么 |
|---|---|---|
| Hao AI Lab | https://haoailab.com/blogs/ | DistServe / CLLM 作者团队，工程深度第一 |
| vLLM 官方博客 | https://vllm.ai/blog/ | V1、Speculative Decode、Wide-EP、DeepSeek V4 集成一手 |
| LMSYS 博客 | https://lmsys.org/blog/ | SGLang 深度工程文（ShadowRadix / HiSparse 类原创） |
| LMCache 博客 | https://blog.lmcache.ai/ | KV offload / NIXL / PD 分离一线 |
| NVIDIA Developer Blog | https://developer.nvidia.com/blog | Dynamo / FlashInfer / NVFP4 / Wide-EP 官方解读 |
| Character.AI Blog | https://blog.character.ai/ | 生产侧服务经验（量化 / KV / 稳定性） |
| Anthropic Engineering | https://www.anthropic.com/engineering | 高层推理与生产工程 |
| InferenceMAX 基准 | https://inferencemax.semianalysis.com/ | 每日开源推理 benchmark；Blackwell vs H100/H200 对照 |
| 核心仓库 Releases | vLLM / SGLang / TensorRT-LLM / Dynamo / Mooncake / FlashInfer / LMCache | GitHub release page 直接订阅 |

### 5.2 PyTorch Internals

| 来源 | 链接 | 价值 |
|---|---|---|
| PyTorch 官方博客 | https://pytorch.org/blog/ | release / OpenReg / FSDP2 / TorchTitan |
| Ezyang Blog | https://blog.ezyang.com/ | Dispatcher/Dynamo/Inductor/Autograd 维护者本人 |
| PyTorch Dev-Discuss | https://dev-discuss.pytorch.org/ | RFC、设计讨论、`hardware-backends` 分类对自研芯片后端尤其重要 |
| Accelerator Integration WG | https://github.com/pytorch-fdn/accelerator-integration-wg | RFC-0045 / RFC-0050 出处，对本职最高价值 |
| Horace He "Thonking" | https://www.thonking.ai/ | torch.compile / GPT-Fast / batch-invariance 视角 |
| PyTorch Conference YouTube | 每年 10 月 | accelerator abstraction / torch.compile 主线 |
| Key Issues 订阅 | #166205（PrivateUse1 graph capture）/ #158917（OpenReg）/ RFC-0050 | |

### 5.3 训练框架 / 分布式

| 来源 | 链接 | 价值 |
|---|---|---|
| PyTorch 官方博客（distributed 标签） | https://pytorch.org/blog | FSDP2 / TorchTitan / DTensor |
| HuggingFace Engineering Blog | https://huggingface.co/blog | nanotron / accelerate / 长文训练心得 |
| DeepSpeed Blog | https://www.deepspeed.ai/ | ZeRO / 通信优化 |
| DeepSeek GitHub Org | https://github.com/deepseek-ai | DeepEP / DualPipe / FlashMLA / TileKernels |
| NVIDIA Developer Blog | https://developer.nvidia.com/blog | NCCL release / Megatron-Core / NVFP4 |
| MaxText / Megatron-Bridge / TorchTitan | 各 GitHub repo | 2025Q4 起最活跃的训练框架开源仓 |
| 关键 arXiv 关键词 | `Megatron`, `FSDP`, `torchtitan`, `context parallel`, `expert parallel`, `pipeline schedule`, `MoE training`, `hyper-connections`, `parallel folding`, `fault tolerance LLM training` | |

### 5.4 并行计算 / 算子

| 来源 | 链接 | 价值 |
|---|---|---|
| gpu-mode (ex-CUDA MODE) | https://github.com/gpu-mode/lectures | 每周新 lecture，kernel 社区最活跃 |
| Tri Dao Blog | https://tridao.me/ | FA 系列作者一手（FA-4 在此） |
| Triton GitHub Releases | https://github.com/triton-lang/triton/releases | 3.x 跳跃式更新 |
| FlashInfer Blog + Releases | https://flashinfer.ai/ + https://github.com/flashinfer-ai/flashinfer/releases | CuTe-DSL backend / NVFP4 / 与 vLLM/SGLang 集成 |
| Colfax Research | https://research.colfax-intl.com/ | CUTLASS / TMA / wgmma / tcgen05 / TMEM 教学最优 |
| Hazy Research Blog | https://hazyresearch.stanford.edu/ | ThunderKittens 2.0 主站，Chris Ré 团队 |
| Helion Releases | https://github.com/pytorch/helion/releases | PyTorch 高层 DSL |
| DeepGEMM Releases | https://github.com/deepseek-ai/DeepGEMM | Mega MoE / FP8×FP4 / PDL |
| TileKernels (DeepSeek) | https://github.com/deepseek-ai/TileKernels | V4 production kernel 集合（2026-04 新出） |
| tilelang 主仓 | https://github.com/tile-ai/tilelang | TileKernels 的 codegen 底子 |
| CUTLASS CHANGELOG | https://docs.nvidia.com/cutlass/latest/CHANGELOG.html | 4.x + CuTe DSL Python |
| 关键 arXiv 关键词 | `Triton`, `FlashAttention`, `FlashInfer`, `wgmma`, `TMA`, `tcgen05`, `TMEM`, `warp specialization`, `NVFP4`, `MXFP8`, `CuTe DSL`, `Helion`, `ThunderKittens` | |

### 5.5 模型理论

| 来源 | 链接 | 价值 |
|---|---|---|
| DeepSeek HuggingFace | https://huggingface.co/deepseek-ai | MLA / MoE / DSA / mHC / Engram / V4 |
| 阿里 Qwen Blog | https://qwenlm.github.io/blog/ | Qwen 系列官方更新（每天适配的模型） |
| Meta AI | https://ai.meta.com/blog/ | Llama-X 架构 release |
| Moonshot AI Blog | https://moonshotai.github.io/Kimi/ | Kimi K2 / MoBA / Long context |
| DeepMind / Anthropic / OpenAI Research | 各 research 主页 | 算法主线 |
| NVIDIA Developer Blog | https://developer.nvidia.com/blog | NVFP4 / FP8 / Blackwell 数据格式 |
| 关键 arXiv 关键词 | `Multi-head Latent Attention`, `sparse attention`, `MoE routing`, `MTP`, `FP4`, `NVFP4`, `RoPE extrapolation`, `VLM` | |

### 5.6 编译器（Track B）

| 来源 | 链接 | 价值 |
|---|---|---|
| LLVM Weekly | https://llvmweekly.org/ | LLVM/MLIR 社区周刊 |
| MLIR discussion forum | https://discourse.llvm.org/c/mlir/ | RFC + 设计讨论 |
| Triton GitHub Releases | https://github.com/triton-lang/triton/releases | 与算子板块共享 |
| NVIDIA CUDA Tile IR Releases | https://github.com/NVIDIA/cuda-tile/releases | NV 下一代编译栈 |
| BBuf 知乎 / GiantPandaCV | 知乎专栏 | 中文 AI 编译器最有信息量的写作源 |
| hiascend.com 社区 | https://www.hiascend.com/ | 华为 CANN 开源后实时动态 |
| 关键 arXiv 关键词 | `MLIR`, `tensor IR`, `kernel autotuning`, `GPU compiler`, `tile IR`, `dialect` | |

### 5.7 TPUs（Track B）

| 来源 | 链接 | 价值 |
|---|---|---|
| Google Cloud AI Blog | https://cloud.google.com/blog/products/ai-machine-learning | TPU 代际 + Ironwood 类大更新一手 |
| JAX GitHub Releases | https://github.com/jax-ml/jax/releases | JAX API 演进 |
| MaxText Commits | https://github.com/AI-Hypercomputer/maxtext/commits | 新 model 支持 |
| Jax Scaling Book | https://jax-ml.github.io/scaling-book/ | draft 状态，偶尔补章 |
| SemiAnalysis Newsletter | https://semianalysis.com/ | 产业视角，非 NV 加速器 |
| Tenstorrent / Cerebras / SambaNova Blog | 各官博 | 独立非 NV 厂动态 |

### 5.8 Leetcode

| 来源 | 链接 | 价值 |
|---|---|---|
| NeetCode YouTube | https://www.youtube.com/@NeetCode | 讲解质量最高 |
| LeetCode Premium 公司 tag | leetcode.com（订阅级，W13 后） | 最近 6 个月高频按公司 |
| 1Point3Acres 面经 | https://www.1point3acres.com/ | AI 公司 tag |
| leetcode.cn 近期面试题 | leetcode.cn | 国内大厂补充 |
| Tensara | https://tensara.org/ | GPU/CUDA kernel 题 |
| LeetGPU | https://leetgpu.com/ | CUDA 题入门补充 |
| interviewing.io blog | https://interviewing.io/blog | 面试趋势 + AI 反检测政策 |

### 5.9 行业横扫 / 综述 / 会议

| 来源 | 链接 | 价值 |
|---|---|---|
| Latent Space Podcast | https://www.latent.space/ | AI 工程访谈 |
| ArXiv Sanity Lite | http://arxiv-sanity-lite.com/ | preference 推荐 |
| Papers with Code Trending | https://paperswithcode.com/ | 实现配套的论文榜 |
| MIT Technology Review（AI 板块） | https://www.technologyreview.com/topic/artificial-intelligence/ | 媒体侧深度评论 |
| Jane Street Tech Talks | https://www.janestreet.com/tech-talks/ | 系统视角技术演讲 |

**会议窗口（论文集中地）**：

| 会议 | 时间 | 重点板块 |
|---|---|---|
| NSDI | 3–4 月 | 训练 / 分布式 / 通信 |
| MLSys | 5 月 | 全板块（含 FlashInfer-Bench Contest） |
| OSDI | 7 月 | 系统主场 |
| NeurIPS | 5 月 / 9 月（投稿/接收）/ 12 月 | 模型理论 / 算法 |
| SOSP | 10 月 | 训练栈工业化 |
| ASPLOS / MICRO / ISCA / HPCA | 2–6 月分布 | 硬件向 |
| PPoPP / CGO / PLDI | 2–6 月 | 算子 / 编译器 |

### 5.10 中文社区与个人渠道

> 这些渠道**强信号但弱过滤**——独家工程实战在这里出现得最快，但噪声也最大。原则：在这里看到的东西，必须找到对应英文一手资料才入选稳定版指引。

- **飞书文档**：内部 / 朋友间分享
- **知乎**：BBuf / GiantPandaCV / 各家 infra 工程师专栏
- **微信公众号**：DeepSeek / 智源 / 量子位 / 机器之心 / NVIDIA 开发者社区 等
- **小红书**：行业风向 + 入职/面试体感
- **X / Twitter**：Tri Dao / Horace He / Anthropic 团队 / vLLM 团队 / SGLang 团队
- **GitHub Trending（Python + C++）**：每周扫一遍
- **各类网页博客**：通过 RSS / 邮件订阅汇总到一处

### 5.11 英语听说训练源（并行子轨道）

> 完整清单 + 10 集入门路线见 [英语/references/AI-infra-podcast.md](英语/references/AI-infra-podcast.md)；如何映射到 5 阶段听力升级见 [英语/学习指引.md §3.3](英语/学习指引.md)。**这些源按"配 transcript + 重复 + shadowing"的方式用，被动听不算训练。**

| 阶段 | 主推材料 | 类型 |
|---|---|---|
| 1（恢复手感）| BBC 6 Minute English | 听力恢复，带 transcript |
| 2（技术桥接）| Practical AI | AI 入门播客 |
| 3（上量）| Latent Space、a16z《Building Real-World Infra for AI》 | AI 工程访谈 |
| 4（工程师语速）| TWIML、Kubernetes Podcast（LLM-D）、Software Engineering Daily | 硬核 infra |
| 5（产出）| Dwarkesh（Dylan Patel）、No Priors（Jensen Huang）| 难集 |

**工具栈**（固定不换）：Anki / 墨墨记忆卡（间隔重复）、Language Reactor（双语字幕）、YouGlish（真实发音）、Cambridge Dictionary（查词）、多邻国（streak）。**自产教材**：同级 `../blog-voice` 把 AI Infra 博客转成"喜欢音色 + 双语 LRC"的音频，每 2–3 周 1 篇。

---

## 6. 阅读路径建议

| 你是谁 / 你想干什么 | 从这里入 |
|---|---|
| 想看我的目标岗位画像 | [Job Description/](Job Description/) |
| 想看我五个月的整体规划 | [计划/主计划.md](计划/主计划.md) |
| 想看某板块要读什么资料 | [{板块}/学习指引.md](推理框架/学习指引.md) |
| 想看我学到哪了 | [计划/进度总表.md](计划/进度总表.md) |
| 想看本周新出的资料 | [计划/周报/](计划/周报/) 最新一份 |
| 想看我的英语听说训练计划 | [英语/学习指引.md](英语/学习指引.md)（进度见 [英语/进度.md](英语/进度.md)）|
| 想看面试故事素材 | [面试准备/](面试准备/) |
| 想看具体的论文笔记 / 实战复盘 | 各板块目录下后续会陆续追加的 `.md` 文件 |

---

## 7. 维护规则（防腐手册）

1. **不让稳定版被周报污染**：周报是高频流入；稳定版指引只在月底人工"晋级"时才动。
2. **进度颗粒度足够细**：每学 0.5h 就在 `进度.md` 填一次，正反馈靠小颗粒打勾建立。
3. **写复盘**：每周末必须输出一篇"自己讲给自己听"的复盘笔记（< 1000 字），落到对应板块目录。这些是面试故事的弹药。
4. **资料分级保持纪律**：🟥 必读 / 🟨 选读 / 🟩 背景 三级一旦定下来，不要随意上调。预算不够时砍数量，不降优先级。
5. **新资料先入周报、再入稳定版**：避免"看到啥都塞进去"导致清单膨胀。
6. **过时资料**：发现某条目被淘汰（如 EAGLE-2 → EAGLE-3），保留老条目位置，行内加 "（替代自 X，YYYY-MM-DD）" 注解。不删，留作历史。
7. **Changelog**：每次稳定版指引发生晋级，在该指引顶部 Changelog 节加一行记录晋级事件。

---

## 8. 起步状态（2026-04-29）

- ✅ 8 个板块的稳定版 `学习指引.md` 全部 2025Q4-2026Q1 资料审计完成
- ✅ 8 份 `进度.md` + 全局 `进度总表.md` 已搭好
- ✅ 第一份周报 [2026-W18.md](计划/周报/2026-W18.md) 已生成（DeepSeek V4 + TileKernels 周）
- ⬜ W1 学习尚未开始

冲刺第一天就是现在。
