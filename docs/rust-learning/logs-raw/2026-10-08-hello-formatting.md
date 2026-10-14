---
archive_type: "study-log-visible-dialogue"
schema_version: 1
archive_id: "sl-bd4cf96545a64409a8a01516fdcaf2ac"
status: "final"
title: "格式化输出：println! 的编译期与运行期、Display 与 Debug、格式说明 · 可追溯可见文本对话"
provider: "claude"
project_name: "programming-lab"
project_fingerprint: "7c4c768a8b0a"
source_session_id: "a955cb4c-7f49-5c49-b59d-1f2d1c81cadd"
source_file: "a955cb4c-7f49-5c49-b59d-1f2d1c81cadd.jsonl"
start_message_id: "msg-c7994246f6017f873bc0"
end_message_id: "msg-b93dc0e30502d76b79a5"
message_count: 32
source_sha256: "1458d2e42f5ec40d1781a86ca5350b452cd36910bf1b3f434966730870b4d41c"
visible_content_sha256: "ce126ad80847375269479206069a2fc5984b5ddb1ee092d582c63f2a5a49d7d3"
target_precondition_sha256: null
first_message_at: "2026-10-07T13:28:41.862Z"
last_message_at: "2026-10-08T04:20:02.714Z"
created_at_utc: "2026-10-14T03:12:17.780663+00:00"
updated_at_utc: "2026-10-14T03:12:17.780663+00:00"
normalization: {"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"}
redaction: {"version":"study-log-redaction-v1","categories":[],"applications":[]}
privacy_risks: {"categories":["proprietary"],"counts":{"proprietary":49}}
structured_record: "docs/rust-learning/logs/2026-10-08-hello-formatting.md"
message_phases: [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null]
migration: null
---

# 格式化输出：println! 的编译期与运行期、Display 与 Debug、格式说明 · 可追溯可见文本对话

> 此文件是规则化提取的“可追溯可见文本对话”，不是完整客户端 Session，也不代表已经匿名化。
> system、developer、reasoning、工具事件、客户端注入和附件正文默认不包含在内。

结构化学习记录：[查看记录](<../logs/2026-10-08-hello-formatting.md>)

---

**001 · 用户** · `2026-10-07T13:28:41.862Z` · `msg-c7994246f6017f873bc0`

好的，让我们开始rust的01课吧。

---

**002 · 助手** · `2026-10-07T13:33:01.435Z` · `msg-abbd4b015a17afd14af2`

资料读完了，正在用固定的编译器取真实产物（宏展开结果、报错原文），接着建第 01 课的记录并做一页图解，然后开讲。

---

**003 · 助手** · `2026-10-07T13:39:52.634Z` · `msg-1b7ec97b9e3f6235d698`

图解页已生成并通过结构检查，接下来发布它、写入第 01 课的记录，然后就开讲。

---

**004 · 助手** · `2026-10-07T13:43:49.927Z` · `msg-b5b0b7af51f3f5c8c411`

第 01 课已开课。记录在 `docs/rust-learning/lessons/01-hello-formatting.md`，Checkpoint 已指向它，这些改动还没有提交。三个目标：说清 `println!` 的编译期与运行期（理解），说清占位符与 `Display`、`Debug` 的对应（理解），自己实现 `Display` 并控制格式（理解加实践）。结课需要你确认，下一课不会自动开始。

我先按“熟悉 C/C++ 和 Python，没有系统写过 Rust”来讲。如果你已经写过一些，告诉我写到什么程度，我会跳过相应的部分。

## 这一课要解决什么

把一个值打印成文字，需要两样信息：输出长什么样，以及每种类型怎样把自己变成文字。

- C 的 `printf` 把第一样交给运行期才解析的格式串，第二样写死在 `%d`、`%s` 这些转换符里。格式和参数对不上时照样能编译，自定义类型也接不进来。
- C++ 的 `cout <<` 靠重载解决了类型安全和扩展，代价是放弃了格式串。
- Rust 两样都要：保留格式串，让“格式和参数对不上”成为编译错误，并且任何类型都能接入。

Rust 的办法是两个机制配合：**宏**负责在编译期读懂格式串，**trait** 负责让类型声明“我能这样打印”。这两个机制贯穿整门语言，这一课是第一次见到它们。

学完你应该能：

- 对着一行 `println!` 讲清编译器做了哪几步、每一步检查什么、运行时还剩什么；
- 看到一段打印代码，判断它能不能编译、错在哪一步；
- 为自己的类型实现 `Display`；
- 用一分钟左右讲清它和 `printf`、`std::format` 的取舍。

全流程骨架，后面每个节点都会回到它：

```text
第 1 步  源码          println!("{} days, {:?}", days, Structure(3));
──────── 编译期：rustc 运行时 ────────
第 2 步  宏展开        println! 变成 _print(format_args!(…))
第 3 步  解析格式串    切成字面文字和占位符，核对占位符与参数的个数
第 4 步  选 trait      {} 要 Display，{:?} 要 Debug；检查参数的类型是否实现了它
第 5 步  生成模板      格式串变成一段模板字节，连同参数表装进 fmt::Arguments
──────── 运行期：程序运行时 ────────
第 6 步  写出结果      锁住标准输出，按模板写；遇到占位符就调用那个类型的 fmt
```

路线：节点 1 讲程序骨架与编译运行，节点 2 讲这六步本身，节点 3 展开第 4 步里的 `Display` 与 `Debug`，节点 4 展开第 6 步里你自己写的 `fmt`，节点 5 展开第 3 步里的格式说明。这次讲前两个节点。

## 节点 1：程序骨架与编译运行

教程的第一个程序只有三行：

```rust
fn main() {
    println!("Hello World!");
}
```

`fn main()` 是程序入口，和 C 的 `main` 一样。函数体里是一条以分号结尾的语句。`println!` 末尾的 `!` 表示这是一次宏调用，不是函数调用，节点 2 专门讲它。

编译和运行各一条命令：`rustc hello.rs` 生成可执行文件 `hello`，`./hello` 运行它，对应 C++ 的 `g++ hello.cpp -o hello`。日常开发用的是 `cargo`，它管理依赖并替你调用 `rustc`。这一课的示例都是单个文件，直接用 `rustc` 就够。

有三处和 C++ 的习惯不同：

- **可执行文件偏大。** 本机用 `rustc` 1.97.1 编出的 `hello` 是 4.35 MB，`g++` 编出的 C++ 版本是 16 KB。差别来自链接方式：Rust 默认把标准库连同调试符号静态链接进来，运行时只依赖 libc。去掉符号（`-C strip=symbols`）后是 343 KB，改成动态链接标准库（`-C prefer-dynamic`）后是 8.6 KB。C++ 这边加上 `-static`，也会涨到 2.3 MB。
- **直接调用 `rustc` 默认按 edition 2015 处理。** 书里的示例按 2021 写，单文件试验时加上 `--edition 2021`。用 `cargo` 时 edition 写在 `Cargo.toml` 里，没有这个问题。
- **块注释可以嵌套。** `/* 外层 /* 内层 */ 还在注释里 */` 在 Rust 里是一个完整的注释，在 C 里不是。另外还有文档注释 `///` 和 `//!`，它们会被生成文档，第 16 课再讲。

## 节点 2：`println!` 为什么是宏

这一节配了一页可以逐步点开的图解，里面有每一步的真实编译产物，以及五种写错时的报错原文：<https://claude.ai/artifact/EcVJMRaxpzCa2V5eQDcXXL>。链接是私有的，只有你能打开；仓库里的副本在 `docs/rust-learning/attachments/01-hello-formatting/println-pipeline.html`。下面的文字和它是同一条线，建议对照着看。

**例子。** 整节只用一个 7 行的程序，下面叫它 `probe.rs`。它定义一个只包着一个 `i32` 的结构体 `Structure`，用 `#[derive(Debug)]` 让编译器为它生成 `Debug` 的实现。`main` 里把整数 31 绑定到 `days`，然后一行 `println!` 打印两样东西：`days` 用 `{}`，`Structure(3)` 用 `{:?}`。输出是 `31 days, Structure(3)`。两个打印都取自教程，我把它们并到了一行。

```rust
#[derive(Debug)]
struct Structure(i32);

fn main() {
    let days = 31;
    println!("{} days, {:?}", days, Structure(3));
}
```

**结论。** 格式串对不对、参数个数对不对、这个类型能不能这样打印，这三件事都在编译期解决；运行期只剩加锁和按模板写出。要做到这一点它必须是宏，因为函数只能拿到运行期的值，拿不到格式串的内容，也拿不到参数的个数和类型。

**机制。** 对照骨架，看编译器实际产出了什么。第 2 步之后，那一行变成：

```rust
::std::io::_print(format_args!("{0} days, {1:?}\n", days, Structure(3)));
```

`println!` 本身只是标准库里一个两条规则的宏。它把参数原样交给 `format_args!`，再把结果传给函数 `_print`。真正读懂格式串的是 `format_args!`，它是编译器内建的。可以看到占位符已经被编了号，换行符也被拼了进去。

第 3 到第 5 步之后，`format_args!(…)` 那一段变成下面这样（排版略有调整，`super let` 是编译器内部的写法，当作 `let` 读）：

```rust
super let args = (&days, &Structure(3));
super let args = [format_argument::new_display(args.0),
                  format_argument::new_debug(args.1)];
unsafe { format_arguments::new(b"\xc0\x07 days, \xc0\x01\n\x00", &args) }
```

这里有三件事：

- **参数是借用的。** 它们以 `&days`、`&Structure(3)` 的形式传入，打印不会拿走它们，所以打印之后 `days` 还能用。
- **占位符决定调用哪个函数。** `{}` 被翻译成 `new_display`，`{:?}` 被翻译成 `new_debug`。两者的签名分别是 `new_display<T: Display>(x: &T)` 和 `new_debug<T: Debug>(x: &T)`。`T: Display` 读作“T 必须实现了 Display”，类型检查就发生在这里。
- **格式串变成了 13 个字节的模板。** `\xc0` 是一个占位符；`\x07` 后面跟 7 个字节的字面文字 ` days, `；再一个占位符；`\x01` 后面跟换行；`\x00` 结束。花括号已经不存在了。

第 6 步在运行期。`_print` 锁住标准输出，顺着模板写。遇到占位符，就调用参数表里记下的那个函数：对 `days` 是 `i32` 的 `Display::fmt`，对 `Structure(3)` 是 derive 出来的 `Debug::fmt`。

**为什么这样设计。** 用同一个错误“少传一个参数”来比三条路。

第一条路是 C 的 `printf`：做成函数，格式串是一个普通的运行期字符串。函数的签名只能写成“一个字符串，加上若干个类型未知的参数”。于是解析只能在运行期做，每次调用做一遍；个数和类型对不上，语言本身发现不了。本机的 gcc 13.3 对 `printf("%d %s\n", 1)` 给了一条 `-Wformat` 警告，但照样编译通过，运行时输出 `1` 加一串乱码。把格式串放进变量后，连警告也没有了。那条警告是编译器针对 `printf` 额外做的检查，不是语言的规则。

