# Codex CLI 代理配置指南

本文说明仓库内置的 v2rayA Lite Compose sidecar 如何提供显式 HTTP/SOCKS5
代理，并让开发容器中的 Codex CLI 通过该代理访问网络。该方案不接管容器
路由表，不需要 iptables、`NET_ADMIN` 或 `privileged: true`。

> v2rayA 和代理 core 由 `mzz2017/v2raya` sidecar 镜像提供，不安装到开发镜像。
> 本仓库目前不安装 Codex CLI；Codex 需另行安装在实际运行位置。

## 为什么使用 Lite 模式

v2rayA 的透明代理模式需要创建 iptables/nftables 规则，并要求进程拥有 root 和网络管理权限。
如果目标只是让 Codex CLI、curl、Git 或其他命令行程序走代理，使用标准代理环境变量更简单：

```text
Codex CLI -> HTTP/SOCKS5 入站 -> v2ray-core -> 远端代理节点 -> OpenAI
```

Compose 为 sidecar 传入的核心启动参数等价于：

```bash
v2raya --lite --config /etc/v2raya --log-level info
```

它不会创建透明代理规则，因此遇到下面这种错误时，不需要安装 iptables：

```text
iptables-legacy: not found
```

应停止透明代理配置，改用 Lite 模式和本文中的显式代理变量。

## Sidecar 部署结构

`compose.yaml` 定义两个独立容器：

```text
Compose project
├── dev     CUDA 开发环境与 Codex CLI
└── proxy   v2rayA Lite 与代理 core
```

`proxy` 设置 `network_mode: service:dev`，因此两个容器的进程、根文件系统和权限
仍然隔离，但共享网络命名空间与 loopback。`dev` 中的程序所访问的
`127.0.0.1:20171` 实际由 `proxy` 容器内的 core 监听。

sidecar 默认使用镜像内的 root 用户写入 `/etc/v2raya`，但 Compose 会丢弃它的
全部 Linux capabilities，并启用 `no-new-privileges`。Lite 模式不需要 root 网络权限，
也无法在该配置下修改 iptables。

## 启动与首次配置

先确认 sidecar 镜像已存在：

```bash
docker image inspect mzz2017/v2raya:latest >/dev/null
```

随后使用仓库脚本启动：

```bash
bash scripts/container.sh up bind persistent
bash scripts/container.sh status bind persistent
```

`up` 会同时启动 `dev` 和 `proxy`，它们都设置了 `restart: unless-stopped`。只要
Docker daemon 恢复运行且容器没有被手动 stop/down，两个服务就会自动恢复，
无需再在开发容器中手工执行 `v2raya --lite`。

打开 `http://127.0.0.1:2017`，在 Web UI 中创建管理员账号、导入订阅、选择节点并
启动连接。Web UI 只发布到宿主机 `127.0.0.1`，默认不对局域网暴露。
从旧版 v2rayA 或开发容器可写层迁移现有数据时，首次启动可能会先进行数据库
升级而不自动启动代理 core；确认订阅和节点存在后，在 Web UI 点击一次“启动”。

查看 sidecar 日志：

```bash
bash scripts/container.sh logs bind persistent
```

按 `Ctrl-C` 只会停止日志跟随，不会停止后台容器。

### 配置持久化

- `persistent` 模式把 `/etc/v2raya` 挂载到 `v2raya-data` 命名卷；`down` 后配置
  仍然存在，下次 `up` 会继续使用。
- `ephemeral` 模式把 `/etc/v2raya` 放在 tmpfs；proxy 容器停止、删除或重建后
  配置即丢失。
- `destroy ... persistent` 会删除 `v2raya-data`，包括管理员账号、订阅和节点
  选择；执行前应确认不再需要。

## 默认端口

v2rayA 的常见默认端口如下，实际值应以管理页面和生成的 v2ray-core 配置为准：

| 端口 | 用途 |
| --- | --- |
| `2017` | v2rayA Web 管理页面 |
| `20170` | SOCKS5 代理 |
| `20171` | HTTP 代理 |
| `20172` | 按规则分流的 HTTP 代理，通常不需要给 Codex 使用 |

先启动 v2rayA，在管理页面导入订阅、选择节点并启动连接。仅仅看到本地端口正在监听，并不
代表远端节点可用。

## 其他网络拓扑

仓库默认使用上述共享网络的 sidecar 拓扑。如果 Codex CLI 不在 `dev` 容器中，
代理地址需要按实际运行位置调整。

### Codex 与 v2rayA 共享网络命名空间

这是最简单的方式，不需要发布端口：

```text
HTTP 代理:   http://127.0.0.1:20171
SOCKS5 代理: socks5h://127.0.0.1:20170
```

