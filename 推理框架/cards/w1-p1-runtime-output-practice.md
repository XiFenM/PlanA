---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "f1cb705d8667f689cd25cd7f2cc9564cb87367f176d66ace74b3734bb24885d3",
  "candidate_sha256": "8afb21c00a57e310735b4d88225a6eb9faad13a7b1e5021a6db5fe48df0e9666",
  "cards": [
    {
      "content_sha256": "e90af0701e1dd6eb66f3d18f067ac8de7d16912eac1d17a2a9d1285656969cc9",
      "content_summary": "区分自动后端的候选优先顺序与最终有效选择",
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
      "content_sha256": "2cae98e603220d5af3f5852b52f109e34c4232fd5e27d62eced110d094a91254",
      "content_summary": "区分自动后端筛选与显式指定无效后端时的处理",
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
      "content_sha256": "1409ca669b31a4c3cf7fa2564c65e0d46c73d96dadcf1eb9496c0c02bbc1215b",
      "content_summary": "区分实现选择函数成功与所选实现实际执行的证据",
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
      "content_summary": "区分类对象检查与继承关系检查",
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
      "content_sha256": "6940c35ea89fd863020dec064a8ac2d58e7f639f4f5a1ac16265214c8c9d55c0",
      "content_summary": "按每次调用的交付列表统计FINAL_ONLY输出数量",
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
      "content_sha256": "6650279da73ae0cc7d2b10fe5839c0f062c2dc1c5c94c57ec8b3920b38c81936",
      "content_summary": "确定排除stop字符串时的最终文本截断位置",
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
      "content_sha256": "2675687351adc3bae39454bccf8c53d8d0e59ee3b0c2444af37809cab909cb74",
      "content_summary": "解释前端判停清理不等待Core取消及迟到输出被忽略的原因",
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
      "content_sha256": "beb389722dee20f1fba4d9a0cdfa252d34f743fa0a7f7c782f14bd2b910bca62",
      "content_summary": "在驱动已传递用例字段时通过修改输入切换测试条件",
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
      "lifecycle": "active",
      "logical_id": "mc-544204f363ea08959c4dcb30",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "p1-structured-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "ee147509ea4bac24702c4b77507e22d5e24e7dc9cc592fc698498a3247f77bf8",
  "manifest_payload_sha256": "cff3cee7320a9c434487d9c758f18ab22f5d71f895315c208c6c37ee9b0bcfba",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 6511,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w1-p1-runtime-output-practice-correction.xlsx",
      "row_count": 4,
      "rows": [
        {
          "content_sha256": "6940c35ea89fd863020dec064a8ac2d58e7f639f4f5a1ac16265214c8c9d55c0",
          "logical_id": "mc-77f3807adca2e196e9b5fbc2",
          "row_sha256": "d0e554bb9d025fc83f498c177703cd9b14db07a38ca03325cbfa193c0e1af1a6"
        },
        {
          "content_sha256": "6650279da73ae0cc7d2b10fe5839c0f062c2dc1c5c94c57ec8b3920b38c81936",
          "logical_id": "mc-9e867890b277accc6e8fb96f",
          "row_sha256": "231ea47ea7d16e87853a6e4cffa30c6427da2a943ae6a9260470bfa0769e581d"
        },
        {
          "content_sha256": "2675687351adc3bae39454bccf8c53d8d0e59ee3b0c2444af37809cab909cb74",
          "logical_id": "mc-2a2f36ee5131912373479c1a",
          "row_sha256": "50806b5e59c3093451c8eaaec9153eeb00c1306efd1f4cc663fb802b8d3330cd"
        },
        {
          "content_sha256": "beb389722dee20f1fba4d9a0cdfa252d34f743fa0a7f7c782f14bd2b910bca62",
          "logical_id": "mc-544204f363ea08959c4dcb30",
          "row_sha256": "c240fad8eff30d4c3221b839d084cf119a2b4d178f7486f0a7bd2d8d3d6bf6c5"
        }
      ],
      "sha256": "4038328cc699813d6c76bc7d86dc2c9fa17ea4d3fa373f12762ae39baf707317",
      "sheet_name": "cards",
      "table_sha256": "43104c13b17cd87c8cf227e6d59d6ec1a1e024dcde2236693fb8dd198d760a6d",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 5448,
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
          "content_sha256": "e90af0701e1dd6eb66f3d18f067ac8de7d16912eac1d17a2a9d1285656969cc9",
          "logical_id": "mc-bf4f0830353ce8175f192f8c",
          "row_sha256": "2ff766e3f7d79c4eac213c890fcd0f3ad454b912a93cd9afd8d5f08992e60c5f"
        },
        {
          "content_sha256": "2cae98e603220d5af3f5852b52f109e34c4232fd5e27d62eced110d094a91254",
          "logical_id": "mc-3122aaa3b9ce689446c681bc",
          "row_sha256": "c36d5f027d79f21584be65b1d30eddb19bf3ff67b3dd5bb304755a1ac68dff6a"
        },
        {
          "content_sha256": "1409ca669b31a4c3cf7fa2564c65e0d46c73d96dadcf1eb9496c0c02bbc1215b",
          "logical_id": "mc-02e87b1438f73bdf09911e42",
          "row_sha256": "7a3bcb4f7b80397ddb7dc9fb126f936c431b50ba777be1a42c5ebd036399ff9e"
        },
        {
          "content_sha256": "c147b5c7b8030e4fccc6952a86d491b1b9bc963f312f66f0d228829b8b82e2d5",
          "logical_id": "mc-e83bfcf671f541a964dfb8b6",
          "row_sha256": "9a2c080df7c8e636c59f8b2f7b28a44ab364bd355641d75a2b08ae03539dfadd"
        }
      ],
      "sha256": "988827ec31ba46d6b771e7bb7f7f2ae9fff908a156ff371fba5b2a992d285987",
      "sheet_name": "cards",
      "table_sha256": "69db18e2bb6f378312347fce6291f902dba2efd18a579706d2eaaea45ee2fb93",
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

导入文件：[w1-p1-runtime-output-practice-correction.xlsx](w1-p1-runtime-output-practice-correction.xlsx)（4 张卡）

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
