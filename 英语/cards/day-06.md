---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "c586d580ac90c3a1d6cceb02862ab11f16b276468b4e9756d91313f1fab1bd0e",
  "candidate_sha256": "4aaf528600e3c90c03d063597a568883941f65156132f1be7e27a9a7ca4d77de",
  "cards": [
    {
      "content_sha256": "51d6f727c7ac07b245a88ff346ae847f8aaad41dd2f75c405a3359a5f5a8fd56",
      "content_summary": "主动产出 normalize an API request into a canonical engine request，并区分规范化与一般转换。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "production",
        "domain": "english-expression",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "主动表达将 api 请求归一化为统一的引擎请求"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7079642f0c830ae341d66d7a",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "english-day-06-log"
      ],
      "successor_to": null,
      "template_id": "active-production",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f260045b11761243bbe7c4c048d9108db65103caa62faf4c3589f4893b1a0c7f",
      "content_summary": "主动产出 remain owned by the API server process，并掌握其所有权与生命周期责任边界。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "production",
        "domain": "english-expression",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "主动表达某项状态仍由 api server 进程持有或负责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3a7bc5b6aaf95736d3178fd5",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "english-day-06-log"
      ],
      "successor_to": null,
      "template_id": "active-production",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "260dbadacb82e4fc8be64780026e4a49db49bacce9430d3bb032ae3c219c0118",
  "manifest_payload_sha256": "6a39f797a6cd66bf055230a3a1014ad80bb68a3a76f64c6726c0ca14f0b7307d",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 4095,
      "columns": [
        "提示",
        "目标表达",
        "边界",
        "场景"
      ],
      "kind": "markji-import-xlsx",
      "path": "英语/cards/day-06-active-production.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "51d6f727c7ac07b245a88ff346ae847f8aaad41dd2f75c405a3359a5f5a8fd56",
          "logical_id": "mc-7079642f0c830ae341d66d7a",
          "row_sha256": "229be96dd2e5e3d8011f79fb2ce51137c5848827cf34f1783f4d75871ceee62e"
        },
        {
          "content_sha256": "f260045b11761243bbe7c4c048d9108db65103caa62faf4c3589f4893b1a0c7f",
          "logical_id": "mc-3a7bc5b6aaf95736d3178fd5",
          "row_sha256": "51c8a13d4975bc211ed4c671cc543487da965d35417758b18c720cf786dc2aa2"
        }
      ],
      "sha256": "7de8ec2a37e590f379c4f9d194af6aceaa389bbc993b8f8b1260f5a922948654",
      "sheet_name": "cards",
      "table_sha256": "12c28cbf4e7cb6a9edc7ab9e46f5067fefcc080d38ad07af6dd06d86e467f068",
      "template_id": "active-production",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "b23703f0fbed2b7864ec44f9897d2688a64ffb7d72e532b4bdac1c9cd84b9714",
  "sources": [
    {
      "collection": "english-study-logs",
      "id": "english-day-06-log",
      "path": "英语/log/day-06.md",
      "sha256": "177c73757246978c6372b18e06ac143fb5928578ec5ec994520da99bde3384e4",
      "summary": "legacy-derived 结构化日志；经定向语言复核，仅将两条稳定表达作为主动产出候选。旧记录缺少可核验的学习者原句、会话 ID 和消息边界，因此不构成纠错证据。"
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

导入文件：[day-06-active-production.xlsx](day-06-active-production.xlsx)（2 张卡）
