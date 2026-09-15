---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "14b736f1de09d58ca2e95b1288c6e697f4e9fcb2818c4eec04d7043a2217710b",
  "candidate_sha256": "86a12dd94d165825b79fa85194c49ae5697a3c16c3fcfe3166ffdb0bafd0863d",
  "cards": [
    {
      "content_sha256": "6cdac87324ffdf61e6d68f073849c4febba8b070d94fcdbcf08cdf6a48874124",
      "content_summary": "区分逻辑shape与物理布局和分配容量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "tensor-layout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分逻辑shape与物理布局和分配容量"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-31f34dc0ef5606ecabd0d4f5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8e99bc3ec70789a229ced2c15cd827892a9a590fba7c3d6669d131a440de6806",
      "content_summary": "解释合法view共享存储以及stride兼容要求",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "pytorch-tensor-views",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch",
          "version": "2.11"
        },
        "recall_target": "解释合法view共享存储以及stride兼容要求"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e1599ccdbe7715208e0cace9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "578c7edd3971a806b66ceb17634483d578c60c1fb520d2a75d899014e5dd1b6d",
      "content_summary": "计算逐内层数据段对齐的物理容量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "tensor-layout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "计算逐内层数据段对齐的物理容量"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-bfe23c17ccfe6211a097fc0b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8844e0bc83f804976d8cbc5dd3ca478e45aa94e08aa20ebb6c68c164ac0c7335",
      "content_summary": "解释短内层维逐段对齐导致的存储膨胀",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "tensor-layout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释短内层维逐段对齐导致的存储膨胀"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-8b8d6b8a6651114c7a176861",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e9a79df7051d719857fac89e297b1d5cebb588611afa5b0b6d65b204db381a39",
      "content_summary": "保持输入与权重共同展平时的元素配对",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "tensor-indexing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "保持输入与权重共同展平时的元素配对"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5cdc4ea3b6cbae16877d2911",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "20cfaecb337b29df2a8e01557be3c457b7658817bebf68c755cfa49a1ff02c6c",
      "content_summary": "以同一参考验证多个实现并限定等价结论",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "operator-correctness-testing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "以同一参考验证多个实现并限定等价结论"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-38cf43cc32de055505f36689",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "34af2b2d2f09c82b08012273b8138de2063cf06b854af8b8e1b1c962e5a37be5",
      "content_summary": "解释相对与绝对容差组合的逐元素判据",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "numerical-validation",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释相对与绝对容差组合的逐元素判据"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-2250a5c1dd8bc69f5a45085d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2be66d7480f02634efba8fbe929ffb87770e4eb5c8d23487623229e34d3e7564",
      "content_summary": "区分跨样本均值与单次观测的证据范围",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "benchmark-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分跨样本均值与单次观测的证据范围"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-84318e41c7c01c5c63d55459",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2e48e8027b26820a2ad063ab8ac8bdb5e8bedc9a25da8a25ca62cda599c14708",
      "content_summary": "界定OOM且无首token时不存在有限TTFT基线",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "benchmark-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "界定oom且无首token时不存在有限ttft基线"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-92d258768937c2b86cf295b4",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "43543364342e7af191db07a2e615a2f92722951981492e6ad7310f3e5c1b781c",
      "content_summary": "区分负载分流与端到端反压",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "serving-flow-control",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分负载分流与端到端反压"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-2740a1ec9b2d0f55348e1bea",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cf25650a1ab455db967e24e45c79352b10628ed058a4ba0397e1a2b2a4956652",
      "content_summary": "区分背压反馈与入口过载拒绝",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "serving-flow-control",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分背压反馈与入口过载拒绝"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5dd39e4c218941d48acac5cc",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "878c5999f11aa081e37d70bda32da51688afbd1fc0556fd5c5575edbdccde82a",
      "content_summary": "解释立即重试造成的前端压力及客户端反馈责任",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "serving-flow-control",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释立即重试造成的前端压力及客户端反馈责任"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-799f6796742c3dd3e2eabc24",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "d1629befa62b3da107af834dbd6949735cec866409702c0b0f89cab4ff634da1",
  "manifest_payload_sha256": "bf2a4110c734ff99edf3099bf9783b45851464c97d99f83d573a326325ca242a",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 11148,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/conv3d-evidence-backpressure-technical-qa.xlsx",
      "row_count": 12,
      "rows": [
        {
          "content_sha256": "6cdac87324ffdf61e6d68f073849c4febba8b070d94fcdbcf08cdf6a48874124",
          "logical_id": "mc-31f34dc0ef5606ecabd0d4f5",
          "row_sha256": "e05b25391655bb0a3bb77178d2df7f2ba73172f77fc463217f8df31f2f638fce"
        },
        {
          "content_sha256": "8e99bc3ec70789a229ced2c15cd827892a9a590fba7c3d6669d131a440de6806",
          "logical_id": "mc-e1599ccdbe7715208e0cace9",
          "row_sha256": "c82ed8c43056b7ec514706fa4dd7621ca26e92dd8af0224c09fb37a1a47bfecb"
        },
        {
          "content_sha256": "578c7edd3971a806b66ceb17634483d578c60c1fb520d2a75d899014e5dd1b6d",
          "logical_id": "mc-bfe23c17ccfe6211a097fc0b",
          "row_sha256": "7ccb4a15d672492ed48cb07f1b8a70a83698752200674c76cffacf3dca803f80"
        },
        {
          "content_sha256": "8844e0bc83f804976d8cbc5dd3ca478e45aa94e08aa20ebb6c68c164ac0c7335",
          "logical_id": "mc-8b8d6b8a6651114c7a176861",
          "row_sha256": "a7543d858f1285b496a0169b6f6eceaac6f4d79b08e7d02f92196ccf96487dfa"
        },
        {
          "content_sha256": "e9a79df7051d719857fac89e297b1d5cebb588611afa5b0b6d65b204db381a39",
          "logical_id": "mc-5cdc4ea3b6cbae16877d2911",
          "row_sha256": "fc7007ae79765c707e22e05bec7717a17feea933d5adf5951affc8433e84c5bd"
        },
        {
          "content_sha256": "20cfaecb337b29df2a8e01557be3c457b7658817bebf68c755cfa49a1ff02c6c",
          "logical_id": "mc-38cf43cc32de055505f36689",
          "row_sha256": "464c442481d70b0311dc807e62de4f4560d05f64415087a473ecda085e6002c3"
        },
        {
          "content_sha256": "34af2b2d2f09c82b08012273b8138de2063cf06b854af8b8e1b1c962e5a37be5",
          "logical_id": "mc-2250a5c1dd8bc69f5a45085d",
          "row_sha256": "46d6fa7c34737c2d47100d96b49c2080c1aec45b516943d72360d9336e8567d4"
        },
        {
          "content_sha256": "2be66d7480f02634efba8fbe929ffb87770e4eb5c8d23487623229e34d3e7564",
          "logical_id": "mc-84318e41c7c01c5c63d55459",
          "row_sha256": "7b5720f677c642b36718b67eff371e173b8ac6f67a6a06a9d46d6f58747c9736"
        },
        {
          "content_sha256": "2e48e8027b26820a2ad063ab8ac8bdb5e8bedc9a25da8a25ca62cda599c14708",
          "logical_id": "mc-92d258768937c2b86cf295b4",
          "row_sha256": "392e1da54befa0539beb32c5b19e9a20adbb8eb4ffc064e66666e739db6cf286"
        },
        {
          "content_sha256": "43543364342e7af191db07a2e615a2f92722951981492e6ad7310f3e5c1b781c",
          "logical_id": "mc-2740a1ec9b2d0f55348e1bea",
          "row_sha256": "a7350d5540d4ca3379fd126a1275a9517ebecf0ca651e5a35fe7545f313e12b4"
        },
        {
          "content_sha256": "cf25650a1ab455db967e24e45c79352b10628ed058a4ba0397e1a2b2a4956652",
          "logical_id": "mc-5dd39e4c218941d48acac5cc",
          "row_sha256": "44e7906873e35fdd5787d2a7c5586ed9237abf148225d6e0337f533204f0cc38"
        },
        {
          "content_sha256": "878c5999f11aa081e37d70bda32da51688afbd1fc0556fd5c5575edbdccde82a",
          "logical_id": "mc-799f6796742c3dd3e2eabc24",
          "row_sha256": "23cc5128e37f004c08dbbeb9459b5fae2c270acec7dcd12e83cf0e07cac5bf7d"
        }
      ],
      "sha256": "fb3f70d040c69c3c60bb593a878107a60528a317cdbfb003ffd988aa916708c4",
      "sheet_name": "cards",
      "table_sha256": "77ba3477d093dfe1ea734af8cf5d6416424f6a47fa61e0401e221438d42ac70f",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "c7a2333a1951893f6ee11eeb7397ad7fb7f7f36e0c27b441c094662f8f12c51e",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "case-log",
      "path": "推理框架/log/2026-09-15-conv3d-claim-backpressure.md",
      "sha256": "aea089067369aa07fd985fd4634fe47b1ae279ebdea00201c6b219e6ca5aa9d6",
      "summary": "Conv3D 通用布局、正确性与性能证据、反压边界；私有参数与待核内容不制卡。"
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

导入文件：[conv3d-evidence-backpressure-technical-qa.xlsx](conv3d-evidence-backpressure-technical-qa.xlsx)（12 张卡）
