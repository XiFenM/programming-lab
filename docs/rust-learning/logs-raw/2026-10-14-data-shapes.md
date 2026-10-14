---
archive_type: "study-log-visible-dialogue"
schema_version: 1
archive_id: "sl-d40bb91bac1a403d96b1919e0d582053"
status: "final"
title: "数据的形状：数值规则、切片、struct 与 enum 的布局、match 与 Box · 可追溯可见文本对话"
provider: "claude"
project_name: "programming-lab"
project_fingerprint: "7c4c768a8b0a"
source_session_id: "a955cb4c-7f49-5c49-b59d-1f2d1c81cadd"
source_file: "a955cb4c-7f49-5c49-b59d-1f2d1c81cadd.jsonl"
start_message_id: "msg-45fa89f9999ed560981d"
end_message_id: "msg-b4f6d6905240aaca01bf"
message_count: 94
source_sha256: "1458d2e42f5ec40d1781a86ca5350b452cd36910bf1b3f434966730870b4d41c"
visible_content_sha256: "e5db15be4ce54091884263087527aefd4705d46bd2fae7ac374cd1df8c5718b0"
target_precondition_sha256: null
first_message_at: "2026-10-08T13:55:25.469Z"
last_message_at: "2026-10-14T02:45:52.847Z"
created_at_utc: "2026-10-14T03:12:18.132310+00:00"
updated_at_utc: "2026-10-14T03:12:18.132310+00:00"
normalization: {"version":"study-log-visible-v1","client_context":"stripped","adjacent_duplicates":"removed","assistant_commentary":"included","tools":"excluded","attachments":"not_embedded"}
redaction: {"version":"study-log-redaction-v1","categories":[],"applications":[]}
privacy_risks: {"categories":["proprietary"],"counts":{"proprietary":65}}
structured_record: "docs/rust-learning/logs/2026-10-14-data-shapes.md"
message_phases: [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null]
migration: null
---

# 数据的形状：数值规则、切片、struct 与 enum 的布局、match 与 Box · 可追溯可见文本对话

> 此文件是规则化提取的“可追溯可见文本对话”，不是完整客户端 Session，也不代表已经匿名化。
> system、developer、reasoning、工具事件、客户端注入和附件正文默认不包含在内。

结构化学习记录：[查看记录](<../logs/2026-10-14-data-shapes.md>)

---

**001 · 用户** · `2026-10-08T13:55:25.469Z` · `msg-45fa89f9999ed560981d`

让我们开始rust的第2课吧。

---

**002 · 助手** · `2026-10-08T13:57:32.151Z` · `msg-4f0b17e33f7047841814`

先把第 02 课的来源和几个关键事实在本机核对一遍（类型大小、溢出、切片与 enum 的布局），再建课程记录并开讲。

---

**003 · 助手** · `2026-10-08T13:58:52.674Z` · `msg-3b4a108e1933ecf99e45`

本机核对基本完成，再取几处真实源码作对照（标准库、路由器项目、safetensors），随后建记录并开讲。

---

**004 · 助手** · `2026-10-08T13:59:29.519Z` · `msg-a183b485ff9cdb0a7539`

正在取 safetensors 的源码做“切片视图”的真实例子，之后就建记录、开讲。

---

**005 · 助手** · `2026-10-08T14:02:06.222Z` · `msg-771328c06d277f3439ee`

核对完成，最后确认在线页面地址，然后写课程记录并开讲。

---

**006 · 助手** · `2026-10-08T14:06:01.478Z` · `msg-97d8638f34a2cf38e0a7`

# 第 02 课：数据的形状

上一课解决的是怎样把一个值打印出来。这一课往下一层：值本身长什么样。它占几个字节，里面装着什么，哪些信息写在类型里、编译时就定了，哪些带在值里、运行时才知道。

C 在这件事上有个老问题：类型只管“这几个字节怎么解释”，很多关键信息不在类型里，要靠程序员记着。

- 数组传进函数就退化成指针，长度丢了。
- `union` 当前存的是哪个成员，靠另一个字段配合，编译器不管两者是否一致。
- 宽度、符号不同的整数混着算，编译器悄悄转换。

越界读写、把一种数据当成另一种读、算大小时溢出，都出在这里。Rust 把这些信息放回类型或值里，再让编译器检查：数组长度写进类型，切片随身带着长度，“多选一”的数据把标签和内容绑在一起，数值转换必须写出来。代价是多写转换和分支，运行时多了越界检查。本课每个节点看这笔交易的一个侧面。

## 贯穿案例：从权重文件里取出一个张量

safetensors 是 Hugging Face 上存模型权重的常用格式，参考实现用 Rust 写成。一个文件分三段：

```text
┌─────────┬─────────────────────┬──────────────────────────────────┐
│ 8 字节 N │ N 字节的文件头（JSON） │ 数据区：所有张量的字节首尾相接       │
└─────────┴─────────────────────┴──────────────────────────────────┘
```

真实例子是 Qwen2.5-7B-Instruct 的第一个分片：文件 3,945,441,440 字节，文件头 9,368 字节，登记了 82 个张量。第一条是 embedding 表：

```json
"model.embed_tokens.weight": {"dtype": "BF16", "shape": [152064, 3584], "data_offsets": [0, 1089994752]}
```

意思是 152,064 行（词表）× 3,584 列（隐藏维），每个元素 16 位，占数据区第 0 到第 1,089,994,752 字节（不含末尾）。

库把这一条读成 `TensorInfo`，校验后交给使用者一个 `TensorView`：

```rust
pub struct TensorInfo {
    pub dtype: Dtype,
    pub shape: Vec<usize>,
    pub data_offsets: (usize, usize),
}

pub struct TensorView<'data> {
    dtype: Dtype,
    shape: Vec<usize>,
    data: &'data [u8],
}

pub enum Dtype { BOOL, /* … */ F16, BF16, /* … */ F32, /* 共 22 个 */ }
```

`'data` 是生命周期标注，第 09 课讲；本课把 `&'data [u8]` 读成 `&[u8]` 即可。

## 路线

| 节点 | 讲什么 | 案例里的对应 | 教程页面 | 新名词 |
| --- | --- | --- | --- | --- |
| 1 | 标量类型与数值规则 | `usize`、`u8`，算字节数时的溢出 | 2 Primitives、2.1 Literals and operators | 标量、字面量与后缀、类型标注、`as`、溢出与回绕、`Option` |
| 2 | 元组 | `data_offsets: (usize, usize)` | 2.2 Tuples | 元组、解构 |
| 3 | 数组与切片 | `data: &[u8]` | 2.3 Arrays and Slices | 数组、切片、范围、胖指针 |
| 4 | struct | `TensorInfo`、`TensorView` | 3 Custom Types、3.1 Structures | 字段、单元结构体、对齐与填充、`repr(C)` |
| 5 | enum 与 `match` | `Dtype` | 3.2 Enums、3.2.1 use、3.2.2 C-like | 枚举、变体、判别值、`match`、类型别名、`Self` |
| 6 | 递归类型 | 案例之外：链表 | 3.2.3 Testcase: linked-list | `Box` |
| 7 | 常量 | — | 3.3 constants | `const`、`static` |

**教程在哪里**：共 11 页，都在仓库的 `docs/rust-by-example/src/` 下，即 `primitives.md`、`primitives/`、`custom_types.md`、`custom_types/`。同版本的在线入口是 <https://doc.rust-lang.org/1.97.1/rust-by-example/primitives.html> 和 <https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types.html>，在线页面的示例可以直接改、直接运行。不用课前通读，每个节点开头我会说读哪一页、先读还是后读。

**完成标准**：

- 对着上面那十来行代码，讲清每个字段的类型为什么这样选、占几个字节、哪些检查在编译期、哪些在运行期。
- 给一个没见过的类型定义，能判断它的大小，以及一段用它的代码能否编译。
- 亲手用这些类型建一个小模型并通过测试。练习在综合验收之后再约定。

记录在 `docs/rust-learning/lessons/02-data-shapes.md`。结课需要你确认，第 03 课不会自动开始。节点 3 起我会配一页内存布局的图解。上一课见过的词（`usize`、`()`、panic、`Result`、`?`）可查名词表 `docs/rust-learning/attachments/00-rust-basics/rust-basics.html`。

---

## 节点 1：标量类型与数值规则

**读哪里**：`docs/rust-by-example/src/primitives.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/primitives.html)）和 `primitives/literals.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/primitives/literals.html)）。建议看完下面的讲解再读：这两页是清单和示例，不解释原因。示例里的 `let mut`、“shadowing”和类型推断属于第 03 课，读到先跳过。

**结论**：标量就是单个的值，即一个整数、一个浮点数、一个字符或一个布尔值。类型决定它占几个字节、能表示哪些值、允许哪些运算。和 C 相比有两处关键差别：

- 不同数值类型之间没有隐式转换。
- 整数溢出不是未定义行为，而是有明确规定的程序错误。

### 清单

你熟悉的 NumPy／PyTorch dtype 是最贴切的对照：每个类型的位宽写在名字里，不随平台变。

| Rust | 字节 | C/C++ 的对应 | 说明 |
| --- | --- | --- | --- |
| `i8` `i16` `i32` `i64` `i128` | 1、2、4、8、16 | `int8_t` … `int64_t` | 有符号整数 |
| `u8` … `u128` | 同上 | `uint8_t` … | 无符号整数；`u8` 就是“字节” |
| `isize`、`usize` | 8（64 位机器） | `ptrdiff_t`、`size_t` | 和指针一样宽；长度、下标、偏移都用 `usize` |
| `f32`、`f64` | 4、8 | `float`、`double` | |
| `bool` | 1 | `bool` | 只有 `true`、`false`；整数不能当条件，`if n` 编译不过 |
| `char` | 4 | `char32_t` | 一个 Unicode 字符；C 的 `char` 对应的是 `u8` |
| `()` | 0 | 近似 `void` | 上一课见过 |

字面量是直接写在代码里的值，如 `42`、`1.5`、`'a'`。

- 后缀定类型：`1u32`、`2.5f32`。
- 不写后缀就按上下文推断，推不出来时整数取 `i32`、浮点取 `f64`。
- 可以写成 `0xff`、`0b1010`、`1_000_000`、`1e6`。
- 类型标注是变量名后加冒号写类型：`let n: u64 = 5;` 相当于 C 的 `uint64_t n = 5;`。

### 规则一：没有隐式转换

embedding 表有 152,064 × 3,584 = 544,997,376 个元素，每个 16 位，总位数是 8,719,958,016。`u32` 的上限是 4,294,967,295，元素个数放得下，位数放不下。

```rust
let numel: u32 = 544_997_376;
let nbits: u64 = numel * 16;   // 编译错误 E0308：expected `u64`, found `u32`
```

C 的同一行 `uint64_t nbits = numel * 16;` 能编译，`-Wall -Wextra` 下也没有警告。它先在 32 位里乘，溢出后才扩成 64 位，本机得到 130,023,424。Rust 拒绝这一行，你必须写出在哪个宽度里算：

```rust
let nbits: u64 = u64::from(numel) * 16;   // 先变宽再乘：8719958016
let nbits: u64 = numel as u64 * 16;       // 同样的结果
```

`as` 是显式转换，相当于 C 的强制类型转换。它总能编译，放不下时不报错：

- `300i32 as u8` 得 44（截断）。
- `-1i32 as u32` 得 4294967295。
- `1e10 as i32` 得 2147483647（浮点转整数时卡在上下限）。

`u64::from(x)` 只在不丢信息的方向上存在，方向写反了编译不过。这两者怎样选是第 03 课的内容，现在知道有这个区别就够。

### 规则二：溢出是程序错误，但行为是确定的

- **常量溢出**：`1u32 - 2` 直接是编译错误。
- **运行时才知道的值**：看是哪种构建。
  - **调试构建**是 `cargo build`、`cargo test` 的默认方式，不优化、带检查，相当于 C 的 `-O0 -g`。溢出时 panic，信息是 `attempt to multiply with overflow`。
  - **发布构建**是 `cargo build --release`，相当于 `-O3`。溢出时回绕：只留下低 32 位，等于对 2³² 取模。
- **想自己决定**：每种运算都有一组方法。
  - `checked_add`、`checked_sub`、`checked_mul` 返回 `Option`。
  - `wrapping_*` 明确要回绕。
  - `saturating_*` 卡在上下限。

`Option` 是标准库里表示“有或没有”的类型，值是 `Some(结果)` 或 `None`，相当于 C++ 的 `std::optional`，或 Python 里“返回值或 `None`”。它本身是个 enum，节点 5 再拆开看。

用 `u32` 算上面的位数（本机，`rustc x.rs` 对比 `rustc -O x.rs`）：

| 写法 | 调试构建 | 发布构建 |
| --- | --- | --- |
| `numel * 16` | panic | 130023424（真实值的约 1/67） |
| `numel.checked_mul(16)` | `None` | `None` |

### 为什么这样设计

**不做隐式转换**：C 的转换规则让“这一步在哪个宽度里算”从代码上看不出来。上面那行是一例；`-1 < 1u` 在 C 里为假是另一例，Rust 里拿 `i32` 和 `u32` 比较同样是 E0308。Rust 让每次变宽度、变符号都留在代码里，读的人能看到哪里可能丢信息。（规则来自编译器行为，动机是我的推断。）

代价是啰嗦，所以惯例是尽早统一成一种类型。`TensorInfo` 的 `shape` 和 `data_offsets` 全是 `usize`，因为它们最终要当下标用，而下标只接受 `usize`：拿 `u32` 做下标是 E0277。

**调试时检查、发布时不检查**：Rust Reference 把溢出定性为程序员的错误。

- 开了调试断言的构建必须检查并 panic。
- 其他构建由实现决定是 panic 还是回绕。
- 回绕时结果必须是确定的二进制补码。

Cargo 的默认值是 `dev` 开、`release` 关，省掉的是每次运算后的一次判断。和 C 的差别在于：C 的有符号溢出是未定义行为，编译器可以假设它不发生；Rust 里有符号、无符号同一条规则，没有未定义行为。

由此得到一个推论：默认的发布构建里，溢出是静默的。输入不可信、算的又是大小或偏移时，要用 `checked_*` 把溢出变成一个必须处理的值。

### 真实系统

safetensors 校验文件头时就是这样做的。文件是别人给的，`shape` 可以随便写：

```rust
let nbits = nelements
    .checked_mul(info.dtype.bitsize())
    .ok_or(SafeTensorError::ValidationOverflow)?;
```

读法：元素个数乘每个元素的位数，溢出就得到 `None`。`.ok_or(错误)` 把 `None` 换成一个错误，变成上一课的 `Result`，`?` 遇到错误就提前返回。它前面一步用同样的 `checked_mul` 把 `shape` 各维连乘成 `nelements`。

这里宽度和检查各管一半。64 位的 `usize` 让真实模型不会溢出。`checked_mul` 防的是恶意文件头，比如把 shape 写成两个 2⁴⁰。

**适用边界**：

- `as` 从不报错，只该用在确知放得下、或者本来就要截断的地方。
- `wrapping_*` 用在回绕本身是算法一部分的地方，例如哈希。
- 稳定版没有 `f16` 类型，写出来报 E0658。所以 `Dtype::F16`、`BF16` 只是标签，数据在 Rust 眼里是一串 `u8`。

**面试怎么讲**：“Rust 的整数类型宽度写在名字里，不同类型之间不做隐式转换，变宽变窄都要写出来。溢出不是未定义行为：调试构建 panic，发布构建默认按补码回绕。所以处理不可信输入的大小计算要用 `checked_*`，让溢出变成必须处理的 `None`。代价是代码里转换多，惯例是长度和下标统一用 `usize`。”

---

## 节点 2：元组

**读哪里**：`docs/rust-by-example/src/primitives/tuples.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/primitives/tuples.html)）。这页以示例为主，建议先读示例再看下面。页面末尾的 Activity 要用上一课的 `Display`，现在不做，留给练习。示例里的 `Matrix` 是上一课见过的元组结构体。

**结论**：元组把固定个数、类型可以不同的几个值捆成一个值，按位置访问。个数和每个位置的类型都写在类型里。

```rust
let offsets: (usize, usize) = (0, 1_089_994_752);
let start = offsets.0;          // 按位置取
let (start, end) = offsets;     // 解构：一次拆成两个变量
```

- **解构**是按形状把一个复合值拆开，同时声明几个变量。对应 C++17 的 `auto [start, end] = offsets;` 和 Python 的 `start, end = offsets`。
- **函数用它返回多个值**：教程里的 `fn reverse(pair: (i32, bool)) -> (bool, i32)`。
- **单元素元组**要写逗号，`(5u32,)`，和 Python 一样。`()` 是零个元素的元组。
- **与 Python 元组的差别**：`(usize, usize)` 和 `(usize, usize, usize)` 是两个不同的类型，不能混用。C++ 的对应是 `std::pair` 和 `std::tuple`。
- **布局**像一个没有字段名的 struct，成员怎么摆由编译器安排。本机 `(u8, u32, u8)` 占 8 字节，同样顺序的 C 结构体占 12 字节。原因在节点 4 讲。

**为什么有它，代价是什么**：临时把两三个值放在一起时，不必专门起一个类型名。代价是位置没有名字。`data_offsets: (usize, usize)` 是（起，止）还是（起，长度），从类型上看不出来，只能读注释和用法。所以成员有独立含义、或者多于两三个时，应该用带字段名的 struct。

**真实系统**：safetensors 的校验循环第一句就是解构，后面拿它和节点 1 算出的字节数 `size` 对账：

```rust
let (s, e) = info.data_offsets;
// …
if e - s != size {
    return Err(SafeTensorError::TensorInvalidInfo);
}
```

embedding 表这一条是 1,089,994,752 − 0，等于 544,997,376 × 16 ÷ 8，对得上。

**适用边界**：标准库只给不超过 12 个元素的元组实现了 `Debug` 等 trait。教程里注释掉的 13 元素元组用 `{:?}` 打印会报 E0277。

---

## 检查题（节点 1–2）

同事写了一个函数，根据文件头里的 `data_offsets` 算一个张量占多少字节。`offsets` 是（起，止），单位字节，来自外部文件，不可信：

```rust
fn byte_len(offsets: (u32, u32)) -> u32 {
    let (start, end) = offsets;
    end - start
}
```

1. 有人把文件头改成 `"data_offsets": [100, 40]`。这个函数在调试构建和发布构建下各会发生什么？对调用它的程序来说哪一种更危险，为什么？
2. 你会怎么改这个函数，让两种构建下行为一致，调用方又没法忽略这个问题？返回类型会变成什么？
3. 调用方手里是 `TensorInfo`，偏移的类型是 `(usize, usize)`。直接写 `byte_len(info.data_offsets)` 能编译吗？如果把两个偏移各用 `as u32` 转一下再传进去，会引入什么风险，在什么样的文件上出现？

用自己的话答，不需要算出具体数字。

---

**007 · 用户** · `2026-10-09T10:57:38.673Z` · `msg-32a6172bdcb9c6620fa4`

1. u32的40-100会发生溢出。在调试构建下会panic，发布构建就会按补码回绕。对调用它的程序来说，发布构建的补码回绕更危险，因为会得到异常的结果，且没有报错。
2. 对于不可信的外部输入，需要用checked_函数来包装这个减法计算。当溢出时返回None，处理None转为报错信息。
3. 不能编译，这二者数据类型不匹配。as u32是强制类型转换，也可能导致溢出。原本范围更大的usize转成范围小的u32。会在offset超过u32范围的大文件中出现。

---

**008 · 助手** · `2026-10-09T11:01:59.084Z` · `msg-2c1d56db9af382eee17e`

页面素材齐了，正在写内存布局图解页，之后验证、发布并接着讲节点 3–4。

---

**009 · 助手** · `2026-10-09T11:06:11.223Z` · `msg-4e7e07c8eb9203af5dd6`

**节点 1–2 检查：通过。** 三问方向都对，补两处。

- **第 2 问的返回类型**是 `Option<u32>`：

  ```rust
  fn byte_len(offsets: (u32, u32)) -> Option<u32> {
      let (start, end) = offsets;
      end.checked_sub(start)
  }
  ```

  调用方拿到的不再是 `u32`，不把 `Option` 拆开就用不了里面的数，所以没法忽略。safetensors 的真实代码用的是等价的另一种写法，先比较再减：`if s != start || e < s { return Err(…InvalidOffset…) }`，之后的 `e - s` 就不可能溢出。

- **第 3 问里 `as` 的截断不归溢出检查管。** 它在调试构建里也不 panic，两种构建都静默截断。所以它比第 1 问的减法更隐蔽：减法至少会在测试里炸，`as` 连测试都不报。出现条件是偏移达到 2³²，也就是超过 4 GiB 的文件。

接下来两个节点配了一页可以动手改的图解：<https://claude.ai/artifact/UAdb78pBPSLcVT9FtHqVuB>（仓库里是 `docs/rust-learning/attachments/02-data-shapes/memory-layout.html`）。

---

## 节点 3：数组与切片

**读哪里**：`docs/rust-by-example/src/primitives/array.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/primitives/array.html)）。建议先读页面开头两段文字，它们就是数组和切片的定义；再看下面的讲解；最后读示例。示例里有三样还没讲：

- `for i in 0..n` 是循环，`i` 从 0 走到 n−1（第 04 课）。
- `match … { Some(x) => …, None => … }` 是按 `Option` 的两种情况分别处理（节点 5）。
- `mem::size_of_val(&xs)` 返回一个值占的字节数，相当于 C 的 `sizeof`。

**结论**：数组 `[T; N]` 的长度写在类型里，值就是 N 个元素本身。切片 `&[T]` 是借来的一段连续元素，长度不在类型里，和指针一起带在值里。一个切片值是两个机器字：指针和长度。

### 名词

- **数组**：`[i32; 5]`，对应 C 的 `int xs[5]`、C++ 的 `std::array<int, 5>`。`[0; 500]` 是 500 个 0。
- **切片**：`&[i32]`，对应 C 里手工传的 `(const int *p, size_t n)`、C++20 的 `std::span<const int>`、NumPy 的视图 `a[1:4]`。
- **范围**：`1..4` 是 1、2、3，不含 4，和 Python 的 `1:4` 一样。`..2`、`4..`、`..` 是省掉一端或两端。
- **胖指针**：比普通指针多带一个字的指针。`&i32` 占 8 字节，`&[i32]` 占 16 字节。

### 机制

```rust
let xs: [i32; 5] = [1, 2, 3, 4, 5];   // 栈上 20 字节，起始地址记作 p
let s: &[i32] = &xs[1..4];            // 两个字：指针 p + 4，长度 3
```

```text
地址    p      p+4    p+8    p+12   p+16
      ┌──────┬──────┬──────┬──────┬──────┐
xs    │  1   │  2   │  3   │  4   │  5   │   [i32; 5]，20 字节
      └──────┴──────┴──────┴──────┴──────┘
               ▲
      ┌────────┴──┬──────────┐
s     │ 指针 p+4   │ 长度 3    │               &[i32]，16 字节
      └───────────┴──────────┘
```

- `s.len()` 就是读第二个字。
- `s[i]` 先比较 `i < 长度`，不成立就 panic，成立才去读 `指针 + 4×i`。
- `s.get(i)` 不 panic，返回 `Option`：`Some(&元素)` 或 `None`。
- 对数组用常量下标越界，直接是编译错误。