`127.0.0.1` 指向共享网络命名空间。这是本仓库 `dev` + `proxy` 的默认方式，
不需要发布 `20170` 或 `20171` 到宿主机。

### Codex 位于宿主机，v2rayA 位于容器

需要让 v2rayA 的代理入站监听容器的非 loopback 地址。可在 v2rayA 设置中启用地址和端口
共享，然后在 Compose 的 `dev` 服务中额外向宿主机 loopback 发布代理端口：

```yaml
ports:
  - "127.0.0.1:20170:20170"
  - "127.0.0.1:20171:20171"
```

不要把宿主机一侧写成 `0.0.0.0:20171:20171`，否则同一网络中的其他设备可能访问这个
未认证代理。发布端口后，宿主机 Codex 仍使用 `127.0.0.1:20171`。

如果 v2ray-core 的入站仍只监听容器内的 `127.0.0.1`，Docker 端口发布不会使它自动变成
外部可访问；必须先在 v2rayA 中允许地址和端口共享。

### Codex 位于容器，v2rayA 位于宿主机

Linux 容器不能使用 `127.0.0.1` 访问宿主机。可在 Compose 服务中增加：

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

然后使用：

```text
http://host.docker.internal:20171
```

宿主机代理也必须允许来自 Docker bridge 的连接，并用防火墙限制访问范围。

## 验证代理链路

在启动 Codex 前先用 curl 验证完整链路：

```bash
curl \
  --proxy http://127.0.0.1:20171 \
  --connect-timeout 10 \
  --max-time 30 \
  -I https://api.openai.com
```

如果拓扑不是“同一容器”，把地址替换成上一节对应的地址。收到 OpenAI 返回的任意 HTTP
状态码，例如 `401`、`403` 或 `404`，都说明 DNS、远端节点、TLS 和 HTTP 链路已经打通；
这里不要求匿名请求获得 `200`。

也可以分别验证 HTTP 和 SOCKS5 入站：

```bash
curl --proxy http://127.0.0.1:20171 -I https://api.openai.com
curl --proxy socks5h://127.0.0.1:20170 -I https://api.openai.com
```

SOCKS5 URL 中使用 `socks5h`，让域名通过代理端解析，避免容器本地 DNS 与代理侧结果不一致。

## 为当前 shell 开启或关闭代理

需要让 curl、Git、uv 等多个命令共同使用 sidecar 时，必须把脚本 source 到当前
shell；直接执行子进程无法修改父 shell 的环境变量。

开启：

```bash
source scripts/proxy-env.sh on
```

查看状态：

```bash
source scripts/proxy-env.sh status
```

关闭并 unset 大小写两套标准代理变量：

```bash
source scripts/proxy-env.sh off
```

开发镜像的交互式 Bash 已提供等价快捷命令：

```bash
proxy-on
proxy-status
proxy-off
```

`on` 会同时 export `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`、`NO_PROXY` 及它们的
小写形式；`off` 会同时 unset 这八个变量。脚本使用 Compose 传入的
`V2RAYA_HTTP_PROXY`、`V2RAYA_SOCKS_PROXY` 与 `V2RAYA_NO_PROXY` 作为地址来源。

## VS Code Server 与扩展市场

四种版本化的 Dev Container 配置均通过 `remoteEnv` 将同一组代理变量传递给
VS Code Server 及其集成终端、任务和调试进程。因此扩展市场下载会使用 sidecar，
无需在工作区 `.vscode/settings.json` 中配置 `http.proxy`。

配置变更后，使用 **Dev Containers: Rebuild and Reopen in Container** 重新创建环境。
可在容器中的 VS Code 终端确认：

```bash
env | rg '(^|_)(HTTP|HTTPS|ALL|NO)_PROXY='
```

`remoteEnv` 只应用于通过 Dev Container 客户端启动的远端工具。若需要从容器外部
启动的独立进程也使用代理，仍可在其 shell 中执行 `proxy-on`。

## 启动 Codex CLI

开发镜像的 `docker/bashrc` 已内置代理函数。新建交互式 Bash 后直接执行：

```bash
codex
```

该 `codex` shell 函数会调用 `codex-proxy`，只为 Codex 进程注入：

```text
HTTP_PROXY  = http://127.0.0.1:20171
HTTPS_PROXY = http://127.0.0.1:20171
ALL_PROXY   = socks5h://127.0.0.1:20170
NO_PROXY    = localhost,127.0.0.1
```

因为没有在整个容器中全局 export 这些标准变量，uv、apt、Git 和其他命令不会
仅因为启动交互式 shell 就被强制使用代理。

也可以显式调用同一个代理函数：

```bash
codex-proxy
```

