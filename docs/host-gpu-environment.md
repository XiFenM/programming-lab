# Linux 宿主机 CPU+GPU 环境

这条路线用于 Docker 暂时不可用、但 Linux 宿主机可以直接访问 NVIDIA GPU 的场景。它覆盖
Python、C++、Rust、原生 CUDA、PyTorch、Triton 和 TileLang，并保留容器路线的完整静态检查。
它与轻量的 `host-cpu.sh` 并存，不会向 CPU-only Python 环境安装 GPU 包。

> 实机基线（2026-08-18）：RTX 5090、驱动 595.71.05、CUDA Toolkit 13.0.88、
> Python 3.12.13、PyTorch 2.13.0、Triton 3.7.1 和 TileLang 0.1.12。`doctor`、C++/CUDA
> CTest、默认 pytest、Rust workspace tests，以及 PyTorch/Triton/TileLang GPU 冒烟均已通过。
> 完整 `host-gpu verify` 当前会在 lint 阶段报告既有
> `leetcode/cpp/78.subsets.cpp` 告警，因此命令整体仍返回非零；这不属于环境安装失败。

## 边界与前置条件

当前锁定路线只支持 Linux x86_64。宿主机必须预先安装可用的 NVIDIA 内核驱动，并且下面的命令
能够成功列出 GPU：

```bash
nvidia-smi
```

驱动不能安全地安装在仓库目录内，也是本路线唯一必须由系统管理员提供的 GPU 组件。宿主机不需要
预装 Docker、CUDA Toolkit、cuDNN、Python、Node.js 或 Rust；这些用户态工具由仓库安装到被
Git 忽略的局部目录。初始化不执行 `sudo`，也不修改 shell 启动文件或系统软件源。

首次安装需要较大的磁盘空间和网络下载量。CUDA Toolkit、cuDNN、PyTorch 及其编译缓存可能合计
占用十余 GiB；建议预留至少 25 GiB 可用空间。

## 初始化

在仓库根目录运行：

```bash
bash scripts/host-gpu.sh init
```

初始化会完成以下工作：

1. 下载并校验固定的 Pixi 0.76.2；中断的下载保留为 `.part`，再次运行会断点续传。
2. 按 `pixi.lock` 安装 `gpu` environment，包括 Python 3.12、GCC、CMake、Ninja、ccache、
   Clang 18、GDB/LLDB、Node.js 24、CUDA Toolkit 13.0.3、cuDNN 9.20 和 CUDA 调试/分析工具。
3. 用固定的 rustup 1.29.0 安装 Rust 1.97.1、rustfmt、Clippy 和 Rust 源码。
4. 按 `uv.lock` 向独立虚拟环境同步 `dev` 组和 `gpu` extra，其中包括 PyTorch、Triton、
   TileLang、NumPy、Pandas 和 Matplotlib。
5. 运行首次诊断，确认工具没有逃逸到宿主机全局环境，并确认 PyTorch 可以访问 NVIDIA GPU。

下载、解包或网络连接中途失败时直接重新执行 `init`。已完成的 Pixi/uv 包会从仓库缓存复用，固定
版本安装器会先校验 SHA-256，再执行或解包。

## 稳定入口

初始化后始终通过同一个包装脚本进入环境：

```bash
bash scripts/host-gpu.sh doctor
bash scripts/host-gpu.sh build
bash scripts/host-gpu.sh test
bash scripts/host-gpu.sh lint
bash scripts/host-gpu.sh verify
bash scripts/host-gpu.sh shell
bash scripts/host-gpu.sh run -- python -m pytest -q gpu/triton/lesson01_vector_ops_test.py
```

这些命令也有对应的 Makefile 别名：`host-gpu-doctor`、`host-gpu-build`、
`host-gpu-test`、`host-gpu-lint`、`host-gpu-verify` 和 `host-gpu-shell`。

- `doctor` 检查锁文件、路径隔离、编译器/语言版本、NVIDIA 驱动、CUDA 13.0、cuDNN 和 GPU
  Python 包；如果已有 CMake cache，也会验证其编译器来源。
- `build` 使用 `host-gpu` CMake preset 全新配置并构建 C++ 与原生 CUDA 目标。
- `test` 运行默认 pytest、整个 Rust workspace、C++ 测试以及真实 CUDA kernel 测试。
- `lint` 对整个仓库运行 Ruff、BasedPyright、clang-format/tidy、rustfmt、Clippy 和 ShellCheck。
- `verify` 依次运行诊断、完整 lint 和测试，最后用 PyTorch 创建 CUDA tensor、运行 Triton JIT
  kernel 并导入 TileLang。