第二条路是 C++ 的 `cout <<`：放弃格式串，每个值用一次重载的 `<<`。类型安全有了，自定义类型也能接入。但“输出长什么样”不再集中写在一处，宽度和精度要靠有状态的操纵符。

第三条路是 Rust 的：格式串留下，但要求它是字面量，让编译器在编译期读它。这需要一种在编译期运行、能看到字面量内容和参数列表的东西，函数做不到，宏可以。普通的 Rust 函数既没有可变参数也没有重载，所以“参数个数不定”这件事本身也只有宏能表达。类型怎样接入则交给 trait：每种占位符对应一个 trait，类型实现了哪个，就能用哪种占位符打印。C++20 的 `std::format` 后来走了同一条路：本机 g++ 13.3 对少传参数的 `std::format("{} {}\n", 1)` 直接报编译错误。

换来的是：格式和参数对不上的错误不可能留到运行期，运行期也不必再解析格式串。付出的是：格式串必须写死在源码里；每一种打印方式都是一个 trait，类型要逐个实现。

**真实系统。** 以上都能在 1.97.1 的标准库源码里对上，路径都在 `library/` 下：

- `std/src/macros.rs`：`println!` 的定义，只有两条规则。
- `core/src/macros/mod.rs`：`format_args!` 标着 `rustc_builtin_macro`，宏体是一句注释 `/* compiler built-in */`。
- `core/src/fmt/rt.rs`：运行期每个参数存成两个指针，一个指向值，一个指向它的 `fmt` 函数。
- `std/src/io/stdio.rs`：`_print` 写失败时执行 `panic!("failed printing to {label}: {e}")`。

**边界。** 有三条：

- **格式串必须是字面量。** 把它存进变量再传给 `println!`，报错是 `format argument must be a string literal`。
- **每次调用都要给标准输出加锁。** 标准库文档提醒，在很热的循环里这可能成为瓶颈。办法是先 `stdout().lock()`，再用 `writeln!` 往锁住的句柄里写。
- **写失败会 panic。** 我写了一个循环打印 10 万行的程序，执行 `./many | head -n 1`。`head` 读完第一行就退出，程序随即 panic，信息是 `failed printing to stdout: Broken pipe (os error 32)`。所以输出要交给管道的命令行工具通常改用 `writeln!`，它返回 `Result`，可以自己处理。文档还建议诊断和进度信息用 `eprintln!` 写到标准错误。

**面试怎么讲**（约 60 秒）：

> `println!` 是宏不是函数，因为它要在编译期读格式串。标准库里的 `println!` 只是把参数转给编译器内建的 `format_args!`。后者把格式串切成字面文字和占位符，核对占位符和参数的个数，再按占位符选 trait：`{}` 要 `Display`，`{:?}` 要 `Debug`，类型没实现就是编译错误。编译结果是一段模板字节加一张参数表，每个参数是一个值指针加一个 `fmt` 函数指针。运行期不再解析，只是锁住标准输出按模板写。和 `printf` 比，错配不会留到运行期，代价是格式串必须是字面量。另外它每次调用都加锁，写失败会 panic。

## 检查题

假设 Rust 当初把它做成一个普通函数，像 C 的 `printf` 那样到运行时才解析格式串。对照六步回答：

1. 哪几步的工作会从编译期挪到运行期？
2. “少传一个参数”和“用 `{}` 打印一个没有实现 `Display` 的类型”这两种错误，暴露的时机分别会怎样变化？
3. 这样做反过来能得到什么现在得不到的灵活性？

用自己的话回答就行，不需要写代码。另外，Program 里的学习目标还标着“尚未确认”，方便时看一眼 `docs/rust-learning/README.md` 里的 Objective，告诉我是否合适。

---

**005 · 用户** · `2026-10-07T14:57:39.813Z` · `msg-473b8d01e5d6dde85701`

1. 第3、4、5步工作从编译期挪到运行时，第2步应该直接没了，因为函数没有展开的过程。
2. 这两种错误在宏的方案中可以在编译期的第3步和第4步检查发现，但做成普通函数后只能到运行时才会被解析发现。
3. 由于此时编译期不检查个数和类型对不对的上，可以将某些参数以另一种类型的方式进行打印出来。

---

**006 · 助手** · `2026-10-07T14:59:39.732Z` · `msg-24947699d1027e5420f8`

You've hit your session limit · resets 6:20pm (UTC)

---

**007 · 用户** · `2026-10-07T22:50:54.119Z` · `msg-ba0ffc779fbc72b4c710`

请继续

---

**008 · 助手** · `2026-10-07T22:54:04.153Z` · `msg-1a91f55d93237981ffd2`

前两问答对了，第三问差一点。先说反馈，再接着讲节点 3 和节点 4。

## 上一题的反馈

**第 1 问，对。** 第 3、4、5 步挪到运行期，第 2 步消失，和你说的一样。

**第 2 问，方向对，补两点。**

- “运行时才发现”的前提是那一行真的被执行到。一条写在错误处理分支里的打印语句，可能上线很久才第一次运行。
- 能不能“发现”，取决于运行期有没有专门做检查。Python 做了，所以会抛异常：本机 `"{} {}".format(1)` 报 `IndexError: Replacement index 1 out of range for positional args tuple`。C 没做，所以表现为上次看到的 `1` 加一串乱码。

**第 3 问，有差距。** 这一问我问得比较宽，没有说清是哪方面的灵活性，责任在题目。你的回答“可以把参数按另一种类型的方式打印”要分成两种情况：

- **同一个值换一种写法。** 比如整数用十进制、十六进制或调试格式。这在现在的设计里就能做，而且是安全的：`println!("{:x}", 255)` 输出 `ff`。
- **把一种类型的字节当成另一种类型来读。** 比如 C 里的 `printf("%s", 42)`。不检查类型确实拦不住它，但那是未定义行为，不是一种能力。Python 的运行期方案同样不允许：`"{:x}".format(1.5)` 报 `ValueError: Unknown format code 'x' for object of type 'float'`。

真正换来的灵活性是：**格式串本身可以是运行期的值**，来自配置文件、翻译文件或用户输入。Python 里 `fmt = "{} days"; fmt.format(31)` 可以正常输出 `31 days`。Rust 里 `println!(fmt, 31)` 就是图解页第三种改法的那个编译错误。一个真实的例子：Infera 的 router 依赖模板引擎 `minijinja`，它的 `Cargo.toml` 注释里提到了 chat template。chat template 是运行时才从模型配置里读到的数据，不可能写成 `format!` 的字面量，只能交给运行期的模板引擎。

下面的检查题里会换一个场景再问这一点。你提到的“换一种写法打印”正好是节点 3 的主题。

## 节点 3：`Display` 与 `Debug`

对应骨架的第 4 步“选 trait”。

**结论。** 占位符里冒号后面的内容决定用哪个 trait。`{}` 用 `Display`，是给最终读者看的，必须自己写。`{:?}` 用 `Debug`，是给开发者看的，可以让编译器生成。标准库的类型几乎都有 `Debug`，只有写法没有争议的类型才有 `Display`。

**机制。** 标准库在 `library/core/src/fmt/mod.rs` 里定义了 9 个格式化 trait，各自对应一种占位符。右边一列是我在本机逐个编译确认的：

| 占位符 | trait | 哪些类型能用 |
| --- | --- | --- |
| `{}` | `Display` | 数字、`bool`、`char`、字符串、`Ipv4Addr` 这类有公认写法的类型 |
| `{:?}` | `Debug` | 标准库里几乎所有类型，包括 `Vec`、元组、`Duration` |
| `{:x}` `{:X}` `{:o}` `{:b}` | `LowerHex` `UpperHex` `Octal` `Binary` | 整数。浮点数不行：`println!("{:x}", 1.5)` 报 E0277 |
| `{:e}` `{:E}` | `LowerExp` `UpperExp` | 整数和浮点数 |
| `{:p}` | `Pointer` | 引用和指针 |

`Debug` 可以自动生成。例子用教程 Debug 一节的 `Person`：一个有两个字段的结构体，`name` 是字符串，`age` 是 `u8`；取 `name` 为 `"Peter"`、`age` 为 27。类型名后面的 `<'a>` 是生命周期参数，第 09 课讲，这里可以略过。

```rust
#[derive(Debug)]
struct Person<'a> {
    name: &'a str,
    age: u8,
}
```

编译器为它展开出的实现是（本机 `-Zunpretty=expanded` 的输出）：

```rust
impl<'a> ::core::fmt::Debug for Person<'a> {
    fn fmt(&self, f: &mut ::core::fmt::Formatter) -> ::core::fmt::Result {
        ::core::fmt::Formatter::debug_struct_field2_finish(f, "Person",
            "name", &self.name, "age", &&self.age)
    }
}
```

它做的事很机械：写出类型名，再依次写出每个字段的名字和字段自己的 `Debug` 输出。

- `{:?}` 打印出 `Person { name: "Peter", age: 27 }`。
- `{:#?}` 是同样的内容分成多行、带缩进。
- 每个字段都必须有 `Debug`。把一个没有 `Debug` 的 `UnPrintable` 放进去再 derive，报错是 E0277 “`UnPrintable` doesn't implement `Debug`”，并指向那个字段。

同一个值在两种占位符下的差别，用字符串最容易看出来。本机输出：`println!("{} / {:?}", "Bob", "Bob")` 打印 `Bob / "Bob"`；把内容换成带制表符的 `"a\tb"`，`{}` 打出一个真的制表符，`{:?}` 打出 `"a\tb"`。`Debug` 把值写成它在源码里的样子，`Display` 写出它的内容。

**为什么这样设计。** 有三个问题。

*为什么 `Debug` 能自动生成，`Display` 不能？* `Debug` 的输出有一条不需要理解含义的规则：照着类型的定义，把名字和字段写出来。`Display` 是给用户看的，怎么写取决于含义。教程用 `Vec` 举例：一个路径列表也许该写成 `/:/etc:/home/username:/bin`，用冒号分隔；一个数字列表也许该写成 `1,2,3`，用逗号分隔。同一个 `Vec<T>` 没有对所有元素类型都合适的写法，所以标准库不替你决定。本机确认：`println!("{}", vec![1, 2, 3])` 报 E0277，`{:?}` 则打印 `[1, 2, 3]`。元组和 `Duration` 也一样只有 `Debug`，`Duration` 的 `{:?}` 输出是 `1.5s`。

*为什么分成两个 trait，而不是一个？* 因为读者不同，承诺也不同。标准库文档写明：`Display` 用于面向用户的输出，因此不能 derive；derive 出来的 `Debug` 格式不稳定，可能随 Rust 版本变化。`Display` 的输出算作类型对外行为的一部分，`Debug` 的输出只供调试，不该被程序解析。Python 的 `__str__` 和 `__repr__` 是同样的分工。

*一种占位符一个 trait，换来了什么？* 类型可以只声明自己支持的那几种写法，不支持的在编译期就被拦下。这就是前面说的“同一个值换一种写法是安全的”：`{:x}` 只对实现了 `LowerHex` 的类型开放。

