# 学习记录 · 2026-09-24 · Fused Attention 全貌补充与 FP16 前向实践

> 来源：codex:01a0bcfa（完整会话 ID：`01a0bcfa-1045-7650-84c5-c9674e06ad62`），2026-09-20—24。
> 消息边界：`msg-a104eec606d45cc6091c` → `msg-1c89b0306b8b17cd5728`，共 120 条可见消息。
> Source SHA-256：`88939e435da4a52edc98baa4f397fc5d88a258d90c780f2e8e4d60218fc43075`。
> 关联：[第 06 课](../lessons/06-fused-attention.md)、[此前学习记录](2026-09-19-fused-attention.md)。完整教学和实践契约见 Lesson；本记录保留本轮追问、理解变化及可独立复习的最小结论，不代替课程状态或知识权威。
> 可追溯对话：[同名原文](../logs-raw/2026-09-24-fused-attention.md)。
> 源码锚点：[官方本地快照](../../triton-tutorials/official/06-fused-attention.py)，本次只读核验 SHA-256：`5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317`。下文 FP8 V 的上游修订单独注明，不将旧快照与修订混为同一实现。
> 证据边界：从指定 extract 蒸馏；外部文档和修订是当时答复引用的来源，本次未重新运行示例或 GPU 测试。GPU 结果仅来自用户远端实测报告及当时对保存记录的核对摘要。

## 全貌、符号与精度

- [转折] 为什么重新补充全貌？——用户指出“我虽然跟着学完了，但依旧对算子整体全流程依旧比较模糊”，要求先说明输入输出、未分块数学与精度、program 分工、kernel 间传参以及保存量的反向用途，再逐点展开。助手承认局部题答对不能证明全流程已建立，改为先补全貌、读源码，再完成既有实践；Skill 优化放在实践之后。（来源：`msg-a104eec606d45cc6091c`、`msg-b75e660c017772b11ec2`。）

- [要点] 这份 Attention 的完整数学和接口边界是什么？——Q/K/V 已由调用方准备；FP16 路径中三者和 O 均为 `[B,H,N,D]`，每个 head 计算 `S=sQKᵀ`、`P=softmax_key(S)`、`O=PV`。S/P 的逻辑 shape 为 `[N,N]`，causal 允许 `j≤i`；线性投影和多头输出投影不在该算子内。官方接口只返回 O，通过 ctx 保存 Q/K/V/O/M；练习接口额外返回 FP32 `[B,H,N]` 的 M，便于验收。（来源：`msg-b75e660c017772b11ec2`；完整说明见 [Lesson](../lessons/06-fused-attention.md)。）

- [要点] 前向和反向各阶段传递什么？——前向 `_attn_fwd` 内调用 `_attn_fwd_inner`，后者是 JIT 辅助函数，不是另一次 launch。反向先由 `_attn_bwd_preprocess` 用 O/dO 写出 Delta，再由 `_attn_bwd` 读取 Q、预缩放 K、V、M、dO、Delta，写出 dQ/dK/dV；wrapper 还用 PyTorch 预缩放 K，所以“两次 Triton kernel 启动”不等于整个反向只有两次 GPU 操作。（来源：`msg-f59e34007bbb0c352293`、`msg-b75e660c017772b11ec2`、`msg-d08c6e56bcea3186b119`。）

- [转折] 为什么先用符号而不是相等的数字维度？——用户提出“常规情况下，我有能力理解通用公式”，并指出 `acc=[64,64]` 容易让人误以为是 `[BLOCK_M,BLOCK_M]`。本轮因此改为符号先行：Q 为 `[BLOCK_M,D]`，K/V 为 `[BLOCK_N,D]`，score 为 `[BLOCK_M,BLOCK_N]`，`acc/O` 为 `[BLOCK_M,D]`，`m/l/M` 为 `[BLOCK_M]`；`pV` 归约 key 轴，保留 query 和特征轴。（来源：`msg-6c5d822c69ff241119f1`、`msg-fdcc4b0b7595e2a475e5`。）

- [要点] 一个前向 program 负责什么，grid 尾部的 1 是什么？——grid 为 `(ceil(N/BLOCK_M),B*H,1)`；一个 program 固定一个 batch/head 的 Q tile，扫描所需 K/V 块，独占写出对应 O/M。第三轴大小为 1 且本实现未使用，可省略；grid 轴的语义来自 kernel 怎样使用 `program_id`，不是预设的 Q/batch/head 名称。用户的追问是“最后一个1是什么？为什么要多出一个1来？”（来源：`msg-b75e660c017772b11ec2`、`msg-335ddeaa1dc243ea2411`、`msg-6733776e878f0b81bdbc`。）

