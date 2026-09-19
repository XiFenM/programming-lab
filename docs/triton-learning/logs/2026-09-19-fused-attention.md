# 学习记录 · 2026-09-14—19 · Triton 06 Fused Attention

> 来源：`codex:01a084ec`，四段根会话；首段 `msg-3f7c5d6364ef13a88041`，末段
> `msg-7bb02fe072c66cc57d3e`。各段 source SHA-256 依次为
> `266fcc305f5e6880ca0966ab3402e620c2e9a979507e8092b7e71bcc48952d32`、
> `a5a8ec3727f3c0e20ba905bceeba15d0fd7e10924edfa704e6338d05f046d9e2`、
> `51d550229fe79c665130104daee8afdc0ada8c393a9e4a2a961adabca3cedff7`、
> `b18a11ea661123d09902c909229095078825d3060ca30841c7b7fe8a6f242b73`。
> 关联：[第 06 课 Lesson](../lessons/06-fused-attention.md)

## 学习过程

- [要点] FlashAttention 避免写出什么，仍要计算什么？——学习者算出单个 head、`N=4` 时
  `S/P` 合计 32 个元素，并指出不物化它们不会消除 `QKᵀ` 与 `PV` 的主要计算。
  （来源：`msg-a36cacef74ef43c24785`）

- [要点] 新 score 块把最大值从 2 提到 3 时，旧分母和输出分子怎样并入？——学习者独立写出
  `α=e^{-1}`、`l=e^{-2}+e^{-1}+1`、`acc=10e^{-2}+20e^{-1}+30` 及 `O=acc/l`。
  （来源：`msg-aa33725e76eaa5c3d7c4`）

- [高价值问题] “如果说是这一行 softmax 分母的 base-2 log 表示，我不明白为什么前面要加m_i的
  最大值。”——减最大值后的分母为 `l=2^{-m}Σ2^{x_j}`；加回 `m` 才得到原分母的 `log2`。
  学习者随后用 `x=[1,3]` 算出概率 `1/5、4/5`。（来源：`msg-1edcbdbed7a77a84c59d`、
  `msg-405984a90d7ad274e798`）

- [高价值问题] “之前的例子中为什么没有乘1/ln2的缩放，是这里的x是已经缩放后的吗？”——
  该手算例子的 `x` 已在 `exp2` 域；自然指数 score 才需乘 `1/ln2`。
  （来源：`msg-847c1b0b3108607d5b3c`）

- [转折] 学习者指出 program/grid 讲法抽象，“不知道`program_id(0)`是怎么选择query tile”，
  改用二维 grid 表后，独立算出 `pid0=0,pid1=4,H=3` 对应 query 行 `0–3`、`batch=1,head=1`。
  （来源：`msg-5561e87555cb6f42d10c`、`msg-c29fc9892e42c70bb03e`）

- [高价值问题] “为什么外层stage=3时内层还调用stage 2呢？3&2的值是True吗？”——
  `3=0b11`，`3&2=2` 为真；外层是阶段 bitmask，内层是具体模式。学习者再指出，若都为
  编译期常量，改写为 `if CAUSAL` 在理论上可有同样专用化效率。
  （来源：`msg-37e2a60ff7d2c877092c`、`msg-ff4d99704f404c086033`）

- [高价值问题] “那对于non-causal，BLOCK_SIZE就没用了吗？”——仍需分块扫描；学习者在
  `N=16,BLOCK_M=4,BLOCK_N=8` 的新例中算出每 head 4 个 Q program、每 program 两轮 K/V、
  每轮 `qk=[4,8]`。（来源：`msg-fa9e525632808ca70697`、`msg-92eed14353fb88cdf15d`）

- [纠错] 场景：判断前向 K/V 第二轮必须保留的量。我说“`m_i`、`l_i`需要保留”，漏了 `acc`
  和 Q tile → 正确：在线状态 `m_i/l_i/acc` 与循环不变的 Q 都要保留；第一块 V 对输出分子的贡献
  在 `α·acc₁` 中延续。原因：只有分母统计量无法恢复旧 value 贡献，Q 又要参与每轮新 `QKᵀ`。
  （来源：`msg-964c77d4d8d89b8c44ca`、`msg-3a8aee1c134fb3130d84`）

