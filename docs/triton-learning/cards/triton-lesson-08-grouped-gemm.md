---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "94be1225af449dedd5117ff57e712a000c8c39a7e8b0e77db229eec2c5859a10",
  "candidate_sha256": "ccf44fbf52364879379ce555d46b62138bdda53e524d82d356353b4e961a7c37",
  "cards": [
    {
      "content_sha256": "85c6640d3476d76f6f24bc53bc7311addfba3d682ca31dee2bc69e96e3d85da5",
      "content_summary": "逐个调用闲置 SM 且多次发射，补齐白算零；grouped 一次发射，代价是扫描、共用块大小与只均分块数",
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
      "content_sha256": "7f3f26e6b37500cc021053572c507dd62d79c27f19a06cf3114e4709f63046d8",
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
      "content_sha256": "7979b8d78e46e7d13f0ba533ac9a12f43582d7cae81e3ff4aa042ab6244e6337",
      "content_summary": "偏移表是地址表的特例，所以 PyTorch 能在设备上从 offs 展开地址、不读回行数；教程在主机上建表",
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
      "content_sha256": "8a589d73702b30a5f8d1f3566a57abc59ea739e33422929e57ed12f82c7e3c5f",
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
      "content_sha256": "1ccbf4c5f932c490da5d8155228c6842d1b26dc02c73fcc2eee297c29a66a012",
      "content_summary": "缩小块只能把最忙 CTA 压到平均值附近，却让每次乘加的读入量翻倍、按块计的开销变多；块大小需实测决定",
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
      "content_sha256": "0c567a62375449a3d73038b20a27e2082094a3f6ac38f19c86d607f2ae4289bd",
      "content_summary": "一块不可切分是不均衡的根因；按 K 降序排序让相邻块工作量相近，Stream-K 切分 K 循环但要合并部分和",
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
      "content_sha256": "ace1cabf4e14206d5b6d23cd1518ff8eec1533bcfca95f792598b89c7b3d3eef",
      "content_summary": "顺序扫描的步数是 CTA 数乘问题数；CUTLASS 的 warp 内前缀和与主机预计算不需逐个问题扫描（动机为推断）",
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
      "content_sha256": "e3374f38611c208faa8ec216f9ff4f00150a7b8a26a43114d687f45e8462a568",
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
      "content_sha256": "e23c995a53b48d3a58e6a3518d18525966e5379b4e5b1a1e73f974a80e97112d",
      "content_summary": "输入嵌进 NaN、输出嵌进哨兵值的缓冲区，四周至少留一整块；被测函数接收视图并按 stride(0) 取行步长",
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
      "content_sha256": "05bda9d54e8f5d987d1fbbc690b441b6afd03ef22d34cc4647757387a9f1b3c4",
      "content_summary": "tl.multiple_of 是不被检查的 16 字节对齐保证；表里的指针没有发射时的对齐特化；去掉退回 2 字节读且无流水；违反时 H100 实测报 misaligned address",
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
      "content_sha256": "c642651878e82ebdb1e094ef30593be774d52eb72e8136631015381c7fc59c21",
      "content_summary": "每行行首都要对齐；行步长只是 8 字节倍数时如实保证 8，宽度减半、流水仍在，TMA 不能降档",
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
      "content_sha256": "0f7a3989e413288be1ec058e199ef2da7bd71590adcfca4aa34e67fe59e757cb",
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
      "content_sha256": "ae364cb560d13968fe54fcd9f9edbc2e9025e38b496c24c648322ba250e8ae90",
      "content_summary": "描述符让硬件处理界外从而不要求整块，代价是 16 字节对齐、设备端现场创建与全局暂存区",
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
      "content_sha256": "7c9ea3ca38aa6a2eb817ae2ccf309671117627911d0ca2fb1b39b03b5f9ceaa8",
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
      "content_sha256": "ebb25314c99e708aed07add890e1da10e561ce06d79283d8b8d4c439258d5545",
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
      "content_sha256": "cf6c2e14339e7494c8f096beea156de5e3739b8180ed61f48b385388f414539f",
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
      "content_sha256": "d845b378c7dd9964cb1c675985dda32a36412c23be13278464730b729b990932",
      "content_summary": "宽度取指针对齐与 mask 恒定长度的较小者：行 mask 保持 16 字节异步拷贝，表里读出的 N、K 让三向 mask 的宽度降到 2 字节",
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
      "content_sha256": "c20b49ad844ab18255cac7614e10e5c70eac08978b6a68bfd82e7eadec533e17",
      "content_summary": "调度、地址表与行 mask 与后端无关；描述符版是否改写成指针加 mask 取决于后端的 pass；先保 M 方向正确与行数不回主机",
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
      "content_sha256": "1c103bd7c8db2d4a09f255b529baf662f1222c592a8826eb527b4d12d58f935d",
      "content_summary": "kernel 只见整数表无法验证假定，漏掉检查多为静默错误；包装函数是最后的检查点，每项检查对应一条假定",
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
      "content_sha256": "1e10f279785f23357c998274c9baabe593d00dba330fded7459469e70cfb2c5a",
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
      "content_sha256": "b396e7408888887c4ba97d2b9b76ab3b3910ff3ae551c7ee2663c425fa077a6a",
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
      "content_sha256": "b3344e1e21ea8e2e201d3be906cd698e4118f9ef769ecf724c899f76a153b539",
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
      "content_sha256": "69d0f0d9b4da915c17eaac890677490e45112b73fed573e60e669553c28c7f4a",
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
      "content_sha256": "7e27573510d206d73ecd48e1a0a31f3f4c3ee323ea61516a6706b78be98c125b",
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
      "content_sha256": "4af44641aa8a32b406b4929e0b1513c5ff3195fa56783e8ab3b8d678509456b1",
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
      "content_sha256": "1f243618149ff7ad2355b3b6ac12e45cc72252b067740164cea51b07fef012f6",
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
      "content_sha256": "02faaaeecc11ae6f6907ccbb08a2f0c64aec44e7a65ca156793e57425e2c110e",
      "content_summary": "设备检查保护表中地址在 kernel 运行设备上有效，不是要求 CUDA；所有张量要与同一个设备比较",
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
      "content_sha256": "90aeb804a9559d3cbdb80acce93156f1f6d1350c3f628fb1668ef0d987cdbfa8",
      "content_summary": "对齐保证不成立是未定义行为，结果取决于设备（解释器算对、H100 实测报 misaligned address），数值测试测不出，只能用参数测试覆盖；维数检查去掉后行为不变",
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
      "content_sha256": "6735aca7e1d0d9636a0b74ba665454c03cd3c3e407d0d0368b2fb1ea3cf2e8d9",
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
      "content_sha256": "d942196d5e9fc38f943bf1157ea6452ce0e518f7e0ffd3924f95719094357796",
      "content_summary": "口述 grouped GEMM 的地址表、队列与步长领取、收益代价，以及满块假定与真实 MoE 只有行数参差",
      "dependency_content_sha256": {
        "mc-4cb9703d2980c4bdd7ab2cd9": "85c6640d3476d76f6f24bc53bc7311addfba3d682ca31dee2bc69e96e3d85da5",
        "mc-8757b9f6e70151e0f6984d61": "8a589d73702b30a5f8d1f3566a57abc59ea739e33422929e57ed12f82c7e3c5f",
        "mc-87ec651f88fce5d9d7a20a58": "cf6c2e14339e7494c8f096beea156de5e3739b8180ed61f48b385388f414539f",
        "mc-8b3156614883d3ed58facc2c": "e3374f38611c208faa8ec216f9ff4f00150a7b8a26a43114d687f45e8462a568",
        "mc-f837b672b778ec0219eaadef": "7f3f26e6b37500cc021053572c507dd62d79c27f19a06cf3114e4709f63046d8"
      },
      "depends_on": [
        "mc-4cb9703d2980c4bdd7ab2cd9",
        "mc-8757b9f6e70151e0f6984d61",
        "mc-87ec651f88fce5d9d7a20a58",
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
      "review_resolution": {
        "summary": "已按更新后的子卡复核：子卡改为 why-grouped、address-table-indirection、static-strided-scheduling、full-tile-assumption-failures、moe-real-scale；参考回答删去子卡之外的两句，边界改为真实 MoE 只有行数参差；五个锚点均有子卡支撑。"
      },
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ea0a4926130a54d6db06488a45013d0043f4c9acd248107b22f7c5cb9ef263a4",
      "content_summary": "口述对齐保证、异步拷贝的档位、mask 的影响与 TMA 描述符的条件，以及违反保证属未定义行为",
      "dependency_content_sha256": {
        "mc-0dded41e05aaaec7ff1dcf5e": "ae364cb560d13968fe54fcd9f9edbc2e9025e38b496c24c648322ba250e8ae90",
        "mc-1c0584cb957cee3a2629ad34": "0f7a3989e413288be1ec058e199ef2da7bd71590adcfca4aa34e67fe59e757cb",
        "mc-56b14f2e2270888b7db0a794": "05bda9d54e8f5d987d1fbbc690b441b6afd03ef22d34cc4647757387a9f1b3c4",
        "mc-7a2b8dde2017ce97c129968a": "c642651878e82ebdb1e094ef30593be774d52eb72e8136631015381c7fc59c21",
        "mc-7eb958bcfe8137ad5610eb65": "d845b378c7dd9964cb1c675985dda32a36412c23be13278464730b729b990932"
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
      "review_resolution": {
        "summary": "已按更新后的子卡 multiple-of-promise 复核：违反对齐保证的后果改为 H100 实测报 misaligned address、进程的 CUDA 不能再用、其他后端未实测；锚点 5 同步改为不能把报错当作检查；其余四个锚点仍由子卡支撑。"
      },
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b0cdfebaec41c0ece1a21d0226dd8791b6246a2f1ecaf1823abeb2863ff7b247",
      "content_summary": "口述 kernel 的输入假定由包装函数保证、保护区与参数测试的分工以及数值测试的盲区",
      "dependency_content_sha256": {
        "mc-24a5f092066054573d026d16": "6735aca7e1d0d9636a0b74ba665454c03cd3c3e407d0d0368b2fb1ea3cf2e8d9",
        "mc-341b7b7b70e55196c7f63ae3": "90aeb804a9559d3cbdb80acce93156f1f6d1350c3f628fb1668ef0d987cdbfa8",
        "mc-5041b4749a815ed256ca914e": "e23c995a53b48d3a58e6a3518d18525966e5379b4e5b1a1e73f974a80e97112d",
        "mc-92948c07aa071915af8a9d1d": "1c103bd7c8db2d4a09f255b529baf662f1222c592a8826eb527b4d12d58f935d",
        "mc-d8e3e65238ac006bc0e9c895": "0bc7754b8ab9a29688008bc54173c29bc76792a9072c5c72b97f1f2f3b6a4c6c"
      },
      "depends_on": [
        "mc-24a5f092066054573d026d16",
        "mc-341b7b7b70e55196c7f63ae3",
        "mc-5041b4749a815ed256ca914e",
        "mc-92948c07aa071915af8a9d1d",
        "mc-d8e3e65238ac006bc0e9c895"
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
      "review_resolution": {
        "summary": "已按更新后的子卡 alignment-check-untestable 复核：测试盲区改为解释器算对、H100 实测报错且进程不能再用，结论仍是只能用参数测试覆盖；五个锚点均有子卡支撑。"
      },
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ad9b1b07b19dd09f2897e95b0b301980638465fc44751f19c741072d9c0f4e64",
      "content_summary": "固定 CTA 循环领多块时，描述符版发起 TMA 写回后不等待就算下一块，写回与计算重叠；每块一个 CTA 没有这个机会",
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
        "recall_target": "固定数量的 cta 循环领多块相比每块一个 cta, 给描述符版的写回带来什么重叠机会?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4a0b029427535b3bd13b3151",
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
      "content_sha256": "a189db829d3ab6ebe41fced3639b95eb851ca1b98ecda047eb939f0b54952b18",
      "content_summary": "用读回调用会抛 AssertionError 的张量子类代替 offs，打印也会触发；拦不住先转存到普通张量再读回",
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
        "recall_target": "怎样在测试里证明被测代码没有把设备张量读回主机, 这种检查拦不住什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-76013dacd88d00aaaf9163f5",
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
      "content_sha256": "0bc7754b8ab9a29688008bc54173c29bc76792a9072c5c72b97f1f2f3b6a4c6c",
      "content_summary": "整组标志只看最后一个问题时，特殊问题都排在末尾的测试会碰巧通过；测试要变换特殊元素的位置",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-grouped-gemm",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "整组共用的特化标志被写成只看最后一个问题时, 为什么测试没发现, 测试输入应怎样设计?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d8e3e65238ac006bc0e9c895",
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
      "content_sha256": "d3d1f52878e87742141c05e4d36771344be744a75bdd85bbccd346095cd7965c",
      "content_summary": "& 优先级高于 <，a < M & b < K 被解析成链式比较；每个比较都加括号",
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
        "recall_target": "构造 mask 时 a < m & b < k 为什么报错, 应怎样写?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1f8f9a157e092f249e1409c7",
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
      "content_sha256": "cb163177f4b779750d4c6ecee9165264aef0adb9ac7797552da662edf94c2840",
      "content_summary": "对齐要求看行步长字节数是否为 16 的倍数，不是连续；连续的 K=1020 输入不满足，补宽步长的不连续输出反而满足",
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
        "recall_target": "tma 描述符对矩阵内存布局的要求是行步长对齐还是张量连续?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1f4cfaee97d004836018847d",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "grouped-gemm-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "ed96b26c7ab9731bb60d1fae7c0aab7a8c4a9301644a546bc7435181879854ce",
  "manifest_payload_sha256": "6f4d7b1dd56006b18d7e465856d422315037645c5cbfa78b4adb3f3659e7bd25",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 19487,
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
          "content_sha256": "b396e7408888887c4ba97d2b9b76ab3b3910ff3ae551c7ee2663c425fa077a6a",
          "logical_id": "mc-6d12446548eaa6fcae440a49",
          "row_sha256": "5d3a6084afa74ca7e3d08dacbb9e94743b23b744c4dd0d69994603c3c1299b10"
        },
        {
          "content_sha256": "b3344e1e21ea8e2e201d3be906cd698e4118f9ef769ecf724c899f76a153b539",
          "logical_id": "mc-6543932dde3b79554cadacf3",
          "row_sha256": "f0b858238e3ac2d989fe2d472a1744d783ce2b77a8ff2baae05c6f3b6bf04349"
        },
        {
          "content_sha256": "69d0f0d9b4da915c17eaac890677490e45112b73fed573e60e669553c28c7f4a",
          "logical_id": "mc-9d887183d7e364cedaccc1b9",
          "row_sha256": "da8458831a8614b9b6a48f1166c1183986c27d432d7b25895cab4d4079a7c423"
        },
        {
          "content_sha256": "7e27573510d206d73ecd48e1a0a31f3f4c3ee323ea61516a6706b78be98c125b",
          "logical_id": "mc-326c0f996505f917401f4aab",
          "row_sha256": "04520027b08c4e8a4ec7da94276a6bc41d77b44343464b1747333600422d963d"
        },
        {
          "content_sha256": "4af44641aa8a32b406b4929e0b1513c5ff3195fa56783e8ab3b8d678509456b1",
          "logical_id": "mc-1ca1121c65b8603e9099171f",
          "row_sha256": "73d6abb81d0f93943de3f8214be3ce7214d2ad956d96cbd7526488d59435f6f6"
        },
        {
          "content_sha256": "1f243618149ff7ad2355b3b6ac12e45cc72252b067740164cea51b07fef012f6",
          "logical_id": "mc-c34a65e437f7a61c22c5c782",
          "row_sha256": "c0def2f7633a14dd081d5d8b001e3de4827606a329df4cc9ac95bcbdcf4c37c0"
        },
        {
          "content_sha256": "02faaaeecc11ae6f6907ccbb08a2f0c64aec44e7a65ca156793e57425e2c110e",
          "logical_id": "mc-29b23c98f69ce1c8edae90fb",
          "row_sha256": "142ca3afa2a3fbf299a347c4f88be5b1f258413eb7e5731881df51f2213069dd"
        },
        {
          "content_sha256": "90aeb804a9559d3cbdb80acce93156f1f6d1350c3f628fb1668ef0d987cdbfa8",
          "logical_id": "mc-341b7b7b70e55196c7f63ae3",
          "row_sha256": "0e0b8ba3d9a3de5c38c1091a7ac59969b99eb1e6ba10e4b816ee1d2e12b8c362"
        },
        {
          "content_sha256": "6735aca7e1d0d9636a0b74ba665454c03cd3c3e407d0d0368b2fb1ea3cf2e8d9",
          "logical_id": "mc-24a5f092066054573d026d16",
          "row_sha256": "b8bc4e9e91feaa45fc8bd75018c71f12a3a3ad60e299d9633ad215cfb597cf35"
        },
        {
          "content_sha256": "cb163177f4b779750d4c6ecee9165264aef0adb9ac7797552da662edf94c2840",
          "logical_id": "mc-1f4cfaee97d004836018847d",
          "row_sha256": "183ea9caa4887b61063f591bc9d9d5ae461b624ad5158b3ada21981869f24f7b"
        }
      ],
      "sha256": "94f21bac534179e5a29bbc9a1f7788aaa13afb6e2b2ecb41d300cbe1eed48510",
      "sheet_name": "cards",
      "table_sha256": "3f5984b0660715768c6b32b88d6267ff4d853847fd632cea552a898f0854d795",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 40138,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-08-grouped-gemm-technical-qa.xlsx",
      "row_count": 24,
      "rows": [
        {
          "content_sha256": "85c6640d3476d76f6f24bc53bc7311addfba3d682ca31dee2bc69e96e3d85da5",
          "logical_id": "mc-4cb9703d2980c4bdd7ab2cd9",
          "row_sha256": "26a850036252f3938402efbc47896b73e4171e93449e123da9966f231ef30fe6"
        },
        {
          "content_sha256": "7f3f26e6b37500cc021053572c507dd62d79c27f19a06cf3114e4709f63046d8",
          "logical_id": "mc-f837b672b778ec0219eaadef",
          "row_sha256": "83925964b7c7b3e12e5315b873cd1c1b7d23844db8b2beea87f584bce61944de"
        },
        {
          "content_sha256": "7979b8d78e46e7d13f0ba533ac9a12f43582d7cae81e3ff4aa042ab6244e6337",
          "logical_id": "mc-31294289c7cb07c96f94ec7f",
          "row_sha256": "5143fe957f5a36f970ee0a5ac0ac846301dba7334f10fa650d10741daffd1274"
        },
        {
          "content_sha256": "8a589d73702b30a5f8d1f3566a57abc59ea739e33422929e57ed12f82c7e3c5f",
          "logical_id": "mc-8757b9f6e70151e0f6984d61",
          "row_sha256": "1ac556b36fd6092b146579112ed84824a7548b2c8e444113b8ffd15ed9ec3ef9"
        },
        {
          "content_sha256": "1ccbf4c5f932c490da5d8155228c6842d1b26dc02c73fcc2eee297c29a66a012",
          "logical_id": "mc-690767f768283d26c6271c5a",
          "row_sha256": "1a261f775631b17cebe23c565f052365d687695e0783a92c0ca71acff75f93a5"
        },
        {
          "content_sha256": "0c567a62375449a3d73038b20a27e2082094a3f6ac38f19c86d607f2ae4289bd",
          "logical_id": "mc-409e92184013cece6069baea",
          "row_sha256": "3b2dee31701655128931864844a82f23c1917acefbdf401216c3fd42b3122e66"
        },
        {
          "content_sha256": "ace1cabf4e14206d5b6d23cd1518ff8eec1533bcfca95f792598b89c7b3d3eef",
          "logical_id": "mc-c5bf630863ad40f35afaa9a4",
          "row_sha256": "65e6db6c9723134be518fc2812d3e2f68384d533e6b303e04551ba0d2741d678"
        },
        {
          "content_sha256": "e3374f38611c208faa8ec216f9ff4f00150a7b8a26a43114d687f45e8462a568",
          "logical_id": "mc-8b3156614883d3ed58facc2c",
          "row_sha256": "3ae43f747e97e88ef5a4c736b0d991b73beb161850256f4118ff1e14ebe08b2b"
        },
        {
          "content_sha256": "e23c995a53b48d3a58e6a3518d18525966e5379b4e5b1a1e73f974a80e97112d",
          "logical_id": "mc-5041b4749a815ed256ca914e",
          "row_sha256": "914e1e8a3e54b8191c0112854ddcb95c12432d9fc556f95c6957f8f96f233379"
        },
        {
          "content_sha256": "05bda9d54e8f5d987d1fbbc690b441b6afd03ef22d34cc4647757387a9f1b3c4",
          "logical_id": "mc-56b14f2e2270888b7db0a794",
          "row_sha256": "26aa3599ab72a49dbf19bb224869b8284cff85b4669bb554c6869463ebc5daa4"
        },
        {
          "content_sha256": "c642651878e82ebdb1e094ef30593be774d52eb72e8136631015381c7fc59c21",
          "logical_id": "mc-7a2b8dde2017ce97c129968a",
          "row_sha256": "9f363b2216ca3aeff443a85586ba67ccd54399de6b279ab6da78e5f22b94c611"
        },
        {
          "content_sha256": "0f7a3989e413288be1ec058e199ef2da7bd71590adcfca4aa34e67fe59e757cb",
          "logical_id": "mc-1c0584cb957cee3a2629ad34",
          "row_sha256": "4f53c2e50a36253269b1e67dc6f3d38fb778c8614cc16eb7bd7cde8b042ae11b"
        },
        {
          "content_sha256": "ae364cb560d13968fe54fcd9f9edbc2e9025e38b496c24c648322ba250e8ae90",
          "logical_id": "mc-0dded41e05aaaec7ff1dcf5e",
          "row_sha256": "f6864e5ff84f680174e65b99b4504342448753787758c460e91d285295782d33"
        },
        {
          "content_sha256": "7c9ea3ca38aa6a2eb817ae2ccf309671117627911d0ca2fb1b39b03b5f9ceaa8",
          "logical_id": "mc-2d820b27e07e1e50f11a0cad",
          "row_sha256": "f1a60de0d25112aa6350d344d0d35f7d5cbffd7db3a645fb3565a182eba7d655"
        },
        {
          "content_sha256": "ebb25314c99e708aed07add890e1da10e561ce06d79283d8b8d4c439258d5545",
          "logical_id": "mc-a50b796c2d19272f9e534f31",
          "row_sha256": "f607ef0289f724de2d99c94c7f56a7fea29acc356b3eba2c78d09a91337b8543"
        },
        {
          "content_sha256": "cf6c2e14339e7494c8f096beea156de5e3739b8180ed61f48b385388f414539f",
          "logical_id": "mc-87ec651f88fce5d9d7a20a58",
          "row_sha256": "64179c460644c73f49dea746a41716a17efe24c5a4a07d3a3e83090bd50b94f2"
        },
        {
          "content_sha256": "d845b378c7dd9964cb1c675985dda32a36412c23be13278464730b729b990932",
          "logical_id": "mc-7eb958bcfe8137ad5610eb65",
          "row_sha256": "34b41fb2f2ce7604fe97fdd47927772578881c52fe394f74667d446e121e1db0"
        },
        {
          "content_sha256": "c20b49ad844ab18255cac7614e10e5c70eac08978b6a68bfd82e7eadec533e17",
          "logical_id": "mc-60e5eabe7206b7eecd8194ca",
          "row_sha256": "000d67ad507a3e0fa0a769695decead19aa3b29fea6e6aa3383c22c3e45e9cf8"
        },
        {
          "content_sha256": "1c103bd7c8db2d4a09f255b529baf662f1222c592a8826eb527b4d12d58f935d",
          "logical_id": "mc-92948c07aa071915af8a9d1d",
          "row_sha256": "ace206016e29adfbcea80f7ee989420f2519f121b1fcb684c59bb9f0f26973eb"
        },
        {
          "content_sha256": "1e10f279785f23357c998274c9baabe593d00dba330fded7459469e70cfb2c5a",
          "logical_id": "mc-60337711491bb26fd6a0fc5a",
          "row_sha256": "1441dd5c6b96c1751e0957725e8299cba004f1dfdbe1d92ce69a41093dbf2209"
        },
        {
          "content_sha256": "ad9b1b07b19dd09f2897e95b0b301980638465fc44751f19c741072d9c0f4e64",
          "logical_id": "mc-4a0b029427535b3bd13b3151",
          "row_sha256": "15db0ffae0ded798530b864f0d1297da95b3cd5726d64f6de08d8c67b0340e80"
        },
        {
          "content_sha256": "a189db829d3ab6ebe41fced3639b95eb851ca1b98ecda047eb939f0b54952b18",
          "logical_id": "mc-76013dacd88d00aaaf9163f5",
          "row_sha256": "075adfaa14d7a0dabed8c371f2fb44eaa7131fc85c8a3c953c740dc446ffec0b"
        },
        {
          "content_sha256": "0bc7754b8ab9a29688008bc54173c29bc76792a9072c5c72b97f1f2f3b6a4c6c",
          "logical_id": "mc-d8e3e65238ac006bc0e9c895",
          "row_sha256": "5aacc36f0f2494b658f9059d511faa2698edd1fbbebb7e994650889df9a7eb8d"
        },
        {
          "content_sha256": "d3d1f52878e87742141c05e4d36771344be744a75bdd85bbccd346095cd7965c",
          "logical_id": "mc-1f8f9a157e092f249e1409c7",
          "row_sha256": "ddc545334f69123bef594d4720ca7951156752229f25a39f575506720112d805"
        }
      ],
      "sha256": "634f700fcd57f5e2beb70cbf604ccdc3a8f92d2b03da10e0424d3890c5e4659f",
      "sheet_name": "cards",
      "table_sha256": "396b6b0729118b544641d28ffcc1646318be45f28226f92f222f8567f1eb65fc",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 8804,
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
          "content_sha256": "d942196d5e9fc38f943bf1157ea6452ce0e518f7e0ffd3924f95719094357796",
          "logical_id": "mc-7fadec68d292af7ebc7a38a7",
          "row_sha256": "4e38f0e1e52e87ff1b3d19bea6551adc37e8592d6b4a67ba20f162d9b0a9496d"
        },
        {
          "content_sha256": "ea0a4926130a54d6db06488a45013d0043f4c9acd248107b22f7c5cb9ef263a4",
          "logical_id": "mc-9e911b985cc1ce276f1ebe37",
          "row_sha256": "c9fc493249d5d3c61d36c9e9e53d6b0cb07a1ce8e5a5bbc25837b18848370b67"
        },
        {
          "content_sha256": "b0cdfebaec41c0ece1a21d0226dd8791b6246a2f1ecaf1823abeb2863ff7b247",
          "logical_id": "mc-2a6dc333c733daf798c752ba",
          "row_sha256": "bfd4c9913069bc02c5f7422b73f3e510f7d2d1ef7a727251e95862ec0a5902de"
        }
      ],
      "sha256": "d1ff0139cfab9e7e74f50d4bb14788bc21e320d562d92d75cab2a821f0d7608a",
      "sheet_name": "cards",
      "table_sha256": "8bc9eb808c7ce55c7f28a65efd7f82a18ac28681009257db58cf057367570c14",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "1232b287292c52741989a3f06ed9a982bc2a6b2a7c62cf8075a0db029ae5f6c6",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "grouped-gemm-log",
      "path": "docs/triton-learning/logs/2026-10-09-grouped-gemm.md",
      "sha256": "b87bf95f5023a9facff31e35eb99ed4c8440d47406a3ee0ca57d4a0c4cc231c9",
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

导入文件：[triton-lesson-08-grouped-gemm-technical-qa.xlsx](triton-lesson-08-grouped-gemm-technical-qa.xlsx)（24 张卡）

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
