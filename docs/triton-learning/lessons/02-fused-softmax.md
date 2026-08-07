# 第 02 课：Fused Softmax

## 1. 课程档案

| 字段 | 内容 |
| --- | --- |
| 课程编号 | `02` |
| 官方案例 | [`02-fused-softmax.py`](../../triton-tutorials/official/02-fused-softmax.py) |
| 教程快照 | Triton `main` 文档，下载于 2026-07-15 UTC |
| 学习状态 | 已完成 |
| 开始日期 | 2026-07-31 |
| 完成日期 | 2026-08-06 |
| 实践源码 | [`lesson02_fused_softmax.py`](../../../gpu/triton/lesson02_fused_softmax.py) |
| 测试代码 | [`lesson02_fused_softmax_test.py`](../../../gpu/triton/lesson02_fused_softmax_test.py)（37 个 GPU cases）；[`lesson02_fused_softmax_benchmark_test.py`](../../../gpu/triton/lesson02_fused_softmax_benchmark_test.py)（27 个 GPU cases） |
| 原始对话 | [02-A](../dialogues/02-fused-softmax.md)（29 条，暂停）；[02-B](../dialogues/02-fused-softmax-part2.md)（32 条，暂停）；[02-C](../dialogues/02-fused-softmax-part3.md)（153 条，结课段）；[02-D](../dialogues/02-fused-softmax-part4.md)（6 条，结课后性能答疑）；[02-E](../dialogues/02-fused-softmax-part5.md)（9 条，Log-softmax 回顾收尾快照） |
| 补充材料 | [`experiment_results/lesson02/softmax`](../../../experiment_results/lesson02/softmax/)：最终资源、性能 CSV 与 PNG |

### 环境基线

| 项目 | 版本或型号 |
| --- | --- |
| GPU | NVIDIA A100-SXM4-80GB；最终验收使用物理 GPU 3（`CUDA_VISIBLE_DEVICES=3`） |
| NVIDIA driver | 580.159.03 |
| CUDA Toolkit (`nvcc`) | 13.0，build 13.0.88 |
| Python | 3.12.13 |
| PyTorch | 2.13.0，CUDA runtime 13.0 |
| Triton | 3.7.1 |
| 设备属性 | 108 SM、每 SM 65,536 registers、166,912 bytes max shared memory、warp size 32 |

### 进度检查

- [x] 已完成课前知识定位
- [x] 已阅读完整讲解
- [x] 已解决当前问题
- [x] 已接受实践任务
- [x] 已提交第一版实现
- [x] 已完成至少一轮代码评审
- [x] 已处理全部阻塞问题
- [x] 已通过正确性与边界测试
- [x] 已完成知识复述与变式验收
- [x] 已总结并关闭本课
- [x] 已在课程结束或中断时后验导出原始对话

## 2. 学习目标与前置知识

### 本课目标

完成本课后，我应该能够：

1. 写出数值稳定的行级 softmax，并解释减去行最大值为什么不改变结果。
2. 从全局内存流量角度解释 kernel fusion 对带宽受限算子的价值。
3. 使用 `tl.max`、`tl.sum` 和广播完成一个 program 内的行级 reduction。
4. 为非 2 的幂列宽选择静态 `BLOCK_SIZE`，并为 max 与 sum 设计正确的 padding 值。
5. 区分普通“一行一个 program”网格与 persistent grid，解释
   `tl.num_programs`、`tl.range` 和 occupancy 的关系。
6. 识别官方 wrapper 的 shape、stride、dtype、资源和 API 稳定性边界。
7. 正确解释 softmax benchmark 的有效带宽，而不把它误认为实际 DRAM 带宽。

### 前置知识检查

| 知识点 | 当前证据 | 本课需要补充的内容 |
| --- | --- | --- |
| `program_id + arange + mask` | Lesson 01 已通过概念与实践验收 | 从一维分块迁移到二维矩阵的一整行 |
| `tl.constexpr` | Lesson 01 已掌握不同 launch 可选择不同特化 | 理解静态 row block 对 reduction 和资源用量的影响 |
| masked load/store | Lesson 01 已掌握 false lane 不压缩 tensor | 为不同 reduction 选择单位元 |
| PyTorch tensor shape/stride | 已在 wrapper 评审中使用 | 区分 row stride 与 column stride |
| softmax 数学定义 | 尚未在档案中验证 | 数值稳定变换、行归一化和特殊值 |
| reduction | 本课新主题 | `tl.max`、`tl.sum`、axis 与块内广播 |
| occupancy / persistent kernel | 本课新主题 | registers、shared memory、resident programs 与循环处理多行 |

### 课前预测

本次进入课程后直接开始了完整讲解，没有在讲解前收集学习者预测。以下内容不事后代填：

- 我认为这个案例要解决的问题是：未记录。
- 我预计一个 Triton program 会负责：未记录。
- 我最不确定的是：未记录。

## 3. 官方案例地图

### 文件组成与执行入口

| 源码位置 | 作用 |
| --- | --- |
| 24–39 行 | 导入 Torch/Triton，获取 active device，并定义 HIP/CDNA 判断 |
| 42–59 行 | 用多个 PyTorch 操作实现数值稳定的 `naive_softmax` |
| 63–70 行 | 估算 naive 与 fused 两种实现的全局内存流量 |
| 84–109 行 | 定义 persistent row-wise softmax kernel |
| 115–121 行 | 读取设备资源属性 |
| 124–175 行 | 选择 block/warps/stages，预编译，估算 occupancy 并启动 kernel |
| 186–190 行 | 用不规则矩阵 `1823×781` 对照 `torch.softmax` |
| 203–229 行 | 比较 Triton、`torch.softmax` 和 naive PyTorch 的有效 GB/s |

这是 Sphinx-Gallery 教程脚本，不是无副作用的库模块。直接导入或执行会立即：

1. 创建 GPU tensor；
2. 编译并运行正确性案例；
3. 执行 98 个列宽、3 个 provider 的完整 benchmark；
4. 尝试显示性能图。

### 输入、输出与约束

| 项目 | shape | dtype | device | 布局/stride | 其他约束 |
| --- | --- | --- | --- | --- | --- |
| `x` | 二维 `[M, N]` | 官方只测试 float32 | active Torch device | 传入 row stride；column stride 被假定为 1 | `N > 0`，且 padded row 能放入可用片上资源 |
| `y` | 与 `x` 相同 | `empty_like(x)` | 与 `x` 相同 | 传入 row stride；column stride 被假定为 1 | 每个有效元素恰好写一次 |
| 一次行计算 | `[BLOCK_SIZE]` | 由输入与算术推导 | GPU on-chip | 静态连续 block | `BLOCK_SIZE = next_power_of_2(N)` |

官方 wrapper 通过 `n_rows, n_cols = x.shape` 隐式要求二维输入，但没有显式检查：

- 输入是否在支持的 GPU backend；
- `N` 是否大于 0；
- column stride 是否为 1；
- dtype 是否受支持；
- `BLOCK_SIZE` 是否超过编译器或设备资源限制；
- 输入与输出是否发生不支持的 alias。

### 高层执行流程

```text
x[M, N]
  -> Python wrapper 读取 M、N 和 row stride
  -> BLOCK_SIZE = next_power_of_2(N)
  -> 预编译一个 row-softmax 特化，读取 registers/shared-memory 用量
  -> 估算每个 SM 可同时驻留的 program 数 occupancy
  -> grid = min(NUM_SM * occupancy, M)
  -> 启动固定数量 persistent programs
       program pid 处理行：
       pid, pid + grid_size, pid + 2 * grid_size, ...
         -> masked load 一整行到静态 block，padding 为 -inf
         -> 块内 max reduction
         -> 减 max、exp
         -> 块内 sum reduction
         -> 归一化
         -> masked store 有效 N 列
  -> y[M, N]
```

## 4. 详细讲解

### 4.1 问题背景与 PyTorch baseline

对矩阵 `x ∈ R^(M×N)`，本课计算每一行的 softmax：

```text
y[i, j] = exp(x[i, j]) / Σ_k exp(x[i, k])
```

直接计算可能让较大的 `x[i, j]` 在 `exp` 时溢出。令一行最大值为 `m`，则：

```text
exp(x[j] - m) / Σ_k exp(x[k] - m)
= exp(x[j]) / exp(m) / (Σ_k exp(x[k]) / exp(m))
= exp(x[j]) / Σ_k exp(x[k])
```

因此减去同一个行最大值不会改变 softmax，却保证所有指数输入都小于等于 0；至少一个位置为
0，其指数为 1。它能显著降低上溢风险，但不表示所有包含 `NaN`、`+inf` 或全 `-inf` 的输入都
会得到有限结果。

官方 `naive_softmax` 把数学步骤写成多个 PyTorch 操作：

1. 每行求最大值；
2. 从每个元素减去行最大值；
3. 逐元素指数；
4. 每行求和；
5. 逐元素除以行和。

若这些步骤分别物化中间 tensor，理论全局内存流量为：

| 步骤 | 读取元素数 | 写入元素数 |
| --- | ---: | ---: |
| row max | `MN` | `M` |
| subtract | `MN + M` | `MN` |
| exp | `MN` | `MN` |
| row sum | `MN` | `M` |
| divide | `MN + M` | `MN` |
| 合计 | `5MN + 2M` | `3MN + 2M` |

合计搬运 `8MN + 4M` 个元素。融合 kernel 理想情况下只从 DRAM 读取一次 `MN`，最后写回一次
`MN`，即 `2MN` 个元素；大 `N` 时理论流量比接近 4 倍：

```text
(8MN + 4M) / (2MN) = 4 + 2/N
```

这只是带宽上限直觉，不是 4 倍运行时间的保证。归约、指数计算、occupancy、Torch 内核选择、
cache 和 launch 开销都会影响实测。

官方注释中“only `MN` bytes”少算了写回且省略了元素大小；后面的 `2MN` 比值才表达了实际意图：
读取 `MN` 个元素并写回 `MN` 个元素。

### 4.2 Triton 编程模型映射

| 层次 | 本案例中的含义 |
| --- | --- |
| 整个问题 | 对 `M` 行、每行 `N` 列执行独立 softmax |
| launch grid | 一维，仅启动能够驻留的 persistent program 数量 |
| 一个 program instance | 循环处理多行：`pid + k * num_programs` |
| 一次循环迭代 | 处理一整行 |
| 一个静态 block | `[BLOCK_SIZE]`，覆盖 `N` 个有效列与 padding lanes |
| 行内元素 | `col_offsets = 0 .. BLOCK_SIZE-1` |
| 归约 | `tl.max(..., axis=0)` 与 `tl.sum(..., axis=0)` 把一行压成标量 |

Lesson 01 中每个 program 通常只处理一个连续片段，grid 由问题长度直接决定。本课 grid 不等于
行数；program 会在 kernel 内循环取下一行。这是 persistent kernel 的核心变化。

### 4.3 Kernel 签名与参数分类

```python
@triton.jit
def softmax_kernel(
    output_ptr,
    input_ptr,
    input_row_stride,
    output_row_stride,
    n_rows,
    n_cols,
    BLOCK_SIZE: tl.constexpr,
    num_stages: tl.constexpr,
):
    ...
```

| 参数 | 类型/角色 | 何时确定 | 用途 |
| --- | --- | --- | --- |
| `output_ptr` | 输出指针 | launch 时 | 写回 softmax |
| `input_ptr` | 输入指针 | launch 时 | 读取矩阵 |
| `input_row_stride` | 运行时元素 stride | launch 时 | 从一行首地址移动到下一行 |
| `output_row_stride` | 运行时元素 stride | launch 时 | 计算输出行首地址 |
| `n_rows` | 运行时 shape | launch 时 | 控制 persistent row loop 的终点 |
| `n_cols` | 运行时 shape | launch 时 | 生成有效列 mask |
| `BLOCK_SIZE` | `tl.constexpr` | 编译/特化时 | 决定静态行 block 和 reduction 宽度 |
| `num_stages` | `tl.constexpr` | 编译/特化时 | 控制 `tl.range` 的软件流水阶段数 |
| `num_warps` | launch meta-parameter | 编译/launch 配置时 | 决定一个 program 使用多少 warps |

`input_row_stride` 和 `output_row_stride` 的单位是元素，不是字节。代码没有接收 column stride，
因此 `row_start_ptr + col_offsets` 只适用于行内相邻元素在内存中连续的布局。

### 4.4 Kernel 逐段解析

#### Persistent program 与行索引

```python
row_start = tl.program_id(0)
row_step = tl.num_programs(0)
for row_idx in tl.range(row_start, n_rows, row_step, num_stages=num_stages):
    ...
```

若 `M=10`、只启动 `P=3` 个 program：

```text
pid 0 -> rows 0, 3, 6, 9
pid 1 -> rows 1, 4, 7
pid 2 -> rows 2, 5, 8
```

每一行只属于一个 program，行之间没有数据依赖，因此不需要原子操作或跨 program 同步。
`tl.num_programs(0)` 读取本次实际 grid 的 axis-0 大小，而不是设备 SM 数或 `n_rows`。

#### 行指针与静态列索引

```python
row_start_ptr = input_ptr + row_idx * input_row_stride
col_offsets = tl.arange(0, BLOCK_SIZE)
input_ptrs = row_start_ptr + col_offsets
```

`row_start_ptr` 定位当前行首元素。`col_offsets` 必须具有编译期静态长度，所以 wrapper 把
`N` 向上扩到 2 的幂。对于官方测试的 `N=781`：

```text
BLOCK_SIZE = 1024
有效 offsets = 0..780       共 781 个
padding offsets = 781..1023  共 243 个
```

这里的 padding 只是静态 block 中的逻辑 lanes，不会修改输入 tensor 的 shape，也不会先创建
一份真正补齐到 1024 列的 GPU tensor。

#### Mask 与 reduction 单位元

```python
mask = col_offsets < n_cols
row = tl.load(input_ptrs, mask=mask, other=-float("inf"))
```

padding lane 必须参与后续的 `tl.max` 和 `tl.sum`，因此不能像纯 elementwise 案例那样忽略其
值。填 `-inf` 有两个连续作用：

1. `max(valid_values ∪ {-inf}) = max(valid_values)`，不改变最大值；
2. 减去有限行最大值后，padding 仍为 `-inf`，而 `exp(-inf) = 0`，也不改变指数和。

这体现了 reduction mask 的核心规则：padding 应映射到相应运算的单位元。max 通常用 `-inf`，
sum 通常用 0；本例用一次 `-inf` 同时满足两阶段需求。

#### 行级 reduction、广播与归一化

```python
row_minus_max = row - tl.max(row, axis=0)
numerator = tl.exp(row_minus_max)
denominator = tl.sum(numerator, axis=0)
softmax_output = numerator / denominator
```

`row` 是形状 `[BLOCK_SIZE]` 的块级 tensor。两个 reduction 沿唯一的 axis 0 把它变成标量；
标量随后广播回整行：

```text
[BLOCK_SIZE] --max--> scalar --broadcast subtract--> [BLOCK_SIZE]
[BLOCK_SIZE] --sum--> scalar --broadcast divide----> [BLOCK_SIZE]
```

`tl.exp` 使用快速近似实现，官方将其类比为 CUDA `__expf`。这通常比严格数学库更快，但意味着
与 PyTorch reference 的验证应使用合理容差，而不是要求逐 bit 相等。

#### Store mask

```python
output_row_start_ptr = output_ptr + row_idx * output_row_stride
output_ptrs = output_row_start_ptr + col_offsets
tl.store(output_ptrs, softmax_output, mask=mask)
```

padding lane 在计算中会得到 0 或其他中间值，但 store mask 保证只写前 `N` 个有效位置。
load mask 负责为 reduction 定义安全值；store mask 负责阻止越界副作用，二者职责不同。

#### `num_stages`

`num_stages` 传给 `tl.range`，让编译器对循环迭代尝试软件流水。它描述编译器可安排的流水阶段，
不应简单理解成“手工创建了几份 shared-memory buffer”。实际寄存器、shared memory 和生成
指令仍需查看编译结果或 profiler。

### 4.5 Python wrapper、资源估算与 launch grid

#### Block、warps 与 stages

```python
BLOCK_SIZE = triton.next_power_of_2(n_cols)
num_warps = 8
num_stages = 4 if SIZE_SMEM > 200000 else 2
```

- `BLOCK_SIZE` 是能覆盖整行的最小 2 的幂。
- `num_warps=8` 表示一个 program 使用 8 个 warp 协作处理一行；这是手写 heuristic。
- 当前 A100 报告 `SIZE_SMEM=166,912`，所以官方分支选择 `num_stages=2`。

当 `N` 从一个 2 的幂加 1 时，静态 block 会翻倍。例如：

```text
N=2048 -> BLOCK_SIZE=2048
N=2049 -> BLOCK_SIZE=4096
N=8192 -> BLOCK_SIZE=8192
N=8193 -> BLOCK_SIZE=16384
```

有效数据只增加一列，但寄存器压力、reduction 宽度和 padding lanes 可能大幅增加，所以性能
曲线可能在这些边界附近出现台阶。

#### 预编译与资源读取

wrapper 先调用 `softmax_kernel.warmup(..., grid=(1,))` 得到特化后的 compiled kernel，再读取：

- `kernel.n_regs`：每线程寄存器用量；
- `kernel.metadata.shared`：每 program 的 shared-memory 用量。

`kernel._init_handles()` 以下划线开头，是私有 API。它适合解释当前教程实现，但生产代码依赖它
会承担 Triton 版本升级风险。

#### Occupancy

NVIDIA 分支先按 registers 估算每个 SM 能同时驻留多少 program：

```text
register-limited occupancy
= NUM_REGS / (n_regs * WARP_SIZE * num_warps)
```

再与 shared-memory 限制取最小值：

```text
occupancy
= min(register-limited occupancy, SIZE_SMEM / size_smem)
```

这里的 `occupancy` 是“每 SM 可驻留的该类 program 数”，不是常见报告中的百分比。随后：

```text
num_programs = min(NUM_SM * occupancy, n_rows)
```

当前 A100 有 108 个 SM。若资源允许每个 SM 驻留 2 个 program，且 `M` 足够大，grid 就会是
216，而不是 `M`。这 216 个 program 通过循环共同覆盖全部行。

HIP/CDNA 分支还考虑 VGPR 池和每 CU 最大 resident waves；这是跨 backend 的资源模型差异，
不是 softmax 数学本身的一部分。

### 4.6 内存访问、数据布局与并行性

每次处理一行时，有效列地址连续，有利于合并访存。输入只从全局内存加载一次，中间的 max、
减法、exp、sum 和除法留在 program 的片上生命周期内，最后只写一次输出。

“留在 SRAM”是教程级概括，不保证所有中间量都物理位于某一种存储：

- 标量和块值可能主要使用 registers；
- reduction 可能需要 warp shuffle 或 shared memory；
- 资源压力过高时可能 spill 到 local memory，破坏理想流量模型。

行与行之间独立；行内 reduction 则需要同一个 program 中参与该行的 warps 协作。把一行拆给
多个独立 program 会额外需要跨 program reduction 或多阶段 kernel，本教程有意避免这种复杂度。

wrapper 只传 row stride。以下布局并不自动受支持：

- 转置矩阵导致 `stride(1) != 1`；
- 取每隔一列的 view；
- 需要负 stride 或任意二维 stride 的输入。

如果要支持它们，应额外传入 input/output column stride，并把列地址改为
`col_offsets * col_stride`；或者在 wrapper 中强制 `.contiguous()` 并清楚记录复制成本。

### 4.7 正确性验证

官方用例：

```text
shape = [1823, 781]
dtype = float32
BLOCK_SIZE = 1024
reference = torch.softmax(x, axis=1)
assertion = torch.allclose(...)
```

两个不规则维度分别覆盖：

- `M=1823` 不一定能被 persistent program 数整除；
- `N=781` 不是 2 的幂，验证了 243 个 padding lanes。

2026-07-31 在当前 A100、PyTorch 2.13.0、Triton 3.7.1 环境完整执行官方脚本，正确性断言和
后续 benchmark 均通过，进程退出码为 0。

这一条随机 float32 用例仍未覆盖：

- `M=0`、`N=0`、单行、单列和超大 `N`；
- float16、bfloat16、float64；
- 非连续或 column stride 不为 1；
- 极大有限值、`NaN`、`+inf`、全 `-inf`；
- 输出每行和是否接近 1；
- wrapper 对错误 shape/device/layout 的异常契约；
- 不同当前 device 与多 GPU 行为。

后续实践测试应区分“与 Torch 一致”“满足 softmax 数学不变量”和“接口明确拒绝不支持输入”
三类证据。

### 4.8 Benchmark 与性能解释

官方 benchmark 固定 `M=4096`，扫描：

```text
N = 256, 384, ..., 12672
provider = Triton / torch.softmax / naive_softmax
```

报告指标：

```text
effective_gbps = 2 * numel * element_size / runtime
```

分子统一使用 fused 算法的最小逻辑流量：读一次输入、写一次输出。它适合用同一有效工作量比较
provider，但不是 profiler 测得的真实 DRAM 字节数。特别是 naive provider 实际有多个中间
tensor 和更高流量，因此它的“有效 GB/s”不能解释成硬件只搬运了分子中的字节。

本机完整运行的部分结果：

| `N` | Triton GB/s | Torch GB/s | Naive GB/s | 本次较快者 |
| ---: | ---: | ---: | ---: | --- |
| 256 | 382.24 | 551.64 | 175.71 | Torch |
| 1024 | 1093.50 | 1038.57 | 353.95 | Triton |
| 4096 | 1411.88 | 1333.05 | 349.84 | Triton |
| 6144 | 1450.44 | 1452.22 | 368.01 | 近似持平 |
| 8192 | 1478.84 | 1152.54 | 375.33 | Triton |
| 10240 | 1461.68 | 1510.18 | 384.26 | Torch |
| 12672 | 1486.07 | 1438.73 | 387.67 | Triton |

当前证据支持：

- fused Triton 明显快于由多个 eager PyTorch 操作组成的 naive baseline；
- Triton 与高度优化的 `torch.softmax` 谁更快依赖列宽；
- 不能把官方结尾“noticeably faster”推广为所有 shape、设备和版本的结论。

官方末尾还写“Triton is 4x faster than the Torch JIT”，但当前源码没有
`@torch.jit.script`，benchmark 的第三条线实际调用普通 `naive_softmax`。因此本课程把它记录为
“对 eager naive baseline 的比较”，不把该文字当作已验证的 Torch JIT 结论。

benchmark 每次调用还会新建并设置 stream，但不恢复先前 stream。它是教程测量代码，不应直接
当作应用库接口。正式实验需要记录 warm-up、分位数、stream、是否包含 output allocation、
独立重复次数和 GPU 当前负载。

### 4.9 容易误解或踩坑的地方

1. **Fusion 不等于少做数学运算。** 它主要避免把中间结果反复写入和读回 DRAM。
2. **`-inf` 不是任意 padding。** 它是 max 的单位元，并在 exp 后变成 sum 的单位元 0。
3. **Mask 不会缩短 reduction tensor。** padding lane 保留在静态 `[BLOCK_SIZE]` 中。
4. **一个 program 不只处理一行。** persistent program 会按 grid stride 循环处理多行。
5. **`num_programs` 不等于 `NUM_SM`。** 它还乘以由 registers/shared memory 决定的 occupancy。
6. **`BLOCK_SIZE` 的翻倍会改变资源压力。** `N` 只增加 1 也可能触发完全不同的特化。
7. **传 row stride 不等于支持任意 stride。** 行内地址仍假设 `stride(1) == 1`。
8. **有效 GB/s 不等于真实 DRAM 带宽。** 尤其不能用该分子推断 naive 实现的物理流量。
9. **数值稳定不等于所有特殊值都有限。** `+inf - +inf` 和 `-inf - -inf` 仍可能产生 `NaN`。
10. **教程 wrapper 使用私有 compiled-kernel API。** Triton 升级时需要重新验证。

## 5. 我的理解与知识复述

### 当前心智模型

待学习者在答疑后用自己的话填写。建议覆盖：

- 为什么整行必须在一个 program 的静态 block 中；
- padding 如何先服务 max、再服务 sum；
- persistent grid 如何覆盖 `M` 行；
- fusion 节省的是哪一段全局内存流量。

### 我可以独立解释的问题

- [ ] 为什么 grid 不是简单的 `(M,)`？
- [ ] 一个 persistent program 依次处理哪些行？
- [ ] 为什么 masked load 使用 `-inf` 而不是 0？
- [ ] `BLOCK_SIZE`、`num_warps`、`num_stages` 分别控制什么？
- [ ] 为什么输入只传 row stride 仍不支持任意二维 view？
- [ ] 正确性和性能分别如何验证？
- [ ] 为什么同一个 benchmark 中 Triton 不必在每个 `N` 上都胜过 Torch？

### 尚不牢固的概念

- Persistent grid 如何从编译资源推导 program 数，以及它与普通 `(M,)` grid 的差别。
- `tl.range(..., num_stages=S)` 如何让多个行迭代同时处于 in-flight 状态。
- 流水深度、register/shared-memory 用量、occupancy 和延迟隐藏之间的取舍。

## 6. 问题与答疑记录

### Q01：Persistent programs 与 `num_stages` 软件流水

- **日期**：2026-07-31
- **我的原始问题**：“关于persistent programs与num_stages软件流水线这两方面，我没怎么理解。
  你可以更详细地讲讲吗？我想知道这两方面的功能主要是代码文件中哪些行的代码实现的，具体是
  怎么做的？软件流水线的整体流程是怎样设计的？为什么这样设计软件流水？”