- [要点] FP16 前向的低精度操作数与高精度状态怎样连接？——Q/K/V 为 FP16；QKᵀ 使用 FP16 操作数、FP32 累加与 score；缩放、指数和 `m/l/acc` 为 FP32。局部指数权重先以 FP32 求分母，再转成 FP16 参与 pV，累计到 FP32 acc；最终 O 转回 FP16，M 保留 FP32。因此既有最终写回转换，也有第二次矩阵乘前的转换。（来源：`msg-b75e660c017772b11ec2`、`msg-1f6d846f1d21a27442fa`、`msg-cdbe6b60d1b566c84719`。）

- [高价值问题] “对于其他大多数深度学习算子也都是这样吗？”——不能从本课推广出“内部默认全为 FP32”，也不能从输出 dtype 推断操作数或累加精度。用户继而问“没有一个相对通用的设置逻辑？”；得到的判断方法是：先确定误差和数值范围，识别指数、归约等敏感环节，再决定低精度存储/计算及转换位置，最后分别验证数值与性能。通用的是判断方法，不是固定 dtype 配方。（来源：`msg-1f6d846f1d21a27442fa`、`msg-cdbe6b60d1b566c84719`、`msg-44b5696cf4d8152c1059`、`msg-01f37a08847a0f041ff1`。）

- [要点] 用 M 恢复概率时为什么仍然稳定？——用户问“指数部分就没有减去最大值的操作了，那么计算中会不会出现溢出呢？”令 `x=S/ln2`，前向稳定计算 `m=max(x)`、`l=Σ2^(x−m)`，保存 `M=m+log2(l)`；于是 `2^(x−M)=2^(x−m)/l`，同时完成减最大值和归一化。对一致、有限的有效 score，`M≥m≥x`，指数不大于 0。反向从 M 读出的局部变量 `m` 是 log-sum-exp，不再是行最大值；因果无效位置可能先取指数再置零，不受这个有效位置范围证明保护，浮点下仍可能舍入或下溢。（来源：`msg-2d54c0e8c6483ded56bb`、`msg-66c364988a3eecd24aa0`。）

## TensorDescriptor、边界与启动准备

- [要点] descriptor 的 shape、stride、block_shape 与 load 起点分别是什么？——descriptor 描述已有存储，创建时不读取整张量。连续 Q `[B,H,N,D]` 可用二维视图 `[BHN,D]`、元素 stride `[D,1]` 表示；program 的全局行起点为 `(bH+h)N+p_m*BLOCK_M`。`load([r0,0])` 给块起点，`block_shape=[BLOCK_M,D]` 给块大小。用户正确回答，起点加 `BLOCK_M` 后读取下一个视图块，“返回shape保持不变”。（来源：`msg-b0bc4271a0557eb2f470`、`msg-0083a4e279efbfd78420`、`msg-72dffca88fa5fea6f95a`。）

- [要点] descriptor 的越界处理为什么不能代替 head 边界？——用户追问“会自动处理越界整个访问视图时的mask吗？”本轮核对的默认 load 越过声明视图时补零、tile shape 不变，但 `[BHN,D]` 只知道整个视图边界；跨过当前 head 而仍在该视图内，会读取下一 head，不会自动补零。逻辑 head 边界必须由访问坐标和范围保证。（来源：`msg-0083a4e279efbfd78420`、`msg-72dffca88fa5fea6f95a`。）

- [要点] K/V 补零为什么不能消除无效 key 的 softmax 贡献？——零 K 的点积为零，指数权重仍可为 `exp(0)=1`；V 补零也不能消除分母里的这一项。无效 key 应在 score 上屏蔽，causal 的 `j≤i` 同样是逻辑规则，不由 descriptor 的合法地址判断代办。（来源：`msg-72dffca88fa5fea6f95a`、`msg-836c6aace3ce9491216f`。）

- [高价值问题] “可以指定越界补什么值吗？类似于tl.load里的other参数。”——当时核对的接口提供预设 `zero` 和浮点 `nan`，不是任意 `other`；host 参数为 `padding`，device 参数为 `padding_option`。需要其他值时可加载后按有效条件替换或采用普通带 mask 的 load。Attention 应屏蔽无效 score，不能把 K/V 填成 `-inf` 来代替。（来源：`msg-516f563c941e8cbce5c6`、`msg-836c6aace3ce9491216f`。）

- [要点] host/device descriptor 路径为什么都需要匹配本次 tile 配置？——host 构造传 descriptor，device 路径传指针并在 kernel 内构造；数据仍在 GPU 上。host 的 `dummy_block=[1,1]` 由候选配置的 pre-hook 改成 Q/O 的 `[BLOCK_M,D]`、K/V 的 `[BLOCK_N,D]`。用户正确判断 `_maybe_make_tensor_desc` 遇到已有 descriptor 就原样返回，不会用传入的 `block_shape` 重写它；因此 pre-hook、grid 与 kernel 内形状必须使用同一配置。（来源：`msg-2b19365f64e94d8b03f5`、`msg-27e48242434a6a99b757`、`msg-bf0bff668be426aaca39`。）

