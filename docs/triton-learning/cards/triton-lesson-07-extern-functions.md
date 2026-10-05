---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "2ee60424232f244c288448bb11ae4dd7d1b1f5e1eed0c9ad72c548da882ebb04",
  "candidate_sha256": "e53bce16e42693986a71c8b3cde02eb275fac04b2cdfaefacd5044ec17bbd30c",
  "cards": [
    {
      "content_sha256": "505c4ba582f03e796858d54229cf9a6da75864e9a3701e32bfb1e3e633098025",
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
      "content_sha256": "0c8fb5fc7893c279792f94013561e33c6a29ede1b3e877b8c2a76fff58557e0b",
      "content_summary": "libdevice 函数是 dtype 元组到符号的表，半精度查不到报 KeyError，需先转 fp32",
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
        "recall_target": "libdevice 函数怎样按 dtype 选符号, 半精度输入会怎样?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-498ea0884e7adb7d8db05f93",
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
      "content_sha256": "b8cc5a86b52be7e2712afa0963725d9e764a6989bf202f2d6c14711e3ccffe46",
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
      "content_sha256": "e6d689577f504d5be1148c436868e5ba068424839096de33b90fcf414b79ff9d",
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
      "content_sha256": "78d0804825626235d74f3a6769858895122598a30c02c47bfde5ae261b57fd6a",
      "content_summary": "默认库路径、按需且只拷用到的定义、内容哈希进缓存键、路径错误早报 FileNotFoundError",
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
      "content_sha256": "57cb4513dabb4bf701bff5489f1f0efa981079a2659f80630855e3ed2cd2a51c",
      "content_summary": "默认 FTZ=1、PREC_SQRT=0，相当于 nvcc 的 use_fast_math，只影响 libdevice 内部",
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
      "content_sha256": "9f3e57955de36060e5d4180130409265ed44fb27a75db0568087ee8cf4ae8cac",
      "content_summary": "默认 ftz 使次正规数输入得 0，enable_reflect_ftz=False 后与 torch 一致",
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
      "content_sha256": "916c489bced2612ce016602d427738e895a653ec66ab9baaa2b3f0b257af2ded",
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
      "content_sha256": "895453a90d5ff50477d59c9b7d42c572821eed9f9bfebcdc6f08728383911df9",
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
      "content_sha256": "4d43d513ea2bed69ef2fe94f9789a45f5deb993a41bd9af00868483bf047c82e",
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
      "content_sha256": "1f514b5e6328af6604aafb73a1d24da439d0da604a05e80c38922abd5ce95596",
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
      "content_sha256": "2324a0b4dcc1ee272ef199d2d9fd9429581fe2d788989fb8ff60fe2dfa0a8f0b",
      "content_summary": "自定义库需要 dtype 符号表和经 extern_libs 传入的库文件，缺库在汇编阶段才报错",
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
      "content_sha256": "bebdbd27cb80854fdc616b93681f6cc2273bfb07e84884b14d4853d0739535d9",
      "content_summary": "新后端需提供映射、函数、符号表、库、链接、内联与数值开关，各有对应的失败现象",
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
        "recall_target": "给新后端加 libdevice 支持要提供哪六样东西?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-600578dbdc7e370d7f027260",
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
      "content_sha256": "0fd2ec97733d1ed048dc8d9fadae155d9c656cfbe69de057b9269db02832f55a",
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
      "content_sha256": "4c728ab139a042b82f68343dbfd71af436e773940af7f212c13b3b4b0300c09f",
      "content_summary": "换到 AMD 后符号、每线程元素数、链接库和次正规数默认处理都变，机制不变",
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
      "content_sha256": "ac27b17facb7c1d3f775c0dfe028c07532a2753ea2c717ec9d11a6590ba6abeb",
      "content_summary": "普通赋值使布尔值变张量导致运行期分支，用 tl.constexpr 注解保持编译期",
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
      "content_sha256": "9c11431de1319a240a9182dc73ca0df6bb33464616afcf8e45515f2a7b679790",
      "content_summary": "两家 asin 实现的算法写法不同，fma 条数差异不代表工作量差异",
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
        "recall_target": "同一个 asin 在 nvidia 和 amd 上 fma 条数不同, 说明什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-314b402f4a504bdce2f55d30",
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
      "content_sha256": "7eecf842b6d2667ba6ca27db5757319adcbcbdf3fe39917c11765af6b99aa0dd",
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
      "content_sha256": "f05ec0dae8ef4158d23bfba0b78d4de9fe9f1bdba8e0fd9c3d7071c8cf036a80",
      "content_summary": "包装函数须新建输出张量并返回，不能把输入同时当输出",
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
      "content_sha256": "26e31bc521effbd1483dc435bdb294325d51078da1dda9820b33fd6a505d9c1f",
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
      "content_sha256": "b2fd5db9a75d7c34cb10924a2db89c60342c3a46ec7d59e59cfe6c863b5f5e26",
      "content_summary": "变量被重新绑定后再判断其 dtype 不成立，写回半精度由 tl.store 隐式完成",
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
        "recall_target": "升精度后想把结果转回半精度, 应怎样处理?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-0e7dc3433477cec1c4838123",
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
      "content_sha256": "654467eb40caa2e5189a65226d9e5c79f3d07cb050b76fce2bc2cb4d11829c8e",
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
      "content_sha256": "1919ff49cb1a5a191448486ab17425fc06f668e1440a2dfab5051bb98c3a731b",
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
      "content_sha256": "f2c479b4b0ec30ff1b76b02b0d957262869b118306f4d58b06115460d6673eed",
      "content_summary": "口述 libdevice.asin 从接口替换、查表、逐元素调用到链接、内联与反射参数的全链路",
      "dependency_content_sha256": {
        "mc-498ea0884e7adb7d8db05f93": "0c8fb5fc7893c279792f94013561e33c6a29ede1b3e877b8c2a76fff58557e0b",
        "mc-9555a9080a7ebf622b773758": "505c4ba582f03e796858d54229cf9a6da75864e9a3701e32bfb1e3e633098025",
        "mc-b64417d0916261bcf64ee860": "e6d689577f504d5be1148c436868e5ba068424839096de33b90fcf414b79ff9d",
        "mc-be63c7cf4646448fc25fe75f": "57cb4513dabb4bf701bff5489f1f0efa981079a2659f80630855e3ed2cd2a51c",
        "mc-eb8ba5ca8a041412f7151aef": "78d0804825626235d74f3a6769858895122598a30c02c47bfde5ae261b57fd6a"
      },
      "depends_on": [
        "mc-498ea0884e7adb7d8db05f93",
        "mc-9555a9080a7ebf622b773758",
        "mc-b64417d0916261bcf64ee860",
        "mc-be63c7cf4646448fc25fe75f",
        "mc-eb8ba5ca8a041412f7151aef"
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
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "76105c46bd102d38605e9aaac0ffe370eba149a7c216469429f9e636f9c6495c",
      "content_summary": "口述 Triton 与 eager 数值不一致的三类来源及排查、对齐办法",
      "dependency_content_sha256": {
        "mc-1bb7330a29bdeab1a29274d4": "4c728ab139a042b82f68343dbfd71af436e773940af7f212c13b3b4b0300c09f",
        "mc-314b402f4a504bdce2f55d30": "9c11431de1319a240a9182dc73ca0df6bb33464616afcf8e45515f2a7b679790",
        "mc-6a353374391eea62b23d6433": "9f3e57955de36060e5d4180130409265ed44fb27a75db0568087ee8cf4ae8cac",
        "mc-be63c7cf4646448fc25fe75f": "57cb4513dabb4bf701bff5489f1f0efa981079a2659f80630855e3ed2cd2a51c",
        "mc-e75cf3837f70e205d8f09c3a": "895453a90d5ff50477d59c9b7d42c572821eed9f9bfebcdc6f08728383911df9"
      },
      "depends_on": [
        "mc-1bb7330a29bdeab1a29274d4",
        "mc-314b402f4a504bdce2f55d30",
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
      "source_ids": [
        "extern-functions-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "a8e911665542332a14c16f8b9735a6c60c330f59ef7c953f885a1452bb79c0a3",
  "manifest_payload_sha256": "eabe205e1638394964f632b70ac602e2302ccb29a4cb1c8b24bfe0b2055c3f6f",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 10286,
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
          "content_sha256": "f05ec0dae8ef4158d23bfba0b78d4de9fe9f1bdba8e0fd9c3d7071c8cf036a80",
          "logical_id": "mc-c70f4801d89ce67298d6eb2c",
          "row_sha256": "decfcf5647f9d7adb59efa97996f43ba546a4a207c17c0b657c4233eb486047b"
        },
        {
          "content_sha256": "26e31bc521effbd1483dc435bdb294325d51078da1dda9820b33fd6a505d9c1f",
          "logical_id": "mc-ae58ca5f4ffd85b72b18f8a9",
          "row_sha256": "ab014df3c47ce4c1ea4f38a80fae0358a933a1a06017215a1a51840187526ca4"
        },
        {
          "content_sha256": "b2fd5db9a75d7c34cb10924a2db89c60342c3a46ec7d59e59cfe6c863b5f5e26",
          "logical_id": "mc-0e7dc3433477cec1c4838123",
          "row_sha256": "32b74ca91b0308c1c8ce061b7d018422176ac18363fac3ecdca4662f9ae30875"
        },
        {
          "content_sha256": "654467eb40caa2e5189a65226d9e5c79f3d07cb050b76fce2bc2cb4d11829c8e",
          "logical_id": "mc-90d48b89ad914e50e8961280",
          "row_sha256": "9bda5c32bf4a1ae62fdab069c2644d6f84c9ba72908381115bc19261592bf129"
        },
        {
          "content_sha256": "1919ff49cb1a5a191448486ab17425fc06f668e1440a2dfab5051bb98c3a731b",
          "logical_id": "mc-3c80afdcd4d0a934190abd84",
          "row_sha256": "8b6afc51f9e9e905a9f24160f4233bbf5ffe8556cad0946a2f70a1a971656a6c"
        }
      ],
      "sha256": "3249756808fe13c539c5790ff90fd301fab0b05e62d58595a593cf2c01bf251f",
      "sheet_name": "cards",
      "table_sha256": "1a5d0c6c415e6040d5f7467d9993884ff90efbc7e356094ffebf94d4956a735a",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 28586,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-07-extern-functions-technical-qa.xlsx",
      "row_count": 18,
      "rows": [
        {
          "content_sha256": "505c4ba582f03e796858d54229cf9a6da75864e9a3701e32bfb1e3e633098025",
          "logical_id": "mc-9555a9080a7ebf622b773758",
          "row_sha256": "0107db0e8d37f57c798a64910033359ce97a8d6225ca223c246fd2753293a739"
        },
        {
          "content_sha256": "0c8fb5fc7893c279792f94013561e33c6a29ede1b3e877b8c2a76fff58557e0b",
          "logical_id": "mc-498ea0884e7adb7d8db05f93",
          "row_sha256": "c64c134b9a35b1623dbacb36dc9bcc5005d6ff3ddbfe62434eb4b595b3bfc0b1"
        },
        {
          "content_sha256": "b8cc5a86b52be7e2712afa0963725d9e764a6989bf202f2d6c14711e3ccffe46",
          "logical_id": "mc-58a9421ebbb480690a2063e8",
          "row_sha256": "440005b88f45e51fa16378b7c5f38114ef7efa712ef709acc685a5afc157fc8e"
        },
        {
          "content_sha256": "e6d689577f504d5be1148c436868e5ba068424839096de33b90fcf414b79ff9d",
          "logical_id": "mc-b64417d0916261bcf64ee860",
          "row_sha256": "4c9600e281ef00d9bfa71423715d9eae52fde3d6f67635bb6d5a9fbfcf672f25"
        },
        {
          "content_sha256": "78d0804825626235d74f3a6769858895122598a30c02c47bfde5ae261b57fd6a",
          "logical_id": "mc-eb8ba5ca8a041412f7151aef",
          "row_sha256": "500f7853941dfb648d6de98efc0b43da50b6bb71fbc1493494a5edf46fd579cf"
        },
        {
          "content_sha256": "57cb4513dabb4bf701bff5489f1f0efa981079a2659f80630855e3ed2cd2a51c",
          "logical_id": "mc-be63c7cf4646448fc25fe75f",
          "row_sha256": "125a70da4dec800aed476313552e9d6e0f7e8b5a383997b440ee8477cebe8d6b"
        },
        {
          "content_sha256": "9f3e57955de36060e5d4180130409265ed44fb27a75db0568087ee8cf4ae8cac",
          "logical_id": "mc-6a353374391eea62b23d6433",
          "row_sha256": "51c2c74196a74e337038edfa422ccb67b9b597cd39dac1010e2921229473fdbe"
        },
        {
          "content_sha256": "916c489bced2612ce016602d427738e895a653ec66ab9baaa2b3f0b257af2ded",
          "logical_id": "mc-7f751c559031a02dba76474f",
          "row_sha256": "8b9f742086a23fb790fa99c29eeab6fbbc4bd67dc5a0264c0d72d7507acab7eb"
        },
        {
          "content_sha256": "895453a90d5ff50477d59c9b7d42c572821eed9f9bfebcdc6f08728383911df9",
          "logical_id": "mc-e75cf3837f70e205d8f09c3a",
          "row_sha256": "090ea1643e2c054515b7689afead38a9cbe32a3a670d6a02c681430f57ccb2f7"
        },
        {
          "content_sha256": "4d43d513ea2bed69ef2fe94f9789a45f5deb993a41bd9af00868483bf047c82e",
          "logical_id": "mc-124f818a7fe3826dab719c4d",
          "row_sha256": "112ba296d977608a5877e099dabc493b7353d4de3dda6e9b45e9b1ea58f06c27"
        },
        {
          "content_sha256": "1f514b5e6328af6604aafb73a1d24da439d0da604a05e80c38922abd5ce95596",
          "logical_id": "mc-bf99d430d51b246e6eeb859a",
          "row_sha256": "f076c47f45ed090bf8dde04017485e5890b4ecdbf33683bcb066b3f42f5861c0"
        },
        {
          "content_sha256": "2324a0b4dcc1ee272ef199d2d9fd9429581fe2d788989fb8ff60fe2dfa0a8f0b",
          "logical_id": "mc-096ead4cf8f972e07e7a3dcf",
          "row_sha256": "758a899bd4d18dc9c5c53a6936d29eb495bf79e36ec7556ad4c4955a7c028934"
        },
        {
          "content_sha256": "bebdbd27cb80854fdc616b93681f6cc2273bfb07e84884b14d4853d0739535d9",
          "logical_id": "mc-600578dbdc7e370d7f027260",
          "row_sha256": "f971ae5f9372bc0b93a9d96fc6aa08f6f7eaccf52ff70e703e0e0788e8feb4ce"
        },
        {
          "content_sha256": "0fd2ec97733d1ed048dc8d9fadae155d9c656cfbe69de057b9269db02832f55a",
          "logical_id": "mc-f345b815272846cccb6a6b20",
          "row_sha256": "34993f0562c3c998901e2f2c76f9eac6dd6c3676ce7f7c6cb18c36af366f33d1"
        },
        {
          "content_sha256": "4c728ab139a042b82f68343dbfd71af436e773940af7f212c13b3b4b0300c09f",
          "logical_id": "mc-1bb7330a29bdeab1a29274d4",
          "row_sha256": "38fda73a06589d7e369473f2598e8be94b5a05a6c53f94dcd8e7c8a89705273d"
        },
        {
          "content_sha256": "ac27b17facb7c1d3f775c0dfe028c07532a2753ea2c717ec9d11a6590ba6abeb",
          "logical_id": "mc-595c4a33ca5f8d1ef86bb8f3",
          "row_sha256": "cb8c2b6808b66849f5ed3008f808986c9e4dcd9e5220892471db56809fa1085c"
        },
        {
          "content_sha256": "9c11431de1319a240a9182dc73ca0df6bb33464616afcf8e45515f2a7b679790",
          "logical_id": "mc-314b402f4a504bdce2f55d30",
          "row_sha256": "4462598c407e0bfaa34966e4c519126e883dafddba579db5008b8524c44d1fd5"
        },
        {
          "content_sha256": "7eecf842b6d2667ba6ca27db5757319adcbcbdf3fe39917c11765af6b99aa0dd",
          "logical_id": "mc-0c708fa3eaa5d508bdfa514a",
          "row_sha256": "1fff7e2aab4e9ad4475557954e42d69584861d355cc1a8803ce25b9c5d37e883"
        }
      ],
      "sha256": "008b713513e81b0a60f1816ed363a0a5f72677269f387c85ca3330c74b64a1ba",
      "sheet_name": "cards",
      "table_sha256": "84ca1234760afd5f60047b9c8810ef0c774fa33a9f7bcc099ac01311d1024fe1",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 6463,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-07-extern-functions-oral.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "f2c479b4b0ec30ff1b76b02b0d957262869b118306f4d58b06115460d6673eed",
          "logical_id": "mc-fe65c36ff3210d3d70723c7e",
          "row_sha256": "ea2cf1a8302d8ed19b080a7f41dba2f35a8cfa1b3f0c2c4bbeb4ef9c2a354e9f"
        },
        {
          "content_sha256": "76105c46bd102d38605e9aaac0ffe370eba149a7c216469429f9e636f9c6495c",
          "logical_id": "mc-9ef4217f53d55ccf9549cbed",
          "row_sha256": "0bf90dd3eff8b196fcb5c595d11becd38c914a728d01e3ff16078dda025c3909"
        }
      ],
      "sha256": "272b18e6b58da41c396db4d317ebda9c95aa881e59de6921117ff6f67612c672",
      "sheet_name": "cards",
      "table_sha256": "f69ea58bf3dfaa1bfc663897b5313786b80c0b937296e9ad9ceba842a3a01c24",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "8ac2279c7559f60f72a160c34374bb19c3443e82d3438758b2c6817697dfc0b3",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "extern-functions-log",
      "path": "docs/triton-learning/logs/2026-10-05-extern-functions.md",
      "sha256": "7ec9675ecb1f1079384c1430437678b418f782c93b08ed10f96af9503c2cc066",
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

导入文件：[triton-lesson-07-extern-functions-technical-qa.xlsx](triton-lesson-07-extern-functions-technical-qa.xlsx)（18 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-07-extern-functions-oral.xlsx](triton-lesson-07-extern-functions-oral.xlsx)（2 张卡）
