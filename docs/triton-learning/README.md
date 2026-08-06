# Triton 学习档案

本目录用于持续记录基于 `docs/triton-tutorials/official/` 的 Triton 学习过程。目标不只是保存
教程摘要，还要保留理解形成的过程：详细讲解、问题与答疑、实践任务、实验结果、代码评审、
修改记录、错误尝试和最终掌握情况。

## 固定学习闭环

每个官方案例按下面的顺序推进：

1. **课前定位**：明确本课依赖的知识、学习目标和对应的官方源码。
2. **完整讲解**：说明问题背景、PyTorch baseline、Triton kernel、launch grid、数据布局、
   边界处理、正确性验证和 benchmark。
3. **问题与答疑**：记录学习者的原始问题、当时的理解、解释、最小例子和最终结论。
4. **实践任务**：布置一个或多个逐级练习，写清要求、约束、测试数据和验收标准。
5. **自主实现**：代码放在 `gpu/triton/`，学习档案只链接源码、测试和实验结果，不复制一份
   容易失去同步的实现。
6. **代码评审**：检查正确性、边界、可读性、Triton 编程模型、内存访问和性能测量方式，
   每条意见都记录处理结果。
7. **修改与复审**：保留各轮修改的动机和结果，直到没有未解决的阻塞问题。
8. **掌握验收**：能够用自己的话解释核心机制，并独立完成变式后，才将本课标记为完成。
9. **后验对话归档**：在课程结束或中断时，从 Codex session 截取用户与助手可见消息，生成
   独立原始对话档案并由单课主记录链接。

失败的实验和曾经存在的误解也应保留。它们属于学习记录的一部分，不应只留下最终正确答案。

## 目录约定

```text
docs/triton-learning/
├── README.md                         # 总索引、流程和写作约定
├── templates/
│   └── lesson-record.md              # 单课学习记录模板
├── references/
│   ├── pytest-gpu-kernel-tests.md     # Triton GPU 正确性测试参考
│   └── raw-dialogue-export.md         # Codex 原始对话后验导出说明
├── dialogues/
│   ├── 00-learning-workflow.md        # 学习流程建立的原始对话
│   ├── 01-vector-add.md               # 第一课开课至阶段性保存
│   ├── 01-vector-add-part2.md         # 第一课恢复学习至最终复验
│   ├── 01-vector-add-part3.md         # 第一课可选性能扩展至阶段性暂停
│   ├── 01-vector-add-part4.md         # 第一课性能扩展工程收尾
│   ├── 02-fused-softmax.md            # 第二课开课至 P01 实现前暂停
│   ├── 02-fused-softmax-part2.md      # 第二课 P01 实践与三轮评审
│   ├── 02-fused-softmax-part3.md      # 第二课 Persistent、资源与 Benchmark 至结课
│   └── 02-fused-softmax-part4.md      # 第二课结课后 Benchmark 解释补充
├── lessons/
│   ├── 01-vector-add.md              # 每个官方案例一份主记录
│   ├── 02-fused-softmax.md
│   └── ...
└── attachments/                      # 可选的图表、性能数据等补充材料
    └── <课程序号>-<主题>/
```

- 单课主记录统一命名为 `<两位序号>-<英文主题>.md`。
- 实践源码、测试和 benchmark 仍放在 `gpu/triton/`；文档使用相对链接指向它们。
- 少量实验结果直接写入单课记录。只有内容过大或需要机器读取时，才放入 `attachments/`。
- 官方教程快照保持原样，不在 `docs/triton-tutorials/official/` 中写笔记或直接改代码。
- 原始对话统一放在 `dialogues/`，由脚本后验生成；不在其中人工润色、补写结论或删除失败过程。

## 课程索引

状态只使用：`未开始`、`讲解中`、`答疑中`、`实践中`、`评审中`、`待验收`、`已完成`。

| 课次 | 官方案例 | 学习记录 | 状态 |
| --- | --- | --- | --- |
| 01 | `01-vector-add.py` | [lessons/01-vector-add.md](lessons/01-vector-add.md) | 已完成 |
| 02 | `02-fused-softmax.py` | [lessons/02-fused-softmax.md](lessons/02-fused-softmax.md) | 已完成 |
| 03 | `03-matrix-multiplication.py` | `lessons/03-matrix-multiplication.md` | 未开始 |
| 04 | `04-low-memory-dropout.py` | `lessons/04-low-memory-dropout.md` | 未开始 |
| 05 | `05-layer-norm.py` | `lessons/05-layer-norm.md` | 未开始 |
| 06 | `06-fused-attention.py` | `lessons/06-fused-attention.md` | 未开始 |
| 07 | `07-extern-functions.py` | `lessons/07-extern-functions.md` | 未开始 |
| 08 | `08-grouped-gemm.py` | `lessons/08-grouped-gemm.md` | 未开始 |
| 09 | `09-persistent-matmul.py` | `lessons/09-persistent-matmul.md` | 未开始 |
| 10 | `10-block-scaled-matmul.py` | `lessons/10-block-scaled-matmul.md` | 未开始 |

