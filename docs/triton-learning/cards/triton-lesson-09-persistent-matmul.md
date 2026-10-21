---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "5b2c3b9ae7665e56dbe6a36992d5237239f77c332d9b2bf4a9bc93871abc9aff",
  "candidate_sha256": "ddb2680386a866598d356aa2045185d3ae38d80c30857f424259371a0e8a003e",
  "cards": [
    {
      "content_sha256": "2b11342e475f58d2f7caba23c8fc6a6ac18d8ccc3bb8046f5b4824ba9f0e082d",
      "content_summary": "flatten 合并两层循环让流水跨 tile：预热排空每 CTA 一次，tile 的 prologue 与 epilogue 仍每 tile 一次；条件不满足时静默忽略",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "持久化矩阵乘的 tile 循环加 flatten=true 后, 每个 cta 省掉什么、省不掉什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-ea7ddc8c39a8b54f9f0dfb43",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2e76f1a306ef41f4668ab7aa21c25a40db1343181e87188ae3a5e8ddd2caaf07",
      "content_summary": "flatten 后 prologue 里算的连续方向下标经 scf.if 传出、取不到声明，B 退回同步；在 K 循环里计算、写回另算一份可修复",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "b 按行主序存放时, 为什么 flatten 开后 b 的读入退回同步而 a 不受影响, 怎样修?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-aef5d803d3de8f31fe6e6ca7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1bbdc0517462aef71b03e549bee43daa9fefbd608ee64d4a177ce57be17c5183",
      "content_summary": "多 CTA 驻留时调度器切换 warp 让张量核心不闲；大块一 SM 一 CTA 时等待成为真空档",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "多个 cta 驻留时每个 tile 的固定成本怎样被掩盖, 大块时为什么掩盖不了?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-15ea16898338952dfbc21e77",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "27b66b0f7a779d421fa855637d37748d11893e4277888d007ac1eea28774afe2",
      "content_summary": "flatten 调整一条执行顺序内的先后，专用化增加执行顺序；乘加与 epilogue 能否重叠取决于乘加指令；Triton 3.7.1 的 sm_90 上二者不能同开",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为了不在 tile 边界停顿, flatten 与 warp 专用化在机制上的根本区别和各自代价"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7ed00a8f3615f0f2d0b036f5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "05c36fd5b448b8848acb6849f06b4268fe3f43dcf5137166cd50c9d5ba5dc27a",
      "content_summary": "M、N 越界改下标只需地址合法；K 越界必须读成 0；不处理是未定义行为",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "分块矩阵乘里 m、n 方向的越界下标可以改成 0, k 方向为什么不行; m、n 方向为什么又必须处理?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-419812ab9e3c766b37ca840b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "049d4e5e4857bcef49581d4eae7cb43a38d12eec253e789e8566a62ef87c25ba",
      "content_summary": "tl.where 的 gcd 规则让取值连续度降到 1；保守结论，完整 tile 的值仍连续；这里的连续是取值连续，不是存储连续",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "tl.where 之后编译器为什么认定下标的取值连续度只剩 1"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-558ab777fd4b7293a5864b30",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6542bbb403e6140fbe36f4c0a366de7849a6a3bd25e9e24715b15b72b6851daa",
      "content_summary": "受控测量：固定配置、两个开关、交替测与轮内相除、预先判据、比值拆因子",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "怎样设计测量, 才能把持久化矩阵乘的速度差别归到具体的改动上"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-8444f39ef05660455739c1de",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b75357e343e1e735c84c29686310659fecd6a219e0439d4ab6b86a9c02b3c6d1",
      "content_summary": "异步拷贝不等于有提前量；看 ttg.async_wait 的 num 是否大于 0",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "读入已经是异步拷贝时, 怎样从 ttgir 判断它是否真的提前发出"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-825d27f5f1d09de05c268fe5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8faf178ddbfc9029d07bbd09e7324e188fde4a6dfcb43152358158023d4d335d",
      "content_summary": "网格与步长不一致导致重复计算且测试发现不了；用 tl.num_programs(0) 取步长",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "持久化矩阵乘的网格与领取 tile 的步长不一致会怎样, 怎样避免"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7634d201cf2302a81d4f90d9",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4501fb68124ba14fe33e59de840c5b3f9ca023536832f4657635750844bb390a",
      "content_summary": "NVIDIA 后端确认 flatten 生效：scf.if 出现为主证据，排空移出循环，共享内存只作辅助；gfx942 上表现不同；无报错不算证据",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "怎样确认 flatten 真的生效, 而不是被编译器静默忽略"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-34e5ddded2a878f08c4e269a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3a7fb393bd4826cb01c3a12598524cfa7b5c14bb09bce65e8346a84f60bb72b3",
      "content_summary": "flatten 后 epilogue 执行时 tile_id 已前进；tile_id_c 打断依赖、规避 Blackwell 缺陷；不写时编译器自带一份旧值，更费寄存器，sm_100 上是否触发缺陷未验证",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "开了 flatten 的持久化 kernel 为什么给 epilogue 单独维护一个 tile 游标, 不写会怎样"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4ad67e4bf89b9d1fccf36b84",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b3017b79844114c72f2249294ce1dbad7699291d8d516f27160d28fe2b2c9101",
      "content_summary": "B 按 [N,K] 存放让操作数沿 K 连续；[K,N] 摆法 fp16 在 sm_120 多转置读取，fp8 在 sm_90 的 wgmma 上要经寄存器重排；sm_100 上 fp8 两种摆法相同",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "ptx-isa",
          "version": "9.4"
        },
        "recall_target": "tma 版矩阵乘为什么把 b 按 [n, k] 存放, fp16 与 fp8 有何不同"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-aa14c9d821c28308d764ec8e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0ff9097b53e553444059e3417c0a65e533d5d93ad9781590248ad8b382c1dc2c",
      "content_summary": "张量核心让数据离开寄存器是为了解放线程：寄存器紧、逐条喂数据、计算绑定",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "新一代张量核心为什么让操作数和累加器离开线程的寄存器"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-28f897ad8a5fe0e4a3ea14c6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fbcd4c9aeb7ec286559883f3e6b7d2681f43f82ade7d7a156e1a8055bb84773d",
      "content_summary": "where 后的连续性声明在边界 tile 里不成立却安全的三个条件",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "tl.where 之后的连续性声明在边界 tile 里不成立, 为什么不会读错或越界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-8535ff3240e81707b3cc7d0f",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5d5b5d55e4ec303e6267d2739edf825af98c3ffbe612629d2504e8dde902d315",
      "content_summary": "max_contiguous 与 multiple_of 分别保证连续与对齐，缺一不可；一次搬多少取二者较小者",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "tl.max_contiguous 与 tl.multiple_of 各声明什么, 为什么缺一不可"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0bce910539e203eaf3cf37c9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2824eb20ba6cbb5ec292068ee3814e8a458ddd7e4e3bc434e410ed207c6ecd60",
      "content_summary": "Triton 发射时的整数与指针特化：等于 1 当常量、16 的倍数挂 divisibility、写进缓存键",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton 发射 kernel 时对整数与指针实参做了哪些特化"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-813451003ac19a697e423417",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d35b46d3e34cf3669a27f6e3ffefb29c426d7ebf7ec9d63a3bb0bcb5d363756a",
      "content_summary": "持久化直接省 CTA 发射与退出；prologue/epilogue 的重叠要靠 flatten 或专用化",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "持久化相对逐 tile 发射直接省掉什么, prologue 与 epilogue 的重叠是否随之发生?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f8281736b7d9c4060a33773e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9d4c1bc30f5cc8d92b7fdbc7a12be3dbabe6d0d706f50935a53c508ffb8e5841",
      "content_summary": "共享内存超限抛 OutOfResources、autotune 记无穷大；会溢出的是寄存器",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton kernel 的共享内存超过设备上限时会发生什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-077f37d68441b7d58f9d55cb",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fa3f1db89cad8c45f07fd02239ab43a55fedd48bee86a8df46dae3775f67cc66",
      "content_summary": "输入槽数取决于槽被占用的时长：取进寄存器则 S−1，就地读则 S；提前量两代相同，共享内存多、寄存器少是操作数换了地方",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "同样的 num_stages, 为什么 sm_90 的 wgmma 每个操作数比 sm_89 多一个输入槽?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d2a126cb974f004a3189ba20",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1feb4991e1f94ee1c0618681f3af005266fe92aad7e067eb8691f8c53fa21610",
      "content_summary": "tile 边界停顿的根因是一条执行顺序里读入排在 epilogue 之后，不是算地址",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "不合并、不专用化的持久化矩阵乘为什么在 tile 边界停顿?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7bcbbcfc3af2613f2cc99704",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7e217b1933edf0c0d9bbce6b60918abf1dafbc90a34ea3fc783195a173111f84",
      "content_summary": "先 where 后算 mask 使 mask 恒真，K 越界位置读入真实数据进入求和",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "k 方向先用 tl.where 把越界下标改成 0 再算 mask, 为什么结果出错?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-96458a7ae787cb0ffdd97dec",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0380710b240e0008e2b2018ff9d1bad94020c30500e98f6ef4f58bf9c286ca8c",
      "content_summary": "改写后的行号把越界写回引到第 0 行重复写入，值相同所以碰巧正确",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "写回的 mask 恒为真时, m、n 不整块的测试为什么仍然通过?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b6e1c7bc61a09c21af41c0c3",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "19261551184aeb4517adcaaf3130bc89af6db56a7bbebaa41b62cbbaa1ae6d12",
      "content_summary": "声明要落在操作数的连续方向：A 看 K、B 看 N",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "读行主序 b 的矩阵乘, 连续性声明应加在哪个方向的下标上?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-67daad7e80dfa27e69ab9bec",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2618ea07333cd1b9a203ea36002c9cb2bbdb22d27d58bc7dc690b75ee373cded",
      "content_summary": "合并后的两个 scf.if 是 tile 的 prologue 与 epilogue（每 tile 一次），不是流水的预热排空（合并后每 CTA 一次）",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "flatten 合并循环后出现的两个 scf.if 包住的是什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7c92dea413044da374f93684",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1242c6e81f34cc9b4e4979410778ffae9b062e5a67be40ebdbc7866174d573c7",
      "content_summary": "声明是贴在定义值的操作上的标签，挪声明无效，要挪值的计算",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "flatten 下修复 b 的连续性声明丢失时, 应把什么挪进 k 循环?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-98dbd9178f8edfe9b73bd740",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2c890ce9081ada13c099329d961dc9f7caf38d51f7ad935f0191595f44010304",
      "content_summary": "判据只给方向；解释要拆因子，说明支持、不支持与回答不了的部分",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "实测按判据支持预测后, 对结果的解释应包括什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d794901c2b34c57696fdab27",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e648da90f7746d5c6e8b39383552cc6df30ba579c07b428be43f67735db38a79",
      "content_summary": "口述持久化与 flatten 的机制、收益、代价与确认方法",
      "dependency_content_sha256": {
        "mc-34e5ddded2a878f08c4e269a": "4501fb68124ba14fe33e59de840c5b3f9ca023536832f4657635750844bb390a",
        "mc-4e3c913fd0957cde68b238e3": "d930edfed08ca8ffeb96ceb9200a3d70206579db4d5e43b7caa4a8ba40151720",
        "mc-7634d201cf2302a81d4f90d9": "8faf178ddbfc9029d07bbd09e7324e188fde4a6dfcb43152358158023d4d335d",
        "mc-ea7ddc8c39a8b54f9f0dfb43": "2b11342e475f58d2f7caba23c8fc6a6ac18d8ccc3bb8046f5b4824ba9f0e082d",
        "mc-f8281736b7d9c4060a33773e": "d35b46d3e34cf3669a27f6e3ffefb29c426d7ebf7ec9d63a3bb0bcb5d363756a"
      },
      "depends_on": [
        "mc-34e5ddded2a878f08c4e269a",
        "mc-4e3c913fd0957cde68b238e3",
        "mc-7634d201cf2302a81d4f90d9",
        "mc-ea7ddc8c39a8b54f9f0dfb43",
        "mc-f8281736b7d9c4060a33773e"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清持久化矩阵乘与 flatten 改了什么、省掉什么、代价与确认方法。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-000831b41e4c256b4db5dcad",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已依据更新后的 01、09、10 与新增的 flatten-shared-memory-cost、21 复核参考回答与五个锚点，删去无子卡支撑的“为何需要”，确认证据限定为 NVIDIA。"
      },
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3611444b232935d603cb5d922fdf060a37320c6f64d48dc75861d7b1b538ec6a",
      "content_summary": "口述四代目标上操作数与累加器的位置、数据离开寄存器的原因与代价、专用化的作用",
      "dependency_content_sha256": {
        "mc-28f897ad8a5fe0e4a3ea14c6": "0ff9097b53e553444059e3417c0a65e533d5d93ad9781590248ad8b382c1dc2c",
        "mc-7ed00a8f3615f0f2d0b036f5": "27b66b0f7a779d421fa855637d37748d11893e4277888d007ac1eea28774afe2",
        "mc-d2a126cb974f004a3189ba20": "fa3f1db89cad8c45f07fd02239ab43a55fedd48bee86a8df46dae3775f67cc66"
      },
      "depends_on": [
        "mc-28f897ad8a5fe0e4a3ea14c6",
        "mc-7ed00a8f3615f0f2d0b036f5",
        "mc-d2a126cb974f004a3189ba20"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清四代目标上乘加的操作数与累加器放在哪、为什么让数据离开寄存器及其代价, 以及专用化解决什么。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-092763e394c5c80cab1be653",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "383cdb12103becdce2b9f8269e95c47cde0e3c546ec438bbdf0bb5ef5ac4c19f",
      "content_summary": "口述行主序 B 保住异步拷贝与提前量的做法与诊断",
      "dependency_content_sha256": {
        "mc-0bce910539e203eaf3cf37c9": "5d5b5d55e4ec303e6267d2739edf825af98c3ffbe612629d2504e8dde902d315",
        "mc-558ab777fd4b7293a5864b30": "049d4e5e4857bcef49581d4eae7cb43a38d12eec253e789e8566a62ef87c25ba",
        "mc-825d27f5f1d09de05c268fe5": "b75357e343e1e735c84c29686310659fecd6a219e0439d4ab6b86a9c02b3c6d1",
        "mc-8535ff3240e81707b3cc7d0f": "fbcd4c9aeb7ec286559883f3e6b7d2681f43f82ade7d7a156e1a8055bb84773d",
        "mc-aef5d803d3de8f31fe6e6ca7": "2e76f1a306ef41f4668ab7aa21c25a40db1343181e87188ae3a5e8ddd2caaf07"
      },
      "depends_on": [
        "mc-0bce910539e203eaf3cf37c9",
        "mc-558ab777fd4b7293a5864b30",
        "mc-825d27f5f1d09de05c268fe5",
        "mc-8535ff3240e81707b3cc7d0f",
        "mc-aef5d803d3de8f31fe6e6ca7"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清行主序 b 怎样在 flatten 开关下都保住 16 字节、提前发出的异步拷贝, 以及怎样诊断。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-10ec2eb178242ba25b686071",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已依据更新后的 02（写回另算一份）、06（并入取值与存储连续的区分）、14、15 复核参考回答与锚点。"
      },
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3265e40ce9337e83c4c199c5c635dcdcf6ad89b91631dd5b449d2367b9c37b4f",
      "content_summary": "口述 M1 的测量设计、结果与结论边界",
      "dependency_content_sha256": {
        "mc-8444f39ef05660455739c1de": "6542bbb403e6140fbe36f4c0a366de7849a6a3bd25e9e24715b15b72b6851daa",
        "mc-d794901c2b34c57696fdab27": "2c890ce9081ada13c099329d961dc9f7caf38d51f7ad935f0191595f44010304",
        "mc-f062131fde8aa04f73b8163b": "04094838b49b0fc7511ad6abbce4bea8ba00fe92a768b727e9cb7629218afc1f"
      },
      "depends_on": [
        "mc-8444f39ef05660455739c1de",
        "mc-d794901c2b34c57696fdab27",
        "mc-f062131fde8aa04f73b8163b"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清怎样检验“持久化的优势随 k 增大而减小”, 结果说明了什么、没说明什么。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-b2edcf5bb5fe74b429490050",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已依据更新后的 07、30 复核参考回答，结果只保留量级。"
      },
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "622206aff1a88fcfce67f65b548aa424409a60ef368c579ceb77495f9f2528eb",
      "content_summary": "拆半省半个输出块，能否换多一级流水取决于超出上限的量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "epilogue 拆半什么时候能换来多一级流水"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4ef123242d7aa007c70afbd1",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "be51001da1c5f45d9b7baf314ae7aed23dd1fc7f78d3762b3553b92c693aa010",
      "content_summary": "Triton 编译的 SSA 作用域：if 内首次赋值的名字在 if 后不存在，解释器发现不了",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "手写合并循环在解释器里能跑、编译时报 nameerror 的原因"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-0c26d31e310e78360921c5a4",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "04094838b49b0fc7511ad6abbce4bea8ba00fe92a768b727e9cb7629218afc1f",
      "content_summary": "持久化本身一列含分派、固定工作、调度方式三项，测量只给净和",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "“每个 cta 一个 tile”对“持久 cta”的时间比里包含哪几项变化"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f062131fde8aa04f73b8163b",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fe37df5f69bc2e98edd3810af2479ea39e0294ab3e5026bb9cac17d29a2d9bb3",
      "content_summary": "autotune 下设备侧描述符更省事；主机侧要 pre_hook 改写块形状",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "autotune 下主机侧与设备侧描述符哪个更省事, 各自代价是什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-422574c717b612e2fbb572ff",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3d06d3ff71c2043bcfd9eb8c76ffb2571b531b006524a9b4cce68b6b551bdbcf",
      "content_summary": "资源用量在无溢出时主要通过驻留数影响速度；先算驻留数，驻留数不变就不是变慢的主因",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "资源用量的差别能否解释一个 kernel 版本变慢, 应该先算什么"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-ad2121831fdfbf782053ad16",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ec3f011b63f603178a395d690cbdedfa4647e62ada78fb019a994781ace085f8",
      "content_summary": "持久化由手写 tile 循环与包装函数的网格决定，不是编译器变换；flatten 开时 tile 循环并入合并循环",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "从编译产物怎样确认持久化已经实现?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-2ef43c89b6814d0b0ab746d9",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c125ffb88a607ebe890d47e7ff6ee46697d93c6340457af42e2fbcbb541f4b03",
      "content_summary": "迁到无 cp.async/TMA 的后端：持久化原样保留，flatten 收益取决于读入能否在后台进行，TMA/TMEM/专用化随硬件消失；gfx942 只编译观察",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "持久化加 flatten 的矩阵乘移到没有 cp.async 与 tma 的后端后, 哪些收益还在, flatten 的收益取决于什么"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e8e1dc54713a51cc0d67c79c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a7bd9c580471db114d3de9532acec0c2757e9e90967cf634306535772483e3ae",
      "content_summary": "持久化与 flatten 的收益只来自 tile 间隔的占比：tile 不多于 SM 时为零，K 越大、每 CTA tile 越少收益越小，大 K 时 flatten 可能是净代价",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "持久化与 flatten 什么时候不划算, 收益怎样随 tile 数和 k 变化"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1228d96c241676355fd4702e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d930edfed08ca8ffeb96ceb9200a3d70206579db4d5e43b7caa4a8ba40151720",
      "content_summary": "flatten 后 epilogue 的换布局中转借不到仍被占用的输入槽，共享内存多一档",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "flatten 合并后共享内存为什么多出一块, 不合并时为什么不需要"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4e3c913fd0957cde68b238e3",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4295f3cff5452e838c6f644bd0bc07d85f186c25a34e582d97779109846266d5",
      "content_summary": "Triton 3.7.1 的 Hopper 专用化 pass 遇带 else 的 scf.if 即放弃，合并必然产生它，故 sm_90 上不能同开；关 flatten 不丢跨 tile 预取",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton 3.7.1 的 sm_90 上 warp 专用化为什么不能与 flatten 同时开"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3c32a5db11bcb2e15d889434",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "547880f1194477b5bd4b70e529d969a023e1528e91ab6f790b88101969bf37ab",
      "content_summary": "sm_100 写回：TMA 只在显存与共享内存间搬，累加器经 tcgen05.ld 读回寄存器、写入共享内存再由 TMA 写出",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "ptx-isa",
          "version": "9.4"
        },
        "recall_target": "sm_100 上累加器在 tmem 时写回 c 要经过哪些存储, tma 为什么不能直接从 tmem 搬"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-44f6cbbb5a69a02bf45a7522",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "bb59117ebc9bb6b624f3c24604989c7d313841ac6179d8d9478812f23456d415",
  "manifest_payload_sha256": "517d44f96ca5f191461717fa35972f6ba97f23d9a43900e5cc9e2f60dbd2de6c",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 21009,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-09-persistent-matmul-correction.xlsx",
      "row_count": 12,
      "rows": [
        {
          "content_sha256": "d35b46d3e34cf3669a27f6e3ffefb29c426d7ebf7ec9d63a3bb0bcb5d363756a",
          "logical_id": "mc-f8281736b7d9c4060a33773e",
          "row_sha256": "8b207c991083323c7c4a495e6a0c5ab9ed33945f83618241d0ae9daa7b17a96b"
        },
        {
          "content_sha256": "9d4c1bc30f5cc8d92b7fdbc7a12be3dbabe6d0d706f50935a53c508ffb8e5841",
          "logical_id": "mc-077f37d68441b7d58f9d55cb",
          "row_sha256": "be7c41e84b30a80b4f60f45ef91e9d3e521dcf9c17e89fb618f65e01f4084bd2"
        },
        {
          "content_sha256": "fa3f1db89cad8c45f07fd02239ab43a55fedd48bee86a8df46dae3775f67cc66",
          "logical_id": "mc-d2a126cb974f004a3189ba20",
          "row_sha256": "76010f20737f1c93939d7e9f387512aa4a82e62bb2b72cad722f1e6c9ea7434a"
        },
        {
          "content_sha256": "1feb4991e1f94ee1c0618681f3af005266fe92aad7e067eb8691f8c53fa21610",
          "logical_id": "mc-7bcbbcfc3af2613f2cc99704",
          "row_sha256": "d6149283c6e913875cd773d0a0e62facab3a42c3ca0ad95d318816757d2fa12b"
        },
        {
          "content_sha256": "7e217b1933edf0c0d9bbce6b60918abf1dafbc90a34ea3fc783195a173111f84",
          "logical_id": "mc-96458a7ae787cb0ffdd97dec",
          "row_sha256": "b8f93aa79952e999bca474caf8ce178b320fdfe75381351b0a63562d2c08601b"
        },
        {
          "content_sha256": "0380710b240e0008e2b2018ff9d1bad94020c30500e98f6ef4f58bf9c286ca8c",
          "logical_id": "mc-b6e1c7bc61a09c21af41c0c3",
          "row_sha256": "26e65699812e9bfc1ab04f3e7b76a95903e67293b35bbe47b70a685fcb25e015"
        },
        {
          "content_sha256": "19261551184aeb4517adcaaf3130bc89af6db56a7bbebaa41b62cbbaa1ae6d12",
          "logical_id": "mc-67daad7e80dfa27e69ab9bec",
          "row_sha256": "8586b824036235dc881ba7822a8df56d669fa4c87b6a0add6188b18d32bcd0d3"
        },
        {
          "content_sha256": "2618ea07333cd1b9a203ea36002c9cb2bbdb22d27d58bc7dc690b75ee373cded",
          "logical_id": "mc-7c92dea413044da374f93684",
          "row_sha256": "48ae410087373172921ad1349fca4e4b880a7d26834b7397700133c5b75e8f62"
        },
        {
          "content_sha256": "1242c6e81f34cc9b4e4979410778ffae9b062e5a67be40ebdbc7866174d573c7",
          "logical_id": "mc-98dbd9178f8edfe9b73bd740",
          "row_sha256": "32b4eaaef6e9827fcaa1e75be70f6d12a05dacf46c2ca18e9628a63561a16a57"
        },
        {
          "content_sha256": "2c890ce9081ada13c099329d961dc9f7caf38d51f7ad935f0191595f44010304",
          "logical_id": "mc-d794901c2b34c57696fdab27",
          "row_sha256": "686ce2d207a9ea4957d90d4391d672babdd959333bffa8165b9dd13b7979f703"
        },
        {
          "content_sha256": "fe37df5f69bc2e98edd3810af2479ea39e0294ab3e5026bb9cac17d29a2d9bb3",
          "logical_id": "mc-422574c717b612e2fbb572ff",
          "row_sha256": "332a0bcecfb16f7b17a8a898f047ee8241357537e121bbfa54c41df308f16def"
        },
        {
          "content_sha256": "ec3f011b63f603178a395d690cbdedfa4647e62ada78fb019a994781ace085f8",
          "logical_id": "mc-2ef43c89b6814d0b0ab746d9",
          "row_sha256": "c85ea4558cebeb78224c8048c0835ead3425748f5561687a2cb99e6b9c1d76d1"
        }
      ],
      "sha256": "ba2205d485c980c89339e1910428c73870684db289cfbb8b4b9e80795133966e",
      "sheet_name": "cards",
      "table_sha256": "7fdcea511fba64ea3f6ac4976cbd37a0bb141b3e74ffb3b1a169430e1f79984d",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 42846,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-09-persistent-matmul-technical-qa.xlsx",
      "row_count": 25,
      "rows": [
        {
          "content_sha256": "2b11342e475f58d2f7caba23c8fc6a6ac18d8ccc3bb8046f5b4824ba9f0e082d",
          "logical_id": "mc-ea7ddc8c39a8b54f9f0dfb43",
          "row_sha256": "b8bd692e78f11770b440cb1b84566fe2561d0742d6a8e4680c8fd571a15e4536"
        },
        {
          "content_sha256": "2e76f1a306ef41f4668ab7aa21c25a40db1343181e87188ae3a5e8ddd2caaf07",
          "logical_id": "mc-aef5d803d3de8f31fe6e6ca7",
          "row_sha256": "9e87a921f14122844d9dde5d7e0f98547e0b118f3995d78c446bedde72981f32"
        },
        {
          "content_sha256": "1bbdc0517462aef71b03e549bee43daa9fefbd608ee64d4a177ce57be17c5183",
          "logical_id": "mc-15ea16898338952dfbc21e77",
          "row_sha256": "0c87a8984af7f7d7c41b81c8c3184189cd6d02f641188cf0d053009a366104dd"
        },
        {
          "content_sha256": "27b66b0f7a779d421fa855637d37748d11893e4277888d007ac1eea28774afe2",
          "logical_id": "mc-7ed00a8f3615f0f2d0b036f5",
          "row_sha256": "38f2867914c5c2cfd45b83e50694a9cf02a501e1f27dc23db79b80a0d40c8652"
        },
        {
          "content_sha256": "05c36fd5b448b8848acb6849f06b4268fe3f43dcf5137166cd50c9d5ba5dc27a",
          "logical_id": "mc-419812ab9e3c766b37ca840b",
          "row_sha256": "e005b8188f86f8306b041be81f2ac705e9b0c71a3f487dbe72c6fc1d461dc79b"
        },
        {
          "content_sha256": "049d4e5e4857bcef49581d4eae7cb43a38d12eec253e789e8566a62ef87c25ba",
          "logical_id": "mc-558ab777fd4b7293a5864b30",
          "row_sha256": "c4aea9fec7b9e8fdc8315be90634c277ad2a35d716d46e66a8ebd0c79220a545"
        },
        {
          "content_sha256": "6542bbb403e6140fbe36f4c0a366de7849a6a3bd25e9e24715b15b72b6851daa",
          "logical_id": "mc-8444f39ef05660455739c1de",
          "row_sha256": "c7bd9ab60cdfd2f2a981cfc5afa7d62bb27f8bd265ba98297cf72a676dd07686"
        },
        {
          "content_sha256": "b75357e343e1e735c84c29686310659fecd6a219e0439d4ab6b86a9c02b3c6d1",
          "logical_id": "mc-825d27f5f1d09de05c268fe5",
          "row_sha256": "21bb25390e61a1d91845b5a4ac6514ec85f3270303568c3fda4c3935c99928d3"
        },
        {
          "content_sha256": "8faf178ddbfc9029d07bbd09e7324e188fde4a6dfcb43152358158023d4d335d",
          "logical_id": "mc-7634d201cf2302a81d4f90d9",
          "row_sha256": "f6d1ba7dc03520c095405b742f65fe09bb33fb252028b66d016334f4c28567d6"
        },
        {
          "content_sha256": "4501fb68124ba14fe33e59de840c5b3f9ca023536832f4657635750844bb390a",
          "logical_id": "mc-34e5ddded2a878f08c4e269a",
          "row_sha256": "5b26a7b1a1360b2fecbe7cc8a8bf36d03bbf16f3e729bf57c0631a58a30cd972"
        },
        {
          "content_sha256": "3a7fb393bd4826cb01c3a12598524cfa7b5c14bb09bce65e8346a84f60bb72b3",
          "logical_id": "mc-4ad67e4bf89b9d1fccf36b84",
          "row_sha256": "bb4173e4669819f49074d2374783fe61906148d5e471be4c4057c8b8560abf7b"
        },
        {
          "content_sha256": "b3017b79844114c72f2249294ce1dbad7699291d8d516f27160d28fe2b2c9101",
          "logical_id": "mc-aa14c9d821c28308d764ec8e",
          "row_sha256": "0c53cb0cfa541046f30c6dd72411b4114c5ee52a017b969682ef6e7734c725bf"
        },
        {
          "content_sha256": "0ff9097b53e553444059e3417c0a65e533d5d93ad9781590248ad8b382c1dc2c",
          "logical_id": "mc-28f897ad8a5fe0e4a3ea14c6",
          "row_sha256": "b1d38b9c172fe5bf38b7182c1b0df93f15a46e48802afe9aaad6f06fd64259e1"
        },
        {
          "content_sha256": "fbcd4c9aeb7ec286559883f3e6b7d2681f43f82ade7d7a156e1a8055bb84773d",
          "logical_id": "mc-8535ff3240e81707b3cc7d0f",
          "row_sha256": "d1b29716549f50593cb29247a47f9798baa0bb599e7987ea87142a992e57b9a7"
        },
        {
          "content_sha256": "5d5b5d55e4ec303e6267d2739edf825af98c3ffbe612629d2504e8dde902d315",
          "logical_id": "mc-0bce910539e203eaf3cf37c9",
          "row_sha256": "fc11b51f5c8a055b82a537d22fb4660acea2cb34caadfeeb4626e6bfeb99867a"
        },
        {
          "content_sha256": "2824eb20ba6cbb5ec292068ee3814e8a458ddd7e4e3bc434e410ed207c6ecd60",
          "logical_id": "mc-813451003ac19a697e423417",
          "row_sha256": "ef9d04b29de18dad1643523fa327218033422c8acc0fcdfc204da292f95e2bcb"
        },
        {
          "content_sha256": "622206aff1a88fcfce67f65b548aa424409a60ef368c579ceb77495f9f2528eb",
          "logical_id": "mc-4ef123242d7aa007c70afbd1",
          "row_sha256": "a8021d6bd00f0a57de15a3d17e7d169859021489f4fbdfeeefe8a52b176644d9"
        },
        {
          "content_sha256": "be51001da1c5f45d9b7baf314ae7aed23dd1fc7f78d3762b3553b92c693aa010",
          "logical_id": "mc-0c26d31e310e78360921c5a4",
          "row_sha256": "bfba0b61e33e20b5d70734ce529bfeb98f0cff8706f83a2b7d5c45642b889965"
        },
        {
          "content_sha256": "04094838b49b0fc7511ad6abbce4bea8ba00fe92a768b727e9cb7629218afc1f",
          "logical_id": "mc-f062131fde8aa04f73b8163b",
          "row_sha256": "46df774d4c6d614dcafbf3e9d001b1454f6bc282b58f0a73cbbd95f4b7ab67f0"
        },
        {
          "content_sha256": "3d06d3ff71c2043bcfd9eb8c76ffb2571b531b006524a9b4cce68b6b551bdbcf",
          "logical_id": "mc-ad2121831fdfbf782053ad16",
          "row_sha256": "2bc18b15c10a2e3b02d4ee9069e20134efc04ed2ced27fa9701aabc5d25da1f6"
        },
        {
          "content_sha256": "c125ffb88a607ebe890d47e7ff6ee46697d93c6340457af42e2fbcbb541f4b03",
          "logical_id": "mc-e8e1dc54713a51cc0d67c79c",
          "row_sha256": "96108bfdbdfed3b38f382e28fd39bb281c3263521025cdd769e594859a657e51"
        },
        {
          "content_sha256": "a7bd9c580471db114d3de9532acec0c2757e9e90967cf634306535772483e3ae",
          "logical_id": "mc-1228d96c241676355fd4702e",
          "row_sha256": "229524a0080a6cc83d62d770fa5cabc0260ebb602559e1c1349b967c7aa65992"
        },
        {
          "content_sha256": "d930edfed08ca8ffeb96ceb9200a3d70206579db4d5e43b7caa4a8ba40151720",
          "logical_id": "mc-4e3c913fd0957cde68b238e3",
          "row_sha256": "cf000d78af4d07cad9a683e576d8bfe37f543a1fdbc9f854569d43c6f54a45e2"
        },
        {
          "content_sha256": "4295f3cff5452e838c6f644bd0bc07d85f186c25a34e582d97779109846266d5",
          "logical_id": "mc-3c32a5db11bcb2e15d889434",
          "row_sha256": "619e6a041a43fb3e2313133b9f5334659ca3138778402bf8712bd72b900177ed"
        },
        {
          "content_sha256": "547880f1194477b5bd4b70e529d969a023e1528e91ab6f790b88101969bf37ab",
          "logical_id": "mc-44f6cbbb5a69a02bf45a7522",
          "row_sha256": "570b42be2f37763dac8c0d414c9556a5d5cb3eb6f106e255c0bd4596dbc6297f"
        }
      ],
      "sha256": "8ed13bc9e8807a66f0a5039ebd5137472a0233aee3e5f06ec69cb5154b9d7495",
      "sheet_name": "cards",
      "table_sha256": "7fb1d359d5db697c39f265805bb67bb3d97d6823fa4662a158d9d2ef96492900",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 9652,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-09-persistent-matmul-oral.xlsx",
      "row_count": 4,
      "rows": [
        {
          "content_sha256": "e648da90f7746d5c6e8b39383552cc6df30ba579c07b428be43f67735db38a79",
          "logical_id": "mc-000831b41e4c256b4db5dcad",
          "row_sha256": "991b5e801a1047ebbbd70fa4d06a4d34cdb66e098b28cf1d7c96d3e1d5748c69"
        },
        {
          "content_sha256": "3611444b232935d603cb5d922fdf060a37320c6f64d48dc75861d7b1b538ec6a",
          "logical_id": "mc-092763e394c5c80cab1be653",
          "row_sha256": "42331d18cbd4cf38cd502443d45e2dc8a6297d7233a43dcee686d4091c08fe4b"
        },
        {
          "content_sha256": "383cdb12103becdce2b9f8269e95c47cde0e3c546ec438bbdf0bb5ef5ac4c19f",
          "logical_id": "mc-10ec2eb178242ba25b686071",
          "row_sha256": "feba5159627161b8b0adf743676ad172d1dda844026ce75d58e5b6d440211773"
        },
        {
          "content_sha256": "3265e40ce9337e83c4c199c5c635dcdcf6ad89b91631dd5b449d2367b9c37b4f",
          "logical_id": "mc-b2edcf5bb5fe74b429490050",
          "row_sha256": "14b6cb77704a7083d6f57f0510e210111d81530ae5b8bf98f4f5356de4486186"
        }
      ],
      "sha256": "811d6fbff1eecfd86cd74a0bba91495d77647d1d38117de3f57be4bba7926605",
      "sheet_name": "cards",
      "table_sha256": "ff260b50dd399721d8fb87288eafad4d655c74e15b68a8ecf07f6f4f64162f9a",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "41bf847dabe909df037946d4fba3d97ed50f77d91262d5de0c04e489fb9f1bc1",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "persistent-matmul-log",
      "path": "docs/triton-learning/logs/2026-10-14-persistent-matmul.md",
      "sha256": "39c7eb19c1bff2b0f45e7abe31df12c068ef1392da1d197ccafbfa053d493743",
      "summary": "10/10–10/14：持久化矩阵乘、flatten、搬与算、M1 测量、取值连续与两条声明的纠错与答疑"
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

导入文件：[triton-lesson-09-persistent-matmul-correction.xlsx](triton-lesson-09-persistent-matmul-correction.xlsx)（12 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-09-persistent-matmul-technical-qa.xlsx](triton-lesson-09-persistent-matmul-technical-qa.xlsx)（25 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-09-persistent-matmul-oral.xlsx](triton-lesson-09-persistent-matmul-oral.xlsx)（4 张卡）
