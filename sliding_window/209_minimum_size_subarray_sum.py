"""
LeetCode 209 - Minimum Size Subarray Sum
Given an array of positive integers nums and a positive integer target,
return the minimal length of a subarray whose sum >= target.
Return 0 if no such subarray exists.

Example:
  Input:  target = 7, nums = [2,3,1,2,4,3]
  Output: 2  ([4,3])

  Input:  target = 4, nums = [1,4,4]
  Output: 1  ([4])

  Input:  target = 11, nums = [1,1,1,1,1,1,1,1]
  Output: 0

KEY INSIGHT:
  All numbers are positive → adding more always increases sum,
  removing always decreases. This monotonic property makes
  two-pointer / sliding window provably correct and O(n).
"""

from typing import List
import bisect


# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(n^2)
# Space: O(1)
#
# Try every possible starting index.
# Expand right until sum >= target, record length, then move on.
# The `break` is valid because all nums are positive — a longer
# window from the same left can only be worse (larger length).
# ─────────────────────────────────────────────
def minSubArrayLen_brute(target: int, nums: List[int]) -> int:
    n = len(nums)
    best = float("inf")

    for left in range(n):          # try every starting position
        total = 0
        for right in range(left, n):
            total += nums[right]   # expand window to the right
            if total >= target:
                best = min(best, right - left + 1)  # valid window — record length
                break   # longer window from same left = worse answer
                        # only valid because all nums > 0

    return 0 if best == float("inf") else best


# ─────────────────────────────────────────────
# Approach 2: Sliding Window
# Time:  O(n)  — each element is added & removed at most once
# Space: O(1)
#
# Two pointers: right expands the window, left shrinks it.
#
# WHY the while loop (not if):
#   After shrinking once, total might still be >= target,
#   so keep shrinking to find the minimum valid window.
#
# WHY this is O(n) and not O(n^2):
#   left only ever moves forward — at most n times total
#   across all iterations of the outer loop.
# ─────────────────────────────────────────────
def minSubArrayLen_sliding(target: int, nums: List[int]) -> int:
    left = 0
    total = 0
    best = float("inf")

    for right in range(len(nums)):
        total += nums[right]           # expand: add right element to window

        while total >= target:         # window is valid — try to shrink it
            best = min(best, right - left + 1)  # record current window length
            total -= nums[left]        # shrink: remove left element from window
            left += 1                  # move left pointer forward

    return 0 if best == float("inf") else best

'''
# ─────────────────────────────────────────────
# Approach 3: Prefix Sum + Binary Search
# Time:  O(n log n)
# Space: O(n)
#
# prefix[i] = sum of nums[0..i-1]
# sum of subarray [left, right) = prefix[right] - prefix[left]
#
# For a fixed left, we want the smallest right such that:
#   prefix[right] >= prefix[left] + target
#
# Since prefix is strictly increasing (all nums > 0),
# binary search finds this right in O(log n).
#
# TRACE for nums=[2,3,1,2,4,3], target=7:
#   prefix = [0, 2, 5, 6, 8, 12, 15]
#   left=0: needed=7, bisect finds right=4 → length=4
#   left=1: needed=9, bisect finds right=5 → length=4
#   left=4: needed=16, bisect finds right=6 → length=2  ← best
# ─────────────────────────────────────────────
def minSubArrayLen_binary(target: int, nums: List[int]) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)         # prefix[0] = 0 (empty subarray)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]   # prefix[i+1] = sum of nums[0..i]

    best = float("inf")
    for left in range(n):
        needed = prefix[left] + target         # minimum prefix[right] to satisfy sum >= target
        right = bisect.bisect_left(prefix, needed)  # find smallest valid right index
        if right <= n:                         # right <= n means a valid subarray exists
            best = min(best, right - left)     # subarray length = right - left

    return 0 if best == float("inf") else best
'''

# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Sliding Window)
# O(n) time  |  O(1) space
# ─────────────────────────────────────────────
minSubArrayLen = minSubArrayLen_sliding


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        (7,  [2, 3, 1, 2, 4, 3],       2),
        (4,  [1, 4, 4],                 1),
        (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),
        (15, [1, 2, 3, 4, 5],           5),
        (7,  [2, 3, 1, 2, 4, 3],        2),
        (1,  [1, 1, 1],                 1),
        (100,[1, 2, 3],                 0),
        (6,  [10, 2, 3],                1),
    ]

    solvers = [
        ("Brute Force",  minSubArrayLen_brute),
        ("Sliding",      minSubArrayLen_sliding),
     #   ("Binary Search",minSubArrayLen_binary),
    ]

    for target, nums, expected in tests:
        for name, fn in solvers:
            out = fn(target, nums[:])
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | target={target} nums={nums} | got={out}")
