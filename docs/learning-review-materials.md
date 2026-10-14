# 学习复盘材料索引

整理与核对日期：2026-09-14；2026-10-05 补入 Triton 第 06、07 课，2026-10-09 补入第 08 课，2026-10-14 补入 Rust 第 01、02 课与 Triton 第 09 课，此前各行未重新核对。
本页索引已经完成课程的复盘材料及可恢复来源，
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
| Triton 06：Fused Attention | [9 月 14–19 日](triton-learning/logs/2026-09-19-fused-attention.md)、[9 月 20–24 日全貌补充与 FP16 前向实践](triton-learning/logs/2026-09-24-fused-attention.md) | 9 月 14–19 日未保存原文；[9 月 20–24 日 120 条](triton-learning/logs-raw/2026-09-24-fused-attention.md) | [34 张，3 个 XLSX](triton-learning/cards/triton-lesson-06-fused-attention.md)，覆盖两份日志 |
| Triton 07：外部函数（libdevice） | [9 月 30 日–10 月 5 日](triton-learning/logs/2026-10-05-extern-functions.md) | [开课到确认结课 90 条](triton-learning/logs-raw/2026-10-05-extern-functions.md) | [25 张，3 个 XLSX](triton-learning/cards/triton-lesson-07-extern-functions.md) |
| Triton 08：Grouped GEMM | [10 月 5–9 日](triton-learning/logs/2026-10-09-grouped-gemm.md) | [开课到确认结课 82 条](triton-learning/logs-raw/2026-10-09-grouped-gemm.md) | [34 张，3 个 XLSX](triton-learning/cards/triton-lesson-08-grouped-gemm.md) |
| Triton 09：持久化矩阵乘 | [10 月 10–14 日](triton-learning/logs/2026-10-14-persistent-matmul.md) | [开课到确认结课 161 条](triton-learning/logs-raw/2026-10-14-persistent-matmul.md) | [39 张，3 个 XLSX](triton-learning/cards/triton-lesson-09-persistent-matmul.md) |
| Rust 01：第一个程序与格式化输出 | [10 月 7–8 日，补整理](rust-learning/logs/2026-10-08-hello-formatting.md) | [开课到结课后的反馈 32 条](rust-learning/logs-raw/2026-10-08-hello-formatting.md) | [21 张，3 个 XLSX](rust-learning/cards/rust-lesson-01-hello-formatting.md) |
| Rust 02：数据的形状 | [10 月 8–14 日](rust-learning/logs/2026-10-14-data-shapes.md) | [开课到确认结课 94 条](rust-learning/logs-raw/2026-10-14-data-shapes.md) | [42 张，3 个 XLSX](rust-learning/cards/rust-lesson-02-data-shapes.md) |

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
| Triton 06：全貌补充与 FP16 前向实践 | [2026-09-24](triton-learning/logs-raw/2026-09-24-fused-attention.md) | 120 |
| Triton 07：开课至确认结课 | [2026-10-05](triton-learning/logs-raw/2026-10-05-extern-functions.md) | 90 |
| Triton 08：开课至确认结课 | [2026-10-09](triton-learning/logs-raw/2026-10-09-grouped-gemm.md) | 82 |
| Triton 09：开课至确认结课 | [2026-10-14](triton-learning/logs-raw/2026-10-14-persistent-matmul.md) | 161 |
| Rust 01：开课至结课后的两点反馈 | [2026-10-08](rust-learning/logs-raw/2026-10-08-hello-formatting.md) | 32 |
| Rust 02：开课至确认结课 | [2026-10-14](rust-learning/logs-raw/2026-10-14-data-shapes.md) | 94 |

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

第 06、07 课的原文采用现行配对规则：由 `study_log.py` 直接生成在 `logs-raw/`，与结构化日志同名
并互相链接，状态为 `final`，元数据同样带有 source SHA-256、可见内容摘要、稳定消息 ID 和起止边界。
第 06 课较早的 9 月 14–19 日日志没有配对原文。第 07 课的原文由两段连续范围合并而成：复查题的
第一次回复已被学习者重发后的回复取代，按学习者要求略去，各段来源与校验值记录在该文件的元数据中。

