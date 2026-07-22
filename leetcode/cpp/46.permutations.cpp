/*
 * @lc app=leetcode id=46 lang=cpp
 *
 * [46] Permutations
 */

// @lc code=start
#include <cstddef>
#include <vector>
using namespace std;
class Solution {
 private:
  vector<vector<int>> res;
  void findNums(const vector<int>& remaining_nums, const vector<int>& previous_nums) {
    if (remaining_nums.empty()) {
      res.push_back(previous_nums);
      return;
    }
    for (size_t i = 0; i < remaining_nums.size(); i++) {
      vector<int> next_remaining_nums = remaining_nums;
      vector<int> next_nums = previous_nums;
      next_nums.push_back(remaining_nums[i]);
      next_remaining_nums.erase(next_remaining_nums.begin() + i);
      findNums(next_remaining_nums, next_nums);
    }
  }

 public:
  vector<vector<int>> permute(vector<int>& nums) {
    res.clear();
    if (nums.empty()) {
      return res;
    }
    findNums(nums, {});
    return res;
  }
};
// @lc code=end
