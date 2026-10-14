# 第 09 课：持久化矩阵乘——跨 tile 的流水、TMA 与 warp 专用化

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-09-persistent-matmul` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 解释把分块矩阵乘做成持久化 kernel 的整套设计（每个 SM 一个 CTA 循环领取 tile、跨 tile 的流水、TMA 搬运、warp 专用化、epilogue 拆半）各自消除哪一段空转、依赖哪一代硬件、付出什么资源，能判断它们在缺少这些硬件特性的设备上退到哪一档，并实现、验证和度量一个持久化矩阵乘 kernel |
| 阶段 | `complete`（2026-10-14 结课） |
| 启动授权 | 2026-10-10，学习者提出“好，接下来让我们开始下一节triton课程的学习吧。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/09-persistent-matmul.py` | `teaching-spine` | 仓库 commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；本地 SHA-256 `26b19072955dd4472f9821d68c97943f625137f89850be1c5d9451cae3011aa3`。与 v3.7.1 tag 的 `python/tutorials/09-persistent-matmul.py` 逐字相同（2026-10-10 以 `diff` 核对） | 教学顺序与示例：五个 kernel（逐 tile 发射、TMA、持久化、TMA 持久化、设备侧描述符持久化）及其包装函数、autotune 配置、基线与 benchmark |
| [Triton v3.7.1](https://github.com/triton-lang/triton/tree/v3.7.1) | `implementation-authority` | tag `v3.7.1`，commit `f797708c0626e5f9840ca5b0a98790e2c7cb09ad`，与 `uv.lock` 一致；核对于 2026-10-10 | `python/triton/language/core.py` 中 `tl.range` 的 `flatten`、`warp_specialize` 等参数；`third_party/nvidia/backend/compiler.py` 按 compute capability 分支的 pass 流水线；`lib/Dialect/TritonGPU/Transforms/FuseNestedLoops.cpp` 的循环合并；`lib/Dialect/TritonGPU/Transforms/Pipeliner/{AssignLatencies.cpp,PipeliningUtility.cpp}` 的流水选择条件；`third_party/nvidia/hopper/lib/Transforms/WarpSpecialization.cpp` 的 Hopper warp 专用化前提；`python/triton/tools/tensor_descriptor.py` 与 `third_party/nvidia/backend/driver.py` 对主机侧描述符的检查和展开；`python/triton/runtime/autotuner.py` 与 `python/triton/compiler/compiler.py` 对资源超限的处理；`third_party/nvidia/include/cublas_instance.h` 的基线库加载 |
| [CUTLASS v3.9.2](https://github.com/NVIDIA/cutlass/blob/v3.9.2/media/docs/cpp/efficient_gemm.md) | `explanatory-support`（真实系统锚点） | tag `v3.9.2`；取回于 2026-10-10 | `media/docs/cpp/efficient_gemm.md` 的 “Hopper Warp Specialization” 一节：producer／consumer warp 组、持久化线程块的收益（摊薄线程块发射与 kernel prologue 的开销）、Cooperative 与 Ping-Pong 两种设计 |
| [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html) | `interface-authority` | 访问于 2026-10-10 | [§5.1 Compute Capabilities](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compute-capabilities.html)：各 compute capability 的每线程块共享内存上限、每 SM 的寄存器数与可驻留 warp 数；[§3.2.2.2 Hardware Multithreading](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html)：SM 把驻留的线程块拆成 warp，由 warp 调度器在每个发射周期挑选就绪的 warp，切换没有代价 |
| [PTX ISA 9.4](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html) | `interface-authority` | 版本 9.4；副本保存于 2026-10-06（第 08 课），2026-10-12 用于本课 | `cp.async.bulk.tensor`（异步的张量拷贝，以 `mbarrier` 报告完成）、`tensormap.replace`；`wgmma.mma_async`（warpgroup 为 4 个相邻的 warp；A 可在寄存器或共享内存，B 必须在共享内存）；`tcgen05`（`mma` 由一个线程发起；Tensor Memory 在 sm_100 上为每个 CTA 512 列 × 128 行、每格 32 位，按 32 列为单位分配；D 在 Tensor Memory，A、B 经共享内存描述符给出） |
| NVIDIA 架构说明：[Tesla V100 架构白皮书](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)、[Ampere Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-ampere-architecture-in-depth/)、[Hopper Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) | `explanatory-support`（硬件结构锚点） | 取回于 2026-10-11 | SM 的内部划分与张量核心数量：V100 的 SM 分为 4 个处理块，每块有 1 个 warp 调度器和 2 个张量核心；A100 每个 SM 有 4 个张量核心（每个分区 1 个，合计每时钟周期 1024 次 fp16 乘加），共 108 个 SM；H100 每个 SM 有 4 个张量核心。sm_89 与 Blackwell 的对应数字未查到公开来源 |

### 目标与所需证据

| ID | 可观察目标 | 理解 | 实践 | 实证 |
| --- | --- | --- | --- | --- |
| O1 | 讲清持久化矩阵乘的完整数据流与调度：发射网格从“每个 tile 一个 CTA”变为“每个 SM 一个 CTA、按步长 `NUM_SMS` 领取 tile”，持久循环内怎样保持 grouped ordering；一个 tile 的三段（prologue、K 循环、epilogue）；`flatten` 把两层循环合成一层后流水怎样跨过 tile 边界，为此付出什么。说明它相对逐 tile 发射换来什么、什么时候不划算 | 需要 | 不需要 | 不需要 |
| O2 | 解释搬运与计算的分工在硬件代际间的演进并能迁移：`cp.async` 加 `mma.sync`、TMA 加 `wgmma`、TMA 加 `tcgen05` 与 TMEM；主机侧与设备侧描述符；warp 专用化解决什么、前提与代价；epilogue 拆半与流水深度怎样争用共享内存；同一份源码在 sm_89、sm_120 与非 NV 后端上各退到哪一档 | 需要 | 不需要 | 不需要 |
| O3 | 会度量并解释矩阵乘 kernel 的性能：TFLOPS 与 launch metadata、proton、与 cuBLAS 和 `torch.matmul` 的基线；对“持久化在自己的设备上是否更快、随 K 怎样变化”先给出可证伪的预测，再用受控测量和编译产物解释结果并说明结论的边界 | 需要 | 不需要 | 需要 |
| O4 | 实现并验证一个持久化矩阵乘 kernel 与包装函数：本机以只编译和解释器检查，GPU 上与 `torch.matmul` 数值对照 | 需要 | 需要 | 不需要 |

O3 的实证只要求在学习者能用的设备上比较逐 tile 发射与持久化两种调度。TMA、warp 专用化与 FP8 的实机运行、与 cuBLAS 的对比结论、autotune
调参都不属于完成门槛；有 sm_90 及以上或 sm_120 的设备时可以作为观察另行约定。练习的具体内容在综合验收之后按仍缺的证据约定。
学习者在节点 3 提出的“把第 08 课的 grouped GEMM 改造成能跨 tile 流水”（2026-10-12）是 O4 练习的候选题目，尚未约定。

**实测设备（学习者 2026-10-11 说明）**：主测量预计使用 NVIDIA GeForce RTX 4070 Laptop GPU，另可使用 RTX 5090 与 RTX 4090。
NVIDIA 的[列表](https://developer.nvidia.com/cuda/gpus)把 GeForce RTX 4070 与 RTX 4090 归在 compute capability 8.9（不区分桌面与
笔记本型号），RTX 5090 为 12.0；[笔记本型号对照表](https://www.nvidia.com/en-us/geforce/laptops/compare/)给出该型号 4,608 个 CUDA
核心、8 GB 显存、GPU 子系统功耗 35–115 W、boost 时钟 1230–2175 MHz（均取回于 2026-10-11）。按每个 SM 128 个核心推算为 36 个 SM，
属推断；设备名、capability、SM 数、共享内存上限与运行环境（原生 Linux、WSL2 或容器）都还没有在该设备上读取，已请学习者上机时
读一次。教程脚本在 capability 主版本小于 9 的设备上只运行 cuBLAS、`torch.matmul`、逐 tile 发射与持久化四个版本（第 59–68、85–87、
662–678 行），满足 O3 的门槛；TMA 与 warp 专用化的实机观察只有 RTX 5090 能做，仍是另行约定的可选项。笔记本的功耗与温度漂移是
测量设计要控制的风险：教程 `bench()` 对每个版本连续运行 10,000 次预热与 10,000 次测量后才换下一个版本（第 644–668 行）。

**设备读数（学习者 2026-10-12 贴回，改用借到的 RTX 5090）**：`NVIDIA GeForce RTX 5090 (31.4 GiB)`，capability `(12, 0)`，170 个 SM，
每个 CTA 的共享内存上限 101,376 字节（Triton 的 `max_shared_mem`），`torch 2.13.0+cu130`、`triton 3.7.1`，内核 `5.15.0-119-generic`
（原生 Linux）。上限与此前按 CUDA 文档取的 99 KB 一致，SM 数与按 21,760 个 CUDA 核心的推算一致。该设备的 capability 主版本不小于 9，
教程脚本会运行描述符版与 warp 专用化的版本，可选观察因此具备条件，是否进行尚未约定。

**O3 的预测（学习者 2026-10-12，先于任何测量）**：块固定为 `128×128×64`、`M = N = 8192`，K 取 128、512、2048 时，持久版对逐 tile 发射版的
TFLOPS 比值随 K 增大而下降；理由是持久化省掉的是重复发射的开销，K 增大后 K 循环在 kernel 中的占比变大、发射部分占比变小。
可证伪条件：比值没有显著变化，或反而随 K 增大。预测作出时题面写的设备是 RTX 4070 Laptop，同一条回复里学习者说明改用 RTX 5090；
推理不依赖具体设备，实测时以 5090 为准，并以测量的波动幅度界定“显著”。

**M1 的测量结果（2026-10-14，学习者在 RTX 5090 上运行）**：AutoDL 容器，NVIDIA GeForce RTX 5090，capability (12, 0)，170 个 SM，torch 2.13.0+cu130（CUDA 13.0），Triton 3.7.1；实现文件 `6d628fbc`，测量脚本 `01fbd235`，设置见练习约定一节。三个版本的最大相对误差都在 2.5e-4 以内；编译资源：逐 tile 与持久 `flatten` 关为共享内存 65,536 B、每线程 182 个寄存器，持久 `flatten` 开为 73,728 B、154 个，都没有溢出。各轮中位数（ms）与TFLOPS：K=128 时逐 tile 0.1286（133.5）、持久关 0.1260（136.4）、持久开 0.1061（162.0）；K=512 时 0.3584（191.7）、0.3580（191.9）、0.3461（198.5）；K=2048 时 1.2790（214.9）、1.2790（214.9）、1.2951（212.2）。逐 tile 对持久开的时间比 S(K) 依次为 1.213（1.207–1.220）、1.037（1.035–1.040）、0.987（0.983–0.989）；对持久关为 1.023（1.018–1.028）、1.002（0.995–1.006）、1.000（1.000–1.000）。按运行前打印的判据，主判据与辅助判据都判为“支持”。学习者对结果的解释尚待提交。学习者随后说明，作预测时所说的“持久版”指不带 `flatten` 的持久化；脚本把带 `flatten` 的比值定为主判据，是 Agent 未经确认的假设。两种比值的判据都在运行前打印，结论都是“支持”，所以改按学习者的原意（逐 tile / 持久关）评判，结论不受影响，也不存在看过结果再挑判据的问题。

**M1 的解释（学习者 2026-10-14，第二稿，判定通过）**：指出持久化本身的效应很小（最多 2.3%），数据不能支持“收益来自重复发射变少”，因为这一列同时包含 CTA 分派、每个 CTA 的固定工作与调度方式三项变化，比值随 K 下降也不一定是发射占比变小；指出总比值的大部分来自 `flatten`（1.184、1.035 远大于 1.023、1.002），K=2048 时 `flatten` 为净代价，并对“多出的共享内存是原因”自行存疑（写回总要经过共享内存）；列出测量回答不了的两点（持久化一列里三项各占多少；`flatten` 一列里流水的收益与未知代价各占多少）。评语中补充两点：静态领取的积压在本例两种调度下都是最后多出一个 tile，占比不随 K 变化，难以解释随 K 的趋势；三个版本每个 SM 都只驻留 1 个 CTA，多出的共享内存与少用的寄存器都没有改变驻留数。另以未验证的假设给出 `flatten` 在大 K 下的一种可能代价（合并后每一轮都要做是否进入新 tile、是否写回的判断）。首稿只复述了判据的结论，经三个引导问题后重写。

**A6 的说明（学习者 2026-10-14，第二稿，判定通过）**：第一点——`offset_n` 若在 prologue 里算，合并后只有进入 `if` 的那条路径带着声明，不进 `if` 的路径沿用旧值，流水看不到连续性，所以把它的计算挪进 K 循环并声明 N 方向连续；第二点——流水为后面的 tile 做准备，epilogue 执行时 `tile_id` 已指向下一个 tile，所以 epilogue 要有自己的游标。首稿把第二点归因于作用域，经指向教程注释、图解页交接表与第四版现象后改正。学习者随即追问自己的代码为何不需要独立游标：已用其第五版的 TTGIR 说明，编译器在合并循环里自动多带了一份落后一步的 `tile_id_n` 与行起点（`iter_args` 中的 `%tile_id_n_110`、`%offset_m_109`），epilogue 用它们重算坐标；教程手写 `tile_id_c` 是为了打断 prologue 与 epilogue 的依赖（第 538–539 行），并规避 Blackwell 流水的缺陷（第 305–306 行），去掉它的探查副本在 sm_100 上寄存器由 104 增至 114。“为什么不是正确性所必需”这一半由 Agent 补充。

**V1（学习者 2026-10-14，无提示，判定通过）**：预测“`flatten` 关与开时 A 仍是 16 字节一组、仍提前发出，因为声明只是为了补上被 `tl.where` 干扰的连续性，去掉 `tl.where` 后就不需要”，并在实现中注释掉这两行（第六版 `27b89b39`）。本机验证：解释器层 `46 passed, 16 skipped`，只编译层 `16 passed, 46 skipped`；sm_89、sm_90 两种取值下都是 12 处 16 字节 `cp.async`、循环内等待 `num = 2`，与预测一致。只编译层由 Agent 在本机运行。

### 当前证据

- **已有证据**：[阶段事件](#条件片段阶段事件) E-01 至 E-03 提供 O1 的节点级理解证据（节点 1–3 已通过）。已确认的前置只决定讲解起点：Lesson 02 的 persistent kernel（按 occupancy 确定 program 数、`num_stages` 软件流水的
  prologue 与 epilogue）、Lesson 03 的分块矩阵乘（tile 数据流、grouped ordering、autotune 与一次受控测量）、Lesson 06 的 `tl.dot` 与 FP8
  （warp 专用化只提到过，不在当时的门槛内）、Lesson 08 的按步长领取 tile、对齐保证、`cp.async` 与 TMA 描述符及其回退。
- **仍缺证据**：O1、O2 所需的理解证据已充分（节点级检查与综合验收，见 E-01 至 E-10）。O3 仍缺实测结果与学习者对结果的解释（理解部分与测量前的预测已有）；O4 仍缺独立实践证据。练习约定 P1 已于 2026-10-12 接受，验收测试已建立并确认 expected red，见[练习约定](#条件片段练习约定)。
- **来源与环境核对（2026-10-10）**：本机无 NVIDIA GPU，在仓库外的临时环境（`triton==3.7.1`、`torch==2.13.0+cu130`）中只编译不运行；
  特化方式与 `JITFunction.run` 相同（指针参数带 16 字节对齐、等于 1 的步长成为常量）。以下各项的条件都是 fp16、`M=N=8192`、`K=512`、块
  `128×128×64`、`GROUP_SIZE_M=8`、`num_stages=3`、`num_warps=8`，共享内存以字节计。两个指针版 kernel 的 B 有两种传法：教程 `bench()` 与
  `validate()` 传入的是 `b.T`（内存中按 `[N, K]` 存放，步长 `(1, K)`，连续方向是 K）；普通的行主序 `[K, N]` 步长为 `(N, 1)`，连续方向是 N。
  2026-10-10 的首次核对只编译了后一种，2026-10-11 补上前一种并据此更正了下表与相关条目。

  | kernel | sm_89 | sm_90 | sm_100 | sm_120 |
  | --- | --- | --- | --- | --- |
  | `matmul_kernel`（两种传法相同） | `cp.async` 24 条，`mma.sync`，65,536 | `cp.async` 24 条，`wgmma`，98,304 | `cp.async` 32 条，`tcgen05.mma`，98,320 | `cp.async` 24 条，`mma.sync`，65,536 |
  | `matmul_kernel_persistent`，B 为 `b.T`（教程的传法） | `cp.async` 24 条，98,304 | `cp.async` 24 条，131,072 | `cp.async` 32 条，106,512 | `cp.async` 24 条，73,728 |
  | `matmul_kernel_persistent`，B 为行主序 `[K, N]` | A 为 `cp.async` 12 条，B 为同步的 `ld.global.v4` 4 条，65,536 | 同样只有 A 异步，81,920 | 同样只有 A 异步，49,160 | 同样只有 A 异步，49,152 |
  | `matmul_kernel_tma` | 描述符改写为普通读写，`ld.global.b16` 64 条，无异步拷贝，32,768 | TMA 读写，98,328 | TMA 读写，98,352 | TMA 读写，`mma.sync`，65,552 |
  | `matmul_kernel_tma_persistent`，不拆半／拆半 | 同上一行，32,768 | 131,096／114,712 | 131,120／114,736 | 98,320／81,936 |
  | `matmul_kernel_descriptor_persistent`，`flatten` 开／关 | `cp.async` 24 条，98,304／65,536 | 每个描述符 13 条 `tensormap.replace`，全局暂存 384 字节，131,096／131,096 | 131,120／131,120 | 98,320／98,320 |

  - 指令族：sm_89 与 sm_120 用 `mma.sync`，sm_90 用 `wgmma.mma_async`，sm_100 用 `tcgen05.mma` 且累加器放在 TMEM（元数据 `tmem_size`
    为 128 或 256 列）。sm_120 没有 `wgmma` 与 `tcgen05`，但描述符版使用 TMA（`cp.async.bulk.tensor.2d`）与 mbarrier。
  - epilogue 拆半使 TMA 持久版的共享内存少 16,384 字节，等于半个输出块（`128 × 64 × 2`）。
  - **`flatten` 与流水**：B 按教程的传法（`b.T`）时，`matmul_kernel_persistent` 的 A、B 都是异步拷贝，代价是共享内存比逐 tile 发射的版本多
    一档（sm_89 上 98,304 对 65,536，sm_90 上 131,072 对 98,304）；把 `flatten` 改成可开关的探查副本显示，关闭后共享内存回到与
    `matmul_kernel` 相同。B 为行主序 `[K, N]` 时，`flatten` 开启后只有 A 的读入成为异步拷贝，B 是同步读入；关闭时 A、B 都是异步拷贝。
    逐 pass 的 IR 转储显示，`tritongpu-fuse-nested-loops` 之后外层循环的 prologue 位于 `scf.if` 中，`tritongpu-assign-latencies` 只给 A 的
    `tt.load` 标了 `tt.latency = 2`。把列偏移及其连续性提示移到 K 循环内计算的副本，在两种设置下都得到 24 条 `cp.async`；据此判断原因是
    带提示的 `offs_bn` 经 `scf.if` 传出后，流水选择阶段取不到它的连续性（`canBeConvertedToAsyncLoad` 要求连续宽度不少于 32 bit）。
    `b.T` 的连续方向是 K，其偏移在 K 循环体内计算，不经过这个 `scf.if`，所以不受影响。
  - **`flatten` 的结构与代价（2026-10-11，B 为 `b.T`）**：不合并时，每个 tile 在 K 循环前发出两轮异步拷贝、循环后以 `async_wait {num = 0}`
    排空；合并后这两处各只出现一次，位于整个合并循环的前后，循环体内依次是下一个 tile 的 prologue（`scf.if`）、等待与 `tt.dot`、
    为两轮之后发出的异步拷贝、当前 tile 的 epilogue（`scf.if`）。IR 中 prologue 与 epilogue 各有自己的 tile 游标，对应源码的
    `tile_id` 与 `tile_id_c`。合并前后输入缓冲都是每个操作数 2 个槽（sm_90 为 3 个）；多出的共享内存是 epilogue 中
    `ttg.convert_layout`（`#mma` 到写回布局，fp16）的中转缓冲，`lib/Analysis/Allocation.cpp` 按该操作自身的存活期为它分配，不合并时
    与已不再使用的输入缓冲重叠。中转的大小等于整块除以转换的批数：块 128×128、8 个 warp 时为 32,768，4 个 warp 时为 16,384，
    `BLOCK_N=256`、8 个 warp 时为 8,192。每线程寄存器在合并前后相近：sm_89 为 166 与 160，sm_90 为 118 与 116，sm_100 为 101 与 104；
    sm_100 上共享内存为 98,320 与 106,512。
  - **`flatten` 的适用条件（2026-10-11）**：把 K 循环次数改成随 tile 变化（`range(k_tiles - (tile_id % 2))`）的探查副本上，`flatten=True`
    与不写的产物相同（没有 `scf.if`，共享内存不变），也没有任何报错或警告。2026-10-12 重读 `FuseNestedLoops.cpp` 并补做实验后，
    依据更正为三条：`shouldFuse` 只接受恰有两个节点、根循环带 `tt.flatten` 的嵌套；构造嵌套时遇到其他带区域的操作（`scf.while`、
    `scf.if`）就另起一组；内层边界不随外层变化时由 `speculateInnerLoopLength` 处理，随外层变化时要求匹配到 `llvm.assume(ub > lb)`，
    且边界可由函数参数与外层循环变量经无副作用或只读内存的标量操作算出（`canSliceBounds`），这时先生成一个求总迭代数的循环。
    pass 开头“只合并边界不随父循环变化的子循环”的注释与这段代码不一致，以代码与实验为准。
  - **把 grouped GEMM 改成可合并的形状（2026-10-12，探查副本，只编译）**：以学习者第 08 课的实现为底改写六种循环形状，块
    `128×128×64`、3 个 stage、8 个 warp、`NUM_SM=36`，A、B 行主序，指针与行步长从表中读出。以下为 sm_89／sm_90 的共享内存。
    原写法（`for` 问题、`while` 领取、`for` K）加 `flatten=True` 前后都是 65,536／98,304；只把 `while` 换成 `for`（三层 `for`）
    前后相同；在该三层的 tile 循环外包一层 `if`，里面两层被合并（98,304／131,072），流水仍在每个问题的边界重新预热。改成
    “一个 `for` 遍历本 CTA 的全部 tile、问题号查主机建的表、K 为共用标量”的两层嵌套后合并生效：行列偏移在 tile 开头算时
    B 退回同步读入（65,536／81,920，`cp.async` 12 条加 `ld.global.b16` 32 条），偏移挪进 K 循环后 A、B 都是异步拷贝
    （98,304／131,072，24 条）。K 逐 tile 从表中读出时，不加 `tl.assume` 则 `flatten=True` 被忽略，加
    `tl.assume(num_k_tiles > 0)` 后合并（sm_89 为 98,304，24 条）。均未在设备上运行，数值与性能未验证。
  - **流水深度与共享内存（2026-10-12，教程 `matmul_kernel_persistent`，sm_89，B 为 `b.T`）**：`flatten` 开／关在 4 个 stage 时为
    131,072／98,304，5 个 stage 时为 163,840／131,072，与“每个操作数 S−1 个槽”一致。`python/triton/compiler/compiler.py` 在
    加载二进制之前比较 `metadata.shared` 与设备的 `max_shared_mem`，超限抛 `OutOfResources`；`runtime/autotuner.py` 捕获后把
    该配置记为无穷大，只有设了 `TRITON_PRINT_AUTOTUNING` 才打印。寄存器不足的处理不同：`driver.c` 的 `load_binary` 读回
    `n_regs` 与 `n_spills`（本地内存字节数除以 4）。
  - **查看编译产物的途径（2026-10-12）**：`JITFunction.run` 返回编译结果对象（`runtime/jit.py`），其 `asm` 以扩展名为键保存各阶段
    文本，`metadata.shared` 为共享内存；缓存目录每个特化一个子目录，含 `.ttir`、`.ttgir`、`.llir`、`.ptx`、`.cubin`、`.json`、
    `.source`，位置可用 `TRITON_CACHE_DIR` 指定。图解页“查看产物”一节的两份 TTGIR 由教程原文件直接编译得到（导入模块时以
    替身驱动绕过设备探测；`flatten` 关的一份只把第 312 行改为 `False`），位置信息带教程行号。两份的
    `ttg.async_copy_global_to_local` 都是 6 处、`ttg.async_wait` 都是 2 处、`ttg.local_alloc` 都合计 65,536 字节；`scf.if` 为 0 处
    与 4 处。排空的 `ttg.async_wait {num = 0}` 在关时位于 tile 循环内（第 190 行，位置记为教程第 324 行），开时位于合并循环
    之后（第 335 行，记为第 312 行）；输入缓冲的 `ttg.local_dealloc` 在关时位于 epilogue 之前（第 191–192 行），开时位于循环之后
    （第 336–337 行）。页面上的两段命令已按原文在本机运行：对第 08 课 kernel 的只编译脚本输出 `shared memory: 65536 bytes`。
  - **去掉 `tile_id_c`（2026-10-11）**：让 epilogue 直接使用 prologue 算出的坐标的探查副本，在 sm_89、sm_90、sm_100 上都能编译，读入方式与
    共享内存不变；sm_100 上每线程寄存器由 104 变为 114。教程注释所说的 Blackwell 流水缺陷无法由只编译判断。
  - **warp 专用化**：sm_90 上 8 个 warp 时 `warp_specialize=True` 不改变产物；Hopper 的 pass 要求恰好 4 个 warp，且函数内没有带 else 块的
    `scf.if`（循环合并后必然有）。4 个 warp、设备侧描述符、`flatten` 关闭时生效：总 warp 数由 4 变为 12，`mbarrier.init` 33 条，共享内存
    131,544；4 个 warp 的 `matmul_kernel_tma` 开启后编译失败（`PassManager::run failed`）。这与教程在第 592、673、713 行的三处规避一致。
    sm_100 与 sm_120 上 8 个 warp 即生效，总 warp 数由 8 变为 12；sm_120 上开启后的共享内存为 98,572（`matmul_kernel_tma`）与
    131,196／114,812（TMA 持久版不拆半／拆半）。
  - **教程的 24 组配置在 sm_89 上**：B 按教程的传法时，`matmul_kernel` 需要 32,768–294,912 字节，`matmul_kernel_persistent` 需要
    49,152–303,104 字节，后者在每一组配置上都不少于前者。CUDA 文档给出的每线程块上限是 sm_89 与 12.x 为 99 KB、sm_80 为 163 KB、
    sm_90 与 sm_100 为 227 KB；按 99 KB 计，前者有 10 组、后者有 16 组超限。B 为行主序时持久版需要 32,768–163,840 字节，6 组超限。
    Triton 在加载 kernel 时抛出 `OutOfResources`，autotuner 把这类配置的耗时记为无穷大。
  - **越界下标的处理方式（2026-10-11，sm_89，`matmul_kernel` 及其探查副本）**：比较不处理、`tl.where(…, 0)` 加声明（教程）、
    `tl.where(…, 0)` 不加声明、取模、给读入加 M 与 N 方向的 mask 五种写法。B 为 `b.T` 时五种写法都是 24 条 16 字节的 `cp.async`。
    B 为行主序、N 是 16 的倍数（1024）时，只有“不加声明的 `tl.where`”使 B 退回 32 条逐元素的同步读入。B 为行主序的视图
    （行步长 1024、N 为 1000）时，取模与 mask 两种写法也退回逐元素读入，教程的写法与不处理仍是 24 条 `cp.async`。行步长本身不是
    16 的倍数（N 为 1000 或 1001 的连续张量）时，五种写法的 B 都是逐元素读入。取模的写法多出 5 条整数除法或取余指令。
  - **轴信息与连续性声明（2026-10-14，结课前答疑，v3.7.1 源码与只编译探查，sm_89）**：`lib/Analysis/AxisInfo.cpp` 中 `arith.select`（`tl.where`）的连续度取两个分支的连续度与条件的恒定度的最大公约数（第 877–880 行），常量 0 的连续度为 1，所以结果为 1；比较 `offs < N` 的恒定度取`offs` 的连续度、`offs` 的整除度与 `N` 的整除度的最大公约数（第 767–769 行）；`tt.contiguity`、`tt.divisibility`、`tt.constancy` 属性无条件覆盖推断值（`visitOperation`）；读入能否成为异步拷贝取指针连续度（受整除度换算的对齐限制）与 mask 恒定度中的较小者，须不少于 32 bit（`PipeliningUtility.cpp` 的 `canBeConvertedToAsyncLoad`）。以一个读行主序 B 的小 kernel 对照（块 64×64×32，N 可被 16 整除）：不用 `tl.where` 为 16 字节异步拷贝；`tl.where` 后不加声明、只加 `max_contiguous`、只加 `multiple_of` 都退回同步读入；两者都加为 16 字节；连续度声明为 4 或整除度声明为 4 时为 8 字节；N 不能被 16 整除时以上各种写法都是同步读入。写在循环里、作用于循环携带指针的声明，因代码生成器对循环体的预演（`code_generator.py` 的 `_find_carries`）落到了循环前那个值的定义操作上，因而生效，这解释了教程 08 第 148–149 行丢弃返回值的写法。学习者实现中带 mask 的 `cp.async` 以第四个操作数（`selp` 得到的 16 或 0）为源字节数，mask 为假时不读源地址、目的处填 0（PTX ISA 9.4）。
  - **寄存器（sm_89，`matmul_kernel`）**：B 为 `b.T` 时每线程 135 个，行主序时 162 个；按每 SM 64K 个寄存器与 100 KB 共享内存，
    两种情形下一个 SM 都只能驻留一个这样的 CTA。K 循环体内有 64 条 `mma.sync…m16n8k16`。
  - 主机侧描述符 `TensorDescriptor` 在构造时检查基地址与非末维步长的 16 字节对齐、末维步长为 1；设备上没有 TMA 时，参数被展开为
    基地址、形状与步长。基线 `CublasLt` 通过 `dlopen("libcublas.so")` 加载。

  以上均为本地编译观察，不代表任何设备上的数值或性能结果；设备的 SM 数与共享内存上限尚未在学习者的设备上读取。
  - **搬运与计算的分工（2026-10-12，教程原文件按各自的调用方式编译，只编译）**：`matmul_kernel`（B 为 `b.T`）与 `matmul_kernel_tma`
    （B 按 `[N, K]` 存放，主机侧描述符，块形状按 `pre_hook` 的写法设置），条件同上。依次为共享内存、每线程寄存器与指令构成。
    指针版：sm_89 为 65,536、135，`cp.async` 24 条、`ldmatrix` 24 条、`mma.sync` 64 条；sm_90 为 98,304、111，`cp.async` 24 条、
    `wgmma.mma_async` 4 条；sm_100 为 98,320、94，`cp.async` 32 条、`tcgen05.mma` 8 条、TMEM 128 列；sm_120 为 65,536、158，指令同 sm_89。
    描述符版：sm_89 为 32,768、255，`ld.global.b16` 与 `st.global.b16` 各 64 条，没有异步拷贝；sm_90 为 98,328、90，
    `cp.async.bulk.tensor.2d` 7 条（6 读 1 写）、`wgmma.mma_async` 4 条；sm_100 为 98,352、71，TMA 9 条、`tcgen05.mma` 8 条、TMEM 128 列；
    sm_120 为 65,552、118，TMA 7 条、`ldmatrix` 24 条、`mma.sync` 64 条。TTGIR 里 sm_89 与 sm_120 的操作数经 `ttg.local_load` 进寄存器，
    sm_90 的 `ttng.warp_group_dot` 与 sm_100 的 `ttng.tc_gen5_mma` 直接以共享内存缓冲为操作数；sm_100 另有 `ttng.tmem_alloc`、
    `tmem_store`、`tmem_load` 各一处。PTX 中 TMA 拷贝由 `elect.sync` 选出的一个线程发出，`mbarrier.arrive.expect_tx` 的期望字节数为
    32,768；sm_90 上 B 的缓冲起始于 A 之后 49,152 字节，即每个操作数 3 个槽。流水实现的注释说明等待完成之前缓冲仍在使用
    （`Pipeliner/LowerLoops.cpp`）。主机侧描述符在 sm_90 上是 `!tt.tensordesc` 句柄，在 sm_89 上被展开为基地址（没有
    `tt.divisibility`）、形状与步长等运行时参数；设备侧描述符的 kernel 在 sm_89 上指针带 `tt.divisibility = 16`，步长写在源码里。
    把 B 改按 `[K, N]` 存放、乘加不转置的探查副本，在 sm_90 与 sm_100 上指令构成与教程写法相同，在 sm_120 上多出转置读取
    （`ldmatrix … trans` 8 条），寄存器为 159 对 118。学习者随后指出两点理由（沿 K 方向连续读取；fp8 要求 B 为转置的摆法），
    经核对成立：PTX ISA 9.4 规定 `wgmma.mma_async` 的转置参数只支持 `.f16`、`.bf16`；以 `torch.float8_e4m3fn` 编译，sm_90 上教程
    写法为 49,176 字节、90 个寄存器、`wgmma…m64n128k32.f32.e4m3.e4m3` 2 条，B 按 `[K, N]` 存放的副本为 49,200 字节、113 个寄存器，
    多出 `ld.shared.v4` 2 条与 `st.shared.b8` 32 条（先取进寄存器重排再存回）；sm_100 上两种写法相同。此前“不下结论”的说法据此更正。
  - **乘加指令的形状（2026-10-12）**：sm_89 为 `mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32`，一个 tile 一轮需
    `(128÷16)×(128÷8)×(64÷16)=512` 次，8 个 warp 各 64 条，与静态条数一致；sm_90 为 `wgmma.mma_async.sync.aligned.m64n128k16.f32.f16.f16`，
    两个 warpgroup 各 4 条；sm_100 的 `tcgen05.mma.cta_group::1.kind::f16` 形状由指令描述参数给出，TTGIR 中 `#tmem` 为
    `tensor_memory_encoding<blockM = 128, blockN = 128>`，PTX ISA 给出该类型 K = 16，每处 `ttng.tc_gen5_mma` 展开为 4 条。
  - **输入槽数的规律（2026-10-12，`flatten` 关的指针版副本）**：`num_stages` 为 2、3、4 时，sm_89 每个操作数为 1、2、3 个槽（S−1），
    sm_90 为 2、3、4 个槽（S）。学习者在节点 4 的复查中自行把“槽被占用的时长”与节点 3 的“S−1 个槽”联系起来，与此一致。
  - **warp 专用化的分区（2026-10-12，教程原文件按各自的调用方式编译，只编译）**：启用后三种目标的发射 warp 数都是 12。
    sm_90（`matmul_kernel_descriptor_persistent`，4 个 warp，`flatten` 关）：默认分区 4 个 warp 做 TMA 搬运（tile 循环套 K 循环），
    两个分区各 4 个 warp 各执行 `ttng.warp_group_dot` 并各写回 64×128 的一半；共享内存 131,096 变为 131,544，`mbarrier.init` 33 条。
    sm_100（8 个 warp）：分区 0 为 1 个 warp，只发起 `ttng.tc_gen5_mma`；分区 1 为 2 个 warp，做 TMA 搬运；默认分区的 8 个 warp 只做
    epilogue（等屏障、`tmem_load`、通知、写回）。`matmul_kernel_tma` 为 98,352 变为 98,524、TMEM 128 列；`matmul_kernel_tma_persistent`
    为 131,120 变为 131,172，TMEM 在启用前后都是 256 列（`tmem_alloc` 为 `2x128x128xf32`，两个累加器）。sm_120（8 个 warp）：分区 0 为
    2 个 warp 做 TMA 搬运，默认分区做 `local_load`、`tt.dot` 与 epilogue；`matmul_kernel_tma` 为 65,552 变为 98,572，持久版为 98,320
    变为 131,196，输入缓冲由每个操作数 2 个槽变为 3 个；后者超过 12.x 的每线程块上限 101,376。据此更正节点 3 的一句话：
    “epilogue 与下一个 tile 的乘加重叠要靠 warp 专用化”只对同步的 `mma.sync` 成立，sm_100 上不启用时 TMEM 里也有两个累加器。
  - **分区的实现与 Hopper 的限制（2026-10-12）**：专用化后的 PTX 以 `.reqntid 384` 申请 12 个 warp，入口处由线程号右移 5 位得到 warp 号，
    小于 8 的跳到默认分区的代码，其余经 `brx.idx` 跳转表进入各分区，分区入口有 `setmaxnreg.inc.sync.aligned.u32 24`。Hopper 的 pass
    （`third_party/nvidia/hopper/lib/Transforms/WarpSpecialization.cpp` 第 41–56 行）在 warp 数不等于 4 时直接返回；函数内任何
    `scf.if` 带非空 else 块时也直接返回，注释为 `FIXME: skip warpspec if there is else block. Need to improve CodePartitioning to
    correctly handle channels in else block`；`WarpSpecialization/WSBuffer.cpp` 另有“目前只处理 channel 位于 then 区域的情形”。
  - **epilogue 拆半与预算（2026-10-12，`matmul_kernel_tma_persistent`，8 个 warp，只编译）**：共享内存等于输入槽加输出缓冲加屏障的
    几十字节，输出缓冲为一个输出块，拆半后为半个。sm_90、块 `128×256×64`：3 个 stage 为 213,016／180,248（不拆半／拆半），
    4 个 stage 为 262,176／229,408，上限 232,448，拆半才放得下。sm_120、块 `128×128×64`、上限 101,376：不启用专用化时 3 个 stage 为
    98,320／81,936，4 个 stage 为 131,096／114,712；启用专用化时 2 个 stage 为 98,372／81,988，3 个 stage 为 131,196／114,812。
    教程第 431–434 行的注释说明拆半的目的是省下 epilogue 占用的共享内存以增加 stage 数；`tl.split` 只能沿大小为 2 的最后一维拆分。
  - **拆半用于指针版（2026-10-12，探查副本，只编译）**：把教程第 435–442 行的拆半写法套到 `matmul_kernel_persistent`（B 为 `b.T`，
    块 `128×128×64`，8 个 warp）。`flatten` 开时共享内存在 sm_89 上由 98,304 变为 81,920（3 个 stage）、由 131,072 变为 114,688
    （4 个 stage），sm_90 上由 131,072 变为 114,688、由 163,840 变为 147,456；`flatten` 关时不变。另核对学习者在节点 6 检查题里的估算：
    sm_120 上 `matmul_kernel_tma_persistent`、4 个 stage，块 `64×64×64` 为 57,368（其估算 57,344 加屏障），块 `128×128×32` 为 81,944。
  - **非 NV 后端的退路（2026-10-12，AMD 后端 `gfx942`，只编译）**：教程的两个指针版 kernel 按 `bench()` 的调用方式编译，块 `128×128×64`、
    3 个 stage、8 个 warp。逐 tile 发射版、持久版（`flatten` 关）、持久版（`flatten` 开）的共享内存都是 65,536，输入缓冲都是每个操作数
    2 个槽；读入为 `amdg.buffer_load` 取进寄存器后以 `ttg.local_store` 写入共享内存，没有异步拷贝操作；乘加为 `v_mfma_f32_32x32x8_f16`
    48 条。`flatten` 开时 `scf.if` 由 2 处变为 8 处，说明循环合并生效（AMD 的 `make_ttgir` 同样调用 `add_fuse_nested_loops`，流水用自己的
    `add_schedule_loops` 与 `add_pipeline`），共享内存没有增加。未在 AMD 设备上运行。
- **教学更正（2026-10-11）**：节点 1 曾说“去掉对偏移量的两行声明，B 的读入退回逐元素的同步读”，并用每线程 162 个寄存器估算驻留数。
  这两个数字都来自 B 按行主序存放的编译结果；教程的 benchmark 传入的是 `b.T`，此时声明不改变读入方式，寄存器为每线程 135 个，
  “一个 SM 只驻留一个 CTA”的结论不变。已在回答学习者关于越界下标的提问时一并更正。
- **教学更正（2026-10-12）**：节点 3 曾说“内层的次数不能随外层变化，轮数必须是同一个值”，并把它作为检查题第 3 问的判对理由之一。
  按源码与补做的实验，这只在没有 `tl.assume` 时成立；已在评讲节点 3 时更正，图解页同步改写。学习者按当时所教作答，不记为差距。
- **教学更正（2026-10-12，节点 6）**：曾说“拆半只对描述符版有意义，指针版的写回不经过这块输出缓冲”，并据此出了检查题第 3 问。
  学习者质疑“指针版写回也需要通过共享内存”，补做实验后证实其质疑成立：指针版在 `flatten` 开时同样省半个输出块。两块缓冲的区别只在
  经过共享内存的原因（换布局与 TMA 只能从共享内存搬），图解页已改写。该问的前提有误，不记为学习者的差距。
- **教学更正（2026-10-14，Review R-05）**：曾把 `flatten` 开时没有流水的原因说成“K 循环里给循环前已有的名字重新赋值，它跨轮传递，流水因此算不出后面几轮的地址”。补做的私下变体（由参考实现改写，只编译，sm_89 与 sm_90）显示这个说法过宽：`offs_n` 在 K 循环里被重新赋值、跨轮传递，但写回另算下标时，`flatten` 开仍有提前量（循环内等待 `num = 2`）；只有写回也直接使用 K 循环结束后的这个值时，提前量才消失（`num` 全为 0），学习者第四版正是这种写法。流水 pass 为何因此放弃，仍未读源码确认。学习者据原说法作出的修改（K 循环内重新计算 `offset_n`，写回前另算一份）同时避开了这两点，结论不受影响。
- **教学更正（2026-10-14，M1 讨论）**：解释“逐 tile / 持久关”一列隔离了什么时，曾把“tile 循环本身的开销：每次都要算 tile 编号和坐标”列为持久化多出的一项。学习者指出逐 tile 版的每个 CTA 同样要算一次 tile 编号和坐标；逐 tile 版用的是同一个 kernel，tile 循环也照样执行一次，所以这两样按 tile 计在两种调度下相同，不是差别。已更正为三项真正的差别：硬件分派与回收的 CTA 数（4096 对 170）、每个 CTA 在 tile 循环之前的固定工作、tile 分到 SM 的方式（硬件按空闲动态分派，对固定步长的静态领取，影响负载均衡与同时在算哪些 tile）。不记为学习者的差距。

### 核心工件与参考

| 角色 | 路径或引用 | 说明 |
| --- | --- | --- |
| 来源或知识产物 | `docs/triton-tutorials/official/09-persistent-matmul.py` | 教程快照，不修改 |
| 练习产物 | `gpu/triton/lesson09_persistent_matmul.py` | 学习者拥有；首版（SHA-256 前缀 `cfdced17`）至第五版（`6d628fbc`）与 V1 版（`27b89b39`）均于 2026-10-14 提交，入库版为结课时整理格式后的 `e1af1841`，Review 结果见[需要跟踪的问题](#条件片段需要跟踪的问题) |
| 验证或工具 | `gpu/triton/lesson09_persistent_matmul_test.py` | 练习约定 P1 的验收测试（解释器层、只编译层、GPU 数值层），由 Agent 维护 |
| 验证或工具 | `gpu/triton/lesson09_persistent_matmul_benchmark.py` | M1 的测量脚本，由 Agent 维护，2026-10-14 交付 |
| 来源或知识产物 | [节点 3 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 三种写法在同一个 SM 上的时间线（可调 K 循环轮数与流水深度的示意模型）、循环合并后一次迭代里的两个 tile 与 `tile_id_c`、`flatten` 在共享内存上的代价与适用条件；2026-10-12 增补“查看产物”（三种取得途径、各文件回答什么、`flatten` 关与开的 TTGIR 骨架对照与原文、不用 GPU 的示例命令）与“迁移”（grouped GEMM 六种循环形状的编译结果）两节，以及节点 4 的“搬与算”一节（四种目标 × 两种写法的数据通路、八种组合的对照表、三条乘加指令的形状、sm_90 多一个输入槽的原因、B 按 `[N, K]` 存放的理由、两种描述符的比较），节点 5 的“专用化”一节（三种目标上各分区的 warp 数与循环内容、启用前后的资源对照、前提、分区在产物里的样子），节点 6 的“预算”一节（拆半前后的共享内存构成与六组对照）；2026-10-14 应学习者要求增补“声明”一节（存储连续与取值连续的区分、轴信息分析的三条性质与一次读入宽度的规则、`tl.where` 的规则、可切换 N 与两条声明的单 tile 演示、两条声明缺一不可的实测、边界 tile 里的承诺为何不出事、用法速查、整数参数的特化），并修正页脚长路径在手机宽度下撑出横向滚动的问题；可交互，离线可用 |

## 条件片段：练习约定

本节是练习 P1 的完整约定，实现时以它为准；验收测试是它的可执行形式。两者不一致时以本节为准，由 Agent 修测试。

- **编号与版本**：P1，版本 4。版本 1 由学习者接受于 2026-10-12（“就按照这个约定来吧。……我接受。”）；版本 2 只在包装函数上增加可选参数
  `out=None`（A2 的“输出之外的内存不被改写”必须由测试提供输出缓冲才能检查），学习者于同日确认（“好的，没问题。”）；版本 3 是约定澄清，
  A4 增加“读入提前发出”（原措辞只要求异步拷贝，未写明要有提前量，属约定的歧义，不归咎于学习者），学习者于 2026-10-14 接受（“我同意新的约定版本。”）；版本 4 增加无提示的小变式 V1（课程对“实践”证据的标准要求一个无提示的小变式，前几版约定漏写），学习者同日以直接着手 V1 表示接受。
- **为什么做**：O4 缺独立实践证据；O3 缺实测结果与学习者对结果的解释。

### 交付物

一个文件 `gpu/triton/lesson09_persistent_matmul.py`，含 kernel 与包装函数：

```python
matmul_persistent(a, b, *, out=None, num_sms=None, flatten=True,
                  block_m=128, block_n=128, block_k=64,
                  num_stages=3, num_warps=8) -> c
```

| 参数 | 含义与要求 |
| --- | --- |
| `a` | `[M, K]`，fp16，连续 |
| `b` | `[K, N]`，fp16，连续，按行主序存放（`a @ b` 的普通摆法，不是教程的 `b.T`） |
| `out` | 可选。`[M, N]`，fp16，与 `a` 同设备，列步长为 1；行步长可以大于 N，即可以是更大缓冲里的一个视图。给了就写入并原样返回它；不给则在 `a` 的设备上新建 |
| `num_sms` | 可选的正整数。不给时取 CUDA 设备的 SM 数；非 CUDA 设备上必须给。给了之后 CPU 上的张量也要能用（解释器层与只编译层依赖这一点） |
| `flatten` | 传给 tile 循环的 `tl.range(..., flatten=...)`，两种取值都要可用 |
| `block_m`、`block_n`、`block_k` | 块的大小。测试用到 `32×32×16`、`64×64×32` 与默认的 `128×128×64` |
| `num_stages`、`num_warps` | 原样传给 kernel 的发射 |
| 返回值 | `[M, N]` 的 fp16，位于输入所在的设备 |

对实现的要求：

- **调度**：只发射一次，网格为 `min(num_sms, tile 数)`，其中 tile 数为 `ceil(M / block_m) × ceil(N / block_n)`；每个 CTA 在 kernel 内循环领取 tile，
  每个 tile 恰好被计算一次。tile 的遍历顺序不作要求。
- **计算**：fp16 读入，fp32 累加，fp16 写回；每个 tile 的每一轮 K 调用一次 `tl.dot`。
- **边界**：M、N、K 不必是块大小的整数倍，也可以小于一个块；各维至少为 1，等于 0 的情形不在约定内。不得写到输出范围之外。
- **kernel 的形式**：模块级的 `@triton.jit` 函数，名字和参数自定。
- **错误输入**：下列情形抛 `ValueError`——`a` 或 `b` 不是二维；dtype 不是 fp16；`a` 的列数与 `b` 的行数不等；`a` 或 `b` 不连续；
  `out` 的形状不是 `[M, N]`、dtype 不是 fp16 或列步长不为 1；`a`、`b`、`out` 不在同一设备；`num_sms` 不是正整数；非 CUDA 设备上省略 `num_sms`。

### 验收项

| 编号 | 验收项 | 检查方式 |
| --- | --- | --- |
| A1 | 结果与 `torch.matmul` 一致，形状任意：整块、M／N／K 不整块、小于一个块、只有一个元素 | 测试；解释器层与 GPU 数值层 |
| A2 | 网格为 `min(num_sms, tile 数)`；`num_sms` 取 1、3、7、64 时结果都正确；每个 tile 恰好算一次；输出之外的内存不被改写 | 测试。恰好一次在解释器层按 `tl.dot` 的调用次数等于“tile 数 × K 的轮数”检查；网格在只编译层检查；内存用带保护区的 `out` 检查 |
| A3 | `flatten` 两种取值结果相同；开时循环合并生效（TTGIR 里 `scf.if` 增多，共享内存增多且不超过设备上限），关时不生效 | 测试；只编译，sm_89 与 sm_90 |
| A4 | N、K 整块且输入对齐时，`flatten` 两种取值下 A、B 都是 16 字节一组的异步拷贝，TTGIR 里没有同步的 fp16 读入；并且读入是提前发出的：两种取值下循环里的 `ttg.async_wait` 等待时仍允许有拷贝在途（`num` 大于 0），而不是每次拷贝后立即等它完成（版本 3） | 测试；只编译，sm_89 与 sm_90 |
| A5 | 包装函数以 `ValueError` 拒绝“交付物”一节列出的各类错误输入 | 测试 |
| A6 | 一段 3–5 句的说明：行主序的 B 在 `flatten` 下你是怎样保住异步拷贝的；epilogue 为什么要有自己的游标 | Agent 按要点评 |
| V1 | 无提示的小变式（版本 4）：K 方向去掉 `tl.where` 与连续性声明、只用 mask；先写预测（A 的读入在 `flatten` 关与开时是否仍为 16 字节、是否仍提前发出，理由），再跑只编译层验证并解释 | 预测与解释由 Agent 按要点评；只编译层测试 |
| M1 | 在 RTX 5090 上运行测量脚本并贴回输出；写 5–8 句，对照自己的预测解释结果，说明证据支持什么、不支持什么 | Agent 按要点评；预测不符不算失败 |

M1 的设置：块固定 `128×128×64`、3 个 stage、8 个 warp，`M = N = 8192`，K 取 128、512、2048。三个版本用学习者的同一个 kernel，只改调度：
每个 CTA 一个 tile（`num_sms` 等于 tile 数，相当于逐 tile 发射）；持久且 `flatten` 关；持久且 `flatten` 开。各版本短轮次交替运行，
脚本报出中位数与波动，并在运行前打印“支持、否定、证据不足”的判据。

### 怎样运行测试

都在仓库根目录执行，测试文件是 `gpu/triton/lesson09_persistent_matmul_test.py`。

| 层 | 命令 | 需要 GPU | 覆盖 |
| --- | --- | --- | --- |
| 解释器层 | `TRITON_INTERPRET=1 pytest -q gpu/triton/lesson09_persistent_matmul_test.py` | 否 | A1、A2（含恰好一次）、A3 的数值部分、A5 |
| 只编译层 | `pytest -q gpu/triton/lesson09_persistent_matmul_test.py`（没有 GPU 时数值项自动跳过） | 否 | A2 的网格、A3 的结构、A4 |
| GPU 数值层 | 同上一条，在 RTX 5090 上执行 | 是 | A1、A2、A3 的数值部分、A5，以及只编译层的各项 |

建议的顺序：先解释器层，再只编译层，最后到 GPU 上。

M1 的测量在 RTX 5090 上于仓库根目录执行 `python -m gpu.triton.lesson09_persistent_matmul_benchmark`（可加 `--rounds N`，默认 15 轮），把全部输出贴回。

### 测试没有检查的

- 读入时的越界访问（M、N 方向超出矩阵的下标）。它不影响数值，测试查不出来，但仍是未定义行为，应当像节点 1 讲的那样处理。
- 输入的 16 字节对齐。PyTorch 分配的张量本来就满足，不要求包装函数检查。
- 任何性能指标。性能只在 M1 里作为一次受控测量出现。

### 边界与门槛

- **文件边界**：你写 `gpu/triton/lesson09_persistent_matmul.py`；我维护 `gpu/triton/lesson09_persistent_matmul_test.py`、
  `gpu/triton/lesson09_persistent_matmul_benchmark.py` 与本记录；我只读教程快照与学习者的实现；本次不动第 08 课及更早的文件、其他课程的文件。
- **求助**：可以随时求助；透露了某个验收项的关键解法时，该项之后以新变式确认，其余不受影响。
- **非目标**：`GROUP_SIZE_M` 的分组顺序、autotune、fp8、描述符与 TMA、warp 专用化。
- **可选项（学习者 2026-10-12 说明本轮时间紧，不做，留给后续复习）**：可选一，在 RTX 5090 上运行教程脚本，观察描述符版与专用化版的实际数字；
  可选二，把第 08 课的 grouped GEMM 改造成能跨 tile 流水。
- **完成门槛**：A1–A6 与 M1 全部通过，阻塞问题全部关闭。

### 测试的建立（2026-10-12）

测试共 58 项。仓库内实现尚不存在时为 `1 failed, 57 skipped`（expected red，失败项是“实现文件存在”）。以一份不进仓库的参考实现核对：
解释器层 `46 passed, 12 skipped`，只编译层 `12 passed, 46 skipped`；六个故意写错的变体各被对应的测试报红（偏移放在 tile 开头、去掉写回的
mask、去掉 K 方向的 mask、步长为 1、忽略 `flatten`、网格不取 min）。GPU 数值层没有在本机运行过。测量脚本尚未建立，待 A1–A5 通过后交付。

2026-10-14 改了两处报错信息，判定不变：恰好一次的检查先比较 `tl.dot` 的调用次数、再比较数值，使数值错误不再掩盖计数错误；
A4 的失败信息列出仍为同步读入的值名（TTGIR 以赋值的变量名命名）。改后参考实现的结果不变，六个变体仍各被报红。

2026-10-14 按版本 3 增加“读入提前发出”一项（sm_89、sm_90 × `flatten` 两种取值，共 4 项，测试总数 62）：循环里至少有一处 `ttg.async_wait` 的 `num` 大于 0。参考实现通过；学习者第四版（`48b15b99`）在 `flatten` 开的两项失败；新增第七个故意写错的变体（`offs_n` 在 K 循环里跨轮传递，写回也用它）同样在这两项报红，原有六个变体的结果不变。

测量脚本 `gpu/triton/lesson09_persistent_matmul_benchmark.py` 于 2026-10-14 交付：三种调度（`num_sms` 等于 tile 数且 `flatten` 关；每 SM 一个 CTA、`flatten` 关；每 SM 一个 CTA、`flatten` 开）用同一份输入与学习者的同一个 kernel；15 轮，每轮按轮换的顺序把每个 K 下的三个版本各测一次，每次是 `triton.testing.do_bench` 的一小段（预热 5 ms、重复 20 ms、每次运行前清空 L2）取中位数；比值在同一轮内相除后取各轮的中位数与四分位区间。运行前打印判据：主判据 S(K) = 逐 tile 时间 / 持久（`flatten` 开）时间，中位数随 K 依次下降且 S(128) 与 S(2048) 的四分位区间不重叠为支持；S(2048) 不小于 S(128) 且两端区间不重叠，或两端区间重叠且宽度都小于 0.03 为否定；其余为证据不足；`flatten` 关的比值按同样判据列为辅助。测量前逐项核对结果（最大相对误差不超过 1e-2）并列出各版本的共享内存、寄存器与溢出。本机无 GPU，只以解释器、小尺寸与合成计时做过冒烟运行，判据的五种情形核对无误。

## 条件片段：帮助影响

| 透露到什么程度 | 影响的验收项或工件 | Agent 是否写了学习者核心工件 |
| --- | --- | --- |
| 2026-10-14：首次 Review，学习者说明测试有结果错误并请求 Review。给出了：细化的失败证据（失败的形状全部是 K 不是 `block_k` 整数倍的；M=N=K=1、a=2、b=3 时输出 96；编译报错原文与位置；TTGIR 里仍为同步读入的两个值名；手写循环多领 tile 的计数）；K 方向的不变量（k ≥ K 的位置对和的贡献必须为 0）；约定中 `flatten` 的写法；节点 1 五种越界写法的编译对照（指向来源）；编译报错的语义（Triton 里只在 `if` 内首次赋值的名字在 `if` 之后不存在）。没有指出 R-01、R-03 的出错语句，没有给改法或代码。 | 不影响独立证据：R-01、R-03 只协助到定位的范围；R-02 的改法就是约定本身。同日学习者自行说出 R-01 的机制（先 `tl.where` 后算 mask，mask 恒为真），独立证据成立。随后学习者指出同源的另一处在 M、N 方向的写回，位置对，但把后果说成“写到 C 外面”，与保护区检查的结果不符；已给出保护区检查结果与写回落点的计数（partial-m 时第 0 行每个元素写 27 次，partial-n 时第 0 列写 15 次），并提示读入与写回用的是同一个下标变量。学习者随即正确解释了落点（越界的下标改成 0 后写回第 0 行，27 = 1 + 26，26 = 32×3−70）与数值为何仍对（越界的行读的是 A 的第 0 行，算出的正是第 0 行的值）；已补充：各 CTA 写入的先后不确定，结果正确只因为每次写入的值相同。R-01 的理解证据成立，修复待测试确认 | 否 |
| 2026-10-14（追问）：学习者问 `flatten` 是否只需在外层循环上请求、不必手写合并循环。确认合并由编译器完成，并说明在其 kernel 上的做法（给 tile 循环加 `flatten=flatten`、删去手写分支，属约定内容）；重述节点 3 的两点：合并是请求，须看产物确认；v3.7.1 上行主序 B 有一个已知边界（指向节点 3 页面“代价”一节）。没有给出该边界的处理办法。 | A4（`flatten` 开）与 A6：只指向来源，不影响独立证据 | 否 |
| 2026-10-14（第二版）：学习者给 `offset_m`、`offset_k` 加了连续性声明，问为什么仍有同步读入。给出：现在只剩 B 的读入是同步的（值名），A 已是异步拷贝；以提问引导“声明要落在哪个操作数的哪个方向上”；再次指向节点 3 页面的 v3.7.1 边界。没有指出要改的下标，没有给代码。 | A4、A6：只协助到定位与来源指向，不影响独立证据 | 否 |
| 2026-10-14（第三版）：`flatten` 开时 B 仍为同步读入。给出：A3 的共享内存失败与 B 同源的证据（`cp.async` 条数与共享内存对照）；引述节点 3 页面对该边界原因的说明；以提问引导学习者对照自己手写过的合并循环找出哪些值会成为 `scf.if` 的输出。没有指出要改的语句，没有给代码。 | A3、A4、A6：来源引述与提问，不影响独立证据 | 否 |
| 2026-10-14（追问）：学习者问原因是否是合并引入的 `if` 对 K 循环头尾做特殊处理，以及 A 为什么不受影响。纠正：合并后的 `if` 包住的是 tile 的 prologue 与 epilogue（原先位于 K 循环之外的代码），不是 K 循环的头尾；说明从 `if` 里出来的值会丢掉连续性声明、流水只检查操作数连续方向上的连续性；以提问请学习者对照 A、B 各自连续方向的下标在哪里计算。没有指出要改的语句，没有给代码。 | A4、A6：讲解机制与提问，结论留给学习者，不影响独立证据 | 否 |
| 2026-10-14（追问）：学习者自行答出 A 的 `offset_k` 在 K 循环里算、B 的 `offset_n` 在 `if` 里算，并只把声明挪进 K 循环，结果不变。用私下副本证实只挪声明时 TTGIR 逐字相同，并解释声明的语义：`tl.max_contiguous`、`tl.multiple_of` 不产生新值，而是把属性附在定义该值的操作上（`semantic.py` 第 1824 行；TTGIR 中属性在 prologue 的 `arith.select` 上），所以要挪的是值的计算。改法方向由学习者得出，Agent 补的是声明的语义。 | A4、A6：概念澄清，改法方向由学习者得出，不影响独立证据 | 否 |
| 2026-10-14（M1 与 A6 首答之后）：M1 首答只复述了判据的结论（“比值随 K 下降，支持预测，没什么不支持的”），A6 首答说明了把 `offset_n` 的计算移进 K 循环并声明连续，把 epilogue 需要自己的游标归因于 `offset_n` 的作用域。给出：M1 应覆盖的三点（支持什么、不支持什么、剩余的不确定）与三个引导问题（哪一列只隔离了持久化本身；K=2048 时比值低于 1 说明什么；这次测量回答不了什么）；A6 指出作用域只解释了为何重算 `offset_n`，并指向教程第 305–306、538–539 行的注释、图解页的交接表与学习者自己第四版的现象，另指出其写回仍使用 tile 开头算出的 `tid_n` 与 `offset_m`，并没有独立的游标。没有给出解释本身。 | M1、A6：引导问题与来源指向，解释仍由学习者给出 | 否 |

## 条件片段：需要跟踪的问题

| ID | 对应验收项或目标 | 严重度 | 状态 | 证据 |
| --- | --- | --- | --- | --- |
| R-01 | A1、A2 | 阻塞 | 已关闭 | 2026-10-14 首次 Review（本机解释器层，Triton 3.7.1，实现文件 SHA-256 前缀 `cfdced17`）：27 项失败，失败的形状全部是 K 不是 `block_k` 整数倍的（partial-k、partial-all、smaller-than-a-block、one-element、wide、25 个 tile 的 150×130×40 与默认块的 300×260×150）；M、N 不整块而 K 整块的两项通过。M=N=K=1、a=2、b=3 时两种 `flatten` 下都输出 96。另有一处同源问题测试查不出，已请学习者自查。关闭证据（2026-10-14，第二版 `8baef278`，本机解释器层）：mask 改在 `tl.where` 之前计算，`46 passed, 12 skipped`；M=N=K=1 输出 6；写回落点统计中 partial-m、partial-n 都没有重复写入。GPU 数值层（2026-10-14，RTX 5090，AutoDL 容器，Triton 3.7.1，第三版 `fa0fe29e`）：A1、A2、A5 的数值与参数各项全部通过（`4 failed, 46 passed, 8 skipped`，失败的 4 项均属 R-03）。 |
| R-02 | A3；约定中“`flatten` 传给 tile 循环的 `tl.range`” | 阻塞 | 已关闭 | `flatten` 开的分支是手写的合并循环。只编译层有 8 项在编译时失败：`NameError('offset_m is not defined')`（第 53 行，`offset_m` 只在 `if` 内首次赋值）；解释器按 Python 执行，不报。手写循环每个 CTA 领取的 tile 数在整除时多一个：25 个 tile 时 `tl.dot` 为 78 次（应为 75）；256×256×128、块 64 时为 68 次（应为 64），并出现除以 0 的警告（多出的 tile 编号等于 tile 总数，M 方向 tile 数为 4 的倍数时 `get_tid` 的组内行数为 0，在 GPU 上是未定义行为）。关闭证据（2026-10-14，第二版 `8baef278`）：改为 `tl.range(..., flatten=flatten)` 的两层循环，删去手写分支；只编译层的合并两项与网格四项在 sm_89、sm_90 上通过，解释器层 `flatten` 开时四种 `num_sms` 都是 75 次 `tl.dot`。 |
| R-03 | A4；A3 的共享内存一项 | 阻塞 | 已关闭 | `flatten` 关时 sm_89 与 sm_90 上 A、B 的读入都是同步的 `tt.load`（值名 `%a_data_67`、`%b_data_70`，源码第 89、94 行），PTX 里没有 `cp.async`，共享内存只有 8,192 字节。第二版（`8baef278`）：K 方向下标加了连续性声明后 A 成为 16 字节异步拷贝；B 在 `flatten` 关与开时仍是同步读入（`%b_data_*`），只编译层 A4 四项失败。第三版（`fa0fe29e`，N 方向下标加了声明，仍在 tile 开头计算）：`flatten` 关时 A、B 都是 16 字节异步拷贝（12 条）；`flatten` 开时合并生效（`scf.if` 0 → 4），但 B 退回同步读入（`cp.async` 只剩 A 的 6 条），共享内存不增反减（sm_89 16,384 对 16,384，sm_90 20,480 对 24,576），A3 的共享内存一项因此在 sm_89、sm_90 上失败，与 A4 同源。学习者在 RTX 5090 上运行同一文件（哈希一致）为 `4 failed, 46 passed, 8 skipped`，失败的正是这 4 项。关闭证据（按现行测试）：第四版（`48b15b99`）把 N 方向的 `tl.where` 与声明移入 K 循环，RTX 5090 上 `50 passed, 8 skipped`，本机解释器层 `46 passed, 12 skipped`、只编译层 `12 passed, 46 skipped`。该版在 `flatten` 开时的流水问题另记为 R-05。 |
| R-04 | A5 | 非阻塞 | 已关闭 | 测试未覆盖的两处：`num_sms` 为非数值（如字符串）时先做 `<= 0` 比较而抛 `TypeError`，约定要求 `ValueError`；缺省 `num_sms` 读的是当前 CUDA 设备而不是 `a` 所在的设备（单卡上结果相同）。关闭证据：第四版先检查类型再比较大小，缺省值改为读 `a` 所在设备。 |
| R-05 | A4（版本 3）；M1 | 阻塞 | 已关闭 | 2026-10-14 Review 第四版时发现、现行测试的缺口（Agent 的验收测试没有检查读入是否提前发出）：`flatten` 开时 sm_89、sm_90 上合并循环没有流水，循环前没有预先发出的拷贝，每次 `ttg.async_copy_global_to_local` 之后立即 `ttg.async_wait {num = 0}`（拷贝 2 处，等待 3 处且 `num` 全为 0）；`flatten` 关时正常（拷贝 6 处，循环内等待 `num = 2`）。共享内存增多是因为输入缓冲不再与 epilogue 的中转缓冲共用空间，所以 A3 的检查也通过了。私下副本：K 循环内不给循环前已有的 `offset_n` 重新赋值、改用新名字后，`flatten` 开也是 6 处拷贝、`num = 2`，解释器层全部通过。已向学习者提出约定澄清（A4 增加“两种取值下读入都提前发出”），学习者接受。原因的说明后经更正，见“教学更正（2026-10-14）”。关闭证据（2026-10-14，第五版 `6d628fbc`：`offset_n`、`mask_n` 在 K 循环内由 `tid_n` 重新计算，写回前另算一份）：本机只编译层 `16 passed, 46 skipped`（含新增 4 项），解释器层 `46 passed, 16 skipped`；学习者报告该版在 RTX 5090 上以原测试文件全部通过；以新测试文件（`ecffbf59`）在 RTX 5090 上 `54 passed, 8 skipped`（跳过的是只在解释器层运行的恰好一次检查）。 |

## 条件片段：阶段事件

| 日期 | 覆盖范围 | 证明了什么 | 证据链接 | 标注 |
| --- | --- | --- | --- | --- |
| 2026-10-10 至 2026-10-11 | E-01：开课导入、节点 1–2 与检查 | 节点 1–2 的检查题共三问。第 2 问（矩阵缩小到 tile 数少于 SM 数）正确给出 64 个 CTA、各处理一个 tile，并指出剩下的差别只是指针重算与递推的写法。第 3 问（诊断与设计）一次答对：网格改为 `4 × NUM_SMS` 而步长仍是 `NUM_SMS` 时结果正确但重复计算，编号 1000 的 tile 由 104、232、360、488 号 CTA 各算一次；修法是让步长等于发射的 CTA 数，并指出第 02 课用 `tl.num_programs(0)` 取步长（已核对教程 02 第 89 行与学习者第 02 课的实现；改用该写法的探查副本在 sm_89 与 sm_90 上读入方式、共享内存与寄存器不变）。第 1 问的 tile 数与 K 循环次数正确；“哪一端更明显”被理解成 tile 三段中的哪一段，属题目措辞歧义，不记为学习者的差距，已换题复查。其回答指出持久化使前后两个 tile 的 epilogue 与 prologue 位于同一段代码、因而有了重叠的可能，没有说到发射成本每个 SM 只付一次这一直接收益，已补讲。作答前的四次追问（多个 CTA 驻留时固定成本怎样被掩盖；张量核心是否被多个 CTA 竞争；M、N 方向的越界下标为什么要在读取时处理；越界访问的后果）都指向机制与设计理由；第三个追问促使补做了 B 的两种传法与五种越界处理写法的编译对照，并更正了节点 1 的两个数字。换题复查（两问）通过：正确判断 K=128 时持久化的提速比例更大，理由是 K 循环变短而 tile 之间的固定间隔不变；正确判断 M=N=8192 比 2048 收益更大，并自行从“间隔的绝对数量”改为比较比例（每个 CTA 32 个 tile 有 31 个间隔，2 个 tile 只有 1 个）。仍有一处用词不精确：把持久化本身的收益说成优化 prologue 与 epilogue，而它直接省掉的是间隔里的发射与退出，已用“间隔里的四样东西各由谁消掉”的对照表澄清。随后讲解节点 3（`flatten` 与跨 tile 的流水），配图解页，并发出节点 3 的检查题。 | 本会话；[当前证据](#当前证据)；[节点 3 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 无 |
| 2026-10-12 | E-02：节点 3 检查与两个追问 | 节点 3 检查题三问。第 1 问（怎样确认 `flatten` 生效）：正确指出共享内存会增加，以及“没有报错”不算证据、条件不满足时编译器会回退到普通循环；另一样证据说成“prologue 和 epilogue 的数量显著减少”，把流水的预热与排空（由每个 tile 一次变为每个 CTA 一次）和 tile 自己的 prologue、epilogue（仍是每个 tile 一次）混在一起，是节点 1 起反复出现的用词问题，已用对照表与真实产物里的位置补讲。学习者同时说明自己只会运行 Triton 代码、不会查看编译产物；题目预设了本课没有教过的操作，属出题前提的缺口，不记为学习者的差距。第 2 问 (a)：共享内存算得 131,072 正确；后果答成“溢出到显存、性能更慢”，是误解，已补讲超限时 kernel 在加载前即抛 `OutOfResources`、autotune 下被静默跳过，并与寄存器溢出对照。(b)：两种办法（减小块、关闭 `flatten`）及其代价正确。第 3 问：两条理由（K 循环次数随问题变化；中间是 `while`，不是简单嵌套）正确。两个追问：能否把 grouped GEMM 改造成可以跨 tile 流水（指出 MoE 的 K 相同，问 `while` 能否改成 `for`），是自发的迁移与设计问题；怎样查看编译产物及其中的 prologue、epilogue 与共享内存。为此重读循环合并 pass 并补做六种循环形状的只编译实验，更正了自己关于“内层次数不能随外层变化”的说法；增补图解页“查看产物”“迁移”两节；发出复查两问（读第 08 课 kernel 的真实骨架，判断预热、排空与 epilogue 各自的执行次数及合并后的变化；autotune 中 5 个 stage 的配置“没有收益”的推断错在哪里、怎样确认）。 | 本会话；[当前证据](#当前证据)；[节点 3 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 无 |
| 2026-10-12 | E-03：节点 3 复查，节点 4 讲解 | 节点 3 的复查两问通过。第 1 问：正确判断在一个领到 20 个 tile 的 CTA 里预热、排空与 epilogue 各执行 20 次，合并生效后预热与排空各 1 次、epilogue 仍是 20 次，并概括为“省掉 tile 间隔里的预热和排空，省不掉写回”；此前把二者混称的问题不再出现。第 2 问：指出 5 个 stage 的配置因共享内存不足报错、被 autotune 吞掉、实际没有运行，算出 163,840 与 131,072；确认办法答“看该配置的耗时是否记成无穷大”，方向正确（对应 `Autotuner.configs_timings` 与 `TRITON_PRINT_AUTOTUNING`，已补充具体入口）。学习者指出题目里的“本例”没有说明是哪个例子，属出题措辞的问题，不记为差距；这是“举例先交代场景”的偏好第二次被触及。随后讲解节点 4（搬运与计算在 sm_89、sm_90、sm_100、sm_120 上的分工，主机侧与设备侧描述符及各自的退路），增补图解页“搬与算”一节，发出检查题三问。 | 本会话；[当前证据](#当前证据)；[节点 3–4 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 无 |
| 2026-10-12 | E-04：节点 4 检查与两个追问 | 节点 4 检查题三问。第 1 问（在 sm_89 上强行使用主机侧描述符）：正确指出读入由 `cp.async` 退为逐元素同步读，原因是描述符被展开成运行时参数、地址没有连续与对齐保证，并指出设备侧描述符的 `matmul_kernel_descriptor_persistent` 退路更好。第 2 问：设备侧的适用场景（发射时还不确定的张量，如 grouped GEMM 各问题的矩阵）与多付的代价（`tensormap.replace` 与每个描述符 128 字节的全局暂存）正确；主机侧的场景答成“进行 autotune 时比较方便”，方向相反，主机侧描述符在 autotune 下正是因为块形状要逐配置改写才需要 `pre_hook`，已补讲。第 3 问 (a)：正确指出 sm_120 多出的寄存器装的是乘加的输入数据；(b)：自述不清楚，猜测为“指令更大，需要准备的输入和输出空间更多”，未理解槽数取决于槽被占用的时长（就地、异步读），已用 sm_89 与 sm_90 一轮内的步骤对照补讲。两个追问：要求把指令粒度讲细（`m16n8k16` 是否即 M=16、N=8）；并主动给出 B 按 `[N, K]` 存放的两点理由，经 PTX 文档与 fp8 编译对照核实成立，更正了我此前“不下结论”的说法。图解页增补三块内容。发出复查两问（主机侧描述符在 autotune 下为什么需要钩子而设备侧不需要；预测 sm_120 描述符版的输入槽数并用共享内存验证）。 | 本会话；[当前证据](#当前证据)；[节点 3–4 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 无 |
| 2026-10-12 | E-05：节点 4 复查，节点 5 讲解 | 节点 4 的复查两问通过。第 1 问：说明主机侧描述符在创建时块大小尚未确定、要靠钩子逐配置改写，设备侧在 kernel 内构造时块大小已是编译期参数，并得出设备侧与 autotune 配合更省事，此前说反的判断已改正；“需要运行到 kernel 时才知道块大小”一语不够准确（钩子在每组配置发射前运行），已指出。第 2 问：正确预测 sm_120 描述符版每个操作数 2 个槽，理由是操作数取进寄存器后槽即空出，并以 4×16,384+16=65,552 验证；概括为槽数由 `num_stages` 与乘加指令能否直接读共享内存共同决定，与 TMA 无关。学习者另自行指出这就是 sm_89 只需 S−1 个槽的原因，并复述了 B 按 `[N, K]` 存放的两点理由（fp8 一条说成“必须”，已补充：指令层面必须，Triton 仍能编译但要经寄存器重排）。随后讲解节点 5（warp 专用化的分区、屏障交接、三种目标上的差别、资源代价与前提），增补图解页“专用化”一节，发出检查题三问。 | 本会话；[当前证据](#当前证据)；[节点 3–5 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 无 |
| 2026-10-12 | E-06：节点 5 检查与两个追问，节点 6 讲解 | 节点 5 检查题三问。第 1 问：用三条乘加指令由谁执行的区别正确解释了 8、4+4、1 三个数（第三处把 sm_100 误写成 sm_120，属笔误）。第 2 问：指出 131,196 超过 101,376、该配置的耗时记为无穷大而落选，差的部分是两个操作数各多出的一个缓冲槽，且不会看到报错，三小问都对。第 3 问 (a)：正确区分 `flatten`（在软件层面把流水做长到跨 tile）与专用化（分出 warp 专做预取）；(b) 没有回答“为什么不损失跨 tile 的预取”，转而追问为什么带 else 的 `scf.if` 就不能专用化、是否因为 warp 会分化，已依据源码说明这是该版本 Hopper 实现的一处未完成（FIXME），并讲明合并后的循环为什么必然带 else；(b) 并入节点 6 检查题的第 1 问复查。另一个追问：warp 的“分区”是什么概念——该词使用前没有定义，属讲解的缺口，已用 C 的写法与真实 PTX 的跳转补上，这是“名词渐进引入”的偏好在本课第一次被触及。随后讲解节点 6（epilogue 拆半与共享内存预算），增补图解页，发出检查题三问。 | 本会话；[当前证据](#当前证据)；[节点 3–6 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 无 |
| 2026-10-12 | E-07：节点 6 检查与根因讨论，节点 7 讲解 | 节点 6 检查题。第 1 问（复查节点 5）：答对搬运分区的循环里只有等空槽与发读入，但把不合并时 tile 边界的停顿归因于 prologue 的地址计算；经三轮追问（生产者是一重还是两重循环；根因是不是不用排空；二者是否分别像异步与并行），学习者自行概括出“`flatten` 调整一条顺序里的先后，专用化增加执行顺序的条数”，并提出“前者像异步、后者像并行”的类比，判断成立。换过的补充题（sm_120 启用专用化后 tile 边界上哪些事能重叠）答对：读入可与上一个 tile 的 epilogue 同时进行，乘加不能，理由是乘加与 epilogue 在同一批 warp 上。第 2 问：算出拆半后 114,712 仍超上限 13,336，换不来第 4 个 stage；替代办法给出把块缩到 64×64×64，估算 57,344 加屏障（编译结果 57,368），代价是 tile 变多、间隔变多，正确。第 3 问：判断两块缓冲不是同一样东西，并质疑“拆半对指针版没有意义”的说法；实验证实质疑成立，属我的讲解错误，已更正。另一个追问（TMA 能否直接从 TMEM 搬到显存）已依据 PTX 文档与产物答复。随后讲解节点 7（TFLOPS 的口径、launch metadata、proton、基线、教程 bench 的混杂因素），发出检查题三问，其中第 3 问是 O3 的预测。 | 本会话；[当前证据](#当前证据)；[节点 3–6 图解页](../attachments/09-persistent-matmul/persistent-matmul-timeline.html) | 无 |
| 2026-10-12 | E-08：节点 7 检查，进入串讲与综合验收 | 节点 7 检查题三问通过。第 1 问：`tflop16/s` 由运算数与 kernel 执行时间得到，前者来自 launch metadata，后者由 proton 经 CUPTI 取得；未配 launch metadata 时只剩执行时间。第 2 问：指出两个 kernel 各自 autotune、所选配置可能不同，以及持久版同时带有 `flatten`，改法是固定块等配置或关闭 autotune，并保证两份代码只差持久化；未提到顺序测量带来的漂移，属“至少两个”之外。第 3 问：作出 O3 的预测与可证伪条件（见上）。学习者贴回 RTX 5090 的设备读数。随后给出导师串讲并发出综合验收三问（在 5090 上为贯穿案例选一个教程 kernel 并口述其数据流与取舍；解释寄存器减少与共享内存增加为何是同一件事的两面；把持久版迁到没有 `cp.async` 与 TMA 的非 NV 后端时哪些收益还在、先验证什么）。 | 本会话；[目标与所需证据](#目标与所需证据) | 无 |
| 2026-10-12 | E-09：综合验收首答 | 第 1 问（口述）：学习者指出题目没有给出“按什么标准选”，无法作答；属题目措辞缺口，不记为差距，已补上标准重新发出。另有一个追问（`tflop16/s` 的“三样东西”还差哪一样）：题目计数不当，实质只有两样，已说明第三样指作为汇总键的名字。第 2 问：指出乘加直接读共享内存省去了搬到寄存器这一步，并说明上限较低的设备因此受共享内存制约；但把共享内存的增加解释为“增加槽位以便让更多数据提前搬”，与同一 `num_stages` 下提前量不变的事实不符，是节点 4 已答对内容的回退，已补讲并换题复查。第 3 问 (a)：正确区分持久化不依赖硬件特性、`flatten` 的收益依赖读入能否在后台进行、TMA 与 TMEM 及专用化依赖硬件；已用 AMD 后端的编译结果补充一个实例。(b)：第二样（看是否提前读取下一个 tile 的数据）正确；第一样说成“看发射动作是否从 tile 循环中提出来”，把由源码与包装函数决定的持久化当成了编译产物里的变换，已纠正并换题复查。 | 本会话；[当前证据](#当前证据) | 无 |
| 2026-10-12 | E-10：综合验收复查与口述 | 复查第 2 问：正确指出两种目标提前量相同，sm_90 的操作数留在共享内存、sm_120 的操作数进寄存器，因此一个槽多、一个寄存器多；并追问“硬件升级只是为了让数据换个地方放吗”，提出寄存器更稀缺的猜测，已依据 CUTLASS 文档与编译结果补充（寄存器按线程私有且有上限、线程要逐条指令喂张量核心、数据在谁的寄存器里计算就绑在谁身上）。复查第 3 问：正确指出持久化由手写代码完成，在 TTGIR 里表现为 tile 循环。第 1 问（口述，按“预计最快且装得上”在 RTX 5090 上选 kernel）：选 `matmul_kernel_tma_persistent`，理由是持久化、`flatten` 与 TMA 同时启用；数据流讲对了该设备上的关键差别（TMA 搬进共享内存后操作数仍取进寄存器、用 `mma.sync` 计算，结果经共享内存由 TMA 写回），并说明 `flatten` 让下一个 tile 的读入在 epilogue 之前发出；与最接近的 `matmul_kernel_descriptor_persistent` 的取舍（形状固定时主机侧描述符足够，省去设备侧构建描述符的指令）正确。不足三处：数据流没有从发射与按步长领取 tile 讲起（该内容在节点 1–2 已有充分证据）；没有说出最没把握、需实测确定的一点；“拆半以增加输入槽”在该设备与该块上不成立，与其在节点 6 的计算不一致。判定综合验收通过，三处已在评语中补齐。按证据分流：O1、O2 证据充分；O3 缺实测，O4 缺独立实践，提出练习约定 P1（版本 1）。 | 本会话；[目标与所需证据](#目标与所需证据) | 无 |
| 2026-10-12 | E-11：练习约定与验收测试 | 学习者接受练习约定 P1（版本 1），并要求把两个可选项记录下来、本轮不做。建立验收测试并确认 expected red；因 A2 需要由测试提供输出缓冲，提出版本 2（只增加 `out=None`），学习者同日确认；应其要求把约定的全部细节整理进练习约定一节。 | [练习约定](#条件片段练习约定)；`gpu/triton/lesson09_persistent_matmul_test.py` | 无 |
| 2026-10-14 | E-12：练习首版与首次 Review | 学习者提交首版实现并说明测试有结果错误、请求 Review。本机解释器层 `27 failed, 19 passed, 12 skipped`，只编译层 `10 failed, 2 passed, 46 skipped`，形成阻塞问题 R-01–R-03 与非阻塞观察 R-04。已经成立的部分：包装函数的参数检查（A5 九项）、网格取 `min(num_sms, tile 数)` 且步长等于发射的 CTA 数、`flatten` 关时每个 tile 恰好一次（四种 `num_sms` 下都是 75 次 `tl.dot`）、分组顺序为双射；手写的合并循环在结构上与编译器合并后的循环一致（k 为 0 时进入新 tile、最后一轮写回）。`num_stages` 只写在 K 循环的 `tl.range` 上，经核对合并前后流水深度都随它变化，与作为发射参数传入等效。帮助限于失败证据、不变量、约定与来源指向；测试改了两处报错信息，判定不变。学习者随后说出 R-01 的机制与写回处的同源问题（越界行改成 0 后重复写回第 0 行，27 = 1 + 26，值相同所以结果碰巧正确），同日提交第二版，关闭 R-01、R-02，R-03 只剩 B；第四版在 RTX 5090 上通过现行全部测试，关闭 R-03、R-04，但 Review 发现 `flatten` 开时合并循环没有流水（现行测试的缺口），记为 R-05 并提出约定澄清。学习者接受版本 3，并说出原因（K 循环里改写了 `offset_n`，使它不再是 tile 内不变的值）；第五版关闭 R-05。Agent 补测试并交付测量脚本。学习者在 RTX 5090 上通过全部 62 项中的 54 项（其余 8 项只在解释器层运行）并完成 M1 测量；M1 的解释与 A6 的说明各经一轮反馈后通过；学习者说明预测中的“持久版”指不带 `flatten` 的版本，按原意评判，结论不变；约定升到版本 4 并完成 V1。结课前答疑（`tl.where` 为何破坏连续性、越界置 0 后是否还连续、两个声明函数的用法）中，“连续”一词同时指张量的存储连续（约定里 `a`、`b` 的连续）与下标取值连续（轴信息分析的连续度），讲解时没有区分，学习者因此以为“新构建的张量总该是连续的”；已区分两种含义，属讲解的缺口，不记为学习者的差距，是“名词渐进引入”的偏好在本课第二次被触及。 | [需要跟踪的问题](#条件片段需要跟踪的问题)；[帮助影响](#条件片段帮助影响)；[结课](#条件片段结课) | 结课 |

## 条件片段：结课

| 目标 | 所需证据 | 证据链接 | 判断 |
| --- | --- | --- | --- |
| O1：持久化矩阵乘的数据流与调度、`flatten` 跨 tile 流水及其代价 | 理解 | E-01 至 E-03 的节点 1–3 检查与复查；E-08 至 E-10 的导师串讲与综合验收 | 充分 |
| O2：搬运与计算在各代硬件上的分工、描述符、warp 专用化、epilogue 拆半与退路 | 理解 | E-03 至 E-07 的节点 4–6 检查与复查；E-09、E-10 的综合验收第 2、3 问 | 充分 |
| O3：度量与解释矩阵乘 kernel 的性能 | 理解、实证 | E-07、E-08 的节点 7 检查与 2026-10-12 的可证伪预测；[M1 的测量结果与解释](#目标与所需证据)：RTX 5090 上受控测量，判据事先打印，判定为支持；解释的第二稿说明了支持什么、不支持什么与剩余的不确定 | 充分 |
| O4：实现并验证持久化矩阵乘 kernel 与包装函数 | 理解、实践 | [练习约定 P1](#条件片段练习约定) 版本 4 的 A1–A6 与 V1；E-12：RTX 5090 上 `54 passed, 8 skipped`，本机解释器层 `46 passed, 16 skipped`、只编译层 `16 passed, 46 skipped`；R-01 至 R-05 关闭；A6 经一轮反馈通过；V1 无提示完成 | 充分 |

- **未关闭的阻塞问题**：0。R-01 至 R-05 均已关闭，非阻塞的 R-04 也已修好，见[需要跟踪的问题](#条件片段需要跟踪的问题)。
- **帮助影响是否已恢复**：不需要恢复。各次帮助限于失败证据、不变量、来源指向、约定重述与概念澄清，Agent 没有写学习者的核心工件；
  R-01 的机制、R-03 与 R-05 的改法方向由学习者得出；A6 第二点中“独立游标为什么不是正确性所必需”这一半由 Agent 补充，A6 按学习者
  给出的要点判定；V1 无提示完成。见[帮助影响](#条件片段帮助影响)。
- **非阻塞余项**：K=2048 时 `flatten` 的净代价与寄存器变少的原因没有验证（假设是合并后每轮都要做的判断）；“持久化本身”一列中
  CTA 分派、每个 CTA 的固定工作与调度方式三项变化无法由这次测量拆开；M1 只在一台 RTX 5090、一组块配置上测量；实现里 M、N 方向
  的 `tl.where` 已有 mask 兜底，属可删的冗余；教程的描述符版与 warp 专用化版没有实机运行（可选一），grouped GEMM 的跨 tile 流水
  改造（可选二）按学习者意愿留到复习时做；验收测试先后补过两处缺口（计数被数值失败掩盖；“读入提前发出”由版本 3 补入）。以上都
  不在本课门槛内。
- **学习者确认**：2026-10-14，学习者回复“好的。接下来我们结课吧。”
- **入库版本的整理**：实现文件原有 6 条 Ruff 提示且未格式化，仓库的 CI 会检查。结课时按学习者要求（“lint处理好后提交吧”），由 Agent
  做了不改逻辑的整理：Ruff 的自动修复（import 排序、行尾空白）、格式化、注释掉的旧代码里一行过长的调用折行、注释里一个全角逗号。
  整理前后整个模块的 AST 相同；sm_89 与 sm_90 上 `flatten` 两种取值的 PTX 指令流相同。整理后的文件（`e1af1841`）在本机解释器层
  `46 passed, 16 skipped`、只编译层 `16 passed, 46 skipped`。GPU 层没有复跑：RTX 5090 上的数值验收与测量对应第五版 `6d628fbc`，
  V1 版 `27b89b39` 只注释掉 K 方向的两行，与入库版的 AST 相同，只在本机两层复验过。
- **结课结论**：学习者能讲清持久化矩阵乘的调度（每个 SM 一个 CTA、以发射的 CTA 数为步长领取 tile、tile 的 prologue、K 循环与
  epilogue 三段），以及 `flatten` 把两层循环合成一层后流水怎样跨过 tile 边界、代价是什么、何时不生效；能解释搬运与计算在
  `cp.async` 加 `mma.sync`、TMA 加 `wgmma`、TMA 加 `tcgen05` 与 TMEM 上的分工，主机侧与设备侧描述符、warp 专用化、epilogue
  拆半与共享内存预算的取舍，以及同一份源码在 sm_89、sm_120 与非 NV 后端上各退到哪一档；对“持久化的收益随 K 增大而减小”作出
  可证伪的预测，在 RTX 5090 上经受控测量得到支持，并能把总比值拆成持久化本身与 `flatten` 两个因子，指出收益主要来自 `flatten`、
  持久化本身的效应很小且其中三项变化无法由这次测量拆开；独立实现了接受行主序 B、任意尺寸的持久化 kernel 与带输入检查的包装函数，
  通过解释器、只编译与 GPU 数值验收，并能解释越界下标的改写与 mask 的先后、下标的取值连续与两条声明、合并后 prologue 里算出的
  值为何丢失声明、epilogue 的游标从何而来。本结论的范围是 Triton v3.7.1、NVIDIA 后端 sm_89、sm_90、sm_100、sm_120 与 AMD
  gfx942 的只编译观察、CPU 解释器，以及一台 RTX 5090（sm_120）上的数值验收与测量；描述符版与 warp 专用化版没有实机运行。
