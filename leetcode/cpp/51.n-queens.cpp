/*
 * @lc app=leetcode id=51 lang=cpp
 *
 * [51] N-Queens
 */

// @lc code=start
#include <string>
#include <vector>
using namespace std;
class Solution {
 private:
  vector<vector<string>> res;

 public:
  void findSolutions(int n, const vector<int>& sub_solution) {
    if (sub_solution.size() == n) {
      vector<string> solution;
      for (int i = 0; i < sub_solution.size(); i++) {
        string layout;
        for (int j = 0; j < n; j++) {
          if (j == sub_solution[i]) {
            layout.push_back('Q');
          } else {
            layout.push_back('.');
          }
        }
        solution.push_back(layout);
      }
      res.push_back(solution);
      return;
    }
    int row = static_cast<int>(sub_solution.size());
    for (int col = 0; col < n; col++) {
      // 判断col是否与之前的布置不冲突
      int flag = 0;  // flag==0代表不冲突
      for (int l = 0; l < sub_solution.size(); l++) {
        if ((col == sub_solution[l]) || abs(col - sub_solution[l]) == abs(row - l)) {
          flag = 1;
        }
      }
      if (flag == 0) {
        // col可用
        vector<int> next_solution = sub_solution;
        next_solution.push_back(col);
        findSolutions(n, next_solution);
      }
    }
  }
  vector<vector<string>> solveNQueens(int n) {
    res.clear();
    if (n == 0) {
      return res;
    }
    findSolutions(n, {});
    return res;
  }
};
// @lc code=end