第 07 课原文扫描未发现凭据或个人标识；`proprietary` 类别命中 13 条，来自 Triton 开源代码和本仓库
练习代码块。原文按确认保留本机路径、容器内路径和图解页的私有链接，未做手工润色或脱敏。
`logs-raw/` 下日期命名的原文同样保留原消息的行尾空格，`.gitattributes` 对它们也关闭了行尾空格告警。

第 08 课的原文同样由 `study_log.py` 直接生成在 `logs-raw/`，与结构化日志同名并互相链接，状态为 `final`，
是一段连续范围，其中 4 条是客户端命令留下的记录。扫描未发现凭据或个人标识；`proprietary` 类别命中 22 处，
分布在 14 条消息里，来自 Triton 开源代码和本仓库的练习、测试代码。原文按学习者确认保留 GPU 机器的容器主机名、
其上的绝对路径和图解页的私有链接，未做手工润色或脱敏。

第 09 课的原文同样由 `study_log.py` 直接生成在 `logs-raw/`，与结构化日志同名并互相链接，状态为 `final`，是一段连续范围，其中 5 条是客户端留下的记录（2 条 `/compact`、2 条中断、1 条图解页订阅通知）。提取用的是对进行中的会话文件所做的快照，快照在使用后删除。扫描未发现凭据或个人标识；`proprietary` 类别命中 27 处，分布在 19 条消息里，来自 Triton 开源代码，以及本仓库的练习、测试代码和编译出的 IR、PTX。原文按学习者确认保留本机仓库路径、GPU 机器的容器主机名及其上的绝对路径和图解页的私有链接，未做手工润色或脱敏。

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

## 2026-09-24 Fused Attention 记录与卡片（2026-10-05 补登记）

第 06 课有两份结构化日志：9 月 14–19 日一份 19 条，9 月 20–24 日一份 57 条；后者与 120 条可见消息的
同名原文配对。根据这两份受管日志精选 34 张卡片：29 张技术问答、3 张真实纠错、2 张综合口述，
31 张为 A、3 张为 B，全部使用模板 `1.1.0`。

仓库内没有该课上传过程的记录。2026-10-05 只读查询时，私有牌库 `Triton` 的 `Triton 06` 章节有
34 张卡，且仅出现语法版本 3。

## 2026-10-05 外部函数记录、卡片与 Markji 上传

第 07 课结构化日志从当次会话的指定范围蒸馏，保留 45 条：28 条要点、6 条纠错、6 条转折、3 条高价值
问题和 2 条遗留，各条目共引用 27 个稳定消息 ID 供回查。临时提取正文在蒸馏后删除。

根据该受管日志精选 25 张卡片：18 张技术问答、5 张真实纠错、2 张综合口述，18 张为 A、7 张为 B。
覆盖接口模块替换与 dtype 查表、链接与内联、数值模式与次正规数、`tl.math` 与 libdevice 的区别、
快速档与精确档、新后端适配、跨厂商差异，以及练习中的真实错误。两条遗留（速度与误差未实测、
AMD 未在真机运行）不制卡。跨既有 inventory 未发现重复、冲突、依赖漂移或暂缓项；Markdown 与
3 个 XLSX 以相同 request 复核为 `no-op`、`would_write=false`。

随后按学习者明确请求，通过墨墨官方 API 上传到私有牌库 `Triton` 的 `Triton 07` 章节。上传预览确认
空章节中 25 张均为 `create`，使用从 `Triton 06` 章节既有卡片核实的 `grammar_version=3`；实际结果为
新增 25 张、跳过 0 张。每张卡均完成完整内容、语法版本和章节归属的独立读回验证，最终章节包含
25 张卡且仅出现语法版本 3，再次预览时 25 张均为 `skip`。恢复回执保存在仓库外，不含 token 或
卡片全文；API 验证不代替客户端视觉渲染检查。

## 2026-10-09 Grouped GEMM 记录与卡片

