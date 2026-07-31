# 第 02 课：Fused Softmax

## 1. 课程档案

| 字段 | 内容 |
| --- | --- |
| 课程编号 | `02` |
| 官方案例 | [`02-fused-softmax.py`](../../triton-tutorials/official/02-fused-softmax.py) |
| 教程快照 | Triton `main` 文档，下载于 2026-07-15 UTC |
| 学习状态 | 实践中 |
| 开始日期 | 2026-07-31 |
| 完成日期 | — |
| 实践源码 | `gpu/triton/lesson02_fused_softmax.py`（待创建） |
| 测试代码 | `gpu/triton/lesson02_fused_softmax_test.py`（待创建，需要 GPU） |
| 原始对话 | [02-fused-softmax.md](../dialogues/02-fused-softmax.md)（29 条消息，暂停快照） |
| 补充材料 | 无 |

### 环境基线

| 项目 | 版本或型号 |
| --- | --- |
| GPU | NVIDIA A100-SXM4-80GB；系统共 8 张，本次运行限制到第 0 张 |
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
- [ ] 已提交第一版实现
- [ ] 已完成至少一轮代码评审
- [ ] 已处理全部阻塞问题
- [ ] 已通过正确性与边界测试
- [ ] 已完成知识复述与变式验收
- [ ] 已总结并关闭本课
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
| P01 | 普通 grid 的 fused softmax | reduction、padding、接口和边界测试 | **已开放** |
| P02 | Persistent softmax 与 stages 实验 | 行分配、occupancy、资源和计时证据 | 待 P01 评审通过 |
| P03 | Row-wise log-softmax 迁移 | 不照搬原式完成相关 reduction 算子 | 待 P02 评审通过 |

核心 kernel、wrapper 和测试均由学习者实现。可以请求分级提示或共同定位失败，但提示默认先解释
概念和失败证据，不直接给出完整实现。

### 通用验收要求

- 实现放在 `gpu/triton/`；GPU 测试与实现同目录，保持在默认 CPU-only pytest/CI 范围之外。
- 使用 `@triton.jit` 完成核心计算，不在 wrapper 中调用 `torch.softmax` 代替待实现算子。
- 先验证正确性、数学不变量和错误输入，再做 persistent 转换或性能测量。
- 使用 `torch.testing.assert_close` 对照 PyTorch reference；性能不能代替正确性证据。
- 注释解释设计理由，不逐行翻译代码，也不逐行复制官方实现。

### P01：普通 grid 的 row-wise fused softmax（当前任务）

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
- 每一行的和接近 1；
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

### P02：Persistent softmax 与 `num_stages`（待开放）

P01 通过后，将普通 grid 版本改造成有限 resident programs 循环覆盖全部行的版本。届时需要：

- 使用 `tl.num_programs(0)` 和带 `num_stages` 的 `tl.range`；
- 证明 `M` 不能整除 program 数时每行仍恰好处理一次；
- 对 `num_stages=1/2/4` 记录 compiled registers、shared memory、推导 occupancy 和稳态耗时；
- 先写资源与性能预测，再根据实测解释 latency hiding 与 occupancy 的取舍；
- 不设置“某个 stages 必须最快”的硬编码性能断言。

详细接口、资源读取兼容层和实验矩阵在 P01 评审后开放，避免现在预先解决核心实践。

### P03：Row-wise log-softmax 迁移（待开放）

在不调用 `torch.log_softmax` 代替 kernel 的前提下，把已掌握的 max/sum reduction 迁移到
row-wise log-softmax，并用与原例不同的数学形式、边界测试和 PyTorch reference 验证。详细契约
将在 P02 完成后根据届时暴露的薄弱点确定。

## 8. 实现与实验记录

### 实现文件

| 用途 | 路径 | 说明 |
| --- | --- | --- |
| Kernel / wrapper | `gpu/triton/lesson02_fused_softmax.py` | 待创建 |
| Tests | `gpu/triton/lesson02_fused_softmax_test.py` | 待创建；需要 GPU，保持显式运行 |
| Benchmark | 待定 | 正确性和接口评审通过后再决定 |

### 第一版设计

- 工作划分：P01 契约为一行一个 program；待学习者填写实际实现。
- grid 与 block/tile：P01 契约为 `(M,)` 与 `next_power_of_2(N)`；待学习者解释映射。
- mask 策略：P01 要求 masked load 使用 `-inf`、store 只覆盖有效列；待实现验证。
- dtype/shape/stride 支持：P01 限定二维 CUDA contiguous float32；待 wrapper 与测试验证。
- 主动取舍：待学习者填写。

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

### 正确性用例

P01 最低矩阵已在实践契约中定义，尚未建立学习者测试或结果记录。

### 性能实验

目前只有官方脚本的一次探索性运行；完整结果未保存为课程 benchmark 产物，不构成后续实现的
性能验收。

### 失败尝试与定位过程

无。

## 9. 代码评审与修改闭环

尚无学习者实现，未进入评审。

## 10. 掌握验收

### 概念验收

将在实践和答疑后进行：

1. 用自己的话描述 persistent program、row block 和元素之间的映射。
2. 从 `M`、`N` 和资源占用推导 grid，并解释不能整除时的行覆盖。
3. 解释 `BLOCK_SIZE`、`num_stages` 和 `num_warps` 的确定时机与作用。
4. 解释 padding、两次 reduction 和主要访存模式。
5. 说明 shape、dtype 或 stride 改变时哪些部分必须调整。

### 实践验收

- [ ] 官方示例的核心版本可以独立重写，而不是逐行照抄
- [ ] 非 2 的幂列宽正确
- [ ] reference、数学不变量与断言完整
- [ ] 错误输入行为明确
- [ ] 代码通过项目格式和相关静态检查
- [ ] 性能结论有可复现实验支持，或明确说明本课不要求性能验收
- [ ] 至少完成一个与原例不同的变式

### 最终遗留问题

- 尚未进入验收。

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

- [ ] 所有阻塞评审意见均已关闭
- [ ] 概念和实践验收均已通过
- [ ] 文档中的问题、实验和最终实现已同步
- [ ] 学习者确认可以进入下一课

## 12. 原始对话与参考资料

### 原始对话归档

- **归档文件**：[02-fused-softmax.md](../dialogues/02-fused-softmax.md)
- **归档性质**：Lesson 02-A 暂停快照；课程恢复后的新片段应另行后验导出并按顺序链接。
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
