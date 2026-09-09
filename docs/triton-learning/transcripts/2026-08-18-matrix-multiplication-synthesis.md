---
archive_type: "study-log-visible-dialogue"
schema_version: 1
archive_id: "sl-7a2a11e84c3045c58b75c04032c2fc45"
status: "final"
title: "Triton Lesson 03：综合验收与实践范围校准"
provider: "codex"
project_name: "programming-lab"
project_fingerprint: "422e19696a22"
source_session_id: "01a013fc-5b9e-7c90-8d72-c60db1662995"
source_file: "rollout-2026-08-18T16-28-20-01a013fc-5b9e-7c90-8d72-c60db1662995.jsonl"
start_message_id: "msg-e33bbd3571f5a7916f51"
end_message_id: "msg-011f819a4a12411c7d44"
message_count: 14
source_sha256: "93f629785f6ee20f217ab3da5d65008a17695e74254205221cd43fbb3263e34e"
visible_content_sha256: "104c38034cdd7420abfa78a0000cb54b2b896e0b459f6e4011da6608808fddc6"
target_precondition_sha256: null
first_message_at: "2026-08-18T08:44:36.253Z"
last_message_at: "2026-08-18T09:51:50.522Z"
created_at_utc: "2026-09-09T07:16:22.695344+00:00"
updated_at_utc: "2026-09-09T07:16:22.695344+00:00"
normalization: {"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"}
redaction: {"version":"study-log-redaction-v1","categories":[],"applications":[]}
privacy_risks: {"categories":["proprietary"],"counts":{"proprietary":4}}
---

# Triton Lesson 03：综合验收与实践范围校准

> 此文件是规则化提取的“可追溯可见文本对话”，不是完整客户端 Session，也不代表已经匿名化。
> system、developer、reasoning、工具事件、客户端注入和附件正文默认不包含在内。

---

**001 · 用户** · `2026-08-18T08:44:36.253Z` · `msg-e33bbd3571f5a7916f51`

很好。接下来我想继续triton课程。先前关于triton lesson 03并没有完全结束，打了断点。现在我们从断点处重新开始。

---

**002 · 助手 / 过程更新** · `2026-08-18T08:44:59.221Z` · `msg-e59c96205165e8e944ea`

我会按 `guide-learning` 的恢复规则先做一次只读核验：确认 Triton Program、Lesson 03、Checkpoint、固定教程源码以及先前 evidence 没有漂移。恢复本身不会写状态；若断点仍有效，我们直接从唯一下一动作 S1 继续。

---

**003 · 助手 / 过程更新** · `2026-08-18T08:45:30.139Z` · `msg-9844cc434ec8bf59f86b`

低成本 drift 核验通过：Program、Lesson、源码版本和工作树都没有变化。不过结构化记录为了保持精简，只保存了 S1 的 shape，省略了当时题目里的具体 block/group 参数。为避免我凭空补参数，我会启用 `study-log` 做一次只读预览，只定位该记录已经明确引用的 Codex 会话并恢复 S1 原题；不会归档、提取或写入。相关边界可见 [study-log 使用说明](/root/autodl-tmp/programming-lab/.agent-skills/docs/user-guides/study-log.md)。

---

**004 · 助手 / 过程更新** · `2026-08-18T08:45:54.261Z` · `msg-8ccc56170be6e3c317f3`

该结构化日志引用的旧 Codex 根会话已不在当前客户端可发现目录中，因此我不会继续猜历史会话。接下来只检查 Git 中这两个状态文件的既有版本，看看 S1 原题是否曾以完整形式提交过；仍然是只读恢复。

---

**005 · 助手 / 正式回答** · `2026-08-18T08:46:52.412Z` · `msg-d1fca46a88f53d1aa6c0`

已恢复到 Triton Lesson 03 的断点，没有发现状态或源码漂移。当前位置是 `synthesis`，唯一下一动作是综合验收 S1；本轮尚未写入状态。

旧记录没有保留 S1 的完整参数，原 Codex 会话也已不可发现。根据保存的 shape 和前序 evidence，我重建一个等价的 S1；它不改变目标或验收门槛，但不声称是原题逐字还原。

### S1：跨节点综合推导

给定：

```text
A.shape = (257, 65)
B.shape = (65, 129)
C.shape = (257, 129)

BLOCK_SIZE_M = 64
BLOCK_SIZE_N = 64
BLOCK_SIZE_K = 32
GROUP_SIZE_M = 2
```

请独立完成以下推导：