和节点 1 有一处重要差别：**越界检查在发布构建里也不关**，本机 `-O` 构建越界照样 panic。溢出只是算错一个数；越界读写会碰到不属于你的内存，这是 Rust 承诺安全代码里绝不发生的事。

### 为什么是指针加长度

要解决的问题是：一个函数想处理任意长度的一段元素。

- **长度留在类型里不行。** `fn sum5(a: [i32; 5])` 只收恰好 5 个元素，传 `[i32; 4]` 是 E0308。每种长度是一个不同的类型。
- **C 的做法是丢掉长度。** 数组传参退化成指针。本机 `sizeof(xs)` 在 `main` 里是 20，在被调函数里是 8；把只有 4 个元素的数组传给 `sum5` 能编译，运行时读到了数组之外。长度靠另一个参数传，两者对不对得上没人检查。
- **Rust 把那对 `(指针, 长度)` 做成一个值。** 长度永远跟着指针，所以每次下标访问都有东西可比。
- **切片只看不拥有，取子切片不复制。** `&xs[1..4]` 只算出一个新指针和一个新长度。

代价是引用占 16 字节而不是 8，每次按下标访问多一次比较。`for x in s` 这样逐个遍历不经过下标，没有这次比较：标准库的切片迭代器存的就是头尾两个指针。

### 数组、`Vec`、切片

| | 长度何时确定 | 值里是什么 | 拥有数据吗 |
| --- | --- | --- | --- |
| `[T; N]` | 编译期，写在类型里 | 元素本身 | 是，元素就在值里 |
| `Vec<T>` | 运行期，可以增长 | 指针、容量、长度，24 字节 | 是，数据在堆上；从别处的数据造一个就要复制 |
| `&[T]` | 运行期 | 指针、长度，16 字节 | 否，借别人的 |

函数参数写成 `&[T]`，数组和 `Vec` 都能传进来。教程里的 `analyze_slice(&xs)` 就是 `&[i32; 5]` 自动变成 `&[i32]`。节点 1 说的“不做隐式转换”指数值之间；这里只是把长度从类型搬进值，不丢信息。上一课的 `&str` 是同一个结构：指针加字节数。

### 真实系统

safetensors 取出一个张量的那一行：

```rust
data: &self.data[info.data_offsets.0..info.data_offsets.1],
```

元组的 `.0`、`.1`，范围，切片，都在这一行里。对 embedding 表就是 `&self.data[0..1089994752]`：一个 16 字节的值，指针指向数据区开头，长度 1,089,994,752。1.09 GB 的权重一个字节都没复制。库文档里的用法是把整个文件 mmap 进内存再交给它，所以这段数据甚至还没从磁盘读进来。

`shape` 用 `Vec<usize>`，是因为另外两种都不合适：

- 每个张量的维数不同，运行时才知道，所以不能是数组。
- `TensorInfo` 要自己保存从 JSON 解析出的形状，所以不能是借来的切片。

**适用边界**：

- 切片只能表示连续的一段。步长视图 `a[::2]` 和多维视图它表示不了，NumPy 的视图为此多带了 strides。
- 切片不能比它看的数据活得更久，这由 `'data` 那个生命周期保证（第 09 课）。

**面试怎么讲**：“切片是一个胖指针：指向首元素的指针加元素个数。数组的长度在类型里，所以函数没法用一个类型接收任意长度。C 的解法是退化成指针、把长度丢掉，越界就没人管。Rust 把指针和长度绑成一个值，每次下标访问都能检查，取子切片只是算新的指针和长度，不复制。代价是引用宽一倍，下标访问多一次比较。”

---

## 节点 4：struct

**读哪里**：`docs/rust-by-example/src/custom_types.md`（8 行，一眼看完）和 `custom_types/structs.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/structs.html)）。建议先读示例再看下面。示例第一行的 `#![allow(dead_code)]` 是一个属性，作用是关掉“这段代码没被用到”的警告。末尾的 Activity 留给练习。

**结论**：struct 把几个值捆成一个有名字的新类型。三种写法只差在字段有没有名字。内存里就是字段挨着放、按对齐补空。和 C 不同的是，默认情况下字段的摆放顺序由编译器决定。

### 三种写法

| 写法 | 例子 | 取字段 | 用在哪里 |
| --- | --- | --- | --- |
| 带字段名 | `struct Point { x: f32, y: f32 }` | `p.x` | 常规情况，对应 C 的 struct |
| 元组结构体 | `struct Pair(i32, f32);` | `p.0` | 字段含义一目了然，或者只包一个值来得到一个新类型 |
| 单元结构体 | `struct Unit;` | 没有字段 | 0 字节，只需要一个类型名的时候（第 07 课会用到） |

### 构造与读取

- **构造必须写全。** `Point { x: 5.2, y: 0.4 }` 漏一个字段是 E0063，不存在未初始化的字段。
- **同名简写**：变量名和字段名相同时，`Person { name, age }`。
- **更新语法**：`Point { x: 10.3, ..another_point }`，没写的字段取自另一个值。
- **解构**：`let Point { x: left_edge, y: top_edge } = point;`，和元组解构同理，按字段名对应。
- **嵌套是内嵌。** `Rectangle` 里的两个 `Point` 直接挨着放，共 16 字节，中间没有指针。这和 C 一样，和 Python 的对象引用不同。

### 布局

对齐指一个类型的值的地址必须是某个数的倍数，`u32` 是 4。填充是为满足对齐而空出的字节。这两个概念和 C 里一样。

对 `struct Plain { a: u8, b: u32, c: u8 }`，本机：

| 摆法 | 偏移 | 大小 |
| --- | --- | --- |
| C，或 Rust 加 `#[repr(C)]` 属性 | a 在 0，b 在 4，c 在 8 | 12 字节 |
| Rust 默认 | b 在 0，a 在 4，c 在 5 | 8 字节 |

**为什么敢重排**：C 的字段顺序是和外界的约定，别的编译单元、别的语言都按同一个布局读，编译器不能动。Rust 默认不做这个承诺，Reference 只保证字段不重叠、各自对齐。换来的是编译器可以排得更紧。

代价有两条：

- 默认布局的 struct 不能直接交给 C。
- 不能把内存里的字节原样写进文件，再指望别的程序读回来。

需要固定布局时加 `#[repr(C)]`。重排也不一定省空间：`TensorView` 两种排法都是 48 字节，图解页第三节可以切换着看。

### 真实系统

- **标准库的 struct 很朴素。** `String` 是 `struct String { vec: Vec<u8> }`，`Ipv4Addr` 是 `struct Ipv4Addr { octets: [u8; 4] }`。
- **只包一个值的元组结构体**叫 newtype。上一课的 `WorkerId(u32)` 占 4 字节，和 `u32` 一样大，但类型不同，不会和别的 `u32` 混用。
- **字段是否公开是设计的一部分。** `TensorInfo` 的三个字段都标了 `pub`，`TensorView` 的一个都没标。
  - 没标 `pub` 的字段，库外面的代码读不到，也没法直接构造。
  - 外部只能通过 `TensorView::new(dtype, shape, data)` 得到一个值，`new` 会检查 `data` 的长度和 dtype、shape 对得上，对不上就返回错误。
  - 所以拿到 `TensorView` 的人可以相信三个字段是一致的。
  - `TensorInfo` 是文件头的原样记录，要等校验后才可信；它全部公开与此有关，这一句是我的推断。

  可见性规则在第 06 课系统讲。

**适用边界**：Rust 默认布局不是语言的承诺，上面的偏移是 1.97.1 上的实测，换个编译器版本可能不同。

---

## 检查题（节点 3–4）

**第 1 题。** `TensorView` 的 `data` 字段现在是 `&[u8]`。假设改成下面三种之一，各会失去什么，或者多付出什么？以约 1.09 GB 的 embedding 表为例说。

- (a) `Vec<u8>`
- (b) 拆成两个字段：`ptr: &u8` 和 `len: usize`
- (c) `[u8; 1089994752]`

**第 2 题。** 同事想给文件头换一种二进制格式，每个张量一条定长记录：

```rust
struct Record {
    dtype: u8,
    start: u64,
    flag: u8,
}
```

写文件的 Rust 程序把 `Record` 在内存里的字节原样写出去。读文件的是一个 C 程序，在同一台 64 位 Linux 机器上，按 `struct { uint8_t dtype; uint64_t start; uint8_t flag; }` 的布局读。

1. 会出什么问题？为什么 Rust 这边自己写、自己读的测试发现不了？
2. 怎么修？修完之后这个 struct 变大还是变小，为什么？

说方向和原因即可，不要求算出具体字节数。

---

**010 · 用户** · `2026-10-12T04:00:20.279Z` · `msg-2450b13b0da7ae696c41`

检查题回答：第一题：1. Vec的数据在堆上，从权重文件中读取就会导致复制一份到堆上。对于1.09GB的embedding来说开销很大。2. 拆成两个字段就变成和C的做法一样，长度靠另一个参数传递。但这个长度和指针之间二者是否传的匹配，就只能看调用方了。TensorView无法检查二者匹配。3. 这样就写死了长度，如果换一个模型，长度变了就会类型不匹配报错。第二题：1. C程序读取的数据会出问题，因为Rust的默认布局会调整struct中的元素布局，使其尽可能省空间。在本例中Record中的start很可能会被排到开头，然后再排dtype和flag。这就导致C程序按照dtype、start、flag的顺序读取就会出现问题。Rust自己这边一直按照自己定义的顺序读和写，当然不会有问题。2. 可以加上#[repr(C)]的标签使其固定布局。修完之后，这个struct会变大，因为dtype和flag对齐到8字节，变成一共3*8=24字节；原本是8+8=16字节。我还有一个问题：胖指针多带的一个字就是长度吗？还是说这里的切片将多带的一个字定义为了长度，而不是每个胖指针多带的一个字都是长度？

---

**011 · 助手** · `2026-10-12T04:03:37.163Z` · `msg-ea3f3076e86b6fd8de39`

实测数据齐了，再核对一处（`#[non_exhaustive]`），然后补图解页的 enum 与链表两节，接着讲节点 5–6。

---

**012 · 助手** · `2026-10-12T04:05:57.422Z` · `msg-529d047c9041c9ad62ae`

图解页已更新，正在更新课程记录，然后给出讲解。

---

**013 · 助手** · `2026-10-12T04:09:58.727Z` · `msg-18a7160c822873723b89`

**节点 3–4 检查：通过。** 第 1 题的 (a)(b) 和第 2 题都对，24 和 16 两个数与本机实测一致。补两处。

- **(c) 只答到一半。** 长度写死在类型里是对的，但问题比“换模型”来得更早，还漏了更重的一条：
  - 同一个文件里 82 个张量大小各不相同，而且读完文件头才知道。数组长度必须是编译时的常数，所以一个 `TensorView` 定义没法同时描述它们。
  - 数组的值就是元素本身。`[u8; 1089994752]` 做字段，意味着这 1.09 GB 就装在 `TensorView` 这个值里。造它要把数据复制进来，这个值本身也有 1.09 GB，本机 8 MB 的栈放不下。

  “值就是数据本身，中间没有指针”这一条，节点 6 马上要用。
- **(b) 可以说得更重。** `&u8` 是指向一个字节的引用，安全代码里根本没法拿它去读后面的字节，不只是没人检查。

## 你的问题：胖指针多带的那个字

**不总是长度。它是什么，由指针指向的类型决定。** 切片缺的正好是长度，所以带的是长度。

规则是这样的：一个类型的大小如果编译时就知道，指向它的指针一个字就够，比如 `&u8`、`&[i32; 5]`。大小要到运行时才知道的类型，指针得把缺的那份信息带上，变成两个字。Rust Reference 列了三种：

| 指向的类型 | 多带的字 | 本机实测 |
| --- | --- | --- |
| `[T]`，切片 | 元素个数 | `&xs[1..4]` 是 3 |
| `str`，字符串切片 | 字节数 | `"héllo"` 是 6，而它只有 5 个字符 |
| `dyn Trait` | 虚表的地址 | 两个 `i32` 值带的是同一个地址，换成别的类型就是另一个地址 |

第三种是第 10 课的内容。`dyn Display` 的意思是“某个实现了 `Display` 的类型，具体是哪个运行时才知道”，对应 C++ 里通过基类指针调用虚函数。虚表就是 C++ 的虚函数表，记着这个具体类型的各个方法在哪里。差别在放的位置：C++ 把虚表指针放在每个对象的开头，Rust 把它放在指针里。所以一个 `i32` 平时还是 4 字节，不用为了能被这样调用而多存一个指针。

`Box` 也遵守同一条规则：`Box<u8>` 是 8 字节，`Box<[u8]>` 和 `Box<dyn Display>` 都是 16 字节。标准库把这个字统一叫 metadata，切片的 `len()` 实现只有一行 `ptr::metadata(self)`。

（来源：Rust Reference 1.97.1 的 Dynamically Sized Types 一节；标准库 `core/src/ptr/metadata.rs`。）

图解页补了 enum 和链表两节：<https://claude.ai/artifact/UAdb78pBPSLcVT9FtHqVuB>

---

## 节点 5：enum 与 `match`

**读哪里**：三页，都在 `docs/rust-by-example/src/custom_types/` 下。

- `enum.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/enum.html)），主体。
- `enum/enum_use.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/enum/enum_use.html)），很短。
- `enum/c_like.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/enum/c_like.html)），很短。

建议先看下面的“名词”和“怎样用”，再读 `enum.md` 的第一个示例，然后扫另外两页。示例里的 `"my text".to_owned()` 是从字面量造出一个 `String`。

**结论**：enum 定义一个“几选一”的类型。它的值在任一时刻恰好是其中一个变体，每个变体可以带自己的数据。内存里是标签加载荷。和 C 的差别是标签与载荷绑死：要读数据，必须先用 `match` 判断是哪个变体，编译器还会检查你把所有变体都处理了。

### 名词

- **变体**：enum 的每一个选项。`enum Device { Cpu, Cuda(u32) }` 有两个。
- **载荷**：变体带的数据。写法和 struct 的三种一一对应：
  - 不带数据：`PageLoad`
  - 像元组结构体：`KeyPress(char)`
  - 带字段名：`Click { x: i64, y: i64 }`
- **标签**：记录“现在是哪个变体”的整数。教程和编译器叫它 discriminant（判别值）。
- **`match`**：按值的形状分支。相当于 C 的 `switch`，但每个分支能顺手把载荷拆出来。
- **对照**：
  - C 的 `enum` 只有标签，带数据要自己配一个 `union`。
  - C++ 是 `std::variant`。
  - Python 3.10 的 `match … case` 语法上最像，但不检查有没有漏。

### 怎样用

构造时变体名前带类型名：`let e = WebEvent::KeyPress('x');`。读取只能用 `match`：

```rust
match event {
    WebEvent::PageLoad => println!("page loaded"),
    WebEvent::PageUnload => println!("page unloaded"),
    WebEvent::KeyPress(c) => println!("pressed '{}'.", c),   // c 是载荷里的那个 char
    WebEvent::Paste(s) => println!("pasted \"{}\".", s),
    WebEvent::Click { x, y } => println!("clicked at x={}, y={}.", x, y),
}
```

1. **每个分支是 `模式 => 表达式`。** 模式写的是值的形状。里面的名字（`c`、`x`、`y`）在匹配成功时绑到载荷上，只在这个分支里可用。这就是节点 2、4 的解构，用在了分支上。
2. **必须穷尽。** 漏一个变体是编译错误 E0004：``non-exhaustive patterns: `WebEvent::PageUnload` not covered``。`_ => …` 是兜底分支，匹配其余所有情况。
3. **`match` 是表达式，有值。** 一个函数体可以整个就是一个 `match`。

绕开 `match` 直接取载荷不行：`e.0` 报 E0609。

### 内存里

图解页“enum”一节可以逐个切换着看字节。

| 类型 | 字节 | 怎么放 |
| --- | --- | --- |
| `Device { Cpu, Cuda(u32) }` | 8 | 标签 4 + 载荷 4。`Cuda(3)` 是 `01 00 00 00 03 00 00 00` |
| `Option<u32>` | 8 | 同上。`u32` 的每种取值都有意义，标签只能另占地方 |
| `Option<&i32>`、`Option<Box<T>>` | 8 | 引用和 `Box` 不会是 0，编译器用 0 表示 `None`，不占额外空间 |
| `WebEvent` | 24 | 和最大的变体 `Paste(String)` 一样大，标签藏在 `String` 用不到的取值里 |
| `Number { Zero, One, Two }` | 1 | 只有标签 |

规律是：大小等于最大的变体加标签，再按对齐凑整。编译器找得到永远不会出现的取值时，就把标签藏进去。

`Option` 本身就是一个普通的 enum，标准库里是 `pub enum Option<T> { None, Some(T) }`。节点 1 的 `checked_mul`、节点 3 的 `get` 返回的都是它。

### 不带数据的 enum（`c_like.md`）

所有变体都不带数据时，enum 就是一个整数，和 C 的枚举一样。

- **默认从 0 开始**：`Number::One as i32` 是 1。
- **可以自己指定**：`enum Color { Red = 0xff0000, … }`，`Color::Red as u32` 是 0xff0000。
- **只能单向转**：enum 转整数用 `as`；整数转 enum 不行，`1i32 as Number` 是 E0605，因为不是每个整数都对应一个变体。

### `use` 与别名（`enum_use.md`，以及 `enum.md` 的 Type aliases 小节）

- **`use Stage::{Beginner, Advanced};` 或 `use Role::*;`** 之后可以直接写 `Beginner`，不带类型名。对应 C++20 的 `using enum`。
- **`type Operations = 很长的名字;`** 是类型别名，对应 C 的 `typedef`。它只是同一个类型的另一个名字，可以互换。这和节点 4 的 newtype 正相反：`type Km = f64;` 的值能直接当 `f64` 用，`struct Meters(f64);` 的不行。
- **`Self`** 在 `impl` 块里指正在实现的这个类型，所以能写 `Self::Add`。

### 为什么这样设计

C 的“标签加联合”有三个洞，本机用 gcc 13.3 都试了：

1. **标签和载荷可以不一致。** 把标签改成“点击”，载荷还是按键 `'x'`，读出来是 `clicked at x=120, y=0`。120 是 `'x'` 的 ASCII 码。没有任何警告。
2. **`switch` 漏分支只有警告。** 要开 `-Wall` 才有，不开什么都没有。
3. **任何整数都能当枚举值。** `enum Kind k = 42;` 能编译。

Rust 逐个堵上：载荷只能在 `match` 的对应分支里拿到；漏分支是编译错误；整数不能 `as` 成 enum。

穷尽性检查最大的用处在改代码的时候。给 enum 加一个变体，所有逐个列出变体的 `match` 都会报错，等于编译器给了一张“还有哪些地方要改”的清单。

代价有两条：

- **每个值按最大的变体占空间。** 一个 `PageLoad` 也是 24 字节。
- **`_` 会把那张清单关掉。** 本机给 enum 加一个变体后，逐个列出的 `match` 报 E0004，带 `_` 的照常编译，新变体被悄悄归进“其余”。

和 C++ 比，`std::variant` 也把标签和载荷绑在一起。

- **漏分支**：`std::visit` 漏了同样编译不过，报的是一长串模板错误。
- **取错成员**：`std::get<Paste>` 取错了，要到运行时才抛 `bad_variant_access`。
- **大小**：本机 `std::variant<PageLoad, KeyPress, Paste>` 是 40 字节，比最大的成员 `std::string` 多 8 字节；Rust 的 `WebEvent` 和它最大的成员一样大。

### 真实系统

**safetensors 的 `Dtype`** 有 22 个变体，都不带数据，占 1 字节。`bitsize` 是一个 22 个分支、没有 `_` 的 `match`：

```rust
pub fn bitsize(&self) -> usize {
    match self {
        Dtype::F4 => 4,
        // …
        Dtype::BF16 => 16,
        Dtype::F32 => 32,
        // …
    }
}
```

以后加一种 dtype 而忘了写位数，库自己就编译不过。

它的定义上还有一个属性 `#[non_exhaustive]`，意思是这个 enum 以后还会加变体。效果是库外的代码对它做 `match` 时必须写 `_`，本机不写报 E0004；库内不受影响。这样库加新 dtype 不会让使用者的代码编译失败。它把上面那个取舍按库内、库外分开处理了。

**带数据的 enum** 在路由器项目 `atom/mesh` 里很多，全目录有 60 个 enum：

```rust
pub enum WorkerType {
    Regular,
    Prefill { bootstrap_port: Option<u16> },
    Decode,
}
```

只有 Prefill worker 才有 bootstrap 端口，所以端口放在 `Prefill` 变体里，而不是给所有 worker 一个可能没用的字段。

标准库里，`Ordering` 是不带数据的：`enum Ordering { Less = -1, Equal = 0, Greater = 1 }`。`IpAddr` 带数据：`enum IpAddr { V4(Ipv4Addr), V6(Ipv6Addr) }`。

**适用边界**：标签取什么值、藏在哪里是编译器的选择，上面的字节是 1.97.1 上的实测。enum 的变体集合是封闭的，库外的人不能给它加变体；要开放扩展用 trait（第 10 课）。

**面试怎么讲**：“Rust 的 enum 是带标签的联合，每个变体可以带自己的数据，内存里是标签加最大变体那么大的空间。它比 C 的枚举多了数据，比 C 的 union 多了保证：数据只能在 `match` 的对应分支里取到，`match` 必须穷尽，整数也不能随便转成 enum，所以不会把一种数据当成另一种读。代价是每个值按最大变体占空间，写 `_` 兜底会放弃‘加变体时编译器提醒我’这项好处。`Option` 就是这样一个 enum，对引用和 `Box` 不占额外空间。”

---

## 节点 6：递归类型与 `Box`

**读哪里**：`docs/rust-by-example/src/custom_types/enum/testcase_linked_list.md`（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/enum/testcase_linked_list.html)）。建议先看下面再读示例。这个示例很短，但一下子用了好几样没讲过的写法，我逐个交代。

**结论**：类型里要包含“自己”时不能直接内嵌，必须隔一层指针。`Box<T>` 就是这层指针：它指向堆上的一个 `T`，并且独占它。

**`Box<T>`** 是 8 字节的指针。`Box::new(v)` 在堆上分配空间，把 `v` 放进去；这个 `Box` 不再使用时，堆上的值自动释放。对应 C++ 的 `std::unique_ptr<T>`，C 里是 `malloc` 加手工 `free`。

```rust
enum List {
    Cons(u32, Box<List>),   // 一个元素，加上指向剩余部分的指针
    Nil,                    // 链表结束
}
```

`Cons` 和 `Nil` 这两个名字来自 Lisp，意思是“一个节点”和“空”。

### 为什么必须有 `Box`

前面说过，Rust 的值就是数据本身：数组的值是元素本身，struct 嵌套是直接内嵌。enum 的载荷也放在值里面。

- **不加 `Box`**：写成 `Cons(u32, List)`，一个 `List` 里就要放下另一个完整的 `List`。大小 = 4 + 它自己的大小，无解。编译器报 E0072：``recursive type `List` has infinite size``，并建议插入 `Box`。
- **加 `Box`**：里面放的是 8 字节的指针，大小和它指向什么无关。标签 4 + 元素 4 + 指针 8 = 16 字节。

