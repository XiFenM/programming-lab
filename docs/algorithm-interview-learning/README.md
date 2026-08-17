# 算法面试学习档案

本目录是算法面试长期 Course 的活动状态事实源：

- 本文件承担 Program 控制面与唯一 Checkpoint。
- `lessons/` 中的已授权文件承担对应 Lesson 的 evidence ledger。
- `docs/algorithm-interview-course/` 是只读 teaching source，不承担个人进度或 mastery。
- 学习日志、原始对话和记忆卡只有在另行明确授权后生成，不属于课程状态。

本 Program 与 [`triton-official-tutorials`](../triton-learning/README.md#当前-program-状态) 并行保持
`active`。两条课程分别维护自己的 Program、Lesson 与 Checkpoint；一次具体学习上下文只选择一条课程
的前台 Lesson，切换课程不会冻结、关闭或自动推进另一条课程。

## 当前 Program 状态

| 字段 | 当前值 |
| --- | --- |
| Program ID / 标题 | `leetcode-algorithm-interview` / LeetCode 算法面试能力课程 |
| State | `active` |
| Parallel Program ref | [`triton-official-tutorials`](../triton-learning/README.md#当前-program-状态)（`active`） |
| Objective | 独立处理常见算法面试题：澄清约束、建立模型与基线、定义状态或不变量、实现并验证、说明正确性与复杂度，并迁移到陌生同构题。 |
| Included | 固定文字课程中的面试方法、复杂度、常见数据结构与算法模式；证据需要时在既有 LeetCode 目录完成最小实践。 |
| Excluded | 机械刷完 70 课；课程未系统覆盖的高级算法；未授权的多语言重复实现、optional extension、平台时效信息和生产级工程扩展。 |
| Authorized Lesson refs | [`lessons/01-constraint-driven-selection.md`](lessons/01-constraint-driven-selection.md) |
| Checkpoint ref | [下方唯一 Checkpoint](#checkpoint) |

## Candidate Lessons

候选顺序用于组织路线，不构成启动授权。

| Order | Candidate ID | 能力标题 |
| ---: | --- | --- |
| 1 | `lai-01-constraint-driven-selection` | 约束驱动的算法选择与可观察表达 |
| 2 | `lai-02-baseline-bottleneck-validation` | 基线、瓶颈与验证 |
| 3 | `lai-03-complexity-analysis` | Big O 与复杂度分析 |
| 4 | `lai-04-binary-search-invariants` | 二分查找与循环不变量 |
| 5 | `lai-05-partition-two-pointers` | 原地分区与双指针 |
| 6 | `lai-06-sliding-window` | 滑动窗口与连续区间状态 |
| 7 | `lai-07-lookup-tables` | 查找表与键值建模 |
| 8 | `lai-08-linked-lists` | 链表操作与指针不变量 |
| 9 | `lai-09-stack-queue-heap` | 栈、队列与优先队列的处理顺序 |
| 10 | `lai-10-trees-recursion` | 二叉树与递归契约 |
| 11 | `lai-11-backtracking` | 回溯、选择空间与剪枝 |
| 12 | `lai-12-dynamic-programming` | 动态规划的状态与转移 |
| 13 | `lai-13-greedy-proof` | 贪心选择与正确性论证 |
| 14 | `lai-14-integrated-interview` | 综合迁移与面试模拟 |

## Checkpoint

| 字段 | 当前值 |
| --- | --- |
| Foreground context | `leetcode-algorithm-interview` Program |
| Semantic position | Lesson 01 已确认关闭；当前没有 active Lesson，位于 Lesson 边界等待下一课授权。 |
| Next action | 学习者决定是否授权启动候选 Lesson 02 `lai-02-baseline-bottleneck-validation`。 |
| Forward gate | 只有学习者明确授权后才创建并激活 Lesson 02；关闭 Lesson 01 不自动启动下一课。 |
| Latest evidence ref | [`lessons/01-constraint-driven-selection.md#final-mastery`](lessons/01-constraint-driven-selection.md#final-mastery) |
| As of | 2026-08-15 |
