# 学习日志 · Day 03 — 2026-05-31 周日

> 格式见 [../review-workflow.md](../review-workflow.md) Step 2。每条带「场景」做记忆钩子。
> 学完当天就整理成墨墨表格（review-workflow Step 3 → `../cards/day-03.md`，待生成），当天即可导入复习。
>
> 来源：AI 教练对话——汇报 init.sh 的两个 bug（bun 装包缺 unzip、复用 Cloudflare 隧道时本机凭据文件丢失）让教练修，随后让教练把今日对话整理成日志。下面是这轮对话里的纠错点与词块。

## 报告"踩坑"的说法

- [纠错] ❌ Today, I find two small problem → ✅ Today I **ran into** two small **problems**
  - 场景：开头汇报"今天发现 init.sh 有两个小问题"
  - 为什么：发现/遇到问题用 run into（撞上），过去时 ran；两个 → 复数 problems
- [词块] run into a problem / a bug / an issue = 撞上、碰到一个问题
  - 场景：想说"今天遇到两个小问题"，比 find / meet a problem 地道
  - 为什么：工程师报告"踩坑"的默认动词，口语书面都常用

## 报错的固定搭配

- [纠错] ❌ reusing tunnel results in error → ✅ reusing **the** tunnel **throws an** error
  - 场景：描述"复用已有隧道会报错"
  - 为什么：报错的固定搭配是 throw an error（也可 raise / hit an error）；可数单数 the tunnel / an error 要带冠词

## help sb do sth（反复写 to）

- [纠错] ❌ Please help me **to** fix it / help me **to** generate → ✅ Help me **fix** it / help me **generate**
  - 场景：这轮对话里两次让教练帮忙（帮我修 bug、帮我生成日志），两次都加了 to
  - 为什么：help sb do sth，help 后面直接跟动词原形，不加 to，更口语；这是我反复犯的点

## 第三人称单数 + 名词选词

- [语法] ❌ bun installation need unzip → ✅ the bun **install needs** unzip
  - 场景：说"bun 的安装步骤需要 unzip"
  - 为什么：单数主语第三人称现在时用 needs；口语里 install（名词）比 installation 更常说

## 平级对话的口头禅

- [选择] Very good / Then … vs **Nice / Perfect / Looks good** + **Next / Now** …
  - 场景：开头想说"很好，那么接下来帮我生成日志"，我写成 "Very good. Then, please…"
  - 为什么：Very good 像老师批改评语；平级（engineer-to-engineer）夸"搞定了"用 Nice / Perfect / Looks good。承接下一步用 Next / Now 比 Then 自然，Then 更偏"那(逻辑结果)就…"

## 指给别人看文档的说法

- [选择] as reference vs **for reference**
  - 场景：想说"你可以读 markji 文档和这个目录里的其他文件作参考"，我写 "… and other documents as reference"
  - 为什么：for reference = 供参考（固定短语，最常用）；as a reference 只在"把某物当成那一份参考资料"时用，且要加冠词 a
- [词块] for reference = 供参考、作参考用
  - 场景：让同事去看支撑文档，又不强制照搬时
  - 为什么：工程师指人看 doc/ticket/example 的默认说法

## 语气：祈使句别老挂 please

- [选择] Please add … vs **Add …**（祈使句去掉 please 更像工程师）
  - 场景：给 AI / 同事派活"把上面的反馈加到日志里"，我习惯写 "Please add the feedback…"
  - 为什么：平级协作里直接用祈使句（Add… / Let's… / Can you…）更干脆；please 偏正式、偏请求，多了会显得拘谨。非对错问题，是 register（语域）

## 承认对方发现了遗漏

- [词块] good catch = 发现得好、亏你看到了
  - 场景：对方指出我漏了一个点（漏写、漏改、漏 case），想说"对，这个点抓得好"
  - 为什么：code review / PR 评论里承认队友抓到 bug 或缺口的高频回应
