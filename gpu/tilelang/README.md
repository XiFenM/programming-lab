# TileLang 练习目录

`scripts/check_python_gpu.py` 会验证 TileLang 能否导入，并打印安装版本。TileLang 的 DSL API
仍在快速演进，因此仓库没有把某一版本的 kernel 模板伪装成长期稳定接口。完成首次 `uv sync`
并生成 `uv.lock` 后，请以该锁定版本的官方示例为起点在本目录添加练习，并为每个 kernel 同时保留：

- 一个 PyTorch 参考实现；
- 正确性断言（建议覆盖非整块尺寸）；
- warm-up 后的基准测试；
- 输入尺寸、数据类型、GPU 型号和 TileLang 版本记录。