- [要点] TMA descriptor 的基础布局条件怎样检查？——本轮讨论的 NVIDIA TMA 路径要求数据基址 16 字节对齐、末维 stride 为 1、其余维度的字节 stride 为 16 的倍数；descriptor 的 stride 参数仍以元素为单位。FP16 `[T,D]` 的行跨度为 `2D` 字节，因此行跨度条件要求 D 为 8 的倍数，但这不足以证明整个 kernel、块形状或 dot 合法。用户正确判断转置视图 `[D,T]`、stride `[1,D]` 在 `D>1` 时末维不连续。（来源：`msg-bf0bff668be426aaca39`、`msg-04ca23e84e37a19b752e`。）

- [高价值问题] “基址16字节对齐这一项该怎么判断呢？”——检查 `tensor.data_ptr()%16==0`。对齐存储 A 上偏移 s 个、每个 e 字节的元素后，视图仍对齐须满足 `s*e%16==0`；FP16 对应 s 为 8 的倍数。连续性与基址对齐独立：`x[1:]` 可连续却不再 16 字节对齐；它已连续时 `.contiguous()` 可能原样返回，不能保证通过重新分配修复对齐。（来源：`msg-04ca23e84e37a19b752e`、`msg-33837eb447872551cd17`。）

- [要点] descriptor/TMA 提供什么能力，不能直接证明什么？——规则矩形块访问可由支持硬件上的 TMA 处理多维搬运、寻址及越界填充，为访存与计算重叠提供条件；这不是必然快于普通 `tl.load` 的保证。`desc.load` 返回计算用的 `tl.tensor`，不能仅凭这一行推断底层始终在某种片上存储中；构造成本、块配置、编译结果和设备都影响实际收益。（来源：`msg-bf0bff668be426aaca39`。）

- [要点] `set_allocator` 与 `torch.empty(...,int8)` 各在做什么？——用户正确回答“还未申请缓冲区，实际申请发生在启动一个需要额外工作缓冲区的kernel时”。注册只是登记 host 回调；`size` 是字节数，int8 张量充当 GPU 字节工作区，不表示 Attention 使用 INT8 量化，也不负责创建 Q/K/V。`align` 约束工作区地址，与输入数据基址的 16 字节条件不是同一对象；示例忽略该参数不等于任何场景均可忽略。（来源：`msg-f523e3590829df0fe2d4`、`msg-cce601dde28a72fb2f00`、`msg-00c7a7ac7f8a8c33011c`。）

## 前向在线状态与源码语义

- [要点] `m=-inf,l=1,acc=0` 为什么不会多出一份分母？——首个有效且有限的块令新最大值有限，`alpha=2^(−inf−m_new)=0`，因此初始 l 被消去。用户正确指出，若 m 改成 0 且首块 score 都小于 0，则 alpha 为 1、初始 l 会残留；继而追问“直接设置初始0不行吗？”在原 m 初始化及上述有效输入条件下，l 初始为 0 或 1 的首块结果相同，1 不是保证分母非零所必需。（来源：`msg-00c7a7ac7f8a8c33011c`、`msg-e46c2cf99f4e5d53804e`、`msg-f2c2239b8dd418ae124b`。）

- [高价值问题] “可能写成1就是为了处理出现异常inf值的score的情况？”——这是用户提出的待验证猜想；代码行为不支持它。首块含 `+inf` 会出现 `inf−inf=NaN`，全为 `−inf` 也会产生无效减法，l 初始为 0 或 1 都不能修复，`NaN*0` 仍是 NaN。有限有效值与部分被 mask 的 `−inf` 可以正常共存；不能凭源码中的 1 虚构作者动机。（来源：`msg-418706f2766ba7ffb94c`、`msg-7892d9c482fc31819e0a`。）

- [要点] causal 的两段扫描怎样接续同一状态？——固定 Q 区间 `[a,b)`，过去 key `[0,a)` 全有效，对角 `[a,b)` 检查 `j≤i`，未来 `[b,N)` 跳过。旧快照外层 STAGE 是位掩码：causal 为 3、non-causal 为 1；inner 的 1/2/3 分别表示过去/对角/全序列，两个“3”语义不同。causal 两次 inner 调用共享 `m/l/acc`；用户正确回答首个 Q tile 的过去区为空，“真正的数据处理从第二段开始”。（来源：`msg-34cb71f9164a10032eb4`、`msg-acf699b52fca2d72c451`、`msg-14692456ca81a7c214b2`。）

