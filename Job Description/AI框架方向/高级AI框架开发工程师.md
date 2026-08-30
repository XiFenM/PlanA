## THE ROLE

You will play a critical role in advancing high-performance LLM serving by optimizin Role: Software Engineer / Systems Engineer, GPU Networking & Inference Infrastructure Team: ROCm System Software — Communication Primitives

About the Project
MORI (Modular RDMA Interface) is an open-source framework powering AMD GPU communication in large-scale LLM inference. It provides the RDMA + GPU-direct networking layer for MoE expert parallelism and prefill/decode disaggregation in SGLang and vLLM, and owns the KVCache management and storage layer via MORI-UMBP (Unified Memory & Bandwidth Pool). MORI achieved state-of-the-art results in the SemiAnalysis InferenceX v2 evaluation.

## What You'll Work On

Inference framework integration: Own end-to-end integration of MORI primitives into SGLang and vLLM — Python operator APIs, MORI-EP dispatch/combine in MoE forward passes, and MORI-IO in KVCache transfer pipelines.
MORI-UMBP: Integrate tiered KVCache storage and distributed key-value access into inference serving stacks.
PD disaggregation: Integrate MORI-IO into the prefill/decode path, enabling high-throughput KVCache transfers over GPU-direct RDMA.
Expert Parallelism (EP): Land and maintain MORI-EP in SGLang and vLLM, covering scheduling, routing, and EPLB for MoE models like DeepSeek V3 across 8–64 GPUs.
MORI-SHMEM: Integrate and maintain the symmetric memory runtime that underpins all MORI components — managing symmetric GPU memory allocation, RDMA transport initialization (IB, AINIC, Thor2), P2P/XGMI address translation, and device-side state for GPU kernels via MORI-IR bitcode.
Performance benchmarking: Design and run end-to-end benchmarks (throughput, TTFT, ITL) across EP and PD disagg configurations; drive optimization from profiling data.

## Qualifications

Required: - Deep familiarity with at least one major LLM inference framework (SGLang, vLLM, TensorRT-LLM, or equivalent) — scheduler, attention backend, KVCache manager, and distributed execution engine. - Strong understanding of LLM serving: MoE expert parallelism, prefill/decode disaggregation, KVCache reuse, tensor/pipeline/sequence parallelism. - Solid C++ and Python; comfortable in a mixed C++/HIP/Python codebase with PyTorch custom operator extensions. - Experience contributing to large open-source projects: upstream PRs, code review, cross-team coordination.
Nice to Have: - RDMA concepts: verbs API, queue pairs, completion queues, memory registration, GPUDirect Async (IBGD A). - Collective communication libraries (NCCL, RCCL, MPI) and their integration into distributed stacks. - GPU cluster network topologies: XGMI/NVLink (intra-node), InfiniBand/RoCE (inter-node), and their impact on MoE all-to-all patterns. - NIC v endor ecosystems (Mellanox ConnectX, AMD Pollara/AINIC, Broadcom Thor2) and userspace driver libraries. - Profiling network-bound workloads with rocprofv3, Perfetto, ibstat/perfquery. - ROCm, hipcc, or AMD GPU architecture experience.

## What Makes This Role Unique

You'll own the bridge between MORI's low-level GPU networking layer and inference frameworks running trillion-parameter models at scale. MORI-EP and MORI-IO are already merged into SGLang and vLLM — your contributions ship directly to open-source and production. The team brings deep RDMA and GPU kernel expertise, so you can focus on inference-level impact while learning the networking layer from those who built it. GPU kernels, inference runtimes, and distributed execution strategies across single-node and multi-node systems.
This role is deeply focused on LLM inference stacks, including vLLM, SGLang, and internal inference platforms. You will work at the intersection of model architecture, GPU kernels, compiler technology, and distributed systems, collaborating closely with internal GPU library teams and upstream open-source communities to deliver production-grade performance improvements.
Your work will directly impact throughput, latency, scalability, and cost efficiency for state-of-the-art LLMs running on AMD GPUs.

## THE PERSON:

You are a senior systems engineer with deep LLM domain knowledge who enjoys working close to the metal while keeping a strong understanding of end-to-end inference systems. You are comfortable reasoning about attention, KV cache, batching, parallelism strategies, and how they map to GPU kernels and hardware characteristics.
You thrive in ambiguous problem spaces, can independently define technical direction, and consistently deliver measurable performance gains. You balance strong execution with thoughtful upstream collaboration and maintain a high bar for software quality.

## KEY RESPONSIBILITIES

## Optimize LLM Inference Frameworks

Drive performance improvements in LLM inference frameworks such as vLLM, SGLang, and PyTorch for AMD GPUs, contributing both internally and upstream.
LLM-Aware Kernel Development
Design and optimize GPU kernels critical to LLM inference, including attention, GEMMs, KV cache operations, MoE components, and memory-bound kernels.
Distributed LLM Inference at Scale
Design, implement, and tune multi-GPU and multi-node inference strategies, including TP / PP / EP hybrids, continuous batching, KV cache management, and disaggregated serving.
Model-System Co-Design
Collaborate with model and framework teams to align LLM architectures with hardware-aware optimizations, improving real-world inference efficiency.
Compiler & Runtime Optimization
Leverage compiler technologies (LLVM, ROCm, Triton, graph compilers) to improve kernel fusion, memory access patterns, and end-to-end inference pipelines.
End-to-End Inference Pipeline Optimization
Optimize the full inference stack—from model execution graphs and runtimes to scheduling, batching, and deployment.
Open-Source Leadership
Engage with open-source maintainers to upstream optimizations, influence roadmap direction, and ensure long-term sustain ability of contributions.
Engineering Excellence
Apply best practices in software engineering, including performance benchmarking, testing, debugging, and maintainability at scale.
PREFERRED EXPERIENCE
Good LLM Knowledge
Deep understanding of Large Language Model inference, including attention mechanisms, KV cache behavior, batching strategies, and latency/throughput trade-offs.
LLM Inference Frameworks
Hands-on experience with vLLM, SGLang, or similar inference systems (e.g., FasterTransformer), with demonstrated performance tuning.
GPU Kernel Development
Proven experience optimizing GPU kernels for deep learning workloads, particularly inference-critical paths.
Distributed Inference Systems
Experience designing and tuning large-scale inference systems across multiple GPUs and nodes.
Open-Source Contributions
Track record of meaningful upstream contributions to ML, LLM, or systems-level open-source projects.
Programming & Debugging Skills
Strong proficiency in Python and C++, with deep experience in performance analysis, profiling, and debugging complex systems.
High-Performance Computing
Experience running and optimizing large-scale workloads on heterogeneous GPU clusters.
Compiler & Systems Background
Solid foundation in compiler concepts and tooling (LLVM, ROCm, Triton), applied to ML kernel and runtime optimization. ACADEMIC CREDENTIALS:
Master's or PhD in Computer Science, Computer Engineering, Electrical Engineering, or a related field.
