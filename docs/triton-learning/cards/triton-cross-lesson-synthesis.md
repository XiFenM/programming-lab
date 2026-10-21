---
{
  "adapter": {
    "client_version": "3.8.00",
    "id": "markji",
    "profile": "programming-lab-markji"
  },
  "artifact_set_sha256": "e48ea0516ea8884258c74dfb35b7b1467118f733cde2dcf66b74ed8252902e98",
  "candidate_sha256": "2cb0e3004b1673311bd92533e1a6d25afc62457593f86f463df7f80b372148b3",
  "cards": [
    {
      "content_sha256": "ebc4fe99cda4bc5162f3bfc326b9f54cf129cee36643c2ac5c2955fd00316eaa",
      "content_summary": "填充值变换后仍须是归约单位元：K 尾部补 0 安全，softmax 填 −inf，LayerNorm 中心化后要再置 0，Attention 补 0 的 K 仍进分母",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-cross-lesson",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "masked 位置的填充值怎样才安全:变换后仍须是归约的单位元"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-98185da980e450ac8f23e105",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "l01-vector-add",
        "l02-fused-softmax",
        "l03-matmul-0819",
        "l05-layer-norm",
        "l06-attention-0924"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "5f402078980f7453d3fa5af2e64e9573460039abd023b1acf1cefd3e441eee53",
      "content_summary": "三处 group 同名不同义：矩阵乘的 PID 分组为 L2 复用，LayerNorm 的 G 组共享部分和槽并加锁，grouped GEMM 一次发射一组独立矩阵乘",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-cross-lesson",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "区分矩阵乘的 group_size_m、layernorm 参数梯度分组与 grouped gemm"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-f7998ea9940c0f1ac9f9bc5d",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "l03-matmul-0817",
        "l03-matmul-0819",
        "l05-layer-norm",
        "l08-grouped-gemm"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "f52dd5c7b89317c5366cd279d7c9ae41835f852ecfaac5a7bb35137742864925",
      "content_summary": "固定 P 个 program 按 r=p+kP 静态步长领任务不漏不重；块数均分不等于工作量均分；耗时差异大时改用原子计数器动态领取",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-cross-lesson",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "固定数量的 program 循环领任务:静态步长规则为何不漏不重,何时改用动态领取"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-1c3f8e5202593d23502576de",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "l02-fused-softmax",
        "l08-grouped-gemm",
        "l09-persistent"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "401c17ca8157e8b898bf49f846f559b107538724f61838fa265772e1a08a6b86",
      "content_summary": "TMA 张量规则约束基址与行距 16 字节对齐，块规则约束最内维字节数；x[1:] 连续但不对齐；构造时查行距、编译期查 device 端块",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-cross-lesson",
        "fact_scope": {
          "kind": "snapshot",
          "product": "triton",
          "version": "3.7.1"
        },
        "recall_target": "tma 描述符的两条 16 字节规则:整个张量与块各约束什么,连续为何不等于对齐"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-c1b3d42daef506594c95d8e2",
      "misconception_of": null,
      "priority": 5,
      "quality": "A",
      "source_ids": [
        "l06-attention-0924",
        "l10-block-scaled"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "6e2a84e1932ddec08781c53550eab45988dc3da899750dfc6891e9f2271e18e5",
      "content_summary": "seeded dropout 只存 seed、重算随机数，FlashAttention 只存行统计量 M、反向重算 P；省存储读写、多付计算，不能断言更快",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "mechanism",
        "domain": "triton-cross-lesson",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "反向需要的中间量是存下来还是重算:seeded dropout 与 flashattention 的取舍"
      },
      "layer": "mechanism",
      "lifecycle": "active",
      "logical_id": "mc-3ccf7ff5f66cdc1a7a8d177f",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "l04-dropout",
        "l06-attention-0919"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    },
    {
      "content_sha256": "42d6b781036c2f15a6e648da72cb8d3d19a9fa82ee3d2a0d2c9aaa87d0c9dc9b",
      "content_summary": "K 尾部 mask 要比全局 K 坐标，tl.rand 要传全局 offset；局部偏移只在块内定位，用错会静默出错",
      "dependency_content_sha256": {},
      "depends_on": [],
      "fact_status": "verified",
      "identity": {
        "assessment": "recall",
        "domain": "triton-cross-lesson",
        "fact_scope": {
          "kind": "evergreen"
        },
        "recall_target": "块内局部偏移与全局坐标:k 尾部 mask 与 tl.rand 各该用哪一个"
      },
      "layer": "atomic",
      "lifecycle": "active",
      "logical_id": "mc-66c3917445a574700e7e189b",
      "misconception_of": null,
      "priority": 4,
      "quality": "B",
      "source_ids": [
        "l03-matmul-0817",
        "l04-dropout"
      ],
      "successor_to": null,
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "managed_body_sha256": "49e9f38728e3e92eba7ada627adebddeb8d4f681588a0d0d3da11bae17869d38",
  "manifest_payload_sha256": "d6f60b0b587c756154edccce20fa5ddef88ce0684941182d6b829c416867b28e",
  "schema": "memo-cards.artifact/v2",
  "sidecars": [
    {
      "byte_size": 12663,
      "columns": [
        "问题",
        "答案",
        "锚点",
        "来源"
      ],
      "kind": "markji-import-xlsx",
      "path": "docs/triton-learning/cards/triton-cross-lesson-synthesis-technical-qa.xlsx",
      "row_count": 6,
      "rows": [
        {
          "content_sha256": "ebc4fe99cda4bc5162f3bfc326b9f54cf129cee36643c2ac5c2955fd00316eaa",
          "logical_id": "mc-98185da980e450ac8f23e105",
          "row_sha256": "cd4109c709aa45db2badf63b03686b3fff14c1270e68f3e1dedb8d1d2c918dcb"
        },
        {
          "content_sha256": "5f402078980f7453d3fa5af2e64e9573460039abd023b1acf1cefd3e441eee53",
          "logical_id": "mc-f7998ea9940c0f1ac9f9bc5d",
          "row_sha256": "7ba97d77cbe5e8a6e1d4b6d48bfb881af081a6c33ac412c40fe8d7735b8fe1be"
        },
        {
          "content_sha256": "f52dd5c7b89317c5366cd279d7c9ae41835f852ecfaac5a7bb35137742864925",
          "logical_id": "mc-1c3f8e5202593d23502576de",
          "row_sha256": "b83ba73383ca80ec22484d64ddc11606c7c89223a766dcf1a9fcda8efd0a1c53"
        },
        {
          "content_sha256": "401c17ca8157e8b898bf49f846f559b107538724f61838fa265772e1a08a6b86",
          "logical_id": "mc-c1b3d42daef506594c95d8e2",
          "row_sha256": "42691ad76334464e36b5cbe29e50ccc19efd38ac747870a0c005371a7262547e"
        },
        {
          "content_sha256": "6e2a84e1932ddec08781c53550eab45988dc3da899750dfc6891e9f2271e18e5",
          "logical_id": "mc-3ccf7ff5f66cdc1a7a8d177f",
          "row_sha256": "82483180347a68add5661be45c669f1e32f11f3dc1da0f67f03a84ebdcb523d5"
        },
        {
          "content_sha256": "42d6b781036c2f15a6e648da72cb8d3d19a9fa82ee3d2a0d2c9aaa87d0c9dc9b",
          "logical_id": "mc-66c3917445a574700e7e189b",
          "row_sha256": "8c2f1a70ae5ec0d03892c49fcba219bc5882cc8e005f88d356acc1c34a1298f2"
        }
      ],
      "sha256": "2f11d3d7550d4c5de6c42de2c1aefdf41eb025413fac2175cf239cb7c411b447",
      "sheet_name": "cards",
      "table_sha256": "21b6bff04d6353e3facec57bf26bba60437f42e534e803e948ff1caa55107335",
      "template_id": "technical-qa",
      "template_version": "1.1.0"
    }
  ],
  "source_fingerprint": "aeef6f2eb2e847b01efcb77847c7ebd26bed22f7120507e2a57a172d54029684",
  "sources": [
    {
      "collection": "triton-study-logs",
      "id": "l01-vector-add",
      "path": "docs/triton-learning/logs/2026-07-27-vector-add.md",
      "sha256": "fd35cf8d15f471bd99f209791d53a5367de1b1c3a143849ff0eac886de9383aa",
      "summary": "向量加法：mask、归约与计时"
    },
    {
      "collection": "triton-study-logs",
      "id": "l02-fused-softmax",
      "path": "docs/triton-learning/logs/2026-08-07-fused-softmax.md",
      "sha256": "44335bf79ea2330369e998c0b83a173fd98473bb2c9a0554d7916a3fecaac432",
      "summary": "Fused Softmax：−inf padding、persistent 分配"
    },
    {
      "collection": "triton-study-logs",
      "id": "l03-matmul-0817",
      "path": "docs/triton-learning/logs/2026-08-17-matrix-multiplication.md",
      "sha256": "5d12fb944eeee2c6e3da3db3fa54efa131b8f98c7eef243e3ee8d6b695c3f1b6",
      "summary": "矩阵乘：局部 offs_k 与全局 K 坐标、分组 PID"
    },
    {
      "collection": "triton-study-logs",
      "id": "l03-matmul-0819",
      "path": "docs/triton-learning/logs/2026-08-19-matrix-multiplication.md",
      "sha256": "2cc3e5f83e899a5c97c91e46c65ac69f42dd18ce4141c1399ec22d3de0d47d23",
      "summary": "矩阵乘：K 尾部补零、grouped ordering 的 L2 复用"
    },
    {
      "collection": "triton-study-logs",
      "id": "l04-dropout",
      "path": "docs/triton-learning/logs/2026-08-24-low-memory-dropout.md",
      "sha256": "333dfa19abf05e89eefc53f29c0aeebbcd1241d3ce9ad74f38afab1ec4c40df9",
      "summary": "Low-Memory Dropout：global offsets、seed 取代 mask"
    },
    {
      "collection": "triton-study-logs",
      "id": "l05-layer-norm",
      "path": "docs/triton-learning/logs/2026-09-14-layer-norm.md",
      "sha256": "3dbda96ab8eae4588e1279f26b31a1a5819b7ae64eb169e1448ace1a7fd75e0f",
      "summary": "LayerNorm：中心化后的 padding、参数梯度分组"
    },
    {
      "collection": "triton-study-logs",
      "id": "l06-attention-0919",
      "path": "docs/triton-learning/logs/2026-09-19-fused-attention.md",
      "sha256": "1e51f24058b1b7b546dd9c901fab1f48e8adb1e21b6279d495940be36f864d56",
      "summary": "Fused Attention：只存行统计量、反向重算 P"
    },
    {
      "collection": "triton-study-logs",
      "id": "l06-attention-0924",
      "path": "docs/triton-learning/logs/2026-09-24-fused-attention.md",
      "sha256": "755e51eeb97bc72caf893978d40e46aff500b2e185096fdfba1dc5632ec2a17f",
      "summary": "Fused Attention：K/V 补零与 softmax 分母、TMA 对齐"
    },
    {
      "collection": "triton-study-logs",
      "id": "l08-grouped-gemm",
      "path": "docs/triton-learning/logs/2026-10-09-grouped-gemm.md",
      "sha256": "310ba83ca4f5759ac15c40421e414457bfa66a62773b4646bb385526bb47b770",
      "summary": "Grouped GEMM：块队列、步长领取、原子计数器"
    },
    {
      "collection": "triton-study-logs",
      "id": "l09-persistent",
      "path": "docs/triton-learning/logs/2026-10-14-persistent-matmul.md",
      "sha256": "39c7eb19c1bff2b0f45e7abe31df12c068ef1392da1d197ccafbfa053d493743",
      "summary": "持久化矩阵乘：省掉发射与退出、何时没有收益"
    },
    {
      "collection": "triton-study-logs",
      "id": "l10-block-scaled",
      "path": "docs/triton-learning/logs/2026-10-20-block-scaled-matmul.md",
      "sha256": "eeeda67e2fe0658f83ba13940800d5b100f367a0265b0d68fa2d7cbce898e08b",
      "summary": "块缩放矩阵乘：TMA 块规则与报错时机"
    }
  ],
  "target_collection": "triton-cards",
  "template_registry_sha256": "358d0b6e1ee30ee06c0ae9636266ddafad6f2e81494f6d8975d68448e190996c",
  "template_registry_version": "1.1.0"
}
---
# Markji 表格导入卡片

> Markdown 保留受管元数据与模板定义；卡片数据请使用下列按模板拆分的 XLSX 文件导入。

## 技术问答卡

模板 `technical-qa@1.1.0`：

```text
[P#H1#{{问题}}]
---
{{答案}}
💡 [T#B,!36b59d#{{锚点}}]
📍 [T#!939393#{{来源}}]
```

导入文件：[triton-cross-lesson-synthesis-technical-qa.xlsx](triton-cross-lesson-synthesis-technical-qa.xlsx)（6 张卡）
