---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "ec95fc8e7a6928ff7a18463bf3f83109e49a96576d97849c12c84b2b975ebef1",
  "candidate_sha256": "ae7322425cdf066a657f7d50882e61400db2b7d17fe8a20f6784a8735bd76cfa",
  "cards": [
    {
      "content_sha256": "6d8461e702484ca3b2916d419867bce768b753aacf790ae7a96dfc3b5847f819",
      "content_summary": "算法面试中按数据、语义、访问和资源澄清约束，并具体说明约束对候选算法的影响",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "按稳定维度澄清会改变候选算法的信息,并把约束映射到方案变化"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-4f0190168427ee5f36908a24",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "acd47c772d0afd986c8bafc3f88662bda2ec571513249171650a817d41e07343",
      "content_summary": "向面试官完整解释 Two Sum 不同下标双层枚举：无遗漏与无重复、最坏比较次数、补数查询瓶颈及提前返回边界",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "可验证地解释 two sum 中 i 小于 j 双层枚举基线的正确性、复杂度来源与优化瓶颈"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-df1ae68b936de0326cba0825",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "71acf176a697602b3f3da3b221d24823c6a6db5b630122ea27bbbed68edb797e",
      "content_summary": "在只读、常数空间的 Two Sum 中，准确区分已排除候选、尚未找到优化与全局下界证明",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分若干候选被排除与已经证明不存在更优算法"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-9a2ca0475b56586028b01f47",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "2c619a9e3aaa51e350c027f84d9f8d0f43389e7dfbb07daccb0ab8a02775448b",
      "content_summary": "重复 ID 判定从数组迁移到无回放、无完整历史的单遍流时，先检查逐对枚举的访问依赖",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "判断数组上的双层枚举基线能否迁移到单遍数据流"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-fb9f50860ce8cb63ab2680a0",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7e7b93040fa160d89fdf8dfb164a9b41b9ced6f6aa443058ec41c40312fef379",
      "content_summary": "非递减单遍 ID 流相邻判重的完整性、逐项更新机制、成本与顺序前提；不擅自补完遗留实现边界",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "从单遍访问和非递减顺序推导精确判重方案及适用边界"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-7ecf051e0b5c2a7f2d685e80",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c74b7c75548f20902a748e90d9c007622b7433b180ef4a3b0cf90d2eb85f8642",
      "content_summary": "在元素固定为 0、1、2 的 Two Sum 中，区分可达和值、合法 target 与有解保证，并保留互异下标边界",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "判断元素值域在什么前提下能够限制 two sum 的 target"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-1a48039f55d300c7fd6f3de8",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "25f272be20304a799082285188c2212f83b33c7a25860a0748e59d1d800a6672",
      "content_summary": "固定三值域、只读和常数空间约束下，用至多六个下标完整解决返回一对互异原下标的 Two Sum",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "在值域固定为 0、1、2、只读输入和常数额外空间下构造返回不同原下标的 two sum"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-d6bf5b8ac24ed65ff2044c4c",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "994be38d91b001993e202962002e68a7e44eb0f014bd8949e7bf829e2f3db49d",
      "content_summary": "以单题实际展示的分析和表达为证据，明确未观察的实现、调试与系统设计，不越界推断岗位胜任",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "按已观察和未观察证据界定算法面试评价"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-49862043dfc59100d0b75900",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "04df27daf1293017153658326b985fc042f6ddd248209ff7b0cbb75833f4d8b9",
      "content_summary": "以 Two Sum 为明确场景，45–90 秒完整口述约束澄清、枚举基线、补数查询瓶颈、候选筛选与结论边界",
      "dependency_content_sha256": {
        "mc-4f0190168427ee5f36908a24": "6d8461e702484ca3b2916d419867bce768b753aacf790ae7a96dfc3b5847f819",
        "mc-9a2ca0475b56586028b01f47": "71acf176a697602b3f3da3b221d24823c6a6db5b630122ea27bbbed68edb797e",
        "mc-df1ae68b936de0326cba0825": "acd47c772d0afd986c8bafc3f88662bda2ec571513249171650a817d41e07343"
      },
      "depends_on": [
        "mc-4f0190168427ee5f36908a24",
        "mc-9a2ca0475b56586028b01f47",
        "mc-df1ae68b936de0326cba0825"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "algorithm-interview",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "在 45–90 秒内说明如何从约束澄清推进到可验证基线、候选筛选与保守结论"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-9fa38a858c2f964aaeb624e8",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "review_resolution": {
        "summary": "已重新对照本课 card-01, card-03, card-02 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson-01-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "ff3b694e290d6842073febe1d4872d57387087f2295269472bdcf0fb314c85b0",
  "manifest_payload_sha256": "fd770eb2fc107004e5b983fca7c7034615059052729fc3dda711700cb9ef7cfb",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 8702,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/algorithm-interview-learning/cards/algorithm-interview-lesson-01-constraint-driven-selection-correction.xlsx",
      "row_count": 3,
      "rows": [
        {
          "content_sha256": "acd47c772d0afd986c8bafc3f88662bda2ec571513249171650a817d41e07343",
          "logical_id": "mc-df1ae68b936de0326cba0825",
          "row_sha256": "487762c39e4db7d95507e82ec7f75a0a738b943dea6763f1154245bb86de2150"
        },
        {
          "content_sha256": "71acf176a697602b3f3da3b221d24823c6a6db5b630122ea27bbbed68edb797e",
          "logical_id": "mc-9a2ca0475b56586028b01f47",
          "row_sha256": "73bc259e6dee3b7e6d28e7f32a3147085f86826f088950dc7192df18e6c03d1c"
        },
        {
          "content_sha256": "c74b7c75548f20902a748e90d9c007622b7433b180ef4a3b0cf90d2eb85f8642",
          "logical_id": "mc-1a48039f55d300c7fd6f3de8",
          "row_sha256": "fb037b1196dd866a980fd9008d85d7cb33729338f26629d7d5bfbc3c1e6d275a"
        }
      ],
      "sha256": "a1347776d4e91434b38906eeaede1bc15af2c85b8bfcc9f991223c5397692ffa",
      "sheet_name": "cards",
      "table_sha256": "de5db6f40b672ab06db12260ccf2814da77fd8f1c8983df5909551093b4823b2",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 11535,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/algorithm-interview-learning/cards/algorithm-interview-lesson-01-constraint-driven-selection-technical-qa.xlsx",
      "row_count": 5,
      "rows": [
        {
          "content_sha256": "6d8461e702484ca3b2916d419867bce768b753aacf790ae7a96dfc3b5847f819",
          "logical_id": "mc-4f0190168427ee5f36908a24",
          "row_sha256": "b082751bd86699ad8a7ce33890fc87be0b8c5f5cb5c460ecbc1eacd53a2f884a"
        },
        {
          "content_sha256": "2c619a9e3aaa51e350c027f84d9f8d0f43389e7dfbb07daccb0ab8a02775448b",
          "logical_id": "mc-fb9f50860ce8cb63ab2680a0",
          "row_sha256": "1d1b3106c0cba112e9d924600fee540ccd10f7da34eb5e25b7e6a31abc3dcc50"
        },
        {
          "content_sha256": "7e7b93040fa160d89fdf8dfb164a9b41b9ced6f6aa443058ec41c40312fef379",
          "logical_id": "mc-7ecf051e0b5c2a7f2d685e80",
          "row_sha256": "7a36e81c13407b9a56f32401e5d79aa245245978c32d1eed8bc6c510b535eb90"
        },
        {
          "content_sha256": "25f272be20304a799082285188c2212f83b33c7a25860a0748e59d1d800a6672",
          "logical_id": "mc-d6bf5b8ac24ed65ff2044c4c",
          "row_sha256": "75cdbb3218e3149fcb33686de9802a4b821eb73a7e9913d6683dc0801308df87"
        },
        {
          "content_sha256": "994be38d91b001993e202962002e68a7e44eb0f014bd8949e7bf829e2f3db49d",
          "logical_id": "mc-49862043dfc59100d0b75900",
          "row_sha256": "9013927a7ea72c62790272db5196ae62e8e9832c023bd51d621a654b9e90593f"
        }
      ],
      "sha256": "8c5fdc4ea9d82b53e4b200ed9b5ecadbf0624c38644ee3b4eeedf0228bd0adff",
      "sheet_name": "cards",
      "table_sha256": "81d68dea74f7f5a3db3f6cd905b04c6a33a666c109f2da640a7ff6633e42857d",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4720,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/algorithm-interview-learning/cards/algorithm-interview-lesson-01-constraint-driven-selection-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "04df27daf1293017153658326b985fc042f6ddd248209ff7b0cbb75833f4d8b9",
          "logical_id": "mc-9fa38a858c2f964aaeb624e8",
          "row_sha256": "7b45d8c68fe80400693a1d9053318736683e42d1b737252e35be5b7be1839d5f"
        }
      ],
      "sha256": "55cbe19bd137a23c4c909aee9e1aa781e21b1c0c168b10a517d058d4a7ef0aed",
      "sheet_name": "cards",
      "table_sha256": "a5994a1f4b149de2f86f0fcf84ba72f319c68ddc7ada74562cc55b9ea3578f96",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "1bd3a222b9fed41ec55cca9c7186eab4241b0889243f23de59da9b24dd4469f6",
  "sources": [
    {
      "collection": "algorithm-interview-study-logs",
      "id": "lesson-01-study-log",
      "path": "docs/algorithm-interview-learning/logs/2026-08-15-lesson-01-constraint-driven-selection.md",
      "sha256": "0515443283f925c8bc7e50192c142038bc02ee2f3053debbd3d73070a758fc7d",
      "summary": "Lesson 01 约束驱动的算法选择与可观察表达结构化学习记录"
    }
  ],
  "target_collection": "algorithm-interview-cards",
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

导入文件：[algorithm-interview-lesson-01-constraint-driven-selection-correction.xlsx](algorithm-interview-lesson-01-constraint-driven-selection-correction.xlsx)（3 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[algorithm-interview-lesson-01-constraint-driven-selection-technical-qa.xlsx](algorithm-interview-lesson-01-constraint-driven-selection-technical-qa.xlsx)（5 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[algorithm-interview-lesson-01-constraint-driven-selection-oral.xlsx](algorithm-interview-lesson-01-constraint-driven-selection-oral.xlsx)（1 张卡）
