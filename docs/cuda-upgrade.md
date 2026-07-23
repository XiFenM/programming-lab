# CUDA 升级指南

本文说明如何升级本仓库容器使用的 CUDA Toolkit、cuDNN 或 Ubuntu 基础镜像，以及升级后
需要检查的宿主机驱动、Python GPU 依赖、构建缓存和验收结果。

## 版本来自哪里

系统 CUDA Toolkit 的版本由 `Dockerfile` 顶部的基础镜像决定：

```dockerfile
ARG BASE_IMAGE=nvidia/cuda:13.0.3-cudnn-devel-ubuntu24.04
```

这个 tag 同时表达了四项选择：

- `13.0.3`：CUDA Toolkit 版本；
- `cudnn`：镜像包含 cuDNN；
- `devel`：镜像包含 `nvcc`、头文件和开发库，原生 CUDA 示例依赖这一变体；
- `ubuntu24.04`：容器操作系统版本。

`compose.yaml` 当前没有传入 `BASE_IMAGE` 构建参数，因此日常通过
`scripts/container.sh` 构建时使用的就是 Dockerfile 中的默认值。只在 `.env` 中添加
`BASE_IMAGE` 不会生效。

下面几类 CUDA 版本不要混为一谈：

| 版本 | 查看方式 | 含义 |
| --- | --- | --- |
| 宿主机驱动支持上限 | 宿主机执行 `nvidia-smi` | 驱动能够承载的最高 CUDA 版本，不是容器 Toolkit 版本 |
| 容器 CUDA Toolkit | 容器执行 `nvcc --version` | Docker 基础镜像提供的编译工具链 |
| PyTorch CUDA runtime | 容器执行 `uv run --frozen python -c 'import torch; print(torch.version.cuda)'` | Python wheel 携带或依赖的 CUDA 用户态运行库 |
| GPU 计算能力 | `nvidia-smi --query-gpu=compute_cap --format=csv,noheader` | GPU 架构能力，与 CUDA 软件版本不是同一个概念 |

系统 Toolkit 与 PyTorch runtime 的版本可以不同。当前仓库没有构建 PyTorch C++/CUDA
扩展，原生 CUDA 示例使用系统 `nvcc`，而 PyTorch、Triton 和 TileLang 使用
`uv.lock` 固定的 Python 依赖组合。版本号不同本身不代表环境有问题，最终以完整 GPU 验收
是否通过为准。

## 升级前检查

### 1. 选择存在的 NVIDIA 镜像 tag

先在 NVIDIA CUDA 镜像发布页确认目标 tag、CPU 架构和镜像变体确实存在。仓库需要编译
`.cu` 文件，所以应继续选择 `devel`，不能直接换成只有运行库的 `runtime` 镜像。

如果只升级 CUDA，建议暂时保留 `cudnn-devel-ubuntu24.04` 后缀，减少一次升级中同时变化的
组件数量。例如：

```text
nvidia/cuda:<目标 CUDA 版本>-cudnn-devel-ubuntu24.04
```

如果同时升级 Ubuntu，需要额外确认 Dockerfile 中的软件包名称、清华 Ubuntu 镜像、NVIDIA
APT 仓库和 CMake 最低版本在新发行版上仍然可用。

### 2. 确认宿主机驱动兼容

在宿主机执行：

```bash
nvidia-smi
```

目标 CUDA 版本必须处于宿主机驱动的兼容范围内。容器复用宿主机内核驱动，升级容器镜像
不会升级宿主机驱动，也不能绕过驱动的版本上限。应以 NVIDIA 官方 CUDA Compatibility 和
目标 Toolkit 的 release notes 为准；不要只根据镜像能够成功拉取就判断兼容。

### 3. 记录升级前基线

建议在旧环境仍可用时记录以下输出，便于升级后比较：

```bash
nvidia-smi
nvcc --version
uv run --frozen python - <<'PY'
import torch

print("PyTorch:", torch.__version__)
print("PyTorch CUDA runtime:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
PY
```

工作区存在未提交修改时先确认这些修改已保存。升级不要求提交无关文件，也不要用清理命令
删除不属于本次升级的改动。

## 执行升级

### 1. 修改基础镜像

编辑 `Dockerfile` 的 `BASE_IMAGE`：

```diff
-ARG BASE_IMAGE=nvidia/cuda:13.0.3-cudnn-devel-ubuntu24.04
+ARG BASE_IMAGE=nvidia/cuda:<目标版本>-cudnn-devel-ubuntu24.04
```

仓库源代码、`CMakeLists.txt` 和 Compose GPU 配置当前没有写死 CUDA 13，通常不需要一起
修改。CMake 默认使用 `CMAKE_CUDA_ARCHITECTURES=native`，会针对容器内可见 GPU 重新检测
目标架构。

### 2. 同步文档中的版本描述

