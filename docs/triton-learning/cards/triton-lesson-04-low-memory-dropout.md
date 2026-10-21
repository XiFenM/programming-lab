---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "bb2d730b2ff51222dd9f0153b9765b8b443920345955c70cf3ae1a05e6ad70b1",
  "candidate_sha256": "355c38f256e5c35c36efa08ca1fcdf13bac00c08d6197ff6595e874f32393d04",
  "cards": [
    {
      "content_sha256": "191767499e285ca9f114e441d93d7992fdcfc7e1cdbd1d1a22db6913c2d9d878",
      "content_summary": "在训练期 inverted dropout 的保留/丢弃模型下，推导逆保留概率缩放为何保持单元素期望，并区分保留值与期望。",
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
      "content_sha256": "cb77e228c5995f2cc0d9f741431e50ba46ed26e39bb2d6c501a0b894b05f05c3",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "997c1fe75df07521d645e206d09b14524e718a7adbc4d4b37b92ca388696bb43",
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
      "content_sha256": "05b461c7a239884ab6de18f1de94e407f0bd271ccd566ab17e553a817ef4625e",
      "content_summary": "以逐位复现前向输出为目标，按随机数、keep 决策与数值输出三层列出各自的不变量。",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
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
      "content_sha256": "4173277aef885f8815809dbb2f81a692098bea6ddf094b52f73be257ca14770c",
      "content_summary": "在 n=2057 的尾块中，按是否访问内存判断 tl.load、tl.rand、tl.store 哪些需要 boundary mask。",
      "dependency_content_sha256": {},
      "depends_on": [],
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
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-46554d25559bf0e0f688b0e8",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
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
      "content_sha256": "bf821251df0afb68189cce2a1da025a7677175a65a338ddc7361c037b5d3bc81",
      "content_summary": "以面试问答为场景，口述 seeded dropout 的数学规则、global offset 随机映射、重算条件与相对显式 mask 的取舍。",
      "dependency_content_sha256": {
        "mc-1452241f4974fe80e44e9626": "997c1fe75df07521d645e206d09b14524e718a7adbc4d4b37b92ca388696bb43",
        "mc-711b7d4e6e47ad5dabe798e3": "191767499e285ca9f114e441d93d7992fdcfc7e1cdbd1d1a22db6913c2d9d878",
        "mc-7208dde569c097b5430c14b0": "a0017e88b7b2a0cc6a6b3a2c48c8ee0308bf34e347c5ae31730cb87775528e9c",
        "mc-aa126e51b7b710faebd12184": "05b461c7a239884ab6de18f1de94e407f0bd271ccd566ab17e553a817ef4625e"
      },
      "depends_on": [
        "mc-1452241f4974fe80e44e9626",
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
        "summary": "已对照更新后的 card-01、card-04、card-05 与未变的 card-07 复核：子卡由 5 张减为 4 张（去掉尾部 card-09），参考回答与四个评分锚点只覆盖题面所问的保留与缩放规则、随机映射、重算条件与取舍。"
      },
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "be7c934e79150f5e617d42a8b66fa34d7f9032c11185550e33ee20e1a812eed0",
      "content_summary": "用 A.T.contiguous() 的逐元素 offset 追踪，纠正重排后同一 seed 仍复现逻辑元素决策的误判。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-dropout",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "纠正张量重排并连续化后同一 seed 仍让决策跟随逻辑元素的误判"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1563e66dc14aec7df1f30b4f",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "4858038da027c6be09b2f66e1b058a1321949be1b62513e2499a5901bb1ea147",
  "manifest_payload_sha256": "5f109c57ad2de26979963f349bc5c88f581a3aacba054e9ec416ebbea659db86",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 4396,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-04-low-memory-dropout-correction.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "be7c934e79150f5e617d42a8b66fa34d7f9032c11185550e33ee20e1a812eed0",
          "logical_id": "mc-1563e66dc14aec7df1f30b4f",
          "row_sha256": "4cd681b329b898cfb0a6794de5e3bbb420a4001b41b4aa070c114b45de6dae7a"
        }
      ],
      "sha256": "5fb7eab7d12cea44299381c3ec5261fbc68e4baae6ea28e3464c17b124535a7a",
      "sheet_name": "cards",
      "table_sha256": "68bbdfdfe85497f7c3add86ae157b2fef7c610d9174cc7f3b9dd06bff83ce237",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 11204,
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
          "content_sha256": "191767499e285ca9f114e441d93d7992fdcfc7e1cdbd1d1a22db6913c2d9d878",
          "logical_id": "mc-711b7d4e6e47ad5dabe798e3",
          "row_sha256": "faa5a7f9f7cca954c335324fcef2d9f1d24b7556cbb295301cde9cbed5609d2b"
        },
        {
          "content_sha256": "cb77e228c5995f2cc0d9f741431e50ba46ed26e39bb2d6c501a0b894b05f05c3",
          "logical_id": "mc-11065b73e0b9651d13129eb5",
          "row_sha256": "e0ed82afb29c20072740dce8934779ccd09316dea5447013d8056449c556854e"
        },
        {
          "content_sha256": "997c1fe75df07521d645e206d09b14524e718a7adbc4d4b37b92ca388696bb43",
          "logical_id": "mc-1452241f4974fe80e44e9626",
          "row_sha256": "3065becc0c8ebde403fa5281c6745241adbf7e28cb077f943b40730b1fd4db56"
        },
        {
          "content_sha256": "05b461c7a239884ab6de18f1de94e407f0bd271ccd566ab17e553a817ef4625e",
          "logical_id": "mc-aa126e51b7b710faebd12184",
          "row_sha256": "ac898a1d18a872e3032d0e9ede7f63921bc5fe81e7bed308d9fc08e772a39198"
        },
        {
          "content_sha256": "a0017e88b7b2a0cc6a6b3a2c48c8ee0308bf34e347c5ae31730cb87775528e9c",
          "logical_id": "mc-7208dde569c097b5430c14b0",
          "row_sha256": "49bd75c4891c9c84341599416c6ecf4cce7e9b80a0ef16be20d9e172073f38bf"
        },
        {
          "content_sha256": "4173277aef885f8815809dbb2f81a692098bea6ddf094b52f73be257ca14770c",
          "logical_id": "mc-46554d25559bf0e0f688b0e8",
          "row_sha256": "978108514b49a7c00ba91d7f97c3753e8cd6684ac622c6a89f3c59f128537cbf"
        }
      ],
      "sha256": "28c9cff5d5126f8fa323c5ef9196037f82df2c8f3dc272e25374dc0aab490424",
      "sheet_name": "cards",
      "table_sha256": "3c11ec68497ee5452a58700b5cf62a3e6664d9b5114eb310e2c68d891a30f910",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4562,
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
          "content_sha256": "bf821251df0afb68189cce2a1da025a7677175a65a338ddc7361c037b5d3bc81",
          "logical_id": "mc-058b865b1ac9de96b3131943",
          "row_sha256": "bf436823fe93c770163a3c9730b231b7ce480f0c652d1ec6adf862878403aa0c"
        }
      ],
      "sha256": "b6cb5740deb8baac5c5255c3b8803fbdf615dc12830b59c95678aae110b9daa0",
      "sheet_name": "cards",
      "table_sha256": "142ccea99344fc2cd03d066e98b9f34fd49f3d212b9bcddae78f11694a15dc7f",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "2d9e034b106967270558cf08c8b0f4eb6f232190ea5c7414211890c2b198d2ce",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson-04-study-log",
      "path": "docs/triton-learning/logs/2026-08-24-low-memory-dropout.md",
      "sha256": "333dfa19abf05e89eefc53f29c0aeebbcd1241d3ce9ad74f38afab1ec4c40df9",
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

导入文件：[triton-lesson-04-low-memory-dropout-correction.xlsx](triton-lesson-04-low-memory-dropout-correction.xlsx)（1 张卡）

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
