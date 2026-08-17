# 第 03 课：分块矩阵乘法的数据流、调度与验证

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-03-matrix-multiplication` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 独立解释、实现并验证 Triton 分块矩阵乘法 |
| 阶段 | `synthesis` |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/03-matrix-multiplication.py` | `teaching-spine` | `tutorials_python.zip` SHA-256 `2d838ed48281a3bcf901e230ab9abc29b042e4ddf899eef8347676612259ed04`，下载于 2026-07-15 | 教学顺序、blocked algorithm、grouped ordering、autotune 与 benchmark 示例 |
| `docs/triton-tutorials/official/03-matrix-multiplication.py` | `implementation-authority` | Git commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；blob `526934c1d7c60ccbb8119b1bca0e807f6fc602e8` | 固定快照的 kernel、wrapper、测试和 benchmark 控制流 |
| `docs/triton-tutorials/SOURCE.md` | `explanatory-support` | 下载记录 2026-07-15 | 上游来源、完整性与版本边界 |

### 目标与证据门槛

| ID | 可观察目标 | conceptual | practical | empirical | 本课 evidence 目标 |
| --- | --- | --- | --- | --- | --- |
| O1 | 从一个 `C` tile 出发，追踪 `A`/`B` block 指针、K-loop、FP32 累加与边界 mask，并解释非整除 `M/N/K` 时的正确性 | required | not-required | not-required | 独立完成数据流追踪和一个非整除边界变式 |
| O2 | 从一维 program ID 推导 grouped `(pid_m, pid_n)`，说明尾组覆盖与 L2 数据复用边界 | required | not-required | not-required | 独立推导一个尾组示例，并与 row-major 顺序比较 |
| O3 | 独立实现 FP16 Triton matmul kernel 与 wrapper，并以正常和边界 shape 验证接口与数值正确性 | not-required | required | not-required | learner-owned 实现通过约定的正确性与静态验收，并完成无材料提示变式 |
| O4 | 解释 autotune 的 config/key 选择，并用受控测量检验一个调度或配置预测，给出有环境边界的性能结论 | required | not-required | required | 事前可证伪预测、可复现实验、适当基线与结论边界齐全 |

### 当前证据

- **已确认前置**：Lesson 02 已验证 block/mask、program 映射、资源与 benchmark 边界；本课会复用这些
  模式，但不把既有 evidence 直接当作矩阵乘法 mastery。
- **E-01（O1，节点级）**：能追踪 `A_tile=[BLOCK_M,BLOCK_K]`、
  `B_tile=[BLOCK_K,BLOCK_N]`、FP32 accumulator 与两轮 K-block；能区分 M/N 自由维度的合法 dummy
  load、K 归约维度的 zero-padding load mask 和最终 C store mask。
- **E-02（O2，节点级）**：能从 grouped ordering 推导相邻 PID 的 B tile 复用，并正确计算
  `num_pid_m=5`、`num_pid_n=3`、`GROUP_SIZE_M=2` 时尾组 `pid=12..14 → (4,0..2)`；能说明固定使用
  完整组大小会造成越界和遗漏。
- **E-03（O4 conceptual，节点级）**：能比较两组 tile config 的 program 数、K-loop 次数、资源与边界
  浪费，并在 `M=N=130,K=64` 变式中算出大 tile 配置的无效 output lane 比例更高；已明确性能结论仍需
  目标 GPU 上的受控测量。
- **E-04（O1／O3 准备性，节点级）**：能设计分别触发 M、N、K 尾部的三个 shape，并在纠正后说明
  `K=40,BLOCK_K=32` 的第二轮有 8 个有效 lane、24 个 masked lane，以及 C store mask 不能替代 K
  load mask。
- **综合验收 evidence**：尚无；S1 与 S2 已给出但均未作答，以上节点级证据不提前裁决最终 mastery。
- **仍缺 evidence**：O1/O2/O4 conceptual 的跨节点综合迁移，O3 practical，以及 O4 empirical。
- **权威知识产物引用**：本地固定教程源码及其来源记录，见上方来源表。

## 条件片段：Session event

| ID / 日期 | Lesson ref | 覆盖范围 | 完成动作 | Evidence 引用 | 未关闭问题 | Confirmed duration | Marker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `triton-03-session-2026-08-17-a` / 2026-08-17 | `triton-03-matrix-multiplication` | blocked matmul 数据流与 M/N/K 边界；取模与 mask；grouped ordering 与尾组；autotune config 取舍；正确性测试设计 | 完成四个概念节点及节点级变式，进入综合验收后主动暂停 | E-01–E-04；[结构化学习过程记录](../logs/2026-08-17-matrix-multiplication.md)（非 mastery 事实源） | S1/S2 未作答；O3 正式实践未建立；O4 受控实测未进行 |  | 无 |
