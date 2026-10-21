---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "e2f26e0adffd37fc2334cd0f424ac3b7397411b1119958e1cc3022bc1db21cd4",
  "candidate_sha256": "28c66bf8e43ec69d0da09580c9f950d09297dc688313e58bd48f63abef950f4a",
  "cards": [
    {
      "content_sha256": "5befb3808f31b09a9e81fb633f8f9f486abd05ebeb35e220077ca21c35a4956c",
      "content_summary": "题面给出 load 代码与输出分配，只问 shape 来源；错误栏改用两句原话，说明首句点明错误范围。",
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
      "content_sha256": "bd243921021b95fe51529bd2a4c83830a9c825c09290ad4bdcedc25ade4a9b75",
      "content_summary": "四位置例子解释污染路径；归约前处理补成单位元规则（sum 0、max −∞、prod 1、min +∞）。",
      "dependency_content_sha256": {
        "mc-dbb876a849a86c5fef87e9ed": "5befb3808f31b09a9e81fb633f8f9f486abd05ebeb35e220077ca21c35a4956c"
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
      "review_resolution": {
        "summary": "已依据更新后的 card-01（错误栏改为两句原话、题面给出 load 代码与输出分配）复核本卡：归约污染的因果链、单位元规则与 store mask 边界仍成立，回忆目标未变。"
      },
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "df58bf30257189c8b21ec8ad50b2e517174766576637958cc2db52e59bbec33e",
      "content_summary": "原红色纠错卡改为技术问答：学习者的 -inf 推导是对的；用改变比较方向的情境考查为何要显式合并边界谓词。",
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
        "recall_target": "解释条件写回的 store mask 为什么要显式合并边界条件与数值条件"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-94d70de637bd66de3c7cd62d",
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
      "content_sha256": "2ef74b2bf36407ce7a06d00623c1829db5fc5c50aea9861445e3af401ca92886",
      "content_summary": "二选一改为情境题，考“固定”的范围；补每个新取值首次使用触发 JIT 编译、之后复用；降为 B。",
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
      "content_sha256": "1d346774a1f685f209fd32546869c9bdd8179007b4be227feec15da94f4bdaf4",
      "content_summary": "给出向量覆盖任务与 autotune 时机，明确 callable/tuple 的判断条件。",
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
      "content_sha256": "3ca35bb29b51315b0a9ea9483d4c4116daee59c471dfd5ef41d51f2a045c180f",
      "content_summary": "是非题改为分层定位题：BLOCK_SIZE 属于 block-tensor 层，与 threads/warps 的关系由编译器映射决定。",
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
      "content_sha256": "83190965f7060511fd80f127c162d8693394b176c1bf57700b5475b79a1bbdfa",
      "content_summary": "stride 例子改写为存储偏移 i×2（逻辑位置 1 → base[2]），并升为 A。",
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
      "content_sha256": "1ce8742461975b7d8bb759f3d2060a4176a9fd16eed3e880d1ccfbd271cf07fb",
      "content_summary": "是非题改为推导比值并说明上升来源；原“如何解读”并入结论；降为 B。",
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
      "content_sha256": "08b950876e3e8b9aa6c4df90083a71579a7ef1680a0dc875f0bd1ea3fe4e93b7",
      "content_summary": "新增：fp32 向量加法每元素 12 字节对 1 次加法，解释带宽受限、系数 3 与有效带宽口径。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "估算向量加法每元素的字节与运算量,解释其受带宽限制及有效带宽系数 3"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-62c1c3a3ea283d9cae71d828",
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
      "content_sha256": "91e81b2a47450c49ad4a4f6daf2f73e0d525c71299468dce512c0a613594e610",
      "content_summary": "合并原 10（rep 是总采样预算）与原 11（批量计时换了场景）为一条闭合链，补 do_bench 每样本清 L2 的机制。",
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
        "recall_target": "解释 do_bench 的 rep 与批量计时各改变什么,以及批量平均为何不能替代单次调用结果"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0f622230eb49cd382735cd28",
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
      "content_sha256": "b5f2df3bee54aca58a47cb81a2f3dc02cb56609c20c9e949a377020f57489a53",
      "content_summary": "新增：launch 异步使 CPU 计时漏算、首次 JIT 使其多算；给出同步与预热做法及 do_bench 的处理。",
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
        "recall_target": "解释 gpu launch 异步与首次 jit 为何让 cpu 计时失真及正确计时做法"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-30f3c87b5a0f4efe37caffc4",
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
      "content_sha256": "59562092220967f96ef867796be85b878485249deabbe8ba8861c2aacd8e566e",
      "content_summary": "二选一改为真实误区情境；正面写明 Triton 3.7.1 与 NVIDIA PTX；事务粒度压入边界并注明证据范围。",
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
      "content_sha256": "332ebe0e99b2c08554b0e5b7e3024d168c1025bb7cc6b226e089403e2533e5f4",
      "content_summary": "写明听众；四个锚点对应题面三处并各有子卡支撑；子卡改为 01、02、新 03、13（原 04 删除）。",
      "dependency_content_sha256": {
        "mc-03f7ee3f9b01c0044dd900b5": "bd243921021b95fe51529bd2a4c83830a9c825c09290ad4bdcedc25ade4a9b75",
        "mc-111385513b8b0e97334ae3ee": "59562092220967f96ef867796be85b878485249deabbe8ba8861c2aacd8e566e",
        "mc-94d70de637bd66de3c7cd62d": "df58bf30257189c8b21ec8ad50b2e517174766576637958cc2db52e59bbec33e",
        "mc-dbb876a849a86c5fef87e9ed": "5befb3808f31b09a9e81fb633f8f9f486abd05ebeb35e220077ca21c35a4956c"
      },
      "depends_on": [
        "mc-03f7ee3f9b01c0044dd900b5",
        "mc-111385513b8b0e97334ae3ee",
        "mc-94d70de637bd66de3c7cd62d",
        "mc-dbb876a849a86c5fef87e9ed"
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
      "review_resolution": {
        "summary": "已依据更新后的 card-01、card-02、store-mask-boundary、card-13 复核：四个评分锚点分别由这些子卡支撑；原 04 删除后，‘false store 不写入、原值保留’由 card-13 支撑；参考回答约 335 字，可在 60 秒内讲完。"
      },
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "afafabad61ac1156951668a1534425948fd6b939e5babe846a93ceacb17f0562",
  "manifest_payload_sha256": "ecfe6a3c024d56470367beaccaf6ec947d452aad37719451790af78c46dde6f1",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 4463,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-01-vector-add-correction.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "5befb3808f31b09a9e81fb633f8f9f486abd05ebeb35e220077ca21c35a4956c",
          "logical_id": "mc-dbb876a849a86c5fef87e9ed",
          "row_sha256": "816522eb9b9835cf12c4890f00deb16de198e7f8793ebb5a2f4a955a96dee61d"
        }
      ],
      "sha256": "990d0d8852be6f4fa29fc1b208440bcb0c95c61252687984f7e92a898bde7c4d",
      "sheet_name": "cards",
      "table_sha256": "9b19caa0d8a85d235f9d679fccdb8c6dd252a3a401992d4fa37e8272cfcbab34",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 18741,
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
          "content_sha256": "bd243921021b95fe51529bd2a4c83830a9c825c09290ad4bdcedc25ade4a9b75",
          "logical_id": "mc-03f7ee3f9b01c0044dd900b5",
          "row_sha256": "cb53a48106e2340313a32aaeb6e0c96ac38999b8a140ece4955e30447dfdf6bf"
        },
        {
          "content_sha256": "df58bf30257189c8b21ec8ad50b2e517174766576637958cc2db52e59bbec33e",
          "logical_id": "mc-94d70de637bd66de3c7cd62d",
          "row_sha256": "a178f76245cf7b323e01cf63d4efbf87596c63c4e59911843a5d6f72b1bed38a"
        },
        {
          "content_sha256": "2ef74b2bf36407ce7a06d00623c1829db5fc5c50aea9861445e3af401ca92886",
          "logical_id": "mc-6f60ba491472d6a0fe36fd43",
          "row_sha256": "968234d5723906cc32bcb0f949da62f2327a8d5d5df15ba04a5c9007bc300f7c"
        },
        {
          "content_sha256": "1d346774a1f685f209fd32546869c9bdd8179007b4be227feec15da94f4bdaf4",
          "logical_id": "mc-c007594b3df346419ac002f0",
          "row_sha256": "3821c41cb77b1b9a6322b1d7b626ee3e26237fca82dc4267b4ef538e3fe5091c"
        },
        {
          "content_sha256": "3ca35bb29b51315b0a9ea9483d4c4116daee59c471dfd5ef41d51f2a045c180f",
          "logical_id": "mc-a133c2ec1286463f6931b612",
          "row_sha256": "7f253048ab87680b1f90393b5834722209381173ad754903e2a090d97f1f9777"
        },
        {
          "content_sha256": "83190965f7060511fd80f127c162d8693394b176c1bf57700b5475b79a1bbdfa",
          "logical_id": "mc-657e6c116e07f637d2eb7754",
          "row_sha256": "db9bade25a7f1be53ce0c69fa90cf0720c030f1a80210ba157fd24b7ba0bcfae"
        },
        {
          "content_sha256": "1ce8742461975b7d8bb759f3d2060a4176a9fd16eed3e880d1ccfbd271cf07fb",
          "logical_id": "mc-c30f86b46d850889b795fd81",
          "row_sha256": "e1dfdcad25b4059e320f372cc273cc39710d42da7a3a44d22f82b172278fd4bb"
        },
        {
          "content_sha256": "08b950876e3e8b9aa6c4df90083a71579a7ef1680a0dc875f0bd1ea3fe4e93b7",
          "logical_id": "mc-62c1c3a3ea283d9cae71d828",
          "row_sha256": "414570db2847bfeff433d1867072b6af8acf61ec15d95ba2c99aedd2adf73b02"
        },
        {
          "content_sha256": "91e81b2a47450c49ad4a4f6daf2f73e0d525c71299468dce512c0a613594e610",
          "logical_id": "mc-0f622230eb49cd382735cd28",
          "row_sha256": "cc9c0f1765eff3fe4f52cef02639f80d9b88384e9bf161125bc2faa0d45b6245"
        },
        {
          "content_sha256": "b5f2df3bee54aca58a47cb81a2f3dc02cb56609c20c9e949a377020f57489a53",
          "logical_id": "mc-30f3c87b5a0f4efe37caffc4",
          "row_sha256": "5bdfda532195f59c4a66e3303aaea36dfe8ebcf37c91ed4b10971a09fc31fc47"
        },
        {
          "content_sha256": "59562092220967f96ef867796be85b878485249deabbe8ba8861c2aacd8e566e",
          "logical_id": "mc-111385513b8b0e97334ae3ee",
          "row_sha256": "556968bfa9e7d03193090aed90e94ae3943bfa2ac08e4db12c4595c7205561b0"
        }
      ],
      "sha256": "5cf62b4604610aaccce5725eb59dd5b85713557f2015168bf85c369dd0834046",
      "sheet_name": "cards",
      "table_sha256": "1c2900bba30f551e353bb4eb547a68fae4f7c87c61c4b3b6bde011fe41be69ed",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4126,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-01-vector-add-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "332ebe0e99b2c08554b0e5b7e3024d168c1025bb7cc6b226e089403e2533e5f4",
          "logical_id": "mc-1f8aa5f84db63f091affc38c",
          "row_sha256": "0493875e7bbcee9d4e6545e8faa9399988e82d83b58d34d339ff0a8ce735ef15"
        }
      ],
      "sha256": "37cb328d430492aaf655743477d484e911352e66a8b585353da93c1ccd62b30f",
      "sheet_name": "cards",
      "table_sha256": "4be3c4cfd1afeed4c6ecd4a82a7f076ebc4611c9bc5a06c4a22e47126ab13101",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "5c57b97987c72d324c0b8ecf43f25eef60f6ca37f5ece4de6644565c83df87cc",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson01-structured",
      "path": "docs/triton-learning/logs/2026-07-27-vector-add.md",
      "sha256": "fd35cf8d15f471bd99f209791d53a5367de1b1c3a143849ff0eac886de9383aa",
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

导入文件：[triton-lesson-01-vector-add-correction.xlsx](triton-lesson-01-vector-add-correction.xlsx)（1 张卡）

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

导入文件：[triton-lesson-01-vector-add-oral.xlsx](triton-lesson-01-vector-add-oral.xlsx)（1 张卡）
