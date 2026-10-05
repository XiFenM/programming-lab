# 学习记录 · 2026-10-05 · 外部函数（libdevice）的全链路、取舍与 asin 实践

> 来源：claude:08d279c9（完整会话 ID：`08d279c9-e031-4916-9699-0064ed77037f`），2026-09-30—10-05。
> 消息边界：`msg-ba84e41635dc7c0c8dc7` → `msg-8d07d15dd9009350ed04`，共 90 条可见消息。范围内的 `msg-66354bd786f3867bccb8` 是复查题被重发前的第一次回复，已被重发后的回复取代，按学习者要求不收入本记录和同名原文。
> Source SHA-256：`2e6a3603800d91c08e60dfc9aaefa6653d9390a9f151bb38ef8db17ce1fa5f87`（提取时对进行中的会话文件所做的快照）。
> 关联：[第 07 课](../lessons/07-extern-functions.md)、[交互图解](../attachments/07-extern-functions/libdevice-asin-pipeline.html)。完整讲解见图解页，练习约定、问题跟踪与结课结论见 Lesson；本记录保留学习者的原始回答、纠错、追问与转折，以及可独立复习的最小结论，不代替课程状态或知识权威。
> 可追溯对话：[同名原文](../logs-raw/2026-10-05-extern-functions.md)，由被略去那条回复前后的两段连续范围合并而成，各段来源与校验值见其元数据。
> 源码锚点：[官方本地快照](../../triton-tutorials/official/07-extern-functions.py)，SHA-256 `c9412656298e9bd737d944ac94c5dd6ec427cd30b7657c09d36fa5495ce0d4ba`；实现事实以 Triton v3.7.1 为准。
> 证据边界：从指定 extract 蒸馏。只编译的观察来自当时本机的临时环境；GPU 结果仅来自学习者在 RTX 4070 Ti 上的实测报告。本次整理没有重新运行任何测试。

## 接口模块与 dtype 查表

- [要点] kernel 里写的 `libdevice.asin` 为什么能在不同后端上编译？——`triton.language.extra.libdevice` 只是接口模块，里面的函数是空壳。编译到 TTIR 时，后端的 `get_module_map()` 把它整体换成自己的实现，CUDA 是 `…extra.cuda.libdevice`。直接导入 CUDA 的实现模块也能用，但 kernel 就绑定在 CUDA 上了。（来源：`msg-3f21a5d930e606f6c5d6`。）

- [要点] 后端实现里的一个 libdevice 函数，本质上是什么？——一张“参数 dtype 元组 → (符号名, 返回 dtype)”的表。`extern_elementwise` 在编译期用实参的 dtype 查表，生成带 `symbol` 的 `tt.extern_elementwise`；查不到就编译失败，不做隐式类型提升。`asin` 的表只有 fp32 对 `__nv_asinf`、fp64 对 `__nv_asin` 两项。（来源：`msg-3f21a5d930e606f6c5d6`。）

- [要点] fp16 张量直接传给 `libdevice.erf`，会在哪一步失败，怎么修？——学习者首答正确：“发生在节点2的根据实参dtype查找表的过程中，可能查不到对应fp16的符号。kernel这边最小的修复是可以在load完成后加一个.to(tl.float32)”。真实报错是 `KeyError: (triton.language.float16)`。结果写回 fp16 指针时，`tl.store` 会自动转成指针的元素类型。（来源：`msg-a3304a69e81ed3f4816d`、`msg-e19abb89fda9453a8d05`。）

- [要点] 修好 dtype 后，新后端上同一处调用仍然失败，两种原因怎样区分？——学习者答：“（1）xpu的后端库实现中还没实现erf函数（2）xpu的后端的erf函数实现对于fp32也不支持”，看报错写的是缺函数还是 dtype 不支持。前者是 `AttributeError: module '…libdevice' has no attribute '…'`，发生在模块替换之后取属性时；后者是查表处的 `KeyError`。`AttributeError` 里的模块名是替换后的名字，可以借此确认替换已经生效。（来源：`msg-a3304a69e81ed3f4816d`、`msg-e19abb89fda9453a8d05`。）

