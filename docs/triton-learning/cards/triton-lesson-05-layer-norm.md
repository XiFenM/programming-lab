---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "e3b689528548a15aea36a9a1d0aef6bca5178f80f1801fa955db00f1ef3f88b1",
  "candidate_sha256": "f91f9f499011c65541bc0fb75ac502cc82d8ada14619191bb5107ec142cdc1f1",
  "cards": [
    {
      "content_sha256": "44a9b783a67cb763e303a51e9dc45b411aa22079eae1f2de474d5574a60d56e3",
      "content_summary": "为末维 LayerNorm 定义 M/N 展平映射、按行 mean/rstd 与跨行共享 w/b 的存储和广播形状。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "layernorm-math",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "把沿最后一维的 layernorm 映射为 m 行 n 列并区分统计量与仿射参数形状"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f3e47cb52cfcc440d822f058",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "57cd31e33f0e64caa020873c2cfcd520c455dc9cbe27ac5b0cf6f05e2ca7662c",
      "content_summary": "以逐行 LayerNorm 的归约域纠正 offsets<M 的改法，区分列号与 N、线性偏移与总元素数、行数。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-layernorm-indexing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正逐行 layernorm 用行数或总元素数判断行内有效列的错误"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3f189dd018e0a515751339fa",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0a685e9a817aa883e5649e9dc84fc63864876edf47f4bdb0a14c8581f994539e",
      "content_summary": "说明零 padding 经中心化后变成 −mean、使方差多出 (B−N)×mean²/N，因此要在 FP32 中心化后把无效位置置零。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-layernorm-numerics",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 layernorm 方差归约为何必须在中心化后再次将无效 lane 置零"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4b8c4c94f5dcc855d503cf1b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "86b732f5d6e2d721dd62249b88bba6da72bb38a366329b63cb2f90dc2fb7932a",
      "content_summary": "说明 FP16 load 的 other=mean 会先舍入为 FP16，转回 FP32 后留下残差污染方差，应在 FP32 中心化后置零。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-layernorm-numerics",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "解释 fp16 masked load 用 other=mean 填 padding 为何仍会污染方差"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1663633d4f15f51222c1f5dc",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "80018b6375cd0f8eca2b4f0077526abbdc9ae8e23d02afdaa11cb3ac13453903",
      "content_summary": "从共享仿射参数的前向式定义 dY/x_hat，推导 dw/db 的逐行贡献与跨行归约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "layernorm-backward",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "写出 layernorm 共享仿射参数 w 和 b 的梯度并说明归约方向"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-cbc73c4ece568a8e2a6048f3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "39d4dc0289312c73af4602c7b3001728ceb36c25f1f413c6ed4afa43dcf005c5",
      "content_summary": "在 G<M 的共享 FP32 [G,N] 槽下，串联 pid%G 映射、加锁读改写与第二个 kernel 沿 G 的归约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-layernorm-reduction",
        "fact_scope": {
          "kind": "snapshot",
          "product": "programming-lab triton lesson 05",
          "version": "practice revision 2"
        },
        "recall_target": "解释共享 g 组参数梯度槽的映射、互斥更新和最终归约"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b381f39d42523624ddc91eb1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "56d71351759c5ed6829d5f98417a92c64d5edfc3c516ba6e3a74999467b33b7f",
      "content_summary": "比较 G=M 独占槽（无锁、8MN 字节）与共享 [G,N] 槽（省空间、同组争锁）的取舍，两者都需第二阶段归约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-layernorm-reduction",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "比较参数梯度部分和每行独占槽与共享 g 组槽在临时空间和锁竞争上的取舍"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d50b788a4b300286fae0649c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a6e921e01fadf56361f636adf44f1fd94d0b5effa25c9825036eb68aad8fc582",
      "content_summary": "定义 g、r、x_hat，写出 dx 在直接项之外的均值与方差两项修正，并解释行内耦合。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "layernorm-backward",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 layernorm 输入梯度中的两项行均值修正及分量耦合"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-61f0c63697e23c4bb8877e7e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1841483bd9dab7978ef4853b475fdb0a8d4fed800a7bc21332d72412b8f79a11",
      "content_summary": "用整行平移不改变输出解释行内 Σdx=0，并用 dx 公式核对；常量行例子说明总和为零不等于分量为零。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "layernorm-backward",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 layernorm 一行输入梯度分量之和恒为零的原因"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7d9fbc470e32cec616d8aa9d",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bca94162d7df351465669a555fa17f04ff08950159078df3a3bf91e02c089548",
      "content_summary": "在显式 relaxed 的锁交接中区分锁槽原子性与 release/acquire 数据交接，并说明 Triton 3.7.1 省略 sem 时默认 acq_rel/gpu。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-locks",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton/ptx",
          "version": "triton 3.7.1 / ptx isa current at 2026-09-11"
        },
        "recall_target": "区分 relaxed 锁槽原子性与 release acquire 对受保护数据的交接"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-879fac50921ad524b439c624",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1629338a77c6ef8cec1dd09631b6daece339d061f5588f7664ffdacd81555c23",
      "content_summary": "纠正把跨 program 读到旧值归因于 load/store 异步：数据依赖不保证新版本，交接要靠同步或 kernel 边界。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-memory-ordering",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正把跨 program 读到旧值归因于普通 load/store 是异步操作"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6c3ee89dd146de499b4da75c",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bdd1d2c64d6e75f291e470f1b06d5238d37797e9c7f4d5fbd7c0bfd0421be53b",
      "content_summary": "用已知 T0 解锁、T1 尚未完成的情景，纠正把 barrier 需求归因于解锁线程身份未知。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-locks",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "纠正把解锁前 block barrier 的必要性归因于不知道解锁线程身份"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-946dfd030cd2cebb7efcb48a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e9ff9e379aa411d80c5107b6eb7c15b988256864f5c8a925de88190b5965bc71",
      "content_summary": "围绕多个 program 更新同一梯度向量，串联 CAS 返回旧值决定的所有权、块内汇合与跨 program 交接。",
      "dependency_content_sha256": {
        "mc-879fac50921ad524b439c624": "bca94162d7df351465669a555fa17f04ff08950159078df3a3bf91e02c089548",
        "mc-946dfd030cd2cebb7efcb48a": "bdd1d2c64d6e75f291e470f1b06d5238d37797e9c7f4d5fbd7c0bfd0421be53b"
      },
      "depends_on": [
        "mc-879fac50921ad524b439c624",
        "mc-946dfd030cd2cebb7efcb48a"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-locks",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "串联 triton 共享向量锁中 cas、block barrier 和 release acquire 的职责"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-beed8ffc12a497ed91a95d0a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已对照修订后的 card-09（显式 relaxed 前提，以及 Triton 3.7.1 默认 acq_rel/gpu 的边界）和 card-10（T0 解锁情景）复核本卡：并入了原 card-08 的 CAS 返回旧值与拆分 load/store 竞争，删去与 card-09 同义的边界；三项职责与锚点仍由子卡支持，回忆目标没有变。"
      },
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1438dd5e36dcd6e28696e2e48bbfb16ecc0043d7be9100dc1235d219ae341626",
      "content_summary": "用 wrapper 的 BLOCK_SIZE_N≥N 前提解释官方反向无列循环仍正确，以及绕过前提的后果。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-source-reading",
        "fact_scope": {
          "commit": "35de6d6dcdd3e885a45bce6ba9d1b5e6da191a7c",
          "kind": "snapshot",
          "product": "triton official tutorial 05"
        },
        "recall_target": "通过 wrapper 的 block_size 约束判断官方 layernorm 反向不循环 n 是否正确"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f1be8807a2aa399b0bd38aab",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9defab3791b7c828576041bb4609b0d490f160af327ea9cc92e09d74b603a88c",
      "content_summary": "明确 LayerNorm 中 dy/w/g 的含义与梯度用途，解释先乘后提升为何无法挽回差异。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-layernorm-numerics",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 fp16 layernorm 反向为何要在 dy 与 w 相乘前提升到 fp32"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b498f29892d5db45bfd87e4f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "45ea410f7b46b43ffa5b734abe5ac6c9108f2feb6811fdc139c998178bd8e190",
      "content_summary": "说明普通 / 在本课 NVIDIA 编译产物中是 div.full.f32 近似除法，tl.div_rn 只修这一步舍入，修不了先前的求和误差。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-layernorm-numerics",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "说明 tl.div_rn 改善均值除法的范围以及不能修复前序求和误差"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-01c401f0b87f8a8a6bc0026b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "10165644a0ce508795e759d83dfe2b98e14d32b0b573d8336f4176b5312ce759",
      "content_summary": "追踪常量行均值误差 eta：方差 eta²、r≈1/√ε 把 x_hat 放大为 −eta×r，同号贡献跨行累加使 dw 超差。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-layernorm-numerics",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释近常量行的微小均值误差为何经 rstd 放大并在 dw 中跨行累积"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9e7f35fa3a0e76f647df5bff",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ee54dd75fdcc1ba69020e52b35112caa3e96d539a2eb52ca83fcab9c230b5544",
      "content_summary": "用数据流而非 kernel 数判断 LayerNorm 反向的 dw/db 是否经过全局部分和两阶段归约。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "layernorm-implementations",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch and nvidia layernorm implementations",
          "version": "pytorch 2.13.0; transformer engine 1634a5a; apex a1d527a"
        },
        "recall_target": "区分 layernorm 反向的 kernel 数量、参数梯度归约阶段和全局部分和空间"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-63ec0c40480143b82350e469",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "80e1f49d6fc0672e080f2cc2ff44dcccbee4829db65f41dbb42855d3d96bb22d",
      "content_summary": "向面试官在 90 秒内串联前向统计量与 padding、行内 dx、分组槽的 dw/db 归约和锁同步。",
      "dependency_content_sha256": {
        "mc-4b8c4c94f5dcc855d503cf1b": "0a685e9a817aa883e5649e9dc84fc63864876edf47f4bdb0a14c8581f994539e",
        "mc-61f0c63697e23c4bb8877e7e": "a6e921e01fadf56361f636adf44f1fd94d0b5effa25c9825036eb68aad8fc582",
        "mc-b381f39d42523624ddc91eb1": "39d4dc0289312c73af4602c7b3001728ceb36c25f1f413c6ed4afa43dcf005c5",
        "mc-beed8ffc12a497ed91a95d0a": "e9ff9e379aa411d80c5107b6eb7c15b988256864f5c8a925de88190b5965bc71",
        "mc-cbc73c4ece568a8e2a6048f3": "80018b6375cd0f8eca2b4f0077526abbdc9ae8e23d02afdaa11cb3ac13453903"
      },
      "depends_on": [
        "mc-4b8c4c94f5dcc855d503cf1b",
        "mc-61f0c63697e23c4bb8877e7e",
        "mc-b381f39d42523624ddc91eb1",
        "mc-beed8ffc12a497ed91a95d0a",
        "mc-cbc73c4ece568a8e2a6048f3"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-layernorm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "programming-lab triton lesson 05",
          "version": "practice revision 2 / triton 3.7.1"
        },
        "recall_target": "综合口述 triton layernorm 前向、反向、分组同步和精度边界"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-3d7b7882d5fe98bf89ce8f11",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已对照修订后的 card-03、04、05、06、11 复核本卡：参考回答压到约 400 字，4 个评分锚点各有子卡支撑；删去子卡未覆盖的‘保存统计量’和 FP16 padding 边界；题面写明面试官与 60–90 秒；回忆目标没有变。"
      },
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "4af0bed79b8c48bcf4fb5a1471806a62743d9667e610cba038f8544ff7b82fe5",
  "manifest_payload_sha256": "aeb9ae11645bd362b329ec1bb28a451b7c18416da1b0c2ca40795f6345b36f99",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 7756,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-05-layer-norm-correction.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "57cd31e33f0e64caa020873c2cfcd520c455dc9cbe27ac5b0cf6f05e2ca7662c",
          "logical_id": "mc-3f189dd018e0a515751339fa",
          "row_sha256": "14ceafd317392fa142774932a1853073b3ee919bf0872623e255290b352d7b32"
        },
        {
          "content_sha256": "1629338a77c6ef8cec1dd09631b6daece339d061f5588f7664ffdacd81555c23",
          "logical_id": "mc-6c3ee89dd146de499b4da75c",
          "row_sha256": "71ac6f24f59852c9c8fde1f1c4c08f71c51e42a5db594a6e0a19f6b896787531"
        },
        {
          "content_sha256": "bdd1d2c64d6e75f291e470f1b06d5238d37797e9c7f4d5fbd7c0bfd0421be53b",
          "logical_id": "mc-946dfd030cd2cebb7efcb48a",
          "row_sha256": "43b994665a96fc9b9310ea517540ad2fd18589b5b5dfb473bb4d99ebbb17728a"
        }
      ],
      "sha256": "46727b4fefdc0f26abd9f7eab0749c7cadfb9f53dc0c29e9cd47d0ef0ede1d90",
      "sheet_name": "cards",
      "table_sha256": "878149e58c13f16f6990524e0ebb116320a6b3dfb14773d599ca1c1d1ad0341f",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 25781,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-05-layer-norm-technical-qa.xlsx",
      "row_count": 15,
      "rows": [
        {
          "content_sha256": "44a9b783a67cb763e303a51e9dc45b411aa22079eae1f2de474d5574a60d56e3",
          "logical_id": "mc-f3e47cb52cfcc440d822f058",
          "row_sha256": "8eb9b68eec30faf8b55d7e9c396dbfb3e3100a2d25715bead97a35966f2621b7"
        },
        {
          "content_sha256": "0a685e9a817aa883e5649e9dc84fc63864876edf47f4bdb0a14c8581f994539e",
          "logical_id": "mc-4b8c4c94f5dcc855d503cf1b",
          "row_sha256": "e9e03231aae57b9296bdcc45e149b1719950f9799e4744ff00674614850c08c5"
        },
        {
          "content_sha256": "86b732f5d6e2d721dd62249b88bba6da72bb38a366329b63cb2f90dc2fb7932a",
          "logical_id": "mc-1663633d4f15f51222c1f5dc",
          "row_sha256": "d651da8e1320de9c6c7d14d055073754e02e0e35d280f03ce6a2b951d9d53230"
        },
        {
          "content_sha256": "80018b6375cd0f8eca2b4f0077526abbdc9ae8e23d02afdaa11cb3ac13453903",
          "logical_id": "mc-cbc73c4ece568a8e2a6048f3",
          "row_sha256": "d257007e1c46939f4d07c81c9325aa601346df5a3a8322fad65811a787a50537"
        },
        {
          "content_sha256": "39d4dc0289312c73af4602c7b3001728ceb36c25f1f413c6ed4afa43dcf005c5",
          "logical_id": "mc-b381f39d42523624ddc91eb1",
          "row_sha256": "61af7a33c5e0a98ed1f625f572c153f14ddbfcfa68c90bac8b3f5470ae3f33a6"
        },
        {
          "content_sha256": "56d71351759c5ed6829d5f98417a92c64d5edfc3c516ba6e3a74999467b33b7f",
          "logical_id": "mc-d50b788a4b300286fae0649c",
          "row_sha256": "a6802f08f9fa9ecacbd44f6a7d374acebb87203ea9c445170407f3547973f243"
        },
        {
          "content_sha256": "a6e921e01fadf56361f636adf44f1fd94d0b5effa25c9825036eb68aad8fc582",
          "logical_id": "mc-61f0c63697e23c4bb8877e7e",
          "row_sha256": "c28751cd9c40a7ed07fe9579951e55fd229b0aaed4255df8d1ad0fd2e8a54538"
        },
        {
          "content_sha256": "1841483bd9dab7978ef4853b475fdb0a8d4fed800a7bc21332d72412b8f79a11",
          "logical_id": "mc-7d9fbc470e32cec616d8aa9d",
          "row_sha256": "0d7c143f40108b302011a6b2bd2b0bd8d2b7d1837e6ecfdbe18a4a001ebae56d"
        },
        {
          "content_sha256": "bca94162d7df351465669a555fa17f04ff08950159078df3a3bf91e02c089548",
          "logical_id": "mc-879fac50921ad524b439c624",
          "row_sha256": "f19998af688845e7bc8516ed343f5556df8d7333bd2a9e65d47b0fe07bc89283"
        },
        {
          "content_sha256": "e9ff9e379aa411d80c5107b6eb7c15b988256864f5c8a925de88190b5965bc71",
          "logical_id": "mc-beed8ffc12a497ed91a95d0a",
          "row_sha256": "1f187d3784deca21c030c62007f5c98446e719f140afcabb879c7fbfced8d44a"
        },
        {
          "content_sha256": "1438dd5e36dcd6e28696e2e48bbfb16ecc0043d7be9100dc1235d219ae341626",
          "logical_id": "mc-f1be8807a2aa399b0bd38aab",
          "row_sha256": "36df6a79cbcd81c14a8ccd6edaf85d3465117ba2fdb8da51f1400fa2b9010773"
        },
        {
          "content_sha256": "9defab3791b7c828576041bb4609b0d490f160af327ea9cc92e09d74b603a88c",
          "logical_id": "mc-b498f29892d5db45bfd87e4f",
          "row_sha256": "80c40455f305b8ea8c2bd9da5c5f25b3d3287210a80a8624986fa37a665efb51"
        },
        {
          "content_sha256": "45ea410f7b46b43ffa5b734abe5ac6c9108f2feb6811fdc139c998178bd8e190",
          "logical_id": "mc-01c401f0b87f8a8a6bc0026b",
          "row_sha256": "21127d38c1247c417c3a41ec877ef52a9fd98d1b0d96a09edb6f6072bc2e6ee4"
        },
        {
          "content_sha256": "10165644a0ce508795e759d83dfe2b98e14d32b0b573d8336f4176b5312ce759",
          "logical_id": "mc-9e7f35fa3a0e76f647df5bff",
          "row_sha256": "372a90b85290e168ba794a94e36893bccbb3e677a4541883b46f3187917929ac"
        },
        {
          "content_sha256": "ee54dd75fdcc1ba69020e52b35112caa3e96d539a2eb52ca83fcab9c230b5544",
          "logical_id": "mc-63ec0c40480143b82350e469",
          "row_sha256": "8b2b325d6b3089d3b2286a8ef15207d2f7adef3f825f6e5f8a8baed831ffec8d"
        }
      ],
      "sha256": "35e7e6949e178568377414b6ccd18e76255c6311746081568a92c78eafdca576",
      "sheet_name": "cards",
      "table_sha256": "c17b51334880801f07fb4274be89138de676435c450112c9c70accf23fb61676",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4250,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-05-layer-norm-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "80e1f49d6fc0672e080f2cc2ff44dcccbee4829db65f41dbb42855d3d96bb22d",
          "logical_id": "mc-3d7b7882d5fe98bf89ce8f11",
          "row_sha256": "f7f234f52e1d5c7b713936c5714f5a16609563d278a3c33ed8fd7f20a01d4fb0"
        }
      ],
      "sha256": "78030ff0e60477e696ce55a7a2c729da09f013d0a352f5064eed76599085385a",
      "sheet_name": "cards",
      "table_sha256": "2290dbc2430277dbf3b9fbf45b43e0fa200c7ccbc6ae28d19838ceefdd65105c",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "7d5741315801427cf1c5bc59e6c4b1566a201a1c9600ab7cf99461c7e0a22978",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson-05-study-log",
      "path": "docs/triton-learning/logs/2026-09-14-layer-norm.md",
      "sha256": "3dbda96ab8eae4588e1279f26b31a1a5819b7ae64eb169e1448ace1a7fd75e0f",
      "summary": "Lesson 05 经核验的 LayerNorm 结构化学习过程记录"
    }
  ],
  "target_collection": "triton-cards",
  "template_registry_sha256": "358d0b6e1ee30ee06c0ae9636266ddafad6f2e81494f6d8975d68448e190996c",
  "template_registry_version": "1.1.0"
}
---
# Markji 表格导入卡片

> Markdown 保留受管元数据与模板定义；卡片数据请使用下列按模板拆分的 XLSX 文件导入。

## 真实错误纠错卡

模板 `correction@1.1.0`：

```text
[P#H1#{{意图}}]
📍 [T#!939393#{{场景}}]
---
✅ [T#B,!36b59d#{{正确}}]
❌ [T#!c6413a#{{错误}}]
{{说明}}
```

导入文件：[triton-lesson-05-layer-norm-correction.xlsx](triton-lesson-05-layer-norm-correction.xlsx)（3 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-05-layer-norm-technical-qa.xlsx](triton-lesson-05-layer-norm-technical-qa.xlsx)（15 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-05-layer-norm-oral.xlsx](triton-lesson-05-layer-norm-oral.xlsx)（1 张卡）
