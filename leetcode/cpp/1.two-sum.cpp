/*
 * @lc app=leetcode id=1 lang=cpp
 *
 * [1] Two Sum
 */
#include <cstddef>
#include <unordered_map>
#include <vector>
using namespace std;
// @lc code=start
class Solution {
 public:
  vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, size_t> num_map;
    size_t len = nums.size();
    for (size_t i = 0; i < len; i++) {
      if (num_map.contains(target - nums[i])) {
        return std::vector<int>{static_cast<int>(i), static_cast<int>(num_map[target - nums[i]])};
      }
      num_map[nums[i]] = i;
    }
    return std::vector<int>{0, 0};
  }
};
// @lc code=end
