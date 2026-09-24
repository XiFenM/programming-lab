---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "d0574f84c2e27a219f71391b2e1bb121f38cfcdb3974659ea44a42a08d79d1c4",
  "candidate_sha256": "07519fadbb04bb2815dfea73834c7998cd5429fe3bf41d9dc37f1ece91f4ad75",
  "cards": [
    {
      "content_sha256": "2e02a7f83c033cdeb085eaee62b8094e46aadee0b5e0d72e3a1046f43383d527",
      "content_summary": "在一个 attention head 内，Q、K、V 都是形状为 [N,D] 的张量，分别表示 N 个 token 的 query、key 和 value；s 是给定的点积分数缩放系数。暂不考虑分块，如何由它们计算输出 O？说明各阶段的作用和结果形状。",
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
      "content_sha256": "71efef7bddac861f1d273140261d2a1b6ce10692f39dec18ee0ff5d50122b988",
      "content_summary": "普通 Attention 会把 N 个 query 对 N 个 key 的分数矩阵 S，以及 softmax 概率矩阵 P，写入全局显存。FlashAttention 改为按块计算时，主要避免了什么开销？QKᵀ 和 PV 的计算量是否也因此消失？",
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
      "content_sha256": "936868138b4b145a51d3fda5a06563edfc0f1d19ef43479341149163f3cb3c1d",
      "content_summary": "在所学 FP16 Attention 前向中，输入 Q/K/V 的形状是 [B,H,N,D]：B 为 batch 数、H 为 head 数、N 为 token 数、D 为每个 head 的特征维。BLOCK_M 是一个 Q tile 的行数。grid=(ceil(N/BLOCK_M),B×H,1) 怎样把计算和最终输出分给各 program？",
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
      "content_sha256": "faffbb968a841e2b2f7ef4e8951b9d3b5e7c8c7aec0539935491c58a9b873420",
      "content_summary": "连续 FP16 Q/K/V 原本形状为 [B,H,N,D]，B/H 分别为 batch/head 数，N 为 token 数，D 为特征维。现在 descriptor 将 batch、head、token 合并成 [BHN,D] 的二维视图。已知 batch=b、head=h、head 内 token=t，这个 token 在 descriptor 中的全局行号怎样计算？",
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
      "content_sha256": "4ddbcb784341ac697bffdcbe3bf059b5dfb8ea21f170f73f54fa5d91be81a7fa",
      "content_summary": "分块 Attention 前向中，一个 Q tile 有 B_M 个 query；本轮 K/V tile 有 B_N 个 key/value；每个 value 有 D 个特征。指数权重块的形状是 [B_M,B_N]。累加加权 V 的 acc 应是什么形状，为什么不能因 B_M 恰好等于 D 就把它理解成 [B_M,B_M]？",
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
      "content_sha256": "370fee9d51ba6b56f0c44eb3317bdb173e97d02377cf8eec51ff03c90b64b58d",
      "content_summary": "在 Attention 在线 softmax 的手算中，score 已乘原始 sm_scale，但尚未除以 ln2，也没有取 exp 或 exp2。旧、新运行最大分数分别为 −15 和 −13，而 kernel 使用 exp2。旧状态应乘什么重标定系数？为什么不能直接写 2^(−2)？",
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
      "content_sha256": "1aef964760de8f57a41f21583e74c3980fdf4952c22dce16a05343187f4e0500",
      "content_summary": "固定一个 query，Attention 前向已经扫描过若干 K/V 块，并保存运行最大值 m、指数和 l、加权 V 分子 acc。新 key 块 J 的分数 x_j 已换到 exp2 的输入域，但尚未取指数。怎样把这个新块并入旧状态，最终得到该 query 的输出？",
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
      "content_sha256": "d19df06bc0e7f000fa92eab0abebdc6dc7e2a3ef0e8f6113b4ff90936af2415e",
      "content_summary": "所学 Attention 前向将每个 query 的在线状态初始化为 m=−∞、l=1、acc=0。其中 m 是 exp2 输入域分数的运行最大值。假设首块至少有一个有效 key，且所有有效 score 都有限（无效位置可被 mask 为 −∞），为什么初始 l=1 不会使 softmax 分母多出 1？改成 l=0 是否也可行？",
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
      "content_sha256": "dea82e7c6992aafe2d6e922c90a10f83296be3d182c176def2398ddffbecebf5",
      "content_summary": "在 causal Attention 前向中，一个 program 负责 head 内 query 区间 [a,b)。causal 规则是 query i 只能读取 key j≤i。为了减少逐元素 mask，这个 program 应怎样划分要扫描的 key 区域？",
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
      "content_sha256": "a87b879b5c613221f94f97d4b025fa323c40bf9f15eef4f06ceb677cf9c7818a",
      "content_summary": "Attention 前向采用 exp2，令 x_j=S_j/ln2，其中 S_j 是已乘原始 scale 的点积分数。它为一行有效 key 保存 m=max(x_j)、l=Σ2^(x_j−m)，并只把 M=m+log₂(l) 留给反向。为什么反向用 2^(x_j−M) 就能恢复概率，且没有丢掉减最大值的稳定化效果？",
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
      "content_sha256": "62f914aa2202de58d349ee77dd9ac2187f357b4242f64cb111fbf70f921dd5a2",
      "content_summary": "在所学 FP16 Attention 前向实现中，Q/K/V 以 FP16 存储，输出 O 也需要返回 FP16。沿 QKᵀ、softmax 在线统计、pV 到 O/M 写回这条路径，各阶段使用什么精度，关键转换发生在哪里？",
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
      "content_sha256": "4027b8af5e602967766835e9d3487aac5681f90482854990ddb09bf5aae1cb75",
      "content_summary": "Attention 前向中，p 是 FP32 的未归一化指数权重块，l 要累加每行的 sum(p)；另一路会把 p 转成 FP16 后与 FP16 V 做矩阵乘。如果把 sum(p) 移到 p 转 FP16 之后，即使仍用 FP32 累加，能保证分母结果不变吗？",
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
      "content_sha256": "a259af49da68b59be890bf71322265b61d9aa828e8ad574230f46cea7323954a",
      "content_summary": "阅读或设计一个新的深度学习算子时，输入和输出可能使用 FP16，但内部还有矩阵乘、长归约或指数运算。应怎样决定各阶段的精度，而不是凭输入 dtype 猜测全部内部计算类型？",
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
      "content_sha256": "63f911929593263dd2e3c14a1f981d8313212a084457110e13e203393d05a6b5",
      "content_summary": "在所学 PyTorch/Triton Attention 的前后向流程中，哪些量是在前向结束时保存给反向使用的，哪些是在反向中临时计算的，哪些才是最终输出的梯度？请按产生时间和用途区分。",
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
      "content_sha256": "7138803514c69f1789b07a4ca518cd0a8828984787220f371b39c22ae596314c",
      "content_summary": "阅读所学 Attention 源码时，会看到前向 kernel 内多次调用 _attn_fwd_inner，也会看到反向先启动 preprocess、再启动主 backward。它们分别怎样传递计算状态？为什么不能把每个 @triton.jit 函数调用都当成独立的 kernel launch？",
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
      "content_sha256": "2fcb97f3086dfaf759170e0c05b1070985de9d073671b412c829bf624f492297",
      "content_summary": "Attention 反向预处理拿到前向输出 O 和上游梯度 dO，两者都是 [B,H,N,D]：N 是 query 数，D 是每个输出向量的特征数。为了得到每个 query 一个 Delta，实际应沿哪一维求和？它与沿 key 求和的公式有什么关系？",
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
      "content_sha256": "b9b6deb8cfca1c91f223133b0fd119eaa01d60b28107ee46edc5fcbc9e9fffc9",
      "content_summary": "对一个 head，前向为 S=sQKᵀ、P=softmax_key(S)、O=PV；s 是固定缩放系数，Q/K/V 为 [N,D]。损失传来同形状的上游梯度 dO 后，如何依次算出 dP、分数梯度以及 dQ/dK/dV？",
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
      "content_sha256": "a1dd1e0f58ef2e44031f6ac34a3368c8db9f63e37f61669c4f365060428e0593",
      "content_summary": "Attention 反向重建一个概率 tile 时，M 和 Delta 都是“每个 query 一个值”的统计量。如果概率 tile 有时按 [Bq,Bk]（query×key）存放，有时按 [Bk,Bq]（key×query）存放，这两个向量应怎样广播才能对应到正确 query？",
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
      "content_sha256": "3ade6ae0c7516a2cc83e08a80f29b7eea72e5eba0db0596e4c5e663ad4b67809",
      "content_summary": "分块计算 Attention 的 dK/dV 时，同一个 key 会接收多个 query 的梯度贡献。什么样的 program 分工可以在写回这些梯度时不用 atomic？如果把同一输出块的贡献拆给两个 program，为什么普通 store 不够？",
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
      "content_sha256": "547ed797d1c2141222e9622e1f875ab48dea016c5f34f37e3d6d4eb3805e076e",
      "content_summary": "causal Attention 规定 query i 只能使用 key j≤i。反向计算时，固定一个 query 来求 dQ，与固定一个 key 来求 dK/dV，分别要汇总哪一侧 token 的贡献？为什么扫描方向看起来相反？",
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
      "content_sha256": "2289ea5ae9e0b283a051e70c0fef2c2475e6b8b04ccb1b48d99ff4220470d62e",
      "content_summary": "所学 Attention 反向先把 K 预缩放为 K̃=(s/ln2)K。令 G=P⊙(dP−Delta) 表示损失对自然分数 S=sQKᵀ 的梯度。为什么 dQ 路径用 K̃ 累加后要乘 ln2，而 dK 路径用原始 Q 累加后要乘 s？",
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
      "content_sha256": "1e6faa6bafdecd60cb373470dccdbfc70796a5e22cf2d3ccb7a035093368a3e7",
      "content_summary": "使用 Triton TensorDescriptor 按块读取张量时，base、shape、strides、block_shape 和 load(offsets) 分别决定什么？例如 B/H/N/D 分别表示 batch 数、head 数、token 数和特征维，Q 被展平成 [BHN,D]，每次取 BLOCK_M 个 query。此时 block_shape=[BLOCK_M,D]，load([r0,0]) 会读取哪个块？",
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
      "content_sha256": "2206c8db82bdf9d160a7f0dc3f4398963386a47e2c175009875993b57c87eab6",
      "content_summary": "Attention 的 Q/K/V descriptor 把多个 batch/head 展平成 [BHN,D]，每个 head 占 N 行。若一次 load 跨过当前 head 的末尾，却仍在整个 BHN 行视图之内，descriptor 会自动将越过这个 head 的位置补零吗？",
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
      "content_sha256": "8061f3219770f9b1a6dd79dac1fd3e863fe09c4b1e879ea9d68ab60c38711f15",
      "content_summary": "Attention 处理不足一个 tile 的尾部 key 时，假设 descriptor 已把无效位置的 K 和 V 都补成零。能否省掉对这些 key 的 score mask，直接让 softmax 和 pV 计算整个 tile？",
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
      "content_sha256": "8afedde9c2121200fd82da0283d9f6f7149e75f5213fe068bc3ef300733ad8af",
      "content_summary": "在 Triton 3.7.1 中，普通 tl.load 可用 other 指定 masked 位置的替代值。若改用 TensorDescriptor 的 load，能否同样传入任意 other 值？可选的 padding 在哪里设置？",
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
      "content_sha256": "be4bf7e5ed1d9cea5e09c249c6191567c5e2fe4808a12e3537ccf440dffa4ace",
      "content_summary": "把一个 PyTorch 张量传给 Triton 3.7.1 的 NVIDIA TMA descriptor 前，为什么仅检查 is_contiguous() 不够？应怎样检查实际基址与 stride 的基础对齐条件，切片视图又会带来什么问题？",
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
      "content_sha256": "e884ca5ce8d16ff0a76fb1958023d86408e3acf55b8cd7c706e0087637ab2b25",
      "content_summary": "所学 Attention 的普通 FP16 路径中，D 表示每个 head 的特征维度。wrapper 在 host 侧先用 dummy_block 创建 TensorDescriptor，而 autotune 会尝试不同 BLOCK_M/BLOCK_N。为什么每次配置运行前必须由 pre-hook 更新 block_shape，不能指望 kernel 中的 _maybe_make_tensor_desc 自动改正确？",
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
      "content_sha256": "ccfd66317d868d8e05be3b16e7279eb920f3f2e4dae3cc2a67453a49e18c5af7",
      "content_summary": "比较 FP8 E5M2 和 FP16 的表示精度：前者为 1 位符号、5 位指数、2 位显式小数，后者为 1、5、10。固定同一个正规数指数区间，E5M2 相邻可表示数的间距是 FP16 的多少倍？为什么指数位数相同仍不代表精度相同？",
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
      "content_sha256": "eedbd2c65f4c9ff018b4c136714373fd114b284bb67c82d56cf77aaf5c46793a",
      "content_summary": "所学 FP8 Attention 为 V 调整布局：B/H 分别是 batch/head 数，N 是 token 数，D 是特征维。从连续的 [B,H,N,D] 张量出发，先 permute 成 [B,H,D,N] 并 contiguous()，再用逆 permute 恢复 [B,H,N,D]。最终 shape 已恢复，为什么存储布局仍然改变？删掉中间 contiguous() 又会怎样？",
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
      "content_sha256": "9651abf01753b06b08a53f3a3b7650e8d332da40abb74e3806c5a9fbc72b1d83",
      "content_summary": "验证两个 Attention 实现的反向结果时，参考实现先调用 backward(dout)，然后再运行被测实现。除了 Q/K/V 相同，还必须固定哪些输入条件？为什么保存参考梯度后要清空叶子张量的 .grad？",
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
      "content_sha256": "43ae55b29e0892edbb6e4a2f91a7c37d0fad857c6bc6381f3c97acb18b4c18d7",
      "content_summary": "所学 Attention benchmark 用前向 FLOP 数乘 2.5 来估算反向工作量。这里 FLOP 指浮点运算次数，B/H/N/D 分别是 batch、head、token 和特征维。2.5 的来源是什么，它能否预测反向耗时也是前向的 2.5 倍？",
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
      "content_sha256": "ce6f6a6813eab717b3912e801b173758b16bb4bdf051d4b6765c1e0b3da16ddf",
      "content_summary": "在同一个 Attention head 内，所有 query 向量都相同，K/V 和 scale 固定。非 causal 时，各行 O 与 M 为什么在数学上相同？改成 causal 后，这个“所有行相同”的结论为什么不能直接沿用？M 表示每行归一化分母的 base-2 对数。",
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
      "content_sha256": "35e1811c54dfdee055804854787dc5dfbf5a71c7aeed5839e462c80673938853",
      "content_summary": "请用约 60–90 秒解释分块 Attention 前向：输入 Q/K/V 为 [B,H,N,D]，B/H 分别是 batch/head 数，N 是 token 数，D 是特征维度，s 为原始 scale；每个 program 负责一个 head 的 B_M 行 Q，并逐块扫描 B_N 行 K/V。说明它怎样从完整 Attention 公式出发，维护跨块状态并最终写出 O 和供反向使用的 M。",
      "dependency_content_sha256": {
        "mc-10797edbc02a90f935980a34": "2e02a7f83c033cdeb085eaee62b8094e46aadee0b5e0d72e3a1046f43383d527",
        "mc-3792ef72898b22610a7791b1": "936868138b4b145a51d3fda5a06563edfc0f1d19ef43479341149163f3cb3c1d",
        "mc-55086c744857d6967c992455": "1aef964760de8f57a41f21583e74c3980fdf4952c22dce16a05343187f4e0500",
        "mc-5b8520cad91de49d0fce0551": "4ddbcb784341ac697bffdcbe3bf059b5dfb8ea21f170f73f54fa5d91be81a7fa",
        "mc-dfeb90dfa04b47718a46bbbb": "a87b879b5c613221f94f97d4b025fa323c40bf9f15eef4f06ceb677cf9c7818a"
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
      "review_resolution": {
        "summary": "已重新对照本课 card-01, card-03, card-07, card-05, card-10 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "64f2dbe9aed6b9f7719a1daa46e3f15b406c633ecbf413120d77c77bf31b0a29",
      "content_summary": "请用约 60–90 秒解释所学 Attention 反向的数据流：前向已经从 Q/K/V 得到 O，并保存逐 query 的归一化统计量 M；现在收到损失对 O 的梯度 dO。怎样利用保存量、计算 Delta、按块重建概率，并通过输出分工得到 dQ/dK/dV？",
      "dependency_content_sha256": {
        "mc-08e5a0a6586998294cb74792": "2fcb97f3086dfaf759170e0c05b1070985de9d073671b412c829bf624f492297",
        "mc-86ae6ff76a84b4c6a1b9232a": "b9b6deb8cfca1c91f223133b0fd119eaa01d60b28107ee46edc5fcbc9e9fffc9",
        "mc-ac4172de0a8bc2a4d40c0eca": "3ade6ae0c7516a2cc83e08a80f29b7eea72e5eba0db0596e4c5e663ad4b67809",
        "mc-dfeb90dfa04b47718a46bbbb": "a87b879b5c613221f94f97d4b025fa323c40bf9f15eef4f06ceb677cf9c7818a",
        "mc-e3916767857f2d3c67d3f4c6": "63f911929593263dd2e3c14a1f981d8313212a084457110e13e203393d05a6b5"
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
      "review_resolution": {
        "summary": "已重新对照本课 card-16, card-17, card-19, card-10, card-14 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
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
  "manifest_payload_sha256": "5a6cc23d8ff23ca4f2d87691e3d9c2622d1467e7f365bcf7b96cdcdb96d0fcb5",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 8228,
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
          "content_sha256": "370fee9d51ba6b56f0c44eb3317bdb173e97d02377cf8eec51ff03c90b64b58d",
          "logical_id": "mc-f949a09a279ca9bbaedd40ee",
          "row_sha256": "8c62d7dddc004ada5cfe13d11e55b1f06a96067dea05fa1415fee9a48c6a7e38"
        },
        {
          "content_sha256": "63f911929593263dd2e3c14a1f981d8313212a084457110e13e203393d05a6b5",
          "logical_id": "mc-e3916767857f2d3c67d3f4c6",
          "row_sha256": "544dd36dde4c97fed53146d5f101b7646fc836df5e259cda2fda3e3dcc5453c8"
        },
        {
          "content_sha256": "2fcb97f3086dfaf759170e0c05b1070985de9d073671b412c829bf624f492297",
          "logical_id": "mc-08e5a0a6586998294cb74792",
          "row_sha256": "f59382481d5937a6f3303ac0707bac4a74beff149cff72667820e28adcc6e0d6"
        }
      ],
      "sha256": "4d4f783410ec446c466685c783e6c603e094b4d44705bb6659ea02756c049e14",
      "sheet_name": "cards",
      "table_sha256": "f103a4a540e3e0d1f133d617042a4e2e0061ea0206f2b12490c1f5b49950ee6f",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 49183,
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
          "content_sha256": "2e02a7f83c033cdeb085eaee62b8094e46aadee0b5e0d72e3a1046f43383d527",
          "logical_id": "mc-10797edbc02a90f935980a34",
          "row_sha256": "18d1e87a3cc2b50529edb51c1b009c20c5458b8d6b60a475daa02a2b8d56a89c"
        },
        {
          "content_sha256": "71efef7bddac861f1d273140261d2a1b6ce10692f39dec18ee0ff5d50122b988",
          "logical_id": "mc-6f4b77efdda16289ca9f840e",
          "row_sha256": "9f8d1fa87a5c5b0cfdc511add4841a6a7f976fcbaebdb4f905c8fda2d23e9857"
        },
        {
          "content_sha256": "936868138b4b145a51d3fda5a06563edfc0f1d19ef43479341149163f3cb3c1d",
          "logical_id": "mc-3792ef72898b22610a7791b1",
          "row_sha256": "7c7a83001125bb3e045b459b9a88eb58b165207c409550a7a764f7b135c8f4cc"
        },
        {
          "content_sha256": "faffbb968a841e2b2f7ef4e8951b9d3b5e7c8c7aec0539935491c58a9b873420",
          "logical_id": "mc-525509f1b67e10f3367a6740",
          "row_sha256": "b651345199172daf29cf8eebf904ceab7db0e3263b49af170c31251e3dc6aef7"
        },
        {
          "content_sha256": "4ddbcb784341ac697bffdcbe3bf059b5dfb8ea21f170f73f54fa5d91be81a7fa",
          "logical_id": "mc-5b8520cad91de49d0fce0551",
          "row_sha256": "8044000b2e2188654c8e16dd7b1dc6be1727de2d8dbe84d34d5ab9e1273b81ae"
        },
        {
          "content_sha256": "1aef964760de8f57a41f21583e74c3980fdf4952c22dce16a05343187f4e0500",
          "logical_id": "mc-55086c744857d6967c992455",
          "row_sha256": "b9b3703ff170942745bbc77bd90bee30ac840810c7147e3ec5be24a03a7d9abd"
        },
        {
          "content_sha256": "d19df06bc0e7f000fa92eab0abebdc6dc7e2a3ef0e8f6113b4ff90936af2415e",
          "logical_id": "mc-5fa9999050b2b9eed656dd49",
          "row_sha256": "2bc9b60c3f15ae94ca295914f796082d2aada13ff75a4244964f0c14ca6bf976"
        },
        {
          "content_sha256": "dea82e7c6992aafe2d6e922c90a10f83296be3d182c176def2398ddffbecebf5",
          "logical_id": "mc-36841e7e2e57cd392d7bd040",
          "row_sha256": "0eee7d4c3b15f361cc2f003792ca55317e18f28137a37a53ae7e7713f58ca89b"
        },
        {
          "content_sha256": "a87b879b5c613221f94f97d4b025fa323c40bf9f15eef4f06ceb677cf9c7818a",
          "logical_id": "mc-dfeb90dfa04b47718a46bbbb",
          "row_sha256": "18448c734931315efc9d385b83e4a4d6454f1d5154c0d0af220ff4f5a80fbf5d"
        },
        {
          "content_sha256": "62f914aa2202de58d349ee77dd9ac2187f357b4242f64cb111fbf70f921dd5a2",
          "logical_id": "mc-8d6f166747439b6c1751a274",
          "row_sha256": "865240955a3931e8df214290e916a19cf96c2028df53aa7b8ea55a5106e12a1c"
        },
        {
          "content_sha256": "4027b8af5e602967766835e9d3487aac5681f90482854990ddb09bf5aae1cb75",
          "logical_id": "mc-e24771d0d0fe04e94cc22fc6",
          "row_sha256": "a8bec012f3b092013bf533b95a3d66ce73be935153a414364bb16d1dc348740e"
        },
        {
          "content_sha256": "a259af49da68b59be890bf71322265b61d9aa828e8ad574230f46cea7323954a",
          "logical_id": "mc-3a13fa0014fc53fab79ffd24",
          "row_sha256": "0b215ef5b66e6a48f83e179e652dd2ec25d583f9d39dd41f3b70320955c16296"
        },
        {
          "content_sha256": "7138803514c69f1789b07a4ca518cd0a8828984787220f371b39c22ae596314c",
          "logical_id": "mc-963d2f25bb957912e1c6ed99",
          "row_sha256": "75bbb98a7e573542e8938cce616afe209d1e504a60aba00cd3c984ebdb220210"
        },
        {
          "content_sha256": "b9b6deb8cfca1c91f223133b0fd119eaa01d60b28107ee46edc5fcbc9e9fffc9",
          "logical_id": "mc-86ae6ff76a84b4c6a1b9232a",
          "row_sha256": "9ac116edc81019f6766cf6045c0ec1ee0dd68d8017a4ac4661fa6a6b3c9e2785"
        },
        {
          "content_sha256": "a1dd1e0f58ef2e44031f6ac34a3368c8db9f63e37f61669c4f365060428e0593",
          "logical_id": "mc-9a62292e5f5afbe601084713",
          "row_sha256": "f69fd1696341581db11d6b8270d1bff84890ce0252f6182e8576e51704260507"
        },
        {
          "content_sha256": "3ade6ae0c7516a2cc83e08a80f29b7eea72e5eba0db0596e4c5e663ad4b67809",
          "logical_id": "mc-ac4172de0a8bc2a4d40c0eca",
          "row_sha256": "3ac3d5cdbc8e2d4555d391a66ccd180a6ed55e45c7b1fc2987b536107be5c2df"
        },
        {
          "content_sha256": "547ed797d1c2141222e9622e1f875ab48dea016c5f34f37e3d6d4eb3805e076e",
          "logical_id": "mc-37343051f020c2bb32857654",
          "row_sha256": "cae56c554c0fba87f97928a90d7f13d52e8b0e56d2437327d506f26d5c4c3b05"
        },
        {
          "content_sha256": "2289ea5ae9e0b283a051e70c0fef2c2475e6b8b04ccb1b48d99ff4220470d62e",
          "logical_id": "mc-a3da6f89f9dfff794380bacf",
          "row_sha256": "d8529c3d49ed3abcbdbd4960e688b2d19d54f0dee20ac61422afd5364cc8cad3"
        },
        {
          "content_sha256": "1e6faa6bafdecd60cb373470dccdbfc70796a5e22cf2d3ccb7a035093368a3e7",
          "logical_id": "mc-fe884cab68b5fd014c895d48",
          "row_sha256": "8d002565d62208011a9cb1736ac31682b49e42f46f38cc3b002b6640a1e8ef8e"
        },
        {
          "content_sha256": "2206c8db82bdf9d160a7f0dc3f4398963386a47e2c175009875993b57c87eab6",
          "logical_id": "mc-7b624650264561327c5db3e9",
          "row_sha256": "319decf7f8e6398532cf0a8ced53a14e8036bb71cb61d57d4bd350a9e07bc26e"
        },
        {
          "content_sha256": "8061f3219770f9b1a6dd79dac1fd3e863fe09c4b1e879ea9d68ab60c38711f15",
          "logical_id": "mc-e0f9e3ccb87093480e0c4aaf",
          "row_sha256": "edb485848d3d6e6fb86bd58ec46902c13e64fa107a3ade49b6acb91dcb454322"
        },
        {
          "content_sha256": "8afedde9c2121200fd82da0283d9f6f7149e75f5213fe068bc3ef300733ad8af",
          "logical_id": "mc-a0c0488514cc557c23d96e98",
          "row_sha256": "728be739ad46fd64763ac559655c89f3608b65eb4c91cea507ce4072e7651a5a"
        },
        {
          "content_sha256": "be4bf7e5ed1d9cea5e09c249c6191567c5e2fe4808a12e3537ccf440dffa4ace",
          "logical_id": "mc-0c544303457fe69beb458570",
          "row_sha256": "275db4be1a53211f9dec537d607a31fca5e78a480327a40a99665226436f4bc3"
        },
        {
          "content_sha256": "e884ca5ce8d16ff0a76fb1958023d86408e3acf55b8cd7c706e0087637ab2b25",
          "logical_id": "mc-1e17c1d1f03d092cf091e666",
          "row_sha256": "1d27d9c3bfbbae1910971c8a59b2876c313112a6b1221c26bc25422c4f0fe92a"
        },
        {
          "content_sha256": "ccfd66317d868d8e05be3b16e7279eb920f3f2e4dae3cc2a67453a49e18c5af7",
          "logical_id": "mc-491e7d022820a6bb4bb79c70",
          "row_sha256": "14bf8d52c207f1b435014d2a32751cbb1f2411df5a137bc696f27cc417ff5cde"
        },
        {
          "content_sha256": "eedbd2c65f4c9ff018b4c136714373fd114b284bb67c82d56cf77aaf5c46793a",
          "logical_id": "mc-12391b0b8209a8b11ff4e0a8",
          "row_sha256": "9368cc5d4edefff71f13f0118041ba96983f7dc31c2e63a113927ac7d19b33dd"
        },
        {
          "content_sha256": "9651abf01753b06b08a53f3a3b7650e8d332da40abb74e3806c5a9fbc72b1d83",
          "logical_id": "mc-4fe59a4647c233625e064594",
          "row_sha256": "83d42cab84750caf26161efcb3f71a839a02d7ca68e9148e66e83f8021aedbe6"
        },
        {
          "content_sha256": "43ae55b29e0892edbb6e4a2f91a7c37d0fad857c6bc6381f3c97acb18b4c18d7",
          "logical_id": "mc-dca496c8a60dd217880d597f",
          "row_sha256": "564763c7c31994ac6c11b63a4e50e06b09bb5fde8b77ea4d757e216ba1c8ab84"
        },
        {
          "content_sha256": "ce6f6a6813eab717b3912e801b173758b16bb4bdf051d4b6765c1e0b3da16ddf",
          "logical_id": "mc-51f97e147966f83c6771ca89",
          "row_sha256": "5f483eb6d46f67386bf962f11dd2c4863e945ef946f914c7c70da14db225e930"
        }
      ],
      "sha256": "ae0bdec3be8b8e49910589ef04e3097f51d754b84633404b5d0e2a3ff917c803",
      "sheet_name": "cards",
      "table_sha256": "8cbb5da21bea7407ae15b6353b77ee63a44fca9b0db9b349aa5821c2e5b61b53",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 6810,
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
          "content_sha256": "35e1811c54dfdee055804854787dc5dfbf5a71c7aeed5839e462c80673938853",
          "logical_id": "mc-ee6220cfc1f9d4a258aa6297",
          "row_sha256": "a3e6f1813d3ec3df34b236ffefc868fc7490fa2ac8d786660345a3e5dd6607f4"
        },
        {
          "content_sha256": "64f2dbe9aed6b9f7719a1daa46e3f15b406c633ecbf413120d77c77bf31b0a29",
          "logical_id": "mc-6e28784a6781cdeaed0ec32f",
          "row_sha256": "fbde33fdcae4a60ebd0d0779646c76e25db80cf9aedc75cd6a053ec53e3cef8e"
        }
      ],
      "sha256": "333e3de10c5a9d63d9028316a204b23834d546b63a1b69c7c29a589c07cd7a03",
      "sheet_name": "cards",
      "table_sha256": "95852dba60880963295fd6b89b80d2655da2b1fe7d1b14534a496342f696b039",
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
