# Ubuntu 宿主机 CPU+GPU 环境

宿主机使用系统 APT 工具链和用户目录中的语言管理器。两条路线共享 C++、Python 解释器、Rust、
Node 等工具，分别维护项目虚拟环境、编译缓存和构建产物。CPU 路线只安装开发依赖，GPU 路线
复用已有系统 CUDA/cuDNN，缺失时补装，并增加 Python GPU 库。

## 前置条件与安装范围

支持 Ubuntu 22.04/24.04 x86_64。需要 Bash、基础 GNU 工具、网络，以及 root 或 sudo 的 APT
安装权限。GPU 路线还要求已安装可用 NVIDIA 内核驱动，并且 `nvidia-smi -L` 成功。
脚本只安装 Toolkit 和 cuDNN，不负责内核驱动安装、升级或重启系统。

初始化会修改系统 APT 包和当前用户的语言工具目录。用实际开发用户执行 `init`，脚本仅对系统
步骤调用 sudo；不要对整个初始化命令加 sudo，以免 uv、Rust、Node 装入 root 的用户目录。
GPU Toolkit、Python 库和编译缓存仍可能占用数十 GiB，建议至少预留 25 GiB。

## 初始化

```bash
bash scripts/host-gpu.sh init
```

初始化依次执行：

1. 检查系统版本、架构和 GPU 驱动访问；显示当前 APT 源，测试当前源、Ubuntu 官方源和
   清华 TUNA 源的下载速度，再询问保持现状或切换源（清华选项包括 security 更新）。
   回车默认保持现状，选择修改时先备份文件。
2. 检查 `build-essential`、CMake、Ninja、ccache、clang-format、ShellCheck、ripgrep、
   Git、curl、GPG、pkg-config 等基础包，只通过 APT 安装缺失项，不主动升级已安装包。
3. CMake 已满足 3.28+ 时直接复用；Ubuntu 22.04 的 CMake 过旧时才添加 Kitware 官方签名源
   并升级。24.04 使用发行版 CMake。
4. 复用已有 CUDA 12/13 编译器、开发头文件和运行库，以及能通过编译、链接、加载检查的
   cuDNN 9，不要求固定补丁版本，也不要求安装完整 Toolkit 元包。只有缺失组件时才准备
   NVIDIA 官方签名源并补装；同时补齐缺失的 Clang、clangd、clang-tidy、GDB、LLDB。
5. 使用 uv 官方安装器安装 uv，再执行 `uv python install 3.12` 下载并管理解释器。
6. 使用 rustup 安装固定的 Rust 1.97.1，包含 rustfmt、Clippy、rust-src；已有用户 rustup 可复用，
   全新安装时使用 rustup 1.29.0 并校验安装器 SHA-256。
7. 使用 nvm 0.40.3，优先复用已安装的 Node 24；缺少时执行 `nvm install 24`。
   CPU 路线也包含这套 Node 工具。
8. 在 `.venv-host-gpu/` 中按 `uv.lock` 安装 `dev` 组与 `gpu` extra，最后执行环境诊断。

uv、rustup 和 nvm 安装时不修改 shell 启动文件。宿主机 Ubuntu APT 源由初始化时的选择决定；
uv 安装器和 Python 下载使用官方来源，Python 包索引沿用 `pyproject.toml` 的清华源。
Rust 默认使用官方源。容器 `.env` 中的镜像与代理设置不会自动成为宿主机安装配置。

可以将系统步骤和用户步骤分开：

```bash
# 管理员准备系统包；需要时可单独用 sudo 执行此步骤
bash scripts/host-gpu.sh install-system

# 开发用户安装语言工具与项目依赖，仍会检查系统工具
bash scripts/host-gpu.sh init --skip-apt
```

CPU 路线将脚本名换成 `host-cpu.sh`。它不配置 NVIDIA 源、不安装系统 CUDA/cuDNN，Python
只同步 `--only-group dev`。两条路线的 uv/Rust/Node 工具复用用户目录中的同一份安装。

