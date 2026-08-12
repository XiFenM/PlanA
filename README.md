# Plan A

> 一份长期维护的 AI Infra 学习仓库。
>
> **当前阶段**：5 个月（20 周）面试冲刺。**长期定位**：作为我的二脑，沉淀资料、笔记、复盘、实战结果与新感悟。

---

## 1. 仓库定位

我是一名 AI Infra 框架开发工程师，主要从事**自研非 NV 加速芯片**上的 PyTorch/vLLM 适配、通信与性能优化。这个仓库有两层用途：

- **冲刺层（W1–W20）**：5 个月内进入面试窗口，主攻**推理框架 > 训练框架 > 算子开发**三条路线，详见 [计划/主计划.md](计划/主计划.md)。
- **长期层（W20 之后）**：作为持续学习的根目录——资料 refresh 按需形成可追溯快照，获批资料再沉淀到对应板块；自己的实践结果、复盘、论文笔记和工程经验也持续积累。仓库会比"求职项目"活得长。

---

## 2. 仓库结构

```
PlanA/
├── README.md                       ← 本文件
├── 计划/                           ← 学习计划与进度的中枢
│   ├── 主计划.md                   ← 20 周排程总表 + 时间预算
│   ├── 进度总表.md                 ← 全局 sprint 进度（甘特 + 模块汇总）
│   ├── 周更流程.md                 ← 资料周报的 SOP
│   ├── 月底晋级评审.md             ← 月底晋级评审的 SOP
│   ├── 学习断点.md                 ← 唯一稀疏 Checkpoint（仅语义变化时覆盖）
│   └── 周报/                       ← 按需 refresh 的不可变历史快照，沿用 YYYY-Wxx.md
│       └── 2026-W18.md             ← 第一份（DeepSeek V4 周）
│
├── .agent-skills-config/           ← 四个已适配学习 Skill 的 version 2 公共环境配置
│   └── guide-learning-profile.md   ← PlanA 状态路径、单写者、时长归属与领域透镜
├── 推理框架/                       ← Track A 第一优先级
├── 训练框架与分布式/               ← Track A 第二优先级（含 §J GPU 通信子专题）
├── 并行计算编程/                   ← Track A 第三优先级（GPU 算子）
├── PyTorch/                        ← PyTorch Internals
├── 模型理论/                       ← Attention / MoE / 量化 / RL 后训练
├── Leetcode/                       ← 250 题，贯穿全程（并行子轨道）
├── 英语/                           ← 听力/口语训练，22 周贯穿全程（并行子轨道）
│   学习指引.md + 进度.md（同样的"稳定版/进度"双锚文件）
│   外加 review-workflow.md（路径、授权与交接适配）、log/ cards/ references/
│   音频教材由同级工具仓库 ../blog-voice 生产
├── 编译器/                         ← Track B（offer 后或 Track A 余力推进）
├── TPUs/                           ← Track B
│   每个板块目录恒定包含两份核心文件：
│     学习指引.md                   ← 稳定版资料清单（🟥/🟨/🟩 分级）+ 长期订阅
│     进度.md                       ← Sprint 进度子表（🟥 一行一条 + 🟨🟩 章节聚合）
│   随学习推进，会陆续追加：复盘博客 / 论文笔记 / kernel demo / 心得文档
│   以及 AI 工作流的两类产物：log/（学习记录）与 cards/（墨墨记忆卡 TSV）
│
├── 面试准备/                       ← STAR 故事、自我介绍、common_problems 题答
│   ├── CV-template.md
│   ├── self-introduction.md
│   ├── projects.md
│   └── common_problems.md
│
├── Job Description/                ← 目标岗位 JD 集合，按方向分类
│   ├── AI框架方向/
│   ├── 推理/算子/编译器/通信/集群优化/AI 应用/对外（共 7 个子方向）
│
├── .agent-skills/                   ← 中央 Agent Skills 子模块（固定中央版本）
├── .agent-skills.json               ← 中央 Skill 选择（Codex + Claude）
├── .claude/skills/                 ← materializer 生成的 Claude 发现视图
└── .agents/skills/                 ← materializer 生成的 Codex 发现视图
```

### 2.1 固定源码子模块

仓库使用 Git submodule 保存本轮学习所依据的上游源码快照。它们是少数板块下的参考源码，不属于每个板块都必须具备的双锚文件；`英语/references/` 等普通资料目录也不是子模块。

