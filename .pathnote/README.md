# 同路志内容包作者说明

这个目录保存同路志发布包的模板和统一校验入口。仓库中的普通代码、实验记录和 Markdown 不会自动发布；只有 `publications/<slug>/` 下显式创建的内容包会进入检查范围。

## 创建内容包

从模板复制一个新目录，并把目录名替换为稳定的英文 slug：

```bash
cp -R .pathnote/templates/publication publications/<slug>
```

随后修改 `publication.json` 和 `index.mdx`。`publication.json.slug` 必须与目录名一致。新内容先保持 `draft`，三项审核保持 `pending`；`draft` 只控制同路志网站是否收录内容，不能保护已经提交到公开仓库的信息。

正文从二级标题开始，不重复页面标题。当前内容包独有的图片、字幕和下载文件放在 `assets/` 下。引用仓库中的代码、实验结果或验证证据时，使用相对于仓库根目录的路径。

## 本地检查

先暂存准备提交的内容，再运行：

```bash
make pathnote-check
```

这个命令等价于：

```bash
node .pathnote/pathnote-source-check.mjs --source programming-lab --staged
```

计算准备审核的暂存快照摘要：

```bash
node .pathnote/pathnote-source-check.mjs \
  --source programming-lab \
  --staged \
  --digest <slug>
```

命令会输出 `<slug>: sha256:...`。审核人员应当针对这个暂存快照完成内容、权利和敏感信息审核，再把其中的 `sha256:...` 原样写入 `reviews.subjectDigest`。相关内容发生变化以后，需要重新计算摘要并重新审核。

检查器读取暂存区对应的 Git 对象，校验 Schema、MDX、路径、资源、敏感信息和审核状态。未暂存的相关文件会使检查失败。共享检查器由同路志网站仓库统一分发，并由 `.pathnote/contract-lock.json` 固定版本和 SHA-256。不要在来源仓库中单独修改 bundle、锁文件或发布模板。

## 共享校验器受控升级

Pull Request 校验由目标分支中的 `pull_request_target` workflow 定义。工作流先检出 base 仓库和固定 SHA，从中提取校验器和锁文件，再获取 head 的 Git 对象进行只读检查。`origin` 始终指向 base 仓库，工作流绝不执行 head 中的脚本。这个信任边界必须保留：workflow 继续使用只读权限，检出代码时不保留凭证。

升级共享校验器时，管理员按照以下顺序操作：

1. 从同路志网站工程取得新的完整分发，独立核对 bundle、模板哈希和 `.pathnote/contract-lock.json` 中的 `distributionSha256`。
2. 把核对后的 64 位 `distributionSha256` 临时写入仓库变量 `PATHNOTE_CHECKER_UPGRADE_SHA256`。
3. 建立一个只包含本次 `.pathnote` 工具分发文件的 Pull Request。这个 Pull Request 不混入内容包、workflow 或其他仓库改动。
4. 等待受保护的 PathNote 校验通过并合并，然后立即清空 `PATHNOTE_CHECKER_UPGRADE_SHA256`。

必须用 branch protection 或 ruleset 保护 `main`，把 PathNote 校验设为必需检查，要求 Pull Request 在合并前与目标分支保持最新，并要求维护者审核 `.github/workflows/pathnote-content.yml` 的改动。普通内容 Pull Request 不能修改或绕过这条信任链。

## 审核和状态

状态按照 `draft → reviewed → published` 推进。正文、资源、验证证据或参与审核摘要的 metadata 发生变化后，需要重新计算审核对象摘要并重新完成内容、权利和敏感信息审核。已经发布的 slug 和 `publishedAt` 不能修改；需要停止公开时，由网站使用 withdrawal 记录处理。

实践和项目进入 `reviewed` 前，需要针对准备发布的 revision 补充真实的验证命令、环境、结果和限制。授权证明原件、密钥、个人信息和不能公开的工作资料不得进入这个公开仓库。

## CI 和网站触发

PathNote workflow 会检查每个 Pull Request、`main` 更新和手动运行。Pull Request 使用目标分支中受信任的校验器对比 base/head，不会调用网站构建。`main` 校验通过以后，校验器会判断内容包或它引用的仓库文件是否确实发生变化。

网站构建触发当前保持关闭。等 `pathnote-web` 远端仓库和部署入口完成配置后，维护者需要建立受保护的 `pathnote-preview` environment，添加 secret `PATHNOTE_PREVIEW_DEPLOY_HOOK_URL`，再设置仓库变量 `PATHNOTE_PREVIEW_TRIGGER_ENABLED=true`。workflow 只会在相关内容发生变化，或者维护者手动明确要求时调用这个地址。地址泄漏时应当先在部署平台撤销旧 Hook，再更新 secret；关闭仓库变量可以立即停止新的请求。

内容包新增 `repositoryPath` 或 `validation.evidence` 后，不需要维护一份路径白名单。workflow 会在仓库变更时运行，校验器根据 base/head manifest 反向识别引用关系；只有相关路径发生变化时，结果才会标记为内容变更。
