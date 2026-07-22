/*
 * @lc app=leetcode id=17 lang=cpp
 *
 * [17] Letter Combinations of a Phone Number
 */

// @lc code=start
#include <cstddef>
#include <string>
#include <vector>
using namespace std;
class Solution {
 private:
  vector<string> letter_map = {
      " ",     // 0
      "",      // 1
      "abc",   // 2
      "def",   // 3
      "ghi",   // 4
      "jkl",   // 5
      "mno",   // 6
      "pqrs",  // 7
      "tuv",   // 8
      "wxyz",  // 9
  };
  vector<string> res;

 public:
  void findCombinations(const string& digits, size_t index, const string& previous_string) {
    if (index == digits.size()) {
      // 保存previous_string
      res.push_back(previous_string);
      return;
    }
    char c = digits[index];
    string now = letter_map[static_cast<size_t>(c - '0')];
    for (size_t i = 0; i < now.size(); i++) {
      findCombinations(digits, index + 1, previous_string + now[i]);
    }
  }
  vector<string> letterCombinations(string digits) {
    res.clear();
    if (digits.empty()) {
      return res;
    }
    findCombinations(digits, 0, "");
    return res;
  }
};
// @lc code=end
