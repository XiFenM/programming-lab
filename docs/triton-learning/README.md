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
│   └── 01-vector-add.md               # 第一课原始对话
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
| 01 | `01-vector-add.py` | [lessons/01-vector-add.md](lessons/01-vector-add.md) | 评审中 |
| 02 | `02-fused-softmax.py` | `lessons/02-fused-softmax.md` | 未开始 |
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
| 01 | Vector Addition | [dialogues/01-vector-add.md](dialogues/01-vector-add.md) | 57 | 阶段性已导出 |

## 当前学习断点

阶段性保存时间：2026-07-20。

- 当前课程：第 01 课 Vector Addition。
- 当前阶段：第三轮代码评审之后，状态为 `评审中`，尚未进入最终验收。
- 当前成果：两个练习 kernel 与 wrapper 已完成；pytest 已建立，现有 20 个用例全部通过。
- 对话归档：学习流程建立与第一课截至 2026-07-20 09:14 UTC 的原始可见对话已后验导出；
  当前新增归档功能的元对话不属于第一课文件。
- 整理状态：旧练习 `strided_1d_vector_add` 已从独立文件归并到第一课实践源码；目前只有 kernel，
  尚无 wrapper、pytest 或正式评审，不计入第一课已验收成果。
- 当前遗留：R08/R09 的核心实现已经手工复验，仍需通过 R10 将多 GPU、block-size 类型与验证
  顺序等行为固化为 pytest，并改善跨卡错误消息；R07 的 Ruff/formatter 尚未完成。
- 恢复入口：阅读[第一课“阶段性暂停快照”](lessons/01-vector-add.md#11-阶段性暂停快照2026-07-20)，
  然后从其中的“下一步执行顺序”继续。
- 推进约束：关闭阻塞项、补齐测试并完成概念验收之前，不进入第 02 课。

## 记录原则

- **区分事实与推断**：源码行为、实测结果和解释性推断分别表述。
- **结果必须可复现**：实验记录命令、输入形状、dtype、GPU、软件版本和关键配置。
- **正确性优先于性能**：先覆盖非整块尺寸、不同 shape 和错误输入，再讨论 benchmark。
- **性能结论必须有边界**：注明 warm-up、重复次数、同步方式和比较基线，避免把 JIT 首次编译
  时间计入稳态执行时间。
- **评审意见可追踪**：每条意见有编号、严重程度、处理方式和最终状态。
- **完成意味着能迁移**：不以“代码跑通”作为唯一标准，还要能解释原因并完成相关变式。
- **总结与原始材料分层**：主记录可以纠错和提炼，原始对话只按声明的过滤规则生成并保留
  provenance，二者互相链接但不互相覆盖。
