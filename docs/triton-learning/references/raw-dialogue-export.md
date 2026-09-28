# Study Log 与 legacy 学习对话

第 01、02 课的 `docs/triton-learning/dialogues/*.md` 由旧 exporter 生成，现作为冻结的 legacy evidence
保留；`transcripts/` 中是同名配对规则启用前保存的可追溯可见对话。两者都不要刷新、覆盖、重新格式化或
批量替换其中的旧 Skill 名称、旧路径和历史命令。

学习对话的发现、整理与归档由中央 `study-log` 负责，行为以生成 Skill 自带的说明为准；本页只记录本仓库的
路径约定。用户用自然语言说明目标即可，不需要记忆脚本命令。

| 产物 | 何时生成 | 位置 | 是否属于 Lesson 状态 |
| --- | --- | --- | --- |
| 结构化记录 | 默认：整理学习记录、提取纠错或高价值问答、准备制卡素材 | `logs/<日期>-<主题>.md` | 否 |
| 可追溯可见文本对话 | 仅在用户明确要求保存原文（审计、研究或回查原话）时 | `logs-raw/` 下与结构化记录同名的文件 | 否 |

用户只说“保存这段对话”时，先确认要结构化记录还是原文；整理学习记录不会附带保存原文，也不会自动提议
保存原文。

## 结构化记录

- 只使用用户指定或当前任务直接相关的会话；有多个合理会话或主题边界时先确认。
- 保留学习者的原始回答、误解、纠错、高价值问题和关键转折；Lesson 或文章已记录的结论只链接，不复制
  教学正文、Lesson 阶段、Checkpoint 或结课结论。每条两到四句为宜。
- 临时材料由 `study-log` 放在仓库内的 `.study-log/scratch/`，用完即删。
- 新记录可直接写入用户指定的目标；更新既有记录时先展示 diff 并取得确认，不静默覆盖人工编辑。

## 原文

原文的准确名称是“可追溯可见文本对话”，不是完整客户端 Session，也不等于匿名化。写入前合并展示并确认
provider、会话、source hash、起止消息及首尾预览、消息数、partial／final、隐私风险和目标位置。

- 原文与结构化记录同名配对：`logs/x.md` 对应 `logs-raw/x.md`，由工具生成并写入回链，不手工编辑正文。
- 默认排除 system、developer、reasoning、工具事件、客户端注入和附件正文。
- 高置信度凭据默认阻止写入，也可在用户明确选择后采用可复现脱敏；仓库内不保存原样凭据。
- 公司代码、内部 API、未公开硬件或性能数据等可能的专有内容需要单独确认；所有权不清楚时停止。
- partial 只能在同一 archive 中向后推进，每次更新前展示 diff 并取得确认；final 不再覆盖。
- 保存到仓库内不等于授权 Git stage、commit、push 或公开。

## 内部实现入口

materializer 完成后，Agent 使用 `.agents/skills/study-log/scripts/study_log.py`：结构化记录走
`list → preview → extract`，原文走 `list → preview → archive`，保存原文后用 `verify-pairs` 核验配对。
具体参数与错误处理以生成 Skill 自带的 `references/extraction-contract.md` 为准，不把命令记忆负担交给
学习者。

Lesson 只链接用户已审阅的产物；结构化记录、原文和本页都不能成为课程阶段、当前下一动作或结课结论的
第二事实源。
