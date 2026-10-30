---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "plana-markji"
  },
  "artifact_set_sha256": "3c407e8be79f2ce9d0ef09a1f5485525f24397daf1bbc86471d4abb7a3d57df7",
  "candidate_sha256": "cac7268111ba02cdba30480306bc03ca22edffd2504695a68d2f050ba900531a",
  "cards": [
    {
      "content_sha256": "87c311f0365befcc4cdcef77a10188ebe9e26823c38a59755387bea941eaf187",
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
      "content_sha256": "ab0e724b395f04f2d8a6a438dddbb1bd5258ad375d08db86acbeff8528fe2948",
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
      "content_sha256": "94797291e359a5ab5e7e810dfa1172b7a0e860f18ff9cd019f1a8b276676618f",
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
      "content_sha256": "be092a0592abaf4cad73a6b4e9c523fb6c010836128053eced7d60f484f01ad8",
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
      "content_sha256": "c1e8bcd4950233b182538ca0f4cddb4f1909675177ad3c1616ba5ed5b4b637b5",
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
      "content_sha256": "b0ae9bc4c4bdb6464ab50b920e5ae5ca7c243fa904c6bac6dc9a1737c1be3d86",
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
      "content_sha256": "2e51771c228bbc896b6741bf3339c91d8fe9ed1608362dd2944bdfc059782b7b",
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
      "content_sha256": "7e855300773b8a43bd1b5b6318ec5f70a3156b7b4d2615aa0a810dbd7267178d",
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
      "content_sha256": "82f26a1c82dc9040dd9a46bb3d73276fbaa980e85e7868a06751ef7918ca3cef",
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
      "content_sha256": "8b4b86293ad0f868b8e4080f7e8a18e428db884f4848493377bfaeaca2470022",
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
      "content_sha256": "09290e3de04d9643f971faecb1ad930ec7633775ca82cba509e1aac7a99bd5f7",
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
      "content_sha256": "d6942bc4d26e7b33b3ee9456c3f47a9b41b5595690cc2ea26eadbeb0433995f2",
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
      "content_sha256": "111db85fa4d8251b8b6c655ab01dbcad017199db26dbe94ef8c325892b2eff39",
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
      "content_sha256": "d28a3ef291772924bedaa4888a9541963d290a50b72fca8d9c0ff8b5d8245846",
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
      "content_sha256": "ea049b24a42af9338c022d843da9f1d004b15c28135fc30af2b1fc538a3da5c1",
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
      "content_sha256": "d1ffabd84e434341c8b19e99b80ed64a609001fab5a692a642de6f463961fb38",
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
      "content_sha256": "1e16582507581de087ec1283e2509560979d27f43e97bca8d5c0f4f1a4a8b923",
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
      "content_sha256": "061616d52974efba347b142e0b94956dc899b0e9f0907344500de63bf41c3ec1",
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
      "content_sha256": "88e7b984787488bbb56ca2ed0208f1a0595a5128899a2ba80510545ef33cf0b7",
      "content_summary": "B理由：准确区分分段kernel和网卡推进。材料：讲义LL步骤；ChangeCard§3、§5。源码 d4f41e4：csrc/legacy/buffer.hpp:1507-1513、1577-1592；csrc/kernels/legacy/internode_ll.cu:263-271、323-338、379-407。",
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
      "content_sha256": "97a14542a4a971eba76ec65a7e3601cd9ced60a40ca6b81b334e87ea23a17cd9",
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
      "content_sha256": "e4303b2dc4cc060f579b9ec9a45fbcb362e5d8ba96475b614636275073e4d31a",
      "content_summary": "A理由：防止固定容量输出的无效尾部污染真实路由和结果。材料：讲义V2步骤及计数表；验收记录节点7。源码 d4f41e4：deep_ep/buffers/elastic.py:758-764；csrc/elastic/buffer.hpp:977-1050；deep_ep/include/deep_ep/impls/dispatch_copy_epilogue.cuh:57-80、102-116。",
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
      "content_sha256": "5da9dda329e2e056d10c9cc3f0935c653d6865817c7bf8c265718b85817bcad4",
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
      "content_sha256": "23876f01e99d4cc4de67169e6fab32ea7fb92430fbe619b3b420c331abbd98ee",
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
      "content_sha256": "3d3d5afb6b346e7d02e608ab87610c2aed236b0112556c65b7c0f314e34e4268",
      "content_summary": "A理由：防止把未完成载荷或错误计数交给Experts，污染真实结果。材料：讲义MORI步骤、两类路由补充及验收4；ChangeCard§2。源码 2d4c3e2：src/ops/dispatch_combine/intranode.hpp:200-203、259-299；python/mori/ops/dispatch_combine.py:1347-1400；src/ops/dispatch_combine/ep_local_expert_count.hpp:29-40。",
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
      "content_sha256": "13a31e4624f182bb957a8f011d02eb6f024744f92f5c997a513a0c194fdf03bf",
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
      "content_sha256": "e13e7e7e4703fc0d476e6fddba59926175a2282d2ff74057ea278890d099c745",
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
      "content_sha256": "ba39b82f6f1125934a997e14936a643229d7dfd6d30bd3438b2bc7a8666ad43e",
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
      "content_sha256": "7d22b922293c5b58209c81fed2dbe058313d09d2ef4f5cde139c097271c97898",
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
      "content_sha256": "396ca917a3718843b9c43455487169d5408a5790227a555f0b11c8e4f9031b3d",
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
      "content_sha256": "a7a2c5a35ea4e33a9f53ecb349fa09ffaad99ecbc3c49b77b7b8b0adbf409e63",
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
      "content_sha256": "5bafc7ef286d7f447883c2a1fa525d57619d44b674bf07e0d885b48d0e235667",
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
      "content_sha256": "fa6cd052574c61f518be0d423ad9c3a0cf921770e86649eec21ef650bad991e7",
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
      "content_sha256": "7e1f013a460e124a4bddcb4d39cd20abc2cb9fbba9ce34a3d95803f8a97e1ffe",
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
      "content_sha256": "dcba8e37dea3d6b8df842f3159191b40bbc7344ccaa83a90e8bccbf971b9c349",
      "content_summary": "覆盖o1/o4，组合本请求5张已核验框架子卡；不增加子卡以外的实现结论。A理由：支撑面试中完整解释两套真实框架接入边界，避免只列组件名称。",
      "dependency_content_sha256": {
        "mc-7315df9206599ae11b928dd1": "be092a0592abaf4cad73a6b4e9c523fb6c010836128053eced7d60f484f01ad8",
        "mc-76597101ebd26c3464b19ade": "82f26a1c82dc9040dd9a46bb3d73276fbaa980e85e7868a06751ef7918ca3cef",
        "mc-a0f44f7d2979c0475db2464d": "87c311f0365befcc4cdcef77a10188ebe9e26823c38a59755387bea941eaf187",
        "mc-a0f7983e098e635a1ee52dd6": "ab0e724b395f04f2d8a6a438dddbb1bd5258ad375d08db86acbeff8528fe2948",
        "mc-d653cd227e78ceea04297406": "8b4b86293ad0f868b8e4080f7e8a18e428db884f4848493377bfaeaca2470022"
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
      "content_sha256": "cfdea60a3599de17817daa9f1e0e6f936b3e3b8a378a58fab29bb7e5e16b0c3b",
      "content_summary": "覆盖o2/o4，组合5张同请求已核验实现卡；不承诺跨平台性能排名。A理由：回答面试中的四路径取舍问题，防止把容量、计数与有效布局混为同一种机制。",
      "dependency_content_sha256": {
        "mc-50a37c7580427893d3cfc1cd": "23876f01e99d4cc4de67169e6fab32ea7fb92430fbe619b3b420c331abbd98ee",
        "mc-b7df7e939424aa7a39a58e6b": "3d3d5afb6b346e7d02e608ab87610c2aed236b0112556c65b7c0f314e34e4268",
        "mc-dd81e7bc1ccbdb327767771c": "e4303b2dc4cc060f579b9ec9a45fbcb362e5d8ba96475b614636275073e4d31a",
        "mc-f1e42d2cf27978369eac0de5": "061616d52974efba347b142e0b94956dc899b0e9f0907344500de63bf41c3ec1",
        "mc-f7bfdcbb6d618ea751a629d9": "d1ffabd84e434341c8b19e99b80ed64a609001fab5a692a642de6f463961fb38"
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
      "content_sha256": "bc41d792ff5576b070785701901f03bae9aecc9ebf850367339c78fd2cfe0f49",
      "content_summary": "覆盖o3/o4，组合5张同请求Hybrid-EP快照子卡。A理由：支撑训练/prefill/decode迁移面试题，并防止将设计推导包装成生产性能证据。",
      "dependency_content_sha256": {
        "mc-2979889096ce057fe64b86ab": "a7a2c5a35ea4e33a9f53ecb349fa09ffaad99ecbc3c49b77b7b8b0adbf409e63",
        "mc-3dba932d0ea7abc437c403c9": "fa6cd052574c61f518be0d423ad9c3a0cf921770e86649eec21ef650bad991e7",
        "mc-9fc4d8a4a246584f1ee0ba8f": "396ca917a3718843b9c43455487169d5408a5790227a555f0b11c8e4f9031b3d",
        "mc-ee164f717c744408ef1f3e7c": "e13e7e7e4703fc0d476e6fddba59926175a2282d2ff74057ea278890d099c745",
        "mc-f80ff5e3939e02b6104c7662": "7d22b922293c5b58209c81fed2dbe058313d09d2ef4f5cde139c097271c97898"
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
      "source_ids": [
        "w2-card",
        "w2-ledger",
        "w2-lesson"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "33d24b5e469cfb8af83d21c94e8cf032ea26b003da812fdf2e241188b5f23df3",
  "manifest_payload_sha256": "6a38a0818ba421e0b15daf57a9b651e1da3f2952b06d95bd19a05d27c353520e",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 58286,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "推理框架/cards/2026-10-29-w2-u2-implementations-technical-qa.xlsx",
      "row_count": 36,
      "rows": [
        {
          "content_sha256": "87c311f0365befcc4cdcef77a10188ebe9e26823c38a59755387bea941eaf187",
          "logical_id": "mc-a0f44f7d2979c0475db2464d",
          "row_sha256": "a84248e8c8c482f597000528bbedbe67b232b5e262c5c969e533da763d4221c7"
        },
        {
          "content_sha256": "ab0e724b395f04f2d8a6a438dddbb1bd5258ad375d08db86acbeff8528fe2948",
          "logical_id": "mc-a0f7983e098e635a1ee52dd6",
          "row_sha256": "58224a57bc21937989c2bd540574e48712064e64f640fa6094bbbad8887035d4"
        },
        {
          "content_sha256": "94797291e359a5ab5e7e810dfa1172b7a0e860f18ff9cd019f1a8b276676618f",
          "logical_id": "mc-c08c9e1e782b5f1fca6126a2",
          "row_sha256": "47550eff7b71a88eb291ba0ffd66e50815edd69ca9bd5882fb0c55c7f8eb21eb"
        },
        {
          "content_sha256": "be092a0592abaf4cad73a6b4e9c523fb6c010836128053eced7d60f484f01ad8",
          "logical_id": "mc-7315df9206599ae11b928dd1",
          "row_sha256": "5ae9d58c82a90eafa2ac182cc3a79de2515d24b4d874a6b87a5d0eae7130f635"
        },
        {
          "content_sha256": "c1e8bcd4950233b182538ca0f4cddb4f1909675177ad3c1616ba5ed5b4b637b5",
          "logical_id": "mc-486a27f672d2edbf1836e411",
          "row_sha256": "6175a2410a0eff52328154a5bec83e6febc1f4e3e88e4a6410ddc13e2c87b53f"
        },
        {
          "content_sha256": "b0ae9bc4c4bdb6464ab50b920e5ae5ca7c243fa904c6bac6dc9a1737c1be3d86",
          "logical_id": "mc-eb769bec52690bea988517de",
          "row_sha256": "84d964ca70d3943d6352c93f6dde3f18701c8aaf13dbf98ad43d76f406d0f677"
        },
        {
          "content_sha256": "2e51771c228bbc896b6741bf3339c91d8fe9ed1608362dd2944bdfc059782b7b",
          "logical_id": "mc-99fe51c2ea71d50056eaf79f",
          "row_sha256": "b7f00ee0c5960847b59f4ffdac6eb8fb5d7d898b622b6fa54fe784e256ec8d2e"
        },
        {
          "content_sha256": "7e855300773b8a43bd1b5b6318ec5f70a3156b7b4d2615aa0a810dbd7267178d",
          "logical_id": "mc-a4baf65139adf754752ce42e",
          "row_sha256": "45fe396dec4b0fdbb45aedfeafc3346f9a39f6263f98270726e6cc9bc1cb17fd"
        },
        {
          "content_sha256": "82f26a1c82dc9040dd9a46bb3d73276fbaa980e85e7868a06751ef7918ca3cef",
          "logical_id": "mc-76597101ebd26c3464b19ade",
          "row_sha256": "c02918b3499f8d3c9559a1c20580eadae0344c1c0ed1cf8f6e351d952eec74b9"
        },
        {
          "content_sha256": "8b4b86293ad0f868b8e4080f7e8a18e428db884f4848493377bfaeaca2470022",
          "logical_id": "mc-d653cd227e78ceea04297406",
          "row_sha256": "e332de3c443f021b554c13083ca84a03a2408d02c19bdf2bb6ed256f189bd4e1"
        },
        {
          "content_sha256": "09290e3de04d9643f971faecb1ad930ec7633775ca82cba509e1aac7a99bd5f7",
          "logical_id": "mc-763557e86a5e94c61a29de1f",
          "row_sha256": "e53b6787b2a15bb43b90add6469d406775663a9334d7586ce2aa69c4ea8a3f89"
        },
        {
          "content_sha256": "d6942bc4d26e7b33b3ee9456c3f47a9b41b5595690cc2ea26eadbeb0433995f2",
          "logical_id": "mc-3d93d2812715fe3dfd3076f6",
          "row_sha256": "1752442554a6846e0b34fc666c275d9a214c22e3459399f7bbaa5b4e670e5dd1"
        },
        {
          "content_sha256": "108ecbbec31163b0e88e0e1185340a3d06633617f3ecd9fead2c8e116a927cac",
          "logical_id": "mc-4083d15dec700de28aa4896f",
          "row_sha256": "ecaa71532a8952281a1e5f0667ddbbdb239282be8a42656b10bdc29c05459d38"
        },
        {
          "content_sha256": "111db85fa4d8251b8b6c655ab01dbcad017199db26dbe94ef8c325892b2eff39",
          "logical_id": "mc-411cf42c374113d7e64eab2f",
          "row_sha256": "c579cd4d3fcd0bee48fb4fd13bf10c25aaf80f02eaad5205b12c5a48242c6b35"
        },
        {
          "content_sha256": "d28a3ef291772924bedaa4888a9541963d290a50b72fca8d9c0ff8b5d8245846",
          "logical_id": "mc-38c959e8575cba3ebb9ffe21",
          "row_sha256": "420224d92599d457910e8f5a34ef4c7ae9a514a0289be94baa9bcd243eac3e6b"
        },
        {
          "content_sha256": "ea049b24a42af9338c022d843da9f1d004b15c28135fc30af2b1fc538a3da5c1",
          "logical_id": "mc-87d6421dfb26070f1ff6946e",
          "row_sha256": "326e1639f8aa1407356e572de88c0879b5b174e97e7ba41e988ae5104cd01fc3"
        },
        {
          "content_sha256": "d1ffabd84e434341c8b19e99b80ed64a609001fab5a692a642de6f463961fb38",
          "logical_id": "mc-f7bfdcbb6d618ea751a629d9",
          "row_sha256": "1535ee855296316f1ef18e99a345d275f7e3eef2e5f55d940c06b4dd7649474f"
        },
        {
          "content_sha256": "1e16582507581de087ec1283e2509560979d27f43e97bca8d5c0f4f1a4a8b923",
          "logical_id": "mc-03e1c8c25f1c0cd418456715",
          "row_sha256": "c1c6d5ee4952c2341f343dc0f7135dcf8aa8e7779e3de17bb18567dc3dd12023"
        },
        {
          "content_sha256": "061616d52974efba347b142e0b94956dc899b0e9f0907344500de63bf41c3ec1",
          "logical_id": "mc-f1e42d2cf27978369eac0de5",
          "row_sha256": "88be032922a714112e29f4cd0b67743eb7c734a4e12307ce40dee6edba9de078"
        },
        {
          "content_sha256": "88e7b984787488bbb56ca2ed0208f1a0595a5128899a2ba80510545ef33cf0b7",
          "logical_id": "mc-d1cc666d10bc507528e4e265",
          "row_sha256": "0fdded56c52fe57688aa04421afbdd9e91a546cf453fc39bde1ff2304ecf9425"
        },
        {
          "content_sha256": "97a14542a4a971eba76ec65a7e3601cd9ced60a40ca6b81b334e87ea23a17cd9",
          "logical_id": "mc-07791d48c6f05d757be79c51",
          "row_sha256": "9cbc2726b0bd1942756eea856020b25bd50fa277a649b6e7f7a7416b1d339953"
        },
        {
          "content_sha256": "e4303b2dc4cc060f579b9ec9a45fbcb362e5d8ba96475b614636275073e4d31a",
          "logical_id": "mc-dd81e7bc1ccbdb327767771c",
          "row_sha256": "adc189048c72ce6ef515a4fea53152c9d817a8ede71f639504555145af3c1c38"
        },
        {
          "content_sha256": "5da9dda329e2e056d10c9cc3f0935c653d6865817c7bf8c265718b85817bcad4",
          "logical_id": "mc-20e69924a14dc55b64e6d647",
          "row_sha256": "3afdbad363ed90cd6d49a9f31c4c4aad9444e5f8378efd8c4d5433f80114d544"
        },
        {
          "content_sha256": "0b6c007724aa4a8601f5a7dff493147ed4bc416de22da782645151bc71e73ea0",
          "logical_id": "mc-87a2eea55e446b75cac448b4",
          "row_sha256": "a52e0c5549f3772e2d4beb7ff4a30ad7f758d42dca1336564527620bcb15bb55"
        },
        {
          "content_sha256": "23876f01e99d4cc4de67169e6fab32ea7fb92430fbe619b3b420c331abbd98ee",
          "logical_id": "mc-50a37c7580427893d3cfc1cd",
          "row_sha256": "9ab10793f0ec893ae5c1b1f99b49e5bfc693d8feddd2c3683fb56d4557f90504"
        },
        {
          "content_sha256": "3d3d5afb6b346e7d02e608ab87610c2aed236b0112556c65b7c0f314e34e4268",
          "logical_id": "mc-b7df7e939424aa7a39a58e6b",
          "row_sha256": "a94745c1ab3e59cef04f8d4180211364961a74814bbee6f7eca85d7f6ce04e1f"
        },
        {
          "content_sha256": "13a31e4624f182bb957a8f011d02eb6f024744f92f5c997a513a0c194fdf03bf",
          "logical_id": "mc-35c9c361d6e1758a42f5fe10",
          "row_sha256": "4b20246f16cd3244e4616c66e9b4c8b0fee6b85316c1bbc5a6b8ece82f20a5fe"
        },
        {
          "content_sha256": "704f10c10aa6e21f85d809a9946ad4b4c0439e1c12b236516b48fdb42bc44811",
          "logical_id": "mc-9f06787bb50e7439621c134b",
          "row_sha256": "33e2b69841fb25fcdb8c2aa85323006be23629fae99a7e201905722762d5fb49"
        },
        {
          "content_sha256": "e13e7e7e4703fc0d476e6fddba59926175a2282d2ff74057ea278890d099c745",
          "logical_id": "mc-ee164f717c744408ef1f3e7c",
          "row_sha256": "acedf1cff287461254f99926078309c0cebec6497e61f966518496159316ea08"
        },
        {
          "content_sha256": "ba39b82f6f1125934a997e14936a643229d7dfd6d30bd3438b2bc7a8666ad43e",
          "logical_id": "mc-50ea6c480c0d43fe0a0508a4",
          "row_sha256": "1d3354e115a2dbbf1cb1549407bf9de2cd649d7209dba061fd0e4525e2a4a902"
        },
        {
          "content_sha256": "7d22b922293c5b58209c81fed2dbe058313d09d2ef4f5cde139c097271c97898",
          "logical_id": "mc-f80ff5e3939e02b6104c7662",
          "row_sha256": "0ef62a60fc3c038e71976a7f3b8a59396d431cf776c709d5a37b3596d08a6d6e"
        },
        {
          "content_sha256": "396ca917a3718843b9c43455487169d5408a5790227a555f0b11c8e4f9031b3d",
          "logical_id": "mc-9fc4d8a4a246584f1ee0ba8f",
          "row_sha256": "78a84985a61ee7d27aa7b5ba2f876710b03c2ebf5fc8a1c5429d8aa7c7e0fa2c"
        },
        {
          "content_sha256": "a7a2c5a35ea4e33a9f53ecb349fa09ffaad99ecbc3c49b77b7b8b0adbf409e63",
          "logical_id": "mc-2979889096ce057fe64b86ab",
          "row_sha256": "af99f547cc0fc2cae1acd95ff3c5f4809659d83a4f4e59354c879d65493d465e"
        },
        {
          "content_sha256": "5bafc7ef286d7f447883c2a1fa525d57619d44b674bf07e0d885b48d0e235667",
          "logical_id": "mc-9ddb96841d288103a24cf440",
          "row_sha256": "07760ed40719979c7798c5eb0a299f6c29512548d7933d8d529591c2f96397fd"
        },
        {
          "content_sha256": "fa6cd052574c61f518be0d423ad9c3a0cf921770e86649eec21ef650bad991e7",
          "logical_id": "mc-3dba932d0ea7abc437c403c9",
          "row_sha256": "f014b7963a0db7206eaf112a1b429a0125ba1019988a51e6508f54622dc6ce01"
        },
        {
          "content_sha256": "7e1f013a460e124a4bddcb4d39cd20abc2cb9fbba9ce34a3d95803f8a97e1ffe",
          "logical_id": "mc-a66576e8728d34795904a60a",
          "row_sha256": "83ea8bb8a1ff1ef49333db93aa53bb68c205e860b3f88c11e31b4003c53ed90a"
        }
      ],
      "sha256": "55e269135f2f9d9c950faad34d9ab7e561934db25145f161570170f54b47aa48",
      "sheet_name": "cards",
      "table_sha256": "013cbfaeaeb7665d51ef2c7cc0bcd192e81fd0be1de43aa1a1b2021dc6467fbb",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 7267,
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
          "content_sha256": "dcba8e37dea3d6b8df842f3159191b40bbc7344ccaa83a90e8bccbf971b9c349",
          "logical_id": "mc-2d6e4a350130076b75a27605",
          "row_sha256": "9d30c398ce7479fd4499ae154ce7404c1404f80ff9c26600690d1b35d2eb05ec"
        },
        {
          "content_sha256": "cfdea60a3599de17817daa9f1e0e6f936b3e3b8a378a58fab29bb7e5e16b0c3b",
          "logical_id": "mc-2f3f4b0d53d2559dfc94b6e1",
          "row_sha256": "9fa449a49911d470340311d4fd2ac8730d2a39dd3313866ccc451e06959d5de9"
        },
        {
          "content_sha256": "bc41d792ff5576b070785701901f03bae9aecc9ebf850367339c78fd2cfe0f49",
          "logical_id": "mc-5f8607e9b42c31251fcaf076",
          "row_sha256": "2623be7add37350e128029dc5687f40beff71c4ba8db3970442e02244f7f9a8a"
        }
      ],
      "sha256": "9e356c6c758cf764c6a3125adaa9afa60b9fe8cec130ab924a1c8881dc5655ce",
      "sheet_name": "cards",
      "table_sha256": "09fb6d4fd4f78daed438ea32c58c397ecfd92fbd9b9127cb906405142eda27c7",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "c600d848c312838fc80e8eeb16c64219cc70df37f4d4cc5fb071620f9b1c74a0",
  "sources": [
    {
      "collection": "inference-w2-u2-evidence",
      "id": "w2-card",
      "path": "面试准备/自我准备/ChangeCard-02-MoE-EP-dispatch-combine.md",
      "sha256": "9b9a02a5d8b00a348e0403a251004430c028f04e8a0e566b33b8d24ba9b840c3",
      "summary": "已审核的接入契约与源码纠正；只采用公开固定源码事实，不将用户芯片说明或待验证结果转为确定实现。"
    },
    {
      "collection": "inference-w2-u2-evidence",
      "id": "w2-ledger",
      "path": "计划/八周冲刺进度/历史记录/W2-学习验收记录.md",
      "sha256": "b16f02d4dcbe65acc25723d0a4b580eb0513e99d151808f2db8d00bd7f1aafa4",
      "summary": "单元二固定源码基线、节点检查及已确认的Hybrid-EP场景表；用于确定学习范围和来源锚点，不将mastery状态当知识事实。"
    },
    {
      "collection": "inference-w2-u2-evidence",
      "id": "w2-lesson",
      "path": "课程网页/八周计划/plana-jd-w2-moe-ep-source.html",
      "sha256": "68341403389ef6be12a10c15ebe60d867dd042ebca2a00d8b210893b835a27bf",
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

导入文件：[2026-10-29-w2-u2-implementations-technical-qa.xlsx](2026-10-29-w2-u2-implementations-technical-qa.xlsx)（36 张卡）

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