| 子模块 | 本地路径 | 当前固定版本 | 固定提交 |
|---|---|---|---|
| vLLM | [`推理框架/references/vllm`](推理框架/references/vllm) | `v0.26.0` | `568afb3a13806beb53bb2e6bd518269357b237c0` |
| SGLang | [`推理框架/references/sglang`](推理框架/references/sglang) | `v0.5.17` | `29481685462732237d80d86076d6563e1f658102` |
| PyTorch | [`PyTorch/references/pytorch`](PyTorch/references/pytorch) | `v2.11.0` | `70d99e998b4955e0049d13a98d77ae1b14db1f45` |

根目录 [`.gitmodules`](.gitmodules) 登记了上游地址，并为三个子模块启用浅克隆。父仓库记录的 gitlink 才是精确版本事实源；上述基线的选择理由与用途见 [EP-PD 自研芯片适配设计与验证包](推理框架/EP-PD自研芯片适配设计与验证包.md)。

首次克隆（Windows 建议先启用长路径，以免 PyTorch 的深层目录检出失败）：

```powershell
git config --global core.longpaths true
git clone --recurse-submodules --shallow-submodules git@github.com:XiFenM/PlanA.git
```

如果已经克隆了父仓库，但子模块目录还是空的：

```powershell
git submodule sync --recursive
git submodule update --init --recursive
```

以后拉取父仓库更新时，同时把子模块恢复到父仓库固定的提交：

```powershell
git pull --recurse-submodules
git submodule update --init --recursive
```

子模块处于 `detached HEAD` 是固定版本时的正常状态。日常学习不要在子模块内直接 `pull`，也不要执行 `git submodule update --remote`；需要升级上游版本时，应显式修改父仓库记录的 gitlink，并同步更新本节基线。

### 2.2 Skill 中央管线（version 2 受管配置）

中央规范源以 [`.agent-skills`](.agent-skills) 子模块固定在
`f6abbdf5a1acd00ba6d5e45a92456605b603b392`。[`.agent-skills.json`](.agent-skills.json) 为 Codex 与 Claude
同时选择 `guide-learning`、`study-log`、`english-coach`、`memo-cards`、
`resource-planning` 和 `playwright-cli`，并为前四个已适配的 first-party Skill 引用
[`.agent-skills-config/`](.agent-skills-config/) 下的 Git-tracked 公共配置。`resource-planning` 已使用最新版中央核心，
但本轮不挂载持久上下文；它当前仅可进行无配置、纯对话、零写入的专题 `research`。

materializer 会为有配置的 Skill 在两个宿主副本中生成逐字节一致的 `.agent-skills-context.json`。它只提供
仓库事实定位、已验证的 tracked 输入 collection 和机械写入上限，不授予读取未跟踪文件、保存、覆盖、
制卡、发布、提交或推送。`resource-planning` 当前没有 `.agent-skills-context.json`；source/query 目录、
portfolio slot 和 registry bootstrap 尚未迁移，因此不得运行持久 refresh/review 或保存 research brief。

`.agents/skills/` 与 `.claude/skills/` 是被 Git 忽略的生成发现视图，不是事实源。不要手工修改、复制或
同步这两棵树；只修改中央仓库的规范源或本仓库的选择配置。

已有 checkout 只需初始化中央子模块及其官方依赖：

```powershell
git submodule sync --recursive
git submodule update --init --recursive .agent-skills
```

初始化后生成两个宿主的发现视图，并验证生成状态：

```powershell
uv run --no-project python .agent-skills/tools/materialize_skills.py --repo . --dry-run
uv run --no-project python .agent-skills/tools/materialize_skills.py --repo .
uv run --no-project python .agent-skills/tools/materialize_skills.py --repo . --check
```

---

## 3. 学习计划体系（四件套）

| 文件 | 作用 | 更新频率 |
|---|---|---|
| [计划/主计划.md](计划/主计划.md) | 20 周候选排程、计划预算与可选文章目标 | 季度级，不轻改 |
| [{板块}/学习指引.md](推理框架/学习指引.md) | 每板块的稳定资料组合（🟥 必读 / 🟨 选读 / 🟩 背景）与自测题库 | 仅在资料评审获批后更新 |
| [{板块}/进度.md](推理框架/进度.md) | 模块进度与用户确认的实际学习时长 | 有可归属的实质进展且时长经确认时 |
| [计划/进度总表.md](计划/进度总表.md) | 全局派生 dashboard，20 周甘特与模块汇总 | 经批准的周期触点，不裁决活动状态 |

