---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "3e3823c358b16e1cd18b26cf5316dcd89505a7c72e9576b51a60b954b07f076d",
  "candidate_sha256": "bc334ab7884aeeb4bc92fde74c1daf5f1789175cb5b16e11a7ec399c3e4e59b4",
  "cards": [
    {
      "content_sha256": "45f4459e05d90a2c178e440063d73b124f93723a803d56d73ba3d58a63923eb6",
      "content_summary": "A理由：防止把管理权转移误当对象销毁，从而误判借用指针或遗漏真正的悬空访问。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "cpp-object-lifetime",
        "fact_scope": {
          "kind": "snapshot",
          "product": "c++",
          "version": "c++17"
        },
        "recall_target": "判断所有权转移前后裸借用指针的有效性"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-00a22ac9bd6add4cfe86d5f9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9080fbebe3d50a8be7edbc75a0ebb7f0f6b8cdb8764982a8ba74dd8f08738673",
      "content_summary": "A理由：防止混淆受管对象销毁与智能指针变量存续，正确判断 reset 后的资源访问。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "cpp-object-lifetime",
        "fact_scope": {
          "kind": "snapshot",
          "product": "c++",
          "version": "c++17"
        },
        "recall_target": "区分reset释放受管对象与智能指针自身生命周期"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-60bc058e8e597dab074d7e31",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "042e5b3317ffa1749940010e337b6e8e0d003c801ec92cd52a26b05ace8c93b0",
      "content_summary": "A理由：防止将无虚析构的多态删除当作可预测路径，避免依赖未定义行为设计资源清理。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "cpp-polymorphism",
        "fact_scope": {
          "kind": "snapshot",
          "product": "c++",
          "version": "c++17"
        },
        "recall_target": "识别通过非虚析构基类指针删除派生对象的未定义行为"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-bc769d5fdbbe85a9261c800c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1c8818d5d14c64f81d856a983d2b38aac5b1d9a182a1d6f704e5cf441e29bf73",
      "content_summary": "A理由：回答成员调用中静态选择与动态派发如何组合的面试题，避免把虚派发误当重新选择重载。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "cpp-polymorphism",
        "fact_scope": {
          "kind": "snapshot",
          "product": "c++",
          "version": "c++17"
        },
        "recall_target": "按名字查找重载选择虚派发解释成员调用"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4beafacee5f003364dfce11a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ac79f4987d56985a346c518230781b3c35256ea7a94315a0b0f6ad2236a6d0f4",
      "content_summary": "B理由：校准局部名字与静态存储期的区别；基础辨析有迁移价值，但不以记忆 Section 名称作为核心能力。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "cpp-object-lifetime",
        "fact_scope": {
          "kind": "snapshot",
          "product": "c++",
          "version": "c++17"
        },
        "recall_target": "区分局部作用域与静态存储期"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5793ce0b82de3a2d8692c7e5",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ec75d84393041a1e25faa5c367852e47b2a13effce5258b743887559c203b73e",
      "content_summary": "A理由：诊断函数签名不匹配造成的链接错误，避免误以为链接器会重新重载或转换参数。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "cpp-linkage",
        "fact_scope": {
          "kind": "snapshot",
          "product": "c++",
          "version": "c++17"
        },
        "recall_target": "解释链接时不会重新选择函数重载"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4d4a53d74856aafc271a9a7c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ffacf5dc36a155ae5be65bde097fea2088a016a04088cacb5b6eb3274bea2118",
      "content_summary": "B理由：区分 ELF 文件组织与运行时装载视角，为选择 readelf 观察对象提供基础。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "elf-linking-loading",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分elf section与segment的主要职责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-12c0f1db93c5728c1eafbb30",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "36758e7380f4e6ef06902256afd95c7db230724025a377a1550f1711c668ba4a",
      "content_summary": "B理由：理解零初始化存储为何不需要等量文件字节；强化文件与内存口径，而不死记算例数字。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "elf-linking-loading",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "由pt_load的文件大小和内存大小确定零初始化尾部"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c23eba0a38c5732608cac09a",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f26e467d525e7b80ca4c1a01c0e7e45e8f98c7661f9fbbc891935e70abcb1381",
      "content_summary": "A理由：防止把构建期找到库误当部署时必能加载，正确定位运行时库搜索故障。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "linux-dynamic-linking",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分构建期库搜索与运行时库搜索"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-0582bb6fd6e72fd6286d3b33",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "acb2dd09376dfa89cfef6d7daa1b75f61bbe1162267e0ade327daa8350b56cfc",
      "content_summary": "A理由：防止用当前终端 ldd 覆盖故障进程的实际映射证据，避免诊断错库。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "linux-dynamic-linking",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "使用目标进程映射证据判断已加载共享库"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-cb316aa34f2f5aae61bd2c35",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f71e26df3829adbcc91f37f30a0f183ac84ec5fd17b16dab2bf1f02755ce1143",
      "content_summary": "B理由：解释动态符号表中的待解析引用，作为后续符号诊断的基础，而不把定义复述列为最高优先级。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "elf-symbols",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分und符号引用与可用定义"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-59af503a325be96a588ab102",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c5660f3be451f112dde080e70f5c4bfdb43b64261c8a545ee0bb35909ea05cd3",
      "content_summary": "B理由：解释重载隐藏与虚派发交互，补足框架类层次中选择基类实现与保留多态的取舍。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "cpp-polymorphism",
        "fact_scope": {
          "kind": "snapshot",
          "product": "c++",
          "version": "c++17"
        },
        "recall_target": "区分using引入基类重载与显式限定调用对虚派发的影响"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4f3d3937a7808eee78901430",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "6e9191b108c296d19691b2ca0c6c6f1293e9661288c566c128de78f39b2e24e5",
  "manifest_payload_sha256": "3e47a2fa7063904f7cc28390261d14e77455374bf9a8dbac5447ba9198c1afdc",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 12460,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w1-cpp-linux-baseline-technical-qa.xlsx",
      "row_count": 12,
      "rows": [
        {
          "content_sha256": "45f4459e05d90a2c178e440063d73b124f93723a803d56d73ba3d58a63923eb6",
          "logical_id": "mc-00a22ac9bd6add4cfe86d5f9",
          "row_sha256": "b1bec66199e044c46a3c89291a9929bde42336fe1a380042ed237c7d099e8851"
        },
        {
          "content_sha256": "9080fbebe3d50a8be7edbc75a0ebb7f0f6b8cdb8764982a8ba74dd8f08738673",
          "logical_id": "mc-60bc058e8e597dab074d7e31",
          "row_sha256": "70265000f22e66393ffccb6a2f23d4b443f2b3454ca0894ab0600968d6355bc5"
        },
        {
          "content_sha256": "042e5b3317ffa1749940010e337b6e8e0d003c801ec92cd52a26b05ace8c93b0",
          "logical_id": "mc-bc769d5fdbbe85a9261c800c",
          "row_sha256": "52eae4f1e1421d6f1baa69b3f8cd92362eea3e8aa65d09c9f78751e33e52e4e5"
        },
        {
          "content_sha256": "1c8818d5d14c64f81d856a983d2b38aac5b1d9a182a1d6f704e5cf441e29bf73",
          "logical_id": "mc-4beafacee5f003364dfce11a",
          "row_sha256": "91c43852f2c091e13dde49d74df434e4d85c866033265c88ca465ebda38d30f7"
        },
        {
          "content_sha256": "ac79f4987d56985a346c518230781b3c35256ea7a94315a0b0f6ad2236a6d0f4",
          "logical_id": "mc-5793ce0b82de3a2d8692c7e5",
          "row_sha256": "0a38f5e787d9345e51198e45f57187a6be9d55e9822b1acaa48efb1b047c5787"
        },
        {
          "content_sha256": "ec75d84393041a1e25faa5c367852e47b2a13effce5258b743887559c203b73e",
          "logical_id": "mc-4d4a53d74856aafc271a9a7c",
          "row_sha256": "f08a9dd7a7ba22233238fe86960d4a454afea7b6769091815032f3ef8215d756"
        },
        {
          "content_sha256": "ffacf5dc36a155ae5be65bde097fea2088a016a04088cacb5b6eb3274bea2118",
          "logical_id": "mc-12c0f1db93c5728c1eafbb30",
          "row_sha256": "95c89fbfa6a93a79ed29ddc61131ec46c6dd434dda023b7ef2bcfb9c455c9875"
        },
        {
          "content_sha256": "36758e7380f4e6ef06902256afd95c7db230724025a377a1550f1711c668ba4a",
          "logical_id": "mc-c23eba0a38c5732608cac09a",
          "row_sha256": "5f195fb145c1d14fd88f7600ff3493dcc352416f4858f1b4e69cfb898c2dea62"
        },
        {
          "content_sha256": "f26e467d525e7b80ca4c1a01c0e7e45e8f98c7661f9fbbc891935e70abcb1381",
          "logical_id": "mc-0582bb6fd6e72fd6286d3b33",
          "row_sha256": "3de4430dd0db1851e22b609f3e80ebf2fb66426623c95a050ee65f60edfd2d79"
        },
        {
          "content_sha256": "acb2dd09376dfa89cfef6d7daa1b75f61bbe1162267e0ade327daa8350b56cfc",
          "logical_id": "mc-cb316aa34f2f5aae61bd2c35",
          "row_sha256": "ad99a081ac94eff2b2146fb35dba9c0fe4be7dbb90c84be9636d16eef9fed556"
        },
        {
          "content_sha256": "f71e26df3829adbcc91f37f30a0f183ac84ec5fd17b16dab2bf1f02755ce1143",
          "logical_id": "mc-59af503a325be96a588ab102",
          "row_sha256": "6e8e2b0e5d07d030b5a91ccf521bd3632997234fafb6b89818bcddf9b72efafe"
        },
        {
          "content_sha256": "c5660f3be451f112dde080e70f5c4bfdb43b64261c8a545ee0bb35909ea05cd3",
          "logical_id": "mc-4f3d3937a7808eee78901430",
          "row_sha256": "656f26aa0063ac491c0f0ff87822f5addf2644743e2c8d4be8d979e6facabfdb"
        }
      ],
      "sha256": "e276063aa6de4c508266630ae07a2b94299688ca979c82326d9a87932ebd0460",
      "sheet_name": "cards",
      "table_sha256": "e2e418c5a2ab731aadef7d99b9fd36fd96c9b88309f0321aa641d5cb1fc5f4ec",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "166d0bd71d1560c680c55d944ebbcc2eb6dd49c9c035dd9cf08691c9a1ee1624",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "cpp-log",
      "path": "推理框架/log/2026-09-14-cpp-linux-baseline.md",
      "sha256": "3ab696abc80543d3f35196dfd0c1c54722b6c4626200ccf66e9a3ebb29630afe",
      "summary": "C++／Linux 概念、真实纠错与证据边界；未实践内容不制卡。"
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

导入文件：[w1-cpp-linux-baseline-technical-qa.xlsx](w1-cpp-linux-baseline-technical-qa.xlsx)（12 张卡）
