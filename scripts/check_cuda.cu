// Standalone environment probe; do not depend on exercise implementations.
#include <cuda_runtime.h>

#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

void check_cuda(cudaError_t status, const char* operation) {
  if (status != cudaSuccess) {
    throw std::runtime_error{std::string{operation} + ": " + cudaGetErrorString(status)};
  }
}

__global__ void increment(int* value) {
  *value += 1;
}

}  // namespace

auto main() -> int {
  try {
    int value = 41;
    int* device_value = nullptr;
    check_cuda(cudaMalloc(&device_value, sizeof(value)), "cudaMalloc");
    check_cuda(cudaMemcpy(device_value, &value, sizeof(value), cudaMemcpyHostToDevice),
               "cudaMemcpy to device");
    increment<<<1, 1>>>(device_value);
    check_cuda(cudaGetLastError(), "kernel launch");
    check_cuda(cudaDeviceSynchronize(), "kernel synchronize");
    check_cuda(cudaMemcpy(&value, device_value, sizeof(value), cudaMemcpyDeviceToHost),
               "cudaMemcpy to host");
    check_cuda(cudaFree(device_value), "cudaFree");
    if (value != 42) {
      throw std::runtime_error{"unexpected CUDA kernel result"};
    }
    std::cout << "Native CUDA environment verification passed\n";
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA environment verification failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
