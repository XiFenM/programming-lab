---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "3a9a728580c6cbadca12d319e595c07790d65114856270fee1484d21e53b41c5",
  "candidate_sha256": "b98651d8a871cfdcbbbd3da2a27a20e77ac935c0540f3a3da624765902c6389f",
  "cards": [
    {
      "content_sha256": "f11720d7c6a4cb4a3a8dbcf187345b59f831ad9aba8c17c25e40052b1d3e35b3",
      "content_summary": "从 A[M,K]、B[K,N] 与固定 C 输出块出发，解释 accumulator 形状、沿 K 加载乘加和尾部处理。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "blocked-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "追踪单个输出 tile 的分块加载、k 轴推进和累加数据流"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-93d5cb5f189271bd463f66f5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "0849b2d7b0f02df702bbe300b9a94e3971ddd3d2f46480f41c5c53f0ad31b3a4",
      "content_summary": "在固定 offs_k、指针基址逐轮推进的写法下，用全局 K=t×BLOCK_K+offs_k 区分局部与全局坐标。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "区分分块 matmul 中固定局部 offs_k 与指针推进后的全局 k 坐标"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-a1636912f944d54665961084",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6812ad091a536c7f12dc5b47a61cc12f682a8b7ec7befd517814a82c73a262eb",
      "content_summary": "用 C 的 K 轴点积解释错误输入如何污染有效输出，以及 load mask 与 store mask 的不同作用。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释为什么 k 尾部必须在 load 时补零而不能依赖 c store mask"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-2a2e5e507246b774ac4eee7d",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log",
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6000dc6defcdefc6c8435dcbc664527fc763b94de820f3dcf48049132c759f49",
      "content_summary": "解释 M/N 是独立输出坐标、K 是归约坐标，因此合法替代输入只可服务于最终丢弃的输出。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "blocked-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 m/n 边界读取合法 dummy 数据不会污染有效输出的原因及与 mask 的关系"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-0d4bc6a1836e0d2c6de8bdb5",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "480415802208a80a5c8687a82e4e9c57e932d3d30b6079794f4392561c84c752",
      "content_summary": "通过覆盖全部输出行的目标，纠正 cdiv 之前先整除丢失余数的写法。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "写出 tile 数量的正确 cdiv 调用并避免预先整除"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-b748990eeb64b83da16794a3",
      "misconception_of": null,
      "priority": 3,
      "quality": "B",
      "source_ids": [
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "a4015de03bfe216f7f2ab9af57e3fb39853807852dcd17481dee74252ddaf5db",
      "content_summary": "明确 output-tile 网格与坐标顺序，解释组内先 M 后 N 的 PID 映射及同列 B 的复用关系。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-matmul",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "判定 grouped ordering 中组内线性 pid 到 m/n tile 坐标的变化顺序"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-40db2e4425a22efcb30a44e2",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "7dbaf61ab8a79efdd68803898d0fdf4859fc3b21e39e3c7600d1e77c886a886a",
      "content_summary": "用 5×3 输出 tile 网格说明尾组实际组高如何同时避免非法行号和合法输出遗漏。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 grouped pid 映射为何必须使用尾组实际大小"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-4635ed52ca08d9e8d3d86a8b",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log",
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "fdc2553eb5d07cb9df6f4ee4d7ff29917f30be305019bcfd62cc883e54788ff6",
      "content_summary": "在尾组组高计算的明确场景中，区分双输入逐元素 minimum 与单输入轴归约 min。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "triton-api",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "区分 triton 的 reduction tl.min 与 elementwise tl.minimum"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-ccc79bbbc7f5c0a5be131add",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "94809c331a8a195066f65d54525084e312e70ee80a907bb192260d4b0d116f1d",
      "content_summary": "说明矩阵乘法 tile 配置同时影响边界浪费、寄存器和并发，计数只能筛候选而不能裁决性能。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "matmul-performance",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释仅凭 shape、program 数量和 k-loop 次数不能裁决 tile 配置性能的原因"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-62ebe8a0b30dea5145854637",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "97c1356cfc538045b0fba63acf4d8934a8cac5054cab3ca475415799e793989e",
      "content_summary": "在配置差异与运行漂移无法分离的 benchmark 中，区分证据不足与真实效应很小。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-performance-evidence",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "在配置差异与运行漂移无法分离时给出正确的证据结论"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-4dc66aa7b63f1fe191d09add",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "ccbd31de8a154c42d588051370234678f0420ac69854502f291e0db8f22f27df",
      "content_summary": "串联输出 tile 的 A/B 复用、重排后的访问间隔与 L2 驻留条件，并限定性能结论。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-matmul-performance",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "解释 grouped ordering 何时可能通过 l2 locality 显著获益"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-2fd335ab94ec21c8a7c24c73",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "c978aa09990b6b2ca39977c2459f453a5f139ea405af2b65cc5c6f1d8413dda5",
      "content_summary": "用完整 benchmark 场景口述 grouped ordering 的 L2 机制、成立条件与证据不足的报告方式。",
      "dependency_content_sha256": {
        "mc-2fd335ab94ec21c8a7c24c73": "ccbd31de8a154c42d588051370234678f0420ac69854502f291e0db8f22f27df",
        "mc-4dc66aa7b63f1fe191d09add": "97c1356cfc538045b0fba63acf4d8934a8cac5054cab3ca475415799e793989e"
      },
      "depends_on": [
        "mc-2fd335ab94ec21c8a7c24c73",
        "mc-4dc66aa7b63f1fe191d09add"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-matmul-performance",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "综合说明 grouped ordering 的加速机制并解释一次证据不足的测量"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-89f34aea9a94a29d20e579d9",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "review_resolution": {
        "summary": "已重新对照本课 card-11, card-10 的增强题答复核本卡：场景与符号定义一致，机制关系和适用边界仍成立，参考回答及评分锚点由这些子卡支持；本轮只增强表达，没有扩大原知识目标。"
      },
      "source_ids": [
        "lesson-03-concept-log",
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "fd049ff02482f1b78edabf71511f2c3453e7d167fd144fed31e8b13d32a3a202",
  "manifest_payload_sha256": "9081985eb2312dd331403313cbec0490eb76d479a81204d69f2eac05dd7db434",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5119,
      "columns": [
        "意图",
        "场景",
        "正确",
        "错误",
        "说明"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-03-matrix-multiplication-correction.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "480415802208a80a5c8687a82e4e9c57e932d3d30b6079794f4392561c84c752",
          "logical_id": "mc-b748990eeb64b83da16794a3",
          "row_sha256": "6e69d94152aec57c7df4b295c1c62f457462e8871bc965ebcc2f07e92f308f8f"
        },
        {
          "content_sha256": "fdc2553eb5d07cb9df6f4ee4d7ff29917f30be305019bcfd62cc883e54788ff6",
          "logical_id": "mc-ccc79bbbc7f5c0a5be131add",
          "row_sha256": "f45955bca00dc4fb24a9d85fd6271d3aa37b4f416bb32fe409b9269c47c96393"
        }
      ],
      "sha256": "b6fee9a1d500b89a110ce8a08b9d0e6a0282b13c89ac5c40f63783286e8c32df",
      "sheet_name": "cards",
      "table_sha256": "2066302e5fd2a881bdd33a6f1c0a29070316793753c079c877d1086bad1d625c",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 15354,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-03-matrix-multiplication-technical-qa.xlsx",
      "row_count": 9,
      "rows": [
        {
          "content_sha256": "f11720d7c6a4cb4a3a8dbcf187345b59f831ad9aba8c17c25e40052b1d3e35b3",
          "logical_id": "mc-93d5cb5f189271bd463f66f5",
          "row_sha256": "44e1e8f56d3c83e62e48b8ebd1b2728c4f9561794266cbb3a74eadadb97a9320"
        },
        {
          "content_sha256": "0849b2d7b0f02df702bbe300b9a94e3971ddd3d2f46480f41c5c53f0ad31b3a4",
          "logical_id": "mc-a1636912f944d54665961084",
          "row_sha256": "a4518ee09ca680aac3cbdf27d06a96d27944f175db6603171c807de27311fcc9"
        },
        {
          "content_sha256": "6812ad091a536c7f12dc5b47a61cc12f682a8b7ec7befd517814a82c73a262eb",
          "logical_id": "mc-2a2e5e507246b774ac4eee7d",
          "row_sha256": "1b5121b065cfe55b8cd5999b167c5b2b34477bd41736234a92cc4fedfa697c96"
        },
        {
          "content_sha256": "6000dc6defcdefc6c8435dcbc664527fc763b94de820f3dcf48049132c759f49",
          "logical_id": "mc-0d4bc6a1836e0d2c6de8bdb5",
          "row_sha256": "0605acb1db9549b2caa3916557348c10d426524cee73c53a030f9a899559c876"
        },
        {
          "content_sha256": "a4015de03bfe216f7f2ab9af57e3fb39853807852dcd17481dee74252ddaf5db",
          "logical_id": "mc-40db2e4425a22efcb30a44e2",
          "row_sha256": "055a7ed2a1dde1fce85c5570466b9efa5c0da659fc9364938e21e22958750fed"
        },
        {
          "content_sha256": "7dbaf61ab8a79efdd68803898d0fdf4859fc3b21e39e3c7600d1e77c886a886a",
          "logical_id": "mc-4635ed52ca08d9e8d3d86a8b",
          "row_sha256": "21c2acef98910dcaf045e281d3f79b78de04ce9ccca4843a159b407852b00a10"
        },
        {
          "content_sha256": "94809c331a8a195066f65d54525084e312e70ee80a907bb192260d4b0d116f1d",
          "logical_id": "mc-62ebe8a0b30dea5145854637",
          "row_sha256": "18777b5309730c95183c6b7b17a76b055bd5eb45292a0aa4de011d130d5f9c8c"
        },
        {
          "content_sha256": "97c1356cfc538045b0fba63acf4d8934a8cac5054cab3ca475415799e793989e",
          "logical_id": "mc-4dc66aa7b63f1fe191d09add",
          "row_sha256": "bf64699c49d53f930df4687ae970826b5b53eb0a3fc9e9cfdb23bb567099fbe5"
        },
        {
          "content_sha256": "ccbd31de8a154c42d588051370234678f0420ac69854502f291e0db8f22f27df",
          "logical_id": "mc-2fd335ab94ec21c8a7c24c73",
          "row_sha256": "c17cb30033f85442814501c3496e2df51025c6cf972cdf52f87b1db25b4ddf8d"
        }
      ],
      "sha256": "e732f6df87fecadc1d67dc5e7f8fbac8e1ffc2ee3e0bb43e0efde81ae70d5641",
      "sheet_name": "cards",
      "table_sha256": "5510ae5ab7e44ff16be55b844e206979b908212295d52b5539c91ad5b3a7fb27",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 4243,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-03-matrix-multiplication-oral.xlsx",
      "row_count": 1,
      "rows": [
        {
          "content_sha256": "c978aa09990b6b2ca39977c2459f453a5f139ea405af2b65cc5c6f1d8413dda5",
          "logical_id": "mc-89f34aea9a94a29d20e579d9",
          "row_sha256": "4a552b8d87895bfe38a1abcc5bb030de721acad056e204bd157b42ec986d3920"
        }
      ],
      "sha256": "faeddc5517cad7b3afdb6f1987d368b9dc67ac4d209d913f99e82a27402009e8",
      "sheet_name": "cards",
      "table_sha256": "adb6018ed93bff52a3bacdff280631665acfdaf9de06e141f4cb96089b17e06c",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "62a9f3d524161b8b07fa450e954e734455163b1c41f691f68197e2460c95754e",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson-03-concept-log",
      "path": "docs/triton-learning/logs/2026-08-17-matrix-multiplication.md",
      "sha256": "5d12fb944eeee2c6e3da3db3fa54efa131b8f98c7eef243e3ee8d6b695c3f1b6",
      "summary": "Lesson 03 已核验概念节点、真实纠错与映射示例；不消费遗留项"
    },
    {
      "collection": "triton-study-logs",
      "id": "lesson-03-study-log",
      "path": "docs/triton-learning/logs/2026-08-19-matrix-multiplication.md",
      "sha256": "110cf8458df06de765f7b50a50dd4b6c2820e815d6a7ce715336b936d44c4731",
      "summary": "Lesson 03 实践、纠错、性能证据解释与结课记录"
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

导入文件：[triton-lesson-03-matrix-multiplication-correction.xlsx](triton-lesson-03-matrix-multiplication-correction.xlsx)（2 张卡）

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-03-matrix-multiplication-technical-qa.xlsx](triton-lesson-03-matrix-multiplication-technical-qa.xlsx)（9 张卡）

## 综合口述卡

模板 `oral@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-03-matrix-multiplication-oral.xlsx](triton-lesson-03-matrix-multiplication-oral.xlsx)（1 张卡）