C 也一样：`struct Node { uint32_t v; struct Node next; };` 编译不过，必须写成 `struct Node *next`。差别是 C 的指针可以为空、可以悬空、要手工释放；`Box` 一定指向一个有效的值，释放是自动的。

### 示例逐段读

文件开头的 `use crate::List::*;` 让 `Cons`、`Nil` 不用带 `List::` 前缀，`crate` 指当前这个 crate。

```rust
fn prepend(self, elem: u32) -> List {
    Cons(elem, Box::new(self))
}
```

参数是 `self` 而不是 `&self`：这个方法把原来的链表整个拿走，调用之后原变量不能再用。所以 `main` 里写的是 `list = list.prepend(1);`，拿走旧的，放回新的。它做两件事：`Box::new(self)` 把旧的头节点搬到堆上，再造一个新的头节点指向它。图解页最后一节可以一步步点。

```rust
fn len(&self) -> u32 {
    match *self {
        Cons(_, ref tail) => 1 + tail.len(),
        Nil => 0
    }
}
```

- **`&self`**：只是借来看，不拿走。
- **`*self`**：`self` 是引用，`*` 取出它指向的那个 `List` 来匹配，相当于 C 的 `*p`。
- **`_`**：这个位置有值，但我不用，不起名字。
- **`ref tail`**：让 `tail` 成为指向载荷的引用，而不是把载荷拿走。整个链表是借来的，不能拿走它的一部分。
- **`tail.len()`**：对剩下的部分递归。

教程的注释里也说了，现在可以直接写 `match self { Cons(_, tail) => 1 + tail.len(), Nil => 0 }`，编译器自动按引用处理。两种写法等价，新代码用后一种。`stringify` 的结构和 `len` 相同。

本机运行输出 `linked list has length: 3` 和 `3, 2, 1, Nil`。内存里，头节点 `Cons(3, …)` 在栈上的变量 `list` 里；`Cons(2, …)`、`Cons(1, …)` 和末尾的 `Nil` 各是堆上一个 16 字节的节点。

### 取舍与真实系统

`Box` 的代价是一次堆分配，访问时多跳一次。换来的是大小固定，以及被指的东西可以很大而指针很小。所以它的另一个常见用途是给 enum 减肥，对付节点 5 说的“按最大变体占空间”。`atom/mesh` 的任务队列：

```rust
pub enum Job {
    AddWorker { config: Box<WorkerConfigRequest> },
    UpdateWorker { url: String, update: Box<WorkerUpdateRequest> },
    RemoveWorker { url: String },
    // …
}
```

大的配置对象都放在 `Box` 后面，每个 `Job` 里只留 8 字节的指针。这样队列里的每个 `Job` 都不大，哪怕它只是一个 `RemoveWorker`。（代码如此，动机是我的推断。）

同一个项目里也有真正的递归：`struct TokenHandle { inner: Inner }`，而 `enum Inner` 的一个变体是 `Pair { prefill: Box<TokenHandle>, decode: Box<TokenHandle> }`。两个类型互相包含，同样靠 `Box` 断开。它的另一个变体是 `Single(Box<dyn TokenSource>)`，这就是你问的第三种胖指针。

**适用边界**：

- **教程的链表是教学用的。** 每条链表要多分配一个只装 `Nil` 的节点。更常见的写法是 `struct Node { elem: u32, next: Option<Box<Node>> }`：`Option<Box<Node>>` 只有 8 字节，`None` 就是 0，等于 C 的 `struct Node *next` 加上“用之前必须判空”。
- **递归要吃栈。** 本机栈 8 MB：
  - 100 万个节点时，调试构建下 `len()` 栈溢出。
  - 释放这条链表也栈溢出，两种构建都一样，因为释放是一层套一层进行的。
  - 10 万个节点时都正常。

  实际代码里存一串元素几乎总是用 `Vec`。

---

## 检查题（节点 5–6）

**第 1 题。** 推理服务里一个请求有四种状态：

- 排队中，记入队时间
- 运行中，记 worker 编号和已生成的 token 数
- 已完成，记总 token 数
- 失败，记错误信息

同事按 C 的思路写成：

```rust
struct RequestState {
    kind: u8,            // 0 排队，1 运行，2 完成，3 失败
    enqueued_at: u64,
    worker: u32,
    generated: u32,
    total: u32,
    error: String,
}
```

1. 这种写法允许哪些不该出现的值？举一两个具体例子，说它们会在什么时候造成麻烦。
2. 改写成 enum，写出定义即可。改完之后，“读取失败原因”的代码必须长成什么样？
3. 以后要加一种状态“已取消”。struct 写法、enum 加逐个列出的 `match`、enum 加带 `_` 的 `match`，这三种情况各会发生什么？

**第 2 题。** 下面三个定义，哪些能编译？能编译的，说出一个值的大小由什么决定；不能编译的，说原因。

```rust
enum Tree { Leaf(u32), Node(Tree, Tree) }                        // (a)
enum Tree { Leaf(u32), Node(Box<Tree>, Box<Tree>) }              // (b)
struct Chunk { data: [u8; 1024], next: Option<Box<Chunk>> }      // (c)
```

---

**014 · 用户** · `2026-10-13T00:55:18.837Z` · `msg-27d57faffa1543ffb25e`

"héllo" 只有 5 个字符，为什么字节数是6？

---

**015 · 助手** · `2026-10-13T00:55:51.238Z` · `msg-d358e54430078c027be9`

因为 `é` 这一个字符在内存里占 2 个字节。Rust 的字符串统一按 UTF-8 存，而 UTF-8 是变长编码：不同的字符占 1 到 4 个字节。

`"héllo"` 在本机的 6 个字节是：

```text
字符   h     é        l     l     o
字节   68    c3 a9    6c    6c    6f
```

| 字符 | 字节数 | 例子（本机实测的字节） |
| --- | --- | --- |
| ASCII（英文字母、数字） | 1 | `a` 是 `61` |
| 带重音的拉丁字母等 | 2 | `é` 是 `c3 a9` |
| 汉字 | 3 | `你` 是 `e4 bd a0`，所以 `"你好".len()` 是 6 |
| emoji 等 | 4 | `😀` 是 `f0 9f 98 80` |

所以 `&str` 第二个字里存的是字节数，`s.len()` 返回的也是字节数（6）。字符数要另外数：`s.chars().count()` 得 5。Python 里对应的是 `len("héllo")` 得 5、`len("héllo".encode())` 得 6；C 的 `strlen` 对这段字节返回 6。

这和节点 1 说的“`char` 占 4 字节”不矛盾。`char` 是单独拿出来的一个字符，按最宽的情况留了 4 字节。字符串里不这样存，否则纯英文文本要多占 3 倍空间。UTF-8 让 ASCII 文本每个字符只占 1 字节，代价是不能按“第几个字符”直接定位：

- **`s[1]` 编译不过**（E0277）。第 1 个字符从哪个字节开始，要从头数才知道，Rust 不提供一个看起来很快、实际要扫描的下标。
- **按字节范围切可以，但要切在字符边界上。** `&s[1..3]` 得到 `"é"`；`&s[0..2]` 会从 `é` 中间切开，运行时 panic：`end byte index 2 is not a char boundary`。
- **要第几个字符就用迭代器。** `s.chars().nth(1)` 得到 `Some('é')`。

节点 5–6 的两道检查题还在等你，准备好了直接答就行。

---

**016 · 用户** · `2026-10-13T03:27:26.670Z` · `msg-4fef151f903b7584c21a`

Box是什么？这个也是后面才会讲的内容吗？

---

**017 · 助手** · `2026-10-13T03:31:30.518Z` · `msg-3fe9f3a2fe48464bf763`

刚才在核对上一条消息里 `Box` 是在哪里第一次出现的，并在本机跑了几个小例子，下面是回答。

`Box` 不用等到后面的课，它是本课节点 6 的内容，就在上一条消息的下半部分。我在胖指针那一段就先用了它，比解释它的地方早了两节，顺序排反了。先给一个够用的版本。

**`Box<T>` 是一个指针：它指向堆上的一个 `T`，并且独占这个值。** 独占的意思是这块堆内存只有这一个 `Box` 指着，由它负责释放。

```rust
let a: u32 = 5;                  // 5 直接放在变量 a 里
let b: Box<u32> = Box::new(5);   // 5 放到堆上，b 里放的是它的地址
println!("{}", *b + 1);          // *b 取出指向的值，同 C 的 *p；输出 6
```

```text
栈                                      堆
a   05 00 00 00
b   地址，8 字节  ────────────────────►  05 00 00 00
```

本机一次运行里，变量 `a`、`b` 的地址是 `0x7ffeeafc333c` 和 `0x7ffeeafc3340`，挨在一起，都在栈上；`b` 里存的地址是 `0x6205f3ad3d60`，在堆上。

- **对照**：C++ 的 `std::unique_ptr<T>`，`Box::new(5)` 相当于 `std::make_unique<unsigned>(5)`。C 里是 `malloc` 加手工 `free`。Python 的每个对象本来就在堆上，变量存的是引用，所以不用写出来。
- **写法**：`Box` 是标准库里的一个类型，不是关键字。尖括号里是它指向的类型，和 `Option<u32>` 的尖括号是同一个意思。
- **它本身只是一个地址**：`Box<u32>` 是 8 字节，`Box<[u64; 100]>` 也是 8 字节，而 `[u64; 100]` 本身是 800 字节。
- **不会是空**：它一定指向一个有效的值。所以 `Option<Box<T>>` 可以拿 0 表示 `None`，仍然是 8 字节。
- **自动释放，恰好一次**：`b` 所在的 `{}` 结束时，堆上的值跟着释放，相当于编译器替你写了 `free`。
- **交出去之后不能再用**：`let c = b;` 是把这个 `Box` 交给 `c`，之后再用 `b` 编译不过（E0382）。C++ 里 `std::move(p)` 之后再写 `*p` 能编译，本机运行时段错误。

**和引用 `&T` 的区别**：两个都是指针，大小规则也一样。让你卡住的那句说的就是这个：`Box<u8>` 是 8 字节，`Box<[u8]>` 要多带长度，是 16 字节。差别在值归谁：

- `&T` 是借来看的，值在别处，引用用完什么都不发生。
- `Box<T>` 指向的值归它自己，它用完，值就释放。

**为什么要有它**：Rust 的值默认直接放在变量里，或者内嵌在外层的值里，这样省掉一次堆分配和一次跳转。`Box` 用来处理直接放行不通的情况，比如一个类型里要包含它自己，节点 6 用链表讲的就是这件事。

它会在这几处讲到：

| 位置 | 讲什么 |
| --- | --- |
| 本课节点 6（上一条消息） | 类型里包含自己时为什么必须用它；教程的链表示例 |
| 第 08 课，所有权 | “独占”“交出去之后不能再用”“什么时候释放”这套规则本身 |
| 第 10 课，trait | `Box<dyn Trait>` |
| 第 13 课，标准库类型 | 教程专讲 `Box` 的一页，和 `Vec`、`String` 等放在一起比较 |

教程专讲 `Box` 的那一页是 [std/box.md](docs/rust-by-example/src/std/box.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/std/box.html)），归第 13 课，很短，想现在看也可以。本机运行它的示例：`Point` 16 字节，`Rectangle` 32 字节，三个 `Box` 都是 8 字节。示例里 `derive` 的 `Copy` 还没讲，意思是这个类型的值赋值时直接复制一份，和 C 的 struct 赋值一样。

节点 6 之前还有两处提到 `Box`：节点 5 内存表里的 `Option<Box<T>>`，和节点 5 结尾“面试怎么讲”的最后一句。用上面这个模型都能读懂，接着往下读就行。

（来源：Rust by Example 1.97.1 的 Box, stack and heap 一页；标准库 `alloc/src/boxed.rs` 对 `Box` 的说明是 “A pointer type that uniquely owns a heap allocation of type `T`”；数字是本机 rustc 1.97.1 和 g++ 13.3.0 的实测。）

---

**018 · 用户** · `2026-10-13T06:12:05.722Z` · `msg-628ca6d2269a6b28b9b9`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/docs/rust-learning/attachments/02-data-shapes/memory-layout.html in the IDE. This may or may not be related to the current task.</ide_opened_file>
enum中说绕开 match 直接取载荷不行：e.0 报 E0609。那对于所有枚举的东西，我都需要且只能通过match来进行处理吗？

---

**019 · 助手** · `2026-10-13T06:14:39.303Z` · `msg-c6ac97c7a326c1225271`

刚才在本机把几种写法都编译运行了一遍，并查了标准库和路由器项目里的实际用法。

不是。上一条里我写“读取只能用 `match`”，说窄了。准确的规则是：

**要拿到载荷，必须经过一个写明变体的模式。** `match` 是最完整的一种写法，另外有几种简写。不需要载荷的时候，连模式都不用。

### 拿载荷的几种写法

下面几种在本机 1.97.1 上都能编译。`&e` 的意思是借来看，不把 `e` 拿走。

| 想做的事 | 写法 | C++ 对照 |
| --- | --- | --- |
| 每个变体各做各的 | `match e { … }` | `std::visit` |
| 只关心一个变体 | `if let WebEvent::KeyPress(c) = &e { … }`，可以接 `else` | `if (auto* p = std::get_if<KeyPress>(&v))` |
| 不是这个变体就提前返回 | `let WebEvent::KeyPress(c) = &e else { return; };` | 函数开头的 `if (!p) return;` |
| 只问是不是这个变体 | `matches!(e, WebEvent::KeyPress(_))`，结果是 `bool` | `std::holds_alternative<KeyPress>(v)` |

`matches!` 带 `!`，是宏。标准库里它展开后就是一个两分支的 `match`：匹配上得 `true`，`_` 得 `false`。

`Option` 这类常用的 enum，作者已经把常见的拆法写成了方法，比如 `o.is_some()`、`o.unwrap_or(0)`、`o.unwrap()`，调用方不用自己写模式。它们内部仍然是模式：标准库里 `unwrap` 的函数体是一个两分支的 `match`，`is_some` 只有一行 `matches!(*self, Some(_))`。`unwrap` 的意思是“我断定它是 `Some`，不是就让程序崩”，对 `None` 调用时本机 panic，信息是 ``called `Option::unwrap()` on a `None` value``。

### 不需要模式的情况

- **不拆开，整个用**：把 enum 值传给函数、存进 struct、用 `{:?}` 打印，都不用 `match`。
- **不带数据的 enum**：`k as i32` 直接转整数。加上 `#[derive(PartialEq)]` 之后可以写 `k == Number::One`，不加报 E0369。
- **只有一个变体的 enum**：普通的 `let Wrapper::Only(v) = w;` 就行，因为不存在“不是这个变体”的情况。

### 为什么不给 `e.0`

一个 enum 值里有哪些字段，取决于运行时它是哪个变体。`e.0` 这种写法里没有地方写“我认为它是哪个变体”，编译器只剩两条路：

- **不检查**：这就是 C 的 union，读错了没人知道。
- **运行时偷偷检查**：不对就崩，而代码上看不出这里可能崩。

Rust 两条都不走，要求把“判断是哪个变体”和“取出数据”写成一步，这一步就是模式。所以凡是拿到载荷的地方，一定已经判断过变体。

简写没有省掉判断，只是省了字。对多变体的 enum 写普通的 `let WebEvent::KeyPress(c) = e;` 会报 E0005，说 `PageLoad` 没有覆盖，并建议改成 `let … else`。

### 怎么选

简写都不做穷尽检查，相当于 `match` 里写了 `_`。本机给 enum 加一个新变体后，`if let` 的代码照常编译，新变体被悄悄跳过。

- **每个变体分别处理，或者希望以后加变体时被编译器提醒**：用不带 `_` 的 `match`。
- **只关心一个变体**：用 `if let` 或 `let … else`。
- **只要一个布尔结果**：用 `matches!`。

### 真实系统

`atom/mesh/src` 的 185 个 `.rs` 文件里，按 grep 粗略数，`match` 和 `if let` 各约 520 处，`matches!` 约 90 处，`let … else` 约 40 处。简写和 `match` 一样常用。`core/worker.rs` 里连着的两段正好是两种选择：

```rust
let worker_type_str = match worker_type {
    WorkerType::Regular => "regular",
    WorkerType::Prefill { .. } => "prefill",
    WorkerType::Decode => "decode",
};

let bootstrap_port = match worker_type {
    WorkerType::Prefill { bootstrap_port } => *bootstrap_port,
    _ => None,
};
```

- **第一段**要给每种 worker 一个名字，所以逐个列出。以后加一种 worker，这里会报错。
- **第二段**只有 `Prefill` 有端口，其余用 `_`。
- **两个新写法**：`{ .. }` 的意思是“这个变体有字段，但我不看”。`*bootstrap_port` 里的 `*` 是因为 `worker_type` 是引用，拆出来的字段也是引用。

**读哪里**：`if let` 和 `let … else` 是第 04 课的内容，现在不必读。教程在 [if_let.md](docs/rust-by-example/src/flow_control/if_let.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/flow_control/if_let.html)）和 [let_else.md](docs/rust-by-example/src/flow_control/let_else.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/flow_control/let_else.html)）。节点 5–6 的检查题里，用 `match` 或 `if let` 写都可以。

（来源：标准库 1.97.1 的 `core/src/option.rs` 和 `core/src/macros/mod.rs`；`ROCm/ATOM` 提交 `43f5393`；报错和输出是本机 rustc 1.97.1 的实测。）

---

**020 · 用户** · `2026-10-13T06:21:34.149Z` · `msg-2df933d3a6af018df4e7`

总而言之就是必须要检查对吧？

---

**021 · 助手** · `2026-10-13T06:21:41.286Z` · `msg-e80fbb7ce966aa268f61`

对。要拿载荷，就必须先确认是哪个变体，而且“确认”和“取数据”写在同一步里，编译器保证这一步跳不过去。

补两点，让这句话更准：

- **检查省不掉，但检查不通过时怎么办由你选。** `match` 是每种情况都处理，`if let` 是其余的忽略，`let … else` 是提前返回，`unwrap` 是直接崩。
- **只有拿载荷才需要检查。** 把整个值传走、存起来、打印，或者把不带数据的 enum 转成整数，都不用。

检查本身发生在运行时，就是读一下标签再比较；编译器在编译时做的事，是保证每个取载荷的地方都有这次检查。

---

**022 · 用户** · `2026-10-13T06:24:07.759Z` · `msg-bd6afa4a70c63fecd4e7`

标签就是C中枚举的整数，载荷就是rust引入的给变体添加的数据。是吗？

---

**023 · 助手** · `2026-10-13T06:24:18.953Z` · `msg-b1dd9bf95ed9f6464f3c`

是的，这两句都对。各补一点，让它更准：

- **标签**：就是 C 枚举里的那个整数，记着“现在是哪个变体”。不带数据的 enum 整个值只有它，所以 `Number` 只占 1 字节，和 C 的枚举一样。差别是 C 里任何整数都能塞进枚举变量（`enum Kind k = 42;` 能编译），Rust 的标签只会是声明过的那几个变体，整数也不能 `as` 成 enum。
- **载荷**：就是变体带的数据。C 里也能带，做法是自己在枚举旁边配一个 `union`。Rust 新加的是把两者做成一个类型并且绑死：标签说是哪个变体，载荷就只能按那个变体读。

内存里的样子正是“C 的枚举整数加数据”。`Device::Cuda(3)` 本机是 `01 00 00 00 03 00 00 00`，前 4 字节是标签 1，后 4 字节是载荷 3。

有一个例外要记住：标签在逻辑上一定有，但不一定单独占字节。`Option<Box<T>>` 只有 8 字节，因为 `Box` 不会是 0，编译器直接拿 0 表示 `None`，标签就藏在载荷用不到的取值里了。

---

**024 · 用户** · `2026-10-13T06:27:58.996Z` · `msg-19e044c3673836939a01`

这个例外是什么意思？说的明白一些。

---

**025 · 助手** · `2026-10-13T06:28:41.420Z` · `msg-fb6afd372b4ec87db9df`

意思是：有些类型的值本身就有“永远用不到的取值”，编译器拿其中一个来表示“是哪个变体”，就不用再另外放一个标签了。对比两个 `Option` 最清楚，下面的字节都是本机实测。

### 普通情况：`Option<u32>`，标签单独占地方

`u32` 的 4 个字节，从 0 到 42 亿多的每一种取值都是合法的数。没有哪个取值能空出来表示“没有”，所以必须另外放一个标签：

```text
               标签          载荷
Some(7)        01 00 00 00   07 00 00 00
Some(0)        01 00 00 00   00 00 00 00     ← 0 是一个正常的数，不能拿来当“没有”
None           00 00 00 00   （无意义）
```

所以 `u32` 是 4 字节，`Option<u32>` 是 8 字节。

### 例外：`Option<Box<u32>>`，不另放标签

`Box` 里存的是一个堆地址，而它一定指向一个有效的值，所以这 8 个字节永远不会全是 0。0 这个取值就空出来了，编译器把它分给 `None`：

```text
Some(Box::new(7))   60 fd f4 28 cf 63 00 00     ← 就是那个堆地址 0x63cf28f4fd60
None                00 00 00 00 00 00 00 00     ← 全 0
```

`Box<u32>` 是 8 字节，`Option<Box<u32>>` 还是 8 字节，没有多出来的标签。判断是 `Some` 还是 `None`，就是看这 8 个字节是不是 0。

这其实就是 C 的空指针：`uint32_t *p`，`NULL` 表示没有。内存里一模一样。差别只在类型上：C 的指针可以不判空直接用，`Option<Box<u32>>` 必须先过模式才能拿到里面的 `Box`。

### 不只是指针

规则是通用的：载荷类型只要有用不到的取值，就可以这样省。`bool` 占 1 字节，但只用 0 和 1 两个取值，所以 `Option<bool>` 也只占 1 字节：

```text
Some(false)   00
Some(true)    01
None          02
```

### 对写代码的影响

没有影响，这只是编译器省空间的做法。代码照样写 `match` 或 `if let`，照样必须先确认变体。所以我说“标签在逻辑上一定有”：你总能问它是哪个变体。“不一定单独占字节”是指这个信息有时编码在载荷用不到的取值里。

图解页“enum”一节可以在 `Option<u32>` 和 `Option<&i32>` 之间切换着看这两种放法：<https://claude.ai/artifact/UAdb78pBPSLcVT9FtHqVuB>

---

**026 · 用户** · `2026-10-13T06:31:48.765Z` · `msg-aa5559b9f8fed182468f`

你的意思是定义了一个枚举类型，其中某一个标签带的载荷的类型是Option<u32>？

---

**027 · 助手** · `2026-10-13T06:32:18.834Z` · `msg-87ee5451fbf38ff76d11`

不是。`Option<u32>` 本身就是那个枚举类型，不是别的枚举里的载荷。这个地方我一直直接拿 `Option` 举例，没有把它拆开讲，补上。

### `Option<u32>` 是什么

它是标准库定义的一个 enum，表示“可能有一个 `u32`，也可能没有”。把它手写出来就是：

```rust
enum Option<u32> 相当于 {
    None,         // 变体一：没有值，不带载荷
    Some(u32),    // 变体二：有值，载荷是一个 u32
}
```