**真实系统。** ATOMesh 的熔断器（`atom/mesh/src/core/circuit_breaker.rs`，提交 `43f5393`）正是这样用的：

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CircuitState { Closed, Open, HalfOpen }

impl std::fmt::Display for CircuitState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CircuitState::Closed => write!(f, "Closed"),
            CircuitState::Open => write!(f, "Open"),
            CircuitState::HalfOpen => write!(f, "HalfOpen"),
        }
    }
}
```

`Debug` 靠 derive，`Display` 手写，用在日志里：`info!("Circuit breaker state transition: {} -> {}", from, to)`。整个 `atom/mesh/src` 里有 132 处 derive 了 `Debug`，手写的 `Display` 只有 9 处，其中多数是状态枚举和错误类型。

**边界。**

- **derive 的 `Debug` 会打印所有字段。** 结构体里有密钥或令牌时，`{:?}` 进日志就是泄露。这时要手写 `Debug`，只列出想公开的字段。ATOMesh 的 `Router` 就是手写的，用 `f.debug_struct("Router").field(…)` 挑了 4 个字段。
- **不要依赖 `Debug` 输出的精确文本。** 它不稳定，不适合写进测试断言或协议。

## 节点 4：自己实现 `Display`

对应骨架第 6 步里被调用的那个 `fmt`。

**结论。** 实现 `Display` 就是写一个方法 `fmt`，在里面用 `write!` 把内容写进参数 `f`。`write!` 和 `println!` 用同一套格式串，只是目的地从标准输出换成了 `f`。

**机制。** 先看教程 Display 一节的 `MinMax`：一个包着两个 `i64` 的结构体，取值 `MinMax(0, 14)`，希望打印成 `(0, 14)`。

```rust
use std::fmt;

struct MinMax(i64, i64);

impl fmt::Display for MinMax {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.0, self.1)
    }
}
```

逐个部分看：

- **`impl fmt::Display for MinMax`**：为 `MinMax` 实现 `Display`。对应 C++ 里为这个类型写一个 `operator<<` 重载。
- **`&self`**：借用自己，只读。所以打印不会消耗这个值。
- **`f: &mut fmt::Formatter`**：输出的目的地，由调用方准备好递进来，`&mut` 表示要往里写。
- **返回 `fmt::Result`**：它是 `Result<(), fmt::Error>` 的别名。成功时没有值，失败时只表示“写不进去了”。
- **`write!(f, …)`**：标准库里它展开为 `f.write_fmt(format_args!(…))`，也就是六步流水线在这里又走了一遍。`self.0` 是 `i64`，于是 `i64` 的 `Display` 被调用。你的类型的 `Display` 是用字段的 `Display` 拼起来的。
- **最后一行没有分号**：这个表达式的值就是函数的返回值，不需要写 `return`。第 03 课细讲。

要分几次写时，用教程 Testcase: List 的例子：`List` 包着一个 `Vec<i32>`，取值 `List(vec![1, 2, 3])`，希望打印成 `[1, 2, 3]`。`for` 那一行的意思是逐个取出元素 `v` 和它的下标 `index`，第 04 课细讲。

```rust
impl fmt::Display for List {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let vec = &self.0;
        write!(f, "[")?;
        for (index, v) in vec.iter().enumerate() {
            if index != 0 { write!(f, ", ")?; }
            write!(f, "{}", v)?;
        }
        write!(f, "]")
    }
}
```

每个 `write!` 都返回一个 `Result`。末尾的 `?` 表示：如果是失败，立刻把它作为整个函数的返回值返回；否则继续往下。最后一个 `write!` 不加 `?`，它的结果直接作为返回值。

**为什么这样设计。** 也是三个问题。

*为什么是往 `f` 里写，而不是返回一个字符串？* 返回字符串意味着每一层都要分配一块内存再拼接：`List` 得先把每个 `i32` 变成字符串，再拼成一个更大的字符串。往同一个 `f` 里写，内容一路直通目的地，中间不产生临时字符串。同一个 `fmt` 也因此能同时服务 `println!`、`format!` 和写文件，它不需要知道目的地是什么。C++ 的 `operator<<(ostream&, const T&)` 是同一个形状；Python 的 `__str__` 则是每层返回一个新字符串。

*格式化本身不会失败，为什么要返回 `Result`？* 标准库文档的原话是：string formatting is an infallible operation，返回 `Result` 只是因为往底层的流里写可能失败，需要一条把错误传回去的路。所以规矩是只传递 `f` 报的错，不要自己制造错误。

*为什么要写出 `?`？* Rust 没有异常。错误是普通的返回值，要往上传就得写出来。`?` 把 C 里的 `if (ret < 0) return ret;` 压成了一个字符。第 12 课系统讲。

**真实系统。** 写完 `Display`，`to_string()` 是白送的。`library/alloc/src/string.rs` 里有一条对所有实现了 `Display` 的类型生效的实现：`impl<T: fmt::Display + ?Sized> ToString for T`。本机确认：`MinMax(0, 14).to_string()` 得到 7 个字节的 `(0, 14)`。

**边界。** 外层占位符上的宽度不会自动生效。本机输出：

```text
println!("[{:>10}]", 14);                  →  [        14]
println!("[{:>10}]", minmax);              →  [(0, 14)]
println!("[{:>10}]", minmax.to_string());  →  [   (0, 14)]
```

`{:>10}` 的意思是右对齐、占 10 个字符宽。宽度记在 `f` 里，而上面的 `fmt` 用 `write!` 另起了一个格式串，没有理会它。先转成 `String` 再打印就对齐了，因为 `String` 的 `Display` 会处理宽度。节点 5 讲格式说明时回到这一点。

**面试怎么讲**（约 60 秒）：

> Rust 用 trait 决定一个类型怎样打印，每种占位符对应一个 trait。`Debug` 面向开发者，输出照着类型定义来，所以可以 derive；`Display` 面向用户，写法取决于含义，必须手写，标准库也因此不给 `Vec` 实现 `Display`。实现 `Display` 就是写一个 `fmt`，用 `write!` 往传进来的 `Formatter` 里写，而不是返回字符串，这样嵌套的类型不会产生中间分配，同一个实现也能用于标准输出、字符串和文件。它返回 `Result` 只是为了传递底层写入的失败，用 `?` 逐层传出去。实际工程里要注意两点：derive 的 `Debug` 会打印所有字段，敏感信息要手写遮住；`Debug` 的格式不稳定，不能当协议用。

## 检查题

你在给一个推理路由器写日志。有这样一个结构体，没有任何 derive，也没有任何 `impl`：

```rust
struct Worker {
    id: u32,
    load: f32,
}
```

`w` 是它的一个值。

1. 下面四行各自能否通过编译？不能的话，最少要补什么，或者为什么补不了？

   ```rust
   println!("{}", w);
   println!("{:?}", w);
   println!("{:x}", w.id);
   println!("{:x}", w.load);
   ```

2. 运维希望在配置文件里写一行 `log_format = "{id}: {load}"` 来定制每行日志的样子，程序启动时把它读进来。为什么不能把读到的字符串直接交给 `println!`？这件事只能放到什么时候做？占位符写错了，比如写成 `{idd}`，会变成什么样的错误？

---

**009 · 用户** · `2026-10-07T23:14:14.474Z` · `msg-9a99fc184540ef850de2`

1. 第一和第二行无法通过编译，因为这个结构体没有实现Display和Debug的trait。但第三行可以通过，这是基本类型整数。第四行不行，因为load是浮点数，与x的整数格式不符。 2. 因为println!只能接受字面量的格式串，需要进行编译期的展开和解析。这件事只能放到代码里写成字面量或者改用运行时的模版引擎。占位符写错了，对于运行时的模版引擎，那么只有到运行时运行到这一行日志输出时才可能报错。

---

**010 · 助手** · `2026-10-07T23:18:58.997Z` · `msg-6e7cca7d2bf13c4cf1e7`

两问都对，只差一处没说。先补上，再讲最后一个节点，然后串讲和综合验收。

## 上一题的反馈

**第 1 问，四行的判断全对。** 缺的是“最少要补什么”，这正是节点 3 的核心区别：

- **第二行**只要在结构体上加一行 `#[derive(Debug)]`。两个字段 `u32` 和 `f32` 都有 `Debug`，编译器就能生成。
- **第一行**不能 derive，必须手写 `impl fmt::Display for Worker`。
- **第四行**更准确的说法是：`{:x}` 需要 `LowerHex`，标准库只为整数实现了它。`f32` 和 `LowerHex` 都属于标准库，你也不能替它补上，这条规则第 10 课讲。想看浮点数的位模式，先转成整数：本机 `println!("{:x}", 1.5f32.to_bits())` 输出 `3fc00000`。

**第 2 问，对，上次的差距补上了。** 一点延伸：“运行到那一行才报错”是用到时才解析的情况。更稳妥的做法是在程序启动、读入配置的那一刻就把模板解析一遍，并用一条样例记录试着渲染一次。错误仍然在运行期，但被你提前到了启动时。

## 节点 5：格式说明

对应骨架的第 3 步，以及它在第 6 步的落点。

**结论。** 占位符里冒号后面是一小段格式说明。编译器在第 3 步解析它，把结果写进模板；运行期它经由 `f` 交到每个类型的 `fmt` 手里，由 `fmt` 来执行。宽度、精度这些事不是 `println!` 做的，是各个类型自己的 `fmt` 做的。

**机制。** 一个占位符的完整形状是 `{谁:怎样}`。

“谁”有三种写法：省略表示按顺序取下一个参数；数字如 `{0}` 表示第几个参数；名字如 `{who}` 表示一个命名参数，或者作用域里的同名变量。

“怎样”的语法在标准库文档里是一行：

```text
format_spec := [[fill]align][sign]['#']['0'][width]['.' precision][type]
```

下面的例子用同一组值：`pi = 3.141592`，`id = 7`（`u32`），`load = 0.4567`（`f32`），`width = 6`。输出都是本机实际打印的，方括号是我加在格式串里用来显示边界的。

| 写法 | 含义 | 输出 |
| --- | --- | --- |
| `{:.3}` | 小数点后 3 位 | `[3.142]` |
| `{:8.3}` | 总宽 8，数字默认右对齐 | `[   3.142]` |
| `{:<8.3}`、`{:^8.3}` | 左对齐、居中 | `[3.142   ]`、`[ 3.142  ]` |
| `{:*^8.3}` | 居中，用 `*` 填充 | `[*3.142**]` |
| `{:08.3}` | 用 0 补到宽 8 | `[0003.142]` |
| `{:+}` | 总是写出符号 | `[+5]`、`[-5]` |
| `{:#x}`、`{:#010b}` | `#` 表示加上进制前缀 | `[0xff]`、`[0b00000101]` |
| `{0}-{0}-{1}` | 按位置引用，可以重复 | `[a-a-b]` |
| `{who}: {load:.1}`，另给 `who = "w7"` | `who` 是命名参数，`load` 直接取变量 | `[w7: 0.5]` |
| `{id:>width$}` | 宽度取自变量 `width` | `[     7]` |

字符串默认左对齐：`{:5}` 打印 `"ab"` 得到 `[ab   ]`。

