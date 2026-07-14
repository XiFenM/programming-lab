#include <cuda_runtime.h>

#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

void check_cuda(cudaError_t status, const char* operation) {
  if (status != cudaSuccess) {
    throw std::runtime_error{std::string{operation} + ": " + cudaGetErrorString(status)};
  }
}

__global__ void vector_add(const float* lhs, const float* rhs, float* output,
                           std::size_t element_count) {
  const auto index = static_cast<std::size_t>(blockIdx.x) * blockDim.x + threadIdx.x;
  if (index < element_count) {
    output[index] = lhs[index] + rhs[index];
  }
}

}  // namespace

auto main() -> int {
  try {
    constexpr std::size_t element_count = 1U << 20U;
    constexpr int threads_per_block = 256;
    const std::size_t byte_count = element_count * sizeof(float);

    const std::vector<float> host_lhs(element_count, 1.25F);
    const std::vector<float> host_rhs(element_count, 2.75F);
    std::vector<float> host_output(element_count);

    float* device_lhs = nullptr;
    float* device_rhs = nullptr;
    float* device_output = nullptr;

    check_cuda(cudaMalloc(reinterpret_cast<void**>(&device_lhs), byte_count), "cudaMalloc(lhs)");
    check_cuda(cudaMalloc(reinterpret_cast<void**>(&device_rhs), byte_count), "cudaMalloc(rhs)");
    check_cuda(cudaMalloc(reinterpret_cast<void**>(&device_output), byte_count),
               "cudaMalloc(output)");

    check_cuda(cudaMemcpy(device_lhs, host_lhs.data(), byte_count, cudaMemcpyHostToDevice),
               "cudaMemcpy(lhs)");
    check_cuda(cudaMemcpy(device_rhs, host_rhs.data(), byte_count, cudaMemcpyHostToDevice),
               "cudaMemcpy(rhs)");

    const auto block_count = static_cast<unsigned int>(
        (element_count + static_cast<std::size_t>(threads_per_block) - 1U) /
        static_cast<std::size_t>(threads_per_block));
    vector_add<<<block_count, threads_per_block>>>(device_lhs, device_rhs, device_output,
                                                   element_count);
    check_cuda(cudaGetLastError(), "vector_add launch");
    check_cuda(cudaDeviceSynchronize(), "vector_add synchronize");

    check_cuda(cudaMemcpy(host_output.data(), device_output, byte_count, cudaMemcpyDeviceToHost),
               "cudaMemcpy(output)");

    check_cuda(cudaFree(device_lhs), "cudaFree(lhs)");
    check_cuda(cudaFree(device_rhs), "cudaFree(rhs)");
    check_cuda(cudaFree(device_output), "cudaFree(output)");

    for (const float value : host_output) {
      if (std::abs(value - 4.0F) > 1.0e-5F) {
        std::cerr << "CUDA vector-add verification failed\n";
        return EXIT_FAILURE;
      }
    }

    std::cout << "CUDA vector-add verification passed on " << element_count << " elements\n";
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA smoke test failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
