# 第 07 课：外部设备函数（libdevice）的分派、链接与取舍

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-07-extern-functions` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 解释 Triton 从 `libdevice.asin(x)` 到 PTX 指令的外部函数全链路，能按精度、dtype 与可移植性选择数学函数实现，并实现、验证一个调用 libdevice 的 kernel |
| 阶段 | `complete`（2026-10-05 学习者确认关闭） |
| 启动授权 | 2026-09-30，学习者提出“接下来让我们开始继续Triton课程下一课吧。我们在本机上进行学习和练习。直到需要实机测试和验证时，再转到带有gpu的机器上。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/07-extern-functions.py` | `teaching-spine` | 仓库 commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；本地 SHA-256 `c9412656298e9bd737d944ac94c5dd6ec427cd30b7657c09d36fa5495ce0d4ba`；与 v3.7.1 tag 中同名文件逐字节一致 | 教学顺序与示例：默认 libdevice 路径、自定义 `extern_libs` |
| [Triton v3.7.1](https://github.com/triton-lang/triton/tree/v3.7.1) | `implementation-authority` | tag `v3.7.1`，commit `f797708c0626e5f9840ca5b0a98790e2c7cb09ad`，与 `uv.lock` 一致；核对于 2026-09-30 | `python/triton/language/{core.py,math.py,extra/}`、`python/triton/compiler/code_generator.py` 的接口模块替换、dtype 分派与 `tl.math` 的 dtype 检查；`third_party/nvidia/{language/cuda/libdevice.py,backend/compiler.py,triton_nvidia.cc}`、`python/src/llvm.cc`、两处 `ElementwiseOpToLLVM.cpp` 的降级、链接与 reflect；`third_party/amd/{language/hip/libdevice.py,backend/compiler.py,python/triton_amd.cc}` 的后端对照 |
| [PyTorch v2.13.0 Inductor](https://github.com/pytorch/pytorch/blob/v2.13.0/torch/_inductor/codegen/triton.py) | `implementation-authority`（真实系统锚点） | tag `v2.13.0`，与 `uv.lock` 一致 | `codegen/triton.py` 对 libdevice、`tl_math`、`sqrt_rn`、`div_rn` 的选择与 `maybe_upcast_float32`；`config.py` 的 `eager_numerics`；`runtime/triton_heuristics.py` 传递 `enable_reflect_ftz` |
| [CUDA libdevice User's Guide](https://docs.nvidia.com/cuda/libdevice-users-guide/index.html) | `interface-authority` | 访问时记录 | `__nv_*` 函数语义；只在节点需要时查阅 |
| [NVCC 文档](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html)、[LLVM NVPTXUsage](https://llvm.org/docs/NVPTXUsage.html) | `interface-authority` | NVCC v13.4；均访问于 2026-09-30 | `--ftz`／`--prec-sqrt`／`--use_fast_math` 的默认值；`__nvvm_reflect` 与反射参数的语义 |
| [CUDA Programming Guide：Mathematical Functions](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/mathematical-functions.html) | `interface-authority` | 访问于 2026-10-04 | 标准与快速数学函数的误差上界；只用于说明精度档位，不代表 Triton 实测 |

### 目标与所需证据

| ID | 可观察目标 | 理解 | 实践 | 实证 |
| --- | --- | --- | --- | --- |
| O1 | 讲清 `libdevice.asin(x)` 从 Python 到 PTX 的全链路：接口模块替换、按 dtype 选符号、TTIR 外部调用、逐元素 LLVM 调用、bitcode 链接与内联，并说出每一段由谁负责、产出什么 | 需要 | 不需要 | 不需要 |
| O2 | 在 `tl.math` 内建、libdevice、`inline_asm_elementwise` 与自定义 bitcode（`extern_libs`）之间，按精度、指令代价、dtype 覆盖与可移植性作出选择；说明 ftz、近似 sqrt 等编译期选项的影响，以及教程自定义路径的前提 | 需要 | 不需要 | 不需要 |
| O3 | 把该机制迁移到 AMD 后端和一个假想的非 NV 加速器后端：说明需要提供哪些组件，缺失时在哪一环失败 | 需要 | 不需要 | 不需要 |
| O4 | 实现并验证一个调用 libdevice 的 Triton kernel：dtype 分派与边界处理正确；本机以 compile-only 检查符号分派与内联，GPU 机器上与 PyTorch 数值对照 | 需要 | 需要 | 不需要 |

性能 benchmark、ulp 误差测量和自行编写 bitcode 库不属于完成门槛，需要时作为结课后的 optional extension
另行授权。

### 当前证据

- **已有证据**：[阶段事件](#条件片段阶段事件) E-01、E-02 提供 O1–O3 的节点级理解证据（节点 1–6）；E-03 的综合验收与变式复查
  使 O1–O3 的理解证据充分。已确认前置：Lesson 01 的
  一维 program／mask 数据流，Lesson 06 中 `tl.math.exp2` 与 base-2 score 的使用；这些只决定讲解起点。
- **仍缺证据**：无。逐项判断见 [Final mastery](#final-mastery)。
- **学习者前置（2026-09-30 反馈）**：编译器背景较少。IR 与降级、声明／定义／链接、内联、编译期分支四个概念已在
  图解页补齐；涉及编译器内部的内容先补前置并配图，再检查。
- **来源与环境核对（2026-09-30）**：本机无 NVIDIA GPU。为观察编译产物，在仓库外的临时虚拟环境中安装
  `triton==3.7.1`（未装 PyTorch），以 `GPUTarget("cuda", 90, 32)` 只编译不运行。观察到：fp32 输入在 TTIR 中
  生成 `tt.extern_elementwise {symbol = "__nv_asinf"}`；PTX 中没有 `call`，`asin` 已内联为 `fma.rn.ftz.f32`、
  `sqrt.approx.ftz.f32` 等指令；fp64 选中 `__nv_asin`；fp16 输入在编译期报 `KeyError`。按教程第二段拼出的
  自定义路径在本仓库快照位置不存在，compile 报 `FileNotFoundError`；传入 wheel 自带的
  `triton/backends/nvidia/lib/libdevice.10.bc` 则正常。这些是本地编译观察，不代表 GPU 上的数值结果。
- **来源与环境核对（2026-10-04）**：同一临时环境的只编译观察。NVIDIA 目标上，`tl.log`、`tl.sin`、`tl.erf`、`tl.sqrt`、
  `tl.rsqrt`、`tl.floor`、`tl.exp2` 在链接前同样声明 `__nv_*`，PTX 与对应的 `libdevice.*` 相同；`tl.exp`（`mul`＋
  `ex2.approx.f32`）、`tl.sqrt_rn`（`sqrt.rn.f32`）、`/` 与 `tl.fdiv`（`div.full.f32`）、`tl.div_rn`（`div.rn.f32`）由后端
  直接生成指令。内联汇编文本原样进入 PTX；手写的文本 LLVM IR 经 `extern_libs` 可链接并内联，缺库时 ptxas 报
  `Unresolved extern function`。AMD 目标（`gfx942`）可完整编译到 hsaco：符号 `__ocml_asin_f32`，每个 warp 64 线程，
  只链接 `ocml.bc`，内联后无调用；同一段 PTX 内联汇编在 AMD 汇编阶段报 `invalid instruction`；自定义库只有键名出现在
  未定义函数名中才被链接，否则编译不报错但留下未解析的调用。以上均未在 GPU 上运行。
- **教学更正（2026-10-04）**：开课导入称 `tl.math.exp2` 由 Triton 直接降级为一条硬件指令。实测它经 `__nv_exp2f` 链接并
  内联后得到 `ex2.approx.ftz.f32`：结果是一条指令，路径是 libdevice。已在节点 5 向学习者更正。
- **教学更正（2026-10-04，复查题前提）**：复查第 2 题假设“在 AMD 上传 `enable_reflect_ftz` 后没有效果”。v3.7.1 的
  `JITFunction._pack_args`（`python/triton/runtime/jit.py`）对既不属于后端选项、也不属于 kernel 签名的关键字参数抛
  `KeyError`，所以真实启动会直接报错；只有 `triton.compile(..., options=...)` 入口会丢弃未知选项。已向学习者更正，
  不影响其回答的判定。
- **GPU 运行环境（2026-10-05）**：容器路线，NVIDIA GeForce RTX 4070 Ti，PyTorch `2.13.0+cu130`，CUDA build `13.0`，
  Triton `3.7.1`；驱动版本未记录。只编译测试的目标固定为 `sm_90`，与运行设备无关。
- **OBS-07-FTZ-01（本地观察，可选项，不进门槛）**：学习者事前预测“默认输出 0，关闭 ftz 后非 0”。同一环境下以
  `observe_subnormal_ftz.py` 启动学习者的 `asin_kernel`：输入 `±1e-40` 与 `1e-39`（fp32 次正规数）时，`torch.asin` 原样返回，
  Triton 默认设置输出 `±0`（保留符号），传 `enable_reflect_ftz=False` 后与 `torch.asin` 一致；最小正规数 `1.175494351e-38`、
  `2e-38` 与 `0.5` 三者相同。支持节点 4 的预测；只覆盖这一台设备上的 `asin` 与这几个输入，不推广到其他函数或后端。
- **OBS-07-ASIN-01（本地观察，结课前答疑）**：学习者问两个后端内联后 fma 条数为何不同。对比链接进来的函数体：`__ocml_asin_f32`
  用一条 fma 计算 `(1 − |x|) / 2`，多项式有 6 个系数，分界点 0.5，两个分支的最后一步各用一条 fma，`π/2` 由两个常数在 fma 内相乘得到；
  `__nv_asinf` 用减法加乘法，多项式 5 个系数，分界点 0.57，先选变量再共用一条 fma。每元素算术指令约为 AMD 17 条、NVIDIA 19 条，
  差别在算法写法而非工作量；两家的精度目标未查到来源。图解页节点 6 的表格与说明已据此更正。
- **OBS-07-TUT-01（来源 observation，静态阅读）**：v3.7.1 的 `HIPOptions.__post_init__` 无条件用默认路径覆盖 `ocml`、
  `ockl`，教程 HIP 分支传入的自定义路径在该版本不会生效；CUDA 分支的路径只在上游源码树布局下存在。本地只读快照
  保持原样。
- **权威知识产物**：固定教程源码与上方来源记录。

### 核心工件与参考

| 角色 | 路径或引用 | 说明 |
| --- | --- | --- |
| 你写（learner-owned） | [`lesson07_extern_functions.py`](../../../gpu/triton/lesson07_extern_functions.py) | P1 的核心实现与 A6 变式；本机层全部通过的版本 SHA-256 `b4069dddd1b7138497249f0f861f361c5da7a58cdc11f6a718b922a5270fbf3f` |
| 我维护（agent-owned） | [`lesson07_extern_functions_test.py`](../../../gpu/triton/lesson07_extern_functions_test.py) | P1 的验收测试，共 60 项：主体 41 项，A6 变式 19 项 |
| 我维护（agent-owned） | [`observe_subnormal_ftz.py`](../attachments/07-extern-functions/observe_subnormal_ftz.py) | 可选观察脚本（不进门槛）：GPU 上对比默认与 `enable_reflect_ftz=False` 时次正规数输入的输出 |
| 来源或知识产物 | [`07-extern-functions.py`](../../triton-tutorials/official/07-extern-functions.py) | 只读教程快照 |
| 来源或知识产物 | [`libdevice-asin-pipeline.html`](../attachments/07-extern-functions/libdevice-asin-pipeline.html) | 节点 3–6 的交互图解：四个编译器前置概念、逐站跟踪、布局实验、链接／内联／reflect 对照图、四条实现路线与 NVIDIA／AMD 对照；片段来自 2026-09-30 与 2026-10-04 的本机 compile-only 产物 |

## 条件片段：练习约定

- **编号与版本**：P1，版本 1；学习者接受于 2026-10-04（回复“接受”）。
- **为什么做**：O4 需要实践证据，即独立写出一个调用 libdevice 的 kernel，并证明输入类型与边界处理正确。O1–O3 的
  理解证据已充分。
- **你交付什么**：`gpu/triton/lesson07_extern_functions.py`，包含 kernel
  `asin_kernel(x_ptr, y_ptr, n_elements, BLOCK_SIZE: tl.constexpr)`（参数名与教程一致）、包装函数
  `asin(x, *, extern_libs=None)`，以及返回已安装 Triton 自带 `libdevice.10.bc` 路径的 `bundled_libdevice_path()`。
- **验收项**：

| ID | 可观察标准 | 检查方式 |
| --- | --- | --- |
| A1 | 编译期按类型分派：同一个 `asin_kernel` 在指针类型为 fp16、bf16、fp32、fp64 时都能编译；前三种选中 `__nv_asinf`，fp64 选中 `__nv_asin`；PTX 中没有函数调用。半精度输入在 kernel 内部升精度，不在包装函数里另建 fp32 张量 | 只编译测试（本机）；源码 Review |
| A2 | 接口与边界：`asin(x)` 返回形状、dtype、设备与 `x` 相同的新张量，不修改 `x`；支持多维输入和元素个数不是 `BLOCK_SIZE` 整数倍的输入；空张量返回同形状的空张量。输入不在 CUDA 上、内存不连续、dtype 不是上述四种时报 `ValueError` | 测试：“不在 CUDA 上”在本机，其余在 GPU |
| A3 | 数值：与 `torch.asin` 对照。fp32 的 rtol 为 1e-5，fp64 为 1e-12；fp16、bf16 的参考值是“先转 fp32 计算，再转回原类型”，最多差该类型的一个最小间隔。`x` 为 ±1 和 0 时正确；`|x| > 1` 与 NaN 输入得到 NaN | 测试（GPU） |
| A4 | 库路径：`bundled_libdevice_path()` 指向真实存在、名为 `libdevice.10.bc` 的文件；`extern_libs` 原样传给 kernel，传自带库路径时结果与默认完全相同，传不存在的路径时报 `FileNotFoundError` | 测试：路径与只编译部分在本机，启动部分在 GPU |
| A5 | 解释一个验证：说明 A1 的测试凭什么能证明“升精度发生在 kernel 内”和“函数被内联” | 学习者的文字说明 |
| A6 | 一个无提示的小变式：主体通过后，换一个 libdevice 函数再写一个更小的 kernel，原理相同；题目与测试届时给出 | 测试 |

- **文件边界**：

| 边界 | 路径或受限模式 |
| --- | --- |
| 你写 | `gpu/triton/lesson07_extern_functions.py` |
| 我维护 | `gpu/triton/lesson07_extern_functions_test.py`；本 Lesson 记录；Program 页的 Checkpoint；`docs/triton-learning/attachments/07-extern-functions/` |
| 我只读 | 学习者的实现文件；`docs/triton-tutorials/official/07-extern-functions.py` |
| 本次不动 | 环境脚本、`pyproject.toml`、`uv.lock`、CI、其他课的文件 |

- **运行方式**：本机无 GPU 时，在仓库根目录运行
  `uv run --no-project --no-config --python 3.12 --with pytest --with numpy --with "triton==3.7.1" --with "torch==2.13.0" python -m pytest -q gpu/triton/lesson07_extern_functions_test.py`；
  它不改动仓库的虚拟环境与配置，需要 GPU 的测试自动跳过。GPU 机器上运行
  `bash scripts/host-gpu.sh run -- python -m pytest -q gpu/triton/lesson07_extern_functions_test.py`。
- **求助如何影响证据**：透露关键解法只影响相应范围，之后由 A6 的变式在无提示下恢复。
- **非目标与可选项**：性能测试、与 `torch.asin` 逐位一致、AMD 实机运行、自行编写 bitcode 库、超过 2³¹ 个元素的输入
  均不在范围内。Ruff 检查不进完成门槛，但提交前需要通过。可选项（不进门槛）：在 GPU 上观察默认与
  `enable_reflect_ftz=False` 两种设置下 `asin(1e-40)` 的输出，学习者先预测。
- **A6 的题目（2026-10-04，本机层通过后给出）**：在同一个实现文件中增加两样。其一，kernel
  `atan2_kernel(y_ptr, x_ptr, out_ptr, n_elements, BLOCK_SIZE: tl.constexpr)`，逐元素计算 `atan2(y, x)`；三个指针的
  元素类型相同，为 fp16、bf16、fp32、fp64 之一；前三种选中 `__nv_atan2f`，fp64 选中 `__nv_atan2`；PTX 中没有函数调用；
  不需要包装函数，GPU 测试直接启动 kernel 并与 `torch.atan2` 对照。其二，`bundled_ocml_path()`，返回已安装 Triton 自带
  的 AMD 数学库 `ocml.bc` 的路径，用于恢复 A4 路径部分的独立证据。两项都不给实现提示。
- **验收准备（2026-10-04）**：测试共 41 项。本机层 9 项：实现文件存在、导出与签名、四种 dtype 的符号分派与内联、
  自带库路径、显式库路径下的编译、拒绝 CPU 输入。GPU 层 32 项：16 组形状与 dtype 的数值和元数据、特殊值、定义域外
  与 NaN、空张量、不连续与不支持的 dtype、`extern_libs` 的两种启动情况。当前 expected red 为
  `1 failed / 40 skipped`，唯一失败是学习者的实现文件尚不存在。Ruff check、格式检查与 BasedPyright 通过。测试用仓库外
  的参考实现核验：本机层 9 项通过；GPU 层的逻辑用 CPU 替身核验，替身正确或只差几个最小间隔时 40 项通过，故意算错时
  数值相关的 15 项失败。GPU 层尚未在真实设备上运行，届时若暴露测试自身的问题，由 Agent 修复，不记为学习者的问题。
  Agent 未创建或修改学习者的实现文件。
- **A6 的验收准备（2026-10-04）**：新增 19 项，测试共 60 项。本机层 7 项：变式是否已实现、导出与参数名、四种 dtype 的
  符号分派与内联、`ocml.bc` 路径；GPU 层 12 项：3 种长度与 4 种 dtype 的数值对照。主体的比较函数拆出一个通用版本供
  变式复用，主体测试的判定不变。对学习者当前实现的结果为 `1 failed / 9 passed / 50 skipped`，唯一失败是变式尚未实现。
  用仓库外的参考实现核验：本机层 16 项通过；GPU 层逻辑用 CPU 替身核验，正确或只差几个最小间隔时通过，算错 1% 时
  变式的 12 项全部失败。Ruff 与 BasedPyright 通过。GPU 层尚未在真实设备上运行。

## 条件片段：帮助影响

| 透露到什么程度 | 影响的验收项或工件 | Agent 是否写了学习者核心工件 |
| --- | --- | --- |
| 2026-10-04：学习者不清楚 `bundled_libdevice_path` 应返回哪个路径。给出了分解（先在运行时定位已安装的 `triton` 包目录，再拼上固定的相对位置）、Triton 计算默认路径的源码出处，以及“已导入的模块能报告自己的加载位置”这一概念；没有给代码。 | A4 的路径部分：这一小块的独立证据失效，由 A6 的变式中一个同类小问在无提示下恢复。已恢复（2026-10-05）：学习者无提示写出 `bundled_ocml_path`，本机测试通过 | 否 |

## 条件片段：需要跟踪的问题

| ID | 对应验收项或目标 | 严重度 | 状态 | 证据 |
| --- | --- | --- | --- | --- |
| F1 | A1 | 阻塞 | 已关闭 | 2026-10-04 首次 Review：指针类型为 fp16、bf16 时编译失败（`KeyError`）。第二次 Review：类型处理改由新增的 `is_bf16`、`is_fp16` 两个 `constexpr` 参数驱动，kernel 变为 6 个参数，与约定的 4 个参数不符；导出检查和按约定签名编译的 5 项测试失败。按学习者自己的签名私下编译，四种 dtype 的符号与内联均正确，差距只在接口；标志与指针类型矛盾时（如 fp32 指针配 `is_fp16=True`）能通过编译并静默损失精度。 关闭证据（第三次 Review）：kernel 恢复为约定的 4 个参数，用加载结果的 dtype 做编译期分支；本机层 9 项全部通过，四种 dtype 的符号分派与内联测试通过，源码中升精度发生在 kernel 内。 |
| F2 | A2、A3 | 阻塞 | 已关闭 | 2026-10-04 首次 Review（源码阅读）：包装函数把 `x` 同时作为输入与输出，且没有返回值。第二次 Review：源码已改为新建输出张量并返回；GPU 层测试尚未运行，待复验后关闭。 关闭证据（2026-10-05，RTX 4070 Ti）：16 组数值与元数据测试、特殊值、定义域外与空张量测试全部通过，返回新张量且输入未被修改。 |
| F3 | A2 | 阻塞 | 已关闭 | 2026-10-04 首次 Review：传入 CPU 张量时抛 `RuntimeError`，且没有连续性与 dtype 检查。第二次 Review：本机“拒绝 CPU 输入”通过，源码已加入三项检查；连续性与 dtype 两项负例属 GPU 层，待复验后关闭。 关闭证据（2026-10-05，RTX 4070 Ti）：内存不连续与三种不支持的 dtype 的负例在 GPU 上通过。 |

## 条件片段：阶段事件

| 日期 | 覆盖范围 | 证明了什么 | 证据链接 | 标注 |
| --- | --- | --- | --- | --- |
| 2026-09-30 | E-01：开课导入、节点 1–2；节点 3–4 首讲 | 节点 1–2 的检查题（`xpu` 场景的诊断与迁移）一次答对：把 fp16 输入的编译失败定位到 dtype 查表，给出显式升到 fp32 的修复，并区分“后端未实现函数”与“dtype 不在表中”及其报错。节点 3–4 首讲后学习者反馈编译器前置不足；原诊断题因前置未建立而撤回，不记为学习者错误，改以交互图解补讲。 | [图解页](../attachments/07-extern-functions/libdevice-asin-pipeline.html) | 无 |
| 2026-10-04 | E-02：节点 3–4 图解后的自测；节点 5–6 讲解与检查；导师串讲 | 两道自测题一次答对：`BLOCK_SIZE=2048` 时 E=16，1 条声明对 16 次调用，链接后 1 份定义，内联后 16 份函数体且无调用，并说明声明与调用、定义与内联副本的区别；预测 `__CUDA_PREC_SQRT=1` 时 sqrt 变为 `sqrt.rn.ftz`，说明各份函数体都保留分支、生成 PTX 时统一选定。节点 5–6 的检查题：诊断问一次答对，把 `xpu` 机器码里残留的真实调用归因于库函数未被内联，并提出对比 O3 前后的 LLVM IR 来确认；取舍问指出了 SiLU 中 `/` 与 `tl.exp` 两处快速档、对应指令和误差随 |x| 放大的原因，但该问“各换成什么”的措辞有歧义，“应改写成什么及其速度代价”并入综合验收重问，不记为学习者错误。导师串讲已完成，综合验收三题待答。 | 图解页自测题 1–3 | 无 |
| 2026-10-04 | E-03：综合验收与复查；练习约定 P1 的接受与验收准备 | 口述题讲清了从接口模块替换、查表、布局、逐元素调用到链接、O3 内联的完整顺序与各环职责，并说明机器码里没有调用源于内联；首答没有用上 fp16 与 AMD 两个条件。取舍题给出 `libdevice.exp` 与 `tl.div_rn` 两处改写、exp 的指令代价和保留快速档的条件，并如实说明不清楚除法的速度代价（来源本身也没有实测数字）。诊断题首答只覆盖 NVIDIA 的 reflect／ftz 机制。补差后两道变式复查一次答对：`libdevice.pow(bf16, fp32)` 在查表处报 `KeyError`，应先把 `x` 转成 fp32；AMD 侧应使用 `allow_flush_denorm`。O1–O3 的理解证据充分。随后学习者接受练习约定 P1（版本 1），验收测试已建立并确认 expected red。 | 图解页“综合验收”；[练习约定](#条件片段练习约定) | 无 |
| 2026-10-04 | E-04：P1 第一至三次提交与 Review | 首次提交：本机层 `6 passed / 3 failed`，记录 F1–F3 三个阻塞问题；`bundled_libdevice_path` 在一次分解层面的帮助后实现正确，相应独立证据待 A6 恢复。第二次提交：输出语义与输入检查已按约定修改；半精度分派逻辑正确，但通过新增两个 kernel 参数实现，与约定的签名不符，F1 未关闭。第三次提交：学习者在只被告知“分支依据须由 kernel 自己得到”的情况下，独立改为按加载结果的 dtype 做编译期分支，本机层 `9 passed / 32 skipped`，F1 关闭；F2、F3 的源码已修改，待 GPU 层复验。不阻塞的观察：升精度后变量已是 fp32，其后按半精度判断的两段分支不会执行，写回由 `tl.store` 的隐式转换完成（TTIR 中 `truncf` 的源码位置是 `tl.store` 一行）；文件末尾缺换行（Ruff W292）。随后给出 A5 与 A6。 | [需要跟踪的问题](#条件片段需要跟踪的问题)；[帮助影响](#条件片段帮助影响)；[练习约定](#条件片段练习约定) | 无 |
| 2026-10-05 | E-05：A5、一次答疑与 A6 的本机层 | A5 通过：学习者说明编译测试直接编译 kernel、不经过包装函数，半精度指针下能编译且选中只接受 fp32 的 `__nv_asinf`，因此升精度必然发生在 kernel 内；PTX 中匹配不到 `call`，说明函数已被内联。学习者另问“把 dtype 判断结果先存进变量再 `if`”为何编译失败：已按 v3.7.1 源码与本机探针答复，属语言语义答疑，不涉及 A6 的解法。A6 在无提示下完成：`atan2_kernel` 四种 dtype 的符号分派与内联、参数名、`bundled_ocml_path` 均通过，本机层 `16 passed / 44 skipped`；主体中不会执行的两段分支已删除，Ruff check 与格式检查通过。GPU 层 44 项（主体 32、变式 12）与 F2、F3 的复验待在 GPU 机器上进行；另备可选的次正规数观察脚本。 | 对话；[需要跟踪的问题](#条件片段需要跟踪的问题)；[帮助影响](#条件片段帮助影响) | 无 |
| 2026-10-05 | E-06：GPU 层验收、可选观察、结课前答疑与结课 | 学习者在 GPU 机器上运行全部验收测试：`60 passed`，其中 GPU 层 44 项（主体 32、A6 变式 12）首次在真实设备上运行并全部通过，未暴露测试自身的问题；F2、F3 复验关闭。A1–A6 全部满足：核心工件通过验收，阻塞问题全部关闭，A5 解释了一个验证，A6 在无提示下完成，帮助影响已恢复。可选观察中学习者的事前预测与结果一致（OBS-07-FTZ-01）。O4 的实践证据充分。结课前学习者追问两个后端内联后 fma 条数为何不同，已按链接进来的函数体答复（OBS-07-ASIN-01）。随后学习者确认结课。 | 学习者提供的 pytest 与观察脚本输出；[需要跟踪的问题](#条件片段需要跟踪的问题) | 结课 |

<a id="final-mastery"></a>

## 条件片段：结课

| 目标 | 所需证据 | 证据链接 | 判断 |
| --- | --- | --- | --- |
| O1：从 Python 到 PTX 的全链路 | 理解 | E-01、E-02 的节点检查与图解后自测；E-03 的口述题与复查 | 充分 |
| O2：按精度、dtype 与可移植性选择实现 | 理解 | E-02 的节点 5 检查；E-03 的取舍题与 `libdevice.pow` 变式复查 | 充分 |
| O3：迁移到 AMD 与假想的新后端 | 理解 | E-01 与 E-02 的 `xpu` 诊断题；E-03 的跨后端次正规数题与复查 | 充分 |
| O4：实现并验证调用 libdevice 的 kernel | 理解、实践 | [练习约定 P1](#条件片段练习约定) 的 A1–A6；E-04 至 E-06：本机层 16 项与 GPU 层 44 项通过，F1–F3 关闭，A5 解释与 A6 无提示变式 | 充分 |

- **未关闭的阻塞问题**：0。F1–F3 均已关闭，见[需要跟踪的问题](#条件片段需要跟踪的问题)。
- **帮助影响是否已恢复**：是。`bundled_libdevice_path` 的分解层面帮助，已由 A6 中无提示完成的 `bundled_ocml_path` 恢复，见
  [帮助影响](#条件片段帮助影响)。
- **非阻塞余项**：快速档与精确档（exp、除法、sqrt）的实际速度差和误差未实测；AMD 后端只有只编译观察，未在真实设备上运行；
  本次 GPU 运行未记录驱动版本。三项都不在本课范围内，需要时作为 optional extension 另行授权。
- **学习者确认**：2026-10-05，学习者回复“明白了，可以结课了。”
- **结课结论**：学习者能独立讲清一次 `libdevice` 调用从接口模块替换、按 dtype 查表、布局与逐元素调用，到链接、内联和反射参数
  选定写法的全链路，并说明每一环的职责与出错现象；能按精度、dtype 与可移植性在 `tl.math`、libdevice、内联汇编与自定义库之间
  选择，并把同一机制迁移到 AMD 后端和假想的新后端；独立实现了按输入类型在编译期分派的 `asin` 与 `atan2` kernel，通过只编译与
  GPU 数值验收。本结论的范围是 Triton v3.7.1、NVIDIA 后端的只编译观察与一台 RTX 4070 Ti 上的数值验收；AMD 侧为只编译观察。
