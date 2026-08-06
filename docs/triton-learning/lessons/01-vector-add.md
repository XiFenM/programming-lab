# 第 01 课：Vector Addition

## 1. 课程档案

| 字段 | 内容 |
| --- | --- |
| 课程编号 | `01` |
| 官方案例 | [`01-vector-add.py`](../../triton-tutorials/official/01-vector-add.py) |
| 教程快照 | Triton `main` 文档，下载于 2026-07-15 UTC |
| 学习状态 | 已完成 |
| 开始日期 | 2026-07-20 |
| 完成日期 | 2026-07-22 |
| 可选性能扩展完成日期 | 2026-07-27 |
| 仓库已有参考 | [`gpu/triton/vector_add.py`](../../../gpu/triton/vector_add.py) |
| 学习者实践源码 | [`lesson01_vector_ops.py`](../../../gpu/triton/lesson01_vector_ops.py) |
| 测试代码 | [`lesson01_vector_ops_test.py`](../../../gpu/triton/lesson01_vector_ops_test.py) |
| 原始对话 | [第一段](../dialogues/01-vector-add.md)（57 条）；[第二段](../dialogues/01-vector-add-part2.md)（37 条）；[第三段](../dialogues/01-vector-add-part3.md)（87 条）；[第四段](../dialogues/01-vector-add-part4.md)（18 条） |
| 补充材料 | [pytest GPU 测试参考](../references/pytest-gpu-kernel-tests.md)；[AXPBY Benchmark 简报](../attachments/01-vector-add/axpby-benchmark.md) |

### 环境基线

| 项目 | 版本或型号 |
| --- | --- |
| GPU | 8 × NVIDIA A100-SXM4-80GB（2026-07-22 实测） |
| NVIDIA driver | 580.159.03（2026-07-22 实测） |
| CUDA Toolkit (`nvcc`) | 13.0，build 13.0.88 |
| Python | 3.12.13 |
| PyTorch | 2.13.0，CUDA runtime 13.0 |
| Triton | 3.7.1 |

版本信息只说明当前项目环境。官方教程来自持续更新的 `main` 文档，实际实验结果必须补充 GPU
型号、driver 和运行日期，不能直接把官方页面上的性能数字当成本机基线。

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
- [x] 已在阶段性中断时后验导出原始对话

## 2. 学习目标与前置知识

### 本课目标

完成本课后，应该能够：

1. 区分 Triton 的 program instance、块级 tensor 运算和 CUDA 标量线程心智模型。
2. 从一维问题规模推导 launch grid，并为每个 program 构造一块连续索引。
3. 使用 mask 安全处理不能被块大小整除的尾部元素。
4. 解释运行时参数和 `tl.constexpr` meta-parameter 的区别。
5. 用 Python wrapper 分配输出、启动 kernel，并理解 GPU 异步执行。
6. 使用可靠的 reference、边界用例和 benchmark 方法验证自定义算子。

### 前置知识检查

| 知识点 | 本课所需程度 | 说明 |
| --- | --- | --- |
| Python 与 PyTorch tensor | 基础 | 能理解 shape、dtype、device、`numel()` 和 `empty_like()` |
| 整数向上取整除法 | 基础 | 理解 `ceil(n / block_size)` 为什么覆盖全部元素 |
| GPU 异步执行 | 入门 | 理解 launch 返回不代表 GPU 已经完成 |
| CUDA grid/block/thread | 可选 | 有助于对比，但不能机械等同于 Triton 的块级 program |
| 内存带宽 | 入门 | 理解向量加法为什么通常受访存而非算力限制 |

### 课前预测

以下内容留给学习者在答疑时补充，不能由讲解者代写：

- 我认为这个案例要解决的问题是：待补充。
- 我预计一个 Triton program 会负责：待补充。
- 我最不确定的是：待补充。

## 3. 官方案例地图

### 文件组成与执行入口

| 源码位置 | 作用 |
| --- | --- |
| 21–26 行 | 导入 PyTorch/Triton，并取得当前 Triton backend 对应的 Torch device |
| 29–54 行 | 定义 JIT 编译的 `add_kernel` |
| 62–78 行 | 定义 Python wrapper `add`，负责输出分配、grid 计算和 kernel launch |
| 84–93 行 | 构造输入，与 `x + y` 对照并打印最大误差 |
| 107–129 行 | 定义跨输入规模、跨 provider 的 benchmark |
| 135 行 | 运行 benchmark、打印数据并显示图表 |

`DEVICE = triton.runtime.driver.active.get_active_torch_device()` 不把设备硬编码成 `"cuda"`，而是
查询当前 Triton backend 对应的 Torch device；在本仓库的 NVIDIA 环境中通常就是 CUDA device。
这也意味着文件在 import 阶段便需要可用的 Triton driver。

该文件是 Sphinx-Gallery 教程脚本，不是纯库模块：导入到 84 行后会立即创建 GPU tensor，导入到
135 行还会立即运行完整 benchmark。自己的可复用模块通常应把演示入口放进
`if __name__ == "__main__":`。

### 输入、输出与约束

| 项目 | shape | dtype | device | 布局/stride | 教程实际假设 |
| --- | --- | --- | --- | --- | --- |
| `x` | 一维 `N` | 示例为 float32 | `DEVICE` | 连续 | 至少有 `N` 个可线性访问元素 |
| `y` | 一维 `N` | 示例为 float32 | `DEVICE` | 连续 | 与 `x` 的元素数、语义和 dtype 兼容 |
| `output` | 与 `x` 相同 | 与 `x` 相同 | `DEVICE` | 示例中连续 | 每个有效位置只写一次 |

教程 wrapper 只断言 device，没有检查 shape、dtype、contiguity 或空 tensor。这是为了突出第一课
的 kernel 模型，不代表生产接口已经健壮。

### 高层执行流程

```text
x, y（PyTorch GPU tensors）
  -> output = torch.empty_like(x)
  -> N = output.numel()
  -> grid = (ceil(N / BLOCK_SIZE),)
  -> 并行启动 grid[0] 个 add_kernel program instances
       -> 每个 instance 生成 BLOCK_SIZE 个逻辑索引
       -> mask 掉 >= N 的索引
       -> load x/y，逐元素相加，store output
  -> 返回 output（此时通常仍只是已入队，不意味着 CPU 已同步等待）
```

## 4. 详细讲解

### 4.1 问题背景与 PyTorch baseline

目标算子是最简单的逐元素加法：

```text
output[i] = x[i] + y[i],  i = 0, 1, ..., N - 1
```

PyTorch baseline 是 `x + y`。它已经会启动一个优化过的 GPU kernel，因此本课不是要证明 Triton
一定比 PyTorch 快，而是借一个没有复杂数学干扰的算子学习 Triton 的基本执行模型、JIT、边界
处理、正确性验证和性能测量。

向量加法对每个 float32 元素大致读取 `x` 的 4 字节、读取 `y` 的 4 字节、写出 4 字节，只做
一次加法，即约 `1 FLOP / 12 bytes`。其计算强度很低，输入足够大时通常是内存带宽受限，而不是
浮点计算单元受限。

### 4.2 Triton 编程模型映射

最重要的区别是：Triton 源码中的一次 kernel program 不是只描述一个标量元素。

| 层次 | 本案例中的含义 |
| --- | --- |
| 整个问题 | 对 `N` 个元素执行逐元素加法 |
| launch grid | 一维，共 `ceil(N / BLOCK_SIZE)` 个 program instances |
| 一个 program instance | 负责一段最多含 `BLOCK_SIZE` 个元素的连续区间 |
| program 内的块级 tensor | `offsets`、`mask`、`x`、`y`、`output`，形状均为 `[BLOCK_SIZE]` |
| 实际 GPU threads/warps | 由 Triton 编译器和 launch 配置映射，不由源码逐元素显式书写 |

因此，`BLOCK_SIZE=1024` 表示一个 program 逻辑上处理 1024 个数据元素，**不表示创建 1024 个
CUDA threads**。一个 Triton program 常对应一次块级执行，但实际线程/warp 数量和数据映射由
编译器及 `num_warps` 等 launch meta-parameter 决定。

以 `N=10`、`BLOCK_SIZE=4` 为简化示意：

```text
grid = (ceil(10 / 4),) = (3,)

pid=0: offsets=[0, 1, 2, 3]     mask=[T, T, T, T]
pid=1: offsets=[4, 5, 6, 7]     mask=[T, T, T, T]
pid=2: offsets=[8, 9, 10, 11]   mask=[T, T, F, F]
```

本记录后文用 “lane” 简称块级 tensor 中的一个元素位置；它是逻辑位置，不应直接等同于某个
硬件 warp lane，实际映射仍由编译器决定。

三个 program 的有效写入区间互不重叠，所以不需要原子操作，也没有跨 program 同步。

### 4.3 Kernel 签名与参数分类

```python
@triton.jit
def add_kernel(x_ptr, y_ptr, output_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    ...
```

`@triton.jit` 表示函数由 Triton 编译器 JIT 编译并在 GPU 上运行。它不是普通 Python 函数，
函数体只能使用 Triton 支持的 Python 原语、Triton builtins、参数和其他 JIT 函数。首次遇到新的
相关参数组合时会产生编译开销，后续可命中缓存。

| 参数 | 类型/角色 | 何时确定 | 用途 |
| --- | --- | --- | --- |
| `x_ptr` | 输入首元素指针 | launch 时 | 读取第一个向量 |
| `y_ptr` | 输入首元素指针 | launch 时 | 读取第二个向量 |
| `output_ptr` | 输出首元素指针 | launch 时 | 写回结果 |
| `n_elements` | 运行时标量 | launch 时 | 判断哪些逻辑索引有效 |
| `BLOCK_SIZE` | `tl.constexpr` meta-parameter | 编译/特化时 | 决定每个 program 的静态块形状 |

Torch tensor 传给 JIT kernel 时，会利用其 `data_ptr()` 和 dtype 信息隐式转换成带元素类型的
指针。指针加上整数 offset 按“元素”移动，底层字节地址缩放由指针元素类型决定。

`BLOCK_SIZE` 必须是编译期可见值，因为 `tl.arange(0, BLOCK_SIZE)` 的结果形状需要静态确定，
编译器也依赖这个块形状做线程映射、向量化和访存分析。不同块大小通常会对应不同的 JIT
特化版本；它不是普通的动态循环上限。当前 API 下 `tl.arange` 使用编译期静态边界，块大小
通常取 2 的幂；教程选择的 1024 正符合这一约束和常见优化习惯。

### 4.4 Kernel 逐段解析

#### Program ID 与块起点

```python
pid = tl.program_id(axis=0)
block_start = pid * BLOCK_SIZE
```

grid 是一维的，所以使用 axis 0。`pid` 的取值范围是 `0` 到 `grid[0] - 1`。乘以块大小后，
得到当前 program 所负责区间的第一个逻辑元素位置。

#### 块级索引生成

```python
offsets = block_start + tl.arange(0, BLOCK_SIZE)
```

`tl.arange(0, BLOCK_SIZE)` 产生 `[0, 1, ..., BLOCK_SIZE-1]` 这一块整数 tensor。标量
`block_start` 广播后与其相加，得到当前 program 的全局逻辑索引。

官方源码注释称 offsets 是 “a list of pointers”。更准确地说，`offsets` 此时是整数 offset
tensor；只有执行 `x_ptr + offsets` 后，结果才是“一块指针”。它也不是 Python `list`。

#### Mask 与边界处理

```python
mask = offsets < n_elements
```

向上取整得到的最后一个 program 可能覆盖到 `N` 之外。`mask` 是与 offsets 同形状的布尔
tensor，有效位置为 true，越界位置为 false。它表达的是逐 lane 的 predication，而不是让整个
program 因某一个越界元素而退出。

#### Load、计算与 store

```python
x = tl.load(x_ptr + offsets, mask=mask)
y = tl.load(y_ptr + offsets, mask=mask)
output = x + y
tl.store(output_ptr + offsets, output, mask=mask)
```

- `x_ptr + offsets` 和 `y_ptr + offsets` 是形状 `[BLOCK_SIZE]` 的指针 tensor。
- `tl.load` 只对 mask 为 true 的 lane 执行有效读取。
- 没有提供 `other=` 时，masked-out lane 的载入结果不应被视为有定义值。
- 本例是逐元素独立计算，并且 store 使用同一个 mask，所以无效 lane 的值不会影响任何有效
  输出。
- `tl.store` 对 mask 为 false 的 lane 不做写入，从而避免越界。

如果后续案例要把所有 lane 参与 reduction，masked-out lane 就可能影响有效结果，此时往往要在
load 中用合适的 `other` 填充，例如求和填 0、求最大值填负无穷。第一课不需要 reduction。

### 4.5 Python wrapper 与 launch grid

```python
output = torch.empty_like(x)
n_elements = output.numel()
grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']),)
add_kernel[grid](x, y, output, n_elements, BLOCK_SIZE=1024)
```

wrapper 承担 kernel 外部的控制工作：

1. `empty_like` 只分配输出，不初始化；kernel 必须覆盖全部有效元素。
2. `numel()` 把问题规模表示成元素总数。
3. `triton.cdiv(a, b)` 是整数向上取整除法。
4. grid lambda 会接收 launch meta-parameters，因此可以读取关键字传入的 `BLOCK_SIZE`。
5. `(value,)` 中的逗号不可省略；它表示一维 grid tuple，而不是带括号的整数。
6. `add_kernel[grid](...)` 是 Triton 的 kernel launch 语法。
7. `BLOCK_SIZE=1024` 必须以 meta-parameter 关键字传入。

官方测试的 `N=98,432`：

```text
98,432 = 96 * 1,024 + 128
grid[0] = 97
```

前 96 个 program 各处理 1024 个有效元素；最后一个 program 只有前 128 个 lane 有效，其余 896
个 lane 被 mask。这一尺寸实际上特意覆盖了尾块路径。

grid 也可以直接写成 tuple：

```python
grid = (triton.cdiv(n_elements, 1024),)
```

教程使用 callable grid，是为了展示 grid 可以依赖 meta-parameters；后续做 autotune 时，同一个
kernel 的候选配置可能使用不同块大小，callable 形式更自然。

#### 异步执行

kernel launch 通常只是把工作排入当前 GPU stream。`add` 返回 output 时，GPU 不一定已经完成
计算，但同一 stream 上后续依赖该 tensor 的 GPU 操作会保持顺序。若 CPU 必须确认工作已经
结束，或者自行计时，就需要显式同步或使用能够正确处理 GPU 异步语义的计时工具。

### 4.6 内存访问、数据布局与并行性

每个 program 访问连续的 offsets，相邻 lane 访问相邻元素。这为编译器生成合并访存提供了清晰
信息。不同 program 负责互不重叠的连续区间，理论内存流量为：

```text
读取 x：N * element_size
读取 y：N * element_size
写出 z：N * element_size
合计：  3 * N * element_size
```

这里使用的是裸指针加线性 offset，不会自动遵循 PyTorch tensor 的任意 stride。因此教程实际
依赖连续布局。对非连续 tensor，`numel()` 虽然仍正确，但线性读取底层 storage 不一定等价于
PyTorch 的逻辑元素顺序；后续实践必须选择“先 `.contiguous()`”或“显式传 stride”之一。

### 4.7 正确性验证

教程执行：

```python
output_torch = x + y
output_triton = add(x, y)
max_diff = torch.max(torch.abs(output_torch - output_triton))
```

优点：

- 固定随机种子，方便复现输入。
- 使用不能被 1024 整除的尺寸，覆盖尾部 mask。
- 与成熟的 PyTorch 实现作 reference。

不足：

- 只打印最大误差，没有 assertion；即使结果错误，脚本仍可能继续 benchmark。
- 只有一个大尺寸和默认 float32，没有覆盖很小尺寸、恰好整除、空 tensor 或其他 dtype。
- wrapper 没有验证 shape、dtype 和 contiguity。

正式练习会使用 `torch.testing.assert_close`，并至少覆盖 `N < BLOCK_SIZE`、恰好整除和带尾块三
类尺寸。对于浮点加法，本例常得到 0 最大误差，但不能把“所有 GPU 浮点算子都应逐 bit 相同”
当作普遍结论。

### 4.8 Benchmark 与性能解释

`triton.testing.perf_report` 和 `Benchmark` 描述实验矩阵：

- 横轴参数是 `size`，范围从 `2**12` 到 `2**27`，使用对数刻度。
- `provider` 分成 Triton 和 Torch 两条曲线。
- 每个 `(size, provider)` 调用一次 `benchmark` 函数。
- 输入分配发生在 `do_bench` 外部；被计时 lambda 只执行算子。
- Triton 的 `add` 和 Torch 的 `x + y` 调用路径都会分配输出 tensor，比较口径大致一致；但
  `do_bench` 使用 GPU event，主要测量 stream 上的设备执行时间，并不等同于包含全部 Python
  wrapper 与 host allocator 开销的 CPU wall-clock 延迟。

这套 API 分成两层：

1. `do_bench(fn, ...)` 负责一次配置的预热、重复、GPU 计时和统计汇总。
2. `Benchmark` 声明横轴、对比曲线和固定参数，`perf_report` 把普通函数包装成带 `.run()` 的
   实验对象，负责遍历配置、打印表格和绘图；它本身不是计时器。

```python
quantiles = [0.5, 0.2, 0.8]
ms, min_ms, max_ms = do_bench(..., quantiles=quantiles)
```

返回值按请求顺序分别是 50%、20%、80% 分位耗时。变量名 `min_ms`/`max_ms` 是教程中的简化
叫法，并非样本的绝对最小/最大值。吞吐量与耗时成反比，因此返回给绘图器的是：

```python
gbps(ms), gbps(max_ms), gbps(min_ms)
```

即中心值、较低吞吐边界、较高吞吐边界。

有效带宽公式为：

```text
GB/s = 3 * N * element_size * 1e-9 / (milliseconds * 1e-3)
```

系数 3 对应两次读和一次写。这是基于算法最低数据流量计算的“有效带宽”，不是硬件计数器测得
的精确 DRAM 流量；缓存、写策略和其他内部流量没有计入。

在当前 Triton 3.7.1 环境中，`do_bench` 的主要流程是：

1. 先执行并同步一次 `fn()`；这会触发新配置所需的首次 JIT 编译，但不进入最终样本。
2. 再执行 5 次估算平均单次耗时。
3. 根据估算值把默认 `warmup=25` 和 `rep=100` 两段目标时长换算成预热次数与采样次数；二者
   单位均为毫秒，并不是“预热 25 次、测量 100 次”。
4. 每个正式样本使用同一设备上的 GPU event 包住 `fn()`，最后统一同步并计算 event elapsed
   time；当前实现还会在每个正式样本前清理 L2 cache。
5. 如果传入 `quantiles`，便按给定顺序返回耗时分位数；否则由 `return_mode` 选择
   mean、median、min、max 或全部样本。

因此它能正确处理 GPU launch 的异步语义，也会把首次 JIT 排除在稳态样本之外。不过这个流程是
对本仓库当前版本源码的观察；升级 Triton 后应重新核对，而不能把实现细节当成永久 API 保证。

最大的 `2**27` 个 float32 元素，每个 tensor 为 512 MiB，三个 tensor 合计约 1.5 GiB，因此
运行完整 benchmark 前还要考虑实际显存。无图形界面的环境可先使用
`show_plots=False, print_data=True`。

解释曲线时应区分两个典型区间：小输入通常被 kernel launch、固定指令和统计噪声主导，有效
GB/s 偏低；输入增大后才可能进入内存带宽平台区。块大小会同时改变 program 数量、每个 program
的逻辑工作量以及编译器的资源映射，所以不能从“块更大”直接推出“性能更快”。

### 4.9 容易误解或踩坑的地方

1. `BLOCK_SIZE` 是逻辑数据块大小，不是 CUDA thread 数量。
2. `offsets` 是整数 tensor；`pointer + offsets` 才是指针 tensor。
3. grid 表示 program instance 数量，不是总元素数。
4. `tl.arange` 构造的是编译期静态形状的块级 tensor，不是 Python range 循环；块大小通常应
   选 2 的幂。
