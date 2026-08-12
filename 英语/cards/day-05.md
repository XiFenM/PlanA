---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "candidate_sha256": "870ab976ead76c138e920d30b221813a41a64e559654442d1404b56f5edcf08e",
  "cards": [
    {
      "content_sha256": "6a4282c36d1503c37b11bb65e87f363cfe98842f6b92a8d1ef854693a2f9a0d8",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "f98a926dca894b12b155571c539ecd789fcdb220e0bad1aed61ab2b1a4ce0857",
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
      "template_version": "1.0.0"
    }
  ],
  "managed_body_sha256": "2c37733890c5d2f5ac01c1ab4255a44baecfe163145ccb53845b47b66d12c533",
  "manifest_payload_sha256": "c646ae307a05f1ee86a64a3f06463429c0f4a2e2e18bc19f7b287be674f8d34a",
  "schema": "memo-cards.artifact/v1",
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
怎样表达“把整个 Git 仓库转换成可交互的代码知识图谱”？	turn an entire Git repository into an interactive code knowledge graph	turn A into B 表示把 A 转换为 B；entire 强调整个仓库，interactive code knowledge graph 比泛称 code map 更具体。示例：I am looking for an open-source tool that can turn an entire Git repository into an interactive code knowledge graph.	描述 Graphify、CodeGraph 等源码可视化工具的目标
怎样表达“快速熟悉一个陌生代码库”？	get up to speed on an unfamiliar codebase	get up to speed on 表示快速补齐背景并达到可工作的理解程度，不等同于完全掌握。示例：A good code map can help me get up to speed on an unfamiliar codebase.	说明希望借助代码图谱快速学习 vLLM 等开源项目
```