README 中包含当前镜像、宿主机要求和故障排查示例。用下面的命令查找旧版本引用并更新：

```bash
rg '13\.0\.3|CUDA 13\.0|nvcc 13\.0' README.md Dockerfile docs
```

如果目标版本不再属于 CUDA 13，应同时检查更宽泛的引用：

```bash
rg 'CUDA 13|cu13' README.md pyproject.toml uv.lock docs
```

`uv.lock` 中出现 `cu13` 不一定需要手工修改；锁文件只能由 uv 根据 Python 依赖解析结果生成。

### 3. 重建并启动容器

以下示例沿用 bind 工作区和 persistent 缓存模式：

```bash
bash scripts/container.sh down bind persistent
bash scripts/container.sh up bind persistent
bash scripts/container.sh init bind persistent
bash scripts/container.sh shell bind persistent
```

`up` 操作包含 `docker compose up -d --build`，Dockerfile 的 `FROM` 发生变化后会基于新基础
镜像重建。使用其他工作区或持久化模式时，把上述两个模式参数替换成实际选择，并在整组命令中
保持一致。

`persistent` 模式会保留 CMake/Cargo 构建树以及 uv、ccache、Triton 和 TileLang 缓存。这可以
减少重复下载与编译，但不是全新环境。如果需要排查疑似缓存问题，可先保留现有环境完成一次
升级；只有在确实需要完全重新初始化时才执行对应配置的 `destroy`，因为它会删除所选命名卷：

```bash
bash scripts/container.sh destroy bind persistent
bash scripts/container.sh up bind persistent
bash scripts/container.sh init bind persistent
```

### 4. 让 CMake 重新识别 nvcc

基础镜像升级后，`nvcc` 路径可能仍然是 `/usr/local/cuda/bin/nvcc`，旧 CMake 缓存因路径没有
变化而无法充分反映编译器版本变化。在容器中执行一次 fresh configure：

```bash
cmake --fresh --preset debug
```

这会重新生成 CMake 配置，但不会删除源码。ccache 会把编译器和编译参数纳入缓存判断，通常
无需手工清空；若编译结果异常，再用 `ccache --clear` 排除缓存因素。

## 是否需要升级 Python GPU 依赖

基础镜像和 Python GPU 栈应分开决策。

### 仅升级同一 CUDA 主版本或补丁版本

例如从 CUDA 13.0 升到另一个 CUDA 13.x 版本时，先保留现有 `pyproject.toml` 和
`uv.lock`，执行完整验收。只要 PyTorch、Triton 和 TileLang 的实际 GPU 测试通过，就没有
必要仅为了让版本字符串一致而重新锁定依赖。

## 长期维护升级分支

`codex/upgrade-cuda-13.2.1` 是一个长期存在的候选升级分支。它必须以最新远端 `main` 为
直接基础，并且只包含一个 CUDA 版本升级提交。下面的命令应始终输出 `0 1`，分别表示升级
分支相对 `main` 落后 0 个提交、领先 1 个提交：

```bash
git fetch origin
git rev-list --left-right --count \
  origin/main...origin/codex/upgrade-cuda-13.2.1
```

`.github/workflows/sync-cuda-upgrade.yml` 在每次 push 到 `main` 后自动维护这一拓扑，也支持从
Actions 页面手动触发。工作流会：

1. 抓取最新 `main` 和升级分支，并记录升级分支的远端 SHA；
2. 要求升级分支只有一个非 merge 的独有提交，且该提交的父提交是 `main` 的祖先；
3. 将该升级提交 rebase 到最新 `main`；
4. 再次要求拓扑严格为 `0 1`，并运行 `git diff --check`；
5. 使用绑定旧远端 SHA 的 `--force-with-lease` 更新升级分支。

工作流使用 GitHub 自动创建的临时 `GITHUB_TOKEN`，仓库不需要保存 PAT。工作流只申请
`contents: write`；如果仓库或组织策略禁止该权限，需在 GitHub 的
`Settings → Actions → General → Workflow permissions` 中允许工作流写入仓库内容。

这个分支不能通过“merge main into upgrade branch”更新，否则 merge commit 会让它领先不止
一个提交。若分支保护或 ruleset 禁止 force push，需要对该升级分支允许 GitHub Actions
执行强制更新；不要放宽 `main` 的保护规则。

rebase 冲突、升级分支出现多个独有提交、升级提交变成 merge commit，或者远端分支在工作流
运行期间被其他人更新时，工作流都会失败且不推送。此时应人工检查升级内容，重新建立单提交
分支后，再从 Actions 页面运行 `Sync CUDA upgrade branch`。

### 跨 CUDA 主版本升级

例如未来从 CUDA 13 升到 CUDA 14 时，现有 PyTorch 仍可能使用 CUDA 13 用户态运行库。
只要新驱动向后兼容，这种组合可能继续工作。但是出现以下情况时，应调查并升级 Python GPU
依赖：

