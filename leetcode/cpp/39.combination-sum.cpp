/*
 * @lc app=leetcode id=39 lang=cpp
 *
 * [39] Combination Sum
 */

// 如何去重？为什么index = i就成功去重了？
// @lc code=start
#include <cstddef>
#include <vector>
using namespace std;
class Solution {
 private:
  vector<vector<int>> res;
  void findCombination(const vector<int>& candidates, int remaining_target, size_t index,
                       const vector<int>& now) {
    if (remaining_target == 0) {
      res.push_back(now);
      return;
    }
    for (size_t i = index; i < candidates.size(); i++) {
      if (candidates[i] <= remaining_target) {
        vector<int> now_add_ele = now;
        now_add_ele.push_back(candidates[i]);
        findCombination(candidates, remaining_target - candidates[i], i, now_add_ele);
      }
    }
  }

 public:
  vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    res.clear();
    findCombination(candidates, target, 0, {});
    return res;
  }
};
// @lc code=end
