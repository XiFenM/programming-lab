"""Verify the Python GPU stack with real PyTorch and Triton work."""

from importlib.metadata import PackageNotFoundError, version

import tilelang
import torch

from gpu.triton.vector_add import vector_add


def package_version(package_name: str) -> str:
    """Return a useful package version even for editable/local packages."""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "unknown"


def main() -> None:
    """Exercise the installed GPU Python stack and report its versions."""
    print(f"PyTorch:  {package_version('torch')}")
    print(f"Triton:   {package_version('triton')}")
    print(f"TileLang: {package_version('tilelang')}")
    print(f"NumPy:    {package_version('numpy')}")
    print(f"PyTorch CUDA runtime: {torch.version.cuda}")
    print(f"PyTorch cuDNN runtime: {torch.backends.cudnn.version()}")
    print(f"TileLang module: {tilelang.__file__}")

    if not torch.cuda.is_available():
        raise RuntimeError(
            "torch.cuda.is_available() is false; check the host driver, "
            "NVIDIA Container Toolkit, and Compose GPU configuration"
        )

    device = torch.device("cuda:0")
    properties = torch.cuda.get_device_properties(device)
    print(f"GPU: {properties.name} ({properties.total_memory / 2**30:.1f} GiB)")

    torch.manual_seed(0)
    lhs = torch.randn(98_417, device=device)
    rhs = torch.randn(98_417, device=device)

    torch_result = lhs + rhs
    cpu_reference = lhs.cpu() + rhs.cpu()
    torch.testing.assert_close(torch_result.cpu(), cpu_reference)
    print("PyTorch CUDA tensor verification passed")

    triton_result = vector_add(lhs, rhs)
    torch.cuda.synchronize(device)
    torch.testing.assert_close(triton_result, torch_result)
    print("Triton JIT kernel verification passed")

    print("TileLang import verification passed")


if __name__ == "__main__":
    main()
