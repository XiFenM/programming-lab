# Triton Lesson 01 · Vector Add · 复习卡片预览

> 共 **13 张**：技术问答 11 张、真实纠错 1 张、综合口述 1 张。
> 本文按正式卡片的原有顺序呈现全部题面与答案，可先看目录尝试回忆，再跳转核对。
> 阅读版由已校验的 XLSX 导出；卡片更新后需重新导出本文。

[卡片包与导入模板](../triton-lesson-01-vector-add.md) · [全部课程预览](README.md)

**正式表格：** [真实纠错 XLSX](../triton-lesson-01-vector-add-correction.xlsx) · [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx) · [综合口述 XLSX](../triton-lesson-01-vector-add-oral.xlsx)

## 题目目录

| 编号 | 类型 | 题目 |
| --- | --- | --- |
| 01 | 技术问答 | [Triton kernel 先用 tl.load 的 mask 屏蔽尾块越界位置，再对加载结果做 sum 或 max 归约。为什么仍需处理无效位置的值，不能只依靠 load mask？](#card-01) |
| 02 | 技术问答 | [Triton 条件写回 kernel 的尾块中，offsets 可能越过长度 N。load 用 mask=offsets < N、other=-inf 读入 x；store 的 mask 只写 x > threshold，靠 -inf 通不过这个比较来挡住越界 lane。如果之后把写回条件改成 x < threshold，越界 lane 会怎样？store 的 mask 应怎样构造，才能不论比较条件怎样变都不写越界地址？](#card-02) |
| 03 | 技术问答 | [Triton 向量 kernel 把 BLOCK\_SIZE 声明为 tl.constexpr，用它构造 tl.arange(0, BLOCK\_SIZE)；wrapper 按输入长度从 256、512、1024 中挑一个值传入。tl.constexpr 要求的“固定”是在什么范围内固定？每换到一个新值，第一次 launch 时会发生什么？](#card-03) |
| 04 | 技术问答 | [启动 Triton 向量 kernel 时，program 数需要按输入长度和 BLOCK\_SIZE 计算。什么情况下应使用 lambda META: ... 形式的 callable grid，而不是提前算好的 tuple grid？](#card-04) |
| 05 | 技术问答 | [Triton 向量 kernel 用 tl.program\_id(0) 确定当前块，用 tl.arange(0, BLOCK\_SIZE) 构造块内位置，再用 tl.load/tl.store 访存。BLOCK\_SIZE 是哪一层的数量？它和这个 program 实际使用的 GPU threads/warps 是什么关系？](#card-05) |
| 06 | 技术问答 | [一个 Triton 一维向量 kernel 用 ptr + offsets 读取元素。若 wrapper 开始接受每隔一个元素取一次的切片等非连续输入，为什么仅删除连续性检查还不够？](#card-06) |
| 07 | 技术问答 | [比较向量 kernel 的整块输入与稍长的尾块输入时，尾块的“有效 GB/s”反而更高。写出两者有效 GB/s 之比与有效元素数、测得耗时的关系，并据此说明这个比值上升可能来自哪里。](#card-07) |
| 08 | 技术问答 | [fp32 向量加法 z = x + y 处理 N 个元素。按算法最低数据流量，每个元素要搬运多少字节、做几次运算？据此说明它为什么通常受内存带宽限制。](#card-08) |
| 09 | 技术问答 | [在 Triton 3.7.1 中用 triton.testing.do\_bench 测一个只需几微秒的向量 kernel，单次计时窗口太短。把 rep=100 调大，改变的是什么？若改为在一个样本里连续调用 100 次、再用总时间除以 100，这个平均值测到的又是什么？](#card-09) |
| 10 | 技术问答 | [用 time.perf\_counter() 在调用一次 Triton kernel wrapper 的前后各取一次时间，把差值当作 kernel 耗时。这个读数会漏算什么、又可能多算什么？应怎样正确计时（以 Triton 3.7.1 的 do\_bench 为参照）？](#card-10) |
| 11 | 技术问答 | [Triton 向量 kernel 的尾块用 mask 关闭越界位置的 tl.load/tl.store。有人把这些位置没有访存解释成“GPU 或编译器把冗余访存优化掉了”。在 Triton 3.7.1 为 NVIDIA GPU 生成的 PTX 里，这些访存为什么没有发生？](#card-11) |
| 12 | 真实纠错 | [Triton 向量 kernel 的尾块只有部分位置有效时，每个 program 执行的 tl.load(x\_ptr + offsets, mask=mask) 返回的 tensor 的 shape 由什么决定？](#card-12) |
| 13 | 综合口述 | [向面试官解释：一个 Triton 向量 kernel 的最后一块只有部分位置有效，加载结果还要参与归约，最后按条件写回。请用约 60 秒说明 mask 在读取与形状、归约、写回三处各负责什么。](#card-13) |

<a id="card-01"></a>

## 01. Triton kernel 先用 tl.load 的 mask 屏蔽尾块越界位置，再对加载结果做 sum 或 max 归约。为什么仍需处理无效位置的值，不能只依靠 load mask？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：load mask 保证无效地址不被读取，却不会把无效逻辑位置从结果 tensor 中删除；后续归约仍会合并这些位置的值。

- **问题如何产生**：假设四个局部位置只有前两个有效。load 后仍有四个值；若后两个未定义，直接对四个值求和或求最大值，就可能污染本来有效的归约结果。
- **归约前处理**：应在归约前把无效位置设成不改变该归约结果的值，即该运算的单位元：求和用 0，求最大值用负无穷（同理，乘积用 1、求最小值用正无穷）；通常直接作为 tl.load 的 other 填入。

**边界**：最后的 store mask 只能控制结果写到哪里，不能从已污染的归约结果中撤销无效项的影响。

### 锚点

屏蔽读取 → 位置仍在 → 归约前填单位元

### 来源

Triton 3.7.1 · L01 日志：masked load 与 reduction

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-02"></a>

## 02. Triton 条件写回 kernel 的尾块中，offsets 可能越过长度 N。load 用 mask=offsets < N、other=-inf 读入 x；store 的 mask 只写 x > threshold，靠 -inf 通不过这个比较来挡住越界 lane。如果之后把写回条件改成 x < threshold，越界 lane 会怎样？store 的 mask 应怎样构造，才能不论比较条件怎样变都不写越界地址？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：改成 x < threshold 后，-inf 对任何有限阈值都满足条件，越界 lane 会通过 mask 去写非法地址。稳健写法是把边界条件与数值条件取逻辑与：write\_mask = (offsets < N) & condition，让边界谓词单独负责排除越界地址，数值条件只决定要不要写。

- **原推导为何成立**：在 x > threshold 下，-inf 不会大于任何有限阈值，越界 lane 确实不会被写回；这个推导本身没错，只是安全性依赖于填充值与比较方向的特定关系。
- **为何要显式合并**：other 只是 load 给未读取位置的替代数值，不是 tl.store 会自动继承的边界保护。比较方向或阈值一变（例如改成 x < threshold，或 x >= threshold 而阈值恰为 -inf），sentinel 就可能通过条件；显式合并后，越界位置的 mask 恒为 false。

**边界**：other 仍然有用：未读取位置参与后续计算（例如归约）时取什么值由它决定；但它不能代替写回时的边界条件。

### 锚点

sentinel 只对特定比较成立；边界谓词单独负责越界

### 来源

Triton 3.7.1 · L01 日志：条件写回的边界 mask

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-03"></a>

## 03. Triton 向量 kernel 把 BLOCK\_SIZE 声明为 tl.constexpr，用它构造 tl.arange(0, BLOCK\_SIZE)；wrapper 按输入长度从 256、512、1024 中挑一个值传入。tl.constexpr 要求的“固定”是在什么范围内固定？每换到一个新值，第一次 launch 时会发生什么？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：只要求在一次编译特化内固定：不同 launch 可以传入不同的 Python 整数；每个新值第一次使用时，Triton 会 JIT 编译出与之匹配的特化，之后同一取值复用已编译的版本。

- **固定在哪里**：编译器在生成这一版本的 kernel 时，需要知道 BLOCK\_SIZE，才能确定块级表达式的形状和相关编译决策。
- **怎样变化**：wrapper 本次传 256、下次传 512 都合法；两次调用分别使用与该取值匹配的特化。

**边界**：值必须在 launch 前就是确定的 Python 整数，不能等 kernel 执行时再按运行时 tensor 的值决定；每个新值都要付一次编译，所以候选值宜少。

### 锚点

特化内固定；新值首用即编译

### 来源

Triton 3.7.1 · L01 日志：constexpr 的取值范围、首次调用含 JIT

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-04"></a>

## 04. 启动 Triton 向量 kernel 时，program 数需要按输入长度和 BLOCK\_SIZE 计算。什么情况下应使用 lambda META: ... 形式的 callable grid，而不是提前算好的 tuple grid？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：当 grid 依赖的配置要等 Triton 绑定本次 meta-parameters 后才确定时，用 callable grid 延后计算。

- **配置尚未确定**：例如 autotune 正在选择 BLOCK\_SIZE，grid 也必须跟随当前候选配置变化。callable grid 接收本次 META，再据此计算覆盖输入所需的 program 数。
- **配置已经确定**：如果 wrapper 已知道输入长度 N 和本次 BLOCK\_SIZE，就可以提前计算 triton.cdiv(N, BLOCK\_SIZE)，并作为 tuple grid 传入。

**边界**：输入长度每次不同，并不自动要求 callable grid；关键是计算 grid 所需的值在什么时候才能确定。

### 锚点

看配置何时确定

### 来源

Triton 3.7.1 · L01 日志：callable grid

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 5 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-05"></a>

## 05. Triton 向量 kernel 用 tl.program\_id(0) 确定当前块，用 tl.arange(0, BLOCK\_SIZE) 构造块内位置，再用 tl.load/tl.store 访存。BLOCK\_SIZE 是哪一层的数量？它和这个 program 实际使用的 GPU threads/warps 是什么关系？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：BLOCK\_SIZE 是 block-tensor 层的逻辑位置数，即一个 program 的块级 tensor 有多少个元素位置；实际用多少 threads/warps 由编译器映射决定，二者没有一一对应，不能把 BLOCK\_SIZE 当成线程数。

- **分层**：tl.program\_id 位于 program-instance 层，表示当前是 grid 中的第几个 program；tl.arange 与 tl.load/tl.store 位于 block-tensor 层，对整块逻辑位置逐 lane 运算和访存。
- **硬件层**：编译器再把块级操作映射到 GPU 的线程和 warp；逻辑元素的组织与硬件执行资源的组织是不同层次。

**边界**：例如 BLOCK\_SIZE=4 只说明 arange 产生四个逻辑位置，不能据此断言 GPU 启动了四个线程。

### 锚点

program → block tensor → threads/warps

### 来源

Triton 3.7.1 · L01 日志：抽象层复述

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 6 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-06"></a>

## 06. 一个 Triton 一维向量 kernel 用 ptr + offsets 读取元素。若 wrapper 开始接受每隔一个元素取一次的切片等非连续输入，为什么仅删除连续性检查还不够？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：ptr + offsets 默认相邻逻辑元素也位于相邻存储位置。非连续一维 view 的逻辑索引必须先乘以 stride，才能对应正确地址。

- **stride 的含义**：这里 stride 是相邻两个逻辑元素在底层存储中相隔的元素数，不是字节数。stride 为 2 时，逻辑位置 i 的存储偏移是 i × 2：逻辑位置 1 应读 base\[2\]，只做 ptr + offsets 却会读到 base\[1\]。
- **地址计算**：kernel 需要接收该输入的 stride，并按 ptr + offsets \* stride 生成指针；否则仍会读取连续存储中的元素，得到错误数据。

**边界**：wrapper 的接口范围必须与 kernel 的地址实现一致。放宽校验只能允许数据进入，不能自动改变实际访存方式。

### 锚点

逻辑 offset × 存储 stride

### 来源

Triton 3.7.1 · L01 日志：连续性契约与地址计算

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 7 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-07"></a>

## 07. 比较向量 kernel 的整块输入与稍长的尾块输入时，尾块的“有效 GB/s”反而更高。写出两者有效 GB/s 之比与有效元素数、测得耗时的关系，并据此说明这个比值上升可能来自哪里。

类型：技术问答 · 层级：机制 · 等级：B

### 答案

**结论**：比值等于有效元素数之比乘以耗时的反比：尾块多出几个有效元素而耗时相同，或尾块的测得耗时因测量波动落到更低的计时档位，比值就会上升。这只是工作量与测得时间的比值变化，不能据此认定 DRAM 带宽或 kernel 优化提高。

- **符号定义**：令 N\_exact、N\_tail 分别表示整块和尾块用例的有效元素数，t\_exact、t\_tail 表示测得耗时，G 表示有效 GB/s。两组用例每个元素计入相同有效字节数时，有如下关系。
[E##\frac{G\_{\mathrm{tail}}}{G\_{\mathrm{exact}}}=\frac{N\_{\mathrm{tail}}}{N\_{\mathrm{exact}}}\frac{t\_{\mathrm{exact}}}{t\_{\mathrm{tail}}}]

**边界**：有效字节数不是硬件实际传输的 DRAM 字节数。没有对应的受控测量或硬件证据，不能把比值上升直接解释为物理带宽增加或已证明的 GPU 优化。

### 锚点

有效字节 / 测量时间；不是硬件流量计数

### 来源

L01 日志：尾块有效 GB/s 复盘

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 8 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-08"></a>

## 08. fp32 向量加法 z = x + y 处理 N 个元素。按算法最低数据流量，每个元素要搬运多少字节、做几次运算？据此说明它为什么通常受内存带宽限制。

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：每个元素读 x、读 y、写 z 各 4 字节，共 12 字节，却只做 1 次加法：计算极少、数据搬运很多，耗时主要由内存读写决定，所以通常受带宽限制。benchmark 有效带宽公式里的系数 3 就是这两读一写。

[E##\text{GB/s}=\frac{3\times N\times\text{element\\_size}\times10^{-9}}{\text{ms}\times10^{-3}}]
- **算一笔**：每 12 字节只对应 1 次加法；算术单元很快就能算完这些加法，大部分时间花在等数据读写上。
- **“有效”的含义**：公式按算法最低数据量计字节，不是硬件计数器测得的 DRAM 流量；缓存、写策略和其他内部流量都没有计入。

**边界**：带宽受限描述的是输入足够大时的稳态：小输入时 kernel launch 和固定开销占主导，有效 GB/s 偏低且容易波动。

### 锚点

两读一写 12 B 对 1 次加法 → 带宽受限；系数 3

### 来源

L01 日志：带宽受限与有效带宽

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 9 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-09"></a>

## 09. 在 Triton 3.7.1 中用 triton.testing.do\_bench 测一个只需几微秒的向量 kernel，单次计时窗口太短。把 rep=100 调大，改变的是什么？若改为在一个样本里连续调用 100 次、再用总时间除以 100，这个平均值测到的又是什么？

类型：技术问答 · 层级：机制 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：调大 rep 只会增加样本数，每个样本仍只包住一次调用，窗口不会变长；批量调用确实拉长了窗口，但测到的是连续执行时每次调用的平均成本，缓存状态和发射方式都已不同于原来的单次调用，是另一种指标。

- **采样预算**：rep 的单位是毫秒，表示总共采样多久；它只决定样本数，每个正式样本仍用一对 GPU event 包住一次 fn()。
- **批量改变了什么**：do\_bench 在每个正式样本前清一次 L2 cache；100 次调用算作一个样本时，只有第一次调用前清过缓存，后续调用可能读到前一次留在缓存里的数据，连续发射的方式也与单次调用不同。

**边界**：两种结果都可以报告，但要分别说明测量方式与适用场景；批量结果更平滑，不等于它是原单次指标的更精确版本。

### 锚点

rep 只加样本；批量拉长窗口也换了场景

### 来源

Triton 3.7.1 · L01 日志：do\_bench 采样口径与批量计时

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 10 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-10"></a>

## 10. 用 time.perf\_counter() 在调用一次 Triton kernel wrapper 的前后各取一次时间，把差值当作 kernel 耗时。这个读数会漏算什么、又可能多算什么？应怎样正确计时（以 Triton 3.7.1 的 do\_bench 为参照）？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：kernel launch 只是把工作排进 GPU stream，wrapper 返回时 GPU 可能还没算完，CPU 计时会漏掉这段执行；首次调用还会触发 JIT 编译，把编译时间多算进去。正确做法是先预热，再在开始和停止计时前同步 GPU，或改用 GPU event 计时。

- **漏算**：CPU 可能只等到 kernel 被提交就停止计时。返回 output 本身是安全的：同一 stream 上依赖它的后续操作仍按顺序执行，只是计时读数偏小。
- **多算**：每种配置（例如新的 BLOCK\_SIZE）第一次使用时要编译对应特化，之后复用缓存，所以首次调用不能代表稳态性能。
- **手写计时**：先跑过预热调用；开始计时前和停止计时前各调用一次 torch.cuda.synchronize()。
- **do\_bench**：先调用并同步一次 fn()，编译不进入正式样本；再预热，并在每个正式样本前清 L2、用一对 GPU event 包住一次调用。

**边界**：这样测到的是稳态运行性能，不是首次调用延迟；编译开销依然存在，只是不计入正式样本。

### 锚点

launch 只入队 → 同步或 event；首次含 JIT → 预热

### 来源

Triton 3.7.1 · L01 日志：异步执行与计时

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 11 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-11"></a>

## 11. Triton 向量 kernel 的尾块用 mask 关闭越界位置的 tl.load/tl.store。有人把这些位置没有访存解释成“GPU 或编译器把冗余访存优化掉了”。在 Triton 3.7.1 为 NVIDIA GPU 生成的 PTX 里，这些访存为什么没有发生？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：因为访存本身就是有条件执行的：生成的 PTX 用 guard predicate 修饰 load/store（形如 @%p1 ld.global），predicate 为 false 的 lane 从一开始就不执行对应地址的读写，不是先访问、再由优化撤销。

- **执行条件**：mask 被编译成访存指令的执行条件；尾块中越界 lane 的谓词为 false，对应的读写根本不会执行。

**边界**：predicate 只关掉 false lane 的访存：地址与谓词计算、program 调度仍有成本，有效 lane 的访存仍按硬件事务粒度进行。以上只在 NVIDIA PTX 上核对过，其他后端（如 AMD）的底层形式未核对。

### 锚点

条件访存 ≠ 事后优化

### 来源

Triton 3.7.1 · L01 日志：predicate 因果模型

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-01-vector-add-technical-qa.xlsx)，第 12 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-12"></a>

## 12. Triton 向量 kernel 的尾块只有部分位置有效时，每个 program 执行的 tl.load(x\_ptr + offsets, mask=mask) 返回的 tensor 的 shape 由什么决定？

类型：真实纠错 · 层级：原子 · 等级：A

适用范围：triton · 3.7.1

### 场景

Triton 3.7.1；offsets = pid \* BLOCK\_SIZE + tl.arange(0, BLOCK\_SIZE)，mask = offsets < N，输入 x 共有 N 个元素；wrapper 事先用 torch.empty\_like(x) 分配了与输入同样大小的输出。

### 正确

由当前 program 的局部 pointer tensor x\_ptr + offsets 的形状决定，即 \[BLOCK\_SIZE\]；与 N、输出分配的大小和有效元素个数都无关。

### 错误

“数据目的地已经开辟好了与数据源大小一样的空间，所以返回形状与数据源固定一样”；后来又说“根据输入tensor的形状决定的”

### 说明

**结论**：两句都把形状来源放在了这次 load 之外：先归因于输出的预先分配，后归因于整个输入 tensor。tl.load 逐位置处理传入的指针，返回值就具有这组局部指针的形状；mask 只控制各位置是否读取内存。

- **局部形状**：例如 offsets 有 4 个位置，x\_ptr + offsets 就有 4 个指针。即使 mask 为 \[True, True, False, False\]，load 结果仍有 4 个位置，而不会缩成 2 个。
- **无效位置**：false 位置不从对应地址读数据；指定 other 时得到该替代值，未指定时不能假设其数值有效。

**边界**：输出预先分配多大、整个 PyTorch 输入有多少元素，都不决定这次局部 load 的 shape；预先分配输出只是为了让后续 store 有地方写。

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-01-vector-add-correction.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-13"></a>

## 13. 向面试官解释：一个 Triton 向量 kernel 的最后一块只有部分位置有效，加载结果还要参与归约，最后按条件写回。请用约 60 秒说明 mask 在读取与形状、归约、写回三处各负责什么。

类型：综合口述 · 层级：口述 · 等级：B

适用范围：triton · 3.7.1

### 参考回答

**结论**：mask 逐位置控制访存，但不改变块的静态形状；要让整条计算链正确，还得分别处理归约里的无效值和写回时的地址边界。

- **读取与形状**：load 结果的形状跟随该 program 的局部 pointer tensor；false 位置不读对应地址（访存带 predicate，不是事后优化），却仍占一个逻辑位置。
- **归约**：归约会合并所有位置，所以先给无效位置填该归约的单位元，例如 sum 填 0、max 填负无穷；store mask 无法修复已被污染的归约结果。
- **写回**：条件写回时把地址有效的 boundary mask 与数值条件取逻辑与，不靠填充值恰好通不过比较来防越界；合法地址上 false store 不写入，原值保留。

**边界**：mask 关掉的只是 false lane 的访存，地址计算和调度仍有成本。

### 评分锚点

形状来自局部 pointer tensor；false lane 不访存（predicate）；归约前填单位元；写回合并 boundary 与 condition

### 来源

Triton 3.7.1 · L01 日志：mask 相关要点与复述

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-01-vector-add-oral.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)
