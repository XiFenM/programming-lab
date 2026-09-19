---
archive_type: "study-log-visible-dialogue"
schema_version: 1
archive_id: "sl-da033f4b1b2b438fafa2845b1a35464c"
status: "final"
title: "Triton 06 Fused Attention 反向与综合"
provider: "codex"
project_name: "programming-lab"
project_fingerprint: "422e19696a22"
source_session_id: "01a084ec-0402-7c13-bb42-36c2e352e0bb"
source_file: "rollout-2026-09-18T19-41-53-01a084ec-0402-7c13-bb42-36c2e352e0bb_01a0b452-b388-7e81-be01-90e221653af9.jsonl"
start_message_id: "msg-bfc510f9515a9b70b1b3"
end_message_id: "msg-f769781b669b6d149560"
message_count: 11
source_sha256: "51d550229fe79c665130104daee8afdc0ada8c393a9e4a2a961adabca3cedff7"
visible_content_sha256: "d7d005b08e1c3b2faff4802f23ee2ba8e9f9411b2c1bd33106455b007f0ff79b"
target_precondition_sha256: null
first_message_at: "2026-09-18T11:41:58.436Z"
last_message_at: "2026-09-18T12:43:41.366Z"
created_at_utc: "2026-09-19T12:50:30.236010+00:00"
updated_at_utc: "2026-09-19T12:50:30.236010+00:00"
normalization: {"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"}
redaction: {"version":"study-log-redaction-v1","categories":[],"applications":[]}
privacy_risks: {"categories":["proprietary"],"counts":{"proprietary":1}}
---

# Triton 06 Fused Attention 反向与综合

> 此文件是规则化提取的“可追溯可见文本对话”，不是完整客户端 Session，也不代表已经匿名化。
> system、developer、reasoning、工具事件、客户端注入和附件正文默认不包含在内。

---

**001 · 用户** · `2026-09-18T11:41:58.436Z` · `msg-bfc510f9515a9b70b1b3`

1. 需要位置为0、1、2的key；
2. 需要累加位置为2、3的query；
3. 因为因果注意力的机制：固定query，只能向前看key；固定key或value，只有后面的query能够用到他们。

---

**002 · 助手 / 正式回答** · `2026-09-18T11:42:30.958Z` · `msg-b264cf585d9da546c0e2`

三项都正确。更精确地说：

\[
dQ_i:\quad j\le i,
\]

\[
dK_j,dV_j:\quad i\ge j.
\]

这种互为行、列扫描的关系，直接决定了 causal 反向的分块方式。

假设当前 tile 的 token 范围是：

\[
[a,b).
\]

对于固定的 Q tile，计算 \(dQ\)：

| key 范围 | 处理方式 |
|---|---|
| `[0,a)` | 全部有效，无 mask |
| `[a,b)` | 对角区域，逐元素 mask |
| `[b,N)` | 全部是未来 key，跳过 |

对于固定的 K/V tile，计算 \(dK,dV\)：

| query 范围 | 处理方式 |
|---|---|
| `[0,a)` | 这些 query 早于当前 key，跳过 |
| `[a,b)` | 对角区域，逐元素 mask |
| `[b,N)` | 这些 query 都能看到当前 key，无 mask |

两者正好是镜像关系：

```text
dQ：   过去 key     对角区       未来 key
       无 mask      有 mask      跳过

dK/V：过去 query   对角区       未来 query
       跳过         有 mask      无 mask
```

固定源码的 `_attn_bwd_dq` 和 `_attn_bwd_dkdv` 就是在实现这两种扫描。

应用到：

\[
N=12,\qquad [a,b)=[4,8).
\]

请分别写出：

1. 计算 query tile `4:8` 的 \(dQ\) 时，哪些 key 范围无 mask、哪些需要 mask、哪些跳过？
2. 计算 key/value tile `4:8` 的 \(dK,dV\) 时，哪些 query 范围跳过、哪些需要 mask、哪些无 mask？

---

**003 · 用户** · `2026-09-18T11:47:26.564Z` · `msg-e375adce676e805873bc`

1. [0,4)的key无mask，[4,8)需要逐元素mask，[8,12)需要跳过；
2. [0,4)的query直接跳过，[4,8)需要逐元素mask，[8,12)无mask。

---

**004 · 助手 / 正式回答** · `2026-09-18T11:47:49.441Z` · `msg-512311635a10a21f955f`

分类完全正确。现在映射到固定源码的实际 launch 配置。

主反向 kernel 使用：

