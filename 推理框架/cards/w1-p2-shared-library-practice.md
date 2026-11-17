---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "69a5b61b0ffbf7ebfc8c81135a2270e26d35a9d0572c21496cc4edcbba7df7e8",
  "candidate_sha256": "19d9228d1b43733f04faffeb016aac19af71b4a79e576aeca1d09125085f62f1",
  "cards": [
    {
      "content_sha256": "928fb64966e55f459deea019231efbc306001b1701b21a667632973021e4b3d2",
      "content_summary": "A理由：防止把相同 SONAME 当成接口兼容证明，定位运行时装载旧库或缺少所需符号。",
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
      "content_sha256": "691211e7ef7cb1e17024ab750eaad34d95fdf24af0e02d31e62eb9d9f7a34c30",
      "content_summary": "A理由：防止把到达首次目标调用前的 READY 当成接口可用证据，识别延迟绑定的缺符号故障。",
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
      "content_summary": "A理由：防止只验证启动或当前 ldd 就宣布修复，要求新进程映射与原故障调用共同闭环。",
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
      "content_sha256": "e6d2cfafa7c8a0b2794255278f8c19662e5f2b1c25a11d4e8a2c95300ec32f72",
      "content_summary": "B理由：解释父环境变量如何继续传给子进程，避免把未再次 export 误当变量不存在。",
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
  "manifest_payload_sha256": "99024f09ab30bc5b3a86f518c7d22717dffa1cd2a338ed74d6f99a4c971617e9",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5906,
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
          "content_sha256": "928fb64966e55f459deea019231efbc306001b1701b21a667632973021e4b3d2",
          "logical_id": "mc-fded6fee441f4f83762d70da",
          "row_sha256": "16b1cb21484f613f46330822fd7242aba336bae8f9508bc3720b392e574199ec"
        },
        {
          "content_sha256": "691211e7ef7cb1e17024ab750eaad34d95fdf24af0e02d31e62eb9d9f7a34c30",
          "logical_id": "mc-a3cbf6efd67d3183ee107cf8",
          "row_sha256": "d3390c4383a3278c9fbd69b0ad6abc7ef3e86cc0998dc7f5655169b843b43221"
        },
        {
          "content_sha256": "9332fbbeb5e332fe759aa18728d77be35a34011d83ee0dbb1e995bf0ead18342",
          "logical_id": "mc-b891108a311d074928232fc8",
          "row_sha256": "b6d6a775050a3bbea4febc8ece30358614d1f95e7a4c053737a4be1ae4b5b505"
        },
        {
          "content_sha256": "e6d2cfafa7c8a0b2794255278f8c19662e5f2b1c25a11d4e8a2c95300ec32f72",
          "logical_id": "mc-adda45bf35d8cdba12a6a25e",
          "row_sha256": "9bc5e5579d137ed3499cdcc08fd1c299a6f1962e1100a73d52c51fd265a27983"
        }
      ],
      "sha256": "30b62a582f98552e361503520de44ca29503c30a6932e240320dc10e5a19f282",
      "sheet_name": "cards",
      "table_sha256": "77fa4869091dc9120799dbd7cdccb7abe9a24b1d95e170d03c1e701c45e08ca2",
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