## 初始化输出停留在 Rust 完成信息

`rust-src installed` 和 `1.97.1 ... updated` 表示 Rust 安装已完成；随后会安装 nvm/Node，
再同步 Python 项目依赖。初始化现在显示六个阶段，直接下载安装器时显示进度，并设置
15 秒连接超时、180 秒单次下载上限，以及连续 30 秒低于 1 KiB/s 时中止当前尝试的限制。
下载最多重试两次，超过 300 秒后不再启动重试。失败的临时文件不会当作完整缓存复用。
这些限制只适用于脚本直接下载的安装器；rustup、nvm 和 uv 内部下载由各工具自身处理。

如果已中断初始化，且系统工具已经安装完成，可以继续运行：

```bash
bash scripts/host-gpu.sh init --skip-apt
```

这会跳过 APT 步骤，复用已安装的 Rust 及组件，并继续准备其余用户工具和依赖。
CPU 路线将命令中的 `host-gpu.sh` 换成 `host-cpu.sh` 即可。

## 优先复用 CUDA/cuDNN

脚本优先使用 `/usr/local/cuda` 指向的现有 Toolkit，其次查找其他 `/usr/local/cuda-*` 安装，
再检查系统 PATH 中的 nvcc。自定义路径可显式指定：

```bash
HOST_GPU_CUDA_HOME=/opt/cuda bash scripts/host-gpu.sh init
```

复用时保留原有版本和 APT hold，不添加精确版本锁定：

- CUDA：检查 nvcc、CUDA 12/13 系列、头文件和运行库；系统诊断实际编译并运行仓库的
  C++20 CUDA 向量加示例，验证主机编译器、驱动和 GPU 是否兼容。
- cuDNN：用系统 C++ 编译器编译并链接一个小程序，再加载库核对 cuDNN 9 接口；APT 安装和
  放在 Toolkit include/lib64 目录中的手动安装都可复用，不要求固定 Debian 包版本。
- 两者齐全：跳过 NVIDIA 源安装和 GPU 包安装。普通 Ubuntu 源检查、APT 索引刷新及缺失的
  基础工具安装仍会执行；`init --skip-apt` 才完全跳过系统安装步骤。
- 缺少 CUDA：已有 nvcc 时沿用其主次版本，补 `cuda-minimal-build-<主版本>-<次版本>`；
  完全没有时，从 APT 索引选择可用的最新 CUDA 13 系列最小构建包。驱动仍需与该 Toolkit
  兼容，脚本不会自动升级驱动。不安装完整 `cuda-toolkit-*`、Nsight 图形工具或文档元包。
- 缺少 cuDNN 开发环境：安装对应 CUDA 主版本的 `libcudnn9-dev-cuda-12` 或
  `libcudnn9-dev-cuda-13`，由 APT 补齐匹配的头文件和运行库。不主动补装整个数学库套件。

缺包安装不指定 `=精确版本`，使用 `--no-upgrade` 避免主动升级已安装的目标包；依赖解析仍可能
需要变更其他包，APT 的 hold 和冲突处理保持生效。已有包文件损坏或自定义 Toolkit 检查失败时
会报错，需修复现有安装，不会悄悄替换它。Python GPU 依赖仍单独按 `uv.lock` 同步。

## APT 源检查与选择

`init` 和 `install-system` 会在首次 `apt-get update` 前显示 `/etc/apt/sources.list` 和
`/etc/apt/sources.list.d/` 下的 `.list`、`.sources` 配置，然后测速，再询问：

```text
是否修改 Ubuntu APT 源？
  1) 保持现状（默认）
  2) Ubuntu 官方源
  3) 清华 TUNA 源（包括 Ubuntu security 更新）
请选择 [1/2/3，回车保持现状]：
```

