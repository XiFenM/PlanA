---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "3e85c53e39c8eba5323c2cd3085efe0933c26ffbed543087d318701ea6991864",
  "candidate_sha256": "a93a932cb9c7b8c84d2678cc3a7ee52685ef695a97f08daad3beaee410d14bda",
  "cards": [
    {
      "content_sha256": "9ca120f57fe89c2e12a33b94d61baa8451f262b95c2c053fc7a114aac8ac8b50",
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
      "content_sha256": "673a8a8050f2148191b99e766d7c7d3bc5cf2b3e036ea5424386e753e08a5c3c",
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
      "content_sha256": "dc9bec541a81c6630537e747fe5a872186bdbbf09b161d5a8a4da09936386dfc",
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
      "content_sha256": "732119ae6ef9825193d491fbd1a4a3cc1ae496b6234e2a311d5747cdf13abb13",
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
      "content_sha256": "e93ceb8591d33828ac7b7e295e40e3dd41f95db90ff2b045d5b7e7cd9a703416",
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
      "content_sha256": "994040a2fafaf47e3c592459b8821030ffbbdb1f82a2ecf5b73010ff4295a83b",
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
      "content_sha256": "f28b241b4c238070ca3091ca61a46e7594a981b8f1a97fc74da556b2a96d4561",
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
      "content_sha256": "a045bc8ff7e1f562675299228de4c79bac4224dc902f50dc9718f777545bb51c",
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
      "content_sha256": "b8f022eef2ddede8d85ffd6c197e55dab0361639473677256eeafd94198a5735",
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
      "content_sha256": "65db2ac29d9981a5d1381c3c7cb6f5b96d470170ad075cecca5507be1961d445",
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
      "content_sha256": "7d90ed5639c706c282334e312a741bedde2b82b654f4f44369f77a1831cac8bd",
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
      "content_sha256": "3139c14fedade4aa8ae44a71eba373786b5bceaa68444529f20d358e8880a80d",
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
      "content_sha256": "9c479b191269de5e684b93b1a70a88abcf341b78b74e4b77bfd314439631981d",
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
      "content_sha256": "24c423e891d94b06e6736229a7f8e736ca56d4d5cac87d05bc62bac9cf920cf7",
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
  "manifest_payload_sha256": "329a6b40b18deb32ca2dbaf4fb537ad30ac2d1961385b08437deb82089fe222c",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 3942,
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
          "content_sha256": "9ca120f57fe89c2e12a33b94d61baa8451f262b95c2c053fc7a114aac8ac8b50",
          "logical_id": "mc-1d6b617e469179dac93fe21d",
          "row_sha256": "1df8a135ec01696484585d2e9112124229c7e79901c403aa55b595880f1a3fb8"
        }
      ],
      "sha256": "bde5baa3c9e878a78c260ad431385e005185518f3de9ecfc4d44021215cec36d",
      "sheet_name": "cards",
      "table_sha256": "b9e0037683e023ef3f5832df2ccba96cef9701a1b85d8ece3bfff13f1ebfad15",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 30054,
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
          "content_sha256": "673a8a8050f2148191b99e766d7c7d3bc5cf2b3e036ea5424386e753e08a5c3c",
          "logical_id": "mc-867fd12c1e5ec46954ba4fc5",
          "row_sha256": "556f570faccb4439adb58c367a4d5047216e3f8f58c6d7b0abc436d38ddd0eb9"
        },
        {
          "content_sha256": "dc9bec541a81c6630537e747fe5a872186bdbbf09b161d5a8a4da09936386dfc",
          "logical_id": "mc-89ea1982dbd37d613b62bce4",
          "row_sha256": "a72d983cafa63368426f798a73cad865eb5b524d9e057b1d940d09b154dacfb6"
        },
        {
          "content_sha256": "2a8ac8e77465dbd7737cd1d4b9e0bb572fb1622957744ac9e8efc644326d1bba",
          "logical_id": "mc-b7c838c542999983ae114feb",
          "row_sha256": "f8a494d04514e5dedb8601d3a30f600e51fb494563f7afc2189b49137c4e231b"
        },
        {
          "content_sha256": "732119ae6ef9825193d491fbd1a4a3cc1ae496b6234e2a311d5747cdf13abb13",
          "logical_id": "mc-6bebcad9717b404c52d94fa5",
          "row_sha256": "cda56401fb5af6f5a5c2038763664cab7a2e1c8707970502623e5fdbff8751c8"
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
          "content_sha256": "e93ceb8591d33828ac7b7e295e40e3dd41f95db90ff2b045d5b7e7cd9a703416",
          "logical_id": "mc-3e1db8a92d09ee3eeb0b4f25",
          "row_sha256": "29a8de7de764c858fa03b1a109f70f654a77162ec004a1f039cf2915a1ad8db9"
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
          "content_sha256": "994040a2fafaf47e3c592459b8821030ffbbdb1f82a2ecf5b73010ff4295a83b",
          "logical_id": "mc-a0b94ac2a47f5964de79df6f",
          "row_sha256": "40a880d6de3c87b04fc90998fe476e2b9d711754fad90c919a01f8f056fa3321"
        },
        {
          "content_sha256": "f28b241b4c238070ca3091ca61a46e7594a981b8f1a97fc74da556b2a96d4561",
          "logical_id": "mc-696cfc577159b8b0e927c313",
          "row_sha256": "fcba8af580c4d6f6e0d156045623d3f0b14bcc8eb07b6ebcf72f8769bc55116a"
        },
        {
          "content_sha256": "a045bc8ff7e1f562675299228de4c79bac4224dc902f50dc9718f777545bb51c",
          "logical_id": "mc-34a4f789903fd6761330ed5f",
          "row_sha256": "e4c4405ecc2c49938844c7232d6090b787bb1649be36c85b4446a26355bc61ae"
        },
        {
          "content_sha256": "b8f022eef2ddede8d85ffd6c197e55dab0361639473677256eeafd94198a5735",
          "logical_id": "mc-da4f6e8f0aeaa77ca933d608",
          "row_sha256": "1e2053095f6492fb2cb96d21e3ad55eeabbbb661e912ceca647299c616da730f"
        },
        {
          "content_sha256": "65db2ac29d9981a5d1381c3c7cb6f5b96d470170ad075cecca5507be1961d445",
          "logical_id": "mc-25fee1d5c60e319497fd8a38",
          "row_sha256": "250573c6ef22087b2510a25005fd17592d059ffa77af929146ee849d67d38294"
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
          "content_sha256": "7d90ed5639c706c282334e312a741bedde2b82b654f4f44369f77a1831cac8bd",
          "logical_id": "mc-d9db44b1295a936d592dda2c",
          "row_sha256": "a84a03a1758433b896c693ecc4b304e28d8a7fa2520fb5e5fe74f507fc5c6302"
        },
        {
          "content_sha256": "3139c14fedade4aa8ae44a71eba373786b5bceaa68444529f20d358e8880a80d",
          "logical_id": "mc-88dfb063b92da8833fb69f78",
          "row_sha256": "0efe6c3842a8cb11e022966183f62f0cb901fa76ffacd93fbdc2edb3449b8dcd"
        },
        {
          "content_sha256": "809ee9a56e6c863699f9a1181a8874ff4de005d6d109e394fd85e48f257c26dd",
          "logical_id": "mc-75a8cc0599ad76f6137e8811",
          "row_sha256": "6c2eda5035fe2b7262f44ee263f0137f031e26b766368bab904240e3a3e0b860"
        },
        {
          "content_sha256": "9c479b191269de5e684b93b1a70a88abcf341b78b74e4b77bfd314439631981d",
          "logical_id": "mc-20d9288c4aae633daf07ed15",
          "row_sha256": "1e53942aeaefa142f790bc1a14fee7a0bf7e8e10e6e08b935315ef1173695725"
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
          "content_sha256": "24c423e891d94b06e6736229a7f8e736ca56d4d5cac87d05bc62bac9cf920cf7",
          "logical_id": "mc-d4f5434d74d4a92ee550be1a",
          "row_sha256": "c4fa059b8c67cbd1332349fc73a70bd06aa8d10fc959da7f11384bba50581f2a"
        }
      ],
      "sha256": "6be7e20bdbe9f88498e8d0fd7de562138ea00ab068794ccc9cfddd84082b244a",
      "sheet_name": "cards",
      "table_sha256": "d1f0850641471105b9080f3c4cd617ceefd33e2bdc4ea8ccb9bf3b96661abfb9",
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
