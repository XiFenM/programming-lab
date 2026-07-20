# 用 pytest 测试 Triton GPU Kernel

本文是本仓库 Triton 课程共用的 pytest 入门参考，第一版示例对应：

- 实现：[`gpu/triton/lesson01_vector_ops.py`](../../../gpu/triton/lesson01_vector_ops.py)
- 测试：[`gpu/triton/lesson01_vector_ops_test.py`](../../../gpu/triton/lesson01_vector_ops_test.py)

仓库在 `pyproject.toml` 中约束 pytest `>=8.4,<9`，当前 lockfile 解析为 8.4.2。下文只使用
pytest 的基础稳定接口。

## 1. 从直接运行脚本到 pytest

一个最小 pytest 测试仍然只是普通 Python 函数：

```python
def test_addition() -> None:
    actual = 1 + 2
    assert actual == 3
```

pytest 主要替我们完成三件事：

1. **发现**：收集名称符合 `test_*.py` 或 `*_test.py` 的文件，以及其中以 `test_` 开头的函数。
2. **执行与隔离**：把每个测试函数作为一个独立 test item 执行并单独报告。
3. **判定**：断言失败或出现未预期异常时返回非零退出码，自动化流程能据此阻止错误代码通过。

可以用 Arrange / Act / Assert 理解一个正确性测试：

```python
def test_example() -> None:
    # Arrange：准备输入与 reference
    x = ...
    expected = ...

    # Act：调用待测实现
    actual = ...

    # Assert：明确什么才算正确
    assert actual == expected
```

第一版直接测试与 pytest 测试的差别如下：

| 第一版写法 | 问题 | pytest 写法 |
| --- | --- | --- |
| 在模块顶层直接 `for` 循环 | 导入/收集文件时就执行，不会形成独立 test item | 把执行放入 `test_*` 函数 |
| 只 `print(max_difference)` | 不论误差多大都可能以成功状态退出 | 使用会失败的断言 |
| 只随机产生 size | 不能保证命中空输入、整块和尾块边界 | `@pytest.mark.parametrize` 明确列出边界 |
| 一次循环包含两个算子 | 失败时不容易定位是哪种语义出错 | 每个行为使用独立测试函数 |
| `import lesson01_vector_ops` | 从仓库根目录执行时找不到顶层模块 | 从包路径 `gpu.triton` 导入 |

## 2. 第一课完整参考

下面的版本可以作为 `gpu/triton/lesson01_vector_ops_test.py` 的改写目标。它沿用第一版
`axpby(alpha, x, beta, y)` 的参数顺序，同时假设 wrapper 按练习要求新增仅限关键字的
`block_size` 参数；如果改变了 wrapper API，只需同步调整两处调用。

