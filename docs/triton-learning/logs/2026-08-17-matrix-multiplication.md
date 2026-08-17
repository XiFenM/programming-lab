# 学习记录 · 2026-08-17 · Triton 分块矩阵乘法

> 来源：`codex:01a00da2-dead-7b20-828c-2fada0212024` ·
> `msg-64d576e25f76af98b0f6` → `msg-8bfd7edfc1f58767a089`
>
> 关联：[Lesson 03：分块矩阵乘法](../lessons/03-matrix-multiplication.md)

## 学习过程

- [要点] 从单个 output tile 建立了 blocked matmul 数据流：
  `A_tile=[BLOCK_M,BLOCK_K]`、`B_tile=[BLOCK_K,BLOCK_N]`，每轮沿 K 轴推进并累加到
  `[BLOCK_M,BLOCK_N]` 的 FP32 accumulator。
- [纠错] 学习者最初写道：“`k方向偏移为[4,5,6,7]`”。更精确的区分是：局部 `offs_k` 始终为
  `[0,1,2,3]`，第二轮是指针推进后对应全局 K 坐标 `[4,5,6,7]`；后三个 lane 因 `K=5` 被 mask。
- [高价值问题] 学习者追问：“为什么不直接也使用mask进行屏蔽呢？而要取模后取一些有效元素，取这些
  有效元素难道不会导致访存不连续吗？”结论是：M/N load 使用 mask 也能保证正确；教程的取模让无效
  输出 lane 读取合法 dummy 数据并保持固定 load/dot tile，但边界访存可能有额外成本，性能优劣需要在
  目标 GPU 上受控测量。
- [转折] 学习者进一步区分了自由维度与归约维度：M/N 的 dummy 计算只落入最终不写回的输出 lane；K
  若用 `% K` 回绕，会把重复乘积累加进有效 `C[i,j]`，因此 K 尾部必须通过 load mask 填零。
- [转折] 学习者起初表示 grouped ordering 的公式“没看懂其中逻辑”；借助 `4×3` output-tile 网格后，
  能独立给出 `pid=2 → (0,1)`、`pid=3 → (1,1)`，并识别它们立即复用同一个 B column tile。
- [要点] 在 `num_pid_m=5`、`num_pid_n=3`、`GROUP_SIZE_M=2` 的尾组中，学习者正确推导
  `pid=12,13,14 → (4,0),(4,1),(4,2)`。动态 `group_size_m=1` 可避免错误映射到 `(5,0)` 并避免遗漏
  `(4,2)`。
- [纠错] 学习者曾用“如果M和N偏大，K偏小，可能配置A更合适；如果M和N偏小，K偏大，可能配置B更合适。”
  概括 autotune 选择。补充后的模型是：
  即使 shape 已知，program 数和 K-loop 次数也不足以裁决性能，还要考虑 accumulator／寄存器占用、
  occupancy、数据复用、边界浪费、warps/stages、GPU 架构与编译结果，最终以测量为准。
- [要点] 对 `M=N=130,K=64`，学习者算出 `128×128` tile 配置启动 4 个 program、名义输出 lane
  65,536；`64×64` tile 配置启动 9 个 program、名义输出 lane 36,864；有效输出 lane 为 16,900，
  因而前者的边界无效比例更高。
- [要点] 学习者设计了三个单变量边界 shape：`(130,128,32)` 验证 M 尾部，`(128,130,32)` 验证 N
  尾部，`(128,128,40)` 验证 K 尾部。
- [纠错] 学习者最初写道：“`这里主要验证kernel中对K维边界读取和写入的mask然后other取0的逻辑。`”
  实际没有 K 维 store mask：
  `K=40,BLOCK_K=32` 时第二轮 8 个 K lane 有效、24 个 lane 由 load mask 填零；归约后 K 轴已消失，
  最终 `c_mask` 只能过滤 M/N 输出坐标，不能修复已被错误 K 值污染的 accumulator。

## 遗留

- [遗留] 四个概念节点已完成节点级检查，但跨节点综合验收尚未形成 evidence。恢复后先回答 S1：对
  `A=(257,65)`、`B=(65,129)` 和给定 block/group 参数，完整推导 grid、尾组 PID、有效 M/N/K lane
  与边界正确性。
- [遗留] S1 之后完成 S2：为 `GROUP_SIZE_M=1` 与 `2` 的比较给出可证伪预测、控制变量、测量指标和
  否证条件。
- [遗留] O3 learner-owned Triton 实现与正确性测试尚未建立正式实践契约；O4 的目标 GPU 受控实测尚未
  进行。
