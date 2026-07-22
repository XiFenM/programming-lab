/*
 * @lc app=leetcode id=22 lang=cpp
 *
 * [22] Generate Parentheses
 */

// @lc code=start
#include <string>
#include <vector>
using namespace std;
class Solution {
 private:
  vector<string> res;
  void findParenthesis(int n, int num_left, int num_right, const string& pre) {
    if (num_left + num_right == 2 * n) {
      // 找到一个合法括号字符串
      res.push_back(pre);
      return;
    }
    if (num_left < n) {
      // 可以添加左括号
      findParenthesis(n, num_left + 1, num_right, pre + '(');
    }
    if (num_left > num_right) {
      // 可以添加右括号
      findParenthesis(n, num_left, num_right + 1, pre + ')');
    }
  }

 public:
  vector<string> generateParenthesis(int n) {
    res.clear();
    if (n <= 0) {
      return res;
    }
    findParenthesis(n, 0, 0, "");
    return res;
  }
};
// @lc code=end