- **提问时的理解/假设**：尚未形成确定模型；不清楚 persistent program 的行分配、occupancy
  grid 与 `tl.range` 流水分别对应哪些代码，也不确定 stage 是否等同于固定代码步骤。
- **讲解与回答**：

  Persistent 与软件流水作用于不同层次：

  ```text
  persistent grid：决定启动多少个长生命周期 program，以及每个 program 处理哪些行
  num_stages：决定同一个 program 的行循环中，允许多少个迭代同时处于 in-flight 状态
  ```

  Persistent 部分由以下代码共同实现：

  1. 115–119 行读取 SM、register、shared-memory 和 warp-size 资源。
  2. 142–147 行先编译当前 `BLOCK_SIZE/num_warps/num_stages` 特化，取得真实 `n_regs` 和
     `size_smem`。
  3. 148–168 行根据 registers、shared memory 和 backend 估算每 SM resident programs。
  4. 169–171 行计算 `P = min(NUM_SM * occupancy, n_rows)`。
  5. 173–174 行只启动 `P` 个 program，而不是 `n_rows` 个。
  6. 88–90 行让 pid 为 `p` 的 program 处理 `p, p+P, p+2P, ...` 行。

  `tl.num_programs(0)` 返回本次 axis 0 实际 launch 的 program 数 `P`。使用 grid-stride 行循环
  后，每行只属于一个 program，各 program 的行数最多相差 1。

  软件流水部分由以下代码连接：

  1. 86 行把 `num_stages` 声明为编译期 meta-parameter。
  2. 137 行由 wrapper 选择 2 或 4。
  3. 143–144 行用该值编译特化。
  4. 90 行把值传给 `tl.range(..., num_stages=num_stages)`；这一行才是对行循环施加流水属性的
     核心。
  5. 174 行启动此前特化的 compiled kernel。

  `tl.range` 的官方定义是让编译器尝试把该循环流水化，使最多 `S` 个循环迭代同时在途，并尝试
  流水化循环中的多数 load。它不是创建 `S` 个 CPU 线程，也不把源码机械切成 `S` 个固定阶段。
  这里的一个“迭代”是一整行 softmax。

  无流水时的概念顺序：

  ```text
  row A: load -> max -> exp -> sum -> divide -> store
  row B: load -> max -> exp -> sum -> divide -> store
  row C: load -> ...
  ```

  两级流水的概念时间线：

  ```text
  prologue:       发起/准备 row A 的 load
  steady step 1:  计算 row A，同时让 row B 的 load/地址工作提前进行
  steady step 2:  写回 row A、计算 row B，同时准备 row C
  steady step 3:  写回 row B、计算 row C，同时准备 row D
  epilogue:       排空最后仍在途的行
  ```

  这是帮助理解的依赖图，不是生成指令的一一对应承诺。编译器只能跨没有依赖的行迭代移动工作；
  同一行内部仍必须遵守 `load -> max -> exp -> sum -> divide -> store` 的数据依赖。

  这样设计的原因：

  - 不同 softmax 行完全独立，天然允许跨行重叠。
  - global-memory load 有较长延迟，只串行处理一行时，program 可能在等待数据。
  - 让下一行的 load 提前在途，可以用当前行的 reduction/exp 计算覆盖部分等待。
  - persistent program 本来就会循环多行，给软件流水提供了稳定、重复的 loop body。
  - program 数按 occupancy 控制，目标是让全部 persistent programs 能长期驻留并不断取得新行。

  代价是多个在途迭代的值必须同时存活，通常需要 multi-buffering，从而增加 registers 或 shared
  memory。资源增加可能反过来降低 occupancy，因此 `num_stages` 不是越大越好。

- **最小例子或推导**：

  若 `M=10`、最终 launch `P=3`：

  ```text
  pid 0 -> rows 0, 3, 6, 9
  pid 1 -> rows 1, 4, 7
  pid 2 -> rows 2, 5, 8
  ```

  对 pid 0 而言，软件流水考虑的是它自己的 0、3、6、9 四次循环迭代。例如 `S=2` 时，row 0
  计算期间可以让 row 3 的部分 load 工作在途；它不会让 pid 0 去处理 pid 1 的 row 1。

  本机对官方 kernel、`M=4096`、`N=781`、`BLOCK_SIZE=1024`、`num_warps=8` 的探索性编译：

  | stages | registers/thread | shared/program | register occupancy | shared occupancy | 最终 occupancy | programs | latency |
  | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
  | 1 | 32 | 32 B | 8 | 5216 | 8 | 864 | 0.027193 ms |
  | 2 | 32 | 4,128 B | 8 | 40 | 8 | 864 | 0.029188 ms |
  | 4 | 40 | 12,320 B | 6 | 13 | 6 | 648 | 0.028467 ms |

  三个版本均与 `torch.softmax` 一致。该表只是一轮理解性实验：它能证明更深流水改变了
  multi-buffering 与资源占用，并显示 4 stages 降低 occupancy；延迟差异很小，不能据此宣布
  1 stage 普遍最优。官方 A100 heuristic 因 `SIZE_SMEM=166,912 < 200,000` 选择 2 stages。

- **最终结论**：

  ```text
  persistent = 用有限 resident programs 循环覆盖全部行
  pipeline   = 在每个 resident program 内重叠多个独立行迭代
  ```

  Persistent 解决“长期由谁取活干”，software pipeline 解决“一个 program 取到连续多行后怎样
  减少等待”。更深流水增加潜在延迟隐藏，也增加 live state；最终要在 latency hiding 与
  occupancy 之间平衡。

- **学习者复述与校准**：

  1. `M=10、P=3` 时，学习者正确给出 `pid=1 -> rows 1, 4, 7`，persistent 行分配已确认。
  2. 学习者理解到不同在途工作可能分别处于 load、compute 或 store，但“两个 stage 的工作互相
     独立”需要改成“两个独立的循环迭代可以同时在途”。stage 不是两个独立工人或两个固定代码
     阶段；同一行内部的数据依赖仍不可打乱。
  3. 学习者正确识别更深流水需要更多 shared memory/register。机制上通常先表现为每 SM resident
     programs 减少、occupancy 和延迟隐藏能力下降，而不是直接“拖慢单个 stage”。只有发生
     register spilling 等情况时，单个 program 才可能因额外 local-memory 流量明显变慢。

  更准确的工厂类比是：流水更深需要为每条生产线准备更多在制品存储和工具；厂房总空间有限，
  因而能并行运行的整条生产线变少。若在制品放不下而被迫存到场外仓库，才类似 spilling 带来的
  额外运输开销。

- **是否解决**：核心模型已确认，措辞校准完成。
- **衍生问题**：Q02；也可进一步检查编译 IR/PTX 中实际发生了哪些 load 前移与 buffer 分配，
  但这不是理解本课控制流的前置条件。

### Q02：Triton softmax 与 CUDA 动态任务型 persistent kernel 是否相同

- **日期**：2026-07-31
- **我的原始问题**：“triton里的persistent 好像与其他所讲的cuda的persistent kernel不太
  一样。我记得cuda的persistent kernel好像会有while循环，持续接收处理传过来的task。”
- **提问时的理解/假设**：经典 CUDA persistent kernel 应是长时间运行的 worker，通过
  `while` 循环持续从任务队列接收工作；本课 Triton 使用有界 `for` 和静态行号，因此看起来不
  属于同一种机制。
- **讲解与回答**：

  这个观察成立，但差别在任务分配策略，不在 persistent 的共同核心。广义 persistent execution
  的共同点是：

  ```text
  不为每个 work item 创建一个独立 block/program；
  启动受控数量的长期 worker；
  每个 worker 在退出前处理多个 work items。
  ```

  常见实现可以分成：

  | 形式 | 循环 | 任务来源 | 适用工作 |
  | --- | --- | --- | --- |
  | 静态 grid-stride | 有界 `for` | `pid + k * P` 预分配 | 数量已知、成本均匀 |
  | 动态有限队列 | `while` + 退出条件 | atomic counter / dequeue | 成本不均、需要动态均衡 |
  | 在线常驻服务 | `while (!stop)` | host/device queue、ring buffer | 任务持续到达、减少反复 launch |

  与本课最接近的 CUDA 伪代码：

  ```cpp
  __global__ void softmax_rows(..., int num_rows) {
    for (int row = blockIdx.x; row < num_rows; row += gridDim.x) {
      process_one_row(row);
    }
  }

  int blocks = num_sms * blocks_per_sm;
  softmax_rows<<<blocks, threads_per_block>>>(...);
  ```

  动态任务版本则更像：

  ```cpp
  __global__ void workers(Task* tasks, int task_count, int* next_task) {
    while (true) {
      int task = atomicAdd(next_task, 1);
      if (task >= task_count) {
        break;
      }
      process(tasks[task]);
    }
  }
  ```

  如果任务会在 kernel 运行期间不断到达，循环还可能等待队列并由 sentinel/stop flag 退出。

  本课 Triton 对应关系：

  ```text
  tl.program_id(0)  ≈ blockIdx.x
  tl.num_programs(0) ≈ gridDim.x
  tl.range(pid, M, P) ≈ for (row = blockIdx.x; row < M; row += gridDim.x)
  Triton program ≈ 共同处理一行的 CUDA thread block/CTA
  ```

  官方称它为 persistent，是因为 host 只启动按 occupancy 计算的 resident program 数，program
  不处理完一行就退出，而是复用自身去处理多行。它同时也是一个 program-level grid-stride loop。

  Softmax 行数和地址在 launch 时已知，且同 shape 下每行工作量几乎一致，所以静态分配具有：

  - 不需要 global atomic counter；
  - 不需要任务队列、空队列等待或退出协议；
  - 相邻 pid 在同一轮处理相邻行；
  - 每个 program 的行数最多相差 1；
  - 控制流和性能更容易推导。

  如果 work item 成本高度不均，静态 `pid + kP` 可能让某些 program 提前结束、另一些仍很忙；
  此时动态队列型 persistent workers 可能改善负载均衡，但会引入 atomic、队列竞争和更复杂的
  终止协议。

- **最小例子或推导**：

  ```text
  已知 1000 行、每行成本相近：
    静态 grid-stride 足够，任务顺序可直接计算。

  已知 1000 个稀疏图任务、每个耗时相差数百倍：
    动态 atomic/dequeue 更可能避免 worker 间严重失衡。

  任务由 CPU 在数秒内持续提交：
    长期 while + queue 的在线 persistent service 才符合问题形态。
  ```

- **最终结论**：本课不是“持续等待外部任务”的 server-style persistent kernel，而是 CUDA
  grid-stride persistent threads 思路在 Triton program 粒度上的静态、有界版本。两者属于同一
  persistent 家族，但 work distribution 分别是静态行号和动态任务队列。
- **学习者确认**：“耗时差异很大的大量任务更适合用动态的调度分配，可以让已经完成先前耗时
  短任务的空闲处理单元继续处理。”
- **术语校准**：结论正确；更精确地说，是完成得早的 persistent worker program/CTA 继续
  dequeue。它之后可能仍在原 SM 上运行，但调度逻辑的主体是软件 worker，不应直接表述成某个
  固定硬件处理单元主动从队列取任务。
- **是否解决**：是。
- **衍生问题**：若后续学习不规则 workload，可比较静态 grid-stride、atomic counter 和真正
  在线任务队列的成本与终止语义。

### Q03：Occupancy 的正式定义是什么

- **日期**：2026-07-31
- **我的原始问题**：“先前经常提到 occupancy 下降。occupancy 到底是什么？有没有相对正式的
  定义？”
- **提问时的理解/假设**：尚待学习者复述；需要先区分源码中的整数 `occupancy`、CUDA 正式的
  warp occupancy 百分比和硬件实际利用率。
- **讲解与回答**：

  NVIDIA 对 CUDA kernel occupancy 的正式定义是：

  ```text
  occupancy =
      每个 SM 上的 active warps
      --------------------------------
      该 SM 支持的最大 active warps
  ```

  `active warp` 指已经驻留在 SM 上、尚未执行结束的 warp。它可能正在执行，也可能因等待
  global-memory 数据、指令依赖或同步而 stalled；后两种情况仍计入 occupancy。更细的调度状态
  应区分：

  ```text
  active：  已驻留且未结束
  eligible：active 中当前具备发射下一条指令条件的 warp
  issued：  本周期实际被 scheduler 选中发射指令的 warp
  ```

  因此 occupancy 不是：

  - SM 算力利用率；
  - 每周期真正发射指令的 warp 比例；
  - CUDA core 的忙碌比例；
  - 内存带宽利用率；
  - “程序完成了多少”的进度。

  它描述 SM 中可供 scheduler 切换、用于隐藏延迟的 resident warp 容量。一个 warp 等待时，
  scheduler 如果能从其他 eligible warps 中发射指令，等待时间就可能被覆盖。较高 occupancy
  通常扩大候选池，但候选 warp 也可能同时 stalled，因此高 occupancy 不保证高利用率或高性能。

  编译资源和 launch 配置决定理论上每个 SM 最多能同时驻留多少个 block/program。简化公式为：

  ```text
  resident_programs_per_sm =
      min(
          硬件 resident blocks 上限,
          floor(max_threads_per_sm / threads_per_program),
          floor(registers_per_sm / registers_per_program),
          floor(shared_memory_per_sm / shared_memory_per_program),
          其他架构资源限制
      )

  theoretical_occupancy =
      resident_programs_per_sm * warps_per_program
      ------------------------------------------------
      max_warps_per_sm
  ```

  实际硬件会按架构规定的 allocation granularity 分配 registers/shared memory，所以手算式是
  解释模型；正式计算还需采用目标架构的取整规则或 occupancy calculator。

  理论 occupancy 是由 kernel 资源和 launch configuration 推导出的上限。Profiler 报告的
  achieved occupancy 则根据运行期间每周期观察到的 active warps 求平均，再除以最大 warps；
  它可能因 grid 太小、负载不均或 kernel 尾部只剩少量 blocks 而低于理论值。

  本课官方源码 142–169 行先读取 compiled kernel 的 registers/shared-memory 用量，然后计算：

  ```python
  occupancy = min(
      registers 能容纳的 programs/SM,
      shared memory 能容纳的 programs/SM,
  )
  ```

  所以这里名为 `occupancy` 的变量实际保存“每个 SM 可驻留的 Triton programs 数”，即近似的
  `resident_programs_per_sm`，不是正式定义下 0 到 1 的 warp occupancy。170–174 行再用
  `NUM_SM * occupancy` 得到 persistent programs 的全设备 launch 数。

- **最小例子或推导**：

  当前 A100 每个 SM 最多驻留 2,048 threads，即 64 个 32-thread warps。本课固定
  `num_warps=8`，所以一个 Triton program 对应 8 warps，也就是 256 threads。

  对此前 `N=781` 的实测资源数据：

  | stages | 源码变量：programs/SM | resident warps/SM | 正式理论 occupancy |
  | ---: | ---: | ---: | ---: |
  | 1 | 8 | `8 × 8 = 64` | `64 / 64 = 100%` |
  | 2 | 8 | `8 × 8 = 64` | `64 / 64 = 100%` |
  | 4 | 6 | `6 × 8 = 48` | `48 / 64 = 75%` |

  因此先前所说 stages 4 让 occupancy 从 8 降到 6，更严谨的表述应是：

  ```text
  resident programs/SM：8 -> 6
  理论 warp occupancy：100% -> 75%
  ```

  这次二者能够直接换算，是因为 `num_warps=8` 固定。若比较不同 `num_warps`，只比较
  programs/SM 会误导：8 个四-warp programs 与 4 个八-warp programs 都是 32 resident warps，
  正式 occupancy 相同。

  即使 stages 4 的理论 occupancy 较低，它仍可能通过更强的单 program 指令级并行或软件流水
  隐藏延迟；反过来，100% occupancy 的所有 warps 也可能同时等待数据。因此性能必须结合
  eligible warps、stall 原因、issue rate、带宽和实测耗时判断。

- **最终结论**：

  ```text
  正式 CUDA occupancy = active resident warps / 架构允许的最大 resident warps
  本课源码 occupancy 变量 = 估算的 resident Triton programs per SM
  utilization/performance = 另一个问题，不能由 occupancy 单独推出
  ```

- **确认问题**：
  1. 某 SM 最多支持 64 warps；一个 program 有 4 warps，同时 resident 10 个 programs。
     理论 occupancy 是多少？
  2. 如果 profiler 显示 100% occupancy，能否据此断定计算单元很忙、kernel 已达到最佳性能？
- **学习者复述**：
  1. “理论 occupancy 应该是 `4 * 10 / 64 = 62.5%`。”
  2. “不能，因为这可能所有 warp 中计算单元也可能闲置在等待数据传输完成。不一定达到最佳
     性能。只能说计算单元全都在被用，但不一定用得好。”
- **术语校准**：
  1. 第一题计算与结论完全正确。
  2. 第二题关于“可能全部等待数据、不能推出最佳性能”的判断正确；但“计算单元全都在被用”
     与前句矛盾，也不是 occupancy 能证明的事实。100% occupancy 只能说明 active warp
     residency slots 已占满；这些 warps 可能没有 eligible 指令，算术/访存执行单元都可能闲置。
     更准确的复述是：“warp 驻留容量已占满，但执行资源不一定忙，更不能推出性能最优。”
- **是否解决**：是；正式定义、计算方法和 occupancy/utilization 区分均已确认。

## 7. 实践任务

实践分三层逐级开放，避免把行内 reduction、persistent 调度、软件流水和迁移变式同时引入：

| 层级 | 练习 | 主要证据 | 当前状态 |
| --- | --- | --- | --- |
| P01 | 普通 grid 的 fused softmax | reduction、padding、接口和边界测试 | **已完成** |
| P02 | Persistent softmax 与 stages 实验 | 行分配、occupancy、资源和计时证据 | **已完成** |
| P03 | Row-wise log-softmax 迁移 | 不照搬原式完成相关 reduction 算子 | 已完成概念过课；取消编码实践 |

核心 kernel、wrapper 和测试均由学习者实现。可以请求分级提示或共同定位失败，但提示默认先解释
概念和失败证据，不直接给出完整实现。

### 通用验收要求

- 实现放在 `gpu/triton/`；GPU 测试与实现同目录，保持在默认 CPU-only pytest/CI 范围之外。
- 使用 `@triton.jit` 完成核心计算，不在 wrapper 中调用 `torch.softmax` 代替待实现算子。
- 先验证正确性、数学不变量和错误输入，再做 persistent 转换或性能测量。
- 使用 `torch.testing.assert_close` 对照 PyTorch reference；性能不能代替正确性证据。
- 注释解释设计理由，不逐行翻译代码，也不逐行复制官方实现。

### P01：普通 grid 的 row-wise fused softmax（已完成）

#### 目的

先独立验证一行 softmax 的静态 block、masked load 和两次 reduction。此阶段故意使用一行一个
program 的普通 grid，暂不混入 occupancy、persistent 循环和软件流水。

#### 任务与接口

创建：

| 用途 | 路径 |
| --- | --- |
| Kernel / wrapper | `gpu/triton/lesson02_fused_softmax.py` |
| GPU tests | `gpu/triton/lesson02_fused_softmax_test.py` |

对外接口使用：

```python
def fused_softmax(x: torch.Tensor) -> torch.Tensor:
    ...
```

输入契约：

- `x` 必须是二维、CUDA、contiguous 的 float32 tensor，shape 为 `[M, N]`。
- `N` 必须大于 0，且 `next_power_of_2(N) <= 16384`；超出范围应在 wrapper 中清晰拒绝。
- `M` 可以为 0；此时返回 shape/dtype/device 相同的空 tensor，不启动零大小 grid。

输出必须与输入具有相同的 shape、dtype 和 device。

#### 必须满足

1. Launch grid 固定为 `(M,)`，一个 program 只负责一行。
2. `BLOCK_SIZE = triton.next_power_of_2(N)`，并作为 `tl.constexpr` meta-parameter 传给
   kernel。
3. 使用行号和 `tl.arange(0, BLOCK_SIZE)` 形成二维矩阵中的一行地址；有效列条件为
   `col_offsets < N`。
4. Masked load 的无效 lane 使用 `-inf`，随后依次完成 row max、减 max、exp、row sum 和
   divide，最后只 store 有效列。
5. 第一版固定使用 `num_warps=8`，不要提前加入 autotune 或基于 shape 的性能 heuristic。
6. 本阶段 kernel 中不使用 `tl.range`、`tl.num_programs`、编译结果的私有属性或 occupancy
   计算；这些内容保留给 P02。
7. Wrapper 对不支持的 ndim、device、dtype、layout 和列宽给出明确异常，不能依靠编译器偶然
   失败来定义接口。

#### 最低测试矩阵

正确输入至少覆盖：

| 类型 | shape / 数据 | 验证重点 |
| --- | --- | --- |
| 空行数 | `(0, 7)` | 不 launch，输出元数据正确 |
| 最小输入 | `(1, 1)` | 单元素结果为 1 |
| 非 2 的幂 | `(3, 7)`、`(19, 129)` | padding 与跨幂边界 |
| 恰为 2 的幂 | `(17, 128)` | 无 padding 的 reduction |
| 官方不规则形状 | `(1823, 781)` | 较大 M、非规则 N |
| 常数行 | 例如 `(4, 33)` 全为同一有限值 | 每列应为 `1 / 33` |
| 极大有限值 | 至少一行含 `10000` 附近且彼此不同的值 | 减最大值的数值稳定性 |

每个非空正确用例至少检查：

- 与 `torch.softmax(x, dim=1)` 在 `rtol=1e-4, atol=1e-6` 下接近；
- kernel 输出 `actual` 的每一行之和，即 `actual.sum(dim=1)`，接近全 1 tensor；
- 输出的 shape、dtype 和 device。

错误输入至少覆盖：CPU tensor、非二维 tensor、float64 tensor、非 contiguous 二维 view、
`shape=(3, 0)` 和 `N=16385`。异常类型和消息应稳定、可读。

#### 运行与验证

```bash
CUDA_VISIBLE_DEVICES=0 \
  uv run --frozen python -m pytest -q gpu/triton/lesson02_fused_softmax_test.py

uv run --frozen ruff check \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py

uv run --frozen ruff format --check \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py
```

#### 提交时的三项设计说明

在提交第一版代码时，同时用自己的话回答：

1. `M=5, N=781` 时 grid、`BLOCK_SIZE`、有效 lane 数和 padding lane 数分别是多少？
2. 为什么 `-inf` padding 既不改变 row max，也不改变后续指数和？
3. 为什么 `M=0` 可以直接返回，而 `N=0` 应由本练习的接口拒绝？

#### 允许提示

- **H1 概念提示**：只检查 program/row、block/column 和 mask 的映射。
- **H2 结构提示**：给出索引、地址和 reduction 的伪代码骨架，不给可直接提交的 kernel。
- **H3 定位提示**：根据失败测试或错误信息定位到 wrapper、索引、padding 或数值步骤。

遇到阻塞时可以指定请求 `H1`、`H2` 或 `H3`；也可以直接贴出第一版和失败输出进入评审。

#### 完成定义

- 两个目标文件均由学习者完成，最低正确/错误输入矩阵全部通过；
- 三项设计说明正确；
- Ruff check 和 format check 通过；
- 评审中的阻塞与主要问题全部关闭。

本阶段不以运行速度、persistent program 数或 `num_stages` 为验收条件。

### P02：Persistent softmax 与 `num_stages`（已完成）

#### 学习目标

本阶段把两个容易混在一起的问题分开验证：

1. **Persistent 调度正确性**：用有限 program 的静态 grid-stride 循环覆盖全部行，证明既不遗漏
   也不重复，而不是实现动态任务队列。
2. **软件流水的资源/性能取舍**：比较 `num_stages=1/2/4` 的编译资源、resident programs、
   理论 warp occupancy 与稳态 kernel 延迟；不预设 stages 越大越快。

P02 只要求当前 NVIDIA CUDA/A100 环境，不要求实现官方教程的 HIP/CDNA 分支。P01 普通 grid
版本必须保留，作为正确性和性能基线。

#### 产物与接口

| 用途 | 路径与要求 |
| --- | --- |
| Kernel / wrapper | 扩展 `gpu/triton/lesson02_fused_softmax.py`，保留 P01 API |
| GPU tests | 扩展 `gpu/triton/lesson02_fused_softmax_test.py` |
| 实验脚本 | 新建 `gpu/triton/lesson02_fused_softmax_benchmark.py` |

新增对外接口：

```python
def persistent_fused_softmax(
    x: torch.Tensor,
    *,
    num_stages: int = 2,
    num_programs: int | None = None,
) -> torch.Tensor:
    ...
```

- `x` 沿用 P01 的二维、CUDA、contiguous float32 与列宽契约。
- `num_stages` 只接受 `1`、`2`、`4`，并作为编译期参数传入 `tl.range`。
- `num_programs=None` 时根据编译资源计算 persistent grid；显式正整数用于测试指定的行分配，
  实际 grid 不超过 `M`。非法 stage 或非正 program 数应明确拒绝。
- `M=0` 时仍返回合法空 tensor，不 launch；选项的合法性不能依赖 kernel 偶然报错。

#### Persistent kernel 必须满足

1. 一个 program 从自己的 `tl.program_id(0)` 行开始，步长来自本次 launch 的
   `tl.num_programs(0)`。
