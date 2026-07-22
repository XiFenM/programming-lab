/*
 * @lc app=leetcode id=131 lang=cpp
 *
 * [131] Palindrome Partitioning
 */

// @lc code=start
#include <string>
#include <vector>
using namespace std;
class Solution {
 private:
  bool is_palindrome(const string& s, int start, int end) {
    int half = (end - start + 1) / 2;
    for (int i = 0; i < half; i++) {
      if (s[start + i] != s[end - i]) {
        return false;
      }
    }
    return true;
  }
  vector<vector<string>> res;
  void findPartition(const string& s, int index, vector<string>& temp_s) {
    if (index == s.size()) {
      res.push_back(temp_s);
      return;
    }
    for (int i = index; i < s.size(); i++) {
      if (is_palindrome(s, index, i)) {
        temp_s.push_back(s.substr(index, i - index + 1));
        findPartition(s, i + 1, temp_s);
        temp_s.pop_back();
      }
    }
  }

 public:
  vector<vector<string>> partition(string s) {
    res.clear();
    vector<string> temp_s = {};
    findPartition(s, 0, temp_s);
    return res;
  }
};
// @lc code=end
