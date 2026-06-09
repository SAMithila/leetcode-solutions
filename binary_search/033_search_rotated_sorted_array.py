"""
LeetCode 33 - Search in Rotated Sorted Array
A sorted array was rotated at an unknown pivot. Given the rotated
array and a target, return its index or -1 if not found.

Example:
  Input:  nums = [4,5,6,7,0,1,2], target = 0
  Output: 4

  Input:  nums = [4,5,6,7,0,1,2], target = 3
  Output: -1

  Input:  nums = [1], target = 0
  Output: -1

KEY INSIGHT:
  Even after rotation, one half of the array is always sorted.
  Use that guarantee to decide which half to search next.
  e.g. [4,5,6,7,0,1,2] — mid=7, left half [4,5,6,7] is sorted.
"""

from typing import List


# ─────────────────────────────────────────────
# Approach 1: Brute Force (Linear Search)
# Time:  O(n)
# Space: O(1)
# ─────────────────────────────────────────────
def search_brute(nums: List[int], target: int) -> int:
    for i, val in enumerate(nums):   # scan every element
        if val == target:
            return i
    return -1


# ─────────────────────────────────────────────
# Approach 2: Find Pivot + Binary Search
# Time:  O(log n)
# Space: O(1)
#
# Step 1: Find pivot (index of smallest element) via binary search.
# Step 2: Binary search the correct half based on target vs nums[0].
#
# Pivot example: [4,5,6,7,0,1,2] → pivot = 4 (index of 0)
# ─────────────────────────────────────────────
def search_pivot(nums: List[int], target: int) -> int:
    n = len(nums)
    left, right = 0, n - 1

    # Step 1: find pivot (leftmost / smallest element)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1    # pivot is in the right half
        else:
            right = mid       # pivot is in the left half (or mid itself)
    pivot = left              # index of smallest element

    # Step 2: binary search in the correct half
    if target >= nums[pivot] and target <= nums[n - 1]:
        left, right = pivot, n - 1    # target is in the right segment
    else:
        left, right = 0, pivot - 1   # target is in the left segment

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# ─────────────────────────────────────────────
# Approach 3: One-pass Modified Binary Search
# Time:  O(log n)
# Space: O(1)
#
# At every mid, one of the two halves is always fully sorted.
# Use that sorted half to decide where target could be:
#   - If left half sorted AND target in [nums[left], nums[mid]] → go left
#   - Else → go right
#   - If right half sorted AND target in [nums[mid], nums[right]] → go right
#   - Else → go left
# ─────────────────────────────────────────────
def search_onepass(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1   # target is in the sorted left half
            else:
                left = mid + 1    # target must be in the right half
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1    # target is in the sorted right half
            else:
                right = mid - 1   # target must be in the left half

    return -1


# ─────────────────────────────────────────────
# OPTIMAL — Approach 3 (One-pass Modified Binary Search)
# O(log n) time  |  O(1) space
# No need to find pivot first — single clean pass
# ─────────────────────────────────────────────
search = search_onepass


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([4, 5, 6, 7, 0, 1, 2], 0,  4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1],                   0, -1),
        ([1],                   1,  0),
        ([3, 1],                1,  1),
        ([3, 1],                3,  0),
        ([5, 1, 3],             3,  2),
        ([1, 3],                3,  1),
        ([4, 5, 6, 7, 8, 1, 2, 3], 8, 4),
        ([6, 7, 1, 2, 3, 4, 5], 3,  4),
        ([1, 2, 3, 4, 5, 6, 7], 4,  3),   # no rotation
    ]

    solvers = [
        ("Brute Force",  search_brute),
        ("Find Pivot",   search_pivot),
        ("One Pass",     search_onepass),
    ]

    for nums, target, expected in tests:
        for name, fn in solvers:
            out = fn(nums[:], target)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | nums={nums} target={target} | got={out}")
