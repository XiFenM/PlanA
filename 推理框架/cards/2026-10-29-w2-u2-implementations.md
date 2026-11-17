---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "6665f9cfb2128bb944f735c692f02b2212ee4c8aaec00f4b6535a405c184691e",
  "candidate_sha256": "cd50e54635006d11c7f6688e855202ef48d5added699ca4e441d73399a9dcefa",
  "cards": [
    {
      "content_sha256": "a79ab4991fee64f6a9731641acaec9a0afecaa2b6d51d414201592272daf8a84",
      "content_summary": "追踪Qwen3 MoE未量化modular路径的路由到通信计算主链；材料：课程网页 synthesis §一；Change Card 02 §1–2；框架节点检查；固定源码核验：vLLM@d7ada3aace051fecec553c185225db2259c2ac6a: vllm/model_executor/models/qwen3_moe.py:203–232；fused_moe/runner/moe_runner.py:598–643、904–936；fused_moe/routed_experts.py:1369–1404；fused_moe/unquantized_fused_moe_method.py:276–315；fused_moe/modular_kernel.py:1525–1581；证据为固定源码的调用与条件，不是设备运行或性能实测。；A理由：回答面试中“从模型入口讲清真实MoE执行主链”，防止仅列通信库和GEMM名称而无法连接调用关系。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-moe-implementation",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "追踪qwen3 moe未量化modular路径的路由到通信计算主链"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a0f44f7d2979c0475db2464d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "57049ed9b763d801cd985a772106c9c9c0282defee8c1094541bd1fef74640c4",
      "content_summary": "解释并行通信与Experts选择怎样共同决定modular实现；材料：Change Card 02 §1、§4；课程网页 comparison 表A；框架节点检查；固定源码核验：vLLM@d7ada3aace051fecec553c185225db2259c2ac6a: vllm/model_executor/layers/fused_moe/config.py:1034–1038；all2all_utils.py:182–230、453；oracle/unquantized.py:253–261、283–317、518–551；modular_kernel.py:1739–1747；证据为固定源码的调用与条件，不是设备运行或性能实测。；A理由：防止把后端配置名当成实际执行路径，误判未进入目标通信实现或不兼容的Experts组合。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-moe-configuration",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "解释并行通信与experts选择怎样共同决定modular实现"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a0f7983e098e635a1ee52dd6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "57474bb3aa43492a9f8d42328155624f8831cd0a8992d41ddfbadb2fcce34bbf",
      "content_summary": "明确OOT注册之后建立未量化modular内核的责任；材料：Change Card 02 §4 OOT 子类责任；固定源码核验：vLLM@d7ada3aace051fecec553c185225db2259c2ac6a: vllm/model_executor/custom_op.py:107–126、167–170、326–340；fused_moe/oracle/unquantized.py:231–232；fused_moe/unquantized_fused_moe_method.py:200–232、294–315；证据为固定源码的调用与条件，不是设备运行或性能实测。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-backend-adaptation",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "明确oot注册之后建立未量化modular内核的责任"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c08c9e1e782b5f1fca6126a2",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "55f8aaff9495cefa31d56c8d7b95a8a6fb0ff5c61a7f0b95733167709d65c1ad",
      "content_summary": "按vLLM激活布局解释专家计数与逐行路由的不同职责；材料：Change Card 02 §2；课程网页 synthesis“路由信息分两类”；固定源码核验：vLLM@d7ada3aace051fecec553c185225db2259c2ac6a: vllm/model_executor/layers/fused_moe/modular_kernel.py:157–163、286–319、1293–1297；prepare_finalize/deepep_ll.py:324–338；prepare_finalize/no_dp_ep.py:63–84；experts/fused_batched_moe.py:923–925；prepare_finalize/mori.py:121–130；证据为固定源码的调用与条件，不是设备运行或性能实测。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-moe-contracts",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "按vllm激活布局解释专家计数与逐行路由的不同职责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7315df9206599ae11b928dd1",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4f1d8898adcaef5bc5c9c3be0d2e71dfd693e43e47a935798f5be3a28cb9866c",
      "content_summary": "按Experts输出与P/F能力选择topk加权归约契约；材料：Change Card 02 §2；框架节点检查中的接口补差；固定源码核验：vLLM@d7ada3aace051fecec553c185225db2259c2ac6a: vllm/model_executor/layers/fused_moe/topk_weight_and_reduce.py:11–118；prepare_finalize/deepep_ht.py:383–394；prepare_finalize/deepep_ll.py:278–284、378–403；experts/fused_batched_moe.py:861–863；证据为固定源码的调用与条件，不是设备运行或性能实测。；A理由：防止适配时选择错误的加权归约契约、重复乘路由权重或对不匹配布局执行归约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-moe-contracts",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "按experts输出与p/f能力选择topk加权归约契约"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-486a27f672d2edbf1836e411",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card",
        "w2-ledger"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1c951d59fe8eb471d8b1488093df0cb1cdf3adb20d350587b5b584f4c8468a50",
      "content_summary": "正确解释output_is_reduced与runner条件性all-reduce；材料：Change Card 02 §2；同日源码审稿补正；固定源码核验：vLLM@d7ada3aace051fecec553c185225db2259c2ac6a: vllm/model_executor/layers/fused_moe/modular_kernel.py:249–252、1749–1753；prepare_finalize/no_dp_ep.py:60–61；runner/moe_runner.py:453–515；证据为固定源码的调用与条件，不是设备运行或性能实测。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "vllm-moe-contracts",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "正确解释output_is_reduced与runner条件性all-reduce"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-eb769bec52690bea988517de",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card",
        "w2-ledger"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f430b82f4c529cc0d7b7850541dae886c9f848b2a51d5127ff093839f1f33981",
      "content_summary": "覆盖o1：V2 GPU ModelRunner普通DP协作、idle与graph一致性。材料：框架节点检查节点3、讲义AgRs基线。源码d7ada3a：vllm/v1/worker/gpu_worker.py:1442-1448；v1/worker/gpu/model_runner.py:918-925、1806-1824、1855-1859；v1/worker/gpu/dp_utils.py:64-81、148-198。限定非DBO、无投机且decode_query_len=1；A理由：防止空闲rank跳过集体调用或各rank自行选择不兼容的执行模式。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-distributed-execution",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "解释普通dp协作步中idle参与与graph模式形状一致性"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-99fe51c2ea71d50056eaf79f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "de131f36dd9c18557e8e504108eaab3bad34ac94a55c5140a8eefa33e8bdedb2",
      "content_summary": "定位modular内部共享专家计算与异步combine的实际窗口；材料：Change Card 02 §8；课程网页 comparison 表A；源码审稿补正；固定源码核验：vLLM@d7ada3aace051fecec553c185225db2259c2ac6a: vllm/model_executor/layers/fused_moe/modular_kernel.py:1255–1291、1435–1465、1714–1718；runner/shared_experts.py:79–121；证据为固定源码的调用与条件，不是设备运行或性能实测。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-moe-overlap",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "定位modular内部共享专家计算与异步combine的实际窗口"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a4baf65139adf754752ce42e",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cf8c40c1d53d0737d7e84d9ecd3ec03239cc3a1ce68d1334c1348444cf3139e8",
      "content_summary": "追踪SGLang普通MoE的dispatcher到runner再到combine链路；材料：课程网页 synthesis §一SGLang代码地图、comparison表A；框架节点检查；固定源码核验：SGLang@43a3f956cb0c9fe9b7b7a042af8d8743176b9dba: python/sglang/srt/layers/moe/fused_moe_triton/layer.py:1597–1682；layers/quantization/unquant.py:1185–1218；layers/moe/moe_runner/runner.py:195–269；证据为固定源码的调用与条件，不是设备运行或性能实测。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "sglang-moe-implementation",
        "fact_scope": {
          "commit": "43a3f956cb0c9fe9b7b7a042af8d8743176b9dba",
          "kind": "snapshot",
          "product": "sglang"
        },
        "recall_target": "追踪sglang普通moe的dispatcher到runner再到combine链路"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-76597101ebd26c3464b19ade",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8a36ac7556d0fd6e434e0f8d943e9824e5d256122f48643115ae34775cb84501",
      "content_summary": "按格式与runner双向键完成普通转换路径接入；材料：框架节点检查：SGLang新格式复查；课程网页 synthesis §一、comparison表A；固定源码核验：SGLang@43a3f956cb0c9fe9b7b7a042af8d8743176b9dba: python/sglang/srt/layers/moe/moe_runner/runner.py:239–269；layers/moe/moe_runner/base.py:210–292；证据为固定源码的调用与条件，不是设备运行或性能实测。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "sglang-backend-adaptation",
        "fact_scope": {
          "commit": "43a3f956cb0c9fe9b7b7a042af8d8743176b9dba",
          "kind": "snapshot",
          "product": "sglang"
        },
        "recall_target": "按格式与runner双向键完成普通转换路径接入"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d653cd227e78ceea04297406",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "52b06dd04c5fb650f1860fcd2985bf01cb45260294cfa4b64458b721590f0eda",
      "content_summary": "覆盖o1：attention-DP同步约束DeepEP auto、decode图与TBO。材料：框架节点检查节点4、讲义comparison。源码43a3f95：python/sglang/srt/managers/scheduler_components/dp_attn.py:286-294、355-380、630-682；layers/moe/utils.py:254-272；token_dispatcher/deepep.py:1097-1105；batch_overlap/two_batch_overlap.py:404-416、455-499；schedule_batch.py:3597-3607。题面限定正常同步、非DWDP、TBO开启及普通EXTEND/DECODE混合。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "sglang-distributed-execution",
        "fact_scope": {
          "commit": "43a3f956cb0c9fe9b7b7a042af8d8743176b9dba",
          "kind": "snapshot",
          "product": "sglang"
        },
        "recall_target": "解释attention-dp信息同步对deepep auto与tbo的全组约束"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-763557e86a5e94c61a29de1f",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "870fb9923e45fd137d8105823188aed4764dc9da0c969320b51b2788445f38fd",
      "content_summary": "区分SGLang的双微批阶段交错与单批内部重叠；材料：课程网页 comparison表A；框架节点检查：TBO／SBO；固定源码核验：SGLang@43a3f956cb0c9fe9b7b7a042af8d8743176b9dba: python/sglang/srt/batch_overlap/two_batch_overlap.py:949–1009；batch_overlap/single_batch_overlap.py:28–59、81–144；models/deepseek_v2.py:1529–1535、1572–1615；证据为固定源码的调用与条件，不是设备运行或性能实测。；追加限定：DeepEP LL为compute_overlap_args所需的三维专家槽位布局；single_batch_overlap.py:32–52要求SBO启用并按runner及Blackwell分支选择机制，models/deepseek_v2.py:1530排除NextN。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "sglang-moe-overlap",
        "fact_scope": {
          "commit": "43a3f956cb0c9fe9b7b7a042af8d8743176b9dba",
          "kind": "snapshot",
          "product": "sglang"
        },
        "recall_target": "区分sglang的双微批阶段交错与单批内部重叠"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3d93d2812715fe3dfd3076f6",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "108ecbbec31163b0e88e0e1185340a3d06633617f3ecd9fead2c8e116a927cac",
      "content_summary": "覆盖o1/o4：把模型并行配置映射到专家并行组。材料：ChangeCard02§4并行配置与审稿补充。源码d7ada3a fused_moe/config.py:1106-1114、1198-1244；v0.30.0同类路径已窄对照。8×4×1=32由工具复算，不作为性能数据。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-parallel-configuration",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "区分全局tp配置与启用ep后的专家tp和ep组范围"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4083d15dec700de28aa4896f",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0a691b198bac7043fb00591d9cc66e1e0a6cdae22b6bec1fd1b78efe56334a3e",
      "content_summary": "覆盖o2/o4：P/F容量接口与Experts工作区。材料：ChangeCard02§5容量映射。源码d7ada3a oracle/unquantized.py:533-546；experts/fused_batched_moe.py:865-885；all2all_utils.py:251-270。A理由：防止总容量被再次乘dispatcher数量，造成通信输出与计算workspace契约不一致。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-experts-buffer-contracts",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "将p/f每rank上限与dispatcher数量映射到每专家总容量"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-411cf42c374113d7e64eab2f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7437c4def8a6bd861159d1ce97481495dee2f732f27caf16dcf612d4cb8eb14d",
      "content_summary": "覆盖o1/o4：输入加权分支的源码补正。材料：ChangeCard02§2与§3加权责任，审稿记录。源码d7ada3a prepare_finalize/deepep_ll.py:278-284、378-403；modular_kernel.py:286-307、375-396。A理由：避免已在输入端施权后combine再次乘原权重，改变输出数值。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "vllm-router-weight-placement",
        "fact_scope": {
          "commit": "d7ada3aace051fecec553c185225db2259c2ac6a",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "解释deepep ll输入施权模式如何避免combine重复加权"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-38c959e8575cba3ebb9ffe21",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card",
        "w2-ledger"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "76eae507975e65eb8a100ae664382bbc941ad9da7699e7bf9af168e90d799f64",
      "content_summary": "B理由：回答拓扑感知通信为何采用两级转发。材料：讲义 synthesis/comparison；验收记录§路线节点5。源码 d4f41e4：deep_ep/buffers/legacy.py:334-337；csrc/kernels/legacy/internode.cu:628-677、968-993、2079-2129。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-communication-topology",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "解释deepep v1 ht跨节点两级转发与反向局部归并"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-87d6421dfb26070f1ff6946e",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c403e0548d90081a60447284843eed561bb18b41512990a35b366de1edf89739",
      "content_summary": "B理由：避免把HT主机同步写成无例外通则。材料：讲义HT步骤及验收6参考；验收记录节点5、验收6。源码 d4f41e4：deep_ep/buffers/legacy.py:293-319、354-355、377-401；csrc/legacy/buffer.hpp:532-539、549-603、1084-1108。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-allocation-protocols",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "定位deepep v1 ht计数等待与动态输出分配及例外"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f7bfdcbb6d618ea751a629d9",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6505d8d2232eaf5c1ebdf80b974b6c9999be48e8b0724503f7acd1956879d9c4",
      "content_summary": "B理由：补齐实际接口中的两类路由载体。材料：讲义add-10-1及布局表；ChangeCard§2。源码 d4f41e4：csrc/kernels/legacy/intranode.cu:362-392；deep_ep/buffers/legacy.py:388-405、408-455。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-routing-layouts",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "辨别deepep ht收到的token行专家路由与逆向handle"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-03e1c8c25f1c0cd418456715",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3424bf77de9b7db0c91c51d8fb189837e785d2d72282dd8413b6b3c65d5a46b8",
      "content_summary": "B理由：解释HT与LL的消息量和布局差异。材料：讲义LL步骤、布局表及两类路由补充；验收记录节点6。源码 d4f41e4：csrc/kernels/legacy/internode_ll.cu:209、253-277；csrc/legacy/config.hpp:134-166；csrc/legacy/buffer.hpp:1516-1521。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-routing-layouts",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "解释deepep ll按专家发送与固定接收分段"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f1e42d2cf27978369eac0de5",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9b86372d05820fd357dcd526dd2ef2341a36bd68668dbde3e809eba866662ecd",
      "content_summary": "B理由：准确区分分段kernel和网卡推进。材料：讲义LL步骤；ChangeCard§3、§5。源码 d4f41e4：csrc/legacy/buffer.hpp:1507-1513、1577-1592；csrc/kernels/legacy/internode_ll.cu:263-271、323-338、379-407。；2026-11-03复核：主目标保留为分段提交与完成协议下的重叠窗口；零行信号编码标为延伸，不要求与窗口边界同时独立回忆。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-completion-protocols",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "解释deepep ll分段提交完成信号与零sm窗口边界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d1cc666d10bc507528e4e265",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d731945b043a9dd8f5644568f175078a4f270b5233b37c2c629514c1dbad81ef",
      "content_summary": "B理由：纠正普通输出与内部发送视图的混淆。材料：ChangeCard§5；讲义两类路由补充。源码 d4f41e4：csrc/legacy/buffer.hpp:1516-1521、1655-1663、1717-1728；csrc/kernels/legacy/internode_ll.cu:408-436；deep_ep/buffers/legacy.py:610-621、646-652。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-buffer-ownership",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "辨别deepep ll普通输出与zero-copy发送视图及调用方输出"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-07791d48c6f05d757be79c51",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-card",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0813d40feb5337c54c74538ede7edfe1516a072d951771948c856ef771105b3d",
      "content_summary": "A理由：防止固定容量输出的无效尾部污染真实路由和结果。材料：讲义V2步骤及计数表；验收记录节点7。源码 d4f41e4：deep_ep/buffers/elastic.py:758-764；csrc/elastic/buffer.hpp:977-1050；deep_ep/include/deep_ep/impls/dispatch_copy_epilogue.cuh:57-80、102-116。；2026-11-03复核：沿原输出容量目标补明最坏路由与平均实收不同，避免把满批输入等同于上界全部有效；来自既有节点检查与已固定分配分支，不加入性能推断。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-output-allocation",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "按deepep v2的同步与展开开关判断输出容量和有效行"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-dd81e7bc1ccbdb327767771c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dadf3c45612c5820b553dd8665e1cf26b0df0780d3557d159aecfa16adf91a8b",
      "content_summary": "B理由：解释V2与HT先等计数再发送的不同流水。材料：讲义V2步骤；验收记录节点7-8。源码 d4f41e4：deep_ep/include/deep_ep/impls/dispatch.cuh:78-105、150-157、246-262、330-384、391-402；csrc/kernels/elastic/dispatch.hpp:126-151；impls/dispatch_copy_epilogue.cuh:57-80、111-116。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-dispatch-pipelines",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "解释deepep v2本地领槽并行计数与拷出流水"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-20e69924a14dc55b64e6d647",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0b6c007724aa4a8601f5a7dff493147ed4bc416de22da782645151bc71e73ea0",
      "content_summary": "B理由：防止把相近名称当成兼容接口。材料：验收记录源码基线表及名称区分；讲义代码地图。源码：d4f41e4 deep_ep/__init__.py:87-97、csrc/kernels/backend/nccl.cu:56-59、102-120；4e890fd deep_ep/hybrid_ep_buffer.py:60；f6aa38f README.md:11-18、deep_ep/__init__.py:59-79。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "moe-library-version-boundaries",
        "fact_scope": {
          "kind": "snapshot",
          "product": "deepep",
          "version": "v1/v2 commit d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb; hybrid-ep commit 4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6; v2.5 commit f6aa38fe06cd4a0489e7730365d4e0114970a2f3"
        },
        "recall_target": "区分deepep版本接口传输模式与独立hybridep分支"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-87a2eea55e446b75cac448b4",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d332e6d1558af6bda047e7c8abd97ecfc33b9c1a9adb722bbda17962cfafac5d",
      "content_summary": "B理由：说明共享池在真实实现中的分配粒度与代价。材料：讲义MORI步骤；验收记录节点8。源码 2d4c3e2：src/ops/dispatch_combine/intranode.hpp:121-165、167-214；include/mori/ops/dispatch_combine/dispatch_combine.hpp:160-169。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-shared-receive-pools",
        "fact_scope": {
          "commit": "2d4c3e2748b9329b2e0fc90e12f449231b4691ed",
          "kind": "snapshot",
          "product": "mori-ep"
        },
        "recall_target": "解释mori intranode两级领槽与容量控制"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-50a37c7580427893d3cfc1cd",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "35fd59e0b901602511e677453d924f60e2d3b57d5a10e0b1a83b478db1f52b7c",
      "content_summary": "A理由：防止把未完成载荷或错误计数交给Experts，污染真实结果。材料：讲义MORI步骤、两类路由补充及验收4；ChangeCard§2。源码 2d4c3e2：src/ops/dispatch_combine/intranode.hpp:200-203、259-299；python/mori/ops/dispatch_combine.py:1347-1400；src/ops/dispatch_combine/ep_local_expert_count.hpp:29-40。；2026-11-03复核：把题面收束为“从领槽到可交付的有效行数”这一条闭合数据流；独立的专家路由载体细节标为延伸。完成证据与total_recv计数对象仍保留原回忆目标。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-completion-metadata",
        "fact_scope": {
          "commit": "2d4c3e2748b9329b2e0fc90e12f449231b4691ed",
          "kind": "snapshot",
          "product": "mori-ep"
        },
        "recall_target": "辨别mori共享池分配完成与有效行总数语义"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b7df7e939424aa7a39a58e6b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fa7c0f9aeb1a98678baa67a13de90d805d789a6344e5d20cb49bdfb09e8e15ee",
      "content_summary": "A理由：定位真实后端的micro-batch交错污染，而非只做一般生命周期提醒。材料：讲义两类路由补充及验收2；验收记录验收2；ChangeCard§2、§3。源码 2d4c3e2：python/mori/ops/dispatch_combine.py:992-1013、1100-1130、1184-1212、1361-1400、1509-1513、1784-1805；src/ops/dispatch_combine/intranode.hpp:188-190、578-588。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-buffer-ownership",
        "fact_scope": {
          "commit": "2d4c3e2748b9329b2e0fc90e12f449231b4691ed",
          "kind": "snapshot",
          "product": "mori-ep"
        },
        "recall_target": "诊断mori交错调用中的数据视图和路由状态覆盖"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-35c9c361d6e1758a42f5fe10",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "704f10c10aa6e21f85d809a9946ad4b4c0439e1c12b236516b48fdb42bc44811",
      "content_summary": "B理由：补齐MORI跨节点路径与节点内路径的实现差异。材料：讲义comparison传输行及图10.2说明；验收记录源码基线指定MORI-EP-GUIDE。源码2d4c3e2：python/mori/ops/dispatch_combine.py:1284-1296；src/ops/dispatch_combine/internode_v1.cpp:150-231、274-284、361-397、414-471、623-681。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-communication-topology",
        "fact_scope": {
          "commit": "2d4c3e2748b9329b2e0fc90e12f449231b4691ed",
          "kind": "snapshot",
          "product": "mori-ep"
        },
        "recall_target": "解释mori internodev1跨节点中继与完成条件"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9f06787bb50e7439621c134b",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e2f195e1deef82a4f790fb51cc4f36b62cff86a473fb86d45b47d239d3035fc7",
      "content_summary": "B：具有跨库迁移价值，可区分控制信息与实际载荷。材料：课程HTML synthesis、comparison，W2历史o3场景表。源码4e890fd：csrc/hybrid_ep/hybrid_ep.cu:136-170；csrc/hybrid_ep/executor/executor.cu:23-72、158-198；deep_ep/hybrid_ep_buffer.py:599-651、668-717；docs/Hybrid-EP_Implementation.md:352-363、418-459。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "解释hybrid-ep全收集路由元数据如何决定后续载荷传输与专家布局"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-ee164f717c744408ef1f3e7c",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8d2d2fe8e14cbe85579b761cafad9cd1a28a7b5f1ca7549ddca87d8aae2ed3e5",
      "content_summary": "B：用于迁移分析通信路径和硬件依赖，不要求背诵warp数量。材料：课程HTML synthesis第七节、comparison传输行。源码4e890fd：docs/Hybrid-EP_Implementation.md:465-501、507-519；csrc/hybrid_ep/executor/executor.cu:255-295；csrc/hybrid_ep/backend/hybrid_ep_backend.cuh:126-135、1364-1402、1665-1682。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "解释hybrid-ep分层传输与warp流水分别优化的路径环节"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-50ea6c480c0d43fe0a0508a4",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4aba86a571962a1b94f34044da01bef58b0366a64dd02cafca3934d6c4c37fd7",
      "content_summary": "B：可迁移到ragged collective的统一形状设计。材料：W2历史记录o3 prefill②、导师对空行通信的更正；课程HTML参数对照。源码4e890fd：deep_ep/hybrid_ep_buffer.py:165-232、368-374；csrc/hybrid_ep/executor/executor.cu:32-60；docs/Hybrid-EP_Implementation.md:235-248。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "解释hybrid-ep不等长输入如何借助统一槽位数保持布局一致并区分padding成本"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f80ff5e3939e02b6104c7662",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3848d9f2a6b672134df0766e0354014df7add3c9c40484cfe04e48ea2a180939",
      "content_summary": "A理由：防止前后向间复用失效通信状态，导致错误结果或无法完成的等待。材料：W2历史o3训练①、prefill①；课程HTML完成与复用。源码4e890fd：deep_ep/hybrid_ep_buffer.py:191-209、390-426、611-630；csrc/hybrid_ep/hybrid_ep.cu:109-133；tests/test_ragged_hybrid_ep.py:274-297、452-494。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "判断hybrid-ep训练前后向缓存handle的复用前提与buffer代次失效"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9fc4d8a4a246584f1ee0ba8f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "83918c56c3c701ba6400ce96fff58b0bfc1ddc0181d908ac173feed4f0c21b01",
      "content_summary": "A理由：防止将能录图误当作无丢弃，以及忽略逐专家padding造成容量不足。材料：W2历史o3 decode①、padding更正；课程HTML计数与接收空间。源码4e890fd：deep_ep/hybrid_ep_buffer.py:515-538、576-581；csrc/hybrid_ep/executor/executor.cu:171-198；csrc/hybrid_ep/hybrid_ep.cu:333-340；csrc/hybrid_ep/backend/hybrid_ep_backend.cuh:5370-5408。保守上界按题设由源码布局推导，不是实测建议。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "为hybrid-ep非阻塞录图输出建立计入每专家padding的无丢弃容量条件"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-2979889096ce057fe64b86ab",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a6140ab94198f234bdb96a211d190243c715904d87a3a300c568055cfdd7f25d",
      "content_summary": "A理由：防止把实现层容量保护当作模型语义，静默改变输出。材料：W2历史o3训练②；课程HTML计数与接收空间。源码4e890fd：csrc/hybrid_ep/executor/executor.cu:158-169；csrc/hybrid_ep/jit/compiler.cu:315-329（调用端传入enable_permute）；csrc/hybrid_ep/backend/hybrid_ep_backend.cuh:5380-5411、5646-5650；deep_ep/hybrid_ep_buffer.py:268-269、534。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "区分hybrid-ep容量截断机制与模型训练中的路由丢弃策略"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9ddb96841d288103a24cf440",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "89adbf68ee791eccd37d75db6de0c75181ab964c5198d6b61a0cd5514b7d7695",
      "content_summary": "A理由：防止把返回新张量误推为通信内部状态可以任意并发复用。材料：W2历史o3训练③；课程HTML完成与复用。源码4e890fd：csrc/hybrid_ep/buffer/intranode.cu:204-212；csrc/hybrid_ep/hybrid_ep.cu:333-340；csrc/hybrid_ep/executor/executor.cu:396-408、461-467、491-493；docs/Hybrid-EP_Implementation.md:320-324。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "区分hybrid-ep独立计算输出与内部共享通信区的并发复用约束"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3dba932d0ea7abc437c403c9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cc1084a3769288aca80c57f4a0f8c3d47c1af13a89110c208fa88b83ef33cc48",
      "content_summary": "B：避免把容量参数与每步工作量混为一谈，可迁移到其他预分配通信库。材料：W2历史o3 prefill①、decode②；课程HTML参数对照。源码4e890fd：deep_ep/hybrid_ep_buffer.py:308-315、587-609；csrc/hybrid_ep/buffer/intranode.cu:126-130、198-201；csrc/hybrid_ep/executor/executor.cu:32-60、103-149；csrc/hybrid_ep/hybrid_ep.cu:333-340。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "ai-infra-moe",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "在hybrid-ep混合prefill与decode部署中区分常驻容量和每步处理规模"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a66576e8728d34795904a60a",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "03a658ee39ea20cfff741a0ba56af1c4b5495e0c69e3f99e9ed88796701c6510",
      "content_summary": "覆盖o1/o4，组合本请求5张已核验框架子卡；不增加子卡以外的实现结论。A理由：支撑面试中完整解释两套真实框架接入边界，避免只列组件名称。",
      "dependency_content_sha256": {
        "mc-7315df9206599ae11b928dd1": "55f8aaff9495cefa31d56c8d7b95a8a6fb0ff5c61a7f0b95733167709d65c1ad",
        "mc-76597101ebd26c3464b19ade": "cf8c40c1d53d0737d7e84d9ecd3ec03239cc3a1ce68d1334c1348444cf3139e8",
        "mc-a0f44f7d2979c0475db2464d": "a79ab4991fee64f6a9731641acaec9a0afecaa2b6d51d414201592272daf8a84",
        "mc-a0f7983e098e635a1ee52dd6": "57049ed9b763d801cd985a772106c9c9c0282defee8c1094541bd1fef74640c4",
        "mc-d653cd227e78ceea04297406": "8a36ac7556d0fd6e434e0f8d943e9824e5d256122f48643115ae34775cb84501"
      },
      "depends_on": [
        "mc-7315df9206599ae11b928dd1",
        "mc-76597101ebd26c3464b19ade",
        "mc-a0f44f7d2979c0475db2464d",
        "mc-a0f7983e098e635a1ee52dd6",
        "mc-d653cd227e78ceea04297406"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "moe-framework-comparison",
        "fact_scope": {
          "kind": "snapshot",
          "product": "vllm + sglang",
          "version": "vllm d7ada3a / sglang 43a3f95"
        },
        "recall_target": "向面试官对照vllm和sglang的真实moe接入主链"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-2d6e4a350130076b75a27605",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "2026-11-16 已按语言改写后的依赖卡逐项复核本卡的结论、适用条件与评分锚点；独立语言审查通过，仍覆盖原考查目标，不改变固定版本与实证边界。"
      },
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "469c44460c38279a5bba92e0c84c4ac6cd2bfe51a81741c0c5034abf524312d4",
      "content_summary": "覆盖o2/o4，组合5张同请求已核验实现卡；不承诺跨平台性能排名。A理由：回答面试中的四路径取舍问题，防止把容量、计数与有效布局混为同一种机制。",
      "dependency_content_sha256": {
        "mc-50a37c7580427893d3cfc1cd": "d332e6d1558af6bda047e7c8abd97ecfc33b9c1a9adb722bbda17962cfafac5d",
        "mc-b7df7e939424aa7a39a58e6b": "35fd59e0b901602511e677453d924f60e2d3b57d5a10e0b1a83b478db1f52b7c",
        "mc-dd81e7bc1ccbdb327767771c": "0813d40feb5337c54c74538ede7edfe1516a072d951771948c856ef771105b3d",
        "mc-f1e42d2cf27978369eac0de5": "3424bf77de9b7db0c91c51d8fb189837e785d2d72282dd8413b6b3c65d5a46b8",
        "mc-f7bfdcbb6d618ea751a629d9": "c403e0548d90081a60447284843eed561bb18b41512990a35b366de1edf89739"
      },
      "depends_on": [
        "mc-50a37c7580427893d3cfc1cd",
        "mc-b7df7e939424aa7a39a58e6b",
        "mc-dd81e7bc1ccbdb327767771c",
        "mc-f1e42d2cf27978369eac0de5",
        "mc-f7bfdcbb6d618ea751a629d9"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "moe-communication-implementation-comparison",
        "fact_scope": {
          "kind": "snapshot",
          "product": "deepep + mori-ep",
          "version": "deepep v1/v2 d4f41e4 / mori-ep 2d4c3e2"
        },
        "recall_target": "按计数容量和布局比较ht ll v2与mori的实现取舍"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-2f3f4b0d53d2559dfc94b6e1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "2026-11-16 已按语言改写后的依赖卡逐项复核本卡的结论、适用条件与评分锚点；独立语言审查通过，仍覆盖原考查目标，不改变固定版本与实证边界。"
      },
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "475685370b2e76887dce6a3561deb594eb930cfa38d3c500bb051b44cb071fbe",
      "content_summary": "覆盖o3/o4，组合5张同请求Hybrid-EP快照子卡。A理由：支撑训练/prefill/decode迁移面试题，并防止将设计推导包装成生产性能证据。",
      "dependency_content_sha256": {
        "mc-2979889096ce057fe64b86ab": "83918c56c3c701ba6400ce96fff58b0bfc1ddc0181d908ac173feed4f0c21b01",
        "mc-3dba932d0ea7abc437c403c9": "89adbf68ee791eccd37d75db6de0c75181ab964c5198d6b61a0cd5514b7d7695",
        "mc-9fc4d8a4a246584f1ee0ba8f": "3848d9f2a6b672134df0766e0354014df7add3c9c40484cfe04e48ea2a180939",
        "mc-ee164f717c744408ef1f3e7c": "e2f195e1deef82a4f790fb51cc4f36b62cff86a473fb86d45b47d239d3035fc7",
        "mc-f80ff5e3939e02b6104c7662": "4aba86a571962a1b94f34044da01bef58b0366a64dd02cafca3934d6c4c37fd7"
      },
      "depends_on": [
        "mc-2979889096ce057fe64b86ab",
        "mc-3dba932d0ea7abc437c403c9",
        "mc-9fc4d8a4a246584f1ee0ba8f",
        "mc-ee164f717c744408ef1f3e7c",
        "mc-f80ff5e3939e02b6104c7662"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "hybrid-ep-scenario-adaptation",
        "fact_scope": {
          "commit": "4e890fd19a3a52f23cc7bd38a0d9b0b1276f70d6",
          "kind": "snapshot",
          "product": "deepep hybrid-ep"
        },
        "recall_target": "向面试官解释hybridep在训练变长prefill与graph decode中的适配"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-5f8607e9b42c31251fcaf076",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "2026-11-16 已按语言改写后的依赖卡逐项复核本卡的结论、适用条件与评分锚点；独立语言审查通过，仍覆盖原考查目标，不改变固定版本与实证边界。"
      },
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "36d468b88f9fa96027aaa33fb52ce02994861f601529f27ac666b293f8c3ef3c",
      "content_summary": "A理由：防止把双缓冲索引轮换当成自动忙闲检测，提前复用慢rank仍在读取的槽位或清掉未消费信号。已对照课程页add-10-2、ChangeCard02§5及DeepEP d4f41e4固定源码：internode_ll.cu:286–295、329–338、379–407、776–785、915–976；buffer.hpp:1504–1505、1577–1592、1644–1645、1696–1711。固定源码因果解释，不是实测轨迹。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "deepep-ll-reuse-protocol",
        "fact_scope": {
          "commit": "d4f41e4e93602a15e95f55f6ee8df8f1aaa0e4bb",
          "kind": "snapshot",
          "product": "deepep"
        },
        "recall_target": "解释deepep ll中间轮信号如何证明慢rank旧槽可复用"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-467846640b25015ee66a6a1f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b9a2a2661eff5d3c5822427925d445f573f7c2016f4276b4617f53192fddd341",
      "content_summary": "A理由：回答适配正确性如何验证与定位的面试题，防止通信单测通过就宣称整层正确，或等权重用例掩盖加权错误。素材为ChangeCard02§7已明确的B级测试设计；只转成常青方法，不生成运行结果。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "moe-adapter-validation",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用通信契约与完整单层两层参考定位moe适配错误"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-8a1f8d9122f897096bc8dfd3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "w2-card"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "d5dab95939f7564308d06d138b63be03ef100e5217afc6a2248262330e794382",
  "manifest_payload_sha256": "0b9b5a8bf0f438eccf98beb7fb8207a56ca73c9d8bd26d42721b8f38ac2ed849",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 63470,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/2026-10-29-w2-u2-implementations-technical-qa.xlsx",
      "row_count": 38,
      "rows": [
        {
          "content_sha256": "a79ab4991fee64f6a9731641acaec9a0afecaa2b6d51d414201592272daf8a84",
          "logical_id": "mc-a0f44f7d2979c0475db2464d",
          "row_sha256": "aee0d241930ec1b031f421d77968660cfd9262c8bb57116b741a3c416394c705"
        },
        {
          "content_sha256": "57049ed9b763d801cd985a772106c9c9c0282defee8c1094541bd1fef74640c4",
          "logical_id": "mc-a0f7983e098e635a1ee52dd6",
          "row_sha256": "9fc74df3b854c8925a4deac30dcc40fbd8b63ed48a758c7b548dc46fec2be3cc"
        },
        {
          "content_sha256": "57474bb3aa43492a9f8d42328155624f8831cd0a8992d41ddfbadb2fcce34bbf",
          "logical_id": "mc-c08c9e1e782b5f1fca6126a2",
          "row_sha256": "50041a596a2d1e2bc77aa4f9b65da964950806b65d61d6121b0b6f1b88e20d43"
        },
        {
          "content_sha256": "55f8aaff9495cefa31d56c8d7b95a8a6fb0ff5c61a7f0b95733167709d65c1ad",
          "logical_id": "mc-7315df9206599ae11b928dd1",
          "row_sha256": "dea5a113ab1853475142e3ec8f12d05505d12cd6203c9bc9ad695fcbd969b5bc"
        },
        {
          "content_sha256": "4f1d8898adcaef5bc5c9c3be0d2e71dfd693e43e47a935798f5be3a28cb9866c",
          "logical_id": "mc-486a27f672d2edbf1836e411",
          "row_sha256": "a61905f028c3c7db5427ab6bbd2843a18535d0af7c398a7dcc6d6023133858ad"
        },
        {
          "content_sha256": "1c951d59fe8eb471d8b1488093df0cb1cdf3adb20d350587b5b584f4c8468a50",
          "logical_id": "mc-eb769bec52690bea988517de",
          "row_sha256": "61a3e349a3dae1fe083a8ae9f3bbe0132f9774ffaab0c6cef0d31e9ef668aa6b"
        },
        {
          "content_sha256": "f430b82f4c529cc0d7b7850541dae886c9f848b2a51d5127ff093839f1f33981",
          "logical_id": "mc-99fe51c2ea71d50056eaf79f",
          "row_sha256": "3c5ed4ff16d3f017d8ba760ac4bbcd51e1dc4bc63109aafc47684e9ed0196c5d"
        },
        {
          "content_sha256": "de131f36dd9c18557e8e504108eaab3bad34ac94a55c5140a8eefa33e8bdedb2",
          "logical_id": "mc-a4baf65139adf754752ce42e",
          "row_sha256": "001c7ffa390e2a48b1bb20768a29f4d70198796c662736e773928832a4db547b"
        },
        {
          "content_sha256": "cf8c40c1d53d0737d7e84d9ecd3ec03239cc3a1ce68d1334c1348444cf3139e8",
          "logical_id": "mc-76597101ebd26c3464b19ade",
          "row_sha256": "70c68e7a9d8b1adb7150ce806109164a319f12b07e6d978d491da1bb9a9c8740"
        },
        {
          "content_sha256": "8a36ac7556d0fd6e434e0f8d943e9824e5d256122f48643115ae34775cb84501",
          "logical_id": "mc-d653cd227e78ceea04297406",
          "row_sha256": "87eabe827017d4746a65087e4296c796a42c71a0485c6a1cbeca3753b9d5de4e"
        },
        {
          "content_sha256": "52b06dd04c5fb650f1860fcd2985bf01cb45260294cfa4b64458b721590f0eda",
          "logical_id": "mc-763557e86a5e94c61a29de1f",
          "row_sha256": "6470405dad72b59acdcf33f4bf5efe17cc8e0d7901a094c02349726712b55450"
        },
        {
          "content_sha256": "870fb9923e45fd137d8105823188aed4764dc9da0c969320b51b2788445f38fd",
          "logical_id": "mc-3d93d2812715fe3dfd3076f6",
          "row_sha256": "6adcfa56d75d65a882926c471f52e877586427306803e00f663959a25e060881"
        },
        {
          "content_sha256": "108ecbbec31163b0e88e0e1185340a3d06633617f3ecd9fead2c8e116a927cac",
          "logical_id": "mc-4083d15dec700de28aa4896f",
          "row_sha256": "ecaa71532a8952281a1e5f0667ddbbdb239282be8a42656b10bdc29c05459d38"
        },
        {
          "content_sha256": "0a691b198bac7043fb00591d9cc66e1e0a6cdae22b6bec1fd1b78efe56334a3e",
          "logical_id": "mc-411cf42c374113d7e64eab2f",
          "row_sha256": "4cd0b9501a82f5eb9aa8791d26b1749eca76e08da068e614dd788d147b6ae7e4"
        },
        {
          "content_sha256": "7437c4def8a6bd861159d1ce97481495dee2f732f27caf16dcf612d4cb8eb14d",
          "logical_id": "mc-38c959e8575cba3ebb9ffe21",
          "row_sha256": "7923e80b8a272392f90cfaff2a7aba1f44b4b5f9d1c0e6ebb238996ba744fe95"
        },
        {
          "content_sha256": "76eae507975e65eb8a100ae664382bbc941ad9da7699e7bf9af168e90d799f64",
          "logical_id": "mc-87d6421dfb26070f1ff6946e",
          "row_sha256": "af735cc2f13748bbbb3d9d01a1bb9a36331d36b3f4cfc1e1b17300e22db16805"
        },
        {
          "content_sha256": "c403e0548d90081a60447284843eed561bb18b41512990a35b366de1edf89739",
          "logical_id": "mc-f7bfdcbb6d618ea751a629d9",
          "row_sha256": "953682766310ca5868999d93988b972587c109be5ea9d965337aa1331d3a2908"
        },
        {
          "content_sha256": "6505d8d2232eaf5c1ebdf80b974b6c9999be48e8b0724503f7acd1956879d9c4",
          "logical_id": "mc-03e1c8c25f1c0cd418456715",
          "row_sha256": "24318553cfde8b37567e1fa69e18ef75b5bb5adb482b8b8132442f813e05226c"
        },
        {
          "content_sha256": "3424bf77de9b7db0c91c51d8fb189837e785d2d72282dd8413b6b3c65d5a46b8",
          "logical_id": "mc-f1e42d2cf27978369eac0de5",
          "row_sha256": "2af60b9b230ab7af11d0dcba6dbb2865108a414cacbd5c928b17727d9965af6b"
        },
        {
          "content_sha256": "9b86372d05820fd357dcd526dd2ef2341a36bd68668dbde3e809eba866662ecd",
          "logical_id": "mc-d1cc666d10bc507528e4e265",
          "row_sha256": "4872a19875aadb665bf922b10fda63cd9d467213eeb5278e074637493d8b1278"
        },
        {
          "content_sha256": "d731945b043a9dd8f5644568f175078a4f270b5233b37c2c629514c1dbad81ef",
          "logical_id": "mc-07791d48c6f05d757be79c51",
          "row_sha256": "9377828a3544d7ff1a3042a049989c4190db7abadee7ed8c3096051d2de6718d"
        },
        {
          "content_sha256": "0813d40feb5337c54c74538ede7edfe1516a072d951771948c856ef771105b3d",
          "logical_id": "mc-dd81e7bc1ccbdb327767771c",
          "row_sha256": "98682f9fb3f02584488e2eec4a5414d3f34e11eef1a03f35887b05400ba9d3a5"
        },
        {
          "content_sha256": "dadf3c45612c5820b553dd8665e1cf26b0df0780d3557d159aecfa16adf91a8b",
          "logical_id": "mc-20e69924a14dc55b64e6d647",
          "row_sha256": "d6a76ef6824d314df02947788c00f608f93b8cd285dd1b558ad7f663e14dca3a"
        },
        {
          "content_sha256": "0b6c007724aa4a8601f5a7dff493147ed4bc416de22da782645151bc71e73ea0",
          "logical_id": "mc-87a2eea55e446b75cac448b4",
          "row_sha256": "a52e0c5549f3772e2d4beb7ff4a30ad7f758d42dca1336564527620bcb15bb55"
        },
        {
          "content_sha256": "d332e6d1558af6bda047e7c8abd97ecfc33b9c1a9adb722bbda17962cfafac5d",
          "logical_id": "mc-50a37c7580427893d3cfc1cd",
          "row_sha256": "1e102a8d8fa75d26b6980737773ec330890d7c7bb4ca0c665e61fb4fe8617a8d"
        },
        {
          "content_sha256": "35fd59e0b901602511e677453d924f60e2d3b57d5a10e0b1a83b478db1f52b7c",
          "logical_id": "mc-b7df7e939424aa7a39a58e6b",
          "row_sha256": "33e789e89666ae30d3a220364c7af13d71df4bb7cfb3c359d7e530a27d7d79c3"
        },
        {
          "content_sha256": "fa7c0f9aeb1a98678baa67a13de90d805d789a6344e5d20cb49bdfb09e8e15ee",
          "logical_id": "mc-35c9c361d6e1758a42f5fe10",
          "row_sha256": "726d39622f664faa1fe5fa3819f6f9dbeb7494b724a70930196787d28e5954c3"
        },
        {
          "content_sha256": "704f10c10aa6e21f85d809a9946ad4b4c0439e1c12b236516b48fdb42bc44811",
          "logical_id": "mc-9f06787bb50e7439621c134b",
          "row_sha256": "33e2b69841fb25fcdb8c2aa85323006be23629fae99a7e201905722762d5fb49"
        },
        {
          "content_sha256": "e2f195e1deef82a4f790fb51cc4f36b62cff86a473fb86d45b47d239d3035fc7",
          "logical_id": "mc-ee164f717c744408ef1f3e7c",
          "row_sha256": "1802e119246dcb9ea4bbe9a7fa4c47467c138152d35b491f07c5ff6092c01675"
        },
        {
          "content_sha256": "8d2d2fe8e14cbe85579b761cafad9cd1a28a7b5f1ca7549ddca87d8aae2ed3e5",
          "logical_id": "mc-50ea6c480c0d43fe0a0508a4",
          "row_sha256": "eb20de4b22ca838e96b0687d4815d528e42b05c0a3004f938af0077f78cecf9e"
        },
        {
          "content_sha256": "4aba86a571962a1b94f34044da01bef58b0366a64dd02cafca3934d6c4c37fd7",
          "logical_id": "mc-f80ff5e3939e02b6104c7662",
          "row_sha256": "b2868324c6c93269f616162a04d340642d12a62322977043ffe9286798ad058f"
        },
        {
          "content_sha256": "3848d9f2a6b672134df0766e0354014df7add3c9c40484cfe04e48ea2a180939",
          "logical_id": "mc-9fc4d8a4a246584f1ee0ba8f",
          "row_sha256": "ba26b03ab660edcf7e8af4f0d11b578b2d92311d160cf739fc4ae4315e4e4b17"
        },
        {
          "content_sha256": "83918c56c3c701ba6400ce96fff58b0bfc1ddc0181d908ac173feed4f0c21b01",
          "logical_id": "mc-2979889096ce057fe64b86ab",
          "row_sha256": "b54ca2a6a98beb48c1364a000787d3c4c1eb14d95a995c111de7088339ce7083"
        },
        {
          "content_sha256": "a6140ab94198f234bdb96a211d190243c715904d87a3a300c568055cfdd7f25d",
          "logical_id": "mc-9ddb96841d288103a24cf440",
          "row_sha256": "8d649287e20537bb6e8dc03fe76ffd36cbf51f4efec228922665485a3d2f3d19"
        },
        {
          "content_sha256": "89adbf68ee791eccd37d75db6de0c75181ab964c5198d6b61a0cd5514b7d7695",
          "logical_id": "mc-3dba932d0ea7abc437c403c9",
          "row_sha256": "3f37fb30230f568fee582a3973e475c686be82f22aa16cc891929304024dc750"
        },
        {
          "content_sha256": "cc1084a3769288aca80c57f4a0f8c3d47c1af13a89110c208fa88b83ef33cc48",
          "logical_id": "mc-a66576e8728d34795904a60a",
          "row_sha256": "17e23697c3f577075a5fd595a1bddaefde250879f5298f3dc39f1cf06afef2bd"
        },
        {
          "content_sha256": "36d468b88f9fa96027aaa33fb52ce02994861f601529f27ac666b293f8c3ef3c",
          "logical_id": "mc-467846640b25015ee66a6a1f",
          "row_sha256": "ab4d15157800257329852bcdc9b3b0352e55194fd088de967968238debefb5de"
        },
        {
          "content_sha256": "b9a2a2661eff5d3c5822427925d445f573f7c2016f4276b4617f53192fddd341",
          "logical_id": "mc-8a1f8d9122f897096bc8dfd3",
          "row_sha256": "b44968b9c8f48b3fcd365af791b16d5317012283037ccc44c03c1d66f09ad08a"
        }
      ],
      "sha256": "e9103e0edb8ad2fe6648cd9876f23036b2f3bb99e0b8960af60a8da97f3217f6",
      "sheet_name": "cards",
      "table_sha256": "3a7c586c159cad8d48169a1f256ba015cc279f44fafec4e89a893a4686024804",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 7456,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/2026-10-29-w2-u2-implementations-oral.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "03a658ee39ea20cfff741a0ba56af1c4b5495e0c69e3f99e9ed88796701c6510",
          "logical_id": "mc-2d6e4a350130076b75a27605",
          "row_sha256": "aa67031cf6e5b760547076d83dfaf3b3296796272e2f9a196b93261671ce1d88"
        },
        {
          "content_sha256": "469c44460c38279a5bba92e0c84c4ac6cd2bfe51a81741c0c5034abf524312d4",
          "logical_id": "mc-2f3f4b0d53d2559dfc94b6e1",
          "row_sha256": "d6aaad8ce597ca301cb12e6d9882985d692b4f329670874aa0e0785b3a47ebc6"
        },
        {
          "content_sha256": "475685370b2e76887dce6a3561deb594eb930cfa38d3c500bb051b44cb071fbe",
          "logical_id": "mc-5f8607e9b42c31251fcaf076",
          "row_sha256": "0e9c586b3cc95476724956fe47b9aa19ffd8c9eb9a0952e4644e672da3722ff7"
        }
      ],
      "sha256": "58f0defaf8a6e386c535592ef282d1758ede5665da5a2c39bb832046edfccaa6",
      "sheet_name": "cards",
      "table_sha256": "2b0e7303b735b69779723ee57cb4b057c69ee1777da79a71458d5b2fb21535eb",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "83a09d4e5e02b8620543f0e3a9459175670490aa3825a7b1b6f715a63f496170",
  "sources": [
    {
      "collection": "inference-w2-u2-evidence",
      "id": "w2-card",
      "path": "面试准备/自我准备/学习设计/ChangeCard-02-MoE-EP-dispatch-combine.md",
      "sha256": "d0a2d2c7917b5717d8da9189c4e53f84f4c2aef363054dd0397a6cdfc732f0b0",
      "summary": "已审核的接入契约与源码纠正；只采用公开固定源码事实，不将用户芯片说明或待验证结果转为确定实现。"
    },
    {
      "collection": "inference-w2-u2-evidence",
      "id": "w2-ledger",
      "path": "计划/八周冲刺进度/历史记录/W2-学习验收记录.md",
      "sha256": "e8e8092a426fff22872f1b4f9a57aaccc8d31015e5859dcb05f1bb43a1b890e9",
      "summary": "单元二固定源码基线、节点检查及已确认的Hybrid-EP场景表；用于确定学习范围和来源锚点，不将mastery状态当知识事实。"
    },
    {
      "collection": "inference-w2-u2-evidence",
      "id": "w2-lesson",
      "path": "课程网页/八周计划/plana-jd-w2-moe-ep-source.html",
      "sha256": "31251f6b8c2eab14beb335864d666aec718d758a7a9ada084ce6875002158d05",
      "summary": "既有源码串讲与横向对照讲义；本批逐项核对固定提交，过强简写以本批明确范围和代码依据为准。"
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

导入文件：[2026-10-29-w2-u2-implementations-technical-qa.xlsx](2026-10-29-w2-u2-implementations-technical-qa.xlsx)（38 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[2026-10-29-w2-u2-implementations-oral.xlsx](2026-10-29-w2-u2-implementations-oral.xlsx)（3 张卡）