所以在 `Option<u32>` 里：

- **枚举类型**是 `Option<u32>`。
- **变体**有两个，`None` 和 `Some`。
- **载荷**是 `Some` 带的那个 `u32`。`None` 没有载荷。
- **标签**记的是“现在是 `None` 还是 `Some`”。

顺带纠正一个说法：带载荷的是变体，不是标签。标签只是记录“是哪个变体”的那个整数。

### 尖括号是什么

标准库里的定义只写了一次：

```rust
pub enum Option<T> {
    None,
    Some(T),
}
```

`T` 是一个类型的占位符，用的时候填进具体类型。`Option<u32>` 就是把 `T` 换成 `u32`，`Option<Box<u32>>` 就是把 `T` 换成 `Box<u32>`。这对应 C++ 的模板：`Option<u32>` 相当于 `std::optional<uint32_t>`。Python 里对应类型标注 `Optional[int]`，也就是“要么是 `int`，要么是 `None`”。这种写法叫泛型，第 07 课系统讲，现在知道“尖括号里填类型”就够。

### 回头看上一条的例子

| 类型 | 两个变体 | 标签放哪 |
| --- | --- | --- |
| `Option<u32>` | `None`，`Some(u32)` | 单独占 4 字节：0 是 `None`，1 是 `Some` |
| `Option<Box<u32>>` | `None`，`Some(Box<u32>)` | 不单独放：8 字节全 0 是 `None`，否则是 `Some`，这 8 字节就是那个 `Box` |
| `Option<bool>` | `None`，`Some(bool)` | 不单独放：0 和 1 是 `Some(false)`、`Some(true)`，2 是 `None` |

这个规律和 `Option` 这个名字无关，自己写的 enum 也一样。本机试了两个手写的：

```rust
enum MyOption    { Nothing, Has(u32) }        // 8 字节，Has(7) 是 01 00 00 00 07 00 00 00
enum MyOptionBox { Nothing, Has(Box<u32>) }   // 8 字节，Nothing 是全 0
```

我选 `Option` 举例，是因为它是最简单的“两个变体、其中一个带数据”的 enum，也是 Rust 里用得最多的一个：节点 1 的 `checked_mul` 和节点 3 的 `get` 返回的都是它。

（来源：标准库 1.97.1 的 `core/src/option.rs`；字节和大小是本机 rustc 1.97.1 的实测。）

---

**028 · 用户** · `2026-10-13T06:34:00.911Z` · `msg-b4782e76a907e549fa87`

Some又是什么？是Option定义的标签？

---

**029 · 助手** · `2026-10-13T06:34:33.867Z` · `msg-c4081539b69c71352a9c`

`Some` 是 `Option` 定义的两个**变体**之一，另一个是 `None`。它只是标准库作者起的一个名字，英文 some 在这里的意思是“有值”，`None` 是“没有”。标签是内存里记录“现在是哪个变体”的那个整数，`Some` 对应的标签是 1。

把它和节点 5 的 `Device` 并排放，形状完全一样：

| | 自己写的 `Device` | 标准库的 `Option<u32>` |
| --- | --- | --- |
| 定义 | `enum Device { Cpu, Cuda(u32) }` | `enum Option<T> { None, Some(T) }`，`T` 填 `u32` |
| 不带数据的变体 | `Cpu` | `None` |
| 带数据的变体 | `Cuda(u32)` | `Some(u32)` |
| 造一个值 | `Device::Cuda(3)` | `Some(7)` |
| 标签 | `Cpu` 是 0，`Cuda` 是 1 | `None` 是 0，`Some` 是 1 |
| 内存（本机实测） | `01 00 00 00 03 00 00 00` | `01 00 00 00 07 00 00 00` |

所以 `Some` 之于 `Option`，就是 `Cuda` 之于 `Device`。

### 怎么用

```rust
let x: Option<u32> = Some(7);    // 造一个“有值”的 Option，载荷是 7
let z: Option<u32> = None;       // 造一个“没有”的 Option

match x {
    Some(n) => println!("has {n}"),   // n 绑到载荷 7 上；本机输出 has 7
    None => println!("nothing"),
}
```

- **`Some(7)` 看起来像函数调用，其实是在造这个变体的值**，和 `Device::Cuda(3)` 是同一种写法。
- **为什么不用写 `Option::`**：全名是 `Option::Some`，本机 `Option::Some(7) == Some(7)` 是 `true`。标准库替每个程序预先写好了一句 `use`，把 `Some` 和 `None` 直接引了进来，机制就是节点 5 讲的 `use Stage::*`。

### 为什么要包一层

因为 `u32` 和 `Option<u32>` 是两个不同的类型：前者一定有一个数，后者可能没有。`Some` 就是把前者包成后者的那一步。

- **不包不行**：`let x: Option<u32> = 7;` 报 E0308，编译器直接提示 `try wrapping the expression in Some`。
- **不拆也不行**：`x + 1` 报 E0369，`Option<u32>` 不能直接当数来算，要先用模式把里面的 `u32` 取出来。

这和 Python 不一样。Python 里写 `x = 7` 或 `x = None`，有值的情况不用包，所以也没有东西拦着你对一个可能是 `None` 的变量直接做 `x + 1`。C++ 的对应物是 `std::optional<uint32_t>`，“没有”写作 `std::nullopt`。

（来源：标准库 1.97.1 的 `core/src/option.rs` 和 `core/src/prelude/v1.rs`；字节和报错是本机 rustc 1.97.1 的实测。）

---

**030 · 用户** · `2026-10-13T07:30:31.345Z` · `msg-52765f8e00fcc6d95af5`

Box和& mut的区别是什么？

---

**031 · 助手** · `2026-10-13T07:31:46.857Z` · `msg-f8d38d56ed32a796bc74`

两个都是 8 字节的指针，都能改指向的值，同一时刻也都只有它一个能碰那个值。区别在**值归谁**：`Box<T>` 拥有它指向的值；`&mut T` 只是把别人的值临时借来改。

先交代 `&mut T`：它叫可变引用，是一个指向 `T` 的指针，可以通过它修改这个值。之前说的 `&T` 只能读。对应 C++ 的 `T&`，或者 C 里传给函数让它修改的 `T*`。第 01 课你写过的 `fn fmt(&self, f: &mut fmt::Formatter)` 里就有它。

```rust
fn add_one(p: &mut u32) {   // 借一个 u32 来改
    *p += 1;
}

let mut a: u32 = 5;                   // 值在栈上，归 a。mut 表示之后要改
add_one(&mut a);                      // 借出去改，改完归还；a 是 6

let mut b: Box<u32> = Box::new(5);    // 值在堆上，归 b
*b += 1;                              // 通过 Box 改；是 6
add_one(&mut *b);                     // 把 Box 里的值借出去改；是 7
```

本机一次运行里，`&mut a` 指向 `0x7fff1352925c`（栈），`&mut *b` 指向 `0x60cccc7d7d60`（堆）。

| | `Box<T>` | `&mut T` |
| --- | --- | --- |
| 值归谁 | 归这个 `Box` | 归别人，这里只是借 |
| 值在哪 | 堆 | 哪里都行：栈、堆、某个 struct 里 |
| 怎么来 | `Box::new(v)`，一次堆分配 | `&mut a`，只是取地址，不分配 |
| 用完之后 | 堆上的值被释放 | 什么都不发生，值还在原主手里 |
| 能存在多久 | 随意，可以从函数返回、存进 struct | 不能比原主久 |
| C++ 对照 | `std::unique_ptr<T>` | `T&` |

最后一行代码说明两者不是二选一：`Box` 决定值放在哪、归谁，`&mut` 是把它临时借给别人改的方式。

### 区别在哪里看得出来

**函数里造的值，`Box` 能带出来，`&mut` 不能。**

- **`Box`**：`fn make() -> Box<u32> { Box::new(5) }` 可以编译。值在堆上，归返回的那个 `Box`。
- **`&mut`**：`fn make() -> &mut u32 { let mut x = 5; &mut x }` 报 E0106，提示是 “this function's return type contains a borrowed value, but there is no value for it to be borrowed from”。借的东西必须有主，而 `x` 在函数返回时就没了。
- **C 的对照**：C 里这样写只有一个警告，本机 gcc 13.3 编译出的程序运行时段错误。

**借出去期间，原主自己也不能碰。**

- **借着的时候用 `a`**：`let p = &mut a;` 之后、`p` 还在用的时候写 `a += 1;`，报 E0503。
- **再借一次**：同时再写一个 `&mut a`，报 E0499。

这就是“同一时刻只有一个能碰”的含义，第 08 课展开。

### 为什么链表用 `Box` 而不是 `&mut`

节点 6 的 `Cons(u32, Box<List>)` 里，“剩余部分”必须有主。如果写成 `&mut List`，被指的那个节点就得归链表之外的某个东西，而并没有这样一个东西。用 `Box`，每个节点拥有下一个节点，整条链表从头节点一路拥有下去，头节点释放时整条链跟着释放。

反过来，`fmt` 的参数 `f: &mut fmt::Formatter` 用的是借：格式化器是调用方的，借给你的 `fmt` 往里写，写完归还。你没有创建它，也不负责释放它。

### 怎么选

- **这个值需要一个主人，并且要放在堆上**：用 `Box`。常见于 struct 或 enum 的字段。
- **值已经有主，只是让别人临时改一下**：用 `&mut`。常见于函数参数。

**读哪里**：借用规则是第 08 课的内容，现在不必读。教程在 [scope/borrow/mut.md](docs/rust-by-example/src/scope/borrow/mut.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/scope/borrow/mut.html)）。

（报错和地址是本机 rustc 1.97.1、gcc 13.3.0 的实测。）

---

**032 · 用户** · `2026-10-13T07:38:59.436Z` · `msg-d36957431b4974d30447`

是生命周期上的区别是吗？&mut借来用，“释放”动作还是由原主来管是吧？如果借出去了的时候，原主被销毁了，那么借出去的这个也会被释放吗？

---

**033 · 助手** · `2026-10-13T07:39:40.041Z` · `msg-f5e79a41191663f194e6`

前两句都对，第三种情况在 Rust 里写不出来，编译器会拦住。

**1. 是生命周期上的区别吗？** 是，不过生命周期是结果，根源是值归谁。`Box` 拥有值，所以值跟着 `Box` 活，`Box` 想活多久都行。`&mut` 是借的，所以它必须在原主销毁之前结束。Rust 里“生命周期”正是指“一个引用在多长的范围内有效”，是第 09 课的主题。

**2. 释放还是原主管吗？** 是。`&mut` 用完什么都不发生，释放永远是原主的事。

**3. 借出去的时候原主被销毁了会怎样？** 先澄清一点：借出去的不是另一份东西。`&mut` 只是原主那个值的地址，值从头到尾只有一份。原主销毁，这一份值就释放了，引用手里剩下一个指向已释放内存的地址。这就是 C 里的悬空指针。Rust 的规则是：**原主销毁之前，借用必须已经结束**，违反了编译不过。

### 本机试的三种写法

**原主的作用域先结束**，报 E0597：

```rust
let p: &mut u32;
{
    let mut a: u32 = 5;
    p = &mut a;
}             // a 在这里销毁
*p += 1;      // 还想用 p
```

编译器的原话是 `` `a` dropped here while still borrowed ``。

**手动销毁原主**，报 E0505。`drop(b)` 是标准库函数，意思是“现在就销毁 `b`”：

```rust
let mut b: Box<u32> = Box::new(5);
let p = &mut *b;
drop(b);      // 想销毁原主
*p += 1;      // 之后还要用 p
```

**借用先结束再销毁**，可以编译，输出 6：

```rust
let mut b: Box<u32> = Box::new(5);
let p = &mut *b;
*p += 1;      // p 最后一次使用，借用到这里结束
drop(b);      // 这时销毁没问题
```

借用的结束点是引用最后一次被使用的地方，不一定是 `}`。

### C 和 C++ 里同样的事

| 写法 | 编译 | 本机运行 |
| --- | --- | --- |
| C：`free(b)` 之后 `*p += 1` | 不加选项没有任何提示；加 `-Wall` 有警告 `pointer 'p' used after 'free'` | 正常退出，打印 683878851 |
| C++：`b.reset()` 之后通过引用 `r += 1` | `-Wall -Wextra` 没有任何提示 | 正常退出，打印 2801247753 |

两个程序都没崩，只是悄悄读写了已经释放的内存，打印出垃圾值。这个打印值每次运行可能不同。Rust 把这类错误挪到了编译期，“没有垃圾回收，编译器凭什么保证引用不会悬垂”正是第 08 课要回答的问题。

**读哪里**：现在不必读。第 08 课对应 [scope/borrow.md](docs/rust-by-example/src/scope/borrow.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/scope/borrow.html)），第 09 课对应 [scope/lifetime.md](docs/rust-by-example/src/scope/lifetime.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/scope/lifetime.html)）。

（报错和输出是本机 rustc 1.97.1、gcc/g++ 13.3.0 的实测。）

---

**034 · 用户** · `2026-10-13T08:08:05.623Z` · `msg-50e2ef249332a7e1ee3c`

检查题
1. 同事的这种写法会导致状态上出现不该有的信息。比如已完成状态却有错误信息变量，排队中却有total总token数变量。此时就需要额外为该信息无效设置一个无效的值。如果无效判断没写好，就出现异常情况了。
2.enum RequestState {
	Queuing(u64) ,   // u64表示入队时间
	Running(u32, u32),   // 第一个表示worker编号，第二个表示已生成token数
	Finished(u32),   //总token数
	Failed(String) //错误信息
}。读取失败原因的代码必须先检查状态，再读取。假如用match，分支可以写成RequestState::Failed(s) => println!("Error:{s}"),
3. 要加已取消，那么struct里kind加一个数字约定，再加上已取消的信息。而对于消费这个struct的位置，则没有强制约束添加处理代码。而对于enum，消费处如果是逐个列出的match，则会强制需要添加处理代码。而如果带有_的match，也至少有了兜底的处理方法。
第二题
（a）不能编译，因为载荷变成了自身，递归嵌套了。size无穷，会报错；
（b）可以编译。值大小由最大的情况两个Box决定。标签4字节+两个Box 2 * 8字节 = 20字节。
（c）可以编译。这是一个struct。第一种成员的值大小为1024字节。第二种情况的值大小为8字节。一共1032字节。

---

**035 · 助手** · `2026-10-13T08:13:56.215Z` · `msg-a5d1d40e991ebb50dc27`

正在把检查结果记进课程记录，然后给你反馈、节点 7、串讲和综合验收题。

---

**036 · 助手** · `2026-10-13T08:16:23.573Z` · `msg-13c2837161134f04e441`

**节点 5–6 检查：通过。** 两道题的结论都对，补三处。

- **第 1 题 (1)：还有一类更直接的非法值。** 你说的“状态里带着不属于它的字段”是对的。另一类是 `kind` 本身：它是 `u8`，可以是 7，而 7 不对应任何状态。实际出事常在状态切换时：失败后重试，`kind` 改回 0，`error` 里还留着上次的信息，只看 `error` 非空的监控代码就会报失败。
- **第 1 题 (3)：`_` 的兜底是在新状态出现之前写的。** 它对新状态不一定对，而且编译器不再提醒。本机试了一个判断“请求是否还在进行”的函数，写成“完成和失败返回 `false`，`_` 返回 `true`”。加入“已取消”后照常编译，已取消的请求被判成还在进行。逐个列出的写法在同一处报 E0004。
- **第 2 题 (b)：结论对，数字是 16。** “大小由最大的变体决定，和树有多深无关”是这题的要点，你答到了。数字差在两处：
  - **按规则算是 24，不是 20。** 大小要凑成对齐（8）的整数倍：标签 4 + 填充 4 + 两个指针 16。本机 `enum { Leaf(u32), Node(u64, u64) }` 就是 24。
  - **实际是 16，这里正好是你问过的那个例外。** `Box` 不会是 0，编译器用“第一个指针的位置是 0”表示 `Leaf`。本机 `Leaf(7)` 的前 8 字节全 0，7 放在后面；`Node` 的 16 字节是两个堆地址。你在 (c) 里把 `Option<Box<Chunk>>` 算成 8 字节，用的就是这一条。

另外两点：

- **你的 enum 能编译，本机 24 字节**，同事的 struct 是 48 字节。
- **`Running(u32, u32)` 的两个位置类型相同，写反了编译器发现不了。** 本机把两个数传反，读出来 worker 编号和 token 数就对调了。这种情况用带字段名的变体：`Running { worker: u32, generated: u32 }`。

(c) 的 1024 + 8 也说明“数组的值就是元素本身”这一点没问题了。

---

## 节点 7：`const` 与 `static`

**读哪里**：[constants.md](docs/rust-by-example/src/custom_types/constants.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/constants.html)）。只有一页，先读后读都行。示例最后的 `THRESHOLD = 5;` 是故意留的错误，去掉后本机输出 `This is Rust`、`The threshold is 10`、`16 is big`。

**结论**：两者都是写在函数外面、全程序可见的有名字的值。区别在有没有固定的内存位置。

- **`const`** 是编译期常量。编译器把它的值直接抄到每个用到它的地方，这叫内联。它自己不占固定的内存位置。
- **`static`** 是一块固定地址的内存，从程序启动存在到程序结束，全程序只有一份。

| | `const` | `static` |
| --- | --- | --- |
| 写法 | `const THRESHOLD: i32 = 10;` | `static LANGUAGE: &str = "Rust";` |
| 用到它的地方 | 各自得到一份值 | 都指向同一个地址 |
| C/C++ 对照 | `constexpr`，或 `#define` | 全局变量 |

“同一个地址”本机验证过：两个函数各自取同一个 `static` 的地址，结果相同。它不在栈上也不在堆上，在可执行文件自带的数据区里。

**共同的规则**，本机逐条试过：

- **必须写类型。** `const THRESHOLD = 10;` 报 ``missing type for `const` item``。`let` 可以让编译器推断，这两个不行。
- **初始值必须在编译时就能算出来。** 调用普通函数报 E0015。字面量、算术和标了 `const fn` 的函数可以。`const fn` 是“允许在编译时执行的函数”，对应 C++ 的 `constexpr` 函数。
- **不能赋值。** 对 `const` 赋值报 E0070，对 `static` 赋值报 E0594。
- **名字全大写加下划线。** 这是约定，写成小写编译器会警告。

**`const` 可以用在要求编译时已知的位置。** 节点 3 说过数组长度必须是编译时的常数：`let n = 5; [0u8; n]` 报 E0435，编译器建议把 `let` 改成 `const`。

**怎么选**：默认用 `const`。Rust Reference 列了三种该用 `static` 的情况：数据量大，不想每个使用处各抄一份；需要一个唯一的地址；需要全局的、会被修改的状态。

**会被修改的全局状态。** 教程提到 `static mut`，也就是可变的 `static`。直接改它报 E0133，理由是 `mutable statics can be mutated by multiple threads`，两个线程同时改会出错。要改就必须写在 `unsafe` 块里。`unsafe` 的意思是“这段代码的安全由我自己保证，编译器不再检查”，第 17 课讲，本仓库的代码禁止使用。

实际代码不用 `static mut`，而是给 `static` 一个原子类型。原子类型是“多个线程同时改也不会出错的整数”，对应 C++ 的 `std::atomic<uint64_t>`，第 14 课讲。`atom/mesh/src/middleware.rs` 里记录当前连接数的全局计数器：

```rust
static ACTIVE_HTTP_CONNECTIONS: AtomicU64 = AtomicU64::new(0);
```

每进来一个请求调用 `fetch_add` 加一，结束时调用 `fetch_sub` 减一。这个项目按 grep 数有 143 个 `const`、27 个 `static`、0 个 `static mut`。C 里对应的写法是全局 `int counter;` 加 `counter += 1;`，多线程下同样会出错，但编译器不提示。

**真实系统**：safetensors 的 `tensor.rs` 开头两行：

```rust
const MAX_HEADER_SIZE: usize = 100_000_000;
const N_LEN: usize = size_of::<u64>();
```

第一个是文件头长度的上限，1 亿字节。第二个是“文件开头那个长度字段占几个字节”，值是 8。`size_of` 是 `const fn`，所以能写在这里。

**适用边界**：教程说 `static` 具有 `'static` 生命周期。带撇号的名字是生命周期的写法，`'static` 的意思是“从程序启动活到程序结束”，第 09 课讲。

**面试怎么讲**：“`const` 是编译期常量，值被内联到每个使用处，没有固定地址；`static` 是全程序唯一的一块内存，活到程序结束。默认用 `const`，需要唯一地址、数据很大或者需要全局可变状态时用 `static`。可变的全局状态不用 `static mut`，那需要 `unsafe`，实际用原子类型或锁。”

---

## 串讲：从 3.9 GB 的文件到一个 48 字节的值

沿着 safetensors 读 `Qwen2.5-7B-Instruct` 第一个分片的过程，把七个节点串起来。

1. **整个文件是一个 `&[u8]`。** 它是 16 字节：指针加长度 3,945,441,440。文件多大，传来传去的都只是这两个字。（节点 3）
2. **取文件头长度。** 文件的前 8 字节是一个 `u64`，记着文件头有多长。

   ```rust
   let Some(header_size_bytes) = buffer.get(..N_LEN) else {
       return Err(SafeTensorError::HeaderTooSmall);
   };
   ```

   - **`..N_LEN`** 是 `0..N_LEN` 的简写，`N_LEN` 就是上面那个 `const`。（节点 7）
   - **`get`** 返回 `Option<&[u8]>`。文件不足 8 字节时得到 `None`，不会读到缓冲区外面。（节点 3）
   - **`let … else`** 是你问过的简写：是 `Some` 就拿出里面的切片，否则提前返回。（节点 5）
   - **`SafeTensorError`** 本身也是一个 enum，每种错误是一个变体。`Err(…)` 表示返回一个错误，第 12 课讲。

   这 8 字节读出来是 9,368。
3. **检查这个数。** 它来自文件，不可信。先和 `MAX_HEADER_SIZE` 比，再用 `checked_add` 算文件头的结束位置，溢出就报错。（节点 1）
4. **解析文件头。** 9,368 字节的 JSON 变成 82 个 `TensorInfo`。它是 struct，里面的 `dtype` 是 enum，`shape` 是 `Vec<usize>`，`data_offsets` 是元组 `(usize, usize)`。（节点 2、4、5）
5. **逐个校验。** 起止偏移要首尾相接，止小于起直接拒绝。元素个数乘位数用 `checked_mul`，位数来自 `Dtype::bitsize`，一个 22 个分支、没有 `_` 的 `match`。（节点 1、5）
6. **取出张量。** `&self.data[s..e]` 切出 `model.embed_tokens.weight` 的 1,089,994,752 字节，装进 `TensorView`。这个值是 48 字节，数据一个字节都没复制。（节点 3、4）

规模上：就算把 82 个张量的 `TensorView` 全造出来，也只有 82 × 48 = 3,936 字节，它们描述的是 3,945,432,064 字节的数据。

这条线上反复出现三件事：

