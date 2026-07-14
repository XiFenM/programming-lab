# Programming Lab

一个以 NVIDIA GPU 开发容器为核心的编程练习仓库，用于 LeetCode、CUDA、Triton 和
TileLang。LeetCode 主要支持 Python、C++ 和 Rust；日常编辑、格式化、静态检查、构建和
测试都设计为在容器内完成，宿主机只需要提供 NVIDIA 驱动、Docker、NVIDIA Container
Toolkit 和 VS Code。

> 当前交付状态：本次只创建了仓库文件。按要求，**没有构建镜像、启动容器、下载安装依赖、
> 生成 Python 锁文件或运行任何初始化/检查/测试脚本**。因此文档中的版本输出和测试通过状态
> 不是伪造的执行结果；首次进入容器后需要由你执行初始化和验收。`uv.lock` 会在首次初始化时
> 生成，确认环境可用后建议提交到 Git。当前目录已经初始化为默认分支 `main` 的本地 Git
> worktree，但尚未创建提交、配置 Git 用户信息或添加远端。

## 已配置的内容

- 基础镜像固定为 `nvidia/cuda:13.0.3-cudnn-devel-ubuntu24.04`，包含 CUDA 13.0、cuDNN
  和 `nvcc`。
- Ubuntu/Ubuntu Ports、NVIDIA CUDA apt 软件源使用清华 TUNA 镜像；uv/PyPI、Node.js
  release 和 rustup 同样使用清华镜像，Cargo crate 使用 RsProxy sparse 镜像。
- 使用非 root 用户 `coder` 开发，可通过 `.env` 将 UID/GID 对齐宿主机，减少 bind mount
  文件权限问题。
- 未主动安装 Ubuntu 的 `python3`；使用 uv 官方安装命令安装 uv，再由 uv 下载 CPython
  3.12 并创建项目虚拟环境。
- 使用 nvm `v0.40.3` 的官方安装脚本，并执行 `nvm install 24` 安装 Node.js 24。
- 使用 rustup 安装 stable Rust，以及 `cargo`、`rustfmt`、Clippy 和 Rust 源码组件。
- C++/CUDA 使用 C++20、CMake Presets、Ninja、ccache、clangd、clang-format、clang-tidy、
  GDB/LLDB 和 NVIDIA Nsight VS Code Edition。
- Python 使用 Ruff、BasedPyright strict 和 pytest；Rust 使用 rustfmt、Clippy 和 Cargo
  workspace。
- 提供 Python/C++/Rust 的 Two Sum 示例和测试、原生 CUDA 与 Triton 向量加法 GPU
  冒烟程序、TileLang 安装探针。
- 提供初始化、诊断、格式化、静态检查、测试和全量验收脚本，并由 Makefile 统一入口。
- 工作区可选宿主机 bind 双向同步或构建时一次性快照复制；Python/编译缓存可选命名卷持久化
  或随容器删除。
- 提供四套 VS Code Dev Container 组合、编辑器设置、推荐插件、任务和调试配置。
- 提供可选的本地 pre-commit hook，以及不依赖 GPU 的 GitHub Actions 代码质量检查。

## 仓库结构

```text
.
├── Dockerfile                       # CUDA 13 开发镜像、uv/nvm/rustup 和工具链
├── compose.yaml                     # GPU、镜像源、运行参数和调试权限的公共配置
├── compose.bind.yaml                # 宿主机源码 bind 双向同步
├── compose.copy.yaml                # 构建时把源码快照复制进镜像
├── compose.persist.yaml             # uv/Cargo/GPU 编译缓存命名卷
├── compose.copy-persist.yaml        # 快照模式的 /workspace 持久卷
├── .devcontainer/                   # bind/copy × persistent/ephemeral 四套配置
├── docker/                          # Bash 环境和容器专用 Cargo 镜像配置
├── pyproject.toml                   # Python/GPU 依赖及 Ruff/Pyright/pytest 配置
├── .python-version                  # uv 管理的 CPython 3.12
├── .nvmrc                           # nvm 使用的 Node.js 24 主版本
├── CMakeLists.txt                   # C++ 与 CUDA 示例目标
├── CMakePresets.json                # Debug/Release + Ninja
├── .clang-format
├── .clang-tidy
├── Cargo.toml                       # Rust workspace 与统一 lint 级别
├── rust-toolchain.toml
├── .cargo/config.toml
├── leetcode/
│   ├── python/                      # Python 题解
│   ├── cpp/                         # C++ 题解
│   └── rust/                        # 每题一个 Rust crate
├── gpu/
│   ├── cuda/vector_add.cu           # 原生 CUDA 编译/运行测试
│   ├── triton/vector_add.py         # Triton JIT 编译/运行测试
│   └── tilelang/                    # TileLang 版本探针和练习说明
├── tests/
│   ├── python/
│   └── cpp/
├── scripts/
│   ├── init-env.sh                  # uv 初始化与可选 Git hook
│   ├── container.sh                 # 显式选择工作区和持久化模式
│   ├── doctor.sh                    # 工具链、uv Python 和 NVIDIA 运行时诊断
│   ├── lint.sh                      # 全语言静态质量检查
│   ├── format.sh                    # 全语言格式化
│   ├── test.sh                      # Python/Rust/C++/CUDA 测试
│   ├── check_python_gpu.py          # PyTorch/Triton/TileLang GPU 栈验收
│   └── verify-env.sh                # 完整验收入口
├── .vscode/                         # 插件、设置、任务和调试配置
├── .pre-commit-config.yaml          # 可选的本地静态检查 hook
└── .github/workflows/quality.yml    # 无 GPU 的云端质量检查
```

