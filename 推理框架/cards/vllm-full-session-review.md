---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "44f826a00dcc78f5cac353f53d1dcb11f9c9a8ccc8fb387a803c36b43bd5a949",
  "candidate_sha256": "5210f80bb35e7b173988f33bd2de7d750be390cda32213947a20abbc3e567b76",
  "cards": [
    {
      "content_sha256": "164e5905245930f35cb43bb80526d3b4d35a2f13e009310e31dc8855392063f4",
      "content_summary": "不能；本题预算是115.2 GB，不能直接用设备总容量代替。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "memory-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分设备总容量与配置内存预算"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a4cd934451dbc2f674b835a9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "17a5275718f87ea6ea0a148eef7d0034feb101aed30c39b99cb898777f06b0b5",
      "content_summary": "不能据此推断；倍率只对应发生该物化布局的局部数据。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "tensor-layout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "限定局部padding倍率的适用范围"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d90a8a49188317c4475bb1fa",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "ab6cdb0458a51ef2b47ce222d801ef098b217feadb7d0f70cf516f7d6c5fe1c2",
      "content_summary": "按一次乘法加一次加法计2次浮点运算。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "roofline",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "计算普通矩阵乘的浮点运算量"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-b5ab4a7997b4428cc78802e8",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "e3a9b6b577c47c521ac142b1738be17c9698b61d6d198d69936799477902ac59",
      "content_summary": "把A、B的读取与C的写入都计入，每元素2字节。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "roofline",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "计算给定最小读写假设下的bf16矩阵乘流量"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-abe7eb24831612c9c3d4eef7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "6eb0f3500ffadd113af1515bf9481836b944ede21f6ddb2db0da7c5136d1e0e8",
      "content_summary": "不够；需确认存储层级、地址映射和相应观测证据。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "performance-diagnosis",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分访存变慢现象与bank冲突根因"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-84676054f06c3224f8b9d42a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "6a78722409c088339d455c0f47cb661c01e732f6c69f67cdb3c032a45d1d795e",
      "content_summary": "不能；它去掉采样选择中的随机性，不消除所有并发或Kernel不确定性。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "numerical-debugging",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "限定贪婪采样对确定性的保证"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-386eff0e70f84976785adb7b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "c44bd89a35334c96236cf1f63a69d9010472e7fcff8b80a0dc889a656db9de68",
      "content_summary": "不能；dump可能改变时序或引入同步，使竞态不再复现。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "async-debugging",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释插入dump使异常消失的证据边界"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c44b4d7a9ac36edd8c5dca77",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "bf6c0b626882396ceeea9e9bcca4cfd7681dea0d25c2d225a0d0e1ddcde8224a",
      "content_summary": "后续轨迹依赖前面的token和KV历史，后面的差异可能只是传播结果。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "numerical-debugging",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释优先定位首个生成分叉点的原因"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1ba245772d63b1465ff84b74",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "874b00853e459fcf8e4abcf57365306be523d80ec66ba55f3d7f0f019a267cc9",
      "content_summary": "不能；copy可能尚未提交到设备流，流等待未覆盖前置Host准备。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "async-lifetime",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "识别设备流等待未覆盖的host准备阶段"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-ce38809b2547d6c1f70c85f7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "c7e1a979c99aa5a83e869fd013ed16ae55097354a1b1a25f3f35b0f1d052f9a4",
      "content_summary": "不是；例如Tensor.register_hook可在Python侧观察该Tensor的梯度。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "pytorch-autograd",
        "fact_scope": {
          "commit": "70d99e998b4955e0049d13a98d77ae1b14db1f45",
          "kind": "snapshot",
          "product": "pytorch",
          "version": "v2.11.0"
        },
        "recall_target": "区分autograd实现层与python梯度观测接口"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-405fa0e547ffb00ee0743601",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "a3c271f502e5ce9db4f1c49f3833bed7e953cab8b60411662c9d15aba01e306b",
      "content_summary": "不能这样推断；stream与CPU线程不是一一对应关系。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "runtime-concurrency",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分设备stream与cpu线程上下文切换"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-bdb5ae3a65636b17a13e73b1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "4238e45408b36fb87445296e4313781ea31b18b1a9a4b616d8bfde09013bf0e8",
      "content_summary": "不能；减少依赖和提交开销的收益，要与放弃潜在overlap的代价比较。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "runtime-concurrency",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "限定单流优化相对多流的适用条件"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9d7b2af6315be86cc53562e2",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "860d883002d0b0c680a061df1aa41a6c15249de549a874e60376014be9d64fa8",
      "content_summary": "倍数是旧耗时除以新耗时；降幅是耗时减少量除以旧耗时。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "benchmark-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分加速倍数与耗时降幅的计算"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-81771102328bc5e96dde9dc2",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "5ed87699915e6bfba062e71ce129480fe0d61e78b077d99c69be1590452850a2",
      "content_summary": "不保证；按层的切分规则分片，某些参数或状态仍可能复制。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "tensor-parallelism",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "识别tp分片中的复制项"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7552190fc19fef1335707b7d",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "1b89062283c94c4459c60db93fc79db6e13cabdc1ccab2b0a5efe36593f99154",
      "content_summary": "避免Core快速返回时，前端还没有该请求的输出处理状态和Collector关联。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-request-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释前端输出注册必须先于提交core"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-ae376a7b1a41d3c8475527c6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "09c9abaeb12eb8fde5710040b929a31cfab871a3387244045548712572f37d97",
      "content_summary": "AsyncLLM可以用请求ID和output_kind创建空Collector。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-request-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "识别collector创建所需元数据"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-2731ed1a964329bd32e1ea08",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "4b32d1bf9f3cc3190965aad86c3091ff906b7226fb18ccdbf5c74197fb851c8a",
      "content_summary": "是EngineCoreRequest；Core再将它构造为内部可变Request。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-request-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "识别新增请求跨ipc的核心载荷"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c34a6067dd76a7d3dbf5a43c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "49e8537a3a5411639b09fc5228fea9b371621bdade7dc71686a683a4a7739ffe",
      "content_summary": "不能；它只解除一个等待条件，仍要通过token budget和KV资源检查。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-scheduling",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分grammar就绪与资源准入"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-34b6be82985ed08c4270ddd5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "d30b24aad1cae4723da1ec3f1c93cda0f8f49318ecfa9146ee401924b4332c5f",
      "content_summary": "不会；初始化或取得编译产物后，按请求推进匹配状态并准备本步mask。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-structured-output",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分grammar编译与逐token状态推进"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-50591c6d88488ddba1e419c9",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "be2e95c76ce6c700d407ddd04aaf4599b90c1758f71954fda33ae24d86e5c0a3",
      "content_summary": "不能；结构约束不等于事实和业务语义正确。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "structured-output",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "限定grammar对输出正确性的保证"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-79362f0684e9a30fd97821f9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "427bc70305460cfbe324f2f94dc471d81f637353d7525ad530244e7ebb0ba196",
      "content_summary": "不能；所学路径在执行前按调度计划推进计数。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-scheduling",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分调度计数与设备执行完成"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-485fa8cafc3816acbd51e03b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "9560a630fdf1de47ca14000edafe43027d55db3fef81039594032ff2d84d2571",
      "content_summary": "不能；它本轮才被采样，通常下一轮才作为输入计算自身KV。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "autoregressive-decoding",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分本步输入token与刚采样输出token"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e1d5350c48cf8fd0d15afdce",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "c6e60140da015603e8a282cc05a6dda9497d221a842ca78d6abc69686a495948",
      "content_summary": "完成prompt的最后一次prefill即可产生首个有效输出token。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "autoregressive-decoding",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "定位普通生成的首个有效输出token时机"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7ab1103a71067961285a47b8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "ae4c4e8d84d63e00150cebbfea1772c6c964350ad32e8f4284a8dc8ffa129fc5",
      "content_summary": "不必；它允许按预算拆分，短prompt也可能一次完成。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-scheduling",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分启用分块预填充与实际发生多块"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-99d1339089861715964f1d78",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "21acb6f05d2b2d0659a5da3f626c3b61de7d5de7c09009e7aef3bb904a9094aa",
      "content_summary": "不会仅因抢占而终止；请求及生成历史保留，等待资源恢复。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-request-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分抢占与请求终止"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-af6f8b4a3928337d2ca0f814",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "7931087b9e02ff6c86c690b297979474fda2dbf6bbf7af9080e917418340b3f2",
      "content_summary": "不一定；被抢占的请求可以位于waiting队列，status仍为PREEMPTED。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-scheduling",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分waiting队列与preempted状态"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-48619be5e7dad94f709e6ca0",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "f397aa7ef4644c5e68c21b6c61a673131908ec2a541ebe3e6fadc6bff25194a3",
      "content_summary": "不是；还需要前端已经确定该请求结束。",
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
        "recall_target": "保留前端stop取消分支的外层条件"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7f6b889ffccb7afddf9fea5f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "87e0bd36bba05d883535f8ad68eb81a3dc10881e993b5ca07a49605b7efac84c",
      "content_summary": "不必；未结束的请求可以退出本步batch，同时保留本地缓存供后续恢复。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-device-state",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分runner请求缓存与当前执行batch"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-842ef50d7d3ce590a2b562fd",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "e8c13d295af76f83189b1a8c2a50d7c85f75a07b67ab28087a08da1831a71c29",
      "content_summary": "替换旧列表；恢复载荷表达恢复后的完整映射。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-device-state",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "识别恢复载荷对块表的替换语义"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-15d38c7ca8e263ccc79e1ad2",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "3c8d974d71acbce91088315fd7cb43511acc3ea34baa62ed5959ab8f71268ad5",
      "content_summary": "先定位逻辑块，再叠加块内偏移。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "paged-kv-addressing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "由请求位置和块表计算token槽位"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c1802344a7ebe74999d6ee69",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "e633114f11a97199fff0888ab613bdc8bdc80c93fcaa9424b1064606994c79e0",
      "content_summary": "直接决定新KV写到哪个槽位；历史上下文读取还依赖block table。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-attention-mapping",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分slot写入定位与块表历史读取"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f27bf5c68905845573007bb3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "5a0b254c1de40fefc062defe35eaa4b9605bfeb216df48100c5b84253b69eae4",
      "content_summary": "按请求排列的行要重排；每个请求行内的逻辑块映射可以不变。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-attention-mapping",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分块表行内顺序与batch行顺序"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-360a92513663a1e184c73081",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "2dc8a00a777275dd9a3a456c4380ab5e02ad56f6b7ac9264d4be5b8914472294",
      "content_summary": "前者是本步展平query的请求片段边界，后者是对应请求的序列长度。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-attention-metadata",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分本步query边界与总序列长度"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e48c0b5d4e3fdfff3a079a2b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "34d2c33a71e598d27cf8d3bfd9327e0c79bbc2ac6bb7b823a02e810da67118b8",
      "content_summary": "不能；同一批次计算不取消因果约束。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "causal-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "限定同一prefill片段内的因果可见范围"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a6c09dfcf93944cd2951b72d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "b3529c3764836838921566a44d42c5190c7e03d23cd7f5b44413529bcac79220",
      "content_summary": "不能仅凭shape判断；内容必须对应本步请求、长度和KV映射。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-attention-metadata",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "判断相同shape是否足以复用元数据内容"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-4dc2c29e8fcf8c04979b2598",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "377b98f42943068560726eb72e3d3c61658298cf44522f19fcd43177963226a5",
      "content_summary": "没有；还要追选定backend、运行条件、布局和底层绑定。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-backend-dispatch",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分统一attention入口与实际kernel"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-869c7b15dde8da8ad2b2baa1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "08ac21cfe61df33674e0d9edec60a1cf035def7859234f914e0975f66ca44728",
      "content_summary": "不能仅据此删除；它可表达KV更新先于Attention读取的编译依赖。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-compilation",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释非数值依赖参数的正确性用途"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-05890bf565adf8310a19569d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "b4218defac017f7449239284be733c1078c89443e259eb83780bb6c3360f7885",
      "content_summary": "不是；在所学分离路径中，后续调用sample_tokens取得完整执行输出。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-execution-contract",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释执行采样分离路径返回none的含义"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-fec55735844313fb603e37f7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "6c615ed02c9329a92dcd8b410f3f75547b8be9bdeb8a12a106b8e4225cca4d9d",
      "content_summary": "不是；所学分离路径中，它应用采样约束并真正进行采样。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-execution-contract",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分sample_tokens的计算职责与取回结果"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-2077ed6103d92ccddd84f0e1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "b619c707ed0c39efe8c0d66c74a4bc69d17458c10436c15daf2bb2462fbe3bc1",
      "content_summary": "每个请求通常选本步片段末行的hidden state计算生成logits。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-model-execution",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "定位普通请求生成logits所用的片段末行"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6e80586c21468b342811ed55",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "6ae7535a126b4c93fdc05dd446f42f1e9c25de665ad52eb1fb2179c953d352f3",
      "content_summary": "不需要；设备初始化属于启动阶段，本步经执行入口委托Runner。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-device-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分worker启动初始化与每步执行入口"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f726fd672421c50799332024",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "1e19580f0686ccf6619f95ac9a8feecd904b5182e386c7c3674e252f50a9bfb6",
      "content_summary": "EngineCore将执行结果交给Scheduler的结果更新逻辑回写和判停。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-execution-contract",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "识别core请求历史和停止状态的回写者"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c4305907da34210e2ff9a593",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "d1ff90d280223bc42ad9d1c91acd7e453086661bf5fbcc875a9d105a257def21",
      "content_summary": "在check_and_update_config中设置parallel_config.worker_cls。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-out-of-tree",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "定位platform自定义worker的接入点"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-704e23f2ac33a51b9d1cafc8",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "589a1084fc24a7319297ffc48f2fb12e44fbf3d28eeb0d44dc2c04854f791b58",
      "content_summary": "不会；Attention backend选择与Worker类配置是不同入口。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-out-of-tree",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分attention后端选择与worker选择"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a89805ae36fffe4b3d357833",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "1e4d2e936ee44e1d0854b7744734deccb1178f29f8c296f8a9714a286823005b",
      "content_summary": "不会；还要将对应vLLM模型算子调用路径接入该实现。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-custom-op",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分底层算子注册与vllm模型路径接入"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a30eed37a09de948f40c5e38",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "8f9e1aee14e18199323293479f49e886380e9c71afc0ec99a5f490bc6e43a418",
      "content_summary": "不是；它表示原生PyTorch组合，执行设备取决于tensor与具体实现。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-custom-op",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释forward_native的设备含义"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-209c99a69970415ab4a8fe1d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "a828a7ba5092e31efa4470c7e215e6c53c32a7b1d52706843a5f1b1e84ab6ccd",
      "content_summary": "不够；还需保持数学语义、tensor行为和执行依赖。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-out-of-tree",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分接入动作与替换正确性契约"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-fccc453bd4ab4941409e7bf9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "d5584580392887f37e9a497ea88b6a8ad9a9b561d4551b3420ac05a113c3692d",
      "content_summary": "错误地忽略子组的实现也可能通过；需要多个独立子组暴露跨组归约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "collective-correctness",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "识别只测试world通信组的盲区"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-45d3779fb6c0899ed56d4194",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "23135ac78c2f73e0be2a7149f935528bb23640f405f52fa7d2f4ed7629f22ef9",
      "content_summary": "不必；已有规格与页字节接口能准确表达时，应先在对应实现中兑现契约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-out-of-tree",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "判断padding差异何时不需要core修改"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-8cf820cd4a8ab0b43fbc3bd6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "dcad25b8f328e60a6608ec12395c3ed9f083171f738deb81574b705e8750cc8f",
      "content_summary": "证明需要的语义或保证无法通过现有字段、hook和机制表达。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "framework-extensibility",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "说明核心接口修改所需的证据"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5e59c8a2b0cca6fa8beb9e2a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "74e9b981d7d597dd7413a10cc61c7e97000966d8f34e4aeeca9cb1df3f829128",
      "content_summary": "计算未padding、无额外元数据的单层有效KV字节数，并明确每元素字节数s。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "kv-memory-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "计算普通全注意力每token的kv字节"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1e35d3d80a0dc7e8e4785c53",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "5e62e423418a576d3b8b216f5aa6cbacbc837e5748893ea477330df662511653",
      "content_summary": "不是；前者来自请求未填满逻辑块，后者来自物理布局/跨度的额外占用。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "kv-memory-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分末块空槽与物理页padding"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-602b377049f84ba5753f398a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "a4f5fe543e5be29b58f83bf48c0c5bbd0b6d5e40be2571cfaa522515bc15a3c0",
      "content_summary": "不能这样推断；页跨度、基址对齐和分配器取整是不同约束。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "memory-alignment",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分页跨度与分配器最小粒度"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-caa30e7923ecbc5638183da4",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "3952d07162417a3f024c23e5d588c5af49023a811a2c88988490f936945a7dfb",
      "content_summary": "不可以；每个请求独立占用自己的末块，应分别向上取整再求和。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "kv-memory-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "计算无共享多请求的kv块数"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-284dc7300b3aedb48fb0e420",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "21aec4170f6f3bc2bd5faf02baa251f1bf2856986617c23bb6db720453f1f708",
      "content_summary": "不是；是5个pool ID对应160个单层物理页。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "kv-memory-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分pool块id数量与跨层物理页数"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6e05afd30a1c350d2df82072",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "068c7af197b38579014738055787e968533555af5242765f7d0947d67ab8f149",
      "content_summary": "不能；只解除R的引用，S的存活引用仍保护该块。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "kv-block-lifetime",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "判断共享块何时可以重新分配"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7e660bc46d36e9c0cfc24dbe",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "c4b4ffa5681706b34e998b9c900d4ecb6013f61996c3f324014e55cdd39c58e8",
      "content_summary": "可以；可再命中复用，也可在淘汰旧缓存标识后用于其他内容。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-prefix-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释零引用缓存块与空闲队列的重叠"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a72685e9c1eb7ad97aed8c54",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "9bf2b43be91a27be8975edcefccb0151cfc17c9b9f4e76aa0c2179385f3ed613",
      "content_summary": "不一定；后续容量检查失败时尚未正式引用，成功路径才touch。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-prefix-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分缓存查询命中与正式取得引用"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-0ab4415e85e63ef091d12815",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "35111e9997b409c5db1e21116253778dc5093bd5271f4bce618be63e0ec0ea2b",
      "content_summary": "不一定；末块仍有空槽位时，本步可以无需新增块。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "kv-memory-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "判断空闲块耗尽后尾槽可用性"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-0178da19052b31ed9413b152",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "0427f7305c509361fc35467547ab176d73c45acc72d1060d4df417dd83614986",
      "content_summary": "不能只凭当前块token判断；链式hash还包含父块身份及额外键。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-prefix-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释前缀hash包含父块身份的原因"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3afc59e30aebf237c71c5ed1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "bfab44098010bf41f9cc15806d8b9b1e387ba75a13d522a730289defcbb0ef77",
      "content_summary": "不证明；它限制允许共享的范围，即使数值可能相同也不跨域复用。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-prefix-cache",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分缓存salt隔离与kv数值差异"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-8f0f7a7e25dc774f917af791",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "098066f0bf1423c4c37923ba48f2f8b12770feb9173e8baa4c1da1d4602b4378",
      "content_summary": "命中带来的延迟差异可能暴露某段前缀是否已在缓存的统计线索。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "prefix-cache-security",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释前缀缓存命中的时间侧信道风险"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-2d44e22b6d9485325f8972b5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "e30222f1c443bfd5d713ccee7d2476cb459eb50456ac134a6d3d7e98ed4c0ed8",
      "content_summary": "会减少或消除这些请求之间的前缀缓存复用机会。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "prefix-cache-security",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释可信范围内salt保持稳定的作用"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-80ae6e0f740e097b9da41829",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "7c95ee1ef9e36e86318b683641bc477591dc5d0a4bf5d11420435f0022d34f62",
      "content_summary": "不会；分页访问与跨请求复用已计算前缀是不同功能。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "paged-kv-cache",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分分页访问与跨请求前缀复用"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-41e581d77f242691d8a14b70",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "9991b9a081b3f6765c9fcd31c44bf300396cf3bae527d3428e83a5eee236ddef",
      "content_summary": "不必；省下的池内容量可以留给后续请求，预分配tensor仍保持。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "kv-memory-accounting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分活跃块占用与预分配池大小"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d72838bb6579b9ace4af9cd9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "fa7ffa0b0a46363fd5a15633975ae08789a4edaef6535d99ba530a3bdec29450",
      "content_summary": "不能；字节粒度与token分块单位不同，还要结合dtype、head维度、布局和kernel设计。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "hardware-layout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分搬运字节粒度与逻辑token块大小"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-462e2917ea13b46bfbaa040e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "ca39c7505f1ad56d7f9450b6110d31f2d9ca4c25e4102a9b2d7684835ea90a4e",
      "content_summary": "不能只换getter；原字段还用于逻辑tensor字节数反推块数，需一起调整消费者。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-cl-kv-layout",
        "fact_scope": {
          "commit": "4fd99a4f21d720347c6dec54253504f8321c0437",
          "kind": "snapshot",
          "product": "vllm-cl"
        },
        "recall_target": "解释统一页大小字段时的消费者重构要求"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a9fb9ea14c6d107bbf23d539",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "fe77ae49cd0c2d4eabd8aaae50cf5822ce7a3364f6471233ca900eb86848817c",
      "content_summary": "在前端；Core仍逐步回传内部结果，前端暂不交付中间RequestOutput。",
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
        "recall_target": "定位final-only抑制中间输出的层次"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c0e72e196678952189509127",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "041b20b109260248170dbfa02757305e4575908405df1f7c58ccb411629c83b7",
      "content_summary": "DELTA只包含新增生成内容；CUMULATIVE包含截至当前的累计生成内容。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-output-processing",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分增量输出与累计输出的交付范围"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-73a6eeefde047dc3f11e9f7d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "767a1bd947c031ce9081346570100a01153093eba8f2f693469339a0e44c99a5",
      "content_summary": "不是；这里的异步生成器从Collector消费RequestOutput，再向上yield。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-output-processing",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "解释asyncllm生成器的输出消费职责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-b13b06cdaf66c20fbc1b730e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "a065a82884530624f02fa9db2e6e2eb052f4e531501e8806ef13f19337b7da73",
      "content_summary": "可以；最终结果先放入Collector，generate仍持有它并能继续消费。",
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
        "recall_target": "区分requeststate注销与collector消费生命周期"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-83bf809ee49d5864f0049a85",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "cf50daac9bac2f85c75389a15708279e4c5b86ff259c3769481d2e82125f503b",
      "content_summary": "不能；调度侧已解除引用，Runner只清自己的请求和batch状态。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-kv-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "识别终止请求的kv引用回收所有者"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-b94314f0d50a23dcab697cc7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "7ca0ec4e19955c18d9a01bc5dd690c3f3b662175808f3340c3971d06eac69cd3",
      "content_summary": "移除结束请求的本地缓存状态与InputBatch成员，维护后续请求映射。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-device-state",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "识别runner收到结束id后清理的对象"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-ac522a78ed1ae6861706a904",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "0a70089f9aa4ad9f55e1c7cf51878f47f1979fbea6c8c35ac516f6ded621c703",
      "content_summary": "不必；两条后续路径没有这个互等要求。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-request-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分最终输出交付与runner清理的依赖"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c9e64adaf431ebe5c519d83f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "65d3f7117728be67f5e0e8b262b7a1d0b0c0725b165cb613fb4695b143cae2f3",
      "content_summary": "仍可清理；所学路径先更新状态，再判断是否跳过forward。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "vllm-device-state",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "识别零计算调度仍可驱动状态清理"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3330df6c801eb8afb0c4a4d1",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "90d8702d3d554b3d9e0030f09fef4f590c753835c9c9ba33da2ec49309633e5b",
      "content_summary": "向尚未结束的Core发送ABORT；对用户仍可报告stop。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-request-lifecycle",
        "fact_scope": {
          "commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
          "kind": "snapshot",
          "product": "vllm",
          "version": "v0.26.0"
        },
        "recall_target": "区分用户stop原因与发送core的取消操作"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-58f9377a4e5513c61f851abc",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.0.0"
    }
  ],
  "managed_body_sha256": "4c243a4828bd83d84d828982a8aa5e9f81be6ca9c64f67e290ea2cdd2a6d0099",
  "manifest_payload_sha256": "6b1108c1b32b83f73b7f8929d7600969b6db3d2d3ac34fd74b55df80e1d20031",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 9374,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/vllm-full-session-review-correction.xlsx",
      "row_count": 10,
      "rows": [
        {
          "content_sha256": "c7e1a979c99aa5a83e869fd013ed16ae55097354a1b1a25f3f35b0f1d052f9a4",
          "logical_id": "mc-405fa0e547ffb00ee0743601",
          "row_sha256": "66ac5456c28443a999c11b14d0b23d8f08b4837c59b04821eeababa6367369be"
        },
        {
          "content_sha256": "9560a630fdf1de47ca14000edafe43027d55db3fef81039594032ff2d84d2571",
          "logical_id": "mc-e1d5350c48cf8fd0d15afdce",
          "row_sha256": "f8012bfea894e732adf5525dbef81e43b22b7e2948197645ff36950f2eeae5f7"
        },
        {
          "content_sha256": "f397aa7ef4644c5e68c21b6c61a673131908ec2a541ebe3e6fadc6bff25194a3",
          "logical_id": "mc-7f6b889ffccb7afddf9fea5f",
          "row_sha256": "9060844e23ac38b5f5f24accdba25ad23329f61622b350d00eb2870e7fd4dbfa"
        },
        {
          "content_sha256": "e633114f11a97199fff0888ab613bdc8bdc80c93fcaa9424b1064606994c79e0",
          "logical_id": "mc-f27bf5c68905845573007bb3",
          "row_sha256": "0ab2717f1fd3919b1acb41726cd6261ac24183f02ab113f2dc994d2037c19c3b"
        },
        {
          "content_sha256": "6ae7535a126b4c93fdc05dd446f42f1e9c25de665ad52eb1fb2179c953d352f3",
          "logical_id": "mc-f726fd672421c50799332024",
          "row_sha256": "1c055d254ed829a9e0f1aa5c210dbe12bdf4eb20b731d6929f8d80266fe6f2ef"
        },
        {
          "content_sha256": "a828a7ba5092e31efa4470c7e215e6c53c32a7b1d52706843a5f1b1e84ab6ccd",
          "logical_id": "mc-fccc453bd4ab4941409e7bf9",
          "row_sha256": "7d2dfd79ca289ca5a42da09b4bb65f592353dc96eb550e4862439ab330115444"
        },
        {
          "content_sha256": "fe77ae49cd0c2d4eabd8aaae50cf5822ce7a3364f6471233ca900eb86848817c",
          "logical_id": "mc-c0e72e196678952189509127",
          "row_sha256": "be8e2239bb7107b2776424f55d7a0d67eb9a47486c43b2f78b35b43d326bfd39"
        },
        {
          "content_sha256": "a065a82884530624f02fa9db2e6e2eb052f4e531501e8806ef13f19337b7da73",
          "logical_id": "mc-83bf809ee49d5864f0049a85",
          "row_sha256": "f213d2c8cb3ff141acf5e40d1c1286903c9c2276f200a5aa666bd7633b7d44b1"
        },
        {
          "content_sha256": "cf50daac9bac2f85c75389a15708279e4c5b86ff259c3769481d2e82125f503b",
          "logical_id": "mc-b94314f0d50a23dcab697cc7",
          "row_sha256": "fce8e95f39a33a59dfe291a9d113ff12e1882ff8fbf633ef63c82046a167c18d"
        },
        {
          "content_sha256": "90d8702d3d554b3d9e0030f09fef4f590c753835c9c9ba33da2ec49309633e5b",
          "logical_id": "mc-58f9377a4e5513c61f851abc",
          "row_sha256": "aaa16e23b485479ae0ca67745264c8cefe40fb0b9f4d62dd82642bbe9dcc0ec1"
        }
      ],
      "sha256": "4bf45d4dbcdef5db81403812f8f9751061df4df93be51d23a4142d1efaf0747c",
      "sheet_name": "cards",
      "table_sha256": "1f53dbf47b09d555792499ec8e2c260d6c81c838621d2addafe0c09c2edbac9f",
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "byte_size": 40386,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/vllm-full-session-review-technical-qa.xlsx",
      "row_count": 66,
      "rows": [
        {
          "content_sha256": "164e5905245930f35cb43bb80526d3b4d35a2f13e009310e31dc8855392063f4",
          "logical_id": "mc-a4cd934451dbc2f674b835a9",
          "row_sha256": "b8706cc22232a82c7a19e6eec8095497bbd151ffc353e1328f3195b8b20896ae"
        },
        {
          "content_sha256": "17a5275718f87ea6ea0a148eef7d0034feb101aed30c39b99cb898777f06b0b5",
          "logical_id": "mc-d90a8a49188317c4475bb1fa",
          "row_sha256": "f4795761f14c8a77bb4a0a8784ca29df7960b579de809066c35934cff1e1fa4b"
        },
        {
          "content_sha256": "ab6cdb0458a51ef2b47ce222d801ef098b217feadb7d0f70cf516f7d6c5fe1c2",
          "logical_id": "mc-b5ab4a7997b4428cc78802e8",
          "row_sha256": "0303a3819d6eb3a530276530515d84de8bb8f7a7ef3629f81bb1667cdfd9761c"
        },
        {
          "content_sha256": "e3a9b6b577c47c521ac142b1738be17c9698b61d6d198d69936799477902ac59",
          "logical_id": "mc-abe7eb24831612c9c3d4eef7",
          "row_sha256": "f759ecd9bcbcc2c0ef6935e1b85abc78b9aa97505731adf44b6cd4d35ac2532a"
        },
        {
          "content_sha256": "6eb0f3500ffadd113af1515bf9481836b944ede21f6ddb2db0da7c5136d1e0e8",
          "logical_id": "mc-84676054f06c3224f8b9d42a",
          "row_sha256": "be5f903f07a0b0cd334e20bfe7673a3cc90a929a36bbf2910a0536b4f09bcc6a"
        },
        {
          "content_sha256": "6a78722409c088339d455c0f47cb661c01e732f6c69f67cdb3c032a45d1d795e",
          "logical_id": "mc-386eff0e70f84976785adb7b",
          "row_sha256": "fad1203d541a9ca8eafd1dd6a387da64e39607f44f0b0e6cf1951a3f703755ab"
        },
        {
          "content_sha256": "c44bd89a35334c96236cf1f63a69d9010472e7fcff8b80a0dc889a656db9de68",
          "logical_id": "mc-c44b4d7a9ac36edd8c5dca77",
          "row_sha256": "9e477231405058b79a460a86ecbce2d110f73de1b2006d0d3c729d7cd0ba1dab"
        },
        {
          "content_sha256": "bf6c0b626882396ceeea9e9bcca4cfd7681dea0d25c2d225a0d0e1ddcde8224a",
          "logical_id": "mc-1ba245772d63b1465ff84b74",
          "row_sha256": "4993e4ca2f08d4364de8fff20ca29cbc4e8c6b986b33b6aae72b37802b73c8df"
        },
        {
          "content_sha256": "874b00853e459fcf8e4abcf57365306be523d80ec66ba55f3d7f0f019a267cc9",
          "logical_id": "mc-ce38809b2547d6c1f70c85f7",
          "row_sha256": "03679b5579ee78c053ee70529581865e740c5ec0952dfb0d72fa954d8555e0c8"
        },
        {
          "content_sha256": "a3c271f502e5ce9db4f1c49f3833bed7e953cab8b60411662c9d15aba01e306b",
          "logical_id": "mc-bdb5ae3a65636b17a13e73b1",
          "row_sha256": "a2e1a897a874e1e00a8a454e78f8c691e299f672a67c14b6ff5b7925c41b9620"
        },
        {
          "content_sha256": "4238e45408b36fb87445296e4313781ea31b18b1a9a4b616d8bfde09013bf0e8",
          "logical_id": "mc-9d7b2af6315be86cc53562e2",
          "row_sha256": "e8edb6e4f82f5fb3362d0b78610d795830b9b9262d3f5b96e206df477ccb5c91"
        },
        {
          "content_sha256": "860d883002d0b0c680a061df1aa41a6c15249de549a874e60376014be9d64fa8",
          "logical_id": "mc-81771102328bc5e96dde9dc2",
          "row_sha256": "88c1b777bb0de5ac55f756d6603ea252a69d8377dd331eef69f218d55dd203d7"
        },
        {
          "content_sha256": "5ed87699915e6bfba062e71ce129480fe0d61e78b077d99c69be1590452850a2",
          "logical_id": "mc-7552190fc19fef1335707b7d",
          "row_sha256": "752dccada2df9c86bd51ccea5d4ce23d476d2ef996210275f920fb6010c3ab6f"
        },
        {
          "content_sha256": "1b89062283c94c4459c60db93fc79db6e13cabdc1ccab2b0a5efe36593f99154",
          "logical_id": "mc-ae376a7b1a41d3c8475527c6",
          "row_sha256": "054a33e543ee680f3b68cb4488493adaa154093e90a17823944064762d68a429"
        },
        {
          "content_sha256": "09c9abaeb12eb8fde5710040b929a31cfab871a3387244045548712572f37d97",
          "logical_id": "mc-2731ed1a964329bd32e1ea08",
          "row_sha256": "5c6af00ac49dc47ca6d9aaa7d338d0ed8010e7329a934a51bac884ee6ee8e4ca"
        },
        {
          "content_sha256": "4b32d1bf9f3cc3190965aad86c3091ff906b7226fb18ccdbf5c74197fb851c8a",
          "logical_id": "mc-c34a6067dd76a7d3dbf5a43c",
          "row_sha256": "12c83f286601ed4bc456afc72d3296a6ed7d35c28c8f64d2c554c2176cbcb2b9"
        },
        {
          "content_sha256": "49e8537a3a5411639b09fc5228fea9b371621bdade7dc71686a683a4a7739ffe",
          "logical_id": "mc-34b6be82985ed08c4270ddd5",
          "row_sha256": "6e22298a3baa5f8500689180a9935318c20222c4e31651f570a580fb4881c5d9"
        },
        {
          "content_sha256": "d30b24aad1cae4723da1ec3f1c93cda0f8f49318ecfa9146ee401924b4332c5f",
          "logical_id": "mc-50591c6d88488ddba1e419c9",
          "row_sha256": "74b149c07918a056210e2892bb1f567bd669c89f8ff7e28bbeb9085256802ae2"
        },
        {
          "content_sha256": "be2e95c76ce6c700d407ddd04aaf4599b90c1758f71954fda33ae24d86e5c0a3",
          "logical_id": "mc-79362f0684e9a30fd97821f9",
          "row_sha256": "424842411163dd8ee6d8d0d9b5386d308f7afe6224b18806a45a9cbbca2cddc0"
        },
        {
          "content_sha256": "427bc70305460cfbe324f2f94dc471d81f637353d7525ad530244e7ebb0ba196",
          "logical_id": "mc-485fa8cafc3816acbd51e03b",
          "row_sha256": "1b3cb1a84334895552c69d4f67fa23b0d03276dbf4ab2671e0cea0eb46135cf0"
        },
        {
          "content_sha256": "c6e60140da015603e8a282cc05a6dda9497d221a842ca78d6abc69686a495948",
          "logical_id": "mc-7ab1103a71067961285a47b8",
          "row_sha256": "24a86ac711fdce64be0941bd22c5b497f2c014beaded52d832b1be9b3745c46e"
        },
        {
          "content_sha256": "ae4c4e8d84d63e00150cebbfea1772c6c964350ad32e8f4284a8dc8ffa129fc5",
          "logical_id": "mc-99d1339089861715964f1d78",
          "row_sha256": "b6ab79f63ed2fe3ae72662eeda3b075763c6b5a503c2b579d5e14a48dab90599"
        },
        {
          "content_sha256": "21acb6f05d2b2d0659a5da3f626c3b61de7d5de7c09009e7aef3bb904a9094aa",
          "logical_id": "mc-af6f8b4a3928337d2ca0f814",
          "row_sha256": "d8761f146ba8146492deda9fd6e324ce3033b27ed3efd96ee1a0829596ac58b1"
        },
        {
          "content_sha256": "7931087b9e02ff6c86c690b297979474fda2dbf6bbf7af9080e917418340b3f2",
          "logical_id": "mc-48619be5e7dad94f709e6ca0",
          "row_sha256": "0925a7bcbe9e929fe333bcf4250dfb2edc2907558403605b82ec2a41bdbde604"
        },
        {
          "content_sha256": "87e0bd36bba05d883535f8ad68eb81a3dc10881e993b5ca07a49605b7efac84c",
          "logical_id": "mc-842ef50d7d3ce590a2b562fd",
          "row_sha256": "4f498949d85d84c2c0bb7037f09da11d44bfcebd71ed53aa36d58849dea4315c"
        },
        {
          "content_sha256": "e8c13d295af76f83189b1a8c2a50d7c85f75a07b67ab28087a08da1831a71c29",
          "logical_id": "mc-15d38c7ca8e263ccc79e1ad2",
          "row_sha256": "f8714d71ae5ba1b0d8a6944bfcab0779e175638a5494355b92cd5e62de6e0eab"
        },
        {
          "content_sha256": "3c8d974d71acbce91088315fd7cb43511acc3ea34baa62ed5959ab8f71268ad5",
          "logical_id": "mc-c1802344a7ebe74999d6ee69",
          "row_sha256": "4d1b90f780414b06047b11f3bae3c9238610fd8b65354ef006bea8cfce710b20"
        },
        {
          "content_sha256": "5a0b254c1de40fefc062defe35eaa4b9605bfeb216df48100c5b84253b69eae4",
          "logical_id": "mc-360a92513663a1e184c73081",
          "row_sha256": "3f2341e1ad4d21021dd81a4aedd1b16ec5b49bff0a33a9aa6a9d36e243f23b86"
        },
        {
          "content_sha256": "2dc8a00a777275dd9a3a456c4380ab5e02ad56f6b7ac9264d4be5b8914472294",
          "logical_id": "mc-e48c0b5d4e3fdfff3a079a2b",
          "row_sha256": "9bd8a649e41a8c37b14d0f90c54b506998ef293403f9be226908614621c16a5b"
        },
        {
          "content_sha256": "34d2c33a71e598d27cf8d3bfd9327e0c79bbc2ac6bb7b823a02e810da67118b8",
          "logical_id": "mc-a6c09dfcf93944cd2951b72d",
          "row_sha256": "4eb01cec59808ba72ad9ebc95b94b168668eca1c4533d828b9322a4e97e60c3b"
        },
        {
          "content_sha256": "b3529c3764836838921566a44d42c5190c7e03d23cd7f5b44413529bcac79220",
          "logical_id": "mc-4dc2c29e8fcf8c04979b2598",
          "row_sha256": "b4be858b646bc269d1603a72dabed4aa5fde9b7e5b10cb0f09157b9ba9376ac3"
        },
        {
          "content_sha256": "377b98f42943068560726eb72e3d3c61658298cf44522f19fcd43177963226a5",
          "logical_id": "mc-869c7b15dde8da8ad2b2baa1",
          "row_sha256": "0370adc8ef5d783eea7f5f74b3cce6ad024d26c9509e75bb905e09548fc6927a"
        },
        {
          "content_sha256": "08ac21cfe61df33674e0d9edec60a1cf035def7859234f914e0975f66ca44728",
          "logical_id": "mc-05890bf565adf8310a19569d",
          "row_sha256": "caa5633ce757a5907e71aea2c463ce8d53e21a8f176d4d785b02870ba9dbf9b6"
        },
        {
          "content_sha256": "b4218defac017f7449239284be733c1078c89443e259eb83780bb6c3360f7885",
          "logical_id": "mc-fec55735844313fb603e37f7",
          "row_sha256": "efd7f21f492db28edfb597234ec0e9b72c14c70eba4b1f5327b2eef01ff72377"
        },
        {
          "content_sha256": "6c615ed02c9329a92dcd8b410f3f75547b8be9bdeb8a12a106b8e4225cca4d9d",
          "logical_id": "mc-2077ed6103d92ccddd84f0e1",
          "row_sha256": "311818f9407bb2024715ddb20cfe8e6cd18f8b8dae163dba8949ccbbc394fa28"
        },
        {
          "content_sha256": "b619c707ed0c39efe8c0d66c74a4bc69d17458c10436c15daf2bb2462fbe3bc1",
          "logical_id": "mc-6e80586c21468b342811ed55",
          "row_sha256": "10f06d412fcc2bb1506631421bb98ef2e3a17a0adaf860df142f118b94be40eb"
        },
        {
          "content_sha256": "1e19580f0686ccf6619f95ac9a8feecd904b5182e386c7c3674e252f50a9bfb6",
          "logical_id": "mc-c4305907da34210e2ff9a593",
          "row_sha256": "905f95efa53de290b2ec0108829cdf263e7762bc614ff6c93174e40da683b181"
        },
        {
          "content_sha256": "d1ff90d280223bc42ad9d1c91acd7e453086661bf5fbcc875a9d105a257def21",
          "logical_id": "mc-704e23f2ac33a51b9d1cafc8",
          "row_sha256": "0619e1814a7b25997cd81fd72f49d9327d6a55277612db646409fbd5532b4cc5"
        },
        {
          "content_sha256": "589a1084fc24a7319297ffc48f2fb12e44fbf3d28eeb0d44dc2c04854f791b58",
          "logical_id": "mc-a89805ae36fffe4b3d357833",
          "row_sha256": "28f43784b70459077c9c6094bb29e96d5c391cdb0f64adba29ab607f29c219bc"
        },
        {
          "content_sha256": "1e4d2e936ee44e1d0854b7744734deccb1178f29f8c296f8a9714a286823005b",
          "logical_id": "mc-a30eed37a09de948f40c5e38",
          "row_sha256": "5c4ea5f636c72f695b6369ba5642594b13caf5218532e78e70db3ff87bb6df60"
        },
        {
          "content_sha256": "8f9e1aee14e18199323293479f49e886380e9c71afc0ec99a5f490bc6e43a418",
          "logical_id": "mc-209c99a69970415ab4a8fe1d",
          "row_sha256": "c53875fc3accfbc571ce6250936a13bfa3b0cf0349a1af7b96c6381952e15f39"
        },
        {
          "content_sha256": "d5584580392887f37e9a497ea88b6a8ad9a9b561d4551b3420ac05a113c3692d",
          "logical_id": "mc-45d3779fb6c0899ed56d4194",
          "row_sha256": "f52e4af89e79f0b88f819e2ee9a592f6e97d775f46cbe774e297c127a507a1c3"
        },
        {
          "content_sha256": "23135ac78c2f73e0be2a7149f935528bb23640f405f52fa7d2f4ed7629f22ef9",
          "logical_id": "mc-8cf820cd4a8ab0b43fbc3bd6",
          "row_sha256": "55be9e878b6ee1bf78fc12c15c6bbb6306d60d16e7c1c8bc97f47691188ec17e"
        },
        {
          "content_sha256": "dcad25b8f328e60a6608ec12395c3ed9f083171f738deb81574b705e8750cc8f",
          "logical_id": "mc-5e59c8a2b0cca6fa8beb9e2a",
          "row_sha256": "5f3a3d4bc4100f32c0f02cca6b290e99f8eb745dbc0edc93ac68c845648ae21b"
        },
        {
          "content_sha256": "74e9b981d7d597dd7413a10cc61c7e97000966d8f34e4aeeca9cb1df3f829128",
          "logical_id": "mc-1e35d3d80a0dc7e8e4785c53",
          "row_sha256": "2906b9ed02b47d5712fb126453af601afba84caff9bf057dc9293d3e73448d05"
        },
        {
          "content_sha256": "5e62e423418a576d3b8b216f5aa6cbacbc837e5748893ea477330df662511653",
          "logical_id": "mc-602b377049f84ba5753f398a",
          "row_sha256": "b780c18cd9966824b5657aba9650ce11f3a8f0eaab17aae98a299f931bf878f1"
        },
        {
          "content_sha256": "a4f5fe543e5be29b58f83bf48c0c5bbd0b6d5e40be2571cfaa522515bc15a3c0",
          "logical_id": "mc-caa30e7923ecbc5638183da4",
          "row_sha256": "5dfd6a54847ebd6051ca84d66cdac7840188e2de2c73e50c2f5cdfa7acf83927"
        },
        {
          "content_sha256": "3952d07162417a3f024c23e5d588c5af49023a811a2c88988490f936945a7dfb",
          "logical_id": "mc-284dc7300b3aedb48fb0e420",
          "row_sha256": "5e93fa136e90cd635a838ecf070bf00d211f16d4e6af810783fd0641c0a55a3e"
        },
        {
          "content_sha256": "21aec4170f6f3bc2bd5faf02baa251f1bf2856986617c23bb6db720453f1f708",
          "logical_id": "mc-6e05afd30a1c350d2df82072",
          "row_sha256": "e52268c404be3cf7761d34a29d15ff889608e19027c619a7a969e0e7f9f55f39"
        },
        {
          "content_sha256": "068c7af197b38579014738055787e968533555af5242765f7d0947d67ab8f149",
          "logical_id": "mc-7e660bc46d36e9c0cfc24dbe",
          "row_sha256": "7461b164736a899d2ec91e484cf5c39e752c3258d8e547fb611b9acdd71f5f16"
        },
        {
          "content_sha256": "c4b4ffa5681706b34e998b9c900d4ecb6013f61996c3f324014e55cdd39c58e8",
          "logical_id": "mc-a72685e9c1eb7ad97aed8c54",
          "row_sha256": "04b097a9dfbed1d550153cd3a49974da3a1c40002a79be80560cbbdc45f57105"
        },
        {
          "content_sha256": "9bf2b43be91a27be8975edcefccb0151cfc17c9b9f4e76aa0c2179385f3ed613",
          "logical_id": "mc-0ab4415e85e63ef091d12815",
          "row_sha256": "349c224966ca37d97b8d80d5910c2eddef35e1d876caf9e58af9850bd409da27"
        },
        {
          "content_sha256": "35111e9997b409c5db1e21116253778dc5093bd5271f4bce618be63e0ec0ea2b",
          "logical_id": "mc-0178da19052b31ed9413b152",
          "row_sha256": "fc98f6482596cb52682da594ff1a220ea1d2a71c7977161db37a0ce43c233726"
        },
        {
          "content_sha256": "0427f7305c509361fc35467547ab176d73c45acc72d1060d4df417dd83614986",
          "logical_id": "mc-3afc59e30aebf237c71c5ed1",
          "row_sha256": "f01ffe1476a905f6f920fab67bb85b2fa436908371fdba99d33506eb0c0b65ee"
        },
        {
          "content_sha256": "bfab44098010bf41f9cc15806d8b9b1e387ba75a13d522a730289defcbb0ef77",
          "logical_id": "mc-8f0f7a7e25dc774f917af791",
          "row_sha256": "74dbce1e69ddc160082f264f3bb97ea7831d082a6ced53a3dc5473338503598d"
        },
        {
          "content_sha256": "098066f0bf1423c4c37923ba48f2f8b12770feb9173e8baa4c1da1d4602b4378",
          "logical_id": "mc-2d44e22b6d9485325f8972b5",
          "row_sha256": "e3e8a32f1bf2b9234679698361fdd9e93f866bbafab0234e63cd76af30f2abcd"
        },
        {
          "content_sha256": "e30222f1c443bfd5d713ccee7d2476cb459eb50456ac134a6d3d7e98ed4c0ed8",
          "logical_id": "mc-80ae6e0f740e097b9da41829",
          "row_sha256": "6d0311676c3a5f20b0fd5d97f428e66e1b6f9056dd712d58c5aec65b46e3fb9f"
        },
        {
          "content_sha256": "7c95ee1ef9e36e86318b683641bc477591dc5d0a4bf5d11420435f0022d34f62",
          "logical_id": "mc-41e581d77f242691d8a14b70",
          "row_sha256": "eb6c0ac4bd39771da40c128b4697bde24c6e83588d7b266d4ad9bbeff6321a0d"
        },
        {
          "content_sha256": "9991b9a081b3f6765c9fcd31c44bf300396cf3bae527d3428e83a5eee236ddef",
          "logical_id": "mc-d72838bb6579b9ace4af9cd9",
          "row_sha256": "e2c93ba1b0846654b488e108ba39290e2cb34fc70690719675d3c77803bfbcfb"
        },
        {
          "content_sha256": "fa7ffa0b0a46363fd5a15633975ae08789a4edaef6535d99ba530a3bdec29450",
          "logical_id": "mc-462e2917ea13b46bfbaa040e",
          "row_sha256": "3277fe0002286c33925faf94ce508663d03b2f4e59b423052159e13f7daff5fb"
        },
        {
          "content_sha256": "ca39c7505f1ad56d7f9450b6110d31f2d9ca4c25e4102a9b2d7684835ea90a4e",
          "logical_id": "mc-a9fb9ea14c6d107bbf23d539",
          "row_sha256": "dc5bca4bafd03c6518c6f62b55f089cd9a9e11cae73062aecd7f1d9e977f820b"
        },
        {
          "content_sha256": "041b20b109260248170dbfa02757305e4575908405df1f7c58ccb411629c83b7",
          "logical_id": "mc-73a6eeefde047dc3f11e9f7d",
          "row_sha256": "585dc6e1934fb42f0d7b8c3eb7f2cf58b5eef4fb6972e488f376f7879a7f4334"
        },
        {
          "content_sha256": "767a1bd947c031ce9081346570100a01153093eba8f2f693469339a0e44c99a5",
          "logical_id": "mc-b13b06cdaf66c20fbc1b730e",
          "row_sha256": "01ba085d77b6f40ccce1b19df916108bcf960f0789eea03afd7ee289ee1b3fb0"
        },
        {
          "content_sha256": "7ca0ec4e19955c18d9a01bc5dd690c3f3b662175808f3340c3971d06eac69cd3",
          "logical_id": "mc-ac522a78ed1ae6861706a904",
          "row_sha256": "e3d91ae98011972bfe2fe5d83cacd8d22f69d2a10328a41f2624389461af275f"
        },
        {
          "content_sha256": "0a70089f9aa4ad9f55e1c7cf51878f47f1979fbea6c8c35ac516f6ded621c703",
          "logical_id": "mc-c9e64adaf431ebe5c519d83f",
          "row_sha256": "1fb0a1d485ab20a2b85aceb5fa5a5466025b6a12dd1a02fdaa8501c7f103695b"
        },
        {
          "content_sha256": "65d3f7117728be67f5e0e8b262b7a1d0b0c0725b165cb613fb4695b143cae2f3",
          "logical_id": "mc-3330df6c801eb8afb0c4a4d1",
          "row_sha256": "5afb152ea6d5762557af603c80381d9331e91c0a78c66a4b14ca99ed8983129d"
        }
      ],
      "sha256": "7dc8a197cec51a7038597e7c77a4daaa736f9c59387e429c76ef2ae4401576ac",
      "sheet_name": "cards",
      "table_sha256": "0f0f4e4fcc354bb8d7d9fbf43ded6ba11f9002f8609a7d7af123cf0c6fbc7489",
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    }
  ],
  "source_fingerprint": "b43757c361efaa58c8d088c371a91218f63774be9127aa81332f5b7d95680c00",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "full-session-structured",
      "path": "推理框架/log/2026-09-08-vllm-full-session-review.md",
      "sha256": "457f9c4866494dd20436d57609b7e488b5a8ab2904c332861ee267c17ad43ebe",
      "summary": "全根会话324条可见消息的结构化复盘；含真实用户纠错、导师纠偏归因、固定版本知识与未验证边界。"
    }
  ],
  "target_collection": "inference-cards",
  "template_registry_sha256": "d6cdcd90c996ca6922a06f02a44b06800468a557bec6ad5c433511d7b57761d7",
  "template_registry_version": "1.0.0"
}
---
# Markji 表格导入卡片

> Markdown 保留受管元数据与模板定义；卡片数据请使用下列按模板拆分的 XLSX 文件导入。

## 真实错误纠错卡

模板 `correction@1.0.0`：

```text
[P#H1#{{意图}}]
📍 [T#!939393#{{场景}}]
---
✅ [T#B,!36b59d#{{正确}}]
❌ [T#!c6413a#{{错误}}]
{{说明}}
```

导入文件：[vllm-full-session-review-correction.xlsx](vllm-full-session-review-correction.xlsx)（10 张卡）

## 技术问答卡

模板 `technical-qa@1.0.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[vllm-full-session-review-technical-qa.xlsx](vllm-full-session-review-technical-qa.xlsx)（66 张卡）
