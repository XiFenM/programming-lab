# 第 08 课：Grouped GEMM 的一次发射、设备侧调度与 TMA 描述符

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-08-grouped-gemm` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 解释 grouped GEMM 怎样把一组尺寸不同的矩阵乘法合并成一次 kernel 发射（地址表间接、设备上的静态 tile 调度、TMA 描述符），能判断它的收益、负载与失效边界，并实现、验证一个支持任意尺寸的 grouped GEMM kernel |
| 阶段 | `complete`（2026-10-09 学习者确认关闭） |
| 启动授权 | 2026-10-05，学习者提出“好的，让我们开始下一课吧。我们继续学习triton。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/08-grouped-gemm.py` | `teaching-spine` | 仓库 commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；本地 SHA-256 `0b474fc69d34dfde591454ca735d10abdc72bcc03d6b42530390aceaa2844c3b`。与 v3.7.1 tag 的同名文件只差 3 行：TMA kernel 的 autotune `key`（tag 中是含拼写错误的四项列表，本地为 `['group_size']`）和两处 benchmark 返回值顺序；两个 kernel 与包装函数逐字相同 | 教学顺序与示例：指针版 kernel、TMA 版 kernel、主机侧打包、benchmark 形状 |
| [Triton v3.7.1](https://github.com/triton-lang/triton/tree/v3.7.1) | `implementation-authority` | tag `v3.7.1`，commit `f797708c0626e5f9840ca5b0a98790e2c7cb09ad`，与 `uv.lock` 一致；核对于 2026-10-05 | `python/triton/language/{core.py,semantic.py}` 的整数与指针互转、`multiple_of`、`make_tensor_descriptor`；`python/triton/compiler/code_generator.py` 的 `for`／`while` 生成；`python/triton/backends/compiler.py` 的参数对齐特化；`python/triton/runtime/{autotuner.py,_allocation.py}`；`third_party/nvidia/backend/{compiler.py,driver.py}` 的描述符回退、TMA 降级与全局暂存内存的申请；`lib/Analysis/AxisInfo.cpp` 与 `lib/Dialect/TritonGPU/Transforms/Pipeliner/PipeliningUtility.cpp` 的对齐推导和流水条件；`lib/Dialect/TritonNvidiaGPU/Transforms/{TMALowering.cpp,TMAUtilities.cpp}`、`third_party/nvidia/lib/TritonNVIDIAGPUToLLVM/TMAToLLVM.cpp` 与 `lib/Dialect/Triton/Transforms/RewriteTensorDescriptorToPointer.cpp` 的描述符创建和回退；`python/triton/runtime/interpreter.py` 的描述符读写语义 |
| [CUTLASS v3.9.2](https://github.com/NVIDIA/cutlass/tree/v3.9.2) | `implementation-authority`（真实系统锚点） | tag `v3.9.2`；取回于 2026-10-05 | `include/cutlass/gemm/kernel/{gemm_grouped.h,grouped_problem_visitor.h}` 与 `device/base_grouped.h`：两种调度模式、按网格大小推进 tile、线程块数的确定、warp 内前缀和扫描、主机预计算与按 K 降序排序；`examples/24_gemm_grouped/gemm_grouped.cu` 的接口说明与对比开关 |
| [PyTorch v2.13.0](https://github.com/pytorch/pytorch/tree/v2.13.0) `torch.nn.functional.grouped_mm` | `implementation-authority`（真实系统锚点） | tag `v2.13.0`，与 `uv.lock` 一致；源码取回并在本机临时环境（`torch==2.13.0+cu130`，CPU）运行于 2026-10-05 | `aten/src/ATen/native/GroupedMMUtils.h` 的输入检查、输出分配与回退循环；`cuda/GroupedBlas.cpp` 的快速路径条件；`cuda/GroupMM.cu` 与 `cuda/GroupMMCommon.cuh` 的设备侧准备 kernel 和块大小选择；`derivatives.yaml` 的求导条目。文档字符串只作接口说明，与源码不一致处以源码为准 |
| [NVIDIA PTX ISA](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html) | `interface-authority` | 文档版本 9.4，访问于 2026-10-06 | `cp.async` 的拷贝大小与地址对齐要求；张量搬运（`cp.async.bulk.tensor`）的块、越界填充与 tensor-map 的存放位置；`tensormap.replace` 的字段 |
| [DeepSeek-V3 技术报告](https://arxiv.org/abs/2412.19437v1) | `method-authority`（真实规模锚点） | arXiv:2412.19437 v1，§4.2；访问于 2026-10-06 | MoE 层的真实配置：隐藏维 7168、每层 256 个路由专家、专家中间维 2048、每个 token 激活 8 个路由专家；只用于给出真实的 G、K、N |
| [NVIDIA 博客：cuBLAS grouped GEMM](https://developer.nvidia.com/blog/introducing-grouped-gemm-apis-in-cublas-and-more-performance-updates) | `explanatory-support` | 发布于 2024-06-12，访问于 2026-10-05 | cuBLAS 12.5 的 `gemmGroupedBatched` 接口与其动机；其中的加速比是厂商报告，不代表本仓库实测 |

### 目标与所需证据

| ID | 可观察目标 | 理解 | 实践 | 实证 |
| --- | --- | --- | --- | --- |
| O1 | 讲清 grouped GEMM 的完整数据流：主机侧把地址、尺寸和 leading dimension 打包成设备张量；固定数量的 CTA 以步长 `NUM_SM` 跨问题领取 tile；tile 内做常规 GEMM。说明它相对逐个发射和 batched GEMM 换来了什么、付出了什么 | 需要 | 不需要 | 不需要 |
| O2 | 分析静态调度的负载均衡与 `NUM_SM` 的取舍，并与每 tile 一个 CTA、主机预计算、动态领取相比较；指出教程实现的失效边界：假定满 tile、写死 fp16、对齐提示是一项承诺 | 需要 | 不需要 | 不需要 |
| O3 | 解释 tensor descriptor 与 TMA：描述符描述什么、硬件替代了什么、为什么需要全局内存分配器、越界如何处理、没有 TMA 的设备上怎样回退；并迁移到真实系统（PyTorch `grouped_mm`、cuBLAS、CUTLASS、MoE 专家计算）和非 NV 后端 | 需要 | 不需要 | 不需要 |
| O4 | 实现并验证一个支持任意尺寸（非整 tile）的 grouped GEMM kernel 与包装函数：本机以调度模型和只编译检查，GPU 机器上与 `torch.matmul` 数值对照 | 需要 | 需要 | 不需要 |

与逐个发射或 cuBLAS 的性能对比、`NUM_SM` 调参和 TMA 的实机运行不属于完成门槛；学习者的 GPU 是 sm_89，没有 TMA
硬件。需要时作为观察或结课后的 optional extension 另行约定。

### 当前证据

- **已有证据**：[阶段事件](#条件片段阶段事件) E-01 提供 O1、O2 的节点级理解证据（节点 1–3）。已确认的前置只决定讲解起点：Lesson 02 的 persistent kernel（固定数量的 program
  循环领取任务）、Lesson 03 的分块矩阵乘（mask、stride、fp32 累加）、Lesson 05 的原子操作、Lesson 06 的 FP8
  与 `tl.dot`。
- **仍缺证据**：无。O4 的实践证据见 E-04（[练习约定 P1](#条件片段练习约定) 的 A1–A7 全部通过）；O1–O3 的理解证据见 E-01 至 E-03；O4 的理解证据由综合验收的预测题与迁移题覆盖。结课结论见[结课](#条件片段结课)。
- **来源与环境核对（2026-10-05）**：本机无 NVIDIA GPU，在仓库外的临时环境（`triton==3.7.1`）中只编译不运行。
  - 指针版 kernel：TTIR 含 2 个 `scf.for`、1 个 `scf.while`、3 个 `tt.int_to_ptr`。保留 `tl.multiple_of` 时 K 循环
    被做成异步预取流水（sm_90 与 sm_89 的 PTX 均出现 `cp.async.cg.shared.global`）；去掉后两个目标上都不再出现
    异步拷贝。sm_90 使用 `wgmma.mma_async`，sm_89 使用 `mma.sync`。
  - 描述符版 kernel：sm_90 上生成 `tensormap.replace.*`、`cp.async.bulk.tensor.2d` 与 `wgmma`，元数据
    `global_scratch_size=768`、对齐 128；sm_89 上 `make_tensor_descriptor` 被改写为普通 `tt.load`／`tt.store`，
    没有异步拷贝，仍可编译，FP8 时使用 `mma.sync…e4m3`。
  - 调度模型（纯 Python，按 kernel 控制流逐行对应）：教程示例组在 `BLOCK_SIZE_M=N=128`、`BLOCK_SIZE_K=32`、
    `NUM_SM=84` 时共 85 个 tile，各 CTA 的 K 循环次数最少 8、最多 36、平均 27.9；`NUM_SM=128` 时 43 个 CTA
    领不到 tile。
  以上均为本地编译与模型观察，不代表 GPU 上的数值或性能结果。
- **块大小的编译与模型观察（2026-10-05）**：指针版 kernel 在 sm_89、4 个 warp 下，`128×128×32` 的块每线程
  255 个寄存器、共享内存 32768 字节、PTX 中 64 条 `mma.sync` 与 24 条 `cp.async`；`64×64×32` 的块为 128 个
  寄存器、16384 字节、16 条与 12 条。调度模型中，教程示例组在 `NUM_SM=84` 下最忙 CTA 的乘加量由 36 个单位
  （128 块）降到 33 个单位（64 块），平均都是 27.86；累计读入量由 38.3 MB 升到 76.7 MB。100 个随机尺寸的
  问题按 K 降序排列后，最忙与平均之比由 1.09–1.27 降到 1.03–1.05（3 次随机试验，块大小不变）。未在 GPU 上计时。
- **对齐提示与描述符的编译观察（2026-10-06）**：sm_89 上，指针版保留 `tl.multiple_of` 时 TTGIR 为
  `async_copy_global_to_local {contiguity = 8}`，PTX 有 24 条 16 字节的 `cp.async.cg.shared.global`；去掉后为普通
  `tt.load`，PTX 有 64 条 `ld.global.b16` 与 64 条 `st.shared.b16`，没有异步拷贝。只做写回的小 kernel：`c_ptrs` 无提示时
  128 条 `st.global.b16`，加提示后 16 条 `st.global.v4.b32`。描述符版在 sm_90 上每个描述符 13 条 `tensormap.replace`
  加一次 128 字节的拷贝，每个描述符在全局暂存区占 256 字节；每轮 2 条 `cp.async.bulk.tensor`，预告 32768 字节。
  描述符版在 sm_89 上被改写为带 mask 的普通读写，没有异步拷贝，全局暂存为 0。
- **保证降档与输出步长补齐的核对（2026-10-06）**：指针版的 K 循环在 sm_89 上，保证 16／8／4 时分别生成 24 条 16 字节、
  48 条 8 字节、96 条 4 字节的 `cp.async`，保证 2 或不写时为 64 条 `ld.global.b16` 且没有流水。CPU 上的 `grouped_mm`：
  B 以 `[G,500,1024]` 存放并转置传入时被接受，输出形状 `[768,500]`、步长 `(504,1)`、不连续，结果与逐组循环相同；
  B 按行存放为 `[G,1024,500]`，或输入维为 1020 时，都以 “strides should be multiple of 16 bytes” 被拒绝。
- **mask 与流水、AMD 上的描述符（2026-10-06）**：单块的 K 循环在 sm_89 与 sm_90 上，只加行方向的 mask（`offs_am[:, None] < gm`）
  时仍是 24 条 16 字节的 `cp.async`；M、N、K 三个方向都加 mask 时没有 `cp.async`，退回 64 条 `ld.global.b16`。依据是
  `PipeliningUtility.cpp` 取指针对齐与 mask 沿连续方向的恒定长度两者的较小值；PTX 的 `cp.async` 每条指令只有一个
  `ignore-src` 开关。描述符版以 AMD gfx942 为目标可以编译，描述符被改写为普通 `tt.load`／`tt.store`，生成 32 条 MFMA。
  教程的 `num_sms()` 在非 CUDA 后端返回写死的 148。
- **练习可行性核对（2026-10-07）**：Triton 3.7.1 的解释器模式（`TRITON_INTERPRET=1`，需要 numpy）可以在 CPU 上执行教程的指针版
  kernel，地址表里放 CPU 张量的地址即可，结果与 `torch.matmul` 的相对误差在 5e-4 以内。一份不入库的参考实现在 sm_89 与 sm_90 上
  两种特化都能编译：只有行方向 mask 的特化保留 16 字节的 `cp.async`（块 64×64×32 时 12 条），三个方向都有 mask 的特化没有。
  该实现在解释器下通过了含保护区、`M=0`、多种 `num_sm` 与堆叠接口的试运行。
- **来源核对（2026-10-05，PyTorch `grouped_mm`）**：在 CPU 上以 fp16 运行 `X[768,1024]`、`W[3,1024,512]`、
  `offs=[256,384,768]`，结果与逐组 `mm` 相同；按教程包装函数的同一组语句算出的 A 地址表（相对基地址 0、524288、
  786432 字节）与源码中设备侧准备 kernel 的公式 `A + offs[g-1] * stride` 一致。float64 输入、行步长不是 16 字节
  倍数、int64 偏移表均被输入检查拒绝；以稠密上游梯度反向传播得到的梯度与逐组循环一致。未在 GPU 上运行。
- **不满足满 tile 时的地址模型（2026-10-05）**：按 kernel 的地址公式在 CPU 上建一维内存模型（单个问题，块
  `128×128×32`，基准 `M=128,N=512,K=1024`）。`M=100`：A 之外读 114,688 个元素，C 之外写 14,336 个元素，有效结果
  全对。`N=480`：C 内 4,064 个有效元素被两个 tile 写入不同的值，另有 32 个元素写到 C 之外。`K=1000`：A 之外读
  96 个、B 之外读 12,288 个元素，无越界写，保护区非零时全部输出错误。真机上的越界访问是未定义行为，未在 GPU 验证。
- **教学更正（2026-10-05）**：节点 1 曾按文档字符串称 `grouped_mm`“要求 CUDA、bfloat16、SM ≥ 80”。按 v2.13.0
  源码，它接受 fp32、bf16、fp16；CUTLASS 快速路径只在 sm_90／sm_100 且输入输出均为 bf16 时启用，其余情况
  （含 CPU、sm_89、默认配置的 ROCm）走逐组 `mm` 的回退循环。已在节点 2 的补充讲解中向学习者更正。
- **学习者报告的实现问题（2026-10-09）**：学习者编写 P1 时遇到并自行解决的四个问题，已在本机用 Triton 3.7.1 复现并核对原因。
  1. `continue`：在 kernel 里用 `continue` 跳过 M 为 0 的问题，报 `unsupported AST node type: Continue`。
     `python/triton/compiler/code_generator.py` 没有 `visit_Continue` 与 `visit_Break`，两者都落到 `generic_visit`，
     `break` 同样报错；用 `if` 包住循环体可以编译。本课不需要特殊处理：M 为 0 时块数为 0，`while` 不会进入。
  2. 循环里改写指针变量：把从地址表读出的标量指针原地改写成块指针（`p = p + 行偏移 + 列偏移`）并放进循环，报
     `Loop-carried variable … has initial type pointer<fp16> but is re-assigned to <[…], pointer<fp16>> in loop`
     （`_verify_loop_carried_variable`）：跨迭代传递的变量类型必须不变。类型一致时能编译，但每一轮都在上一轮的结果上再加一次
     完整偏移，地址逐轮累加。可行的写法有两种：每轮用新的名字从基地址重新计算（学习者的做法）；保留块指针、每轮只加增量
     （教程的 `a_ptrs += BLOCK_SIZE_K`）。
  3. mask 的括号：`a < M & b < K` 报 `simultaneous multiple comparison is not supported`。Python 中 `&` 的优先级高于
     比较运算符，表达式被解析成链式比较 `a < (M & b) < K`；每个比较都要加括号，NumPy 与 PyTorch 也是如此。
  4. 行步长：表里的行步长必须取 `stride(0)`，不能用列数代替。`[4, 100]` 的张量取视图 `[:, :64]` 后形状是 `(4, 64)`、
     步长是 `(100, 1)`；验收测试中带保护区的视图和“同一张量的多个视图”两类用例覆盖这一点。

### 核心工件与参考

| 角色 | 路径或引用 | 说明 |
| --- | --- | --- |
| 你写（learner-owned） | `gpu/triton/lesson08_grouped_gemm.py` | P1 的 kernel、包装函数与堆叠接口。在 GPU 上通过全部测试的是第三次提交（SHA-256 前缀 `481ff6f4`）；入库的版本（前缀 `d391376d`）是在它之上做的 Ruff 整理，见[结课](#条件片段结课) |
| 我维护（agent-owned） | `gpu/triton/lesson08_grouped_gemm_test.py` | P1 的验收测试，共 91 项：只编译层 10 项，数值与参数检查 81 项（2026-10-09 两次补充，见 E-04） |
| 来源或知识产物 | `docs/triton-tutorials/official/08-grouped-gemm.py` | 教程快照，不修改 |
| 来源或知识产物 | [节点 5 图解页](../attachments/08-grouped-gemm/grouped-gemm-data-movement.html) | 三种搬运方式、对齐实验、描述符的四步、边界与回退，以及“各种输入情形下调用前要做什么”的速查表；可交互，离线可用 |

## 条件片段：练习约定

- **编号与版本**：P1，版本 1；学习者接受于 2026-10-07（“同意接受。”）。
- **为什么做**：O4 需要实践证据。综合验收后只有理解证据，没有学习者自己实现并通过验收的 kernel。
- **你交付什么**：在 `gpu/triton/lesson08_grouped_gemm.py` 中实现三样东西。
  1. `grouped_matmul_kernel`，参数依次为 `group_a_ptrs, group_b_ptrs, group_c_ptrs, group_gemm_sizes, g_lds, group_size`，以及
     `tl.constexpr` 的 `NUM_SM, BLOCK_SIZE_M, BLOCK_SIZE_N, BLOCK_SIZE_K, RAGGED_NK`。调度方式与教程相同。`RAGGED_NK=False` 时调用方
     保证每个问题的 N、K 是块大小的整数倍，M 任意且可以为 0，并保持 16 字节的异步拷贝；`RAGGED_NK=True` 时 M、N、K 都任意，
     N、K 至少为 1。fp16 读入、fp32 累加、fp16 写回；可以对 A、B 的地址作 16 字节的保证，对 C 不作保证。
  2. `grouped_matmul(group_a, group_b, *, out=None, block_m=64, block_n=64, block_k=32, num_sm=None)`，返回张量列表。只发射一次；
     五张表建在输入所在的设备上；由它决定 `RAGGED_NK`；给了 `out` 就写入并原样返回；`num_sm` 不给时取 CUDA 设备的 SM 数，
     非 CUDA 设备上不给则报错；不修改输入。
  3. `grouped_matmul_stacked(x, w, offs, *, block_m=64, block_n=64, block_k=32, num_sm=None)`：`x` 为 `[总行数, K]`，`w` 为
     `[G, K, N]`，`offs` 为 int32 的 `[G]`（每组的结束行，不含）；返回 `[总行数, N]`，行顺序与 `x` 相同；复用同一个 kernel，
     不得把 `offs` 读回主机。
- **验收项**：

| ID | 可观察标准 | 检查方式 |
| --- | --- | --- |
| A1 | 返回值的个数、形状、dtype、设备正确；`out` 原样返回；输入不被修改；下列情形抛 `ValueError`：两个列表长度不同或为空；元素不是二维 fp16 张量或不在同一设备；A 的列数不等于 B 的行数，N 或 K 为 0；行内不连续；A 或 B 的首地址不是 16 的倍数或行步长的字节数不是 16 的倍数（空矩阵不检查，只有一行的矩阵不检查行步长）；`out` 的个数、形状、dtype、设备不符或行内不连续；`block_m`、`block_n` 不在 16／32／64／128，`block_k` 不在 16／32／64；`num_sm` 不是正整数 | 测试 |
| A2 | 尺寸都是整块时结果与 `torch.matmul` 一致 | 测试 |
| A3 | 任意尺寸时结果一致：M 为 0、1 或不整块；N、K 不整块；混合组；`num_sm` 取 1、小于和大于总块数 | 测试 |
| A4 | 不越界：C 两侧的保护区不被改写；A、B 两侧填满 NaN 时结果里没有 NaN | 测试 |
| A5 | 编译产物：`RAGGED_NK=False` 时有 16 字节的异步拷贝，读 A 和写 C 都带 mask，C 的写是逐个元素的；`RAGGED_NK=True` 能编译 | 只编译测试，sm_89 与 sm_90 |
| A6 | 说明包装函数的每项检查保护 kernel 的哪个假定；指出哪一项即使去掉，数值测试也无法稳定发现，并说明原因 | 学习者的说明，按要点核对 |
| A7 | 无提示变式：堆叠接口结果一致，且不把 `offs` 读回主机 | 测试 |

- **运行方式**：本机没有 GPU，由 Agent 运行只编译层（A5）与解释器层（`TRITON_INTERPRET=1`，在 CPU 上执行 A1–A4、A7）；学习者在
  GPU 机器上运行同一文件，完成门槛要求 GPU 层通过。
- **文件边界**：

| 边界 | 路径或受限模式 |
| --- | --- |
| 你写 | `gpu/triton/lesson08_grouped_gemm.py` |
| 我维护 | `gpu/triton/lesson08_grouped_gemm_test.py`；本 Lesson 记录；`docs/triton-learning/README.md` 的 Checkpoint 与课程索引行 |
| 我只读 | `docs/triton-tutorials/official/08-grouped-gemm.py`；`gpu/triton/lesson03_matrix_multiplication.py` |
| 本次不动 | 其他课程的文件、依赖和配置 |

- **求助如何影响证据**：随时可以求助；透露关键解法只影响相应的验收项，之后用一个小变式在无提示下恢复。A7 期间不给提示。
- **非目标与可选项**：不做 autotune、描述符版、其他 dtype、C 的 16 字节写回、动态调度和任何性能门槛。可选观察（不进入完成门槛）：
  在学习者的 GPU 上先预测再测量逐个 `torch.matmul` 循环与一次 grouped 发射的对比，以及 64 与 128 两种块的对比。
- **完成门槛**：A1–A7 全部通过（含 GPU 层），阻塞问题全部关闭。

## 条件片段：帮助影响

| 透露到什么程度 | 影响的验收项或工件 | Agent 是否写了学习者核心工件 |
| --- | --- | --- |
| 2026-10-09：A7 数值不一致，学习者求助定位。给出了三样：细化的失败证据（输出第 0–49 行正确，第 50–117 行被写入但数值不对，第 118–167 行从未被写入）；约定中地址表的定义；“与已通过的列表接口逐表对比”的定位方法。没有指出出错的语句和错误的类别，没有给代码。 | A7：定位环节有协助，未透露解法。同日学习者自行说出原因（地址表里是按字节计的整数地址，行偏移要再乘元素大小），没有用到进一步的提示，独立证据成立；修复待测试确认 | 否 |

## 条件片段：需要跟踪的问题

| ID | 对应验收项或目标 | 严重度 | 状态 | 证据 |
| --- | --- | --- | --- | --- |
| F-01 | A3、A4 | 阻塞 | 已关闭 | 2026-10-09 首次 Review：N、K 不整块的问题排在整块问题之前的混合组上，该问题的结果含 NaN，C 的保护区被改写；同样的问题排在最后时通过。原有测试的混合组都以不整块的问题结尾，没有覆盖这一情形，属验收测试的缺口：已在保护区测试中补入两个组（4 项），参考实现通过，新增的一种故意写错的变体被判为失败。本机无 GPU，结果来自解释器层对学习者文件副本（只放开 CPU 输入）的运行。第二次提交（2026-10-09）：新增的 4 项在本机解释器层通过。关闭证据（2026-10-09，RTX 4090 D，torch 2.13.0+cu130，Triton 3.7.1，实现文件 SHA-256 前缀 `481ff6f4`）：保护区测试 12 项在 GPU 层与解释器层全部通过。 |
| F-02 | A1（解释器层） | 阻塞 | 已关闭 | 2026-10-09 首次 Review：包装函数拒绝所有非 CUDA 张量（`ValueError: Device cpu is invalid …`），解释器层在 CPU 上有 47 项因此失败。约定允许非 CUDA 设备在给出 `num_sm` 时运行，只在不给时抛 `ValueError`；放开设备检查的副本在后一种情形抛出的是 `RuntimeError`，两条须同时成立。第二次提交（2026-10-09）：解释器层原有各项全部通过。关闭证据（2026-10-09，RTX 4090 D，torch 2.13.0+cu130，Triton 3.7.1，实现文件 SHA-256 前缀 `481ff6f4`）：解释器层 `82 passed, 9 skipped`，GPU 层缺省 `num_sm` 一项通过。 |
| F-03 | A1 | 阻塞 | 已关闭 | 2026-10-09 第二次 Review：两个问题各自位于不同设备（同一问题内的 A、B 设备一致）时没有抛 `ValueError`。原有测试只覆盖同一问题内 A、B 设备不同的情形，属验收测试的缺口：设备检查改为 4 种情形（同一问题内的 B、第一个问题、最后一个问题、`out`），并以不发射的替身代替 kernel，使缺少检查的实现也不会把一个设备的地址交给另一个设备。第二次提交在“第一个问题”“最后一个问题”两项失败（`DID NOT RAISE ValueError`）。关闭证据（2026-10-09，RTX 4090 D，torch 2.13.0+cu130，Triton 3.7.1，实现文件 SHA-256 前缀 `481ff6f4`）：设备检查 4 项在 GPU 层（CPU 作第二设备）与解释器层（`meta` 作第二设备）全部通过。 |

## 条件片段：阶段事件

| 日期 | 覆盖范围 | 证明了什么 | 证据链接 | 标注 |
| --- | --- | --- | --- | --- |
| 2026-10-05 | E-01：开课导入、节点 1–3 与检查；节点 4 首讲 | 节点 1–3 的检查题（MoE 的 8 个专家，换了尺寸分布的迁移场景）一次答对：算出 312 块与各 CTA 6／5 块的分配，指出 K 相同时各块工作量一致、差异只来自余数；指出逐个调用时后 7 次各只占 8 个 SM；判断教程示例更不均衡，根因是各问题 K 不同而调度只均分块数，并自行补充“一块的 K 循环不会拆给多个 CTA”。作答前的三次追问（SM 与 CTA 的区别、与 PyTorch `grouped_mm` 的对比、块大小与均衡的取舍及 CUTLASS 扫描优化的论证依据）都指向设计理由。术语上把 SM 的利用率说成 CTA 的利用率，已当场澄清。讲解顺序调整：对齐提示 `tl.multiple_of` 移到节点 5，与异步拷贝和 TMA 一起讲。 | 本会话；[当前证据](#当前证据)中的模型与编译观察 | 无 |
| 2026-10-06 | E-02：节点 4–5 的检查与复查；节点 6 与导师串讲；综合验收发出 | 节点 4 检查题（K 不是整数倍的预测与测试设计）：正确给出最后一次 K 循环的读取范围、没有越界写及其理由；指出所有输出都可能出错、越界处恰为 0 时会碰巧全对，并得出“测试会假通过”；自行提出把 C 放进更大的缓冲区、核对后半部分不变的保护区测试。差距：把 A 的列越界当成“落到矩阵之外”，没有用上“列号超出会绕到下一行”——A 的越界列大部分读到的是下一行的真实数据，只有最后一行落到 A 之后。已补讲；换条件的复查题（分别只把 A、B 之后的内存清零）一次答对，并指出“A 的行首 24 列恰好为 0”这一例外。随后讲解节点 5（对齐提示、异步拷贝、TMA 描述符与回退），配图解页。学习者追问“是否每一行的行首都要对齐”“奇偶行交替对齐时能否使用”，由此补充了保证可以如实降到 8 或 4 字节而 TMA 不能降档。节点 5 检查题（输出维改为 500）：正确算出 1000 字节的行步长不满足 16 字节条件，正确分析 B、C 在 N 方向的绕行、竞争写与末行越界，并提出“多分配、再切片且不必补零”的输出修法（与 PyTorch 的输出步长补齐一致）。差距有三处，都在“哪个矩阵、哪个版本”上：把没有保证的 C 也算进指针版的对齐问题；漏掉 token 数任意带来的 M 方向越界；没有用上描述符版中 B 转置存放这一条件，因而把 B 也判为不满足。已逐条补讲；换条件的复查题（输入维改为 1020）三问全对：只有 A 的保证不成立并应降到 8，描述符版中 A 与转置后的 B 都不满足，输入无法靠多分配解决而输出可以，并说明 PyTorch 对输入报错是为了不把拷贝代价藏起来。随后完成节点 6（DeepSeek-V3 规模下各节点的落点）与导师串讲，发出综合验收四题（口述、mask 写法的预测、动态领取的设计、陌生后端的迁移）。 | 本会话；[当前证据](#当前证据)中的地址模型；[节点 5 图解页](../attachments/08-grouped-gemm/grouped-gemm-data-movement.html) | 无 |
| 2026-10-07 | E-03：综合验收 | 口述题讲清了按同一块大小切分、块队列、按 pid 领取并以块数前缀和对应问题、块内 GEMM 与 `+= NUM_SM` 的循环，给出两项收益、三项代价和适用范围；没有说到矩阵经地址表交给 kernel 这一环和教程的边界假定。预测题正确：行方向的 mask 可以保持 16 字节异步拷贝，三个方向都加 mask 不行，理由是一段 8 个元素只能整段跳过，并判断 DeepSeek-V3 场景只需行 mask；一处不精确，把“够用”的条件说成 8 的倍数而不是块的整数倍。设计题方向正确但方案偏重：提出每块一个领取标记加原子操作，没有想到单个计数器；对“顺序扫描仍成立”给出了结论，但没有说出编号单调递增这一理由。迁移题指出回退为逐个 `mm`、两个版本在该后端都退回同步搬运、`num_sms()` 写死 148；漏掉回退路径把偏移表拷回主机带来的同步，优先级里没有提 M 方向的正确性。已补讲计数器方案；复查题一次答对：原子的“读旧值并加 1”使两个 CTA 领到相邻的两块，一次领 4 块减少领取次数但均衡变粗，并自拟 K=7168 与 K=32 两个问题各 4 块的例子说明最不利的情形。至此 O1–O3 的理解证据充分。随后提出练习约定 P1（版本 1），学习者当日接受。验收测试已建立并自检：实现文件不存在时为预期失败（`1 failed, 83 skipped`）；一份不入库的参考实现在只编译层 `10 passed`、解释器层 `74 passed`；8 种故意写错的变体（无 mask、行步长取自形状、缺少输入检查、始终三向 mask、堆叠接口读回偏移表、参差时只按行 mask 写回、对 C 作保证、忽略 K 的参差）均被相应测试判为失败。 | 本会话；调度模型：教程示例组静态最忙 36、动态 32；100 个随机问题上静态 1.09–1.27、逐块动态 1.02–1.04、一次领 4 块 1.14–1.23、一次领 16 块 1.62–1.88（完成时间与平均工作量之比） | 无 |
| 2026-10-09 | E-04：P1 第一至三次提交与 Review（A1–A5、A7）；A6 首答 | 学习者在 GPU 机器上运行原有的 84 项测试：`80 passed, 4 failed`，A1–A5 的测试首次在真实设备上全部通过（设备型号与版本未随输出提供，待补）；本机只编译层 `10 passed`。kernel 的调度、两种特化与 mask 的写法符合约定。Review 形成两个阻塞问题 F-01、F-02；F-01 同时暴露了验收测试的缺口，已补入 4 项（共 88 项），约定本身未变。A7 首次尝试：堆叠接口在设备上建表、不读回 `offs`、复用同一个 kernel，但 4 项数值不一致（如 `3112 / 6400`）；学习者为排查加入的调试打印又触发了“读回主机”的断言，已解释该断言的判定方式和禁止读回的理由。本机解释器层对去掉打印的副本复现了与 GPU 相同的数字。学习者两次求助定位，所给帮助见[帮助影响](#条件片段帮助影响)。同日第二次提交（SHA-256 前缀 `20e39ee6`）：F-01、F-02 与 A7 的修改在本机通过，当时的 88 项为只编译层 `10 passed`、解释器层 `78 passed`。复查设备检查时发现测试的第二处缺口，形成 F-03，测试改为 91 项，该提交在解释器层为 `80 passed, 2 failed`。不进入门槛的预测题（DeepSeek-V3 规模下以 int32 计算的地址偏移）：学习者指出乘积超出 int32 的范围并给出数值，提出把 `offs` 改为 int64；已补充应加宽的是乘法而不是接口的类型。同日第三次提交（SHA-256 前缀 `481ff6f4`，本机与 GPU 机器上的文件一致）：学习者在 RTX 4090 D（torch 2.13.0+cu130，Triton 3.7.1）上运行 91 项测试，GPU 层 `91 passed`、解释器层 `82 passed, 9 skipped`；本机只编译层 `10 passed`、解释器层结果相同。A1–A5 与 A7 全部通过，F-01 至 F-03 关闭；堆叠接口的偏移已先转成 int64 再相乘。A7 的独立证据成立（定位有协助，原因与修复由学习者自己得出）。不阻塞的观察：实现文件有 18 条 Ruff 提示，入库前需要处理。随后发出 A6。A6 首答：dtype 与指针转型、行内连续与列步长恒为 1、对齐与 16 字节异步拷贝三处对应关系正确；差距有四处——第二问选了维数检查，并认为对齐不满足时会“报错”，没有用上“对齐提示是不被检查的保证、违反时是未定义行为”；多项检查的后果写成“编译报错”，而在删去相应检查的副本上实测多为不报错的错误结果或越界；设备检查答成“需要 CUDA”，没有说到表中地址只在所属设备上有效；没有覆盖形状检查，也没有区分对齐检查对 A、B 与对 `out` 的不同。已用实测表补讲，并发出两道换条件的复查题（`out` 为行步长 200 字节的视图时的处理；为什么数值测试能发现 dtype 与行内连续的问题而不能发现对齐的问题）。复查结果：第二题通过（前两类改变读到的数据或其解释，对齐是未定义行为、结果可对可错）；第一题仍把对齐的保证算到 C 上，认为拒绝该 `out` 是为了保住 `tl.multiple_of` 的前提——与节点 5 的差距相同，是第三次出现。已改从学习者自己的 kernel 出发补讲：保证只存在于调用了 `tl.multiple_of` 的指针上（编译出的 TTIR 中 `tt.divisibility` 恰有 2 处，A、B 共 12 条 16 字节的 `cp.async`，C 是 32 条 `st.global.b16`），并对照指针版与描述符版对 C 的不同要求；随后发出第二轮复查题（删去 B 的保证后三类张量各自还有无对应假定，以及未对齐的 B 是否仍是未定义行为）。不阻塞的观察：包装函数对 `out` 也做对齐检查，会拒绝 kernel 能正确处理的输出视图。第二轮复查一次答对：只有 A 仍有保证，B 与 `out` 没有对应的假定；没有保证就没有未定义行为，B 改为同步读入，代价是失去异步拷贝（实测删去该行后 A 仍有 6 条 16 字节的 `cp.async`，B 变为 16 条 `ld.global.b16` 加 16 条 `st.shared.b16`）。A6 通过。至此 A1–A7 全部满足、阻塞问题为 0，进入结课确认。学习者另外报告了编写时遇到的四个实现问题，已复现并记入[当前证据](#当前证据)。学习者选择不做可选的 GPU 观察，并确认结课。Agent 没有修改学习者的文件。 | 学习者提供的 pytest 输出；[需要跟踪的问题](#条件片段需要跟踪的问题)；[帮助影响](#条件片段帮助影响)；[结课](#条件片段结课) | 结课 |

## 条件片段：结课

| 目标 | 所需证据 | 证据链接 | 判断 |
| --- | --- | --- | --- |
| O1：grouped GEMM 的完整数据流与取舍 | 理解 | E-01 的节点 1–3 检查；E-03 的口述题 | 充分 |
| O2：静态调度的均衡、`NUM_SM` 的取舍与失效边界 | 理解 | E-01 的节点 3 检查；E-02 的节点 4 检查与复查；E-03 的设计题与计数器方案的复查 | 充分 |
| O3：tensor descriptor、TMA、回退与真实系统 | 理解 | E-02 的节点 5 检查与复查；E-03 的预测题与迁移题 | 充分 |
| O4：实现并验证支持任意尺寸的 grouped GEMM | 理解、实践 | [练习约定 P1](#条件片段练习约定) 的 A1–A7；E-04：GPU 层 91 项、解释器层 82 项、只编译层 10 项通过，F-01 至 F-03 关闭，A6 经两轮复查通过，A7 为无提示变式 | 充分 |

- **未关闭的阻塞问题**：0。F-01 至 F-03 均已关闭，见[需要跟踪的问题](#条件片段需要跟踪的问题)。
- **帮助影响是否已恢复**：不需要恢复。A7 只在定位环节得到协助（失败现象、表的定义、与已通过路径对比的方法），原因和修复由学习者
  自己得出，独立证据成立，见[帮助影响](#条件片段帮助影响)。
- **非阻塞余项**：包装函数对 `out` 也做对齐检查，会拒绝 kernel 能正确写入的输出视图；堆叠接口没有输入检查，N、K 整块时它对
  `x`、`w` 作了同样的对齐保证；`num_sm` 缺省时查询的是默认 CUDA 设备而不是输入所在的设备；`grouped_matmul` 逐个问题向设备
  写表。未对齐的输入在真实硬件上的表现、描述符版在有 TMA 的设备上的运行、任何性能对比都没有实测；约定中的可选 GPU 观察
  学习者选择不做。验收测试的“不读回主机”检查拦不住经普通张量转存后再读回的数据。以上都不在本课范围内，需要时另行授权。
- **学习者确认**：2026-10-09，学习者回复“不做可选的gpu观察了。请结课吧。”
- **入库版本的整理**：实现文件原有 18 条 Ruff 提示，仓库的 CI 会检查它。结课后经学习者选择，由 Agent 做了不改逻辑的整理：
  格式化、import 排序、注释里的全角标点、一个未使用的解包变量、一处等价的条件写法。整理前后 kernel 函数的 AST 相同，
  sm_89 与 sm_90 上两种特化的 PTX 指令流相同；包装函数只有 4 处等价改写。整理后的文件在本机只编译层为 `10 passed`、
  解释器层为 `82 passed, 9 skipped`；GPU 层没有复跑，GPU 证据对应整理前的版本。
- **结课结论**：学习者能讲清 grouped GEMM 怎样把一组尺寸不同的矩阵乘法合并成一次发射（地址表间接、固定数量的 CTA 跨问题领取
  tile、tile 内的常规 GEMM），并说明它相对逐个发射和 batched GEMM 的收益与代价；能分析静态调度的均衡、`NUM_SM` 与块大小的
  取舍，指出满块假定与对齐保证的失效方式，并给出单计数器的动态领取设计；能解释对齐提示、异步拷贝、TMA 描述符与没有 TMA 时的
  回退，并迁移到 PyTorch `grouped_mm`、CUTLASS 和非 NV 后端；独立实现了 M 任意、按 N 与 K 是否整块分两种特化的 kernel、
  带输入检查的包装函数和不读回偏移表的堆叠接口，通过只编译、解释器与 GPU 数值验收，并能说明每项检查对应的 kernel 假定，
  以及对齐检查为什么无法由数值测试发现。本结论的范围是 Triton v3.7.1、NVIDIA 后端 sm_89 与 sm_90 的只编译观察、CPU
  解释器，以及一台 RTX 4090 D（sm_89）上的数值验收；描述符版与 AMD 后端只有只编译观察，性能未测。
