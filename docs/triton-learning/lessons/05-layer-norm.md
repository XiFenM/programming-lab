# 第 05 课：LayerNorm 前向、反向与梯度归约

## 核心记录

| 字段 | 内容 |
| --- | --- |
| Lesson ID | `triton-05-layer-norm` |
| Program | [Triton 学习档案](../README.md) |
| 能力标题 | 独立解释、实现并验证逐行 LayerNorm 的前向与反向数据流 |
| 阶段 | `complete` |
| 启动授权 | 2026-09-09，学习者在确认下一课为 Layer Normalization 后回复“好的，让我们开始吧。” |

### 来源

| Locator | 角色 | 版本锚点 | 本课使用范围 |
| --- | --- | --- | --- |
| `docs/triton-tutorials/official/05-layer-norm.py` | `teaching-spine` | `tutorials_python.zip` SHA-256 `2d838ed48281a3bcf901e230ab9abc29b042e4ddf899eef8347676612259ed04`，下载于 2026-07-15 | 逐行前向、反向梯度、分组部分和与两阶段归约 |
| `docs/triton-tutorials/official/05-layer-norm.py` | `implementation-authority` | Git commit `35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c`；blob `de8afeb2ccddd41d4e17a5b19b7765e4161a30aa` | 固定快照的 kernel、wrapper、保存统计量与并发更新控制流 |
| [PyTorch LayerNorm](https://docs.pytorch.org/docs/2.9/generated/torch.nn.LayerNorm.html) | `interface-authority` | 文档版本 2.9；核验于 2026-09-09 | 补充核验归一化轴、方差分母、epsilon 与仿射参数语义；不裁决本地 runtime 行为 |
| `docs/triton-tutorials/SOURCE.md` | `explanatory-support` | 下载记录 2026-07-15 | 上游来源、完整性与版本边界 |

### 目标与证据门槛

| ID | 可观察目标 | conceptual | practical | empirical | 本课 evidence 目标 |
| --- | --- | --- | --- | --- | --- |
| O1 | 解释逐行归一化域、均值和方差、epsilon、共享仿射参数的作用与形状 | required | not-required | not-required | 独立追踪小矩阵的统计量与输出依赖，解释常量行及未直接讲过的形状变式 |
| O2 | 解释并独立实现逐行融合前向，处理归约、FP32 统计量、padding 与反向所需的保存值 | required | required | not-required | 独立说明数据流及边界；learner-owned 前向通过约定的数值、尾部与无提示变式验收 |
| O3 | 解释并独立实现反向的行内输入梯度、跨行参数梯度与安全的两阶段归约 | required | required | not-required | 独立追踪上游梯度到 dx/dw/db，解释共享参数与并发更新；learner-owned 反向通过约定的梯度与无提示变式验收 |

本课围绕同一逐行 LayerNorm 算子的前向与反向形成一组完成门槛。性能调优、独立缓存机制研究、
通用多轴／任意 stride 接口、生产级集成与下一 Lesson 不属于本课核心范围。所有 empirical 维度均为
`not-required`；功能与梯度正确性验证不构成速度优势的证据。

### 当前证据

- **已确认前置**：Lesson 02 的最终掌握结论已覆盖逐行 program、归约、padding 与 mask；
  Lesson 03／04 已覆盖 kernel／wrapper 实践和边界验证。这些只作为教学起点，不证明 LayerNorm mastery。

<a id="e-01"></a>

- **E-01（O1，节点级）**：能解释固定参数时各行前向独立；把 `(2,3,4)` 的末维归一化映射为
  `M=6,N=4`，正确给出统计量与参数的二维广播形状；对常量行独立算出均值、零方差、零归一化值
  与最终输出 `y=b`。

<a id="e-02"></a>

- **E-02（O2，节点级）**：独立推导未屏蔽的 padding 在方差中增加 `(B-N)*mean²/N`，并算出
  `N=5,B=8,mean=2` 时误差为 `2.4`。初次索引追踪遗漏有效列 mask，后续因混淆 M/N/block size
  提出 `offsets<M`；经澄清后，在新例 `M=5,N=3,B=4,pid=2` 中正确给出 `TTTF`、完整偏移
  `[6,7,8,9]` 与有效偏移 `[6,7,8]`，恢复行内索引与张量线性偏移的区分。

<a id="e-03"></a>

- **E-03（O3，参数梯度节点）**：能正确计算各行对共享 `w/b` 的梯度贡献，并指出沿行归约。
  一次 `3+(-5)` 的汇总符号错误已指出。澄清单 program 局部 `[N]` 与全部行独立暂存 `[M,N]`
  的语义后，能在 `M=4,N=3` 中给出总存储量 `M*N` 与 pid 2 的写入偏移 `[6,7,8]`。

<a id="e-04"></a>

- **E-04（O3，分组归约节点）**：在已讲的分组部分和模型下，对新例 `M=5,G=2` 正确指出 pid 4
  属于组 0，并与 pid 0、2 争用同一把锁；组缓冲区形状与最终归约的综合解释留待 S2。

<a id="e-05"></a>

- **E-05（O3，输入梯度节点）**：能按中心化反向计算 `[4,0,0,0] → [3,-1,-1,-1]`，并说明行内
  均值依赖带来的耦合。按已讲的完整公式计算 `c1=2/3,c2=0,dx=[-1/3,0,1/3]`；在常量行的新变式中，
  独立得到 `dx=[2r/3,-r/3,-r/3]`，据此否定“该点前向输出等于 b，所以输入梯度必为零”。

<a id="e-06"></a>

- **E-06（O1／O2／O3 conceptual，综合验收 S1／S2）**：对连续 `(2,3,5)` 的末维归一化，独立得到
  `M=6,N=5`，pid 4 的有效 X 偏移 `[20,21,22,23,24]` 与 w 偏移 `[0,1,2,3,4]`，并解释总元素数
  mask 会混入下一行。对 `G=4`，正确给出 pid 4 属于组 0、与 pid 0 共享缓冲区、组部分和 `[4,5]`
  及最终 dw `[5]`；进一步解释 `G=M` 只令贡献分别暂存，仍需归约才能形成最终共享参数梯度。

<a id="e-07"></a>

- **E-07（O1／O3 conceptual，综合验收 S3 与纸面推导）**：在固定参数、epsilon 与上游梯度且忽略
  浮点舍入的条件下，正确判断整行平移不改变 y 或 dx，并给出行内 `sum(dx)=0` 的纸面推导。
  推导正确抵消 `sum(h)` 与行内重复的 `mean(h)`，再利用 `sum(x-mean)=0`；
  `r*xhat=(x-mean)/(v+epsilon)` 的展开正确。纸面求和上限写成 `M-1`，应按本课符号统一为 `N-1`，
  属于已指出的非阻塞记号修正；未要求重做已正确的推理。
- **综合验收结论**：S1–S3 通过，结合 E-01–E-05，O1／O2／O3 的 conceptual evidence 已充分。
  此结论不等同于独立实现通过或 final mastery。
- **当前实践结论**：共享组契约 `triton-05-practice-01` revision 2 已接受；E-12 对应版本的数值与
  metadata 验证通过，P05-A4 独立解释已于 2026-09-14 完成，相关受帮助范围的独立证据已恢复。
  设备条件拼接错误已修正，E-14 对最新实现完整复验为 95 pass / 8 skip；F-P05-03 已关闭。
  P05-A1–A4 的证据已充分；学习者于 2026-09-14 明确确认关闭本课，final mastery 已写入。

<a id="e-08"></a>

- **E-08（O2／O3，首次数值 Review）**：审查的实现 SHA-256 为
  `1fedc7b9b01f424708e1e77a83f12e2760f699b7171a26618d0543f79549ac69`。现有 32 项合法数值测试得到
  `16 passed / 16 failed`，前向全部通过，反向全部失败。额外对同一批 16 组输入独立比较各个梯度，
  dx 为 16/16 通过、dw 为 0/16、db 为 16/16；原测试按 dx、dw、db 顺序断言，dw 失败后没有执行
  db 的断言。上述通过仅限本轮输入与契约容差，不代表全部实践或任意输入已通过。

<a id="e-09"></a>

- **E-09（定位与边界复验）**：对 `x=[[1,2,3],[4,5,6]]`、单位 w、零 b、单位 dy，实际 dw 为
  `[5,7,9]`，恰为按原始 x 加权的列和；参考 dw 约为 `[-2.44947,0,2.44947]`，两边 db 均为 `[2,2,2]`。
  对 FP16 `x=[[1,1,1+1/1024]]`，实际 rstd 为 `298.321533`，参考为 `312.929230`；
  将 mean 量化到 FP16 后的 padding 残差预测出额外方差 `1.02457e-6`，与实际 rstd 一致。
  新增该统计量回归后，连同代表性 dw 用例和安全的 `mean-rank` 拒绝用例均复现失败；后者未抛异常。

<a id="e-10"></a>

- **E-10（修订复验与契约对齐）**：学习者修订后的实现 SHA-256 为
  `aec6f878f2f38ae94b436b68040e2b61ea5f3390248d52cfbc0233e7d9c42b09`。原有 99 项完整验收得到
  `91 passed / 8 skipped`，跳过项全部需要第二张 CUDA GPU；dw 已使用 x_hat，前向方差 padding 已在
  FP32 中归零，先前形状／dtype／连续性负例也已通过。学习者明确选择保留共享组与锁方案，契约已更新
  为 revision 2；此轮未修改 learner-owned 代码。

<a id="e-11"></a>

- **E-11（新变式与精度隔离）**：在合法新形状 `(65,67)` 中，用全零常量行及两类接近的加权上游
  梯度隔离 FP16 问题：精确 FP32 乘积分别为 `1.0004067421` 与 `1`，两者在当前 FP16 乘法后均为 `1`。
  当前 dx 全零，参考约为 `0.06335449`／`-0.06524658`；同 dtype 的 PyTorch 与 FP64 oracle 一致，
  FP32 对照实现通过该隔离例。另一例令第 i 行所有输入为 `i/64`、w 与 dy 为 1，正确 dw 为零，
  当前 FP32 dw 最大偏差为 `3.6519248e-4`，超过 `1e-4` 容差，同 dtype PyTorch 为零。
  前向 mean 的最大偏差仅 `5.9604645e-8`，但经过 rstd 与跨行累加后放大；已读取该实现编译产物，
  第 33 行除法对应 `div.full.f32`。两项已分别加入公共回归，均复现失败，故本次新变式不能计为通过。

<a id="e-12"></a>

- **E-12（精度修订与独立变式数值复验）**：当前 learner-owned 实现 SHA-256 为
  `2e6d23581f5f6104e2dbf190d65c067c222aadcf9613670a2dae1f18e48a8502`。前向第 33–34 行将 N 转为
  FP32 后使用 `tl.div_rn`；两个 dx 循环分别在第 199–208、227–236 行把 dy/w 在乘法前转成 FP32。
  现有 101 项完整复验为 `93 passed / 8 skipped`，E-11 的两项回归均通过，关闭 F-P05-05／06。
  随后增加 P05-A4 新形状 `(129,131)` 的 FP16／FP32 两例：第 i 行初值均为 `i/128`，FP16 的
  `(64,0)` 元素额外增加 `1/1024`；前 65 列 w 为 `1.599609375`、dy 为 `0.625`，其他列均为 1，
  b 沿用种子 1234 的 fixture。覆盖多列块、共享组、常量／近常量行及接近的加权上游梯度。
  与既有 PyTorch oracle 按原容差比较 y、mean、rstd、dx、dw、db，metadata 与输入不变性均通过。
  完整命令 `bash scripts/host-gpu.sh run -- python -m pytest -q --tb=short gpu/triton/lesson05_layer_norm_test.py`
  得到 `95 passed / 8 skipped`；新增节点为 `test_independent_shape_variant[fp32]` 和 `[fp16]`。
  环境仍为 RTX 5090、PyTorch `2.13.0+cu130`、Triton `3.7.1`、CUDA build `13.0`；8 项跳过仍因
  缺少第二张 GPU。测试文件 Ruff、格式检查与 BasedPyright 全通过；Agent 未修改核心实现。
  本次 P05-A4 仅完成执行验证，当时尚待学习者解释；后续解释与修订验证见 E-13。

<a id="e-13"></a>

- **E-13（2026-09-14，独立解释与设备修订复验）**：学习者正确追踪 `(129,131)` 的 B=G=64、
  pid 128 与 pid 0／64 共享组 0；尾部计数澄清后，在 N=130 的变式中独立给出 `TTFF`。
  对常量行及 `h=[1+delta,1,1]`，独立推导 `dx=r*[2*delta/3,-delta/3,-delta/3]`，并解释 FP16
  乘积形成后转 FP32 无法恢复已丢失的差异。能解释同号均值误差的参数梯度偏差累积，以及
  `tl.div_rn` 无法修复先前求和误差；澄清保存的 r 后，正确给出偏差均值对应方差
  `(1/N)*sum(eta^2)=eta^2`。结合 E-12，新变式解释要求已通过，恢复相应独立证据；无需重考。
  本次提交 SHA-256 为 `c8c86eea3929276ea4e7a1a87ba2b6932bf99cc5881fe005ba92ddde600f7464`；
  新增设备条件的第 300 行写成 `x.devicex.device.type`，反向在进入 kernel 前抛出 `AttributeError`。
  运行 E-12 同一完整 pytest 命令得到 `42 failed / 53 passed / 8 skipped`，失败均落在该属性访问；
  8 项跳过仍需双 GPU。保留 F-P05-03，当前修订尚未通过接口与整体执行验收，不撤销已通过的
  独立解释或重开原精度 finding。Agent 未修改 learner-owned 实现。

<a id="e-14"></a>

- **E-14（2026-09-14，最终修订复验）**：学习者修正设备条件后的实现 SHA-256 为
  `65bce9d4fcb21206d53b3be4ad9197a938652a1d8e3169c634e9241c064f8272`。第 298–301 行明确要求
  x、w、dy、mean、rstd 位于同一 CUDA 设备，否则在 kernel 启动前抛出 `ValueError`；原属性名
  拼接错误已消除。运行
  `bash scripts/host-gpu.sh run -- python -m pytest -q --tb=short gpu/triton/lesson05_layer_norm_test.py`
  得到 `95 passed / 8 skipped`，覆盖三项精度回归与两个新形状变式。8 项双 GPU 测试因硬件条件
  跳过，跨 GPU 拒绝路径经源码确认，未在双 GPU 上实测。结合接口负例通过与源码复核，关闭
  F-P05-03；此前其余 finding 已关闭。核心实现保持 learner-owned，Agent 未代写或修改。
  本轮验证支持约定形状、dtype 与容差下的功能验收，不构成性能或任意硬件保证。
- **权威知识产物引用**：[固定教程源码](../../triton-tutorials/official/05-layer-norm.py)及
  [来源记录](../../triton-tutorials/SOURCE.md)。

### 记录与推进边界

- Agent-owned 状态为本文件的目标、evidence 与必要 Session event，以及
  [Program / Checkpoint](../README.md#checkpoint)；普通教学轮次不逐条写入。
- 综合验收后，仅为仍缺的 required evidence 提出最小正式练习，并一次性披露具体工件、
  验收和所有权契约。核心实现由学习者完成，Agent 维护获授权的测试与验证工件。
- 所需维度充分后展示 mastery gate，学习者确认才关闭本课；下一课不会自动启动。

<a id="practice-01"></a>

## 条件片段：已接受的正式练习

以下 JSON 是本契约的唯一规范化记录。Digest 仅覆盖 `id`、`targets`、`task`、`deliverables`、
`acceptance`、`scope`、`optional`，按递归 key 排序的紧凑 UTF-8 JSON 计算；revision、digest 和接受事件不参与。

```json
{
  "id": "triton-05-practice-01",
  "targets": [
    {
      "objective_id": "O2",
      "missing_dimensions": [
        "practical"
      ],
      "evidence_gap": "缺少学习者独立完成的融合前向实现、正确性验证与无提示变式。"
    },
    {
      "objective_id": "O3",
      "missing_dimensions": [
        "practical"
      ],
      "evidence_gap": "缺少学习者独立完成的输入梯度及共享组互斥累加的两阶段参数梯度实现、验证与无提示变式。"
    }
  ],
  "task": "实现逐行 LayerNorm：前向一个 Triton kernel；反向第一阶段按共享分组互斥累加 FP32 部分和，第二阶段归约得到最终参数梯度。",
  "deliverables": [
    {
      "artifact": "gpu/triton/lesson05_layer_norm.py",
      "outcome": "提供 layer_norm_forward(x, w, b, eps=1e-5) -> (y, mean, rstd) 和 layer_norm_backward(dy, x, w, mean, rstd) -> (dx, dw, db)。核心计算由学习者用 Triton 完成。"
    }
  ],
  "acceptance": [
    {
      "id": "P05-A1",
      "criterion": "接口与 metadata 正确。x/dy 为连续二维 [M,N]，M>=1、1<=N<=4096；w/b 为连续 [N]；这些张量同属一个 CUDA 设备且 dtype 一致，为 FP16 或 FP32。eps 有限且为正。保存的 mean/rstd 为同设备连续 FP32 [M]，反向使用同一输入前向产生的统计量。y/dx 保持输入形状和 dtype，dw/db 保持参数形状和 dtype，所有输出位于对应输入设备。非法形状、dtype、设备、连续性、尺寸范围或 eps 明确抛出 ValueError 或 TypeError。",
      "evidence_method": "Agent-owned pytest 公共接口、输出 metadata 和拒绝行为用例；只检查统计量 metadata，不通过重算验证调用者提供统计量的来源。"
    },
    {
      "id": "P05-A2",
      "criterion": "前向、保存统计量以及 dx/dw/db 与 PyTorch 和 autograd 对照。覆盖普通输入、非二次幂列数、尾部、单元素、常量行和非均匀上游梯度，覆盖 FP16/FP32。FP32 使用 atol=rtol=1e-4，FP16 使用 atol=rtol=2e-2，保存统计量使用 atol=rtol=1e-4。",
      "evidence_method": "bash scripts/host-gpu.sh run -- python -m pytest -q gpu/triton/lesson05_layer_norm_test.py；PyTorch layer_norm 与 autograd 为参考，fixture 由 Agent 维护。"
    },
    {
      "id": "P05-A3",
      "criterion": "核心计算由 Triton 完成；前向一个 kernel，反向第一阶段将各行参数梯度贡献累加到 FP32 临时槽 [G,N]，共享同一槽的 program 通过 GPU 锁正确互斥并交接更新；第二个 kernel 归约得到最终参数梯度。G 可随 M 选择，不固定具体启发式；槽初始化、行到组的映射和最终归约应确保每行贡献恰好计入一次，不修改输入。",
      "evidence_method": "公共输入不变性测试与学习者源码 Review；不把固定内部函数名、warps 或 AST 结构作为隐藏验收。"
    },
    {
      "id": "P05-A4",
      "criterion": "在已声明接口范围内完成一个未提前给出的形状变式，并解释关键索引和验证结果；需要实质帮助的对应范围以无提示同构新变式恢复独立证据。",
      "evidence_method": "在学习者实现通过基础验收后，Agent 提供新变式、验证数值与 metadata，学习者独立解释结果。"
    }
  ],
  "scope": {
    "learner_owned": [
      {
        "artifact": "gpu/triton/lesson05_layer_norm.py",
        "operations": [
          "create",
          "modify",
          "run"
        ]
      }
    ],
    "agent_owned": [
      {
        "artifact": "gpu/triton/lesson05_layer_norm_test.py",
        "operations": [
          "create",
          "modify",
          "run"
        ]
      },
      {
        "artifact": "docs/triton-learning/lessons/05-layer-norm.md",
        "operations": [
          "modify",
          "record"
        ]
      },
      {
        "artifact": "docs/triton-learning/README.md#当前-program-状态",
        "operations": [
          "modify",
          "record"
        ]
      },
      {
        "artifact": "docs/triton-learning/README.md#checkpoint",
        "operations": [
          "modify",
          "record"
        ]
      }
    ],
    "read_only": [
      {
        "artifact": "docs/triton-tutorials/official/05-layer-norm.py",
        "operations": [
          "read"
        ]
      },
      {
        "artifact": "scripts/host-gpu.sh",
        "operations": [
          "read"
        ]
      },
      {
        "artifact": "pyproject.toml",
        "operations": [
          "read"
        ]
      },
      {
        "artifact": ".agent-skills-config/guide-learning.json",
        "operations": [
          "read"
        ]
      }
    ],
    "excluded": [
      {
        "artifact": "其他课程和实现",
        "operations": []
      },
      {
        "artifact": "性能调优、任意 stride、多轴接口、autograd 封装",
        "operations": []
      }
    ]
  },
  "optional": [],
  "revision": 2,
  "digest": "sha256:69ca7b1725c387851587ef83e06e55bb55ca67055d6d40b7d456664860be35ef",
  "acceptance_event": {
    "event_ref": "triton-05-session-2026-09-13-a",
    "revision": 2,
    "digest": "sha256:69ca7b1725c387851587ef83e06e55bb55ca67055d6d40b7d456664860be35ef",
    "confirmation": "学习者于 2026-09-13 明确选择“保留当前共享分组方案，并相应修订契约（推荐）”。"
  }
}
```

- **契约修订（2026-09-13）**：revision 1（digest `sha256:a71fca6a8261c2265d69f19d04cd9a65a1cbe3e8f2487244cdbf1d3c8e800c3d`）于 2026-09-10 接受，
  要求 G=M 的独占槽。学习者本轮明确选择保留已提交的共享组方案，因此 revision 2 将 P05-A3 对齐为
  共享 FP32 槽的锁保护累加，并移除对此实现的排除项；函数接口、数值容差、输入边界、两阶段反向、
  所有权与独立变式要求均沿用原契约，性能实证仍不属于 required gate。

- **帮助与证据**：可以自然语言求助；实质帮助只影响对应范围，用无提示同构新变式恢复独立证据。
- **完成门槛**：全部 P05-A1–A4 通过、相关 required blocking／major finding 关闭后进入 mastery gate，
  由学习者确认关闭。静态检查中的纯样式或 Triton 类型标注问题作为非阻塞观察。

<a id="practice-tests"></a>

### Agent-owned 验收工件与初始验证

- **测试**：[lesson05_layer_norm_test.py](../../../gpu/triton/lesson05_layer_norm_test.py)。
  2026-09-10 初始 98 项包括前向数值与统计量 16 项、反向数值 16 项、metadata／错误行为 64 项，
  以及实现存在性和公开接口 2 项。2026-09-13 新增 FP16 近常量行统计量回归，之后又新增 FP16 小梯度
  与 FP32 常量行参数梯度两项回归，再加入新形状 FP16／FP32 变式，当前共 103 项；
  反向错误消息明确标注梯度名称。
  前向与反向数值测试分开，可独立检查前向进展。
- **参考与 fixture 预检（2026-09-10）**：16 组 FP16／FP32 数值 fixtures 的 PyTorch 参考计算均完成，
  输出 metadata、有限性、单列梯度退化及常量行行为符合预期；45 种 metadata 负例工厂均能构造目标
  不匹配且不修改原输入。参考使用 PyTorch FP64 `layer_norm` 与 autograd，再转换到约定输出 dtype；
  保存统计量另以 FP32 计算。预检不包含 learner-owned 实现，也不构成实践通过证据。
- **环境**：NVIDIA GeForce RTX 5090，单 CUDA 设备；PyTorch `2.13.0+cu130`、Triton `3.7.1`、
  PyTorch CUDA build `13.0`。跨两个 CUDA 设备的 8 项检查在本机无对应硬件条件，后续需结合源码
  Review 与混合 CPU／CUDA 参数用例核对设备边界。
- **静态检查**：测试文件通过 `ruff check`、Ruff 格式化核对及 `basedpyright`，后者为
  `0 errors, 0 warnings, 0 notes`；测试未包含参考 Triton kernel 或 learner-owned 核心实现。
- **收集**：`bash scripts/host-gpu.sh run -- python -m pytest --collect-only -qq gpu/triton/lesson05_layer_norm_test.py`
  成功收集 98 项。
- **Expected red**：`bash scripts/host-gpu.sh run -- python -m pytest -q gpu/triton/lesson05_layer_norm_test.py`
  返回 `1 failed, 97 skipped`；唯一失败为 `test_lesson05_implementation_exists`，因为学习者文件尚不存在。
  其他项明确因同一缺口跳过；已独立预检环境、参考计算和 fixture，未将跳过当作正确性通过。
- **后续 evidence**：P05-A3 的 Triton 数据流源码 Review，以及 P05-A4 的无提示新变式与解释，
  均在学习者提交实现后执行；公共测试通过本身不会替代这些要求。

<a id="review-2026-09-13"></a>

### Review findings

2026-09-13 的验证环境为 RTX 5090、PyTorch 2.13.0+cu130、Triton 3.7.1、CUDA build 13.0。
E-12 版本完整测试为 95 pass / 8 skip。2026-09-14 独立解释通过；设备检查的新修订因属性名拼接
错误曾得到 42 fail / 53 pass / 8 skip（E-13），学习者修正后完整复验为 95 pass / 8 skip（E-14）。
全部 required finding 已关闭，停止正式 Review。Agent 未修改 learner-owned 实现。

| ID | Maps to | Severity / owner / status | Evidence | Next action |
| --- | --- | --- | --- | --- |
| F-P05-01 | O3 / P05-A2 | major / learner / closed | Opened：E-08／09，dw 使用原始 x。Terminal：E-10，第 176 行改用 dy*x_hat，原有 dw 数值用例复验通过 |  |
| F-P05-02 | O2 / P05-A2 | major / learner / closed | Opened：E-09，FP16 padding 量化残差污染方差。Terminal：E-10，第 43 行在 FP32 中显式归零，新旧前向回归均通过 |  |
| F-P05-03 | O3 / P05-A1 | major / learner / closed | Opened：E-10／12，统计量设备检查遗漏；E-13 修订发生属性名拼接错误。Terminal：E-14，五个输入同 CUDA 设备条件正确，接口与完整测试通过；跨 GPU 路径经源码确认，双 GPU 实测未覆盖 |  |
| F-P05-04 | O3 / P05-A3 / accepted scope | major / learner / closed | Opened：共享槽与 revision 1 独占槽约束不同。Terminal：学习者明确选择共享组方案，已接受 revision 2；源码分组映射、互斥更新及两阶段归约已按该方案核对 |  |
| F-P05-05 | O3 / P05-A2 | major / learner / closed | Opened：E-11，FP16 乘积过早舍入导致 dx 丢失。Terminal：E-12，两个 dx 循环均在 dy/w 相乘前转 FP32；原回归及新形状数值复验通过 |  |
| F-P05-06 | O2／O3 / P05-A2 | major / learner / closed | Opened：E-11，mean 的 div.full.f32 舍入偏差放大为超容差 dw。Terminal：E-12，FP32 分子与分母使用 tl.div_rn；原回归及新形状数值复验通过 |  |

当前 required blocking／major 未关闭数为 0；P05-A4 独立解释已通过，本课已由学习者确认关闭。
F-P05-01–06 均已关闭，历史修订失败不撤销已恢复的独立证据。
第二阶段 `pid + group_index*N` 的列向归约及 wrapper 的覆盖关系未见导致本轮错误的证据。

- **设备边界定位依据（修复前）**：本机 Triton 3.7.1 的 `backends/nvidia/driver.c` 中 `extractPointer` 查询的是
  `CU_POINTER_ATTRIBUTE_DEVICE_POINTER`，没有比较张量设备编号；CUDA 头文件规定该属性表示当前
  context 可访问的指针，启用 peer access 时可包含其他 CUDA 设备的分配。因此这是源码确认的接口缺口，
  不是声称本机已复现跨卡失败。E-14 已在 wrapper 中显式比较全部设备，关闭该缺口。
- **除法语义定位依据（E-11 修复前）**：当时用户 kernel 的 PTX 第 33 行为 `div.full.f32`；
  [PTX 文档](https://docs.nvidia.com/cuda/parallel-thread-execution/#floating-point-instructions-div)
  将其定义为全范围近似除法，不能等同于 IEEE round-to-nearest 的 `div.rn.f32`。
  本机 `tl.div_rn` 实现提供 FP32 精确舍入除法；未替学习者修改或另写参考 Triton kernel。
- **非阻塞静态观察（上一实现版本）**：learner-owned 文件 Ruff 有 12 项（导入、空白、注释标点），BasedPyright 有
  20 项（大写局部变量重赋值、Triton constexpr 调用标注）。按契约不升级为数值／掌握门槛；
  Agent-owned 测试文件的 Ruff、格式与 BasedPyright 均通过。

### Material assistance

| 实际最高披露内容 | 受影响范围 | Agent 写入 learner core |
| --- | --- | --- |
| 指出 dw 使用原始 x 的具体位置，明确局部贡献应采用 dy*x_hat，并提供隔离的小矩阵对照 | O3 / P05-A2 的 dw 实践分支；修订后用无提示变式核对独立证据 | false |
| 定位 FP16 other=mean 的量化残差及方差 padding 不变量，提供回归输入与实测结果 | O2 / P05-A2 的 FP16 方差 padding 分支；修订后用无提示变式核对独立证据 | false |
| 给出两个 dx 循环各自在 load 后、乘法前将 dy/w 转为 FP32 的修订片段，明确每个 block 重建 g，最终 dx 使用该次迭代的 g | O3 / P05-A2 的 FP16 dx 分支；修订后用无提示变式核对独立证据 | false |
| 给出前向 mean 使用 tl.div_rn 的修订片段，分子与 N 显式保持 FP32；说明它修复除法舍入而非消除任意浮点误差 | O2／O3 / P05-A2 的 FP32 统计量与参数梯度精度分支；修订后用无提示变式核对独立证据 | false |

- **恢复结论（2026-09-14）**：E-12 的新形状执行证据与 E-13 的独立解释共同恢复上述对应范围的
  独立证据；E-14 的最新实现已完成整体复验。无未恢复的实质帮助影响范围，Agent 未写入核心实现。

<a id="mastery-gate"></a>
<a id="final-mastery"></a>

## Final mastery

学习者于 2026-09-14 明确回复“关闭结束第05课吧”，确认关闭 Lesson 05。契约 revision 2 未改变；
以下判断一次写入并作为本课最终 mastery 事实源。

| 目标 | required 维度 | 最小证据 | 判断 |
| --- | --- | --- | --- |
| O1：逐行归一化与参数语义 | conceptual | E-01、E-06／07：形状、行间独立、常量行及平移综合验收 | 充分 |
| O2：融合前向、统计量与 padding | conceptual | E-02、E-06、E-13：有效列、padding 误差、均值求值精度及变式解释 | 充分 |
| O2：融合前向、统计量与 padding | practical | learner-owned 前向；E-12／14 的数值、metadata、精度回归与新形状，E-13 独立解释 | 充分 |
| O3：反向、共享组与两阶段归约 | conceptual | E-03–07、E-13：行内耦合、跨行归约、共享槽、参数梯度误差及迁移 | 充分 |
| O3：反向、共享组与两阶段归约 | practical | learner-owned 两阶段实现；E-10／14 源码及完整测试，E-12／13 的独立变式与解释 | 充分 |

- required blocking／major 未关闭数：0；F-P05-01–06 均已关闭。
- Material assistance：对应范围已由 E-12／13 恢复，最新实现的整体执行由 E-14 复验。
- 验证边界：单 RTX 5090；8 项双 GPU 用例未实测，相关拒绝行为以源码检查补充。
- 非阻塞余项：此前静态观察中的格式及 Triton 类型标注问题；不增加验收或掌握门槛。
- empirical：所有目标均为 not-required；没有性能结论或未完成的必需性能实验。
- 最终判断：O1–O3 的全部 required mastery 维度充分，Lesson 05 为 `complete`；下一课未获启动授权。

<a id="production-design"></a>

## 补充讨论：生产实现与临时空间

按学习者 2026-09-11 的明确请求，保存上一轮基于 2026-09-10 源码核验的比较。下列内容属于
实现策略与成本边界说明，不增加当前练习的 required acceptance，也不构成本机性能实验证据。

**两次 kernel launch 不等于参数梯度的两阶段归约。** 以下比较均考虑需要 dx、dw、db 的情况；
框架入口还可能选择不同后端、形状特化和所需梯度分支。

| 实现路径 | 反向组织 | 参数梯度的全局部分和缓冲区 | 实现权威与版本锚点 |
| --- | --- | --- | --- |
| 原练习基线（revision 1） | 一核算 dx 和逐行贡献，另一核汇总参数梯度 | dw/db 各 `[M,N]` FP32，G=M | [契约修订记录](#practice-01) |
| PyTorch 2.13.0 原生 NVIDIA CUDA 常规分支 | 一核算 dx，另一核直接算最终 dw/db | 无该类全局部分和缓冲区；仍使用保存的统计量及块内临时资源 | [`layer_norm_kernel.cu`](https://github.com/pytorch/pytorch/blob/cf30153c4c131c8164ee7798e5022d810682e2cb/aten/src/ATen/native/cuda/layer_norm_kernel.cu#L1564)，本机包对应 commit `cf30153c4c131c8164ee7798e5022d810682e2cb` |
| Transformer Engine 原生 CUDA/NVRTC | 主核融合 dx 与参数梯度部分和，再启动 finalize | 每种参数 `[C,N]`，C 为 `ctas_per_col` | [`rtc_dispatch.cpp`](https://github.com/NVIDIA/TransformerEngine/blob/1634a5a615e164c3e0d4277f25e921bc1c600d39/transformer_engine/common/normalization/rtc_dispatch.cpp#L455)，commit `1634a5a615e164c3e0d4277f25e921bc1c600d39` |
| Apex 经典 affine `fused_layer_norm` | 参数梯度部分和、最终参数梯度、dx，三个 kernel | dw/db 各 `[16,N]`；FP16/BF16 输入的部分和用 FP32 | [`HostLayerNormGradient`](https://github.com/NVIDIA/apex/blob/a1d527a857e8da64c4e7237ca89ec699fb4d9eaf/csrc/layer_norm_cuda_kernel.cu#L824)，commit `a1d527a857e8da64c4e7237ca89ec699fb4d9eaf` |

- **按形状分派**：上述 PyTorch 常规分支不代表所有形状；该版本在 `M > 65536` 且 N 相对 SM 数较小
  时，会为参数梯度建立部分和再归约，见同一固定源码的
  [分派分支](https://github.com/pytorch/pytorch/blob/cf30153c4c131c8164ee7798e5022d810682e2cb/aten/src/ATen/native/cuda/layer_norm_kernel.cu#L976)。
- **减少全局部分和**：Transformer Engine 的 CTA 可循环处理多行，在局部变量中累计贡献后才写部分和，
  见 [主 kernel](https://github.com/NVIDIA/TransformerEngine/blob/1634a5a615e164c3e0d4277f25e921bc1c600d39/transformer_engine/common/normalization/layernorm/ln_bwd_kernels.cuh#L75)。
  C 受 SM 数、occupancy、kernel 配置等影响，部分路径也按行数截断；不能假定 C 永远小于 M。
  多 CTA 协作可能另需 barrier 或 workspace，所以 `[C,N]` 仅描述参数梯度部分和，不是总临时显存。
- **空间计算示例**：两份 FP32 `[M,N]` 部分和占 `8*M*N` 字节。M=8192、N=4096 时为 256 MiB；
  假设只保存 128 行部分和，则为 4 MiB。这是容量计算，不是某个库的固定配置或性能实测。
- **成本取舍**：dx 的行内归约与 dw/db 的跨行归约适合不同工作划分。分开计算可以省去部分和，
  但需要分别访问输入；融合计算可复用已加载数据，但可能增加部分和的读写。launch 数、内存访问、
  并行度、寄存器压力与同步共同影响耗时，不能只按 kernel 数判断速度。
- **图编译路径**：PyTorch v2.13.0 的
  [`native_layer_norm_backward` 分解](https://github.com/pytorch/pytorch/blob/v2.13.0/torch/_decomp/decompositions.py#L1833)
  表达行内／跨行归约；编译器再选择拆分与融合。
  [OpenXLA 的 fusion 说明](https://openxla.org/xla/gpu_architecture#fusion)（核验于 2026-09-10）说明
  一个 fusion 可对应一个 GPU kernel，但没有承诺整个 LayerNorm backward 必定形成一个 fusion。

当时 revision 1 的 G=M 练习作为正确性基线，接受了较大的临时空间；生产实现对比本身不新增性能验收。

## 条件片段：Session event

| ID / 日期 | Lesson ref | 覆盖范围 | 完成动作 | Evidence 引用 | 未关闭问题 | Marker |
| --- | --- | --- | --- | --- | --- | --- |
| `triton-05-session-2026-09-10-a` / 2026-09-10 | `triton-05-layer-norm` | 前向计算、有效列与 padding；参数梯度与分组；输入梯度的均值／方差路径；综合验收与正式实践启动 | 完成节点检查与局部变式；通过 S1–S3；Review 纸面推导；接受 triton-05-practice-01 revision 1；Agent 建立验收并核验 expected red | E-01–E-07；[已接受契约](#practice-01)；[验收工件](#practice-tests) | O2／O3 独立实践 evidence 尚缺；等待学习者实现 |  |
| `triton-05-session-2026-09-11-a` / 2026-09-11 | `triton-05-layer-norm` | 生产实现与临时空间的补充讨论保存；锁机制补充阅读 | 按请求保存固定源码比较、空间计算与结论边界；确认实现文件已由学习者创建，未读取或 Review 核心内容 | [生产实现补充讨论](#production-design) | 当前实践继续按 revision 1；实现验收待学习者提交 |  |
| `triton-05-session-2026-09-13-a` / 2026-09-13 | `triton-05-layer-norm` | learner-owned 实现的数值与接口 Review、修订复验与新变式 | 学习者修订 dw 公式、前向 padding、metadata 及两处精度问题；按选择接受共享组 revision 2；关闭 F-P05-01／02／04／05／06；新形状数值验证通过，完整测试 95 pass / 8 skip | E-08–E-12；[已接受契约](#practice-01)；[Review findings](#review-2026-09-13) | F-P05-03 同设备检查待补齐；P05-A4 独立解释尚未完成 |  |
| `triton-05-session-2026-09-14-a` / 2026-09-14 | `triton-05-layer-norm` | 独立变式解释、设备修订复验与结课 | 完成 P05-A4 解释并恢复独立证据；修订完整测试 95 pass / 8 skip，关闭 F-P05-03；学习者确认关闭本课并写入 final mastery | E-13／14；[Final mastery](#final-mastery) | 无 required 未关闭问题 | `closure` |
