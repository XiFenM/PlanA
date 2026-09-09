---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "c0bdbd838c3b8d7b88e5dced086ba50088a741bb4cbbc32355525ce17f5fbf0f",
  "candidate_sha256": "4bb84d37ddf4cc790c283e09dfb1139964e43b3e1144bb81b90ab9bff52040eb",
  "cards": [
    {
      "content_sha256": "7a06dbcc8872a84c03ba8337113813ce64443cf88fa6efd2a0f173cc96159ec9",
      "content_summary": "page_size_padded 是总页字节配置，page_size_bytes 是只读派生属性；冻结规格通过构造或 replace 设置。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-kv-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分 attention 页大小的配置字段与只读派生属性"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e2bb3d174402490d55dad13a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "91119d59311f07a6bbbd35bd8af48cbf6869deed668c2f77bd4a63167fc57d0a",
      "content_summary": "page_size_padded 同时控制普通 view 的 padding 分支；只改 getter 不能兑现 view 与 kernel 的寻址契约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-kv-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释只改页大小返回值不能保证页尾 padding 访问正确的原因"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-93f0de5e8b00c29d92e3be7f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b92de65d7f19a403c4ae5aaf49305ce279a6c9c32bd30ba954e24f7f0f880989",
      "content_summary": "块数从原始 int8 存储字节数计算，不能混用 BF16 逻辑 view 的 numel；256 KiB 对应 4 个 64 KiB 页或 2 个 128 KiB 页。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-kv-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "使用原始字节存储而非带 padding 的逻辑 view 元素数计算页块数"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-acc5bf9ee669dda4d35f5fbf",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cd82b3de9de483f2513324b7a6b281aedc46deb7445da2985538ff2c63153bae",
      "content_summary": "BF16 块 stride 由页字节跨度除以 2 得到；页尾 padding 不把 head_size 从 96 改成更大的逻辑维度。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-kv-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "把页字节跨度换算为 tensor 块维度的元素 stride"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-093515310c87439e9bb4a53e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6c5a6f1d15563a3326d1f06b8ae9e85436848c91747985796fa66cc0763fdad9",
      "content_summary": "串联固定主线快照的普通单层单组页大小消费链；不推广为插件字段重构禁令。",
      "dependency_content_sha256": {
        "mc-093515310c87439e9bb4a53e": "cd82b3de9de483f2513324b7a6b281aedc46deb7445da2985538ff2c63153bae",
        "mc-93f0de5e8b00c29d92e3be7f": "91119d59311f07a6bbbd35bd8af48cbf6869deed668c2f77bd4a63167fc57d0a",
        "mc-acc5bf9ee669dda4d35f5fbf": "b92de65d7f19a403c4ae5aaf49305ce279a6c9c32bd30ba954e24f7f0f880989",
        "mc-e2bb3d174402490d55dad13a": "7a06dbcc8872a84c03ba8337113813ce64443cf88fa6efd2a0f173cc96159ec9"
      },
      "depends_on": [
        "mc-093515310c87439e9bb4a53e",
        "mc-93f0de5e8b00c29d92e3be7f",
        "mc-acc5bf9ee669dda4d35f5fbf",
        "mc-e2bb3d174402490d55dad13a"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-kv-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释普通单层单组页大小在预算分配视图与 kernel 访问中的一致性链条"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3dc0573e6efa8009574ea78d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "fb895b165fa5ae327799e97bf5748f0097ab96f4b506c6b6589f6ede72c463c4",
  "manifest_payload_sha256": "edf7e3e42a87756ae61f709c7656d23f14e7106f3eaf83541b17ff3ec70fab66",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 7846,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/kv-page-size-interface-technical-qa.xlsx",
      "row_count": 5,
      "rows": [
        {
          "content_sha256": "7a06dbcc8872a84c03ba8337113813ce64443cf88fa6efd2a0f173cc96159ec9",
          "logical_id": "mc-e2bb3d174402490d55dad13a",
          "row_sha256": "235a2c65270374f57e40b1cf3ce53c7258db0a673dea92daa7448dfcaed2cbb6"
        },
        {
          "content_sha256": "91119d59311f07a6bbbd35bd8af48cbf6869deed668c2f77bd4a63167fc57d0a",
          "logical_id": "mc-93f0de5e8b00c29d92e3be7f",
          "row_sha256": "0a580ae67f04990be6b2f5e0f5cfa94f8dfa9df273ae0c38028663a9c35760d4"
        },
        {
          "content_sha256": "b92de65d7f19a403c4ae5aaf49305ce279a6c9c32bd30ba954e24f7f0f880989",
          "logical_id": "mc-acc5bf9ee669dda4d35f5fbf",
          "row_sha256": "f27c2a2dda2f12ce2e63f30aea2330b7de9e5de2fd94464dfc9bc31c3742e863"
        },
        {
          "content_sha256": "cd82b3de9de483f2513324b7a6b281aedc46deb7445da2985538ff2c63153bae",
          "logical_id": "mc-093515310c87439e9bb4a53e",
          "row_sha256": "e4928ce55262705553703997e93cca506b60b2af0bdc6a8abcb252b47b2c628b"
        },
        {
          "content_sha256": "6c5a6f1d15563a3326d1f06b8ae9e85436848c91747985796fa66cc0763fdad9",
          "logical_id": "mc-3dc0573e6efa8009574ea78d",
          "row_sha256": "b36376c5f5cc49d3205a01b47f4f4c3dddfc52674b0c6fc7b20a20373ae4a8c4"
        }
      ],
      "sha256": "4312b80663160f72d57851c4491ca7e17189d4c7c875917f2b42929e01d34740",
      "sheet_name": "cards",
      "table_sha256": "83d9fa11e4bb0bb2507abfe66322571ec2f3948423b3330bc92004698768a512",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "8d5a9aa525fe280c916edeaaa04d68d1e3a44aec56981767241c02b078cfc424",
  "sources": [
    {
      "collection": "inference-adaptation-evidence",
      "id": "kv-spec-learning-evidence",
      "path": "推理框架/EP-PD自研芯片适配设计与验证包.md",
      "sha256": "3d0c46acd756e1c2283c079e2b4912d0b27e0b5dc13dac85e0e51e66b7fb60d2",
      "summary": "仅采用 2026-09-09 kv-page-spec-review 复习片段和固定 vLLM v0.26.0 源码锚点；实现由对应 commit 的 AttentionSpec、MRV1、attn_utils 与 kv_cache_utils 裁决，不采用私有插件历史限制或课程待办。"
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

导入文件：[kv-page-size-interface-technical-qa.xlsx](kv-page-size-interface-technical-qa.xlsx)（5 张卡）
