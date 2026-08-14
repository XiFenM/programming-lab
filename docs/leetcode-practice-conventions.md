# LeetCode 练习目录与验证约定

本文约定在本仓库中新增 LeetCode 题解时的目录、命名、测试和验证方式。它面向不使用
Docker、CUDA 或 GPU 的 Linux x86_64 宿主机路线；GPU 练习继续遵循仓库 README 中的容器路线。

## 核心规则

1. 题解放在 `leetcode/<language>/`，可在宿主机运行的测试放在对应测试目录。
2. 新文件统一使用 `p<题号>_<英文题名>`；题号至少补足四位，英文题名使用
   `snake_case`。例如 LeetCode 3 使用 `p0003_longest_substring`。
3. 一道题至少覆盖标准输入和边界输入；如果本地接口定义了错误行为，也要覆盖无解或非法输入。
4. 默认只使用各语言标准库。不要直接向全局环境或 `.venv` 手工安装依赖。
5. 迭代时先运行单题测试，完成后运行仓库的 CPU-only 全量验证。

现有 `two_sum` 启动示例和 `leetcode/cpp/<数字>.<slug>.cpp` 平台片段早于本约定，暂不为此
重命名；后续新增题目统一采用这里的命名和测试结构。

推荐目录结构：

```text
leetcode/
├── python/
│   └── p0003_longest_substring.py
├── cpp/
│   ├── p0003_longest_substring.hpp
│   └── p0003_longest_substring.cpp
└── rust/
    └── p0003_longest_substring/
        ├── Cargo.toml
        └── src/lib.rs
tests/
├── python/leetcode/
│   └── test_p0003_longest_substring.py
└── cpp/
    └── test_p0003_longest_substring.cpp
```

## 开始前

首次在宿主机使用时，从仓库根目录初始化环境：

```bash
bash scripts/host-cpu.sh init
```

后续命令也统一通过 `scripts/host-cpu.sh` 执行，以便使用仓库内隔离的 Python、C++ 和 Rust
工具链。可以先确认环境状态：

```bash
bash scripts/host-cpu.sh doctor
```

## Python

### 文件位置

- 题解：`leetcode/python/p0003_longest_substring.py`
- 测试：`tests/python/leetcode/test_p0003_longest_substring.py`

测试使用合法的 Python 模块路径导入题解：

```python
from leetcode.python.p0003_longest_substring import length_of_longest_substring
```

函数参数和返回值保留完整类型标注。测试函数使用 `test_*` 命名，并优先使用参数化测试覆盖
多组输入。可以参考现有的 [Two Sum 题解](../leetcode/python/two_sum.py) 和
[测试](../tests/python/leetcode/test_two_sum.py)。

只要题解和测试放在上述目录，就不需要修改额外配置。运行单题：

```bash
bash scripts/host-cpu.sh run -- \
  python -m pytest -q tests/python/leetcode/test_p0003_longest_substring.py
```

`bash scripts/host-cpu.sh test` 会自动运行 `tests/python/leetcode/` 下的全部 Python 测试；
`lint` 和 `verify` 也会自动检查该目录及 `leetcode/python/`。

## C++

### 文件位置

- 声明：`leetcode/cpp/p0003_longest_substring.hpp`
- 实现：`leetcode/cpp/p0003_longest_substring.cpp`
- 测试入口：`tests/cpp/test_p0003_longest_substring.cpp`

把算法放在 `leetcode` namespace 中，头文件保存公开声明，源文件保存实现，测试文件负责
`main()` 和断言。这样题解可以独立复用，也可以在本地构建测试。可以参考现有的
[头文件](../leetcode/cpp/two_sum.hpp)、[实现](../leetcode/cpp/two_sum.cpp) 和
[测试入口](../tests/cpp/test_two_sum.cpp)。

### CMake 登记

C++ 目标不会按文件名自动发现。新增题目后，需要在
[CMakeLists.txt](../CMakeLists.txt) 中登记 executable 和 CTest：