名字是在编译期解析的。`println!("{name}")` 而作用域里没有 `name` 时，报错是 E0425 “cannot find value `name` in this scope”。这也再次说明配置文件里的 `{id}` 为什么不能交给 `println!`。

格式说明由类型的 `fmt` 执行，下面这个对比能看出来。例子是一个只有两个取值的状态枚举 `State`，取值 `Closed` 和 `HalfOpen`。给它写两种 `Display`：`Plain` 用 `write!(f, "{}", name)`，`Padded` 用 `f.pad(name)`，其中 `name` 是状态名的字符串。然后都用 `{:>10}` 打印 `Closed`：

```text
Plain    →  [Closed]
Padded   →  [    Closed]
```

`f.pad(s)` 的意思是：把这段文字按 `f` 里记着的宽度、对齐和填充写出去。`Plain` 没有理会 `f` 里的要求，这就是节点 4 末尾那个现象的原因。

**为什么这样设计。**

*为什么交给类型自己执行，而不是由 `println!` 统一补空格？* 有两个原因。第一，同一个说明对不同类型含义不同，只有类型自己知道该怎么做：`{:05}` 打印 `-7` 得到 `-0007`，0 要补在符号后面；`{:.2}` 对浮点数是保留两位小数，对字符串 `"abcdef"` 则是截成 `ab`。第二，统一补空格需要先拿到这个参数的完整输出才知道长度，那就得先把它存进一个临时字符串，和“直接往目的地写”的设计冲突。

*为什么宽度可以取自变量，格式串却不行？* 因为 `{id:>width$}` 的形状是固定的：一个占位符，带一个宽度。变的只是一个数。编译器仍然知道有几个占位符、各自用哪个 trait。形状必须在编译期确定，数值可以留到运行期。

**边界。** 标准库的类型都会执行这些说明。你自己写的 `Display` 默认不会，需要对齐时要么在 `fmt` 里用 `f.pad`，要么让调用方先 `to_string()`。

## 串讲

沿着贯穿例子把五个节点连起来。在那一行上加两样东西：给 `days` 加上 `{:>5}`，再多打印一个手写了 `Display` 的 `MinMax(0, 14)`。

```rust
println!("{:>5} days, {:?}, {}", days, Structure(3), MinMax(0, 14));
// 输出：   31 days, Structure(3), (0, 14)
```

**编译期。**

1. **宏展开。** `println!` 换成 `_print(format_args!(…))`。`#[derive(Debug)]` 换成一段 `impl Debug for Structure`。`MinMax` 的 `fmt` 里那个 `write!` 也被展开，它是另一次 `format_args!`。
2. **解析格式串。** 切出三个占位符和三段字面文字，核对三个占位符对上三个参数。第一个占位符的说明 `>5` 被解析成“右对齐，宽 5”。
3. **选 trait、查类型。** 三个参数分别交给 `new_display`、`new_debug`、`new_display`。`i32` 有标准库的 `Display`，`Structure` 有 derive 的 `Debug`，`MinMax` 有你手写的 `Display`，三个约束都成立。
4. **生成模板。** 本机实际得到的是：

   ```text
   b"\xc3 \x00\x00(\x05\x00\x07 days, \xc0\x02, \xc0\x01\n\x00"
   ```

   第一个占位符不再是单独一个 `\xc0`，而是 `\xc3` 加 6 个字节：4 个字节记着填充字符是空格、对齐是右对齐，2 个字节记着宽度 5。后两个占位符没有说明，仍是 `\xc0`。`MinMax` 的 `fmt` 里另有一段小模板 `b"\x01(\xc0\x02, \xc0\x01)\x00"`。

**运行期。** `_print` 锁住标准输出，顺着外层模板走：

- 第一个占位符：调用 `i32` 的 `Display::fmt`，此时 `f` 里带着“右对齐、宽 5”，它写出三个空格加 `31`。
- 字面文字 ` days, ` 直接写出。
- 第二个占位符：调用 derive 出来的 `Debug::fmt`，写出 `Structure(3)`。
- 第三个占位符：调用你写的 `MinMax::fmt`。它用自己的小模板再走一轮，两次调用 `i64` 的 `Display::fmt`，写出 `(0, 14)`。
- 最后写出换行。任何一次写入失败，错误沿着 `?` 一路传回 `_print`，在那里变成 panic。

**节点之间的关系。** 宏让编译器能读到格式串（节点 2）；trait 让类型决定自己支持哪些占位符（节点 3）；你写的 `fmt` 是运行期真正干活的地方，它往 `f` 里写而不是返回字符串（节点 4）；格式说明在编译期被解析，在运行期由 `fmt` 执行（节点 5）。

**放到真实系统里。** ATOMesh 的熔断器打日志用的是 `info!("Circuit breaker state transition: {} -> {}", from, to)`，格式串的写法和这里完全一样，`from` 和 `to` 的类型是手写了 `Display` 的 `CircuitState`。整个 `atom/mesh/src` 有 132 处 derive `Debug`、9 处手写 `Display`。日常写 Rust 时的分工就是这样：几乎每个类型都顺手 derive 一个 `Debug`，只有要给人看的少数类型才手写 `Display`。

## 综合验收

三道题，用自己的话回答，第 1 题当作口述写下来即可。

**第 1 题（口述，60 到 90 秒）。** 向面试官讲清 Rust 的格式化输出是怎样设计的：一行 `println!` 在编译期和运行期各做什么；一个类型怎样接入；和 C 的 `printf` 相比换来了什么、付出了什么；实际使用时有哪些要小心的地方。

**第 2 题（预测与最小修法）。** 有下面两个类型，`pool` 是一个 `Pool` 的值：

```rust
#[derive(Debug)]
struct Shard { id: u32 }

struct Pool { name: String, shards: Vec<Shard> }
```

下面三行各自能否通过编译？不能的话，最小的修法是什么？

```rust
println!("{:?}", pool.shards);
println!("{}", pool.shards);
println!("{:?}", pool);
```

另外，要让 `println!("{}", pool)` 能用，最少要做什么？能不能用 derive？

**第 3 题（取舍）。** 同事给 `Worker`（字段 `id: u32`、`load: f32`）写了这样的 `Display`，功能正确，`id` 为 7、`load` 为 0.4567 时打印 `w7: 0.5`：

```rust
impl fmt::Display for Worker {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let s = format!("w{}: {:.1}", self.id, self.load);
        write!(f, "{}", s)
    }
}
```

1. 对照这一课的模型，它比必要的多付出了什么？改成不产生中间字符串的写法，只写 `fmt` 的函数体就行。
2. 现在日志要求把每个 worker 右对齐到 12 个字符宽：`println!("[{:>12}]", w)`。同事的原版和你改好的版本，哪个能对齐？都不能的话，最小的改动是什么？
3. 由此说明：什么情况下先拼成一个字符串反而是合理的？

---

**011 · 用户** · `2026-10-08T01:26:18.910Z` · `msg-a92c977bf7b5176ee8c5`

<pasted_content id="8858">
1. rust中的println!是一个宏。在编译期会展开宏、解析格式串，匹配参数类型和对应的trait输出方式，最后生成输出模版。在运行时，就锁定标准输出，根据模版进行输出，遇到占位符就根据对应参数和其类型调用fmt进行输出。对于一个新的自定义类型，需要实现他的Display trait、Debug trait或者derive出Debug trait来定义其输出格式。和C的printf相比，宏的方式换来了更严格的编译期检查。可以在编译期检查格式串和参数类型的合法性，从而避免运行时的报错和隐式的异常输出。但这使得格式串必须是字面量，无法在运行时动态设置，付出了格式串的灵活性。实际使用时要小心Debug输出时的变量打印，会打印出所有的变量。
2. 第一行可以通过编译，第二三行不行。第二行是因为Vec<Shard>类型没有实现Display trait。第三行是因为结构体Pool没有实现Debug trait，也没有derive Debug。最小的修法就是为Vec<Shard>实现Display trait和derive struct Pool Debug trait。要让println!("{}", pool) 能用，最少要实现Display trait。不能derive ，Display用于面向用户的输出，不能derive。
3. 相比必要的多创建了一个中间变量字符串以存放格式化输出。可以改成write!(f, “w{}: {:.1}”, self.id, self.load)。当需要右对齐时，同事写的这个版本由于先转成了字符串，而字符串可以对齐。但我改后的版本不行。最小的改动是使用f.pad，改成write!(f, f.pad(“w{}: {:.1}”), self.id, self.load)。所以在需要支持更多格式化的情况下，先转成字符串是更合理的。
</pasted_content id="8858">

---

**012 · 助手** · `2026-10-08T01:28:43.435Z` · `msg-95e700ecfc2e9485eb29`

综合验收大部分过了，有三处差距。先逐题说，再用三道小题复查。

## 第 1 题：口述

主线完整：编译期的展开、解析、选 trait、生成模板，运行期的加锁和按模板调用 `fmt`，类型怎样接入，都讲到了。取舍里说出了“格式串必须是字面量”，上次差的那一点补上了。

不足在“要小心的地方”只讲了一条。节点 2 的边界里还有两条和运行期有关，这里先不重复，下面复查的第 3 题会问到。

## 第 2 题：预测与最小修法

三行的判断全对，“`Display` 不能 derive”也说对了，上次没说出的区别补上了。

差距在第二行的修法。你提出为 `Vec<Shard>` 实现 `Display`，编译器不允许。本机的报错是：

```text
error[E0117]: only traits defined in the current crate can be implemented
              for types defined outside of the crate
  = note: define and implement a trait or new type instead
```

规则是：实现一个 trait 时，trait 和类型里至少有一个必须是你自己的 crate 定义的。`Display` 和 `Vec` 都属于标准库，所以不行，哪怕里面装的 `Shard` 是你的。上次说 `f32` 不能补 `LowerHex` 是同一条规则。

为什么要有这条规则：没有它，两个互不知情的库可以各写一份 `Display for Vec<…>`，编译器无法决定用哪一份；标准库以后想补一份通用的实现，也会和你的冲突。第 10 课系统讲。

可行的路有两条：

- **改用 `{:?}`。** `Vec<Shard>` 已经有 `Debug`。
- **包一层自己的类型。** 为 `Pool` 实现 `Display`，在 `fmt` 里逐个写出 shard。教程的 `List(Vec<i32>)` 之所以要把 `Vec` 包进一个新结构体，原因就在这里。

## 第 3 题：取舍

第 1 小问对。更准确地说，`format!` 每次调用都在堆上分配一个 `String`，内容还要再拷贝一遍。你给的 `write!(f, "w{}: {:.1}", self.id, self.load)` 是正确的写法。

第 2 小问有差距。同事的原版也不能对齐。本机两个版本的输出一样：

```text
同事的原版     →  [w7: 0.5]
你改好的版本   →  [w7: 0.5]
```

原因在于宽度 12 记在 `f` 里。同事最后一行是 `write!(f, "{}", s)`，这里的 `{}` 是一个新写的、不带宽度的占位符，没有人去看 `f` 里的那个 12。节点 4 里“先 `to_string()` 再打印就对齐了”是另一回事：那次是调用方拿着 `String` 去配 `{:>10}`，`String` 自己的 `fmt` 收到了带宽度的 `f`。关键是谁手里拿着那个宽度。

