# 第 01 课：第一个程序与格式化输出

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `rust-01-hello-formatting` |
| Program | [Rust 学习档案](../README.md) |
| 能力标题 | 解释一行 `println!` 在编译期和运行期各发生什么：它为什么是宏、格式串为什么能在编译期检查、`Display` 与 `Debug` 怎样让类型决定自己的打印方式；并能为自定义类型实现 `Display`，用格式说明得到指定的输出 |
| 阶段 | `complete`（2026-10-08 学习者确认关闭） |
| 启动授权 | 2026-10-07，学习者提出“好的，让我们开始rust的01课吧。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/rust-by-example/src/hello.md` 与 `docs/rust-by-example/src/hello/` 下的 6 个文件 | `teaching-spine` | 上游提交 `898f0ac1479223d332309e0fce88d44b39927d28`（随 Rust 1.97.1 发布）；仓库 commit `1b88f9a` | 教学顺序、示例与章内 Activity：Hello World、Comments、Formatted print、Debug、Display、Testcase: List、Formatting |
| Rust 1.97.1 标准库源码（本机 `rust-src` 组件，路径均以 `library/` 开头） | `implementation-authority` | `rustc 1.97.1 (8bab26f4f 2026-07-14)` | `std/src/macros.rs` 中 print 系列宏的定义与文档；`std/src/io/stdio.rs` 的 `_print` 与 `print_to`；`core/src/fmt/mod.rs` 的 9 个格式化 trait、`fmt::Result`、`Arguments` 的模板编码与 `Debug`、`Display` 的文档；`core/src/fmt/rt.rs` 的 `Argument::new_display` 与 `new_debug`；`core/src/macros/mod.rs` 的 `format_args!` 与 `write!`；`alloc/src/fmt.rs` 的格式说明语法与关于返回错误的约定；`alloc/src/string.rs` 中 `ToString` 的 blanket 实现；`alloc/src/vec/mod.rs` 中 `Vec` 的 `Debug` 实现；`core/src/net/ip_addr.rs` 中 `Ipv4Addr` 的 `Display` |
| [`std::fmt` 文档](https://doc.rust-lang.org/1.97.1/std/fmt/) | `interface-authority` | 1.97.1 | 格式说明的语法：位置与命名参数、宽度、填充与对齐、精度、符号、`#` 与进制 |
| [`ROCm/ATOM`](https://github.com/ROCm/ATOM) 的 `atom/mesh/src/` | `implementation-authority`（真实系统锚点） | 提交 `43f5393dc456c1047d316d14be6acb662cce6db7` | `core/circuit_breaker.rs` 中 `CircuitState` 的 derive `Debug` 与手写 `Display` 及其在日志里的使用；`routers/http_router.rs` 中 `Router` 的手写 `Debug`；全目录 derive `Debug` 与手写 `Display` 的数量 |
| [`AMD-AGI/Infera`](https://github.com/AMD-AGI/Infera) 的 `rust/router/Cargo.toml` | `implementation-authority`（真实系统锚点） | 提交 `6e9fd6045479589d240a29878a50335a54c85cf4` | 依赖模板引擎 `minijinja`，作为“运行期才确定的格式要交给模板引擎”的例子 |

### 目标与所需证据

| ID | 可观察目标 | 理解 | 实践 | 实证 |
| --- | --- | --- | --- | --- |
| O1 | 说清一个 Rust 程序从源码到运行的过程，以及一行 `println!` 的六步流水线：哪些事在编译期做完、哪些留到运行期；解释它为什么必须是宏，并与 C 的 `printf`、C++ 的 `std::format` 相比说明换来了什么、付出了什么 | 需要 | 不需要 | 不需要 |
| O2 | 解释 `{}`、`{:?}` 等占位符怎样对应到 `Display`、`Debug` 等 trait，标准库为什么不给 `Vec<T>` 这类泛型容器实现 `Display`，`#[derive(Debug)]` 生成了什么；能预测一段打印代码能否编译并说明原因 | 需要 | 不需要 | 不需要 |
| O3 | 为自定义类型实现 `fmt::Display`，包括逐个写出元素时用 `?` 传播错误；用位置与命名参数、宽度、对齐、填充、精度和进制得到指定的输出 | 需要 | 需要 | 不需要 |

### 当前证据

- **已有证据**：[阶段事件](#条件片段阶段事件) E-01 提供 O1、O2 的节点级理解证据；E-02 的综合验收提供 O1 的整体模型与取舍、O2 的
  预测与 derive 规则的理解证据。已确认的前置只决定讲解起点：学习者熟悉 C/C++ 与 Python，见[学习者画像](../../learning-profile.md)；
  Rust 基础按“没有系统写过”起讲，学习者没有提出异议，也没有另作说明。
- **仍缺证据**：无，见[结课](#条件片段结课)。
- **来源与环境核对（2026-10-07）**：本机 `rustc 1.97.1 (8bab26f4f 2026-07-14)`，x86_64 Linux；试验文件都在仓库外的临时目录。
  - 构建：`rustc hello.rs` 生成 4,354,696 字节的可执行文件，加 `-C strip=symbols` 后为 342,888 字节，加
    `-C prefer-dynamic` 后为 8,568 字节。默认把标准库静态链接进来，只动态依赖 libc 与 libgcc_s。同机 `g++ hello.cpp` 为
    16,352 字节，加 `-static` 后为 2,330,800 字节。直接调用 `rustc` 时默认 edition 是 2015。
  - 展开：对 7 行的 `probe.rs`（一个 derive 了 `Debug` 的 `struct Structure(i32)`，加一行
    `println!("{} days, {:?}", days, Structure(3))`），`-Zunpretty=expanded` 显示 `println!` 展开为
    `::std::io::_print(format_args!("{0} days, {1:?}\n", days, Structure(3)))`，derive 展开为调用
    `Formatter::debug_tuple_field1_finish` 的 `impl Debug`。`-Zunpretty=hir` 显示参数以 `&days`、`&Structure(3)` 的形式
    借用，分别交给 `format_argument::new_display` 与 `new_debug`，格式串变成模板字节
    `b"\xc0\x07 days, \xc0\x01\n\x00"`。`-Z` 选项通过 `RUSTC_BOOTSTRAP=1` 在稳定版上打开，只用于观察。
  - 带格式说明的模板：把那一行改成 `println!("{:>5} days, {:?}, {}", days, Structure(3), MinMax(0, 14))` 后，模板为
    `b"\xc3 \x00\x00(\x05\x00\x07 days, \xc0\x02, \xc0\x01\n\x00"`。按 `core/src/fmt/mod.rs` 的注释解码，第一个占位符
    带 32 位的 flags（填充字符为空格、右对齐、宽度有效）和 16 位的宽度 5。`MinMax` 的 `fmt` 里的 `write!` 另有一段
    模板 `b"\x01(\xc0\x02, \xc0\x01)\x00"`。
  - 报错：占位符引用了不存在的参数时为 “invalid reference to positional argument 1 (there is 1 argument)”；参数多出来时
    为 “argument never used”；格式串放进变量时为 “format argument must be a string literal”；类型没有 `Display` 时为
    E0277 “`Structure` doesn't implement `std::fmt::Display`”；命名占位符找不到变量时为 E0425。前三个出自 `format_args!`
    的展开，E0277 出自类型检查。
  - 各占位符的适用类型：`{:x}` 可用于整数，用于 `1.5` 时报 E0277（`{float}: LowerHex` 不满足）；`{:e}` 可用于整数和
    浮点数；`{:p}` 可用于引用；`Vec`、元组、`Duration` 只有 `Debug` 没有 `Display`；`Ipv4Addr` 有 `Display`。
  - 宽度由类型的 `fmt` 执行：`[{:>10}]` 对整数 14 输出 `[        14]`，对用 `write!` 实现 `Display` 的 `MinMax(0, 14)`
    输出 `[(0, 14)]`，先 `to_string()` 再打印则为 `[   (0, 14)]`；把实现改成 `f.pad(...)` 后宽度生效。
  - 运行期边界：循环打印 10 万行的程序接到 `head -n 1` 之后 panic，信息为
    “failed printing to stdout: Broken pipe (os error 32)”，位置在 `library/std/src/io/stdio.rs:1166`。
  - 对照（gcc 与 g++ 13.3.0，Python 3）：C 的 `printf("%d %s\n", 1)` 能编译，带一条 `-Wformat` 警告，运行时输出 `1` 加
    一串乱码；格式串放进变量后在 `-Wall` 下没有警告。C++20 的 `std::format("{} {}\n", 1)`，以及对没有 `std::formatter`
    特化的类型调用 `std::format`，都是编译错误。Python 的 `"{} {}".format(1)` 在运行期抛 `IndexError`，
    `"{:x}".format(1.5)` 抛 `ValueError`。
  - 真实系统：`atom/mesh/src` 中有 132 处 derive 了 `Debug`，手写的 `Display` 有 9 处。

  以上是这一个工具链和平台上的观察。

### 核心工件与参考

| 角色 | 路径或引用 | 说明 |
| --- | --- | --- |
| 来源或知识产物 | `docs/rust-by-example/src/hello.md` 与 `hello/` 目录 | 教程快照，不修改 |
| 你写（learner-owned） | `rust/lesson01_hello_formatting/src/lib.rs` | P1 的五个 `Display` 实现（含 A8 的 `Vector`）与 `status_line`；骨架只含四个类型定义，由 Agent 放入后归学习者 |
| 我维护（agent-owned） | `rust/lesson01_hello_formatting/tests/` | P1 的验收测试，六个文件共 19 项：A1–A5 各一个文件，另有 A8 的 `a8_vector.rs` |
| 我维护（agent-owned） | [节点 2 图解页](../attachments/01-hello-formatting/println-pipeline.html) | 一行 `println!` 的六步流水线、五种改法各在哪一步被拦下、与 C 和 C++ 的对照；可交互，离线可用 |

## 条件片段：练习约定

- **编号与版本**：P1，版本 2；学习者接受于 2026-10-08（“明白，接受版本2约定”）。版本 1 接受于同日（“接受”）。
  版本 2 只改 A2：增加“底层写入失败时返回 `Err` 并停止继续写”。这是约定澄清：O3 本来就要求用 `?` 传播错误，版本 1 的验收项漏掉了对应的检查。
- **为什么做**：O3 需要实践证据。综合验收后只有理解证据，没有学习者亲手写出并通过验收的代码。
- **你交付什么**：在 `rust/lesson01_hello_formatting/src/lib.rs` 中完成五件事。前三件是教程的 Activity，后两件针对本课
  暴露过的差距。
  1. `Complex`（`real: f64`、`imag: f64`）：derive `Debug`；手写 `Display`，输出形如 `3.3 +7.2i`、`4.7 -2.3i`。
  2. `List`（包着 `Vec<i32>`）：手写 `Display`，带下标，`[1, 2, 3]` 输出 `[0: 1, 1: 2, 2: 3]`，空列表输出 `[]`。
  3. `Color`（`red`、`green`、`blue` 均为 `u8`）：手写 `Display`，输出形如 `RGB (128, 255, 90) 0x80FF5A`。
  4. `WorkerId`（包着 `u32`）：手写 `Display`，7 输出 `w7`，调用方给的宽度、对齐和填充字符都要生效。
  5. `status_line(name: &str, load: f32, width: usize) -> String`：`name` 左对齐到 `width` 宽，接 `|`，`load` 右对齐到
     6 宽并保留两位小数，再接 `|`；`status_line("w7", 0.4567, 6)` 返回 `w7    |  0.46|`。
- **验收项**：

| ID | 可观察标准 | 检查方式 |
| --- | --- | --- |
| A1 | `Complex` 的 `Display` 与 `Debug` 输出正确 | 测试 `a1_complex` |
| A2 | `List` 的输出正确，包括单个元素和空列表；底层写入失败时 `fmt` 返回 `Err`，并且不再继续往下写 | 测试 `a2_list` |
| A3 | `Color` 的输出正确，包括需要补 0 的分量 | 测试 `a3_color` |
| A4 | `WorkerId` 不带说明时输出 `w7`，带 `>`、`<`、`^` 和填充字符时都按要求对齐，宽度不足时不截断 | 测试 `a4_worker_id` |
| A5 | `status_line` 的输出正确，包括名字比 `width` 长时不截断 | 测试 `a5_status_line` |
| A6 | 这个 crate 通过 `cargo fmt --check` 与 `cargo clippy -- -D warnings`；不用 `unwrap`、`expect` 和 `unsafe` | 命令 |
| A7 | 说明 A4 选了哪种写法、有没有堆分配、为什么只用 `write!` 不行 | 学习者的说明，按要点核对 |
| A8 | A1–A7 通过后的无提示小变式：实现一个新的小类型并通过测试 | 测试 |

- **运行方式**：单项为
  `bash scripts/host-cpu.sh run -- cargo test -p rust-lesson01-hello-formatting --test a1_complex`，去掉 `--test …` 即全部。
  完成之前整个 workspace 的 `host-cpu.sh test` 与 `host-cpu.sh lint` 会在这个 crate 上失败，练习期间这些改动留在本地。
- **文件边界**：

| 边界 | 路径或受限模式 |
| --- | --- |
| 你写 | `rust/lesson01_hello_formatting/src/lib.rs` |
| 我维护 | `rust/lesson01_hello_formatting/Cargo.toml`；`rust/lesson01_hello_formatting/tests/`；根 `Cargo.toml` 的 workspace members（已加入 `"rust/*"`）与 `Cargo.lock`；本 Lesson 记录；`docs/rust-learning/README.md` 的 Checkpoint 与课程索引行 |
| 我只读 | `docs/rust-by-example/src/hello/` |
| 本次不动 | 其他 crate、CI 配置和依赖 |

- **求助如何影响证据**：随时可以求助；透露关键写法只影响相应的验收项，之后用一个小变式在无提示下恢复。A8 期间不给提示。
- **非目标与可选项**：不引入第三方依赖，不做性能要求，不做教程 Activity 的加分项（符号后加空格）。
- **完成门槛**：A1–A8 全部通过，阻塞问题全部关闭。

## 条件片段：帮助影响

| 透露到什么程度 | 影响的验收项或工件 | Agent 是否写了学习者核心工件 |
| --- | --- | --- |
| 学习者问 F1 怎么改。说明了 `Result` 的三种去处，指出中间的 `write!` 要在后面加 `?`、最后一个直接作为返回值，并给了一个与练习无关的两行示意；另外解释了测试里会失败的 writer 及逐次调用的记录 | A2 中“写入失败时返回 `Err`”一项的独立性；已由 A8 的无提示变式恢复：`a8_vector` 的错误传递一项在无提示下通过 | 否 |

## 条件片段：阶段事件

| 日期 | 覆盖范围 | 证明了什么 | 证据链接 | 标注 |
| --- | --- | --- | --- | --- |
| 2026-10-07 | E-01：开课导入、节点 1–5 与两次节点检查；导师串讲；综合验收发出 | 节点 2 检查（假设把 `println` 做成运行期解析格式串的函数）：一次答对哪几步挪到运行期、宏展开一步消失，以及两类错误推迟到运行期才暴露。差距在取舍：把“不检查类型”当成可以按另一种类型打印的灵活性，没有想到格式串能因此成为运行期的值。这一问对“灵活性”的范围说得宽，属于题目问题，已澄清并补讲。节点 3–4 检查（`Worker` 的四行打印与配置文件里的日志格式）：四行能否编译全部判断正确，原因指向没有实现 trait 和浮点数不支持 `{:x}`；没有说出各自的最小修法，即 `Debug` 可以 derive 而 `Display` 必须手写，留到综合验收复查。换场景的复查通过：指出 `println!` 只接受字面量、运行期的格式只能交给模板引擎、占位符写错要到那一行执行时才报错。随后讲节点 5（格式说明由各类型的 `fmt` 执行，`f.pad`），完成导师串讲，发出综合验收三题：口述、预测与最小修法、中间字符串与对齐的取舍。 | 本会话；[当前证据](#当前证据)中的核对；[节点 2 图解页](../attachments/01-hello-formatting/println-pipeline.html) | 无 |
| 2026-10-08 | E-02：综合验收作答与补讲；复查题发出 | 口述讲清了编译期的展开、解析、选 trait 与生成模板，运行期的加锁与按模板调用 `fmt`，类型通过 `Display`、`Debug` 接入；取舍中说出了“格式串必须是字面量”这一代价，E-01 的差距已补上。注意事项只说了 `Debug` 会打印所有字段，没有提到运行期的加锁与写失败 panic。预测题三行判断全对，并说明 `Display` 不能 derive，E-01 中未说出的区别已补上；差距是提出为 `Vec<Shard>` 实现 `Display`，这会被 E0117 拒绝，该规则此前只提过一句。取舍题指出多了一个中间字符串，并给出直接 `write!` 的写法；差距是认为同事的版本能对齐（本机两个版本都输出 `[w7: 0.5]`），并把 `f.pad` 套在格式串外面（报 “format argument must be a string literal”），“何时先拼字符串合理”因此只答到笼统层面。已补讲：宽度留在 `f` 里，`write!` 里新写的占位符不继承它，`f.pad` 接收的是成品文字；不能为外部类型实现外部 trait，要包一层自己的类型。发出三道复查题。复查作答：四种 `fmt` 写法的输出与理由全部正确，并指出直接把 `f` 传给字段的 `fmt` 比先 `to_string()` 少一个临时字符串；三个 `impl` 的取舍判断正确，只是把元组说成了基本类型 `u32`。这两处差距关闭。运行期边界一题回答“不知道”，只猜到管道会提前关闭，说不出后果、改法和加锁这一条；已对照 `print_to` 的源码重讲，并换成路由器访问日志的场景再次复查。第二次复查通过：指出全进程共用一把锁，一个线程写得慢会让其他线程都等在这一行；磁盘写满时写入失败，`println!` 会 panic。至此 O1、O2 的理解证据充分，O3 的理解证据充分、实践证据待补，已提出练习约定 P1（版本 1），学习者当日接受。验收测试已建立并自检：骨架下五个测试文件都是预期的编译失败，原因分别是四个类型没有 `Display` 和找不到 `status_line`；一份不入库的参考实现通过全部 14 项，clippy 无告警；8 种故意写错的变体（不带符号、不带下标、多出分隔符、十六进制不补 0、十六进制小写、忽略宽度、名字右对齐、只留一位小数）都被对应的测试文件判为失败。 | 本会话；本机核对：`impl fmt::Display for Vec<Shard>` 与对元组的同类实现均报 E0117；把循环打印改成锁住句柄后用 `writeln!` 并在出错时退出，接到 `head -n 2` 后正常结束 | 无 |
| 2026-10-08 | E-03：练习首次提交与首轮 Review | 学习者提交 `src/lib.rs`。Agent 复验：验收测试未被改动，14 项全部通过，`cargo fmt --check` 与 `cargo clippy -- -D warnings` 通过，没有 `unwrap`、`expect`、`unsafe`；A1–A6 按版本 1 的标准通过。提交前学习者问了四个前置点（分支、`Vec` 的长度与遍历、十六进制表示的含义），得到的是通用语法和概念，没有透露任何验收项的写法。Review 发现一个与 O3 直接相关的问题 F1：`List` 的 `fmt` 用 `let _ = write!(…)` 丢弃了写入结果；用一个第 3 次写入失败的 writer 探测，它继续写了 12 次并返回 `Ok(())`，留下残缺的 `[0, 1: 2, 2: 3]`，而用 `?` 的参考实现在第 3 次后停止并返回 `Err`。版本 1 的验收项没有覆盖这一点，属于约定的缺口，已提出版本 2（A2 增加错误传递的检查）等待接受。约定外的观察，不阻塞：`Complex` 用 `{:.1}` 会丢位数（1.25 打印成 1.2），手工拼符号在虚部为 -0.0 时输出 `+-0.0i`；`Color` 多用了两个临时字符串。学习者接受版本 2 后追问怎么改以及那个会失败的 writer 是什么，得到了改法与逐次调用的记录（见帮助影响）。第二次提交：F1 修复并复验关闭；两条不阻塞的观察也一并改了，`Complex` 改用默认精度与 `{:+}`，`Color` 改为一个 `write!` 里重复引用位置参数。A7 的说明通过：选的是先 `format!` 再 `f.pad`，有堆分配，只用 `write!` 不行是因为它带不上 `f` 里的对齐要求；补充了一点，分配来自 `String` 本身，这里长度其实有上界，可以像标准库的 `Ipv4Addr` 那样改用栈上缓冲区。A8 已发出：新类型 `Vector`，测试 `a8_vector` 共 4 项，自检同前（参考实现通过，不带符号与丢弃结果两种变体失败），当时为预期的编译失败。第三次提交：学习者在没有提示的情况下实现了 `Vector` 的 `Display`，Agent 复验 `a8_vector` 4 项全部通过，其中包括写入失败时返回 `Err` 并停止；全套 19 项、`cargo fmt --check` 与 clippy 均通过，测试文件未被改动。A1–A8 全部通过，帮助影响已由 A8 恢复。随后列出结课证据，学习者确认关闭。 | 本会话；本机复验与探测输出 | 练习关闭；结课 |

## 条件片段：需要跟踪的问题

| ID | 对应验收项或目标 | 严重度 | 状态 | 证据 |
| --- | --- | --- | --- | --- |
| F1 | O3、A2 | 阻塞 | 已关闭 | `List` 的 `fmt` 丢弃 `write!` 的结果：第 3 次写入失败时仍返回 `Ok(())` 并继续写。版本 2 的测试已加入并自检（参考实现通过，丢掉一处结果的变体失败）；学习者当时的实现在该测试上失败。关闭证据：学习者把中间的 `write!` 都改为以 `?` 传出，Agent 复验 `a2_list` 4 项全部通过，全套 15 项、`cargo fmt --check` 与 clippy 均通过 |

## 条件片段：结课

| 目标 | 所需证据 | 证据链接 | 判断 |
| --- | --- | --- | --- |
| O1 | 理解 | [阶段事件](#条件片段阶段事件) E-01 的节点 2 检查；E-02 的综合验收口述，以及运行期两条边界的两轮复查 | 充分 |
| O2 | 理解 | E-01 的节点 3–4 检查；E-02 的综合验收预测题，以及“不能为外部类型实现外部 trait”的复查 | 充分 |
| O3 | 理解、实践 | E-02 中四种 `fmt` 写法的输出预测；E-03 中[练习约定 P1](#条件片段练习约定) 的 A1–A8 | 充分 |

- **未关闭的阻塞问题**：0。F1 已复验关闭。
- **帮助影响是否已恢复**：已恢复，见[帮助影响](#条件片段帮助影响)与 E-03。
- **非阻塞余项**：Program 的 Objective 与学习者的 Rust 基础仍没有得到学习者本人的说明；练习前的提问表明分支、循环和 `Vec` 的
  基本操作当时还没有学过，后续课次的练习要先交代用到的语法。`src/lib.rs` 里混用了 `core::fmt` 与 `std::fmt::` 两种路径。
- **学习者确认**：2026-10-08，“确认关闭。”
- **结课结论**：Lesson 01 关闭。学习者能讲清一行 `println!` 在编译期与运行期的分工和它与 `printf` 的取舍，能判断打印代码能否
  编译及其原因，并独立写出了带错误传递和格式说明的 `Display` 实现。