第 08 课结构化日志从当次会话的指定范围蒸馏，保留 82 条：42 条要点、19 条纠错、9 条转折、9 条高价值
问题和 3 条遗留，各条目共引用 59 个稳定消息 ID 供回查；学习者的原话逐句与提取正文核对。临时提取正文
在蒸馏后删除。同名原文为 82 条可见消息，配对校验通过。

根据该受管日志精选 34 张卡片：21 张技术问答、10 张真实纠错、3 张综合口述，24 张为 A、10 张为 B。
覆盖三种做法的取舍、地址表与偏移表、静态步长调度与块大小、三个方向的越界与保护区测试、对齐保证与
降档、TMA 描述符与回退、转置与补齐、真实 MoE 规模下的落点、新后端迁移，以及练习和 A6 中的真实错误。
三条遗留不制卡；`continue` 与 mask 括号两条会直接得到明确的编译报错，评为 C，没有制卡。跨既有
inventory 未发现重复、冲突、依赖漂移或暂缓项；Markdown 与 3 个 XLSX 以相同 request 复核为 `no-op`、
`would_write=false`。本次只生成本地卡片和阅读版预览，没有上传到墨墨；2026-10-14 补传，见文末。

## 2026-10-14 Rust 第 01、02 课记录与卡片

Rust 课程的日志与卡片目录在这一次第一次用到时登记进 `study-log` 与 `memo-cards` 的配置：结构化记录在
`rust-learning/logs/`，同名原文在 `rust-learning/logs-raw/`，卡片在 `rust-learning/cards/`。两课都在同一个
会话 `claude:a955cb4c` 里进行，提取用的是对进行中的会话文件所做的同一个快照。

第 01 课在 10 月 8 日结课时没有整理记录，这次补整理。结构化日志保留 61 条：41 条要点、6 条纠错、7 条转折、
1 条高价值问题和 6 条遗留。范围从开课到学习者结课后的两点反馈及其回复：反馈改变了此后的讲法（先指路、名词
渐进引入），回复里补上了第 01 课的阅读指引和名词解释。两课之间改 Skill、建名词表和处理 PlanA 的对话不在范围内。
第 02 课结构化日志保留 133 条：89 条要点、13 条纠错、8 条转折、15 条高价值问题和 8 条遗留，止于确认结课的
回复，提交和整理记录的对话不在范围内。两份日志引用的消息 ID 都在各自范围内，学习者的原话与提取正文逐句核对；
临时提取正文在蒸馏后删除。

两份原文都是 `final`，各为一段连续范围，配对校验通过。扫描没有发现凭据或个人标识；`proprietary` 类别分别
命中 49 和 65 处，都是代码块，来自 Rust by Example、Rust 标准库、`safetensors`、`ROCm/ATOM`、`AMD-AGI/Infera`
这几个公开仓库，以及本仓库的练习与测试代码。原文按学习者确认保留编辑器提示里的本机路径、第 02 课里贴出的
一段终端输出中的主机名、三个图解页的私有链接、1 条客户端额度提示和 1 条 `/compact` 记录，未做手工润色或脱敏。
`.gitattributes` 对 `rust-learning/logs-raw/` 下日期命名的原文同样关闭了行尾空格告警。

根据两份受管日志精选 63 张卡片。第 01 课 21 张：14 张技术问答、5 张真实纠错、2 张综合口述，14 张为 A、7 张为 B；
覆盖 `println!` 为什么是宏、与 `printf` 的取舍、`Display` 与 `Debug`、`fmt` 往 `Formatter` 里写、宽度怎样生效、
写失败 panic 与全局锁，以及孤儿规则、`let _ =` 吞掉错误等真实错误。第 02 课 42 张：29 张技术问答、10 张真实纠错、
3 张综合口述，31 张为 A、11 张为 B；覆盖数值转换与溢出、切片与胖指针、struct 布局、enum 的布局与模式、`Box`、
`const` 与 `static`、引用与 `*`、移动与 `Copy`，以及练习和综合验收里的真实错误。遗留和只是推断的结论没有制卡；一次性的
细节（如 `hello` 的体积、`if` 的写法、`{:02X}` 补零）评为 C。`#[non_exhaustive]` 只并进了下划线兜底那张卡的
边界；字段私有与构造校验、类型别名与 newtype、教程链表的实际问题、先乘位数再除以 8 的纠错这几项暂缓。跨既有 inventory 未发现重复、冲突或依赖漂移；两套卡片的 Markdown 与各 3 个 XLSX 以相同
request 复核为 `no-op`、`would_write=false`。阅读版预览在 [Rust 复习卡片预览](rust-learning/cards/previews/README.md)。

