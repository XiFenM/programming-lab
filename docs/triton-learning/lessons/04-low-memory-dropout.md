# 第 04 课：基于 seed/offset 的低内存 Dropout

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-04-low-memory-dropout` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 解释并实现基于 seed/offset 的低内存 Dropout |
| 阶段 | `complete` |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/04-low-memory-dropout.py` | `teaching-spine` | `tutorials_python.zip` SHA-256 `2d838ed48281a3bcf901e230ab9abc29b042e4ddf899eef8347676612259ed04`，下载于 2026-07-15 | inverted dropout、显式 keep mask、seeded dropout 与复现性示例 |
| `docs/triton-tutorials/official/04-low-memory-dropout.py` | `implementation-authority` | Git commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；blob `3dd84da47e6f377b4700cd2141f1f87dc76984f3` | 固定快照的 kernel、wrapper 与随机数映射控制流 |
| `docs/triton-tutorials/SOURCE.md` | `explanatory-support` | 下载记录 2026-07-15 | 上游来源、完整性与版本边界 |

### 目标与证据门槛

| ID | 可观察目标 | conceptual | practical | empirical | 本课 evidence 目标 |
| --- | --- | --- | --- | --- | --- |
| O1 | 解释 inverted dropout 的 keep/drop 语义、`1 / (1 - p)` 缩放及其期望保持性质 | required | not-required | not-required | 独立计算一个小向量的可能输出，并推导单元素输出的期望 |
| O2 | 追踪 `(seed, offset)` 到伪随机数和 keep 决策的数据流，说明确定性复现及不物化完整 mask 的内存收益与边界 | required | not-required | not-required | 独立解释同 seed、不同 seed 和全局 offset 在复现性中的作用，并与显式 mask 方案比较 |
| O3 | 独立实现一维 seeded low-memory dropout kernel 与 wrapper，并验证边界、输出不变量和 seed 语义 | not-required | required | not-required | learner-owned 实现通过约定的接口、正确性、复现性与无提示变式验收 |

### 当前证据

- **已确认前置**：既有 Lesson 已覆盖一维 program/offset、边界 mask、masked load/store 和 Triton wrapper
  的基本模式；这些只作为本课起点，不直接证明 Dropout mastery。
<a id="e-01"></a>

- **E-01（O1，节点级）**：能正确计算 `p=0.25,x=12` 时 keep/drop 概率、两个可能输出与期望，并解释
  inverted scaling 保持的是输出期望而非每次实现值；后续一度把 `p=0.5` 时保留值 `2x` 写成期望，
  经最小纠正后在新例中独立恢复为 `0/20` 各半、期望 `10`。
<a id="e-02"></a>

- **E-02（O2，节点级）**：能追踪尾部 program 的 global offsets、boundary mask、显式 keep mask 与写回；
  能诊断 local offsets 会让不同 program 重复随机 pattern，并说明同 seed、global offset、`p` 与输入对
  mask／输出复现的不同作用。经条件变式后还能解释不同输入只在被丢弃位置不同时可得到相同输出。
<a id="e-03"></a>

- **E-03（O1／O2，综合验收 S1）**：能在同一尾部 program 中结合 boundary mask、严格 `random > p`、
  inverted scaling 与 masked store，正确得到有效输出 `0/-4`，并比较显式 mask 与 seeded 方案的状态、
  数据移动和现场 PRNG 取舍。最初误认为元素重排后相同 seed 仍会让 mask 跟随逻辑元素；经最小纠正后，
  在 `A → A.T.contiguous()` 新例中独立追踪 `b:1→2`、`d:3→1`，说明随机数绑定 global offset 而非
  抽象元素。O1/O2 conceptual 综合 evidence 已充分。
<a id="e-04"></a>

- **E-04（O3 practical，首次 Review）**：learner-owned 实现已提交；Agent 独立复验 19/19 通过，确认
  接口拒绝行为、输出 metadata、inverted-dropout 不变量、同／异 seed、exact/tail/multi-program 与
  global-offset 非重复 pattern。源码包含 global offset、boundary mask、`tl.rand(seed, offset)`、严格
  keep 判定与 masked store；但 wrapper 使用 `BLOCK_SIZE=128`，与已接受任务的固定 `1024` 不一致。
  仓库静态检查另报 Ruff I001/E721 和一处 BasedPyright launch typing error，均为契约外 non-gating
  observation。
<a id="e-05"></a>

- **E-05（O3 practical，P04-A4 运行）**：对事前未公开的连续 shape `(17,121)`、`n=2057`、
  `p=0.375`，修订后的固定 `BLOCK_SIZE=1024` 实现通过输出 metadata 与 `0`／scaled-value 不变量；
  seed `20260824` 重复运行完全相同，换为 `20260825` 后本次输出不同，保留数分别为 1286／1280。
<a id="e-06"></a>

- **E-06（O3 practical，P04-A4 解释）**：学习者独立说明 `n=2057` 时 grid 有 3 个 program，最后一个
  `pid=2` 覆盖 `[2048,3072)`，其中 `[2048,2057)` 的 9 个 lane 有效；说明 `tl.load` 与 `tl.store`
  需要 boundary mask，而不访问内存的 `tl.rand` 不需要。能把同 seed 精确复现限定到相同随机函数、输入、
  `p` 与逻辑元素 global offset，并指出不同 seed 只在本次观测中产生不同输出，不能泛化为必然不同。
  在聚焦变式 `n=1025` 中进一步确认最后一个 program 有 `1` 个有效 lane、`1023` 个无效 lane。
