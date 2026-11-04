---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "a287649c81cb21de2432afb3909aab23eadc2fbe94e990b280164f03657c4af5",
  "candidate_sha256": "184a1f57ffc666b72eb3e01b0fdd5a10f16ea91bcdb6551d5cff32a4c74dc8bf",
  "cards": [
    {
      "content_sha256": "89cf25064cc19532374f7f9ace7b4be21e0cd6ec465f814adfee5246450d4efe",
      "content_summary": "A 级理由：回答训练精度调试中如何从 Python 观察 Tensor 梯度的问题，避免因 C++ 调度而误判没有可用观测接口。",
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
      "content_sha256": "1d3f592004af8b15d4cbcf4f2b22456d20425b66602cd3b1cd36cbebd1ce37b4",
      "content_summary": "A 级理由：防止把刚采样的 token 计入本步输入，进而算错调度预算与 KV 进度。",
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
      "content_sha256": "5c0dfd12bce7663f6258aa581ee000ecad9a86c5e5d4d2231f3d7943801b35d3",
      "content_summary": "A 级理由：防止遗漏前端已判停的外层条件，错误取消仍应继续生成的请求。",
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
      "content_sha256": "a7549577b79cfc61a24595e593b382296515171c2d7fb4cdb03a6af484656232",
      "content_summary": "A 级理由：防止将新 KV 写错槽位的问题误诊为历史读取映射，错修状态重排。",
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
      "content_sha256": "e1114abe6ade21674ed1d109b7b3636d78b44d0dd2a821f946000bf3409b234e",
      "content_summary": "B 级选材依据：保留启动生命周期与单步执行的职责边界，用于解释热路径而不反复背接口。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0de4eded45405aa5a7a2dd059fb97734299219cf9f755d79cbf2cadbb1e6fb78",
      "content_summary": "A 级理由：防止把注册成功当作替换算子正确，漏检数学语义、输入修改和执行依赖。",
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
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6b2276306b8fa4bc35bd7a588f1b18c58710f96c4e84de1daffb32cbf03abcb4",
      "content_summary": "A 级理由：防止将非流式输出误实现为阻断 Core 的中间结果回传，混淆内部与对外输出。",
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
      "content_sha256": "1c4730f398f50e073a2b87a270c72d4d2dffbc1cb79bfecaea9fadb543bfb299",
      "content_summary": "A 级理由：防止请求表注销时提前销毁仍需交付最终结果的 Collector。",
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
      "content_sha256": "4b774d75f22ea389737c23e68efc9a127fc4344dbf4194a4cbf2dd9f63b27aa1",
      "content_summary": "A 级理由：防止 Runner 重复扣减调度侧已经管理的 KV 引用，破坏其他请求仍使用的共享块。",
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
      "content_sha256": "361cb0b1a5075ec7847599e8d1f0726c992a3566cceec6d2f7066fe990634fbf",
      "content_summary": "B 级选材依据：保留用户结束原因与内部控制操作的接口辨析，不将当场术语澄清当成反复个人错误。",
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
      "content_sha256": "cd08b1e5ac83ed905099049d974a0afc3c17b2048e8a80ca56a15c2a38c88461",
      "content_summary": "A 级理由：防止按物理容量而非配置预算接纳分配，遗漏可导致 OOM 的预算超额。",
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
      "content_summary": "B 级选材依据：把局部物化存储放大与整体显存账本分开，支持跨布局估算。",
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
      "content_sha256": "4a26fd471b563c6524d9a38685160092eb204c4e95638f2b7b25102770aece3f",
      "content_summary": "2026-11-03本地归档：FLOPs推导由W2-U4的gemm-ledger规范卡统一承担，避免重复复习相同计算账本；保留原身份与内容追溯。",
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
      "lifecycle": "archived",
      "logical_id": "mc-b5ab4a7997b4428cc78802e8",
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
      "content_sha256": "d71f30475e1e5955e3a0e2e5f0956f078d3e32f6e0ca5efe543760478b30afbb",
      "content_summary": "2026-11-03本地归档：BF16输入与输出的最低字节账本由W2-U4的gemm-ledger规范卡统一承担；已补齐历史题面的输出存储精度，保留原身份追溯。",
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
      "lifecycle": "archived",
      "logical_id": "mc-abe7eb24831612c9c3d4eef7",
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
      "content_sha256": "4d6516c2bc3566ad253d9e33d20e49043e972291d58c1c1b0439d6e69b1b2f78",
      "content_summary": "A 级理由：防止仅凭访存变快就写成 bank conflict 已消除，造成错误根因归属。",
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
      "content_sha256": "938c11064b4c179120fad7d6cb34b62b61b73d3bd9cd5d6f2d6d3f9d89b857d0",
      "content_summary": "B 级选材依据：用于区分采样随机性和执行不确定性，避免 temperature=0 的保证被扩大。",
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
      "content_sha256": "677516b14684374d68c6d5887b1faa7ead8de6b26d7c67d1a229fb88222a2cef",
      "content_summary": "A 级理由：防止把加入 dump 后不复现当成正确性修复，忽略观测对异步时序的影响。",
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
      "content_summary": "B 级选材依据：保留从首个分叉定位原因的可迁移调试方法。",
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
      "content_sha256": "9b11e86b2e15dd04c7f542a33f20c5517b5d4529ca5aec4ef56e778c499e974f",
      "content_summary": "A 级理由：防止仅等设备流便消费尚未完成 CPU 准备或提交的 H2D 数据。",
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
      "content_summary": "B 级选材依据：保留设备 stream 与 CPU 线程的分层判断，避免错误解释提交开销。",
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
      "content_sha256": "9038ef593e8277713b55d3d8895be18bfe7788c32b0c43dd48916546bb27d5f8",
      "content_summary": "B 级选材依据：用于比较依赖开销与重叠收益，限定单流优化的迁移条件。",
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
      "content_sha256": "8fb8ee39d9673bc2a53df7d46c1a8df25a1dc3b99cf9cbe0968f4023ce9ff3ae",
      "content_summary": "B 级选材依据：使性能报告正确区分加速倍数与耗时降幅，前提是测量边界一致。",
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
      "content_sha256": "562d25793153c2cc3bb41349f17dab4e189a3d2d1b9460d6588209361771084d",
      "content_summary": "B 级选材依据：保留按层检查切分与复制项的方法，避免用总参数量机械均分。",
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
      "content_sha256": "0ea79878fab636f22bf0a3311aff8fc384e6c291b6681758c4b6b3497221cdf6",
      "content_summary": "A 级理由：防止 Core 快速返回时前端输出状态尚未注册，造成结果找不到接收位置。",
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
      "content_sha256": "1f56c7636515b8f5dae88713c7f6cd143fd3ef98367d1fcca400633b66213518",
      "content_summary": "B 级选材依据：解释结果尚未产生时如何预建接收对象，属于可迁移的状态准备模式。",
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
      "content_sha256": "88a327bc80bc7be54dee44639f5ced2efe1007d59e669d41b2ca3d47250a9f5e",
      "content_summary": "B 级选材依据：区分跨 IPC 的输入载荷与 Core 内可变请求状态，支持沿边界追踪请求。",
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
      "content_sha256": "fc1ae4c6c8784bab0c7a30621837c962a76439491a56deadeff03ed4dff238c4",
      "content_summary": "A 级理由：防止把 grammar 就绪当成资源准入成功，跳过 token 预算与 KV 容量约束。",
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
      "content_sha256": "e263051f2500b1cb0ebf16ee0010ae2c2552a629a8d44baac2cb01ccce811a93",
      "content_summary": "B 级选材依据：区分可复用编译产物与请求匹配状态，避免误解逐 token 的准备成本。",
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
      "content_sha256": "4e6fb09b5e100f0b54ffbdbd4eb6c99788d19e711ce15c88fbc4f7114c861b55",
      "content_summary": "B 级选材依据：保留结构约束与事实/业务正确性的边界，避免过度解释 schema 验证。",
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
      "content_sha256": "c1b6c7614badc802f0914d068303567cf94612b1e9e9cdf21bd567b9cb4b4eaa",
      "content_summary": "A 级理由：防止把执行前推进的调度计数当成设备已完成的凭据。",
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
      "content_sha256": "805b73e8338425e557d0bfffec4401082b84d0f4c20c8745ff3ea313a185fd7c",
      "content_summary": "B 级选材依据：连接最后一次 prefill、首个输出和下一轮 decode，支持理解 token 流程。",
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
      "content_sha256": "2b95507f5c120cac937545d00e625e25caefe5be457ce4323c5fe223c2a5540e",
      "content_summary": "B 级选材依据：区分能力开关与预算驱动的实际分块，避免笼统描述每个请求。",
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
      "content_sha256": "66fca11959495daac9d93cc65503cba6a87f8859d9fb8e85811023fa6fe3118c",
      "content_summary": "A 级理由：防止把暂时抢占当成请求终止，错误交付结束输出或丢失生成历史。",
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
      "content_sha256": "9c8dc01b94c00c85a20624d2e3c8424a52de5aba76f4412d741d964de9a27554",
      "content_summary": "B 级选材依据：区分队列位置与状态枚举，支持阅读抢占和恢复路径。",
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
      "content_sha256": "ccfe68bda0e1166f7061a9942e60196d4a2b11dac06ad5b334a7b28ac9f05780",
      "content_summary": "A 级理由：防止因请求退出 InputBatch 就删除仍需恢复的缓存状态，或把残留块号误当所有权。",
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
      "content_sha256": "4cba0c80f25efd68fe40581963c9fbf8de90dcbbaab1aa900876b5fae74834f1",
      "content_summary": "A 级理由：防止恢复完整块表被错误追加到旧映射，造成 KV 寻址错误。",
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
      "content_sha256": "264986c5970ad74e933aa632a4da452f1366bdc5ca35079245393b81b6987e30",
      "content_summary": "A 级理由：回答分页 KV 怎样由逻辑位置定位物理槽位的问题，防止混用 token 槽位和字节地址。",
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
      "content_sha256": "13bd7083eac11c72a17847ca771a39e344884b9546e07f8a69b8039eb2bbb3f8",
      "content_summary": "A 级理由：防止 batch 重排时只保留行内映射却未重排行，导致请求读到别人的 KV。",
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
      "content_sha256": "672ea59bab92df253a93e90c5b0cefb5b634a9c0fef9066759a68be4dbff5e70",
      "content_summary": "A 级理由：防止把历史长度计入本步 Query 片段边界，破坏 Attention 元数据。",
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
      "content_sha256": "25eb4be3c985febd1fe8ae6451a0f9b5e56900cefef82b5a9956956c9a686d6c",
      "content_summary": "B 级选材依据：用同批计算场景强化因果范围与请求隔离，避免退化成显然的是非题。",
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
      "content_sha256": "6ed5cae8151df2ea5a0ce0491a48372940923a81a188e688ad142db65bc6258a",
      "content_summary": "A 级理由：防止仅凭 shape 相同复用旧 metadata 内容，沿用错误请求或 KV 映射。",
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
      "content_sha256": "d10e9c509312437516ea76bb222d8cb69b6f3ca0ca1a29bc403fba4cc8a1280e",
      "content_summary": "B 级选材依据：保留从入口追到选中实现的源码定位方法，并限定性能最优性结论。",
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
      "content_sha256": "ba3da0c00c8d8c5e752a6cf2fb097677edaf8307ec3aed04297eaa9b75960984",
      "content_summary": "A 级理由：防止删除不参与数值计算但负责图中 KV 保序的依赖参数。",
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
      "content_sha256": "0ab10ab8c66ad06d741e9f92dcc5af78dd2ab90372f04d300d712b709d1dd7d3",
      "content_summary": "A 级理由：防止把阶段返回 None 当成失败，或把后续采样误当成领取已完成 token。",
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
      "content_sha256": "0660081abc03822ecac2c2d93d46aaf4bbbaa6391bdb1d7d1ff9314e31cda91f",
      "content_summary": "2026-11-03本地归档：sample_tokens职责已并入同批execute_model与采样阶段机制卡mc-fec55735844313fb603e37f7；保留原身份，避免同结论重复导出。",
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
      "lifecycle": "archived",
      "logical_id": "mc-2077ed6103d92ccddd84f0e1",
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
      "content_sha256": "8db395b16d6599081cead401a8fa85a5dbe9a3bdf8dffd331b1ddc206309f6f5",
      "content_summary": "B 级选材依据：区分输入行、logits 候选与有效输出，支持多请求混合执行的解释。",
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
      "content_sha256": "2bc5f358dde816126a0295ec8f81105a1bdcc2e1b9af6829a3fa1733a0308c2b",
      "content_summary": "B 级选材依据：把执行结果接回 Scheduler 账本，避免将设备侧缓存当成核心请求状态。",
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
      "content_sha256": "a138d7161540120b5f7b2e96df3fe3f6e7855911b34b9e8484fb7c755b710299",
      "content_summary": "B 级选材依据：定位自定义 Worker 的配置入口并连接 Runner 构造，属于源码接入导航。",
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
      "content_sha256": "da993fc839375da8b522306403d97f0133c4ce8e27709affe92a3c661d2310ac",
      "content_summary": "B 级选材依据：区分两项独立设备扩展入口，避免假定一项替换自动完成另一项。",
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
      "content_sha256": "74973041122f6067ba38384bab349b5262a671a39d1e7f3b14c1b12c4c3fb296",
      "content_summary": "B 级选材依据：把底层算子注册与模型实际调用连接起来，支持排查实现未被采用的问题。",
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
      "content_sha256": "e27ac8a55f819519f20efa9e3aa41419fbe388155b6cc8aff06f6330ffd02640",
      "content_summary": "B 级选材依据：区分原生 PyTorch 组合与执行设备，避免把 native 当成 CPU 同义词。",
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
      "content_sha256": "b332ec1b35cbc1cf5541d9a1f78169d642243590a8075839ed3fddf44bbd6ba6",
      "content_summary": "A 级理由：防止只测 world 组掩盖跨组归约错误，为 collective 正确性设计反例。",
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
      "content_sha256": "bd8c2d48a533b601e682e137f43d82c1b686c572325f96798dff8a8b1ceffdab",
      "content_summary": "A 级理由：防止因 padding 差异直接修改 Scheduler，遗漏已有页字节接口实现错误。",
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
      "content_sha256": "ce52d1bc84ce26b2668ba61c088c9253f79b2b4843e077c0faaa663c5f2beeef",
      "content_summary": "B 级选材依据：要求用无法表达的语义缺口论证 Core 修改，保留可迁移的扩展边界判断。",
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
      "content_sha256": "9578b6220ad3a257dca8401fa6c00af79c4eebd65bf8a1434072f580ad495e6f",
      "content_summary": "B 级选材依据：建立单层有效 KV 的计算口径，避免混用 Query heads 与 KV heads。",
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
      "content_sha256": "6146cfe9f62fd90e50390a8171280500e3481fc25ea75abebda6ef2fa3b871f8",
      "content_summary": "A 级理由：防止将末块空槽与物理 padding 重复加总，算错 KV 容量。",
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
      "content_sha256": "aa23c09b4bdd1a39af4d6105f23d58fc6fac2dbee347adc6d329339d8289569d",
      "content_summary": "B 级选材依据：分开核对页跨度、基址对齐与分配粒度，避免从一个布局数字推断硬件约束。",
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
      "content_sha256": "eb575cd2e18c137dc142b6fa5fdda0514f414f8757f6533aa861a52d15b1576c",
      "content_summary": "A 级理由：防止多请求先合并 token 再取整，低估独立末块造成的容量需求。",
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
      "content_sha256": "aaf63090f7b652d33949c1bb9608946fccd9204f6d9c3a41515c8788f6f325a2",
      "content_summary": "B 级选材依据：区分逻辑 pool ID 与跨层物理页数，保留单位映射而不是练习乘法。",
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
      "content_sha256": "6c09ce3835848337cc5b6bdfe186e1ee0ab279228bb2d5e545c2fe0de816e14d",
      "content_summary": "A 级理由：防止一个请求结束就覆盖仍被其他请求引用的 KV。",
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
      "content_sha256": "b73c0a937770c403b520c4058bcaa5aa90dde8b230a12216745e1e6295d12589",
      "content_summary": "A 级理由：防止把 free queue 理解成全无缓存数据，破坏重命中与淘汰复用。",
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
      "content_sha256": "a4f80f5bc51702dcfffaa54953c8a6a03e11b4492b03fd85a89f0b21afe97a63",
      "content_summary": "A 级理由：防止把查到前缀候选当成已经持有引用，漏掉容量检查与正式保护阶段。",
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
      "content_summary": "B 级选材依据：按新增块需求判断请求可否继续，避免仅由空闲块数作过粗决策。",
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
      "content_sha256": "694828c8c2c11bddc7651e526d048d6537dfcab620bdbffc8b59a00fb9ebeaaf",
      "content_summary": "A 级理由：防止仅按当前块 token 复用不同父上下文下的 KV。",
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
      "content_sha256": "4bc2a76d786802251e5d8c4351e6b0b30cc24d954ebdb7326ff5a00eeed3f03e",
      "content_summary": "B 级选材依据：区分缓存共享策略与 KV 数值关系，支持多租户复用边界说明。",
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
      "content_sha256": "9186444c07f60128c77bd5c3c0ef2e9ea8a9cbedb2062e0834b4af7ccfb93cb3",
      "content_summary": "B 级选材依据：理解缓存延迟侧信道的观测对象，并避免把共享隔离当作完整安全机制。",
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
      "content_sha256": "f07899c1ff097b1c51e2d3b6406ba0855cb1474ba7966e395b7d47c497540b00",
      "content_summary": "B 级选材依据：解释共享范围内 salt 稳定与跨请求命中率的关系。",
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
      "content_sha256": "58eb3329590bc941c564db982ba45b87e5ca78ec9b7368218ac512594f315807",
      "content_summary": "B 级选材依据：区分分页访问和前缀复用两项功能，避免将存储方式当成自动跳过计算。",
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
      "content_sha256": "068b1edd9ca0ad6da94061f8cb8c7c6a696d1425be011032920350fa8f6fb1d4",
      "content_summary": "B 级选材依据：区分活跃占用与预分配池大小，支持解释共享后的显存统计。",
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
      "content_sha256": "4dff49cb068e8d226a31505a4e476eac3d8863055dce08a47b119179829e5436",
      "content_summary": "B 级选材依据：以单位和布局契约判断搬运粒度与 token 分块，避免把 512 B 直接换成 256 token。",
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
      "content_sha256": "ab362f7bc93af35996d5894dbdf64c997878347586a23f76dde512268d1bfa34",
      "content_summary": "B 级选材依据：比较增量与累计交付范围，避免假定一次 token 必有一次 SSE。",
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
      "content_sha256": "7438cd027d770b673d2261327ef94e515e7a30ff5dd45044dc9ae2f54262edff",
      "content_summary": "B 级选材依据：把异步输出生成器与模型执行、采样职责分开，支持完整请求讲述。",
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
      "content_sha256": "0d4433ba5d844a5ccccc46cfab0479b108c1152e350b4323b69e4413cfd42413",
      "content_summary": "A 级理由：防止请求结束时误清服务级权重、设备或物理 KV pool，破坏其他请求。",
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
      "content_sha256": "8244328adfa7b8595e26e5ee6e33eb4372869d6d1a97c9efe7e12dc5baa5ffd3",
      "content_summary": "B 级选材依据：解释最终输出与 Runner 清理的依赖边界，仍保留在途访问约束。",
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
      "content_sha256": "1f0abfa45bb856fcc021e15b79a6ad1ed3897a2fba4aee233bc74daba418cbdb",
      "content_summary": "B 级选材依据：解释无计算步骤仍能处理结束通知，避免误判清理必须伴随 forward。",
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
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "full-session-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "a82f4a3b53e509767a726484a96dfca5d6a256a38dc9822e2f255965bdeec3f0",
  "manifest_payload_sha256": "c16ec48d53cf9a5c99341c563d35a3bd99e0e9432852e3ca90de7ec157053bbd",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 9595,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/vllm-full-session-review-correction.xlsx",
      "row_count": 8,
      "rows": [
        {
          "content_sha256": "89cf25064cc19532374f7f9ace7b4be21e0cd6ec465f814adfee5246450d4efe",
          "logical_id": "mc-405fa0e547ffb00ee0743601",
          "row_sha256": "34c8695ec362950e882620d811c40a9158f3a63f7aecb8421d68f52796bdfb59"
        },
        {
          "content_sha256": "1d3f592004af8b15d4cbcf4f2b22456d20425b66602cd3b1cd36cbebd1ce37b4",
          "logical_id": "mc-e1d5350c48cf8fd0d15afdce",
          "row_sha256": "ea320aafebf388ab7532ca6efda2a52a2ba204fcf32bcb2554647c395a570438"
        },
        {
          "content_sha256": "5c0dfd12bce7663f6258aa581ee000ecad9a86c5e5d4d2231f3d7943801b35d3",
          "logical_id": "mc-7f6b889ffccb7afddf9fea5f",
          "row_sha256": "5ce2f8fc754c55ef100cd3f5b366f7c883dd9ccbdb71a44c666d0ac36d2de2bb"
        },
        {
          "content_sha256": "a7549577b79cfc61a24595e593b382296515171c2d7fb4cdb03a6af484656232",
          "logical_id": "mc-f27bf5c68905845573007bb3",
          "row_sha256": "905bad268d298bf90fe4cebd62169eba9dd5080a9a4053af1bc72634f5c111e3"
        },
        {
          "content_sha256": "e1114abe6ade21674ed1d109b7b3636d78b44d0dd2a821f946000bf3409b234e",
          "logical_id": "mc-f726fd672421c50799332024",
          "row_sha256": "fc566ebcd12742a014f460245b7cc99801be1458ac0da31d70c3132f49d2c8a4"
        },
        {
          "content_sha256": "6b2276306b8fa4bc35bd7a588f1b18c58710f96c4e84de1daffb32cbf03abcb4",
          "logical_id": "mc-c0e72e196678952189509127",
          "row_sha256": "dc43e2e393d44603716eea0b4513383062e2d1dda2577445d40593e99ce4566a"
        },
        {
          "content_sha256": "1c4730f398f50e073a2b87a270c72d4d2dffbc1cb79bfecaea9fadb543bfb299",
          "logical_id": "mc-83bf809ee49d5864f0049a85",
          "row_sha256": "57879ac4a52b35fd83eae3ba0689b2ad7492e8a17a47f5b3a9f817a25462b00d"
        },
        {
          "content_sha256": "4b774d75f22ea389737c23e68efc9a127fc4344dbf4194a4cbf2dd9f63b27aa1",
          "logical_id": "mc-b94314f0d50a23dcab697cc7",
          "row_sha256": "99df8535cc0ab683db919d9354d5ed340ceb630318426d2a372cd0eeb43033c5"
        }
      ],
      "sha256": "e86b4c8acb86d97ad841f1acc86dcc50c9f693285be52dd2305118a305ab239f",
      "sheet_name": "cards",
      "table_sha256": "15ca6987248d32023ff0acbc1242c3e7e9e49e6c2844e5c042b8695ea2787cc1",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 48474,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/vllm-full-session-review-technical-qa.xlsx",
      "row_count": 64,
      "rows": [
        {
          "content_sha256": "0de4eded45405aa5a7a2dd059fb97734299219cf9f755d79cbf2cadbb1e6fb78",
          "logical_id": "mc-fccc453bd4ab4941409e7bf9",
          "row_sha256": "602927f5359be7bb89e7034380db009085563575413bc2941473cb6a8cef5818"
        },
        {
          "content_sha256": "361cb0b1a5075ec7847599e8d1f0726c992a3566cceec6d2f7066fe990634fbf",
          "logical_id": "mc-58f9377a4e5513c61f851abc",
          "row_sha256": "21198ff71554f907fdd9f55765264c9c9f7588db53646e6b56f94f6b92305066"
        },
        {
          "content_sha256": "cd08b1e5ac83ed905099049d974a0afc3c17b2048e8a80ca56a15c2a38c88461",
          "logical_id": "mc-a4cd934451dbc2f674b835a9",
          "row_sha256": "b91a99ce8583929b3928b6bc925f0b9691bcc9c67bb3e498df1af3e5c08cdd7b"
        },
        {
          "content_sha256": "3e72a60bb48950b3440ded7e0c1f84de38a8e02d92f2124c583ce1fc07e82c95",
          "logical_id": "mc-d90a8a49188317c4475bb1fa",
          "row_sha256": "f46d0ad3eee447888d44b245d789c9c798f43ae142315e2e12b16f88ef6cb172"
        },
        {
          "content_sha256": "4d6516c2bc3566ad253d9e33d20e49043e972291d58c1c1b0439d6e69b1b2f78",
          "logical_id": "mc-84676054f06c3224f8b9d42a",
          "row_sha256": "6d95a1e8770d5a0f18c14ab6c2ed950a6c762a405a59b5ca0f37b38e6858985a"
        },
        {
          "content_sha256": "938c11064b4c179120fad7d6cb34b62b61b73d3bd9cd5d6f2d6d3f9d89b857d0",
          "logical_id": "mc-386eff0e70f84976785adb7b",
          "row_sha256": "1eb05b73bf5d4de319360a7a4df46118900edd057f554450c68721599a731297"
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
          "content_sha256": "9038ef593e8277713b55d3d8895be18bfe7788c32b0c43dd48916546bb27d5f8",
          "logical_id": "mc-9d7b2af6315be86cc53562e2",
          "row_sha256": "cf9367ba76ec7e8a70883f1f6250391a9b38b7a9520f5969b6f21508db575cf0"
        },
        {
          "content_sha256": "8fb8ee39d9673bc2a53df7d46c1a8df25a1dc3b99cf9cbe0968f4023ce9ff3ae",
          "logical_id": "mc-81771102328bc5e96dde9dc2",
          "row_sha256": "428d93912bb5ff94593d270a6e53ca907b9a2bdd6f62c5d0da77ba49b6d122cb"
        },
        {
          "content_sha256": "562d25793153c2cc3bb41349f17dab4e189a3d2d1b9460d6588209361771084d",
          "logical_id": "mc-7552190fc19fef1335707b7d",
          "row_sha256": "eb5efd1f53caba6131a5e37c69633f169067ab037a3d1499b1ec0654d292721f"
        },
        {
          "content_sha256": "0ea79878fab636f22bf0a3311aff8fc384e6c291b6681758c4b6b3497221cdf6",
          "logical_id": "mc-ae376a7b1a41d3c8475527c6",
          "row_sha256": "86fb4b54196227f7263520ca09df6dc6504f87a6ea9bb844eed2889d6617eb7c"
        },
        {
          "content_sha256": "1f56c7636515b8f5dae88713c7f6cd143fd3ef98367d1fcca400633b66213518",
          "logical_id": "mc-2731ed1a964329bd32e1ea08",
          "row_sha256": "035f3ceec51bc47d1285c75587399bcab4d2a7abafa1b66882edbf533b36a73e"
        },
        {
          "content_sha256": "88a327bc80bc7be54dee44639f5ced2efe1007d59e669d41b2ca3d47250a9f5e",
          "logical_id": "mc-c34a6067dd76a7d3dbf5a43c",
          "row_sha256": "7735a12ce18de1e84076c08de1df9e7dbfad5c291e9d00b7d631fd18358757a8"
        },
        {
          "content_sha256": "fc1ae4c6c8784bab0c7a30621837c962a76439491a56deadeff03ed4dff238c4",
          "logical_id": "mc-34b6be82985ed08c4270ddd5",
          "row_sha256": "953ab4c659f7bec2376482cedf57c56851c5239bf8fd6970a4075f8aaac782b9"
        },
        {
          "content_sha256": "e263051f2500b1cb0ebf16ee0010ae2c2552a629a8d44baac2cb01ccce811a93",
          "logical_id": "mc-50591c6d88488ddba1e419c9",
          "row_sha256": "3100e9bb539110b463dc0594b9279d348065b36bd6e2a9df38237b96adc984ed"
        },
        {
          "content_sha256": "4e6fb09b5e100f0b54ffbdbd4eb6c99788d19e711ce15c88fbc4f7114c861b55",
          "logical_id": "mc-79362f0684e9a30fd97821f9",
          "row_sha256": "6910a5ee12d1fd730d8a18d0316d26c05633877b1754c60fe7129cb05284b49e"
        },
        {
          "content_sha256": "c1b6c7614badc802f0914d068303567cf94612b1e9e9cdf21bd567b9cb4b4eaa",
          "logical_id": "mc-485fa8cafc3816acbd51e03b",
          "row_sha256": "b933438313524de87eddb5b670d866516e366638f86475f20bc8f1de9480a7f4"
        },
        {
          "content_sha256": "805b73e8338425e557d0bfffec4401082b84d0f4c20c8745ff3ea313a185fd7c",
          "logical_id": "mc-7ab1103a71067961285a47b8",
          "row_sha256": "aebdf6a8e633f0307ff5429dbfa71ee2f1c0360a3124c7efb3844f7af334b4f1"
        },
        {
          "content_sha256": "2b95507f5c120cac937545d00e625e25caefe5be457ce4323c5fe223c2a5540e",
          "logical_id": "mc-99d1339089861715964f1d78",
          "row_sha256": "8e59643924e303b7d9242dd27d0c73b3bcdd753febb39e2e82723c5635daa416"
        },
        {
          "content_sha256": "66fca11959495daac9d93cc65503cba6a87f8859d9fb8e85811023fa6fe3118c",
          "logical_id": "mc-af6f8b4a3928337d2ca0f814",
          "row_sha256": "735ab9db45b770a332f8a364eaf7249608d8d576d8e4c91e2a481f4f0cbccacf"
        },
        {
          "content_sha256": "9c8dc01b94c00c85a20624d2e3c8424a52de5aba76f4412d741d964de9a27554",
          "logical_id": "mc-48619be5e7dad94f709e6ca0",
          "row_sha256": "93daa72420c0080ca94dc48c38c03ca17bcfe7b0da8c136e64e74a7131a812d8"
        },
        {
          "content_sha256": "ccfe68bda0e1166f7061a9942e60196d4a2b11dac06ad5b334a7b28ac9f05780",
          "logical_id": "mc-842ef50d7d3ce590a2b562fd",
          "row_sha256": "11d4ec5996099b877becaf455386a402080272fd4a5c022e693d9c0e761f8c4d"
        },
        {
          "content_sha256": "4cba0c80f25efd68fe40581963c9fbf8de90dcbbaab1aa900876b5fae74834f1",
          "logical_id": "mc-15d38c7ca8e263ccc79e1ad2",
          "row_sha256": "bda3f1ef051205e851347e2431b7990ec0f419df45c2d278d2621a6da618d315"
        },
        {
          "content_sha256": "264986c5970ad74e933aa632a4da452f1366bdc5ca35079245393b81b6987e30",
          "logical_id": "mc-c1802344a7ebe74999d6ee69",
          "row_sha256": "b54e7d173a8a23b0a0025c64f0f21843b1aa76384122125b2aece7b33471648f"
        },
        {
          "content_sha256": "13bd7083eac11c72a17847ca771a39e344884b9546e07f8a69b8039eb2bbb3f8",
          "logical_id": "mc-360a92513663a1e184c73081",
          "row_sha256": "cc777b6a225499d03de3c7a33ae0ffa5c0bf0d07942fe8a843e5b8c7eb344ab6"
        },
        {
          "content_sha256": "672ea59bab92df253a93e90c5b0cefb5b634a9c0fef9066759a68be4dbff5e70",
          "logical_id": "mc-e48c0b5d4e3fdfff3a079a2b",
          "row_sha256": "2440c1f3f7a3a8dfa76c6c325bc3eef868567f9d90f839a640e05653eaa5067d"
        },
        {
          "content_sha256": "25eb4be3c985febd1fe8ae6451a0f9b5e56900cefef82b5a9956956c9a686d6c",
          "logical_id": "mc-a6c09dfcf93944cd2951b72d",
          "row_sha256": "eb8864a9d5be40f112f774347527ec84f84d04b13bc726de7c34fb9e7ddb1f92"
        },
        {
          "content_sha256": "6ed5cae8151df2ea5a0ce0491a48372940923a81a188e688ad142db65bc6258a",
          "logical_id": "mc-4dc2c29e8fcf8c04979b2598",
          "row_sha256": "62854953cf117cfa6dcc90a4fd91ff883b744369f7a3b9ea29d8c3850cc18251"
        },
        {
          "content_sha256": "d10e9c509312437516ea76bb222d8cb69b6f3ca0ca1a29bc403fba4cc8a1280e",
          "logical_id": "mc-869c7b15dde8da8ad2b2baa1",
          "row_sha256": "d7aef420797889ab735f66a3f5fa12be557a1df391524401fe5f4e93ac289364"
        },
        {
          "content_sha256": "ba3da0c00c8d8c5e752a6cf2fb097677edaf8307ec3aed04297eaa9b75960984",
          "logical_id": "mc-05890bf565adf8310a19569d",
          "row_sha256": "cc636282895d693a0d7b75413d73b34ec6386526861435a9feb2189f6e442476"
        },
        {
          "content_sha256": "0ab10ab8c66ad06d741e9f92dcc5af78dd2ab90372f04d300d712b709d1dd7d3",
          "logical_id": "mc-fec55735844313fb603e37f7",
          "row_sha256": "c32b63bd3fac7b094aa9193c139c9c8270504011bbd8d4ace4337aa9a62bb90e"
        },
        {
          "content_sha256": "8db395b16d6599081cead401a8fa85a5dbe9a3bdf8dffd331b1ddc206309f6f5",
          "logical_id": "mc-6e80586c21468b342811ed55",
          "row_sha256": "26e95921ce9c2c637bd7f79c0f817dfabfcd72d308524178956ec81261a29322"
        },
        {
          "content_sha256": "2bc5f358dde816126a0295ec8f81105a1bdcc2e1b9af6829a3fa1733a0308c2b",
          "logical_id": "mc-c4305907da34210e2ff9a593",
          "row_sha256": "22b6ead368376fd6006fe36fa6e714e71076e84f3503b6b3b9a96765e77beb89"
        },
        {
          "content_sha256": "a138d7161540120b5f7b2e96df3fe3f6e7855911b34b9e8484fb7c755b710299",
          "logical_id": "mc-704e23f2ac33a51b9d1cafc8",
          "row_sha256": "c5e6a3d1113b96c52f117c147088b9459c0fbd080e1f64dbbdb8276e3df3ac70"
        },
        {
          "content_sha256": "da993fc839375da8b522306403d97f0133c4ce8e27709affe92a3c661d2310ac",
          "logical_id": "mc-a89805ae36fffe4b3d357833",
          "row_sha256": "c292c8df1d15b1662f7edeefd6a1b2c06da16fd7a2d7a6817e544c2f34bda932"
        },
        {
          "content_sha256": "74973041122f6067ba38384bab349b5262a671a39d1e7f3b14c1b12c4c3fb296",
          "logical_id": "mc-a30eed37a09de948f40c5e38",
          "row_sha256": "72fecad054e21bd596b1c148b6c8bcf200b1b8de0084dbb9b95b07263bc8c33f"
        },
        {
          "content_sha256": "e27ac8a55f819519f20efa9e3aa41419fbe388155b6cc8aff06f6330ffd02640",
          "logical_id": "mc-209c99a69970415ab4a8fe1d",
          "row_sha256": "edc091f14d0b862ba048d4db50d6da675ee7cc03ef5e8d9c14306839166a8386"
        },
        {
          "content_sha256": "b332ec1b35cbc1cf5541d9a1f78169d642243590a8075839ed3fddf44bbd6ba6",
          "logical_id": "mc-45d3779fb6c0899ed56d4194",
          "row_sha256": "19e665f46e52ddb1742dc4542c9d5e1ec7294b89734f013844278d24b5a067ee"
        },
        {
          "content_sha256": "bd8c2d48a533b601e682e137f43d82c1b686c572325f96798dff8a8b1ceffdab",
          "logical_id": "mc-8cf820cd4a8ab0b43fbc3bd6",
          "row_sha256": "0ec64877e5d93a75bc727c68e9dc6f9480992a94aaf5cabdefc2b929a5f92685"
        },
        {
          "content_sha256": "ce52d1bc84ce26b2668ba61c088c9253f79b2b4843e077c0faaa663c5f2beeef",
          "logical_id": "mc-5e59c8a2b0cca6fa8beb9e2a",
          "row_sha256": "e415ff2bc2ae26f9b74d6e8b0ed71432b11e457ba81dcd569b96993ee155dcc5"
        },
        {
          "content_sha256": "9578b6220ad3a257dca8401fa6c00af79c4eebd65bf8a1434072f580ad495e6f",
          "logical_id": "mc-1e35d3d80a0dc7e8e4785c53",
          "row_sha256": "4d40de507897e77e94a43160c952b190a81ec73a6ec755f5058d801fa6896126"
        },
        {
          "content_sha256": "6146cfe9f62fd90e50390a8171280500e3481fc25ea75abebda6ef2fa3b871f8",
          "logical_id": "mc-602b377049f84ba5753f398a",
          "row_sha256": "c920dcc1aac6d5d3e14721a5ce45898fcb3ab7197552496d6efefaa4b4ff3f93"
        },
        {
          "content_sha256": "aa23c09b4bdd1a39af4d6105f23d58fc6fac2dbee347adc6d329339d8289569d",
          "logical_id": "mc-caa30e7923ecbc5638183da4",
          "row_sha256": "a2b78925c6e2650bd374df1db091039460155fe4e90f0d25bea94a4b8a22eed3"
        },
        {
          "content_sha256": "eb575cd2e18c137dc142b6fa5fdda0514f414f8757f6533aa861a52d15b1576c",
          "logical_id": "mc-284dc7300b3aedb48fb0e420",
          "row_sha256": "b6ecf8bf1d6b3d0951c67cfa5d61489a4dc268d8478d56f1e026ef45462ec003"
        },
        {
          "content_sha256": "aaf63090f7b652d33949c1bb9608946fccd9204f6d9c3a41515c8788f6f325a2",
          "logical_id": "mc-6e05afd30a1c350d2df82072",
          "row_sha256": "4cf8f0c3e728c6507b5fcf91eff6628f23deeb6201cd5d36a5305d13041e85c6"
        },
        {
          "content_sha256": "6c09ce3835848337cc5b6bdfe186e1ee0ab279228bb2d5e545c2fe0de816e14d",
          "logical_id": "mc-7e660bc46d36e9c0cfc24dbe",
          "row_sha256": "94ebe0b05f815421d1997b22a6a7050bf716280ea04d239cc12b02e0516af858"
        },
        {
          "content_sha256": "b73c0a937770c403b520c4058bcaa5aa90dde8b230a12216745e1e6295d12589",
          "logical_id": "mc-a72685e9c1eb7ad97aed8c54",
          "row_sha256": "41f9ef37bc3cac00a2aceccf5406092fe60eb3f275e5cad026e870790efb1b06"
        },
        {
          "content_sha256": "a4f80f5bc51702dcfffaa54953c8a6a03e11b4492b03fd85a89f0b21afe97a63",
          "logical_id": "mc-0ab4415e85e63ef091d12815",
          "row_sha256": "2ea0ae04235f9d7e97339e28076f6136d488c480c19721efc94e4eae3b243c7e"
        },
        {
          "content_sha256": "31889e7d8c7f02ffdafe136b6abd187017e69c343e209fd74a9a40e693d57bba",
          "logical_id": "mc-0178da19052b31ed9413b152",
          "row_sha256": "3dc115e0692832a5276c167c9ddba145200c2354875b60fbd5c7a5573e0ada62"
        },
        {
          "content_sha256": "694828c8c2c11bddc7651e526d048d6537dfcab620bdbffc8b59a00fb9ebeaaf",
          "logical_id": "mc-3afc59e30aebf237c71c5ed1",
          "row_sha256": "9dd16ae4f36b414107b26bdf91898ba475935bc8b21baf56d2cf1d6c58b1ae32"
        },
        {
          "content_sha256": "4bc2a76d786802251e5d8c4351e6b0b30cc24d954ebdb7326ff5a00eeed3f03e",
          "logical_id": "mc-8f0f7a7e25dc774f917af791",
          "row_sha256": "2b6d6cc5641176458d7fb7a59caf268919b7074e18f9db5f577ead27b0046d19"
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
          "content_sha256": "068b1edd9ca0ad6da94061f8cb8c7c6a696d1425be011032920350fa8f6fb1d4",
          "logical_id": "mc-d72838bb6579b9ace4af9cd9",
          "row_sha256": "dd7f0f802177330e1e702d9149e8b6b39cebaa13b2b6bfa98de17ee3d9e8fd9d"
        },
        {
          "content_sha256": "4dff49cb068e8d226a31505a4e476eac3d8863055dce08a47b119179829e5436",
          "logical_id": "mc-462e2917ea13b46bfbaa040e",
          "row_sha256": "bcf479269de57780f36af8d24aba8b748bc292afae36309abc198234ee2d43c5"
        },
        {
          "content_sha256": "ab362f7bc93af35996d5894dbdf64c997878347586a23f76dde512268d1bfa34",
          "logical_id": "mc-73a6eeefde047dc3f11e9f7d",
          "row_sha256": "864e89abda26008dbc36d4ec21fb086c9e12ccb38b550b3632f22e9b9833de31"
        },
        {
          "content_sha256": "7438cd027d770b673d2261327ef94e515e7a30ff5dd45044dc9ae2f54262edff",
          "logical_id": "mc-b13b06cdaf66c20fbc1b730e",
          "row_sha256": "b57c9cf6940a7a8c3a72e7df1a359b41d9325e5debe18ea520e48be70b84b07c"
        },
        {
          "content_sha256": "0d4433ba5d844a5ccccc46cfab0479b108c1152e350b4323b69e4413cfd42413",
          "logical_id": "mc-ac522a78ed1ae6861706a904",
          "row_sha256": "39b08431454bd5e58e9b0b2627f9b17fd5929b660366809abc8fc52998cc92c0"
        },
        {
          "content_sha256": "8244328adfa7b8595e26e5ee6e33eb4372869d6d1a97c9efe7e12dc5baa5ffd3",
          "logical_id": "mc-c9e64adaf431ebe5c519d83f",
          "row_sha256": "d5a18e68456b868326937249ed261dd4570f8bfb4084d58b44463472cbcb2a8a"
        },
        {
          "content_sha256": "1f0abfa45bb856fcc021e15b79a6ad1ed3897a2fba4aee233bc74daba418cbdb",
          "logical_id": "mc-3330df6c801eb8afb0c4a4d1",
          "row_sha256": "74a13e6f0b477952d60569c9b75efd9a2250d1b97d55205141b032e7b772262d"
        }
      ],
      "sha256": "3f174642f5d1dc583bebe64fd9e11de681d8d6bd62d6a5592e35cce4deebc560",
      "sheet_name": "cards",
      "table_sha256": "40f230b51083dc784b1110996413106fa66b61576e6d6c64ab1dcbc9de8e8907",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "0cc74047acfdf588dab106893976d42eb88c5b6922b4fdd19d611b6df1749b34",
  "sources": [
    {
      "collection": "inference-study-logs",
      "id": "full-session-structured",
      "path": "推理框架/log/2026-09-08-vllm-full-session-review.md",
      "sha256": "af2c4e701fe66c829232e5bf3f5d6e6e0da7be9d70cf53e91d326d1b71f021a0",
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

导入文件：[vllm-full-session-review-correction.xlsx](vllm-full-session-review-correction.xlsx)（8 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[vllm-full-session-review-technical-qa.xlsx](vllm-full-session-review-technical-qa.xlsx)（64 张卡）
