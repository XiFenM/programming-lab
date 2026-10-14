---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "f54d4692b0f15a48dcc989d2bcda6615f381729905836280fe2b9dee37fb56f4",
  "candidate_sha256": "5e2ea306e1b006f382f9684a0481a3c8d074e79bff593c6519556190930819d8",
  "cards": [
    {
      "content_sha256": "f5f4b946814375bc020a8f75517585746a43b29f43e4a99e29fa8d255ac59609",
      "content_summary": "println! 必须在编译期读格式串所以是宏；编译期四步，运行期只加锁按模板写",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "rust 的 println! 为什么必须是宏, 编译期和运行期各做什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-fde08401126f0391a2d220ab",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "adf6eba1d175f2d85531824558129df62cfa172895f59d28a01e8740afc407a6",
      "content_summary": "同一个少传参数的错误: printf 运行期乱码, cout 无格式串, Rust 编译错误; 代价是格式串必须是字面量",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "少传一个参数这个错误在 printf、cout 和 rust 里各何时暴露, rust 换来与付出了什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-8462448c6766cb7b2ff31c56",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c58e531a0efc4f3364a17805c9c47d9c229ac43b50adf2b9a6540fdd2ef08fa4",
      "content_summary": "Debug 的输出照类型定义机械生成所以能 derive; Display 的写法取决于含义, Vec 没有通用写法",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为什么 debug 可以 derive 而 display 必须手写, 标准库为什么不给 vec 实现 display?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-21ab7ca3cacb56731019eb33",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "423a07df552c2aef2500f4822385ec1fa6cb82faa4fff2246ce7cc3f48c59713",
      "content_summary": "Display 输出是类型对外行为; derive 的 Debug 只供调试且格式不稳定, 不该被解析或写进断言",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "display 与 debug 对输出各作了什么承诺, 这对测试和协议意味着什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-b54970ed955536e2c8654658",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "61742638e29059bb3797474b23de0740bd1cc7c7694860544e82d387a5081c94",
      "content_summary": "derive 的 Debug 打印所有字段, 密钥会进日志; 敏感类型要手写 Debug 只列出可公开字段",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "带密钥字段的结构体 derive 了 debug, 用 {:?} 打日志会怎样, 怎么改?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-fe68f0a8578d9a23a0730f6a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "bde5cf43b62440d266e2b736b777da64dce224c667eb7dee3e938345d75760e7",
      "content_summary": "fmt 往 Formatter 里写避免中间字符串并与目的地无关; 返回 Result 只为传递底层写入失败",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "手写 display 时 fmt 为什么往 f 里写而不是返回字符串, 为什么返回 result?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e5f80237194fcc4940320f60",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "83b896be5673fb3a9d36702532f6d5fcec432ddf2d02c79fa32d88f6d62194f2",
      "content_summary": "宽度记在 Formatter 里; write! 新写的占位符不继承它, 转发同一个 f 或用 f.pad 才会生效",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "手写 display 时, 调用方给的宽度和对齐怎样才会生效?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-b2a41220bc9b951bd120c48f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f472541c77d5b78e252479c2d5d8a955a99777ee067b67782ffffd4dd1992e1a",
      "content_summary": "格式说明由类型自己的 fmt 执行: 含义因类型而异, 统一补齐需要临时字符串",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "格式说明为什么交给各类型自己的 fmt 执行, 而不是由 println! 统一补空格?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-54cde4862625fed06d44b76f",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f36303ebc82f3428ea2e3ccc003ad4da52fddf4a055ce0de55c3eff233bf662e",
      "content_summary": "占位符的形状必须编译期确定, 宽度这样的数值可以留到运行期",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为什么宽度可以取自变量而格式串本身不能是变量?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-38556ec04772c01511bbfd34",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "635924aadbdf64de4fba83484c8330a351c3824c99f21c62dfa1098199c54580",
      "content_summary": "整体对齐需要先知道总长度所以要先缓冲; Ipv4Addr 用 15 字节栈上缓冲区再 pad",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "手写 display 时什么情况下先写进缓冲区是合理的, ipv4addr 怎么做?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f6037137047f61095369cd21",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "de2b47a345890ecf6a0a63f8be46e7f818f90d8f3396817a3aa7c89bca64a749",
      "content_summary": "每种占位符对应一个 trait; 类型没实现就编译错误, 浮点数没有 LowerHex, 看位模式先 to_bits",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "一种占位符对应一个 trait 换来了什么, 为什么 {:x} 不能打印浮点数?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5151dc30eec2605731df12bd",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "50edb7eb049000e7956709b4693bdab3d5dd9ec8f32c0f5a56b91b13ec13e0a9",
      "content_summary": "println! 写失败直接 panic: 管道关闭 Broken pipe, 磁盘写满; 改用 writeln! 处理 Result",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "println! 写失败时会怎样, 管道关闭和磁盘写满各是什么表现, 怎么改?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c5ddf16d54145a6a356cb4db",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "721e7014e0026e88372df47dd7c378e7c3ddc7e3093e583217795a702e22bde8",
      "content_summary": "标准输出全进程一把锁且按行缓冲: 多线程在 println! 处排队, 每行一次系统调用",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "多线程里每个请求用 println! 打一行日志会带来什么问题, 原因和改法是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-5c3dc3280d36bebe6fd45dc0",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "06dbad042fd149ebc062d11957513eaab9704b1f56eec11d41aa54b1679ebe07",
      "content_summary": "比较输出文字的测试走不到错误路径; 用自造的会失败的 fmt::Write 逐次注入失败来测",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "怎样测出一个 display 实现丢掉了写入错误?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-eb441b16a75cf5f922a2027b",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "993f5163d14e4a86756ee208cbf651dee0d8cabd47eac63ce3e3a7bfba4cc18b",
      "content_summary": "运行期解析换来的是格式串可为运行期的值, 不是把参数当别的类型打印; Rust 里交给模板引擎",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "把 println 做成运行期解析的函数, 换来的灵活性到底是什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-01801cbabf455741d8c967f4",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3f567d60730d330c65024de1def53d3ee8336047983e18cf0c575bae5a6ea3fc",
      "content_summary": "先拼成字符串再 write! 仍不对齐: 宽度在 f 里; 用 f.pad(&s) 才按 f 的要求写出",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "先 format! 成字符串再 write!(f, \"{}\", s) 能让外层的宽度生效吗?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-6efe12d31b0eb2d4dd4c0c04",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "caa13c61384942d4d0d518b71f164554bfb0a7d284fa4b6c871bb9141a58163c",
      "content_summary": "trait 和类型至少一个是自己 crate 的; 不能为 Vec<Shard> 实现 Display, 改用 Debug 或包一层",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "能不能为 vec<自己的类型> 实现 display, 为什么, 出路是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-e059807e6c996e64024c08d8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e0b6e51c29e251b452e0a8c8f5ffa87e8adb6b8b80d2ed8a09b9a7bd25e45ee0",
      "content_summary": "let _ = 只消警告不传错误: 输出残缺却返回 Ok; fmt 里中间的 write! 要用问号传出错误",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "fmt 里用 let _ = write!(...) 消掉 unused result 警告有什么问题, 该怎么写?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-dfcfc78a75ba00c477b96e96",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7d8767bc99115da0bcc713fe0140e533ccfa3020f5dc532eed049aae151d0208",
      "content_summary": "format! 有堆分配是因为返回 String, 与长度是否确定无关; 长度有上界可用栈上缓冲区",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "先 format! 再 f.pad 的写法为什么有堆分配, 能不能省?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-04279d406ec50634a181281c",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1e31ffbe643e13d9e73248fcc6240f07994bfec499111b271182676dda135cf7",
      "content_summary": "口述 println! 的编译期四步与运行期、Debug 与 Display 的接入方式、与 printf 的取舍和使用边界",
      "dependency_content_sha256": {
        "mc-21ab7ca3cacb56731019eb33": "c58e531a0efc4f3364a17805c9c47d9c229ac43b50adf2b9a6540fdd2ef08fa4",
        "mc-8462448c6766cb7b2ff31c56": "adf6eba1d175f2d85531824558129df62cfa172895f59d28a01e8740afc407a6",
        "mc-c5ddf16d54145a6a356cb4db": "50edb7eb049000e7956709b4693bdab3d5dd9ec8f32c0f5a56b91b13ec13e0a9",
        "mc-e5f80237194fcc4940320f60": "bde5cf43b62440d266e2b736b777da64dce224c667eb7dee3e938345d75760e7",
        "mc-fde08401126f0391a2d220ab": "f5f4b946814375bc020a8f75517585746a43b29f43e4a99e29fa8d255ac59609"
      },
      "depends_on": [
        "mc-21ab7ca3cacb56731019eb33",
        "mc-8462448c6766cb7b2ff31c56",
        "mc-c5ddf16d54145a6a356cb4db",
        "mc-e5f80237194fcc4940320f60",
        "mc-fde08401126f0391a2d220ab"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用 60–90 秒讲清 rust 格式化输出的设计: 编译期与运行期、类型怎样接入、与 printf 的取舍、使用边界。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-08f37fa302e572a98536c443",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8fa058430b3e51027555a03da02b7922eb90f096375f3f257d5492941d4a2dba",
      "content_summary": "口述 println! 在生产中的三个风险: 写失败 panic、全局锁与按行缓冲、Debug 泄露字段",
      "dependency_content_sha256": {
        "mc-5c3dc3280d36bebe6fd45dc0": "721e7014e0026e88372df47dd7c378e7c3ddc7e3093e583217795a702e22bde8",
        "mc-c5ddf16d54145a6a356cb4db": "50edb7eb049000e7956709b4693bdab3d5dd9ec8f32c0f5a56b91b13ec13e0a9",
        "mc-fe68f0a8578d9a23a0730f6a": "61742638e29059bb3797474b23de0740bd1cc7c7694860544e82d387a5081c94"
      },
      "depends_on": [
        "mc-5c3dc3280d36bebe6fd45dc0",
        "mc-c5ddf16d54145a6a356cb4db",
        "mc-fe68f0a8578d9a23a0730f6a"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "rust-formatting",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "用约 60 秒讲清在服务和命令行工具里直接用 println! 输出日志与数据要小心的三件事及处理办法。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-39d4762c35e182d30b7fc955",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "hello-formatting-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "27e50ddfb545d139f6ae0ab13adf8cad0335da2f0f3f76df03bfb568820b5ff0",
  "manifest_payload_sha256": "06340474e68626a719d0aae833545122ff3f37162f7d5122bd0af35ace834d29",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 10723,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/rust-learning/cards/rust-lesson-01-hello-formatting-correction.xlsx",
      "row_count": 5,
      "rows": [
        {
          "content_sha256": "993f5163d14e4a86756ee208cbf651dee0d8cabd47eac63ce3e3a7bfba4cc18b",
          "logical_id": "mc-01801cbabf455741d8c967f4",
          "row_sha256": "8ef22db4ddf2e70dc8382f13fb77587b4b05ec02f1a706ec92a82bf1e3fda96a"
        },
        {
          "content_sha256": "3f567d60730d330c65024de1def53d3ee8336047983e18cf0c575bae5a6ea3fc",
          "logical_id": "mc-6efe12d31b0eb2d4dd4c0c04",
          "row_sha256": "f64ae705aebcd4da2edeb59f7a94c2919f76632905a3a388b43793266993bdb1"
        },
        {
          "content_sha256": "caa13c61384942d4d0d518b71f164554bfb0a7d284fa4b6c871bb9141a58163c",
          "logical_id": "mc-e059807e6c996e64024c08d8",
          "row_sha256": "35b04b2f65b0f2c78d42dbf31dc817e799659025145045dba3becbbd360ff36c"
        },
        {
          "content_sha256": "e0b6e51c29e251b452e0a8c8f5ffa87e8adb6b8b80d2ed8a09b9a7bd25e45ee0",
          "logical_id": "mc-dfcfc78a75ba00c477b96e96",
          "row_sha256": "24236d29975906a176b438e8ddef5d733cfe2968ccdeebe7a9e039d3f2e031b8"
        },
        {
          "content_sha256": "7d8767bc99115da0bcc713fe0140e533ccfa3020f5dc532eed049aae151d0208",
          "logical_id": "mc-04279d406ec50634a181281c",
          "row_sha256": "6dcaff02c343be1686821ff537c430a4ca24eeb43fcf784c7483aca353817f07"
        }
      ],
      "sha256": "7b801fd7e945dfff56cbf5245a1bd91cfa4effa7a75795429c9f983eb597e7ec",
      "sheet_name": "cards",
      "table_sha256": "7d847cd8d935d6bd894d85ac155cdf004550e3eb2da00e39f5f15e420b5c17cd",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 22562,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/rust-learning/cards/rust-lesson-01-hello-formatting-technical-qa.xlsx",
      "row_count": 14,
      "rows": [
        {
          "content_sha256": "f5f4b946814375bc020a8f75517585746a43b29f43e4a99e29fa8d255ac59609",
          "logical_id": "mc-fde08401126f0391a2d220ab",
          "row_sha256": "cc5362f412871101300df55e30f098957ab8429ca72a7e99323fb557055f0110"
        },
        {
          "content_sha256": "adf6eba1d175f2d85531824558129df62cfa172895f59d28a01e8740afc407a6",
          "logical_id": "mc-8462448c6766cb7b2ff31c56",
          "row_sha256": "d85471c692bec8226d32af200944c9aa0c5bc8b7a59f60a31d30f28937616e2f"
        },
        {
          "content_sha256": "c58e531a0efc4f3364a17805c9c47d9c229ac43b50adf2b9a6540fdd2ef08fa4",
          "logical_id": "mc-21ab7ca3cacb56731019eb33",
          "row_sha256": "662bed05c8ebf0eb5a134ca49913d86a661295015b9c0f9423c4dcdb597e945f"
        },
        {
          "content_sha256": "423a07df552c2aef2500f4822385ec1fa6cb82faa4fff2246ce7cc3f48c59713",
          "logical_id": "mc-b54970ed955536e2c8654658",
          "row_sha256": "a4079577904dd3b3fdece26a8c14f130d652f6949f4f1cb6f070d4c0ad124920"
        },
        {
          "content_sha256": "61742638e29059bb3797474b23de0740bd1cc7c7694860544e82d387a5081c94",
          "logical_id": "mc-fe68f0a8578d9a23a0730f6a",
          "row_sha256": "409c42c6e7d9e039ec46a3db58a5e4c7069d738496a6d60a1713f4eecb6ea5a7"
        },
        {
          "content_sha256": "bde5cf43b62440d266e2b736b777da64dce224c667eb7dee3e938345d75760e7",
          "logical_id": "mc-e5f80237194fcc4940320f60",
          "row_sha256": "9460cd1d3426587109367eeb36b429c6a52d0a539a397a0f8d048fbfb92403f1"
        },
        {
          "content_sha256": "83b896be5673fb3a9d36702532f6d5fcec432ddf2d02c79fa32d88f6d62194f2",
          "logical_id": "mc-b2a41220bc9b951bd120c48f",
          "row_sha256": "2bd63516bd2f7f23a125e91161a47dea2ee1d82556529408775509a7c7e058c0"
        },
        {
          "content_sha256": "f472541c77d5b78e252479c2d5d8a955a99777ee067b67782ffffd4dd1992e1a",
          "logical_id": "mc-54cde4862625fed06d44b76f",
          "row_sha256": "1b8c454a13bbd3b22206a3325deb8da3b2ee2149f44d285173fd7a3199765535"
        },
        {
          "content_sha256": "f36303ebc82f3428ea2e3ccc003ad4da52fddf4a055ce0de55c3eff233bf662e",
          "logical_id": "mc-38556ec04772c01511bbfd34",
          "row_sha256": "7d9588b709474f9dbb0b712bf2078c1909afce0d0943fb8a01926f587e602f43"
        },
        {
          "content_sha256": "635924aadbdf64de4fba83484c8330a351c3824c99f21c62dfa1098199c54580",
          "logical_id": "mc-f6037137047f61095369cd21",
          "row_sha256": "917a9a1d803ba5a3aa28d66588fc9fe602f593d3f18167350e2e69f9925c75e9"
        },
        {
          "content_sha256": "de2b47a345890ecf6a0a63f8be46e7f818f90d8f3396817a3aa7c89bca64a749",
          "logical_id": "mc-5151dc30eec2605731df12bd",
          "row_sha256": "22d50d3bb07c3290168625d42414557d2ae065607bf05ff51c39ec12964f3ac6"
        },
        {
          "content_sha256": "50edb7eb049000e7956709b4693bdab3d5dd9ec8f32c0f5a56b91b13ec13e0a9",
          "logical_id": "mc-c5ddf16d54145a6a356cb4db",
          "row_sha256": "556224269c6e3758accdbe2d351bf558ebd47f56c1d0c776155fed4a50128056"
        },
        {
          "content_sha256": "721e7014e0026e88372df47dd7c378e7c3ddc7e3093e583217795a702e22bde8",
          "logical_id": "mc-5c3dc3280d36bebe6fd45dc0",
          "row_sha256": "c92c6616a639d80311a2128565edcc47f0b8c6345026fb2ad9ee528215b7b6f2"
        },
        {
          "content_sha256": "06dbad042fd149ebc062d11957513eaab9704b1f56eec11d41aa54b1679ebe07",
          "logical_id": "mc-eb441b16a75cf5f922a2027b",
          "row_sha256": "ae5c0d33697a8ec4935c6fbc5c9ad4c1cd861f78ebd902c22c39ac28a4f60e92"
        }
      ],
      "sha256": "6d86f5412d4636daf4003fd3325024d218878a748a36c8072ece3e5d729a51f6",
      "sheet_name": "cards",
      "table_sha256": "2891082c7bfb782289d5f59ca7a64c7ea2c7d04a110e5b582881800f68f719eb",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 6082,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/rust-learning/cards/rust-lesson-01-hello-formatting-oral.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "1e31ffbe643e13d9e73248fcc6240f07994bfec499111b271182676dda135cf7",
          "logical_id": "mc-08f37fa302e572a98536c443",
          "row_sha256": "94e1a98552b26e5318080bcf57edd27152c22e01afba50313b7643999eea570e"
        },
        {
          "content_sha256": "8fa058430b3e51027555a03da02b7922eb90f096375f3f257d5492941d4a2dba",
          "logical_id": "mc-39d4762c35e182d30b7fc955",
          "row_sha256": "76e60c9abf6ab9af5aff82dc14dcee7c40fafcd16624aee50eed90af045a4fa9"
        }
      ],
      "sha256": "3bfe38d2577c12a1ee1c495fdd82812bf7fa932fd9d64a6b56812de0d926c4f8",
      "sheet_name": "cards",
      "table_sha256": "ea84c51a282fc92c030807c17af4831ba787bf8d1ddf9d2482c2d2d9e9aaa707",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "63bc78839d255a95e58bfadf9af9e570f6769dd265602cb3fb44b0259c6257a7",
  "sources": [
    {
      "collection": "rust-study-logs",
      "id": "hello-formatting-log",
      "path": "docs/rust-learning/logs/2026-10-08-hello-formatting.md",
      "sha256": "c454612d7411b14e66c04969987f922f3a322d5d36fad571407f33b28b823c43",
      "summary": "10/7–10/8：println! 的六步、Display 与 Debug、格式说明、手写 Display 的纠错与答疑"
    }
  ],
  "target_collection": "rust-cards",
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

导入文件：[rust-lesson-01-hello-formatting-correction.xlsx](rust-lesson-01-hello-formatting-correction.xlsx)（5 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[rust-lesson-01-hello-formatting-technical-qa.xlsx](rust-lesson-01-hello-formatting-technical-qa.xlsx)（14 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[rust-lesson-01-hello-formatting-oral.xlsx](rust-lesson-01-hello-formatting-oral.xlsx)（2 张卡）
