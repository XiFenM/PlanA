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

跨面试题目按主题汇总在 [common_problems.md](common_problems.md)。该文件是已有内容，本次归档没有改写。

## 目录结构

```text
面试问题经验/
├── README.md                     # 本入口
├── common_problems.md            # 跨面试问题主题汇总
├── 分析成果/                     # 23 个报告、审计、转写和 JSON 结果
│   ├── analysis/                 # 结构化分析与技术 QA
│   ├── reports/                  # 逐场复盘报告
│   └── transcripts/              # 转写、校准稿与交叉 QA
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

## 阅读和维护约定

1. 最终报告用于快速复盘；原始记录用于确认说话人、时间戳和上下文。
2. 技术审计与 QA 用于区分现场事实、技术校准和未知项，不代表面试官正式评价。
3. `.raw.json` 保存原始模型响应，`.normalized.json` 是结构化衍生结果；一般阅读无需从 JSON 开始。
4. `分析成果` 保留原 `outputs` 的三层相对结构，确保报告中的内部链接可以继续使用。
5. 新增面试时继续按“公司 / 日期与轮次”归档，并保持分析成果和原始素材分离。
6. 不覆盖原始素材；修订报告时创建新版本或明确记录替代关系。

## 来源与同步状态

- 最近归档日期：2026-08-29。
- 分析成果来源：`daily-work/outputs/managed/interview-video-analysis` 的全部 23 个文件；本次增量同步 8 个文件。
- 原始素材维持 2026-08-26 的归档状态，共 12 个文件；本次没有复制后续补充的视频。
- 归档采用复制方式，`daily-work` 中的源文件没有移动、删除或改写。
- 当前 35 个归档文件均保留原文件名和原始字节；本目录不是自动同步镜像，后续在 `daily-work` 中新增或修改内容时需要再次归档并校验。
