"""
========================================================
LeetCode 001 - Two Sum
========================================================
Difficulty : Easy
Link       : https://leetcode.com/problems/two-sum/

Problem Statement
-----------------
Given an array of integers `nums` and an integer `target`,
return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution,
and you may not use the same element twice.

You can return the answer in any order.

Examples
--------
Input : nums = [2, 7, 11, 15], target = 9
Output: [0, 1]  →  nums[0] + nums[1] = 2 + 7 = 9

Input : nums = [3, 2, 4], target = 6
Output: [1, 2]

Input : nums = [3, 3], target = 6
Output: [0, 1]
========================================================
"""

from typing import List


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force
# ──────────────────────────────────────────────────────
# Intuition  : Check every pair (i, j) where i < j.
# Time       : O(n²)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def twoSum_brute_force(nums: List[int], target: int) -> List[int]:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []   # guaranteed to have a solution per problem constraints


# ──────────────────────────────────────────────────────
# Approach 2 : Two-Pass Hash Map
# ──────────────────────────────────────────────────────
# Intuition  : First pass builds a value→index map.
#              Second pass looks up the complement.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def twoSum_two_pass_hashmap(nums: List[int], target: int) -> List[int]:
    index_map = {num: i for i, num in enumerate(nums)}   # pass 1

    for i, num in enumerate(nums):                        # pass 2
        complement = target - num
        if complement in index_map and index_map[complement] != i:
            return [i, index_map[complement]]
    return []


# ──────────────────────────────────────────────────────
# Approach 3 : One-Pass Hash Map  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : While inserting each element, check if
#              its complement was seen before.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def twoSum_one_pass_hashmap(nums: List[int], target: int) -> List[int]:
    seen = {}                              # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


# ──────────────────────────────────────────────────────
# Approach 4 : Sorting + Two Pointers
# ──────────────────────────────────────────────────────
# Intuition  : Sort a (value, original_index) array,
#              then use left/right pointers.
#              We must remember original indices before sorting.
# Note       : Returns original indices, NOT sorted positions.
# Time       : O(n log n)  — dominated by sort
# Space      : O(n)        — for the sorted copy
# ──────────────────────────────────────────────────────
def twoSum_two_pointers(nums: List[int], target: int) -> List[int]:
    indexed = sorted(enumerate(nums), key=lambda x: x[1])
    left, right = 0, len(indexed) - 1

    while left < right:
        current_sum = indexed[left][1] + indexed[right][1]
        if current_sum == target:
            return [indexed[left][0], indexed[right][0]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []


# ──────────────────────────────────────────────────────
# Approach 5 : Walrus Operator  (Python 3.8+)
# ──────────────────────────────────────────────────────
# Intuition  : Use the := (walrus) operator to assign and
#              test the complement in a single expression
#              inside a for-loop, keeping it tight and readable.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def twoSum_pythonic(nums: List[int], target: int) -> List[int]:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        if (comp := target - num) in seen:   # walrus: assign + check in one step
            return [seen[comp], i]
        seen[num] = i
    return []


# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | Approach              | Time    | Space | Notes                    |
# |-----------------------|---------|-------|--------------------------|
# | 1. Brute Force        | O(n²)   | O(1)  | Simple, slow             |
# | 2. Two-Pass Hash Map  | O(n)    | O(n)  | Two iterations           |
# | 3. One-Pass Hash Map  | O(n)    | O(n)  | Best — single pass ★     |
# | 4. Sort + Two Ptr     | O(nlogn)| O(n)  | Good if sorted input     |
# | 5. Walrus Operator    | O(n)    | O(n)  | Clean Python 3.8+ style  |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9,  [0, 1]),
        ([3, 2, 4],       6,  [1, 2]),
        ([3, 3],          6,  [0, 1]),
        ([1, 2, 3, 4, 5], 9,  [3, 4]),
        ([-3, 4, 3, 90],  0,  [0, 2]),
    ]

    solutions = [
        ("Brute Force",        twoSum_brute_force),
        ("Two-Pass Hash Map",  twoSum_two_pass_hashmap),
        ("One-Pass Hash Map",  twoSum_one_pass_hashmap),
        ("Sort + Two Ptrs",    twoSum_two_pointers),
        ("Pythonic",           twoSum_pythonic),
    ]

    for nums, target, expected in test_cases:
        print(f"\nnums={nums}, target={target}  →  expected={sorted(expected)}")
        for name, fn in solutions:
            result = sorted(fn(nums[:], target))   # copy to avoid mutation
            status = True if result == sorted(expected) else False
            print(f"  {status}  {name:<22} → {result}")
