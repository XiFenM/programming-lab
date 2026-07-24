# Lesson 01：AXPBY Benchmark 简报

本简报服务于第一轮 Triton 编程学习，只验证基本 benchmark 流程并形成初步性能直觉，不进行
系统性能研究。精确分位数、区间和原始浮点结果由 CSV 保存；第二轮性能专题再研究 profiler、
多轮统计、cache、硬件计数器和更完整的 baseline。

## 1. 实验配置

| 项目 | 本次配置 |
| --- | --- |
| 日期 | 2026-07-24 |
| GPU | current device 0，NVIDIA A100-SXM4-80GB；系统共 8 张同型号 GPU |
| Driver | 580.159.03 |
| Python | 3.12.13 |
| PyTorch | 2.13.0+cu130 |
| Torch CUDA runtime | 13.0 |
| Triton | 3.7.1 |
| 输入 | float32，`alpha=1.234`，`beta=2.345` |
| Block size | 128、256、512、1024 |
| 主矩阵 size | `2**12`、`2**16`、`2**20`、`2**24` |
| 尾块 size | `2**20`、`2**20 + 17` |
| `do_bench` | `warmup=25 ms`、`rep=100 ms`、`quantiles=[0.5, 0.2, 0.8]` |

运行命令：

```bash
uv run --frozen python -m pytest -q gpu/triton/lesson01_vector_ops_test.py
uv run --frozen python -m gpu.triton.lesson01_vector_ops_benchmark
```

课程中已验证 correctness tests 为 `58 passed`。Benchmark 测量现有 `ops.axpby` wrapper，输入
张量在计时 callable 外创建，output allocation 属于 wrapper。`do_bench` 使用 GPU event 处理
异步执行并在正式采样前触发 JIT；它测量的不是完整 CPU wall-clock。

AXPBY 对每个有效元素读取 `x`、读取 `y`、写入 `output`，因此本简报使用：

```text
effective_bytes = 3 * N * sizeof(float32)
effective_gbps = effective_bytes / runtime
```

它是算法有效带宽，不是硬件计数器测得的实际 DRAM 带宽。p50 用作中心值；完整
p20/p50/p80 延迟和 GB/s 下界/中心/上界保存在 detailed CSV。

## 2. 保存结果

### 2.1 主矩阵 p50 有效 GB/s

| Size | BS=128 | BS=256 | BS=512 | BS=1024 |
| ---: | ---: | ---: | ---: | ---: |
| `2**12` | 6.000 | 6.000 | 6.857 | 6.857 |
| `2**16` | 109.714 | 109.714 | 109.714 | 96.000 |
| `2**20` | 819.200 | 768.000 | 877.714 | 877.714 |
| `2**24` | 1489.455 | 1585.548 | 1611.541 | 1624.860 |

### 2.2 尾块 p50 对照

| Block size | Exact p50 (µs) | Tail p50 (µs) | 延迟变化 | Exact GB/s | Tail GB/s | GB/s 变化 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 128 | 15.360 | 15.360 | 0.00% | 819.200 | 819.213 | +0.002% |
| 256 | 16.384 | 15.360 | -6.25% | 768.000 | 819.213 | +6.67% |
| 512 | 14.336 | 16.384 | +14.29% | 877.714 | 768.012 | -12.50% |
| 1024 | 15.360 | 16.384 | +6.67% | 819.200 | 768.012 | -6.25% |

原始产物：

- [主矩阵 detailed CSV](../../../../experiment_results/lesson01/axpby_block_size/axpby_block_size_detailed.csv)
- [主矩阵图](../../../../experiment_results/lesson01/axpby_block_size/axpby_block_size.png)
- [主矩阵 HTML](../../../../experiment_results/lesson01/axpby_block_size/results.html)
- [尾块 detailed CSV](../../../../experiment_results/lesson01/axpby_tail_block/axpby_block_size_detailed.csv)
- [尾块图](../../../../experiment_results/lesson01/axpby_tail_block/axpby_tail_block.png)
- [尾块 HTML](../../../../experiment_results/lesson01/axpby_tail_block/results.html)

## 3. 预测与尾块复盘

### 3.1 证据说明