## 宿主机要求

推荐 Linux；Windows 建议使用带 GPU 支持的 WSL2。macOS 不能运行这个 NVIDIA CUDA
容器。

1. NVIDIA GPU 和能够支持 CUDA 13.0 的宿主机驱动。容器使用宿主机驱动，而不是在容器
   中安装内核驱动。
2. Docker Engine 与较新的 Docker Compose v2；建议 Compose 2.30+，需要支持 `gpus: all`。
3. [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)。
4. VS Code，以及宿主机侧的 `Dev Containers` 插件（如果使用推荐的一键方式）。
5. 足够磁盘空间。CUDA devel 镜像、PyTorch、Triton、TileLang 和编译缓存合计可能需要
   数十 GiB。

宿主机应先能正常执行 `nvidia-smi`。如果 Docker 的 GPU 转发尚未配置，可参考 NVIDIA
Container Toolkit 文档先验证一个带 `--gpus all` 的 CUDA 容器；仓库内部配置无法修复宿主机
驱动或 Docker runtime 的问题。

## 首次使用

当前目录已经由 Git 管理，默认分支为 `main`。首次提交、Git 用户信息和远端仓库请根据你的
实际账号与托管平台自行配置。

### 1. 配置本机参数与镜像源

复制环境变量模板：

```bash
cp .env.example .env
```

查看宿主机的 `id -u` 和 `id -g`，把 `.env` 中的 `LOCAL_UID`、`LOCAL_GID` 改成对应值。
默认值都是 `1000`，如果宿主机恰好也是该值则无需修改。`.env` 已被 Git 忽略。
多 GPU 主机还可以把 `NVIDIA_VISIBLE_DEVICES` 从 `all` 改成索引或 UUID 列表，例如 `0` 或
`0,1`。

模板还包含以下国内镜像，可在 `.env` 中独立覆盖：

- `UBUNTU_MIRROR`：清华 Ubuntu 镜像；
- `UBUNTU_PORTS_MIRROR`：清华 Ubuntu Ports 镜像；
- `NVIDIA_APT_MIRROR`：清华 NVIDIA CUDA 软件源镜像；
- `PYPI_INDEX_URL`：清华 PyPI 镜像，传给 uv 和兼容的 pip 构建过程；
- `NVM_NODEJS_ORG_MIRROR`：清华 Node.js release 镜像，供 nvm 下载 Node 二进制；
- `RUSTUP_DIST_SERVER` / `RUSTUP_UPDATE_ROOT`：清华 rustup 镜像。

UID/GID 会在构建镜像时用于创建 `coder`。如果先构建后再修改，需要重新构建镜像；如果还
复用了旧的命名卷，参见“常见问题”中的权限处理。

### 2. 选择工作区与持久化模式

启动时必须在两个维度上作出选择，`scripts/container.sh` 不会静默替你决定：

| 工作区 | 持久化 | 行为 |
| --- | --- | --- |
| `bind` | `persistent` | 宿主机与容器双向实时同步；uv、Cargo、编译缓存使用命名卷。适合日常开发 |
| `bind` | `ephemeral` | 源码仍双向同步；环境和缓存只在容器可写层，删除容器后丢失 |
| `copy` | `persistent` | 构建时复制源码快照，不与宿主机同步；`/workspace` 和缓存放入命名卷 |
| `copy` | `ephemeral` | 构建时复制源码快照，不同步、不使用命名卷；删除容器后所有容器内改动丢失 |