- [纠错] 场景：`pid1=5,N=8,start_n=2,BLOCK_N=2` 的 K descriptor 行。我说“为2、3行”→
  正确：`2、3` 是该 `(batch,head)` 内的 token；该 head 基址为 40，全局 descriptor 行是
  `42、43`。原因：K/V 扫描也必须加当前 `(batch,head)` 的 `offset_y`；学习者在新例中算出
  `pid1=4,start_n=6` 对应全局行 `38、39`。
  （来源：`msg-f3b33634af2188769fd8`、`msg-bd35c8c0fe2395752a05`）

- [要点] 一个前向 program 从 grid 定位到写回经历什么？——学习者串起固定
  `(batch,head,Q tile)`、Q 常驻、逐块载入 K/V、以新最大值重标定旧状态，以及写回 O 与 `M`。
  （来源：`msg-c3fda0addf5cfcf874a2`）

- [转折] 学习者从局部梯度公式回退追问“反向的整体概况。比如输入有哪些，需要输出什么”，
  随后辨认 `O/dO/dQ/dK/dV=[2,4,128,64]`、`M/Delta=[2,4,128]`，并追问教程反向为何有两个 kernel。
  （来源：`msg-2d5a761450ca37c847b4`、`msg-3660c5773e1a855189ad`）

- [要点] 为什么每行 `Delta` 可由 O 和 dO 求得？——学习者用
  `P=[1/4,3/4]、V=[2,6]、dO=2` 算出 `O=5`、`dP=(4,12)`、`P·dP=O·dO=10`，进而算出
  `dS=(-3/2,3/2)`。（来源：`msg-c7d76f77bf219c8b5adb`）

- [要点] Causal 反向中固定 query 与固定 key 的扫描范围怎样互换？——学习者指出 `dQ₂`
  看 key `0–2`，`dK₂/dV₂` 汇总 query `2–3`；对 tile `[4,8)`，能分别列出过去、对角与未来区域
  的 mask/跳过方式。（来源：`msg-bfc510f9515a9b70b1b3`、`msg-e375adce676e805873bc`）

- [要点] 多个 query 贡献同一 `dK/dV`，为何这份反向实现不需要 atomic？——学习者用
  `pid=1,N=256` 的例子说明，负责 `dK/dV[128:256]` 的单个 program 扫描有效 query 并独占写回。
  （来源：`msg-a841dbabfa1d209cefc9`）

- [纠错] 场景：综合题中已算对 `l'=3e^{-3}+4` 与 `acc'=e^{-3}A+B`，却把最终输出写为
  “`(3e^{-3}+4)/(e^{-3}A+B)`”→ 正确：`O=(e^{-3}A+B)/(3e^{-3}+4)`。原因：`acc` 是加权
  value 分子，`l` 是 softmax 分母；学习者随后用新数值题写对 `(10e^{-1}+20)/(2e^{-1}+1)`。
  （来源：`msg-7fdd821d2bcd30526379`、`msg-54b46b79cc5c1f22d49f`）

- [纠错] 场景：描述反向预处理的归约轴。我说“`delta=OdO对j求和`”→ 正确：
  `Delta_i=Σ_d O_{i,d}dO_{i,d}`，沿特征维 D 求和，结果 `[B,H,N]`。原因：它是每个 query
  的两个 D 维输出向量的点积；学习者在追问后明确了维度和形状。
  （来源：`msg-7fdd821d2bcd30526379`、`msg-dc55232ff44d2d69c910`）

- [纠错] 场景：区分反向要复用的前向量与最终梯度。我说“`backward保存dQ、dK和dV，重新计算了P`”
  → 正确：前向保存 `Q/K/V/O/M`，反向临时生成 `Delta`、按 tile 重算 score/P，最终输出
  `dQ/dK/dV`。原因：梯度在反向计算后才产生；学习者随后独立分清了三类量。
  （来源：`msg-7fdd821d2bcd30526379`、`msg-dc55232ff44d2d69c910`）

- [转折] 学习者接受 P06 FP16 前向契约后，澄清“测试的核心kernel当然是由我来编写，但我现在
  暂时没有充足时间”，要求先完成 Agent-owned 测试包、打断点并提取日志，自己日后再实现。
  恢复时不能把目前 expected red 的 `1 failed / 43 skipped` 视为实现失败，也不能把核心代码归给 Agent。
  （来源：`msg-d976f99d617f977818cf`、`msg-7bb02fe072c66cc57d3e`）

## 遗留

- [遗留] 学习者稍后编写 FP16 前向核心，再按 P06-A1–A4 进行验收；恢复位置与正式契约见
  [第 06 课 Lesson](../lessons/06-fused-attention.md)。（来源：`msg-7bb02fe072c66cc57d3e`）
