# Lesson 01：约束驱动的算法选择与可观察表达

## 核心记录

| 字段 | 当前值 |
| --- | --- |
| Lesson ID | `lai-01-constraint-driven-selection` |
| Program | [`leetcode-algorithm-interview`](../README.md) |
| 能力标题 | 根据约束选择算法方向，并让面试官能够观察和评估推理过程 |
| Stage | `complete` |
| Final mastery | [已确认关闭](#final-mastery) |
| Event refs | [Closure event](#se-lai-01-2026-08-15-closure) |

## 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| [`docs/algorithm-interview-course/notes/lessons/01-01.md`](../../algorithm-interview-course/notes/lessons/01-01.md) | `teaching-spine` | `daily-work@d74ca5e61cc4552cd134f1064c04beb3cd4ce584`，2026-08-13 导入 | 面试评价框架、排序约束示例、难题中的持续表达 |
| [`docs/algorithm-interview-course/SOURCE.md`](../../algorithm-interview-course/SOURCE.md) | `explanatory-support` | 同一固定来源提交 | 来源范围、缺失媒体与编辑综合边界 |

## 目标与 Evidence Targets

| ID | 可观察目标 | conceptual | practical | empirical | Evidence target |
| --- | --- | --- | --- | --- | --- |
| O1 | 解释算法面试为什么不只评价最终结果，并说明它与完整技术面试、最终 Offer 的边界。 | required | not-required | not-required | 独立复述评价框架，并应用到一个暂时没有完整终解的场景。 |
| O2 | 识别数据特征、语义要求、表示方式与资源限制，并解释它们为什么会改变候选算法。 | required | required | not-required | 面对未直接讲过的问题提出必要澄清项，并把至少一个约束变化映射到方案变化。 |
| O3 | 把候选方向与已确认约束绑定，同时说明取舍和剩余未知。 | required | required | not-required | 完成一次简洁的面试式方案陈述，不把关键词与算法机械配对。 |

## 当前证据

<a id="e-01"></a>

- **E-01（2026-08-14，独立理解检查）**：学习者主动识别了规模、重复度、已有有序性、值域、稳定性、是否原地、数据结构和可用内存等约束；并在值域固定为 `{0, 1, 2}` 的假设下，提出计数后重写的线性扫描方向。
- **支持范围**：为 O2 的 conceptual／practical 和 O3 的 conceptual 提供初步证据。

<a id="e-02"></a>

- **E-02（2026-08-14，变式理解检查）**：学习者说明了 `i < j` 完整覆盖两个不同下标的解空间，解释了两层枚举的二次成本，并把后续方向落到保存查询信息、减少重复查找。
- **支持范围**：为 O1 的情境应用和 O3 的 practical 提供证据。

<a id="e-03"></a>

- **E-03（2026-08-14，补差后的独立变式）**：在输入只读、额外空间 `O(1)`、返回原始下标且值域固定为 `{0, 1, 2}` 时，学习者用每个值至多保存两个下标的常数状态得到 `O(n)` 时间、`O(1)` 空间方案；经反例修正后完整识别六类无序值对，并在 `nums = [1, 0, 2]`、`target = 2` 上返回 `[1, 2]`，以第二个 `1` 的下标仍为 `-1` 排除复用同一下标。
- **支持范围**：巩固 O2 的 conceptual／practical 和 O3 的 practical 证据。

<a id="e-04"></a>

- **E-04（2026-08-14，补差后的评价边界复述）**：学习者把正向评价限制在当前算法问题中实际观察到的约束澄清、正确基线、复杂度分析、优化探索和思路表达，并把完整实现、调试、边界处理、系统设计及其他技术知识列为尚未观察的能力；同时明确不能由这段局部表现直接推出整体岗位胜任或 Offer。
- **支持范围**：补足 O1 的 conceptual 证据。

<a id="e-05"></a>

- **E-05（2026-08-15，跨节点综合验收及补差后独立变式）**：面对陌生的精确重复 ID 检测，学习者先询问规模、值域、存储／访问方式和额外空间；把普通数组、任意值域且允许 `O(n)` 空间映射到哈希集合，把小固定值域映射到标记数组，并在任意顺序、单遍、`O(1)` 空间下正确排除排序、哈希集合和小值域表，同时保留剩余未知。学习者最初误把数组上的 `O(n²)` 基线视为仍可用于单遍流；经定点纠正后，在未给出解法的“非递减流”变式中独立证明重复值必然相邻，只保存前一个 ID 即可得到 `O(n)` 时间、`O(1)` 空间，并解释该方案为何不适用于任意顺序流。
- **支持范围**：补足 O2 与 O3 的 conceptual／practical 证据；访问模型相关的定点帮助已由新变式恢复。
- **Mastery gate**：全部 required 维度已有最低充分证据；无 required blocking／major finding。

<a id="final-mastery"></a>

## Final Mastery

| 目标 | Required 维度 | 最小 evidence | 结论 |
| --- | --- | --- | --- |
| O1 | conceptual | [E-04](#e-04) | 充分 |
| O2 | conceptual | [E-01](#e-01)、[E-05](#e-05) | 充分 |
| O2 | practical | [E-03](#e-03)、[E-05](#e-05) | 充分 |
| O3 | conceptual | [E-01](#e-01)、[E-05](#e-05) | 充分 |
| O3 | practical | [E-02](#e-02)、[E-03](#e-03)、[E-05](#e-05) | 充分 |

- **Closure confirmation**：学习者于 2026-08-15 明确确认关闭 Lesson 01。
- **Required findings**：未关闭的 blocking／major finding 为 0。
- **Assistance recovery**：单遍流访问模型的定点帮助已由 E-05 中的非递减流独立变式恢复；Agent 未写入 learner-owned 核心工件。
- **Nonblocking follow-up**：`unordered_set` 的平均与最坏复杂度、标记数组的 `O(K)` 表述，以及有序流首元素初始化，留待后续相关 Lesson 或 optional 复习。
- **Final conclusion**：O1–O3 的全部 required 维度均已满足；empirical 均为 not-required。

<a id="se-lai-01-2026-08-15-closure"></a>

## Session Event

| 字段 | 当前值 |
| --- | --- |
| Event ID | `se-lai-01-2026-08-15-closure` |
| Date | 2026-08-15 |
| Context | `lai-01-constraint-driven-selection` Lesson |
| Covered scope | 重复 ID 综合验收补差、非递减流独立变式与 mastery gate。 |
| Completed actions | 形成 E-05；展示目标与 required 维度的 evidence matrix；学习者确认关闭 Lesson 01。 |
| Evidence refs | [E-05](#e-05)、[Final mastery](#final-mastery) |
| Marker | `closure` |
