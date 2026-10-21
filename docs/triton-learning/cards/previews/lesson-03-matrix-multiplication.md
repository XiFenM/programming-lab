# Triton Lesson 03 · Matrix Multiplication · 复习卡片预览

> 共 **13 张**：技术问答 9 张、真实纠错 2 张、综合口述 2 张。
> 本文按正式卡片的原有顺序呈现全部题面与答案，可先看目录尝试回忆，再跳转核对。
> 阅读版由已校验的 XLSX 导出；卡片更新后需重新导出本文。

[卡片包与导入模板](../triton-lesson-03-matrix-multiplication.md) · [全部课程预览](README.md)

**正式表格：** [真实纠错 XLSX](../triton-lesson-03-matrix-multiplication-correction.xlsx) · [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx) · [综合口述 XLSX](../triton-lesson-03-matrix-multiplication-oral.xlsx)

## 题目目录

| 编号 | 类型 | 题目 |
| --- | --- | --- |
| 01 | 技术问答 | [计算 C=A×B，其中 A 的形状为 \[M,K\]、B 为 \[K,N\]。若一个 program 负责 C 的一个 \[BLOCK\_M,BLOCK\_N\] 输出块，它如何沿 K 轴完成这个块的计算？](#card-01) |
| 02 | 技术问答 | [Triton 分块矩阵乘法的 K 循环里，offs\_k=tl.arange(0,BLOCK\_K) 是块内的局部 K 偏移，每轮结束时把 A、B 的指针沿 K 推进 BLOCK\_K。为什么 K 尾部的 load mask 不能直接写成 offs\_k<K？](#card-02) |
| 03 | 技术问答 | [计算 C\[M,N\]=A\[M,K\]×B\[K,N\] 时，若 K 不是 BLOCK\_K 的整数倍，为什么不能只靠最终写回 C 的 mask 来处理 K 尾部的越界读取？](#card-03) |
| 04 | 技术问答 | [在分块矩阵乘法 C\[M,N\]=A\[M,K\]×B\[K,N\] 的边界块中，为什么可以让超出 M/N 的位置通过取模读取合法的替代输入，再丢弃对应输出？](#card-04) |
| 05 | 技术问答 | [Triton 官方 matmul 教程在单个 GEMM 内重排 PID（grouped ordering）。输出 tile 网格为 4 行×3 列、GROUP\_SIZE\_M=2 时，第一组里 PID 递增，输出 tile 坐标按什么规律变化？](#card-05) |
| 06 | 技术问答 | [分块矩阵乘法按 GROUP\_SIZE\_M 个输出 tile 行分组时，若最后一组不足整组，为什么 PID 映射必须使用尾组的实际行数？](#card-06) |
| 07 | 技术问答 | [为同一个矩阵乘法 A\[M,K\]×B\[K,N\] 选择 BLOCK\_M、BLOCK\_N、BLOCK\_K 时，为什么只比较输入 shape、program 数和 K 循环次数，仍不能确定哪组 tile 配置最快？](#card-07) |
| 08 | 技术问答 | [在单个 GEMM 内，grouped ordering 只重排线性 PID 到输出 tile 的映射。为什么这样可能提高 GPU 的 L2 cache 命中率并加速分块矩阵乘法？](#card-08) |
| 09 | 技术问答 | [Triton 官方 matmul 教程用一个例子说明单个 GEMM 内的 grouped ordering：A、B 都是 9×9 个 block，要算出最先的 9 个输出 block。按 row-major 顺序需要加载 90 个输入 block，按每组 3 个 tile 行的 grouped ordering 只需 54 个。这两个数分别怎样数出来？差距来自哪里？](#card-09) |
| 10 | 真实纠错 | [在 Triton kernel 里计算输出 tile 尾组的实际组高：在两个标量之间取较小值。](#card-10) |
| 11 | 真实纠错 | [根据 ABBA 顺序的 benchmark 读数，给出 GROUP\_SIZE\_M=1 与 2 的性能结论。](#card-11) |
| 12 | 综合口述 | [面试官问：“你在 RTX 5090 上只改 GROUP\_SIZE\_M=1/2 对比 matmul，看不出稳定的性能差异，那 grouped ordering 还有用吗？”请在 60–90 秒内回答：它靠什么机制争取收益、什么条件下更可能见效，以及你会怎样解读这次结果。](#card-12) |
| 13 | 综合口述 | [面试官请你走读 Triton 官方 matmul 教程的 kernel：C\[M,N\]=A\[M,K\]×B\[K,N\]，每个 program 负责一个 \[BLOCK\_M,BLOCK\_N\] 的输出 tile。请在 60–90 秒内按执行顺序讲清：program 怎样从 pid 找到自己的 tile、怎样沿 K 算完它，以及 M/N/K 三类边界分别在哪一步处理、为什么。](#card-13) |

<a id="card-01"></a>

## 01. 计算 C=A×B，其中 A 的形状为 \[M,K\]、B 为 \[K,N\]。若一个 program 负责 C 的一个 \[BLOCK\_M,BLOCK\_N\] 输出块，它如何沿 K 轴完成这个块的计算？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：固定输出块覆盖的 M 行和 N 列，沿共享的 K 轴逐段加载 A、B，并把每段矩阵乘法的结果累加到同一输出块。

- **初始化**：为这块输出建立形状为 \[BLOCK\_M,BLOCK\_N\] 的 FP32 accumulator，并初始化为零。它的两个轴对应输出行和输出列，不包含 K 轴。
- **每轮加载**：在当前 K 段，加载 A 的 \[BLOCK\_M,BLOCK\_K\] 块以及 B 的 \[BLOCK\_K,BLOCK\_N\] 块；两者共享同一段 K 坐标。
- **乘加与推进**：两块相乘得到 \[BLOCK\_M,BLOCK\_N\] 的部分和并加入 accumulator；随后 A、B 的读取位置都沿 K 轴前进 BLOCK\_K 个元素（对 A 是移到后面的列，对 B 是移到后面的行），输出行列坐标保持不变。
- **完成输出**：遍历全部 K 段后，accumulator 才包含完整点积，可以写回该 program 负责的 C 块。

**边界**：K 不是 BLOCK\_K 的整数倍时，最后一段越界的 K 位置要在 load 时补零；超出 M/N 的输出位置在写回时丢弃。

### 锚点

固定 M/N，遍历 K，累加部分和

### 来源

Lesson 03 · 8/17 概念记录

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-02"></a>

## 02. Triton 分块矩阵乘法的 K 循环里，offs\_k=tl.arange(0,BLOCK\_K) 是块内的局部 K 偏移，每轮结束时把 A、B 的指针沿 K 推进 BLOCK\_K。为什么 K 尾部的 load mask 不能直接写成 offs\_k<K？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：因为 offs\_k 是不随轮次变化的局部偏移，而 mask 要判断的是全局 K 坐标：第 t 轮（t 从 0 计）的全局坐标是 t×BLOCK\_K+offs\_k，正确条件是 t×BLOCK\_K+offs\_k<K，即 offs\_k<K−t×BLOCK\_K。

- **局部与全局**：指针推进后，同一组 offs\_k=\[0,…,BLOCK\_K−1\] 每轮指向不同的全局 K 坐标；变化的是指针基址，不是 offs\_k 本身。
- **写错的后果**：offs\_k<K 只在第 0 轮与全局条件一致。例如 BLOCK\_K=4、K=5：第 1 轮 offs\_k 仍为 \[0,1,2,3\]，全部小于 5，全局坐标 5、6、7 的越界位置没有被屏蔽，读到的错误值会进入有效输出的累加。

**边界**：只有 K 大于 BLOCK\_K 且不是它的整数倍时，这个错误才会暴露；所以测试要有专门触发 K 尾部的 shape，例如 K=40、BLOCK\_K=32。

### 锚点

mask 比全局 K 坐标，不比局部偏移

### 来源

Lesson 03 · 8/17 概念记录 · Triton 3.7.1

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-03"></a>

## 03. 计算 C\[M,N\]=A\[M,K\]×B\[K,N\] 时，若 K 不是 BLOCK\_K 的整数倍，为什么不能只靠最终写回 C 的 mask 来处理 K 尾部的越界读取？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：因为 K 是每个有效输出元素内部的求和轴；错误的尾部输入会先进入有效结果的累加和，写回 mask 无法再把这些错误项剔除。

[E##C\_{ij}=\sum\_{k=0}^{K-1}A\_{ik}B\_{kj}]
- **污染发生的位置**：对合法的 i、j，如果最后一块仍把 k≥K 的数据参与乘加，得到的 accumulator 就已经不是上式的结果。
- **写回 mask 的职责**：最终 mask 只判断输出行 i<M、列 j<N 是否有效。它能丢弃不存在的 C 元素，却不能检查一个合法 C 元素内部哪些乘积来自错误 K 坐标。

**边界**：因此 K 尾部必须在读取 A/B 时屏蔽并补零，使额外乘积为零；M/N 输出边界才由最终 store mask 裁掉。

### 锚点

归约前补零，写回时裁边界

### 来源

Lesson 03 · 8/17 概念记录；8/19 综合验收

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)；[Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-04"></a>

## 04. 在分块矩阵乘法 C\[M,N\]=A\[M,K\]×B\[K,N\] 的边界块中，为什么可以让超出 M/N 的位置通过取模读取合法的替代输入，再丢弃对应输出？

类型：技术问答 · 层级：机制 · 等级：B

### 答案

**结论**：因为 M/N 决定的是不同输出元素的位置，而不是同一个输出内部的求和项；无效行列位置的计算只会生成最终被丢弃的输出。

- **替代输入的作用**：例如无效的 A 行号对 M 取模、无效的 B 列号对 N 取模，可以让读取落在合法地址，同时保留固定大小的输入 tile。这里的替代值只是为无效输出位置提供占位计算。
- **为何不污染有效结果**：矩阵乘法的每个 C\[i,j\] 只沿 K 求和，不会把别的输出行或列加进自己。有效 i、j 的点积仍使用其本来对应的 A 行和 B 列。
- **写回条件**：写回时必须用未经取模的原始输出行列号判断 i<M 且 j<N，丢弃替代位置算出的结果。

**边界**：M/N load 直接用 mask 也能保证正确，取模并不保证更快。这个理由不能用于 K：K 若回绕并参与求和，就会把重复乘积加进有效输出。

### 锚点

无效输出可丢弃，归约污染不可丢弃

### 来源

Lesson 03 · 8/17 概念记录

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 5 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-05"></a>

## 05. Triton 官方 matmul 教程在单个 GEMM 内重排 PID（grouped ordering）。输出 tile 网格为 4 行×3 列、GROUP\_SIZE\_M=2 时，第一组里 PID 递增，输出 tile 坐标按什么规律变化？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：组内 PID 先沿 M 方向让 tile 行号递增、走完组高后，再换到下一个 tile 列（N 方向）：第一组依次处理 (0,0)、(1,0)、(0,1)、(1,1)、(0,2)、(1,2)。

- **坐标约定**：坐标写作 (输出 tile 行号,输出 tile 列号)，不是原矩阵中的单个元素坐标；第一组覆盖 tile 行 0、1，组高为 2。
- **映射规律**：把组内线性编号记作 p、实际组高记作 h，则组内行号为 p%h，tile 列号为 p//h；全局行号还需加上该组起始 tile 行号。
- **复用关系**：相邻的 pid=2、3 负责 (0,1)、(1,1)：输出行不同、输出列相同，因此在相同 K 段读同一块 B 列 tile。

**边界**：这是线性 PID 到输出坐标的映射，不保证 GPU 按这个顺序执行完成；最后一组不足两行时，h 要改用实际组高。

### 锚点

组内先 M，后 N

### 来源

Lesson 03 · 8/17 概念记录 · Triton 3.7.1

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 6 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-06"></a>

## 06. 分块矩阵乘法按 GROUP\_SIZE\_M 个输出 tile 行分组时，若最后一组不足整组，为什么 PID 映射必须使用尾组的实际行数？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：因为尾组实际只有剩下的 tile 行：组内行号用 p%h、列号用 p//h 计算（p 是组内线性编号），h 必须取尾组的实际组高；若仍用设定组高，就会映射出不存在的 tile，同时漏掉必须计算的 tile。

- **实际组高**：设 tile 总行数为 num\_pid\_m，当前组的起始 tile 行号为 first\_pid\_m，则实际组高是 min(GROUP\_SIZE\_M,num\_pid\_m−first\_pid\_m)。
- **具体例子**：tile 网格有 5 行、3 列，设定组高为 2。前两组覆盖行 0–3，尾组只有行 4，所以剩余 pid=12、13、14 应依次映射到 (4,0)、(4,1)、(4,2)。
- **错误后果**：若尾组仍按两行计算，pid=13 会被映射到不存在的 (5,0)，pid=14 只到 (4,1)，导致必须计算的 (4,2) 没有 program 负责。

**边界**：完整组继续使用设定组高；仅当剩余 tile 行数不足一组时缩小。实际组高保证的是输出覆盖正确性，不能仅靠 store mask 修复遗漏。

### 锚点

不越界，也不漏块

### 来源

Lesson 03 · 8/17 概念记录；8/19 尾组变式

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)；[Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 7 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-07"></a>

## 07. 为同一个矩阵乘法 A\[M,K\]×B\[K,N\] 选择 BLOCK\_M、BLOCK\_N、BLOCK\_K 时，为什么只比较输入 shape、program 数和 K 循环次数，仍不能确定哪组 tile 配置最快？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：因为 tile 大小同时改变复用收益，以及边界浪费和资源占用两类代价；program 更少或 K 循环更短只反映了部分开销，不等于总延迟更低。

- **复用收益**：\[BLOCK\_M,BLOCK\_K\]×\[BLOCK\_K,BLOCK\_N\] 的一次块乘里，每个 A 元素参与 BLOCK\_N 次乘加、每个 B 元素参与 BLOCK\_M 次；tile 越大，每次加载的数据用得越多。
- **边界浪费**：M/N 尾部不满时，大 tile 会多算不写回的位置。例如 M=N=130：128×128 tile 只要 4 个 program，名义输出却有 65,536 个；64×64 tile 要 9 个，名义输出 36,864 个；有效输出都是 16,900 个。
- **资源占用**：更大的输出 tile 需要更大的 accumulator，可能提高寄存器占用，让同时驻留的 program/warp 变少，隐藏访存与执行延迟的机会也随之减少。

**边界**：warps/stages、GPU 架构和编译结果也会改变实际瓶颈；shape 分析只适合筛选候选和提出预测，最终以目标 GPU 上相同输入、可比计时条件下的测量为准。

### 锚点

复用收益与资源代价共同决定性能

### 来源

Lesson 03 · 8/17 概念记录

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 8 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-08"></a>

## 08. 在单个 GEMM 内，grouped ordering 只重排线性 PID 到输出 tile 的映射。为什么这样可能提高 GPU 的 L2 cache 命中率并加速分块矩阵乘法？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：它让需要相同 A/B 输入 tile 的 program 在映射上更接近，缩短数据再次被访问的间隔；如果数据此时仍在 L2 中，就可能减少重复从显存读取的流量。

- **复用机会**：同一输出 tile 列的不同行，会在相同 K 段使用同一个 B tile；同一输出 tile 行的不同列，也会使用相同 A tile。分组排序尝试让这些复用更及时。
- **缓存条件**：“访问间隔短”必须短到数据尚未被其他访问从 L2 淘汰，才可能转化为命中收益。
- **何时更有帮助**：二维 tile 网格较大、留有重排空间，计算对访存较敏感，且 group size 与并发窗口（同时活跃的那一小批 program）、block 配置和目标架构匹配时，减少显存流量更有机会降低耗时。

**边界**：PID 映射不强制实际调度顺序；L2 容量和并发访问也会改变数据驻留。因此 grouped ordering 不能保证每次更快，更不能推出 group size 越大越快。

### 锚点

复用赶在 L2 淘汰之前

### 来源

Lesson 03 · 8/19 实践记录 · grouped ordering

**来源记录：** [Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 9 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-09"></a>

## 09. Triton 官方 matmul 教程用一个例子说明单个 GEMM 内的 grouped ordering：A、B 都是 9×9 个 block，要算出最先的 9 个输出 block。按 row-major 顺序需要加载 90 个输入 block，按每组 3 个 tile 行的 grouped ordering 只需 54 个。这两个数分别怎样数出来？差距来自哪里？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：输出 block (i,j) 需要 A 的第 i 个 tile 行和 B 的第 j 个 tile 列；一批输出覆盖的不同 tile 行数加不同 tile 列数越少，要加载的输入 block 就越少。row-major 的 9 个输出排成 1×9，分组后排成 3×3。

- **计数单位**：A、B 都是 9×9 个 block，所以一个 A tile 行或一个 B tile 列各含沿 K 方向的 9 个 block。
- **row-major**：前 9 个输出 block 同在第 0 个 tile 行：需要 1 个 A tile 行和全部 9 个 B tile 列，共 9+81=90 个。
- **grouped**：每组 3 个 tile 行、组内先沿 M，前 9 个输出 block 是左上的 3×3：需要 3 个 A tile 行和 3 个 B tile 列，共 27+27=54 个。

**边界**：这是假设每个不同的输入 block 只加载一次的理想化计数；实际能省多少显存流量，还要看这些 block 被再次使用时是否仍在 L2 中。

### 锚点

覆盖的行数加列数越少，输入 block 越少

### 来源

Lesson 03 · 8/19 实践记录 · grouped ordering 访存对比

**来源记录：** [Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-03-matrix-multiplication-technical-qa.xlsx)，第 10 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-10"></a>

## 10. 在 Triton kernel 里计算输出 tile 尾组的实际组高：在两个标量之间取较小值。

类型：真实纠错 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 场景

在 Triton 3.7.1 中：num\_pid\_m 是输出 tile 的总行数，first\_pid\_m 是当前组的起始 tile 行号，GROUP\_SIZE\_M 是设定组高；实际组高取 num\_pid\_m − first\_pid\_m 与 GROUP\_SIZE\_M 中较小的一个。

### 正确

tl.minimum(num\_pid\_m - first\_pid\_m, GROUP\_SIZE\_M)，或教程使用的 Python 内建 min(num\_pid\_m - first\_pid\_m, GROUP\_SIZE\_M)

### 错误

this\_group\_size\_m = tl.min(num\_pid\_m - first\_pid\_m, GROUP\_SIZE\_M)

### 说明

**结论**：错在把归约 API tl.min 当成两数取小：它的第二个位置参数是归约轴，GROUP\_SIZE\_M 被当成了轴号，于是编译阶段就报 invalid axis。

- **两类 API**：tl.minimum 与 JIT 中的内建 min 都表示两个值取小，这里比较的是两个标量；tl.min 则把一个张量沿指定轴归约。
- **诊断线索**：第一版的数值用例全部停在编译阶段，报错指向 axis 而不是数值结果，这正是参数被当成归约轴的信号。

**边界**：需要沿张量的某个轴求最小值时，tl.min 仍是对应的归约操作；以上 API 语义按 Triton 3.7.1 核对。

**来源记录：** [Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-03-matrix-multiplication-correction.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-11"></a>

## 11. 根据 ABBA 顺序的 benchmark 读数，给出 GROUP\_SIZE\_M=1 与 2 的性能结论。

类型：真实纠错 · 层级：原子 · 等级：A

### 场景

RTX 5090 上的 matmul，M=N=K=4096，固定 64×64×32 block、4 warps、3 stages 和同一输入，只改变 GROUP\_SIZE\_M；按 1→2→2→1 的顺序测得 median 0.6687、0.6902、0.6943、0.6975 ms（group 1 首末两次相差约 4%）。

### 正确

只能说：在这台 RTX 5090、该 shape、固定 launch 配置和本次方法下，GROUP\_SIZE\_M 的影响无法与约 4% 的运行状态漂移稳定分离；既不支持 group 2 更快，也不支持 group 1 更快。

### 错误

在当前环境和固定配置上，对性能影响较小

### 说明

**结论**：错在把“分不出差异”升级成“差异很小”：配置差异与约 4% 的运行漂移混在一起时，看不清差异可能是噪声太大，而不是差异本身小。

- **读数为何分不开**：前半程 group 1 更快、后半程 group 2 略快，两对比较的方向相反；同一个 group 1 首末两次就差约 4%，配置带来的差异淹没在漂移里。
- **能下的结论**：这组读数既不支持 group 2 更快，也不能反过来断言 group 1 更快；结论只限于本机、该 shape、固定配置和本次测量方法。

**边界**：这次“分不出来”不能外推成 grouped ordering 没有收益；换设备、shape、分组大小或测量方法都要重新测量。

**来源记录：** [Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-03-matrix-multiplication-correction.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-12"></a>

## 12. 面试官问：“你在 RTX 5090 上只改 GROUP\_SIZE\_M=1/2 对比 matmul，看不出稳定的性能差异，那 grouped ordering 还有用吗？”请在 60–90 秒内回答：它靠什么机制争取收益、什么条件下更可能见效，以及你会怎样解读这次结果。

类型：综合口述 · 层级：口述 · 等级：A

### 参考回答

**结论**：有用，但不是必然加速：它靠缩短 A/B tile 的复用间隔来争取 L2 命中；这次对照只说明在本机该配置下，差异无法与运行漂移区分，不能说明它没用。

- **复用机制**：同一输出 tile 列的 program 在相同 K 段共用 B tile，同一 tile 行的共用 A tile；分组让这些 program 在映射上更接近，若再次访问时数据仍在 L2，就能少读显存。
- **生效条件**：二维 tile 网格较大、kernel 对访存敏感、group size 与并发窗口和 block 配置匹配时更可能见效；PID 映射也不强制实际调度顺序。
- **解读结果**：两种配置的差异与约 4% 的运行漂移混在一起，只能报告证据不足：既不能说哪组更快，也不能说真实影响很小；结论只限所测设备、shape、配置和计时口径。

### 评分锚点

说出复用来源：同列 program 共用 B tile、同行共用 A tile，分组让它们在映射上更接近；说明复用必须发生在数据仍驻留 L2 时，才会减少显存读取；说出至少两个生效条件：二维 tile 网格较大、访存敏感、group size 与并发窗口匹配；把这次结果表述为无法与漂移区分的证据不足，不说成影响很小，并限定外推范围

### 来源

Lesson 03 · 8/17 概念记录；8/19 性能解释

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)；[Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-03-matrix-multiplication-oral.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-13"></a>

## 13. 面试官请你走读 Triton 官方 matmul 教程的 kernel：C\[M,N\]=A\[M,K\]×B\[K,N\]，每个 program 负责一个 \[BLOCK\_M,BLOCK\_N\] 的输出 tile。请在 60–90 秒内按执行顺序讲清：program 怎样从 pid 找到自己的 tile、怎样沿 K 算完它，以及 M/N/K 三类边界分别在哪一步处理、为什么。

类型：综合口述 · 层级：口述 · 等级：A

### 参考回答

**结论**：pid 先映射到输出 tile，再沿 K 循环乘加到 FP32 accumulator，最后带 mask 写回；K 尾部在 load 时补零，M/N 越界只在写回时丢弃。

- **定位 tile**：grouped ordering 把线性 pid 映射成 (pid\_m, pid\_n)：组内行号 p%h、列号 p//h；尾组的 h 取实际剩余行数，否则会越界又漏块。
- **K 循环**：accumulator 为 \[BLOCK\_M,BLOCK\_N\]、初值为零；每轮加载 A 的 \[BLOCK\_M,BLOCK\_K\] 与 B 的 \[BLOCK\_K,BLOCK\_N\]，乘加后两边读取位置沿 K 前进 BLOCK\_K。
- **K 尾部**：K 是归约轴：越界的 K 位置必须在 load 时补零，错误项一旦加进有效的 C\[i,j\]，写回 mask 就剔除不了。
- **M/N 边界**：M/N 是独立的输出坐标：越界行列可取模读合法的替代数据，结果在写回时按原始行列号 mask 丢弃；直接用 load mask 也正确，取模不保证更快。

### 评分锚点

pid 经分组映射到输出 tile，尾组用实际组高，避免越界和漏块；FP32 accumulator 固定在一个输出 tile 上，沿 K 逐段加载 A、B 并乘加，读取位置沿 K 前进；K 尾部在 load 时补零，因为累加进有效输出的错误项无法被写回 mask 剔除；M/N 越界可取模读替代数据，写回时按原始行列号 mask 丢弃

### 来源

Lesson 03 · 8/17 概念记录；8/19 实践记录

**来源记录：** [Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项](../../logs/2026-08-17-matrix-multiplication.md)；[Lesson 03 实践、纠错、性能证据解释与结课记录](../../logs/2026-08-19-matrix-multiplication.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-03-matrix-multiplication-oral.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)
