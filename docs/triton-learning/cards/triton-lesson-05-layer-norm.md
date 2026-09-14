---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "f63e1dca11a03efe547cfae84a6c7a2f3789925bf085b21844f275157d7f2399",
  "candidate_sha256": "9db959ad13aa04b063fb5ac406110f8630833ebab20521c2296521b9fbe7d8f3",
  "cards": [
    {
      "content_sha256": "8fb68375551564beada5b786cbd1e19aa8c80ddd96c128957900b51658ec25b0",
      "content_summary": "把末维归一化映射为行，并区分统计量和共享参数的存储与广播形状",
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
      "content_sha256": "8da556d2c9cb4f12b9b3cd423a1a5838106ea1b0f32bbb21c3ebd2ada27ecc7c",
      "content_summary": "逐行 LayerNorm 的 mask 比较行内列号与 N，避免跨行误读",
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
      "content_sha256": "c8d0a9e07749fa14f5796527e1083927c5bebdba7dd8c3d9d69335ed3817b9e2",
      "content_summary": "无效 lane 在减均值后必须再次归零，避免污染方差",
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
      "content_sha256": "2c86a6a6f1cf03f74a9217838e700d2163be517c8f2e7bae4a9ee5b9501c2b20",
      "content_summary": "参数梯度按特征列跨行归约，dw 使用归一化输入",
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
      "content_sha256": "9e98cea2f660da8349817479bff04528d1ffa387233f08a8a46beac2f9628be1",
      "content_summary": "共享分组槽用锁汇总行贡献，再由第二阶段沿组归约",
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
      "content_sha256": "12e033b480045d30cedc2c572a1faac2ee5de216c62fb859596f49d3e3927307",
      "content_summary": "输入梯度通过两项行均值修正体现行内分量耦合",
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
      "content_sha256": "eafc6999bc4d2c8551b645a691c3b536d023f405566058589da850bd4f025d67",
      "content_summary": "用非均匀加权上游梯度反驳常量行输入梯度必为零",
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
      "content_sha256": "d3fe392c7718f758d5be75eded00ba5d7e11ee73997764ee6b693ae34530639a",
      "content_summary": "CAS 返回旧锁值并原子完成0到1，避免拆分检查的竞态",
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
      "content_sha256": "36a286c52e25fe150d47f93d1c9c87075c6994e666efddd0c4485f57261658d7",
      "content_summary": "release acquire 把锁同步扩展到受保护数据，relaxed 仅保证锁槽原子性",
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
      "content_sha256": "478743a1009f4ed7cd9f444bba54af083649a5fba2bd9dd644a02b9b4a781745",
      "content_summary": "block barrier 等待所有协作写者，与解锁线程身份是否已知无关",
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
      "content_sha256": "ec0e4a8253cc03fff906403f05bb5c96b543e6d66b4b2760a05e7041c4e14269",
      "content_summary": "CAS、block barrier、release acquire 分别承担锁协议的三种保证",
      "dependency_content_sha256": {
        "mc-315521cbea3d61b699c57c01": "d3fe392c7718f758d5be75eded00ba5d7e11ee73997764ee6b693ae34530639a",
        "mc-879fac50921ad524b439c624": "36a286c52e25fe150d47f93d1c9c87075c6994e666efddd0c4485f57261658d7",
        "mc-946dfd030cd2cebb7efcb48a": "478743a1009f4ed7cd9f444bba54af083649a5fba2bd9dd644a02b9b4a781745"
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
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5af45392d09ffd8ea06db292bc30195e23c0b3b3ee792c8ad417913fcd2c2cf6",
      "content_summary": "wrapper 保证一块覆盖整行，裁决官方反向无N循环的正确边界",
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
      "content_sha256": "256cdeef2cbfcd1c93af8084f2ff0424983684b19ddee380b50e705542ffc657",
      "content_summary": "在乘法前提升 dy 和 w，避免 FP16 乘积先丢失差异",
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
      "content_sha256": "f1675ed6531d97b99684e0b5be16cc6d1a8032f696f146dde76ac60f8d19ee00",
      "content_summary": "div_rn 限定于当前除法舍入，不能修复前序求和，并说明均值误差传播",
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
      "content_sha256": "75bfe426f0fdbfd7201f91aceabb577dea641e7de6333ae603df127fad23d07f",
      "content_summary": "固定版本实现表明kernel数、部分和策略与速度不能相互直接推出",
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
      "content_sha256": "c6489d54510d9c1db3e5230dc85deb807f607537010f1f51fcbba065738a648a",
      "content_summary": "综合口述逐行前向、两类反向归约、锁同步、数值精度和接口边界",
      "dependency_content_sha256": {
        "mc-4b8c4c94f5dcc855d503cf1b": "c8d0a9e07749fa14f5796527e1083927c5bebdba7dd8c3d9d69335ed3817b9e2",
        "mc-61f0c63697e23c4bb8877e7e": "12e033b480045d30cedc2c572a1faac2ee5de216c62fb859596f49d3e3927307",
        "mc-b381f39d42523624ddc91eb1": "9e98cea2f660da8349817479bff04528d1ffa387233f08a8a46beac2f9628be1",
        "mc-beed8ffc12a497ed91a95d0a": "ec0e4a8253cc03fff906403f05bb5c96b543e6d66b4b2760a05e7041c4e14269",
        "mc-cbc73c4ece568a8e2a6048f3": "2c86a6a6f1cf03f74a9217838e700d2163be517c8f2e7bae4a9ee5b9501c2b20"
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
      "source_ids": [
        "lesson-05-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "1c271528cf93acc7b6c6c4257421b2b0fa9ee7dede07e371c6cca7413189227a",
  "manifest_payload_sha256": "523dc46ab53715b821a304790a03dfee7129558a6cb1f335666e82307c835da2",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 4418,
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
          "content_sha256": "8da556d2c9cb4f12b9b3cd423a1a5838106ea1b0f32bbb21c3ebd2ada27ecc7c",
          "logical_id": "mc-3f189dd018e0a515751339fa",
          "row_sha256": "dc078861b2c967126a72519d02d3410e91d93ecda67244c929f31d826fc6dcab"
        },
        {
          "content_sha256": "478743a1009f4ed7cd9f444bba54af083649a5fba2bd9dd644a02b9b4a781745",
          "logical_id": "mc-946dfd030cd2cebb7efcb48a",
          "row_sha256": "8ef27499daa4c68a1e7d43027ee737f7fcff3cc9276559649068eff80d80bb94"
        }
      ],
      "sha256": "c9c48a77a42857a7833e311c6e355317040dd10511c659bd475ce0a96b703de9",
      "sheet_name": "cards",
      "table_sha256": "4da6255e04c3931a3ebd24a1ba979f158f86eeff38763f97c327d470c9a42677",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 13496,
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
          "content_sha256": "8fb68375551564beada5b786cbd1e19aa8c80ddd96c128957900b51658ec25b0",
          "logical_id": "mc-f3e47cb52cfcc440d822f058",
          "row_sha256": "f63b6c99b63ef473281b82a8803b914a448adf2343867737e10bbb968740d2fe"
        },
        {
          "content_sha256": "c8d0a9e07749fa14f5796527e1083927c5bebdba7dd8c3d9d69335ed3817b9e2",
          "logical_id": "mc-4b8c4c94f5dcc855d503cf1b",
          "row_sha256": "6b4a7390f7cef6b62dc18c65f419da1de7fe96ee8fa94a6b25553423b8c28cdc"
        },
        {
          "content_sha256": "2c86a6a6f1cf03f74a9217838e700d2163be517c8f2e7bae4a9ee5b9501c2b20",
          "logical_id": "mc-cbc73c4ece568a8e2a6048f3",
          "row_sha256": "9fe7cb14bd8e04bc0094324facc8db8bc8a8d71c7094e73c05db20bf4dd9ebdb"
        },
        {
          "content_sha256": "9e98cea2f660da8349817479bff04528d1ffa387233f08a8a46beac2f9628be1",
          "logical_id": "mc-b381f39d42523624ddc91eb1",
          "row_sha256": "fdc903ab90c4c32f8987af64aaefbc0ecd82664d00a40259ec3bed2dfd14a3ec"
        },
        {
          "content_sha256": "12e033b480045d30cedc2c572a1faac2ee5de216c62fb859596f49d3e3927307",
          "logical_id": "mc-61f0c63697e23c4bb8877e7e",
          "row_sha256": "6ca2462cd610ee0f7794d0ed868bdab9302f242e69bc758ceb1359b6bdf3234d"
        },
        {
          "content_sha256": "eafc6999bc4d2c8551b645a691c3b536d023f405566058589da850bd4f025d67",
          "logical_id": "mc-f6dfb343d6a843799454c598",
          "row_sha256": "25a1350ae7ac6c190cae57706c35985921c494c4b090a30318fc26d39051a586"
        },
        {
          "content_sha256": "d3fe392c7718f758d5be75eded00ba5d7e11ee73997764ee6b693ae34530639a",
          "logical_id": "mc-315521cbea3d61b699c57c01",
          "row_sha256": "8b1d3c86e1cc9a0ff590723ec9520d191162a2dd9e3394712bb45ccf9769dbe1"
        },
        {
          "content_sha256": "36a286c52e25fe150d47f93d1c9c87075c6994e666efddd0c4485f57261658d7",
          "logical_id": "mc-879fac50921ad524b439c624",
          "row_sha256": "477c96da776d20d9f0b301b8fde3ef8833b64bbc218bf6eac39bfee84e992576"
        },
        {
          "content_sha256": "ec0e4a8253cc03fff906403f05bb5c96b543e6d66b4b2760a05e7041c4e14269",
          "logical_id": "mc-beed8ffc12a497ed91a95d0a",
          "row_sha256": "61742e1322bcce346e0c3809686c5cd6c266227c4c3e20d63f9c7f982bcf7cdd"
        },
        {
          "content_sha256": "5af45392d09ffd8ea06db292bc30195e23c0b3b3ee792c8ad417913fcd2c2cf6",
          "logical_id": "mc-f1be8807a2aa399b0bd38aab",
          "row_sha256": "ff8d79f18f8bb89e9bf2eb1370e49c9487d3d77e125b30df610577565c97df6f"
        },
        {
          "content_sha256": "256cdeef2cbfcd1c93af8084f2ff0424983684b19ddee380b50e705542ffc657",
          "logical_id": "mc-b498f29892d5db45bfd87e4f",
          "row_sha256": "37161120e6ed486ceb6d0bc218bf7fab8b002cbf1b7e662e053df72191a1f698"
        },
        {
          "content_sha256": "f1675ed6531d97b99684e0b5be16cc6d1a8032f696f146dde76ac60f8d19ee00",
          "logical_id": "mc-01c401f0b87f8a8a6bc0026b",
          "row_sha256": "b295f985b830947946f43b24490d5f4f4cbcb40269768d4c5ff4c51567bb4e1e"
        },
        {
          "content_sha256": "75bfe426f0fdbfd7201f91aceabb577dea641e7de6333ae603df127fad23d07f",
          "logical_id": "mc-63ec0c40480143b82350e469",
          "row_sha256": "638f2287f2f8d9410a8596c52a244e3ed28b1ee1b6d1e8216ab6fb98a0f58b2b"
        }
      ],
      "sha256": "7dc3756e4ceb2a263c3e65f94d94926cc04b16c7fa51f8b8b50e396cbf60dbc3",
      "sheet_name": "cards",
      "table_sha256": "ed9684a392ab87e1647d6ea910cce690f71922d8b5e91d9cba266c62a335de4f",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 3854,
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
          "content_sha256": "c6489d54510d9c1db3e5230dc85deb807f607537010f1f51fcbba065738a648a",
          "logical_id": "mc-3d7b7882d5fe98bf89ce8f11",
          "row_sha256": "ef143ed62ca48cf6de2b5f09f5f12d5c88f47610668b4bf81a0971ddd3dd8489"
        }
      ],
      "sha256": "c2ebdb8edde8ccafd8ee6c53b0143305eba54fc0d9d3513b5d89fb60a890c4e0",
      "sheet_name": "cards",
      "table_sha256": "955e7d3549c6708bca853745ad0021fd5e8a5544efcee8c8f3394a31e3066314",
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
