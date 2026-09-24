---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "bf31e1e426a8c05722d008cf78016af6ed0e8f8d0f9e7a64d89e3b9f1c31465a",
  "candidate_sha256": "16c5cb89bdab6a64b35c39b21eb19b4c55bd2ba0debb9a76261bfd304b35e925",
  "cards": [
    {
      "content_sha256": "b13f7106f0bdb73fb86725fc0e39fff244f49df559c57c809d9df8f41840e415",
      "content_summary": "单个 head 的 Attention 完整计算是什么？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "单个 head 的 attention 完整计算是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-10797edbc02a90f935980a34",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "98bdc89c7bc05c03c1bc2a6fc18b7a1fe8a4645c94a7dfa5887b99ed0040f3cb",
      "content_summary": "FlashAttention 避免了哪项开销？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "flashattention 避免了哪项开销?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6f4b77efdda16289ca9f840e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a4350b49021875db31384f066e7710489b4fe0fcbbe51c5245c7b8e3db1e18fa",
      "content_summary": "前向 grid 怎样分配输出块？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "前向 grid 怎样分配输出块?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3792ef72898b22610a7791b1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6a18b09e02a9ec14aa38bdb469462f25c2d67bdf4e77e461f2b83ce1155df3a7",
      "content_summary": "FP16 的 [BHN,D] 视图怎样定位 token 行？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "fp16 的 [bhn,d] 视图怎样定位 token 行?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-525509f1b67e10f3367a6740",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e8fbf4e1108666d37565a0bb163f6aefcf7b4c4ad266bca8f3ba1499aada1fea",
      "content_summary": "为什么 acc 的形状是 [BLOCK_M,D]？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为什么 acc 的形状是 [block_m,d]?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5b8520cad91de49d0fce0551",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5c8fd292f9ab5e7508e25ad1b4a9ebdfd6b7b6428e122ecaf4e119414e137748",
      "content_summary": "重标定时 exp 与 exp2 怎样匹配？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "重标定时 exp 与 exp2 怎样匹配?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f949a09a279ca9bbaedd40ee",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f5278436eec30dbfa0956d9e2d8447ef9f98b9d58ac7803ba2aa1e37e6234321",
      "content_summary": "新 key 块如何并入在线 softmax 状态？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "新 key 块如何并入在线 softmax 状态?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-55086c744857d6967c992455",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fef9700fec9d72b96219d4f0379550360e61058d695481d30bd190607f2b81e9",
      "content_summary": "m=−∞ 时，l 初始为 1 为什么不污染首块？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "m=−∞ 时,l 初始为 1 为什么不污染首块?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-5fa9999050b2b9eed656dd49",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ef1beaf3a09aac182a654cb84989376158588ad24a0387208c0783c1fa48a20b",
      "content_summary": "causal 前向怎样划分 key 区域？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "causal 前向怎样划分 key 区域?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-36841e7e2e57cd392d7bd040",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "be243dc2d7e4df877bf104a95ad574316b2d8e6862d09e2b51b52a95c9074972",
      "content_summary": "为什么 M=m+log₂(l) 能恢复概率？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为什么 m=m+log2(l) 能恢复概率?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-dfeb90dfa04b47718a46bbbb",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0fac4d63403eb534be4068f439bfc921db7e4392d819fe52b5aa2785113c8911",
      "content_summary": "本课 FP16 前向怎样安排精度？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "本课 fp16 前向怎样安排精度?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-8d6f166747439b6c1751a274",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2f78b683c3c26995deca50415584ba6f91acb000b892ddad6b25526886615474",
      "content_summary": "为什么 p 的分母归约放在转 FP16 之前？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为什么 p 的分母归约放在转 fp16 之前?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e24771d0d0fe04e94cc22fc6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "254f34f83dd4d42d1ef3e7c231b640572c126b9564cbf6bb3133145d43f40faa",
      "content_summary": "新算子的精度应按什么逻辑选择？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "新算子的精度应按什么逻辑选择?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3a13fa0014fc53fab79ffd24",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1c93934a90f65ae5411abe47e46a007ec77c3adc99b8d2c05a996a24fe7bef38",
      "content_summary": "前向保存量、反向临时量和梯度如何区分？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "前向保存量、反向临时量和梯度如何区分?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e3916767857f2d3c67d3f4c6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1848a0ee90badbe9eb63092784e7ee529fe0cc589b7917dc6b1ab30b64cb5c45",
      "content_summary": "所学前后向怎样跨函数和 kernel 传状态？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "所学前后向怎样跨函数和 kernel 传状态?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-963d2f25bb957912e1c6ed99",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a6f125e5988406e26591f64a90d73435694844a58389f57887301e7baaddf33b",
      "content_summary": "Delta 应沿哪个维度归约？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "delta 应沿哪个维度归约?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-08e5a0a6586998294cb74792",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e84e5242c7cec03dd8fab567904d9b648e6c83d8be9edbb5998eff695c198b21",
      "content_summary": "Attention 的反向链怎样闭合？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "attention 的反向链怎样闭合?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-86ae6ff76a84b4c6a1b9232a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b80aadfdccec68af60feac7f38c43caf35e0b4c576523c3eee227e654036c72a",
      "content_summary": "M、Delta 应沿概率块的哪个轴广播？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "m、delta 应沿概率块的哪个轴广播?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9a62292e5f5afbe601084713",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "043eb0d20727faa9f2dc2771b3b4b7bbe4e426fbe5fd004f5f781db48570b60e",
      "content_summary": "何时可以不用 atomic 写回 dK/dV？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "何时可以不用 atomic 写回 dk/dv?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-ac4172de0a8bc2a4d40c0eca",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "308045415c68305fc9845d6c70b46f692d06280820d42fda9e619ab277367cff",
      "content_summary": "causal 反向为什么沿两个方向扫描？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "causal 反向为什么沿两个方向扫描?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-37343051f020c2bb32857654",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ef48e0d7b47f4abb32d200d1f5b0a69de414f36ce66f44b5624ee9924562139f",
      "content_summary": "为什么 dQ 末尾乘 ln2，而 dK 乘 s？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "为什么 dq 末尾乘 ln2,而 dk 乘 s?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a3da6f89f9dfff794380bacf",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d2dfd576dd6a9c70d347ef68a2c40f7208e5a58d03f3a50f9d2b0c3080af5388",
      "content_summary": "descriptor 怎样确定一次 load 读取的块？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "descriptor 怎样确定一次 load 读取的块?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-fe884cab68b5fd014c895d48",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c67c70b95cce455a25e79325b71c02f3ca7344bc15d9a018a6f7018cbd9fa0c3",
      "content_summary": "descriptor 会自动保护当前 head 的边界吗？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "descriptor 会自动保护当前 head 的边界吗?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7b624650264561327c5db3e9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b69a35cb8e7b7d9227b4d3259928c5a5fa9b548e2a0b7876bc7a51468dd9b78c",
      "content_summary": "K/V 补零为什么不能代替无效 key 的 mask？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "k/v 补零为什么不能代替无效 key 的 mask?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e0f9e3ccb87093480e0c4aaf",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f4f50902d8e3b30c0bd4a2f0d8fa67ccfc87a5734f5792bf07c4ba339c5ac244",
      "content_summary": "descriptor 的 padding 能像 other 一样任意指定吗？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "descriptor 的 padding 能像 other 一样任意指定吗?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a0c0488514cc557c23d96e98",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "66cd788f1a6e7b55e41ba3aff5fb324faf19bebb1b006f774005002c0d23efc1",
      "content_summary": "连续张量为什么仍可能不满足 TMA 对齐？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "连续张量为什么仍可能不满足 tma 对齐?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0c544303457fe69beb458570",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c62c5a6d9b9504d3bf6c1dc164fcbeb1b518b67c41c4ad57d4a7cdf2a8d3a371",
      "content_summary": "host descriptor 为何需要 pre-hook 更新块大小？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "tutorial source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "host descriptor 为何需要 pre-hook 更新块大小?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1e17c1d1f03d092cf091e666",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "aae6253dace86ab22c2ee0f8e1443189edd8954092c227ed033722142d366a50",
      "content_summary": "E5M2 与 FP16 的有效精度差在哪里？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "e5m2 与 fp16 的有效精度差在哪里?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-491e7d022820a6bb4bb79c70",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5ed6f8ff339f2a36dcf919bba51156ad1912e0480e7aaf7dbba7a692c780dc1f",
      "content_summary": "两次逆 permute 中间的 contiguous 改变了什么？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "两次逆 permute 中间的 contiguous 改变了什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-12391b0b8209a8b11ff4e0a8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "20860b16d6db474fe79565f8104e1287e7f57fedada63f71d4fd85e1a0144ed0",
      "content_summary": "比较反向结果怎样保证输入条件一致？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch/triton attention correctness test",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "比较反向结果怎样保证输入条件一致?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4fe59a4647c233625e064594",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7fb9f38b8ac0185de49bb1d3fb81aa710562c17c20500d9760befe84e59373bc",
      "content_summary": "反向 FLOP 系数 2.5 说明什么？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "反向 flop 系数 2.5 说明什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-dca496c8a60dd217880d597f",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fa1db0e815f098d4fef8672fcd98b64eb375cf299d963bd19110c33f5787cc6b",
      "content_summary": "相同 Q 行为何不总产生相同 Attention 输出？",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "相同 q 行为何不总产生相同 attention 输出?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-51f97e147966f83c6771ca89",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8808f07db598a483c23ae2a37ce3777b5ad823bc702e8a969b7a832e1e5a682f",
      "content_summary": "用 60–90 秒串起分块 Attention 前向。",
      "dependency_content_sha256": {
        "mc-10797edbc02a90f935980a34": "b13f7106f0bdb73fb86725fc0e39fff244f49df559c57c809d9df8f41840e415",
        "mc-3792ef72898b22610a7791b1": "a4350b49021875db31384f066e7710489b4fe0fcbbe51c5245c7b8e3db1e18fa",
        "mc-55086c744857d6967c992455": "f5278436eec30dbfa0956d9e2d8447ef9f98b9d58ac7803ba2aa1e37e6234321",
        "mc-5b8520cad91de49d0fce0551": "e8fbf4e1108666d37565a0bb163f6aefcf7b4c4ad266bca8f3ba1499aada1fea",
        "mc-dfeb90dfa04b47718a46bbbb": "be243dc2d7e4df877bf104a95ad574316b2d8e6862d09e2b51b52a95c9074972"
      },
      "depends_on": [
        "mc-10797edbc02a90f935980a34",
        "mc-3792ef72898b22610a7791b1",
        "mc-55086c744857d6967c992455",
        "mc-5b8520cad91de49d0fce0551",
        "mc-dfeb90dfa04b47718a46bbbb"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "用 60–90 秒串起分块 attention 前向。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-ee6220cfc1f9d4a258aa6297",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7453857f0094b545dde58ee1a72840a788f5fa5f5ad92dfff4a755a6547fccc2",
      "content_summary": "用 60–90 秒串起重算概率的反向。",
      "dependency_content_sha256": {
        "mc-08e5a0a6586998294cb74792": "a6f125e5988406e26591f64a90d73435694844a58389f57887301e7baaddf33b",
        "mc-86ae6ff76a84b4c6a1b9232a": "e84e5242c7cec03dd8fab567904d9b648e6c83d8be9edbb5998eff695c198b21",
        "mc-ac4172de0a8bc2a4d40c0eca": "043eb0d20727faa9f2dc2771b3b4b7bbe4e426fbe5fd004f5f781db48570b60e",
        "mc-dfeb90dfa04b47718a46bbbb": "be243dc2d7e4df877bf104a95ad574316b2d8e6862d09e2b51b52a95c9074972",
        "mc-e3916767857f2d3c67d3f4c6": "1c93934a90f65ae5411abe47e46a007ec77c3adc99b8d2c05a996a24fe7bef38"
      },
      "depends_on": [
        "mc-08e5a0a6586998294cb74792",
        "mc-86ae6ff76a84b4c6a1b9232a",
        "mc-ac4172de0a8bc2a4d40c0eca",
        "mc-dfeb90dfa04b47718a46bbbb",
        "mc-e3916767857f2d3c67d3f4c6"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "gpu-attention",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton fused-attention tutorial",
          "version": "source sha-256 5b16be48b7b781ef018931c789b191f3390886ac479bb5df8a3418e5612ab317"
        },
        "recall_target": "用 60–90 秒串起重算概率的反向。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-6e28784a6781cdeaed0ec32f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "05995feca7b9db71965298e29820102b65ff46293ac75f3eab8fa1865a74c97d",
  "manifest_payload_sha256": "0bf3553c1679c0935b81656d73d15a3b51c3eb6bac3a6997929aa9b844a201f9",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5397,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-06-fused-attention-correction.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "5c8fd292f9ab5e7508e25ad1b4a9ebdfd6b7b6428e122ecaf4e119414e137748",
          "logical_id": "mc-f949a09a279ca9bbaedd40ee",
          "row_sha256": "415908f4363bc05e040d7e99ef304caa4c46020b8f3485a8fa0d690e213d4f2e"
        },
        {
          "content_sha256": "1c93934a90f65ae5411abe47e46a007ec77c3adc99b8d2c05a996a24fe7bef38",
          "logical_id": "mc-e3916767857f2d3c67d3f4c6",
          "row_sha256": "f6b11c224d3278d4f0444f056358f4f5861173725acf277dcc96d94dc38667ea"
        },
        {
          "content_sha256": "a6f125e5988406e26591f64a90d73435694844a58389f57887301e7baaddf33b",
          "logical_id": "mc-08e5a0a6586998294cb74792",
          "row_sha256": "ea1e0099760a075aa8216d214116a967c1a1e69f92217210257e7069b6178059"
        }
      ],
      "sha256": "61a0623a6d761c2d28f2c3e490ddf54e4efb87f27c94e07a70c821f20e5df7f4",
      "sheet_name": "cards",
      "table_sha256": "107455db3ed695b90e4af44e6dbc63a35718ccae62e382ba6e6def242af74a07",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 29231,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-06-fused-attention-technical-qa.xlsx",
      "row_count": 29,
      "rows": [
        {
          "content_sha256": "b13f7106f0bdb73fb86725fc0e39fff244f49df559c57c809d9df8f41840e415",
          "logical_id": "mc-10797edbc02a90f935980a34",
          "row_sha256": "2fb1aa48d31e2beed19dd7a6e20e9c184b3a96fcc7a2c59f092e69665d456d34"
        },
        {
          "content_sha256": "98bdc89c7bc05c03c1bc2a6fc18b7a1fe8a4645c94a7dfa5887b99ed0040f3cb",
          "logical_id": "mc-6f4b77efdda16289ca9f840e",
          "row_sha256": "adb3d19ef79b63418f15acf1d05d920c2a58e90fb9dca4ff9a49938c95b1e010"
        },
        {
          "content_sha256": "a4350b49021875db31384f066e7710489b4fe0fcbbe51c5245c7b8e3db1e18fa",
          "logical_id": "mc-3792ef72898b22610a7791b1",
          "row_sha256": "9f6cabbd7451d54ce444b0c0ffed1b4da0ecad02ab673b0eb891531c34cdd59c"
        },
        {
          "content_sha256": "6a18b09e02a9ec14aa38bdb469462f25c2d67bdf4e77e461f2b83ce1155df3a7",
          "logical_id": "mc-525509f1b67e10f3367a6740",
          "row_sha256": "829ca3c35df8b92122f957fb67ac5aced986c061865841546c49280a253a1eb4"
        },
        {
          "content_sha256": "e8fbf4e1108666d37565a0bb163f6aefcf7b4c4ad266bca8f3ba1499aada1fea",
          "logical_id": "mc-5b8520cad91de49d0fce0551",
          "row_sha256": "83c0cc93277f8effd1fdc5e9a539714ae17c87f66b219933ca6abbdd87159c2c"
        },
        {
          "content_sha256": "f5278436eec30dbfa0956d9e2d8447ef9f98b9d58ac7803ba2aa1e37e6234321",
          "logical_id": "mc-55086c744857d6967c992455",
          "row_sha256": "ffc63e8d42ebe1c00a22b96b3d39157f84e2cee8760a0d4cae83e72c7eef86e7"
        },
        {
          "content_sha256": "fef9700fec9d72b96219d4f0379550360e61058d695481d30bd190607f2b81e9",
          "logical_id": "mc-5fa9999050b2b9eed656dd49",
          "row_sha256": "c5efb5f7ee54060a9ff758f69ee94985b841a7fd10d75dc63c449ead571954ef"
        },
        {
          "content_sha256": "ef1beaf3a09aac182a654cb84989376158588ad24a0387208c0783c1fa48a20b",
          "logical_id": "mc-36841e7e2e57cd392d7bd040",
          "row_sha256": "f6ecfa6283ff0e8cff87466fb59008520ebd2434c82af1eda88109c84ec3ac76"
        },
        {
          "content_sha256": "be243dc2d7e4df877bf104a95ad574316b2d8e6862d09e2b51b52a95c9074972",
          "logical_id": "mc-dfeb90dfa04b47718a46bbbb",
          "row_sha256": "0f2a515542e41388504d53343632565c0fcacab1178ef5156a9cdc1cbb32809a"
        },
        {
          "content_sha256": "0fac4d63403eb534be4068f439bfc921db7e4392d819fe52b5aa2785113c8911",
          "logical_id": "mc-8d6f166747439b6c1751a274",
          "row_sha256": "10ae51e109f620403f7b795608617d540844805184459a99e492ae26844641dd"
        },
        {
          "content_sha256": "2f78b683c3c26995deca50415584ba6f91acb000b892ddad6b25526886615474",
          "logical_id": "mc-e24771d0d0fe04e94cc22fc6",
          "row_sha256": "a09cd9436aeaa7fa512552e72cb5bbecf2166ce8d61dd801b59d6b5b5332dd14"
        },
        {
          "content_sha256": "254f34f83dd4d42d1ef3e7c231b640572c126b9564cbf6bb3133145d43f40faa",
          "logical_id": "mc-3a13fa0014fc53fab79ffd24",
          "row_sha256": "c8ab288b6480871f45534287dd9c983a3d96e5e9269f6be8cc973d273eccf1c9"
        },
        {
          "content_sha256": "1848a0ee90badbe9eb63092784e7ee529fe0cc589b7917dc6b1ab30b64cb5c45",
          "logical_id": "mc-963d2f25bb957912e1c6ed99",
          "row_sha256": "f3eae9c578b6eaafdad9b5cd3fc8e345948a984552e1f21dcdef688c33099d7c"
        },
        {
          "content_sha256": "e84e5242c7cec03dd8fab567904d9b648e6c83d8be9edbb5998eff695c198b21",
          "logical_id": "mc-86ae6ff76a84b4c6a1b9232a",
          "row_sha256": "79d7fbd1f49294a629a6a439521bd8bae9f2be82f39228c306fda6b110e50c8f"
        },
        {
          "content_sha256": "b80aadfdccec68af60feac7f38c43caf35e0b4c576523c3eee227e654036c72a",
          "logical_id": "mc-9a62292e5f5afbe601084713",
          "row_sha256": "fd8f24b82e714c34beef2e22bf9df25442dccd56300841e6f8ce5e52d91d7152"
        },
        {
          "content_sha256": "043eb0d20727faa9f2dc2771b3b4b7bbe4e426fbe5fd004f5f781db48570b60e",
          "logical_id": "mc-ac4172de0a8bc2a4d40c0eca",
          "row_sha256": "9c72bbe60e80b00bb5f1d27cb77d11c9c57b4df57453e1691291733677d228ed"
        },
        {
          "content_sha256": "308045415c68305fc9845d6c70b46f692d06280820d42fda9e619ab277367cff",
          "logical_id": "mc-37343051f020c2bb32857654",
          "row_sha256": "a4a5eba982ac155a033e8fe81a88d28f1448e84a83f64449a4bf956784889489"
        },
        {
          "content_sha256": "ef48e0d7b47f4abb32d200d1f5b0a69de414f36ce66f44b5624ee9924562139f",
          "logical_id": "mc-a3da6f89f9dfff794380bacf",
          "row_sha256": "0deecf2aaedc89545ab4ecfd79d469def844e184ade2bbcb1cbbe2d35a20695f"
        },
        {
          "content_sha256": "d2dfd576dd6a9c70d347ef68a2c40f7208e5a58d03f3a50f9d2b0c3080af5388",
          "logical_id": "mc-fe884cab68b5fd014c895d48",
          "row_sha256": "e83498b552d020ad707512ba6136966c17519bb38bb3008c06d01dca6a880db2"
        },
        {
          "content_sha256": "c67c70b95cce455a25e79325b71c02f3ca7344bc15d9a018a6f7018cbd9fa0c3",
          "logical_id": "mc-7b624650264561327c5db3e9",
          "row_sha256": "0e312eb5082f62404890ee13eb5c772a1f8cb3a9fc833de43062991ce789e481"
        },
        {
          "content_sha256": "b69a35cb8e7b7d9227b4d3259928c5a5fa9b548e2a0b7876bc7a51468dd9b78c",
          "logical_id": "mc-e0f9e3ccb87093480e0c4aaf",
          "row_sha256": "808f0bada53401f7f81568319ab27b3e88491c6d62b475cce3674ced0e8e7723"
        },
        {
          "content_sha256": "f4f50902d8e3b30c0bd4a2f0d8fa67ccfc87a5734f5792bf07c4ba339c5ac244",
          "logical_id": "mc-a0c0488514cc557c23d96e98",
          "row_sha256": "efdf11aeedf0476c2d7833988d2f6110c811f5ecb68cc10aef710b7f71908c04"
        },
        {
          "content_sha256": "66cd788f1a6e7b55e41ba3aff5fb324faf19bebb1b006f774005002c0d23efc1",
          "logical_id": "mc-0c544303457fe69beb458570",
          "row_sha256": "158662a765ddd481cbf441cf8dd111467a90bcd4baaf834ac9e663ff83bdfc48"
        },
        {
          "content_sha256": "c62c5a6d9b9504d3bf6c1dc164fcbeb1b518b67c41c4ad57d4a7cdf2a8d3a371",
          "logical_id": "mc-1e17c1d1f03d092cf091e666",
          "row_sha256": "d5eb41fc8afa56a886b5294a7f9370dc37af1574211ead3d778ac353df355847"
        },
        {
          "content_sha256": "aae6253dace86ab22c2ee0f8e1443189edd8954092c227ed033722142d366a50",
          "logical_id": "mc-491e7d022820a6bb4bb79c70",
          "row_sha256": "67ad50c3890585516eae14066941f205eeada65e029ba6a21c880a6ab8cfd95f"
        },
        {
          "content_sha256": "5ed6f8ff339f2a36dcf919bba51156ad1912e0480e7aaf7dbba7a692c780dc1f",
          "logical_id": "mc-12391b0b8209a8b11ff4e0a8",
          "row_sha256": "b4b21c2c659c58e4e85257d8a675995284f5ce312ee6827bd7b67ba74a6ba6aa"
        },
        {
          "content_sha256": "20860b16d6db474fe79565f8104e1287e7f57fedada63f71d4fd85e1a0144ed0",
          "logical_id": "mc-4fe59a4647c233625e064594",
          "row_sha256": "32b2dec3746cdc76a6dbbbc8619011bc3514fd5f8822c616fa51cb7d5c675266"
        },
        {
          "content_sha256": "7fb9f38b8ac0185de49bb1d3fb81aa710562c17c20500d9760befe84e59373bc",
          "logical_id": "mc-dca496c8a60dd217880d597f",
          "row_sha256": "5eea8f844030c3ef4ddda00da6ef1b7974e55950d6b1274d7ba6b09b455e20b9"
        },
        {
          "content_sha256": "fa1db0e815f098d4fef8672fcd98b64eb375cf299d963bd19110c33f5787cc6b",
          "logical_id": "mc-51f97e147966f83c6771ca89",
          "row_sha256": "7676e1dfbe2e8f0baa866a82b0cc17dedaf6f8d42ed599e72e0154fab9ea7612"
        }
      ],
      "sha256": "2ade9be1675d57aa45bbc482c97a0ccdcc06e572f38fd9f6b9b63b49e1908f10",
      "sheet_name": "cards",
      "table_sha256": "f61af527e5195dff7890c0f03851002ce5b72dc5358b203e7b75d7c16c830c13",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4511,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-06-fused-attention-oral.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "8808f07db598a483c23ae2a37ce3777b5ad823bc702e8a969b7a832e1e5a682f",
          "logical_id": "mc-ee6220cfc1f9d4a258aa6297",
          "row_sha256": "03bcaf2811ba6397c0944e00d31c4f1c843265251e476589adcc2be407e98829"
        },
        {
          "content_sha256": "7453857f0094b545dde58ee1a72840a788f5fa5f5ad92dfff4a755a6547fccc2",
          "logical_id": "mc-6e28784a6781cdeaed0ec32f",
          "row_sha256": "eb0767998544f8b662b723edb1109ae34cc2e58b9efc314aa9f131ff5516276e"
        }
      ],
      "sha256": "fad4278f019285682c59d2d7daba5f6c3151ef4401286c467226074e7e3a94bb",
      "sheet_name": "cards",
      "table_sha256": "b930d3fd24a46d6e1435aae4cffa350117718aeb750f3de49845b8c4e137f814",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "0f55ccf7737bf0ef653ea21f228720ff64afe3246dcae95c1c4b7100c7b29a18",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "attention-early",
      "path": "docs/triton-learning/logs/2026-09-19-fused-attention.md",
      "sha256": "6ef6f3909db980b0b9ad12cb6bca5d8cdebe3750ed0119c00e27a0a395d9c48c",
      "summary": "9/14–19：概念、在线状态、反向与真实纠错"
    },
    {
      "collection": "triton-study-logs",
      "id": "attention-late",
      "path": "docs/triton-learning/logs/2026-09-24-fused-attention.md",
      "sha256": "fa6c5dab615b7735f4afb328b3418238baf30e83cf4b5f19f297b6f52aaec413",
      "summary": "9/20–24：全貌、源码机制、descriptor、FP8、实践和A4解释"
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

导入文件：[triton-lesson-06-fused-attention-correction.xlsx](triton-lesson-06-fused-attention-correction.xlsx)（3 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-06-fused-attention-technical-qa.xlsx](triton-lesson-06-fused-attention-technical-qa.xlsx)（29 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-06-fused-attention-oral.xlsx](triton-lesson-06-fused-attention-oral.xlsx)（2 张卡）