主矩阵首次运行前没有保存预测，不能事后补写为事前预测。以下预测只针对当时尚未运行的 P02
尾块实验。

### 3.2 P02 尾块实验前预测

记录时间：2026-07-24，运行实验之前。

1. 尾块尺寸的 p50 延迟预计上升、近似不变，还是变化会被运行噪声淹没？

   预测：我认为尾块的延迟可能有非常小的上升，但这种变化会被运行噪声淹没。因为对于所有
   program是并行执行的，+17的输入大小影响启动时只多启动了1个program。而2**20这个规模按照
   我们设置的block_size，原本就会启动 1024~8192个program。那么在这种规模下，我再多启动
   1个program变成1025~8193个program，相对于原本的情况影响非常小。这种程度的影响，运行
   噪声的影响会更大一些。

2. 哪个 block size 可能对额外 program 最敏感？为什么？

   预测：block_size=1024受到的影响可能更大一些。因为此时需要启动的program从1024个变成了
   1025个，影响在千分之一左右。而对于其他的block_size，影响估计只有两千分之一、四千分之一.

3. 有效 GB/s 预计升高还是降低？注意分子也增加了 17 个有效元素。

   预测：有效GB/s肯定下降。因为多处理了一整块的数据。虽然分子增加了17个有效元素，但实际
   处理了128、256、512和1024个这么多的元素。之前用于测试的都是2的整次幂，都是充分利用程序
   中计算和带宽能力的。

4. 什么结果会让你承认预测不成立？

   尾块测试中延迟出现了5%以外的波动和有效GB/s升高。

### 3.3 P02 实验后复盘

#### 哪些预测得到支持？

按照原本的标准，关于延迟变化不大的预测是被推翻的。BS=256 已经满足5%以外的波动且有效GB/s
升高；BS=512 延迟更达到 +14.29%。但在实验中发现，计时台阶大约在1.024微秒，而整个kernel的
平均延迟在14-18微秒左右。这就导致了计时台阶的波动就已经超过了5%，所以这本质属于实验设计
不合理。

而对于BS=1024受影响更敏感的预测，在当前环境的实验中获得有限支持。但只有一两个计时台阶且
区间重叠，不能推广为普遍规律。

#### 哪些预测被推翻？

有效GB/s肯定下降的预测被推翻。有效GB/s实际上不一定下降。这是由于在gpu上，masked的load
store到了最终硬件执行层，并不一定真的完整做了有效显存读写。甚至，由于分母上计时的波动，
也有可能上升。根据gbps的计算：

```text
tail_gbps / exact_gbps = (N_tail / N_exact) × (t_exact / t_tail)
```

N+17 会增大有效字节分子。只要耗时没有按更大比例增加，有效 GB/s 就不会下降，甚至会上升；
这不代表实际 DRAM 流量或物理带宽提高。

#### 我对 masked-out lane 的显存行为有什么新理解？

现在，我知道了masked-out的lane的显存行为到了硬件执行上当mask/predicate=False 时，对应
地址的 load/store 确定不发生；但地址、谓词和部分算术计算仍可能发生。mask在ptx底层执行时
就编译为 guard predicate，如果为false，就直接不执行读写行为了。这也就是之前masked load
store不一定做了全部block的读写行为的原因。

但实际上的读写数据量依旧可能更多，这是由于GPU 会合并 active lane 的地址，并按照 memory
transaction 粒度访问显存。A100 这类 GPU 的 global-memory access 使用 32-byte segment。

此外，虽然阻止了无效lane的显存冗余行为，但尾program依旧会执行地址计算、逻辑调度等额外
操作，并不是完全省去了冗余行为。

#### 为什么 program 数量不能直接线性换算成耗时？

因为在gpu硬件中，并行计算资源和显存资源都是有限的。并行的program不可能无限的线性扩展，
只能在资源有限的情况下做有限的扩展。编译后的 warps、寄存器和共享内存决定 program 在某个
SM 上的驻留；多个 program 可以同时驻留，资源不足时分波次执行。有时多出一个program，也有
可能直接延长了耗时，因为可能这个program要求资源过多或者正巧资源不够而排到下一批。