创建新课程记录时，复制 `templates/lesson-record.md`，替换占位内容，并同步更新本表状态。

## 原始对话索引

原始对话只保存用户与助手可见消息；详细规则与命令见
[Codex 学习对话后验归档](references/raw-dialogue-export.md)。

| 编号 | 范围 | 原始对话 | 消息数 | 归档状态 |
| --- | --- | --- | --- | --- |
| 00 | 学习流程建立 | [dialogues/00-learning-workflow.md](dialogues/00-learning-workflow.md) | 4 | 已导出 |
| 01-A | Vector Addition：开课至阶段性保存 | [dialogues/01-vector-add.md](dialogues/01-vector-add.md) | 57 | 已导出 |
| 01-B | Vector Addition：恢复至最终复验 | [dialogues/01-vector-add-part2.md](dialogues/01-vector-add-part2.md) | 37 | 已导出 |
| 01-C | Vector Addition：可选性能扩展至暂停 | [dialogues/01-vector-add-part3.md](dialogues/01-vector-add-part3.md) | 87 | 已导出 |
| 01-D | Vector Addition：性能扩展工程收尾 | [dialogues/01-vector-add-part4.md](dialogues/01-vector-add-part4.md) | 18 | 已导出 |
| 02-A | Fused Softmax：开课至 P01 布置与 Q03 确认 | [dialogues/02-fused-softmax.md](dialogues/02-fused-softmax.md) | 29 | 暂停快照 |
| 02-B | Fused Softmax：P01 实践与三轮评审 | [dialogues/02-fused-softmax-part2.md](dialogues/02-fused-softmax-part2.md) | 32 | 暂停快照 |
| 02-C | Fused Softmax：Persistent、资源与 Benchmark 至结课 | [dialogues/02-fused-softmax-part3.md](dialogues/02-fused-softmax-part3.md) | 153 | 已导出 |
| 02-D | Fused Softmax：结课后 Benchmark 解释 | [dialogues/02-fused-softmax-part4.md](dialogues/02-fused-softmax-part4.md) | 6 | 已导出 |

## 当前学习断点

最近同步时间：2026-08-06。

- 最近完成课程：第 02 课 Fused Softmax；第 01、02 课均已关闭。
- 当前课程：无。下一入口是第 03 课 Matrix Multiplication，尚未开始。
- Lesson 02 成果：完成普通与 persistent row-wise softmax、stages 1/2/4、默认资源 grid、
  compiled resources/理论 occupancy 推导，以及 prepared steady-state wrapper-level benchmark。
- 最终证据：物理 A100 GPU 3 上功能测试 37 passed、benchmark 27 passed；默认 CI 20 passed；
  Ruff、format、BasedPyright、skill validation 与 `git diff --check` 全绿。
- 最终实验：三个 shape × 六条 provider/stage 曲线共 18 行；`N=781` 的 stages 1/2/4 均为
  8 resident programs/SM、100% 理论 occupancy，`N=2049` 则分别为 4/5/3 和 50%/62.5%/37.5%。
  本次 stage 1 均不慢于更深 stages，因此不把 stage 深度或 occupancy 视为单调性能指标。
- 对话归档：Lesson 02-A/B/C/D 分别为 29、32、153、6 条；02-D 单独保留结课后的性能解释，
  没有覆盖已冻结的 02-C。
- 后续性能专题：profiler、置信区间、cache 与 autotune 仅在它们成为核心问题时开展。

## 记录原则

- **区分事实与推断**：源码行为、实测结果和解释性推断分别表述。
- **结果必须可复现**：实验记录命令、输入形状、dtype、GPU、软件版本和关键配置。
- **正确性优先于性能**：先覆盖非整块尺寸、不同 shape 和错误输入，再讨论 benchmark。
- **性能结论必须有边界**：注明 warm-up、重复次数、同步方式和比较基线，避免把 JIT 首次编译
  时间计入稳态执行时间。
- **Benchmark 测试聚焦性能因素**：优先验证计时边界、warm-up、同步、资源配置、工作量口径和
  可复现性；除非参数校验本身是核心学习目标，否则不为 benchmark 设置参数错误路径测试。
- **减少非核心消耗**：文档、测试夹具、格式化和元数据只保留支撑掌握结论所需的最小范围；
  安全的例行工作由 AI 处理或明确推迟，不扩张学习者任务。
- **评审意见可追踪**：每条意见有编号、严重程度、处理方式和最终状态。
- **完成意味着能迁移**：不以“代码跑通”作为唯一标准，还要能解释原因并完成相关变式。
- **总结与原始材料分层**：主记录可以纠错和提炼，原始对话只按声明的过滤规则生成并保留
  provenance，二者互相链接但不互相覆盖。