需要临时绕过 sidecar 直连时：

```bash
codex-direct
```

代理地址默认继承 Compose 传入的 `V2RAYA_*` 变量；如果 Codex 需要不同的
代理，可在宿主机的 `.env` 中设置专用覆盖：

```dotenv
CODEX_HTTP_PROXY=
CODEX_SOCKS_PROXY=
CODEX_NO_PROXY=
```

函数的实际定义为：

```bash
codex-proxy() {
  local http_proxy="${CODEX_HTTP_PROXY:-${V2RAYA_HTTP_PROXY:-http://127.0.0.1:20171}}"
  local socks_proxy="${CODEX_SOCKS_PROXY:-${V2RAYA_SOCKS_PROXY:-socks5h://127.0.0.1:20170}}"
  local no_proxy="${CODEX_NO_PROXY:-${V2RAYA_NO_PROXY:-localhost,127.0.0.1}}"

  HTTP_PROXY="${http_proxy}" \
  HTTPS_PROXY="${http_proxy}" \
  ALL_PROXY="${socks_proxy}" \
  NO_PROXY="${no_proxy}" \
    command codex "$@"
}

codex() {
  codex-proxy "$@"
}

codex-direct() {
  command codex "$@"
}
```

这些函数只由交互式 Bash 加载。脚本、IDE 任务或其他不读取 `~/.bashrc` 的进程需要
显式设置标准代理变量。

## 故障排查

### `Connection refused`

示例：

```text
Failed to connect to 127.0.0.1 port 20171: Connection refused
```

curl 没有连上本地代理。检查：

- v2rayA 和 v2ray-core 是否已经启动；
- HTTP 入站端口是否确实为 `20171`；
- Codex 和 v2rayA 是否位于预期的宿主机或容器；
- 跨容器边界时是否配置了监听地址和 Compose 端口发布。

### CONNECT 成功后 TLS 失败

示例：

```text
HTTP/1.1 200 Connection established

curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL
```

`200 Connection established` 只表示 curl 已连接到本地 HTTP 代理，并且本地代理接受了 CONNECT
请求；它不证明远端节点已经连接成功。随后出现 `SSL_ERROR_SYSCALL`，通常表示代理隧道在 TLS
握手期间被关闭。

依次检查：

1. 在 v2rayA 管理页面更新订阅；
2. 对节点执行延迟和连通性测试；
3. 切换到另一个可用节点；
4. 用 HTTP、SOCKS5 两个入站分别测试多个 HTTPS 站点；
5. 如果是自建节点，检查服务端进程、监听端口、云安全组和防火墙。

如果普通 HTTP 经代理返回 `503`，HTTP 和 SOCKS5 同时失败，而且宿主机、容器都无法连接
节点端口，问题通常位于代理节点或服务提供商，不是 OpenAI 证书、Codex 配置或容器 iptables。

不要使用 `curl -k` 掩盖这个错误。`-k` 只关闭证书校验，无法修复不可达的节点或被中途关闭的
TLS 隧道。

### OpenAI 可访问，但 Codex 仍失败

先确认变量和 Codex 处于同一个进程环境：

```bash
env | rg -i '^(http|https|all|no)_proxy='
command -v codex
codex --version
```

如果在一个终端中执行 `export`，却从另一个终端、IDE 任务或宿主机启动 Codex，新进程不会
自动继承这些变量。应在实际启动 Codex 的位置设置代理。

登录使用外部浏览器时，浏览器网络与 CLI 网络是两条链路。CLI 的设备码或 token 请求可以走
上述代理，但外部浏览器仍需具备自己的可用网络。

## 代理作用范围

运行在开发容器里的 v2rayA 只能代理容器启动后的 Codex、curl、Git、uv 等进程。它不能代理：

- Docker 基础镜像拉取；
- 在 v2rayA 启动之前执行的 Dockerfile `RUN` 指令；
- 宿主机上未显式配置代理的其他程序。

Docker pull 和镜像构建需要单独配置宿主机 Docker daemon、BuildKit 或构建参数代理。不要因为
容器内 curl 已经成功，就假设 Docker 构建也会自动使用同一个代理。

## 安全注意事项

- 优先使用 Lite 和显式代理变量，不要仅为 Codex 开启 `privileged: true`；
- Web 管理端口和代理端口只发布到宿主机 `127.0.0.1`；
- 不要把订阅 URL、节点地址、UUID、Reality 密钥或带密码的代理 URL 提交到 Git；
- 不要在故障日志中直接粘贴完整 v2ray-core 配置；
- 本机无需代理的服务应加入 `NO_PROXY`，避免循环代理；
- 更换代理服务提供商或节点后，重新运行 curl 验证，再启动 Codex。
