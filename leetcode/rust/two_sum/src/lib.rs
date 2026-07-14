//! LeetCode 1: Two Sum.

use std::collections::HashMap;

/// Returns the indices of two values whose sum equals `target`.
///
/// Time complexity is O(n); auxiliary space complexity is O(n).
pub fn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {
    let mut seen = HashMap::with_capacity(nums.len());

    for (index, &value) in nums.iter().enumerate() {
        if let Some(&matching_index) = seen.get(&(target - value)) {
            return Some((matching_index, index));
        }
        seen.insert(value, index);
    }

    None
}

#[cfg(test)]
mod tests {
    use super::two_sum;

    #[test]
    fn finds_distinct_values() {
        assert_eq!(two_sum(&[2, 7, 11, 15], 9), Some((0, 1)));
    }

    #[test]
    fn finds_duplicate_values() {
        assert_eq!(two_sum(&[3, 3], 6), Some((0, 1)));
    }

    #[test]
    fn reports_missing_solution() {
        assert_eq!(two_sum(&[1, 2, 3], 100), None);
    }
}