- [要点] 后端的 `get_module_map()` 没有生效时，现象是什么？——kernel 调到接口里的空壳函数，它静默返回 `None`。报错要到下一行才出现，指向 `tl.store`：`cannot convert None of type <class 'NoneType'> to tensor`，看上去和 libdevice 无关。（来源：`msg-e19abb89fda9453a8d05`。）

- [要点] `tl.math` 和 libdevice 为什么都只接受 fp32、fp64？——`tl.math` 的 `_check_dtype` 在源码里写明：沿用 libdevice 的约定，很多加速器不支持 fp16、bf16 的数学运算，应让用户知情并显式转换。助手在节点 2 把“不做隐式提升是有意的”标为推断，后来由这段源码证实。（来源：`msg-3f21a5d930e606f6c5d6`、`msg-8dce86aba8c15ba7972b`。）

## 编译器前置与逐元素调用、链接、内联

- [转折] 节点 3、4 为什么改用图解重讲？——学习者说明：“我对于编译器的了解非常少。所以关于这两个节点所讲的，我不太看得懂，希望可以使用一些可视化的方式对其中的一些复杂点、难点进行详细描述”。助手承认讲解默认了没有建立的前置，撤回当时的诊断题且不计入回答，先补四个编译器概念，再用交互图解重讲。学习者随后要求“html产物放在本地仓库里吧。这样方便复习。”（来源：`msg-22a69eb78541fe6d6ae3`、`msg-6a61f523ee4d2945c4cf`、`msg-44d3676e0a5a54ecca26`。）

- [要点] 声明、定义、链接、内联分别是什么，对应 C/C++ 里的什么？——声明只有名字和签名，定义才有函数体；链接是按名字把调用接到定义上，找不到就是 `undefined reference`；内联是把调用换成一份函数体，对应 `inline`。本课里，链接前只有 `declare float @__nv_asinf(float)`，函数体在 `libdevice.10.bc` 中。（来源：`msg-6a61f523ee4d2945c4cf`；图示见[图解页](../attachments/07-extern-functions/libdevice-asin-pipeline.html)。）

- [要点] `BLOCK_SIZE=2048`、`num_warps=4` 时，每个线程几个元素？声明和调用各几条，为什么不同？——学习者首答正确：“每个线程持有BLOCK_SIZE / (num_warps * 32) = 2048 / (4 * 32) = 16个元素。declare @__nv_asinf 依旧只有1条……call @__nv_asinf 有16条”，理由是“函数声明只需一次，后续调用次数则根据持有元素数量而定”。（来源：`msg-a9826744adf4e2cd5a8d`。）

- [要点] 链接后定义只有一份，O3 之后函数体却有多份，为什么？——学习者答：“LLVM优化器进行了函数内联优化，将函数定义内联嵌入到了调用位置，原本的调用也就消除了”。链接按名字只拷入一份定义；内联在每个调用处各放一份，所以是 16 份函数体、0 条 `call`。补充：内联之后没人再调用那份定义，它本身也被删除。（来源：`msg-a9826744adf4e2cd5a8d`、`msg-8dce86aba8c15ba7972b`。）

- [要点] 如果 `__CUDA_PREC_SQRT` 也取 1，`asin` 里的 sqrt 变成哪条指令？为什么所有函数体一起变？——学习者预测“会变成sqrt.rn.ftz”，正确。各份函数体抄自同一份定义，都带着同一句查询；这个参数整个模块只有一个值，生成 PTX 时所有查询被换成同一个常数。每份函数体保留的分支共四种：ftz 与否，乘以精确与近似。（来源：`msg-a9826744adf4e2cd5a8d`、`msg-8dce86aba8c15ba7972b`。）

- [要点] 指针按 16 特化后访存变成 `ld.global.v4.b32`，为什么 `asin` 的展开仍是每元素一份？——布局里的 S 只决定相邻元素能否合成一次更宽的访存。libdevice 函数的签名是标量的，逐元素生成调用；并行来自 warp 里同时执行同一条指令的 32 个线程，所以每线程元素数 E 不变，展开份数也不变。（来源：`msg-e19abb89fda9453a8d05`。）