2. 用带 `num_stages` 的 `tl.range` 依次处理该 program 负责的行；不能在 host 为每一轮重复
   launch，也不能引入原子任务队列。
3. 每次循环迭代复用 P01 已验证的完整行 softmax：静态 block、`-inf` padding、两次 reduction
   与 masked store。行与行之间不得共享归一化状态。
4. 固定 `num_warps=8`，不加入 autotune，确保实验只改变 `num_stages`。
5. `M` 不能整除 grid 时仍与 PyTorch reference 一致。提交时还需用商余分解说明：每个
   `row_idx` 为什么属于唯一的 `(pid, iteration)`。

#### 默认 grid 与资源证据

对给定 `BLOCK_SIZE`、`num_warps=8` 和 stage 特化，先用 `warmup` 得到 compiled kernel，再读取：

- 初始化 handle 后的 registers/thread；
- metadata 中的 shared bytes/program；
- 当前设备的 registers/SM、shared bytes/SM、SM 数、warp size 与 max threads/SM。

至少分别计算 register、shared-memory 和 thread 三个 resident-program 上限，并取最小值：

```text
resident_programs_per_sm = min(register_limit, shared_limit, thread_limit)
grid = min(M, SM_count * resident_programs_per_sm)

theoretical_warp_occupancy =
    resident_programs_per_sm * num_warps / max_warps_per_sm
```

shared bytes 为 0 时代表它不构成限制，不能发生除零。若计算结果小于 1，应在 wrapper 中给出
资源不足的清晰异常。compiled-kernel handle 属于版本敏感 API；把访问集中在一个小 helper 中，
写明兼容性边界，不把私有细节散落到 kernel 数学或测试各处。

#### 正确性与调度测试

除复用 P01 的 reference、row-sum 和输出元数据断言外，至少覆盖：

| `M, N` | 指定 programs | 验证重点 |
| --- | ---: | --- |
| `10, 7` | 3 | `M % P != 0`，各 program 迭代次数不同 |
| `257, 129` | 7 | 多轮循环与非 2 的幂列宽同时存在 |
| `2, 33` | 8 | grid 被 cap 到 `M`，不启动多余 program |
| `1, 1` | 1 | 单 program、单次迭代 |
| `0, 7` | 任一合法值 | 空 batch 不 launch |

对 `num_stages=1/2/4` 都至少运行一个 `M > P` 且 `M % P != 0` 的正确性用例。另测非法
`num_stages`、`num_programs=0` 和负数。测试不得断言某个 stage 必须最快，也不依赖某个固定的
register/shared-memory 数值。

#### 资源与性能实验

先不运行实验，提交以下四项预测；预测只需给方向和理由，不要求猜精确数值：

1. `M=10, P=3` 时三个 program 分别处理哪些行，为什么不会重复或遗漏？
2. stages 从 1 增到 4 时，register/shared-memory 用量与 resident programs/SM 更可能怎样变化？
3. 当设备可提供的 program capacity 大于等于 `M`、实际 grid 被 cap 为 `M` 时，提高 stages
   是否仍有跨行迭代可流水？
4. stages 4 的理论 occupancy 若低于 stages 2，它是否仍可能更快？需要什么实测才能判断？

实现后，在同一张空闲 GPU 上生成两个表：

1. 对 `M=4096, N=781` 和 stages 1/2/4，记录 registers/thread、shared/program、三个资源上限、
   resident programs/SM、全设备 grid 和理论 warp occupancy。
2. 对 `(256, 781)`、`(4096, 781)`、`(4096, 2049)`，比较 `torch_naive`、`torch_fused`、
   `triton_naive` 与 `triton_persistent` stages 1/2/4 的稳态端到端 median provider latency，并
   报告有效 GB/s。

实验问题采用学习者选择的“重复调用公开 provider 的实际稳态表现”：input、JIT 编译和
persistent resource/grid 初始化位于 timed closure 外；每次 closure 调用
对应的 provider function/wrapper，保留其参数检查、output 与中间 tensor 分配和 kernel/op launch。
persistent case 在初始化阶段计算一次 grid，计时时把 `grid[0]` 作为 `num_programs` 传给 wrapper，
避免重复不可摊销的资源探测。固定 `num_warps=8`，记录 GPU、软件版本、warm-up/rep 参数。input
初始化后先同步 GPU；benchmark 本身不计算 reference 或执行 correctness assertion。三个实验 shape
与 ordinary/persistent stages 1/2/4 的正确性由独立 GPU 功能测试验证，性能结果不能替代这些测试。
该实验不测首次 JIT/初始化的 cold-start latency，也不声称是排除 wrapper overhead 的 kernel-only
microbenchmark。

#### P02-C tests-first 交接（2026-08-06）

AI agent 已创建 `gpu/triton/lesson02_fused_softmax_benchmark_test.py`。测试保持在显式 GPU 范围，
不会进入默认 CPU CI。学习者实现目标为
`gpu/triton/lesson02_fused_softmax_benchmark.py`，测试所需最小接口如下。

固定实验配置：

```python
STAGES = (1, 2, 4)
SHAPES = ((256, 781), (4096, 781), (4096, 2049))
WARMUP_MS = <positive int>
REP_MS = <positive int>
```

`ResourceRecord` 为 dataclass，字段顺序固定为：

```text
size_m, size_n, num_stages,
registers_per_thread, shared_bytes_per_program,
register_limit, shared_limit, thread_limit,
resident_programs_per_sm, grid, theoretical_warp_occupancy
```

`BenchmarkRecord` 为 dataclass，字段顺序固定为：

```text
size_m, size_n, provider, num_stages,
warmup_ms, rep_ms, latency_ms, effective_gbps
```

必须实现三个可独立验证的函数：

1. `effective_gbps(*, size_m, size_n, element_size, latency_ms) -> float`
   - 分子只表示一个输入 read 和一个输出 write，即 `2 * M * N * element_size`；
   - 这是有效带宽，不声称等于硬件实际流量；
   - 非正或非有限 latency 明确抛含 `latency` 的 `ValueError`。
2. `derive_resource_record(resource, *, size_m, size_n, num_stages) -> ResourceRecord`
   - 复用 P02-B 的 register/shared/thread 公式；shared=0 时 `shared_limit=None`；
   - `grid` 保留 Triton launch 使用的一元 tuple，例如 `(648,)`；
   - theoretical occupancy 使用 resident programs、固定 8 warps 和 max warps/SM。
3. `measure_case(*, size_m, size_n, provider, num_stages, warmup_ms, rep_ms) -> BenchmarkRecord`
   - provider 只接受 `torch_naive`、`torch_fused`、`triton_naive`、`triton_persistent`；前三者
     要求 `num_stages=None`，`triton_persistent` 只接受 1/2/4；不一致配置必须在任何大 tensor
     分配前拒绝；
   - 返回正且有限的 median latency/effective GB/s，并原样记录 warm-up/rep。

计时污染边界：

- `measure_case` 在 timed closure 外创建 input、完成 JIT/warm-up，并为 persistent case
  读取一次 resource/grid；这些是当前重复调用场景中可摊销的一次性 setup；
- input 初始化后同步 GPU；benchmark 不执行 untimed provider correctness call 或 `assert_close`；
- timed closure 调用四种 provider 对应的 function/wrapper，保留每次调用的输入检查、output/中间
  tensor 分配与 launch；`triton_persistent` 必须传 `num_programs=grid[0]`，避免 wrapper 在每个
  样本中重复 resource introspection；`triton_naive` 继续调用其公开 wrapper；
- 正确性由 `lesson02_fused_softmax_test.py` 对三个 benchmark shape 和 persistent stages 1/2/4
  独立验证；`torch_naive_softmax` 也在 benchmark test 中单独对照 PyTorch；
- `triton.testing.do_bench` 必须显式收到 `warmup=warmup_ms`、`rep=rep_ms`；测试不比较谁最快，
  也不设置固定 latency/GB/s 门槛。

脚本入口最终应在同一设备上打印：

1. `M=4096,N=781` 的 stages 1/2/4 三行资源表；
2. 三个 `SHAPES` ×（三个非 persistent providers + persistent stages 1/2/4）共 18 行性能表；
3. GPU 名称、PyTorch/Triton 版本、`NUM_WARPS`、warm-up/rep 参数。

验收命令与当前状态：

```bash
CUDA_VISIBLE_DEVICES=3 \
  uv run --frozen python -m pytest -q \
  gpu/triton/lesson02_fused_softmax_benchmark_test.py
```

```text
当前 red：13 passed, 11 failed
失败覆盖 SHAPES、small-grid occupancy、提前配置校验和 Triton timing 参数转发
默认 pytest：20 passed in 1.56s
benchmark test Ruff/format/BasedPyright：通过
```

更新后的 24 个 cases 分别覆盖固定 schema、有效 GB/s 公式与非法 latency、资源公式/shared=0/
small grid、四种 provider 的组合校验、timing 参数转发，以及四种 providers（persistent 展开
stages 1/2/4）的小尺寸实际计时。测试由 AI agent 维护；
学习者只实现 benchmark 生产模块，不需要修改测试来迎合当前失败。

#### 运行与验证

```bash
CUDA_VISIBLE_DEVICES=<free-gpu> \
  uv run --frozen python -m pytest -q gpu/triton/lesson02_fused_softmax_test.py

CUDA_VISIBLE_DEVICES=<free-gpu> \
  uv run --frozen python -m pytest -q \
  gpu/triton/lesson02_fused_softmax_benchmark_test.py

CUDA_VISIBLE_DEVICES=<free-gpu> \
  uv run --frozen python gpu/triton/lesson02_fused_softmax_benchmark.py

uv run --frozen ruff check \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py \
  gpu/triton/lesson02_fused_softmax_benchmark_test.py \
  gpu/triton/lesson02_fused_softmax_benchmark.py

uv run --frozen ruff format --check \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py \
  gpu/triton/lesson02_fused_softmax_benchmark_test.py \
  gpu/triton/lesson02_fused_softmax_benchmark.py

uv run --frozen basedpyright \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py \
  gpu/triton/lesson02_fused_softmax_benchmark_test.py \
  gpu/triton/lesson02_fused_softmax_benchmark.py
```

#### 允许提示与完成定义

- **H1**：只复查 `pid / num_programs / row_idx` 的集合映射或 occupancy 术语。
- **H2**：指出应修改 P01 的哪个层次，以及资源公式所需字段，不给完整 kernel。
- **H3**：针对失败测试、编译错误或 benchmark 污染定位原因并给局部伪代码。
- **H4**：学习者持续阻塞或明确请求时，才给一个最小可运行片段；需要记录提示范围。

P02 完成要求：正确性与非法输入测试、唯一覆盖证明、资源表、稳态计时表和预测复盘齐全；Ruff、
格式、BasedPyright 通过；评审中的 blocking/major finding 全部关闭。性能没有固定胜负门槛，能用
资源、可流水迭代数和实测证据解释结果即可。P03 后在结课时按学习者范围决定取消。

### P03：Row-wise log-softmax 迁移（本课取消）

原计划把 max/sum reduction 迁移到 row-wise log-softmax。学习者在 P02 完成后明确结束 Lesson 02，
并要求减少核心学习以外的消耗；现有 persistent 调度、资源推导和性能评价已提供足够的变式与迁移
证据，因此 P03 不再作为本课 gate。2026-08-07 补充完成 softmax 与 log-softmax 的
概念和 kernel 数据流对比，但不新增实现、测试或 benchmark。

## 8. 实现与实验记录

### 实现文件

| 用途 | 路径 | 说明 |
| --- | --- | --- |
| Kernel / wrapper | `gpu/triton/lesson02_fused_softmax.py` | P01、P02-A、P02-B 最终版 |
| CPU grid helper | `gpu/triton/lesson02_fused_softmax_grid.py` | `Resource`/`compute_grid` 纯 Python 实现；默认 CI 无需 Torch/Triton |
| GPU tests | `gpu/triton/lesson02_fused_softmax_test.py` | 37 个用例；含默认路径、空 batch、真实资源 helper 与三个 benchmark shape 的独立正确性 |
| CPU grid tests | `tests/python/test_lesson02_fused_softmax_grid.py` | 6 个用例；进入默认 CI，覆盖三类资源限制、row cap、shared=0 和零 resident |
| Benchmark tests | `gpu/triton/lesson02_fused_softmax_benchmark_test.py` | AI agent 编写；27 个显式 GPU cases，当前全部通过 |
| Benchmark | `gpu/triton/lesson02_fused_softmax_benchmark.py` | P02-C 最终版；行为、静态检查和最终实验均通过 |

### 第一版设计

- 工作划分：第一版使用 `pid = tl.program_id(0)`，一个 program 处理一行；地址按
  `pid * N + col_offset` 计算。
- grid 与 block/tile：wrapper 使用 `(M,)` 和 `next_power_of_2(N)`；学习者正确推导
  `M=5, N=781` 时 grid 为 `(5,)`、block 为 1024、有效/padding lanes 为 781/243。
- mask 策略：masked load 使用 `-inf`，两次 reduction 后只 store 有效列。
- dtype/shape/stride 支持：wrapper 限定二维 CUDA contiguous float32，允许 `M=0`，拒绝
  `N=0` 和 padded block 大于 16384 的输入。
- launch 配置：第一版未显式传 `num_warps=8`，实际编译元数据为默认 4 warps，见 P01-R01。

第二版已在 launch 中显式指定 `num_warps=8`，并补充输出 row-sum 与六类非法输入测试。

### 第一版设计说明评审

1. **Grid/block/lane 推导：正确。** `(5,)`、1024、781、243 均正确。
2. **`-inf` padding：核心正确。** 它不会战胜有限有效值成为 max；减去有限 row max 后仍为
   `-inf`，其指数为 0，因此不改变指数和。本练习尚不要求定义 `NaN`、`+inf` 或全 `-inf` 行。
3. **`M=0` 与 `N=0`：第二次复述正确。** 学习者说明前者没有样本但样本内部 schema 有效，
   后续出现样本仍可计算；后者是样本内部/reduction domain 为空，无法计算，因此接口应明确
   拒绝。更正式的术语是“合法空 batch”与“已有 rows 的空 reduction domain”。

### P02 实践前预测（2026-08-05）

#### 学习者原始预测

1. `M=10, P=3` 时，三个 program 分别处理 `0/3/6/9`、`1/4/7`、`2/5/8`；认为这是根据
   `M` 和 `P` 连续合理安排的结果，因此不会重复或遗漏。
2. stages 增加时，为预取后续行可能需要更多 registers/shared memory，使每 SM 的 resident
   programs 变少。
3. 即使实际 grid 等于 `M`，也可能在前一批 programs 计算时预先启动后一批 programs 读取数据，
   因而仍可能形成跨行软件流水。
4. stages 4 可能需要四行存储；可以把一行再拆成小 blocks，降低每 program 资源需求并提高
   occupancy，然后用吞吐和延迟判断是否改善。

#### 预测复核与术语校准

| ID | 结论 | 复核 |
| --- | --- | --- |
| P02-PRED-01 | 映射正确，证明待补 | 三组行号完全正确；“合理安排”尚未证明覆盖的完备性与唯一性 |
| P02-PRED-02 | 方向正确，需保留不确定性 | 更多在途迭代可能延长值的 live range 或增加 buffering，资源可能增加、resident programs 可能下降；不保证 registers 与 shared memory 都增加 |
| P02-PRED-03 | 需修正 | `num_stages` 作用于一个 program 内的 `tl.range` 迭代；不同 programs 的 warp/block 调度属于硬件并发，不是这条循环的软件流水 |
| P02-PRED-04 | 未回答原问题 | 降低 tile 会改变行级 reduction 算法；“4 stages”也不等于必然存放四个完整行，不能用该改造解释 stages 4 在较低 occupancy 下仍可能更快 |

唯一覆盖可用整数除法的商余唯一性证明。对任意 `0 <= row < M`：

```text
pid = row mod P
iteration = floor(row / P)
row = pid + iteration * P
```

每个 row 都有这样一组商和余数，所以不会遗漏；余数与商都是唯一的，所以两个不同
`(pid, iteration)` 不会处理同一 row。

软件流水的目标时间线是同一个 program 内让相邻循环迭代部分重叠，例如尝试让第 `k+1` 行的
load 与第 `k` 行的计算在途。若 capacity 足够且实际 grid 被 cap 为 `M`，每个 program 只有一次
循环迭代，就没有“下一行迭代”可与当前行重叠。GPU 仍可交错执行不同 programs 的 warps，但那是
硬件 scheduler 的 latency hiding，不是 `tl.range(num_stages=...)` 的跨迭代软件流水。

即使 stages 4 降低理论 occupancy，它仍可能通过更多单 program 指令级并行或更早发起后续迭代
的访存，更充分地隐藏延迟；也可能因资源压力和 resident warps 减少而变慢。最低判断证据是在
相同 shape、grid、`num_warps` 和数据条件下比较 stages 2/4 的 compiled resources、理论
occupancy、稳态端到端 provider latency 与有效 GB/s；若 wrapper overhead 掩盖 stages 差异，
再把 kernel-only microbenchmark 或 profiler 的 eligible warps、stall reasons 和内存吞吐作为
解释机制的辅助证据，而非主要实际场景结论。

#### 第二次复述与状态

学习者确认最初把问题 4 误解成“如何提高 stages 4 的 occupancy”，并重新回答：

1. 商和余数唯一，因此能唯一确定每一行由哪个 program 处理。
2. 不同 programs 之间的执行属于硬件调度，不是 `num_stages` 的 program 内循环流水。
3. stages 4 可能因增加单 program 的“数据并行度”而更快，应比较延迟与吞吐。

| ID | 生命周期结果 | 复核证据 |
| --- | --- | --- |
| P02-PRED-01 | learner-revised -> verified -> closed | 余数唯一确定 `pid`，商唯一确定该 program 的 iteration，覆盖证明成立 |
| P02-PRED-02 | verified -> closed | 已使用“可能增加”而非固定资源结论，最终以 compiled metrics 为准 |
| P02-PRED-03 | learner-revised -> verified -> closed | 已区分不同 programs 的硬件调度与单 program 的 `tl.range` 流水 |
| P02-PRED-04 | learner-revised -> needs-more-work | 已识别 latency/throughput 证据，但“数据并行度”术语不正确，且解释取舍还需资源/occupancy 证据 |

PRED-04 的目标术语是**指令级并行与多个循环迭代在途**：stage 深度可能让同一 program 更早
发起后续独立行迭代的 load，并与当前迭代的计算/写回重叠；它不会把当前行自动切成更多并行
数据块。延迟和有效 GB/s 判断“是否更快”，compiled resources 与理论 occupancy 则解释它在
resident warps 变少时为什么仍可能更快或更慢。

#### P02-Q04：资源与 occupancy 怎样获得

- **学习者问题**：已理解 stages 增加的是指令级并行与延迟隐藏机会；延迟和有效 GB/s 可以
  实测，但 registers、shared memory、resident programs 和理论 occupancy 是否也能测、应怎样
  得到？
- **证据分层**：

  | 量 | 获得方式 | 性质 |
  | --- | --- | --- |
  | registers/thread | 初始化 compiled kernel handles 后读取 `compiled.n_regs` | 编译/装载产物报告，不是运行时平均值 |
  | shared bytes/program | 读取 `compiled.metadata.shared` | 编译产物报告的静态分配量 |
  | resident programs/SM | 用设备容量除以上述每 program 资源，并加入 thread 上限后取最小值 | 理论上限的教程级推导 |
  | theoretical occupancy | `resident programs × warps/program ÷ max warps/SM` | 由资源和 launch 配置推导 |
  | achieved occupancy | Nsight Compute 运行时采样 active warps | profiler 观测值，可能低于理论值 |

  当前 Triton 3.7.1 可按下面的最小方式读取编译资源；`_init_handles()` 和 `n_regs` 属于版本敏感
  API，应集中封装并在升级后复验：

  ```python
  compiled = persistent_kernel.warmup(
      ...,
      BLOCK_SIZE=block_size,
      num_stages=num_stages,
      num_warps=8,
      grid=(1,),
  )
  compiled._init_handles()
  registers_per_thread = compiled.n_regs
  shared_bytes_per_program = compiled.metadata.shared
  ```

  设备容量来自 Triton driver properties 与 Torch device properties：

  ```text
  register_limit = floor(registers_per_sm /
                         (registers_per_thread * warp_size * num_warps))
  shared_limit   = floor(shared_bytes_per_sm / shared_bytes_per_program)
  thread_limit   = floor(max_threads_per_sm / (warp_size * num_warps))

  resident_programs_per_sm = min(register_limit, shared_limit, thread_limit)
  max_warps_per_sm = max_threads_per_sm / warp_size
  theoretical_occupancy =
      resident_programs_per_sm * num_warps / max_warps_per_sm
  ```

  shared bytes 为 0 时，它不构成限制，不能直接做除法。实际 GPU 还按 allocation granularity 和
  架构 block 限制分配资源，因此这是课程和官方 wrapper 使用的解释性估算，不替代完整 occupancy
  calculator 或 profiler。

  当前 A100 的探索性编译数据可以直接验证计算链：

  | stages | registers/thread | shared/program | register limit | shared limit | thread limit | resident programs/SM | theoretical occupancy |
  | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
  | 1 | 32 | 32 B | 8 | 5216 | 8 | 8 | 100% |
  | 2 | 32 | 4,128 B | 8 | 40 | 8 | 8 | 100% |
  | 4 | 40 | 12,320 B | 6 | 13 | 8 | 6 | 75% |

  若需要运行时观测，本机 Nsight Compute 2025.3.1 提供 `LaunchStats` 与 `Occupancy` sections；
  achieved occupancy 对应 active-warps 类指标，例如
  `sm__warps_active.avg.pct_of_peak_sustained_active`。Profiler 会使运行变慢，只在正确性与基础
  benchmark 完成后做解释性采样，不放入 pytest。
- **答疑时状态**：指令级并行术语已修正；等待学习者用 stages 4 的数据独立复算 resident
  programs、理论 occupancy 和全设备 grid 后关闭 P02-PRED-04/P02-Q04。

#### 资源复算确认

学习者对 stages 4、`M=4096` 的独立计算：

```text
register limit = floor(65536 / (40 * 8 * 32)) = 6
shared limit   = floor(166912 / 12320) = 13
thread limit   = 2048 / (8 * 32) = 8

resident programs/SM = min(6, 13, 8) = 6
theoretical occupancy = 6 * 8 / (2048 / 32) = 75%
grid = min(4096, 108 * 6) = 648
```

六项结果均正确，并正确识别 stages 4 在此特化下受 registers 限制。P02-PRED-04 与 P02-Q04
现已 verified/closed；实践前预测门槛全部通过。

#### P02-Q05：怎样记录私有 API 边界，怎样用标准库 dataclass

- **学习者问题**：P02B-R05 的兼容性说明应怎样修改；P02B-R07 建议的
  `dataclass(frozen=True, slots=True)` 应怎样替代 Pydantic `BaseModel`？
- **R05 结论**：兼容性说明最好写在 `get_gpu_resource` 的 docstring，而不是泛化的
  `# kernel requirement`。它应准确说明：
  1. `_init_handles()`、`n_regs` 与 `metadata.shared` 来自 compiled-kernel 内部/版本敏感接口；
  2. `triton.runtime.driver.active.utils` 是动态 driver API，静态类型没有公开该属性，所以只在
     这一行使用 `reportAttributeAccessIssue` ignore；
  3. 当前实现已在 Triton 3.7.1 验证，升级 Triton 后必须复跑 CPU grid、GPU resource helper
     和默认路径测试。

  最小示例：

  ```python
  def get_gpu_resource(compiled_kernel, device: torch.device) -> Resource:
      """Read resources for one compiled Triton specialization.

      Compatibility boundary: `_init_handles`, `n_regs`, `metadata.shared`, and
      `driver.active.utils` are private or dynamic Triton APIs verified with Triton 3.7.1.
      Re-run the resource-helper and default-launch tests after Triton upgrades.
      """
      ...
  ```

  该说明的目标是让维护者知道升级时首先检查哪里，不需要为当前没有发生的版本差异增加
  `try/except` 或多版本分支。窄范围 pyright ignore 仍保留在 `driver.active.utils` 那一行。
- **R07 结论**：这里的 `Resource` 只是可信内部数据的定型记录，不需要 Pydantic 的输入解析、
  coercion、schema 或序列化。标准库版本为：

  ```python
  from dataclasses import dataclass


  @dataclass(frozen=True, slots=True)
  class Resource:
      registers_per_thread: int
      shared_bytes_per_program: int
      num_SM: int
      registers_per_sm: int
      shared_bytes_per_sm: int
      warp_size: int
      max_threads_per_sm: int
  ```

  `frozen=True` 禁止实例创建后重新赋值，避免资源快照在 grid 推导期间被意外改变；`slots=True`
  不创建每实例 `__dict__`，禁止动态添加拼错的字段，并降低这类小记录的开销。它不会像 Pydantic
  那样在运行时转换或校验类型，但这些值来自已验证的 Triton/Torch properties，静态标注和现有
  tests 已足够。

  构造语法和属性访问不变，因此 `Resource(...)`、`resource.registers_per_sm`、`compute_grid`
  以及当前 agent-owned tests 均无需改变。替换 class/import 后，可用 `uv remove pydantic` 删除
  direct dependency 并同步 `uv.lock`。若保留 Pydantic，应记录确实需要运行时 validation/schema
  的理由；否则 dataclass 是本例更小的依赖边界。
