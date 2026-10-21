---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "119e0ff8a875329dd8596d5d7e247f0d16d88e0c7032ee88832d65aa3f4934bc",
  "candidate_sha256": "5c033b02d8fa84fdf0a92996fbe77f25d0a845e98b02c899a0c5ff6e779df4d8",
  "cards": [
    {
      "content_sha256": "aa8b05dc7c7bf4ab5321d6a41da52d8e57c16a1fcd5e7a525421f9df6b87d363",
      "content_summary": "从 A[M,K]、B[K,N] 与固定 C 输出块出发，解释 FP32 accumulator、沿 K 的加载乘加与指针推进，以及尾部处理的位置。",
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
      "content_sha256": "8fc05684ff1e8508e5f12a95ebe8cf3c39e4f42b9f33ead0dbed70487c97c4fc",
      "content_summary": "指针推进写法下，用全局 K=t×BLOCK_K+offs_k 说明 K 尾部 load mask 为何不能写成 offs_k<K。",
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
      "priority": 4,
      "quality": "B",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-03-concept-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "d62fb148ff0c21f9b8742a80a50622d0399cb0c6f915e3b2fe16fb8a622e2814",
      "content_summary": "在单个 GEMM 内的 grouped ordering 中，说明组内 PID 先沿 M 后沿 N 的映射规律及相邻 PID 的 B tile 复用。",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-03-concept-log"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "87d5e9cbc6faee011515126853b24086d645a6cca417a3e3f18d0e7a17962164",
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
      "content_sha256": "413e5d547833c6204d32bbc95a9593a5015139aa50cbcd0f626736426c0219db",
      "content_summary": "恢复 tl.min(num_pid_m - first_pid_m, GROUP_SIZE_M) 的真实错误，区分归约 tl.min 与两值取小的 tl.minimum／内建 min。",
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
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "dfbeb4b33af10f2a5c4c39208352120ac4eabc876dce1062dcbd92905a75f2b8",
      "content_summary": "说明 tile 配置同时影响复用收益、边界浪费与寄存器驻留，计数只能筛候选而不能裁决性能。",
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
      "content_sha256": "a657297b49b3f98d317c06ee7122486d6527d56cad31b8596a5801892e658950",
      "content_summary": "用 RTX 5090 上 ABBA 四个 median 的读数，纠正把无法与漂移区分的差异说成影响较小。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "discrimination",
        "domain": "gpu-performance-evidence",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "纠正把无法与运行漂移区分的配置差异说成对性能影响较小"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-21b6813aa2b0574e1285b5a8",
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
      "content_sha256": "2fd9e9762d839f934b75fc2ca5629e6db81cdd4bfcdd8f8489544ebfbc6bf2b0",
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
      "content_sha256": "8aa29c3883a0bd444ad6543d09784a808f72202ba911e69b76cdcc58cd8b6a91",
      "content_summary": "以面试追问为场景，口述 grouped ordering 的 L2 复用机制、生效条件，以及一次证据不足的测量怎样解读。",
      "dependency_content_sha256": {
        "mc-21b6813aa2b0574e1285b5a8": "a657297b49b3f98d317c06ee7122486d6527d56cad31b8596a5801892e658950",
        "mc-2fd335ab94ec21c8a7c24c73": "2fd9e9762d839f934b75fc2ca5629e6db81cdd4bfcdd8f8489544ebfbc6bf2b0"
      },
      "depends_on": [
        "mc-21b6813aa2b0574e1285b5a8",
        "mc-2fd335ab94ec21c8a7c24c73"
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
        "summary": "已对照更新后的 card-11 与新子卡 group-size-benchmark-correction 复核：参考回答只使用两张子卡中的复用机制、生效条件、约 4% 漂移与证据不足结论，四个评分锚点与题面三问一一对应。"
      },
      "source_ids": [
        "lesson-03-concept-log",
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "734ccca9200f22d753ca51b4f6a71be8888c5f10ca146fa4446818dc4e79c7ca",
      "content_summary": "用教程 9×9 block 例子，按 A tile 行与 B tile 列计数，说明 row-major 90 与分组 54 的差距来源。",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-matmul-performance",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "用 9×9 block 例子数出 row-major 与分组顺序的输入 block 加载量并说明差距来源"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-6a9002bc8f021366a579fe04",
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
      "content_sha256": "3c6217c3ed85676dcf781a890d258347ad9787acf4eee74b957f203fcfdeb75e",
      "content_summary": "以面试走读为场景，串联 grouped PID 映射与尾组、K 循环与 FP32 累加、K 尾部补零和 M/N 写回 mask。",
      "dependency_content_sha256": {
        "mc-0d4bc6a1836e0d2c6de8bdb5": "6000dc6defcdefc6c8435dcbc664527fc763b94de820f3dcf48049132c759f49",
        "mc-2a2e5e507246b774ac4eee7d": "6812ad091a536c7f12dc5b47a61cc12f682a8b7ec7befd517814a82c73a262eb",
        "mc-4635ed52ca08d9e8d3d86a8b": "87d5e9cbc6faee011515126853b24086d645a6cca417a3e3f18d0e7a17962164",
        "mc-93d5cb5f189271bd463f66f5": "aa8b05dc7c7bf4ab5321d6a41da52d8e57c16a1fcd5e7a525421f9df6b87d363"
      },
      "depends_on": [
        "mc-0d4bc6a1836e0d2c6de8bdb5",
        "mc-2a2e5e507246b774ac4eee7d",
        "mc-4635ed52ca08d9e8d3d86a8b",
        "mc-93d5cb5f189271bd463f66f5"
      ],
      "fact_status": "verified",
      "identity": {
        "assessment": "oral",
        "domain": "triton-matmul",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "综合走读 triton matmul kernel 从 pid 映射到写回的流程与 m/n/k 边界处理"
      },
      "layer": "oral",
      "lifecycle": "active",
      "logical_id": "mc-daf9aff716344732e34b491e",
      "misconception_of": null,
      "priority": 4,
      "quality": "A",
      "source_ids": [
        "lesson-03-concept-log",
        "lesson-03-study-log"
      ],
      "successor_to": null,
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "379e79fd1a0266567bec14a9c072197c0caf0449423464fd5a74a018e301d185",
  "manifest_payload_sha256": "921f475c33b98c7192aff3bdd7e8a7b49c89fe2b54ba602218aabb2fbf4b7b03",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 5829,
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
          "content_sha256": "413e5d547833c6204d32bbc95a9593a5015139aa50cbcd0f626736426c0219db",
          "logical_id": "mc-ccc79bbbc7f5c0a5be131add",
          "row_sha256": "3b7fd84453138c704d2926df79621c291a91018e3fecb7a3d6ef17990d8d696c"
        },
        {
          "content_sha256": "a657297b49b3f98d317c06ee7122486d6527d56cad31b8596a5801892e658950",
          "logical_id": "mc-21b6813aa2b0574e1285b5a8",
          "row_sha256": "eb9b4463870eb49bb955d0799c0b5cb403f0bbc955c3212d5f1183f08671af9d"
        }
      ],
      "sha256": "b4257aef4e833ca5d39f85e210aa8425b4b22ae4c4495566e62656e9b4d10a02",
      "sheet_name": "cards",
      "table_sha256": "9b4021f94dfca0c08089432d059be4467ff546d48a51ffa92fdad9305e80a251",
      "template_id": "correction",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 16144,
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
          "content_sha256": "aa8b05dc7c7bf4ab5321d6a41da52d8e57c16a1fcd5e7a525421f9df6b87d363",
          "logical_id": "mc-93d5cb5f189271bd463f66f5",
          "row_sha256": "82ebe018476cf856a42bfa2108d2c156005984293456df09c2e3b0690230c707"
        },
        {
          "content_sha256": "8fc05684ff1e8508e5f12a95ebe8cf3c39e4f42b9f33ead0dbed70487c97c4fc",
          "logical_id": "mc-a1636912f944d54665961084",
          "row_sha256": "9ada30fb984cefaf7b647c58370ef074ef8b76702f9b1818b78791c358e6d5dd"
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
          "content_sha256": "d62fb148ff0c21f9b8742a80a50622d0399cb0c6f915e3b2fe16fb8a622e2814",
          "logical_id": "mc-40db2e4425a22efcb30a44e2",
          "row_sha256": "6837f6d525c11dff31f71e766819bc095202e3138903b22db3af92a3029a8eb5"
        },
        {
          "content_sha256": "87d5e9cbc6faee011515126853b24086d645a6cca417a3e3f18d0e7a17962164",
          "logical_id": "mc-4635ed52ca08d9e8d3d86a8b",
          "row_sha256": "1c2dd8d8900ae65e75a3b5efb1af1658dca9f9ffc4a566d07ad84ddb5a827178"
        },
        {
          "content_sha256": "dfbeb4b33af10f2a5c4c39208352120ac4eabc876dce1062dcbd92905a75f2b8",
          "logical_id": "mc-62ebe8a0b30dea5145854637",
          "row_sha256": "ceb0859199c65756aac619c9600268a723fa017a95018157f4f68ad510b85b79"
        },
        {
          "content_sha256": "2fd9e9762d839f934b75fc2ca5629e6db81cdd4bfcdd8f8489544ebfbc6bf2b0",
          "logical_id": "mc-2fd335ab94ec21c8a7c24c73",
          "row_sha256": "1ab8b321c099ec2ec2dbf9636706a1df0690f9608602e7f6daddc483fe8cdd20"
        },
        {
          "content_sha256": "734ccca9200f22d753ca51b4f6a71be8888c5f10ca146fa4446818dc4e79c7ca",
          "logical_id": "mc-6a9002bc8f021366a579fe04",
          "row_sha256": "3e402709e37cffd800506869082178c441b049f6d1e6e28714f64b3b83eab134"
        }
      ],
      "sha256": "844963100c30f050062cfeaf31ae115888479e1b4374edc70973c0c8fe599ac0",
      "sheet_name": "cards",
      "table_sha256": "fcd0deb8ccd7e4eed3449e267f05658f72cfbd769422eefe8ef09b14ab3086d5",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "byte_size": 6390,
      "columns": [
        "问题",
        "参考回答",
        "评分锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-lesson-03-matrix-multiplication-oral.xlsx",
      "row_count": 2,
      "rows": [
        {
          "content_sha256": "8aa29c3883a0bd444ad6543d09784a808f72202ba911e69b76cdcc58cd8b6a91",
          "logical_id": "mc-89f34aea9a94a29d20e579d9",
          "row_sha256": "4225aee8fe9f4b2c0d0876b5599a033f7e18d187428fac087cd1d6fee5591fe8"
        },
        {
          "content_sha256": "3c6217c3ed85676dcf781a890d258347ad9787acf4eee74b957f203fcfdeb75e",
          "logical_id": "mc-daf9aff716344732e34b491e",
          "row_sha256": "58601bdd7b86b5ca28424292ab17f3502fa218f723061647426b9aa7f34849c7"
        }
      ],
      "sha256": "dca1611fcb14916e3b1a6d4a649dd49162f4cdf5cea57e2158d06fa0075916b9",
      "sheet_name": "cards",
      "table_sha256": "5b838ced07805550b1067d2950555f8acb009f2408ee0636027d711e81b10c2c",
      "template_id": "oral",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "3e9d3ea7b3ce318f9761240fa2621c265e92afc773f8464dd1c277eb88349182",
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
      "sha256": "2cc3e5f83e899a5c97c91e46c65ac69f42dd18ce4141c1399ec22d3de0d47d23",
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

导入文件：[triton-lesson-03-matrix-multiplication-oral.xlsx](triton-lesson-03-matrix-multiplication-oral.xlsx)（2 张卡）