你给的 `write!(f, f.pad("w{}: {:.1}"), self.id, self.load)` 过不了编译，报错正是节点 2 的那一条：`format argument must be a string literal`。另外 `f.pad` 不是套在格式串外面的东西，它接收一段已经写好的文字，按 `f` 里的要求把它写出去。

最小的改动是保留同事的 `format!`，只换最后一行：

```rust
let s = format!("w{}: {:.1}", self.id, self.load);
f.pad(&s)          // 输出 [     w7: 0.5]
```

第 3 小问因此可以说得更准：**要把整段输出当作一个整体来对齐时**，先拼出来是合理的。补多少空格取决于总长度，而总长度要等全部内容写完才知道，所以必须先放在某个地方。

标准库自己就是这样做的。`Ipv4Addr` 的 `Display`（`library/core/src/net/ip_addr.rs`）先看 `fmt.width()` 和 `fmt.precision()`：都没有就直接 `write!`；有的话，先写进一个 15 字节的栈上缓冲区，再 `fmt.pad`。15 是最长地址 `255.255.255.255` 的长度。最大长度已知，所以它连堆分配都省了。

## 复查

三道小题，每题一两句话即可。

**第 1 题。** 有一个类型 `struct Id(u32);`，下面是它的 `Display` 里 `fmt` 函数体的四种写法。用 `println!("[{:>10}]", Id(7))` 打印，四种写法各输出什么？为什么？B 那一行的意思是：直接调用 `u32` 的 `Display::fmt`，并把同一个 `f` 传给它。

```rust
// A
write!(f, "{}", self.0)
// B
fmt::Display::fmt(&self.0, f)
// C
write!(f, "{:>6}", self.0)
// D
f.pad(&self.0.to_string())
```

如果有两种写法输出相同，其中一种比另一种省了什么？

**第 2 题。** 沿用前面的 `Pool`、`Shard` 和 `Worker`，它们都是你自己的 crate 定义的。下面三个实现，编译器各自接受吗？依据是什么？

```rust
impl fmt::Display for Pool { … }
impl fmt::Display for (u32, u32) { … }
impl fmt::LowerHex for Worker { … }
```

**第 3 题。** 一个导出工具在循环里用 `println!` 输出 100 万行，使用者把它接到 `head -n 20` 上只看前 20 行。这个工具会遇到哪两个问题？分别怎么改？

---

**013 · 用户** · `2026-10-08T01:56:05.328Z` · `msg-99a61767174da5eb5fb8`

<pasted_content id="8858">
第1题
A输出了7，因为忽略了对齐格式。
B输出了右对齐10位的数字7，因为直接调用u32的Display format，也将对齐格式传到了u32的Display中。
C输出了右对齐6位的数字7，因为格式串里写死了>6。
D通过转成string再pad的方式来输出，也可以输出右对齐10位的数字7.
其中B和D写法输出相同，但B相比于D少了一个临时中间的字符串，少了中间再拷贝一次的开销。
第2题
第一和三行可以接受，第二行不能接受。
第一行是为自定义的类型实现Display。
第二行是为基本类型u32进行实现Display。
第三行是为自定义的类型实现LowerHex。
第3题
不知道。我猜测可能会出现输出pipe提前结束的问题。因为head -n 20只看完前20行就可以结束了。不知道该怎么改。
</pasted_content id="8858">

---

**014 · 助手** · `2026-10-08T01:57:17.808Z` · `msg-e3165ba1314965bfde0d`

前两题过了，第 3 题说“不知道”是有用的信息：这部分上次我是在节点 2 末尾用三条要点带过的，讲得太密，这次慢一点重讲。

## 第 1、2 题

**第 1 题全对。** 四种写法的输出和理由都正确，“B 比 D 少一个临时字符串”也对。宽度怎样经过 `f` 传递这一点可以关闭了。

**第 2 题判断全对，理由有一处要改。** 第二行的类型不是 `u32`，而是元组 `(u32, u32)`。元组不是任何 crate 自己定义的类型，`Display` 也不是你的，两边都不是自己的，所以被拒绝。第三行能过，是因为类型 `Worker` 是你的，哪怕 `LowerHex` 属于标准库。

## 重讲：`println!` 在运行期的两条边界

这两条不用背，都能从骨架第 6 步的源码里读出来。`println!` 最终调用的是标准库里的这个函数（`library/std/src/io/stdio.rs`，1.97.1）：

```rust
fn print_to<T>(args: fmt::Arguments<'_>, global_s: fn() -> T, label: &str)
where
    T: Write,
{
    if let Err(e) = global_s().write_fmt(args) {
        panic!("failed printing to {label}: {e}");
    }
}
```

中间省略了一段只在测试时生效的代码。剩下的只有一句话：取得标准输出，把内容写进去，写失败就 panic。两条边界分别藏在这句话的前半和后半。

**第一条：写失败就 panic。** `write_fmt` 返回的是 `Result`，但 `println!` 没有把它交给你，而是自己处理了，处理方式是 `panic!`。所以用 `println!` 的程序没有机会对“写不进去”作出反应。

你猜到了管道会提前关闭，这正是最常见的触发方式。完整的过程是这样的：

1. `head -n 20` 读够 20 行就退出，管道的读端关闭。
2. 你的工具还在循环里，下一次往管道里写，操作系统返回错误 `Broken pipe`。
3. `write_fmt` 把它作为 `Err` 返回，`print_to` 执行 `panic!`。

我把循环打印的程序接到 `head -n 2` 上实际跑了一遍：

```text
$ ./many | head -n 2
line 0
line 1

thread 'main' panicked at library/std/src/io/stdio.rs:1166:9:
failed printing to stdout: Broken pipe (os error 32)
```

使用者只想看前两行，却看到了一段崩溃信息。

**第二条：每次调用都加锁，而且每行写一次。** 这一条在 `global_s()` 里。标准输出在整个进程里只有一个，定义是：

```rust
static STDOUT: OnceLock<ReentrantLock<RefCell<LineWriter<StdoutRaw>>>> = OnceLock::new();
```

这一长串类型里只需要看两个词：

- **`ReentrantLock`**：一把锁。每次 `println!` 都要先拿到它，写完再放开。输出 100 万行就是加锁、解锁各 100 万次。
- **`LineWriter`**：按行缓冲。每遇到一个换行就把这一行真正交给操作系统，也就是每行一次系统调用。

**怎么改。** 两个问题用同一个办法解决：自己先把锁拿住，用 `writeln!` 往里写。`writeln!` 会把 `Result` 交还给你。

```rust
use std::io::{self, Write};

fn main() {
    let mut out = io::stdout().lock();          // 只加一次锁
    for i in 0..1_000_000 {
        if writeln!(out, "line {i}").is_err() { // 写失败时自己决定怎么办
            break;                              // 这里选择安静地结束
        }
    }
}
```

本机实际运行：`./many_fixed | head -n 2` 打印两行后正常结束，没有崩溃信息，退出码是 0。

对照一下两种写法：

| | `println!` | 锁住句柄后用 `writeln!` |
| --- | --- | --- |
| 加锁 | 每行一次 | 整个循环一次 |
| 写失败 | 库替你 panic | 得到一个 `Result`，由你决定 |

这段改法只解决了加锁和 panic。每行一次系统调用还在，因为锁住的句柄仍然按行缓冲；要减少它，得再包一层更大的缓冲区，这是第 13、15 课的内容。

## 复查

换一个场景。你写的推理路由器同时处理很多请求，每个请求由一个线程处理。每处理完一个请求，线程就用 `println!` 打印一行访问日志。运维把路由器的标准输出重定向到了磁盘上的一个日志文件。

1. 请求量很大、64 个线程同时在跑时，这一行 `println!` 会带来什么问题？对照上面的 `STDOUT` 定义来说。
2. 某天日志所在的磁盘写满了。接下来第一个要打印日志的线程会发生什么？为什么？

---

**015 · 用户** · `2026-10-08T02:10:30.032Z` · `msg-702c8dc4765a5f943253`

1. STDOUT使得println!需要加锁并按行缓冲输出。当请求量很大，有很多现场同时跑的情况下，这一行println!很可能加大打印输出的开销。如果有一个线程一行迟迟没写完，不放开锁，可能会导致其他线程也输出不了而卡死。
2. 如果磁盘写满了，无法再继续写入日志。那么就会引发接下来要打印日志的线程写失败，println!会触发panic报错崩溃。

---

**016 · 助手** · `2026-10-08T02:13:09.321Z` · `msg-cfb15cd060a250cfeaa6`

两问都对，运行期边界这一处可以关闭了。综合验收到此通过，下面是练习约定，请你看完决定是否接受。

## 复查的反馈

**第 1 问，对。** 补一个用词：其他线程是在等那把锁，等前一个线程写完就能继续，属于阻塞，不是死锁。后果是 64 个线程处理请求本来互不相干，到了这一行却要排成一队，日志写得多慢，请求就被拖多慢。

**第 2 问，对。** 我用一个永远写不进去的设备 `/dev/full` 模拟了磁盘写满，实际输出是：

```text
thread 'main' panicked at library/std/src/io/stdio.rs:1166:9:
failed printing to stdout: No space left on device (os error 28)
```

panic 之后会怎样，取决于它发生在哪个线程：发生在主线程，整个进程以退出码 101 结束；发生在别的线程，默认只有那个线程终止，它正在处理的请求就丢了。这部分第 12、14 课细讲。

## 练习约定 P1（版本 1）

**为什么做。** 目标 O3 是“为自定义类型实现 `Display`，并用格式说明得到指定的输出”，它需要实践证据。到现在为止你讲清了、也预测对了，但还没有亲手写出能通过验收的代码。

**你交付什么。** 在 `rust/lesson01_hello_formatting/src/lib.rs` 里完成五件事。前三件是教程里的 Activity，后两件针对这一课暴露过的差距。

1. **`Complex`**（字段 `real: f64`、`imag: f64`）：derive `Debug`；手写 `Display`，实部 3.3、虚部 7.2 时输出 `3.3 +7.2i`，虚部为 -2.3 时输出 `4.7 -2.3i`。
2. **`List`**（包着一个 `Vec<i32>`）：手写 `Display`，带上每个元素的下标，`[1, 2, 3]` 输出 `[0: 1, 1: 2, 2: 3]`，空列表输出 `[]`。
3. **`Color`**（字段 `red`、`green`、`blue`，都是 `u8`）：手写 `Display`，128、255、90 输出 `RGB (128, 255, 90) 0x80FF5A`。
4. **`WorkerId`**（包着一个 `u32`）：手写 `Display`，7 输出 `w7`，并且调用方给的宽度、对齐和填充字符都要生效，例如 `{:>6}` 输出 `    w7`。
5. **函数 `status_line(name: &str, load: f32, width: usize) -> String`**：`name` 左对齐到 `width` 个字符宽，接一个 `|`，`load` 右对齐到 6 个字符宽并保留两位小数，再接一个 `|`。`status_line("w7", 0.4567, 6)` 返回 `w7    |  0.46|`。