- **信息放在类型里，还是带在值里。** `[u8; 8]` 的长度在类型里，编译时就知道；`&[u8]` 的长度带在值里，运行时才知道。
- **值是数据本身，还是隔一层指针。** struct、数组、enum 的载荷都直接内嵌；切片、`Box`、`Vec` 里放的是指针。前者省一次跳转，后者让大小固定。
- **C 里靠约定的事，Rust 写进了类型。** 由编译器或运行时的检查来保证，代价是运行时多几次检查，代码里多写几个分支。

---

## 综合验收

三道题。答完再看还需不需要动手练习。

**第 1 题（口述，60–90 秒）。** 面试官说：“C 里我用 `(const uint8_t *p, size_t len)` 传一段数据，用可空指针 `T *p` 表示‘可能没有’。Rust 里这两样分别对应什么类型？内存里变大了吗？Rust 多保证了什么，代价是什么？”把回答按说话的方式写下来，不用列表。

**第 2 题（没讲过的真实代码）。** 路由器项目里，推理引擎流式吐出的每个分片是一个 `TokenChunk`。中间的分片是 `Partial`，最后一个是 `Complete`。

```rust
pub enum TokenChunk {
    Partial {
        token_ids: Vec<u32>,
        logprobs: Option<TokenLogprobs>,
    },
    Complete {
        token_ids: Vec<u32>,
        finish_reason: FinishReason,
        matched_stop: Option<MatchedStop>,
        usage: Usage,
        // 还有 3 个字段，略
    },
}

pub enum FinishReason {
    Stop,
    Length,
    ContentFilter,
    ToolCalls,
    Abort,
    Other(String),
}
```

`TokenLogprobs`、`MatchedStop`、`Usage` 是别的 struct 和 enum，不用管里面是什么。本机实测：`Partial` 的两个字段合计 48 字节，`Complete` 的全部字段合计 188 字节，这个 enum 的标签没有单独占空间，对齐是 8。

1. 一次生成 500 个 token，流里有几百个 `Partial` 和 1 个 `Complete`。一个 `Partial` 值占多少字节？为什么？它带的那些 token id 放在哪里？
2. 想让每个 `Partial` 变小，可以怎么改 `TokenChunk` 的定义？改完多付出什么？什么情况下才值得改？
3. 有人写了一个函数，判断这次生成是不是正常结束：

   ```rust
   fn is_normal_end(reason: &FinishReason) -> bool {
       match reason {
           FinishReason::Stop => true,
           FinishReason::Length => true,
           _ => false,
       }
   }
   ```

   后来 `FinishReason` 加了一个变体 `StopSequence`，语义上也算正常结束。重新编译时编译器会说什么？程序跑起来是什么表现？这个函数当初该怎么写，代价是什么？

**第 3 题（改一个条件，预测结果）。** 下面的程序本机输出 2。

```rust
static ACTIVE: AtomicU64 = AtomicU64::new(0);

fn main() {
    ACTIVE.fetch_add(1, Ordering::Relaxed);          // 加 1
    ACTIVE.fetch_add(1, Ordering::Relaxed);          // 再加 1
    println!("{}", ACTIVE.load(Ordering::Relaxed));  // 读出当前值
}
```

把第一行的 `static` 改成 `const`，程序仍然能编译。输出会变成多少？为什么？`Ordering::Relaxed` 这个参数可以忽略。

（来源：Rust by Example 与 Rust Reference 1.97.1；`safetensors` v0.8.0；`ROCm/ATOM` 提交 `43f5393`；数字和报错是本机 rustc 1.97.1 的实测。课程记录和断点已更新，未提交。）

---

**037 · 用户** · `2026-10-13T08:23:28.103Z` · `msg-0cf7fc085bd0aa95fb68`

噢enum里载荷还能带名字啊。请你把带字段名的变体的RequestState以及Tree { Leaf(u32), Node(Box<Tree>, Box<Tree>) } 的内存布局情况添加到图解页对应位置里。

---

**038 · 助手** · `2026-10-13T08:26:28.538Z` · `msg-5e2094d1f47bd65c4cf2`

正在核对图解页的改动（颜色约定、脚本语法、截图），马上发布。

---

**039 · 助手** · `2026-10-13T08:28:26.453Z` · `msg-a8130ec5db55a3d85d23`

对，变体的载荷可以带名字，写法和 struct 的三种形式一一对应：不带数据、按位置（`Running(u32, u32)`）、带字段名（`Running { worker: u32, generated: u32 }`）。字段名只存在于代码里，不占内存，两种写法本机都是 24 字节。

两个类型都加进图解页了：<https://claude.ai/artifact/UAdb78pBPSLcVT9FtHqVuB>（仓库里的源文件是 [memory-layout.html](docs/rust-learning/attachments/02-data-shapes/memory-layout.html)）。

**“enum”一节**，类型按钮里多了 `Tree` 和 `RequestState`，可以逐个变体切换着看字节：

- **`RequestState`（24 字节）**：和 `WebEvent` 是同一种放法。`Failed { error: String }` 占满 24 字节；其余三个变体的标签借用 `String` 容量用不到的取值，本机依次是 `0x8000…0000`、`…0001`、`…0002`。`Running { worker: 3, generated: 17 }` 的两个字段是偏移 8 和 12 处并排的两个 `u32`。
- **`Tree`（16 字节）**：`Leaf(7)` 的前 8 字节全是 0，表示 `Leaf`，7 在偏移 8 处；`Node(…)` 的 16 字节是两个堆地址。
- **新增“定义”一栏**：每个类型现在都显示它的定义。`Option<u32>` 那里写明了它就是 `enum Option<T> { None, Some(T) }`，`T` 填的是 `u32`。

**“链表与 Box”一节**，末尾加了一个二叉树的小图：变量 `t` 里是两个指针，各指向堆上一个 16 字节的叶子，格子宽度按字节数画。

改动时发现并修了一处问题：新加的“定义”栏在窄屏上会把整个面板撑宽，现在长代码只在自己的框里横向滚动。

字节都读自本机 rustc 1.97.1 的一次运行，地址每次运行不同。页面改动和课程记录都还没有提交。综合验收的三道题仍在等你回答。

---

**040 · 用户** · `2026-10-13T08:30:39.613Z` · `msg-97462ac8d0e72c5cd74f`

我发现这些内存都是对齐8的。所以大小都是对齐8吗？

---

**041 · 助手** · `2026-10-13T08:31:09.263Z` · `msg-ce0a1a1c4ca3e7128585`

不是。对齐是 8 的只是含有指针、`usize` 或 `u64` 的类型，而你最近看的几个类型恰好都含有这些。规则是三条：

1. **每个基本类型有自己的对齐，一般等于它的大小。** `u8` 是 1，`u16` 是 2，`u32` 是 4，`u64`、`usize` 和各种指针是 8。
2. **复合类型的对齐，等于它的字段里最大的那个对齐。**
3. **大小是对齐的整数倍。**

所以对齐不是 8 的类型很多，本机实测：

| 类型 | 大小 | 对齐 | 为什么 |
| --- | --- | --- | --- |
| `struct Rgb { r: u8, g: u8, b: u8 }` | 3 | 1 | 全是 `u8` |
| `[u8; 5]` | 5 | 1 | 元素是 `u8` |
| `struct Pair { a: u16, b: u8 }` | 4 | 2 | 最大的是 `u16`，3 凑成 2 的倍数是 4 |
| `Number { Zero, One, Two }` | 1 | 1 | 只有 1 字节的标签 |
| `Color` | 4 | 4 | 只有 4 字节的标签 |
| `Device { Cpu, Cuda(u32) }` | 8 | 4 | 大小碰巧是 8，对齐只有 4 |
| `Tree`、`RequestState`、`String` | 16、24、24 | 8 | 里面有指针或 `u64` |
| `struct Wide { a: u8, b: u128 }` | 32 | 16 | `u128` 的对齐是 16，比 8 还大 |

图解页“enum”一节里的 `Color` 就是 4 字节，不是 8 的倍数。

**为什么大小要是对齐的整数倍**：为了放进数组。数组里第 i 个元素在偏移 i × 大小处，大小是对齐的整数倍，每个元素才都落在对齐的地址上。本机 `[Pair; 2]` 的两个元素地址相差 4，`[Rgb; 2]` 的两个元素地址相差 3。

回头看你那道题：`Tree` 里有 `Box`，对齐是 8，所以按“标签 4 + 两个指针 16”算出的 20 要凑成 24。换成对齐为 4 的类型，20 就是合法的大小。

实际代码里的类型大多含有指针、`String` 或 `Vec`，所以在 64 位机器上经常看到 8。

（数字是本机 rustc 1.97.1、x86_64 Linux 的实测。）

---

**042 · 用户** · `2026-10-13T08:35:30.374Z` · `msg-93223c9ac10d2cbc4bb7`

对齐的是最大的字段的基本类型大小是吗？复合类型里面有一个[u32;100]，对齐的是u32，而不是100个u32是吗？

---

**043 · 助手** · `2026-10-13T08:35:48.480Z` · `msg-c522c11bdb14556b99a7`

对，取的是 `u32` 的对齐，不是 100 个 `u32` 的大小。数组的对齐就等于它元素的对齐，和有多少个元素无关。

只把说法收紧一点：比的是各字段的**对齐**，不是大小。对齐会一层层往里传，最后落到最里面的基本类型上：

- **数组**：对齐等于元素的对齐。
- **struct 和 enum**：对齐等于各字段里最大的那个对齐。

本机实测：

| 类型 | 大小 | 对齐 |
| --- | --- | --- |
| `[u32; 100]` | 400 | 4 |
| `struct S { tag: u8, data: [u32; 100] }` | 404 | 4 |
| `struct T { tag: u8, data: [u8; 100] }` | 101 | 1 |
| `struct U { tag: u8, data: [u64; 100] }` | 808 | 8 |
| `struct Pair { a: u16, b: u8 }` | 4 | 2 |
| `struct Deep { flag: u8, items: [Pair; 10] }` | 42 | 2 |

`S` 里最大的字段有 400 字节，但对齐只是 4，所以 1 + 400 凑成 4 的倍数是 404。`Deep` 是嵌了两层的例子：`items` 是 `Pair` 的数组，`Pair` 的对齐来自里面的 `u16`，所以一路传上来是 2。

“基本类型的对齐等于它的大小”在这台机器上对整数和浮点数成立，但这是平台的规定，不是语言的规定。比如在 32 位 x86 上，`u64` 是 8 字节，对齐却是 4。所以判断时看对齐，不要拿大小代替。

（数字是本机 rustc 1.97.1、x86_64 Linux 的实测；32 位 x86 那一条来自该平台的 C ABI 约定，本机没有试。）

---

**044 · 用户** · `2026-10-13T09:18:46.345Z` · `msg-c96deb5158620d358d83`

1. 我理解的是Rust里不用这两样。rust中对应的是一个&[u8]胖指针。这里就带有两个字，一个数据指针和一个长度值。但如果需要表示可能没有，那么可以用enum Option再包一层，就是Option<&[u8]>.在C中，这两样参数的内存占用一共是8+8=16字节。在rust中，&[u8]胖指针的大小也是指针空间8+长度8=16字节。对于Option，此处由于指针不会为0，0可以直接表示None，就不会再多标签空间了。所以rust里也还是16字节。内存占用没有变大。其中，rust多保证了长度参数和数据地址绑定，不会出现传错的情况。而且还避免使用空指针，空情况Option直接就是None，而不是靠约定。代价是增加了更多编译器检查。
2. （1）enum中，大小需要和最大的变体对齐。所以一个Partial也占Complete全部字段的188字节。但由于还要对齐8，所以还要多4个字节。总共占192字节。token ids的类型是Vec<u32>，里面的token id分配在堆上。（2）可以尝试将TokenLogprobs、MatchedStop、Usage等自定义的类型用Box取指针，而不是整个类型放在里面。但代价是增加了代码复杂度以及将这些自定义的东西分配放到了堆上。我觉得只有在发现由于Partial占用空间过大导致产生性能瓶颈问题时才需要改。（3）此时编译器不会有提示，因为match里写了_的情况判断。但程序跑起来会显示StopSequence时也是非正常结束。这个函数当初不应该写_的兜底全判false，而是应该逐个情况判断，这样就会在增加一个变体时编译器要求消费处要增加处理方式。代价是多写一些啰嗦代码。
3. Const是编译期内联，main里面的两行代码相当于都变成AtomicU64::new(0).fetch_add(1, Ordering::Relaxed)。就做了两次0+1，输出变成1.

---

**045 · 助手** · `2026-10-13T09:23:43.781Z` · `msg-c1380a245f4d0e83181e`

正在记录综合验收的结果，并核对两个要反馈给你的数字。

---

**046 · 助手** · `2026-10-13T09:24:46.135Z` · `msg-668b8a559c4c4b9c28c6`

**综合验收：通过。** O1–O3 的理解证据够了。三题的结论和理由都站得住，补三处。

- **第 1 题：代价说偏了。** 对应关系、16 字节、长度与地址绑定、“没有”不靠约定，这些都对；本机 `Option<&[u8]>` 确实是 16 字节。但代价不是“更多编译器检查”，编译期的检查不花运行时间。真正的代价有两样：
  - **运行时的边界检查**：每次 `data[i]` 都要比较一次，不通过就 panic。
  - **必须写出来的分支**：`None` 的情况不处理就拿不到数据。

  另外，题里那个单独的可空指针 `T *p` 对应 `Option<&T>` 或 `Option<Box<T>>`，是 8 字节。
- **第 2 题 (2)：要缩小的是最大的那个变体。** 方向、代价和“成了瓶颈才改”的判断都对。但 enum 的大小由 `Complete` 决定，所以只动 `Partial` 里的字段没有用。本机试了三种改法：

  | 改法 | 整个 enum 的大小 | 每个 `Complete` 多几次堆分配 |
  | --- | --- | --- |
  | 只把 `Partial` 里的 `TokenLogprobs` 装箱 | 192，没变 | 0 |
  | 把自定义类型的字段逐个装箱 | 136 | 最多 4 次 |
  | 把 `Complete` 的全部字段整体装进一个 `Box` | 48 | 1 次 |

  `Usage` 只有 12 字节，装箱后指针就占 8 字节，还多一次分配，不划算。
- **第 3 题：机制对，输出是 0。** “每次使用都是一份新的 `AtomicU64::new(0)`”完全正确。漏的是第三行：`ACTIVE.load(…)` 也是一次使用，读的是又一份新的 0。前两份各自加到 1，然后就被丢掉了。

第 2 题 (1) 的 192 和 (3) 都对，上次留下的“按对齐凑整”和“`_` 的代价”两处复查通过。

---

## 练习约定 P1（版本 1），请确认

**为什么做**：O4 是“用元组、切片、struct 和 enum 给一个小领域建模”，需要实践证据。到现在为止这一课你还没有亲手写过代码。

**你交付什么**：在 `rust/lesson02_data_shapes/src/lib.rs` 里完成五件事，大约 60 到 80 行。文件开头我会给出教程里的三个类型 `Matrix`、`Point`、`Rectangle`，其余都由你写，包括类型定义。前两件是教程的 Activity，后三件是本课的贯穿案例。

1. **`transpose(matrix: Matrix) -> Matrix`**：2×2 矩阵转置，`Matrix(a, b, c, d)` 变成 `Matrix(a, c, b, d)`。
2. **`rect_area(rect: Rectangle) -> f32` 和 `square(top_left: Point, side: f32) -> Rectangle`**：面积用嵌套解构取出四个坐标，结果不为负。`square` 以给定的点为左上角，向右、向下各延伸 `side`。y 轴向上，和教程示例一致。
3. **`Dtype`**：不带数据的 enum，变体是 `U8`、`I32`、`F32`、`BF16`、`F64`。方法 `bitsize(self) -> usize` 返回一个元素的位数，用 `match` 写，不用 `_`。
4. **`Device`**：变体是 `Cpu` 和 `Cuda(u32)`。方法 `name(&self) -> String` 返回 `cpu` 或 `cuda:3` 这样的名字。
5. **`TensorInfo`**：struct，三个公开字段 `dtype: Dtype`、`shape: Vec<usize>`、`data_offsets: (usize, usize)`。两个方法：
   - `byte_len(&self) -> Option<usize>`：各维相乘得元素个数，再乘位数、除以 8。空 shape 算 1 个元素。任何一步溢出返回 `None`。
   - `slice<'a>(&self, data: &'a [u8]) -> Option<&'a [u8]>`：返回 `data` 里这个张量的字节。起止颠倒、超出 `data`、长度和 `byte_len` 不一致、`byte_len` 溢出，都返回 `None`，不能 panic。

**验收项**：

| ID | 可观察标准 | 检查方式 |
| --- | --- | --- |
| A1 | `transpose` 正确，转置两次得到原矩阵 | 测试 `a1_transpose` |
| A2 | `rect_area` 正确，两个角给反时也不为负；`square` 的两个角正确 | 测试 `a2_rectangle` |
| A3 | `Dtype` 五个变体的位数正确；占 1 字节，能复制、能用 `==` 比较；`match` 里没有 `_` | 测试 `a3_dtype`，加读代码 |
| A4 | `Device` 的名字正确，能用 `==` 比较 | 测试 `a4_device` |
| A5 | `byte_len`：普通形状、空 shape、含 0 的维度、两处溢出 | 测试 `a5_byte_len` |
| A6 | `slice`：取出的字节正确；四种坏输入都返回 `None` | 测试 `a6_slice` |
| A7 | 通过 `cargo fmt --check` 与 `cargo clippy -- -D warnings`；不用 `unwrap`、`expect`、`unsafe` | 命令 |
| A8 | 说明 `slice` 的四种坏输入各由哪一步拦住；`byte_len` 里的 `checked_mul` 换成 `*` 后，测试在调试构建和发布构建下各会怎样 | 你的说明，按要点核对 |
| A9 | A1–A8 通过后的无提示小变式：实现一个新的小类型并通过测试 | 测试 |

**运行方式**：单项是 `bash scripts/host-cpu.sh run -- cargo test -p rust-lesson02-data-shapes --test a1_transpose`，去掉 `--test …` 就是全部。完成之前，整个 workspace 的 `host-cpu.sh test` 和 `host-cpu.sh lint` 会在这个 crate 上失败。

**练习会用到、但还没讲过的写法**，都很小：

- **`pub`**：类型、字段、函数前都要加，测试才看得见。
- **定义上方的 derive**：`Dtype` 写 `#[derive(Debug, Clone, Copy, PartialEq, Eq)]`，`Device` 写 `#[derive(Debug, PartialEq, Eq)]`，`TensorInfo` 写 `#[derive(Debug, Clone, PartialEq, Eq)]`。`Clone, Copy` 表示赋值时直接复制，和 C 的枚举一样；`PartialEq, Eq` 让它能用 `==`，测试里要比较。
- **`#[must_use]`**：返回值的公开函数上方要加，第 01 课的 `status_line` 上你加过。
- **`A | B => …`**：`match` 里两个变体走同一个分支。两个分支结果相同时，Clippy 会要求合并成这样。
- **`?` 用在 `Option` 上**：`let v = x.checked_mul(y)?;` 的意思是，是 `Some(v)` 就取出 `v` 往下走，是 `None` 就让当前函数立刻返回 `None`。和第 01 课 `write!(…)?` 是同一个符号。
- **遍历 `Vec`**：`for dim in &self.shape { … }`，这里 `dim` 是 `&usize`，用 `*dim` 取出数。
- **`slice` 签名里的 `'a`**：意思是返回的切片是从 `data` 借来的，和 `self` 无关。照抄即可，第 09 课讲。
- **两个小方法**：`(a - b).abs()` 取绝对值；`String::from("cpu")` 从字面量造 `String`。

**文件边界**：

| 边界 | 路径 |
| --- | --- |
| 你写 | `rust/lesson02_data_shapes/src/lib.rs` |
| 我维护 | `rust/lesson02_data_shapes/Cargo.toml`；`rust/lesson02_data_shapes/tests/`；根 `Cargo.lock`；本课记录；`docs/rust-learning/README.md` 的 Checkpoint |
| 我只读 | `docs/rust-by-example/src/primitives/`、`docs/rust-by-example/src/custom_types/` |
| 本次不动 | 其他 crate、CI 配置和依赖 |

**求助如何影响证据**：随时可以问。透露了关键写法只影响相应的验收项，之后用一个小变式在无提示下恢复。A9 期间不给提示。

**非目标**：不引入第三方依赖；不做性能要求；教程 Activity 里给 `Matrix` 加 `Display` 是第 01 课的复习，不在本次范围。

**完成门槛**：A1–A9 全部通过，阻塞问题全部关闭。

你回复“接受”后，我再创建这个 crate 和验收测试，确认它们按预期失败，然后交给你。想改哪一项直接说。

（课程记录和断点已更新，未提交。）

---

**047 · 用户** · `2026-10-13T09:34:39.541Z` · `msg-016aa475ea98c2e531a5`

把 Complete 的全部字段整体装进一个 Box是怎么做到的？

---

**048 · 助手** · `2026-10-13T09:35:12.529Z` · `msg-2c2d15636e81e61cdbf0`

分两步：先把 `Complete` 的字段搬进一个单独的 struct，再让这个变体只带一个指向它的 `Box`。

```rust
// 第一步：原来 Complete 里的字段，原样搬进一个 struct
pub struct CompleteData {
    token_ids: Vec<u32>,
    finish_reason: FinishReason,
    matched_stop: Option<MatchedStop>,
    usage: Usage,
    // 其余 3 个字段
}

// 第二步：Complete 从“带一堆字段”改成“带一个 Box”
pub enum TokenChunk {
    Partial {
        token_ids: Vec<u32>,
        logprobs: Option<TokenLogprobs>,
    },
    Complete(Box<CompleteData>),
}
```

必须先有 struct，是因为 `Box<T>` 的尖括号里要填一个类型，而变体本身不是类型。本机写 `Box<X::A>` 报 E0573：`expected type, found variant`。

**内存里的变化**，本机实测：

```text
改之前，每个值 192 字节
  Partial    [token_ids 24][logprobs 24][          用不到          ]
  Complete   [                 全部字段 188                 ][凑整 4]

改之后，每个值 48 字节
  Partial    [token_ids 24][logprobs 24]
  Complete   [Box 指针 8][   用不到   ] ───► 堆上 192 字节：CompleteData
```

最大的变体从 `Complete` 的 188 字节变成了 `Partial` 的 48 字节。`Complete` 的数据没有变小，只是搬到了堆上，值里只留 8 字节的指针。

**用起来的两处变化**：

```rust
// 构造：多一层 Box::new
let last = TokenChunk::Complete(Box::new(CompleteData {
    token_ids: vec![42],
    finish_reason: FinishReason::Stop,
    // …
}));

// 读取：先拿到 Box，再用 . 取字段
match chunk {
    TokenChunk::Partial { .. } => None,
    TokenChunk::Complete(data) => Some(data.usage.total_tokens),
}
```

`data` 是 `Box<CompleteData>`，`data.usage` 里的 `.` 会自动穿过 `Box` 去取字段，不用写 `(*data).usage`。

**代价**是每造一个 `Complete` 要做一次堆分配，读它的字段时多跳一次指针，所有构造和匹配 `Complete` 的代码都要跟着改。一次请求只有一个 `Complete`，所以分配只多一次。

这和节点 6 里 `Job` 的做法是同一招：`AddWorker { config: Box<WorkerConfigRequest> }`，那里是把大的字段单独装箱，这里是把整个变体的字段打包后装箱。

