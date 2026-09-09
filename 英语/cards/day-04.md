---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "bc735573983be730120452f406aa9efba1274119007a66f3344ad289ca708c24",
  "candidate_sha256": "d0cb048f54e0736a87f3590db350187fe7193e3acfdb0c7b2207266b9c8328c0",
  "cards": [
    {
      "content_sha256": "ce0ddc656e43917cbe982b52110c3ded64c32e7070670269948a30b382059346",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "45158a3c1b07b83a57d31c30f615679b0a465e12db384a61115c46ad764f601a",
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
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "3a6ba8dc1d198b66bc8a5c34b6b881513f91fe566fbc1c69967bef0348913f12",
  "manifest_payload_sha256": "9f71b7826a9f19b6b24d7b408d2e09aa5fe54ecf97d8c3b37c39fd26ac9fdc2d",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 3791,
      "columns": [
        "提示",
        "目标表达",
        "边界",
        "场景"
      ],
      "kind": "markji-import-xlsx",
      "path": "英语/cards/day-04-active-production.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "ce0ddc656e43917cbe982b52110c3ded64c32e7070670269948a30b382059346",
          "logical_id": "mc-efc48f267d52372ab3db2753",
          "row_sha256": "ba7b22ecd20919ee957cc1f1d0926b9e3ca3534fe2ced6bc49fdd0374a52e664"
        },
        {
          "content_sha256": "45158a3c1b07b83a57d31c30f615679b0a465e12db384a61115c46ad764f601a",
          "logical_id": "mc-fb796aca4feff08d5ee3546a",
          "row_sha256": "0022b8f07f9b9810a60f0feee8c8ef882329eeca741fdc42504c674d2dc15a10"
        }
      ],
      "sha256": "38167e1dac270222fa7dc794fc942ecd6514ce55a0fca94e6b212f21b81b65a5",
      "sheet_name": "cards",
      "table_sha256": "c95db80e25d007e550b31804feeb6d4acff3e3c2c9fe456479ea7ee7e29f9832",
      "template_id": "active-production",
      "template_version": "1.1.0"
    }
  ],
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
  "template_registry_sha256": "358d0b6e1ee30ee06c0ae9636266ddafad6f2e81494f6d8975d68448e190996c",
  "template_registry_version": "1.1.0"
}
---
# Markji 表格导入卡片

> Markdown 保留受管元数据与模板定义；卡片数据请使用下列按模板拆分的 XLSX 文件导入。

## 主动产出卡

模板 `active-production@1.1.0`：

```text
[P#H1#{{提示}}]
---
[T#B,!36b59d#{{目标表达}}]
{{边界}}
📍 [T#!939393#{{场景}}]
```

导入文件：[day-04-active-production.xlsx](day-04-active-production.xlsx)（2 张卡）
