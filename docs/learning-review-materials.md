# 学习复盘材料索引

整理与核对日期：2026-09-14。本页索引已经完成课程的复盘材料及可恢复来源，
不裁决课程进度或掌握程度；课程状态仍以各轨道的 Program 和 Lesson 为准。

## 材料覆盖

| 课程 | 结构化学习日志 | 可追溯可见对话 | 本地复习卡片 |
| --- | --- | --- | --- |
| 算法面试 01：约束驱动的算法选择 | [8 月 15 日](algorithm-interview-learning/logs/2026-08-15-lesson-01-constraint-driven-selection.md) | 本机未找到该课原会话或已保存全文；保留日志已有来源标识 | [9 张，3 个 XLSX](algorithm-interview-learning/cards/algorithm-interview-lesson-01-constraint-driven-selection.md) |
| Triton 01：向量运算与基础 Benchmark | [7 月 20–27 日，补整理](triton-learning/logs/2026-07-27-vector-add.md) | 4 段 frozen legacy，共 199 条，见下方索引 | [15 张，3 个 XLSX](triton-learning/cards/triton-lesson-01-vector-add.md) |
| Triton 02：Fused Softmax | [7 月 31 日–8 月 7 日，补整理](triton-learning/logs/2026-08-07-fused-softmax.md) | 5 段 frozen legacy，共 229 条，见下方索引 | [17 张，3 个 XLSX](triton-learning/cards/triton-lesson-02-fused-softmax.md) |
| Triton 03：矩阵乘法 | [8 月 17 日概念学习](triton-learning/logs/2026-08-17-matrix-multiplication.md)、[8 月 18–19 日综合验收与实践](triton-learning/logs/2026-08-19-matrix-multiplication.md) | 本机恢复 8 月 18 日 14 条与 8 月 19 日 37 条；8 月 17 日全文未找到 | [12 张，3 个 XLSX](triton-learning/cards/triton-lesson-03-matrix-multiplication.md)，覆盖两份日志 |
| Triton 04：Low-Memory Dropout | [8 月 24 日](triton-learning/logs/2026-08-24-low-memory-dropout.md) | 本机恢复开课到关闭的 62 条可见消息 | [10 张，3 个 XLSX](triton-learning/cards/triton-lesson-04-low-memory-dropout.md) |
| Triton 05：LayerNorm | [9 月 9–14 日](triton-learning/logs/2026-09-14-layer-norm.md) | [学习与实践 111 条](triton-learning/transcripts/2026-09-09-layer-norm-learning.md)、[复验与结课 14 条](triton-learning/transcripts/2026-09-14-layer-norm-review-and-closure.md) | [16 张，3 个 XLSX](triton-learning/cards/triton-lesson-05-layer-norm.md) |

新增两份结构化日志从已保存的课程对话蒸馏，保留真实回答、误解、纠错、关键问题与转折，
并标注补整理日期及原有消息位置。现有日志中的历史遗留按当时语境阅读；例如 8 月 17 日
矩阵乘法日志的待完成事项已有后续记录，不表示该课现在仍未结束。

## 已保存的可见对话

| 课程片段 | 文件 | 可见消息数 |
| --- | --- | ---: |
| Triton 01：开课与第一轮实践 | [01-A](triton-learning/dialogues/01-vector-add.md) | 57 |
| Triton 01：恢复与最终复验 | [01-B](triton-learning/dialogues/01-vector-add-part2.md) | 37 |
| Triton 01：可选性能实验 | [01-C](triton-learning/dialogues/01-vector-add-part3.md) | 87 |
| Triton 01：性能扩展工程收尾 | [01-D](triton-learning/dialogues/01-vector-add-part4.md) | 18 |
| Triton 02：开课与概念答疑 | [02-A](triton-learning/dialogues/02-fused-softmax.md) | 29 |
| Triton 02：普通 softmax 实践 | [02-B](triton-learning/dialogues/02-fused-softmax-part2.md) | 32 |
| Triton 02：Persistent、资源与 benchmark | [02-C](triton-learning/dialogues/02-fused-softmax-part3.md) | 153 |
| Triton 02：Benchmark 解释补充 | [02-D](triton-learning/dialogues/02-fused-softmax-part4.md) | 6 |
| Triton 02：Log-softmax 快速回顾 | [02-E](triton-learning/dialogues/02-fused-softmax-part5.md) | 9 |
| Triton 03：综合验收与实践范围校准 | [2026-08-18](triton-learning/transcripts/2026-08-18-matrix-multiplication-synthesis.md) | 14 |
| Triton 03：编程实践、实验解释与结课 | [2026-08-19](triton-learning/transcripts/2026-08-19-matrix-multiplication-practice.md) | 37 |
| Triton 04：开课至关闭 | [2026-08-24](triton-learning/transcripts/2026-08-24-low-memory-dropout.md) | 62 |
| Triton 05：学习、概念、实现与首轮 Review | [2026-09-09](triton-learning/transcripts/2026-09-09-layer-norm-learning.md) | 111 |
| Triton 05：精度解释、最终复验与结课确认 | [2026-09-14](triton-learning/transcripts/2026-09-14-layer-norm-review-and-closure.md) | 14 |

第 01、02 课的九段旧对话保持原样。已核对消息计数、编号、时间顺序和分段边界；
它们使用旧格式，不将其解释为现行 raw schema，也不单凭分段连续性声明原会话没有遗漏。