```python
import pytest
import torch

from gpu.triton import lesson01_vector_ops as ops


pytestmark = pytest.mark.skipif(
    not torch.cuda.is_available(),
    reason="lesson 01 requires a CUDA GPU",
)

RTOL = 1e-5
ATOL = 1e-6


@pytest.fixture
def cuda_generator() -> torch.Generator:
    """Give every test an independently seeded CUDA random generator."""
    return torch.Generator(device="cuda").manual_seed(1234)


@pytest.mark.parametrize(
    ("size", "block_size", "alpha", "beta"),
    [
        pytest.param(0, 128, 1.0, 1.0, id="empty"),
        pytest.param(1, 256, 2.0, -0.5, id="single-element"),
        pytest.param(127, 128, 0.0, 3.0, id="one-before-block"),
        pytest.param(128, 128, 1.0, 1.0, id="exact-block"),
        pytest.param(129, 128, 2.0, -0.5, id="one-after-block"),
        pytest.param(1023, 512, 0.0, 3.0, id="large-tail"),
        pytest.param(1024, 1024, 1.0, 1.0, id="exact-large-block"),
        pytest.param(1025, 1024, 2.0, -0.5, id="large-block-tail"),
        pytest.param(98_417, 256, 0.0, 3.0, id="many-programs-tail"),
    ],
)
def test_axpby_matches_torch(
    size: int,
    block_size: int,
    alpha: float,
    beta: float,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.randn(
        size,
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )
    y = torch.randn(
        size,
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )

    expected = alpha * x + beta * y
    actual = ops.axpby(alpha, x, beta, y, block_size=block_size)

    assert actual.shape == x.shape
    assert actual.dtype == x.dtype
    assert actual.device == x.device
    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize(
    ("values", "threshold", "block_size"),
    [
        pytest.param(
            [-1.0, 0.49, 0.5, 0.51, 2.0],
            0.5,
            128,
            id="below-equal-above",
        ),
        pytest.param(
            [-3.0, -2.0, -1.0, -0.5],
            -1.5,
            128,
            id="negative-threshold",
        ),
    ],
)
def test_threshold_square_semantics(
    values: list[float],
    threshold: float,
    block_size: int,
) -> None:
    x = torch.tensor(values, device="cuda", dtype=torch.float32)

    expected = torch.where(x > threshold, x * x, x)
    actual = ops.threshold_square(x, threshold, block_size=block_size)

    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize(
    ("size", "block_size"),
    [
        pytest.param(0, 128, id="empty"),
        pytest.param(1, 256, id="single-element"),
        pytest.param(259, 128, id="multi-program-tail"),
        pytest.param(1025, 512, id="large-tail"),
    ],
)
def test_threshold_square_matches_torch(
    size: int,
    block_size: int,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.randn(
        size,
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )
    threshold = -0.25

    expected = torch.where(x > threshold, x * x, x)
    actual = ops.threshold_square(x, threshold, block_size=block_size)

    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize("block_size", [0, 64, 127, 2048])
def test_axpby_rejects_invalid_block_size(block_size: int) -> None:
    x = torch.randn(8, device="cuda", dtype=torch.float32)
    y = torch.randn_like(x)

    with pytest.raises(ValueError, match="block_size"):
        ops.axpby(1.0, x, 1.0, y, block_size=block_size)


def test_axpby_rejects_cpu_tensors() -> None:
    x = torch.randn(8, dtype=torch.float32)
    y = torch.randn_like(x)

    with pytest.raises(ValueError, match="CUDA"):
        ops.axpby(1.0, x, 1.0, y, block_size=128)
```

这份参考有意把“空 tensor”和“调用者选择 block size”写成测试契约。当前第一版 wrapper 还不
满足这两项，所以改写测试后先失败是正常现象。应修改实现使测试通过，不要删掉暴露问题的用例。

## 3. 五个核心 pytest 用法

### 3.1 测试发现

当前文件名 `lesson01_vector_ops_test.py` 已符合 pytest 默认的 `*_test.py` 规则。函数还必须以
`test_` 开头；类并非必需。

本仓库另有一项有意的配置：

```toml
[tool.pytest.ini_options]
testpaths = ["tests/python"]
```

因此直接运行 `pytest` 只会从 CPU 测试目录开始发现，不会自动运行 `gpu/triton/` 中的练习。
执行 GPU 测试时要显式给出路径。

### 3.2 参数化 `parametrize`

`@pytest.mark.parametrize` 会把一份测试逻辑展开为多个独立 test item。每一组边界数据都有
自己的通过/失败结果，`pytest.param(..., id="...")` 则让报告名称表达该用例的意图。

固定边界用例应优先于纯随机压力测试。随机测试可以补充覆盖，但不能替代 `0`、`1`、
`BLOCK_SIZE - 1`、`BLOCK_SIZE` 和 `BLOCK_SIZE + 1` 等结构化边界。

### 3.3 Fixture

`@pytest.fixture` 用于提供测试所需的可复用上下文。测试函数只要声明同名参数，pytest 就会在
运行测试前调用 fixture 并注入返回值。

参考中的 fixture 默认为 function scope，因此每个参数化用例会获得一个重新以 1234 播种的
generator。这样失败可复现，也避免一个测试改变后使后续测试的随机序列整体偏移。

