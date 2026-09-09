# 面试问题与经验

这里集中保存真实面试材料、逐场复盘报告和跨面试问题总结。目录先按照“分析成果”和“原始素材”分开：分析成果保留原来的 `analysis / reports / transcripts` 相对结构，原始素材再按公司、日期与轮次归档。

建议先阅读每场面试的最终报告，再按报告中的证据边界回到文字记录、校准转写或技术审计。AI 智能纪要和自动总结图只能作为辅助线索，不能替代原始记录。

## 快速入口

| 公司与场次                           | 材料情况                                                     | 建议优先阅读                                                                              | 原始素材                                         |
| ------------------------------------ | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 地平线，2026-08-13                   | 完整音频的双 ASR、结构化分析与技术审计；本归档未收录原始录像 | [双 ASR 校准版复盘](分析成果/reports/interview-20260813-01-self-review-asr-calibrated.md) | 原视频已在 daily-work 补回，本次未归档           |
| 小红书，轮次未记录                   | 只有 5 组重要问题简记，没有现场作答                          | [最终分析报告](分析成果/reports/interview-xiaohongshu-notes-01-analysis.md)               | [面试简记](原始素材/小红书/小红书简记.md)        |
| 奕行智能简记，轮次未记录             | 只有主题级简记，没有完整问答                                 | [最终分析报告](分析成果/reports/interview-yixing-notes-01-analysis.md)                    | [面试简记](原始素材/奕行智能/奕行智能简记.md)    |
| 奕行智能二面，日期未确认             | 完整音频的单模型理解与本地证据审计；没有独立 ASR 逐字稿      | [二面最终分析报告](分析成果/reports/interview-yixing-recording-02-analysis.md)            | 本次仅归档分析成果，原视频仍在 daily-work        |
| XG 科技一面，2026-08-18              | 后半段带时间戳文字记录、AI 纪要与 2 张图                     | [一面最终分析报告](分析成果/reports/interview-xg-20260818-01-analysis.md)                 | [一面原始素材](原始素材/XG科技/2026-08-18-一面/) |
| XG 科技二面，2026-08-24              | 主体较完整的带时间戳文字记录、AI 纪要与 4 张图               | [二面最终分析报告](分析成果/reports/interview-xg-20260824-02-analysis.md)                 | [二面原始素材](原始素材/XG科技/2026-08-24-二面/) |
| 安霸半导体，2026-08-28（容器元数据） | 完整音频的单模型理解与本地证据审计；分析副本已做响度归一化   | [最终分析报告](分析成果/reports/interview-ambarella-20260828-01-analysis.md)              | 本次仅归档分析成果，原视频仍在 daily-work        |
| 进迭时空，日期与轮次未确认           | 完整音频的一次 Gemini 理解与本地技术审查；整理出 17 组主要问答 | [分析报告](分析成果/reports/interview-jindie-recording-01-analysis.md)                  | 本次仅归档分析成果，原录音仍在 daily-work        |
| 寒武纪，日期与轮次未确认 | 同音频的 Gemini 理解与 OpenAI 转写对照；17 组问答加 1 项补充追问 | [转写校准版复盘](分析成果/reports/interview-cambricon-recording-01-asr-calibrated-analysis.md) | 原视频仍在 daily-work；分析音频与抽帧随配套材料本地归档 |

跨面试题目按主题汇总在 [common_problems.md](common_problems.md)。该文件是已有内容，本次归档没有改写。

## 目录结构

```text
面试问题经验/
├── README.md                     # 本入口
├── common_problems.md            # 跨面试问题主题汇总
├── 分析成果/                     # 报告、审计、转写和配套证据
│   ├── analysis/                 # 结构化分析与技术 QA
│   ├── reports/                  # 逐场复盘报告
│   ├── transcripts/              # 转写、校准稿与交叉 QA
│   └── 配套材料/寒武纪/           # 处理说明、媒体副本、请求与验证记录
└── 原始素材/                     # 12 个文字、简记和图片文件
    ├── 小红书/
    ├── 奕行智能/
    └── XG科技/
        ├── 2026-08-18-一面/
        └── 2026-08-24-二面/
```

## 完整文件导航

### 地平线：2026-08-13

最终报告：

- [双 ASR 校准版复盘](分析成果/reports/interview-20260813-01-self-review-asr-calibrated.md)：建议优先阅读。
- [早期候选版复盘](分析成果/reports/interview-20260813-01-self-review.md)：保留早期分析过程与时间戳证据边界。

技术审计：

- [双 ASR 独立技术审计](分析成果/analysis/interview-20260813-01.asr-technical-audit.md)
- [视频理解结果的证据与技术 QA](分析成果/analysis/run-20260823-01.evidence-qa.md)

转写与校准：

- [双模型校准稿](分析成果/transcripts/interview-20260813-01.calibrated.md)
- [双模型转写交叉 QA](分析成果/transcripts/interview-20260813-01.cross-model-qa.md)
- [OpenAI 原始转写响应](分析成果/transcripts/run-20260823-02.openai-gpt-transcribe.raw.json)
- [豆包原始转写响应](分析成果/transcripts/run-20260823-03.bytedance-doubao-seed-asr-2-0.raw.json)