- [要点] K tile 的 `.T` 和 `multiple_of` 应怎样读？——`desc_k.load(...).T` 转置的是已经加载的 tile，将 `[BLOCK_N,D]` 变为 `[D,BLOCK_N]`，不等于把全局 K descriptor 改成不连续的转置视图。`tl.multiple_of(start_n,BLOCK_N)` 向编译器声明整除事实，不会取整或修复索引；事实必须由循环起点与步长保证。`start_m` 是 Q 块编号，`start_n` 是 head 内 token 起点，不能混用单位。（来源：`msg-34cb71f9164a10032eb4`、`msg-14692456ca81a7c214b2`。）

- [要点] 在线合并必须共同维护什么不变量？——在 base-2 score `x=sQKᵀ/ln2` 下，`m'=max(m,rowmax(x_new))`、`alpha=2^(m−m')`、`p=2^(x_new−m')`，然后 `l'=alpha*l+rowsum(p)`、`acc'=alpha[:,None]*acc+pV`。分子和分母必须同时转到新最大值基准；用户正确回答当前块最大值更小时 alpha 为 1，可直接相加。计算 alpha 时必须保留旧 m，不能先覆盖；最后才计算 `O=acc/l`、`M=m+log2(l)`。（来源：`msg-14692456ca81a7c214b2`、`msg-f577814dcdb570e2a8fe`、`msg-c6ea4ed9da8962a4ba66`。）

- [要点] 把分母求和移到 p 转为 FP16 之后，FP32 累加能保证结果相同吗？——用户正确解释“前一步转fp16导致的精度损失已经产生了，后续fp32累加无法弥补”。因此源码先对 FP32 p 归约分母，再把 p 转为 FP16 做 pV；两路实际使用的权重精度不同。前向内层 p 是未归一化指数权重，反向根据完整 M 重建的 p 才是归一化概率。（来源：`msg-c6ea4ed9da8962a4ba66`、`msg-472b950867449a4b8e53`、`msg-339c3d85e49aee24d7f2`、`msg-47aac13aa1f7701ffc6a`。）

- [要点] 公式中的 causal `−inf` 与旧快照实际写法完全相同吗？——旧前向对无效 score 加 `−1e6`，而非直接替换为负无穷；在常规 score 量级下指数会下溢为零，但不保证任意极端输入下严格等价。无 mask 分支先求原始点积的行最大值再乘缩放，使用了本课 `sm_scale>0` 的条件。（来源：`msg-14692456ca81a7c214b2`。）

## 反向统计量、归约与缩放

- [要点] Delta 为什么沿 D 归约，且可在不同 key 块间复用？——`Delta_i=Σ_d O_id*dO_id=Σ_j P_ij*dP_ij`，所以用保存的 O 和 dO 即可计算 softmax 反向的逐 query 统计量，不必为此物化整行 P/dP。Delta 为 FP32 `[B,H,N]`；完整梯度链为 `dP=dOVᵀ`、`dS_ij=P_ij(dP_ij−Delta_i)`、`dV=PᵀdO`、`dK=s dSᵀQ`、`dQ=s dSK`，其中 `S=sQKᵀ`。用户正确回答“不需要，delta的值已经再预处理kernel中全部算好了”；它只随 query 行变化，M 用于恢复 P，Delta 用于得到 dS。（来源：`msg-b75e660c017772b11ec2`、`msg-339c3d85e49aee24d7f2`、`msg-65d7ceda7b267a002c48`、`msg-947121821f093a4a0614`。）

- [要点] 反向输出所有权怎样决定归约方向和 atomic 需求？——dQ 固定 query、沿 key 累加；dK/dV 固定 key/value、沿 query 累加。本实现一个 program 算齐其输出块的全部贡献，其他 program 写不同块，所以无需 atomic。causal 中固定 query `[a,b)` 依赖此前 key，固定 key `[a,b)` 则依赖同区及后续 query；二者扫描方向不能照搬。（来源：`msg-947121821f093a4a0614`。）

- [转折] 两个 program 分别算半份 dK 时，问题只是写回顺序吗？——用户正确指出“如果一个program正在写回时，另一个program也发起了写回，最终写回的值就无法确定了”。助手补充：即使强制有序，普通 store 仍是覆盖，不会得到 A+B。改为互不重叠的临时缓冲区后，用户回答“还缺少将二者的结果综合求和起来”；消除写冲突与完成归约是两件事。这是对正确判断的补全，不是将原答复判错。（来源：`msg-b17a0b0712e248ab1662`、`msg-0e5e2be80f95f8730350`、`msg-caabded3a8fc33e6a50d`、`msg-47aac13aa1f7701ffc6a`。）