`bind` 模式最直观，但容器内任何源码修改会立刻修改宿主机。`copy` 模式通过 Dockerfile 的
`workspace-copy` target 在构建时执行一次 `COPY`，`.git`、`.env`、构建产物等由
`.dockerignore` 排除，因此容器内快照不包含宿主机 Git 元数据和私密环境文件。

`copy + persistent` 的 `workspace-data` 卷只在第一次创建时由镜像中的 `/workspace` 填充。
之后即使重新构建镜像，也不会覆盖该卷内的练习代码。这可以保护容器内改动，但意味着要获得
新的宿主机快照，需要先导出需要保留的内容，再显式删除旧卷并重建。

这里的 `ephemeral` 指“不使用命名卷”：执行 stop/restart 时容器可写层仍存在；执行 down、
删除或重建容器时才会丢失。

### 3. VS Code Dev Container

1. 用 VS Code 打开仓库。
2. 执行命令面板中的 `Dev Containers: Reopen in Container`。
3. VS Code 会列出四套配置：`bind + persistent`、`bind + ephemeral`、
   `copy + persistent`、`copy + ephemeral`，选择符合本次工作的组合。
4. VS Code 会合并公共 Compose 文件与对应覆盖文件，构建并启动 `dev` 服务，随后执行
   `bash scripts/init-env.sh`。
5. 初始化脚本会让 uv 下载/确认 CPython 3.12，创建
   `/home/coder/.venvs/programming-lab`，解析 `pyproject.toml`，安装 GPU 与开发依赖，并在
   当前容器工作区生成 `uv.lock`。
6. 打开容器终端，执行 `make doctor`，然后执行 `make verify`。

在 `bind` 模式中，生成的 `uv.lock` 会同步回宿主机；在 `copy` 模式中不会，若要保留它和
容器内代码，需要使用下节的 `export` 操作。

首次构建和首次 Python 依赖解析下载量较大。VS Code 的 `postCreateCommand` 只有在容器创建
阶段运行；重连已有容器不会每次重装全部依赖。只有 persistent 组合会跨容器复用命名卷缓存。

### 4. 纯命令行方式

脚本要求显式给出工作区和持久化模式。例如，使用同步源码与持久缓存：

```bash
bash scripts/container.sh build bind persistent
bash scripts/container.sh up bind persistent
bash scripts/container.sh init bind persistent
bash scripts/container.sh shell bind persistent
```

进入容器后：

```bash
make init
make doctor
make verify
```

使用不与宿主机同步、也不保留命名卷的快照容器：

```bash
bash scripts/container.sh up copy ephemeral
bash scripts/container.sh init copy ephemeral
```

从 copy 模式导出容器工作区：

```bash
bash scripts/container.sh export copy persistent ./container-export
```

生命周期操作也必须带相同模式，以便脚本合并相同的 Compose 文件：

```bash
bash scripts/container.sh stop bind persistent
bash scripts/container.sh down bind persistent
```

`down` 删除容器但保留已声明的命名卷；显式的 `destroy` 会执行带 volumes 的清理，删除当前
组合声明的 uv Python、虚拟环境、源码快照与编译缓存。copy 模式下应先 export，再使用
`down`（ephemeral）或 `destroy`（persistent）。

四种组合共用同一个 Compose project 和 `dev` 服务，目的是一次只运行一种模式。切换组合时
Compose 可能重建现有容器；若当前是 copy + ephemeral，必须在切换前导出修改，否则容器可写层
会随重建消失。

`compose.yaml` 只是公共基底，故意不自行决定工作区挂载方式。推荐通过 `container.sh` 使用；
需要直接调用 Compose 时，必须至少叠加 `compose.bind.yaml` 或 `compose.copy.yaml`，再按需叠加
持久化文件。容器入口还会检查 `/workspace/pyproject.toml`，若只启动公共基底，会给出模式选择
提示并退出，而不是运行一个空工作区。

## 容器设计说明

### CUDA 与系统工具链

`Dockerfile` 的基础镜像使用精确 tag：

```dockerfile
ARG BASE_IMAGE=nvidia/cuda:13.0.3-cudnn-devel-ubuntu24.04
```

在第一次 `apt-get update` 之前，Dockerfile 会同时处理 Ubuntu 24.04 常见的 deb822
`ubuntu.sources` 和传统 `sources.list`：

- `archive.ubuntu.com` / `security.ubuntu.com` → 清华 Ubuntu；
- `ports.ubuntu.com/ubuntu-ports` → 清华 Ubuntu Ports；
- `developer.download.nvidia.com/compute/cuda/repos` → 清华 NVIDIA CUDA 镜像。

