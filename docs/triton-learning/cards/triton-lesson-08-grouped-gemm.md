---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "f47655704345e2e5da8b23d79d9dca9924717265be31daee86c485760e7dd7e7",
  "candidate_sha256": "56d1df5459fef6e5b175d977e58a881b44e06cfe5244b4ae7d50d5b8c60b1b4e",
  "cards": [
    {
      "content_sha256": "be717113fce320e4608ce71343ced1f3dbca72ee0be643a4f87b3c25a5e9511e",
      "content_summary": "逐个调用闲置 SM 且多次发射，补齐白算零，grouped 一次发射但要设备侧调度并共用块大小",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "一组尺寸不同的矩阵乘法, 逐个调用、补齐后 batched、grouped 一次发射各浪费在哪里?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4cb9703d2980c4bdd7ab2cd9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "adcf62225977727b8a4af1c4d3e9b5ea062a32b3f981fb6eb0eba269b3c2b50e",
      "content_summary": "地址当整数存进设备表、kernel 内转成指针；类型、对齐与生命周期信息随之丢失",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "个数运行时才知道的一组矩阵怎样交给 triton kernel, 这样交丢掉了哪些信息?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f837b672b778ec0219eaadef",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "792406d45ba708b822b076e4ecfa73bbed0a14600faea7baa66d498d78f6cb9c",
      "content_summary": "偏移表是地址表的特例；PyTorch 在设备上展开偏移表而不读回行数，教程在主机上建表",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch",
          "version": "2.13.0"
        },
        "recall_target": "grouped_mm 的偏移表与 grouped gemm 的地址表是什么关系, 表由谁在哪里生成?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-31294289c7cb07c96f94ec7f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "556d8f5d183b6a91eb691013c46bfb42dd29ae969034ecb434b86c615d68035a",
      "content_summary": "块排成队列、CTA 按步长 NUM_SM 领取并用前缀和定位问题；只均分块数不均分工作量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "教程 grouped gemm 的静态步长调度怎样分配块, 保证什么、不保证什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-8757b9f6e70151e0f6984d61",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a12c2b879df5daaac004004048ba9fd05d38de8b86b058a181a06d8ed6886cf8",
      "content_summary": "缩小块只把最忙 CTA 的工作量降 8%，却让访存翻倍、固定开销变多；需实测决定",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "静态调度下缩小块让负载更均衡, 是否就更快? 换来什么、付出什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-690767f768283d26c6271c5a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "57781db70941f5a184ea01819328259b1d0cec30111bbb8135fb2288a600b2fa",
      "content_summary": "一块不可切分是不均衡的根因；按 K 降序排序或 Stream-K 切分 K 循环可以改进",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "cutlass",
          "version": "3.9.2"
        },
        "recall_target": "按块分配在各问题 k 不同时不均衡的根因, 以及不缩小块的两种改进。"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-409e92184013cece6069baea",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e7750eb89546bbb7da78e01252d640ce06f21b4b3a2532ca1e1df08b13cd2372",
      "content_summary": "顺序扫描的步数是 CTA 数乘问题数；CUTLASS 用 warp 内前缀和或主机预计算降低",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "cutlass",
          "version": "3.9.2"
        },
        "recall_target": "grouped gemm 找任务的扫描开销怎样增长, cutlass 用哪两种办法降低?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c5bf630863ad40f35afaa9a4",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "88a8d1f7a49fc6eee77ce8131f3a3cea6c6b6f28788dff4dcbaa9ea21e3277d8",
      "content_summary": "无 mask 时 M 不整写坏 C 之后的内存，N 不整绕行并竞争写，K 不整读入别处数据",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "去掉 mask 的 grouped gemm kernel 在 m、n、k 不整块时各会发生什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-8b3156614883d3ed58facc2c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b40b2e7d8c7f1dd3d1ba9a6cdf7c1e9cb91ff0af3344fb0483d2ee08fbb6fba7",
      "content_summary": "输入嵌进 NaN、输出嵌进哨兵值的缓冲区，四周至少留一整块，越界读写都会暴露",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "怎样设计测试让 kernel 的越界读和越界写必然暴露?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-5041b4749a815ed256ca914e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fe332142dd8cdda609f94502b6f3fb57739fc1a9e2f54c286c936bbded054264",
      "content_summary": "tl.multiple_of 是不被检查的对齐保证，决定能否用 16 字节异步拷贝和流水，不成立即未定义行为",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "tl.multiple_of 是什么性质的语句, 为什么地址表里读出的指针要写它, 去掉会怎样?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-56b14f2e2270888b7db0a794",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "224e3d9af520594ccb0bfaf799da2d74b9c89eafbf5b8b9e7e8aaff269978b7a",
      "content_summary": "每行行首都要对齐；行步长只是 8 字节倍数时如实保证 8 仍有流水，TMA 不能降档",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "行步长只是 8 字节倍数的矩阵, 对齐保证应怎样写, 能否用 tma?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7a2b8dde2017ce97c129968a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e40fae97951862358c355d6d3dc38c139ee3cad5dea4dd8859a9e8b64cb8572d",
      "content_summary": "cp.async 只有显存到共享内存一个方向；给 C 加保证只把写指令变宽，异步写回需要 TMA",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "给输出指针加对齐保证能否得到异步写回?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1c0584cb957cee3a2629ad34",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2bec3d36c2fd2ecea5ed75df81d7fdaa5c9199e132fdb326d5654b940f81e630",
      "content_summary": "描述符让硬件处理界外从而不要求整块，但要求对齐与全局暂存区，无 TMA 时改写成指针加 mask",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "描述符版 grouped gemm 怎样处理界外, 解除什么限制, 带来什么要求, 无 tma 时变成什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0dded41e05aaaec7ff1dcf5e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2ab23c834825c2fa9e21f2473bf78e442e8bf7f56633c593754c29473fa17a3c",
      "content_summary": "输出补齐只是分配方式不需拷贝，输入补齐必须拷贝，所以 PyTorch 对输入报错、对输出自己补宽",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch",
          "version": "2.13.0"
        },
        "recall_target": "行步长不对齐时, 为什么输出可以靠分配解决而输入只能拷贝?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-2d820b27e07e1e50f11a0cad",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "606ec25edcbec9034eda20caaaefc5ae0ecadaa60722e87550e38818d1778960",
      "content_summary": "B.T 只是视图，.contiguous() 才重排内存，kernel 内的 b.T 只贴转置标记；视图不能交给描述符版",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "b.t、b.t.contiguous() 与 kernel 里的 b.t 各自是否移动数据?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a50b796c2d19272f9e534f31",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a98a3e11e2e716ceec214eba5613fc29d4e2acafc239e60b58cd692a335b3079",
      "content_summary": "真实 MoE 只有 M 参差：N、K 整块且对齐成立、调度天然均衡，要处理的是不满的行和扫描开销",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "deepseek-v3 规模的 moe 层上, grouped gemm 的哪些问题真的会遇到?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-87ec651f88fce5d9d7a20a58",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "82f28bcc8cb4f25e9ae67aef5ae2039384a2afdc203b1cebcfd5f3e49d7f6539",
      "content_summary": "行方向的 mask 保持 16 字节异步拷贝，三向 mask 退回逐元素读；N、K 整块时行 mask 就够",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "只按行的 mask 与三个方向的 mask 对 16 字节异步拷贝各有什么影响?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7eb958bcfe8137ad5610eb65",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ed4b0819f9516a07c9d66f0b2d7835de26cda6253b968188c103e0903593a46f",
      "content_summary": "新后端上两版都退回同步搬运；先保证 M 方向正确与行数不回主机，再优化搬运",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "给没有 tma 和异步拷贝的新后端写 grouped gemm, 哪些会变, 优先保证什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-60e5eabe7206b7eecd8194ca",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f33d40ab38b57130989c3b3a6a7dfb1913f135e876d57f3f072ff0c3fd636360",
      "content_summary": "kernel 只见整数表无法验证假定，漏掉检查多为静默错误；检查放在包装函数并各自对应一条假定",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "包装函数漏掉检查时只收到整数表的 kernel 会怎样, 检查应依据什么来定?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-92948c07aa071915af8a9d1d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8328e570c4b45a255920f903c631948a8e9115d1f914df877c4ad13623b01e4b",
      "content_summary": "循环携带变量的类型不能变；类型一致时原地加完整偏移会逐轮累加",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton 循环里把标量指针原地改写成块指针会怎样?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-60337711491bb26fd6a0fc5a",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e872261a678ac37c9e550f01c2b5782e41a6090fcd598c856a108b306688b2df",
      "content_summary": "行步长取 stride(0) 而非列数；视图的行步长大于列数，用错不报错只是结果错",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "交给按行步长寻址的 kernel 时, 行步长应从哪里取?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f2703926f8452ddfb07707ea",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d1b8526da4f9e6f20cf9963cd63950debb613239b6c0d6ffb9ac8400642e8b01",
      "content_summary": "CTA 是任务、SM 是硬件；小问题让 SM 闲置，应说 SM 的利用率",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "小问题只发射少量 cta 时, 应说哪种资源的利用率低?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6d12446548eaa6fcae440a49",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "36d0f81b04fd45c2b003c81ed8af4ac66a9ef230e9e9cdf053a511483b8fab50",
      "content_summary": "行步长由最后一维决定；B 转置存放后满足对齐，描述符版里不满足的是 C",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "n 不是 8 的倍数时, 描述符版 grouped gemm 卡在哪个矩阵上?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6543932dde3b79554cadacf3",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c62856ec54e0daefdf089b9b7cc52213aca3fbe72a3bcf604e1177e5c98226b1",
      "content_summary": "动态领取只需一个原子计数器；每块一个标记要清零、搜索并重试",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "谁空谁领的动态调度需要什么共享状态, 怎样领取?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9d887183d7e364cedaccc1b9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c7bf3f9ecd7ac17b73323bd899644dd7bc888f548d80a1a0de1bf8602ce483de",
      "content_summary": "回退路径除多次发射和 SM 闲置外，还要把偏移表读回主机造成一次同步",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch",
          "version": "2.13.0"
        },
        "recall_target": "grouped_mm 回退路径相对一次发射的代价有哪些?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-326c0f996505f917401f4aab",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cd8753c550ba52f41382f957eab0f2cbfa82c7fcf332b04682e0d199f2dffe87",
      "content_summary": "data_ptr 是字节地址，偏移须乘元素大小；kernel 内转成指针后才按元素计",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "在设备上由偏移表计算各组首地址时, 偏移量用什么单位?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1ca1121c65b8603e9099171f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "917daee34357fe29e521548de402067270a6e6f45846cc1ea5ea0783c87765de",
      "content_summary": "溢出的是行数乘步长乘元素大小的乘积；offs 保持 int32，先在设备上转 int64 再乘",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "pytorch",
          "version": "2.13.0"
        },
        "recall_target": "int32 偏移表在真实规模下计算字节偏移时应怎样避免溢出?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c34a65e437f7a61c22c5c782",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "de1d2f634d1f768856d008b1c18233ebdb88395b9105b4754a7841bb3366c4ee",
      "content_summary": "整组共用的特化标志要遍历所有问题来定，不能只看循环里剩下的最后一个",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为整组问题选择 kernel 特化的标志应依据什么来定?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f1f63fdbab207650a86976a3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "882a478ec4581056518a12ef50573d1ce9fc1d6f099039c9810fca37a1823133",
      "content_summary": "所有张量与同一个设备比较；它保护表中地址在 kernel 运行设备上有效",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "包装函数的同设备检查应和谁比较, 它保护 kernel 的哪个假定?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-29b23c98f69ce1c8edae90fb",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "75dec7187f2896676aae9c52034c9fc72947613bd27af153f36f6497366d8b43",
      "content_summary": "对齐保证不成立是未定义行为且不改变请求的字节，数值测试测不出，只能用参数测试覆盖",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "包装函数的哪项检查删掉后数值测试无法稳定发现, 应怎样测?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-341b7b7b70e55196c7f63ae3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "44a931499956a910e44ca73cad41c47c9411784be993b734485146152762e613",
      "content_summary": "保证只在调用了 tl.multiple_of 的指针上；指针版的 C 没有对齐假定，不应检查",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "指针版 grouped gemm 的包装函数该不该拒绝行步长未对齐的输出张量?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-24a5f092066054573d026d16",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "eb8957726b41b72a674f625cd153535e618f4802df65404b851b75e09c3a3bbe",
      "content_summary": "口述 grouped GEMM 的地址表、队列与步长领取、收益代价与满块边界",
      "dependency_content_sha256": {
        "mc-4cb9703d2980c4bdd7ab2cd9": "be717113fce320e4608ce71343ced1f3dbca72ee0be643a4f87b3c25a5e9511e",
        "mc-7eb958bcfe8137ad5610eb65": "82f28bcc8cb4f25e9ae67aef5ae2039384a2afdc203b1cebcfd5f3e49d7f6539",
        "mc-8757b9f6e70151e0f6984d61": "556d8f5d183b6a91eb691013c46bfb42dd29ae969034ecb434b86c615d68035a",
        "mc-8b3156614883d3ed58facc2c": "88a8d1f7a49fc6eee77ce8131f3a3cea6c6b6f28788dff4dcbaa9ea21e3277d8",
        "mc-f837b672b778ec0219eaadef": "adcf62225977727b8a4af1c4d3e9b5ea062a32b3f981fb6eb0eba269b3c2b50e"
      },
      "depends_on": [
        "mc-4cb9703d2980c4bdd7ab2cd9",
        "mc-7eb958bcfe8137ad5610eb65",
        "mc-8757b9f6e70151e0f6984d61",
        "mc-8b3156614883d3ed58facc2c",
        "mc-f837b672b778ec0219eaadef"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清教程的 grouped gemm 怎样一次发射算完一组矩阵乘, 以及收益、代价与边界。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-7fadec68d292af7ebc7a38a7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3fb1485e322d2aa59ddc917905cf47cfd90b530cb9bee9582af39bee73b9adfa",
      "content_summary": "口述对齐保证、异步拷贝的档位、mask 的影响与 TMA 描述符的条件和回退",
      "dependency_content_sha256": {
        "mc-0dded41e05aaaec7ff1dcf5e": "2bec3d36c2fd2ecea5ed75df81d7fdaa5c9199e132fdb326d5654b940f81e630",
        "mc-1c0584cb957cee3a2629ad34": "e40fae97951862358c355d6d3dc38c139ee3cad5dea4dd8859a9e8b64cb8572d",
        "mc-56b14f2e2270888b7db0a794": "fe332142dd8cdda609f94502b6f3fb57739fc1a9e2f54c286c936bbded054264",
        "mc-7a2b8dde2017ce97c129968a": "224e3d9af520594ccb0bfaf799da2d74b9c89eafbf5b8b9e7e8aaff269978b7a",
        "mc-7eb958bcfe8137ad5610eb65": "82f28bcc8cb4f25e9ae67aef5ae2039384a2afdc203b1cebcfd5f3e49d7f6539"
      },
      "depends_on": [
        "mc-0dded41e05aaaec7ff1dcf5e",
        "mc-1c0584cb957cee3a2629ad34",
        "mc-56b14f2e2270888b7db0a794",
        "mc-7a2b8dde2017ce97c129968a",
        "mc-7eb958bcfe8137ad5610eb65"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清对齐保证、异步拷贝与 tma 描述符各自的作用和失效条件。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-9e911b985cc1ce276f1ebe37",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d262d36a94f8601cfb46e8b8e11610e84669015ea38b68f0929cfe0fe85ae302",
      "content_summary": "口述 kernel 的输入假定由包装函数保证、保护区与参数测试的分工以及数值测试的盲区",
      "dependency_content_sha256": {
        "mc-24a5f092066054573d026d16": "44a931499956a910e44ca73cad41c47c9411784be993b734485146152762e613",
        "mc-341b7b7b70e55196c7f63ae3": "75dec7187f2896676aae9c52034c9fc72947613bd27af153f36f6497366d8b43",
        "mc-5041b4749a815ed256ca914e": "b40b2e7d8c7f1dd3d1ba9a6cdf7c1e9cb91ff0af3344fb0483d2ee08fbb6fba7",
        "mc-92948c07aa071915af8a9d1d": "f33d40ab38b57130989c3b3a6a7dfb1913f135e876d57f3f072ff0c3fd636360",
        "mc-f1f63fdbab207650a86976a3": "de1d2f634d1f768856d008b1c18233ebdb88395b9105b4754a7841bb3366c4ee"
      },
      "depends_on": [
        "mc-24a5f092066054573d026d16",
        "mc-341b7b7b70e55196c7f63ae3",
        "mc-5041b4749a815ed256ca914e",
        "mc-92948c07aa071915af8a9d1d",
        "mc-f1f63fdbab207650a86976a3"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清 grouped gemm kernel 的输入假定由谁保证、怎样测试、哪些错误测不出来。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-2a6dc333c733daf798c752ba",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "467d52a55bab41696b7b9eb470979a9b7b15cfd0bc9c063a3dbed5c64567e71d",
  "manifest_payload_sha256": "ee66eb10f34498b74831016e0e0a553f3d5c7289c1931fca0b3a2c1a3c468be2",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 18485,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-08-grouped-gemm-correction.xlsx",
      "row_count": 10,
      "rows": [
        {
          "content_sha256": "d1b8526da4f9e6f20cf9963cd63950debb613239b6c0d6ffb9ac8400642e8b01",
          "logical_id": "mc-6d12446548eaa6fcae440a49",
          "row_sha256": "3bf8452b7f310e22c6672c6f047b458eeddf1a566d0159e6decb5e2e77f7b19a"
        },
        {
          "content_sha256": "36d0f81b04fd45c2b003c81ed8af4ac66a9ef230e9e9cdf053a511483b8fab50",
          "logical_id": "mc-6543932dde3b79554cadacf3",
          "row_sha256": "4fdfd4effe323273c74f3280a9f2b8697addc5da02ae51bbc455c7973fe58f20"
        },
        {
          "content_sha256": "c62856ec54e0daefdf089b9b7cc52213aca3fbe72a3bcf604e1177e5c98226b1",
          "logical_id": "mc-9d887183d7e364cedaccc1b9",
          "row_sha256": "434e12d25e7232a82101ca6579b982822b4a2db06b85168c15a1ddf711fe6baf"
        },
        {
          "content_sha256": "c7bf3f9ecd7ac17b73323bd899644dd7bc888f548d80a1a0de1bf8602ce483de",
          "logical_id": "mc-326c0f996505f917401f4aab",
          "row_sha256": "2cd47c721741074ee60e722c038b00306c1f292e6ff534133cf534570be94783"
        },
        {
          "content_sha256": "cd8753c550ba52f41382f957eab0f2cbfa82c7fcf332b04682e0d199f2dffe87",
          "logical_id": "mc-1ca1121c65b8603e9099171f",
          "row_sha256": "a56299b39376c9b823e0cd5ba114bfa913e15939f56ea75a52dd62a1b19c1e01"
        },
        {
          "content_sha256": "917daee34357fe29e521548de402067270a6e6f45846cc1ea5ea0783c87765de",
          "logical_id": "mc-c34a65e437f7a61c22c5c782",
          "row_sha256": "6b8e179d34fd7170f85a5ad20d4d3bac755a010122c7a474d2cee75e33720478"
        },
        {
          "content_sha256": "de1d2f634d1f768856d008b1c18233ebdb88395b9105b4754a7841bb3366c4ee",
          "logical_id": "mc-f1f63fdbab207650a86976a3",
          "row_sha256": "bf47e2854f7b52fcdcc56bc4ab08c1a8dd54d42614dc4d21c45befc7da046ab1"
        },
        {
          "content_sha256": "882a478ec4581056518a12ef50573d1ce9fc1d6f099039c9810fca37a1823133",
          "logical_id": "mc-29b23c98f69ce1c8edae90fb",
          "row_sha256": "d3443950c3f16f5c4b0cc72cd837ea3c6f0c27dd4c7eaf1c05fd1eab3100ce92"
        },
        {
          "content_sha256": "75dec7187f2896676aae9c52034c9fc72947613bd27af153f36f6497366d8b43",
          "logical_id": "mc-341b7b7b70e55196c7f63ae3",
          "row_sha256": "114afadf356ff449c7ff119d4b15a16840e80bb81ff14602051ac5f6cfa53f95"
        },
        {
          "content_sha256": "44a931499956a910e44ca73cad41c47c9411784be993b734485146152762e613",
          "logical_id": "mc-24a5f092066054573d026d16",
          "row_sha256": "5ed1cc33774dafd9e84ac0ad4ece9d51bc1397c2a23c99307038720ad58ccaab"
        }
      ],
      "sha256": "3fc2b616f9dbd5519d8894b82e28021e586e85c495d21c78e217c1bd31ad0c9b",
      "sheet_name": "cards",
      "table_sha256": "36f03c003bfafa1bc34047ca4be54d68bd3dd4176ccd425528e78135f8673fdd",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 35479,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-08-grouped-gemm-technical-qa.xlsx",
      "row_count": 21,
      "rows": [
        {
          "content_sha256": "be717113fce320e4608ce71343ced1f3dbca72ee0be643a4f87b3c25a5e9511e",
          "logical_id": "mc-4cb9703d2980c4bdd7ab2cd9",
          "row_sha256": "ded2da341391ae4338217e9bf14d984370277d072a45651d34fde8ffec005da2"
        },
        {
          "content_sha256": "adcf62225977727b8a4af1c4d3e9b5ea062a32b3f981fb6eb0eba269b3c2b50e",
          "logical_id": "mc-f837b672b778ec0219eaadef",
          "row_sha256": "aeb1d6cb6b0d54e16d347826cf976bd32ba38909d1de7b0434a3739c6a978687"
        },
        {
          "content_sha256": "792406d45ba708b822b076e4ecfa73bbed0a14600faea7baa66d498d78f6cb9c",
          "logical_id": "mc-31294289c7cb07c96f94ec7f",
          "row_sha256": "1c7886ad571b727db22d84cdc2b219b56b9304e2a4df75354488e388457aa802"
        },
        {
          "content_sha256": "556d8f5d183b6a91eb691013c46bfb42dd29ae969034ecb434b86c615d68035a",
          "logical_id": "mc-8757b9f6e70151e0f6984d61",
          "row_sha256": "6b22ad06624601635aac34633f072748d7a21472262e85ca3e195fcb2807efe6"
        },
        {
          "content_sha256": "a12c2b879df5daaac004004048ba9fd05d38de8b86b058a181a06d8ed6886cf8",
          "logical_id": "mc-690767f768283d26c6271c5a",
          "row_sha256": "24862b2e71fb7c5cb44bd33c566d184dc72714d1153d8a2002ce8c8bb0f08a76"
        },
        {
          "content_sha256": "57781db70941f5a184ea01819328259b1d0cec30111bbb8135fb2288a600b2fa",
          "logical_id": "mc-409e92184013cece6069baea",
          "row_sha256": "38799e3ae30ebcb487820ca8b111838cce1aa7ff66c64eea67d52bdc0dd4ca0d"
        },
        {
          "content_sha256": "e7750eb89546bbb7da78e01252d640ce06f21b4b3a2532ca1e1df08b13cd2372",
          "logical_id": "mc-c5bf630863ad40f35afaa9a4",
          "row_sha256": "247aac8ae7921ad8738960b39f5807cb240b1a26a4803451302c5830b5e6a4f0"
        },
        {
          "content_sha256": "88a8d1f7a49fc6eee77ce8131f3a3cea6c6b6f28788dff4dcbaa9ea21e3277d8",
          "logical_id": "mc-8b3156614883d3ed58facc2c",
          "row_sha256": "86cee517d3ad4dbc5e59de20c7290584d46d3db6e2ebc5c15020568f83bca500"
        },
        {
          "content_sha256": "b40b2e7d8c7f1dd3d1ba9a6cdf7c1e9cb91ff0af3344fb0483d2ee08fbb6fba7",
          "logical_id": "mc-5041b4749a815ed256ca914e",
          "row_sha256": "879a4511909b6ce07449b0b35b80cf54d6c05f46bcdd0f41cdac2405f03fe53c"
        },
        {
          "content_sha256": "fe332142dd8cdda609f94502b6f3fb57739fc1a9e2f54c286c936bbded054264",
          "logical_id": "mc-56b14f2e2270888b7db0a794",
          "row_sha256": "50d3d8abc682b1bf987c9d83c6175419f0d2d4d046ae81108c5caca668c14934"
        },
        {
          "content_sha256": "224e3d9af520594ccb0bfaf799da2d74b9c89eafbf5b8b9e7e8aaff269978b7a",
          "logical_id": "mc-7a2b8dde2017ce97c129968a",
          "row_sha256": "1ed63026382cf33edaf1a627b13b1a9630fc54b5fa04023bfa65a2d8f12c2e3b"
        },
        {
          "content_sha256": "e40fae97951862358c355d6d3dc38c139ee3cad5dea4dd8859a9e8b64cb8572d",
          "logical_id": "mc-1c0584cb957cee3a2629ad34",
          "row_sha256": "856905163440814ecc8bab8fa88d0236a40f02819094b2a2bd0022185ad92a0f"
        },
        {
          "content_sha256": "2bec3d36c2fd2ecea5ed75df81d7fdaa5c9199e132fdb326d5654b940f81e630",
          "logical_id": "mc-0dded41e05aaaec7ff1dcf5e",
          "row_sha256": "7a0d2ec60108edada8ae891d9ff1824ae9c9e1ddb1fa5ffd68de9d449f7f5986"
        },
        {
          "content_sha256": "2ab23c834825c2fa9e21f2473bf78e442e8bf7f56633c593754c29473fa17a3c",
          "logical_id": "mc-2d820b27e07e1e50f11a0cad",
          "row_sha256": "81b331fc482641e26f39ce5d17114188e2c2d4149a3f7de4cd635834a02c0f6e"
        },
        {
          "content_sha256": "606ec25edcbec9034eda20caaaefc5ae0ecadaa60722e87550e38818d1778960",
          "logical_id": "mc-a50b796c2d19272f9e534f31",
          "row_sha256": "e9795113643f8b3251d934342da70c81575139498789950c27b7fba787f0c0b7"
        },
        {
          "content_sha256": "a98a3e11e2e716ceec214eba5613fc29d4e2acafc239e60b58cd692a335b3079",
          "logical_id": "mc-87ec651f88fce5d9d7a20a58",
          "row_sha256": "322f1de2557411fd11b88791026e23459ee13e37fc9e5099c70287a0ebd2b8b9"
        },
        {
          "content_sha256": "82f28bcc8cb4f25e9ae67aef5ae2039384a2afdc203b1cebcfd5f3e49d7f6539",
          "logical_id": "mc-7eb958bcfe8137ad5610eb65",
          "row_sha256": "b6c8638fa33003f52e85d499a50a26fea2970a9df45ba18d595c4641e9f69008"
        },
        {
          "content_sha256": "ed4b0819f9516a07c9d66f0b2d7835de26cda6253b968188c103e0903593a46f",
          "logical_id": "mc-60e5eabe7206b7eecd8194ca",
          "row_sha256": "c9d433d4fd56e158cfdbee8fa358bc2d427a6d7d0e3fd5e5dd61ba8b6cf5650b"
        },
        {
          "content_sha256": "f33d40ab38b57130989c3b3a6a7dfb1913f135e876d57f3f072ff0c3fd636360",
          "logical_id": "mc-92948c07aa071915af8a9d1d",
          "row_sha256": "8c05bf89c9655a94f7640184ce90b665c6bb5fa90471432d64bd23b2fcf5425f"
        },
        {
          "content_sha256": "8328e570c4b45a255920f903c631948a8e9115d1f914df877c4ad13623b01e4b",
          "logical_id": "mc-60337711491bb26fd6a0fc5a",
          "row_sha256": "53b6be391f2e4201a83133cb500d8a7568f71873ab228761153a092a5db15967"
        },
        {
          "content_sha256": "e872261a678ac37c9e550f01c2b5782e41a6090fcd598c856a108b306688b2df",
          "logical_id": "mc-f2703926f8452ddfb07707ea",
          "row_sha256": "150fd2a4cd1f7bf52c7ae5e88aa6407de4468a800360b6f7f323361a61c408e2"
        }
      ],
      "sha256": "0984bc3a39fb14e283ebb1574823704f706a449d992334048bb670ee31704d56",
      "sheet_name": "cards",
      "table_sha256": "1694691e522bc843a219ddc824cfd0e4e2e64cbbcc7cb46b2551a940a74b7eb1",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 8382,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-08-grouped-gemm-oral.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "eb8957726b41b72a674f625cd153535e618f4802df65404b851b75e09c3a3bbe",
          "logical_id": "mc-7fadec68d292af7ebc7a38a7",
          "row_sha256": "1fa78fe94c297de88ffa96e995b3df25fb1bf3915ac52b704ebb5eb84e2ae357"
        },
        {
          "content_sha256": "3fb1485e322d2aa59ddc917905cf47cfd90b530cb9bee9582af39bee73b9adfa",
          "logical_id": "mc-9e911b985cc1ce276f1ebe37",
          "row_sha256": "198dd507d8dd03b0345cd12a153baa4438bbc4b2038eea26629f9b9b0981d11d"
        },
        {
          "content_sha256": "d262d36a94f8601cfb46e8b8e11610e84669015ea38b68f0929cfe0fe85ae302",
          "logical_id": "mc-2a6dc333c733daf798c752ba",
          "row_sha256": "a3eceac573e803936dccf5b03143fd4b5b09de9e0e3c12c5392c9a2feca7c193"
        }
      ],
      "sha256": "0364d6e9b51d002073f5847a68ef57fff9e291c1991e6610ec030e86ffce2342",
      "sheet_name": "cards",
      "table_sha256": "9ffcae8254a3df39f8c34b5854b1fced5b215ff6a4765465275c86c1a2de2ae2",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "f3c848cdcd125cb81992c38e816b2262935cc80ee53703e22ef978993adcdc73",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "grouped-gemm-log",
      "path": "docs/triton-learning/logs/2026-10-09-grouped-gemm.md",
      "sha256": "9c5f117ccd3e5cc326b257099a99fc7a65dc1645d24c8551abdf4212e38af253",
      "summary": "10/5–10/9：grouped GEMM 的调度、对齐与 TMA、任意尺寸实现的纠错与答疑"
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

导入文件：[triton-lesson-08-grouped-gemm-correction.xlsx](triton-lesson-08-grouped-gemm-correction.xlsx)（10 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-08-grouped-gemm-technical-qa.xlsx](triton-lesson-08-grouped-gemm-technical-qa.xlsx)（21 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-08-grouped-gemm-oral.xlsx](triton-lesson-08-grouped-gemm-oral.xlsx)（3 张卡）
