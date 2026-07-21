# 第 01 课：Vector Addition

## 1. 课程档案

| 字段 | 内容 |
| --- | --- |
| 课程编号 | `01` |
| 官方案例 | [`01-vector-add.py`](../../triton-tutorials/official/01-vector-add.py) |
| 教程快照 | Triton `main` 文档，下载于 2026-07-15 UTC |
| 学习状态 | 评审中 |
| 开始日期 | 2026-07-20 |
| 完成日期 | — |
| 仓库已有参考 | [`gpu/triton/vector_add.py`](../../../gpu/triton/vector_add.py) |
| 学习者实践源码 | [`lesson01_vector_ops.py`](../../../gpu/triton/lesson01_vector_ops.py) |
| 测试代码 | [`lesson01_vector_ops_test.py`](../../../gpu/triton/lesson01_vector_ops_test.py) |
| 原始对话 | [`dialogues/01-vector-add.md`](../dialogues/01-vector-add.md)，阶段性已导出 |
| 补充材料 | [pytest GPU 测试参考](../references/pytest-gpu-kernel-tests.md) |

### 环境基线

| 项目 | 版本或型号 |
| --- | --- |
| GPU | 当前记录环境未透传 GPU，待实际实验时补充 |
| NVIDIA driver | 当前记录环境无法通过 `nvidia-smi` 查询 |
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
- [ ] 已处理全部阻塞问题
- [ ] 已通过正确性与边界测试
- [ ] 已完成知识复述与变式验收
- [ ] 已总结并关闭本课
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
- Triton 的 `add` 和 Torch 的 `x + y` 都包含输出 tensor 分配，比较口径大致一致。

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

当前环境的 `do_bench` 默认先 warm-up 25 ms，再累计测量 100 ms；教程没有覆盖这两个参数。
它会处理 GPU 计时所需的同步，避免用普通 CPU wall-clock 错误测量异步 GPU launch。
最大的 `2**27` 个 float32 元素，每个 tensor 为 512 MiB，三个 tensor 合计约 1.5 GiB，因此
运行完整 benchmark 前还要考虑实际显存。无图形界面的环境可先使用
`show_plots=False, print_data=True`。

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

待补充。

### 我可以独立解释的问题

- [ ] 为什么 grid 是 `ceil(N / BLOCK_SIZE)`？
- [ ] 一个 program instance 处理哪些数据？
- [ ] 为什么最后一个 program 需要 mask？
- [ ] `BLOCK_SIZE` 为什么是 `tl.constexpr`？
- [ ] `BLOCK_SIZE=1024` 为什么不等于 1024 个 CUDA threads？
- [ ] `x_ptr + offsets` 的含义是什么？
- [ ] 为什么这个算子通常受内存带宽限制？
- [ ] 为什么普通 CPU 计时可能错误衡量异步 GPU kernel？

### 尚不牢固的概念

- 当前没有已知的未解决概念。Q01–Q03 均已由学习者确认解决。

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

使用 `triton.testing.do_bench` 对练习 1 的 `BLOCK_SIZE=128/256/512/1024` 进行测量：

- 输入规模至少包含 `2**12`、`2**16`、`2**20` 和 `2**24`。
- 记录 GPU、driver、Triton/PyTorch 版本、warm-up、测量时长和分位数。
- 第一次 JIT 调用不计入稳态结果。
- 同时记录延迟和按“两读一写”计算的有效 GB/s。
- 只描述实际观察，不预设 1024 必然最快。

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
| Benchmark | 可放在实现文件的 `main()` 或独立文件 | 可选 |

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

## 10. 掌握验收

### 概念验收

1. 脱离源码画出 `N=10, BLOCK_SIZE=4` 时三个 program 的 offsets 和 mask。
2. 解释 `tl.arange`、`tl.program_id`、`tl.load` 和 `tl.store` 各自处在哪个抽象层。
3. 解释运行时 `n_elements` 和编译期 `BLOCK_SIZE` 的不同职责。
4. 指出官方 wrapper 对 shape、dtype、stride 和空 tensor 的隐含假设。
5. 推导 benchmark 中系数 3 的来源，并解释为什么它叫有效带宽。

### 实践验收

- [ ] 可以独立重写核心 kernel，而不是逐行照抄
- [ ] 覆盖小尺寸、整除尺寸和非整除尺寸
- [ ] reference 与断言完整
- [ ] 输入契约明确
- [ ] 代码通过项目格式检查
- [ ] benchmark 排除首次 JIT 并正确处理异步执行
- [ ] 至少完成一个与纯连续一维加法不同的变式

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

- **归档文件**：[第 01 课原始学习对话](../dialogues/01-vector-add.md)
- **来源 session**：`rollout-2026-07-20T01-13-19-019f7d15-aa74-7bd2-abf5-e028149c8b47.jsonl`
- **session ID**：`019f7d15-aa74-7bd2-abf5-e028149c8b47`
- **截取范围**：从用户消息“非常好，这就让我们开始第一课时吧。”开始，到 2026-07-20
  09:14:28 UTC 助手完成旧 strided vector add 整理提交为止；本次新增归档功能的元对话未纳入。
- **消息数量**：57，包括用户消息、助手过程更新和助手正式回答。
- **规范化**：移除 environment/IDE context，去除相邻重复；不包含 system/developer、reasoning、
  工具调用和工具输出。
- **导出日期**：2026-07-21。
- **使用说明**：[Codex 学习对话后验归档](../references/raw-dialogue-export.md)

本文件是阶段性导出。第一课最终结束时，如果后续仍在同一 session 中继续，应使用原有开课
边界和新的结束边界重新导出并人工审核 diff；若跨 session，则分别保留 provenance 并在此建立
多文件索引。

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
