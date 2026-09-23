# 第 06 课：Fused Attention 的在线 Softmax 与分块数据流

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-06-fused-attention` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 独立解释 FlashAttention 的精确分块计算，并实现、验证一个 Triton FP16 前向 |
| 阶段 | `review`（上一轮静态缺陷已修复；GPU 编译与数值验证待进行） |
| 启动授权 | 2026-09-14，学习者在 Lesson 05 关闭并推送后明确提出“接下来，我想开启triton下一课。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/06-fused-attention.py` | `teaching-spine` | 上游 commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；本地 SHA-256 `5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317` | 在线 softmax、前向分块、因果阶段与反向数据流的教学顺序 |
| `docs/triton-tutorials/official/06-fused-attention.py` | `implementation-authority` | Git blob `b1283e8ef99cb01a1acc3df0accf2caeba38e506` | 固定源码的 grid、descriptor、kernel 控制流、测试与边界 |
| [上游 FP8 V descriptor 修复源码](https://github.com/triton-lang/triton/blob/dc3101b3a6fe03f20fa7384c4d312ee17f160415/python/tutorials/06-fused-attention.py) | `implementation-authority`（窄范围补充） | commit `dc3101b3a6fe03f20fa7384c4d312ee17f160415`，2026-09-19；文件 SHA-256 `36eb1f04b8ae795a554c69529e8c930edc5727a43322b39e87f916c535d7ba63` | 仅裁决 FP8 V 的 descriptor shape、坐标及专用回归；不替换本地 teaching spine，见 OBS-06-FP8-01 |
| [Triton v3.7.1 实现](https://github.com/triton-lang/triton/tree/v3.7.1) | `implementation-authority`（静态 Review） | tag `v3.7.1`，与 `uv.lock` 一致；核对于 2026-09-23 | `tools/tensor_descriptor.py`、`language/{core,math,semantic}.py`、`_utils.py` 与 NVIDIA backend 的构造器、静态 shape、log／dot 类型和最小 dot 维度规则 |
| [FlashAttention](https://arxiv.org/abs/2205.14135) | `method-authority` | arXiv `2205.14135`，2022 | IO-aware exact attention、分块与避免二次中间量物化的算法依据 |
| [FlashAttention-2](https://arxiv.org/abs/2307.08691) | `method-authority` | arXiv `2307.08691`，2023 | 更好的 block／warp 工作划分；本课只采用与固定教程核心数据流相关的范围 |
| `docs/triton-tutorials/SOURCE.md` | `explanatory-support` | `tutorials_python.zip` SHA-256 `2d838ed48281a3bcf901e230ab9abc29b042e4ddf899eef8347676612259ed04`，下载于 2026-07-15 | 上游来源、许可与本地快照边界 |

### 目标与证据门槛

| ID | 可观察目标 | conceptual | practical | empirical | 本课 evidence 目标 |
| --- | --- | --- | --- | --- | --- |
| O1 | 解释 scaled dot-product attention 的形状、归约域、因果 mask，以及标准实现的二次中间量与 IO 问题 | required | not-required | not-required | 独立追踪一个小矩阵的 score、逐行 softmax 与输出依赖，并区分计算量、存储量和 HBM 流量 |
| O2 | 推导在线 softmax 合并 score 分块时的运行最大值、分母与输出累加器重标定 | required | required | not-required | 独立合并两个 score 分块，说明 `m_i/l_i/acc/alpha` 不变量；后续 learner-owned FP16 前向通过数值与变式验收 |
| O3 | 解释并实现 Triton 前向的 program/grid、Q 常驻与 K/V 扫描、causal stage、descriptor 和边界约束 | required | required | not-required | 追踪固定源码的 tile 地址与 causal key 范围；实现不物化完整 score/probability 矩阵的前向 |
| O4 | 解释固定源码怎样利用保存的行统计量与 `Delta=sum(O*dO)` 组织 `dQ/dK/dV` 和 causal 分块 | required | not-required | not-required | 独立追踪 preprocess、`dK/dV` 与 `dQ` 的形状、扫描方向和 mask；不要求本课独立实现反向 kernel |

本课围绕“保持数学等价的分块注意力”形成一组完成门槛。FP8、warp specialization、硬件专属调参、
独立性能 benchmark、任意 attention 变体和 learner-owned 反向实现不属于核心范围；需要时可作为结课后
optional extension 另行授权。所有 empirical 维度均为 `not-required`，不会用正确性测试代替性能证据。

### 当前证据

- **已确认前置**：Lesson 02 已验证逐行 stable softmax、padding 与归约；Lesson 03 已验证分块矩阵乘法、
  `tl.dot` 与二维 program 映射；Lesson 05 已验证跨块统计量、FP32 累加、反向归约与同步边界。这些只
  决定本课可以从注意力整体数据流开始，不直接证明 Fused Attention mastery。
- **来源与环境核对（2026-09-14—19 历史）**：固定源码与来源记录均通过 UTF-8 和路径安全检查。当时环境为 RTX 5090
  （compute capability 12.0）、PyTorch `2.13.0+cu130`、Triton `3.7.1`、CUDA build `13.0`。

<a id="e-01"></a>

- **E-01（O1–O4，节点级 conceptual）**：能在单头小矩阵中给出 Q/K/V、score/probability 与输出形状，
  正确追踪 causal query 的有效 key，并区分避免物化二次中间量与不消除主要矩阵乘法。独立完成两个
  score block 的在线 softmax 合并，解释最大值变化时 `l/acc` 的 `alpha` 重标定、base-2 score 转换及
  `M=m+log2(l)`；在变式中修复了把保存的 `M` 误解为单纯运行最大值的缺口。能把二维 grid 映射到
  `(batch,head,Q tile)`，追踪 descriptor 的局部 token 与全局行，解释 non-causal／causal stage bitmask、
  Q 常驻与 K/V 扫描，并完整复述前向 program 生命周期。反向方面，能给出输入／输出／保存量形状，
  计算 `Delta=O*dO=P*dP` 的数值例，解释 `dQ` 按行扫描 key、`dK/dV` 按列扫描 query、causal 镜像区域、
  单 program 输出所有权，以及 `sm_scale` 与 `ln2` 的补偿；固定 wrapper 的 head dimension、stride 与
  `N_CTX%128` 边界判断正确。

<a id="e-02"></a>

- **E-02（O1–O4，综合验收）**：在三题变式中，学习者正确给出跨分块 `m'=5`、
  `alpha=e^-3`、`l'=3e^-3+4` 与 `acc'=e^-3*A+B`，并识别旧新块需统一最大值基准；最初把最终输出
  的分子分母写反，换条件后独立得到 `O=(10e^-1+20)/(2e^-1+1)`。对新形状
  `Z=2,H=2,N=16,D=64,BLOCK_M=4,BLOCK_N=8`，正确追踪 `(batch,head)=(1,1)`、
  `offset_y=48`、Q token `8:12` 与 descriptor 行 `56:60`，遗漏的两轮 K/V 扫描及每轮 `[4,8]`
  score tile 已澄清。反向题中，正确判断 causal `pid=1` 对角 query 范围、无锁独占写回及 `dQ`
  的 key 范围；最初混淆 `Delta` 的归约轴与前向保存量／反向输出，补差后能对新形状独立说出
  `Delta` 沿特征维 D 求和、形状 `[B,H,N]`，并区分前向保存的 Q/K/V/O/M、反向临时 Delta 和
  反向输出 dQ/dK/dV。综合模型、关键边界与条件变式 evidence 已充分。
- **2026-09-19 综合验收结论**：当轮判断 O1–O4 的 `conceptual` 已具最低充分证据；这不等同于
  O2／O3 practical 或 final mastery。2026-09-20 学习者反馈整体数据流仍不清晰，后续以 E-05
  补充需求为准；保留已发生的局部与变式证据，不据此跳过全流程讲解。
- **仍缺 evidence**：O2／O3 practical。学习者已接受以下 revision 1 契约，且于 2026-09-19
  澄清核心 kernel 由本人编写；Agent 维护验收和记录，并进行 Review。经过 E-05–07 补充讲解，
  学习者于 2026-09-23 提交首次实现并完成一轮修订；E-08 的 9 项静态缺陷经 E-09 复核关闭，
  GPU 验证尚未进行。

<a id="e-03"></a>

- **E-03（2026-09-19，P06-A1–A3 验收准备）**：Agent-owned 公开测试收集 44 项，覆盖 FP16 合法数值与
  base-2 `M` 对照 8 组、接口与输入不变性、形状／dtype／device／连续性／scale／causal 负例；
  单 GPU 下跨 CUDA 设备的 3 项将在实现存在后跳过。参考计算、Ruff check、格式检查和
  BasedPyright 均通过。当时完整命令的 expected red 为 `1 failed / 43 skipped`，唯一失败是
  learner-owned 实现文件尚不存在；其余按设计因同一缺口跳过，不把跳过当作正确性通过。
  P06-A3 的 descriptor／在线状态／不物化完整矩阵仍需实现提交后的源码 Review；P06-A4 未提前
  写入公开测试。Agent 未创建或修改核心实现。

<a id="e-04"></a>

- **E-04（所有权澄清与恢复边界）**：学习者明确说明“测试的核心kernel当然是由我来编写”，当前
  只是没有足够时间，要求 Agent 完成验收工件后暂停、保存学习断点并按需整理日志。revision 1 的
  learner-owned 核心实现、A1–A4 验收和独立证据门槛均不变；此轮不将缺失实现记为 learner finding，
  后续从已验证的 expected red 继续。暂停不是本课完成，亦不启动下一课。
- **权威知识产物引用**：固定教程源码、FlashAttention／FlashAttention-2 论文及上方来源记录。

<a id="e-05"></a>

- **E-05（2026-09-20，学习者反馈与补充范围）**：学习者明确指出，虽然已完成局部学习与综合题，
  仍未形成清晰的算子全流程；输入输出的 dtype／shape／含义、未分块数学与中间精度、分块与 program
  输出所有权、kernel 间参数传递、前向统计量的反向用途，需要先连贯讲解，再逐点展开。另需补足
  TensorDescriptor 的用法、适用条件与取舍，以及 `float8e5` 和固定源码相关分支。该反馈不撤销
  E-01／02 中已发生的独立回答，但限制其“整体模型已充分建立”的解释；补充理解尚待后续交流确认。
- **补充路线与边界**：先建立全流程和课程路线，再按输入输出与精度、分块与在线状态、descriptor、
  前向源码、反向与统计量、FP8／硬件分支及测试与 benchmark 组织逐点阅读固定教程；导师先完成
  串联讲解，再进行与已讲内容相称的检查。revision 1 实践契约与核心实现所有权保留，不新增 FP8、
  反向实现或性能实证的实践门槛。学习者要求在理解原始教学代码并完成实践后，再基于本轮问题优化
  `guide-learning`；本轮先补课，不修改 Skill。
- **讲解顺序偏好**：学习者要求默认先定义符号与各轴含义，推导通用公式并标注 shape，再映射源码；
  数字例子用于必要的补充解释，避免 `BLOCK_M=D` 等数值重合掩盖维度语义。

<a id="e-06"></a>

- **E-06（2026-09-21，补充理解与来源核验）**：学习者已明确反馈算子全貌清晰，并在后续交流中
  独立解释 descriptor 块形状与起点、Delta 的 query 归属与广播、分块梯度所需的跨贡献归约、
  dQ 的 `ln2` 补偿及 FP8 E5M2 相对 FP16 的间距比。当时 FP8 V 布局和硬件分支仍在阅读中；这些是
  补充概念证据，不替代尚未提交的 learner-owned 实现或 final mastery。
- **OBS-06-FP8-01（来源 observation）**：固定快照为 FP8 V 声明 `shape=[D,B*H*N]`、
  `strides=[N,1]`，却用列坐标 `(b*H+h)*N*D+start_n` 加载；多 head 时坐标会越过所声明列界。
  上游提交 `dc3101b3a6fe03f20fa7384c4d312ee17f160415`（PR #11461）明确修复这一点，改为
  `shape=[B*H*D,N]`、`load([(b*H+h)*D,start_n])`，并添加 `test_fp8_v_batch_head_descriptor`。
  本次纯 Python 坐标检查在 `B=H=2,N=128,D=64` 下确认旧列坐标从第二个 head 起越界，修订后的
  坐标均在界内且地址公式匹配。当前环境无 GPU，未运行原版或修订版 FP8 kernel；不推断具体设备
  上的报错或输出表现。本地只读快照保持原样，教学以明确区分版本的修订片段补足这一处；不扩大
  revision 1 的 FP16 实践门槛，不建立 learner finding。

<a id="e-07"></a>

- **E-07（2026-09-21，补充阅读收束与返回实践）**：学习者继续独立说明了互逆 permute 与存储布局、
  `acc` 特征半块的索引、grid 与 `num_warps` 的职责、反向对照须使用同一 dO，以及计算量估算不能
  直接预测耗时。结合 E-01／02／06，O1–O4 的概念证据足以恢复已接受的 revision 1 实践；
  源码教学不替代 learner-owned 实现、P06-A4 独立变式或 final mastery。当前仍缺 O2／O3 practical。
- **实践环境安排**：学习者明确选择先在当前仓库编写，稍后到 GPU 机器验证；Agent 可先进行源码
  Review 与可运行的静态检查，GPU 数值结果到对应环境实际运行后再记录。
- **验收维护**：核对发现 P06-A1 已要求连续 FP32 M，但原数值测试缺少连续性断言，Agent 已在
  `test_forward_matches_torch` 补入 `m.is_contiguous()`；required gate 和契约 revision／digest
  不变。测试语法、Ruff check 与格式检查通过。当前会话无 NVIDIA 设备、GPU 虚拟环境和 PyTorch，
  未重跑 GPU 测试；E-03 的 expected red 是历史结果，不作为本轮复验。该修复不属于 learner finding。
- **OBS-06-BENCH-01（非 gate 的源码阅读边界）**：本地 benchmark 只在 `mode=fwd` 时转换 FP8，
  所以 `triton-fp8` 的 bwd 标签实际仍走 FP16 输入。`2.5` 是反向 FLOP 的约定估算系数；该实现的
  dQ 与 dK/dV 路径分别重算 score／dP，报告数字不等于实际指令工作量或耗时倍数。

<a id="e-08"></a>

- **E-08（2026-09-23，首次核心提交与静态 Review）**：学习者提交
  `gpu/triton/lesson06_fused_attention.py`，明确尚未进行 GPU 测试，请求先检查代码。本次审查版本
  SHA-256 为 `8ba2daa28c645dc133e169f04d8c12ff68921fb957b1f7c2a42d20a977b3dea5`；revision 1
  契约与 digest 核验一致。AST 语法解析通过；源码与 Triton v3.7.1 规则核对发现下方 9 个 required
  finding。Q 常驻、全局行坐标的一致性、causal 过去／对角区间和未物化完整 score 矩阵的结构方向
  未发现同类缺陷，但不能据此认定数值通过。核心文件未由 Agent 修改。
- **本轮验证边界**：`bash scripts/host-cpu.sh run -- ruff check gpu/triton/lesson06_fused_attention.py --output-format concise`
  报告 10 项规范问题；`bash scripts/host-cpu.sh run -- ruff format --check gpu/triton/lesson06_fused_attention.py`
  报告需要格式化。命名、导入顺序、空白与类型比较形式属于非数值阻断的规范余项。当前无 GPU
  虚拟环境或 NVIDIA 设备，未执行 Triton JIT 或 GPU pytest；类型／shape 结论来自定版源码规则，
  不是设备错误日志。1D M descriptor 在 v3.7.1 的维数检查范围内，未据旧网页的 2–5 维描述列为错误。

<a id="e-09"></a>

- **E-09（2026-09-23，修订实现的静态复核）**：学习者修订后的核心文件 SHA-256 为
  `02e77c9f285f745001403b1de97db90dee692310cd93a3cfda8f4f5dc7e0f242`。按原 finding 的具体
  失效条件逐项复核，F-P06-01–09 均已修正；关闭只针对这些静态根因，不表示 Triton 编译或数值通过。
  Python 语法及契约 digest 核验通过，Agent 未修改核心文件。
- **索引与状态核对**：三次 helper 调用的实参映射正确，均接收并接续 `(acc,l,score_max)`；
  `D` 标记为 `tl.constexpr`，初值为负无穷，换底使用浮点常量；分母在 FP32 权重转为 FP16 之前
  归约。新分块 `BLOCK_M=32,BLOCK_N=16` 满足已核对的 dot 维度规则。一次纯 Python 坐标检查
  提取源码的扫描边界与 mask 表达式，覆盖 16 个契约内形状／causal 组合、216 个 program 和
  6912 个 query 行：key 集合与数学预期完全一致，未跨 head 或重复写输出行，每 program 最少
  两轮 K/V。该检查未执行 Triton 算术、descriptor 或 GPU 指令，不替代 GPU 验收。
- **验证余项**：同 E-08 的 Ruff 命令仍报告 13 项规范问题，格式检查仍需整理；内容集中于导入、
  `l` 命名、空白和类型比较形式。当前仍无 GPU 验证结果，P06-A1–A3 的设备验收与 A4 未完成。
- **OBS-06-ALIGN-01（输入覆盖边界）**：wrapper 检查连续性，但仍依赖 descriptor 要求的 16 字节
  基址对齐；连续的偏移视图不一定满足这一条件。现有公开数值用例使用新分配的张量，未覆盖这类
  视图。保留为支持范围／覆盖边界观察，不静默修改 revision 1 或新增 required gate，也不宣称
  当前实现已支持所有连续视图。

<a id="practice-01"></a>

## 条件片段：已接受的正式练习

以下 JSON 是本练习的规范化契约。Digest 只覆盖 `id`、`targets`、`task`、`deliverables`、
`acceptance`、`scope` 与 `optional`，按递归 key 排序的紧凑 UTF-8 JSON 计算；revision、digest
和 acceptance event 不参与。

```json
{
  "id": "triton-06-practice-01",
  "targets": [
    {
      "objective_id": "O2",
      "missing_dimensions": ["practical"],
      "evidence_gap": "尚缺学习者拥有的在线 softmax 分块前向实现、数值验证与无提示变式。"
    },
    {
      "objective_id": "O3",
      "missing_dimensions": ["practical"],
      "evidence_gap": "尚缺学习者拥有的 descriptor 块访存、Q 常驻、K/V 扫描及 causal 前向实现与验证。"
    }
  ],
  "task": "用 Triton 实现 FP16 分块注意力前向，单 kernel 计算输出 O 和按 query 行保存的 base-2 log-sum-exp M。",
  "deliverables": [
    {
      "artifact": "gpu/triton/lesson06_fused_attention.py",
      "outcome": "由学习者实现 attention_forward(q, k, v, causal, sm_scale) -> (o, M)，核心计算使用 Triton。"
    }
  ],
  "acceptance": [
    {
      "id": "P06-A1",
      "criterion": "q/k/v 为同形、连续、同 CUDA 设备的 FP16 [B,H,N,D]；B,H∈{1,2}，N∈{128,256}，D=64；causal 为 bool，sm_scale 为有限正数。o 与输入同形、dtype、device；M 为同设备连续 FP32 [B,H,N]，表示每个 query 行的 base-2 log-sum-exp。非法形状、dtype、设备、连续性或缩放参数明确抛 ValueError 或 TypeError。",
      "evidence_method": "Agent-owned pytest 检查公开接口、输出 metadata、合法输入和非法输入拒绝行为。"
    },
    {
      "id": "P06-A2",
      "criterion": "causal 与 non-causal、N=128/256、单头与多头的 o 和 M 与 PyTorch FP32 参考计算匹配。o 使用 atol=rtol=1e-2，M 使用 atol=rtol=1e-3。参考 softmax 沿 key 维，causal 屏蔽未来 key；输入不被修改。",
      "evidence_method": "bash scripts/host-gpu.sh run -- python -m pytest -q gpu/triton/lesson06_fused_attention_test.py；参考用 q/k/v.float() 计算 score、softmax、输出与 logsumexp/ln2。"
    },
    {
      "id": "P06-A3",
      "criterion": "前向只有一个 Triton kernel；采用二维 tensor descriptor 对 Q/K/V/O 作块式访存，可在 host 或 kernel 构造。每个 program 固定一个 Q tile、扫描至少两个 K/V tile，用 FP32 m/l/acc 在线重标定；causal 只扫描过去与对角区域，并在对角区逐元素屏蔽未来 key。核心实现不分配或写回完整 [N,N] score/probability 张量。",
      "evidence_method": "数值与输入不变性测试，加学习者源码 Review；不绑定内部函数名、固定 AST、tile 配置或特定 descriptor 构造位置。"
    },
    {
      "id": "P06-A4",
      "criterion": "基础验收通过后，在上述接口范围内完成一个未提前给出的形状和 score 分布变式，并由学习者解释关键索引、在线状态和结果；需要实质帮助的对应范围用新的无提示同构变式恢复独立证据。",
      "evidence_method": "Agent 在基础通过后执行并解释新变式的数值与 metadata 检查，学习者独立解释验证结果。"
    }
  ],
  "scope": {
    "learner_owned": [
      {"artifact": "gpu/triton/lesson06_fused_attention.py", "operations": ["create", "modify", "run"]}
    ],
    "agent_owned": [
      {"artifact": "gpu/triton/lesson06_fused_attention_test.py", "operations": ["create", "modify", "run"]},
      {"artifact": "docs/triton-learning/lessons/06-fused-attention.md", "operations": ["modify", "record"]},
      {"artifact": "docs/triton-learning/README.md#当前-program-状态", "operations": ["modify", "record"]},
      {"artifact": "docs/triton-learning/README.md#checkpoint", "operations": ["modify", "record"]}
    ],
    "read_only": [
      {"artifact": "docs/triton-tutorials/official/06-fused-attention.py", "operations": ["read"]},
      {"artifact": "scripts/host-gpu.sh", "operations": ["read"]},
      {"artifact": "pyproject.toml", "operations": ["read"]}
    ],
    "excluded": [
      {"artifact": "其他课程、实现、依赖、配置与 CI", "operations": []},
      {"artifact": "FP8、warp specialization、硬件调参、性能基准、任意 stride、其他 attention 变体与反向实现", "operations": []}
    ]
  },
  "optional": [],
  "revision": 1,
  "digest": "sha256:56bef738f6d0941d99c0e9a68075cdf1ef8dc3f505379a507aa58c7fb0a2be82",
  "acceptance_event": {
    "event_ref": "triton-06-session-2026-09-19-a",
    "revision": 1,
    "digest": "sha256:56bef738f6d0941d99c0e9a68075cdf1ef8dc3f505379a507aa58c7fb0a2be82",
    "confirmation": "学习者于 2026-09-19 明确回复“确认接受”，随后安排测试、实现、暂停、学习日志与提交。"
  }
}
```

- **帮助与证据**：可自然语言求助；实质实现提示只影响对应范围，后续以无提示同构变式恢复。
- **非目标与完成门槛**：P06-A1–A4 全部通过、相关 required blocking／major finding 关闭后进入
  mastery gate；需学习者确认才关闭 Lesson。本课不要求性能实证。

### Agent-owned 验收工件

- 目标：[lesson06_fused_attention_test.py](../../../gpu/triton/lesson06_fused_attention_test.py)。
  2026-09-19 已由 Agent 建立并预检；44 项收集成功，当时 `1 failed / 43 skipped` 的唯一 red
  为核心文件缺失。2026-09-21 补齐既有数值用例中的 M 连续性检查，静态验证通过，GPU 复验待完成。
  命令：`bash scripts/host-gpu.sh run -- python -m pytest -q --tb=short gpu/triton/lesson06_fused_attention_test.py`。

### Review findings

Opened 行号对应 E-08，Terminal 行号对应 E-09。上一轮 9 项静态 finding 已逐项复核关闭；
当前没有激活的源码修复动作，下一步是 GPU 编译与原契约验收。

| ID | Maps to | Severity | Owner | Status | Evidence | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| F-P06-01 | O3 / P06-A1 | blocking | learner | closed | Opened：E-08 五处构造器使用 `stride=`。Terminal：E-09 L140／146／152／158／164 均改为正确的 `strides=`，与 v3.7.1 签名一致 | |
| F-P06-02 | O2／O3 / P06-A2–A3 | blocking | learner | closed | Opened：E-08 的缩放值与状态实参错位。Terminal：E-09 L76／83／91 三次调用的 `score_max,l,acc,sm_scale` 映射经 AST 核对均正确 | |
| F-P06-03 | O2 / P06-A2–A3 | blocking | learner | closed | Opened：E-08 丢弃内层返回状态。Terminal：E-09 L76／83／91 均接收 `(acc,l,score_max)`，causal 第二段与最终写回使用接续状态 | |
| F-P06-04 | O2 / P06-A2 | major | learner | closed | Opened：E-08 运行最大值初始为正无穷。Terminal：E-09 L72 改为零加负无穷，初值符合首次有效更新的不变量 | |
| F-P06-05 | O3 / P06-A3 | blocking | learner | closed | Opened：E-08 运行时 D 参与静态 shape。Terminal：E-09 L60 的 D 具有 `tl.constexpr` 注解，L74 累加器形状具备编译期维度 | |
| F-P06-06 | O2 / P06-A2 | blocking | learner | closed | Opened：E-08 将整数 2 传入浮点 log。Terminal：E-09 L71 使用浮点常量 `2.0`，符合已核对的类型规则 | |
| F-P06-07 | O2／O3 / P06-A2–A3 | blocking | learner | closed | Opened：E-08 的 PV dot 混用 FP32／FP16。Terminal：E-09 L45 在 FP32 分母归约之后转换权重为 FP16，L46 两个 dot 操作数同 dtype，累加器保持 FP32 | |
| F-P06-08 | O3 / P06-A3 | blocking | learner | closed | Opened：E-08 的 PV 归约维为 8。Terminal：E-09 L135–136 改为 32×16，dot 归约维满足下限，坐标穷举确认每 program 至少两轮 K/V | |
| F-P06-09 | O3 / P06-A1 | major | learner | closed | Opened：E-08 仅校验设备相等。Terminal：E-09 L119 在分配／构造前明确拒绝非 CUDA q，结合 L121 的设备相等检查约束三输入位于同 CUDA 设备 | |

### 记录与推进边界

- 本文件是 Lesson 06 唯一 evidence ledger；Program 与恢复游标由
  [Triton 学习档案](../README.md#当前-program-状态)维护，不在此复制 Checkpoint。
- **按需过程材料**：[结构化学习记录](../logs/2026-09-19-fused-attention.md)；可追溯可见文本对话分为
  [开课](../transcripts/2026-09-14-fused-attention-start.md)、
  [前向与概念](../transcripts/2026-09-14-fused-attention-concepts.md)、
  [反向与综合](../transcripts/2026-09-18-fused-attention-backward-and-synthesis.md)及
  [练习与暂停](../transcripts/2026-09-19-fused-attention-practice-pause.md)四段。过程材料不裁决
  当前阶段、Checkpoint 或 final mastery。
- 普通讲解、追问和正确回答保持零写；只在 durable evidence、正式练习、finding、mastery 或会话边界
  发生语义变化时更新。
- learner-owned 前向工件与 Agent-owned 验收路径由上方已接受的 revision 1 契约限定。
- 关闭本课仍需学习者确认；不会自动启动下一课或 optional extension。

## 条件片段：Session event

| ID / 日期 | Lesson ref | 覆盖范围 | 完成动作 | Evidence 引用 | 未关闭问题 |
| --- | --- | --- | --- | --- | --- |
| `triton-06-session-2026-09-19-a` / 2026-09-19 | `triton-06-fused-attention` | 综合验收、最小 FP16 前向实践启动与计划内暂停 | 综合验收通过；学习者接受 `triton-06-practice-01` revision 1；Agent 建立并验证 44 项验收与可信 expected red；学习者确认核心仍为 learner-owned，暂时中断课程 | E-01–04；[已接受契约](#practice-01) | O2／O3 practical 尚缺；待学习者有时间时提交实现 |
| `triton-06-session-2026-09-20-a` / 2026-09-20 | `triton-06-fused-attention` | 实践前教学补充需求 | 根据学习者反馈转入全流程与源码补充讲解，明确 descriptor／精度／FP8 阅读范围，以及实践完成后再改进 Skill 的顺序 | E-05 | 整体模型与源码细节待补充确认；O2／O3 practical 尚缺 |
| `triton-06-session-2026-09-21-a` / 2026-09-21 | `triton-06-fused-attention` | 全流程与源码补充、验收维护、返回实践 | 完成补充讲解与局部变式；核验 FP8 V 上游修复；补齐 M 连续性断言并静态验证；复用概念证据恢复 revision 1 实践 | E-06／07；OBS-06-FP8-01；OBS-06-BENCH-01 | O2／O3 practical 尚缺；待学习者提交实现并在 GPU 环境验收 |
| `triton-06-session-2026-09-23-a` / 2026-09-23 | `triton-06-fused-attention` | 核心提交与修订后的静态 Review | 首轮定位 9 个静态问题；学习者修订后逐项复核关闭，完成索引集合核对；保持 learner-owned 核心不变 | E-08／09；F-P06-01–09 | GPU 编译／数值与 A4 尚未验收；规范余项及输入对齐覆盖边界已说明 |
