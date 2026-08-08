# 学习日志 · Day 02 — 2026-05-27 周三

> 格式见 [../review-workflow.md](../review-workflow.md) Step 2。每条带「场景」做记忆钩子。
> 学完当天就整理成墨墨表格（review-workflow Step 3 → `../cards/day-02.md`，待生成），当天即可导入复习。
>
> 来源：AI 教练对话——解释墨墨复习流程的设想时，想法多、不知道怎么用英语表达，先用中文说了（⭐ 碰壁切中文，正是要补的缺口）。

英文版（可做 shadowing）：

> "I've got a lot of ideas here and I'm not sure how to **put** them **in English**, so let me explain in Chinese first. Here's the workflow I **have in mind**: ① **Spot the issue** — while I'm studying I hit something **worth memorizing** that isn't just a plain vocab word. ② **Jot it down** — I (or you, the AI coach) log it in that day's notes, in loose natural language, not strict card format."

## 词块

- [词块] ⭐ put sth in English = 把某事用英语表达（比 express in English 更口语）
  - 场景：想说"我不知道怎么用英语表达这些想法"
- [词块] ⭐ I have in mind = 我设想的 / 我心里想的（the workflow I have in mind）
  - 场景：想说"我设想中的流程是这样的"
- [词块] ⭐ something worth memorizing = 值得记的东西（worth + 动名词）
  - 场景：想说"遇到某个值得记忆的点"
- [词块] ⭐ jot it down = 随手记下（比 write it down 更轻、更口语）
  - 场景：想说"把它记进当天的文档"

## 复现 benchmark 结果 / 找现成工具

来源：AI 教练对话——讨论在多个 benchmark 上复现结果、想找现成的评测工具（提到 HMMT 2026 Feb）

- [纠错] ❌ reproduce the result of four datasets → ✅ reproduce **results on** four **benchmarks**
  - 场景：想说"在四个 benchmark 上复现结果"
  - 为什么：results **on** a benchmark 是标准搭配（不是 of）；而且这些是 benchmark，不只是 dataset
- [纠错] ❌ I don't know if I can use some software packages or libraries to test it → ✅ I'm not sure if there are **off-the-shelf tools** I can use to run these
  - 场景：想问"有没有现成的工具/库可以拿来跑"
  - 为什么：更地道；off-the-shelf 一个词就顶 "some software packages or libraries" 一长串
- [纠错] ❌ Please help me find if there is a tool I can use → ✅ Can you **point me to** any tools that would work?
  - 场景：想请对方推荐能用的工具
  - 为什么：point me to X 是地道的请求方式；"find if there is" 是中式英语腔
- [词块] ⭐ off-the-shelf = 现成的 / 开箱即用的（工具、库）
  - 场景："Is there an off-the-shelf harness for HMMT 2026 Feb?" / "We can't use off-the-shelf vLLM yet — the CSA kernels aren't upstreamed."
  - 为什么：infra 对话里在"用现成工具 vs 自己造"之间抉择时高频；反义词 in-house（we built it in-house ↔ we used off-the-shelf）

## 带新人上手 CUDA / C++（设计学习路径）

来源：AI 教练对话——说要给一个刚毕业的同事准备 tutorial，帮他系统地上手 CUDA 和 C++

- [纠错] ❌ fresh graduated colleague → ✅ **new grad** colleague / a colleague who **just graduated**
  - 场景：想说"一个刚毕业的同事"
  - 为什么："fresh graduated" 不是真实搭配；"new grad" 才是标准说法
- [纠错] ❌ they know some basics, but not systematic and solid → ✅ ... but **nothing structured** / but their **foundation isn't solid**
  - 场景：想说"他们懂点基础，但不系统、不扎实"
  - 为什么：英语里形容词不能这样悬空，要接名词或用完整从句（nothing structured / foundation isn't solid）
- [纠错] ❌ I hope I can give a systematic learning path for them → ✅ I want to **put together** a learning path **for** them
  - 场景：想说"我想给他们设计一条系统的学习路径"
  - 为什么：give X for them 介词错；put together 是工程师"设计课程/文档"的地道动词
- [词块] ⭐ get someone up to speed（兄弟说法 ramp someone up）= 让某人快速上手 / 跟上进度
  - 场景："I'm preparing this tutorial to get a new grad up to speed on CUDA and C++." / "we need to ramp him up on the inference stack before the next release" / "are you up to speed on the new TMA stuff?"
  - 为什么：AI Infra 团队带新人/onboarding 的标准说法，替代 "make them reach the level" / "help them become familiar" 这种中式翻译

## 口语：随口确认用 right?

来源：AI 教练对话——想确认"其他的都是免费的吧？"

- [纠错] ❌ Others are free, aren't they? → ✅ **The rest** are free, **right?** / **Everything else** is free, right?
  - 场景：想说"其他的都免费吧？"求个确认
  - 为什么：两点——① 母语者用 the rest / everything else 而不是光秃秃的 others；② 随口确认用 right?，而 aren't they? / isn't it? 这类 tag question 很书面、口语/聊天里几乎没人用
- [词块] ⭐ ..., right?（句尾随口确认的 tag）= ……对吧？
  - 场景："The KV cache lives in HBM, right?" / "We're still on CUDA 12.4 in prod, right?"
  - 为什么：工程师英语里万能的确认 tag，替代 isn't it / aren't they / don't you 这类几乎没人说的书面 tag question；句尾一挂，友好、低风险，方便对方顺手纠正你
