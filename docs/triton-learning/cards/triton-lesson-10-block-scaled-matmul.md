---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "addf88da03699cb4d574cfdc3d83b57cd34d4596f317d425709bdee27d9f771a",
  "candidate_sha256": "27e9d0534ffb95a2b0fef2d7aa65089e57a6c557d66462f25039c37091f9f033",
  "cards": [
    {
      "content_sha256": "67fac8defcfebef76940a86226d7d4d593093848b289c623f5e366b24ce60411",
      "content_summary": "scale 只平移；FP4 窗口 3.58 档必须分块，FP8 17.8 档常可整张量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为什么 fp4 必须分块配 scale, 而 fp8 往往一个整张量 scale 就够?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c6ff59ea5ef045fc55f6a23f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "77d4848c5ff60c4955257562af9c62f61fe6abf73c82ea88cac973baded10941",
      "content_summary": "MXFP4 与 NVFP4 的块 scale 类型之争：E8M0 范围宽但对不准 6，E4M3 对得准但窗口窄、多读一趟",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "mxfp4 与 nvfp4 的块大小、scale 类型、位数与代价各是什么, 怎样取舍?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f976aa38b9879032b0c34640",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8a84d64b78a91da06c62043076285413652ee3e6614a9380688f77fc020e8af4",
      "content_summary": "NVFP4 每张量 scale 只定位 E4M3 窗口；块间跨度超过 17.8 档时小块 scale 下溢、整块变 0",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "nvfp4 的每张量 scale 解决什么、解决不了什么, 块 amax 跨度过大时会怎样?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d0cadfeaa8b31d4fdf194f4d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "27ccc4cd983a197bc58eebfc39cab098c4974028457245930412f3b304061345",
      "content_summary": "整 batch 共用的每张量 scale 让结果依赖 batch 组成；按 token 设第二级 scale",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "线上 nvfp4 激活量化时, 为什么一个异常 token 会让同 batch 的别的 token 出错、单独跑又正常?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1b6b6bf5b5cae30680cd15b3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4695cb40c657e53c8b64474a5c660590a187a9f36807a82f1d68bc32de0b8d3b",
      "content_summary": "OCP 向下取整让块最大值进最上档，代价是截断；向上取整避免截断但小值更易变 0",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "ocp 为什么按 ⌊log2 amax⌋ − 2 取 mxfp4 的 scale, 和向上取整相比代价在哪?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-26b2bd02cc7fc3baad3d7816",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fa71174624dedb7b89ce4b1d5ecef80a366f5684221ae2c2b0b06e6c0e5e7bd0",
      "content_summary": "不随 k 变的 scale 提到最外层；块 scale 只能逐块乘，三种位置数学等价、按硬件选",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "块缩放矩阵乘里, scale 可以乘在哪一步, 由什么决定, 各由谁采用?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e236c2fffc4d370ff9caf8a7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c31a39752a280c5af11ab15a0b8ae321649144da9fe9ad6913053bf4d98be279",
      "content_summary": "K 块须由整数个 scale 块组成且同起点；M、N 方向不必对齐；split-K 从 V 的倍数开始",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "kernel 的分块与 scale 的分块必须怎样对齐, k 方向与 m、n 方向有什么不同?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-385020ed4fdd34484e631abf",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dfa884434bb15e74272c6dcf0d37b73ef501fe5665682e9e29a36e839d57882a",
      "content_summary": "H100 上把 scale 乘在部分和上的代价与乘 scale 次数之比，以及 DeepGEMM 每 128 个 K 一组的两个理由",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "在 h100 上想用 fp8 张量核跑 mxfp8, scale 放哪, 条件与代价是什么, deepgemm 为什么取 block_k = 128?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0be1cfb5e7e0f6f93e2c2381",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8d9b52bf220ec98a591658dc1b390cff5a5aa8a05707bd78f183462e4c359256",
      "content_summary": "5D 预排让字节顺序等于 TMEM 顺序；tcgen05.cp 原样拷；kernel 里的 reshape/trans 只是视图",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "blackwell 教程为什么把 scale 预排成 (m/128, k/v/4, 32, 4, 4), kernel 里的 reshape/trans 为什么不搬数据?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-5a62d0166df698913c98a27d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "489e8bad9dc91bbf86611c5da25a0a081c9643478f2704a2f96d709839612c40",
      "content_summary": "TMA 规则分别约束块与整个张量；二维 scale 描述符 MXFP4/MXFP8 建不起来；报错时机",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "tma 描述符的三条规则各约束哪个形状, 二维 scale 描述符在哪些格式上建不起来、错误何时暴露?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-dfa47e6149b7d295651f617c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e54a5c1c51a95f1192711ffbeacf6cd6fa0dd0ae15daa519cff36e98c86f3b9a",
      "content_summary": "tl.dot_scaled 走原生、软件换算还是编译失败的判定规则，以及五种目标各落在哪一类",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "同一个 tl.dot_scaled 在 sm_100、sm_120、sm_89、gfx950、gfx942 上各落成什么, scale 放在哪, 代价在哪?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-fb0c625aeade1143e630eb7b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "23fccd3f68e209681f61b053c1e479a800600219cf844faa191a3236fea81183",
      "content_summary": "搬到 RTX 5090：绕过入口检查，缩小分块以适应寄存器与共享内存",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "把 blackwell 块缩放教程搬到 rtx 5090 要改什么, 为什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-30df6d9a5c0fd8e684af2f17",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "58554aa9677a121a83c23ced304c6e658fa077a222a3237ba7777f30429ba842",
      "content_summary": "MI300X 上 bf16 对 MXFP4 权重：解码最多快约 3.6 倍，预填充最多持平、解码藏不住时慢约四成",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "mi300x 上 moe 专家权重存 bf16 还是 mxfp4(走一侧模拟), 解码与预填充各怎样判断?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-281380095aabd19ad91c51d6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "79ab2459a7162eb7f525e5b3d1083526b4fe0ad0489be53bf8b9b83aa70520a0",
      "content_summary": "按资源忙碌时间估算：解码对 MFMA 为 16c/BM，解码对带宽为 0.244c",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "怎样量化估算“解码能否藏进矩阵乘”和“解码能否跟上显存带宽”?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-455b749f88ebfaba60062e8d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6a9c850c84d5fc3f8d067ed94cd87e47d1ce4921c457094e426eeace587cfe0f",
      "content_summary": "软件换算在每个 warp 内解码；warpsPerCTA 决定重复解码与每份的复用次数",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "warpspercta 的排法怎样影响软件换算路径的解码量与复用次数?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-be5feb89a08576b9a714cf5b",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7d28c6750b9ce83c1f4fa62929e7cd208027a677a7a0faa1acaf9dbaf9b80756",
      "content_summary": "打包 FP4 原样交给 dot_scaled；沿 K 的偏移按字节；rhs_scale 不转置",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "在 triton kernel 里把打包的 fp4 交给 tl.dot_scaled 时, 要不要拆包, 偏移怎样算?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-23c1c68e40760d05b71a8647",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4e39e9a979a73098aba1f4c86f3141013c81dc6a264d981233fd0a067b97fbcc",
      "content_summary": "按最忙 SM 的每个调度器估发射时间；线程级与 warp 级条数差 32 倍",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "怎样从 sass 指令数或每元素的线程级条数估算 gpu 上的发射时间?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-82b94c492ffa21b4e82a3f04",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "10a74e6ff07ccb1735736b4cb3afc0a42ac707d111508ac71c24511f875a4648",
      "content_summary": "实际总时间靠近 max 还是 sum，由每个调度器上能轮流的 warp 数决定",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "已知发射时间与显存时间, 总时间的上下限怎样取, 实际靠近哪一端、受什么限制?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c87676f61863c78bcbf9f2e6",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "255bc30bde5a2a8e36bd78f419434df0c457cd4e6f6ae7f37d1cee72daa5d7ca",
      "content_summary": "格式范围按 log₂(最大/最小正值) 量；E2M1 为 3.58 档",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "怎样量一种浮点格式的范围, e2m1 为什么是 3.58 档而不是 3 档?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-82357876d3d94994eda54ed6",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "eccc0ea148135178f9a7af5a872b39cd623b78cfed98447d40aa18553b3f95cd",
      "content_summary": "离群值的影响要看占比与每块损失；真实系统用小块、Hadamard 旋转、敏感层 BF16",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "块内有离群值时, 为什么“离群值很少”不足以支持选 e2m1, 真实系统怎样压低离群值的损失?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-034e387fadad8ebbc0e6a813",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d490c197a9aaddbd0b097208f6155739ebe5b63c613727449ef1d8006f02f720",
      "content_summary": "E2M1 就近取偶：按档定间距再整数舍入，饱和放在舍入后",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "缩放后的值怎样就近取偶舍入到 e2m1 格点?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5516e8dc029539f4cd2a7d20",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f1311176e7d0b3001e5f8d3451507c9dab471a313406c6042a519bf0c17ff831",
      "content_summary": "不预排时全体 warp 搬 scale、读 4 遍、多两次等待",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "sm_100 上 scale 不预排时, 从 smem 到 tmem 的路径与额外代价是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-baa834639ffae733c9e8be5d",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f8f144cb1c42b41c682395daeeefa650ed97318962efb2b77bf4e4d7cc98ea82",
      "content_summary": "用数位拆分推导 scale 形状链；区分硬件固定与随分块变化的数字",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "怎样从目标推导预排 scale 的形状链, 哪些数字由硬件固定、哪些随分块和输入变化?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-36e11025799d6f84e627893b",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e926a60cff12385f62a841b53d7fe7d3680496c2a59acb014352100b0c9de05c",
      "content_summary": "BLOCK_K 只受粒度约束；TMEM 不紧，共享内存与级数才是限制",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "blackwell 块缩放 kernel 的 block_k 是否被 tmem 和 v 定死, 真正限制它的是什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-cf106f94c307b097e01f50c5",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9f4a978f5a9c23c4bb3b006d52c7fe25340d7e3253be76202747c4f508858cc6",
      "content_summary": "AMD 预排让每 lane 的 4 个 scale 相邻，LDS 读取从逐字节变成 32 位",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "amd cdna4 的 scale 预排与 nvidia 的目标有什么不同?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-32cb7a3958719df772201f26",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8aac8d8a023646bbda0d69eb7b40a6eb8ed92c17517ea82e7570f45d7f182b43",
      "content_summary": "FP4 编码等于有序格点下标；低半字节放偶数元素",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "把量化后的 fp4 值变成编码并两两打包成字节, 怎样用整数运算做?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f5fd3b25c2b1051f48aa2bc0",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bf5793840921b5f7974de23532e06036d6afd021e37b04f45819939a5ad64a7b",
      "content_summary": "数值测试分不出原生与软件路径，要查编译产物",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "为什么数值测试证明不了块缩放 kernel 走了原生指令, 要怎样测?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-401590969bcaa1ef6ff794b7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "18bef0895bff69b7f3272b5ca7a6404d4e11a48e106331803e1c869591759723",
      "content_summary": "软件换算的解码与 scale 处理之分；SEL 是 NaN 处理，fast_math 可省",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton 软件换算路径里解码与 scale 处理各包含什么, fast_math 省掉什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-739b495a4d363d6539380874",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7acdbf3e3622c530d3e86ccc8ff177818ea022edaae2aa593cae4bf07dbf803e",
      "content_summary": "E2M1 胜在块最大值附近格点多，而非 0 附近",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "元素格式都配块 scale 时, 为什么选 e2m1 而不是 e3m0?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1b27b1ffae129f2ba42ee08d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e296bc184d75bdd2d1adea21484221101e3990afc6a3666773e63de9045b88ae",
      "content_summary": "E8M0 指数 −127 到 127；截断避免全零块写出 NaN",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "e8m0 scale 的指数范围是多少, 量化时为什么把 e 截到 [−127, 127]?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-bd3becea988ba214a166dfb5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cf4134fb2ec766acc597a2299776777af8bc091932772b743e388e3e4307afba",
      "content_summary": "乘在部分和上需 V ≥ 指令 K；2 的幂 scale 可在低精度内换",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "有低精度 mma 时, 块 scale 是否一定要乘在部分和上, 前提和例外是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-22af7057aad390b599c70b08",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d2e0d0ef34cfe3b11a72b3b197563d4c1785a1eb1151b8d87fc65b5d2d45594a",
      "content_summary": "trans 管下标含义而非访存；写错静默算错",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "scale 预排后 kernel 里那次 trans 起什么作用, 漏掉或写错会怎样?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c4e84caf7808f58085e182fa",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "37f262ddfdb5265463a44759d02fa4643e7e5874e15914fbcddb1c202312d5e6",
      "content_summary": "MXFP4 权重始终保留的是容量，不是访存量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "权重存 mxfp4 在任何负载下都保留的好处是什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-af0e33b93ba22e83c454dd0f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ff86c896e0c75e6bbfc42f6ce12fc0d8d22aa8c0302bd2fdb48a31f3684817c3",
      "content_summary": "强度与平衡点同单位：乘加 123，FLOP 247；计入输出后 MXFP4 专家约 124，处在平衡点附近",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "算出的计算强度和平衡点比较时, 单位要怎样统一?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6b8a6ac1e7ef6441eb8a60e1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "699cb403877bdc119a56a85b8c75aefa60c7f81aef71645f66020745140bdc72",
      "content_summary": "解码占比 16c/BLOCK_M 与 M 无关",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解码能否藏进 mfma 与 m 的大小有什么关系?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-63cae5cd70cc11611b5399eb",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "653f53412d5e0a3f06103e4224ce62d2fbd0fb5f10ef9981b92b91f9d8b00b72",
      "content_summary": "int 底数配 int 张量指数仍是 int，2⁻¹ 变 0；uint8 减法回绕",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch",
          "version": "2.13.0"
        },
        "recall_target": "torch.pow(2, e)(e 为 int32 张量)为什么得到 0, 同类陷阱还有哪些?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e04e352a1f9e05fd644b3a02",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d183e243dac9a8ec13b63d346e423e60cd7c667724c01857001b54d595a467ef",
      "content_summary": "块宽错编译报错，前进量错静默读错；测试要有多个 K 步",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "kernel 的前进量写错与块宽写错各会怎样, 测试怎样才能抓到前进量的错?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e2fba85bcd99b38a89b3f5f8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e9b4e7d11c902752904fd33b8fb61e63199b47c38aa990206ed07caa886ab195",
      "content_summary": "小端位流：第 0 个元素在第 0 字节最低位；往返测试抓不到约定错",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "6 位元素按小端位流打包时字节里的位怎样排, 为什么往返测试抓不到位序错?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c9bcfe52ab839d10dad93cd1",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "871075c898af5d02b36a49177fac3d12e93e54f10d80b8125be2af3940695dc9",
      "content_summary": "复用次数按 warp 子块与实际解码的操作数算，不是 BLOCK_M",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "估算软件换算路径的解码开销时, 复用次数应按什么算?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-79720aded9a054c2c531be18",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4f0133cb16c9cdf5f5ffb7720281fe473d4086448f9bb6de374c9bd82832ee3f",
      "content_summary": "按同一字节数算出的带宽差就是耗时比，不能当原因",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "解释两条路径的耗时差时, 能否用“按最少字节算出的带宽差”当原因?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-67d438cf55759feb8f8b68a8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "024730bdf0ce48f4f33e2429fe150079114416d1d1ac8682346d96f28fe758db",
      "content_summary": "计算受限时比值 = 峰值比 × 效率比；溢出出在未选中的配置",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "计算受限时两条路径的耗时比怎样拆解, 为什么不是峰值比?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-62beb53d71b97bf090ffbd2f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f08dcb8978f87f2af56f60209e2e8c75d5939da499c51057fd151cd58f1941dc",
      "content_summary": "指数取所在档的左端；尾数等分一档",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "浮点数的指数段取的是哪一个 2 的幂, 尾数怎样表示档内的数?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e6288e8d97ab5cfd9dc26f15",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9349971fc93b083a4362a65e119529d8201b7c9180264c794e048584f9c4cc9e",
      "content_summary": "MX scale 交给 Triton 用 uint8；float8_e8m0fnu 的转换不是 OCP 取法",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "给 triton 的 tl.dot_scaled 传 mx scale 时用什么 dtype, 能否用 torch.float8_e8m0fnu?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-aff6698aa51d74780aa2bff5",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6eb520096680d3829e74d704ad86e5ed142f549773b2026c0009a9d8ea42ae77",
      "content_summary": "一个解码出的元素参与 BLOCK_M 次乘加，不是 BLOCK_M × K",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "一个 cta 里, 一个解码出的权重元素参与几次乘加?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c5458d9bf53e30e69cdf8922",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b35370dbc8afc5bfb4168ad5e4f2269e459fab8e367b53f260e915dc086372df",
      "content_summary": "口述块缩放格式的必要性、E2M1、MX 与 NVFP4 的取舍、scale 的取法",
      "dependency_content_sha256": {
        "mc-1b27b1ffae129f2ba42ee08d": "7acdbf3e3622c530d3e86ccc8ff177818ea022edaae2aa593cae4bf07dbf803e",
        "mc-26b2bd02cc7fc3baad3d7816": "4695cb40c657e53c8b64474a5c660590a187a9f36807a82f1d68bc32de0b8d3b",
        "mc-c6ff59ea5ef045fc55f6a23f": "67fac8defcfebef76940a86226d7d4d593093848b289c623f5e366b24ce60411",
        "mc-d0cadfeaa8b31d4fdf194f4d": "8a84d64b78a91da06c62043076285413652ee3e6614a9380688f77fc020e8af4",
        "mc-f976aa38b9879032b0c34640": "77d4848c5ff60c4955257562af9c62f61fe6abf73c82ea88cac973baded10941"
      },
      "depends_on": [
        "mc-1b27b1ffae129f2ba42ee08d",
        "mc-26b2bd02cc7fc3baad3d7816",
        "mc-c6ff59ea5ef045fc55f6a23f",
        "mc-d0cadfeaa8b31d4fdf194f4d",
        "mc-f976aa38b9879032b0c34640"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用 60–90 秒讲清块缩放格式为什么存在、mx 与 nvfp4 怎样取舍、scale 怎样取。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-b454b74ff5412e8cdecb6903",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已依据更新后的子卡 01、02、03、05 复核：参考回答与五个锚点只用到子卡仍保留的事实（3.58 档、平移不加宽、E2M1 多给尾数、MX 与 NVFP4 的块大小／scale 类型／位数与代价、OCP 向下取整的截断代价），内容不需改动。"
      },
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "030256112b852926af7fe5f8b6e2d4f1d2251c5087bfbfc810465d11973f5406",
      "content_summary": "口述 B200 上块缩放的 scale 位置、预排与路径，以及换卡后的落地",
      "dependency_content_sha256": {
        "mc-30df6d9a5c0fd8e684af2f17": "23fccd3f68e209681f61b053c1e479a800600219cf844faa191a3236fea81183",
        "mc-5a62d0166df698913c98a27d": "8d9b52bf220ec98a591658dc1b390cff5a5aa8a05707bd78f183462e4c359256",
        "mc-e236c2fffc4d370ff9caf8a7": "fa71174624dedb7b89ce4b1d5ecef80a366f5684221ae2c2b0b06e6c0e5e7bd0",
        "mc-fb0c625aeade1143e630eb7b": "e54a5c1c51a95f1192711ffbeacf6cd6fa0dd0ae15daa519cff36e98c86f3b9a"
      },
      "depends_on": [
        "mc-30df6d9a5c0fd8e684af2f17",
        "mc-5a62d0166df698913c98a27d",
        "mc-e236c2fffc4d370ff9caf8a7",
        "mc-fb0c625aeade1143e630eb7b"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清块缩放矩阵乘在 b200 上怎么做、换到别的卡会怎样。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-d1dda4cc075c9bc27a784223",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已依据更新后的子卡 11 复核：11 的判定规则把“两侧都带 scale”限定为 sm_120 原生模式的额外要求，本卡边界同步改为“一侧不是低精度格式，或过不了原生模式的要求时退回软件换算”；参考回答其余内容与四个评分锚点仍由子卡 06、09、11、12 支撑。"
      },
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "98a0888dba45f3c8478da8df8df2979b01a70d938108f01b29250857d068c226",
      "content_summary": "口述 MI300X 上 MXFP4 权重的快慢判断与部署选择",
      "dependency_content_sha256": {
        "mc-281380095aabd19ad91c51d6": "58554aa9677a121a83c23ced304c6e658fa077a222a3237ba7777f30429ba842",
        "mc-455b749f88ebfaba60062e8d": "79ab2459a7162eb7f525e5b3d1083526b4fe0ad0489be53bf8b9b83aa70520a0",
        "mc-63cae5cd70cc11611b5399eb": "699cb403877bdc119a56a85b8c75aefa60c7f81aef71645f66020745140bdc72",
        "mc-6b8a6ac1e7ef6441eb8a60e1": "ff86c896e0c75e6bbfc42f6ce12fc0d8d22aa8c0302bd2fdb48a31f3684817c3",
        "mc-af0e33b93ba22e83c454dd0f": "37f262ddfdb5265463a44759d02fa4643e7e5874e15914fbcddb1c202312d5e6"
      },
      "depends_on": [
        "mc-281380095aabd19ad91c51d6",
        "mc-455b749f88ebfaba60062e8d",
        "mc-63cae5cd70cc11611b5399eb",
        "mc-6b8a6ac1e7ef6441eb8a60e1",
        "mc-af0e33b93ba22e83c454dd0f"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清在 mi300x 上是否把 moe 专家权重存成 mxfp4, 怎样量化判断。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-3d3e052793ab6f4d8ea66293",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已依据更新后的子卡 13、14、36、38 与新加入的 37 复核：强度计入输出字节后，M = 128 的专家处在平衡点附近，边界与第一个锚点已同步改写，并删去子卡不支撑的“wave 沿 M 排”。"
      },
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d63b8369a7758503ce339cb8b577733baa4ef13b757506433423bc2b9e9133af",
      "content_summary": "口述 RTX 5090 上原生对软件换算的测量、解释与预测错误",
      "dependency_content_sha256": {
        "mc-62beb53d71b97bf090ffbd2f": "024730bdf0ce48f4f33e2429fe150079114416d1d1ac8682346d96f28fe758db",
        "mc-67d438cf55759feb8f8b68a8": "4f0133cb16c9cdf5f5ffb7720281fe473d4086448f9bb6de374c9bd82832ee3f",
        "mc-79720aded9a054c2c531be18": "871075c898af5d02b36a49177fac3d12e93e54f10d80b8125be2af3940695dc9",
        "mc-82b94c492ffa21b4e82a3f04": "4e39e9a979a73098aba1f4c86f3141013c81dc6a264d981233fd0a067b97fbcc",
        "mc-c87676f61863c78bcbf9f2e6": "10a74e6ff07ccb1735736b4cb3afc0a42ac707d111508ac71c24511f875a4648"
      },
      "depends_on": [
        "mc-62beb53d71b97bf090ffbd2f",
        "mc-67d438cf55759feb8f8b68a8",
        "mc-79720aded9a054c2c531be18",
        "mc-82b94c492ffa21b4e82a3f04",
        "mc-c87676f61863c78bcbf9f2e6"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清 rtx 5090 上原生块缩放对软件换算的受控测量: 预测、结果与解释。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-378dffdf971fa311ae0ebbf2",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已依据更新后的子卡 17、18、42、43、44 复核：比值、发射与等数据的估算、复用次数和 0.33 ms 余项都仍由子卡支撑；“指令数估算没有 profiler 证实”与 43 的证据边界一致；只在问题里补了版本。"
      },
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2733e495067bd63784e2ad1832659ed392d1ee68cc7bec27dd5186ebc7514b46",
      "content_summary": "MI300X 的 FP8 是 FNUZ：同位值减半、0x80 为 NaN；vLLM 置 0、重新解读、scale 乘 2",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "commit": "8530aed2b78a19eb00e242031c22bb78d615eea2",
          "kind": "snapshot",
          "product": "vllm"
        },
        "recall_target": "mi300x 原生 fp8 是 fnuz 变体时, 为什么不能直接复用 ocp e4m3 权重的位模式, 要怎样转换?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c55a9823b372c95442dc2db8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3fbb7a91b3eab3e1eb7abbacd95fcb7f62cf79cd3912e4ea89ff61d5d54d85a2",
      "content_summary": "TMA 描述符靠形状和步长表达连续：首尾相接的维度自己合并；swizzle 限制最内维",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "想让 tma 把首尾相接的几行当成一段连续数据时, 描述符里怎样表达, 有什么限制?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-546505f89a561f1a96c83248",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e4689759e8f033a4cb208a6c9b2a71076d6d9e0c8d87d02c72d0ad778a1a7b07",
      "content_summary": "软件换算靠 E8M0 移位进 bf16 指数、缩放 MFMA 只认 E8M0，NVFP4 在 Triton 3.7.1 只有 Blackwell 编得过",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton 3.7.1 中 nvfp4 的 tl.dot_scaled 为什么在 rtx 4090 和 mi355x 上都编不过, 这对格式选择意味着什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-390d11525fd439f45c189931",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "015321c3e88e3d48f3f1b0cbd60bfbdd2ab6eb572d0fdb92fbfebff30caec43a",
  "manifest_payload_sha256": "c7b4191c2f8befc440117ac19be0e4bed746e12ad842f48f4bca87925bb790ff",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 30975,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-10-block-scaled-matmul-correction.xlsx",
      "row_count": 16,
      "rows": [
        {
          "content_sha256": "7acdbf3e3622c530d3e86ccc8ff177818ea022edaae2aa593cae4bf07dbf803e",
          "logical_id": "mc-1b27b1ffae129f2ba42ee08d",
          "row_sha256": "331901f9816cda70639ca738ffe360a36e845db48500511ab7fb74feec74dbbd"
        },
        {
          "content_sha256": "e296bc184d75bdd2d1adea21484221101e3990afc6a3666773e63de9045b88ae",
          "logical_id": "mc-bd3becea988ba214a166dfb5",
          "row_sha256": "3a49ec8bd69ab9a2660f0ed6a8fe31d263a1c0d8452a5f20b7f989b9b279d25d"
        },
        {
          "content_sha256": "cf4134fb2ec766acc597a2299776777af8bc091932772b743e388e3e4307afba",
          "logical_id": "mc-22af7057aad390b599c70b08",
          "row_sha256": "2f4534a614c0c24477f4a091f0ebd1f2ed0f6c31d9e5e4dbde956c5465b3552e"
        },
        {
          "content_sha256": "d2e0d0ef34cfe3b11a72b3b197563d4c1785a1eb1151b8d87fc65b5d2d45594a",
          "logical_id": "mc-c4e84caf7808f58085e182fa",
          "row_sha256": "72436009154930243e9adba314e28158c72bc5e9e9b40a0d746f690900cac8fe"
        },
        {
          "content_sha256": "37f262ddfdb5265463a44759d02fa4643e7e5874e15914fbcddb1c202312d5e6",
          "logical_id": "mc-af0e33b93ba22e83c454dd0f",
          "row_sha256": "13186f59b47ef24947b124f9e3b9010cd8e771e98f3e21bd6e9da19073abbd19"
        },
        {
          "content_sha256": "ff86c896e0c75e6bbfc42f6ce12fc0d8d22aa8c0302bd2fdb48a31f3684817c3",
          "logical_id": "mc-6b8a6ac1e7ef6441eb8a60e1",
          "row_sha256": "15de080627a3cc848e87f9ad546f9f5e52dcfcf7010eba5baa5c8688bbb56031"
        },
        {
          "content_sha256": "699cb403877bdc119a56a85b8c75aefa60c7f81aef71645f66020745140bdc72",
          "logical_id": "mc-63cae5cd70cc11611b5399eb",
          "row_sha256": "106853c0df00b5581144a781412554dc8684dffdafc72c091d26af51094bf6b2"
        },
        {
          "content_sha256": "653f53412d5e0a3f06103e4224ce62d2fbd0fb5f10ef9981b92b91f9d8b00b72",
          "logical_id": "mc-e04e352a1f9e05fd644b3a02",
          "row_sha256": "f786a067c6433d07a9a995d7659027879708f9e67da8199a2ee48c661b23d26a"
        },
        {
          "content_sha256": "d183e243dac9a8ec13b63d346e423e60cd7c667724c01857001b54d595a467ef",
          "logical_id": "mc-e2fba85bcd99b38a89b3f5f8",
          "row_sha256": "9a474f3adbf69d691f18d8c6b8d7125dfb38453517d3f08b13dbdf3a94f6df75"
        },
        {
          "content_sha256": "e9b4e7d11c902752904fd33b8fb61e63199b47c38aa990206ed07caa886ab195",
          "logical_id": "mc-c9bcfe52ab839d10dad93cd1",
          "row_sha256": "59f6a85c25fca0ad03509663cf74177af220b07538ba8cf71137e0101ebdfa8d"
        },
        {
          "content_sha256": "871075c898af5d02b36a49177fac3d12e93e54f10d80b8125be2af3940695dc9",
          "logical_id": "mc-79720aded9a054c2c531be18",
          "row_sha256": "921af73cdf71dac23004687534f049cdf01a1a49a226627e6ac86279621da556"
        },
        {
          "content_sha256": "4f0133cb16c9cdf5f5ffb7720281fe473d4086448f9bb6de374c9bd82832ee3f",
          "logical_id": "mc-67d438cf55759feb8f8b68a8",
          "row_sha256": "6d37ef35cbb7a28e96f014142125cb7ed799ebd07489bee6360cb522c9324821"
        },
        {
          "content_sha256": "024730bdf0ce48f4f33e2429fe150079114416d1d1ac8682346d96f28fe758db",
          "logical_id": "mc-62beb53d71b97bf090ffbd2f",
          "row_sha256": "0e95b8e2ddbc23017ef5a11f10be4838fde9ba56cb9c7ed675b56707eede47c4"
        },
        {
          "content_sha256": "f08dcb8978f87f2af56f60209e2e8c75d5939da499c51057fd151cd58f1941dc",
          "logical_id": "mc-e6288e8d97ab5cfd9dc26f15",
          "row_sha256": "a1679e3641f90ec5a7eae00231792be6e818d4a9536a0a12304c9e104c36f998"
        },
        {
          "content_sha256": "9349971fc93b083a4362a65e119529d8201b7c9180264c794e048584f9c4cc9e",
          "logical_id": "mc-aff6698aa51d74780aa2bff5",
          "row_sha256": "82fd3153c4ec6e1988528b2c967833934f92beed9ae4c35cd073777387b83db8"
        },
        {
          "content_sha256": "6eb520096680d3829e74d704ad86e5ed142f549773b2026c0009a9d8ea42ae77",
          "logical_id": "mc-c5458d9bf53e30e69cdf8922",
          "row_sha256": "3853ac7377112a3ec31b57ccae66168dc79895fb771f8bc99a382793c7a4f451"
        }
      ],
      "sha256": "9a1130697b01e1ce9194cd7c02fc2dd187c2e3c5c0a223f4be24ba19e8493d5c",
      "sheet_name": "cards",
      "table_sha256": "5166276c98780bf25822b78e28c4d99cd482fb3b9e0a30451f4a65bc1d4d737d",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 55194,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-10-block-scaled-matmul-technical-qa.xlsx",
      "row_count": 31,
      "rows": [
        {
          "content_sha256": "67fac8defcfebef76940a86226d7d4d593093848b289c623f5e366b24ce60411",
          "logical_id": "mc-c6ff59ea5ef045fc55f6a23f",
          "row_sha256": "fdc2d13af02ae35285cec1647be892fb4b8d96804c32e7018d9d6e1694ba742c"
        },
        {
          "content_sha256": "77d4848c5ff60c4955257562af9c62f61fe6abf73c82ea88cac973baded10941",
          "logical_id": "mc-f976aa38b9879032b0c34640",
          "row_sha256": "e71a0bb4c7b7d61380fb73ff8fedf303e05502123b20c06dda94ef12b95e925a"
        },
        {
          "content_sha256": "8a84d64b78a91da06c62043076285413652ee3e6614a9380688f77fc020e8af4",
          "logical_id": "mc-d0cadfeaa8b31d4fdf194f4d",
          "row_sha256": "3aca1c8dd6c7baa5b2a6db1bda2a7cac0f8b5ad295eafd7be42a6582d1b1551c"
        },
        {
          "content_sha256": "27ccc4cd983a197bc58eebfc39cab098c4974028457245930412f3b304061345",
          "logical_id": "mc-1b6b6bf5b5cae30680cd15b3",
          "row_sha256": "a6bf2ba3f3a306f2f177d7590c3f3aebb503ee81d7e26c09e82c3b55397f0d32"
        },
        {
          "content_sha256": "4695cb40c657e53c8b64474a5c660590a187a9f36807a82f1d68bc32de0b8d3b",
          "logical_id": "mc-26b2bd02cc7fc3baad3d7816",
          "row_sha256": "5684cb94c561377d4276033b307fbeb1a049cac09ee7f01964349c1965f83ec4"
        },
        {
          "content_sha256": "fa71174624dedb7b89ce4b1d5ecef80a366f5684221ae2c2b0b06e6c0e5e7bd0",
          "logical_id": "mc-e236c2fffc4d370ff9caf8a7",
          "row_sha256": "4c1fcce6a658760c4e49781606fbde05529bd30e0651c283e05599529d4f64b1"
        },
        {
          "content_sha256": "c31a39752a280c5af11ab15a0b8ae321649144da9fe9ad6913053bf4d98be279",
          "logical_id": "mc-385020ed4fdd34484e631abf",
          "row_sha256": "0e6aaa091344871ffaf48ce3fd3f77bbe637002b9657c84e6e4fd8fd30222981"
        },
        {
          "content_sha256": "dfa884434bb15e74272c6dcf0d37b73ef501fe5665682e9e29a36e839d57882a",
          "logical_id": "mc-0be1cfb5e7e0f6f93e2c2381",
          "row_sha256": "39d229d4bd0d680961fc5a0d76df09d8dad3cd7572478f26c699ec27b8072b5b"
        },
        {
          "content_sha256": "8d9b52bf220ec98a591658dc1b390cff5a5aa8a05707bd78f183462e4c359256",
          "logical_id": "mc-5a62d0166df698913c98a27d",
          "row_sha256": "4548f00459049f7a1110e7548f053b7e10dca3445b41b46aa93049c23c9daa6d"
        },
        {
          "content_sha256": "489e8bad9dc91bbf86611c5da25a0a081c9643478f2704a2f96d709839612c40",
          "logical_id": "mc-dfa47e6149b7d295651f617c",
          "row_sha256": "c4bfe8f0bae37c616438bac8a0b62c3502645c194a9f76e51a88c918b39c3c62"
        },
        {
          "content_sha256": "e54a5c1c51a95f1192711ffbeacf6cd6fa0dd0ae15daa519cff36e98c86f3b9a",
          "logical_id": "mc-fb0c625aeade1143e630eb7b",
          "row_sha256": "52947c67a1e5fd182be26873205ef448ab0a84e441ff8e90e64d02c011fe778d"
        },
        {
          "content_sha256": "23fccd3f68e209681f61b053c1e479a800600219cf844faa191a3236fea81183",
          "logical_id": "mc-30df6d9a5c0fd8e684af2f17",
          "row_sha256": "63458c14cc1af6fa30007e505c5c0e556693c902c8cfbe984ed38aff746e5a5a"
        },
        {
          "content_sha256": "58554aa9677a121a83c23ced304c6e658fa077a222a3237ba7777f30429ba842",
          "logical_id": "mc-281380095aabd19ad91c51d6",
          "row_sha256": "88f6b0e28cf6d3f4599c6ba7098741fdb82e695fccc4863fce0193a70e085bba"
        },
        {
          "content_sha256": "79ab2459a7162eb7f525e5b3d1083526b4fe0ad0489be53bf8b9b83aa70520a0",
          "logical_id": "mc-455b749f88ebfaba60062e8d",
          "row_sha256": "2023815dc3bcd633258eb65b1b40bd320c3dd50c109e1dfbf7c1674fe45457b0"
        },
        {
          "content_sha256": "6a9c850c84d5fc3f8d067ed94cd87e47d1ce4921c457094e426eeace587cfe0f",
          "logical_id": "mc-be5feb89a08576b9a714cf5b",
          "row_sha256": "be1fa9fbcb7330b4661cdefb3bb48836d1545ec04b22e7f18dbd4ace9b8fae7f"
        },
        {
          "content_sha256": "7d28c6750b9ce83c1f4fa62929e7cd208027a677a7a0faa1acaf9dbaf9b80756",
          "logical_id": "mc-23c1c68e40760d05b71a8647",
          "row_sha256": "ef134a7c027201f7c721b63c94c914c38d4dd8fb93e7ce4dc7c2cf2e1cd64de2"
        },
        {
          "content_sha256": "4e39e9a979a73098aba1f4c86f3141013c81dc6a264d981233fd0a067b97fbcc",
          "logical_id": "mc-82b94c492ffa21b4e82a3f04",
          "row_sha256": "612a52bee53ea8948ba60362a24151d4080e5c80a31bd592d0dc0a848fe17bf3"
        },
        {
          "content_sha256": "10a74e6ff07ccb1735736b4cb3afc0a42ac707d111508ac71c24511f875a4648",
          "logical_id": "mc-c87676f61863c78bcbf9f2e6",
          "row_sha256": "59325cfbedaa3d3c280d833b00b611d0aa1fc6791a4acc83aafa78248bfb25d8"
        },
        {
          "content_sha256": "255bc30bde5a2a8e36bd78f419434df0c457cd4e6f6ae7f37d1cee72daa5d7ca",
          "logical_id": "mc-82357876d3d94994eda54ed6",
          "row_sha256": "5319df47a4e36ae2d2a157e282f2e1d5e90c9c09388628126de80186fe920dc9"
        },
        {
          "content_sha256": "eccc0ea148135178f9a7af5a872b39cd623b78cfed98447d40aa18553b3f95cd",
          "logical_id": "mc-034e387fadad8ebbc0e6a813",
          "row_sha256": "ebf3ab3452bdddcf24a7af09d8d568ec4749a1c88160395998e770f8b0300c74"
        },
        {
          "content_sha256": "d490c197a9aaddbd0b097208f6155739ebe5b63c613727449ef1d8006f02f720",
          "logical_id": "mc-5516e8dc029539f4cd2a7d20",
          "row_sha256": "8aa7c156ccbc192bb8fe4fc408f79371909975539bb73e05dcc9202822679250"
        },
        {
          "content_sha256": "f1311176e7d0b3001e5f8d3451507c9dab471a313406c6042a519bf0c17ff831",
          "logical_id": "mc-baa834639ffae733c9e8be5d",
          "row_sha256": "bc4a99efc74c8e9533d754b06ff73736682f7aab71570ba41a8356ced3fbfc79"
        },
        {
          "content_sha256": "f8f144cb1c42b41c682395daeeefa650ed97318962efb2b77bf4e4d7cc98ea82",
          "logical_id": "mc-36e11025799d6f84e627893b",
          "row_sha256": "bfab2b3ddf52fe5e7af43c0dd4bfe8cedd385b1be13ac04ef78201dfe5d51c4d"
        },
        {
          "content_sha256": "e926a60cff12385f62a841b53d7fe7d3680496c2a59acb014352100b0c9de05c",
          "logical_id": "mc-cf106f94c307b097e01f50c5",
          "row_sha256": "5e45a05a734b9a6301a2826f6a978d053f01e4e43b75b91d9f6dffff8db5b317"
        },
        {
          "content_sha256": "9f4a978f5a9c23c4bb3b006d52c7fe25340d7e3253be76202747c4f508858cc6",
          "logical_id": "mc-32cb7a3958719df772201f26",
          "row_sha256": "3bc4119f3040f6adccd24e2783baab6572ff12b579c1e567a086ed8c1b2f393c"
        },
        {
          "content_sha256": "8aac8d8a023646bbda0d69eb7b40a6eb8ed92c17517ea82e7570f45d7f182b43",
          "logical_id": "mc-f5fd3b25c2b1051f48aa2bc0",
          "row_sha256": "18ed755b986316a26859e52a0bdd547f4007465533dbd722586ab4bc62b8c2d5"
        },
        {
          "content_sha256": "bf5793840921b5f7974de23532e06036d6afd021e37b04f45819939a5ad64a7b",
          "logical_id": "mc-401590969bcaa1ef6ff794b7",
          "row_sha256": "8464e0d6ff3354bf9e4a721587d8bcb0ffff15be8a92ba329603243e8321a0eb"
        },
        {
          "content_sha256": "18bef0895bff69b7f3272b5ca7a6404d4e11a48e106331803e1c869591759723",
          "logical_id": "mc-739b495a4d363d6539380874",
          "row_sha256": "fe88342bfaee3c54c146eb8cbfe3215d0bc8b5589b477ff76823fb63056767af"
        },
        {
          "content_sha256": "2733e495067bd63784e2ad1832659ed392d1ee68cc7bec27dd5186ebc7514b46",
          "logical_id": "mc-c55a9823b372c95442dc2db8",
          "row_sha256": "e39ec81af5b2f24ac2694502a14d0d6a0180ce0657ea4cc569d4ca253b93f6ad"
        },
        {
          "content_sha256": "3fbb7a91b3eab3e1eb7abbacd95fcb7f62cf79cd3912e4ea89ff61d5d54d85a2",
          "logical_id": "mc-546505f89a561f1a96c83248",
          "row_sha256": "a87475c300002090bcc08f83c7d890a1e62e91148b0162f914910dac520fc28e"
        },
        {
          "content_sha256": "e4689759e8f033a4cb208a6c9b2a71076d6d9e0c8d87d02c72d0ad778a1a7b07",
          "logical_id": "mc-390d11525fd439f45c189931",
          "row_sha256": "11476d029161895fab279cc7c50429af7d177a9d2e448b9da948c23a90da6e64"
        }
      ],
      "sha256": "aabe123820dd6252c3184e1603b64150a631961e569c670cdbdef95b6f39b429",
      "sheet_name": "cards",
      "table_sha256": "35b6162a0d2068f54066c2d43e7ec2324d8536813446e8f22d7962584c2a0597",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 10053,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-10-block-scaled-matmul-oral.xlsx",
      "row_count": 4,
      "rows": [
        {
          "content_sha256": "b35370dbc8afc5bfb4168ad5e4f2269e459fab8e367b53f260e915dc086372df",
          "logical_id": "mc-b454b74ff5412e8cdecb6903",
          "row_sha256": "dc876ec3f4bb73c55447c677c751dceb3f4536bbc67d6029483297ca61acc2fa"
        },
        {
          "content_sha256": "030256112b852926af7fe5f8b6e2d4f1d2251c5087bfbfc810465d11973f5406",
          "logical_id": "mc-d1dda4cc075c9bc27a784223",
          "row_sha256": "c4611d3353db45089c392198d0b8ac4da518fa7eb3a317087880aaa43d4101e1"
        },
        {
          "content_sha256": "98a0888dba45f3c8478da8df8df2979b01a70d938108f01b29250857d068c226",
          "logical_id": "mc-3d3e052793ab6f4d8ea66293",
          "row_sha256": "24d9cc2cb3c4b5b2751a6c15679f4f84072adc0dedd33e6ff237ff3cde44d3be"
        },
        {
          "content_sha256": "d63b8369a7758503ce339cb8b577733baa4ef13b757506433423bc2b9e9133af",
          "logical_id": "mc-378dffdf971fa311ae0ebbf2",
          "row_sha256": "029e5d8de42ddb6306f5382ea981c7fd860bcd436d43d6baabb434aa277e1a20"
        }
      ],
      "sha256": "b3b213956385964629697dc55cd95e95fcab5bbd1c403c3ae021a8680e1d5a3e",
      "sheet_name": "cards",
      "table_sha256": "3135c5ed4576208e086f0e4cf754509f4678b83af17378d3c3d73560aa48331d",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "0978be2420e385741d8f901733ac609323b738c5b530c16b5f00a6eec3f28efb",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "block-scaled-matmul-log",
      "path": "docs/triton-learning/logs/2026-10-20-block-scaled-matmul.md",
      "sha256": "5cd7d2d14a150a4fbb22aaf87f201e1e6cc15d921f5f453e066aa96aaede6f9e",
      "summary": "10/14–10/20：浮点与块缩放格式、scale 乘在哪一步与预排、五种硬件落地、MI300X 取舍、练习与 M1 测量的纠错与答疑"
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

导入文件：[triton-lesson-10-block-scaled-matmul-correction.xlsx](triton-lesson-10-block-scaled-matmul-correction.xlsx)（16 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-10-block-scaled-matmul-technical-qa.xlsx](triton-lesson-10-block-scaled-matmul-technical-qa.xlsx)（31 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-10-block-scaled-matmul-oral.xlsx](triton-lesson-10-block-scaled-matmul-oral.xlsx)（4 张卡）
