---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "fb39e754f14db19c656f3fffde9fbbf39c8c4be0243ca30a5b49a628d95eb8da",
  "candidate_sha256": "f0526ae60c033ad489d1d62481939095eab1f62ebbe81471f28d995d58030c33",
  "cards": [
    {
      "content_sha256": "58e5481e8160460d1a16a6f31858f1873844db9f1789d43a153a974ec65fcdfd",
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
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "cb722a1da7207e9e8a69cd796536268025ec69ce6d0a0c9d77c1a67c6b2a9838",
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
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "79b35e11f1bc89a436efa07860242a984e81b1c276744266e780af13efa14cdc",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "1c06fa1dfeec495abef1a6cb02288a5950cf5f5b8d670c472e3d4d3a16ee21e3",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "788fb80857cd78f3b7b4df7b68f1425ea4458104d8cf3a9d70ea74936e0a05f8",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "9edcc53457d1835b7da896a2ac8835b1f4adccc159ae6364913bbd1c58c05225",
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
      "template_version": "1.0.0"
    },
    {
      "content_sha256": "1391c094d7b46f0bed1f25c4621cf1c6165929f7da8027e8a5a13c79f4cf7c3d",
      "content_summary": "综合口述 grouped ordering 的机制、适用条件与证据边界",
      "dependency_content_sha256": {
        "mc-2fd335ab94ec21c8a7c24c73": "9edcc53457d1835b7da896a2ac8835b1f4adccc159ae6364913bbd1c58c05225",
        "mc-4dc66aa7b63f1fe191d09add": "788fb80857cd78f3b7b4df7b68f1425ea4458104d8cf3a9d70ea74936e0a05f8"
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
      "source_ids": [
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.0.0"
    }
  ],
  "managed_body_sha256": "71b654da2a072d4861c239199a55947cd2728fd1bd3d05783fd4a55c2422797f",
  "manifest_payload_sha256": "13cc381b76dad30fbfb7c6593be170f1f85d9b1ae42509be876a7d7fb2eb711f",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 3923,
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
          "content_sha256": "79b35e11f1bc89a436efa07860242a984e81b1c276744266e780af13efa14cdc",
          "logical_id": "mc-b748990eeb64b83da16794a3",
          "row_sha256": "868ae1adee645cf4b13817142c304a49becb65bb7460953513e3f797722acc76"
        },
        {
          "content_sha256": "1c06fa1dfeec495abef1a6cb02288a5950cf5f5b8d670c472e3d4d3a16ee21e3",
          "logical_id": "mc-ccc79bbbc7f5c0a5be131add",
          "row_sha256": "d0a5d31193f04ed85b1fa2c6e31e42a8b6a0b6cda9df26984934f0b5520746f0"
        }
      ],
      "sha256": "9dfb175c1e9f7545f413dc34d9dcae752520a6acf7891a1eb94d40a36af3e0af",
      "sheet_name": "cards",
      "table_sha256": "16eb560a1c51b513f58aea247378253f82e15d4f1df1fbe4dc6b9a27f83ff3d3",
      "template_id": "correction",
      "template_version": "1.0.0"
    },
    {
      "byte_size": 5846,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-03-matrix-multiplication-technical-qa.xlsx",
      "row_count": 4,
      "rows": [
        {
          "content_sha256": "58e5481e8160460d1a16a6f31858f1873844db9f1789d43a153a974ec65fcdfd",
          "logical_id": "mc-2a2e5e507246b774ac4eee7d",
          "row_sha256": "c9ae267864027ed70a10a7b3bddd48c3df537911070d2789af69c39984fdd065"
        },
        {
          "content_sha256": "cb722a1da7207e9e8a69cd796536268025ec69ce6d0a0c9d77c1a67c6b2a9838",
          "logical_id": "mc-4635ed52ca08d9e8d3d86a8b",
          "row_sha256": "e9b2f3e080aaac5bcc449395733622ac678e154f5a87395763bf8e499bf77ad4"
        },
        {
          "content_sha256": "788fb80857cd78f3b7b4df7b68f1425ea4458104d8cf3a9d70ea74936e0a05f8",
          "logical_id": "mc-4dc66aa7b63f1fe191d09add",
          "row_sha256": "020bcafd04722fc9fa54497d32141a8984d8c2ac246bec3f94bc40fcf3a6346a"
        },
        {
          "content_sha256": "9edcc53457d1835b7da896a2ac8835b1f4adccc159ae6364913bbd1c58c05225",
          "logical_id": "mc-2fd335ab94ec21c8a7c24c73",
          "row_sha256": "c5ba958be9d8a9e2a6f304dd2eac9ed38b85fcc655abc73582b707d9f3d26c5e"
        }
      ],
      "sha256": "776dfcad372528cfc76438bdbf2d7f2c25b769a2fcd66be8dadd88d18e71e8b3",
      "sheet_name": "cards",
      "table_sha256": "2fa70ab971ba5851fd97d0a538fbe187b136095b640828895707deec6ef6d40c",
      "template_id": "technical-qa",
      "template_version": "1.0.0"
    },
    {
      "byte_size": 3704,
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
          "content_sha256": "1391c094d7b46f0bed1f25c4621cf1c6165929f7da8027e8a5a13c79f4cf7c3d",
          "logical_id": "mc-89f34aea9a94a29d20e579d9",
          "row_sha256": "9731f664155dc159d861b3e7960486b9f9961d074de01fa36f602b0aab7de05a"
        }
      ],
      "sha256": "35285464b35b4b2ebb3e9e2f9384e2ca7eb3ec47befc6b94488d00581e945ab2",
      "sheet_name": "cards",
      "table_sha256": "18449acc6acfabedc55f4e71ef5bd2b998d1245b58780b6869194e06960d57f8",
      "template_id": "oral",
      "template_version": "1.0.0"
    }
  ],
  "source_fingerprint": "6987ed70032b40ef38c91fe1cdfbd9bfc7637b6af77774a6d4a7185262c1b534",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "lesson-03-study-log",
      "path": "docs/triton-learning/logs/2026-08-19-matrix-multiplication.md",
      "sha256": "110cf8458df06de765f7b50a50dd4b6c2820e815d6a7ce715336b936d44c4731",
      "summary": "Lesson 03 实践、纠错、性能证据解释与结课记录"
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

导入文件：[triton-lesson-03-matrix-multiplication-correction.xlsx](triton-lesson-03-matrix-multiplication-correction.xlsx)（2 张卡）

## 技术问答卡

模板 `technical-qa@1.0.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-03-matrix-multiplication-technical-qa.xlsx](triton-lesson-03-matrix-multiplication-technical-qa.xlsx)（4 张卡）

## 综合口述卡

模板 `oral@1.0.0`：

```text
[P#H1#{{问题}}]
---
{{参考回答}}
💡 [T#B,!36b59d#{{评分锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-lesson-03-matrix-multiplication-oral.xlsx](triton-lesson-03-matrix-multiplication-oral.xlsx)（1 张卡）
