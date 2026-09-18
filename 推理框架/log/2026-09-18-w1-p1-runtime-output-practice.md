# 学习记录 · 2026-09-18 · W1-P1 运行路径与输出契约实践

> 来源：Codex 会话 `01a0a827-1cb1-7610-8e92-da6bc5a2cb78`，2026-09-16～2026-09-17。
> 消息边界：`msg-a0a9a79f6a0391ba2d7b` → `msg-468c7e7fc527278ef822`，共 50 条用户／助手可见消息，含过程更新。
> 起点：用户“很好，接下来我们开始实践P1吧。同样，请基于guide-learning skill学习流程开始。”；终点：P1 复核通过的助手回复。不包含此前的环境准备对话。
> 关联：[实践分析](../实践/W1-P1/分析.md) · [学习者实现](../实践/W1-P1/scenario.py) · [运行证据](../实践/W1-P1/results.json) · [验收记录](../../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-p1-accepted-20260916)。
> 可追溯对话：[同名原文](../log-raw/2026-09-18-w1-p1-runtime-output-practice.md)。本文件保存过程差异，不拥有课程进度或最终掌握状态。

## 来源与实现边界

- 教学源码固定为 `vLLM v0.26.0 @ 568afb3a13806beb53bb2e6bd518269357b237c0`。本文涉及类名、内部字段和选择行为的结论只裁决该版本。
- 本次复用 GPU 环境与 Qwen tokenizer；输出实验使用真实 OutputProcessor 和模拟 EngineCore 输出。它不执行模型推理，也不证明 Core 已处理取消或 GPU KV 已回收。
- 下文的稳定消息 ID 可在同名原文中定位；源 JSONL 首份快照 SHA-256 为 `f35b0ca9bb5298565cea05ce982dd30df125b5bc47e75993ae26f154d353784a`。

## 学习过程

### P1-01 [转折] 从概念复述进入可核验的小型实验

用户接受两项相连的交付：配置到执行组件的源码核对，以及 FINAL_ONLY 与跨输出 stop string 的最小用例。导师负责辅助构造、验收与环境，学习者负责 `scenario.py` 和分析。已有概念验收继续有效，未重新展开完整 vLLM 课程。

来源：`msg-a7d91f0937f5bd5afcb5`、`msg-4962b55ab1a103e6c98b`。

### P1-02 [要点] Executor 的 backend 能否决定 Attention backend？

学习者先正确识别 `uni` 的 Executor 分支及 CUDA 平台 `worker_cls="auto"` 的 Worker 分支，并指出 Attention 仍有独立筛选条件。导师只补全 Executor 的完整类名，随后把“候选优先顺序”与“最终有效候选”区分开。具体四行映射见实践分析，不在此复制。

来源：`msg-d80ea50b3fabaa56c2f5` → `msg-eb9ac39936d8b0fae283`。

### P1-03 [要点] 配置选择 V2 Runner，能证明 Runner 已运行吗？

学习者依据 `self.use_v2_model_runner` 正确填出 V2 的完整类名，并明确“配置选择采用 V2，但实际执行尚未执行”。本轮证据是配置值实测与选类分支源码推导；Worker／Runner 未实例化。历史 MRV1 题设不被本机默认配置覆盖。

来源：`msg-9e7ef70cb24db91cbd68`、`msg-cd0b717b0a392dc15531`。

### P1-04 [要点] 自动选择与显式指定 backend 的失败处理相同吗？

学习者在非 MLA、SM12 条件下正确找到前三候选 `FLASH_ATTN → FLASHINFER → TRITON_ATTN`，并解释 `num_heads` 没有参与这条分支的排序。随后正确区分：自动模式排除无效候选后选最高优先级；显式指定的 backend 校验失败则抛 `ValueError`，不会静默换另一个。

导师实际运行选择器，得到 `FLASH_ATTN`；这是选择函数的执行证据，不能升级为 Attention kernel 已执行。候选及排除原因见运行证据的 `attention_probe`。

来源：`msg-11c671db7981abe6dffe`、`msg-0748a933c917f5759eac`、`msg-94f3e895d83c5d07f29c`。

### P1-05 [纠错] 本次返回列表的数量与调用次数混在一起

- 场景：单请求 FINAL_ONLY；先输入 `The river is`，再输入 ` quiet today.`，最后输入迟到的 ` later`；每次 Core 均未判停。
- 原始回答：表格把三次 `request_outputs` 数量填为 `1 → 2 → 2`，但文字又说第一次“暂不对外进行输出”、第三次“没有输出”。这两部分原样保留于配对对话及运行前预测记录。
- 正确差值：本题未使用队列，每次 `process_outputs()` 返回一个外层结果对象，其中 `request_outputs` 是本次可交付结果的列表。列表长度应为 `0 → 1 → 0`；空列表为 `[]`，不能写成 `None`。
- 原因：该列表每次调用重新建立；FINAL_ONLY 未结束时不生成 RequestOutput。处理了输入，并不意味着列表中一定新增结果。
- 复核：学习者后来正确给出新文本变式第二次 1 个、第三次 0 个，并明确迟到输出被忽略。

来源：`msg-ae2bad3af5a652d15e1e` → `msg-920491ede9198fb59be6` → `msg-4e1b4aab68d926756e0e`。

### P1-06 [纠错] 排除 stop string 时，截断点在其起点

- 场景：`stop="is quiet"`，`include_stop_str_in_output=False`。
- 原始回答：第二次输出的文本填写为 `The river is quiet`。
- 正确差值：原题最终文本应为 `"The river "`，末尾保留一个空格；stop 本身及其后面的文本均不保留。
- 原因：固定版 `check_stop_strings()` 在不保留 stop 时返回其起点作为截断位置；保留 stop 时才截到末尾。
- 复核：纸面变式将 stop 改成 `END` 并保留它，学习者正确回答最终文本为 `Go END`，不带其后的 ` now.`。

