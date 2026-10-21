# Triton Lesson 02 · Fused Softmax · 复习卡片预览

> 共 **17 张**：技术问答 13 张、真实纠错 3 张、综合口述 1 张。
> 本文按正式卡片的原有顺序呈现全部题面与答案，可先看目录尝试回忆，再跳转核对。
> 阅读版由已校验的 XLSX 导出；卡片更新后需重新导出本文。

[卡片包与导入模板](../triton-lesson-02-fused-softmax.md) · [全部课程预览](README.md)

**正式表格：** [真实纠错 XLSX](../triton-lesson-02-fused-softmax-correction.xlsx) · [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx) · [综合口述 XLSX](../triton-lesson-02-fused-softmax-oral.xlsx)

## 题目目录

| 编号 | 类型 | 题目 |
| --- | --- | --- |
| 01 | 技术问答 | [Triton 按行计算 softmax 时，一个 program 用 BLOCK\_SIZE = next\_power\_of\_2(N) 的静态块装下一行，超出有效列数 N 的位置是 padding。假设有效输入非空且全部有限，为什么 tl.load 对这些 padding 位置应填负无穷，而不能随意填零？](#card-01) |
| 02 | 技术问答 | [数值稳定的 softmax 先求每行的最大值 m，再计算 exp(x\_j − m) / Σ\_k exp(x\_k − m)。为什么减去 m 不改变 softmax 的结果，又能防止什么数值问题？](#card-02) |
| 03 | 技术问答 | [对 M×N 矩阵按行做 softmax。naive 的 PyTorch 写法分五步：row max → subtract → exp → row sum → divide，每一步都把结果写回全局内存，下一步再读出来。分别估算它和一个 fused kernel 的全局内存搬运量（以元素计），并说明 fusion 省下的是什么。](#card-03) |
| 04 | 技术问答 | [在 Triton 3.7.1 的 persistent softmax 中，一个 program 用 for row in tl.range(start, M, step, num\_stages=s) 依次处理多行。这里的 num\_stages 描述的是什么范围内的流水？](#card-04) |
| 05 | 技术问答 | [persistent softmax 有 M 行输入，启动 P 个 program（P>0）。编号 p 的 program 从行 p 开始，每次增加 P，直到行号达到 M。怎样证明这种 grid-stride 分配让每一行恰好被处理一次？](#card-05) |
| 06 | 技术问答 | [同一个 persistent GPU kernel 保持行分配算法不变。增大 tl.range 行循环的 num\_stages（软件流水深度）后，即使每个 SM 的驻留数量和 occupancy 降低，执行时间为什么仍有可能缩短？](#card-06) |
| 07 | 技术问答 | [persistent softmax 的 wrapper 先按每个 program 的寄存器和共享内存用量估算每个 SM 能驻留几个 program，再据此（并以行数 M 为上限）选择默认 grid。复算官方教程 kernel（num\_stages=4）的资源时得到 grid 648。你自己写的简化 persistent kernel，应该用什么来确定默认 grid？](#card-07) |
| 08 | 技术问答 | [persistent softmax 先按每个 SM 的资源容量推导该特化的理论驻留上限，再因为只有 M 行，把全设备 grid 限制为不超过 M。M 很小、实际只 launch 1 个 program 时，这个特化的资源理论 occupancy 应该怎样计算？](#card-08) |
| 09 | 技术问答 | [比较 persistent softmax 与 torch.softmax 等实现的速度时，有人主张“只有预分配输出、直接 launch kernel 才公平”。若实验要回答的是各实现作为 Python 接口被调用时的成本，计时边界应怎样划？](#card-09) |
| 10 | 技术问答 | [Triton fused softmax 中，每个 program 用 BLOCK\_SIZE = triton.next\_power\_of\_2(N) 的静态块装下一整行，再在块内做 max 与 sum。为什么块要这样确定，这种“一行一块”的设计又有什么代价和上限？](#card-10) |
| 11 | 技术问答 | [一次 persistent softmax 实验比较 num\_stages=1/2/4，但每个配置都按各自的编译资源推导默认 grid，例如 N=2049 时三个 stage 的 grid 分别是 432、540、324。这组速度差异比较的究竟是什么？](#card-11) |
| 12 | 技术问答 | [对一行有限输入 x，需要计算每个位置的 log-softmax。为什么“先计算 softmax 概率，再对概率取 log”可能丢失有限结果，而直接计算稳定的 log-softmax 可以避免这个问题？](#card-12) |
| 13 | 技术问答 | [CUDA 中常见的 persistent kernel 会在 while 循环里不断从任务队列取任务；Triton fused softmax 的 persistent 版本则让每个 program 用有界的 for 依次处理 pid、pid+P、pid+2P… 行。两种做法的任务分配方式差在哪里，各适合什么样的任务？](#card-13) |
| 14 | 真实纠错 | [Triton 3.7.1 的 persistent softmax 增大 tl.range 行循环的 num\_stages 后，若每个 program 因此占用更多寄存器或共享内存，最先受影响的是什么？](#card-14) |
| 15 | 真实纠错 | [分析 GPU kernel 性能时，profiler 报告某 kernel 的 occupancy 为 100%。这个 100% 准确地说明了哪一种“占满”？](#card-15) |
| 16 | 真实纠错 | [persistent softmax 有 M 行，program p 依次处理 p、p+P、p+2P… 行（P 为实际启动的 program 数）。若实际启动 P=M，增大 tl.range 行循环的 num\_stages 能带来什么样的重叠？](#card-16) |
| 17 | 综合口述 | [向面试官解释：在 Triton 3.7.1 的 persistent softmax 中，一个 program 用 tl.range 行循环处理多行，num\_stages 控制这个循环的流水深度。为什么增加 num\_stages 不保证提速？请用约 60 秒从重叠收益、驻留资源和实验归因三方面说明。](#card-17) |

<a id="card-01"></a>

## 01. Triton 按行计算 softmax 时，一个 program 用 BLOCK\_SIZE = next\_power\_of\_2(N) 的静态块装下一行，超出有效列数 N 的位置是 padding。假设有效输入非空且全部有限，为什么 tl.load 对这些 padding 位置应填负无穷，而不能随意填零？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：负无穷不会改变有效元素的最大值，并且在减去行最大值、取指数后变成 0，从而既不影响 max，也不增加 softmax 的归一化分母。

- **先求最大值**：令 m 为有效输入的行最大值。额外的负无穷位置不会超过任何有限有效值，因此整块求 max 仍得到 m；若填零，在有效值全为负数时就会改变最大值。
- **再取指数求和**：padding 的负无穷减去有限 m 后仍为负无穷，取 exp 得 0，加入指数和对分母没有贡献；填零则每个 padding 位置都会给分母加上一个正数 exp(0 − 行最大值)，必然改变归一化结果（除非该项下溢为 0）。
- **最终输出**：只有有效列的位置需要写回；padding 只是为块级计算补齐形状，不是 softmax 输入中新增的有效元素。

**边界**：上述推导要求有至少一个有效元素且有效输入有限。整行均为负无穷等情形可能遇到未定义运算，需要另行规定语义。

### 锚点

max 中不竞争 → exp 后为 0

### 来源

Fused Softmax 学习日志 · 2026-08-07 · B #005–009 · padding

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-02"></a>

## 02. 数值稳定的 softmax 先求每行的最大值 m，再计算 exp(x\_j − m) / Σ\_k exp(x\_k − m)。为什么减去 m 不改变 softmax 的结果，又能防止什么数值问题？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：分子和分母都乘上了同一个因子 exp(−m)，约掉后就是原式，所以结果不变；减去 m 后所有指数输入都不大于 0，exp 的结果都不超过 1，普通的有限大数就不会让 exp 上溢。

[E##\frac{e^{x\_j-m}}{\sum\_k e^{x\_k-m}}=\frac{e^{-m}\,e^{x\_j}}{e^{-m}\sum\_k e^{x\_k}}=\frac{e^{x\_j}}{\sum\_k e^{x\_k}}]
- **为什么能防上溢**：直接计算时，较大的有限输入可能让 exp(x\_j) 先上溢成 inf；减去 m 后，最大元素处 x − m = 0、exp 为 1，所以分母至少为 1，其余各项都不超过 1。

**边界**：它只防住有限大数的上溢，不保证所有特殊值都有限：含 +inf 时 +inf − (+inf) 得 NaN；一行没有有效元素、只剩 −inf padding 时，−inf − (−inf) 也是 NaN，这类输入要由接口约定处理。

### 锚点

同乘 exp(−m) → 比值不变；指数输入 ≤ 0 → 不上溢

### 来源

Fused Softmax 学习日志 · 2026-08-07 · A #007 · 数值稳定

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-03"></a>

## 03. 对 M×N 矩阵按行做 softmax。naive 的 PyTorch 写法分五步：row max → subtract → exp → row sum → divide，每一步都把结果写回全局内存，下一步再读出来。分别估算它和一个 fused kernel 的全局内存搬运量（以元素计），并说明 fusion 省下的是什么。

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：naive 约搬运 8MN + 4M 个元素，fused 理想情况下只读一次输入、写一次输出，共 2MN 个元素，大矩阵时流量比接近 4 倍；fusion 省下的是中间结果在全局内存上的往返，不是 max、exp、sum、divide 这些计算。

- **逐步计数**：row max 读 MN、写 M；subtract 读 MN + M、写 MN；exp 读 MN、写 MN；row sum 读 MN、写 M；divide 读 MN + M、写 MN。合计读 5MN + 2M、写 3MN + 2M。
[E##\frac{8MN+4M}{2MN}=4+\frac{2}{N}]
- **fused 为何只要 2MN**：fused kernel 把一行读进来后，减最大值、exp、求和与除法的中间结果都不再写回全局内存，最后只写一次输出。

**边界**：约 4 倍是理论流量比，不是运行时间的保证：本机实测 fused 的 Triton 明显快于 naive，但并非在每个列宽上都快于 torch.softmax。

### 锚点

5 读 3 写 → 1 读 1 写：约 4×，省的是 DRAM 往返

### 来源

Fused Softmax 学习日志 · 2026-08-07 · A #007、D #006 · fusion 流量

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-04"></a>

## 04. 在 Triton 3.7.1 的 persistent softmax 中，一个 program 用 for row in tl.range(start, M, step, num\_stages=s) 依次处理多行。这里的 num\_stages 描述的是什么范围内的流水？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：programming-lab triton lesson02 · 2026-08-07 learning baseline

### 答案

**结论**：它描述同一个 program 内行循环的跨迭代流水：不同行的迭代可以同时在途、相互重叠，具体怎样重叠由编译器安排。

- **迭代是什么**：一次迭代计算一行 softmax；只有同一个 program 有多次迭代时，后一行的工作才可能与前一行重叠。
- **依赖仍存在**：对于同一行，加载后才能求最大值，再计算指数、指数和、归一化和写回。这些依赖不会因为 num\_stages 变大而消失。

**边界**：stage 不是独立的 program 或 worker，也不表示把一行机械切成 s 段并行处理。

### 锚点

同 program · 跨迭代 · 编译器安排

### 来源

Fused Softmax 学习日志 · 2026-08-07 · A #013–016、C #010–014 · stages 纠错

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 5 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-05"></a>

## 05. persistent softmax 有 M 行输入，启动 P 个 program（P>0）。编号 p 的 program 从行 p 开始，每次增加 P，直到行号达到 M。怎样证明这种 grid-stride 分配让每一行恰好被处理一次？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：对任意合法行号，除以 P 得到唯一的商和余数；余数确定负责它的 program，商确定该 program 的循环迭代，所以既不会漏行，也不会重行。

- **符号定义**：设 r 是行号，满足 0≤r<M；p 是 program 编号，满足 0≤p<P；k 是从 0 开始的迭代编号。它们满足以下对应关系。
[E##r=p+kP,\qquad p=r\bmod P,\qquad k=\lfloor r/P\rfloor]
- **不漏与不重**：存在这组商和余数，说明每个 r 都有对应的 program 和迭代；商余数唯一，说明不会有另一组 program 与迭代再次处理同一行。

**边界**：循环必须以 r<M 为条件，并使用同一个正步长 P。证明依赖这套静态行分配规则，而不是仅凭某个数字例子看起来覆盖完整。

### 锚点

商余数唯一 → 行归属唯一

### 来源

Fused Softmax 学习日志 · 2026-08-07 · C #006–013 · 覆盖证明转折

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 6 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-06"></a>

## 06. 同一个 persistent GPU kernel 保持行分配算法不变。增大 tl.range 行循环的 num\_stages（软件流水深度）后，即使每个 SM 的驻留数量和 occupancy 降低，执行时间为什么仍有可能缩短？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：流水可能让同一 program 中更多独立迭代的工作重叠，提高指令级并行与延迟隐藏能力；这部分收益有时可以抵消较少驻留工作的代价。

- **怎样隐藏延迟**：当某一行迭代等待加载结果时，另一行迭代中不依赖该结果的指令可能继续推进，减少 program 只有等待而没有可做工作的时间。
- **为何不矛盾**：occupancy 是相应测量口径下驻留 warp 数占硬件上限的比例，跨迭代并行则描述已驻留工作内部有多少独立指令可推进。驻留比例降低时，剩余工作的推进效率仍可能改善。

**边界**：这是一种需要测量核验的可能机制。stages 不会自动把一行切成更多块，也不保证每次增加流水深度都会提速。

### 锚点

跨迭代独立工作 → 延迟隐藏机会

### 来源

Fused Softmax 学习日志 · 2026-08-07 · C #006–014 · 指令级并行纠错

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 7 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-07"></a>

## 07. persistent softmax 的 wrapper 先按每个 program 的寄存器和共享内存用量估算每个 SM 能驻留几个 program，再据此（并以行数 M 为上限）选择默认 grid。复算官方教程 kernel（num\_stages=4）的资源时得到 grid 648。你自己写的简化 persistent kernel，应该用什么来确定默认 grid？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：用它自己实际要 launch 的那份编译特化的资源记录；官方特化算出的 648 只属于那份特化，不能拿来代替。

- **什么叫同一特化**：需要把 kernel 实现、输入形状对应的块配置，以及 num\_warps、num\_stages 等编译和启动配置一一对应；这些设置可能改变编译后的资源用量。
- **为何影响 grid**：默认 grid 由资源推导驻留能力。如果资源记录来自旧配置，后面的容量估算和 program 数就可能与真正执行的版本不匹配。
- **反例**：学习中写的简化 kernel 在 N=781 下实际读取资源后，stages 1/2/4 的默认 grid 都是 864，而不是官方特化的 648。
- **排查方法**：核对资源探测与最终 launch 的参数是否一致，例如块大小要按列数 N 取 next\_power\_of\_2(N)；形状或配置改变后重新读取资源。

**边界**：某一特化测得的 grid 不是整个算法的常量；旧分支测试通过，也不能替代当前默认路径的验证。

### 锚点

实际 launch 特化 = 资源探测特化

### 来源

Fused Softmax 学习日志 · 2026-08-07 · C #039–044、#129–130、#135–137、#146 · 默认 grid 复审

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 8 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-08"></a>

## 08. persistent softmax 先按每个 SM 的资源容量推导该特化的理论驻留上限，再因为只有 M 行，把全设备 grid 限制为不超过 M。M 很小、实际只 launch 1 个 program 时，这个特化的资源理论 occupancy 应该怎样计算？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：仍按该特化单个 program 的资源需求与每个 SM 的资源容量推导，结果不受 M 截断影响；截断只减少这次实际启动的 program 数，设备因此达不到这个上限。

- **理论上限**：资源理论 occupancy 回答“如果有足够多的工作，该特化最多能占用多少 warp 驻留容量”，依据是每份工作的资源需求和每个 SM 的资源容量。
- **实际启动量**：grid 回答“这次在整个设备上总共启动多少个 program”。小 M 限制的是这次有多少工作，而不是每个 SM 理论上装得下多少工作。
- **延伸**：achieved occupancy 是执行时实际观测到的驻留情况，会受工作量、调度及执行过程影响，需要与静态理论估算分开。

**边界**：不能把被 M 截断后的全设备 grid 直接代入每个 SM 的资源容量公式，否则会把启动规模和理论驻留能力混为一谈。

### 锚点

资源容量 · launch 数 · 运行时观测

### 来源

Fused Softmax 学习日志 · 2026-08-07 · C #112–113、#137 · occupancy 公式复审

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 9 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-09"></a>

## 09. 比较 persistent softmax 与 torch.softmax 等实现的速度时，有人主张“只有预分配输出、直接 launch kernel 才公平”。若实验要回答的是各实现作为 Python 接口被调用时的成本，计时边界应怎样划？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：计时边界由要回答的问题决定：一次性的 JIT、资源探测和默认 grid 初始化放在计时外；计时内继续调用 wrapper，保留每次调用都要做的分配、参数检查与 launch，各实现在同一 API 层级比较。

- **为什么先准备**：如果每次重复资源探测，就会把初始化策略的成本带入结果；该结果不能直接代表已经准备好的常规调用。
- **为何不改测 kernel-only**：其他实现的调用同样包含分配和检查；只把自己的实现改成直接 launch kernel，会悄悄换掉被比较的对象。

**边界**：准备后 wrapper、kernel-only，以及未缓存初始化的首次或默认 API 调用，回答的是不同问题；这些耗时不能不加说明地混用。

### 锚点

一次性准备在外 · 每次 wrapper 成本在内

### 来源

Fused Softmax 学习日志 · 2026-08-07 · C #113–122 · benchmark 口径转折

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 10 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-10"></a>

## 10. Triton fused softmax 中，每个 program 用 BLOCK\_SIZE = triton.next\_power\_of\_2(N) 的静态块装下一整行，再在块内做 max 与 sum。为什么块要这样确定，这种“一行一块”的设计又有什么代价和上限？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：Triton 的归约需要编译期已知的块形状，而 max 与 sum 都要覆盖整行，所以块必须一次装下整行，取不小于 N 的最小 2 的幂；代价是块随 N 跳档、每档都是另一份编译特化，而且整行 padding 后必须装进片上资源，太长的行不能直接沿用。

- **静态块**：例如 N=781 时 BLOCK\_SIZE=1024：781 个有效 lane、243 个 padding lane；padding 只是 program 内部的逻辑位置，用 −∞ 填充，不会写回。
- **越过 2 的幂**：N 只多一列，块就可能翻倍：N=32 时块为 32，N=33 时实际特化的块是 64。块变了就是另一份编译特化，寄存器、共享内存、驻留数和默认 grid 都要按新特化重新读取，不能沿用旧 N 的资源表。

**边界**：一整行 padding 后必须能装进单个 program 可用的片上资源；教程实现没有处理超大列宽，N 很大时不能只靠继续调大 BLOCK\_SIZE 沿用这个设计。

### 锚点

编译期块形状 + 整行归约 → next\_power\_of\_2；越档即换特化；须装进片上

### 来源

Fused Softmax 学习日志 · 2026-08-07 · A #007、C #135–137、D #003–006 · 整行静态块

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 11 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-11"></a>

## 11. 一次 persistent softmax 实验比较 num\_stages=1/2/4，但每个配置都按各自的编译资源推导默认 grid，例如 N=2049 时三个 stage 的 grid 分别是 432、540、324。这组速度差异比较的究竟是什么？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：比较的是流水设置、编译资源占用和默认启动规模一起变化后的整套默认策略，不能把速度差异只归因于流水深度。

- **有哪些联动**：num\_stages 可能改变资源使用，资源变化又影响默认 grid；grid 改变后，每个 program 分到的行数和循环迭代数也可能改变。
- **怎样追加对照**：若要缩小到流水深度的影响，可保持输入和实现一致，显式使用共同的 grid，再比较不同 stages；同时核对实际编译资源与计时结果。

**边界**：固定 grid 只是控制一项混杂因素。要进一步断言是 occupancy、流水开销或其他机制导致变快或变慢，仍需要对应测量证据。

### 锚点

联动策略比较 ≠ stage 单因素因果

### 来源

Fused Softmax 学习日志 · 2026-08-07 · D #001–006 · 结论范围收紧

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 12 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-12"></a>

## 12. 对一行有限输入 x，需要计算每个位置的 log-softmax。为什么“先计算 softmax 概率，再对概率取 log”可能丢失有限结果，而直接计算稳定的 log-softmax 可以避免这个问题？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：很小的 softmax 概率在浮点数中可能先下溢成 0，随后取 log 就得到负无穷。直接使用稳定的对数表达式，可以避免先形成这个已经丢失精度的最终概率。

- **定义所用量**：令 x\_i 为当前元素，m 为整行的最大值，j 遍历行内所有有效元素。先减去 m，再计算指数和的对数，最后从 x\_i−m 中减去它。
[E##\log\operatorname{softmax}(x\_i)=(x\_i-m)-\log\sum\_j e^{x\_j-m},\qquad m=\max\_j x\_j]
- **最小例子**：输入 \[0, -1000\] 时，第二项概率可能在浮点表示中成为 0；再取 log 只能得到负无穷。稳定公式保留原始分数 -1000，得到的第二项仍约为 -1000。

**边界**：这里假设行非空且输入有限。数学上等价的表达式不保证在浮点中同样稳定；非有限输入还需要单独约定和验证。

### 锚点

保留对数域 → 避免概率先下溢

### 来源

Fused Softmax 学习日志 · 2026-08-07 · E #001–004 · log-softmax 快速回顾

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 13 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-13"></a>

## 13. CUDA 中常见的 persistent kernel 会在 while 循环里不断从任务队列取任务；Triton fused softmax 的 persistent 版本则让每个 program 用有界的 for 依次处理 pid、pid+P、pid+2P… 行。两种做法的任务分配方式差在哪里，各适合什么样的任务？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：差在任务何时分配：softmax 的行在 launch 前全部已知、每行工作量相同，可以按公式静态分给各 program；动态队列在运行时让先空闲的 program 继续取任务，适合数量多、耗时差异很大的任务。判断依据是任务来源与成本差异，而不是循环写成 for 还是 while。

- **静态分配**：program p 由自己的编号直接算出负责的行，不需要运行时取任务或互相协调。
- **动态分配**：任务耗时差异很大时，静态分配可能让一些 program 早早做完、另一些还压着重任务；动态取任务让完成得早的 program 接着处理剩下的任务。

**边界**：Triton softmax 的有界 for 同样属于 persistent 写法，只是任务在 launch 前就已分好。

### 锚点

launch 前已知且等成本 → 静态公式；耗时差异大 → 运行时取任务

### 来源

Fused Softmax 学习日志 · 2026-08-07 · A #013–018 · persistent 两种形态

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-02-fused-softmax-technical-qa.xlsx)，第 14 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-14"></a>

## 14. Triton 3.7.1 的 persistent softmax 增大 tl.range 行循环的 num\_stages 后，若每个 program 因此占用更多寄存器或共享内存，最先受影响的是什么？

类型：真实纠错 · 层级：原子 · 等级：B

### 场景

同一个 kernel 只改变 num\_stages；编译结果显示每个 program 的资源用量上升。

### 正确

最先受影响的是每个 SM 能同时驻留的 program 数：资源压力通常先减少并行驻留，而不是直接让单个 stage 变慢；只有出现 spilling 等机制，才谈得上单个 program 变慢，且需要相应证据。

### 错误

如果资源不足，会拖慢单个stage的耗时，进而拖慢整体耗时

### 说明

**结论**：错在因果的落点：资源随在途工作增加而上升这一前提没错，但这些资源限制的是 SM 能同时容纳多少个 program，而不是某个 stage 自身跑多快。

- **驻留容量**：每个 SM 的寄存器和共享内存总量固定；每个 program 占得越多，能同时驻留的 program 越少，并行度随之下降，整体才可能变慢。
- **何时才是单个变慢**：若资源放不下而发生 spilling，单个 program 才可能变慢；要这样下结论，需要 spilling 的证据。

**边界**：stages=4 也不保证保存四个完整行，不保证寄存器与共享内存同时增长；结论以实际编译特化的资源记录为准。

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-02-fused-softmax-correction.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-15"></a>

## 15. 分析 GPU kernel 性能时，profiler 报告某 kernel 的 occupancy 为 100%。这个 100% 准确地说明了哪一种“占满”？

类型：真实纠错 · 层级：原子 · 等级：A

### 场景

只讨论 occupancy 这一项读数本身能说明什么。

### 正确

100% 只说明 warp 驻留容量已满：每个 SM 上驻留的 active warps 达到硬件上限；这些 warp 可能在等待数据，不能据此断定执行单元都在工作。

### 错误

只能说计算单元全都在被用，但不一定用得好

### 说明

**结论**：原答“不一定用得好”（不能推出最佳性能）是对的；错在“计算单元全都在被用”：occupancy 衡量的是驻留容量的占用，不是执行单元有多忙。

- **为何会不同**：一个 warp 可以已经驻留，却因等待内存数据或前序指令结果而暂停推进。这类 stalled warp 仍计入 active warps。
- **状态层次**：active 表示已驻留；eligible 表示当时有可调度的就绪指令；issued 表示指令实际被发射。驻留并不自动意味着后两种状态。

**边界**：高 occupancy 可能帮助隐藏延迟，但不能单独证明最佳性能，更不能把 100% occupancy 直接翻译成“所有计算单元一直满负荷”。

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-02-fused-softmax-correction.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-16"></a>

## 16. persistent softmax 有 M 行，program p 依次处理 p、p+P、p+2P… 行（P 为实际启动的 program 数）。若实际启动 P=M，增大 tl.range 行循环的 num\_stages 能带来什么样的重叠？

类型：真实纠错 · 层级：原子 · 等级：B

### 场景

Triton 3.7.1；行循环写作 for row in tl.range(pid, M, P, num\_stages=s)。

### 正确

同一 program 内没有可流水的重叠：P=M 时每个 program 只有一次行迭代，没有自己的下一行；不同 program 的交错执行属于硬件调度，不是 tl.range(num\_stages) 的跨迭代流水。

### 错误

如果能够在前一批program进行计算处理时，预先启动后一批program开始读取数据，也有可能实现软件流水

### 说明

**结论**：错在把两种不同层次的重叠混为一谈：num\_stages 的作用域是同一个 program 内行循环的不同迭代，原答描述的却是不同 program 之间的交错。

- **按行号推导**：program p 第一次处理行 p，下一次的行号是 p+M，已不小于 M，循环立即结束，所以每个 program 只有一次迭代。
- **硬件调度**：GPU 可能让不同 program 交错执行，一个在计算时另一个在读数据，但这是硬件对独立 program 的调度，不属于某个 program 行循环内部的流水。

**边界**：要让 num\_stages 有可流水的对象，同一 program 必须有多次迭代，例如 P 小于 M、每个 program 处理多行。

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-02-fused-softmax-correction.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-17"></a>

## 17. 向面试官解释：在 Triton 3.7.1 的 persistent softmax 中，一个 program 用 tl.range 行循环处理多行，num\_stages 控制这个循环的流水深度。为什么增加 num\_stages 不保证提速？请用约 60 秒从重叠收益、驻留资源和实验归因三方面说明。

类型：综合口述 · 层级：口述 · 等级：A

适用范围：programming-lab triton lesson02 · 2026-08-07 learning baseline

### 参考回答

**结论**：增加 stages 只是增加跨迭代重叠的机会；有没有足够的迭代、重叠收益能否超过资源和流水成本，才决定是否更快。

- **作用域**：流水属于同一 program 的行循环，不是新增 worker；若启动的 program 数等于行数，每个 program 只有一行，就没有可重叠的下一行。
- **潜在收益**：多个独立行迭代在途时，一个等待数据，另一个可能推进指令，增加指令级并行与延迟隐藏机会。
- **潜在代价**：每个 program 占用更多受限资源时，每个 SM 能同时驻留的 program 可能减少；但不能仅由驻留下降断言单个 stage 变慢。
- **实验归因**：若 stages、资源占用和默认 grid 一起变化，结果评价的是整套策略；要缩小归因，需要共同显式 grid 等对照。

**边界**：occupancy 下降仍可能与加速同时出现，相同 occupancy 也不保证相同速度。

### 评分锚点

同 program 跨迭代；单次迭代无跨行流水；延迟隐藏与驻留权衡；联动策略的因果边界

### 来源

Fused Softmax 学习日志 · 2026-08-07 · A #013–016、C #006–014、D #001–006

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-02-fused-softmax-oral.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)
