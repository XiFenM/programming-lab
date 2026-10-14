# 第 02 课：数据的形状：基本类型、struct 与 enum

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `rust-02-data-shapes` |
| Program | [Rust 学习档案](../README.md) |
| 能力标题 | 看到一个 Rust 类型，能说出它的值占多少字节、里面装着什么，哪些信息写在类型里、哪些带在值里；解释 Rust 在数值运算、数组访问和“多选一”的数据上，各把 C 的哪种隐患变成了编译错误或确定的运行期行为、付出了什么；并能用元组、切片、struct 和 enum 为一个小领域建模，用解构和 `match` 把数据读出来 |
| 阶段 | `complete`（2026-10-14 学习者确认关闭） |
| 启动授权 | 2026-10-08，学习者提出“让我们开始rust的第2课吧。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/rust-by-example/src/primitives.md` 与 `primitives/` 下的 3 个文件；`docs/rust-by-example/src/custom_types.md` 与 `custom_types/` 下的 6 个文件 | `teaching-spine` | 上游提交 `898f0ac1479223d332309e0fce88d44b39927d28`（随 Rust 1.97.1 发布）；仓库 commit `1b88f9a` | 教学顺序、示例与章内 Activity：Primitives、Literals and operators、Tuples、Arrays and Slices、Custom Types、Structures、Enums、use、C-like、Testcase: linked-list、constants |
| Rust 1.97.1 标准库源码（本机 `rust-src` 组件，路径均以 `library/` 开头） | `implementation-authority` | `rustc 1.97.1 (8bab26f4f 2026-07-14)` | `core/src/cmp.rs` 的 `Ordering`；`core/src/option.rs` 的 `Option`；`core/src/net/ip_addr.rs` 的 `IpAddr` 与 `Ipv4Addr`；`core/src/time.rs` 的 `Duration`；`alloc/src/vec/mod.rs` 的 `Vec`；`alloc/src/string.rs` 的 `String`；`core/src/slice/mod.rs` 的 `len`；`core/src/num/uint_macros.rs` 的 `checked_mul`；`core/src/option.rs` 的 `unwrap` 与 `is_some`；`core/src/macros/mod.rs` 的 `matches!`；`core/src/prelude/v1.rs`；`alloc/src/boxed.rs` 的 `Box` |
| [Rust Reference](https://doc.rust-lang.org/1.97.1/reference/) | `interface-authority` | 1.97.1 | Behavior not considered unsafe 的 Integer overflow；Type layout 的默认表示与 `repr(C)`；Constant items、Static items |
| [Cargo Book 的 Profiles](https://doc.rust-lang.org/1.97.1/cargo/reference/profiles.html) | `interface-authority` | 1.97.1 | `dev` 与 `release` 两个 profile 的 `overflow-checks` 默认值 |
| [`safetensors/safetensors`](https://github.com/safetensors/safetensors) 的 `safetensors/src/tensor.rs` | `implementation-authority`（真实系统锚点，本课的贯穿案例） | tag `v0.8.0`，提交 `a406ca3e7a90598be0cd05a50069cb9bf5ef6ba6` | `TensorInfo`、`TensorView`、`Dtype` 的定义，`Dtype::bitsize`，校验字节数时的 `checked_mul`，按 `data_offsets` 取出数据切片的那一行；文件开头的两个 `const`（`MAX_HEADER_SIZE`、`N_LEN`）与 `read_metadata` |
| Hugging Face 上 [`Qwen/Qwen2.5-7B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) 的 `config.json` 与 `model-00001-of-00004.safetensors` 的文件头 | `empirical-evidence`（真实规模的数字） | 版本 `a09a35458c702b33eeacc393d103063234e8bc28`，读取于 2026-10-08 | 文件头长度、张量条数，以及前几个张量的 dtype、shape 与 `data_offsets` |
| [`ROCm/ATOM`](https://github.com/ROCm/ATOM) 的 `atom/mesh/src/` | `implementation-authority`（真实系统锚点） | 提交 `43f5393dc456c1047d316d14be6acb662cce6db7` | 带数据的 enum：`core/worker.rs` 的 `WorkerType`，`routers/token_handle/token_chunk.rs` 的 `TokenChunk`、`FinishReason`、`MatchedStop`，`config/types.rs` 的 `RoutingMode` 及其 `match`；`core/worker.rs` 中对 `WorkerType` 的两个 `match`；`middleware.rs` 的 `static ACTIVE_HTTP_CONNECTIONS`；全目录 enum、struct、`const`、`static` 与各种模式写法的数量 |

### 目标与所需证据

| ID | 可观察目标 | 理解 | 实践 | 实证 |
| --- | --- | --- | --- | --- |
| O1 | 说清标量类型怎样决定一个数的大小、取值范围和允许的运算；解释 Rust 为什么不做隐式的数值转换，整数溢出在调试构建和发布构建下各发生什么；能在 `as`、`checked_*` 与 `wrapping_*` 之间按场景选择并说出理由（`From` 与 `TryFrom` 的系统讲解在第 03 课） | 需要 | 不需要 | 不需要 |
| O2 | 解释元组、数组 `[T; N]` 与切片 `&[T]` 的区别：个数和长度写在类型里还是带在值里；切片为什么由指针和长度两部分组成，越界访问凭什么被拦住、代价是什么；与 C 的数组退化、`(指针, 长度)` 传参和 NumPy 视图对照 | 需要 | 不需要 | 不需要 |
| O3 | 解释 struct 三种形式各自的用途和内存布局；enum 作为“标签加载荷”的布局，`match` 的穷尽性检查防住了什么，与 C 的 `enum` 加 `union`、C++ 的 `std::variant` 相比换来了什么、付出了什么；递归类型为什么需要 `Box`；`const` 与 `static` 的区别 | 需要 | 不需要 | 不需要 |
| O4 | 用元组、切片、struct 和 enum 为一个小领域建模：定义类型、实现方法，用解构和 `match` 读出数据，并处理溢出与越界 | 需要 | 需要 | 不需要 |

### 当前证据

- **已有证据**：[阶段事件](#条件片段阶段事件) E-01 提供 O1、O2 的节点级理解证据，以及 O3 中 struct 布局部分的节点级理解证据。E-02 提供 O3 中 enum 与递归类型部分的节点级理解证据、O4 的理解证据（把四种请求状态建模成 enum），关闭了 O2 中“数组的值就是元素本身”的复查，并包含综合验收：O1–O3 的理解证据充分。已确认的前置只决定讲解起点：学习者熟悉 C/C++ 与 Python，Rust 只学过第 01 课，见[学习者画像](../../learning-profile.md)。
- **仍缺证据**：无。O4 的实践证据由 E-03、E-04 提供：练习约定 P1 版本 2 的 A1–A9 全部通过，阻塞问题全部关闭。结论见[结课](#条件片段结课)。
- **来源与环境核对（2026-10-08）**：本机 `rustc 1.97.1 (8bab26f4f 2026-07-14)`，x86_64 Linux，gcc 与 g++ 13.3.0；试验文件都在仓库外的临时目录。
  - 大小与对齐（`size_of`、`align_of`）：`i8` 到 `i128` 为 1、2、4、8、16 字节，`isize` 与 `usize` 8，`f32` 4，`f64` 8，`char` 4，`bool` 1，
    `()` 0。`[i32; 5]` 20，`&[i32; 5]` 与 `&i32` 都是 8，`&[i32]` 与 `&str` 16，`Vec<i32>` 与 `String` 24。`(u8, u32, u8)` 8。
  - 数值规则：`let b: u64 = a;`（`a: u32`）、`a + 10u64`、`-1i32 < 1u32`、`let total: u64 = numel * 16;`（`numel: u32`）都是 E0308；
    `if n`（`n` 为整数）也是 E0308；`xs[i]`（`i: u32`）是 E0277，提示下标必须是 `usize`。`300i32 as u8` 得 44，`-1i32 as u32` 得
    4294967295，`1e10f64 as i32` 得 2147483647，`f64::NAN as i32` 得 0，`u8::try_from(300i32)` 得 `Err`。稳定版上写 `f16` 报
    E0658（类型尚不稳定）。
  - 溢出：`1u32 - 2` 写成常量时是编译错误 “this arithmetic operation will overflow”（lint `arithmetic_overflow`，默认 deny）。
    运行期才知道操作数时，不带 `-O` 的构建 panic，信息为 “attempt to subtract with overflow”；带 `-O` 的构建输出 4294967295。
    用 `u32` 计算 152064 × 3584 × 16：不带 `-O` 时在第二次乘法处 panic，带 `-O` 时得到 130023424（正确值 8719958016）；
    `checked_mul` 返回 `None`，先转成 `u64` 或 `usize` 再乘得到正确值。
  - 数组与切片：把 `[i32; 4]` 传给要 `[i32; 5]` 的函数是 E0308。常量下标越界是编译错误 “this operation will panic at runtime”
    （lint `unconditional_panic`）；运行期越界在两种构建下都 panic，信息为 “index out of bounds: the len is 5 but the index is 5”。
    栈上的数组 `xs` 起始地址为 `p` 时，`&xs[1..4]` 的两个字是 `p + 4` 和 3；`xs.get(5)` 返回 `None`。
  - 布局（`-Zprint-type-sizes`，通过 `RUSTC_BOOTSTRAP=1` 打开，只用于观察）：`struct { a: u8, b: u32, c: u8 }` 默认 8 字节，
    字段被排成 `b`、`a`、`c`；加 `#[repr(C)]` 后 12 字节。教程里的 `WebEvent` 24 字节，没有单独的判别值字段；
    `List`（`Cons(u32, Box<List>)`、`Nil`）16 字节，其中判别值 4 字节；`Number` 1 字节；`Color`（判别值到 `0xff0000`）4 字节；
    `Option<u32>` 8 字节，`Option<Box<List>>`、`Option<&i32>` 都是 8 字节，`Option<NonZero<u32>>` 4 字节，`Option<String>` 24 字节。
  - 贯穿案例的布局（`offset_of!`，按 safetensors 的字段定义在本机复刻）：`TensorInfo` 与 `TensorView` 都是 48 字节、对齐 8；`TensorView`
    默认把 `shape` 放在偏移 0、`data` 在 24、`dtype` 在 40，加 `#[repr(C)]` 后依次为 8、32、0，仍是 48 字节。`{ a: u8, b: u32, c: u8 }` 默认
    偏移为 4、0、5，`#[repr(C)]` 下为 0、4、8。`{ dtype: u8, start: u64, flag: u8 }` 默认 16 字节，`#[repr(C)]` 下 24 字节。对 28 字节的缓冲区取
    `&buf[16..40]`，在带 `-O` 的构建下 panic，信息为 “range end index 40 out of range for slice of length 28”；取 `&buf[20..10]` 的信息为
    “slice index starts at 20 but ends at 10”。`as` 的截断在不带 `-O` 的构建下也不 panic。
  - 胖指针的第二个字（2026-10-12）：`&[u8]` 取 `&xs[1..4]` 时是 3；`&str` 取 `"héllo"` 时是 6，即字节数，而字符数是 5；`&dyn Display` 的第二个字是一个地址，
    两个 `i32` 值相同，换成另一个类型就不同，按虚表读出的大小与对齐分别是 4、4 和 8、8。`&dyn Display`、`Box<dyn Display>`、`Box<[u8]>` 都是 16 字节，
    `Box<u8>` 8 字节。Reference 的 Dynamically Sized Types 一节写明指向切片和 `str` 的指针另存元素个数，指向 trait 对象的指针另存虚表指针；标准库
    `core/src/ptr/metadata.rs` 用 `Pointee::Metadata` 统一表示这个字，`core/src/slice/mod.rs` 的 `len` 就是 `ptr::metadata(self)`。
  - enum 的原始字节（2026-10-12）：`Device::Cuda(3)` 为 `01 00 00 00 03 00 00 00`，`Option<u32>` 的 `Some(7)` 为 `01 00 00 00 07 00 00 00`；
    `Option<&i32>` 与 `Option<Box<i32>>` 的 `None` 是全 0；`Color::Red`、`Green`、`Blue` 分别是 `0xff0000`、`0x00ff00`、`0x0000ff` 的小端 4 字节。`WebEvent`
    的三个字：`PageLoad` 的第一个字是 `0x8000000000000000`，`PageUnload`、`KeyPress('x')`、`Click` 依次是末位 1、2、4，`KeyPress` 的字符在第二个字；
    `Paste("my text")` 的三个字是容量 7、堆指针、长度 7。
  - 链表（2026-10-12）：教程的 4 个 enum 示例在 edition 2021 与 2024 下都无诊断，链表示例输出 “linked list has length: 3” 和 “3, 2, 1, Nil”。3 个元素的链表
    头节点在栈上，其余两个 `Cons` 和末尾的 `Nil` 各占堆上一个 16 字节的节点；`Cons` 的判别值是 0，`Nil` 是 1。主线程栈 8 MB 时，100 万个节点的链表在
    不带 `-O` 的构建下调用递归的 `len` 报 “has overflowed its stack”，改成循环则正常；释放这个链表在两种构建下都栈溢出，10 万个节点时都正常。
  - `match` 的边界（2026-10-12）：给 enum 新增一个变体后，逐个列出变体的 `match` 报 E0004，带 `_` 的 `match` 照常编译。标了 `#[non_exhaustive]` 的 enum，
    在定义它的 crate 内可以不写 `_`，在另一个 crate 里不写 `_` 报 E0004，并提示 “a wildcard `_` is necessary to match exhaustively”。`type Km = f64;` 的值
    可以直接当 `f64` 用，`struct Meters(f64);` 的值不行（E0308）。safetensors 的 `Dtype::bitsize` 有 22 个分支，没有 `_`。
  - 节点 5–6 检查题用到的类型（2026-10-12）：`enum Tree { Leaf(u32), Node(Tree, Tree) }` 是 E0072；把两处换成 `Box<Tree>` 后 16 字节，没有单独的判别值；
    `struct Chunk { data: [u8; 1024], next: Option<Box<Chunk>> }` 1032 字节；`struct Node { elem: u32, next: Option<Box<Node>> }` 16 字节。把请求的四种状态写成
    一个带 `kind: u8` 的 struct 是 48 字节，写成四个变体的 enum 是 24 字节。`match self { Cons(_, tail) => 1 + tail.len(), Nil => 0 }` 可以编译。C 里
    `struct Node { uint32_t v; struct Node next; };` 报 “field ‘next’ has incomplete type”。`atom/mesh/src` 的 `core/job_queue.rs` 中 `Job` 的各变体把配置对象放在
    `Box` 里；`routers/token_handle/token_handle.rs` 中 `TokenHandle` 与 `Inner` 互相包含，靠 `Box<TokenHandle>` 断开，另一个变体是 `Single(Box<dyn TokenSource>)`。
  - 答疑与节点 7 的核对（2026-10-13）：
    - `Box`：`Box<u32>` 与 `Box<[u64; 100]>` 都是 8 字节，`[u64; 100]` 800 字节；交给另一个变量后再用原名是 E0382；C++ 的 `unique_ptr` 在 `std::move` 之后为空，
      解引用能编译，运行时段错误。教程 `std/box.md` 的示例输出 16、32、8、8、8、16。
    - 模式：`if let`、`let … else`、`while let`、`matches!` 都能编译；对多变体 enum 写普通 `let` 是 E0005；没有 `PartialEq` 时用 `==` 是 E0369；对 `None` 调 `unwrap`
      panic，信息为 “called `Option::unwrap()` on a `None` value”。标准库里 `Option::unwrap` 的函数体是两分支的 `match`，`is_some` 是 `matches!(*self, Some(_))`，
      `matches!` 展开成带 `_ => false` 的 `match`；`Some`、`None` 由 `core/src/prelude/v1.rs` 预先引入。`let x: Option<u32> = 7;` 是 E0308，提示用 `Some` 包起来。
      enum 新增变体后，`if let` 的代码照常编译。`atom/mesh/src` 的 185 个 `.rs` 文件里，按 grep 粗略计数，`match` 与 `if let` 各约 520 处，`matches!` 约 90 处，
      `let … else` 约 40 处。
    - 不单独占字节的标签：`Option<Box<u32>>` 的 `Some` 是堆地址本身，`None` 是全 0；`Option<bool>` 的三个值是 `00`、`01`、`02`；手写的
      `enum { Nothing, Has(u32) }` 与 `enum { Nothing, Has(Box<u32>) }` 都是 8 字节，布局与 `Option` 相同。
    - `Box` 与 `&mut`：`&mut u32` 与 `Box<u32>` 都是 8 字节；返回指向局部变量的 `&mut` 是 E0106（写上生命周期后是 E0515）；借出期间使用原变量是 E0503，再借一次是
      E0499；原变量的作用域先结束是 E0597，借用期间 `drop` 原主是 E0505，借用最后一次使用之后再 `drop` 可以编译。C 里 `free` 之后解引用，不加选项没有诊断，
      `-Wall` 有 `-Wuse-after-free`；C++ 里 `reset` 之后通过引用写入，`-Wall -Wextra` 没有诊断；两个程序都正常退出并打印无意义的数。
    - 节点 5–6 检查的复核：学习者写的四变体 enum 能编译，24 字节。`Running(u32, u32)` 的两个位置写反能编译，读出来的含义就反了；带字段名的写法与顺序无关。
      带 `_ => true` 的 `match` 在加入 `Cancelled` 后把它判成“仍在进行”，逐个列出的 `match` 报 E0004。`Tree::Leaf(7)` 的第一个字是 0，7 在第二个字的低 4 字节；
      `Node` 的两个字是两个堆地址。`enum { Leaf(u32), Node(u64, u64) }` 没有可借用的取值，是 24 字节。
    - `const` 与 `static`：教程 `constants.md` 的示例去掉最后的赋值后输出 “This is Rust”“The threshold is 10”“16 is big”。初始值调用普通函数是 E0015，
      `const fn` 可以；`let n = 5; [0u8; n]` 是 E0435 并建议改用 `const`，`static N` 作数组长度在 1.97.1 上能编译；给不可变的 `static` 赋值是 E0594。同一个 `static`
      在两个函数里取到的地址相同，与栈、堆上的地址不在一个区域。`static` 的 `AtomicU64` 加两次后读出 2；改成 `const` 能编译，有 `const_item_interior_mutations`
      警告，读出 0。Reference 写明 `const` “not associated with a specific memory location”“essentially inlined wherever they are used”，并建议除数据量大、需要唯一地址、
      需要内部可变性三种情况外优先用 `const`。safetensors 的 `tensor.rs` 第 10、11 行是 `const MAX_HEADER_SIZE: usize = 100_000_000;` 与
      `const N_LEN: usize = size_of::<u64>();`。`atom/mesh/src` 按 grep 计数有 143 个 `const`、27 个 `static`、0 个 `static mut`。
    - 嵌套模式与 `WorkerType`：`atom/mesh/src/core/worker.rs` 里 `WorkerType` 的 `Display` 实现是 `match` 套 `match`；改写成 `Prefill { bootstrap_port: Some(port) }` 与
      `Prefill { bootstrap_port: None }` 两个并列分支后，四种取值的输出相同，删掉 `None` 分支报 E0004；对 enum 写 `w.bootstrap_port` 报 E0609。`WorkerType` 是 4 字节、对齐 2，
      开头 2 个字节在 `Prefill` 且端口为 `None`、为 `Some`、`Regular`、`Decode` 四种情况下依次是 0、1、2、4，`Some(8998)` 的后 2 个字节是 `26 23`。`rect_area` 的字段访问版和
      解构版在 `-O` 下分别是 7 条和 8 条指令，都没有函数调用和额外的内存复制。
    - 综合验收用到的类型：`atom/mesh/src/routers/token_handle/token_chunk.rs` 的 `TokenChunk` 是 192 字节，`Complete` 的字段合计 188 字节，`Partial` 的字段合计
      48 字节，没有单独的判别值；把 `Complete` 的字段装进 `Box` 后整个 enum 是 48 字节。
  - 报错：递归而不加间接的 `enum List { Cons(u32, List), Nil }` 是 E0072 “recursive type `List` has infinite size”；`match` 少写一个
    变体是 E0004 “non-exhaustive patterns: `WebEvent::PageUnload` not covered”；`1i32 as Number` 是 E0605；直接取变体里的数据
    `e.0` 是 E0609；给 `const` 赋值是 E0070；`const` 不写类型报 “missing type for `const` item”；改 `static mut` 而不写 `unsafe` 是
    E0133；初始化 struct 时漏字段是 E0063；13 个元素的元组用 `{:?}` 打印是 E0277。
  - 对照：C 里 `sizeof` 在 `main` 中对 `int xs[5]` 得 20，在参数写成 `int a[5]` 的函数里得 8（`-Wsizeof-array-argument`），把
    `int ys[4]` 传给它能编译；`struct { uint8_t; uint32_t; uint8_t; }` 为 12 字节。`uint64_t total = numel * 16;`（`numel` 为
    `uint32_t`）在 `-Wall -Wextra` 下没有警告，得到 130023424；`-1 < 1u` 的结果是 0。手写的 `enum` 加 `union`：`switch` 少一个分支只在
    `-Wall` 下有 `-Wswitch` 警告，把标签改成另一种而不改载荷后读出 `x=120, y=0`，`enum Kind k = 42;` 能编译。C++ 的
    `std::variant<PageLoad, KeyPress, Paste>` 为 40 字节（`std::string` 32），`std::get<Paste>` 取错成员时在运行期抛
    `bad_variant_access`，`std::visit` 少一个分支是编译错误。
  - 真实规模：`Qwen/Qwen2.5-7B-Instruct` 的第一个分片文件 3,945,441,440 字节，文件头 9,368 字节，登记 82 个张量；第一个是
    `model.embed_tokens.weight`，BF16，shape 为 [152064, 3584]，`data_offsets` 为 [0, 1089994752]；最后一个张量的起始偏移是
    3,941,762,048，超过 `i32` 的上限。`atom/mesh/src` 中有 60 个 enum、250 个 struct。

  以上是这一个工具链和平台上的观察。

### 核心工件与参考

| 角色 | 路径或引用 | 说明 |
| --- | --- | --- |
| 来源或知识产物 | `docs/rust-by-example/src/primitives.md`、`primitives/`、`custom_types.md`、`custom_types/` | 教程快照，不修改 |
| 你写（learner-owned） | `rust/lesson02_data_shapes/src/lib.rs` | P1 的三个函数、三个类型及其方法；骨架只含教程里的 `Matrix`、`Point`、`Rectangle` 三个类型定义，由 Agent 放入后归学习者 |
| 我维护（agent-owned） | `rust/lesson02_data_shapes/tests/` | P1 的验收测试，七个文件共 40 项：A1–A6 各一个文件（版本 2 给 `a6_slice.rs` 增加了 3 项），另有 A9 的 `a9_placement.rs`（8 项） |
| 我维护（agent-owned） | [内存布局图解页](../attachments/02-data-shapes/memory-layout.html) | 五节：数组与切片的两个机器字、从权重文件里取出一个张量、struct 的字段怎样摆、enum 的标签与载荷（含检查题里的 `RequestState` 与 `Tree`，以及 `WorkerType` 的两种 `match` 写法）、用 `Box` 串起来的链表与二叉树；可交互，离线可用 |

## 条件片段：练习约定

- **编号与版本**：P1，版本 2；学习者接受于 2026-10-13（“我接受版本2”）。版本 1 接受于同日（“我接受练习约定。”）。
  版本 2 有两处变化，都不归咎于学习者：
  1. 交付说明第 2 项删去“用嵌套解构取出四个坐标”，`rect_area` 用字段访问或解构都可以。Agent 最初提议把这一要求加进 A2 的检查方式；
     学习者指出这里字段访问同样直接、解构还要多声明变量，Agent 核对后同意：带字段名的 struct 读几个字段时解构没有实际好处。
     嵌套模式的实践证据改由 A9 的变式在 `match` 里取得。
  2. A6 写明空张量的边界并增加三项测试。版本 1 的测试只在缓冲区中间放了空张量，是 Agent 的测试缺口。
- **为什么做**：O4 需要实践证据。综合验收后只有理解证据，这一课学习者还没有亲手写过代码。
- **你交付什么**：在 `rust/lesson02_data_shapes/src/lib.rs` 中完成五件事。前两件是教程的 Activity，后三件沿用本课的贯穿案例。
  1. `transpose(matrix: Matrix) -> Matrix`：`Matrix(a, b, c, d)` 变成 `Matrix(a, c, b, d)`。
  2. `rect_area(rect: Rectangle) -> f32` 与 `square(top_left: Point, side: f32) -> Rectangle`：面积不为负；
     `square` 以给定的点为左上角，向右、向下各延伸 `side`，y 轴向上。
  3. `Dtype`：不带数据的 enum，变体 `U8`、`I32`、`F32`、`BF16`、`F64`；`bitsize(self) -> usize` 用 `match` 写，不用 `_`。
  4. `Device`：变体 `Cpu` 与 `Cuda(u32)`；`name(&self) -> String` 返回 `cpu` 或 `cuda:3` 这样的名字。
  5. `TensorInfo`：公开字段 `dtype: Dtype`、`shape: Vec<usize>`、`data_offsets: (usize, usize)`；
     `byte_len(&self) -> Option<usize>` 是各维乘积乘位数再除以 8，空 shape 算 1 个元素，任何一步溢出返回 `None`；
     `slice<'a>(&self, data: &'a [u8]) -> Option<&'a [u8]>` 返回这个张量的字节，起止颠倒、超出 `data`、长度与 `byte_len` 不一致、
     `byte_len` 溢出时返回 `None`，不能 panic。空张量的起止相等：只要不超过 `data` 的长度就返回空切片，包括两者都等于 `data` 的长度、
     以及 `data` 本身为空；超过则仍返回 `None`。
- **约定里一并交代的写法**（练习要用、此前没有系统讲过）：`pub`；三个类型各自的 derive 行；`#[must_use]`；`match` 里的 `A | B`；
  `?` 用在 `Option` 上；`for dim in &self.shape` 与 `*dim`；`slice` 签名里的 `'a` 照抄；`(a - b).abs()` 与 `String::from`。
- **验收项**：

| ID | 可观察标准 | 检查方式 |
| --- | --- | --- |
| A1 | `transpose` 正确，转置两次得到原矩阵 | 测试 `a1_transpose` |
| A2 | `rect_area` 正确，两个角给反时也不为负；`square` 的两个角正确 | 测试 `a2_rectangle` |
| A3 | `Dtype` 五个变体的位数正确；占 1 字节，能复制、能用 `==` 比较；`match` 里没有 `_` | 测试 `a3_dtype`，加读代码 |
| A4 | `Device` 的名字正确，能用 `==` 比较 | 测试 `a4_device` |
| A5 | `byte_len`：普通形状、空 shape、含 0 的维度、两处溢出 | 测试 `a5_byte_len` |
| A6 | `slice`：取出的字节正确，包括位于缓冲区开头、中间、末尾和空缓冲区里的空张量；四种坏输入和超出缓冲区的空区间都返回 `None` | 测试 `a6_slice` |
| A7 | 这个 crate 通过 `cargo fmt --check` 与 `cargo clippy -- -D warnings`；不用 `unwrap`、`expect` 和 `unsafe` | 命令 |
| A8 | 说明 `slice` 的四种坏输入各由哪一步拦住；`byte_len` 里的 `checked_mul` 换成 `*` 后，测试在调试构建和发布构建下各会怎样 | 学习者的说明，按要点核对 |
| A9 | A1–A8 通过后的无提示小变式：实现一个新的小类型并通过测试。2026-10-13 发出的题目是 `Placement`（`Unloaded`，`Loaded { device: Device, bytes: usize }`）：`gpu_index(&self) -> Option<u32>` 只用一个 `match`，不套 `match`，不用 `_` 和 `if let`；`padded_bytes(&self) -> Option<usize>` 把字节数向上取整到 64 的倍数，`Unloaded` 算 0，结果放不进 `usize` 时返回 `None`。约定澄清（2026-10-14，不改变门槛）：“不用 `_`”指不写 `_ =>` 这样的兜底分支，模式里略过用不到的字段不受限制 | 测试 `a9_placement`；`gpu_index` 的写法读代码核对；格式检查与 Clippy 同 A7 |

- **运行方式**：单项为
  `bash scripts/host-cpu.sh run -- cargo test -p rust-lesson02-data-shapes --test a1_transpose`，去掉 `--test …` 即全部。
  完成之前整个 workspace 的 `host-cpu.sh test` 与 `host-cpu.sh lint` 会在这个 crate 上失败，练习期间这些改动留在本地。
- **文件边界**：

| 边界 | 路径或受限模式 |
| --- | --- |
| 你写 | `rust/lesson02_data_shapes/src/lib.rs` |
| 我维护 | `rust/lesson02_data_shapes/Cargo.toml`；`rust/lesson02_data_shapes/tests/`；根 `Cargo.lock`；本 Lesson 记录；`docs/rust-learning/README.md` 的 Checkpoint |
| 我只读 | `docs/rust-by-example/src/primitives/`、`docs/rust-by-example/src/custom_types/` |
| 本次不动 | 其他 crate、CI 配置和依赖 |

- **求助如何影响证据**：随时可以求助；透露关键写法只影响相应的验收项，之后用一个小变式在无提示下恢复。A9 期间不给提示。
- **非目标与可选项**：不引入第三方依赖，不做性能要求；教程 Activity 里给 `Matrix` 加 `Display` 是第 01 课的复习，不在本次范围。
- **完成门槛**：A1–A9 全部通过，阻塞问题全部关闭。

## 条件片段：帮助影响

| 透露到什么程度 | 影响的验收项或工件 | Agent 是否写了学习者核心工件 |
| --- | --- | --- |
| 学习者贴出 `a5_byte_len` 的失败并问为什么“还是溢出了”。指出代码没有溢出，是第 97 行先把位数除以 8 再乘，与约定“先乘位数、再除以 8”的顺序不同，并解释约定按位计算的理由（safetensors 有不足一个字节的 dtype）；没有给出代码 | A5 中“乘位数这一步溢出返回 `None`”一项的独立性；已恢复：A9 在无提示下写出 `padded_bytes`（先 `checked_add` 再除再乘），首次提交 8 项全过（E-04） | 否 |
| 学习者问嵌套解构是什么、struct 能不能解构。用与练习无关的 `Size`、`Window` 和 `TensorInfo` 示范了 struct 解构与嵌套解构的写法，并指出 `Rectangle` 的两个字段都是 `Point`、冒号右边要写 `Point` 的模式；没有写出 `rect_area` 的代码 | A2 中“嵌套解构”一项的独立性；已恢复：A9 在无提示下把 `gpu_index` 写成一个 `match` 里的嵌套模式（E-04） | 否 |

## 条件片段：阶段事件

| 日期 | 覆盖范围 | 证明了什么 | 证据链接 | 标注 |
| --- | --- | --- | --- | --- |
| 2026-10-08 至 10-12 | E-01：开课导入；节点 1（标量类型与数值规则）、节点 2（元组）与检查；节点 3（数组与切片）、节点 4（struct）与检查；节点 5（enum 与 `match`）、节点 6（递归类型与 `Box`）与检查题发出 | 节点 1–2 检查（按 `(u32, u32)` 的起止偏移算字节数的函数，文件头不可信）：三问首答都对。指出止小于起时调试构建 panic、发布构建按补码回绕，后者更危险，因为得到错误的结果却没有报错；改法是用 `checked_*` 把溢出变成 `None` 再转成错误；把 `(usize, usize)` 传给要 `(u32, u32)` 的函数不能编译，`as u32` 会在偏移超出 `u32` 范围的大文件上出问题。两处补充，不构成差距：没有写出返回类型变成 `Option<u32>`；把 `as` 的截断说成“也可能导致溢出”，已补明它在两种构建下都不 panic，比算术溢出更隐蔽。随后讲节点 3、4，并发出节点 3–4 的检查题。节点 3–4 检查（把 `TensorView` 的 `data` 换成三种别的类型；Rust 默认布局的记录交给 C 读）：指出 `Vec<u8>` 要把约 1.09 GB 复制到堆上；拆成指针和长度两个字段就回到 C 的做法，两者是否匹配只能靠调用方；Rust 默认布局会重排字段，C 按声明顺序读会出错，而 Rust 自己读写用的是同一种布局所以测不出来；加 `#[repr(C)]` 后从 16 字节变成 24 字节。一处差距：对 `[u8; N]` 只说到长度写死、换模型会类型不匹配，没有说到同一个文件里 82 个张量大小各不相同、长度要到运行期才知道，也没有说到数组的值就是数据本身，1.09 GB 会装进 `TensorView` 里并被复制；已补讲，留到节点 6 的检查题（不加 `Box` 的递归类型为什么大小无限）复查。学习者追问胖指针多带的那个字是否总是长度，已答：它的含义由指向的类型决定，切片和 `str` 是元素个数，trait 对象是虚表指针。随后讲节点 5（enum 与 `match`）、节点 6（递归类型与 `Box`），图解页补入对应两节，发出节点 5–6 的检查题。 | 本会话；[当前证据](#当前证据)中的核对；[内存布局图解页](../attachments/02-data-shapes/memory-layout.html) | 无 |
| 2026-10-13 | E-02：节点 5–6 检查；节点 7（`const` 与 `static`）；导师串讲；综合验收；练习约定 P1 接受，验收测试建立 | 作答前学习者追问了七处，都已答复：`"héllo"` 的字节数与字符数、`Box` 是什么、枚举是否只能用 `match` 处理、标签不单独占字节的含义、`Option<u32>` 与 `Some` 是什么、`Box` 与 `&mut` 的区别、原主销毁时借用会怎样。其中 `Box` 与 `Option<T>` 两处是我在定义之前先用了名词。节点 5–6 检查（把带 `kind: u8` 的请求状态 struct 改写成 enum；三个递归或自引用的类型定义）：指出 struct 写法里每种状态都带着不属于它的字段，要靠约定的无效值和自觉的判断；写出四个变体的 enum，并说明读失败原因必须先判断变体，给出 `Failed(s) =>` 分支；新增状态时 struct 写法没有任何约束，逐个列出的 `match` 会被强制补上处理。第 2 题三个定义的能否编译都判断正确，理由是不加间接时载荷就是自身、大小无穷，加 `Box` 后大小由最大的变体决定而与树的深度无关，`Chunk` 是 1024 加 8 共 1032 字节，这一条同时关闭了“数组的值就是元素本身”的复查。三处补充：没有举出 `kind` 可以取 0–3 之外的值；对带 `_` 的 `match` 只说到“至少有兜底”，没有说到编译器不再提醒、兜底分支可能把新状态处理错；`Tree` 的大小算成 20 字节，漏了按对齐凑整（按规则是 24），实际因两个 `Box` 不会为 0 而没有单独的标签，是 16 字节。后两处放进综合验收复查。随后讲节点 7，沿 safetensors 读文件头到取出张量的过程做了导师串讲。综合验收三题：口述（C 的指针加长度、可空指针在 Rust 里对应什么）答出 `&[u8]` 是指针加长度两个字、`Option<&[u8]>` 借指针不为 0 表示 `None` 而仍是 16 字节、长度与地址绑定、“没有”不再靠约定；没讲过的 `TokenChunk`（`atom/mesh`）答出一个 `Partial` 也按最大变体占 188 字节并凑到对齐 8 的 192 字节、token id 在 `Vec` 指向的堆上、可以用 `Box` 换小而代价是堆分配、只在成为瓶颈时才值得改；带 `_` 的 `match` 在新增变体后编译器不提示、新变体被判成非正常结束、应当逐个列出，代价是代码更长；`static` 改 `const` 的预测题说出每次使用都是一份新的 `AtomicU64::new(0)`。“`_` 的代价”与“按对齐凑整”两处复查通过。三处补充，不构成差距：把代价说成“更多编译器检查”，实际是下标访问的运行期边界检查和必须写出的分支；用 `Box` 减小 enum 要针对最大的变体，把自定义类型的字段逐个装箱后是 136 字节，只装 `Partial` 里的字段则仍是 192 字节，把 `Complete` 的字段整体装箱是 48 字节（本机实测）；预测题的输出答成 1，漏了读取那一行也是一份新值，实际是 0。O1–O3 的理解证据充分，O4 仍缺实践证据，学习者追问整体装箱怎么写，已答（把字段搬进一个 struct，再让变体带一个指向它的 `Box`）。练习约定 P1 版本 1 展示后被接受。Agent 建立 crate 与验收测试：参考实现通过全部 29 项并通过 `cargo clippy --all-targets -- -D warnings`，19 个错误变体各至少被一项测试拦下；仓库内六个测试文件在骨架上都只因缺少对应的函数或类型而编译失败（E0432），即预期的失败。 | 本会话；[当前证据](#当前证据)中的核对；[练习约定](#条件片段练习约定) | 无 |
| 2026-10-13 | E-03：练习首次提交与四轮 Review；约定版本 2 接受；A8 通过，A9 发出 | 学习者提交 `src/lib.rs`。第一轮：29 项里 27 项通过，`a5_byte_len` 与 `a6_slice` 各一项失败，格式检查未通过，Clippy 11 条；学习者就 a5 的失败和嵌套解构各求助一次，见[帮助影响](#条件片段帮助影响)。第二轮：Agent 复验验收测试与 `Cargo.toml` 未被改动，29 项全部通过，`cargo fmt --check` 与 `cargo clippy --all-targets -- -D warnings` 通过，没有 `unwrap`、`expect`、`unsafe` 和 `#[allow]`，`match` 里没有 `_`；A1、A3、A4、A5、A7 按版本 1 通过。读代码发现两处，见[需要跟踪的问题](#条件片段需要跟踪的问题)：`rect_area` 没有用嵌套解构；`slice` 把位于缓冲区末尾的空张量也判成 `None`，而版本 1 的测试没有覆盖这个边界。两处都作为约定澄清提出了版本 2。学习者质疑嵌套解构这一要求的必要性，Agent 核对后把它从提议中撤回；学习者接受修订后的版本 2。第三轮：三项新测试加入后复验，32 项里 30 项通过，失败的是 F1 对应的两项；`cargo fmt --check` 因一处 `return None` 少了分号而未通过；Clippy 通过。原因是学习者的修改没有保存。第四轮：文件保存后复验，验收测试未被改动，32 项全部通过，格式检查与 Clippy 通过，没有 `unwrap`、`expect`、`unsafe` 和 `#[allow]`，`match` 里没有 `_`；A1–A7 按版本 2 通过，F1 关闭。A8：四种坏输入与代码的对应第一次写反了两项，学习者说明是复制粘贴出错；复查题（去掉 `start > end` 后输入 `(20, 10)` 会怎样）答出会走到 `end - start` 一行、`usize` 的小减大溢出、调试构建 panic、发布构建回绕成很大的数；`checked_mul` 换成 `*` 答出调试构建 panic、发布构建静默回绕。Agent 补充了回绕之后的后果（本机实测）：`byte_len` 返回错误的 `Some`，凑好的形状会被 `slice` 当成 3 字节接受；去掉 `start > end` 时发布构建下 32 项测试全部通过，是回绕出的数碰巧对不上。A8 通过。A9 发出：参考实现通过 `a9_placement` 的 8 项与 Clippy，12 个错误变体各至少被一项拦下，另外五种正确写法都能通过；仓库里该文件因找不到 `Placement` 而编译失败（E0432），即预期的失败。 | 本会话；`rust/lesson02_data_shapes/src/lib.rs`（未提交到 Git） | 无 |
| 2026-10-14 | E-04：A9 首次提交与复验；结课前答疑；结课 | 学习者在无提示下提交 `Placement`。Agent 复验验收测试与 `Cargo.toml` 未被改动；全套 40 项通过，其中 `a9_placement` 8 项首次提交即全部通过。读代码：`gpu_index` 是一个三分支的 `match`，用嵌套模式 `Placement::Loaded { device: Device::Cuda(index), … }` 同时判断两层，没有嵌套的 `match`、`_ =>` 和 `if let`，写法要求满足；`padded_bytes` 用 `checked_add(63)`、`checked_div(64)`、`checked_mul(64)`，没有会 panic 的运算。未通过的是格式检查（两处）与 Clippy（10 条：未使用的绑定 3 条、从未读取的初值 1 条、多余的 `return` 3 条、缺 `#[must_use]` 2 条、`size=*bytes` 的书写 1 条；最后一条格式化后消失），见 F3。没有 `unwrap`、`expect`、`unsafe` 和 `#[allow]`。学习者在无提示下修改后再次提交：验收测试与 `Cargo.toml` 未被改动；调试构建与发布构建下 40 项都全部通过；`cargo fmt --check` 通过；`cargo clippy --all-targets -- -D warnings` 在全新构建上通过；`gpu_index` 把两个返回 `None` 的情况用 `\|` 并成一个分支，仍是一个不带兜底分支的 `match`，用不到的字段写成 `bytes: _`；`padded_bytes` 改为 `let mut size = match … ;`。A9 通过，F3 关闭，两条帮助影响恢复。整个 workspace 的 `cargo fmt --all --check`、`cargo clippy --workspace --all-targets --locked -- -D warnings` 通过，`cargo test --workspace --locked` 62 项全部通过。练习约定 P1 的完成门槛达到，进入结课确认。等待确认期间学习者追问了几处，都已答复：变体用圆括号还是花括号；`&`、`*` 各在什么时候写（以 `byte_len` 为例，逐个对照了 `&self` 与 `self`、`in &self.shape` 与 `in self.shape`、`*s` 与 `s`）；`TensorInfo` 为什么不能 `Copy`；`Eq` 是什么；`data.get(start..end)` 与下标的区别。学习者说明这些是写练习时反复遇到的困惑，其中 `&` 与 `*`、`Copy` 的系统讲解在第 04、08、10 课，约定里只有零散的说明；这是练习设计的疏漏。学习者还指出 Rust 的简写多、令人迷惑，按其要求把简写对照表加进了[《Rust 基础知识》](../attachments/00-rust-basics/rust-basics.html)，同时补入本课的 35 个名词（共 84 个）。 | 本会话；`rust/lesson02_data_shapes/src/lib.rs`（未提交到 Git） | 练习关闭；结课 |

## 条件片段：需要跟踪的问题

| ID | 对应验收项或目标 | 严重度 | 状态 | 证据 |
| --- | --- | --- | --- | --- |
| F1 | O4、A6 | 阻塞 | 已关闭 | `slice` 对起止都等于 `data` 长度的空张量返回 `None`，约定的行为是返回空切片；`data` 为空、偏移 `(0, 0)` 时同样。版本 2 的三项测试已加入 `a6_slice.rs` 并自检：参考实现三项都通过，“空区间一律接受”的错误变体被第三项拦下。第三轮复验时磁盘上的文件还是旧条件，两项仍失败；学习者确认是没有保存。关闭证据：13:31 保存的 `src/lib.rs` 把第 107 行的 `start >= len` 改成 `start > len`，Agent 复验 `a6_slice` 12 项、全套 32 项全部通过，`cargo fmt --check` 与 `cargo clippy --all-targets -- -D warnings` 通过。 |
| F2 | O4、A2 | 非阻塞 | 已关闭（撤回） | `rect_area` 用字段访问取坐标，版本 1 的交付说明要求用嵌套解构；`transpose` 已改用元组结构体的解构。学习者质疑这一要求的必要性后，Agent 提议从约定中删去，证据改由 A9 取得；版本 2 被接受后撤回。 |
| F3 | O4、A9 | 阻塞 | 已关闭 | A9 的行为与写法要求已满足，但 2026-10-14 首次提交的 `src/lib.rs` 没有通过 `cargo fmt --check`（第 125–136 行两处）和 `cargo clippy --all-targets -- -D warnings`（10 条，都在 `impl Placement` 内）。关闭证据：01:27 保存的 `src/lib.rs` 经 Agent 复验，格式检查与全新构建上的 Clippy 通过，40 项测试全部通过。 |

## 条件片段：结课

| 目标 | 所需证据 | 证据链接 | 判断 |
| --- | --- | --- | --- |
| O1 | 理解 | [阶段事件](#条件片段阶段事件) E-01 的节点 1–2 检查；E-02 的综合验收 | 充分 |
| O2 | 理解 | E-01 的节点 3–4 检查；E-02 中“数组的值就是元素本身”的复查，以及综合验收的口述题 | 充分 |
| O3 | 理解 | E-01 的节点 3–4 检查（struct 的布局）；E-02 的节点 5–6 检查、综合验收的 `TokenChunk` 题与 `const` 预测题，以及“`_` 的代价”“按对齐凑整”两处复查 | 充分 |
| O4 | 理解、实践 | E-02 节点 5–6 检查中把请求状态建模成 enum 的一题；E-03、E-04 中[练习约定 P1](#条件片段练习约定) 版本 2 的 A1–A9 | 充分 |

- **未关闭的阻塞问题**：0。F1、F3 已复验关闭，F2 已撤回。
- **帮助影响是否已恢复**：已恢复，见[帮助影响](#条件片段帮助影响)与 E-04。
- **非阻塞余项**：
  - 代码里的四处观察都已向学习者说明，不要求修改：`bitsize(&self)` 与约定写的 `bitsize(self)` 不同；`Dtype`、`Device`、
    `TensorInfo`、`Placement` 的 derive 里没有 `Eq`；`slice` 手写的三个比较可以换成 `data.get(start..end)`；`padded_bytes`
    里除以常数 64 不会失败，`checked_div` 可以换成 `/`。
  - 带到后续课的起点：学习者在结课前说明，写练习时反复卡在三处，即变体用圆括号还是花括号、`&` 与 `*` 各在什么时候写、
    `TensorInfo` 为什么不能 derive `Copy`。三处都已讲了大概，并以 `byte_len` 为例逐个对照。第 04 课（模式里的 `&`、
    对着引用做 `match`、`for` 的三种遍历）、第 08 课（移动、借用、`Copy`）和第 10 课（`Clone`、`Eq`、derive）从这里接着讲，
    不默认学习者已经掌握。
  - 练习设计：本课约定对 `&`、`*` 只给了零散的说明。以后出练习前先写参考解法，把其中的每个符号和每个 derive 列出来，
    没有讲过的在约定里先给出最小的模型。
- **学习者确认**：2026-10-14，“接下来进行本次课程的结课吧。”
- **结课结论**：Lesson 02 关闭。学习者能从一个类型说出它的值占多少字节、哪些信息写在类型里、哪些带在值里；能解释 Rust 在
  数值运算、数组访问和“多选一”的数据上，各把 C 的哪种隐患变成了编译错误或确定的运行期行为，以及为此付出了什么；并独立
  用 struct、enum、元组和切片为一个小领域建模，用 `match` 和嵌套模式读出数据，处理了溢出与越界。