APT 还配置了 5 次重试和 30 秒 HTTP/HTTPS 超时。所有镜像地址都是 Docker build args，既有
清华默认值，也能从 `.env` 覆盖，不需要修改 Dockerfile。

这些 URL 会进入 Compose 配置或镜像环境，不应直接写入带用户名、密码或访问令牌的私有镜像
地址；私有源凭据应改用 Docker BuildKit secret 或运行时 secret。

Ubuntu 层安装了 CMake、Ninja、GCC/G++、Clang/clangd、clang-format、clang-tidy、GDB、
LLDB、ccache、ShellCheck、ripgrep、Git、OpenSSH client 等开发工具。没有显式安装 apt 的
`python3`。某些 Ubuntu 工具即使间接依赖系统 Python，也不会被本项目选作解释器；uv 通过
`UV_PYTHON_PREFERENCE=only-managed` 强制选择 uv 管理的 Python。

Compose 做了以下设置：

- `gpus: all` 把所有可见 NVIDIA GPU 交给容器；可按需调整 `NVIDIA_VISIBLE_DEVICES`。
- `NVIDIA_DRIVER_CAPABILITIES=compute,utility` 只打开计算和诊断能力。
- `shm_size: 8gb` 避免深度学习/GPU 测试过早耗尽默认共享内存。
- `SYS_PTRACE` 与 `seccomp=unconfined` 用于容器内 GDB/LLDB 调试。这个配置降低了默认
  seccomp 限制，只应把该容器用于可信的本地开发代码。
- `compose.bind.yaml` 与 `compose.copy.yaml` 决定工作区是双向挂载还是镜像快照。
- `compose.persist.yaml` 可选地挂载 uv、Cargo、ccache、Triton 和 TileLang 命名卷。
- `compose.copy-persist.yaml` 只用于 copy + persistent，为 `/workspace` 添加快照持久卷。

Dockerfile 包含三个 stage：`toolchain` 安装工具，`workspace-copy` 在其上复制源码，最后的
`runtime` 不包含源码快照。bind 模式构建 `runtime`，所以普通源码修改不会让工具链镜像失效；
copy 模式显式构建 `workspace-copy`，每次取得构建时的宿主机文件快照。

### Python 与 uv

uv 使用要求的官方命令安装：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装脚本本身仍来自 Astral 官方地址；第三方 Python 包解析和下载通过：

```text
UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple
PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

其中 `UV_DEFAULT_INDEX` 是 uv 实际使用的默认索引，`PIP_INDEX_URL` 供少数构建后端或用户手动
调用 pip 时保持一致。二者都来自 `.env` 的 `PYPI_INDEX_URL`，可以临时换回官方 PyPI 或其他
内部镜像。`uv python install` 下载的是 uv 管理的 CPython 发行物，不经过 PyPI 镜像。

镜像构建阶段执行 `uv python install 3.12`，项目初始化阶段再次以幂等方式确认该版本。项目
虚拟环境不放在 `/workspace/.venv`，而放在：

```text
/home/coder/.venvs/programming-lab
```

把虚拟环境放在工作区之外，可以避免 bind 模式覆盖环境，也避免 copy 模式导出源码时顺带复制
庞大的 `.venv`。persistent 模式把 uv 解释器、虚拟环境与下载缓存挂入命名卷；ephemeral 模式
仍使用相同路径，但数据位于容器可写层，删除容器即消失。交互式 Bash 在环境存在时自动激活，
脚本和文档仍优先使用 `uv run`，避免意外调用其他 Python。

`pyproject.toml` 当前包括：

- 运行/GPU 依赖：NumPy、PyTorch、Triton、TileLang；
- 开发依赖组：Ruff、BasedPyright、pytest、pytest-cov、pre-commit；
- Python 版本范围：`>=3.12,<3.13`；
- `tool.uv.package = false`，因为本仓库是练习集合，不需要把根目录构建成 Python wheel。

GPU 包在 `pyproject.toml` 中没有预设彼此可能冲突的最低版本，而是让 uv 第一次选择当前索引中
同时支持 Python 3.12 的最高兼容组合，再由 `uv.lock` 精确固定。这样不会在未实际解析前假定
某个 TileLang 版本一定兼容某个 PyTorch/Triton 版本；可复现性由提交后的锁文件提供。

首次没有 `uv.lock` 时，`init-env.sh` 会解析依赖并生成它；锁文件存在后，脚本使用
`uv sync --locked`，防止初始化时静默改锁。如果修改了依赖，建议在容器内显式执行：

```bash
uv lock
uv sync --locked --group dev
```

或者使用 `uv add <package>` / `uv add --group dev <package>`。确认新的 GPU 依赖组合通过
`make verify` 后再提交 `pyproject.toml` 和 `uv.lock`。

没有强行配置一个假定存在的 CUDA 13 PyTorch wheel index。PyPI 上的 PyTorch wheel 通常
携带自己的 CUDA 用户态依赖，它报告的 `torch.version.cuda` 可能与系统 `nvcc 13.0` 不同，
这本身不等于错误；关键是宿主机驱动兼容，并且实际 PyTorch/Triton kernel 能运行。首次生成
锁文件后，PyTorch、Triton 与 TileLang 的具体兼容组合由 `uv.lock` 固定。

### Node.js 与 nvm

Node 使用给定的 nvm 官方流程：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
. "$HOME/.nvm/nvm.sh"
nvm install 24
```

