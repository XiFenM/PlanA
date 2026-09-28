---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "460029e639e11e0347e65859cee2a62001377f256f9c7e4c8719a6427b031fd9",
  "candidate_sha256": "3e2f8fb39c190f3f5015cfe1478752d8a88e858f0b0efbb41528b5bbafcbdbe4",
  "cards": [
    {
      "content_sha256": "8ea7345e9100027c381b8bdfeac8bd4c7cba8e71993ead2244a6e8056deea334",
      "content_summary": "纠正EP必然触发All-to-All的判断",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正ep必然触发all-to-all的判断"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1d6b617e469179dac93fe21d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e816657f48abed7dbb62a78b4a4c4f9a55aff3250911e2e13dc276a0bd82d172",
      "content_summary": "区分专家参数分布与Token激活的切分轴",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分专家参数分布与token激活的切分轴"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-867fd12c1e5ec46954ba4fc5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0c17685148364466f96a2ca262572c7c0eeb95f8a7c0a7acbf156c6c8c88d6a0",
      "content_summary": "核对top-k分配总数和单专家Token数上界",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-routing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "核对top-k分配总数和单专家token数上界"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-89ea1982dbd37d613b62bce4",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "149006aa3bfc08a0a496b4c0658eb15b0fb00d6b9aaaed19677081f4197aed78",
      "content_summary": "区分相同输入存储与不同专家输出的复用",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-correctness",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分相同输入存储与不同专家输出的复用"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-b7c838c542999983ae114feb",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2db65ab8204e6e93d6b1ce238e658190b04aefd0a96606f740891410ce9c224c",
      "content_summary": "解释top-k展开后的结果如何还原原Token",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-routing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释top-k展开后的结果如何还原原token"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-6bebcad9717b404c52d94fa5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2bb6b3d120bf24e594d1800ccae25e70ef202df65c6507a12e0716f42b2c7537",
      "content_summary": "依据目标设备去重规则计算激活传输量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-communication",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "依据目标设备去重规则计算激活传输量"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-cefcb2fc250dc77c80289b67",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "78c9833e04444005b41811a4edb7b2c19ac1402812272c5224e36a3cb3f36c06",
      "content_summary": "解释回传前局部加权合并如何减少向量份数",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-communication",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释回传前局部加权合并如何减少向量份数"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-35c4641158473f885021ed6d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3aa3aca77a1825d7b347a9cdc0d2f1fe5664ef182b6777e773a1bdb836598510",
      "content_summary": "按独立与共享带宽资源推导通信时间下界",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "communication-modeling",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "按独立与共享带宽资源推导通信时间下界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-73374ad0ac1508fc72980cfb",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "86d42e4cd85aa09104ce75016980df221666aab234f7696590ef2804f2e6ec00",
      "content_summary": "区分逻辑路由专家放置与EPLB的职责",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-load-balancing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分逻辑路由专家放置与eplb的职责"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3e1db8a92d09ee3eeb0b4f25",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "901afb8beb12a5ee52b5be376be4fbea88b06ccd081e8175569e88e7c62e90b8",
      "content_summary": "保持冗余专家副本下的逻辑任务唯一性",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-load-balancing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "保持冗余专家副本下的逻辑任务唯一性"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d4a71e99049d650808ed8767",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4c7bbc57b60b909bc9a7c90eb69d07422858956021c0ad8acf7d6bf51f097912",
      "content_summary": "区分路由需求保留任务与padding槽位",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-routing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分路由需求保留任务与padding槽位"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d08dd585ede6e06c0c6781ff",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c787e7e0c335e3a5ce9ddf2af8712f77539e53a04e444d439e98aedf8644368e",
      "content_summary": "解释专家容量为什么不能只看单个GEMM利用率",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-execution",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释专家容量为什么不能只看单个gemm利用率"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a0b94ac2a47f5964de79df6f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6b19f404ffea5e66004d70932032082271bb317282f52f8841e72a5b7fadb390",
      "content_summary": "判断丢弃专家分配后残差是否恢复缺失贡献",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-correctness",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "判断丢弃专家分配后残差是否恢复缺失贡献"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-696cfc577159b8b0e927c313",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "08c843676d3afb7e423bf7adc6a8a2ecc6653be3a405a7f4289a784fc7abf793",
      "content_summary": "区分显式专家分配丢弃与一般推理服务过载",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-correctness",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分显式专家分配丢弃与一般推理服务过载"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-34a4f789903fd6761330ed5f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8e154db111f7ea7d4dc852914ce46f494b0a15b98da39825b9407cf0a588031b",
      "content_summary": "推导SwiGLU专家的激活与权重形状",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-ffn",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "推导swiglu专家的激活与权重形状"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-da4f6e8f0aeaa77ca933d608",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6f634a695b31547727f0678537fcf672ca9f2c5f1522a6ae58777c28487a2c3b",
      "content_summary": "区分SwiGLU门控与MoE专家路由",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-ffn",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分swiglu门控与moe专家路由"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-25fee1d5c60e319497fd8a38",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b28c476bd5242ce7643406450633391f2837dde384dcdc646f7042fe36b704ae",
      "content_summary": "由SwiGLU中间维切分推导下投影归约",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "tensor-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "由swiglu中间维切分推导下投影归约"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-bb71f024764a3bd8fed6fd2d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "58db90887bb230e9bad828c8517dff032e9a42070ba32a4ef8624fa0c4df704b",
      "content_summary": "解释先截取不同Token行再AllReduce为何错误",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "sequence-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释先截取不同token行再allreduce为何错误"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-ae0e4dd53d8ff183052d2771",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fcdc83603e83e623f1e78ea101a064769d6d823b7766330743648fb4bbd71f74",
      "content_summary": "连接TP与SP的前向布局转换",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "sequence-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "连接tp与sp的前向布局转换"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d9db44b1295a936d592dda2c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "81ef427df97cc9d23db47d720f83072737b79df2d605bdaf28c8cb6ea1b4ebe1",
      "content_summary": "解释分块Attention为何需要归一化统计",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "context-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释分块attention为何需要归一化统计"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-88dfb063b92da8833fb69f78",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "95da2201f47d152fd8ace07672ecb88c178f420299fead00027504c8d3aa2e99",
      "content_summary": "识别Megatron-Core 0.15中CP通信路径的布局差异",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "context-parallelism",
        "fact_scope": {
          "kind": "snapshot",
          "product": "megatron-core",
          "version": "0.15.0"
        },
        "recall_target": "识别megatron-core 0.15中cp通信路径的布局差异"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-75a8cc0599ad76f6137e8811",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "80cfe495729e8433bf68178f8babcd0ddab3dc22652cfe6b37b729b1dc80d85a",
      "content_summary": "区分DP副本之间与副本内TP归约的输出身份",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "data-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分dp副本之间与副本内tp归约的输出身份"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-20d9288c4aae633daf07ed15",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2d61116998ab3a00b4b33918a6b4a66f3a4b9fa53cab7ab0bce9fe81672d2ecd",
      "content_summary": "区分前向流水线首批延迟与持续产出间隔",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "pipeline-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分前向流水线首批延迟与持续产出间隔"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-ede3b7761d8f0fefedd61576",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "103848c2476d8112c8691c28cc762a3912ca2ac6b064ad50771a858d185c9632",
      "content_summary": "按每个TP rank的约束判断副本准入",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "serving-admission",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "按每个tp rank的约束判断副本准入"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9407bd4570b8f2fc67ae005a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ce430d5fbf4cf97841feff4a2e5607432ee5f1a2c1801e1ece595b0ae9953326",
      "content_summary": "正确计算闭区间Token行数及BF16载荷",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "tensor-indexing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "正确计算闭区间token行数及bf16载荷"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-352fad97a7752e880758c21a",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6e446139220b5b1a968b6b21785c1a2d534c3cf97f9bff67fa8f4362d391fe94",
      "content_summary": "区分grouped GEMM组织方式与专家计算语义",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-ffn",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分grouped gemm组织方式与专家计算语义"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d4f5434d74d4a92ee550be1a",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-u1-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "41a27cbc2d05c916a823b2924d1eb071960c42f0dd0decab43807f6f3e5754cf",
  "manifest_payload_sha256": "0755ba43335096ee24e1df58bdf90d0839639406f1f13642757b52528b80eb71",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5079,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w2-u1-moe-ep-parallelism-correction.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "8ea7345e9100027c381b8bdfeac8bd4c7cba8e71993ead2244a6e8056deea334",
          "logical_id": "mc-1d6b617e469179dac93fe21d",
          "row_sha256": "d5524a93a7f1e6fea839397e113cf49a41fb4423aeeee632d5af59a30b5b3ba9"
        },
        {
          "content_sha256": "ce430d5fbf4cf97841feff4a2e5607432ee5f1a2c1801e1ece595b0ae9953326",
          "logical_id": "mc-352fad97a7752e880758c21a",
          "row_sha256": "73c343a347542f85c4ace6697884b3a230abc9f14a10f85c0a9a38a19c739a3c"
        }
      ],
      "sha256": "e3bb0a9108cbaa51d5cf598464967b21a116adca68d370b0afdb4a06bd399cf3",
      "sheet_name": "cards",
      "table_sha256": "17e4401caf43d2726020d483ee8a809eab651259435c38ae4dd61f5f8fa1335a",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 28909,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w2-u1-moe-ep-parallelism-technical-qa.xlsx",
      "row_count": 24,
      "rows": [
        {
          "content_sha256": "e816657f48abed7dbb62a78b4a4c4f9a55aff3250911e2e13dc276a0bd82d172",
          "logical_id": "mc-867fd12c1e5ec46954ba4fc5",
          "row_sha256": "a00a4135a3a082e71b747613bac0a43e27002d3d6000bce810242cec16a4ed73"
        },
        {
          "content_sha256": "0c17685148364466f96a2ca262572c7c0eeb95f8a7c0a7acbf156c6c8c88d6a0",
          "logical_id": "mc-89ea1982dbd37d613b62bce4",
          "row_sha256": "35016b27bfadc08d08e5b62dfb5ff416b26dcbe77dd10de94eb56b2dd5e1843f"
        },
        {
          "content_sha256": "149006aa3bfc08a0a496b4c0658eb15b0fb00d6b9aaaed19677081f4197aed78",
          "logical_id": "mc-b7c838c542999983ae114feb",
          "row_sha256": "5cd2e16bd916c8f8525151a05eda65ac6b6fac44d638ed2b05b048c4e7c2bbe4"
        },
        {
          "content_sha256": "2db65ab8204e6e93d6b1ce238e658190b04aefd0a96606f740891410ce9c224c",
          "logical_id": "mc-6bebcad9717b404c52d94fa5",
          "row_sha256": "2a829bb3371175c47e1eec6843e621268450e521a93c6f1b3060b192029d3607"
        },
        {
          "content_sha256": "2bb6b3d120bf24e594d1800ccae25e70ef202df65c6507a12e0716f42b2c7537",
          "logical_id": "mc-cefcb2fc250dc77c80289b67",
          "row_sha256": "23ab96aca5827a47632893af03428660a23b5d39f444f67d9a761eb6752cc9e4"
        },
        {
          "content_sha256": "78c9833e04444005b41811a4edb7b2c19ac1402812272c5224e36a3cb3f36c06",
          "logical_id": "mc-35c4641158473f885021ed6d",
          "row_sha256": "306ec969fb7f9de92069e681508f1f38b756d1d08f07e1028817dceb5e085692"
        },
        {
          "content_sha256": "3aa3aca77a1825d7b347a9cdc0d2f1fe5664ef182b6777e773a1bdb836598510",
          "logical_id": "mc-73374ad0ac1508fc72980cfb",
          "row_sha256": "db84d78935d55451c78e38104f0d269c66b530c18cf82d0946e07f1daaf6b19f"
        },
        {
          "content_sha256": "86d42e4cd85aa09104ce75016980df221666aab234f7696590ef2804f2e6ec00",
          "logical_id": "mc-3e1db8a92d09ee3eeb0b4f25",
          "row_sha256": "db52b3c23c4fcaec33b87a6a2b104042c6207d3117990a42c9b70c2632962eb2"
        },
        {
          "content_sha256": "901afb8beb12a5ee52b5be376be4fbea88b06ccd081e8175569e88e7c62e90b8",
          "logical_id": "mc-d4a71e99049d650808ed8767",
          "row_sha256": "7977282c4cc71da151abbdf273aa8a9482a58296aadd97fe6e15cf8e4e51449b"
        },
        {
          "content_sha256": "4c7bbc57b60b909bc9a7c90eb69d07422858956021c0ad8acf7d6bf51f097912",
          "logical_id": "mc-d08dd585ede6e06c0c6781ff",
          "row_sha256": "0dd96ae910a6de6e107027cfb0eaf0f9c2a295d72e37ac6bb44a3f8ac7cf40a3"
        },
        {
          "content_sha256": "c787e7e0c335e3a5ce9ddf2af8712f77539e53a04e444d439e98aedf8644368e",
          "logical_id": "mc-a0b94ac2a47f5964de79df6f",
          "row_sha256": "cf0d727ade02877444fbbb94373f980ff921df99d287ac8ac48ebce1d1c24ec3"
        },
        {
          "content_sha256": "6b19f404ffea5e66004d70932032082271bb317282f52f8841e72a5b7fadb390",
          "logical_id": "mc-696cfc577159b8b0e927c313",
          "row_sha256": "3974aa14eac65bcce344cc37c100ef2aeb3f9ce08e137dd04fbf88c8c94f663a"
        },
        {
          "content_sha256": "08c843676d3afb7e423bf7adc6a8a2ecc6653be3a405a7f4289a784fc7abf793",
          "logical_id": "mc-34a4f789903fd6761330ed5f",
          "row_sha256": "5899e6748278430bc48e2abf77ce46eae0056ac2b2c5182d6b84980448b6174a"
        },
        {
          "content_sha256": "8e154db111f7ea7d4dc852914ce46f494b0a15b98da39825b9407cf0a588031b",
          "logical_id": "mc-da4f6e8f0aeaa77ca933d608",
          "row_sha256": "9369959749a3b380bf6aa8a1b21cb7fd92576c5f216466044d77fc61e02414ac"
        },
        {
          "content_sha256": "6f634a695b31547727f0678537fcf672ca9f2c5f1522a6ae58777c28487a2c3b",
          "logical_id": "mc-25fee1d5c60e319497fd8a38",
          "row_sha256": "bf5a9a525e05bcfea58c91dc50d7973f1881fd847802ffa993e2f527ded5e098"
        },
        {
          "content_sha256": "b28c476bd5242ce7643406450633391f2837dde384dcdc646f7042fe36b704ae",
          "logical_id": "mc-bb71f024764a3bd8fed6fd2d",
          "row_sha256": "d7670bd7acc2deb62227a5c3cb306da800225707b3c4bf7ec71fb8ac8a11e133"
        },
        {
          "content_sha256": "58db90887bb230e9bad828c8517dff032e9a42070ba32a4ef8624fa0c4df704b",
          "logical_id": "mc-ae0e4dd53d8ff183052d2771",
          "row_sha256": "81b47abdf7641efc4d486dbdb703ed2c9a2ec98ab93f1e8a4929e85f9df6ce95"
        },
        {
          "content_sha256": "fcdc83603e83e623f1e78ea101a064769d6d823b7766330743648fb4bbd71f74",
          "logical_id": "mc-d9db44b1295a936d592dda2c",
          "row_sha256": "6194a1abed3841d45a7ef5a98421ac5ffead89c56eaa89fa8777eae029080628"
        },
        {
          "content_sha256": "81ef427df97cc9d23db47d720f83072737b79df2d605bdaf28c8cb6ea1b4ebe1",
          "logical_id": "mc-88dfb063b92da8833fb69f78",
          "row_sha256": "e1097d863af47f6b95bea11d6d0c691620d50eb017224908151a906193c14b7c"
        },
        {
          "content_sha256": "95da2201f47d152fd8ace07672ecb88c178f420299fead00027504c8d3aa2e99",
          "logical_id": "mc-75a8cc0599ad76f6137e8811",
          "row_sha256": "d89d10cb0245df7a6e1cc44a6579bfc864e55074850ca42b0330cd3f62f7d4a5"
        },
        {
          "content_sha256": "80cfe495729e8433bf68178f8babcd0ddab3dc22652cfe6b37b729b1dc80d85a",
          "logical_id": "mc-20d9288c4aae633daf07ed15",
          "row_sha256": "fdedd7972e8b0c0cf78cb057b9d9adc9ba9165d90ef1dad47aed260e57576961"
        },
        {
          "content_sha256": "2d61116998ab3a00b4b33918a6b4a66f3a4b9fa53cab7ab0bce9fe81672d2ecd",
          "logical_id": "mc-ede3b7761d8f0fefedd61576",
          "row_sha256": "1b6b2ca5cb72193d32cd41b2ee9fe3ff83abb725d205af3d501d855820c906b4"
        },
        {
          "content_sha256": "103848c2476d8112c8691c28cc762a3912ca2ac6b064ad50771a858d185c9632",
          "logical_id": "mc-9407bd4570b8f2fc67ae005a",
          "row_sha256": "c55637ac5bef7fac131c0dc2865a7c5efca02e95a9f282f65d154cb323306c89"
        },
        {
          "content_sha256": "6e446139220b5b1a968b6b21785c1a2d534c3cf97f9bff67fa8f4362d391fe94",
          "logical_id": "mc-d4f5434d74d4a92ee550be1a",
          "row_sha256": "5a7d05add69a79049240c2fe3458318a15ebe2d93966d53662c8b013ecc6f977"
        }
      ],
      "sha256": "68d38009ae413c996152e8c6e002da28afe914496f23960375f10c10b8db6de7",
      "sheet_name": "cards",
      "table_sha256": "96cb871affacf353bce74ce932dbaeba7c1dbee6189d00822c76b5dd6f299437",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "a85c73a97689de75329b156064eefa318050e2b6bdfa39e8869dd9549baffc38",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "w2-u1-log",
      "path": "推理框架/log/2026-09-28-w2-u1-moe-ep-parallelism.md",
      "sha256": "547b1e81a488fce070624c59956614d8b49ace00cc1db137d7c517e13e2fda58",
      "summary": "W2单元一的结构化学习过程：真实纠错、关键转折与已核验的MoE/并行策略边界；不消费raw或遗留猜测。"
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

导入文件：[w2-u1-moe-ep-parallelism-correction.xlsx](w2-u1-moe-ep-parallelism-correction.xlsx)（2 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[w2-u1-moe-ep-parallelism-technical-qa.xlsx](w2-u1-moe-ep-parallelism-technical-qa.xlsx)（24 张卡）
