---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "84e3cae6f246f74496e004e4fcdc4240720b3a28e0eec8b8aa97d522bac2a0e4",
  "candidate_sha256": "13caee445e0fa60908a7b294665da8a135b325ccdb995e12ad4ac38a52186ed1",
  "cards": [
    {
      "content_sha256": "6cdac87324ffdf61e6d68f073849c4febba8b070d94fcdbcf08cdf6a48874124",
      "content_summary": "A理由：防止以逻辑元素数估算真实显存，遗漏布局、padding 或同时存活缓冲导致 OOM。",
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
      "content_sha256": "b9ba6633f31c8f203bde910d7329957317f7f4d5bde1250b03520b9666f7abbb",
      "content_summary": "B理由：区分合法 view 与需要物化的重排，为显存分析提供前置概念，不将基础 API 定义一律列为 A。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "578c7edd3971a806b66ceb17634483d578c60c1fb520d2a75d899014e5dd1b6d",
      "content_summary": "A理由：支持逐段对齐容量估算，避免将整张量对齐错误套用于每个内层段的真实分配。",
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
      "content_summary": "A理由：解释短内层维如何累计 padding 并触发显存膨胀，支持布局优化的因果分析。",
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
      "content_sha256": "37134d63d086415911b2d98fe7a973ab84fd1fe47ae4a0eafea42ae60bd7b393",
      "content_summary": "A理由：防止输入与权重展平映射不一致造成静默数值错误，并能解释有效元素配对依据。",
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
      "content_summary": "A理由：防止把各自接近参考误推为新旧实现彼此满足同一容差，避免错误验收数值结果。",
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
      "content_summary": "B理由：掌握容差组合与参考幅值的关系，辅助正确性核对；不把公式定义本身列为最高优先级。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2be66d7480f02634efba8fbe929ffb87770e4eb5c8d23487623229e34d3e7564",
      "content_summary": "A理由：防止把跨样本均值误报成重复稳定性或每请求上界，维护性能结论的有效范围。",
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
      "content_summary": "A理由：防止对没有首 Token 的 OOM 用例伪造 TTFT 加速比或借用其他工作负载的基线。",
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
      "content_summary": "A理由：回答负载分流为何不能解决全局过载，避免把无界 waiting 队列误称端到端反压。",
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
      "content_summary": "B理由：区分入口拒绝与上游减速的配合条件，作为完整反压设计的补充辨析。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "case-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "878c5999f11aa081e37d70bda32da51688afbd1fc0556fd5c5575edbdccde82a",
      "content_summary": "A理由：防止队列限额下的立即重试风暴，明确客户端必须消费反馈并降低提交速率。",
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
    },
    {
      "content_sha256": "98e68837bda44c9799ba6b2ee753d2997840ef73d1b16341d46fdfd4bd27986a",
      "content_summary": "A理由：防止把 padding 猜想直接当成 OOM 根因，支撑用可区分证据选择实际需要优化的分配阶段。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-memory-diagnosis",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用分阶段显存观测与对象生命周期区分输入重排输出和workspace分配"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7d10e772fcdcb48a17378d5f",
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
  "managed_body_sha256": "53ba9d2053a1f6a1d39035c631d2e6385b0e9cb93f88b717264c4df1c12ef975",
  "manifest_payload_sha256": "c44b1b2484f8c47e537dec466ad99dbc998d92faf4d1048c99878dd33c795b7b",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 13215,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/conv3d-evidence-backpressure-technical-qa.xlsx",
      "row_count": 13,
      "rows": [
        {
          "content_sha256": "6cdac87324ffdf61e6d68f073849c4febba8b070d94fcdbcf08cdf6a48874124",
          "logical_id": "mc-31f34dc0ef5606ecabd0d4f5",
          "row_sha256": "e05b25391655bb0a3bb77178d2df7f2ba73172f77fc463217f8df31f2f638fce"
        },
        {
          "content_sha256": "b9ba6633f31c8f203bde910d7329957317f7f4d5bde1250b03520b9666f7abbb",
          "logical_id": "mc-e1599ccdbe7715208e0cace9",
          "row_sha256": "52f00d478c8e10e5909f751f503e5922b918576835109601d6fa419b94e22b87"
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
          "content_sha256": "37134d63d086415911b2d98fe7a973ab84fd1fe47ae4a0eafea42ae60bd7b393",
          "logical_id": "mc-5cdc4ea3b6cbae16877d2911",
          "row_sha256": "afa73a46e5ce195a51c5b9a72624a2805b44d8955849ebc71a706efead33a181"
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
        },
        {
          "content_sha256": "98e68837bda44c9799ba6b2ee753d2997840ef73d1b16341d46fdfd4bd27986a",
          "logical_id": "mc-7d10e772fcdcb48a17378d5f",
          "row_sha256": "598015dc22ae0761bc9001ed6bd2452e52326345e3321a3b9b5678ad21ef2843"
        }
      ],
      "sha256": "4162ef17376d0bd64dd451802c5e441defd266b04edb8d37eb37f32655de24eb",
      "sheet_name": "cards",
      "table_sha256": "713997ce47d567cec393928f47c3455f70b8806fc0418e7a090f18c646382ddf",
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

导入文件：[conv3d-evidence-backpressure-technical-qa.xlsx](conv3d-evidence-backpressure-technical-qa.xlsx)（13 张卡）
