---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "candidate_sha256": "6e2e97d75da7919cf7730af6dc2f25e0d5b2f6323234a6ff6eb4948a98f130e4",
  "cards": [
    {
      "content_sha256": "cdd8f19d3a496bc8e9ad556e07447e58baef8241f4709b73c9ea24f1b4d26502",
      "content_summary": "主动产出 write up my study notes as a blog post，并区分 write up 与一般 write 的侧重点。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "production",
        "domain": "english-expression",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "主动表达将学习笔记整理成博客文章"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-efc48f267d52372ab3db2753",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "english-day-04-log"
      ],
      "successor_to": null,
      "template_id": "active-production",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "0ab2c882e6a7446d6aed59ccd94acfd9af4440d05ed7fc2da90e69501b1473f4",
      "content_summary": "主动产出 start by reading both pieces，并掌握 both 与 pieces 的上下文边界。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "production",
        "domain": "english-expression",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "主动表达先从阅读两篇文章开始"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-fb796aca4feff08d5ee3546a",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "english-day-04-log"
      ],
      "successor_to": null,
      "template_id": "active-production",
      "template_version": "1.0.0"
    }
  ],
  "managed_body_sha256": "4c2d05e7f1487fab63093baee4a35c67307f4252a76f1ae66d3003826c54337e",
  "manifest_payload_sha256": "3efb91bbe2636eb614a39e9e03c92f618d5a904f0651d189db815880f0b160cf",
  "schema": "memo-cards.artifact/v1",
  "source_fingerprint": "9139dbd65cd3af7583d55cc85971f34bd9efd8969d6f9a05297f6e3ba6be183f",
  "sources": [
    {
      "collection": "english-study-logs",
      "id": "english-day-04-log",
      "path": "英语/log/day-04.md",
      "sha256": "7ddf7113315d924988bbfa827dd4a0420eb3cf8d67bd552b01bf9b948ab28f18",
      "summary": "legacy-derived 结构化日志；2026-08-12 定向语言复核确认表达自然度、适用边界与主动产出价值。旧记录缺少学习者原句，因此不构成纠错证据。"
    }
  ],
  "target_collection": "english-cards",
  "template_registry_sha256": "d6cdcd90c996ca6922a06f02a44b06800468a557bec6ad5c433511d7b57761d7",
  "template_registry_version": "1.0.0"
}
---
# Markji 表格导入暂存

> 供粘贴进 Markji 下载表格；这不是可直接上传的 TSV 文件。

## 主动产出卡

模板 `active-production@1.0.0`：

```text
[P#H1#{{提示}}]
---
[T#B,!36b59d#{{目标表达}}]
{{边界}}
📍 [T#!939393#{{场景}}]
```

```tsv
提示	目标表达	边界	场景
怎样表达“把学习笔记整理成博客文章”？	write up my study notes as a blog post	write up 强调把零散笔记整理成较完整的文稿；若只想表达一般性的“写”，可直接用 write。示例：I studied Ezyang's PyTorch Internals and wrote up my notes as a two-part blog series.	向协作者介绍自己把 PyTorch Internals 学习笔记整理成博客文章
怎样表达“先从阅读这两篇文章开始”？	start by reading both pieces	start by doing 表示先做某事；both 只用于上下文已经明确的两项，pieces 在这里指两篇书面作品。示例：Please start by reading both pieces—the introduction and the main article.	请协作者先阅读引言和正式文章，再继续后续工作
```