日期命名的归档均由官方 `study_log.py archive` 在仓库外生成，再按学习者对具体边界与风险的明确
授权逐字节导入 `transcripts/` 并加入 Git 跟踪。它们是所选课程片段的 `final` 快照，含 source
SHA-256、可见内容摘要、稳定消息 ID、起止边界和归档身份；`final` 表示该片段已定稿，不代表未选
边界或其他机器上的内容已经恢复。第 05 课在客户端续接处重复出现的同一回答只保留后段副本。

可见对话含用户与助手的过程更新和正式回答；没有收录 system、developer、隐藏推理、工具事件
或附件正文。原有本机路径、容器名和附件描述仍可见。该批次入库是本次明确授权的结果，
不更改 `study-log` 对未来归档的默认位置与范围规则。

第 05 课两段全文扫描未发现凭据或个人标识；`proprietary` 类别命中分别为 30 和 2，均来自本仓库
练习代码块及本机路径。归档按确认保留这些内容，未做手工润色或脱敏。

归档正文保留原消息的 Markdown 行尾换行空格和终端输出空格；`.gitattributes` 仅对日期命名的
这些全文快照关闭行尾空格告警，正文与可见内容摘要仍按原样核对。

## 历史消息锚点恢复

第 03、04 课两份既有日志中的 27 个旧消息 ID 已全部对应到当前可读消息，详见
[消息定位表](triton-learning/transcripts/message-id-map.md)。表中保留旧 ID、当前 ID、
归档消息序号与核对依据，既有日志和卡片来源内容摘要保持不变。

第 03 课的 8 月 19 日日志包含 8 月 18 日内容，需结合两个归档阅读。第 04 课旧日志的终点
是用户确认关闭（第 59 条）；本次全文还包含随后三条助手关闭执行与确认。

## 来源边界与制卡范围

- 算法面试 01 的 `codex:019ffe56` 与 Triton 03 早期的 `codex:01a00da2` 在本机未找到可用
  原会话或单独归档。按学习者选择不再追补其他机器；现有结构化日志继续作为已保存来源使用。
- 卡片直接来源仅为受管结构化日志。对话全文与消息定位表用于追溯，不直接作为制卡 request 的素材。
- 本批采用精选：优先保留反复使用的概念、真实误解与迁移边界。未确定的计时量化成因、未开展的
  profiler／固定 grid 研究及其他遗留问题不制成确定事实卡；绘图配置和一次性工程收尾等低频内容暂缓。

## 2026-09-09 卡片审核与优化

五套卡片共 63 张、15 个 XLSX，全部使用当前 registry／模板 `1.1.0`。原有 24 张保留逻辑身份，
优化短题面、结论／要点／边界层次及评分锚点；新增 39 张补齐向量运算、Softmax、矩阵乘法概念
和 Dropout 的实际纠错。重复的有效 GB/s 方法卡集中在第 01 课，不跨课复制。

审核中将缺少直接错误原话支撑的算法卡改为问答；Dropout 复现卡补齐固定 `p` 的条件；
尾部复合问题按机制链组织；矩阵乘法口述卡保持常青机制范围。更新子卡后，对依赖它们的
机制卡和口述卡完成复核并恢复 `active`，没有遗留的 `review` 卡。

受管文件、来源摘要和工作簿行映射校验通过；每套卡片以同一 request 验证为 `no-op`、
`would_write=false`。

## 2026-09-09 Markji 上传

按学习者指定的两个私有自建牌库上传，共新增 63 张、跳过 0 张。每张卡均完成完整内容、
语法版本及章节归属的读回校验。

| 牌库 | 章节 | 新增卡片 |
| --- | --- | ---: |
| LeetCode算法面试 | 算法面试 01 | 9 |
| Triton | Triton 01 | 15 |
| Triton | Triton 02 | 17 |
| Triton | Triton 03 | 12 |
| Triton | Triton 04 | 10 |

上传使用从同账号既有正常卡片核实的 `grammar_version=3`。恢复与去重回执由上传器保存在
仓库外；本仓库不保存凭据或私有回执。API 读回校验不包含客户端视觉渲染检查。

## 2026-09-14 LayerNorm 记录与卡片

第 05 课结构化日志从上述两个已确认的可见对话片段蒸馏，保留 21 条真实回答、误解、纠错、
高价值问题、转折与验证边界，并以 56 个稳定消息 ID 回查提取材料。临时提取正文在蒸馏后删除。

根据该受管日志精选 16 张卡片：13 张技术问答、2 张真实纠错、1 张综合口述。覆盖逐行映射、
padding、前后向梯度、共享分组、CAS／barrier／release-acquire、wrapper 契约和数值精度；一张固定
版本的生产实现策略卡标为 B，其余为 A。跨既有 inventory 未发现重复、冲突、依赖漂移或暂缓项。
Markdown 与 3 个 XLSX 以相同 request 复核为 `no-op`、`would_write=false`。本次只生成本地卡片，
随后按学习者明确请求，通过墨墨官方 API 上传到私有牌库 `Triton` 的 `Triton 05` 章节。

上传预览确认空章节中 16 张均为 `create`，使用从既有正常卡片核实的 `grammar_version=3`；实际结果为
新增 16 张、跳过 0 张。每张卡均完成完整内容、语法版本和章节归属的独立读回验证，最终章节包含
16 张卡且仅出现语法版本 3。恢复回执保存在仓库外，不含 token 或卡片全文；API 验证不代替客户端
视觉渲染检查。
