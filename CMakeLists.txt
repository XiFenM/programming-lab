cmake_minimum_required(VERSION 3.28)

project(
  programming_lab
  VERSION 0.1.0
  LANGUAGES CXX
)

option(PROGRAMMING_LAB_ENABLE_CUDA "Build CUDA exercises" ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(PROGRAMMING_LAB_ENABLE_CUDA)
  if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
    set(CMAKE_CUDA_ARCHITECTURES native)
  endif()

  enable_language(CUDA)
  set(CMAKE_CUDA_STANDARD 20)
  set(CMAKE_CUDA_STANDARD_REQUIRED ON)
  set(CMAKE_CUDA_EXTENSIONS OFF)
endif()

find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
  set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
  if(PROGRAMMING_LAB_ENABLE_CUDA)
    set(CMAKE_CUDA_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
  endif()
endif()

function(enable_project_warnings target_name)
  target_compile_options(
    "${target_name}"
    PRIVATE
      $<$<COMPILE_LANGUAGE:CXX>:-Wall;-Wextra;-Wpedantic;-Wconversion;-Wshadow>
  )

  if(PROGRAMMING_LAB_ENABLE_CUDA)
    target_compile_options(
      "${target_name}"
      PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:-Xcompiler=-Wall,-Wextra,-Wpedantic,-Wshadow>
    )
  endif()
endfunction()

add_executable(
  cpp_two_sum
  leetcode/cpp/two_sum.cpp
  tests/cpp/test_two_sum.cpp
)
target_include_directories(cpp_two_sum PRIVATE "${PROJECT_SOURCE_DIR}")
enable_project_warnings(cpp_two_sum)

if(PROGRAMMING_LAB_ENABLE_CUDA)
  add_executable(cuda_vector_add gpu/cuda/vector_add.cu)
  enable_project_warnings(cuda_vector_add)
endif()

include(CTest)
if(BUILD_TESTING)
  add_test(NAME cpp_two_sum COMMAND cpp_two_sum)
  if(PROGRAMMING_LAB_ENABLE_CUDA)
    add_test(NAME cuda_vector_add COMMAND cuda_vector_add)
  endif()
endif()