练习约定 P1 还在等你确认。

---

**049 · 用户** · `2026-10-13T09:40:16.162Z` · `msg-1b2f5f9515f771d6b993`

噢，是再通过中间的struct来间接获取内部字段是吧。我接受练习约定。

---

**050 · 助手** · `2026-10-13T09:42:22.040Z` · `msg-29c1c69a86e7e3ca8bea`

对，变体里只留一个 `Box`，字段都在它指向的那个 struct 里，取字段时经过这层指针。

练习已经建好，可以开始写了。

**你要写的文件**：[rust/lesson02_data_shapes/src/lib.rs](rust/lesson02_data_shapes/src/lib.rs)。里面现在只有教程的三个类型 `Matrix`、`Point`、`Rectangle`，其余都由你添加。

**验收测试**在 [rust/lesson02_data_shapes/tests/](rust/lesson02_data_shapes/tests/)，六个文件共 29 项，请不要改动：

| 文件 | 检查什么 |
| --- | --- |
| `a1_transpose.rs` | 转置结果；转置两次回到原矩阵；对称矩阵不变 |
| `a2_rectangle.rs` | 面积等于宽乘高；两个角给反时仍为正；退化成线时为 0；`square` 的两个角 |
| `a3_dtype.rs` | 五个变体的位数；`Dtype` 占 1 字节，能复制、能比较 |
| `a4_device.rs` | `cpu`、`cuda:0`、`cuda:15`；能比较 |
| `a5_byte_len.rs` | 普通形状；真实的 embedding 表（152064 × 3584 的 BF16，应得 1,089,994,752）；空 shape；含 0 的维度；两处溢出 |
| `a6_slice.rs` | 取出的字节和位置正确；空张量；越界、起止颠倒、长度不符、溢出都返回 `None` |

**运行**：

```bash
# 单项
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson02-data-shapes --test a1_transpose
# 全部
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson02-data-shapes
# A7 的两条检查
bash scripts/host-cpu.sh run -- cargo fmt -p rust-lesson02-data-shapes --check
bash scripts/host-cpu.sh run -- cargo clippy -p rust-lesson02-data-shapes --all-targets -- -D warnings
```

现在六个测试文件都编译不过，报的都是 E0432：找不到 `transpose`、`Dtype` 这些名字。这是预期的起点，你每写完一项，对应的那个文件就能编译并运行。建议按 A1 到 A6 的顺序做，每项单独跑。

两点提醒：

- **格式**：`cargo fmt -p rust-lesson02-data-shapes`（不带 `--check`）会直接帮你排好。
- **Clippy 的提示**：它会给出改法，照着改即可。约定里列的 `#[must_use]`、`A | B`、`?` 都属于这一类。

写完告诉我，并附上 A8 的说明。中途卡住随时问。

我这边做过的核对：测试先用我自己的一份参考实现跑过，29 项全过，Clippy 也通过；另外试了 19 种写错的实现，每一种都至少被一项测试拦下。参考实现没有放进仓库。

约定已记入[课程记录](docs/rust-learning/lessons/02-data-shapes.md)，断点已更新。根目录的 `Cargo.lock` 多了这个 crate 的一条记录。以上改动都还没有提交。

---

**051 · 用户** · `2026-10-13T09:45:48.696Z` · `msg-6501e3fb24f8bc8e3f6e`

transpose需要原地修改转置还是转置成一个新矩阵？

---

**052 · 助手** · `2026-10-13T09:45:57.622Z` · `msg-de8b0bd4128c15aa097c`

转置成一个新矩阵并返回，不改原来的。

签名 `transpose(matrix: Matrix) -> Matrix` 已经定了这一点：参数按值传入，函数拿到的是自己的一份；结果通过返回值交出去。这和教程里给的模板 `reverse(pair: (i32, bool)) -> (bool, i32)` 是同一种写法。

调用方手里的矩阵不受影响。`Matrix` 的定义上有 `Clone, Copy`，传进函数时是复制了一份，所以测试里才能在 `transpose(transpose(matrix))` 之后继续拿 `matrix` 来比较。

原地修改会是另一种签名，`fn transpose(matrix: &mut Matrix)`，没有返回值。这次不是这个要求。

约定里我写的是“`Matrix(a, b, c, d)` 变成 `Matrix(a, c, b, d)`”，“变成”这个词有歧义，是我没写清楚，意思是返回值长这样。

---

**053 · 用户** · `2026-10-13T12:31:59.610Z` · `msg-56bf677ab7272d5a4948`

我写好了，但遇到一个报错，请你帮我看看。

<pasted_content id="8858">
test a_zero_dimension_means_no_bytes ... ok
test an_empty_shape_is_a_single_element ... ok
test overflow_in_the_element_count_is_none ... ok
test counts_elements_times_width ... ok
test the_embedding_table_of_a_real_model ... ok
test overflow_when_multiplying_by_the_width_is_none ... FAILED
test the_largest_count_that_still_fits_is_some ... ok

failures:

---- overflow_when_multiplying_by_the_width_is_none stdout ----

thread 'overflow_when_multiplying_by_the_width_is_none' (1233811) panicked at rust/lesson02_data_shapes/tests/a5_byte_len.rs:52:5:
assertion `left == right` failed
  left: Some(18446744073709551608)
 right: None
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    overflow_when_multiplying_by_the_width_is_none

test result: FAILED. 6 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `-p rust-lesson02-data-shapes --test a5_byte_len`
root@ubuntu-8gb-hil-1:~/workspace/learning/programming-lab#
</pasted_content id="8858">

 
我在byte_len方法最后写了checked_mul了，不明白为什么还是溢出了

---

**054 · 助手** · `2026-10-13T12:33:34.727Z` · `msg-bf42230613be34976fbf`

一句话诊断：你的代码没有溢出，`checked_mul` 也在正常工作；失败是因为运算顺序和约定不一样。

**这个测试在算什么**：`shape` 是 `[usize::MAX / 8]`，也就是 2305843009213693951 个元素，类型是 `F64`。

| 算法 | 算式 | 结果 |
| --- | --- | --- |
| 约定：先乘位数，再除以 8 | 2305843009213693951 × 64 | 超出 `usize`，返回 `None` |
| 你的第 97 行：先把位数除以 8，再乘 | 2305843009213693951 × 8 = 18446744073709551608 | 没超出，返回 `Some(…)` |

所以报错里的 `left: Some(18446744073709551608)` 就是你这行算出来的字节数，它确实放得下。从数学上说你的结果没错，这个张量就是这么多字节。测试要 `None`，是因为约定第 5 项规定的行为是“乘位数、除以 8，任何一步溢出返回 `None`”，测试按约定来。

**约定为什么按位算**：这是照着真实的 safetensors 定的。它的 `Dtype` 里有不足一个字节的类型，`Dtype::F4` 只有 4 位。对这种类型，`bitsize() / 8` 等于 0，整个张量会被算成 0 字节。所以它必须先乘位数，检查总位数是不是 8 的倍数，再除以 8。练习里的五个变体都是 8 的倍数，你的算法在正常输入上结果一样，区别只出现在这种接近上限的输入上。

改法就是让第 97 行按约定的顺序来，我不替你写。

另外，我把全部检查跑了一遍，告诉你还剩什么。`cargo test` 默认在第一个失败的测试文件处停下，所以你只看到了 a5。加 `--no-fail-fast` 可以一次看全：

- **测试**：29 项里 27 项通过。除了上面这项，`a6_slice` 还有一项失败：`returns_exactly_the_bytes_between_the_offsets`，期望取出第 4 到 27 号字节，实际得到 `None`。
- **A7 的格式检查**：没通过。运行 `cargo fmt -p rust-lesson02-data-shapes` 会自动排好。
- **A7 的 Clippy**：11 条，分四类：缺 `#[must_use]`（7 条）、两个分支结果相同（1 条）、可以改用 `?`（2 条）、多余的分号（1 条）。每条它都给了改法。
- **和约定对不上的一处**：约定第 2 项写的是 `rect_area` 用嵌套解构取出四个坐标，你现在用的是字段访问。

A1 到 A4 的测试已经全过了。

---

**055 · 用户** · `2026-10-13T12:39:36.848Z` · `msg-2a07e0316f731046e7b8`

<ide_opened_file>The user opened the file /root/workspace/learning/programming-lab/rust/lesson02_data_shapes/src/lib.rs in the IDE. This may or may not be related to the current task.</ide_opened_file>
嵌套解构是什么？这个结构体也能解构？

---

**056 · 助手** · `2026-10-13T12:40:20.696Z` · `msg-6fd922fe20a4f59d331b`

能。解构就是写一个和值形状相同的“模式”，一次把里面各部分取出来并起名字。你的代码里其实已经用了两次：

- 第 100 行 `let (start, end) = self.data_offsets;`，这是解构元组。
- 第 75 行 `Device::Cuda(index) => …`，这是解构 enum 的变体。

struct 也是同一回事，模式写成 struct 的样子。

### 解构一个 struct

用一个和练习无关的小类型举例，下面几种写法本机都编译通过：

```rust
struct Size { w: u32, h: u32 }

let s = Size { w: 800, h: 600 };

let Size { w, h } = s;                    // 取出两个字段，变量就叫 w 和 h
let Size { w: width, h: height } = s;     // 取出来并改名：w 叫 width，h 叫 height
let Size { w: only_w, .. } = s;           // 只要 w，其余用 .. 略过
```

左边的 `Size { … }` 不是在造一个值，而是在描述“右边那个值长什么样”。冒号左边是字段名，右边是你给它起的变量名。

对应 C++17 的结构化绑定 `auto [w, h] = s;`，Python 里是 `w, h = s` 这种拆包。

### 嵌套解构

嵌套的意思是：模式里面再套模式。字段本身是元组或 struct 时，冒号右边不写变量名，而是再写一个模式，一直拆到里面去。

```rust
// 字段是元组：struct 里套元组模式
let TensorInfo { dtype, shape, data_offsets: (start, end) } = info;
// 一条语句得到四个变量：dtype、shape、start、end

// 字段是 struct：struct 里套 struct 模式
struct Window { title: String, size: Size }
let Window { title, size: Size { w: cols, h: rows } } = win;
// 得到 title、cols、rows
```

`size: Size { w: cols, h: rows }` 读作：`size` 这个字段是一个 `Size`，把它的 `w` 取出来叫 `cols`，`h` 取出来叫 `rows`。

### 和字段访问比，好处在哪

`win.size.w` 这种写法也能拿到数据。解构多出来的是一项检查：模式里必须把字段列全，漏了就编译不过。本机写 `let Size { w } = s;` 报 E0027：``pattern does not mention field `h` ``，要么补上，要么明确写 `..` 表示不要。所以以后给 struct 加字段，所有没写 `..` 的解构处都会被编译器指出来。这和 `match` 不写 `_` 是同一个道理。

### 回到练习

`Rectangle` 的两个字段都是 `Point`，所以每个字段冒号右边要写的是一个 `Point` 的模式。一条 `let` 可以直接得到四个坐标。这一步你来写。

**读哪里**：教程 [structs.md](docs/rust-by-example/src/custom_types/structs.md)（[在线](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/structs.html)）示例里的 `let Point { x: left_edge, y: top_edge } = point;` 和 `let Pair(integer, decimal) = pair;` 就是解构，页面末尾的 Activity 提示用嵌套解构。

（示例和报错是本机 rustc 1.97.1 的实测。）

---

**057 · 用户** · `2026-10-13T12:57:51.005Z` · `msg-412ba83ca0dd176041b8`

好了，我修改了。请你review吧。

---

**058 · 助手** · `2026-10-13T13:01:28.222Z` · `msg-cbdfd5d6bfcce3620c2c`

**Review 结论：按版本 1 的检查，全部通过；读代码另外发现两处，需要你确认一次约定的修订。**

**验证证据**（刚才复验的）：

- 验收测试和 `Cargo.toml` 没有被改动。
- `cargo test`：29 项全部通过。
- `cargo fmt --check` 和 `cargo clippy --all-targets -- -D warnings`：都通过。
- 没有 `unwrap`、`expect`、`unsafe`，`match` 里没有 `_`。

A1、A3、A4、A5、A7 通过。`byte_len` 现在的顺序和约定一致，`transpose` 也改成了解构。

### 读代码发现的两处

**F1：`slice` 把位于缓冲区末尾的空张量拒绝了。**

| 输入 | 约定的行为 | 你的代码 |
| --- | --- | --- |
| 28 字节的缓冲区，`shape = [0]`，偏移 `(28, 28)` | 返回空切片 | `None` |
| 空缓冲区，`shape = [0]`，偏移 `(0, 0)` | 返回空切片 | `None` |

`28..28` 这个区间一个字节都不取，也没有超出缓冲区，所以不属于约定里那四种坏输入。问题出在第 107 行的条件里。真实文件里，最后一个张量为空时就是这种偏移。

这一处**是我的测试漏了**：我只在缓冲区中间放了空张量，没有放在末尾，所以 29 项测不出来。我在仓库外用你代码的副本补试了三项，两项失败。

**F2：`rect_area` 还是字段访问。** 约定第 2 项写的是用嵌套解构取出四个坐标。你把解构用在了 `transpose` 上，那里是对的，但 `rect_area` 没有改。这一处**是我的约定写得不一致**：交付说明里写了要求，验收表 A2 的检查方式却只写了测试。

### 约定版本 2，请确认

两处都是澄清，不算你的问题，但它们改变了通过的标准，所以需要你重新接受：

1. **A2**：检查方式增加“读代码：`rect_area` 用嵌套解构取出四个坐标”。
2. **A6**：写明空张量的边界。起止相等时，只要不超过 `data` 的长度就返回空切片，包括两者都等于 `data` 的长度、以及 `data` 本身为空；超过则仍返回 `None`。我往 `a6_slice.rs` 里加三项测试。

其余不变。你接受之前我不动测试文件。

### 接下来

1. 回复是否接受版本 2。
2. 修 F1 和 F2。
3. 提交 A8 的说明：`slice` 的四种坏输入各由哪一步拦住；`byte_len` 里的 `checked_mul` 换成 `*` 后，测试在调试构建和发布构建下各会怎样。

### 不影响通过的两点观察

- **`bitsize(&self)`**：约定写的是 `bitsize(self)`。`Dtype` 只有 1 字节而且能复制，按值传更直接；`&self` 传的是一个 8 字节的指针。两种写法测试都能过。
- **derive 行少了 `Eq`**：你照着 `Matrix` 那几个类型写的，它们不能加 `Eq` 是因为里面有 `f32`，而 NaN 不等于自己。`Dtype`、`Device`、`TensorInfo` 里只有整数，可以加。

课程记录里已经记下这次提交、两处问题和待确认的版本 2，都还没有提交到 Git。

---

**059 · 用户** · `2026-10-13T13:08:06.991Z` · `msg-cf93b007d7d71dd18ae9`

为什么经常说要用嵌套解构获取内部元素呢？嵌套结构比起字段访问有什么优势吗？rect_area 用嵌套解构，还需要预先多一步声明变量，字段访问可以直接开始计算边长了。

---

**060 · 助手** · `2026-10-13T13:10:19.774Z` · `msg-9fca43ce5d8409733b35`

在 `rect_area` 这个函数里，嵌套解构没有优势，你的写法没问题。你说的代价也对：多一行，多四个名字。

我反复提它，只是因为约定里写了。约定这样写是照搬教程 Activity 的提示（try using nested destructuring），用意是找个地方练模式的写法，并不是因为这里解构更好。这一点我之前没说清楚。

### 两种写法各自适合什么

| 情况 | 更合适的 | 原因 |
| --- | --- | --- |
| 带字段名的 struct，读几个字段 | 字段访问 | 名字已经有了，`rect.top_left.y` 直接、少一行。`rect_area` 属于这种 |
| 元组、元组结构体 | 解构 | `.0`、`.2` 看不出含义，解构能起名字。你写的 `let (start, end) = self.data_offsets;` 和改后的 `transpose` 就是 |
| enum 的载荷 | 只能用模式 | 字段访问进不去，本机对 enum 写 `w.bootstrap_port` 报 E0609 |
| 要同时判断好几层的形状 | 嵌套模式 | 判断和取值一步完成，见下面的例子 |
| 希望加字段时被编译器提醒 | 不带 `..` 的解构 | 上次说的 E0027 |

所以嵌套模式真正的用武之地在 `match` 里，不在对普通 struct 的 `let` 上。

### 嵌套模式有用的例子

`atom/mesh/src/core/worker.rs` 里打印 worker 类型的代码，是 `match` 套 `match`：

```rust
match self {
    WorkerType::Regular => write!(f, "Regular"),
    WorkerType::Prefill { bootstrap_port } => match bootstrap_port {
        Some(port) => write!(f, "Prefill(bootstrap:{})", port),
        None => write!(f, "Prefill"),
    },
    WorkerType::Decode => write!(f, "Decode"),
}
```

用嵌套模式可以压平成四个并列的分支。本机验证过，两种写法输出相同：

```rust
match self {
    WorkerType::Regular => write!(f, "Regular"),
    WorkerType::Prefill { bootstrap_port: Some(port) } => write!(f, "Prefill(bootstrap:{})", port),
    WorkerType::Prefill { bootstrap_port: None } => write!(f, "Prefill"),
    WorkerType::Decode => write!(f, "Decode"),
}
```

`bootstrap_port: Some(port)` 一次做了三件事：确认是 `Prefill`，确认端口是 `Some`，把端口取出来叫 `port`。穷尽检查照样管用：删掉 `None` 那一行，本机报 E0004，指出 `Prefill { bootstrap_port: None }` 没有覆盖。字段访问做不到这些。上游选的是第一种写法，两种在真实代码里都常见。

### 运行时

没有实质差别。两种写法读的是同样的 16 个字节，变量名在编译后不存在。本机用 `-O` 编译 `rect_area` 的两个版本，都只是取数、相减、相乘，没有函数调用，也没有多出来的内存复制。指令数是字段访问 7 条、解构 8 条，多的那一条是在寄存器里调换位置。

### 对约定的影响

既然这里解构没有实际好处，我不该把它设成通过条件。**版本 2 的提议改成这样**：

1. **A2**：删掉“用嵌套解构”的要求，`rect_area` 保持你现在的写法。F2 撤回。
2. **A6**：不变，还是上一条说的空张量边界和三项新测试。

嵌套模式的练习挪到 A9 的小变式里，放在 `match` 中，那里它是自然的写法。

接下来三件事：回复是否接受修订后的版本 2；修 F1；提交 A8 的说明。

（代码来自 `ROCm/ATOM` 提交 `43f5393`；报错和指令数是本机 rustc 1.97.1 的实测，指令数只代表这一次编译。）

---

**061 · 用户** · `2026-10-13T13:15:48.665Z` · `msg-b3a5e17e328478215b02`

噢，对于这种多层match的判断就可以一次性优雅地完成。这个workertype的例子很有意义。可以加到图解页中。我接受版本2，已经修了F1.

---

**062 · 助手** · `2026-10-13T13:18:55.169Z` · `msg-020001aef4b852cb880d`

图解页的新一块已经写好，正在看渲染结果，然后发布。

---

**063 · 助手** · `2026-10-13T13:19:34.527Z` · `msg-40b92ee8c2b4186e0951`

`WorkerType` 的例子已经加进图解页，版本 2 也已生效。但 **F1 在磁盘上的文件里还没有修好**，先说这个。

### F1 还没关闭

我读到的 [lib.rs](rust/lesson02_data_shapes/src/lib.rs) 是 13:04 保存的版本。和上一轮相比只有一处变化：第 108 行 `return None;` 的分号没了。第 107 行的条件还是原样：

```rust
if (start >= len) || (end > len) || (start > end) {
```

版本 2 的三项测试已经加进 `a6_slice.rs`，复验结果：

| 检查 | 结果 |
| --- | --- |
| `cargo test` | 32 项里 30 项通过。失败的是 `an_empty_tensor_at_either_end_is_an_empty_slice` 和 `an_empty_tensor_in_an_empty_buffer_is_an_empty_slice`，都是期望空切片、实际得到 `None` |
| `cargo fmt --check` | 没通过，要求把第 108 行的分号加回去 |
| `cargo clippy` | 通过 |

可能是你改了但编辑器里没保存，请确认一下文件内容。单独跑这一项的命令：

```bash
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson02-data-shapes --test a6_slice
```

### 图解页

<https://claude.ai/artifact/UAdb78pBPSLcVT9FtHqVuB>，“enum”一节下面多了一块“用 match 读出来：两层判断，一个模式”：

- **选一个值**：`Regular`、`Prefill { bootstrap_port: Some(8998) }`、`Prefill { bootstrap_port: None }`、`Decode`。
- **两种写法并排**：上游的 `match` 套 `match`，和压平后的嵌套模式。选中的值走到的分支会高亮，下面写明走了几步、`port` 绑到了什么。
- **这个值的 4 个字节**：本机实测，`Prefill { bootstrap_port: Some(8998) }` 是 `01 00 26 23`。

量字节时有个发现，正好呼应你说的“一次性完成”：代码里的两层判断，在内存里本来就合在开头的 2 个字节里。0 和 1 是 `Prefill` 的端口为 `None` 和 `Some`，2 是 `Regular`，4 是 `Decode`。`Option<u16>` 自己的标签只用 0 和 1，编译器把另外两个变体记在了同一个位置上，所以整个 `WorkerType` 只有 4 字节。

### 约定

版本 2 已记为接受。F2 撤回，`rect_area` 保持现在的写法。

### 接下来

1. 让第 107 行的修改落到文件里，并把第 108 行的分号加回去（或运行 `cargo fmt -p rust-lesson02-data-shapes`）。
2. 提交 A8 的说明：`slice` 的四种坏输入各由哪一步拦住；`byte_len` 里的 `checked_mul` 换成 `*` 后，测试在调试构建和发布构建下各会怎样。

这两项过了之后我发 A9 的小变式。课程记录和图解页的改动都还没有提交到 Git。

---

**064 · 用户** · `2026-10-13T13:32:43.490Z` · `msg-1f07de0975bbd49a6e0a`

可能我刚才修改没报错好。我这边是这样的。请你再读一次试试看。

---

**065 · 助手** · `2026-10-13T13:34:08.183Z` · `msg-53c1ea17598d74133293`

这次读到了。文件是 13:31 保存的，第 107 行已经是 `start > len`，第 108 行的分号也在。

**复验结果：A1–A7 全部通过，F1 关闭。**

| 检查 | 结果 |
| --- | --- |
| 验收测试文件 | 没有被改动，是版本 2 的那一套 |
| `cargo test` | 32 项全部通过，其中 `a6_slice` 12 项 |
| `cargo fmt --check` | 通过 |
| `cargo clippy --all-targets -- -D warnings` | 通过 |
| `unwrap`、`expect`、`unsafe`、`match` 里的 `_` | 都没有 |

你的改法是对的：`start == len` 时区间 `len..len` 一个字节都不取，没有超出缓冲区，所以只有 `start > len` 才该拒绝。

一点观察，不用改：这三个比较正是容易差一的地方，这次的问题就出在 `>=` 和 `>` 上。串讲里 safetensors 用的 `data.get(start..end)` 把这三种情况一次判完，越界或起止颠倒都返回 `None`，不用自己写比较。

