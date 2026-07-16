# Triton 官方教程学习区

这里保存从 Triton 官方文档下载的教程源码，以及本仓库建议的学习顺序。
`official/` 中的文件保持官方原样，学习笔记和练习代码请分别放到 `notes/` 和
`gpu/triton/`，这样后续更新官方教程时不会覆盖自己的修改。

## 开始之前

仓库的 `pyproject.toml` 已声明 `torch`、`triton` 和 `pytest`。进入已配置 GPU 的开发容器后，
先确认环境：

```bash
make doctor
uv run python gpu/triton/vector_add.py
```

教程需要受支持的 GPU；不同教程对 GPU 架构的要求不同。前几课适合先学习，后面的 persistent
matmul 和 block-scaled matmul 涉及更新的硬件特性，不必一开始就追求跑通全部 benchmark。

## 建议路线

| 阶段 | 官方源码 | 学习重点 |
| --- | --- | --- |
| 1 | [`01-vector-add.py`](official/01-vector-add.py) | JIT kernel、program ID、block、offset、mask、launch grid |
| 2 | [`02-fused-softmax.py`](official/02-fused-softmax.py) | 行级并行、reduction、融合、occupancy 与性能分析 |
| 3 | [`03-matrix-multiplication.py`](official/03-matrix-multiplication.py) | 二维分块、指针运算、`tl.dot`、autotune |
| 4 | [`04-low-memory-dropout.py`](official/04-low-memory-dropout.py) | Triton 随机数与可复现性 |
| 5 | [`05-layer-norm.py`](official/05-layer-norm.py) | forward/backward、reduction、并发更新 |
| 6 | [`06-fused-attention.py`](official/06-fused-attention.py) | Flash Attention、分阶段计算与硬件相关优化 |
| 7 | [`07-extern-functions.py`](official/07-extern-functions.py) | 调用 `tl.extra.libdevice` 外部数学函数 |
| 8 | [`08-grouped-gemm.py`](official/08-grouped-gemm.py) | 多个 GEMM 的调度与 descriptor |
| 9 | [`09-persistent-matmul.py`](official/09-persistent-matmul.py) | persistent kernel、TMA、warp specialization |
| 10 | [`10-block-scaled-matmul.py`](official/10-block-scaled-matmul.py) | block-scaled 数据类型和新一代 Tensor Core |

官方建议按顺序阅读。实际学习时可先完成 01–03，确保掌握 Triton 的核心编程模型，再进入
算子融合和高级硬件专题。

## 每课的学习循环

1. 先读文件开头的目标说明和 PyTorch baseline。
2. 手画一个 program 负责的数据块，明确 grid、block shape 和 mask。
3. 只读 kernel，逐行写下每个张量的 shape 和所在存储层级。
4. 运行正确性检查，再运行 benchmark；不要只比较速度而跳过数值误差。
5. 在 `gpu/triton/` 自己重写一个最小版本，不直接修改 `official/`。
6. 改一个参数或边界条件，预测结果后再实验。

第一课可直接运行：

```bash
uv run python docs/triton-tutorials/official/01-vector-add.py
```

部分高级教程还导入 `tabulate`、Proton profiler 或只在特定 GPU 架构上可用的 Triton API。
遇到缺少可选依赖或硬件不支持时，先阅读代码和完成较低阶段练习，不要为了跑 benchmark
盲目更换 Triton 版本。

## 来源与更新

下载来源、日期和校验值记录在 [`SOURCE.md`](SOURCE.md)。官方 `main` 文档会持续变化，更新时
应重新下载完整压缩包并同步更新来源记录，避免混合不同日期的教程文件。