5. 最后一个 program 仍然启动；mask 只关闭其中无效 lane 的内存操作。
6. masked load 没有 `other` 时，无效 lane 的值不能参与会影响有效输出的 reduction。
7. 裸指针线性寻址不自动尊重任意 PyTorch stride。
8. 返回 output 不代表 GPU 已同步完成，但同一 stream 上的依赖仍保持正确顺序。
9. 第一次调用可能包含 JIT 编译，不能拿来代表稳态 kernel 性能。
10. 教程脚本在模块顶层运行测试和 benchmark，直接 import 也会触发这些工作。

## 5. 我的理解与知识复述

本节由学习者在答疑过程中用自己的话补充。

### 当前心智模型

一个 Triton launch 先通过 grid 创建多个 program instances；每个 program 用自己的
`program_id` 定位数据块，再由 `tl.arange` 创建固定形状的 block tensor。`tl.load/store` 对
pointer tensor 逐 lane 执行带 mask 的内存操作，编译器再把这些逻辑操作映射到实际 GPU
threads/warps。`BLOCK_SIZE` 是逻辑数据块大小而不是 CUDA thread 数；mask 是 predication 而
不是 compaction。

### 我可以独立解释的问题

- [x] 为什么 grid 是 `ceil(N / BLOCK_SIZE)`？
- [x] 一个 program instance 处理哪些数据？
- [x] 为什么最后一个 program 需要 mask？
- [x] `BLOCK_SIZE` 为什么是 `tl.constexpr`？
- [x] `BLOCK_SIZE=1024` 为什么不等于 1024 个 CUDA threads？
- [x] `x_ptr + offsets` 的含义是什么？
- [x] 为什么这个算子通常受内存带宽限制？
- [x] 为什么普通 CPU 计时可能错误衡量异步 GPU kernel？

### 尚不牢固的概念

- Q01–Q04 已由学习者口头确认解决；Q05–Q09 已通过后续测试实现与复审验证。

## 6. 问题与答疑记录

### Q01：Masked load 的无效位置为什么仍会影响 reduction？

- **日期**：2026-07-20
- **我的原始问题**：`tl.load` 已经使用 mask 时，无效位置为什么还能影响 sum/max？mask 为
  false 的位置是消失，还是作为未定义值保留在固定形状的数据块中？例如 `N=10`、
  `BLOCK_SIZE=4` 时，最后一块是 `[9, 10, 未定义, 未定义]` 还是 `[9, 10]`？
- **提问时的理解/假设**：mask 可能只禁止越界读取，但不会缩短 `tl.load` 返回的块级 tensor；
  最后一块仍有 4 个逻辑位置。
- **讲解与回答**：这个假设正确。mask 控制逐位置的内存访问，不执行筛选或压缩。
  `tl.load` 的结果保持 `[BLOCK_SIZE]` 静态形状；mask 为 false 且没有指定 `other` 的位置返回值
  未定义。elementwise 计算配合同一个 masked store 时，无效位置不会流入有效输出；reduction
  会把整个固定形状数据块折叠，因此无效位置也属于 reduction 的输入，未定义值可能污染结果。
- **最小例子或推导**：最后一个 program 的 `offsets=[8, 9, 10, 11]`、
  `mask=[T, T, F, F]`。`tl.load(..., mask=mask)` 的抽象结果为 `[9, 10, ?, ?]`；使用
  `other=0` 后为 `[9, 10, 0, 0]`，适合求和；使用 `other=-inf` 后为
  `[9, 10, -inf, -inf]`，适合求最大值。
- **最终结论**：mask 是 predication，不是 compaction。需要跨位置组合数据时，应给无效位置
  填入该运算的单位元：sum 用 0、product 用 1、max 用负无穷、min 用正无穷。
- **是否解决**：是，学习者已确认。
- **衍生问题**：暂无。

### Q02：`tl.store` 中的 mask 是否也保留固定形状？

- **日期**：2026-07-20
- **我的原始问题**：`tl.store` 中的 mask 是否和 masked load 类似？
- **提问时的理解/假设**：store mask 可能也只控制每个逻辑位置是否写入，而不会压缩或重排
  `value`。
- **讲解与回答**：这个假设正确。pointer、value 和 mask 仍按相同的静态块形状逐位置对应；
  mask 为 true 的位置执行写入，false 的位置完全不执行写入。`tl.store` 不返回数据，因此没有
  masked load 中“false 位置返回未定义值还是 other”的问题。若 false 位置对应一个有效地址，
  该地址原有内容保持不变；若它是越界地址，则不会访问该地址。
- **最小例子或推导**：`offsets=[8, 9, 10, 11]`、`value=[9, 10, ?, ?]`、
  `mask=[T, T, F, F]` 时，只执行 `ptr[8]=9` 和 `ptr[9]=10`。不会把 value 压缩成
  `[9, 10]`，也不会向 `ptr[10]`、`ptr[11]` 写 0 或未定义值。
- **最终结论**：load mask 决定“是否读取，以及 false 位置返回什么”；store mask 决定
  “是否产生写入副作用”。二者都不是 compaction。masked store 只能阻止无效 lane 写出，不能
  修复此前已经被无效 lane 污染的 reduction 结果。
- **是否解决**：是，学习者已确认。
- **衍生问题**：暂无。

### Q03：`BLOCK_SIZE: tl.constexpr` 必须写死，还是可以变化？

- **日期**：2026-07-20
- **我的原始问题**：Python wrapper 中的 `BLOCK_SIZE` 作为编译期参数，必须以常量输入，还是
  也可以变化？
- **提问时的理解/假设**：需要区分“源码中写死的字面量”和“kernel 编译某个特化版本时已知
  的值”。
- **讲解与回答**：不必永远写死为 `1024`。`tl.constexpr` 要求 Triton 编译某次 kernel 特化时
  已经知道一个具体值；wrapper 可以先在 host Python 中计算或选择一个整数，再把它作为
  `BLOCK_SIZE=block_size` 传入。以 256、512、1024 分别 launch 都是合法思路，首次使用每个新
  配置时通常会编译相应特化，后续可复用缓存。它不能是 GPU tensor 中到 kernel 运行时才知道
  的值；若移除 `tl.constexpr`，再用动态参数决定 `tl.arange` 的静态形状，也无法成立。
- **最小例子或推导**：

  ```python
  def add(x, y, block_size: int):
      output = torch.empty_like(x)
      n = x.numel()
      grid = lambda meta: (triton.cdiv(n, meta["BLOCK_SIZE"]),)
      add_kernel[grid](x, y, output, n, BLOCK_SIZE=block_size)
      return output

  add(x, y, 256)   # 选择/编译 BLOCK_SIZE=256 的特化
  add(x, y, 1024)  # 选择/编译 BLOCK_SIZE=1024 的特化
  ```

  值也可以由 `triton.heuristics` 根据参数计算，或由 `triton.autotune` 在有限的
  `triton.Config` 候选中测量选择。实践中通常只提供少量满足 `tl.arange` 静态形状要求的 2 的幂
  候选，避免产生大量编译版本。
- **最终结论**：`tl.constexpr` 的准确含义是“对当前编译出的 kernel variant 为常量”，不是
  “整个 Python 程序生命周期中永远不变”，也不要求必须直接写成源代码字面量。
- **是否解决**：是，学习者已确认。
- **衍生问题**：不同块大小为何影响性能、何时用 heuristics 或 autotune，可在后续实践展开。

### Q04：CPU 上不能运行 Triton kernel 吗？

- **日期**：2026-07-20
- **我的原始问题**：CPU 上不能运行 Triton 的 kernel 吗？
- **提问时的理解/假设**：由 CPU tensor 传入普通 Triton launch 时出现
  `Pointer argument cannot be accessed from Triton (cpu tensor?)`，需要区分正常编译执行、
  host wrapper 和解释器模式。
- **讲解与回答**：在本课程当前的普通执行模式下，不能把 PyTorch CPU tensor 直接交给
  NVIDIA Triton kernel。Python wrapper、grid 计算和 JIT 调度逻辑运行在 CPU 上，但
  `@triton.jit` kernel 会由已选择的 accelerator backend 编译并在对应设备上执行；NVIDIA
  backend launch 需要可由该设备访问的 tensor 指针。当前安装的 Triton 3.7.1 只注册了
  `nvidia` 与 `amd` backend，没有可供普通 launch 使用的 CPU backend。

  但 Triton 另有 `TRITON_INTERPRET=1` 解释器模式。它绕过 GPU 编译，用 NumPy 等价操作在
  CPU 上逐个、顺序模拟 Triton program instance，适合检查中间值和单步调试。这是“解释执行
  Triton 语义”，不是把 kernel 编译成高性能 CPU kernel，不能用于 GPU 性能结论，而且存在
  不支持某些 dtype/访存模式等限制。
- **最小例子或推导**：本课当前 AXPBY kernel 已用 CPU tensor 验证解释器模式：

  ```bash
  TRITON_INTERPRET=1 python -c \
    'import torch; from gpu.triton import lesson01_vector_ops as ops; \
    x=torch.tensor([1.0,2.0]); y=torch.tensor([3.0,4.0]); \
    print(ops.axpby(2.0,x,-1.0,y,block_size=128))'
  ```

  输出为 `tensor([-1., 0.])`。环境变量应在导入 Triton/待测模块之前设置。若生产 wrapper 按本
  课接口显式拒绝 CPU tensor，则应为解释器另写一个仅用于调试的入口，不能让普通 CUDA 接口
  在两种设备语义之间含糊切换。
- **最终结论**：本课正常路径是“CPU 上运行 Python wrapper，GPU 上运行编译后的 Triton
  kernel”；CPU tensor 应由 wrapper 提前拒绝。解释器可以在 CPU 上模拟 kernel，但它是调试
  工具。上游另有独立的实验性 CPU backend 项目，CPU 支持仍处于开发阶段，不属于当前 pip
  安装与本课验收范围。
- **学习者复述**：Triton kernel 存在 CPU 上运行或模拟的办法，但默认安装的正常编译路径并不
  提供 CPU 执行；解释器需要 `TRITON_INTERPRET=1`，真正的 CPU 编译执行则需要额外 backend。
- **是否解决**：是，学习者已确认。
- **衍生问题**：以后需要调试 kernel 中间值时，可专门练习 `TRITON_INTERPRET=1`、
  `static_print` 和 `device_print`。

### Q05：pytest 参数中如何携带 `expected_exception`？

- **日期**：2026-07-22
- **我的原始问题**：不知道如何在参数中携带 `expected_exception`。
- **提问时的理解/假设**：已经会参数化普通输入值，但还不清楚异常类型本身也能作为 Python
  对象放入 pytest 参数表。
- **讲解与回答**：异常类可以像整数、shape 或 dtype 一样作为参数传入。参数表可同时提供
  `block_size` 与 `expected_exception`，测试函数再把后者交给
  `pytest.raises(expected_exception, ...)`。应传 `TypeError`/`ValueError` 这样的异常类，而不是
  `TypeError()` 实例。当前接口约定中，浮点配置属于错误类型，期待 `TypeError`；整数但取值不在
  允许集合中，期待 `ValueError`。
- **最小例子或推导**：

  ```python
  @pytest.mark.parametrize(
      ("block_size", "expected_exception"),
      [
          pytest.param(0, ValueError, id="zero"),
          pytest.param(1.2, TypeError, id="float"),
      ],
  )
  def test_invalid_block_size(
      block_size: int | float,
      expected_exception: type[Exception],
  ) -> None:
      with pytest.raises(expected_exception, match="block_size"):
          ...
  ```

- **最终结论**：pytest 参数不仅能携带测试数据，也能携带异常类、函数、dtype 等普通 Python
  对象；参数化的价值是让每一行用例同时声明输入与期望行为。
- **是否解决**：待学习者修改测试后确认。
- **衍生问题**：若不同异常还需要不同消息，可再增加一个 `match` 参数；若每种错误准备逻辑差异
  很大，拆成独立测试会比过度参数化更清楚。

### Q06：如何构造一维非连续 PyTorch 输入？

- **日期**：2026-07-22
- **我的原始问题**：不知道如何构建非连续输入。
- **提问时的理解/假设**：需要得到仍为一维、shape 正常，但 `is_contiguous()` 为 false 的 tensor，
  用于验证 wrapper 的 stride 契约。
- **讲解与回答**：先分配更长的连续 tensor，再用步长切片取得 view。例如长度 16 的 storage
  取 `base[::2]` 后，逻辑 shape 是 8，但 stride 是 `(2,)`；相邻逻辑元素在 storage 中间隔两个
  元素，因此它不是连续 tensor。切片通常不复制数据，适合构造这一测试。只需令 AXPBY 的一个
  输入非连续，就能验证 wrapper 是否拒绝不受支持的布局。
- **最小例子或推导**：

  ```python
  base = torch.randn(16, device="cuda", dtype=torch.float32)
  x = base[::2]
  y = torch.randn(8, device="cuda", dtype=torch.float32)

  assert x.shape == y.shape == (8,)
  assert x.stride() == (2,)
  assert not x.is_contiguous()

  with pytest.raises(ValueError, match="contiguous"):
      ops.axpby(1.0, x, 1.0, y)
  ```

- **最终结论**：contiguous 描述逻辑索引到 storage 地址的布局，不等同于 shape。`base[::2]`
  保持一维 shape，却将 stride 改为 2，正好能暴露本课裸指针线性寻址的接口限制。
- **是否解决**：待学习者补充 AXPBY 与 threshold 测试后确认。
- **衍生问题**：以后完善 `strided_1d_vector_add` 时，这类 view 可以从“应被拒绝的输入”变成
  “显式传入 stride 后应被正确支持的输入”。

### Q07：Ruff 的 import 排序与 lambda 赋值诊断具体指什么？

- **日期**：2026-07-22
- **我的原始问题**：import 排序问题和 lambda 赋值问题具体是什么？
- **提问时的理解/假设**：`I001` 看起来像导入名称顺序错误，`E731` 则指向 callable grid 的
  lambda 写法，但不知道为什么不允许。
- **讲解与回答**：本轮运行 `ruff check --diff` 后确认，两个 `I001` 实际都不是 `torch`、
  `triton` 或 `pytest` 的顺序问题，而是 import 区块与后续模块常量之间多了一行空行；删除额外
  空行即可。`E731` 表示把 lambda 赋值给名称，例如 `grid = lambda meta: ...`。若确实需要命名
  callable，PEP 8/Ruff 建议写普通 `def`，这样函数名、traceback 和可读性更明确。本例中
  `resolve_block_size` 已经在 host 端给出具体整数，因此 grid 根本不必是 callable，可以直接
  构造一维 tuple，并用关键字明确传入 meta-parameter。
- **最小例子或推导**：

  ```python
  grid = (triton.cdiv(n_elements, block_size),)
  axpby_kernel[grid](
      alpha,
      x,
      beta,
      y,
      output,
      n_elements,
      BLOCK_SIZE=block_size,
  )
  ```

  callable grid 适合其维度依赖 launch meta-parameters 的场景；直接 tuple 则适合当前所有配置都
  已在 wrapper 中解析完成的场景。
- **最终结论**：先看 Ruff 的实际 diff，不要只从规则名称猜修复方式；本次 `I001` 修空行，
  `E731` 则通过直接 tuple grid 消除，而不是机械地把 lambda 改成另一个不必要的函数。
- **是否解决**：待学习者完成 R07 后确认。
- **衍生问题**：当后续使用 `triton.autotune`、不同 config 改变 `BLOCK_SIZE` 时，callable grid
  重新具有价值，但应使用符合项目 lint 约定的命名函数或教程允许的内联形式。

### Q08：什么情况下需要 callable grid？

- **日期**：2026-07-22
- **我的原始问题**：什么情况下需要写成 callable grid？
- **提问时的理解/假设**：已经知道本课可把 lambda grid 改成直接 tuple，但需要区分这只是当前
  wrapper 的简化，还是 callable grid 本身没有用途。
- **讲解与回答**：grid 必须在 launch 前确定 program instance 的数量和维度。直接 tuple 是
  “wrapper 现在就计算”；callable grid 是“先把计算规则交给 Triton，等 kernel 参数和配置绑定
  后再计算”。当前 Triton 3.7.1 的 launch 路径会先绑定参数，再以这份参数映射调用 grid
  callable。它在 grid 依赖 `tl.constexpr` meta-parameter，而该值要由 `triton.autotune`、
  `triton.heuristics` 或其他 launch 配置稍后决定时最有价值。
- **最小例子或推导**：autotuned matmul 的不同候选可能采用不同 `BLOCK_SIZE_M/N`。每个 program
  覆盖的输出 tile 随配置改变，因此 program 数也必须用同一候选重新计算：

  ```python
  def grid(meta):
      return (
          triton.cdiv(m, meta["BLOCK_SIZE_M"])
          * triton.cdiv(n, meta["BLOCK_SIZE_N"]),
      )

  matmul_kernel[grid](..., M=m, N=n, K=k)
  ```

  若 wrapper 已经把 `block_size` 解析为具体整数，则直接写
  `grid = (triton.cdiv(n_elements, block_size),)` 更简单。输入 `n_elements` 每次调用会变化本身并不
  要求 callable，因为 wrapper 每次仍可重新计算 tuple。
- **最终结论**：当 grid 依赖“launch 时才绑定或选出的 meta 配置”时使用 callable；当 grid 所需
  的值已在 wrapper 中确定时使用 tuple。callable 在 CPU 端求值，不能读取 GPU tensor 内容来
  决定本次 launch 的 grid。
- **是否解决**：待学习者确认。
- **衍生问题**：有 autotune 并不自动意味着必须 callable；只有被调优的值会改变 grid 时才需要
  延迟计算。例如只改变 `num_warps` 而 tile 大小不变时，grid 可以仍是固定 tuple。

### Q09：如何单独参数化测试 `resolve_block_size(n, None)`？

- **日期**：2026-07-22
- **我的原始问题**：如何为 `resolve_block_size(n, None)` 单独参数化测试？
- **提问时的理解/假设**：现有端到端测试会省略 `block_size` 并检查数值结果，但还不知道如何
  直接观察 resolver 选择的具体配置。
- **讲解与回答**：`resolve_block_size` 是不需要 GPU 数据的纯 host 函数，可以把
  `n_elements` 和 `expected_block_size` 作为两列 pytest 参数，直接断言返回值。当前分支使用
  严格小于 512、1024、2048，因此每个阈值都应至少测试“前一个值”和“阈值本身”，这样能捕获
  把 `<` 误写成 `<=` 等边界错误。
- **最小例子或推导**：

  ```python
  @pytest.mark.parametrize(
      ("n_elements", "expected_block_size"),
      [
          pytest.param(0, 128, id="empty"),
          pytest.param(511, 128, id="before-512"),
          pytest.param(512, 256, id="at-512"),
          pytest.param(1023, 256, id="before-1024"),
          pytest.param(1024, 512, id="at-1024"),
          pytest.param(2047, 512, id="before-2048"),
          pytest.param(2048, 1024, id="at-2048"),
      ],
  )
  def test_resolve_block_size_uses_size_heuristic(
      n_elements: int,
      expected_block_size: int,
  ) -> None:
      assert ops.resolve_block_size(n_elements, None) == expected_block_size
  ```

- **最终结论**：端到端测试证明“无论选什么合法配置，结果都正确”；resolver 单元测试证明
  “默认选择策略本身符合当前约定”。两者观察的行为不同，不能互相替代。
- **是否解决**：待学习者补充测试后确认。
- **衍生问题**：只有当 heuristic 选择策略被视为稳定契约时才应断言具体值；若以后准备频繁调整
  性能策略，可只断言返回值属于允许集合，把具体选择留给 benchmark，而避免测试过度绑定实现。

### Q10：`Benchmark.x_names` 能否同时放 `size` 和 `block_size`？