- **状态**：解释已完成；等待学习者应用 R05 docstring，并自行选择关闭或保留非阻塞 R07。

#### P02-Q06：benchmark 为什么也需要测试，要测什么

- **学习者问题**：benchmark 也需要测试吗；如果需要，测试的对象是什么？
- **核心区分**：需要轻量测试，但测试的是 benchmark **测量工具的正确性和可运行性**，不是在
  pytest 中断言某个实现一定更快。benchmark 很容易输出看似合理、实际错误的数字，例如单位换算
  错误、少算一次写流量、把 JIT/内存分配混入计时、provider 与 stages 组合错误，或产生
  `NaN`/`inf` 后仍写入结果表。
- **本阶段的三层证据**：

  | 层次 | 当前检查内容 | 不检查什么 |
  | --- | --- | --- |
  | 纯函数与数据契约 | 固定 shapes/stages、记录字段、有效 GB/s 公式、非法 latency、资源上限/grid/occupancy 推导 | 不启动 kernel，不比较速度 |
  | benchmark 配置契约 | 拒绝未知 provider、三个非 persistent providers 错带 stages、persistent 缺 stages 或使用不支持的 stages | 不设性能阈值 |
  | GPU smoke | 四种 providers（persistent 展开 stages 1/2/4）都能完成小规模计时，latency/GB/s 为正且有限，带宽与 latency 公式一致 | 不断言 stages 4 必须快于 stages 2 |

  当前 24 个 cases 来自 7 个语义测试组的参数化展开：1 个固定契约、1 个公式、4 个非法
  latency、2 个资源情况、6 个非法配置、4 个 timing 参数转发和 6 个 GPU smoke。它们只在显式
  GPU pytest 中运行，不进入常规 CPU CI；学习者也不需要编写这些测试，只需按 red/green 反馈
  实现 benchmark。
- **实验结论的取得方式**：哪种 provider 或 stage 更快，必须单独运行完整实验，在相同 shape、
  dtype、grid、`num_warps`、warm-up 与重复计时条件下记录 latency、有效 GB/s 和资源表，再解释
  差异。共享 GPU 的抖动、温度、频率与后台负载都会影响数值，因此当前 pytest 不写
  “stage 4 必须更快”或固定毫秒阈值。
- **计时边界**：预分配输入输出、JIT warm-up、正确性检查和资源读取应放在计时闭包之外；计时
  闭包只发起目标 kernel。该边界中一部分适合自动测试，另一部分在实现评审和实验复现时检查。
- **状态**：已解释 benchmark 验收测试与性能实验的职责边界；P02-C 第一版正在修改。

#### P02-Q07：一条 benchmark 曲线怎样同时表示 provider 和 num_stages

- **学习者问题**：最终图以三种 shape 为横坐标，每条线由 provider 与指定 `num_stages` 共同
  决定；`line_arg` 怎样同时指定两个变量？
- **当前 Triton 3.7.1 API 结论**：`Benchmark` 只有单数 `line_arg: str`，没有 `line_args`。
  `Mark._run` 会遍历 `line_vals`，把每个值作为这一个关键字参数传给 benchmark 函数。因此可把
  `(provider, num_stages)` 作为一个 tuple 配置值传入，再在函数内解包；`line_names` 单独提供
  六条曲线的人类可读标签。
- **横轴边界**：虽然 `x_names=["size_m", "size_n"]` 配合 tuple `x_vals` 可以把两个参数传入
  函数，但当前绘图只使用第一个 `x_name` 作为横轴。本课后两个 shape 的 `M` 都是 4096，会落在
  同一横坐标。可靠做法是把 0/1/2 的 `shape_index` 放在第一个 x 参数，同时传入 M/N；绘图完成
  后再把三个数值刻度替换成 shape 标签。

  ```python
  import matplotlib.pyplot as plt


  X_VALUES = [(index, m, n) for index, (m, n) in enumerate(SHAPES)]
  LINE_CONFIGS = (
      ("torch_naive", None),
      ("torch_fused", None),
      ("triton_naive", None),
      ("triton_persistent", 1),
      ("triton_persistent", 2),
      ("triton_persistent", 4),
  )

  @triton.testing.perf_report(
      triton.testing.Benchmark(
          x_names=["shape_index", "size_m", "size_n"],
          x_vals=X_VALUES,
          line_arg="provider_config",
          line_vals=list(LINE_CONFIGS),
          line_names=[
              "torch_naive",
              "torch_fused",
              "triton_naive",
              "triton_persistent-s1",
              "triton_persistent-s2",
              "triton_persistent-s4",
          ],
          xlabel="shape (M x N)",
          ylabel="effective GB/s",
          plot_name="lesson02_softmax",
          args={},
      )
  )
  def benchmark(
      shape_index: int,
      size_m: int,
      size_n: int,
      provider_config: tuple[str, int | None],
  ) -> float:
      del shape_index  # 只负责确定横轴位置
      provider, num_stages = provider_config
      record = measure_case(
          size_m=size_m,
          size_n=size_n,
          provider=provider,
          num_stages=num_stages,
          warmup_ms=WARMUP_MS,
          rep_ms=REP_MS,
      )
      return record.effective_gbps

  benchmark.run(show_plots=False)
  axis = plt.gcf().axes[0]
  axis.set_xticks(
      range(len(SHAPES)),
      [f"{m}x{n}" for m, n in SHAPES],
  )
  plt.savefig("lesson02_softmax.png")
  ```

  已用不启动 GPU kernel 的最小 `perf_report` 实验验证：tuple line value 会原样传入并可在函数
  内解包，0/1/2 三个点可被正确替换为三个 shape 标签。字符串 `x_vals` 虽能产生不同点，但当前
  内置绘图不会自动显示字符串刻度，因此不采用。`args` 也不适合承载 provider/stages，因为它对
  全部 shape 和全部曲线固定不变。若使用 `benchmark.run(save_path=...)`，Triton 会在返回前保存
  原始图；要保留自定义刻度，应像示例一样先运行、改轴，再自行 `savefig`。
- **状态**：复合曲线配置与 shape 横轴/刻度方案已验证；等待学习者应用到最终 benchmark。

#### P02-Q08：warm-up、资源/grid 推导应在何时执行

- **学习者复述**：当前 persistent 结果慢，主要因为 warm-up 和计算资源/grid 的时间进入重复计时；
  是否应在第一次调用时计算一次，后续复用 grid？
- **结论**：方向正确。更精确地说，应当对每一个 `(shape, provider, num_stages)` benchmark case
  在进入 `do_bench` **之前**完成一次准备，而不是依赖 timed wrapper 的“第一次调用”。当前 Triton
  `do_bench` 会先调用一次 `fn`、再调用 5 次估算耗时，之后执行 `n_warmup` 次预热和 `n_repeat`
  次正式采样；如果 `fn` 是完整 persistent wrapper，output 分配、compiled warm-up、resource
  introspection 和 grid 推导会在这些调用中反复发生。
- **两种 warm-up 必须分开理解**：

  | 操作 | 位置 | 目的 | 是否属于被测时间 |
  | --- | --- | --- | --- |
  | `persistent_kernel.warmup(...)` | `do_bench` 外，每个 specialization 准备一次 | 编译/取得 compiled handle，以读取 registers/shared | 否 |
  | `do_bench(..., warmup=...)` | `do_bench` 内部 | 反复执行最终被测 callable，使运行状态稳定 | warm-up 样本不计入结果，但 callable 必须已经只含目标工作 |

  推荐时间线：

  ```text
  每个 measure_case：
    1. 提前校验 provider/stages
    2. 创建 input、reference、可复用 output
    3. 计算 BLOCK_SIZE
    4. persistent specialization：kernel.warmup -> resource -> grid（一次）
       naive Triton：grid = (M,)，不做 resource introspection
    5. untimed direct kernel launch -> assert_close -> synchronize
    6. do_bench(lambda: direct kernel launch with prepared output/grid)
       ├─ do_bench 自己的 warm-up：只反复 launch kernel
       └─ 正式采样：仍然只 launch kernel
  ```

  output 可以复用，因为每次 softmax kernel 都会覆盖所有有效输出元素；无需每轮重新分配。
- **复用边界**：同一个 case 内复用 prepared grid。不要先做复杂的全局缓存：`M` 会改变最终
  `min(M, capacity)`，`N/BLOCK_SIZE`、`num_stages`、`num_warps`、dtype、device/backend 则可能
  改变 compiled specialization 或资源占用。课程实现按 case 准备一次最清晰；以后若优化缓存，
  可以缓存 specialization 的 resource capacity，但仍应针对每个 `M` 重新 cap 最终 grid。
- **状态**：学习者已复述 R01 的正确修复方向；R01 仍为 open，等待代码修改与重新计时验证。

#### P02-Q09：预计算 grid 后能否继续调用 wrapper

- **学习者问题**：是否可以在 `measure_case` 调用 `do_bench` 前计算一次资源/grid，然后把它传给
  wrapper 的 `num_programs`，后续复用？
- **结论**：`num_programs=grid[0]` 可以跳过 persistent wrapper 内部的 compiled warm-up、资源
  读取和 grid 推导，因此比当前实现更接近目标；但它仍不是本阶段要求的稳态 kernel-only 计时。
  wrapper 每次调用仍会执行输入校验、计算 block size，并在进入 `num_programs is not None` 分支
  之前调用 `torch.empty` 分配新 output。注意 `compute_grid` 返回一元 tuple，而 wrapper 参数要求
  int，因此若仅做 wrapper 方案应传 `grid[0]`，不能传整个 `grid`。
- **两种实验语义**：

  | closure | 实际测量内容 | 适用场景 |
  | --- | --- | --- |
  | `lambda: persistent_fused_softmax(x, num_programs=grid[0], ...)` | wrapper 校验 + output 分配 + kernel launch | 端到端 Python API latency |
  | `lambda: persistent_kernel[grid](x, prepared_output, ...)` | prepared kernel launch | 本阶段的稳态 kernel latency 与 stages 比较 |

  本课要求第二种，否则 Triton ordinary/persistent 与 stages 的差异仍会混入 wrapper/allocator 开销。
  推荐在 `measure_case` 外层准备 output、compiled specialization、resource 和 grid，再定义一个只含
  direct launch 的 callable；先 untimed 调用它完成 correctness 检查，最后把同一个 callable 交给
  `do_bench`。普通 Triton 分支也同样直接 launch，保证两个 Triton providers 的计时边界一致。
- **状态**：已澄清“预计算 grid + wrapper”只能消除资源探测，不能消除 output 分配；R01 的验收
  仍要求 direct kernel closure。
- **后续修订**：上述“本课必须 kernel-only”的判断被学习者以实际端到端场景为理由反对；该理由
  经复核成立，现由 P02-Q10 的稳态 wrapper-level 契约取代。此处保留原判断以记录设计演进。

#### P02-Q10：为什么本实验选择 wrapper-level 端到端比较

- **学习者异议**：另外两个 Torch providers 会在函数内部做检查并分配 output/中间 tensor；若
  Triton 只测预分配 output 的 direct kernel launch，比较过于理想化，脱离实际调用场景。学习者
  偏向比较公开 function/wrapper 的实际端到端表现。
- **复核结论**：异议成立。benchmark 边界由要回答的问题决定，kernel-only 并不天然比
  wrapper-level 更“公平”。如果问题是“应用在初始化后反复调用这些公开 providers 时，一次调用
  要多久”，就应把每次调用固有的检查、output/中间分配、dispatch 和 kernel/op 执行全部纳入。
  先前要求两个 Triton providers direct launch、两个 Torch providers 调函数，反而混用了两种
  API 层级。
- **本课最终选定场景**：warm steady-state end-to-end provider latency。

  ```text
  case setup（不计时）：
    input/reference、首次 JIT、persistent compiled resources/grid、正确性检查

  每次 provider call（计时）：
    torch_naive       -> torch_naive_softmax(x)
    torch_fused       -> torch.nn.functional.softmax(x, dim=1)
    triton_naive      -> fused_softmax(x)
    triton_persistent -> persistent_fused_softmax(
                            x,
                            num_stages=stage,
                            num_programs=grid[0],
                         )
  ```

  四条路径都从已有 input 开始并返回新 output；各自的检查、output/中间分配和 dispatch 都属于
  计时。persistent 的资源/grid 初始化被视为可缓存、可摊销的 setup，必须在结果元数据中明确写
  “excluded”；如果实际应用不会缓存它，那么默认 wrapper 的 resource introspection 也应计入，
  但那是另一个 cold/default-API 实验问题，不能与当前 prepared steady-state 结果混称。
- **finding 生命周期**：P02C-R01 中“wrapper 调用本身是污染、必须 direct kernel”的部分标记为
  `rejected-with-rationale`；新建 P02C-R08（blocking/open），要求 persistent case 在 `do_bench`
  外准备 grid、closure 内继续调用 wrapper 并显式传 `num_programs=grid[0]`。首次 0.95 ms 结果仍
  不回答这一选定问题，因为它在每个样本中重复了被定义为一次性 setup 的 resource introspection。
- **状态**：wrapper-level 实验问题与计时边界已由学习者选定并确认；等待按新契约修改实现。

#### P02-Q11：怎样生成资源表与 GPU/软件环境信息

- **学习者问题**：P02C-R05 要求的三行资源表和 GPU/软件环境信息应怎样实现？
- **资源表采集流程**：固定 `M=4096,N=781`，创建一次 input 和临时 output，计算
  `BLOCK_SIZE=1024`；对 stages 1/2/4 分别调用 exact persistent specialization 的
  `kernel.warmup(..., grid=(1,), num_warps=8)`，再用 `ops.get_gpu_resource` 读取 compiled/device
  resources，并交给 `derive_resource_record` 计算 limits、resident programs、最终 grid 和理论
  occupancy。整个过程属于 setup，不进入 `do_bench`。

  ```python
  def collect_resource_records() -> list[ResourceRecord]:
      size_m, size_n = 4096, 781
      block_size = triton.next_power_of_2(size_n)
      x = torch.randn((size_m, size_n), device="cuda", dtype=torch.float32)
      output = torch.empty_like(x)
      records: list[ResourceRecord] = []

      with torch.cuda.device(x.device):
          for num_stages in STAGES:
              compiled = ops.persistent_fused_softmax_kernel.warmup(
                  x,
                  output,
                  size_m,
                  size_n,
                  BLOCK_SIZE=block_size,
                  num_stages=num_stages,
                  num_warps=NUM_WARPS,
                  grid=(1,),
              )
              resource = ops.get_gpu_resource(compiled, x.device)
              records.append(
                  derive_resource_record(
                      resource,
                      size_m=size_m,
                      size_n=size_n,
                      num_stages=num_stages,
                  )
              )
      return records
  ```

  records 可用现有的 `asdict` + `csv.DictWriter` 写成 `resources.csv`；终端打印时把
  `theoretical_warp_occupancy` 乘 100 显示成百分比即可。不要把实测 registers/shared/grid 写入
  acceptance tests，它们会随 GPU、Triton/compiler 和 specialization 改变。
- **当前环境的真实采集结果**：

  | stages | regs/thread | shared/program | reg limit | shared limit | thread limit | resident/SM | grid | theoretical occupancy |
  | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
  | 1 | 32 | 32 | 8 | 5216 | 8 | 8 | `(864,)` | 100% |
  | 2 | 32 | 4128 | 8 | 40 | 8 | 8 | `(864,)` | 100% |
  | 4 | 32 | 12320 | 8 | 13 | 8 | 8 | `(864,)` | 100% |

  这些是 2026-08-06 在当前 Triton 3.7.1/A100 specialization 上观察到的证据，只用于对照本次
  脚本输出；此前练习中的 40 registers、grid 648 是受控算术示例，不是应硬编码的设备结论。
- **环境 metadata**：推荐写 `environment.json`，同时在终端打印。最低包含 GPU identity、软件
  版本和实验配置，并明确计时边界：

  ```python
  import json
  import platform


  device_index = torch.cuda.current_device()
  properties = torch.cuda.get_device_properties(device_index)
  metadata: dict[str, object] = {
      "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
      "gpu_name": torch.cuda.get_device_name(device_index),
      "gpu_compute_capability": torch.cuda.get_device_capability(device_index),
      "gpu_total_memory_bytes": properties.total_memory,
      "gpu_sm_count": properties.multi_processor_count,
      "torch_version": str(torch.__version__),
      "triton_version": str(triton.__version__),
      "torch_cuda_build": torch.version.cuda,
      "python_version": platform.python_version(),
      "dtype": "float32",
      "num_warps": NUM_WARPS,
      "warmup_ms": WARMUP_MS,
      "rep_ms": REP_MS,
      "quantiles": QUANTILES,
      "stages": STAGES,
      "shapes": SHAPES,
      "timing_scope": "prepared steady-state wrapper-level end-to-end",
      "setup_excluded": [
          "input/reference",
          "first JIT",
          "persistent resources/grid",
          "correctness",
      ],
      "per_call_included": [
          "provider checks",
          "output/intermediate allocation",
          "dispatch",
          "kernel/op",
      ],
  }

  text = json.dumps(metadata, indent=2, sort_keys=True)
  print(text)
  (results_path / "environment.json").write_text(text + "\n", encoding="utf-8")
  ```

  `torch_cuda_build` 表示当前 PyTorch 构建所使用的 CUDA 版本，不应误标为 NVIDIA driver 版本；
  `CUDA_VISIBLE_DEVICES=3` 时进程内 `current_device()` 通常仍为 0，所以同时记录该环境变量才能知道
  可见设备映射。当前实测 metadata 为 A100-SXM4-80GB、compute capability 8.0、108 SM、
  PyTorch 2.13.0+cu130、Triton 3.7.1、CUDA build 13.0、Python 3.12.13。
- **建议产物布局**：同一结果目录保存 `environment.json`、`resources.csv`、18 行
  `detailed.csv`、Triton perf-report CSV 和 PNG。这样资源解释、性能数据和复现条件不会分离。
- **后续修订**：学习者认为额外的 collector、完整 environment JSON 和产物布局过度设计，要求
  直接复用已经存在的 `derive_resource_record`。该反馈成立，当前最小方案由 P02-Q12 取代；本节
  保留用于记录被拒绝的复杂方案和一次真实资源观察。

#### P02-Q12：直接复用 derive_resource_record 的最小方案

- **学习者反馈**：既然已经实现 `derive_resource_record`，不应再增加冗余的资源采集抽象和复杂
  metadata 文件。
- **最小修改**：现有 persistent 分支已经完成 compiled warm-up 和 `get_gpu_resource`。在该位置
  直接构造 record，并把它的 grid 传给 wrapper：

  ```python
  resource_record = derive_resource_record(
      resource,
      size_m=size_m,
      size_n=size_n,
      num_stages=num_stages,
  )
  grid = resource_record.grid

  bench_result = triton.testing.do_bench(
      lambda: ops.persistent_fused_softmax(
          x,
          num_stages=num_stages,
          num_programs=grid[0],
      ),
      warmup=warmup_ms,
      rep=rep_ms,
      quantiles=QUANTILES,
  )
  ```

  若当前 case 是 `(4096, 781)`，把该 `resource_record` 加入一个与现有 `benchmark_records` 对称的
  `resource_records` list；perf report 完成后直接对这三项 `print(asdict(record))`，或复用现有
  `csv.DictWriter` 写三行即可。运行开始时与 `benchmark_records` 一起 clear，避免同进程重复运行
  产生重复行。不新增 `collect_resource_records`，也不重复 limits/grid 公式。
- **当前实现中的必要修正**：compiled warm-up 的 `BLOCK_SIZE` 必须是
  `triton.next_power_of_2(size_n)`，当前误写为 `size_m`；否则读取的是错误 block specialization 的
  registers/shared，推导出的 grid 与真正 wrapper 使用的 kernel 不匹配。
- **最小环境输出**：契约只要求记录，不强制 JSON。可在 `__main__` 中打印一行：

  ```python
  device = torch.cuda.current_device()
  print(
      f"GPU={torch.cuda.get_device_name(device)}, "
      f"PyTorch={torch.__version__}, Triton={triton.__version__}, "
      f"CUDA-build={torch.version.cuda}, num_warps={NUM_WARPS}, "
      f"warmup_ms={WARMUP_MS}, rep_ms={REP_MS}"
  )
  ```

  这已经满足本课复现需要；以后确有机器处理结果的需求时再升级为 JSON。
- **状态**：接受学习者的简化设计；R05 仍 open，等待直接复用 record、输出三行资源与一行环境。

#### P02-Q13：怎样把 perf-report 横轴改成三个 shape 标签

- **学习者问题**：当前以 `shape_index=0/1/2` 区分三个 shape，怎样让最终图显示具体 shape？
- **当前 Triton 3.7.1 行为**：`Mark._run()` 固定使用第一个 `x_name` 作为横轴数据，所以现有
  `X_VALUES` 会画出数值 0/1/2；`xlabel` 只设置轴标题，不设置 tick labels。它在保存 PNG 后没有
  关闭 figure，因此单 benchmark 的最小方案是在 `benchmark_fn.run(...)` 返回后取得当前 figure，
  把位置 0/1/2 的标签设为三个 `(M,N)`，再覆盖保存同一个 PNG。
- **推荐局部修改**：在模块顶部导入 `matplotlib.pyplot as plt`；在 `run_benchmark` 的 `.run()`
  调用之后执行：

  ```python
  figure = plt.gcf()
  axis = figure.axes[0]
  axis.set_xticks(
      range(len(SHAPES)),
      labels=[f"{size_m} x {size_n}" for size_m, size_n in SHAPES],
  )
  figure.tight_layout()
  figure.savefig(results_path / "lesson02_softmax.png")
  plt.close(figure)
  ```

  这里使用 ASCII `x`，因为仓库 Ruff 的 RUF001 会拒绝易混淆字符 `×`。上一版答疑给出的 `×`
  示例与仓库规则不兼容，现已更正，不作为学习者设计错误。tick 位置必须继续对应
  `shape_index` 的 0/1/2；不要只改 `xlabel`，也不要把 `(M,N)` 直接作为
  第一个数值横坐标，否则两个 `M=4096` case 会重叠。该方案依赖当前 Triton run 后保留 figure 的
  行为，适合本课单图脚本；若以后生成多个 benchmark 图，再改为显式接收 dataframe 并自行绘图。
- **状态**：绘图机制与最小修改已说明；P02C-R06 等待学习者应用并重跑 PNG 验证。

#### P02-Q14：benchmark 不进行正确性检查

- **学习者决定**：`measure_case` 只负责准备并测量 provider，不在 benchmark 内计算 reference 或
  调用 `assert_close`。
- **复核结论**：该边界成立。性能 harness 与功能正确性可以分离；关键是不能让性能数据成为唯一
  的正确性证据。benchmark 保留 input 初始化后的同步，避免随机输入生成混入计时；provider 的
  数学正确性转移到显式 GPU 功能测试。
- **AI-owned 测试调整**：删除四类 provider 的 benchmark-local correctness/sync 时序断言；新增
  三个固定实验 shape 的独立测试，验证 ordinary kernel 和 persistent stages 1/2/4 均与 PyTorch
  一致，特别覆盖此前缺失的 `N=2049 -> BLOCK_SIZE=4096` specialization；另单测
  `torch_naive_softmax` baseline。
- **finding 生命周期**：P02C-R10 标记为 `rejected-with-rationale`，理由是学习者明确选择职责分离，
  且等价正确性证据已移入独立功能 suite，而不是删除正确性保障。
- **实测证据**：物理 GPU 3 上 benchmark harness 27 passed；Lesson 02 功能测试 37 passed；新增
  三个 exact-shape cases 全部通过。
- **状态**：benchmark/正确性职责边界已确认并验证；后续不再要求 `measure_case` 调用
  `assert_close`。

#### P02-Q15：为什么最终 benchmark 中 stage 4 不是最快

- **学习者问题**：最终结果应怎样理解；为什么更深的 `num_stages=4` kernel 并没有表现最好？
- **核心模型**：`num_stages` 是编译器对同一 program 的 `tl.range` 循环尝试采用的软件流水深度，
  不是优化等级。增加 stages 的收益来自让更多独立行迭代同时在途，以当前行的计算覆盖后续行的
  load 延迟；代价则包括流水填充/排空、更多同时存活的数据、shared-memory/register buffering，
  以及由此可能减少的 resident programs。只有“额外隐藏的延迟”大于这些成本时，更深流水才会
  更快。
