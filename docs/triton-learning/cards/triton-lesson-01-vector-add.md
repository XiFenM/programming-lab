---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "0b5cf9688b8a4573d61f6534ef3ea0eb992c3ef2e2c89de5af61ee0422014698",
  "candidate_sha256": "076a2a8ef6f3fd1c2eaba333e6e2aaba78be20a1d38909007f4c5e23f4fafa86",
  "cards": [
    {
      "content_sha256": "5ab82964188d29fc800eee19335354fbdbd023a469ca6fbe2d16da7023b57a57",
      "content_summary": "补足尾块读取场景，定义局部指针与 false 位置，保留真实错误并解释形状来源。",
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
      "content_sha256": "83c48d58b060ae7262aafa3f807176d52751344e9101ffb6862987684ec8eb0b",
      "content_summary": "明确 load 后归约的完整场景，以四位置例子解释污染路径及归约前修正。",
      "dependency_content_sha256": {
        "mc-dbb876a849a86c5fef87e9ed": "5ab82964188d29fc800eee19335354fbdbd023a469ca6fbe2d16da7023b57a57"
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
        "summary": "已重新对照本课 card-01 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b33a963bd82a489ecd6e0c3080dc8064bfa50dbee363171c1006d692f503dd83",
      "content_summary": "为条件写回定义长度、边界和业务条件，以比较方向变化解释 sentinel 失效。",
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
      "content_sha256": "396831528c7611a8c92ebf2a16d5abb2187d60b43143c29c340b35ea00e4f191",
      "content_summary": "限定合法输出地址，补具体前后值及 load/store 差别，说明未初始化输出边界。",
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
      "content_sha256": "85761aba07fbaa2400e76696bf6975bf98fe3fe19167b92d15cd50e523cc5fde",
      "content_summary": "说明 constexpr 用于块形状的场景，区分源码写死、特化固定和不同 launch 选值。",
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
      "content_sha256": "4cd8824ff6b0c8565842900320a1b3c7868103ad32cf4cc278911482467185b1",
      "content_summary": "以 arange 的明确用法定义 BLOCK_SIZE，分开 program、逻辑 tensor 与线程/warp。",
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
      "content_sha256": "7d11ab6822c52cc3ac2b6e12e4d9d2faf70d43f85924eada7774c9b8a770304f",
      "content_summary": "补切片输入例子、stride 单位及具体地址错位，串联 wrapper 契约与访存实现。",
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
      "content_sha256": "dcfd4d176fd09689d91886e9b59e2fff53ee4449d34c028497b72d6e022f3623",
      "content_summary": "补整块/尾块比较背景，定义比值公式全部符号，解释指标提升与真实流量的区别。",
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
      "content_sha256": "ba73207f5be03337c90507d4d87297d2cb5b876b625ff687ab890c0dea5254f0",
      "content_summary": "定义 do_bench 与时间单位，区分总采样预算和一次调用的短测量窗口。",
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
      "content_sha256": "207c02abd44d43d0e17ea3017eb449750cc6b7375fbef563a1cb90b44be278b7",
      "content_summary": "说明批量设计的动机、被测成本与场景变化，避免把两种延迟直接替换。",
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
      "content_sha256": "72c65963f0a28be3ba8f83d028807c237ea174d1e3a2929665c47b8db050fe3b",
      "content_summary": "补实验预测、5% 判据与事后发现的完整背景，区分原规则结果和物理结论。",
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
      "content_sha256": "cac53a684504b45911af911b60c77648377d493ed442ff72c74d2b126f955877",
      "content_summary": "给出尾块条件访存的两种因果解释，分开逻辑请求、硬件事务与执行开销。",
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
      "content_sha256": "b4e3fb1a94c404558696bb5be545bef701489c2220a8ee8809332cef9567452d",
      "content_summary": "口述题补全尾块读取到归约再到写回的任务，答案独立覆盖五个原有评分锚点。",
      "dependency_content_sha256": {
        "mc-03f7ee3f9b01c0044dd900b5": "83c48d58b060ae7262aafa3f807176d52751344e9101ffb6862987684ec8eb0b",
        "mc-111385513b8b0e97334ae3ee": "cac53a684504b45911af911b60c77648377d493ed442ff72c74d2b126f955877",
        "mc-76c2a1b0b86707e61910facc": "396831528c7611a8c92ebf2a16d5abb2187d60b43143c29c340b35ea00e4f191",
        "mc-dbb876a849a86c5fef87e9ed": "5ab82964188d29fc800eee19335354fbdbd023a469ca6fbe2d16da7023b57a57",
        "mc-f50b2e34931b504fad4ce2b1": "b33a963bd82a489ecd6e0c3080dc8064bfa50dbee363171c1006d692f503dd83"
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
      "review_resolution": {
        "summary": "已重新对照本课 card-02, card-13, card-04, card-01, card-03 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dfe82c4b88747c81c0dc59e3f5619b946ae184807e5b82d5ed63b2db3a5e43f4",
      "content_summary": "口述题明确尾块微小差异任务，完整串联指标、采样、批量和事前判据。",
      "dependency_content_sha256": {
        "mc-526b34ca3272ac96162c4ef8": "ba73207f5be03337c90507d4d87297d2cb5b876b625ff687ab890c0dea5254f0",
        "mc-aa96ca5a69a65b8c5200a9b5": "72c65963f0a28be3ba8f83d028807c237ea174d1e3a2929665c47b8db050fe3b",
        "mc-be35b4a473f21cbc5da83fef": "207c02abd44d43d0e17ea3017eb449750cc6b7375fbef563a1cb90b44be278b7",
        "mc-c30f86b46d850889b795fd81": "dcfd4d176fd09689d91886e9b59e2fff53ee4449d34c028497b72d6e022f3623"
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
      "review_resolution": {
        "summary": "已重新对照本课 card-10, card-12, card-11, card-09 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson01-structured"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "8bdebeb71122d13e28fcd3adab2cbd24da07dda0ee8fab103d9905d21c2c3e2f",
  "manifest_payload_sha256": "490923c9dfb29fd7d35f98a0e18459fe56342f0a28528abf5820ce715ee3ba60",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5522,
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
          "content_sha256": "5ab82964188d29fc800eee19335354fbdbd023a469ca6fbe2d16da7023b57a57",
          "logical_id": "mc-dbb876a849a86c5fef87e9ed",
          "row_sha256": "476e0c28848174a47e563c4e77f2175a3ce194e6eae69b127c01dda27291e35f"
        },
        {
          "content_sha256": "b33a963bd82a489ecd6e0c3080dc8064bfa50dbee363171c1006d692f503dd83",
          "logical_id": "mc-f50b2e34931b504fad4ce2b1",
          "row_sha256": "a5ff10121a9593d5989f35e3153a39c27b86078024d7eda98cfe324097f1c1cc"
        }
      ],
      "sha256": "600d1a16d1448044d0d4ff43e19349556e7669ada571b8efdfa3e51dd36488ab",
      "sheet_name": "cards",
      "table_sha256": "1011887297986366dec1c4a91872542cb0742aea11026e0df627054c5486b0ae",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 16452,
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
          "content_sha256": "83c48d58b060ae7262aafa3f807176d52751344e9101ffb6862987684ec8eb0b",
          "logical_id": "mc-03f7ee3f9b01c0044dd900b5",
          "row_sha256": "bb6a4322bab79d9a7cd4c193553ce07ecd20655351e82de42be9c85fa77a8c35"
        },
        {
          "content_sha256": "396831528c7611a8c92ebf2a16d5abb2187d60b43143c29c340b35ea00e4f191",
          "logical_id": "mc-76c2a1b0b86707e61910facc",
          "row_sha256": "5657d9ff1366b23a898c8dc02e3fd5f2274d4a38c89035d1425bdb91d2e0f109"
        },
        {
          "content_sha256": "85761aba07fbaa2400e76696bf6975bf98fe3fe19167b92d15cd50e523cc5fde",
          "logical_id": "mc-6f60ba491472d6a0fe36fd43",
          "row_sha256": "1c7acd463322f61e529fbb087dae886ef2b59b55bc8c009ba859ad5956d7dd3b"
        },
        {
          "content_sha256": "1d346774a1f685f209fd32546869c9bdd8179007b4be227feec15da94f4bdaf4",
          "logical_id": "mc-c007594b3df346419ac002f0",
          "row_sha256": "3821c41cb77b1b9a6322b1d7b626ee3e26237fca82dc4267b4ef538e3fe5091c"
        },
        {
          "content_sha256": "4cd8824ff6b0c8565842900320a1b3c7868103ad32cf4cc278911482467185b1",
          "logical_id": "mc-a133c2ec1286463f6931b612",
          "row_sha256": "ce3cc44f504d3b85e335bf5f202121650f4eb25cd508d4b3b8dd3ce4b3b7f316"
        },
        {
          "content_sha256": "7d11ab6822c52cc3ac2b6e12e4d9d2faf70d43f85924eada7774c9b8a770304f",
          "logical_id": "mc-657e6c116e07f637d2eb7754",
          "row_sha256": "dfc0e3c3d685a78c71291417f8e951aac5a712b0f2adf1ce72633cdd16ec011c"
        },
        {
          "content_sha256": "dcfd4d176fd09689d91886e9b59e2fff53ee4449d34c028497b72d6e022f3623",
          "logical_id": "mc-c30f86b46d850889b795fd81",
          "row_sha256": "b2cb98802dda44a8c9e45d3223416b2940b2b35f5ebb8e464771003bc1d8b74d"
        },
        {
          "content_sha256": "ba73207f5be03337c90507d4d87297d2cb5b876b625ff687ab890c0dea5254f0",
          "logical_id": "mc-526b34ca3272ac96162c4ef8",
          "row_sha256": "294d7161e7b0e0eb781c6a888f1657d6fe1939e065e950763869ffbf6e55cb42"
        },
        {
          "content_sha256": "207c02abd44d43d0e17ea3017eb449750cc6b7375fbef563a1cb90b44be278b7",
          "logical_id": "mc-be35b4a473f21cbc5da83fef",
          "row_sha256": "d37e3189454ff94bc38807b9dee82e88acbdff7d0bed87e367c01d329eb23640"
        },
        {
          "content_sha256": "72c65963f0a28be3ba8f83d028807c237ea174d1e3a2929665c47b8db050fe3b",
          "logical_id": "mc-aa96ca5a69a65b8c5200a9b5",
          "row_sha256": "0611d792a02e86c70312ee0d536bbf29cbd86c6604014d8883d6645e6f0304a9"
        },
        {
          "content_sha256": "cac53a684504b45911af911b60c77648377d493ed442ff72c74d2b126f955877",
          "logical_id": "mc-111385513b8b0e97334ae3ee",
          "row_sha256": "065bfd8dceaf8c1c70282bfa01804ee4b83a5e43e1888cdfb23c2e730368593a"
        }
      ],
      "sha256": "5585a54e80fd8621b82a9b438955920c2a2ca4c73e667bf2ef21e8fcf4bf34d9",
      "sheet_name": "cards",
      "table_sha256": "373ecdebe6e033aab43d02920d283dfc4be3a66e9d15e11209cbad59b1ed64fa",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 5869,
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
          "content_sha256": "b4e3fb1a94c404558696bb5be545bef701489c2220a8ee8809332cef9567452d",
          "logical_id": "mc-1f8aa5f84db63f091affc38c",
          "row_sha256": "d424d17f914e3c0b11611eb255396ee4a8d3e718b4a61e1003e0ff0e1d1ddd23"
        },
        {
          "content_sha256": "dfe82c4b88747c81c0dc59e3f5619b946ae184807e5b82d5ed63b2db3a5e43f4",
          "logical_id": "mc-7387175e84296c256e43fd20",
          "row_sha256": "4e2042116b8652930c8d9f12ffadc45b65813f9858256c5946711cb8501bfb86"
        }
      ],
      "sha256": "3c4339e31fab0dcb10821df83df7a8d71ba27bd4786e8446464967469005bc95",
      "sheet_name": "cards",
      "table_sha256": "a02b217097d431fe8a18f245601c14ff30804defd586e4d9d25952135982fdb9",
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
