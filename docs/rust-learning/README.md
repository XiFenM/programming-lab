# Rust 学习档案

本目录记录 Rust 学习，分两部分：

- **语言部分（第 01–17 课）**以 Rust by Example（下称 RBE）为教学主线。主线是仓库内固定版本的原文快照
  [`docs/rust-by-example/src/`](../rust-by-example/src/SUMMARY.md)，与宿主机固定的 Rust 1.97.1 配套；版本、许可与
  核对结果见[来源记录](../rust-by-example/SOURCE.md)。
- **异步部分（第 18–25 课）**讲异步的执行模型和服务端并发。RBE 没有覆盖这部分，改用 Rust 官方教材的并发与异步
  两章、Tokio 官方教程和相关库的文档与源码，见[异步部分的来源](#异步部分的来源)。

本 Program 与 [`triton-official-tutorials`](../triton-learning/README.md#当前-program-状态)、
[`leetcode-algorithm-interview`](../algorithm-interview-learning/README.md#当前-program-状态) 并行保持 `active`。
各条课程分别维护自己的 Program、Lesson 与 Checkpoint；一次具体学习上下文只选择一条课程的前台 Lesson，切换课程
不会冻结、关闭或自动推进其他课程。

## 教学与状态

讲解、提问、练习、Review 与结课的行为由中央 `guide-learning` 定义，本仓库不复制；学习者画像与目标深度见
[学习者画像](../learning-profile.md)。本课程的状态只落在三处：

| 职责 | 位置 |
| --- | --- |
| Program：长期范围、排除项与候选顺序 | 本页“当前 Program 状态”与“课程索引” |
| Lesson：目标、来源、阶段事件、练习约定、证据与结课结论 | `lessons/<NN>-<topic>.md` |
| Checkpoint：当前位置、唯一下一动作与前进门槛 | 本页 [Checkpoint](#checkpoint) |

当前是哪一课只写在 Checkpoint；Program 与课程索引不重复记录当前课或逐课状态。受管配置已登记本课程的 Program、
Checkpoint、Lesson 目录与练习目录，切换课程不需要修改配置或重新 materialize。文章、结构化过程记录、卡片和
原始对话均为按需产物，不是 Program、Lesson 或 Checkpoint 的事实源。

## 目录约定

目前只有本页。其余位置在第一次用到时才创建，不预建空目录：

| 位置 | 用途 | 何时出现 |
| --- | --- | --- |
| `docs/rust-learning/lessons/<NN>-<topic>.md` | 单课记录，以 [Lesson 模板](../triton-learning/templates/lesson-record.md)的“核心记录”为基础，把 Program、Lesson ID 前缀和来源换成本课程的 | 学习者授权开课时 |
| `docs/rust-learning/attachments/<NN>-<topic>/` | 图解、实验数据等补充材料 | 某一课实际产生时 |
| `rust/lessonNN_<topic>/` | 正式练习的 crate，每课一个 | 第一份练习约定被接受时 |

- RBE 快照保持原样，不在 `docs/rust-by-example/` 中写笔记或修改示例。
- 实践源码与测试放在 `rust/`；Lesson 使用相对链接，不复制实现。

## 课程全貌

RBE 开篇这样概括 Rust：一门注重安全、速度与并发的系统编程语言，做法是不用垃圾回收而保证内存安全。语言部分围绕
这句话展开：编译器凭哪些规则在编译期排除悬垂引用、重复释放和数据竞争，这些规则又让抽象付出了什么、省下了什么。
异步部分把同一套规则放进一个长期运行的网络服务：成千上万个任务共享状态、互相等待、随时可能被取消，服务还要在
过载和故障下保持可控。

全课 25 个候选课次，分八个阶段：

| 部分 | 阶段 | 课次 | 形成的能力 | 讲解时挂靠的已有经验 |
| --- | --- | --- | --- | --- |
| 语言 | 语言表层 | 01–05 | 读写不涉及复杂借用的程序：类型、绑定、模式匹配、函数与闭包 | C/C++ 的类型与控制流、`std::variant`、lambda |
| 语言 | 工程组织 | 06 | 把代码组织成模块和 crate，用 Cargo 构建并做条件编译 | 头文件与翻译单元、命名空间、`#ifdef`、CMake |
| 语言 | 类型系统与所有权 | 07–10 | 泛型、所有权与借用、生命周期、trait，是语言部分的核心 | 模板、RAII、`std::move`、虚函数 |
| 语言 | 惯用法与标准库 | 11–13 | 声明宏、错误处理、标准库的容器与智能指针 | 预处理器、异常与错误码、`unique_ptr`、`shared_ptr`、STL 容器 |
| 语言 | 系统编程 | 14–17 | 线程与通道、文件与进程、测试与文档、unsafe 与 FFI（含 Python 绑定） | `std::thread`、POSIX 接口、pytest、`extern "C"`、pybind11 |
| 异步 | 异步基础 | 18–20 | 说清任务怎样被调度、怎样共享状态、被取消时发生什么 | Python `asyncio`、事件循环与线程池、RAII |
| 异步 | 服务端并发 | 21–24 | 在异步网络服务里控制流量和故障：背压、超时与重试、排空、流式取消传播 | 分布式通信里的超时、挂起与资源生命周期问题 |
| 异步 | 综合 | 25 | 把各课的部件装成一个简化的推理路由器 | 推理引擎前面的网关与调度层 |

最后一栏是课程设计，不是来源事实；实际对照以学习者画像和开课时的前置核对为准。

三处贯穿全课的安排：

- **前向引用**：前五课的示例里已经会出现移动和借用，例如 `for` 的三种迭代方式、闭包的捕获方式、链表示例里的
  `Box`。遇到时先给一个够用的最小模型，系统讲解放在第 08、09 课。
- **工具**：从第 01 课起就要用 `cargo` 和测试来运行示例、提交练习，当时只交代用到的最小操作；系统讲解放在
  第 06 课和第 16 课。
- **异步部分的贯穿案例**：一个简化的推理路由器，前面挂客户端，后面挂若干推理 worker。第 19–24 课各补上它的一个
  部件，依次是 worker 注册表、请求任务的取消、有界队列、心跳与重试、排空、流式转发；第 25 课把它们装成一个服务。

### 异步部分要能回答的问题

学习者于 2026-10-07 给出下面八个问题，要求学完后能回答包括但不限于这些。每个问题对应到讲它的课次：

| 目标问题 | 课次 |
| --- | ---: |
| 为什么使用 `Arc`？何时还需要 `Mutex`／`RwLock`？ | 19 |
| Tokio task 被取消时资源如何释放？ | 20 |
| 如何设计 bounded channel 与 backpressure？ | 21 |
| 如何实现 heartbeat 和 timeout？ | 22 |
| retry 如何避免 retry storm？ | 22 |
| 如何实现 drain 而不丢失 in-flight request？ | 23 |
| `DashMap` 与单一 `Mutex<HashMap>` 的权衡是什么？ | 19 |
| gRPC streaming 的取消如何向下游传播？ | 24 |

题单之外，这部分还覆盖：异步的执行模型（第 18 课，后面七个问题的共同前提）、原子类型与读多写少的配置（第 19 课）、
限流与熔断（第 21、22 课）、Axum 与 Tonic 的服务入口（第 24 课）、路由策略与指标（第 25 课）。

## 课程索引

下面两张表是规划顺序，不构成启动授权。课次只在学习者明确开始后才创建记录；已有记录的课次在“课次”一栏链接到
它的记录，没有链接的都是候选。各课的目标、所需证据和补充来源在开课时确定；“学完要能回答”只说明这一课的落点。

### 语言部分（第 01–17 课）

章节名后的数字是该课包含的小节数，合计 196。

| 课次 | Candidate ID | 能力标题 | 学完要能回答 | RBE 章节 |
| ---: | --- | --- | --- | --- |
| 01 | `rust-01-hello-formatting` | 第一个程序与格式化输出 | `println!` 为什么是宏而不是函数？一个类型怎样决定自己被打印成什么样？ | [1 Hello World](../rust-by-example/src/hello.md)（7） |
| 02 | `rust-02-data-shapes` | 数据的形状：基本类型、struct 与 enum | 切片为什么由指针和长度两部分组成？Rust 的 enum 比 C 的枚举多了什么？ | [2 Primitives](../rust-by-example/src/primitives.md)、[3 Custom Types](../rust-by-example/src/custom_types.md)（11） |
| 03 | `rust-03-bindings-types-conversion` | 绑定、类型与转换 | 默认不可变和遮蔽各防住什么？`as` 与 `From`、`TryFrom` 该怎样选？ | [4 Variable Bindings](../rust-by-example/src/variable_bindings.md)、[5 Types](../rust-by-example/src/types.md)、[6 Conversion](../rust-by-example/src/conversion.md)、[7 Expressions](../rust-by-example/src/expression.md)（15） |
| 04 | `rust-04-control-flow-patterns` | 控制流与模式匹配 | `match` 的穷尽性检查防住了什么？`for` 的三种迭代方式分别对集合做了什么？ | [8 Flow of Control](../rust-by-example/src/flow_control.md)（19） |
| 05 | `rust-05-functions-closures` | 函数、方法与闭包 | 闭包捕获了什么、以哪种方式捕获？`Fn`、`FnMut`、`FnOnce` 怎样与捕获方式对应？ | [9 Functions](../rust-by-example/src/fn.md)（13） |
| 06 | `rust-06-modules-crates-cargo` | 代码组织与构建 | 模块树怎样对应到文件？crate、Cargo 与 `cfg` 各管哪一层？ | [10 Modules](../rust-by-example/src/mod.md)、[11 Crates](../rust-by-example/src/crates.md)、[12 Cargo](../rust-by-example/src/cargo.md)、[13 Attributes](../rust-by-example/src/attribute.md)（19） |
| 07 | `rust-07-generics` | 泛型与约束 | 泛型函数为什么在定义时就能完成类型检查？关联类型和泛型参数怎样取舍？ | [14 Generics](../rust-by-example/src/generics.md)（14） |
| 08 | `rust-08-ownership-borrowing` | 所有权、移动与借用 | 没有垃圾回收，编译器凭什么保证资源只释放一次、引用不会悬垂？ | [15 Scoping rules](../rust-by-example/src/scope.md) 的 RAII、Ownership and moves、Borrowing（9） |
| 09 | `rust-09-lifetimes` | 生命周期 | 生命周期标注描述的到底是什么？哪些情况下可以省略？ | 15 Scoping rules 的 [Lifetimes](../rust-by-example/src/scope/lifetime.md)（10） |
| 10 | `rust-10-traits` | trait 与多态 | 泛型的静态分发和 `dyn` 的动态分发各付出什么？`Drop`、`Iterator`、`Clone` 怎样接入语言本身？ | [16 Traits](../rust-by-example/src/trait.md)（10） |
| 11 | `rust-11-macro-rules` | 声明宏 | `macro_rules!` 和 C 的宏差在哪里？什么时候该用宏而不是函数或泛型？ | [17 macro_rules!](../rust-by-example/src/macros.md)（8） |
| 12 | `rust-12-error-handling` | 错误处理 | 什么时候 `panic`，什么时候返回 `Option` 或 `Result`？`?` 展开成了什么？ | [18 Error handling](../rust-by-example/src/error.md)（20） |
| 13 | `rust-13-std-types` | 标准库的容器与智能指针 | `Box`、`Vec`、`String`、`Rc`、`Arc` 各自拥有什么、数据放在哪里、代价是什么？ | [19 Std library types](../rust-by-example/src/std.md)（13） |
| 14 | `rust-14-threads-channels` | 线程与通道 | 数据怎样安全地交给另一个线程？共享状态和消息传递怎样选？ | [20 Std misc](../rust-by-example/src/std_misc.md) 的 Threads、Channels（4） |
| 15 | `rust-15-os-interaction` | 与操作系统交互：文件、进程与命令行 | 文件、子进程和命令行参数的接口里，所有权与错误处理是怎样配合的？ | 20 Std misc 的 Path、File I/O、Child processes、Filesystem Operations、Program arguments（11） |
| 16 | `rust-16-testing-docs` | 测试与文档 | 单元测试、文档测试和集成测试各自能看到什么？文档注释怎样同时成为测试？ | [21 Testing](../rust-by-example/src/testing.md)、[24 Meta](../rust-by-example/src/meta.md)（8） |
| 17 | `rust-17-unsafe-ffi` | unsafe 与外部接口：C FFI 与 Python 绑定 | `unsafe` 放开了哪几件事、没有放开什么？调用 C 函数时安全边界画在哪里？把 Rust 函数暴露给 Python 时，GIL 和对象的生命周期由谁保证？ | 20 Std misc 的 [Foreign Function Interface](../rust-by-example/src/std_misc/ffi.md)、[22 Unsafe Operations](../rust-by-example/src/unsafe.md)、[23 Compatibility](../rust-by-example/src/compatibility.md)（5）；另加 [PyO3 部分](#第-17-课的-pyo3-部分) |

每个小节恰好归属一课。除下面几处外，课次顺序与原书章节顺序一致：

- 第 15 章 Scoping rules 拆成两课：所有权与借用（第 08 课）、生命周期（第 09 课）。两者是各自独立的心智模型。
- 第 20 章 Std misc 拆成三部分：线程与通道（第 14 课），文件、进程与命令行（第 15 课），FFI 并入第 17 课与 unsafe
  合讲。
- 第 24 章 Meta 提前到第 16 课，与第 21 章 Testing 合讲：文档注释和文档测试是同一件事的两面。第 22、23 章因此
  排在它之后。
- 第 2–3 章、第 4–7 章、第 10–13 章各合为一课。

### 第 17 课的 PyO3 部分

RBE 的 FFI 一节只讲调用 C 函数。学习者于 2026-10-07 决定把 PyO3 的基础并入第 17 课。PyO3 是用 Rust 编写 Python
扩展模块的库，位置相当于 C++ 里的 pybind11。并入的范围是：用 `#[pyfunction]`、`#[pymodule]`、`#[pyclass]` 把 Rust 暴露
给 Python，两边的类型转换与异常映射，GIL 的持有与释放，以及构建出可以 `import` 的模块。从 Rust 调用 Python、PyO3 的
async 支持、自由线程的 Python 和 wheel 的发布不在范围内。

下表核对于 2026-10-07，开课时重新固定：

| 来源 | 角色 | 版本锚点 | 用在哪里 |
| --- | --- | --- | --- |
| [PyO3 用户指南](https://pyo3.rs/v0.29.3/) | `teaching-spine` | 当天的最新版本 0.29.3，即 `PyO3/pyo3` 的 tag `v0.29.3`（提交 `451d99fdcdcddf159e8e0a1186960b332cdb5d7c`） | Getting started、Using Rust from Python、Type conversions、Parallelism 四章 |
| [`pyo3` 的 API 文档](https://docs.rs/pyo3/0.29.3/pyo3/)与源码 | `interface-authority`、`implementation-authority` | 0.29.3；实际版本以练习写入 `Cargo.lock` 的为准 | `Python<'py>`、`Bound`、`PyResult` 等接口的语义 |
| [maturin 用户指南](https://www.maturin.rs/) | `interface-authority` | PyPI 上的 1.15.0 | 构建并安装扩展模块 |
| [`ROCm/ATOM`](https://github.com/ROCm/ATOM) 的 `atom/mesh/src/python.rs` | `implementation-authority`（真实系统锚点） | 提交 `43f5393dc456c1047d316d14be6acb662cce6db7`，该项目依赖 `pyo3` 0.28.2 | 真实实现对照：向 Python 导出配置类和启动函数，启动函数先放开 GIL，再创建 Tokio 运行时启动服务 |

### 异步部分（第 18–25 课）

TRPL 指 Rust 官方教材 The Rust Programming Language；各来源的版本见[异步部分的来源](#异步部分的来源)。

| 课次 | Candidate ID | 能力标题 | 学完要能回答 | 主要来源 |
| ---: | --- | --- | --- | --- |
| 18 | `rust-18-async-execution-model` | 异步的执行模型：Future、任务与运行时 | `async fn` 被编译成了什么？任务在 `.await` 处让出之后，由谁、凭什么把它重新调度？为什么不能在任务里做阻塞调用？ | TRPL 第 17 章；Tokio 教程的 Hello Tokio、Spawning、Async in depth |
| 19 | `rust-19-shared-state` | 任务间共享状态：`Arc`、锁与并发容器 | 为什么用 `Arc`，什么时候还要加 `Mutex` 或 `RwLock`？锁为什么不能跨 `.await` 持有？`DashMap` 与单个 `Mutex<HashMap>` 各适合什么负载？ | TRPL 第 16 章的共享状态与 `Send`、`Sync`；Tokio 教程的 Shared state；`dashmap` 与 `std::sync::atomic` 文档 |
| 20 | `rust-20-cancellation` | 取消与资源释放 | 任务被取消时到底发生了什么，资源由谁释放？哪些操作在 `select!` 里被丢弃是安全的？清理本身需要 `.await` 时怎么办？ | Tokio 教程的 Select；`tokio::select!`、`JoinHandle::abort` 与 `CancellationToken` 文档 |
| 21 | `rust-21-channels-backpressure` | 通道与背压 | 有界通道的容量怎么定？队列满了是等待、拒绝还是丢弃，压力各传到了哪里？无界通道什么时候会出事？ | Tokio 教程的 Channels；`tokio::sync` 的 `mpsc`、`oneshot`、`watch`、`Semaphore` 文档；SRE Book 的 Handling Overload |
| 22 | `rust-22-timeouts-heartbeats-retries` | 超时、心跳与重试 | 超时之后被丢弃的操作处于什么状态？心跳间隔和判死阈值怎么定？重试为什么会放大故障，退避、抖动、重试预算和熔断各管哪一环？ | `tokio::time` 文档；`tower` 的 retry 与 timeout；gRPC 重试指南与 gRFC A6；AWS 与 SRE Book 的两篇文章 |
| 23 | `rust-23-graceful-shutdown-drain` | 优雅停机与排空 | 停止接收、通知、等待、强制终止各用什么机制？怎样知道还有多少请求在途？排空超时后没做完的请求怎么交代？ | Tokio 专题 Graceful Shutdown；`TaskTracker` 文档；`axum` 与 `tonic` 的停机接口 |
| 24 | `rust-24-streaming-cancel-propagation` | 流式服务与取消传播：HTTP 与 gRPC | 客户端断开或超时后，服务端怎样得知？取消怎样一级一级传到下游，哪一环断了就会泄漏任务？ | `tonic` 的 streaming、cancellation 示例；`axum` 文档；gRPC 的取消与截止时间指南 |
| 25 | `rust-25-inference-router` | 综合项目：简化的推理路由器 | 一个请求从进入、排队、转发到流式返回，中途客户端取消或后端失效时，各环节分别发生什么？ | 第 19–24 课的工件；两个开源路由器的对应模块 |

### 课次之间的依赖

异步部分依赖语言部分的第 05、07–10、12–14 课：闭包、泛型、所有权与借用、生命周期、trait、错误处理、标准库类型、
线程与通道。添加依赖还要用到第 06 课里 Cargo 的那一部分。第 11、15、16、17 课与异步部分互不依赖，可以排在它
之后，也可以穿插进行。候选顺序只是默认路线，先学哪一课由学习者在开课时决定。

## 异步部分的来源

下表核对于 2026-10-07。TRPL 随工具链版本固定；其余来源没有与工具链绑定的版本，表中是当天的状态，各课开课时
重新固定并写入该课记录。目前这些来源都没有复制进仓库。

| 来源 | 角色 | 版本锚点 | 用在哪里 |
| --- | --- | --- | --- |
| [The Rust Programming Language](https://doc.rust-lang.org/1.97.1/book/) 第 16、17 章 | `teaching-spine` | 随 Rust 1.97.1 发布的版本，即 `rust-lang/book` 的提交 `05d114287b7d6f6c9253d5242540f00fbd6172ab`；示例使用 edition 2024 和 `trpl` crate | 第 18 课的执行模型；第 19 课的 `Send`、`Sync` 与共享状态；第 21、22 课的通道与超时示例 |
| [Tokio 官方教程](https://tokio.rs/tokio/tutorial)与专题 | `teaching-spine` | `tokio-rs/website` 的提交 `7024518b5df165bca6f9e88fc483731ebefbbf8b`（2026-10-06） | 第 18–21 课用到 Spawning、Shared state、Channels、Async in depth、Select；第 23 课用到 Graceful Shutdown |
| `tokio`、`tokio-util`、`tokio-stream`、`dashmap`、`tower`、`axum`、`tonic` 的文档与源码 | `interface-authority`、`implementation-authority` | 当天的最新版本：`tokio` 1.53.2、`tokio-util` 0.7.19、`tokio-stream` 0.1.19、`dashmap` 6.2.1、`tower` 0.5.3、`axum` 0.8.9、`tonic` 0.14.6；实际版本以第一份异步练习写入 `Cargo.lock` 的为准 | 各课的接口语义与实现细节，例如取消安全、通道容量、`CancellationToken`、`TaskTracker` |
| [`tonic` 仓库的示例](https://github.com/hyperium/tonic/tree/master/examples/src) | `explanatory-support` | 提交 `2681a7e20c2f211f3e46228af55db5b2b163e562`（2026-10-02）；开课时换成与所用 `tonic` 版本对应的 tag | 第 24 课的 `streaming`、`cancellation`、`health` |
| gRPC 指南的[取消](https://grpc.io/docs/guides/cancellation/)、[截止时间](https://grpc.io/docs/guides/deadlines/)、[重试](https://grpc.io/docs/guides/retry/)，以及 [gRFC A6](https://github.com/grpc/proposal/blob/master/A6-client-retries.md) | `interface-authority` | 访问于 2026-10-07 | 第 22、24 课 |
| AWS Builders' Library 的 [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)；Google SRE Book 的 [Handling Overload](https://sre.google/sre-book/handling-overload/) 与 [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) | `method-authority` | 访问于 2026-10-07 | 第 21、22 课的过载、重试风暴与重试预算 |
| 两个开源的推理路由器：[`AMD-AGI/Infera`](https://github.com/AMD-AGI/Infera) 的 `rust/router/`，[`ROCm/ATOM`](https://github.com/ROCm/ATOM) 的 `atom/mesh/` | `implementation-authority`（真实系统锚点） | 提交 `6e9fd6045479589d240a29878a50335a54c85cf4`（2026-09-24）与 `43f5393dc456c1047d316d14be6acb662cce6db7`（2026-10-07）；两者更新很快 | 第 19–25 课的真实实现对照 |

两个路由器在依赖上的差别本身就是讲解素材（读自上表两个提交的 `Cargo.toml` 与源码）：`atom/mesh` 直接依赖 `tokio`、
`axum`、`tower`、`tonic`、`dashmap` 和 `metrics`；`rust/router` 依赖 `tokio`、`axum` 和 `arc-swap`，没有用 `dashmap`
与 `tonic`。两者都没有直接依赖 `tokio-util`，源码里也没有出现 `CancellationToken`。

下表是按关键词出现位置筛出的阅读入口，只说明“从哪里读起”。各模块的行为结论留到开课时按固定提交核对。

| 课次 | `ROCm/ATOM` 的 `atom/mesh/` | `AMD-AGI/Infera` 的 `rust/router/` |
| ---: | --- | --- |
| 19 | `src/core/worker_registry.rs`、`src/policies/tree.rs`、`src/core/circuit_breaker.rs` | `src/pool.rs`、`src/disagg.rs` |
| 20 | `src/core/admission.rs`、`src/routers/http_pd_router.rs`、`tests/load_guard_raii_test.rs` | `src/proxy.rs`、`src/disagg.rs` |
| 21 | `src/core/admission.rs`、`src/core/job_queue.rs`、`src/core/token_bucket.rs` | `src/kv_selfheal.rs` |
| 22 | `src/core/worker.rs`、`src/core/retry.rs`、`src/core/circuit_breaker.rs`、`tests/reliability/` | `src/breaker.rs`、`src/discovery.rs` |
| 23 | `src/server.rs`、`src/middleware.rs`、`tests/inflight_tracker_test.rs` | `src/disagg.rs`、`src/discovery_k8s.rs` |
| 24 | `src/routers/grpc/`、`src/ext_proc/session.rs`、`tests/grpc_engine_drop_tests.rs` | `src/proxy.rs` |
| 25 | `src/policies/`、`src/observability/` | `src/policy.rs`、`src/pool.rs` |

## 当前 Program 状态

| 字段 | 当前值 |
| --- | --- |
| Program ID / 标题 | `rust-language-and-async` / Rust 语言与异步服务端编程 |
| State | `active` |
| Parallel Program ref | [`triton-official-tutorials`](../triton-learning/README.md#当前-program-状态)（`active`）、[`leetcode-algorithm-interview`](../algorithm-interview-learning/README.md#当前-program-状态)（`active`） |
| Objective | 能独立阅读、编写并验证惯用的 Rust 程序，并能设计和实现异步网络服务里的并发控制。语言部分：解释所有权、借用与生命周期怎样在编译期保证内存安全，泛型与 trait 怎样提供抽象、各自付出什么代价，错误和并发怎样用类型表达，以及 Rust 与 C、Python 交界处的安全边界画在哪里。异步部分：解释任务怎样被调度与取消，并在共享状态、背压、超时与重试、排空、流式取消传播上作出有依据的取舍，能回答[上面的目标问题](#异步部分要能回答的问题)。两部分都要能用到没讲过的代码上，在 60–90 秒内讲清一个机制及其取舍。 |
| Included | 语言部分：RBE 快照 24 章的概念、可运行示例和章内 Activity，与示例直接相关的标准库类型和 trait，以及第 17 课里 PyO3 的基础。异步部分：TRPL 第 16、17 章，Tokio 官方教程与专题，以及讲解和练习用到的 `tokio`、`tokio-util`、`tokio-stream`、`dashmap`、`tower`、`axum`、`tonic` 接口。两部分都包括与 C/C++、Python 的对照，以及证据需要时在 `rust/` 完成的最小实践。 |
| Excluded | 过程宏的编写、`no_std` 与嵌入式、完整的 unsafe 规则；运行时内部（调度器、I/O 驱动）的源码级研究；PyO3 基础之外的用法（从 Rust 调用 Python、async 支持、自由线程与发布）；分布式共识、服务发现与集群运维；上面没有列出的第三方 crate 的系统学习；把章节逐节读完当作目标；未获授权的 optional extension、性能研究与下一 Lesson 执行。 |

- **建立授权**：2026-10-07，学习者提出“我现在打算新开一条课程路线——学习rust”，要求基于 RBE 构建系列课程并放在
  本仓库，随后确认按“完整登记”的范围写入。
- **范围扩展**：同日，学习者询问课程是否涵盖 Rust async，并要求“如果没有，希望能添加一些这方面的内容，使得学完后能够
  回答包括但不限于图中的这些问题”。据此加入异步部分（第 18–25 课），原来可选的综合课改为第 25 课的综合项目。
  随后学习者决定把 PyO3 的基础并入第 17 课：“请并进第17课吧”。
- Objective 是按学习者画像和上述要求写出的默认表述，学习者尚未逐条确认；第一课开课时核对。

当前位置只见下方 Checkpoint；已授权课程与各课阶段见[课程索引](#课程索引)链接的记录。

### Checkpoint

| 字段 | 当前值 |
| --- | --- |
| Foreground context | `rust-language-and-async` Program |
| Semantic position | Program 已建立，尚无已授权的 Lesson，位于第一课之前 |
| Next action | 学习者选择第一课并授权开课；候选顺序的第一项是 Lesson 01 `rust-01-hello-formatting` |
| Forward gate | 只有学习者明确授权后才创建并激活对应的 Lesson 记录；候选顺序不构成启动授权 |
| Latest evidence ref | 尚无学习证据；来源快照的核对见[来源记录](../rust-by-example/SOURCE.md#本地核对) |
| As of | 2026-10-07 |

## 本课程的记录约定

通用的证据、练习、Review 与结课规则见中央 `guide-learning`；本课程另外约定：

- **版本锚点**：语言部分的原文、示例行为和输出以固定快照与 Rust 1.97.1 为准，见[来源记录](../rust-by-example/SOURCE.md)。
  引用标准库文档、Rust Reference 或 TRPL 时使用同一版本，即 `https://doc.rust-lang.org/1.97.1/` 下的页面。异步
  部分的其余来源和真实系统的源码锚点在各课开课时固定版本。在线的最新版与固定版本不一致时，讲解顺序沿用固定
  版本，差别记为观察。
- **edition**：RBE 的示例按 edition 2021 编写，仓库的 Cargo workspace 和 TRPL 的示例使用 edition 2024。固定工具链下
  RBE 示例在两个 edition 之间唯一的差别是 FFI 一节的 `extern` 块，在 edition 2024 下要写成 `unsafe extern`；核对
  方法与数字见来源记录。
- **示例与临时试验**：运行或改写书中示例属于讲解的一部分，文件放在仓库外的临时目录，不入库，也不写进快照目录。
  需要留档的代码才属于练习工件。
- **练习位置**：正式练习每课一个 crate，放在 `rust/lessonNN_<topic>/`，包名 `rust-lessonNN-<topic>`，`Cargo.toml`
  沿用 [`leetcode/rust/two_sum`](../../leetcode/rust/two_sum/Cargo.toml) 的写法。验收测试由 Agent 维护，学习者实现
  核心逻辑。单课命令是 `bash scripts/host-cpu.sh run -- cargo test -p rust-lessonNN-<topic> --locked`；
  `host-cpu.sh test` 与 `host-cpu.sh lint` 会覆盖整个 workspace。本课程不需要 GPU。
- **workspace 登记**：第一个练习 crate 创建时，把 `"rust/*"` 加入根 `Cargo.toml` 的 workspace members 并更新
  `Cargo.lock`，在那一份练习约定里一并确认。此前不能提前加：`rust/` 不存在或为空时，这个通配会让整个 workspace
  加载失败；加入之后，`rust/` 下的每个子目录都必须是 crate（核对于 Cargo 1.97.1）。
- **第三方依赖**：第 01–16 课的练习只用标准库；第 17 课的 PyO3 部分和整个异步部分必须用第三方 crate。每个依赖都在
  对应课的练习约定里确认后才加入，版本由根 `Cargo.lock` 固定。已知有三处要在各自的约定里先定做法：
  - PyO3 的练习除了 `pyo3` crate，还需要一个构建并安装扩展模块的工具（指南推荐 maturin，它是 Python 包，不在仓库
    现有的 Python 依赖里）。
  - `tonic` 的代码生成需要 protobuf 编译器 `protoc`，本机没有安装，宿主机的安装清单里也没有。
  - `tonic` 0.14.6 声明的最低 Rust 版本是 1.88，高于 workspace 声明的 `rust-version = "1.85"`，而工具链 1.97.1 本身
    满足这个要求。
- **lint 与书中写法**：仓库的 workspace lint 禁止 `unsafe`，并拒绝 `unwrap`、`expect`、`todo!`、`unimplemented!`
  与 `dbg!`；RBE 快照中有 13 个文件使用 `unwrap`、4 个使用 `expect`、8 个涉及 `unsafe`。练习默认遵守仓库规则。
  确实需要例外的课次（预计是第 12、17 课）在该课的练习约定里单独约定做法，不提前放宽全局规则。
- **按需产物**：`study-log` 的 structured 记录与原文、`memo-cards` 的卡片都只在学习者明确要求时生成。本课程的
  日志与卡片目录还没有登记到这些 Skill 的配置中，第一次需要时再登记。