- [要点] 链接这一步怎样决定用哪个库、拷多少、何时重新编译？——默认用 wheel 自带的 `triton/backends/nvidia/lib/libdevice.10.bc`，可由 `TRITON_LIBDEVICE_PATH` 或启动参数 `extern_libs` 替换。模块里有未定义的外部函数时才链接，`LinkOnlyNeeded` 只拷入用到的定义并设为 internal。库文件的内容哈希计入编译缓存键，换库会重新编译。（来源：`msg-e19abb89fda9453a8d05`。）

- [要点] 教程第二段演示自定义 libdevice 路径，为什么在本仓库或 pip 环境里跑不通？——教程拼路径的方式假设脚本位于 Triton 源码树的 `python/tutorials/` 下，在本仓库的快照位置或 pip 安装的环境里这个路径不存在。库文件的内容要参与计算缓存键，所以错误出现得很早：还没生成任何 IR，就报 `FileNotFoundError`。pip 环境里正确的位置是已安装 `triton` 包下的 `backends/nvidia/lib/libdevice.10.bc`。（来源：`msg-e19abb89fda9453a8d05`、`msg-8dce86aba8c15ba7972b`。）

- [要点] 在 ftz 和 sqrt 这两个开关上，Triton 默认编进来的 libdevice 相当于 nvcc 的哪种设置？——Triton 默认设置 `nvvm-reflect-ftz=1`，`__CUDA_PREC_SQRT` 没人设置而按 0 处理，所以是“冲掉次正规数、近似 sqrt”。nvcc 默认是 `--ftz=false`、`--prec-sqrt=true`，只有 `--use_fast_math` 才与 Triton 的默认一致。反射参数只作用于 libdevice 函数内部。（来源：`msg-e19abb89fda9453a8d05`。）

## 四条实现路线与后端迁移

- [转折] 开课时的一个说法被探针推翻。——助手开课时说 `tl.math.exp2` 由 Triton 直接降级成一条硬件指令。实测它先变成对 `__nv_exp2f` 的调用，链接、内联后才剩一条 `ex2` 指令：结果对，路径说错了。由此得到节点 5 的第一个结论：`tl.math` 和 libdevice 不是“指令”对“库”的关系。（来源：`msg-3f21a5d930e606f6c5d6`、`msg-8dce86aba8c15ba7972b`。）

- [要点] NVIDIA 后端上，`tl.math` 的哪些函数直接生成指令，哪些其实走 libdevice？——本机测到直接出指令的有 `tl.exp`、`tl.sqrt_rn`、除法、`tl.abs`。`tl.log`、`tl.sin`、`tl.erf`、`tl.sqrt`、`tl.rsqrt`、`tl.floor`、`tl.exp2` 被改成 `__nv_*` 调用，PTX 与对应的 `libdevice.*` 完全相同。`tl.math` 是后端中立的写法，怎么实现由各后端决定：同样的只编译观察里，AMD 后端的 exp、log、sqrt 不链接任何库，erf、sin 才走它的数学库。（来源：`msg-8dce86aba8c15ba7972b`。）

- [要点] exp、sqrt、除法各自的快速档和精确档是什么？——`tl.exp` 每元素 2 条指令，`libdevice.exp` 是 8 条；`tl.sqrt` 是近似，`tl.sqrt_rn` 是 IEEE 就近舍入；`a / b` 生成近似的 `div.full`，`tl.div_rn` 生成 `div.rn`。PyTorch 2.13 的 Inductor 为贴近 eager，sqrt 一律生成 `tl.sqrt_rn`，exp 默认生成 `libdevice.exp`，并用 `eager_numerics` 的开关控制除法舍入、ftz 和 libdevice 的版本。其中改用 CUDA 工具链的 libdevice，是因为源码注释说两份库的多项式不同，`erf`、`pow` 会差约 1 ulp。（来源：`msg-8dce86aba8c15ba7972b`。）

- [要点] 快速版 exp 为什么在 |x| 大时更不准？——学习者自己说出了机制：“由于tl.exp会先做log系数乘积再做指数计算，会导致在|x| 大时，放大指数结果误差”。乘积只有 24 位有效数字，丢掉的误差被指数放大。CUDA 文档给同类快速函数的上界是 2 + ⌊|1.173·x|⌋ ulp，标准 `expf` 是 2 ulp；用在 Triton 上是推断，没有实测。（来源：`msg-0cb671c61108393bea26`、`msg-115c0150ef294e79ebc5`。）