**怎样算通过。**

| 编号 | 标准 | 检查方式 |
| --- | --- | --- |
| A1 | `Complex` 的 `Display` 与 `Debug` 输出正确 | 测试 |
| A2 | `List` 的输出正确，包括单个元素和空列表 | 测试 |
| A3 | `Color` 的输出正确，包括需要补 0 的分量 | 测试 |
| A4 | `WorkerId` 不带说明时输出 `w7`，带 `>`、`<`、`^` 和填充字符时都按要求对齐 | 测试 |
| A5 | `status_line` 的输出正确，包括名字比 `width` 长时不截断 | 测试 |
| A6 | 这个 crate 通过 `cargo fmt --check` 和 `cargo clippy -- -D warnings`。仓库规则是不用 `unwrap`、`expect` 和 `unsafe` | 命令 |
| A7 | 说明 A4 你选了哪种写法、它有没有堆分配、为什么只用 `write!` 不行 | 你的说明 |
| A8 | A1–A7 通过后，我给一个新的小类型，你在没有提示的情况下实现并通过测试 | 测试 |

**文件边界。**

| 边界 | 路径 |
| --- | --- |
| 你写 | `rust/lesson01_hello_formatting/src/lib.rs`。我先放入只含四个类型定义的骨架，之后归你 |
| 我维护 | `rust/lesson01_hello_formatting/Cargo.toml`；`rust/lesson01_hello_formatting/tests/` 下的验收测试，每个验收项一个文件；根 `Cargo.toml` 的 workspace members（加入 `"rust/*"`）与 `Cargo.lock`；本课记录与 Checkpoint |
| 我只读 | `docs/rust-by-example/src/hello/` |
| 本次不动 | 其他 crate、CI 配置和依赖 |

**运行方式。** 一次跑一个验收项，例如第一个：

```bash
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson01-hello-formatting --test a1_complex
```

去掉 `--test a1_complex` 就是全部。开始时的失败会是编译错误，比如“`Complex` doesn't implement `Display`”，这是预期的起点。

**一个副作用。** 在你完成之前，整个 workspace 的 `host-cpu.sh test` 和 `host-cpu.sh lint` 会在这个 crate 上失败，远端的 CI 也会。所以练习期间这些改动留在本地，通过之后再提交。

**求助怎样影响证据。** 随时可以问。如果我透露了某一项的关键写法，只影响那一项，之后用一个小变式在无提示下补回来。A8 期间不给提示。

**不在范围内。** 第三方依赖、性能、教程 Activity 里的加分项（符号后面加空格）都不做。

**完成门槛。** A1–A8 全部通过，阻塞问题全部关闭。

接受的话回一句即可，我再建 crate 和测试，并确认初始状态是预期的失败。

---

**017 · 用户** · `2026-10-08T02:15:08.273Z` · `msg-3ee9acc2f095320f3395`

接受

---

**018 · 助手** · `2026-10-08T02:16:47.820Z` · `msg-d8a0fd5278856cdb2653`

练习已经就位，初始状态是预期的失败，可以开始写了。

## 你要写的文件

`rust/lesson01_hello_formatting/src/lib.rs`。里面现在只有四个类型的定义，其余都由你来写：四个 `Display` 实现、`Complex` 的 `Debug`，以及函数 `status_line`。

## 验收测试

在 `rust/lesson01_hello_formatting/tests/` 下，每个验收项一个文件，共 14 个测试：

| 文件 | 检查什么 |
| --- | --- |
| `a1_complex.rs` | `3.3 +7.2i`、`4.7 -2.3i`，以及 `Debug` 输出 `Complex { real: 3.3, imag: 7.2 }` |
| `a2_list.rs` | `[0: 1, 1: 2, 2: 3]`、单个元素 `[0: -5]`、空列表 `[]` |
| `a3_color.rs` | `RGB (128, 255, 90) 0x80FF5A`，以及要补 0 的 `0x0003FE` 和 `0x000000` |
| `a4_worker_id.rs` | `w7`；`{:>6}`、`{:<6}`、`{:^6}` 的对齐；`{:*^6}` 的填充；宽度不够时不截断 |
| `a5_status_line.rs` | `w7    \|  0.46\|`；名字比宽度长时不截断；load 为 0 时仍是两位小数 |

## 怎么跑

一次一个验收项：

```bash
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson01-hello-formatting --test a1_complex
```

全部通过后再跑 A6 的两条命令：

```bash
bash scripts/host-cpu.sh run -- cargo fmt -p rust-lesson01-hello-formatting --check
bash scripts/host-cpu.sh run -- cargo clippy -p rust-lesson01-hello-formatting --all-targets --locked -- -D warnings
```

`cargo fmt` 去掉 `--check` 就是直接帮你排好版。clippy 报出的每一条都带修改建议，照着改即可。

## 现在的状态

五个测试文件目前都编译不过，原因正是要你补的东西：

```text
a1_complex       `Complex` doesn't implement `std::fmt::Display`
a2_list          `List` doesn't implement `std::fmt::Display`
a3_color         `Color` doesn't implement `std::fmt::Display`
a4_worker_id     `WorkerId` doesn't implement `std::fmt::Display`
a5_status_line   unresolved import `…::status_line`
```

测试本身我核对过：一份不入库的参考实现能通过全部 14 项；8 种故意写错的写法，比如不带符号、十六进制不补 0、忽略宽度，都被对应的文件判为失败。

写完后把测试和 A6 两条命令的输出贴给我，或者直接说一声，我来跑。卡住了随时问。这些改动（crate、根 `Cargo.toml` 和 `Cargo.lock`、课程记录）目前都没有提交。

---

**019 · 用户** · `2026-10-08T02:48:19.432Z` · `msg-5a3dc99e6b146c3acc13`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/rust/lesson01_hello_formatting/src/lib.rs in the IDE. This may or may not be related to the current task.</ide_opened_file>
练习中有用到几个点，我还没有学到，需要先了解一下：判断分支、获取Vec的长度、循环遍历Vec的方式、从RGB的三个数字如何得到类似于0x80FF5A的表示。

---

**020 · 助手** · `2026-10-08T02:49:10.133Z` · `msg-219f330c5ff60b977968`

前三个是第 02 到 04 课的语法，练习提前用到了，这是我设计练习时该先交代的，下面给够用的最小版本。第四个是 A3 要你自己完成的核心，我只讲清这个表示是什么、该回头翻哪里，具体的格式串留给你。

下面的输出都是本机实际运行的结果。例子用一个和练习无关的类型：`Scores` 包着一个 `Vec<u32>`，取值 `[90, 75, 60]`。

## 判断分支

```rust
if i == 0 {
    print!("first={s}");
} else {
    print!(" then={s}");
}
```

和 C++ 有三处不同：

- **条件不用加括号，花括号不能省。** 哪怕只有一条语句。
- **条件必须是 `bool`。** 整数不会自动当成真假，`if n { … }` 在 `n` 是整数时报 E0308 “expected `bool`, found integer”。要写成 `if n != 0`。
- **`if` 是表达式，可以有值。** 相当于 C++ 的三目运算符：

  ```rust
  let label = if x >= 0.0 { "non-negative" } else { "negative" };
  // x 为 -2.5 时，label 是 "negative"
  ```

  这种写法里两个分支末尾都没有分号，分支的值就是整个 `if` 的值。

比较运算符 `==`、`!=`、`<`、`>=` 和 C++ 一样。

## 取 Vec 的长度

```rust
self.0.len()        // 元素个数，类型是 usize；上例为 3
self.0.is_empty()   // 是否为空；上例为 false
```

`usize` 是和指针一样宽的无符号整数，相当于 C++ 的 `size_t`。下标和长度都用它。`self.0` 是取元组结构体的第一个字段，这个你在 `MinMax` 里见过。

## 遍历 Vec

最常用的两种写法：

```rust
// 只要元素
for s in &self.0 {
    print!("{s} ");
}
// 输出：90 75 60

// 同时要下标和元素
for (i, s) in self.0.iter().enumerate() {
    …
}
// i 依次是 0、1、2，s 依次是 90、75、60
```

`.iter()` 的意思是逐个借出元素，`.enumerate()` 给每个元素配上从 0 开始的序号，`(i, s)` 把这一对拆成两个名字。

有一个现在就会碰到的坑：**`&` 不能省。** 在 `fmt(&self, …)` 里，`self` 是借来的，你无权把里面的 `Vec` 拿走。写成 `for x in self.0` 会被拒绝：

```text
error[E0507]: cannot move out of `self` which is behind a shared reference
```

够用的最小模型是：`for x in v` 会把 `v` 整个交出去，`for x in &v` 和 `for x in v.iter()` 只是借着看。为什么这样设计放在第 04 课和第 08 课。

## `0x80FF5A` 是什么

它不是把三个数做了什么运算，只是换了一种写法再连在一起。

一个 `u8` 的取值范围是 0 到 255，正好能用两位十六进制数写出来。把三个分量各写成两位，依次排开：

| 分量 | 十进制 | 十六进制 |
| --- | --- | --- |
| red | 128 | `80` |
| green | 255 | `FF` |
| blue | 90 | `5A` |

拼起来是 `80FF5A`，前面的 `0x` 只是照惯例写上的两个字符。所以这个输出是“同一个分量打印两次”：前半段 `RGB (128, 255, 90)` 用十进制，后半段用十六进制。

本机的两个观察，供你自己组合：

```text
println!("{:x} {:X} {:#X}", 128, 255, 90);   →  80 FF 0x5A
println!("{:X} vs {:02X}", 3, 3);            →  3 vs 03
```

第二行说明了测试里 `0x0003FE` 那个例子为什么存在：分量小于 16 时只有一位十六进制数，不处理就会少一位。节点 5 那张格式说明的表里有你需要的全部零件。教程在 `docs/rust-by-example/src/hello/print/fmt.md` 的末尾也给了两条提示，实在卡住再看。

这次讲的都是通用语法和概念，没有涉及任何一项的具体写法，不影响验收的独立性。

---

**021 · 用户** · `2026-10-08T03:31:10.080Z` · `msg-a4f394f729496f7db9bf`

好了，我完成了练习，并通过了测试，也按照cargo fmt和clippy的建议修改了格式。请review。

---

**022 · 助手** · `2026-10-08T03:33:19.043Z` · `msg-5d312a839a5371148e84`

按版本 1 的标准，A1 到 A6 都通过了，但 Review 发现一个测试没测到的问题，需要你决定是否把它补进约定。

## 复验结果

我自己重跑了一遍：

- 验收测试没有被改动，14 项全部通过。
- `cargo fmt --check` 和 `cargo clippy -- -D warnings` 都通过，代码里没有 `unwrap`、`expect`、`unsafe`。

写得好的地方：`WorkerId` 用的是“先拼出来再 `f.pad`”，正是综合验收里那条结论；你还把它用到了 `Complex` 上，所以 `{:>12}` 对 `Complex` 也能对齐。`status_line` 直接用了变量捕获和 `width$`。

