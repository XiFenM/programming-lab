# Triton Lesson 06 · Fused Attention · 复习卡片预览

> 共 **34 张**：技术问答 29 张、真实纠错 3 张、综合口述 2 张。
> 本文按正式卡片的原有顺序呈现全部题面与答案，可先看目录尝试回忆，再跳转核对。
> 阅读版由已校验的 XLSX 导出；卡片更新后需重新导出本文。

[卡片包与导入模板](../triton-lesson-06-fused-attention.md) · [全部课程预览](README.md)

**正式表格：** [真实纠错 XLSX](../triton-lesson-06-fused-attention-correction.xlsx) · [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx) · [综合口述 XLSX](../triton-lesson-06-fused-attention-oral.xlsx)

## 题目目录

| 编号 | 类型 | 题目 |
| --- | --- | --- |
| 01 | 技术问答 | [在一个 attention head 内，Q、K、V 都是形状为 \[N,D\] 的张量，分别表示 N 个 token 的 query、key 和 value；s 是给定的点积分数缩放系数。暂不考虑分块，如何由它们计算输出 O？说明各阶段的作用和结果形状。](#card-01) |
| 02 | 技术问答 | [普通 Attention 按 S=sQKᵀ、P=softmax(S)、O=PV 逐步计算（N 个 query、N 个 key，s 为缩放系数），每一步都先得到完整结果再交给下一步。FlashAttention 改为按块计算后，省掉的是哪一类开销，哪一类主要工作仍然保留？](#card-02) |
| 03 | 技术问答 | [在 Triton 官方 fused-attention 教程（快照版）的 FP16 前向中，输入 Q/K/V 的形状是 \[B,H,N,D\]：B 为 batch 数、H 为 head 数、N 为 token 数、D 为每个 head 的特征维。BLOCK\_M 是一个 Q tile 的行数。grid=(ceil(N/BLOCK\_M),B×H,1) 怎样把计算和最终输出分给各 program？](#card-03) |
| 04 | 技术问答 | [连续 FP16 Q/K/V 原本形状为 \[B,H,N,D\]，B/H 分别为 batch/head 数，N 为 token 数，D 为特征维。现在 descriptor 将 batch、head、token 合并成 \[BHN,D\] 的二维视图。已知 batch=b、head=h、head 内 token=t，这个 token 在 descriptor 中的全局行号怎样计算？](#card-04) |
| 05 | 技术问答 | [分块 Attention 前向中，一个 program 负责 B\_M 个 query；本轮读入 B\_N 个 key/value，每个 value 是 D 维特征向量；当前块的未归一化指数权重 p 形状为 \[B\_M,B\_N\]。跨多轮 K/V 累计 pV 的输出分子 acc 应是什么形状？请用乘加时被归约和被保留的轴说明。](#card-05) |
| 06 | 技术问答 | [固定一个 query，Attention 前向已经扫描过若干 K/V 块，并保存运行最大值 m、指数和 l、加权 V 分子 acc。新 key 块 J 的分数 x\_j 已换到 exp2 的输入域，但尚未取指数。怎样把这个新块并入旧状态，最终得到该 query 的输出？](#card-06) |
| 07 | 技术问答 | [某个分块 Attention 前向把每个 query 的在线状态初始化为 m=−∞、l=1、acc=0，其中 m 是 exp2 输入域分数的运行最大值。假设首块至少有一个有效 key，有效 score 都有限，无效位置被 mask 为 −∞。为什么初始的 l=1 不会进入最终分母？](#card-07) |
| 08 | 技术问答 | [在 causal Attention 前向中，一个 program 负责 head 内 query 区间 \[a,b)。causal 规则是 query i 只能读取 key j≤i。为了减少逐元素 mask，这个 program 应怎样划分要扫描的 key 区域？](#card-08) |
| 09 | 技术问答 | [Triton 官方 fused-attention 教程（快照版）的前向 kernel 有一个编译期参数 STAGE，causal 时取 3、non-causal 时取 1；它的 autotune 候选配置里另有 num\_stages。这两个名字相近的参数分别控制什么？](#card-09) |
| 10 | 技术问答 | [Attention 前向采用 exp2，令 x\_j=S\_j/ln2，其中 S\_j 是已乘原始 scale 的点积分数。它为一行有效 key 保存 m=max(x\_j)、l=Σ2^(x\_j−m)，并只把 M=m+log₂(l) 留给反向。为什么反向用 2^(x\_j−M) 就能恢复概率，且没有丢掉减最大值的稳定化效果？](#card-10) |
| 11 | 技术问答 | [在 Triton 官方 fused-attention 教程（快照版）的 FP16 前向中，Q/K/V 以 FP16 存储，输出 O 也需要返回 FP16。沿 QKᵀ、softmax 在线统计、pV 到 O/M 写回这条路径，各阶段使用什么精度，关键转换发生在哪里？](#card-11) |
| 12 | 技术问答 | [Attention 前向中，p 是 FP32 的未归一化指数权重块：一路对每行求 sum(p) 累加到分母 l，另一路把 p 转成 FP16 后与 FP16 V 做矩阵乘。若把 sum(p) 改到 p 转成 FP16 之后再算，并且仍用 FP32 累加，分母会受什么影响？请从误差产生的位置解释。](#card-12) |
| 13 | 技术问答 | [Triton 官方 fused-attention 教程（快照版）的反向不保存前向算出的概率矩阵 P：前向末尾只为每个 query 留一个统计量 M，反向再按块用 Q/K 与 M 重算 P。输入有 B 个 batch、H 个 head，每个 head N 个 token。这个设计省下了什么，又多付出了什么？](#card-13) |
| 14 | 技术问答 | [阅读 Triton 官方 fused-attention 教程（快照版）的源码时，会看到前向 kernel 内多次调用 \_attn\_fwd\_inner，也会看到反向先启动 preprocess、再启动主 backward。它们分别怎样传递计算状态？为什么不能把每个 @triton.jit 函数调用都当成独立的 kernel launch？](#card-14) |
| 15 | 技术问答 | [对一个 head，前向为 S=sQKᵀ、P=softmax\_key(S)、O=PV；s 是固定缩放系数，Q/K/V 为 \[N,D\]。损失传来同形状的上游梯度 dO 后，如何依次算出 dP、分数梯度以及 dQ/dK/dV？](#card-15) |
| 16 | 技术问答 | [Attention 反向重建一个概率 tile 时，M 和 Delta 都是“每个 query 一个值”的统计量。如果概率 tile 有时按 \[Bq,Bk\]（query×key）存放，有时按 \[Bk,Bq\]（key×query）存放，这两个向量应怎样广播才能对应到正确 query？](#card-16) |
| 17 | 技术问答 | [分块计算 Attention 的 dK/dV 时，同一个 key 会接收多个 query 的梯度贡献。什么样的 program 分工可以在写回这些梯度时不用 atomic？如果把同一输出块的贡献拆给两个 program，为什么普通 store 不够？](#card-17) |
| 18 | 技术问答 | [causal Attention 规定 query i 只能使用 key j≤i。反向计算时，固定一个 query 来求 dQ，与固定一个 key 来求 dK/dV，分别要汇总哪一侧 token 的贡献？为什么扫描方向看起来相反？](#card-18) |
| 19 | 技术问答 | [Triton 官方 fused-attention 教程（快照版）的反向先把 K 预缩放为 K̃=(s/ln2)K。令 G=P⊙(dP−Delta) 表示损失对自然分数 S=sQKᵀ 的梯度。为什么 dQ 路径用 K̃ 累加后要乘 ln2，而 dK 路径用原始 Q 累加后要乘 s？](#card-19) |
| 20 | 技术问答 | [在 Triton 3.7.1 中，用 TensorDescriptor 描述展平后的 Q：base 指向连续 Q 的存储，shape=\[BHN,D\]、strides=\[D,1\]（B/H/N/D 分别为 batch 数、head 数、token 数和特征维），block\_shape=\[BLOCK\_M,D\]。一次 desc.load(\[r0,0\]) 读到的块由哪个参数决定大小、哪个参数决定位置？把起点改成 \[r0+BLOCK\_M,0\] 时，读到的块和返回的 shape 各怎样变化？](#card-20) |
| 21 | 技术问答 | [在 Triton 3.7.1 中，Attention 的 Q/K/V descriptor 把多个 batch/head 展平成 \[BHN,D\] 的视图，每个 head 占连续 N 行。若一次 load 跨过当前 head 的末尾、但仍在整个 BHN 行视图之内，越过 head 末尾的那些行会读到什么？为什么？](#card-21) |
| 22 | 技术问答 | [Attention 处理不足一个 tile 的尾部 key 时，假设 descriptor 已把无效位置的 K 和 V 都补成零。如果省掉对这些 key 的 score mask，直接让 softmax 和 pV 计算整个 tile，结果会怎样？为什么？](#card-22) |
| 23 | 技术问答 | [在 Triton 3.7.1 中，要把 PyTorch FP16 张量交给 NVIDIA TMA descriptor。设 x 是基址 16 字节对齐的一维连续 FP16 张量，它的切片 x\[1:\] 调用 is\_contiguous() 仍返回 True，却不满足 TMA 的布局条件。为什么连续还不够？传入前应检查哪些量？](#card-23) |
| 24 | 技术问答 | [在 Triton 3.7.1 中，把 Attention 的 K/V 读取从“指针加 mask 的 tl.load”改成 TensorDescriptor 的 desc.load。在支持 TMA 的 NVIDIA GPU 上，这种写法带来了什么能力？又有哪些事情不能据此断言？](#card-24) |
| 25 | 技术问答 | [Triton 官方 fused-attention 教程（快照版）的普通 FP16 路径中，D 表示每个 head 的特征维度。wrapper 在 host 侧先用 dummy\_block 创建 TensorDescriptor，而 autotune 会尝试不同 BLOCK\_M/BLOCK\_N。为什么每次配置运行前必须由 pre-hook 更新 block\_shape，不能指望 kernel 中的 \_maybe\_make\_tensor\_desc 自动改正确？](#card-25) |
| 26 | 技术问答 | [把 FP16 数值转换为 FP8 E5M2 时，即使数值落在 E5M2 的范围内、没有溢出，误差为什么仍可能明显变大？已知 E5M2 为 1 位符号、5 位指数、2 位显式小数，FP16 为 1、5、10。请用同一正规数指数区间内相邻可表示数的间距说明。](#card-26) |
| 27 | 技术问答 | [Triton 官方 fused-attention 教程（快照版）的 FP8 路径为 V 调整布局：B/H 分别是 batch/head 数，N 是 token 数，D 是特征维。从连续的 \[B,H,N,D\] 张量出发，先 permute 成 \[B,H,D,N\] 并 contiguous()，再用逆 permute 恢复 \[B,H,N,D\]。最终 shape 已恢复，为什么存储布局仍然改变？删掉中间 contiguous() 又会怎样？](#card-27) |
| 28 | 技术问答 | [对照两个 Attention 实现的反向结果：参考实现先执行 backward(dout)，再让被测实现执行反向，两边的 Q/K/V、causal 开关和 scale 都相同。为什么两边还必须使用同一个上游梯度 dout？](#card-28) |
| 29 | 技术问答 | [在同一个 Attention head 内，所有 query 向量都相同，K/V 和 scale 固定。非 causal 时，各行 O 与 M 为什么在数学上相同？改成 causal 后，这个“所有行相同”的结论为什么不能直接沿用？M 表示每行归一化分母的 base-2 对数。](#card-29) |
| 30 | 真实纠错 | [在线 softmax 手算：score 已乘原始 sm\_scale，属于自然指数域（softmax 权重为 e^score），还没有取指数。旧、新运行最大分数分别为 −15 和 −13。旧分母和旧分子都要乘同一个重标定系数，它等于多少？请分别写出用 exp 和用 exp2 表示的形式。](#card-30) |
| 31 | 真实纠错 | [在 Triton 官方 fused-attention 教程（快照版）的前后向流程中，哪些量是在前向结束时保存给反向使用的，哪些是在反向中临时计算的，哪些才是最终输出的梯度？请按产生时间和用途区分。](#card-31) |
| 32 | 真实纠错 | [Attention 反向预处理拿到前向输出 O 和上游梯度 dO，两者都是 \[B,H,N,D\]：N 是 query 数，D 是每个输出向量的特征数。为了得到每个 query 一个 Delta，实际应沿哪一维求和？它与沿 key 求和的公式有什么关系？](#card-32) |
| 33 | 综合口述 | [以 Triton 官方 fused-attention 教程（快照版）为例，向面试官用约 60–90 秒解释分块 Attention 前向：输入 Q/K/V 为 \[B,H,N,D\]，B/H 分别是 batch/head 数，N 是 token 数，D 是特征维度，s 为原始 scale；每个 program 负责一个 head 的 B\_M 行 Q，并逐块扫描 B\_N 行 K/V。请从完整 Attention 公式出发，说明它怎样维护跨块状态，并最终写出 O 和供反向使用的 M。](#card-33) |
| 34 | 综合口述 | [以 Triton 官方 fused-attention 教程（快照版）为例，向面试官在 90 秒内解释 Attention 反向的数据流：前向已由 Q/K/V 得到 O，并为每个 query 保存归一化统计量 M；现在收到损失对 O 的梯度 dO。请说明怎样利用保存量、计算 Delta、按块重建概率，并通过输出分工得到 dQ/dK/dV。](#card-34) |

<a id="card-01"></a>

## 01. 在一个 attention head 内，Q、K、V 都是形状为 \[N,D\] 的张量，分别表示 N 个 token 的 query、key 和 value；s 是给定的点积分数缩放系数。暂不考虑分块，如何由它们计算输出 O？说明各阶段的作用和结果形状。

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：先让每个 query 与所有 key 计算匹配分数，再把该行分数归一化为权重，最后用这些权重汇总 value。

- **匹配分数**：S=sQKᵀ 的形状为 \[N,N\]。S\[i,j\] 是 query i 与 key j 的缩放点积；它此时还没有取指数，也不是概率。
- **归一化**：沿 S 的每一行，也就是 key 轴做 softmax，得到同形状的 P。P\[i,j\] 是 query i 分配给 value j 的权重；每个有效行的权重和为 1。
- **输出**：O=PV 的形状为 \[N,D\]。O\[i,:\] 是第 i 个 query 对所有有效 value 向量的加权和，仍保留 D 个特征。
[E##S=sQK^{\mathsf T},\qquad P=\operatorname{softmax}\_{\mathrm{key}}(S),\qquad O=PV]

**边界**：causal 模式只允许 key 索引 j≤query 索引 i，包含自身；无效位置不参与归一化。这里的 Q/K/V 已由调用方生成，前面的线性投影和后面的多头输出投影都不属于此算子。

### 锚点

分数 → 沿 key 归一化 → 加权 V

### 来源

Attention 学习记录 09-24 · 全貌、符号与精度

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-02"></a>

## 02. 普通 Attention 按 S=sQKᵀ、P=softmax(S)、O=PV 逐步计算（N 个 query、N 个 key，s 为缩放系数），每一步都先得到完整结果再交给下一步。FlashAttention 改为按块计算后，省掉的是哪一类开销，哪一类主要工作仍然保留？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：省掉的是完整 N×N 分数矩阵与概率矩阵的物化，以及它们在全局显存中的写入和读回；QKᵀ 与 PV 两个主要矩阵乘仍要完成。

- **普通路径**：先写出完整 S，再读取它求 softmax 并写出 P，最后读取 P 与 V 相乘，会产生大量中间数据的存储和搬运。
- **分块路径**：固定一个 Q 块，逐块读取 K/V；分数和指数权重只作为当前块的临时量，旧块的影响由少量逐行统计量及输出累加器保留。
- **计算边界**：仍需对相关 query–key 对计算分数，并把权重作用到 V。对完整非因果注意力，主要矩阵乘工作量仍随 N²D 增长。

**边界**：减少显存流量是优化机制，不是固定倍数的加速承诺。实际耗时还与 GPU、输入形状、分块及实现有关。

### 锚点

不物化 N×N；仍计算 QKᵀ、PV

### 来源

Attention 学习记录 09-19 · 不物化 S/P 的要点

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-03"></a>

## 03. 在 Triton 官方 fused-attention 教程（快照版）的 FP16 前向中，输入 Q/K/V 的形状是 \[B,H,N,D\]：B 为 batch 数、H 为 head 数、N 为 token 数、D 为每个 head 的特征维。BLOCK\_M 是一个 Q tile 的行数。grid=(ceil(N/BLOCK\_M),B×H,1) 怎样把计算和最终输出分给各 program？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：每个 program 固定一个 batch/head 和一个 Q 行块，扫描这个行块需要的 K/V，最终独占写回对应的 O 行块及 M 行统计量。

- **第0轴**：program\_id(0) 选择 Q tile。编号为 p 的 tile 对应 head 内从 p×BLOCK\_M 开始的 query 行。
- **第1轴**：program\_id(1) 选择合并后的 batch/head 编号 g；可由 b=g//H、h=g%H 还原到具体输入切片。
- **内部循环**：K/V 的分块扫描在同一个 program 内完成。扫描多少轮与启动多少个 program 是不同概念；这个前向不是每个 Q×K 块都启动一个独立 program。
- **第2轴**：尾部 1 表示第三轴只有一个位置。该教程没有使用这根轴，把 grid 写成前两维即可表达相同分工。

**边界**：grid 轴的业务含义来自 kernel 如何使用 program\_id。它们不是 Triton 预先规定的 query、batch、head 轴。

### 锚点

Q tile × batch/head；K/V 在内部扫描

### 来源

Attention 学习记录 09-24 · 全貌、符号与精度

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-04"></a>

## 04. 连续 FP16 Q/K/V 原本形状为 \[B,H,N,D\]，B/H 分别为 batch/head 数，N 为 token 数，D 为特征维。现在 descriptor 将 batch、head、token 合并成 \[BHN,D\] 的二维视图。已知 batch=b、head=h、head 内 token=t，这个 token 在 descriptor 中的全局行号怎样计算？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：先求当前 batch/head 的序列起点，再加上该 head 内的 token 索引。

[E##g=bH+h,\qquad r=gN+t]
- **各量含义**：g 是合并后的 batch/head 编号，每个 g 占连续 N 行；因此 gN 是该 head 的首行，t 才是它内部的局部偏移。特征坐标 d 不参与这一步行号计算。
- **例子**：若 g=5、N=8，head 内 token 2、3 应读 descriptor 全局行 42、43。只写行号 2、3 会访问整个视图开头的 head。
- **用到哪里**：Q tile 起点和 K/V 的每轮扫描起点都需要加当前 head 基址。判断 causal 的先后关系时，也要保证两个 token 坐标使用同一坐标系。

**边界**：这是 FP16 的普通 \[BHN,D\] 视图；FP8 V 的重排 descriptor 使用另一组轴，不能直接套用这套行号公式。

### 锚点

先 gN，再加局部 token

### 来源

Attention 学习记录 09-19 · K descriptor 行号纠错；09-24 · TensorDescriptor、边界与启动准备

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 5 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-05"></a>

## 05. 分块 Attention 前向中，一个 program 负责 B\_M 个 query；本轮读入 B\_N 个 key/value，每个 value 是 D 维特征向量；当前块的未归一化指数权重 p 形状为 \[B\_M,B\_N\]。跨多轮 K/V 累计 pV 的输出分子 acc 应是什么形状？请用乘加时被归约和被保留的轴说明。

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：acc 的形状是 \[B\_M,D\]：乘加归约掉本轮的 key 轴 B\_N，保留 query 轴 B\_M 和特征轴 D，每个 query 对应一个 D 维加权 value 向量。

[E##\underbrace{p}\_{B\_M\times B\_N}\ \underbrace{V}\_{B\_N\times D}\ \longrightarrow\ \underbrace{acc}\_{B\_M\times D}]
- **归约轴**：乘加时对本轮的 key/value 索引求和，B\_N 这一轴被消去；下一轮 K/V 的贡献继续加到同一个 acc，形状不变。
- **逐行统计**：运行最大值 m、指数和 l、重标定系数 alpha 都是一 query 一个值，所以形状为 \[B\_M\]。给 acc 重标定时用 alpha\[:,None\] 沿 D 轴广播。

**边界**：形状由轴的含义决定，不能看数值：即使 B\_M 与 D 都取 64，acc 的两根轴仍分别是 query 和特征；B\_M=32、D=64 时 acc 为 \[32,64\]。

### 锚点

消去 key；留下 query × feature

### 来源

Attention 学习记录 09-24 · 全貌、符号与精度

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 6 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-06"></a>

## 06. 固定一个 query，Attention 前向已经扫描过若干 K/V 块，并保存运行最大值 m、指数和 l、加权 V 分子 acc。新 key 块 J 的分数 x\_j 已换到 exp2 的输入域，但尚未取指数。怎样把这个新块并入旧状态，最终得到该 query 的输出？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：先选择旧块与新块共同使用的最大值基准，再同步缩放旧分母和旧分子，加入新块贡献。

- **旧状态含义**：旧 l 是此前各 key 的 2^(x\_j−m) 之和；旧 acc 是这些权重乘 V\_j 后的向量和。acc 保存着旧 value 对输出的贡献，不能只留下 m 和 l。
[E##m'=\max\bigl(m,\max\_{j\in J}x\_j\bigr),\qquad \alpha=2^{m-m'},\qquad p\_j=2^{x\_j-m'}]
[E##l'=\alpha l+\sum\_{j\in J}p\_j,\qquad acc'=\alpha acc+\sum\_{j\in J}p\_jV\_j]
- **为何共同缩放**：旧权重原先减的是 m，现在必须改成减 m′，每一项都恰好多乘 2^(m−m′)。分母和加权分子使用同一批权重，所以必须一起缩放；若最大值不变，alpha=1。
- **最终输出**：扫描完所有有效 K/V 后，O=acc/l，其中 acc 是 D 维分子，l 是标量分母。对一个 Q tile 同时做这些操作时，每一行独立维护状态，Q tile 在整个扫描中保持不变。

**边界**：p\_j 在这里是当前最大值基准下的未归一化指数权重；它不是已经除以整行分母的概率 P\_j。

### 锚点

新最大值 → 同缩放 → 合并 → acc/l

### 来源

Attention 学习记录 09-19 · 第二轮保留量纠错；09-24 · 前向在线状态与源码语义

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 7 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-07"></a>

## 07. 某个分块 Attention 前向把每个 query 的在线状态初始化为 m=−∞、l=1、acc=0，其中 m 是 exp2 输入域分数的运行最大值。假设首块至少有一个有效 key，有效 score 都有限，无效位置被 mask 为 −∞。为什么初始的 l=1 不会进入最终分母？

类型：技术问答 · 层级：机制 · 等级：B

### 答案

**结论**：因为 m 从 −∞ 开始：首块使最大值变为有限数，重标定系数 alpha=2^(−∞−m\_new)=0，初始 l 被乘 0 消去。所以在这些条件下 l 初值取 0 或 1 都可以，关键是 m 必须从 −∞ 开始。

- **符号**：令 x\_j 表示尚未取指数、已换底为 exp2 标度的有效 key 分数，m\_new 是加入首块后的有限最大值；l₀ 是初始的有限分母状态。
[E##\alpha=2^{-\infty-m\_{new}}=0,\qquad l\_{new}=\alpha l\_0+\sum\_j2^{x\_j-m\_{new}}]
- **m初值的作用**：若误把 m 初始化为 0，而首块分数都小于 0，新最大值仍是 0，alpha=1，初始 l=1 会残留在分母里；若误写成 +∞，首次重标定就出现 inf−inf，得到 NaN。
- **异常值**：l=1 修复不了 inf−inf 产生的 NaN；首块全无效或含 +∞ 时，必须另行定义和处理数值语义，NaN 乘 0 仍是 NaN。

**边界**：这只说明该初始化在上述有效输入下成立；没有证据表明选择 1 是为了防止某种异常。

### 锚点

有限首块 → alpha=0 → 初始 l 消失

### 来源

Attention 学习记录 09-24 · 前向在线状态与源码语义；实践修改与 A4 独立解释

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 8 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-08"></a>

## 08. 在 causal Attention 前向中，一个 program 负责 head 内 query 区间 \[a,b)。causal 规则是 query i 只能读取 key j≤i。为了减少逐元素 mask，这个 program 应怎样划分要扫描的 key 区域？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：把 key 分成过去区 \[0,a)、对角区 \[a,b) 和未来区 \[b,N)：过去区全有效，对角区逐元素检查，未来区跳过。

- **过去区**：对任意 i∈\[a,b)，若 j<a，则 j≤i 恒成立，所以这部分 K/V 块可以直接参与计算。
- **对角区**：query 与 key 都在 \[a,b) 内时，有些 key 仍在当前 query 之后，必须按 j≤i 加 mask；当前位置自身也有效。
- **未来区**：若 j≥b，则它对整个 Q tile 都在未来，没有有效贡献，可以不扫描。
- **状态接续**：过去区和对角区属于同一批 query，必须接续同一个 m/l/acc。第一个 Q tile 的 a=0，过去区为空，实际处理直接从对角区开始。

**边界**：这里描述逻辑 token 区间。实际 tile 步长、尾块和整除条件仍需保证循环没有跨过应访问的范围。

### 锚点

过去／对角／未来

### 来源

Attention 学习记录 09-24 · 前向在线状态与源码语义

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 9 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-09"></a>

## 09. Triton 官方 fused-attention 教程（快照版）的前向 kernel 有一个编译期参数 STAGE，causal 时取 3、non-causal 时取 1；它的 autotune 候选配置里另有 num\_stages。这两个名字相近的参数分别控制什么？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：STAGE 决定前向扫描哪些 key 区段，管的是计算范围和 mask；num\_stages 是软件流水线深度，属于执行配置，不改变扫描哪些 key。

- **外层位掩码**：外层 STAGE 按位使用：3=0b11，STAGE&1 与 STAGE&2 都非零，于是先以内层模式 1 扫描过去区、再以模式 2 扫描对角区，两次调用接续同一组 m/l/acc；non-causal 的 1 只打开第一位，以内层模式 3 扫描整段序列。
- **两个“3”**：传给 \_attn\_fwd\_inner 的 1/2/3 是具体扫描模式（过去／对角／全序列），与外层位掩码同名不同义：外层 3 表示两段都执行，内层 3 表示扫描全序列。
- **num\_stages**：num\_stages 与 num\_warps、maxnreg 同属执行与资源配置：它设定编译器软件流水线的深度，影响性能和资源占用，但不是越大越好。

**边界**：num\_stages 不是 causal 的 STAGE：调整它不会改变 STAGE 决定的扫描区段和有效 key 范围。

### 锚点

STAGE 管扫描哪些段；num\_stages 管流水线多深

### 来源

Attention 学习记录 09-19 · STAGE 位掩码问题；09-24 · 前向在线状态与源码语义；FP8、布局与执行配置

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 10 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-10"></a>

## 10. Attention 前向采用 exp2，令 x\_j=S\_j/ln2，其中 S\_j 是已乘原始 scale 的点积分数。它为一行有效 key 保存 m=max(x\_j)、l=Σ2^(x\_j−m)，并只把 M=m+log₂(l) 留给反向。为什么反向用 2^(x\_j−M) 就能恢复概率，且没有丢掉减最大值的稳定化效果？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：M 是整行原始指数和的 log₂；减去 M 同时完成了减最大值和除以归一化分母。

[E##M=m+\log\_2l=\log\_2\sum\_j2^{x\_j}]
[E##P\_j=2^{x\_j-M}=\frac{2^{x\_j-m}}{l}]
- **加回m的作用**：l 是减最大值后得到的指数和，比原始指数和少了因子 2^m。只保存 log₂(l) 会遗漏这个因子；加上 m 才恢复完整分母的对数。
- **稳定性**：对一行有限有效 score，最大值对应的指数项为 1，所以 l≥1，进而 M≥m≥x\_j。恢复有效概率时指数不大于 0，不会出现指数上溢。

**边界**：这个结论限定在有效位置以及前后向使用一致分数的数学运算；全屏蔽行、非有限输入需要单独处理，浮点也仍可能舍入或下溢。M 是 log-sum-exp，不能再把它误认成行最大值 m。

### 锚点

先稳定求和；再保存 log 分母

### 来源

Attention 学习记录 09-19 · 加回 m 的问题；09-24 · 全貌、符号与精度

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 11 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-11"></a>

## 11. 在 Triton 官方 fused-attention 教程（快照版）的 FP16 前向中，Q/K/V 以 FP16 存储，输出 O 也需要返回 FP16。沿 QKᵀ、softmax 在线统计、pV 到 O/M 写回这条路径，各阶段使用什么精度，关键转换发生在哪里？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：矩阵乘用低精度操作数配合 FP32 累加，归一化与在线状态保留 FP32；中途 pV 前和最终 O 写回前都会发生降精度转换。

- **QKᵀ与score**：Q 和 K 是 FP16 操作数，点积累加结果为 FP32。后续缩放、最大值、减最大值和指数权重计算使用 FP32，保护归约和指数相关的数值计算。
- **在线状态**：每个 query 的最大值 m、指数和 l，以及 D 维输出分子 acc 都保留 FP32，使跨多个 K/V 块的合并不必每轮舍入到 FP16。
- **pV之前**：p 表示当前块的未归一化指数权重。先用 FP32 p 求分母增量，再把 p 转为 FP16，与 FP16 V 相乘；乘积继续累计到 FP32 acc。这次转换不可省：在 Triton 3.7.1 的这条路径上，tl.dot 的两个操作数要同型，FP32 p 不能直接与 FP16 V 相乘。
- **输出**：最后 acc/l 得到归一化输出，O 写回时转成 FP16；供反向重建概率的 M=m+log₂l 仍以 FP32 保存。

**边界**：这是该教程的精度安排。调用者看到的输入或输出 dtype，不能代表每一步内部运算精度；也不能概括成“只有最终 O 才转换精度”。

### 锚点

低精度乘法输入；高精度统计与累加

### 来源

Attention 学习记录 09-24 · 全貌、符号与精度；实践修改与 A4 独立解释

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 12 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-12"></a>

## 12. Attention 前向中，p 是 FP32 的未归一化指数权重块：一路对每行求 sum(p) 累加到分母 l，另一路把 p 转成 FP16 后与 FP16 V 做矩阵乘。若把 sum(p) 改到 p 转成 FP16 之后再算，并且仍用 FP32 累加，分母会受什么影响？请从误差产生的位置解释。

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：分母可能改变：转成 FP16 时的舍入已经发生在求和的输入上，FP32 累加只能更准确地加这些舍入后的值，找不回丢失的低位。

- **原顺序**：先对尚未降精度的 FP32 权重求行和，用于更新 l；然后仅为 pV 的矩阵乘把 p 转成 FP16。分母因此保留了转换前的权重信息。
- **交换后**：若先转换，传给求和的是 round\_fp16(p)，而不是原始 p。即使累加器是 FP32，也无法知道每个元素在转换中丢失了多少低位。
- **误差位置**：高精度累加主要减少累加过程引入的误差，不能撤销累加开始前已经发生的输入量化误差。这就是要分别考虑操作数和累加器精度的原因。
- **迁移（延伸）**：设计其他算子时同样要分开判断存储、操作数、累加器和输出 dtype：先明确误差与数值范围，识别指数、长归约等敏感环节，再决定低精度存储与转换位置，最后对照可信参考验证数值与性能。通用的是这套判断方法，不是固定的 dtype 配方。

**边界**：并非每组输入都会出现可见差异，例如恰好能被 FP16 精确表示的权重结果一致；但两种顺序不是普遍数值等价的改写，也不能凭输入或输出 dtype 推断内部精度。

### 锚点

先保住输入信息，再谈累加精度

### 来源

Attention 学习记录 09-24 · 前向在线状态与源码语义；全貌、符号与精度

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 13 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-13"></a>

## 13. Triton 官方 fused-attention 教程（快照版）的反向不保存前向算出的概率矩阵 P：前向末尾只为每个 query 留一个统计量 M，反向再按块用 Q/K 与 M 重算 P。输入有 B 个 batch、H 个 head，每个 head N 个 token。这个设计省下了什么，又多付出了什么？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：用一部分重复计算换掉 N² 量级的存储：不再保存、写出和读回每个 head 的 N×N 概率，只保存线性大小的 M；代价是反向要重新计算分数和概率。

- **省下的存储**：完整 P 为 \[B,H,N,N\]，M 只有 \[B,H,N\]。以 \[B,H,N,D\]=\[2,4,128,64\] 为例，P 有 2·4·128²=131072 个元素，M 只有 2·4·128=1024 个；两者相差 N 倍，N 越大差距越大。
- **多付的计算**：反向要重新计算 QKᵀ 并取指数来重建 P。教程 benchmark 的 FLOP 模型写作 2.0(bwd)+0.5(recompute)：dV、dP、dQ、dK 四个反向矩阵乘之外，再记一次重算的 QKᵀ，合计约为前向的 2.5 倍。
- **实际执行**：该实现的 dK/dV 与 dQ 两条路径还各自重算 score 和 dP，存在重复计算；2.5 是约定的计算量模型，不是硬件实际执行的运算次数。

**边界**：这是用计算换存储与显存读写的取舍，不是性能保证：是否更快要实测，2.5 也不能当作反向耗时相对前向的倍数。

### 锚点

存 O(N) 的 M，重算 O(N²) 的 P；省存储，多计算

### 来源

Attention 学习记录 09-19 · 只存行统计量的要点；09-24 · 正确性与 benchmark 边界

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 14 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-14"></a>

## 14. 阅读 Triton 官方 fused-attention 教程（快照版）的源码时，会看到前向 kernel 内多次调用 \_attn\_fwd\_inner，也会看到反向先启动 preprocess、再启动主 backward。它们分别怎样传递计算状态？为什么不能把每个 @triton.jit 函数调用都当成独立的 kernel launch？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：前向 inner 调用在同一个 kernel/program 内接续局部在线状态；反向的两个独立 Triton launch 则通过全局 Delta 缓冲区传递数据。

- **前向helper**：\_attn\_fwd\_inner 是 JIT 辅助函数。它更新当前 Q tile 的 m、l、acc，并返回新状态；外层必须按返回顺序重新绑定变量，后续区域才能继续之前的累加。
- **前向出错方式**：只调用 helper 却不接收返回值，不能指望 helper 内的重新赋值自动更新外层局部变量。causal 的过去区和对角区就可能失去状态接续。
- **反向launch**：\_attn\_bwd\_preprocess 用 O 和 dO 计算 Delta，并写入全局缓冲区；随后主反向读取它，以及 Q、预缩放 K、V、M、dO，生成输入梯度。

**边界**：反向 wrapper 还包含 K 的预缩放等操作。因此“两次 Triton kernel 启动”只是在描述这两个显式 launch，不代表整个反向恰好只有两项 GPU 操作。

### 锚点

局部返回状态；全局传递 Delta

### 来源

Attention 学习记录 09-24 · 全貌、符号与精度；实践修改与 A4 独立解释

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 15 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-15"></a>

## 15. 对一个 head，前向为 S=sQKᵀ、P=softmax\_key(S)、O=PV；s 是固定缩放系数，Q/K/V 为 \[N,D\]。损失传来同形状的上游梯度 dO 后，如何依次算出 dP、分数梯度以及 dQ/dK/dV？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：沿前向的相反方向：先从 O=PV 回传到 P/V，再通过每行 softmax 回传到 S，最后通过缩放点积回传到 Q/K。

- **记号**：dP 表示损失对概率 P 的梯度；令 G=∂L/∂S，避免把“对自然分数 S 的梯度”与某种源码临时变量混淆。S、P、dP、G 都是 \[N,N\]。
[E##dP=dOV^{\mathsf T},\qquad dV=P^{\mathsf T}dO]
[E##\Delta\_i=\sum\_jP\_{ij}dP\_{ij}=\sum\_dO\_{id}\,dO\_{id},\qquad G\_{ij}=P\_{ij}(dP\_{ij}-\Delta\_i)]
[E##dQ=sGK,\qquad dK=sG^{\mathsf T}Q]
- **形状与分块**：dQ/dK/dV 都回到 \[N,D\]。实现用右式 Σ\_d O\_id·dO\_id 从保存的 O 与传入的 dO 算出 Δ，再按块用 Q/K 和保存的 M 重建 P、累计这些梯度，无需保存完整 N×N 概率。

**边界**：causal 模式中，无效 query–key 位置的 P 和 G 均不贡献梯度。这里求的是对 Q/K/V 的梯度，假设 s 固定。

### 锚点

O → P/V → S → Q/K

### 来源

Attention 学习记录 09-24 · 反向统计量、归约与缩放

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 16 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-16"></a>

## 16. Attention 反向重建一个概率 tile 时，M 和 Delta 都是“每个 query 一个值”的统计量。如果概率 tile 有时按 \[Bq,Bk\]（query×key）存放，有时按 \[Bk,Bq\]（key×query）存放，这两个向量应怎样广播才能对应到正确 query？

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：先找出概率 tile 的 query 轴，让每个统计量保持与对应 query 的绑定，再沿 key 轴复制。

- **query在行**：对于 \[Bq,Bk\]，M 与 Delta 的形状都是 \[Bq\]。用 M\[:,None\]、Delta\[:,None\] 得到 \[Bq,1\]，向同一 query 的各个 key 列广播。
- **query在列**：对于 \[Bk,Bq\]，query 是第二轴。用 M\[None,:\]、Delta\[None,:\] 得到 \[1,Bq\]，向各个 key 行广播。
- **为什么会不同**：该教程的 dQ 路径固定 Q 并扫描 K/V，使用 query×key 布局；dK/dV 路径固定 K/V 扫描 Q，使用转置的 key×query 布局。

**边界**：不能按变量名照抄另一路的 \[:,None\] 或 \[None,:\]。M 用来恢复概率，Delta 用来计算 softmax 梯度，但它们都必须跟随 query 轴。

### 锚点

统计量属于 query；广播跨 key

### 来源

Attention 学习记录 09-24 · 反向统计量、归约与缩放

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 17 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-17"></a>

## 17. 分块计算 Attention 的 dK/dV 时，同一个 key 会接收多个 query 的梯度贡献。什么样的 program 分工可以在写回这些梯度时不用 atomic？如果把同一输出块的贡献拆给两个 program，为什么普通 store 不够？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：让一个 program 算齐某个 dK/dV 输出块的全部贡献，并让它成为该块唯一的写入者，就无需跨 program 的 atomic 累加。

- **完整归约**：固定一个 K/V tile 后，负责它的 program 扫描所有有效 query 块，在自己的累加器中把各块贡献求和。扫描结束后只写回一次完整结果。
- **独占输出**：不同 program 可以并行计算不同 K/V 输出块，因为它们的写入位置不重叠；许多 query 参与同一输出，并不必然意味着许多 program 写同一地址。
- **拆分后的要求**：若两个 program 分别得到 A 和 B，最终结果需要 A+B。普通 store 只覆盖目标值，即使强制顺序也不会自动求和；可用 atomic，或分别写临时缓冲区后再归约。

**边界**：无需 atomic 的前提是“单个 program 完成完整归约且独占输出”。不能把它推广为所有 Attention 反向实现都不需要同步或归约。

### 锚点

完整归约 + 独占输出

### 来源

Attention 学习记录 09-19 · dK/dV 无需 atomic 的要点；09-24 · 反向统计量、归约与缩放

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 18 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-18"></a>

## 18. causal Attention 规定 query i 只能使用 key j≤i。反向计算时，固定一个 query 来求 dQ，与固定一个 key 来求 dK/dV，分别要汇总哪一侧 token 的贡献？为什么扫描方向看起来相反？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：它们来自同一个因果约束，只是固定的索引不同：固定 i 时取 j≤i，固定 j 时取 i≥j。

- **dQ的归约**：求 query i 的 dQ，需要汇总它看得到的 key，所以扫描该位置及此前的 key：0≤j≤i。未来 key 从未参与其前向输出，没有对应贡献。
- **dK/dV的归约**：求 key/value j 的梯度，需要找到所有用过它的 query；这些 query 位于 j 及之后，即 j≤i<N。更早的 query 看不到这个未来 key。
- **分块时**：固定 query tile 通常扫描过去 key 区和对角区；固定 key tile 则扫描对角 query 区和后续区。对角块内部还要按逐元素 i/j 关系加 mask。

**边界**：两种范围都包含当前位置自身。不要把前向的“query 看过去 key”机械改写成“key 的梯度也只看过去 query”。

### 锚点

dQ 看过去 key；dK/dV 看后续 query

### 来源

Attention 学习记录 09-19 · causal 反向扫描范围的要点

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 19 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-19"></a>

## 19. Triton 官方 fused-attention 教程（快照版）的反向先把 K 预缩放为 K̃=(s/ln2)K。令 G=P⊙(dP−Delta) 表示损失对自然分数 S=sQKᵀ 的梯度。为什么 dQ 路径用 K̃ 累加后要乘 ln2，而 dK 路径用原始 Q 累加后要乘 s？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：末尾系数是在补回各路径尚缺或多带的缩放；两条路径输入中的 scale 并不相同。

- **dQ路径**：数学目标是 dQ=sGK。使用预缩放 K̃ 后，临时结果为 GK̃=(s/ln2)GK，已含 s，却多了 1/ln2，因此最后乘 ln2。
- **dK路径**：数学目标是 dK=sGᵀQ。该路径使用原始 Q 得到 GᵀQ，尚未包含 s，所以在写回前乘 s。
[E##(G\widetilde K)\ln2=sGK=dQ,\qquad s(G^{\mathsf T}Q)=dK]
- **常见遗漏**：如果漏掉 dQ 的末尾 ln2，结果会是正确 dQ 的 1/ln2 倍。dV=PᵀdO 则没有上述点积分数缩放，不需要这两项系数。

**边界**：必须追踪这个版本 wrapper 与 kernel 实际使用的张量。这里的 G 是对自然分数 S 的梯度；若另一实现选择不同表示域或预缩放位置，不能照搬末尾系数。

### 锚点

追踪预缩放；不要机械套同一系数

### 来源

Attention 学习记录 09-24 · 反向统计量、归约与缩放

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 20 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-20"></a>

## 20. 在 Triton 3.7.1 中，用 TensorDescriptor 描述展平后的 Q：base 指向连续 Q 的存储，shape=\[BHN,D\]、strides=\[D,1\]（B/H/N/D 分别为 batch 数、head 数、token 数和特征维），block\_shape=\[BLOCK\_M,D\]。一次 desc.load(\[r0,0\]) 读到的块由哪个参数决定大小、哪个参数决定位置？把起点改成 \[r0+BLOCK\_M,0\] 时，读到的块和返回的 shape 各怎样变化？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：大小由 descriptor 的 block\_shape 决定，位置由每次 load 的 offsets 决定。load(\[r0,0\]) 返回从第 r0 行、第 0 列开始的 \[BLOCK\_M,D\] 块；起点改成 \[r0+BLOCK\_M,0\] 就读下一个 Q tile，返回 shape 仍是 \[BLOCK\_M,D\]。

- **视图**：base 指向已有存储，shape=\[BHN,D\] 与 strides=\[D,1\] 声明整个访问视图；strides 以元素为单位，换算字节偏移要再乘元素字节数。创建 descriptor 只建立访问描述，不会提前读取整个张量。
- **block\_shape**：\[BLOCK\_M,D\] 是每次 load 返回 tile 的局部形状，属于 descriptor 本身，不随单次 load 改变，也不等于整个视图的大小。
- **offsets**：offsets 是每次 load 的参数，不是创建 descriptor 时固定的块起点；改变它只移动读取位置。

**边界**：访问仍须满足该接口的布局、对齐和边界要求；offsets 越过视图时按 descriptor 的填充方式处理。

### 锚点

布局由描述给出；大小看 block\_shape；位置看 offsets

### 来源

Attention 学习记录 09-24 · TensorDescriptor、边界与启动准备

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 21 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-21"></a>

## 21. 在 Triton 3.7.1 中，Attention 的 Q/K/V descriptor 把多个 batch/head 展平成 \[BHN,D\] 的视图，每个 head 占连续 N 行。若一次 load 跨过当前 head 的末尾、但仍在整个 BHN 行视图之内，越过 head 末尾的那些行会读到什么？为什么？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：会读到下一个 head 的真实数据，不会补零：descriptor 只按声明的整体视图判断越界，不知道其中哪 N 行属于当前 head。

- **为何仍合法**：跨到下一 head 的行号只要仍小于 BHN，就是 \[BHN,D\] 中的合法坐标，load 会把它当作正常数据读出。
- **需要保证的范围**：调用方必须正确计算当前 head 的基址，并限制本 program 的 token 扫描范围；batch/head 的逻辑隔离是索引设计的一部分。
- **真正越界时**：只有超出整个声明视图的元素才会被填充：默认补零，返回 tile 的形状仍由 block\_shape 决定。
- **填充值（延伸）**：填充值在构造 descriptor 时从 zero（默认）和 nan 两种预设中选定：host 侧 TensorDescriptor 用 padding 参数，kernel 内 tl.make\_tensor\_descriptor 用 padding\_option，nan 只适用于浮点数据。它不能像 tl.load 的 other 那样每次指定任意值；需要别的值时，在 load 后按有效条件替换，或改用带 mask 的普通 tl.load。

**边界**：自动处理视图越界，不等于自动实现 Attention 的 head 边界或 causal 规则；这些逻辑条件仍要由访问范围和 score mask 保证。

### 锚点

视图边界由 descriptor 管；head 范围由索引保证

### 来源

Attention 学习记录 09-24 · TensorDescriptor、边界与启动准备

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 22 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-22"></a>

## 22. Attention 处理不足一个 tile 的尾部 key 时，假设 descriptor 已把无效位置的 K 和 V 都补成零。如果省掉对这些 key 的 score mask，直接让 softmax 和 pV 计算整个 tile，结果会怎样？为什么？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：结果会错：零 K/V 没有把无效 key 从 softmax 的归一化集合中删除，每个无效 key 仍向分母贡献一个正项。

- **零K的分数**：对有限 query，零 K 的点积为零，乘 scale 后 score 仍为零。但零分数的指数权重不是零。
[E##S\_{ij}=0\quad\Longrightarrow\quad e^{S\_{ij}}=1]
- **稳定化也不删除**：本卡用自然分数 S 说明，令 m\_S=max(S)。减去最大值后，零分数的指数项为 exp(−m\_S)，仍会计入分母；稳定化没有删除这个无效 key。若换成 exp2，则最大值也必须使用对应的换底标度。
- **零V只影响分子**：零 V 使该项在加权分子中的直接贡献为零，但它仍占据分母，会把真实 key 的权重都压小。

**边界**：应在 score/概率上按有效 key 条件屏蔽这些位置，使它们不参与归一化。也不能改成把 K/V 填成 −∞ 来代替：以 K 为例，−∞ 与 q 的负分量相乘得 +∞、与 0 相乘得 NaN，点积可能变成 +∞ 或 NaN，不能保证得到所需的 −∞。

### 锚点

零数据不等于零概率；分母也要排除

### 来源

Attention 学习记录 09-24 · TensorDescriptor、边界与启动准备

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 23 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-23"></a>

## 23. 在 Triton 3.7.1 中，要把 PyTorch FP16 张量交给 NVIDIA TMA descriptor。设 x 是基址 16 字节对齐的一维连续 FP16 张量，它的切片 x\[1:\] 调用 is\_contiguous() 仍返回 True，却不满足 TMA 的布局条件。为什么连续还不够？传入前应检查哪些量？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：连续只说明元素按顺序紧挨着，不保证视图首地址对齐：x\[1:\] 的首地址比 x 后移 2 字节，已不是 16 的倍数。传入前要检查视图的实际首地址，以及按字节计的各维 stride。

- **需要的量**：设 A=tensor.data\_ptr() 为当前视图第一个元素的地址，e 为每元素字节数，s\_k 为第 k 维的元素 stride。descriptor 的 strides 参数以元素计，对齐条件则以字节计。
[E##A\bmod16=0,\qquad s\_{last}=1,\qquad (s\_ke)\bmod16=0\quad(k<last)]
- **偏移规律**：在对齐的存储上偏移 s 个元素、每个元素 e 字节后，视图仍对齐要求 s·e 是 16 的倍数；FP16 每元素 2 字节，偏移须是 8 个元素的倍数。
- **contiguous的限制**：如果这个视图本来就连续，contiguous() 可以直接返回它，不会为了对齐自动分配新存储。因此调用 contiguous() 不能替代地址检查。

**边界**：这里只列出本路径的基础布局条件。即使这些条件满足，也还需要核对 block\_shape、设备支持及后续矩阵乘的限制。

### 锚点

查实际首地址与字节步长；连续不保证对齐

### 来源

Attention 学习记录 09-24 · TensorDescriptor、边界与启动准备

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 24 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-24"></a>

## 24. 在 Triton 3.7.1 中，把 Attention 的 K/V 读取从“指针加 mask 的 tl.load”改成 TensorDescriptor 的 desc.load。在支持 TMA 的 NVIDIA GPU 上，这种写法带来了什么能力？又有哪些事情不能据此断言？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：它让规则矩形块的访问可以交给 TMA 硬件处理多维搬运、寻址和越界填充，为访存与计算重叠创造条件；但这只是能力，不保证比普通 tl.load 更快。

- **带来的能力**：descriptor 事先声明视图的 shape、strides 和 block\_shape，之后每次 load 只给块起点；在支持的硬件上，块的地址计算和越界填充由 TMA 完成。
- **不保证更快**：实际收益取决于 descriptor 的构造成本、块配置、编译结果和设备，要实测才能下结论。
- **不说明存放位置**：desc.load 返回的是参与计算的 tl.tensor，不能只凭这一行判断数据始终放在某种片上存储里。

**边界**：这些能力以硬件支持 TMA 为前提，张量还要满足 descriptor 的对齐与布局条件。

### 锚点

TMA 提供搬运与填充的能力，不提供更快的保证

### 来源

Attention 学习记录 09-24 · TensorDescriptor、边界与启动准备

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 25 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-25"></a>

## 25. Triton 官方 fused-attention 教程（快照版）的普通 FP16 路径中，D 表示每个 head 的特征维度。wrapper 在 host 侧先用 dummy\_block 创建 TensorDescriptor，而 autotune 会尝试不同 BLOCK\_M/BLOCK\_N。为什么每次配置运行前必须由 pre-hook 更新 block\_shape，不能指望 kernel 中的 \_maybe\_make\_tensor\_desc 自动改正确？

类型：技术问答 · 层级：机制 · 等级：B

适用范围：triton · tutorial source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：host 传入的已经是 descriptor，helper 会原样返回它；因此进入 kernel 前，它的块大小就必须与当前配置一致。

- **占位阶段**：dummy\_block 只是构造 descriptor 时的占位形状。实际一轮候选可能选择不同的 Q tile 行数 BLOCK\_M 和 K/V tile 行数 BLOCK\_N。
- **pre-hook的职责**：运行每个候选前，把 Q/O descriptor 的 block\_shape 改为 \[BLOCK\_M,D\]，K/V 改为 \[BLOCK\_N,D\]，使 load/store 的实际形状匹配该候选。
- **helper两条路径**：收到普通指针时，helper 才使用 shape、strides、block\_shape 构造 descriptor；收到已有 descriptor 时直接返回，额外传入的 block\_shape 不会覆盖对象。

**边界**：pre-hook、grid 和 kernel 内计算形状必须使用同一候选配置。这个问题来自该教程的 host descriptor 调用方式，不能假设所有 descriptor 都必须采用 dummy\_block。

### 锚点

当前配置 → 更新 descriptor → 原样传入 kernel

### 来源

Attention 学习记录 09-24 · TensorDescriptor、边界与启动准备；FP8、布局与执行配置

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 26 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-26"></a>

## 26. 把 FP16 数值转换为 FP8 E5M2 时，即使数值落在 E5M2 的范围内、没有溢出，误差为什么仍可能明显变大？已知 E5M2 为 1 位符号、5 位指数、2 位显式小数，FP16 为 1、5、10。请用同一正规数指数区间内相邻可表示数的间距说明。

类型：技术问答 · 层级：原子 · 等级：B

### 答案

**结论**：因为小数位少：两者都有 5 位指数，但 E5M2 只有 2 位显式小数。同一正规指数区间内，它的相邻间距是 FP16 的 2^(10−2)=256 倍，转换时只能舍入到更稀疏的点上。

- **正规数模型**：在固定指数 e 的正规区间中，数值可写成符号×2^e×(1+f/2^p)，p 是显式小数位数。f 每增加 1，相邻数就相差 2^(e−p)。
[E##\frac{2^{e-2}}{2^{e-10}}=2^8=256]
- **含义**：E5M2 只有 2 位显式小数，同一个区间内可表示的点更稀疏。把 FP16 数值转为它时，即使不发生范围溢出，也可能产生更大的舍入误差。

**边界**：这里比较的是同一正规指数区间的间距，不覆盖零、非正规数或特殊值。指数位数主要关联范围，小数位数影响局部表示分辨率。

### 锚点

范围看指数；精度看小数位

### 来源

Attention 学习记录 09-24 · FP8、布局与执行配置

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 27 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-27"></a>

## 27. Triton 官方 fused-attention 教程（快照版）的 FP8 路径为 V 调整布局：B/H 分别是 batch/head 数，N 是 token 数，D 是特征维。从连续的 \[B,H,N,D\] 张量出发，先 permute 成 \[B,H,D,N\] 并 contiguous()，再用逆 permute 恢复 \[B,H,N,D\]。最终 shape 已恢复，为什么存储布局仍然改变？删掉中间 contiguous() 又会怎样？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：中间 contiguous() 按转置后的轴顺序复制了数据；逆 permute 只恢复逻辑轴顺序，不会把这次复制后的存储重新排列回去。

- **原布局**：连续 \[B,H,N,D\] 的末两维 stride 是 \[D,1\]，同一个 token 的 D 个特征相邻。令 g=bH+h，则元素 (g,n,d) 的线性偏移为 gND+nD+d。
- **复制后**：在 \[B,H,D,N\] 下做 contiguous 后，同一个特征的 N 个 token 相邻。再恢复逻辑 shape，末两维 stride 变成 \[1,N\]，元素偏移为 gND+dN+n。
[E##gND+nD+d\ \longrightarrow\ gND+dN+n]
- **删除中间复制**：仅连续做两次互逆 permute 会把 shape 和 stride 都恢复，底层存储没有搬动。对于原本连续的张量，最后再调用 contiguous 通常也无需复制。

**边界**：判断布局必须同时看 shape、stride 和是否发生实际复制。此处解释的是该教程的 V 重排；后续转换为 FP8 的 dtype 操作，与轴布局变化是另一件事。

### 锚点

shape 相同不保证存储布局相同

### 来源

Attention 学习记录 09-24 · FP8、布局与执行配置

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 28 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-28"></a>

## 28. 对照两个 Attention 实现的反向结果：参考实现先执行 backward(dout)，再让被测实现执行反向，两边的 Q/K/V、causal 开关和 scale 都相同。为什么两边还必须使用同一个上游梯度 dout？

类型：技术问答 · 层级：机制 · 等级：B

适用范围：pytorch/triton attention correctness test · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 答案

**结论**：因为 dout 也是反向的输入：backward(dout) 可理解为对固定 dout 的标量 L=Σ(O\*dout) 求导，换一个 dout 就是在求另一个损失的梯度，两边的差异不能归因于 kernel。

- **同一前向问题**：Q/K/V、causal 开关与原始 scale 决定前向函数本身；它们相同只保证两边算的是同一个 O。
- **dout的作用**：dout 即 dO，决定损失对输出各元素的加权；换一个 dout，得到的 dQ/dK/dV 通常也会变。

**边界**：另需注意 PyTorch 的 backward 会累计叶子张量的 .grad：保存参考梯度后要清空，否则第二次读到的是两次结果之和。前向 O 一致也不能替代对 dout 一致性的检查。

### 锚点

dout 也是反向输入；同一个 dout 才能比较梯度

### 来源

Attention 学习记录 09-24 · 正确性与 benchmark 边界

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 29 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-29"></a>

## 29. 在同一个 Attention head 内，所有 query 向量都相同，K/V 和 scale 固定。非 causal 时，各行 O 与 M 为什么在数学上相同？改成 causal 后，这个“所有行相同”的结论为什么不能直接沿用？M 表示每行归一化分母的 base-2 对数。

类型：技术问答 · 层级：机制 · 等级：B

### 答案

**结论**：相同 Q 让每行对同一个 key 的分数相同；只有每行的有效 key 集合也相同，权重、O 和 M 才相同。causal 下有效集合随 query 位置变化，这个前提不再成立。

- **非causal**：每个 query 都访问完整 K/V，因此分数序列和归一化集合都相同。softmax 概率相同，加权相同的 V 后输出也相同，分母的 log₂ 即 M 同样相同。
- **causal下的M**：第 i 行只访问 j≤i 的前缀，包含自身。分数有限时，每多一个有效 key，分母就多一个正项，所以 M 随有效前缀严格增长，各行的 M 互不相同。
- **causal下的O**：O 通常随之变化，但不必两两不同：例如所有 value 向量都相同时，每行输出都等于这个 value，各行必然相同。

**边界**：这里讨论同一 head、同一 scale、有限 score 下的数学关系；浮点实现还有舍入误差。“O 通常变化”不能加强成“任意两行的 O 必定不同”。

### 锚点

相同 score + 相同有效集合

### 来源

Attention 学习记录 09-24 · 实践修改与 A4 独立解释

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 30 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-30"></a>

## 30. 在线 softmax 手算：score 已乘原始 sm\_scale，属于自然指数域（softmax 权重为 e^score），还没有取指数。旧、新运行最大分数分别为 −15 和 −13。旧分母和旧分子都要乘同一个重标定系数，它等于多少？请分别写出用 exp 和用 exp2 表示的形式。

类型：真实纠错 · 层级：原子 · 等级：A

### 场景

要把已累积的分母 l 和加权 V 分子 acc 换到新最大值的基准上；kernel 内部用 exp2 计算指数。

### 正确

系数为 e^(−15−(−13))=e^(−2)；改用 exp2 时要先把自然分数差除以 ln2，写成 2^(−2/ln2)，数值仍是 e^(−2)。

### 错误

那么重标定系数为2^(-2)

### 说明

**结论**：错在把自然指数域的分数差 −2 直接交给 exp2，跳过了换底；判断旧分母和旧分子都要重标定是对的。

- **定义**：令 s\_j 表示已乘原始 sm\_scale 的点积分数，x\_j=s\_j/ln2 表示供 exp2 使用的分数。两者均尚未取指数。
[E##e^{s\_j}=2^{x\_j},\quad x\_j=s\_j/\ln2,\qquad \alpha=2^{x\_{old}-x\_{new}}=e^{s\_{old}-s\_{new}}]
- **代入**：这里自然分数差为 −2，因此 alpha=e⁻²。把 −2 直接交给 exp2 相当于跳过换底，得到的 1/4 不是相同权重基准。
- **用于状态**：旧分母 l 与旧加权 V 分子 acc 都乘同一个 alpha；原答在这一点上正确，需要修正的只是系数。

**边界**：给定分数时先确认它处于哪个表示域：只有已换到 exp2 输入域、已含 1/ln2 的分数差，才能直接作为 2 的指数。

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-06-fused-attention-correction.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-31"></a>

## 31. 在 Triton 官方 fused-attention 教程（快照版）的前后向流程中，哪些量是在前向结束时保存给反向使用的，哪些是在反向中临时计算的，哪些才是最终输出的梯度？请按产生时间和用途区分。

类型：真实纠错 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 场景

前向已用 Q/K/V 计算 O，随后损失函数会提供上游梯度 dO。需要梳理自动求导上下文保存的输入，与反向运算新产生的中间量和输出。

### 正确

前向保存 Q/K/V/O/M；反向用 O、dO 生成 Delta 并按块重建 score/P；最终输出 dQ/dK/dV。

### 错误

backward保存dQ、dK和dV，重新计算了P

### 说明

**结论**：错在把反向的最终输出 dQ/dK/dV 当成保存量；原答“重新计算了 P”是对的，只是没有说出前向真正保存的 Q/K/V/O/M。

- **前向保存**：Q/K/V 是原输入，O 是前向输出，M 是每个 query 的 base-2 log-sum-exp。官方 wrapper 把这些量交给 ctx，以便之后求输入梯度。
- **反向临时量**：损失传来 dO 后，预处理先计算逐 query 的 Delta=sum\_d(O\*dO)。主反向利用 Q/K 和 M 按 tile 恢复概率 P，而非读取一张前向保存的完整 P。
- **最终梯度**：dQ、dK、dV 分别描述损失对三个输入张量的导数。它们是反向的结果，不能列为前向就已保存的数据。

**边界**：这是该教程的保存策略。其他 Attention 实现可能选择不同的保存与重算取舍；分类时仍按每个量何时产生、由谁消费来判断。

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-06-fused-attention-correction.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-32"></a>

## 32. Attention 反向预处理拿到前向输出 O 和上游梯度 dO，两者都是 \[B,H,N,D\]：N 是 query 数，D 是每个输出向量的特征数。为了得到每个 query 一个 Delta，实际应沿哪一维求和？它与沿 key 求和的公式有什么关系？

类型：真实纠错 · 层级：原子 · 等级：A

### 场景

要为 softmax 反向准备逐 query 的标量统计量。这里 i 标识 query，j 标识 key，d 标识输出特征，三个索引代表不同的归约方向。

### 正确

实际预处理沿特征 d 求和：Delta\_i=Σ\_d O\_id\*dO\_id，结果为 \[B,H,N\]。它等于 Σ\_j P\_ij\*dP\_ij，但两式的归约轴不同。

### 错误

delta=OdO对j求和

### 说明

**结论**：原答“O 与 dO 相乘”是对的，错在归约轴：实现对同一 query 的 D 个特征求和，即 O\[i,:\] 与 dO\[i,:\] 两个 D 维向量的点积，而不是对 key j 求和。

- **概率与梯度**：P\_ij 是 query i 对 key j 的 softmax 概率，dP\_ij 是损失对该概率的梯度；它们都用 query×key 两个轴索引。
[E##\Delta\_i=\sum\_d O\_{id}\,dO\_{id}=\sum\_j P\_{ij}\,dP\_{ij}]
- **恒等式来源**：由 O\_id=Σ\_j P\_ij V\_jd 和 dP\_ij=Σ\_d dO\_id V\_jd，交换有限求和顺序，就得到两个表达式相等。
- **实现意义**：右边需要该 query 对所有 key 的 P/dP；左边只需已经保存的 O 和传入的 dO，所以预处理不必为计算 Delta 再物化整行概率。
- **反向用途**：之后每个 query 的 Delta 可以在扫描多个 key 块时复用，用在 dS\_ij=P\_ij(dP\_ij−Delta\_i) 中。

**边界**：实际代码中的 O\*dO 归约轴是特征 D。不能因为等价式右边对 key j 求和，就把左边也说成“对 j 求和”。

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-06-fused-attention-correction.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-33"></a>

## 33. 以 Triton 官方 fused-attention 教程（快照版）为例，向面试官用约 60–90 秒解释分块 Attention 前向：输入 Q/K/V 为 \[B,H,N,D\]，B/H 分别是 batch/head 数，N 是 token 数，D 是特征维度，s 为原始 scale；每个 program 负责一个 head 的 B\_M 行 Q，并逐块扫描 B\_N 行 K/V。请从完整 Attention 公式出发，说明它怎样维护跨块状态，并最终写出 O 和供反向使用的 M。

类型：综合口述 · 层级：口述 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 参考回答

**结论**：分块实现与完整公式算的是同一个输出，只是靠逐行在线状态避免保存完整的概率矩阵。

- **公式与分工**：每个 head 算 S=sQKᵀ、P=softmax\_key(S)、O=PV。一个 program 固定一个 Q tile，在内部逐块扫描 K/V，并独占对应的输出行。
- **形状**：分数块是 \[B\_M,B\_N\]，沿 key 轴归约；acc 保留 query 与特征轴，是 \[B\_M,D\]；每个 query 的 m、l 各是一个标量。
- **跨块合并**：分数先换成 x=S/ln2 再用 exp2。m 是已见 x 的最大值，l=Σ2^(x−m)，acc 是同一权重下的加权 V；出现新最大值时，旧 l 与 acc 乘同一个 alpha，再加入新块。
- **最终写回**：扫描结束写出 O=acc/l，并保存 M=m+log₂l，即完整分母的 log₂；反向用 2^(x−M) 恢复概率。

**边界**：全程要分清 query、key、特征三根轴，以及未归一化的局部权重与最终概率。

### 评分锚点

写出带原始 scale 的完整公式，并指出 softmax 沿 key 轴；明确一个 program 固定 Q tile、内部扫描 K/V 并独占输出；正确区分 score=\[B\_M,B\_N\] 与 acc=\[B\_M,D\]；解释 m/l/acc 的含义及分子分母共同重标定；说明 O=acc/l 以及 M 在反向恢复概率中的用途

### 来源

Attention 学习记录 09-19 与 09-24 · 全流程串联

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-06-fused-attention-oral.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-34"></a>

## 34. 以 Triton 官方 fused-attention 教程（快照版）为例，向面试官在 90 秒内解释 Attention 反向的数据流：前向已由 Q/K/V 得到 O，并为每个 query 保存归一化统计量 M；现在收到损失对 O 的梯度 dO。请说明怎样利用保存量、计算 Delta、按块重建概率，并通过输出分工得到 dQ/dK/dV。

类型：综合口述 · 层级：口述 · 等级：A

适用范围：triton fused-attention tutorial · source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317

### 参考回答

**结论**：反向用前向保存量和 dO 按块重建概率，再按各个梯度的归约方向分工，全程不物化 N×N 矩阵。

- **保存与准备**：前向保存 Q/K/V/O/M，dQ/dK/dV 是反向才产生的输出。预处理对每个 query 沿特征维算 Delta\_i=Σ\_d O\_id·dO\_id，一行一个标量。
- **恢复概率**：用 Q/K 重算分数并换到 exp2 域 x=S/ln2，再以 P=2^(x−M) 恢复概率；M 是完整分母的 log₂，不只是行最大值。
- **梯度链**：dV=PᵀdO，dP=dO·Vᵀ；对自然分数 S 的梯度 G=P⊙(dP−Delta)；dQ=s·G·K，dK=s·Gᵀ·Q，s 为原始 scale。
- **输出所有权**：dK/dV 固定 key、沿 query 汇总，dQ=s·G·K 则固定 query、沿 key 汇总；一个 program 算齐自己的输出块后独占写回，不需要 atomic。

**边界**：若把同一输出块的归约拆给多个 program，就要另外合并部分贡献。

### 评分锚点

区分前向保存的 Q/K/V/O/M、反向临时量与最终梯度；说明 Delta 沿特征维求和、每个 query 一个值；说明用 M 重建概率，且 M 不只是行最大值；说出 G=P⊙(dP−Delta)，以及 dQ/dK/dV 各由哪两个量相乘；把归约方向与单 program 完整归约、独占写回联系起来

### 来源

Attention 学习记录 09-19 与 09-24 · 全流程串联

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)；[9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-06-fused-attention-oral.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)
