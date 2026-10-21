---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "814edae56e8c8cb71ba6e8dd8539b7c0751e4d7b886b1e9bd950e3f7fe04cac3",
  "candidate_sha256": "7e075769e362a269fba3d0763598bdc6060080d1e99ee4597142ccf67f157b2f",
  "cards": [
    {
      "content_sha256": "3557fa158cc620a2375af258dc23e86d0ae3f10151568c54bc6e326465bc06a8",
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
      "content_sha256": "846dcb45d529bca5dda85cd42e4035edb2fe6e0183e7bc2b4acf4dac2d2c9850",
      "content_summary": "普通 Attention 按 S=sQKᵀ、P=softmax(S)、O=PV 逐步计算（N 个 query、N 个 key，s 为缩放系数），每一步都先得到完整结果再交给下一步。FlashAttention 改为按块计算后，省掉的是哪一类开销，哪一类主要工作仍然保留？",
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
      "content_sha256": "e61f4001baa49c7e2fe55945088391e83d270c04d63eacfdb64323330ce4cb9d",
      "content_summary": "在 Triton 官方 fused-attention 教程（快照版）的 FP16 前向中，输入 Q/K/V 的形状是 [B,H,N,D]：B 为 batch 数、H 为 head 数、N 为 token 数、D 为每个 head 的特征维。BLOCK_M 是一个 Q tile 的行数。grid=(ceil(N/BLOCK_M),B×H,1) 怎样把计算和最终输出分给各 program？",
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
      "content_sha256": "3943e7504e51f4f965457a8d91e6ae7ef37f2af817fdb26e2b65c2a494f91c1d",
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
      "content_sha256": "a4db0ff069983c51f7ebafa7ef3330a0bb93c60f61604a2b08cee835cb4860f5",
      "content_summary": "分块 Attention 前向中，一个 program 负责 B_M 个 query；本轮读入 B_N 个 key/value，每个 value 是 D 维特征向量；当前块的未归一化指数权重 p 形状为 [B_M,B_N]。跨多轮 K/V 累计 pV 的输出分子 acc 应是什么形状？请用乘加时被归约和被保留的轴说明。",
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
      "content_sha256": "8c2ee515977d546f9a8fe9e4cd33dcdb58fc5244063f30231773f1468339e59f",
      "content_summary": "在线 softmax 手算：score 已乘原始 sm_scale，属于自然指数域（softmax 权重为 e^score），还没有取指数。旧、新运行最大分数分别为 −15 和 −13。旧分母和旧分子都要乘同一个重标定系数，它等于多少？请分别写出用 exp 和用 exp2 表示的形式。",
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
      "content_sha256": "37190aa0b111dc0bb43863801ff2c6140bcf175f2ca65d08f853cf3152095743",
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
      "content_sha256": "0fde9af627aeffd30f8bbb7ff373d119b0032f0a83c6aa3251f3d3eba01bb067",
      "content_summary": "某个分块 Attention 前向把每个 query 的在线状态初始化为 m=−∞、l=1、acc=0，其中 m 是 exp2 输入域分数的运行最大值。假设首块至少有一个有效 key，有效 score 都有限，无效位置被 mask 为 −∞。为什么初始的 l=1 不会进入最终分母？",
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
      "content_sha256": "636b670dec83b23805927014b24c8be0756d1fad3cd9bc867d0b3c359e7a8475",
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
      "content_sha256": "051442f2ce8455255f1f45ef4ef68cf5a6214d31b4577aec28aff227a4b37d11",
      "content_summary": "Triton 官方 fused-attention 教程（快照版）的前向 kernel 有一个编译期参数 STAGE，causal 时取 3、non-causal 时取 1；它的 autotune 候选配置里另有 num_stages。这两个名字相近的参数分别控制什么？",
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
        "recall_target": "辨析教程前向的 stage 与 autotune 的 num_stages 各控制什么"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e618c051620589a255fa9cad",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "attention-early",
        "attention-late"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d4c40f5d0db933b0925f4d3406cab9305bb671e1d608f79f66e9f983f0e5ee19",
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
      "content_sha256": "1d0b4d8822752addea106ce1e1c3ec7e7de46a651479b23ee320037d658db52f",
      "content_summary": "在 Triton 官方 fused-attention 教程（快照版）的 FP16 前向中，Q/K/V 以 FP16 存储，输出 O 也需要返回 FP16。沿 QKᵀ、softmax 在线统计、pV 到 O/M 写回这条路径，各阶段使用什么精度，关键转换发生在哪里？",
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
      "content_sha256": "09a86bd283c61a74130c200f7d05c780e71db8b51d1efff834b3fa061d8532c0",
      "content_summary": "Attention 前向中，p 是 FP32 的未归一化指数权重块：一路对每行求 sum(p) 累加到分母 l，另一路把 p 转成 FP16 后与 FP16 V 做矩阵乘。若把 sum(p) 改到 p 转成 FP16 之后再算，并且仍用 FP32 累加，分母会受什么影响？请从误差产生的位置解释。",
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
      "content_sha256": "285990076c2795a143cce7fdfdeb24c3ba91adce323b130934e28729ee87c5fb",
      "content_summary": "在 Triton 官方 fused-attention 教程（快照版）的前后向流程中，哪些量是在前向结束时保存给反向使用的，哪些是在反向中临时计算的，哪些才是最终输出的梯度？请按产生时间和用途区分。",
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
      "content_sha256": "ba12ba27881459f55e96124d2b208510d07baeee013381e0693076672d154b4a",
      "content_summary": "Triton 官方 fused-attention 教程（快照版）的反向不保存前向算出的概率矩阵 P：前向末尾只为每个 query 留一个统计量 M，反向再按块用 Q/K 与 M 重算 P。输入有 B 个 batch、H 个 head，每个 head N 个 token。这个设计省下了什么，又多付出了什么？",
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
        "recall_target": "反向为什么只存每行 m 并按块重算 p,而不保存前向的 p"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3b1feda15f9269b40346e62a",
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
      "content_sha256": "7ba3db8598788376f7724a9232db4bc8926c15d89528a3c26ce394ff35d5997b",
      "content_summary": "阅读 Triton 官方 fused-attention 教程（快照版）的源码时，会看到前向 kernel 内多次调用 _attn_fwd_inner，也会看到反向先启动 preprocess、再启动主 backward。它们分别怎样传递计算状态？为什么不能把每个 @triton.jit 函数调用都当成独立的 kernel launch？",
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
      "content_sha256": "fd24c06e2269d63b391e2926810e49e10d92e96b6be04cd52db960953edd97b8",
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
      "content_sha256": "412591b356ad7c43d2750adda36038c2a110d74338b74cb3f088d5c562e68521",
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
      "content_sha256": "ee008381d5536518b3df8418d81f68005cff5af5e900cee1754ab80c1ebbfb63",
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
      "content_sha256": "854f3ff115cd22fc9e0df4260173b18595a3f7ae3be7f8b4878674ce10baf365",
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
      "content_sha256": "4b81c9a1068f987035a6cb547e0df1c16c867d580c8906afacbcef4765683918",
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
      "content_sha256": "37facdceef59ea25ab767dce91e0742fcc745205d150bd5cec4bc60ed0f3650f",
      "content_summary": "Triton 官方 fused-attention 教程（快照版）的反向先把 K 预缩放为 K̃=(s/ln2)K。令 G=P⊙(dP−Delta) 表示损失对自然分数 S=sQKᵀ 的梯度。为什么 dQ 路径用 K̃ 累加后要乘 ln2，而 dK 路径用原始 Q 累加后要乘 s？",
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
      "content_sha256": "d2edd7d58e1f56fd288302875b990d6f6c658a0a785f73919f0bde8e4837bde9",
      "content_summary": "在 Triton 3.7.1 中，用 TensorDescriptor 描述展平后的 Q：base 指向连续 Q 的存储，shape=[BHN,D]、strides=[D,1]（B/H/N/D 分别为 batch 数、head 数、token 数和特征维），block_shape=[BLOCK_M,D]。一次 desc.load([r0,0]) 读到的块由哪个参数决定大小、哪个参数决定位置？把起点改成 [r0+BLOCK_M,0] 时，读到的块和返回的 shape 各怎样变化？",
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
      "content_sha256": "e017d87efdaf163e85415aa71fe7df6bd6b9f5dcf7753aeb5d8c09aed368a6a2",
      "content_summary": "在 Triton 3.7.1 中，Attention 的 Q/K/V descriptor 把多个 batch/head 展平成 [BHN,D] 的视图，每个 head 占连续 N 行。若一次 load 跨过当前 head 的末尾、但仍在整个 BHN 行视图之内，越过 head 末尾的那些行会读到什么？为什么？",
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
      "content_sha256": "98b744712580e2f60c3b8798d8d59eef639537584e975467cf77231c2b9742eb",
      "content_summary": "Attention 处理不足一个 tile 的尾部 key 时，假设 descriptor 已把无效位置的 K 和 V 都补成零。如果省掉对这些 key 的 score mask，直接让 softmax 和 pV 计算整个 tile，结果会怎样？为什么？",
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
      "content_sha256": "aa4c175c164c399520b507ff9be96004daa37d16c3d6e6126719220f31e4a3cd",
      "content_summary": "在 Triton 3.7.1 中，要把 PyTorch FP16 张量交给 NVIDIA TMA descriptor。设 x 是基址 16 字节对齐的一维连续 FP16 张量，它的切片 x[1:] 调用 is_contiguous() 仍返回 True，却不满足 TMA 的布局条件。为什么连续还不够？传入前应检查哪些量？",
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
      "content_sha256": "3433b0724abec8fd1f8df0b7a6d5c36070704e9887191c3f4dc0da8a6d1c214a",
      "content_summary": "在 Triton 3.7.1 中，把 Attention 的 K/V 读取从“指针加 mask 的 tl.load”改成 TensorDescriptor 的 desc.load。在支持 TMA 的 NVIDIA GPU 上，这种写法带来了什么能力？又有哪些事情不能据此断言？",
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
        "recall_target": "descriptor/tma 带来什么能力,又不能据此断言什么"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-b0cb9529af111050f4401712",
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
      "content_sha256": "9091a4fbe55b13d4274fea4d4492ed7a2bb49eb362dc2325e7a9cd69c9f23b78",
      "content_summary": "Triton 官方 fused-attention 教程（快照版）的普通 FP16 路径中，D 表示每个 head 的特征维度。wrapper 在 host 侧先用 dummy_block 创建 TensorDescriptor，而 autotune 会尝试不同 BLOCK_M/BLOCK_N。为什么每次配置运行前必须由 pre-hook 更新 block_shape，不能指望 kernel 中的 _maybe_make_tensor_desc 自动改正确？",
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
      "content_sha256": "f22e681603b77e1fdf5092ea6a78a46e5e70525677ee4c3ff233d5fff6988b03",
      "content_summary": "把 FP16 数值转换为 FP8 E5M2 时，即使数值落在 E5M2 的范围内、没有溢出，误差为什么仍可能明显变大？已知 E5M2 为 1 位符号、5 位指数、2 位显式小数，FP16 为 1、5、10。请用同一正规数指数区间内相邻可表示数的间距说明。",
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
      "content_sha256": "2fa336d3a99f5145433d4769cd7ac6469102c977fafa677d54a6b20bfbc1ef73",
      "content_summary": "Triton 官方 fused-attention 教程（快照版）的 FP8 路径为 V 调整布局：B/H 分别是 batch/head 数，N 是 token 数，D 是特征维。从连续的 [B,H,N,D] 张量出发，先 permute 成 [B,H,D,N] 并 contiguous()，再用逆 permute 恢复 [B,H,N,D]。最终 shape 已恢复，为什么存储布局仍然改变？删掉中间 contiguous() 又会怎样？",
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
      "content_sha256": "38461a7ba84fd916ccc4f411bd3b75b899993573c59fa94365c8e3b53f31b217",
      "content_summary": "对照两个 Attention 实现的反向结果：参考实现先执行 backward(dout)，再让被测实现执行反向，两边的 Q/K/V、causal 开关和 scale 都相同。为什么两边还必须使用同一个上游梯度 dout？",
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
      "content_sha256": "7d283d022639f0c7fce924472a3d1166102bb21715edf9fd55e57424c9343704",
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
      "content_sha256": "480cd0fb5b2d4bbbce87b439a5da83f2a89bf88949c69fcc91f5100b238afc11",
      "content_summary": "以 Triton 官方 fused-attention 教程（快照版）为例，向面试官用约 60–90 秒解释分块 Attention 前向：输入 Q/K/V 为 [B,H,N,D]，B/H 分别是 batch/head 数，N 是 token 数，D 是特征维度，s 为原始 scale；每个 program 负责一个 head 的 B_M 行 Q，并逐块扫描 B_N 行 K/V。请从完整 Attention 公式出发，说明它怎样维护跨块状态，并最终写出 O 和供反向使用的 M。",
      "dependency_content_sha256": {
        "mc-10797edbc02a90f935980a34": "3557fa158cc620a2375af258dc23e86d0ae3f10151568c54bc6e326465bc06a8",
        "mc-3792ef72898b22610a7791b1": "e61f4001baa49c7e2fe55945088391e83d270c04d63eacfdb64323330ce4cb9d",
        "mc-55086c744857d6967c992455": "37190aa0b111dc0bb43863801ff2c6140bcf175f2ca65d08f853cf3152095743",
        "mc-5b8520cad91de49d0fce0551": "a4db0ff069983c51f7ebafa7ef3330a0bb93c60f61604a2b08cee835cb4860f5",
        "mc-dfeb90dfa04b47718a46bbbb": "d4c40f5d0db933b0925f4d3406cab9305bb671e1d608f79f66e9f983f0e5ee19"
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
        "summary": "已对照更新后的子卡 card-01、card-03、card-05、card-07、card-10 复核：card-05 改为按轴的含义推出 acc=[B_M,D] 并降为 B，card-03 改称“Triton 官方 fused-attention 教程（快照版）”，card-01、card-07、card-10 只改来源标签；参考回答压缩到约 390 字，题面补上听众（面试官）与教程版本，五个评分锚点只统一了中英文间距，每个锚点仍有子卡支撑，没有引入子卡之外的事实。"
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
      "content_sha256": "d60b540f5eed199594855dbcfa4be48b83848dd35324a069903ed5d6ae57fad1",
      "content_summary": "以 Triton 官方 fused-attention 教程（快照版）为例，向面试官在 90 秒内解释 Attention 反向的数据流：前向已由 Q/K/V 得到 O，并为每个 query 保存归一化统计量 M；现在收到损失对 O 的梯度 dO。请说明怎样利用保存量、计算 Delta、按块重建概率，并通过输出分工得到 dQ/dK/dV。",
      "dependency_content_sha256": {
        "mc-08e5a0a6586998294cb74792": "fd24c06e2269d63b391e2926810e49e10d92e96b6be04cd52db960953edd97b8",
        "mc-86ae6ff76a84b4c6a1b9232a": "412591b356ad7c43d2750adda36038c2a110d74338b74cb3f088d5c562e68521",
        "mc-ac4172de0a8bc2a4d40c0eca": "854f3ff115cd22fc9e0df4260173b18595a3f7ae3be7f8b4878674ce10baf365",
        "mc-dfeb90dfa04b47718a46bbbb": "d4c40f5d0db933b0925f4d3406cab9305bb671e1d608f79f66e9f983f0e5ee19",
        "mc-e3916767857f2d3c67d3f4c6": "285990076c2795a143cce7fdfdeb24c3ba91adce323b130934e28729ee87c5fb"
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
        "summary": "已对照更新后的子卡 card-10、card-14、card-16、card-17、card-19 复核：card-14 改称教程快照版，并在说明首句点明“重新计算了 P”是对的；card-16 点明“O 与 dO 相乘”是对的、只错在归约轴；card-17 在 Delta 式旁补上实现用的 Σ_d O·dO 形式；card-10、card-19 只改来源标签。参考回答压缩到约 400 字以内，题面写明面试官、教程版本和 90 秒，锚点 4 改为只考 G=P⊙(dP−Delta) 及 dQ/dK/dV 各由哪两个量相乘，五个锚点均由子卡支撑。"
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
  "manifest_payload_sha256": "a0ef972dbf58d05a14abb119030e08687a39d4239305138ece15272e1c5bb9c2",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 8218,
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
          "content_sha256": "8c2ee515977d546f9a8fe9e4cd33dcdb58fc5244063f30231773f1468339e59f",
          "logical_id": "mc-f949a09a279ca9bbaedd40ee",
          "row_sha256": "ec6c7938d7fcd65dbe381bf25b34a89a53a08f3bf231b9a2a429f441811a90e1"
        },
        {
          "content_sha256": "285990076c2795a143cce7fdfdeb24c3ba91adce323b130934e28729ee87c5fb",
          "logical_id": "mc-e3916767857f2d3c67d3f4c6",
          "row_sha256": "6ecd6d4d022350236f9f0d495b9ad06c492775261af9f4e3389d698401319ef5"
        },
        {
          "content_sha256": "fd24c06e2269d63b391e2926810e49e10d92e96b6be04cd52db960953edd97b8",
          "logical_id": "mc-08e5a0a6586998294cb74792",
          "row_sha256": "7fb24c6e5cc34be005a0702edfa7c6cabf4a69e4aa33dd81b14e1b50113c8891"
        }
      ],
      "sha256": "ebcb16e8cb77857e57def095a0fe07973a3de85c5f9c5a893d6a94cfba0c31a8",
      "sheet_name": "cards",
      "table_sha256": "0f50b18a19a6579df494d96ff84284819a3269dc1ce7ad683251d23756ec9bad",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 50844,
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
          "content_sha256": "3557fa158cc620a2375af258dc23e86d0ae3f10151568c54bc6e326465bc06a8",
          "logical_id": "mc-10797edbc02a90f935980a34",
          "row_sha256": "2372e81d6db1efe55bb01f4ec5523a6281474850e067f0652952286ee2c7135e"
        },
        {
          "content_sha256": "846dcb45d529bca5dda85cd42e4035edb2fe6e0183e7bc2b4acf4dac2d2c9850",
          "logical_id": "mc-6f4b77efdda16289ca9f840e",
          "row_sha256": "6e5c16233fe299c16cc715562d405837e5d2d30ec515f11ced81352e20747ac4"
        },
        {
          "content_sha256": "e61f4001baa49c7e2fe55945088391e83d270c04d63eacfdb64323330ce4cb9d",
          "logical_id": "mc-3792ef72898b22610a7791b1",
          "row_sha256": "ef386ae70a24d4d2e4e757d7bd67fb7f6c461126a3af960a925e0d69f1a97ee3"
        },
        {
          "content_sha256": "3943e7504e51f4f965457a8d91e6ae7ef37f2af817fdb26e2b65c2a494f91c1d",
          "logical_id": "mc-525509f1b67e10f3367a6740",
          "row_sha256": "ea2eb7b789533136191cabd2f0b019559ddb9b5accc4d110db5aa1e9f015d38e"
        },
        {
          "content_sha256": "a4db0ff069983c51f7ebafa7ef3330a0bb93c60f61604a2b08cee835cb4860f5",
          "logical_id": "mc-5b8520cad91de49d0fce0551",
          "row_sha256": "1e904212ccec73ea4086f82593b2599062787b2e9d3eca8430b900b13c1fbdf3"
        },
        {
          "content_sha256": "37190aa0b111dc0bb43863801ff2c6140bcf175f2ca65d08f853cf3152095743",
          "logical_id": "mc-55086c744857d6967c992455",
          "row_sha256": "1a00a45974b90c5789e91d5ff622b1b88285310efaef5bdd5c70112f659aef04"
        },
        {
          "content_sha256": "0fde9af627aeffd30f8bbb7ff373d119b0032f0a83c6aa3251f3d3eba01bb067",
          "logical_id": "mc-5fa9999050b2b9eed656dd49",
          "row_sha256": "b651b6b62a3701588e333ae92bf1399a3bbd8274df7b2c6ec3e0a9306d34136a"
        },
        {
          "content_sha256": "636b670dec83b23805927014b24c8be0756d1fad3cd9bc867d0b3c359e7a8475",
          "logical_id": "mc-36841e7e2e57cd392d7bd040",
          "row_sha256": "12ba56a6a9cfac11b99d9cc65506376ff70b6f9d964a1202188b0a2e49c104b1"
        },
        {
          "content_sha256": "051442f2ce8455255f1f45ef4ef68cf5a6214d31b4577aec28aff227a4b37d11",
          "logical_id": "mc-e618c051620589a255fa9cad",
          "row_sha256": "f9a77300f15724a51b4484e6e1afa1217eb11fb01532a9f5549a7e427e739b61"
        },
        {
          "content_sha256": "d4c40f5d0db933b0925f4d3406cab9305bb671e1d608f79f66e9f983f0e5ee19",
          "logical_id": "mc-dfeb90dfa04b47718a46bbbb",
          "row_sha256": "37495f86703eb65ad024974579d8fe039b347a15e25c5eec6a29e72063c8da41"
        },
        {
          "content_sha256": "1d0b4d8822752addea106ce1e1c3ec7e7de46a651479b23ee320037d658db52f",
          "logical_id": "mc-8d6f166747439b6c1751a274",
          "row_sha256": "e892c55d576fafbaac7272b038c5c64932cba41591d0f61fb96602a09fdc9c93"
        },
        {
          "content_sha256": "09a86bd283c61a74130c200f7d05c780e71db8b51d1efff834b3fa061d8532c0",
          "logical_id": "mc-e24771d0d0fe04e94cc22fc6",
          "row_sha256": "503822ac9be0582bbe0e59382c02b5aabf36673ce32e41161ebb0bea9da61135"
        },
        {
          "content_sha256": "ba12ba27881459f55e96124d2b208510d07baeee013381e0693076672d154b4a",
          "logical_id": "mc-3b1feda15f9269b40346e62a",
          "row_sha256": "b0c271d97d8f548d36467e23add2a02cf4be96655edbbf0bc2c0e424e475ab96"
        },
        {
          "content_sha256": "7ba3db8598788376f7724a9232db4bc8926c15d89528a3c26ce394ff35d5997b",
          "logical_id": "mc-963d2f25bb957912e1c6ed99",
          "row_sha256": "1ed5614be7795e2e95728e419c60afdff5b3aead3f08db35f9be2ac22b3abb32"
        },
        {
          "content_sha256": "412591b356ad7c43d2750adda36038c2a110d74338b74cb3f088d5c562e68521",
          "logical_id": "mc-86ae6ff76a84b4c6a1b9232a",
          "row_sha256": "4583748190194620c837df803ca9e7b77336c145962902140e62cacd88e39472"
        },
        {
          "content_sha256": "ee008381d5536518b3df8418d81f68005cff5af5e900cee1754ab80c1ebbfb63",
          "logical_id": "mc-9a62292e5f5afbe601084713",
          "row_sha256": "baef8e9e2c262ec31ef2465abbaf0d6890bc7cabe74085c0945ea59be7627dee"
        },
        {
          "content_sha256": "854f3ff115cd22fc9e0df4260173b18595a3f7ae3be7f8b4878674ce10baf365",
          "logical_id": "mc-ac4172de0a8bc2a4d40c0eca",
          "row_sha256": "5ca340e0450f1c9a0312e17c5a0f70dfac54d5fb8853287815f40637e6d6f9ca"
        },
        {
          "content_sha256": "4b81c9a1068f987035a6cb547e0df1c16c867d580c8906afacbcef4765683918",
          "logical_id": "mc-37343051f020c2bb32857654",
          "row_sha256": "06e29f9f879061eb26a5413a36e9f54278e369869c8528996f35411b17f96227"
        },
        {
          "content_sha256": "37facdceef59ea25ab767dce91e0742fcc745205d150bd5cec4bc60ed0f3650f",
          "logical_id": "mc-a3da6f89f9dfff794380bacf",
          "row_sha256": "546a2869af633f2dcae1627c5fe8c915d4742c673d91f69b085c59246c3941e2"
        },
        {
          "content_sha256": "d2edd7d58e1f56fd288302875b990d6f6c658a0a785f73919f0bde8e4837bde9",
          "logical_id": "mc-fe884cab68b5fd014c895d48",
          "row_sha256": "649c68d056ef921d20aac5a807e466607c74cd73ea39c7b86101ec98a197723c"
        },
        {
          "content_sha256": "e017d87efdaf163e85415aa71fe7df6bd6b9f5dcf7753aeb5d8c09aed368a6a2",
          "logical_id": "mc-7b624650264561327c5db3e9",
          "row_sha256": "d89d3c5a7ab8d93d2b42e5c8fd93e3e8033a3b087f7bbe1e9fff47dd61a92909"
        },
        {
          "content_sha256": "98b744712580e2f60c3b8798d8d59eef639537584e975467cf77231c2b9742eb",
          "logical_id": "mc-e0f9e3ccb87093480e0c4aaf",
          "row_sha256": "2bacc27ae3a13cdf3361bb3f6def666438a07359ab9af17cb93012376b3ed8d5"
        },
        {
          "content_sha256": "aa4c175c164c399520b507ff9be96004daa37d16c3d6e6126719220f31e4a3cd",
          "logical_id": "mc-0c544303457fe69beb458570",
          "row_sha256": "10d3422d869b30f85b68f75f3fbb37e9c91eef6db2c28c4c9bb89590654b5dd7"
        },
        {
          "content_sha256": "3433b0724abec8fd1f8df0b7a6d5c36070704e9887191c3f4dc0da8a6d1c214a",
          "logical_id": "mc-b0cb9529af111050f4401712",
          "row_sha256": "82626fc052967260ac42c8ffa02c5d8f6a70960845cb4fe4046d6fd6d5583688"
        },
        {
          "content_sha256": "9091a4fbe55b13d4274fea4d4492ed7a2bb49eb362dc2325e7a9cd69c9f23b78",
          "logical_id": "mc-1e17c1d1f03d092cf091e666",
          "row_sha256": "6fed58cd4d01ea5841b811ed80ce3d5e490081f10ab5a78351f262f4f9b20461"
        },
        {
          "content_sha256": "f22e681603b77e1fdf5092ea6a78a46e5e70525677ee4c3ff233d5fff6988b03",
          "logical_id": "mc-491e7d022820a6bb4bb79c70",
          "row_sha256": "4536d5d18607130bb8de969715c6abbd6dc1f3b4a049147281538fa99aa37004"
        },
        {
          "content_sha256": "2fa336d3a99f5145433d4769cd7ac6469102c977fafa677d54a6b20bfbc1ef73",
          "logical_id": "mc-12391b0b8209a8b11ff4e0a8",
          "row_sha256": "87d006a87ae5333a668555c69f67b80d5c251d124f0a5c995694af4dc0d03455"
        },
        {
          "content_sha256": "38461a7ba84fd916ccc4f411bd3b75b899993573c59fa94365c8e3b53f31b217",
          "logical_id": "mc-4fe59a4647c233625e064594",
          "row_sha256": "0579cd0d29cb47ce7c35d5dde74dd4bfe0022713ab9211e759faed0528d3f30f"
        },
        {
          "content_sha256": "7d283d022639f0c7fce924472a3d1166102bb21715edf9fd55e57424c9343704",
          "logical_id": "mc-51f97e147966f83c6771ca89",
          "row_sha256": "74c3502a3a962d5dab5041a1b2ca507dabfb3f1537c2acda080339f2b54e958e"
        }
      ],
      "sha256": "ce192dd2029ef2210483a7554a4e7096fb18be9d6e1192b4ebb9363fd06480ed",
      "sheet_name": "cards",
      "table_sha256": "8cb757886a4897c3dd46b478865a75b6f8272b4f693021aaf9184a046f9534de",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 6536,
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
          "content_sha256": "480cd0fb5b2d4bbbce87b439a5da83f2a89bf88949c69fcc91f5100b238afc11",
          "logical_id": "mc-ee6220cfc1f9d4a258aa6297",
          "row_sha256": "04f56bd2eed0b794e5533d696ae5ca90765cd359e705eea3da2608eac53f6e8e"
        },
        {
          "content_sha256": "d60b540f5eed199594855dbcfa4be48b83848dd35324a069903ed5d6ae57fad1",
          "logical_id": "mc-6e28784a6781cdeaed0ec32f",
          "row_sha256": "0180322ed50bc9ceb856beb95bad78c7f02d2cb5c5ad1834f2cb3230312955d3"
        }
      ],
      "sha256": "ef5ffa3b1cbe9bb6f284cc20418287b12e8fa702337d666d4fe50593c790a74a",
      "sheet_name": "cards",
      "table_sha256": "30c8831f0a556ba64488ef70ed62589575ee544163e9cc6ea51b60df4d9896c8",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "f04b66137a8b61b0c8969599c33883de1c3e9169b545321bf4b9508028a27422",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "attention-early",
      "path": "docs/triton-learning/logs/2026-09-19-fused-attention.md",
      "sha256": "1e51f24058b1b7b546dd9c901fab1f48e8adb1e21b6279d495940be36f864d56",
      "summary": "9/14–19：概念、在线状态、反向与真实纠错"
    },
    {
      "collection": "triton-study-logs",
      "id": "attention-late",
      "path": "docs/triton-learning/logs/2026-09-24-fused-attention.md",
      "sha256": "755e51eeb97bc72caf893978d40e46aff500b2e185096fdfba1dc5632ec2a17f",
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