**还差两项**：

1. **A8，你的说明**。两个问题：
   - `slice` 的四种坏输入（起止颠倒、超出 `data`、长度和 `byte_len` 不一致、`byte_len` 溢出）各由你代码里的哪一步拦住？
   - 把 `byte_len` 里的 `checked_mul` 换成普通的 `*`，测试在调试构建和发布构建下各会怎样？
2. **A9，无提示的小变式**。A8 过了之后我发。

课程记录已更新，还没有提交到 Git。

---

**066 · 用户** · `2026-10-13T13:48:25.427Z` · `msg-31dc56461ee4dc95e35b`

1. 起止颠倒被(start > len)拦，超出data被(end > len) || (start > end)拦，长度不一致被byte_len != (end - start)拦，byte_len 溢出则是在byte_len 方法内部被拦住。

---

**067 · 助手** · `2026-10-13T13:49:38.648Z` · `msg-6351b50297669921571d`

四项里两项对，另外两项写反了。

| 坏输入 | 你说的 | 实际 |
| --- | --- | --- |
| 长度不一致 | `byte_len != (end - start)` | 对 |
| `byte_len` 溢出 | 在 `byte_len` 方法内部被拦住 | 对，补一句：`byte_len` 返回 `None` 之后，是 `slice` 第 110 行的 `?` 把它接着传了出去 |
| 起止颠倒 | `(start > len)` | 是 `(start > end)` |
| 超出 `data` | `(end > len) \|\| (start > end)` | 是 `(end > len)` |

拿两个具体输入走一遍第 107 行，缓冲区 28 字节：

| 输入 | `start > len` | `end > len` | `start > end` |
| --- | --- | --- | --- |
| 起止颠倒：`(20, 10)` | 20 > 28，否 | 10 > 28，否 | 20 > 10，**是** |
| 超出 `data`：`(16, 40)` | 16 > 28，否 | 40 > 28，**是** | 16 > 40，否 |

`len` 和 `end` 长得像，可能是看串了。但这两个比较各管什么要分清，所以换个问法再确认一次。

**还差两个回答：**

1. **A8 的第二问**：把 `byte_len` 里两处 `checked_mul(…)?` 换成普通的 `*`，测试在调试构建和发布构建下各会怎样？
2. **复查**：把第 107 行的 `(start > end)` 去掉，其余不变。输入是 28 字节的缓冲区、`U8`、`shape = [10]`、偏移 `(20, 10)`。代码会走到哪一行出事？调试构建和发布构建各是什么表现？

---

**068 · 用户** · `2026-10-13T13:51:56.690Z` · `msg-48fceed64f9d1c4d9621`

噢，我刚才复制黏贴判断代码复制错了。byte len换成普通的*，会溢出，我记得调试构建里会溢出panic，发布构建会静默溢出。

---

**069 · 助手** · `2026-10-13T13:52:27.690Z` · `msg-78cf887d33ff48c1722a`

语言层面的行为说对了：调试构建在乘法处 panic，发布构建不报错、结果回绕。差的是后半句：回绕之后函数返回什么，测试会不会发现。我在仓库外拿你代码的副本改了试过：

| 构建 | 函数的表现 | 失败的测试 |
| --- | --- | --- |
| 调试 | 乘法处 panic：`attempt to multiply with overflow` | 4 项：`a5_byte_len` 的两项溢出测试，`a6_slice` 的两项 |
| 发布 | 不 panic，`byte_len` 返回 `Some(一个错的数)` | 3 项：`a5_byte_len` 两项拿到的是 `Some(2305843009213693950)` 这类值而不是 `None`，`a6_slice` 一项 |

“静默”的真正含义在 `a6_slice` 那一项里。输入是 `U8`、`shape = [2^61 + 3]`、偏移 `(0, 3)`：

- 元素个数乘 8 位，回绕后正好是 24 位，也就是 3 字节。
- 3 和偏移给出的长度相等，于是 `slice` 返回 `Some([0, 1, 2])`。

一个声称有 2.3×10¹⁸ 个元素的张量，被当成 3 字节的正常张量接受了。没有报错，返回值看起来也正常，后面的代码会拿着这个形状继续算。这就是真实的 safetensors 在校验里用 `checked_mul` 的原因。

`a6_slice` 另一项溢出测试在发布构建下反而通过了：回绕出的数碰巧和 28 不相等，返回了 `None`。这种“碰巧对”说明只靠一组普通的测试发现不了回绕，所以我专门加了上面那个凑好的输入。发布构建的测试用 `cargo test --release` 跑。

复制粘贴的事没关系。不过上一条的复查题还没答，它正好接着这个话题：

> 把第 107 行的 `(start > end)` 去掉，其余不变。输入是 28 字节的缓冲区、`U8`、`shape = [10]`、偏移 `(20, 10)`。代码会走到哪一行出事？调试构建和发布构建各是什么表现？

答完这一题 A8 就过了，接着我发 A9。

---

**070 · 用户** · `2026-10-13T13:58:52.981Z` · `msg-bd3ba53c59d16d4746b8`

你的意思是回绕的数值可能会正巧凑对，导致测试可能发现不了是吗？复查题中，会到end-start那一行计算长度中出事。这里类型是usize，小的减去大的会溢出。调试构建会panic报错，发布构建会回绕到一个很大的usize数。

---

**071 · 助手** · `2026-10-13T14:01:31.936Z` · `msg-4f8c00afdbe1e0d99238`

先回答你的问题：差不多，但“凑对”和“发现不了”其实是两种相反的情况，要分开看。

| 情况 | 回绕出的数 | 函数的行为 | 测试 |
| --- | --- | --- | --- |
| 普通的坏输入 | 和偏移给出的长度对不上 | 返回 `None`，碰巧是正确答案 | 通过，所以发现不了代码有问题 |
| 特意凑好的输入 | 正好等于偏移给出的长度 | 返回 `Some(…)`，坏张量被接受 | 只有专门写这种输入的测试才抓得住 |

所以危险的是第二种：对攻击者来说，形状是他自己填的，凑出一个回绕后正好对上的数并不难。第一种的问题是它给人“测试都过了”的错觉。

**复查题：对。** 走到 `end - start` 那一行，`usize` 小减大溢出，调试构建 panic，发布构建回绕成很大的数。补上最后一步：回绕出的数是 2⁶⁴ − 10，和 `byte_len` 算出的 10 不相等，于是函数返回 `None`。这正是上表的第一种情况。我实测了去掉 `(start > end)` 的版本：

- **调试构建**：`reversed_offsets_are_none` 失败，信息是 `attempt to subtract with overflow`。
- **发布构建**：32 项全部通过。

也就是说，这个检查在发布构建下靠测试是看不出来少了的，调试构建的 panic 才把它暴露出来。

**A8 通过。** A1–A8 都过了，下面是最后一项。

---

## A9：`Placement`（无提示）

这一项期间我不给提示，只报告检查结果。

**场景**：推理引擎要记录每个张量的权重现在在哪里，以及给它分配多少内存。分配时按 64 字节一块对齐，所以要把字节数向上取整到 64 的倍数。

**你要写的**，加在同一个 [lib.rs](rust/lesson02_data_shapes/src/lib.rs) 里：

1. **enum `Placement`**，两个变体：
   - `Unloaded`：还没加载，不带数据。
   - `Loaded`：已加载，带两个有名字的字段，`device: Device` 和 `bytes: usize`。
2. **`gpu_index(&self) -> Option<u32>`**：权重加载在某块 GPU 上时返回它的编号，其余情况返回 `None`。
   - 写法要求：只用一个 `match`，不套 `match`，不用 `_` 和 `if let`。
3. **`padded_bytes(&self) -> Option<usize>`**：把占用的字节数向上取整到 64 的倍数。
   - 0 得 0，1 得 64，64 得 64，65 得 128。
   - `Unloaded` 算 0 字节。
   - 取整后的结果放不进 `usize` 时返回 `None`，不能 panic。

**怎样算通过**：

| 检查 | 方式 |
| --- | --- |
| 行为正确 | 测试 `a9_placement`，8 项 |
| `gpu_index` 的写法符合要求 | 我读代码 |
| 格式和 Clippy | 和 A7 相同的两条命令 |

**运行**：

```bash
bash scripts/host-cpu.sh run -- cargo test -p rust-lesson02-data-shapes --test a9_placement
```

现在这个文件编译不过，报 E0432，找不到 `Placement`，这是预期的起点。在你写出 `Placement` 之前，不带 `--test` 的整套测试也会因此编译失败；原来的六个文件单独跑仍然是 32 项全过。

写完告诉我。

---

**072 · 用户** · `2026-10-13T14:03:37.922Z` · `msg-32fa0c5856372a506982`

> command: /compact

---

**073 · 用户** · `2026-10-14T01:18:23.340Z` · `msg-f9a9d9574128c7703afd`

写好了

---

**074 · 助手** · `2026-10-14T01:20:00.443Z` · `msg-354fea427e0c7e74ac29`

检查都跑完了，正在把这次提交记进课程记录，马上给你结果。

---

**075 · 助手** · `2026-10-14T01:20:39.735Z` · `msg-f79a9e33ab442211afca`

**A9 的核心两项都过了，而且是无提示、首次提交就过。** 还差格式检查和 Clippy，所以 A9 暂时不能关。

