# Codex 学习对话后验归档

本功能用于在一节课结束或阶段性中断后，从 Codex rollout JSONL 中截取该课的原始可见对话，
生成独立 Markdown 档案。它与单课主记录分工不同：

| 文档 | 作用 | 是否整理观点 |
| --- | --- | --- |
| `lessons/<NN>-<topic>.md` | 结构化讲解、结论、实践、评审和下一步 | 是 |
| `dialogues/<NN>-<topic>.md` | 用户与助手实际可见消息的原始材料 | 否 |

导出脚本是 [`scripts/export_codex_dialogue.py`](../../../scripts/export_codex_dialogue.py)，只使用
Python 标准库，不修改原始 JSONL。

## 导出边界

默认保留：

- `response_item` 中 role 为 `user` 或 `assistant` 的文本消息。
- 助手的 `commentary` 过程更新和 `final_answer` 正式回答。
- 每条消息原有的 Markdown 正文和时间戳。

默认排除：

- system、developer 指令。
- reasoning、工具调用、工具输出和其他内部事件。
- 独立的 `<environment_context>` 消息。
- IDE 自动注入的 active file、open tabs、附件列表等外壳；只保留
  `## My request for Codex:` 后面的用户请求。
- 规范化后相邻且完全相同的重复消息。这类重复可能在 session 恢复或 compaction 后出现。

这是一种有明确规则的“原始对话导出”，不是逐字节复制 session。若研究客户端注入信息，可以
使用 `--keep-client-context --keep-duplicates`；system、developer 和工具事件仍不会进入对话
档案。当前脚本只导出 `input_text` / `output_text`，不会把图片等非文本内容嵌入 Markdown，原始
JSONL 始终是最终溯源依据。

## 推荐的后验流程

### 1. 找到 session 文件

Codex session 通常位于 `/home/coder/.codex/sessions/`。可以列出候选文件：

```bash
rg --files /home/coder/.codex/sessions -g 'rollout-*.jsonl'
```

优先根据修改时间、session ID 和消息预览确认来源，不要只凭文件名日期猜测。

### 2. 预览可截取边界

```bash
uv run --frozen python scripts/export_codex_dialogue.py list \
  <session.jsonl> \
  --role user \
  --preview 180
```

列表中的文本已经按默认规则移除客户端上下文，可直接选取一条独特的开课用户消息和下一阶段
用户消息作为边界。

### 3. 导出一节课

```bash
uv run --frozen python scripts/export_codex_dialogue.py export \
  <session.jsonl> \
  docs/triton-learning/dialogues/01-vector-add.md \
  --title '第 01 课：Vector Addition 原始学习对话' \
  --lesson 01-vector-add \
  --start-user '非常好，这就让我们开始第一课时吧。' \
  --end-before-user '下一阶段第一条用户消息的独特片段'
```

- `--start-user`：包含第一条匹配的规范化用户消息。
- `--end-before-user`：在后续第一条匹配的用户消息之前停止，不把它写入本课。
- 两项都是 substring 匹配；应选择足够独特但不必复制整段的文本。
- 未提供结束边界时会导出到当前日志末尾，因此 active session 更推荐明确指定结束边界。

也可以按 ISO-8601 时间进一步限制：

```bash
--start-time 2026-07-20T01:44:15Z \
--end-time 2026-07-20T09:15:00Z
```

开始时间包含，结束时间不包含。文本边界和时间边界同时提供时取交集。

### 4. 审核再归档

至少确认：

1. 第一条和最后一条消息属于目标课程。
2. `message_count` 与角色标签合理。
3. 没有意外包含凭据、私人路径、附件内容或下一课对话。
4. 单课主记录已链接到原始对话文件。
5. 导出文件的 frontmatter 保留 source/session/hash 和规范化选项。

脚本默认拒绝覆盖已有档案。确认边界和 diff 后才能显式使用 `--overwrite`：

```bash
uv run --frozen python scripts/export_codex_dialogue.py export \
  <其余参数> \
  --overwrite
```

这可以避免 active session 误选边界时静默破坏先前归档。

## 其他选项

### 只保留正式回答

```bash
--final-only
```

它会排除助手 commentary，但保留全部用户消息和正式回答。原始材料档案默认不使用该选项，
因为过程更新也是用户实际看到的对话。

### 保留客户端上下文和重复消息

```bash
--keep-client-context --keep-duplicates
```

该模式更接近 response item 原文，但会混入环境、IDE 标签和恢复时重复注入的消息。它仍然不会
导出 system/developer、reasoning 或工具事件。

## 输出格式与可追溯性

每份档案的 frontmatter 包含：

- `source_file` 与 `session_id`。
- 导出时整个 JSONL 快照的 `source_sha256`。
- 所选规范化消息序列的 `dialogue_sha256`。
- 导出时间、首尾消息时间和消息数量。
- client context、重复消息和 commentary 的处理选项。

正文按顺序标记为“用户”“助手 / 过程更新”“助手 / 正式回答”。脚本不摘要或改写消息正文；
主记录中的提炼、纠错和最终结论不能反向覆盖原始对话档案。

## 已知限制

- Codex rollout schema 可能随版本变化。当前实现以本仓库 2026-07-20 session 中的
  `response_item -> payload.type=message` 为依据；schema 变化后应先更新合成测试。
- 同一节课可能跨多个 session。当前一次 export 接受一个 JSONL；跨 session 时应分别导出后
  人工建立索引，不能直接拼接并丢失 provenance。
- substring 边界若不唯一会选择第一处匹配。先使用 `list` 预览，必要时换更独特文本或时间。
- 非文本输入不会嵌入 Markdown，应保留原 session 和必要附件。
- session 在 active 对话期间会继续追加；后验导出应明确结束边界并审核最终 diff。

## 验证命令

```bash
uv run --frozen python -m pytest -q tests/python/test_export_codex_dialogue.py
uv run --frozen ruff check scripts/export_codex_dialogue.py \
  tests/python/test_export_codex_dialogue.py
uv run --frozen ruff format --check scripts/export_codex_dialogue.py \
  tests/python/test_export_codex_dialogue.py
uv run --frozen basedpyright scripts/export_codex_dialogue.py \
  tests/python/test_export_codex_dialogue.py
```
