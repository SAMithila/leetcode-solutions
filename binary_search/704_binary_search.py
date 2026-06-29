"""
LeetCode 704 - Binary Search
Given a sorted array of integers and a target, return the index of
the target. Return -1 if not found.

Example:
  Input:  nums = [-1,0,3,5,9,12], target = 9
  Output: 4

  Input:  nums = [-1,0,3,5,9,12], target = 2
  Output: -1

KEY INSIGHT:
  The array is sorted → every comparison eliminates half the remaining
  elements. Check the middle: if too small go right, if too large go left.
"""

from typing import List
import bisect


# ─────────────────────────────────────────────
# Approach 1: Linear Search (Brute Force)
# Time:  O(n)
# Space: O(1)
# ─────────────────────────────────────────────
def search_linear(nums: List[int], target: int) -> int:
    for i, val in enumerate(nums):   # scan every element
        if val == target:
            return i
    return -1


# ─────────────────────────────────────────────
# Approach 2: Iterative Binary Search
# Time:  O(log n)
# Space: O(1)
#
# Maintain a [left, right] window.
# At each step, check the midpoint and halve the window.
#
# TRACE [-1,0,3,5,9,12], target=9:
#   left=0 right=5 mid=2 → nums[2]=3 < 9  → left=3
#   left=3 right=5 mid=4 → nums[4]=9 == 9 → return 4 ✓
# ─────────────────────────────────────────────
def search_iterative(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2    # find midpoint

        if nums[mid] == target:
            return mid               # found
        elif nums[mid] < target:
            left = mid + 1           # target is in the right half
        else:
            right = mid - 1          # target is in the left half

    return -1                        # target not found


# ─────────────────────────────────────────────
# Approach 3: Recursive Binary Search
# Time:  O(log n)
# Space: O(log n)  — recursion stack depth
# ─────────────────────────────────────────────
def search_recursive(nums: List[int], target: int) -> int:
    def binary_search(left: int, right: int) -> int:
        if left > right:
            return -1                # base case: window is empty

        mid = (left + right) // 2

        if nums[mid] == target:
            return mid               # found
        elif nums[mid] < target:
            return binary_search(mid + 1, right)   # search right half
        else:
            return binary_search(left, mid - 1)    # search left half

    return binary_search(0, len(nums) - 1)

# ─────────────────────────────────────────────
# Approach 4: Built-in bisect
# Time:  O(log n)
# Space: O(1)
#
# bisect_left returns the leftmost index where target could be inserted
# to keep the list sorted. If that index holds the target, it's found.
# ─────────────────────────────────────────────
def search_bisect(nums: List[int], target: int) -> int:
    idx = bisect.bisect_left(nums, target)   # find insertion point
    if idx < len(nums) and nums[idx] == target:
        return idx                           # target exists at that index
    return -1                               # target not in array

# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Iterative Binary Search)
# O(log n) time  |  O(1) space
# Preferred over recursive — no stack overhead
# ─────────────────────────────────────────────
search = search_iterative


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([-1, 0, 3, 5, 9, 12], 9,   4),
        ([-1, 0, 3, 5, 9, 12], 2,  -1),
        ([5],                   5,   0),
        ([5],                   3,  -1),
        ([1, 2, 3, 4, 5],       1,   0),   # target at left edge
        ([1, 2, 3, 4, 5],       5,   4),   # target at right edge
        ([1, 2, 3, 4, 5],       3,   2),   # target in middle
        ([-5, -3, 0, 2, 7],     0,   2),   # negative numbers
        ([1, 3],                3,   1),
        ([1, 3],                1,   0),
    ]

    solvers = [
        ("Linear",    search_linear),
        ("Iterative", search_iterative),
        ("Recursive", search_recursive),
        ("Bisect",    search_bisect),
    ]

    for nums, target, expected in tests:
        for name, fn in solvers:
            out = fn(nums[:], target)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | nums={nums} target={target} | got={out}")
