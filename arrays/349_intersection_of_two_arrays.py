"""
========================================================
LeetCode 349 - Intersection of Two Arrays
========================================================
Difficulty : Easy
Link       : https://leetcode.com/problems/intersection-of-two-arrays/

Problem Statement
-----------------
Given two integer arrays nums1 and nums2, return an array of
their intersection. Each element in the result must be UNIQUE
and you may return the result in any order.

Examples
--------
Input : nums1 = [1, 2, 2, 1], nums2 = [2, 2]
Output: [2]

Input : nums1 = [4, 9, 5], nums2 = [9, 4, 9, 8, 4]
Output: [9, 4]  (order does not matter)

Key difference from LeetCode 350
---------------------------------
| Problem | Each element in result |  Use       |
|---------|------------------------|------------|
| 349     | Unique (once only)     | Hash Set ✓ |
| 350     | Count duplicates       | Hash Map ✓ |
========================================================
"""

from typing import List
import bisect


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force
# ──────────────────────────────────────────────────────
# Intuition  : Check every pair; collect matches in a set
#              to automatically avoid duplicates in result.
# Time       : O(n * m)
# Space      : O(min(n, m))
# ──────────────────────────────────────────────────────
def intersection_brute_force(nums1: List[int], nums2: List[int]) -> List[int]:
    result = set()
    for n1 in nums1:
        for n2 in nums2:
            if n1 == n2:
                result.add(n1)
    return list(result)


# ──────────────────────────────────────────────────────
# Approach 2 : Hash Set  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : Convert nums1 to a set for O(1) lookups.
#              Iterate nums2; if a value exists in set1,
#              add it to the result set (deduplicates automatically).
# Time       : O(n + m)
# Space      : O(min(n, m))
# ──────────────────────────────────────────────────────
def intersection_hashset(nums1: List[int], nums2: List[int]) -> List[int]:
    set1 = set(nums1)
    result = set()
    for num in nums2:
        if num in set1:
            result.add(num)
    return list(result)


# ──────────────────────────────────────────────────────
# Approach 3 : Set & Operator  (one-liner)
# ──────────────────────────────────────────────────────
# Intuition  : Python's & on two sets returns their
#              intersection — unique elements in both.
# Time       : O(n + m)
# Space      : O(n + m)
# ──────────────────────────────────────────────────────
def intersection_set_operator(nums1: List[int], nums2: List[int]) -> List[int]:
    return list(set(nums1) & set(nums2))


# ──────────────────────────────────────────────────────
# Approach 4 : set.intersection() Method
# ──────────────────────────────────────────────────────
# Intuition  : Built-in method; converts nums2 to a set
#              internally. Slightly different from & in that
#              it accepts any iterable (not just a set).
# Time       : O(n + m)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def intersection_set_method(nums1: List[int], nums2: List[int]) -> List[int]:
    return list(set(nums1).intersection(nums2))

'''
# ──────────────────────────────────────────────────────
# Approach 5 : Sorting + Two Pointers
# ──────────────────────────────────────────────────────
# Intuition  : Sort both arrays. Advance two pointers:
#              - match  → add to result (skip same value again)
#              - no match → advance the smaller pointer
# Time       : O(n log n + m log m)
# Space      : O(1)  — ignoring output
# ──────────────────────────────────────────────────────
def intersection_two_pointers(nums1: List[int], nums2: List[int]) -> List[int]:
    nums1.sort()
    nums2.sort()
    i, j = 0, 0
    result = []
    while i < len(nums1) and j < len(nums2):
        if nums1[i] == nums2[j]:
            if not result or result[-1] != nums1[i]:  # skip duplicates
                result.append(nums1[i])
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1
    return result


# ──────────────────────────────────────────────────────
# Approach 6 : Sorting + Binary Search
# ──────────────────────────────────────────────────────
# Intuition  : Sort nums1. For each unique element in nums2,
#              binary-search nums1. If found → intersection.
# Time       : O(n log n + m log n)
# Space      : O(n)  — sorted copy
# ──────────────────────────────────────────────────────
def intersection_binary_search(nums1: List[int], nums2: List[int]) -> List[int]:
    sorted1 = sorted(nums1)
    result = set()
    for num in set(nums2):                         # unique nums2 values only
        pos = bisect.bisect_left(sorted1, num)
        if pos < len(sorted1) and sorted1[pos] == num:
            result.add(num)
    return list(result)


# ──────────────────────────────────────────────────────
# Approach 7 : Filter + Set  (Functional Style)
# ──────────────────────────────────────────────────────
# Intuition  : filter() keeps elements of set(nums2) that
#              are also in set(nums1). No explicit loop.
# Time       : O(n + m)
# Space      : O(n + m)
# ──────────────────────────────────────────────────────
def intersection_filter(nums1: List[int], nums2: List[int]) -> List[int]:
    set1 = set(nums1)
    return list(filter(set1.__contains__, set(nums2)))


# ──────────────────────────────────────────────────────
# Approach 8 : List Comprehension + Set
# ──────────────────────────────────────────────────────
# Intuition  : Same idea as filter but expressed as a
#              set comprehension — more Pythonic and readable.
# Time       : O(n + m)
# Space      : O(n + m)
# ──────────────────────────────────────────────────────
def intersection_comprehension(nums1: List[int], nums2: List[int]) -> List[int]:
    set1 = set(nums1)
    return list({num for num in nums2 if num in set1})
'''

# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach              | Time        | Space       | Notes                         |
# |----|-----------------------|-------------|-------------|-------------------------------|
# | 1  | Brute Force           | O(n * m)    | O(min(n,m)) | Simple, slow                  |
# | 2  | Hash Set              | O(n + m)    | O(min(n,m)) | Best general case ★           |
# | 3  | Set & Operator        | O(n + m)    | O(n + m)    | Cleanest one-liner            |
# | 4  | set.intersection()    | O(n + m)    | O(n)        | Takes any iterable            |
# | 5  | Sort + Two Pointers   | O(n log n)  | O(1)        | Best when already sorted      |
# | 6  | Sort + Binary Search  | O(n log n)  | O(n)        | Good when one array is sorted |
# | 7  | Filter + Set          | O(n + m)    | O(n + m)    | Functional style              |
# | 8  | Set Comprehension     | O(n + m)    | O(n + m)    | Most readable Pythonic form   |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 2, 1],  [2, 2],           [2]),
        ([4, 9, 5],     [9, 4, 9, 8, 4],  [4, 9]),
        ([1, 2, 3],     [4, 5, 6],        []),
        ([1],           [1],              [1]),
        ([1, 1, 1],     [1, 1],           [1]),
        ([3, 1, 2],     [1, 1],           [1]),
        ([1, 2, 3],     [3, 2, 1],        [1, 2, 3]),
    ]

    solutions = [
        ("1. Brute Force",         intersection_brute_force),
        ("2. Hash Set",            intersection_hashset),
        ("3. Set & Operator",      intersection_set_operator),
        ("4. set.intersection()",  intersection_set_method),
     #  ("5. Sort + Two Ptrs",     intersection_two_pointers),
     #  ("6. Sort + Binary Search",intersection_binary_search),
     #  git add ("7. Filter + Set",        intersection_filter),
     #  ("8. Set Comprehension",   intersection_comprehension),
    ]

    for nums1, nums2, expected in test_cases:
        print(f"\nnums1={nums1}, nums2={nums2}  →  expected={sorted(expected)}")
        for name, fn in solutions:
            result = sorted(fn(nums1[:], nums2[:]))
            status = "PASS" if result == sorted(expected) else "FAIL"
            print(f"  {status}  {name:<28} → {result}")
