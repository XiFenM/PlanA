---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "2a5fc608779da0e1c70b323a7443111a5abb682bb641d68408c6e8bec7aa37d8",
  "candidate_sha256": "54f7197685dcec7c0022fbbbd68c43b57c152dc156560c8ca947fcde4de5cb17",
  "cards": [
    {
      "content_sha256": "ef8cdf0ec4ed40333ac47dc8cc8660084383df2ea14c4c7f95b4beb113c89b79",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fc2e2356098fb81ea26a1ae4eca069d61818fa19508cd87c6599ea5ab66c796a",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ecf9f7b621703fda136e24af7b330c18996556b174fdb31a24de371e14dcc8f2",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "89053c3446fef9f964631d8a03b7bce731d03d470cd0c57551e3a5ff914ab812",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d3e2bf04bd7746346f324b5f15570a8718c95594dba85d47235c9bfd0293a7e4",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ba04e8e5ba6973b8c02595149dcaadf60193ad0e0a58f2399e0091783e1750c1",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9b768b4af87487df2a90b76c82e70040d6b2da744ed9194c100c7bf453e58607",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0527b41937fb4e88726079058c2f2fd90d7ba8dc6592ec040c63b6cc46711693",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "70799c1e8d691027ba2e5b527038e36304c34b15d23b357deb76bfc5bd88540c",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d1f7e585e4983a7e8fe8120797f15fec035a6d6b770506a497177734463c8c06",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b400d201ad7ee47cbe312c3497f8b2ea52e947a9bd401c7dfab3ee15f49f1645",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3e72a60bb48950b3440ded7e0c1f84de38a8e02d92f2124c583ce1fc07e82c95",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "002080a3044fd1e85e0c8ffd4d997eb6e187042a6e64fc36e9da4f65dd414cca",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c20ea0db6f0334e16d582bf6e8e6cfff48e4936ef1f17b16bd9910c751680d60",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "94b870feda8d20f2f95d91d29d81dd499695c459b8ec47b52e63b55b13f0ade8",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4b6b942aada9b4c6b4879aa5f5ea5f09868dee89bdaad92441f88b3d054c8617",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "677516b14684374d68c6d5887b1faa7ead8de6b26d7c67d1a229fb88222a2cef",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e4e1cc43710bbbbfc7a28f62a224257318377a40ff0a3ecf982b29f841e4a9bd",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9b11e86b2e15dd04c7f542a33f20c5517b5d4529ca5aec4ef56e778c499e974f",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0af128bbe20b17f24275713d10836d32c72f4f6533a24a5a128f111d180e028a",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a6930ffc7c8c115c965de888e40a3f80020f6be0bad3f451b7a0d1ebddd318a8",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5e82427e61011cce80361f075bb3090b14bb71d5765d4b1f3e06cdb705fba89e",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b83f7b5d28ab049156735c9e0f63a30ded8ac62a62c74d9ec8ac0a02223b544e",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "87392c7f478c1c50d698b5a97f827e52f665076d6025a53e8fa752629cb1c48e",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fd0e9679b6cb23dae373673c9fb3f80546d866fed4d4f9c042a9598882805453",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3d238ef2427e630e77635dd8db1745ab6bcf540e00bda333b79ae68c01ce5714",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2b2f5269de898e285b739fa824bef54da971dc58ad1ae468dad542597ccfd035",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d8df754851187fb46d3cbe83216366085b5ff2eba90109f0afbc271ab5cb4367",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "82afdf3b80699dd2f055ef18e4589f1aa8b79f2a0b81211940790edaf1021071",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b4b1f2a91911743a4c34917469bdebd8328f38513e42a36a0a9a6785d98f2ed4",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c9f7d0628969e98c3b46746f721f4a9416f1739dfec19e259aafa3d97aff81ca",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8e1b2d28ff9f4c143ee137570af54a29a2ae5a155f0081022fabe2b7b9dd9c7c",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "863b2a3f2e59c35961eade991a5cfbd7335a50233e40cbc5cb6a92a5cc95a8b4",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ef9d820735db5116867fc1279aa4221563a36690bc24d93cf731713d6e5c088f",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e020ff916ab76b86cacf325a428ced1de404ae2b020609d59aa1b3887eaf0434",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0449e99a96014407b84f83922b82ef5238ae1a38c91882ddc0fd78ad026da078",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "627a9ebd605b3b440e65f0efac2a35ac44425e9ead26d3f016e97b5471ec8bc7",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "15ea26ab7fa58c85364b27278e608e10de9a7d8f1ebbbf0b290e82738b77645b",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8477066bb92175e64192f4cde88ccb5dd9ada6409b2473de6b09b0e3fb7f2a14",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a31af8d0aad8a1a4628ca39394a44057d6d614d7578414132a1718983cefaaed",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "941361d29b39d43d310389d97ec8093da7fbb0b771577febb439de6c5cc4dadc",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b4019c2243b5c66eb9b849c01100fd5f12d8426b8e412452fc07c14096de3537",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "72606bd781d181d43caa09d854c6fd8fa6645329d976d43135570d04e658b43c",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2c1aecfa26c925d5ad3162e40e98e4f58596f5dcc54f439a1167900bca2278b2",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bf701482df29b08d17565591ebecd39217658eff79e3f430e627208b9a2f969e",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e7168c7b8b98432469297b0897a52d29fe807e68ee6576b17deb27778183b15e",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "52f44ba1471885118e95ca0dc2ac3bd61a67fe4b2db6e43c1d9ec7a5292b8b77",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ee384cc6dd78d0860f449fab160db73c6c9839ff8c36ffb3b0e073ea55ed15c8",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e301b9767b2bd2ef49f6d817220f64ec0c67e929de660cc990e4a771fac4263b",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c8a7057ba45a9bc6c6e79fd4fffb5340f313b6f98b589a0693f7b6027221fcfb",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4e0e4426675673c11e65182029eb8e00c37521a8ed0f5566f2457f3643fbdaf8",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b332ec1b35cbc1cf5541d9a1f78169d642243590a8075839ed3fddf44bbd6ba6",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bc29f86ac633021bb4f413e9d8b86ed84ae83250ce90dfa3a4fd79df025823de",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f09e1b2d6b3935a6d1a155c9c745a325f62e97c8b92c31d42a481d1168f81c41",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dabaad0040d1a60cca1809ed3970e8b63b5886c61274fd03f45da1578c0fc663",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6146cfe9f62fd90e50390a8171280500e3481fc25ea75abebda6ef2fa3b871f8",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "91f34ae64d330316965cf5ab9fa6674de74c52f1505bdb8556c117e9b3255976",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "45826f560ea20fe6d1d21fc1302145d907a711ba9d87f3a4be94d1b855851ed6",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b60cc92d12b889b079fe740f098477e2a6d2311de6b791a2fd62f152fdbec64e",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "eefec9d550379b920d2b098a669c06da4f0bf415ef8bf6301c93e734c6f6cf4b",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dbd9f8c23d14d5fc4f3b07b908e882e15359c4044a9c24bf1d3f7415ebc5b764",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6a6096d15b55eea0171c7e58ab677d3c3abd20575f67fdc2c37b3616ae0488b1",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "31889e7d8c7f02ffdafe136b6abd187017e69c343e209fd74a9a40e693d57bba",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "73cd4f6f33d84eeb885920669c8e2e99840a1781d0f413f88651c68be8660044",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a98951e7e9fc73ae6013b510cfef1d77afffe047c937ee210896c5b472f246da",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9186444c07f60128c77bd5c3c0ef2e9ea8a9cbedb2062e0834b4af7ccfb93cb3",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f07899c1ff097b1c51e2d3b6406ba0855cb1474ba7966e395b7d47c497540b00",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "58eb3329590bc941c564db982ba45b87e5ca78ec9b7368218ac512594f315807",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fe223dcfd770fc9f29e34c02a8afc58add655f1cb3a0da18bfef850bc2f29da2",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1e7af79a53c77d6a1dcddb0dbd124757b066c532017ea00e327477089c5b570c",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "10443f7d7b5894bff22b4fadb5078e75dc7a507e43081823f7a53a2df64c56b0",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3f4cc4ceb9dfc5c758f8b851ed77b6dec052e2764fc39a2c143fa6a76dfe814e",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7f54805a7f19f74e7ecc9b60ea225d0fd07521dad21a48e2682bf885740d076f",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9ae8ddbc4786ff0c580b47a3237637c60c5ed7ab509a2cb4c81efd63c5e7ac35",
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
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "92f9197e1f5fdae782c1b482f5fe39eab480c2d8ac8d10b0c4da26dcb31c4730",
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
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "10ba28c455d9f86650ae34e89b68b5702ca4839c705d240648e8ef9695daadc6",
  "manifest_payload_sha256": "138e7ce657ca898b3b0523e34762ffa88a0211330400649b92245d63a888703e",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 10535,
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
          "content_sha256": "ef8cdf0ec4ed40333ac47dc8cc8660084383df2ea14c4c7f95b4beb113c89b79",
          "logical_id": "mc-405fa0e547ffb00ee0743601",
          "row_sha256": "d4b177a1101511d48449b3fc535619d73132a36dbfecc175f7a8d72f81284d94"
        },
        {
          "content_sha256": "fc2e2356098fb81ea26a1ae4eca069d61818fa19508cd87c6599ea5ab66c796a",
          "logical_id": "mc-e1d5350c48cf8fd0d15afdce",
          "row_sha256": "ae6219f4f24ce1df69befa126e1a7f33badb3152e49432d946bced8ce976ec5d"
        },
        {
          "content_sha256": "ecf9f7b621703fda136e24af7b330c18996556b174fdb31a24de371e14dcc8f2",
          "logical_id": "mc-7f6b889ffccb7afddf9fea5f",
          "row_sha256": "24afd8084cee5aaa468dbdb430670cd7a00a2d1e21a49b3d6a45d645d5e97d93"
        },
        {
          "content_sha256": "89053c3446fef9f964631d8a03b7bce731d03d470cd0c57551e3a5ff914ab812",
          "logical_id": "mc-f27bf5c68905845573007bb3",
          "row_sha256": "365a9a13a657e4c560b92eb7181923b67ef5d438b2e35e79c5d2109472f84ce8"
        },
        {
          "content_sha256": "d3e2bf04bd7746346f324b5f15570a8718c95594dba85d47235c9bfd0293a7e4",
          "logical_id": "mc-f726fd672421c50799332024",
          "row_sha256": "d2893e754d0b7dc5236b281ecf3b139e8a92666be54b7b9cef65db2c5136571a"
        },
        {
          "content_sha256": "ba04e8e5ba6973b8c02595149dcaadf60193ad0e0a58f2399e0091783e1750c1",
          "logical_id": "mc-fccc453bd4ab4941409e7bf9",
          "row_sha256": "0f6e629573e6aca9a8af11c7d7b0d1a757d2771651f4c21b1a4bd2657ee4dd3e"
        },
        {
          "content_sha256": "9b768b4af87487df2a90b76c82e70040d6b2da744ed9194c100c7bf453e58607",
          "logical_id": "mc-c0e72e196678952189509127",
          "row_sha256": "6485aed6b0204447d7536857d8ce3956af1649cdb120207f7cc699411aceff73"
        },
        {
          "content_sha256": "0527b41937fb4e88726079058c2f2fd90d7ba8dc6592ec040c63b6cc46711693",
          "logical_id": "mc-83bf809ee49d5864f0049a85",
          "row_sha256": "aa9ed77cd186ad7116321209a503095fd59a4b02d1324023621e4dc961307584"
        },
        {
          "content_sha256": "70799c1e8d691027ba2e5b527038e36304c34b15d23b357deb76bfc5bd88540c",
          "logical_id": "mc-b94314f0d50a23dcab697cc7",
          "row_sha256": "3a1ed3ba3f3ab442c8746e272405a545e73249102c9c0de76743fef518e13df5"
        },
        {
          "content_sha256": "d1f7e585e4983a7e8fe8120797f15fec035a6d6b770506a497177734463c8c06",
          "logical_id": "mc-58f9377a4e5513c61f851abc",
          "row_sha256": "f3f06891296b51d5b9de19ade2824db14b1513afbc11b19b143cbaa26c890b3e"
        }
      ],
      "sha256": "78132223c85d19a940f4ccd77bd1404fded686295285b39794f7b70e760e9d58",
      "sheet_name": "cards",
      "table_sha256": "8ab607945954b15d73e4a507d9d2ced4f6e2af15dc06fce1e3e7fdea783224df",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 41636,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/vllm-full-session-review-technical-qa.xlsx",
      "row_count": 65,
      "rows": [
        {
          "content_sha256": "b400d201ad7ee47cbe312c3497f8b2ea52e947a9bd401c7dfab3ee15f49f1645",
          "logical_id": "mc-a4cd934451dbc2f674b835a9",
          "row_sha256": "47ce8b1c65390f9f9682eca259334e86c2bf2ea4dcd92a5ed73b05c85bbbbc1a"
        },
        {
          "content_sha256": "3e72a60bb48950b3440ded7e0c1f84de38a8e02d92f2124c583ce1fc07e82c95",
          "logical_id": "mc-d90a8a49188317c4475bb1fa",
          "row_sha256": "f46d0ad3eee447888d44b245d789c9c798f43ae142315e2e12b16f88ef6cb172"
        },
        {
          "content_sha256": "002080a3044fd1e85e0c8ffd4d997eb6e187042a6e64fc36e9da4f65dd414cca",
          "logical_id": "mc-b5ab4a7997b4428cc78802e8",
          "row_sha256": "887a5c6124ff1b7a57e5124e153ccd59067cd84f0acda667c930a056bf2cdd29"
        },
        {
          "content_sha256": "c20ea0db6f0334e16d582bf6e8e6cfff48e4936ef1f17b16bd9910c751680d60",
          "logical_id": "mc-abe7eb24831612c9c3d4eef7",
          "row_sha256": "afd4bef36391b8cfb23957d2a4256922e8c98d7f2d421175ae1bb4be770f1405"
        },
        {
          "content_sha256": "94b870feda8d20f2f95d91d29d81dd499695c459b8ec47b52e63b55b13f0ade8",
          "logical_id": "mc-84676054f06c3224f8b9d42a",
          "row_sha256": "0f21f962137d8ac011b70aab3a3895d1d99f6d8232eb0911be62f3b71a4fe709"
        },
        {
          "content_sha256": "4b6b942aada9b4c6b4879aa5f5ea5f09868dee89bdaad92441f88b3d054c8617",
          "logical_id": "mc-386eff0e70f84976785adb7b",
          "row_sha256": "e5332d6a1c7e283aaa6f91e81700958000c503ff140a8699ce22d14abaf22aa9"
        },
        {
          "content_sha256": "677516b14684374d68c6d5887b1faa7ead8de6b26d7c67d1a229fb88222a2cef",
          "logical_id": "mc-c44b4d7a9ac36edd8c5dca77",
          "row_sha256": "96f0922c3751ba80b0219341dc4c69068d0b2b167f18ecc5fc2036c8fb5b50c1"
        },
        {
          "content_sha256": "e4e1cc43710bbbbfc7a28f62a224257318377a40ff0a3ecf982b29f841e4a9bd",
          "logical_id": "mc-1ba245772d63b1465ff84b74",
          "row_sha256": "3a9e83dbf3a35d5f512cc29e7733ba1cf0bb3de34ababd00da2fdd9498cf945f"
        },
        {
          "content_sha256": "9b11e86b2e15dd04c7f542a33f20c5517b5d4529ca5aec4ef56e778c499e974f",
          "logical_id": "mc-ce38809b2547d6c1f70c85f7",
          "row_sha256": "da282feef7455991e007eb0699f26c3afd3e55a2e088d677dad56ef2840442f6"
        },
        {
          "content_sha256": "0af128bbe20b17f24275713d10836d32c72f4f6533a24a5a128f111d180e028a",
          "logical_id": "mc-bdb5ae3a65636b17a13e73b1",
          "row_sha256": "feeb90014500baedb96869afa00940909a4b6c4d001b8b2d06e60dd9778c1992"
        },
        {
          "content_sha256": "a6930ffc7c8c115c965de888e40a3f80020f6be0bad3f451b7a0d1ebddd318a8",
          "logical_id": "mc-9d7b2af6315be86cc53562e2",
          "row_sha256": "504ff07f15d77ec1c4b76d7cbb4c2f59e846128ebdf5c8cd96a660b6e124c06c"
        },
        {
          "content_sha256": "5e82427e61011cce80361f075bb3090b14bb71d5765d4b1f3e06cdb705fba89e",
          "logical_id": "mc-81771102328bc5e96dde9dc2",
          "row_sha256": "d9f1390afcb02af43edd370f42f12c5c9a1acd5e4a9fb153338ad5208d409827"
        },
        {
          "content_sha256": "b83f7b5d28ab049156735c9e0f63a30ded8ac62a62c74d9ec8ac0a02223b544e",
          "logical_id": "mc-7552190fc19fef1335707b7d",
          "row_sha256": "12e6dd1d2eb7e9ce9fa04b7fb8a1882d86e114d0c33c9a8b19a225c588ac5e12"
        },
        {
          "content_sha256": "87392c7f478c1c50d698b5a97f827e52f665076d6025a53e8fa752629cb1c48e",
          "logical_id": "mc-ae376a7b1a41d3c8475527c6",
          "row_sha256": "c8336bec91b964533ef91f60a30e0eacebeae7d623fa576e043e92df0b90a6e5"
        },
        {
          "content_sha256": "fd0e9679b6cb23dae373673c9fb3f80546d866fed4d4f9c042a9598882805453",
          "logical_id": "mc-2731ed1a964329bd32e1ea08",
          "row_sha256": "e77be603abecbcc68d21f032399764acab0e1db5f512a99659a893f6fc9ac6f9"
        },
        {
          "content_sha256": "3d238ef2427e630e77635dd8db1745ab6bcf540e00bda333b79ae68c01ce5714",
          "logical_id": "mc-c34a6067dd76a7d3dbf5a43c",
          "row_sha256": "0be52256ac88501f305bed6fd4096dbe83af5673d055c08eb548e76531d466ca"
        },
        {
          "content_sha256": "2b2f5269de898e285b739fa824bef54da971dc58ad1ae468dad542597ccfd035",
          "logical_id": "mc-34b6be82985ed08c4270ddd5",
          "row_sha256": "8786013fbadb97d03fe6a893dca2c206212f22a34fe9a9f4ea1aee03b0bb4510"
        },
        {
          "content_sha256": "d8df754851187fb46d3cbe83216366085b5ff2eba90109f0afbc271ab5cb4367",
          "logical_id": "mc-50591c6d88488ddba1e419c9",
          "row_sha256": "c7c8dddce10e6a8890c538f785a036aad7c89f9cbc4932ebc4d0b523b39c7375"
        },
        {
          "content_sha256": "82afdf3b80699dd2f055ef18e4589f1aa8b79f2a0b81211940790edaf1021071",
          "logical_id": "mc-79362f0684e9a30fd97821f9",
          "row_sha256": "0624d21821a0941bf730f59d8ca102ae5d493957806466247ccf93c72120b1b5"
        },
        {
          "content_sha256": "b4b1f2a91911743a4c34917469bdebd8328f38513e42a36a0a9a6785d98f2ed4",
          "logical_id": "mc-485fa8cafc3816acbd51e03b",
          "row_sha256": "7a7047502a23ccea2e9cb74b2ec200887e7ae5c0ae7e394e9456c558965af632"
        },
        {
          "content_sha256": "c9f7d0628969e98c3b46746f721f4a9416f1739dfec19e259aafa3d97aff81ca",
          "logical_id": "mc-7ab1103a71067961285a47b8",
          "row_sha256": "e32745ac2f4475f29ae60dc523f8a513a6164c2d29fadd880bf566cc3fe5f96b"
        },
        {
          "content_sha256": "8e1b2d28ff9f4c143ee137570af54a29a2ae5a155f0081022fabe2b7b9dd9c7c",
          "logical_id": "mc-99d1339089861715964f1d78",
          "row_sha256": "06dba3839b0c025e20a75b26eedae778fd5cf116515e5aee3863c14d3903f4d1"
        },
        {
          "content_sha256": "863b2a3f2e59c35961eade991a5cfbd7335a50233e40cbc5cb6a92a5cc95a8b4",
          "logical_id": "mc-af6f8b4a3928337d2ca0f814",
          "row_sha256": "cbcf6c39b2238a02f09e1c36e15c083864782ae6f6d3cbc5c058ccd2b5733256"
        },
        {
          "content_sha256": "ef9d820735db5116867fc1279aa4221563a36690bc24d93cf731713d6e5c088f",
          "logical_id": "mc-48619be5e7dad94f709e6ca0",
          "row_sha256": "98caf9eaa07ae0a1bf954ad1e37a0a7018ddbcb6b65d2a6d8a1ddde51395aafb"
        },
        {
          "content_sha256": "e020ff916ab76b86cacf325a428ced1de404ae2b020609d59aa1b3887eaf0434",
          "logical_id": "mc-842ef50d7d3ce590a2b562fd",
          "row_sha256": "9f3d76e8ac590804bbb3025eb01eaefc24d1913a73dac7ec28654626e76263d5"
        },
        {
          "content_sha256": "0449e99a96014407b84f83922b82ef5238ae1a38c91882ddc0fd78ad026da078",
          "logical_id": "mc-15d38c7ca8e263ccc79e1ad2",
          "row_sha256": "580bbba73b77e15d1d3c343ce5bb0de6fb195692c10bdab25af721e5c24a6f5b"
        },
        {
          "content_sha256": "627a9ebd605b3b440e65f0efac2a35ac44425e9ead26d3f016e97b5471ec8bc7",
          "logical_id": "mc-c1802344a7ebe74999d6ee69",
          "row_sha256": "782c8f74b51cf346d66543e2c336972f1ef79024ac1ebcfc5ce1f5b1d76b7434"
        },
        {
          "content_sha256": "15ea26ab7fa58c85364b27278e608e10de9a7d8f1ebbbf0b290e82738b77645b",
          "logical_id": "mc-360a92513663a1e184c73081",
          "row_sha256": "0b4c054ffa6499210aef4521065def9745b20f4bbb1bd5631ffd08b915bf342b"
        },
        {
          "content_sha256": "8477066bb92175e64192f4cde88ccb5dd9ada6409b2473de6b09b0e3fb7f2a14",
          "logical_id": "mc-e48c0b5d4e3fdfff3a079a2b",
          "row_sha256": "50164d4b08082ae72bb990654631c1e0c0b0eb32bd4c60b34041bb3e6f206159"
        },
        {
          "content_sha256": "a31af8d0aad8a1a4628ca39394a44057d6d614d7578414132a1718983cefaaed",
          "logical_id": "mc-a6c09dfcf93944cd2951b72d",
          "row_sha256": "4eafdeeb021fe78a5723c48d52e703d50acef19f2a367c735f32daec8abe5ae3"
        },
        {
          "content_sha256": "941361d29b39d43d310389d97ec8093da7fbb0b771577febb439de6c5cc4dadc",
          "logical_id": "mc-4dc2c29e8fcf8c04979b2598",
          "row_sha256": "93c4b2317277d57f7ade96ee40ebe2d66b3eff34317a4b1f53776c42fc392923"
        },
        {
          "content_sha256": "b4019c2243b5c66eb9b849c01100fd5f12d8426b8e412452fc07c14096de3537",
          "logical_id": "mc-869c7b15dde8da8ad2b2baa1",
          "row_sha256": "d1120c502e5d9446e0704b07d363e971eebdc84670702b78bda60fcefe432090"
        },
        {
          "content_sha256": "72606bd781d181d43caa09d854c6fd8fa6645329d976d43135570d04e658b43c",
          "logical_id": "mc-05890bf565adf8310a19569d",
          "row_sha256": "bd24c7b00472407c7c7c81b681ea6d49352325f53a102e6fabbf74247cb042d5"
        },
        {
          "content_sha256": "2c1aecfa26c925d5ad3162e40e98e4f58596f5dcc54f439a1167900bca2278b2",
          "logical_id": "mc-fec55735844313fb603e37f7",
          "row_sha256": "19de56b1801152d61bf7d501c9cfecdf576fbf19511673f1735a1891e281e7dd"
        },
        {
          "content_sha256": "bf701482df29b08d17565591ebecd39217658eff79e3f430e627208b9a2f969e",
          "logical_id": "mc-2077ed6103d92ccddd84f0e1",
          "row_sha256": "063e4c7e44c782dd71bda9ee70f2a30610300aacabf3baf7ffe09d0008adbb44"
        },
        {
          "content_sha256": "e7168c7b8b98432469297b0897a52d29fe807e68ee6576b17deb27778183b15e",
          "logical_id": "mc-6e80586c21468b342811ed55",
          "row_sha256": "00911a6ec7ab0a0b6c74cce452d53f2ed47ddc807c762bc949364a70f50bcba3"
        },
        {
          "content_sha256": "52f44ba1471885118e95ca0dc2ac3bd61a67fe4b2db6e43c1d9ec7a5292b8b77",
          "logical_id": "mc-c4305907da34210e2ff9a593",
          "row_sha256": "0763c7395da8c776057b8b0ffb17ff1cb243315b6af8662bb58b741035a940df"
        },
        {
          "content_sha256": "ee384cc6dd78d0860f449fab160db73c6c9839ff8c36ffb3b0e073ea55ed15c8",
          "logical_id": "mc-704e23f2ac33a51b9d1cafc8",
          "row_sha256": "a854ceaa1637b8e616910e351563c17d83d84b99b460a36d199b551aad032b7f"
        },
        {
          "content_sha256": "e301b9767b2bd2ef49f6d817220f64ec0c67e929de660cc990e4a771fac4263b",
          "logical_id": "mc-a89805ae36fffe4b3d357833",
          "row_sha256": "08f09ba9fddd4e4b56baf53240893a8e377bb382482524c27b284d3679b7fd3b"
        },
        {
          "content_sha256": "c8a7057ba45a9bc6c6e79fd4fffb5340f313b6f98b589a0693f7b6027221fcfb",
          "logical_id": "mc-a30eed37a09de948f40c5e38",
          "row_sha256": "f34ade4da26d31fbc4c473a2301b3a92ae6177ccf0f1176bfc5f92b8ee99aa1c"
        },
        {
          "content_sha256": "4e0e4426675673c11e65182029eb8e00c37521a8ed0f5566f2457f3643fbdaf8",
          "logical_id": "mc-209c99a69970415ab4a8fe1d",
          "row_sha256": "1cfbf4495a5e2eecfca686291150a4fcae47765f7a65dd90c951dbc80d47408e"
        },
        {
          "content_sha256": "b332ec1b35cbc1cf5541d9a1f78169d642243590a8075839ed3fddf44bbd6ba6",
          "logical_id": "mc-45d3779fb6c0899ed56d4194",
          "row_sha256": "19e665f46e52ddb1742dc4542c9d5e1ec7294b89734f013844278d24b5a067ee"
        },
        {
          "content_sha256": "bc29f86ac633021bb4f413e9d8b86ed84ae83250ce90dfa3a4fd79df025823de",
          "logical_id": "mc-8cf820cd4a8ab0b43fbc3bd6",
          "row_sha256": "8942e3e20752b551811443f6277e4aae9015ba23ce4e2f86316b0400019ca1ac"
        },
        {
          "content_sha256": "f09e1b2d6b3935a6d1a155c9c745a325f62e97c8b92c31d42a481d1168f81c41",
          "logical_id": "mc-5e59c8a2b0cca6fa8beb9e2a",
          "row_sha256": "81c4fc3054c3ecec753f35bfa61b7699d222341f934113cd698bdc5304234446"
        },
        {
          "content_sha256": "dabaad0040d1a60cca1809ed3970e8b63b5886c61274fd03f45da1578c0fc663",
          "logical_id": "mc-1e35d3d80a0dc7e8e4785c53",
          "row_sha256": "55f9c68daf0a2df41bc808f6eafa0557568902842fb984380cb3edc937250980"
        },
        {
          "content_sha256": "6146cfe9f62fd90e50390a8171280500e3481fc25ea75abebda6ef2fa3b871f8",
          "logical_id": "mc-602b377049f84ba5753f398a",
          "row_sha256": "c920dcc1aac6d5d3e14721a5ce45898fcb3ab7197552496d6efefaa4b4ff3f93"
        },
        {
          "content_sha256": "91f34ae64d330316965cf5ab9fa6674de74c52f1505bdb8556c117e9b3255976",
          "logical_id": "mc-caa30e7923ecbc5638183da4",
          "row_sha256": "38c5dd52d7c594e5596cd0d3f17475d7b163224af08168784cecb4afe658d768"
        },
        {
          "content_sha256": "45826f560ea20fe6d1d21fc1302145d907a711ba9d87f3a4be94d1b855851ed6",
          "logical_id": "mc-284dc7300b3aedb48fb0e420",
          "row_sha256": "84f32a1d70ce9cec4cf84eb791b9ab63e709bb8188093a2fbfefb52291cb05e4"
        },
        {
          "content_sha256": "b60cc92d12b889b079fe740f098477e2a6d2311de6b791a2fd62f152fdbec64e",
          "logical_id": "mc-6e05afd30a1c350d2df82072",
          "row_sha256": "7c096771d2b217a0f00a53a7d4da1585917594dffc5e899906a7816583fd58e8"
        },
        {
          "content_sha256": "eefec9d550379b920d2b098a669c06da4f0bf415ef8bf6301c93e734c6f6cf4b",
          "logical_id": "mc-7e660bc46d36e9c0cfc24dbe",
          "row_sha256": "bc73a68f485a932abb78f368451127afc96b4946572b18e52a8a99ca22c98b81"
        },
        {
          "content_sha256": "dbd9f8c23d14d5fc4f3b07b908e882e15359c4044a9c24bf1d3f7415ebc5b764",
          "logical_id": "mc-a72685e9c1eb7ad97aed8c54",
          "row_sha256": "3426572581ee6ca16508532de74a482227e23d04df2bb45ef3860a125103926a"
        },
        {
          "content_sha256": "6a6096d15b55eea0171c7e58ab677d3c3abd20575f67fdc2c37b3616ae0488b1",
          "logical_id": "mc-0ab4415e85e63ef091d12815",
          "row_sha256": "4211bf9b8d3495c16201f3b6230cb024bb3ae268bd94e07cce84a6768bb0f0d6"
        },
        {
          "content_sha256": "31889e7d8c7f02ffdafe136b6abd187017e69c343e209fd74a9a40e693d57bba",
          "logical_id": "mc-0178da19052b31ed9413b152",
          "row_sha256": "3dc115e0692832a5276c167c9ddba145200c2354875b60fbd5c7a5573e0ada62"
        },
        {
          "content_sha256": "73cd4f6f33d84eeb885920669c8e2e99840a1781d0f413f88651c68be8660044",
          "logical_id": "mc-3afc59e30aebf237c71c5ed1",
          "row_sha256": "c066af4edc9c5200ad375145fd43eb23d3a86050564fb65ef86a27061135cef7"
        },
        {
          "content_sha256": "a98951e7e9fc73ae6013b510cfef1d77afffe047c937ee210896c5b472f246da",
          "logical_id": "mc-8f0f7a7e25dc774f917af791",
          "row_sha256": "f8a442dfa57ab67f41a2925afb04e9339aa5970f920234a6be9b5271bc1184d6"
        },
        {
          "content_sha256": "9186444c07f60128c77bd5c3c0ef2e9ea8a9cbedb2062e0834b4af7ccfb93cb3",
          "logical_id": "mc-2d44e22b6d9485325f8972b5",
          "row_sha256": "918072cc8de7cc01e911fbb7bfc52ae17932be4a3848029e26bc6324fab78b5c"
        },
        {
          "content_sha256": "f07899c1ff097b1c51e2d3b6406ba0855cb1474ba7966e395b7d47c497540b00",
          "logical_id": "mc-80ae6e0f740e097b9da41829",
          "row_sha256": "233aef58fbb4a41b477023267e467073a8cf071e206ba3aac90a1a6ddb2766db"
        },
        {
          "content_sha256": "58eb3329590bc941c564db982ba45b87e5ca78ec9b7368218ac512594f315807",
          "logical_id": "mc-41e581d77f242691d8a14b70",
          "row_sha256": "9bda2fceed44be5a108da435ea391130a0104e93e884a7568f24fbf7081fab98"
        },
        {
          "content_sha256": "fe223dcfd770fc9f29e34c02a8afc58add655f1cb3a0da18bfef850bc2f29da2",
          "logical_id": "mc-d72838bb6579b9ace4af9cd9",
          "row_sha256": "11dd5a46c003999bf290addf53888aea233c3aaa1d890f1cbfa741f51ae0ec67"
        },
        {
          "content_sha256": "1e7af79a53c77d6a1dcddb0dbd124757b066c532017ea00e327477089c5b570c",
          "logical_id": "mc-462e2917ea13b46bfbaa040e",
          "row_sha256": "d14075f9569616b446d556057de3c4bbfeb8e940e769aede3bf9428e4ff87b6f"
        },
        {
          "content_sha256": "10443f7d7b5894bff22b4fadb5078e75dc7a507e43081823f7a53a2df64c56b0",
          "logical_id": "mc-73a6eeefde047dc3f11e9f7d",
          "row_sha256": "f2cb1eec8a0a10e084ed2e8e07241009791379714e9f2f10ff7bdacbce6e3a98"
        },
        {
          "content_sha256": "3f4cc4ceb9dfc5c758f8b851ed77b6dec052e2764fc39a2c143fa6a76dfe814e",
          "logical_id": "mc-b13b06cdaf66c20fbc1b730e",
          "row_sha256": "d8b80b05c2ef30b1c8b6cb797675dddd9b486c928c47b0d008534ae067e7dc18"
        },
        {
          "content_sha256": "7f54805a7f19f74e7ecc9b60ea225d0fd07521dad21a48e2682bf885740d076f",
          "logical_id": "mc-ac522a78ed1ae6861706a904",
          "row_sha256": "77b0657991d914a52c92094af7d3baf2ba1dc27a4f5858e374255ebc4e017277"
        },
        {
          "content_sha256": "9ae8ddbc4786ff0c580b47a3237637c60c5ed7ab509a2cb4c81efd63c5e7ac35",
          "logical_id": "mc-c9e64adaf431ebe5c519d83f",
          "row_sha256": "3fff588f79a36e2a228458abad710faaddf8b80058fa072c55cb21ab419ce080"
        },
        {
          "content_sha256": "92f9197e1f5fdae782c1b482f5fe39eab480c2d8ac8d10b0c4da26dcb31c4730",
          "logical_id": "mc-3330df6c801eb8afb0c4a4d1",
          "row_sha256": "951331eed1a064ed88c1e94d346ac1cfb6183f849b086acd2ba53150226c884a"
        }
      ],
      "sha256": "b8e64714a1038d26b1bb86fbced6cb4dcc2768eb5b64894d3f9ceaa8d7850ffa",
      "sheet_name": "cards",
      "table_sha256": "a8ecd80b93051d1174a859460d7a389e0488119f0c3ebae3ae09fe2ba3690d15",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
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

导入文件：[vllm-full-session-review-correction.xlsx](vllm-full-session-review-correction.xlsx)（10 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[vllm-full-session-review-technical-qa.xlsx](vllm-full-session-review-technical-qa.xlsx)（65 张卡）
