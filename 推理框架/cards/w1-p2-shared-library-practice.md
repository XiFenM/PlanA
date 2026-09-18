---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "44eeb0ec645c7e762084db83e1d67f1aa727fd5ed4b25c6a6d01444f6541cc1c",
  "candidate_sha256": "4a1e671863e437dde3a2d58be32c5dc7e465a528e1e14dcdd12e53b97e236038",
  "cards": [
    {
      "content_sha256": "3cc7f5ae891f5e570ad8dfa59786e429128eee3fb687f2c1fb2dae79d62e2062",
      "content_summary": "区分相同SONAME与所需函数符号可用性的保证",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "linux-dynamic-linking",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分相同soname与所需函数符号可用性的保证"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-fded6fee441f4f83762d70da",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p2-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ca82a94a7f60ddc664a0d3bfe29de44b81bc0a901d988ffe79a0e06b57ea7291",
      "content_summary": "限定延迟绑定场景中进入main对函数符号可用性的证明",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "linux-dynamic-linking",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "限定延迟绑定场景中进入main对函数符号可用性的证明"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a3cbf6efd67d3183ee107cf8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p2-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9332fbbeb5e332fe759aa18728d77be35a34011d83ee0dbb1e995bf0ead18342",
      "content_summary": "用新进程映射与原故障函数调用共同验证库路径修复",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "linux-library-diagnosis",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用新进程映射与原故障函数调用共同验证库路径修复"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b891108a311d074928232fc8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p2-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9c47ad400ae4d34100c5d7284e958580216330e38d78856484e65c7d3fd87195",
      "content_summary": "解释脚本未再次export时子进程仍继承已有环境变量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "linux-process-environment",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释脚本未再次export时子进程仍继承已有环境变量"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-adda45bf35d8cdba12a6a25e",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "p2-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "4c8fc7fc526b845074cb48151d54afab15953eb54d38083236e17dc11f01769a",
  "manifest_payload_sha256": "b8c7ad7df94164c11abece90652f73b176a597e3f86eca4c6104326c63ee2e01",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5548,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w1-p2-shared-library-practice-technical-qa.xlsx",
      "row_count": 4,
      "rows": [
        {
          "content_sha256": "3cc7f5ae891f5e570ad8dfa59786e429128eee3fb687f2c1fb2dae79d62e2062",
          "logical_id": "mc-fded6fee441f4f83762d70da",
          "row_sha256": "9df883df31c3f37567dead3225c109d6b0488a8b731e3bd17ac1bf191b853606"
        },
        {
          "content_sha256": "ca82a94a7f60ddc664a0d3bfe29de44b81bc0a901d988ffe79a0e06b57ea7291",
          "logical_id": "mc-a3cbf6efd67d3183ee107cf8",
          "row_sha256": "6b573d4c76d4695870196abe02c09d87b3a1d1172cdef282ec2e436ae8d27eaa"
        },
        {
          "content_sha256": "9332fbbeb5e332fe759aa18728d77be35a34011d83ee0dbb1e995bf0ead18342",
          "logical_id": "mc-b891108a311d074928232fc8",
          "row_sha256": "b6d6a775050a3bbea4febc8ece30358614d1f95e7a4c053737a4be1ae4b5b505"
        },
        {
          "content_sha256": "9c47ad400ae4d34100c5d7284e958580216330e38d78856484e65c7d3fd87195",
          "logical_id": "mc-adda45bf35d8cdba12a6a25e",
          "row_sha256": "98596686be351dca393d6f2f30faeb3b8a1ff405337f09a1a140884d01a90350"
        }
      ],
      "sha256": "2ae32d5dd15f0708e8f444d80753d619a54f3225f1e39a89fc8d7a0bc8108587",
      "sheet_name": "cards",
      "table_sha256": "b197926b3371046b7c189328c7367f030caf011807e00b18988a6d5812692c5d",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "148df862bf2c8cab36b750ce93c6c05bc32191dd11761ce73e59d5f2b2c8c526",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "p2-structured-log",
      "path": "推理框架/log/2026-09-18-w1-p2-shared-library-practice.md",
      "sha256": "38f04743e1bdf2572ae22ca6114cfe7bb4bd1447dba07e6f40d636f63d88f208",
      "summary": "W1-P2 已核验学习过程；仅采用稳定要点与真实纠错，不读取 raw 为卡片来源。"
    }
  ],
  "target_collection": "inference-cards",
  "template_registry_sha256": "358d0b6e1ee30ee06c0ae9636266ddafad6f2e81494f6d8975d68448e190996c",
  "template_registry_version": "1.1.0"
}
---
# Markji 表格导入卡片

> Markdown 保留受管元数据与模板定义；卡片数据请使用下列按模板拆分的 XLSX 文件导入。

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[w1-p2-shared-library-practice-technical-qa.xlsx](w1-p2-shared-library-practice-technical-qa.xlsx)（4 张卡）
