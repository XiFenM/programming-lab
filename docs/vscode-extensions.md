# VS Code 推荐扩展说明

本仓库在 [`.vscode/extensions.json`](../.vscode/extensions.json) 中推荐 20 个扩展，用于覆盖
开发容器、Python、C++/CUDA、Rust、配置文件和文档编辑。四套 Dev Container 配置还会自动
安装其中 13 个核心开发扩展；仅出现在工作区推荐列表中的扩展，需要在 VS Code 提示后手动
安装。

扩展提供编辑器集成，但不代替仓库自己的检查流程。提交前仍应按改动范围运行 `make lint`、
`make test` 或 `make verify`。

## 容器与通用工作流

| 扩展 | Dev Container 自动安装 | 在本仓库中的用途 |
| --- | --- | --- |
| [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) | 否，安装在宿主机 | 构建并进入 `.devcontainer/` 定义的四套开发环境，是推荐开发方式的入口。 |
| [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) | 否 | 查看容器、镜像、网络和 Compose 资源，辅助排查开发容器与 v2rayA sidecar。 |
| [EditorConfig](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig) | 是 | 读取 `.editorconfig`，统一缩进、换行、文件末尾换行和尾随空白规则。 |
| [Error Lens](https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens) | 否 | 把诊断信息直接显示在相关代码行旁，便于及时发现类型、lint 和编译问题。 |

`Dev Containers` 必须先安装在宿主机 VS Code 中，否则无法执行
`Dev Containers: Reopen in Container`。其他语言扩展应安装在容器侧，使其能够访问容器中的
解释器、编译器和命令行工具。

## Python

| 扩展 | Dev Container 自动安装 | 在本仓库中的用途 |
| --- | --- | --- |
| [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) | 是 | 选择 uv 创建的 Python 3.12 解释器、发现 pytest 测试，并提供 Python 编辑器基础支持。 |
| [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) | 是 | 为 `.vscode/launch.json` 中的 `Python: current file` 提供 `debugpy` 调试后端。 |
| [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) | 是 | 提供 lint、格式化和 import 排序；本仓库将它设为 Python 默认格式化器。 |
| [BasedPyright](https://marketplace.visualstudio.com/items?itemName=detachhead.basedpyright) | 是 | 提供 Python 语言服务和静态类型检查；工作区启用了 `strict` 模式。 |

这里的职责是分开的：Python 扩展负责解释器和测试集成，BasedPyright 负责类型诊断，Ruff
负责代码风格、格式化和部分可自动修复的问题。

Triton kernel 是由 `@triton.jit` 编译的 DSL，静态分析时会产生普通 Python 类型系统无法准确
表达的指针、block tensor 和编译期参数。`pyproject.toml` 因此只在 `gpu/triton/` 下关闭五类
由 `Unknown` 级联产生的诊断，其他 BasedPyright strict 规则仍然有效；`int` 传给
`tl.constexpr` 的启动假阳性则在对应参数处使用带规则名的 `# pyright: ignore` 定点抑制。
不要为消除提示而给所有 kernel 变量添加 `Any`，也不要全局关闭 BasedPyright。

## C++ 与 CUDA

| 扩展 | Dev Container 自动安装 | 在本仓库中的用途 |
| --- | --- | --- |
| [clangd](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd) | 是 | 负责 C++/CUDA 补全、跳转、诊断、clang-tidy 和格式化；读取 `build/debug/compile_commands.json`。 |
| [CMake Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools) | 是 | 识别 `CMakePresets.json`，在 VS Code 中执行 configure、build 和目标选择。 |
| [C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) | 是 | 为 `launch.json` 中的 `cppdbg` 配置提供 GDB 调试能力。 |
| [NVIDIA Nsight Visual Studio Code Edition](https://marketplace.visualstudio.com/items?itemName=nvidia.nsight-vscode-edition) | 是 | 调试原生 CUDA 程序，检查 kernel、线程和设备端状态；需要可用的 NVIDIA GPU 和 CUDA 调试环境。 |
| [CodeLLDB](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb) | 是 | 提供 LLDB 调试后端；当前 `Rust: Two Sum tests` 调试模板使用它。 |

工作区显式设置了 `"C_Cpp.intelliSenseEngine": "disabled"`：Microsoft C/C++ 扩展只承担
GDB 调试，代码补全和静态诊断统一交给 clangd，避免两套语言服务重复报错。首次运行
`make configure` 后，clangd 才能获得准确的 include 路径、宏和 C++20/CUDA 编译参数。

Nsight 面向原生 CUDA 调试，不是 Triton kernel 的通用源码级调试器。Triton 练习通常仍以
PyTorch reference、pytest、边界用例和必要的数值/性能检查为主。

## Rust

| 扩展 | Dev Container 自动安装 | 在本仓库中的用途 |
| --- | --- | --- |
| [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer) | 是 | 提供补全、类型信息、跳转、重构和 rustfmt；工作区将后台检查命令配置为 Clippy。 |
| [CodeLLDB](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb) | 是 | 启动和单步调试 Cargo 构建出的 Rust 测试或程序。 |

rust-analyzer 的编辑器诊断不能替代完整检查；提交前仍需让 rustfmt、Clippy 和测试覆盖整个
workspace。

## 文档、配置与脚本

| 扩展 | Dev Container 自动安装 | 在本仓库中的用途 |
| --- | --- | --- |
| [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) | 否 | 检查 Markdown 标题、列表、空行和其他常见排版问题。 |
| [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) | 否 | 为 Compose、GitHub Actions 和其他 YAML 文件提供语法检查、补全和结构导航。 |
| [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml) | 是 | 编辑 `pyproject.toml`、`Cargo.toml` 和 Rust 工具链配置时提供语法、高亮和结构支持。 |
| [ShellCheck](https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck) | 是 | 在编辑 `scripts/` 和 `docker/` 下的 shell 脚本时显示 ShellCheck 诊断。 |
| [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) | 否 | 检查英文文档、注释、字符串和标识符中的常见拼写错误。 |

## 练习辅助

| 扩展 | Dev Container 自动安装 | 在本仓库中的用途 |
| --- | --- | --- |
| [LeetCode](https://marketplace.visualstudio.com/items?itemName=LeetCode.vscode-leetcode) | 否 | 在 VS Code 中浏览题目、编写题解、运行样例并提交；仓库中的正式题解仍应整理到 `leetcode/<language>/`。 |

登录 LeetCode 产生的会话信息属于本机私密数据，不应写入仓库。扩展内的运行或提交结果也不能
替代仓库测试：可复用的题解应配套放入 `tests/python/`、`tests/cpp/` 或对应 Rust crate 的
测试中。

## 安装与排查

用 VS Code 打开仓库后，执行 `Extensions: Show Recommended Extensions` 可以查看推荐列表。
进入开发容器时，`.devcontainer/*/devcontainer.json` 会安装核心扩展；其余扩展可在扩展页面
选择 `Install in Dev Container`。

如果扩展没有按预期工作，依次检查：

1. 当前窗口左下角是否显示已连接开发容器；
2. 扩展安装位置是宿主机还是当前容器；
3. `make doctor` 是否能找到对应的解释器、编译器或命令行工具；
4. C++/CUDA 项目是否已运行 `make configure` 生成 compile database；
5. 必要时执行 `Developer: Reload Window`，或重启相应语言服务器。