nvm 安装脚本仍来自指定的 GitHub 官方地址；Node 24 二进制下载通过
`NVM_NODEJS_ORG_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/nodejs-release` 使用清华镜像。

镜像还设置了 Node 安装目录的稳定链接，因此非交互命令也能直接找到 `node` 和 `npm`；交互式
shell 会加载 `nvm.sh`，仍可使用完整 nvm 命令。

仓库根目录的 `.nvmrc` 同样记录为 `24`，便于在交互式 shell 中使用 `nvm use` 时与镜像配置
保持一致。

`nvm install 24` 的含义是“构建镜像当时最新的 24.x”，不是固定补丁版本。因此示例中的
`v24.18.0` / `npm 11.16.0` 只有在它们恰好是当时 Node 24 的解析结果时才会完全一致；
`doctor.sh` 强制 Node 主版本为 24、npm 主版本为 11，并打印实际完整版本。如果希望逐字固定版本，
把 Dockerfile 中的 `nvm install 24` 和 `nvm which 24` 同时改成所需完整版本，再重建镜像。

### Rust

Rust 通过 rustup 的官方脚本按 `coder` 用户安装，不污染 apt 工具链。rustup 的工具链与组件
下载使用清华 `rustup` 镜像；Cargo 第三方库则通过容器内的 `~/.cargo/config.toml`（来源文件为
`docker/cargo-config.toml`）把 crates.io 替换为
`sparse+https://rsproxy.cn/index/`。这里没有使用传统的 Git 全量索引镜像，因为 sparse 协议
首次使用下载量更小，RsProxy 同时针对中国大陆提供 crate 文件加速。

`rust-toolchain.toml` 选择 stable，并安装 Clippy、rustfmt 和 `rust-src`。根 `Cargo.toml` 是
edition 2024 workspace，会自动包含 `leetcode/rust/*` 下的 crate，并统一启用：

- `unsafe_code = "forbid"`；
- Clippy `all` 与 `pedantic`；
- 禁止 `dbg!`、`todo!`、`unimplemented!`、`unwrap` 和 `expect`。

## 常用命令

以下命令都应在容器内执行。

| 命令 | 作用 | 是否修改源码/状态 |
| --- | --- | --- |
| `make help` | 显示入口 | 否 |
| `make init` | 安装/同步 uv Python 环境 | 会创建环境和可能首次生成 `uv.lock` |
| `make hooks` | 初始化环境；若当前是 Git worktree，再安装 pre-commit hook | 可能修改 `.git/hooks` |
| `make doctor` | 检查工具路径、版本、uv Python、GPU runtime | 只诊断 |
| `make configure` | 生成 `build/debug` 与 compile database | 会写 `build/` |
| `make build` | 编译 C++ 和 CUDA 示例 | 会写 `build/` 和缓存 |
| `make test` | 运行 Python、Rust、C++、CUDA 测试 | 会构建原生目标 |
| `make lint` | Ruff、Pyright、clang-format/tidy、Clippy、ShellCheck | 会生成 CMake 配置/缓存，不改源码 |
| `make format` | 自动格式化 Python、C++、CUDA、Rust | **会修改源码** |
| `make verify` | doctor + lint + 全语言测试 + Python GPU 栈 | 完整且耗时 |

常用的单项命令：

```bash
# Python
uv run --frozen pytest tests/python/test_two_sum.py
uv run --frozen ruff check .
uv run --frozen basedpyright

# C++ / CUDA
cmake --preset debug
cmake --build --preset debug --parallel
ctest --preset debug

# Rust
cargo test --workspace --all-targets --locked
cargo clippy --workspace --all-targets --locked -- -D warnings

# Triton / TileLang
uv run --frozen python -m gpu.triton.vector_add
uv run --frozen python -m gpu.tilelang.check_install
```