1. 计算 `num_pid_m`、`num_pid_n`、一维 launch grid 的 program 总数。
2. 找出最后一个 group 包含哪些一维 PID，并逐个映射成 `(pid_m, pid_n)`。
3. 对最后一个 PID：

   - 写出它负责的名义 `C` tile 范围；
   - 分别计算 M、N 方向有效与无效 lane 数；
   - 说明最终实际写回多少个 `C` 元素。

4. 推导 K-loop：

   - 一共执行几轮；
   - 每轮有多少个有效 K lane；
   - 最后一轮哪些 lane 被 mask 并填零。

5. 最后从正确性角度串起来解释：

   - 为什么 M/N load 可以用取模读入 dummy 数据；
   - 为什么这些 dummy 计算不会污染有效输出；
   - 为什么 K 尾部不能取模，必须在 load 时补零；
   - `c_mask` 最终负责保证什么，又不能修复什么。

请把公式和中间结果写出来。你回答后，我会先判断 S1 的 evidence，只对实际差距做补充，然后进入 S2 的受控实验预测。

---

**006 · 用户** · `2026-08-18T09:23:03.801Z` · `msg-daa5e03c53b4d05361f6`

1.
M = 257, K = 65, N=129
num_pid_m = cdiv(M // BLOCK_SIZE_M) = 5
num_pid_n = cdiv(N // BLOCK_SIZE_N) = 3
num_program = num_pid_m * num_pid_n = 15
2.
num_group = cdiv(num_pid_m // GROUP_SIZE_M) = 3
last_group_id = num_group - 1 = 2
first_pid_in_last_group = last_group_id * GROUP_SIZE_M * num_pid_n = 12
pid_in_last_group = [12, 13, 14]
first_pid_m_in_last_group = last_group_id * GROUP_SIZE_M = 4
last_group_size_m = min(num_pid_m - first_pid_m_in_last_group, GROUP_SIZE_M) = 1
pid_m = first_pid_m_in_last_group + (pid_in_last_group - first_pid_in_last_group) % last_group_size_m = [4, 4, 4]
pid_n =  (pid_in_last_group - first_pid_in_last_group) // last_group_size_m = [0, 1, 2]
所以最后一个group包含id为[12, 13, 14]的program，并且各自的(pid_m, pid_n)为(4,0),(4,1),(4,2)。
3.
最后一个pid对应(4,2)位置，就名义负责的C tile范围是C[256:320,128:192]
M方向有效lane为1，无效为63；N方向同样，有效lane为1，无效为63.
最终写回仅一个元素C[256,128]。
4.
一共执行cdiv(K,BLOCK_SIZE_K)=3轮。
前两轮均有32个有效lane，最后一轮只有1个有效lane。
最后一轮的后31个lane均被mask填零。
5.
因为 M/N load 的dummy数据不影响有效位置数据的计算。每一个有效位置的计算只在K方向上循环乘积求和，其他方向的结果不影响其计算。只需要在写回结果时通过mask去除掉这些dummy数据的结果写入就不影响结果正确性了。
而K尾部由于会影响有效位置数据的计算，如果取模而不是补零，就会导致多计算了一部分元素的乘积求和，结果就会出错。
最终的写回c_mask保证不写回M/N load 的dummy数据结果，这样保证不会越界写入脏数据；但不能修复K方向的脏数据。如果K方向没有补零，而多计算了一部分结果，就会导致错误的结果已经在里面，对M和N方向进行的c_mask就无能为力了。

---

**007 · 助手 / 过程更新** · `2026-08-18T09:23:35.854Z` · `msg-f3bbfc2496c925e9aded`

S1 通过。你的 grid、尾组映射、最后 tile、K 尾部以及三类 mask 的职责都形成了完整的跨节点证据；唯一需要修正的是记号：应写 `cdiv(M, BLOCK_SIZE_M)`，而不是 `cdiv(M // BLOCK_SIZE_M)`，你后面的数值计算本身是正确的。

这次回答使 S1 evidence 和唯一下一动作发生了耐久变化，因此 `guide-learning` 会按稀疏记录规则只更新 Lesson evidence 与 Checkpoint 到 S2；不会生成学习日志或卡片。

---

**008 · 助手 / 正式回答** · `2026-08-18T09:24:44.263Z` · `msg-fcb102c092d0f59c2fc0`

S1 已通过并记录为 `E-05`。Checkpoint 已推进到 S2；`git diff --check` 通过。

记号修正：

```python
num_pid_m = triton.cdiv(M, BLOCK_SIZE_M)
num_groups = triton.cdiv(num_pid_m, GROUP_SIZE_M)
```

你的核心解释是正确的：M/N 是独立输出坐标，只有 K 是归约维度，所以 K 中的错误值会直接污染有效输出。

### S2：受控实验预测

固定以下条件，只改变 `GROUP_SIZE_M`：

```text
M = N = K = 4096
dtype = float16

BLOCK_SIZE_M = 128
BLOCK_SIZE_N = 128
BLOCK_SIZE_K = 32
num_warps = 4
num_stages = 4

Variant A: GROUP_SIZE_M = 1
Variant B: GROUP_SIZE_M = 2
```

暂时不要运行代码。请给出一份实验前预测，覆盖：

1. **可证伪预测**  
   你预测哪个 variant 更快，或者预测二者没有稳定差异？原因是什么？请联系 PID 顺序、A/B tile 复用和 L2 locality。

2. **控制变量**  
   哪些条件必须保持一致，才能把差异归因于 `GROUP_SIZE_M`？特别说明如何避免 autotune 同时改变其他配置。

3. **测量方法与指标**  
   如何安排 warm-up、同步、重复测量？主要比较 latency、TFLOPS，还是两者？正确性应怎样独立验证？

4. **否证条件**  
   出现什么结果时，你会承认原预测不成立？不要只写“另一组更快”，请给出能区分真实差异与测量波动的判据。

预测不必最终正确；这里检验的是你能否在看到结果前提出边界明确、可以被数据推翻的解释。

---

**009 · 用户** · `2026-08-18T09:43:41.994Z` · `msg-5bc17ee5f929bad6f995`

1. GROUP_SIZE_M = 1相当于就是原本的row-major的分块顺序。而GROUP_SIZE_M=2就是采用了我们本次学习到的grouped ordering。我预测variant B会稍快一些，因为正如先前所提到的，grouped ordering可以增加邻近program的tile复用，增加L2 cache命中率。
2. BLOCK_SIZE_M, BLOCK_SIZE_N, BLOCK_SIZE_K, num_warps, num_stages, num_program都需要保持一致。采用控制变量法，只有GROUP_SIZE_M进行改变。对于autotune，就把其中的config删掉，仅剩一个。
3. 测量方法可以先多次warmup，然后同步，然后重复测量多次。latency和TFLOPS都可以比较。正确性另外验证，与pytorch的matmul结果比较。
4. 根据先前的经验。需要先确定计时的基本单位。如果二者仅相差几个基本计时单位，是无法判定哪个更快的。然后需要多次计时，严谨的话，可能需要统计学校验来判断某一个比另一个快。然后承认原预测不成立。

---

**010 · 助手 / 正式回答** · `2026-08-18T09:44:37.861Z` · `msg-72eb3520fcd3f87f8795`

你的性能方向与 cache-locality 机制判断成立，但 S2 暂未通过：主要缺口是实验方法和否证条件仍不够可执行。

需要修正三点：

- 只保留一个 autotune config 只能测一个 variant。应禁用 autotune，做两个固定 launch；除 `GROUP_SIZE_M` 外配置完全相同，并排除首次编译时间。
- 固定 shape 时，`TFLOPS = 2MNK / latency`，两者不是独立证据。应以 latency 为主要指标，TFLOPS 只作为派生展示。
- 计时器分辨率不是主要噪声来源。GPU 调度、频率、温度和系统负载通常产生更大的波动，因此必须预先定义数值化判据。

还应固定输入、布局、stream、是否包含输出分配，并交替采用 A→B、B→A 的顺序，降低运行顺序和温度漂移的影响。正确性比较放在计时之外完成。

请补全下面这份最小实验契约：

```text
warm-up 次数：
独立 paired batches 数：
每个 batch 的计时次数：
A/B 运行顺序：
主要统计量：

支持“B 更快”的条件：
否定“B 更快”的条件：
判定为证据不足的条件：
```

三种结果必须分开：支持预测、否定预测、差异落在噪声内而无法判断。完成这个可执行判据后，S2 才形成合格的事前预测证据。

---

**011 · 用户** · `2026-08-18T09:49:01.555Z` · `msg-6e6a7f8ad4e662713c47`

我不想做这些，这与我们的学习目标不一致。我们现在处于哪个节点哪个阶段？为什么到现在还没有编程的练习？实验和测试部分，在先前的讨论中应该已经说明了尽可能减少。

---

**012 · 助手 / 过程更新** · `2026-08-18T09:49:57.544Z` · `msg-f72b4b740aed69af2e01`

你指出得对：我刚才把“一个最小受控测量”膨胀成了成对批次、数值阈值和统计判据，这超出了本课已记录的范围；它不应被视为你的学习差距。

当前仍在 Lesson 03 的 `synthesis` 阶段。之所以还没编程，是既有 Checkpoint 把顺序设成“先完成 S1/S2 综合验收，再提出 O3 正式实践契约”。S1 已完成；你对 S2 给出的方向、控制变量、重复测量和可被反例推翻的意识，按“尽可能减少实验”的原范围已经足够。下一步应当进入编程练习，而不是继续扩展实验设计。

我现在会按 `guide-learning` 的正式练习边界，核对现有练习文件后给出一份最小实践契约；在你接受前不会创建测试或改动练习代码。

---

**013 · 助手 / 过程更新** · `2026-08-18T09:50:46.851Z` · `msg-2077a87ccc56400cdd0f`

现有记录本来就明确限定：O4 只做一次最小受控测量，profiler、置信区间、统计研究、cache 深挖和穷举调参都排除在核心范围外。你的 S2 回答已经满足进入实践前所需的概念准备；我会把 Checkpoint 从“S2 待回答”更正为“综合验收完成，等待最小实践契约确认”。这不会创建测试或练习实现。

---

**014 · 助手 / 正式回答** · `2026-08-18T09:51:50.522Z` · `msg-011f819a4a12411c7d44`

你说得对。刚才我把最小实验要求过度扩张了，这延误了编程练习一轮。

当前状态：

- Lesson：03 Matrix Multiplication
- 阶段：`synthesis` 已完成
- 已通过：O1/O2/O4 conceptual，包括 S1 和原始 S2
- 尚缺：O3 practical 编程证据，以及 O4 的一次最小测量
- 下一节点：确认正式实践契约，然后立即开始编程

之所以此前没有编程，是原 Checkpoint 要求先完成综合验收再进入正式实践。这个顺序本身符合既有流程，但我不应该在 S2 后继续追加统计实验要求。状态现已更正，且 `git diff --check` 通过。

## 最小实践契约 `triton-03-practice-01` · revision 1

1. 为什么做

- O3 practical：尚未独立实现并验证矩阵乘法。
- O4 empirical：只缺一次最小受控观察，不要求性能研究。

2. 你交付什么

你编写：

[gpu/triton/lesson03_matrix_multiplication.py](/root/autodl-tmp/programming-lab/gpu/triton/lesson03_matrix_multiplication.py)

内容包括：

- FP16 矩阵乘法 kernel；
- FP32 accumulator；
- grouped PID mapping；
- K 尾部补零和 C store mask；
- 面向连续 CUDA FP16 二维矩阵的最小 wrapper。

3. 怎样算通过

- `A01`：正常 shape 返回正确的 shape、device 和 FP16 dtype。
- `A02`：一个正常 shape 和一个同时包含 M/N/K 尾部的 shape 与 `torch.matmul` 在合理容差内一致。
- `A03`：初次通过后，再完成一个新的非整除 shape，并解释它覆盖的边界。
- `A04`：代码中的 grouped mapping、K mask、FP32 accumulation 和 C mask 与已掌握的模型一致。
- `A05`：正确性通过后，只运行一次固定配置下 `GROUP_SIZE_M=1/2` 的简单计时；不要求 B 必须更快，只需记录结果并说明该结果能与不能支持什么。

4. 文件边界

- 你写：`gpu/triton/lesson03_matrix_multiplication.py`
- 我维护：`gpu/triton/lesson03_matrix_multiplication_test.py`、Lesson evidence 和 Checkpoint
- 我只读：固定的官方教程源码、Lesson 01/02 实现
- 本次不动：依赖、CI、公共配置、官方教程快照以及其他练习文件

5. 帮助边界

你可以随时自然提问。我会先提供最小诊断或概念定位；若需要我给出核心伪代码或具体修复，受影响部分之后用一个新变式恢复独立实践证据。我不会直接修改你的实现文件。

6. 非目标与完成门槛

不做：

- 完整 autotune 配置表复刻；
- profiler、统计检验或置信区间；
- cache 机制深挖；
- 穷举 shape、调参或生产级输入验证；
- 固定性能阈值。

通过 `A01–A05`、关闭 required major/blocking finding，并能解释关键验证后，就进入 mastery gate。

如果你接受这份最小契约，请直接回复“接受”；我随后只创建最小验收测试，把精确运行命令交给你，然后由你开始实现。