随后按学习者的明确请求，通过墨墨官方 API 上传到学习者新建的私有牌组 `Rust`，按课分章节：

| 牌库 | 章节 | 新增卡片 |
| --- | --- | ---: |
| Rust | 字符串格式化（第 01 课） | 21 |
| Rust | 数据类型（第 02 课） | 42 |

上传预览确认两个章节都是空的，63 张均为 `create`；语法版本取自同账号已上传的 `Triton 07` 章节，为 3。实际结果为
新增 63 张、跳过 0 张，每张卡均完成完整内容、语法版本和章节归属的读回验证；随后独立只读核对，两个章节分别
恰好包含这 21 张和 42 张卡，且只出现语法版本 3。恢复回执保存在仓库外，不含 token 或卡片全文；API 验证不代替
客户端视觉渲染检查。

## 2026-10-14 持久化矩阵乘记录与卡片

第 09 课结构化日志从当次会话的指定范围蒸馏，保留 61 条：14 条要点、21 条纠错、10 条转折、11 条高价值问题和 5 条遗留，各条目共引用 97 个稳定消息 ID 供回查；学习者的原话逐句与提取正文核对。临时提取正文在蒸馏后删除。同名原文为 161 条可见消息，配对校验通过。

根据该受管日志精选 39 张卡片：20 张技术问答、15 张真实纠错、4 张综合口述，31 张为 A、8 张为 B。覆盖持久化省掉什么、`flatten` 的收益代价与确认方法、搬运与计算在四代目标上的分工与 warp 专用化、越界下标的处理、行主序 B 在循环合并后保住异步拷贝与提前量、下标的取值连续与两条声明、整数参数的特化、受控测量的设计与解释，以及练习、M1 和 A6 中的真实错误。五条遗留不制卡；Hopper 专用化遇到带 else 的分支即放弃这一实现细节、TMA 不能读 TMEM、“tflop16/s 三样东西”的数错评为 C，没有制卡。跨既有 inventory 未发现重复、冲突、依赖漂移或暂缓项；Markdown 与 3 个 XLSX 以相同 request 复核为 `no-op`、`would_write=false`。阅读版预览已加入[Triton 复习卡片预览](triton-learning/cards/previews/README.md)。生成时只有本地卡片，随后按学习者的明确请求上传到墨墨，见下一节。

## 2026-10-14 Triton 第 08、09 课 Markji 上传

按学习者的明确请求，通过墨墨官方 API 上传到私有牌库 `Triton`，每课一个章节。第 09 课是学习者直接指定的目标；第 08 课在10 月 9 日结课时只生成了本地卡片，这次经学习者确认补传。

| 牌库 | 章节 | 新增卡片 |
| --- | --- | ---: |
| Triton | Triton 08 | 34 |
| Triton | Triton 09 | 39 |

上传前两套卡片的本地产物都以原 request 复核为 `no-op`、`would_write=false`；两个章节都是空的，预览中 34 张与 39 张均为 `create`。语法版本取自同牌库已上传 25 张卡的 `Triton 07` 章节，为 3。实际结果为新增 73 张、跳过 0 张，每张卡均完成完整内容、语法版本和章节归属的读回验证；随后独立只读核对，两个章节分别恰好包含这 34 张和 39 张卡，且只出现语法版本 3，再次预览时全部为 `skip`。恢复回执保存在仓库外，不含 token 或卡片全文；API 验证不代替客户端视觉渲染检查。
