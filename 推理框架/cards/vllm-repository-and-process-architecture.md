---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "0a072791ad1e1fecf831c47d183015cf30847d3e910e3b804bd506613558a798",
  "candidate_sha256": "57b3eb1795b378fb9142152e11500f43e5b43bfc47c9f839696a4f809960c120",
  "cards": [
    {
      "content_sha256": "272c69d72e00ab121a6bed609c3b5be66cca31707eaa71cbe48991bfdd07e76e",
      "content_summary": "B理由：目录职责辨析可帮助缩小源码定位范围，但无需按高优先级背诵目录名称。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f1e46fd6f432a2342fb2ed88411494079203928fd6fbb41905bb5aa897637011",
      "content_summary": "B理由：区分同名目录与组件，减少源码定位绕路，属于辅助性知识。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d9f48e0699c3d309ef86affb6f3b7f3794e07252e910a914db56c07dc5c5b7fa",
      "content_summary": "B理由：保留可迁移的职责定位方法，不要求逐个背诵完整目录表。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4fac2a1620599ea2f262f032940156749eb9642bd40cbecb31eb6496642813f3",
      "content_summary": "A理由：防止把新增Worker进程误认为模型已做TP分片，影响拓扑与资源判断。",
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
      "content_sha256": "55938ae05c5075e28c9dee66bfb43ac6bc728b6bb5d0f6e7232b81bc5aa93258",
      "content_summary": "A理由：回答服务为何隔离前端与核心循环的架构取舍题，并防止误解uni的进程范围。",
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
      "content_sha256": "741dba1dc0eca30dbfcd0d384868b5bde2c9bb757989d310557c1112b32914e1",
      "content_summary": "A理由：回答内部DP如何分流和隔离请求状态的系统设计题。",
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
      "content_sha256": "497ad8e82f58520bddae2dc452d8d45f242284d61b69d991e1cd392b9f832056",
      "content_summary": "B理由：理解固定实现的选路启发式与局限，具体权重属于低频版本细节。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e83353a043ad309934afcc7caa3b30478a922351a8baa10e490615a699cf33c7",
      "content_summary": "A理由：防止只迁移ID或重做prefill便声称实现等价请求迁移，遗漏采样与输出状态。",
      "dependency_content_sha256": {
        "mc-0231ee421ef176e4361b8092": "741dba1dc0eca30dbfcd0d384868b5bde2c9bb757989d310557c1112b32914e1",
        "mc-6ecc1a209cfc46dfdedd5775": "1ab47cf369be27adf32c4947379f647abd1345b07e5c9aa7a3b31c14144cf08e",
        "mc-e7291be4ff573e99f0b21531": "497ad8e82f58520bddae2dc452d8d45f242284d61b69d991e1cd392b9f832056",
        "mc-ff2bbe335a098a1d6b3715af": "0f30ba6847d526cf21bda4e5a3ee42f0fb105892682ba20fc9f1b6e98b5b56b8"
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
        "summary": "2026-11-07已对照修订后的 DPLB 子卡及固定版本源码复核：本地负载估计在每次自动选定实例后、发送前更新，仅澄清新请求选路的常规记账行为；执行中请求迁移仍须衔接调度进度、物理 KV 与采样状态、输出和取消路由，原题答保持成立。"
      },
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dd93fea58617bb1cb24e478adf3ec09900b1728fb8ead61dd1b6b97fe331b4a8",
      "content_summary": "B理由：校准协调进程与请求选路的职责，不把拓扑位置记忆作为核心能力。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0f30ba6847d526cf21bda4e5a3ee42f0fb105892682ba20fc9f1b6e98b5b56b8",
      "content_summary": "A理由：回答Worker与Runner的职责设计题，防止设备初始化与每步执行逻辑混放。",
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
      "content_sha256": "1ab47cf369be27adf32c4947379f647abd1345b07e5c9aa7a3b31c14144cf08e",
      "content_summary": "A理由：防止把逻辑KV账本与物理显存所有权混为一体，导致适配修改层级错误。",
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
      "content_sha256": "29358b095e117649f3097766717c38800c5c5f2613b1159b1e55e12c7f3a07b5",
      "content_summary": "A理由：防止把未找到源码路径直接宣称为已确认bug，影响技术结论可信度。",
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
      "content_sha256": "71e3597fae13245bbf1a950918e84e0881ada36d76f890e15f388a3dd4e3d9a6",
      "content_summary": "B理由：通过放置关系推导进程组成，练习拓扑理解而非死记4和6。",
      "dependency_content_sha256": {
        "mc-0231ee421ef176e4361b8092": "741dba1dc0eca30dbfcd0d384868b5bde2c9bb757989d310557c1112b32914e1",
        "mc-04939c201c37cffd8e5c77fc": "dd93fea58617bb1cb24e478adf3ec09900b1728fb8ead61dd1b6b97fe331b4a8",
        "mc-f302cc845ea60e085cced69b": "4fac2a1620599ea2f262f032940156749eb9642bd40cbecb31eb6496642813f3"
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
      "priority": 3,
      "quality": "B",
      "review_resolution": {
        "summary": "2026-11-03已按同请求的uni/mp、内部DP及DPCoordinator子卡复核：在题设单机、单API、DP backend mp、DP=2且TP=PP=PCP=1下，由组件放置推导uni为4、mp为6个主要进程；不把增加进程当作模型分片。"
      },
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1e9b7257284f5f0e300ee4dae1360bbab13f23a910de580c2bb0159c38ed4538",
      "content_summary": "A理由：防止误以为执行层再次调度请求，明确一次决策与执行落实的边界。",
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
      "content_sha256": "41616150145ea413332c491cae9d1860b1a3d256cad8429819ef29f2a76133e1",
      "content_summary": "B理由：组合既有子卡形成可自评的架构口述，不引入新的实现结论。",
      "dependency_content_sha256": {
        "mc-33d40a2ab95e6129b9c5f4c5": "1e9b7257284f5f0e300ee4dae1360bbab13f23a910de580c2bb0159c38ed4538",
        "mc-3c230b513e2bfac0bc2a6179": "55938ae05c5075e28c9dee66bfb43ac6bc728b6bb5d0f6e7232b81bc5aa93258",
        "mc-80af1f420bd379f601b14f22": "f1e46fd6f432a2342fb2ed88411494079203928fd6fbb41905bb5aa897637011",
        "mc-96e1b69dea2352f136f7bf25": "272c69d72e00ab121a6bed609c3b5be66cca31707eaa71cbe48991bfdd07e76e",
        "mc-ff2bbe335a098a1d6b3715af": "0f30ba6847d526cf21bda4e5a3ee42f0fb105892682ba20fc9f1b6e98b5b56b8"
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
      "priority": 3,
      "quality": "B",
      "review_resolution": {
        "summary": "2026-11-03已逐项对照五张修订子卡，核对前端隔离、EngineCore/Scheduler决策、Executor下发和Worker/Runner执行；参考回答及四项评分锚点都有同请求active子卡支持，版本一致，未增加未核验事实。"
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
  "manifest_payload_sha256": "ff02ad69ae4e43d076192f2b9c6b986d857d2c72d8b7e2c06aebd0ca2f49f06c",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 16514,
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
          "content_sha256": "272c69d72e00ab121a6bed609c3b5be66cca31707eaa71cbe48991bfdd07e76e",
          "logical_id": "mc-96e1b69dea2352f136f7bf25",
          "row_sha256": "5696dcb355fae7a22d6c2bd7f1bd91932534ce1e3a654d42771e488ecb54e5d4"
        },
        {
          "content_sha256": "f1e46fd6f432a2342fb2ed88411494079203928fd6fbb41905bb5aa897637011",
          "logical_id": "mc-80af1f420bd379f601b14f22",
          "row_sha256": "bdbe4c5f3780ec1462bb33f2346daac5be82ae308a996c9fa6178f7949483ac0"
        },
        {
          "content_sha256": "d9f48e0699c3d309ef86affb6f3b7f3794e07252e910a914db56c07dc5c5b7fa",
          "logical_id": "mc-83e65d952696673938e97510",
          "row_sha256": "efac7ee0dcfb4e7c74fe4fbc093bcc7bcb533baf67661d512ecfff2f8d37fb3a"
        },
        {
          "content_sha256": "4fac2a1620599ea2f262f032940156749eb9642bd40cbecb31eb6496642813f3",
          "logical_id": "mc-f302cc845ea60e085cced69b",
          "row_sha256": "feff8cee26752d43447a07aee80ddd62a488ecdd6cd8f66f074dd1e3036625cc"
        },
        {
          "content_sha256": "55938ae05c5075e28c9dee66bfb43ac6bc728b6bb5d0f6e7232b81bc5aa93258",
          "logical_id": "mc-3c230b513e2bfac0bc2a6179",
          "row_sha256": "774be7c2d10892384f09d6a82d782a6e7993973d1c8577dd4c57c767bc9c66c1"
        },
        {
          "content_sha256": "741dba1dc0eca30dbfcd0d384868b5bde2c9bb757989d310557c1112b32914e1",
          "logical_id": "mc-0231ee421ef176e4361b8092",
          "row_sha256": "7d0491b2cfa3a937c75e55c98d7e69a8b6ef9a80c7612e26589fd905180265ea"
        },
        {
          "content_sha256": "497ad8e82f58520bddae2dc452d8d45f242284d61b69d991e1cd392b9f832056",
          "logical_id": "mc-e7291be4ff573e99f0b21531",
          "row_sha256": "78cf0bda688082b6408c2a5aec9883fb6a592c91d3975fea4ac849612cce6f16"
        },
        {
          "content_sha256": "e83353a043ad309934afcc7caa3b30478a922351a8baa10e490615a699cf33c7",
          "logical_id": "mc-3c06179493ab5a7e28f8814c",
          "row_sha256": "1137eb73bc22d2b39e1a0b106ed9920b49c821103cd05f9492171e3d5d4cafe0"
        },
        {
          "content_sha256": "dd93fea58617bb1cb24e478adf3ec09900b1728fb8ead61dd1b6b97fe331b4a8",
          "logical_id": "mc-04939c201c37cffd8e5c77fc",
          "row_sha256": "a4b65db2e239872b5896f8eea3e505aa98b27723d07afc4d7b2cd872868aeb82"
        },
        {
          "content_sha256": "0f30ba6847d526cf21bda4e5a3ee42f0fb105892682ba20fc9f1b6e98b5b56b8",
          "logical_id": "mc-ff2bbe335a098a1d6b3715af",
          "row_sha256": "82fa4d57b2b50af0f6d05d438fe0db5ecb94dd958c5696e9dbfd4296c0f78a34"
        },
        {
          "content_sha256": "1ab47cf369be27adf32c4947379f647abd1345b07e5c9aa7a3b31c14144cf08e",
          "logical_id": "mc-6ecc1a209cfc46dfdedd5775",
          "row_sha256": "f9b78e5db332cccff35ccfe4baf2fb039c8bb9a95a831f9e7d6e50284d706862"
        },
        {
          "content_sha256": "29358b095e117649f3097766717c38800c5c5f2613b1159b1e55e12c7f3a07b5",
          "logical_id": "mc-91cab0d3196c0a4921fc8603",
          "row_sha256": "70acddbf523482328d277be9119d670d80b8f539962fb5db4f248fa0eb64b5e4"
        },
        {
          "content_sha256": "71e3597fae13245bbf1a950918e84e0881ada36d76f890e15f388a3dd4e3d9a6",
          "logical_id": "mc-d5efa0a4591b7b115ec6d666",
          "row_sha256": "2313f10c7d66d5f0b611da5188610986542bf29c43b04d0683b03c23dd185909"
        },
        {
          "content_sha256": "1e9b7257284f5f0e300ee4dae1360bbab13f23a910de580c2bb0159c38ed4538",
          "logical_id": "mc-33d40a2ab95e6129b9c5f4c5",
          "row_sha256": "4f10f83a2e65ff4c28b2ef9ef10ed3496fbcd14b72330ebad1c62aa3c1dc6632"
        }
      ],
      "sha256": "5ecf4a01ed621ba916ea675f6c19a5e20053bddbbe3065606c7e815b090c51ca",
      "sheet_name": "cards",
      "table_sha256": "d23468523c88a0312c306de55277251814d07e0d25e3a3957ce4d034c0400c15",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 3832,
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
          "content_sha256": "41616150145ea413332c491cae9d1860b1a3d256cad8429819ef29f2a76133e1",
          "logical_id": "mc-da4be48b928b158d4537e1bc",
          "row_sha256": "d60e30ba9ef6ef2a8f1560d2b7cf4f6c1bcf1bcccdb7aa74644b744955c7ebd8"
        }
      ],
      "sha256": "9e403508010f01ff4bbcf85e0429b8092d14a713e96b3cd0bcb4327f783a4b29",
      "sheet_name": "cards",
      "table_sha256": "4a3533e09f924061c1c5f6df00368a6c5e3fd8e89088006fd41453c6dd45c7bf",
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
