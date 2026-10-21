# Triton 跨课辨析与综合 · 复习卡片预览

> 共 **6 张**：技术问答 6 张。
> 本文按正式卡片的原有顺序呈现全部题面与答案，可先看目录尝试回忆，再跳转核对。
> 阅读版由已校验的 XLSX 导出；卡片更新后需重新导出本文。

[卡片包与导入模板](../triton-cross-lesson-synthesis.md) · [全部课程预览](README.md)

**正式表格：** [技术问答 XLSX](../triton-cross-lesson-synthesis-technical-qa.xlsx)

## 题目目录

| 编号 | 类型 | 题目 |
| --- | --- | --- |
| 01 | 技术问答 | [masked load 给越界位置填的值，随后还要经过运算再进入归约。为什么同样是补 0，在矩阵乘的 K 尾部是安全的，到了 LayerNorm 求方差和 Attention 的 softmax 分母里却会出错？判断一个填充值安不安全，通用规则是什么？](#card-01) |
| 02 | 技术问答 | [Triton 教程里有三处叫“group”的东西：矩阵乘的 GROUP\_SIZE\_M、LayerNorm 反向把参数梯度的临时槽分成 G 组、grouped GEMM。它们各把什么分成组，为了解决什么问题？](#card-02) |
| 03 | 技术问答 | [Triton 的 persistent softmax（按行领）、教程的 grouped GEMM（一组矩阵乘的块）和持久化矩阵乘（单个 GEMM 的 tile）都只发射固定数量 P 个 program，让每个 program 循环领任务。三者共同的分配规则是什么、为什么不漏不重？什么情况下该改成运行时动态领取？](#card-03) |
| 04 | 技术问答 | [在 Triton 3.7.1 中用 TMA 描述符搬数据，有两条都带“16 字节”的规则：一条约束整个张量，一条约束每次搬运的块（box）。两条各约束什么量？为什么 x.is\_contiguous() 为真时仍可能不满足？](#card-04) |
| 05 | 技术问答 | [反向需要前向的某个中间量时，可以把它存下来，也可以在反向里重算。seeded dropout 不存 mask，FlashAttention 不存概率矩阵 P：两者各存了什么、重算了什么？能据此断言一定更快吗？](#card-05) |
| 06 | 技术问答 | [Triton kernel 里常同时有块内局部偏移（如 tl.arange(0, BLOCK)）和全局坐标（块起点 + 局部偏移）。矩阵乘按 K 推进指针时的尾部 mask、seeded dropout 调用 tl.rand 时，各该用哪一个？用错会怎样？](#card-06) |

<a id="card-01"></a>

## 01. masked load 给越界位置填的值，随后还要经过运算再进入归约。为什么同样是补 0，在矩阵乘的 K 尾部是安全的，到了 LayerNorm 求方差和 Attention 的 softmax 分母里却会出错？判断一个填充值安不安全，通用规则是什么？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：规则：填充值经过归约之前的所有运算后，仍须是该归约的单位元，也就是不改变结果的那个值。补 0 只在 0 原样进入求和时安全；中间有平移或取指数时，要按变换之后的值来判断。

- **K 尾部**：点积沿 K 求和，补 0 让乘积为 0，正是求和的单位元。K 尾部若读进垃圾值，错误会先累加进有效的 C\[i,j\]，写回时的 mask 已经修不了，所以必须在 load 时补 0。
- **softmax**：求行最大值和指数和时填 −inf：它不改变有限的行最大值，减去最大值后仍是 −inf，exp 得 0，不进分母。
- **LayerNorm**：先减均值再平方：补的 0 变成 −mean，平方后多出 mean²，方差偏大，要在中心化之后再把无效位置置 0。
- **Attention**：补 0 的 K 与 q 的点积为 0，exp(0 − m) 仍是正数，进了分母；补 0 的 V 也消不掉这一项，无效 key 要在 score 上屏蔽成 −inf。

**边界**：规则只管数学上是否中性；访存是否合法另由 load/store 的 mask 保证，填充值不能代替边界检查。

### 锚点

填充值经过变换后仍须是归约的单位元；补 0 只对原样求和安全

### 来源

跨课 · 向量加法、Softmax、矩阵乘、LayerNorm、Attention 学习记录

**来源记录：** [已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。](../../logs/2026-07-27-vector-add.md)；[第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)；[Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)；[Lesson 05 经核验的 LayerNorm 结构化学习过程记录](../../logs/2026-09-14-layer-norm.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-cross-lesson-synthesis-technical-qa.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-02"></a>

## 02. Triton 教程里有三处叫“group”的东西：矩阵乘的 GROUP\_SIZE\_M、LayerNorm 反向把参数梯度的临时槽分成 G 组、grouped GEMM。它们各把什么分成组，为了解决什么问题？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：三者同名不同义：矩阵乘的分组是给同一个 GEMM 的 program 排顺序，LayerNorm 的分组是给部分和分配共享槽，grouped GEMM 的 group 是一次发射里的一组独立矩阵乘。

- **矩阵乘**：GROUP\_SIZE\_M 让连续的 program 先沿 M 方向走完一组 tile 行。同时活跃的一小批 program 用到的 A 行 tile 和 B 列 tile 更少，更可能命中 L2：8 个 program 的窗口从约 9 种输入 tile 降到 6 种。计算结果不变。
- **LayerNorm**：M 行的参数梯度贡献不再各存一份 \[M,N\]，而是累加进 G 组共享的 \[G,N\] 部分和；同组 program 要用锁互斥地读改写，最后由第二个 kernel 汇总各组。省的是临时空间，代价是争锁。
- **grouped GEMM**：一组尺寸不同的矩阵乘（例如 MoE 各专家）一次发射算完：所有问题的块排成一条队列，固定数量的 CTA 按步长领取，省掉逐个调用的多次发射和空闲的 SM。

**边界**：复习时先分清是在排顺序、分槽位，还是打包多个问题，不要按名字套用结论。

### 锚点

排顺序（L2 复用）／分槽位（省空间、要加锁）／打包多个 GEMM（一次发射）

### 来源

跨课 · 矩阵乘、LayerNorm、Grouped GEMM 学习记录

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)；[Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)；[Lesson 05 经核验的 LayerNorm 结构化学习过程记录](../../logs/2026-09-14-layer-norm.md)；[Lesson 08 经核验的 Grouped GEMM 结构化学习过程记录](../../logs/2026-10-09-grouped-gemm.md)

**表格定位：** [技术问答 XLSX](../triton-cross-lesson-synthesis-technical-qa.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-03"></a>

## 03. Triton 的 persistent softmax（按行领）、教程的 grouped GEMM（一组矩阵乘的块）和持久化矩阵乘（单个 GEMM 的 tile）都只发射固定数量 P 个 program，让每个 program 循环领任务。三者共同的分配规则是什么、为什么不漏不重？什么情况下该改成运行时动态领取？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：共同规则是静态步长分配：program p 依次处理第 p、p+P、p+2P… 号任务，P 是实际发射的 program 数。每个任务号 r 都能唯一写成 r = p + kP（0 ≤ p < P），所以既不漏也不重。

- **任务单位**：persistent softmax 领的是行；grouped GEMM 把所有问题的块首尾相接排成一条队列再按步长领，各 program 的块数最多差 1，但工作量不一定相等；持久化矩阵乘领的是同一个 GEMM 的输出 tile，每个 SM 只付一次发射与退出。
- **动态领取**：任务耗时差异很大时（例如 K 相差很大的几组矩阵乘），改用一个全局计数器：空闲的 program 原子地读出旧值并加 1，读到的就是自己的任务号，旧值不小于任务总数就退出。代价是每领一次做一次原子操作，各任务工作量相同时没有收益。

**边界**：步长必须等于实际发射的 program 数；任务数不多于 SM 数时，没有可以摊薄的发射，持久化的收益为零。

### 锚点

r = p + kP 唯一分解；块数均分≠工作量均分；耗时差异大时改用原子计数器

### 来源

跨课 · Softmax、Grouped GEMM、持久化矩阵乘学习记录

**来源记录：** [第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。](../../logs/2026-08-07-fused-softmax.md)；[Lesson 08 经核验的 Grouped GEMM 结构化学习过程记录](../../logs/2026-10-09-grouped-gemm.md)；[Lesson 09 经核验的持久化矩阵乘结构化学习过程记录](../../logs/2026-10-14-persistent-matmul.md)

**表格定位：** [技术问答 XLSX](../triton-cross-lesson-synthesis-technical-qa.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-04"></a>

## 04. 在 Triton 3.7.1 中用 TMA 描述符搬数据，有两条都带“16 字节”的规则：一条约束整个张量，一条约束每次搬运的块（box）。两条各约束什么量？为什么 x.is\_contiguous() 为真时仍可能不满足？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：整个张量：基址 16 字节对齐，最后一维步长为 1，其余各维的字节步长是 16 的倍数。块：最内维的字节数必须是 16 的倍数。连续只说明元素紧挨着存放，不说明起点和行距对齐。

- **张量**：FP16 的 \[T,D\] 行距是 2D 字节，所以要求 D 是 8 的倍数；基址用 data\_ptr() % 16 == 0 判断。
- **块**：块每维最多 256 个元素，这条管的是一次搬运，不是整个张量；NVFP4 的 scale 块 \[128, 16\] 最内维正好 16 字节，可以建。
- **连续≠对齐**：x\[1:\] 仍然连续，但 FP16 下基址偏了 2 字节，不再对齐；它已连续时 .contiguous() 可能原样返回，不能指望它修正对齐。
- **何时暴露**：Python 端构造 TensorDescriptor 时会断言起点和行距对齐；块最内维的字节数在构造时不检查，用 tl.make\_tensor\_descriptor 在 kernel 里建时，编译期就检查。

**边界**：主机端描述符的块最内维不足 16 字节要到启动时才失败，这是按 CUDA 文档推断的，没有在 sm\_100 上实测。

### 锚点

张量管基址与行距，块管最内维字节数；连续≠对齐

### 来源

跨课 · Attention、块缩放矩阵乘学习记录

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)；[Lesson 10 经核验的块缩放矩阵乘结构化学习过程记录](../../logs/2026-10-20-block-scaled-matmul.md)

**表格定位：** [技术问答 XLSX](../triton-cross-lesson-synthesis-technical-qa.xlsx)，第 5 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-05"></a>

## 05. 反向需要前向的某个中间量时，可以把它存下来，也可以在反向里重算。seeded dropout 不存 mask，FlashAttention 不存概率矩阵 P：两者各存了什么、重算了什么？能据此断言一定更快吗？

类型：技术问答 · 层级：机制 · 等级：B

### 答案

**结论**：两者都只存很小的状态、重算体积大的中间量：dropout 只存 seed，随机数由 seed 和 offset 现场生成；Attention 只存每个 query 一个的行统计量 M，反向按块重算 P。省的是存储和读写，代价是额外的计算，不能据此断言更快。

- **dropout**：不再物化、保存和读取完整的 mask，持久状态从 O(N) 降为 O(1)；但输入输出、逐元素选择与缩放仍在，还要现场算 tl.rand。
- **Attention**：以 \[B,H,N,D\]=\[2,4,128,64\] 为例，完整的 P 有 131072 个元素，形状为 \[B,H,N\] 的行统计量只有 1024 个；反向要重算 QKᵀ 与指数。

**边界**：取舍要看重算的计算量和省下的显存流量哪个更贵；课上两处都只论证了省下什么，没有测量哪种更快。

### 锚点

只存小状态、重算大中间量；省存储与读写，多付计算

### 来源

跨课 · Low-Memory Dropout、Fused Attention 学习记录

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)；[9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-cross-lesson-synthesis-technical-qa.xlsx)，第 6 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-06"></a>

## 06. Triton kernel 里常同时有块内局部偏移（如 tl.arange(0, BLOCK)）和全局坐标（块起点 + 局部偏移）。矩阵乘按 K 推进指针时的尾部 mask、seeded dropout 调用 tl.rand 时，各该用哪一个？用错会怎样？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：凡是要和全局边界比较、或要求每个元素各不相同的地方，都用全局坐标；局部偏移只在块内定位。

- **K 尾部 mask**：指针沿 K 推进后，局部 offs\_k 每一轮都是 \[0,1,2,3\]，第二轮对应的全局 K 坐标是 \[4,5,6,7\]；mask 要拿全局坐标和 K 比，K=5 时后三个 lane 要屏蔽，只看局部偏移判断不出来。
- **tl.rand**：随机数由 (seed, offset) 决定：传局部 offset 时，pid 0 与 pid 1 拿到同一组随机数，x\[8:12\] 会重复 x\[0:4\] 的 keep/drop 决策；传全局 offset，两块才分别用 F(seed, 0..7) 和 F(seed, 8..15)。

**边界**：用错通常不会报错，只会让结果或随机模式静默出错。

### 锚点

比边界、要唯一的用全局坐标；局部偏移只在块内定位

### 来源

跨课 · 矩阵乘、Low-Memory Dropout 学习记录

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)；[Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [技术问答 XLSX](../triton-cross-lesson-synthesis-technical-qa.xlsx)，第 7 行（第 1 行为表头）。

[返回题目目录](#题目目录)