### 3.4 张量断言

不要只打印最大误差，也不要对整个 Torch tensor 使用普通的 `actual == expected`。对 PyTorch
tensor 使用：

```python
torch.testing.assert_close(actual, expected, rtol=1e-5, atol=1e-6)
```

它会检查数值接近性，并在失败时给出不匹配数量、最大绝对误差和最大相对误差等信息。AXPBY
可能受浮点舍入和融合乘加影响，所以使用明确容差，而不是要求逐 bit 相等。

### 3.5 异常与跳过

`pytest.raises` 用于验证错误输入确实被 wrapper 以约定方式拒绝：

```python
with pytest.raises(ValueError, match="block_size"):
    call_with_bad_block_size()
```

这同时检查异常类型和消息中的关键字。wrapper 应抛出明确的 `ValueError` 或 `TypeError`；不要
把普通输入契约完全依赖于 Python `assert`，因为优化模式可以移除 assert 语句。

模块级 `pytestmark = pytest.mark.skipif(...)` 会在 CUDA 不可用时把测试报告为 skipped，而不是
failed。为了让无 GPU 环境能够先成功导入待测模块，模块本身不要在 import 阶段查询 active
Triton driver；第一版中未使用的 `DEVICE = ...get_active_torch_device()` 应删除。

## 4. 常用命令

从仓库根目录运行：

```bash
# 收集测试但不执行，用来检查文件名、导入和参数化展开结果
uv run --frozen pytest --collect-only -q gpu/triton/lesson01_vector_ops_test.py

# 运行本课全部 GPU 测试
uv run --frozen pytest -q gpu/triton/lesson01_vector_ops_test.py

# 显示每个参数化用例的完整名称
uv run --frozen pytest -vv gpu/triton/lesson01_vector_ops_test.py

# 只运行名称中包含 axpby 的用例
uv run --frozen pytest -q -k axpby gpu/triton/lesson01_vector_ops_test.py

# 遇到第一个失败就停止
uv run --frozen pytest -q -x gpu/triton/lesson01_vector_ops_test.py

# 只重跑一个测试函数
uv run --frozen pytest -q \
  gpu/triton/lesson01_vector_ops_test.py::test_threshold_square_semantics
```

常见状态：

| 标记 | 含义 |
| --- | --- |
| `.` / `PASSED` | 断言全部满足 |
| `F` / `FAILED` | 测试已经运行，但断言失败 |
| `E` / `ERROR` | 收集、fixture、setup 等阶段出错，测试可能尚未真正运行 |
| `s` / `SKIPPED` | 前置条件不满足，本例通常是没有 CUDA GPU |

正确性断言会实际读取/比较结果，从而等待相关 GPU 工作完成；无需为了普通正确性测试手写一次
额外同步。性能 benchmark 则是另一类测试，仍应使用 `triton.testing.do_bench` 等正确处理
warm-up 与同步的工具，不应混在这些 pytest 正确性用例中。

## 5. 推荐的渐进改写顺序

1. 修正包导入，并把顶层循环移进一个 `test_*` 函数。
2. 把 `print(max_difference)` 换成 `torch.testing.assert_close`。
3. 用一个小型 `parametrize` 覆盖 `N=1/128/129`，先确认 pytest 工作流跑通。
4. 加入空 tensor、不同 block size 与大尾块用例，并修复 wrapper。
5. 加入 threshold 的手工语义数据，尤其覆盖“等于 threshold”和负 threshold。
6. 最后用 `pytest.raises` 补齐输入契约测试，并运行 Ruff。

## 6. 官方资料

- [pytest Get Started](https://docs.pytest.org/en/stable/getting-started.html)
- [测试发现与命令行调用](https://docs.pytest.org/en/stable/how-to/usage.html)
- [断言与 `pytest.raises`](https://docs.pytest.org/en/stable/how-to/assert.html)
- [`@pytest.mark.parametrize`](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [Fixtures](https://docs.pytest.org/en/latest/explanation/fixtures.html)
- [`skip` / `skipif` API](https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif)
