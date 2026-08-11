# 第 NN 课：可独立验收的能力标题

<!--
仅在学习者明确授权当前 Lesson 后创建。复制“核心记录”，再按实际发生追加条件片段；不要预建空的
练习、finding、event、Checkpoint 或原始对话章节。第 01、02 课是冻结的 legacy evidence，不迁入本模板。
-->

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-NN-<topic>` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | （一项可独立描述和验收的能力） |
| 阶段 | `teaching` / `synthesis` / `practice` / `review` / `mastery-gate` / `complete` |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/<file>.py` | `teaching-spine` | 仓库 commit | 教学顺序与示例 |
| `docs/triton-tutorials/official/<file>.py` | `implementation-authority` | 仓库 commit | 固定版本实现与控制流 |

### 目标与证据门槛

<!-- 只保留 2–4 个紧密相关目标；required 维度在激活 Lesson 时声明，扩大门槛须重新授权。 -->

| ID | 可观察目标 | conceptual | practical | empirical | 本课 evidence 目标 |
| --- | --- | --- | --- | --- | --- |
| O1 |  | required / not-required | required / not-required | required / not-required |  |

### 当前证据

- **综合验收 evidence**：
- **仍缺 evidence**：无 / 列出目标与维度
- **权威知识产物引用**：文章、源码说明或其他稳定锚点；不复制教学正文。
- **Fallback 心智模型**：仅在没有可链接的权威知识产物时写 3–6 行，否则删除本项。

### 核心工件与参考

| 角色 | 路径或引用 | 说明 |
| --- | --- | --- |
| learner-owned artifact |  | 仅在实际存在时记录 |
| Agent-owned evidence |  | 测试、rubric、fixture 或实验记录 |
| source / knowledge artifact |  | 不复制正文 |

## 条件片段：Session event

<!-- 每个有实质增量的会话段最多一条；无增量时不要添加。 -->

| ID / 日期 | Lesson ref | 覆盖范围 | 完成动作 | Evidence 引用 | 未关闭问题 | Confirmed duration | Marker |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | 本 Lesson ID |  |  |  |  | 仅用户提供时填写 | 无 / `closure` |

## 条件片段：已接受的正式练习

<!-- 只有综合验收仍有 evidence 缺口且学习者接受六块契约后，才追加本节。 -->

- **Practice ID / revision / digest**：
- **目标、缺失维度与 evidence gap**：
- **Task**：
- **Deliverables**：

| Artifact | Learner 必须交付的 outcome |
| --- | --- |
|  |  |

- **Acceptance**：

| ID | 可观察标准 | Evidence method |
| --- | --- | --- |
| A1 |  |  |

| 边界 | 路径或受限 pattern | 允许操作 |
| --- | --- | --- |
| learner-owned |  | read / create / modify / run |
| agent-owned |  | read / create / modify / run / record |
| read-only |  | read |
| excluded |  | 无 |

- **帮助如何影响独立 evidence**：说明 material assistance 只撤销受影响范围，并用无提示同构变式恢复。
- **非目标与完成门槛**：列出 excluded 能力；required acceptance、映射的 blocking／major finding 与
  已声明 mastery 维度共同决定完成。

| Optional ID | 可观察 criterion | Evidence method |
| --- | --- | --- |
|  |  |  |

| Acceptance event ref | Accepted revision | Accepted digest |
| --- | --- | --- |
|  |  |  |

## 条件片段：Material assistance

| 实际最高披露内容 | 受影响目标／acceptance／工件 | Agent 写入 learner core |
| --- | --- | --- |
|  |  | true / false |

## 条件片段：Durable findings

<!-- 同一根因只保留一条并原地更新；完整命令输出保留在原工件。 -->

| ID | Maps to | Severity | Owner | Status | Evidence | Next action |
| --- | --- | --- | --- | --- | --- | --- |
|  | O# / A# | blocking / major / minor / suggestion |  | open / closed / deferred / dismissed | 开启证据；终态验证或理由 | open 时恰好一个动作 |

## 条件片段：Mastery gate 与关闭

<!-- 每行只对应一个“目标 × 一个 required 维度”；同一目标有多个 required 维度时分行。 -->

| 目标 | 单一 Required 维度 | 最小 evidence 锚点 | 判断 |
| --- | --- | --- | --- |
| O1 | conceptual |  | 充分 / 不足 |

- **Required blocking／major 未关闭**：0 / 列出 ID
- **Assistance 影响是否已恢复**：不适用 / evidence 引用
- **Nonblocking／optional 余项**：无 / 列出
- **学习者关闭确认**：日期与确认引用；未确认时不得写 final mastery
- **Final mastery**：仅在确认关闭后记录每个目标与 required 维度的终态 evidence

原始对话或 structured 过程记录由 `study-log` 按需生成，只在本课链接已审阅产物；它们不保存当前阶段、
Checkpoint 或 final mastery。确有跨会话恢复任务时，另在已披露且获授权的唯一位置保存可覆盖
Checkpoint，不在本 Lesson 累积暂停快照。
