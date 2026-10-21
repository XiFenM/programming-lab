# 学习记录 · 2026-08-19 · Triton 分块矩阵乘法实践与结课

> 来源：`codex:01a013fc-5b9e-7c90-8d72-c60db1662995` ·
> `msg-f1d589144c7d8a0a905f` → `msg-64f390350c7c13692051`
>
> 关联：[Lesson 03：分块矩阵乘法](../lessons/03-matrix-multiplication.md)

## 学习过程

- [纠错] 场景：为综合验收计算 output grid 与尾组数量。学习者写
  “`num_pid_m = cdiv(M // BLOCK_SIZE_M)`”和“`num_group = cdiv(num_pid_m // GROUP_SIZE_M)`”
  → 正确记号分别是 `cdiv(M, BLOCK_SIZE_M)` 与 `cdiv(num_pid_m, GROUP_SIZE_M)`。原因：`cdiv`
  本身完成向上整除，不能先用 `//` 丢掉余数；本次后续数值结果正确，错误只在公式记号。
  （来源：`msg-f1d589144c7d8a0a905f` → `msg-2dd8ca95c5eff08934ca`）
- [要点] 为什么最终 C store mask 不能修复 K 尾部的错误 load？——学习者解释：M/N 是独立输出
  坐标，dummy 计算只会落入不写回的 output lane；K 是归约维度，错误值会先累加进有效
  `C[i,j]`，到 store 时已经无法区分。因此 K 尾部必须在 load 时补零。（来源：
  `msg-f1d589144c7d8a0a905f`；课程证据 E-05）
- [转折] 学习者指出，把一次最小 grouped-ordering 对照继续扩张为由学习者设计成对批次、数值阈值
  和统计判据，已经偏离本课的编程目标。此后职责被收紧为：学习者拥有核心实现并负责事前预测与
  结果解释，Agent 负责测试、实验 harness 和最低充分的测量方法；课程随即进入测试驱动编程实践。
  （来源：`msg-00aebbfd07156a83fd36` → `msg-2b6e6caa5f37f3fb5e58`）
- [纠错] 场景：本次 Triton 3.7.1 环境中，第一版 kernel 的尾组大小计算在全部数值用例编译前失败。
  实现使用了 reduction API `tl.min` → 应使用合法的 scalar/elementwise minimum，例如本次修复采用的
  `tl.minimum`。原因：`tl.min` 的第二个位置参数被解释为 reduction axis，而这里需要比较两个标量值。
  （来源：`msg-40874887f335c2da1b3d` → `msg-00a38e9314153d8f62fe`）
- [要点] 第一版报错的原代码是 `this_group_size_m = tl.min(num_pid_m - first_pid_m, GROUP_SIZE_M)`：
  10 个数值用例都在编译阶段报 `invalid axis`，因为 `tl.min` 把第二个位置参数 `GROUP_SIZE_M` 当成
  了归约轴。Review 指出这里需要标量 minimum，可以写成 Python 内建
  `min(num_pid_m - first_pid_m, GROUP_SIZE_M)`（固定教程快照的写法）；学习者实际改用
  `tl.minimum`，复核确认它同样是合法的 elementwise/scalar minimum。（来源：
  `msg-5f08cba109dd2297a0ed` → `msg-9f2270845615af0dbdea`，对话原文 08-19 #016–#021；Lesson 记录
  F-P03-01、Material assistance）
- [要点] 尾组动态大小除了防止什么错误？——在未公开变式 `(M,K,N)=(129,71,67)` 中，学习者推导
  `pid=4,5 → (2,0),(2,1)`。若仍按完整组大小映射，`pid=5` 不仅会落到不存在的 `(3,0)`，还会遗漏
  必须计算的 `(2,1)`；因此尾组逻辑同时保证“不越界”和“不漏块”。（来源：
  `msg-75a268ba2b2cf0167bf6` → `msg-af6bd112b73e669bc015`；课程证据 E-07）
- [要点] P03-A5 最小对照的条件与读数：RTX 5090、`M=N=K=4096`，固定 `64×64×32` block、4 warps、
  3 stages 与同一输入，只改变 `GROUP_SIZE_M`；预编译后按 ABBA（`1→2→2→1`）顺序计量，median 依次为
  `0.6687`、`0.6902`、`0.6943`、`0.6975 ms`。前半程 group 1 更快，后半程 group 2 略快，group 1
  首末两次相差约 4%。（来源：`msg-b11cdbfa525e39901d49` → `msg-88c211afd98d2382361a`，对话原文
  08-19 #026–#027；课程证据 E-08）
- [纠错] 场景：解释 ABBA benchmark 的四个 median。学习者说“在当前环境和固定配置上，对性能
  影响较小”→ 当前证据只能说明：在这台 RTX 5090、该 shape、固定 launch 配置和本次方法下，
  `GROUP_SIZE_M` 的影响无法与约 4% 的运行状态漂移稳定分离。原因：证据不足不能进一步证明真实
  effect size 很小，也不能支持 group 1 或 group 2 更快。（来源：`msg-a2ead6bfb84330910ddb` →
  `msg-acdaa139a50ec0c641ef`；课程证据 E-08、E-09）
- [高价值问题] “什么场景下 grouped ordering 会有相对显著的优化效果？”——结论已核验并写入课程
  证据 E-10：关键是相邻 program 的 A/B tile 复用距离落在 L2 驻留窗口内；大型二维 tile grid、
  访存敏感且 group size 与并发窗口和 block 配置匹配时更可能获益。本次单 shape、group 1/2 与
  wrapper 计时不能裁决跨 shape、group size 或架构结论。（来源：`msg-312a5dd271976b8316cf` →
  `msg-3f4c110fbc799fe2e303`）
- [要点] grouped ordering 为什么能少加载输入 tile？——把同时活跃的一小批 program 看成输出网格中的
  一个窗口：窗口有 8 个 program 时，row-major 近似 `1×8`，约访问 1 个 A tile 行和 8 个 B tile 列；
  `GROUP_SIZE_M=2` 近似 `2×4`，约访问 2 个 A tile 行和 4 个 B tile 列，输入 tile 种类从约 `1+8=9`
  降到 `2+4=6`，因此更可能命中 L2。固定教程的 `9×9` block 示例是同一机制：计算前 9 个输出 block
  时，row-major 需要加载 90 个输入 block，grouped ordering 只需 54 个。（来源：
  `msg-3f4c110fbc799fe2e303`，对话原文 08-19 #033；课程证据 E-10）（2026-10-21 复算：A、B 各为
  9×9 个 block，一个 A tile 行或一个 B tile 列各含 9 个 block。row-major 的前 9 个输出 block 同在
  第 0 个 tile 行，需要 1 个 A tile 行和全部 9 个 B tile 列，共 9+81=90；54 对应把前 9 个输出 block
  排成 3×3，需要 3 个 A tile 行和 3 个 B tile 列，共 27+27=54。）
