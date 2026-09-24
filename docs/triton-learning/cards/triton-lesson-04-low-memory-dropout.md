---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "a152b606327fbcc4ca5292adce21296a75c4c97e9683a695c840a96bc7654f3a",
  "candidate_sha256": "641ec683e8bb7d7ecc8fbd5fe814e7cfa8a8970b91549760b4b46111b5a0ae5e",
  "cards": [
    {
      "content_sha256": "9618072fc2777338ef58736914b0489e45efa434eb90d921fcf7ef7d8ea92c2d",
      "content_summary": "在训练期 inverted dropout 的保留/丢弃模型下，推导逆保留概率缩放为何保持单元素期望。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "dropout-math",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 inverted dropout 缩放如何保持单元素输出期望"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-711b7d4e6e47ad5dabe798e3",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "415b9ecaf0b31cfbb84661de710a4555d268b8825eeb9cdacd8275f38459f869",
      "content_summary": "在两个 seed、p=0.5 的比较场景中，纠正把保留值 2x 当成无条件输出期望。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "dropout-math",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正把 dropout 保留分支的实现值误当作输出期望"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a221d1ca9b2a0baea78a067c",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4b40ccfec01de0e2cd7cfde421539bdcff89df2086938a7e4b9461afd9049e9d",
      "content_summary": "把分块 dropout 的地址合法性与随机数学决策分开，说明两种 mask 不能互相替代。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分 dropout kernel 中 boundary mask 与 keep mask 的职责"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-11065b73e0b9651d13129eb5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5d411705955e44ba67158547886ff2402b267fc3350d4107e2af1646438f2e6d",
      "content_summary": "从 seed/offset 随机映射出发，解释多 program 重用局部索引为何重复模式，以及全局坐标的作用。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "解释 seeded dropout 为什么必须用 global offsets 生成随机数"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1452241f4974fe80e44e9626",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "4c4fc599d4e22bd25f4f0d79d6ea92f5fe93812d9b7913a76a54d3b8db824a26",
      "content_summary": "以重计算前向输出为目标，分清随机数、mask 决策与数值输出各自要求的不变量。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "说明相同 seed 精确复现 dropout 决策所需的不变量及元素重排边界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-aa126e51b7b710faebd12184",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "385a537fed6657f5a3bb0f3010754be76cd274adbb342a9c093d9e4c9fce838b",
      "content_summary": "用明确 mask 编码与双输入反例，说明 dropout 可抹掉输入差异，不能据输入不同断言输出不同。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "dropout-math",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正相同 dropout mask 下不同输入必然产生不同输出的判断"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-3e5086b8fec794eec0a47fc9",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a0017e88b7b2a0cc6a6b3a2c48c8ee0308bf34e347c5ae31730cb87775528e9c",
      "content_summary": "区分 seeded dropout 节省的随机状态和 mask 流量，与仍存在及新增的计算开销。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 seeded dropout 的随机状态内存收益及不能直接推出更快的原因"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7208dde569c097b5430c14b0",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "668423465a9b1bb2cb88d61e8e4cccfebfbda5c309b63fc9b520924c35d89379",
      "content_summary": "在 n=1025、固定块长 1024 的尾块中，用半开区间与总数守恒纠正无效位置多算一个。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正把尾部无效 lane 数多算一个而破坏数量守恒的错误"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-e72b538ae95230c44696bca8",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a050dbe8d38971fa683aeef88b1203f7044b63d947260f2a4f9ae252a4bee3c6",
      "content_summary": "从具体尾块半开区间到位置计数，再区分随机纯计算与必须 mask 的内存操作。",
      "dependency_content_sha256": {
        "mc-11065b73e0b9651d13129eb5": "4b40ccfec01de0e2cd7cfde421539bdcff89df2086938a7e4b9461afd9049e9d",
        "mc-e72b538ae95230c44696bca8": "668423465a9b1bb2cb88d61e8e4cccfebfbda5c309b63fc9b520924c35d89379"
      },
      "depends_on": [
        "mc-11065b73e0b9651d13129eb5",
        "mc-e72b538ae95230c44696bca8"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "判断 seeded dropout 尾部 program 的半开区间、mask 操作与 lane 守恒"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-46554d25559bf0e0f688b0e8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已重新对照本课 card-03, card-08 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "63d9983ae969af70149c363cdaf100a8133b29a84ac4e29e448398017c88e21e",
      "content_summary": "用完整向量任务串联 inverted scaling、全局随机身份、精确复现条件、状态取舍与尾部访存。",
      "dependency_content_sha256": {
        "mc-1452241f4974fe80e44e9626": "5d411705955e44ba67158547886ff2402b267fc3350d4107e2af1646438f2e6d",
        "mc-46554d25559bf0e0f688b0e8": "a050dbe8d38971fa683aeef88b1203f7044b63d947260f2a4f9ae252a4bee3c6",
        "mc-711b7d4e6e47ad5dabe798e3": "9618072fc2777338ef58736914b0489e45efa434eb90d921fcf7ef7d8ea92c2d",
        "mc-7208dde569c097b5430c14b0": "a0017e88b7b2a0cc6a6b3a2c48c8ee0308bf34e347c5ae31730cb87775528e9c",
        "mc-aa126e51b7b710faebd12184": "4c4fc599d4e22bd25f4f0d79d6ea92f5fe93812d9b7913a76a54d3b8db824a26"
      },
      "depends_on": [
        "mc-1452241f4974fe80e44e9626",
        "mc-46554d25559bf0e0f688b0e8",
        "mc-711b7d4e6e47ad5dabe798e3",
        "mc-7208dde569c097b5430c14b0",
        "mc-aa126e51b7b710faebd12184"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "综合口述 seeded low-memory dropout 的数学语义、随机映射、复现和边界"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-058b865b1ac9de96b3131943",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已重新对照本课 card-04, card-09, card-01, card-07, card-05 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "d5fadfbb973d0ffd7854862d868077a3460beae66d13a9dfce8525855450fb90",
  "manifest_payload_sha256": "2a857e12fdc2715d4849da72efeb534712d39e9c3b678f96e1d7ecaac5c6ac16",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 6817,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-04-low-memory-dropout-correction.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "415b9ecaf0b31cfbb84661de710a4555d268b8825eeb9cdacd8275f38459f869",
          "logical_id": "mc-a221d1ca9b2a0baea78a067c",
          "row_sha256": "1e531202e5e27eb7590676ae601fcd1199ef2d00c159a80243237e302e0d05bb"
        },
        {
          "content_sha256": "385a537fed6657f5a3bb0f3010754be76cd274adbb342a9c093d9e4c9fce838b",
          "logical_id": "mc-3e5086b8fec794eec0a47fc9",
          "row_sha256": "699be1b277378033a1747d9688d45313c2dd7f932235d36d8bd8a792d5faa374"
        },
        {
          "content_sha256": "668423465a9b1bb2cb88d61e8e4cccfebfbda5c309b63fc9b520924c35d89379",
          "logical_id": "mc-e72b538ae95230c44696bca8",
          "row_sha256": "ecec4cde42c5dcaaa306769b7ffb645586bc940490703fca97dda09003a44383"
        }
      ],
      "sha256": "e944841e648aa2a51d37813e116d6781cb2a0101e45c66d10136b9967ab39e6e",
      "sheet_name": "cards",
      "table_sha256": "8949a2527697e1b4b6c758e84ed0d82d85ebe7905904b14b8e116e92e18d7889",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 11147,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-04-low-memory-dropout-technical-qa.xlsx",
      "row_count": 6,
      "rows": [
        {
          "content_sha256": "9618072fc2777338ef58736914b0489e45efa434eb90d921fcf7ef7d8ea92c2d",
          "logical_id": "mc-711b7d4e6e47ad5dabe798e3",
          "row_sha256": "9eab1ae39e4e4057b39b67e627eca5cf4aa5813489b731a38692aa39f53d1e43"
        },
        {
          "content_sha256": "4b40ccfec01de0e2cd7cfde421539bdcff89df2086938a7e4b9461afd9049e9d",
          "logical_id": "mc-11065b73e0b9651d13129eb5",
          "row_sha256": "10fbbf494f1c6d23f93acf4a3d3cd02abd301a5c0469296bbc894bba18c62613"
        },
        {
          "content_sha256": "5d411705955e44ba67158547886ff2402b267fc3350d4107e2af1646438f2e6d",
          "logical_id": "mc-1452241f4974fe80e44e9626",
          "row_sha256": "23433b28c4550f820fd255a384706f7fd07e6b247192f59cef2dc48dd7e8189a"
        },
        {
          "content_sha256": "4c4fc599d4e22bd25f4f0d79d6ea92f5fe93812d9b7913a76a54d3b8db824a26",
          "logical_id": "mc-aa126e51b7b710faebd12184",
          "row_sha256": "23b3c015347dcd931e4f443ec7ac041cea1579ebf9b693cc58176b42e6343c29"
        },
        {
          "content_sha256": "a0017e88b7b2a0cc6a6b3a2c48c8ee0308bf34e347c5ae31730cb87775528e9c",
          "logical_id": "mc-7208dde569c097b5430c14b0",
          "row_sha256": "49bd75c4891c9c84341599416c6ecf4cce7e9b80a0ef16be20d9e172073f38bf"
        },
        {
          "content_sha256": "a050dbe8d38971fa683aeef88b1203f7044b63d947260f2a4f9ae252a4bee3c6",
          "logical_id": "mc-46554d25559bf0e0f688b0e8",
          "row_sha256": "1841279514ff10ffdc59235bf20c58cfea5b021e17a01a83b84b01835d1f98b4"
        }
      ],
      "sha256": "774ba6ff8085cb9bbb1739b510e5164108e54da50df4c11e5a68b29c79740277",
      "sheet_name": "cards",
      "table_sha256": "d0d23c5b4724688ea27e89533c4b85bb66d6df155311583064524c30d15c5458",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4635,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-04-low-memory-dropout-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "63d9983ae969af70149c363cdaf100a8133b29a84ac4e29e448398017c88e21e",
          "logical_id": "mc-058b865b1ac9de96b3131943",
          "row_sha256": "04a68e64d62f02b06ab3a02a5627b0c9f594e5f8e07807d162cd8aaa291f1799"
        }
      ],
      "sha256": "c1dfbbb56346e38b12ce2918611eb16f057fbf51335dfaee4fb061c4dc22fc33",
      "sheet_name": "cards",
      "table_sha256": "0c526b4bc901a4dadca768fefe5b9fdc515f72cea1d018ac378ab5a999f0d4e6",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "b301d3a596e09a1017cff996f272f873c502269c1a4f6ccec440af91545d4be9",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson-04-study-log",
      "path": "docs/triton-learning/logs/2026-08-24-low-memory-dropout.md",
      "sha256": "a3cf8bfa43e7b369202addb10cd285e49fe69df5e311c5a672cddbc0046c7154",
      "summary": "Lesson 04 经核验的 Low-Memory Dropout 结构化学习过程记录"
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

导入文件：[triton-lesson-04-low-memory-dropout-correction.xlsx](triton-lesson-04-low-memory-dropout-correction.xlsx)（3 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-04-low-memory-dropout-technical-qa.xlsx](triton-lesson-04-low-memory-dropout-technical-qa.xlsx)（6 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-04-low-memory-dropout-oral.xlsx](triton-lesson-04-low-memory-dropout-oral.xlsx)（1 张卡）
