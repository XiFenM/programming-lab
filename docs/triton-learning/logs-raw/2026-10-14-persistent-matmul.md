---
archive_type: "study-log-visible-dialogue"
schema_version: 1
archive_id: "sl-fe8ec557961b44348970ae7a7181c25e"
status: "final"
title: "持久化矩阵乘：跨 tile 流水、搬与算的分工、受控测量与下标的取值连续"
provider: "claude"
project_name: "programming-lab"
project_fingerprint: "7c4c768a8b0a"
source_session_id: "08d279c9-e031-4916-9699-0064ed77037f"
source_file: "session-08d279c9-snapshot.jsonl"
start_message_id: "msg-414ca97898d0aa9dbc7b"
end_message_id: "msg-dc91e00aff87fcbb5916"
message_count: 161
source_sha256: "7e02a5828185d0b4eeb3c79de7c2e8456da9f66ed2f51aae004f7b951a74c6fd"
visible_content_sha256: "0204d547229eb7530a4dc39f716859c98de4bb9e74643f668bb33baa4fd3df46"
target_precondition_sha256: null
first_message_at: "2026-10-10T03:18:35.924Z"
last_message_at: "2026-10-14T12:01:22.896Z"
created_at_utc: "2026-10-14T12:28:09.852434+00:00"
updated_at_utc: "2026-10-14T12:28:09.852434+00:00"
normalization: {"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"}
redaction: {"version":"study-log-redaction-v1","categories":[],"applications":[]}
privacy_risks: {"categories":["proprietary"],"counts":{"proprietary":27}}
structured_record: "docs/triton-learning/logs/2026-10-14-persistent-matmul.md"
message_phases: [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null]
migration: null
---

# 持久化矩阵乘：跨 tile 流水、搬与算的分工、受控测量与下标的取值连续

> 此文件是规则化提取的“可追溯可见文本对话”，不是完整客户端 Session，也不代表已经匿名化。
> system、developer、reasoning、工具事件、客户端注入和附件正文默认不包含在内。

结构化学习记录：[查看记录](<../logs/2026-10-14-persistent-matmul.md>)

---

**001 · 用户** · `2026-10-10T03:18:35.924Z` · `msg-414ca97898d0aa9dbc7b`

好，接下来让我们开始下一节triton课程的学习吧。

---

**002 · 助手** · `2026-10-10T03:22:00.740Z` · `msg-024c72247ff454ae1e07`

源码缓存只取了一部分目录，正在补齐 Triton v3.7.1 中与本课相关的几个目录（循环合并、流水、warp 专用化、TMA），随后做只编译探查。

---

**003 · 助手** · `2026-10-10T03:22:44.800Z` · `msg-54d4c519a31d64603380`

源码已读到主机侧描述符的处理方式。现在开始写只编译探查脚本，把教程的五个 kernel 分别编到 sm_89、sm_90、sm_100，拿到共享内存用量和指令证据。

---

**004 · 助手** · `2026-10-10T03:24:22.888Z` · `msg-df96052bcc8d6e596ddc`

正在看 sm_89 上的编译结果：persistent 版有一处与 naive 版不同的读入方式，需要读中间表示确认原因；之后再编 sm_90 和 sm_100。

---

**005 · 助手** · `2026-10-10T03:27:05.313Z` · `msg-ae90fad34a367412cfe6`

还在核对同一个现象的成因（已确认是流水阶段分配时 B 的读入没有被选中），马上读完判定条件，然后转去 Hopper/Blackwell 的部分。

---

**006 · 助手** · `2026-10-10T03:29:55.072Z` · `msg-335525a1b3dfb2bb2c14`

核对基本完成，正在收最后一项（教程 24 组配置在 sm_89 上的共享内存用量），随后写课程记录并给出开课导入。

---

**007 · 助手** · `2026-10-10T03:34:05.577Z` · `msg-e088aafec2e63b83ff6a`

快收尾了：正在确认各代硬件的共享内存上限（CUDA 官方表），然后立即写课程记录并开讲。

---

**008 · 助手** · `2026-10-10T03:41:23.316Z` · `msg-ffe1234dafa24ac653b2`

第 09 课开始。课程记录建在 [09-persistent-matmul.md](docs/triton-learning/lessons/09-persistent-matmul.md)，Checkpoint 已指向本课，改动都没有提交。

本课有四个目标：

- **O1**：持久化调度与跨 tile 的流水。
- **O2**：搬运与计算的分工（TMA、warp 专用化、epilogue 拆半），以及它们在各代硬件上的回退。
- **O3**：度量。需要你在自己的 GPU 上做一次“先预测、再测量、再解释”。
- **O4**：动手实现一个持久化矩阵乘。

O3 的实测和 O4 的实现如果想改成可选，现在说就行。结课要你确认，下一课不会自动开始。

开课前我把教程的五个 kernel 在本机按 sm_89、sm_90、sm_100、sm_120 只编译了一遍。下面的数字都来自这次编译，没有任何实机数值或性能结果。

## 参考教程

