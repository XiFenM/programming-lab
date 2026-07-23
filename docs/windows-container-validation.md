# Windows 容器工作流验证清单

## 当前状态

`scripts/container.ps1` 与 `scripts/container.sh` 已完成代码级行为对照。两者使用相同的参数、
模式、Compose 版本阈值、覆盖文件顺序、action 映射、提示信息和退出码约定。PowerShell 入口
显式采用区分大小写的值比较，并与 Bash 一样在导出目录为空时使用 `container-export`。
这里的“一致”指文档所示的位置参数接口和容器工作流语义；脚本调用语法、宿主机路径形式、
终端编码以及 PowerShell 自带的命名参数和 common parameters 仍遵循各自平台约定。

截至 2026-07-23，Windows PowerShell、Docker Desktop、WSL2 和 GPU 环境中的实际运行尚未
验证。代码级对齐不应被描述成已通过 Windows 实机验收。

## 后续环境矩阵

- Windows PowerShell 5.1 与 PowerShell 7；
- Docker Compose 2.27–2.29 的 legacy GPU 配置与 2.30+ 的 `gpus: all` 配置；
- `bind/copy` × `persistent/ephemeral` 四种组合；
- Windows Docker Desktop 的 WSL2 后端和 NVIDIA GPU 转发。

## 后续验证项目

- 对无参数、帮助、非法 action、非法模式和过低 Compose 版本核对输出及退出码；
- 对 `build`、`up`、`status`、`logs`、`shell`、`init`、`stop`、`down`、`destroy`、
  `config` 和 `export` 核对两种脚本生成的 Docker Compose 参数；
- 验证 copy + persistent 的旧 `workspace-data` 提示，以及 copy + ephemeral 删除前警告；
- 验证 export 仅接受 copy 模式，并覆盖默认目录、相对路径、绝对路径和含空格路径；
- 验证基础镜像已经占用 UID/GID 1000 时仍能创建可用的 `coder` 用户；
- 验证 CRLF checkout 不会破坏 Linux entrypoint；
- 验证 Windows bind mount 下的 `/workspace/build` 与 `/workspace/target` 分别使用命名卷或
  tmpfs，并能完成 CMake、Cargo 和 GPU 工具链检查；
- 最后在容器内运行 `make doctor` 和 `make verify`，记录 Windows、PowerShell、Docker、
  Compose、驱动和 GPU 版本。
