# 第 03 课：分块矩阵乘法的数据流、调度与验证

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-03-matrix-multiplication` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 独立解释、实现并验证 Triton 分块矩阵乘法 |
| 阶段 | `complete` |

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
<a id="e-05"></a>

- **E-05（O1／O2 conceptual，综合验收 S1）**：对 `A=(257,65)`、`B=(65,129)`、
  `BLOCK_M=BLOCK_N=64`、`BLOCK_K=32`、`GROUP_M=2` 的新 shape，学习者独立推导出 `5×3=15`
  个 program、尾组 `pid=12..14 → (4,0..2)`、最后 output tile 仅写回 `C[256,128]`，以及三轮
  K-loop 的有效 lane 数 `32/32/1`。能从“只沿 K 归约”解释 M/N 取模 dummy load 不污染有效输出，
  并区分 K load zero-padding mask 与最终 C store mask；`cdiv` 的书写记号经指出后修正，不影响推导。
<a id="e-06"></a>

- **E-06（O4 conceptual，综合验收 S2）**：学习者预测固定 tile、warps、stages 与 program 数时，
  `GROUP_M=2` 相比 `1` 可能通过相邻 program 的 tile 复用提高 L2 命中率并略快；提出固定其余配置、
  关闭多配置 autotune、预热、同步、重复计时，并在计时外与 PyTorch 验证正确性。学习者能够接受测量
  结果不支持预测；后续不把统计检验、置信区间或精细噪声建模加入本课 required gate。
- **综合验收 evidence**：S1/S2 均已通过，支持 O1/O2/O4 conceptual 的跨节点迁移与实验前预测。
- **E-07（O3 practical，Review）**：学习者第一版修订后由 Agent 独立复验得到 21 passed / 1 skipped；
  唯一 skip 是单 GPU 环境无法构造跨设备输入，源码已包含 `a.device == b.device` 防线。未提前公开的
  `(M,K,N)=(129,71,67)` 变式在 `GROUP_SIZE_M=1/2` 下均通过，最大绝对误差均为 `0.001953`；
  学习者独立推导其 `3×2` grid、最后两个 PID 到 `(2,0)/(2,1)`、K lane 数 `32/32/7`、右下角
  3 个有效输出，并解释尾组、K load mask 与 C store mask 的错误边界；尾组若错误固定为 2 还会遗漏
  `(2,1)` 的补充不影响整体判断。P03-A4 通过，受 assistance 影响的独立 evidence 已恢复。
- **E-08（O4 empirical，结果待解释）**：RTX 5090、Torch 2.13.0+cu130、Triton 3.7.1，固定
  `M=N=K=4096`、block `64×64×32`、4 warps、3 stages、同一输入，仅改变 `GROUP_SIZE_M=1/2`；
  两个 specialization 预编译后按 ABBA 顺序分别 warm-up 100 ms、计量 300 ms。四轮 median 为
  `G1 0.668704 ms`、`G2 0.690176 ms`、`G2 0.694272 ms`、`G1 0.697504 ms`；前后配对方向相反，
  且 G1 自身首末 p20–p80 区间不重叠。等待学习者判断支持／否定／证据不足及结论边界。
- **E-09（O4 empirical，结果解释）**：学习者正确判断 E-08 不支持原 `GROUP_SIZE_M=2` 更快的预测，
  也不能因首轮结果反向断言 group 1 更快；经即时收紧后，结论限定为“在本机、该 shape、固定配置与
  当前方法下，group 影响无法和约 4% 的运行状态漂移稳定分离”，不把证据不足扩大成“参数影响必然很小”。
- **E-10（O2／O4 conceptual，结课补充）**：固定教程的来源事实是：在 `9×9` output-block 示例中，
  计算前 9 个 output block 时，row-major 需要把 90 个 input block 加载到 SRAM，grouped ordering 为
  54 个；教程报告该机制在部分架构上可超过 10%，并给出 A100 约 `220 → 245 TFLOPS` 的示例，固定
  CUDA autotune configs 使用 `GROUP_SIZE_M=8`。据此形成的有边界推断是：当 M/N 均形成较大的二维
  tile grid、相邻 program 的 A/B tile 复用距离能落在 L2 驻留窗口内、kernel 对 L2／显存流量敏感，
  且 group size 与并发窗口和 block 配置匹配时，优化更可能显著；小或狭长 grid、全部工作集都命中／
  都无法驻留、计算或 wrapper 开销占主导，以及调度没有兑现线性 PID 局部性时，收益可能很弱。本课
  只比较 RTX 5090 上一个 shape/config 的 group 1/2，且 wrapper 计时包含 output allocation 并出现约
  4% 运行状态漂移，因此 E-08 不能裁决上述跨 shape、group size 或架构推断。
- **仍缺 evidence**：无；全部 required 维度已达到最低充分证据，Lesson 已由学习者确认关闭。
- **权威知识产物引用**：本地固定教程源码及其来源记录，见上方来源表。

## 条件片段：正式实践

| 字段 | 已接受内容 |
| --- | --- |
| Practice ID / revision | `triton-03-practice-01` / `1` |
| Digest | `sha256:917276363d8fa9ebaacc9fabd50260514712f1a352bcaeb24af5518c2645db30` |
| Targets | O3 `practical`：缺 learner-owned matmul 实现与正确性证据；O4 `empirical`：缺 `GROUP_SIZE_M=1/2` 最小受控测量与解释 |
| Task | 实现固定 `64×64×32` block 的 FP16 Triton matmul kernel 与 `matmul(a, b, *, group_size_m=2)`；随后解释一次 Agent-owned grouped-ordering 对照 |
| Deliverables | `gpu/triton/lesson03_matrix_multiplication.py`；一个关键边界测试解释；测量后的有边界证据判断 |
| Acceptance | `P03-A1` wrapper 输入／输出契约；`P03-A2` grouped mapping、指针、K mask、FP32 累加与 store mask；`P03-A3` 正常及 M/N/K/组合尾部正确性；`P03-A4` 无提示新变式与测试解释；`P03-A5` 事前预测、最小对照和结果解释 |
| Learner-owned | `gpu/triton/lesson03_matrix_multiplication.py`：create、modify、run |
| Agent-owned | `gpu/triton/lesson03_matrix_multiplication_test.py`、`gpu/triton/lesson03_matrix_multiplication_benchmark.py`、practice locator、Lesson 与 Checkpoint 记录 |
| Read-only / excluded | 固定官方教程源码只读；其他 Lesson、Skill 源码、依赖、CI、activation、FP8、穷举 autotune、profiler 与生产级 API 不动 |
| Help / completion gate | material assistance 只影响对应独立 evidence，并用新同构变式恢复；全部 required acceptance 通过且 required blocking／major finding 关闭后进入 mastery gate |
| Acceptance event | 学习者于 2026-08-19 明确回复“接受” |

### Agent-owned 验收工件

- 正确性与接口测试：`gpu/triton/lesson03_matrix_multiplication_test.py`。
- 最小测量 harness：`gpu/triton/lesson03_matrix_multiplication_benchmark.py`；固定 block、warps、stages、
  shape、输入与 program 数，仅改变 `GROUP_SIZE_M=1/2`，预编译后按 ABBA 顺序计量。
- 验收命令：`bash scripts/host-gpu.sh run -- python -m pytest -q gpu/triton/lesson03_matrix_multiplication_test.py`。
- **Expected red（2026-08-19）**：21 items 正常收集；仅
  `test_lesson03_implementation_exists` 因 learner-owned 文件尚不存在而失败，其余 20 项按设计跳过；
  Agent-owned 文件已通过 Ruff 与 BasedPyright。

### Review findings

| ID | Maps to | Severity / owner / status | Opened evidence | Next action |
| --- | --- | --- | --- | --- |
| `F-P03-01` | `P03-A2` | `major` / learner / `closed` | 第一版的 10 个数值用例均在编译阶段停于 `tl.min(num_pid_m - first_pid_m, GROUP_SIZE_M)`；`tl.min` 把第二个位置参数解释为 reduction axis，而输入是标量。Terminal：学习者改为合法的 `tl.minimum`；21 个可运行用例通过，未公开变式在两个 group 下通过 |  |
| `F-P03-02` | `P03-A1` | `major` / learner / `closed` | empty-dimension 已抛出 `ValueError`，但消息把 `positive` 写成 `postitive`；非法 group 消息使用 `group_num_size`，未指出公开参数 `group_size_m`。Terminal：两条消息修正后对应 3 个测试通过 |  |
| `F-P03-03` | `P03-A1` | `major` / learner / `closed` | wrapper 分别检查两者是 CUDA tensor，但未拒绝 `a.device != b.device`。Terminal：源码已在 launch 前拒绝不同 device；多 GPU 条件测试已收集，本机因只有一个 CUDA device 而 skip |  |

### Material assistance

- **Highest disclosure**：指出 `tl.min` 是 reduction API，并明确本处需要 scalar minimum（固定教程快照
  使用 Python 内建 `min`）；指出两处消息不匹配与同设备校验缺口。Agent 未修改 learner-owned 核心文件。
- **Affected scope**：`P03-A2` 尾组映射的独立实现证据、`P03-A1` wrapper 边界证据；后续由
  `P03-A4` 的无提示新 shape 变式恢复受影响的独立实践 evidence。`(129,71,67)` 已在两个 group 下
  独立通过，学习者的边界推导与错误解释充分，恢复完成。

<a id="final-mastery"></a>

## Final mastery

学习者于 2026-08-19 确认关闭 Lesson 03；以下判断一次写入并作为本课最终 mastery 事实源。

| 目标 | 所需维度 | 最小 evidence 锚点 | 判断 |
| --- | --- | --- | --- |
| O1：追踪 blocked matmul 数据流与 M/N/K 边界正确性 | conceptual | E-01、E-04、E-05；非整除新变式 E-07 | 充分 |
| O2：推导 grouped PID、尾组覆盖与复用边界 | conceptual | E-02、E-05、E-07、E-10 | 充分 |
| O3：独立实现并验证 FP16 Triton matmul | practical | learner-owned 实现；21 pass / 1 hardware skip；E-07 | 充分 |
| O4：解释 config 并作有边界的受控性能判断 | conceptual、empirical | E-03、E-06、E-08–E-10 | 充分 |

- 映射到 required gate 且未关闭的 blocking／major finding：0；`F-P03-01..03` 均已关闭。
- Material assistance：受影响的 P03-A1／P03-A2 独立 evidence 已由无材料提示的 P03-A4 新变式恢复；
  Agent 未写入 learner-owned 核心实现。
- Nonblocking 余项：单 GPU 环境使跨 CUDA device 测试条件性 skip；learner-owned 实现仍有 4 个 Ruff
  自动修复级样式问题（E713、W293×2、W292）。二者均不改变已验证的 required 行为或 mastery。
- 最终判断：O1–O4 的全部 required mastery 维度充分，Lesson 03 状态为 `complete`。

## 条件片段：Session event

| ID / 日期 | Lesson ref | 覆盖范围 | 完成动作 | Evidence 引用 | 未关闭问题 | Confirmed duration | Marker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `triton-03-session-2026-08-17-a` / 2026-08-17 | `triton-03-matrix-multiplication` | blocked matmul 数据流与 M/N/K 边界；取模与 mask；grouped ordering 与尾组；autotune config 取舍；正确性测试设计 | 完成四个概念节点及节点级变式，进入综合验收后主动暂停 | E-01–E-04；[结构化学习过程记录](../logs/2026-08-17-matrix-multiplication.md)（非 mastery 事实源） | S1/S2 未作答；O3 正式实践未建立；O4 受控实测未进行 |  | 无 |
| `triton-03-session-2026-08-19-a` / 2026-08-19 | `triton-03-matrix-multiplication` | 正式实践、实现 Review、最小实证测量、grouped ordering 适用边界与结课 | 接受 `triton-03-practice-01` revision 1；Agent 建立验收工件；学习者提交并修订核心实现；关闭 `F-P03-01..03`；完成无提示新变式与边界解释；Agent 运行 grouped-ordering ABBA 对照；学习者解释证据不足，并区分教程事实、本地观察与跨场景推断；确认关闭本课 | Accepted practice digest；initial expected-red；修订后 21 pass / 1 hardware skip；E-07–E-10；[Final mastery](#final-mastery) | 无 |  | `closure` |