测速会依次比较当前配置中已启用、可识别的 Ubuntu 镜像、官方 archive/security 两个地址，以及
清华源。多个当前镜像分别列出；同一个地址只请求一次，其余行复用结果。禁用条目和第三方源不
参与测速；若当前配置没有可识别的 Ubuntu 镜像，会提示跳过当前源测速，官方和清华仍会测。

每个地址使用 curl 下载当前 Ubuntu 版本的同一份 `main/binary-amd64/Packages.xz` 索引，
丢弃下载内容，显示平均速度（MiB/s）、下载量（MiB）和耗时（秒）。连接超时 3 秒，每个地址
总时限 10 秒，不重试；拒绝声明大小超过 8 MiB 的样本。超时时若已有有效下载数据，会标为
“限时样本”；HTTP、连接或证书错误显示失败状态，不阻止后续选源，也不会自动切换到最快源。
结果反映本次小文件下载吞吐，受连接、代理、缓存和网络波动影响，不代表线路带宽上限。测速使用
curl 的网络环境（包括 shell 代理），不读取 APT 专用代理配置。

测速发生在安装系统包之前。若机器尚无 curl，会提示跳过；安装系统工具后可再次执行
`install-system` 测速。默认启用测速，自动化或离线操作可显式设置 `HOST_APT_SPEED_TEST=0`
跳过下载请求，例如：

```bash
HOST_APT_SPEED_TEST=0 HOST_APT_SOURCE=keep bash scripts/host-cpu.sh install-system
```

仅替换已识别的 Ubuntu 镜像地址，包括官方、清华、阿里云、中科大、华为云、腾讯云、南京大学
和北外的常见地址。发行版、组件、`deb-src`、架构和签名选项会保留，注释和禁用条目不改动。
Kitware、NVIDIA、PPA 等第三方源保留各自地址；其他未识别的自定义镜像也保持原样。
如果所有源都无法识别，显式换源会停止，提示手动检查或选择保持现状。

官方模式使用 `archive.ubuntu.com`，独立的 security 条目使用 `security.ubuntu.com`。
清华模式将识别到的 Ubuntu 源（包括 security）切到 `https://mirrors.tuna.tsinghua.edu.cn/ubuntu/`。
若希望 security 继续使用官方源，可在初始化前自行配置，再选择保持现状。

修改前将全部受影响文件备份到 `/etc/apt/programming-lab-source-backups/<时间戳-进程号>/`，
输出中会显示具体位置。可将该目录中的文件复制回原来的相对位置恢复。已匹配目标的文件不会再次
改写；符号链接源文件需要由其管理方手动修改。

自动化运行可以显式选择，避免交互等待：

```bash
HOST_APT_SOURCE=keep bash scripts/host-cpu.sh init
HOST_APT_SOURCE=official bash scripts/host-gpu.sh install-system
HOST_APT_SOURCE=tuna bash scripts/host-gpu.sh init
```

这三个值分别表示保持现状、官方源和清华源。未设置且无法读取输入时会退出，不会默认换源或继续
安装系统包。`init --skip-apt` 完全跳过源检查、测速、选择及系统包安装。

## 目录与激活

| 内容 | 位置 |
| --- | --- |
| APT 原生工具 | `/usr/bin/` 等系统路径 |
| CUDA Toolkit | 自动检测的已有安装；可用 `HOST_GPU_CUDA_HOME` 指定 |
| cuDNN 运行库与头文件 | 现有系统目录或 Toolkit 的 include/lib64；缺少时由 APT 补装 |
| uv | `~/.local/bin/uv` |
| uv 管理的 Python | `~/.local/share/uv/python/` |
| Python 下载缓存 | `~/.cache/uv/` |
| Rust | `~/.cargo/`、`~/.rustup/`，包装脚本设置 `RUSTUP_TOOLCHAIN=1.97.1` |
| nvm / Node | `~/.nvm/` |
| CPU / GPU Python 依赖 | `.venv/` / `.venv-host-gpu/` |
| 路线下载与编译缓存 | `.cache/host-cpu/` / `.cache/host-gpu/` |
| CMake 产物 | `build/host-cpu/` / `build/host-gpu/` |
| Cargo 产物 | `target/host-cpu/` / `target/host-gpu/` |