来源：`msg-ae2bad3af5a652d15e1e`、`msg-920491ede9198fb59be6`、`msg-4e1b4aab68d926756e0e`。

### P1-07 [纠错] 前端状态清理不等待 Core 完成取消

- 场景：前端文本命中 stop，而输入的 EngineCoreOutput 仍未判停。
- 原话：“内部RequestState应该需要等到abort完成才删除吧。”第三次又预测继续取消且状态仍存在。
- 正确差值：第二次先构造最终结果，再删除前端 RequestState，随后把内部 ID 放入本次 `reqs_to_abort`。第三次查不到状态，直接跳过，不再交付，也不重复生成取消项。
- 原因：前端状态生命周期、返回取消请求及 Core 执行取消属于不同动作。这里的取消列表不是完成确认，前端删除状态也不是 GPU KV 回收证据。
- 复核原话：“因为前端RequestState已经删除，前端查不到该请求就直接跳过。”纸面变式特意保留 Core 尚未处理取消的条件。

来源：`msg-ae2bad3af5a652d15e1e` → `msg-920491ede9198fb59be6` → `msg-4e1b4aab68d926756e0e`。

### P1-08 [高价值问题] run_case 到底负责什么？

用户主动问：“可以详细讲讲run case需要实现什么逻辑吗？我还不是很清楚。”导师把分工拆清：用例对象提供资源与输入；学习者函数构造参数、创建并注册请求、依次提交三批输出；真实处理器执行被测行为；观察器记录，验收工具断言。

这里最重要的接口区别是：`make_request()` 只构造数据对象，`add_request()` 才建立处理器的请求状态。函数返回 None 不妨碍测试读取观察器保存的实际调用。该段属于实现步骤指导，不能改写成完全无提示的独立实现。

来源：`msg-d10ca20c59d8dce4dd73` → `msg-bb8c40c7f3907115b74b`。

### P1-09 [转折] 区分学习者逻辑与验收工具故障

学习者提交了完整的三次调用。首次验收被 `.harness` 相对导入阻断，根因是导师的动态加载器未设置包上下文。导师修复加载器，未改学习者文件；原始实现随后通过三项检查。此故障未归责为学习者的输出契约错误。

来源：`msg-4a9027042fd2de9cae85`、`msg-ae9c2b6afc3b127ec312`、`msg-11d5a7a2bc8f4299f235`；细节见运行证据的 `loader_issue`。

### P1-10 [纠错] 修改参数化输入，不必改写测试驱动函数

- 场景：原题只将 `include_stop_str_in_output` 改为 True。
- 原话：“`run_case` 需要修改，在构造SamplingParams中强制指定`include_stop_str_in_output` 参数变成True。”
- 正确差值：现有实现已把 `case.include_stop_str_in_output` 传给 SamplingParams；测试入口创建 True 的 case，同一份函数即可验证新条件。硬编码 True 反而会破坏 False 用例。
- 原因：输入条件与执行流程已经分离；应沿实际参数传递链定位改动层次。
- 复核：同一文件哈希下，False／True 两组均 `3 passed`。用户随后回应“明白，只要修改case就行”，最终分析稿补出了测试入口 → case → SamplingParams 的链路。行为预测原本正确，参数来源解释得到过提示，二者分别保留。

来源：`msg-f30bb3d888126c2a19ce` → `msg-acf54ae79fce226a50d5` → `msg-1ade0adf7696c7c60ea2`；复审反馈见 `msg-17e2461d1a893ee5d9cc`。

### P1-11 [高价值问题] isinstance(backend, type) 在判断什么？

用户追问 Executor 的类对象分支。导师说明：它判断参数值是否是一个类；后续 `issubclass(..., Executor)` 才检查继承关系。例如执行器类本身与字符串 `"uni"` 走不同分支；`str` 也是类，却不满足 Executor 继承约束。选定类的赋值不等于实例化。

本段是新问题的讲解，没有对应的学习者错误，不标为纠错。该区别适合迁移到接收类对象的工厂／插件接口。

来源：`msg-1ade0adf7696c7c60ea2` → `msg-1a7f0003579703e0b92b`。

### P1-12 [转折] 把“未执行模型”与“未执行选择器”分开

分析稿的几轮 Review 不是新增技术实验，而是校准结论与已有证据的对应：GPU 型号不能替代 `worker_cls`／`use_v2_model_runner` 等真实分支条件；本机已经执行配置构造和 Attention 选择器，不能把四行全写成“源码验证”；这些运行又不证明 Worker／Runner 已实例化或 kernel 已执行。

学习者最终补齐版本锚点、类名、条件和证据层次。这个过程保留了导师给出表格校准建议的事实，不把编辑结果当成一次新的独立设备实验。最终分析与原始证据见头部关联文件。

来源：`msg-ac4d37ac9fcf8d11c5a1` → `msg-84cf28e2b719d6bfcdb6`，`msg-1ca6a2d2c208374f7390` → `msg-78d3660bf3c0f13372ef`，`msg-20eccb12384510e72deb` → `msg-468c7e7fc527278ef822`。

## 遗留与交接

- [遗留] P1 分析表中 Worker 的一个来源文件路径笔误属于非阻塞备注；具体定位及后续处理只由[验收记录](../../计划/八周冲刺进度/历史记录/W1-学习验收记录.md#w1-p1-accepted-20260916)维护，不转成知识卡。
- [遗留] 整周最终确认与后续课程位置只见[学习断点](../../计划/学习断点.md)。本日志不写入 mastery，也不把前端小用例升级为完整 vLLM 服务实测。
