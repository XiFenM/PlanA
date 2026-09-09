---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "5f70cf75acf8f8001bc486752416703d2f3a75b928a55871fbdd6dcb0f80a2da",
  "candidate_sha256": "8d5ce58e7ee48dd792219aa25a686ae539a6628f360ff92e4a77a84e9c0cae94",
  "cards": [
    {
      "content_sha256": "704ca3e3439e9d644298ccf86c4a711e9973d7d0325884f840b0c8865952f551",
      "content_summary": "区分 v1 executor 的执行拓扑职责与 model_executor 的模型计算职责",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-runtime-architecture",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分执行拓扑层与模型计算实现层的职责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-96e1b69dea2352f136f7bf25",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bba7ec6b06a8e0a0951ca91dae4bee7b4343bb5e757a72f9d919acf829f9536d",
      "content_summary": "拆开同名 core 文件与目录所代表的总协调组件和调度资源模块",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-runtime-architecture",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分 enginecore 总协调组件与 v1 core 调度资源模块"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-80af1f420bd379f601b14f22",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "518d0e08ebb4d66a99144e6c9e37a6f587b49339a6b25d1276a3e7de4b234142",
      "content_summary": "把仓库分区映射为问题的第一定位区域，并区分目录地图与真实调用链",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-source-navigation",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "按源码问题类型选择 vllm 仓库的第一定位区域"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-83e65d952696673938e97510",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "13e861c35d2ec9bf7bc951806e4b6aaa0d51257e4621d3e80b242468c875e422",
      "content_summary": "把进程放置、调用边界与张量并行的模型语义分成正交维度",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-process-topology",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分 uni 或 mp 进程放置与张量并行模型分片语义"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f302cc845ea60e085cced69b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d093ced77aaa45596930365cf9ce5440a8ed49fc8514f27a62fb64c7a1bd5248",
      "content_summary": "说明在线前端与 EngineCore 的进程隔离价值，并限定 uni 的含义",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-process-topology",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释在线前端与 enginecore 进程隔离的目的和 uni 边界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3c230b513e2bfac0bc2a6179",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ee98df83e32a6c7618051ef995de3ae69d7871806172f181b5987d2dfdeae013",
      "content_summary": "建立 internal DP 的多 EngineCore、独立状态和前端选路模型",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-data-parallel-runtime",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释 internal dp 由多个独立 enginecore 构成的运行拓扑"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0231ee421ef176e4361b8092",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "63670e3c8ccf74354cb7ef4f32c932b4a79945e494497ee085bc23e8c8f5eafa",
      "content_summary": "解释 DPLB 的加权队列打分、乐观 waiting 更新、同分轮转及其观测盲区",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-data-parallel-runtime",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释 dplb 新请求负载打分、乐观计数与同分轮转的边界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e7291be4ff573e99f0b21531",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ed0ab969b8ea94280b463614e301fe91f7805addb856b94b54d236a3faf74f21",
      "content_summary": "从分散在前端、调度器和设备执行层的状态解释 live migration 边界",
      "dependency_content_sha256": {
        "mc-0231ee421ef176e4361b8092": "ee98df83e32a6c7618051ef995de3ae69d7871806172f181b5987d2dfdeae013",
        "mc-6ecc1a209cfc46dfdedd5775": "b14d9f89b6751d144a44ff1b5f8d06cf9bf018883090705dd8ed4d9d3af8d7f9",
        "mc-e7291be4ff573e99f0b21531": "63670e3c8ccf74354cb7ef4f32c932b4a79945e494497ee085bc23e8c8f5eafa",
        "mc-ff2bbe335a098a1d6b3715af": "c4348fb44a8f28ea9a64d897a35d84fdfbd2d57d4e30ff5b2aa92af7b7f74946"
      },
      "depends_on": [
        "mc-0231ee421ef176e4361b8092",
        "mc-6ecc1a209cfc46dfdedd5775",
        "mc-e7291be4ff573e99f0b21531",
        "mc-ff2bbe335a098a1d6b3715af"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-data-parallel-runtime",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释执行中请求不能仅凭 request id 无损迁移的状态所有权原因"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3c06179493ab5a7e28f8814c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "2026-09-09 按固定 v0.26.0 源码与已修订子卡复核：DP 调度状态独立不等于 MoE 权重完整复制；续跑需要调度、KV、采样与前端路由共同衔接，单独重做 prefill 不足。"
      },
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d1d6f62e9a6b19910c3cb863d1bebbf54568a800926401c21117a04de84d46c1",
      "content_summary": "明确 DPCoordinator 的独立进程位置、对等汇总职责与非所有权边界",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-data-parallel-runtime",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释 internal dp 中 dpcoordinator 的独立进程位置与职责边界"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-04939c201c37cffd8e5c77fc",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c4348fb44a8f28ea9a64d897a35d84fdfbd2d57d4e30ff5b2aa92af7b7f74946",
      "content_summary": "明确 Worker 外层设备生命周期与 ModelRunner 设备内热路径的所有权",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-device-execution",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分 worker 的设备生命周期职责与 modelrunner 的设备内执行职责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-ff2bbe335a098a1d6b3715af",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b14d9f89b6751d144a44ff1b5f8d06cf9bf018883090705dd8ed4d9d3af8d7f9",
      "content_summary": "区分 Scheduler、Worker 和 ModelRunner 对 KV 的逻辑、资源与物理所有权",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-device-execution",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释逻辑 kv、显存预算与物理 kv tensor 的分层所有权"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6ecc1a209cfc46dfdedd5775",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3992f7218c3fbef5e7120e6420884e6de8c63c6f0976917f032ed9fdf13b8dfd",
      "content_summary": "用主线核对、上游意图和最小复现约束从源码观察到 bug 结论的升级",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-source-evidence",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "判断固定源码观察何时足以升级为已确认缺陷结论"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-91cab0d3196c0a4921fc8603",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e87e95b413ad45e221cd1ce50d17756f8ca624b9f37e09440d7811904c60ab68",
      "content_summary": "根据前端、协调子进程、EngineCore 与 Worker 的放置推导 DP 等于 2 的进程数",
      "dependency_content_sha256": {
        "mc-0231ee421ef176e4361b8092": "ee98df83e32a6c7618051ef995de3ae69d7871806172f181b5987d2dfdeae013",
        "mc-04939c201c37cffd8e5c77fc": "d1d6f62e9a6b19910c3cb863d1bebbf54568a800926401c21117a04de84d46c1",
        "mc-f302cc845ea60e085cced69b": "13e861c35d2ec9bf7bc951806e4b6aaa0d51257e4621d3e80b242468c875e422"
      },
      "depends_on": [
        "mc-0231ee421ef176e4361b8092",
        "mc-04939c201c37cffd8e5c77fc",
        "mc-f302cc845ea60e085cced69b"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-process-topology",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "推导单 api、dp 等于 2、tp 等于 1 时 uni 与 mp 的主要进程数"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d5efa0a4591b7b115ec6d666",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "2026-09-09 按固定 v0.26.0 启动与 executor 源码复核：单机在线内部 DP、单 API、DP backend mp、DP=2 且 TP=PP=PCP=1，uni 为4、mp为6个主要进程。"
      },
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6009c25141a8348cb9e6285be85a952639e3ee333b5524906f4fe4857cf01388",
      "content_summary": "拆开 Scheduler 的逻辑计划与 Executor、Worker、ModelRunner 的执行落地",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-runtime-architecture",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分 scheduler 的单次逻辑决策与后续设备执行"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-33d40a2ab95e6129b9c5f4c5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f42da0d597a1a3f5b4c9d2c598e145996fa5538c5128cdfe687478e884573f95",
      "content_summary": "以完整口述串联 V1 四个运行时所有者及其责任边界",
      "dependency_content_sha256": {
        "mc-33d40a2ab95e6129b9c5f4c5": "6009c25141a8348cb9e6285be85a952639e3ee333b5524906f4fe4857cf01388",
        "mc-3c230b513e2bfac0bc2a6179": "d093ced77aaa45596930365cf9ce5440a8ed49fc8514f27a62fb64c7a1bd5248",
        "mc-80af1f420bd379f601b14f22": "bba7ec6b06a8e0a0951ca91dae4bee7b4343bb5e757a72f9d919acf829f9536d",
        "mc-96e1b69dea2352f136f7bf25": "704ca3e3439e9d644298ccf86c4a711e9973d7d0325884f840b0c8865952f551",
        "mc-ff2bbe335a098a1d6b3715af": "c4348fb44a8f28ea9a64d897a35d84fdfbd2d57d4e30ff5b2aa92af7b7f74946"
      },
      "depends_on": [
        "mc-33d40a2ab95e6129b9c5f4c5",
        "mc-3c230b513e2bfac0bc2a6179",
        "mc-80af1f420bd379f601b14f22",
        "mc-96e1b69dea2352f136f7bf25",
        "mc-ff2bbe335a098a1d6b3715af"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "vllm-runtime-architecture",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "口述 engine、core、executor 与 worker 四个运行时所有者的协作边界"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-da4be48b928b158d4537e1bc",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已逐一核对五张前置卡：调度与执行、前端进程、EngineCore/core、executor/model_executor、Worker/Runner；口述顺序和四项评分锚点均受这些子卡支持。"
      },
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "1de59d3fa3611caa064adc7e8ce0e59dec35550930a0324f099bc0b16fb68b82",
  "manifest_payload_sha256": "eb2c6bb33aba46613284f9cf2ea4ca505ab4bf539daa5376c96833b12e22904d",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 14195,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/vllm-repository-and-process-architecture-technical-qa.xlsx",
      "row_count": 14,
      "rows": [
        {
          "content_sha256": "704ca3e3439e9d644298ccf86c4a711e9973d7d0325884f840b0c8865952f551",
          "logical_id": "mc-96e1b69dea2352f136f7bf25",
          "row_sha256": "a59952b739d3b7075224a059a7f9b5ef9e3f32900c91025961382c146a0d1d27"
        },
        {
          "content_sha256": "bba7ec6b06a8e0a0951ca91dae4bee7b4343bb5e757a72f9d919acf829f9536d",
          "logical_id": "mc-80af1f420bd379f601b14f22",
          "row_sha256": "a2c84f47c36c8db890f540a91c10212e49ead840439aafeb1d5315b25bd1d604"
        },
        {
          "content_sha256": "518d0e08ebb4d66a99144e6c9e37a6f587b49339a6b25d1276a3e7de4b234142",
          "logical_id": "mc-83e65d952696673938e97510",
          "row_sha256": "132c4aae7ed80ec0499aaa9e772bccf72b08e43243cbf132a59d234167e8ec40"
        },
        {
          "content_sha256": "13e861c35d2ec9bf7bc951806e4b6aaa0d51257e4621d3e80b242468c875e422",
          "logical_id": "mc-f302cc845ea60e085cced69b",
          "row_sha256": "f1caeb43d2dad134617215c74d16d9a8cb330366e8dc75b9f9c671ec2fb22234"
        },
        {
          "content_sha256": "d093ced77aaa45596930365cf9ce5440a8ed49fc8514f27a62fb64c7a1bd5248",
          "logical_id": "mc-3c230b513e2bfac0bc2a6179",
          "row_sha256": "3dfb4d3b3d5783388ce69339dd6a1b202b9bb2b5985f9b7df5ac18cd1186570f"
        },
        {
          "content_sha256": "ee98df83e32a6c7618051ef995de3ae69d7871806172f181b5987d2dfdeae013",
          "logical_id": "mc-0231ee421ef176e4361b8092",
          "row_sha256": "f27f6a8eb2c31cafb5c9de41b332fa0c7ce03ca094c1734155b460fe98a1fbb7"
        },
        {
          "content_sha256": "63670e3c8ccf74354cb7ef4f32c932b4a79945e494497ee085bc23e8c8f5eafa",
          "logical_id": "mc-e7291be4ff573e99f0b21531",
          "row_sha256": "750597d54df9fc5d90fe8e6e14815182a88d84484407ef0282d3c6742b50475a"
        },
        {
          "content_sha256": "ed0ab969b8ea94280b463614e301fe91f7805addb856b94b54d236a3faf74f21",
          "logical_id": "mc-3c06179493ab5a7e28f8814c",
          "row_sha256": "85e04eedc9af7490d7d771f032348783f890b31ea08d1076f4d3484fabc79c5d"
        },
        {
          "content_sha256": "d1d6f62e9a6b19910c3cb863d1bebbf54568a800926401c21117a04de84d46c1",
          "logical_id": "mc-04939c201c37cffd8e5c77fc",
          "row_sha256": "910581a5ceff5a2f5bafbd9746c4a5d56ea53203a34ef58f0181caf13d55172a"
        },
        {
          "content_sha256": "c4348fb44a8f28ea9a64d897a35d84fdfbd2d57d4e30ff5b2aa92af7b7f74946",
          "logical_id": "mc-ff2bbe335a098a1d6b3715af",
          "row_sha256": "892d13c0cd67ef3bc0872c96297ed53a3ce2f198ebb72587460933f8cacecd07"
        },
        {
          "content_sha256": "b14d9f89b6751d144a44ff1b5f8d06cf9bf018883090705dd8ed4d9d3af8d7f9",
          "logical_id": "mc-6ecc1a209cfc46dfdedd5775",
          "row_sha256": "a41a49dc1bae426100ca8eca714eafb8f734b6989b68e6a70c2917b87dea0222"
        },
        {
          "content_sha256": "3992f7218c3fbef5e7120e6420884e6de8c63c6f0976917f032ed9fdf13b8dfd",
          "logical_id": "mc-91cab0d3196c0a4921fc8603",
          "row_sha256": "5a18a5ba3a24605c0d583bb52abb9f923d8ef44b7ddbb870e9b7d89411f7935d"
        },
        {
          "content_sha256": "e87e95b413ad45e221cd1ce50d17756f8ca624b9f37e09440d7811904c60ab68",
          "logical_id": "mc-d5efa0a4591b7b115ec6d666",
          "row_sha256": "1096e7843d0e2364f392fd77e5604df04412009a83532d3b24304485ee499209"
        },
        {
          "content_sha256": "6009c25141a8348cb9e6285be85a952639e3ee333b5524906f4fe4857cf01388",
          "logical_id": "mc-33d40a2ab95e6129b9c5f4c5",
          "row_sha256": "e4c6dabc2fc685cc5261a9862e8580b2c2cbaafb0dc769920ba7822e2576f097"
        }
      ],
      "sha256": "e24399daa624287f740b5d2bd1513cc084480e1b628bf5dbedbc393bf5f6eded",
      "sheet_name": "cards",
      "table_sha256": "aa37182f70940b2da02fe11b128c651d844ca534c76889c9eeeee1093dc7fc97",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 3591,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/vllm-repository-and-process-architecture-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "f42da0d597a1a3f5b4c9d2c598e145996fa5538c5128cdfe687478e884573f95",
          "logical_id": "mc-da4be48b928b158d4537e1bc",
          "row_sha256": "e4bf54d2e8d85b3a07fb77d2ba6e7d032d1ce0b8b24bec71211c61230da55d18"
        }
      ],
      "sha256": "8048fd26a8d64f4d567cc86e3abcde0510a1056dcc2f8b3ab55eb7b5b57682c7",
      "sheet_name": "cards",
      "table_sha256": "26236fd7dfabfaf79a0a14b972eab4fdc3b76d3572a2a5a3e9283e27024f30ac",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "451dc88a36d2854d2f61a58c181cebcfbb4eb0392601bbf052cf04e6c17ff8a6",
  "sources": [
    {
      "collection": "inference-study-article",
      "id": "vllm-repository-process-article",
      "path": "推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md",
      "sha256": "1fec8d77e12e0f123ee7b65e64fe9013cb7fbd7278906485af984292056310da",
      "summary": "基于固定 vLLM v0.26.0 源码形成的仓库地图、进程拓扑、调度与组件所有权文章"
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

导入文件：[vllm-repository-and-process-architecture-technical-qa.xlsx](vllm-repository-and-process-architecture-technical-qa.xlsx)（14 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[vllm-repository-and-process-architecture-oral.xlsx](vllm-repository-and-process-architecture-oral.xlsx)（1 张卡）