包装脚本清理可能干扰编译的外部环境变量，选择 `/usr/bin/gcc`、`/usr/bin/g++`，加载 nvm 的
Node 24，再激活对应 venv。GPU 路线设置 `CUDA_HOME`、`CUDA_PATH`、`CUDACXX` 指向检测到的
CUDA Toolkit，并让 nvcc 使用系统 GCC。`shell` 会加载 nvm，交互式终端可直接使用 `nvm`。

已有虚拟环境若来自其他解释器来源或其基础解释器已不存在，`init` 会重建该 venv 后按锁文件同步。
有效的 uv Python 3.12 环境会保留。重建仅处理带 `pyvenv.cfg` 的生成目录，拒绝符号链接或普通
目录。旧工具缓存不参与新环境；用户可自行移除已不用的旧安装目录。

VS Code 默认配置面向容器。宿主机 GPU 开发应选择 `.venv-host-gpu/bin/python`、`host-gpu`
CMake preset 和 `build/host-gpu/compile_commands.json`；CPU 路线使用对应的 CPU 路径。

## 日常命令与验证范围

```bash
bash scripts/host-gpu.sh doctor
bash scripts/host-gpu.sh build
bash scripts/host-gpu.sh test
bash scripts/host-gpu.sh lint
bash scripts/host-gpu.sh verify
bash scripts/host-gpu.sh shell
bash scripts/host-gpu.sh run -- python -m pytest -q gpu/triton/lesson01_vector_ops_test.py
```

Makefile 提供 `host-gpu-install-system`、`host-gpu-init`、`host-gpu-doctor`、`host-gpu-build`、
`host-gpu-test`、`host-gpu-lint`、`host-gpu-verify`、`host-gpu-shell` 别名。

- `doctor` 检查系统工具、uv Python 3.12 的实际来源、项目 venv、锁文件、Rust、nvm/Node、
  NVIDIA 驱动、CUDA 实际编译运行和 cuDNN 编译链接加载，并确认 PyTorch 能访问 GPU；
  已有 CMake cache 也会校验。
- `build` 使用 `host-gpu` preset 重新配置 CMake，编译登记的 C++/CUDA 目标。GPU 架构为 native。
- `test` 运行默认 pytest、Rust workspace tests、C++ 和原生 CUDA 测试。
- `lint` 包含 Ruff、BasedPyright、clang-format/tidy、rustfmt、Clippy、ShellCheck。
- `verify` 只验收环境：运行 `doctor`，GPU 路线再执行 PyTorch CUDA 运算、Triton JIT kernel
  和 TileLang 导入检查。CUDA 和 Triton 探针独立放在 `scripts/`，不读取或检查 `leetcode/`、
  `gpu/` 中的练习代码，也不调用 `lint`、`build` 或 `test`。CPU 路线只运行环境诊断。
  练习的静态检查和测试请单独运行 `lint`、`test`，课内 Triton 测试需要显式指定文件。

旧安装策略下曾在 RTX 5090 上通过环境和 GPU 冒烟检查；这些历史结果不验证本次 APT 初始化。
旧文档记录过的题解静态检查问题由 `lint` 单独报告，不再阻断 `verify` 的环境验收。
本次策略迁移的自动化测试覆盖安装命令选择、CPU/GPU 分离、解释器选择、旧环境迁移和参数错误。

