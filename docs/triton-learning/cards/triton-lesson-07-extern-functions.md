---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "5debb5a87074958aefb2e6a7b656b63ed1ba60b4bb17c6bce4112f7e6cd808f9",
  "candidate_sha256": "9f68f8b6ff124720dea7c0d3b1aee4bbbb182f2af771f52152d22446bed89b31",
  "cards": [
    {
      "content_sha256": "cbb912a2a8d8cb0ba0fe02596df56a782df5c68ac56aad1cd584bbb4ff17b756",
      "content_summary": "接口模块按后端的 get_module_map 整体替换，直接导入实现模块会绑定后端",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "同一份调用 libdevice 的 kernel 为什么能在不同后端编译?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9555a9080a7ebf622b773758",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b815cc3912e89fe5cd1bf6c636b2818df0f5d21575c3b42b39feb9fe5ae7fa67",
      "content_summary": "libdevice 的表只有 fp32、fp64，半精度须在 kernel 内先转 fp32，fp64 仍走 __nv_asin；查表失败报 KeyError",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "支持多种浮点类型的 kernel 里, load 之后能否把半精度值直接传给 libdevice 函数?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-19e3929a6a3c493d606ec4f5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a37a10b41c5887d6ee43c2ea0d2858a079a2dc264ecb325a7c257151c50a2908",
      "content_summary": "映射未生效时空壳函数返回 None，报错落在下一行的 tl.store",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "后端的 get_module_map 没有生效时是什么现象?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-58a9421ebbb480690a2063e8",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7cbfc591b996a8dc4af4eb767cddded5632df92e44ea2860b09af6058c10311e",
      "content_summary": "每线程 E 个元素：1 条声明、E 次调用、1 份定义、内联成 E 份函数体",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "一次 extern_elementwise 降级到 ptx 的过程中, 声明、调用、定义、函数体各有几份?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b64417d0916261bcf64ee860",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0404a087735510ec2acd6fd1633dcdd157b811b7b0e329af74e9c7ae07efc836",
      "content_summary": "库内容哈希进缓存键：换库会重新编译，路径错误在算缓存键时就报 FileNotFoundError",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "nvidia 后端链接 libdevice 时用哪个库、何时链接、拷多少、怎样影响缓存?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-eb8ba5ca8a041412f7151aef",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bc913e231f7768a15e489d2af73db157b64560e0b5d25036178e2eac16482866",
      "content_summary": "默认 FTZ=1、PREC_SQRT=0，相当于 nvcc 的 --ftz=true 与 --prec-sqrt=false，只影响 libdevice 内部",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton 默认把 libdevice 编成哪种数值模式, 相当于 nvcc 的什么设置?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-be63c7cf4646448fc25fe75f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "35b52e284da8678234d99b8e220bcd64b8bd5e103795451193059e12f3e75da3",
      "content_summary": "默认 FTZ 使次正规数输入得 0，enable_reflect_ftz=False 后与 torch 一致；常规容差测试看不出",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "triton 的 libdevice.asin 对次正规数输入输出 0 而 torch 不是, 原因与处理?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6a353374391eea62b23d6433",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1a58f6a90f3ce6c0bd67eff8b0e997abc19d282e8d387eb809f82ecab2479661",
      "content_summary": "tl.math 多数函数在 NVIDIA 上也走 libdevice，区别在后端中立性与函数覆盖面",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "tl.math 是硬件指令而 libdevice 是库调用, 这个说法对吗?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-7f751c559031a02dba76474f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0f71d738af19135972b8e7103b37083af1cb2d7d29b41338da12fafa4ec4c860",
      "content_summary": "tl.exp、tl.sqrt、普通除法是快速档，精确档为 libdevice.exp、sqrt_rn、div_rn",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "exp、sqrt、除法各自的快速档和精确档是什么, inductor 怎么选?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e75cf3837f70e205d8f09c3a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "efdbb283703b4a08e375791ccba17c4b9d241fa9b7e9d115a68981a341fe8be6",
      "content_summary": "快速 exp 的乘积舍入误差被指数放大，误差随 |x| 增长",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "先乘 log2e 再做 2 的幂的快速 exp, 为什么 |x| 越大越不准?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-124f818a7fe3826dab719c4d",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c0b061bb11b92e1bf8225a4edbe9c23fed5e5498672e104915148f4285393aaa",
      "content_summary": "内联汇编文本不经链接原样进入最终汇编，换后端即失败",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "内联汇编进入编译流程的方式与可移植性?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-bf99d430d51b246e6eeb859a",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c891a0813a210b4c82f02cd9325108dbc33ee56d879f3c71d999fd2316666840",
      "content_summary": "自定义库需要 dtype 符号表和经 extern_libs 传入的库文件，名字须一致，缺库在最后一步才报错",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "让 kernel 调用自己提供的数学函数要准备什么, 缺库时是什么现象?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-096ead4cf8f972e07e7a3dcf",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "03a5232fba59619757b9a50eb49f180a78558d3a99b146f8b311b3ef9be10c71",
      "content_summary": "口述非 NV 后端接入 libdevice 要填的四环（映射与符号表、库与缓存键、链接、内联）及各环失败现象",
      "dependency_content_sha256": {
        "mc-096ead4cf8f972e07e7a3dcf": "c891a0813a210b4c82f02cd9325108dbc33ee56d879f3c71d999fd2316666840",
        "mc-19e3929a6a3c493d606ec4f5": "b815cc3912e89fe5cd1bf6c636b2818df0f5d21575c3b42b39feb9fe5ae7fa67",
        "mc-58a9421ebbb480690a2063e8": "a37a10b41c5887d6ee43c2ea0d2858a079a2dc264ecb325a7c257151c50a2908",
        "mc-eb8ba5ca8a041412f7151aef": "0404a087735510ec2acd6fd1633dcdd157b811b7b0e329af74e9c7ae07efc836",
        "mc-f345b815272846cccb6a6b20": "bdaaa46106b642dc48bfe4f588e3695c728149ef98caea67e603a85c0174cd17"
      },
      "depends_on": [
        "mc-096ead4cf8f972e07e7a3dcf",
        "mc-19e3929a6a3c493d606ec4f5",
        "mc-58a9421ebbb480690a2063e8",
        "mc-eb8ba5ca8a041412f7151aef",
        "mc-f345b815272846cccb6a6b20"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲给非 nvidia 后端接入 libdevice 要填哪几环、各环漏掉时在哪里失败。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-80bed66011f61f4bf380f45a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bdaaa46106b642dc48bfe4f588e3695c728149ef98caea67e603a85c0174cd17",
      "content_summary": "残留调用有未内联与未链接两种原因，链接后的 IR 中 define 或 declare 可区分",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "新后端机器码里残留对库函数的真实调用, 两种原因怎样区分?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f345b815272846cccb6a6b20",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3dd7f8180dcde8237318af1ed6938a7b2bd6cb841f24dac10031aeb88fb17299",
      "content_summary": "换到 AMD gfx942 后符号、每线程元素数（warp 64，RDNA 为 32）、链接库和次正规数默认处理都变，机制不变",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "同一个 libdevice.asin kernel 从 nvidia 换到 amd, 哪些变哪些不变?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1bb7330a29bdeab1a29274d4",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "93519a5ceac613fa656c70af90f6845bb69d5bd4e0a4e4a4dd14796ce111515f",
      "content_summary": "普通赋值使布尔值变张量导致运行期分支，用 tl.constexpr 注解保持编译期；重新绑定后再判断 dtype 永不成立",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "kernel 里按 dtype 分支时, 为什么先存进变量再 if 会编译报错?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-595c4a33ca5f8d1ef86bb8f3",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2be6e4c821a92f3009da1a98f5b0b8412429205d8814b9feb81361b45186cdc7",
      "content_summary": "口述 tl.math、libdevice、内联汇编与自定义库四条路线按可移植性、精度代价与 dtype 的取舍顺序",
      "dependency_content_sha256": {
        "mc-096ead4cf8f972e07e7a3dcf": "c891a0813a210b4c82f02cd9325108dbc33ee56d879f3c71d999fd2316666840",
        "mc-19e3929a6a3c493d606ec4f5": "b815cc3912e89fe5cd1bf6c636b2818df0f5d21575c3b42b39feb9fe5ae7fa67",
        "mc-7f751c559031a02dba76474f": "1a58f6a90f3ce6c0bd67eff8b0e997abc19d282e8d387eb809f82ecab2479661",
        "mc-bf99d430d51b246e6eeb859a": "c0b061bb11b92e1bf8225a4edbe9c23fed5e5498672e104915148f4285393aaa",
        "mc-e75cf3837f70e205d8f09c3a": "0f71d738af19135972b8e7103b37083af1cb2d7d29b41338da12fafa4ec4c860"
      },
      "depends_on": [
        "mc-096ead4cf8f972e07e7a3dcf",
        "mc-19e3929a6a3c493d606ec4f5",
        "mc-7f751c559031a02dba76474f",
        "mc-bf99d430d51b246e6eeb859a",
        "mc-e75cf3837f70e205d8f09c3a"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒说明 triton kernel 里数学函数四条实现路线怎样选。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-fd69faa9f8c944174f8be4ab",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c0351f17bb7bdade91065cb68d581055b6d58289558edbafd6b5c6231e4d7c16",
      "content_summary": "只编译时用 TTIR 的符号验证 kernel 内升精度，用 PTX 无 call 验证内联",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "没有 gpu 时怎样用编译产物验证 kernel 内升精度和函数内联?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0c708fa3eaa5d508bdfa514a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2a105c83fe30d069d354ea4d00f6d7321db242465ff1cbc40a35846a3996c575",
      "content_summary": "包装函数须新建输出张量并返回，extern_libs 原样透传，不能把输入同时当输出",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "逐元素 kernel 的包装函数应怎样传输出张量并返回?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-c70f4801d89ce67298d6eb2c",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "84319d3b5615c3ceb526b8ebf8062816d7a395d6217b1e9ae55dcd2ae9c2bf6f",
      "content_summary": "类型分支应依据加载结果自身的 dtype，额外标志可能与指针类型矛盾并静默损失精度",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "kernel 按元素类型分支时, 类型信息应从哪里来?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-ae58ca5f4ffd85b72b18f8a9",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d6b394e40c0fb2bbd45edfa7c22b1db40c890d52ca2bac2c01ae30631d7ba8e8",
      "content_summary": "TTGIR 到 LLVM IR 的降级由 Triton 完成，LLVM 负责链接、O3 和生成汇编",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "ttgir 到 llvm ir 的转换由谁完成, llvm 从哪里接手?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-90d48b89ad914e50e8961280",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ac9c34b553a7726c89003479b3d03d4fb40a1c515f424832581e9bb9fa893b2a",
      "content_summary": "NVIDIA 用 enable_reflect_ftz，AMD 用 allow_flush_denorm，两者机制不同且默认值相反",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "让 nvidia 和 amd 对次正规数的结果一致, 各调哪个选项?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3c80afdcd4d0a934190abd84",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "65c04982430bbb747ba15f057d3b93c38833b4c08c98ad4e265d6da630aa3735",
      "content_summary": "口述 libdevice.asin 从接口替换、查表、逐元素调用到链接、内联与反射参数的全链路，并分清 Triton 与 LLVM 的职责",
      "dependency_content_sha256": {
        "mc-19e3929a6a3c493d606ec4f5": "b815cc3912e89fe5cd1bf6c636b2818df0f5d21575c3b42b39feb9fe5ae7fa67",
        "mc-90d48b89ad914e50e8961280": "d6b394e40c0fb2bbd45edfa7c22b1db40c890d52ca2bac2c01ae30631d7ba8e8",
        "mc-9555a9080a7ebf622b773758": "cbb912a2a8d8cb0ba0fe02596df56a782df5c68ac56aad1cd584bbb4ff17b756",
        "mc-b64417d0916261bcf64ee860": "7cbfc591b996a8dc4af4eb767cddded5632df92e44ea2860b09af6058c10311e",
        "mc-be63c7cf4646448fc25fe75f": "bc913e231f7768a15e489d2af73db157b64560e0b5d25036178e2eac16482866"
      },
      "depends_on": [
        "mc-19e3929a6a3c493d606ec4f5",
        "mc-90d48b89ad914e50e8961280",
        "mc-9555a9080a7ebf622b773758",
        "mc-b64417d0916261bcf64ee860",
        "mc-be63c7cf4646448fc25fe75f"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒讲清 libdevice.asin 从 python 到 ptx 的全链路。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-fe65c36ff3210d3d70723c7e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已按更新后的子卡复核：子卡 05 换成 22（职责边界），02 换成合并后的半精度纠错卡；新增职责锚点；参考回答和锚点的每个事实都能在 01、新 02、04、06、22 中找到。"
      },
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cede291f5eea28e20dab50603e4947c779ce89356618821bd5181256a3de48b9",
      "content_summary": "口述 Triton/Inductor 与 eager 数值不一致的三类来源、按症状排查与对齐办法，含 Inductor 默认开关",
      "dependency_content_sha256": {
        "mc-3c80afdcd4d0a934190abd84": "ac9c34b553a7726c89003479b3d03d4fb40a1c515f424832581e9bb9fa893b2a",
        "mc-6a353374391eea62b23d6433": "35b52e284da8678234d99b8e220bcd64b8bd5e103795451193059e12f3e75da3",
        "mc-be63c7cf4646448fc25fe75f": "bc913e231f7768a15e489d2af73db157b64560e0b5d25036178e2eac16482866",
        "mc-e75cf3837f70e205d8f09c3a": "0f71d738af19135972b8e7103b37083af1cb2d7d29b41338da12fafa4ec4c860"
      },
      "depends_on": [
        "mc-3c80afdcd4d0a934190abd84",
        "mc-6a353374391eea62b23d6433",
        "mc-be63c7cf4646448fc25fe75f",
        "mc-e75cf3837f70e205d8f09c3a"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-extern-functions",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "用 60–90 秒回答 triton kernel 与 pytorch eager 结果不一致的来源与排查。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-9ef4217f53d55ccf9549cbed",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已按更新后的子卡复核：子卡去掉 17、15，改为 09、07、06、23；补上 Inductor 的 eager_numerics 三个开关默认关闭（09 的延伸，依据日志 L51 复核更正）；‘AMD 默认保留’限定为同一个 asin kernel。"
      },
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "07175fdb20291e32437a48f28139d7890d8eb9b42847f42922a279f472218de9",
  "manifest_payload_sha256": "e6936f174be495207cf73271a93115b1bf453994afa1e36f255329eec41371c5",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 10682,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-07-extern-functions-correction.xlsx",
      "row_count": 5,
      "rows": [
        {
          "content_sha256": "b815cc3912e89fe5cd1bf6c636b2818df0f5d21575c3b42b39feb9fe5ae7fa67",
          "logical_id": "mc-19e3929a6a3c493d606ec4f5",
          "row_sha256": "0c985f0f2740c1e46f290408f1dd03d3d5636dc1aea3df703fd9ea5e102ce01c"
        },
        {
          "content_sha256": "2a105c83fe30d069d354ea4d00f6d7321db242465ff1cbc40a35846a3996c575",
          "logical_id": "mc-c70f4801d89ce67298d6eb2c",
          "row_sha256": "8ffa9f879f668ed38b35d1ef7a16f393657873fe79530430386dc81b55616e89"
        },
        {
          "content_sha256": "84319d3b5615c3ceb526b8ebf8062816d7a395d6217b1e9ae55dcd2ae9c2bf6f",
          "logical_id": "mc-ae58ca5f4ffd85b72b18f8a9",
          "row_sha256": "0be739df726b5f78b397e28b981fd9abcf5e6978a023363972a591b87fd295bd"
        },
        {
          "content_sha256": "d6b394e40c0fb2bbd45edfa7c22b1db40c890d52ca2bac2c01ae30631d7ba8e8",
          "logical_id": "mc-90d48b89ad914e50e8961280",
          "row_sha256": "c460263e651ec2baba25ffd0b51fcabf83b8bb7317ae31ae5608d4bfce011329"
        },
        {
          "content_sha256": "ac9c34b553a7726c89003479b3d03d4fb40a1c515f424832581e9bb9fa893b2a",
          "logical_id": "mc-3c80afdcd4d0a934190abd84",
          "row_sha256": "98661c02f940548ce1ba978422464b0f9123f0d05c5c8e5d60f6494c1fe71c35"
        }
      ],
      "sha256": "7b2e37e83b96c931839eeb10811bb3325a653c61fea2847ffa260fd9e37d6f71",
      "sheet_name": "cards",
      "table_sha256": "e7d80bcf424fa7ac1fcf0ed9e07ea2c2c1ea7bef543984a00184908e5a5b6b3f",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 24925,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-07-extern-functions-technical-qa.xlsx",
      "row_count": 15,
      "rows": [
        {
          "content_sha256": "cbb912a2a8d8cb0ba0fe02596df56a782df5c68ac56aad1cd584bbb4ff17b756",
          "logical_id": "mc-9555a9080a7ebf622b773758",
          "row_sha256": "526b22d313bda09895370249317ad0299c06f08746a5226731c1739a2c1edcfe"
        },
        {
          "content_sha256": "a37a10b41c5887d6ee43c2ea0d2858a079a2dc264ecb325a7c257151c50a2908",
          "logical_id": "mc-58a9421ebbb480690a2063e8",
          "row_sha256": "d800d67078de755c764179bfbda9d50802654784f8682cecb4864cf2521db1a1"
        },
        {
          "content_sha256": "7cbfc591b996a8dc4af4eb767cddded5632df92e44ea2860b09af6058c10311e",
          "logical_id": "mc-b64417d0916261bcf64ee860",
          "row_sha256": "87c2e2aefdf3527a9aaccf6299af479d602f92ef55f9d34ec2ac6507b1652f41"
        },
        {
          "content_sha256": "0404a087735510ec2acd6fd1633dcdd157b811b7b0e329af74e9c7ae07efc836",
          "logical_id": "mc-eb8ba5ca8a041412f7151aef",
          "row_sha256": "afb01d20c322a8b2fc3dbf2ad8552b402256118eb02cf7f4a66c312e5d3fc178"
        },
        {
          "content_sha256": "bc913e231f7768a15e489d2af73db157b64560e0b5d25036178e2eac16482866",
          "logical_id": "mc-be63c7cf4646448fc25fe75f",
          "row_sha256": "343f1705d91b4b14e2924954ab95f8484aec03e6bceaf4b7949116a8dbab19bb"
        },
        {
          "content_sha256": "35b52e284da8678234d99b8e220bcd64b8bd5e103795451193059e12f3e75da3",
          "logical_id": "mc-6a353374391eea62b23d6433",
          "row_sha256": "5143ca18b96d8b53def3fdd04d6481bd9d68dae81f6ef6dcf3d600e2c064039d"
        },
        {
          "content_sha256": "1a58f6a90f3ce6c0bd67eff8b0e997abc19d282e8d387eb809f82ecab2479661",
          "logical_id": "mc-7f751c559031a02dba76474f",
          "row_sha256": "8c9c5348bfd2c92d03a7c24edf8a895b10d0240321fca8e6f73782038ecc36d9"
        },
        {
          "content_sha256": "0f71d738af19135972b8e7103b37083af1cb2d7d29b41338da12fafa4ec4c860",
          "logical_id": "mc-e75cf3837f70e205d8f09c3a",
          "row_sha256": "cdde77352ba51caf3c2b47f168c7ad80d8a4bc9217cef0c1325778e161706a8f"
        },
        {
          "content_sha256": "efdbb283703b4a08e375791ccba17c4b9d241fa9b7e9d115a68981a341fe8be6",
          "logical_id": "mc-124f818a7fe3826dab719c4d",
          "row_sha256": "8ea4b4d4451a5b3765c13cde706545af90deee2c9b11490c0f7550b28d1c112a"
        },
        {
          "content_sha256": "c0b061bb11b92e1bf8225a4edbe9c23fed5e5498672e104915148f4285393aaa",
          "logical_id": "mc-bf99d430d51b246e6eeb859a",
          "row_sha256": "0b4b61f6288de1dee9acd84e8636b49b65805490acd393717e7d3e727ac3c8e8"
        },
        {
          "content_sha256": "c891a0813a210b4c82f02cd9325108dbc33ee56d879f3c71d999fd2316666840",
          "logical_id": "mc-096ead4cf8f972e07e7a3dcf",
          "row_sha256": "33330662aad9b0aabca193a4577d591936a3f4a7dd7ae7e04ca9277b8d1e435f"
        },
        {
          "content_sha256": "bdaaa46106b642dc48bfe4f588e3695c728149ef98caea67e603a85c0174cd17",
          "logical_id": "mc-f345b815272846cccb6a6b20",
          "row_sha256": "c16cbc36896c8b85ec681828a5885fb77bbf0db4b68488787bb2b6424bfcaaa8"
        },
        {
          "content_sha256": "3dd7f8180dcde8237318af1ed6938a7b2bd6cb841f24dac10031aeb88fb17299",
          "logical_id": "mc-1bb7330a29bdeab1a29274d4",
          "row_sha256": "0cd21aae3ce981e429865fb7b26e93312baf70c60faf1dfe0142cde6440cef32"
        },
        {
          "content_sha256": "93519a5ceac613fa656c70af90f6845bb69d5bd4e0a4e4a4dd14796ce111515f",
          "logical_id": "mc-595c4a33ca5f8d1ef86bb8f3",
          "row_sha256": "feb1d22f755c2b110669e2e53b2a654879fa17640243caeb97ff176f9183e2a8"
        },
        {
          "content_sha256": "c0351f17bb7bdade91065cb68d581055b6d58289558edbafd6b5c6231e4d7c16",
          "logical_id": "mc-0c708fa3eaa5d508bdfa514a",
          "row_sha256": "ad40361b6bfb263918139f33437696d51b76ff9807fa51440d384579266cc2e0"
        }
      ],
      "sha256": "6b3f22aad7ed635638b3958d01e8380e0a2d1d1504676357aad6084cac7f8285",
      "sheet_name": "cards",
      "table_sha256": "ca2492e14d55ee11edb3fa85cb5d3d5ce19a418d9429039efc9431273f9b4556",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 10645,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-07-extern-functions-oral.xlsx",
      "row_count": 4,
      "rows": [
        {
          "content_sha256": "03a5232fba59619757b9a50eb49f180a78558d3a99b146f8b311b3ef9be10c71",
          "logical_id": "mc-80bed66011f61f4bf380f45a",
          "row_sha256": "880531e38a751d6fb9a524fe8b26aa244390211642e81a3693e4863f4494dcc0"
        },
        {
          "content_sha256": "2be6e4c821a92f3009da1a98f5b0b8412429205d8814b9feb81361b45186cdc7",
          "logical_id": "mc-fd69faa9f8c944174f8be4ab",
          "row_sha256": "7cbb99be73ed50274597e1ab81c31a7f7fcc99282ff3777249563054f786427b"
        },
        {
          "content_sha256": "65c04982430bbb747ba15f057d3b93c38833b4c08c98ad4e265d6da630aa3735",
          "logical_id": "mc-fe65c36ff3210d3d70723c7e",
          "row_sha256": "342f96ea9dfa4045205cd7b11e9637e07523acadd868c05925c2d2dfd065febc"
        },
        {
          "content_sha256": "cede291f5eea28e20dab50603e4947c779ce89356618821bd5181256a3de48b9",
          "logical_id": "mc-9ef4217f53d55ccf9549cbed",
          "row_sha256": "4a52782e5573a776c8ce17ddb7b12ef86d7d653683da11f99933f9b514acfb0b"
        }
      ],
      "sha256": "cda98803e161fc90bef6ffa4a7f78f6b9da9e212fd3732480a5ffe05eeb8b5c8",
      "sheet_name": "cards",
      "table_sha256": "ce7c94627bb211b04b2b2e89d6f1983000d81dfff68f56a8a88925b22ed84e23",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "549badb416cf365895b8aa687ba78f4cb6581e3eb97c5cca414ee06b1b66a7f4",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "extern-functions-log",
      "path": "docs/triton-learning/logs/2026-10-05-extern-functions.md",
      "sha256": "d14fe72f393e8417a6b3c261fe1e7501d796bc7444b3af1504b719dcd6308a91",
      "summary": "9/30–10/5：libdevice 全链路、实现路线与后端迁移、asin 练习的纠错与答疑"
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

导入文件：[triton-lesson-07-extern-functions-correction.xlsx](triton-lesson-07-extern-functions-correction.xlsx)（5 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-07-extern-functions-technical-qa.xlsx](triton-lesson-07-extern-functions-technical-qa.xlsx)（15 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-07-extern-functions-oral.xlsx](triton-lesson-07-extern-functions-oral.xlsx)（4 张卡）
