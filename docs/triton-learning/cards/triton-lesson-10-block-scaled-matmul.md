---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "35a7620188978cec372199be913ebf621a6375ca41238fb0d0a9b6844086bce5",
  "candidate_sha256": "76d419c94ff40253abe01478cd7150c09f0d37025f32dce75ba4fea6e83b72eb",
  "cards": [
    {
      "content_sha256": "ce33c5292f052b3be13f5adc81952e4c1198d06c12fd169f3dfc710e7c76fc11",
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
      "content_sha256": "d8e7aff5b24ae8a733e575d3835c434c465ec6eac4ef7e795846f92f654fac70",
      "content_summary": "MXFP4 与 NVFP4 的块大小、scale 类型、位数、对齐 6 的能力与代价",
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
      "content_sha256": "ffa27069691e0796665d0a53a1a55bf78d3baaf2e845e8dc39d661a50b7caf76",
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
      "content_sha256": "5118e552c2ebdcf077224f43f04bb1c42bdf64bf350b5b76c6141cf575106759",
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
      "content_sha256": "867f4cd927a698aa588099b53a775cae7bc57be595a47a2fc1e91069f21ceee9",
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
      "content_sha256": "714c83ede40e424991a6c519f5957b6acaf67e366136901400f2258e90565c19",
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
      "content_sha256": "30ff4b583caf83cb29994761a9626026783de5b9c2c71d2efdb9d8a01fb477a2",
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
      "content_sha256": "a53e7ad77d6de99834281ee9ce19ee1af3c993cfb319922a4bbb38f780c7946e",
      "content_summary": "无块缩放指令时把 scale 放到部分和上需 V ≥ 指令 K；代价与 DeepGEMM 的 128 分组",
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
      "content_sha256": "79e569454836dc9619d1fa119df6b86d6e4680ce42eedd51c69fe5da4c34504b",
      "content_summary": "5D 预排让字节顺序等于 TMEM 顺序；tcgen05.cp 原样拷；第 220 行只是视图",
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
      "content_sha256": "676b003180768f78f5b0597b60b9a9157d1e86467e3f2622fed1b6f205aad9ae",
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
      "content_sha256": "303b7a5d2bf7e60b4cf16a865275248e25c242a4fb2f4fa80e843b14c19dc897",
      "content_summary": "五种目标上的落地：原生、软件换算、编译失败，scale 的位置与限制",
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
      "content_sha256": "937c7b19650e2ff83f6641c88115a6b896d4bd57adcc3f66fa450b19b3ce3c16",
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
      "content_sha256": "a46baec908042f52c153e1ee35093cb8d66243f2c39d316004e00488e67c6804",
      "content_summary": "MI300X 上 bf16 对 MXFP4 权重：解码受访存、预填充受计算，容量是始终保留的好处",
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
      "content_sha256": "f4070cdcf6bfb860ebfa1e8a2fec20af7f98fbe6d2ee8547d1429adfb5fe1273",
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
      "content_sha256": "4fda5e015ec1e0cfa3c97778be5a8a55bfefe94f46e22d81581a99c63ef1edbe",
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
      "content_sha256": "f51876e32bf00e1b74fdde89e0e31c24fe796eb774995581fb0ee765c0fd8b2e",
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
      "content_sha256": "a18858677f44074aa56c4f995817b54a402fee87975a8f08988065892c9df54b",
      "content_summary": "总时间介于 max 与 sum 之间；warp 少、驻留少时靠近相加",
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
      "content_sha256": "1b031cbfdbed1360fd916d851980ac4a43fb38e630fbc27b57ae319b09907f7d",
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
      "content_sha256": "a7e74733ef959865dd4622b360ccacfe8648a75c9286c703f16f4a3e9640988a",
      "content_summary": "两种位置乘 scale 次数之比的含义；V 大于约 85 时部分和更省",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "比较“乘在部分和上”与“乘在元素上”的乘 scale 次数, 比值 bm·bn/(v·(bm+bn)) 的含义是什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-39eb3cefd390d467f780353e",
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
      "content_sha256": "996da066c0c32fd06d61c90affa41a38bbcc95f20d69ba37b4484fe804529b5e",
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
      "content_sha256": "89b2f8c5736936c5419091f13e480837a9641839179a0f610c999c731956fcad",
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
      "content_sha256": "0121c4fbb352e0dae43366626ef3c3755fb48da22283b9e9b1530e04a197b5a1",
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
      "content_sha256": "ce63446bc17ae4b5822ae988ea3329bf551ee571ff8affa39684c3bc05d88e97",
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
      "content_sha256": "59dd853717fd026d8c2b0c7b60082c5f2019fb79f642ca1b513cfdac5a1f91ac",
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
      "content_sha256": "92ba9c40f4bacd0796048d97fc00c620aabcc6f63894bd8dda81b9faf91c8c76",
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
      "content_sha256": "e9cebefe830ad4b076a6b800fd3fef4fee96cf2df08b0b9e0d309c06c7f5aa59",
      "content_summary": "Triton 用 prmt 查表把 8 个 FP4 转成 bf16，约 2.1 条/元素",
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
        "recall_target": "triton 在 nvidia 上怎样把 fp4 解码成 bf16, 每个元素约几条指令?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-40f72bc8635f39f0bf7723b3",
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
      "content_sha256": "1cecfc0f59d2f5795b10f2eca2a775d84edfa2de6a2d84acd91d41626db62898",
      "content_summary": "W4A16 在 M=16 只快约 7%：B 的解码才是大头",
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
        "recall_target": "m = 16 时把 a 改存 bf16(w4a16)能让软件换算快多少, 为什么不多?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9c2d0dd6f8e7310510b51d0a",
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
      "content_sha256": "d42b157e5707e59f1a7d9c8c44693d425829870228e4eb4aaf1f7efd62c3ef37",
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
      "content_sha256": "5913e6c461a52a239215169a8d9c328bd9693ba82631588c2a3681667140c7ec",
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
      "content_sha256": "af419afe98b728ea7a835761d97fa926bff707c6cd0a8621bbec15ae41b4495f",
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
      "content_sha256": "b6e3b2421995c107237fee95a93ce0ae4a673f15457776fa725e0673a0cf7665",
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
      "content_sha256": "e337b1e2017a38ccb4445b57d4b55585dd0dfc30d123153687d13daf9e7a8f51",
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
      "content_sha256": "0108f046502de087050a45b6dbb0e509edf9955b6c26462ca3bc98a8344af7d3",
      "content_summary": "强度与平衡点同单位：乘加 123，FLOP 247",
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
      "content_sha256": "9f75a73f094dc41307349ce2a4f8c3f50990c1da1154042541db12d9cd097f4e",
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
      "content_sha256": "146b63807c5b487fbb09cbabe8e53440ac0ce7cecde35e98f438c24a75c92154",
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
      "content_sha256": "4f44813d33237291d435ab80273c6df9e63d70242be55be29bf0acf2654e91ab",
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
      "content_sha256": "bc0b9ba3fb886277448881cba49e976c7ab8efc3a09f22b6517e50009a902867",
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
      "content_sha256": "609c87ead15a8cbf2d0bde0c7107446d86fd53cd0e6cafab428312ccbe5685d4",
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
      "content_sha256": "8c2f69850070d9ec902be5179075fa23567c3bdb5111d904f978a5dfa8aeb4f4",
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
      "content_sha256": "931c0f7b149f5f5c88bd6eb006b5d4a0316eaf7bb276fa9768e2c1166473c75a",
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
      "content_sha256": "2224b641cdd0c02c01cef82dde227ffd786d6805ec5836f96d220611065cd13d",
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
      "content_sha256": "502dae92cc5cc30d7f38663af935b58b42dcb34f89dfe2a1185cd78f50f75811",
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
      "content_sha256": "c8abf6c2794a489fbf1fe3de92a3d6aeec1def6ccf86c52e7ac149f118c6bde1",
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
      "content_sha256": "29ce303c06d05a79ff8400b05c3213a23751e994ca9ddf949436c3123badf682",
      "content_summary": "乘 −sign 会把正数变成 −0；用 where 选 ±1",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-block-scaled-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "整张量反量化时用 x *= -sign 取符号为什么会出错?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1d75315b1d98e6198d11bea5",
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
      "content_sha256": "81ce6a29d3885da3ba8da9f6a03111dc9941231c6c65556e2003a53f6ea7c5b9",
      "content_summary": "口述块缩放格式的必要性、E2M1、MX 与 NVFP4 的取舍、scale 的取法",
      "dependency_content_sha256": {
        "mc-1b27b1ffae129f2ba42ee08d": "d42b157e5707e59f1a7d9c8c44693d425829870228e4eb4aaf1f7efd62c3ef37",
        "mc-26b2bd02cc7fc3baad3d7816": "867f4cd927a698aa588099b53a775cae7bc57be595a47a2fc1e91069f21ceee9",
        "mc-c6ff59ea5ef045fc55f6a23f": "ce33c5292f052b3be13f5adc81952e4c1198d06c12fd169f3dfc710e7c76fc11",
        "mc-d0cadfeaa8b31d4fdf194f4d": "ffa27069691e0796665d0a53a1a55bf78d3baaf2e845e8dc39d661a50b7caf76",
        "mc-f976aa38b9879032b0c34640": "d8e7aff5b24ae8a733e575d3835c434c465ec6eac4ef7e795846f92f654fac70"
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
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2dcb14cbb54462a6942e9f1d8f91e14289faae62eef319c743c3d80029497241",
      "content_summary": "口述 B200 上块缩放的 scale 位置、预排与路径，以及换卡后的落地",
      "dependency_content_sha256": {
        "mc-30df6d9a5c0fd8e684af2f17": "937c7b19650e2ff83f6641c88115a6b896d4bd57adcc3f66fa450b19b3ce3c16",
        "mc-5a62d0166df698913c98a27d": "79e569454836dc9619d1fa119df6b86d6e4680ce42eedd51c69fe5da4c34504b",
        "mc-e236c2fffc4d370ff9caf8a7": "714c83ede40e424991a6c519f5957b6acaf67e366136901400f2258e90565c19",
        "mc-fb0c625aeade1143e630eb7b": "303b7a5d2bf7e60b4cf16a865275248e25c242a4fb2f4fa80e843b14c19dc897"
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
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8430db281ea1cc6b2f18b85d7ac1466c20c10060ccdb7bff2a05b0ebdb940956",
      "content_summary": "口述 MI300X 上 MXFP4 权重的快慢判断与部署选择",
      "dependency_content_sha256": {
        "mc-281380095aabd19ad91c51d6": "a46baec908042f52c153e1ee35093cb8d66243f2c39d316004e00488e67c6804",
        "mc-455b749f88ebfaba60062e8d": "f4070cdcf6bfb860ebfa1e8a2fec20af7f98fbe6d2ee8547d1429adfb5fe1273",
        "mc-63cae5cd70cc11611b5399eb": "9f75a73f094dc41307349ce2a4f8c3f50990c1da1154042541db12d9cd097f4e",
        "mc-af0e33b93ba22e83c454dd0f": "e337b1e2017a38ccb4445b57d4b55585dd0dfc30d123153687d13daf9e7a8f51"
      },
      "depends_on": [
        "mc-281380095aabd19ad91c51d6",
        "mc-455b749f88ebfaba60062e8d",
        "mc-63cae5cd70cc11611b5399eb",
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
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "356c9c055c9be63604e3aa16c65a75214d36ea640867e7400b7ad4bebbbb136e",
      "content_summary": "口述 RTX 5090 上原生对软件换算的测量、解释与预测错误",
      "dependency_content_sha256": {
        "mc-62beb53d71b97bf090ffbd2f": "931c0f7b149f5f5c88bd6eb006b5d4a0316eaf7bb276fa9768e2c1166473c75a",
        "mc-67d438cf55759feb8f8b68a8": "8c2f69850070d9ec902be5179075fa23567c3bdb5111d904f978a5dfa8aeb4f4",
        "mc-79720aded9a054c2c531be18": "609c87ead15a8cbf2d0bde0c7107446d86fd53cd0e6cafab428312ccbe5685d4",
        "mc-82b94c492ffa21b4e82a3f04": "4e39e9a979a73098aba1f4c86f3141013c81dc6a264d981233fd0a067b97fbcc",
        "mc-c87676f61863c78bcbf9f2e6": "a18858677f44074aa56c4f995817b54a402fee87975a8f08988065892c9df54b"
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
      "source_ids": [
        "block-scaled-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "69826090fa5ce8537c921c84d1b3e66bb448873817b611d1ab5f0d6565bd0d48",
  "manifest_payload_sha256": "004c50d7f8d2d22dbf19e2a9d016c56b32d91978cc0e699ca8a66fdceec8675f",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 30840,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-10-block-scaled-matmul-correction.xlsx",
      "row_count": 17,
      "rows": [
        {
          "content_sha256": "d42b157e5707e59f1a7d9c8c44693d425829870228e4eb4aaf1f7efd62c3ef37",
          "logical_id": "mc-1b27b1ffae129f2ba42ee08d",
          "row_sha256": "7de4d4397ea1be88d9a9d4ab8eb9615a980c551cfeef5933d062ef73c6c98e4e"
        },
        {
          "content_sha256": "5913e6c461a52a239215169a8d9c328bd9693ba82631588c2a3681667140c7ec",
          "logical_id": "mc-bd3becea988ba214a166dfb5",
          "row_sha256": "ed18139b5bb3bc469ef53f5fc060e12dc0b9ee66299d6e5372c4edb78191563c"
        },
        {
          "content_sha256": "af419afe98b728ea7a835761d97fa926bff707c6cd0a8621bbec15ae41b4495f",
          "logical_id": "mc-22af7057aad390b599c70b08",
          "row_sha256": "c5836b53e610b0f13dfc329e71be25f4dcf6ca088d123563ca00b7e7bcda4de4"
        },
        {
          "content_sha256": "b6e3b2421995c107237fee95a93ce0ae4a673f15457776fa725e0673a0cf7665",
          "logical_id": "mc-c4e84caf7808f58085e182fa",
          "row_sha256": "11815add4c63fc183dc710f4f6e15ce4949922e16e8da622af4f9ccfc7e891d7"
        },
        {
          "content_sha256": "e337b1e2017a38ccb4445b57d4b55585dd0dfc30d123153687d13daf9e7a8f51",
          "logical_id": "mc-af0e33b93ba22e83c454dd0f",
          "row_sha256": "35e47a8d21f4c74d6f28d07dacc15fb933dabfc9b9e6bffe9adaf9b257074b0f"
        },
        {
          "content_sha256": "0108f046502de087050a45b6dbb0e509edf9955b6c26462ca3bc98a8344af7d3",
          "logical_id": "mc-6b8a6ac1e7ef6441eb8a60e1",
          "row_sha256": "c6920ef29f88c259d33ea9944e6ba9ddb25388c8bdd57734e42b721d5ae116dd"
        },
        {
          "content_sha256": "9f75a73f094dc41307349ce2a4f8c3f50990c1da1154042541db12d9cd097f4e",
          "logical_id": "mc-63cae5cd70cc11611b5399eb",
          "row_sha256": "043232bec9182208d7f331b84cd6e3299a9a04056aa6f8a8487c464c376f44cc"
        },
        {
          "content_sha256": "146b63807c5b487fbb09cbabe8e53440ac0ce7cecde35e98f438c24a75c92154",
          "logical_id": "mc-e04e352a1f9e05fd644b3a02",
          "row_sha256": "de56116787bd021f6dc6c91a5bc178caf4b291cd771f70a233707bc3369686be"
        },
        {
          "content_sha256": "4f44813d33237291d435ab80273c6df9e63d70242be55be29bf0acf2654e91ab",
          "logical_id": "mc-e2fba85bcd99b38a89b3f5f8",
          "row_sha256": "1cd869b34f40a88b968b7ccb527f3bb40703c09b0a2624e90bcfa557f3264c9b"
        },
        {
          "content_sha256": "bc0b9ba3fb886277448881cba49e976c7ab8efc3a09f22b6517e50009a902867",
          "logical_id": "mc-c9bcfe52ab839d10dad93cd1",
          "row_sha256": "aed6503a820dea2686cf93eb25c7be0d5ef71d35e98564774a4df695c1cb2eb9"
        },
        {
          "content_sha256": "609c87ead15a8cbf2d0bde0c7107446d86fd53cd0e6cafab428312ccbe5685d4",
          "logical_id": "mc-79720aded9a054c2c531be18",
          "row_sha256": "d5368aee152e982c9cf2aa772530ed29a012a1aa281e6bdb7ff5b4365fba3a10"
        },
        {
          "content_sha256": "8c2f69850070d9ec902be5179075fa23567c3bdb5111d904f978a5dfa8aeb4f4",
          "logical_id": "mc-67d438cf55759feb8f8b68a8",
          "row_sha256": "8b03e09fad90119ba7e2a90de57b896eb8d6e554eca142e8f53d031680b13d7f"
        },
        {
          "content_sha256": "931c0f7b149f5f5c88bd6eb006b5d4a0316eaf7bb276fa9768e2c1166473c75a",
          "logical_id": "mc-62beb53d71b97bf090ffbd2f",
          "row_sha256": "1c3431ff11d54246f62e6e06d7d4d8b7df9227f8c16c30d68c4a38762a143b2f"
        },
        {
          "content_sha256": "2224b641cdd0c02c01cef82dde227ffd786d6805ec5836f96d220611065cd13d",
          "logical_id": "mc-e6288e8d97ab5cfd9dc26f15",
          "row_sha256": "3024c77a3e6381010d5ead9104f5cecb844bac4a1240465a440cd087111c196d"
        },
        {
          "content_sha256": "502dae92cc5cc30d7f38663af935b58b42dcb34f89dfe2a1185cd78f50f75811",
          "logical_id": "mc-aff6698aa51d74780aa2bff5",
          "row_sha256": "e823506a5305e24e74b5e58e15e13aa919dc249ac051d1bfdfb4a96bc5fbb278"
        },
        {
          "content_sha256": "c8abf6c2794a489fbf1fe3de92a3d6aeec1def6ccf86c52e7ac149f118c6bde1",
          "logical_id": "mc-c5458d9bf53e30e69cdf8922",
          "row_sha256": "1332886658e4d7d7989ff974eaff3a8e036e76174b87a9b6399c4563b9d72573"
        },
        {
          "content_sha256": "29ce303c06d05a79ff8400b05c3213a23751e994ca9ddf949436c3123badf682",
          "logical_id": "mc-1d75315b1d98e6198d11bea5",
          "row_sha256": "cb75a2e999ef7be65ff81f4ecb23cdaa840fe2929d867a40ff93ed9fe2e9a43c"
        }
      ],
      "sha256": "4e61310fa980697d404e57d2e2b75d78512c9336cc463b74218146f29a7c0472",
      "sheet_name": "cards",
      "table_sha256": "aac9209bb07d393d6ea7b79c170700548c2479db83cd903b1e8729315bbbfa72",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 53904,
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
          "content_sha256": "ce33c5292f052b3be13f5adc81952e4c1198d06c12fd169f3dfc710e7c76fc11",
          "logical_id": "mc-c6ff59ea5ef045fc55f6a23f",
          "row_sha256": "74bc034c419dab2550496dbedab751041df467587437d8deb81c03d6d0c758b0"
        },
        {
          "content_sha256": "d8e7aff5b24ae8a733e575d3835c434c465ec6eac4ef7e795846f92f654fac70",
          "logical_id": "mc-f976aa38b9879032b0c34640",
          "row_sha256": "8103b3a5405013844c8d7ed32d04a7c7f9409fd11fb5bc9d49175ed3b118887e"
        },
        {
          "content_sha256": "ffa27069691e0796665d0a53a1a55bf78d3baaf2e845e8dc39d661a50b7caf76",
          "logical_id": "mc-d0cadfeaa8b31d4fdf194f4d",
          "row_sha256": "2aa2e8f6365ff1ffa32b660d918867d9aec765bfbab4ffd168adc7da4af162b8"
        },
        {
          "content_sha256": "5118e552c2ebdcf077224f43f04bb1c42bdf64bf350b5b76c6141cf575106759",
          "logical_id": "mc-1b6b6bf5b5cae30680cd15b3",
          "row_sha256": "388049c9a08bd2dded4084c2c627a7d91320f8314fbf5ace40134a8252be868a"
        },
        {
          "content_sha256": "867f4cd927a698aa588099b53a775cae7bc57be595a47a2fc1e91069f21ceee9",
          "logical_id": "mc-26b2bd02cc7fc3baad3d7816",
          "row_sha256": "773148748107a71963f93ab49376fbc1576f532b930acf00d413bf156f57363f"
        },
        {
          "content_sha256": "714c83ede40e424991a6c519f5957b6acaf67e366136901400f2258e90565c19",
          "logical_id": "mc-e236c2fffc4d370ff9caf8a7",
          "row_sha256": "0b4caa93e3b1a644013e6c848b6625e9d426d2f6bd064dcf06818eb8bd8e0c72"
        },
        {
          "content_sha256": "30ff4b583caf83cb29994761a9626026783de5b9c2c71d2efdb9d8a01fb477a2",
          "logical_id": "mc-385020ed4fdd34484e631abf",
          "row_sha256": "1fd621d34a22d0a47e3c0b0e5a3510898b857cbcb9c6409e7878aa9262418271"
        },
        {
          "content_sha256": "a53e7ad77d6de99834281ee9ce19ee1af3c993cfb319922a4bbb38f780c7946e",
          "logical_id": "mc-0be1cfb5e7e0f6f93e2c2381",
          "row_sha256": "fdd20bc0f4b8d4b23aef503cf32b93ba994fc46104a301b639ba48873e6f57db"
        },
        {
          "content_sha256": "79e569454836dc9619d1fa119df6b86d6e4680ce42eedd51c69fe5da4c34504b",
          "logical_id": "mc-5a62d0166df698913c98a27d",
          "row_sha256": "611f80e117bde827550e2e8220e2e77e2740675f439c50732938614af939bb16"
        },
        {
          "content_sha256": "676b003180768f78f5b0597b60b9a9157d1e86467e3f2622fed1b6f205aad9ae",
          "logical_id": "mc-dfa47e6149b7d295651f617c",
          "row_sha256": "9e40b4d0967f3ce2c18b7828e90710eaf9b5ebc43ed25e54865136837060ca41"
        },
        {
          "content_sha256": "303b7a5d2bf7e60b4cf16a865275248e25c242a4fb2f4fa80e843b14c19dc897",
          "logical_id": "mc-fb0c625aeade1143e630eb7b",
          "row_sha256": "1be8c086e59de1a4d1fa5dc50a9b5d0521a939e17b610611021536d278fd49bb"
        },
        {
          "content_sha256": "937c7b19650e2ff83f6641c88115a6b896d4bd57adcc3f66fa450b19b3ce3c16",
          "logical_id": "mc-30df6d9a5c0fd8e684af2f17",
          "row_sha256": "b23e48a70c2d1568dc9a644b26d544a33be5ddd6f43b5ca033c11d0958c2617d"
        },
        {
          "content_sha256": "a46baec908042f52c153e1ee35093cb8d66243f2c39d316004e00488e67c6804",
          "logical_id": "mc-281380095aabd19ad91c51d6",
          "row_sha256": "43787f5da1e66f00c2762f12c099511ce1a477e3ec88d8fc3dddeff77df618be"
        },
        {
          "content_sha256": "f4070cdcf6bfb860ebfa1e8a2fec20af7f98fbe6d2ee8547d1429adfb5fe1273",
          "logical_id": "mc-455b749f88ebfaba60062e8d",
          "row_sha256": "3246a66630a2d289132fb3896bdff7393ce89de001b2f42e46d45b8534e1d1e9"
        },
        {
          "content_sha256": "4fda5e015ec1e0cfa3c97778be5a8a55bfefe94f46e22d81581a99c63ef1edbe",
          "logical_id": "mc-be5feb89a08576b9a714cf5b",
          "row_sha256": "f5e17744f35932abc42c9ceca5feaa4f2c26e723eb88d85d438b4bff07f08042"
        },
        {
          "content_sha256": "f51876e32bf00e1b74fdde89e0e31c24fe796eb774995581fb0ee765c0fd8b2e",
          "logical_id": "mc-23c1c68e40760d05b71a8647",
          "row_sha256": "f437009173f09309d8c2ba4536e8450ea7fa8e849908833026586b57f6d445d5"
        },
        {
          "content_sha256": "4e39e9a979a73098aba1f4c86f3141013c81dc6a264d981233fd0a067b97fbcc",
          "logical_id": "mc-82b94c492ffa21b4e82a3f04",
          "row_sha256": "612a52bee53ea8948ba60362a24151d4080e5c80a31bd592d0dc0a848fe17bf3"
        },
        {
          "content_sha256": "a18858677f44074aa56c4f995817b54a402fee87975a8f08988065892c9df54b",
          "logical_id": "mc-c87676f61863c78bcbf9f2e6",
          "row_sha256": "8393b317185a531f6a7c42f878373c3be076204742a32cef965347170f172ce2"
        },
        {
          "content_sha256": "255bc30bde5a2a8e36bd78f419434df0c457cd4e6f6ae7f37d1cee72daa5d7ca",
          "logical_id": "mc-82357876d3d94994eda54ed6",
          "row_sha256": "5319df47a4e36ae2d2a157e282f2e1d5e90c9c09388628126de80186fe920dc9"
        },
        {
          "content_sha256": "1b031cbfdbed1360fd916d851980ac4a43fb38e630fbc27b57ae319b09907f7d",
          "logical_id": "mc-034e387fadad8ebbc0e6a813",
          "row_sha256": "2bd7dabf118cfc9e0f908af7515f27213f6fa07959847ac8a5e6404e55de2377"
        },
        {
          "content_sha256": "d490c197a9aaddbd0b097208f6155739ebe5b63c613727449ef1d8006f02f720",
          "logical_id": "mc-5516e8dc029539f4cd2a7d20",
          "row_sha256": "8aa7c156ccbc192bb8fe4fc408f79371909975539bb73e05dcc9202822679250"
        },
        {
          "content_sha256": "a7e74733ef959865dd4622b360ccacfe8648a75c9286c703f16f4a3e9640988a",
          "logical_id": "mc-39eb3cefd390d467f780353e",
          "row_sha256": "cf79c3f0bd4d961eec9d48d9ec6ab8701eeab17ad7fbc9401c45dca5545cd1a6"
        },
        {
          "content_sha256": "996da066c0c32fd06d61c90affa41a38bbcc95f20d69ba37b4484fe804529b5e",
          "logical_id": "mc-baa834639ffae733c9e8be5d",
          "row_sha256": "abfe039a59a4d21e5e3749687b71804953aa8fe26267178a40be4540bc81bfb7"
        },
        {
          "content_sha256": "f8f144cb1c42b41c682395daeeefa650ed97318962efb2b77bf4e4d7cc98ea82",
          "logical_id": "mc-36e11025799d6f84e627893b",
          "row_sha256": "bfab2b3ddf52fe5e7af43c0dd4bfe8cedd385b1be13ac04ef78201dfe5d51c4d"
        },
        {
          "content_sha256": "89b2f8c5736936c5419091f13e480837a9641839179a0f610c999c731956fcad",
          "logical_id": "mc-cf106f94c307b097e01f50c5",
          "row_sha256": "f71c01b553611f6228d2d4875975d6b21d371e4cebf3134d3afaacd22941992d"
        },
        {
          "content_sha256": "0121c4fbb352e0dae43366626ef3c3755fb48da22283b9e9b1530e04a197b5a1",
          "logical_id": "mc-32cb7a3958719df772201f26",
          "row_sha256": "3504446151546e845d8d14a8d1cde87674b3d94a59deeba7050283f427ee94ae"
        },
        {
          "content_sha256": "ce63446bc17ae4b5822ae988ea3329bf551ee571ff8affa39684c3bc05d88e97",
          "logical_id": "mc-f5fd3b25c2b1051f48aa2bc0",
          "row_sha256": "faad237b6c3d7caf37319859c97a1edd7c8b8c282ffe67a44052051266704812"
        },
        {
          "content_sha256": "59dd853717fd026d8c2b0c7b60082c5f2019fb79f642ca1b513cfdac5a1f91ac",
          "logical_id": "mc-401590969bcaa1ef6ff794b7",
          "row_sha256": "1cd167b6e5f47f3ddfbe5bcf0113e90f535ef71cc8a9b6655149561c86a53b80"
        },
        {
          "content_sha256": "92ba9c40f4bacd0796048d97fc00c620aabcc6f63894bd8dda81b9faf91c8c76",
          "logical_id": "mc-739b495a4d363d6539380874",
          "row_sha256": "f9fce1f4f4d1ff67441ed585112f81b52f30196798c2c657fce1eb14673734ad"
        },
        {
          "content_sha256": "e9cebefe830ad4b076a6b800fd3fef4fee96cf2df08b0b9e0d309c06c7f5aa59",
          "logical_id": "mc-40f72bc8635f39f0bf7723b3",
          "row_sha256": "3e8a9c34c0d8811b038e6315a643825994b158f9f85417ce821f72e89b2e605f"
        },
        {
          "content_sha256": "1cecfc0f59d2f5795b10f2eca2a775d84edfa2de6a2d84acd91d41626db62898",
          "logical_id": "mc-9c2d0dd6f8e7310510b51d0a",
          "row_sha256": "493a663b655382de34f9ef761f6e5df8c1406857ba4e0e91a858e5e591fa908d"
        }
      ],
      "sha256": "140074b91845e1c0f30890b42a35cbd736be354c2b2f71ba7e275998562699cd",
      "sheet_name": "cards",
      "table_sha256": "985ac50c4723929a4c377fb5cc582fa63d2416e47ee968adc8c92efccbce0107",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 9812,
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
          "content_sha256": "81ce6a29d3885da3ba8da9f6a03111dc9941231c6c65556e2003a53f6ea7c5b9",
          "logical_id": "mc-b454b74ff5412e8cdecb6903",
          "row_sha256": "dc876ec3f4bb73c55447c677c751dceb3f4536bbc67d6029483297ca61acc2fa"
        },
        {
          "content_sha256": "2dcb14cbb54462a6942e9f1d8f91e14289faae62eef319c743c3d80029497241",
          "logical_id": "mc-d1dda4cc075c9bc27a784223",
          "row_sha256": "152ecc070203b12683a6728c7f9fa3c02b53e0e93ac8066f6bb76cf568489b28"
        },
        {
          "content_sha256": "8430db281ea1cc6b2f18b85d7ac1466c20c10060ccdb7bff2a05b0ebdb940956",
          "logical_id": "mc-3d3e052793ab6f4d8ea66293",
          "row_sha256": "d17a3b616aacc35330bf7a4a6aa35590c7e2243d95b9aa7434b7a30759788b54"
        },
        {
          "content_sha256": "356c9c055c9be63604e3aa16c65a75214d36ea640867e7400b7ad4bebbbb136e",
          "logical_id": "mc-378dffdf971fa311ae0ebbf2",
          "row_sha256": "da823f49a5752474a3d8379f9907efdb41568d0813b207f23e33ab0ec651c435"
        }
      ],
      "sha256": "9996102d6ff0e2c03221b67733be1185c9174fbdf5e15c1dfb2f81d1ae05c157",
      "sheet_name": "cards",
      "table_sha256": "f72423551f442abb0daf82568add419aca7d05e3f214c055c0dcb9ee96aca4f1",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "9aede5ce2330eedac8c2dc3f1bc8ecff8f353a0d8ef681ab8c06196811b9c76e",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "block-scaled-matmul-log",
      "path": "docs/triton-learning/logs/2026-10-20-block-scaled-matmul.md",
      "sha256": "34630f5faaffb19ce8e5e75d44ebdf508c87ee08c209442aa7ea0fc9fd9a2f36",
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

导入文件：[triton-lesson-10-block-scaled-matmul-correction.xlsx](triton-lesson-10-block-scaled-matmul-correction.xlsx)（17 张卡）

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
