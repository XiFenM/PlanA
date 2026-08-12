---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "candidate_sha256": "54a21fc5fa0882a9f2d6875ada3196a088dafa88e1ab6cdc87554e5f07b60aec",
  "cards": [
    {
      "content_sha256": "7afbb21868a783b39b4ea16a01e2a9e324e3bdc9373145a284760c7f4ccbbc24",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "f918dc35b6131922c265faf1cf1a8d82eca4af8b0a464e712f4415f20451c058",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "a76e3d7b917ba61303aea69df1e25de81f0c44fa9d7acb5fa2ed4f9cd30233f3",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "cd2db4147cc8a7af59193d8ebf11cf2f9738a338cc3c6c156627353481a74bd9",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "8a5eff668193e74d00c102a2e63be739862189d425186da09413eee05196bd51",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "7ee8da35bcf4688d0ef52dd4e2fa1e4039e2557e04142854a0a0aec61dd34db9",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "059069aea7c682fdde27c9170795f38adcd39375bf24aa2c8b73413264a0af0e",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "d3aaf67828b6cef2228b924583587759674c165a1c25c78b939e4842d9065da6",
      "content_summary": "从分散在前端、调度器和设备执行层的状态解释 live migration 边界",
      "dependency_content_sha256": {
        "mc-0231ee421ef176e4361b8092": "7ee8da35bcf4688d0ef52dd4e2fa1e4039e2557e04142854a0a0aec61dd34db9",
        "mc-6ecc1a209cfc46dfdedd5775": "f006b24fdba5f57fed41f05f5c266eae7dfe701188b51bbefa4d29cbf446d22a",
        "mc-e7291be4ff573e99f0b21531": "059069aea7c682fdde27c9170795f38adcd39375bf24aa2c8b73413264a0af0e",
        "mc-ff2bbe335a098a1d6b3715af": "376a4a7fa907686fbc988c5f4b8bb798013576544e50bd262afa710e44eda1ac"
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
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "7bf74979726121f13f4b3db9286d71eb098797d711705922816294363f249e51",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "376a4a7fa907686fbc988c5f4b8bb798013576544e50bd262afa710e44eda1ac",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "f006b24fdba5f57fed41f05f5c266eae7dfe701188b51bbefa4d29cbf446d22a",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "863d1c18c37aa0b514f941093002057afca575cd45a7a9304daf9506a96ac057",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "214330d4e67b901e07894ea2e367583cedd9d16c119baae303103ac53c913e01",
      "content_summary": "以完整口述串联 V1 四个运行时所有者及其责任边界",
      "dependency_content_sha256": {
        "mc-33d40a2ab95e6129b9c5f4c5": "23ba2648dcfafef6816fd98c01d274821371083299d05ff8b2312ea23787f679",
        "mc-3c230b513e2bfac0bc2a6179": "8a5eff668193e74d00c102a2e63be739862189d425186da09413eee05196bd51",
        "mc-80af1f420bd379f601b14f22": "f918dc35b6131922c265faf1cf1a8d82eca4af8b0a464e712f4415f20451c058",
        "mc-96e1b69dea2352f136f7bf25": "7afbb21868a783b39b4ea16a01e2a9e324e3bdc9373145a284760c7f4ccbbc24",
        "mc-ff2bbe335a098a1d6b3715af": "376a4a7fa907686fbc988c5f4b8bb798013576544e50bd262afa710e44eda1ac"
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
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "76fc67b04c83e8b5be4b154946afdd8cc3de0f475aff8099196cd814f1e31bcc",
      "content_summary": "根据前端、协调子进程、EngineCore 与 Worker 的放置推导 DP 等于 2 的进程数",
      "dependency_content_sha256": {
        "mc-0231ee421ef176e4361b8092": "7ee8da35bcf4688d0ef52dd4e2fa1e4039e2557e04142854a0a0aec61dd34db9",
        "mc-04939c201c37cffd8e5c77fc": "7bf74979726121f13f4b3db9286d71eb098797d711705922816294363f249e51",
        "mc-f302cc845ea60e085cced69b": "cd2db4147cc8a7af59193d8ebf11cf2f9738a338cc3c6c156627353481a74bd9"
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
      "source_ids": [
        "vllm-repository-process-article"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "23ba2648dcfafef6816fd98c01d274821371083299d05ff8b2312ea23787f679",
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
      "template_version": "1.0.0"
    }
  ],
  "managed_body_sha256": "539a7e3b4965a601bd3695c4b63343318308b0e40a544812f024dbfa754e33fc",
  "manifest_payload_sha256": "5d3482d19f5797b8d5c5e045642b32f0c68f185b37cad911c9525b2c6d311923",
  "schema": "memo-cards.artifact/v1",
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
  "template_registry_sha256": "d6cdcd90c996ca6922a06f02a44b06800468a557bec6ad5c433511d7b57761d7",
  "template_registry_version": "1.0.0"
}
---
# Markji 表格导入暂存

> 供粘贴进 Markji 下载表格；这不是可直接上传的 TSV 文件。

## 技术问答卡

模板 `technical-qa@1.0.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

```tsv
问题	答案	锚点	来源
vLLM v0.26.0 中 executor 与 model_executor 分别负责什么？	vllm/v1/executor 负责执行拓扑、RPC 和任务下发，隔离 uni、mp 或 Ray 等放置方式；vllm/model_executor 负责模型、层、权重加载、量化和算子，也就是具体执行什么。前者不决定模型计算内容，后者不负责 EngineCore 到 Worker 的放置与调用拓扑。	executor 管怎样发过去；model_executor 管具体算什么	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §1 与面试问题 Q1
vllm/v1/engine/core.py 中的 EngineCore 与 vllm/v1/core 目录有什么区别？	engine/core.py 定义 EngineCore 总协调组件，组织每轮 schedule、execute 和 update；v1/core 目录保存 Scheduler、KV Cache Manager 等调度算法与逻辑资源状态。前者是总协调者，后者是其调度和逻辑资源能力所在。	EngineCore 是总协调者；v1 core 是调度与逻辑资源模块	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §2 与面试问题 Q2
面对一个 vLLM 源码问题，怎样选择第一定位区域，为什么目录地图不能替代调用链？	用户入口和协议先看 entrypoints，请求生命周期与 IPC 看 v1/engine，调度与逻辑 KV 看 v1/core，执行拓扑看 v1/executor，设备运行入口看 v1/worker，模型层与算子看 model_executor，设备插件、通信和高性能 kernel 分别看 platforms 或 plugins、distributed、kernels 或 csrc。目录地图用于缩小搜索范围；真正判断行为仍需从 Python 调用位置沿 backend、wrapper 和 kernel 继续追踪，不能把目录分类当成运行时调用栈。	先按问题类型缩小范围，再沿真实调用链下钻	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §1、源码定位题与知识树
为什么从 uni 切到 mp 不等于从 TP 等于 1 切到 TP 大于 1？	uni 或 mp 决定 Worker 与 EngineCore 是同进程直接调用还是跨进程 IPC；TP 决定模型权重和计算是否跨 rank 分片。TP 等于 1 时显式使用 mp 会改变 Worker 的进程位置、IPC、CUDA context 和资源生命周期归属，但不会因此产生模型分片或跨 rank collective。	uni 或 mp 管放置；TP 管模型分片与 collective	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §3 与面试问题 Q3
常规单卡在线 vLLM 为什么仍会把前端与 EngineCore 放在不同进程？	API Server 和 AsyncLLM 处理 HTTP、tokenization、连接与流式输出，这些工作具有较大抖动；EngineCore 需要稳定执行 schedule、execute、update 热循环。用 IPC 隔离二者可以减少前端抖动对核心循环的干扰。uni 只表示 Worker 与 EngineCore 同进程，不表示整个在线服务单进程。	前端抖动与核心热循环隔离；uni 不是全服务单进程	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §3 与面试问题 Q5
vLLM internal DP 是怎样让一个前端连接多个后端实例的？	它启动多个相互独立的 EngineCore，每个实例拥有自己的 Scheduler、请求队列、逻辑 KV 状态和模型副本，再由 API 进程中的 DPLBAsyncMPClient 为新请求选择目标。它不是把一个 EngineCore 拆成多个进程，也不是让多个 EngineCore 共享同一份调度状态。	一个前端连接多个独立 EngineCore，而非拆分一个 Core	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §4 与面试问题 Q6
vLLM v0.26.0 的 DPLBAsyncMPClient 如何按负载选择 EngineCore，这个启发式有哪些边界？	前端计算 score 等于 4 乘 waiting 加 running，并选择最低分 EngineCore。等待下一次统计快照期间，它会乐观增加已选实例的本地 waiting 计数，并轮转同分时的扫描起点，以减少突发集中和固定顺序偏置。该启发式只看加权请求数量，不直接考虑 token 工作量、GPU 利用率、剩余 KV blocks 或 prefix-cache locality。	加权队列计数加乐观更新和同分轮转；不是完整负载模型	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §4 与面试问题 Q7
为什么执行中的请求不能因为另一个 EngineCore 空闲就直接 live-migrate？	请求开始执行后，EngineCore 和 Scheduler 持有 token 进度、调度状态与逻辑 KV 映射，Worker 和 ModelRunner 持有物理 KV、持久 batch 与采样状态，前端还持有输出 collector、请求路由与 abort 目标。只转发 request id 无法恢复等价的下一步；重新 prefill 属于重算或重启，不是无损 live migration。	调度状态、物理 KV、采样状态和输出路由必须共同迁移或重建	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §4 与面试问题 Q8
internal DP 场景中的 DPCoordinator 位于哪里，负责什么？	它由独立进程承载，不位于 API 进程，也不归属于任一 EngineCore。它是所有 DP ranks 的对等协调和汇总点，聚合各 EngineCore 的 DP 状态与协调信息并反馈给前端；它不选择具体请求，也不持有请求的逻辑或物理 KV。	独立对等汇总进程；不隶属某个 EngineCore，也不持有请求 KV	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §4、§5 与面试问题 Q9
Worker 与 ModelRunner 的职责边界是什么？	Worker 管在哪个设备和 rank、以什么生命周期运行，包括 distributed 环境、显存预算、外围资源控制和面向 Executor 的进程级入口；ModelRunner 管这一轮在设备上怎样运行，包括持久 batch、输入 tensor、物理 KV、attention metadata、图执行、模型调用、采样与设备侧状态。ModelRunner 不只是调用一次 forward。	Worker 管设备与生命周期；ModelRunner 管设备内推理热路径	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §6 与面试问题 Q10
vLLM 中逻辑 KV 与物理 KV Cache 分别由谁拥有？	EngineCore 和 Scheduler 管请求对应的逻辑 KV block 账本与调度状态；Worker 负责设备显存预算、初始化时机和资源生命周期；ModelRunner 实际分配并持有物理 KV tensor，维护 block table 与 slot mapping，并在 attention 执行中使用它们。KV 所有权因此不是单层归属。	Scheduler 管逻辑账本；Worker 管预算生命周期；ModelRunner 管物理 KV 与映射	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §2、§5 与 §6
在固定源码中没有找到 dense internal DP 的实时计数发布链，能否直接判定为 bug？	不能。当前证据只能支持对固定 commit 的源码观察及其限定范围；从未找到某条路径到已确认 bug，还需要核对最新 main、检索 issue 和 PR、确认维护者预期，并构造最小复现或失败测试。应把源码观察、运行行为和缺陷归因分成三个证据层级。	固定源码观察不等于运行复现，更不等于已确认 bug	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §4 固定版本落差与 §实践
忽略 supervisor 与监控进程时，API 等于 1、DP 等于 2、TP 等于 1 的 uni 和 mp 各有多少个主要进程？	uni 有 4 个：1 个 API 前端进程、1 个独立 DPCoordinator 协调进程，以及 2 个各自内嵌 Worker 和 ModelRunner 的 EngineCore 进程。只把 backend 改成 mp 后，每个 EngineCore 再增加 1 个 Worker 子进程，因此共有 6 个；TP 仍为 1，所以这次增加不代表模型分片。	uni 为 1 加 1 加 2 等于 4；mp 再加 2 个 Worker 等于 6	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §5
为什么逻辑 KV 资源调度到模型运行调度不是两个前后相接的 Scheduler？	Scheduler 在同一次决策中选择请求与本轮 token 数、分配或复用逻辑 KV blocks，并产出 SchedulerOutput。Executor、Worker 和 ModelRunner 随后把这个既定计划下发并转成物理 KV 映射、batch、tensor 与模型执行，它们不再重新决定本轮运行哪些请求。	一次 Scheduler 决策产出 SchedulerOutput；后续是执行落地而非二次调度	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §2
```

## 综合口述卡

模板 `oral@1.0.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

```tsv
问题	参考回答	评分锚点	来源
请用 45 到 90 秒说明 vLLM V1 中 engine、core、executor、worker 四个 owner 如何协作，并指出各自不负责什么。	API Server 和 AsyncLLM 处理请求输入输出，并通过 IPC 连接 EngineCore；EngineCore 组织 schedule、execute、update，借助 Scheduler 和 core 状态管理队列、token 预算与逻辑 KV；executor 按 uni、mp 或 Ray 等拓扑下发既定计划，不重新调度请求；Worker 管设备、rank、资源生命周期与执行入口，ModelRunner 在其内部落实 batch、物理 KV、模型执行和采样。	API Server 与 AsyncLLM 负责请求输入输出，并通过 IPC 连接 EngineCore；EngineCore 组织 schedule、execute、update，Scheduler 与 core 状态管理队列和逻辑 KV；executor 只隔离执行拓扑并下发既定计划；Worker 管设备与资源生命周期，ModelRunner 管设备内 batch、物理 KV、执行和采样	推理框架/深入学习理解vLLM/1-Repository-and-Process-Architecture.md §2
```
