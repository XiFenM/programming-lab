# 学习记录 · 2026-08-24 · Triton Low-Memory Dropout

> 来源：codex:01a013fc · msg-89f14b5699544e84b741 → msg-6f5ed818a1da2c173c7a
> 关联：[Lesson 04：基于 seed/offset 的低内存 Dropout](../lessons/04-low-memory-dropout.md)

## 学习过程

- [要点] Inverted dropout 为什么能保持单元素输出的期望？——我在 `x=12,p=0.25` 的例子中推导：
  保留概率为 `0.75`，保留时输出 `16`，丢弃时输出 `0`，所以期望是
  `0.75×16+0.25×0=12`；若只清零而不缩放，期望会降为 `9`。（来源：
  `msg-8d132420ba1892ef34fd`）
- [要点] Boundary mask 与 Dropout keep mask 分别回答什么？——我说：“`valid_mask` 检查该位置是否是
  有效元素，是否越界；而 `x_keep` 是 dropout 计算逻辑中的判断元素是否被保留。”前者保护合法访存，
  后者在合法元素中选择清零或保留并缩放。（来源：`msg-acc0212b75a5b8b1fe2c`）
- [要点] 为什么 `tl.rand` 必须接收 global offsets？——我判断 local offsets 会让 `pid 0` 与 `pid 1`
  得到完全相同的随机模式，使 `x[8:12]` 重复 `x[0:4]` 的 keep/drop 决策；global offsets 让两段分别
  使用 `F(seed,0..7)` 与 `F(seed,8..15)`。（来源：`msg-de0d18a0fc033e9bc227`）
- [纠错] 场景：判断 `p=0.5` 时不同 seed 调用的输出期望。我说“二者的元素数值期望应该均为 `2x`”
  → 正确：`2x` 只是元素被保留时的一次实现值，两个可能输出是 `0` 与 `2x`，各以 `0.5` 概率出现，
  所以期望仍为 `x`。原因：inverted scaling 抵消的是 keep probability。（来源：
  `msg-b3abc48c6e1e28622474` → `msg-104f07bcfe8f077c1da1`）
- [纠错] 场景：比较相同 mask 下的不同输入。我说“输出结果不同，因为二者来自不同的输入 tensor”
  → 正确：若输入只在被丢弃的位置不同，差异会同时被清零，最终输出可以完全相同。原因：相同 seed、
  `p` 和 offset 映射只保证 mask 相同，输出差异还取决于被保留位置的输入值。（来源：
  `msg-b3abc48c6e1e28622474` → `msg-104f07bcfe8f077c1da1`）
- [纠错] 场景：判断重排并连续化后能否用相同 seed 恢复逻辑元素的决策。我说“能保证逻辑元素获得相同
  决策，因为 mask pattern 与输入元素连续性也没有关系”→ 正确：随机数绑定整数 global offset，而不
  跟随抽象逻辑元素；重排会改变“逻辑元素 → offset”的映射。原因：`tl.rand(seed, offsets)` 不知道元素
  身份。（来源：`msg-b75761f2040d877f95e4`）
- [转折] 在 `A → A.T.contiguous()` 的聚焦复查中，我独立追踪出 `b:1→2`、`d:3→1`，并说明前向与
  recompute 分别调用 `F(seed,1/3)` 和 `F(seed,2/1)`；由此把“相同 seed 保持随机序列”收紧为“只有
  offset 映射不变时，逻辑元素的决策才保持”。（来源：`msg-968fbd4a3650b4b92770`）
- [要点] Seeded dropout 相对显式 mask 节省了什么，又为什么不能据此断言更快？——它避免完整 mask
  tensor 的物化、保存和读取，但输入／输出 tensor、逐元素选择与缩放仍存在，并增加现场 `tl.rand`
  计算；因此状态从 `O(N)` 降为 `O(1)` 不等价于延迟必然降低。`p` 是两种方案共有的算子参数，不是被
  seed 替代的随机状态。（来源：`msg-b75761f2040d877f95e4`）
- [要点] 精确复现一次 seeded dropout 输出需要保持哪些条件？——相同 seed、PRNG 实现、`p`、输入值
  与 dtype、kernel 数值语义，以及相同的“逻辑元素 → global offset”映射；不同 seed 在本次运行中可以
  产生不同结果，但不能扩大成“一定不同”。（来源：`msg-d8dacacc542feb6fca95`）
- [转折] 第一版实现的 19 项行为测试全部通过，但源码 Review 发现 wrapper 使用 `BLOCK_SIZE=128`，与
  已接受契约的固定 `1024` 不一致；我随后对齐为 `1024`，复验仍为 19/19。这个过程表明黑盒行为测试与
  契约／源码 Review 能发现不同类型的偏差。（来源：`msg-4b0e208cb5ffe3dbdcc2` →
  `msg-e32a347c034133137f9a`）
- [纠错] 场景：解释 `n=2057,BLOCK_SIZE=1024` 的尾部 program。我写成 offsets
  “`[2048,2049,...,3072]`”，并只明确提到防止越界保存 → 正确：完整范围是半开区间
  `[2048,3072)`，有效范围为 `[2048,2057)`；`tl.load` 与 `tl.store` 都必须使用 boundary mask，纯计算
  的 `tl.rand` 不需要。原因：`tl.arange` 不含右端点，只有内存访问存在越界风险。（来源：
  `msg-d8dacacc542feb6fca95`）
- [纠错] 场景：计算 `n=1025,BLOCK_SIZE=1024` 的最后一个 program。我说“有效 lane 数为 1，无效数为
  1024”→ 正确：总 lane 数固定为 1024，所以 `1024=1+1023`，无效 lane 为 1023。原因：有效与无效
  lane 必须满足 lane 守恒。（来源：`msg-c9fb69b0b9e93d8c3a62` →
  `msg-2dd36a9ccdb0760afcea`）

## 遗留

- 无；本次记录范围内的纠错均已通过聚焦复查，Lesson 04 已关闭。
