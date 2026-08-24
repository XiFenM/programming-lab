---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "c056319a4fac26080be23af9acc2084e751be250ba3823df22c43b4acdd84cb2",
  "candidate_sha256": "15ac6f9fc15f0f95fe12a6bebb8e0dc881f5b35ce47a32078e672b413209adc4",
  "cards": [
    {
      "content_sha256": "2ab7f8cf8c2a858aedd99d35758aaeb385044696f470e4df2ff74f9e241348ad",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "a57ef376fde6e76921eb15908bb8b67ccaee0f11c5a5491ab2426de8a96147f4",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "1bde638a4f8d7a6ddab9c2017e96ee044f327504be89cf87cf33652c472adfd5",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "34228a2bcdd14d6bce4983a0994dd0a27725a7c06009bcdc15e2f43b29174659",
      "content_summary": "seeded dropout 精确复现依赖 offset 映射和完整数值条件",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "dd0197be13b30bda8c0639e8690ca4c115d2b3260e6e6972e28f880d7bc5ab98",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "8c578a6b680b88e994487bebd03db5360ffa43eb0d2249930ba8e63ce4f9526e",
      "content_summary": "尾部 lane 的半开区间、访存 mask 与数量守恒",
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
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "10b28a3e0c1ee55ef4265c3f075eded7205e31963d1f1a08e3cedc6dc528441f",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "0a3d4c3904e43edf9cab84383dbda2143dbe7d1630479854f6119d8c1bd3cdd4",
      "content_summary": "综合口述 seeded dropout 的期望、随机身份、复现、内存取舍和尾部边界",
      "dependency_content_sha256": {
        "mc-1452241f4974fe80e44e9626": "1bde638a4f8d7a6ddab9c2017e96ee044f327504be89cf87cf33652c472adfd5",
        "mc-46554d25559bf0e0f688b0e8": "8c578a6b680b88e994487bebd03db5360ffa43eb0d2249930ba8e63ce4f9526e",
        "mc-711b7d4e6e47ad5dabe798e3": "2ab7f8cf8c2a858aedd99d35758aaeb385044696f470e4df2ff74f9e241348ad",
        "mc-7208dde569c097b5430c14b0": "dd0197be13b30bda8c0639e8690ca4c115d2b3260e6e6972e28f880d7bc5ab98",
        "mc-aa126e51b7b710faebd12184": "34228a2bcdd14d6bce4983a0994dd0a27725a7c06009bcdc15e2f43b29174659"
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
      "source_ids": [
        "lesson-04-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.0.0"
    }
  ],
  "managed_body_sha256": "ef4ee9d5bab6485dff52ef6479f896f00c8af1ec3ff9b32c182aacc270d0f44d",
  "manifest_payload_sha256": "abf1946ad72be829e1cb2947407d128599af9b640781d2d6010226c2e33f3b36",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 3215,
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
          "content_sha256": "10b28a3e0c1ee55ef4265c3f075eded7205e31963d1f1a08e3cedc6dc528441f",
          "logical_id": "mc-a221d1ca9b2a0baea78a067c",
          "row_sha256": "10766b4022f822a7f526e7ee6b82ea06e0803de34dc8029f01eeed896c640116"
        }
      ],
      "sha256": "55cf11ec668284935f2bfeaca3239a6c1c9bbb6318d6a4bbf0a279005ec80425",
      "sheet_name": "cards",
      "table_sha256": "62b6dca69930201004f4a57b88f0e8d1baa5dcec7f35c16748f5b86cd32d83c4",
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "byte_size": 7675,
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
          "content_sha256": "2ab7f8cf8c2a858aedd99d35758aaeb385044696f470e4df2ff74f9e241348ad",
          "logical_id": "mc-711b7d4e6e47ad5dabe798e3",
          "row_sha256": "3d0926f2cc4c18909e7cf004c43e1227a0f3fad383a2da8c018b6b967b0ecbdd"
        },
        {
          "content_sha256": "a57ef376fde6e76921eb15908bb8b67ccaee0f11c5a5491ab2426de8a96147f4",
          "logical_id": "mc-11065b73e0b9651d13129eb5",
          "row_sha256": "661c96979b9ec8f358c4299d0e370ef4c984847b2b33239c8720ad8afdc3b4e9"
        },
        {
          "content_sha256": "1bde638a4f8d7a6ddab9c2017e96ee044f327504be89cf87cf33652c472adfd5",
          "logical_id": "mc-1452241f4974fe80e44e9626",
          "row_sha256": "5bd1f48bbde08f61204fac977eacb78f8d2e98c8c0faf7a56e29d5b8ad6ad1dc"
        },
        {
          "content_sha256": "34228a2bcdd14d6bce4983a0994dd0a27725a7c06009bcdc15e2f43b29174659",
          "logical_id": "mc-aa126e51b7b710faebd12184",
          "row_sha256": "ebfc722964d07b7fb271ab7524d1297cafb406e33cc581b48e43dcf4c642199a"
        },
        {
          "content_sha256": "dd0197be13b30bda8c0639e8690ca4c115d2b3260e6e6972e28f880d7bc5ab98",
          "logical_id": "mc-7208dde569c097b5430c14b0",
          "row_sha256": "a2d07ed9a28ca629ea0a0d6e84b0178dfed7de9a1901f08aaf569f08ffb73184"
        },
        {
          "content_sha256": "8c578a6b680b88e994487bebd03db5360ffa43eb0d2249930ba8e63ce4f9526e",
          "logical_id": "mc-46554d25559bf0e0f688b0e8",
          "row_sha256": "050a609b50b285d3e2ccf3c79cfe758ef01ce48cda0bcef1e2361fda625126bd"
        }
      ],
      "sha256": "549e883cdbdc16502491bd079db0abd39a1c3285fbb9b59e0a3d8e0d17cbfbc4",
      "sheet_name": "cards",
      "table_sha256": "4899f944f0cb3507198af6cad156bda22a319f404fbfb401ce42f90c5c2230c8",
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "byte_size": 3952,
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
          "content_sha256": "0a3d4c3904e43edf9cab84383dbda2143dbe7d1630479854f6119d8c1bd3cdd4",
          "logical_id": "mc-058b865b1ac9de96b3131943",
          "row_sha256": "3bef31947129527bc545b436ebb637e590f8a016da925febc1d004945390f641"
        }
      ],
      "sha256": "1310eeddad9ca8a1d8d0843f0893c9ea979c303576e54be5e10f640c413676f0",
      "sheet_name": "cards",
      "table_sha256": "e9498f8725829220ee68caed4ce9a853a64b37ebd292d7785aebd467c6ee2ec1",
      "template_id": "oral",
      "template_version": "1.0.0"
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
  "template_registry_sha256": "d6cdcd90c996ca6922a06f02a44b06800468a557bec6ad5c433511d7b57761d7",
  "template_registry_version": "1.0.0"
}
---
# Markji 表格导入卡片

> Markdown 保留受管元数据与模板定义；卡片数据请使用下列按模板拆分的 XLSX 文件导入。

## 真实错误纠错卡

模板 `correction@1.0.0`：

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

模板 `technical-qa@1.0.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-04-low-memory-dropout-technical-qa.xlsx](triton-lesson-04-low-memory-dropout-technical-qa.xlsx)（6 张卡）

## 综合口述卡

模板 `oral@1.0.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-04-low-memory-dropout-oral.xlsx](triton-lesson-04-low-memory-dropout-oral.xlsx)（1 张卡）