- **仍缺 evidence**：无；P04-A1–A4 已完成，required finding 已全部关闭，Lesson 已由学习者确认关闭。
- **权威知识产物引用**：本地固定教程源码及其来源记录，见上方来源表。

<a id="practice-01"></a>

## 条件片段：正式实践

| 字段 | 已接受内容 |
| --- | --- |
| Practice ID / revision | `triton-04-practice-01` / `1` |
| Digest | `sha256:e75f6664e2718193ca2a182ac960e844e371fe1add5ab501ff78e3ee23441820` |
| Targets | O3 `practical`：缺 learner-owned seeded dropout kernel、wrapper、正确性、复现性与独立变式 evidence |
| Task | 在 `gpu/triton/lesson04_low_memory_dropout.py` 实现固定 `BLOCK_SIZE=1024` 的一维 seeded dropout kernel 与 wrapper |
| Deliverables | 导出 `seeded_dropout_kernel` 和 `seeded_dropout`；支持已披露的非空连续 CUDA float32 输入、`0 <= p < 1` 与非负 int32 seed 契约 |
| Acceptance | `P04-A1` 接口校验与输出 metadata；`P04-A2` global offsets、boundary mask、`tl.rand`、严格 keep 判定、缩放与 store；`P04-A3` identity、seed、输出不变量、exact/tail/multi-program；`P04-A4` 无提示新变式与解释 |
| Learner-owned | `gpu/triton/lesson04_low_memory_dropout.py`：create、modify、run |
| Agent-owned | `gpu/triton/lesson04_low_memory_dropout_test.py`：create、modify、run；本 Lesson 与 Program Checkpoint：record |
| Read-only / excluded | 固定教程源码、`scripts/host-gpu.sh`、`pyproject.toml` 只读；其他 Lesson、教程修改、依赖／CI／配置、backward、矩阵逐行 seed、stride、sparse JL 与性能工作不动 |
| Help / completion gate | material assistance 只影响对应 acceptance，并用无提示同构变式恢复；P04-A1–A4 全部通过且 required blocking／major finding 关闭后进入 mastery gate |
| Acceptance event | 学习者于 2026-08-24 明确回复“接受” |

### Agent-owned 验收工件

- 测试：`gpu/triton/lesson04_low_memory_dropout_test.py`；只验证公开接口、行为、不变量和已披露边界，
  不包含参考 kernel。
- 命令：`bash scripts/host-gpu.sh run -- python -m pytest -q -vv gpu/triton/lesson04_low_memory_dropout_test.py`。
- **Expected red（2026-08-24）**：19 items 正常收集；仅 `test_lesson04_implementation_exists` 因
  learner-owned 文件尚不存在而失败，其余 18 项按设计跳过；Agent-owned 测试通过 Ruff 与 BasedPyright。

### Review findings

| ID | Maps to | Severity / owner / status | Opened evidence | Next action |
| --- | --- | --- | --- | --- |
| `F-P04-01` | O3 / accepted task / `P04-A2` | `major` / learner / `closed` | Opened：19 项运行测试均通过，但 wrapper 的 launch block 为 `128`；revision 1 要求固定 `1024`。Terminal：学习者改为 `1024`，Agent 复验 19/19 通过 |  |

<a id="final-mastery"></a>

## Final mastery

学习者于 2026-08-24 确认关闭 Lesson 04；以下判断一次写入并作为本课最终 mastery 事实源。

| 目标 | 所需维度 | 最小 evidence 锚点 | 判断 |
| --- | --- | --- | --- |
| O1：解释 inverted dropout、缩放与期望保持 | conceptual | E-01、E-03 | 充分 |
| O2：解释 seed/offset 随机映射、复现性与内存取舍 | conceptual | E-02、E-03 | 充分 |
| O3：独立实现并验证一维 seeded low-memory dropout | practical | learner-owned 实现；19/19 pass；E-04–E-06 | 充分 |

- 映射到 required gate 且未关闭的 blocking／major finding：0；`F-P04-01` 已关闭。
- Material assistance：未发生影响独立实践 evidence 的实质帮助；Agent 未写入 learner-owned 核心实现。
- Nonblocking 余项：learner-owned 实现仍有 Ruff I001/E721，以及一处 BasedPyright launch typing
  observation；这些契约外观察不改变已验证的 required 行为或 mastery。
- 最终判断：O1–O3 的全部 required mastery 维度充分，Lesson 04 状态为 `complete`。

## 条件片段：Session event

| ID / 日期 | Lesson ref | 覆盖范围 | 完成动作 | Evidence 引用 | 未关闭问题 | Confirmed duration | Marker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `triton-04-session-2026-08-24-a` / 2026-08-24 | `triton-04-low-memory-dropout` | inverted dropout；seed/offset 随机映射与复现边界；正式实践、Review、无提示变式与结课 | 完成 O1/O2 教学循环与综合验收；接受 `triton-04-practice-01` revision 1；Agent 建立验收测试；学习者提交并修订核心实现；关闭 `F-P04-01`；完成 P04-A4 变式及解释；确认关闭本课 | Accepted practice digest；19/19 pass；E-01–E-06；[Final mastery](#final-mastery) | 无 |  | `closure` |
