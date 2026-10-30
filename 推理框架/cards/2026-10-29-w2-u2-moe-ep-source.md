---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "263868e8ae2ba22d3de4c3965c6974181b3ff2ccc22ab78a38e06e2dfa4eef4f",
  "candidate_sha256": "f07131ba2bb43eebb265fea75c47d13d08b2b02347cd4a7c39661ae9ea71a8d0",
  "cards": [
    {
      "content_sha256": "11f8fc9a25812c98ec824afc5042184a3bee15ad6f5ba983e80179f49d1bcd0b",
      "content_summary": "输入倾斜与路由倾斜的诊断；日志 msg-b5465a61f417efa7f284 至 msg-e4082364be91580724fe；A理由：防止把输入负载不均误诊为通信后端问题，导致选错优化层。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-communication",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分输入倾斜与路由倾斜对全量汇聚和定向通信热点的影响"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0ed50a88db9ac96840141528",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9d162456f5080f75a396017b7374f7b9a8d31a532a842007addc39897e660d2a",
      "content_summary": "收到的行数与有效专家任务分离；日志 msg-8e6587f51eeaf023328f 至 msg-39258735807febc64986",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-communication",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分通信接收行数与逻辑专家任务数的变化"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-56b599c1069c19ef0ddc6ef7",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c66b5ade570685dde7e25c7eaa1b3f562331924bc633a768ff3996c59e9912b3",
      "content_summary": "由格式相容转向完整接口适配；日志 msg-cd242279ff3dbbe261e0 至 msg-e11af1bd6506dfdf24de",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-backend-adaptation",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "沿调用和双向数据转换检查新通信与专家计算库接入"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4746777d4ed0903d46fc6ef1",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "86cbdbb905cad598ae621c6c7e11e76634956d1b1769873cf6e067ca3dc9af43",
      "content_summary": "区分独立数据与独立路由状态；日志 msg-3c29e30f014f680127da 至 msg-01cf4c895e5c9d2863c1",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-state-ownership",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分专家计算路由与返回原token的逆向路由状态"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-8bfa17595cb98670cd20c6bf",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "669498f8622fd1128f57c76b38740a517772c5818545f17f1d25af5707f4e03f",
      "content_summary": "容量、流量与延迟不能互相直接代替；日志 msg-213da940761ce5e646da 至 msg-1c493574a996a1f9eca1",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "communication-memory",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分预分配容量上限和本次有效通信载荷"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-05666abf8041226167e2d565",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ebe5d362ba562e1bc72ca9456776f6b09ab0add244d497e2da11981f62ab7c41",
      "content_summary": "分段隔离与共享池复用的取舍；日志 msg-399b4eca85d61636702d 至 msg-39b7a8578708aa702d95",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "communication-buffer-allocation",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "比较发送方固定分段与共享接收池的空间利用和协调代价"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-244543b92a4e79a7a9d3d8c0",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "88f57b18878b856993785d4922f951ed5f2616de6bac7cb870d33ba5f75405b0",
      "content_summary": "CPU 精确分配的前置依赖；日志 msg-00f78fbfaac95c3d4afc 至 msg-e11af1bd6506dfdf24de",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "device-host-dependencies",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释设备端小元数据进入主机精确分配时的同步依赖"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-227c85ef5fbbfd21a1eb9fbb",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "86ae33cba88cbda3aec8eb76aee788b3aa43cd6b0abf6f586672abf7eb3c0011",
      "content_summary": "存储寿命与执行顺序分离；日志 msg-00f78fbfaac95c3d4afc 至 msg-e11af1bd6506dfdf24de；A理由：防止把对象存活误当成并发读写安全，造成难复现的数据污染。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "async-memory-safety",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分存储生命周期保护与异步读写的执行依赖"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c0a6bbabec1878d631276cdb",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a731f1f409f5be29b0d370599a011293ef8c6543aadc592bb78fb77289e24ab9",
      "content_summary": "双缓冲的复用判据；日志 msg-aedd4102796e1b87223a 至 msg-db2722a1efa647880e95；A理由：防止把双缓冲误用成自动管理空闲槽的队列，覆盖仍在使用的数据或信号。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "async-communication-protocols",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "根据完成依赖而非槽位轮换判断双缓冲安全复用"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-62d5f03146b33e44f5f1fd5c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "00bc2bc781b0ec121868ac6fc06c80e677f6f8ead26d21b3fc4d551af7e42961",
      "content_summary": "图捕获地址与资源代次的边界；日志 msg-0b11a3f01d08750d1938 至 msg-04357ec5c2c2e17e7571；A理由：防止扩容后继续重放旧地址，引入越界、旧数据或悬空访问。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "execution-graph-lifetimes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释固定地址执行图在缓冲区扩容后的有效性责任"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e5a5695b3491317cdb16a670",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a5b10a95fc4f13272eec65ad236ca6324e584e895e9cefa88f8786183ea26e84",
      "content_summary": "小批量的固定开销占比；日志 msg-9329c4b20defdb06330a 至 msg-4be32abee930fcef52d1",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "communication-performance-models",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释小批量下通信字节缩小与端到端延迟不成比例"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3081bf56f50be64e703a3e6d",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "03c010299cb71902991e29c68309f9580fce35002216fcd380c488a228a37071",
      "content_summary": "超时与取消／复用边界；日志 msg-99ff094769014856582f 至 msg-eb00d3c44be4fb8d8a0e；A理由：防止通信超时后在未隔离旧操作时重试，破坏缓冲区与跨 rank 状态。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "distributed-failure-semantics",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分异步通信超时检测与资源可安全重用的证明"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4b35d3fa343cc7fef863995b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "73e940b5d14d64aff32ef2a22010cdf058ec5d2b813a6778c5919931594ff220",
      "content_summary": "溢出标志与逐分配有效性；日志 msg-d762ecbfb4d55cff810b 至 msg-015b0394ddbba83d8977",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-capacity-semantics",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分溢出标志专家分段与有效贡献映射的职责"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-07a8956677d3ff9aeaece8b2",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1b8c56373eb440534aed78996514a491400ea26a3f8df79758913b3fc09454a2",
      "content_summary": "串联同批已核验子卡，不引入实现结果；日志异步与图重放相关条目；A理由：直接支撑一道关于异步通信适配正确性的系统面试题。",
      "dependency_content_sha256": {
        "mc-62d5f03146b33e44f5f1fd5c": "a731f1f409f5be29b0d370599a011293ef8c6543aadc592bb78fb77289e24ab9",
        "mc-8bfa17595cb98670cd20c6bf": "86cbdbb905cad598ae621c6c7e11e76634956d1b1769873cf6e067ca3dc9af43",
        "mc-c0a6bbabec1878d631276cdb": "86ae33cba88cbda3aec8eb76aee788b3aa43cd6b0abf6f586672abf7eb3c0011",
        "mc-e5a5695b3491317cdb16a670": "00bc2bc781b0ec121868ac6fc06c80e677f6f8ead26d21b3fc4d551af7e42961"
      },
      "depends_on": [
        "mc-62d5f03146b33e44f5f1fd5c",
        "mc-8bfa17595cb98670cd20c6bf",
        "mc-c0a6bbabec1878d631276cdb",
        "mc-e5a5695b3491317cdb16a670"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "moe-adaptation-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "向面试官串联异步moe的数据路由状态与缓冲复用责任"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-debb09f1299fe28fc7773875",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "78f0ce1819f5c09657607115f5f5b74fc259d9399a7dffd92ad301eb8d5181fd",
      "content_summary": "容量参数与实际计数分离；日志 msg-572418169362c2f6c4d0 至 msg-0240f26975e51eee1550",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "jit-runtime-boundaries",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分容量特化参数与运行时有效计数的变化"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e342f4616fd0e374130f8eae",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "705329b0bb6b09b7c0a1ef8bcf3f8541be48c15f931f1ebb7f7323fb42909259",
      "content_summary": "图内错误标志与图后处理；日志 msg-7364d634a002abb3179a 至 msg-ab2e9b1835238bcd5dc9",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "execution-graph-failure-handling",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释执行图内标错与图后拒绝结果的边界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c29b701b7aaba17a07471d8a",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ff6b546fdd0c8f2d26faf98ff9f87556b8c12e123a0de6890174a08ab43df6b5",
      "content_summary": "通信资源预算与重叠机会；日志 msg-0307955549c557089157 至 msg-98a2af8a3ef74f623c34",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-overlap-performance",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "按可重叠工作判断通信资源预算的优化价值"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-157cfe1fef7b451ade6352ea",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u2-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "6875e844f7cf8bf43b88dd5773680f0d1ff7ff5eecd2e76f2657d4f8c992e5e4",
  "manifest_payload_sha256": "dfa25c1b9eb7ae5d56b6de797c453b6c28fa80d4f7717f73f0d3062cbff4a0ba",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 6561,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/2026-10-29-w2-u2-moe-ep-source-correction.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "11f8fc9a25812c98ec824afc5042184a3bee15ad6f5ba983e80179f49d1bcd0b",
          "logical_id": "mc-0ed50a88db9ac96840141528",
          "row_sha256": "3f5a2bb97dcc749ca322d69f34f924a40e8e37654a349b68e75fe56f2a7cb7ed"
        },
        {
          "content_sha256": "9d162456f5080f75a396017b7374f7b9a8d31a532a842007addc39897e660d2a",
          "logical_id": "mc-56b599c1069c19ef0ddc6ef7",
          "row_sha256": "81facd830a548a56c882b12aa9a8994394f62e5288cd6f8fefffcf37889de44a"
        },
        {
          "content_sha256": "669498f8622fd1128f57c76b38740a517772c5818545f17f1d25af5707f4e03f",
          "logical_id": "mc-05666abf8041226167e2d565",
          "row_sha256": "b2da6ade39792003cbc1b00550db4221e5bc7a1514a1d892bd1b382bf907a83b"
        }
      ],
      "sha256": "e99813f2e190f22c2e72bfc89fc682047216cf556573c9a4f6bceb42520a55c7",
      "sheet_name": "cards",
      "table_sha256": "3f20a4befebb35f3afb2fd53d0c2d901f5968280b700f9df56991a077134214c",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 17305,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/2026-10-29-w2-u2-moe-ep-source-technical-qa.xlsx",
      "row_count": 13,
      "rows": [
        {
          "content_sha256": "c66b5ade570685dde7e25c7eaa1b3f562331924bc633a768ff3996c59e9912b3",
          "logical_id": "mc-4746777d4ed0903d46fc6ef1",
          "row_sha256": "1fc1b35b330c4f231c65ed529fd8219b2889f841f57c42e76aa220766e5ebcd3"
        },
        {
          "content_sha256": "86cbdbb905cad598ae621c6c7e11e76634956d1b1769873cf6e067ca3dc9af43",
          "logical_id": "mc-8bfa17595cb98670cd20c6bf",
          "row_sha256": "3ef9d0aa3b9cd09712844543cc6def7cd34d111fbc302d363bcdf8110d5281bf"
        },
        {
          "content_sha256": "ebe5d362ba562e1bc72ca9456776f6b09ab0add244d497e2da11981f62ab7c41",
          "logical_id": "mc-244543b92a4e79a7a9d3d8c0",
          "row_sha256": "b01f5dace38e5fbe41cf479c8883c02d30f6a168ddd8439c9a6ba14083820c88"
        },
        {
          "content_sha256": "88f57b18878b856993785d4922f951ed5f2616de6bac7cb870d33ba5f75405b0",
          "logical_id": "mc-227c85ef5fbbfd21a1eb9fbb",
          "row_sha256": "c8f7d28d039d6260f2cc6420167f4016c3cc04e83cae38341d5f5b04746d3ba2"
        },
        {
          "content_sha256": "86ae33cba88cbda3aec8eb76aee788b3aa43cd6b0abf6f586672abf7eb3c0011",
          "logical_id": "mc-c0a6bbabec1878d631276cdb",
          "row_sha256": "ee0d5fbfb49259502d8f6a12eb6ff81f2efc1adb4afaf7462d7cbb114337b6b6"
        },
        {
          "content_sha256": "a731f1f409f5be29b0d370599a011293ef8c6543aadc592bb78fb77289e24ab9",
          "logical_id": "mc-62d5f03146b33e44f5f1fd5c",
          "row_sha256": "eb6ded915713319062c4b5dc0be90d40b21d43e2e740147515edf8959582008c"
        },
        {
          "content_sha256": "00bc2bc781b0ec121868ac6fc06c80e677f6f8ead26d21b3fc4d551af7e42961",
          "logical_id": "mc-e5a5695b3491317cdb16a670",
          "row_sha256": "a47303e742c653be444722930b9f72c051791eb1108d6690e6fffa2e382d8971"
        },
        {
          "content_sha256": "a5b10a95fc4f13272eec65ad236ca6324e584e895e9cefa88f8786183ea26e84",
          "logical_id": "mc-3081bf56f50be64e703a3e6d",
          "row_sha256": "05fa029538ea67f2338e49540b4120f936aae359034e5402ea7f40c137f2dcd2"
        },
        {
          "content_sha256": "03c010299cb71902991e29c68309f9580fce35002216fcd380c488a228a37071",
          "logical_id": "mc-4b35d3fa343cc7fef863995b",
          "row_sha256": "2011f16a8941d60111da3ab1459b0c2afdfe0e8cfe50eecf4b209aa88992bcd4"
        },
        {
          "content_sha256": "73e940b5d14d64aff32ef2a22010cdf058ec5d2b813a6778c5919931594ff220",
          "logical_id": "mc-07a8956677d3ff9aeaece8b2",
          "row_sha256": "ebcef1dadae3c48bd9e5b5ea2d4f60dc8e19a333a93527bb1e9d314bb484460b"
        },
        {
          "content_sha256": "78f0ce1819f5c09657607115f5f5b74fc259d9399a7dffd92ad301eb8d5181fd",
          "logical_id": "mc-e342f4616fd0e374130f8eae",
          "row_sha256": "9ca122296ae03ee591e4c9e2fd0f079320677025c98f9b80f2fb1ec40fa3c606"
        },
        {
          "content_sha256": "705329b0bb6b09b7c0a1ef8bcf3f8541be48c15f931f1ebb7f7323fb42909259",
          "logical_id": "mc-c29b701b7aaba17a07471d8a",
          "row_sha256": "7a477b99fd8e9a316f57b5da47e251c6b51433823b3b1985076cb2413e1fbf2c"
        },
        {
          "content_sha256": "ff6b546fdd0c8f2d26faf98ff9f87556b8c12e123a0de6890174a08ab43df6b5",
          "logical_id": "mc-157cfe1fef7b451ade6352ea",
          "row_sha256": "76e4751224622b7fecfdb5d02c4d34da9ded64430b2d5ac98134d61624e8b146"
        }
      ],
      "sha256": "5990f8f0f4e2701c038ba6eea4b293649ec3cb7237302d1f35b5b25908f829a6",
      "sheet_name": "cards",
      "table_sha256": "5b4a5bdbcb890dd9b39f4a05d1e97374147a784ac125a37654eb94d8750fd4ae",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4227,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/2026-10-29-w2-u2-moe-ep-source-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "1b8c56373eb440534aed78996514a491400ea26a3f8df79758913b3fc09454a2",
          "logical_id": "mc-debb09f1299fe28fc7773875",
          "row_sha256": "fcd8193aa3afc10736e3b090f816089640f24be2ac33b108ef53e453c773cc13"
        }
      ],
      "sha256": "826dba2f2565a5102ce422bff8049c2e907e25bc2691277a920fde2b90aca7c2",
      "sheet_name": "cards",
      "table_sha256": "15cf8f9a26c439057988dd7b7fb1380c96f3226e2073762526abc024a26b4388",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "3411de8ce7e4f5163e01860f26daaf0afb24492d780acb776e3164abb8b22611",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "w2-u2-log",
      "path": "推理框架/log/2026-10-29-w2-u2-moe-ep-source.md",
      "sha256": "1fdb5dd6149d08b8c2f233ac08abf9ff79949dbe36fe504156f4cc6a00c801fc",
      "summary": "用户明确指定的 W2 单元二结构化学习日志；取已核验的稳定机制与真实纠错，未使用 raw、遗留或未验证芯片实现作为事实。"
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

导入文件：[2026-10-29-w2-u2-moe-ep-source-correction.xlsx](2026-10-29-w2-u2-moe-ep-source-correction.xlsx)（3 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[2026-10-29-w2-u2-moe-ep-source-technical-qa.xlsx](2026-10-29-w2-u2-moe-ep-source-technical-qa.xlsx)（13 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[2026-10-29-w2-u2-moe-ep-source-oral.xlsx](2026-10-29-w2-u2-moe-ep-source-oral.xlsx)（1 张卡）
