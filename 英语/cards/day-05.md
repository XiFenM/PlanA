---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "7c36a815a862f87cfe1b9bb7430e7d627aba142f398af8e9bcd1e4d8b1c835f3",
  "candidate_sha256": "04d072199912ac264f1dd9946655627f67aea98bd81fd584784b438f18913c53",
  "cards": [
    {
      "content_sha256": "eb23e217d5967c368bd8cd54329052d1f63b576ef3bab01fe8e7b411425de489",
      "content_summary": "主动产出 turn an entire Git repository into an interactive code knowledge graph，并掌握 turn A into B 的结构。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "production",
        "domain": "english-expression",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "主动表达将整个 git 仓库转换为可交互代码知识图谱"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1e655c30d6cc98adf68462fb",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "english-day-05-log"
      ],
      "successor_to": null,
      "template_id": "active-production",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5028b4ee8783dd384148a3eb365c9ca716bb2f5f52d0d5e61ae0ad56d7240d4c",
      "content_summary": "主动产出 get up to speed on an unfamiliar codebase，并掌握其“达到可工作理解”的边界。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "production",
        "domain": "english-expression",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "主动表达快速熟悉陌生代码库"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c44ae3571855a03f4c4e3c06",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "english-day-05-log"
      ],
      "successor_to": null,
      "template_id": "active-production",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "7fcbc8ed1a9b9f9423ff31c167c31572d0994cc88174b26658287df07cd315be",
  "manifest_payload_sha256": "f2ee0ef66124bcf5166a0df5b0863609c8915410d191ceb7e6e3f4d785d533a6",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 3933,
      "columns": [
        "提示",
        "目标表达",
        "边界",
        "场景"
      ],
      "kind": "markji-import-xlsx",
      "path": "英语/cards/day-05-active-production.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "eb23e217d5967c368bd8cd54329052d1f63b576ef3bab01fe8e7b411425de489",
          "logical_id": "mc-1e655c30d6cc98adf68462fb",
          "row_sha256": "76a674311a78e96f2c7d335b0f455b494c912c9dd6357ab4495aa09652723b32"
        },
        {
          "content_sha256": "5028b4ee8783dd384148a3eb365c9ca716bb2f5f52d0d5e61ae0ad56d7240d4c",
          "logical_id": "mc-c44ae3571855a03f4c4e3c06",
          "row_sha256": "5f750ac470eccb2f349784e472df353a7a172c5add2a088bf410a39ab00b0356"
        }
      ],
      "sha256": "362011f34f043b653cc4db8d8daaad9c4aadfb134e9f4bf6830a1434ac10e176",
      "sheet_name": "cards",
      "table_sha256": "d59fd6d0ce580690f5e4ad02f4ba8bbf3eb8b441ef03ec25e7659ec43d9a9256",
      "template_id": "active-production",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "2a446f04e3efe30fc3468154c54b6af4d93bcd9f8027987a080bc7179cdd0d13",
  "sources": [
    {
      "collection": "english-study-logs",
      "id": "english-day-05-log",
      "path": "英语/log/day-05.md",
      "sha256": "e05f2fc5918a9d1fe96e8a036b0a01b56ba27429f5d99e6ce04987156f6c36a0",
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

导入文件：[day-05-active-production.xlsx](day-05-active-production.xlsx)（2 张卡）
