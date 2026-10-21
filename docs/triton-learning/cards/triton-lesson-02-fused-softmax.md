---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "83b8a558e8221a0ec8d82caa0e95d75caf8782fe96fc319269ac235717ec5e32",
  "candidate_sha256": "09f721e72a1dd212db42ab105a21e81ca36444585b2b52bf36d76805e651ce7c",
  "cards": [
    {
      "content_sha256": "4ed77bcd3d9903374938b7035c003d99130ebc54ac12eef0286f5e5c01730495",
      "content_summary": "题面写明补到 next_power_of_2(N)；零填充对分母的影响改为“必然增大（下溢除外）”。",
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
      "content_sha256": "5c4f1ddececc83f95fad391002628346ea76ce84b11085d8742513164ec67781",
      "content_summary": "新增：分子分母同乘 exp(−m) 故结果不变；指数输入 ≤ 0 防上溢；非有限输入仍可能得 NaN。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 softmax 先减行最大值为何结果不变、能防止什么以及不能保证什么"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1cbf2e7f12f4c8144f731151",
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
      "content_sha256": "a7ee368f2ae6754e42eff8d0a458b3d674765ea8147caf87c3e7be3c0e4c9713",
      "content_summary": "新增：逐步计数 naive 读 5MN+2M、写 3MN+2M，对比 fused 2MN，比值 4+2/N；省的是 DRAM 往返而非计算。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "估算 naive 与 fused softmax 的全局内存搬运量并说明 fusion 省下什么"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1f92d177462e95f9f49f06eb",
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
      "content_sha256": "5ca8b76b4343f37dddb8404ec8285ddb8afb2c21d45be54c444286e953da2078",
      "content_summary": "去掉附带的是非问，结论直接给出作用域（同 program 行循环的跨迭代在途）；worker 误解移入边界；正面写明 Triton 3.7.1。",
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
      "content_sha256": "f552c51141f5044396c6476a87e3f70cb8d8cb2f18220ad5a7b5e0cc1a9a6113",
      "content_summary": "原 05 由技术问答改为真实纠错卡：保留原话，点明错在把资源代价落到单个 stage 变慢。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正把流水资源代价归为单个 stage 变慢的误解:资源压力先减少每 sm 的驻留数"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e722fbbdd4ce4c40df8796d5",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "652f01b7950c5273b04ff5b1906d02b4b8652359e3ac9a2ce6c66f44748abddb",
      "content_summary": "场景不再写出定义；正确栏给出驻留容量定义；说明首句界定错误范围（“不一定用得好”是对的）。",
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
      "content_sha256": "27f1ddb6d453eeb7db5cec4338eabd08e8e7cee818a8bb91af1cd58be80e506d",
      "content_summary": "原 08 由技术问答改为真实纠错卡：保留跨 program 交错的原话，区分硬件调度与 tl.range 跨迭代流水。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正把不同 program 交错执行当作 tl.range 跨迭代流水的误解"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-4b58cd831ef5e06216ffdd48",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3602bc5f70bad11890768aa4cd9670e9733939bb0dcff339256a6aad418704af",
      "content_summary": "题面加上“tl.range 行循环的 num_stages”区分线索，避免与 matmul 的 kernel 参数 num_stages 混答。",
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
      "content_sha256": "a30010c27ed0d7e68e8fca31629a10df92cb9bddbbb53cd7609671f9d261a2fc",
      "content_summary": "改为情境题（官方 648 能否沿用 → 用自身特化的资源），补 864 反例与按 N 取块大小的排查点；降为 B。",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c514589006e0edafa504efd9ddf1388583a3314aaec04f72b5eaba724d1d59fc",
      "content_summary": "是非题改为“该怎样算”；运行时 achieved occupancy 标为延伸；降为 B。",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b1d7417227359e3dbcdede871a7eafdb4e41a796b4b62c069cf4a717ba327a99",
      "content_summary": "题面改为反驳“只测 kernel 才公平”的情境，考计时边界由要回答的问题决定；降为 B。",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f1a443ae088b21e4ef6e2d61371eb0de9376801bba4bf7402aa4cace2c3305d6",
      "content_summary": "新增：整行一个静态块的原因（编译期块形状、整行归约）、越过 2 的幂即换特化、须装进片上资源的上限。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释整行由一个 program 的静态 2 的幂块负责的原因、代价与上限"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b91e2f8be53d73a72abc622c",
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
      "content_sha256": "fe99556fda57bbd12d9c0d7dab13f086ddeb3ca1e44a5ca50baaa9360852d954",
      "content_summary": "是非题改为“比较的究竟是什么”，题面给出 432/540/324 的联动 grid；降为 B。",
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
      "priority": 4,
      "quality": "B",
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
      "content_sha256": "fac292dbf590eba8481021f87f6db5808c47a045d823b0fe81e059888d7d7b4b",
      "content_summary": "写明听众与 Triton 3.7.1；子卡 05、08 换成两张新纠错卡；参考回答压缩到 60 秒内。",
      "dependency_content_sha256": {
        "mc-2c14f887e9971035fd276088": "5ca8b76b4343f37dddb8404ec8285ddb8afb2c21d45be54c444286e953da2078",
        "mc-44d3da87054aeaef39448cf4": "3602bc5f70bad11890768aa4cd9670e9733939bb0dcff339256a6aad418704af",
        "mc-4b58cd831ef5e06216ffdd48": "27f1ddb6d453eeb7db5cec4338eabd08e8e7cee818a8bb91af1cd58be80e506d",
        "mc-e722fbbdd4ce4c40df8796d5": "f552c51141f5044396c6476a87e3f70cb8d8cb2f18220ad5a7b5e0cc1a9a6113",
        "mc-f17f63dac191a159febbc944": "fe99556fda57bbd12d9c0d7dab13f086ddeb3ca1e44a5ca50baaa9360852d954"
      },
      "depends_on": [
        "mc-2c14f887e9971035fd276088",
        "mc-44d3da87054aeaef39448cf4",
        "mc-4b58cd831ef5e06216ffdd48",
        "mc-e722fbbdd4ce4c40df8796d5",
        "mc-f17f63dac191a159febbc944"
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
        "summary": "已依据更新后的 card-04、card-09、card-14 与新纠错卡 pm-pipeline-correction、resource-residency-correction 复核：作用域、单次迭代无跨行流水、延迟隐藏与驻留权衡、联动归因四个锚点都有子卡支撑；参考回答约 350 字，可在 60 秒内讲完。"
      },
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e5898cce23900516c2d90ae9be3702972129f683fd7eda6f449b5466bd93dafd",
      "content_summary": "新增：静态 grid-stride 与动态任务队列的分配时机对比，判断依据是任务来源与成本差异。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "比较静态 grid-stride 与动态任务队列两种 persistent 的任务分配方式与适用负载"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-312ed81b22df320ca2241130",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "softmax-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "b41e10f0a0ed4df5bd646e36a8c7876776bfc8221dfa01bc8eaa0fa5369d2e47",
  "manifest_payload_sha256": "3b477124877a309d94d9fd706ac061895aa4a95eb2204f336988f0273e597c45",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 7503,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-02-fused-softmax-correction.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "f552c51141f5044396c6476a87e3f70cb8d8cb2f18220ad5a7b5e0cc1a9a6113",
          "logical_id": "mc-e722fbbdd4ce4c40df8796d5",
          "row_sha256": "a9fc1a6b735c00d4713ddd913419ba1a414959b903385f23c41ace1bb4cec9d8"
        },
        {
          "content_sha256": "652f01b7950c5273b04ff5b1906d02b4b8652359e3ac9a2ce6c66f44748abddb",
          "logical_id": "mc-c913f6453bf2816a27739147",
          "row_sha256": "f61766146ea5361133545f035f9295f31e92970c3837ba69b9c074c47b496ed1"
        },
        {
          "content_sha256": "27f1ddb6d453eeb7db5cec4338eabd08e8e7cee818a8bb91af1cd58be80e506d",
          "logical_id": "mc-4b58cd831ef5e06216ffdd48",
          "row_sha256": "a8a910a6ff39dc8afda4c31625670c98fecf607658f791bf9efe70457db4c2e3"
        }
      ],
      "sha256": "a1664f4f9e6fe4dc5aa165085b4fae5ee72ba1558cacebdd4d93bca8c0565cfd",
      "sheet_name": "cards",
      "table_sha256": "a97f45451a7639fec1ec21413b1b3c7485feecf81877d7d108097a5e904bbf3a",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 22538,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-02-fused-softmax-technical-qa.xlsx",
      "row_count": 13,
      "rows": [
        {
          "content_sha256": "4ed77bcd3d9903374938b7035c003d99130ebc54ac12eef0286f5e5c01730495",
          "logical_id": "mc-85fe37304bbbe805507fa2a3",
          "row_sha256": "d5ca19073e30600c3e30097a46427ce196c6ab8299a1a9bee31f0b92063e1e0b"
        },
        {
          "content_sha256": "5c4f1ddececc83f95fad391002628346ea76ce84b11085d8742513164ec67781",
          "logical_id": "mc-1cbf2e7f12f4c8144f731151",
          "row_sha256": "ab9fab8c87df35880336d9529dc0e8392f41f8841c4fa413189111049c439b8b"
        },
        {
          "content_sha256": "a7ee368f2ae6754e42eff8d0a458b3d674765ea8147caf87c3e7be3c0e4c9713",
          "logical_id": "mc-1f92d177462e95f9f49f06eb",
          "row_sha256": "8b02941b13daf05a7b52885d700338522a6a4f05a7f693cbdf54eb92c7bd44d4"
        },
        {
          "content_sha256": "5ca8b76b4343f37dddb8404ec8285ddb8afb2c21d45be54c444286e953da2078",
          "logical_id": "mc-2c14f887e9971035fd276088",
          "row_sha256": "cb059dd1dbd073d54a0eff72fa1f61c54d2931677fdce6a85a540320a85e1480"
        },
        {
          "content_sha256": "2d62441c50d10b09d9daa48825f9f6aa7d31269e2937de5629f8e8228f3583f1",
          "logical_id": "mc-6a3bd974f47fdf662ef670cc",
          "row_sha256": "24d08e4d3fbae2a248b61d628a78b45c5208d128a93dd7273c17d466ff2e29b8"
        },
        {
          "content_sha256": "3602bc5f70bad11890768aa4cd9670e9733939bb0dcff339256a6aad418704af",
          "logical_id": "mc-44d3da87054aeaef39448cf4",
          "row_sha256": "8bf813b98858c9cf6c26f73423e1a3bfb693022eb786372ba7e445b87fa73bd6"
        },
        {
          "content_sha256": "a30010c27ed0d7e68e8fca31629a10df92cb9bddbbb53cd7609671f9d261a2fc",
          "logical_id": "mc-14e074440686c51694404e59",
          "row_sha256": "b5202435de79f954950aad0664ab44b463cddbec142731a39e2931bac4f0edd2"
        },
        {
          "content_sha256": "c514589006e0edafa504efd9ddf1388583a3314aaec04f72b5eaba724d1d59fc",
          "logical_id": "mc-e7250d3c9195bcac9febca8b",
          "row_sha256": "c8a0dbaf5e7a868913353b8896b6f9a27827a11ec210637865fa891508e21ed6"
        },
        {
          "content_sha256": "b1d7417227359e3dbcdede871a7eafdb4e41a796b4b62c069cf4a717ba327a99",
          "logical_id": "mc-a6376571125a23f801d94f15",
          "row_sha256": "f10621e29b666e618042a65b38e7ddf456d659fa97aeecb7852375302abaf566"
        },
        {
          "content_sha256": "f1a443ae088b21e4ef6e2d61371eb0de9376801bba4bf7402aa4cace2c3305d6",
          "logical_id": "mc-b91e2f8be53d73a72abc622c",
          "row_sha256": "dadccfd116fdd9e86b28bd097fdde70d102a1ed1b5b451150c9c45a994500896"
        },
        {
          "content_sha256": "fe99556fda57bbd12d9c0d7dab13f086ddeb3ca1e44a5ca50baaa9360852d954",
          "logical_id": "mc-f17f63dac191a159febbc944",
          "row_sha256": "6cf76abea310e3a325463de8290f7a99608e0c7b56b60d94acbe995717f59508"
        },
        {
          "content_sha256": "5dd6cb5d641dc1169f597bd7975543655944c8cde714a049e0c7d0a8efd24662",
          "logical_id": "mc-40a03076a6306ec969dbdd18",
          "row_sha256": "efe778e1e2a397fbe2268ab562fb3c4873d4c3010c303b2a2a23943ebc8bc0b0"
        },
        {
          "content_sha256": "e5898cce23900516c2d90ae9be3702972129f683fd7eda6f449b5466bd93dafd",
          "logical_id": "mc-312ed81b22df320ca2241130",
          "row_sha256": "0e55b4c011efb9c2daae011fa2dc549f7b6c349424c2351962ddca7fdd006130"
        }
      ],
      "sha256": "5a22fa9e59c031ebc60de59cb0960bd8a8e02a2f2ad6dcf00a4ba4e33f803648",
      "sheet_name": "cards",
      "table_sha256": "303f42421dc53b57521daac4b0a25cc3467857e9478fb93d06f645e9ae6c03cf",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4284,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-02-fused-softmax-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "fac292dbf590eba8481021f87f6db5808c47a045d823b0fe81e059888d7d7b4b",
          "logical_id": "mc-5a4591a30e434953f66de828",
          "row_sha256": "1ded434ac84976f5e305a16255a7632aa12367a7a50596029ceb7d1dac3e3019"
        }
      ],
      "sha256": "d80401ed687ae587897dc0154b65efbf1b86f2c5d1b51a6bf9e3e88c2de021e7",
      "sheet_name": "cards",
      "table_sha256": "eb4007a3e14b63c63d83036b4b0455fdfb59cb7b050f0862daa7624291423cd9",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "1b2377df7b2e1c6b177b867d3a272c112d412f4bbbd0230e340caed8d664fb15",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "softmax-log",
      "path": "docs/triton-learning/logs/2026-08-07-fused-softmax.md",
      "sha256": "44335bf79ea2330369e998c0b83a173fd98473bb2c9a0554d7916a3fecaac432",
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

导入文件：[triton-lesson-02-fused-softmax-correction.xlsx](triton-lesson-02-fused-softmax-correction.xlsx)（3 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-02-fused-softmax-technical-qa.xlsx](triton-lesson-02-fused-softmax-technical-qa.xlsx)（13 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-02-fused-softmax-oral.xlsx](triton-lesson-02-fused-softmax-oral.xlsx)（1 张卡）
