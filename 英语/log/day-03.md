# 学习日志 · Day 03 — 2026-05-31 周日

> 记录性质：`legacy-derived` 学习记录。内容来自历史 AI 教练对话：汇报 init.sh 的两个问题（Bun 安装缺少 unzip、复用 Cloudflare 隧道时本机凭据文件缺失），随后整理了当时的纠错和表达。
> 来源限制：旧文件没有保留可核验的 provider、会话或消息边界；下列原表达和场景沿用历史记录，本次迁移不补造来源标识。
> 交接边界：只有用户明确要求时，才把已核验条目交给 `memo-cards` 预览；整理日志不会自动触发制卡、导入或其他收尾动作。

## 报告“踩坑”

- [纠错] 场景：开头汇报“今天发现 init.sh 有两个小问题”。我写“Today, I find two small problem” → 最小正确表达：`Today, I found two small problems.`；更贴近“踩坑”的表达：`Today, I ran into two small problems.` 原因：回顾当天已发生的事要用过去时，`two` 后接复数名词；`ran into` 是可选的语义升级，不是修复语法所必需。
- [要点] 工程师怎样表达“遇到一个问题”？——`run into a problem / bug / issue`，例如 `I ran into two small problems today.`

## 描述报错

- [纠错] 场景：描述“复用已有隧道会报错”。我写“reusing tunnel results in error” → 正确：`Reusing the tunnel results in an error`；也可说 `Reusing the tunnel throws an error.` 原因：这里的特定隧道需要 `the`，可数单数 `error` 需要 `an`；`results in` 本身并没有错，`throws` 只是更直接的工程表达。

## `help someone (to) do something`

- [要点] `help me to fix it` 必须删掉 `to` 吗？——不必；`help someone do` 和 `help someone to do` 都合乎语法。工程对话中 `Help me fix it` / `Help me generate the log` 更简洁，原形式不是语法错误。

## 第三人称单数与名词选择

- [纠错] 场景：表达“Bun 的安装步骤需要 unzip”。我写“bun installation need unzip” → 正确：`The Bun installation requires unzip.` 原因：单数主语需要第三人称单数谓语；在该工程语境中也要限定具体安装步骤。`install` 可作非正式名词，`installation` 并非原句的问题所在。

## 平级协作语气

- [要点] 完成一步后怎样自然承接下一步？——平级工程对话中可用 `Nice / Perfect / Looks good. Next, ...`。`Very good. Then, ...` 并非语法错误，但可能带有评价式或较书面的语气，是否替换取决于关系和场景。
- [要点] 怎样表达“供参考”？——通常用 `for reference`，例如 `Read these documents for reference.`；`as a reference` 表示把某个具体对象当作一份参考资料，需要冠词。
- [要点] 给 AI 或同事派活时必须去掉 `please` 吗？——不必。`Add ...` 更直接，`Please add ...` 更礼貌或正式，`Can you add ...?` 更像协作请求；这是语域选择，不是正误区别。
- [要点] 怎样承认对方发现了遗漏？——`Good catch.` 常用于 code review、PR 评论或调试中，表示“这个缺口发现得好”。
