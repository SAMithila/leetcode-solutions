"""
========================================================
LeetCode 560 - Subarray Sum Equals K
========================================================
Difficulty : Medium
Link       : https://leetcode.com/problems/subarray-sum-equals-k/

Problem Statement
-----------------
Given an array of integers nums and an integer k, return the
total number of subarrays whose sum equals k.

A subarray is a contiguous non-empty sequence of elements
within an array.

Examples
--------
Input : nums = [1, 1, 1], k = 2
Output: 2

Input : nums = [1, 2, 3], k = 3
Output: 2  →  [1,2] and [3]

Input : nums = [1, -1, 1], k = 1
Output: 3  →  [1], [1,-1,1], [1]

Constraints
-----------
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

Key insight
-----------
sum(i..j) = prefix[j] - prefix[i-1]
We want sum == k  →  prefix[i-1] = prefix[j] - k
So for each j, count how many past prefix sums equal prefix[j] - k.
========================================================
"""

from typing import List
from collections import defaultdict


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force  (three loops)
# ──────────────────────────────────────────────────────
# Intuition  : For every pair (i, j), compute the subarray
#              sum from scratch with a third inner loop.
# Time       : O(n³)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def subarraySum_brute_force(nums: List[int], k: int) -> int:
    n = len(nums)
    count = 0
    for i in range(n):
        for j in range(i, n):
            total = sum(nums[i:j + 1])   # O(n) each time
            if total == k:
                count += 1
    return count


# ──────────────────────────────────────────────────────
# Approach 2 : Running Sum  (two loops)
# ──────────────────────────────────────────────────────
# Intuition  : Fix start index i. Extend j one step at a time,
#              accumulating the sum. No need to recompute
#              the entire subarray each time.
# Time       : O(n²)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def subarraySum_running_sum(nums: List[int], k: int) -> int:
    n = len(nums)
    count = 0
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            if total == k:
                count += 1
    return count

'''
# ──────────────────────────────────────────────────────
# Approach 3 : Prefix Sum Array + Nested Loop
# ──────────────────────────────────────────────────────
# Intuition  : Pre-build a prefix sum array so that
#              sum(i..j) = prefix[j+1] - prefix[i].
#              Check every (i, j) pair in O(1) each.
# Time       : O(n²)
# Space      : O(n)  — prefix array
# ──────────────────────────────────────────────────────
def subarraySum_prefix_array(nums: List[int], k: int) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    count = 0
    for i in range(n):
        for j in range(i + 1, n + 1):
            if prefix[j] - prefix[i] == k:
                count += 1
    return count
'''

# ──────────────────────────────────────────────────────
# Approach 4 : Prefix Sum + Hash Map  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : We need prefix[j] - prefix[i] == k
#              ↔  prefix[i] == prefix[j] - k
#
#              As we scan left-to-right, keep a running
#              prefix sum and a frequency map of all
#              prefix sums seen so far.
#              For each new prefix sum p, the number of
#              valid subarrays ending here = freq[p - k].
#
#              Initialise freq = {0: 1} to account for
#              subarrays that start at index 0.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def subarraySum_hashmap(nums: List[int], k: int) -> int:
    freq: dict[int, int] = {0: 1}   # prefix_sum → count
    prefix = 0
    count  = 0

    for num in nums:
        prefix += num
        count  += freq.get(prefix - k, 0)   # how many past sums equal prefix-k
        freq[prefix] = freq.get(prefix, 0) + 1

    return count

'''
# ──────────────────────────────────────────────────────
# Approach 5 : Prefix Sum + defaultdict  (cleaner variant)
# ──────────────────────────────────────────────────────
# Intuition  : Same as Approach 4; defaultdict(int) removes
#              the .get() fallback boilerplate.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def subarraySum_defaultdict(nums: List[int], k: int) -> int:
    freq: defaultdict[int, int] = defaultdict(int)
    freq[0] = 1
    prefix = 0
    count  = 0

    for num in nums:
        prefix += num
        count  += freq[prefix - k]
        freq[prefix] += 1

    return count
'''

# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach                | Time  | Space | Notes                        |
# |----|-------------------------|-------|-------|------------------------------|
# | 1  | Brute Force (3 loops)   | O(n³) | O(1)  | Recomputes every sum         |
# | 2  | Running Sum (2 loops)   | O(n²) | O(1)  | Avoids recomputing sum       |
# | 3  | Prefix Array + 2 loops  | O(n²) | O(n)  | Pre-built prefix array       |
# | 4  | Prefix Sum + Hash Map   | O(n)  | O(n)  | One-pass — optimal ★        |
# | 5  | Prefix Sum + defaultdict| O(n)  | O(n)  | Cleaner version of #4        |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([1, 1, 1],          2,  2),
        ([1, 2, 3],          3,  2),
        ([1, -1, 1],         1,  3),
        ([1],                1,  1),
        ([1],                0,  0),
        ([-1, -1, 1],        0,  1),
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
        ([1, 2, 1, 2, 1],    3,  4),
    ]

    solutions = [
        ("1. Brute Force (3 loops)",    subarraySum_brute_force),
        ("2. Running Sum (2 loops)",    subarraySum_running_sum),
     #  ("3. Prefix Array + 2 loops",  subarraySum_prefix_array),
        ("4. Prefix Sum + Hash Map",   subarraySum_hashmap),
     #  ("5. Prefix Sum + defaultdict",subarraySum_defaultdict),
    ]

    for nums, k, expected in test_cases:
        print(f"\nnums={nums}, k={k}  →  expected={expected}")
        for name, fn in solutions:
            result = fn(nums[:], k)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}  {name:<30} → {result}")