- **代码对应**：[persistent kernel 的第 95 行](../../../gpu/triton/lesson02_fused_softmax.py#L95)
  把 `num_stages` 交给 `tl.range`；第 96–101 行是一整次行迭代。它不是把这六行机械切成四段，
  而是允许编译器在不破坏依赖的前提下重叠不同的行迭代。同一行内部的
  `load -> max -> exp -> sum -> divide -> store` 依赖仍然存在。
- **按 shape 解释**：

  1. `256 x 781` 时最终 grid 为 256，每个 program 只处理一行。循环没有第二次迭代，因而没有
     跨行 load/compute 可以重叠。stage 2/4 比 stage 1 多约 1.024 us，只能说明本轮测量中深流水
     没有收益；差异很小且没有重复试验置信区间，不宜解释成稳定的普遍差距。
  2. `4096 x 781` 时三个 stage 的 grid 都是 864。由
     `4096 = 4 * 864 + 640`，640 个 programs 处理 5 行，224 个处理 4 行。stage 4 要先填充最多
     四个在途迭代，但整个循环只有 4–5 次，几乎没有足够长的稳态区间来摊薄 prologue/epilogue。
     三种配置的理论 occupancy 都是 100%，所以这里不能用 occupancy 下降解释 stage 4 较慢；
     12,320 B shared buffering 虽未降低 resident 数，也不自动产生性能收益。
  3. `4096 x 2049` 时 `BLOCK_SIZE=4096`，每行只有 2049 个有效 lanes，并包含更大的 reduction。
     补充编译资源诊断如下：

     | stages | registers/thread | shared/program | resident/SM | grid | theoretical occupancy | rows/program |
     | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
     | 1 | 63 | 32 B | 4 | `(432,)` | 50.0% | 9–10 |
     | 2 | 48 | 16,416 B | 5 | `(540,)` | 62.5% | 7–8 |
     | 4 | 62 | 49,184 B | 3 | `(324,)` | 37.5% | 12–13 |

     stage 4 的 shared-memory limit 为 3，最终只有 24 resident warps/SM，是其没有取得收益的
     一个合理因素。但 stage 2 的理论 occupancy 高于 stage 1，实测却仍更慢，这同时证明
     occupancy 只是“可驻留多少 warps”的资源指标，不是性能排名函数。没有 profiler 的 stall、
     memory throughput 和 achieved occupancy 证据时，不能把结果归因于单一资源。
- **provider 排名怎样读**：`torch_naive` 会发射多个 eager operations 并物化中间 tensor，所以在
  三个 shape 上都明显最慢；`torch_fused` 已消除大部分中间全局内存流量；`triton_naive` 让每行
  对应一个独立 program，由硬件调度大量独立行，在这三个 shape 上均最快或并列最快。persistent
  版本限制 program 数并在 program 内循环多行，但本例没有可跨行复用的数据；它提供了软件流水
  机会，也同时减少了硬件可直接调度的独立 programs，因此不是必然优化。
- **有效 GB/s 的边界**：脚本统一按 `2 * M * N * element_size / latency` 计算语义上的一读一写
  工作量，便于所有 provider 横向比较。它没有计入 `torch_naive` 的中间 tensor 流量、padding
  lanes、shared-memory traffic 或 reduction/exp 工作，所以不是实际 DRAM bandwidth，也不能只看
  数字接近硬件峰值就判断某个瓶颈。
- **当前 benchmark 能回答什么**：它比较的是每种 stage 按自身编译资源推导 grid 后的
  prepared wrapper-level 默认策略。对 `N=781`，三种 stage 的 grid 相同，stage 对比相对干净；
  对 `N=2049`，stage 同时改变了 pipeline depth、资源占用、resident programs、grid 和每个 program
  的循环次数，因此只能得出“当前默认 stage 1 策略最快”，不能声称差异完全由
  `num_stages` 本身造成。
- **若以后做因果实验**：可以让 stages 1/2/4 使用共同的显式 grid（例如三者最小值 324），隔离
  pipeline depth；再固定 stage 单独 sweep grid 或 `M / P`，观察每个 program 的行迭代数。当前
  Lesson 02 不扩展为 profiler/统计专题。
- **最终结论**：stage 4 不最快是有效且符合模型的结果。`num_stages` 应当按 kernel、shape 和资源
  实测调优，通常交给 autotune，而不是选择允许值中最大的一个。

#### P03-Q16：Log-softmax 与 softmax 的差异和额外注意点

- **学习者范围选择**：不实现 P03，只快速过一遍数学式、kernel 数据流和工程边界。
- **稳定公式**：对一行 `x` 取 `m=max(x)`、`z=x-m`、`s=sum(exp(z))`。Softmax 输出
  `exp(z_i)/s`；log-softmax 输出 `z_i-log(s)`，即 `x_i-logsumexp(x)`。两者共享
  max reduction、减 max、exp 和 sum reduction；最后一步从“向量除以行和”变成“行和取
  log 后做向量减法”。
- **不能写成 `log(softmax(x))`**：极小概率可能先在 softmax 中下溢为 0，再取 log 得到
  `-inf`。CPU 最小实验中 `x=[0,-1000]` 的 `log(softmax(x))=[0,-inf]`，而稳定
  `log_softmax(x)=[0,-1000]`。
- **与现有代码的对应**：ordinary kernel 的 masked load/max 保持第 79–80 行不变；第
  81–84 行应改为保留 `row_minus_max`，用它的 exp 值求和，再输出
  `row_minus_max - tl.log(sum_exp)`。Persistent kernel 的第 96–101 行做同样的局部替换；行分配、
  grid-stride 循环、`BLOCK_SIZE`、mask 和 `num_stages` 模型都不变。
- **Padding 与空维度**：`other=-inf` 仍是正确 padding；它不影响 max，且在 exp 后贡献
  0。对至少有一个有限值的非空行，最大元素会贡献 `exp(0)=1`，因而 `s>=1`。`M=0`
  仍可直接返回；`N=0` 没有有效 max 或该锚点，应继续由 wrapper 拒绝。
- **正确性不变量**：log-softmax 的每行和不应接近 1。应对照
  `torch.log_softmax(x, dim=1)`，并检查 `logsumexp(output, dim=1)` 接近 0，或
  `exp(output).sum(dim=1)` 接近 1。`N=1` 时唯一输出应为 0。
- **性能和资源**：逻辑全局内存流量仍是每元素一读一写，但指令组合和值的 live range
  发生变化；需要保留 `row_minus_max` 到行和完成，并新增一次每行 log。编译后 registers、
  shared memory 和最佳 stages 不保证与 softmax 相同；若使用资源推导 grid，必须针对
  log-softmax 的实际 specialization 重新读取，不能复用 softmax 的资源记录。
- **训练边界**：log-softmax 常与 NLL loss 连用；对目标类 `k`，交叉熵是
  `-log_softmax(x)[k]`。现有 Triton wrapper 只是 forward 教学算子；若用于真实训练，还要提供
  autograd/backward 集成，不能因 forward 数值正确就直接替换 PyTorch 算子。
- **学习者复述**：主要差异是计算公式；Triton 代码框架和优化方法与普通 softmax
  没有太大差别。
- **评估**：正确。两者共享 row-wise mapping、padding/mask、max/sum reduction、尾端融合、
  persistent 调度与软件流水模型；但数值不变量、最后计算步骤和编译后资源仍要分别对待。
- **状态**：Q16 已确认；P03 保持取消编码实践，Lesson 02 状态仍为已完成。

### 运行命令与结果

官方脚本验证：

```bash
CUDA_VISIBLE_DEVICES=0 MPLBACKEND=Agg \
  uv run --frozen python docs/triton-tutorials/official/02-fused-softmax.py
```

```text
官方 1823×781 正确性断言通过；
98 个 N × 3 个 provider 的 benchmark 完成；
进程退出码 0。
```

P01 第一版评审验证：

```bash
CUDA_VISIBLE_DEVICES=0 \
  uv run --frozen python -m pytest -q gpu/triton/lesson02_fused_softmax_test.py

uv run --frozen ruff check \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py

uv run --frozen ruff format --check \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py

uv run --frozen basedpyright \
  gpu/triton/lesson02_fused_softmax.py \
  gpu/triton/lesson02_fused_softmax_test.py
```

```text
pytest：8 passed in 2.92s
Ruff：通过
format check：2 files already formatted
BasedPyright：0 errors, 0 warnings, 0 notes
GPU：NVIDIA A100-SXM4-80GB，CUDA_VISIBLE_DEVICES=0
```

P01 第二版复审：

```text
第一次在物理 GPU 0 运行：12 failed, 1 passed；失败均为 tensor 分配时 CUDA OOM。
当时 GPU 0 显存占用：81029 / 81920 MiB；判定为外部设备占用，不是实现失败。

切换到空闲物理 GPU 5：13 passed in 3.18s。
compiled metadata：num_warps = 8。
Ruff：失败，1 个 F841（pytest.raises 内未使用的 actual）。
format check：通过。
BasedPyright：7 errors（6 个未使用 actual；1 个 Triton 动态 launcher 关键字类型误报）。
```

P01 最终复审：

```text
物理 GPU 3：13 passed in 3.38s。
Ruff：通过。
format check：2 files already formatted。
BasedPyright：0 errors, 0 warnings, 0 notes。
compiled metadata：num_warps = 8。
```

### 正确性用例

第一版测试覆盖空行数、最小输入、两种非 2 的幂列宽、2 的幂列宽、官方不规则 shape、常数行和
极大有限值，8 个用例均与 Torch reference 一致。额外只读诊断得到：

| 证据 | 结果 |
| --- | --- |
| 最大 reference 绝对误差 | `1.49e-8` |
| 最大 row-sum 绝对误差 | `2.38e-7` |
| 六类非法输入 | wrapper 均抛出 `ValueError`，但尚未写入 pytest |
| 默认 launch warps | compiled metadata 显示 4，不符合契约要求的 8 |

第二版已把输出 row-sum 和六类错误输入写入 pytest；在空闲 A100 上共 13 个用例全部通过。

### 性能实验

目前只有官方脚本的一次探索性运行；完整结果未保存为课程 benchmark 产物，不构成后续实现的
性能验收。

### 失败尝试与定位过程

第二轮最初在 GPU 0 出现 12 个 CUDA OOM。`nvidia-smi` 显示该卡已占用 81029 MiB，切换到空闲
GPU 5 后全部 13 个用例通过，故该失败归因于外部资源状态。

读取 compiled metadata 时曾同时访问 `compiled.n_regs`，当前对象未公开该属性而触发
`AttributeError`；去掉与本 finding 无关的私有属性访问后，成功验证 `metadata.num_warps == 8`。

## 9. 代码评审与修改闭环

### P01 第一轮评审（2026-08-03）

结论：核心计算在现有正确输入上工作，暂无 `blocking` finding；P01 仍有 4 项 `major` 和 2 项
`minor` finding，尚不能进入 P02。

| ID | 严重度 | 状态 | 位置与证据 | 修改方向 |
| --- | --- | --- | --- | --- |
| P01-R01 | major | open | `lesson02_fused_softmax.py:39` 未传 `num_warps`；compiled metadata 为 4 | 按契约在 launch 中显式固定 8 warps |
| P01-R02 | major | open | 测试文件到第 96 行结束，没有六类非法输入测试；只读诊断只能证明当前行为，不能防回归 | 为六类输入添加 pytest，并检查稳定、可读的异常类型/消息 |
| P01-R03 | major | open | 新澄清的契约项：原文“每一行的和”主语不明确；当前测试没有断言输出 `actual.sum(dim=1)` 接近 1 | 为所有非空正确用例增加输出 row-sum 不变量；不把原歧义归责于学习者 |
| P01-R04 | major | open | 第三项设计说明明确表示“不太清楚”，且把主要原因归于是否浪费 launch | 重新解释空批次与空 reduction domain 的语义区别 |
| P01-R05 | minor | open | `lesson02_fused_softmax.py:30` 对 `N=0` 报告 “shape cannot be negative” | 让消息准确描述列数必须大于 0 |
| P01-R06 | minor | open | `lesson02_fused_softmax_test.py:8` 的 skip reason 仍写 “lesson 01” | 改为 Lesson 02/Fused Softmax |

#### P01-R01 提示记录（2026-08-03）

学习者询问 launch 时如何指定 `num_warps`。已提供最小语法提示：它是 JIT launch option，放在
`kernel[grid](...)` 调用的关键字参数中，例如
`kernel[grid](..., BLOCK_SIZE=block_size, num_warps=8)`；不加入 kernel 函数签名。未修改学习者
代码，P01-R01 保持 open，等待修改后通过 compiled metadata 复验。

#### P01-R03/R04 提示记录（2026-08-03）

学习者询问为何 reference 对比之外还需断言 row sum，以及“第三项设计说明”所指内容。已说明：

- row sum 接近 1 是 softmax 定义直接给出的独立数学不变量，能证明归一化结果本身成立，并在失败
  时把问题定位到 denominator/normalization；它与逐元素对照 Torch 是两类互补证据。只对
  `M > 0` 的用例检查。
- 第三项设计说明就是 P01 提交问题 3：“为什么 `M=0` 可以直接返回，而 `N=0` 应由本练习接口
  拒绝？”`M=0, N>0` 是没有任何 row 的合法空 batch，不需要 reduction；`M>0, N=0` 则让每个
  已存在 row 的 reduction domain 为空，无法满足本练习的 row max/归一化及 row-sum 不变量。
  提前返回或拒绝首先是接口语义，是否 launch/浪费资源只是实现后果。

已给出测试断言的结构提示，但未修改学习者测试。P01-R03/R04 保持 open，等待学习者补测并用
自己的话重新复述。

学习者随后指出原契约可能被理解为“输入每行之和”。该反馈成立：softmax 不要求输入行和为 1，
需要检查的是 kernel 输出行和。P01-R03 已标记为新澄清的契约项，任务正文现明确写为
`actual.sum(dim=1)`；这一歧义不计作学习者遗漏明确要求。

评审未修改学习者的 kernel 或测试。下一轮由学习者完成修改后，再逐项运行相关证据并把 finding
推进为 `learner-revised -> verified -> closed`。

### P01 第二轮评审（2026-08-03）

上一轮 findings 的处理结果：

| ID | 生命周期结果 | 复验证据 |
| --- | --- | --- |
| P01-R01 | learner-revised -> verified -> closed | launch 显式指定 8；compiled metadata 为 8 warps |
| P01-R02 | learner-revised -> verified -> closed | CPU、ndim、float64、非连续、`N=0`、`N=16385` 均进入 pytest，GPU 5 全部通过 |
| P01-R03 | learner-revised -> verified -> closed | 所有正确输入路径均断言输出 `actual.sum(dim=1)` 接近 1 |
| P01-R04 | learner-revised -> verified -> closed | 学习者正确区分合法空 batch 与空 reduction domain |
| P01-R05 | learner-revised -> needs-more-work | 消息改为 “shape must be positive”，但接口允许 `M=0`，仍未明确是 `N`/列数必须大于 0 |
| P01-R06 | learner-revised -> verified -> closed | skip reason 已改为 Lesson 02 |

第二轮新增 findings：

| ID | 严重度 | 状态 | 位置与证据 | 修改方向 |
| --- | --- | --- | --- | --- |
| P01-R07 | minor | open | 测试第 135、141、145、150、154、157 行在 `pytest.raises` 内赋值给未使用的 `actual`；Ruff F841、BasedPyright 均失败 | 直接调用待验证函数，不保存不会使用的返回值 |
| P01-R08 | minor | open | 新澄清的工具兼容项：实现第 39 行是有效 Triton launch，运行与 metadata 均通过，但 BasedPyright 的静态接口不知道 `num_warps`，报 `reportCallIssue` | 在该调用处添加范围最小、带具体规则名的 Pyright ignore，并保留运行时复验证据；不归责为运行时实现错误 |

#### P01-R08 提示记录（2026-08-03）

学习者询问如何添加最小范围的 `reportCallIssue` ignore。已说明把 launch 格式化为多行，并只在
触发误报的 `num_warps=8` 参数行添加
`# pyright: ignore[reportCallIssue]`。不使用裸 `# type: ignore`，不关闭整个文件的规则，也不修改
全局 BasedPyright 配置。未修改学习者代码，P01-R08 保持 open，等待静态检查复验。

第二轮仍未修改学习者代码。P01 的数值、边界和概念证据已经通过；清理 P01-R05、R07、R08 并
重新通过静态检查后即可进行 P01 最终复审。

### P01 最终复审（2026-08-04）

| ID | 生命周期结果 | 复验证据 |
| --- | --- | --- |
| P01-R05 | learner-revised -> verified -> closed | `N=0` 消息明确为 `shape[1] must be positive`，与允许 `M=0` 的契约一致 |
| P01-R07 | learner-revised -> verified -> closed | 六处未使用赋值已移除；Ruff 与 BasedPyright 通过 |
| P01-R08 | learner-revised -> verified -> closed | ignore 仅位于 `num_warps=8` 参数行且限定 `reportCallIssue`；运行与 metadata 再次验证 8 warps |

P01-R01–R08 已全部关闭，没有新增 finding。学习者独立完成核心 kernel、wrapper、正确输入、输出
数学不变量和错误输入测试；三项设计说明也已确认。P01 完成，P02 解锁。

### P02-A 第一轮评审（2026-08-05）

结论：persistent 的核心行分配与数值计算正确，显式 program 数、program cap、空 batch 和非法
参数均有测试；物理 GPU 0 上 P01/P02-A 共 25 个用例通过。当前没有 blocking finding，但有
1 项 major 与 4 项 minor finding，P02-A 尚不能进入默认资源 grid。

| ID | 严重度 | 状态 | 位置与证据 | 修改方向 |
| --- | --- | --- | --- | --- |
| P02A-R01 | major | open；新澄清项 | `lesson02_fused_softmax.py:108-115` 把 `num_stages` 作为位置 constexpr 传入；1/2/4 的 `tl.range` 资源不同，但三次 `compiled.metadata.num_stages` 都是后端默认 3 | 按官方调用方式让同一个 stage 值同时成为 kernel constexpr 和 Triton 编译选项；复验 metadata 为 1/2/4、warps 为 8，且 25 个测试仍通过 |
| P02A-R02 | minor | open | 实现第 1 行误导入未使用的 `tarfile.BLOCKSIZE`；Ruff F401 与 BasedPyright `reportUnusedImport` | 删除与本课无关的导入 |
| P02A-R03 | minor | open | Ruff E501/C408，format check 报两个文件均需格式化；实现第 94 行用 `tuple()` 创建随后必被覆盖的空 grid | 整理 `None`/显式 program 分支，避免空占位 grid，并运行项目 formatter |
| P02A-R04 | minor | open；工具兼容项 | 实现第 28 行的 `tl.range` 可运行且 25 个 GPU 用例通过，但 BasedPyright 报 `reportGeneralTypeIssues`：“range is not iterable” | 只在触发误报的循环行添加带具体规则名的窄范围 ignore；不关闭全文件或全局规则 |
| P02A-R05 | minor | open | 实现第 97 行生成如 `num_programs0 arg is invalid.` 的消息；测试只匹配字段名，未约束可读语义 | 把异常消息明确为 program 数必须为正，并让测试匹配稳定的语义关键词 |

`P02A-R01` 是本轮新澄清的 Triton 双重参数语义：当 `num_stages` 仅作为位置参数绑定 kernel 的
`tl.constexpr` 时，`tl.range` stage 已改变，但 NVIDIA backend 的同名 compile option 仍取默认
3。只读诊断结果：

```text
requested tl.range stages: 1 / 2 / 4
compiled metadata stages:  3 / 3 / 3
compiled metadata warps:   8 / 8 / 8
registers/thread:           16 / 20 / 28
shared bytes/program:       0 / 32 / 96
```

改用同名关键字做只读 warmup 后，metadata stages 正确变为 1/2/4，资源结果保持上述差异。原契约
只明确了把 stage 作为 `tl.range` 的编译期参数，没有揭示它还会被 backend options 读取，因此
该 finding 不归责为遗漏已声明要求；但必须在 P02-B 资源与性能对比前修正，才能让请求配置、
编译元数据和实验标签一致。

验证结果：

```text
物理 GPU 0：25 passed in 2.70s
Ruff：3 errors（F401、E501、C408）
format check：2 files would be reformatted
BasedPyright：2 errors（unused import、tl.range 类型桩误报）
git diff --check：通过
```

评审没有修改学习者 kernel 或测试。`num_programs=None` 仍抛出 `NotImplementedError` 是本次
P02-A 的明确分阶段边界，不登记 finding；资源自动 grid 和 benchmark 继续留给 P02-B。

### P02-A 第二轮复审（2026-08-05）

| ID | 生命周期结果 | 复验证据 |
| --- | --- | --- |
| P02A-R01 | learner-revised -> verified -> closed | launch 用同名关键字绑定 stage；metadata 为 1/2/4，三者均为 8 warps，25 个 GPU 用例通过 |
| P02A-R02 | learner-revised -> verified -> closed | 无关 `tarfile.BLOCKSIZE` 导入已移除；Ruff/BasedPyright 通过 |
| P02A-R03 | learner-revised -> verified -> closed | 空 grid 占位已移除；Ruff、format check 通过 |
| P02A-R04 | learner-revised -> verified -> closed | ignore 只位于 `tl.range` 循环行且限定 `reportGeneralTypeIssues`；运行与静态检查通过 |
| P02A-R05 | learner-revised -> needs-more-work | 消息已明确为 `It must be positive.`，但测试仍只匹配 `num_programs`，旧的不可读消息也会通过 |

第二轮没有新增 finding。R05 的最后一步是让零值和负值测试匹配稳定的正数约束语义，例如消息中
的 `positive`；修改后只需重跑 GPU pytest、Ruff、format 和 BasedPyright，无需再次解释 stage。

```text
物理 GPU 3：25 passed in 2.54s
Ruff：通过
format check：2 files already formatted
BasedPyright：0 errors, 0 warnings, 0 notes
metadata stages：1 / 2 / 4
metadata warps：8 / 8 / 8
```

### P02-A 最终复审（2026-08-05）

| ID | 生命周期结果 | 复验证据 |
| --- | --- | --- |
| P02A-R05 | learner-revised -> verified -> closed | 零值与负值均匹配 `must be positive`，旧的不可读消息不再满足测试；GPU 与静态检查通过 |

P02A-R01–R05 已全部 verified/closed，没有新增 finding。P02-A 的 persistent grid-stride 调度、
stages 1/2/4 特化、显式 program cap、接口边界和回归测试均完成，P02-B 默认资源 grid 解锁。

```text
物理 GPU 3：25 passed in 2.63s
Ruff：通过
format check：2 files already formatted
BasedPyright：0 errors, 0 warnings, 0 notes
metadata (requested, compiled, warps)：(1, 1, 8)、(2, 2, 8)、(4, 4, 8)
```

### P02-B 第一轮评审（2026-08-05）

结论：register/shared/thread 三类上限取最小值、再乘 SM 数并 cap 到 `M` 的总体公式方向正确，
但当前默认路径不可执行，且尚未满足 P02-B 的边界与证据要求。

| ID | 严重度 | 状态 | 位置与证据 | 修改方向 |
| --- | --- | --- | --- | --- |
| P02B-R01 | blocking | open | 实现第 120–129 行从 Triton properties 读取不存在的 `max_threads_per_sm`，默认 stages 1/2/4 均先抛 `KeyError`；第 127 行随后还引用未定义的 `num_warps` | 从 Torch device properties 读取 max threads/SM；把固定 warps 定义为一个一致复用的配置值，用于 warmup、三个公式和 launch |
| P02B-R02 | blocking | open | 第 128 行无条件执行 `shared_bytes_per_sm // shared_bytes_per_program`；当前 `(M,N)=(10,7)`、stage 1 编译为 shared=0，修复 R01 后会除零 | 把 shared=0 明确定义为“不构成限制”，不能执行除法；用结构化分支参与最终 min |
| P02B-R03 | major | open | 第 91–93 行在 stage/program 校验前对 `M=0` 返回；只读诊断显示空 batch 接受 `num_stages=3` 和 `num_programs=0` | 先验证所有公开选项，再对合法空 batch 提前返回；补充组合边界测试 |
| P02B-R04 | major | open | 第 131–132 行未检查 `resident_programs_per_sm < 1`；资源不足时将形成 grid 0，而不是契约要求的清晰异常 | 在构造 grid 前拒绝无法驻留一个 program 的资源组合，并验证稳定错误语义 |
| P02B-R05 | major | open | 新增默认分支没有测试；现有 25 个用例全部显式传 `num_programs`，所以即使默认路径总是 `KeyError` 仍全绿；compiled/private resource 读取与算术也都内联在 wrapper | 隔离版本敏感资源读取和可测试的纯 grid 计算；覆盖真实默认调用、shared=0、空 batch 非法选项、资源不足及可观察的 grid/resource info |
| P02B-R06 | minor | open | Ruff 报未使用 `math` 和未定义 `num_warps`；format check 需重排实现；BasedPyright 另报动态 driver `utils` 属性 | 在确定 shared=0 表示法后清理导入、格式化，并只对已由运行证据验证的 Triton 动态属性使用窄范围 ignore |

#### P02B-R01 提示记录

学习者询问如何读取 `max_threads_per_sm`。当前环境不从 Triton properties 字典读取该字段；使用
PyTorch 对目标 tensor 设备的属性，并注意 API 字段名不同：

```python
torch_properties = torch.cuda.get_device_properties(x.device)
max_threads_per_sm = torch_properties.max_threads_per_multi_processor
```

在当前可见 A100 上只读验证结果为 2048。显式传入 `x.device` 可以避免多 GPU 环境下误读当前
默认设备。该提示只解决 P02B-R01 的属性来源，不代替 shared=0、统一 warps 或边界测试修改。

只读复现：

```text
默认调用 stages 1：KeyError 'max_threads_per_sm'
默认调用 stages 2：KeyError 'max_threads_per_sm'
默认调用 stages 4：KeyError 'max_threads_per_sm'
M=0, num_stages=3：错误地接受
M=0, num_programs=0：错误地接受
显式 num_programs 的既有测试：25 passed in 3.25s
```

当前 A100 的 Triton properties 只提供 `max_shared_mem`、`max_num_regs`、`multiprocessor_count`、
`warpSize` 等字段；`max_threads_per_multi_processor=2048` 来自 Torch device properties。

绕开 wrapper、对学习者 kernel 独立读取 `M=4096,N=781` 的资源后得到：

| stages | registers/thread | shared/program | register limit | shared limit | thread limit | resident/SM | grid | theoretical occupancy |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 32 | 32 B | 8 | 5216 | 8 | 8 | 864 | 100% |
| 2 | 32 | 4,128 B | 8 | 40 | 8 | 8 | 864 | 100% |
| 4 | 32 | 12,320 B | 8 | 13 | 8 | 8 | 864 | 100% |

这组结果与此前官方 kernel 的探索表不同是合理的：学习者 kernel 假设 contiguous 并省略 row
stride 参数，生成代码与资源用量不同。资源公式可以复用，具体数值必须来自当前特化，不能复制
官方或先前实验结果。

```text
Ruff：2 errors（unused math、undefined num_warps）
format check：1 file would be reformatted
BasedPyright：3 errors（unused math、dynamic driver utils、undefined num_warps）
git diff --check：通过
```

评审没有修改学习者实现或测试；P02 benchmark 仍未解锁。

### P02-B 第二轮复审（2026-08-05）

结论：默认资源路径已能执行，`max_threads_per_sm` 的来源和 `shared=0` 分支均已得到 GPU
运行验证；原来的两个运行时阻塞问题中，P02B-R02 可以关闭。当前还不能完成 P02-B，因为公开
参数校验和零 resident 边界仍不满足契约，默认资源计算也没有进入回归测试。

| ID | 严重度 | 状态 | 本轮验证 | 剩余修改 |
| --- | --- | --- | --- | --- |
| P02B-R01 | blocking | needs-more-work | Torch device properties 已正确提供 max threads/SM；默认调用不再 `KeyError`，也不存在未定义变量 | `8` 仍分别硬编码在 warmup、两个资源公式和 launch；定义一个固定 warps 配置并在这些位置复用，避免编译资源、grid 推导和最终 launch 漂移 |
| P02B-R02 | blocking | verified / closed | `(M,N)=(10,7)` 的 stages 1/2/4 默认调用均正确；stage 1 的 `shared=0` 不再除零 | 无 |
| P02B-R03 | major | needs-more-work | `num_stages` 已移到空 batch 返回前，`M=0,num_stages=3` 正确拒绝；但 `M=0,num_programs=0/-1` 仍被接受 | 把显式 `num_programs` 合法性校验也移到合法空 batch 返回前，并补组合边界测试 |
| P02B-R04 | major | needs-more-work | 当前第 136 行用 `max(..., 1)` 把零 resident 强制变为 grid 1，未提供契约要求的资源不足异常 | 在构造 grid 前明确检查并拒绝 `resident_programs_per_sm < 1`；通过可控资源输入验证错误语义 |
| P02B-R05 | major | open | 现有 25 个测试仍全部显式传 `num_programs`；本轮默认正确性来自评审诊断，不是仓库回归测试；资源读取和算术仍全部内联 | 按契约集中版本敏感 compiled-resource 访问，隔离可测试的 grid 计算；覆盖真实默认调用、shared=0、空 batch 非法选项、零 resident 和可观察 resource/grid info |
| P02B-R06 | minor | needs-more-work | 未定义变量已消失；Ruff、format 和 BasedPyright 仍未通过 | 删除未使用 `math`，格式化实现；对已由运行验证的 Triton `driver.active.utils` 动态属性添加范围最小的 `reportAttributeAccessIssue` ignore |

GPU 只读复现使用物理 GPU 3：

```text
默认调用 (10, 7)，stages 1/2/4：全部 allclose，最大误差 5.96e-08
默认调用 (4096, 781)，stages 1/2/4：全部 allclose，最大误差不超过 1.49e-08
M=0, num_stages=3：ValueError
M=0, num_programs=0：错误地接受
M=0, num_programs=-1：错误地接受
既有 GPU tests：25 passed in 4.01s
Ruff：2 errors（unused math、119 字符长行）
format check：1 file would be reformatted
BasedPyright：2 errors（unused math、dynamic driver utils）
```

评审仍未修改学习者实现或测试。P02-C benchmark 保持锁定，直到 P02B-R01–R06 全部
verified/closed，并且默认 grid/resource info 有可复现的测试与记录。

### P02-B 第三轮复审（2026-08-05）

结论：功能实现已经跨过本轮核心门槛。统一 `NUM_WARPS`、空 batch 前的选项校验、资源 helper、
纯 grid 计算和零 resident 异常均已实现；新增的真实默认调用使 GPU 用例从 25 个增至 30 个，
全部通过。当前剩余项是把已由临时诊断验证的资源边界固化为仓库测试，并完成静态清理。

| ID | 严重度 | 状态 | 本轮验证 | 剩余修改 |
| --- | --- | --- | --- | --- |
| P02B-R01 | blocking | verified / closed | `NUM_WARPS=8` 已统一用于 warmup、register/thread 公式与最终 launch；30 个 GPU 用例通过 | 无 |
| P02B-R02 | blocking | verified / closed | 默认 `(10,7)` 的 stage 1 继续通过；模拟 `shared_bytes_per_program=0` 得到正常 grid `(648,)` | 无 |
| P02B-R03 | major | needs-more-work | 实现已在 `M=0` 返回前校验选项；诊断确认 stage 3、program 0 和 -1 均抛 `ValueError` | 将空 batch 与三个非法选项的组合写入 pytest，防止校验顺序回归 |
| P02B-R04 | major | needs-more-work | 模拟 register capacity 为零时，`compute_grid` 明确抛出 `RuntimeError`，不再强制 grid 1 | 为纯 grid helper 增加零 resident 测试，并断言稳定错误语义 |
| P02B-R05 | major | needs-more-work | 资源读取与 grid 算术已经拆分；新增 5 个默认调用用例，三种 stages 均与 PyTorch 一致 | 测试纯 grid helper 的正常 `(648,)`、shared=0 和零 resident；让 computed limits/resident/grid 可观察以支持资源表；在资源 helper 注释其 Triton 私有 API 兼容性边界 |
| P02B-R06 | minor | needs-more-work | 未使用导入已清理；静态检查仍失败 | 运行 formatter；拆分两条超长算式；对第 13 行已由 GPU 验证的动态 `utils` 属性添加范围最小的 `reportAttributeAccessIssue` ignore |

本轮可复现证据使用物理 GPU 3：

```text
GPU pytest：30 passed in 3.30s
M=0, num_stages=3：ValueError
M=0, num_programs=0/-1：ValueError
compute_grid normal：grid (648,)
compute_grid shared=0：grid (648,)
compute_grid resident=0：RuntimeError "resource is not enough to launch program."
Ruff：2 个 E501（123/147 字符）
format check：2 files would be reformatted
BasedPyright：1 个 reportAttributeAccessIssue（driver.active.utils）
```

临时诊断证明 R03/R04 的实现行为已正确，但 finding 要求的回归证据尚未提交，因此状态保留为
`needs-more-work`，而不是仅凭代码变更关闭。评审没有修改学习者实现或测试。

### P02-B AI-owned 验收测试补充（2026-08-05）

根据课程流程更新，本轮测试由 AI agent 编写，学习者生产实现保持不变。测试分成两个范围：

- `tests/python/test_lesson02_fused_softmax_grid.py` 使用受控资源数据验证 register/shared/thread
  三类限制、`M` cap、`shared=0` 非限制语义和零 resident 异常；不需要 GPU，进入常规 CI。
- `gpu/triton/lesson02_fused_softmax_test.py` 新增空 batch 与非法 stage/program 的组合覆盖，并
  直接读取当前特化的 compiled/device resources，验证资源字段和最终 grid 不变量。

| ID | 严重度 | 状态 | 验证结果 | 剩余修改 |
| --- | --- | --- | --- | --- |
| P02B-R03 | major | verified / closed | 三个空 batch 组合用例分别验证 stage 3、program 0/-1 均在提前返回前抛 `ValueError` | 无 |
| P02B-R04 | major | verified / closed | register、shared-memory 或 thread 任一限制为零时，三个参数化用例均验证稳定 `RuntimeError` | 无 |
| P02B-R05 | major | needs-more-work | 默认路径、纯 grid 算术、shared=0、零 resident 和实际 resource info 均已有回归覆盖；CPU/GPU tests 全绿 | 在 `get_gpu_resource` 附近写明 `_init_handles`、compiled metadata 和 Triton driver utils 属于版本敏感 API；生产 helper 增加足够类型标注以让测试调用可静态检查 |
| P02B-R06 | minor | needs-more-work | 两个测试文件 Ruff/format 全绿；完整目标仍有源文件静态失败 | 格式化生产文件并拆分长行；标注 `compute_grid` 输入/返回类型；给动态 `driver.active.utils` 使用范围最小的 `reportAttributeAccessIssue` ignore |

可复现结果：

```text
CUDA_VISIBLE_DEVICES='' CPU-only 新文件：6 passed in 1.36s
默认 pytest/CI 范围：20 passed in 1.78s
物理 GPU 3：34 passed in 3.25s
测试文件 Ruff/format：通过
完整 Ruff：2 个 E501，均在生产 compute_grid 算式
完整 format check：仅生产文件需要格式化
完整 BasedPyright：2 errors（dynamic driver utils；compute_grid 缺少类型导致测试 import 为 Unknown）
```

本轮只新增和整理 agent-owned 测试及课程记录，没有修改学习者生产实现。后续不再要求学习者
编写 R03–R05 的测试；学习者只需完成上表中的 helper 文档、类型和格式清理。

### P02-B 第四轮复审（2026-08-06）

结论：学习者使用 typed `Resource` 补齐 `compute_grid` 的输入/返回类型，格式化生产文件，并对
Triton 动态 `driver.active.utils` 添加了准确的窄范围 ignore。由于资源输入从字典变为属性对象，
先前 agent-owned 测试的访问协议已经过时；本轮由 AI agent 修正测试，使其只要求关键字构造和
属性读取，不锁定 Pydantic 或标准库 dataclass 的具体选择。修正后所有验证通过。

| ID | 严重度 | 状态 | 本轮验证 | 剩余修改 |
| --- | --- | --- | --- | --- |
| P02B-R05 | major | needs-more-work | CPU pure-grid、GPU 默认路径、实际 resource info 和 grid 不变量全部通过；资源读取与纯计算已隔离 | 第 20–26 行仍只有泛化的 `kernel requirement` 注释；明确记录 `_init_handles`、compiled metadata、`driver.active.utils` 是当前 Triton 版本的私有/动态兼容边界，升级 Triton 后需复验 |
| P02B-R06 | minor | verified / closed | `Resource`/`compute_grid` 类型消除了 Unknown；动态属性 ignore 范围准确；完整 Ruff、format、BasedPyright 全绿 | 无 |
| P02B-R07 | suggestion | open | 为仅包含 7 个整数的内部资源记录新增 Pydantic，并使 lockfile 增加 `pydantic-core`、`annotated-types`、`typing-inspection` 等依赖 | 可考虑标准库 `@dataclass(frozen=True, slots=True)` 或 `NamedTuple`；此项不阻塞 P02-B，也可保留 Pydantic 并记录理由 |

测试协议修正前，CPU 6 个用例因向新 `Resource` 参数传字典失败，GPU resource-info 用例也因
继续按 mapping 访问失败。这属于 agent-owned 测试未跟随已声明类型契约，不登记为学习者
finding。测试改用 `Resource(**values)` 和属性访问后：

```text
CUDA_VISIBLE_DEVICES='' CPU-only：6 passed in 1.43s
默认 pytest/CI 范围：20 passed in 1.63s
物理 GPU 3：34 passed in 2.83s
Ruff：All checks passed
format check：3 files already formatted
BasedPyright：0 errors, 0 warnings, 0 notes
```

本轮 AI agent 只修改了验收测试与课程记录，没有修改学习者生产实现或依赖选择。P02-C
benchmark 仍等待 P02B-R05 的兼容性说明关闭；P02B-R07 为非阻塞建议。

### P02-B 第五轮复审（2026-08-06）

结论：P02B-R05 的 docstring 已准确列出 `_init_handles`、`n_regs`、`metadata.shared`、动态
driver API、验证版本和升级后的复验动作，可以关闭。P02B-R07 也采用了标准库
`@dataclass(frozen=True, slots=True)`，Pydantic direct dependency 与 lockfile 增量已经清除。
功能、类型与依赖验证全部通过，但新编辑后的生产文件尚未运行 formatter。

| ID | 严重度 | 状态 | 本轮验证 | 剩余修改 |
| --- | --- | --- | --- | --- |
| P02B-R05 | major | verified / closed | helper docstring 明确私有/动态 API、Triton 3.7.1 边界和升级复验；CPU/GPU resource/default tests 通过 | 无 |
| P02B-R07 | suggestion | verified / closed | frozen/slotted dataclass 保持关键字构造与属性访问协议；Pydantic 不再出现在 source、pyproject 或 lockfile | 无 |
| P02B-R08 | minor | open | Ruff lint 与 BasedPyright 通过，但 `ruff format --check` 报生产文件需要重排动态 driver 调用 | 对 `gpu/triton/lesson02_fused_softmax.py` 运行 Ruff formatter，再复跑完整静态检查 |

可复现证据：

```text
CUDA_VISIBLE_DEVICES='' CPU-only：6 passed in 1.40s
默认 pytest/CI 范围：20 passed in 1.69s
物理 GPU 3：34 passed in 3.84s
Ruff lint：All checks passed
format check：1 file would be reformatted（仅生产文件）
BasedPyright：0 errors, 0 warnings, 0 notes
uv lock --check：通过，70 packages resolved
```

Formatter 的只读 diff 只把第 34–37 行链式调用恢复为一行；该行尾的 pyright task comment 使
Ruff 对长行豁免，因此格式化后 lint 仍应通过。本轮没有修改学习者生产实现或 agent-owned tests。
P02-C 只等待 P02B-R08 关闭。

### P02-B 最终复审（2026-08-06）

学习者运行 Ruff formatter 后，只读检查确认动态 driver 调用被规范化为 formatter 预期的一行，
没有语义变化。Ruff lint、format、BasedPyright、lockfile 与 diff 检查全部通过；沿用第五轮已通过
的 CPU-only 6、默认 CI 20、GPU 34 个测试证据，无需因纯布局变化重复运行 GPU。

| ID | 严重度 | 状态 | 最终证据 |
| --- | --- | --- | --- |
| P02B-R08 | minor | verified / closed | `ruff format --check` 报 3 files already formatted；Ruff lint 与 BasedPyright 同时通过 |

P02B-R01–R08 现已全部 verified/closed，P02-B 默认资源 grid 阶段完成。P02-C benchmark 正式
解锁；按照更新后的课程流程，下一步先由 AI agent 编写 benchmark 的结构/污染防护验收测试，
再由学习者实现资源表和 stages 1/2/4 的稳态计时实验。

### P02-C 第一轮评审（2026-08-06）

结论：第一版成功生成 18 行性能 CSV 和曲线，但当前数据不能回答后来选定的“prepared
steady-state wrapper”问题；persistent 三条曲线约 0.95 ms 且几乎不随 shape 变化，是 timed
closure 每次重复 resource introspection/grid setup 的明显证据。wrapper 自身的 output 分配则在
P02-Q10 后被确认是端到端 provider latency 的有意组成。用户怀疑的 BasedPyright 问题无法复现：
单文件与仓库级检查均为 0 errors；实际静态失败是 Ruff 的 7 个 E501 与 formatter 差异。

| ID | 严重度 | 状态 | 证据 | 学习者修改方向 |
| --- | --- | --- | --- | --- |
| P02C-R01 | blocking | rejected-with-rationale | 初始评审把任何 wrapper/output 分配都视为污染并要求 direct kernel；学习者指出 Torch baselines 仍以公开函数端到端执行，这会混用 API 层级 | 接受学习者的实际场景定义；保留 wrapper 检查/分配，direct-kernel 要求由 Q10 废止，重复 setup 另由 R08 跟踪 |
| P02C-R02 | major | open | Triton 两个分支实际传常量 25/100，却把调用者的 1/2 写入 record；新增转发测试准确失败 | 四个 providers 都把形参 `warmup_ms`/`rep_ms` 原样传给 `do_bench` |
| P02C-R03 | major | open | `torch.randn` 位于 provider/stages 校验之前；六个非法配置都会先分配 GPU tensor | 在任何 tensor 分配前一次性验证 provider、非 persistent 的 `None` stages，以及 persistent 的 1/2/4 |
| P02C-R04 | major | open | 小 `M=1` 时 grid 正确为 `(1,)`，但公式返回 0.00116；字段契约要求由 resident programs/SM 推导的 0.75 | occupancy 分子使用 `resident_programs_per_sm * NUM_WARPS`，分母使用 max warps/SM；不要使用全设备 grid |
| P02C-R05 | major | open | 脚本未输出三行资源表、GPU/软件版本或实验参数；现有 persistent 分支已取得 `resource` | 直接调用 `derive_resource_record` 取代 `ops.compute_grid`，保留目标 shape 的三项 record 并打印；`__main__` 打印一行 GPU/版本/warps/warm-up/rep，不增加复杂 collector/JSON |
| P02C-R06 | minor | open | `SHAPES` 被改成 `(index,M,N)`；生成图横轴仍显示 0.00/1.00/2.00，而非三种 shape | 保持 `SHAPES` 为 `(M,N)` pairs，另建 `X_VALUES`；run 后设置 shape tick labels 再保存 |
| P02C-R07 | minor | open | Ruff 报 7 个 E501；format check 报 1 file would be reformatted | 完成功能修改后运行 Ruff formatter，再复跑 lint/format/BasedPyright |
| P02C-R08 | blocking | learner-revised | persistent 分支现已在 `do_bench` 外准备 resource/grid，closure 调 public wrapper 并传 `num_programs=grid[0]` | 修正 R09 的 specialization 后重跑，确认资源探测不再进入每个样本，再 verified/closed |
| P02C-R09 | major | open | persistent compiled warm-up 当前使用 `next_power_of_2(size_m)`，而真正 kernel/wrapper 按列宽 N 选择 block；资源和实际 launch specialization 不一致 | 改为 `next_power_of_2(size_n)`，再用同一 resource 调 `derive_resource_record` 取得 grid |

按 tests-first 规则，本轮 AI agent 只修正/加强验收测试，没有修改学习者生产实现：恢复固定
`SHAPES`，验证非法配置先于 tensor 分配、四类 provider 转发 timing 参数，并加入小 grid 不改变
资源理论 occupancy 的边界。更新后测试为 24 cases：13 passed、11 failed；测试文件自身的
Ruff/format/BasedPyright 全绿，默认 CPU CI 仍为 20 passed。

可复现环境与证据：

```text
GPU：NVIDIA A100-SXM4-80GB（物理 GPU 3）
PyTorch 2.13.0+cu130；Triton 3.7.1；CUDA 13.0
benchmark tests：13 passed, 11 failed
默认 pytest：20 passed in 1.56s
benchmark source BasedPyright：0 errors, 0 warnings, 0 notes
仓库级 BasedPyright：0 errors, 0 warnings, 0 notes
gpu/triton 目录级 BasedPyright：1 个既有 vector_add.py constexpr error，与本次文件无关
benchmark source Ruff：7 个 E501；format check：would reformat
```

若编辑器仍显示大量 BasedPyright 错误，应确认工作区根目录为
`/workspace/programming-lab`，让语言服务器读取
根目录 `pyproject.toml` 的 `gpu/triton` execution environment；详细模式中的 `Could not import`
是解析追踪，最终 `0 errors` 时不属于诊断错误。

### P02-C 第二轮复审（2026-08-06）

结论：本版已经按学习者选定的实验语义让四条 timed closure 调用公开 provider，并把 persistent
resource/grid setup 移到 `do_bench` 外；`derive_resource_record`、三行 `resource.csv` 和一行
环境信息也已直接复用，没有引入冗余 collector。计时参数、理论 occupancy 和静态问题均已修好。
但这次生成的性能与资源表仍不能作为最终实验：resource warm-up 使用行数 `M` 推导 block，与
wrapper 实际按列数 `N` 编译的 specialization 不同；另外缺少计时前正确性检查、提前配置校验和
重复运行时的资源记录清理。生成图的横轴仍显示 0/1/2，而不是三种 shape。

| ID | 严重度 | 状态 | 本轮证据 | 学习者最小修改方向 |
| --- | --- | --- | --- | --- |
| P02C-R02 | major | verified / closed | 四类 provider 的 timing 转发用例通过；record 与 `do_bench` 都收到调用者的 1/2 | 无需再改 |
| P02C-R03 | major | needs-more-work | 6 个非法组合仍先进入 `torch.randn`，验收准确失败 | 在创建 `x` 前统一校验：provider 必须在四项集合中；前三类只接受 `None`；persistent 只接受 `STAGES` |
| P02C-R04 | major | verified / closed | 受控资源例和 `M=1` 边界均得到 75% theoretical occupancy | 无需再改 |
| P02C-R05 | major | learner-revised | `resource.csv` 已有三行，入口已有最小环境行；但三行来自 R09 的错误 specialization，尚不能验收 | 修正 R09 后重跑；保留现有 `derive_resource_record` 与 CSV 方案即可 |
| P02C-R06 | minor | needs-more-work | `SHAPES`/`X_VALUES` 已恢复正确结构；实际 PNG 横轴仍为 0.00、1.00、2.00 | 保存最终图前把三个 tick label 设置为 `(256,781)`、`(4096,781)`、`(4096,2049)`，或采用能输出同等标签的最小绘图方案 |
| P02C-R07 | minor | verified / closed | 两个 benchmark 文件 Ruff、format、BasedPyright 全绿；四个 Lesson 02 文件复跑也全绿 | 无需再改 |
| P02C-R08 | blocking | learner-revised | resource/grid 已在 `do_bench` 外推导，closure 已调用 wrapper 并传 `num_programs=grid[0]` | 结构正确；修正 R09 并通过 exact-specialization 测试后即可关闭 |
| P02C-R09 | major | needs-more-work | 新增验收在 `M=32,N=33` 观察到 warm-up block 为 32，正确列 specialization 应为 64；现有 `resource.csv` 因此不对应实际 wrapper kernel | 将 `next_power_of_2(size_m)` 改为 `next_power_of_2(size_n)`；其余 resource/grid 流程保持不变 |
| P02C-R10 | major | open | `measure_case` 从 input setup 直接进入 `do_bench`，没有 untimed provider output、reference、`assert_close` 或同步；新增时序验收失败 | setup 中计算 reference，先调用一次与 timed closure 相同的 provider，`torch.testing.assert_close` 后同步，再进入 `do_bench` |
| P02C-R11 | minor | open | `run_benchmark` 只清 `benchmark_records`；受控同进程重跑后旧 resource record 仍保留 | 在运行前同时调用 `resource_records.clear()` |

R01 继续保持 `rejected-with-rationale`：wrapper 的参数检查和 output/intermediate 分配属于本实验
有意测量的端到端 provider 成本，不应改回 direct kernel。R05/R08 的总体设计已经正确，只因 R09
读取了另一份 specialization 的资源而暂不能关闭。

按 AI-tests-first 规则，本轮只向 agent-owned benchmark test 新增 3 个语义用例，没有修改学习者
生产实现：验证 untimed correctness/sync、列宽 specialization + derived grid，以及同进程重跑清理
两类全局 records。现有 27 cases 为 18 passed、9 failed；9 个失败准确分成提前配置校验 6 个和
R09/R10/R11 各 1 个。

可复现证据：

```text
GPU：NVIDIA A100-SXM4-80GB（物理 GPU 3）
P02-C benchmark tests：18 passed, 9 failed
既有 Lesson 02 GPU tests：34 passed
默认 pytest：20 passed
Ruff：通过；format：4 files already formatted
BasedPyright：0 errors, 0 warnings, 0 notes
uv lock --check：通过；git diff --check：通过
```

当前 `detailed.csv` 的 18 行和 `resource.csv` 的 3 行只保留为第二次失败实验。它们已经证明重复
resource introspection 不再污染每个样本，但因 R09 的 grid/resource specialization 错配和 R10
缺少实验 shape 正确性门槛，暂不用于 stages 性能结论。

### P02-C 第三轮复审（2026-08-06）

结论：本版已修正列宽 specialization、derived grid、两类 records 清理和 shape labels；实际
`resource.csv` 已恢复为 `M=4096,N=781,BLOCK_SIZE=1024` 对应的三行资源，PNG 也显示三个具体
shape。第三轮中 agent-owned 的 records 测试最初因 fake perf-report 未创建 figure 而误报
`IndexError`；测试夹具已由 AI 修正，该错误不计入学习者 finding。真正剩余行为缺口为：persistent
stage 3 仍在 tensor 分配后才被拒绝；四个 provider 都只在 input 分配后同步，没有执行 untimed
provider、reference 与 `assert_close`。绘图实现另有两项 Ruff 清理。

| ID | 严重度 | 状态 | 本轮证据 | 学习者最小修改方向 |
| --- | --- | --- | --- | --- |
| P02C-R03 | major | learner-revised -> needs-more-work | 未知 provider、三个非 persistent 错带 stages、persistent 缺 stage 共 5 项已在分配前拒绝；仅 stage 3 仍先进入 `torch.randn` | persistent 分支不要只判断 `None`，应在分配前要求 `num_stages in STAGES` |
| P02C-R05 | major | verified / closed | 最新 `resource.csv` 三行为 stages 1/2/4：regs 均 32，shared 为 32/4128/12320，resident/SM 均 8，grid 均 `(864,)`，occupancy 均 100%；入口环境行保留 | 无需再改资源采集结构 |
| P02C-R06 | minor | learner-revised -> needs-more-work | agent 测试和实际 PNG 均确认三个 shape 标签；但上一轮 AI 示例使用的 `×` 触发 RUF001 | 只把标签分隔符改为 ASCII `x`；该兼容性问题来自 AI 提示，非学习者设计错误 |
| P02C-R08 | blocking | verified / closed | exact resource/grid setup 位于 `do_bench` 外，wrapper closure 传入 `num_programs=grid[0]`；对应验收通过 | 无需再改 |
| P02C-R09 | major | verified / closed | warm-up 已改为 `next_power_of_2(size_n)`；`M=32,N=33` 验收观察到 block 64，并收到 derived grid 32 | 无需再改 |
| P02C-R10 | major | learner-revised -> needs-more-work | 四个分支均调用了 `torch.cuda.synchronize`，但都未在 `do_bench` 前调用 provider 或 `torch.testing.assert_close`；四项参数化时序验收失败 | 每个 case 构造一个与 timed closure 相同的 operation；计时前计算 reference、调用 operation、`assert_close`、同步，再把 operation 交给 `do_bench` |
| P02C-R11 | minor | verified / closed | 修正后的受控同进程重跑测试确认 `benchmark_records` 与 `resource_records` 都只保留 fresh record | 无需再改 |
| P02C-R12 | minor | open | Ruff 报 import block 未排序和标签字符 RUF001；format 与 BasedPyright 仍通过 | 将 `matplotlib` import 排到 Torch/Triton 前，并使用 ASCII `x`；复跑 Ruff |

按测试归属规则，AI 本轮修复了 fake benchmark 的 figure fixture，并把 correctness/sync 时序从一个
代表性 provider 参数化到四个 provider。验收因此由 27 增至 30 cases；当前 25 passed、5 failed，
其中 1 个是 unsupported stage，4 个是四类 provider 缺少 correctness assertion。

可复现证据：

```text
GPU：NVIDIA A100-SXM4-80GB（物理 GPU 3）
P02-C benchmark tests：25 passed, 5 failed
既有 Lesson 02 GPU tests：34 passed
默认 pytest：20 passed
benchmark test Ruff/format/BasedPyright：全绿
benchmark source Ruff：I001 + RUF001
benchmark source format：通过；BasedPyright：0 errors
git diff --check：通过
```

最新 18 行性能表、3 行资源表和带 shape 标签的 PNG 已结构完整，但 R10 尚未建立实验 shape 的
显式 correctness gate；修正后应再跑一次，届时才作为 P02-C 最终实验进入性能复盘。

### P02-C benchmark/正确性职责修订（2026-08-06）

学习者明确决定 benchmark 不进行正确性检查。复核后接受该实验边界，并把正确性证据移到独立
功能测试；此前第三轮结论保留为契约变更前的评审历史。

| ID | 状态更新 | 证据 |
| --- | --- | --- |
| P02C-R03 | verified / closed | persistent 现要求 `num_stages in STAGES`，unsupported stage 验收在 tensor 分配前通过 |
| P02C-R06 | verified / closed | agent 测试与实际 PNG 都确认三个 shape 标签；字符静态规则单独由 R12 跟踪 |
| P02C-R10 | rejected-with-rationale | 删除 benchmark-local correctness 要求；三个 exact shapes 的 ordinary/persistent stages 1/2/4 独立 GPU 测试全部通过，`torch_naive_softmax` baseline 也单独通过 |
| P02C-R12 | learner-revised -> needs-more-work | import 顺序已修正；Ruff 仅余标签字符 `×` 的 RUF001，改为 ASCII `x` 即可 |

AI-owned test 变更与实测：

```text
benchmark harness：27 passed
Lesson 02 GPU functional suite：37 passed
  - 新增 (256,781)、(4096,781)、(4096,2049)
  - 每项验证 ordinary 与 persistent stages 1/2/4 对照 PyTorch
默认 pytest：20 passed
两个测试文件 Ruff/format/BasedPyright：全绿
benchmark source：format/BasedPyright 通过；Ruff 仅余 RUF001
```

至此 benchmark 行为 finding 已全部关闭；只需完成 R12 的单字符静态清理并重跑最终实验产物。

### P02-C 最终实验与性能复盘（2026-08-06）

最终脚本在物理 GPU 3 上运行成功：A100-SXM4-80GB、PyTorch 2.13.0+cu130、Triton 3.7.1、
CUDA build 13.0、`num_warps=8`、warm-up 25 ms、rep 100 ms。计时语义为 prepared
steady-state wrapper-level latency：保留每次公开 provider 调用的检查、分配与 dispatch，排除
persistent resource/grid 初始化；benchmark 不做 correctness assertion，三个 exact shapes 的
正确性由独立 GPU suite 提供。

`M=4096,N=781` 的 compiled resources：

| stages | registers/thread | shared/program | register limit | shared limit | thread limit | resident/SM | grid | theoretical occupancy |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 32 | 32 B | 8 | 5216 | 8 | 8 | `(864,)` | 100% |
| 2 | 32 | 4,128 B | 8 | 40 | 8 | 8 | `(864,)` | 100% |
| 4 | 32 | 12,320 B | 8 | 13 | 8 | 8 | `(864,)` | 100% |

结课后为解释性能结果，补充读取了 `M=4096,N=2049` 对应 specialization 的编译资源：

| stages | registers/thread | shared/program | register limit | shared limit | thread limit | resident/SM | grid | theoretical occupancy |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 63 | 32 B | 4 | 5,216 | 8 | 4 | `(432,)` | 50.0% |
| 2 | 48 | 16,416 B | 5 | 10 | 8 | 5 | `(540,)` | 62.5% |
| 4 | 62 | 49,184 B | 4 | 3 | 8 | 3 | `(324,)` | 37.5% |

最终有效 GB/s：

| shape | torch naive | torch fused | Triton naive | persistent s1 | persistent s2 | persistent s4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `256 x 781` | 38.10 | 142.00 | 195.25 | 195.25 | 173.56 | 173.56 |
| `4096 x 781` | 337.73 | 999.68 | 1041.33 | 1041.33 | 999.68 | 892.57 |
| `4096 x 2049` | 331.15 | 910.67 | 1395.06 | 1260.92 | 1111.32 | 1111.32 |

结论按证据强度分层：

1. **事实**：对 `N=781`，stages 增加显著提高 shared-memory 用量，但 registers、resident
   programs、grid 和理论 occupancy 均不变；因此不能用“occupancy 下降”解释这个 shape 的差异。
2. **事实**：三个 shape 中 persistent stage 1 均不慢于 stages 2/4；`M=256` 时 grid 被 cap 为
   256，每个 program 只有一行，没有下一次跨行迭代可供软件流水。
3. **事实**：`M=4096,N=781` 时 grid 为 864，每个 program 只处理 4–5 行；短循环留给 stage 4
   稳态流水的空间很少，更深 stages 未在本次端到端测量中转化为收益。
4. **事实**：`M=4096,N=2049` 时 stage 1/2/4 的 grid 分别为 432/540/324，理论 occupancy 分别为
   50%/62.5%/37.5%；Triton naive 仍最快。stage 2 occupancy 高于 stage 1 但性能更慢，再次说明
   occupancy 不能单独预测性能。
5. **推断边界**：当前 `N=2049` 对比同时改变 pipeline depth 和资源推导出的 grid，衡量的是各
   stage 的默认完整策略，不能把差异只归因于 `num_stages`。结果足以反驳“更多 stages 单调更快”；
   没有固定-grid 对照或 profiler stall/throughput 证据时，不进一步断言单一根因。

最终产物为 [`detailed.csv`](../../../experiment_results/lesson02/softmax/detailed.csv)、
[`resource.csv`](../../../experiment_results/lesson02/softmax/resource.csv) 和
[`lesson02_softmax.png`](../../../experiment_results/lesson02/softmax/lesson02_softmax.png)。

P02C-R12 的 ASCII label 修改后，Ruff、format、BasedPyright 全绿；P02-C findings 已全部
`verified/closed` 或 `rejected-with-rationale`，无开放项。

## 10. 掌握验收

### 概念验收

将在实践和答疑后进行：

1. 用自己的话描述 persistent program、row block 和元素之间的映射。
2. 从 `M`、`N` 和资源占用推导 grid，并解释不能整除时的行覆盖。
3. 解释 `BLOCK_SIZE`、`num_stages` 和 `num_warps` 的确定时机与作用。
4. 解释 padding、两次 reduction 和主要访存模式。
5. 说明 shape、dtype 或 stride 改变时哪些部分必须调整。

### 实践验收

- [x] 官方示例的核心版本可以独立重写，而不是逐行照抄
- [x] 非 2 的幂列宽正确
- [x] reference、数学不变量与断言完整
- [x] 错误输入行为明确
- [x] P01 代码通过项目格式和相关静态检查
- [x] P02 kernel/wrapper 与测试通过项目格式和相关静态检查
- [x] P02-C benchmark 通过相关静态检查
- [x] 性能结论有可复现实验支持
- [x] 已完成普通 grid 到 persistent grid、默认资源 grid 和 stages 对比等变式

### 最终掌握结论

- **概念**：能够解释行级 reduction、`-inf` padding、persistent 静态 grid-stride、软件流水、
  theoretical occupancy 与实际利用率的区别，并独立完成资源上限计算。
- **实践**：完成普通与 persistent softmax、默认资源 grid、资源读取兼容层和 wrapper-level
  benchmark；agent-owned correctness、benchmark、默认 CI 与静态检查全部通过。
- **反思**：已修正“stage 是独立 worker/固定代码段”“occupancy 等于计算单元利用率”以及
  “persistent 必须使用动态 while 队列”等早期模型；能够用本次实测反驳“stages 越多越快”。
- **范围决定**：P03 log-softmax 不再作为本课门槛；本课已有 persistent 调度、资源推导和性能
  评价三类独立变式。若以后需要练习 reduction 迁移，另开一个聚焦的短练习。
- **遗留项**：无阻塞或 major finding；profiler、autotune、cache 与置信区间属于后续性能专题。

## 11. 当前检查点与本课总结

### 暂停检查点（2026-07-31）

| 项目 | 状态 |
| --- | --- |
| 暂停位置 | Q03 已确认关闭；P01 契约已开放，但自主实现尚未开始 |
| 已完成 | 源码地图、数学与流量分析、官方脚本实测；Q01–Q03 已确认；三层实践已设计 |
| 实测证据 | 官方正确性与 benchmark 通过；stages 1/2/4 编译资源和探索性延迟已记录 |
| 学习者产物 | `lesson02_fused_softmax.py` 与对应测试均未创建；没有待处理代码评审意见 |
| 未解决问题 | 无；Q01 persistent/stages、Q02 persistent 类型、Q03 occupancy 均已关闭 |
| 未完成 | P01 实现与测试、P02/P03、完整知识复述、代码评审与掌握验收 |
| 当前阻塞 | 无；本次是学习者主动暂停 |
| 恢复入口 | 直接阅读第 7 节 P01 契约，不重复完整讲解或 Q01–Q03 |
| 下一动作 1 | 学习者创建 P01 的 kernel/wrapper 与 GPU tests |
| 下一动作 2 | 运行指定 GPU pytest、Ruff check 和 format check |
| 下一动作 3 | 提交第一版代码以及 P01 的三项设计说明，进入代码评审 |
| P02 解锁门槛 | P01 正确性、接口、静态检查和主要评审问题全部通过 |
| 暂停归档 | Lesson 02-A 原始对话暂停快照已导出并审核，共 29 条消息 |

### 恢复检查点（2026-08-03）

| 项目 | 状态 |
| --- | --- |
| 恢复来源 | 上述 2026-07-31 暂停检查点与 Lesson 02-A 原始对话暂停快照 |
| 仓库状态 | 工作区干净，`main` 与 `origin/main` 同步 |
| 当前阶段 | P01 普通 grid row-wise fused softmax 自主实践 |
| 学习者产物 | Kernel/wrapper 与 GPU test 文件仍未创建；没有待处理评审意见 |
| 已关闭内容 | 完整讲解及 Q01 persistent/stages、Q02 persistent 类型、Q03 occupancy |
| 当前任务 | 按第 7 节 P01 契约独立完成实现、测试和三项设计说明 |
| 当前阻塞 | 无 |
| P02 解锁门槛 | P01 正确性、接口、静态检查和主要评审问题全部通过 |

### P01 第一轮评审检查点（2026-08-03）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P01 第一轮评审完成，等待学习者修改 |
| 已验证 | 8 个现有 GPU 用例、Ruff、格式、BasedPyright 通过；额外诊断确认数值主路径和当前异常行为 |
| 开放 findings | P01-R01–R04（major），P01-R05–R06（minor） |
| 当前阻塞 | 无 blocking finding；4 项 major 阻止 P02 解锁 |
| 下一动作 | 学习者修改 launch、补齐测试、修正两条消息，并重新复述第三项设计说明 |
| 复审命令 | P01 GPU pytest、Ruff、format check、BasedPyright |
| P02 解锁门槛 | P01-R01–R04 至少全部 verified/closed，且 P01 完成定义满足 |

### P01 第二轮评审检查点（2026-08-03）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P01 第二轮复审完成，等待最后一轮小修 |
| 已关闭 | P01-R01、R02、R03、R04、R06 |
| 待处理 | P01-R05（minor, needs-more-work）、P01-R07–R08（minor, open） |
| GPU 证据 | 物理 GPU 5 上 13 passed；`metadata.num_warps == 8` |
| 环境事件 | 物理 GPU 0 因 81029/81920 MiB 已占用而 OOM，不计作实现失败 |
| 下一动作 | 精确化 `N=0` 消息，移除未使用赋值，为 Triton launcher 添加窄范围 Pyright ignore |
| P02 解锁门槛 | P01-R05、R07、R08 verified/closed，Ruff/format/BasedPyright 全部通过 |

### P01 完成检查点（2026-08-04）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P01 已完成，P02 已解锁但尚未开始 |
| 正确性 | 物理 GPU 3 上 13 passed；reference、row-sum、边界和错误输入均有证据 |
| 静态检查 | Ruff、format check、BasedPyright 全部通过 |
| Launch 证据 | `metadata.num_warps == 8` |
| Findings | P01-R01–R08 全部 verified/closed，无开放项 |
| 概念证据 | Grid/block/lane、`-inf` padding、空 batch/空 reduction domain 三项说明均通过 |
| 下一动作 | 进入 P02 前布置 persistent softmax、occupancy 与 stages 实验的详细契约 |
| Lesson 02 剩余 | P02、P03、整课知识复述与最终掌握验收 |

### P01 完成后暂停检查点（2026-08-04）

| 项目 | 状态 |
| --- | --- |
| 暂停位置 | P01 已完成；P02 已解锁但没有开始讲解、预测或实现 |
| 已完成工作 | 学习者独立完成 P01 kernel、wrapper 和 13 个测试；三轮评审结束 |
| 验收证据 | 物理 GPU 3 上 13 passed；Ruff、format check、BasedPyright 全绿；`metadata.num_warps == 8` |
| Findings | P01-R01–R08 全部 verified/closed；P01 无开放项 |
| 未解决问题 | 无；本次是学习者主动暂停，不是被问题阻塞 |
| 未完成 | P02 persistent/stages 实践、P03 log-softmax、整课复述与最终掌握验收 |
| 恢复入口 | 直接从第 7 节 P02 开始，先布置详细实践契约；不重复 P01 或已关闭的 Q01–Q03 |
| 下一动作 1 | 明确 P02 的接口、persistent grid、资源读取和实验矩阵 |
| 下一动作 2 | 学习者先写资源/性能预测，再自主实现 persistent 版本 |
| 下一动作 3 | 运行正确性、覆盖性、资源与计时实验，进入 P02 评审 |
| P03 解锁门槛 | P02 正确性、persistent 行覆盖、资源解释和主要评审问题通过 |
| 暂停归档 | Lesson 02-B 原始对话暂停快照已导出并审核，共 32 条消息 |

### P02 恢复检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 恢复来源 | P01 完成后暂停检查点与 Lesson 02-B 原始对话暂停快照 |
| 仓库状态 | 工作区干净；`main` 与 `origin/main` 同步于 `b6c3b3f` |
| 当前阶段 | P02 实践前预测已通过，进入 persistent softmax 自主实现 |
| 已关闭内容 | P01 实现、13 个测试、三轮评审与 P01-R01–R08 |
| 当前任务 | P02 自主实现；先完成显式 `num_programs` 的 persistent kernel/wrapper 与正确性测试 |
| 当前阻塞 | 无 |
| 实验边界 | 当前 NVIDIA/A100；固定 8 warps；stages 1/2/4；不要求固定性能胜负 |
| 下一动作 | 保留 P01 基线，完成 P02-A 强制 program 数调度；正确后再做 P02-B 默认资源 grid |
| P03 解锁门槛 | P02 正确性、唯一覆盖证明、实验解释、静态检查和主要评审问题全部通过 |

### P02-A 第一轮评审检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-A 第一版评审完成，等待学习者修改 |
| 已验证 | Persistent 行覆盖、stages 1/2/4 数值、program cap、空 batch 与非法参数；GPU 25 passed |
| 开放 findings | P02A-R01（major）；P02A-R02–R05（minor） |
| 当前阻塞 | 无 blocking；R01 与静态检查门槛阻止进入 P02-B |
| 下一动作 | 统一 stage constexpr/backend option，清理导入和 grid，格式化，并添加窄范围 Pyright ignore |
| 复审证据 | GPU pytest、Ruff、format、BasedPyright，以及 compiled metadata stages/warps |
| P02-B 解锁门槛 | P02A-R01–R05 verified/closed，25 个测试与所有静态检查通过 |

### P02-A 第二轮复审检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-A 第二轮复审完成，等待最后一处测试语义收紧 |
| 已关闭 | P02A-R01–R04 |
| 待处理 | P02A-R05（minor, needs-more-work） |
| 已验证 | GPU 25 passed；Ruff/format/BasedPyright 全绿；metadata stages 1/2/4、warps 均为 8 |
| 下一动作 | 将 program 非正数测试从 `num_programs` 字段名匹配收紧为 `positive`/等价稳定语义 |
| P02-B 解锁门槛 | P02A-R05 verified/closed；同一组 GPU 与静态检查继续通过 |

### P02-A 完成检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-A 已完成；P02-B 默认资源 grid 已解锁但尚未开始 |
| 正确性 | 物理 GPU 3 上 25 passed；persistent 非整除覆盖、program cap、三种 stages 均通过 |
| 静态检查 | Ruff、format check、BasedPyright 全部通过 |
| 编译证据 | requested/compiled stages 均为 1/2/4；`num_warps` 均为 8 |
| Findings | P02A-R01–R05 全部 verified/closed，无开放项 |
| 下一动作 | 实现 `num_programs=None`：读取 compiled/device resources，推导安全 resident programs 与 grid |
| 暂不进行 | P02 benchmark；等待默认资源 grid 的正确性与资源表先通过评审 |
| P02-C 解锁门槛 | P02-B 默认 grid、资源边界、空 shared 情况和 resource table verified |

### P02-B 第一轮评审检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-B grid 第一版评审完成，等待学习者修改 |
| 公式方向 | register/shared/thread limits 取 min，再乘 SM 数并 cap 到 `M`，方向正确 |
| 开放 findings | P02B-R01–R02（blocking）；R03–R05（major）；R06（minor） |
| 当前证据 | 默认调用均 KeyError；显式 program 路径 25 passed；静态检查失败 |
| 下一动作 | 修复资源来源与统一 warps，处理 shared=0 和零 resident，再补默认/边界测试 |
| P02-C 解锁门槛 | P02B-R01–R06 verified/closed；默认 grid correctness/resource info 与静态检查通过 |

### P02-B 第二轮复审检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-B 默认路径已能运行，第二轮复审后等待边界、测试与静态检查修改 |
| 正确性 | 手工默认调用覆盖 `(10,7)`、`(4096,781)` 和 stages 1/2/4，均与 PyTorch 一致；既有显式路径 25 passed |
| Findings | P02B-R02 verified/closed；R01、R03、R04、R06 needs-more-work；R05 open |
| 当前阻塞 | warps 配置未集中；空 batch 绕过 program 校验；零 resident 被强制成 grid 1；默认/resource grid 无回归测试；静态检查失败 |
| 下一动作 | 先修 R01/R03/R04，提取最小资源/grid helper 并补 R05 测试，最后清理 R06 |
| P02-C 解锁门槛 | P02B-R01–R06 verified/closed；默认 grid correctness/resource info 与静态检查通过 |

### P02-B 第三轮复审检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-B 功能行为已通过，等待资源边界回归测试、可观察资源信息与静态清理 |
| 正确性 | 物理 GPU 3 上 30 passed；默认与显式 program 路径、stages 1/2/4 均通过 |
| 资源诊断 | normal/shared=0 得到 `(648,)`；零 resident 明确抛 `RuntimeError` |
| Findings | P02B-R01–R02 verified/closed；R03–R06 needs-more-work |
| 当前阻塞 | R03/R04 边界仅有临时诊断；computed limits/resident/grid 尚不可观察；Ruff、format、BasedPyright 未通过 |
| 下一动作 | 增加空 batch 组合与纯 grid helper 测试，暴露资源表所需结果，写明私有 API 边界，最后通过三项静态检查 |
| P02-C 解锁门槛 | P02B-R01–R06 verified/closed；默认 grid correctness/resource info 与静态检查通过 |

### P02-B AI-owned 测试检查点（2026-08-05）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-B 所需验收测试已由 AI agent 补齐，等待学习者完成最小生产代码清理 |
| CPU evidence | 新增 6 个 pure-grid cases；默认 pytest 共 20 passed |
| GPU evidence | 物理 GPU 3 上 34 passed；空 batch 组合和实际 resource helper 均覆盖 |
| Findings | P02B-R01–R04 verified/closed；R05–R06 needs-more-work |
| Agent-owned tests | 已完成；学习者无需继续编写测试 |
| Learner next action | 注释私有 API 兼容性边界；标注 helper 类型；添加窄范围 pyright ignore；格式化生产文件 |
| P02-C 解锁门槛 | P02B-R05–R06 verified/closed；完整 Ruff、format、BasedPyright 通过 |

### P02-B 第四轮复审检查点（2026-08-06）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-B 功能、测试与静态检查全部通过，仅余一处私有 API 兼容性说明 |
| 测试证据 | CPU-only 6、默认 CI 20、物理 GPU 3 上 34 个用例全部通过 |
| 静态证据 | Ruff、format、BasedPyright 全部通过 |
| Findings | P02B-R01–R04、R06 verified/closed；R05 needs-more-work；R07 nonblocking suggestion |
| Agent-owned tests | 已适配 typed `Resource` 属性协议；学习者无需修改测试 |
| Learner next action | 在 `get_gpu_resource` 记录 `_init_handles`、metadata 和 driver utils 的 Triton 版本兼容性边界；决定是否保留 Pydantic |
| P02-C 解锁门槛 | P02B-R05 verified/closed；R07 可带理由保留或采用标准库记录类型 |

### P02-B 第五轮复审检查点（2026-08-06）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-B 功能、资源边界、测试、类型与依赖已通过；只差生产文件格式化 |
| 验证证据 | CPU-only 6、默认 CI 20、GPU 34；Ruff lint、BasedPyright、lock check 通过 |
| Findings | P02B-R01–R07 verified/closed；P02B-R08 minor/open |
| Learner next action | 运行 `uv run --frozen ruff format gpu/triton/lesson02_fused_softmax.py`，再复跑三项静态检查 |
| P02-C 解锁门槛 | P02B-R08 verified/closed；Ruff、format、BasedPyright 全绿 |

### P02-B 完成检查点（2026-08-06）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-B 默认资源 grid 完成；P02-C benchmark 已解锁 |
| 正确性证据 | CPU-only 6、默认 CI 20、物理 GPU 3 上 34 个用例通过 |
| 静态证据 | Ruff、format、BasedPyright、`uv lock --check`、`git diff --check` 全部通过 |
| Findings | P02B-R01–R08 全部 verified/closed，无开放项 |
| 下一动作 1 | AI agent 定义并编写 P02-C benchmark 验收测试，覆盖 warm-up、同步、重复计时与结果 schema |
| 下一动作 2 | 学习者实现 `lesson02_fused_softmax_benchmark.py`，生成 stages 1/2/4 的资源表和稳态延迟/GB/s 表 |
| P02 完成门槛 | P02-C 实验可复现、预测复盘完成，随后进行 P02 概念/实践/反思验收 |

### P02-C tests-first 检查点（2026-08-06）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-C 第一轮评审与计时边界复议完成；采用 prepared steady-state wrapper-level 端到端比较 |
| Agent-owned tests | 24 个显式 GPU cases；补充校验顺序、timing 参数转发与小 grid occupancy 边界 |
| 当前 red | 13 passed、11 failed；对应 SHAPES、occupancy、提前校验和 Triton timing 参数四类问题 |
| 默认 CI | 20 passed；P02-C 测试不在默认 CPU testpaths |
| Findings | R01 rejected-with-rationale；R08 blocking/learner-revised；R02–R05、R09 major/open；R06–R07 minor/open |
| Learner next action | 把 persistent warm-up block 改为由 `size_n` 推导，直接用 `derive_resource_record` 取得 grid/三行资源；打印一行环境信息，再处理其余 findings |
| Green 门槛 | 24 个 P02-C cases、既有 34 个 GPU cases和完整静态检查通过 |
| 实验门槛 | 修正后重跑 3 行资源表与 18 行端到端性能表，明确 one-time JIT/resource/grid setup excluded；首次结果只保留为失败实验 |

### P02-C 第二轮复审检查点（2026-08-06）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | P02-C wrapper-level 结构已成立；修正四类 harness 边界后再生成最终实验 |
| Agent-owned tests | 27 个显式 GPU cases；新增 correctness/sync、exact specialization/grid 和重复运行清理 |
| 当前 red | 18 passed、9 failed；提前校验 6 个，R09/R10/R11 各 1 个 |
| 回归证据 | 既有 Lesson 02 GPU 34 passed；默认 CI 20 passed |
| 静态证据 | Ruff、format、BasedPyright、lock check、`git diff --check` 全绿 |
| Findings | R02/R04/R07 verified/closed；R01 rejected；R03/R06/R09 needs-more-work；R05/R08 learner-revised；R10/R11 open |
| Learner next action | 先做前置配置校验；把 warm-up block 改为按 `size_n`；补 untimed reference/assert/sync；运行前 clear 两类 records；最后修 shape tick labels |
| Green 门槛 | 27 个 P02-C cases、既有 34 个 GPU cases和完整静态检查通过 |
| 实验门槛 | 全绿后重新生成 3 行资源表、18 行 performance table 和带 shape 标签的图；当前第二版输出仍标为失败实验 |

### P02-C 第三轮复审检查点（2026-08-06）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | 资源/grid/records/plot 已验证；补 correctness gate 和最后一项 stage 前置校验 |
| Agent-owned tests | 30 个显式 GPU cases；correctness/sync 覆盖四个 provider，plot fixture 已修正 |
| 当前 red | 25 passed、5 failed；unsupported stage 1 个，四类 provider correctness 4 个 |
| 回归证据 | 既有 Lesson 02 GPU 34 passed；默认 CI 20 passed |
| 静态证据 | 测试 Ruff/format/BasedPyright 全绿；生产文件 format/BasedPyright 通过，Ruff 剩 I001/RUF001 |
| Findings | R05/R08/R09/R11 verified/closed；R03/R06/R10 needs-more-work；R12 minor/open；R01 rejected |
| Learner next action | stage 3 在分配前拒绝；四类 operation 计时前做 reference/assert_close/sync；标签改 ASCII `x` 并排序 import |
| Green 门槛 | 30 个 P02-C cases、既有 34 个 GPU cases和完整静态检查通过 |
| 实验门槛 | 全绿后重新生成并验收最终 3 行资源、18 行性能和带 shape 标签的 PNG |

### P02-C correctness 职责修订检查点（2026-08-06）

| 项目 | 状态 |
| --- | --- |
| 当前阶段 | benchmark 行为验收全绿；最后清理 RUF001 后重跑最终产物 |
| Benchmark tests | 27 passed；不在 `measure_case` 内做 correctness assertion |
| 独立正确性 | Lesson 02 GPU 37 passed；三个 benchmark shape × ordinary/persistent stages 1/2/4 均覆盖 |
| 默认 CI | 20 passed |
| 静态证据 | 两个测试文件全绿；benchmark source format/BasedPyright 通过，Ruff 仅余 `×` 的 RUF001 |
| Findings | R03/R05/R06/R08/R09/R11 verified/closed；R01/R10 rejected-with-rationale；R12 needs-more-work |
| Learner next action | 把 shape 标签的 `×` 改成 ASCII `x`，复跑 Ruff，再运行完整 benchmark |
| P02-C green 门槛 | benchmark 27、功能 GPU 37、默认 CI 20 和完整静态检查全部通过 |

### Lesson 02 完成检查点（2026-08-06）

| 项目 | 最终状态 |
| --- | --- |
| 课程状态 | **已完成**；学习者明确要求结束 Lesson 02 |
| 核心产物 | 普通 fused softmax、persistent stages 1/2/4、默认资源 grid、资源表与 wrapper-level benchmark |
| 正确性 | 物理 GPU 3：Lesson 02 功能测试 37 passed；三个 benchmark shapes 独立覆盖 |
| Benchmark | 27 passed；最终 18 行性能、3 行资源和 ASCII shape PNG 已重跑 |
| 默认 CI | 20 passed |
| 静态证据 | 四个 Lesson 02 文件 Ruff/format/BasedPyright 全绿；`git diff --check` 通过 |
| Findings | 所有 blocking/major/minor 均 verified/closed 或 rejected-with-rationale；无开放项 |
| 掌握证据 | 概念复述、商余唯一覆盖、资源复算、persistent 变式、预测与实测复盘齐全 |
| P03 范围 | 已完成 log-softmax 概念回顾；编码迁移仍取消，不阻塞 Lesson 02 完成 |
| 后续学习规则 | benchmark 测试聚焦性能影响因素与测量有效性，不做参数校验测试；减少非核心工作 |
| 对话归档 | 02-A 29 条、02-B 32 条、02-C 153 条、02-D 6 条、02-E 9 条，均含 provenance 并已审核 |

### 最重要的三个结论

1. Fused softmax 的收益核心是让行内中间值留在片上，避免多个 kernel 反复访问 DRAM。
2. 行级 reduction 要求静态 block 和有数学意义的 padding；本例的 `-inf` 同时保护 max 与 sum。
3. Persistent grid 由资源 occupancy 决定 resident programs，再由每个 program 循环覆盖多行。

### 我曾经的关键误解及修正

- 最初把 `num_stages=2` 表述成两个相互独立的“stage 工作”；修正为两个相互独立的循环迭代
  可以同时在途，而 stage 不是独立 worker 或固定代码段。
- 最初认为片上资源不足会直接拖慢单个 stage；修正为资源占用通常先减少 resident programs 和
  occupancy，只有 spilling 等情况才会直接增加单 program 的内存流量。
- 最初把 persistent kernel 限定为 `while + 动态任务队列`；修正为 persistent 的共同核心是
  有限长期 workers 复用处理多个 work items，静态 grid-stride 与动态 dequeue 是不同分配策略。

### 可复用到后续课程的模式

- `next_power_of_2 + mask + reduction identity`；
- 一整个 reduction domain 由一个 program 负责；
- 先编译读取资源占用，再决定 persistent launch grid；
- 用有效工作量统一比较性能，同时明确它不是实际硬件流量。

### 进入下一课的条件

- [x] 所有阻塞评审意见均已关闭
- [x] 概念和实践验收均已通过
- [x] 文档中的问题、实验和最终实现已同步
- [x] 学习者确认结束本课；下一课可在新请求中启动

### P03 快速回顾完成检查点（2026-08-07）

| 项目 | 状态 |
| --- | --- |
| 课程状态 | Lesson 02 仍为**已完成**；本段是结课后快速回顾，没有重开课程 |
| 完成内容 | stable log-softmax 公式、与 softmax kernel 的共用框架、padding/空维度、正确性不变量、资源和训练边界 |
| 最小证据 | CPU float32：`x=[0,-1000]` 时 `log(softmax(x))=[0,-inf]`，stable log-softmax 为 `[0,-1000]` |
| 学习者确认 | 正确复述“主要是计算公式差异，Triton 框架与优化方法大体共用” |
| P03 范围 | 编码实践继续取消；未新增实现、测试或 benchmark |
| 开放问题 | 无 |
| 下一入口 | 在学习者提出新请求时开始 Lesson 03 Matrix Multiplication |
| 对话归档 | 02-E 收尾快照已导出并审核，共 9 条可见消息 |

## 12. 原始对话与参考资料

### 原始对话归档

#### Lesson 02-A：开课至 P01 实现前

- **归档文件**：[02-fused-softmax.md](../dialogues/02-fused-softmax.md)
- **归档性质**：Lesson 02-A 暂停快照。
- **Codex session**：`019fb5e8-54c6-77c0-8c7a-b489d135ee40`
- **包含起点**：用户消息“很好，接下来让我们进入triton的下一课学习。”
- **排他终点**：用户消息“接下来我们先暂停课程，打个断点。”
- **消息范围**：2026-07-31 03:45:52–06:08:50 UTC，共 29 条；包含 commentary。
- **哈希**：source snapshot
  `2ec0ef760e13e263e068c3b6fab9cc729c28aafecda72af6193e625080b86f7b`；
  selected dialogue
  `725d001847c51f307bdeb5de519c96240c88946752db0682d7a504e635a2c153`。
- **审核结果**：首尾边界正确，7 条用户消息与 22 条助手消息顺序合理；未包含暂停归档元对话、
  先前仓库整理对话、system/developer/tool 事件、客户端注入、凭据、私人 home 路径或附件内容。
- **导出命令**：

  ```bash
  uv run --frozen python scripts/export_codex_dialogue.py export \
    <session-jsonl> \
    docs/triton-learning/dialogues/02-fused-softmax.md \
    --title '第 02 课：Fused Softmax 原始学习对话（暂停快照）' \
    --lesson 02-fused-softmax \
    --start-user '很好，接下来让我们进入triton的下一课学习。' \
    --end-before-user '接下来我们先暂停课程，打个断点'
  ```

#### Lesson 02-B：P01 实践与三轮评审

- **归档文件**：[02-fused-softmax-part2.md](../dialogues/02-fused-softmax-part2.md)
- **归档性质**：Lesson 02-B 暂停快照；P01 已完成，P02 尚未开始。
- **Codex session**：`019fb5e8-54c6-77c0-8c7a-b489d135ee40`
- **包含起点**：用户消息“好的，现在让我们从断点处恢复lesson 02吧”。
- **排他终点**：用户消息“我们可以先暂停提交一下阶段性结果”。
- **消息范围**：2026-08-03 00:53:02–2026-08-04 09:15:44 UTC，共 32 条；包含 commentary。
- **哈希**：source snapshot
  `2a4d52241eef9418517f69f30b2596909e3b7c8c763d24b140fd22aa89ef3b60`；
  selected dialogue
  `c38baca914597070da593afaa892e392a1088a6fd9404974711e34ed0cb8be49`。
- **审核结果**：首尾边界正确，8 条用户消息与 24 条助手消息顺序合理；未包含本次暂停提交
  元对话、Lesson 02-A 片段、system/developer/tool 事件、客户端注入、凭据、私人 home 路径或
  附件内容。
- **导出命令**：

  ```bash
  uv run --frozen python scripts/export_codex_dialogue.py export \
    <session-jsonl> \
    docs/triton-learning/dialogues/02-fused-softmax-part2.md \
    --title '第 02 课：Fused Softmax P01 实践与评审原始对话（暂停快照）' \
    --lesson 02-fused-softmax-part2 \
    --start-user '现在让我们从断点处恢复lesson 02吧' \
    --end-before-user '我们可以先暂停提交一下阶段性结果'
  ```

#### Lesson 02-C：Persistent、资源与 Benchmark 实践至结课

- **归档文件**：[02-fused-softmax-part3.md](../dialogues/02-fused-softmax-part3.md)
- **归档性质**：结课段；从 P02 开始到学习者明确结束 Lesson 02。
- **Codex session**：`019fb5e8-54c6-77c0-8c7a-b489d135ee40`
- **包含起点**：用户消息“很好，让我们开始进入下一个阶段吧。”
- **包含终点**：用户消息“好的，结束lesson02吧……”；用显式时间上界截断，不包含结课归档过程。
- **消息范围**：2026-08-05 05:59:24–2026-08-06 07:27:16 UTC，共 153 条；包含 commentary。
- **哈希**：source snapshot
  `8b42d5f95de1c70db972683d7a4076aeea69cb8929a039987a8f2faaaf5d8ea3`；
  selected dialogue
  `9e42a5380a402e62c51473f53c673a1fdfe9ddc1a750a8de0cf9eee55d0d67fa`。
- **审核结果**：首尾边界正确，33 条用户消息与 120 条助手消息顺序合理；未包含 Lesson 02-A/B
  已归档片段、结课归档过程、system/developer/reasoning/tool 事件、凭据、私人 home 路径或附件内容。
- **导出命令**：

  ```bash
  uv run --frozen python skills/learn-by-practice/scripts/export_codex_dialogue.py export \
    <session-jsonl> \
    docs/triton-learning/dialogues/02-fused-softmax-part3.md \
    --title '第 02 课：Fused Softmax Persistent、资源与 Benchmark 实践原始对话' \
    --lesson 02-fused-softmax-part3 \
    --start-user '很好，让我们开始进入下一个阶段吧。' \
    --end-time '2026-08-06T07:27:17Z'
  ```

#### Lesson 02-D：结课后 Benchmark 解释补充

- **归档文件**：[02-fused-softmax-part4.md](../dialogues/02-fused-softmax-part4.md)
- **归档性质**：结课后补充；仅保存 stage 4 为何没有最优的性能答疑，不覆盖已冻结的 02-C。
- **Codex session**：`019fb5e8-54c6-77c0-8c7a-b489d135ee40`
- **包含起点**：用户消息“稍等一下，我们似乎遗漏了一点……”
- **排他终点**：用户消息“明白了。那么接下来请提交git……”
- **消息范围**：2026-08-06 08:11:15–08:15:20 UTC，共 6 条；包含 commentary。
- **哈希**：source snapshot
  `722acb122307d3dff53dd16bb02958d7cf9fbfe9aea71090ad9aa2344d32ca91`；
  selected dialogue
  `db081b58f0b1f1f5963cb8ae7c697f1d5261321e723d5880c24f313ad47ccb4e`。
- **审核结果**：首尾边界正确，1 条用户消息与 5 条助手消息顺序合理；未包含提交/归档元对话、
  system/developer/reasoning/tool 事件、凭据、私人 home 路径或附件内容。
- **导出命令**：

  ```bash
  uv run --frozen python skills/learn-by-practice/scripts/export_codex_dialogue.py export \
    <session-jsonl> \
    docs/triton-learning/dialogues/02-fused-softmax-part4.md \
    --title '第 02 课：Fused Softmax 结课后 Benchmark 解释原始对话' \
    --lesson 02-fused-softmax-part4 \
    --start-user '稍等一下，我们似乎遗漏了一点' \
    --end-before-user '明白了。那么接下来请提交git'
  ```

#### Lesson 02-E：Softmax 与 Log-softmax 快速回顾

- **归档文件**：[02-fused-softmax-part5.md](../dialogues/02-fused-softmax-part5.md)
- **归档性质**：结课后回顾的收尾快照；只保存 log-softmax 概念过课、学习者复述和
  明确结束边界，不覆盖已冻结的 02-C/02-D。
- **Codex session**：`019fb5e8-54c6-77c0-8c7a-b489d135ee40`
- **包含起点**：用户消息“我看到lesson02 softmax的实践任务中还有P03 row-wise
  log-softmax……”。
- **排他终点**：`2026-08-07T01:40:29Z`；包含学习者明确结束小课堂及随后的收尾过程更新。
- **消息范围**：2026-08-07 01:24:23–01:40:28 UTC，共 9 条；包含 commentary。
- **哈希**：source snapshot
  `eb6cbf82dcb41dd6c17bc0d1e816dc9416570f1fada0b67fcbb85149a023cd38`；
  selected dialogue
  `bb28d498cadd5f149743364b0d9cdcf17ac7f7f95518b93461e3bb8a23fbb6fd`。
- **审核结果**：首尾边界正确，3 条用户消息与 6 条助手消息顺序合理；未包含前一段容器
  配置工作、system/developer/reasoning/tool 事件、凭据、私人 home 路径或附件内容。
- **导出命令**：

  ```bash
  uv run --frozen python skills/learn-by-practice/scripts/export_codex_dialogue.py export \
    <session-jsonl> \
    docs/triton-learning/dialogues/02-fused-softmax-part5.md \
    --title '第 02 课：Fused Softmax 与 Log-softmax 快速回顾对话（收尾快照）' \
    --lesson 02-fused-softmax-part5 \
    --start-user '我看到lesson02 softmax的实践任务中还有P03 row-wise log-softmax' \
    --end-time '2026-08-07T01:40:29Z'
  ```

归档规则见 [`raw-dialogue-export.md`](../references/raw-dialogue-export.md)。

### 参考资料

- [本地官方 Fused Softmax 案例](../../triton-tutorials/official/02-fused-softmax.py)
- [本地教程来源记录](../../triton-tutorials/SOURCE.md)
- [Triton 官方 Fused Softmax 教程](https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html)
- [Triton reduction 操作](https://triton-lang.org/main/python-api/triton.language.html#reduction-ops)
- [Triton `range`](https://triton-lang.org/main/python-api/generated/triton.language.range.html)
- [Triton `num_programs`](https://triton-lang.org/main/python-api/generated/triton.language.num_programs.html)
- [CUDA Programming Guide：kernel occupancy 与 SM 资源](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)
- [CUDA Best Practices Guide：Occupancy](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy)
- [Nsight Compute：Occupancy 与 scheduler 状态](https://docs.nvidia.com/nsight-compute/2023.2/ProfilingGuide/index.html)
- [PyTorch softmax](https://pytorch.org/docs/stable/generated/torch.nn.functional.softmax.html)

## 13. 文档变更记录

| 日期 | 阶段 | 变更摘要 |
| --- | --- | --- |
| 2026-07-31 | 建档与完整讲解 | 创建 Lesson 02，记录官方源码、实测结果、边界与当前答疑 checkpoint |
| 2026-07-31 | Q01 答疑 | 解释 persistent 行分配、occupancy grid、软件流水时间线与 stages 资源取舍 |
| 2026-07-31 | Q01 复述与 Q02 | 校准 stages/occupancy 模型，对比静态 grid-stride 与动态队列 persistent |
| 2026-07-31 | Q02 确认 | 学习者正确说明动态调度对不均匀任务的负载均衡价值，Q02 关闭 |
| 2026-07-31 | P01 布置 | 建立三层实践阶梯，开放普通 grid fused softmax 与明确的接口/测试契约 |
| 2026-07-31 | Q03 答疑 | 区分正式 warp occupancy、源码 resident-program 计数和硬件实际利用率 |
| 2026-07-31 | Q03 确认 | 正确计算 62.5% occupancy，校准 warp residency 与执行单元利用率的区别 |
| 2026-07-31 | 阶段性暂停 | 保存 P01 前断点，导出并审核 29 条 Lesson 02-A 原始可见对话 |
| 2026-08-03 | 恢复课程 | 从 Lesson 02-A 暂停断点恢复，确认 P01 产物尚未创建并重新进入自主实践 |
| 2026-08-03 | P01 第一轮评审 | 现有 8 个 GPU 用例与静态检查通过；登记 P01-R01–R06，等待学习者修改 |
| 2026-08-03 | P01 契约澄清 | 明确 row-sum 检查对象是 kernel 输出 `actual`，将 P01-R03 标记为新澄清项 |
| 2026-08-03 | P01 第二轮评审 | GPU 5 上 13 个用例与 8-warps 元数据通过；关闭 5 项，保留/新增 P01-R05、R07、R08 |
| 2026-08-04 | P01 最终复审 | GPU 3、静态检查和 metadata 全部通过；关闭 P01-R05、R07、R08，P01 完成 |
| 2026-08-04 | 阶段性暂停 | 保存 P01 完成后断点；导出并审核 32 条 Lesson 02-B 原始可见对话 |
| 2026-08-05 | 恢复并开放 P02 | 建立 persistent/stages 详细契约，等待四项实践前预测与自主实现 |
| 2026-08-05 | P02 预测复核 | 行映射与资源趋势正确；校准唯一覆盖、program 内流水和低 occupancy 性能取舍 |
| 2026-08-05 | P02 预测二次复述 | 关闭 PRED-01–03；PRED-04 仅剩数据并行/指令级并行术语与证据校准 |
| 2026-08-05 | P02-Q04 资源答疑 | 区分 compiled resource 报告、理论 occupancy 推导和 Nsight achieved occupancy |
| 2026-08-05 | P02 预测验收 | stages 4 六项资源/occupancy/grid 复算全对；关闭 PRED-04/Q04，进入自主实现 |
| 2026-08-05 | P02-A 第一轮评审 | GPU 25 passed；登记 stage metadata 新澄清项与 4 项静态/接口问题 |
| 2026-08-05 | P02-A 第二轮复审 | GPU、静态检查和 stage metadata 全绿；关闭 R01–R04，R05 测试语义待收紧 |
| 2026-08-05 | P02-A 最终复审 | R05 语义测试通过；关闭 P02A-R01–R05，P02-A 完成并解锁 P02-B |
| 2026-08-05 | P02-B 第一轮评审 | grid 公式方向正确，但默认路径 KeyError；登记资源来源、shared=0、校验与测试问题 |
| 2026-08-05 | P02-B 第二轮复审 | 默认 stages 1/2/4 数值正确并关闭 R02；保留 warps 复用、空 batch、零 resident、测试与静态检查问题 |
| 2026-08-05 | P02-B 第三轮复审 | 30 个 GPU 用例和资源诊断通过并关闭 R01；R03–R06 等待边界测试、资源可观察性与静态清理 |
| 2026-08-05 | P02-B AI-owned 测试补充 | 新增 6 个 CPU grid cases 和 4 个 GPU cases；关闭 R03–R04，学习者仅余 helper 文档/类型/格式清理 |
| 2026-08-06 | P02-B 第四轮复审 | AI 修正测试的旧字典假设后 CPU/GPU/静态全绿；关闭 R06，R05 仅余私有 API 兼容性说明 |
| 2026-08-06 | P02-Q05 设计答疑 | 给出私有 Triton API docstring 边界，并说明 frozen/slotted dataclass 对 Pydantic 的轻量替换 |
| 2026-08-06 | P02-B 第五轮复审 | 关闭 R05/R07；CPU/GPU/类型/锁文件通过，新登记 R08 单文件格式化项 |
| 2026-08-06 | P02-B 最终复审 | format 与完整静态检查全绿，关闭 R08 和 P02-B；解锁 AI-tests-first 的 P02-C benchmark |
| 2026-08-06 | P02-C tests-first 交接 | AI 新增 16 个显式 GPU benchmark cases；确认仅因目标模块缺失而预期 red，移交学习者实现 |
| 2026-08-06 | P02-C 契约修订 | 按学习者设计保留 tuple grid，采用四种 provider；验收扩为 20 cases，第一版得到 17 passed、3 failed |
| 2026-08-06 | P02-Q07 绘图答疑 | 验证用 tuple 复合 `line_arg` 配置，并用 shape index/自定义刻度避免相同 M 的横坐标重叠 |
| 2026-08-06 | P02-C 第一轮评审 | BasedPyright 实际全绿；确认 wrapper 污染 persistent 计时，补强 agent tests 并登记 R01–R07 |
| 2026-08-06 | P02-Q08 计时答疑 | 区分 compiled `.warmup()` 与 `do_bench` warm-up；确认每个 case 预备一次 resources/grid、计时只直接 launch |
| 2026-08-06 | P02-Q09 wrapper 边界 | 明确预传 `grid[0]` 仅跳过资源探测，wrapper 仍分配 output；稳态实验必须 direct kernel launch |
| 2026-08-06 | P02-Q10 实验边界复议 | 接受学习者的端到端场景理由；改为四种 provider 均调用公开 wrapper/function，保留每次检查/分配，仅摊销 persistent grid setup |
| 2026-08-06 | P02-Q11 实验记录 | 给出 resources.csv/environment.json 采集方案；实测 stages 1/2/4 的 compiled resources 和 A100 软件环境 |
| 2026-08-06 | P02-Q12 方案简化 | 接受学习者对过度设计的反馈；直接在 persistent 分支复用 `derive_resource_record`，资源三行与环境一行打印即可 |
| 2026-08-06 | P02-C 第二轮复审 | 关闭 timing/occupancy/静态项；AI 验收增至 27 cases，定位前置校验、exact specialization、correctness/sync 和重复运行清理，当前 18 passed/9 failed |
| 2026-08-06 | P02-Q13 绘图标签 | 说明 perf-report 使用首个 x 值绘图，采用 run 后设置 shape ticks 并覆盖 PNG；后续把 AI 示例的 `×` 更正为 Ruff 兼容的 ASCII `x` |
| 2026-08-06 | P02-C 第三轮复审 | 验证 resource/grid/records/shape labels，修正 agent plot fixture并将 correctness 验收扩到四类 provider；当前 25 passed/5 failed |
| 2026-08-06 | P02-Q14 correctness 职责修订 | 接受 benchmark 不做正确性断言；移除 4 项 harness 时序测试，新增三个 exact-shape 独立功能用例，benchmark 27/27、GPU 功能 37/37 |
| 2026-08-06 | P02-C 最终实验 | 修正 ASCII shape label；最终资源/18 行性能/PNG 重跑，Ruff/format/BasedPyright 与全部测试通过 |
| 2026-08-06 | Lesson 02 完成 | 完成概念、实践、性能复盘与 153 条结课段对话归档；P03 从本课取消，无开放 finding |
| 2026-08-06 | 学习流程精简 | 后续 benchmark 测试聚焦性能影响因素和测量有效性，不设置参数校验测试；减少非核心学习消耗 |
| 2026-08-06 | P02-Q15 结课后答疑 | 解释 stage 4 未最优；补充 N=2049 资源/grid，区分默认策略比较与固定-grid 因果比较；另存 6 条 02-D 对话归档 |
| 2026-08-07 | P03-Q16 概念过课与确认 | 对比 stable softmax/log-softmax 公式、kernel 数据流、padding、不变量、编译资源和训练边界；学习者正确复述共用框架与差异边界，不恢复编码实践 |
| 2026-08-07 | P03 快速回顾收尾 | 保持 Lesson 02 已完成和 P03 编码实践取消；写入恢复检查点，导出并审核 9 条 02-E 收尾快照 |
