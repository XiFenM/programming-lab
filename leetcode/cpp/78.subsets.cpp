/*
 * @lc app=leetcode id=78 lang=cpp
 *
 * [78] Subsets
 */

// @lc code=start
#include <vector>
using namespace std;
class Solution {
 private:
  vector<vector<int>> res;

 public:
  void findSubset(const vector<int>& nums, int index, int len, const vector<int> now_subset) {
    if (now_subset.size() == len) {
      res.push_back(now_subset);
      return;
    }
    for (int i = index; i < nums.size(); i++) {
      vector<int> next_subset = now_subset;
      next_subset.push_back(nums[i]);
      findSubset(nums, i + 1, len, next_subset);
    }
  }
  vector<vector<int>> subsets(vector<int>& nums) {
    res.clear();
    for (int l = 0; l <= nums.size(); l++) {
      findSubset(nums, 0, l, {});
    }
    return res;
  }
};
// @lc code=end
