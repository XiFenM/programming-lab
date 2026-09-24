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
| 02 | 技术问答 | [普通 Attention 会把 N 个 query 对 N 个 key 的分数矩阵 S，以及 softmax 概率矩阵 P，写入全局显存。FlashAttention 改为按块计算时，主要避免了什么开销？QKᵀ 和 PV 的计算量是否也因此消失？](#card-02) |
| 03 | 技术问答 | [在所学 FP16 Attention 前向中，输入 Q/K/V 的形状是 \[B,H,N,D\]：B 为 batch 数、H 为 head 数、N 为 token 数、D 为每个 head 的特征维。BLOCK\_M 是一个 Q tile 的行数。grid=(ceil(N/BLOCK\_M),B×H,1) 怎样把计算和最终输出分给各 program？](#card-03) |
| 04 | 技术问答 | [连续 FP16 Q/K/V 原本形状为 \[B,H,N,D\]，B/H 分别为 batch/head 数，N 为 token 数，D 为特征维。现在 descriptor 将 batch、head、token 合并成 \[BHN,D\] 的二维视图。已知 batch=b、head=h、head 内 token=t，这个 token 在 descriptor 中的全局行号怎样计算？](#card-04) |
| 05 | 技术问答 | [分块 Attention 前向中，一个 Q tile 有 B\_M 个 query；本轮 K/V tile 有 B\_N 个 key/value；每个 value 有 D 个特征。指数权重块的形状是 \[B\_M,B\_N\]。累加加权 V 的 acc 应是什么形状，为什么不能因 B\_M 恰好等于 D 就把它理解成 \[B\_M,B\_M\]？](#card-05) |
| 06 | 真实纠错 | [在 Attention 在线 softmax 的手算中，score 已乘原始 sm\_scale，但尚未除以 ln2，也没有取 exp 或 exp2。旧、新运行最大分数分别为 −15 和 −13，而 kernel 使用 exp2。旧状态应乘什么重标定系数？为什么不能直接写 2^(−2)？](#card-06) |
| 07 | 技术问答 | [固定一个 query，Attention 前向已经扫描过若干 K/V 块，并保存运行最大值 m、指数和 l、加权 V 分子 acc。新 key 块 J 的分数 x\_j 已换到 exp2 的输入域，但尚未取指数。怎样把这个新块并入旧状态，最终得到该 query 的输出？](#card-07) |
| 08 | 技术问答 | [所学 Attention 前向将每个 query 的在线状态初始化为 m=−∞、l=1、acc=0。其中 m 是 exp2 输入域分数的运行最大值。假设首块至少有一个有效 key，且所有有效 score 都有限（无效位置可被 mask 为 −∞），为什么初始 l=1 不会使 softmax 分母多出 1？改成 l=0 是否也可行？](#card-08) |
| 09 | 技术问答 | [在 causal Attention 前向中，一个 program 负责 head 内 query 区间 \[a,b)。causal 规则是 query i 只能读取 key j≤i。为了减少逐元素 mask，这个 program 应怎样划分要扫描的 key 区域？](#card-09) |
| 10 | 技术问答 | [Attention 前向采用 exp2，令 x\_j=S\_j/ln2，其中 S\_j 是已乘原始 scale 的点积分数。它为一行有效 key 保存 m=max(x\_j)、l=Σ2^(x\_j−m)，并只把 M=m+log₂(l) 留给反向。为什么反向用 2^(x\_j−M) 就能恢复概率，且没有丢掉减最大值的稳定化效果？](#card-10) |
| 11 | 技术问答 | [在所学 FP16 Attention 前向实现中，Q/K/V 以 FP16 存储，输出 O 也需要返回 FP16。沿 QKᵀ、softmax 在线统计、pV 到 O/M 写回这条路径，各阶段使用什么精度，关键转换发生在哪里？](#card-11) |
| 12 | 技术问答 | [Attention 前向中，p 是 FP32 的未归一化指数权重块，l 要累加每行的 sum(p)；另一路会把 p 转成 FP16 后与 FP16 V 做矩阵乘。如果把 sum(p) 移到 p 转 FP16 之后，即使仍用 FP32 累加，能保证分母结果不变吗？](#card-12) |
| 13 | 技术问答 | [阅读或设计一个新的深度学习算子时，输入和输出可能使用 FP16，但内部还有矩阵乘、长归约或指数运算。应怎样决定各阶段的精度，而不是凭输入 dtype 猜测全部内部计算类型？](#card-13) |
| 14 | 真实纠错 | [在所学 PyTorch/Triton Attention 的前后向流程中，哪些量是在前向结束时保存给反向使用的，哪些是在反向中临时计算的，哪些才是最终输出的梯度？请按产生时间和用途区分。](#card-14) |
| 15 | 技术问答 | [阅读所学 Attention 源码时，会看到前向 kernel 内多次调用 \_attn\_fwd\_inner，也会看到反向先启动 preprocess、再启动主 backward。它们分别怎样传递计算状态？为什么不能把每个 @triton.jit 函数调用都当成独立的 kernel launch？](#card-15) |
| 16 | 真实纠错 | [Attention 反向预处理拿到前向输出 O 和上游梯度 dO，两者都是 \[B,H,N,D\]：N 是 query 数，D 是每个输出向量的特征数。为了得到每个 query 一个 Delta，实际应沿哪一维求和？它与沿 key 求和的公式有什么关系？](#card-16) |
| 17 | 技术问答 | [对一个 head，前向为 S=sQKᵀ、P=softmax\_key(S)、O=PV；s 是固定缩放系数，Q/K/V 为 \[N,D\]。损失传来同形状的上游梯度 dO 后，如何依次算出 dP、分数梯度以及 dQ/dK/dV？](#card-17) |
| 18 | 技术问答 | [Attention 反向重建一个概率 tile 时，M 和 Delta 都是“每个 query 一个值”的统计量。如果概率 tile 有时按 \[Bq,Bk\]（query×key）存放，有时按 \[Bk,Bq\]（key×query）存放，这两个向量应怎样广播才能对应到正确 query？](#card-18) |
| 19 | 技术问答 | [分块计算 Attention 的 dK/dV 时，同一个 key 会接收多个 query 的梯度贡献。什么样的 program 分工可以在写回这些梯度时不用 atomic？如果把同一输出块的贡献拆给两个 program，为什么普通 store 不够？](#card-19) |
| 20 | 技术问答 | [causal Attention 规定 query i 只能使用 key j≤i。反向计算时，固定一个 query 来求 dQ，与固定一个 key 来求 dK/dV，分别要汇总哪一侧 token 的贡献？为什么扫描方向看起来相反？](#card-20) |
| 21 | 技术问答 | [所学 Attention 反向先把 K 预缩放为 K̃=(s/ln2)K。令 G=P⊙(dP−Delta) 表示损失对自然分数 S=sQKᵀ 的梯度。为什么 dQ 路径用 K̃ 累加后要乘 ln2，而 dK 路径用原始 Q 累加后要乘 s？](#card-21) |
| 22 | 技术问答 | [使用 Triton TensorDescriptor 按块读取张量时，base、shape、strides、block\_shape 和 load(offsets) 分别决定什么？例如 B/H/N/D 分别表示 batch 数、head 数、token 数和特征维，Q 被展平成 \[BHN,D\]，每次取 BLOCK\_M 个 query。此时 block\_shape=\[BLOCK\_M,D\]，load(\[r0,0\]) 会读取哪个块？](#card-22) |
| 23 | 技术问答 | [Attention 的 Q/K/V descriptor 把多个 batch/head 展平成 \[BHN,D\]，每个 head 占 N 行。若一次 load 跨过当前 head 的末尾，却仍在整个 BHN 行视图之内，descriptor 会自动将越过这个 head 的位置补零吗？](#card-23) |
| 24 | 技术问答 | [Attention 处理不足一个 tile 的尾部 key 时，假设 descriptor 已把无效位置的 K 和 V 都补成零。能否省掉对这些 key 的 score mask，直接让 softmax 和 pV 计算整个 tile？](#card-24) |
| 25 | 技术问答 | [在 Triton 3.7.1 中，普通 tl.load 可用 other 指定 masked 位置的替代值。若改用 TensorDescriptor 的 load，能否同样传入任意 other 值？可选的 padding 在哪里设置？](#card-25) |
| 26 | 技术问答 | [把一个 PyTorch 张量传给 Triton 3.7.1 的 NVIDIA TMA descriptor 前，为什么仅检查 is\_contiguous() 不够？应怎样检查实际基址与 stride 的基础对齐条件，切片视图又会带来什么问题？](#card-26) |
| 27 | 技术问答 | [所学 Attention 的普通 FP16 路径中，D 表示每个 head 的特征维度。wrapper 在 host 侧先用 dummy\_block 创建 TensorDescriptor，而 autotune 会尝试不同 BLOCK\_M/BLOCK\_N。为什么每次配置运行前必须由 pre-hook 更新 block\_shape，不能指望 kernel 中的 \_maybe\_make\_tensor\_desc 自动改正确？](#card-27) |
| 28 | 技术问答 | [比较 FP8 E5M2 和 FP16 的表示精度：前者为 1 位符号、5 位指数、2 位显式小数，后者为 1、5、10。固定同一个正规数指数区间，E5M2 相邻可表示数的间距是 FP16 的多少倍？为什么指数位数相同仍不代表精度相同？](#card-28) |
| 29 | 技术问答 | [所学 FP8 Attention 为 V 调整布局：B/H 分别是 batch/head 数，N 是 token 数，D 是特征维。从连续的 \[B,H,N,D\] 张量出发，先 permute 成 \[B,H,D,N\] 并 contiguous()，再用逆 permute 恢复 \[B,H,N,D\]。最终 shape 已恢复，为什么存储布局仍然改变？删掉中间 contiguous() 又会怎样？](#card-29) |
| 30 | 技术问答 | [验证两个 Attention 实现的反向结果时，参考实现先调用 backward(dout)，然后再运行被测实现。除了 Q/K/V 相同，还必须固定哪些输入条件？为什么保存参考梯度后要清空叶子张量的 .grad？](#card-30) |
| 31 | 技术问答 | [所学 Attention benchmark 用前向 FLOP 数乘 2.5 来估算反向工作量。这里 FLOP 指浮点运算次数，B/H/N/D 分别是 batch、head、token 和特征维。2.5 的来源是什么，它能否预测反向耗时也是前向的 2.5 倍？](#card-31) |
| 32 | 技术问答 | [在同一个 Attention head 内，所有 query 向量都相同，K/V 和 scale 固定。非 causal 时，各行 O 与 M 为什么在数学上相同？改成 causal 后，这个“所有行相同”的结论为什么不能直接沿用？M 表示每行归一化分母的 base-2 对数。](#card-32) |
| 33 | 综合口述 | [请用约 60–90 秒解释分块 Attention 前向：输入 Q/K/V 为 \[B,H,N,D\]，B/H 分别是 batch/head 数，N 是 token 数，D 是特征维度，s 为原始 scale；每个 program 负责一个 head 的 B\_M 行 Q，并逐块扫描 B\_N 行 K/V。说明它怎样从完整 Attention 公式出发，维护跨块状态并最终写出 O 和供反向使用的 M。](#card-33) |
| 34 | 综合口述 | [请用约 60–90 秒解释所学 Attention 反向的数据流：前向已经从 Q/K/V 得到 O，并保存逐 query 的归一化统计量 M；现在收到损失对 O 的梯度 dO。怎样利用保存量、计算 Delta、按块重建概率，并通过输出分工得到 dQ/dK/dV？](#card-34) |

<a id="card-01"></a>

## 01. 在一个 attention head 内，Q、K、V 都是形状为 \[N,D\] 的张量，分别表示 N 个 token 的 query、key 和 value；s 是给定的点积分数缩放系数。暂不考虑分块，如何由它们计算输出 O？说明各阶段的作用和结果形状。

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：先让每个 query 与所有 key 计算匹配分数，再把该行分数归一化为权重，最后用这些权重汇总 value。

- **匹配分数**：S=sQKᵀ 的形状为 \[N,N\]。S\[i,j\] 是 query i 与 key j 的缩放点积；它此时还没有取指数，也不是概率。
- **归一化**：沿 S 的每一行，也就是 key 轴做 softmax，得到同形状的 P。P\[i,j\] 是 query i 分配给 value j 的权重；每个有效行的权重和为 1。
- **输出**：O=PV 的形状为 \[N,D\]。O\[i,:\] 是第 i 个 query 对所有有效 value 向量的加权和，仍保留 D 个特征。

$$
S=sQK^{\mathsf T},\qquad P=\operatorname{softmax}_{\mathrm{key}}(S),\qquad O=PV
$$

**边界**：causal 模式只允许 key 索引 j≤query 索引 i，包含自身；无效位置不参与归一化。这里的 Q/K/V 已由调用方生成，前面的线性投影和后面的多头输出投影都不属于此算子。

### 锚点

分数 → 沿 key 归一化 → 加权 V

### 来源

Attention 学习记录 09-24 · 分数 → 沿 key 归一化 → 加权 V

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-02"></a>

## 02. 普通 Attention 会把 N 个 query 对 N 个 key 的分数矩阵 S，以及 softmax 概率矩阵 P，写入全局显存。FlashAttention 改为按块计算时，主要避免了什么开销？QKᵀ 和 PV 的计算量是否也因此消失？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：主要省去完整 N×N 中间矩阵的物化及其显存读写；QKᵀ 和 PV 的主要计算仍然需要完成。

- **普通路径**：先写出完整 S，再读取它求 softmax 并写出 P，最后读取 P 与 V 相乘，会产生大量中间数据的存储和搬运。
- **分块路径**：固定一个 Q 块，逐块读取 K/V；分数和指数权重只作为当前块的临时量，旧块的影响由少量逐行统计量及输出累加器保留。
- **计算边界**：仍需对相关 query–key 对计算分数，并把权重作用到 V。对完整非因果注意力，主要矩阵乘工作量仍随 N²D 增长。

**边界**：减少显存流量是优化机制，不是固定倍数的加速承诺。实际耗时还与 GPU、输入形状、分块及实现有关。

### 锚点

不物化 N×N；仍计算 QKᵀ、PV

### 来源

Attention 学习记录 09-19 · 不物化 N×N；仍计算 QKᵀ、PV

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-03"></a>

## 03. 在所学 FP16 Attention 前向中，输入 Q/K/V 的形状是 \[B,H,N,D\]：B 为 batch 数、H 为 head 数、N 为 token 数、D 为每个 head 的特征维。BLOCK\_M 是一个 Q tile 的行数。grid=(ceil(N/BLOCK\_M),B×H,1) 怎样把计算和最终输出分给各 program？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：每个 program 固定一个 batch/head 和一个 Q 行块，扫描这个行块需要的 K/V，最终独占写回对应的 O 行块及 M 行统计量。

- **第0轴**：program\_id(0) 选择 Q tile。编号为 p 的 tile 对应 head 内从 p×BLOCK\_M 开始的 query 行。
- **第1轴**：program\_id(1) 选择合并后的 batch/head 编号 g；可由 b=g//H、h=g%H 还原到具体输入切片。
- **内部循环**：K/V 的分块扫描在同一个 program 内完成。扫描多少轮与启动多少个 program 是不同概念；这个前向不是每个 Q×K 块都启动一个独立 program。
- **第2轴**：尾部 1 表示第三轴只有一个位置。本实现没有使用该轴，把 grid 写成前两维即可表达相同分工。

**边界**：grid 轴的业务含义来自 kernel 如何使用 program\_id。它们不是 Triton 预先规定的 query、batch、head 轴。

### 锚点

Q tile × batch/head；K/V 在内部扫描

### 来源

Attention 学习记录 09-24 · 所学源码快照 · Q tile × batch/head；K/V 在内部扫描

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-04"></a>

## 04. 连续 FP16 Q/K/V 原本形状为 \[B,H,N,D\]，B/H 分别为 batch/head 数，N 为 token 数，D 为特征维。现在 descriptor 将 batch、head、token 合并成 \[BHN,D\] 的二维视图。已知 batch=b、head=h、head 内 token=t，这个 token 在 descriptor 中的全局行号怎样计算？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：先求当前 batch/head 的序列起点，再加上该 head 内的 token 索引。

$$
g=bH+h,\qquad r=gN+t
$$

- **各量含义**：g 是合并后的 batch/head 编号，每个 g 占连续 N 行；因此 gN 是该 head 的首行，t 才是它内部的局部偏移。特征坐标 d 不参与这一步行号计算。
- **例子**：若 g=5、N=8，head 内 token 2、3 应读 descriptor 全局行 42、43。只写行号 2、3 会访问整个视图开头的 head。
- **用到哪里**：Q tile 起点和 K/V 的每轮扫描起点都需要加当前 head 基址。判断 causal 的先后关系时，也要保证两个 token 坐标使用同一坐标系。

**边界**：这是 FP16 的普通 \[BHN,D\] 视图；FP8 V 的重排 descriptor 使用另一组轴，不能直接套用这套行号公式。

### 锚点

先 gN，再加局部 token

### 来源

Attention 学习记录 09-19／09-24 · 所学源码快照 · 先 gN，再加局部 token

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 5 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-05"></a>

## 05. 分块 Attention 前向中，一个 Q tile 有 B\_M 个 query；本轮 K/V tile 有 B\_N 个 key/value；每个 value 有 D 个特征。指数权重块的形状是 \[B\_M,B\_N\]。累加加权 V 的 acc 应是什么形状，为什么不能因 B\_M 恰好等于 D 就把它理解成 \[B\_M,B\_M\]？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：acc 的形状是 \[B\_M,D\]：每个 query 保留一个 D 维加权 value 向量。

$$
\underbrace{p}_{B_M\times B_N}\ \underbrace{V}_{B_N\times D}\ \longrightarrow\ \underbrace{acc}_{B_M\times D}
$$

- **归约轴**：乘加时对本轮的 key/value 索引求和，B\_N 这一轴被归约；保留下来的是 query 轴 B\_M 和 value 特征轴 D。下一轮 K/V 继续加到同一个 acc。
- **逐行统计**：运行最大值 m、指数和 l、重标定系数 alpha 都是一 query 一个值，所以形状为 \[B\_M\]。给 acc 重标定时用 alpha\[:,None\] 沿 D 轴广播。

**边界**：B\_M=64、D=64 只是数值偶合，不能改变轴的含义。换成 B\_M=32、D=64 时，acc 仍然是 \[32,64\]。

### 锚点

消去 key；留下 query × feature

### 来源

Attention 学习记录 09-24 · 消去 key；留下 query × feature

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 6 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-06"></a>

## 06. 在 Attention 在线 softmax 的手算中，score 已乘原始 sm\_scale，但尚未除以 ln2，也没有取 exp 或 exp2。旧、新运行最大分数分别为 −15 和 −13，而 kernel 使用 exp2。旧状态应乘什么重标定系数？为什么不能直接写 2^(−2)？

类型：真实纠错 · 层级：原子 · 等级：A

### 场景

A4 变式使用自然指数形式 softmax 的分数；要把已经积累的分母和加权 V 分子换到新的最大值基准。此前题目“自然指数 score”的措辞曾使表示域不够明确。

### 正确

系数为 exp(−15−(−13))=e^(−2)。使用 exp2 时必须先把分数差除以 ln2，即 2^(−2/ln2)。

### 错误

那么重标定系数为2^(-2)

### 说明

**结论**：exp2 的输入与自然指数 exp 的输入不是同一标度；先确定 score 是否已完成换底，再计算系数。

- **定义**：令 s\_j 表示已乘原始 sm\_scale 的点积分数，x\_j=s\_j/ln2 表示供 exp2 使用的分数。两者均尚未取指数。

$$
e^{s_j}=2^{x_j},\quad x_j=s_j/\ln2,\qquad \alpha=2^{x_{old}-x_{new}}=e^{s_{old}-s_{new}}
$$

- **代入**：这里自然分数差为 −2，因此 alpha=e⁻²。把 −2 直接交给 exp2 相当于跳过换底，得到的 1/4 不是相同权重基准。
- **用于状态**：旧分母 l 与旧加权 V 分子 acc 都乘同一个 alpha。原答关于二者都需要重标定的判断正确，需要修正的是这个系数。

**边界**：题目必须注明给出的分数处于哪个表示域。后来把自然分数改为从 1 到 4，你独立得到 e⁻³，说明已区分原始 sm\_scale 与 kernel 内融合换底后的缩放。

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-06-fused-attention-correction.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-07"></a>

## 07. 固定一个 query，Attention 前向已经扫描过若干 K/V 块，并保存运行最大值 m、指数和 l、加权 V 分子 acc。新 key 块 J 的分数 x\_j 已换到 exp2 的输入域，但尚未取指数。怎样把这个新块并入旧状态，最终得到该 query 的输出？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：先选择旧块与新块共同使用的最大值基准，再同步缩放旧分母和旧分子，加入新块贡献。

- **旧状态含义**：旧 l 是此前各 key 的 2^(x\_j−m) 之和；旧 acc 是这些权重乘 V\_j 后的向量和。acc 保存着旧 value 对输出的贡献，不能只留下 m 和 l。

$$
m'=\max\bigl(m,\max_{j\in J}x_j\bigr),\qquad \alpha=2^{m-m'},\qquad p_j=2^{x_j-m'}
$$

$$
l'=\alpha l+\sum_{j\in J}p_j,\qquad acc'=\alpha acc+\sum_{j\in J}p_jV_j
$$

- **为何共同缩放**：旧权重原先减的是 m，现在必须改成减 m′，每一项都恰好多乘 2^(m−m′)。分母和加权分子使用同一批权重，所以必须一起缩放；若最大值不变，alpha=1。
- **最终输出**：扫描完所有有效 K/V 后，O=acc/l，其中 acc 是 D 维分子，l 是标量分母。对一个 Q tile 同时做这些操作时，每一行独立维护状态，Q tile 在整个扫描中保持不变。

**边界**：p\_j 在这里是当前最大值基准下的未归一化指数权重；它不是已经除以整行分母的概率 P\_j。

### 锚点

新最大值 → 同缩放 → 合并 → acc/l

### 来源

Attention 学习记录 09-19／09-24 · 新最大值 → 同缩放 → 合并 → acc/l

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 7 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-08"></a>

## 08. 所学 Attention 前向将每个 query 的在线状态初始化为 m=−∞、l=1、acc=0。其中 m 是 exp2 输入域分数的运行最大值。假设首块至少有一个有效 key，且所有有效 score 都有限（无效位置可被 mask 为 −∞），为什么初始 l=1 不会使 softmax 分母多出 1？改成 l=0 是否也可行？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：首块使新最大值变为有限数，因此重标定系数为 0，初始 l 的有限值会被消去；在这些条件下，l 初始为 0 或 1 都可行。

- **符号**：令 x\_j 表示尚未取指数、已换底为 exp2 标度的有效 key 分数，m\_new 是加入首块后的有限最大值；l₀ 是初始的有限分母状态。

$$
\alpha=2^{-\infty-m_{new}}=0,\qquad l_{new}=\alpha l_0+\sum_j2^{x_j-m_{new}}
$$

- **为什么选m很关键**：这里能消去初值，依赖于 m 的初始值是 −∞。如果误把 m 初始化为 0，而首块所有分数都小于 0，新最大值可能仍是 0，alpha=1，初始 l=1 就会残留。
- **异常值边界**：l=1 并不能修复 inf−inf 产生的 NaN；首块全无效或包含异常无穷值时，必须另行定义和处理数值语义。NaN 也不会因为乘 0 自动消失。

**边界**：代码行为能解释这种初始化在合法输入下成立，但没有足够证据据此断言作者选择 1 是为了防止某种异常。

### 锚点

有限首块 → alpha=0 → 初始 l 消失

### 来源

Attention 学习记录 09-24 · 有限首块 → alpha=0 → 初始 l 消失

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 8 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-09"></a>

## 09. 在 causal Attention 前向中，一个 program 负责 head 内 query 区间 \[a,b)。causal 规则是 query i 只能读取 key j≤i。为了减少逐元素 mask，这个 program 应怎样划分要扫描的 key 区域？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：把 key 分成过去区 \[0,a)、对角区 \[a,b) 和未来区 \[b,N)：过去区全有效，对角区逐元素检查，未来区跳过。

- **过去区**：对任意 i∈\[a,b)，若 j&lt;a，则 j≤i 恒成立，所以这部分 K/V 块可以直接参与计算。
- **对角区**：query 与 key 都在 \[a,b) 内时，有些 key 仍在当前 query 之后，必须按 j≤i 加 mask；当前位置自身也有效。
- **未来区**：若 j≥b，则它对整个 Q tile 都在未来，没有有效贡献，可以不扫描。
- **状态接续**：过去区和对角区属于同一批 query，必须接续同一个 m/l/acc。第一个 Q tile 的 a=0，过去区为空，实际处理直接从对角区开始。

**边界**：这里描述逻辑 token 区间。实际 tile 步长、尾块和整除条件仍需保证循环没有跨过应访问的范围。

### 锚点

过去／对角／未来

### 来源

Attention 学习记录 09-24 · 过去／对角／未来

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 9 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-10"></a>

## 10. Attention 前向采用 exp2，令 x\_j=S\_j/ln2，其中 S\_j 是已乘原始 scale 的点积分数。它为一行有效 key 保存 m=max(x\_j)、l=Σ2^(x\_j−m)，并只把 M=m+log₂(l) 留给反向。为什么反向用 2^(x\_j−M) 就能恢复概率，且没有丢掉减最大值的稳定化效果？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：M 是整行原始指数和的 log₂；减去 M 同时完成了减最大值和除以归一化分母。

$$
M=m+\log_2l=\log_2\sum_j2^{x_j}
$$

$$
P_j=2^{x_j-M}=\frac{2^{x_j-m}}{l}
$$

- **加回m的作用**：l 是减最大值后得到的指数和，比原始指数和少了因子 2^m。只保存 log₂(l) 会遗漏这个因子；加上 m 才恢复完整分母的对数。
- **稳定性**：对一行有限有效 score，最大值对应的指数项为 1，所以 l≥1，进而 M≥m≥x\_j。恢复有效概率时指数不大于 0，不会出现指数上溢。

**边界**：这个结论限定在有效位置以及前后向使用一致分数的数学运算；全屏蔽行、非有限输入需要单独处理，浮点也仍可能舍入或下溢。M 是 log-sum-exp，不能再把它误认成行最大值 m。

### 锚点

先稳定求和；再保存 log 分母

### 来源

Attention 学习记录 09-19／09-24 · 先稳定求和；再保存 log 分母

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 10 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-11"></a>

## 11. 在所学 FP16 Attention 前向实现中，Q/K/V 以 FP16 存储，输出 O 也需要返回 FP16。沿 QKᵀ、softmax 在线统计、pV 到 O/M 写回这条路径，各阶段使用什么精度，关键转换发生在哪里？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：矩阵乘用低精度操作数配合 FP32 累加，归一化与在线状态保留 FP32；中途 pV 前和最终 O 写回前都会发生降精度转换。

- **QKᵀ与score**：Q 和 K 是 FP16 操作数，点积累加结果为 FP32。后续缩放、最大值、减最大值和指数权重计算使用 FP32，保护归约和指数相关的数值计算。
- **在线状态**：每个 query 的最大值 m、指数和 l，以及 D 维输出分子 acc 都保留 FP32，使跨多个 K/V 块的合并不必每轮舍入到 FP16。
- **pV之前**：p 表示当前块的未归一化指数权重。先用 FP32 p 求分母增量，再把 p 转为 FP16，与 FP16 V 相乘；乘积继续累计到 FP32 acc。
- **输出**：最后 acc/l 得到归一化输出，O 写回时转成 FP16；供反向重建概率的 M=m+log₂l 仍以 FP32 保存。

**边界**：这是该实现的精度安排。调用者看到的输入或输出 dtype，不能代表每一步内部运算精度；也不能概括成“只有最终 O 才转换精度”。

### 锚点

低精度乘法输入；高精度统计与累加

### 来源

Attention 学习记录 09-24 · 所学源码快照 · 低精度乘法输入；高精度统计与累加

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 11 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-12"></a>

## 12. Attention 前向中，p 是 FP32 的未归一化指数权重块，l 要累加每行的 sum(p)；另一路会把 p 转成 FP16 后与 FP16 V 做矩阵乘。如果把 sum(p) 移到 p 转 FP16 之后，即使仍用 FP32 累加，能保证分母结果不变吗？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：不能保证。FP16 转换已经改变了参与求和的权重，FP32 累加只能更准确地累加这些舍入后的值。

- **原顺序**：先对尚未降精度的 FP32 权重求行和，用于更新 l；然后仅为 pV 的矩阵乘把 p 转成 FP16。分母因此保留了转换前的权重信息。
- **交换后**：若先转换，传给求和的是 round\_fp16(p)，而不是原始 p。即使累加器是 FP32，也无法知道每个元素在转换中丢失了多少低位。
- **误差位置**：高精度累加主要减少累加过程引入的误差，不能撤销累加开始前已经发生的输入量化误差。这就是要分别考虑操作数和累加器精度的原因。

**边界**：并非每组输入都会产生可见差异，例如恰好能被 FP16 精确表示的权重可能一致；但两个顺序不是普遍数值等价的改写。

### 锚点

先保住输入信息，再谈累加精度

### 来源

Attention 学习记录 09-24 · 先保住输入信息，再谈累加精度

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 12 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-13"></a>

## 13. 阅读或设计一个新的深度学习算子时，输入和输出可能使用 FP16，但内部还有矩阵乘、长归约或指数运算。应怎样决定各阶段的精度，而不是凭输入 dtype 猜测全部内部计算类型？

类型：技术问答 · 层级：机制 · 等级：B

### 答案

**结论**：先确定允许的数值误差和输入范围，再把精度用在误差容易累积或放大的环节，最后用实验核对数值与成本。

- **数值要求**：了解输入可能的大小、动态范围以及输出可接受的误差。有限表示范围可能造成溢出或下溢；有限有效位数可能使舍入误差累积。
- **分开选择**：分别判断存储 dtype、实际操作数 dtype、累加器 dtype 和输出 dtype。它们可以不同，例如低精度矩阵乘操作数与高精度累加器配合。
- **转换位置**：长归约、指数和归一化通常值得单独检查。明确在哪里升精度、在哪里允许降精度；高精度累加无法弥补早先已经丢失的输入信息。
- **验证**：先对照可信参考验证正常与边界输入的误差，再测实际速度和存储收益。只有同时满足所需准确性与成本目标，精度配置才有依据。

**边界**：通用的是这套判断方法，不是一套所有算子都适用的 dtype 配方。单凭“输出为 FP16”或“文档没有特别说明”，都不能推断内部始终是 FP16 或 FP32。

### 锚点

数值要求 → 敏感环节 → 转换位置 → 验证

### 来源

Attention 学习记录 09-24 · 数值要求 → 敏感环节 → 转换位置 → 验证

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 13 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-14"></a>

## 14. 在所学 PyTorch/Triton Attention 的前后向流程中，哪些量是在前向结束时保存给反向使用的，哪些是在反向中临时计算的，哪些才是最终输出的梯度？请按产生时间和用途区分。

类型：真实纠错 · 层级：原子 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 场景

前向已用 Q/K/V 计算 O，随后损失函数会提供上游梯度 dO。需要梳理自动求导上下文保存的输入，与反向运算新产生的中间量和输出。

### 正确

前向保存 Q/K/V/O/M；反向用 O、dO 生成 Delta 并按块重建 score/P；最终输出 dQ/dK/dV。

### 错误

backward保存dQ、dK和dV，重新计算了P

### 说明

**结论**：前向保存量是反向开始前已有的依据；Delta 和概率块是反向过程中的计算材料；dQ/dK/dV 则要到反向完成后才产生。

- **前向保存**：Q/K/V 是原输入，O 是前向输出，M 是每个 query 的 base-2 log-sum-exp。官方 wrapper 把这些量交给 ctx，以便之后求输入梯度。
- **反向临时量**：损失传来 dO 后，预处理先计算逐 query 的 Delta=sum\_d(O\*dO)。主反向利用 Q/K 和 M 按 tile 恢复概率 P，而非读取一张前向保存的完整 P。
- **最终梯度**：dQ、dK、dV 分别描述损失对三个输入张量的导数。它们是反向的结果，不能列为前向就已保存的数据。

**边界**：这是本课官方实现的保存策略。其他 Attention 实现可能选择不同的保存/重算取舍；分类时仍按每个量何时产生、由谁消费来判断。

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-06-fused-attention-correction.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-15"></a>

## 15. 阅读所学 Attention 源码时，会看到前向 kernel 内多次调用 \_attn\_fwd\_inner，也会看到反向先启动 preprocess、再启动主 backward。它们分别怎样传递计算状态？为什么不能把每个 @triton.jit 函数调用都当成独立的 kernel launch？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：前向 inner 调用在同一个 kernel/program 内接续局部在线状态；反向的两个独立 Triton launch 则通过全局 Delta 缓冲区传递数据。

- **前向helper**：\_attn\_fwd\_inner 是 JIT 辅助函数。它更新当前 Q tile 的 m、l、acc，并返回新状态；外层必须按返回顺序重新绑定变量，后续区域才能继续之前的累加。
- **前向出错方式**：只调用 helper 却不接收返回值，不能指望 helper 内的重新赋值自动更新外层局部变量。causal 的过去区和对角区就可能失去状态接续。
- **反向launch**：\_attn\_bwd\_preprocess 用 O 和 dO 计算 Delta，并写入全局缓冲区；随后主反向读取它，以及 Q、预缩放 K、V、M、dO，生成输入梯度。

**边界**：反向 wrapper 还包含 K 的预缩放等操作。因此“两次 Triton kernel 启动”只是在描述这两个显式 launch，不代表整个反向恰好只有两项 GPU 操作。

### 锚点

局部返回状态；全局传递 Delta

### 来源

Attention 学习记录 09-24 · 所学源码快照 · 局部返回状态；全局传递 Delta

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 14 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-16"></a>

## 16. Attention 反向预处理拿到前向输出 O 和上游梯度 dO，两者都是 \[B,H,N,D\]：N 是 query 数，D 是每个输出向量的特征数。为了得到每个 query 一个 Delta，实际应沿哪一维求和？它与沿 key 求和的公式有什么关系？

类型：真实纠错 · 层级：原子 · 等级：A

### 场景

要为 softmax 反向准备逐 query 的标量统计量。这里 i 标识 query，j 标识 key，d 标识输出特征，三个索引代表不同的归约方向。

### 正确

实际预处理沿特征 d 求和：Delta\_i=Σ\_d O\_id\*dO\_id，结果为 \[B,H,N\]。它等于 Σ\_j P\_ij\*dP\_ij，但两式的归约轴不同。

### 错误

delta=OdO对j求和

### 说明

**结论**：对同一个 query，O\[i,:\] 和 dO\[i,:\] 都是 D 维向量；做这两个向量的点积，才得到该 query 的 Delta。

- **概率与梯度**：P\_ij 是 query i 对 key j 的 softmax 概率，dP\_ij 是损失对该概率的梯度；它们都用 query×key 两个轴索引。

$$
\Delta_i=\sum_d O_{id}\,dO_{id}=\sum_j P_{ij}\,dP_{ij}
$$

- **恒等式来源**：由 O\_id=Σ\_j P\_ij V\_jd 和 dP\_ij=Σ\_d dO\_id V\_jd，交换有限求和顺序，就得到两个表达式相等。
- **实现意义**：右边需要该 query 对所有 key 的 P/dP；左边只需已经保存的 O 和传入的 dO，所以预处理不必为计算 Delta 再物化整行概率。
- **反向用途**：之后每个 query 的 Delta 可以在扫描多个 key 块时复用，用在 dS\_ij=P\_ij(dP\_ij−Delta\_i) 中。

**边界**：实际代码中的 O\*dO 归约轴是特征 D。不能因为等价式右边对 key j 求和，就把左边也说成“对 j 求和”。

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)

**表格定位：** [真实纠错 XLSX](../triton-lesson-06-fused-attention-correction.xlsx)，第 4 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-17"></a>

## 17. 对一个 head，前向为 S=sQKᵀ、P=softmax\_key(S)、O=PV；s 是固定缩放系数，Q/K/V 为 \[N,D\]。损失传来同形状的上游梯度 dO 后，如何依次算出 dP、分数梯度以及 dQ/dK/dV？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：沿前向的相反方向：先从 O=PV 回传到 P/V，再通过每行 softmax 回传到 S，最后通过缩放点积回传到 Q/K。

- **记号**：dP 表示损失对概率 P 的梯度；令 G=∂L/∂S，避免把“对自然分数 S 的梯度”与某种源码临时变量混淆。S、P、dP、G 都是 \[N,N\]。

$$
dP=dOV^{\mathsf T},\qquad dV=P^{\mathsf T}dO
$$

$$
\Delta_i=\sum_jP_{ij}dP_{ij},\qquad G_{ij}=P_{ij}(dP_{ij}-\Delta_i)
$$

$$
dQ=sGK,\qquad dK=sG^{\mathsf T}Q
$$

- **形状与分块**：dQ/dK/dV 都回到 \[N,D\]。实现可以在需要时按块用 Q/K 和保存的 M 重建 P，再累计这些公式对应的梯度，无需保存完整 N×N 概率。

**边界**：causal 模式中，无效 query–key 位置的 P 和 G 均不贡献梯度。这里求的是对 Q/K/V 的梯度，假设 s 固定。

### 锚点

O → P/V → S → Q/K

### 来源

Attention 学习记录 09-24 · O → P/V → S → Q/K

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 15 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-18"></a>

## 18. Attention 反向重建一个概率 tile 时，M 和 Delta 都是“每个 query 一个值”的统计量。如果概率 tile 有时按 \[Bq,Bk\]（query×key）存放，有时按 \[Bk,Bq\]（key×query）存放，这两个向量应怎样广播才能对应到正确 query？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：先找出概率 tile 的 query 轴，让每个统计量保持与对应 query 的绑定，再沿 key 轴复制。

- **query在行**：对于 \[Bq,Bk\]，M 与 Delta 的形状都是 \[Bq\]。用 M\[:,None\]、Delta\[:,None\] 得到 \[Bq,1\]，向同一 query 的各个 key 列广播。
- **query在列**：对于 \[Bk,Bq\]，query 是第二轴。用 M\[None,:\]、Delta\[None,:\] 得到 \[1,Bq\]，向各个 key 行广播。
- **为什么会不同**：所学 dQ 路径固定 Q 并扫描 K/V，使用 query×key 布局；dK/dV 路径固定 K/V 扫描 Q，使用转置的 key×query 布局。

**边界**：不能按变量名照抄另一路的 \[:,None\] 或 \[None,:\]。M 用来恢复概率，Delta 用来计算 softmax 梯度，但它们都必须跟随 query 轴。

### 锚点

统计量属于 query；广播跨 key

### 来源

Attention 学习记录 09-24 · 统计量属于 query；广播跨 key

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 16 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-19"></a>

## 19. 分块计算 Attention 的 dK/dV 时，同一个 key 会接收多个 query 的梯度贡献。什么样的 program 分工可以在写回这些梯度时不用 atomic？如果把同一输出块的贡献拆给两个 program，为什么普通 store 不够？

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

Attention 学习记录 09-19／09-24 · 完整归约 + 独占输出

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 17 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-20"></a>

## 20. causal Attention 规定 query i 只能使用 key j≤i。反向计算时，固定一个 query 来求 dQ，与固定一个 key 来求 dK/dV，分别要汇总哪一侧 token 的贡献？为什么扫描方向看起来相反？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：它们来自同一个因果约束，只是固定的索引不同：固定 i 时取 j≤i，固定 j 时取 i≥j。

- **dQ的归约**：求 query i 的 dQ，需要汇总它看得到的 key，所以扫描该位置及此前的 key：0≤j≤i。未来 key 从未参与其前向输出，没有对应贡献。
- **dK/dV的归约**：求 key/value j 的梯度，需要找到所有用过它的 query；这些 query 位于 j 及之后，即 j≤i&lt;N。更早的 query 看不到这个未来 key。
- **分块时**：固定 query tile 通常扫描过去 key 区和对角区；固定 key tile 则扫描对角 query 区和后续区。对角块内部还要按逐元素 i/j 关系加 mask。

**边界**：两种范围都包含当前位置自身。不要把前向的“query 看过去 key”机械改写成“key 的梯度也只看过去 query”。

### 锚点

dQ 看过去 key；dK/dV 看后续 query

### 来源

Attention 学习记录 09-19 · dQ 看过去 key；dK/dV 看后续 query

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 18 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-21"></a>

## 21. 所学 Attention 反向先把 K 预缩放为 K̃=(s/ln2)K。令 G=P⊙(dP−Delta) 表示损失对自然分数 S=sQKᵀ 的梯度。为什么 dQ 路径用 K̃ 累加后要乘 ln2，而 dK 路径用原始 Q 累加后要乘 s？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：末尾系数是在补回各路径尚缺或多带的缩放；两条路径输入中的 scale 并不相同。

- **dQ路径**：数学目标是 dQ=sGK。使用预缩放 K̃ 后，临时结果为 GK̃=(s/ln2)GK，已含 s，却多了 1/ln2，因此最后乘 ln2。
- **dK路径**：数学目标是 dK=sGᵀQ。该路径使用原始 Q 得到 GᵀQ，尚未包含 s，所以在写回前乘 s。

$$
(G\widetilde K)\ln2=sGK=dQ,\qquad s(G^{\mathsf T}Q)=dK
$$

- **常见遗漏**：如果漏掉 dQ 的末尾 ln2，结果会是正确 dQ 的 1/ln2 倍。dV=PᵀdO 则没有上述点积分数缩放，不需要这两项系数。

**边界**：必须追踪这个版本 wrapper 与 kernel 实际使用的张量。这里的 G 是对自然分数 S 的梯度；若另一实现选择不同表示域或预缩放位置，不能照搬末尾系数。

### 锚点

追踪预缩放；不要机械套同一系数

### 来源

Attention 学习记录 09-24 · 所学源码快照 · 追踪预缩放；不要机械套同一系数

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 19 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-22"></a>

## 22. 使用 Triton TensorDescriptor 按块读取张量时，base、shape、strides、block\_shape 和 load(offsets) 分别决定什么？例如 B/H/N/D 分别表示 batch 数、head 数、token 数和特征维，Q 被展平成 \[BHN,D\]，每次取 BLOCK\_M 个 query。此时 block\_shape=\[BLOCK\_M,D\]，load(\[r0,0\]) 会读取哪个块？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：descriptor 给出全局存储视图与每次访问块的形状；load 的 offsets 再指定这一次从视图中的哪个坐标开始。

- **base与shape**：base 是已有张量存储的首地址；shape=\[BHN,D\] 声明一个有 BHN 行、D 列的访问视图。创建 descriptor 只是建立访问描述，不会提前读取整个张量。
- **strides**：strides 表示某一维索引增加 1 时跨过多少个元素，而不是字节。连续二维视图通常为 \[D,1\]；换算实际字节偏移还要乘元素字节数。
- **block\_shape**：\[BLOCK\_M,D\] 指定每次 load 返回 BLOCK\_M 行、D 列的 tile。这是读取结果的局部形状，与整体视图大小不同。
- **本次起点**：load(\[r0,0\]) 从第 r0 行、第 0 列开始取该形状的块。若把起点改为 \[r0+BLOCK\_M,0\]，就向下移动一个 Q tile；返回形状仍为 \[BLOCK\_M,D\]。

**边界**：offsets 是每次 load 的参数，不是创建 descriptor 时固定的块起点。以上访问仍须满足该接口的布局、对齐和边界要求；本卡以 Triton 3.7.1 为准。

### 锚点

布局由描述给出；大小看 block\_shape；位置看 offsets

### 来源

Attention 学习记录 09-24 · Triton 3.7.1 · 布局由描述给出；大小看 block\_shape；位置看 offsets

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 20 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-23"></a>

## 23. Attention 的 Q/K/V descriptor 把多个 batch/head 展平成 \[BHN,D\]，每个 head 占 N 行。若一次 load 跨过当前 head 的末尾，却仍在整个 BHN 行视图之内，descriptor 会自动将越过这个 head 的位置补零吗？

类型：技术问答 · 层级：原子 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：不会。descriptor 只判断坐标是否越过声明的整体视图，不知道其中哪 N 行属于当前逻辑 head。

- **为何仍合法**：跨到下一 head 的行号只要仍小于 BHN，就还是 \[BHN,D\] 中的合法坐标。load 可能正常读到下一 head 的数据，而不会把它当成越界。
- **需要保证的范围**：调用方必须正确计算当前 head 的基址，并限制本 program 的 token 扫描范围；batch/head 的逻辑隔离是索引设计的一部分。
- **真正越界时**：在默认 zero padding 且访问满足其他约束的情况下，只有超出整个声明视图的元素才会补零。即使尾部有补值，返回 tile 的形状仍由 block\_shape 决定。

**边界**：自动处理内存视图越界，不等于自动实现 Attention 的 head 边界或 causal 规则；这些逻辑条件仍需由访问范围和 score mask 保证。

### 锚点

视图边界由 descriptor 管；head 范围由索引保证

### 来源

Attention 学习记录 09-24 · Triton 3.7.1 · 视图边界由 descriptor 管；head 范围由索引保证

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 21 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-24"></a>

## 24. Attention 处理不足一个 tile 的尾部 key 时，假设 descriptor 已把无效位置的 K 和 V 都补成零。能否省掉对这些 key 的 score mask，直接让 softmax 和 pV 计算整个 tile？

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：不能。零 K/V 并没有把无效 key 从 softmax 的归一化集合中删除，它仍可能改变分母。

- **零K的分数**：对有限 query，零 K 的点积为零，乘 scale 后 score 仍为零。但零分数的指数权重不是零。

$$
S_{ij}=0\quad\Longrightarrow\quad e^{S_{ij}}=1
$$

- **稳定化也不删除**：本卡用自然分数 S 说明，令 m\_S=max(S)。减去最大值后，零分数的指数项为 exp(−m\_S)，仍会计入分母；稳定化没有删除这个无效 key。若换成 exp2，则最大值也必须使用对应的换底标度。
- **零V只影响分子**：零 V 使该项在加权分子中的直接贡献为零，但它仍占据分母，可能把真实 value 的输出权重压小。

**边界**：应在 score/概率上按有效 key 条件屏蔽这些位置，使它们对归一化不贡献权重。也不能把 K/V 填成 −∞ 来代替 score mask，因为点积和乘法会产生不同的数值行为。

### 锚点

零数据不等于零概率；分母也要排除

### 来源

Attention 学习记录 09-24 · 零数据不等于零概率；分母也要排除

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 22 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-25"></a>

## 25. 在 Triton 3.7.1 中，普通 tl.load 可用 other 指定 masked 位置的替代值。若改用 TensorDescriptor 的 load，能否同样传入任意 other 值？可选的 padding 在哪里设置？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton · 3.7.1

### 答案

**结论**：descriptor 不提供任意 other 值；它在构造时选择预设的 zero 或 nan padding，默认是 zero。

- **host构造**：host 侧 TensorDescriptor 使用 padding 参数，例如 padding="zero"。这项设置属于 descriptor，而不是每次 load 时单独给出的标量。
- **device构造**：kernel 内 tl.make\_tensor\_descriptor 使用 padding\_option 参数，提供同样的预设选择。nan 仅适用于浮点数据。
- **其他替代值**：如果运算需要别的值，可以在 load 后根据有效位置条件替换，或者改用普通带 mask 和 other 的 tl.load。选择要满足所用接口的访问约束。

**边界**：Attention 的无效 key 需要的是对 score/概率的语义屏蔽；改变 K/V 的越界填充值不能直接代替 softmax mask。本卡的 API 选项限定于 Triton 3.7.1。

### 锚点

构造时选预设；不是 load 时传任意 other

### 来源

Attention 学习记录 09-24 · Triton 3.7.1 · 构造时选预设；不是 load 时传任意 other

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 23 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-26"></a>

## 26. 把一个 PyTorch 张量传给 Triton 3.7.1 的 NVIDIA TMA descriptor 前，为什么仅检查 is\_contiguous() 不够？应怎样检查实际基址与 stride 的基础对齐条件，切片视图又会带来什么问题？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 3.7.1

### 答案

**结论**：连续性描述元素的排列关系，并不保证视图首地址满足 TMA 对齐；必须检查实际地址和以字节计的步长。

- **需要的量**：设 A=tensor.data\_ptr() 为当前视图第一个元素的地址，e 为每元素字节数，s\_k 为第 k 维的元素 stride。descriptor 的 strides 参数以元素计，对齐条件则以字节计。

$$
A\bmod16=0,\qquad s_{last}=1,\qquad (s_ke)\bmod16=0\quad(k<last)
$$

- **切片反例**：一个基址对齐的一维 FP16 张量取 x\[1:\] 后，视图仍可连续，但首地址向后移动 2 字节，从而破坏 16 字节对齐。必须检查传入视图的 data\_ptr，而非原始存储的起点。
- **contiguous的限制**：如果这个视图本来就连续，contiguous() 可以直接返回它，不会为了对齐自动分配新存储。因此调用 contiguous() 不能替代地址检查。

**边界**：这里只列出本路径的基础布局条件。即使这些条件满足，也还需要核对 block\_shape、设备支持及后续矩阵乘的限制。

### 锚点

查实际首地址与字节步长；连续不保证对齐

### 来源

Attention 学习记录 09-24 · Triton 3.7.1 · 查实际首地址与字节步长；连续不保证对齐

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 24 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-27"></a>

## 27. 所学 Attention 的普通 FP16 路径中，D 表示每个 head 的特征维度。wrapper 在 host 侧先用 dummy\_block 创建 TensorDescriptor，而 autotune 会尝试不同 BLOCK\_M/BLOCK\_N。为什么每次配置运行前必须由 pre-hook 更新 block\_shape，不能指望 kernel 中的 \_maybe\_make\_tensor\_desc 自动改正确？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：host 传入的已经是 descriptor，helper 会原样返回它；因此进入 kernel 前，它的块大小就必须与当前配置一致。

- **占位阶段**：dummy\_block 只是构造 descriptor 时的占位形状。实际一轮候选可能选择不同的 Q tile 行数 BLOCK\_M 和 K/V tile 行数 BLOCK\_N。
- **pre-hook的职责**：运行每个候选前，把 Q/O descriptor 的 block\_shape 改为 \[BLOCK\_M,D\]，K/V 改为 \[BLOCK\_N,D\]，使 load/store 的实际形状匹配该候选。
- **helper两条路径**：收到普通指针时，helper 才使用 shape、strides、block\_shape 构造 descriptor；收到已有 descriptor 时直接返回，额外传入的 block\_shape 不会覆盖对象。

**边界**：pre-hook、grid 和 kernel 内计算形状必须使用同一候选配置。这个问题来自所学教程的 host descriptor 调用方式，不能假设所有 descriptor 都必须采用 dummy\_block。

### 锚点

当前配置 → 更新 descriptor → 原样传入 kernel

### 来源

Attention 学习记录 09-24 · 所学源码快照 · 当前配置 → 更新 descriptor → 原样传入 kernel

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 25 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-28"></a>

## 28. 比较 FP8 E5M2 和 FP16 的表示精度：前者为 1 位符号、5 位指数、2 位显式小数，后者为 1、5、10。固定同一个正规数指数区间，E5M2 相邻可表示数的间距是 FP16 的多少倍？为什么指数位数相同仍不代表精度相同？

类型：技术问答 · 层级：原子 · 等级：A

### 答案

**结论**：E5M2 的相邻间距是 FP16 的 256 倍；相同指数位数没有补回少掉的小数位。

- **正规数模型**：在固定指数 e 的正规区间中，数值可写成符号×2^e×(1+f/2^p)，p 是显式小数位数。f 每增加 1，相邻数就相差 2^(e−p)。

$$
\frac{2^{e-2}}{2^{e-10}}=2^8=256
$$

- **含义**：E5M2 只有 2 位显式小数，同一个区间内可表示的点更稀疏。把 FP16 数值转为它时，即使不发生范围溢出，也可能产生更大的舍入误差。

**边界**：这里比较的是同一正规指数区间的间距，不覆盖零、非正规数或特殊值。指数位数主要关联范围，小数位数影响局部表示分辨率。

### 锚点

范围看指数；精度看小数位

### 来源

Attention 学习记录 09-24 · 范围看指数；精度看小数位

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 26 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-29"></a>

## 29. 所学 FP8 Attention 为 V 调整布局：B/H 分别是 batch/head 数，N 是 token 数，D 是特征维。从连续的 \[B,H,N,D\] 张量出发，先 permute 成 \[B,H,D,N\] 并 contiguous()，再用逆 permute 恢复 \[B,H,N,D\]。最终 shape 已恢复，为什么存储布局仍然改变？删掉中间 contiguous() 又会怎样？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：中间 contiguous() 按转置后的轴顺序复制了数据；逆 permute 只恢复逻辑轴顺序，不会把这次复制后的存储重新排列回去。

- **原布局**：连续 \[B,H,N,D\] 的末两维 stride 是 \[D,1\]，同一个 token 的 D 个特征相邻。令 g=bH+h，则元素 (g,n,d) 的线性偏移为 gND+nD+d。
- **复制后**：在 \[B,H,D,N\] 下做 contiguous 后，同一个特征的 N 个 token 相邻。再恢复逻辑 shape，末两维 stride 变成 \[1,N\]，元素偏移为 gND+dN+n。

$$
gND+nD+d\ \longrightarrow\ gND+dN+n
$$

- **删除中间复制**：仅连续做两次互逆 permute 会把 shape 和 stride 都恢复，底层存储没有搬动。对于原本连续的张量，最后再调用 contiguous 通常也无需复制。

**边界**：判断布局必须同时看 shape、stride 和是否发生实际复制。此处解释的是所学 V 重排；后续转换为 FP8 的 dtype 操作，与轴布局变化是另一件事。

### 锚点

shape 相同不保证存储布局相同

### 来源

Attention 学习记录 09-24 · 所学源码快照 · shape 相同不保证存储布局相同

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 27 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-30"></a>

## 30. 验证两个 Attention 实现的反向结果时，参考实现先调用 backward(dout)，然后再运行被测实现。除了 Q/K/V 相同，还必须固定哪些输入条件？为什么保存参考梯度后要清空叶子张量的 .grad？

类型：技术问答 · 层级：机制 · 等级：A

适用范围：pytorch/triton attention correctness test · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：两边必须对同一计算问题、同一上游梯度求导，并避免后一次 backward 把结果累加到已有梯度上。

- **同一前向问题**：Q/K/V、causal 开关与原始 scale 都要相同，否则前向函数本身就不同。
- **同一dout**：dout 即 dO，决定损失对输出各元素的加权。可把 backward(dout) 理解为对固定 dout 的标量 L=Σ(O\*dout) 求导；换一个 dout，得到的梯度通常也会变。
- **保存再清空**：先保存参考的 dQ/dK/dV，再清空对应叶子张量的 .grad。PyTorch 的 backward 会累计叶子梯度，否则第二次读到的可能是两次结果之和。

**边界**：输入条件或梯度累计状态不同，得到的差异不能直接归因于被测 kernel 错误。比较前向 O 一致，也不能替代对上游 dO 的一致性检查。

### 锚点

同 QKV、同规则、同 dO；清空累计梯度

### 来源

Attention 学习记录 09-24 · 所学源码快照 · 同 QKV、同规则、同 dO；清空累计梯度

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 28 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-31"></a>

## 31. 所学 Attention benchmark 用前向 FLOP 数乘 2.5 来估算反向工作量。这里 FLOP 指浮点运算次数，B/H/N/D 分别是 batch、head、token 和特征维。2.5 的来源是什么，它能否预测反向耗时也是前向的 2.5 倍？

类型：技术问答 · 层级：原子 · 等级：B

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 答案

**结论**：2.5 是主要矩阵乘工作量的报告模型：反向按五次、前向按两次估算，因此得到 5/2；它不是耗时预测。

- **前向口径**：QKᵀ 与 PV 各有约 BHN²D 次乘加，按一次乘加计两个 FLOP，合计约 4BHN²D。
- **反向口径**：benchmark 用五次主要矩阵乘来代表反向，相对前向两次形成 2.5 系数。它是一种统一报告口径，不是逐条核算该 kernel 执行的所有指令。
- **实际实现**：不同梯度路径还可能重复重算概率相关项，并包含归约、指数、读写等工作。causal 把工作量乘 0.5 也只是近似。

**边界**：耗时同时受数据搬运、并行度、资源与执行组织影响，必须实际测量。不能由这个系数断言反向必定慢 2.5 倍，也不能把报告 FLOP 当作精确的硬件指令数。

### 锚点

FLOP 模型 ≠ 实际指令数 ≠ 耗时

### 来源

Attention 学习记录 09-24 · 所学源码快照 · FLOP 模型 ≠ 实际指令数 ≠ 耗时

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 29 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-32"></a>

## 32. 在同一个 Attention head 内，所有 query 向量都相同，K/V 和 scale 固定。非 causal 时，各行 O 与 M 为什么在数学上相同？改成 causal 后，这个“所有行相同”的结论为什么不能直接沿用？M 表示每行归一化分母的 base-2 对数。

类型：技术问答 · 层级：机制 · 等级：A

### 答案

**结论**：相同 Q 保证对同一个 key 的分数相同；还需要每行使用同一组有效 key，才能推出相同的权重、O 和 M。

- **非causal**：每个 query 都访问完整 K/V，因此分数序列和归一化集合都相同。softmax 概率相同，加权相同的 V 后输出也相同，分母的 log₂ 即 M 同样相同。
- **causal**：第 i 行只访问 j≤i 的前缀，包含自身。即使对共同 key 的分数一样，参与归一化的集合仍随 query 位置改变，所以不能继续推断所有 O/M 行相同。
- **输出并非必然两两不同**：有效集合变化通常会使 O 变化，但特殊的 V 仍可能使某些行输出相同；例如所有 value 相同，归一化后的加权和仍可能相同。

**边界**：这里讨论同一 head、同一 scale 和一致输入下的数学关系。浮点实现会有舍入误差；不能把“通常变化”加强成“任意两行必定不同”。

### 锚点

相同 score + 相同有效集合

### 来源

Attention 学习记录 09-24 · 相同 score + 相同有效集合

**来源记录：** [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [技术问答 XLSX](../triton-lesson-06-fused-attention-technical-qa.xlsx)，第 30 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-33"></a>

## 33. 请用约 60–90 秒解释分块 Attention 前向：输入 Q/K/V 为 \[B,H,N,D\]，B/H 分别是 batch/head 数，N 是 token 数，D 是特征维度，s 为原始 scale；每个 program 负责一个 head 的 B\_M 行 Q，并逐块扫描 B\_N 行 K/V。说明它怎样从完整 Attention 公式出发，维护跨块状态并最终写出 O 和供反向使用的 M。

类型：综合口述 · 层级：口述 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 参考回答

**结论**：完整目标是缩放点积、沿 key 归一化、再加权 V；分块实现通过逐行在线状态，得到同一数学输出而不保存完整概率矩阵。

- **公式与分工**：每个 head 的计算是 S=sQKᵀ、P=softmax\_key(S)、O=PV。一个 program 固定该 head 的一个 Q tile，内部扫描所需 K/V，最后独占对应的输出行。
- **形状**：当前分数/权重块是 \[B\_M,B\_N\]，沿 key 轴归约；输出分子 acc 保留 query 与特征轴，所以是 \[B\_M,D\]。每个 query 的 m、l 都是一个标量。
- **跨块合并**：先把自然分数 S 换成 x=S/ln2，再用 exp2。m 是当前已见 x 的最大值，l=Σ2^(x−m)，acc 是同一权重下的加权 V 分子。新最大值出现时，要把旧 l 和 acc 同时重标定，再加入新块贡献。
- **最终写回**：扫描结束后 O=acc/l。采用 exp2 时保存 M=m+log₂l，即完整分母的 base-2 对数；反向重算同一表示域的 x 后，用 2^(x−M) 恢复局部归一化概率。

**边界**：必须始终区分 query、key 和特征轴，以及未归一化的局部指数权重与最终概率；每个 program 的输出所有权贯穿整个扫描。

### 评分锚点

写出带原始scale的完整公式，并指出softmax沿key轴；明确一个program固定Q tile、内部扫描K/V并独占输出；正确区分score=\[B\_M,B\_N\]与acc=\[B\_M,D\]；解释m/l/acc的含义及分子分母共同重标定；说明O=acc/l以及M在反向恢复概率中的用途

### 来源

Attention 学习记录 09-19 与 09-24 · 全流程串联

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-06-fused-attention-oral.xlsx)，第 2 行（第 1 行为表头）。

[返回题目目录](#题目目录)


<a id="card-34"></a>

## 34. 请用约 60–90 秒解释所学 Attention 反向的数据流：前向已经从 Q/K/V 得到 O，并保存逐 query 的归一化统计量 M；现在收到损失对 O 的梯度 dO。怎样利用保存量、计算 Delta、按块重建概率，并通过输出分工得到 dQ/dK/dV？

类型：综合口述 · 层级：口述 · 等级：A

适用范围：triton fused-attention tutorial · 所学源码快照（固定版本信息见卡片包）

### 参考回答

**结论**：反向用前向保存量和 dO 重新建立局部概率，再沿每种输出梯度所需的方向归约，避免物化完整的 N×N 中间矩阵。

- **保存与准备**：前向保存 Q/K/V/O/M。反向先对每个 query 沿特征维计算 Delta\_i=Σ\_d O\_id\*dO\_id，结果是一行一个标量；它等于该行 Σ\_j P\_ij\*dP\_ij。
- **恢复概率**：用 Q/K 重算自然分数 S，再换成 x=S/ln2，以 P=2^(x−M) 恢复对应概率。M 保存的是完整分母的 log₂，不能把它当成仅有行最大值。
- **反向链**：由 O=PV 得到 dP=dOVᵀ 和 dV=PᵀdO，再令 G=P⊙(dP−Delta)，即对自然分数 S=sQKᵀ 的梯度，得到 dQ=sGK、dK=sGᵀQ。这里 s 为固定的原始 scale。
- **输出所有权**：dQ 固定 query 并沿 key 汇总；dK/dV 固定 key 并沿 query 汇总。一个 program 算齐自己的输出块后独占写回，所以这种分工不需要跨 program atomic。

**边界**：前向保存量、反向临时量和最终梯度的产生时间不同。若把同一输出块的归约拆给多个 program，就必须另行合并部分贡献。

### 评分锚点

按产生时间区分前向保存量、反向临时量与最终梯度；说明Delta沿特征维求和且每query一个值；说明M重建概率而非只代替行最大值；完整说明dP、softmax分数梯度和三个输入梯度的关系；把归约方向与单program完整归约、独占写回联系起来

### 来源

Attention 学习记录 09-19 与 09-24 · 全流程串联

**来源记录：** [9/14–19：概念、在线状态、反向与真实纠错](../../logs/2026-09-19-fused-attention.md) · [9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释](../../logs/2026-09-24-fused-attention.md)

**表格定位：** [综合口述 XLSX](../triton-lesson-06-fused-attention-oral.xlsx)，第 3 行（第 1 行为表头）。

[返回题目目录](#题目目录)
