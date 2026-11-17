---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "4e1e3442603eb95011085d106d4f0bbe227ebfacc800b5462245f0e80439c2ac",
  "candidate_sha256": "1109d4efba06aa826558598d2262cf38e5e64ed617938ded0285a0a98443d260",
  "cards": [
    {
      "content_sha256": "6fba62c5bd23eb7a827aba92e3941ff6597528b84d86b7951c7417b6d6eac859",
      "content_summary": "A理由：防止把候选排序首位当成最终可用实现，正确诊断后端能力与配置筛选。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-attention-selection",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分自动后端的候选优先顺序与最终有效选择"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-bf4f0830353ce8175f192f8c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e0cfe8f2eeff5483d9401d25a9eca9788a4854a9a36e6a845d6f47216ccac5ed",
      "content_summary": "A理由：防止对显式指定的无效后端误期待静默 fallback，定位选择阶段的实际报错路径。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-attention-selection",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分自动后端筛选与显式指定无效后端时的处理"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3122aaa3b9ce689446c681bc",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1a68cc0707ad4c800a23b464ec59ddb93f3d29fa06f5af6430919f219ddd3822",
      "content_summary": "A理由：防止以配置或选择函数成功宣称 Runner／kernel 已运行，限定设备能力与验收证据。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "runtime-evidence",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分实现选择函数成功与所选实现实际执行的证据"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-02e87b1438f73bdf09911e42",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c147b5c7b8030e4fccc6952a86d491b1b9bc963f312f66f0d228829b8b82e2d5",
      "content_summary": "B理由：区分插件工厂的类对象入口与继承约束，属于可迁移的 Python 接口基础。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "python-type-introspection",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分类对象检查与继承关系检查"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e83bfcf671f541a964dfb8b6",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "98dba6b327621f787529be554da4dae976a36ee6c78a9b624416013044c12368",
      "content_summary": "B理由：区分每次交付列表与输入批次／调用次数；保留真实概念纠错，但不把一次 0、1、0 计数列为最高优先级。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-output-processing",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "按每次调用的交付列表统计final_only输出数量"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-77f3807adca2e196e9b5fbc2",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "305bdcb4865ea8bd965205690a05cdbd451c3f74367ed0967cf93fb452c99d09",
      "content_summary": "B理由：校准文本 stop 的截断边界；保留真实预测差值，不以记忆具体示例字符串作为高优先级目标。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-output-processing",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "确定排除stop字符串时的最终文本截断位置"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9e867890b277accc6e8fb96f",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8bca1ac7961e2569fb3c0212c7f40d1c439b11618b88f31ec6dec106234011ee",
      "content_summary": "A理由：防止把前端状态清理错误依赖于 Core 取消完成，避免迟到输出再次交付或重复取消。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-output-processing",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释前端判停清理不等待core取消及迟到输出被忽略的原因"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-2a2f36ee5131912373479c1a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3e1427144308e27335cfe51e3be6f8a4971507a7ec80337238f1fc9e53774adf",
      "content_summary": "2026-11-03本地归档：题面已明确参数从case贯通，判断几乎直接可得，重复复习价值不足；保留既有身份与真实错误用于追溯，不再导出。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "test-design",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "在驱动已传递用例字段时通过修改输入切换测试条件"
      },
      "layer": "atomic",
      "lifecycle": "archived",
      "logical_id": "mc-544204f363ea08959c4dcb30",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "55c582ddbfa23fecf9d96feb8ae53d6e0c3cfa4ea155c8774bfd1a84f244569a",
  "manifest_payload_sha256": "9422ec9cbcb68405f0cde5451de636f17c622b92276e3a58c14b0fe3f4aad81b",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5685,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w1-p1-runtime-output-practice-correction.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "98dba6b327621f787529be554da4dae976a36ee6c78a9b624416013044c12368",
          "logical_id": "mc-77f3807adca2e196e9b5fbc2",
          "row_sha256": "c2283db4a33aee05d798efd6163cb0794e406050605cc0c510fddc007f521d9b"
        },
        {
          "content_sha256": "305bdcb4865ea8bd965205690a05cdbd451c3f74367ed0967cf93fb452c99d09",
          "logical_id": "mc-9e867890b277accc6e8fb96f",
          "row_sha256": "5dd7af4418e0d3c63222f95e105d5993bac80870807759844fce0eddcec830e9"
        },
        {
          "content_sha256": "8bca1ac7961e2569fb3c0212c7f40d1c439b11618b88f31ec6dec106234011ee",
          "logical_id": "mc-2a2f36ee5131912373479c1a",
          "row_sha256": "69a63f9f395f4f3c15a390aa63942c1dc43c1af3a4baf74101baa53fb519138d"
        }
      ],
      "sha256": "66627063a0fad9344757b7e63cc77fad7020b3ebefb0b38dab066a0178bf0707",
      "sheet_name": "cards",
      "table_sha256": "3658883dcb3ff063b9351fdb0ad54fd24bf038e61708fbbf999e93967e261a7c",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 5762,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w1-p1-runtime-output-practice-technical-qa.xlsx",
      "row_count": 4,
      "rows": [
        {
          "content_sha256": "6fba62c5bd23eb7a827aba92e3941ff6597528b84d86b7951c7417b6d6eac859",
          "logical_id": "mc-bf4f0830353ce8175f192f8c",
          "row_sha256": "81090df9c0c3d0ec4828a51aaac64d8e15d9b872def7cd4678ac6f12dc381fd8"
        },
        {
          "content_sha256": "e0cfe8f2eeff5483d9401d25a9eca9788a4854a9a36e6a845d6f47216ccac5ed",
          "logical_id": "mc-3122aaa3b9ce689446c681bc",
          "row_sha256": "828f8dee8ba435c1f92709208ab485be35acc3fe2c0fe16c1deb97198f5d0867"
        },
        {
          "content_sha256": "1a68cc0707ad4c800a23b464ec59ddb93f3d29fa06f5af6430919f219ddd3822",
          "logical_id": "mc-02e87b1438f73bdf09911e42",
          "row_sha256": "cc9af00adf5805b4659484e7696d5f80f5515020c41b34ede5ea7ee05e99dadc"
        },
        {
          "content_sha256": "c147b5c7b8030e4fccc6952a86d491b1b9bc963f312f66f0d228829b8b82e2d5",
          "logical_id": "mc-e83bfcf671f541a964dfb8b6",
          "row_sha256": "9a2c080df7c8e636c59f8b2f7b28a44ab364bd355641d75a2b08ae03539dfadd"
        }
      ],
      "sha256": "e58100836c5c99517a701f156707a3e99a506549446c124729d51fff962a5199",
      "sheet_name": "cards",
      "table_sha256": "cfa21afad97056745a23e0debdd97642820148aff67675e1efd60dfe578a1650",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "df3d870b4c8d4e41598f4399bc8fa282a318215f3afd59b05e013276a8c077f4",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "p1-structured-log",
      "path": "推理框架/log/2026-09-18-w1-p1-runtime-output-practice.md",
      "sha256": "e8050f7bf17e5198c7539b3da18786b5e5262fcdc36366e10d952fa86fb832fa",
      "summary": "W1-P1 已核验学习过程；仅采用稳定要点与真实纠错，不读取 raw 为卡片来源。"
    }
  ],
  "target_collection": "inference-cards",
  "template_registry_sha256": "358d0b6e1ee30ee06c0ae9636266ddafad6f2e81494f6d8975d68448e190996c",
  "template_registry_version": "1.1.0"
}
---
# Markji 表格导入卡片

> Markdown 保留受管元数据与模板定义；卡片数据请使用下列按模板拆分的 XLSX 文件导入。

## 真实错误纠错卡

模板 `correction@1.1.0`：

```text
[P#H1#{{意图}}]
📍 [T#!939393#{{场景}}]
---
✅ [T#B,!36b59d#{{正确}}]
❌ [T#!c6413a#{{错误}}]
{{说明}}
```

导入文件：[w1-p1-runtime-output-practice-correction.xlsx](w1-p1-runtime-output-practice-correction.xlsx)（3 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[w1-p1-runtime-output-practice-technical-qa.xlsx](w1-p1-runtime-output-practice-technical-qa.xlsx)（4 张卡）
