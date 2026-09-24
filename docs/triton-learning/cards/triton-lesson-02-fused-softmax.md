---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "f1041dcf0ef6e7ff24043edc0d23bf671844ee5e0be39ac9eaeb8d7a79415c12",
  "candidate_sha256": "91268c8666a63a84da5124d05daecc3d814f9eca84263c9fe8fdcfd665ace9b6",
  "cards": [
    {
      "content_sha256": "4b87c511c0408fb58bc5b1dafe173780525f2df02f3718c0f3697345d1f3bf2b",
      "content_summary": "定义按行 softmax 的补齐场景、有效输入前提和 m，串联 max/exp/sum 的正确性。",
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
      "content_sha256": "952be6f18d66688f649d3c95ad81bbf5bd7e72846bda08f5c0aa378a65117ecb",
      "content_summary": "在题面定义 M/N，分别解释空 batch 与空归约域，并保留实现范围。",
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
      "content_sha256": "abb18105a1c07e4a451e6460330985c893bf9d8bfe13b9e8c83fac8b5c123bc6",
      "content_summary": "测试按行计算的 softmax kernel 时，假设每行非空且有效输入都为有限值，我们希望检查“每行元素之和接近 1”这一不变量。应该对输入矩阵 X 还是输出矩阵 Y 求行和，为什么？",
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
      "content_sha256": "17c2cc2bcde5411d47a65816502988474ed18c7475ff2518cba6a841f9554623",
      "content_summary": "定义 persistent 行循环和一次迭代，明确 num_stages 的作用域与数据依赖。",
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
      "content_sha256": "058465854d1e46cdf8b1914f547225393aa2f38193d2ca019a70f996d470627e",
      "content_summary": "补 SM 固定容量和驻留定义，解释资源代价，避免把驻留下降直接说成单阶段变慢。",
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
      "content_sha256": "ebd87915d413ab70afd58f3b77dac009e510bfa65e40b6bf299a939dbb316759",
      "content_summary": "在题面明确性能判断，定义 occupancy 的分子分母并保留真实错误原话。",
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
      "content_sha256": "2d62441c50d10b09d9daa48825f9f6aa7d31269e2937de5629f8e8228f3583f1",
      "content_summary": "题面完整定义静态行分配，公式前定义 r/p/k，分别说明覆盖与唯一性。",
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
      "content_sha256": "29ca21cf0b8b4a321b26a5ec8a90555a3f020c3f0adb3d77d3d824d8cbd24751",
      "content_summary": "定义 M/P 与行分配后推导单迭代情形，区别跨 program 调度和循环流水。",
      "dependency_content_sha256": {
        "mc-2c14f887e9971035fd276088": "17c2cc2bcde5411d47a65816502988474ed18c7475ff2518cba6a841f9554623",
        "mc-6a3bd974f47fdf662ef670cc": "2d62441c50d10b09d9daa48825f9f6aa7d31269e2937de5629f8e8228f3583f1"
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
      "review_resolution": {
        "summary": "已重新对照本课 card-04, card-07 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f46138e0470bdca0bbaa9c414e621e33939278f945a3613d43e965b38b9394af",
      "content_summary": "补保持算法不变的性能比较条件，说明驻留数量与在途迭代各自影响。",
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
      "content_sha256": "9a9e6c008951d001ef176c0c718771f03ad8e956171577d1bbbdc075e8e51e36",
      "content_summary": "解释资源为何参与默认 grid，定义同一特化并补参数对应与排查目标。",
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
      "content_sha256": "8a399b8f1721657a7f1fdafdeedc7c39f9df731a87afd22021199ee08338cef9",
      "content_summary": "定义 grid cap 的来由，分别说明理论容量、全设备启动量和 achieved occupancy。",
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
      "content_sha256": "978810c2f0a0d4449d92c4bc5a39d1d109c19aa3ef16c478f580c9190bcf8231",
      "content_summary": "把准备后 wrapper 定义为实验对象，明确哪些步骤在边界内外与比较条件。",
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
      "content_sha256": "f264b887a93aa2029f5337b2cbca0771f6f03c9f35ae2605c60b480915ca3fa8",
      "content_summary": "解释把正确性检查移出 benchmark 的安排，明确独立测试职责与配置覆盖。",
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
      "content_sha256": "9e1fbb6bfb473905faba63c911ffca3bfe839f64a71dc9175535a05a100b184f",
      "content_summary": "题面重建 stages/资源/grid 联动实验，限定策略比较与后续因果对照。",
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
      "content_sha256": "5dd6cb5d641dc1169f597bd7975543655944c8cde714a049e0c7d0a8efd24662",
      "content_summary": "定义输入、指数和符号与计算目标，完整解释概率下溢及稳定路径的有限结果。",
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
      "content_sha256": "4b8f156d7abc708e7797bc7b62b9dff7224b26d687dbefdaf305dc16dfb0cc91",
      "content_summary": "口述题明示行循环设置，独立串联迭代条件、重叠收益、驻留代价和归因。",
      "dependency_content_sha256": {
        "mc-2c14f887e9971035fd276088": "17c2cc2bcde5411d47a65816502988474ed18c7475ff2518cba6a841f9554623",
        "mc-44d3da87054aeaef39448cf4": "f46138e0470bdca0bbaa9c414e621e33939278f945a3613d43e965b38b9394af",
        "mc-e088d59bc183346ef7718aa1": "29ca21cf0b8b4a321b26a5ec8a90555a3f020c3f0adb3d77d3d824d8cbd24751",
        "mc-f17f63dac191a159febbc944": "9e1fbb6bfb473905faba63c911ffca3bfe839f64a71dc9175535a05a100b184f",
        "mc-fe47de7ce75e682e7494cc9c": "058465854d1e46cdf8b1914f547225393aa2f38193d2ca019a70f996d470627e"
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
      "review_resolution": {
        "summary": "已重新对照本课 card-04, card-09, card-08, card-14, card-05 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "46bb791ce2bb38622ef776869f03e6774bb3d1158451932215e963d5ac4e3dfc",
      "content_summary": "口述题给出审查对象，补齐 wrapper/资源/正确性/因果四条可执行核对线。",
      "dependency_content_sha256": {
        "mc-14e074440686c51694404e59": "9a9e6c008951d001ef176c0c718771f03ad8e956171577d1bbbdc075e8e51e36",
        "mc-41745e10797fdfa3f4097eec": "f264b887a93aa2029f5337b2cbca0771f6f03c9f35ae2605c60b480915ca3fa8",
        "mc-a6376571125a23f801d94f15": "978810c2f0a0d4449d92c4bc5a39d1d109c19aa3ef16c478f580c9190bcf8231",
        "mc-e7250d3c9195bcac9febca8b": "8a399b8f1721657a7f1fdafdeedc7c39f9df731a87afd22021199ee08338cef9",
        "mc-f17f63dac191a159febbc944": "9e1fbb6bfb473905faba63c911ffca3bfe839f64a71dc9175535a05a100b184f"
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
      "review_resolution": {
        "summary": "已重新对照本课 card-10, card-13, card-12, card-11, card-14 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "68ce3a8d53ae9479e275838b3272c4d525d179757eb54835317b4fd0b643309b",
  "manifest_payload_sha256": "b93c21933f13087d1d7ba3bc2a4c5b9c37fc8a61c50f12d9d4a32fbdc4cd2b33",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 4038,
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
          "content_sha256": "ebd87915d413ab70afd58f3b77dac009e510bfa65e40b6bf299a939dbb316759",
          "logical_id": "mc-c913f6453bf2816a27739147",
          "row_sha256": "c459903b0db2390a81bb870d8daf3d458ec5fbcd7b2ac2e2b5c2eec6f1a9ae2c"
        }
      ],
      "sha256": "69541eb54d4a935061adcfcc2355ee8ddc2c0a3c20a8537ceacc65d5b45af123",
      "sheet_name": "cards",
      "table_sha256": "c48d45497b6a5ffb8ff7a4e47e85288ae2d91295e8306affb5b42b4e8314b238",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 22496,
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
          "content_sha256": "4b87c511c0408fb58bc5b1dafe173780525f2df02f3718c0f3697345d1f3bf2b",
          "logical_id": "mc-85fe37304bbbe805507fa2a3",
          "row_sha256": "d859a7e3de79f25d30107bbdd7cc53c159a7992c3e6b35b4f22b8a064f7b13d4"
        },
        {
          "content_sha256": "952be6f18d66688f649d3c95ad81bbf5bd7e72846bda08f5c0aa378a65117ecb",
          "logical_id": "mc-a0616b26964c9ef9372bef32",
          "row_sha256": "d391ebc866b160b5638825dcdf11863898a237f9c827a2a26601783efeeae801"
        },
        {
          "content_sha256": "abb18105a1c07e4a451e6460330985c893bf9d8bfe13b9e8c83fac8b5c123bc6",
          "logical_id": "mc-9bb771500be5bf1f92614113",
          "row_sha256": "f4aebf6ff41c31a83ebd88bd8efccc7d60f92d5bffb840a7bedec0a3b25a35c1"
        },
        {
          "content_sha256": "17c2cc2bcde5411d47a65816502988474ed18c7475ff2518cba6a841f9554623",
          "logical_id": "mc-2c14f887e9971035fd276088",
          "row_sha256": "5558da43f5bbd94c90d98f09f912f3e987a2f39e9238a8fad756497589fa3dc1"
        },
        {
          "content_sha256": "058465854d1e46cdf8b1914f547225393aa2f38193d2ca019a70f996d470627e",
          "logical_id": "mc-fe47de7ce75e682e7494cc9c",
          "row_sha256": "474b8c55609bb39b995ad81d5ce0ac00397794a1f5a1205415bab50dee01354d"
        },
        {
          "content_sha256": "2d62441c50d10b09d9daa48825f9f6aa7d31269e2937de5629f8e8228f3583f1",
          "logical_id": "mc-6a3bd974f47fdf662ef670cc",
          "row_sha256": "24d08e4d3fbae2a248b61d628a78b45c5208d128a93dd7273c17d466ff2e29b8"
        },
        {
          "content_sha256": "29ca21cf0b8b4a321b26a5ec8a90555a3f020c3f0adb3d77d3d824d8cbd24751",
          "logical_id": "mc-e088d59bc183346ef7718aa1",
          "row_sha256": "ad1f4ecc16427f015e3408fb8e51fd2dd120c7d6f1d5b1af1bff531fd5a9ef6a"
        },
        {
          "content_sha256": "f46138e0470bdca0bbaa9c414e621e33939278f945a3613d43e965b38b9394af",
          "logical_id": "mc-44d3da87054aeaef39448cf4",
          "row_sha256": "23ae37c27a7b3ce4b1fcbf4a89bdc4b05db4ba9df2fd44700580f8a3e3597acf"
        },
        {
          "content_sha256": "9a9e6c008951d001ef176c0c718771f03ad8e956171577d1bbbdc075e8e51e36",
          "logical_id": "mc-14e074440686c51694404e59",
          "row_sha256": "668598d34527c9ce7bfbd1e0cfc3e338d51df2a3a545b07a4dfdbf3a3cf94190"
        },
        {
          "content_sha256": "8a399b8f1721657a7f1fdafdeedc7c39f9df731a87afd22021199ee08338cef9",
          "logical_id": "mc-e7250d3c9195bcac9febca8b",
          "row_sha256": "b8f51c0e19351a0e3a681210df7e38605ab527be76cc81e918c2cb98b3c82fcc"
        },
        {
          "content_sha256": "978810c2f0a0d4449d92c4bc5a39d1d109c19aa3ef16c478f580c9190bcf8231",
          "logical_id": "mc-a6376571125a23f801d94f15",
          "row_sha256": "ddb93d5752b36f47a141fbb2d73bca00a2268d43752698e4602a624a57461cc4"
        },
        {
          "content_sha256": "f264b887a93aa2029f5337b2cbca0771f6f03c9f35ae2605c60b480915ca3fa8",
          "logical_id": "mc-41745e10797fdfa3f4097eec",
          "row_sha256": "49833e603008439fe94aa999b9f11786d328ec709ba8aeaa915b9f7e0102dbe8"
        },
        {
          "content_sha256": "9e1fbb6bfb473905faba63c911ffca3bfe839f64a71dc9175535a05a100b184f",
          "logical_id": "mc-f17f63dac191a159febbc944",
          "row_sha256": "efba7aa7b2fe3fc3034b0908df379a360b12e4cec35dd0dc3db5a49c3c60b36e"
        },
        {
          "content_sha256": "5dd6cb5d641dc1169f597bd7975543655944c8cde714a049e0c7d0a8efd24662",
          "logical_id": "mc-40a03076a6306ec969dbdd18",
          "row_sha256": "efe778e1e2a397fbe2268ab562fb3c4873d4c3010c303b2a2a23943ebc8bc0b0"
        }
      ],
      "sha256": "8a9cee75297c28473ce88197caf46569b2e4a779d197e5e3ed73bd6444dfbcd9",
      "sheet_name": "cards",
      "table_sha256": "1e00bd65a5d049be376d5e4ec03e3fb524eb5e18990428bdf023c6f3a2789f5b",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 6270,
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
          "content_sha256": "4b8f156d7abc708e7797bc7b62b9dff7224b26d687dbefdaf305dc16dfb0cc91",
          "logical_id": "mc-5a4591a30e434953f66de828",
          "row_sha256": "ea23e5db73d9aacb1c0c8c0908477d80d1b5998553a410b64948c2886b432188"
        },
        {
          "content_sha256": "46bb791ce2bb38622ef776869f03e6774bb3d1158451932215e963d5ac4e3dfc",
          "logical_id": "mc-d6afcb3c2c8463b1444bbe94",
          "row_sha256": "ab916a27069da203879062ef0ba841d9059a869c1cd4cea4143d66831f23e43c"
        }
      ],
      "sha256": "09aff0e4d4d1045a79d9a35993d02db064ecee27233f93e3ae79c6c3e430c17a",
      "sheet_name": "cards",
      "table_sha256": "1a1617f6d79712dd12bb3ea605f5c277c39e5e6f52e5979388a615155360b903",
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
