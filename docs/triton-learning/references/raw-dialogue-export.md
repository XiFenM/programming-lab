# Study Log 与 legacy 学习对话

第 01、02 课的 `docs/triton-learning/dialogues/*.md` 由旧 exporter 生成，现作为冻结的 legacy evidence
保留。不要刷新、覆盖、重新格式化或批量替换其中的旧 Skill 名称、旧路径和历史命令。

M3 起，学习对话提取由中央 `study-log` 唯一负责。用户只需用自然语言说明目标，不需要记忆脚本命令。
Agent 根据意图区分两种按需产物：

| 模式 | 适用请求 | 保存内容 | 是否属于 Lesson 状态 |
| --- | --- | --- | --- |
| `structured` | 整理学习记录、提取纠错／高价值问答、准备制卡素材 | 原始回答、误解、纠错、关键问题与转折 | 否 |
| `raw` | 保存原始／逐轮可见文本，用于审计、研究或复盘 | 经过固定过滤的可追溯可见文本 | 否 |

用户只说“保存这段对话”时，先确认要精炼过程记录还是隐私风险更高的 raw。陪学暂停或收尾时可以在
取得同意后生成 structured；绝不自动提议或生成 raw。

## Structured 边界

- 只使用用户指定或当前任务直接相关的会话；有多个合理会话或主题边界时先确认。
- 保留学习者的原始回答、误解、纠错、高价值问题和关键转折，不复制完整教学正文、Lesson stage、
  Checkpoint 或 mastery。
- 先在仓库外临时提取，再蒸馏到用户授权的位置；完成后删除临时材料。
- 新记录可直接写入已授权目标；更新既有记录时必须先展示 diff 并取得确认，不得静默覆盖人工编辑。

## Raw 安全边界

raw 的准确名称是“可追溯可见文本对话”，不是完整客户端 Session，也不等于匿名化。写入前必须合并
展示并确认 provider、会话、source hash、起止消息及首尾预览、消息数、partial／final、隐私风险和
私有目标位置。

- 默认排除 system、developer、reasoning、工具事件、客户端注入和附件正文。
- 私有 archive root 没有隐式默认值；缺失时必须停止并询问绝对目录。默认写入 Git 工作树外，
  本仓库的 `dialogues/` 不再接收新 raw。
- 凭据默认阻止写入。优先缩小边界或改用 structured；脱敏或原样私存必须由用户明确选择。
- 公司代码、内部 API、未公开硬件或性能数据等专有内容需要单独确认；所有权不清楚时停止。
- 普通个人信息必须告警并纳入写入确认。用户坚持写入 Git 工作树时，目标必须未被跟踪且已被 Git
  忽略；`study-log` 不修改 `.gitignore`。
- raw 严格解析会话；任何坏行都停止，且原目标保持不变。
- source 或目标内容在预览后变化时必须停止并重新预览。final 不覆盖；partial 只能在同一 archive 中
  原位前进，并在每次更新前展示 diff、取得确认。
- 不手工润色生成的消息正文。边界或隐私处理错误时调整规则并重新生成。

## 内部实现入口

materializer 完成后，Agent 使用：

```text
.agents/skills/study-log/scripts/study_log.py
```

其内部流程固定为 `list → preview → extract`（structured）或 `list → preview → archive`（raw）。
`extract` 与 `archive` 都带预览所得 source hash；raw 始终需要隐私确认，只有刷新或终结既有 partial
时还必须同时带稳定 `archive_id` 与审阅过的目标 SHA-256。CLI 是机器接口，具体参数与错误处理以生成 Skill 自带的
`references/extraction-contract.md` 为准，不把命令记忆负担交给学习者。

Lesson 只链接用户已审阅并批准的产物；structured、raw 和本页都不能成为课程 stage、当前下一动作或
final mastery 的第二事实源。