- **日期**：2026-07-23
- **我的原始问题**：`triton.testing.Benchmark` 中的 `x_names` 可以设多个自变量吗？本实验需要
  `size` 和 `block_size` 都变化。
- **提问时的理解/假设**：把所有会变化的 benchmark 函数参数都理解成了 `x_names`，因此考虑将
  `size` 和 `block_size` 一起放进去。
- **讲解与回答**：`x_names` 确实支持多个名字，此时 `x_vals` 的每一项可以是与名字数量相同的
  tuple/list，例如 `x_names=["m", "n"]` 配 `x_vals=[(128, 256), (256, 512)]`。但它表示一组
  联动变化的横轴配置，不会自动生成多个参数的笛卡尔积；当前绘图实现也只用第一个 `x_name`
  作为真正横坐标。若多个 `x_names` 却给标量 `x_val`，当前实现会把同一个标量复制给所有名字，
  并不是本实验需要的行为。

  对 AXPBY 实验，`size` 是横轴，`block_size` 是需要比较的四条曲线，应分别放在 `x_names` 和
  `line_arg`。`perf_report` 会对每个 size 遍历全部 `line_vals`，自然得到二者的笛卡尔积：

  ```python
  triton.testing.Benchmark(
      x_names=["size"],
      x_vals=[2**12, 2**16, 2**20, 2**24],
      x_log=True,
      line_arg="block_size",
      line_vals=[128, 256, 512, 1024],
      line_names=["128", "256", "512", "1024"],
      styles=[("blue", "-"), ("green", "-"), ("orange", "-"), ("red", "-")],
      ylabel="GB/s",
      plot_name="axpby-block-size",
      args={},
  )
  ```

  被装饰函数相应接收 `benchmark(size, block_size)`。内部遍历等价于：

  ```text
  for size in x_vals:
      for block_size in line_vals:
          benchmark(size=size, block_size=block_size)
  ```

- **最终结论**：`x_names` 不是“所有自变量”，而是横轴配置参数；本实验使用
  `x_names=["size"]`、`line_arg="block_size"`。多个 `x_names` 更适合 `(M, N, K)` 等需要成组
  变化的 shape 配置。如果以后还要同时比较 Torch/Triton provider，因 `Benchmark` 只有一个
  `line_arg`，宜另建一份 provider report，或把 provider 与 block size 组合成单个配置标签。
- **是否解决**：已回答，待学习者实现时验证。
- **衍生问题**：`styles` 若显式提供，应与四条 `line_vals` 一一对应；否则可省略并让绘图库选择
  默认样式。

### Q11：为什么 `x_names` 始终是 `List[str]`，多个名字会生成什么？

- **日期**：2026-07-23
- **我的原始问题**：为什么 `x_names` 的类型是 `List[str]`？如果真的传入一组 `x_names`，结果会
  是什么样？
- **提问时的理解/假设**：单横轴似乎只需要一个字符串，因此列表类型可能意味着每个名字都是一条
  独立横轴。
- **讲解与回答**：`Benchmark` 用统一的列表接口表示“一项或多项共同描述横轴配置的函数参数”，
  避免 API 同时接受 `str` 与 `list[str]` 两套形态。运行时，每一项 `x_val` 会先变成一组值，
  再与 `x_names` 做 `zip`，构造传给 benchmark 函数的关键字参数。

  tuple/list 形式表示显式配对：

  ```python
  x_names=["m", "n"]
  x_vals=[(128, 256), (256, 512)]
  ```

  会生成两行配置，并对每行继续遍历所有 `line_vals`：

  ```text
  benchmark(m=128, n=256, ...)
  benchmark(m=256, n=512, ...)
  ```

  当前 Triton 3.7.1 的无 GPU 最小实验得到的结果表结构为：

  ```text
    m    n    A(score)    B(score)
  128  256      ...         ...
  256  512      ...         ...
  ```

  标量形式则会复制给所有名字：

  ```python
  x_names=["m", "n", "k"]
  x_vals=[128, 256]
  ```

  等价于两组方阵配置 `(128, 128, 128)` 和 `(256, 256, 256)`。这在 square GEMM 等场景很方便。
  若 tuple/list 长度与 `x_names` 不同，则抛出 `ValueError`。

- **最终结论**：多个 `x_names` 会形成结果表中的多个配置列，但不是多个独立图形坐标轴。当前
  绘图只选择第一个 `x_name` 作为横坐标，其余名字仍会传入被测函数并保存在表格/CSV 中。若多行
  共享相同的第一个值、只改变后续值，点会落在同一横坐标附近甚至被连成难读的曲线，因此本次
  size/block-size 实验仍应使用一个 `x_name` 加一个 `line_arg`。
- **是否解决**：已回答，待学习者确认。
- **衍生问题**：若真正需要两个彼此独立的扫描维度和热力图，`perf_report` 的折线抽象并不合适，
  应手工生成笛卡尔积结果表，再用更适合二维数据的绘图方式。

### Q12：为什么指定新的 `save_path` 时第一次失败、第二次成功？

- **日期**：2026-07-24
- **我的原始问题**：第一版 benchmark 把结果保存到
  `experiment_results/lesson01/axpby-block-size`。第一次运行在 `plt.savefig` 抛出
  `FileNotFoundError`，不做修改直接运行第二次却能正常生成结果。
- **提问时的理解/假设**：现象看起来像 GPU benchmark 或图片保存具有不稳定性，但相同命令第二
  次总能成功。
- **观察证据**：本地 Triton 3.7.1 的 `Mark._run()` 会先执行
  `plt.savefig(save_path / plot_name.png)`，之后才准备写 CSV；而外层 `Mark.run()` 把
  `os.makedirs(save_path, exist_ok=True)` 放在 `finally` 中，并且位于 `_run()` 调用之后。
- **讲解与回答**：当目标目录尚不存在时，第一次 `savefig` 无法打开目标 PNG 路径，于是抛出
  `FileNotFoundError`。无论 `_run()` 是否成功，`finally` 都会执行，因此失败路径反而创建了
  `save_path` 和 `results.html`。第二次运行时目录已经存在，PNG、CSV 和 HTML 便可以全部保存。
  这是当前 Triton 测试工具的目录创建顺序问题，不是 AXPBY kernel、GPU 异步执行或 JIT 的错误。
- **修复方向**：调用 `.run()` 前由 benchmark 脚本显式创建输出目录：

  ```python
  result_dir.mkdir(parents=True, exist_ok=True)
  benchmark_axpby_block_size.run(
      print_data=True,
      show_plots=False,
      save_path=str(result_dir),
  )
  ```

  目录创建与 `.run()` 一起放进 `main()`，并使用 `if __name__ == "__main__":` 调用，避免 import
  benchmark 模块时自动运行完整实验。若使用相对路径，还应明确它相对于启动命令的当前工作目录，
  或从 `__file__` 推导仓库根目录。
- **最终结论**：第一次失败后第二次成功是完全可解释、可复现的控制流结果。正确做法是在调用方
  预先建立 `save_path`，而不是依赖一次预期失败来初始化目录。
- **是否解决**：学习者已在 `run_benchmark` 中预先创建目录并补上 main guard。正式评审使用临时
  的全新嵌套目录验证：运行前 `exists=False`，一次调用后 PNG、CSV、HTML 均存在；已验证关闭。
- **衍生问题**：本版 `perf_report` 保存的 CSV 只保留中心曲线列；p20/p80 延迟与吞吐区间仍需
  由练习脚本或独立实验记录显式保存，不能仅凭该 CSV 视为已满足完整证据要求。

### Q13：P01 要如何保存延迟分位数和完整 GB/s 区间？

- **日期**：2026-07-24
- **我的原始问题**：已经修复 P05/P06，接下来逐项处理前三个主要发现；P01 中缺少的数据应该
  如何添补？
- **提问时的理解/假设**：`perf_report` 已经拿到三项 GB/s 并画出阴影，因此可能可以从其 CSV
  或返回 DataFrame 中直接获得全部耗时与区间。
- **讲解与回答**：当前 Triton 3.7.1 的 `perf_report` 只接受一个 y 值或
  `(中心值, 下界, 上界)` 三元组用于绘图，并在保存 CSV/返回 DataFrame 前删去上下界列。因此
  不能返回 9 个指标，也不能靠 `return_df=True` 找回原始延迟。数据必须在
  `benchmark_axpby_block_size` 内部、`do_bench` 返回之后且转换为绘图三元组之前另行捕获。

  建议把单配置结果建模为一条结构化记录，至少包含：

  ```text
  size, block_size, warmup_ms, rep_ms,
  p20_ms, p50_ms, p80_ms,
  gbps_lower, gbps_p50, gbps_upper
  ```

  使用能表达真实顺序的变量名：

  ```python
  p50_ms, p20_ms, p80_ms = do_bench(
      fn,
      warmup=WARMUP_MS,
      rep=REP_MS,
      quantiles=[0.5, 0.2, 0.8],
  )
  ```

  然后同一次测量完成两件事：

  ```text
  1. 把完整记录追加到本次运行的 records；
  2. 仍向 perf_report 返回
     (gbps(p50_ms), gbps(p80_ms), gbps(p20_ms))。
  ```

  `.run()` 成功结束后，再把 records 写成独立的
  `axpby-block-size-detailed.csv`。可使用 dataclass 加标准库 `csv.DictWriter`，或等价的清晰
  结构；开始一次新实验前先清空 collector，防止重复调用 `.run()` 时产生重复行。为以后复用到
  P02，可进一步把“一组 size/block size 的输入分配、do_bench 和换算”提取成返回单条 record
  的测量函数，主图和尾块实验共同调用它。

- **完整性检查**：核心矩阵应产生 `4 * 4 = 16` 行。每行必须满足：

  ```text
  p20_ms <= p50_ms <= p80_ms
  gbps_lower <= gbps_p50 <= gbps_upper
  ```

  检查、记录追加和 CSV 写入都在 `do_bench` 的被测 callable 外，不会污染单次 kernel event
  时间。对微秒级小 kernel，保存足够的小数位，避免把不同分位数过早四舍五入成相同值。
- **最终结论**：保留 `perf_report` 自动生成的中心 GB/s CSV/PNG，同时新增一份以“每配置一行”
  保存原始延迟与换算带宽的 detailed CSV；二者职责不同，不能互相替代。
- **是否解决**：学习者已实现并通过 P01 定向复审，详细数据连续两次运行均为 16 行且换算正确。
- **衍生问题**：首次主实验没有保存的原始分位数无法从中心 CSV 精确恢复，必须重新测量；旧
  CSV 应保留为第一版证据或明确标为已被新实验取代，不能人工反推补写。

### Q14：P02 要预测什么、写在哪里，以及如何复用主 benchmark？

- **日期**：2026-07-24
- **我的原始问题**：尾块实验前所说的“写下预测”具体要预测什么、写在哪里？尾块测试几乎可以
  复制主 benchmark 并只改装饰器，能否复用？
- **提问时的理解/假设**：预测可能是猜最快的 block size；实现上则可能需要复制整个被装饰函数。
- **讲解与回答**：预测是尚未看见 P02 数据时写下的、可被结果推翻的假设，不要求猜对。应在
  `docs/triton-learning/attachments/01-vector-add/axpby-benchmark.md` 新建“实验前预测”小节，
  明确注明主矩阵首次运行前没有保存预测，本次内容只针对尚未运行的尾块实验，不能回填成旧实验
  的事前预测。

  P02 对比 `N=2**20` 与 `N=2**20+17`。前者被四种块大小整除，后者每种配置都多一个 program：

  | block size | 整除尺寸 programs | 尾块尺寸 programs | 尾 program 有效/无效 lane |
  | ---: | ---: | ---: | ---: |
  | 128 | 8192 | 8193 | 17 / 111 |
  | 256 | 4096 | 4097 | 17 / 239 |
  | 512 | 2048 | 2049 | 17 / 495 |
  | 1024 | 1024 | 1025 | 17 / 1007 |

  预测至少回答：

  1. 尾块尺寸的 p50 延迟相对整除尺寸预计上升、近似不变还是可能被噪声淹没？
  2. 哪个 block size 可能对额外 program 最敏感，理由是尾 program 利用率、program 总数还是
     调度波次？
  3. 有效 GB/s 预计如何变化？注意分子也多了 17 个有效元素，不能只看运行时间。
  4. 什么观察会推翻预测？可比较 p50 相对变化与各自 p20–p80 运行波动，但后者只是样本分布区间，
     不是统计置信区间。

  实现上不应复制完整 decorated function。把“测量一个 `(size, block_size, provider)` 配置”的
  逻辑提取成普通函数，返回一条 `BenchmarkRecord`：

  ```text
  measure_axpby(...)
    -> 分配固定输入
    -> 选择被测 callable
    -> do_bench
    -> 校验分位顺序
    -> 换算 GB/s
    -> return BenchmarkRecord
  ```

  主 `perf_report` adapter 只负责调用它、收集 record，并返回绘图三元组。尾块实验则用两层循环
  对两个 size 和四个 block size 调用同一个测量函数，生成 8 行独立 detailed CSV。写 CSV 的
  函数也应接收 `records` 与输出路径/文件名，避免尾块运行覆盖主矩阵记录。

  Triton 还支持把多个 `Benchmark` 配置列表传给同一个 `@perf_report([...])`，从而复用同一被
  装饰函数。但这两个 size 在数轴上只差 17，折线图几乎重合；而同一 collector 还会再次出现
  `2**20` 的记录，需要增加 experiment 标签。因此本课更推荐共享普通测量函数、用独立尾块表
  对比，而不是再画一张信息量很低的图。
- **最终结论**：预测写入结构化实验报告，内容是方向、理由、不确定性和可证伪条件；代码复用以
  “单配置测量函数”为边界，主曲线与尾块表只保留很薄的 orchestration 层。
- **是否解决**：方案已给出，待学习者先写 P02 预测，再重构和运行尾块实验。
- **衍生问题**：若以后确实使用一组 `Benchmark` 配置运行多个实验，应在 record 中增加
  `experiment` 字段，并以 `(experiment, size, block_size)` 判断唯一性。

### Q15：为什么尾块实验中的有效 GB/s 有时反而上升？

- **日期**：2026-07-24
- **我的原始问题**：GB/s 不一定下降可以理解为代码多层优化和 GPU 细粒度控制使性能保持不变，
  但为什么实验中有时会出现 GB/s 上升？
- **提问时的理解/假设**：GB/s 上升意味着尾块触发了更优的代码或硬件执行策略。
- **讲解与回答**：本实验的 GB/s 是用算法有效字节数除以独立测得时间得到的比值，不是硬件
  计数器直接测得的 DRAM 带宽。对同一 block size，`n_elements` 是运行时参数，两个 size 通常
  使用同一 JIT kernel specialization，只是 grid 多一个 program；因此不能先把上升归因于重新
  优化了代码。

  两次结果的比值为：

  ```text
  tail_gbps / exact_gbps
    = (N_tail / N_exact) * (t_exact / t_tail)
  ```

  其中 `N_tail/N_exact = (2**20+17)/2**20 = 1.0000162`。若两次 p50 都为 15.360 µs，第二项
  等于 1，仅因有效元素多 17 个，尾块 GB/s 就会机械地微升约 0.00162%；学习者 BS=128 的
  819.200 -> 819.213 GB/s 正属于此类，不代表实际硬件带宽提高。

  较大的上升来自分母变化。例如 BS=256 的保存结果从 16.384 µs 降到 15.360 µs，恰好少一个
  当前环境观测到的 1.024 µs 计时台阶，于是有效 GB/s 从 768.000 升到 819.213，约 +6.67%。
  这不是尾块必然加速的证据：两组 p20–p80 区间高度重叠，独立复测时变化方向也会反转。p50 是
  两个独立样本分布的中心统计量，可能因计时离散、GPU 时钟、SM 调度波次和系统活动落到相邻
  档位；清理 L2 也不能重置所有硬件状态。

  masked-out lane 不产生完整一块的有效 load/store 流量，但尾 program 仍有调度和 predication
  成本。理论上 grid 大小变化可能改变波次与负载分配，不过当前只有一个计时台阶的差异且运行间
  不稳定，不能从本数据识别出这种真实机制。若需要判断实际 DRAM 流量或持续带宽，应使用硬件
  profiler 和更强的重复/实验控制。
- **最终结论**：本实验中 GB/s 上升有两类：

  1. 时间相同、有效字节略增造成的约 0.00162% 公式性上升；
  2. 独立 p50 落到更低计时档位造成的约 6% 表观上升，当前证据主要应解释为测量波动。

  对区间重叠且跨轮次方向反转的结果，应写“本方法未检测到稳定差异”，不能写“尾块更快”。
- **是否解决**：已回答，待学习者在 P02 实验后复盘中用自己的话区分比值变化与真实硬件带宽。
- **衍生问题**：增大 `rep` 会增加样本数量，但不会自动消除单次事件的离散时间档位；若把多个
  launch 批量放进一次被测 callable 再求平均，又会改变 cache 和测量边界，必须作为另一种方法
  单独声明。

### Q16：能否让 benchmark 连续运行多次并用总时间求平均？

- **日期**：2026-07-24
- **我的原始问题**：尾块结果的分母是否因为单次采样时间太短而容易波动；能否让 benchmark
  连续运行多次、测总时间后再求平均？
- **提问时的理解/假设**：把 `rep` 调大可能会自动延长每个 GPU event 所覆盖的计时间隔。
- **讲解与回答**：方向基本正确，但需要区分“总采样预算”和“单个计时间隔”。当前 Triton
  3.7.1 的 `do_bench` 先估算一次 callable 的耗时，再按
  `n_repeat = max(1, int(rep / estimate_ms))` 决定样本数；每个样本仍用一对 GPU event 只包围
  一次 callable。因此 `rep=100` 表示总计约采样 100 ms，不是每个样本运行 100 ms。增大
  `rep` 可以让分位数建立在更多单次样本上，却不会提高约 15 µs 单次 event 的时间分辨率。

  可以把多次 launch 放进一个 callable，测得批量总时间后除以批次数：

  ```python
  batch_runs = 100

  def launch_batch() -> None:
      for _ in range(batch_runs):
          launch_once()

  total_p50, total_p20, total_p80 = triton.testing.do_bench(
      launch_batch,
      warmup=WARMUP_MS,
      rep=REP_MS,
      quantiles=[0.5, 0.2, 0.8],
  )
  p50_per_launch = total_p50 / batch_runs
  ```

  本地用预分配输出、`size=2**20`、`BLOCK_SIZE=256` 做方向性对照，单次 `do_bench` 的 p50
  为 17.408 µs；每组连续发射 100 次时，组总 p50 为 0.918528 ms，折算为 9.185 µs/次；
  `do_bench_cudagraph` 折算约为 4.742 µs/次。这些差异说明批量方法并非只是给同一测量“增加
  精度”：

  1. `do_bench` 只在每个外层样本前清理一次 L2，批内后续 launch 会看到热缓存；
  2. 普通 Python 循环可能包含主机发射跟不上 GPU 所形成的流空闲；
  3. `do_bench_cudagraph` 会捕获许多固定地址的 launch、测图的总时间并除以次数，进一步移除
     大部分主机发射间隙，但它不清理每次 launch 之间的 L2。

  因此三者回答不同问题。当前单次 `do_bench` 更接近“每次清 L2 后的单次 kernel 延迟”；手工
  batching 更接近“Python 连续发射时的批处理吞吐”；CUDA Graph 更接近“固定工作集、热缓存且
  发射开销被摊薄的设备稳态吞吐”。若使用 batching，应把它作为独立实验，记录 `batch_runs`，
  并用 `batch_runs * effective_bytes / total_time` 计算吞吐；不能与原来的单次冷缓存曲线混在
  一张表中解释。若仍要保持冷缓存语义，需要轮换总工作集明显大于 L2 的多组缓冲区，或继续采用
  单次测量并承认 `+17` 元素的差异小于该方法的可分辨能力。