## 一个阻塞问题：`List` 把写入错误丢掉了

`List` 的 `fmt` 里是这样写的：

```rust
let _ = write!(f, "[");
…
let _ = write!(f, "{i}: {s}");
```

`let _ =` 的意思是“我知道这里有个结果，故意不要”。编译器看到没人用的 `Result` 会给警告，并且提示可以这样消掉它，我猜你是照着提示改的。但这里的结果不能不要：这一课的目标 O3 写的就是“逐个写出元素时用 `?` 传播错误”，节点 4 也讲过，`fmt` 的规矩是把 `f` 报的错传出去。

测试之所以没发现，是因为往字符串里写永远不会失败。我做了一个第 3 次写入会失败的假输出，用它打印 `List(vec![1, 2, 3])`：

| | 返回值 | 之后还写了几次 | 留下的内容 |
| --- | --- | --- | --- |
| 你的实现 | `Ok(())` | 一直写完，共 12 次 | `[0, 1: 2, 2: 3]` |
| 用 `?` 的实现 | `Err` | 立刻停止，共 3 次 | `[0` |

你的实现在中间丢了一段内容，却告诉调用方“成功了”。放到真实场景里，就是日志文件写坏了而程序毫不知情。

这是我写约定时的疏漏：版本 1 的 A2 只检查了输出的文字，没有检查出错时的行为。所以它不算你的失误，但它确实是 O3 要求的能力。

## 约定版本 2（需要你确认）

只改一处，其余不变：

| 项目 | 版本 1 | 版本 2 |
| --- | --- | --- |
| A2 | `List` 的输出正确，包括单个元素和空列表 | 在此之上增加：底层写入失败时，`fmt` 返回 `Err`，并且不再继续往下写 |

检查方式是我在 `tests/a2_list.rs` 里加一个测试，用的就是上面那种会失败的假输出。

## 不阻塞的观察

这两条不在验收范围内，改不改由你：

- **`Complex` 的 `{:.1}` 会丢位数。** 实部 1.25、虚部 0.125 被打印成 `1.2 +0.1i`，3 和 4 被打印成 `3.0 +4.0i`。另外符号是手工拼的，虚部为 `-0.0` 时输出 `1.0 +-0.0i`。节点 5 那张表里有一个现成的格式说明能替你处理符号。
- **`Color` 多用了两个临时字符串。** `format!` 一个，`.to_uppercase()` 又一个。这和综合验收第 3 题里同事的写法是同一类问题，格式说明本身就能直接输出大写。

## 接下来

1. 告诉我是否接受版本 2。
2. 接受的话我加上那个测试，你再改 `List`。
3. 可以顺便把 A7 答了：`WorkerId` 你选的是哪种写法，它有没有堆分配，为什么只用 `write!` 不行。

---

**023 · 用户** · `2026-10-08T03:46:32.998Z` · `msg-d67dd60057940232abcd`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/rust/lesson01_hello_formatting/src/lib.rs in the IDE. This may or may not be related to the current task.</ide_opened_file>
明白，接受版本2约定。但我该怎么改呢？就去掉“let _ = ”就可以了吗？还有我没明白你做的第3次写入会失败的假输出例子为什么会报错。例子具体是什么样的？Complex和Color的问题我也改了。

---

**024 · 助手** · `2026-10-08T03:48:17.304Z` · `msg-90055b5a89b1f2735f60`

版本 2 已记下，对应的测试我加进了 `tests/a2_list.rs`，你现在的 `List` 在它上面是失败的，这是预期的起点。`Complex` 和 `Color` 的修改我看了，都对，`Color` 里用 `{0}`、`{1}`、`{2}` 重复引用同一个参数是很好的写法。

下面回答你的两个问题。

## 只去掉 `let _ =` 行不行

不行。去掉之后，`write!` 的结果既没有被用到，也没有被传出去，编译器会警告：

```text
warning: unused `Result` that must be used
help: use `let _ = ...` to ignore the resulting value
```

你最初大概就是照最后那行提示加上的 `let _ =`。它只是让警告闭嘴，错误照样丢了。而且 A6 把警告当错误，去掉后 clippy 那一关也过不了。

一个 `Result` 有三种去处：

| 去处 | 写法 | 含义 |
| --- | --- | --- |
| 丢掉 | `let _ = write!(…);` | 我知道可能失败，故意不管 |
| 传出去 | `write!(…)?;` | 失败了就立刻让当前函数带着这个错误返回 |
| 当场处理 | 用 `if` 或 `match` 判断 | 自己决定失败后做什么 |

`fmt` 里要的是第二种。写法是在 `write!(…)` 后面加一个 `?`：

```rust
write!(f, "(")?;   // 失败：立刻带着这个 Err 返回；成功：继续下一行
write!(f, ")")     // 最后一个不加 ?，也不加分号，它的结果就是返回值
```

`?` 相当于 C 里的 `if (ret < 0) return ret;`，只是压成了一个字符。

## 那个“会失败的假输出”是什么

它不是编译报错，而是我故意造的一个会在指定时刻说“写不进去”的输出目的地，用来模拟磁盘写满或管道关闭。完整代码就在 `tests/a2_list.rs` 开头，核心是这一段：

```rust
struct FailingWriter {
    calls: usize,     // 到目前为止被写了几次
    fail_on: usize,   // 第几次写入要失败
    text: String,     // 成功写进来的内容
}

impl Write for FailingWriter {
    fn write_str(&mut self, s: &str) -> fmt::Result {
        self.calls += 1;
        if self.calls == self.fail_on {
            return Err(fmt::Error);   // 这一次假装写失败
        }
        self.text.push_str(s);        // 其他时候正常收下
        Ok(())
    }
}
```

要点有三个：

- **`fmt::Write` 是一个 trait**，只要求一个方法 `write_str`。谁实现了它，谁就能当 `write!` 的目的地。`String` 实现了它，所以平时能往字符串里写。这里是我自己的类型实现了它，写法和你给 `Complex` 实现 `Display` 是同一个套路。
- **`write_str` 每被调用一次，就是一小段文字要写进来。** 它先把计数加一；如果正好是第 `fail_on` 次，就返回 `Err(fmt::Error)`，这个值的意思就是“写不进去了”。
- **一个 `write!` 会拆成好几次 `write_str`。** 字面文字和每个占位符的内容是分开写的。比如你的 `write!(f, "{i}: {s}")` 在 `i` 为 0、`s` 为 1 时是三次：`"0"`、`": "`、`"1"`。

把 `fail_on` 设成 3，用你现在的 `List` 打印 `List(vec![1, 2, 3])`，逐次调用的记录是这样的（本机实际输出）：

```text
call  1: "["    -> Ok
call  2: "0"    -> Ok
call  3: ": "   -> Err     ← 这次失败了
call  4: ", "   -> Ok      ← 但后面照常继续
call  5: "1"    -> Ok
 …
call 12: "]"    -> Ok
返回 Ok(())，留下的内容："[0, 1: 2, 2: 3]"
```

第 3 次失败后，那一个 `write!` 提前结束，所以 `": "` 和它后面的 `"1"` 都没写进去。它返回了 `Err`，却被 `let _ =` 丢掉了，于是循环接着跑，最后一个 `write!(f, "]")` 成功，整个函数返回 `Ok`。

换成 `?` 之后，第 3 次失败时函数立刻返回，记录只有三行，返回值是 `Err`。

## 新加的测试怎么判

它先用一个永不失败的输出跑一遍，数出总共写了几次；然后让第 1 次、第 2 次直到最后一次轮流失败，每次都要求两件事：`fmt` 返回了 `Err`，并且失败之后没有再写。你现在的实现在第一轮就被拦下：

```text
write number 1 failed, but `fmt` returned Ok after writing "0: 1, 1: 2, 2: 3]"
```

改完后跑这一条就能看到结果：

```bash
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson01-hello-formatting --test a2_list
```

这次我直接说了改法，所以“写入失败时返回 `Err`”这一项的独立性由最后的 A8 变式来补，那道题会再用到它。改好后顺便把 A7 答了：`WorkerId` 你选的是哪种写法，它有没有堆分配，为什么只用 `write!` 不行。

---

**025 · 用户** · `2026-10-08T03:54:03.390Z` · `msg-786df6ecef89a6c30cec`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/rust/lesson01_hello_formatting/src/lib.rs in the IDE. This may or may not be related to the current task.</ide_opened_file>
我改好了。A7:我选用的写法是先format构造一个临时的中间字符串，再通过f.pad将格式化信息赋予到输出字符串中。因为长度不定，有堆分配。因为只用write!无法将f中的对齐格式化信息赋予到输出中。

---

**026 · 助手** · `2026-10-08T03:55:09.367Z` · `msg-ce42c64e4144128917cf`

F1 关闭，A7 通过。现在只剩最后一项 A8。

## 复验

我重跑了全部检查：15 项测试全部通过，其中 `a2_list` 新加的那一项也过了；`cargo fmt --check` 和 clippy 都干净。`List` 里三处中间的 `write!` 都改成了用 `?` 传出，最后一个直接作为返回值，写法正确。

## A7 的反馈

三点都答对了：先 `format!` 再 `f.pad`，有堆分配，只用 `write!` 带不上 `f` 里的对齐要求。

有一处可以更准确。堆分配的原因不是“长度不定”，而是 `format!` 返回的是 `String`，而 `String` 的内容总是放在堆上。这里的长度其实有上界：`u32` 最大是 4294967295，加上前面的 `w` 一共 11 个字节。所以完全可以像标准库的 `Ipv4Addr` 那样，先写进一个固定大小的栈上缓冲区再 `f.pad`，连这次分配也省掉。这不要求你现在做，知道有这条路即可。

## A8：无提示变式

这一项不给提示。规则和前面一样：我写测试，你写实现。

**在 `src/lib.rs` 里加一个新类型：**

```rust
/// A vector of real numbers.
pub struct Vector(pub Vec<f64>);
```

**为它手写 `Display`，要求是：**

- 所有分量写在一对圆括号里，用 `, ` 分隔。
- 每个分量都带符号，正数也要写出 `+`，小数位数用默认的。`Vector(vec![1.5, -2.0, 0.25])` 输出 `(+1.5, -2, +0.25)`。
- 只有一个分量时没有分隔符：`Vector(vec![3.0])` 输出 `(+3)`。
- 空的输出 `()`。
- 底层写入失败时返回 `Err`，并且不再继续往下写。

**测试**在 `tests/a8_vector.rs`，共 4 项。现在是预期的编译失败，原因是找不到 `Vector`。运行：

```bash
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson01-hello-formatting --test a8_vector
```

通过后同样要过 `cargo fmt --check` 和 clippy。A8 过了，这一课就进入结课确认。

---

**027 · 用户** · `2026-10-08T04:02:41.554Z` · `msg-8032afff6c5ea7b25af5`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/rust/lesson01_hello_formatting/src/lib.rs in the IDE. This may or may not be related to the current task.</ide_opened_file>
写好了。

---

**028 · 助手** · `2026-10-08T04:03:29.917Z` · `msg-ab30df9badf5c1b77429`

