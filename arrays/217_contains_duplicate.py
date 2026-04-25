"""
========================================================
LeetCode 217 - Contains Duplicate
========================================================
Difficulty : Easy
Link       : https://leetcode.com/problems/contains-duplicate/

Problem Statement
-----------------
Given an integer array nums, return true if any value appears
at least twice in the array, and return false if every element
is distinct.

Examples
--------
Input : nums = [1, 2, 3, 1]
Output: True

Input : nums = [1, 2, 3, 4]
Output: False

Input : nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
Output: True
========================================================
"""

from typing import List
from collections import Counter, defaultdict


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force
# ──────────────────────────────────────────────────────
# Intuition  : Check every pair (i, j) where i < j.
# Time       : O(n²)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def containsDuplicate_brute_force(nums: List[int]) -> bool:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False


# ──────────────────────────────────────────────────────
# Approach 2 : Sorting
# ──────────────────────────────────────────────────────
# Intuition  : After sorting, duplicates become adjacent.
#              One linear scan suffices.
# Time       : O(n log n)
# Space      : O(1)  (in-place sort)
# ──────────────────────────────────────────────────────
def containsDuplicate_sorting(nums: List[int]) -> bool:
    nums.sort()
    for i in range(len(nums) - 1):
        if nums[i] == nums[i + 1]:
            return True
    return False


# ──────────────────────────────────────────────────────
# Approach 3 : Hash Set with Early Exit  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : Insert elements one by one; if a number is
#              already in the set, we found a duplicate.
#              Stops as soon as the first duplicate is found.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def containsDuplicate_hashset(nums: List[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


# ──────────────────────────────────────────────────────
# Approach 4 : Set Length Comparison
# ──────────────────────────────────────────────────────
# Intuition  : A set holds only unique values. If the set
#              is smaller than the list, a duplicate existed.
# Note       : Always processes the entire array (no early exit).
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def containsDuplicate_set_length(nums: List[int]) -> bool:
    return len(set(nums)) != len(nums)

'''
# ──────────────────────────────────────────────────────
# Approach 5 : Counter (collections.Counter)
# ──────────────────────────────────────────────────────
# Intuition  : Count frequency of every element.
#              Any frequency > 1 means a duplicate exists.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def containsDuplicate_counter(nums: List[int]) -> bool:
    freq = Counter(nums)
    return any(count > 1 for count in freq.values())


# ──────────────────────────────────────────────────────
# Approach 6 : Dictionary Frequency Count
# ──────────────────────────────────────────────────────
# Intuition  : Manually track counts; return True the moment
#              any count exceeds 1 (early exit variant of Counter).
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def containsDuplicate_dict(nums: List[int]) -> bool:
    freq: dict[int, int] = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1
        if freq[num] > 1:
            return True
    return False


# ──────────────────────────────────────────────────────
# Approach 7 : defaultdict
# ──────────────────────────────────────────────────────
# Intuition  : Same as dict approach but uses defaultdict(int)
#              to avoid explicit default handling.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def containsDuplicate_defaultdict(nums: List[int]) -> bool:
    freq: defaultdict[int, int] = defaultdict(int)
    for num in nums:
        freq[num] += 1
        if freq[num] > 1:
            return True
    return False


# ──────────────────────────────────────────────────────
# Approach 8 : any() + Generator (Functional Style)
# ──────────────────────────────────────────────────────
# Intuition  : Use any() with a generator that tracks seen
#              elements via a mutable set side-effect.
#              any() short-circuits on the first True.
# Note       : Side-effect inside a generator is unconventional
#              but valid Python; included for completeness.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def containsDuplicate_any_generator(nums: List[int]) -> bool:
    seen: set[int] = set()
    return any((num in seen) or seen.add(num) for num in nums)  # type: ignore[func-returns-value]


# ──────────────────────────────────────────────────────
# Approach 9 : Binary Search on Sorted Copy
# ──────────────────────────────────────────────────────
# Intuition  : For each element, binary-search in the
#              already-sorted prefix to check for a match.
#              Demonstrates bisect usage; not faster than sort.
# Time       : O(n log n)
# Space      : O(n)  — sorted copy
# ──────────────────────────────────────────────────────
import bisect

def containsDuplicate_binary_search(nums: List[int]) -> bool:
    sorted_nums: list[int] = []
    for num in nums:
        pos = bisect.bisect_left(sorted_nums, num)
        if pos < len(sorted_nums) and sorted_nums[pos] == num:
            return True
        bisect.insort(sorted_nums, num)
    return False

'''
# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach              | Time     | Space | Notes                        |
# |----|-----------------------|----------|-------|------------------------------|
# | 1  | Brute Force           | O(n²)    | O(1)  | Simple, slow                 |
# | 2  | Sorting               | O(nlogn) | O(1)  | No extra space               |
# | 3  | Hash Set              | O(n)     | O(n)  | Early exit — best ★          |
# | 4  | Set Length            | O(n)     | O(n)  | One-liner, no early exit     |
# | 5  | Counter               | O(n)     | O(n)  | Builds full freq table first |
# | 6  | Dict Frequency        | O(n)     | O(n)  | Manual Counter w/ early exit |
# | 7  | defaultdict           | O(n)     | O(n)  | Cleaner dict w/ early exit   |
# | 8  | any() + Generator     | O(n)     | O(n)  | Functional, short-circuits   |
# | 9  | Binary Search         | O(nlogn) | O(n)  | bisect demo, not practical   |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 1],                        True),
        ([1, 2, 3, 4],                        False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],      True),
        ([],                                  False),
        ([5],                                 False),
        ([-1, -1],                            True),
        ([0, 0],                              True),
    ]

    solutions = [
        ("1. Brute Force",        containsDuplicate_brute_force),
        ("2. Sorting",            containsDuplicate_sorting),
        ("3. Hash Set",           containsDuplicate_hashset),
        ("4. Set Length",         containsDuplicate_set_length),
    #   ("5. Counter",            containsDuplicate_counter),
    #   ("6. Dict Frequency",     containsDuplicate_dict),
    #   ("7. defaultdict",        containsDuplicate_defaultdict),
    #   ("8. any() Generator",    containsDuplicate_any_generator),
    #  ("9. Binary Search",      containsDuplicate_binary_search),
    ]

    for nums, expected in test_cases:
        print(f"\nnums={nums}  →  expected={expected}")
        for name, fn in solutions:
            result = fn(nums[:])
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}  {name:<22} → {result}")