- **最终结论**：单次计时间隔过短确实会放大分母的离散与波动，但 `rep` 只增加样本数。批量总
  时间法和 `do_bench_cudagraph` 都能延长计时间隔，却会切换到热缓存或稳态测量语义；它们适合
  作为补充实验，而不是静默替换当前 benchmark。
- **是否解决**：已回答；若后续实施批量实验，需要先明确要测冷缓存单次延迟、连续调用吞吐，
  还是 CUDA Graph 下的设备执行吞吐。

### Q17：为什么测量值呈现约 1.024 µs 的整数倍，什么是计时台阶？

- **日期**：2026-07-24
- **我的原始问题**：为什么之前的时间测量值约为 1.024 µs 的整数倍；“计时台阶”具体是什么？
- **提问时的理解/假设**：GPU kernel 的实际执行时间可能只能以 1.024 µs 为单位变化。
- **讲解与回答**：“计时台阶”是本课对 **quantization step（量化步长）** 的描述性简称，不是
  CUDA API 中的正式术语。有限分辨率的计时器不能区分任意接近的时间，真实运行时间经过事件
  时间戳和差值换算后，只能落到一组离散的可报告值上。若本次观测到的相邻值为
  `15.360、16.384、17.408 µs`，它们之间的 `1.024 µs` 就是这批数据呈现出的有效计时台阶。
  这类似最小刻度为 1 mm 的尺子：物体长度可以落在刻度之间，但读数不会连续呈现所有可能值。

  当前 Triton 3.7.1 的 `do_bench` 在 NVIDIA backend 上使用 `torch.cuda.Event`，底层走
  `cudaEventElapsedTime`。NVIDIA 文档只说明 CUDA Event 的分辨率约为 0.5 µs，并没有承诺所有
  GPU、驱动和软件栈都返回固定的 0.5 µs 或 1.024 µs 网格：
  [CUDA Runtime API 13.0 的 event 说明](https://docs.nvidia.com/cuda/archive/13.0.0/cuda-runtime-api/group__CUDART__EVENT.html)。

  为区分格式化舍入和原始计时量化，本轮用 `quantiles=None, return_mode="all"` 检查了当前
  A100-SXM4-80GB、驱动 580.159.03 环境中的单次原始样本。不同工作量分别出现：

  ```text
  size=2**16:  8192, 9216, 10240, 11264 ns
  size=2**20:  15360, 16384, 17408, 18432, ... ns
  size=2**24:  123904, 124928, 125952, 126976, ... ns
  ```

  相邻原始值都相差 1024 ns，因此在**当前栈**中，把 1.024 µs 称为“观测到的有效台阶”是有
  数据依据的。它不是 CSV 小数位造成的，也不是 Python 浮点数在这个数量级的精度上限。但公开
  文档没有给出足够依据把其内部原因精确归结为某个 A100 硬件时钟或驱动常数，所以不能把
  1.024 µs 当作 CUDA 的通用定律；更换 GPU、驱动、backend 或计时 API 后，台阶可能不同。

  这也不表示 kernel 只能以 1.024 µs 为单位执行。GPU 指令周期、内存事务、program 波次和实际
  调度仍能在更细尺度上变化，只是 CUDA Event 这条测量路径未必能把这些差异反映到返回值中。
  原始样本先被量化，随后 `do_bench` 才计算 p20/p50/p80；分位数插值有时可以产生不在原始网格
  上的数，但这不会凭空恢复丢失的时间信息。
- **影响举例**：当 kernel 约为 15.360 µs 时，一个 1.024 µs 台阶已经占
  `1.024 / 15.360 = 6.67%`。真实分布只需略微移动，使中位数从相邻量化区间的一侧跨到另一侧，
  报告的 p50 就可能整体跳一个台阶；以它作分母的有效 GB/s 也会出现约 6% 的反向跳变。因此
  “相差一个台阶”不能单独作为真实性能差异的证据。
- **最终结论**：1.024 µs 是当前环境原始 CUDA Event 样本呈现的经验量化步长，不是 kernel 的
  执行粒度，也不是 CUDA 对所有设备的固定保证。“计时台阶”就是相邻可报告时间值之间的间隔。
  面对只有一两个台阶的差异，应查看原始分布、独立复测并承认测量分辨率限制；若改用批量计时来
  拉长区间，则按 Q16 将其作为测量语义不同的补充实验。
- **是否解决**：已回答；同时将此前的“1.024 µs 计时台阶”表述限定为当前环境中的观察结果。

### Q18：masked lane 的访存为何消失，它与“GPU 优化冗余访存”有什么区别？

- **日期**：2026-07-24
- **我的原始问题**：既然 masked-out lane 的访存不是 GPU 优化掉的冗余动作，为什么这部分
  访存动作最终没有发生？
- **提问时的理解/假设**：Triton 可能先生成完整 block 的无条件 load/store，再由编译器或 GPU
  发现越界 lane 的访问无用并删掉。
- **讲解与回答**：`mask` 本身就是 `tl.load` / `tl.store` 的执行条件，而不是给一条已经存在的
  无条件访存附加的优化提示。可将一条 masked load 的语义写成：

  ```text
  predicate = offset < n_elements
  if predicate:
      value = load(pointer)
  else:
      value = other 或未定义占位值
  ```

  因此 false lane 从语义上就没有对应地址的 load/store。编译器通常用 predicated instruction
  实现这个条件，而不必生成一次真正的分支。对当前 AXPBY、`BLOCK_SIZE=256` 编译出的 PTX
  可见：

  ```ptx
  setp.lt.s32  %p1, %r15, %r14;
  @%p1 ld.global.b32 { %r1 }, [ %rd1 + 0 ];
  @%p1 st.global.b32 [ %rd5 + 0 ], { %r5 };
  ```

  `setp` 根据 `offset < n_elements` 产生谓词 `%p1`；指令前的 `@%p1` 是 guard predicate。
  `%p1=false` 时，该 lane 不执行 `ld.global` / `st.global`，不会求值该指令的地址，也不会产生
  该 lane 的内存请求。地址计算、谓词计算以及后续算术指令仍可能占用指令和调度资源；本次 PTX
  中 false load lane 的寄存器碰巧先初始化为 0，但源码未传 `other`，不能依赖这个实现细节。

  需要区分三个层次：

  | 层次 | false lane 的行为 |
  | --- | --- |
  | Triton 语义 | 不访问 `pointer[idx]`；load 返回 `other[idx]` 或未指定时的未定义值，store 不写入 |
  | PTX / SIMT 执行 | warp 可以发射同一条 predicated 指令，但 false predicate 的 lane 被禁用 |
  | cache / DRAM transaction | 内存系统只合并 active lane 的请求，但按 sector/cache-line 粒度传输，物理字节数可能大于 active 标量字节数 |

  例如尾块的逻辑 mask 为 `[T, T, F, F]` 时，前两个 lane 请求两个 float，后两个 lane 不请求
  地址。对 compute capability 6.0 及以上 GPU，global memory access 以 32-byte transaction
  粒度合并；即使只有 8 个有效字节，一个覆盖它们的 32-byte segment 仍可能整体传输。这不等于
  false lane 执行了自己的 load：相邻未使用字节可能随物理 segment 被搬运，但没有作为 false
  lane 的请求被读取、返回或越界解引用。

  因此“处理完整逻辑 block”和“产生完整 block 的显存流量”不是一回事。尾 program 仍保留固定
  block tensor 形状、program/warp 调度、谓词和部分算术成本；有效 lane 才提出内存请求，实际
  transaction 又受对齐、合并、cache 和 sector 粒度影响。当前有效 GB/s 只用
  `3 * N * element_size / time` 计算算法字节数，不能从它反推实际 DRAM 字节数。
- **为什么不称为优化**：优化通常表示实现发现某个原本允许执行的冗余操作，并在不改变语义的
  前提下删除它；这里 false lane 不访存本来就是 `mask` 所规定的正确性语义。predication 是
  实现这项语义的硬件机制。可以说 GPU 对条件执行提供了高效支持，但不能说它事后猜测并优化掉
  了整块冗余访存。
- **最终结论**：mask 不是“先访存再过滤”，而是“先计算 predicate，再决定该 lane 是否执行
  内存指令”。false lane 没有地址访问；active lane 的请求仍可能因物理 transaction 粒度搬运
  更多相邻字节。lane 级语义、实际 DRAM 流量和有效 GB/s 必须分别讨论。
- **是否解决**：已讲解并用当前 kernel 的 PTX 验证；P02-R1 仍待学习者在复盘中用自己的话
  重述后复审。

## 7. 实践任务

实践使用以下新文件，不覆盖仓库已有的 `gpu/triton/vector_add.py` 冒烟实现：

| 用途 | 建议路径 |
| --- | --- |
| 两个 kernel 及其 Python wrapper | `gpu/triton/lesson01_vector_ops.py` |
| GPU 正确性测试 | `gpu/triton/lesson01_vector_ops_test.py` |

测试文件放在 `gpu/triton/`，避免加入默认的 CPU-only pytest 集；在真实 GPU 开发容器中显式
运行该文件。

### 通用验收要求

- 使用 `@triton.jit` 实现核心计算，不在 wrapper 中用 PyTorch 代替待实现的 Triton 算子。
- 第一版只要求一维、CUDA、contiguous、相同 shape/dtype 的 float32 tensor；wrapper 必须显式
  检查并清楚拒绝不支持的输入。
- 输出 shape、dtype、device 与输入一致。
- `BLOCK_SIZE` 必须作为 `tl.constexpr` meta-parameter，并允许 wrapper 从
  `{128, 256, 512, 1024}` 中接收不同选择；不接受集合外或非 2 的幂配置。
- 对空 tensor 在 wrapper 中直接返回正确的空输出，不 launch 一个零大小 grid。
- 使用 `torch.testing.assert_close` 与 PyTorch reference 比较。
- 至少覆盖小于块大小、恰好整除和带尾块三类尺寸。
- 保留简短 docstring 和必要注释，但不要逐行复述代码。

### 练习 1：AXPBY 融合向量运算（必做）

实现：

```text
output[i] = alpha * x[i] + beta * y[i]
```

建议接口：

```python
def axpby(
    x: torch.Tensor,
    y: torch.Tensor,
    alpha: float,
    beta: float,
    *,
    block_size: int = 256,
) -> torch.Tensor:
    ...
```

必须满足：

1. Kernel 参数包含 `alpha`、`beta` 和 `BLOCK_SIZE: tl.constexpr`。
2. 使用 `program_id + arange` 生成一维 offsets。
3. load 和 store 都用正确的边界 mask。
4. grid 必须根据本次传入的 meta-parameter 计算，不能与默认块大小偷偷绑定。
5. wrapper 验证两个输入的一维 shape、device、dtype、contiguity 和 block size。
6. `x.numel() == 0` 时返回空输出。

最低测试矩阵：

```text
BLOCK_SIZE: 128, 256, 512, 1024
N:          0, 1, 127, 128, 129, 1023, 1024, 1025, 98417
(alpha, beta): (1.0, 1.0), (2.0, -0.5), (0.0, 3.0)
```

不要求对所有组合做笛卡尔积，但每种 block size、边界类型和系数组合都至少出现一次。

PyTorch reference：

```python
expected = alpha * x + beta * y
```

完成定义：所有正确性用例通过；错误 shape、CPU tensor、不同 dtype、非连续输入和非法 block
size 均产生清晰异常。

### 练习 2：条件平方更新（必做）

这个练习专门验证 Q02 的 store mask 语义。实现：

```text
如果 x[i] > threshold：output[i] = x[i] * x[i]
否则：               output[i] = x[i]
```

建议接口：

```python
def square_above_threshold(
    x: torch.Tensor,
    threshold: float,
    *,
    block_size: int = 256,
) -> torch.Tensor:
    ...
```

实现约束：

1. Wrapper 先用 `x.clone()` 初始化 output。
2. Kernel 使用 boundary mask 加载 x；为 masked-out load 显式提供合适的 `other`。
3. 构造 `write_mask = boundary_mask & (x_values > threshold)`。
4. 只通过 masked `tl.store` 写入平方值；不要在 kernel 中用 `tl.where` 生成全部最终输出。
5. 这样，条件为 false 的有效地址必须保留 clone 中的原值。

最低测试：

- 同时包含小于、等于和大于 threshold 的值。
- 至少一个 `N < BLOCK_SIZE` 用例。
- 至少一个非整除尺寸，例如 `N=259, BLOCK_SIZE=128`。
- 使用全负数且 threshold 也为负数的用例，避免只靠 0 恰好得到正确结果。

PyTorch reference：

```python
expected = torch.where(x > threshold, x * x, x)
```

完成定义：结果与 reference 一致，并能解释为什么 false 的 store lane 会保留 `x.clone()` 中的
内容，而不是被写成 0 或未定义值。

### 练习 3：块大小与性能观察（可选）

本练习已于 2026-07-23 恢复为进入第 02 课前的当前实践。

#### 学习目标与产物

理解 `do_bench`、GPU 异步计时、JIT 预热、耗时分位数、有效带宽和实验矩阵，并用实测证据评价
不同块大小。学习者需要独立完成：

1. `gpu/triton/lesson01_vector_ops_benchmark.py`：可直接作为模块运行的 benchmark 脚本。
2. `docs/triton-learning/attachments/01-vector-add/axpby-benchmark.md`：环境、预测、结果与分析记录。

#### 必须满足

1. 使用 `triton.testing.do_bench` 测量现有 `axpby` wrapper，不修改 kernel 来迎合 benchmark。
2. 比较 `BLOCK_SIZE=128/256/512/1024`，输入规模至少包含 `2**12`、`2**16`、`2**20`、
   `2**24`；另测一个带尾块的 `2**20 + 17`，可单独输出而不放进主曲线。
3. 固定 dtype 为 float32、固定 `alpha`/`beta`，在每个被测配置的计时区间外创建 `x` 和 `y`。
   不在被测 callable 中生成随机输入、做 correctness assertion、打印或显式同步。
4. 使用 `quantiles=[0.5, 0.2, 0.8]`，保留 p20、p50、p80 延迟；明确 `warmup` 和 `rep` 的毫秒
   参数。依靠 `do_bench` 正确处理同步并排除首次 JIT，不另把首次手工 wall-clock 结果混入。
5. 按 `3 * N * element_size` 计算有效 GB/s，并正确反转耗时区间：中心值用 p50、吞吐下界用
   p80、吞吐上界用 p20。
6. 使用 `Benchmark`/`perf_report` 生成以 size 为横轴、四种 block size 为曲线的主结果；容器中
   默认 `show_plots=False`。脚本必须使用 `if __name__ == "__main__":`，不能在 import 时运行。
7. benchmark 在当前 CUDA device 上创建输入，并保证 event、cache buffer 和 kernel 位于同一
   device context。无 CUDA 时给出清晰错误，而不是静默生成结果。
8. 结果记录必须包含运行日期、GPU、driver、Python、Torch、Torch CUDA runtime、Triton、
   warmup、rep、quantiles、完整运行命令，以及 p20/p50/p80 延迟和有效 GB/s。
9. 运行性能实验前先执行现有 correctness tests。不要在 pytest 中断言某个 block size 必须最快，
   也不要设置依赖当前 A100 的固定性能阈值。

#### 实验前预测与实验后分析

运行前先在记录中预测各规模下哪个 block size 可能最快，并写出理由；预测允许错误，但必须先于
结果保存。运行后回答：

1. 每个规模下实测最快的 block size 是什么？差异是否大于 p20–p80 波动区间？
2. 小输入与大输入的 GB/s 曲线为何不同，何时开始接近平台区？
3. `2**20` 与 `2**20 + 17` 的结果是否支持“尾块一定很慢”？为什么不能从一次测量下定论？
4. 当前 `resolve_block_size` 策略是否得到数据支持？哪些输入区间仍缺少证据？
5. 本实验测到的是 wrapper 所代表操作的 GPU stream 时间，还是完整 CPU 调用 wall-clock？

#### 验证与完成定义

```bash
uv run --frozen python -m pytest -q gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff check gpu/triton/lesson01_vector_ops_benchmark.py
uv run --frozen ruff format --check gpu/triton/lesson01_vector_ops_benchmark.py
uv run --frozen python -m gpu.triton.lesson01_vector_ops_benchmark
```

完成定义：脚本可复现运行，四种块大小和规定尺寸均有数据，统计与 GB/s 区间方向正确，实验记录
区分事实、解释和限制，并能回答上述五个问题。第一版完成后先提交源码、运行输出和记录供 review，
不要根据“看起来应该更快”提前改动 kernel。

允许的初始提示仅限本课 4.8 节和官方 `01-vector-add.py` 的 benchmark 结构。需要时可以逐级请求
更具体的提示。

可选扩展：在完成核心实验后，另建 Torch eager 的 `alpha * x + beta * y` 对照，或比较
预分配 output 的 kernel-only 计时；必须单独标明测量边界和有效字节口径，不能混入核心结果后
直接宣称是实际 DRAM 带宽。

### 运行与提交检查

在有 GPU 的开发容器中运行：

```bash
uv run --frozen pytest gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff format --check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py
```

完成第一版后，保留运行输出并提交这两个文件给代码评审。不要先执行 `ruff --fix` 掩盖自己想
理解的诊断；可以先阅读提示，再决定如何修改。

## 8. 实现与实验记录

### 计划实现文件

| 用途 | 路径 | 当前状态 |
| --- | --- | --- |
| Kernel / wrapper | `gpu/triton/lesson01_vector_ops.py` | 第三轮评审后已修 R08/R09 核心逻辑，待测试固化与代码整理 |
| GPU tests | `gpu/triton/lesson01_vector_ops_test.py` | 现有 20 个用例全通过，输入契约覆盖仍待补齐 |
| 旧 strided add 练习 | 已归并到 `gpu/triton/lesson01_vector_ops.py` | 仅整理位置，尚无 wrapper、pytest 与正式评审 |
| Benchmark | `gpu/triton/lesson01_vector_ops_benchmark.py` | 第一版已实现，第 1 轮性能评审后待修改 |
| 性能记录 | `docs/triton-learning/attachments/01-vector-add/axpby-benchmark.md` | 已布置，待预测与实测 |

### 第一版实现摘要

- 提交日期：2026-07-20。
- `axpby_kernel` 已完成一维 offsets、边界 masked load/store 和融合表达式。
- `threshold_square_kernel` 已正确采用 `output = x.clone()` 加条件 masked store 的总体方案。
- Python wrapper 已分配输出并根据问题规模选择一个 block size。
- 第一版测试对 128 个随机 size 与 PyTorch reference 计算最大误差，但只打印结果，尚无测试
  断言，也没有结构化覆盖空输入和确定的 block 边界。
- 当前记录环境没有 GPU，本轮只完成 pytest collection 与静态检查；数值结果仍待学习者在 GPU
  容器中提供。

### 第二版 pytest 运行记录

- 运行日期：2026-07-20。
- 命令：`uv run --frozen pytest -vv gpu/triton/lesson01_vector_ops_test.py`。
- 环境：Python 3.12.13、pytest 8.4.2；本次输出未记录 GPU 型号。
- 收集结果：20 个独立 test items，说明包导入、测试发现和参数化已经正确工作。
- 运行结果：15 passed、5 failed，用时 4.42 秒。
- 15 个数值用例全部通过，覆盖 AXPBY、threshold 语义、空输入和多个尾块尺寸。
- 4 个非法 block size 用例均为 `DID NOT RAISE`；1 个 CPU tensor 用例抛出了 Triton 底层
  `ValueError`，但消息不符合 wrapper 契约。

### 第三版 pytest 与边界探针记录

- 运行日期：2026-07-20。
- pytest：`20 passed in 4.26s`，现有全部用例通过。
- 默认 `block_size=None`：另行验证两个算子在 `N=513` 时均与 PyTorch reference 一致。
- Ruff：`ruff check` 仍报告 4 项；`ruff format --check` 显示实现文件待格式化、测试文件已通过。
- 多 GPU 探针：当前环境可见 8 张 GPU。`x@cuda:0`、`y@cuda:1` 未被 wrapper 提前拒绝，进入
  Triton 后报 pointer access `ValueError`。
- 非当前设备探针：当前 device 为 0，而 `x/y@cuda:1` 时，即使二者同设备，直接调用 wrapper
  仍报 pointer access `ValueError`；外层使用 `with torch.cuda.device(x.device)` 后计算通过。
- 配置探针：`block_size=128.0` 因 Python 集合相等语义通过成员检查，随后在
  `tl.arange` 处产生 `CompilationError`。
- 空输入探针：两个算子在 `block_size=0` 时均直接返回空输出，非法配置未被验证。

### 第三轮评审后的实现更新

学习者在第三轮 review 后继续修改了 wrapper，本次阶段性保存前重新执行了定向探针：

- `resolve_block_size` 已增加严格 Python `int` 类型检查；`block_size=128.0` 现在由 wrapper 抛出
  `TypeError`。
- block-size resolver 已移动到空输入早返回之前；空 tensor 配 `block_size=0` 现在由 wrapper
  抛出 `ValueError`。
- AXPBY 已加入 `x.device == y.device` 条件；跨 GPU 输入现在由 wrapper 抛出 `ValueError`，但
  当前消息仍笼统写成“must be CUDA tensors”，尚未指出真正原因是 device 不同。
- 两个 wrapper 的 kernel launch 已放入 `with torch.cuda.device(x.device)`；当前 device 为 0、
  输入均位于 `cuda:1` 的探针正确返回 `cuda:1` 上的 `[2.0, ..., 2.0]`。
- 修改后重新运行现有测试：`20 passed in 4.51s`。
- 上述四项新行为尚未全部写入 pytest，因此 R08/R09 标为“实现已修改、待 R10 固化”，而不是
  直接关闭。

### 旧 strided vector add 练习归档

阶段性保存后，学习者将原本独立位于 `gpu/triton/strided_vector_add.py` 的
`strided_1d_vector_add` kernel 原样移动到 `gpu/triton/lesson01_vector_ops.py`，并删除旧文件，
便于把第一课相关的一维向量 kernel 集中整理。此次变更没有修改该 kernel 的计算逻辑。

当前归档边界：

- 只有 `@triton.jit` kernel，没有 Python wrapper。
- 没有 pytest 覆盖；现有 `20 passed` 不包含该 kernel。
- 尚未正式检查 stride 单位、输入/输出 shape 契约、负 stride、零 stride、地址重叠、空输入、
  launch grid 或非连续 PyTorch view 的端到端行为。
- 因此它当前属于“保存下来的旧练习”，而不是已通过第一课验收的第三个算子。后续若要继续
  完善，应单独定义 wrapper 与测试要求，不与 R07–R10 的当前收尾工作混在一起。
- 归并后复跑现有测试：`20 passed in 4.27s`；Ruff 仍为此前已知的 4 项，未新增诊断。

### 可选性能扩展恢复（2026-07-23）

学习者决定在进入第 02 课前补做练习 3。第 01 课原有的概念、正确性实践和结课判定继续有效；
当前仅重开可选性能扩展，不把已完成状态回退为未完成。

本轮已恢复并核对官方 benchmark 机制以及本地 Triton 3.7.1 的 `do_bench` 实现。练习 3 已按
本节详细契约重新布置，学习者随后提交了第一版
`gpu/triton/lesson01_vector_ops_benchmark.py`，并在
`experiment_results/lesson01/axpby-block-size/` 生成 PNG、CSV 和 HTML。主表覆盖四种规定
size 与四种 block size；完整 review 尚未开始。

第一次向尚不存在的 `save_path` 运行时出现 `FileNotFoundError`，第二次运行成功。Q12 已确认
根因是本地 Triton 3.7.1 在 `_run()` 中先保存 PNG、再在外层 `finally` 创建目录。学习者已预先
创建目录并补上 main guard，正式评审以全新临时目录验证一次运行成功，Q12 关闭。

本轮性能扩展已经暂停在最终轻量评审之后。P01–P06 详见第 9 节；当前状态为：

1. P01 详细数据、P02 尾块实验与复盘、P03 第一轮简报均已验证关闭。
2. P06 的无 CUDA 错误路径已验证关闭。
3. P04 仍需格式化 benchmark 文件；P05 仍有两处 `do_bench` 可选返回类型需要收窄。二者均为
   次要工程质量项，不回退第 01 课已经完成的掌握判定。

## 9. 代码评审与修改闭环

### 第 1 轮评审（2026-07-20）

| 编号 | 严重程度 | 发现 | 建议 | 状态 |
| --- | --- | --- | --- | --- |
| R01 | 阻塞 | 从仓库根目录收集测试时，`import lesson01_vector_ops` 导致 `ModuleNotFoundError` | 改为 `from gpu.triton import lesson01_vector_ops as ops` | 已关闭 |
| R02 | 阻塞 | 测试逻辑位于模块顶层且只打印误差，pytest 不会收集 test item，错误数值也不会令测试失败 | 改成 `test_*` 函数并使用 `torch.testing.assert_close` | 已关闭 |
| R03 | 阻塞 | 两个 wrapper 都没有空 tensor 早返回，也不允许调用者从规定集合传入 `block_size` | 新增并验证关键字参数；`numel()==0` 时不 launch | 基本完成，验证顺序待改 |
| R04 | 主要 | `axpby` 以 Python `assert` 检查部分条件且没有拒绝 CPU；`threshold_square` 只检查 contiguous | 用明确异常完整验证 1-D、CUDA、float32、shape/device/dtype 与 contiguous | 已修改，同设备约束待补 |
| R05 | 主要 | `threshold_square_kernel` 的 masked load 未按练习要求显式提供 `other` | 为无效 lane 指定定义良好的值，并保留 boundary mask 与 write mask | 已关闭 |
| R06 | 次要 | 模块导入时查询 active driver，但所得 `DEVICE` 未使用；这会妨碍无 GPU 环境完成 pytest 收集/跳过 | 删除未使用的 import-time driver 查询 | 已关闭 |
| R07 | 次要 | Ruff 报告导入顺序、两个 `lambda` 赋值、未使用的 test import、长行和格式问题 | 理解诊断后手工整理，再运行 Ruff 检查 | 待修改 |

pytest 入门、完整测试骨架和命令说明见
[pytest GPU Kernel 测试参考](../references/pytest-gpu-kernel-tests.md)。该参考沿用当前函数名和参数
顺序，但增加了练习契约要求的 `block_size` 关键字参数。

本轮执行证据：

```text
pytest --collect-only ...
  ERROR: ModuleNotFoundError: No module named 'lesson01_vector_ops'
  no tests collected

ruff check ...
  Found 7 errors.

ruff format --check ...
  2 files would be reformatted
```

这些结果不表示 kernel 数值错误；它们表示测试尚未进入可执行的 pytest 正确性验证阶段。

### 第 2 轮评审（2026-07-20）

#### 已确认的进展

- R01 已关闭：测试改用完整包路径，仓库根目录能够成功导入。
- R02 已关闭：pytest 成功收集 20 个用例，参数化名称清楚，数值比较使用
  `torch.testing.assert_close`，失败能够令命令返回非零状态。
- AXPBY 和条件平方的 15 个正常输入用例全部通过，当前没有发现可观察的 kernel 数值错误。

#### 五个失败的共同根因

当前 wrapper 的逻辑是：

```python
if block_size is not None:
    # 根据 n_elements 重新赋值 block_size
```

因此，只要调用者提供任何值，包括 `0`、`64`、`127` 和 `2048`，该值都会先被静默覆盖成
128/256/512/1024 中的一个值。测试看到的是一次成功计算，自然报告 `DID NOT RAISE`。同样，
正常数值测试通过只能证明覆盖后的配置算对，不能证明调用者请求的 block size 真正被采用。

如果本课采用“调用者选择”的接口，应让默认值为一个合法配置，并直接验证成员关系：

```python
ALLOWED_BLOCK_SIZES = {128, 256, 512, 1024}

if block_size not in ALLOWED_BLOCK_SIZES:
    raise ValueError(
        f"block_size must be one of {sorted(ALLOWED_BLOCK_SIZES)}, got {block_size}"
    )
```

如果希望同时保留自动选择，则只能在 `block_size is None` 时运行 heuristic；调用者明确传值时
仍必须验证并尊重该值。这两种 API 只能选定一种清楚的语义，不能把“已提供”和“自动选择”
混在同一个分支中。

CPU 用例中，`x.device == y.device` 对两个 CPU tensor 也成立，所以现有 assert 全部通过，调用
继续进入 Triton。Triton 随后抛出 `ValueError: Pointer argument cannot be accessed from Triton
(cpu tensor?)`。`pytest.raises` 已经捕获到正确异常类型，但 `match="CUDA"` 没有匹配底层消息，
所以最终报告 `Regex pattern did not match`。正确修复点在 wrapper：launch 之前显式检查
`x.device.type == "cuda"` 和 `y.device.type == "cuda"`，并由 wrapper 抛出包含 `CUDA` 的清晰
`ValueError`。

#### 仍需一并完成的项目

1. `numel() == 0` 时直接返回已分配的空输出。当前空用例通过，只证明返回值正确，并不能证明
   满足“不 launch 零大小 grid”的实现约束。
2. `threshold_square` 也应验证 1-D、CUDA、float32 和 contiguous，并采用相同的 block-size
   策略。
3. `threshold_square_kernel` 的 masked load 按练习要求补上显式 `other`。
4. 删除未使用的 import-time `DEVICE` 查询。
5. 可直接构造 `grid = (triton.cdiv(n_elements, block_size),)`，并以
   `BLOCK_SIZE=block_size` 关键字启动 kernel；这样也会消除 Ruff 的两个 E731。
6. 本轮 Ruff 仍报告 4 个问题；实现文件待格式化，测试文件已经符合 formatter。

第二轮后请再次运行：

```bash
uv run --frozen pytest -vv gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff format --check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py
```

### 第 3 轮评审（2026-07-20）

#### 总体判断

现有 20 个 pytest 用例全部通过，核心索引、tail mask、条件 masked store、空输入早返回和已覆盖的
错误输入均表现正确。当前还不能关闭本课实践：多 GPU 设备语义、block-size 类型/验证顺序以及
练习要求的完整错误输入矩阵仍有可复现缺口，Ruff 也尚未通过。

#### 新增评审意见

| 编号 | 严重程度 | 发现 | 建议 | 状态 |
| --- | --- | --- | --- | --- |
| R08 | 阻塞 | `axpby` 只检查两个输入都是 CUDA，没有检查 `x.device == y.device`；同时两个 wrapper 都未保证在输入 device 上 launch。同卡但位于非当前 GPU、或跨 GPU 输入时均已复现底层 pointer error | 先拒绝不同 device；随后用 `with torch.cuda.device(x.device):` 包住 kernel launch，使同一非当前 GPU 的合法输入也能工作 | 实现已修改，待测试与消息优化 |
| R09 | 主要 | 空输入在调用 `resolve_block_size` 前返回，所以显式非法配置被忽略；`128.0` 又会因与整数相等而通过 set membership，最终产生编译错误 | 在空输入早返回前完成配置验证；明确要求 Python `int`，非法类型抛 `TypeError`，非法取值抛 `ValueError` | 实现已修改，待测试固化 |
| R10 | 主要 | 当前测试尚未覆盖默认 heuristic、threshold wrapper 的错误输入、shape/dtype/contiguous、空输入配非法配置以及多 GPU 行为 | 补充结构化异常测试；多 GPU 用例用 `skipif(torch.cuda.device_count() < 2, ...)` | 待修改 |

#### 代码质量意见

- `grid` 可直接写为 `(triton.cdiv(n_elements, block_size),)`，因为 block size 已在 host 端解析；
  kernel launch 使用 `BLOCK_SIZE=block_size` 可明确标出 meta-parameter，并消除两个 E731。
- wrapper 的 `block_size` 建议设为仅关键字参数并补齐 `int | None` 类型；`alpha`、`beta`、
  `threshold` 也可补上标量类型标注。
- 两个公开 wrapper 应按任务要求添加简短 docstring。错误消息中的单复数可以顺便整理。
- 不直接执行自动修复；先按 Ruff 诊断手工整理，再运行 formatter/check 验证。

#### 推荐新增测试

1. 两个算子各自省略 `block_size`，验证 heuristic 默认路径。
2. 空 tensor 加 `block_size=0`，约定仍然拒绝非法配置。
3. `block_size=128.0`，期望 wrapper 抛清晰 `TypeError`，不能进入 Triton 编译。
4. AXPBY 的 shape 不同、dtype 不同、二维、非连续输入。
5. threshold wrapper 的 CPU、二维、非 float32、非连续与非法 block size。
6. 有两张 GPU 时：不同 device 必须被拒绝；同一张非当前 GPU 必须成功并返回在该设备上的结果。

### 第 4 轮评审（2026-07-22）

#### 本轮提交与执行证据

学习者已开始扩充 R10：为两个 wrapper 增加默认 `block_size=None` 用例、空输入与非法配置组合，
并为 AXPBY 增加 shape、dtype 和二维输入用例。当前环境可见 8 张 A100-SXM4-80GB，driver 为
580.159.03；本轮执行结果为：

```text
pytest：收集 43 项，41 passed、2 failed，用时 2.55s
ruff check：4 errors（两个 import 排序、两个 E731 lambda 赋值）
ruff format --check：两个文件均待格式化
```

两项 pytest 失败都来自同一个测试契约不一致：`block_size=1.2` 会按 wrapper 的既定设计抛出
`TypeError`，而两组空输入测试统一期待 `ValueError`。这反而证明配置验证确实发生在空输入早
返回之前，不是 kernel 数值错误。

#### 评审意见与状态迁移

| 编号 | 严重程度 | 发现与证据 | 修改方向 | 状态 |
| --- | --- | --- | --- | --- |
| R07 | 次要 | Ruff 仍报告 4 项，formatter 认为实现与测试文件都需整理 | 手工整理 import、grid 和空格/换行，再运行 check 与 format check | 待修改 |
| R08 | 阻塞 | 手工探针再次确认跨卡输入由 wrapper 拒绝，同一非当前卡输入可成功；但跨卡消息仍写成“must be CUDA tensors”，且没有 pytest | 分开表达“必须是 CUDA”与“必须同 device”，再固化两种多 GPU 行为 | 实现已手工验证，待测试与消息优化 |
| R09 | 主要 | 空输入配非法整数已由测试验证；浮点配置正确抛 `TypeError`，但测试错误期待 `ValueError` | 按“类型错误 / 值错误”分别声明预期异常，并同步测试参数类型 | 需进一步修改测试 |
| R10 | 主要 | 默认 heuristic 的四个选择区间已被覆盖；仍缺 AXPBY 非连续输入、threshold 的 CPU/二维/非 float32/非连续输入以及两种多 GPU 用例，文件末尾目前只有占位注释 | 把每个占位项变成独立、可失败的测试；多 GPU 测试在设备数不足时跳过 | 修改中 |
| R11 | 主要 | 两个 `block_size=1.2` 用例导致当前测试集失败：实现抛 `TypeError`，测试期待 `ValueError` | 参数化预期异常类型，或将类型错误与非法整数值拆成两组测试 | 待修改 |

本轮没有修改学习者实践代码。R08 只达到“实现已观察正确”，R09/R10 也仍未达到可关闭状态；
待上述测试补齐且全部通过后再关闭相应发现。

### 第 5 轮评审（2026-07-22）

#### 本轮成果与执行证据

学习者已补齐默认配置、异常类型、非连续输入、threshold 输入契约和多 GPU 测试，并将 callable
grid 改成已解析 block size 对应的直接 tuple。完整 GPU 测试结果为：

```text
pytest：收集 50 项，50 passed，用时 3.19s
非连续输入探针：shape=(5,)，stride=(2,)，is_contiguous=False
ruff check：3 个 E501，均为测试函数签名超过 100 列
ruff format --check：实现与测试两个文件仍需格式化
```

额外聚焦运行 BasedPyright 得到 125 个错误，但这不作为本课新增失败门槛：项目配置只将
`leetcode/python` 与 `tests/python` 纳入常规 BasedPyright，显式检查 Triton 文件会因当前 Triton
Python API 类型信息大量为 unknown 而产生噪声。wrapper 自身的 host 类型标注仍可作为代码质量
改进，但本课按既定 pytest 与 Ruff 验收。

#### 评审意见与状态迁移

| 编号 | 严重程度 | 发现与证据 | 修改方向 | 状态 |
| --- | --- | --- | --- | --- |
| R07 | 次要 | import 区块与 E731 已修复；仍有 3 个超长测试签名，两个文件均未通过 formatter check | 运行 formatter 处理机械排版，再复跑 Ruff check/format check | 学习者已修改，仍需收尾 |
| R08 | 阻塞 | 跨 GPU pytest 通过；错误消息已包含 same-device 要求；同一非当前 GPU 行为此前手工探针及本轮正常环境测试均通过 | 无 | 已验证并关闭 |
| R09 | 主要 | 两个 wrapper 的空输入非法整数和浮点类型用例全部通过，证明配置验证先于空输入早返回 | 无 | 已验证并关闭 |
| R10 | 主要 | 要求的输入矩阵均已转化为 pytest 且 50 项全通过；但“非当前 GPU”用例没有自行建立此前提 | 修复 R12 后即可关闭 | 需进一步修改测试 |
| R11 | 主要 | 参数表已携带预期异常类，`1.2 -> TypeError`、非法整数值 `-> ValueError` 均通过 | 无 | 已验证并关闭 |
| R12 | 主要 | `test_axpby_same_no_active_gpu` 固定使用 `cuda:1`，却未保证当前 device 不是 1；强制 `torch.cuda.set_device(1)` 后该测试仍通过，说明它可能没有测试名称声称的条件 | 根据 `torch.cuda.current_device()` 动态选择另一张卡，并断言输入卡确实不是当前卡 | 待修改 |
| R13 | 次要 | shape 类型注解与数据不一致：`tuple[int]` 不能表达二维/任意维 shape；若想表达一维 shape，`(10)` 实际是整数而非 tuple | 使用 `tuple[int, ...]`，一元素 tuple 写成 `(10,)`；参数集合类型也应与实际结构一致 | 待修改 |

#### 非阻塞建议

- 默认 heuristic 的数值测试能证明各尺寸均正确运行，但不能观察 resolver 实际选择了哪个
  block size；可直接参数化 `resolve_block_size(n, None)` 的预期返回值，使四个分支的配置选择也
  成为可回归行为。
- 非连续用例可在调用 wrapper 前显式断言 `not x.is_contiguous()`，让测试夹具失效时更易定位。
- 实践契约要求公开 wrapper 保留简短 docstring；可在本轮 Ruff 收尾时一并补齐。

本轮没有修改学习者实践代码。当前已没有阻塞级发现；R07、R12、R13 收尾并复跑验证后，可以
将课程从“评审中”推进到“待验收”。

### 第 6 轮评审（2026-07-22）

#### 验证结果

学习者已修正非当前设备测试的前置条件、shape 类型标注与一元素 tuple，加入非连续布局断言，
并为默认 block-size heuristic 增加 8 个直接单元测试。执行结果：

```text
pytest：收集 58 项，58 passed，用时 3.79s
ruff check：All checks passed
ruff format --check：2 files already formatted
反向设备探针：先强制 current device=1，非当前 GPU 定向测试仍通过
```

反向设备探针中，测试根据 `torch.cuda.current_device()` 动态选择下一张卡，因此不再依赖进程
默认设备为 0。resolver 测试覆盖 511/512、1023/1024、2047/2048 三组阈值两侧，能直接观察
heuristic 的配置选择，而不仅是最终数值结果。

#### 评审意见与状态迁移

| 编号 | 严重程度 | 验证结论 | 状态 |
| --- | --- | --- | --- |
| R07 | 次要 | 三个超长签名已格式化；lint 与 formatter 均通过 | 已验证并关闭 |
| R10 | 主要 | 默认路径、输入契约、非连续、异常顺序和多 GPU 矩阵均已由 pytest 固化 | 已验证并关闭 |
| R12 | 主要 | 非当前设备由当前设备动态推导并显式断言；current=1 的反向探针通过 | 已验证并关闭 |
| R13 | 次要 | shape 改用 `tuple[int, ...]`，一维 shape 均使用 `(10,)` | 已验证并关闭 |
| R14 | 次要 | 原实践契约要求公开 wrapper 保留简短 docstring，当前 `axpby` 与 `threshold_square` 仍没有 docstring | 待最终关闭前补齐，不阻挡概念验收 |

此前所有阻塞与主要发现均已关闭，实践代码的正确性、边界和格式证据可复现。课程状态由
“评审中”推进到“待验收”；R14 可与最终知识总结一并收尾。

### 性能扩展第 1 轮评审（2026-07-24）

#### 总体判断与验证证据

第一版已正确构造 `size × block_size` 实验矩阵，输入分配位于 `do_bench` 外，GB/s 公式和
p20/p50/p80 到吞吐区间的反向映射正确。图像包含四条曲线与阴影区间，现有 wrapper 正确性测试
全部通过。首次目录问题已修复并用全新路径验证。

本轮环境为 8 × NVIDIA A100-SXM4-80GB、driver 580.159.03、Python 3.12.13、Torch
2.13.0+cu130、Torch CUDA runtime 13.0、Triton 3.7.1，current device 为 0。执行证据：

```text
pytest：58 passed in 4.29s
ruff check：All checks passed
ruff format --check：benchmark 文件待格式化
basedpyright（显式聚焦）：5 errors
全新临时 save_path：运行前不存在，一次运行后生成 PNG、CSV、HTML
```

独立复测的中心 GB/s 为：

| size | BS=128 | BS=256 | BS=512 | BS=1024 |
| ---: | ---: | ---: | ---: | ---: |
| `2**12` | 5.33 | 6.00 | 5.33 | 6.86 |
| `2**16` | 96.00 | 96.00 | 109.71 | 96.00 |
| `2**20` | 819.20 | 819.20 | 819.20 | 768.00 |
| `2**24` | 1489.45 | 1585.55 | 1611.54 | 1624.86 |

这些数字是本轮观察，不是最终性能结论。它们与学习者保存结果在小尺寸排名上存在变化；大尺寸
趋势较接近，但 BS=512 与 BS=1024 的差距仍需结合数值化区间判断。

#### 评审发现

| 编号 | 严重程度 | 发现与证据 | 修改方向 | 状态 |
| --- | --- | --- | --- | --- |
| P01 | 主要 | `do_bench` 得到 p20/p50/p80 耗时后只返回 GB/s 三元组；当前 Triton CSV 又只保存中心曲线，因此没有数值化延迟和区间。`warmup`/`rep` 也依赖未记录的默认值 | 显式声明并传入 warmup/rep；为每个配置保存 p20/p50/p80 ms 以及对应 GB/s 下界/中心/上界 | 已验证并关闭 |
| P02 | 主要 | 主矩阵只有四个 2 的幂尺寸，契约要求的 `2**20 + 17` 尾块测量不存在 | 单独测量尾块尺寸并与 `2**20` 比较，不必把两个相邻点挤进主图 | 已验证并关闭 |
| P03 | 主要 | 约定的 `attachments/01-vector-add/axpby-benchmark.md` 尚不存在；环境、首次预测、运行命令、结果分析和限制均未归档 | 保留当前原始产物并建立结构化报告；不得事后把新预测伪装成首次运行前预测，可先记录遗漏，再对尚未运行的尾块实验做前置预测 | 第一轮简报已通过轻量评审并关闭；保留 4 项非阻塞措辞建议 |
| P04 | 次要 | `ruff format --check` 明确报告 benchmark 文件需要格式化 | 先阅读 diff 或运行 formatter，再复跑 check 与 format check | 待修改 |
| P05 | 次要 | `size` 实际为 `int` 却标成 `tuple[int]`；未知 provider 会使 `ms/min_ms/max_ms` 未绑定；Torch 分支在固定 `provider="triton"` 的核心实验中不可达。聚焦 BasedPyright 共报 5 项 | 修正 size 类型；删除暂不用的 provider 分支，或用穷尽的 `if/elif/else` 明确拒绝非法值；在 Triton 返回类型不精确处做最小、可解释的类型收窄 | size 与穷尽分支已修复；剩余两处 `"None" is not iterable`，待收窄 `do_bench` 返回值 |
| P06 | 次要 | 脚本默认使用当前 `"cuda"`，合法 GPU 环境下设备一致；但无 CUDA 时没有练习契约要求的主动、清晰错误 | 在入口处验证 CUDA 可用，并明确当前 benchmark device；不要把检查放进计时 callable | 已验证并关闭 |

#### 已验证通过的部分

- `Path.mkdir(parents=True, exist_ok=True)` 位于 `.run()` 前，首次保存问题已关闭。
- main guard 存在，import 模块不会自动运行 benchmark。
- 四种 block size 与四种主尺寸形成完整笛卡尔积。
- 随机输入创建、常量与 correctness 工作不在被计时 callable 中。
- AXPBY 两读一写的有效字节公式正确，吞吐下界使用 p80、上界使用 p20。
- 没有在 pytest 中加入固定性能阈值；58 个 correctness tests 全部通过。

本轮没有修改学习者 benchmark 或测试代码。P01–P03 是完成性能扩展前的主要证据缺口；P04–P06
属于收尾质量项。完成修改后进入第 2 轮性能评审。

#### P01 定向复审（2026-07-24）

学习者新增冻结的 `BenchmarkRecord`、显式 `WARMUP_MS=25` / `REP_MS=100`、全量分位数和带宽
字段，以及独立 `axpby_block_size_detailed.csv`。collector 在每次 `.run()` 前清空，CSV 在
测量结束后覆盖写入。

本轮通过临时目录连续执行两次完整主矩阵，每次均验证：

```text
记录数：16
唯一 (size, block_size)：16
warmup_ms：全部为 25
rep_ms：全部为 100
p20_ms <= p50_ms <= p80_ms：16/16
gbps_lower <= gbps_p50 <= gbps_upper：16/16
第二次执行后仍为 16 行，无重复累积
```

另对学习者保存的 16 行 detailed CSV 逐项按 float32 的
`3 * size * 4 bytes / runtime` 复算，共 48 个 lower/center/upper GB/s 均一致。P01 达到
`learner-revised -> verified -> closed`。

非阻塞代码质量备注：当前 `assert condition, RuntimeError(...)` 实际失败时抛出
`AssertionError`，`RuntimeError` 只是 assertion message；后续处理 P04/P05 时可改成普通
`if ...: raise RuntimeError(...)`，但不影响本轮 P01 数据完整性。

#### P02 预测与结果定向复审（2026-07-24）

学习者先建立 `docs/triton-learning/attachments/01-vector-add/axpby-benchmark.md`，记录尾块预测；
实现将单配置逻辑提取为共享的 `measure_axpby`，主矩阵与尾块分别保留标准
`perf_report/Benchmark` adapter。尾块产物包含 `2 sizes * 4 block sizes = 8` 行 detailed CSV，
数据字段与 P01 一致。

学习者保存结果的 p50 变化为：

| block size | exact p50 (µs) | tail p50 (µs) | 延迟变化 | 有效 GB/s 变化 |
| ---: | ---: | ---: | ---: | ---: |
| 128 | 15.360 | 15.360 | 0.00% | 约 +0.002% |
| 256 | 16.384 | 15.360 | -6.25% | +6.67% |
| 512 | 14.336 | 16.384 | +14.29% | -12.50% |
| 1024 | 15.360 | 16.384 | +6.67% | -6.25% |

当前环境中的所有耗时都是 1.024 µs 的整数倍；在约 14–18 µs 的 kernel 上，一个观测到的
计时台阶就对应约 6%–7%，
两个台阶约 13%–14%。因此原预测用“5% 变化”作为反证门槛低于当前观察到的单台阶粒度，不适合
直接解释为稳定性能差异。

评审另用临时目录独立运行三轮，p50 延迟变化如下：

| block size | 学习者保存结果 | 复测 1 | 复测 2 | 复测 3 |
| ---: | ---: | ---: | ---: | ---: |
| 128 | 0.00% | -5.88% | +6.67% | -6.25% |
| 256 | -6.25% | -5.88% | -5.88% | +6.25% |
| 512 | +14.29% | 0.00% | 0.00% | +6.67% |
| 1024 | +6.67% | +6.67% | +6.25% | +13.33% |

据此对预测逐项校准：

1. “总体影响很小、容易被运行波动覆盖”对 128/256/512 基本得到支持；变化方向和排名不稳定。
2. “1024 可能更敏感”有一定支持：三轮独立复测及学习者结果中，1024 尾块延迟都增加。但样本
   仍少，只能写成当前环境的观察，不能推广成普遍规律。
3. “有效 GB/s 肯定下降，因为处理了完整一块数据”被推翻。masked-out lane 不执行实际
   load/store，因此不会产生整块有效 DRAM 流量；尾 program 仍有逻辑 lane、predication 和调度
   成本，但有效带宽分子只增加 17 个有效元素。如果时间落在同一计时台阶，GB/s 反而会微升约
   `17 / 2**20 = 0.00162%`。
4. “所有 program 并行执行”需要修正为“program 相互独立、可并行调度”。GPU 驻留资源有限，
   数千个 program 会分批执行；额外一个 program 是否增加关键路径取决于 SM 调度波次、占用和
   运行波动，不能仅由 `+1 / program_count` 线性推出延迟。

标准装饰器方案本身有效，共享测量函数也消除了核心代码复制；尾块图因两个 x 值只差 17 而较难
阅读，结论应以 detailed CSV 表为主。

证据 provenance 仍有一个待说明点：文件系统显示尾块结果时间早于预测文档最终落盘时间约 33
秒。这可能只是编辑器延迟保存，但仓库证据无法机械证明预测先于结果。实验报告应如实备注该
歧义；以后在运行命令前先保存预测文件。

P02 的实现和原始数据已达到要求。本定向复审时学习闭环尚差学习者自己的“实验后复盘”：逐条
说明哪些预测得到支持、哪些被推翻、原心智模型哪里需要修正，以及最终结论的适用边界。学习者
随后提交了第一版复盘，评审结果如下。

#### P02 实验后复盘第 1 轮评审（2026-07-24）

复盘已正确识别：program 数量不能线性换算成耗时，额外 program 可能因有限驻留资源进入后续
调度波次；“有效 GB/s 肯定下降”的原预测不成立；约 15 µs 的单次 kernel 上，当前环境观测到的
1.024 µs 量化步长足以造成约 6%–7% 的比值跳变。评审重新核对 8 行尾块 CSV，四组 p20–p80
区间均重叠，保存结果的 p50 延迟变化仍为 `0.00% / -6.25% / +14.29% / +6.67%`。

| 编号 | 严重程度 | 发现与证据 | 修改方向 | 状态 |
| --- | --- | --- | --- | --- |
| P02-R1 | 阻塞 | 报告 30–33 行把 false lane 不访存写成“可能经 GPU 调度优化掉冗余读写”，并用它解释有效 GB/s。Triton 语义是 false lane 不访问对应地址；物理 DRAM transaction 仍有 sector/cache 粒度，当前比值无法证明实际 DRAM 字节数 | 分开说明 lane 级 mask 语义、物理内存事务和 `effective_bytes / time`；把 GB/s 上升归因限定为有效分子与离散/波动分母 | 待学习者修改 |
| P02-R2 | 主要 | 报告 21–27 行事前规定延迟超出 5% 或 GB/s 上升即反证，结果两项都发生，却在事后以门槛过严为由继续判定“基本支持”；BS=512 的 +14.29% 也不是“略微超出” | 先按原判据承认定量预测被推翻，再单独说明该判据为何设计不佳，以及跨轮方向反转对“噪声主导”这一宽泛假设提供了什么证据 | 待学习者修改 |
| P02-R3 | 主要 | 报告没有评价“BS=1024 可能更敏感”的独立预测；学习者结果及三轮复测均为尾块更慢，但只有一两个计时台阶且区间重叠 | 写成当前环境中的有限支持；不得由 `+1 / program_count` 线性推出因果或推广成通用规律 | 待学习者修改 |
| P02-R4 | 主要 | 报告 38–39 行笼统结论为延迟和 GB/s “变化不大”，未覆盖 BS=512 的 +14.29% 和 BS=1024 四轮同向现象，也没有实验边界 | 按 block size 分层总结；限定 A100、当前软件栈、float32、两个 N、四个 block size 与单 launch `do_bench`，明确能与不能支持的结论 | 待学习者修改 |
| P02-R5 | 主要 | 报告 3–8 行断言预测在运行前完成，但已有审计记录显示尾块 CSV 比预测文件最终落盘早约 33 秒；可能是编辑器延迟保存，仓库证据无法证明顺序 | 保留学习者回忆，同时披露 mtime 冲突与证据限制；以后先保存预测再执行实验 | 待学习者修改 |
| P02-R6 | 次要 | 报告 35–36 行将 program 描述为各自占用“一部分 SM”，并把显存与寄存器并列为 per-program 驻留资源 | 表述为编译后的 warps、寄存器和共享内存决定 program 在某个 SM 上的驻留；多个 program 可同时驻留，资源不足时分波次 | 待学习者修改 |

本轮状态为 `learner-revised -> needs-more-work`。P02 尚未关闭；先修正 P02-R1–R6，再复审
学习者自己的结论。P03 的环境、命令、完整数值结果与限制归档仍是独立待办，不因本轮复盘而自动
关闭。

#### P02 实验后复盘第 2 轮评审（2026-07-24）

学习者按第一轮意见修订复盘，并在 Q18 后重新说明 masked lane。第二轮逐项结果：

| 编号 | 验证结论 | 状态 |
| --- | --- | --- |
| P02-R1 | 报告 34–36 行已经正确写出 predicate=false 时不执行对应读写、active lane 请求仍受 32-byte transaction 粒度影响，尾 program 仍保留地址计算与调度等成本；核心错误模型已纠正。但第 34 行“可能并不发生”与后句的确定语义冲突，第 31 行也仍缺 `effective_bytes / time` 的直接数学因果 | `learner-revised -> needs-more-work`；严重度由阻塞降为主要 |
| P02-R2 | 明确先按原 5% 判据承认预测被推翻，再把计时台阶大于阈值识别为实验设计缺陷，没有事后改判 | 已验证并关闭 |
| P02-R3 | 明确将 BS=1024 四轮同向结果写为当前环境中的有限支持，并禁止推广为普遍规律 | 已验证并关闭 |
| P02-R4 | 按 BS=128/256/512 与 BS=1024 分层总结，并限定 A100、软件栈、dtype、尺寸和测量方法 | 已验证并关闭 |
| P02-R5 | 学习者说明预测先记录在仓库外，实验后才复制到当前文档，并要求不再追究文件 mtime；该来源说明被接受，不作为学习门槛 | `rejected-with-rationale` |
| P02-R6 | 改为由编译后 warps、寄存器和共享内存决定 SM 驻留，多个 program 可同时驻留、资源不足时分波次 | 已验证并关闭 |

P02 现在只剩 P02-R1 的两个窄修改点：

1. 将“masked-out lane 的显存行为实际上**可能**不发生”改成确定语义：mask/predicate 为 false
   时，对应地址的 load/store 不发生；地址、谓词和部分算术计算仍可能发生。
2. 在有效 GB/s 结论中明确
   `tail_gbps / exact_gbps = (N_tail / N_exact) * (t_exact / t_tail)`；`N+17` 令有效字节分子
   增加，只要时间没有按更大比例增加，比值就不会下降，甚至会升高。这不证明实际 DRAM 流量或
   物理带宽提高。

完成后只需定向复审这两处即可决定关闭 P02。另有非阻塞文字勘误：报告第 27 行两处“微妙”应为
“微秒”。

#### P02 实验后复盘最终评审（2026-07-24）

学习者完成最后两处修改：

1. 报告 35–38 行明确说明 `mask/predicate=False` 时对应地址的 load/store 确定不发生，同时
   地址、谓词和部分算术计算仍可能发生；active lane 的请求还受 32-byte memory transaction
   粒度影响，尾 program 也没有免除调度等成本。
2. 报告 31–33 行补上
   `tail_gbps / exact_gbps = (N_tail / N_exact) * (t_exact / t_tail)`，说明 `N+17` 增加有效
   字节分子，只要耗时没有按更大比例增加，有效 GB/s 就可能不降或上升；同时明确该比值不能证明
   真实 DRAM 流量或物理带宽提高。
3. “微妙”已更正为“微秒”。

P02-R1 达到 `learner-revised -> verified -> closed`。结合上一轮状态，P02-R1–R4/R6 均已验证
关闭，P02-R5 为 `rejected-with-rationale`，不再构成门槛。P02 尾块实验的实现、原始数据、
事前预测、反证处理、机制反思和适用边界现已形成完整闭环，P02 正式关闭。

没有新的阻塞或主要问题。仅有非阻塞编辑建议：报告第 36 行存在一个重复句号，且“类似
if-else”可进一步写成“编译为 guard predicate”，以避免让读者误以为 PTX 必然产生真实分支；
这不影响当前概念结论或 P02 关闭。

#### P03 实验档案补全任务（2026-07-24）

P03 不要求重新运行或改写 benchmark；目标是把已有预测、24 行详细结果、分析和限制整理成一份
离开课堂主记录后仍可独立理解和复现的实验报告。当前 CSV/PNG/HTML 保持原样；如果后续主动重跑，
必须写入新的时间戳目录，不能覆盖本轮证据。

学习者在 `docs/triton-learning/attachments/01-vector-add/axpby-benchmark.md` 中补齐：

1. **标题、目的与范围**：说明比较 AXPBY 的四种 block size，主矩阵为四个规模，尾块实验为
   `2**20` 与 `2**20 + 17`；明确测量对象是现有 Python wrapper。
2. **环境**：日期、current device 0 的 A100-SXM4-80GB、driver 580.159.03、Python 3.12.13、
   Torch 2.13.0+cu130、Torch CUDA runtime 13.0、Triton 3.7.1，以及 float32、
   `alpha=1.234`、`beta=2.345`。系统虽有 8 张同型号 GPU，本轮只测 current device。
3. **方法与命令**：记录 correctness 和 benchmark 的完整命令，写明
   `warmup=25 ms`、`rep=100 ms`、`quantiles=[0.5, 0.2, 0.8]`、两读一写的有效字节公式、
   p80/p50/p20 到 GB/s 下界/中心/上界的反向关系，以及 `do_bench` 的 GPU event 测量边界。
4. **完整结果**：分别给出主矩阵 16 行和尾块 8 行。推荐列为
   `size | block_size | p20/p50/p80 (µs) | lower/p50/upper (GB/s)`；报告中可合理舍入，但需链接
   detailed CSV 作为精确 canonical data，并链接对应 PNG/HTML。
5. **五项分析**：逐项回答实践契约中的问题：各规模最快配置与区间重叠、规模增长与平台区、
   尾块结论、默认 `resolve_block_size` heuristic 的证据边界、GPU event 与 CPU wall-clock 的
   区别。主矩阵未保留事前预测是程序性缺口，必须继续如实记录，不能补写成事前预测。
6. **限制**：至少说明单机单设备/一次保存运行、当前环境约 1.024 µs 的经验计时量化、
   p20–p80 不是置信区间、有效 GB/s 不是硬件 DRAM 计数、wrapper 包含 output allocation、
   当前只测 float32 和有限尺寸、尚无 Torch 或 kernel-only 对照。

结果分析必须区分“保存数据直接显示的事实”“对机制的解释”和“证据不足时的限制”。判断两个
配置能否区分时，不只比较 p50 排名，还要比较它们的 p20–p80/GB/s 区间是否重叠；只有一个最大
尺寸点时，不得把“开始更接近带宽受限区”写成“已经证明到达稳定平台”。

验收条件：

- 环境、命令、配置、24 行数据、五项分析、限制和原始产物链接齐全；
- 表中 µs/GB/s 单位和上下界方向正确；
- 保留错误预测、反证过程与 P02 复盘，不事后美化；
- 不从有效 GB/s 反推实际 DRAM 流量，不把一次 A100 结果推广为通用最优 block size。

完成报告后先做 P03 内容复审，再进入 P04–P06 的源码格式、类型和错误路径统一验证。

学习者随后请求先搭建报告框架。现有预测与 P02 复盘原文已迁入完整档案结构，并预置：

- 环境、方法、correctness/benchmark 命令与有效带宽口径；
- 主矩阵 16 行、尾块 8 行结果表及精确 CSV/PNG/HTML 链接；
- 五项分析、限制、事实/推断/不可支持结论分层；
- 产物索引和提交前检查清单。

框架只提供字段、问题和 `<待填写>` 占位，没有代替学习者填写结果或实验结论。所有相对链接目标
均已验证存在，原始 benchmark 产物未被覆盖。

##### P03 范围调整（2026-07-24）

学习者指出 55 个占位会把第一轮 Triton 编程学习变成系统 benchmark 研究，负担超过当前目标。
该反馈成立：前述完整报告验收标准和详细框架标记为本轮不再执行，保留在课堂记录中作为一次
范围校准；系统性能研究延期到第二轮专题。

当前 P03 改为简短 benchmark 档案：

- 环境、命令、测量口径、16 个主矩阵 p50 和 4 组尾块对照由现有证据直接预填；
- p20/p50/p80 与精确区间不要求手抄，继续由 detailed CSV 保存；
- 原始预测和已通过评审的 P02 复盘保留；
- 学习者只需填写两段各 3–5 句话的总结：主矩阵观察、benchmark 方法心得；
- profiler、置信区间、cache/CUDA Graph、baseline、autotune 和 heuristic 系统研究均明确延期。

简报中的 16 个主矩阵 p50 已逐项与 CSV 核对，尾块表沿用 P02 已验证数据；原始产物链接均存在。
完成两段总结并通过一次轻量内容复审后即可关闭 P03。

#### P03 第一轮简报最终评审（2026-07-24）

学习者已完成“主矩阵观察”和“Benchmark 方法心得”。总结正确识别了当前采样点中有效 GB/s
随 size 整体增长、block size 的相对表现随规模变化，也说明了 CUDA Event、当前环境的经验
计时量化以及单机短 kernel 结果的限制。在简化后的第一轮学习范围内，没有阻塞或主要问题，
P03 达到 `learner-revised -> verified -> closed`。

以下四项作为非阻塞文字建议保留，没有代替学习者改写原文：

| 编号 | 严重程度 | 评审意见 | 状态 |
| --- | --- | --- | --- |
| P03-R1 | 次要 | “三条 block size 曲线”应为四条 | 已记录，非阻塞 |
| P03-R2 | 次要 | 两段模板 `<待填写>` 提示仍留在最终简报中 | 已记录，非阻塞 |
| P03-R3 | 次要 | 除了不同 size 下排名变化，还可明确一次 p50 会受采样与当前计时量化影响，不能确定稳定排名 | 已记录，非阻塞 |
| P03-R4 | 次要 | 有效 GB/s 按逻辑有效字节数统一比较；它不计 masked 尾 lane，但这不等于测得真实 DRAM 流量或证明硬件消除了某类“无效数据干扰” | 已记录，非阻塞 |

完整评审已同时写入
[AXPBY Benchmark 简报](../attachments/01-vector-add/axpby-benchmark.md#5-第一轮简报评审2026-07-24)。
本次只关闭第一轮简报，不扩大为第二轮系统性能研究。

#### P04–P06 暂停前统一验证（2026-07-24）

本轮对学习者代码保持只读，执行：

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --frozen python -m pytest -q \
  -p no:cacheprovider gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py gpu/triton/lesson01_vector_ops_benchmark.py
uv run --frozen ruff format --check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py gpu/triton/lesson01_vector_ops_benchmark.py
uv run --frozen basedpyright gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py gpu/triton/lesson01_vector_ops_benchmark.py
```

结果：

- correctness：`58 passed in 5.18s`；
- Ruff lint：`All checks passed!`；
- Ruff format：未通过，仅 `lesson01_vector_ops_benchmark.py` 需要格式化，P04 保持开放；
- BasedPyright：剩余两处 `"None" is not iterable`，位于两条 `do_bench` 返回值解包处；
  `size` 类型与非法 provider 穷尽分支已经修好，P05 收敛但保持开放；
- Triton/Torch 两个 provider 的运行时 smoke 均成功且分位顺序正确；
- 模拟无 CUDA 入口时主动抛出
  `RuntimeError: CUDA device is necessary in this benchmark.`，P06 验证关闭；
- 主矩阵 16 条、尾块 8 条 detailed record 的笛卡尔积、分位顺序、有效带宽公式、汇总 CSV、
  PNG magic 和 HTML 图片引用全部一致。

另有一项低优先级命名建议：尾块目录中的详细表仍名为
`axpby_block_size_detailed.csv`。现有文档链接和数据均正确，因此不影响本轮证据；以后可改成
`axpby_tail_block_detailed.csv` 提高辨识度。

后续命名收尾（2026-08-06）：生成函数同时服务主矩阵和尾块实验，而目录名已经区分二者，因此
两个目录中的详细表统一改为 `detailed.csv`；上述段落保留为当时评审的历史记录。

#### P04/P05 恢复复审第 1 轮（2026-07-27）

学习者已格式化 benchmark 文件，并把两处 `do_bench` 直接解包改为先保存返回值、判断
`list` 及长度后再解包。本轮保持实践代码只读，复跑结果如下：

- Ruff check：`All checks passed!`；
- Ruff format：`3 files already formatted`，P04 达到
  `learner-revised -> verified -> closed`；
- BasedPyright：`0 errors, 0 warnings, 0 notes`，原两处 `"None" is not iterable`
  已消失；
- correctness：`58 passed in 4.48s`；
- A100 环境中 Triton/Torch 两个 provider 均运行成功，延迟与带宽分位顺序正确。

当前 Triton 3.7.1 的 `do_bench` 没有显式类型注解；传入
`quantiles=[0.5, 0.2, 0.8]` 时，内部 `_quantile` 按输入顺序返回三元素
`list[float]`，所以正常路径的 `p50_ms, p20_ms, p80_ms` 顺序正确。防御路径仍有以下窄问题：

| 编号 | 严重程度 | 发现与证据 | 修改方向 | 状态 |
| --- | --- | --- | --- | --- |
| P05-R1 | 次要 | 三个延迟先初始化为 `0.0`；若 `do_bench` 返回 `None`、标量或非三元素列表，条件分支不解包，但后续浮点类型断言仍对占位值成立，四类探针最终都误报 `ZeroDivisionError` | 不使用合法的 `0.0` 作为失败哨兵；返回后先显式拒绝非列表或非三元素结果，再解包 | `learner-revised -> needs-more-work` |
| P05-R2 | 次要 | `assert condition, ValueError(...)` 实际抛出 `AssertionError`，而且在 `python -O` 下会被移除；全零延迟还能通过类型和排序检查 | 用普通 `if ...: raise ...` 检查元素类型以及有限正数约束，使异常靠近 `do_bench` 契约边界 | `learner-revised -> needs-more-work` |

因此 P05 的静态类型目标已达到，但约定的运行时三元素检查尚未真正闭合，P05 暂不关闭。下一轮只需
修正这两个 guard，并复跑 Ruff、BasedPyright、58 项正确性测试以及有效/无效返回值探针。

#### P05 恢复复审第 2 轮（2026-07-27）

学习者移除了三个 `0.0` 延迟占位，改为先显式验证 `do_bench` 返回三元素列表，再解包并检查
元素类型、正值和分位顺序。只读探针确认：

- `None`、标量和错误长度列表均在解包前抛出 `AssertionError`；
- 错误元素类型在计算前抛出 `AssertionError`；
- 零值与 NaN 均在延迟约束处抛出 `RuntimeError`；
- 正常三元素列表以及 Triton/Torch 两个真实 provider 均成功。

P05-R1 达到 `learner-revised -> verified -> closed`。P05-R2 中“使用显式分支而非可被优化删除的
`assert`”以及正值检查也已完成；但有限值检查还有一个遗漏：`p80=+inf` 仍满足
`p20 > 0` 和 `p20 <= p50 <= p80`，会被接受并生成 `gbps_lower=0.0`。因此 P05-R2 保持
`needs-more-work`，范围收敛为对三个延迟都执行有限数检查。显式
`raise AssertionError` 不会像 `assert` 语句一样在 `python -O` 下消失；异常类型是否改为
`TypeError`/`RuntimeError` 只作为非阻塞语义建议。

本轮回归继续通过：Ruff check、Ruff format、BasedPyright `0 errors`、58 项 pytest 以及两个
provider smoke 均无回退。补齐 `math.isfinite` 或等价检查后只需复跑上述矩阵和 `+inf` 探针，
即可决定关闭 P05。

#### P05 最终复审（2026-07-27）

学习者为 p20、p50、p80 三个延迟补充 `math.isfinite` 检查。最终只读验证结果：

- Ruff check：`All checks passed!`；
- Ruff format：`3 files already formatted`；
- BasedPyright：`0 errors, 0 warnings, 0 notes`；
- Lesson 01 pytest：`58 passed in 4.60s`；
- Triton/Torch 两个真实 provider 均成功，延迟与有效带宽区间顺序正确；
- `None`、标量、错误长度、错误元素类型、零值、NaN、`+inf` 和 `-inf` 探针均在带宽计算前
  被拒绝；合法三元素浮点列表仍正常生成记录。

P05-R2 达到 `learner-revised -> verified -> closed`，P05 随之关闭。本轮没有新的阻塞、主要或
次要发现；显式异常类型还可按语义细分为 `TypeError`/`RuntimeError`，但只属于可选风格调整。
结合此前状态，P01–P06 已全部关闭，Lesson 01 的可选性能扩展正式完成。

## 10. 掌握验收

### 概念验收

1. 脱离源码画出 `N=10, BLOCK_SIZE=4` 时三个 program 的 offsets 和 mask。
2. 解释 `tl.arange`、`tl.program_id`、`tl.load` 和 `tl.store` 各自处在哪个抽象层。
3. 解释运行时 `n_elements` 和编译期 `BLOCK_SIZE` 的不同职责。
4. 指出官方 wrapper 对 shape、dtype、stride 和空 tensor 的隐含假设。
5. 推导 benchmark 中系数 3 的来源，并解释为什么它叫有效带宽。

#### 概念验收第 1 轮（2026-07-22）

学习者已用自己的话完成第一轮复述，评估如下：

| 项目 | 学习者复述要点 | 评估 |
| --- | --- | --- |
| grid、offsets、mask | 正确给出三个 program 的 offsets 与 `[T,T,F,F]` 尾块 mask，并用向上取整解释 grid=3 | 通过 |
| `BLOCK_SIZE` 心智模型 | 正确说明它是每个 program 的逻辑数据块大小，不是计算单元或 CUDA thread 数量 | 基本通过；“抽象层”术语仍需补讲 |
| masked load/store | 正确说明 false store lane 不写入，因此保留 clone 原值；知道 `other` 防止未定义值传播 | 部分通过；固定形状的原因误归因于“目的地已分配同样空间” |
| 运行时与编译期参数 | 正确区分 `n_elements` 与 `tl.constexpr BLOCK_SIZE`，并指出 autotune 改变 block size 时适合 callable grid | 通过；直接 tuple 的对照结论已在 Q08 实践中验证 |
| stride 迁移 | 正确指出当前裸指针 `+offset` 不支持非连续布局，支持时需传 stride 并按 `offset * stride` 寻址 | 通过 |
| 带宽与异步计时 | 正确解释低计算强度、两读一写的系数 3，以及 CPU wall-clock 在异步 kernel 完成前停止会低估时间 | 通过 |
| 反思 | 识别出曾将 mask 误解为 compaction；现已理解 false lane 仍属于静态形状，未提供 `other` 时值未定义 | 通过 |

需要纠正的关键点：`tl.load` 的结果不是因为预先分配了一块同尺寸“目的地内存”才保持形状。
`offsets` 是形状 `[BLOCK_SIZE]` 的块级 tensor，`x_ptr + offsets` 因此是同形状的 pointer tensor；
`tl.load` 对它逐 lane 求值并返回同形状的块级值。mask 只控制各 lane 是否访问内存及 false lane
取什么值，不改变表达式的静态形状。这个结果主要是 kernel 内部的编译器值，不是 wrapper
预先分配的 output tensor。

概念门槛尚差一次很短的补充复述：说明 `program_id`、`arange`、`load/store` 与实际 GPU
threads/warps 的层次关系，并用 pointer tensor 的形状重新解释 masked load。完成后即可关闭概念
验收；反思维度已经通过。

#### 概念验收第 2 轮（2026-07-22）

学习者补充说明：`program_id` 属于 program-instance 层，`arange` 创建 block-tensor，
`load/store` 对 block-tensor 逐 lane 访存，而 threads/warps 位于编译器映射后的硬件执行层；
mask 只改变各 lane 的访存和值，不改变 load 结果形状。该层次关系正确，概念验收通过。

术语上的最后校准是：load 结果形状由 `x_ptr + offsets` 形成的 **pointer tensor** 形状决定，
不是由完整 PyTorch 输入 `x` 的 shape 决定。例如 `x` 有 N 个元素，而每个 program 的 pointer
tensor 与 load 结果仍只具有 `[BLOCK_SIZE]` 形状。

学习者还正确推导出：若条件 store 不再显式合并 boundary mask，而 masked load 的 `other=0`、
threshold 又为负数，越界 lane 可能错误满足条件并尝试越界写。`other=-inf` 可令“是否越界”编码
进该特定大于比较，但稳健实现仍应显式保留 `boundary_mask & condition`，避免把内存安全依赖于
填充值和谓词的偶然关系。

概念、实践与反思三个维度现已通过。结课只剩 R14：为两个公开 wrapper 补充简短 docstring，
复跑既定检查，并由学习者确认关闭本课。

### 实践验收

- [x] 可以独立重写核心 kernel，而不是逐行照抄
- [x] 覆盖小尺寸、整除尺寸和非整除尺寸
- [x] reference 与断言完整
- [x] 输入契约明确
- [x] 代码通过项目格式检查
- [x] benchmark 排除首次 JIT 并正确处理异步执行
- [x] 至少完成一个与纯连续一维加法不同的变式

benchmark 原属本课可选练习，不阻挡 2026-07-22 的主课程验收；学习者随后在 2026-07-27
完成该扩展，并保留环境、方法、原始产物、错误预测和适用边界。

### 结课判定（2026-07-22）

学习者最终明确复述：masked load 的固定形状来自当前 program 中局部 pointer tensor 的形状，
而不是完整输入 tensor 的 shape。两个公开 wrapper 已补充简短 docstring，R14 随最终复验关闭。

最终证据：

```text
pytest -q gpu/triton/lesson01_vector_ops_test.py：58 passed in 2.74s
ruff check：All checks passed
ruff format --check：2 files already formatted
```

概念、实践与反思三个掌握维度均通过；全部阻塞、主要和要求关闭的次要发现均已关闭。学习者已
完成 AXPBY 与条件 masked store 两个变式，并能解释 grid、program instance、block tensor、
pointer tensor、mask、`tl.constexpr`、stride、多 GPU device guard、有效带宽和异步计时。

可选的 block-size benchmark 未完成，因此本课不记录任何本机性能结论。旧
`strided_1d_vector_add` 只作为历史练习归档，仍无 wrapper/pytest，不属于本课已验收成果，也不
阻挡官方 Vector Addition 案例结课。学习者已完成最终修改并确认理解，课程状态设为“已完成”。

后续补记（2026-07-27）：上段是 2026-07-22 主课程结课时的历史判定；此后可选 block-size
benchmark 已完成。其本机观察、原始结果和限制见
[AXPBY Benchmark 简报](../attachments/01-vector-add/axpby-benchmark.md)，不追溯改写原结课记录。

## 11. 阶段性暂停快照（2026-07-20）

本节是本次阶段性保存的恢复入口。此前的完整讲解、逐次答疑、练习要求和三轮评审仍保留在
前文；恢复学习时先阅读本节，无需重新梳理整份文档。

### 11.1 当前所处位置

| 项目 | 当前状态 |
| --- | --- |
| 当前课程 | 第 01 课 Vector Addition |
| 官方案例 | `docs/triton-tutorials/official/01-vector-add.py` |
| 学习阶段 | 评审中，第三轮 review 后已完成 R08/R09 实现修改，等待测试固化与复审 |
| Kernel / wrapper | `gpu/triton/lesson01_vector_ops.py` |
| pytest | `gpu/triton/lesson01_vector_ops_test.py` |
| 旧练习归档 | `strided_1d_vector_add` 已并入实践源码，但不在当前 20 个 pytest 用例内 |
| 原始对话 | 57 条用户/助手可见消息已导出到 `dialogues/01-vector-add.md` |
| 最近完整测试 | 20 passed in 4.27s，Python 3.12.13 / pytest 8.4.2 |
| 尚未关闭 | R07、R10；R08/R09 实现已修改但尚未由新增 pytest 固化 |
| 下一课程 | 第 02 课尚未开始 |

这不是“第一课已经完成”的快照，而是“核心数值路径已通过，正在完善接口边界和工程质量”的
暂停点。

### 11.2 已完成的学习内容

#### 教程理解

- 已完整阅读并讲解官方 Vector Addition 案例，包括 PyTorch baseline、Triton program instance、
  一维 grid、offset 生成、边界 mask、wrapper、JIT 特化和 benchmark。
- 已区分 Triton 的块级 tensor/lane 与 CUDA 标量 thread，不再把 `BLOCK_SIZE=1024` 直接理解为
  “显式创建 1024 个 CUDA threads”。
- 已理解 `grid = ceil(N / BLOCK_SIZE)` 如何保证覆盖全部元素，以及不同 program instance 如何
  处理互不重叠的连续区间。
- 已理解 `BLOCK_SIZE: tl.constexpr` 是“对当前编译特化为常量”，而不是整个 Python 进程中
  永远只能使用一个值。

#### 问题与答疑

| 问题 | 已形成的结论 | 状态 |
| --- | --- | --- |
| Q01 masked load 与 reduction | mask 不会压缩 tensor；false lane 仍占据静态形状，未提供 `other` 时值未定义，参与 reduction 前必须填单位元 | 已确认 |
| Q02 masked store | store mask 是逐 lane 写入谓词；false lane 不写内存，也不会压缩 value | 已确认 |
| Q03 `tl.constexpr` 是否可变 | wrapper 可在不同 launch 选择不同具体值，每个值对应一个可编译/缓存的特化 | 已确认 |
| Q04 CPU 能否执行 Triton kernel | 默认编译路径使用 GPU backend；`TRITON_INTERPRET=1` 是 CPU 模拟调试，实验性 CPU backend 是另一条路径 | 已确认 |

#### 实践与测试能力

- 已独立实现 AXPBY：`output = alpha * x + beta * y`。
- 已独立实现条件平方：仅对 `x > threshold` 的位置 masked store 平方值，其余位置保留 clone
  中的原值。
- 两个 kernel 均使用 `program_id + arange`、边界 mask 和 `tl.constexpr BLOCK_SIZE`。
- 条件平方的 masked load 已显式使用 `other=0.0`。
- wrapper 已加入 CPU、维度、dtype、contiguous 等显式异常检查，并实现空输入早返回和
  block-size resolver。
- wrapper 已加入同设备检查和 CUDA device guard；block-size resolver 已增加严格类型检查并在
  空输入早返回之前执行。
- 已从顶层直接执行脚本迁移到 pytest，掌握测试发现、`test_*`、参数化、fixture、
  `torch.testing.assert_close`、`pytest.raises` 和 GPU skip。
- 已建立固定边界用例，覆盖空输入、单元素、块边界前后、整块、大尾块和多个 program。

### 11.3 当前代码状态与证据

| 组成 | 已验证状态 | 当前限制 |
| --- | --- | --- |
| `axpby_kernel` | 现有参数化数值测试全部通过；同一非当前 GPU 手工探针通过 | 多 GPU 行为尚未固化为 pytest；跨卡错误消息待细化 |
| `threshold_square_kernel` | 正/负 threshold、等于边界、尾块测试通过 | wrapper 异常测试矩阵待补 |
| 空输入 | 两个 wrapper 都直接返回正确空输出；配置先于早返回验证 | 非法配置行为尚未固化为 pytest |
| block size | 显式 128/256/512/1024 通过；`128.0` 已由 wrapper 拒绝 | 类型与空输入组合尚未固化为 pytest |
| 默认 heuristic | 手工探针在 `N=513` 时两个算子均与 reference 一致 | 尚未固化为 pytest 用例 |
| pytest | `20 passed in 4.27s` | 通过集合仍未覆盖最新修复、旧 strided kernel 和全部接口契约 |
| 静态质量 | 测试文件已通过 Ruff formatter | `ruff check` 仍有 4 项，实现文件尚待格式化 |

阶段验证命令：

```bash
uv run --frozen pytest -vv gpu/triton/lesson01_vector_ops_test.py
```

最近结果：

```text
collected 20 items
20 passed in 4.27s
```

第三轮 review 时复现过、必须保留的反例证据：

1. 当前环境可见 8 张 GPU；`x@cuda:0`、`y@cuda:1` 没有被 wrapper 提前拒绝，而是在 Triton
   launch 时产生 pointer access `ValueError`。
2. 当前 device 为 0、两个输入都在 `cuda:1` 时，wrapper 仍 launch 失败；外层加入
   `with torch.cuda.device(x.device)` 后计算通过。
3. `block_size=128.0` 会通过 Python set membership，随后在 `tl.arange` 处产生
   `CompilationError`。
4. 空 tensor 配 `block_size=0` 会在 resolver 前返回，非法配置没有被拒绝。

当前实现已通过手工探针修复上述四项：跨卡输入由 wrapper 拒绝、同一非当前 GPU 正常运行、
`128.0` 抛 `TypeError`、空输入配 0 抛 `ValueError`。保留旧反例用于说明问题如何被发现；在 R10
补成自动测试之前，这些修复仍可能发生回归。现有 20 项全绿只代表“已覆盖行为正确”，不能
推导出“所有接口契约均正确”。

### 11.4 尚未关闭的评审项

| ID | 优先级 | 待完成内容 | 完成信号 |
| --- | --- | --- | --- |
| R08 | P1 / 待复审 | 同设备检查与 device guard 已实现；细化跨卡错误消息并增加多 GPU 测试 | 跨卡输入消息准确，同一非当前 GPU 用例稳定通过 |
| R09 | P1 / 待复审 | 严格类型检查和验证顺序已实现；增加对应自动测试 | 空输入配 0、`128.0` 等 pytest 用例稳定通过 |
| R10 | P1 / 主要 | 补全默认路径、threshold 错误输入、shape/dtype/stride 和多 GPU pytest | 新增用例稳定通过，失败信息清晰 |
| R07 | P2 / 工程质量 | 消除 Ruff 的导入/空行和 E731，格式化实现文件 | Ruff check 与 format check 均为零错误 |

可选练习 3 的 block-size benchmark 尚未执行。它不阻塞当前 wrapper 修复，但第一课最终关闭前
需要明确选择“完成并记录”或“本课跳过，留到后续性能专题”，不能保持未决状态。

### 11.5 下一步执行顺序

恢复学习后按以下顺序继续，避免同时大范围修改实现和测试：

1. 将 AXPBY 的“不是 CUDA”和“两个输入 device 不同”拆成两个检查，使跨卡错误消息准确表达
   根因；保留当前同设备检查与 device guard。
2. 补充 R10 中的 pytest：默认 heuristic、空输入非法配置、`128.0`、两个 wrapper 的错误输入，
   以及跨卡拒绝/同一非当前 GPU 成功。先把已手工验证的行为固化，防止回归。
3. 将 grid 简化为 host tuple，并使用 `BLOCK_SIZE=block_size` 关键字传递 meta-parameter。
4. 手工整理类型标注、短 docstring、错误消息、空行与代码格式，然后运行 Ruff；不依赖自动修复
   来掩盖尚未理解的诊断。
5. 执行完整 pytest/Ruff 验证并提交下一轮 review。R07–R10 全部关闭后，再进行概念复述与
   变式验收。

恢复后的完整验证命令：

```bash
uv run --frozen pytest -vv gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py
uv run --frozen ruff format --check gpu/triton/lesson01_vector_ops.py \
  gpu/triton/lesson01_vector_ops_test.py
```

### 11.6 进入第 02 课前的完成标准

- [ ] R07–R10 全部关闭，没有遗留阻塞或主要正确性问题
- [ ] 正常路径、错误输入、空输入、默认配置和多 GPU 语义都有对应测试
- [ ] pytest、Ruff check、Ruff format check 全部通过
- [ ] 能脱离源码解释 program、grid、offsets、mask、load/store mask 和 `tl.constexpr`
- [ ] 能说明为什么“20 个现有测试全绿”不等于接口已经被完整验证
- [ ] 决定并记录是否完成可选 block-size benchmark
- [ ] 将最终实现状态、测试输出和本课总结同步到学习档案

### 11.7 当前最重要的可迁移结论

1. Triton program 以静态形状的块级 tensor 表达工作；`program_id + arange + mask` 是一维
   elementwise kernel 的基础模式。
2. load mask 决定读取与 false lane 的值，store mask 决定是否产生写入副作用；二者都不会做
   compaction。
3. `tl.constexpr` 可以由 wrapper 动态选择具体配置，但一个已编译 variant 内必须是常量。
4. Python wrapper 是算子契约的一部分：device、dtype、shape、stride、空输入和配置校验与 kernel
   数学表达同等重要。
5. pytest 只能证明已执行断言覆盖的行为；边界枚举、负向测试和代码审阅共同决定验证强度。
6. 默认 Triton 编译 kernel 运行在 GPU；CPU wrapper、解释器模拟和实验性 CPU backend 是三个
   不同层次，不能混为一谈。

## 12. 原始对话与参考资料

### 原始对话归档

- **归档文件**：
  - [第一段：开课至阶段性保存](../dialogues/01-vector-add.md)
  - [第二段：恢复学习至最终复验](../dialogues/01-vector-add-part2.md)
  - [第三段：可选性能 Benchmark 扩展至本次暂停](../dialogues/01-vector-add-part3.md)
  - [第四段：性能扩展工程收尾关闭快照](../dialogues/01-vector-add-part4.md)
- **来源 session**：`rollout-2026-07-20T01-13-19-019f7d15-aa74-7bd2-abf5-e028149c8b47.jsonl`
- **session ID**：`019f7d15-aa74-7bd2-abf5-e028149c8b47`
- **截取范围**：第一段从用户消息“非常好，这就让我们开始第一课时吧。”开始，到
  2026-07-20 09:14:28 UTC 阶段性保存为止；第二段从用户消息“好的，接下来我们继续 lesson 01
  的学习”开始，到 2026-07-22 09:54:40 UTC 最终复验通过为止；第三段从用户重新开启可选
  benchmark 扩展开始，到 2026-07-24 10:10:00 UTC 本次暂停边界为止。课程片段之间的归档
  功能、Skill 创建和仓库贡献指南等元对话未纳入；第四段从 2026-07-27 恢复检查点开始，到用户
  提出提交 Lesson 01 之前为止。
- **消息数量**：第一段 57 条、第二段 37 条、第三段 87 条、第四段 18 条，合计 199 条，包括
  用户消息、助手过程更新和助手正式回答。
- **规范化**：移除 environment/IDE context、客户端注入的 Skill 文档、推荐插件列表和
  `AGENTS.md` 指令，去除相邻重复；不包含 system/developer、reasoning、工具调用和工具输出。
- **导出日期**：第一段 2026-07-21，第二段 2026-07-22，第三段 2026-07-24，第四段
  2026-07-27。
- **使用说明**：[Codex 学习对话后验归档](../references/raw-dialogue-export.md)

同一 rollout 中间包含不属于本课的元工作，因此按四个课程片段分别保存 provenance，没有把
中间消息拼入课程对话。第二至第四段均采用显式结束边界；四份生成文件均未人工改写消息正文。
第四段最终采用下一条用户提交请求作为排他语义边界，已经包含性能扩展的最终正式回答；提交与
后续课程元工作不属于该原始学习对话。

### 性能扩展暂停快照（2026-07-24）

| 项目 | 当前状态 |
| --- | --- |
| 第 01 课主课程 | 已完成；概念、正确性实践、反思与 R01–R14 不回退 |
| 可选性能扩展 | P01、P02、P03、P06 已关闭；P04、P05 尚有次要工程收尾 |
| Benchmark 报告 | 第一轮简报通过；保留四项非阻塞措辞建议 |
| 正确性 | `58 passed in 5.18s` |
| 静态质量 | Ruff lint 通过；benchmark 格式检查未通过；BasedPyright 剩余 2 项 |
| 实验产物 | 主矩阵 16 条、尾块 8 条 detailed record 及 CSV/PNG/HTML 已核对一致 |
| 原始对话 | 性能扩展 87 条可见消息已导出为第三段 |

恢复学习时按以下顺序继续：

1. 学习者自行处理 P04：格式化 `lesson01_vector_ops_benchmark.py` 并理解机械排版变化。
2. 处理 P05：对 `do_bench(..., quantiles=...)` 的返回值做最小且可解释的类型收窄，保留运行时
   三元素顺序检查。
3. 可顺手修正 P03-R1–R4 和尾块 detailed CSV 的命名；这些不阻塞课程。
4. 复跑 pytest、Ruff check/format 和聚焦 BasedPyright。P04/P05 关闭后，再建立第 02 课
   Fused Softmax 档案。

当前没有阻塞或主要正确性问题。暂停原因是时间安排，不是技术阻塞；未完成项及其复现命令已在
P04–P06 统一验证中保存。

### 性能扩展恢复快照（2026-07-27）

| 项目 | 当前状态 |
| --- | --- |
| P04 | Ruff check/format 已验证通过，正式关闭 |
| P05 静态类型 | BasedPyright `0 errors`，原两条解包错误已消失 |
| P05 运行时 guard | P05-R1 已关闭；P05-R2 只剩三个延迟值的有限数检查，`+inf` 当前仍会被接受 |
| 回归证据 | 58 项 pytest、Ruff、BasedPyright 与 Triton/Torch provider smoke 均通过 |

恢复入口收敛为一次窄修改：在现有三元素、浮点、正值和顺序 guard 上补齐三个延迟的有限数检查，
然后复跑当前验证矩阵与 `+inf` 探针。P05 关闭后即可结束第一课性能扩展并建立第 02 课
Fused Softmax 档案。

### 性能扩展最终关闭快照（2026-07-27）

| 项目 | 最终状态 |
| --- | --- |
| P01–P06 | 全部验证关闭 |
| 正确性 | `58 passed in 4.60s` |
| 静态质量 | Ruff check/format 与 BasedPyright 全部通过 |
| Benchmark guard | 返回形状、元素类型、正值、有限值与分位顺序均已验证 |
| 真实运行 | Triton/Torch provider smoke 的延迟和带宽区间顺序均正确 |
| 原始对话 | 第四段 18 条已按下一条用户提交请求为边界定稿 |

Lesson 01 现在没有未关闭的必做项、阻塞项、主要项或次要项。P03-R1–R4 的措辞与尾块 detailed
CSV 命名仍是明确的非阻塞建议，不影响结课。下一学习入口是建立第 02 课 Fused Softmax 档案并
开始官方案例讲解；profiler、cache、baseline、置信区间和 autotune 留到第二轮性能专题。

### 参考资料

- [本地官方案例](../../triton-tutorials/official/01-vector-add.py)
- [本地教程来源记录](../../triton-tutorials/SOURCE.md)
- [Triton 官方 Vector Addition 教程](https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html)
- [Triton 编程模型简介](https://triton-lang.org/main/programming-guide/chapter-1/introduction.html)
- [triton.jit](https://triton-lang.org/main/python-api/generated/triton.jit.html)
- [program_id](https://triton-lang.org/main/python-api/generated/triton.language.program_id.html)
- [arange](https://triton-lang.org/main/python-api/generated/triton.language.arange.html)
- [load](https://triton-lang.org/main/python-api/generated/triton.language.load.html)
- [store](https://triton-lang.org/main/python-api/generated/triton.language.store.html)
- [do_bench](https://triton-lang.org/main/python-api/generated/triton.testing.do_bench.html)
- [Triton 官方调试与解释器说明](https://triton-lang.org/main/programming-guide/chapter-3/debugging.html)
- [Triton 上游兼容性说明](https://github.com/triton-lang/triton#compatibility)
- [实验性 Triton CPU backend](https://github.com/triton-lang/triton-cpu)
- [本仓库 pytest GPU 测试参考](../references/pytest-gpu-kernel-tests.md)
- [pytest 官方 Get Started](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest 官方参数化测试](https://docs.pytest.org/en/stable/how-to/parametrize.html)

## 13. 文档变更记录

| 日期 | 阶段 | 变更摘要 |
| --- | --- | --- |
| 2026-07-20 | 建档与讲解 | 创建第一课档案，记录官方代码解析、边界条件和 benchmark 方法 |
| 2026-07-20 | Q01 答疑 | 说明 masked load 保持静态块形状及 reduction 所需的单位元 |
| 2026-07-20 | Q02 答疑 | 对比 store mask 的逐位置写入谓词与 load mask 的返回语义 |
| 2026-07-20 | Q03 答疑 | 区分 constexpr 的单个特化内固定与不同 launch 间可变 |
| 2026-07-20 | 实践布置 | 布置 AXPBY、条件平方更新及可选 block-size benchmark |
| 2026-07-20 | 第一版评审 | 记录实现状态、pytest 收集问题、Ruff 结果与 R01–R07 修改项 |
| 2026-07-20 | pytest 参考 | 新增 GPU kernel 正确性测试指南和第一课完整测试骨架 |
| 2026-07-20 | 第二版评审 | 记录 20 个 pytest 用例的 15 passed / 5 failed，并定位 wrapper 契约问题 |
| 2026-07-20 | Q04 答疑 | 区分 GPU 编译执行、CPU host wrapper、解释器模式与实验性 CPU backend |
| 2026-07-20 | 第三版评审 | 确认现有 20 项全通过，并新增多 GPU、配置类型/顺序和测试覆盖意见 |
| 2026-07-20 | 阶段性保存 | 汇总已完成内容、实测证据、R07–R10、恢复顺序及进入第二课的门槛 |
| 2026-07-20 | 旧练习归档 | 将 `strided_1d_vector_add` 原样并入第一课实践源码，明确其尚未评审或测试 |
| 2026-07-21 | 原始对话归档 | 新增后验导出功能，并生成包含 57 条消息的第一课阶段性原始对话 |
| 2026-07-22 | 复审与掌握验收 | 完成 58 项测试、六轮评审、两轮概念复述并关闭 R01–R14 |
| 2026-07-22 | 正式结课 | 最终 pytest/Ruff 通过，记录可选 benchmark 未完成，并导出续段原始对话 |
| 2026-07-22 | 归档过滤修正 | 默认排除客户端独立注入的 Skill 文档，续段由 38 条修正为 37 条 |
| 2026-07-23 | 可选性能扩展 | 恢复练习 3，补充本地 `do_bench` 计时流程并记录下一步实践入口 |
| 2026-07-23 | 性能实践布置 | 约定 AXPBY benchmark 的源码、实验记录、测量矩阵和验收标准 |
| 2026-07-23 | Q10 答疑 | 区分多 `x_names` 的联动配置与 `line_arg` 形成的 size/block-size 实验矩阵 |
| 2026-07-23 | Q11 答疑 | 通过最小实验说明多 `x_names` 的 tuple 配对、标量复制和结果表结构 |
| 2026-07-24 | Q12 答疑 | 定位 `perf_report` 首次保存失败为创建目录晚于 `savefig` 的调用顺序问题 |
| 2026-07-24 | 性能第 1 轮评审 | 验证首次保存修复与 58 项正确性测试，记录 P01–P06 |
| 2026-07-24 | Q13 答疑 | 设计独立 detailed CSV，在 `perf_report` 丢弃区间前保存延迟与带宽三元组 |
| 2026-07-24 | P01 定向复审 | 两次运行均验证 16 行不重复记录、分位顺序及 48 个带宽换算值，P01 关闭 |
| 2026-07-24 | Q14 答疑 | 明确尾块事前预测内容与位置，并以单配置测量函数复用主曲线和尾块实验 |
| 2026-07-24 | P02 定向复审 | 核对 8 行尾块数据并独立复测三轮，校准 mask、program 调度与计时粒度模型 |
| 2026-07-24 | Q15 答疑 | 用有效字节/时间比值区分公式性微升、p50 档位波动与真实硬件带宽 |
| 2026-07-24 | Q16 答疑 | 区分 `rep` 总采样预算与单次 event，并界定 batching、冷缓存和 CUDA Graph 的测量语义 |
| 2026-07-24 | Q17 答疑 | 将 1.024 µs 限定为当前 CUDA Event 栈的经验量化步长，并与 kernel 执行粒度区分 |
| 2026-07-24 | P02 复盘第 1 轮评审 | 核对事前反证、masked lane、BS=1024、结论边界与 provenance，记录 P02-R1–R6 |
| 2026-07-24 | Q18 答疑 | 用当前 AXPBY PTX 的 guard predicate 区分 false lane、物理 transaction 与有效 GB/s |
| 2026-07-24 | P02 复盘第 2 轮评审 | 关闭 R2–R4/R6，按学习者说明终止 R5，将 R1 收敛为两个窄修改点 |
| 2026-07-24 | P02 最终评审 | 验证确定 mask 语义与带宽比值因果，关闭 R1 和整个 P02 尾块实验 |
| 2026-07-24 | P03 补档任务 | 约定环境、方法、24 行结果、五项分析、限制与原始产物链接的验收标准 |
| 2026-07-24 | P03 框架搭建 | 保留原预测与复盘，新增可填写的完整实验报告结构和结果表 |
| 2026-07-24 | P03 范围调整 | 将过重的 55 项完整报告收缩为预填事实加两段学习者总结，系统性能研究延期 |
| 2026-07-24 | P03 最终评审 | 第一轮简报通过并关闭 P03，保留四项非阻塞措辞建议 |
| 2026-07-24 | P04–P06 统一验证 | 58 项正确性与 Ruff lint 通过，关闭 P06；P04 格式和 P05 两项类型错误留待恢复 |
| 2026-07-24 | 性能扩展暂停 | 保存恢复顺序并导出 87 条第三段原始对话；客户端插件与 AGENTS 注入已过滤 |
| 2026-07-27 | P04/P05 恢复复审 | 关闭 P04，确认 P05 静态类型通过，并以无效返回探针记录 P05-R1/R2 |
| 2026-07-27 | P05 恢复复审第 2 轮 | 关闭 P05-R1，将 P05-R2 收敛为遗漏的有限数检查 |
| 2026-07-27 | P05 最终复审 | 有限数探针与完整回归通过，关闭 P05 和整个可选性能扩展 |
| 2026-07-27 | 原始对话定稿 | 以用户提交请求为边界重导出 18 条第四段对话，纳入最终复审回答 |
| 2026-08-06 | 结果文件命名收尾 | 主矩阵与尾块目录的详细表统一为 `detailed.csv`，同步生成代码和现行文档链接 |