- [转折] 一道题因为措辞有歧义而重问。——题目问 SiLU kernel 里两处快速档“各换成什么”。学习者答的是它们被编译成什么：“各自换成了‘div.full.f32’和‘`mul.f32`、`ex2.approx.f32`’。各自的代价是2ulp和2 + ⌊|1.173·x|⌋ ulp”，内容本身正确。助手承认“换成”可以有两种理解，不记为学习者的错误，把“应改写成什么、速度代价是什么”放进综合验收重问。（来源：`msg-0cb671c61108393bea26`、`msg-115c0150ef294e79ebc5`。）

- [要点] 内联汇编为什么不可移植？——`tl.inline_asm_elementwise` 里写的指令文本不经过链接，原样带到最终汇编。同一段 PTX 文本换成 AMD 目标，会被原样写进 AMD 汇编，汇编器报 `invalid instruction`，在最后一步失败。（来源：`msg-8dce86aba8c15ba7972b`。）

- [要点] 自己提供数学库要准备什么，缺了库是什么现象？——用 `core.extern_elementwise` 写一张“dtype → 符号”的表，再用 `extern_libs` 传入含有这些定义的 bitcode 或文本 LLVM IR 文件，之后走和 libdevice 完全相同的链接、内联。本机用一个手写的 5 行文本 IR 验证过；不传 `extern_libs` 时，链接不报错，要到最后一步才报 `Unresolved extern function`。（来源：`msg-8dce86aba8c15ba7972b`。）

- [要点] 新后端编译成功，机器码里却仍有对库函数的真实调用，最可能漏了什么？——学习者答：“最可能是漏了内联优化的标志。可能通过查看O3优化前后的LLVM IR进行对比”，正确。补充一个更省事的顺序：先看链接之后的 IR，有 `define` 但没有 `alwaysinline` 是内联的问题；仍然只有 `declare` 则是库根本没链接进来，只是后端最后一步没有为此报错。（来源：`msg-0cb671c61108393bea26`、`msg-115c0150ef294e79ebc5`。）

- [要点] 给一个新后端加 libdevice 支持，要补哪六样东西？——一是 `get_module_map()`，把接口模块映射到自己的实现模块；二是实现模块里的各个函数；三是每个函数的“dtype → 符号”表；四是库文件和默认路径，内容哈希计入缓存键；五是生成 LLVM IR 阶段的按需链接，表里的符号名要和库里的定义一致；六是让库函数被内联，并把次正规数等数值开关传给库。逐元素拆成标量调用、按名字链接这些机制是 Triton 的公共代码，不用重写。（来源：`msg-8dce86aba8c15ba7972b`。）

- [要点] NVIDIA 和 AMD 决定“链接哪些库”的规则有什么不同？——NVIDIA 只要发现未定义的外部函数，就把 `extern_libs` 里的库都交给链接器。AMD 只链接“键名出现在某个未定义函数名里”的库。本机实测同一个自定义库：键名不匹配时，AMD 编译不报错，但最终 IR 里留着一次未解析的调用。（来源：`msg-8dce86aba8c15ba7972b`。）

- [要点] 同一个 `libdevice.asin` kernel 换到 AMD，哪些内容变了？——符号变成 `__ocml_asin_f32`；每个 warp 是 64 个线程，所以 `BLOCK_SIZE=1024`、`num_warps=4` 时每线程 4 个元素；默认库是 `ocml.bc` 和 `ockl.bc`，这里只链接用到的 `ocml.bc`；次正规数默认保留，由 kernel 函数上的属性控制。逐元素调用、按名字链接、内联这些机制是 Triton 的公共代码，没有变。（来源：`msg-8dce86aba8c15ba7972b`。）

## 综合验收与复查