- PyTorch、Triton 或 TileLang 明确不支持目标 Toolkit 或驱动组合；
- 项目开始编译 PyTorch C++/CUDA 扩展，需要系统 `nvcc` 与 PyTorch 构建版本满足其兼容要求；
- 希望 Python 栈也切换到新 CUDA 主版本，并且上游已经发布对应 wheel；
- 完整验收出现能够定位到 CUDA ABI、PTX、编译器或运行库的错误。

确认上游兼容性后，在容器中升级并重新生成锁文件：

```bash
uv lock --upgrade
uv sync --locked --group dev
make verify
```

然后审查并提交 `pyproject.toml` 和 `uv.lock` 的预期变化。不要手工编辑 `uv.lock`，也不要在
尚无上游支持时强行指定不存在的 CUDA wheel index。

## 完整验收

在容器中先确认工具链版本：

```bash
nvcc --version
nvidia-smi
ldconfig -p | rg libcudnn
```

再运行仓库的完整验收：

```bash
make verify
```

验收至少应覆盖：

- `doctor.sh` 能找到 `nvcc`、`nvidia-smi` 和 cuDNN；
- C++ 与原生 CUDA 目标能够重新配置、编译并运行；
- PyTorch 能创建真实 CUDA tensor；
- Triton kernel 能够 JIT 编译并运行；
- TileLang 能够导入并通过仓库探针；
- 静态检查、Python 测试和 Rust 测试没有受到基础镜像变化影响。

还可以单独打印 Python GPU 栈版本：

```bash
uv run --frozen python - <<'PY'
import torch
import triton

print("PyTorch:", torch.__version__)
print("PyTorch CUDA runtime:", torch.version.cuda)
print("Triton:", triton.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
PY
```

不要把 `nvidia-smi`、`nvcc --version` 和 `torch.version.cuda` 必须完全相同作为通过条件；应
结合 NVIDIA 驱动兼容规则和实际 kernel 验收结果判断。

## 常见问题

### 基础镜像拉取失败

先确认完整 tag 和当前 CPU 架构确实由 NVIDIA 发布。Dockerfile 中配置的 Ubuntu、NVIDIA
APT 和 PyPI 镜像只会在基础镜像成功拉取后生效，不能加速或修复基础镜像 tag 拉取。

### `nvcc` 正常但 `nvidia-smi` 失败

这说明容器中存在 Toolkit，但宿主机 GPU 转发没有正确进入容器。检查宿主机驱动、NVIDIA
Container Toolkit 和 Docker GPU runtime；重新安装 Python 包不能解决这个问题。

### `no kernel image is available` 或架构检测失败

确认容器实际可见 GPU，并重新执行 `cmake --fresh --preset debug`。如果构建环境无法访问最终
运行 GPU，需要显式设置适合目标设备的 `CMAKE_CUDA_ARCHITECTURES`，而不是使用 `native`。

### PyTorch 能运行，但原生 CUDA 编译失败

PyTorch wheel 可能使用自己的 CUDA 用户态运行库，而原生目标使用系统 `nvcc`，所以二者可以
表现不同。优先查看 `nvcc` 编译错误、CMake 编译器检测结果以及新 Toolkit 对主机编译器版本的
支持情况。

### Triton 或 TileLang 首次运行很慢

升级可能使已有 JIT 缓存失效，首次运行需要重新编译 kernel。先让首次运行完成，再评估稳态
性能；如果反复出现缓存相关错误，再清理对应 persistent 缓存卷。

## 回滚

如果升级无法通过验收：

1. 保存完整的 `make verify` 日志和三个版本输出：`nvidia-smi`、`nvcc --version`、
   `torch.version.cuda`；
2. 将 Dockerfile 的 `BASE_IMAGE` 恢复为升级前的精确 tag；
3. 如果本次升级修改了 Python 依赖，同时恢复经过验证的 `pyproject.toml` 和 `uv.lock`；
4. 重新执行容器重建、`cmake --fresh --preset debug` 和 `make verify`。

不要通过 `git reset --hard` 回滚，因为它会同时删除工作区中与 CUDA 升级无关的修改。

## 提交前清单

- [ ] Dockerfile 使用存在且适合当前 CPU 架构的精确 `cudnn-devel` tag；
- [ ] 宿主机驱动支持目标 CUDA 版本；
- [ ] README 中的基础镜像、驱动要求和故障排查文字已经同步；
- [ ] Python 依赖未被无理由重锁；如果确实升级，已审查并提交 `uv.lock`；
- [ ] CMake 已通过 fresh configure 重新检测新 `nvcc`；
- [ ] `make verify` 在真实 NVIDIA GPU 上完整通过；
- [ ] 提交内容不包含无关的工作区文件或本机专用 `.env`。
