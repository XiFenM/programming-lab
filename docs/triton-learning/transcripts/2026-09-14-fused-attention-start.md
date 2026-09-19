---
archive_type: "study-log-visible-dialogue"
schema_version: 1
archive_id: "sl-f64df742d37a472cb2030409ddfb052b"
status: "final"
title: "Triton 06 Fused Attention 开课"
provider: "codex"
project_name: "programming-lab"
project_fingerprint: "422e19696a22"
source_session_id: "01a084ec-0402-7c13-bb42-36c2e352e0bb"
source_file: "rollout-2026-09-14T09-12-29-01a084ec-0402-7c13-bb42-36c2e352e0bb_01a09d79-05c5-70a2-abbd-855a506a381e.jsonl"
start_message_id: "msg-3f7c5d6364ef13a88041"
end_message_id: "msg-b01b1b91d426abaade6d"
message_count: 5
source_sha256: "266fcc305f5e6880ca0966ab3402e620c2e9a979507e8092b7e71bcc48952d32"
visible_content_sha256: "c323bb8aa8bed82775340b3b48877250c479d0606ae78c1c38dc412b923433da"
target_precondition_sha256: null
first_message_at: "2026-09-14T02:53:41.897Z"
last_message_at: "2026-09-14T03:01:49.169Z"
created_at_utc: "2026-09-19T12:50:29.644499+00:00"
updated_at_utc: "2026-09-19T12:50:29.644499+00:00"
normalization: {"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"}
redaction: {"version":"study-log-redaction-v1","categories":[],"applications":[]}
privacy_risks: {"categories":[],"counts":{}}
---

# Triton 06 Fused Attention 开课

> 此文件是规则化提取的“可追溯可见文本对话”，不是完整客户端 Session，也不代表已经匿名化。
> system、developer、reasoning、工具事件、客户端注入和附件正文默认不包含在内。

---

**001 · 用户** · `2026-09-14T02:53:41.897Z` · `msg-3f7c5d6364ef13a88041`

好的，我已经推送了。接下来，我想开启triton下一课。

---

**002 · 助手 / 过程更新** · `2026-09-14T02:54:02.507Z` · `msg-c0e9cd584c268e7702aa`

我会用 `guide-learning` 启动下一课：先核对推送后的仓库状态、Triton Program 的课间位置和固定教程来源，再建立第 06 课的目标、证据门槛与唯一 Checkpoint，然后开始课程导入。

---

**003 · 助手 / 过程更新** · `2026-09-14T02:56:38.674Z` · `msg-12b1e19756b9346c6d43`

固定来源已确认是第 06 课 **Fused Attention**，核心实现基于 FlashAttention-2。它同时包含在线 softmax 前向、因果分块、反向梯度和硬件特化；为了让本课保持可独立验收，我会把“完整前向实现”设为实践主线，把较复杂的反向先设为源码理解目标，性能与 FP8/warp specialization 留在核心门槛之外。

---

**004 · 助手 / 过程更新** · `2026-09-14T02:57:35.703Z` · `msg-9645cce90994412cdfcb`

第 06 课将写入 `docs/triton-learning/lessons/06-fused-attention.md`，Program 与唯一 Checkpoint 继续由 `docs/triton-learning/README.md` 管理。

本课设四个目标：注意力数学与 IO 瓶颈、在线 softmax 分块不变量、Triton 前向映射与因果分段、反向 `dQ/dK/dV` 数据流。概念理解均为 required；实践只要求独立实现和验证 FP16 前向，反向实践、性能基准、FP8 与 warp specialization 不进入核心门槛。所有 empirical 维度均为 not-required。第一个动作是建立普通注意力的矩阵与依赖范围。

---

**005 · 助手 / 正式回答** · `2026-09-14T03:01:49.169Z` · `msg-b01b1b91d426abaade6d`

第 06 课已启动：**Fused Attention 的在线 Softmax 与分块数据流**。

课程记录在 [06-fused-attention.md](/root/autodl-tmp/programming-lab/docs/triton-learning/lessons/06-fused-attention.md)，当前位于 O1：注意力数学与依赖范围。

本课路线是：

1. scaled dot-product attention、causal mask 与二次中间量。
2. 在线 softmax 的 `m_i / l_i / acc / alpha` 更新。
3. Triton 前向的 Q tile 常驻、K/V 扫描和 causal stage。
4. 利用保存统计量组织 `dQ/dK/dV` 的反向数据流。

实践门槛聚焦 FP16 前向；反向要求能独立读懂数据流。性能、FP8 和 warp specialization 暂不进入核心门槛。

对一个 batch 和一个 head，令序列长度为 \(N\)，head dimension 为 \(D\)：

\[
S=sQK^\mathsf{T},\qquad
P=\operatorname{softmax}(S),\qquad
O=PV
\]

其中：

- \(Q,K,V\) 都是 \([N,D]\)；
- \(S,P\) 都是 \([N,N]\)；
- softmax 沿 key 维度逐行计算；
- \(O\) 是 \([N,D]\)。

标准实现若把 \(S\) 和 \(P\) 都写入显存，会产生随 \(N^2\) 墀长的中间量。FlashAttention 仍计算精确注意力，但通过分块和在线 softmax 避免把完整 \(S/P\) 写入 HBM；它减少的是中间存储和数据搬运，并没有把注意力的主要算术复杂度变成线性。[FlashAttention 论文](https://arxiv.org/abs/2205.14135)；FlashAttention-2 进一步改进了 block 和 warp 的工作划分。[FlashAttention-2 论文](https://arxiv.org/abs/2307.08691)

固定教程的[前向内循环](/root/autodl-tmp/programming-lab/docs/triton-tutorials/official/06-fused-attention.py:48)正是让一个 Q tile 留在片上，同时依次扫描 K/V tile，并维护在线统计量。

先完成第一个检查。假设：

\[
B=1,\quad H=1,\quad N=4,\quad D=2
\]

并使用 causal attention，索引从 0 开始：

1. 完整 \(Q/K/V\)、\(S/P\) 和 \(O\) 的形状分别是什么？
2. query 位置 \(i=2\) 的 softmax 包含哪些 key 位置？其输出依赖哪些 \(V_j\)？
3. 若显式保存 \(S\) 和 \(P\)，两者合计有多少个元素？FlashAttention 避免物化它们，是否也消除了 \(QK^\mathsf{T}\) 和 \(PV\) 的主要计算？
