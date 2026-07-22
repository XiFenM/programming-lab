/*
 * @lc app=leetcode id=2 lang=cpp
 *
 * [2] Add Two Numbers
 */

// @lc code=start
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
 public:
  ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
    ListNode* p = l1;
    ListNode* q = l2;
    ListNode* res = new ListNode();
    ListNode* l = res;
    int carry = 0;
    while (p || q || (carry != 0)) {
      if (p) {
        carry += p->val;
      }
      if (q) {
        carry += q->val;
      }
      ListNode* num = new ListNode(carry % 10);
      l->next = num;
      carry = carry / 10;
      l = l->next;
      if (p) {
        p = p->next;
      }
      if (q) {
        q = q->next;
      }
    }
    return res->next;
  }
};
// @lc code=end