#### 当前数据最多能支持什么结论，不能支持什么结论？

- BS=128/256/512：跨轮变化方向不稳定，当前方法未检测到稳定方向。

- BS=1024：四轮均出现变慢迹象，但证据不足以确认一般规律。

- 结论仅适用于当前 A100、软件栈、float32、两个尺寸和单次 do_bench 方法。

## 4. 第一轮学习者简要总结

### 4.1 主矩阵观察

<待填写：用 3–5 句话说明 size 增长时有效 GB/s 的总体变化，以及为什么不能仅凭一次 p50
排名断言某个 block size 普遍最优。>

从目前的实验结果来看，随着size增长，三条block size曲线的有效GB/s也持续增长，且尚未看到拐点。
不能仅凭一次 p50排名断言某个 block size 普遍最优，是因为对于不同的size的输入数据，不同block size的kernel有不同的表现。
在2^20和2^24规模级别的输入数据测试中，BS=1024体现出优势有效 GB/s，但对于2^16规模级别下，BS=1024相较于其他BS配置又有劣势。

### 4.2 Benchmark 方法心得

<待填写：用 3–5 句话说明本次学会了怎样正确计时、什么是有效 GB/s，以及当前结果最重要的
限制。>

在本次benchmark中，我了解到了Triton中使用CUDA Event的计时方式，且其中的计时台阶机制。这对于后续设计实验计时以及实验结果中耗时延迟的时间波动判定有着重要意义。
benchmark中的有效带宽指标是很重要的，他衡量了kernel有效处理数据的吞吐性能。由于triton中是按block来批量处理数据，这个指标尤为重要，我们需要尽可能避免被无效数据的干扰。
当前实验结果仅是在本台A100机器上的结果，且由于kernel复杂度较低，单个kernel耗时在十几微秒的水平上，很容易受到计时台阶的影响，所以结果是相对不稳定的。

## 5. 第一轮简报评审（2026-07-24）

结论：**在第一轮 Triton 编程学习的简化范围内通过，P03 关闭**。两段总结已经覆盖本轮要求的
核心观察：有效 GB/s 随当前四个采样规模整体上升，不同规模下 block size 的相对表现会变化；
计时应使用 GPU event，并且当前十几微秒的 kernel 容易受到经验计时量化的影响。没有阻塞或
主要问题。

以下四项是保留给以后顺手修订的非阻塞意见，不改写学习者原文：

| 编号 | 严重程度 | 评审意见 | 状态 |
| --- | --- | --- | --- |
| P03-R1 | 次要 | 4.1 的“三条 block size 曲线”应为四条 | 已记录，非阻塞 |
| P03-R2 | 次要 | 两段 `<待填写>` 提示仍留在最终简报中，可在文字收尾时删除 | 已记录，非阻塞 |
| P03-R3 | 次要 | “不同 size 排名不同”足以反驳普遍最优，但还可明确补充：一次保存运行的 p50 会受采样和当前计时量化影响，不能据此确定稳定排名 | 已记录，非阻塞 |
| P03-R4 | 次要 | 有效 GB/s 的价值在于用 `3 * N * sizeof(float32) / time` 按逻辑有效工作量统一比较；它按定义不计 masked 尾 lane，不能解释成真实无效访存被消除，也不等于硬件 DRAM 带宽 | 已记录，非阻塞 |

这次结论只关闭“第一轮简略 benchmark 报告”任务，不代表完成系统性能研究。上述措辞建议以及
源码格式、静态类型收尾均保留在课程暂停检查点中。

## 6. 延期到第二轮性能专题

以下内容不作为 Lesson 01 第一轮学习的完成门槛：

- 多次独立实验、置信区间和更系统的统计分析；
- Nsight Systems / Nsight Compute 与真实 DRAM transaction、cache、occupancy 指标；
- cold-cache、warm-cache、批量 launch 和 CUDA Graph 的严格对照；
- Torch eager、预分配 output、kernel-only 等不同测量边界；
- 系统搜索 block size、`num_warps`、autotune 和 `resolve_block_size` heuristic；
- 更多 dtype、尺寸分布、GPU 型号和软件版本。