## 隔离目录

| 路径 | 内容 |
| --- | --- |
| `.pixi/envs/gpu/` | 锁定的 C/C++、CUDA、cuDNN、Node 和基础 Python 工具链 |
| `.venv-host-gpu/` | `uv.lock` 固定的开发与 GPU Python 包 |
| `.cache/host-gpu/` | Pixi、uv、Rust、ccache、Triton、TileLang 及安装器下载缓存 |
| `build/host-gpu/` | CMake CPU+CUDA 构建树与 compile database |
| `target/host-gpu/` | Rust 构建树 |

CPU-only 路线继续使用 `.pixi/envs/default/`、`.venv/`、`.cache/host-cpu/`、
`build/host-cpu/` 和 `target/host-cpu/`。两个 Pixi environment 共享一个受版本控制的
`pixi.lock`，但可变缓存、Python/Rust 环境和构建产物彼此分离。

## 可选配置

默认把下载和编译并发限制为 2，可按宿主机资源临时覆盖：

```bash
HOST_GPU_BUILD_JOBS=4 \
HOST_GPU_UV_CONCURRENT_DOWNLOADS=4 \
bash scripts/host-gpu.sh init
```

可用变量还包括：

- `HOST_GPU_CCACHE_MAXSIZE`：ccache 上限，默认 `4G`；
- `HOST_GPU_RUSTUP_DIST_SERVER` / `HOST_GPU_RUSTUP_UPDATE_ROOT`：rustup 下载源；默认分别使用
  `https://static.rust-lang.org` 和 `https://static.rust-lang.org/rustup`；
- `HOST_GPU_RUSTUP_MAX_RETRIES`：rustup 单次下载的重试上限，默认 `5`；
- `HOST_GPU_RUSTUP_DOWNLOAD_TIMEOUT`：rustup 单次网络等待秒数，默认 `60`；
- `CUDA_VISIBLE_DEVICES`：限制当前命令可见的 GPU，例如 `CUDA_VISIBLE_DEVICES=1`。

`host-gpu.sh` 会主动设置 `CUDA_HOME`、`CUDA_PATH` 和 `CUDACXX`，使 CMake 使用
`.pixi/envs/gpu/bin/nvcc`。不要用这些变量把它改回系统 CUDA，否则 `doctor` 会拒绝路径逃逸。

## 版本与故障判断

系统驱动、Pixi CUDA Toolkit 和 PyTorch 自带 CUDA 用户态运行库是三个不同层次，版本不要求逐字
相同。当前路线要求原生编译器为 CUDA 13.0，并通过真实 native CUDA、PyTorch 与 Triton kernel
执行来判断兼容性。

- `nvidia-smi` 失败：先修复宿主机驱动或设备权限；仓库脚本无法修复内核驱动。
- CMake 报找不到 GPU 架构：确认 `nvidia-smi` 成功，且没有错误设置
  `CUDA_VISIBLE_DEVICES`；`host-gpu` preset 使用当前 GPU 的 `native` 架构。
- PyTorch 看不到 GPU：运行 `host-gpu.sh doctor`，检查驱动、锁文件和虚拟环境路径，再查看
  `torch.version.cuda`；不要用系统 `pip` 修补局部环境。
- 下载中断：重新运行 `init`；Pixi/rustup 安装器使用断点文件，Pixi 和 uv 也会复用缓存。
- 只做 LeetCode CPU 练习：改用 `host-cpu.sh`，避免 GPU 依赖的磁盘和初始化成本。

修改 `pixi.toml` 后使用固定 Pixi 更新并检查 `pixi.lock`；修改 Python GPU 依赖后更新
`uv.lock`。两类变更都必须在可访问 GPU 的机器上通过 `host-gpu.sh verify`，并在提交说明中记录
GPU 型号、驱动版本和验证命令。

需要使用清华镜像时，可以按
[TUNA rustup 帮助](https://mirrors.tuna.tsinghua.edu.cn/help/rustup/) 为当次安装显式覆盖：

```bash
HOST_GPU_RUSTUP_DIST_SERVER=https://mirrors.tuna.tsinghua.edu.cn/rustup \
HOST_GPU_RUSTUP_UPDATE_ROOT=https://mirrors.tuna.tsinghua.edu.cn/rustup/rustup \
bash scripts/host-gpu.sh init
```

CPU-only 路线使用同名的 `HOST_CPU_RUSTUP_DIST_SERVER` 和
`HOST_CPU_RUSTUP_UPDATE_ROOT` 覆盖变量。镜像尚未同步固定版本时保持官方默认源。
