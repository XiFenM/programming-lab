# Triton Lesson 04 · Low-Memory Dropout · 复习卡片预览

> 共 **8 张**：技术问答 6 张、真实纠错 1 张、综合口述 1 张。
> 本文按正式卡片的原有顺序呈现全部题面与答案，可先看目录尝试回忆，再跳转核对。
> 阅读版由已校验的 XLSX 导出；卡片更新后需重新导出本文。

[卡片包与导入模板](../triton-lesson-04-low-memory-dropout.md) · [全部课程预览](README.md)

**正式表格：** [真实纠错 XLSX](../triton-lesson-04-low-memory-dropout-correction.xlsx) · [技术问答 XLSX](../triton-lesson-04-low-memory-dropout-technical-qa.xlsx) · [综合口述 XLSX](../triton-lesson-04-low-memory-dropout-oral.xlsx)

## 题目目录

| 编号 | 类型 | 题目 |
| --- | --- | --- |
| 01 | 技术问答 | [训练时对一个输入元素 x 做 inverted dropout：以概率 p 丢弃、以概率 1−p 保留。为什么保留分支要输出 x/(1−p)，而不是直接输出 x？](#card-01) |
| 02 | 技术问答 | [对长度为 n 的向量实现分块 Triton dropout 时，boundary mask（offset<n）与随机生成的 keep mask 分别解决什么问题？](#card-02) |
| 03 | 技术问答 | [多个 Triton program 用同一个 seed 处理同一向量的不同 dropout 分块时，为什么 tl.rand 应接收元素的 global offsets，而不能让每个 program 都传入从 0 开始的 local offsets？](#card-03) |
| 04 | 技术问答 | [希望稍后重新计算 seeded dropout，并精确复现同一次前向的输出。除了保存相同的 seed，还必须保持哪些条件？请按“随机数相同 → keep 决策相同 → 数值输出相同”三层作答。](#card-04) |
| 05 | 技术问答 | [Low-memory seeded dropout 用 seed 重建随机决策，替代保存长度为 N 的完整 mask。这能减少哪些内存开销，为什么却不能直接断言运行更快？](#card-05) |
| 06 | 技术问答 | [Triton seeded dropout 处理长度 n=2057 的向量，BLOCK\_SIZE=1024；最后一个 program（pid=2）的 offsets 是半开区间 \[2048,3072)。这个 program 里的 tl.load、tl.rand 和 tl.store，哪些必须用 offset<n 的 boundary mask？依据是什么？](#card-06) |
| 07 | 真实纠错 | [判断张量重排并重新连续存储后，用同一个 seed 重算 dropout，能否让每个逻辑元素得到前向时的 keep/drop 决策。](#card-07) |
| 08 | 综合口述 | [面试官问：“在 Triton kernel 里怎样实现 dropout？稍后重算（例如反向传播）时需要和前向完全相同的 keep/drop 决策，但不想把 mask 存下来。”请在 60–90 秒内讲清：保留与缩放规则、随机决策怎样由 seed 和元素位置重建、重算时必须保持什么，以及相对显式保存 mask 的取舍。](#card-08) |

<a id="card-01"></a>

## 01. 训练时对一个输入元素 x 做 inverted dropout：以概率 p 丢弃、以概率 1−p 保留。为什么保留分支要输出 x/(1−p)，而不是直接输出 x？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：除以保留概率 1−p，是为了抵消随机清零造成的期望下降，使输出对随机决策取平均后仍等于原输入 x。

- **两种输出**：设随机输出为 y：被保留时 y=x/(1−p)，被丢弃时 y=0；两种情况的概率分别为 1−p 和 p。
[E##\mathbb{E}\lbrack y\rbrack=(1-p)\frac{x}{1-p}+p\cdot0=x]
- **不缩放的后果**：如果只随机清零而保留分支仍输出 x，期望就会变为 (1−p)x。例如 x=12、p=0.25 时，不缩放的期望是 9；保留时改输出 16，期望才回到 12。
- **常见误区**：不要把保留时的输出值当成期望：p=0.5 时保留值是 2x，但输出 0 和 2x 各以 0.5 的概率出现，期望仍是 x。

**边界**：要求 0≤p<1。保持的是单元素输出的期望，不是每次调用的输出值，也不保证有限样本的平均恰好等于 x。

### 锚点

保留概率乘缩放系数等于1

### 来源

Lesson 04 · 8/24 学习记录 · inverted scaling

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-04-low-memory-dropout-technical-qa.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-02"></a>

## 02. 对长度为 n 的向量实现分块 Triton dropout 时，boundary mask（offset<n）与随机生成的 keep mask 分别解决什么问题？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：Boundary mask 判断某个位置能否合法读写 tensor；keep mask 决定合法元素在 dropout 中被清零，还是保留并缩放。它们回答的是两个独立的问题。

- **访存边界**：每个 program 生成固定数量的 offset，尾部可能出现 offset≥n。Boundary mask 用于 load/store，防止访问向量范围之外的地址。
- **数学分支**：Keep mask 是 random>p，其中 random 是 tl.rand 为该 offset 生成的 \[0,1) 伪随机数。对合法位置，keep 为真输出 x/(1−p)，为假输出 0。
- **为何不能混用**：一个合法元素即使被丢弃，也仍有合法输出位置，需要把 0 写回；一个越界位置即使随机结果为“保留”，也不能因此获得访存权限。

**边界**：生成一个 offset 或计算该 offset 的随机数，都不等于可以读取对应内存；最终安全性由 boundary mask 保证。

### 锚点

访存合法性与随机决策分开

### 来源

Lesson 04 · 8/24 学习记录 · 两类 mask

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-04-low-memory-dropout-technical-qa.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-03"></a>

## 03. 多个 Triton program 用同一个 seed 处理同一向量的不同 dropout 分块时，为什么 tl.rand 应接收元素的 global offsets，而不能让每个 program 都传入从 0 开始的 local offsets？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：因为给定同一随机数生成实现，seed 与 offset 共同决定随机数；不同 program 若重复传入相同的局部 offset，就会重复生成同一块随机模式。

- **坐标定义**：设块长为 B、program 编号为 pid，局部偏移 local 从 0 到 B−1。元素在整条向量中的 global offset 是 pid×B+local。
- **错误会怎样出现**：若每个 program 都调用 F(seed,local)，第 0、1、2 块的同一局部位置会使用同一个随机数，进而重复相同的 keep/drop 模式。
- **正确随机位置**：应让全局位置 i 的元素调用 F(seed,i)，即使用 tl.rand(seed,global\_offsets)，使每块对应自己的随机数位置。

**边界**：这里随机数的“身份”是整数 offset，不是元素值或抽象的逻辑元素：同一 seed 下，同一 offset 总得到同一随机数。

### 锚点

随机身份由 seed 和 global offset 指定

### 来源

Lesson 04 · 8/24 学习记录 · Triton 3.7.1

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-04-low-memory-dropout-technical-qa.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-04"></a>

## 04. 希望稍后重新计算 seeded dropout，并精确复现同一次前向的输出。除了保存相同的 seed，还必须保持哪些条件？请按“随机数相同 → keep 决策相同 → 数值输出相同”三层作答。

类型：技术问答 · 层级：机制 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：三层各有自己的条件：随机数要保持 PRNG 实现和“逻辑元素 → global offset”映射；决策还要保持丢弃概率 p；数值输出还要保持输入值、dtype 和 kernel 的数值计算语义。

- **随机数相同**：每个逻辑元素必须再次调用相同的 F(seed,offset)：除 seed 外，伪随机数生成器（PRNG）的实现和元素到 global offset 的映射都不能变，例如重排后再连续化就会改变映射。
- **决策相同**：随机数相同还不够，比较阈值 p 也要相同；p 变了，同一个随机数的保留／丢弃判断也可能变化。
- **输出相同**：保留位置输出的是缩放后的输入，而不是随机数本身，所以输入值、dtype 和 kernel 的数值计算语义也要一致。

### 锚点

随机数相同、决策相同、输出相同分三层

### 来源

Lesson 04 · 8/24 学习记录 · 复现条件

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-04-low-memory-dropout-technical-qa.xlsx)，第 5 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-05"></a>

## 05. Low-memory seeded dropout 用 seed 重建随机决策，替代保存长度为 N 的完整 mask。这能减少哪些内存开销，为什么却不能直接断言运行更快？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：它用现场生成随机数的计算，换掉完整 mask 的物化、保存和读取；内存状态更少是明确收益，但总延迟还取决于新增计算与其他开销。

- **减少的状态**：显式 mask 需要保存随元素数 N 增长的 O(N) 随机决策；在随机映射约定不变时，seeded 方案只需保存 O(1) 的 seed 来重建这些决策。
- **仍然存在的工作**：输入和输出 tensor 的访问、每个元素的保留/清零选择，以及 x/(1−p) 的缩放都没有消失。
- **新增的代价**：kernel 需要执行伪随机数生成器（PRNG）。省下的 mask 访存与增加的随机数计算谁更重要，取决于目标硬件和实际瓶颈。

**边界**：O(N)→O(1) 描述的是持久随机状态，而不是输入/输出的总空间，也不是时间复杂度或实际耗时。丢弃概率 p 是两种方案共有的算子参数。

### 锚点

省 mask 流量，付 PRNG 计算

### 来源

Lesson 04 · 8/24 学习记录 · 内存取舍

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-04-low-memory-dropout-technical-qa.xlsx)，第 6 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-06"></a>

## 06. Triton seeded dropout 处理长度 n=2057 的向量，BLOCK\_SIZE=1024；最后一个 program（pid=2）的 offsets 是半开区间 \[2048,3072)。这个 program 里的 tl.load、tl.rand 和 tl.store，哪些必须用 offset<n 的 boundary mask？依据是什么？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：tl.load 和 tl.store 必须用 boundary mask，tl.rand 不需要：只有访问内存的操作才有越界风险。

- **有效范围**：末块的 1024 个 offset 中，只有 \[2048,2057) 的 9 个落在输入范围内，其余 1015 个越界。
- **访存操作**：tl.load 读输入、tl.store 写输出，都要用 offset<2057 屏蔽越界位置；只保护 store 时，越界的 load 仍会读到向量之外。
- **纯计算**：tl.rand 只根据 seed 和整数 offset 计算随机数，不访问该 offset 处的内存，所以在无效 offset 上也可以算；这些位置的结果不会被写回。

**边界**：offsets 由 2048 加上 tl.arange(0,1024) 得到，tl.arange 不含右端点，所以末块是 2048…3071，而不是闭区间 \[2048,3072\]。

### 锚点

访存才要 mask，纯计算不必

### 来源

Lesson 04 · 8/24 学习记录 · 尾部 mask

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-04-low-memory-dropout-technical-qa.xlsx)，第 7 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-07"></a>

## 07. 判断张量重排并重新连续存储后，用同一个 seed 重算 dropout，能否让每个逻辑元素得到前向时的 keep/drop 决策。

类型：真实纠错 · 层级：原子 · 等级：A

适用范围：triton · 3.7.1

### 场景

前向时，连续存储的二维 tensor 按扁平 global offset 调用 tl.rand(seed, offsets)。recompute 前先把元素重新排列并物化成新的连续 tensor，例如 A=\[\[a,b,c\],\[d,e,f\]\] 变成 A.T.contiguous()；seed、p 和 tl.rand 实现都不变。

### 正确

不能保证：tl.rand 只认整数 offset，重排后 b 的 offset 由 1 变为 2、d 由 3 变为 1，recompute 调用 F(seed,2)、F(seed,1)，而前向用的是 F(seed,1)、F(seed,3)。

### 错误

能保证逻辑元素获得相同决策，因为 mask pattern 与输入元素连续性也没有关系

### 说明

**结论**：错在以为随机决策会跟着逻辑元素走：tl.rand(seed, offsets) 只接收整数 offset，不知道元素身份；重排并连续化改变了“逻辑元素 → offset”的映射。

- **逐元素追踪**：A 按行展平为 \[a,b,c,d,e,f\]，b、d 的 offset 是 1、3；A.T.contiguous() 为 \[\[a,d\],\[b,e\],\[c,f\]\]，展平为 \[a,d,b,e,c,f\]，b、d 的 offset 变为 2、1。
- **后果**：按 offset 排列的随机数序列没有变，却分给了不同的元素，所以重算出的 keep/drop 决策不能保证与前向一致。

**边界**：同一 seed 只保证同一 offset 得到同一随机数；只有“逻辑元素 → global offset”映射不变时，逻辑元素的决策才保持。

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-04-low-memory-dropout-correction.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-08"></a>

## 08. 面试官问：“在 Triton kernel 里怎样实现 dropout？稍后重算（例如反向传播）时需要和前向完全相同的 keep/drop 决策，但不想把 mask 存下来。”请在 60–90 秒内讲清：保留与缩放规则、随机决策怎样由 seed 和元素位置重建、重算时必须保持什么，以及相对显式保存 mask 的取舍。

类型：综合口述 · 层级：口述 · 等级：A

适用范围：triton · 3.7.1

### 参考回答

**结论**：用 seed 加每个元素的 global offset 现场生成随机数来重建 mask：只需保存一个 seed，代价是每次都要重新计算随机数。

- **数学规则**：每个元素以概率 p 丢弃并输出 0，以 1−p 保留并输出 x/(1−p)，所以单元素输出的期望仍是 x。
- **随机位置**：元素用 tl.rand(seed, offset) 取随机数，再与 p 比较；offset 必须是 pid×BLOCK+local 的 global offset，若各 program 都传从 0 开始的 local offset，每块会重复同一随机模式。
- **重算条件**：要得到同样的随机数，需保持 seed、PRNG 实现和“逻辑元素 → offset”映射；同样的决策还要同一个 p；同样的输出还要输入值、dtype 与数值语义一致。
- **取舍**：显式方案要物化、保存并读回 O(N) 的 mask，seeded 方案只存 O(1) 的 seed；但输入输出访问和缩放仍在，还多了 PRNG 计算，所以不能直接断言更快。

### 评分锚点

说明以 1−p 的概率保留并乘 1/(1−p)，使单元素期望仍为 x；说明 tl.rand 要用 seed 和 global offset，local offset 会让各块重复同一随机模式；按随机数、决策、输出三层说出重算时要保持的条件；说明省掉 O(N) mask 的物化、保存与读取，换来 PRNG 计算，因此不能直接断言更快

### 来源

Lesson 04 · 8/24 学习记录 · 综合口述

**来源记录：** [Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录](../../logs/2026-08-24-low-memory-dropout.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-04-low-memory-dropout-oral.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)
