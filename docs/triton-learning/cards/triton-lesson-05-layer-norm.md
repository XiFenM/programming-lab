---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "12b90dff07d69eb60f63c124166de50dbd6ea63cd033ed1df027cb11bb7e3e29",
  "candidate_sha256": "61992a3ece7faef40c0246b5f07fe68209bea2ae216e1c6609d234c5cbe313ee",
  "cards": [
    {
      "content_sha256": "8fbb0d060514e572c004778b47b9f702a8174c600be62315e7d489ac5f654857",
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
      "content_sha256": "3bd8730560f0030097c2eebbc333b5e63f8d4414ebf1c98737c3da01c0a1cfff",
      "content_summary": "以逐行 LayerNorm 的归约范围解释 cols<N，并用跨行误读和尾列例子澄清行数、列数、地址的区别。",
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
      "content_sha256": "4b68468be5abdb1f5f4ba99ae81a17bdfba4e7f1b414472bba16caf4335f684a",
      "content_summary": "说明零 padding 经中心化后不再是归约中性值，并解释 FP16 other=mean 仍可能留下残差。",
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
      "content_sha256": "c3d05d87cd4242148b44ef4c0e4c765097dcee76d714433a87f8fcd50d9aa9c4",
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
      "content_sha256": "dd709354d4b285c987c277eef5a41f24d2729f3252e6fd415e79a6f097b7d3df",
      "content_summary": "定义 M/N/G 和组槽语义，串联 pid%G、互斥累加与第二 kernel 的列向归约。",
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
      "content_sha256": "9e82f5d3244f736dd2552319aa06fcf8a5ed64a761981ddafa5446f15204f02c",
      "content_summary": "定义 g、r、x_hat 与行均值，解释 LayerNorm 输入梯度通过均值/方差共享产生的行内耦合。",
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
      "content_sha256": "d1e6aeb361474e94543202d60685a93b25fe54d6ef725ecf20bfe55ef8f5a9a0",
      "content_summary": "针对常量输入行，定义上游加权梯度并用三列反例区分前向点值与输入导数。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "layernorm-backward",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正常量行前向输出为 b 就断言输入梯度必为零"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f6dfb343d6a843799454c598",
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
      "content_sha256": "b86496d88c1f1f7bfa90fffd4a1836d1a6a6906cf0b7392a75de5b99ce8e043b",
      "content_summary": "在明确 0/1 状态的共享梯度锁中解释 CAS 返回旧值、成功条件与拆分 load/store 的竞争。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-locks",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "解释 atomic_cas 获取标量锁时的返回值及拆分 load/store 的竞争"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-315521cbea3d61b699c57c01",
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
      "content_sha256": "8c8d0316fb62ee1950fb3521a6e611059ac906ea107385532e7096d98bb70de6",
      "content_summary": "在锁地址与梯度 buffer 分离的情景下，解释 relaxed 原子竞争与 release/acquire 数据交接的区别。",
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
      "content_sha256": "80e130243dafaccd29a91fa248f3973453afbd5fe1ef290b428edf71c726f659",
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
      "content_sha256": "fcffcb90d572b7cf562c5903f83b473a478b513ca66c09ddcf266096701b6dc0",
      "content_summary": "围绕多个 program 更新同一梯度向量，串联锁所有权、块内协作完成与跨 program 数据可见性。",
      "dependency_content_sha256": {
        "mc-315521cbea3d61b699c57c01": "b86496d88c1f1f7bfa90fffd4a1836d1a6a6906cf0b7392a75de5b99ce8e043b",
        "mc-879fac50921ad524b439c624": "8c8d0316fb62ee1950fb3521a6e611059ac906ea107385532e7096d98bb70de6",
        "mc-946dfd030cd2cebb7efcb48a": "80e130243dafaccd29a91fa248f3973453afbd5fe1ef290b428edf71c726f659"
      },
      "depends_on": [
        "mc-315521cbea3d61b699c57c01",
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
        "summary": "已重新对照本课 card-08, card-09, card-10 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "272f4e2609be405b7909c120ef2256bcb268719568b2e4c8738c995805a2c3c0",
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
      "content_sha256": "158d01b08f7bffd0a03f72df732f4f77817474bb38c5639d42a1852d0c2efbe6",
      "content_summary": "限定 div_rn 只改善当前除法，并在明确 dy=1 的常量行场景下追踪均值偏差、实际 rstd 与 dw 贡献。",
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
      "content_sha256": "9a9aa2f0cec3689ddc82a071a9912d51fe84bafb2713986a04ceb5d2e7336480",
      "content_summary": "区分两次 kernel 启动、dx/dw/db 的任务划分与参数梯度是否经过全局部分和两阶段归约。",
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
      "content_sha256": "418e19dfa6a31d7a5116bae0bd0e08965e0776b6fa7c93273a8d8ec9cbf81fe2",
      "content_summary": "围绕 [M,N] 输入与带锁 [G,N] 参数梯度槽，串联前向保存、行内 dx、跨行 dw/db 和同步协议。",
      "dependency_content_sha256": {
        "mc-4b8c4c94f5dcc855d503cf1b": "4b68468be5abdb1f5f4ba99ae81a17bdfba4e7f1b414472bba16caf4335f684a",
        "mc-61f0c63697e23c4bb8877e7e": "9e82f5d3244f736dd2552319aa06fcf8a5ed64a761981ddafa5446f15204f02c",
        "mc-b381f39d42523624ddc91eb1": "dd709354d4b285c987c277eef5a41f24d2729f3252e6fd415e79a6f097b7d3df",
        "mc-beed8ffc12a497ed91a95d0a": "fcffcb90d572b7cf562c5903f83b473a478b513ca66c09ddcf266096701b6dc0",
        "mc-cbc73c4ece568a8e2a6048f3": "c3d05d87cd4242148b44ef4c0e4c765097dcee76d714433a87f8fcd50d9aa9c4"
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
        "summary": "已重新对照本课 card-03, card-06, card-05, card-11, card-04 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "1c271528cf93acc7b6c6c4257421b2b0fa9ee7dede07e371c6cca7413189227a",
  "manifest_payload_sha256": "9753cab9d77596f10140e4d569829133ec7acba079aa3934bc6d6af7202447a5",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5748,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-05-layer-norm-correction.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "3bd8730560f0030097c2eebbc333b5e63f8d4414ebf1c98737c3da01c0a1cfff",
          "logical_id": "mc-3f189dd018e0a515751339fa",
          "row_sha256": "6ca30031086406f180e78ae5d1992c07f71574ca53eff1a4f665bbc79a0cf7a7"
        },
        {
          "content_sha256": "80e130243dafaccd29a91fa248f3973453afbd5fe1ef290b428edf71c726f659",
          "logical_id": "mc-946dfd030cd2cebb7efcb48a",
          "row_sha256": "4c49493575fbbe8f46a41d3d51cac6b1e62b8e5f4a5ef47156ebff347cf68fa8"
        }
      ],
      "sha256": "9cc0e630a61a4faccf2b01b70cc0db53d7c1f66773b92b66b10ff029c52df730",
      "sheet_name": "cards",
      "table_sha256": "617c31c190c28eefc9354ce301bb7057f1e897dea87ace6145286ea09d8d799d",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 22413,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-05-layer-norm-technical-qa.xlsx",
      "row_count": 13,
      "rows": [
        {
          "content_sha256": "8fbb0d060514e572c004778b47b9f702a8174c600be62315e7d489ac5f654857",
          "logical_id": "mc-f3e47cb52cfcc440d822f058",
          "row_sha256": "01c0f4995d2e09d5a4e54c79ec582732596cab9988154eff69d387c392d5b57c"
        },
        {
          "content_sha256": "4b68468be5abdb1f5f4ba99ae81a17bdfba4e7f1b414472bba16caf4335f684a",
          "logical_id": "mc-4b8c4c94f5dcc855d503cf1b",
          "row_sha256": "9bab325aa1c86ce1823c5ebed11298c7edbc63a3e0b10e50200e0489fdbaed0f"
        },
        {
          "content_sha256": "c3d05d87cd4242148b44ef4c0e4c765097dcee76d714433a87f8fcd50d9aa9c4",
          "logical_id": "mc-cbc73c4ece568a8e2a6048f3",
          "row_sha256": "9e9a659503f854312b878e397df9d7c9f5535cc4e3d1a41a2eb60bdef4897be5"
        },
        {
          "content_sha256": "dd709354d4b285c987c277eef5a41f24d2729f3252e6fd415e79a6f097b7d3df",
          "logical_id": "mc-b381f39d42523624ddc91eb1",
          "row_sha256": "cb1da3726a42b322b9414346cec4db36039ac3b0ff08f5589805178ceadbf823"
        },
        {
          "content_sha256": "9e82f5d3244f736dd2552319aa06fcf8a5ed64a761981ddafa5446f15204f02c",
          "logical_id": "mc-61f0c63697e23c4bb8877e7e",
          "row_sha256": "393e55c7dc577a888f55a1ef934abdc59b296236366e013f81f06acc02c6274c"
        },
        {
          "content_sha256": "d1e6aeb361474e94543202d60685a93b25fe54d6ef725ecf20bfe55ef8f5a9a0",
          "logical_id": "mc-f6dfb343d6a843799454c598",
          "row_sha256": "a5588f16c91106e6e5f8d5499b61ce2722d28ac07175c45551136f19e1a1f828"
        },
        {
          "content_sha256": "b86496d88c1f1f7bfa90fffd4a1836d1a6a6906cf0b7392a75de5b99ce8e043b",
          "logical_id": "mc-315521cbea3d61b699c57c01",
          "row_sha256": "b788a203c8da784db9f630cb79ee598f74cbac239f6d86d33fd09799b2148ece"
        },
        {
          "content_sha256": "8c8d0316fb62ee1950fb3521a6e611059ac906ea107385532e7096d98bb70de6",
          "logical_id": "mc-879fac50921ad524b439c624",
          "row_sha256": "3108e4c959b07dade8c7eaa184221573006a8af6c8465e2db8d373724936c472"
        },
        {
          "content_sha256": "fcffcb90d572b7cf562c5903f83b473a478b513ca66c09ddcf266096701b6dc0",
          "logical_id": "mc-beed8ffc12a497ed91a95d0a",
          "row_sha256": "5bca76d5ef41c05ec49514c4cb5a8d9425b50df608778de7e89ad2624bc389e8"
        },
        {
          "content_sha256": "272f4e2609be405b7909c120ef2256bcb268719568b2e4c8738c995805a2c3c0",
          "logical_id": "mc-f1be8807a2aa399b0bd38aab",
          "row_sha256": "3be06fc7d7efb50e8b49d1d622e564806a2782bd550a642cc817360e40c6f4f7"
        },
        {
          "content_sha256": "9defab3791b7c828576041bb4609b0d490f160af327ea9cc92e09d74b603a88c",
          "logical_id": "mc-b498f29892d5db45bfd87e4f",
          "row_sha256": "80c40455f305b8ea8c2bd9da5c5f25b3d3287210a80a8624986fa37a665efb51"
        },
        {
          "content_sha256": "158d01b08f7bffd0a03f72df732f4f77817474bb38c5639d42a1852d0c2efbe6",
          "logical_id": "mc-01c401f0b87f8a8a6bc0026b",
          "row_sha256": "9eb4380dbd5990ae3b6cdaf749b628a818bc869e188cda385af57d6722011ef9"
        },
        {
          "content_sha256": "9a9aa2f0cec3689ddc82a071a9912d51fe84bafb2713986a04ceb5d2e7336480",
          "logical_id": "mc-63ec0c40480143b82350e469",
          "row_sha256": "4376df869ff817a1e2062cc2d64c21458744faf4c74acabe3c267a6edd0bf412"
        }
      ],
      "sha256": "1cc3dd828b60be8ce8d033a9b812cb3bc7a5f293c7dc4ab4562332f67df1e86d",
      "sheet_name": "cards",
      "table_sha256": "ceeebc570cbcbac7c05d05af43635df24b932abe4df6d1963f5b239a4d9ac5af",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4725,
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
          "content_sha256": "418e19dfa6a31d7a5116bae0bd0e08965e0776b6fa7c93273a8d8ec9cbf81fe2",
          "logical_id": "mc-3d7b7882d5fe98bf89ce8f11",
          "row_sha256": "93f792586b1c7ed10b8fe8722dffd8f93652e68254e2a719728f810491985689"
        }
      ],
      "sha256": "553129a64636e423e465e8a6ff7b536278b6e77f90f566e9a5c6c0474a5318cb",
      "sheet_name": "cards",
      "table_sha256": "316e72f86c36a1b6e801a2c13395aeae959e64e9416566805900d21e5bbd4a7e",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "f1cb3760e74f3eee76b57277574861919de99b20b9b15b5f457468f3b2c8cd0c",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson-05-study-log",
      "path": "docs/triton-learning/logs/2026-09-14-layer-norm.md",
      "sha256": "8ecd1459eaebca14b401f670f54da83d1693a8fe150a4e25492d29830ca4f828",
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

导入文件：[triton-lesson-05-layer-norm-correction.xlsx](triton-lesson-05-layer-norm-correction.xlsx)（2 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-05-layer-norm-technical-qa.xlsx](triton-lesson-05-layer-norm-technical-qa.xlsx)（13 张卡）

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