- 仓库快照：[09-persistent-matmul.py](docs/triton-tutorials/official/09-persistent-matmul.py)，共 758 行，与[线上 v3.7.1 的同名文件](https://github.com/triton-lang/triton/blob/v3.7.1/python/tutorials/09-persistent-matmul.py)逐字相同。
- 本课覆盖整个文件。课前建议只读两处：[文件头说明](docs/triton-tutorials/official/09-persistent-matmul.py#L1-L20)，以及 [`bench()` 与 `validate()`](docs/triton-tutorials/official/09-persistent-matmul.py#L654-L716)，看它把哪几种实现放在一起比。
- 五个 kernel 随节点读，每个节点我会说对应哪几行。

## 为什么学、学什么

第 03 课的矩阵乘把 C 切成 tile，每个 tile 发射一个 CTA。它是对的，但离 cuBLAS 有距离。差距不在算法，乘加次数完全一样，而在张量核心（执行 `tl.dot` 编出的 MMA 指令的硬件）有多少时间真的在算。

一个 tile 从发射到退出经过三段：

1. **prologue**：算坐标，发出头几轮读入。
2. **K 循环**：读入与乘加交替。
3. **epilogue**：转回 fp16，写回 C。

只有 K 循环里数据已经到位时，张量核心才在工作。prologue、等第一批数据、epilogue、CTA 退出后再发射下一个，这些时间它都闲着。块越大、流水越深，一个 SM 上同时放得下的 CTA 越少，就越没有别的 CTA 来填这些空档。

这一课要解决的矛盾就是：tile 之间的交接和数据搬运都要时间，而每个 SM 上往往只有一个 CTA，怎样让张量核心在这些时间里不停下来。教程的五个 kernel 是逐步加码的回答：

| 教程里的 kernel | 发射网格 | 搬运方式 | 引入的新东西 |
| --- | --- | --- | --- |
| `matmul_kernel` | 每个 tile 一个 CTA | 指针加 `tl.load` | 基线，结构同第 03 课 |
| `matmul_kernel_persistent` | 每个 SM 一个 CTA | 同上 | 持久循环、`flatten` |
| `matmul_kernel_tma` | 每个 tile 一个 CTA | 主机侧描述符 | TMA、`warp_specialize` |
| `matmul_kernel_tma_persistent` | 每个 SM 一个 CTA | 主机侧描述符 | epilogue 拆半 |
| `matmul_kernel_descriptor_persistent` | 每个 SM 一个 CTA | 设备侧描述符 | `flatten` 可以关掉 |

代价也是逐步加上去的：更多共享内存、更多 warp、更严的对齐要求、更新的硬件。所以每一步都要回答三件事：换来什么、付出什么、哪一代硬件才有。

学完你应该能：

- 画出持久化矩阵乘从发射到写回的完整流程。
- 说清每种手段消掉的是哪一段空转。
- 判断同一份源码在 sm_89、Hopper、Blackwell 和非 NV 后端上各退到哪一档。
- 自己测一次，并用编译产物解释结果。
- 用一分半钟向面试官讲清这些取舍。

**全流程骨架**（后面每个节点都回到这张图）：

```text
C[M,N] = A[M,K] @ B[K,N]，fp16 读入，fp32 累加，fp16 写回
  → 切成 T = ⌈M/BLOCK_M⌉ × ⌈N/BLOCK_N⌉ 个 tile，按 grouped ordering 编号为 tile_id
  → 发射 P 个 CTA：逐 tile 发射时 P = T；持久化时 P = min(NUM_SMS, T)
  → 每个 CTA： for tile_id in range(pid, T, NUM_SMS)          ← 节点 2
        prologue：tile_id → (pid_m, pid_n) → 行列偏移，累加器清零
        K 循环 × k_tiles：读 A、B 各一块 → tl.dot 累加        ← 怎么搬：节点 4；谁来搬：节点 5
        epilogue：fp32 → fp16，写回 C 的一块                   ← 节点 6
     两层循环合成一层后，流水跨过 tile 边界                    ← 节点 3
  → 度量：TFLOPS = 2·M·N·K ÷ 时间，与 cuBLAS、torch.matmul 对照 ← 节点 1 与节点 7
```

**路线**：

1. tile 的三段与度量
2. 持久化调度
3. `flatten` 与跨 tile 的流水（涉及编译器内部，会配图解）
4. TMA 与两种描述符
5. warp 专用化
6. epilogue 拆半与共享内存预算
7. 基线与测量方法

之后是串讲和综合验收。

**完成标准**：能对着骨架讲清每一步为什么这样设计，并对一个没讲过的设备或配置判断哪一步失效。

## 贯穿案例

全课沿用教程 `bench()` 的默认形状：

- A 是 `[M, K] = [8192, 512]`，B 是 `[K, N] = [512, 8192]`，C 是 `[8192, 8192]`，全部 fp16。
- 块取教程 autotune 配置中的一组：`BLOCK_M = 128`、`BLOCK_N = 128`、`BLOCK_K = 64`、`GROUP_SIZE_M = 8`、`num_stages = 3`、`num_warps = 8`（256 个线程）。
- 设备先按上一课的 sm_89 讲。SM 数记作 `NUM_SMS`，举例时取 128；实际值用 `torch.cuda.get_device_properties(0).multi_processor_count` 查。

由此得到：

| 量 | 算式 | 数值 |
| --- | --- | --- |
| tile 数 T | (8192 ÷ 128) × (8192 ÷ 128) | 64 × 64 = 4096 |
| 每个 tile 的 K 循环次数 `k_tiles` | 512 ÷ 64 | 8 |
| A 的一块 `[BLOCK_M, BLOCK_K]` | 128 × 64 × 2 字节 | 16,384 字节 |
| B 的一块 `[BLOCK_K, BLOCK_N]` | 64 × 128 × 2 字节 | 16,384 字节 |
| 累加器 `[BLOCK_M, BLOCK_N]`，fp32 | 128 × 128 个值 ÷ 256 个线程 | 每线程 64 个寄存器 |
| C 的一块，fp16 | 128 × 128 × 2 字节 | 32,768 字节 |
| 一个 tile 的计算量 | 2 × 128 × 128 × 512 | 约 1.68 × 10⁷ 次浮点运算 |
| 整个问题的计算量 | 2 × 8192 × 8192 × 512 | 约 6.87 × 10¹⁰ 次 |

## 节点 1：一个 tile 的三段，张量核心在哪里空转

**对应教程**：[`_matmul_launch_metadata`](docs/triton-tutorials/official/09-persistent-matmul.py#L71-L82)，以及[配置、naive kernel 与包装函数](docs/triton-tutorials/official/09-persistent-matmul.py#L90-L180)。建议讲完再读，对照你第 03 课的实现。

**结论**：逐 tile 发射的 kernel 里，每个 tile 都要付一遍与 K 无关的固定成本。本例的块大到一个 SM 只放得下一个 CTA，这些成本没有别的 CTA 来掩盖，直接变成张量核心的空转。

**机制**。一个 CTA 处理一个 tile 的时间线：

```text
发射 │ prologue │ 预热：先发 2 轮读入 │ K 循环 × 8：读入 ∥ MMA │ epilogue │ 退出
     └──────── 张量核心空转 ────────┘                        └─ 空转 ─┘
```

- **prologue**：由 `pid` 算出 `(pid_m, pid_n)`、行列偏移和指针，把累加器清零。
- **预热**：`num_stages = 3` 表示读入比乘加提前两轮。编译产物里循环之前有两轮异步拷贝，第一次 MMA 必须等第一轮数据从显存到达，这段等待没有计算可以重叠。
- **K 循环**：稳态下，本轮的 MMA 与后两轮的读入同时进行。
- **epilogue**：把 fp32 累加器转成 fp16 并写回 C。

用词上和第 02 课区分一下：那里 prologue、epilogue 指流水的预热和排空；这一课按教程和 Triton 源码的用法，指一个 tile 在 K 循环之前和之后的代码。流水的那两段我称为预热和排空。

**为什么这在本例里是问题**。分三步看。

第一步，每个 tile 的寿命很短。教程 03 提到 A100 上 fp16 矩阵乘是 220–245 TFLOPS 的量级。按这个量级，本例只要约 0.3 ms；摊到 4096 个 tile 和一百个左右的 SM 上，一个 tile 在一个 SM 上只活七八微秒。这是借用另一台设备的数字做的量级估计，不是本例的实测。在这个尺度上，每个 tile 多出零点几微秒的固定成本就是百分之几。

第二步，本例的 CTA 很大，一个 SM 只放得下一个。按第 02 课的 occupancy 模型，用 naive 版在 sm_89 上的编译结果来算：

| 资源 | 每个 CTA 需要 | 每个 SM 拥有 | 可驻留 |
| --- | --- | --- | --- |
| 寄存器 | 162 × 256 线程 = 41,472 | 65,536 | 1 个 |
| 共享内存 | 65,536 字节 | 100 KB | 1 个 |

共享内存的 65,536 字节，是 A、B 各一块（共 32,768 字节）乘以两个缓冲槽。

第三步，把两者合起来。小块的 kernel 里，一个 SM 同时驻留好几个 CTA，硬件让它们的 warp 交替执行，一个 CTA 的 epilogue 会被另一个 CTA 的 K 循环填上。本例没有这个余地：每个 SM 把“发射、prologue、预热、8 轮 K 循环、epilogue、退出”串行重复 32 次（4096 ÷ 128），每次的空档都是真空档。这个“驻留多个 CTA 时空档会被自然填上”的说法是从 occupancy 模型推出来的，O3 的测量会检验它。

**教程的 naive kernel 比第 03 课多了什么**。有三处，第二处后面会反复用到。

1. **越界下标的处理**。第 03 课教程用取模（`% M`），这里改成置 0：`offs_am = tl.where(offs_am < M, offs_am, 0)`。
2. **对偏移量的声明**：`tl.max_contiguous(tl.multiple_of(offs_am, BLOCK_SIZE_M), BLOCK_SIZE_M)`。
   - 上一课的 `tl.multiple_of` 是对指针声明对齐，这里是对下标声明。
   - 按 Triton 的定义，contiguity 是“可以切成多长的连续整数段”，divisibility 是“每段的第一个元素能被多大的 2 的幂整除”。这一行说的是：这 128 个下标是一整段连续整数，首个是 128 的倍数。
   - 需要它的原因：`tl.where` 之后，编译器无法再从 `arange` 推出“相邻下标连续”，也就不能把一行里相邻的 8 个 fp16 当成一个 16 字节的整体去读，而那正是异步拷贝的前提（上一课节点 5）。
   - 实测：去掉这两行，B 的读入退回逐元素的同步读（12 条 `cp.async` 加 32 条 `ld.global.b16`）；保留时 A、B 都是异步拷贝（24 条 `cp.async`）。
   - 和上一课一样，这是一项不被检查的声明。在边界 tile 上尾部下标被置 0，它并不严格成立，后果留到讲边界时再看。
3. **度量信息与 FP8 输出**。`launch_metadata` 给每次发射挂上名字、`flops16 = 2·M·N·K` 和字节数，供 profiler 换算成 TFLOPS。输出类型按 `c_ptr` 的元素类型在编译期分支，fp16 或 FP8。

**度量**。每个输出元素是 K 次乘加，一次乘加算两次浮点运算，所以总量是 2·M·N·K。本例如果一次发射耗时 1 ms，就是 68.7 TFLOPS。全课都用这个口径，proton 和 cuBLAS 基线放在节点 7。

**边界**。空转是否显著取决于两个比值：固定成本相对 K 循环的长度，以及一个 SM 上能驻留几个 CTA。K 很大或块很小时，这个问题会自己变轻。

## 节点 2：持久化调度

**对应教程**：[`_compute_pid`、`matmul_kernel_persistent` 与 `matmul_persistent`](docs/triton-tutorials/official/09-persistent-matmul.py#L273-L366)。讲完再读。

**结论**：发射的 CTA 数从 T 降到 `min(NUM_SMS, T)`。每个 CTA 在 kernel 内用步长 `NUM_SMS` 的循环依次处理多个 tile。这样发射和退出只付一次，而且“同一个 SM 上哪个 tile 接在哪个后面”从硬件调度器手里转到了 kernel 手里。

**机制**。包装函数只改了两处：

```python
NUM_SMS = torch.cuda.get_device_properties("cuda").multi_processor_count
grid = lambda META: (min(NUM_SMS, cdiv(M, BLOCK_SIZE_M) * cdiv(N, BLOCK_SIZE_N)), )
```

kernel 多了一层外循环，`NUM_SMS` 作为编译期常量传入：

```python
start_pid = tl.program_id(axis=0)
for tile_id in tl.range(start_pid, num_tiles, NUM_SMS, flatten=True):
    pid_m, pid_n = _compute_pid(tile_id, num_pid_in_group, num_pid_m, GROUP_SIZE_M, NUM_SMS)
    ...                         # prologue：行列偏移，累加器清零
    for ki in range(k_tiles):   # K 循环
        ...
    ...                         # epilogue：写回 C
```

`_compute_pid` 就是第 03 课的 grouped ordering 换算，输入从 `pid` 换成 `tile_id`。`flatten=True` 留到节点 3，这里先当它不存在。

代入贯穿案例，T = 4096，`NUM_SMS = 128`，所以发射 128 个 CTA，每个处理 32 个 tile。每组有 `GROUP_SIZE_M × num_pid_n = 8 × 64 = 512` 个 tile。看 5 号 CTA 走过的路：

| 第几轮 | `tile_id` | 组号 | `pid_m` | `pid_n` |
| --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 0 + 5 % 8 = 5 | 5 // 8 = 0 |
| 1 | 133 | 0 | 0 + 133 % 8 = 5 | 133 // 8 = 16 |
| 2 | 261 | 0 | 5 | 32 |
| 3 | 389 | 0 | 5 | 48 |
| 4 | 517 | 1 | 8 + 517 % 8 = 13 | (517 % 512) // 8 = 0 |

从这张表读出三件事：

- **它在同一个行块上连做 4 个 tile**，每次向右跳 16 个列块，然后换到下一组的行块。
- **grouped ordering 的效果保留了下来**。同一轮里 128 个 CTA 处理的是连续的 128 个编号。第 0 轮是编号 0–127，正好是 8 个行块乘 16 个列块的一片，共用 8 个 A 行块和 16 个 B 列块。
- **负载是均衡的**。上一课不均衡是因为各问题的 K 不同；这里只有一个问题，每个 tile 的 K 循环次数相同，每个 CTA 拿到 ⌈T/P⌉ 或 ⌊T/P⌋ 个 tile，也不需要前缀和扫描。

还有一处写法值得注意。naive 版在 K 循环里用 `a_ptrs += BLOCK_SIZE_K * stride_ak` 递推指针；持久版改成每轮从基地址重算（`offs_k = ki * BLOCK_SIZE_K + tl.arange(...)`）。原因和你上一课遇到的第 2 个问题相同：跨循环传递的指针会一直累加，换 tile 时还得复位，重算就没有这个状态。

**为什么这样设计**。

- **摊薄固定成本**。CUTLASS 文档对同类设计的说法是：持久化线程块在其生命期内计算多个输出 tile，主要收益是摊薄线程块发射与 kernel prologue 的开销。本例每个 SM 从 32 次发射变成 1 次。
- **拿到 tile 之间的交接权**。逐 tile 发射时，前一个 CTA 退出、后一个 CTA 开始，中间发生什么 kernel 管不到。持久化之后，前一个 tile 的 epilogue 和后一个 tile 的 prologue 在同一段代码里，才有可能让后一个 tile 的读入在前一个还没算完时就发出去。节点 3 的 `flatten` 和节点 5 的 warp 专用化都建立在这一点上。单看节点 2，它只解决了发射成本，预热和 epilogue 的空档还在。
- **和第 02 课的区别**。那里的 persistent softmax 把网格设成 `NUM_SM × occupancy`，因为一行 softmax 很轻，一个 SM 能驻留很多 program。这里直接设成 `NUM_SMS`，默认每个 SM 一个，前提正是节点 1 算出的“这种块一个 SM 只放得下一个”。

**真实系统**。CUTLASS 从 Hopper 起的 GEMM 主力设计就是 warp 专用化加持久化，由一个 tile scheduler 决定网格形状和 tile 到线程块的分配。教程这个 kernel 相当于其中最简单的静态调度。来源：CUTLASS v3.9.2 的 `media/docs/cpp/efficient_gemm.md`。

**边界**。

- T 不超过 `NUM_SMS` 时，每个 CTA 只做一个 tile，循环只转一圈。
- `NUM_SMS` 只影响步长和网格大小，传错了结果仍然正确，变的只是性能。教程查的是默认 CUDA 设备，不是输入所在的设备。
- “每个 SM 恰好一个 CTA”是按调度器的通常行为设计的，CUDA 没有把 CTA 绑到某个 SM 的接口。
- 调度是静态的。某个 SM 被别的任务占用时，它名下的 tile 只能等，没有别的 CTA 来接手（上一课讨论过的动态领取可以解决）。

## 检查题

条件都按贯穿案例：fp16、块 128×128×64、`GROUP_SIZE_M = 8`、3 stages、8 warps、sm_89、`NUM_SMS = 128`。

1. **预测**。教程的 benchmark 固定 M = N = 8192，把 K 从 1024 扫到 128，块不变。K = 1024 和 K = 128 时，tile 数和每个 tile 的 K 循环次数各是多少？持久化相对逐 tile 发射的收益，你预计在哪一端更明显？请用 tile 的三段说明理由。
2. **边界**。把矩阵换成 M = N = 1024、K = 512。持久版会发射多少个 CTA，每个处理几个 tile？这时它和 naive 版还剩什么差别？
3. **迁移**。节点 1 算出本例的 naive CTA 在一个 SM 上只能驻留一个。假如换成一种很小的块配置，使一个 SM 能同时驻留 4 个 naive CTA，这时仍然“每个 SM 只发一个持久 CTA”会出什么问题？第 02 课的 persistent softmax 是怎么处理这件事的？

顺带一问，不急：后面做实测时你打算用哪台 GPU？讲解里我先按上一课的 RTX 4090 D（sm_89）举例。

---

**009 · 用户** · `2026-10-10T09:55:23.841Z` · `msg-c8168d338be7d97ea6e9`

如果BLOCK没那么大，一个SM可以放得下多个CTA，为什么每个tile发射的的固定成本可能被其他CTA掩盖？不会变成tensor core的空转？是怎么掩盖的？

---

**010 · 助手** · `2026-10-10T09:58:24.774Z` · `msg-f1c3905201ff15b8aec1`

固定成本并没有消失，每个 CTA 照样要付自己的那一份。“被掩盖”说的是另一件事：空转要按 SM 算，不按 CTA 算。张量核心属于 SM，是这个 SM 上所有驻留 warp 共用的。一个 CTA 在等数据或做 epilogue 时，别的 CTA 的 warp 可以接着用它，所以它不闲。

## 机制：SM 怎样在多个 CTA 之间切换

按 CUDA Programming Guide 的 Hardware Multithreading 一节，SM 是这样工作的：

- SM 拿到一个或多个线程块后，把它们拆成 warp，交给 warp 调度器。
- 每个 warp 的执行上下文（程序计数器、寄存器）在它的整个生命期里都留在片上，所以在 warp 之间切换没有代价。
- 每个指令发射周期，调度器挑一个“有线程就绪”的 warp，发射它的下一条指令。

所以调度器眼里只有一池子 warp，不区分它们来自哪个 CTA。一个 warp 在等显存数据到达，或者它的 CTA 刚退出、新的还没就位，它就不是就绪状态，调度器会去发射别的 warp 的指令。只要池子里还有任何一个 warp 手上有 MMA 可做，张量核心就在工作。

## 例子

先固定一组假想的数字，只为看清机制，不是测量值：

- 一个 tile 的固定成本（发射、prologue、等第一批数据、epilogue）合计 2 µs。
- 一个 tile 的 MMA 如果独占张量核心，需要 6 µs。
- 再做一个对“多 CTA”最不利的假设：张量核心同一时刻只够一个 CTA 用。

下图每格 2 µs。`F` 是固定成本，`M` 是在用张量核心，`-` 是在排队等张量核心，`.` 是张量核心空闲，`TC` 行是这个 SM 的张量核心。

```text
只驻留 1 个 CTA
CTA a   FMMMFMMMFMMMFMMM
TC      .MMM.MMM.MMM.MMM       每 8 µs 完成一个 tile，张量核心 75% 的时间在忙

驻留 4 个 CTA
CTA a   FMMMF--------MMMF---
CTA b   F---MMMF--------MMMF
CTA c   F------MMMF--------M
CTA d   F---------MMMF------
TC      .MMMMMMMMMMMMMMMMMMM   稳定后每 6 µs 完成一个 tile，张量核心一直在忙
```

从下半张图能读出两种掩盖方式：

- **错开时的掩盖**。看第 8–10 µs：CTA a 在为下一个 tile 付固定成本，这 2 µs 一点没少；但同一时间 `TC` 行是 `M`，张量核心在给 CTA b 算。a 的固定成本落在了 b 的计算时间里。
- **对齐时的掩盖**。看第 0–2 µs：四个 CTA 同时在付固定成本，张量核心确实闲着。但这是四个 tile 的固定成本一起付的，墙上时间只过了 2 µs，而不是 8 µs。

第二点是更本质的原因。固定成本大部分是等待（等发射、等数据到达），等待可以很多个 CTA 同时进行。MMA 是吞吐，受 SM 上张量核心数量的限制，不能靠多放 CTA 加速。多个 CTA 驻留，就是把串行的等待变成并行的等待。这和第 02 课里 occupancy 用来隐藏访存延迟是同一个道理。

回到本例的大块：一个 SM 只有一个 CTA，就是上半张图。它等的时候，池子里没有第二个 warp 组可以顶上，那 2 µs 就是张量核心的真空档。后面的节点做的事，是让同一个 CTA 自己把等待和计算叠起来：下一个 tile 的读入在当前 tile 还在算时就发出去（节点 3），或者让一部分 warp 专门搬数据、另一部分专门算（节点 5）。

## 那为什么不直接用小块

小块能白拿这种掩盖，但要付两样代价：

- **每次浮点运算要搬的数据变多**。一个 tile 读入 `(BLOCK_M + BLOCK_N) × K` 个元素，完成 `2 × BLOCK_M × BLOCK_N × K` 次浮点运算。两者之比在 128×128 的块上是 128，在 64×64 的块上是 64。块减半，同样的计算量要搬两倍的数据。上一课的调度模型里也见过：块从 128 降到 64，累计读入量从 38.3 MB 升到 76.7 MB。
- **tile 数变成 4 倍**，固定成本的总次数也变成 4 倍，只是它们更容易被掩盖。

所以大块赢在访存，输在没有别的 CTA 帮忙掩盖。这一课的几种手段就是为了让大块两头都占。

## 这个模型的可信范围

- 调度器按就绪 warp 逐条发射指令、切换无代价，是文档写明的。
- “张量核心同一时刻只服务一个 CTA”是我为了画图做的简化。真实的交替发生在指令粒度上，一个 CTA 能不能吃满一个 SM 的张量核心，文档没有给数字。
- 一个 CTA 退出、新 CTA 就位期间，其他 CTA 受不受影响，文档也没有细节。

方向是可靠的，幅度要靠 O3 的测量来定。

## 检查题的调整

第 1、2 问不变。原来的第 3 问前半已经被上面的解释覆盖，换成下面这道：

3. **诊断与设计**。把块换成 64×64×32，矩阵仍是 M = N = 8192，所以 T = 16384；假设这时一个 SM 能同时驻留 4 个 CTA，`NUM_SMS = 128`。有人为了利用这一点，只把持久版包装函数里的网格从 `min(NUM_SMS, T)` 改成 `min(4 × NUM_SMS, T)`，kernel 一行没动。
   - (a) 结果还正确吗？编号为 1000 的 tile 会被几个 CTA 计算？
   - (b) 应该怎样改才对？第 02 课的 persistent softmax 是怎么处理同一件事的？

---

**011 · 用户** · `2026-10-11T08:51:03.884Z` · `msg-d4282489d5593ddf76b8`

那么，对于驻留4个CTA的场景，假如四个CTA都搬好数据，给TC计算了，此时TC是只能给各个CTA一个一个算吗？CTA多了会不会竞争占用TC？

---

**012 · 助手** · `2026-10-11T08:53:52.789Z` · `msg-77a0e0cc3a739aa6d248`

资料已核对完（NVIDIA 的架构白皮书和本例的编译产物），下面直接回答。

会竞争。不过不是按 CTA 排队、一个算完再算下一个，而是按 warp、按指令交替：四个 CTA 同时都在往前走，只是每个都比独占时慢。上一条里我把它画成“一个 CTA 连续占用 6 µs”，那是为了好读做的简化，这里把它改准确。

## 硬件上，张量核心是怎样被分用的

公开资料里能查到的结构：

| 设备 | SM 内部 | 来源 |
| --- | --- | --- |
| V100 | SM 分成 4 个处理块，每块有自己的 1 个 warp 调度器、寄存器堆和 2 个张量核心 | V100 架构白皮书 |
| A100 | 每个 SM 有 4 个张量核心，每个分区 1 个，合计每个时钟周期 1024 次 fp16 乘加 | Ampere Architecture In-Depth |
| H100 | 每个 SM 有 4 个张量核心 | Hopper Architecture In-Depth |

你的 RTX 4090 D 这一代，我没有查到公开的对应数字。

从这张表能读出两点：

- **张量核心是个位数的固定资源。** 一个 SM 每个周期能发射的 MMA 指令只有几条，这是吞吐的上限。
- **调度单位是 warp，不是 CTA。** 每个处理块的调度器每个周期从就绪的 warp 里挑一个，发射它的下一条指令，不区分这个 warp 属于哪个 CTA。

## “交给 TC 计算”在代码里是什么

它不是把整块数据一次交出去，而是一连串由 warp 发射的指令。以贯穿案例的 naive 版在 sm_89 上的编译结果为例：

- K 循环体里有 64 条 `mma.sync…m16n8k16`。
- 每条由一个 warp 发射，算输出里 16×8 的一小片，沿 K 方向吃 16 个元素。
- 8 个 warp 各发 64 条，一轮 K 循环共 512 条。

所以四个 CTA 都准备好时，SM 面对的是一大池子就绪的 warp，每个手里都排着一串 MMA 指令。调度器每个周期挑几个发射，下个周期再挑。结果是四个 CTA 的指令交错执行，谁也不会等别人整轮算完。

## 改准确后的时间线

沿用上一条的假想数字：固定成本 2 µs，MMA 独占张量核心时要 6 µs。四个 CTA 同时就绪，各自拿到四分之一的张量核心，于是每个都要 24 µs 才算完。

下图每格 2 µs。`F` 是固定成本，`m` 是在算但只有四分之一速度，`TC` 行是张量核心。

```text
CTA a   FmmmmmmmmmmmmFmmmmmmm
CTA b   FmmmmmmmmmmmmFmmmmmmm
CTA c   FmmmmmmmmmmmmFmmmmmmm
CTA d   FmmmmmmmmmmmmFmmmmmmm
TC      .MMMMMMMMMMMM.MMMMMMM    每 26 µs 完成 4 个 tile
```

这是四个 CTA 步调完全一致的情形，对“多驻留”最不利。把三种情形放在一起：

| 情形 | 每个 tile 的墙上时间 | 张量核心在忙的比例 |
| --- | --- | --- |
| 只驻留 1 个 CTA | 8 µs | 75% |
| 驻留 4 个，步调完全一致 | 26 ÷ 4 = 6.5 µs | 24 ÷ 26 ≈ 92% |
| 驻留 4 个，完全错开（上一条的图） | 6 µs | 100% |

真实情况落在后两行之间。

## 竞争意味着什么

- **竞争不是损失，它说明张量核心被吃满了。** 我们要的正是这个状态。多驻留 CTA 并不增加张量核心的容量，只是减少它闲着的时间。
- **收益有上限。** 按这组假想数字，每个 tile 最快就是 6 µs，也就是纯 MMA 的时间。从 8 µs 到 6 µs 最多快 1.33 倍，吃满之后再多放 CTA 也不会更快。
- **吃满之后多放的 CTA 只有代价。** 每个 tile 从开始到结束拖得更长；占着更多寄存器和共享内存；同时在途的读入更多，争用显存带宽和 L2。
- **有一种情况多放还能再涨。** CTA 很小、warp 很少时，单个 CTA 即使在算，就绪的 warp 也喂不满所有张量核心。这时多驻留几个，除了填空档，还能提高同时在算的 warp 数。这一条是我按处理块结构推断的。

## 回到本课

本例的大块 CTA 有 8 个 warp，算的时候不缺就绪的 warp，缺的是它自己等待时有别的事可做。所以后面的手段都不是去多放 CTA，而是让这一个 CTA 尽量一直有可发射的 MMA。

## 这段解释的可信范围

- 文档写明的：调度器按就绪 warp 逐周期发射；V100、A100、H100 的张量核心数量。
- 我的简化：“各拿四分之一”是按平均分配画的，真实的挑选策略没有公开。
- 没有依据的：sm_89 上一个 SM 到底能同时执行几条 MMA。

方向可靠，幅度留给 O3 的测量。

三道检查题（第 3 问是上一条换过的那道）还在等你作答。

---

**013 · 用户** · `2026-10-11T08:55:22.928Z` · `msg-cc211054c43820969aaa`

明白了，我还有一个问题，你之前讲到越界下标的处理。第 03 课教程用取模（% M），这里改成置 0：offs_am = tl.where(offs_am < M, offs_am, 0)。我的问题是，为什么需要对M和N的越界下标进行处理？在读取计算时直接不处理，最后计算完成写回C时带上M和N维度的mask防止写回不就可以了吗？感觉读取时的处理似乎有些多余？

---

**014 · 助手** · `2026-10-11T09:00:35.364Z` · `msg-8eb0d050b248e1750ccd`

实验做完了，结论已经清楚；正在把课程记录里受影响的两处数据更正过来，然后回答你的问题。

---

**015 · 助手** · `2026-10-11T09:02:08.930Z` · `msg-7f9f3ada5b09f32496d4`

你对数值的判断是对的：只为了算对，读取时确实不用处理，写回时 mask 就够了。读取时的处理是为了另一件事——地址。`tl.load` 会真的去访问内存，越界的下标算出来的是矩阵之外的地址。

## 两类维度，两种要求

| 维度 | 越界的元素会不会影响有效输出 | 需要保证什么 | 教程的做法 |
| --- | --- | --- | --- |
| K（被求和的维度） | 会，它会进到累加里 | 值必须是 0 | 读入时 mask，`other=0.0` |
| M、N（自由维度） | 不会，只落到 C 的越界行列 | 只要地址合法，读到什么都行 | 把下标改到矩阵内，写回时 mask |

所以 M、N 方向的处理不是为了数值，而是为了让这次读取落在自己的内存里。

## 不处理会读到哪里

用教程自己的 [`validate(32, 32, 32)`](docs/triton-tutorials/official/09-persistent-matmul.py#L750) 来看：

- A 是 `[M, K] = [32, 32]` 的 fp16，共 1024 个元素、2048 字节。
- 教程所有配置的 `BLOCK_M` 都是 128，所以只有一个 tile，行下标是 0–127。
- 元素 `A[行, 列]` 的地址是 `a_ptr + (行 × 32 + 列) × 2` 字节。K 方向有 mask，列只取 0–31。

| 写法 | 第 32–127 行读的是什么 |
| --- | --- |
| 不处理 | 元素偏移 1024–4095，即 A 末尾之后的 3072 个元素、6,144 字节 |
| `tl.where(offs_am < M, offs_am, 0)` | 行下标变成 0，把第 0 行再读 96 遍，全部在 A 内 |

读到矩阵外面是未定义行为，通常有两种结局：

- **碰巧没事**。那段地址属于别的张量或分配器的内存池，读回来的是垃圾。垃圾只进了 C 的越界行，写回时被 mask 掉，结果仍然正确，没人发现。
- **直接出错**。那段地址没有映射，GPU 报非法内存访问，整个 CUDA 上下文作废。

落到哪一种取决于当时的内存布局，所以表现为有时对、有时崩。这是 CUDA 的一般行为，我们没有在 GPU 上实际触发过。

还有一点和上一课的 A6 是同一类：这种越界读不改变有效输出，数值测试发现不了。上一课在 A、B 两侧填 NaN 的保护区测试也拦不住它，因为 NaN 只进了被 mask 掉的行列。所以只能在写法上保证。

## 为什么是改下标，而不是像你上一课那样给读入加 mask

让地址合法有三种写法，加上“不处理”和“不加声明的 `tl.where`”一共五种。我在 sm_89 上把它们都编译了一遍，只看 B 的读入。条件：B 按普通的行主序 `[K, N]` 存放（连续方向是 N），块 128×128×64。

| 写法 | 地址安全 | N = 1024 | N = 1000（B 是一个 `[512, 1024]` 张量的前 1000 列，行步长仍是 1024） |
| --- | --- | --- | --- |
| 不处理 | 否 | 异步，16 字节一组 | 异步，16 字节一组 |
| 给读入加 M、N 方向的 mask | 是 | 异步，16 字节一组 | 同步，逐元素 |
| 取模 `% N`（第 03 课教程） | 是 | 异步，16 字节一组 | 同步，逐元素 |
| `tl.where(…, 0)`，不加声明 | 是 | 同步，逐元素 | 同步，逐元素 |
| `tl.where(…, 0)` 加声明（本课教程） | 是 | 异步，16 字节一组 | 异步，16 字节一组 |

“异步，16 字节一组”是 12 条 `cp.async`；“同步，逐元素”是 32 条 `ld.global.b16`，同时失去流水。

读这张表：

- **处理本身几乎不花钱**。不处理和教程的写法编出来的读入完全一样，差别只是每个 tile 多一次选择运算。所以它不多余，是用很小的代价换地址安全。
- **mask 和取模的效果依赖编译器知不知道 N 的整除性**。要把相邻 8 个 fp16 当成一个 16 字节的整体，编译器得能证明这 8 个要么全读要么全不读（mask），或者取模后仍然连续。这需要知道 N 是 8 的倍数之类的信息。JIT 只在调用时看到 N 是 16 的倍数才把这一点告诉编译器（上一课讲过的参数特化）；N = 1000 时没有这个信息，就退回逐元素。
- **你上一课三个方向都加 mask 后丢了异步拷贝，是同一个原因**。那里的尺寸是从表里读出来的，编译器对它一无所知。
- **声明是程序员直接作保证**，不依赖 N 的整除性，所以两列都保持异步。这是我从编译结果归纳出的差别；教程没有说明它为什么从取模改成这种写法。

## 声明不严格成立的地方

节点 1 留了一句“边界 tile 上这个声明并不严格成立”，这里补上。以下是按 `cp.async` 的语义推出来的，没有实测。

- 编译器相信声明，按 8 个元素一组整组读，每组从第一个元素的地址起连续读 16 字节。
- 整组都越界时，第一个元素的下标是 0，读的是第 0–7 列，合法。
- 一组跨在 N 上时（只有 N 不是 8 的倍数才会出现），它会多读第 N 列之后的最多 7 个元素。
- 多读的部分落在这一行自己的补齐区里。原因是只有行步长被确认是 16 的倍数时才会用 16 字节一组：
  - B 是连续张量时，行步长就是 N，N 是 16 的倍数，不会有跨界的组。
  - B 是视图时，行步长大于 N，多读的是底层张量里被切掉的那几列。
- M 方向不受影响：读入不沿行方向合并，越界的行只是去读第 0 行。

剩下的风险只有一种：底层存储在最后一行的行步长之内就结束了，比如手工用 `as_strided` 造出来的张量。

## 更正节点 1 的两个数字

教程的 `bench()` 和 `validate()` 传给指针版 kernel 的是 `b.T`，内存里按 `[N, K]` 存放，连续方向是 K 而不是 N。我之前是按行主序的 B 编译的，有两处要改：

- **声明的作用范围**。我说“去掉这两行声明，B 退回逐元素同步读”，这只在 B 按行主序存放时成立。按教程的传法，五种写法编出来的读入完全相同，声明不起作用。
- **寄存器数**。按教程的传法，naive 版每线程用 135 个寄存器，不是 162 个。135 × 256 = 34,560，两个 CTA 仍超过 65,536，“一个 SM 只驻留一个”的结论不变。

课程记录里的相关数据已经一并改正。

三道检查题还在等你作答。

---

**016 · 用户** · `2026-10-11T09:06:40.955Z` · `msg-45f040df98c1e5edb72b`

噢，是因为越界访问是有可能导致报错，程序崩掉，所以要处理是吗？

---

**017 · 助手** · `2026-10-11T09:06:50.579Z` · `msg-be0d0bd062ef43ed155e`

对，就是这个原因。补一点让它更准确：

- **越界读是未定义行为，崩溃只是其中看得见的一种结局。** 另一种结局是读到了别人的内存、结果碰巧还对。这种更麻烦，因为数值测试发现不了，换一种内存布局或换一台机器才突然崩。
- **所以不能靠“跑一下没报错”来判断，只能在写法上保证每次读取的地址都在矩阵内。** 改下标（置 0 或取模）和给读入加 mask 都是做这件事的办法。

没有别的疑问的话，可以回到那三道检查题。

---

**018 · 用户** · `2026-10-11T13:01:59.850Z` · `msg-548d0c1cc788e1d78ebf`

<pasted_content id="b992">
# 检查题

1. tile数量为 8192/128 * 8192/128 = 4096个。K=1024时，K方向循环次数为1024/64=16；K=128时，K方向循环次数为128/64=2次。持久化相对逐tile发射的收益，我预计在tile的三段中的prologue和epilogue上。因为相比于逐tile的分离发射，持久化将前一个tile的epilogue和后一个tile的prologue放在同一段代码里，于是可以在前一个tile写回结果时开始让后一个tile开始计算地址偏移和预热读取的工作，使得二者存在了被重叠优化的可能。
2. 该场景中，tile数量为 1024/128 * 1024/128 = 64个。而NUM_SMS=128。所以持久版会发射二者取小值，为64个，每个CTA处理一个tile。此时它和naive版只剩了naive版的K循环用的指针递推，而persistent版采用了地址重算
3. 那么此时就启动了4 * NUM_SMS个CTA，但是kernel内部tile循环时递增的偏移是NUM_SMS。那就导致很多tile会被重复计算多次。最终结果还是正确的，只是会产生很多冗余计算和重复写入结果。此时一共有4 * 128=512个CTA。编号1000的tile就会被第104、232、360、488号CTA处理计算。被4个CTA计算。应该在传参NUM_SMS时也改成4*NUM_SMS。02的kernel里，使用了tl.num_programs(0)来获取启动的program数量，而不作为传入参数进行判断。
</pasted_content id="b992">

---

**019 · 助手** · `2026-10-11T13:04:58.118Z` · `msg-3e570c5206f0455425b4`

第 2、3 问正确。第 1 问的数字正确，后半是我题目写得有歧义，下面换一种问法复查，不算你的问题。

## 第 1 问

- **数字都对**：4096 个 tile，K 循环 16 次和 2 次。
- **题目的歧义**：我问“在哪一端更明显”，本意是 K 扫描的两端（K = 1024 还是 K = 128）。紧接着又让你“用 tile 的三段说明”，于是被读成了“三段里的哪一段”。
- **你答的内容方向是对的**。前后两个 tile 的 epilogue 和 prologue 到了同一段代码里，才有了重叠的可能。你用的是“可能”，这个词很准确。

两点补充：

1. **漏了持久化直接拿到的那一项。** CTA 的发射和退出，每个 SM 只付一次。本例是从 32 次变成 1 次。这是不依赖任何后续手段就到手的收益。
2. **只加持久循环时，重叠并没有发生。** 代码仍然按顺序执行：第 i 个 tile 的 epilogue 做完，才轮到第 i+1 个 tile 的 prologue 和第一轮读入，等数据的那段空档还在。要真的叠起来，得靠节点 3 的 `flatten` 或节点 5 的 warp 专用化。

## 第 2 问

正确：64 个 CTA，每个处理一个 tile，剩下的差别只是指针重算和递推的写法。

三点补充：

- **调度上两者等价**，没有可摊薄的东西，所以收益是零。
- **两个版本都只用了 64 个 SM，另一半空着。** 这时该调的是块大小而不是调度方式，比如 64×64 的块有 256 个 tile，能把 SM 用满。
- **教程的持久版还带着 `flatten`，它在这里只有代价。** 即使每个 CTA 只做一个 tile，共享内存也多一档（sm_89 上 98,304 字节对 65,536 字节）。原因放到节点 3。

## 第 3 问

全部正确，而且比我预想的答案更好。

- **诊断对**：结果正确，但重复计算、重复写入。编号 1000 的 tile 由 104、232、360、488 号 CTA 各算一次。
- **冗余的规模**：编号 0–127 算一次，128–255 两次，256–383 三次，其余 16000 个都是四次，总工作量约为 3.95 倍。
- **修法对**：步长必须等于发射的 CTA 数。
- **`tl.num_programs(0)` 记得对**。教程 02 第 89 行就是 `row_step = tl.num_programs(0)`，你第 02 课的实现也是这样写的。

我原本想要的答案是“网格取 `NUM_SM × occupancy`”。你指出的是更根本的一层：步长直接从发射的网格里读，两者就不可能不一致。

我把持久版矩阵乘的步长也改成 `tl.num_programs(0)` 编译了一遍。sm_89 和 sm_90 上读入方式、共享内存、寄存器都不变，只多一条除法指令。所以教程 09 用编译期常量 `NUM_SMS` 并不是编译结果逼出来的，教程也没有说明原因。

这和上一课 `num_sm` 查错设备是同一类教训：主机和 kernel 都要用的量，尽量只在一处产生。

## 复查（第 1 问换一种问法）

条件同贯穿案例：块 128×128×64，`NUM_SMS = 128`，只考虑持久化本身，不考虑 `flatten`。两问各用一两句话回答即可。

1. M = N = 8192 不变。K = 128 和 K = 1024 两种情况，哪一种情况下持久化相对 naive 的提速比例更大？为什么？
2. K = 512 不变。M = N = 8192 和 M = N = 2048 两种情况，哪一种提速比例更大？为什么？

答完之后进入节点 3：`flatten` 怎样把两层循环合成一层，让流水跨过 tile 边界。那一节涉及编译器内部，我会配图解和真实的编译产物。

---

**020 · 用户** · `2026-10-11T13:23:24.239Z` · `msg-831b2e9f960a52088931`

<pasted_content id="b992">
# 复查
1. 我觉得持久化对K=128的情况的提速比例更大。因为对于K=128，K循环更少，其在整个kernel里的占比相比于K=1024更小，prologue和epilogue的占比就更大。而持久化主要就是优化这两部分，那么对于K=128的提速效果就更大了。
2. 我认为对于M = N = 8192的提速比例会更大。同样也是如上的原因。在M = N = 8192情况下，分出的tile数量更多，那么相比于M = N = 2048，其tile循环上的epilogue+prologue的间隔就更多。有了更多的间隔，其可优化空间就更大。最终提速比例应该就更大。
等下，我再重考虑下。虽然绝对的间隔值更多，但是间隔的相对比例不一定。第一种有4096个tile，每个CTA负责32个tile，那么就有31个间隔，间隔相比于K循环就是31:32；第二种则是256个tile，每个CTA负责2个tile，就只有一个间隔，间隔相比于K循环就是1:2。那么从相对的比例上看，依旧是M = N = 8192的间隔占比更多，提速比例应该更大。
</pasted_content id="b992">

---

**021 · 助手** · `2026-10-11T13:34:50.146Z` · `msg-417f13a73bd6e210f098`

图解页已经写好并通过了脚本检查，现在发布，并存一份到仓库。

---

**022 · 助手** · `2026-10-11T13:37:55.833Z` · `msg-0f3addffb3ed4fc20de1`

复查两问都答对了。先给评语，再进入节点 3。

## 复查评语

- **第 1 问正确**：K = 128 一端的提速比例更大。K 循环变短，tile 之间的固定间隔不变，间隔的占比就上去了。
- **第 2 问正确**：M = N = 8192 更大。你中途从“间隔的绝对数量”改成比较比例，这一步改得对。31/32 和 1/2 正好是“被省掉的发射占全部发射的比例”。

有一处用词要收紧。你说“持久化主要优化 prologue 和 epilogue”，其实间隔里有四样东西，持久化本身只消掉其中一样：

| 间隔里的成分 | 只加持久循环 | 再加 `flatten` |
| --- | --- | --- |
| CTA 的退出与发射 | 省掉，每个 SM 只付一次 | — |
| prologue 的计算（坐标、偏移、清零） | 还在 | 还在，但提前到上一个 tile 的尾部执行 |
| 等第一批数据 | 还在 | 省掉 |
| epilogue（转 fp16、写回） | 还在 | 还在，但这时下一个 tile 的数据已经在路上 |

第二列就是节点 3 要讲的。

## 节点 3：`flatten` 与跨 tile 的流水

**图解页**：[持久化矩阵乘时间线](https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW)，仓库里有一份离线副本 [persistent-matmul-timeline.html](docs/triton-learning/attachments/09-persistent-matmul/persistent-matmul-timeline.html)。建议先打开它的“时间线”一节，把三种写法各点一遍，再往下读。

**对应教程**：[持久版 kernel 的第 305–343 行](docs/triton-tutorials/official/09-persistent-matmul.py#L305-L343)，重点是第 307、312、333–334 行；还有描述符版[第 538–543 行](docs/triton-tutorials/official/09-persistent-matmul.py#L538-L543)的注释。看完图解页再读。

**结论**：`flatten=True` 请编译器把“tile 循环套 K 循环”合成一个循环。流水只在一个循环内部生效，所以合并前每个 tile 都要重新预热；合并后整个 CTA 只预热一次，下一个 tile 的头两轮读入在当前 tile 的最后两轮乘加期间就发出去了。

### 两个前置概念

图解页第一节用 C 写出了这两件事，这里只说要点。

- **流水只管一个循环。** `num_stages = 3` 的意思是读入比乘加提前两轮。循环一结束，在路上的东西清空；下次再进这个循环，要重新发两轮读入并等第一轮到达。
- **循环合并是加一个计数器。** 用 T 记住“现在是这个 tile 的第几轮”。T 为 0 时顺手做外层开头的事，T 到末尾时做外层结尾的事：

```c
T = 0; i = -1;
for (it = 0; it < tiles * n; it++) {
    if (T == 0)     { i++; prologue(i); k = 0; }
    body(i, k); k++;
    if (T == n - 1) epilogue(i);
    T = (T == n - 1) ? 0 : T + 1;
}
```

这正是 Triton 的合并 pass 生成的形式，我在编译器输出里核对过。

### 合并之后，一次迭代里有两个 tile

流水把“为两轮之后做准备”和“做本轮的计算”放进同一次迭代。到了 tile 的末尾，这两件事分属不同的 tile。取 n = 4、S = 3，看 tile i 和 i+1 交接处：

| 迭代 | 先为两轮之后做准备 | 本轮乘加 | 发出读入 | 收尾 |
| --- | --- | --- | --- | --- |
| i 的第 1 轮 | — | tile i | tile i 的第 3 轮 | — |
| i 的第 2 轮 | tile i+1 的 prologue | tile i | tile i+1 的第 0 轮 | — |
| i 的第 3 轮 | — | tile i | tile i+1 的第 1 轮 | tile i 的 epilogue |
| i+1 的第 0 轮 | — | tile i+1 | tile i+1 的第 2 轮 | — |

中间两行里，同一次迭代的前半段在为下一个 tile 做准备，后半段还在处理当前这个。

这解释了教程里那个看起来多余的计数器 `tile_id_c`：

- `tile_id` 是 prologue 的游标，会被提前推进。
- epilogue 写回时如果还用 `tile_id` 算坐标，就写到下一个 tile 去了。
- 所以 epilogue 自己维护一个 `tile_id_c`，收尾时才前进。这和环形缓冲区里读指针、写指针分开走是一回事。

我试过去掉 `tile_id_c`，让 epilogue 直接用 prologue 算好的坐标。在 v3.7.1 上三代目标都能编译，由编译器自己把那几个值多保留两轮。教程注释说 Blackwell 的流水在这种写法上有 bug，只编译无法判断那个 bug 是否存在。

### 编译产物里看到的变化

条件是贯穿案例、sm_89、B 按教程的传法。

- **不合并**：每个 tile 的 K 循环前有两轮异步拷贝，循环后有一次排空。本例一个 CTA 做 32 个 tile，就是 32 次预热。
- **合并**：这两处各只出现一次，在整个循环的前后。

### 代价

主要代价是共享内存，多出 32,768 字节：

| 目标 | `flatten` 关 | `flatten` 开 | 每个 CTA 的上限 |
| --- | --- | --- | --- |
| sm_89 | 65,536 | 98,304 | 101,376 |
| sm_90 | 98,304 | 131,072 | 232,448 |

多出来的这块是 epilogue 的中转区：

- epilogue 要把累加器从张量核心的布局换成写回用的布局，这一步借共享内存做中转。
- 不合并时，输入缓冲这时已经用完，中转可以借它们的地方。
- 合并后，下一个 tile 的读入已经在途，输入缓冲借不了，只能另开一块。

本例的中转正好是一个 fp16 输出块的大小（128 × 128 × 2）。这不是固定规律，别的块或 warp 数下编译器会分批转换，中转更小。

寄存器基本不变，sm_89 上每线程是 166 个对 160 个。

### 它没有解决什么

`flatten` 消掉的是等待，不是 epilogue 本身。转换和写回仍由同一批 warp 执行，这段时间张量核心还是空的。要把这一段也叠起来，得让不同的 warp 分工，这是节点 5 的 warp 专用化。

CUTLASS 的 Ping-Pong 设计做的是同一件事的另一种版本：两组 warp 各算一个 tile，让一组的 epilogue 和另一组的乘加重叠。来源是 CUTLASS v3.9.2 的 `efficient_gemm.md`。

### 边界

- **只认最简单的嵌套**：一个外层 `for` 里正好套一个内层 `for`。
- **内层次数不能随外层变化**。合并后的总迭代数是“tile 数 × 每个 tile 的轮数”，轮数必须是同一个值。
- **它是请求，不是保证**。我把 K 循环次数改成随 tile 变化，`flatten=True` 被忽略，产物和不写它完全相同，没有报错也没有警告。
- **Hopper 上不能和 warp 专用化同时用**，教程第 592 行因此把它关掉。
- **v3.7.1 的一个边界**：B 按普通的行主序 `[K, N]` 存放时，合并后 B 会从异步拷贝变成同步读入。教程 benchmark 传的是 `b.T`，不受影响。

## 检查题

条件按贯穿案例：sm_89、块 128×128×64、8 个 warp、B 按教程的传法。

1. **诊断**。你在自己的 kernel 上加了 `flatten=True`，没有任何报错。不跑性能测试，只看编译产物，举出两样能判断它是否真的生效的东西。为什么“没有报错”不能当作证据？
2. **取舍**。实测发现读入延迟偏长，想把流水从 3 个 stage 加到 4 个。已知 sm_89 上输入缓冲是每个操作数 S−1 个槽，每个槽 16,384 字节，中转区 32,768 字节，上限 101,376 字节。
   - (a) `flatten` 版的共享内存会变成多少？会发生什么？
   - (b) 不换硬件，给出两种能让 4 个 stage 放得下的办法，并说出各自放弃了什么。
3. **迁移**。上一课的 grouped GEMM kernel 是三层：外层 `for` 遍历问题，中间 `while` 领取 tile，最里层是 K 循环，各问题的 K 不同。给它加 `flatten=True` 能得到跨 tile 的流水吗？说出两条理由。

---

**023 · 用户** · `2026-10-11T13:40:04.135Z` · `msg-a8451f823c64658c70cf`

> command: /compact

---

**024 · 用户** · `2026-10-11T13:45:05.426Z` · `msg-63a6ec704ada9d30b178`

对了，我估计会采用NVIDIA GeForce RTX 4070 Laptop GPU来进行实测。这个可以吗？如果不行，我再去找其他的，我还可以找到5090和4090来测。

---

**025 · 助手** · `2026-10-11T13:51:24.976Z` · `msg-5848f7bf48148766ac5d`

核对完了：这台卡的规格、教程脚本在它上面会跑哪些版本、以及 Triton 读取设备上限的接口。现在把设备安排记进课程记录，然后给你答复。

---

**026 · 助手** · `2026-10-11T13:52:37.134Z` · `msg-9bce3bc6f15946dfb580`

**可以，主测量和练习都用它。** 不必为这节课另找设备。

## 为什么够用

- **它是 sm_89。** NVIDIA 的列表把 RTX 4070 归在 compute capability 8.9（列表不区分桌面和笔记本型号）。这正是贯穿案例和图解页用的目标，前面讲过的编译证据在它上面直接适用：`cp.async` 加 `mma.sync`，每个 CTA 的共享内存上限 99 KB。节点 3 第 2 题的结论，之后可以在它上面实际验证。
- **教程脚本在它上面正好测四个版本**：cuBLAS、`torch.matmul`、朴素版（逐 tile 发射）、持久版。capability 主版本小于 9 时，TMA、描述符和 warp 专用化的版本整个跳过，见教程[第 59–68 行](docs/triton-tutorials/official/09-persistent-matmul.py#L59-L68)和[第 662–678 行](docs/triton-tutorials/official/09-persistent-matmul.py#L662-L678)。本课的实测门槛只要求比较朴素版和持久版。
- **8 GB 显存足够。** 最大的张量是 8192 × 8192 的 fp16 矩阵，一个 128 MiB。

## 和课上示例不同的三处

1. **SM 数不是 128。** 公开规格是 4,608 个 CUDA 核心，按每个 SM 128 个核心推算是 36 个 SM。这是推算，要在设备上读一次。如果是 36，持久版只发射 36 个 CTA，每个连续处理 113 或 114 个 tile；课上的示例是 128 个 CTA、各 32 个 tile。
2. **测量波动要控制。** NVIDIA 给这个型号列的功耗范围是 35–115 W，boost 时钟 1230–2175 MHz，取决于具体机型和电源模式。教程的 `bench()` 对每个版本连跑 10,000 次预热加 10,000 次测量，测完一个才换下一个（[第 644–668 行](docs/triton-tutorials/official/09-persistent-matmul.py#L644-L668)）。笔记本持续满载时温度和频率可能漂移，各版本就不是在同一状态下测的。这是风险，不是我对你那台机器的结论。
   - 我写测量脚本时会让各版本分短轮次交替运行，并报告波动。
   - 你这边只需要插电、开性能模式、关掉其他占用 GPU 的程序。
3. **TMA 和 warp 专用化在它上面跑不了。** 节点 4–5 只能靠编译产物来讲。这两项本来就不在结课门槛里。

## 另外两张卡的用处

| 设备 | compute capability | 朴素版对持久版 | TMA、warp 专用化的实机运行 |
| --- | --- | --- | --- |
| RTX 4070 Laptop | 8.9 | 能测 | 教程脚本跳过 |
| RTX 4090 | 8.9 | 能测；同一组配置下生成的代码与上一行相同，只有 `NUM_SMS` 这个常数不同 | 教程脚本跳过 |
| RTX 5090 | 12.0 | 能测 | 教程脚本会运行；我只编译时看到了 TMA 指令和专用化后的 12 个 warp |

- **4090** 不带来新的机制。只有笔记本的波动大到分不出两个版本时，才值得换它。
- **5090** 是唯一能真跑 TMA 和 warp 专用化的。这属于可选观察，做不做由你定，学完节点 5 再决定也不迟。

## 上机时顺手做一件事

用那台机器上平时跑课程代码的 Python 执行下面这段，把输出贴回来。它读出我上面靠文档和推算得到的几个数。

```bash
python - <<'EOF'
import platform
import torch
import triton
from triton.runtime import driver

i = torch.cuda.current_device()
p = torch.cuda.get_device_properties(i)
t = driver.active.utils.get_device_properties(i)
print("GPU          :", p.name, f"({p.total_memory / 2**30:.1f} GiB)")
print("capability   :", torch.cuda.get_device_capability(i))
print("SM count     :", p.multi_processor_count)
print("shared limit :", t["max_shared_mem"], "bytes per CTA")
print("versions     :", "torch", torch.__version__, "| triton", triton.__version__)
print("kernel       :", platform.release())
EOF
```

- 预期是 capability `(8, 9)`、SM 数 36、共享内存上限 101376。有出入就以设备为准，我据此改后面的例子。
- `shared limit` 就是 Triton 判断“放不放得下”时比较的那个数。
- `kernel` 一行能看出是原生 Linux 还是 WSL2（WSL2 的版本号里带 `microsoft`）。NVIDIA 的 WSL 文档说 `nvidia-smi` 的部分查询在 WSL2 下不可用，proton 依赖的 CUPTI 列为预览支持。如果是 WSL2，我会让测量脚本不依赖这两样。

这段脚本我在本机只用替身数值试跑过格式，没有在真实 GPU 上跑过。设备安排已记入第 09 课的记录，未提交。

节点 3 的三道检查题照常作答，不必和这段输出一起交。

来源：[CUDA GPU Compute Capability](https://developer.nvidia.com/cuda/gpus)、[Compare GeForce RTX Laptops](https://www.nvidia.com/en-us/geforce/laptops/compare/)、[CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)。

---

**027 · 用户** · `2026-10-12T02:09:52.763Z` · `msg-74789a56f05937a4f538`

<pasted_content id="b992">
1. 可以从编译产物中查看prologue和epilogue的数量和共享内存相比之前是否有变化。如果真的生效了，那么prologue和epilogue的数量应该会显著减少，共享内存的使用量会增多。不能只看“没有报错”是因为flatten=True本身只是请求生成跨tile的流水，而不是强制要求的保证。当编译器无法实现跨tile的流水后，会自动回退到普通的循环上。
2. （a）那么就需要多两个输入缓冲槽（一个A，一个B）。输入缓冲变成一共需要6*16384，输出中转需要32768，一共需要131072字节。共享内存不够了，会溢出到显存，性能就更慢了；（b）第一种办法，可以减小块大小。通过减小块大小来减少缓冲和中转的需求量，从而减少对共享内存的占用。代价是增加了tile总工作数量。第二种办法，放弃flatten版的跨tile流水，回归到原始版本。此时就放弃了对prologue和epilogue的优化。
3. 对于这种情况，就不能加flatten=True得到跨tile的流水。因为跨tile流水要求每个tile的k循环轮数不变。此外grouped GEMM的内层是while，不是for，也不是简单的嵌套循环。
我有两个问题，那有没有办法改造grouped GEMM成可以跨tile流水呢？比如MoE中对于K方向维度应该是一样的，对于MoE的情形满足了K循环轮数一致。那么对于内层的while，能不能改成for呢？
第二，如何查看编译产物？我只会运行triton代码。我该怎么看triton编译出的东西在哪里？然后怎么看里面的prologue和epilogue和共享内存呢？
</pasted_content id="b992">

---

**028 · 助手** · `2026-10-12T02:23:26.712Z` · `msg-ef46cd8b1eb80906612a`

产物已按教程原文件重新生成（IR 里带教程行号）。现在提取骨架、核对本机可运行的查看步骤，然后更新图解页并写答复。

---

**029 · 助手** · `2026-10-12T02:30:01.477Z` · `msg-83569d55b4910af6f555`

页面的新内容已生成并通过了与真实产物的逐行核对。现在做脚本检查、发布，并更新仓库里的副本和课程记录。

---

**030 · 助手** · `2026-10-12T02:31:22.065Z` · `msg-2c8680b544c910ead2d1`

正在逐块查看新页面的截图，确认排版没有问题后就发布。

---

**031 · 助手** · `2026-10-12T02:32:25.001Z` · `msg-d188169dcb4f473b9dc7`

排版检查基本通过，再修一处代码连字（`<<` 被字体画成了 `≪`，会误导你敲命令），然后发布。

---

**032 · 助手** · `2026-10-12T02:34:58.072Z` · `msg-7e4d22c327b1f61de7da`

课程记录和 Checkpoint 已更新。最后补一条工作备忘，然后给你完整答复。

---

**033 · 助手** · `2026-10-12T02:36:48.712Z` · `msg-d565a7d32714d540e690`

三道题里有两处要改，其余都对。两个追问我都做了只编译的实验。下面先给评语，再讲怎样看产物，最后回答能否改造 grouped GEMM，因为它的证据要用前一节的方法来读。

## 检查题评语

**第 1 题：一半对。**

- 对的部分：共享内存会变多；“没有报错”不算证据，因为 `flatten` 只是请求，条件不满足时编译器不声不响地退回普通循环。
- 要改的部分：减少的不是 prologue 和 epilogue。有两组东西容易混：

| | 谁写的 | 做什么 | 不合并 | 合并后 |
| --- | --- | --- | --- | --- |
| tile 的 prologue | 你的源码 | 算坐标和偏移，累加器清零 | 每个 tile 一次 | 每个 tile 一次 |
| tile 的 epilogue | 你的源码 | 转 fp16，写回 C | 每个 tile 一次 | 每个 tile 一次 |
| 流水的预热 | 编译器加的 | 循环开始前先发出头两轮读入 | 每个 tile 一次 | 每个 CTA 一次 |
| 流水的排空 | 编译器加的 | 循环结束后等在途的读入到齐 | 每个 tile 一次 | 每个 CTA 一次 |

- `flatten` 只改变后两行。这个变化在产物里也不是“数量变少”，而是位置变了，下一节能看到。
- 这道题有我的问题：它要你从编译产物里找证据，可我没教过怎样看产物。

**第 2 题 (a)：算术对，后果要改。**

- 131,072 字节算得对。
- 共享内存没有“溢出到显存”这条退路。Triton 把 kernel 装上 GPU 之前，先拿这个数和设备上限比较，超了就抛 `OutOfResources`，kernel 不会运行。
- 在 autotune 里更隐蔽：异常被捕获，这个配置的耗时记成无穷大，默认什么都不打印。
- “放不下就溢出、变慢”是寄存器的行为：寄存器不够时，一部分值被放到每线程的本地内存，kernel 照样能跑。Triton 加载后读回的 `n_spills` 就是它。

**第 2 题 (b)：对。** 关掉 `flatten` 后是 98,304 字节，放得下。补一点：把 `BLOCK_K` 从 64 减到 32 不增加 tile 数，只让 K 循环轮数翻倍；减 `BLOCK_M`、`BLOCK_N` 才增加 tile 数。

**第 3 题：对。** 其中“K 循环轮数要相同”这一条，是我上一节说得太绝对，放在第三部分更正。

## 怎样查看编译产物

图解页新增了“查看产物”一节：[持久化矩阵乘时间线](https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW)，[仓库副本](docs/triton-learning/attachments/09-persistent-matmul/persistent-matmul-timeline.html)同步更新。里面有读 TTGIR 要认得的几个词、两份真实产物的骨架对照和原文。这里只说要点。

**产物从哪里拿**

| 途径 | 怎么做 | 什么时候用 |
| --- | --- | --- |
| 调用的返回值 | `k = my_kernel[grid](...)`，返回的就是编译结果 | 自己写的 kernel；要在 GPU 上运行 |
| 缓存目录 | 默认在 `~/.triton/cache/`，每种特化一个子目录；运行前设 `TRITON_CACHE_DIR=/tmp/t09` 指到空目录 | 不改代码，例如直接跑教程脚本 |
| 只编译不运行 | `triton.compile(ASTSource(...), target=GPUTarget("cuda", 89, 32))` | 没有 GPU，或想看别的硬件代际 |

这些接口仓库里已经用过：第 02 课读了 `n_regs` 和 `metadata.shared`（[lesson02_fused_softmax.py:17-18](gpu/triton/lesson02_fused_softmax.py#L17-L18)），第 08 课的测试用的是第三条（[lesson08_grouped_gemm_test.py:531-535](gpu/triton/lesson08_grouped_gemm_test.py#L531-L535)）。

**每个文件回答什么**

| 文件 | 是什么 | 用来回答 |
| --- | --- | --- |
| `.ttir` | 源码逐句翻成的张量运算，还没做硬件相关的决定 | 源码被理解成了什么 |
| `.ttgir` | 做完 GPU 相关决定之后的版本 | 流水有没有生效，循环有没有合并，预热和排空在哪里 |
| `.ptx` | NVIDIA 的汇编，相当于 `gcc -S` 的输出 | 最终用了哪些指令 |
| `.json` | 这次编译的元数据 | `shared` 就是共享内存字节数 |

**现在就能试，不需要 GPU。** 在仓库根目录、课程的 Python 环境里运行。它把你第 08 课的 kernel 按 sm_89 编译，写出三个阶段的文本，再列出骨架：

```bash
python - <<'PY'
import pathlib
import triton
from triton.backends.compiler import GPUTarget
from triton.compiler import ASTSource
from gpu.triton.lesson08_grouped_gemm import grouped_matmul_kernel

signature = {"group_a_ptrs": "*i64", "group_b_ptrs": "*i64", "group_c_ptrs": "*i64",
             "group_gemm_sizes": "*i32", "g_lds": "*i32", "group_size": "i32"}
constexprs = {"NUM_SM": 36, "BLOCK_SIZE_M": 128, "BLOCK_SIZE_N": 128, "BLOCK_SIZE_K": 64, "RAGGED_NK": False}
k = triton.compile(ASTSource(fn=grouped_matmul_kernel, signature=signature, constexprs=constexprs),
                   target=GPUTarget("cuda", 89, 32), options={"num_stages": 3, "num_warps": 8})
print("shared memory:", k.metadata.shared, "bytes")
out = pathlib.Path("/tmp/lesson08-sm89")
out.mkdir(parents=True, exist_ok=True)
for ext in ("ttir", "ttgir", "ptx"):
    (out / f"grouped.{ext}").write_text(k.asm[ext])
print("written:", sorted(p.name for p in out.iterdir()))
PY
grep -n "scf\.\(for\|while\|if\)\|ttg\.local_alloc\|ttg\.async_copy_global_to_local\|ttg\.async_wait\|tt\.dot\|ttg\.convert_layout\|tt\.store" \
    /tmp/lesson08-sm89/grouped.ttgir | cut -c1-96
```

我在本机跑过，输出 `shared memory: 65536 bytes`。骨架整理如下，左边是 `.ttgir` 里的行号，右边的说明是我加的：

```text
 38       scf.for                      问题循环
 62         scf.while                  领取 tile
112–113       ttg.local_alloc ×2       A、B 的缓冲，各 2 个槽
126 · 130     ttg.async_copy… ×2       预热：第 0 轮
146 · 150     ttg.async_copy… ×2       预热：第 1 轮
152           scf.for                  K 循环
158             ttg.async_wait {num = 2}
163             tt.dot
184 · 188       ttg.async_copy… ×2     为两轮之后发出读入
192           ttg.async_wait {num = 0} 排空
198           ttg.convert_layout       epilogue
199           tt.store                 epilogue
```

缩进就是嵌套，和 C 的花括号一样。`async_wait {num = 0}` 表示把在途的读入全部等完，也就是排空。

**教程 kernel 的对照**（完整骨架在页面上）

| | `flatten` 关 | `flatten` 开 |
| --- | --- | --- |
| `.json` 的 `shared` | 65,536 | 98,304 |
| `scf.if` | 0 处 | 4 处 |
| `async_copy` 与 `async_wait` 的出现次数 | 6 处、2 处 | 6 处、2 处 |
| 预热的位置 | tile 循环里面 | 合并后的循环之前 |
| 排空的位置 | tile 循环里面（第 190 行） | 合并后的循环之后（第 335 行） |
| epilogue 的位置 | tile 循环里面 | 合并后的循环里面，在一个 `scf.if` 中 |

所以第 1 题的两样证据是：`shared` 是否多了一块；TTGIR 里有没有 `scf.if`，预热和排空是否移到了循环外面。数出现次数分不出来。

## 能不能把 grouped GEMM 改成跨 tile 流水

**能。你抓的两点都对，但只把 `while` 换成 `for` 不够。** 我以你第 08 课的实现为底，改写循环形状做了只编译实验。条件是 sm_89、块 128×128×64、3 个 stage、8 个 warp。

| 写法 | 循环的形状 | 加 `flatten=True` 之后 | 共享内存 |
| --- | --- | --- | --- |
| ① 你现在的写法 | `for` 问题 → `while` → `for` K | 没有变化 | 65,536 |
| ② 只把 `while` 换成 `for` | 三层 `for` | 没有变化 | 65,536 |
| ③ 一个 `for` 遍历本 CTA 的全部 tile，问题号查表；K 是共用的标量 | 两层 `for` | 合并了，但 B 退回同步读入 | 65,536 |
| ④ 同 ③，行列偏移挪到 K 循环里算 | 两层 `for` | 合并，A、B 都是异步拷贝 | 98,304 |

原因在编译器找循环的规则，出自 `FuseNestedLoops.cpp`：

- **只合并正好两层的嵌套。** 带 `flatten=True` 的 `for` 在最外层，里面正好一个 `for`。② 是三层，所以不行。
- **遇到 `while` 或 `if` 就停下**，里外各算一组。① 因此不行。

所以要让“本 CTA 的全部 tile”成为唯一的外层 `for`。这就是教程 09 持久版的那个循环：从 `pid` 起，步长 `NUM_SM`，到所有问题的 tile 总数为止。

原来的 `for` 加 `while` 是在回答“这个全局 tile 号属于哪个问题”。现在这个回答不能再用循环，要换成一次查表：主机预先建一张“tile 号 → 问题号”的表。上一课讲过的 CUTLASS `kHostPrecompute` 调度模式就是这个做法。

MoE 的条件在这里起作用：K 相同，就能作为一个标量参数传进来，K 循环的次数在进入 tile 循环之前就定了。

**还要一起带上的三件事**

- epilogue 要有自己的游标，并再查一次表。道理和 `tile_id_c` 相同。
- 行列偏移放在 K 循环里算。③ 和 ④ 的差别就在这里，是上一节说的 v3.7.1 的那个边界。
- 代价：共享内存多 32,768 字节，主机多建一张表，每个 tile 多几次读表。

**更正我上一节的一句话。** 我说“内层的次数不能随外层变化”，说得太绝对。

- 准确的说法：默认要求它在进入外层之前就能算出来。
- v3.7.1 另留了一条路：用 `tl.assume` 向编译器保证 K 循环至少执行一次，并且次数只由外层循环变量经标量运算得到。这时编译器先用一个小循环把总迭代数加出来，再合并。
- 我验证过：K 逐问题不同时，不加 `tl.assume` 被忽略（65,536），加了就合并（98,304）。

所以 K 不同的 grouped GEMM 也不是没有办法。你第 3 题是按我当时讲的答的，不算你的错。

**边界。** 以上都是只编译看到的结构，没有在设备上验证数值，也没有测性能。值不值得做要实测：K 循环越长，省下的那一段占比越小，这是你上次自己推出来的；MoE 的 K 是隐藏维度，一个 tile 往往有几十轮。

这个改造很适合当本课的练习题目。到约定练习时由你决定，所以我没有给出代码。

## 复查（两问）

1. **读产物。** 用上面第 08 课 kernel 的骨架，假设某个 CTA 一共领到 20 个 tile。
   - (a) 预热（第 126–150 行）、排空（第 192 行）、epilogue（第 198–199 行）各执行多少次？依据是骨架里的什么？
   - (b) 改成写法 ④ 并且合并生效后，这三样的次数各是多少？
   - (c) 用一句话说：`flatten` 省掉了什么，没省掉什么。
2. **诊断。** 同事在一台 sm_89 的机器上，给教程的配置表加了 `num_stages=5`。autotune 跑完没有任何报错，选出的最优配置和原来一样。他的结论是“5 个 stage 在这台机器上没有收益”。
   - (a) 这个结论为什么站不住？按本例的块，算出朴素版和持久版在 5 个 stage 时各要多少共享内存。
   - (b) 这些配置在 autotune 里实际经历了什么？你会让他看什么来确认？

课程记录和 Checkpoint 已更新，都还没有提交。

---

**034 · 用户** · `2026-10-12T03:35:00.531Z` · `msg-e5feb6595b04c0e46bd9`

1. (a)预热跟着tile while循环，是tile数量次，一共20次；排空和epilogue也是tile循环，一共20次。（b）改成合并生效后，预热和排空应该就只剩下各自1次，epilogue写回则依旧跟着tile数量走，需要20次。（c）flatten可以省掉在tile循环间隔中的预热和排空，但不能省掉写回epilogue。
2. 因为stage开了5有可能实际上是共享内存不够而报错了，但因为开了autotune，吞掉了报错。autotune实际上根本没跑stage=5的情况。我不知道你讲的本例是哪个例子。假设就是前一个问题的缓冲槽计算的例子，那么就需要4*2*16384+32768=163840字节。如果去掉flatten，则也需要131072字节。（b）这些配置实际很可能报错了，我会让他看这个配置的耗时是不是被记成了无穷大来确认。

---

**035 · 助手** · `2026-10-12T03:36:21.373Z` · `msg-33a499338c34f3f7990b`

复查两问都过了，稍后给评语。按路线接下来是节点 4（TMA 与两种描述符），我先核对教程源码、PTX 文档和已有的编译产物，再开讲。

---

**036 · 助手** · `2026-10-12T03:38:04.460Z` · `msg-23d8912074b6409c4b81`

还在核对 PTX 文档里关于 TMA、`wgmma` 和 `tcgen05` 的原文定义，马上进入编译对照。

---

**037 · 助手** · `2026-10-12T03:41:09.973Z` · `msg-7809c53b272fa4d7558b`

证据已经齐了：四代目标上“谁搬数据、谁取操作数、累加器放哪”的编译对照都核对过。现在画节点 4 的图解并写讲解。

---

**038 · 助手** · `2026-10-12T03:44:36.632Z` · `msg-a0fdbf90e8942184a8f2`

正在核对图解在不同目标下的切换效果，确认无误后发布并写节点 4 的讲解。

---

**039 · 助手** · `2026-10-12T03:47:23.377Z` · `msg-fe0574f2b0b866a802b9`

复查两问都通过了。先给评语，再进入节点 4。

## 复查评语

- **第 1 问全对。** 预热、排空、epilogue 都在 tile 循环里面，各 20 次；合并后预热和排空各 1 次，epilogue 仍是 20 次。你那句总结也准确。
- **第 2 问对。** 163,840 和 131,072 都超过 101,376，所以不是“可能”报错，而是这些配置一定没有运行过。
- **“看耗时是不是无穷大”有三个现成的入口：**
  - `matmul_kernel_persistent.configs_timings`：autotune 跑完后，每组配置的耗时都在这个字典里。
  - 运行前设 `TRITON_PRINT_AUTOTUNING=1`：失败的配置会打印 `Autotuning failed with out of resource: shared memory…`。
  - 上一节的办法：看缓存目录里那组配置的 `.json` 的 `shared`。
- **“本例”是我没写清楚。** 它指课上一直用的那组设置，我应当每次写全。下面先把它列出来。

## 节点 4：谁在搬数据，谁在算

**本节的例子**

- A 是 `[M, K] = [8192, 512]`，B 是 `[K, N] = [512, 8192]`，都是 fp16。
- 块是 `BLOCK_M × BLOCK_N × BLOCK_K = 128 × 128 × 64`。一个 A 块或 B 块是 16,384 字节，累加器是 128 × 128 的 fp32。
- `num_stages = 3`，`num_warps = 8`，一个 CTA 有 256 个线程。
- 所有数字来自只编译，没有实机结果。

**图解页**：[持久化矩阵乘时间线](https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW)最后新增了“搬与算”一节，[仓库副本](docs/triton-learning/attachments/09-persistent-matmul/persistent-matmul-timeline.html)同步更新。建议先把四个目标、两种写法各点一遍，再读代码。

**对应教程**

- [第 183–270 行](docs/triton-tutorials/official/09-persistent-matmul.py#L183-L270)：主机侧描述符的 kernel `matmul_kernel_tma`，以及它的 `pre_hook` 和包装函数。
- [第 495–570 行](docs/triton-tutorials/official/09-persistent-matmul.py#L495-L570)：设备侧描述符的 kernel `matmul_kernel_descriptor_persistent`。
- [第 59–68 行](docs/triton-tutorials/official/09-persistent-matmul.py#L59-L68)：哪些设备上才运行这些版本。

**结论**：一轮 K 循环里，通用线程原本有三件事要做：算地址把数据搬进共享内存，把操作数从共享内存取进寄存器，在寄存器里攒累加器。从 sm_89 到 sm_100，硬件把这三件事一件件接走。源码几乎不变，由编译器按设备选指令。

### 四个要用到的名词

| 名词 | 是什么 |
| --- | --- |
| TMA | 第 08 课见过：一条指令搬一整块，地址由硬件按描述符去算 |
| 屏障（`mbarrier`） | 共享内存里的一个计数器。发起搬运前登记“要等多少字节”，硬件搬完自动记账，线程等它清零。可以当成带计数的条件变量 |
| warpgroup | 4 个相邻的 warp，共 128 个线程。sm_90 的乘加指令以它为单位执行 |
| TMEM | 张量核心专用的片上存储，只有 sm_100 有。每个 CTA 有 512 列 × 128 行，每格 32 位 |

### 同一轮 K 循环，在四个目标上

| 写法 | 目标 | 搬入 | 操作数 | 乘加 | 累加器 | 寄存器 | 共享内存 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 指针版 `matmul_kernel` | sm_89 | `cp.async` 24 条 | 经寄存器 | `mma.sync` 64 条 | 寄存器 | 135 | 65,536 |
| | sm_90 | `cp.async` 24 条 | 直接读共享内存 | `wgmma` 4 条 | 寄存器 | 111 | 98,304 |
| | sm_100 | `cp.async` 32 条 | 直接读共享内存 | `tcgen05.mma` 8 条 | TMEM | 94 | 98,320 |
| | sm_120 | `cp.async` 24 条 | 经寄存器 | `mma.sync` 64 条 | 寄存器 | 158 | 65,536 |
| 描述符版 `matmul_kernel_tma` | sm_89 | 逐元素同步读 64 条 | 经寄存器 | `mma.sync` 64 条 | 寄存器 | 255 | 32,768 |
| | sm_90 | TMA 7 条 | 直接读共享内存 | `wgmma` 4 条 | 寄存器 | 90 | 98,328 |
| | sm_100 | TMA 9 条 | 直接读共享内存 | `tcgen05.mma` 8 条 | TMEM | 71 | 98,352 |
| | sm_120 | TMA 7 条 | 经寄存器 | `mma.sync` 64 条 | 寄存器 | 118 | 65,552 |

sm_89 是你的 4070 Laptop 和 4090，sm_120 是 5090。

### 三件事各是怎样被接走的

**一、搬入：TMA 接走了算地址和发指令。**

- `cp.async` 一条搬 16 字节。一个 16,384 字节的块，要 256 个线程各发 4 条，每个线程自己算地址。
- TMA 由选出的一个线程发一条 `cp.async.bulk.tensor.2d`，硬件按描述符里的形状和步长算地址。
- 线程用屏障等数据到齐。产物里登记的字节数是 32,768，正好是 A、B 各一块。
- 搬运只需要一个线程，这为下一节的 warp 专用化铺了路。

**二、取操作数：新的乘加指令直接读共享内存。**

- sm_89 的 `mma.sync` 要求操作数在寄存器里，所以线程先用 `ldmatrix` 把 A、B 取出来。
- sm_90 的 `wgmma` 直接从共享内存读，这一步消失。
- 指令也变粗了：`mma.sync` 一条算 16 × 8 的一小片，每个 warp 每轮发 64 条；`wgmma` 一条算 64 × 128，每个 warpgroup 每轮 4 条。
- 代价是共享内存。乘加是异步的，正在被读的槽在算完之前不能被下一轮覆盖，所以每个操作数要 3 个槽，65,536 变成 98,304。

**三、累加器：TMEM 接走了它。**

- sm_100 的 `tcgen05.mma` 由一个线程发起，累加器放在 TMEM 里。
- 它占 128 列：128 列 × 128 行 × 4 字节 = 65,536 字节，和本例累加器的大小相同。
- 线程只在 epilogue 把结果读回来。

寄存器数是这条线索的直接证据：指针版是 135、111、94；描述符版在 sm_90 和 sm_100 上是 90 和 71。

**sm_120 是混合的**：搬运用上了 TMA，计算仍是 `mma.sync`，操作数和累加器还在寄存器里。

### 两种描述符

| | 主机侧 `TensorDescriptor.from_tensor` | 设备侧 `tl.make_tensor_descriptor` |
| --- | --- | --- |
| 谁来建 | Python 包装函数，发射前由驱动填好 | 每个 CTA 在 kernel 开头自己填，每个描述符 13 条 `tensormap.replace` |
| 块形状 | 建描述符时就要给；autotune 每试一组配置，由 `pre_hook` 改写（教程第 183–193 行） | 源码里的编译期常量 |
| 额外开销 | 无 | 每个描述符 128 字节的全局暂存，要先 `triton.set_allocator` |
| 能描述 | 发射前就确定的一个张量 | 运行中才知道的张量，例如 grouped GEMM 每个问题各自的矩阵 |
| 没有 TMA 时 | 逐元素同步读写，寄存器 255 个 | 改写成普通指针读写，仍是 24 条 `cp.async` |

### 没有 TMA 时，为什么两种描述符退得不一样远

差别在编译器还能看见什么。

- **主机侧**描述符在 sm_89 上被展开成十一个运行时参数：基地址、形状、步长等。基地址不带对齐保证，步长是运行时才知道的数。编译器无法确认“连续、对齐的 16 字节一组”，只能逐元素同步读写。
- **设备侧**描述符的 kernel 里，指针参数带着对齐保证，步长 `[K, 1]` 写在源码里。编译器把它改写成普通的指针读写，照样生成 `cp.async`。

这和节点 3 那个边界是同一个道理：编译器看不见的信息，就当它不成立。教程脚本本身不会走到这里，它只在 capability 主版本不小于 9 的设备上运行描述符版。

### 关于 `b.T`

描述符版要求 B 按 `[N, K]` 存放，kernel 里写的是 `tl.dot(a, b.T, accumulator)`。我编译了一个 B 按 `[K, N]` 存放、不转置的副本：

- sm_90 和 sm_100 上指令构成完全相同。
- sm_120 上多出转置读取，寄存器是 159 对 118。

教程为什么选 `[N, K]`，源码里没有说明，我不下结论。

## 检查题

条件同本节开头的例子。

1. **诊断。** 你的 4070 Laptop 是 sm_89。同事建议去掉教程里对设备的判断，直接在这台机器上运行 `matmul_kernel_tma`，理由是“代码更短，没有指针运算，至少不会比指针版慢”。
   - (a) 用编译结果反驳：这时数据是怎样读进来的，和指针版差在哪？
   - (b) 为什么编译器这次生成不了 `cp.async`？
   - (c) 如果一定要在 sm_89 上保留描述符的写法，教程里哪个 kernel 的退路更好，好在哪里？
2. **设计取舍。** 各举一个场景：什么时候只能用设备侧描述符，什么时候主机侧更合适。设备侧多付出的两样东西是什么？
3. **解释两个数字。**
   - (a) 描述符版在 sm_90 上每线程 90 个寄存器，在 sm_120 上是 118 个。两者都用了 TMA，多出来的寄存器装的是什么？
   - (b) 指针版从 sm_89 换到 sm_90，少了“把操作数取进寄存器”这一步，共享内存却从 65,536 涨到 98,304。为什么？

图解页已更新到第 4 版，课程记录和 Checkpoint 也已更新，都还没有提交。

---

**040 · 用户** · `2026-10-12T06:30:09.106Z` · `msg-be81441543026ea04bf5`

指令的粒度变化可以再讲细一点吗？mma.sync 一条算 16 × 8 的一小片是指的m=16，n=8吗？还有wgmma和tcgen05.mma 的。关于选 [N, K]，我记得有两点，一个是上节课讲可以使得读取B的block时按照K方向连续进行读取，另一个是fp8类型中我记得似乎要求B需要是转置的形状。
检查题中1. （a）对sm_89的编译结果中可以看到，此时数据的读取方式会从cp.async变成是逐元素同步读取，相比指针版的cp.async异步读取存在回退。（b）因为主机侧描述符在 sm_89 上被展开成十一个运行时参数，地址参数没有连续和对齐保证，就会变成逐元素同步读。（c）如果一定要在sm_89上保留描述符，可以采用设备侧描述符。教程中matmul_kernel_descriptor_persistent就用了这种写法，在设备侧对指针进行描述符化。2. 当我们进行autotune时，就需要主机侧描述符化，比较方便。对于编译期发射时还不确定的张量，比如grouped GEMM 每个问题各自的矩阵，这种就只能设备侧进行描述符化。设备侧描述符化需要多出一些tensormap.replace指令和每个描述符 128 字节的全局暂存的代价。3. （a）sm_90的wgmma的操作数可以直接读共享内存，而不经过寄存器；sm_120需要经寄存器。所以多出的寄存器应该是用来装矩阵乘指令的输入数据了；（b）这个问题我不太清楚。我估计一下，之前我也问到矩阵乘指令的粒度变化，我估计这是因为wgmma一条算的东西更大了，使得需要在共享内存上准备的输入数据和输出空间更多了。

---

**041 · 助手** · `2026-10-12T06:34:39.164Z` · `msg-66970acdb093f6f73d97`

三问里有两处要补，其余都对。你记得的两点理由我核对过了，都成立，我之前说“不下结论”应当更正。下面依次是：你的两个问题、检查题评语、复查。

图解页的“搬与算”一节补了三块内容，和下面对应：[持久化矩阵乘时间线](https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW)，[仓库副本](docs/triton-learning/attachments/09-persistent-matmul/persistent-matmul-timeline.html)同步更新。

## 指令的粒度

**是的，`m16n8k16` 就是 M = 16、N = 8、K = 16。** 一条指令完成 D[M × N] += A[M × K] · B[K × N]。

下面的例子和上一节相同：一个 tile 的输出是 128 × 128，一轮 K 循环是 `BLOCK_K = 64`，8 个 warp。

| 指令 | 一条算什么 | 谁来执行 | 本例一轮要几条 | 操作数在哪 | 结果在哪 |
| --- | --- | --- | --- | --- | --- |
| `mma.sync` `m16n8k16` | D[16 × 8] += A[16 × 16] · B[16 × 8] | 一个 warp，同步 | (128 ÷ 16) × (128 ÷ 8) × (64 ÷ 16) = 512 次，8 个 warp 各 64 条 | 寄存器 | 寄存器 |
| `wgmma.mma_async` `m64n128k16` | D[64 × 128] += A[64 × 16] · B[16 × 128] | 一个 warpgroup（4 个 warp），异步 | (128 ÷ 64) × (64 ÷ 16) = 8 次，两个 warpgroup 各 4 条 | 共享内存 | 寄存器 |
| `tcgen05.mma` `kind::f16` | 本例是 D[128 × 128] += A[128 × 16] · B[16 × 128] | 一个线程发起，异步 | 64 ÷ 16 = 4 条 | 共享内存 | TMEM |

- **三条指令的 K 都是 16**，变的是一条指令覆盖的输出面积：16 × 8，64 × 128，128 × 128。
- **`tcgen05.mma` 的形状不写在名字里**，由指令的一个描述参数给出。我是从编译产物里读到 128 × 128 的。
- **面积越大，线程手里要拿的东西越少。** `mma.sync` 的每个线程要拿 A 的 8 个元素、B 的 4 个元素和 4 个累加值；`tcgen05.mma` 的线程什么都不用拿。
- **“同步”和“异步”的区别**：`mma.sync` 返回时已经算完；后两条发出后立刻返回，要另行等待完成。这一点决定了下面第 3 题 (b) 的答案。

## B 为什么按 [N, K] 存放

你记得的两点都对。

- **沿 K 方向连续。** 描述符要求最后一维连续。按 `[N, K]` 存，取出的 B 块在内存里就是沿 K 连续的，这正是乘加指令默认要的摆法。
- **fp8 没有转置这个选项。** PTX 文档规定，`wgmma` 的转置参数只支持 fp16 和 bf16。
  - fp16 时 B 按 `[K, N]` 存也行，指令带一个转置标志就够。这解释了我上次的实验为什么看不出差别：我只编了 fp16。
  - fp8 时编译器只能先把 B 取进寄存器，重排后再存回共享内存。

我补做了 fp8 的编译对照（sm_90，描述符版）：

| B 的存法 | 每线程寄存器 | 多出的指令 |
| --- | --- | --- |
| `[N, K]`，kernel 里写 `b.T`（教程的写法） | 90 | 无 |
| `[K, N]`，不转置 | 113 | 32 条逐字节写共享内存 |

教程要同时支持 fp16 和 fp8，所以统一按 `[N, K]` 存。

## 检查题评语

**第 1 题：对。** 三小问都成立。(c) 可以再补一句好在哪里：设备侧描述符的 kernel 在 sm_89 上仍是 24 条 `cp.async`，因为指针带着对齐保证，步长写在源码里。

**第 2 题：设备侧的部分对，主机侧的场景说反了。**

- 设备侧：发射时还不确定的张量只能用它，代价是 `tensormap.replace` 和全局暂存。这些都对。
- 主机侧并不是“autotune 时比较方便”，恰恰相反：
  - 主机侧描述符在 Python 里创建时就要给块形状，而这时还不知道 autotune 会选哪组配置。
  - 所以教程先用占位的 `[1, 1]` 建描述符，再靠 `pre_hook` 在每组配置运行前改写（[第 183–193 行](docs/triton-tutorials/official/09-persistent-matmul.py#L183-L193)、[第 253–257 行](docs/triton-tutorials/official/09-persistent-matmul.py#L253-L257)）。
  - 设备侧的块形状是源码里的编译期常量，每组配置自动各编一份，不需要钩子。
- 主机侧合适的场景是：张量在发射前就完全确定，例如普通的矩阵乘。好处是每个 CTA 不用自己填描述符，也不需要全局暂存和分配器。

**第 3 题 (a)：对。** sm_120 多出的寄存器装的是乘加的操作数。

**第 3 题 (b)：需要补。** 你说不太清楚，这样说比硬猜好。你的猜测方向不对：每轮搬进来的数据量没有变，都是 A、B 各一块；输出也不在共享内存里。变的是**一个槽要被占多久**。

取 `num_stages = 3`，看第 k 轮里发生的事：

| 步骤 | sm_89：先取走，再计算 | sm_90：就地读，边读边算 |
| --- | --- | --- |
| 1 | 等第 k 轮的数据到齐 | 等第 k 轮的数据到齐 |
| 2 | `ldmatrix` 把它取进寄存器，**这个槽空了** | 发出 `wgmma`，它直接读这个槽并立刻返回，**这个槽还在被读** |
| 3 | `mma.sync` 在寄存器上计算 | 发出第 k+2 轮的读入：第 k 轮的槽不能用，第 k+1 轮的槽里有数据，只能用第三个槽 |
| 4 | 发出第 k+2 轮的读入，写进刚空出来的槽 | — |
| 同时被占 | 第 k+1、k+2 两轮：2 个槽 | 第 k、k+1、k+2 三轮：3 个槽 |

所以共享内存是 2 × 2 × 16,384 = 65,536 对 3 × 2 × 16,384 = 98,304。少了一次“搬到寄存器”，换来的是槽被占得更久。

## 复查（两问）

例子同上一节：块 128 × 128 × 64，一个 A 块或 B 块 16,384 字节，`num_stages = 3`，8 个 warp。

1. **描述符与 autotune。** 教程给 `matmul_kernel_tma` 配了 `pre_hook`，给 `matmul_kernel_descriptor_persistent` 没配。
   - (a) 为什么前者需要这个钩子，后者不需要？
   - (b) 据此判断：和 autotune 配合时，哪一种描述符更省事？
2. **预测再验证。** sm_120（RTX 5090）上的描述符版：搬运用 TMA，乘加用 `mma.sync`。
   - (a) 按上面表格的道理，预测它每个操作数需要几个输入槽，并说出理由。
   - (b) 上一节的对照表里，这个组合的共享内存是 65,552 字节，其中 16 字节是屏障。用它验证你的预测。
   - (c) 一句话概括：输入槽的数量由什么决定，和用不用 TMA 有没有关系？

图解页已更新到第 5 版，课程记录和 Checkpoint 也已更新，都还没有提交。

---

**042 · 用户** · `2026-10-12T07:22:35.583Z` · `msg-913705aa9167628be898`

噢，所以乘加指令一开始就默认要的沿K维度连续。其中fp16要求宽松一些，可以带转置符号接受正常的[K,N]摆法，但fp8要求严，必须是转置摆法，所以才这样摆。噢，看了你讲的槽被占时间我明白了。这就是之前讲的需要S-1个槽的原因是吗？对于sm_89，由于正在被计算的数据被放到寄存器了，所以只需要S-1个槽了。而sm_90直接从共享内存读，省去了寄存器，但更多地占用了共享内存。
1（a）因为前者是主机侧的描述符，autotune时block大小正在被微调，是不定的，需要运行到kernel时才知道block大小，就需要这个钩子来修改block大小了；但设备侧描述符可以进入到kernel内再构造描述符，此时block大小等编译期参数都已经定了。(b)这样看下来，其实设备侧描述符更方便，省了pre_hook。
2（a）sm_120乘加用的mma.sync也是需要从寄存器读取操作数，乘加结果也是放到寄存器。那么就也只需要2个槽。因为将操作数读到寄存器后，那个槽就空了。（b）共享内存应该是4*16384+16=65552字节。没问题（c）输入槽数量由num_stages与MMA指令是否可以直接从共享内存中读取操作数共同决定。与用不用TMA没有关系。

---

**043 · 助手** · `2026-10-12T07:26:08.202Z` · `msg-1a15e6884439f153b433`

分区结构已经从编译产物里读清楚了。现在把节点 5 的图解加到页面上，然后写评语和讲解。

---

**044 · 助手** · `2026-10-12T07:28:04.493Z` · `msg-d82d805b7b4a4ff4a105`

复查两问都通过，你自己接上的那条线也对。先给评语，再进入节点 5。

## 评语

- **B 的存放：理解对。** 补一个精度：fp8 的“必须”是指令层面的。Triton 遇到 `[K, N]` 的 fp8 仍然能编译，办法是先取进寄存器重排，再存回共享内存，代价就是上次表里的 113 个寄存器和 32 条多出的指令。
- **S−1 个槽：是的，就是这个原因。** 我用不同的 `num_stages` 核对了：

| `num_stages` | sm_89 每个操作数的槽数 | sm_90 每个操作数的槽数 |
| --- | --- | --- |
| 2 | 1 | 2 |
| 3 | 2 | 3 |
| 4 | 3 | 4 |

  sm_89 是 S−1，因为正在算的那一轮已经搬进寄存器；sm_90 是 S，因为它还占着槽。这一条是你自己推出来的。
- **第 1 题对。** 设备侧和 autotune 配合更省事。一处措辞：块大小不是“运行到 kernel 时才知道”，而是每组配置发射之前就知道了，钩子正是在那个时刻运行。问题在于描述符对象建得更早。
- **第 2 题全对。** (c) 的概括可以再准一点：决定槽数的是乘加会不会就地、异步地读共享内存。

## 节点 5：warp 专用化

**本节的例子**（和前两节相同）：块 128 × 128 × 64，一个 A 块或 B 块 16,384 字节，`num_stages = 3`。sm_100 和 sm_120 用 8 个 warp，sm_90 用 4 个 warp。全部来自只编译。

**图解页**：[持久化矩阵乘时间线](https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW)新增“专用化”一节，[仓库副本](docs/triton-learning/attachments/09-persistent-matmul/persistent-matmul-timeline.html)同步更新。先把三个目标各点一遍。

**对应教程**

- [第 229 行](docs/triton-tutorials/official/09-persistent-matmul.py#L229)和[第 543 行](docs/triton-tutorials/official/09-persistent-matmul.py#L543)：`tl.range(..., warp_specialize=WARP_SPECIALIZE)`，源码里只有这一个开关。
- [第 59–68 行](docs/triton-tutorials/official/09-persistent-matmul.py#L59-L68)、[第 85–87 行](docs/triton-tutorials/official/09-persistent-matmul.py#L85-L87)：哪些设备启用。
- [第 591–592 行](docs/triton-tutorials/official/09-persistent-matmul.py#L591-L592)、[第 669–678 行](docs/triton-tutorials/official/09-persistent-matmul.py#L669-L678)：Hopper 上的三处规避。

**结论**：不专用化时，同一批 warp 轮流做搬运、乘加和写回。专用化把循环体按角色拆开，分给不同的 warp 分区，每个分区有自己的循环，靠屏障交接。

### 它是生产者与消费者

用 C 的话说：共享内存里的输入槽是环形缓冲，每个槽配两个信号。

- “数据到了”：搬运的一方填完后发出，乘加的一方等它。
- “槽空了”：乘加的一方用完后发出，搬运的一方等它。

上一节的屏障就是这两个信号的载体。

### 三种目标上分得不一样

| 目标 | 搬运 | 乘加 | epilogue |
| --- | --- | --- | --- |
| sm_90 | 默认分区，4 个 warp | 两个分区各 4 个 warp，各算 tile 的一半（64 行） | 两个乘加分区各写回自己那一半 |
| sm_100 | 一个分区，2 个 warp | 一个分区，1 个 warp，只负责发起 | 默认分区的 8 个 warp，K 循环期间什么都不做 |
| sm_120 | 一个分区，2 个 warp | 默认分区的 8 个 warp | 默认分区 |

启用后三种目标都发射 12 个 warp。

**乘加分到几个 warp，由那一代的乘加指令决定**，这正好接上一节的指令粒度：

- `mma.sync` 每个 warp 只能算自己那一份，所以 sm_120 的乘加留在原来的 8 个 warp 里。
- `wgmma` 以 warpgroup 为单位，一条算 64 行，所以 sm_90 用两个 warpgroup 各算一半。
- `tcgen05.mma` 一个线程就能发起，所以 sm_100 只分 1 个 warp。

### 它换来什么

- **搬运者有自己的循环。** 它只看有没有空槽，不管乘加进行到哪里，自然会跨过 tile 的边界。所以 Hopper 上关掉 `flatten` 并不丢掉跨 tile 的预取。
- **sm_100 上三件事真正并行。** 持久版在 TMEM 里开了两个累加器，共 256 列。默认分区读出并写回上一个 tile 时，下一个 tile 的乘加写进另一个累加器。

这里要更正节点 3 的一句话。我说过“要让 epilogue 和下一个 tile 的乘加重叠，得靠 warp 专用化”。这只对同步的 `mma.sync` 成立。sm_100 上乘加是异步的，累加器在 TMEM，不启用专用化时编译器也开了两个累加器。

### 代价

| 目标 | kernel | warp | 共享内存 | TMEM |
| --- | --- | --- | --- | --- |
| sm_90 | `matmul_kernel_descriptor_persistent`，`flatten` 关 | 4 → 12 | 131,096 → 131,544 | — |
| sm_100 | `matmul_kernel_tma` | 8 → 12 | 98,352 → 98,524 | 128 列 |
| sm_100 | `matmul_kernel_tma_persistent` | 8 → 12 | 131,120 → 131,172 | 256 列 |
| sm_120 | `matmul_kernel_tma` | 8 → 12 | 65,552 → 98,572 | — |
| sm_120 | `matmul_kernel_tma_persistent` | 8 → 12 | 98,320 → 131,196 | — |

- **线程变多。** 12 个 warp 是 384 个线程。
- **sm_120 的共享内存涨得最多。** 专用化之后每个操作数是 3 个槽，原来是 2 个。
- **最后一行超过了 sm_120 的上限。** sm_120 每个 CTA 的共享内存上限是 101,376 字节，和 sm_89 相同。131,196 装不上。

### 它是请求，而且前提很多

- **教程只在 capability 主版本不小于 9 时启用。** 你的 4070 Laptop 和 4090 不运行这些版本，5090 会运行。
- **Hopper 的实现要求恰好 4 个 warp。** 写 8 个时 `warp_specialize=True` 被忽略，产物不变，没有报错。
- **Hopper 上不能和 `flatten` 同用。** 合并后的循环里有带 else 的 `scf.if`，Hopper 的实现遇到它就放弃。
- **Hopper 上教程只对设备侧描述符的版本启用。** 我给主机侧描述符的 `matmul_kernel_tma` 配 4 个 warp 强行启用，编译失败。
- **Triton 的文档写的是“只支持 Blackwell，且只对简单的矩阵乘循环有效”。**

### 真实系统

CUTLASS 3 的 Hopper kernel 就是这个结构：线程块分成生产者 warp 组和消费者 warp 组，生产者等缓冲被标记为空再用 TMA 填，消费者等缓冲被标记为满再做乘加。它的文档也说明 Blackwell 的分工结构和 Hopper 差别很大，但“生产者与消费者分开”的思路相同。

**边界**：没有实机结果，也没有测过专用化带来多少收益。

## 检查题

条件同本节开头的例子。

1. **解释。** 启用专用化后，乘加分到的 warp 数在 sm_120、sm_90、sm_100 上分别是 8、4 + 4、1。不看上面的解释，用三条乘加指令“由谁执行”的区别说明这三个数。
2. **诊断。** 你在 RTX 5090（sm_120，每个 CTA 的共享内存上限 101,376 字节）上跑教程。`matmul_kernel_tma_persistent` 启用专用化的那一行，autotune 选出的配置不是 128 × 128 × 64、3 个 stage。
   - (a) 用表里的数字解释原因。
   - (b) 同样的配置不启用专用化就放得下，差的那部分共享内存是什么？
   - (c) 这组配置被淘汰时你会看到报错吗？
3. **比较。** 专用化和 `flatten` 都能让下一个 tile 的数据提前上路。
   - (a) 两者的做法有什么不同？
   - (b) 为什么 Hopper 上二者不能同用，却不损失跨 tile 的预取？

图解页已更新到第 6 版，课程记录和 Checkpoint 也已更新，都还没有提交。

---

**045 · 用户** · `2026-10-12T08:17:14.184Z` · `msg-7431b1e14d54737c5b8d`

我想知道warp的分区是什么概念？就是专用化的功能分区吗？
检查题1. sm_120上使用mma.sync指令，每个warp只算自己的一份，所以就需要和专用化前一样的warp数量8个；sm_90上使用wgmma，以warpgroup为单位，一条算64*128，需要两个warpgroup分别算一半；sm_120上使用tcgen05.mma，一个线程就能发起，而且能算128*128的，所有只用一个warp。
检查题2. 因为这个配置下，之前课程中提到共享内存将涨到131,196，超过了上限101,376字节。这个配置下运行会出现共享内存不够的报错。所以耗时会变成无穷大，就不会选用了。启用专用化后，对于操作数的输入缓冲会增加槽数。差的那部分共享内存就是两个操作数各少了一个缓冲槽。不会看到报错，autotune把报错吞掉了。
检查题3，flatten是在软件层面把循环的流水做长，做到跨tile的流水。专用化则是专门分出一些warp来做数据预取。之前上面说hopper中不能同用是因为带 else 的 scf.if，我不理解为什么这个带else的if出现就不能warp专用化了。是因为带else了，warp会分化吗？

---

**046 · 助手** · `2026-10-12T08:19:34.755Z` · `msg-5db5215fd2cef10ed063`

正在把“分区是什么”和节点 6 的共享内存预算图补到页面上，随后给你完整答复。

---

**047 · 助手** · `2026-10-12T08:22:21.162Z` · `msg-625440d33fee61e786d2`

三道题基本都对。你的两个问题都问到了我没讲清楚的地方，先回答它们，再给评语，然后进入节点 6。

图解页的“专用化”一节补了“分区是什么”，并新增了节点 6 的“预算”一节：[持久化矩阵乘时间线](https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW)，[仓库副本](docs/triton-learning/attachments/09-persistent-matmul/persistent-matmul-timeline.html)同步更新。

## “分区”是什么

是的，就是专用化划出来的功能分组。这个词我没有先定义就用了，补上：

- **分区是 CTA 里一段编号连续的 warp，被指定去跑同一段代码。**
- **硬件只认 warp，不认分区。** 分区是编译器划的，CUTLASS 把同样的东西叫 warp group。
- **所有 warp 跑的是同一份二进制。** 入口处每个线程先算出自己在第几个 warp，再跳到那个分区的循环。

用 C 写是这样：

```c
// 12 个 warp、384 个线程都从这里进来
int warp = thread_id / 32;
if (warp < 8)  default_partition();      // 默认分区：原来申请的那 8 个 warp
else           jump_table[warp - 8]();   // 其余的 warp 各自跳到自己分区的循环
```

sm_100 的产物里能直接看到这几步：`.reqntid 384` 申请 384 个线程，线程号右移 5 位得到 warp 号，小于 8 的跳到默认分区，其余查跳转表。

“默认分区”特殊在它还负责专用化那段循环之外的代码，例如开头的准备和结尾的写回。别的分区只在那段循环里存在。

## 为什么带 else 的 `if` 挡住了 Hopper 的专用化

**不是因为 warp 会分化。** 让不同的 warp 走不同的代码，本来就是专用化要做的事。原因是这个版本的 Hopper 实现有一处没做完，源码里自己标着：

```cpp
// FIXME: skip warpspec if there is else block. Need to improve
// CodePartitioning to correctly handle channels in else block.
```

这段在 `WarpSpecialization.cpp` 第 45–56 行：函数里只要有一个带 else 的 `scf.if`，整个专用化就直接放弃。紧挨着的上面两行是“warp 数不等于 4 就放弃”。

没做完的是什么：

- **channel** 是编译器对“一次交接”的称呼：搬运方填一个槽，乘加方读这个槽。
- 两边要对得上“现在用第几个槽”，编译器给每个 channel 配一个计数器，并把它穿过包着它的每一层循环和 `if`。
- 一个 `if` 有两条分支时，计数器在两条路上都要正确更新。这一步目前只实现了 then 一侧。

那 `flatten` 为什么一定带来 else：

- 合并后的循环里有 `if (T == 0) { 算新 tile 的坐标 }`。
- 这个 `if` 要产出值：新的 `tile_id` 和偏移。不进 `if` 的那些轮也得有值，就是沿用旧的。
- 所以它在 IR 里是 `if … else { 沿用旧值 }`，相当于 C 的 `x = cond ? 新值 : 旧值`。

这是 Triton v3.7.1 的状态，不是硬件的限制。

## 检查题评语

- **第 1 题对。** 第三处应是 sm_100，你写成了 sm_120，是笔误。
- **第 2 题全对。** 差的那部分正是两个操作数各多出的一个槽，2 × 16,384 字节。
- **第 3 题 (a) 对。** (b) 你没有直接回答，改成了提问，问题本身提得好。“为什么不损失跨 tile 的预取”放进下面的检查题第 1 问。

## 节点 6：epilogue 拆半与共享内存的预算

**本节的例子**：kernel 是 `matmul_kernel_tma_persistent`，fp16，8 个 warp。块有两组：

- 128 × 128 × 64：A 块、B 块各 16,384 字节，输出块 128 × 128 × 2 = 32,768 字节。
- 128 × 256 × 64：A 块 16,384 字节，B 块 256 × 64 × 2 = 32,768 字节，输出块 128 × 256 × 2 = 65,536 字节。

**对应教程**：[第 431–445 行](docs/triton-tutorials/official/09-persistent-matmul.py#L431-L445)是拆半的代码和注释，[第 369–382 行](docs/triton-tutorials/official/09-persistent-matmul.py#L369-L382)把它放进配置表，[第 190–193 行](docs/triton-tutorials/official/09-persistent-matmul.py#L190-L193)改写 C 的块形状。

**结论**：描述符版写回 C 时，要先把整块结果放进共享内存，TMA 再从那里搬走。这块输出缓冲和输入槽争同一份共享内存。把输出切成左右两半、分两次写回，输出缓冲只要一半，省下的地方可以换成多一级流水。

### 共享内存的构成

共享内存 = 输入槽 + 输出缓冲 + 屏障的几十字节。

- 输入槽：槽数 × （一个 A 块 + 一个 B 块）。
- 输出缓冲：一个输出块；拆半后是半个。

### 一个它起决定作用的例子

sm_90，块 128 × 256 × 64，4 个 stage，上限 232,448 字节：

| | 输入槽 | 输出缓冲 | 合计 | |
| --- | --- | --- | --- | --- |
| 不拆半 | 4 × 49,152 = 196,608 | 65,536 | 262,176 | 装不上 |
| 拆半 | 196,608 | 32,768 | 229,408 | 放得下 |

同样的块在 3 个 stage 时是 213,016 对 180,248，两种都放得下。所以这里拆半换来的正是第 4 个 stage。教程的注释说的也是这个目的。

### 源码里怎样切

```python
acc = tl.reshape(accumulator, (BLOCK_SIZE_M, 2, BLOCK_SIZE_N // 2))  # 把 N 方向看成“2 段 × 每段 N/2 列”
acc = tl.permute(acc, (0, 2, 1))                                    # 把“段”换到最后一维
acc0, acc1 = tl.split(acc)                                          # 沿最后一维拆成两个 M × N/2 的张量
c_desc.store([offs_am_c, offs_bn_c], acc0.to(dtype))                         # 左半
c_desc.store([offs_am_c, offs_bn_c + BLOCK_SIZE_N // 2], acc1.to(dtype))     # 右半
```

绕这一圈是因为 Triton 没有“取张量左半边”这种切片，只有 `tl.split`：沿大小为 2 的最后一维拆开。

### 它什么时候不起作用

sm_120（RTX 5090），块 128 × 128 × 64，上限 101,376 字节：

| 写法 | stage | 不拆半 | 拆半 | 结论 |
| --- | --- | --- | --- | --- |
| 不启用专用化 | 3 | 98,320 | 81,936 | 都放得下 |
| 不启用专用化 | 4 | 131,096 | 114,712 | 都装不上 |
| 启用专用化 | 2 | 98,372 | 81,988 | 都放得下 |
| 启用专用化 | 3 | 131,196 | 114,812 | 都装不上 |

- **拆半省的是半个输出块，多一级流水要的是 A、B 各一个块。** 块 128 × 256 × 64 时省 32,768、要 49,152；块 128 × 128 × 64 时省 16,384、要 32,768。
- **它只在恰好差这么一点时起作用。** sm_90 那一行超出上限 29,728 字节，拆半省 32,768，够了。sm_120 装不上的两行超出 29,720 和 29,820 字节，拆半只省 16,384，不够。
- **代价**是两次写回而不是一次，累加器要多做一次重排。
- **它只对描述符版有意义。** 指针版的写回不经过这块输出缓冲。

**边界**：全部来自只编译。教程把 `EPILOGUE_SUBTILE` 放进 autotune 的配置表，用不用由实测决定；我没有任何性能数据。

## 检查题

1. **复查节点 5。** Hopper 上启用专用化时 `flatten` 被关掉，循环又回到“tile 循环套 K 循环”。按节点 3 的说法，不合并时流水每个 tile 都要重新预热。为什么这时搬运并不会在 tile 的边界停下来？说出是哪个分区在搬运，它自己的循环里有什么、没有什么。
2. **取舍。** 条件用本节 sm_120 的那张表：块 128 × 128 × 64，上限 101,376 字节，不启用专用化。
   - (a) 用“省下多少”和“超出多少”这两个数说明：为什么 sm_90 的例子里拆半能换来第 4 个 stage，这里不能。
   - (b) 如果目标就是让 4 个 stage 在这里放得下，除了拆半你还会动什么？给出一个办法，估算它的共享内存，并说出代价。
3. **区分两样东西。** 节点 3 里，指针版 `matmul_kernel_persistent` 在 `flatten` 之后也多出了 32,768 字节。它和本节描述符版的输出缓冲是同一样东西吗？各自是什么，为什么本节的拆半办法对指针版没有意义？

课程记录和 Checkpoint 已更新，都还没有提交。

---

**048 · 用户** · `2026-10-12T09:05:23.359Z` · `msg-ac51eab21502ab5b0a82`

在sm_100中，MMA指令直接写回TMEM，那TMA能从TMEM直接搬到显存吗？
1. 因为这时搬运数据的生产者warp分区在搬运。它自己的循环里等待槽空了和发起搬运load，没有MMA计算和写回结果。导致之前情况中在tile边界停下来主要是因为对新的tile的prologue地址计算吧。在warp专用化里，我理解是不用按串行的先做前面的tile的mma，而后再做新tile的prologue。新tile的prologue可以在生产者warp里做，与消费者warp的mma并行。

---

**049 · 助手** · `2026-10-12T09:06:32.746Z` · `msg-b4cd0a8e76ed7193664f`

## TMA 能从 TMEM 直接搬到显存吗

**不能。** 我查了 PTX 文档和 sm_100 的编译产物。

- **TMA 只在两种存储之间搬**：显存到共享内存，共享内存到显存。它的指令 `cp.async.bulk.tensor` 没有 TMEM 这个端点。
- **TMEM 的出入口是另一组指令**：
  - `tcgen05.ld`：TMEM 到线程的寄存器。
  - `tcgen05.st`：寄存器到 TMEM。
  - `tcgen05.cp`：共享内存到 TMEM，只有这一个方向。

所以 sm_100 上结果要走三步才能回到显存。编译出的 epilogue 就是这个顺序：

| 步骤 | 从哪到哪 | 谁做 |
| --- | --- | --- |
| 读出累加器 | TMEM → 寄存器 | 线程，`tcgen05.ld` |
| fp32 转 fp16 | 在寄存器里 | 线程 |
| 放进输出缓冲 | 寄存器 → 共享内存 | 线程 |
| 写回 C | 共享内存 → 显存 | TMA |

这解释了前两节的两件事：

- **节点 5**：sm_100 的默认分区为什么留着 8 个 warp 专做 epilogue。读出 128 × 128 的累加器要靠线程的寄存器，每个线程拿 64 个值，256 个线程才拿得完。
- **节点 6**：sm_100 上为什么还有那块输出缓冲。结果最终得先落到共享内存，TMA 才搬得走。

另外，就算能直接搬也不够：累加器是 fp32，C 是 fp16，中间这次类型转换只能在寄存器里做。

## 第 1 题评语

**搬运分区的部分答对了。**

- 搬运的是生产者分区，它的循环里只有“等空槽、发起读入”，没有乘加和写回。
- 你最后一句也对：新 tile 的坐标由搬运分区自己算，和消费者的乘加并行。

**有一处归因要改。** 你说不合并时在 tile 边界停下来“主要是因为对新 tile 的 prologue 地址计算”。地址计算只是几条整数指令，不是停顿的来源。停顿来自流水的范围：

- 流水只管 K 循环这一个循环。K 循环一结束，在途的读入就排空，路上不再有任何数据。
- 同一批 warp 接着做 epilogue，这期间不会有人去发下一个 tile 的读入。
- 下一个 tile 开始后，才发出头两轮读入，然后**等第一批数据到达**。

损失的是“读入发得太晚”，以及随之而来的等待。`flatten` 和专用化解决的都是这件事：让下一个 tile 的读入提前发出。它们没有让地址算得更快。

这一点你之前碰到过两次，都是把“等数据”算到了 prologue 头上，所以补一道小题确认。

## 还等着你的

1. **补充题（改条件）。** 假设 prologue 的地址计算完全不花时间。不合并、也不专用化的版本，在 tile 的边界还会不会停顿？为什么？
2. 上一条消息里检查题的**第 2 题**（拆半的取舍）。
3. 上一条消息里检查题的**第 3 题**（指针版多出的 32,768 字节和描述符版的输出缓冲是不是同一样东西）。

Checkpoint 已更新，仍未提交。

---

**050 · 用户** · `2026-10-12T09:36:51.861Z` · `msg-273665fe63bd5bb10848`

所以对于生产者的warp，他的循环是只有一个循环吗？没有tile和K两重循环？

---

**051 · 助手** · `2026-10-12T09:38:04.120Z` · `msg-170fe2471911c4a771b3`

**两种情况都有，取决于有没有开 `flatten`。** 我之前只说“搬运者有自己的循环”，没说清是几层。下面按编译出的 IR 整理。

## Hopper（sm_90）：两重循环都还在

Hopper 上专用化要求关掉 `flatten`，所以搬运分区拿到的仍是 tile 循环套 K 循环：

```c
// 搬运分区自己的那份循环
for (tile = start; tile < num_tiles; tile += NUM_SMS) {   // tile 循环
    算这个 tile 的坐标;                                      // prologue
    for (k = 0; k < k_tiles; k++) {                        // K 循环
        等一个空槽;  发 TMA 搬 A 的上半;
        等一个空槽;  发 TMA 搬 B;
        等一个空槽;  发 TMA 搬 A 的下半;
    }
    // 这里什么都没有：没有排空，没有 epilogue
}
```

A 分两半搬，是因为两个乘加分区各算 tile 的一半（64 行），各要自己那一半 A。

## Blackwell（sm_100）：合成了一层

教程的持久版在这里开着 `flatten=True`，两层先被合并，再做专用化。搬运分区拿到的是一个循环：

```c
for (it = 0; it < 本 CTA 的 tile 数 * k_tiles; it++) {
    if (这一轮是某个 tile 的第 0 轮)  算新 tile 的坐标;
    等一个空槽;  发 TMA 搬 A、B;
}
```

## 要点不在几层，而在里面剩了什么

- **每个分区各拿一份同样形状的循环，里面只留自己的操作。** 乘加分区的那份里是“等数据、乘加、通知槽空了”，tile 结束时写回；搬运分区的那份里只有上面这些。
- **所以搬运分区不会在 tile 的边界停下来。** 在 Hopper 的两重循环里，一个 tile 的 K 循环结束后，紧接着就是下一个 tile 的坐标计算和读入，中间没有任何要等的东西。能让它停下的只有“没有空槽”。
- **各分区的循环各数各的。** 它们没有共用的循环变量，只靠屏障对齐。

这也正好对上那道补充题：不专用化时，同一份循环里 K 循环之后还排着排空和 epilogue，下一个 tile 的读入只能等它们做完才发出。

图解页的“专用化”一节按这个说法改了措辞：[持久化矩阵乘时间线](https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW)，仓库副本同步更新，未提交。

还等着你的三道题不变：补充题，以及节点 6 检查题的第 2、3 题。

---

**052 · 用户** · `2026-10-12T10:09:21.493Z` · `msg-74f025acf1dfcd87fb40`

所以根因究竟是什么？为什么只留自己的操作就可以不停下来？是不是不用排空了？原本每次tile循环的流水会需要前一个tile流水完全结束排空，但分开之后就不需要排空了。

---

**053 · 助手** · `2026-10-12T10:10:13.991Z` · `msg-d217413a1a5d069a3983`

**根因是执行顺序：一批 warp 只有一条执行顺序，“请求下一个 tile 的数据”这句话排在哪里，就在哪里发出。** 你说的“不用排空了”对了一半，排空是结果，不是原因。

## 不合并、不专用化时，这句话排在哪

同一批 warp 按源码的顺序往下执行，一次只能做一件事：

```text
tile i 的 K 循环 → 排空 → tile i 的 epilogue → tile i+1 的坐标 → 发出 tile i+1 的头两轮读入 → 等第一轮到达
```

“发出 tile i+1 的读入”排在 tile i 的 epilogue 后面。所以 epilogue 期间路上没有任何数据，等它做完才发请求，然后还要等数据到。

这也说明排空不是原因。我做个推理：假设把排空那条指令拿掉，停顿仍然在，因为下一个 tile 的读入还是要等 epilogue 做完才发得出去。

## 三种写法，区别只在这句话的位置

| 写法 | “发出 tile i+1 第 0 轮读入”什么时候发生 | 靠什么做到 |
| --- | --- | --- |
| 不合并、不专用化 | tile i 的 epilogue 做完之后 | — |
| `flatten` | tile i 的倒数第 2 轮乘加时 | 编译器把这句话在同一条执行顺序里往前挪 |
| 专用化 | 只要有空槽就发 | 给这句话单开一条执行顺序，由另一批 warp 执行 |

## 为什么“只留自己的操作”就不停

一批 warp 只会停在它自己程序里的等待上。

- **搬运分区的程序里**，两次读入之间没有 epilogue，也没有乘加，唯一的等待是“等一个空槽”。所以只要有空槽，它就一直往下发。
- **不专用化的程序里**，从“tile i 的最后一次读入”到“tile i+1 的第一次读入”之间，排着剩下的乘加、排空、epilogue 和坐标计算。

用 C 的线程来比：单线程程序写成 `compute(i); write(i); read_async(i+1);`，读永远在写之后。改成两个线程加一个缓冲队列，读线程就只受队列有没有空位的限制。

## 回到你的说法

- “分开之后不需要排空了”：搬运分区的循环里确实没有 tile 之间的排空，这句对。
- 但更准确的说法是：**分开之后，下一个 tile 的读入不再排在上一个 tile 的 epilogue 后面。** 没有排空只是这件事的表现。

上次那道补充题的答案我在这里已经讲出来了，换一道。

## 还等着你的

1. **补充题（换过的）。** sm_120 上启用专用化后，搬运单独分了出去，乘加和 epilogue 仍然在默认分区的同一批 warp 里。在 tile 的边界上，下面两件事各能不能和 tile i 的 epilogue 同时进行？用“一批 warp 只有一条执行顺序”说明。
   - (a) tile i+1 的读入。
   - (b) tile i+1 的乘加。
2. 节点 6 检查题的**第 2 题**（拆半的取舍）。
3. 节点 6 检查题的**第 3 题**（指针版多出的 32,768 字节和描述符版的输出缓冲是不是同一样东西）。

---

**054 · 用户** · `2026-10-12T10:19:10.877Z` · `msg-c1a47c3fa75cb73595eb`

所以flatten是通过调整做事情的顺序实现的“不停下来”，让耗时长的读数据的事情放在顺序前面。而专用化则是直接增加做事情的warp，让另一批warp去做搬运，也使得做事情之间的顺序不出现下一个 tile 的读入在上一个 tile 的 epilogue 后面的现象。是吧？flatten思想上更像异步，而专用化思想上更像并行？

---

**055 · 助手** · `2026-10-12T10:19:40.442Z` · `msg-93a8a5494ae9661510ea`

**是的，两句都对，这个类比也成立。** 补三点让它更准。

## 类比为什么成立

- **`flatten` 像单线程的异步。** 执行顺序只有一条。读入本身早就是异步的：`cp.async` 发出后立刻返回，数据在后台搬。`flatten` 做的是把“发请求”这一步挪到更早的位置，让后台搬运和手上的计算重叠。这就是异步 I/O 的写法：先发请求，接着干别的，稍后回来取结果。
- **专用化像多线程。** 多出一条执行顺序，由另一批 warp 跑。两边通过一块有限的缓冲和两个信号对接，就是生产者与消费者。

## 三点补充

**一、异步不是 `flatten` 带来的，它只是把异步用到了 tile 的边界上。**
不开 `flatten` 时，K 循环内部已经是“先发请求、后取结果”了。断的只是 tile 交接那一处。专用化之后的搬运分区发的也还是异步的读入，所以两者并不互斥，区别在由谁来安排发请求的时机。

**二、时机一个是写死的，一个是跟着信号走的。**

| | `flatten` | 专用化 |
| --- | --- | --- |
| 谁决定何时发下一批读入 | 编译器，编译时定死：固定提前两轮 | 搬运分区自己，运行时看有没有空槽 |
| 能提前多少 | 正好 `num_stages − 1` 轮 | 缓冲有多少空位就能提前多少 |
| 乘加慢下来时 | 读入跟着一起慢，因为在同一条顺序里 | 读入照常往前填，直到缓冲满 |

**三、代价也和这两种编程方式对得上。**

- 单线程异步不添人手：还是 8 个 warp，只多了一块中转。但所有事仍然挤在同一批 warp 的时间里，例如 sm_89 上 epilogue 期间，下一个 tile 的乘加照样做不了。
- 多线程要添人手：发射的 warp 从 8 个变成 12 个，还要付同步的开销（屏障）和更多的缓冲（每个操作数从 S−1 个槽变成 S 个）。

用一句话收住：**`flatten` 改的是一条顺序里的先后，专用化改的是有几条顺序。**

你这个概括其实已经能回答那道换过的补充题了，试着把它用上。还等着你的三道题不变：

1. 补充题：sm_120 启用专用化后，tile i+1 的读入、tile i+1 的乘加，各能不能和 tile i 的 epilogue 同时进行。
2. 节点 6 检查题第 2 题（拆半的取舍）。
3. 节点 6 检查题第 3 题（指针版多出的 32,768 字节和描述符版的输出缓冲是不是同一样东西）。

---

**056 · 用户** · `2026-10-12T11:39:52.443Z` · `msg-55c984375909f969cbc3`

<pasted_content id="b992">
1. tile i+1的读入可以与前一个tile的epilogue同时进行，但tile i+1的乘加不可以同时进行。因为读入和epilogue分别是两个warpgroup做的事情，可以并行。但乘加和epilogue在同一批warp上，一个时间点上只能做一件事，不能同时进行。
2. 因为对于stage=4，折半之后共享内存需求从131096变成了114712字节，省下了16384字节，但依旧比上限101376超出了13336字节。所以换不来第四个stage；如果一定要让4个stage放得下，那么还可以减小块的大小。改成64 * 64 * 64.那么输入槽就变成64 * 64 * 2 * 2 *3=49152字节，输出缓冲就变成64 * 64 * 2 = 8192字节，一共就只有57344字节的共享内存需求。再加上几十字节的屏障，完全足够了。但代价就是块数量会变多，tile任务变多，tile之间间隔也就更多了。
3. 不一样。flatten版中是为输出结果单独开辟了一块缓冲空间，因为相比于非flatten版无法复用输入槽的空间。而本节中的输出缓冲依旧是和输入槽争用同一份共享内存，这里减少了输出缓冲空间可以给输入槽用。我不太理解折半方法对指针版没有意义，指针版写回也需要通过共享内存呀。
</pasted_content id="b992">

---

**057 · 助手** · `2026-10-12T11:43:18.859Z` · `msg-043438adcbff1dc5367b`

三道题都过了。第 3 题里你的质疑是对的：我说“拆半对指针版没有意义”，这句话错了。先更正，再进入节点 7。

## 评语

**补充题：对。** 读入和 epilogue 在不同的分区，可以同时进行；乘加和 epilogue 在同一批 warp 上，只能一先一后。一处用词：sm_120 上是“两个分区”（2 个 warp 和 8 个 warp），不是两个 warpgroup，warpgroup 专指 4 个 warp 一组。

**第 2 题：对。** 114,712 仍超出 13,336 字节，换不来第 4 个 stage。你的替代办法我编译验证了：

| 块 | 你的估算 | 编译结果（sm_120，4 个 stage） |
| --- | --- | --- |
| 64 × 64 × 64 | 57,344 加屏障 | 57,368 |

代价除了 tile 变多，还有一条：每个搬进来的元素参与的乘法变少了。块从 128 × 128 缩到 64 × 64，每算一次乘加要搬的字节数翻倍。

**第 3 题：你的质疑成立，我讲错了。** 指针版写回前确实也要经过共享内存。我把教程的拆半写法套到指针版 `matmul_kernel_persistent` 上编译：

| 目标 | `flatten` | 不拆半 | 拆半 |
| --- | --- | --- | --- |
| sm_89 | 开 | 98,304 | 81,920 |
| sm_89 | 关 | 65,536 | 65,536 |
| sm_90 | 开 | 131,072 | 114,688 |

- **`flatten` 开着时，指针版同样省半个输出块。**
- **`flatten` 关着时没有变化**，因为那时中转本来就借用空出的输入槽。
- **两块缓冲的区别只在“为什么要经过共享内存”**：指针版是为了换布局，累加器在各线程手里的摆法不适合直接写回；描述符版是因为 TMA 只能从共享内存搬。

那道题的前提是错的，不算你的差距。图解页和课程记录都已更正。

## 节点 7：怎样度量

**本节的例子**：A 是 `[8192, 512]`，B 是 `[512, 8192]`，fp16，也就是 `M = N = 8192`、`K = 512`。

**对应教程**

- [第 71–82 行](docs/triton-tutorials/official/09-persistent-matmul.py#L71-L82)：launch metadata。
- [第 608–632 行](docs/triton-tutorials/official/09-persistent-matmul.py#L608-L632)：cuBLAS 和 `torch.matmul` 两条基线。
- [第 635–678 行](docs/triton-tutorials/official/09-persistent-matmul.py#L635-L678)：`bench()`。
- [第 719–758 行](docs/triton-tutorials/official/09-persistent-matmul.py#L719-L758)：出表和主流程。

这一节不涉及编译器内部，没有配图。

**结论**：教程报的 `tflop16/s` 等于“这次矩阵乘的浮点运算数”除以“proton 量到的 GPU 执行时间”。运算数由你通过 launch metadata 告诉 proton，时间由 proton 自己量。

### TFLOPS 的分子

矩阵乘的每个输出元素要做 K 次乘、K 次加，所以运算数是 `2 × M × N × K`。本例是 2 × 8192 × 8192 × 512 ≈ 6.87 × 10¹⁰。

分母是整个 kernel 的时间，发射、prologue、epilogue 全算在内。所以 K 越小，TFLOPS 越低，即使张量核心一样快。这和节点 1–2 的结论是同一件事。

### launch metadata：把分子交给 profiler

```python
def _matmul_launch_metadata(grid, kernel, args):
    ...
    ret["name"] = f"{kernel.name}{ws_str} [M={M}, N={N}, K={K}]"
    ret[f"flops{bytes_per_elem * 8}"] = 2. * M * N * K     # fp16 时键名是 flops16
    ret["bytes"] = bytes_per_elem * (M * K + N * K + M * N)
    return ret

@triton.jit(launch_metadata=_matmul_launch_metadata)
def matmul_kernel(...):
```

- **它是一个回调。** 每次发射前 Triton 调用它，拿到一个字典，交给 profiler。
- **只有装了 profiler 才会调用。** 平时没有开销。
- **proton 认得的键**：`name`、`flops8`、`flops16`、`flops32`、`flops64`、`bytes`。

### proton：量分母

proton 是 Triton 自带的 profiler，在 NVIDIA 上通过 CUPTI 拿到每个 kernel 的执行时间，再按名字汇总。教程的用法是：

| 调用 | 作用 |
| --- | --- |
| `proton.start("matmul", hook="triton")` | 开始一次记录；`hook="triton"` 表示发射前调用 launch metadata |
| `proton.deactivate()` | 暂停记录，预热那一万次不计入 |
| `proton.activate(0)` … `proton.deactivate(0)` | 只记录正式的那一万次 |
| `proton.finalize()` | 写出 `matmul.hatchet` |
| `show_profile(...)` | 按 `tflop16/s` 和 `time/ms` 出表 |

它和前几课用的“`perf_counter` 加 `synchronize`”不同：前者量的是 GPU 上 kernel 的执行时间，后者量的是主机上从调用到同步完成的时间，包含 Python 和发射的开销。

### 基线

- **cuBLAS 和 `torch.matmul`** 不是 Triton kernel，没有 launch metadata。教程用 `proton.scope(名字, {"flops16": ..., "bytes": ...})` 把它们包起来，手工给出运算数。
- **基线是参照，不是目标。** 它告诉你同一台设备上成熟实现大概在什么位置。
- **你的机器上要留意**：教程在导入时就加载 `libcublas.so`，找不到这个库脚本会直接失败。

### 直接跑教程脚本，结果里混着什么

教程的 `bench()` 给出的“persistent 对 naive”并不只反映持久化：

- **两个 kernel 各自 autotune。** 选出的块和 stage 可能不同。在 sm_89 上，24 组配置里朴素版有 10 组因共享内存超限被跳过，持久版有 16 组。
- **持久版同时开着 `flatten`。** 两个效果叠在一起。
- **顺序测量。** 每个版本连跑两万次才换下一个，笔记本上频率可能漂移。

所以我们自己的测量要固定同一组配置，把 `flatten` 单独作为一个开关，并让各版本交替运行。测量脚本由我来写，在约定练习之后给你。

## 检查题

1. **口径。** proton 表里的 `tflop16/s` 是由哪三样东西得到的，各来自哪里？如果一个 kernel 忘了配 `launch_metadata`，表里会缺什么、还剩什么？
2. **控制变量。** 同事在一台 sm_89 的机器上直接跑教程脚本，得到“persistent 比 naive 快 6%”，据此说“持久化带来 6% 的提升”。指出这个数字里至少两个不属于持久化本身的因素，并说明你会怎样改测量把它们分开。
3. **预测（先于测量）。** 设备是你的 4070 Laptop，块固定为 128 × 128 × 64，`M = N = 8192`，K 取 128、512、2048 三个值。
   - (a) 持久版对朴素版的 TFLOPS 比值，随 K 增大会怎样变化？写出方向和理由。
   - (b) 什么样的测量结果会推翻你的预测？
   - (c) 上机时顺手把前几天那段设备读数的输出贴回来，我要用真实的 SM 数来写测量脚本。

课程记录和 Checkpoint 已更新，都还没有提交。

---

**058 · 用户** · `2026-10-12T12:31:39.546Z` · `msg-3463579ea1ff5ab5c76d`

<pasted_content id="b992">
1. 来自运算操作数和kernel执行时间，分别来自launch metadata的计算和通过 CUPTI 拿到每个 kernel 的执行时间。如果没有配launch metadata，那就只有执行时间了。

2. （1）两个kernel分别进行autotune，最后跑的最佳性能的配置可能不一样。二者的对比可能并不是在相同配置下的对比。（2）持久化可能还同时有flatten写法。我认为首先要固定BLOCK大小等autotune的配置，或者直接把autotune关闭。然后确保二者代码写法中只有persistent的差异。然后再进行比较。

3. （a）随着K的增大。持久版的优势可能会下降。比值会下降。因为持久版最大的开销减小就是去除了多次发射的开销。随着K增大，K循环在kernel中的占比变大，发射部分开销占比变小。持久版的相对优势也就变小了。（b）测量结果显示比值没有显著变化或者反而增大会推翻我的结论吧（c）我借用到了5090的卡。结果如下：

   GPU          : NVIDIA GeForce RTX 5090 (31.4 GiB)
   capability   : (12, 0)
   SM count     : 170
   shared limit : 101376 bytes per CTA
   versions     : torch 2.13.0+cu130 | triton 3.7.1
   kernel       : 5.15.0-119-generic
</pasted_content id="b992">

---

**059 · 助手** · `2026-10-12T12:33:49.581Z` · `msg-174875e2a4dcb5b9398d`

节点 7 三问都通过，七个节点到这里全部讲完。下面是评语、串讲，然后是综合验收。

## 节点 7 评语

- **第 1 题对。** 运算数来自 launch metadata，时间来自 proton。没配 metadata 就只剩时间。
- **第 2 题对。** 两个因素都找准了，改法也对。要把 `flatten` 单独分出来，还需要一个“持久但不合并”的版本，这样是三个版本两两相比。另有一个你没提的因素：教程是一个版本连跑两万次才换下一个，各版本不在同一状态下测。
- **第 3 题：预测已记入课程记录。** 方向和理由都清楚。可证伪条件再收紧一点：以测量的波动幅度来界定“显著”。
- **设备读数收到，改用 5090。** 你的预测不依赖具体设备，实测时以 5090 为准。读数还证实了两件事：
  - sm_120 每个 CTA 的共享内存上限确实是 101,376 字节，和我按文档取的值一致。
  - SM 数是 170。持久版在这台机器上发射 170 个 CTA，每个处理约 24 个 tile。

5090 是 sm_120，教程会运行描述符版和专用化的版本，所以之前说的可选观察现在具备条件了，做不做到约定练习时再定。

## 串讲

沿用贯穿案例：`M = N = 8192`、`K = 512`、fp16，块 128 × 128 × 64。输出被分成 4096 个 tile，每个 tile 的 K 循环是 8 轮。

**起点是第 03 课的写法。** 4096 个 CTA，每个算一个 tile：prologue 算坐标，K 循环做乘加，epilogue 写回。K 循环内部有流水，读入比乘加提前 2 轮。张量核心只在 K 循环里忙，每个 tile 还要付发射、等第一批数据、排空和写回这些固定的部分。K 越小，它们占得越多。

**第一步，持久化。** 每个 SM 只发射一个 CTA，它按步长循环领取 tile。重复发射省掉了。这一步引入的关键状态是 `NUM_SMS`：它既是网格的大小，又是领取的步长，两者必须相等。tile 之间的交接现在进了同一段代码，但“请求下一个 tile 的数据”仍排在上一个 tile 的 epilogue 后面。

**第二步，`flatten`。** 编译器把两层循环合成一层，流水于是跨过 tile 的边界，请求在同一条执行顺序里被往前挪了两轮。它引入的状态是计数器 T，以及 prologue 和 epilogue 各自的游标 `tile_id` 与 `tile_id_c`。代价是写回用的中转不能再借输入槽。

**第三步，换硬件。** 源码几乎不变，编译器按设备选指令：

- 搬运从 `cp.async` 变成 TMA，线程不再算地址。这需要描述符，可以在主机上建，也可以在 kernel 里建。
- 乘加从 `mma.sync` 变成 `wgmma`，再变成 `tcgen05.mma`，一条指令覆盖的面积越来越大，操作数不再进寄存器。
- 累加器从寄存器搬进 TMEM。

**第四步，warp 专用化。** 前面都只有一条执行顺序。专用化多开几条：搬运、乘加、写回各归一个分区，靠屏障交接。

**所有这些都在争同一份共享内存。** 它由输入槽和写回的缓冲组成。输入槽是 S−1 个还是 S 个，取决于乘加会不会就地读它；写回的缓冲能不能借输入槽，取决于下一个 tile 的数据是否已在路上。epilogue 拆半是这份预算上的一个旋钮。

**有两条纪律贯穿全课。**

- **开关是请求，不是保证。** `flatten`、`warp_specialize`、autotune 里的配置，都可能被不声不响地跳过。确认的办法是看编译产物。
- **编译器看不见的信息，就当它不成立。** 对齐和连续性靠提示传达；经过 `scf.if` 传出、或者被展开成运行时参数之后，信息丢了，读入就退回同步。

**落到真实系统。** CUTLASS 3 的 Hopper kernel 是同一套结构：持久化的线程块，TMA 搬运，`wgmma` 计算，生产者与消费者两组 warp。教程是它在 Triton 里的写法，区别在于这些决定由编译器的 pass 代你做，你能控制的是几个开关和提示。度量上，教程报的 TFLOPS 是 `2 × M × N × K` 除以 kernel 的执行时间，整个 kernel 的固定部分都在分母里。

## 综合验收

三道题，可以查图解页和教程。第 1 题请写成你会说出口的话。

1. **口述（60–90 秒）。** 你的 5090 是 sm_120：170 个 SM，共享内存上限 101,376 字节。要给贯穿案例（`M = N = 8192`、`K = 512`、fp16）从教程的五个 kernel 里选一个。说出你选哪个，按从发射到写回的顺序讲清它的数据流，并说明你为什么不选另外几个里最接近的那一个。
2. **两个相反的趋势。** 同一组配置下，描述符版从 sm_89 的指针版起算，到 sm_100 时每线程寄存器从 135 降到 71，共享内存却从 65,536 涨到 98,352。用本课的机制解释：为什么这两个变化是同一件事的两面？这对 sm_120 这样上限只有 101,376 字节的设备意味着什么？
3. **迁移。** 你工作里用的是非 NV 的加速器。假设要把教程的持久版搬到一个没有 `cp.async`、也没有 TMA 的后端上。
   - (a) 本课的四步里，哪些收益不依赖这些硬件特性，哪些会消失？
   - (b) 动手之前，你会先看哪两样编译产物，各想确认什么？

课程记录已切到 `synthesis` 阶段，预测和设备读数都已记录，仍未提交。

---

**060 · 用户** · `2026-10-12T12:37:19.698Z` · `msg-26c84f7939460c342bd2`

稍等，之前你说tflop16/s 是由哪三样东西，我只说了两样，还有其他的吗？

---

**061 · 助手** · `2026-10-12T12:37:38.504Z` · `msg-4090c449e2a0b9743351`

你没有漏掉实质内容，是我的题目数错了，评语里又没说明。

`tflop16/s` 在 proton 的出表代码里就是一个除法：

```text
tflop16/s = 这一行累计的 flops16 ÷ 这一行累计的时间（秒） ÷ 10¹²
```

实质的量只有两样，正是你答的：运算数来自 launch metadata，时间由 proton 量。

我出题时心里的“第三样”是**名字**，也就是 metadata 里的 `name`。它不进算式，但决定“一行”是什么：

- proton 按名字把多次发射归到同一行，分子分母都是这一行里所有发射的累计值。教程正式测一万次，表里的数是一万次的运算数之和除以一万次的时间之和。
- 教程把 M、N、K 写进了名字，例如 `matmul_kernel [M=8192, N=8192, K=512]`。所以扫 K 的时候，不同的 K 会各占一行，不会被混在一起平均。
- 反过来，如果两个不同形状的调用用了同一个名字，它们会被并成一行，得到的是一个没有意义的混合值。

这一点对后面的实测有用：我们会让“朴素版、持久版、持久版关 `flatten`”各有自己的名字，并把 K 写进去。

综合验收的三道题照旧等你作答。

---

**062 · 用户** · `2026-10-12T12:59:48.748Z` · `msg-69b5cacd248038877dd3`

明白。1. 我要选一个最怎么样的kernel呢？我随机选的话就没有不选其他kernel的理由。
2. 因为这两个变化实际上都是为了让数据传输不停下来，减少数据传输的开销。共享内存不断增加，是为了增加缓冲槽位空间，让尽可能多的数据提前开始搬，提前准备好。MMA指令直接从共享内存读数据进行计算，也减少了共享内存到寄存器的搬运过程。这对共享内存上限较低的设备来说，就使得kernel的性能在一定程度上受到了共享内存空间的制约。
3. （a）持久化的省去发射开销的收益不依赖于硬件特性。几乎所有硬件总要起kernel发射的。所以持久化的收益不会消失。flatten中，调整了代码流水，使得load数据的异步行为跨越tile边界往前移，减少数据读取的等待。这一点依赖于异步拷贝读入数据，需要硬件支持该功能。可能会消失。第三、四步中，tma、tmem、warp专用化，这些都与硬件有关，都可能消失。（b）对于非nv加速器，我会先看编译产物中发射动作是不是从tile循环中提出来了，然后如果支持异步拷贝再看编译结果中本tile循环中有没有提取读取后一个tile的数据的行为。

---

**063 · 助手** · `2026-10-12T13:02:06.210Z` · `msg-d8d5e5b56cb50ede6982`

第 1 题你问得对，是题目没给标准。第 2、3 题各有一处要补。下面先评，再把三道题重新收拢成复查。

## 第 1 题：补上标准

**标准是：预计在这台 5090 上，对贯穿案例跑得最快（TFLOPS 最高），并且装得上。** 现在还没有测量，所以这是一个有理由的押注，我评的是理由，不是押中没有。

五个候选：

| kernel | 调度 | 读写方式 |
| --- | --- | --- |
| `matmul_kernel` | 逐 tile 发射 | 指针 |
| `matmul_kernel_persistent` | 持久，带 `flatten` | 指针 |
| `matmul_kernel_tma` | 逐 tile 发射 | 主机侧描述符 |
| `matmul_kernel_tma_persistent` | 持久，带 `flatten`，可拆半 | 主机侧描述符 |
| `matmul_kernel_descriptor_persistent` | 持久 | 设备侧描述符 |

后三个还各有“启用专用化”的版本。共享内存和指令的数字可以查图解页的表。

## 第 2 题：对了一半

- **对的部分**：乘加直接读共享内存，省去了搬到寄存器这一步；上限低的设备因此被共享内存卡住。
- **要改的部分**：共享内存变多不是“为了让更多数据提前搬”。两种目标的 `num_stages` 都是 3，提前量一样，都是 2 轮。

这两个变化是同一件事的两面，指的是**数据换了地方住**：

| | sm_89 | sm_100 |
| --- | --- | --- |
| 正在被乘加用的操作数 | 住在线程的寄存器里 | 住在共享内存的槽里 |
| 累加器 | 住在线程的寄存器里 | 住在 TMEM 里 |
| 结果 | 寄存器多，槽腾得快，S−1 个槽 | 寄存器少，槽被占得久，S 个槽 |

你在节点 4 的复查里说过“sm_90 省去了寄存器，但更多地占用了共享内存”，那句是准确的。这次只是把原因说偏了。

## 第 3 题

**(a) 对。** 你的三层划分都成立。补一个实例，我把教程的两个指针版 kernel 按 AMD 后端（`gfx942`）编译了，它正是一个没有 `cp.async` 和 TMA 的后端：

| 版本 | 共享内存 | 输入槽 | `scf.if` |
| --- | --- | --- | --- |
| 逐 tile 发射 | 65,536 | 每个操作数 2 个 | 2 处 |
| 持久，`flatten` 关 | 65,536 | 2 个 | 2 处 |
| 持久，`flatten` 开 | 65,536 | 2 个 | 8 处 |

- **流水还在。** 没有异步拷贝指令，读入是先取进寄存器、再存进共享内存，但仍然提前一轮发出，槽数也一样。
- **循环合并也生效了**，`scf.if` 从 2 处变成 8 处，而且共享内存没有增加。
- 所以你说的“可能会消失”可以收紧成一个判据：**关键不在有没有 `cp.async` 这条指令，而在读入能不能在后台进行、让线程先去干别的。**

这是只编译的结果，没有在 AMD 设备上运行。

**(b) 第二样对，第一样要改。** “看发射动作是不是从 tile 循环中提出来”在编译产物里看不到。持久化不是编译器做的变换，它由两处手写的代码决定：包装函数把网格设成 `min(NUM_SMS, tile 数)`，kernel 里自己写了一层 tile 循环。编译器只是照着编。

## 复查（三问）

1. **口述（60–90 秒）。** 按上面的标准，在你的 5090 上为贯穿案例选一个 kernel。依次说：选哪个；它从发射到写回的数据流；为什么不选和它最接近的那一个；你最没把握、要靠实测才能定的一点。
2. **数据住在哪里。** 两组都是描述符版、`num_stages = 3`、不启用专用化，也都用 TMA 搬运：
   - sm_120：每个操作数 2 个槽，每线程 118 个寄存器。
   - sm_90：每个操作数 3 个槽，每线程 90 个寄存器。

   用“正在被乘加用的操作数住在哪里”解释这两组数。
3. **谁完成了持久化。** 持久化是编译器做的，还是你写的代码做的？它在 TTGIR 里留下的痕迹是什么？举出骨架里的一行来说明。

课程记录和 Checkpoint 已更新，仍未提交。

---

**064 · 用户** · `2026-10-12T13:15:20.365Z` · `msg-8cfedbe6a73e4c8f8dee`

题目2中我理解提前量是一样的了。sm90操作数放在共享内存，sm120操作数放在寄存器。所以sm120的寄存器占用多，sm90的共享内存槽用得多。但是对于“同一件事”我觉得还不够深。硬件花大力气升级，只是为了让数据换个地方放吗？那我就原本放在寄存器里用着不也好好的，共享内存槽不还腾的快吗？为什么就要少用寄存器呢？我觉得应该是因为寄存器更加稀缺，让数据放在空间更多的共享内存上。

持久化是手写的代码做出来的变化。它在代码里表现为出现了tile循环吧。可以看TTGIR中有没有出现`scf.for` tile 循环。

---

**065 · 助手** · `2026-10-12T13:16:16.863Z` · `msg-04229d7b3058588e24ca`

第 2、3 两问都通过了。你追问的那个“为什么”问得对，“换地方住”确实只是表象。你的猜测对了一半，我把另一半补上。

## 评语

- **第 2 问对。** 提前量相同；sm_90 的操作数留在共享内存，sm_120 的操作数进寄存器，所以一个槽多、一个寄存器多。
- **第 3 问对。** 持久化是手写的代码。它在 TTGIR 里的痕迹就是那层 tile 循环，例如骨架第 64 行：`scf.for %tile_id = %start_pid to %num_tiles step %c128_i32`。步长是 `NUM_SMS` 这个常数，说明一个 CTA 在自己领 tile。

## 硬件为什么要让数据离开寄存器

**目的不是换地方，而是把通用线程从数据通路上拿掉。** 数据住在寄存器里，就意味着每一个字节都得由线程亲手经手。换地方是这个目的的表现，共享内存变多是它的价钱。

具体有三个原因。

**一、寄存器确实紧，你猜对了，但紧的原因不是“共享内存更大”。**

- 寄存器是每个线程私有的，线程之间不能互相访问。一个矩阵放进寄存器，必须切成碎片分给每个线程。
- 本例的累加器是 128 × 128 的 fp32，每个线程 64 个寄存器，256 个线程合计 16,384 个，占一个 SM 全部 65,536 个寄存器的四分之一。
- 每个线程最多只能有 255 个寄存器，而算地址、存循环变量也都要用它。

CUTLASS 的文档直接说了后果：累加器通常占掉一个线程寄存器预算的一半以上，所以这类 kernel 的 occupancy 很低，SM 没有多余的线程可以切换过去，也就掩盖不了访存延迟。这正是第 1 节里“一个 SM 只驻留一个 CTA”的来历。

**二、数据在寄存器里，线程就得一条条指令去喂张量核心。**

本例每轮 K 循环：

| 目标 | 线程要发的指令 |
| --- | --- |
| sm_89 | 每个 warp 先发 24 条 `ldmatrix` 取操作数，再发 64 条 `mma.sync` |
| sm_90 | 每个 warpgroup 发 4 条 `wgmma` |
| sm_100 | 一个线程发 4 条 `tcgen05.mma` |

sm_89 上，张量核心算得多快，受线程发指令的速度牵制。后两代里，张量核心自己成块地去共享内存取数。

**三、数据在谁的寄存器里，计算就绑在谁身上。** 这一条和你前面总结的“异步与并行”是同一件事。

- 操作数和累加器在这批线程的寄存器里，这批线程就得守着乘加，腾不出手做别的。sm_89 上 epilogue 期间下一个 tile 的乘加做不了，原因就在这里。
- 数据搬到共享内存和 TMEM 之后，乘加变成“发出去、稍后再等”的操作，线程可以去做写回或搬运。sm_100 上默认分区的 8 个 warp 在 K 循环期间完全空闲，就是这样腾出来的。

## 回到你的两个疑问

- **“原本放在寄存器里用着不也好好的？”** 对固定的块来说确实能用，共享内存还更省。它的代价是上面三条：寄存器预算卡住块的大小和 occupancy，每轮多一步由线程执行的搬运，以及计算和别的事不能重叠。
- **“只是为了换个地方放吗？”** 不是。更准确的“同一件事”是：**张量核心越来越不依赖线程来喂数据和存结果。** 寄存器变少、指令变少、能重叠的事变多，都是它的收益；槽被占得更久、写回要在共享内存里中转，是它的代价。

有一点我没有证据：这三条各自贡献多少性能。那要靠实测，本课只有编译产物。

## 还差一道

综合验收只剩第 1 问的口述：按“预计最快且装得上”，在你的 5090 上为贯穿案例选一个教程 kernel，说清它的数据流、为什么不选最接近的那一个，以及你最没把握的一点。

Checkpoint 已更新，仍未提交。

---

**066 · 用户** · `2026-10-12T13:33:29.167Z` · `msg-5462af6a5d3e2e13e125`

在5090上，我选matmul_kernel_tma_persistent。因为对于这个kernel，持久化、flatten和tma这三个优化手段都启用了，而且对于输出缓冲，还可以拆半进行减少，以增加输入槽。相比matmul_kernel_tma，有了持久化；相比matmul_kernel_persistent，带了描述符tma。它的数据流上，先进行tma从显存读到共享内存，然后再读取到寄存器中，进行mma.sync计算处理，最后写回共享内存，再由tma写回显存。其中，flatten可以使得在epilogue写回之前，发出读取下一个tile的指令。而对于最接近它的，则是matmul_kernel_descriptor_persistent，主要区别在于设备侧的描述符。设备侧描述符的主要优势在于面对动态的形状，比如grouped gemm，可以在设备侧构建描述符来进行tma。但本例中形状已经固定，所以主机侧完全足够构建描述符，可以省去设备侧构建描述符的指令。

---

**067 · 助手** · `2026-10-12T13:35:56.423Z` · `msg-a5f450a60f9935f0a8e8`

综合验收通过。先给口述的评语，再对照证据，最后是练习约定，请你确认。

## 口述评语

**选择和理由都成立。**

- 数据流讲对了这台设备上最容易错的地方：TMA 把数据搬进共享内存后，操作数还要取进寄存器，由 `mma.sync` 计算。这是 sm_120 和 sm_90 的区别，你没有混。
- 和 `matmul_kernel_descriptor_persistent` 的取舍也对：形状固定时主机侧描述符足够，省掉每个 CTA 自己填描述符的指令。

**三处要补。**

- **开头少了发射。** 完整的数据流从“发射 170 个 CTA，每个按步长 170 领取约 24 个 tile”讲起。这部分你在前两节已经答得很扎实，这里只是漏说。
- **没有说最没把握的一点。** 我替你列两个：
  - 它是否真的比指针版 `matmul_kernel_persistent` 快，没有依据。sm_120 上操作数仍要进寄存器，TMA 只省了算地址这一步。
  - 这组配置占 98,320 字节，离上限只差 3,056 字节，没有任何加深流水的余地。
- **“拆半以增加输入槽”在这里不成立。** 你在节点 6 自己算过：这台设备、这组块，拆半后 4 个 stage 仍超出 13,336 字节。

## 证据对照

| 目标 | 需要的证据 | 现状 |
| --- | --- | --- |
| O1 调度与跨 tile 流水 | 理解 | 已充分 |
| O2 硬件代际、描述符、专用化、预算 | 理解 | 已充分 |
| O3 度量与解释 | 理解加实证 | 理解和预测已有，缺实测结果和你对结果的解释 |
| O4 实现并验证 | 理解加实践 | 缺独立实现 |

所以还需要一次练习，它同时补 O4 和 O3。

## 练习约定 P1（版本 1）

**1. 为什么做。** O4 缺你独立实现的证据；O3 缺实测。这次练习让你写一个持久化矩阵乘，再用它在 5090 上做那次测量，检验你的预测。

**2. 你交付什么。** 一个文件 `gpu/triton/lesson09_persistent_matmul.py`，包含 kernel 和包装函数：

```python
matmul_persistent(a, b, *, num_sms=None, flatten=True,
                  block_m=128, block_n=128, block_k=64,
                  num_stages=3, num_warps=8) -> c
```

- `a` 是 `[M, K]`，`b` 是 `[K, N]`，都是 fp16；返回 `[M, N]` 的 fp16。
- **`b` 按行主序 `[K, N]` 存放**，也就是 PyTorch 里 `a @ b` 的普通摆法，不是教程的 `b.T`。这是本练习和教程不同的地方。
- `num_sms` 为空时取设备的 SM 数；测试会传入别的值。
- `flatten` 是开关，两种取值都要能用。

**3. 怎样算通过。**

| 编号 | 验收项 | 检查方式 |
| --- | --- | --- |
| A1 | 结果与 `torch.matmul` 一致，形状任意：整块、M/N/K 不整块、小于一个块 | 测试；本机解释器层，GPU 上数值层 |
| A2 | 网格是 `min(num_sms, tile 数)`；每个 tile 恰好算一次；输出范围之外的内存不被改写 | 测试，`num_sms` 取 1、几个、多于 tile 数 |
| A3 | `flatten` 两种取值结果相同；开时循环合并生效，关时不生效 | 测试，只编译，看 TTGIR 与共享内存 |
| A4 | N、K 整块且输入对齐时，`flatten` 两种取值下 A、B 都是 16 字节一组的异步拷贝 | 测试，只编译，sm_89 与 sm_90 |
| A5 | 包装函数拒绝不合法的输入：设备、dtype、形状不匹配、不连续 | 测试 |
| A6 | 一段 3–5 句的说明：行主序的 B 在 `flatten` 下你是怎样保住异步拷贝的；epilogue 为什么要有自己的游标 | 我按要点评 |
| M1 | 在 5090 上运行测量脚本，贴回输出；写 5–8 句，对照你的预测解释结果，说明证据支持什么、不支持什么 | 我按要点评；预测不符不算失败 |

M1 的设置：块固定 128 × 128 × 64、3 个 stage、8 个 warp，`M = N = 8192`，K 取 128、512、2048。三个版本都用你的同一个 kernel，只改调度：

- 每个 CTA 一个 tile（`num_sms` 等于 tile 数），相当于逐 tile 发射。
- 持久，`flatten` 关。
- 持久，`flatten` 开。

各版本短轮次交替运行，脚本报出中位数和波动，并事先打印“支持、否定、证据不足”的判据。

**4. 文件边界。**

| 标签 | 路径 |
| --- | --- |
| 你写 | `gpu/triton/lesson09_persistent_matmul.py` |
| 我维护 | `gpu/triton/lesson09_persistent_matmul_test.py`、`gpu/triton/lesson09_persistent_matmul_benchmark.py`、第 09 课的记录 |
| 我只读 | 教程快照、你的实现 |
| 本次不动 | 第 08 课及更早的文件，其他课程的文件 |

**5. 求助。** 可以随时问。如果我透露了某个验收项的关键解法，那一项之后换一个变式来确认，别的项不受影响。

**6. 非目标与完成门槛。**

- 不要求：`GROUP_SIZE_M` 的分组顺序、autotune、fp8、描述符与 TMA、warp 专用化。
- 可选一：在 5090 上跑教程脚本，看描述符版和专用化版的实际数字。
- 可选二：你提的那个改造，把第 08 课的 grouped GEMM 改成能跨 tile 流水。
- A1–A6 和 M1 全部通过、阻塞问题全部关闭，即为完成。

**我的建议**是按上面的必做项来：它最小，而且 M1 直接用你自己的 kernel。grouped GEMM 的改造更有意思，但范围大得多，放在可选二。如果你更想把它作为必做题，告诉我，我改约定。

回复“接受”，我就去写验收测试，确认它们在你动手之前是红的，再把运行方法交给你。

---

**068 · 用户** · `2026-10-12T13:39:53.259Z` · `msg-0ea60f278b3a2ead029a`

就按照这个约定来吧。两个可选也可以记录下来。本轮学习时间紧，不做，留给后续复习时做。我接受。

---

**069 · 助手** · `2026-10-12T13:43:34.572Z` · `msg-95f8eaa8ae253a89698a`

收到，按约定开始。我先在本机写验收测试，并用一份不进仓库的参考实现验证测试本身，确认它们在你动手前是红的，再把运行方法交给你。

---

**070 · 助手** · `2026-10-12T13:46:18.222Z` · `msg-7012f10b84a68e1eba35`

测试在参考实现上有一处我自己的夹具问题（重复编译同一配置时取不到“新编译的 kernel”），正在修。

---

**071 · 助手** · `2026-10-12T13:50:58.035Z` · `msg-0330656c597d136505ae`

测试已经能在参考实现上全绿、在六个故意写错的变体上报红。现在把约定记入课程记录，然后把运行方法交给你。

---

**072 · 助手** · `2026-10-12T13:51:48.455Z` · `msg-94ee23035362a7243a05`

验收测试已经建好，现在是预期中的红。两个可选项也记进了课程记录，本轮不做。

## 先确认一处改动（约定版本 2）

写测试时发现版本 1 漏了一个参数，需要你确认：

```python
matmul_persistent(a, b, *, out=None, num_sms=None, flatten=True,
                  block_m=128, block_n=128, block_k=64,
                  num_stages=3, num_warps=8) -> c
```

**只多了 `out=None`。** 原因是 A2 要检查“输出范围之外的内存不被改写”，这只有测试自己提供输出缓冲才查得出来。其余都不变。不同意的话告诉我，我换一种检查办法。

## 测试在哪，怎样跑

文件是 [lesson09_persistent_matmul_test.py](gpu/triton/lesson09_persistent_matmul_test.py)，共 58 项，分三层：

| 层 | 命令（在仓库根目录） | 需要 GPU 吗 |
| --- | --- | --- |
| 解释器层 | `TRITON_INTERPRET=1 pytest -q gpu/triton/lesson09_persistent_matmul_test.py` | 不需要 |
| 只编译层 | `pytest -q gpu/triton/lesson09_persistent_matmul_test.py` | 不需要 |
| GPU 数值层 | 同上一条，在 5090 上运行 | 需要 |

没有 GPU 的机器上跑第二条命令，数值相关的测试会自动跳过，只跑只编译的那 12 项。

现在的状态是 `1 failed, 57 skipped`，失败的那一项是“实现文件不存在”。

## 测试默认了哪些行为

这些是约定里没有逐条写出、但测试会查的，先说清楚：

- **不合法的输入一律抛 `ValueError`**：不是二维、dtype 不是 fp16、内维对不上、`a` 或 `b` 不连续、`out` 的形状或 dtype 不对、`out` 的列步长不是 1、设备不一致、`num_sms` 不是正整数、在非 CUDA 设备上省略 `num_sms`。
- **`out` 可以是一个更大缓冲里的视图。** 它的列步长是 1，但行步长可以大于 N。给了 `out` 就写进去，并原样返回它。
- **CPU 张量要能用。** 传了 `num_sms` 时，CPU 上的输入不能被拒绝，解释器层和只编译层都靠它。
- **kernel 写成模块级的 `@triton.jit` 函数，每次调用只发射一次。** 只编译层就是这样找到并检查它的，名字和参数由你定。
- **每个 tile 每轮 K 调用一次 `tl.dot`。** “恰好算一次”是在解释器层数 `tl.dot` 的调用次数来查的。

## 各项对应什么

| 验收项 | 测试查什么 |
| --- | --- |
| A1 | 九种形状与 `torch.matmul` 对照，含不整块和只有一个元素的情形 |
| A2 | `num_sms` 取 1、3、7、64 时结果都对；保护区没被改写；`tl.dot` 的次数正好；网格是两者的较小值 |
| A3 | `flatten` 开时 `scf.if` 变多、共享内存变多；关时没有 |
| A4 | 整块、对齐的输入下，没有同步的 fp16 读入，异步拷贝都是 16 字节 |
| A5 | 上面列的那些 `ValueError` |

A3、A4 在 sm_89 和 sm_90 两个目标上各查一遍，用的就是上周教你的那套证据。

## 我这边核对过什么，没核对什么

- 用一份不进仓库的参考实现跑过：解释器层 46 项通过，只编译层 12 项通过。
- 用六个故意写错的版本跑过，每个都被对应的测试抓到：偏移放在 tile 开头、去掉写回的 mask、去掉 K 方向的 mask、步长写成 1、忽略 `flatten`、网格不取较小值。
- **GPU 数值层没有在本机跑过**，这里没有 GPU。第一次在 5090 上跑如果有测试本身的问题，告诉我，我来修。
- **测量脚本还没写。** 等你 A1–A5 过了我再给你，M1 用得上的时候它会在。

## 建议的顺序

1. 先让解释器层变绿，这一层最快，不用等编译。
2. 再看只编译层。A4 是这次练习的关键：`b` 按行主序存放，教程的写法直接搬过来在 `flatten` 开着时过不了这一项。
3. 最后到 5090 上跑数值层，把输出贴回来。

遇到问题随时问。课程记录已切到 `practice` 阶段，这些改动都还没有提交。

---

**073 · 用户** · `2026-10-12T13:54:09.471Z` · `msg-86b1c76922f00050e60b`

好的，没问题。有没有一个文档里包含练习约定的所有细节？我后续实现就照着这个来。

---

**074 · 助手** · `2026-10-12T13:55:06.508Z` · `msg-3a94da949a158331c860`

有，就是第 09 课记录里的“练习约定”一节。我刚把它整理成了完整的规格，版本 2 也标成了已接受：

[docs/triton-learning/lessons/09-persistent-matmul.md 的“条件片段：练习约定”](docs/triton-learning/lessons/09-persistent-matmul.md#L213)

它包含这几部分：

| 小节 | 内容 |
| --- | --- |
| 交付物 | 函数签名、每个参数的含义与要求、返回值；对调度、计算、边界、kernel 形式的要求；哪些输入要抛 `ValueError` |
| 验收项 | A1–A6 和 M1 各查什么、怎么查；M1 的测量设置 |
| 怎样运行测试 | 三层各自的命令、是否需要 GPU、覆盖哪些验收项 |
| 测试没有检查的 | 读入时的越界访问、对齐、性能 |
| 边界与门槛 | 文件边界、求助规则、非目标、两个可选项、完成门槛 |

有三条是上一条消息里没明说、这次补进去的：

- **累加用 fp32。** fp16 读入，fp32 累加，fp16 写回。
- **各维至少为 1。** M、N、K 等于 0 的情形不在约定内，测试也不查。
- **读入时的越界访问测试查不出来，但仍要处理。** 它不影响数值，却是未定义行为，按节点 1 讲的办法处理。

文档和测试如果有不一致，以文档为准，告诉我，我来修测试。这些改动都还没有提交。

---

**075 · 用户** · `2026-10-12T13:55:17.682Z` · `msg-6559b8a80d35bc76bae8`

> command: /compact

---

**076 · 用户** · `2026-10-14T05:30:44.207Z` · `msg-67d75ff859dca8d8750b`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/gpu/triton/lesson09_persistent_matmul.py in the IDE. This may or may not be related to the current task.</ide_opened_file>
我写好了一版。但测试出来有结果错误。请你review看看

---

**077 · 助手** · `2026-10-14T05:34:18.172Z` · `msg-f79e8e05fd530f7a8133`

我先在一个隔离目录里把你的文件跑一遍解释器层和只编译层，拿到失败证据再看代码。

---

**078 · 助手** · `2026-10-14T05:36:04.884Z` · `msg-a2add4cbc567e2d04c88`

我在核对两件事：结果错误的根因（已定位），以及只编译层另外报出的两类失败各自来自哪几行。

---

**079 · 助手** · `2026-10-14T05:40:08.034Z` · `msg-2f2ceee02c5d0dd19468`

三个问题都已用实验确认。最后再核对一个小点：`num_stages` 只写在 K 循环的 `tl.range` 上、没作为发射参数传入时，循环合并后是否还生效。

---

**080 · 助手** · `2026-10-14T05:43:30.486Z` · `msg-5ad267629913412cc302`

Review 的结论已经清楚了。动笔前再做一个只为我自己确认的检查：写回时有没有重复写同一位置（这一项测试查不出来）。

---

**081 · 助手** · `2026-10-14T05:46:53.523Z` · `msg-799761c51d25f248af2d`

变体与参考实现的结果都和改动前一致。现在把这次 Review 的问题和帮助范围记进第 09 课记录，并更新 Checkpoint。

---

**082 · 助手** · `2026-10-14T05:49:08.352Z` · `msg-98b7ec72004122a46338`

你的首版我在本机跑过了，三个阻塞问题都定位到了。总体判断：主要是一个概念问题，即越界下标的处理办法只在某些方向上成立；另外 `flatten` 没按约定写，还碰上一个 Triton 编译时的作用域规则。下面只给失败证据、不变量和该回头看的地方，没指出出错的语句，改法留给你。卡住了随时问，我可以再往前提示一步。

在临时环境里跑了你的文件（Triton 3.7.1，只有 CPU，文件 SHA-256 前缀 `cfdced17`）：

| 层 | 结果 |
| --- | --- |
| 解释器层 | `27 failed, 19 passed, 12 skipped` |
| 只编译层 | `10 failed, 2 passed, 46 skipped` |

**已经对的部分**
- 包装函数的 9 项参数检查全过。
- 网格取 `min(num_sms, tile 数)`，步长等于实际发射的 CTA 数。
- `flatten` 关时，`num_sms` 取 1、3、7、64 都恰好调用 75 次 `tl.dot`（25 个 tile × 3 轮 K）。
- 手写的合并循环在结构上就是编译器合并后的样子：k 为 0 时进入新 tile，最后一轮写回，和节点 3 的骨架一致。
- `num_stages` 只写在 K 循环的 `tl.range` 上也没问题。我核对过，合并前后流水深度都跟着它变，和作为发射参数传入效果一样。

### R-01（阻塞，A1、A2）：结果错误全部来自 K 方向

- 27 项失败都是数值不一致。失败的形状全是 K 不是 `block_k` 整数倍的：partial-k、partial-all、smaller-than-a-block、one-element、wide，以及 150×130×40 和默认块下的 300×260×150。
- M 或 N 不整块、K 整块的 partial-m 和 partial-n 都通过了。
- 最小的例子：M=N=K=1，a=[[2]]，b=[[3]]，`block_k=16`。两种 `flatten` 下都输出 **96**，不是 6。
- 不变量：k ≥ K 的那些位置，对和的贡献必须恰好是 0。

请想清楚：同一套越界处理，为什么在 M、N 方向没让数值出错，在 K 方向却出错了？找到之后再查一下：同一个原因在 kernel 里还出现在另一处，那里数值碰巧不受影响，测试查不出来。

### R-02（阻塞，A3）：`flatten` 分支不是约定的写法，而且编译不过

- **约定的要求**：`flatten` 传给 tile 循环的 `tl.range(..., flatten=...)`，两种取值用同一份 kernel 代码。M1 依赖这一点：三个版本只改调度，测出的差别才能归到编译器的循环合并上。手写的合并循环是另一个程序。
- **编译报错**：只编译层有 8 项报 `NameError('offset_m is not defined')`，位置在 [lesson09_persistent_matmul.py:53](gpu/triton/lesson09_persistent_matmul.py#L53)。
- **解释器层为什么没报**：解释器按 Python 执行，上一轮赋值的变量这一轮还在。编译时则不同，Triton 要生成 SSA 形式的 IR：
  - `if` 之后只能看到进 `if` 之前就有的名字，或两个分支都赋值的名字；只在 `if` 里第一次赋值的名字，出了 `if` 就不存在；
  - 能跨轮次传下去的，也只有循环之前已定义的名字。

  所以解释器层通过，不等于能编译。
- **手写循环还多领了 tile**：
  - 25 个 tile 时 `tl.dot` 调用 78 次，应为 75；
  - 256×256×128、块 64 时调用 68 次，应为 64，还出现了除以 0 的警告；
  - 多出来的 tile 编号等于 tile 总数。M 方向 tile 数是 4 的倍数时（M1 的 8192/128=64 就是），`get_tid` 里的组内行数会算成 0，在 GPU 上是未定义行为。

这一条的改法就是约定本身。换成约定的写法后，上面这两处问题都不会再出现。

### R-03（阻塞，A4）：`flatten` 关时 A、B 都是同步读入

- **证据**：sm_89 和 sm_90 上，TTGIR 里还剩两条 fp16 的同步 `tt.load`，值名是 `%a_data_67` 和 `%b_data_70`，就是从[第 89 行](gpu/triton/lesson09_persistent_matmul.py#L89)和[第 94 行](gpu/triton/lesson09_persistent_matmul.py#L94)开始的两次读入。PTX 里一条 `cp.async` 也没有；共享内存只有 8,192 字节，没有分配流水用的输入缓冲。
- **不变量**：要发出 16 字节一组的异步拷贝，编译器必须能证明沿连续方向有 8 个相邻且对齐的 fp16。
- **回头看节点 1 的那组对照**：在行主序 B 上比较过五种越界写法：
  - 不处理；
  - `tl.where` 改成 0 并加连续性声明（教程的写法）；
  - `tl.where` 不加声明；
  - 取模；
  - 给读入加 mask。

  其中有一种会让读入退回逐元素的同步读。再想一想，A 沿哪个方向连续，B 沿哪个方向连续。

这一条只有只编译层看得出来，解释器不模拟读入方式。

### R-04（不阻塞）

两处测试没覆盖的小地方：
- `num_sms` 传入字符串时，代码先做 `<= 0` 比较，抛出的是 `TypeError`，约定要求的是 `ValueError`；
- 缺省的 `num_sms` 读的是当前 CUDA 设备，不是 `a` 所在的设备。单卡上没有区别。

### 接下来

1. 找出 R-01 的原因并修改。下次回复时用一两句话说明：为什么 M、N 方向那样处理不出错，K 方向却出错；同源的另一处在哪里。
2. 把 `flatten` 分支换成约定的写法：一个 kernel，tile 循环用 `tl.range(..., flatten=...)`，K 循环在它里面。
3. 两层都跑一遍（都不需要 GPU），贴回汇总行和 `sha256sum gpu/triton/lesson09_persistent_matmul.py` 的输出。改完后，只编译层里 `flatten` 开的那几项会接着检查两件事：合并是否生效，A 和 B 是否仍是异步拷贝。

**测试文件改了两处报错信息，判定标准没变：**
- 恰好一次的检查，现在先比 `tl.dot` 的调用次数，再比数值，免得数值错误把计数错误盖住；
- A4 失败时，会列出仍是同步读入的值名。

改完后参考实现照样全过，六个故意写错的变体也仍然都被报红。新测试文件的 SHA-256 前缀是 `aa8cd741`，在 GPU 机器上跑之前请先同步过去。

你的实现文件我没有动。这次 Review 的问题和给出的帮助已经记进第 09 课记录，Checkpoint 也更新了，都还没有提交。

---

**083 · 用户** · `2026-10-14T06:25:11.722Z` · `msg-7b200ccff2afbe2294fe`

K方向的错误是因为先做了where，然后才计算mask，此时offset上的值已经变成0了，那么mask就全是True了。flatten是由编译期自动优化是吗？不需要手动写合并循环和其中的头尾判断？只在外层循环上加一个flatten=True就行了是吗？

---

**084 · 助手** · `2026-10-14T06:26:49.369Z` · `msg-d040b75b7833602fed5f`

**R-01 的机制你说对了。** 先用 `tl.where` 把 ≥ K 的下标改成 0，再拿改过的下标算 mask，`offset_k < K` 就恒为真。结果 k ≥ K 的位置读进来的不是 0，而是 A 的第 0 列和 B 的第 0 行，每个输出都多加了几份 `a[m,0]·b[0,n]`。拿 1×1×1 来对：k=1…15 都读成了 k=0 的数据，和里多了 15 份 2×3，所以输出是 16×6=96。

上次的问题还有两半没答。用你刚找到的机制，把 M 方向也走一遍就能回答：
1. M、N 方向的 mask 同样恒为真，为什么数值没错？
2. 同源的另一处在哪里？

**`flatten`：是的，合并由编译器在编译期完成，不用手写合并循环和头尾判断。**
- `flatten=True` 写在外层 tile 循环的 `tl.range` 上，作用是给这个循环打上“请求合并”的标记。编译时，`tritongpu-fuse-nested-loops` 这个 pass 把两层循环合成一层。“k 为 0 时进入新 tile”和“最后一轮之后写回”这两段，它会自己生成两个 `scf.if`，就是你手写的那两个 `if`。
- 你 `else` 分支里的两层循环已经是要的形状。给 tile 循环的 `tl.range` 加上 `flatten=flatten`，再删掉 `if flatten:` 那个手写分支，两种取值就走同一份代码了。`flatten` 参数已经是 `tl.constexpr`，满足“必须是编译期常量”的要求。

不过“只加一个参数就行”要打两个折扣，节点 3 都讲过：
1. **它是请求，不是保证。** 编译器只合并两层嵌套：tile 循环里直接套一个 K 循环，中间没有别的 `if` 或循环；内层的边界也不能随外层变化（你的 K 是 kernel 参数，满足）。条件不满足时它不报错，两层循环原样保留。所以要看编译产物：`scf.if` 有没有出现，共享内存有没有变多。A3 的测试查的就是这两样。
2. **合并可能改变读入的编译方式。** Triton v3.7.1 在行主序的 B 上有一个已知的坑，节点 3 页面“代价”一节最后一条讲过。A4 在 `flatten` 开时查的、A6 要你解释的，就是你怎样处理它。

你找到 R-01 原因这件事我记进了第 09 课记录：原因是你自己找到的，这部分独立证据成立。还没有提交。

---

**085 · 用户** · `2026-10-14T06:33:12.694Z` · `msg-3fe402f4708f7af517e8`

M、N 方向没错是因为写入到C矩阵外面去了吧。同源的另一处就是M和N方向吧，写到外面去了，数值正巧不会出错。

---

**086 · 助手** · `2026-10-14T06:34:36.708Z` · `msg-e89d29bedcdad5ff2aae`

位置你找对了一半：同源的另一处确实在写回，就是 [第 72 行](gpu/triton/lesson09_persistent_matmul.py#L72)和[第 104 行](gpu/triton/lesson09_persistent_matmul.py#L104)的 mask。它用的也是被 `tl.where` 改过的 `offset_m`、`offset_n`，所以同样恒为真。但后果不是“写到 C 外面”。

**证据**
- **没写到 C 外面。** 测试在 C 的四周各留了 32 格哨兵值（−7），调用后检查这些格子有没有被改。partial-m 和 partial-n 两项连这一检查也通过了。真要是写到了 C 外面，这两项会报 `memory around the output was modified`。
- **写回落在了 C 里面，而且重复写。** 我在本机用解释器统计了你的写回落点（`flatten` 关，`num_sms=3`，块 32×32×16）：
  - partial-m（M=70）：C 的每个元素都写到了，但**第 0 行的每个元素各被写了 27 次**；
  - partial-n（N=50）：**第 0 列的每个元素各被写了 15 次**。

请用这两个数解释：
1. 为什么偏偏落在第 0 行（第 0 列）？为什么是 27 次（15 次）？
2. 同一个位置写了 27 次，为什么最后的值还是对的？

提示：`tl.where` 对 `offset_m` 做的事，要同时放到读入 A 和写回 C 两处去看，它们用的是同一个变量。

这一处测试查不出来，但它和 K 方向是同一个根因，建议一起改。

---

**087 · 用户** · `2026-10-14T06:39:43.268Z` · `msg-b78baa7e17101d3cffbc`

噢，offset超出位置改成了0，是重复写到了0位置上去。27次是1次正常写，26（32*3-70）次超出位置写。15次也是同样的道理。最后值还是对的是因为读到的值是正常的0位置的值，计算也是正常的，最后的值就由最后一次写回决定。就也是对的。

---

**088 · 助手** · `2026-10-14T06:40:08.474Z` · `msg-ce62d7b6297cfd0eeeeb`

对，三点都说对了：越界的行号被改成 0，写回到了第 0 行；27 = 1 次正常写 + 26 次越界写（32×3−70）；越界的那些行读的是 A 的第 0 行，算出来的正是第 0 行的值。15 次也一样：1 + (32×2−50)。

补充一点：“最后的值由最后一次写回决定”没错，但这 27 次写入来自不同的 CTA，谁先谁后是不确定的。结果之所以总是对，只是因为 27 次写入的值完全相同。这就是我说它“碰巧”的原因：只要哪天这些写入的值不一样了，结果就会随写入顺序变化。另外，26 次多余的写回本身也是白白占用的带宽。

R-01 的根因你已经完整讲清楚了，这部分理解证据记下了。接下来就是改代码：
1. K 方向和写回两处一起改（R-01）；
2. `flatten` 换成约定的写法（R-02）；
3. 处理 `flatten` 关时 A、B 的同步读入（R-03）；

改完把解释器层和只编译层都跑一遍，贴回汇总行和 `sha256sum gpu/triton/lesson09_persistent_matmul.py` 的输出。别忘了先把新的测试文件（SHA-256 前缀 `aa8cd741`）同步过去。

---

**089 · 用户** · `2026-10-14T06:58:49.666Z` · `msg-9108efb2879f8f95b189`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/gpu/triton/lesson09_persistent_matmul.py in the IDE. This may or may not be related to the current task.</ide_opened_file>
对于同步、异步读入部分。我觉得应该是要加上连续性声明max_contiguous。但我加上了offset_m = tl.max_contiguous(tl.multiple_of(offset_m, BLOCK_M), BLOCK_M)和offset_k = tl.max_contiguous(tl.multiple_of(offset_k, BLOCK_K), BLOCK_K)还是显示没有异步

---

**090 · 助手** · `2026-10-14T06:59:38.576Z` · `msg-68861db2e310107da28b`

你的新版本把循环改成了约定的写法，mask 也挪到了 `tl.where` 前面。我先在本机跑一遍两层测试，看清楚现在是哪个读入还在同步。

---

**091 · 助手** · `2026-10-14T07:03:27.816Z` · `msg-2e77299966032c1092b3`

你这一版（SHA-256 前缀 `8baef278`）进步很大，我在本机用新测试文件跑了两层：

| 层 | 结果 |
| --- | --- |
| 解释器层 | `46 passed, 12 skipped` |
| 只编译层 | `4 failed, 8 passed, 46 skipped` |

- **R-01 已关闭**：mask 挪到 `tl.where` 之前算，1×1×1 现在输出 6。我统计了写回落点，partial-m 和 partial-n 都没有重复写入了。
- **R-02 已关闭**：改成了 `tl.range(..., flatten=flatten)`。只编译层里合并的两项和网格的四项在 sm_89、sm_90 上都过了；`flatten` 开时，四种 `num_sms` 下都恰好 75 次 `tl.dot`。

剩下的 4 项失败全是 A4，而且同步读入只剩 B 一个（报错里的值名是 `%b_data_*`），两种 `flatten` 下都是。

**你的方向是对的。** `offset_k` 上的声明确实起了作用，A 正是因为它变成了 16 字节的异步拷贝。所以问题缩小到了 B：一个操作数能不能 16 字节一组地搬，看的是它沿自己连续方向的那个下标。请对照一下：
- A 是 `[M, K]`，B 是 `[K, N]`，都按行主序存放，各自沿哪个方向连续？
- 你加的两个声明，分别落在 A 的哪个方向、B 的哪个方向上？

B 在 `flatten` 关时那两项改对后就会通过。`flatten` 开的两项如果还剩 B，就回到上次说的节点 3 页面“代价”一节最后一条。

另外，R-04 的两处不阻塞的小地方还在，可以顺手改。记录里已关闭 R-01、R-02，Checkpoint 指向 R-03，都还没有提交。

---

**092 · 用户** · `2026-10-14T07:08:07.419Z` · `msg-ec1c0d8299b81e18308f`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/gpu/triton/lesson09_persistent_matmul.py in the IDE. This may or may not be related to the current task.</ide_opened_file>
A 沿K方向连续，B沿N方向连续。所以我应该写offset m和k的声明吗？

---

**093 · 用户** · `2026-10-14T07:08:15.879Z` · `msg-53ba40c01723838f8cc6`

[Request interrupted by user]

---

**094 · 用户** · `2026-10-14T07:08:15.893Z` · `msg-24e99846de0e2876ece3`

<task-notification>
<task-type>artifact-auto-react</task-type>
<summary>3 artifact auto-reply subscriptions paused by the interrupt (comments sent to Claude meanwhile are answered then)</summary>
The user's interrupt paused them and the watches are kept; when the user asks you to publish these artifacts again, that publish resumes them, or resume_replies if the user asks, as does the user's next typed message — each only on hosts that pass typed input through as the user's, and comments sent to Claude in the meantime are answered then; publishing without being asked, while handling a notification or a wake-up, leaves them paused. Do not republish or resume just to re-enable auto-replies unless the user asks.
</task-notification>

---

**095 · 用户** · `2026-10-14T07:08:18.980Z` · `msg-e38f96a7af3c3eb183be`

[Request interrupted by user]

---

**096 · 助手** · `2026-10-14T07:11:01.150Z` · `msg-e56f9b72336a82187ad7`

No response requested.

---

**097 · 用户** · `2026-10-14T07:11:24.564Z` · `msg-f9a764a03d60f2358121`

A 沿K方向连续，B沿N方向连续。所以我应该写offset k和n的声明吗？

---

**098 · 助手** · `2026-10-14T07:11:35.510Z` · `msg-31ef5ee8b80468ad3395`

对，就是这样。读入要能 16 字节一组地搬，看的是这个操作数沿自己连续方向的那个下标：
- **A 看 `offset_k`。** 你已经加过声明，所以 A 现在是异步拷贝。
- **B 看 `offset_n`。** 它还被 `tl.where` 改写过，又没有声明，所以 B 仍是同步读入。

`offset_m` 是 A 跨行的方向，那里的声明对读入不起作用，留着也无害。同理，`offset_k` 对 B 来说也是跨行的方向，它的声明只帮到了 A。

还有一点值得想清楚：为什么需要声明？`tid_n * BLOCK_N + tl.arange(0, BLOCK_N)` 本身是连续的，编译器自己就知道。是 `tl.where` 把一部分值换成 0 之后，编译器才不再能确定它连续，声明的作用是把这条信息补回去。节点 1 那组对照里，出问题的正是“`tl.where` 不加声明”那一种，原因就在这里。顺着这个道理，N 方向其实有两种改法，你自己挑。

改完先看只编译层 `flatten` 关的两项。`flatten` 开的两项如果还剩 B，就回到节点 3 页面“代价”一节最后那条。

---

**099 · 用户** · `2026-10-14T07:12:48.088Z` · `msg-ba510a2d3378cc72ac56`

那教程里为什么用的m和n方向的声明？教程里不应该是k方向连续吗？

---

**100 · 助手** · `2026-10-14T07:13:19.224Z` · `msg-ad88aa72d75a35c17b81`

你说得对，在教程的调用方式下，A 和 B 都沿 K 连续：
- A 是 `[M, K]` 行主序；
- B 在第 660 行先存成连续的 `[N, K]`，第 668 行再以 `b.T` 传进 pointer kernel。所以 kernel 里 B 的 `stride_bk = 1`，同样沿 K 连续。

那声明为什么写在 M、N 上？因为**声明只用来修补被 `tl.where` 抹掉的信息，而教程只对 M、N 用了 `tl.where`**：
- **K 方向没有声明，也不需要。** 第 325 行 `offs_k = ki * BLOCK_SIZE_K + tl.arange(0, BLOCK_SIZE_K)` 没经过 `tl.where`，编译器自己就看得出它连续。K 的越界靠第 329–330 行的 mask 处理（`other=0.0`），没有把下标改成 0。
- **M、N 方向经过了 `tl.where`**（第 318–319 行），连续性信息被抹掉，所以紧接着在第 320–321 行补上声明。

在教程自己的调用方式下，这两行声明对读入其实不起作用。节点 1 那组对照里，B 用 `b.T` 传入时，五种写法（包括“`tl.where` 不加声明”）都是 24 条 16 字节的 `cp.async`，因为 M、N 只是跨行的方向。

它们起作用的场景，恰好是你现在的情形：B 按行主序 `[K, N]` 传入，连续方向变成 N。这个 kernel 的步长是运行时参数（`stride_bk`、`stride_bn`），写 kernel 时并不知道哪个方向连续；Triton 会把值为 1 的整数参数特化，传进来后才确定。教程在 M、N 上都补了声明，A、B 换成别的存放方式也照样能成组搬运。

所以规则只有一条：**哪个方向是操作数的连续方向，就要保证编译器在那个方向上看得出连续。** 没碰过的下标编译器自己知道，被 `tl.where` 改过的才需要声明。你把 K 也改成了 `tl.where`，所以 K 要声明；N 也改过，所以 N 同样要声明，或者干脆不在 N 上用 `tl.where`。

---

**101 · 用户** · `2026-10-14T07:19:07.768Z` · `msg-5b8e7122c8f56f7eadb1`

啊这，教程里加的声明实际上并没起作用，这不误导人吗？行吧。我明白了。我改好了。但遇到了如下报错：

<pasted_content id="b992">
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_flatten_fuses_the_two_loops[sm_89] - AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_flatten_fuses_the_two_loops[sm_90] - AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_both_operands_use_16_byte_async_copies[sm_89-flatten-on] - AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_87'] (TTGIR names each value after the variable it was assigned to)
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_both_operands_use_16_byte_async_copies[sm_90-flatten-on] - AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_83'] (TTGIR names each value after the variable it was assigned to)
4 failed, 46 passed, 8 skipped in 2.38s
</pasted_content id="b992">

---

**102 · 助手** · `2026-10-14T07:20:16.791Z` · `msg-190f4b144be1c2b9fdea`

**先说教程。** 你的意见有一半在理：教程没说明这两行声明是为谁写的，读的人很容易以为它们对 `b.T` 这种传法也起作用。但这两行不算错，更像一份不花成本的保险。这个 kernel 的步长都是参数，换一种存放方式传进来（比如你的行主序 B），它们就起作用了。另外要说明，“没起作用”这个结论我只在 sm_89 上对比过读入方式，没有覆盖所有目标和所有方面。

**再说你的结果。** 我用你现在的文件（SHA-256 前缀 `fa0fe29e`）在本机复现了这 4 项失败。

| sm_89 | `flatten` 关 | `flatten` 开 |
| --- | --- | --- |
| `scf.if` | 0 | 4（合并生效了） |
| 16 字节 `cp.async` | 12 条（A、B 都是） | 6 条（只剩 A） |
| 共享内存 | 16,384 | 16,384 |

sm_90 上也一样，`flatten` 开时只剩 A 是异步拷贝，共享内存反而从 24,576 降到了 20,480。

- **`flatten` 关已经解决。** A、B 都是 16 字节异步拷贝，那两项通过了，R-03 完成了一半。
- **这 4 项失败是同一个原因。** `flatten` 开时 B 退回了同步读入，参与流水的只剩 A，需要的输入缓冲就少了，所以共享内存没有增加，A3 的共享内存检查跟着失败。B 改好以后，这一项应该会一起转绿。

这就是我前两次提到的节点 3 页面“代价”一节最后那条。原文是：

> B 按普通的行主序 `[K, N]` 存放时，合并后只有 A 保持异步拷贝，B 变成同步读入。原因是带连续性声明的列偏移变成了 `scf.if` 的输出，流水挑选读入时取不到这条声明。

你手写过合并循环，可以拿它来对照：合并后，你 kernel 里哪些代码会被放进“k 为 0 时进入新 tile”的那个 `if` 里？B 的读入用到的哪个值从那里出来？想清楚后，怎么让 B 的读入不再依赖它，你就能自己定了。这也正是 A6 要你解释的第一点。

另外确认一下：你贴的结果是 `4 failed, 46 passed, 8 skipped`，说明是在有 GPU 的机器上跑的，GPU 数值层也全过了。下次贴结果时请附上这两行输出，我好把 GPU 上的通过记进去：
- `python -c "import torch; print(torch.cuda.get_device_name())"`
- `sha256sum gpu/triton/lesson09_persistent_matmul.py`

记录已经更新：A3 的这项失败并入了 R-03，没有另开新问题。

---

**103 · 用户** · `2026-10-14T07:25:07.000Z` · `msg-a1a7d0c7cbef04e52b81`

原因是因为flatten开的时候会引入if，对K循环头尾进行特殊处理是吗？那为什么A还能保持呢？结果信息如下：

<pasted_content id="b992">
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# pytest -q gpu/triton/lesson09_persistent_matmul_test.py
..............................ssssssss.............FF.F.F.                                                                                                            [100%]
================================================================================= FAILURES ==================================================================================
__________________________________________________________________ test_flatten_fuses_the_two_loops[sm_89] __________________________________________________________________

ops = <module 'gpu.triton.lesson09_persistent_matmul' from '/root/workspace/programming-lab/gpu/triton/lesson09_persistent_matmul.py'>
recorder = <gpu.triton.lesson09_persistent_matmul_test._RecordingDriver object at 0x7f213ffddbb0>

    def test_flatten_fuses_the_two_loops(ops: ModuleType, recorder: _RecordingDriver) -> None:
        """A3: with flatten the loop nest is fused, which costs shared memory; without it, not."""
        plain = _compile(ops, recorder, num_sms=3, flatten=False)
        fused = _compile(ops, recorder, num_sms=3, flatten=True)
        assert "ttg.async_copy_global_to_local" in plain.asm["ttgir"], "the K loop must be pipelined"
        assert fused.asm["ttgir"].count("scf.if") > plain.asm["ttgir"].count("scf.if"), (
            "flatten=True left the loop nest as it was: the request was ignored"
        )
>       assert fused.metadata.shared > plain.metadata.shared, (
            "a fused loop keeps the input buffers busy during the epilogue and needs more shared memory"
        )
E       AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
E       assert 16384 > 16384
E        +  where 16384 = KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm89', backend_name=...PUTarget(backend='cuda', arch=89, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32).shared
E        +    where KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm89', backend_name=...PUTarget(backend='cuda', arch=89, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32) = <triton.compiler.compiler.CompiledKernel object at 0x7f213ffde450>.metadata
E        +  and   16384 = KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm89', backend_name=...PUTarget(backend='cuda', arch=89, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32).shared
E        +    where KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm89', backend_name=...PUTarget(backend='cuda', arch=89, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32) = <triton.compiler.compiler.CompiledKernel object at 0x7f213ffdf7d0>.metadata

gpu/triton/lesson09_persistent_matmul_test.py:441: AssertionError
__________________________________________________________________ test_flatten_fuses_the_two_loops[sm_90] __________________________________________________________________

ops = <module 'gpu.triton.lesson09_persistent_matmul' from '/root/workspace/programming-lab/gpu/triton/lesson09_persistent_matmul.py'>
recorder = <gpu.triton.lesson09_persistent_matmul_test._RecordingDriver object at 0x7f213ffa2990>

    def test_flatten_fuses_the_two_loops(ops: ModuleType, recorder: _RecordingDriver) -> None:
        """A3: with flatten the loop nest is fused, which costs shared memory; without it, not."""
        plain = _compile(ops, recorder, num_sms=3, flatten=False)
        fused = _compile(ops, recorder, num_sms=3, flatten=True)
        assert "ttg.async_copy_global_to_local" in plain.asm["ttgir"], "the K loop must be pipelined"
        assert fused.asm["ttgir"].count("scf.if") > plain.asm["ttgir"].count("scf.if"), (
            "flatten=True left the loop nest as it was: the request was ignored"
        )
>       assert fused.metadata.shared > plain.metadata.shared, (
            "a fused loop keeps the input buffers busy during the epilogue and needs more shared memory"
        )
E       AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
E       assert 20480 > 24576
E        +  where 20480 = KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm90', backend_name=...PUTarget(backend='cuda', arch=90, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32).shared
E        +    where KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm90', backend_name=...PUTarget(backend='cuda', arch=90, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32) = <triton.compiler.compiler.CompiledKernel object at 0x7f213ffecbf0>.metadata
E        +  and   24576 = KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm90', backend_name=...PUTarget(backend='cuda', arch=90, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32).shared
E        +    where KernelMetadata(allowed_dot_input_precisions=['tf32', 'tf32x3', 'ieee', 'bf16x3', 'bf16x6'], arch='sm90', backend_name=...PUTarget(backend='cuda', arch=90, warp_size=32), tensordesc_meta=[], tmem_size=0, triton_version='3.7.1', warp_size=32) = <triton.compiler.compiler.CompiledKernel object at 0x7f213ffa2cc0>.metadata

gpu/triton/lesson09_persistent_matmul_test.py:441: AssertionError
_______________________________________________________ test_both_operands_use_16_byte_async_copies[sm_89-flatten-on] _______________________________________________________

ops = <module 'gpu.triton.lesson09_persistent_matmul' from '/root/workspace/programming-lab/gpu/triton/lesson09_persistent_matmul.py'>
recorder = <gpu.triton.lesson09_persistent_matmul_test._RecordingDriver object at 0x7f213ffee000>, flatten = True

    @pytest.mark.parametrize("flatten", FLATTEN_VALUES)
    def test_both_operands_use_16_byte_async_copies(
        ops: ModuleType, recorder: _RecordingDriver, flatten: bool
    ) -> None:
        """A4: with whole blocks and aligned inputs neither A nor B falls back to synchronous loads."""
        kernel = _compile(ops, recorder, num_sms=3, flatten=flatten)
        synchronous = re.findall(r"(%[\w.]+) = tt\.load [^\n]*ptr<f16>", kernel.asm["ttgir"])
>       assert not synchronous, (
            f"these fp16 loads were not turned into asynchronous copies: {synchronous} "
            "(TTGIR names each value after the variable it was assigned to)"
        )
E       AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_87'] (TTGIR names each value after the variable it was assigned to)
E       assert not ['%b_data_87']

gpu/triton/lesson09_persistent_matmul_test.py:454: AssertionError
_______________________________________________________ test_both_operands_use_16_byte_async_copies[sm_90-flatten-on] _______________________________________________________

ops = <module 'gpu.triton.lesson09_persistent_matmul' from '/root/workspace/programming-lab/gpu/triton/lesson09_persistent_matmul.py'>
recorder = <gpu.triton.lesson09_persistent_matmul_test._RecordingDriver object at 0x7f213ffeeed0>, flatten = True

    @pytest.mark.parametrize("flatten", FLATTEN_VALUES)
    def test_both_operands_use_16_byte_async_copies(
        ops: ModuleType, recorder: _RecordingDriver, flatten: bool
    ) -> None:
        """A4: with whole blocks and aligned inputs neither A nor B falls back to synchronous loads."""
        kernel = _compile(ops, recorder, num_sms=3, flatten=flatten)
        synchronous = re.findall(r"(%[\w.]+) = tt\.load [^\n]*ptr<f16>", kernel.asm["ttgir"])
>       assert not synchronous, (
            f"these fp16 loads were not turned into asynchronous copies: {synchronous} "
            "(TTGIR names each value after the variable it was assigned to)"
        )
E       AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_83'] (TTGIR names each value after the variable it was assigned to)
E       assert not ['%b_data_83']

gpu/triton/lesson09_persistent_matmul_test.py:454: AssertionError
========================================================================== short test summary info ==========================================================================
SKIPPED [8] gpu/triton/lesson09_persistent_matmul_test.py:234: the exactly-once check counts tl.dot calls and needs TRITON_INTERPRET=1
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_flatten_fuses_the_two_loops[sm_89] - AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_flatten_fuses_the_two_loops[sm_90] - AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_both_operands_use_16_byte_async_copies[sm_89-flatten-on] - AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_87'] (TTGIR names each value after the variable it was assigned to)
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_both_operands_use_16_byte_async_copies[sm_90-flatten-on] - AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_83'] (TTGIR names each value after the variable it was assigned to)
4 failed, 46 passed, 8 skipped in 2.55s
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# python -c "import torch; print(torch.cuda.get_device_name())"
NVIDIA GeForce RTX 5090
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# sha256sum gpu/triton/lesson09_persistent_matmul.py
fa0fe29e9fef37ba6da3e240a79bbb28be1ce2dd130d014554ec6668beae6013  gpu/triton/lesson09_persistent_matmul.py
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# 
</pasted_content id="b992">

 接下来我还要改吗？

---

**104 · 助手** · `2026-10-14T07:25:53.622Z` · `msg-699738e6b245e8f8302c`

还要改。完成门槛是 A1–A5 全部通过，这 4 项失败都是同一个原因：`flatten` 开时 B 退回了同步读入。A3 的共享内存一项也是它带出来的，B 改好后会跟着转绿。

先说好消息：你在 RTX 5090 上跑的这一版（哈希 `fa0fe29e`，和我本机的一致）其余 46 项全过了。A1、A2、A5 在 GPU 上的数值和参数检查都通过，R-01 的 GPU 证据我已经补进记录。

**一处更正：合并引入的 `if` 不是处理 K 循环的头尾。** 它包住的是 tile 的 prologue 和 epilogue，也就是原先在 tile 循环里、K 循环之外的那些代码：
- K 循环之前的部分：算 tile 坐标、算下标和 mask、把 `acc` 清零；
- K 循环之后的部分：写回。

合并后只剩一个大循环，这两段分别在“k 为 0”和“最后一轮”时才执行，所以各包进一个 `if`。K 循环的预热和排空是另一回事，由流水负责，合并后每个 CTA 只做一次，节点 3 区分过这两样。

**机制是这样的：**
- 在 prologue 那个 `if` 里算出来的值，要作为 `if` 的结果传出来。不进 `if` 的那些轮次，沿用上一次的值。经过这条路径之后，流水阶段看不到附在它上面的连续性声明了。
- 流水在挑选哪些读入可以改成异步拷贝时，只检查一件事：在这个操作数的连续方向上，地址能不能证明是连续的。

**A 为什么还能保持？** 请你自己对一下：
- A 的连续方向是 K，决定它的下标是哪个变量？这个变量在哪里算：在 prologue 的 `if` 里，还是在每一轮都执行的 K 循环体里？
- B 的连续方向是 N，同样的问题再答一遍。

两个问题答完，你就知道该怎么改了。改完先跑只编译层，`flatten` 开的 A4 和 A3 的共享内存这两类应该会一起转绿；然后照旧在 5090 上跑一遍完整的测试。

---

**105 · 用户** · `2026-10-14T07:33:43.085Z` · `msg-74df1c211b56261d9190`

A的offset_k在K循环里算，B的offset_n在if里算。所以我要把这俩声明都放到K循环里面去吗？我改了后还是报错：

<pasted_content id="b992">
========================================================================== short test summary info ==========================================================================
SKIPPED [8] gpu/triton/lesson09_persistent_matmul_test.py:234: the exactly-once check counts tl.dot calls and needs TRITON_INTERPRET=1
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_flatten_fuses_the_two_loops[sm_89] - AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_flatten_fuses_the_two_loops[sm_90] - AssertionError: a fused loop keeps the input buffers busy during the epilogue and needs more shared memory
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_both_operands_use_16_byte_async_copies[sm_89-flatten-on] - AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_87'] (TTGIR names each value after the variable it was assigned to)
FAILED gpu/triton/lesson09_persistent_matmul_test.py::test_both_operands_use_16_byte_async_copies[sm_90-flatten-on] - AssertionError: these fp16 loads were not turned into asynchronous copies: ['%b_data_83'] (TTGIR names each value after the variable it was assigned to)
4 failed, 46 passed, 8 skipped in 2.34s
</pasted_content id="b992">

---

**106 · 助手** · `2026-10-14T07:34:39.509Z` · `msg-e2f188c02c291077a376`

你的判断是对的：A 的 `offset_k` 在 K 循环里算，B 的 `offset_n` 在 `if` 里算，差别就在这里。改了没生效，是因为“声明”在 IR 里的样子和直觉不一样：**它不产生新值，只是给定义这个值的那条操作贴一个标签。**

看 Triton 3.7.1 的 `semantic.py` 第 1824 行，`tl.max_contiguous` 做的事情只有一件：

```python
x.handle.set_attr("tt.contiguity", ...)
return x
```

它把属性挂在算出 `x` 的那条操作上，然后原样返回 `x`。在你的 TTGIR 里，这个标签挂在 prologue 里那条 `arith.select`（即 `tl.where`）上：

```
%offset_n_21 = arith.select %mask_n_20, %offset_n_19, %cst_4 {tt.contiguity = dense<64> ..., tt.divisibility = dense<64> ...}
```

所以声明写在哪一行都一样：标签总是贴回值诞生的地方。值在 prologue 的 `if` 里诞生，标签就留在 `if` 里，流水照样看不到。

我拿你的文件做了个私下副本，只把 `offset_n` 那行声明挪进 K 循环，编译出的 TTGIR 和原来逐字相同，同步读入的值名也还是 `%b_data_87`，正是你贴的那个。我猜你的改动就是这样。你这台机器上的文件还是 `fa0fe29e`，我看不到你在 GPU 机器上的改动，有出入就告诉我。

**要挪进 K 循环的不是声明，而是 B 在 N 方向那个下标的计算本身。** 值在 K 循环体里诞生，贴在它身上的标签才在流水看得到的地方。A 一直没问题，正是因为 `offset_k` 从头到尾都是在 K 循环里算的。

改完后：
1. 先跑只编译层；
2. 再在 5090 上跑完整测试，贴回汇总行和 `sha256sum` 的输出；
3. 把文件同步回这边，我好看代码。

---

**107 · 用户** · `2026-10-14T07:43:58.671Z` · `msg-6e1df43c3d722e803088`

好的。我修改好了。测试通过了。

<pasted_content id="b992">
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# pytest -q gpu/triton/lesson09_persistent_matmul_test.py
..............................ssssssss....................                                                                                                            [100%]
========================================================================== short test summary info ==========================================================================
SKIPPED [8] gpu/triton/lesson09_persistent_matmul_test.py:234: the exactly-once check counts tl.dot calls and needs TRITON_INTERPRET=1
50 passed, 8 skipped in 2.25s
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# sha256sum gpu/triton/lesson09_persistent_matmul.py
48b15b990d565f95b2b0dbf493dae1aae89e9cf993891c80bf73b5a4c93c8439  gpu/triton/lesson09_persistent_matmul.py
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# 





</pasted_content id="b992">

---

**108 · 助手** · `2026-10-14T07:45:24.283Z` · `msg-c4119c71b5c8e6048d16`

R-03 修好了。我先在本机核对这一版（`48b15b99`，和你 5090 上的一致），再看代码。

---

**109 · 助手** · `2026-10-14T07:48:48.526Z` · `msg-32071e5953c12307a0c0`

按现行测试，这一版全部通过了：
- RTX 5090 上 `50 passed, 8 skipped`，哈希 `48b15b99`，和本机的文件一致；
- 本机解释器层 `46 passed, 12 skipped`，只编译层 `12 passed, 46 skipped`。

R-03 关闭了。R-04 的两处你也顺手改好了（先查类型再比大小，缺省值读 `a` 所在的设备），一并关闭。

**但 Review 时我发现了验收测试的一个缺口，责任在我：`flatten` 开时，你这一版的合并循环没有流水。**

| sm_89（sm_90 相同） | `flatten` 关 | `flatten` 开 |
| --- | --- | --- |
| 循环开始前预先发出的拷贝 | 有 | 没有 |
| 循环里的 `ttg.async_wait` | `num = 2`：等的时候还有两轮在路上 | `num = 0`：发出一次就等它完成一次 |
| `async_copy` 出现的处数 | 6 | 2 |

也就是说，`flatten` 开时虽然用的是“异步拷贝”指令，但每轮发出后立刻等它做完，效果和同步读入一样：tile 内、tile 之间都没有任何提前量。共享内存变多是因为别的原因（输入缓冲不再和写回用的中转缓冲共用空间），所以 A3 也通过了。我的测试只查了“是不是异步拷贝”和“共享内存有没有变多”，没查“有没有提前发出”。

**这件事会直接影响 M1。** 用现在这一版测，`flatten` 关与开比的就是“有流水”对“没流水”，`flatten` 开会显得更慢，而原因和跨 tile 流水毫无关系。A6 说的“保住异步拷贝”，要保住的其实是提前量。

**往哪里看。** 不变量是：要在第 i 轮就发出第 i+2 轮的读入，第 i+2 轮的地址必须能直接由轮次号和 tile 内不变的值算出来。请回想你上次遇到 `NameError` 时那条规则：循环之前已有的名字，在循环里被重新赋值，就会跨轮次传下去。你的 K 循环里，有没有给这样一个名字重新赋值？这会让 B 的地址变成什么？

我用私下副本验证过：只改掉这一点，`flatten` 开时就恢复成 6 处拷贝、`num = 2`，现有测试也都还通过。至于流水的 pass 为什么因此放弃，我没有去读它的源码，上面的不变量是我的推断；实验现象是确定的。

**需要你确认一个约定澄清，这会成为版本 3。** A4 现在写的是：

> `flatten` 两种取值下 A、B 都是 16 字节一组的异步拷贝，TTGIR 里没有同步的 fp16 读入

我想补一句：

> 并且读入是提前发出的：两种取值下，循环里的 `ttg.async_wait` 等待时仍允许有拷贝在途（`num` 大于 0），而不是每次拷贝后立即等它完成

检查方式是只编译层，sm_89 和 sm_90 上两种取值各一项，其余不变。我已经私下试过这项检查：参考实现四项都过；你现在的版本只有 `flatten` 开的两项不过。这一条改变了完成门槛，所以需要你同意。同意后我把测试补上，你再改 R-05；R-05 关闭后，我交付 M1 的测量脚本。

记录里已关闭 R-03、R-04，新增 R-05（等你确认澄清），Checkpoint 也更新了，都还没有提交。

---

**110 · 用户** · `2026-10-14T08:01:31.528Z` · `msg-3acd262c9f72fb666572`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/gpu/triton/lesson09_persistent_matmul.py in the IDE. This may or may not be related to the current task.</ide_opened_file>
我明白了，offset_n应该要tile内不变，才能计算后面轮的地址。但k循环里改了offset_n，导致了无法流水化。我再修改了一下。我同意新的约定版本。你可以添加上测试后再测下。我在5090上测试修改后的版本依旧是全过的。

---

**111 · 助手** · `2026-10-14T08:06:18.357Z` · `msg-095fbadd0c8069a84599`

现在写 M1 的测量脚本。

---

**112 · 助手** · `2026-10-14T08:07:54.890Z` · `msg-ab9e84f9f256b13366d0`

测量脚本写好了，正在过 lint 和类型检查，然后在本机用解释器做一次小规模的冒烟运行。

---

**113 · 助手** · `2026-10-14T08:09:32.518Z` · `msg-a40617a895de2861deb6`

版本 3 的测试已经补上，你这一版（`6d628fbc`）全部通过，R-05 关闭。到这里 A1–A5 都过了。

**新测试**

新增“读入提前发出”一项：sm_89、sm_90 × `flatten` 两种取值，共 4 项，测试总数变成 62。判定规则是：循环里至少有一处 `ttg.async_wait` 的 `num` 大于 0。

| 对象 | 只编译层 |
| --- | --- |
| 你的第五版 `6d628fbc` | `16 passed`（解释器层 `46 passed`） |
| 你的第四版 `48b15b99` | 只有 `flatten` 开的两项失败，正是上次那个问题 |
| 参考实现 | 全过 |
| 原有六个故意写错的变体 | 结果不变 |
| 新增第七个变体（照第四版的问题写） | 同样被报红 |

**更正我上次的解释。** 我说“K 循环里给循环前已有的名字重新赋值，它跨轮传递，流水就算不出后面几轮的地址”，这个说法过宽了。为了做第七个变体，我补了对照实验：

| 写法（私下变体，`flatten` 开） | 有没有提前量 |
| --- | --- |
| `offs_n` 在 K 循环里被重新赋值、跨轮传递，写回另算下标 | 有（`num = 2`） |
| 同上，但写回直接用 K 循环结束后的这个 `offs_n` | 没有（`num` 全为 0） |

所以光是跨轮传递并不会让流水失效。失效发生在这个跨轮传递的值既被读入用、又被 K 循环之后的写回用的时候，你的第四版正是这样。流水 pass 为什么因此放弃，我仍然没读源码确认。你的第五版两点都避开了（K 循环里由 `tid_n` 重新算，写回前另算一份），结论不受影响。

还有一点：你说“`offset_n` 应该 tile 内不变”。按数值看，第四版的 `offset_n` 其实一直是 tile 内不变的，因为 `tl.where` 重复做也是同一个结果。问题出在编译器看到的依赖关系上，不在数值上。这条更正记进了记录。

**M1 的测量脚本已交付：** [lesson09_persistent_matmul_benchmark.py](gpu/triton/lesson09_persistent_matmul_benchmark.py)。设置思路如下：
- **三种调度，只改调度。** 都用你的同一个 kernel、同一份输入，块 128×128×64、3 个 stage、8 个 warp，`M = N = 8192`，K 取 128、512、2048：
  - 逐 tile：`num_sms` 等于 tile 数（4096），`flatten` 关；
  - 持久、`flatten` 关：每个 SM 一个 CTA；
  - 持久、`flatten` 开：每个 SM 一个 CTA。
- **轮换交替，抵消漂移。** 共 15 轮，每轮按轮换的顺序，把每个 K 下的三个版本各测一次。每次测量是 `do_bench` 的一小段：预热 5 ms，重复 20 ms，每次运行前清空 L2，取中位数。
- **比值在同一轮内相除。** 时钟、温度的漂移在一轮内对三个版本是一样的，先在轮内相除就能抵掉。之后报各轮比值的中位数和四分位区间。
- **判据在测量前打印。** 主判据是 S(K) = 逐 tile 的时间 / 持久（`flatten` 开）的时间：
  - **支持**：S 的中位数随 K 依次下降，且 S(128) 与 S(2048) 的四分位区间不重叠；
  - **否定**：S(2048) 不小于 S(128) 且两端区间不重叠（反而增大），或者两端区间重叠而宽度都小于 0.03（测得够准，却没有变化）；
  - **证据不足**：其余情形。

  `flatten` 关的比值按同样的判据列为辅助。
- **先核对正确性。** 测量前逐项检查结果（最大相对误差不超过 1e-2），并列出各版本的共享内存、寄存器和溢出，供你解释结果时用。

这台机器没有 GPU，脚本只做过冒烟运行：在 CPU 上用解释器、小尺寸和合成计时，跑通了全部流程，判据的五种情形也都判对了。真实数字要等 5090 的结果。

**接下来**
1. 把这两个文件同步到 5090：测试文件（SHA-256 前缀 `ecffbf59`）和测量脚本（`01fbd235`）。
2. 在仓库根目录依次运行，并把全部输出贴回：
   - `pytest -q gpu/triton/lesson09_persistent_matmul_test.py`
   - `python -m gpu.triton.lesson09_persistent_matmul_benchmark`
3. 看到结果后写 M1：5–8 句，对照你在 2026-10-12 的预测，说明证据支持什么、不支持什么，还剩哪些不确定。
4. 写 A6：3–5 句，说明行主序的 B 在 `flatten` 下你是怎样保住异步拷贝的，以及 epilogue 为什么要有自己的游标。A6 现在就可以写，不必等测量。

记录已更新：约定升到版本 3，R-05 已关闭，教学更正、测量设计和 Checkpoint 都记下了。都还没有提交。

---

**114 · 用户** · `2026-10-14T08:13:18.169Z` · `msg-eb0eaa0aea635ac3b3bd`

结果如下：

<pasted_content id="b992">
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# pytest -q gpu/triton/lesson09_persistent_matmul_test.py
..............................ssssssss........................                                                                                                        [100%]
========================================================================== short test summary info ==========================================================================
SKIPPED [8] gpu/triton/lesson09_persistent_matmul_test.py:234: the exactly-once check counts tl.dot calls and needs TRITON_INTERPRET=1
54 passed, 8 skipped in 2.44s
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab# python -m gpu.triton.lesson09_persistent_matmul_benchmark
== Environment
GPU NVIDIA GeForce RTX 5090, capability (12, 0), 170 SMs
torch 2.13.0+cu130 (CUDA 13.0), triton 3.7.1
SHA-256 of the learner's file: 6d628fbcd167fefb88f6fa81d4dc6dcfe1cb11ad0bc3c90db76a7a1bb6c857e3
== Setup
M = N = 8192, K in [128, 512, 2048], blocks and launch options {'block_m': 128, 'block_n': 128, 'block_k': 64, 'num_stages': 3, 'num_warps': 8}
  one-tile        grid  4096 CTAs, flatten False
  persistent-off  grid   170 CTAs, flatten False
  persistent-on   grid   170 CTAs, flatten True
4096 tiles; 15 rounds, each timing every schedule once per K, order rotated.
One timing = median of a do_bench burst (5 ms warm-up, 20 ms repeat,
L2 flushed before every run). Statistics are over rounds; ratios are taken per round.

== Prediction and criteria (printed before measuring)
Prediction (learner, 2026-10-12): the TFLOPS ratio of the persistent kernel over
one tile per CTA falls as K grows; refuted if it does not change or grows instead.
S(K) = time(one-tile) / time(persistent-on) is the primary ratio; the same criteria
are also applied to persistent-off as a secondary ratio.
  SUPPORTED: the medians of S fall at every step and the interquartile ranges of
             S(128) and S(2048) do not overlap;
  REFUTED: S(2048) is not below S(128) and the two ranges do not overlap,
           or the two ranges overlap while both are narrower than 0.03;
  INCONCLUSIVE: anything else.

== Correctness and compiled resources
  K=  128 one-tile        max relative error 2.5e-04; compiled: shared 65,536 B, 182 registers per thread, 0 spilled
  K=  128 persistent-off  max relative error 2.5e-04; compiled: shared 65,536 B, 182 registers per thread, 0 spilled
  K=  128 persistent-on   max relative error 2.5e-04; compiled: shared 73,728 B, 154 registers per thread, 0 spilled
  K=  512 one-tile        max relative error 2.5e-04
  K=  512 persistent-off  max relative error 2.5e-04
  K=  512 persistent-on   max relative error 2.5e-04
  K= 2048 one-tile        max relative error 2.4e-04
  K= 2048 persistent-off  max relative error 2.4e-04
  K= 2048 persistent-on   max relative error 2.4e-04

== Measuring...............

== Results (ms; ranges are the first to third quartile over rounds)
K = 128
  one-tile        median   0.1286  range   0.1286 to   0.1294    133.5 TFLOPS
  persistent-off  median   0.1260  range   0.1255 to   0.1265    136.4 TFLOPS
  persistent-on   median   0.1061  range   0.1055 to   0.1069    162.0 TFLOPS
  persistent (flatten on) over one-tile: 1.213 (1.207 to 1.220)
  persistent (flatten off) over one-tile: 1.023 (1.018 to 1.028)
  time(persistent-off) / time(persistent-on): 1.184 (1.180 to 1.195)
K = 512
  one-tile        median   0.3584  range   0.3555 to   0.3596    191.7 TFLOPS
  persistent-off  median   0.3580  range   0.3549 to   0.3584    191.9 TFLOPS
  persistent-on   median   0.3461  range   0.3429 to   0.3465    198.5 TFLOPS
  persistent (flatten on) over one-tile: 1.037 (1.035 to 1.040)
  persistent (flatten off) over one-tile: 1.002 (0.995 to 1.006)
  time(persistent-off) / time(persistent-on): 1.035 (1.032 to 1.037)
K = 2048
  one-tile        median   1.2790  range   1.2785 to   1.2790    214.9 TFLOPS
  persistent-off  median   1.2790  range   1.2782 to   1.2790    214.9 TFLOPS
  persistent-on   median   1.2951  range   1.2936 to   1.2995    212.2 TFLOPS
  persistent (flatten on) over one-tile: 0.987 (0.983 to 0.989)
  persistent (flatten off) over one-tile: 1.000 (1.000 to 1.000)
  time(persistent-off) / time(persistent-on): 0.987 (0.982 to 0.988)

== Verdict
  primary, persistent (flatten on) over one-tile: SUPPORTED (the medians fall at every step and the two ends do not overlap)
  secondary, persistent (flatten off) over one-tile: SUPPORTED (the medians fall at every step and the two ends do not overlap)
root@autodl-container-215f42a675-fb5fb51b:~/workspace/programming-lab#
</pasted_content id="b992">

---

**115 · 助手** · `2026-10-14T08:14:03.396Z` · `msg-2866e9671ff1943e0008`

测试和测量都顺利。

**测试**：用新测试文件在 RTX 5090 上 `54 passed, 8 skipped`，跳过的 8 项是只在解释器层运行的“恰好一次”检查，本机已经跑过。A1–A5 在 GPU 上全部通过。

**这次测量本身是可信的**：
- 运行的是你的文件（`6d628fbc`）；
- 三个版本在三个 K 下结果都正确，最大相对误差 ≤ 2.5e-4；
- 编译后都没有寄存器溢出；
- 各轮之间的波动很小，四分位区间大多只有千分之几。

为方便你对照，把比值整理在一起（括号里是各轮的四分位区间）：

| K | 逐 tile / 持久（`flatten` 开） | 逐 tile / 持久（`flatten` 关） | 持久关 / 持久开 |
| --- | --- | --- | --- |
| 128 | 1.213（1.207–1.220） | 1.023（1.018–1.028） | 1.184 |
| 512 | 1.037（1.035–1.040） | 1.002（0.995–1.006） | 1.035 |
| 2048 | 0.987（0.983–0.989） | 1.000（1.000–1.000） | 0.987 |

编译资源：逐 tile 和持久 `flatten` 关都是共享内存 65,536 B、每线程 182 个寄存器；持久 `flatten` 开是 73,728 B、154 个寄存器。

按运行前打印的判据，主判据和辅助判据都判为**支持**。不过判据只回答“比值是否随 K 下降”，不回答“为什么下降”。为什么，要由你来解释。

**接下来请写两段：**
1. **M1，5–8 句。** 对照你 2026-10-12 的预测和它的理由（“持久化省掉的是重复发射的开销，K 增大后这部分占比变小”），说明这组数据支持什么、不支持什么，还剩哪些不确定，也就是哪些结论这次测量回答不了。三列比值和上面的编译资源都可以用。
2. **A6，3–5 句。** 行主序的 B 在 `flatten` 下，你是怎样保住异步拷贝的；epilogue 为什么要有自己的游标。

预测和你最后的结论对不上，不算失败，要看的是解释是否站得住。测量结果已记进第 09 课记录，紧挨着你当时的预测；Checkpoint 指向这两段。都还没有提交。

---

**116 · 用户** · `2026-10-14T08:27:10.026Z` · `msg-2ccc3f1d741952691d35`

1. 这组数据显示出了TFLOPS 比值随 K 增大而下降。支持了我的预测。没什么不支持的。我不知道有什么还要回答。
2. 行主序的 B 在 flatten 下，我将offset_n的计算移到了k循环内。声明了N方向连续。使其保住异步拷贝。epilogue中需要根据offset_n来计算写回地址，而原本offset_n作用域在K循环内，于是需要有自己的游标。

---

**117 · 助手** · `2026-10-14T08:28:25.447Z` · `msg-a360cb5171ba2dedcaaf`

这两段都还不够，需要再写一版。先说清楚缺在哪里。

### M1：只复述了判据的结论，还没有解释

“比值随 K 下降”是脚本按事先定好的判据判出来的。M1 要的是你用机制解释数据，包括三样东西：
- 证据支持什么；
- 证据不支持什么；
- 还有哪些问题这次测量回答不了。

你的预测不只说了方向，还说了理由：“持久化省掉的是重复发射的开销”。方向对上了，不代表理由也对。下面三个问题可以帮你检查：

1. 表里哪一列只隔离了“持久化本身”，没有 `flatten` 的影响？它在 K=128 时是多少？逐 tile / 持久开是 1.213，其中有多少能归到持久化本身，剩下的来自哪里？这对“省掉重复发射的开销”这条理由意味着什么？
2. K=2048 时，持久开反而比持久关和逐 tile 都慢（0.987）。你的预测没说过比值会低于 1。在 tile 之间的间隔几乎可以忽略的时候，`flatten` 可能带来什么代价？可以看一看上面的编译资源。
3. 这次只用了一张卡、一组块配置，也没有拆开“tile 间隔”里各部分的耗时。哪些结论因此还不能下？

### A6 第一点：怎么做的说对了，缺“为什么”

把 `offset_n` 的计算挪进 K 循环并加上声明，这是对的。再补一句为什么要这样做：不挪的话，合并之后 `offset_n` 会经过什么，流水为什么看不到它的连续性？这个机制你在 R-03 时已经找到了。

### A6 第二点：作用域不是原因

作用域只解释了你为什么要在 K 循环后面再算一次 `offset_n`，并不是 epilogue 需要自己游标的原因。另外，你的写回用的仍是 tile 开头由 `tid` 算出的 `tid_n` 和 `offset_m`。和教程比，你的代码其实没有一个独立的 epilogue 游标。

请对照这三处重新回答：
- **教程第 305–306 行与第 538–539 行的注释。** 前者说这是对一个 Blackwell 流水 bug 的规避，后者说 `tile_id_c` 是为了“打断 prologue 与 epilogue 之间的依赖”。
- **图解页里“循环合并后一次迭代里的两个 tile 与 `tile_id_c`”那张交接表。** 在 tile i 收尾的那次迭代里，`tile_id` 已经指向谁了？
- **你自己第四版的现象。** 写回用了和读入绑在一起的那个值之后，流水的提前量怎么样了？

每一点各写一两句就够了，A6 总共 3–5 句。

这次的反馈已记进记录，Checkpoint 指向重写这一步，都还没有提交。

---

**118 · 用户** · `2026-10-14T08:35:30.314Z` · `msg-9bba3cd4983ff73ddb46`

逐 tile / 持久（flatten 关）和持久关 / 持久开有什么区别？

---

**119 · 助手** · `2026-10-14T08:35:48.651Z` · `msg-392a8916cc31cbdae556`

区别在于：每个比值都是两个版本的时间相除，看这两个版本之间改了哪个开关。

三个版本用的是同一个 kernel，只有两个开关不同：

| 版本 | 调度 | `flatten` |
| --- | --- | --- |
| 逐 tile | 4096 个 CTA，每个只算一个 tile | 关 |
| 持久关 | 170 个 CTA，每个循环领取约 24 个 tile | 关 |
| 持久开 | 170 个 CTA，同上 | 开 |

- **逐 tile / 持久关**：两者 `flatten` 都关，**只差调度**。它单独衡量“持久化本身”：从 4096 个各算一个 tile 的 CTA，换成 170 个在 kernel 内循环领 tile 的 CTA，带来多少变化。
- **持久关 / 持久开**：两者都是 170 个持久 CTA，**只差 `flatten`**。它单独衡量循环合并，也就是跨 tile 的流水，连同它的代价。
- **逐 tile / 持久开**：调度和 `flatten` **两个开关同时变了**，所以是前两个比值的乘积：

  逐 tile / 持久开 = (逐 tile / 持久关) × (持久关 / 持久开)

  用你的数据验证一下（表里是各轮比值的中位数，所以只是近似相等）：

  | K | 逐 tile / 持久关 | × 持久关 / 持久开 | ≈ 逐 tile / 持久开 |
  | --- | --- | --- | --- |
  | 128 | 1.023 | × 1.184 = 1.211 | 1.213 |
  | 512 | 1.002 | × 1.035 = 1.037 | 1.037 |
  | 2048 | 1.000 | × 0.987 = 0.987 | 0.987 |

读法都一样：时间比大于 1，说明分母那个版本更快；等于 1 说明没差别；小于 1 说明分母那个版本更慢。

你的预测比的是“持久版对逐 tile 版”，主判据用的是两个开关同时变的那一列。所以要回答“方向对了，理由对不对”，就要看这个总比值拆成两个因子后，各自在不同 K 下是什么样子。拆开以后说明了什么，留给你在 M1 里写。

---

**120 · 用户** · `2026-10-14T08:39:08.046Z` · `msg-4840fa99776497cff74c`

那表里逐 tile / 持久（flatten 关）这一列应该是没有flatten影响的吧

---

**121 · 助手** · `2026-10-14T08:39:16.866Z` · `msg-6f653ea996d3dd62732d`

对，这一列不受 `flatten` 影响：逐 tile 和持久关的 `flatten` 都是关的。编译结果也能佐证，两者都是共享内存 65,536 B、每线程 182 个寄存器，生成的代码一样，差别只在调度。

不过要注意一点：这一列隔离的是“调度方式”整体，不只是“发射开销”。从 4096 个各算一个 tile 的 CTA，换成 170 个循环领 tile 的 CTA，同时变了好几样：
- 硬件要分派的 CTA 数；
- 每个 CTA 开始和结束时的固定工作；
- tile 循环本身的开销：持久版每个 CTA 循环约 24 次，逐 tile 版只循环 1 次。

这一列告诉你这些变化合起来是多少，但没法把它们再拆开。这一点可以写进 M1 的“不确定”部分。

---

**122 · 用户** · `2026-10-14T08:40:09.498Z` · `msg-cadf3bfa594eee653d6f`

为什么不确定？这不就是持久化带来的变化吗？

---

**123 · 助手** · `2026-10-14T08:40:20.275Z` · `msg-f72f5c5769638234c3f0`

这个数确实就是持久化带来的变化，测得也很准，各轮区间很窄。这一点是确定的。

不确定的不是“变化有多大”，而是“变化来自哪里”。你预测里的理由更具体：持久化省掉的是**重复发射的开销**。可是持久化同时改了好几样东西，这一列只给出它们合起来的净效果：
- 硬件要分派的 CTA 从 4096 个变成 170 个（这是你说的发射部分）；
- 每个 CTA 开头和结尾的固定工作，从做 4096 次变成做 170 次；
- 多出了 tile 循环本身的开销：每个 CTA 循环约 24 次，每次都要算 tile 编号和坐标。

好比秤只能称出一整包的重量，称不出包里每样东西各重多少。假如净效果接近 1，至少有两种情况都说得通：
- 省下的本来就很少；
- 省下了一些，但被别的新增开销抵掉了。

这一列分不出是哪一种。

所以，“持久化本身带来的总变化是多少”可以下结论；“重复发射的开销就是这么多”这次测量回答不了。要拆开，得另做实验，比如用 profiler 看时间线，或者单独测一次空 kernel 的发射开销。这不在本课范围内，写进 M1 的“不确定”部分就行。

---

**124 · 用户** · `2026-10-14T08:44:22.866Z` · `msg-f9db42a6ed1b3324b6d0`

tile 循环本身的开销为什么会多呢？分成4096个CTA做，一样也要计算tile编号和坐标

---

**125 · 助手** · `2026-10-14T08:44:52.779Z` · `msg-03a4d7c92115bc1861e2`

你说得对，是我列错了。两种调度下，每个 tile 都要算一次编号和坐标，总共都是 4096 次。逐 tile 版用的也是同一个 kernel，tile 循环同样要执行一次，循环的计数和判断按 tile 算也是一样的。所以这一项不是差别。这条更正我记进了记录。

“逐 tile / 持久关”这一列里，真正不同的是这三样：

- **硬件分派和回收的 CTA 数：4096 对 170。** 每个 CTA 都要分配寄存器和共享内存、启动、结束、释放资源。逐 tile 版每算完一个 tile，就要走一遍“旧 CTA 退出、新 CTA 上来”；持久版里，这一步只是回到循环开头。
- **每个 CTA 在 tile 循环之前的固定工作。** 你的 kernel 在进入循环前要读参数，算 `pid`、`num_tile_m`、`num_tile_n`、`num_tile` 和 `group_tile_size`。逐 tile 版要做 4096 次，持久版只做 170 次。
- **tile 分到 SM 的方式。** 逐 tile 版由硬件调度器看哪个 SM 空了就派下一个 CTA，是动态的。持久版是固定步长的静态领取：第 p 号 CTA 算 p、p+170、p+340……
  - 4096 = 170×24 + 16，所以有 16 个 CTA 要多算一个 tile；
  - 各 CTA 跑着跑着会错开，同一时刻在算哪些 tile 也会和逐 tile 版不同，这又影响它们共用 L2 里的数据。

这三样合起来，就是这一列的净效果。前两样正是你预测里“省掉重复发射”的那部分，第三样不属于发射，却也算进了这一列。所以前面的结论不变：这一列能说明持久化总共带来多少变化，但分不出其中多少来自发射。

---

**126 · 用户** · `2026-10-14T08:49:53.810Z` · `msg-bc8c24e6ef880aa23d4e`

所以持久化带来的变化一共有多个点。1.省去发射CTA的开销。2.省去CTA工作中进入循环前的固定工作。3. 调度tile的方式从硬件动态调度变成了软件静态调度。所以不一定只有第一项带来收益，第二项也可能有优化效果。第三项还可能带来负收益。是这样吗？

---

**127 · 助手** · `2026-10-14T08:50:09.953Z` · `msg-9ecdbd2924e0f61dcee1`

基本是这样，补充三点：

1. **第 1、2 项其实是同一类：每个 CTA 都要付一次的固定成本。** 逐 tile 版付 4096 次，持久版付 170 次，所以两项都只会是收益。要注意，这里的“发射”指 GPU 内部分派 CTA，不是 CPU 发射 kernel。两个版本从 CPU 看都只发射了一次 kernel，CPU 那边的发射开销在这次测量里没有差别。
2. **第 3 项的方向是不确定的，不一定是负的。**
   - 静态领取适应不了快慢差异，有的 CTA 先做完也只能空等，这是可能的负面。
   - 但这次 tile 数恰好是 170 的 24 倍多 16，逐 tile 版的最后一波也只有 16 个 CTA，两边的尾巴差不多。
   - 同一时刻在算哪些 tile 变了，共用 L2 的情况可能变好，也可能变差。

   所以第 3 项可能是负的、正的，也可能几乎没有影响。
3. **这次测量只能看到三项相加的结果。** 你的说法“不一定只有第一项带来收益”是对的。更准确的说法是：这一列给出的是三项的净和，单靠它分不出各项的大小，连第 3 项是正是负也判断不了。

这些都只关于“逐 tile / 持久关”这一列。`flatten` 那一列是另一回事，它比的是两个都是 170 个 CTA 的持久版。

想清楚这些之后，可以开始写 M1 了。前面三个问题都要回答：持久化本身那一列说明了什么，K=2048 时比值低于 1 说明了什么，以及这次测量回答不了什么。

---

**128 · 用户** · `2026-10-14T08:58:28.682Z` · `msg-31490ea364916bd07ca4`

M1的问题重说一遍。持久化本身那一列是哪一列？比值低于1说明了负收益大于了正收益。本次测量回答不了是不是仅仅是发射本身的开销变化导致的比值变化。

---

**129 · 助手** · `2026-10-14T08:58:49.367Z` · `msg-76c55da5bbe26a92596f`

先回答你的问题：**“持久化本身”那一列，就是“逐 tile / 持久（`flatten` 关）”。** 这两个版本 `flatten` 都关，只差调度。

下面把 M1 重说一遍，场景和数字都写全。

**场景**：RTX 5090，你的同一个 kernel，块 128×128×64、3 个 stage、8 个 warp，`M = N = 8192`，K 取 128、512、2048。比了三个版本：
- 逐 tile：4096 个 CTA，`flatten` 关；
- 持久关：170 个 CTA，`flatten` 关；
- 持久开：170 个 CTA，`flatten` 开。

**你的预测**：持久版对逐 tile 版的比值随 K 增大而下降，理由是持久化省掉了重复发射的开销，K 变大后这部分的占比变小。

**M1 要回答三个问题，总共 5–8 句：**

**问题 1：总比值下降，主要是哪个因子在下降？** 前面说过，总比值是两个因子的乘积：

| K | 总比值：逐 tile / 持久开 | = 持久化本身：逐 tile / 持久关 | × `flatten`：持久关 / 持久开 |
| --- | --- | --- | --- |
| 128 | 1.213 | 1.023 | 1.184 |
| 512 | 1.037 | 1.002 | 1.035 |
| 2048 | 0.987 | 1.000 | 0.987 |

请回答：从 K=128 到 2048，总比值的下降主要来自哪一列？你预测的方向对了，那预测里的理由（省掉重复发射的开销）被这组数据支持了吗，支持到什么程度？

**问题 2：K=2048 时总比值低于 1，原因在哪？** 你说“负收益大于正收益”，方向是对的，但还要说清两件事：
- 这个负收益来自哪个开关？用上表的拆分就能定位。
- 那个开关在 K 很大时可能付出了什么代价？可以对照编译资源：逐 tile 和持久关是共享内存 65,536 B、每线程 182 个寄存器；持久开是 73,728 B、154 个寄存器。

**问题 3：这次测量回答不了什么？** 你已经说了一条：“持久化本身”那一列分不出其中多少是发射开销。这一条成立。再想一两条，比如这次只测了哪些条件；问题 2 的原因是你推测的，还是测量直接证明的。

三个问题都想清楚后，连起来写成一段 5–8 句的话就行。

---

**130 · 用户** · `2026-10-14T09:10:42.302Z` · `msg-8e7bd26a6977b7211c3c`

我一开始预测时认为你说的持久版意思就是纯粹的只有持久化没有flatten的版本。如果你之前指的是带有flatten的持久化版，那我接下来的回答当作是“有flatten的持久化版”=“持久版”来答。

---

**131 · 助手** · `2026-10-14T09:11:11.346Z` · `msg-d8f274e5663e5050c84a`

不用改成我的说法，按你当时的原意回答就行。这是我的问题：写脚本时，我把带 `flatten` 的版本定成了主判据，没有先跟你确认“持久版”指的是哪一个。你的理由（省掉重复发射的开销）说的本来就是纯粹的持久化，按原意评判更合适。

换过来不影响结论。两种比值的判据在测量前都打印了，按事先的判据两个都判为“支持”，所以这里不存在看过结果再挑判据的问题。这件事我已经记进了记录。

按你的原意，“持久版”就是持久关。三个问题相应调整如下：

**问题 1：你的预测本身。** 持久化本身那一列是“逐 tile / 持久关”，三个 K 下依次是 1.023、1.002、1.000，方向和你预测的一致。请回答：
- 这个效应有多大？
- 对照你的理由（省掉重复发射的开销），这组数据支持到什么程度？
- 结合我们刚讨论过的，这一列包含三项变化，这又意味着什么？

**问题 2：预测之外，数据还说明了什么。** `flatten` 那一列（持久关 / 持久开）不在你的预测里，但它就在同一组数据中，依次是 1.184、1.035、0.987。请回答：
- 如果拿教程那种带 `flatten` 的持久版去和逐 tile 版比，收益主要来自哪个开关？
- K=2048 时比值低于 1，代价出在哪个开关上？可能是什么代价？编译资源：持久关是共享内存 65,536 B、182 个寄存器；持久开是 73,728 B、154 个寄存器。

**问题 3：这次测量回答不了什么。** 你已经说了一条：持久化那一列分不出发射与其他两项。可以再补一两条。

三个问题合起来，写成 5–8 句。

---

**132 · 用户** · `2026-10-14T09:34:36.084Z` · `msg-fdc79c37d0d7a759b348`

1. 这个优化效应比较微小。最明显的优化效果的K下也只有2.3%的变化。由于之前讨论过的发射开销、固定工作开销和调度变化的三项变化。这组数据无法支持仅是重复发射开销变少而形成的优化。此外，比值变低也不一定是因为重复发射占比变小。还可能是因为K循环变多，静态调度可能出现部分CTA的任务积压的情况。
2. 从数值上看，可以发现总比值上的突出数值主要来自于flatten。flatten的1.184、1.035远比1.023和1.002大。K=2048时，比值低于1，flatten反而有负收益。这可能是因为共享内存用的更多？但多的共享内存我记得是用来给输出缓冲的。就算没有flatten，输出也会借用空的输入槽来做缓冲。总要绕到共享内存上一步。寄存器用的更少了，这个我不清楚为什么。
3. 这次测量回答不了持久版中发射和其他两项变化的收益差别。也不能回答flatten中流水化和另一个我不知道的负收益因素之间的差别收益。

---

**133 · 助手** · `2026-10-14T09:35:35.568Z` · `msg-6b854a8794453b40852b`

**M1 通过。** 这一稿做到了 M1 要求的三件事，而且是用数据和机制来论证的：
- **支持什么，支持到什么程度。** 持久化本身的效应方向和预测一致，但很小，最多 2.3%。
- **不支持什么。** 这一列同时包含三项变化，所以支持不了“收益来自重复发射变少”这个理由，比值下降也不一定是发射占比变小。
- **预测之外的发现。** 总比值的大部分来自 `flatten`；K=2048 时，`flatten` 是净代价。
- **回答不了什么。** 两列各自内部的几项变化分不开，测不出各占多少。

有两处推理需要修正：

1. **“K 循环变多后，静态调度会让部分 CTA 积压”解释不了随 K 的趋势。** 本例里，持久版是 16 个 CTA 最后多算一个 tile；逐 tile 版的最后一波也只有 16 个 CTA。两边的尾巴都是“一个 tile 的时间”，K 变大时这段尾巴和总时间同比例变长，占比不变。所以它造不出随 K 下降的趋势。
2. **你对共享内存的怀疑是对的，而且可以再进一步。** 多用资源本身不会变慢，除非它减少了每个 SM 能同时驻留的 CTA 数。这三个版本每个 SM 都只能驻留 1 个 CTA：
   - 共享内存：两个 CTA 需要 131,072 B 以上，放不下；
   - 寄存器：持久关是 182×256 个，持久开是 154×256 个，放两个 CTA 都会超过每个 SM 的 65,536 个。

   所以多出的 8,192 B 共享内存和少用的寄存器，都没有改变驻留数，不太可能是代价的来源。

至于 `flatten` 在 K 很大时的代价到底是什么，你把它列为“回答不了”，这是对的。下面给一个**没有验证过的假设**，只作参考，不算 M1 的内容：合并以后，K 的每一轮都要判断“是否进入新 tile”和“是否写回”；而跨 tile 的好处每个 tile 只得一次。K=2048 时，每个 tile 有 32 轮，好处摊薄了，每轮的判断却一轮都不少。要证实它，需要用 profiler 看指令级的耗时。寄存器为什么变少，我也不确定，就不猜了。

**还剩 A6。** 上次的两处反馈请照着改：
- 第一点补上“为什么”：不挪进 K 循环的话，合并之后 `offset_n` 会经过什么，流水为什么看不到它的连续性；
- 第二点改答 epilogue 为什么要有自己的游标：对照教程第 305–306、538–539 行的注释，图解页交接表里 tile i 收尾时 `tile_id` 指向谁，以及你第四版的现象。

A6 总共 3–5 句。M1 的解释和评语已记进记录，Checkpoint 现在指向 A6，都还没有提交。

---

**134 · 用户** · `2026-10-14T09:48:42.474Z` · `msg-42c79a5a970180e75921`

噢，flatten的循环中可能有判断的开销。
A6，第一点不挪进K循环的话，offset_n就是处于prologue上，flatten后变成只有首次if路径有声明，后续不进if的路径沿用offset_n值进行读取地址，但看不到连续性声明。第二点要有自己的游标是因为tile_id在epilogue时由于流水为后续的tile处理做准备，已经指向了下一个tile，所以需要有独立游标。
但为什么我的代码里不需要独立游标？

---

**135 · 助手** · `2026-10-14T09:50:54.770Z` · `msg-08c1e454a882103c7987`

**A6 通过。** 两点都说对了：
- **第一点：** 在 prologue 里算的值，合并后只有进入 `if` 的那条路径带着声明，不进 `if` 的路径沿用旧值，流水看不到连续性。所以要把 `offset_n` 挪进 K 循环里算。
- **第二点：** 流水在为后面的 tile 做准备，epilogue 执行时 `tile_id` 已经指向下一个 tile 了。

“flatten 的循环里可能有判断的开销”，也正是我那个假设的意思。

**为什么你的代码不需要独立游标？因为编译器替你造了一个。**

“`tile_id` 已经指向下一个 tile”，说的是编译、流水之后的执行顺序。你源码里写的是普通的两层循环：写回用的是同一个 tile 开头算出的 `tid_n` 和 `offset_m`。保持源码的语义是编译器的责任，所以合并时它会自动把写回要用的值多带一份。

看你第五版在 sm_89 上 `flatten` 开的 TTGIR，合并循环的 `iter_args` 里有这样两组值（这里做了简化）：

```
scf.for ... iter_args(..., %arg11 = <prologue 的 tile_id_n>, %arg12 = <prologue 的行起点>, ...,
                      %offset_m_109 = ..., %tile_id_n_110 = ...)
  ...
  scf.yield ..., %arg12, %arg11      // 把这一轮 prologue 的值交给下一轮的 epilogue 那一份
```

`%arg11`、`%arg12` 在进入新 tile 时更新，给读入用；`%tile_id_n_110`、`%offset_m_109` 每轮从前者接过来，总是落后一步，给写回用。epilogue 那个 `if` 正是用这两个落后的值重新算出 `offset_m` 和 `offset_n`，再去写回。这就是一个由编译器生成的 epilogue 游标。

那教程为什么还要手写 `tile_id_c`？
- **打断依赖。** 第 538–539 行的注释说，它用来打断 prologue 与 epilogue 之间的依赖，编译器就不必替你多带这些值。第 2 天的探查副本里，去掉 `tile_id_c` 后，sm_100 上每线程寄存器从 104 增到了 114。
- **规避缺陷。** 第 305–306 行的注释说，Blackwell 的流水处理不了“一个值同时被 prologue 和 epilogue 使用”，手写游标是绕开这个缺陷的办法。

所以，独立游标不是正确性所必需的，而是为了减轻编译器的负担、绕开缺陷。你的 R-05 也是同一类问题：写回用了一个和流水中的读入绑在一起、每轮都在变的值，结果流水干脆放弃了提前量。

A6 第二点里“为什么不是必需”的这一半，是我补充的，记录里已经写明。

**还剩一步：一个无提示的小变式。** 按课程对“实践”证据的标准，除了通过验收，还要独立完成一个没有提示的小变式。这一项我在约定 P1 里漏写了，所以提议升到**版本 4，增加 V1**：

> **V1**：在你的 kernel 里，把 K 方向的 `tl.where` 和那行连续性声明都去掉，只用 mask 处理 K 的越界。改之前先写下预测：A 的读入在 `flatten` 关和开时，是否仍是 16 字节一组、是否仍提前发出，理由是什么。然后跑只编译层验证，用一两句话解释结果和预测是否一致。

这一项预计只要几分钟。做 V1 期间我不给提示；改完的版本你可以保留，也可以改回去。

V1 完成后，我会按四个目标逐项列出证据、帮助影响和非阻塞余项，请你确认是否结课。同意版本 4 的话，直接开始做 V1 就行。记录和 Checkpoint 已更新，都还没有提交。

---

**136 · 用户** · `2026-10-14T10:00:51.263Z` · `msg-803b24d1a7f7582c3d0c`

A 的读入在 flatten 关和开时，仍会是 16 字节一组、仍提前发出。因为tl.where 原本会干扰连续性，才需要连续性声明，但去掉之后就不需要了。我已经去掉了tl.where 和那行连续性声明了。

---

**137 · 助手** · `2026-10-14T10:02:15.322Z` · `msg-3ed9da55255006d4f667`

**V1 通过。** 预测和理由都对：声明只是为了补上被 `tl.where` 抹掉的连续性，去掉 `tl.where`，`start_k + tl.arange(0, BLOCK_K)` 本身就是连续的，编译器自己看得出来。你没跑只编译层，我在本机替你跑了（文件 `27b89b39`）：

- 解释器层 `46 passed`，只编译层 `16 passed`，全部通过；
- sm_89、sm_90 上，`flatten` 关和开都是 12 处 16 字节的 `cp.async`，循环里的等待都是 `num = 2`，和你的预测一致。

V1 是在 `flatten` 开时验证的，你的 `offset_k` 一直在 K 循环里算，所以合并也不会遮住它。

## 结课前的证据清单

| 目标 | 所需证据 | 证据 | 判断 |
| --- | --- | --- | --- |
| O1 持久化的数据流与调度、`flatten` 的作用与代价 | 理解 | 节点 1–3 的检查与复查、导师串讲、综合验收（阶段事件 E-01–E-10） | 充分 |
| O2 搬运与计算在各代硬件上的分工、描述符、专用化、拆半、退路 | 理解 | 节点 4–6 的检查与复查、综合验收第 2、3 问 | 充分 |
| O3 度量与解释性能 | 理解 + 实证 | 节点 7 的检查；10-12 先于测量的可证伪预测；RTX 5090 上的受控测量（环境、版本、输入、对照、事先打印的判据都记录在案）；M1 的解释说清了支持什么、不支持什么、回答不了什么；正确性另有测试与测量前的逐项核对 | 充分 |
| O4 实现并验证持久化 matmul | 理解 + 实践 | 你的实现在 RTX 5090 上通过 54 项，本机解释器层与只编译层全过；A6 说清了一个重要的验证；V1 无提示完成 | 充分 |

- **阻塞问题**：R-01 至 R-05 全部关闭，R-04 本是非阻塞的，也已修好。
- **帮助的影响**：各次帮助都停在失败证据、不变量、来源指向和提问，没有给过改法或代码，我也没有写过你的实现文件。独立证据都成立。A6 第二点中“独立游标为什么不是正确性所必需”这一半是我补充的，记录里写明了。

**不阻塞的余项**
- **提交前，你的文件过不了仓库的 lint，而 CI 每次推送都会跑。** Ruff 报 6 处，其中 3 处可以自动修，比如 import 顺序和行尾空格；还要跑一次 `ruff format`。其余几处（两行过长、一个中文全角逗号）都在注释掉的手写合并循环里，删掉那段就解决了。这是你的文件，你来改，或者授权我跑格式化。
- **两个现象还没有解释**：K=2048 时 `flatten` 的代价，以及寄存器为什么变少。我给过一个假设，没有验证。
- **两个可选项已按你的意思留到复习时做**：在 5090 上跑教程脚本；改造 grouped GEMM。
- **测量记录里的教学更正共三条**，都不记为你的差距。

**请确认是否结课。** 确认后我一次写入结课结论，并移动 Checkpoint。另外两件事请一并告诉我：
1. 要不要为这一课生成学习记录（结构化记录，可以另附原始对话存档）和卡片？
2. 第 09 课的文件现在都还没提交。lint 处理好之后，要不要提交到 `main` 并推送？

---

**138 · 用户** · `2026-10-14T10:44:33.140Z` · `msg-caa8855ed8f7f2759f35`

在结课之前，我还有几个问题。第一，为什么where会破坏连续化？第二，where后越界部分设为0位置。这还符合连续化性质吗？这不是从结尾跳到开头了吗？第三，我希望详细了解一下max contiguous和multiple of那个声明连续性的函数的用法。

---

**139 · 助手** · `2026-10-14T10:45:57.715Z` · `msg-b78a98d1a6b5b3e70d12`

这三个问题都落在 Triton 编译器的“轴信息分析”（AxisInfo）上。我先去读 v3.7.1 的源码，把规则核对准确，再结合你的代码做几个小实验来回答。

---

**140 · 助手** · `2026-10-14T10:46:44.546Z` · `msg-da1e344dfd26af8b6d2e`

我在核对读源码得到的规则，接下来看 `tl.multiple_of`、`tl.max_contiguous` 的定义，以及读入时编译器怎样用这些信息决定一次搬多少字节。

---

**141 · 助手** · `2026-10-14T10:47:54.584Z` · `msg-120ae2b9eeee6c30425a`

规则已经从源码里核对清楚了。再做一组小实验，验证这两个声明各自少写一个时读入会变成什么样，并找出教程里的用法实例。

---

**142 · 助手** · `2026-10-14T10:51:21.749Z` · `msg-7404849ee9e3a3fc5e3e`

三个问题都绕着一件事：编译器是怎样“知道”一个下标连续的。我先交代这个机制，再逐个回答。下面的规则都核对过 Triton v3.7.1 的源码，也用一个小 kernel 做了只编译实验。

## 先交代：编译器怎样判断“连续”

编译时，编译器不知道下标的具体数值（`pid`、`N` 都要到运行时才知道）。它对每个整数张量、指针张量逐维记录三个性质，这套分析叫**轴信息分析（AxisInfo）**。定义取自 `include/triton/Analysis/AxisInfo.h`：

| 性质 | 含义 | `pid_n * 64 + tl.arange(0, 64)` 的值 |
| --- | --- | --- |
| 连续度 contiguity = C | 张量能切成若干组，每组 C 个元素，组内是 v, v+1, …, v+C−1 | 64 |
| 整除度 divisibility = D | 每组的**第一个**元素是 D 的倍数（D 取 2 的幂） | 64 |
| 恒定度 constancy = C | 能切成若干组，每组 C 个元素都相等 | 1 |

每种操作都有一条固定的推导规则。例如 `tl.arange(0, 64)` 的连续度是 64；乘上 `pid_n * 64` 再相加，连续度还是 64，组首是 64 的倍数。

读入时，一个线程一次搬几个元素，取下面几项中最小的：
- 连续度：最多能连着取几个元素；
- 由整除度推出的地址对齐：组首地址对齐到多少字节；
- mask 的恒定度：mask 要在一整组里取值相同，才能整组一起搬或一起不搬。

一次至少要搬 32 bit 才能用 `cp.async`（见 `PipeliningUtility.cpp` 里的 `canBeConvertedToAsyncLoad`）。fp16 要一次搬 16 字节，就得证明 8 个相邻元素连续、组首对齐、mask 一致。

## 问题一：为什么 `tl.where` 会破坏连续性

`tl.where(cond, x, y)` 在 IR 里是 `arith.select`。它的规则（`AxisInfo.cpp` 第 877–880 行）是：

> 结果的连续度 = gcd（x 的连续度，y 的连续度，cond 的恒定度）

在 `tl.where(offset_n < N, offset_n, 0)` 里，y 是常量 0。常量张量所有元素都相等，恒定度是整个长度，连续度只有 1。所以结果的连续度是 gcd(64, 1, …) = 1，每个元素自成一组，整除度也随之失效。

这条规则是保守的，因为它必须对**任何运行时的取值**都成立。编译器不知道 N，就得考虑某些位置被换成 0 的情况。这不等于值真的不连续了：绝大多数完整的 tile 里，值照样连续，只是编译器再也证明不了。

对比一下：`mask_n = offset_n < N` 并不改动 `offset_n` 本身，`offset_n` 的连续度仍是 64。你在 V1 里去掉 `tl.where` 后读入照样是 16 字节，就是这个原因。

## 问题二：越界位置变成 0，还算连续吗？

你说得对，**不算**。在跨过边界的那个 tile 里，值确实从末尾跳回了 0。这正是编译器在问题一里不肯认定连续的理由。所以 `tl.where` 之后加的声明，是一个**在最后一个 tile 里并不成立的承诺**。

**具体例子。** 设 `BLOCK_N = 64`，`N = 208`（16 的倍数），第 3 号 tile 负责第 192–255 列：
- `tl.where` 之前：192, 193, …, 255；
- `tl.where` 之后：192, …, 207（16 个有效），后面 48 个都是 0。

按 8 个一组（每组对应一次 16 字节的搬运）：

| 组 | 值 | 真的连续吗 |
| --- | --- | --- |
| 第 0 组 | 192 … 199 | 是 |
| 第 1 组 | 200 … 207 | 是 |
| 第 2–7 组 | 0, 0, …, 0 | 否 |

声明说“64 个连续”，对第 2–7 组是假的。编译器信了声明，会对每组发一条 16 字节的拷贝，起点取组里第一个下标。对第 2–7 组，它要搬的是这一行的第 0–7 列，而不是“8 份第 0 列”。至于这次搬运实际发不发生，要看 mask：

- **你的代码**：`mask_n` 是在 `tl.where` 之前算的，第 2–7 组的 mask 全为假。PTX 里是这样一条指令：

  ```
  cp.async.cg.shared.global [ %r105 + 0 ], [ %rd4 + 0 ], 0x10, %r106;   // %r106 = selp(16 或 0)
  ```

  第四个操作数是要从源地址读的字节数。按 PTX ISA，它小于 16 时，余下的字节填 0。mask 为假时它是 0：一个字节也不读，直接写 16 个字节的 0。所以假承诺根本没有变成一次读取。
- **教程的 kernel**：B 没有 N 方向的 mask。第 2–7 组真的会读这一行的第 0–7 列，读到的是真实数据，只是列不对。这些位置只会算出第 208 列以后的输出，而写回的 mask（用没改过的 `offs_cn` 算）会把它们全部丢掉。

假承诺不出事，靠的是两个条件：

1. **组不会跨过边界。** 只有能证明地址对齐时，编译器才会成组地搬。这里的前提是行步长 N 是 16 的倍数，于是边界 N 正好落在组与组之间：每组要么全部有效（真的连续），要么全部越界。N 不是 16 的倍数时，行首本身就不对齐，编译器会退回逐元素读入，声明根本用不上。下面的实验印证了这一点。
2. **越界位置的值不影响结果。** 它们要么被 mask 成 0，要么在写回时被丢弃。M、N 方向天然满足这一点。K 方向只有在 mask 用没改过的下标计算时才满足，这正是你在 R-01 里修好的地方；否则这些读进来的值会被加进求和。

## 问题三：`tl.max_contiguous` 和 `tl.multiple_of` 的用法

**它们做什么。** 这三个函数都只给值贴标签，不做计算（见 `semantic.py` 第 1815–1830 行）：
- `tl.multiple_of(x, D)` 给定义 `x` 的那条操作挂上 `tt.divisibility = D`；
- `tl.max_contiguous(x, C)` 挂上 `tt.contiguity = C`；
- `tl.max_constancy(x, C)` 挂上 `tt.constancy = C`。

返回的是原来那个 `x`。轴信息分析遇到这些标签，会**无条件**用它们替换自己推出来的值（`AxisInfo.cpp` 的 `visitOperation`，注释写着 “override with hint”），不做任何检查。

**参数。** `values` 必须是编译期常量整数，每一维给一个：
- 一维下标写一个数，比如 `tl.multiple_of(offs, 64)`；
- 二维指针张量写一个列表，比如 `[1, 64]`，表示第 0 维不作声明，第 1 维连续 64、组首是 64 的倍数。

取值应当是 2 的幂，轴信息分析就是按这个前提设计的。

**含义的精确版本。** 以 `AxisInfo.h` 的定义为准：
- `max_contiguous(x, C)`：x 能切成每组 C 个的连续段。
- `multiple_of(x, D)`：**每组第一个**元素是 D 的倍数。文档字符串写的是 “the values in input are all multiples”，这只在连续度为 1 时（比如标量或指针）才准确。
- 单位：给整数下标声明时，按元素计；给指针声明时，整除度按字节计。所以 `tl.multiple_of(ptr, 16)` 表示 16 字节对齐。

**为什么两个都要写。** 用同一个读行主序 B 的小 kernel，在 sm_89 上只编译对照（块 64×64×32）：

| 写法 | N 是 16 的倍数 | N 不是 16 的倍数 |
| --- | --- | --- |
| 不用 `tl.where` | 16 字节异步拷贝 | 逐元素同步读入 |
| `tl.where`，不加声明 | 同步读入 | 同步读入 |
| `tl.where` + 只加 `max_contiguous(64)` | 同步读入 | 同步读入 |
| `tl.where` + 只加 `multiple_of(64)` | 同步读入 | 同步读入 |
| `tl.where` + 两个都加（64, 64） | 16 字节 | 同步读入 |
| 两个都加，连续度改为 4 | 8 字节 | 同步读入 |
| 两个都加，整除度改为 4 | 8 字节 | 同步读入 |

一次 16 字节的搬运要同时满足两件事：8 个元素相邻，**并且**起点地址 16 字节对齐。连续度只管前一件，整除度只管后一件，缺一个就退到最小。两个值取小一点，一次搬的字节数就跟着变小。最后一列说明：声明只描述 `offset_n` 这一个张量；行首对不齐时，它补救不了。

**写在哪里。**
- **标签贴在定义这个值的那条操作上。** 写在另一行，不会把标签挪过去，你在 R-03 里已经见过。
- **值经过 `if` 或循环的合并点，标签就丢了。** 合并时取两边信息的最大公约数，没带标签的那一边会把它拉下来。

**一个冷知识，不要依赖它。** 写在循环里、作用于循环携带的变量的声明，按理挂不上去。可是代码生成器在正式生成循环之前，会先把循环体“预演”一遍，以找出哪些变量要跨轮传递（`code_generator.py` 的 `_find_carries`）。预演时，这个名字指向的还是循环前的那个值，标签就这样作为副作用，贴到了循环前那个值的定义操作上。所以它“碰巧”生效了，实验里写在循环中、作用于循环携带指针的声明，得到的确实是 16 字节的拷贝。教程 08 第 148–149 行在 K 循环里写 `tl.multiple_of(a_ptrs, [16, 16])`，连返回值都没接，能起作用也是这个原因。这是实现细节，换个版本可能就变了。

**教程里的三种典型用法：**
- **09 第 135–136、320–321 行：在 `tl.where` 之后补回被抹掉的信息。** 就是本课这种情形。
- **06 第 59、70 行：标量。** 例如 `lo = tl.multiple_of(lo, BLOCK_M)`、`start_n = tl.multiple_of(start_n, BLOCK_N)`。告诉编译器，运行时算出的起点是块大小的倍数。
- **08 第 148–149 行：指针。** 指针是从表里读出来的，编译器不知道它是否对齐，只能由人来声明。

**风险。** 编译器不检查声明。声明不成立、而那些数据又真的被用到时，会读错数据；地址实际不对齐时，运行会报 misaligned address 之类的错误。原则是：**只声明对每一组都成立的性质；要是只在用不到的组里不成立（就像问题二），就得像问题二那样，能说清它为什么不出事。**

这些核对过的规则和实验结果，我作为证据补进了第 09 课记录。其他还是之前的状态：你确认结课后，我再写入结课结论；学习记录、卡片和提交的问题，也请一并告诉我。

---

**143 · 用户** · `2026-10-14T11:00:04.476Z` · `msg-f3425a3b5a4bbb69a081`

select的意思是对于condition where后的结果张量，使用的时候可能是在x和y两个张量中来回跳着用的吗？所以才要gcd二者的连续度。而不是构建一个连续的结果张量？

---

**144 · 助手** · `2026-10-14T11:00:30.154Z` · `msg-6f81fc80af0f2249f00d`

你的直觉对了一半：结果里每个位置，确实可能取自 x，也可能取自 y。但这件事发生在**算出结果的时候**，不是“使用的时候”。`tl.where` 会实实在在地构建一个新张量，逐位置算：

```c
r[i] = cond[i] ? x[i] : y[i];
```

算完以后，`r` 就是寄存器里的一组普通数值。后面拿它做地址运算或读入时，不会再到 x、y 之间来回挑。

问题出在**编译时不知道 `cond` 是什么样子**，于是不知道 `r` 的哪些位置来自 x、哪些来自 y。设 x = 192, 193, …, 199（连续度 8），y = 8 个 0，`cond = x < N`，看三种 N：

| N | cond | r | r 连续吗 |
| --- | --- | --- | --- |
| 208 | 全真 | 192 … 199 | 是，就是 x |
| 196 | 前 4 个真，后 4 个假 | 192, 193, 194, 195, 0, 0, 0, 0 | 否 |
| 100 | 全假 | 0 … 0 | 否，全是常量 |

编译器记下的性质必须对每一种 N 都成立，所以只能取最坏的情况。gcd 的三项各对应一种破坏连续性的可能：

- **cond 的恒定度。** 一组里如果有的取 x、有的取 y，就会像 N=196 那行一样断开。要保证一组 C 个连续，cond 得在这 C 个位置上一样。
- **x 的连续度。** 整组都取 x 时，要求 x 本身在这 C 个位置上连续。
- **y 的连续度。** 整组都取 y 时，同样要求 y 连续。y 是常量 0，连续度只有 1，这一项把结果压到了 1。

三项都满足，才能保证每组连续，所以取三者的最大公约数。组长都是 2 的幂，这里的最大公约数其实就是最小值。

源码里另外两个分支也能印证，这条规则针对的正是“不知道每个位置取自哪边”（`AxisInfo.cpp` 第 851–875 行）：
- **cond 是编译期常量时**，编译器知道整个结果来自哪一边，直接沿用那一边的性质，不取 gcd。
- **cond 是一个标量布尔值时**，整个张量要么全取 x、要么全取 y，不会混着取，于是只取 gcd(x, y)，不再算 cond 的恒定度。

一句话总结：`tl.where` 确实构建出了一个结果张量，只是这个张量连续不连续取决于运行时的 N，编译器只能按最坏的情况记账。

---

**145 · 用户** · `2026-10-14T11:05:24.356Z` · `msg-58b0aba314023d7ff881`

这里的连续性指的难道不是结果张量的连续性吗？既然where实实在在地构建一个新张量，那这个新张量总该是连续的呀？

---

**146 · 助手** · `2026-10-14T11:05:58.535Z` · `msg-c1b421c83ac0f13d086b`

这是我用词的问题。“连续”在这门课里其实有两个意思，我一直没有分开讲：

| | **存储连续** | **取值连续**（轴信息分析里的连续度） |
| --- | --- | --- |
| 说的是什么 | 张量**自己的元素**在内存里是不是挨着放 | 张量里**存的那些数**是不是 v, v+1, v+2, … |
| 本课里的例子 | 约定要求 `a`、`b` 连续（`is_contiguous()`） | `offset_n` 是不是 192, 193, 194, … |
| 关心它是因为 | 决定怎样按步长找到每个元素 | 下标指向的**目标地址**是不是相邻，能不能一次搬完 |

你说的“新张量总该是连续的”，指的是第一种。`tl.where` 新构建的张量在这个意义上没有问题：它的 64 个数分在各线程的寄存器里，一个不少。轴信息分析关心的是第二种：这些数**作为下标**用的时候，指向的地址相邻不相邻。

拿 C 来类比：

```c
int idx[8] = {192, 193, 194, 195, 0, 0, 0, 0};   // 数组 idx 本身在内存里是挨着放的
for (int i = 0; i < 8; i++) v[i] = b_row[idx[i]];  // 但访问的是 b_row[192..195] 和 4 次 b_row[0]
```

`idx` 这个数组“存储连续”，可它里面的数不是 192 到 199 这样一路加一。所以 `b_row[idx[i]]` 访问的不是 8 个相邻的元素，没法合成一次 16 字节的读取。

放回本课。设 `BLOCK_N` 中的某 8 个位置，N = 196：
- `tl.where` 之前，`offset_n` 这段是 192, 193, …, 199，指向 B 这一行相邻的 8 个元素，一条 16 字节的 `cp.async` 就能搬完；
- `tl.where` 之后，这段是 192, 193, 194, 195, 0, 0, 0, 0。张量照样完整存在，但它指向的是第 192–195 列和 4 次第 0 列，地址不再相邻，一条指令搬不了。

所以我前面说的“连续度”“连续性声明”，指的都是第二种：**取值连续**。`tl.max_contiguous(x, 64)` 声明的是“x 里的数每 64 个一组、一路加一”，和 x 自己怎么存放无关。

这个区分我已经记进第 09 课记录，算我讲解的缺口。下面我会把轴信息里的说法写作“取值连续”，免得再和张量的存储连续混在一起。

---

**147 · 用户** · `2026-10-14T11:37:22.747Z` · `msg-4fdf42f5de599e411302`

噢，这我就明白了，原来是取值连续。问题二中，本次kernel的假承诺不出问题，就是靠形状凑巧是16倍数，且边界正巧落在组之间，而且越界的值因为mask和丢弃不产生最终影响是吗？

---

**148 · 助手** · `2026-10-14T11:37:45.396Z` · `msg-0baa424946e2f3ccc399`

基本对，但“凑巧”这个词要改一下。三条里，前两条不是运气，而是编译器自己保证的；真正要你保证的只有第三条。

1. **N 是 16 的倍数，不是凑巧，而是编译器肯用这条承诺的前提。** 它只有在**证明得了**地址对齐时，才会成组地搬。Triton 会把能被 16 整除的整数参数特化成“已知是 16 的倍数”，这时 B 每一行的行首都对齐，才可能发 16 字节的拷贝。N 不是 16 的倍数时，编译器证明不了对齐，直接退回逐元素读入，承诺根本用不上：结果照样正确，只是慢。上次实验表的右列就是这种情况。
2. **边界落在组与组之间，是第 1 条自动带来的。** 每组 8 个元素，组首都是 8 的倍数；N 又是 16 的倍数，边界只能落在两组之间，不会把一组劈成两半。所以只要编译器肯成组地搬，就不会出现“半组有效、半组越界”。
3. **越界位置的值不影响结果，这一条要靠写代码的人保证。** 承诺不成立的那些组：
   - 你的代码里，mask 是在 `tl.where` 之前算的，这些组整组被 mask 掉，一个字节也不读；
   - 教程里，B 读进来的这些值只会算出第 N 列以后的输出，写回时被丢弃。

   M、N 方向天然满足这一条。K 方向只有在 mask 用没改过的下标计算时才满足，也就是你 R-01 修好的那一处。

所以更准确的说法是：编译器只在第 1 条成立时才会依赖这条承诺；第 1 条成立时，第 2 条一定成立；剩下的第 3 条由你来保证。三条都满足，“在最后一个 tile 里不成立的承诺”就不会造成任何影响。

补充一个边界情况：教程的 kernel 如果接收的是一个行步长为 16 的倍数、但 N 不是 16 倍数的视图，编译器仍会成组地搬。这时第 2 条可能不成立，会有一组跨过 N。这一组读到的仍是同一行里第 N 列之后的元素，没有越出这一行；那些列的结果最后又被写回的 mask 丢掉，所以还是靠第 3 条兜住。

问题都答完了，结课还等你确认。确认时请一并告诉我两件事：要不要生成学习记录和卡片；处理完 lint 后，要不要提交。

---

**149 · 用户** · `2026-10-14T11:45:34.395Z` · `msg-bbfbcb59b739bc9bedb4`

噢，是因为BLOCK_N = 64，N = 208，这里N被转成了已知是 16 的倍数，所以某种程度上N也是部分的编译期参数。然后N减去BLOCK_N 的倍数就也是16的倍数，所以肯定会落到两组之间。所以triton的整数参数一定程度上也是编译期的？

---

**150 · 助手** · `2026-10-14T11:46:31.355Z` · `msg-b3ff14de33b99dca9518`

对，你的推理成立。Triton 的整数参数确实“部分是编译期的”。我核对了 Triton v3.7.1 发射时的特化规则（`python/src/specialize.cc` 第 238–247 行）。每次发射 kernel，它会看一眼实参，把几条信息固化进编译结果：

| 实参 | 被固化的信息 | 在 IR 里的样子 |
| --- | --- | --- |
| 整数恰好等于 1 | 整个值，按编译期常量处理 | 参数直接变成常量 1 |
| 整数是 16 的倍数 | 只有“是 16 的倍数”这一条，具体值仍在运行时传入 | `%N: i32 {tt.divisibility = 16 : i32}` |
| 指针（张量的地址）16 字节对齐 | “16 字节对齐”这一条 | `%b_ptr: !tt.ptr<f16> {tt.divisibility = 16 : i32}` |

你的 kernel 用 `M = N = K = 256` 编译出来，函数签名就是这样（取自 sm_89 的 TTGIR）：

```
tt.func public @matmul_persistent_kernel(
    %a_ptr: !tt.ptr<f16> {tt.divisibility = 16 : i32}, %b_ptr: ..., %c_ptr: ...,
    %M: i32 {tt.divisibility = 16 : i32}, %N: i32 {tt.divisibility = 16 : i32},
    %K: i32 {tt.divisibility = 16 : i32}, %c_row_stride: i32 {tt.divisibility = 16 : i32})
```

这条信息是缓存键的一部分，所以：
- `N = 208` 和 `N = 1024` 共用同一份编译结果，因为两者都是“16 的倍数”这一类；
- `N = 200` 会触发另一次编译，得到的 kernel 不知道 N 是否对齐，B 的读入就退回逐元素同步读。

如果不想要这种特化，可以用 `@triton.jit(do_not_specialize=[...], do_not_specialize_on_alignment=[...])` 关掉。

这和 `tl.constexpr` 的区别在于固化了多少：`constexpr` 把整个值都固化进去，值一变就重新编译。你的 `NUM_SMS` 就是这样，M1 的输出里，逐 tile（4096）和持久（170）各编译了一份。普通整数参数只固化“等于 1”和“是不是 16 的倍数”这两条，具体数值仍是运行时的。

你对边界的推理也对，可以说得再精确一点：
- 一个 tile 负责从 `tid_n × 64` 开始的 64 列，组首在 `tid_n × 64 + 8j`，都是 8 的倍数；
- N 是 16 的倍数，自然也是 8 的倍数；
- 所以 N 本身就是某一组的组首，边界只能落在两组之间。

这也解释了约定里 A4 为什么写“N、K 整块且输入对齐时”，测试为什么特意用 256×256×128 这样的形状：只有在 16 的倍数这一类里，编译器才拿得到对齐信息，才可能发出 16 字节的拷贝。M1 的 8192 和 128、512、2048 也都属于这一类。

问题都答完的话，结课还等你确认；学习记录、卡片和提交，也请一并告诉我。

---

**151 · 用户** · `2026-10-14T11:49:13.352Z` · `msg-45ece81efdb1bf99ae0a`

好的。接下来我希望你将tl.max_contiguous 和 tl.multiple_of 的用法也做进图解页中。

---

**152 · 助手** · `2026-10-14T11:49:59.843Z` · `msg-484575356cff81a0b674`

我先看一下图解页的现有结构和之前记下的发布约定，再设计新的一节。

---

**153 · 助手** · `2026-10-14T11:50:06.985Z` · `msg-c90c5632da0cfa546bbe`

页面已有一套固定的样式组件，新的一节沿用它。先看页面的结构、样式组件和脚本组织方式。

---

**154 · 助手** · `2026-10-14T11:52:41.324Z` · `msg-ff9f06afc682f64013f2`

规则和实测都齐了。下面先查几处行号，供页面的“来源”一栏引用，然后开始写这一节。

---

**155 · 助手** · `2026-10-14T11:55:11.439Z` · `msg-56419fa00514f73f9969`

版本 10 已生成。接下来更新仓库副本的转换脚本，再用无头 Chromium 实际点一遍新控件、检查脚本错误并截图看排版。

---

**156 · 助手** · `2026-10-14T11:57:06.314Z` · `msg-13ccc0084f1dbf3fe038`

暗色主题下颜色正常，表格和图都在各自的横向滚动容器里。现在修掉列表的溢出问题，重建后再测一次手机宽度。

---

**157 · 助手** · `2026-10-14T11:57:35.472Z` · `msg-0a68fa68eaca8b7e0e60`

检查全部通过：手机宽度不再横向溢出，38 个按钮和新控件的 72 种组合都没有脚本错误。现在发布到原来的图解页链接。

---

**158 · 助手** · `2026-10-14T11:58:05.550Z` · `msg-9cd0a77e742cbd604b86`

“声明”这一节已经加进图解页，发布为第 10 版，链接不变：https://claude.ai/artifact/TWiPUi32TvQAo7W1DdTDxW 。点顶部导航最后一项“声明”就能直接跳到这一节。仓库里的离线副本也同步更新了：[persistent-matmul-timeline.html](docs/triton-learning/attachments/09-persistent-matmul/persistent-matmul-timeline.html)。

这一节按我们这几轮答疑的顺序编排：
- **两种“连续”**：存储连续和取值连续的对照表。
- **编译器记下的三条性质**：取值连续度、组首整除度、恒定度，以及“一次读入搬几个元素”的取最小规则。
- **`tl.where` 的规则**：为什么要取 gcd，并附上 N = 208、196、100 三种情况的对照。
- **单 tile 演示**（可以操作）：可以切换 N（256、208、200、196），切换 N 方向用不用 `tl.where`，`tl.max_contiguous` 和 `tl.multiple_of` 各写不写、写 4 还是 64。图上逐行显示第 3 号 tile 的 64 个下标，用橙框标出一条读入指令一次搬的范围，右侧写明每组实际怎样读；下方实时给出 N 的特化、取值连续度、mask 恒定度和一次读入的字节数，并附一段文字解释当前这种组合。
- **实测表**：两条声明缺一不可，声明的值也决定一次搬几个字节。
- **边界 tile 里的承诺为什么不出事**：三条条件，配一段你实现中带 mask 的 `cp.async` 的真实 PTX，以及 K 方向和“视图”这两种例外。
- **用法速查**：写法与参数、精确含义、标签贴在哪里（含循环体预演那条冷知识）、教程里的三种用法，以及“编译器不检查声明”的风险提示。
- **整数参数的特化**：等于 1、是 16 的倍数、指针对齐这三种情况在 IR 里的样子。

**怎么验证的**：我在无头 Chromium 里把全页 38 个按钮和新演示的 72 种组合都点了一遍，没有脚本错误。演示里的读数和只编译实测的几种情形一一对上。图注里写明了，其余组合是按同一套规则推出来的，没有逐一实测。

**顺手修了一个旧问题**：检查时发现，从第 9 版起，页脚“来源与条件”里的长路径会在手机宽度下把页面撑出 113 像素的横向滚动。这次一起修好了，现在手机宽度下没有横向滚动。

图解页的说明已更新进第 09 课记录，这些改动都还没有提交。结课仍等你确认；确认时，请一并告诉我要不要生成学习记录和卡片、要不要提交。

---

**159 · 用户** · `2026-10-14T11:59:24.464Z` · `msg-b3f4107d8e2ca7d4a4a0`

最后一个问题，连续度、整除度和恒定度指的都是取值上的，而不是存储的是吧？所以multiple_of、max_contiguous和max_constancy的声明也都是取值上的是吧？

---

**160 · 助手** · `2026-10-14T11:59:39.250Z` · `msg-63a2b1e9a28e9104c62f`

对，三者都是对**取值**的描述，三个声明函数声明的也都是取值上的性质。源码头文件里的定义说得很直白（`include/triton/Analysis/AxisInfo.h`），说的都是“整数”本身：

| 性质 | 源码里的定义 | 对应的声明 |
| --- | --- | --- |
| 取值连续度 | “the length of the shortest sequence of contiguous integers” | `tl.max_contiguous` |
| 组首整除度 | “the largest power of two that divides the first element of all groups” | `tl.multiple_of` |
| 恒定度 | “the length of the shortest sequence of repeating integers” | `tl.max_constancy` |

有两点补充，能帮你把“取值”和“访存”连起来：

1. **指针张量的“取值”就是地址。** 对指针张量来说，取值连续就是地址一个挨一个（按元素算），整除度就是地址按字节的对齐。所以这些性质仍然是取值上的。只因为这些值恰好是地址，它们才直接决定了访存能不能成组。下标张量也一样，它的值加到基址上就成了地址。
2. **张量自己怎么存放，只在一个地方出现，而且不由你声明。** “一次读入搬几个元素”那个最小值里，第四项是“布局分给每个线程的元素数”，也就是这个张量的元素怎样分到各线程的寄存器里。它由编译器选定的布局决定，不在这三条性质里，三个声明函数也管不到它。

PyTorch 的 `is_contiguous()`，也就是约定里要求 `a`、`b` 满足的那种“连续”，说的是存储，和这三条性质是两回事。

问题都答完的话，结课还等你确认。确认时请一并告诉我：要不要生成学习记录和卡片；lint 处理好之后要不要提交。

---

**161 · 用户** · `2026-10-14T12:01:22.896Z` · `msg-dc91e00aff87fcbb5916`

好的。接下来我们结课吧。结课完毕后要生成可追溯和结构化学习记录以及复习卡片。要使用对应的skill噢。最后lint处理好后提交吧。