\[
BLOCK\_N1=128,\qquad BLOCK\_M2=128,
\]

grid 为：

\[
\left(\frac{N_{\text{CTX}}}{128},\,1,\,B\cdot H\right).
\]

对于每个 `program_id(0)=pid`，同一个 program 分别拥有：

- K/V token tile：

  \[
  [pid\cdot128,(pid+1)\cdot128)
  \]

  用于输出对应位置的 `dK/dV`；

- Q token tile：

  \[
  [pid\cdot128,(pid+1)\cdot128)
  \]

  用于输出对应位置的 `dQ`。

例如 \(N=256\)，每个 `(batch,head)` 只有两个主反向 program：

| `pid` | 拥有的 `dK/dV` 行 | 拥有的 `dQ` 行 |
|---:|---|---|
| 0 | `0:128` | `0:128` |
| 1 | `128:256` | `128:256` |

内部归约则使用较小的 tile：

- 计算 `dK/dV` 时，每次扫描 32 个 query；
- 计算 `dQ` 时，每次扫描 32 个 key；
- 对角 causal 区域进一步切成 16 个位置的小块。

这里有一个很重要的并行设计：**每个输出 token 的梯度只有一个 program 负责写回。**

因此，即使多个 query 都会贡献给同一个 \(dK_j,dV_j\)，也不需要跨 program 的锁或 atomic。负责该 key tile 的 program 会：

1. 扫描所有有效 query tile；
2. 在本地 `dk/dv` accumulator 中累加；
3. 完成整个归约后一次写回自己独占的输出行。

这和上一课共享 `w/b` 的情况不同：LayerNorm 的许多行 program 同时贡献同一参数位置，因此需要部分和或同步；这里通过工作划分让一个 program 独占一组 `dK/dV` 输出。

确认一下：对于 \(N=256\)、causal 模式、`pid=1`：

1. 它计算 `dK/dV[128:256]` 时需要扫描哪些 query 范围？
2. 多个 query 都贡献这些梯度，为什么仍不需要锁或 atomic？
3. 它计算 `dQ[128:256]` 时需要扫描哪些 key 范围？

---

**005 · 用户** · `2026-09-18T12:03:23.656Z` · `msg-a841dbabfa1d209cefc9`

1. 需要扫描有mask的[128:256)范围的query；
2. 因为只有一个program负责写回梯度，这个program会扫描所有有效的query tile，而后计算，写回自己独占的输出行；
3. 需要扫描无mask的[0:128)范围和有mask的[128:256)范围的key。

---

**006 · 助手 / 正式回答** · `2026-09-18T12:03:55.360Z` · `msg-1161e0692e3ac5f28721`

三项都正确。

第一项中，因为 \(N=256\)，`pid=1` 的 key tile 已经是最后一个 tile，所以：

- query `[128,256)`：对角区域，需要 mask；
- query `[256,N)`：为空，因此没有后续无 mask 区域；
- query `[0,128)`：早于当前 key，直接跳过。

接下来补上反向中的 base-2 缩放。前向为了使用 `exp2`，把 K 参与 score 计算时的缩放写成：

\[
K_{\text{scaled}}
=
K\cdot\frac{s}{\ln2}.
\]

于是：

\[
QK_{\text{scaled}}^\mathsf T
=
\frac{sQK^\mathsf T}{\ln2},
\]

可以直接结合保存的 base-2 `M` 重建：

\[
P=2^{QK_{\text{scaled}}^\mathsf T-M}.
\]

但最终需要的梯度仍是原始自然指数 attention 的：

\[
dQ=s\,dS K,
\qquad
dK=s\,dS^\mathsf TQ.
\]

教程分别处理这两个缩放。

### \(dK\)

`dK` 的累加使用未缩放的 Q：

\[
dk_{\text{tmp}}=dS^\mathsf TQ.
\]

循环结束后：

\[
dK=s\cdot dk_{\text{tmp}}.
\]

### \(dQ\)

`dQ` 直接乘了已经预缩放的 K：

\[
dq_{\text{tmp}}
=
dS K_{\text{scaled}}
=
\frac{s}{\ln2}dS K.
\]

所以最后乘回：

\[
\ln2
\]

得到：

\[
dQ
=
\ln2\cdot dq_{\text{tmp}}
=
s\,dS K.
\]

### \(dV\)

\[
dV=P^\mathsf TdO
\]

不经过 score 的缩放，因此不需要乘 \(s\) 或 \(\ln2\)。

请确认这三个最终处理：

