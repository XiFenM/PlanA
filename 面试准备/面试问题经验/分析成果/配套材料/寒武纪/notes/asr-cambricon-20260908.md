# 寒武纪 OpenAI 转写与 Gemini 对照计划

- 记录 ID：`interview-cambricon-recording-01`。
- 本次运行：`transcribe-cambricon-recording-01-openai-20260908`。
- 用户明确要求走音频转写路线对照分析，并指定可用 `openai/gpt-transcribe`；本次不再调用 Gemini。
- 本文件是本地处理与比较协议，不作为 ASR 提示词发送。

## 精确输入与请求

复用上一轮 Gemini 收到的同一份完整归一化双声道音频：`work/managed/interview-video-analysis/derived/interview-cambricon-recording-01.normalized-stereo-16k-64kbps.mp3`，17,615,853 bytes，2201.940 秒，SHA-256 `3a4e76277132d28cc3bf60629d9c801ac97b522a7d013927ce266cafd4a99b04`。原片保留，本轮不再转码或裁切，避免把输入差异混入模型比较。

通过仓库 `pnpm zenmux transcribe`，使用 `openai/gpt-transcribe`、`language=zh`、`enable_itn=true`、`stream=false`、25 MiB 上限，执行一次完整音频转写。输出只包含一个精确 JSON 文件：`outputs/managed/interview-video-analysis/transcripts/transcribe-cambricon-recording-01-openai-20260908.raw.json`。

已查阅 [ZenMux 转写接口](https://zenmux.ai/docs/zh/api/openai/create-audio-transcriptions.html)、[模型页](https://zenmux.ai/openai/gpt-transcribe)与实时模型目录。公开费率 USD 0.000075/秒，对当前副本估算约 USD 0.16515。本次执行边界为 USD 0.50、estimate-only、一次尝试；不构成货币硬上限。实际账单可能与估算不同。失败或结果不明保留记录，不自动重试。

## 对照规则

1. ASR 请求只发送音频和固定参数，不输入 Gemini 底稿、先验题目或术语清单，避免用既有结论引导转写。
2. 先按 ASR 文本建立顺序段落与引用定位，再对照旧报告 Q1–Q17。原始响应和上一轮全部终态、底稿及报告保持不变。
3. 结果分别归类为相互支持、ASR 补充、表述冲突、ASR 未找到支持及无法确认。没有出现在转写中的内容不自动视为不存在。
4. 重点核查：Prefix Caching 的实际输入例子与逻辑/物理块；Conv3D shape 和字节单位；异步问题排查与修复；Dispatcher 与 ProcessGroup；构造函数、全局变量、装饰器、Monkey Patch、GIL、IPC；反问中的团队职责。
5. 返回时间戳或说话人字段前，不假定接口具有这些能力。若只有全文，使用段落号/字符区间定位；旧 Gemini 时间码只能标为继承的近似导航，不能当作独立对齐。
6. ASR 更贴近文字表述，但同样可能错词、漏句、重复或误标角色；两种模型一致不证明技术说法正确，不一致也不以多数票确定原话。
7. 新增转写文本、对照记录和基于转写修订的报告，明确哪些旧判断保留、收窄或撤回。保留人工回听需求，不宣称人工已确认。

## Gemini 默认配置修正

本轮检查时本地 `.env` 已设置 `ZENMUX_UNDERSTAND_MODEL=google/gemini-3.8-flash`，且没有同名进程环境覆盖。此前分析是显式传入 3.7 导致未采用该默认值。现在将 `.env.example` 同步为 3.8，并在项目 README 写明后续新理解请求采用 3.8，不复制历史 3.7 参数。语音转写默认已是 `openai/gpt-transcribe`。

默认解析用 `understand --dry-run` 验证，不调用 Gemini，也不覆盖旧模型记录。