A8 通过了，而且这次没有任何提示。练习全部完成，这一课可以进入结课确认。

## 复验

- `a8_vector` 的 4 项全部通过，包括写入失败时返回 `Err` 并停止的那一项。测试文件没有被改动。
- 全套 19 项测试通过，`cargo fmt --check` 和 clippy 干净。
- 整个 workspace 的 `host-cpu.sh test` 和 `host-cpu.sh lint` 也都恢复通过了。

`Vector` 的写法是对的：中间三处用 `?` 传出，符号用 `{s:+}`。你还顺手去掉了 `List` 里那层多余的 `is_empty` 判断，循环在空列表上本来就不会执行。

## 结课证据

| 目标 | 需要的证据 | 证据在哪里 | 判断 |
| --- | --- | --- | --- |
| O1：`println!` 的六步、为什么是宏、与 `printf` 的取舍 | 理解 | 节点 2 检查三问中两问一次答对；综合验收的口述讲清了流程，并补上了“格式串必须是字面量”这一代价；运行期两条边界经一次重讲后，换场景复查通过 | 充分 |
| O2：占位符与 trait 的对应、`Vec` 为什么没有 `Display`、derive 生成什么、预测能否编译 | 理解 | 节点 3–4 检查四行判断全对；综合验收三行判断全对，并说明 `Display` 不能 derive；“不能为外部类型实现外部 trait”经补讲后复查通过 | 充分 |
| O3：实现 `Display`、用 `?` 传播错误、用格式说明得到指定输出 | 理解与实践 | 四种 `fmt` 写法的输出预测全对；练习 A1–A8 全部通过；A7 的说明通过；A8 在无提示下完成 | 充分 |

- **未关闭的阻塞问题**：0 个。唯一的 F1（`List` 丢弃写入错误）已修复并复验关闭。
- **帮助影响**：有一处。F1 的改法是我直接说的，影响“写入失败时返回 `Err`”这一项；已由 A8 在无提示下恢复。
- **不阻塞的余项**：
  - Program 里的学习目标还标着“尚未确认”，你的 Rust 基础我也一直按“没有系统写过”处理。两件事都还等你说一句。
  - `lib.rs` 里同时出现了 `core::fmt` 和 `std::fmt::` 两种写法，它们指向同一个东西，统一成一种会更整齐。
- **过程中值得记住的三处纠正**：格式串可以成为运行期的值，这才是“做成函数”换来的灵活性；宽度记在 `f` 里，`write!` 里新写的占位符不会继承它；`let _ =` 只是让警告闭嘴，错误要用 `?` 传出去。

## 需要你决定的两件事

1. **是否关闭第 01 课。** 你确认后我才写入结课结论。关闭后不会自动开始第 02 课。
2. **是否提交。** 这一课的全部改动目前都在本地，没有提交：课程记录、图解页、练习 crate、根 `Cargo.toml` 和 `Cargo.lock`。现在 workspace 是全绿的，可以安全提交。要提交并推送的话说一声。

---

**029 · 用户** · `2026-10-08T04:04:04.610Z` · `msg-d230e1f5d18a187ab5cb`

确认关闭。请提交commit，暂不推送。

---

**030 · 助手** · `2026-10-08T04:05:44.593Z` · `msg-b0184fc62b759a5356fc`

第 01 课已关闭，提交也做好了，没有推送。

## 结课

- 课程记录写入了结课结论，阶段改为 `complete`，确认引用的是你这句“确认关闭。”
- Checkpoint 回到课程边界：当前没有进行中的课，下一步是你决定是否开始第 02 课“数据的形状：基本类型、struct 与 enum”。不会自动开始。

## 提交

提交 `f41a322`（`feat: complete Rust formatted output lesson`）在本地 `main` 上，比远端领先 1 个提交，工作区干净。包含 15 个文件：

- 课程记录 `docs/rust-learning/lessons/01-hello-formatting.md` 和节点 2 的图解页
- 练习 crate `rust/lesson01_hello_formatting/`：你的 `src/lib.rs` 和 6 个测试文件
- 根 `Cargo.toml`（workspace 加入 `rust/*`）和 `Cargo.lock`
- `docs/rust-learning/README.md` 的 Checkpoint 与课程索引

提交前跑过的检查都通过：整个 workspace 的 `host-cpu.sh test` 和 `host-cpu.sh lint`、全量 pytest（114 项）、Ruff、文档链接，以及 Skill 生成副本的一致性。

## 两处顺手同步

练习目录现在真实存在了，有两句说明因此过时，我一并改了：

- `AGENTS.md` 原来写着“`rust/` 要到第一个练习开始时才存在”，现在改成“`rust/` 下的练习 crate 通过 `rust/*` 加入 workspace，每个子目录都必须是 crate”。
- 根 `README.md` 的目录树里加了 `rust/` 一行。

## 留给以后的

- Program 里的学习目标仍标着“尚未确认”。
- 这一课里你在练习前问到了分支、循环和 `Vec` 的基本用法。后面课次的练习，我会先把用到但还没讲的语法交代清楚。
- 这一课的学习日志和卡片没有生成，需要时再说。

推送时说一声即可。

---

**031 · 用户** · `2026-10-08T04:17:51.402Z` · `msg-befa28591263cad8acc1`

我看了Program 里的学习目标，可以确认。Rust基础设置为先前完全没有接触过Rust，没有关于Rust的任何基础，这一点也是我接下来想跟你提的学习中遇到的困难之一。我在这次课程学习中遇到了两个困难，第一点是，我们的课程是属于有参考教程的课程。在课程开头和一个个节点的学习过程中，你需要提醒我去看本次课程的参考教程在哪和要看参考教程里的哪些部分。第二点就是由于我完全没有Rust基础，所以看到很多名词都很疑惑，比如trait、crate等等，我通过课程外查找了一些资料才初步理解一点，从而继续了课程。如果一直有这么多令人疑惑的名词，我感到学习的阻力很大。我希望后续的学习尽可能渐进地继续或者详细解释必要的名词。

---

**032 · 助手** · `2026-10-08T04:20:02.714Z` · `msg-b93dc0e30502d76b79a5`

这两点都是我讲法上的问题，不是你的问题。两件事已经记下来了，下面先说怎么改，再把第 01 课欠的两样东西补上。

## 已经记下的

- **学习目标**：Program 里的 Objective 标成了“2026-10-08 学习者确认”。
- **起点**：Program 和第 01 课的记录里都写明了你此前完全没有接触过 Rust。
- **两条新约定**写进了 `docs/rust-learning/README.md` 的“本课程的记录约定”，以后不管是我还是 Codex 带课都会看到。

## 以后每一课怎么上

**先指路，再讲解。** 开课时我会列出这一课对应教程的哪几页。每个节点开头写明这一步对应哪一页、建议先读还是听完再读。页面同时给仓库里的路径和在线地址。

**名词渐进引入。** 每课开头列出这一课会出现的新名词。每个名词第一次出现时，先用平实的话讲清它是什么，并说出它在 C++ 或 Python 里对应什么，然后才使用。还没讲到的名词，我不拿它去解释别的东西；实在绕不开，当场补一句。

## 补上第 01 课的阅读指引

五个节点对应的教程页面如下。仓库里的路径都在 `docs/rust-by-example/src/` 下，在线地址都在 `https://doc.rust-lang.org/1.97.1/rust-by-example/` 下，把 `.md` 换成 `.html` 即可。

| 节点 | 内容 | 教程页面 |
| --- | --- | --- |
| 1 | 程序骨架与编译运行 | `hello.md`、`hello/comment.md` |
| 2 | `println!` 为什么是宏 | `hello/print.md` 的前半 |
| 3 | `Display` 与 `Debug` | `hello/print/print_debug.md`、`hello/print/print_display.md` |
| 4 | 自己实现 `Display` | `hello/print/print_display.md`、`hello/print/print_display/testcase_list.md` |
| 5 | 格式说明 | `hello/print.md` 的后半、`hello/print/fmt.md` |

教程原文比我讲的简略得多，现在回头读一遍会很快，可以当作复习。

## 补上第 01 课欠解释的名词

下面这些词我在第 01 课里要么没解释就用了，要么只带了半句。

| 名词 | 是什么 | 对应你熟悉的 |
| --- | --- | --- |
| crate | Rust 的编译单位。一个 crate 整体编译成一个库或一个可执行文件 | C++ 里的一个库或一个可执行目标；Python 里一个可安装的包 |
| package | 一个带 `Cargo.toml` 的目录，里面通常放一个 crate。练习目录 `rust/lesson01_hello_formatting/` 就是一个 | CMake 里的一个子工程 |
| workspace | 把多个 package 放在一起统一构建。仓库根目录的 `Cargo.toml` 定义了它 | 顶层的 `CMakeLists.txt` |
| Cargo | 构建工具兼依赖管理器，替你调用编译器 `rustc` | CMake 加 pip |
| struct | 把几个字段放在一起的自定义类型 | C++ 的 `struct` |
| 元组结构体 | 字段没有名字、按位置排的 struct，比如 `struct MinMax(i64, i64)`，用 `.0`、`.1` 取字段 | `std::pair` 或 `std::tuple`，但有自己的类型名 |
| trait | 一组方法的约定。类型声明自己满足这个约定之后，就能用在要求它的地方 | C++ 的抽象基类或 concept；Python 里“只要有 `__str__` 就能 `str()`”这种协议 |
| `impl` | 为一个类型写方法，或者为它实现某个 trait 的代码块 | C++ 里类的成员函数定义 |
| 属性 | 写在定义上方、以 `#[…]` 包起来的标注，告诉编译器怎样对待下面这一项 | C++ 的 `[[nodiscard]]`；Python 的装饰器 |
| derive | 一种属性。`#[derive(Debug)]` 让编译器替你生成 `impl Debug` | Python 的 `@dataclass` 自动生成 `__repr__` |
| 借用 | `&T` 是只读的引用，`&mut T` 是可写的引用。拿着引用不等于拥有这个值 | C++ 的 `const T&` 和 `T&` |
| `Result` | 表示“成功或失败”的返回值类型，取值是 `Ok(值)` 或 `Err(错误)` | C 的返回码；C++23 的 `std::expected` |
| panic | 程序遇到无法继续的错误时的受控崩溃：打印信息，然后结束当前线程 | C++ 里没人接住的异常 |
| rustfmt、Clippy | 前者自动排版，后者检查不地道或可疑的写法 | clang-format、clang-tidy |

其中借用和 `Result` 在这里只是够用的说法，分别在第 08 课和第 12 课展开；crate、package 和 workspace 在第 06 课展开。

## 两件事要问你

1. **第一条约定要不要推广。** “先指路”对 Triton 和算法课同样适用。我目前只写进了 Rust 课程的约定，要不要也写进三条课程共用的学习者画像 `docs/learning-profile.md`？
2. **要不要建一份名词表。** 可以在 `docs/rust-learning/` 下放一页词表，把上面这张表作为起点，以后每课结课时补入新名词，方便你随时查。

这次对课程约定和第 01 课记录的修改还没有提交，上一个提交 `f41a322` 也还没有推送。
