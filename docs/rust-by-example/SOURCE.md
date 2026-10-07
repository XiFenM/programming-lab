# 来源记录

本目录是 Rust by Example（RBE，Rust 官方的示例式教程）的固定版本快照，作为
[Rust 学习档案](../rust-learning/README.md) 的教学主线。`src/` 保持上游原样，不在其中写笔记或修改示例。

## 来源快照

- 在线地址：<https://doc.rust-lang.org/rust-by-example/>，跟随 stable 发布更新，没有固定版本
- 与本快照同一版本的在线地址：<https://doc.rust-lang.org/1.97.1/rust-by-example/>
- 上游仓库：<https://github.com/rust-lang/rust-by-example>
- 固定提交：`898f0ac1479223d332309e0fce88d44b39927d28`（提交日期 2026-04-19）
- 选择依据：`rust-lang/rust` 的 tag `1.97.1`（commit `8bab26f4f68e0e26f0bb7960be334d5b520ea452`）中，子模块
  `src/doc/rust-by-example` 指向的就是这个提交，也就是随 Rust 1.97.1 发布的那一版书。宿主机路线固定的
  工具链是 `rustc 1.97.1 (8bab26f4f 2026-07-14)`，两者一致
- 取回日期：2026-10-07 (UTC)
- 校验：`src/` 的 Git tree 为 `0d9cd7b98e79324ca6b6879ab58ce4ffb5318319`，与上游该提交的 `src` 相同

## 已复制与未复制的内容

| 本地路径 | 内容 |
| --- | --- |
| `src/` | 198 个 Markdown，约 0.4 MB：196 个章节文件、首页 `index.md` 和目录 `SUMMARY.md` |
| `book.toml` | 上游的 mdBook 配置，其中 `[rust] edition = "2021"` 是书中示例采用的 edition |
| `LICENSE-MIT`、`LICENSE-APACHE` | 上游的两份许可证原文 |

没有复制 `po/` 下的译文、`theme/`、CI 配置和贡献说明。

上游以 MIT 或 Apache-2.0 双许可发布，使用者任选其一；版权与许可条款以上游仓库为准。

## 与在线最新版的差别

2026-10-07 时 stable 是 Rust 1.99.0（2026-10-01 发布），它对应的上游提交是
`15308f3e951814ef3475d2b58f48276e6b17b9af`。与本快照相比只改了 5 个文件、13 行，都是措辞、注释排版和一个变量名：
`src/expression.md`、`src/hello/comment.md`、`src/macros.md`、`src/meta.md`、`src/mod/split.md`。

同一天上游 `master`（`dcc14f912bf8790792a2df082eddc82ab2539229`）又改了 4 个文件，其中链表示例被重写，这些改动
还没有进入 stable。

## 本地核对

核对于 2026-10-07，环境是 x86_64 Linux 上的 `rustc 1.97.1 (8bab26f4f 2026-07-14)`，edition 2021 与 2024 各做一遍。
书按 edition 2021 编写，仓库的 Cargo workspace 使用 edition 2024，所以两种都要看。

| 核对内容 | 方法 | 结果 |
| --- | --- | --- |
| 示例能否通过 | 对 `index.md` 和 196 个章节文件逐个执行 `rustdoc --test --edition <E> <文件>` | 收集到 257 个示例：211 个参与测试并全部通过（其中 4 个只编译不运行，2 个预期编译失败），46 个标记为 `ignore`；两个 edition 结果相同 |
| 未被运行的代码块 | 上面的 46 个，加上 31 个同时标了 `editable` 与 `ignore`、不被 rustdoc 收集的代码块，共 77 个；逐个抽出，用 `rustc --edition <E> --emit=metadata` 只编译不运行 | 36 个在两个 edition 下都能编译，40 个报完全相同的错误，1 个不同 |
| 输出是否随 edition 变化 | 去掉 `ignore`、`no_run`、`compile_fail` 和单独指定 edition 的代码块后剩下 206 个，在两个 edition 下分别编译运行，比较标准输出 | 202 个逐字相同；3 个只有行的顺序不同；1 个打印的是可执行文件自身的路径 |

- 唯一随 edition 变化的是 `src/std_misc/ffi.md`：其中的 `extern` 块在 edition 2021 下可以编译，在 edition 2024 下
  报错 “extern blocks must be unsafe”，需要写成 `unsafe extern`。
- 只有行顺序不同的 3 个是 `src/std/hash.md`、`src/std_misc/threads.md` 和
  `src/std_misc/threads/testcase_mapreduce.md`，原因是 `HashMap` 的遍历顺序和线程调度本来就不确定。
- 77 个未运行的代码块多数是故意留错、等读者修复的示例，或者是不完整的片段，报错属于预期。
- `src/unsafe/asm.md` 的内联汇编示例按目标架构分支，这里只核对了 x86_64。

以上是这一版书在这一个工具链和平台上的观察，不代表其他 Rust 版本的行为。

## 更新方式

宿主机固定的 Rust 版本升级时，按新版本的 tag 找到子模块 `src/doc/rust-by-example` 指向的提交，整体替换 `src/`
并更新本文件和上面的核对结果。不要混用不同提交的文件，也不要只为跟上在线最新版而单独更新某几页。