1. `dq_tmp = dS @ (K*s/ln2)` 后，应乘什么得到正确的 \(dQ\)？
2. `dk_tmp = dS.T @ Q` 后，应乘什么得到正确的 \(dK\)？
3. 为什么 \(dV\) 不需要 `sm_scale`？

---

**007 · 用户** · `2026-09-18T12:34:01.886Z` · `msg-9b21afa7815a855e887e`

1. 乘ln2得到正确的dQ；
2. 乘sm\_scale得到正确的dK；
3. 因为不经过score的缩放。

---

**008 · 助手 / 正式回答** · `2026-09-18T12:34:26.146Z` · `msg-c65c58a6cef8102fb651`

三项都正确。这样反向中的 base-2 变换也连起来了。

在进入综合验收前，还要明确固定教程的接口边界。这些约束来自 wrapper，而不是 FlashAttention 数学本身：

- `Q/K/V` 的 `HEAD_DIM` 必须相同；
- `HEAD_DIM` 只能是：

  \[
  \{16,32,64,128,256\};
  \]

- 反向要求 `dO` 连续；
- `Q/K/V/O/dO` 的 stride 必须一致；
- 反向固定使用 128-token 外层 tile，因此要求：

  \[
  N_{\text{CTX}}\bmod128=0;
  \]

- 教程只验证 FP16 反向；FP8 只覆盖部分前向路径。

这些都是“固定实现支持什么”的边界，不能从 FlashAttention 算法本身推导出来。

判断下面三组输入中，哪些能够执行这份教程的完整前向和反向：

1. \(N_{\text{CTX}}=256,\ HEAD\_DIM=64\)
2. \(N_{\text{CTX}}=192,\ HEAD\_DIM=64\)
3. \(N_{\text{CTX}}=256,\ HEAD\_DIM=80\)

请分别说明通过或拒绝的原因。

---

**009 · 用户** · `2026-09-18T12:42:32.114Z` · `msg-37a676b9c051ce2be999`

1. 可以执行；
2. 不能，因为N不是128的倍数；
3. 不能，因为HEAD\_DIM不在允许范围{16,32,64,128,256}内。

---

**010 · 助手 / 过程更新** · `2026-09-18T12:42:54.520Z` · `msg-472d6e8505409e2ba60e`

三项判断都正确。至此，前向在线 softmax、program/tile 映射、causal 分段、反向接口与扫描方向、数值缩放和固定 wrapper 边界都已覆盖。我会把课程推进到跨节点综合验收，并将唯一恢复点更新到综合题。

---

**011 · 助手 / 正式回答** · `2026-09-18T12:43:41.366Z` · `msg-f769781b669b6d149560`

三项都正确。我们现在进入三题跨节点综合验收；答完后，将根据 evidence 缺口进入最小 FP16 前向实践。

### 1. 在线 Softmax 故障诊断

某行在处理旧分块后保存：

\[
m=2,\qquad l=3,\qquad acc=A.
\]

新分块最大值为 \(5\)，其在新最大值基准下的局部分母为 \(4\)，局部输出分子为 \(B\)。

请写出：

- \(\alpha\)；
- 合并后的 \(m',l',acc'\)；
- 最终输出；
- 如果更新最大值却没有用 \(\alpha\) 重标定旧 `l/acc`，错误的本质是什么？

### 2. 未见过的前向映射

给定：

\[
Z=2,\ H=2,\ N=16,\ D=64,\ BLOCK_M=4,\ BLOCK_N=8,
\]

使用 non-causal attention。某 program：

\[
program\_id(0)=2,\qquad program\_id(1)=3.
\]

请给出：

- 对应的 `(batch,head)`；
- `offset_y`；
- Q 的局部 token 范围与 descriptor 全局行；
- K/V 循环次数及每轮 `qk` 形状；
- 最后写回哪些对象，哪些二次中间量不会写入 HBM。

### 3. 反向全链路

给定 causal attention：

\[
N=256,
\]

主反向 kernel 的 `pid=1`。

请说明：

- 预处理 kernel 的输入、输出以及 `Delta` 的公式；
- 该 program 负责的 `dK/dV` 和 `dQ` 行范围；
- 计算 `dK/dV` 时扫描哪些 query 区域，分别怎样 mask；
- 计算 `dQ` 时扫描哪些 key 区域，分别怎样 mask；
- backward 保存了什么、重新计算了什么；
- 多个 query 都贡献同一个 `dK/dV` 时，为什么不需要 atomic？