- [纠错] 场景：综合验收的口述题，条件是输入为 fp16、调用 `libdevice.erf`、目标后端是 AMD。我说“第三，再将TTGIR交由LLVM进行处理，成为LLVM IR。LLVM的处理过程基本分为三步：1、转换，从TTGIR的张量描述方式，转为线程描述方式”，并且全篇没有提 fp16 怎么处理 → 正确：TTGIR 到 LLVM IR 的转换是 Triton 自己做的，LLVM 接手的是之后的链接、O3 和生成汇编；fp16 必须先在 kernel 里 `.to(tl.float32)`，否则在查表处报 `KeyError`；AMD 上符号是 `__ocml_erf_f32`，每个 warp 64 个线程，链接的是 `ocml.bc`。原因：全链路的顺序和“链接加内联所以没有调用”都答对了，但题目给的条件要落到每一环的具体内容上。（来源：`msg-09c3d4a1f584f9d3a1ac`、`msg-56b08ac9654bfcb511c9`。）

- [要点] 要让 `y = x / (1 + tl.exp(-x))` 更接近 PyTorch eager，两处各改成什么，代价是什么？——学习者答：“tl.exp需要换成libdevice.exp，除法'/'需要换成tl.div_rn；exp速度上会变成8条指令，而原本只有2条。除法'/'则不清楚。没有要求与pytorch eager结果尽量一致时，会采用快速版。”改写和取舍都对，也如实说明了不知道除法的代价：`div.rn` 比 `div.full` 慢，Inductor 源码只说“会带来性能损失”，没有实测数字。（来源：`msg-09c3d4a1f584f9d3a1ac`、`msg-56b08ac9654bfcb511c9`。）

- [纠错] 场景：综合验收的诊断题，同一个 kernel 对输入 1e-40，NVIDIA 输出 0，AMD 输出约 1e-40。我说“想要两边保持一致，可以调整enable_reflect_ftz的参数……可能会影响所有有可能有次正规数的计算” → 正确：这只说了 NVIDIA 一侧。AMD 不用 reflect，靠 kernel 函数上的属性 `denormal-fp-math-f32` 控制，对应选项 `allow_flush_denorm` 默认是 False，所以两边默认值相反；可以 NVIDIA 传 `enable_reflect_ftz=False`，或 AMD 传 `allow_flush_denorm=True`。`enable_reflect_ftz` 只影响这个 kernel 里 libdevice 函数内部的代码。原因：两个后端控制次正规数的机制不同，Triton 自己生成的指令也不受反射参数影响。（来源：`msg-09c3d4a1f584f9d3a1ac`、`msg-56b08ac9654bfcb511c9`。）

- [要点] `libdevice.pow(x, y)` 中 `x` 是 bf16、`y` 是 fp32，会怎样，怎么改？——学习者答：“直接写会出现KeyError。因为输入的数据类型bf16不支持。需要先进行x.to(tl.float32)，然后再进行pow计算”，正确。有多个参数时，表的键是所有参数 dtype 组成的元组；真实报错是 `KeyError: (triton.language.bfloat16, triton.language.float32)`，改后选中 `__nv_powf`。（来源：`msg-9e34e05dfcdd67e38a0b`、`msg-2cc3cbd98a5a10a8ef21`。）

- [转折] 助手更正了自己一道复查题的前提。——题目假设“在 AMD 上传 `enable_reflect_ftz=True` 后极小数仍然没有变成 0”。核实后发现，AMD 的选项里没有这个字段，真实启动 kernel 会直接报 `Keyword argument enable_reflect_ftz was specified but unrecognised`；只有 `triton.compile(..., options=...)` 这个只编译的入口才会静默丢掉不认识的选项。学习者“要用 `allow_flush_denorm`”的回答不受影响。（来源：`msg-9e34e05dfcdd67e38a0b`、`msg-2cc3cbd98a5a10a8ef21`。）

## 练习：实现、Review 与变式

- [高价值问题] “对于bundled_libdevice_path，我不知道该设置哪个路径。”——当时学习者照教程写了 `is_cuda` 的分支，并用到需要 GPU 驱动的 `triton.runtime.driver.active`。助手给了分解：运行时找出已安装的 `triton` 包目录，再拼上固定的相对位置 `backends/nvidia/lib/libdevice.10.bc`，并指出 Triton 自己算默认路径的出处；没有给代码。因为透露了分解，这一小块的独立证据后来由变式里无提示写出的 `bundled_ocml_path` 补回。（来源：`msg-81e8322d75a2a20cafc8`、`msg-583e1927c23a527a752a`、`msg-2a79fc11fe1eb8b2a6b8`。）