## 环境验收具体做什么

`make verify` 不是只打印版本，它依次完成：

1. `doctor.sh` 检查 uv、Node/npm/nvm、Rust、CMake/Ninja、Clang 工具、`nvcc`、
   `nvidia-smi`、cuDNN 动态库、ShellCheck 等命令/组件。
2. 确认 Node 主版本为 24、npm 主版本为 11，确认项目虚拟环境的解释器实际指向 uv 管理目录。
3. 调用 `nvidia-smi`，验证 Docker 到宿主机 NVIDIA 驱动的通路。
4. 运行 Ruff lint/format check 和 BasedPyright strict。
5. 运行 clang-format，生成 CMake compile database 后运行 clang-tidy。
6. 运行 rustfmt 与 Clippy。
7. 运行 ShellCheck。
8. 运行 pytest 和 Cargo tests。
9. 用 `nvcc`/CMake 编译 CUDA 13 向量加法，实际分配显存、启动 kernel、拷回并断言结果。
10. 用 PyTorch 实际创建 CUDA tensor。
11. JIT 编译并运行 Triton 向量加法，与 PyTorch 结果比较。
12. 导入 TileLang，打印实际锁定版本和模块位置。

TileLang 的导入检查是有意设置的边界：TileLang DSL 仍在快速变化，在未生成实际 `uv.lock`
之前硬编码某个版本的 kernel 模板容易产生“仓库看似完整、首次安装却 API 不兼容”的假象。
首次锁定版本后，按照 `gpu/tilelang/README.md` 和该版本官方示例添加 kernel，并同时保存参考
实现、正确性测试和 benchmark。CUDA、Triton 两条路径已经提供真实 kernel 级验收。

## 代码质量配置

### Python

- Ruff 同时负责 lint、import 排序和格式化，目标 Python 3.12，行宽 100。
- 启用了 Pyflakes、pycodestyle、BugBear、性能、简化、升级与 Ruff 自有规则等规则集。
- BasedPyright 对 `leetcode/python` 和 `tests/python` 使用 strict 类型检查。
- GPU DSL 常使用动态装饰器和生成式 API，因此 GPU 目录由 Ruff 检查语法与风格，但没有为了
  “零类型错误”而大量添加无意义的忽略注释。

### C++ / CUDA

- C++20/CUDA C++20，启用 `-Wall -Wextra -Wpedantic -Wconversion -Wshadow`。
- clang-format 基于 Google 风格，行宽 100。
- clang-tidy 启用 bugprone、performance、portability 和一组低噪声 modernize/readability
  检查；严重类别按错误处理。
- CMake 导出 `build/debug/compile_commands.json` 供 clangd 和 clang-tidy 使用。
- CUDA 架构默认是 `native`，即按当前可见 GPU 构建，避免默认生成与硬件无关的大量架构。

### Rust

- edition 2024 workspace；每道题可以作为独立 crate。
- 保存时 rustfmt；rust-analyzer 后台调用 Clippy。
- CI 和脚本都以 `-D warnings` 运行 Clippy，避免告警逐渐积累。

### pre-commit

hook 默认不自动安装，以免仓库初始化未经同意修改 `.git/hooks`。需要时执行 `make hooks`。
当前 hook 调用完整 `scripts/lint.sh`，检查严格但比普通轻量 hook 慢；适合希望提交前一次性完成
所有静态检查的用法。copy 模式的构建上下文排除了 `.git`，因此其中默认不是 Git worktree，
`make hooks` 会跳过 hook 安装；需要 Git 操作时优先使用 bind 模式。

## 添加新练习

### Python LeetCode

建议文件名使用合法模块名，例如：

```text
leetcode/python/p0001_two_sum.py
tests/python/test_p0001_two_sum.py
```

题解函数保留完整类型标注，测试至少覆盖标准输入、边界输入和不存在/非法输入。运行单题：

```bash
uv run --frozen pytest tests/python/test_p0001_two_sum.py
```

### C++ LeetCode

建议把可提交的算法放在 `leetcode/cpp/`，测试放在 `tests/cpp/`。为新题在
`CMakeLists.txt` 增加一个 executable 和 CTest；这样既能保留 LeetCode 风格接口，又能在
本地独立验证。配置后 clangd 会从 compile database 获得准确 include path 和 C++20 参数。

### Rust LeetCode

在 `leetcode/rust/<题名>/` 新建 library crate。根 workspace 的 glob 会自动发现它；crate 的
`Cargo.toml` 建议继承：

