---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "0afcd66a4d125ac53d778202a17d118ba7198414734da6427f8fd759474c0c8d",
  "candidate_sha256": "91a810ebf58dfb85a407c8634d21f67ec8c7bda9d869d1825677a24949555c36",
  "cards": [
    {
      "content_sha256": "8ea7345e9100027c381b8bdfeac8bd4c7cba8e71993ead2244a6e8056deea334",
      "content_summary": "纠正EP必然触发All-to-All的判断；2026-11-03复核：A理由：防止把EP必然等同于All-to-All而误判真实执行路径；能解释输入复制布局下的替代归约。",
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
      "content_sha256": "9591d7b2240a6cbac656498c42a91a69b19d5fd7cef748499a5bf6791db5d262",
      "content_summary": "区分专家参数分布与Token激活的切分轴；2026-11-03复核：B理由：保留专家参数、Token行和隐藏维的布局辨析，便于组合并行策略；来源中后续判断已经正确，按迁移基础而非高优先纠错保留。",
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
      "content_sha256": "0c17685148364466f96a2ca262572c7c0eeb95f8a7c0a7acbf156c6c8c88d6a0",
      "content_summary": "核对top-k分配总数和单专家Token数上界；2026-11-03复核：B理由：保留检查Token–expert任务守恒和容量上界的方法；属于已掌握的计数基础，不再将单纯TK计数列为A级。",
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
      "content_sha256": "2a8ac8e77465dbd7737cd1d4b9e0bb572fb1622957744ac9e8efc644326d1bba",
      "content_summary": "区分相同输入存储与不同专家输出的复用；2026-11-03复核：B理由：保留输入存储复用与计算结果复用的等价性边界；来源首答正确，按稳定迁移知识保留。",
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
      "content_sha256": "2db65ab8204e6e93d6b1ce238e658190b04aefd0a96606f740891410ce9c224c",
      "content_summary": "解释top-k展开后的结果如何还原原Token；2026-11-03复核：A理由：防止把专家打包行直接当作原Token输出，或遗漏top-k加权汇合，造成静默错误。",
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
      "content_summary": "依据目标设备去重规则计算激活传输量；2026-11-03复核：A理由：防止混用目标GPU和目标节点的去重粒度，成倍误估跨节点载荷和通信瓶颈。",
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
      "content_summary": "解释回传前局部加权合并如何减少向量份数；2026-11-03复核：A理由：防止局部合并后回源时重复施加路由权重，并能解释保持数学关系的载荷缩减。",
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
      "content_summary": "按独立与共享带宽资源推导通信时间下界；2026-11-03复核：A理由：回答通信时间下界的面试题，防止把独立双向、共享出口和串行阶段按同一个字节总量计算。",
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
      "content_summary": "区分逻辑路由专家放置与EPLB的职责；2026-11-03复核：B理由：保留放置与逻辑专家选择的职责区分；来源中学习者已独立说明不改变router选择，降低重复复习优先级。",
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
      "content_sha256": "901afb8beb12a5ee52b5be376be4fbea88b06ccd081e8175569e88e7c62e90b8",
      "content_summary": "保持冗余专家副本下的逻辑任务唯一性；2026-11-03复核：B理由：保留物理副本与逻辑任务唯一性的区别及权重存储代价；来源首答已正确，作为迁移基础保留。",
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
      "content_sha256": "4c7bbc57b60b909bc9a7c90eb69d07422858956021c0ad8acf7d6bf51f097912",
      "content_summary": "区分路由需求保留任务与padding槽位；2026-11-03复核：A理由：防止把补齐后的相同形状当成任务无丢失证据，导致padding或丢弃贡献进入错误的combine判断。",
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
      "content_summary": "解释专家容量为什么不能只看单个GEMM利用率；2026-11-03复核：B理由：保留单GEMM效率与全层热点、显存及padding成本的取舍；作为设计理由复习，不要求背记例子中的槽位数。",
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
      "content_sha256": "6b19f404ffea5e66004d70932032082271bb317282f52f8841e72a5b7fadb390",
      "content_summary": "判断丢弃专家分配后残差是否恢复缺失贡献；2026-11-03复核：A理由：防止把丢弃专家分配当成由残差或重归一化自动补偿的等价优化。",
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
      "content_summary": "区分显式专家分配丢弃与一般推理服务过载；2026-11-03复核：A理由：防止由服务压力或buffer容量上限直接宣称框架静默少算专家，混淆调度故障与模型语义。",
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
      "content_summary": "推导SwiGLU专家的激活与权重形状；2026-11-03复核：B理由：保留沿SwiGLU计算链推导激活和权重形状的可迁移方法；来源已独立掌握，不再将形状复述设为A级。",
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
      "content_sha256": "6f634a695b31547727f0678537fcf672ca9f2c5f1522a6ae58777c28487a2c3b",
      "content_summary": "区分SwiGLU门控与MoE专家路由；2026-11-03复核：B理由：同名gate存在不同作用轴，保留辨析以减少术语干扰。",
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
      "content_summary": "由SwiGLU中间维切分推导下投影归约；2026-11-03复核：A理由：回答TP为何需要输出归约的面试题，防止把形状完整的局部部分和当成数值完整输出。",
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
      "content_summary": "解释先截取不同Token行再AllReduce为何错误；2026-11-03复核：A理由：防止将不同全局Token的局部切片直接AllReduce，造成跨Token错位求和和贡献丢失。",
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
      "content_summary": "连接TP与SP的前向布局转换；2026-11-03复核：A理由：回答TP与SP如何连接完整前向布局的面试题，说明AG、FFN、RS及本地LayerNorm的必要条件。",
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
      "content_summary": "解释分块Attention为何需要归一化统计；2026-11-03复核：A理由：防止直接相加局部softmax输出；能用归一化质量说明分块Attention合并为何需要额外统计。",
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
      "content_sha256": "809ee9a56e6c863699f9a1181a8874ff4de005d6d109e394fd85e48f257c26dd",
      "content_summary": "识别Megatron-Core 0.15中CP通信路径的布局差异；2026-11-03复核：B理由：保留固定版本CP路径的布局差异，防止把Q留本地外推到所有通信类型。",
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
      "content_sha256": "73990218d90b65dde1cdab8d1767fbf8f559807d152dc4d88fb1462f52967f1a",
      "content_summary": "区分DP副本之间与副本内TP归约的输出身份；2026-11-03复核：B理由：保留用逻辑输出身份确定归约组的迁移原则；来源首答已完整说明不同请求不能相加。",
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
      "content_sha256": "2d61116998ab3a00b4b33918a6b4a66f3a4b9fa53cab7ab0bce9fe81672d2ecd",
      "content_summary": "区分前向流水线首批延迟与持续产出间隔；2026-11-03复核：B理由：保留单批依赖链与瓶颈阶段的不同时间含义；数值只作给定条件下的推导，不以首答正确的算术作为A级考点。",
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
      "content_sha256": "642bd8f46a46fa763b982b81fafc7814558c7c176a35030ee653197bc5f56a2c",
      "content_summary": "按每个TP rank的约束判断副本准入；2026-11-03复核：A理由：防止把TP组资源相加当作任意共享池，接收某个rank实际无法容纳的新请求。",
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
      "content_summary": "2026-11-03本地归档：本轮按C级价值判定的一次算术口误，不进入正式复习；quality保留历史B以兼容工具的归档记录，不能据此重新纳入导出。",
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
      "lifecycle": "archived",
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
      "content_sha256": "cba9680ae255ed249f9d4fe6b5f6c75a761aa0ff2a5797fe72ca6315ba0e1249",
      "content_summary": "区分grouped GEMM组织方式与专家计算语义；2026-11-03复核：B理由：保留共同组织矩阵乘与共享权重、整链融合之间的边界，避免从名称推断实现。",
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
  "managed_body_sha256": "9a3192d7c2c4af2466b8df28855a80fbe48e32c7a3fcd1eb555b1e8100fb87b1",
  "manifest_payload_sha256": "8730c9c5770809a796adf93efcdeb9fa19605d840bf1ae709df7801fb262a1db",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 3851,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/w2-u1-moe-ep-parallelism-correction.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "8ea7345e9100027c381b8bdfeac8bd4c7cba8e71993ead2244a6e8056deea334",
          "logical_id": "mc-1d6b617e469179dac93fe21d",
          "row_sha256": "d5524a93a7f1e6fea839397e113cf49a41fb4423aeeee632d5af59a30b5b3ba9"
        }
      ],
      "sha256": "7c58e4ecbb8a2dcbb8e8f9c7f1d427f2c9b71b29a3432f7ff5bf4c6b1a09b214",
      "sheet_name": "cards",
      "table_sha256": "d85aac4492d85b62522faed446cb8b335d0a45eb37f3f6b8d9550321d265de0b",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 29431,
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
          "content_sha256": "9591d7b2240a6cbac656498c42a91a69b19d5fd7cef748499a5bf6791db5d262",
          "logical_id": "mc-867fd12c1e5ec46954ba4fc5",
          "row_sha256": "a8164f843bb763ade7ed8b75781fe3073349a110f5e0489b42f62abd557d712c"
        },
        {
          "content_sha256": "0c17685148364466f96a2ca262572c7c0eeb95f8a7c0a7acbf156c6c8c88d6a0",
          "logical_id": "mc-89ea1982dbd37d613b62bce4",
          "row_sha256": "35016b27bfadc08d08e5b62dfb5ff416b26dcbe77dd10de94eb56b2dd5e1843f"
        },
        {
          "content_sha256": "2a8ac8e77465dbd7737cd1d4b9e0bb572fb1622957744ac9e8efc644326d1bba",
          "logical_id": "mc-b7c838c542999983ae114feb",
          "row_sha256": "f8a494d04514e5dedb8601d3a30f600e51fb494563f7afc2189b49137c4e231b"
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
          "content_sha256": "809ee9a56e6c863699f9a1181a8874ff4de005d6d109e394fd85e48f257c26dd",
          "logical_id": "mc-75a8cc0599ad76f6137e8811",
          "row_sha256": "6c2eda5035fe2b7262f44ee263f0137f031e26b766368bab904240e3a3e0b860"
        },
        {
          "content_sha256": "73990218d90b65dde1cdab8d1767fbf8f559807d152dc4d88fb1462f52967f1a",
          "logical_id": "mc-20d9288c4aae633daf07ed15",
          "row_sha256": "c050ecde1b0d7d1a9768444fe74525856d6766a06aa5e792fb93e04472ebc914"
        },
        {
          "content_sha256": "2d61116998ab3a00b4b33918a6b4a66f3a4b9fa53cab7ab0bce9fe81672d2ecd",
          "logical_id": "mc-ede3b7761d8f0fefedd61576",
          "row_sha256": "1b6b2ca5cb72193d32cd41b2ee9fe3ff83abb725d205af3d501d855820c906b4"
        },
        {
          "content_sha256": "642bd8f46a46fa763b982b81fafc7814558c7c176a35030ee653197bc5f56a2c",
          "logical_id": "mc-9407bd4570b8f2fc67ae005a",
          "row_sha256": "7ceacd8a3a276407cb8d31427ff9c68bfd8d3d3f9aeddd603bf692a7856cb54f"
        },
        {
          "content_sha256": "cba9680ae255ed249f9d4fe6b5f6c75a761aa0ff2a5797fe72ca6315ba0e1249",
          "logical_id": "mc-d4f5434d74d4a92ee550be1a",
          "row_sha256": "af7554680662d43c2d4c18be807a50d5e186bba888e0d78cafb10f4c7f103683"
        }
      ],
      "sha256": "5cda2523caca3fc06eac4a4f15913f1344f149980addae299547ddcfaa61789a",
      "sheet_name": "cards",
      "table_sha256": "949bed0471950dce2115a61f93dc43ab1ca152751bd02bb414fcdef643263130",
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

导入文件：[w2-u1-moe-ep-parallelism-correction.xlsx](w2-u1-moe-ep-parallelism-correction.xlsx)（1 张卡）

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
