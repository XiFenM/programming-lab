#include "leetcode/cpp/two_sum.hpp"

#include <cstddef>
#include <stdexcept>
#include <unordered_map>

namespace leetcode {

auto two_sum(const std::vector<int>& nums, int target) -> std::array<int, 2> {
  std::unordered_map<int, std::size_t> seen;
  seen.reserve(nums.size());

  for (std::size_t index = 0; index < nums.size(); ++index) {
    const int complement = target - nums[index];
    if (const auto match = seen.find(complement); match != seen.end()) {
      return {static_cast<int>(match->second), static_cast<int>(index)};
    }
    seen.emplace(nums[index], index);
  }

  throw std::invalid_argument{"no two-sum solution exists"};
}

}  // namespace leetcode