```toml
[package]
edition.workspace = true
rust-version.workspace = true

[lints]
workspace = true
```

算法单元测试直接放在 `src/lib.rs` 的 `#[cfg(test)]` 模块，或放到 crate 的 `tests/`。

### CUDA / Triton / TileLang

- 原生 CUDA 放在 `gpu/cuda/`，并在 CMake 中建立目标与 CTest。
- Triton 放在 `gpu/triton/`，保留一个 PyTorch reference，并测试非 block 整倍数尺寸。
- TileLang 放在 `gpu/tilelang/`，以 `uv.lock` 中的实际版本文档为准。
- benchmark 要先 warm-up，再同步 GPU；记录 GPU、dtype、shape、版本和编译选项，不要只记录
  一次异步 kernel launch 的主机耗时。

## VS Code 配置

`.devcontainer/` 下有四个子配置。执行 `Dev Containers: Reopen in Container` 时按本次需求
选择 bind/copy 与 persistent/ephemeral 组合。四套配置共享相同的 GPU、用户、初始化脚本和
插件清单，只在 Compose 覆盖文件上不同。copy 模式中 VS Code 编辑的是容器快照，不会改动
宿主机；关闭前需要自行 export 希望保留的内容。

`.vscode/extensions.json` 推荐了：

- Dev Containers、Docker；
- Python、debugpy、Ruff、BasedPyright；
- CMake Tools、clangd、Microsoft C/C++ 调试器、NVIDIA Nsight；
- rust-analyzer、CodeLLDB；
- Even Better TOML、YAML、ShellCheck、Markdownlint、EditorConfig、Error Lens；
- VS Code LeetCode 插件。

clangd 和 Microsoft C/C++ IntelliSense 同时启用会产生重复诊断，因此配置保留 Microsoft 插件
的 GDB 调试能力，但关闭它的 IntelliSense，由 clangd 负责补全和 clang-tidy。首次执行
`make configure` 后 clangd 才能读取 `build/debug/compile_commands.json`。

命令面板中的 `Tasks: Run Task` 提供初始化、doctor、lint、test、完整 verify、CMake build、
Triton 和 TileLang 入口。`launch.json` 提供当前 Python 文件、C++ Two Sum 和 Rust 测试的
调试模板；Python Test Explorer 已指向 `tests/python` 并启用 pytest。

## GitHub Actions

`.github/workflows/quality.yml` 在 push、pull request 或手动触发时运行：

- Python Ruff、BasedPyright 和 pytest；
- C++ 格式检查、CPU Two Sum 编译/执行和 ShellCheck；
- Rust rustfmt、Clippy 和 tests。

GitHub 托管 runner 默认没有 NVIDIA GPU，因此云端 workflow 不声称验证 CUDA/Triton/TileLang
运行时。完整 GPU 验收必须在有兼容 GPU 的本机容器或自托管 GPU runner 上执行
`make verify`。

## 常见问题

### 容器中 `nvidia-smi` 失败或 PyTorch 看不到 CUDA

先在宿主机运行 `nvidia-smi`，再确认 NVIDIA Container Toolkit 已配置给 Docker。检查 Docker
是否能运行任意 `--gpus all` 容器。若 `nvcc --version` 正常但 `nvidia-smi` 失败，通常说明
镜像工具链存在、GPU runtime 转发不存在；重装 Python 包不会解决它。

还要确认宿主机驱动支持 CUDA 13.0。基础镜像里的 CUDA toolkit 版本可以高于 PyTorch wheel
携带的 CUDA runtime 版本，但不能高于宿主机驱动实际能够承载的范围。

### `nvidia/cuda:13.0.3-cudnn-devel-ubuntu24.04` 拉取失败

先确认 tag、CPU 架构和 NVIDIA registry 可用性。仓库按你的要求固定了该 tag，不会静默回退到
另一个 CUDA 版本。如果 NVIDIA 未为宿主机架构发布它，需要明确选择受支持的镜像 tag，并
同步更新 README/锁文件后重新验收。

APT 镜像只在基础镜像已经拉取、Dockerfile 开始执行后生效，不会加速 Docker Hub/NVIDIA
基础镜像本身。uv 官方安装脚本和 nvm 官方安装脚本也仍分别来自 Astral 与 GitHub；镜像配置
加速的是后续 PyPI 包、Node 二进制、Rust 工具链和 Cargo crate。

### 国内镜像暂时不可用或同步滞后

所有主要 URL 都集中在 `.env`。需要临时回到官方服务时可以替换为：

