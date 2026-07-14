"""LeetCode 1: Two Sum."""


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """Return the indices of two values whose sum equals ``target``.

    Time complexity is O(n); auxiliary space complexity is O(n).
    """
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return seen[complement], index
        seen[value] = index

    raise ValueError("no two-sum solution exists")