- [纠错] 场景：首次提交的包装函数 `asin`。我写了 `asin_kernel[grid](x, x, n, BLOCK_SIZE, extern_libs=extern_libs)`，函数也没有 `return` → 正确：新建一个 `torch.empty_like(x)` 作为输出指针传给 kernel，再把它返回。原因：把输入同时当输出，会原地覆盖调用者的数据；约定要求返回新张量且不修改输入。这一条只有 GPU 测试能测到，本机是读代码发现的。（来源：`msg-7cf7d22551cb183e8928`、`msg-764ca404f40a104ee030`。）

- [纠错] 场景：首次提交时我说“我写好了asin_kernel和asin”，kernel 里直接写 `res = libdevice.asin(x_data)` → 正确：fp16、bf16 指针下编译失败，报 `KeyError: (triton.language.float16)`；要在 kernel 内部按类型升到 fp32，同时让 fp64 仍然走 `__nv_asin`。原因：`asin` 的表里只有 fp32 和 fp64；这个报错在节点 2 和复查题里都处理过，写 kernel 时没有用上。（来源：`msg-81e8322d75a2a20cafc8`、`msg-7cf7d22551cb183e8928`。）

- [纠错] 场景：第二次提交，为了按类型分支，我给 kernel 加了 `is_bf16: tl.constexpr, is_fp16: tl.constexpr` 两个参数，由包装函数传入 → 正确：kernel 保持约定的 4 个参数，用加载结果自身的 `dtype` 做编译期分支。原因：指针类型已经包含元素类型，额外的标志是重复信息，可能互相矛盾。实测 fp32 指针配 `is_fp16=True` 能通过编译，结果先被截成 fp16 再转回 fp32，精度被悄悄丢掉。分派逻辑本身是对的，差的只是接口；改用 `x_data.dtype` 是学习者只被告知“分支依据要由 kernel 自己得到”后独立找到的。（来源：`msg-764ca404f40a104ee030`、`msg-f6c7085fc583e44469b6`。）

- [纠错] 场景：第三次提交，在 `x_data = x_data.to(tl.float32)` 之后，我又写了 `if x_data.dtype == tl.bfloat16: res = res.to(tl.bfloat16)` 和对应的 fp16 分支，想把结果转回半精度 → 正确：这些分支永远不会执行，可以删掉。原因：判断的是变量当前绑定的值，`x_data` 此时已经是 fp32。结果仍然正确，是因为 `tl.store` 写入时会自动转成指针的元素类型；编译产物里那条 fp32 转 fp16 的指令，源码位置正是 `tl.store` 那一行。（来源：`msg-f6c7085fc583e44469b6`。）

- [高价值问题] “我先前尝试先用is_bf16 = x.dtype == tl.bfloat16保存判断结果，然后再if is_bf16进行判断。但会发生编译报错。这是为什么？”——普通赋值会把 Python 布尔值转成张量，`if` 因而成了运行期分支：两个分支都要编译，同一个变量在两条路径上类型必须一致，于是报 `initial value for x is of type bf16…, but the then block redefines it as fp32…`。直接写 `if x.dtype == …` 走的是编译期分支，只编译选中的一支。想先存再用，可以写 `is_bf16: tl.constexpr = x.dtype == tl.bfloat16`；这和 C++ 里 `if constexpr` 与普通 `if` 的区别是一回事。（来源：`msg-35273bf51f4941c39321`、`msg-000b5e86960628a310fe`。）

- [要点] 只编译的测试凭什么能证明“升精度发生在 kernel 内”和“函数被内联了”？——学习者的解释：测试“直接对kernel算子进行了编译，而不通过wrapper包装函数调用kernel”，半精度输入下选中的是只接受 fp32 的 `__nv_asinf`，“所以半精度的输入在执行指令计算前一定有进行升精度”；PTX 里匹配不到 `call`，所以函数被内联了。推理成立。措辞上，`__nv_asinf` 是函数的符号，不是指令，内联之后才变成一串指令。（来源：`msg-35273bf51f4941c39321`、`msg-000b5e86960628a310fe`。）

