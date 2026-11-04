---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "b435abf29229d4a4d38ae22897c64fa15b488b3037e3308640ca4eb008da017c",
  "candidate_sha256": "77e8df5a36ac65ba3717804a18283873fa70c41cb434094b03c2c22644604f95",
  "cards": [
    {
      "content_sha256": "acf4fdc169bc2465fb30e7f38b32e617172c834b6f804c06011e78a178cf61a8",
      "content_summary": "B理由：辨析配置字段与派生只读属性，避免在固定接口上使用错误的修改入口。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d39542c2d31577fb9190b8e5048ce839f7e81886436fe5d11ed01d91c7a336ad",
      "content_summary": "A理由：防止只扩容页字节数却让view或kernel仍按旧跨度寻址，造成KV读写错误。",
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
      "content_sha256": "91464cbaf1c0fcc0966ac8752000eaf78ce10064ef68c9e03ece0e29c8d892a5",
      "content_summary": "A理由：防止用逻辑元素数冒充含padding的字节容量，算错可分配块数。",
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
      "content_sha256": "44a1a9a61d60893c6871be549a93b70d68b843b947698d6f0446328893783196",
      "content_summary": "B理由：保持字节跨度与元素stride的单位一致，巩固页尾padding不改变逻辑head维度的关系。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d90de1a9007ca0e2058cb539b51759b8eee49f589fa937b82cf11bba28ac8c5c",
      "content_summary": "A理由：回答KV页规格适配如何贯穿预算与kernel的设计题，防止各层对同一存储布局解释不一致。",
      "dependency_content_sha256": {
        "mc-093515310c87439e9bb4a53e": "44a1a9a61d60893c6871be549a93b70d68b843b947698d6f0446328893783196",
        "mc-93f0de5e8b00c29d92e3be7f": "d39542c2d31577fb9190b8e5048ce839f7e81886436fe5d11ed01d91c7a336ad",
        "mc-acc5bf9ee669dda4d35f5fbf": "91464cbaf1c0fcc0966ac8752000eaf78ce10064ef68c9e03ece0e29c8d892a5",
        "mc-e2bb3d174402490d55dad13a": "acf4fdc169bc2465fb30e7f38b32e617172c834b6f804c06011e78a178cf61a8"
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
      "review_resolution": {
        "summary": "2026-11-03已对照四张页规格子卡和迁移后仍保持同一固定源码锚点的W1复习片段，复核页大小配置、原始字节容量、BF16元素stride与kernel访问链；题面已前置普通未量化、单层单组、无packed/CP/override等条件，结论未外推到任意backend。"
      },
      "source_ids": [
        "kv-spec-learning-evidence"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "fb895b165fa5ae327799e97bf5748f0097ab96f4b506c6b6589f6ede72c463c4",
  "manifest_payload_sha256": "5b1a85cd94b419fa4ee1eeb1f6e77025fc0b2463ddb493ed3b00f3f8ebd9bfc5",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 8855,
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
          "content_sha256": "acf4fdc169bc2465fb30e7f38b32e617172c834b6f804c06011e78a178cf61a8",
          "logical_id": "mc-e2bb3d174402490d55dad13a",
          "row_sha256": "9b797c1eca515a1bc9151c713ba9fe64e02df21d99c97931040cef3f94ad43bf"
        },
        {
          "content_sha256": "d39542c2d31577fb9190b8e5048ce839f7e81886436fe5d11ed01d91c7a336ad",
          "logical_id": "mc-93f0de5e8b00c29d92e3be7f",
          "row_sha256": "df219249ab1d2d66742e887babc8b75d86092df086e40621d65b42f1a29f2af8"
        },
        {
          "content_sha256": "91464cbaf1c0fcc0966ac8752000eaf78ce10064ef68c9e03ece0e29c8d892a5",
          "logical_id": "mc-acc5bf9ee669dda4d35f5fbf",
          "row_sha256": "2b0f18683de2dcace9b53fe18cebfa25f905d098041ffdb63c2a3247dc3705e4"
        },
        {
          "content_sha256": "44a1a9a61d60893c6871be549a93b70d68b843b947698d6f0446328893783196",
          "logical_id": "mc-093515310c87439e9bb4a53e",
          "row_sha256": "efce4c3fe46a65c8782884e83ccecbf8dae5e1b12678866966dfa5b493a4790a"
        },
        {
          "content_sha256": "d90de1a9007ca0e2058cb539b51759b8eee49f589fa937b82cf11bba28ac8c5c",
          "logical_id": "mc-3dc0573e6efa8009574ea78d",
          "row_sha256": "795b3e422f2aa37566df4e8984c749bc23fec03ee38f232d5e7e8c3759c1c6bb"
        }
      ],
      "sha256": "6450a977a696af57ea1bb558cc16542555103cade1912e119e1b6eadc7a2c729",
      "sheet_name": "cards",
      "table_sha256": "987e520242026dfb6e72934e445cb37e5b115279ec40a25ef98312ce95e69b2f",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "93c32ad7b8a26c25f8489bf0c8a7e3bf5720820ed459c346786b4de86908c3b2",
  "sources": [
    {
      "collection": "inference-adaptation-evidence",
      "id": "kv-spec-learning-evidence",
      "path": "计划/八周冲刺进度/历史记录/W1-学习验收记录.md",
      "sha256": "a4afc026cce9e690cd79de0f6782cd908ab8e9534b9a89c37ff32c366978e96d",
      "summary": "已逐项核对从旧验证包迁移的2026-09-09页大小复习片段；仅消费该片段及其vLLM v0.26.0固定源码锚点，不使用待办或其他课程结论。"
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