- [要点] M 和 Delta 的广播方向为什么随概率布局改变？——dK/dV 使用 `[B_k,B_q]` 的转置概率块，query 在列，因此是 `M[None,:]`、`Delta[None,:]`；dQ 使用 `[B_q,B_k]`，query 在行，因此是 `M[:,None]`、`Delta[:,None]`。用户正确选择后者；准确含义是保留逐 query 的对应关系，沿 key 轴广播。源码参数 D 可能指 Delta 指针，特征维则叫 HEAD_DIM。（来源：`msg-47aac13aa1f7701ffc6a`、`msg-6d423825b1a4b81c1a98`、`msg-46128a88a6884452ce64`。）

- [要点] 为什么 dQ 写回前乘 ln2，dK 却乘 sm_scale？——wrapper 先生成 `K_tilde=(s/ln2)K`。源码 ds 表示自然指数 score `S=sQKᵀ` 的梯度；dQ 临时量 `Σds*K_tilde` 已含 s、多出 `1/ln2`，所以末尾乘 ln2；dK 用原始 Q 累加 `ΣdsᵀQ`，末尾乘 s；dV 不需要这两项缩放。用户正确回答漏掉 `dq*=LN2` 会得到正确 dQ 的 `1/LN2` 倍。（来源：`msg-47aac13aa1f7701ffc6a`、`msg-46128a88a6884452ce64`、`msg-2414585ada8d65c6e257`。）

- [要点] 源码注释称 Delta 已除以 `ds_scale`，应据此额外缩放吗？——不应。该版本预处理实际只计算 `sum(O*dO)`，wrapper 也没有执行对应除法，应按实际数据流解释 Delta，不能让过时注释覆盖实现。（来源：`msg-47aac13aa1f7701ffc6a`。）

- [要点] `BLK_SLICE_FACTOR` 改变什么，反向末块怎样保证不漏贡献？——它把需要 mask 的对角区域扫描步长由 `R_q/R_k` 分别减为 `R_q/F`、`R_k/F`，固定输出块和因果关系不变。dK/dV 扫描对角 query `[a,b)` 与后续 `[b,N)`；dQ 扫描对角 key `[a,b)` 与过去 `[0,a)`。用户正确回答最后 key 块 `b=N` 时后续区循环为 0；更早 query 不能访问未来 key，因此只算对角仍覆盖全部有效贡献。（来源：`msg-f45fa05b7934c009ec41`、`msg-715c8d5339cd39d2495e`、`msg-6dfe616ceceb9b7c643c`。）

## FP8、布局与执行配置

- [要点] E5M2 的指数范围与精度为什么要分开看？——`torch.float8_e5m2` 对应 `tl.float8e5`：1 位符号、5 位指数、2 位显式小数；FP16 为 1/5/10。正规数同一指数 e 下，相邻间距为 `2^(e−p)`，所以 E5M2 间距是 FP16 的 `2^8=256` 倍。用户原答“间距是2^(-2)/2^(-10)=2^8倍”正确；同样的指数位数不意味着同样的表示精度。（来源：`msg-6dfe616ceceb9b7c643c`、`msg-78a86abe81b15e04eec3`、`msg-c9b9e5a87e2f35f95569`。）

- [要点] FP8 分支改变哪些 dtype，保留哪些高精度状态？——调用方先把 Q/K/V 转为 E5M2；`FP8_OUTPUT` 不会自动转换这些输入。该分支的矩阵乘操作数、p 转换及最终 O 使用 FP8，score、`m/l/acc` 和保存的 M 仍为 FP32。减少存储字节数和使用硬件 FP8 运算只是潜在收益；该教程正确性测试明确跳过 FP8 反向，不应把 FP16 反向理解成已支持 FP8。（来源：`msg-6dfe616ceceb9b7c643c`。）

- [要点] 为什么 `permute → contiguous → 逆permute` 能保留 shape 却改变 V 布局？——中间 contiguous 按 `[B,H,D,N]` 的轴顺序复制；恢复逻辑 `[B,H,N,D]` 后最后两维 stride 为 `[1,N]`，元素偏移由 `gND+nD+d` 改为 `gND+dN+n`。用户正确判断，删掉中间复制、只做互逆 permute 不改变布局；助手补充必须同时看 stride，不能仅凭 shape 相同判断。重排适配本教程 FP8 矩阵乘路径，后续 dtype 转换与布局变化是不同操作。（来源：`msg-c9b9e5a87e2f35f95569`、`msg-1eda1290409de74a6b50`、`msg-6f435fe3c11cc0315619`。）

- [要点] FP8 V 的正确二维 descriptor 如何与物理布局对应？——对上述布局，可描述为 `[BHD,N]`、stride `[N,1]`、block `[D,BLOCK_N]`，从 `[gD,n0]` 读取后转置为 `[BLOCK_N,D]`；元素地址 `(gD+d)N+n` 与 `gND+dN+n` 一致。descriptor 最后一维是 token，因而连续，即使 PyTorch 逻辑 V 的最后一维 stride 为 N，也不矛盾。（来源：`msg-c9b9e5a87e2f35f95569`。）