迁移验证（2026-09-23）在 Ubuntu 22.04 上完成：官方安装器在临时目录安装 uv 0.12.18、
Python 3.12.14、Rust 1.97.1、nvm 0.40.3 和 Node 24.21.0，并按仓库 `uv.lock` 同步 CPU 开发依赖。
使用这套 Python 执行 `python -m pytest -q tests/python`：43 项通过，6 项因无 Docker Compose
跳过；固定 Rust 执行 `cargo test --workspace --all-targets --locked`：3 项通过，Clippy 通过。
系统 GCC 11.4 搭配临时 CMake/Ninja 成功构建并通过 CPU CTest。改动代码通过 Ruff、BasedPyright、
ShellCheck 和 Bash 语法检查。系统 APT 命令使用替身验证，未实际执行；完整 APT 初始化与 GPU
运行仍需要在按上述步骤配置的机器上验收。

## 缺失 GPU 组件的 APT 安装失败

已有 CUDA/cuDNN 通过检查时不需要 NVIDIA 包索引。只有补装缺失组件时，脚本才配置 NVIDIA
独立的 APT 源；清华 Ubuntu 源不提供这些 NVIDIA 包。

已确认的一种情况是：机器仍安装着 `cuda-keyring`，但其源文件已被清理。脚本使用
`dpkg --force-confmiss -i` 恢复缺失的配置，同时保留仍存在的自定义源和 pin 文件。所有 APT
更新使用 `APT::Update::Error-Mode=any`；索引下载失败立即停止，缺失包没有候选版本也会提前
报错。已有源文件若被禁用或改成其他地址，需要检查该文件及更新错误。

可保留当前源并跳过测速，重新执行初始化：

```bash
HOST_APT_SOURCE=keep HOST_APT_SPEED_TEST=0 bash scripts/host-gpu.sh init
```

旧脚本中强制升级 CUDA/cuDNN、要求解除旧 cuDNN hold 的策略已取消。正常可用的现有版本会
直接复用；无需为迁就脚本去解除 hold 或补齐完整 Toolkit。若缺失组件的依赖确实与 hold 冲突，
由 APT 报告后再处理，脚本不自动解除锁定。

## 版本与更新策略

- Python 项目依赖继续由 `pyproject.toml` 和 `uv.lock` 管理，初始化使用 `--locked`。
- Rust 固定 1.97.1；nvm 固定 0.40.3；Python 3.12 和 Node 24 固定系列，补丁版本可变化。
- CUDA/cuDNN 优先复用可用的已有安装，不锁定补丁或 Debian 包版本；缺失项的版本由 APT 解析。
  CUDA 12/13、cuDNN 9 是当前接口支持范围，兼容性通过实际检查验证。
- GCC、CMake、Clang 等优先复用，缺失或不满足 CMake 最低要求时才通过软件源补装。两条宿主机路线共享这些系统组件，不承诺相互隔离。
- GPU Python 包可能携带自己的 CUDA/cuDNN 用户态库。系统 Toolkit、系统 cuDNN 和 PyTorch
  报告的版本属于不同层次，兼容性要通过实际 kernel 运行验证。

默认编译和 uv 下载并发为 2，可以临时覆盖：

```bash
HOST_GPU_BUILD_JOBS=4 HOST_GPU_UV_CONCURRENT_DOWNLOADS=4 bash scripts/host-gpu.sh init
```

其他选项包括 `HOST_GPU_CCACHE_MAXSIZE`（默认 `4G`）、`HOST_GPU_RUSTUP_DIST_SERVER`、
`HOST_GPU_RUSTUP_UPDATE_ROOT`，以及 `CUDA_VISIBLE_DEVICES`。CPU 对应变量使用 `HOST_CPU_`
前缀，ccache 默认 `1G`。下载失败可重新执行 `init`；完整安装器文件和 uv 缓存会复用，未完成的
安装器下载会重试。

安装机制参考：[Kitware APT](https://apt.kitware.com/)、
[NVIDIA CUDA 安装指南](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)、
[cuDNN Linux 安装指南](https://docs.nvidia.com/deeplearning/cudnn/installation/latest/linux.html)、
[Ubuntu 清华源配置说明](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)、
[uv 安装器](https://docs.astral.sh/uv/reference/installer/)、
[nvm 0.40.3](https://github.com/nvm-sh/nvm/tree/v0.40.3)。