```dotenv
UBUNTU_MIRROR=http://archive.ubuntu.com/ubuntu
UBUNTU_PORTS_MIRROR=http://ports.ubuntu.com/ubuntu-ports
NVIDIA_APT_MIRROR=https://developer.download.nvidia.com/compute/cuda/repos
PYPI_INDEX_URL=https://pypi.org/simple
NVM_NODEJS_ORG_MIRROR=https://nodejs.org/dist
RUSTUP_DIST_SERVER=https://static.rust-lang.org
RUSTUP_UPDATE_ROOT=https://static.rust-lang.org/rustup
```

Cargo 的 RsProxy 配置位于 `docker/cargo-config.toml`，只复制到容器用户目录，不影响 GitHub
托管 CI。需要官方 crates.io 时，移除该文件中的 `[source.crates-io]` 替换配置并重建镜像。

### 源码或缓存目录 Permission denied

确认 `.env` 的 UID/GID 与宿主机一致，然后重建镜像。旧命名卷仍可能保留此前的 ownership。
不需要保留缓存时，可以先备份重要内容，再对当前组合执行：

```bash
bash scripts/container.sh destroy bind persistent
```

该操作会永久删除此 Compose 组合声明的命名卷。copy + persistent 还会删除容器工作区，必须
先 export；bind 模式的宿主机源码不会因删除卷而消失。

### copy 模式看不到宿主机新改动

这是快照隔离的预期行为。copy + ephemeral 可以通过再次 `up`（脚本会带 `--build`）取得新的
镜像快照。copy + persistent 的现有 `workspace-data` 卷不会被重建镜像覆盖，需要先 export
容器内改动，然后 destroy 旧卷，再重新 up。反方向也一样：容器内修改不会自动回写宿主机，
必须执行 `container.sh export ...`。

### `uv sync --locked` 报锁文件过期

这表示 `pyproject.toml` 与已提交 `uv.lock` 不一致，是预期保护。确认依赖改动后在容器内运行：

```bash
uv lock
uv sync --locked --group dev
make verify
```

不要为了绕过冲突删除版本约束后直接提交；PyTorch、Triton、TileLang 的兼容组合应以实际 GPU
验收结果和锁文件为准。

### `python` 指向错误位置

首选 `uv run --frozen python ...`。`make doctor` 会检查项目环境的 `pyvenv.cfg`，并要求
其 Python home 位于 `$HOME/.local/share/uv/python/`。persistent 模式可删除对应 Docker
命名卷后重新初始化；ephemeral 模式重新创建容器即可。不要用 `sudo pip` 或 apt Python 修补
项目环境。

### Node/npm 版本与示例不同

这是 `nvm install 24` 的正常语义：主版本固定，补丁版本随镜像构建日期变化。使用
`node -v`、`npm -v` 查看实际版本，`make doctor` 会拒绝非 Node 24 或非 npm 11。需要完全复现时请把
Dockerfile 改为完整 Node 版本号。

### clangd 没有补全或 include 报错

先在容器内执行 `make configure`，确认 `build/debug/compile_commands.json` 存在；然后在
VS Code 执行 `clangd: Restart language server`。如果 GPU 在 configure 阶段不可见，CMake
的 `native` CUDA 架构检测也会失败，应先修复 GPU 转发，或明确传入适合目标 GPU 的
`CMAKE_CUDA_ARCHITECTURES`。

### Triton 首次运行很慢

首次运行包含 JIT 编译。persistent 模式把 `TRITON_CACHE_DIR` 和 `TILELANG_CACHE_DIR` 放在
命名卷，后续同一签名 kernel 会复用缓存；ephemeral 模式仅在当前容器存在期间复用。性能测试
应把首次编译排除在稳态计时之外。

## 更新策略

- CUDA/cuDNN/Ubuntu：修改 `Dockerfile` 的 `BASE_IMAGE` 后重新构建，并完整运行 GPU 验收。
- uv：重新构建镜像会重新执行官方安装脚本，因此会取得当时版本；需要完全可复现时，应额外
  固定 uv 安装版本。
- Python 包：在容器内使用 `uv lock --upgrade` 或按包升级，运行 `make verify` 后提交锁文件。
- Node：当前跟随 Node 24 最新补丁；需要升级主版本时同时调整 Dockerfile 和 doctor 断言。
- Rust：当前跟随 stable；升级后运行 rustfmt、Clippy 和全部测试。

这个仓库刻意把“镜像与工具是否存在”“语言实现是否正确”“GPU kernel 是否真的运行”分成
可定位的检查层级。日常可以运行单项测试，依赖或驱动升级后则运行 `make verify` 做完整回归。
