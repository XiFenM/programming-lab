# 第 10 课：块缩放矩阵乘——低精度格式、scale 布局与硬件落地

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-10-block-scaled-matmul` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 解释块缩放（microscaling）低精度矩阵乘的整套设计：MXFP8、MXFP4、NVFP4 的数值格式与量化规则，`tl.dot_scaled` 的数据表示与 scale 预排布局，同一份源码在 sm_100、sm_120 与没有原生支持的架构上分别落成什么、付出什么；并实现、验证和度量一个块缩放矩阵乘 kernel |
| 阶段 | `complete`（2026-10-20 结课） |
| 启动授权 | 2026-10-14，学习者提出“很好，接下来我们开始第十课吧。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/10-block-scaled-matmul.py` | `teaching-spine` | 仓库 commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；本地 SHA-256 `742a9a71e4ea1a2a0bfe4621906870b74ea01fec325b9f67451d9ce938aa3e35`。与 v3.7.1 tag 的 `python/tutorials/10-block-scaled-matmul.py` 相比只有两处不同：cuBLAS 基线的 scale 在 mxfp4、mixed 下补了 `None` 分支（第 432–434 行），proton 的 `activate`／`deactivate` 不带参数（4 处）；kernel 与数据准备逐字相同（2026-10-14 以 `diff` 核对） | 教学顺序与示例：NVIDIA 与 AMD 两段背景、`block_scaled_matmul_kernel` 及其主机侧数据准备与参考计算、CDNA4 kernel 与 scale 预排、基线与 benchmark |
| [Triton v3.7.1](https://github.com/triton-lang/triton/tree/v3.7.1) | `implementation-authority` | tag `v3.7.1`，commit `f797708c0626e5f9840ca5b0a98790e2c7cb09ad`，与 `uv.lock` 一致 | `python/triton/language/core.py` 第 2100–2138 行与 `semantic.py` 第 1589–1672 行的 `dot_scaled` 接口与形状检查；`semantic.py` 第 1950 行描述符块最后一维至少 16 字节；`lib/Dialect/TritonGPU/Transforms/AccelerateMatmul.cpp` 中 sm_120 的 `ScaledBlockedToMMA`、sm_100 的 `ScaledBlockedToMMAv5` 与模式注册；`DecomposeScaledBlocked.cpp` 的软件换算；`third_party/nvidia/lib/TritonNVIDIAGPUToLLVM/DotOpToLLVM/MMAv2.cpp` 的 sm_120 指令表；`third_party/nvidia/backend/compiler.py` 在 sm_90 以下把描述符改写为指针；`python/triton/tools/{mxfp.py,tensor_descriptor.py}`。另用于节点 1、5：`core.py` 第 2037–2061 行（`tl.dot` 对 fp32 输入默认用 TF32，并提醒可能截断而不舍入）；`third_party/amd/backend/compiler.py` 第 45–49、129–141 行（CDNA3 原生支持 FNUZ 的 FP8，CDNA4 起原生支持 OCP 的 FP8；TF32 只对 gfx942 开放）；`third_party/amd/lib/TritonAMDGPUTransforms/AccelerateAMDMatmul.cpp` 第 1817–1838 行的模式注册（CDNA4 用第 1048 行起的 `ScaledBlockedToScaledMFMAF8F6F4`，FP6 尚未支持；CDNA3 用第 774 行起的 `ScaledBlockedToMFMA`，按第 269 行的注释以 bf16／fp16 模拟）。另用于节点 3、4：`lib/Dialect/TritonGPU/Transforms/OptimizeDotOperands.cpp` 第 183–318 行的 `UseShmemForScales`（认出 scale 的 reshape／trans 写法后改写为共享内存视图与 `tmem_copy`）；`third_party/nvidia/lib/TritonNVIDIAGPUToLLVM/DotOpToLLVM/MMAv5.cpp` 第 273–277、596–607、628、673–674 行（块缩放指令的 K 与 scale 字节的选择）；`third_party/nvidia/backend/driver.c` 第 401 行起的 `fillTMADescriptorTiled`（启动时调用 `cuTensorMapEncodeTiled`，失败则报错）。另用于节点 5：`AccelerateMatmul.cpp` 第 657–700 行（sm_120 的 `ScaledBlockedToMMA` 要求两侧都有 scale，不接受 FP8 与 FP4 混合）与第 1010–1013 行（NVIDIA 总会登记通用的软件换算）；`DecomposeScaledBlocked.cpp` 第 62–93 行（E8M0 零扩展后左移进 bf16 的指数位）与第 191–212 行（解码、逐元素乘 scale、NaN 处理）；`AccelerateAMDMatmul.cpp` 第 774–805 行（CDNA3 的模拟路径遇到两侧都有 scale 时不处理）；`third_party/amd/lib/TritonAMDGPUToLLVM/DotOpToLLVM/MFMA.cpp` 第 44–58 行（cbsz、blgp 的格式编码）与第 671–676 行（4 个 scale 装进一个 32 位值，op_sel 选字节）。另用于综合验收的复查：`third_party/amd/lib/TritonAMDGPUToLLVM/TargetInfo.cpp` 第 87–96 行（LDS 上限：CDNA3 为 64 KB，CDNA4 为 160 KB）；`python/triton/compiler/compiler.py` 第 456–459 行（加载 kernel 时共享内存超过设备上限即报 `OutOfResources`）；`third_party/amd/lib/TritonAMDGPUTransforms/AccelerateAMDMatmul.cpp` 第 119–141 行（`warpsPerTile` 的常规启发式，128 × 128、8 个 wave 得 [2, 4]）、第 853–859 行（CDNA3 的 `ScaledBlockedToMFMA` 把 wave 全排在带 scale 那个操作数的非 K 方向，注释的理由是让 scale 与它所管的元素留在同一个 wave）、第 947 行起的 `DecomposeAMDScaledBlocked` 与第 1829 行的 CDNA4 注册（拆成解码加普通矩阵乘，排法随常规启发式）。另用于练习 P1：`python/triton/tools/mxfp.py` 的 `MXFP4Tensor`（E2M1 的编码、打包与解包，作为验收测试的对照；`_from_float` 以固定的 1e-6 打破平局，离中点约 1e-6 以内的值也被取偶）；`python/triton/runtime/interpreter.py` 的解释器没有 `create_dot_scaled`。另用于练习期间的答疑：`core.py` 第 2116–2125 行（FP4 两个元素拼一个 uint8、首个元素在低位；scale 以 uint8 表示 E8M0，`rhs_scale` 不转置）；`python/triton/_utils.py` 第 76–111 行的 dtype 映射没有 `float8_e8m0fnu`（以 `triton.runtime.jit.mangle_type` 实测报 `KeyError`）；`DecomposeScaledBlocked.cpp` 第 137–174 行的 `maskNan`（scale 为 0xFF 时置 NaN；左移写法下字节 0 得 0.0）；`python/triton_kernels/triton_kernels/numerics_details/mxfp.py` 第 18–26 行（`DequantScaleRoundingMode`，默认 `ROUND_UP`，注释称 OCP 的向下取约有一半机会截断块最大值；SHA-256 `a2981a904a95725e8c10254ec517f27937ddde4501467e71847188e71fe47989`）与 `mxfp_details/_downcast_to_mxfp.py` 第 45–58 行（两种取法的位运算；SHA-256 `0585f99ac7ecec78f726debd2e924aa99c137fe7bcbd677007ccca2943afce6c`），均取回于 2026-10-19。另用于 M1：`python/triton/testing.py` 的 `do_bench` 与 `third_party/nvidia/backend/driver.py` 第 370–375 行（每次运行前清空 256 MB 缓冲以冲掉 L2） |
| [vLLM `qutlass_utils.to_blocked`](https://docs.vllm.ai/en/v0.23.0/api/vllm/model_executor/layers/quantization/qutlass_utils/) | `explanatory-support`（真实系统锚点） | vLLM v0.23.0 文档，取回于 2026-10-17 | 节点 4 答疑：把 scale 补到行数是 128 的倍数、列数是 4 的倍数，按 128 × 4 切块后排成 (r, g, c)，最后展平成一维返回；字节顺序与教程的五维排法相同，形状只是标签 |
| [OCP Microscaling Formats (MX) v1.0](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf) | `method-authority` | Version 1.0，2023-09；PDF SHA-256 `d195d6a36dd4a0c89064af0c479bcaad5c0fe29d63f628502ea6d7c4b4279421`，取回于 2026-10-14 | §5.1 MX 的三要素（scale X、元素 P_i、块大小 k；每块 w + k·d 位，第 9 页）；§5.2 具体格式表；§5.3 元素类型（第 10–13 页：编码公式，FP8 转换的 SAT 与 OVF 两种方式，FP6、FP4 的编码表与饱和、下溢规则）；§5.4 E8M0；§6.1–6.2 点积语义；§6.3 由一组标量求 scale 与元素的规则。练习期间的答疑另用：§5.4.1 表 7（第 14 页：bias 127，指数范围 −127 到 127，NaN 为 `11111111`，没有 Inf 与 0）；§5.1（第 9 页：scale 为 NaN 时整块为 NaN）；§5.3.3（第 12 页：FP4 没有 Inf 与 NaN 编码）；§6.3（第 15 页：向下取 2 的幂，允许其他算法） |
| [PTX ISA 9.4](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html) | `interface-authority` | 版本 9.4；副本保存于 2026-10-06（第 08 课） | §9.7.16.3 `mma.sync` 的块缩放（Table 44、45，scale 选择器）；§9.7.18.9.2 `tcgen05.cp`；§9.7.18.10.7 `tcgen05.mma` 的块缩放（Table 68、69，Figure 237：scale A 在 TMEM 中的布局）；§9.7.18.8.1 每个 warp 只能访问 TMEM 中自己的 32 个 lane；§9.7.18.6.2 哪些 tcgen05 指令对按发出顺序访问 TMEM（不同 warp 发出的指令之间不保证顺序） |
| [CUDA Driver API：Tensor Map Object Management](https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__TENSOR__MEMORY.html) | `interface-authority` | 在线文档，取回于 2026-10-16，2026-10-17 复核 | `cuTensorMapEncodeTiled` 的约束：起点 16 字节对齐；整个张量每维不超过 2^32，行距是 16 的倍数且小于 2^40；一次搬运的块（boxDim）每维不超过 256，不交错时最内维的字节数须是 16 的倍数 |
| [Introducing NVFP4 for Efficient and Accurate Low-Precision Inference](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) | `explanatory-support` | NVIDIA 技术博客，2025-06-24 | NVFP4 的定义：E2M1 元素、16 个一块、E4M3 块 scale、每张量一个 FP32 scale、每值 4.5 bit；E8M0 把 scale 取成 2 的幂，可能给块最大值带来较大误差 |
| [Pretraining Large Language Models with NVFP4](https://arxiv.org/abs/2509.25149) | `method-authority` | arXiv:2509.25149v1（NVIDIA，2025-09-29）；PDF SHA-256 `d3bf773be5fc6266763f2bcad3f1435e82f960fd522a941682ffcee5215b5a56`，取回于 2026-10-15 | §1：MXFP4 与 NVFP4 的对比（块从 32 缩到 16，E4M3 scale，FP32 每张量 scale；2 的幂 scale 可能损失近一档和 ±4、±6 两个格点）；附录 B.1–B.3：两级 scale 的取法（s_enc = 6·448 / amax_x，块的 decode scale = amax_b / 6，乘 s_enc 后按就近取偶存成 E4M3），张量核把块 scale 乘在每块的部分点积上、每张量 scale 乘在最终输出上；B.4：MXFP8 训练中饱和导致收敛问题，因而把 2 的幂 scale 向上取 |
| [gpt-oss-120b & gpt-oss-20b Model Card](https://arxiv.org/abs/2508.10925) | `explanatory-support`（真实系统锚点） | arXiv:2508.10925v1（OpenAI，2025-08-05）；PDF SHA-256 `8839e1efdf835be08ad1d60bfa99c8c4fdde15c7ef49eda6a8b910575fb699a0`，取回于 2026-10-15 | Table 1：120b 共 116.83B 参数，其中 MLP 114.71B、注意力 0.96B、嵌入与反嵌入 1.16B，checkpoint 60.8 GiB；§2.1：MoE 权重量化为 MXFP4，每参数 4.25 bit，占总参数 90% 以上，使 120b 能放进单张 80 GB GPU |
| [DeepSeek-V3 技术报告](https://arxiv.org/abs/2412.19437v2) | `explanatory-support`（真实系统锚点） | arXiv:2412.19437v2 | §3.3.2 激活按 1×128、权重按 128×128 分组的 FP8 量化，每 128 个元素提升到 CUDA core 上累加（H800 的 FP8 累加只保留约 14 位）；同节的 Mantissa over Exponents（全部张量用 E4M3，归功于细粒度 scale 让一组元素共享指数位）与 Low-Precision Activation（需要重新分组的激活，scale 取 2 的整数次幂）；§3.5.2 建议张量核直接接收 scale；§4.2 的模型超参数（61 层，前三层之外的 FFN 都换成 MoE；每层 1 个共享专家与 256 个路由专家，每个专家的中间维 2048，每个 token 激活 8 个），用于综合验收的复查 |
| [FP8 Formats for Deep Learning](https://arxiv.org/abs/2209.05433) | `method-authority` | arXiv:2209.05433v2；PDF SHA-256 `809a9557e907765b452c5a1b7308a92e31dd31a07e668d49d14b1594b6c0cf0c`，取回于 2026-10-15 | §2：先乘 scale 再转 FP8，按张量最大值选 scale，溢出饱和，在转换之后或线性运算输出之后除回 scale；§3 Table 1：E4M3 与 E5M2 的编码与用途；§3.1：E4M3 收回特殊值的编码，最大值从 240 到 448 |
| [Mixed Precision Training](https://arxiv.org/abs/1710.03740) | `method-authority` | arXiv:1710.03740v3（ICLR 2018）；PDF SHA-256 `3bbff2f757abdcfe4c5a4cee338f7b7d888110b9013ec4a934e334016f527c78`，取回于 2026-10-15 | §3.1 FP32 主权重；§3.2 loss scaling：幅度低于 2⁻²⁴ 的值在 FP16 中变 0，Multibox SSD 不做 loss scaling 时发散，乘 8 即可恢复（§4.2 Table 2） |
| [BFloat16 介绍](https://cloud.google.com/blog/products/ai-machine-learning/bfloat16-the-secret-to-high-performance-on-cloud-tpus)、[A100 上的 TF32](https://developer.nvidia.com/blog/accelerating-tensorflow-on-a100-gpus/) | `explanatory-support` | Google Cloud 博客 2019-08-23；NVIDIA 开发者博客 2020-07-24 | BF16 为 1 位符号、8 位指数、7 位尾数，范围与 FP32 相同，训练无需 loss scaling，乘法器面积随尾数位宽的平方增长；TF32 是张量核的计算模式：FP32 输入，内部按 TF32 相乘，FP32 累加 |
| [ROCm：Precision support](https://rocm.docs.amd.com/en/latest/reference/precision-support.html) | `interface-authority` | 页面未标版本，取回于 2026-10-15 | CDNA3（MI300A、MI300X、MI325X）原生 FP8 为 FNUZ 变体；CDNA4（MI350X、MI355X）支持 OCP FP8，以及 FP6、FP4 |
| [AMD Instinct MI300X](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)、[AMD 新闻稿](https://www.amd.com/en/newsroom/press-releases/2023-12-6-amd-delivers-leadership-portfolio-of-data-center-a.html)、[ROCm：MI300 微架构](https://rocm.docs.amd.com/en/docs-7.0.1/conceptual/gpu-arch/mi300.html) | `interface-authority` | 产品页、2023-12-06 新闻稿与 ROCm 7.0.1 文档，取回于 2026-10-17 | 综合验收：bf16 矩阵峰值 1307.4 TFLOPS（2,100 MHz，稠密；稀疏为 2614.9）、向量 FP32 163.4 TFLOPS、向量 FP64 81.7 TFLOPS、304 个 CU、192 GB HBM3、理论峰值带宽 5.3 TB/s |
| [AMD Matrix Instruction Calculator](https://github.com/ROCm/amd_matrix_instruction_calculator) | `interface-authority` | `matrix_calculator.py` 版本 1.3.2，SHA-256 `53b027855ca44120401eeff69f41961821d1a393b163e112f7aa4d2a313e185d`，取回于 2026-10-18；只读取数据表，未运行 | 综合验收的复查与答疑：CDNA3 的 `v_mfma_f32_16x16x16_bf16` 执行 16 个周期，可与向量指令同时执行，发出 4 个周期后才能同时发射（每条留出 12 个周期）；`v_mfma_f32_32x32x8_bf16` 为 32 个周期，同为 4 个周期；第 5242 行把每条指令的运算数记为 2 × M × N × K（每 CU 每周期 2048 FLOPs，乘 304 个 CU 与 2.1 GHz 即 1307.4 TFLOPS） |
| [NVIDIA Ampere 架构白皮书](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf) | `explanatory-support` | PDF SHA-256 `3a800ad7668ec37037fa5870a8e3bb681b75f19668b3d11492ab9b0da0d58815`，取回于 2026-10-18 | 综合验收答疑（规格表的 TFLOPS 口径）：A100 每个 SM 每周期 1024 次稠密 FP16 FMA，“or 2048 individual FP16 floating point operations per clock”，108 个 SM 合计 312 TFLOPS；Table 1 的稀疏一栏注为 “Effective TFLOPS / TOPS using the new Sparsity feature” |
| [vLLM `normalize_e4m3fn_to_e4m3fnuz`](https://github.com/vllm-project/vllm/blob/8530aed2b78a19eb00e242031c22bb78d615eea2/vllm/model_executor/layers/quantization/utils/w8a8_utils.py#L109-L130) | `explanatory-support`（真实系统锚点） | commit `8530aed2b78a19eb00e242031c22bb78d615eea2`（main，2026-10-15） | 把 OCP 的 E4M3 权重转成 MI300 的 FNUZ：`0x80` 置 0，按 FNUZ 重新解读，权重与输入的 scale 乘 2 |
| [gpt-oss-120b 模型卡](https://huggingface.co/openai/gpt-oss-120b)、[vLLM 博客](https://vllm.ai/blog/2025-08-05-gpt-oss) | `explanatory-support`（真实系统锚点） | 取回于 2026-10-14；博客 2025-08-05 | MoE 权重以 MXFP4 存储，117B 参数的模型可放进单张 80 GB GPU；Blackwell 用原生 MXFP4 张量核，Hopper 用 Triton 的 `matmul_ogs`，FP4 在乘法 kernel 内即时解包 |
| [NVIDIA RTX Blackwell GPU Architecture](https://images.nvidia.com/aem-dam/Solutions/geforce/blackwell/nvidia-rtx-blackwell-gpu-architecture.pdf) | `interface-authority` | 白皮书 PDF，SHA-256 `906ff2a409d7a7e4cbc56f5d3a179d574120d19aaba99520670e1a0c064595fa`，取回于 2026-10-19 | M1 的规格：附录 A 表 3（第 46–48 页）的 GeForce RTX 5090：170 个 SM、21,760 个 CUDA core、680 个第 5 代 Tensor Core，Boost 2407 MHz；非张量 FP32 104.8 TFLOPS；FP4 张量（FP32 累加）1676，FP8 张量 FP16 累加 838、FP32 累加 419，FP16／BF16 张量 FP32 累加 209.5（稠密，斜杠后的数为稀疏）；32 GB GDDR7、512 位、28 Gbps、1792 GB/s；L2 98,304 KB；L1／共享内存 21,760 KB；寄存器堆 43,520 KB；表注：峰值按 Boost 频率计 |
| [microsoft/microxcaling `mx/mx_ops.py`](https://github.com/microsoft/microxcaling/blob/7bc41952de394f5cc5e782baf132e7c7542eb4e4/mx/mx_ops.py) | `explanatory-support`（真实系统锚点） | commit `7bc41952de394f5cc5e782baf132e7c7542eb4e4`（main，2024-08-19）；SHA-256 `e8ebe1baee065663d4f5cb6df81d96056054964a85711ae2e1db40c4b4b8533a`，取回于 2026-10-19 | 练习答疑：第 279–283 行先减去元素格式的 emax，再把低于 −127 的指数截到 −127、高于 127 的置为 NaN；第 75–80 行以 floor(log2) 取块最大值的指数 |
| [Recipes for Pre-training LLMs with MXFP8](https://arxiv.org/abs/2506.08027) | `method-authority` | arXiv:2506.08027v2（Mishra、Stosic、Layton、Micikevicius，NVIDIA，2025-08-18 修订）；HTML SHA-256 `833093b375778d56e425f9f8ee2b04b335f33f075bd7c0893e0dfc7397e61c1c`，取回于 2026-10-19 | 练习答疑：§3.3 的 Algorithm 1 把 scale 向正无穷取整，指出 OCP 的向下取会让缩放后的值超出可表示范围、引入更多量化噪声，并推测这是图 5 中按 OCP 取法训练出问题的原因；同节说明设备上的 log2 返回值就近舍入，因而直接操作位表示 |
| PyTorch 2.13.0（`torch==2.13.0+cu130`，与 `uv.lock` 一致） | `implementation-authority` | 本机临时环境中的安装 | 练习答疑：`torch/include/torch/headeronly/util/Float8_e8m0fnu.h` 的文件头注释（即 OCP §5.4.1 的 E8M0）与第 61–112 行（float32 转 E8M0 按就近取偶，对正规数平局向上）；`torch/_meta_registrations.py` 第 7008–7017 行（`torch._scaled_mm` 以 scale 的 dtype 判断块缩放：`float8_e8m0fnu` 或 `float8_e4m3fn`）；`torch.round` 平局取偶 |

### 目标与所需证据

| ID | 可观察目标 | 理解 | 实践 | 实证 |
| --- | --- | --- | --- | --- |
| O1 | 从统一的浮点模型讲起（符号、带偏置的指数、尾数与隐含位、次正规数、特殊值），说明 FP64、FP32、TF32、FP16、BF16 各自的取舍，以及降到 FP8（E4M3、E5M2，含 AMD MI300 的 FNUZ 变体）、FP6、FP4 时每少一位丢掉什么；解释块缩放格式的数值设计：为什么沿 K 每 V 个元素共享一个 scale；MXFP8、MXFP4、NVFP4 的元素类型、块大小与 scale 类型（E8M0 的 2 的幂，UE4M3 加每张量 FP32）的取舍；OCP 的量化规则在什么情况下让元素饱和、在什么情况下把小值变成 0；能为给定数据选择格式并说出代价 | 需要 | 需要 | 不需要 |
| O2 | 说明 scale 在矩阵乘里可以放在哪一步（乘之前逐元素换算、每组部分和之后、MMA 指令内部），为什么这取决于 scale 沿哪个下标变化，各自代价在哪里；讲清教程 kernel 的数据流与 scale 布局：`tl.dot_scaled` 的形状语义、FP4 两个元素拼一个字节与按字节推进的偏移、scale 从逻辑 `[M, K/V]` 到 5D 预排布局的对应，以及这种布局为什么让每个 K 步的 scale 读取连续、为什么 kernel 里的 reshape 与 trans 不搬数据；能对没讲过的块形状推出 `rep_m`、`rep_k` 与描述符的块形状 | 需要 | 需要 | 不需要 |
| O3 | 说明同一个 `tl.dot_scaled` 在 sm_100（`tcgen05.mma` 块缩放，scale 与累加器在 TMEM）、sm_120（`mma.sync` 块缩放，累加器在寄存器）、没有原生支持的 NVIDIA 架构（转成 bf16 再乘 scale），以及 AMD 的 CDNA3（没有块缩放指令，以 bf16／fp16 模拟）与 CDNA4（scaled MFMA，只支持 OCP 的 MX 格式）上分别落成什么，scale 各放在哪里、代价落在哪里，用编译产物验证；判断教程配置搬到 RTX 5090 要改什么；对“原生块缩放比软件换算快多少”先作可证伪的预测，再用一次受控测量解释 | 需要 | 不需要 | 需要 |

O3 的实证只要求在学习者能用的 RTX 5090 上做一次受控测量，并以本机的编译产物对照；sm_100 的实机运行、与 cuBLAS 的对比和 autotune
调参不属于完成门槛，学习者能借到 sm_100 设备时可另行约定为观察。练习的具体内容在综合验收之后按仍缺的证据约定。

**路线调整（2026-10-15）**：学习者看完开课导入后提出三点，要求不直接回答、并入后续节点：“scale用在了矩阵乘的哪些操作上？……所以说scale该用在哪？”；
格式节点“从经典的浮点表示开始（比如fp32，fp64，fp16，bf16，tf32），逐步引出到低位数的格式”；“硬件落地中，可以再添加与amd的硬件的对照”。据此路线改为
五个节点：1 浮点表示，从 FP64 到 FP4（新增）；2 块缩放格式与量化规则；3 scale 用在哪一步，以及 `tl.dot_scaled` 与 kernel 的数据表示；4 scale 预排布局；
5 硬件落地，含 AMD CDNA3 与 CDNA4 的对照。O1–O3 的描述相应补充，所需证据类型不变。

**设备**：学习者可用 RTX 5090（capability 12.0，每个 CTA 的共享内存上限 101,376 字节，见[第 09 课设备读数](09-persistent-matmul.md#目标与所需证据)）与
RTX 4090／4070 系列（8.9）。教程的 `supports_block_scaling()`（第 139–140 行）只接受 capability 主版本 10、11 或 AMD gfx950，所以教程脚本
在这些设备上只打印提示后退出。

### 当前证据

- **已有证据**：[阶段事件](#条件片段阶段事件) E-01、E-02 提供 O1 的节点级理解证据：E-01 覆盖浮点表示，E-02 覆盖块缩放格式、scale 的取法与量化的失效条件。E-03、E-04 提供 O2 中 scale 布局与数据通路部分的理解证据：`tl.dot_scaled` 的逻辑语义与物理布局分离，5D 预排为什么让 scale 原样进 TMEM，不预排时的通用路径与代价，TMA 描述符的三条规则各约束哪个形状；E-04 另证明能由硬件约束推出各级形状，并对没讲过的配置推出 rep 与描述符块形状。E-05 提供 O3 的理解证据，并补上 O2 中 scale 放在哪一步的取舍。E-06 是导师串讲后的综合验收：能把五个节点串成一条叙述，并用计算强度判断 MI300X 上两种存权重方式的取舍；验收中的缺口已补讲；第一次复查暴露的强度单位混用与“藏得住”的判断方式已再补讲；第二次复查暴露的“一个解码出的 FP4 参与几次乘加”已从定义补讲，第三次复查（换成 wave 的排法）答对，综合验收完成。E-07：练习 P1 的实现在 RTX 5090 上通过全部 47 项测试，Review 没有发现阻塞问题，提供 O1、O2 的实践证据（A1–A5）。E-08：A6 的说明补上了 O2 中按字节推进的偏移的理解证据。E-11：V1 通过，补上 A1 的舍入与取指数、A2 的打包的独立证据；可选项 O-1 完成。已确认的前置只决定讲解起点：第 03 课的分块矩阵乘，第 06 课的 FP8 与间距，第 07 课的次正规数，第 08、09 课的
  TMA 描述符、`mma.sync`／`wgmma`／`tcgen05` 的分工与 TMEM、sm_120 的资源上限。
- **仍缺证据**：无。O3 的实证证据由 M1 提供：运行前的预测（E-12）、RTX 5090 上的受控测量（E-13）、对照预测的解释与复查（E-14–E-17）。
- **来源与环境核对（2026-10-14）**：本机无 NVIDIA GPU，在仓库外的临时环境（`triton==3.7.1`、`torch==2.13.0+cu130`）中只编译不运行，特化方式与
  `JITFunction.run` 相同；参数按教程 `initialize_block_scaled()` 与 `block_scaled_matmul()` 的方式构造（`M=N=K=8192`，块 `128×256`，K 方向块
  在 FP4 下为 256、FP8 下为 128，`NUM_STAGES=4`，默认 4 个 warp，输出 fp16）。共享内存以字节计。

  | 格式 | sm_100 | sm_120 | sm_89 |
  | --- | --- | --- | --- |
  | nvfp4 | `tcgen05.mma … kind::mxf4nvf4.block_scale.scale_vec::4X`，221,232 | `mma.sync … m16n8k64 … kind::mxf4nvf4.block_scale.scale_vec::4X … ue4m3`，165,976 | 编译失败：软件换算按 E8M0 处理 scale，`TritonGPUAccelerateMatmul` 断言失败 |
  | mxfp4 | `kind::mxf4.block_scale.scale_vec::2X`，208,944 | `m16n8k64 … kind::mxf4nvf4 … scale_vec::2X … ue8m0`，156,760 | 软件换算（`ttg.fp4_to_fp`、乘 scale、bf16 的 `mma.sync m16n8k16`），32,768 |
  | mxfp8 | `kind::mxf8f6f4.block_scale.scale_vec::1X`，202,800 | `m16n8k32 … kind::mxf8f6f4 … scale_vec::1X`，152,152 | 软件换算，32,768 |
  | mixed（e4m3 × e2m1） | `kind::mxf8f6f4`，202,800 | 软件换算（sm_120 的原生模式不接受 FP8 与 FP4 混合），103,032 | 软件换算，16,384 |

  - sm_100：A、B 用二维 TMA，scale 用五维 TMA（`cp.async.bulk.tensor.5d`）；kernel 中对 scale 的 reshape 与 trans 成为共享内存描述符上的
    `ttg.memdesc_reshape`／`ttg.memdesc_trans`，再由 `tcgen05.cp … .32x128b.warpx4` 从共享内存直接拷入 TMEM（mxfp8、mxfp4、nvfp4 分别
    6、12、24 条）；每线程 170 个寄存器，无溢出。
  - sm_120：scale 经 `ttg.local_load` 读入寄存器，reshape 与 trans 之间没有 `ttg.convert_layout`；累加器在寄存器中，教程配置下每线程用满
    255 个寄存器并溢出（mxfp8 溢出写 2,704 字节，nvfp4 3,548 字节），共享内存也超过 101,376 字节的上限。缩成 `128×128`、`NUM_STAGES=3`、
    8 个 warp 时 mxfp8 为 67,632 字节、200 个寄存器，mxfp4 为 69,680 字节、199 个，都没有溢出。
  - sm_89：描述符在 `make_ttir` 阶段被改写为普通指针读写（逐字节的 `ld.global.b8`，无异步拷贝）。
- **格式核对（2026-10-15）**：在本机按位枚举 FP8（E4M3、E5M2 与两种 FNUZ）、FP6、FP4 的全部编码，最大值、最小正规数与最小次正规数和 OCP MX v1.0 的
  表 2、4、5 及 FP8 论文的 Table 1 一致，FP16、BF16、FP8 的参数与 PyTorch 2.13.0 的 `torch.finfo` 一致。就近取偶的参考编码器与 PyTorch 2.13.0 的
  四种 FP8 类型转换在 459,564 个输入上逐一相同；图解页的编码器与该参考在 78,150 个用例上相同。
- **不预排时的通用路径（2026-10-16）**：同样只编译不运行。把 scale 改为逻辑 `[M, K/V]` 的二维 TMA（块 `[BLOCK_M, BLOCK_K/V]`）并直接传给
  `tl.dot_scaled`，sm_100 下三种格式都能编译。TTGIR 中不再有 `ttg.memdesc_reshape`／`ttg.memdesc_trans` 与 `ttng.tmem_copy`，改为
  `ttg.local_load` 读入寄存器后 `ttng.tmem_alloc`。PTX 中每个 K 步由全部 4 个 warp 各把整块 scale 读进寄存器（nvfp4、mxfp4 用 `ld.shared`，
  mxfp8 用 `ldmatrix`），各自用 `tcgen05.st` 写入自己的 32 个 lane，每次写后 `tcgen05.wait::st` 与 `bar.sync`，再由一个线程发 MMA；教程的
  5D 写法在 `tcgen05.cp` 与 MMA 之间没有等待。编译记录中 A 的 scale 块为 `[128, 16]`、`[128, 8]`、`[128, 4]`（B 为 `[256, …]`），后两者
  不满足块最内维为 16 字节倍数的规则，按 CUDA 文档会在启动时被 `cuTensorMapEncodeTiled` 拒绝，未实跑。
- **节点 5 的 AMD 与单侧 scale 核对（2026-10-17）**：同样只编译不运行。教程的 CDNA4 kernel（MXFP4，128 × 128 × 256，8 个 warp，2 级）在
  gfx950 上编译成 `v_mfma_scale_f32_16x16x128_f8f6f4`（`matrix_instr_nonkdim = 32` 时为 `32x32x64`），scale 是每个 lane 一个 32 位 VGPR、由
  `op_sel` 选字节，`cbsz:4 blgp:4` 表示两侧都是 E2M1；共享内存 34,816 字节，123 个 VGPR，无溢出。同一 kernel 在 gfx942 上编译失败：CDNA3 的模拟
  路径不处理两侧都带 scale 的情形，`tt.dot_scaled` 一直留到转 LLVM，报 `Unsupported DotScaleOp`。另用一套指针写法补齐其余格式：gfx950 上 MXFP8、
  FP8 × FP4 混合都走缩放 MFMA，NVFP4 编译失败；gfx942 上 MXFP8、NVFP4、混合都编译失败。只有一侧带 scale（bf16 × MXFP4）时，各目标都在矩阵乘之前
  解码 MXFP4、乘上 scale，再用 bf16 的矩阵乘：gfx942 用 `amdg.upcast_mxfp`（`v_perm_b32`、`v_and_b32`、`v_pk_mul_f32` 等）加
  `v_mfma_f32_16x16x16_bf16`，gfx950 用 `v_cvt_scalef32_pk_bf16_fp4` 加 `v_mfma_f32_16x16x32_bf16`，sm_100 用 `ttg.fp4_to_fp` 加
  `tcgen05.mma … kind::f16`，sm_120 与 sm_89 用 `ttg.fp4_to_fp` 加 bf16 的 `mma.sync m16n8k16`。gfx950 上 scale 按逻辑形状存时，从 LDS 读 scale 用
  36 条 `ds_read_u8`，按教程预排后用 6 条 32 位读，从显存读进 LDS 的指令两者相同。教程 kernel 编译到 sm_90（H100）：MXFP8 为 `tt.fp_to_fp`、
  `arith.mulf` 加 bf16 的 `wgmma.mma_async … m64n256k16`，保留 TMA，共享内存 217,688 字节；MXFP4 同样走 bf16 wgmma，共享内存 287,864 字节，超过
  每个 block 227 KB 的上限；NVFP4 编译失败。RTX 5090 上 NVFP4 的 128 × 256 × 128、3 级、8 个 warp 为 65,536 字节、223 个寄存器。
- **综合验收的估算依据（2026-10-17）**：MI300X 的平衡点按 1307.4 TFLOPS ÷ 5.3 TB/s ≈ 247 FLOP/字节计，即每读 1 字节约 123 次乘加；向量单元按
  304 个 CU × 每周期 64 个 lane × 2.1 GHz ≈ 40.9 万亿 lane·条/秒计（与向量 FP64 的 81.7 TFLOPS 一致）。节点 5 编出的 gfx942 一侧路径（bf16 × MXFP4，
  128 × 128 × 256，8 个 warp，2 级）中，MFMA 布局为 `warpsPerCTA = [1, 8]`，B 的解码不在 warp 间重复；循环体内每个 wave 每个 K 步有 128 条
  `v_mfma_f32_16x16x16_bf16` 与 222 条其他向量指令（`v_perm_b32` 48、`v_and_b32` 40、`v_cvt_pk_f32_fp8` 32、`v_pk_mul_f32` 22、`v_mul_f32` 20、
  `v_add_u32` 19 等），每个 lane 解码 64 个 FP4。按峰值反推，这条 MFMA 约 16 个周期、一条向量指令 4 个周期，向量指令约为 MFMA 时间的 43%；带宽跑满时
  每秒约需解码 10.6 万亿个 FP4，要用掉向量单元的八到九成。以上都是编译产物上的粗估，未实测。
  2026-10-18 订正与补充：这个配置需要 81,920 字节 LDS，超过 CDNA3 每个 CU 的 64 KB，加载时会报 `OutOfResources`，只能当作编译产物来数指令；
  改用 BLOCK_K = 128（40,960 字节）重编，每个 wave 每个 K 步为 64 条 MFMA 与 104 条其他向量指令，每个 lane 解码 32 个 FP4，c ≈ 3.25，
  向量指令约为 MFMA 时间的 41%，跟上带宽约需向量单元的八成，结论不变。AMD Matrix Instruction Calculator 给出这条 MFMA 发出 4 个周期后
  才能同时发射向量指令，每条最多盖住 3 条向量指令，所以解码最多藏进 MFMA 时间的 75%，超出时计算侧按 max(t_mfma, t_valu + 0.25·t_mfma) 估。
  比较 A、B 时默认访存与计算重叠：循环体先发下一块 A、B 的 `amdg.buffer_load`，再对 LDS 中的当前块做 `local_load`、`amdg.upcast_mxfp`
  与 `tt.dot`（B 的 scale 本轮读、本轮用）；不重叠时取两者之和。B 在 `local_load` 之后按 MFMA 的操作数布局、在各 wave 的寄存器里解码
  （TTGIR 第 109–112 行），M 方向排几个 wave 就解码几份。同样分块的普通 bf16 GEMM 在 gfx942 上排成 `warpsPerCTA = [2, 4]`，每个 wave
  每个 K 步读 24 KB LDS（24 条 `ds_read2st64_b64`，即 64 行 A 加 32 列 B）；单边路径的 [1, 8] 下每个 wave 读 33 KB（32 条 `ds_read_b128`
  读整块 A，2 条 `ds_read2_b32` 读 16 列打包的 B）。节点 5 的 gfx950 单边 kernel 也排成 [2, 4]，`amdg.scaled_upcast_fp4` 作用在各 wave
  `local_load` 出来的 B 上（TTGIR 第 121、132 行）。CDNA3 的 LDS 带宽没有查到官方数字，所以只比较读取量。

### 核心工件与参考

| 角色 | 路径或引用 | 说明 |
| --- | --- | --- |
| 来源 | [`docs/triton-tutorials/official/10-block-scaled-matmul.py`](../../triton-tutorials/official/10-block-scaled-matmul.py) | 教程快照，只读 |
| 来源或知识产物 | [图解页](../attachments/10-block-scaled-matmul/block-scaled-matmul.html) | 节点 1：浮点格式的统一公式与位段对照；尾数怎样切开一档（可调尾数位数与 x，逐步给出 k、r、f、M 与舍入、进位；2026-10-15 应学习者提问增补）；位元探索器（点位看值，输入一个数看舍入、溢出与下溢）；范围与间距对照及参数表（含按 log<sub>2</sub>(最大值 ÷ 最小次正规数) 计的“范围（档）”列）；FP8 的两种分法与两种 E4M3（含 vLLM 的转换）；FP4 的全部编码与舍入区间、档数的两种数法（2026-10-15 应学习者对“3.6 档”的疑问增补）、E8M0。节点 2：同一块数的三种挑 scale 办法（OCP 规则、向上取 2 的幂、NVFP4 两级 scale；每张量 scale 只平移、不加宽，块 scale 在 E4M3 中下溢时整块变 0，2026-10-16 订正节点 2 讲解中的错误表述后增补）与 64 个数的分块对照（MXFP4、NVFP4、MXFP8，每块一个与整行一个 scale）；量化器与 Python 参考实现在 1,208 个用例上逐一相同。节点 4（2026-10-16 增补）：scale 的 5D 预排布局，即逻辑 128 × (BLOCK_K/V) 网格与 512 字节一块的对应，块内字节顺序在显存、SMEM、TMEM 三处相同；可切换格式、拖动滑块或点任一边的格子；第 220 行 reshape／trans 逐步的下标变化（SMEM 字节偏移不变）、C 的取址函数对照、sm_100 TTGIR 节选与 `#shared7` 的读法。五维形状逐维看（2026-10-17 应学习者提问增补）：选一维，看它在块网格、512 字节块、32 位格子、第 394 行的 [2, 256] 视图与同一块的逻辑视图里怎么走；形状链按代码顺序列出 A 的 scale 经过的 8 个形状，每个数字按硬件、TMA 规则、输入大小与分块着色，并跟踪一个 scale 的下标与字节偏移，在 5 组规模与分块上与 PyTorch 实际 reshape／permute 的结果逐项相同；另注明去掉第 394 行的首维 1、改用四维描述符后，sm_100 仍编译成 `tcgen05.cp`。节点 5（2026-10-17）：同一个 `tl.dot_scaled` 在 B200、RTX 5090、RTX 4090、MI355X、MI300X 上对 NVFP4、MXFP4、MXFP8、FP8 × FP4 与 bf16 × MXFP4 的支持矩阵（每格来自本机编译探测）；点格子看数据与 scale 各经过哪些存储层次与指令、scale 用在哪一步、怎样从 32 位里选出、累加器在哪、代价与编译记录；附三种硬件把 4 个 scale 装进 32 位的编译产物对照，以及两家预排 scale 的目标对照；2026-10-18 订正 MI300X 一侧路径格子的编译记录（原配置的共享内存超过 64 KB 上限）。可交互，离线可用 |
| 练习产物 | [`gpu/triton/lesson10_block_scaled_matmul.py`](../../../gpu/triton/lesson10_block_scaled_matmul.py) | 学习者拥有；2026-10-19 版本（SHA-256 前缀 `52586b5f`）在 RTX 5090 上通过全部 47 项测试；第二版（`5ca2a1fb`）只改了名称、报错信息与未用的变量，本机 CPU 层通过；最终版（`95c2840e`，2026-10-20，与第五版 `6399ca8d` 只差 R-06 的两行注释）在 RTX 5090 上通过全部 92 项测试，本机 CPU 层 `82 passed, 10 skipped`，Ruff 通过；入库版即最终版，2026-10-21 提交 |
| 验证或工具 | [`gpu/triton/lesson10_block_scaled_matmul_benchmark.py`](../../../gpu/triton/lesson10_block_scaled_matmul_benchmark.py) | M1 的测量脚本，由 Agent 维护；学习者的预测填入 `PREDICTION` 之前拒绝运行，2026-10-20 已填入（SHA-256 `ecc1a101…`），学习者在 RTX 5090 上运行，结果见 E-13；2026-10-21 以该版本提交 |
| 验证或工具 | [`gpu/triton/lesson10_block_scaled_matmul_test.py`](../../../gpu/triton/lesson10_block_scaled_matmul_test.py) | 练习约定 P1 的验收测试（CPU 层、GPU 层；版本 2 共 92 项，含 O-1 与 V1），由 Agent 维护；最终版 SHA-256 `ab273f93…`，2026-10-21 提交 |

## 条件片段：阶段事件

| 日期 | 覆盖范围 | 证明了什么 | 证据链接 | 标注 |
| --- | --- | --- | --- | --- |
| 2026-10-14 至 2026-10-15 | E-01：开课导入、路线调整、节点 1 与尾数追问、检查 | 学习者追问尾数公式怎样表示两个 2 的幂之间的数；补讲“档的左端 × 1.M”、格点编号、就近取整与进位后，学习者自述为“尾数是在 2 的幂次上放缩的倍数”，并正确解释格点间距逐档翻倍。检查题（E4M3 中 100 与 0.1 所在两档的最坏误差）：两档的格点间距 8 与 2⁻⁷、最坏绝对误差 4 与 2⁻⁸ 都正确，最坏相对误差给出精确值 1/17（在档内第一个中点取到），并说明两档相同；绝对误差的比值写成 2⁹，应为 2¹⁰，属算术笔误，已指出。证明了 O1 前半（浮点表示与精度）的理解 | 本会话；[图解页](../attachments/10-block-scaled-matmul/block-scaled-matmul.html) | 无 |
| 2026-10-15 至 2026-10-16 | E-02：节点 2、节点 1–2 检查题与两次复查 | 第 1 问（E3M0 加每张量 scale）：(a)(b) 正确；(c) 结论对，但理由“0 附近格点更多”说反，补讲按大小加权的绝对误差后，学习者自行归纳出指数位决定范围与跨档的不均匀、尾数位决定每档切多细。复查 1（每块一个 8 倍离群值）：正确选出 E3M0，并用 1/8 以下的格点数说明；对“离群值是少数”补了盈亏点随离群值倍数的变化（约一半到 2–3%）和真实系统的另行处理。第 2 问（块 amax 从 3×10⁴ 到 2×10⁻³）：学习者分析了最大块的精度并提出 E1M2，依据是“每张量 scale 提升了范围”；这一误解来自导师节点 2 第 5 小节的错误表述，题面的“块内跨度不大”“出问题”也没有界定，订正为“每张量 scale 只平移 E4M3 的 17.8 档窗口”。复查 2（vLLM 的 batch 混入块 amax 为 10⁴ 的 token）：正确说明每张量 scale 由异常 token 决定、amax 小的块 scale 下溢后整块变 0、单独运行正常的原因、MXFP4 各块互不牵连，并提出按 token 的第二级 scale；小差距：变 0 的门槛约 0.022 而非 0.044，(b) 所说的格点浪费只在异常块内、两种格式都有，(c) 未提到按行求 amax 可省掉整张量那一遍。证明了 O1 块缩放部分的理解 | 本会话；[图解页](../attachments/10-block-scaled-matmul/block-scaled-matmul.html) | “3.6 档”属出题未定义，第 2 问的误解源于导师讲解错误，均不计为学习者错误 |
| 2026-10-16 至 2026-10-17 | E-03：节点 3、两次答疑、节点 4、节点 3–4 检查题与复查 | 节点 3 后学习者追问两点：scale 的分块是否必须与 kernel 的分块对齐；没有低精度 MMA 的硬件上，scale 乘在元素上还是部分和上。答疑说明沿 K 只须逐层整除（V 整除指令的 K，指令的 K 整除 BLOCK_K），M、N 不必对齐，并比较了两种放法的运算量、寄存器与数值范围。检查题（scale 按逻辑 `[M, K/V]` 存，二维 TMA，直接传给 `tl.dot_scaled`）：第 1 问正确，指出结果仍对，编译器改走经寄存器与 `tcgen05.st` 的路径；第 3 问路径正确，补充寄存器里并不重排字节，代价在于全部 warp 参与、每个 warp 各读一遍整块 scale、MMA 前的等待与更小的 TMA 请求；第 2 问把“每维不超过 256”用到整个张量的 K/V 上，得出 NVFP4 建不起描述符的相反结论，补讲描述符的两种形状与三条规则各自约束的对象。复查（scale 转置存为 `[K/V, M]`，块 `[BLOCK_K/V, BLOCK_M]`）：逐条把规则用到正确的形状上，判断三种格式都能建，并指出 M 须是 16 的倍数。证明了 O2 中 scale 布局与数据通路部分的理解 | 本会话；[图解页](../attachments/10-block-scaled-matmul/block-scaled-matmul.html) | 第 2 问的误解源于导师讲解直接用了未定义的 box，也没有区分整个张量与一次搬运的块，不计为学习者错误 |
| 2026-10-17 | E-04：节点 4 补充答疑（五维形状的推导与各数字的来历，图解页“五维形状”一节）、检查与复查 | 学习者指出这串形状“中间变得太多”，要求从目标逐步推导。补讲按数位拆下标（m = 128mb + 32g + r，j = 4kc + c）：块内 (r, g, c) 由 TMEM 决定，kc 紧挨块外由 K 循环决定，2 × 256 由 TMA 规则决定，首维 1 可去掉（四维描述符的编译探测），trans 是唯一改变数位先后的一步。检查题（TMEM 格子改为 64 位、一格装 8 个 scale）：物理形状、主机端四维 [M/128, K/V/8, 32, 32]、TMA 视图 [1, M/128, K/V/8, 4, 256]、块形状与第 220 行三步都推对，trans 不变的理由（行、列的数位各自挨在一起）正确；小差距：没写出 rep_k 随之变为 BLOCK_K/V/8，没列出不变的数字；把 trans 的作用说成“更好的连续访存”，订正为 trans 只改变下标的含义，访存是否连续由物理排法决定，漏掉它会算错。复查（块内改为 (g, r, c)）：正确写出 reshape(rep_m, rep_k, 4, 32, 4)、trans(0, 2, 3, 1, 4)，并指出照抄原顺序会因合并顺序错而算错。证明了 O2 中由硬件约束推出 scale 布局与第 220 行换算、对没讲过的配置推出各级形状的理解 | 本会话；[图解页](../attachments/10-block-scaled-matmul/block-scaled-matmul.html) | 无 |
| 2026-10-17 | E-05：节点 5（五种目标的落地）、检查与复查 | 讲解同一 `tl.dot_scaled` 在 sm_100、sm_120、sm_89、gfx950、gfx942 上的落地，支持矩阵来自编译探测。检查题（迁移到没讲过的 H100）：第 1 问正确预测 Triton 走通用软件换算，即解码成 bf16、在矩阵乘之前乘 scale、用 bf16 张量核，与 sm_90 的编译结果（bf16 的 `wgmma … m64n256k16`）一致；第 2 问正确把 scale 挪到部分和上，但没答出条件与代价，补讲 V ≥ 指令的 K、乘法次数之比 BM·BN/(V·(BM + BN))、两份累加器的寄存器压力与异步流水被打断。复查（NVFP4 的 V = 16；每 128 个元素一个 scale）：正确指出 V = 16 时一条 wgmma 跨两个 scale 块、部分和已无法拆开，并说明每 128 一个 scale 时乘 scale 与等待都降到 1/4、FP8 约 2 倍的吞吐足以掩盖，由此解释 DeepGEMM 的 BLOCK_K = 128。证明了 O3 的理解部分（各目标上 scale 放在哪、代价落在哪，以及迁移到新硬件），也补上 O2 中 scale 放在哪一步的取舍 | 本会话；[图解页](../attachments/10-block-scaled-matmul/block-scaled-matmul.html) | 无 |
| 2026-10-17 至 2026-10-18 | E-06：导师串讲与综合验收（口述一题，MI300X 上的取舍一题）、三次复查 | 第 1 题（口述五点）：为什么要块缩放（格点少、按块把离群值的影响限在块内、scale 的存储开销、饱和与变 0）、B200 在 MMA 指令内部乘 scale、主机端预排成 [M/128, K/V/4, 32, 4, 4] 而 kernel 里只改视图、没有块缩放指令时 Triton 解码成 bf16 并逐元素乘 scale 再用 bf16 矩阵乘，均正确。缺口：没讲 scale 进矩阵单元的物理通路（五维 TMA → SMEM → 单线程 `tcgen05.cp` → TMEM）；软件换算没讲代价与边界（只认 E8M0，NVFP4 编不过；MI300X 上两侧都带 scale 时编译失败）；把 (32, 4, 4) 归因于“一个 warp 只能用 32 个 lane”，订正为 PTX 图 237 的规定与 `.32x128b.warpx4` 的复制，访问限制只约束 `tcgen05.ld`／`tcgen05.st`。第 2 题：两种负载的瓶颈与 B 的快慢方向正确，取 N = K = 1000 估出 7.87 与约 445 FLOP/字节（写出的式子漏了乘加的 2 与输出项，数值按完整式子）。缺口：没有和 MI300X 的平衡点（约 247 FLOP/字节）比较；预填充应为 B 至多和 A 一样快（例中 B 只少读 8% 的字节，解码指令按编译产物粗估约为 MFMA 时间的 43%）；“总保留的好处”答成访存量，订正为显存容量。复查（DeepSeek-V3 式路由，均匀时每个专家 M = 128，学习者取 N = K = 1024）：M 与“省出的显存给 KV cache、承载更多并发”正确，强度计入了激活与 scale 的字节；但把乘加次数当作 FLOP 与 247 相比，A 的结论碰巧仍对，B 的 163.8 次乘加/字节实际高于平衡点约 123、已到计算瓶颈，却被判为访存瓶颈，进而判断 B 可能比 A 慢（以 MFMA 按峰值的时间 T 计，A 约 2.2T，B 在解码并行与不并行时为 1T 与 1.43T，应为快约 1.5–2.2 倍）；把解码藏不住归因于 M 小，订正为 M ≥ BLOCK_M 时解码相对 MFMA 的开销只取决于 BLOCK_M，且“藏不住”须算出总时间再与 A 比。学习者问怎样量化“藏得住”与“跟得上带宽”，补讲按资源分别算忙碌时间（t_mem、t_mfma、t_valu）、比值 16c/BLOCK_M、每条 MFMA 只留出 16 个周期中的 12 个给向量指令，以及带宽一侧的 0.244c。第二次复查（BLOCK_M 改为 32）：比值 16 × 3.5 / 32 = 1.75 超过 0.75、藏不住，尽量并行时 B 约 2.0T、比 A 略快，完全不并行时约 2.75T、比 A 慢，均正确（后者误写为“完全并行”）。缺口：一个解码出的 FP4 在 CTA 内参与的乘加数答成 BLOCK_M × K = 32768，应为 BLOCK_M = 32（它只与本 CTA 的 BLOCK_M 行各乘一次，32768 是 B 一整列 K 个元素的合计）；学习者同时追问比值的来历，已用循环嵌套、每个 CTA 每个 K 步的解码数与乘加数、总量与忙碌时间从定义推导，并说明规格表把一次乘加记作 2 次运算。学习者还指出导师评阅第一次复查时默认访存与计算重叠而未写明，并补算不重叠时 B 快约 1.8 与 1.45 倍，正确；已补两种假设的对照。导师另订正：节点 5 的 gfx942 探测配置超出 LDS 上限，换成可运行的配置后 c ≈ 3.25，结论不变（见“综合验收的估算依据”）。学习者问 wave 改排为 [2, 4] 会改变什么，补讲 warpsPerCTA：每个 wave 负责 CTA 块中的一个子块，要从 LDS 读这个子块用到的 A 行与 B 列，并以编译产物对照两种排法每个 wave 的读取量。第三次复查（8 个 wave 改排为 [2, 4]）：学习者把排法概括为块内再分块，答出 M 方向的两个 wave 各解码一份、每份参与 64 次乘加、分别累加进本块前 64 行与后 64 行（应限定为第 n₀ 列的各 64 个元素），比值 16 × 3.5 × 2 / 128 = 0.875 超过 0.75、藏不住，尽量并行时 B 约 1.125T，方法与结论正确；题目给定 c = 3.25，对应 0.81 与约 1.06T，结论相同。综合验收至此完成：O1–O3 的理解证据充分，只差 O2 中 FP4 的打包与按字节推进的偏移 | 本会话 | (32, 4, 4) 的归因来自导师节点 4 的讲法，不计为学习者错误；第一次复查的评阅默认访存与计算重叠而未写明，由学习者指出，属导师讲解缺口；gfx942 探测配置超出 LDS 上限，属导师核对疏漏；第三次复查出题时没讲每个 wave 负责哪一块、读哪些数据，属出题缺口 |
| 2026-10-18 至 2026-10-19 | E-07：练习 P1 的实现与首次 Review | 学习者在 GPU 机器上写完四个函数并拷回本机：RTX 5090（capability 12.0，驱动 595.71.05，torch 2.13.0+cu130，CUDA 13.0，Triton 3.7.1）上 `47 passed`，实现文件 SHA-256 `52586b5f4ed745278a8161420f111dcd7b785ea262dc6c7e2bb2c1c6df78fcf3`，测试文件 `c3179560d8318325224f0bab3a16b4ab158f2db419e690fdf5f186dddcb0f32e`（即仓库中的版本）；本机 CPU 层 `42 passed, 5 skipped`。Review 核对了测试不查的部分：kernel 用指针读入、每个 K 步调用一次 `tl.dot_scaled`、fp32 累加，B 以转置传入而它的 scale 不转置，参数检查都在发射之前，没有调用库的 FP4、E8M0 转换（指数直接读 FP32 的指数字段，次正规数与 0 读出 −127、减 2 后截回 −127，结果仍对；舍入按档定间距后用 `torch.round` 取偶；反量化先转 float32 再减 127）。问题见 R-01–R-04，均不阻塞验收。证明了 A1–A5 通过；其中 A1 的舍入与取指数、A2 的打包有求助，由 V1 确认；A6、V1、M1 待完成 | 本会话；`gpu/triton/lesson10_block_scaled_matmul.py`（未提交） | 实现过程中的求助见[帮助影响](#条件片段帮助影响) |
| 2026-10-19 | E-08：A6 书面说明 | (a) 前半正确：一个 K 步处理 BLOCK_K 个元素，两个元素占一个字节，所以 packed 前进 BLOCK_K // 2；每 32 个元素一个 scale，所以 scale 前进 BLOCK_K // 32。后半首答把块宽与前进量混在一起：实测时把两个 `tl.arange` 也改成了 BLOCK_K，得到 `dot_scaled` 的形状报错（scale 块 `[128, 128]`，期望 `[128, 8]`），据此认为会编译报错。指出两种角色（块宽是张量形状，编译时检查；前进量是运行时的地址）后重做，只改前进量：正确说明形状不变、能编译，packed 读到约 2 倍远、scale 约 32 倍远的位置，越过本行乃至张量末尾；RTX 5090 上 3 项数值测试失败（误差相对界限为 inf、3.88e7、nan），其余 44 项通过。补充说明：单个 K 步的用例因 k_id = 0 而照常通过，抓这类错误要有多个 K 步；读到的 scale 字节可能是 255（NaN）或极大的 2 的幂，所以出现 nan、inf；越界读不一定报错。(b) 选 `test_sm120_uses_the_native_block_scaled_mma`，说明它检查编译产物、防止退回软件换算，正确。证明了 O2 中按字节推进的偏移的理解，A6 通过 | 本会话 | 无 |
| 2026-10-19 | E-09：P1 版本 2（可选项 O-1）、V1 与测试扩充 | 学习者选做可选项 O-1，接受 Agent 提出的接口与验收方式（“我接受O-1”）；A1–A6 通过后按约定给出 V1（MXFP6 E3M2 的量化、打包与反量化）。测试扩充为 92 项，O-1、V1 各从一项 expected red 开始，参考实现与 17 个故意写错的变体的核对见[测试的扩充](#测试的扩充2026-10-19)。同日学习者把量化与反量化改成整张量写法，量化通过，反量化出现回归（R-05） | [练习约定](#条件片段练习约定)；`gpu/triton/lesson10_block_scaled_matmul_test.py` | 无 |
| 2026-10-19 | E-10：M1 的脚本与规格 | 学习者请 Agent 开始准备 M1（“好的，请开始吧。”）。交付测量脚本，公布方法、候选、判据与 RTX 5090 的规格（白皮书附录 A 表 3），请学习者在运行前写出两个 M 下 time(software) / time(native) 的区间、各路径的瓶颈与理由 | [M1 的脚本与规格](#m1-的脚本与规格2026-10-19)；`gpu/triton/lesson10_block_scaled_matmul_benchmark.py` | 无 |
| 2026-10-20 | E-11：V1 通过；可选项 O-1 完成；R-04、R-05 关闭 | V1 首交（`878a2f26`）数值全对，但打包的位序约定反了，并漏了 K 的检查（见[帮助影响](#条件片段帮助影响)）；学习者画图说明小端位流、手算答对后自己改正。第五版（本机副本 SHA-256 `6399ca8d0ca00959995a83f35630955d5643fbaf1dca9f4739e0a60759ad2b51`）：学习者报告在 GPU 机器上 `92 passed in 2.85s`，GPU 机器为 RTX 5090（驱动 595.71.05，torch 2.13.0+cu130，CUDA 13.0，Triton 3.7.1），测试文件 SHA-256 `ab273f93cd344d2d8c5bba89bb6672ca6897e3aafdac68f29c251bd91308959a` 与本机相同，实现文件却是 `95c2840e78b7533499d47988b226dbdd5da0ae7641c812a53917aefac621fbe2`。学习者随后把它拷回本机；把其中第 306–307 行的注释改回原样，得到的文件与 Review 过的 `6399ca8d` 逐字节相同，两版只差 R-06 的注释，GPU 上的结果对两版都成立；本机 CPU 层 `82 passed, 10 skipped`，与不进仓库的参考实现相同；`ruff check`、`ruff format --check` 通过。Review 核对了测试不查的部分：V1 按 E3M2 的七档定舍入间距（次正规数与 E = 1 同为 0.0625），取指数的偏移 −4（E3M2 能表示的最大 2 的幂为 16 = 2^4）由约定推出，指数直接读 FP32 的指数字段，没有调用库的 FP6、E8M0 转换；打包与解包逐位对照约定无误。O-1 的 kernel 用指针直接读五维 scale（块间步长 4K 与 512，块内 16、4、1），在 kernel 内转置并 reshape 成二维后交给 `tl.dot_scaled`，参数检查都在发射之前。V1 通过：A1 的舍入与取指数有了独立证据；A2 的打包中，位操作是独立证据，位序约定经 Agent 指出出错的步骤后自己改正。O-1 完成（不属于完成门槛）。R-04、R-05 关闭，新记 R-06（不阻塞） | [练习约定](#条件片段练习约定)；`gpu/triton/lesson10_block_scaled_matmul.py`（未提交） | V1 的求助见[帮助影响](#条件片段帮助影响) |
| 2026-10-20 | E-12：M1 的预测（运行前） | 学习者在运行前写出两个 M 下的比值区间、各路径的瓶颈与估算（见 [M1 的脚本与规格](#m1-的脚本与规格2026-10-19)）：M = 16 为 [0.99, 1.01]，两条路径都受显存带宽限制；M = 8192 为 [7.8, 8.2]，两条路径都受张量核算力限制。预测原样填入脚本（SHA-256 `ecc1a101b1e2252f53122245537f161b835cecc974f80d47687cac32c82d717b`），可被事前判据推翻；运行与解释待完成 | [M1 的脚本与规格](#m1-的脚本与规格2026-10-19) | 无 |
| 2026-10-20 | E-13：M1 的运行结果 | 学习者在 RTX 5090 上运行脚本，打印的 SHA-256 为 `ecc1a101…`，即填入预测后的版本；驱动 595.71.05，最高 SM 频率 3090 MHz，功耗上限 575 W，torch 2.13.0+cu130，CUDA 13.0，Triton 3.7.1。40 个候选都通过了路径与数值核对，没有跳过。选中的配置：M = 16 时两条路径都是 16×32×512、3 级、4 个 warp；M = 8192 时原生为 128×128×256、2 级、8 个 warp，软件为 128×64×64、3 级、4 个 warp（软件的 128×128×256 溢出 412 字节，用了 33.2 ms）。15 轮的中位数（四分位距）：M = 16 原生 0.0287 ms（74.8 TFLOPS；必须搬运的字节对应 1263 GB/s，为峰值的 70.5%），软件 0.0451 ms（47.6 TFLOPS，为 BF16 峰值的 22.7%；804 GB/s，44.9%），比值 1.570（1.568–1.571）；M = 8192 原生 1.3792 ms（797.2 TFLOPS，为 FP4 峰值的 47.6%），软件 6.0099 ms（183.0 TFLOPS，为 BF16 峰值的 87.3%），比值 4.368（4.169–4.377）。按事前判据，两个 M 都是“否定”。百分比按白皮书 2407 MHz 下的峰值计算，运行时的实际频率没有记录。学习者的解释待完成 | 学习者贴回的完整输出（本会话） | 无 |
| 2026-10-20 | E-14：M1 的首次解释与评估 | 学习者的解释：M = 16 时“访存的速度相差较大……带宽差距接近 1.5 倍，导致最终耗时比值在 1.5 倍左右”；M = 8192 时“软件的测试上出现了寄存器溢出……我不明白为什么比值低了。看上去fp4没达到峰值”；“结果不支持我的预测”；要分开访存、解码与矩阵乘加，“可能需要制作独立的kernel”。按要点评：剩余不确定性一项合理；M = 8192 看出 FP4 没到峰值，但把未选中的配置的溢出当成了测量的配置（选中的软件配置 229 个寄存器、没有溢出），也没有把比值拆成峰值比 × 效率比；M = 16 以带宽差解释耗时差是循环论证（带宽一列是同一字节数除以时间），没有指出软件路径既没到带宽上限也没到算力上限；没有说出结果支持什么。Agent 补讲了这几处，并按事前的承诺逐步对照了预测的推理（见[帮助影响](#条件片段帮助影响)）；给出换条件的复查题（M = 16、A 改为 bf16 存放的 W4A16 变式）。M1 待复查 | 本会话；[M1 的脚本与规格](#m1-的脚本与规格2026-10-19) | 解释的缺口由 Agent 讲出，以复查题确认 |
| 2026-10-20 | E-15：M1 复查题的回答；第 2 问的出题歧义与换题 | 学习者的回答：第 1 问“每个K步需要解码`512*16 = 8,192`个元素，每个元素在本次K步中参与8次乘加”，正确（A 改为 bf16 后只有 B 要解码，复用次数从 5.3 升到 8）。第 2 问按“`2*4*8192*4.5 = 294,912`条解码指令”加“`200*8 = 1,600`条其他指令”，除以 2407 MHz 得 123.18 µs，“远大于显存的20.2µs”；第 3 问据此答“软件总时间大概更慢，主要受解码的影响”。核对：题目给的“每个元素约 4 条”是线程级条数（一个 lane 为它负责的一个元素执行的条数），“每个调度器每周期发射 1 条”是 warp 级，两者差 32 倍，题目和 E-14 的讲解都没有写出这一换算（E-14 同时给了“约 1500 条用来解码”与“12,288 个元素、每个约 4 条”，没有对上）；每个 SM 有 4 个调度器也只是隐含。这两处属出题问题，不记为学习者的差距。学习者自己的差距：题目写明的 16 个 K 步只算了 1 个（执行差距）；没有拿已知结果核对（这一变式要解码的元素比实测少三分之一，估出的发射时间却是实测总时间的近 3 倍）；第 3 问没有给出范围。Agent 澄清了两种条数与换算，用实测的 M = 16 软件路径演示了 warp 级记账（见[帮助影响](#条件片段帮助影响)），没有给出 W4A16 变式的正确数字；按规则换题复查：M = 16、A 为 bf16、B 为 MXFP8（E4M3）的 W8A16 变式，结构同实测的软件路径，每个 B 元素约 4.8 条线程级指令（含乘 scale）、其他每个 warp 每个 K 步约 300 条 warp 指令（按本机编译出的 SASS），每个 CTA 66,048 字节共享内存、每个 SM 同一时刻只驻留 1 个 CTA，最少字节约 70.0 MB。学习者随后追问 12,288 与 3.9 的来历：Agent 说明约 1505 条是 SASS 中直接数出的解码类 warp 指令、3.9 = 1505 ÷ 384（每个 lane 384 个元素）是由它反推的 A、B 平均（E-15 的演示把推导方向写反了），并按 Triton 源码拆分这 1505 条（每 8 个 FP4 17 条的内联 PTX、只属于 B 的 NaN 处理 `SEL`、重排与搬运）；W4A16 题把这个平均值当作 B 的单价，偏低，是该题的又一处出题问题（该题已撤换）。学习者再问“12,288 × 3.9 ÷ 32 ≈ 1500 条”是否有错：Agent 确认这一行归类有误，1505 条里的 256 条 `SEL` 是 B 的 NaN 处理，应算作 scale 处理，B 的 scale 处理每个元素 1.5 条而不是 0.5 条；总数 1842 条与 24.5 µs 不受影响；W8A16 题的 4.8 条已含乘 scale 与 NaN 处理两项，题面“含乘 scale”应读作“含 scale 处理”，数值不变。M1 待复查 | 本会话；[M1 的脚本与规格](#m1-的脚本与规格2026-10-19) | 第 2、3 问受出题歧义影响，以换题复查确认 |
| 2026-10-20 | E-16：M1 换题复查（W8A16）的回答与评估 | 学习者的回答：第 1 问“`8192/32*4.8+300 = 1,528.8`”，每个调度器“`2*16*1528.8 = 48,921.6`”条，“`48921.6/2407 = 20.325`微秒”，显存“`70/1.792 = 39.0625`微秒”：线程级到 warp 级的换算、16 个 K 步、4 个调度器全部正确，两个 CTA 先后执行时每个调度器仍承担 2 个 warp 也处理对了（E-15 中受出题歧义影响的范围由此确认）；把加上 300 条后的总数称作“解码指令数”，只是用词。第 2 问上限“59微秒左右”正确；“实际更接近完全不重叠”，理由是重叠需要每个调度器上有足够多的 warp 轮流，而同一时刻每个 SM 只驻留 1 个 CTA，正确；下限答“20微秒左右”，错：两部分完全重叠时总时间等于较长的一项，即显存的约 39.1 µs，与第 3 问“主要受到显存搬运的限制”也不一致。第 3 问“更慢”“主要受到显存搬运的限制”结论正确，但没有给出理由（完全重叠也不少于约 39.1 µs，已超过原生的 28.7 µs；FP8 权重的最少字节约 70 MB，MXFP4 约 36 MB）。Agent 补讲了下限的取法（见[帮助影响](#条件片段帮助影响)），给出更小的换条件题：同一 W8A16 kernel 换到显存带宽 3584 GB/s、其余与 RTX 5090 相同的假想卡上，问两部分时间、上下限与限制资源；W4A16 的对照放到这道题之后。M1 待复查 | 本会话 | 下限的取法由 Agent 讲出，以小题确认 |
| 2026-10-20 | E-17：M1 的小题；M1 通过，P1 必需项全部通过 | 学习者先说明 E-16 的下限是笔误（“之前应该是取大的那个显存搬运时间39微秒”），再答小题：显存时间减半为“19.5微秒”，“发射时间不变，还是20.3微秒”，“下限就是取大的那个20.3微秒，上限是二者之和39.8微秒”，“这时受到发射时间的限制……下限被发射时间的20.3限制了”，全部正确：较长的一项换成发射时间后，下限仍取对。Agent 补充：两项接近且重叠差时，实际时间靠近两者之和，只缩短其中一项收效有限；并按承诺对照了 W4A16 变式（按题设每个 warp 每个 K 步 1352 条、发射约 18.0 µs，本机编译为 1608 条、约 21.4 µs，显存约 20.3 µs，处在转折点；比实测软件路径的 45.1 µs 快，但按相加只快约 7%，因为去掉的 A 解码只是解码里较小、较便宜的一部分），均为只编译的估算。M1 的预测（E-12）、受控测量（E-13）、解释与复查（E-14 至本条）齐备，M1 通过；P1 的必需项 A1–A6、V1、M1 全部通过，阻塞问题均已关闭，进入结课确认 | 本会话；[M1 的脚本与规格](#m1-的脚本与规格2026-10-19) | 结课 |

## 条件片段：练习约定

本节是练习 P1 的完整约定，实现时以它为准；验收测试是它的可执行形式。两者不一致时以本节为准，由 Agent 修测试。

- **编号与版本**：P1，版本 2，学习者接受于 2026-10-19（“我接受O-1”）：在版本 1（2026-10-18，“接受P1”）之上补定可选项 O-1 的接口与验收测试，门槛不变。V1 的内容按约定在 A1–A6 通过后给出，见下文。
- **为什么做**：O1、O2 缺实践证据，O2 还缺“两个 FP4 拼一个字节与按字节推进的偏移”的理解证据；O3 缺实证证据（RTX 5090 上先预测、再做一次受控测量）。

### 交付物

一个文件 `gpu/triton/lesson10_block_scaled_matmul.py`，含四个函数。教程用随机生成的 FP4 编码与 scale（第 333、367 行）；这里从真实的浮点数出发，
完整走一遍“量化 → 打包 → 矩阵乘”。

| 函数 | 输入 | 输出与要求 |
| --- | --- | --- |
| `quantize_mxfp4(x)` | 二维 float32 或 bfloat16，形状 `[R, K]`，K 是 32 的倍数，只含有限值；CPU 或 CUDA | `(packed, scales)`：`[R, K // 2]` 与 `[R, K // 32]` 的 uint8，与 `x` 同设备 |
| `dequantize_mxfp4(packed, scales)` | 上面两个张量 | `[R, K]` 的 float32 |
| `swizzle_scales(scales)` | `[R, K // 32]` 的 uint8；R 是 128 的倍数，K // 32 是 4 的倍数 | `[R // 128, K // 128, 32, 4, 4]` 的连续 uint8，`out[mb, kc, r, g, c] = scales[128·mb + 32·g + r, 4·kc + c]` |
| `mxfp4_matmul(a_packed, a_scales, b_packed, b_scales, *, block_m=128, block_n=128, block_k=128, num_stages=3, num_warps=8)` | A 为 `[M, K // 2]` 与 `[M, K // 32]`；B 为 `[N, K // 2]` 与 `[N, K // 32]`（权重按 `[N, K]` 存、沿 K 打包，同教程的 `b`）；全部是连续的 uint8，在同一设备 | `[M, N]` 的 float32，等于 `dequantize(A) @ dequantize(B).T` |

对实现的要求：

- **量化规则**（OCP §6.3）：沿 K 每 32 个元素一块。指数 e = ⌊log₂(amax)⌋ − 2，截到 [−127, 127]，scale 字节 = e + 127；元素 = V / 2^e，按就近取偶
  舍入到 E2M1 的格点 {0, 0.5, 1, 1.5, 2, 3, 4, 6}（带符号），超过 6 的饱和到 ±6，绝对值不超过 0.25 的变 0；全零块的元素全为 0，scale 字节不得为
  255；零的符号不作要求。实现里不调用 `triton.tools.mxfp` 或其他库现成的 FP4、E8M0 转换。
- **编码与打包**：一个 FP4 编码为 4 位 `S EE M`（1 位符号、偏置为 1 的 2 位指数、1 位尾数）；第 j 个字节的低 4 位放第 2j 个元素，高 4 位放第 2j+1 个。
- **kernel**：模块级的 `@triton.jit`；用指针读入，不用描述符；每个 K 步调用一次 `tl.dot_scaled(..., "e2m1", ..., "e2m1", acc)`，fp32 累加。
- **尺寸**：M、N、K 分别是 block_m、block_n、block_k 的整数倍；测试用 `64×64×64`（4 个 warp）与默认的 `128×128×128`。
- **错误输入**抛 `ValueError`：`quantize_mxfp4` 的输入不是二维、dtype 不对、K 不是 32 的倍数；`swizzle_scales` 的形状不满足倍数；`mxfp4_matmul`
  的张量不是二维 uint8、不连续、不在同一设备，A、B 的 K 不一致，packed 与 scales 的 K 对不上，尺寸不是块大小的整数倍。不必检查是否在 CUDA 上
  （只编译层用 CPU 张量调用包装函数）。

### 验收项

| 编号 | 验收项 | 检查方式 |
| --- | --- | --- |
| A1 | `quantize_mxfp4` 的 scale 字节与元素编码符合上述规则：取偶、饱和、变 0、全零块、e 截到 −127，float32 与 bfloat16 两种输入 | 测试（CPU），以 Triton 的 `MXFP4Tensor` 构造对照 |
| A2 | 打包顺序正确；`dequantize_mxfp4` 与量化、打包相互对得上 | 测试（CPU） |
| A3 | `swizzle_scales` 的下标对应与错误输入 | 测试（CPU），另以教程第 404–407 行 `unpack_scale` 的写法反向核对 |
| A4 | `mxfp4_matmul` 的结果正确：多个 K 步、多个 CTA、非方阵、每块 scale 不同；错误输入抛 `ValueError` | 测试：数值在 GPU 上（RTX 4090 走软件换算，RTX 5090 走原生），错误输入在 CPU 上 |
| A5 | 编到 sm_120 时走原生块缩放（PTX 有 `kind::mxf4nvf4.block_scale`，TTGIR 没有 `ttg.fp4_to_fp`），编到 sm_89 能成功 | 测试（只编译，替身驱动，不需要 GPU） |
| A6 | 3–5 句书面说明：(a) 为什么打包的操作数每个 K 步前进 BLOCK_K // 2 字节、scale 前进 BLOCK_K // 32，误写成 BLOCK_K 时哪项测试失败、结果错成什么样；(b) 从测试里挑一项，说明它防的是哪种错误 | Agent 按要点评 |
| V1 | A1–A6 通过后，Agent 给一个无提示的小变式（表面不同、原理相同），学习者独立完成 | 测试或按要点评 |
| M1 | RTX 5090 上的一次受控测量：结果出来前写预测，出来后用 5–8 句对照预测解释 | Agent 按要点评；预测不符不算失败 |

M1 的设置（方法与脚本由 Agent 负责，运行前完整公布）：两个 kernel 只差 A 带不带 scale，输入字节相同。带 scale 时编成原生的
`mma.sync … kind::mxf4nvf4.block_scale`；去掉 A 的 scale 时，sm_120 的原生模式要求两侧都有 scale，Triton 退回软件换算（`ttg.fp4_to_fp` 解码成
bf16、乘 B 的 scale、bf16 的 `mma.sync … m16n8k16`，本机编译探测已确认）。软件这边少乘一次 A 的 scale，偏向软件，测出的原生优势是下限。形状为
M = 16（访存受限，像解码）与 M = 8192（计算受限），N = K = 8192；两条路径用同一组候选配置、各取最快；计时前先核对结果；多轮轮换、取中位数与
波动；运行前打印“支持／否定／证据不足”的判据。学习者预测两个形状下“软件时间 ÷ 原生时间”各约多少、瓶颈在哪、理由；预测前 Agent 给出 RTX 5090
的带宽、FP4 与 BF16 张量核算力等规格并注明来源。

### 怎样运行测试

在仓库根目录执行（容器里写作 `uv run --frozen python -m pytest …`），测试文件是 `gpu/triton/lesson10_block_scaled_matmul_test.py`。

| 层 | 命令 | 需要 GPU | 覆盖 |
| --- | --- | --- | --- |
| CPU 层 | `pytest -q gpu/triton/lesson10_block_scaled_matmul_test.py`（没有 GPU 时数值项自动跳过） | 否 | A1–A3、A4 的错误输入、A5 |
| GPU 层 | 同一条命令，在 RTX 4090 或 RTX 5090 上执行 | 是 | A4 的数值、CUDA 上的量化，以及上面各项 |

Triton 3.7.1 的解释器没有实现 `dot_scaled`，没有解释器层，kernel 的数值只能在 GPU 上验证。

### 测试没有检查的

- NaN、Inf 输入与零的符号，约定不作要求。
- kernel 的读入方式：“用指针读入、不用描述符”不由测试检查，Review 时看源码。
- 任何性能指标。性能只在 M1 里作为一次受控测量出现。

### 边界与门槛

- **文件边界**：你写 `gpu/triton/lesson10_block_scaled_matmul.py`；我维护 `gpu/triton/lesson10_block_scaled_matmul_test.py`、
  `gpu/triton/lesson10_block_scaled_matmul_benchmark.py` 与本记录、Checkpoint；我只读教程快照、学习者的实现与 Triton 的 `triton/tools/mxfp.py`；
  本次不动其他课程与其他 Lesson 的文件、`docs/triton-tutorials/official/`、依赖文件（`pyproject.toml`、`uv.lock`）。
- **求助**：可以随时求助；透露了某个验收项的关键解法时，只影响那一项，之后以表面不同、原理相同的新变式确认，其余不受影响。
- **非目标**：NVFP4 与 MXFP8 的量化器、NaN 与 Inf 输入、尺寸不整除时的 mask、TMA 描述符、sm_100 实机、与 cuBLAS 对比、autotune。
- **可选项**：kernel 改读 `swizzle_scales` 的五维输出，像教程第 220 行那样在 kernel 里 reshape 与 trans（学习者 2026-10-19 选做，接口见下文“可选项 O-1”）；M1 里顺带测 Triton 的单边 bf16 × MXFP4（W4A16）作参照。
- **完成门槛**：A1–A6、V1、M1 全部通过，阻塞问题全部关闭。

### 测试的建立（2026-10-18）

测试共 47 项。仓库内实现尚不存在时为 `1 failed, 46 skipped`（expected red，失败项是“实现文件存在”）。以一份不进仓库的参考实现核对：本机（无 GPU）
CPU 层 `42 passed, 5 skipped`，跳过的 5 项是 GPU 数值项；15 个故意写错的变体各被对应的测试报红：指数少减 1、tie 一律进位、按 1e-6 的容差取偶、
指数不截到 −127、高低半字节对调、全零块的 scale 写成 255、用 float32 的 `log2` 取指数、swizzle 的维度次序错、反量化丢符号、解包时高低对调、
kernel 去掉 A 的 scale、不查连续性、先发射再检查、不查 B 的 K、只查 A 的 scale。GPU 层没有在本机运行过。

对照的两处局限：`MXFP4Tensor` 离中点约 1e-6 以内也会取偶（例如 2.500000238 被舍成 2，应为 3），所以随机数据取在 1/64 的格上，紧挨中点（上下各一个
ulp）的情形在测试里手写期望；float32 的 `torch.log2` 在紧挨 2 的幂下方会舍成整数（`log2(7.9999995)` 得 3.0），测试改用 `frexp` 取指数，并含
“块最大值比 2 的幂小一个 ulp”的用例。测量脚本于 2026-10-19 交付，见“M1 的脚本与规格”。

### 可选项 O-1（版本 2，2026-10-19 接受）

学习者 2026-10-19 选做。不改 `mxfp4_matmul` 的约定，另加一个入口：

| 函数 | 输入 | 输出与要求 |
| --- | --- | --- |
| `mxfp4_matmul_swizzled(a_packed, a_scales, b_packed, b_scales, *, block_m=128, block_n=128, block_k=128, num_stages=3, num_warps=8)` | packed 同 `mxfp4_matmul`；scale 是 `swizzle_scales` 的输出 `[M // 128, K // 128, 32, 4, 4]` 与 `[N // 128, K // 128, 32, 4, 4]`，连续的 uint8，在同一设备 | 与 `mxfp4_matmul` 用未预排的 scale 算出的结果相同（同一容差）的 `[M, N]` float32 |

- **kernel**：模块级的 `@triton.jit`，用指针读入；每个 K 步读出本块的 `[rep_m, rep_k, 32, 4, 4]` 与 `[rep_n, rep_k, 32, 4, 4]`，像教程第 220 行
  那样 trans、reshape 成二维，再传给 `tl.dot_scaled`。
- **块大小**：block_m、block_n、block_k 都是 128 乘 2 的幂（一块五维 scale 管 128 行、沿 K 128 个元素，`tl.arange` 的长度要是 2 的幂）；M、N、K
  分别是对应块大小的整数倍。
- **错误输入**在发射之前抛 `ValueError`：scale 不是五维、不连续或不是 uint8，scale 的形状与 packed 不符，块大小不满足上述条件，以及
  `mxfp4_matmul` 的各项检查。
- **测试**：入口存在（expected red）；只编译，4 种块配置（默认、rep_m = 2、rep_n = 2、rep_k = 2 且 2 级流水）× sm_120 与 sm_89，检查
  `tl.dot_scaled`、共享内存不超上限、TTIR 中由 kernel 自己读入五维的 scale 块（防止在主机端还原成二维再调用二维 kernel）；sm_120 走原生块缩放
  4 项；参数检查 10 种，在替身驱动下“先报错、不发射”；GPU 数值 4 种配置，每种 4 个 CTA、至少 2 个 K 步。运行：`-k o1`。
- **可行性核对**：Agent 用不进仓库的探测 kernel 确认，这四种配置在 sm_120 上都编成原生指令，共享内存最多 51,712 字节；在 sm_89 上都能编译。
- **门槛**：不属于完成门槛；中途放弃时撤掉这部分测试。

### V1（2026-10-19 给出）：MXFP6（E3M2）的量化、打包与反量化

- **为什么**：A1 的舍入与取指数、A2 的打包有求助（见[帮助影响](#条件片段帮助影响)），V1 换一种格式重做这三件事，确认独立掌握。
- **交付**：在 `gpu/triton/lesson10_block_scaled_matmul.py` 中加两个函数：

| 函数 | 输入 | 输出与要求 |
| --- | --- | --- |
| `quantize_mxfp6_e3m2(x)` | 同 `quantize_mxfp4` | `(packed, scales)`：`[R, K * 3 // 4]` 与 `[R, K // 32]` 的 uint8，与 `x` 同设备 |
| `dequantize_mxfp6_e3m2(packed, scales)` | 上面两个张量 | `[R, K]` 的 float32 |

- **格式**：OCP MX v1.0 §5.3.2 表 4 的 E3M2，一个编码 6 位 `S EEE MM`，指数偏置 3，E = 0 为次正规数，没有 Inf 与 NaN；各编码的值以表 4 与规范的
  公式为准。
- **量化规则**：OCP §6.3，块大小 32：X 取“不超过 amax 的最大 2 的幂”除以“E3M2 能表示的最大 2 的幂”，记 X = 2^e，e 截到 [−127, 127]，
  scale 字节 = e + 127；元素 V / X 按就近取偶舍入到 E3M2 的格点（带符号），超过最大值的饱和；全零块的 scale 字节不得为 255；零的符号不作要求。
- **打包**：每行沿 K 看成一条小端位流，第 i 个元素占第 6i 到 6i + 5 位，位流的第 b 位在第 ⌊b / 8⌋ 个字节的第 b mod 8 位（编码的最低位在前）。
  P1 的 FP4 打包是同一规则取 4 位。
- **实现要求**：不调用库现成的 FP6、FP4、E8M0 转换；错误输入抛 `ValueError`（同 `quantize_mxfp4` 的三种）；整张量写法与循环写法均可。
- **验收**：测试 18 项（CPU 层 17 项，GPU 层 1 项：CUDA 上的量化与 CPU 一致）。运行：`-k v1`。
- **求助**：V1 用来确认独立掌握，不提供提示；卡住时说明卡在哪一步，Agent 改用口头解释或另一个小题确认，不直接给写法。

### 测试的扩充（2026-10-19）

测试共 92 项：P1 原有 47 项，O-1 27 项，V1 18 项；O-1 与 V1 各以一项“入口存在”作 expected red，其余在入口缺失时跳过。第三版实现（`269d7ce9`）下本机
CPU 层为 `4 failed, 40 passed, 48 skipped`：两个入口项，另两项是反量化改写引起的回归（R-05）。不进仓库的参考实现为 `82 passed, 10 skipped`，
跳过的 10 项都是 GPU 数值项。17 个故意写错的变体中有 16 个在 CPU 层被对应的测试报红：O-1 的主机端还原成二维、不查块大小、不查 scale 形状、不查
连续性、先发射再检查；V1 的指数偏移写成 −2、平局进位、24 位字内高低倒置、三个字节的顺序倒置、用 float32 的 `log2` 取指数、不截到 −127、饱和到
24、全零块写成 255、反量化把次正规数当正规数、丢符号、按 8 位移位解包。O-1 块内步长写错（c 的步长为 4）只有 GPU 数值项能发现，本机无法验证；
GPU 层没有在本机运行过。

### M1 的脚本与规格（2026-10-19）

脚本 `gpu/triton/lesson10_block_scaled_matmul_benchmark.py` 按上文 M1 的设置实现，学习者在 RTX 5090 上运行：

- **两条路径**：同一个 kernel 源码，只差 A 的 scale 是否传给 `tl.dot_scaled`（`A_SCALED`）；A 的 scale 字节全为 127，两条路径算的是同一个数。
  计时前对每个候选核对编译产物（原生须有 `kind::mxf4nvf4.block_scale`、没有 `ttg.fp4_to_fp`，软件反之）与结果（最多 256 行与 float64 参考比较，
  容差同验收测试），不符即停止、不计时。
- **形状与候选**：N = K = 8192，M = 16 与 8192；两条路径用同一组候选（M = 16 为 10 个 `BLOCK_M = 16` 的配置，M = 8192 为 10 个 64 或 128 见方的
  配置），各取最快。候选均在 101,376 字节以内；本机只编译的核对显示，M = 8192 时 4 个 warp 的 128 × 128 及以上的块两条路径都大量溢出寄存器，
  因此候选以 8 个 warp 与较小的块为主，每条路径都有不溢出的配置。
- **计时**：`do_bench` 中位数（5 ms 预热、50 ms 重复，每次运行前清空 256 MB 缓冲，B 的 34 MB 从显存读而不是从 96 MB 的 L2 读）；15 轮，每轮两条
  路径的先后交替；比值 time(software) / time(native) 在轮内计算，报告中位数与四分位距；另报告达到的 TFLOPS 与“必须搬运的字节”对应的带宽占峰值的比例。
- **判据**（运行前打印）：学习者对每个 M 预测比值的区间；中位数落在区间内为支持，整个四分位距在区间外为否定，其余为证据不足。
- **预测前给出的规格**：见来源表中 RTX Blackwell 白皮书一行；数据量：B 打包 33.6 MB、B 的 scale 2.1 MB，M = 16 时 A 64 KB、输出 0.5 MB，M = 8192
  时 A 33.6 MB、A 的 scale 2.1 MB、fp32 输出 268 MB。
- **核对**：本机没有 GPU，脚本只在 CPU 上用假的发射走通了选择、轮换、统计与判据的流程，`_dequantize` 与 Triton 的 `MXFP4Tensor` 解码一致；
  GPU 上的运行与结果待学习者执行。
- **学习者的预测**（2026-10-20，运行前写定，原样填入 `PREDICTION`）：
  - 平衡点：FP4 为 1676 TFLOPS ÷ 1.75 TB/s = 957.7 FLOP/B，BF16 为 209.5 ÷ 1.75 = 119.7 FLOP/B。
  - M = 16：计算强度 56.5 FLOP/B（字节数按 (33.6 + 2.1 + 0.5) × 1024² + 64 × 1024 计），低于两个平衡点，访存受限。软件路径：设 BF16 矩阵乘的时间为
    T，访存为 119.7 ÷ 56.5 = 2.12T；解码按每个元素 3.5 条指令（沿用综合验收中 MI300X 一题的估计），为 (3.5 ÷ 52.4) ÷ (128 ÷ 104.75) = 0.0547T；
    假设访存与矩阵乘互相掩盖、解码藏进矩阵乘，耗时 2.12T，瓶颈为显存带宽。原生路径：设 FP4 矩阵乘的时间为 Tx，访存为 957.7 ÷ 56.5 = 16.96Tx，
    没有解码，耗时 16.96Tx，瓶颈为显存带宽。假设两条路径的矩阵乘都达到峰值，T = 8Tx，比值 2.12 × 8 ÷ 16.96 ≈ 1.000；考虑随机波动，区间
    [0.99, 1.01]。
  - M = 8192：计算强度 3089.5 FLOP/B（字节数按 (2 × 33.6 + 2 × 2.1 + 268) × 1024² 计），远高于两个平衡点，计算受限。软件路径：访存 0.0387T、
    解码 0.0547T，耗时 T，瓶颈为 BF16 张量核；原生路径：访存 0.31Tx，耗时 Tx，瓶颈为 FP4 张量核。比值 T ÷ Tx = 8；考虑随机波动，区间 [7.8, 8.2]。
- **结果的分析**（2026-10-20，Agent 在本机只编译）：把选中的四个配置编到 sm_120、用 `ptxas-blackwell` 汇编为 sm_120a，统计 K 循环里每个 warp
  每个 K 步的 SASS 指令：M = 16 原生 166 条（8 条 `OMMA`），软件 1842 条（32 条 `HMMA`；查表换算 816 条，即 `PRMT` 480、`LOP3` 192、`SHF` 144，
  每 8 个 FP4 码 17 条；其余 `PRMT` 318 与 `MOV` 115 共 433 条用于重排与搬运，按操作码归类、未逐条核对；B 的 scale 处理 384 条，即 NaN 处理
  `SEL` 256 与乘法 `HMUL2` 128；其他 209 条）；M = 8192 原生 307 条（64 条 `OMMA`），软件 1058 条（64 条 `HMMA`）。TTGIR 显示软件路径在
  `ttg.local_load` 按 dot 操作数布局读出 FP4 字节后就地解码，A、B 都要解码；M = 16 时每个 warp 每个 K 步解码 12,288 个元素、做 65,536 次
  乘加（每个解码出的元素参与 5.3 次），M = 8192 的选中配置为 21 次；按元素平均，查表换算约 2.1 条、重排约 1.1 条，B 的每个元素另有 1.5 条 scale 处理（2026-10-20 更正：原写“每个元素约 3.9 条、B 另加 0.5 条 scale 乘法”，把 B 的 NaN 处理算进了解码）。按 2407 MHz、每个调度器
  每周期发射 1 条、最忙的 SM 估算：M = 16 软件的发射约 24.5 µs，DRAM（最少字节）20.2 µs，两者相加 44.7 µs，实测 45.1 µs；原生的发射约 2.2 µs，
  实测 28.7 µs 对 DRAM 20.2 µs。M = 8192 软件的张量核（峰值）5.25 ms、发射 2.76 ms，实测 6.01 ms；原生的张量核 0.66 ms、发射 0.20 ms、
  DRAM 0.19 ms，三者相加 1.05 ms 仍小于实测 1.38 ms，剩下的部分（等待与流水线空泡、运行时频率与功耗、该指令实际能达到的速率）这次的测量
  分不开。这些都是静态指令数上的估算，没有 profiler 数据。

## 条件片段：帮助影响

| 透露到什么程度 | 影响的验收项或工件 | Agent 是否写了学习者核心工件 |
| --- | --- | --- |
| 2026-10-18：学习者问算出格点值后怎样转成 FP4、两个怎样拼一个字节。给出：值与编码的区别（PyTorch 没有可直接转换的 FP4 类型，编码存在 uint8 里）、E2M1 编码表、编码等于有序格点表的下标（与 IEEE 浮点非负数位模式的单调性同理）、负数加 8；字节布局、C 写法 `lo \| (hi << 4)` 与例子 `[3.0, −0.5] → 0x95`；整数张量逐元素位运算、以步长为 2 的切片分出偶数列与奇数列；解包为 `& 0xF`、`>> 4` 后交错放回；提醒 float32 输入不要降成 bf16（参考实现这样改后 4 项量化测试失败） | A2 的打包与解包：基本给出写法，以 V1 确认 | 否 |
| 2026-10-18：学习者问 e 为什么截到 [−127, 127] 而不是 [−128, 128]。讲解 E8M0 的 256 个编码、bias 127 与 FP32 指数字段对齐、0xFF 留给 NaN（FP4 没有 NaN），截断让 scale 字节落在 0–254，截到 −128 时字节回绕成 255、全零块变成 NaN；提醒反量化时字节 0 应得 2^−127，左移 23 位的写法会得到 0 | 规则约定已写明，属原理讲解；反量化的边界提醒不涉及写法，不影响独立证据 | 否 |
| 2026-10-19：学习者问为什么对 log₂(amax) 向下取整。讲解向下取整即取 amax 的二进制指数（C 的 `ilogb`，硬件上读指数位，`triton_kernels` 的 `bits & 0x7F800000`），以及与向上取整的取舍（附 2^22 个随机数上两种取法的对比，与 `triton_kernels`、NVIDIA MXFP8 论文的选择） | A1“块最大值比 2 的幂小一个 ulp”一项：给出解法方向（直接读指数位），学习者的实现即按位取指数，以 V1 确认 | 否 |
| 2026-10-19：学习者问 scale 是否用 `torch.float8_e8m0fnu`。说明约定与 Triton 都用 uint8，Triton 3.7.1 不接受这一 dtype，PyTorch 的转换按就近舍入、不符合 OCP 的向下取 | 约定已写明，不影响独立证据 | 否 |
| 2026-10-19：学习者问缩放后怎样就近舍入到格点。给出：按档定间距 s（[0, 2) 为 0.5，[2, 4) 为 1，[4, 8) 为 2）、round(\|v\| ÷ s) × s、平局取偶等于倍数 k 取偶（`torch.round` 默认如此）、舍入后再饱和、≤ 0.25 自然变 0，附例子表；说明 Agent 按此思路核对过量化测试 | A1 的舍入：基本给出写法（学习者实现与之相同），以 V1 确认 | 否 |
| 2026-10-19：调试与错误输入。诊断 `torch.pow(2, -e)` 在 int32 里得 0，给出浮点写法，提醒 uint8 的 `scales - 127` 会回绕；说明 5 项失败都要在入口抛 `ValueError`，一维、三维两项可能因元组解包碰巧通过 | A1–A3 的错误输入与 dtype：调试帮助，检查项约定已写明，不影响独立证据 | 否 |
| 2026-10-19：学习者问 kernel 内是否要拆包、偏移是否减半。确认不拆包（`dot_scaled` 文档与教程第 215–231 行）、沿 K 的偏移按字节计、M 与 N 方向不变；其余沿 K 的量与 scale 的系数以提问留给学习者；说明 `rep_m` 只属于五维 scale 的路径，约定的 kernel 读二维 scale | A4、A6：确认方向并指向来源，具体偏移与 A6 的说明留给学习者，不影响独立证据 | 否 |
| 2026-10-19：学习者问 R-04 怎样改成整张量运算。讲了循环与整张量写法的对应：按块 reshape 后沿最后一维求最大值、`[..., None]` 广播 scale、分支改为 `torch.where`、查表改为 `torch.searchsorted` 或以整数张量作下标、奇偶切片打包、`torch.stack` 后 reshape 交错解包，并给出本机计时对照 | R-04（不在约定内）：给出改写方法，不涉及验收项 | 否 |
| 2026-10-19：学习者把量化与反量化都改成整张量写法，反量化结果有误，请 Review。指出量化部分的测试全部通过；反量化中取符号的两行（`low *= -low_sign`、`high *= -high_sign`）在符号位为 0 时乘的是 −0，把正数都变成了 −0，循环版“符号为 1 才取负”在整张量里要按符号位选 1 或 −1；指出这两项失败是 A2 的回归 | R-04（不在约定内）与 R-05（A2 的回归）：指出出错的两行与原因 | 否 |
| 2026-10-20：学习者交了 V1（第四版 `878a2f26`），说结果不对。本机 CPU 层 V1 `11 failed, 6 passed, 1 skipped`。Agent 核对后告知：scale 字节、舍入、平局、饱和都对（随机输入上自己的往返与参考值逐位相同；只把位序换成约定的测试替身下 16 项通过）；问题在打包与解包的位序——第 0 个元素放在第 0 个字节的高位，相当于把 3 个字节看成大端的 24 位数，约定是小端位流、第 0 个元素占最低 6 位，并指出 P1 的 FP4 打包（第 0 个元素在低半字节）就是同一规则；两边用同一种位序，往返测试因此通过；另外 K 不是 32 的倍数时由 `reshape` 抛 `RuntimeError`，一维、三维输入只是碰巧由解包 `M, K = x.shape` 抛出 `ValueError`。没有给写法，留一道手算小题：编码 1、2、3、4 按约定打成的 3 个字节。学习者画图说明位流在每个字节内由最低位走向最高位、第 k 个字节的最高位之后接第 k+1 个字节的最低位，手算 `10000001 00110000 00010000`，正确 | V1：A1 的舍入与取指数为独立证据；A2 的打包只指出步骤与约定，位操作由学习者自己改，以测试与小题确认 | 否 |
| 2026-10-20：学习者对 M1 的首次解释有缺口，并问 M = 8192 的比值为什么低。Agent 指出带宽一列由同一字节数除以时间得到、不能用来解释耗时；说明测量的软件配置没有溢出，溢出只出现在没选中的配置；把 M = 8192 的比值拆成峰值比 × 效率比（8 × 47.6% ÷ 87.3% ≈ 4.4）；给出上述 SASS 指令计数与发射、DRAM、张量核三部分的估算（M = 16 的软件路径两部分都没饱和、相加接近实测，M = 8192 的软件路径把解码藏在 BF16 张量核后面、原生路径有三部分都解释不了的时间）；补上结果支持的部分；并逐步对照了预测的推理：MB 与 TB/s 的单位、每个解码出的元素参与的乘加次数（按 128 算，实际 5.3 与 21，A 也要解码、warp 之间不共享解码结果）、取最大值的重叠假设、两条路径都到峰值的假设 | M1 的解释：缺口部分由 Agent 讲出，以换条件的复查题（W4A16 变式）确认 | 否 |
| 2026-10-20：M1 复查题第 2 问的单位有歧义（出题问题）。Agent 说明线程级条数与 warp 指令的区别及 32 倍的换算（一条 warp 指令让 32 个 lane 各执行一次，类比 SIMD 指令），每个 SM 有 4 个调度器同时发射，学习者的算式只算了 1 个 K 步；用实测的 M = 16 软件路径演示 warp 级记账（12,288 × 3.9 ÷ 32 ≈ 1500 条解码，加 B 的 scale 128 条与其他约 210 条共 1842 条；每个调度器 2 × 16 × 1842 = 58,944 条，÷ 2407 MHz ≈ 24.5 µs）；提醒估算后先与已知实测核对；没有给出 W4A16 变式的正确数字。追问后讲了 12,288 的来历（交换操作数、2 × 2 个 warp、每个 warp 解码自己 MMA 要用的 16 行 B 与 8 行 A）与 3.9 的拆分（Triton 内联 PTX 的查表换算、B 的 NaN 处理、重排） | M1 的复查：以换题（W8A16 变式）确认 | 否 |
| 2026-10-20：W8A16 复查的下限取了较短的一项。Agent 说明两部分完全重叠时总时间等于较长的一项（两件事都要做完，重叠最多把短的藏进长的里，类比两个线程并行后 `join`），完全不重叠时为两者之和；指出取 20 µs 意味着约 3.5 TB/s 的带宽；说明第 3 问的结论应由“下限已超过 28.7 µs”得出 | M1 的下限取法：以小题（显存带宽翻倍的假想卡）确认 | 否 |

## 条件片段：需要跟踪的问题

| ID | 对应验收项或目标 | 严重度 | 状态 | 证据 |
| --- | --- | --- | --- | --- |
| R-01 | 提交前（CI 的 Ruff） | 非阻塞（提交前须修） | 已关闭 | 2026-10-19 Review（实现文件 SHA-256 前缀 `52586b5f`）：`ruff check` 报 4 处，第 288–290 行未使用的 `rep_m`、`rep_n`、`rep_k`（F841），第 308 行 `return` 之后的测试命令注释超过 100 列（E501）；CI 每次 push 都对全仓库运行 `ruff check .`。`ruff format --check` 通过。关闭证据（2026-10-19，第二版 `5ca2a1fb`）：`ruff check` 与 `ruff format --check` 均通过，与首版的差异只有改名、报错信息、删去未用变量与注释，本机 CPU 层 `42 passed, 5 skipped` |
| R-02 | 可选项（kernel 读五维 scale） | 非阻塞 | 已关闭 | `mxfp4_matmul_lernel_5dscale`（第 159–213 行）没有被调用，测试不覆盖。块内三个 `tl.arange(0, 32)`、`tl.arange(0, 4)`、`tl.arange(0, 4)` 都没乘步长，`[32, 4, 4]` 连续存放时应为 16、4、1：本机按它的下标从 `swizzle_scales` 的输出取第一块，与 `scales[:128, :4]` 不同，改成 16、4、1 后相同。它只适用于 128 的倍数的块。删去，或修正后接入测试。第二版（`5ca2a1fb`）把步长改为 16、4、4，最后一维应为 1：按 16、4、4 取数仍与 `scales[:128, :4]` 不同；仍未被调用。关闭证据：第三版（`269d7ce9`）改为 16、4、1，与本机按此下标取数的核对一致；该 kernel 改由可选项 O-1 的测试覆盖 |
| R-03 | A3；代码整洁 | 非阻塞 | 已关闭 | `swizzle_scales` 的报错信息写 “K_32 must be a multiple of 128”，应为 4（第 151 行）；两个 kernel 名拼成 `lernel`（第 160、217、292 行）。关闭证据：第二版报错信息改为 4，kernel 名改为 `mxfp4_matmul_kernel_*` |
| R-04 | 不在约定内（性能） | 非阻塞 | 已关闭 | `quantize_mxfp4`、`dequantize_mxfp4` 在 Python 里逐元素循环并多次调用 `.item()`：本机 CPU 上 64 × 512 的量化用 2.38 秒（约 73 µs／元素），反量化 1.03 秒，照此 4096 × 4096 的量化约 20 分钟；在 CUDA 上每次 `.item()` 都要同步。约定不要求性能，M1 的输入也不经过它，不要求修改。第三版（`269d7ce9`）两者都改成整张量写法：量化部分测试全部通过，反量化见 R-05。关闭证据（2026-10-20，第五版 `6399ca8d`）：已没有逐元素循环与 `.item()`，本机 CPU 上 4096 × 4096 的 `quantize_mxfp4` 用 0.31 秒，`dequantize_mxfp4` 用 0.14 秒 |
| R-05 | A2（回归） | 阻塞 | 已关闭 | 第三版（`269d7ce9`）把反量化改成整张量写法后，本机 CPU 层 `test_dequantize_decodes_any_bytes` 与 `test_round_trip_is_exact_on_representable_values` 失败：取符号的两行在符号位为 0 时乘 −0，正数都变成了 −0。关闭证据（2026-10-20，第四版 `878a2f26`）：改为按符号位选 −1 或 1，本机 CPU 层除 V1 外全部通过（`11 failed, 71 passed, 10 skipped`，失败的 11 项都是 V1） |
| R-06 | 提交前；代码整洁 | 非阻塞 | 已关闭 | 第五版（`6399ca8d`）`mxfp4_matmul_swizzled` 开头的注释（第 306–307 行）把 scale 的形状写成 `[M // 128, K // 128, 32, 32, 4]`，应为 `[..., 32, 4, 4]`；2026-10-20 第一次指出时一并提了 Ruff，学习者改了换行，形状未改。关闭证据（2026-10-20，`95c2840e`）：两行都改为 `32, 4, 4`，这是与 `6399ca8d` 唯一的差别；本机 CPU 层 `82 passed, 10 skipped`，`ruff check` 与 `ruff format --check` 通过 |

## 条件片段：结课

| 目标 | 所需证据 | 证据链接 | 判断 |
| --- | --- | --- | --- |
| O1：从浮点表示到 FP4，块缩放格式与 OCP 的量化规则 | 理解、实践 | E-01、E-02 的节点 1–2 检查与复查；E-06 的综合验收；E-07 的 A1、A2（RTX 5090 上全部测试通过）；E-11 的 V1：MXFP6（E3M2）的量化、打包与反量化 | 充分 |
| O2：scale 放在哪一步，`tl.dot_scaled` 的数据表示与 scale 的 5D 预排布局 | 理解、实践 | E-03 至 E-05 的节点 3–5 检查与复查；E-06 的综合验收；E-07 的 A3–A5；E-08 的 A6；E-11 的可选项 O-1（kernel 读 `swizzle_scales` 的五维输出） | 充分 |
| O3：同一个 `tl.dot_scaled` 在各架构上的落地，原生块缩放比软件换算快多少 | 理解、实证 | 理解：E-05、E-06。实证（M1）：E-12 运行前的可证伪预测；E-13 在 RTX 5090 上的受控测量，方法与判据运行前公布，40 个候选配置在计时前全部通过路径与数值核对，两个 M 的预测都被否定；E-14 至 E-17 的解释与复查，说明了结果支持什么（两种 M 下原生都更快，计算受限时的优势远大于访存受限时，M = 8192 时软件路径的解码藏在 BF16 张量核后面）、不支持什么与剩余的不确定（M = 8192 原生路径约 0.33 ms 分不出来源）。性能结论另有 A4 的数值正确性证据 | 充分 |

- **未关闭的阻塞问题**：0。R-01 至 R-06 均已关闭，其中阻塞的 R-05 已关闭，见[需要跟踪的问题](#条件片段需要跟踪的问题)。
- **帮助影响是否已恢复**：已恢复，Agent 没有写学习者的核心工件，见[帮助影响](#条件片段帮助影响)。A1 的舍入与取指数、A2 的打包有求助，由 E-11 的
  V1 独立恢复；V1 中位序的问题只指出步骤与约定，位操作由学习者自己改，并以手算小题确认。M1 的解释中由 Agent 讲出的部分，由 E-15 至 E-17 的换条件
  复查恢复（W4A16 的解码量与复用次数；W8A16 的发射时间、上下限与限制资源；显存带宽翻倍后的下限与限制资源）。E-15 第 2 问的错误主要来自出题：线程级
  与 warp 级的条数没有写明换算，调度器个数只是隐含，3.9 是 A、B 的平均且把 B 的 NaN 处理算进了解码；这些不记为学习者的差距。
- **非阻塞余项**：M = 8192 原生路径实测 1.38 ms，比张量核、发射、显存三部分相加的 1.05 ms 多约 0.33 ms，来源这次分不开，可用 Nsight Compute 看
  张量核的忙碌比例与 warp 停顿原因、运行时记录频率与功耗、单测 `OMMA` 的小 kernel 来分辨，运行时的 SM 频率也没有记录；发射时间都按静态 SASS 计数与
  “每个调度器每周期发射 1 条”估算，没有 profiler 数据；W4A16、W8A16 变式只编译未运行，约定里“顺带测 W4A16”的可选项没有做；M1 只在一台 RTX 5090
  上测量，每个形状各取最快的一组候选配置；sm_100 实机、与 cuBLAS 的对比和 autotune 属约定的非目标；练习文件在结课时尚未提交（实现与 benchmark 未被跟踪，
  测试文件有改动），2026-10-21 与本课记录一起提交。以上都不在本课门槛内。
- **学习者确认**：2026-10-20，学习者回复“确认结课。这是triton系列课程的最后一课了。”
- **结课结论**：学习者能从统一的浮点模型（符号、带偏置的指数、尾数与隐含位、次正规数、特殊值）讲到 FP8、FP6、FP4 每少一位丢掉什么，讲清块缩放
  格式的设计：沿 K 每 V 个元素共享一个 scale，MXFP8、MXFP4、NVFP4 的元素类型、块大小与 scale 类型的取舍，OCP 的量化规则下何时饱和、何时变 0；
  能说明 scale 可以放在乘之前、部分和之后或 MMA 指令内部，取决于 scale 沿哪个下标变化，讲清 `tl.dot_scaled` 的形状语义、FP4 按字节推进的偏移，
  以及 scale 的 5D 预排布局为什么让每个 K 步的读取连续、kernel 里的 reshape 与 trans 为什么不搬数据，并能对没讲过的块形状推出 rep 与描述符的块形状；
  能说明同一个 `tl.dot_scaled` 在 sm_100、sm_120、没有原生支持的 NVIDIA 架构与 AMD 的 CDNA3、CDNA4 上各落成什么、scale 放在哪里、代价在哪里。
  独立实现了 MXFP4 的量化、打包、反量化、scale 预排与块缩放矩阵乘 kernel（含读五维 scale 的可选项），在 RTX 5090 上通过全部 92 项测试，并独立完成
  MXFP6（E3M2）的变式。对“原生块缩放比软件换算快多少”作出可证伪的预测，经 RTX 5090 上的受控测量，两个 M 的预测都被否定（软件 ÷ 原生：M = 16
  为 1.57，M = 8192 为 4.37）；能用 SASS 指令计数估算发射、显存与张量核三部分的时间，把 M = 8192 的比值拆成峰值比与效率比，说明 M = 16 时软件
  路径既没到带宽上限也没到算力上限、两部分重叠很差，并在换条件的变式中正确算出解码量与复用次数、发射时间、总时间的上下限与限制资源。本结论的范围
  是 Triton v3.7.1、NVIDIA 后端 sm_89、sm_90、sm_100、sm_120 与 AMD gfx942、gfx950 的只编译观察，以及一台 RTX 5090（sm_120，驱动 595.71.05，
  CUDA 13.0，torch 2.13.0+cu130）上的数值验收与测量；sm_100 没有实机运行。