```cmake
add_executable(
  cpp_p0003_longest_substring
  leetcode/cpp/p0003_longest_substring.cpp
  tests/cpp/test_p0003_longest_substring.cpp
)
target_include_directories(cpp_p0003_longest_substring PRIVATE "${PROJECT_SOURCE_DIR}")
enable_project_warnings(cpp_p0003_longest_substring)

if(BUILD_TESTING)
  add_test(
    NAME cpp_p0003_longest_substring
    COMMAND cpp_p0003_longest_substring
  )
endif()
```

构建并只运行这道题：

```bash
bash scripts/host-cpu.sh build
bash scripts/host-cpu.sh run -- \
  ctest --preset host-cpu -R '^cpp_p0003_longest_substring$' \
  --output-on-failure --no-tests=error
```

`leetcode/cpp/` 中已有的 `1.two-sum.cpp` 这类文件是 LeetCode 平台提交片段。单独保存这样的
文件不需要配置，但宿主机路线只会对它做格式检查，不会自动编译或测试。需要本地验证时，应使用
上面的 `.hpp + .cpp + test.cpp + CMake` 结构。

## Rust

### crate 位置和配置

每道题使用一个 library crate：

```text
leetcode/rust/p0003_longest_substring/
├── Cargo.toml
└── src/lib.rs
```

`Cargo.toml` 使用以下基础配置：

```toml
[package]
name = "leetcode-p0003-longest-substring"
version = "0.1.0"
edition.workspace = true
rust-version.workspace = true

[lints]
workspace = true
```

根目录 [Cargo workspace](../Cargo.toml) 会通过 `leetcode/rust/*` 自动发现新 crate，不需要
手工修改 workspace members。算法测试优先放在 `src/lib.rs` 的 `#[cfg(test)]` 模块；需要
黑盒测试时，再使用该 crate 的 `tests/` 目录。现有 [Two Sum crate](../leetcode/rust/two_sum)
可以作为参考。

首次新增 crate 后，允许 Cargo 更新并检查根目录锁文件：

```bash
bash scripts/host-cpu.sh run -- \
  cargo check -p leetcode-p0003-longest-substring
git diff -- Cargo.lock
```

确认锁文件变更符合预期后，运行单题测试：

```bash
bash scripts/host-cpu.sh run -- \
  cargo test -p leetcode-p0003-longest-substring --locked
```

后续 `host-cpu.sh test`、`lint` 和 `verify` 会自动覆盖整个 Rust workspace。

## 依赖边界

普通 LeetCode 题目应只使用标准库。如果确实需要第三方依赖：

- Python：不要直接执行 `pip install`。当前宿主机路线只同步约定的 CPU 开发依赖；新增运行时
  依赖需要同时设计 `pyproject.toml` 中的 CPU 依赖组、更新 `uv.lock`，并调整初始化策略。
- C++：需要同时在 `pixi.toml`/`pixi.lock` 和 CMake 中显式管理，不能假定宿主机已全局安装。
- Rust：在题目 crate 的 `Cargo.toml` 中声明，并提交更新后的根 `Cargo.lock`。

除非题目本身要求，否则不要为一道算法题扩大公共工具链。

## 完成一道题

开发过程中先运行上述单题命令。准备结束时，从仓库根目录运行：

```bash
bash scripts/host-cpu.sh test
bash scripts/host-cpu.sh lint
```

需要同时检查环境、锁文件、隔离状态、构建、测试和静态质量时运行：

```bash
bash scripts/host-cpu.sh verify
```

提交前确认：

- 题解和测试使用统一的题号与题名；
- 标准、边界和约定的错误输入均有测试；
- C++ 新目标已经登记到 CMake，Rust 新 crate 已更新 `Cargo.lock`；
- 没有提交 `.venv/`、`.pixi/`、`.cache/`、`build/` 或 `target/`；
- `host-cpu.sh verify` 通过。
