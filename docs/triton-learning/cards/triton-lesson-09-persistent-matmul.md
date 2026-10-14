---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "43d2a9fbbe6b711910beac558c7ca79a366ec09e93a10452756b1c94bd50c18c",
  "candidate_sha256": "f8033b2bbfb4a16934cf11554bc306c7a3107c806f9eadd7ad41d82e7170166b",
  "cards": [
    {
      "content_sha256": "5ab9ff5fa7d155e5af0773e69bd3de396226691626bb59429f678f1ad3263b40",
      "content_summary": "flatten 合并两层循环让流水跨 tile；省预热排空不省写回；多占共享内存；条件不满足时静默忽略",
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
        "recall_target": "持久化矩阵乘的 tile 循环加 flatten=true 后, 编译器做了什么, 省掉什么、省不掉什么、代价是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a723253b09367bafdfc916a9",
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
      "content_sha256": "1249dd6ed25671f4e45b32784771506743aa2acfec22a7488e688f65e56dd4f1",
      "content_summary": "flatten 后 prologue 里算的连续方向下标经 scf.if 丢失声明，B 退回同步；在 K 循环里计算可修复",
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
      "content_sha256": "183e9219cb5cc74ab45702406b9ab0a67500de09f41774e3d7bf3ea59c96ffe8",
      "content_summary": "flatten 调整一条执行顺序内的先后，专用化增加执行顺序；代价分别是中转缓冲与更多 warp、屏障、缓冲",
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
      "content_sha256": "24656ea44eb6ce6a9ef1e49ebd5028541fcd97d3a755a074904ab56fe1359829",
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
      "content_sha256": "2529e63191c668b36992e0b0d14c1ac825b93e2386a948a6df79c96b3d8996e2",
      "content_summary": "tl.where 的 gcd 规则让取值连续度降到 1；保守结论，完整 tile 的值仍连续",
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
      "content_sha256": "be145375a2fc87574031e0cd9a3d99b00c71e678a896a0b389ae142858c9627f",
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
      "content_sha256": "6dcc7bdcc14644e3ced88e9e74f1ed326ee93868a3b9762b2f9a278ef2f05632",
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
      "content_sha256": "316dc1f03bbef3c002bf2fb1105ec8d9ae145a1c59164ae4647e413ba9a6f6f3",
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
      "content_sha256": "a1e8f6a9e126707960b1bc1e7068199cf896522fc784009031323561cd145aa0",
      "content_summary": "确认 flatten 生效看 scf.if、共享内存增加、async_wait num=0 移出循环；无报错不算证据",
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
      "content_sha256": "55a350e0f4964e7c60bb74ffc1e05c87af3da26e7d766fd55708abc385e40b37",
      "content_summary": "flatten 后 epilogue 执行时 tile_id 已前进；tile_id_c 打断依赖、规避缺陷，否则编译器自带一份旧值",
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
      "content_sha256": "80a9fd7dff6474a8c4629f0b3c9c64a93a63f9dfdde34482f1fc76aeded8b9ba",
      "content_summary": "B 按 [N,K] 存放让操作数沿 K 连续；wgmma 转置只支持 f16/bf16，fp8 须沿 K 连续",
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
      "content_sha256": "472ac287fb6a379c66ff33737003fb0374031923a4f2fafb406a0aab4eea72cf",
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
      "content_sha256": "34976866893e6312109f30ea0d2f7afb08a5759fe03a6fb4af0bc909e7b86dbf",
      "content_summary": "max_contiguous 与 multiple_of 分别保证连续与对齐，缺一不可，值决定一次搬多少字节",
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
      "content_sha256": "4da63dd0b4e6ddd24356710a2d833b9fad477f22d45961db952e0609b8717bd3",
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
      "content_sha256": "469c5c9b84b75e5d8fdaca2b593e3da9aeb73252becb2b45b66e2de038e2964f",
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
      "content_sha256": "ab2a0e73140061df4f02ceb645cf4a8c61da6b9a6b7efd202709fa0d4126d5ca",
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
      "content_sha256": "5793630766630cdf9254c6de612181a2dec628cbbc0016598a7b21c9c2c57995",
      "content_summary": "输入槽数取决于槽被占用的时长：取进寄存器则 S−1，就地读则 S",
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
      "content_sha256": "f69586d31e67f3f144980f312255cf6a04a544a6cf579e22dd51f3807fa47e16",
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
      "content_sha256": "e54329f9d31ae42a085a58f89d4152cb6bb9d3c3c08748bf69482ef2394d4b4e",
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
      "content_sha256": "db4f3e23035b53467f5667421a78f91d7aae9c4012fef319c21fefdbbaacba71",
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
      "content_sha256": "8aaccd80dd45d9efd9188e948287d80762e5038daef75263e2175c2e7d540c43",
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
      "content_sha256": "db9d81bbbc3ae5af847db74628b9bb06a745f6a13f80a8f4fbefb7b09cbeb08c",
      "content_summary": "合并后的两个 scf.if 是 tile 的 prologue 与 epilogue，不是 K 循环的头尾",
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
      "content_sha256": "b824233ad984db1bab7dcdae6352ada92cb12d8eac94f00f6d79bf0e67b0c6a9",
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
      "content_sha256": "1c07294cb8fc5298e3a13fc02669b6ba88f179e9ccad1f3965ae09e5a046d90c",
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
      "content_sha256": "75d834eed7cb16c429d5f029d844eaace0954d9ce002514c9a1a205263db5c22",
      "content_summary": "轴信息分析的连续是取值连续，不是存储连续",
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
        "recall_target": "triton 编译器说下标张量连续时, 指的是存储连续还是取值连续?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-156f556d54a464954cf7b781",
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
      "content_sha256": "fee22c2bf89dae7a72f519db4545a5c2f9cb408caa5353f2ad6c814b55ddcb4a",
      "content_summary": "口述持久化与 flatten 的机制、收益、代价与确认方法",
      "dependency_content_sha256": {
        "mc-15ea16898338952dfbc21e77": "1bbdc0517462aef71b03e549bee43daa9fefbd608ee64d4a177ce57be17c5183",
        "mc-34e5ddded2a878f08c4e269a": "a1e8f6a9e126707960b1bc1e7068199cf896522fc784009031323561cd145aa0",
        "mc-7634d201cf2302a81d4f90d9": "316dc1f03bbef3c002bf2fb1105ec8d9ae145a1c59164ae4647e413ba9a6f6f3",
        "mc-a723253b09367bafdfc916a9": "5ab9ff5fa7d155e5af0773e69bd3de396226691626bb59429f678f1ad3263b40"
      },
      "depends_on": [
        "mc-15ea16898338952dfbc21e77",
        "mc-34e5ddded2a878f08c4e269a",
        "mc-7634d201cf2302a81d4f90d9",
        "mc-a723253b09367bafdfc916a9"
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
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b9113b52616621f2abdf4016980ccae7cdf7a86a8d3ef4ca3963deb2981f09ec",
      "content_summary": "口述四代目标上搬运与乘加的分工、数据离开寄存器的原因与专用化",
      "dependency_content_sha256": {
        "mc-28f897ad8a5fe0e4a3ea14c6": "0ff9097b53e553444059e3417c0a65e533d5d93ad9781590248ad8b382c1dc2c",
        "mc-7ed00a8f3615f0f2d0b036f5": "183e9219cb5cc74ab45702406b9ab0a67500de09f41774e3d7bf3ea59c96ffe8",
        "mc-9ab9c438d6e685caf034a90e": "089209be918e6b75844b12a791c5072695260eee91801107f11bbd8810cdae9d",
        "mc-aa14c9d821c28308d764ec8e": "80a9fd7dff6474a8c4629f0b3c9c64a93a63f9dfdde34482f1fc76aeded8b9ba",
        "mc-d2a126cb974f004a3189ba20": "5793630766630cdf9254c6de612181a2dec628cbbc0016598a7b21c9c2c57995"
      },
      "depends_on": [
        "mc-28f897ad8a5fe0e4a3ea14c6",
        "mc-7ed00a8f3615f0f2d0b036f5",
        "mc-9ab9c438d6e685caf034a90e",
        "mc-aa14c9d821c28308d764ec8e",
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
        "recall_target": "用 60–90 秒讲清矩阵乘的搬运与计算在四代目标上由谁完成, 以及专用化解决什么。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-8ee3e4fa29b4a8035ada4054",
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
      "content_sha256": "ae2d2dfe1ea0a8b92d425772670a8617ba80f5f214b85dca5e4f40d895c0f87b",
      "content_summary": "口述行主序 B 保住异步拷贝与提前量的做法与诊断",
      "dependency_content_sha256": {
        "mc-0bce910539e203eaf3cf37c9": "34976866893e6312109f30ea0d2f7afb08a5759fe03a6fb4af0bc909e7b86dbf",
        "mc-558ab777fd4b7293a5864b30": "2529e63191c668b36992e0b0d14c1ac825b93e2386a948a6df79c96b3d8996e2",
        "mc-825d27f5f1d09de05c268fe5": "6dcc7bdcc14644e3ced88e9e74f1ed326ee93868a3b9762b2f9a278ef2f05632",
        "mc-8535ff3240e81707b3cc7d0f": "472ac287fb6a379c66ff33737003fb0374031923a4f2fafb406a0aab4eea72cf",
        "mc-aef5d803d3de8f31fe6e6ca7": "1249dd6ed25671f4e45b32784771506743aa2acfec22a7488e688f65e56dd4f1"
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
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b5c6828a3a393bf70d31eda30065807e21d5bbf193aeaada496e0d8dbf0275f0",
      "content_summary": "口述 M1 的测量设计、结果与结论边界",
      "dependency_content_sha256": {
        "mc-8444f39ef05660455739c1de": "be145375a2fc87574031e0cd9a3d99b00c71e678a896a0b389ae142858c9627f",
        "mc-d794901c2b34c57696fdab27": "1c07294cb8fc5298e3a13fc02669b6ba88f179e9ccad1f3965ae09e5a046d90c",
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
      "source_ids": [
        "persistent-matmul-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "089209be918e6b75844b12a791c5072695260eee91801107f11bbd8810cdae9d",
      "content_summary": "三代乘加指令的形状、发起者与每轮条数",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "ptx-isa",
          "version": "9.4"
        },
        "recall_target": "三代张量核心乘加指令的形状、发起者与每轮条数"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9ab9c438d6e685caf034a90e",
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
      "content_sha256": "a55e48f2bf02bd2eb1fed018aca3fbc653b98580c1e24db8a01f9ad33ff893da",
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
      "content_sha256": "379d6c3d50b24f8388179c920b7a8accbbb5117101579ede71968f6077521594",
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
      "content_sha256": "08a195b5a6ea41962394c4eb7d05a7ba8750fa1311b0b647a1a3ba6aa3e75425",
      "content_summary": "共享内存多是因为操作数留在共享内存，不是提前量更大",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "同一 num_stages 下 sm_90 多用共享内存、少用寄存器, 是因为提前得更多吗?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-d9713a58d6e2b0e40daf5355",
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
      "content_sha256": "150e255f8a30b936d3ca35b689ee502c42704d3a938465bf60394543e7e26fda",
      "content_summary": "资源用量只在改变驻留数时影响速度",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-persistent-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "一个版本多用共享内存、少用寄存器, 能否据此说它变慢了?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9947558b311d187829cd1663",
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
      "content_sha256": "6ac51ec50d7c977102245829850e2656455fe78dd5518b2b32e473eaecbee33c",
      "content_summary": "持久化是手写的 tile 循环，不是编译器把发射提出循环",
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
    }
  ],
  "managed_body_sha256": "c565f0268c8a7ab30147661c0ad4f762bc1fa52ac0063fbbf0f4a3a43e08bdc4",
  "manifest_payload_sha256": "a11346aaf124f707f251c4fb4016efcddc8d95089c4452b9192dba3d1da730ed",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 24002,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-09-persistent-matmul-correction.xlsx",
      "row_count": 15,
      "rows": [
        {
          "content_sha256": "469c5c9b84b75e5d8fdaca2b593e3da9aeb73252becb2b45b66e2de038e2964f",
          "logical_id": "mc-f8281736b7d9c4060a33773e",
          "row_sha256": "8c27ba59eecda613873057345b41a6d236a25329ca601e7628184cb1c50cc453"
        },
        {
          "content_sha256": "ab2a0e73140061df4f02ceb645cf4a8c61da6b9a6b7efd202709fa0d4126d5ca",
          "logical_id": "mc-077f37d68441b7d58f9d55cb",
          "row_sha256": "03c95971fc769b2ff732a1263e56c09588f23de2264ce9741457d2f1d6e9b485"
        },
        {
          "content_sha256": "5793630766630cdf9254c6de612181a2dec628cbbc0016598a7b21c9c2c57995",
          "logical_id": "mc-d2a126cb974f004a3189ba20",
          "row_sha256": "9b3700910140e2defc7f4a609483d7eba5db8c1545193edd56d4d8ee0c3e7c95"
        },
        {
          "content_sha256": "f69586d31e67f3f144980f312255cf6a04a544a6cf579e22dd51f3807fa47e16",
          "logical_id": "mc-7bcbbcfc3af2613f2cc99704",
          "row_sha256": "2571fb60609972df1e9b1e489ec9371d3c713a0f958930da8970f921c921534e"
        },
        {
          "content_sha256": "e54329f9d31ae42a085a58f89d4152cb6bb9d3c3c08748bf69482ef2394d4b4e",
          "logical_id": "mc-96458a7ae787cb0ffdd97dec",
          "row_sha256": "9b97c98451429185ecf804c9c09b594e836d6cf10f468417a0b496e87c14e998"
        },
        {
          "content_sha256": "db4f3e23035b53467f5667421a78f91d7aae9c4012fef319c21fefdbbaacba71",
          "logical_id": "mc-b6e1c7bc61a09c21af41c0c3",
          "row_sha256": "0c487782db031b7885c07c693c86463f113b0bea0993dfd85321aa3beb45bafa"
        },
        {
          "content_sha256": "8aaccd80dd45d9efd9188e948287d80762e5038daef75263e2175c2e7d540c43",
          "logical_id": "mc-67daad7e80dfa27e69ab9bec",
          "row_sha256": "9d87bca3222cb7d20e96546d9f06efbea35636ad8959ea7062cac47de8a1b1a1"
        },
        {
          "content_sha256": "db9d81bbbc3ae5af847db74628b9bb06a745f6a13f80a8f4fbefb7b09cbeb08c",
          "logical_id": "mc-7c92dea413044da374f93684",
          "row_sha256": "a4873c57988af9965c065ca3dc4aebc195dbc2106c4708415a25b5774c3649c8"
        },
        {
          "content_sha256": "b824233ad984db1bab7dcdae6352ada92cb12d8eac94f00f6d79bf0e67b0c6a9",
          "logical_id": "mc-98dbd9178f8edfe9b73bd740",
          "row_sha256": "c9a6fee323313828b897a1f5c8173e88576af650b6e5ae740141bd398a100241"
        },
        {
          "content_sha256": "1c07294cb8fc5298e3a13fc02669b6ba88f179e9ccad1f3965ae09e5a046d90c",
          "logical_id": "mc-d794901c2b34c57696fdab27",
          "row_sha256": "1fe44e6e02fb5f258b705dec0108e2ad8a408ccaa6c4d3ccf86580fd97996216"
        },
        {
          "content_sha256": "75d834eed7cb16c429d5f029d844eaace0954d9ce002514c9a1a205263db5c22",
          "logical_id": "mc-156f556d54a464954cf7b781",
          "row_sha256": "6c53a07044ea5b3ed6a8a68e280f2c28900e2c35ce65e769410597b8b60b7cd0"
        },
        {
          "content_sha256": "379d6c3d50b24f8388179c920b7a8accbbb5117101579ede71968f6077521594",
          "logical_id": "mc-422574c717b612e2fbb572ff",
          "row_sha256": "79423b0ec13a264ef836fc84e8c04f7cf8f0f7437fe06c56e01d6b22a8bf1879"
        },
        {
          "content_sha256": "08a195b5a6ea41962394c4eb7d05a7ba8750fa1311b0b647a1a3ba6aa3e75425",
          "logical_id": "mc-d9713a58d6e2b0e40daf5355",
          "row_sha256": "b59aaecf0ec9a310a0d4d28c24b3fe1f5599d0f27053674118ae8778a12b5123"
        },
        {
          "content_sha256": "150e255f8a30b936d3ca35b689ee502c42704d3a938465bf60394543e7e26fda",
          "logical_id": "mc-9947558b311d187829cd1663",
          "row_sha256": "5a03b374257fa7cf6d6c626037f6b56e98723bdb1d9c5daa33dbaebb186ecc45"
        },
        {
          "content_sha256": "6ac51ec50d7c977102245829850e2656455fe78dd5518b2b32e473eaecbee33c",
          "logical_id": "mc-2ef43c89b6814d0b0ab746d9",
          "row_sha256": "04ccc41d921b4e15373242a7f01658cad91346e17ca4a78be052a3c391c16d04"
        }
      ],
      "sha256": "10cdf092f16cb39e954a3603e7c1a799a5dada40748168160a33ca84eccce3b2",
      "sheet_name": "cards",
      "table_sha256": "b9daa53e78aa2c99d70cd2a39ef30dea97a8e60b061af42fd9ee6000dea9cdc4",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 32571,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-09-persistent-matmul-technical-qa.xlsx",
      "row_count": 20,
      "rows": [
        {
          "content_sha256": "5ab9ff5fa7d155e5af0773e69bd3de396226691626bb59429f678f1ad3263b40",
          "logical_id": "mc-a723253b09367bafdfc916a9",
          "row_sha256": "c59b08c7ddfca939562d2ee9d80336fbff0cf07fa683e8d7bb0e716a88ab9169"
        },
        {
          "content_sha256": "1249dd6ed25671f4e45b32784771506743aa2acfec22a7488e688f65e56dd4f1",
          "logical_id": "mc-aef5d803d3de8f31fe6e6ca7",
          "row_sha256": "3b17114e5819dd3017b130edd8fa8e8677eec0e3722891ee71b1b0ef0532e0ef"
        },
        {
          "content_sha256": "1bbdc0517462aef71b03e549bee43daa9fefbd608ee64d4a177ce57be17c5183",
          "logical_id": "mc-15ea16898338952dfbc21e77",
          "row_sha256": "0c87a8984af7f7d7c41b81c8c3184189cd6d02f641188cf0d053009a366104dd"
        },
        {
          "content_sha256": "183e9219cb5cc74ab45702406b9ab0a67500de09f41774e3d7bf3ea59c96ffe8",
          "logical_id": "mc-7ed00a8f3615f0f2d0b036f5",
          "row_sha256": "3b56c76069310f2fb3625e909090b38ff54964b8a28e29235b434105571700cd"
        },
        {
          "content_sha256": "24656ea44eb6ce6a9ef1e49ebd5028541fcd97d3a755a074904ab56fe1359829",
          "logical_id": "mc-419812ab9e3c766b37ca840b",
          "row_sha256": "0fc86f7033cd823ac07b6a0aace66f042ca3434c175e43a3c87083cda107ab0a"
        },
        {
          "content_sha256": "2529e63191c668b36992e0b0d14c1ac825b93e2386a948a6df79c96b3d8996e2",
          "logical_id": "mc-558ab777fd4b7293a5864b30",
          "row_sha256": "f38b876b1c2e8f0f0492188a2744522e4cc15ca06f704be9d6bb49161885996e"
        },
        {
          "content_sha256": "be145375a2fc87574031e0cd9a3d99b00c71e678a896a0b389ae142858c9627f",
          "logical_id": "mc-8444f39ef05660455739c1de",
          "row_sha256": "a26f448c4e2b64e9a091d4efe08c5107e8e36207e25fec828b6ad90dd49b6092"
        },
        {
          "content_sha256": "6dcc7bdcc14644e3ced88e9e74f1ed326ee93868a3b9762b2f9a278ef2f05632",
          "logical_id": "mc-825d27f5f1d09de05c268fe5",
          "row_sha256": "512ac9b0d36063ed7b333f3ecd75dd2889d09daaa7d1cbf8dd99899047ac9f1f"
        },
        {
          "content_sha256": "316dc1f03bbef3c002bf2fb1105ec8d9ae145a1c59164ae4647e413ba9a6f6f3",
          "logical_id": "mc-7634d201cf2302a81d4f90d9",
          "row_sha256": "dd79542abe1d1c4c61a8f88a3a76f10a13efdf4f0a658649ca41c4418ae4f59f"
        },
        {
          "content_sha256": "a1e8f6a9e126707960b1bc1e7068199cf896522fc784009031323561cd145aa0",
          "logical_id": "mc-34e5ddded2a878f08c4e269a",
          "row_sha256": "568be9cc6ef432eb6dc887a3880ebd902ffdc2f43dca27ec3a3273a222bae621"
        },
        {
          "content_sha256": "55a350e0f4964e7c60bb74ffc1e05c87af3da26e7d766fd55708abc385e40b37",
          "logical_id": "mc-4ad67e4bf89b9d1fccf36b84",
          "row_sha256": "3d5220e7b9da60878b407b85769f1ec905409375076adee5ae36545a249ba7dd"
        },
        {
          "content_sha256": "80a9fd7dff6474a8c4629f0b3c9c64a93a63f9dfdde34482f1fc76aeded8b9ba",
          "logical_id": "mc-aa14c9d821c28308d764ec8e",
          "row_sha256": "a04ea1d33c5686c4cdfd25e8e2307b1238413e7f5437b24f062bcaf148cb9c12"
        },
        {
          "content_sha256": "0ff9097b53e553444059e3417c0a65e533d5d93ad9781590248ad8b382c1dc2c",
          "logical_id": "mc-28f897ad8a5fe0e4a3ea14c6",
          "row_sha256": "b1d38b9c172fe5bf38b7182c1b0df93f15a46e48802afe9aaad6f06fd64259e1"
        },
        {
          "content_sha256": "472ac287fb6a379c66ff33737003fb0374031923a4f2fafb406a0aab4eea72cf",
          "logical_id": "mc-8535ff3240e81707b3cc7d0f",
          "row_sha256": "e1dd7ebf82eee8a5128eed835ca1f7eb7fd4eeb82484e284285f6f7b8a68661b"
        },
        {
          "content_sha256": "34976866893e6312109f30ea0d2f7afb08a5759fe03a6fb4af0bc909e7b86dbf",
          "logical_id": "mc-0bce910539e203eaf3cf37c9",
          "row_sha256": "86408519063c1748aa698963c91786980025b678f16b35dd9143af5c929a0611"
        },
        {
          "content_sha256": "4da63dd0b4e6ddd24356710a2d833b9fad477f22d45961db952e0609b8717bd3",
          "logical_id": "mc-813451003ac19a697e423417",
          "row_sha256": "a1d3ef9cc4badbe93f3af17e6eb71e889f62a72ac406cdbc212bf5597220a126"
        },
        {
          "content_sha256": "089209be918e6b75844b12a791c5072695260eee91801107f11bbd8810cdae9d",
          "logical_id": "mc-9ab9c438d6e685caf034a90e",
          "row_sha256": "bdf3624e6458a843f78831d01ba0fee206dfdfba88fdc223de28dd8c0705d719"
        },
        {
          "content_sha256": "622206aff1a88fcfce67f65b548aa424409a60ef368c579ceb77495f9f2528eb",
          "logical_id": "mc-4ef123242d7aa007c70afbd1",
          "row_sha256": "a8021d6bd00f0a57de15a3d17e7d169859021489f4fbdfeeefe8a52b176644d9"
        },
        {
          "content_sha256": "a55e48f2bf02bd2eb1fed018aca3fbc653b98580c1e24db8a01f9ad33ff893da",
          "logical_id": "mc-0c26d31e310e78360921c5a4",
          "row_sha256": "2ac7566085b308323fa19d5570dc92bbcb0c35c009a42471c07d9b77d6fc1e1e"
        },
        {
          "content_sha256": "04094838b49b0fc7511ad6abbce4bea8ba00fe92a768b727e9cb7629218afc1f",
          "logical_id": "mc-f062131fde8aa04f73b8163b",
          "row_sha256": "46df774d4c6d614dcafbf3e9d001b1454f6bc282b58f0a73cbbd95f4b7ab67f0"
        }
      ],
      "sha256": "18e25e1063a75dfb7cab3bd3f5c4107034037826d036bd7325c7c62ef7eb65c5",
      "sheet_name": "cards",
      "table_sha256": "1f0d7bbad75ed88772cec95689039eda941145ce6db2c4af3f842f27fc40c10a",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 9291,
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
          "content_sha256": "fee22c2bf89dae7a72f519db4545a5c2f9cb408caa5353f2ad6c814b55ddcb4a",
          "logical_id": "mc-000831b41e4c256b4db5dcad",
          "row_sha256": "d3a0a54c41ba73366d0ad98717fc5a10151f0794ab5523c618b3e364beb4b079"
        },
        {
          "content_sha256": "b9113b52616621f2abdf4016980ccae7cdf7a86a8d3ef4ca3963deb2981f09ec",
          "logical_id": "mc-8ee3e4fa29b4a8035ada4054",
          "row_sha256": "195976482917efded6fd4246393b0b5a3a522f6f1e53e56bd1afa24a12ea2aed"
        },
        {
          "content_sha256": "ae2d2dfe1ea0a8b92d425772670a8617ba80f5f214b85dca5e4f40d895c0f87b",
          "logical_id": "mc-10ec2eb178242ba25b686071",
          "row_sha256": "1bbd537f32c4ac1dbe2155c8670b4fd4f3ce6166553c9ca76d7ef22db6235bb1"
        },
        {
          "content_sha256": "b5c6828a3a393bf70d31eda30065807e21d5bbf193aeaada496e0d8dbf0275f0",
          "logical_id": "mc-b2edcf5bb5fe74b429490050",
          "row_sha256": "4b3bd4f29609eab8c9a634bec9a39be491fc51d4f1af88ef2bf152cf3aca32db"
        }
      ],
      "sha256": "453ced7ad54ec1396c0b7c9a475a9472517e1db95f7e22d0ae26874f5e254c4e",
      "sheet_name": "cards",
      "table_sha256": "bb8e07fafaf0b2313084f62a64c3527294e783fc1d6066ac8883d45291fce17d",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "74b1d5a1bc5533fbebe1898d1a60a77b4146f0cdb7af7d6a6364db08535a2393",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "persistent-matmul-log",
      "path": "docs/triton-learning/logs/2026-10-14-persistent-matmul.md",
      "sha256": "460dc60c4be421528663a5169d96cb0efbaebdc2045ac16424ff50db00a8fe30",
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

导入文件：[triton-lesson-09-persistent-matmul-correction.xlsx](triton-lesson-09-persistent-matmul-correction.xlsx)（15 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-09-persistent-matmul-technical-qa.xlsx](triton-lesson-09-persistent-matmul-technical-qa.xlsx)（20 张卡）

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