结构化分析：

- [规范化分析结果](分析成果/analysis/run-20260823-01.normalized.json)
- [原始视频理解结果](分析成果/analysis/run-20260823-01.raw.json)
- [视频理解响应元数据](分析成果/analysis/run-20260823-01.raw.json.response.json)

`daily-work/work/managed/interview-video-analysis/incoming` 后续已补回这场面试的原始录像，但本目录当前仍只收录现存分析、审计和转写成果。校准稿不是逐字稿，角色和术语仍应结合原音频复核。

### 小红书：面试简记

- [最终分析报告](分析成果/reports/interview-xiaohongshu-notes-01-analysis.md)
- [原始简记](原始素材/小红书/小红书简记.md)

简记没有记录现场作答、追问和结果，报告只整理考察范围与准备方向。

### 奕行智能：面试简记

- [最终分析报告](分析成果/reports/interview-yixing-notes-01-analysis.md)
- [原始简记](原始素材/奕行智能/奕行智能简记.md)

简记只有主题词和一条融合判断逻辑，报告不据此评价现场表现。

### 奕行智能二面：日期未确认

- [二面最终分析报告](分析成果/reports/interview-yixing-recording-02-analysis.md)
- [音频证据审计](分析成果/analysis/interview-yixing-recording-02.audio-evidence-audit.md)
- [全音频理解原始结果](分析成果/analysis/understand-yixing-recording-02-20260829.audio.md)
- [响应元数据](分析成果/analysis/understand-yixing-recording-02-20260829.audio.md.response.json)

本次没有成功获得完整 ASR 转写，报告基于单模型全音频理解和本地证据审计。报告中的时间点是近似回听锚点，不应当作逐字稿时间码；一面简记只作为有限背景。

### XG 科技一面：2026-08-18

- [一面最终分析报告](分析成果/reports/interview-xg-20260818-01-analysis.md)
- [带时间戳文字记录](原始素材/XG科技/2026-08-18-一面/XG科技面试文字记录.md)
- [AI 智能纪要](原始素材/XG科技/2026-08-18-一面/XG科技面试智能纪要.md)
- [AI 关系图](原始素材/XG科技/2026-08-18-一面/meetgraph.png)
- [AI 白板图](原始素材/XG科技/2026-08-18-一面/whiteboard_exported_image.png)

文字记录只覆盖约 `00:41:52–01:29:48` 的后半段。报告中的结论不能外推到缺失的前半段。

### XG 科技二面：2026-08-24

- [二面最终分析报告](分析成果/reports/interview-xg-20260824-02-analysis.md)
- [带时间戳文字记录](原始素材/XG科技/2026-08-24-二面/XG科技-2-文字记录.md)
- [AI 智能纪要](原始素材/XG科技/2026-08-24-二面/XG科技-2-智能纪要.md)
- [AI 总视图](原始素材/XG科技/2026-08-24-二面/总视图.png)
- [AI 图 1](原始素材/XG科技/2026-08-24-二面/pics/meetgraph_1.png)
- [AI 图 2](原始素材/XG科技/2026-08-24-二面/pics/meetgraph_2.png)
- [AI 白板图](<原始素材/XG科技/2026-08-24-二面/pics/whiteboard_exported_image _1.png>)

文字记录覆盖 `00:06:50–00:50:07`，正式面试约从 `00:07:22` 开始。智能纪要和图片混有面试官提示与自动评价，应以文字记录和报告中的纠偏章节为准。

### 安霸半导体：2026-08-28（仅来自容器元数据）

- [最终分析报告](分析成果/reports/interview-ambarella-20260828-01-analysis.md)
- [音频证据审计](分析成果/analysis/interview-ambarella-20260828-01.audio-evidence-audit.md)
- [全音频理解原始结果](分析成果/analysis/understand-ambarella-20260828-01-20260829.audio.md)
- [响应元数据](分析成果/analysis/understand-ambarella-20260828-01-20260829.audio.md.response.json)

源音频音量很轻，分析副本从约 `-35.37 LUFS` 归一化到约 `-18.64 LUFS`；原视频没有被改写。本次同样没有独立 ASR 逐字稿，报告中的时间点只用于近似回听。日期来自视频容器元数据，尚未独立确认。

### 进迭时空：日期与轮次未确认

- [分析报告](分析成果/reports/interview-jindie-recording-01-analysis.md)
- [证据与技术审查](分析成果/analysis/interview-jindie-recording-01.audio-evidence-audit.md)
- [全音频理解原始底稿](分析成果/analysis/understand-jindie-recording-01-20260907.audio.md)
- [响应元数据](分析成果/analysis/understand-jindie-recording-01-20260907.audio.md.response.json)

录音约 46 分 14 秒，经响度归一化后，通过 ZenMux 调用 Gemini 3.7 Flash 一次，再完成本地证据与技术审查。报告整理出 17 组主要问答，重点涉及布局与访存优化、异步拷贝排障、PyTorch 后端接入和 AI 编码验证。

