---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "7c7398b28792655918680f548dc84c971fdb84c60403e7b3154495dbb0bb1a13",
  "candidate_sha256": "3aa960a39942529cc4ea78c25df7320077357aefd0baece5ab2427e42cb86abb",
  "cards": [
    {
      "content_sha256": "894df417a31ef17943835be7800a38ae3ed0e007d8c90d9b8fa065a3128bad20",
      "content_summary": "保留真实错误，区分局部 pointer tensor 的静态形状与完整输入、输出分配。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "确定 masked load 的结果形状由局部 pointer tensor 决定"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-dbb876a849a86c5fef87e9ed",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9e1ee0d1d3f6ad26184cf346eb97f9196cab44611408231d4eb7fe66d956e190",
      "content_summary": "由保留形状到无效值进入归约的闭合因果链，不把 mask 当作自动过滤。",
      "dependency_content_sha256": {
        "mc-dbb876a849a86c5fef87e9ed": "894df417a31ef17943835be7800a38ae3ed0e007d8c90d9b8fa065a3128bad20"
      },
      "depends_on": [
        "mc-dbb876a849a86c5fef87e9ed"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "解释 load mask 无法自动排除归约中无效 lane 的因果链"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-03f7ee3f9b01c0044dd900b5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "64f5a8f5df03ffd6d6185d2ce71d8fb39aba054ae1b59ccdd9ee75bfdab0a25d",
      "content_summary": "保留真实原话，将地址边界谓词与填充值的数值语义分开。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "使用 boundary_mask 与 condition 的合取保证条件写回的越界安全"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f50b2e34931b504fad4ce2b1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "eded799acb59804041c1881f4024dc6f931470c03f74d27f64d5a27aff68bd0e",
      "content_summary": "只考 false store 的副作用，不混入 load 返回值或 reduction 的第二个问题。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "确定合法地址上 masked store 的 false lane 保留原值"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-76c2a1b0b86707e61910facc",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bfa1b868de760d9f553c8eba951d4e4a874b9141a44d6ecb9cc8a25ea09a035f",
      "content_summary": "消除把编译期参数等同于 Python 源码永远写死的混淆。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "区分 constexpr 在单次特化内固定与跨 launch 可变化"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6f60ba491472d6a0fe36fd43",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bb3250ed232d46049a027c439779491400ad4d8355a901e7b8339fbe89d74d41",
      "content_summary": "以 grid 依赖参数的确定时机作单一判断，不把动态 shape 泛化成必须 callable。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "判断 grid 依赖尚待绑定的 meta-parameters 时采用 callable grid"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c007594b3df346419ac002f0",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "47e64a076035fac3308c2d843f25c6feaf6d500aa0bd90f8aa3c6199a9a2e40d",
      "content_summary": "建立 program、块级逻辑 tensor 与硬件执行层的分工，防止机械套用线程模型。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "区分 triton block_size 的逻辑位置数与实际 gpu 线程数"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a133c2ec1286463f6931b612",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e2c276d3b74c00ead85cba40887886d902caef689346542deba74bd3f73609e7",
      "content_summary": "把本课连续性限制解释为访存模型的前提，不扩张到未学习的多维 stride 接口。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "由一维地址计算判断连续布局假设与 stride 支持条件"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-657e6c116e07f637d2eb7754",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1486750db58aa996c8af58ef0981cfdc462fe8bfeb239274b7fbc9a160d12068",
      "content_summary": "将有效带宽的数学变化与硬件流量和优化归因分开，作为通用带宽口径主卡。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释有效 gb/s 上升不能直接证明真实 dram 带宽或代码优化提升"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c30f86b46d850889b795fd81",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "366407284ecbcb2392efb2e47bc7b0ad3560e26a4f44640553420308a740c7ba",
      "content_summary": "区分增加总采样预算与延长单个样本窗口，保留明确 API 版本范围。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "说明 do_bench 的 rep 是总采样预算而非单次 kernel 计时间隔"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-526b34ca3272ac96162c4ef8",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0b5b3bf55d618932f9512b76e7c6f2096cc177ae248d688b693bae0ba4319b97",
      "content_summary": "以缓存和发射场景变化解释为什么批量计时必须单列口径。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释批量计时改变执行场景而不能直接替代单次调用结果"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-be35b4a473f21cbc5da83fef",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0af415b0735ab50d261447f3fcb7d42aad4efc4571d45d6b2409225d446b95d5",
      "content_summary": "保留真实 Review 中的后验阈值问题，形成可迁移的实验报告原则。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "在发现反证阈值不合理后仍按原规则报告结果并改进后续实验"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-aa96ca5a69a65b8c5200a9b5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3c710057d90e2a282b9beb8e9e7a9ef66329811ad65c7a05686c3244b8bc27c7",
      "content_summary": "依据日志中已核对的 predicate 行为解释无效访存消失，区分语义与硬件事务。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "解释 false predicate 直接禁用 lane 访存及其与物理事务粒度的区别"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-111385513b8b0e97334ae3ee",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c90e6199fca3484655f55988a567805416a799af3d38e837f8ca46abe9a4cfe4",
      "content_summary": "综合五张已核验子卡，在一分钟内贯通形状、读取、归约和写回，明确成本边界。",
      "dependency_content_sha256": {
        "mc-03f7ee3f9b01c0044dd900b5": "9e1ee0d1d3f6ad26184cf346eb97f9196cab44611408231d4eb7fe66d956e190",
        "mc-111385513b8b0e97334ae3ee": "3c710057d90e2a282b9beb8e9e7a9ef66329811ad65c7a05686c3244b8bc27c7",
        "mc-76c2a1b0b86707e61910facc": "eded799acb59804041c1881f4024dc6f931470c03f74d27f64d5a27aff68bd0e",
        "mc-dbb876a849a86c5fef87e9ed": "894df417a31ef17943835be7800a38ae3ed0e007d8c90d9b8fa065a3128bad20",
        "mc-f50b2e34931b504fad4ce2b1": "64f5a8f5df03ffd6d6185d2ce71d8fb39aba054ae1b59ccdd9ee75bfdab0a25d"
      },
      "depends_on": [
        "mc-03f7ee3f9b01c0044dd900b5",
        "mc-111385513b8b0e97334ae3ee",
        "mc-76c2a1b0b86707e61910facc",
        "mc-dbb876a849a86c5fef87e9ed",
        "mc-f50b2e34931b504fad4ce2b1"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "综合解释固定形状尾块中 load、归约、store 与 predicate 的职责和边界"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-1f8aa5f84db63f091affc38c",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "18040c20f17635ad95a94f930cc4d381c40013ac870d00e7ecdd87e155d03cee",
      "content_summary": "综合四张子卡给出限定测量口径的性能解释，避免把波动、场景变化或改判据写成优化证据。",
      "dependency_content_sha256": {
        "mc-526b34ca3272ac96162c4ef8": "366407284ecbcb2392efb2e47bc7b0ad3560e26a4f44640553420308a740c7ba",
        "mc-aa96ca5a69a65b8c5200a9b5": "0af415b0735ab50d261447f3fcb7d42aad4efc4571d45d6b2409225d446b95d5",
        "mc-be35b4a473f21cbc5da83fef": "0b5b3bf55d618932f9512b76e7c6f2096cc177ae248d688b693bae0ba4319b97",
        "mc-c30f86b46d850889b795fd81": "1486750db58aa996c8af58ef0981cfdc462fe8bfeb239274b7fbc9a160d12068"
      },
      "depends_on": [
        "mc-526b34ca3272ac96162c4ef8",
        "mc-aa96ca5a69a65b8c5200a9b5",
        "mc-be35b4a473f21cbc5da83fef",
        "mc-c30f86b46d850889b795fd81"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "综合解释微小性能差异时的指标、采样口径与事前判据边界"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-7387175e84296c256e43fd20",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "8bdebeb71122d13e28fcd3adab2cbd24da07dda0ee8fab103d9905d21c2c3e2f",
  "manifest_payload_sha256": "3d9a387a515c1f568f36b42201a871731a0e1d2483ee60ec5eae3bbd6e476537",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 4220,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-01-vector-add-correction.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "894df417a31ef17943835be7800a38ae3ed0e007d8c90d9b8fa065a3128bad20",
          "logical_id": "mc-dbb876a849a86c5fef87e9ed",
          "row_sha256": "97d476511625a4b7d8df062c5decb9dfb93a667438a355908498b98452894a47"
        },
        {
          "content_sha256": "64f5a8f5df03ffd6d6185d2ce71d8fb39aba054ae1b59ccdd9ee75bfdab0a25d",
          "logical_id": "mc-f50b2e34931b504fad4ce2b1",
          "row_sha256": "10a09e655f9353d63acb21efa31de9ba54e4b6c2d80a41ae829a73f8cfa3fa2a"
        }
      ],
      "sha256": "d380739ed201d13b5e0bc9e0e94346b0b0345e847095745b9c0d4925666ef996",
      "sheet_name": "cards",
      "table_sha256": "27a9de004bdffde5e8bea79d7a642142aabb33499b8013d19701c6457594321f",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 10796,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-01-vector-add-technical-qa.xlsx",
      "row_count": 11,
      "rows": [
        {
          "content_sha256": "9e1ee0d1d3f6ad26184cf346eb97f9196cab44611408231d4eb7fe66d956e190",
          "logical_id": "mc-03f7ee3f9b01c0044dd900b5",
          "row_sha256": "018adac23d1e563ec2b3e686f4c87aa8cb008a5ca0c16925fa1a094b21540841"
        },
        {
          "content_sha256": "eded799acb59804041c1881f4024dc6f931470c03f74d27f64d5a27aff68bd0e",
          "logical_id": "mc-76c2a1b0b86707e61910facc",
          "row_sha256": "92daf9d076dc2d40f115330911522ef06e677bd1411cb5cb2640216f3874c203"
        },
        {
          "content_sha256": "bfa1b868de760d9f553c8eba951d4e4a874b9141a44d6ecb9cc8a25ea09a035f",
          "logical_id": "mc-6f60ba491472d6a0fe36fd43",
          "row_sha256": "f43f7454f30f90dba5661d8d62558b81ac637095f9ead77fb0623f2cdee38fce"
        },
        {
          "content_sha256": "bb3250ed232d46049a027c439779491400ad4d8355a901e7b8339fbe89d74d41",
          "logical_id": "mc-c007594b3df346419ac002f0",
          "row_sha256": "80e04f8ccccda09f114bce5f034dff8ca32f7dbd71ec9e58b2b349064d486802"
        },
        {
          "content_sha256": "47e64a076035fac3308c2d843f25c6feaf6d500aa0bd90f8aa3c6199a9a2e40d",
          "logical_id": "mc-a133c2ec1286463f6931b612",
          "row_sha256": "28add24b6d99a988be97c8b0b88fa793018c9cf3d35f4b2910ed1dce44b12373"
        },
        {
          "content_sha256": "e2c276d3b74c00ead85cba40887886d902caef689346542deba74bd3f73609e7",
          "logical_id": "mc-657e6c116e07f637d2eb7754",
          "row_sha256": "3394a40558f69b78f49485b4dfe659b446d102e8a21ab419608af209b9e361da"
        },
        {
          "content_sha256": "1486750db58aa996c8af58ef0981cfdc462fe8bfeb239274b7fbc9a160d12068",
          "logical_id": "mc-c30f86b46d850889b795fd81",
          "row_sha256": "42bf0925c809a3e25c6c7dc45f80f54f13eeb54465599a56c97ff14e3e91d257"
        },
        {
          "content_sha256": "366407284ecbcb2392efb2e47bc7b0ad3560e26a4f44640553420308a740c7ba",
          "logical_id": "mc-526b34ca3272ac96162c4ef8",
          "row_sha256": "3a42e6a6d337c30dd01bccf1a631dc147a5d0eea0bc78c853a4364baf7b5903d"
        },
        {
          "content_sha256": "0b5b3bf55d618932f9512b76e7c6f2096cc177ae248d688b693bae0ba4319b97",
          "logical_id": "mc-be35b4a473f21cbc5da83fef",
          "row_sha256": "e8b9597f2f13b7b02a49a87bfdeffb2a79ebe527284102a056c39a0da79e03bc"
        },
        {
          "content_sha256": "0af415b0735ab50d261447f3fcb7d42aad4efc4571d45d6b2409225d446b95d5",
          "logical_id": "mc-aa96ca5a69a65b8c5200a9b5",
          "row_sha256": "a3f1caf848ac40b745a4b26525a240d465154577b49700eb59f81fae73704532"
        },
        {
          "content_sha256": "3c710057d90e2a282b9beb8e9e7a9ef66329811ad65c7a05686c3244b8bc27c7",
          "logical_id": "mc-111385513b8b0e97334ae3ee",
          "row_sha256": "e3950a39481e8cf0321fe572f9c54f15e9dbe65ee968c6f50242cca4c03f84cf"
        }
      ],
      "sha256": "d714a5638cdcf59bc0cbc7a01255e78516c0fa0e13667d4b9402b4e82ff67e88",
      "sheet_name": "cards",
      "table_sha256": "2dbb41908aa0ff90f55f5298867d1dfd4d7a42b44c8137055a119bb68f99ca45",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4784,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-01-vector-add-oral.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "c90e6199fca3484655f55988a567805416a799af3d38e837f8ca46abe9a4cfe4",
          "logical_id": "mc-1f8aa5f84db63f091affc38c",
          "row_sha256": "f64b74da6380498df1ee64baa08f70b2517256786e08d56c39488897d80e114b"
        },
        {
          "content_sha256": "18040c20f17635ad95a94f930cc4d381c40013ac870d00e7ecdd87e155d03cee",
          "logical_id": "mc-7387175e84296c256e43fd20",
          "row_sha256": "6158c75897b55464261284eb1ae0eab199dbb565dc6c7bc76ebc6aeab360ddcd"
        }
      ],
      "sha256": "6810218cdcb5b69dd65e7e280b2ec73df4da1f2a8dec48e4f520d2889df1be7a",
      "sheet_name": "cards",
      "table_sha256": "aa9a3585be4bcfa91efbcf594b0c328607a1a05b5efb1aec475d50bd23fefdb5",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "da387fb664e1acff49af5535a96cf3228f13b4f67f0d631e7fe525ac878b4b54",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson01-structured",
      "path": "docs/triton-learning/logs/2026-07-27-vector-add.md",
      "sha256": "19d038d0239239236e03ccb1343a139c70a35985cfda9ef0ef335c3e225de61b",
      "summary": "已核验结构化日志：L01 向量运算、真实 mask 纠错与基础 Benchmark 复盘；不消费 raw 对话。"
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

导入文件：[triton-lesson-01-vector-add-correction.xlsx](triton-lesson-01-vector-add-correction.xlsx)（2 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-01-vector-add-technical-qa.xlsx](triton-lesson-01-vector-add-technical-qa.xlsx)（11 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-01-vector-add-oral.xlsx](triton-lesson-01-vector-add-oral.xlsx)（2 张卡）
