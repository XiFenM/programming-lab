---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "ecff96b0cf2fb24cb264a45e65b34bcc73d60ff7eb0dbb58498def15f93ad4b6",
  "candidate_sha256": "55575d4b42b8d30535448c966a7d148e3219cf1bae985516d02eb2bad7734bc5",
  "cards": [
    {
      "content_sha256": "90afab22ec3bcff7f2c4b45273dfcf08f96c63dbac07c7968103e1376b866b07",
      "content_summary": "解释 softmax 中负无穷 padding 不污染 max 与指数和的闭合机制",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "softmax-math",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 softmax 中负无穷 padding 不污染 max 与指数和的闭合机制"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-85fe37304bbbe805507fa2a3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1a461056707a3f59c79d848648d84d53d284a2f16c8c7115401461eac89200d8",
      "content_summary": "区分本课 softmax 接口的空 batch 与空归约维度约定",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-softmax",
        "fact_scope": {
          "kind": "snapshot",
          "product": "programming-lab triton lesson02",
          "version": "2026-08-07 learning baseline"
        },
        "recall_target": "区分本课 softmax 接口的空 batch 与空归约维度约定"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a0616b26964c9ef9372bef32",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0cdc278278b1bdc0ef92b38da7dc02374737a6426c6176a516b616033c3c0d26",
      "content_summary": "判断 softmax 行和归一化不变量属于输出而非输入",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "softmax-math",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "判断 softmax 行和归一化不变量属于输出而非输入"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9bb771500be5bf1f92614113",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c596ba8c9119ee2da9a20dba65531e2f9c0a382824654f13c33e60bbb34b1f5b",
      "content_summary": "解释本课 tl.range num_stages 描述同 program 内跨迭代流水机会的作用域",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-softmax",
        "fact_scope": {
          "kind": "snapshot",
          "product": "programming-lab triton lesson02",
          "version": "2026-08-07 learning baseline"
        },
        "recall_target": "解释本课 tl.range num_stages 描述同 program 内跨迭代流水机会的作用域"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-2c14f887e9971035fd276088",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "784cb379e739552bc6b84da497d953cbc30a73ee054dafc23cee602d8b3d9fe5",
      "content_summary": "解释增加软件流水资源压力为何可能先减少并行驻留容量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-execution",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释增加软件流水资源压力为何可能先减少并行驻留容量"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-fe47de7ce75e682e7494cc9c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "213f9f7e34167e7d43f20fd2c2ce4c21c03a56bc581d8b3d45aa4e456f008793",
      "content_summary": "区分 occupancy 的 warp 驻留容量含义与执行单元忙碌程度",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-execution",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分 occupancy 的 warp 驻留容量含义与执行单元忙碌程度"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c913f6453bf2816a27739147",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "822d8a6d796966bb6ea069da0ad546d37c657df24e7e2ed2a6376677ddb207ea",
      "content_summary": "用商余数唯一性证明静态 grid-stride 行分配不漏不重",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "parallel-indexing",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用商余数唯一性证明静态 grid-stride 行分配不漏不重"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-6a3bd974f47fdf662ef670cc",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "af5a344deecaa15b2eb6f34c90b971358108d40a5d05823a990b62ddc24bab38",
      "content_summary": "解释本课 grid 等于行数时没有同 program 跨行迭代可供流水",
      "dependency_content_sha256": {
        "mc-2c14f887e9971035fd276088": "c596ba8c9119ee2da9a20dba65531e2f9c0a382824654f13c33e60bbb34b1f5b",
        "mc-6a3bd974f47fdf662ef670cc": "822d8a6d796966bb6ea069da0ad546d37c657df24e7e2ed2a6376677ddb207ea"
      },
      "depends_on": [
        "mc-2c14f887e9971035fd276088",
        "mc-6a3bd974f47fdf662ef670cc"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-softmax",
        "fact_scope": {
          "kind": "snapshot",
          "product": "programming-lab triton lesson02",
          "version": "2026-08-07 learning baseline"
        },
        "recall_target": "解释本课 grid 等于行数时没有同 program 跨行迭代可供流水"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e088d59bc183346ef7718aa1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "38c10b117be76427c3abf734fddb7b4e0a07ebce792100aa163cf257512e928f",
      "content_summary": "解释更多在途迭代为何可能在较低 occupancy 下仍改善延迟隐藏",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-execution",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释更多在途迭代为何可能在较低 occupancy 下仍改善延迟隐藏"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-44d3da87054aeaef39448cf4",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d6a7e9515dce84aa7189b94a29e61f934bf58473f390449b5365fdd7e304556d",
      "content_summary": "说明资源记录与默认 grid 必须来自实际 launch 的同一编译特化",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-performance-evidence",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "说明资源记录与默认 grid 必须来自实际 launch 的同一编译特化"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-14e074440686c51694404e59",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e6da2e38373ca4f6bce7cecd61f8855d10771e7ee3d3ae9563d6f5839d167a11",
      "content_summary": "区分资源理论 occupancy 与实际 launch 数量及运行时 achieved occupancy",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-performance-evidence",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分资源理论 occupancy 与实际 launch 数量及运行时 achieved occupancy"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e7250d3c9195bcac9febca8b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cc8875368793ab02dada7e5dbf5a2a52228d09c36fd4b037fa0722acdd5dae8b",
      "content_summary": "界定准备后 wrapper 调用的 benchmark 计时边界",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-benchmark-method",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "界定准备后 wrapper 调用的 benchmark 计时边界"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a6376571125a23f801d94f15",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4391927de7ca58e8f37eabb2e02e483450cb676aa498a3d4205ff339f5001d75",
      "content_summary": "区分独立功能测试与 benchmark 对正确性和性能证据的职责",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-benchmark-method",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分独立功能测试与 benchmark 对正确性和性能证据的职责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-41745e10797fdfa3f4097eec",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e29937c276f35a17fb6b4ae011fc58be9e675581134c57bc8bcf570aeb58d3d0",
      "content_summary": "界定 stages 与默认 grid 同时变化时性能比较支持的因果范围",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-performance-evidence",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "界定 stages 与默认 grid 同时变化时性能比较支持的因果范围"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f17f63dac191a159febbc944",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "269e5d9db70e6d8cf5408f54e4d8df8d54066e50f9067bf302611b57964e7ca7",
      "content_summary": "解释直接稳定计算 log-softmax 如何避免概率下溢后取对数丢失有限值",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "softmax-math",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释直接稳定计算 log-softmax 如何避免概率下溢后取对数丢失有限值"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-40a03076a6306ec969dbdd18",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fd52990d95363f1a6ce9cf324859ba8598d5919b1ade450d7b503ef4fe1c5a3f",
      "content_summary": "综合说明本课增加 stages 不保证提速的流水作用域和驻留资源权衡",
      "dependency_content_sha256": {
        "mc-2c14f887e9971035fd276088": "c596ba8c9119ee2da9a20dba65531e2f9c0a382824654f13c33e60bbb34b1f5b",
        "mc-44d3da87054aeaef39448cf4": "38c10b117be76427c3abf734fddb7b4e0a07ebce792100aa163cf257512e928f",
        "mc-e088d59bc183346ef7718aa1": "af5a344deecaa15b2eb6f34c90b971358108d40a5d05823a990b62ddc24bab38",
        "mc-f17f63dac191a159febbc944": "e29937c276f35a17fb6b4ae011fc58be9e675581134c57bc8bcf570aeb58d3d0",
        "mc-fe47de7ce75e682e7494cc9c": "784cb379e739552bc6b84da497d953cbc30a73ee054dafc23cee602d8b3d9fe5"
      },
      "depends_on": [
        "mc-2c14f887e9971035fd276088",
        "mc-44d3da87054aeaef39448cf4",
        "mc-e088d59bc183346ef7718aa1",
        "mc-f17f63dac191a159febbc944",
        "mc-fe47de7ce75e682e7494cc9c"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "gpu-performance-evidence",
        "fact_scope": {
          "kind": "snapshot",
          "product": "programming-lab triton lesson02",
          "version": "2026-08-07 learning baseline"
        },
        "recall_target": "综合说明本课增加 stages 不保证提速的流水作用域和驻留资源权衡"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-5a4591a30e434953f66de828",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cbde9ba14a38e41686baf54ac331f7e390708a080449276b2b5b4eca8ca3d900",
      "content_summary": "综合说明准备后 wrapper 性能比较的计时和证据边界",
      "dependency_content_sha256": {
        "mc-14e074440686c51694404e59": "d6a7e9515dce84aa7189b94a29e61f934bf58473f390449b5365fdd7e304556d",
        "mc-41745e10797fdfa3f4097eec": "4391927de7ca58e8f37eabb2e02e483450cb676aa498a3d4205ff339f5001d75",
        "mc-a6376571125a23f801d94f15": "cc8875368793ab02dada7e5dbf5a2a52228d09c36fd4b037fa0722acdd5dae8b",
        "mc-e7250d3c9195bcac9febca8b": "e6da2e38373ca4f6bce7cecd61f8855d10771e7ee3d3ae9563d6f5839d167a11",
        "mc-f17f63dac191a159febbc944": "e29937c276f35a17fb6b4ae011fc58be9e675581134c57bc8bcf570aeb58d3d0"
      },
      "depends_on": [
        "mc-14e074440686c51694404e59",
        "mc-41745e10797fdfa3f4097eec",
        "mc-a6376571125a23f801d94f15",
        "mc-e7250d3c9195bcac9febca8b",
        "mc-f17f63dac191a159febbc944"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "gpu-performance-evidence",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "综合说明准备后 wrapper 性能比较的计时和证据边界"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-d6afcb3c2c8463b1444bbe94",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "68ce3a8d53ae9479e275838b3272c4d525d179757eb54835317b4fd0b643309b",
  "manifest_payload_sha256": "eba574418543ac33ae14c1f80fcc0f49cc70b154c0ca7a29a17f39d4d6f3af2b",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 3430,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-02-fused-softmax-correction.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "213f9f7e34167e7d43f20fd2c2ce4c21c03a56bc581d8b3d45aa4e456f008793",
          "logical_id": "mc-c913f6453bf2816a27739147",
          "row_sha256": "6c265c5d388e6c882a3409d1d456977bf47ee93dd83c941efab35ebcf17d4a1a"
        }
      ],
      "sha256": "9ed395e5bb083ecad4c5c573df28ffed06932a479f1ab9f9d71d0a450193371a",
      "sheet_name": "cards",
      "table_sha256": "3927ef09230ee847704b94eefbb7b891929c72d1b432d2bc367db98243688812",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 13963,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-02-fused-softmax-technical-qa.xlsx",
      "row_count": 14,
      "rows": [
        {
          "content_sha256": "90afab22ec3bcff7f2c4b45273dfcf08f96c63dbac07c7968103e1376b866b07",
          "logical_id": "mc-85fe37304bbbe805507fa2a3",
          "row_sha256": "e244a5afc2282b5313230b2c903b552c98c3a6384264343c7ff0d657225c8777"
        },
        {
          "content_sha256": "1a461056707a3f59c79d848648d84d53d284a2f16c8c7115401461eac89200d8",
          "logical_id": "mc-a0616b26964c9ef9372bef32",
          "row_sha256": "e67f1684eb0ee3af85f75f99c304c39bf7e52b9a12c0a4a85316841c9a6666f3"
        },
        {
          "content_sha256": "0cdc278278b1bdc0ef92b38da7dc02374737a6426c6176a516b616033c3c0d26",
          "logical_id": "mc-9bb771500be5bf1f92614113",
          "row_sha256": "fcbc50f6cb492f905d26d00abd572e8d914c5abb4dac19621e6164d10b38e7f9"
        },
        {
          "content_sha256": "c596ba8c9119ee2da9a20dba65531e2f9c0a382824654f13c33e60bbb34b1f5b",
          "logical_id": "mc-2c14f887e9971035fd276088",
          "row_sha256": "d2bbe6682665a221d226223d26a0837a90eaf4aa9607dfdff3c8171273c06c49"
        },
        {
          "content_sha256": "784cb379e739552bc6b84da497d953cbc30a73ee054dafc23cee602d8b3d9fe5",
          "logical_id": "mc-fe47de7ce75e682e7494cc9c",
          "row_sha256": "a02ba4771e2f8e4491df21d2189b4fe1fa224d9b44e218d01924b70d12a179c8"
        },
        {
          "content_sha256": "822d8a6d796966bb6ea069da0ad546d37c657df24e7e2ed2a6376677ddb207ea",
          "logical_id": "mc-6a3bd974f47fdf662ef670cc",
          "row_sha256": "4b0e969e222c76162b3fc58fd68f3a51ad6333b0efdfa75d8cb3f3c368d7871b"
        },
        {
          "content_sha256": "af5a344deecaa15b2eb6f34c90b971358108d40a5d05823a990b62ddc24bab38",
          "logical_id": "mc-e088d59bc183346ef7718aa1",
          "row_sha256": "304100515a8427b9f59f14c51a336456084da9497c813a68ee609a43aafc09d3"
        },
        {
          "content_sha256": "38c10b117be76427c3abf734fddb7b4e0a07ebce792100aa163cf257512e928f",
          "logical_id": "mc-44d3da87054aeaef39448cf4",
          "row_sha256": "d38ba0406305e76f9f059c1f2486a6dd4962b79f7255d0664b8252c484f24b7f"
        },
        {
          "content_sha256": "d6a7e9515dce84aa7189b94a29e61f934bf58473f390449b5365fdd7e304556d",
          "logical_id": "mc-14e074440686c51694404e59",
          "row_sha256": "a62360b62e0e61daa406ffaa86c98ad32fcceca8ff0120c947666a0e6071958c"
        },
        {
          "content_sha256": "e6da2e38373ca4f6bce7cecd61f8855d10771e7ee3d3ae9563d6f5839d167a11",
          "logical_id": "mc-e7250d3c9195bcac9febca8b",
          "row_sha256": "87e2abe53ccbb503adf0e3fa615d028cd7ff67321c4d1309b84a45ac80528411"
        },
        {
          "content_sha256": "cc8875368793ab02dada7e5dbf5a2a52228d09c36fd4b037fa0722acdd5dae8b",
          "logical_id": "mc-a6376571125a23f801d94f15",
          "row_sha256": "95b1412df9c2dfb1338db82caf06955b8c3ac5807c53b6ddb4b885918bcfb0a9"
        },
        {
          "content_sha256": "4391927de7ca58e8f37eabb2e02e483450cb676aa498a3d4205ff339f5001d75",
          "logical_id": "mc-41745e10797fdfa3f4097eec",
          "row_sha256": "104c461492cd743a46144999a6b1aa0fc17ffe14e84380200631da3dd6fd6884"
        },
        {
          "content_sha256": "e29937c276f35a17fb6b4ae011fc58be9e675581134c57bc8bcf570aeb58d3d0",
          "logical_id": "mc-f17f63dac191a159febbc944",
          "row_sha256": "63a5b734bed586fceb671fc04b04a49ac76bb1a2e79162ec906b257790d2d73f"
        },
        {
          "content_sha256": "269e5d9db70e6d8cf5408f54e4d8df8d54066e50f9067bf302611b57964e7ca7",
          "logical_id": "mc-40a03076a6306ec969dbdd18",
          "row_sha256": "e68b63145b83b413ae6e2e66fdb8d89e0f12bab866dd069ab20d9a5a43ea8413"
        }
      ],
      "sha256": "d46f3fe11ab6304fa9383bc5e03ac8efb7babbadaf914e215fbd688aeff32b76",
      "sheet_name": "cards",
      "table_sha256": "3bc971c771658c189488a62471b6f592383c8123021082a142b3eb0d090a9019",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 5046,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-02-fused-softmax-oral.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "fd52990d95363f1a6ce9cf324859ba8598d5919b1ade450d7b503ef4fe1c5a3f",
          "logical_id": "mc-5a4591a30e434953f66de828",
          "row_sha256": "4268eab49e72611a735ffdf1ad0297082b1d88f69a933d137f6a75a4ed0b88d6"
        },
        {
          "content_sha256": "cbde9ba14a38e41686baf54ac331f7e390708a080449276b2b5b4eca8ca3d900",
          "logical_id": "mc-d6afcb3c2c8463b1444bbe94",
          "row_sha256": "26208078924597c96e5f2b48a10a0b830e2283fdb3300e4288753e8983224fa6"
        }
      ],
      "sha256": "a2f39e818aadffba3867493d3bcd82ac007d8b731ac72c153f3c901a570e97eb",
      "sheet_name": "cards",
      "table_sha256": "1dfe32e5f5f9d4c5638b6a654882eef2861e11bd320ac2d6d01b2f208f551a45",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "491ce1c1c95e4de6397a9c6a4f1313d093de55a01025810c62b25c058c60f5c7",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "softmax-log",
      "path": "docs/triton-learning/logs/2026-08-07-fused-softmax.md",
      "sha256": "12f4e78d92ec0101c2c17adf3e613a3512ae6087eb37a8a68ebd36965eff8617",
      "summary": "第02课已核验结构化日志；按冻结 A–E 段原消息编号追溯；未直接消费 raw 对话，不纳入未完成性能因果研究。"
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

导入文件：[triton-lesson-02-fused-softmax-correction.xlsx](triton-lesson-02-fused-softmax-correction.xlsx)（1 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-02-fused-softmax-technical-qa.xlsx](triton-lesson-02-fused-softmax-technical-qa.xlsx)（14 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-02-fused-softmax-oral.xlsx](triton-lesson-02-fused-softmax-oral.xlsx)（2 张卡）