本次没有独立 ASR 或人工回听，时间码只作近似导航。底稿在约 `02:45–06:10`、`14:50–16:00` 等区间没有展开内容，仍需回听；技术审查已收窄模型对硬件细节的推断，并纠正 FlashAttention 复杂度等表述。2026-09-07 是处理与归档日期，不作为面试实际日期。

### 寒武纪：日期与轮次未确认

- [转写校准版复盘](分析成果/reports/interview-cambricon-recording-01-asr-calibrated-analysis.md)：建议优先阅读。
- [OpenAI 与 Gemini 逐题对照](分析成果/analysis/interview-cambricon-recording-01.asr-gemini-comparison.md)
- [对照引用与字符区间 JSON](分析成果/analysis/interview-cambricon-recording-01.asr-gemini-comparison.json)
- [OpenAI 转写原文索引](分析成果/transcripts/interview-cambricon-recording-01.openai-asr-indexed.md)
- [无损字符索引 JSON](分析成果/transcripts/interview-cambricon-recording-01.openai-asr-indexed.json)
- [OpenAI 原始转写响应](分析成果/transcripts/transcribe-cambricon-recording-01-openai-20260908.raw.json)
- [第一版 Gemini 复盘](分析成果/reports/interview-cambricon-recording-01-analysis.md)
- [第一轮证据与技术审查](分析成果/analysis/interview-cambricon-recording-01.audio-evidence-audit.md)
- [Gemini 原始底稿](分析成果/analysis/understand-cambricon-recording-01-20260908.audio.md)
- [Gemini 响应元数据](分析成果/analysis/understand-cambricon-recording-01-20260908.audio.md.response.json)

本场录像约 36 分 42 秒。两次处理采用同一份完整音频：Gemini 3.7 Flash 理解一次，OpenAI GPT Transcribe 转写一次，后者返回 9,977 字符。对照修正了缓存尾块、Conv3D 完整维度、device guard 与反问归属的部分解读，并补出 C++ 多线程追问。报告没有人工回听支持；ASR 无时间戳和说话人字段，专名错识仍需回听。

配套材料按原有职责分目录保存：

- [处理说明](分析成果/配套材料/寒武纪/notes/)与[实际提示词](分析成果/配套材料/寒武纪/prompts/)
- [媒体副本、抽帧及元数据](分析成果/配套材料/寒武纪/derived/)
- [请求提案与精确计划](分析成果/配套材料/寒武纪/workflow-proposals/)
- [预检与验证记录](分析成果/配套材料/寒武纪/preflight/)，包括[第一轮交付验证](分析成果/配套材料/寒武纪/preflight/interview-cambricon-recording-01.delivery-validation.json)和[转写对照交付验证](分析成果/配套材料/寒武纪/preflight/interview-cambricon-recording-01.asr-delivery-validation.json)
- [本场来源与运行清单快照](分析成果/配套材料/寒武纪/source-manifest.snapshot.json)与[归档文件及哈希映射](分析成果/配套材料/寒武纪/archive-manifest.json)

2026-09-08 是分析与归档日期，不认定为面试日期。后续理解默认模型已更新为 Gemini 3.8 Flash，本场没有再用 3.8 调用。归档的 JSON 中原路径与哈希保留 daily-work 上下文，用于追溯；清单快照不接管业务状态。音频副本与会议画面按本目录的 Git 忽略规则仅在本地保留，原始 MKV 沿用此前视频归档约定，仍在 daily-work。

## 阅读和维护约定

1. 最终报告用于快速复盘；原始记录用于确认说话人、时间戳和上下文。
2. 技术审计与 QA 用于区分现场事实、技术校准和未知项，不代表面试官正式评价。
3. `.raw.json` 保存原始模型响应，`.normalized.json` 是结构化衍生结果；一般阅读无需从 JSON 开始。
4. 核心分析成果沿用原 `outputs` 的 `analysis / reports / transcripts` 结构；配套材料按场次归档。必要的相对链接调整记录在对应归档清单中。
5. 新增面试时继续按“公司 / 日期与轮次”归档，并保持分析成果和原始素材分离。
6. 不覆盖原始素材；修订报告时创建新版本或明确记录替代关系。

## 来源与同步状态

- 最近归档日期：2026-09-08。
- 本次复制寒武纪已登记的全部 36 个产物：10 个核心分析文件、26 个配套产物；归档映射、清单快照和媒体忽略规则另行生成。
- 核心 analysis / reports / transcripts 现有 37 个文件；原有 27 个文件保持原样。
- 寒武纪新增副本中，35 个与 daily-work 源文件逐字节一致；第一版报告仅调整一条指向接收说明的相对链接，源文件和副本哈希均在归档映射中记录。
- 原始素材仍为此前归档的 12 个文件；本次归档包括分析音频副本和抽帧，原始录像继续保留在 daily-work。
- 归档采用复制方式；daily-work 仍是来源、运行和产物业务清单的维护位置。归档 JSON 保留源仓库的路径语境，不应直接作为新环境中的执行计划。
- 报告保留生成时的执行状态，最新归档情况以本节为准。本目录不是自动同步镜像，后续更新需重新复制并校验。
