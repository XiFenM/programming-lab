#include "leetcode/cpp/two_sum.hpp"

#include <array>
#include <cassert>
#include <stdexcept>
#include <vector>

auto main() -> int {
  const auto first = leetcode::two_sum(std::vector<int>{2, 7, 11, 15}, 9);
  assert((first == std::array<int, 2>{0, 1}));

  const auto duplicate = leetcode::two_sum(std::vector<int>{3, 3}, 6);
  assert((duplicate == std::array<int, 2>{0, 1}));

  try {
    static_cast<void>(leetcode::two_sum(std::vector<int>{1, 2, 3}, 100));
  } catch (const std::invalid_argument&) {
    return 0;
  }

  return 1;
}
