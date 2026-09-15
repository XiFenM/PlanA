---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "1071982e21d250c9cc7d2dca7124c63b95a58437a92705d9eab5651c6c2d9367",
  "candidate_sha256": "111a449e540b81036ba1fe47c17002acfe7c6ad3c51382773f37e576cf91eb7a",
  "cards": [
    {
      "content_sha256": "d4264ba5f6052122f47f90f8dc5753e40b42485134e5fbb838456c46685abf02",
      "content_summary": "判断所有权转移前后裸借用指针的有效性",
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
      "content_sha256": "05705b1e137e9cf2e5a2d65ff518b80f8ec37bacc36109610d771486108c9f54",
      "content_summary": "区分reset释放受管对象与智能指针自身生命周期",
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
      "content_summary": "识别通过非虚析构基类指针删除派生对象的未定义行为",
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
      "content_summary": "按名字查找重载选择虚派发解释成员调用",
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
      "content_summary": "区分局部作用域与静态存储期",
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
      "content_sha256": "ec75d84393041a1e25faa5c367852e47b2a13effce5258b743887559c203b73e",
      "content_summary": "解释链接时不会重新选择函数重载",
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
      "content_summary": "区分ELF section与segment的主要职责",
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
      "content_sha256": "9a8c57ba3db59a57c90e43a420f5b0f9b55569d872f020562798f17f952b4de8",
      "content_summary": "由PT_LOAD的文件大小和内存大小确定零初始化尾部",
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
      "content_sha256": "21a85afe47e69a775542917cfa9d52e63b61c30b6f12ba83e11d9ab63d5c2fc6",
      "content_summary": "区分构建期库搜索与运行时库搜索",
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
      "content_sha256": "980530bf71ff34959ee3ed701064267b284a46862264c6c3dc7c76ed02f5e9a2",
      "content_summary": "使用目标进程映射证据判断已加载共享库",
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
      "content_summary": "区分UND符号引用与可用定义",
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
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "cpp-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "bc60573491bf4c6b62c57f0c0e03e674b7bb0b5c6873957d4d0fbd9ea900d0c4",
  "manifest_payload_sha256": "da498123c35628adb4d61643de58d288b4c1e53d2cf4736b836d2b60ae55a382",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 10562,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w1-cpp-linux-baseline-technical-qa.xlsx",
      "row_count": 11,
      "rows": [
        {
          "content_sha256": "d4264ba5f6052122f47f90f8dc5753e40b42485134e5fbb838456c46685abf02",
          "logical_id": "mc-00a22ac9bd6add4cfe86d5f9",
          "row_sha256": "ef8b72d4020840466e0c83f22c6a4760957641603f79c735d384b67a5606b597"
        },
        {
          "content_sha256": "05705b1e137e9cf2e5a2d65ff518b80f8ec37bacc36109610d771486108c9f54",
          "logical_id": "mc-60bc058e8e597dab074d7e31",
          "row_sha256": "884a9286ecec75a41209b71cdb48eeaf49e88fe999cb9972c24b46a6d1373703"
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
          "content_sha256": "9a8c57ba3db59a57c90e43a420f5b0f9b55569d872f020562798f17f952b4de8",
          "logical_id": "mc-c23eba0a38c5732608cac09a",
          "row_sha256": "a300b66f11f4d78eba68c5518336d73a2d32707d4ed0e046c9f0579cd3e1ddbd"
        },
        {
          "content_sha256": "21a85afe47e69a775542917cfa9d52e63b61c30b6f12ba83e11d9ab63d5c2fc6",
          "logical_id": "mc-0582bb6fd6e72fd6286d3b33",
          "row_sha256": "7cd12e7c141407f666ba5951633f4be1be22ef101c8028b022e051d0796d2266"
        },
        {
          "content_sha256": "980530bf71ff34959ee3ed701064267b284a46862264c6c3dc7c76ed02f5e9a2",
          "logical_id": "mc-cb316aa34f2f5aae61bd2c35",
          "row_sha256": "32e117414f95a6a07e990dc0a313e849dcadca894268189b22e820b1442943c6"
        },
        {
          "content_sha256": "f71e26df3829adbcc91f37f30a0f183ac84ec5fd17b16dab2bf1f02755ce1143",
          "logical_id": "mc-59af503a325be96a588ab102",
          "row_sha256": "6e8e2b0e5d07d030b5a91ccf521bd3632997234fafb6b89818bcddf9b72efafe"
        }
      ],
      "sha256": "ca204046572fa9e13f37f471ea1fb2d0034304f09b283828cf704ac28adc0ada",
      "sheet_name": "cards",
      "table_sha256": "ade35b3948650c54dee07f7082f612193af16f7b50fa64b515dd37e8e7e20e1f",
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

导入文件：[w1-cpp-linux-baseline-technical-qa.xlsx](w1-cpp-linux-baseline-technical-qa.xlsx)（11 张卡）
