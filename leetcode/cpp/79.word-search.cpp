/*
 * @lc app=leetcode id=79 lang=cpp
 *
 * [79] Word Search
 */

// @lc code=start
#include <cstdio>
#include <string>
#include <vector>
using namespace std;
class Solution {
 public:
  bool exist_by_location(const vector<vector<char>>& board, vector<vector<int>>& visited,
                         const vector<int>& location, int index, const string& word) {
    if (index == word.size()) {
      return true;
    }
    char wanted = word[index];
    // 分别判断上下左右位置元素是否符合要求。
    // 上
    if (location[0] > 0 && visited[location[0] - 1][location[1]] == 0 &&
        board[location[0] - 1][location[1]] == wanted) {
      visited[location[0] - 1][location[1]] = 1;
      bool res = exist_by_location(board, visited, {location[0] - 1, location[1]}, index + 1, word);
      visited[location[0] - 1][location[1]] = 0;
      if (res) {
        return true;
      }
    }
    // 下
    if (location[0] < board.size() - 1 && visited[location[0] + 1][location[1]] == 0 &&
        board[location[0] + 1][location[1]] == wanted) {
      visited[location[0] + 1][location[1]] = 1;
      bool res = exist_by_location(board, visited, {location[0] + 1, location[1]}, index + 1, word);
      visited[location[0] + 1][location[1]] = 0;
      if (res) {
        return true;
      }
    }
    // 左
    if (location[1] > 0 && visited[location[0]][location[1] - 1] == 0 &&
        board[location[0]][location[1] - 1] == wanted) {
      visited[location[0]][location[1] - 1] = 1;
      bool res = exist_by_location(board, visited, {location[0], location[1] - 1}, index + 1, word);
      visited[location[0]][location[1] - 1] = 0;
      if (res) {
        return true;
      }
    }
    // 右
    if (location[1] < board[0].size() - 1 && visited[location[0]][location[1] + 1] == 0 &&
        board[location[0]][location[1] + 1] == wanted) {
      visited[location[0]][location[1] + 1] = 1;
      bool res = exist_by_location(board, visited, {location[0], location[1] + 1}, index + 1, word);
      visited[location[0]][location[1] + 1] = 0;
      if (res) {
        return true;
      }
    }
    return false;
  }
  bool exist(vector<vector<char>>& board, string word) {
    vector<vector<int>> visited(board.size(), vector<int>(board[0].size()));
    for (int i = 0; i < board.size(); i++) {
      for (int j = 0; j < board[0].size(); j++) {
        visited[i][j] = 0;
      }
    }
    for (int i = 0; i < board.size(); i++) {
      for (int j = 0; j < board[0].size(); j++) {
        if (board[i][j] == word[0]) {
          visited[i][j] = 1;
          bool res = exist_by_location(board, visited, {i, j}, 1, word);
          visited[i][j] = 0;
          if (res) {
            return true;
          }
        }
      }
    }
    return false;
  }
};
// @lc code=end
