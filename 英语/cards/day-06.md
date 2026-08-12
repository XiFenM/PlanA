---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "candidate_sha256": "3c14cd932f0791b5f352e5a58088673f843c62d27884e9525f4fead1142cc3af",
  "cards": [
    {
      "content_sha256": "700cb6bf70cdcacbd611616ef1ab5170d371d3be683079bc4dbdd5a3d0b81b51",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "5580018df20ba39da2d346dde985fe573649344eaa8ddddcee2aec0016eb269b",
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
      "template_version": "1.0.0"
    }
  ],
  "managed_body_sha256": "a48be04b1a48e9e5bdcd5595178584b903b92998da6394e183681f9c88f528b2",
  "manifest_payload_sha256": "6f4cd1c85c2a8f6d219baba0f7882d955f3a1006946cd04a8aeee81a295df58d",
  "schema": "memo-cards.artifact/v1",
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
怎样表达“将 API 请求归一化为统一的引擎请求”？	normalize an API request into a canonical engine request	normalize A into B 强调多个外部表示收敛到统一的内部表示；如果只是一般转换、不强调规范化，可按语境使用 convert、map 或 translate。示例：Under this design, the frontend would normalize the API request into a canonical engine request before crossing the IPC boundary.	描述一种假设的系统设计：前端在跨 IPC 边界前将外部协议请求转换为稳定内部表示
怎样表达“某项状态仍由 API server 进程持有或负责”？	remain owned by the API server process	remain owned by 强调所有权或生命周期责任没有随边界转移，不只是对象物理上仍在某处。示例：Under this design, the HTTP connection and response-stream state would remain owned by the API server process.	在假设的跨进程设计中区分 API 边缘状态与跨边界传递的内部请求
```
