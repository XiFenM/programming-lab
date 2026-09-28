# Triton 学习档案

本目录持续记录基于 `docs/triton-tutorials/official/` 的 Triton 学习。第 01、02 课及其对话由旧流程
形成，现作为冻结的 legacy evidence 保留；从第 03 课起采用中央 `guide-learning`。

本 Program 与 [`leetcode-algorithm-interview`](../algorithm-interview-learning/README.md#当前-program-状态)
并行保持 `active`。两条课程分别维护自己的 Program、Lesson 与 Checkpoint；一次具体学习上下文只选择
一条课程的前台 Lesson，切换课程不会冻结、关闭或自动推进另一条课程。

## 教学与状态

讲解、提问、练习、Review 与结课的行为由中央 `guide-learning` 定义，本仓库不复制；学习者画像与目标
深度见 [学习者画像](../learning-profile.md)。本课程的状态只落在三处：

| 职责 | 位置 |
| --- | --- |
| Program：长期范围、排除项与候选顺序 | 本页“当前 Program 状态”与“课程索引” |
| Lesson：目标、来源、阶段事件、练习约定、证据与结课结论 | `lessons/<NN>-<topic>.md` |
| Checkpoint：当前位置、唯一下一动作与前进门槛 | 本页 [Checkpoint](#checkpoint) |

当前是哪一课只写在 Checkpoint；Program 与课程索引不重复记录当前课或逐课状态。受管配置同时登记了
两条课程的 Program、Checkpoint、Lesson 与练习目录，切换课程不需要修改配置或重新 materialize。
文章、结构化过程记录、卡片和原始对话均为按需产物，不是 Program、Lesson 或 Checkpoint 的事实源。

## 目录约定

```text
docs/triton-learning/
├── README.md                         # Program 控制面、课程索引和记录边界
├── templates/
│   └── lesson-record.md              # 第 03 课起使用的精简 Lesson 模板
├── references/
│   ├── pytest-gpu-kernel-tests.md     # Triton GPU 正确性测试参考
│   └── raw-dialogue-export.md         # study-log 现行规则与 legacy 说明
├── dialogues/                        # 冻结的第 01、02 课 legacy 对话
├── transcripts/                      # 配对规则启用前保存的可追溯可见对话，保持原样
├── logs/                             # 按需生成的 structured 学习过程记录
├── logs-raw/                         # 明确要求时保存的同名配对原文
├── cards/                            # 按需生成的受管 Markji 暂存卡片
├── lessons/
│   ├── 01-vector-add.md              # 冻结的旧结构 Lesson 记录
│   ├── 02-fused-softmax.md
│   └── ...
└── attachments/                      # 可选图表、性能数据等补充材料
    └── <课程序号>-<主题>/
```

- 单课记录统一命名为 `<两位序号>-<英文主题>.md`。
- 实践源码、测试和 benchmark 放在 `gpu/triton/`；Lesson 使用相对链接，不复制实现。
- 少量实验结果可以写入 Lesson；过大或需要机器读取的内容放入 `attachments/` 并链接。
- 官方教程快照保持原样，不在 `docs/triton-tutorials/official/` 中写笔记或修改代码。
- `dialogues/` 不再接收新 raw 归档；其中旧名称、旧路径和历史命令保持原样。
- `logs/` 是 `study-log` 的 structured target，也是 `english-coach` 与 `memo-cards` 共享的学习记录
  目录；制卡与英语回顾只读取学习者明确指定的记录，与文件是否已被 Git 跟踪无关。
- `cards/` 是 `memo-cards` 的输出目录；只有 `triton-*.md` 进入受管 inventory。静态目录与配置都不授权
  制卡或发布，legacy 对话、transcripts 与 Lesson 也不会被隐式读取。`cards/previews/` 中已有的课程卡片
  预览保持原样。
- 原始可见对话默认不保存；学习者明确要求时，由 `study-log` 在确认边界与隐私后写入 `logs-raw/`，与
  `logs/` 中的记录同名配对。保存不等于授权提交或公开。

## 课程索引

下表是规划顺序，不构成启动授权。已有记录链接的课次已经授权，阶段与结课结论只写在各课记录中；候选
课次只在学习者明确开始后才创建记录。第 01、02 课是冻结的 legacy 记录。

| 课次 | 官方案例 | 学习记录 |
| --- | --- | --- |
| 01 | `01-vector-add.py` | [lessons/01-vector-add.md](lessons/01-vector-add.md)（legacy） |
| 02 | `02-fused-softmax.py` | [lessons/02-fused-softmax.md](lessons/02-fused-softmax.md)（legacy） |
| 03 | `03-matrix-multiplication.py` | [lessons/03-matrix-multiplication.md](lessons/03-matrix-multiplication.md) |
| 04 | `04-low-memory-dropout.py` | [lessons/04-low-memory-dropout.md](lessons/04-low-memory-dropout.md) |
| 05 | `05-layer-norm.py` | [lessons/05-layer-norm.md](lessons/05-layer-norm.md) |
| 06 | `06-fused-attention.py` | [lessons/06-fused-attention.md](lessons/06-fused-attention.md) |
| 07 | `07-extern-functions.py` | 候选，尚无记录 |
| 08 | `08-grouped-gemm.py` | 候选，尚无记录 |
| 09 | `09-persistent-matmul.py` | 候选，尚无记录 |
| 10 | `10-block-scaled-matmul.py` | 候选，尚无记录 |

获得新 Lesson 授权后，以 `templates/lesson-record.md` 的“核心记录”为基础创建 `lessons/<NN>-<topic>.md`；
条件片段只在对应事实实际发生时追加，不要整份复制出空章节。

## Legacy 对话索引

以下文件是旧流程生成的可见文本快照，保留其旧 Skill 名称、路径和正文，不再刷新或覆盖。现行原文只在
学习者明确要求时由 `study-log` 生成，确认边界与隐私后写入 `logs-raw/`；规则见
[study-log 与 legacy 对话](references/raw-dialogue-export.md)。

| 编号 | 范围 | 原始对话 | 消息数 | 归档状态 |
| --- | --- | --- | --- | --- |
| 00 | 学习流程建立 | [dialogues/00-learning-workflow.md](dialogues/00-learning-workflow.md) | 4 | 已导出（frozen legacy） |
| 01-A | Vector Addition：开课至阶段性保存 | [dialogues/01-vector-add.md](dialogues/01-vector-add.md) | 57 | 已导出（frozen legacy） |
| 01-B | Vector Addition：恢复至最终复验 | [dialogues/01-vector-add-part2.md](dialogues/01-vector-add-part2.md) | 37 | 已导出（frozen legacy） |
| 01-C | Vector Addition：可选性能扩展至暂停 | [dialogues/01-vector-add-part3.md](dialogues/01-vector-add-part3.md) | 87 | 已导出（frozen legacy） |
| 01-D | Vector Addition：性能扩展工程收尾 | [dialogues/01-vector-add-part4.md](dialogues/01-vector-add-part4.md) | 18 | 已导出（frozen legacy） |
| 02-A | Fused Softmax：开课至 P01 布置与 Q03 确认 | [dialogues/02-fused-softmax.md](dialogues/02-fused-softmax.md) | 29 | 暂停快照（frozen legacy） |
| 02-B | Fused Softmax：P01 实践与三轮评审 | [dialogues/02-fused-softmax-part2.md](dialogues/02-fused-softmax-part2.md) | 32 | 暂停快照（frozen legacy） |
| 02-C | Fused Softmax：Persistent、资源与 Benchmark 至结课 | [dialogues/02-fused-softmax-part3.md](dialogues/02-fused-softmax-part3.md) | 153 | 已导出（frozen legacy） |
| 02-D | Fused Softmax：结课后 Benchmark 解释 | [dialogues/02-fused-softmax-part4.md](dialogues/02-fused-softmax-part4.md) | 6 | 已导出（frozen legacy） |
| 02-E | Fused Softmax：Softmax/Log-softmax 快速回顾 | [dialogues/02-fused-softmax-part5.md](dialogues/02-fused-softmax-part5.md) | 9 | 收尾快照（frozen legacy） |

## 当前 Program 状态

| 字段 | 当前值 |
| --- | --- |
| Program ID / 标题 | `triton-official-tutorials` / Triton 官方教程学习 |
| State | `active` |
| Parallel Program ref | [`leetcode-algorithm-interview`](../algorithm-interview-learning/README.md#当前-program-状态)（`active`） |
| Objective | 理解、实现并验证本仓库固定版本的 Triton 官方教程 |
| Included | 官方案例的概念、实现、正确性与目标明确时的实证验证 |
| Excluded | 未获授权的独立性能研究、optional extension 与下一 Lesson 执行 |

当前位置只见下方 Checkpoint；已授权课程与各课阶段见[课程索引](#课程索引)链接的记录。

- Lesson 02 的历史 evidence 只由[冻结记录](lessons/02-fused-softmax.md)承担，本 Program 不复制。
- Lesson 03 的 O4 仅完成了约定的一次 grouped ordering 受控测量；profiler、置信区间、cache 机制深挖
  与穷举调参不属于已关闭 Lesson 的核心范围。

### Checkpoint

| 字段 | 当前值 |
| --- | --- |
| Foreground context | `triton-official-tutorials` Program |
| Semantic position | 第 01–06 课均已关闭；Lesson 06 于 2026-09-24 确认关闭，位于 Lesson 边界，当前没有 active Lesson |
| Next action | 学习者选择并授权下一 Lesson |
| Forward gate | 明确授权后才激活下一 Lesson；当前不会自动启动 Lesson 07 |
| Latest evidence ref | [Lesson 06 Final mastery](lessons/06-fused-attention.md#final-mastery) |
| As of | 2026-09-28；guide-learning 改进已完成，Lesson 06 complete，Program 保持 active |

## 本课程的记录约定

通用的证据、练习、Review 与结课规则见中央 `guide-learning`；本课程另外约定：

- **版本锚点**：源码行为以本仓库固定的教程快照为准，见 `docs/triton-tutorials/SOURCE.md`。
- **结果必须可复现**：实验记录 GPU 型号、驱动、CUDA 与 Triton 版本、输入规模、控制变量、warm-up、
  同步、重复策略和比较基线。
- **性能结论有边界**：不把单台设备上的某个配置、stage 深度或理论 occupancy 泛化为单调规律。
- **按需产物**：`study-log` 的 structured 记录只保留原始回答、误解、纠错、高价值问题和转折；原文只在
  明确要求时保存到 `logs-raw/`。两者都不裁决 Lesson 阶段或结课结论。