**资源快照独立成线**：[计划/周更流程.md](计划/周更流程.md) 与 [计划/月底晋级评审.md](计划/月底晋级评审.md)
暂时保留为 legacy 人类 SOP。它们不构成 version 2 的机器配置；在后续将 source/query 目录、portfolio
slot 与 registry bootstrap 作为一个整体完成并评审前，`resource-planning` 仅进行无配置、纯对话、零写入
的专题 `research`，不执行持久 refresh/review。未来 refresh 按需计算自上次成功运行后的补缺窗口；周日／
月末只可作为提醒，不构成运行或评审前置。

**两条全程并行子轨道**：[Leetcode/](Leetcode/) 和 [英语/](英语/) 都不占主线板块周次，而是每天用独立时间块推进、贯穿全程，各自同样用 `学习指引.md` + `进度.md` 双锚文件管理。英语轨 22 周（比冲刺多 2 周到 W22），其每日 60–75 min **不计入** 650h 主预算；音频教材由同级工具仓库 `../blog-voice` 生产。

**AI 学习工作流（6 个 Skills）**：中央 [`.agent-skills`](.agent-skills) 是 Skill 规范源，
`.agents/skills/` 与 `.claude/skills/` 只是生成的宿主发现视图。Agent 侧路由表与管线图见
[CLAUDE.md](CLAUDE.md)；[`.agent-skills-config/guide-learning-profile.md`](.agent-skills-config/guide-learning-profile.md)
只定义 PlanA 的状态路径、单写者、时长归属与领域透镜，不复制中央教学流程：

| Skill | 流程站位 | 触发 |
|---|---|---|
| `resource-planning` | **供给侧**：最新版核心已启用，持久上下文未挂载 | 「研究／比较这些资料」时仅纯对话、零写入；refresh/review 暂时阻断 |
| `guide-learning` | **主干**：来源化教学 → 讲后检查 → 按证据缺口练习 → mastery → 稀疏恢复 | 教我／带我学／继续或恢复 Lesson |
| `study-log` | **按需交接**：结构化过程记录，或经边界与隐私确认的 raw 可见文本存档 | 「整理学习记录／保存原始对话」 |
| `memo-cards` | **记忆侧**：学习记录 / 文章面试Q&A / 英语日志 → 墨墨 TSV 卡 | 「制卡」 |
| `english-coach` | **英语轨**：学后「英语回顾」专项（主）+ 技术对话轮末反馈（辅） | 「英语回顾」/ 直接写英文 |
| `playwright-cli` | 工具件，不占流程位 | 浏览器自动化 |

学习、文章、结构化记录、原始对话、卡片和英语回顾是六个可独立授权的动作。学习收尾不自动生成后五者；
有价值时 Agent 可以提议，用户确认后才交给对应 Skill。

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
| Accelerator Integration WG | https://github.com/pytorch-fdn/accelerator-integration-wg | RFC-0045 / RFC-0050 出处，第三方加速器接入重点资料 |
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

**工具栈**（固定不换）：墨墨记忆卡（间隔重复）、Language Reactor（双语字幕）、YouGlish（真实发音）、Cambridge Dictionary（查词）、多邻国（streak）。合格英语素材制卡时以每个学习日新增 8–12 张逻辑卡为软目标，不是硬上限，也不构成自动制卡或写入授权。**自产教材**：同级 `../blog-voice` 把 AI Infra 博客转成"喜欢音色 + 双语 LRC"的音频，每 2–3 周 1 篇。

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
| 想看 AI 怎么带我学 | [中央 `guide-learning`](.agent-skills/skills/guide-learning/SKILL.md) + [PlanA 配置层](.agent-skills-config/guide-learning-profile.md) |
| 想看学习过程记录 / 记忆卡 | 各板块 `log/`（学习记录）与 `cards/`（墨墨 TSV），如 [PyTorch/log/](PyTorch/log/) |
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
8. **AI 产物与行为各有事实源**：结构化学习记录只进 `{板块}/log/`，更新已有记录时先展示 diff 并确认；raw 对话默认放在 Git 工作树外。记忆卡只进 `{板块}/cards/`，文章 Q&A 卡为主牌，学习记录卡只保留纠错与文章未收录的过程细节。中央 Skill 拥有 Agent 行为规范；本仓库配置层只保存 PlanA 路径、事实职责、时长归属与领域透镜。

---

## 8. 起步快照（2026-04-29，历史）

- ✅ 8 个板块的稳定版 `学习指引.md` 全部 2025Q4-2026Q1 资料审计完成
- ✅ 8 份 `进度.md` + 全局 `进度总表.md` 已搭好
- ✅ 第一份周报 [2026-W18.md](计划/周报/2026-W18.md) 已生成（DeepSeek V4 + TileKernels 周）
- ⬜ W1 学习尚未开始

冲刺第一天就是现在。
