---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "7b836ca1dba099717e3e6a5ecf2782bb18552d043324d6b130f25a0d3cec53f5",
  "candidate_sha256": "b810cbb621545bc48e7a0a330c33b00abf8cee6cabdca9dfc4fbd4fc378a1f10",
  "cards": [
    {
      "content_sha256": "823cb749d91f816d98744e0590a8182cb72d7c85aa2bfea175b84575dada21ca",
      "content_summary": "inverted dropout 通过逆 keep-probability 缩放保持输出期望",
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
      "content_sha256": "6d19c78a9c0c3a844c3363e57da0db98d91c0da3d652e6b395c38f374a8aab95",
      "content_summary": "纠正把 p=0.5 时的保留值 2x 写成输出期望",
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
      "content_sha256": "011b6ab4f7163c7594b894d55cef98da3dcd703c9d60a7d17fba39864535e0b4",
      "content_summary": "区分访存边界 mask 与随机 keep mask",
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
      "content_sha256": "1c73d33b5bd8df599030695798624a187f111afd6e2e22b58d664f7b9ebfe2a8",
      "content_summary": "global offset 防止不同 program 重复 local-offset 随机模式",
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
      "content_sha256": "808069c951114c9d52587c1c10641e526d68522ef908d36bdf2d8567290e6434",
      "content_summary": "分清随机数、keep/drop决策和最终输出的复现条件，明确 p 决定阈值",
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
      "content_sha256": "60024a0a0220cab885c79f1a3a766bbb52837aee7df42734edd65d6175430ffc",
      "content_summary": "相同 mask 可把不同输入的差异同时清零，阻止从输入不同推出输出必不同",
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
      "content_sha256": "4533ad7e13f84972267159cf1ef1e2b3668e31f7d8e554a21867efe99d0d5b07",
      "content_summary": "seeded dropout 以现场随机计算换取 mask 状态和流量减少",
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
      "content_sha256": "d4e12695282f75eb8ef26c2e0ae712f194b88a60e0e687f3bc1e721b6b23db00",
      "content_summary": "通过真实 off-by-one 错误强化尾部有效与无效 lane 的数量守恒",
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
      "content_sha256": "1563cb8ce153f4afe612d15185d033d09d9c9c4cf805c1777d0601c0c783937b",
      "content_summary": "将原尾部复合目标明确组织为区间、数量与访存保护的机制链",
      "dependency_content_sha256": {
        "mc-11065b73e0b9651d13129eb5": "011b6ab4f7163c7594b894d55cef98da3dcd703c9d60a7d17fba39864535e0b4",
        "mc-e72b538ae95230c44696bca8": "d4e12695282f75eb8ef26c2e0ae712f194b88a60e0e687f3bc1e721b6b23db00"
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
        "summary": "已依据两类 mask 的职责与真实 lane 计数纠错复核区间、数量守恒和访存保护链，确认 n=2057 的 9/1015 推导及 tl.rand/load/store 边界一致。"
      },
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "56e29352346caa59b9ce2d92b10a48464e36303308d4999f3c53bb102506069d",
      "content_summary": "综合口述 seeded dropout 的期望、随机身份、复现、内存取舍和尾部边界",
      "dependency_content_sha256": {
        "mc-1452241f4974fe80e44e9626": "1c73d33b5bd8df599030695798624a187f111afd6e2e22b58d664f7b9ebfe2a8",
        "mc-46554d25559bf0e0f688b0e8": "1563cb8ce153f4afe612d15185d033d09d9c9c4cf805c1777d0601c0c783937b",
        "mc-711b7d4e6e47ad5dabe798e3": "823cb749d91f816d98744e0590a8182cb72d7c85aa2bfea175b84575dada21ca",
        "mc-7208dde569c097b5430c14b0": "4533ad7e13f84972267159cf1ef1e2b3668e31f7d8e554a21867efe99d0d5b07",
        "mc-aa126e51b7b710faebd12184": "808069c951114c9d52587c1c10641e526d68522ef908d36bdf2d8567290e6434"
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
        "summary": "已复核期望、global offset、包含 p 的决策复现条件、内存取舍及尾部机制五张子卡；口述覆盖相同边界且未新增未经子卡核验的结论。"
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
  "manifest_payload_sha256": "513bb3090274242ad9e300ec00a0d607ef30f2d9e96f80fc9d43064d79ca7580",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5009,
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
          "content_sha256": "6d19c78a9c0c3a844c3363e57da0db98d91c0da3d652e6b395c38f374a8aab95",
          "logical_id": "mc-a221d1ca9b2a0baea78a067c",
          "row_sha256": "7df9f8cecc218bdd9fa6c10a10007165fe101fba9c2f043860fd827d28908565"
        },
        {
          "content_sha256": "60024a0a0220cab885c79f1a3a766bbb52837aee7df42734edd65d6175430ffc",
          "logical_id": "mc-3e5086b8fec794eec0a47fc9",
          "row_sha256": "715f7d30ba3f22b4b3046f4bfd186c9ff968cbd89a68c9e8bf9d0e38483d51f0"
        },
        {
          "content_sha256": "d4e12695282f75eb8ef26c2e0ae712f194b88a60e0e687f3bc1e721b6b23db00",
          "logical_id": "mc-e72b538ae95230c44696bca8",
          "row_sha256": "4c66cc28be69cbd16ff4c17f3cf60cb7ae9c0244d112be54bd5323b55c8fd7ab"
        }
      ],
      "sha256": "42423d2cf9550ef339ba5eaef8e1c28a4bcba088c5ae2bac1af0ea80af96e9d6",
      "sheet_name": "cards",
      "table_sha256": "7f49b6680a4195a0e037c3b52e5150c4a6362faa80f66bb7a8b04d547434053a",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 7689,
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
          "content_sha256": "823cb749d91f816d98744e0590a8182cb72d7c85aa2bfea175b84575dada21ca",
          "logical_id": "mc-711b7d4e6e47ad5dabe798e3",
          "row_sha256": "d6c6fee396194a9f46f35aa487faf551d81a86ff55b59731db4855a7e9b3c034"
        },
        {
          "content_sha256": "011b6ab4f7163c7594b894d55cef98da3dcd703c9d60a7d17fba39864535e0b4",
          "logical_id": "mc-11065b73e0b9651d13129eb5",
          "row_sha256": "72bacb9fd7166b18fcc2584bb21a1d515258c18d4ad986ae919261b132e07293"
        },
        {
          "content_sha256": "1c73d33b5bd8df599030695798624a187f111afd6e2e22b58d664f7b9ebfe2a8",
          "logical_id": "mc-1452241f4974fe80e44e9626",
          "row_sha256": "eac0b1a57412ab2599e7c3e614a05b063d54bce17bd169fd907b1c413127ba47"
        },
        {
          "content_sha256": "808069c951114c9d52587c1c10641e526d68522ef908d36bdf2d8567290e6434",
          "logical_id": "mc-aa126e51b7b710faebd12184",
          "row_sha256": "831d1aa6a198a322aa255e4d9cbf9ea55e762fe3e950c12300b3c19d11a36f06"
        },
        {
          "content_sha256": "4533ad7e13f84972267159cf1ef1e2b3668e31f7d8e554a21867efe99d0d5b07",
          "logical_id": "mc-7208dde569c097b5430c14b0",
          "row_sha256": "8231495d767042d15ce1e0c35a91156d0b46538a77a6939e6227df6e9b0d90fc"
        },
        {
          "content_sha256": "1563cb8ce153f4afe612d15185d033d09d9c9c4cf805c1777d0601c0c783937b",
          "logical_id": "mc-46554d25559bf0e0f688b0e8",
          "row_sha256": "d2d2e27db376fc5449dd3bee52042dbfb61c4e30d9e40fb78d440577e73aef7c"
        }
      ],
      "sha256": "0738295e327ccae0d7b6a2be343bbef4b178642c0321e5a21687190d181dd48b",
      "sheet_name": "cards",
      "table_sha256": "9c4a26bb72089e195e4720fc82c3f13fd5255e39c33e8de07200a5c29b806be5",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 3905,
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
          "content_sha256": "56e29352346caa59b9ce2d92b10a48464e36303308d4999f3c53bb102506069d",
          "logical_id": "mc-058b865b1ac9de96b3131943",
          "row_sha256": "200ba90080707989ec75327d86138967c1b30b55a34079855e6ac1573fc1a5df"
        }
      ],
      "sha256": "8175809a6f8b6541132aa4a7b0a23ae711f7d2dc6d11629a56556cdaa38617a8",
      "sheet_name": "cards",
      "table_sha256": "2d7a3f1730263bc6e14594ea293519766dcc2d38e35a5b0f7c6ebfa19f898b7e",
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
