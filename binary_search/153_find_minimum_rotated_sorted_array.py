"""
LeetCode 153 - Find Minimum in Rotated Sorted Array
Given a sorted array rotated at an unknown pivot, find the minimum element.
All values are unique.

Example:
  Input:  nums = [3,4,5,1,2]
  Output: 1

  Input:  nums = [4,5,6,7,0,1,2]
  Output: 0

  Input:  nums = [11,13,15,17]
  Output: 11  (no rotation)

KEY INSIGHT:
  The minimum element is the only one smaller than its left neighbor
  — it's the "inflection point" where the rotation happened.
  Binary search: compare nums[mid] with nums[right].
    - nums[mid] > nums[right] → min is in the right half
    - nums[mid] < nums[right] → min is in the left half (mid could be it)
"""

from typing import List


# ─────────────────────────────────────────────
# Approach 1: Brute Force (Linear Scan)
# Time:  O(n)
# Space: O(1)
# ─────────────────────────────────────────────
def findMin_brute(nums: List[int]) -> int:
    minimum = nums[0]
    for val in nums:           # scan every element
        minimum = min(minimum, val)
    return minimum


# ─────────────────────────────────────────────
# Approach 2: Binary Search
# Time:  O(log n)
# Space: O(1)
#
# Compare nums[mid] with nums[right] to determine which half
# contains the minimum (the inflection point).
#
# WHY compare with right (not left)?
#   Comparing with right always tells us which side is "broken".
#   If nums[mid] > nums[right] → right side has the drop → min is right
#   If nums[mid] < nums[right] → right side is clean → min is left (or mid)
#
# TRACE [4,5,6,7,0,1,2]:
#   left=0 right=6 mid=3 → nums[3]=7 > nums[6]=2 → left=4
#   left=4 right=6 mid=5 → nums[5]=1 < nums[6]=2 → right=5
#   left=4 right=5 mid=4 → nums[4]=0 < nums[5]=1 → right=4
#   left=4 right=4 → return nums[4] = 0 ✓
# ─────────────────────────────────────────────
def findMin_binary(nums: List[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:                      # stop when window collapses to 1
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            left = mid + 1                   # min is in the right half
        else:
            right = mid                      # min is in the left half (mid included)

    return nums[left]                        # left == right == index of minimum


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Binary Search)
# O(log n) time  |  O(1) space
# ─────────────────────────────────────────────
findMin = findMin_binary


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([3, 4, 5, 1, 2],          1),
        ([4, 5, 6, 7, 0, 1, 2],    0),
        ([11, 13, 15, 17],         11),   # no rotation
        ([1],                       1),
        ([2, 1],                    1),
        ([3, 1, 2],                 1),
        ([5, 6, 7, 8, 1, 2, 3, 4], 1),
        ([1, 2],                    1),
        ([2, 3, 4, 5, 1],           1),
    ]

    solvers = [
        ("Brute Force",  findMin_brute),
        ("Binary Search",findMin_binary),
    ]

    for nums, expected in tests:
        for name, fn in solvers:
            out = fn(nums[:])
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | nums={nums} | got={out}")
