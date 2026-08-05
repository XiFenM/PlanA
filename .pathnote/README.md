# 同路志内容发布说明

同路志只读取 `publications/<slug>/` 中显式创建的发布包。仓库原有的学习笔记、周报、进度、日志、卡片和 Obsidian 文件不会因为提交到 `main` 而自动发布。

发布包中的 `status` 还需要满足网站门禁。`draft` 和 `reviewed` 不会进入生产网站，只有完成审核并明确改为 `published` 的内容才会进入公开索引。

## 公开仓库边界

这个仓库是公开仓库。`draft` 只控制同路志是否收录内容，不能保护已经提交到 GitHub 的文件。发布包及其引用的证据不得包含以下信息：

- 密钥、令牌、Cookie 和登录凭证；
- 公司内部系统名称、私有主机名、内部任务编号和不能公开的工作资料；
- 个人绝对路径、请求 ID 和包含敏感内容的原始输出；
- 未取得公开使用许可的文章、图片、截图、代码、数据和授权证明原件。

转载收藏和以翻译为主的笔记不能默认作为原创内容发布。确实取得授权时，需要在 `rights` 中记录授权范围，授权证明原件继续保存在公开仓库之外。

## 发布包结构

```text
publications/
└── <slug>/
    ├── publication.json
    ├── index.mdx
    └── assets/            # 可选，只保存当前发布包使用的小型资源
```

`<slug>` 只使用小写英文字母、数字和连字符，并与 `publication.json.slug` 保持一致。`index.mdx` 从二级标题开始，一级标题由网站根据 manifest 生成。正文图片、字幕和下载文件放在当前包的 `assets/` 中，不使用 Obsidian 双链、本地绝对路径或任意脚本。

## 创建内容

1. 复制 `.pathnote/templates/publication/`，将副本命名为 `publications/<slug>/`。
2. 修改 `publication.json` 中的 slug、标题、摘要、日期、类型和主题。
3. 在 `index.mdx` 中整理面向读者的正文，并记录主要来源和结论边界。
4. 分别核对正文、图片、代码和数据的权利信息。第三方材料需要逐项记录来源与许可。
5. 检查正文、metadata 和证据中没有不适合公开的信息。
6. 暂存准备提交的内容，并校验暂存区生成的固定快照。校验器读取 Git 对象，不读取未暂存的工作树内容。

新包保持 `draft`，三项审核保持 `pending`。内容、权利和敏感信息审核全部通过并绑定同一个审核摘要以后，才能改为 `reviewed`。`published` 属于正式发布动作，不能用来跳过页面预览和发布检查。

## 本地校验

准备提交以前，先暂存发布包和它引用的仓库文件，再运行：

```bash
node .pathnote/pathnote-source-check.mjs --source plana --staged
```

计算准备审核的暂存快照摘要：

```bash
node .pathnote/pathnote-source-check.mjs \
  --source plana \
  --staged \
  --digest <slug>
```

命令会输出 `<slug>: sha256:...`。审核人员应当针对这个暂存快照完成内容、权利和敏感信息审核，再把其中的 `sha256:...` 原样写入 `reviews.subjectDigest`。正文、metadata、资源或引用证据发生变化以后，需要重新计算摘要并重新审核。

校验当前 commit：

```bash
node .pathnote/pathnote-source-check.mjs \
  --source plana \
  --head "$(git rev-parse HEAD)"
```

检查两个 commit 之间的发布状态迁移：

```bash
node .pathnote/pathnote-source-check.mjs \
  --source plana \
  --base <base-commit> \
  --head <head-commit>
```

`.pathnote/pathnote-source-check.mjs` 由同路志网站工程生成，并由 `.pathnote/contract-lock.json` 固定版本和 SHA-256。不要在本仓库中单独修改 bundle、锁文件或发布模板。校验失败时，发布包不能进入预览或触发新的站点构建。

## 共享校验器受控升级

Pull Request 校验由目标分支中的 `pull_request_target` workflow 定义。工作流先检出 base 仓库和固定 SHA，从中提取校验器和锁文件，再获取 head 的 Git 对象进行只读检查。`origin` 始终指向 base 仓库，工作流绝不执行 head 中的脚本。这个信任边界必须保留：workflow 继续使用只读权限，检出代码时不保留凭证。

升级共享校验器时，管理员按照以下顺序操作：

1. 从同路志网站工程取得新的完整分发，独立核对 bundle、模板哈希和 `.pathnote/contract-lock.json` 中的 `distributionSha256`。
2. 把核对后的 64 位 `distributionSha256` 临时写入仓库变量 `PATHNOTE_CHECKER_UPGRADE_SHA256`。
3. 建立一个只包含本次 `.pathnote` 工具分发文件的 Pull Request。这个 Pull Request 不混入发布包、workflow 或其他仓库改动。
4. 等待受保护的 PathNote 校验通过并合并，然后立即清空 `PATHNOTE_CHECKER_UPGRADE_SHA256`。

必须用 branch protection 或 ruleset 保护 `main`，把 PathNote 校验设为必需检查，要求 Pull Request 在合并前与目标分支保持最新，并要求维护者审核 `.github/workflows/pathnote-content.yml` 的改动。普通内容 Pull Request 不能修改或绕过这条信任链。

## GitHub Actions

`.github/workflows/pathnote-content.yml` 在以下情况运行：

- Pull Request 发生变更时，使用目标分支中受信任的校验器对比 base 与 head；
- `main` 收到变更时，校验合并后的 head，并判断发布包或其引用文件是否发生变化；
- 维护者通过 `workflow_dispatch` 重新检查指定 commit 或当前 commit。

预览构建触发目前没有完成联调。工作流中的触发 job 由仓库变量 `PATHNOTE_PREVIEW_TRIGGER_ENABLED` 控制；变量不存在或不等于 `true` 时不会发送网络请求。只有 `main` 中的发布包或被引用文件确实发生变化，或者维护者在手动运行时明确选择触发，才会调用 Hook。完成预览端点、并发和重复触发验证以后，维护者还需要：

1. 建立受保护的 `pathnote-preview` environment；
2. 将 Deploy Hook 保存为 environment secret `PATHNOTE_PREVIEW_DEPLOY_HOOK_URL`；
3. 确认 Hook 只生成隔离、禁止索引的预览；
4. 将仓库变量 `PATHNOTE_PREVIEW_TRIGGER_ENABLED` 设为 `true`；
5. 执行一次真实触发并保存验证结果。

如果 Hook 泄漏或行为异常，先将开关改为 `false`，再删除并轮换 secret。Pull Request 和校验失败的提交不会触发 Deploy Hook。手动运行及其重跑会沿用 `trigger_site` 输入；只有维护者明确选择触发并且仓库开关为 `true` 时，工作流才会发送请求。
