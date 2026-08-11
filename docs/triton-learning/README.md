# Triton 学习档案

本目录持续记录基于 `docs/triton-tutorials/official/` 的 Triton 学习。第 01、02 课及其对话由旧流程
形成，现作为冻结的 legacy evidence 保留；从第 03 课起，新会话采用中央 `guide-learning` 的自适应
教学、证据门槛和稀疏状态规则。

## 活动学习流程

结构化主题先给一张很短的全局图，再围绕每个关键节点循环：

1. 详细讲清当前节点的中心关系、机制和边界。
2. 留出追问，并只做服务当前节点的必要扩展。
3. 检查刚讲过或已确认的前置知识，不要求猜测尚未教授的事实。
4. 理解有差距时只补差值，并换条件、例子或问法复查；理解无误时直接推进。
5. 完成一次轻量复述、举例、自测、映射或推导，并即时校正。

所有关键节点覆盖后，先合成完整心智模型并做跨节点综合验收。只有 required mastery 仍缺实践、迁移
或实证证据时，才提出能补齐缺口的最小正式练习。正式练习必须先展示并接受完整契约；学习者拥有核心
工件，Agent 只维护契约内的测试、rubric、fixture 和记录。结课必须展示“目标 × required 维度”证据，
并由学习者确认关闭；不会自动启动下一课或 optional 内容。

普通讲解、追问、正确回答和节点推进不逐轮写入。只在正式练习获接受、核心工件提交、durable finding、
验证或 mastery 判断改变、跨会话恢复点改变、暂停／收工或确认关闭等耐久事实变化时按需同步。

## 状态职责

- 本 README 的课程索引承担 Triton Program 的长期范围、候选顺序和当前前台引用；不复制 Lesson 证据。
- `lessons/<NN>-<topic>.md` 是对应 Lesson 的唯一 evidence ledger；只保存来源、目标、required mastery、
  当前阶段和实际发生的契约、finding、assistance、event 与 final mastery。
- Session event 每个有实质增量的会话段最多一条，不保存精确恢复游标。
- 只有确实存在恢复任务时才建立一个可覆盖 Checkpoint；它只保存精确语义位置、唯一下一动作、前进
  门槛和必要引用，不累积历史快照。
- 文章、结构化过程记录、卡片和原始对话均为按需产物，不是 Program、Lesson 或 Checkpoint 的事实源。

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

## 课程索引

第 01、02 课的“已完成”沿用历史终态。从第 03 课起，候选顺序不构成启动授权；只有学习者明确开始
某课后，才创建或激活对应 Lesson，并使用 `teaching`、`synthesis`、`practice`、`review`、
`mastery-gate`、`complete` 阶段。

| 课次 | 官方案例 | 学习记录 | 状态 |
| --- | --- | --- | --- |
| 01 | `01-vector-add.py` | [lessons/01-vector-add.md](lessons/01-vector-add.md) | 已完成（legacy） |
| 02 | `02-fused-softmax.py` | [lessons/02-fused-softmax.md](lessons/02-fused-softmax.md) | 已完成（legacy） |
| 03 | `03-matrix-multiplication.py` | `lessons/03-matrix-multiplication.md` | 候选（未授权） |
| 04 | `04-low-memory-dropout.py` | `lessons/04-low-memory-dropout.md` | 候选（未授权） |
| 05 | `05-layer-norm.py` | `lessons/05-layer-norm.md` | 候选（未授权） |
| 06 | `06-fused-attention.py` | `lessons/06-fused-attention.md` | 候选（未授权） |
| 07 | `07-extern-functions.py` | `lessons/07-extern-functions.md` | 候选（未授权） |
| 08 | `08-grouped-gemm.py` | `lessons/08-grouped-gemm.md` | 候选（未授权） |
| 09 | `09-persistent-matmul.py` | `lessons/09-persistent-matmul.md` | 候选（未授权） |
| 10 | `10-block-scaled-matmul.py` | `lessons/10-block-scaled-matmul.md` | 候选（未授权） |

获得新 Lesson 授权后，才以 `templates/lesson-record.md` 的“核心记录”为基础创建文件；条件片段只在
对应事实实际发生时追加。不要整份复制出空章节，也不要因为候选顺序自动开始第 03 课。

## Legacy 对话索引

以下文件是旧流程生成的可见文本快照，保留其旧 Skill 名称、路径和正文，不再刷新或覆盖。现行 raw
归档由 `study-log` 在用户明确请求并确认边界、隐私和仓库外私有位置后生成；规则见
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

最近迁移核对：2026-08-11。

| 字段 | 当前值 |
| --- | --- |
| Program ID / 标题 | `triton-official-tutorials` / Triton 官方教程学习 |
| State | `active` |
| Objective | 理解、实现并验证本仓库固定版本的 Triton 官方教程 |
| Included | 官方案例的概念、实现、正确性与目标明确时的实证验证 |
| Excluded | 未获授权的独立性能研究、optional extension 与下一 Lesson 执行 |
| Authorized Lesson refs | `lessons/01-vector-add.md`、`lessons/02-fused-softmax.md`（均为已关闭 legacy） |
| Active Lesson ref | 无 |
| Checkpoint ref | [下方唯一 Checkpoint](#checkpoint) |

- 第 01、02 课均已关闭；当前没有 active Lesson。
- 第 03 课 Matrix Multiplication 是下一候选入口，但尚未获得启动授权。
- Lesson 02 的历史 evidence 只由[冻结记录](lessons/02-fused-softmax.md)承担，本 Program 不复制。
- profiler、置信区间、cache 与 autotune 只有在成为新的核心目标并取得授权后，才进入后续 Lesson。

### Checkpoint

| 字段 | 当前值 |
| --- | --- |
| Foreground context | `triton-official-tutorials` Program |
| Semantic position | Lesson 02 已关闭；停在下一 Lesson 授权边界 |
| Next action | 等待学习者明确授权启动一个候选 Lesson |
| Forward gate | 学习者确认目标、范围与 required mastery 维度 |
| Blockers | 无 |
| Latest evidence ref | `lessons/02-fused-softmax.md` |
| As of | 2026-08-11；随本次 M3 语义迁移更新 |

## 记录原则

- **区分事实与推断**：源码行为、实测结果和解释性推断分别表述并给出版本锚点。
- **按目标声明证据**：每项目标在激活时声明 conceptual、practical、empirical 为 `required` 或
  `not-required`，不得在结课时临时改变。
- **正式练习只补证据缺口**：综合验收已经足够时跳过；需要时先接受六块契约，再创建验收工件。
- **核心工件归学习者**：Agent 不因验证失败自动接管；material assistance 只撤销受影响范围的独立
  evidence，并用无提示同构变式恢复。
- **finding 原地更新**：同一根因只保留一个稳定 finding；required blocking／major 关闭后停止正式
  Review，minor／suggestion 默认不阻塞。
- **结果必须可复现**：实验记录环境、版本、输入、控制变量、warm-up、同步、重复策略和比较基线。
- **性能结论有边界**：不把单台设备上的某个配置、stage 深度或理论 occupancy 泛化为单调规律。
- **按需分层产物**：`study-log` 的 structured 记录只保留原始回答、误解、纠错、高价值问题和转折；
  raw 需要单独确认且默认位于 Git 工作树外。两者都不裁决 Lesson stage 或 mastery。
