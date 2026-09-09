---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "4cc16b416b80ec01a83b43163d5fcbe76464e1bd90356f06fdcd5da7efb07845",
  "candidate_sha256": "46a68e6537a42fc9013a02a498864bd4195c6e719c939de2a3b438b0312b6f9d",
  "cards": [
    {
      "content_sha256": "9ee6f52b089106348627bf120738824a3948a2500ef00c7e2405a33ecdf4cc3c",
      "content_summary": "单个输出 tile 通过沿 K 分块乘加形成；A/B tile 形状与 accumulator 形状对应",
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
      "content_sha256": "a7c96475fd07ebe405e9043c15cc3ddf0d549850a22b432af2f3bebd6d6dba8e",
      "content_summary": "澄清局部 K 偏移不变而全局地址随指针推进",
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
      "content_sha256": "f51a45eb7d39bcd2be01fd5b70e021210f2fef61f6b6d07784de727397fe240e",
      "content_summary": "区分 K load mask 与 M/N store mask 的职责",
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
      "content_sha256": "2d5e397b19ea67ec881915eed4ef5860720247206673d24e862238c857090c5e",
      "content_summary": "M/N dummy 计算保持固定 tile，正确性来自输出坐标独立及最终写回裁剪",
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
      "content_sha256": "32f54b575207d6c896880e35d37a474d7c52b24a054a8686af8bd21e0979235a",
      "content_summary": "修正 cdiv 前误用整数除法的公式记号",
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
      "content_sha256": "4f6687bd83fa5bea516cf12a3e6b019ea17838422d050156717b76a271f9f1d2",
      "content_summary": "用已核验 PID 例子建立组内 M 优先映射及 B tile 复用直觉",
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
      "content_sha256": "41a47000eed10cf3884a3407a3af34563bdc93a9d4e519151c6daae492370bc7",
      "content_summary": "尾组实际大小保证 grouped grid 完整覆盖",
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
      "content_sha256": "1f5a7758c059f8632594480cf94f715b7b122dae8c826b125c88b6b9f6e10092",
      "content_summary": "真实编译错误揭示 reduction 与 elementwise minimum 的差异",
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
      "content_sha256": "88a09e8f3cf55f8891278145da3fd3b2145be82b615bf8c016d88e47c962eba2",
      "content_summary": "通过工作量、资源和目标设备测量纠正只按 shape 选配置",
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
      "content_sha256": "2773254a6d7354f664ff465b44d680ae8d7f95737d64b3b2097dc5d5b32711f6",
      "content_summary": "证据不足与 effect size 很小不是同一结论",
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
      "content_sha256": "40c11ef73efc3fc02309481f7114614e328c50ffdb1d40a8b89205fa4528f47e",
      "content_summary": "grouped ordering 的缓存复用机制与失效边界",
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
      "content_sha256": "8c1106b7e7f2c878e03dd5b10678d6e84aeeb5e9e3fac0e80429f63901688ef9",
      "content_summary": "综合口述 grouped ordering 的机制、适用条件与证据边界",
      "dependency_content_sha256": {
        "mc-2fd335ab94ec21c8a7c24c73": "40c11ef73efc3fc02309481f7114614e328c50ffdb1d40a8b89205fa4528f47e",
        "mc-4dc66aa7b63f1fe191d09add": "2773254a6d7354f664ff465b44d680ae8d7f95737d64b3b2097dc5d5b32711f6"
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
        "summary": "已依据更新后的 L2 复用机制与证据不足辨析卡复核口述；移除特定版本的 M-first 映射，保持常青的复用机会、条件与结论边界。"
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
  "manifest_payload_sha256": "216cda1dce69cd375bb16decfe4a4c0781ff2a287027d6c75e295272982d9f80",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 4094,
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
          "content_sha256": "32f54b575207d6c896880e35d37a474d7c52b24a054a8686af8bd21e0979235a",
          "logical_id": "mc-b748990eeb64b83da16794a3",
          "row_sha256": "adca55f4208cbc17897eabc4c985619dce0e6e67027d083e9b7f2a5476ff87d4"
        },
        {
          "content_sha256": "1f5a7758c059f8632594480cf94f715b7b122dae8c826b125c88b6b9f6e10092",
          "logical_id": "mc-ccc79bbbc7f5c0a5be131add",
          "row_sha256": "5a8793001bf7ce18319f050772152956b41d78bd510dcd8bc40f59aa0ea205e8"
        }
      ],
      "sha256": "dae6ac6571c4e37f41fd516bf810361c1c695f91d76b9d98abf68121d276d181",
      "sheet_name": "cards",
      "table_sha256": "d9ac1457eaeecd30488488303c41546f77cbeca8f4649b3a426127a19d31a4a7",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 10057,
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
          "content_sha256": "9ee6f52b089106348627bf120738824a3948a2500ef00c7e2405a33ecdf4cc3c",
          "logical_id": "mc-93d5cb5f189271bd463f66f5",
          "row_sha256": "434b1b791946374b3ba189bd455777928386b40af8d09df0aadf666fdce3f070"
        },
        {
          "content_sha256": "a7c96475fd07ebe405e9043c15cc3ddf0d549850a22b432af2f3bebd6d6dba8e",
          "logical_id": "mc-a1636912f944d54665961084",
          "row_sha256": "4dfb2066cc8aa0d87c99e4732fd150b1becde9a17b08c2b873f38c525fc2cb08"
        },
        {
          "content_sha256": "f51a45eb7d39bcd2be01fd5b70e021210f2fef61f6b6d07784de727397fe240e",
          "logical_id": "mc-2a2e5e507246b774ac4eee7d",
          "row_sha256": "53dd73c9257b656c46fd355a2b069d63011e51922ae3dce456c5b09983e6cd57"
        },
        {
          "content_sha256": "2d5e397b19ea67ec881915eed4ef5860720247206673d24e862238c857090c5e",
          "logical_id": "mc-0d4bc6a1836e0d2c6de8bdb5",
          "row_sha256": "6c4ffc5425d74340f378e37bd3f8e03b2088ea0b94becc0230f3aabde9029b73"
        },
        {
          "content_sha256": "4f6687bd83fa5bea516cf12a3e6b019ea17838422d050156717b76a271f9f1d2",
          "logical_id": "mc-40db2e4425a22efcb30a44e2",
          "row_sha256": "d455700274602d1521846b9a43df58e6f2142d21a98876717a2c0cd657f0f828"
        },
        {
          "content_sha256": "41a47000eed10cf3884a3407a3af34563bdc93a9d4e519151c6daae492370bc7",
          "logical_id": "mc-4635ed52ca08d9e8d3d86a8b",
          "row_sha256": "1a649dbde09eae2c6b4543375fadc57b689df3514e9cd50680b26b15f5207bc7"
        },
        {
          "content_sha256": "88a09e8f3cf55f8891278145da3fd3b2145be82b615bf8c016d88e47c962eba2",
          "logical_id": "mc-62ebe8a0b30dea5145854637",
          "row_sha256": "b472fb36a6bf29cbce23202fdf1890338003021e682f5f1e81c9f812d424b9e9"
        },
        {
          "content_sha256": "2773254a6d7354f664ff465b44d680ae8d7f95737d64b3b2097dc5d5b32711f6",
          "logical_id": "mc-4dc66aa7b63f1fe191d09add",
          "row_sha256": "e47ba3dd73454081bf6b398cdae6582165bea4b9294d2aa60654371fab0fb0fd"
        },
        {
          "content_sha256": "40c11ef73efc3fc02309481f7114614e328c50ffdb1d40a8b89205fa4528f47e",
          "logical_id": "mc-2fd335ab94ec21c8a7c24c73",
          "row_sha256": "08212db2ee4190b0280261e3848fa75f54a916395a47bc277d258dd97c2bec09"
        }
      ],
      "sha256": "17a5193fd56248ddb16628650205bde21a08b4104581615687a367ea4d674b74",
      "sheet_name": "cards",
      "table_sha256": "4acb6be4be92013a4856e6da981a939a7632c7989d491d4b9ad2cac7eeeb57e2",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 3686,
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
          "content_sha256": "8c1106b7e7f2c878e03dd5b10678d6e84aeeb5e9e3fac0e80429f63901688ef9",
          "logical_id": "mc-89f34aea9a94a29d20e579d9",
          "row_sha256": "4d60ef8c54e760e363abfb3a7176464bb05f9a4d231d50bd53c6da4f5e3f4d0b"
        }
      ],
      "sha256": "94f9e1b2d535dfffee67d5027894367d56c0978e9197bc5d6a10db6afaa310dd",
      "sheet_name": "cards",
      "table_sha256": "b175e0ec89b63f97a4a4262528b5fc4e28fbc068c6909f04b6dfdf952f905fd0",
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