| 检查 | 结果 |
| --- | --- |
| 测试 `a9_placement` | 8 项全部通过；全套 40 项全部通过 |
| `gpu_index` 的写法 | 符合：一个 `match`，三个分支，用嵌套模式同时判断两层 |
| `padded_bytes` 不能 panic | 符合：三步都是 `checked_*` |
| `cargo fmt --check` | 未通过，2 处，在 [lib.rs:125-136](rust/lesson02_data_shapes/src/lib.rs#L125-L136) |
| Clippy | 未通过，10 条，都在 `impl Placement` 里 |
| 禁用项（`unwrap`、`expect`、`unsafe`） | 没有 |

我没有改动你的文件，验收测试和 `Cargo.toml` 也核对过没有被改。

**Clippy 的 10 条**，按种类：

| 行 | 报的是什么 | 条数 |
| --- | --- | --- |
| 128、129 | 绑定了 `bytes` 但没用到 | 2 |
| 136 | 绑定了 `device` 但没用到 | 1 |
| 133 | `size` 的初值 0 从来没被读过 | 1 |
| 127、128、129 | 多余的 `return` | 3 |
| 125、132 | 缺 `#[must_use]` | 2 |
| 136 | `size=*bytes` 看起来像 `*=` | 1 |

最后一条在格式化之后会自己消失，我在副本上试过，格式化后剩 9 条。

**一处约定澄清**（是我原来写得不够清楚）：A9 里说的“不用 `_`”，指的是不写 `_ =>` 这种兜底分支。在模式里略过用不到的字段不受这条限制。

**接下来**，这一项仍然不给提示：

1. 先格式化：
   ```bash
   bash scripts/host-cpu.sh run -- cargo fmt -p rust-lesson02-data-shapes
   ```
2. 再跑 Clippy，改到没有输出为止。有些检查要等前面的清掉才会报出来，所以改完一轮要重跑：
   ```bash
   bash scripts/host-cpu.sh run -- cargo clippy -p rust-lesson02-data-shapes --locked --all-targets -- -D warnings
   ```
3. 重跑测试确认还是全过，然后告诉我。记得先保存文件。

课程记录已更新（这次提交记为 E-04，未关闭的问题记为 F3），仓库里没有提交任何东西。

---

**076 · 用户** · `2026-10-14T01:28:18.733Z` · `msg-35d2e3094bcb489be202`

修改好了。

---

**077 · 助手** · `2026-10-14T01:29:28.033Z` · `msg-4a0c6e263e29114eb052`

**A9 通过，练习约定 P1 的 A1–A9 全部完成。** 这一轮你是在没有提示的情况下自己改完的。

| 检查 | 结果 |
| --- | --- |
| 全套测试 | 40 项全部通过，调试构建和发布构建都是 |
| `cargo fmt --check` | 通过 |
| Clippy | 通过（在一份全新构建上复核过，不是缓存结果） |
| `gpu_index` 的写法 | 仍是一个 `match`，两个 `None` 的情况用 `\|` 并成了一个分支，没有兜底分支 |
| 整个 workspace 的 Rust 检查 | 格式、Clippy 通过，62 项测试全部通过 |

F3 已关闭。之前两次求助影响的证据（先乘后除的顺序、嵌套模式）都由 A9 在无提示下恢复了。

## 结课确认

| 目标 | 需要的证据 | 证据在哪 | 判断 |
| --- | --- | --- | --- |
| O1 标量类型与数值规则 | 理解 | 节点 1–2 检查，综合验收 | 充分 |
| O2 元组、数组与切片 | 理解 | 节点 3–4 检查，节点 6 的复查，综合验收第 1 题 | 充分 |
| O3 struct、enum、`match`、`Box`、`const` 与 `static` | 理解 | 节点 3–4、5–6 检查，综合验收第 2、3 题 | 充分 |
| O4 用这些类型建模 | 理解和实践 | 节点 5–6 检查第 1 题；练习 A1–A9 | 充分 |

- **未关闭的阻塞问题**：没有。F1、F3 已关闭，F2 已撤回。
- **帮助影响**：两条都已恢复。
- **非阻塞的观察**，不影响结课：
  - 你写的 `bytes: _` 和 `..` 都能略过字段，区别是前者把字段列全了，以后给 `Loaded` 加字段时编译器会在这里报 E0027 提醒你，`..` 不会。
  - `padded_bytes` 里除以常数 64 不会失败，所以 `checked_div` 可以换成普通的 `/`。
  - 之前提过的三条不变：`bitsize(&self)` 与约定的 `bitsize(self)` 写法不同，derive 里没有 `Eq`，`slice` 的三个比较可以用 `data.get(start..end)` 代替。

详细记录在 [02-data-shapes.md](docs/rust-learning/lessons/02-data-shapes.md)。

**你确认第 02 课结课吗？** 确认后我会做这几件事：

1. 写入结课结论，把断点改成“等待下一课授权”。第 03 课不会自动开始。
2. 把第 02 课出现的新名词补进《Rust 基础知识》名词表并重新发布。
3. 在学习者画像的“已有基础”里加一行第 02 课。这一条改的是三条课程共用的画像，不想加的话说一声。

第 02 课的所有改动现在都还没有提交到 Git，需要提交时告诉我。

---

**078 · 用户** · `2026-10-14T01:41:21.338Z` · `msg-8ffcff81d33b86814591`

写练习的过程中我常常遇到一些问题：1. 有的enum里元素用大括号，有时候用小括号。不知道什么时候该用什么？2. 有的地方用&，有的地方不用。有的地方还要用*。我知道&有借用的含义，但不知道为什么要用*才能取到值。3. 对TensorInfo启用和其他类型一样的#[derive(Debug, Clone, Copy, PartialEq)]时，编译期报错Copy不行。不知道为什么。以上这些问题的知识点是否会在后续的课程中讲解？如果后续课程里有，那么先讲个大概就行，以后再详细讲。还有你说derive 里没有 Eq，slice 的三个比较可以用 data.get(start..end) 代替是什么意思？

---

**079 · 助手** · `2026-10-14T01:44:39.935Z` · `msg-867a1ae035bab5754c0f`

几个结论都在本机试过了，下面按你的问题顺序回答。

**先说哪些以后会讲：**

| 你的问题 | 属于哪一课 | 这次讲到什么程度 |
| --- | --- | --- |
| 1. 圆括号还是花括号 | 本课 | 讲全 |
| 2. `&` 和 `*` | 第 08 课（所有权、移动与借用），模式里的部分在第 04 课 | 大概 |
| 3. `Copy` 为什么不行 | 第 08 课和第 10 课（trait） | 大概 |
| `Eq` | 第 10 课 | 大概 |
| `data.get(start..end)` | 本课节点 3 讲过的 `get` 的延伸 | 讲全 |

问题 2、3 的写法练习里必须用到，但我在约定里只零散提过，没有先把道理讲清。这是练习设计的疏漏，不是你的问题；以后出练习前我会把参考解法里用到的每个符号核对一遍。

## 1. 圆括号还是花括号

教程里的 `WebEvent` 把三种写法放在了一起：

```rust
enum WebEvent {
    PageLoad,                  // 不带数据
    KeyPress(char),            // 圆括号：数据按位置排，没有名字
    Click { x: i64, y: i64 },  // 花括号：每个数据有名字
}
```

它们和节点 4 的三种 struct 一一对应，例如 `Matrix(f32, f32, f32, f32)` 和 `Point { x, y }`。一个变体就是“标签加上一个同样写法的 struct”。

- **用别人的类型时**：没有选择，定义里是哪种，构造和 `match` 就写哪种。
- **自己定义时**：这是约定，编译器不管。常见的取舍是：

| 情况 | 选 | 例子 |
| --- | --- | --- |
| 只有一个数据，看变体名和类型就知道是什么 | 圆括号 | `Cuda(u32)`、`Some(T)` |
| 两个以上数据，或者光看类型不知道是什么 | 花括号 | `Loaded { device, bytes }`、`Click { x, y }` |

理由是圆括号里的含义全靠位置。写成 `Loaded(Device, usize)`，读的人不知道 `usize` 是字节数还是个数。写成 `Click(i64, i64)`，把 x 和 y 写反了编译器也不会报错。

两种写法的内存布局相同，区别只在名字。

## 2. `&` 和 `*`

**核心**：`u32` 和 `&u32` 是两个不同的类型。

- `u32` 是数本身，4 字节。
- `&u32` 是一个地址，那里放着一个 `u32`，8 字节。这种值叫**引用**，相当于 C 的 `const uint32_t *p`，但保证有效、不为空。
- `&x` 取地址，`*r` 顺着地址读出值，叫**解引用**，和 C 的 `&x`、`*p` 相同。

C++ 的引用会自动解引用，所以在那边你从来不写 `*`；Rust 的引用更像 C 的指针。规则只有一条：**要的是 `u32`，手里是 `&u32`，就写 `*`。**

对照你自己的代码：

| 你的代码 | 引用从哪来 | 去掉符号会怎样（本机） |
| --- | --- | --- |
| `for s in &self.shape` | 你写的 `&` 表示只借 `shape` 来遍历，所以 `s` 是 `&usize` | 去掉 `&` 报 E0507：`self` 是借来的，不能把 `shape` 拿走 |
| `checked_mul(*s)` | 同上；参数要的是 `usize` | 去掉 `*` 报 E0308：expected `usize`, found `&usize` |
| `Device::Cuda(index) => Some(*index)` | `self` 是引用，对着引用做 `match`，拆出来的 `index` 也是引用 | 去掉 `*` 报 E0308：expected `u32`, found `&u32` |

第三行最不直观：整个值是借来的，里面的部分也只能借。

**不用写 `*` 的地方**：`.` 会自动解引用。`self.dtype.bitsize()`、`rect.top_left.y` 在 C 里要写 `p->x`，Rust 的 `.` 把两种合并了。所以 `*` 主要出现在传参、返回和构造值的时候。漏写时编译器会给出 `help: consider dereferencing the borrow`。

## 3. `TensorInfo` 为什么不能 `Copy`

- **`Copy`** 是一个标记，意思是“这个类型的值只要把字节照抄一份就算复制好了”，对应 C++ 的 trivially copyable。有了它，`let q = p;` 之后 `p` 和 `q` 都能用。
- 没有它时，`let b = a;` 是**移动**：`a` 之后不能再用，报 E0382。这就是讲 `Box` 时你见过的那个错误。

`Vec<usize>` 的值是 24 字节：指针、长度、容量，元素在堆上。如果照抄这 24 字节，就有两个 `Vec` 指向同一块堆内存，各自释放一次，就是重复释放。所以 `Vec` 不是 `Copy`。

规则是：**所有字段都是 `Copy`，类型才能是 `Copy`。** `TensorInfo` 里有 `shape: Vec<usize>`，所以报 E0204，并指着这个字段说 “this field does not implement `Copy`”。

要复制它得用 **`Clone`**，也就是显式调用 `.clone()`，它会新分配一块内存并把元素抄过去。三种语言的对照：

| | `b = a` 做了什么 | 深复制怎么写 |
| --- | --- | --- |
| C++ `std::vector` | 悄悄调用复制构造，深复制 | 同左 |
| Python `list` | 两个名字指向同一个列表 | `copy.deepcopy(a)` |
| Rust `Vec` | 移动，`a` 失效 | `a.clone()` |

safetensors 也是这样：`Dtype` 有 `Copy`，`TensorInfo` 只有 `Clone`。

这也回答了问题 2 的后半：`*index` 能读出值，是因为 `u32` 是 `Copy`。对 `&Vec<usize>` 写 `*r` 想取走整个 `Vec`，本机报 E0507。

## 4. `Eq` 是什么

- `PartialEq` 提供 `==`。
- `Eq` 不增加任何功能，只是一个承诺：“任何值都等于它自己”。

浮点数做不到这个承诺，本机 `f32::NAN == f32::NAN` 是 `false`。所以带 `f32` 的 `Matrix`、`Point`、`Rectangle` 不能加 `Eq`（报 E0277）。`Dtype`、`Device`、`TensorInfo`、`Placement` 里只有整数，可以加：

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
```

用处是标准库有些功能要求 `Eq`，比如做哈希表的键（`HashMap`，相当于 Python 的 `dict`）。本机把没有 `Eq` 的类型放进 `HashSet` 会报 E0277，并建议加上它。惯例是能加就加，safetensors 的 `Dtype` 就带着。练习约定没有要求这一条，对应的 Clippy 检查也不在仓库启用的范围里。

## 5. `data.get(start..end)`

节点 3 讲过 `xs.get(5)` 越界时返回 `None` 而不是 panic。`get` 也接受一个范围。对 5 字节的 `[10, 11, 12, 13, 14]`，本机结果是：

| 调用 | 结果 | 情况 |
| --- | --- | --- |
| `get(1..4)` | `Some([11, 12, 13])` | 正常 |
| `get(4..1)` | `None` | 起止颠倒 |
| `get(3..9)` | `None` | 越界 |
| `get(5..5)` | `Some([])` | 末尾的空区间 |
| `get(6..6)` | `None` | 超过末尾 |

这正好是你第 107 行的三个比较，连 F1 的那个边界也一致。所以 `slice` 可以写成：

```rust
let (start, end) = self.data_offsets;
let bytes = data.get(start..end)?;
if bytes.len() != self.byte_len()? {
    return None;
}
Some(bytes)
```

我在副本上验证过：40 项测试在两种构建下都通过，Clippy 通过。好处有两点：

- 边界规则交给标准库，不用手写。F1 就是手写边界时差了一个等号。
- 不再有 `end - start` 和 `&data[start..end]` 这两处可能溢出或 panic 的地方。

你现在的写法是正确的，这只是更常见的写法，改不改都可以。

## 读哪里

| 内容 | 仓库里的快照 | 在线（1.97.1） |
| --- | --- | --- |
| 变体的三种写法（已读过） | [enum.md](docs/rust-by-example/src/custom_types/enum.md) | [Enums](https://doc.rust-lang.org/1.97.1/rust-by-example/custom_types/enum.html) |
| 模式里的 `&` 和 `*`（第 04 课） | [destructure_pointers.md](docs/rust-by-example/src/flow_control/match/destructuring/destructure_pointers.md) | [pointers/ref](https://doc.rust-lang.org/1.97.1/rust-by-example/flow_control/match/destructuring/destructure_pointers.html) |
| 移动与借用（第 08 课） | [move.md](docs/rust-by-example/src/scope/move.md)、[borrow.md](docs/rust-by-example/src/scope/borrow.md) | [Ownership and moves](https://doc.rust-lang.org/1.97.1/rust-by-example/scope/move.html)、[Borrowing](https://doc.rust-lang.org/1.97.1/rust-by-example/scope/borrow.html) |
| `derive` 与 `Clone`（第 10 课） | [derive.md](docs/rust-by-example/src/trait/derive.md)、[clone.md](docs/rust-by-example/src/trait/clone.md) | [Derive](https://doc.rust-lang.org/1.97.1/rust-by-example/trait/derive.html)、[Clone](https://doc.rust-lang.org/1.97.1/rust-by-example/trait/clone.html) |

后三行现在不用读，到那一课再读。

第 02 课的结课确认还在等你。确认的话，我会把问题 2、3 记进结课结论，作为第 04、08、10 课的讲解起点。

---

**080 · 用户** · `2026-10-14T02:04:22.409Z` · `msg-7237b36187fb0770cd31`

噢，那我能否理解rust里就没有C++的引用这个东西，只有指针地址？TensorInfo不能Copy是因为里面的shape这个Vec没有Copy？所以data.get相比于直接的[start,end]，可以多给出异常情况的检查，异常时返回None是吧？

---

**081 · 助手** · `2026-10-14T02:05:16.935Z` · `msg-a5a587d7b5df939cdd1e`

三条里两条对，一条要修正一半。

## 1. 引用：方向对，补两点

Rust 把 `&T` 就叫“引用”，名字还在，但它的用法确实更像指针，是一个可以存、可以改指向的值。本机对照：

| | C 指针 | C++ 引用 | Rust `&T` |
| --- | --- | --- | --- |
| 可以为空 | 可以 | 不可以 | 不可以 |
| 取值要写 `*` | 要 | 不要 | 要（`.` 除外） |
| 能改指向、能放进容器 | 能 | 不能 | 能 |
| 指向的东西已经没了，谁来防 | 没人 | 没人 | 编译器 |

- **像指针的地方**：`let mut r = &a; r = &b;` 之后读到的是 `b`，`Vec<&u32>` 能编译，`&u32` 占 8 字节。C++ 那边 `r = b` 是把 `b` 的值写进 `a`，`sizeof(r)` 是 4，`std::vector<int&>` 编译不过。
- **不像 C 指针的地方**：不能为空（`let r: &u32 = 0;` 报 E0308），没有指针加减，借出去期间的规则由编译器检查，就是你之前见过的 E0499、E0597 那一类。

所以更准确的说法是：用法像指针，保证像 C++ 引用，再加上编译器检查。

和 C 完全一样的指针 Rust 也有，叫裸指针，写作 `*const T`。它解引用必须放在 `unsafe` 里，本机不写会报 E0133。这是第 17 课的内容。

## 2. `Copy`：对

就是因为 `shape: Vec<usize>`。`dtype` 和 `data_offsets` 都是 `Copy`，只有它拦着。本机把 `shape` 字段去掉，同一行 derive 就通过了，`let b = a;` 之后两个都能用。

## 3. `get`：返回 `None` 对，“多了检查”不对

`&data[start..end]` 也做同样的检查，区别只在检查不通过之后。

| 写法 | 有没有检查 | 不通过时 |
| --- | --- | --- |
| C 的 `data + start` | 没有 | 读到别的内存 |
| `&data[start..end]` | 有 | panic |
| `data.get(start..end)` | 同一个检查 | 返回 `None` |

标准库里这两个函数写在一起，在 `core/src/slice/index.rs`：第 366–375 行的 `get` 和第 435–444 行的 `index` 用的是同一个条件，即 `end - start` 不溢出且 `end <= len`。不满足时前者返回 `None`，后者 panic。

本机对 5 字节的数据取 `3..9`：`get` 得到 `None`；下标写法 panic，信息是 `range end index 9 out of range for slice of length 5`，带 `-O` 的构建也一样。

怎么选：

- **范围是自己的程序算出来的**，越界说明程序有 bug：用下标，panic 正合适。
- **范围来自外部**，比如文件头里的偏移，越界是预料之中的情况：用 `get`，把它交给调用方处理。

你现在的 `slice` 先手写了三个比较，所以后面的下标不会 panic；等于同一个检查做了两遍，一遍手写，一遍在下标里。

第 02 课的结课确认还在等你。

---

**082 · 用户** · `2026-10-14T02:09:44.551Z` · `msg-9f8845415cb916e79061`

最后我想再以一个例子认真过一下&和*这些标记。就以TensorInfo的byte_len方法为例。这里传入参数是&self与传入self有什么区别，对后续使用有什么区别。遍历时in &self.shape和in self.shape又有什么区别？最后*s和s的区别。

---

**083 · 助手** · `2026-10-14T02:11:55.930Z` · `msg-58cb1ae6194152f0e843`

下面的结论都是用你的 `byte_len` 在本机跑出来的。

**一句话的模型**：每个位置先问“这里放的是东西本身，还是指向它的地址”。写 `&` 是只给地址，写 `*` 是顺着地址读值，什么都不写是把东西本身交出去。

## 例子和内存图

调用方写了一个 2×3 的 `F32` 张量，结果应该是 2 × 3 × 32 ÷ 8 = 24：

```rust
let info = TensorInfo { dtype: Dtype::F32, shape: vec![2, 3], data_offsets: (0, 24) };
info.byte_len()   // Some(24)
```

运行时打印出的地址（只留末尾几位）：

```text
main 的栈                                   堆
info: TensorInfo，48 字节
…dc0 ┌─────────────────────┐
     │ shape: 指针 ────────┼────────▶ …d60 ┌───┐
     │        长度 2       │               │ 2 │
     │        容量 2       │          …d68 ├───┤
     │ data_offsets (0,24) │               │ 3 │
     │ dtype: F32          │               └───┘
     └─────────────────────┘                 ▲
        ▲                                    │
byte_len 的栈                                │
self = …dc0（8 字节）                        │
s    = …d60，下一轮是 …d68 ──────────────────┘
```

函数里每个表达式的类型：

| 表达式 | 类型 | 是什么 |
| --- | --- | --- |
| `self` | `&TensorInfo` | 地址，指向调用方的 `info` |
| `self.shape` | `Vec<usize>` | `info` 里的那个字段本身 |
| `&self.shape` | `&Vec<usize>` | 那个字段的地址 |
| `s` | `&usize` | 堆上某个元素的地址 |
| `*s` | `usize` | 那个元素的值，先是 2，再是 3 |

## 1. `&self` 和 `self`

`&self` 是 `self: &TensorInfo` 的简写，`self` 是 `self: TensorInfo`。

调用处不用写 `&`，是因为 `.` 会替你加上：`info.byte_len()` 就是 `TensorInfo::byte_len(&info)`，本机两种写法都得到 `Some(24)`。

| | `&self` | `self` |
| --- | --- | --- |
| 传进去的 | 8 字节的地址 | 48 字节的值本身，`info` 被移动 |
| 方法返回时 | 什么都不释放 | `shape` 的堆内存被释放 |
| 调用方之后再用 `info` | 可以，想调几次调几次 | 报 E0382：`byte_len` takes ownership of the receiver `self`, which moves `info` |
| 在 `slice(&self, …)` 里调用它 | 可以 | 报 E0507：cannot move out of `*self` |

`byte_len` 只是读一读、算个数，没有理由把 `info` 拿走，所以用 `&self`。

`self` 适合两种情况：

- **方法要把这个值消耗掉**，比如 `Option::unwrap(self)`，拆开之后原来的 `Option` 就没用了。
- **类型很小而且是 `Copy`**，比如 `Dtype` 只有 1 字节。约定里写的 `bitsize(self)` 就是这个意思：传值时抄一份，调用方手里的还在。本机改成 `bitsize(self)` 后连调两次都正常。

对应到 C++：`&self` 相当于 `size_t byte_len() const`，其中 `this` 是 `const TensorInfo*`。`self` 相当于调用方写 `std::move(info)` 传进来，区别是 Rust 的编译器之后不让你再碰 `info`。Python 的 `self` 永远是引用。

## 2. `in &self.shape` 和 `in self.shape`

`&self.shape` 是 `&(self.shape)`，也就是只把 `shape` 借给循环。

| 写法 | `s` 的类型 | 循环之后 `Vec` | 在 `&self` 方法里 |
| --- | --- | --- | --- |
| `for s in &self.shape` | `&usize` | 还在 | 可以 |
| `for s in self.shape` | `usize` | 被循环拿走，没了 | 报 E0507 |

- **带 `&`**：循环每轮给你一个元素的地址。上图里 `s` 先是 `…d60`，再是 `…d68`，相差 8 字节，都指进堆上那块内存。
- **不带 `&`**：把整个 `Vec` 交给循环，每轮直接给你 `usize` 的值。在一个局部变量 `v` 上试，循环后再写 `v.len()` 报 E0382。
- **在 `byte_len` 里不带 `&` 行不通**：`self` 本身是借来的，不能把它的字段送人。编译器的 help 就是建议加上 `&`。

这里和 C++ 不一样，容易带错习惯：C++ 的 `for (size_t s : shape)` 是把每个元素抄一份，`shape` 还在（本机循环后 `size()` 仍是 2）。Rust 不带 `&` 是把容器整个交出去。Python 的 `for s in shape` 相当于 Rust 带 `&` 的写法。

## 3. `*s` 和 `s`

- `s` 是地址，8 字节。
- `*s` 是那个地址上的数。

`checked_mul` 的参数类型是 `usize`，所以传 `s` 报 E0308：expected `usize`, found `&usize`。`*s` 把数读出来抄一份，`usize` 是 `Copy`，所以允许，`Vec` 里的元素不受影响。

同一个函数里 `self.dtype.bitsize()` 一个符号都没有，是因为 `.` 自动做了两件事。完整写出来是：

```rust
Dtype::bitsize(&(*self).dtype)
```

`(*self)` 是顺着 `self` 找到 `info`，外面的 `&` 是因为 `bitsize` 要的是 `&self`。本机两种写法都得到 32。

以后你会见到另一种等价写法 `for &s in &self.shape`，这时 `s` 直接就是 `usize`，循环体里不用写 `*`。它的规则是“`&` 写在 `for` 和 `in` 之间的模式里，是拆掉一层引用”，第 04 课讲。

## 小结

| 写法 | 含义 |
| --- | --- |
| `&x` | 不交出 `x`，只给它的地址 |
| `*r` | 顺着地址读出值 |
| 什么都不写 | 把东西本身交出去：`Copy` 类型是抄一份，其他类型是移动，原主不能再用 |
| `.` | 自动加 `&`、自动解 `*`，所以方法调用和取字段时不用管 |

## 读哪里

| 内容 | 仓库里的快照 | 在线（1.97.1） |
| --- | --- | --- |
| `&self`、`&mut self`、`self` 三种写法（第 05 课） | [methods.md](docs/rust-by-example/src/fn/methods.md) | [Methods](https://doc.rust-lang.org/1.97.1/rust-by-example/fn/methods.html) |
| `for` 的三种遍历方式（第 04 课） | [for.md](docs/rust-by-example/src/flow_control/for.md) | [for and range](https://doc.rust-lang.org/1.97.1/rust-by-example/flow_control/for.html) |

这两页现在不用读。第 02 课的结课确认还在等你。

---

**084 · 用户** · `2026-10-14T02:28:34.769Z` · `msg-7a5ce29ba71a141617f3`

直接穿参默认都是移动语义是吗？那如果我想要做Copy，需要怎么写呢？传入的时候.clone()一下吗？for s in self.shape就是把这个Vec移动到循环体里，循环结束就释放了是吗？所以传参了&self，既然self是地址，那么&self.shape其实也是简写，完整其实是&((*self).shape)是吗？Dtype::bitsize(&(*self).dtype)也还可以更清楚表明顺序其实是Dtype::bitsize(&((*self).dtype))，里面是先取dtype再取&是吧。所以rust里面.的作用可以取代C中的->是吧？

---

**085 · 助手** · `2026-10-14T02:29:46.891Z` · `msg-86cf158320d152286670`

六条都对，其中两条补一点细节。

## 1. 直接传参默认是移动：对

不只是传参，`let b = a;`、作为返回值、放进 struct 或 `Vec`，都一样。例外是 `Copy` 类型，它们是抄一份，原来的还能用。

两种情况在机器层面做的是同一件事，都是把值的字节抄过去。区别只在编译器之后还让不让你用原来那个。

## 2. 想要一份副本：对，写 `.clone()`

用词上分清两个东西：

- **`Copy`** 是类型自己的属性，自动发生，你什么都不用写。`Dtype` 是 `Copy`，本机 `takes_dtype(d)` 连调两次都正常。
- **`.clone()`** 是你在调用处明确要一份副本，给不是 `Copy` 的类型用。

所以调用处有三种写法：

| 写法 | 含义 | 代价 | 之后 `info` |
| --- | --- | --- | --- |
| `f(info)` | 移动 | 抄 48 字节 | 不能用，报 E0382 |
| `f(&info)` | 借出 | 传 8 字节 | 能用 |
| `f(info.clone())` | 先造一份副本，把副本移动进去 | 新分配堆内存并抄元素 | 能用 |

本机打印堆地址：原来的在 `…d60`，`clone()` 出来的在 `…d80`，是两块不同的内存。

只是读数据时，首选是 `&info`，不是 `.clone()`。E0382 的提示里，编译器也是先建议把参数改成借用，再建议 `clone`。

## 3. `for s in self.shape` 移动进循环、循环结束就释放：对

我用一个统计堆内存的分配器量了一下，`vec![2, 3]` 占 16 字节堆内存：

| 时刻 | 还没释放的堆内存 |
| --- | --- |
| `for s in v` 的最后一轮循环体内 | 16 字节 |
| `for s in v` 结束后 | 0 |
| `for s in &w` 结束后 | 16 字节，`w` 还在 |

精确一点说，`Vec` 是移动给了循环背后的一个隐藏的值，由它持有那块内存并逐个交出元素。循环结束时这个值被销毁，内存随之释放。用 `?` 或 `return` 提前跳出循环时也一样会释放。

## 4. `&self.shape` 完整是 `&((*self).shape)`：对

本机两种写法打印出同一个地址。

顺序由优先级决定：`.` 比前缀的 `&` 和 `*` 结合得更紧，这和 C 里 `&p->x` 是 `&(p->x)` 相同。[Rust Reference 的优先级表](https://doc.rust-lang.org/1.97.1/reference/expressions.html#expression-precedence)里，方法调用和取字段排在最前，一元的 `-`、`!`、`*` 和借用排在它们后面。

## 5. `Dtype::bitsize(&((*self).dtype))`，先取 `dtype` 再取 `&`：对，补一点

本机三种写法都得到 32。

要补的是“取 `dtype`”这一步的含义：`(*self).dtype` 在这里指的是**那个字段所在的位置**，不是把它的值读出来。外面的 `&` 取的是这个位置的地址，中间没有复制，也没有移动。本机算出来的地址正好是 `info` 的地址加 40，就是 `dtype` 字段在 `TensorInfo` 里的偏移。

这也解释了第 3 条和第 4 条的差别：

- `&self.shape`：只取字段的地址，谁也没被拿走，所以借来的 `self` 也可以这样写。
- `self.shape` 单独当值用：要把字段本身拿走，所以是移动，在 `&self` 方法里报 E0507。

C 里的说法是左值，`&(p->dtype)` 也不会先把 `dtype` 复制出来。

实际代码里写短的形式就行。把完整写法放进 crate 跑 Clippy，会报 `explicit_auto_deref`，要求把 `(*self)` 改回 `self`。

## 6. `.` 取代了 `->`：对

Rust 取字段和调方法只有 `.`。本机写 `r->x`，编译器直接说：

```text
error: `->` is not valid syntax for field accesses and method calls
help: the `.` operator will automatically dereference the value, except if the value is a raw pointer
```

`->` 在 Rust 里只用来写函数的返回类型。

`.` 比 C 的 `->` 多做两件事：

- **有几层解几层**：本机通过 `&TensorInfo`、`&&TensorInfo`、`Box<TensorInfo>` 写 `.shape.len()` 都得到 2。C 里两层指针要写 `(*pp)->x`。
- **调方法时自动补 `&`**：就是上次说的 `info.byte_len()` 等于 `TensorInfo::byte_len(&info)`。

有两个限制：

- 自动解引用只发生在 `.` 上，传参和运算时仍然要自己写 `*`，比如 `checked_mul(*s)`。
- 如报错里所说，裸指针不会自动解引用。

第 02 课的结课确认还在等你。

---

**086 · 用户** · `2026-10-14T02:32:04.231Z` · `msg-d4f4ab88867cbd27083e`

我发现rust中有好多简写，这还挺令人迷惑的。

---

**087 · 助手** · `2026-10-14T02:32:50.016Z` · `msg-339f62cef30401af3b7e`

这个感觉是正常的。到现在为止你碰到的简写其实就这几种，每一种都只有一个固定的展开方式：

| 你写的 | 编译器读成 |
| --- | --- |
| `fn byte_len(&self)` | `fn byte_len(self: &Self)`，`Self` 就是 `TensorInfo` |
| `info.byte_len()` | `TensorInfo::byte_len(&info)` |
| `self.shape`（`self` 是引用） | `(*self).shape` |
| `for s in &self.shape` | `for s in self.shape.iter()` |
| `numel.checked_mul(*s)?` | `match … { Some(v) => v, None => return None }` |
| `Rectangle { top_left, bottom_right }` | `Rectangle { top_left: top_left, bottom_right: bottom_right }` |
| `format!("cuda:{index}")` | `format!("cuda:{}", index)` |
| 函数最后一行 `Some(n)` | `return Some(n);` |
| `let len = data.len();` | `let len: usize = data.len();` |

我把 `byte_len` 的简写版和全部展开的版本各写了一遍，本机对正常输入和溢出输入的结果都相同。

**为什么这样设计**：Rust 的完整写法里，每一处借用、移动和类型都是明写的，天天这么写会很啰嗦。所以它只在“展开方式唯一、纯属机械”的地方允许省略，省掉的基本是 `&`、`*`、类型标注和重复的名字。有两样必须写出来：深复制要写 `.clone()`，数值类型转换要写 `as`。这和 C++ 相反，C++ 里复制构造和隐式转换是悄悄发生的。

**看不清某个变量是什么类型时**，有一个不依赖任何工具的办法：故意把它赋给一个类型明显不对的变量，让编译器告诉你。

```rust
for s in &shape {
    let probe: () = s;
}
```

本机报 E0308：expected `()`, found `&usize`。看完删掉这一行就行。如果你的 VSCode 装了 rust-analyzer 扩展，它会直接在变量后面用灰字标出类型。

结课更新名词表时，我可以把上面这张简写对照表加进去，要的话说一声。

---

**088 · 用户** · `2026-10-14T02:34:32.685Z` · `msg-63c7964ba490c8da0200`

明白了。加进去吧

---

**089 · 助手** · `2026-10-14T02:39:29.824Z` · `msg-eed5843c3ae7487db355`

页面结构看完了，现在写名词条目和简写表，然后校验、截图、重新发布。

---

**090 · 助手** · `2026-10-14T02:42:28.826Z` · `msg-d793639d49073d35075e`

名词卡片渲染正常，现在看一眼简写表本身的效果，然后发布。

---

**091 · 助手** · `2026-10-14T02:42:41.083Z` · `msg-3584e3b8bf485d3370ff`

Now read the published artifact (required before updating it) and republish.

---

**092 · 助手** · `2026-10-14T02:43:25.030Z` · `msg-1a092e383875b239cbf4`

简写对照表已经加进《Rust 基础知识》并重新发布：<https://claude.ai/artifact/QWuM4hG3rcan33BLwKg2N1>（Version 2），仓库里的源文件是 [rust-basics.html](docs/rust-learning/attachments/00-rust-basics/rust-basics.html)。

**简写对照表**
- 位置在名词表的正后方，名词表开头的说明里有一个“简写对照”链接可以直接跳过去。
- 共 11 行：聊天里的 9 行，加上 `let Point { x, y } = p;` 和 `#[derive(Debug)]` 两行。
- 每行最后一列链接到相关的名词卡片。
- 表下面附了“看不清类型时加一行 `let probe: () = s;`”的办法。

**顺带提前做了一件事**：表里要用到 `match`、`Option`、解引用这些词，而名词表原来只收到第 01 课。所以我把原计划结课时才补的第 02 课名词一起补了：
- 新增 35 个，现在共 84 个。问过的几个都在里面：解引用、自动借用与自动解引用、Copy 与 Clone、PartialEq 与 Eq、边界检查、生命周期标注。
- 改了两条旧的：“方法与 self”补上了只写 `self` 的含义，“? 运算符”补上了它也能用在 `Option` 上。

新条目里的 25 个教程链接都能打开，页面在手机和桌面宽度、深浅两种主题下都看过。

仓库里的改动仍然没有提交。

还差一句明确的话：**第 02 课可以结课了吗？** 确认后我写入结课结论，把断点改成“等待下一课授权”，并在学习者画像的“已有基础”里加一行第 02 课。

---

**093 · 用户** · `2026-10-14T02:44:23.881Z` · `msg-1f72101748e695385e30`

接下来进行本次课程的结课吧。

---

**094 · 助手** · `2026-10-14T02:45:52.847Z` · `msg-b4f6d6905240aaca01bf`

第 02 课已结课。

**结课结论**：你能从一个类型说出它的值占多少字节、哪些信息写在类型里、哪些带在值里；能解释 Rust 在数值运算、数组访问和“多选一”的数据上各把 C 的哪种隐患变成了编译错误或确定的运行期行为，以及代价；并独立用 struct、enum、元组和切片建模，用 `match` 和嵌套模式读出数据，处理了溢出与越界。

**写入的记录**
- [02-data-shapes.md](docs/rust-learning/lessons/02-data-shapes.md)：阶段改为 `complete`，加了结课一节，四个目标的证据都判为充分。
- [README.md](docs/rust-learning/README.md) 的断点：现在没有进行中的课，等待你授权下一课。候选是第 03 课“绑定、类型与转换”，不会自动开始。
- [learning-profile.md](docs/learning-profile.md)：“已有基础”改为 Rust 第 01–02 课，零基础的范围相应改为“第 01–02 课之外”。

**带到后面的课**（记在结课一节里）
- 你这次说的三处困惑，即括号的选择、`&` 与 `*`、`Copy`，在第 04、08、10 课从这次讲到的地方接着讲，不默认你已经掌握。
- 以后出练习前，我先把参考解法里的每个符号和 derive 列出来，没讲过的在约定里先讲清。

**结课前的最后核对**：练习文件自 A9 复验后没有变化，40 项测试、格式检查和整个 workspace 的 Clippy 都通过。

第 02 课的全部改动仍然没有提交到 Git：练习 crate、课程记录、两个图解页、画像和 `Cargo.lock`。需要提交或推送时告诉我。想开始第 03 课时也直接说。