- [转折] 旧 FP8 V 坐标为何不能当作正确范式？——当时助手报告：旧快照采用 `[D,BHN]` 与起点 `[0,gND+n0]`，可能线性地址看似合理却越过 descriptor 声明的列边界；上游修订改为 `[BHD,N]` 与 `[gD,n0]`。答复明确引用 [修复 commit dc3101b3a6fe03f20fa7384c4d312ee17f160415](https://github.com/triton-lang/triton/commit/dc3101b3a6fe03f20fa7384c4d312ee17f160415)，并报告加入多 batch/head 回归测试。本记录可确认的是当时的源码对照、静态坐标核验与引用；该轮没有 GPU，也未运行 FP8 kernel。这不是用户认知错误或 FP8 实践验收。（来源：`msg-362612ca502df02735c1`、`msg-c9b9e5a87e2f35f95569`。）

- [要点] warp specialization 与 acc 拆半重标定分别改变什么？——前者请求不同 warp 分担搬运、矩阵乘或向量计算，不改变 program 的输出所有权；可能增加同步和资源成本。特殊 acc 分支把 `[R,D]` 拆成两份 `[R,D/2]`，各乘同一逐 query 的 alpha，再逆变换，数学上仍是 `acc'[i,d]=alpha_i*acc[i,d]`。用户正确回答后半特征进入 `acc1`，列索引为 `d−D/2`；局部变量 BN 在这里是 D，不是 BLOCK_N，该条件也不是 FP8 专属。Triton 内部张量变换不能直接照搬 PyTorch view 的零搬运判断，更不能凭源码推断性能收益。（来源：`msg-6f435fe3c11cc0315619`、`msg-b9880cb2f64d9672841d`、`msg-6c6c6259b487526046c1`。）

- [要点] tile、warp、流水线和寄存器限制各管什么？——BLOCK_M 决定输出 query 块并影响 grid，BLOCK_N 决定每轮 K/V 块和扫描次数；num_warps 是 program 内资源配置，num_stages 是软件流水线深度，maxnreg 是每线程寄存器上限。用户正确回答仅把 num_warps 从 4 改为 8，“program数量不会翻倍”；自动 warp specialization 还可能增加专门的 warp。num_stages 不等于 causal 的 STAGE，资源参数也不是越大越好。（来源：`msg-6c6c6259b487526046c1`、`msg-3e78255323170003e0d5`、`msg-85ed2e7ba06037f534c5`。）

- [要点] autotune 为什么先筛选配置，又需要 pre-hook？——旧快照先按设备筛选，再按输入筛选 `BLOCK_M≤N_CTX`、causal 下 `BLOCK_M≥BLOCK_N`，并有 `BLOCK_N≤HEAD_DIM` 的编译断言；其候选为 2 的幂，因而相关块边界整除。之后测量多个候选，pre-hook 令 descriptor block_shape 与每次 grid/kernel 配置一致。显式 key 为 N_CTX、HEAD_DIM、FP8_OUTPUT、warp_specialize；调优会重复启动 kernel。检测到 PYTEST_VERSION 时采用固定配置，测试通过不能证明性能最优。（来源：`msg-6c6c6259b487526046c1`。）

## 正确性与 benchmark 边界

- [要点] 比较两套反向结果必须固定什么，为什么清空 `.grad`？——Q/K/V、causal、scale 及上游 dO 都须一致；`backward(dout)` 可理解为对固定 dout 的 `L=ΣO*dout` 求导。用户正确指出不同 dout 意味着“输入参数都不一致”，不能直接将梯度差异归因于 kernel。保存参考梯度后清空 `.grad`，是因为后续 backward 会累计叶子梯度。（来源：`msg-85ed2e7ba06037f534c5`、`msg-292c7d2074383a9bcd65`、`msg-40cd38fab24d60347943`。）

- [要点] 官方测试的路径和容差能支持多大范围的结论？——FP16 backward 测试已经比较 O，因此单独 FP16 forward 跳过不等于没有前向验证；FP8 只比较前向。旧 FP8 参考在输入量化前计算，误差含输入、中间和输出量化，最终转回 FP16不会恢复精度；旧快照 `atol=3,rtol=0` 较宽松，不替代 descriptor 索引检查。官方 FP16 参考也并非全程 FP32 张量；本次练习另用输入的 FP32 转换构造参考，并验证 O/M、接口和输入不变性。（来源：`msg-85ed2e7ba06037f534c5`。）

- [要点] 前后向 benchmark 各计时哪一段？——前向计时调用 attention，随机生成输入、FP8 转换和 V 布局准备在外。反向先建立 O/图，再计时 `o.backward(do,retain_graph=True)`，不在每次重复完整前向；范围包括预缩放 K、Delta 预处理、主反向及相关 autograd 工作。未逐轮清空梯度时累计也可能影响计时，所以它不是单独 `_attn_bwd` 的耗时。（来源：`msg-40cd38fab24d60347943`。）

- [要点] benchmark 的 2.5 系数和 TFLOPS 应怎样解释？——按乘加计两次 FLOP，前向主要矩阵乘估算为 `4BHN²D`，causal 乘 0.5 是近似；反向用五次主要矩阵乘相对前向两次得到 2.5，但本实现的不同梯度路径还会重复重算，故不是逐指令实际 FLOP 统计。报告 `TFLOPS=F*10^-12/(ms*10^-3)`。用户正确回答“2.5的倍数是对计算量的估计，并不是耗时的统计和预测”；耗时需实测。（来源：`msg-40cd38fab24d60347943`、`msg-56b6606fee10958d5fd3`、`msg-9419c8fbf2df52144e93`。）

- [要点] 为什么图例 `triton-fp8` 不能证明 FP8 backward 已支持？——旧 benchmark 只在 `mode==fwd` 且 provider 含 fp8 时转换输入；bwd 即使使用该名称，实际仍是 FP16。必须核对执行分支、dtype、计时范围及 FLOP 模型，而非只看曲线标签。（来源：`msg-40cd38fab24d60347943`。）

## 实践修改与 A4 独立解释

- [转折] 从源码学习怎样进入实践？——用户选择“先在当前仓库编写，稍后到 GPU 机器验证”，继而提交“我编写好了核心实现。目前还没有去GPU机器上测试验证”。本次仍是既有 FP16 前向范围；测试补上契约原本要求的 M 连续性断言。以下实现问题依据当时 review 报告整理，代码片段不是用户口头答复，也不冒充本次重新检查代码所得。（来源：`msg-3e4d0b7926a71a1380ca`、`msg-d08c6e56bcea3186b119`、`msg-0ffef56e5a47924a07a7`、`msg-91cb16a60494c5bb73d0`。）

- [要点] 实践中的 descriptor 和内层调用边界出了什么问题？——首轮 review 指出 `stride=` 应为 `strides=`；形参 `score_max,l,acc,sm_scale` 被传成 `sm_scale,score_max,l,acc`；三次 inner 调用未接收返回的 `(acc,l,score_max)`。后两项会使状态含义/shape 错位，或让 causal 两段无法接续；内层重新赋值不会自动更新外层变量。用户修改后，二轮复核确认三项修正。（来源：`msg-91cb16a60494c5bb73d0`、`msg-e6f6916071feebb017f6`、`msg-930b8cc368276fb0119c`。）

- [要点] 实践中的初值和编译期条件如何影响正确性？——当时实现的 `0-float("-inf")` 实为 `+inf`，会使首次重标定出现 `inf−inf`；用于 `tl.zeros([BLOCK_M,D])` 的 D 未声明为编译期常量；`tl.log(2)` 使用了不合适的整数输入类型。二轮复核确认这些修改完成。读数学含义之外，还要核对表达式符号、Triton shape 的编译期要求与实际参数 dtype。（来源：`msg-91cb16a60494c5bb73d0`、`msg-930b8cc368276fb0119c`。）

- [要点] 实践中的 PV 为什么需要同时核对类型与块大小？——首轮 FP32 指数权重与 FP16 V 的 dot 操作数不同型；当时 `BLOCK_N=8` 也使 `[16,8]@[8,64]` 的归约维小于所核对 Triton 3.7.1 NVIDIA 后端要求的 16。修正精度转换并改为 `BLOCK_M=32,BLOCK_N=16` 后通过静态约束核对，仍保留每 program 至少扫描两块 K/V 的练习要求。这是该版本和路径的约束，不推广为所有 dot 的通则。（来源：`msg-0a3156b7ec2596ac8c9b`、`msg-91cb16a60494c5bb73d0`、`msg-930b8cc368276fb0119c`。）

- [要点] 输入校验和静态覆盖还留下什么边界？——三个输入设备相同不等于是 CUDA 张量，首轮缺少 CUDA 设备检查；二轮已修正。静态索引检查覆盖 16 组输入、216 个 program、6912 个 query 行，确认允许 key 覆盖、head 边界、独占写回与至少两轮扫描，但不是 JIT/数值验证。连续且基址未 16 字节对齐的偏移视图未被公开数值用例覆盖；二轮仍报告 13 项 Ruff 规范问题和格式余项。（来源：`msg-91cb16a60494c5bb73d0`、`msg-930b8cc368276fb0119c`。）

- [转折] GPU 验证证据来自哪里？——9 月 24 日用户报告“已经在另外的gpu机器上测试验证过了练习代码”，并更新仓库进度。当时助手对保存记录的核对摘要为：RTX 5090 上基础测试 41 passed / 3 skipped，加入两项 A4 变式后 43 passed / 3 skipped；三项跳过为需两张 GPU 的跨设备检查。这里没有原始 pytest 输出，不写成当前环境执行，也不据此产生性能结论；此前 Triton 3.7.1 的静态核对不充当远端完整环境记录。（来源：`msg-21eda83ac712f83d478e`、`msg-ce2516763034928a6b4c`。）

- [要点] A4 中怎样区分局部 token 与 descriptor 全局行？——用户对 `[B,H,N,D]=[2,1,256,64]`、`BLOCK_M=32`、`(b,h)=(1,0)`、Q tile 编号 2，正确给出局部 `[64,96)`；加 `(bH+h)N` 后全局为 `[320,352)`；局部 query 70 的 causal key 范围为 `[0,71)`。可复用的是局部区间加 head 基址的关系，causal 判断仍使用 head 内 token 坐标，并包括自身。（来源：`msg-ce2516763034928a6b4c`、`msg-2c5a5a0b418aaacf7965`、`msg-b6bd9cfb8c4fd23e4345`。）

- [纠错] 场景：A4 给定已乘原始 sm_scale、尚未取指数的 score `s_j=2*floor(j/16)−15`，前两块分别全为 −15、−13；用户先询问它是否已经经过 exp2，随后说“那么重标定系数为2^(-2)”，并算出 `l=20`、`acc=U_0/4+U_1`。正确差值：kernel 使用 `x=s/ln2`，故 `alpha=2^((−15+13)/ln2)=e^-2`，`l_new=16e^-2+16`，`acc_new=e^-2*U_0+U_1`。原因：原答把自然指数分数标度与 base-2 指数混用。助手也澄清了“自然指数 score”措辞；用户识别块分数、旧 `l=16`、旧 `acc=U_0` 及“两个旧状态都须重标定”的理由均正确，错误仅在换底系数。（来源：题目 `msg-b6bd9cfb8c4fd23e4345`；用户 `msg-5683cef16b138fa68a84`；修正 `msg-234125abb7d702da8655`。）

- [要点] 换底补差后怎样确认掌握的是表示域而非记住数值？——换成已乘原始 scale、尚未取指数的首块 1、次块 4，用户独立回答“重标定系数为e^(-3)”。稳定关系为 `x=s/ln2`，`2^(x_old−x_new)=e^(s_old−s_new)`；题目原始 sm_scale 与 kernel 内额外融合 `1/ln2` 后的缩放应分别命名。（来源：`msg-234125abb7d702da8655`、`msg-94e6d051f059f6c2e810`、`msg-efc6d108a0e37a868c7f`。）

- [要点] 同一 head 中所有 Q 相同，是否所有 O/M 都相同？——用户正确推理 non-causal 下 score 和有效 K/V 集合相同，因此 O/M 相同；causal 下有效前缀随 query 变化，不能直接沿用。助手补准确：score 仍含 sm_scale，允许 `j≤i` 包括自身；该变式 M 随有效前缀增长，O 通常变化，但不保证任意两行都不同。保留这个核心正确回答及表述收紧，不把整项改写成误解。（来源：`msg-efc6d108a0e37a868c7f`、`msg-e48bec819d43f122850d`、`msg-76582b83151442cc7667`、`msg-5f4e9e842b1bc79d74d6`。）

- [转折] 本段学习如何结束？——在代码审查、远端数值记录和 A4 解释串联之后，用户明确说“很好，结课吧”。这里只记录这次关闭确认；指定消息范围到此结束，不声称范围内已经展示后续持久化关闭写入，也不复制 mastery 表。（来源：`msg-5f4e9e842b1bc79d74d6`、`msg-1c89b0306b8b17cd5728`。）

## 遗留

- [遗留] 规范/格式余项与连续但基址未对齐视图的覆盖边界保留在 [Lesson 的 Review 记录](../lessons/06-fused-attention.md#review-findings)；FP8 修订未在本段做 GPU 复验，且本次未形成性能实证结论。这些边界不作为稳定技术结论直接制卡。（来源：`msg-c9b9e5a87e2f35f95569`、`msg-930b8cc368276fb0119c`、`msg-5f4e9e842b1bc79d74d6`。）
- [遗留] 根据此次先全貌、符号优先、API 前置解释与检查时机的反馈优化 guide-learning，是用户指定的后续方向；本结构化记录不开展该项修改。（来源：`msg-a104eec606d45cc6091c`、`msg-6c5d822c69ff241119f1`、`msg-1c89b0306b8b17cd5728`。）