- [要点] 包装函数按元素个数让 `BLOCK_SIZE` 取 256、512、1024，有什么后果？——它是 `constexpr`，每取一个值，Triton 都要单独编译一份 kernel，同一种 dtype 最多编译三次。这符合约定，只是一个需要知道的代价。（来源：`msg-7cf7d22551cb183e8928`。）

- [转折] 变式在无提示下完成。——主体本机通过后，学习者独立写出 `atan2_kernel` 和 `bundled_ocml_path`：三个指针同类型，前三种选中 `__nv_atan2f`，fp64 选中 `__nv_atan2`，`libdevice.atan2(y_data, x_data)` 的参数顺序正确；AMD 数学库的路径是自己在安装目录里找到的。本机 16 条测试全部通过。（来源：`msg-09f5cfa4826aff3a1d25`、`msg-2a79fc11fe1eb8b2a6b8`。）

## GPU 验收、观察与结课前答疑

- [转折] GPU 证据来自哪里？——学习者在另一台机器的容器里运行全部测试并贴回输出：`60 passed`，设备是 RTX 4070 Ti，PyTorch 2.13.0+cu130，Triton 3.7.1。需要 GPU 的 44 条测试此前只用 CPU 替身检查过判定逻辑，这是第一次在真实设备上运行，没有暴露测试本身的问题。（来源：`msg-8b9956fc31638fcf1008`、`msg-6d10fd7515a4b2180132`。）

- [要点] 默认设置和关闭 ftz 时，`asin(1e-40)` 各输出什么？——学习者事先预测：“默认设置下，asin(1e-40)输出成0；enable_reflect_ftz=False下，输出非0.”实测一致：默认输出 0，负输入得到 -0；关闭后输出 1e-40，与 `torch.asin` 相同。分界点在最小的正规数 1.175e-38，从它开始三者结果相同。差值只有 1e-40 量级，带绝对容差的常规数值测试发现不了。这只是一台设备上 `asin` 对几个输入的观察。（来源：`msg-8b9956fc31638fcf1008`、`msg-6d10fd7515a4b2180132`。）

- [高价值问题] “nv平台上asinf函数内联后变成每元素 1 条 sqrt、6 条 fma的指令；而amd平台上会变成每元素 1 条 sqrt、9 条 fma／mad的指令。为什么会不一样？amd平台上指令为什么需要更多？”——两个后端用的是两家各自写的库，算法写法不同，AMD 并没有做更多的工作。AMD 多出的 3 条 fma：一条把 (1 − |x|) ÷ 2 合成一步，NVIDIA 用的是减法加乘法；一条来自多一项的多项式，6 个系数对 5 个，换算的分界点也不同，分别是 0.5 和 0.57；一条来自两个分支的最后一步各算一遍，NVIDIA 是先选好变量再共用一条。算上全部算术指令，NVIDIA 约 19 条，AMD 约 17 条。图解页原来只列 fma 条数，容易误解，已据此更正。（来源：`msg-b5f0279094d987752fab`、`msg-e29ea408fd896a138575`。）

## 遗留

- [遗留] 快速档与精确档（exp、除法、sqrt）的实际速度差和误差没有实测；学习者在综合验收里也说明不清楚除法的代价。（去向：[Lesson 的非阻塞余项](../lessons/07-extern-functions.md#final-mastery)，需要时作为 optional extension 另行授权。来源：`msg-09c3d4a1f584f9d3a1ac`、`msg-6d10fd7515a4b2180132`。）
- [遗留] AMD 后端只有只编译的观察，没有在真实设备上运行；这次 GPU 运行没有记录驱动版本；两家 `asin` 实现的精度目标没有查到文档，“AMD 的写法更看重精度”只是从代码推断。这些不作为稳定结论直接制卡。（去向：同上。来源：`msg-6d10fd7515a4b2180132`、`msg-e29ea408fd896a138575`。）
