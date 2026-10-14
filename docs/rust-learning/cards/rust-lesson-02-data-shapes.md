---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "0435089caec0c9467160e6a8395a9517774e58741d7ca61c7b50383be4262764",
  "candidate_sha256": "ea45657ee3c732c78ce84bec7eda2d6e0ba48ddbe0437bcc68aca12edc6461c6",
  "cards": [
    {
      "content_sha256": "080593f6e0dcf87b1fbb1f821050a84d91fae72ce600e93a12221bc2f8005e3a",
      "content_summary": "C 的 u32 乘法先溢出再变宽且无警告; Rust 没有隐式数值转换, 要写出在哪个宽度里算",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "u32 乘出的结果赋给 u64 时, c 和 rust 各发生什么, rust 为什么不做隐式数值转换?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-29301bc27a5b0e2b2dcb6c78",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e236d784f85922e3ba98f79bb7ccd54808badae81fabbac6a3730d4311c03ff0",
      "content_summary": "Rust 整数溢出不是未定义行为: 常量编译错误, 调试构建 panic, 发布构建补码回绕",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "rust 的整数溢出在常量、调试构建、发布构建下各怎样, 和 c 有什么不同, 为什么这样规定?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-06abc5395a9b603631fed773",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b4c90e3fa1062e1822ed35b8eb8311ac503c587d159cdd33df5b3b94f2cb0c39",
      "content_summary": "不可信输入的大小计算用 checked_* 把溢出变成 None; wrapping 用于哈希等, saturating 卡上下限",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用不可信的 shape 算大小时乘法该怎么写, checked、wrapping、saturating 三组方法各用在哪?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-55fbc5a19e7081dafd2b429b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "e23f427069dbda907dbcf4001e4b2d7e4f5d9abb541471803516cf0b2cb1cffa",
      "content_summary": "切片把指针和长度做成一个值: 函数能收任意长度, 下标可检查; 代价是 16 字节和每次下标的比较",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "切片为什么是指针加长度, 解决了什么问题, 代价是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4071e1fefb04731b071bb454",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f4166023843059ce9bee3a9b15dca7af9f4a05890f103382121f261bff6c25bc",
      "content_summary": "数组的值是元素本身且长度在类型里; Vec 拥有堆上数据; 切片是借来的指针加长度; 参数写 &[T]",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "[t; n]、vec<t>、&[t] 三者在长度、值的内容、所有权上有什么区别, 参数该写哪种?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-622dee7e9718a371ab920273",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7295233a9b0a46e5726d08d9d7dea91099844a23fdbf8da77e203f847774c7df",
      "content_summary": "越界检查在发布构建也保留: 溢出只是算错数, 越界会碰到不属于你的内存",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "发布构建里下标越界检查还在吗, 为什么和溢出检查的处理不同?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a3f20551112c767c640656da",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1db7ccf3eac678500ef6643b309ad378d13e62da342fb2f5d3687542b5875321",
      "content_summary": "胖指针多带的字由指向的类型决定: 切片是元素个数, str 是字节数, dyn Trait 是虚表地址",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "胖指针多带的那个字是什么, 由什么决定, 和 c++ 的虚表指针放法有何不同?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3a02ddd141c936f4dd69b0f7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c2eee750e7ce42149fc4535d7b307f21b5ce3b42ed39885eabea9f87a5fd6521",
      "content_summary": "safetensors 取张量只是切一段 &[u8], 16 字节的切片描述 1.09 GB, 配合 mmap 零复制",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "snapshot",
          "product": "safetensors",
          "version": "0.8.0"
        },
        "recall_target": "safetensors 从权重文件取出一个张量时复制了多少数据, 为什么能做到?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-5f8a5bff4006a6de702833fe",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ac3cb074c2d8be91d59d42e622ec98fbb8b01dcd2019a5ed1ee0f417fcae968b",
      "content_summary": "字符串按 UTF-8 存, len 是字节数; 不能按下标取字符, 按字符用 chars()",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "rust 字符串的 len 为什么是字节数, 为什么不能按下标取字符?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-ddad0bc752c8166b1239f7b9",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4e066716630dab50605ede48fc29a8ba5358999680a140003aebe4c8247373bb",
      "content_summary": "Rust 默认可重排字段以省填充, 不承诺布局; 与 C 或文件格式对接时用 repr(C)",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "rust 默认怎样摆 struct 的字段, 为什么敢重排, 带来什么限制, repr(c) 何时需要?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-eede1301bdde51f0a67f2f7a",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dd9071c294dd2730b3cff0c887f4909f1a76ec09c99332eecc96bc14d84b013f",
      "content_summary": "C 的 enum 加 union 可不一致、可漏分支、可塞任意整数; Rust 的 enum 把三者都变成做不到或编译错误",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "c 的标签加联合有哪三个洞, rust 的 enum 怎样堵上?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-40a03a3c79485eba297026ee",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "72ff6bf93728ed0a961a665ca44949d0be9bf74119d785818eb5c955c06efec8",
      "content_summary": "enum 大小是最大变体加标签并按对齐凑整; 载荷有用不到的取值时标签藏进去, Option<Box> 仍 8 字节",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "enum 的值多大由什么决定, option<u32>、option<box<u32>>、option<bool> 的大小各怎么解释?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d56d18bd285cb83db2012ce9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7266945325274700757e30f84d98e7522b45a4be8cf2059eb825ca6d682df9bb",
      "content_summary": "取载荷必须经过写明变体的模式; match、if let、let else、matches! 各有用处, 后三者不做穷尽检查",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "为什么取 enum 的载荷必须经过模式, 有哪几种写法, 加变体时各自表现如何?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-90f8cfd884bf298456b78bae",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6c9e630a4e33517b8cc5eee1f2e5ec231dbac2e33d31660a94f77cb76a578c60",
      "content_summary": "变体带一个自明的数据用圆括号, 多个或含义不明用带字段名的花括号; 布局相同",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "enum 的变体什么时候用圆括号, 什么时候用带字段名的花括号?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-ccbcd805a534a7e17aa8ee56",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "51f375a1a02090d819a66fae0f5a772d9858c2c0d383d8b7884246fea2cbd81e",
      "content_summary": "kind 加全部字段的 struct 允许非法状态; enum 让每种状态只带自己的数据并强制先判断",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用 kind 字段加全部字段的 struct 表示多种状态有什么问题, 改成 enum 换来什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f613c30693f458f560c5b49d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1367823ffed5229bbb25e339dfaaa4a310c921080df1c633bfaf299b8a8bf7af",
      "content_summary": "有名字的字段直接访问, 元组用解构起名, 多层判断用嵌套模式把 match 套 match 压平",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "字段访问、解构、嵌套模式各适合什么情况, 嵌套模式怎样压平 match 套 match?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d78212cfe235c254e23fb99a",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0e982ac8fdb4f711f175617d346db113c2ccc97076fa20abc002fb6b0121c24c",
      "content_summary": "variant 与 Rust enum 思路相同; variant 取错成员运行时才抛, 漏分支报模板错误, 实测更占空间",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "rust 的 enum 与 c++ 的 std::variant 在漏处理、取错成员、占用空间上有何不同?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-5ed1a803e725ffff0bf76663",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "1e21d89ad53e16a9ed69f81563525c5b47883ee17e12e73b4c5f50ad2bc3ca1d",
      "content_summary": "类型直接包含自己会让大小无穷; Box 是固定 8 字节且独占堆上值的指针, 代价是分配和一次跳转",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "递归类型为什么必须隔一层 box, box 起什么作用, 代价是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-f16304c56dfec962fa354f2c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f69a619878a0c48eb90cadbe43cde12eae4d7d18e5196d9eb61895ce38bca992",
      "content_summary": "Box 拥有堆上的值并负责释放, &mut 只是临时借来改; 借用不能比原主久, 违反则编译不过",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "box<t> 与 &mut t 的根本区别是什么, 在哪里看得出来, 各用在什么场合?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-01ad1a4c01f198e929d69fdd",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c279f50acdc9bedb0ed10277401427c1c4676b77d4f7553b9f6e1ba84aafd235",
      "content_summary": "const 值被内联到每个使用处且无固定地址; static 是唯一的一块内存; 全局可变状态用 static 加原子类型",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "const 与 static 的区别是什么, 默认用哪个, 全局可变计数器怎么做?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-84ddf7e4e2a9bcc346832955",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "cb1e3f457e0d9d67032f40b9c52b6067cdfda43888a287732b707a2ee99146e2",
      "content_summary": "普通乘法在发布构建回绕后, 凑好的形状会通过校验; 普通坏输入碰巧被拒绝所以测试发现不了",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "把大小计算里的 checked_mul 换成普通乘法, 发布构建下为什么比崩溃更危险, 测试为何发现不了?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-18fd290085069e62fc1963ab",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8e223a9872015ae404b2949b67ab47de14e8e781f0812cc418f6fd0f5874a24e",
      "content_summary": "u32 与 &u32 是两个类型: & 取地址, * 顺地址读值; 传参、返回、构造时要值就写 *, 点号自动解引用",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用值与地址的模型解释 & 和 * 各做什么, 什么时候必须写 *?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d7d675f13ece58f3d2234601",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c0fc443952f98217a9afb8a6cad068169ee619bdd55fe44e2de5182b67b4debd",
      "content_summary": "Rust 的引用可存可改指向且取值写 *, 但不为空、无指针运算, 悬垂由编译器防; 裸指针需 unsafe",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "rust 的 &t 与 c 的指针、c++ 的引用相比, 像在哪里, 不像在哪里?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-aebe27dd15103dd698e65e0e",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ab449ce2767c0c0916f6fdc05a753f7afdcc40766316edcfd55b2e0169257e79",
      "content_summary": "&self 传地址且调用后值仍可用; self 把值移动进方法, 适合消耗值或小的可复制类型",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "方法的接收者写 &self 与写 self 有什么区别, 什么时候该用 self?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-bb6e7a927edb06c6bb103e32",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "613af88c39a5f6e52d3d7927d40427fbece9d630a6fda5a127539b6a4e25cae8",
      "content_summary": "for s in &v 只借且得到元素的引用; for s in v 把 Vec 移动进循环; C++ 的范围 for 只是逐个复制",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "for s in &v 与 for s in v 有什么区别, 和 c++ 的范围 for 一样吗?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-2f8a90c77d628a8aac08bf98",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "b1093aca78613f4693c184f89b79a1ba12b90008ebf9b88794564f377045c6a1",
      "content_summary": "传值默认移动; 调用处可移动、借出或 clone 后移动; 只读时首选借出",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "把不能按字节复制的值直接传给函数会怎样, 调用处有哪三种写法?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-45c2bc75f325bd8d0893789e",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "9b9d007c53eaf64ac3c0c1482d01c5f1b1072f268a357962dd9e49c4c3ccd366",
      "content_summary": "所有字段都是 Copy 类型才能是 Copy; Vec 照抄会重复释放; 要副本用显式的 clone",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "带 vec 字段的类型为什么不能 derive copy, copy 与 clone 各是什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-21dcf2ed0dcf3bae97e82554",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c23fd248b361666ec47656264016449474a38e33d7820443a6c786e58a6685fb",
      "content_summary": "Eq 只是任何值等于自己的承诺; 浮点数的 NaN 做不到所以只有 PartialEq; 哈希表的键要求 Eq",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "eq 比 partialeq 多了什么, 为什么带浮点字段的类型不能 derive eq?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-df219766ae26f6cfc1f86c56",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "382b8083b50c920d62febbc8146b5c0cfcadba9791e30fdd93545d57570ddf41",
      "content_summary": "点号取字段和调方法时自动借用与解引用, 取代了 ->; 传参和运算时仍要自己写 & 和 *",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "点号在取字段和调方法时自动做了什么, 完整写法是什么, 和 c 的 -> 是什么关系?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3398b0849ce57fba895402f1",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2e3c80d9b22c16174d7e9c9d20afbe29b0cf1e3ceca902558adbad649286b54d",
      "content_summary": "as 的截断不受溢出检查保护, 两种构建都静默; 大于 4 GiB 的偏移 as u32 会悄悄算错",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用 as 把 usize 的偏移转成 u32 有什么风险, 它受溢出检查保护吗?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-6bd38147a9b9d3d99c1be3b6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "82aa96f08a5b3ec0d4826408924c4c54e68661db7b5b167c2349002785f0bcc4",
      "content_summary": "数组的值就是元素本身: 长度须编译期确定, 且 1.09 GB 会内嵌在值里并被复制",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "把借来的切片字段换成定长数组字段, 会失去什么, 多付出什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-dd34bed268308fe47e3a0aeb",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "108352448d3f8ff4cc1d9cc0007365106735166efac6a0a1377ed2a4a0b5f166",
      "content_summary": "下标与 get 做同一个范围检查; 不通过时下标 panic 而 get 返回 None; 外部来的范围用 get",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "&data[a..b] 与 data.get(a..b) 在检查上有什么区别, 各用在什么场合?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-22db894cf72f898560a83624",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5ca24f4139c9753eb44e35c57a79810498ebaa375d5343c2311956ca31126eb3",
      "content_summary": "对齐取字段中最大的对齐, 大小是对齐的整数倍; 对齐 8 只是因为含指针或 64 位整数",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "所有类型的大小都按 8 对齐吗, 对齐和大小是怎样决定的?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-a8fc4c5780df6377438b130c",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "88846dda54213d2bc9234b994cae3882ee91cea32f1dcefac1b2c166fc78217f",
      "content_summary": "Tree 是 16 字节: 按规则应凑整到 24, 但 Box 不为 0, 标签借用了第一个指针的 0 值",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "带两个 box 的 enum tree 一个值多大, 为什么不是 20 也不是 24?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-91f72a8f282561086a05fa85",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d41c9fa1988642c300147e04aefa8c452f6993ed993b8a8449e9bbb2f262c5a9",
      "content_summary": "下划线兜底写于新变体出现之前且关掉编译器的提醒; 逐个列出的 match 在加变体时会报错",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "给 enum 加变体后, 逐个列出的 match 与带下划线兜底的 match 各会怎样?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c7917bb1c882d7394df00142",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "3878f419a77447d0e8ac755efde9645424655e2d54d5be2e51f9adea6945a30b",
      "content_summary": "Some 是 Option 的变体而非标签; 标签是记录变体的整数, 载荷是变体带的值",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "some 是什么, 它和标签、载荷是什么关系?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-8bd49db18dd5d828ddfc95ed",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4d29064aa5141caa713e45e6d65b322930c393bbb6b6a19f2bc95a0d26637b87",
      "content_summary": "enum 大小由最大变体决定: 把最大变体的字段整体搬进 struct 再装箱, 192 字节降到 48",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "commit": "43f5393dc456c1047d316d14be6acb662cce6db7",
          "kind": "snapshot",
          "product": "atom"
        },
        "recall_target": "想让 enum 的每个值变小, 应该把哪个变体的什么装进 box?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3aa54a161c600b41fd63daf6",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5d574e0052ef218c5d76dfba53f4d425ecd302191584e94b89b329f60970d1b2",
      "content_summary": "const 的每次使用都是一份新值, 连读取也是, 所以输出 0; 共享的可变状态要用 static",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "把 static 的原子计数器改成 const 之后, 两次加一再读取会得到多少, 为什么?"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-9e5269f3ad9b0d1cd0f197c7",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "baa1d99a9d3118797f1ccf2a0e8a7e0e044af5960ff48c3779f25a5d2ca86ce0",
      "content_summary": "安全保证的代价是运行时的边界检查和必须写的分支, 不是编译器检查; 内存没有变大",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "rust 用切片和 option 换来的保证, 代价到底是什么?"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a258a0ba5746f9ca1dacb152",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "03838c3818079f243842814c7b6e521ff56602402cb7c8413ff347e0a2cb5afe",
      "content_summary": "口述 C 的指针加长度与可空指针对应 Rust 的切片与 Option: 大小不变, 多了绑定与检查, 代价在运行时",
      "dependency_content_sha256": {
        "mc-4071e1fefb04731b071bb454": "e23f427069dbda907dbcf4001e4b2d7e4f5d9abb541471803516cf0b2cb1cffa",
        "mc-90f8cfd884bf298456b78bae": "7266945325274700757e30f84d98e7522b45a4be8cf2059eb825ca6d682df9bb",
        "mc-a258a0ba5746f9ca1dacb152": "baa1d99a9d3118797f1ccf2a0e8a7e0e044af5960ff48c3779f25a5d2ca86ce0",
        "mc-a3f20551112c767c640656da": "7295233a9b0a46e5726d08d9d7dea91099844a23fdbf8da77e203f847774c7df",
        "mc-d56d18bd285cb83db2012ce9": "72ff6bf93728ed0a961a665ca44949d0be9bf74119d785818eb5c955c06efec8"
      },
      "depends_on": [
        "mc-4071e1fefb04731b071bb454",
        "mc-90f8cfd884bf298456b78bae",
        "mc-a258a0ba5746f9ca1dacb152",
        "mc-a3f20551112c767c640656da",
        "mc-d56d18bd285cb83db2012ce9"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用 60–90 秒回答: c 的 (指针, 长度) 与可空指针在 rust 里对应什么, 内存是否变大, 多保证了什么, 代价是什么。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-4c222a4a73430d0a23d4b090",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "8f9a9ed5c167883b260917aea618a3983ce85e09ab2cfe02befe2150ac2bfb4d",
      "content_summary": "口述 Rust enum 的布局、相对 C 的三项保证、与 variant 的差别以及两条代价",
      "dependency_content_sha256": {
        "mc-40a03a3c79485eba297026ee": "dd9071c294dd2730b3cff0c887f4909f1a76ec09c99332eecc96bc14d84b013f",
        "mc-5ed1a803e725ffff0bf76663": "0e982ac8fdb4f711f175617d346db113c2ccc97076fa20abc002fb6b0121c24c",
        "mc-90f8cfd884bf298456b78bae": "7266945325274700757e30f84d98e7522b45a4be8cf2059eb825ca6d682df9bb",
        "mc-c7917bb1c882d7394df00142": "d41c9fa1988642c300147e04aefa8c452f6993ed993b8a8449e9bbb2f262c5a9",
        "mc-d56d18bd285cb83db2012ce9": "72ff6bf93728ed0a961a665ca44949d0be9bf74119d785818eb5c955c06efec8"
      },
      "depends_on": [
        "mc-40a03a3c79485eba297026ee",
        "mc-5ed1a803e725ffff0bf76663",
        "mc-90f8cfd884bf298456b78bae",
        "mc-c7917bb1c882d7394df00142",
        "mc-d56d18bd285cb83db2012ce9"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "snapshot",
          "product": "rust",
          "version": "1.97.1"
        },
        "recall_target": "用 60–90 秒讲清 rust 的 enum 相对 c 的 enum 加 union、c++ 的 variant: 布局、保证与代价。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-d4bf55f60282677744e473c0",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c82ee2a6a1ed9caa87a6e0fa581776dbe27072bd9ed0e6412534e311748b300a",
      "content_summary": "口述解析不可信文件头: 溢出在发布构建静默、as 静默截断、用 checked 运算和 get, 并举出回绕被接受的输入",
      "dependency_content_sha256": {
        "mc-06abc5395a9b603631fed773": "e236d784f85922e3ba98f79bb7ccd54808badae81fabbac6a3730d4311c03ff0",
        "mc-18fd290085069e62fc1963ab": "cb1e3f457e0d9d67032f40b9c52b6067cdfda43888a287732b707a2ee99146e2",
        "mc-22db894cf72f898560a83624": "108352448d3f8ff4cc1d9cc0007365106735166efac6a0a1377ed2a4a0b5f166",
        "mc-55fbc5a19e7081dafd2b429b": "b4c90e3fa1062e1822ed35b8eb8311ac503c587d159cdd33df5b3b94f2cb0c39",
        "mc-6bd38147a9b9d3d99c1be3b6": "2e3c80d9b22c16174d7e9c9d20afbe29b0cf1e3ceca902558adbad649286b54d"
      },
      "depends_on": [
        "mc-06abc5395a9b603631fed773",
        "mc-18fd290085069e62fc1963ab",
        "mc-22db894cf72f898560a83624",
        "mc-55fbc5a19e7081dafd2b429b",
        "mc-6bd38147a9b9d3d99c1be3b6"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "rust-data-shapes",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用 60–90 秒讲清解析不可信的权重文件头时, rust 在大小计算和取数据上哪里帮你、哪里要自己小心。"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-3a870011f6ef84f7e0efac6f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "data-shapes-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "fdb4a4a8ea7610d5e24d0e4915887fac0f66b26ea65148c322cf57e0aa6df21b",
  "manifest_payload_sha256": "a60c026c729992a78b7c2e975dd0b059bc5af7c70f551a93acc5ab215a74df87",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 17548,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/rust-learning/cards/rust-lesson-02-data-shapes-correction.xlsx",
      "row_count": 10,
      "rows": [
        {
          "content_sha256": "2e3c80d9b22c16174d7e9c9d20afbe29b0cf1e3ceca902558adbad649286b54d",
          "logical_id": "mc-6bd38147a9b9d3d99c1be3b6",
          "row_sha256": "6f430749fba4ed4785341839f5645935b0dec407b1dc042e3bfa8a8872731223"
        },
        {
          "content_sha256": "82aa96f08a5b3ec0d4826408924c4c54e68661db7b5b167c2349002785f0bcc4",
          "logical_id": "mc-dd34bed268308fe47e3a0aeb",
          "row_sha256": "e432904acc3f50c8b87172b44ffd6391aba626f034e0f99b1045fbd8885ace7c"
        },
        {
          "content_sha256": "108352448d3f8ff4cc1d9cc0007365106735166efac6a0a1377ed2a4a0b5f166",
          "logical_id": "mc-22db894cf72f898560a83624",
          "row_sha256": "bd6a9189c711e5fe0fa75c1d2d5c36b90156a1e2fb6fa89605ff3b1534a3f091"
        },
        {
          "content_sha256": "5ca24f4139c9753eb44e35c57a79810498ebaa375d5343c2311956ca31126eb3",
          "logical_id": "mc-a8fc4c5780df6377438b130c",
          "row_sha256": "df5352dea07e3323a102e59e189b978c4cd8cd3eafad15b88ba0f61213c949f5"
        },
        {
          "content_sha256": "88846dda54213d2bc9234b994cae3882ee91cea32f1dcefac1b2c166fc78217f",
          "logical_id": "mc-91f72a8f282561086a05fa85",
          "row_sha256": "0008cdb33d1c802c53775b99f65a9e308807b6c97ed7835ce773ed80ec90e051"
        },
        {
          "content_sha256": "d41c9fa1988642c300147e04aefa8c452f6993ed993b8a8449e9bbb2f262c5a9",
          "logical_id": "mc-c7917bb1c882d7394df00142",
          "row_sha256": "e66fb7a3b8c70ff2062ddd052653f2ce121521c2dfd509f11f37dae62ac0d6b7"
        },
        {
          "content_sha256": "3878f419a77447d0e8ac755efde9645424655e2d54d5be2e51f9adea6945a30b",
          "logical_id": "mc-8bd49db18dd5d828ddfc95ed",
          "row_sha256": "5c2e2310c184e6552872d0a565e155800117b0a661c7ee4a7023d72a66e5acbe"
        },
        {
          "content_sha256": "4d29064aa5141caa713e45e6d65b322930c393bbb6b6a19f2bc95a0d26637b87",
          "logical_id": "mc-3aa54a161c600b41fd63daf6",
          "row_sha256": "d2996e8620e910766a2409b02527d6553f5bdc0165423566eeac87f7917039fa"
        },
        {
          "content_sha256": "5d574e0052ef218c5d76dfba53f4d425ecd302191584e94b89b329f60970d1b2",
          "logical_id": "mc-9e5269f3ad9b0d1cd0f197c7",
          "row_sha256": "815b6866e0d2794fc68e6909bc12b58b63b27b902d37b19172d170c6d3090280"
        },
        {
          "content_sha256": "baa1d99a9d3118797f1ccf2a0e8a7e0e044af5960ff48c3779f25a5d2ca86ce0",
          "logical_id": "mc-a258a0ba5746f9ca1dacb152",
          "row_sha256": "acc95982146660f548487d4b365fc3a04fb71647492b085c261f2e63cdc7f20f"
        }
      ],
      "sha256": "a834021eaba9b6f6541c7e8a9085ed65b0d804b568c6f6aa4ddbbaa54b6e06e4",
      "sheet_name": "cards",
      "table_sha256": "949e3061a90de55aa9555208b7c1112b987459467137fa02033d5ad2227e6f99",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 43184,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/rust-learning/cards/rust-lesson-02-data-shapes-technical-qa.xlsx",
      "row_count": 29,
      "rows": [
        {
          "content_sha256": "080593f6e0dcf87b1fbb1f821050a84d91fae72ce600e93a12221bc2f8005e3a",
          "logical_id": "mc-29301bc27a5b0e2b2dcb6c78",
          "row_sha256": "c77a66af26f27414b8528b7da30afe05fb8794f600381796a927dc864e9cac46"
        },
        {
          "content_sha256": "e236d784f85922e3ba98f79bb7ccd54808badae81fabbac6a3730d4311c03ff0",
          "logical_id": "mc-06abc5395a9b603631fed773",
          "row_sha256": "d95a053c6f7e08cd65722fafaa334e6511dbb6afbf8872d5b168ee59370be652"
        },
        {
          "content_sha256": "b4c90e3fa1062e1822ed35b8eb8311ac503c587d159cdd33df5b3b94f2cb0c39",
          "logical_id": "mc-55fbc5a19e7081dafd2b429b",
          "row_sha256": "981f4ad41c35c3bafd12712b7bc1e174b3ab4aa566ade27efe396829e8403af9"
        },
        {
          "content_sha256": "e23f427069dbda907dbcf4001e4b2d7e4f5d9abb541471803516cf0b2cb1cffa",
          "logical_id": "mc-4071e1fefb04731b071bb454",
          "row_sha256": "6411b394736e508bd2d885968a80cfda7df1e038c1a73e2a0f1077ef41dd8d3e"
        },
        {
          "content_sha256": "f4166023843059ce9bee3a9b15dca7af9f4a05890f103382121f261bff6c25bc",
          "logical_id": "mc-622dee7e9718a371ab920273",
          "row_sha256": "1becbc79b30d4d7741dd95b13efe90bc5e6e0ea4ece27528f62d746473f6fb55"
        },
        {
          "content_sha256": "7295233a9b0a46e5726d08d9d7dea91099844a23fdbf8da77e203f847774c7df",
          "logical_id": "mc-a3f20551112c767c640656da",
          "row_sha256": "62f1b6925ca9d731a58d637b3d6c089102bfbdb19c188a1192fba88bcc1b491a"
        },
        {
          "content_sha256": "1db7ccf3eac678500ef6643b309ad378d13e62da342fb2f5d3687542b5875321",
          "logical_id": "mc-3a02ddd141c936f4dd69b0f7",
          "row_sha256": "6a19cdb106bef7eda81ec8a1cc5f2c04e20031fa494b28c03e82d34eeb04e96e"
        },
        {
          "content_sha256": "c2eee750e7ce42149fc4535d7b307f21b5ce3b42ed39885eabea9f87a5fd6521",
          "logical_id": "mc-5f8a5bff4006a6de702833fe",
          "row_sha256": "35fdf893314b9f595a072c8694342adc0a5e1aa7c50323a926d56fc3d916a960"
        },
        {
          "content_sha256": "ac3cb074c2d8be91d59d42e622ec98fbb8b01dcd2019a5ed1ee0f417fcae968b",
          "logical_id": "mc-ddad0bc752c8166b1239f7b9",
          "row_sha256": "00ddab08d8cd8848b1847eeda9891c4bfdd5d1299ff26e5b387c12cc57876491"
        },
        {
          "content_sha256": "4e066716630dab50605ede48fc29a8ba5358999680a140003aebe4c8247373bb",
          "logical_id": "mc-eede1301bdde51f0a67f2f7a",
          "row_sha256": "403c66baa741df8b99029f0d51ec7203071eb9252f09e4227f750d9ddfa7ef7f"
        },
        {
          "content_sha256": "dd9071c294dd2730b3cff0c887f4909f1a76ec09c99332eecc96bc14d84b013f",
          "logical_id": "mc-40a03a3c79485eba297026ee",
          "row_sha256": "38c3cb6c30a9f2def32ef044054053a810f029701f26db69e670c8b4567feee3"
        },
        {
          "content_sha256": "72ff6bf93728ed0a961a665ca44949d0be9bf74119d785818eb5c955c06efec8",
          "logical_id": "mc-d56d18bd285cb83db2012ce9",
          "row_sha256": "18ed1c7a769e54fa6cc896435df8d44706eac75accda161f8032e66f4d41815a"
        },
        {
          "content_sha256": "7266945325274700757e30f84d98e7522b45a4be8cf2059eb825ca6d682df9bb",
          "logical_id": "mc-90f8cfd884bf298456b78bae",
          "row_sha256": "eb79850b3d598171146e43644fdf31dc3faecc11f650d0f84cc48954cb6d8fab"
        },
        {
          "content_sha256": "6c9e630a4e33517b8cc5eee1f2e5ec231dbac2e33d31660a94f77cb76a578c60",
          "logical_id": "mc-ccbcd805a534a7e17aa8ee56",
          "row_sha256": "1c37acbbc48a0d1431b971003487b840f2bd43ccddf9d8b8a4f7131b081155ca"
        },
        {
          "content_sha256": "51f375a1a02090d819a66fae0f5a772d9858c2c0d383d8b7884246fea2cbd81e",
          "logical_id": "mc-f613c30693f458f560c5b49d",
          "row_sha256": "8cd05df6eec578c328c7a6931a1094cb1794076fc5ffecbdf708f9afec490ccc"
        },
        {
          "content_sha256": "1367823ffed5229bbb25e339dfaaa4a310c921080df1c633bfaf299b8a8bf7af",
          "logical_id": "mc-d78212cfe235c254e23fb99a",
          "row_sha256": "d70f982d3d5ad6b08dca849edc7f3b1fbe7f6cdedcccb6c93885c283cd4a53a4"
        },
        {
          "content_sha256": "0e982ac8fdb4f711f175617d346db113c2ccc97076fa20abc002fb6b0121c24c",
          "logical_id": "mc-5ed1a803e725ffff0bf76663",
          "row_sha256": "433dc6e10c33e78081845ace14f809d7c0c391729d06fe9714ea911255538d3e"
        },
        {
          "content_sha256": "1e21d89ad53e16a9ed69f81563525c5b47883ee17e12e73b4c5f50ad2bc3ca1d",
          "logical_id": "mc-f16304c56dfec962fa354f2c",
          "row_sha256": "9f23d5623a7999296ce3030ee51d4568af927de8e29ee5a1496de4a48c0c2bc7"
        },
        {
          "content_sha256": "f69a619878a0c48eb90cadbe43cde12eae4d7d18e5196d9eb61895ce38bca992",
          "logical_id": "mc-01ad1a4c01f198e929d69fdd",
          "row_sha256": "146811c8edadcec5c4edb6b4efd4653f86368f0aafb1c1bf02292f679366430e"
        },
        {
          "content_sha256": "c279f50acdc9bedb0ed10277401427c1c4676b77d4f7553b9f6e1ba84aafd235",
          "logical_id": "mc-84ddf7e4e2a9bcc346832955",
          "row_sha256": "e072128730805fdead5f7dac11c8682667b52ef4361198981a314192ca310191"
        },
        {
          "content_sha256": "cb1e3f457e0d9d67032f40b9c52b6067cdfda43888a287732b707a2ee99146e2",
          "logical_id": "mc-18fd290085069e62fc1963ab",
          "row_sha256": "5e0249169a72a3018b1e72a500f64b64fb62fbcc5ab76c63a1783c5db960018c"
        },
        {
          "content_sha256": "8e223a9872015ae404b2949b67ab47de14e8e781f0812cc418f6fd0f5874a24e",
          "logical_id": "mc-d7d675f13ece58f3d2234601",
          "row_sha256": "0646eab6581f003b804fa17b366c48130b5112b25b49de98c8df80012e3390c4"
        },
        {
          "content_sha256": "c0fc443952f98217a9afb8a6cad068169ee619bdd55fe44e2de5182b67b4debd",
          "logical_id": "mc-aebe27dd15103dd698e65e0e",
          "row_sha256": "247e2b10c88652902f5a7d157a11af528a255a8f951fd7daf9fbc9c610031462"
        },
        {
          "content_sha256": "ab449ce2767c0c0916f6fdc05a753f7afdcc40766316edcfd55b2e0169257e79",
          "logical_id": "mc-bb6e7a927edb06c6bb103e32",
          "row_sha256": "c148a5832088201b05580854139a0c320826ebc37b26040d9f29160445639677"
        },
        {
          "content_sha256": "613af88c39a5f6e52d3d7927d40427fbece9d630a6fda5a127539b6a4e25cae8",
          "logical_id": "mc-2f8a90c77d628a8aac08bf98",
          "row_sha256": "fe021fca7a0e831fde5277b21c10bbb09cbfb297c2cb941104d1b24f46521a12"
        },
        {
          "content_sha256": "b1093aca78613f4693c184f89b79a1ba12b90008ebf9b88794564f377045c6a1",
          "logical_id": "mc-45c2bc75f325bd8d0893789e",
          "row_sha256": "e0fcbf8ca72fe4ffffa50b0d3fe9182ca76bbc13375a4b327161dab791c1bcba"
        },
        {
          "content_sha256": "9b9d007c53eaf64ac3c0c1482d01c5f1b1072f268a357962dd9e49c4c3ccd366",
          "logical_id": "mc-21dcf2ed0dcf3bae97e82554",
          "row_sha256": "ad9aa3b6fca5a4329ea678565838816cd87eddab2475c9fd23039d39a05ef0d6"
        },
        {
          "content_sha256": "c23fd248b361666ec47656264016449474a38e33d7820443a6c786e58a6685fb",
          "logical_id": "mc-df219766ae26f6cfc1f86c56",
          "row_sha256": "b0be8ba3dea5fb2c38f5758503e8ae4eee6dc6a2a4e910f96c22da6d5a2c865a"
        },
        {
          "content_sha256": "382b8083b50c920d62febbc8146b5c0cfcadba9791e30fdd93545d57570ddf41",
          "logical_id": "mc-3398b0849ce57fba895402f1",
          "row_sha256": "624c62eabc41ce52c39fd5cf9694407c9058c0d5fef7214056e8fbe74a8d84a6"
        }
      ],
      "sha256": "bff104cb5f62f586a7306c72debdfc7683c75828a00780c906c1d7a4995e75c7",
      "sheet_name": "cards",
      "table_sha256": "e6263f51633a36c1d99ae37fdc7899d045d53b22e853c02dc6b4f4696259519e",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 7987,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/rust-learning/cards/rust-lesson-02-data-shapes-oral.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "03838c3818079f243842814c7b6e521ff56602402cb7c8413ff347e0a2cb5afe",
          "logical_id": "mc-4c222a4a73430d0a23d4b090",
          "row_sha256": "a4f4e3b535740fb5d56012f8f1b19af8818f701faf128018f4c5ef46073e4c5a"
        },
        {
          "content_sha256": "8f9a9ed5c167883b260917aea618a3983ce85e09ab2cfe02befe2150ac2bfb4d",
          "logical_id": "mc-d4bf55f60282677744e473c0",
          "row_sha256": "9ff9315c979b1c7bd52d7398fae93ba0436dfbe87246496cd3379bd7645740b2"
        },
        {
          "content_sha256": "c82ee2a6a1ed9caa87a6e0fa581776dbe27072bd9ed0e6412534e311748b300a",
          "logical_id": "mc-3a870011f6ef84f7e0efac6f",
          "row_sha256": "8c795d1bde8cf7280a8ba39690561c1ce7cf25f39ca5da9d0fe63d2e03d88c4a"
        }
      ],
      "sha256": "3d96ce2783e3bfba6e7fde11667720114226b3c1d59ba06f170b157679502ea6",
      "sheet_name": "cards",
      "table_sha256": "2e5a7e4574c70f9b916ef6d5be9dfbc429656c28fc4c3f7b0f01709bbd0f1d92",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "10e0b4bcc5b06b774b375cbe7307abf16919211edcb5defb331507675d832b3a",
  "sources": [
    {
      "collection": "rust-study-logs",
      "id": "data-shapes-log",
      "path": "docs/rust-learning/logs/2026-10-14-data-shapes.md",
      "sha256": "1b817b981de07199e814fe3620e69be01c207e003a9acb2831f3ea5177f512e2",
      "summary": "10/8–10/14：数值规则、切片、struct 与 enum 的布局、match、Box、引用与 Copy 的纠错与答疑"
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

导入文件：[rust-lesson-02-data-shapes-correction.xlsx](rust-lesson-02-data-shapes-correction.xlsx)（10 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[rust-lesson-02-data-shapes-technical-qa.xlsx](rust-lesson-02-data-shapes-technical-qa.xlsx)（29 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[rust-lesson-02-data-shapes-oral.xlsx](rust-lesson-02-data-shapes-oral.xlsx)（3 张卡）
