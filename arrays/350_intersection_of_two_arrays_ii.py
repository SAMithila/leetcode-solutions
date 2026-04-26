"""
========================================================
LeetCode 350 - Intersection of Two Arrays II
========================================================
Difficulty : Easy
Link       : https://leetcode.com/problems/intersection-of-two-arrays-ii/

Problem Statement
-----------------
Given two integer arrays nums1 and nums2, return an array of
their intersection. Each element in the result must appear as
many times as it shows in both arrays. You may return the
result in any order.

Examples
--------
Input : nums1 = [1, 2, 2, 1], nums2 = [2, 2]
Output: [2, 2]

Input : nums1 = [4, 9, 5], nums2 = [9, 4, 9, 8, 4]
Output: [4, 9]  (order does not matter)

Constraints
-----------
- 1 <= nums1.length, nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 1000

Follow-up questions (common in interviews)
------------------------------------------
Q1: What if arrays are already sorted?       → Use Two Pointers (Approach 2)
Q2: What if nums1 is much smaller?           → Hash Map on smaller array (Approach 3)
Q3: What if nums2 is too large to fit RAM?   → Stream nums2, keep hash map of nums1 in memory
========================================================
"""

from typing import List
from collections import Counter, defaultdict
import bisect


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force
# ──────────────────────────────────────────────────────
# Intuition  : For each element in nums1, scan nums2 linearly.
#              Mark used positions to avoid reusing elements.
# Time       : O(n * m)
# Space      : O(m)  — visited array
# ──────────────────────────────────────────────────────
def intersect_brute_force(nums1: List[int], nums2: List[int]) -> List[int]:
    visited = [False] * len(nums2)
    result = []
    for n1 in nums1:
        for j, n2 in enumerate(nums2):
            if not visited[j] and n1 == n2:
                result.append(n1)
                visited[j] = True
                break
    return result


# ──────────────────────────────────────────────────────
# Approach 2 : Sorting + Two Pointers
# ──────────────────────────────────────────────────────
# Intuition  : Sort both arrays. Use two pointers i, j:
#              - match  → record, advance both
#              - no match → advance the pointer with smaller value
# Time       : O(n log n + m log m)
# Space      : O(1)  — ignoring output; O(n+m) if sort is not in-place
# ──────────────────────────────────────────────────────
def intersect_two_pointers(nums1: List[int], nums2: List[int]) -> List[int]:
    nums1.sort()
    nums2.sort()
    i, j = 0, 0
    result = []
    while i < len(nums1) and j < len(nums2):
        if nums1[i] == nums2[j]:
            result.append(nums1[i])
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1
    return result


# ──────────────────────────────────────────────────────
# Approach 3 : Hash Map on Smaller Array  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : Count frequencies of the smaller array.
#              Iterate the larger; collect matches and
#              decrement the count to handle duplicates.
# Time       : O(n + m)
# Space      : O(min(n, m))
# ──────────────────────────────────────────────────────
def intersect_hashmap(nums1: List[int], nums2: List[int]) -> List[int]:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1        # always build map on smaller

    freq: dict[int, int] = {}
    for num in nums1:
        freq[num] = freq.get(num, 0) + 1

    result = []
    for num in nums2:
        if freq.get(num, 0) > 0:
            result.append(num)
            freq[num] -= 1
    return result


# ──────────────────────────────────────────────────────
# Approach 4 : Counter & Operator  (Pythonic one-liner)
# ──────────────────────────────────────────────────────
# Intuition  : Counter & keeps the minimum count for each
#              shared key — exactly the intersection with
#              duplicate counts. elements() expands it back.
# Time       : O(n + m)
# Space      : O(min(n, m))
# ──────────────────────────────────────────────────────
def intersect_counter(nums1: List[int], nums2: List[int]) -> List[int]:
    return list((Counter(nums1) & Counter(nums2)).elements())


# ──────────────────────────────────────────────────────
# Approach 5 : defaultdict
# ──────────────────────────────────────────────────────
# Intuition  : Same logic as Approach 3 but uses
#              defaultdict(int) to avoid .get() fallbacks.
# Time       : O(n + m)
# Space      : O(min(n, m))
# ──────────────────────────────────────────────────────
def intersect_defaultdict(nums1: List[int], nums2: List[int]) -> List[int]:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    freq: defaultdict[int, int] = defaultdict(int)
    for num in nums1:
        freq[num] += 1

    result = []
    for num in nums2:
        if freq[num] > 0:
            result.append(num)
            freq[num] -= 1
    return result


# ──────────────────────────────────────────────────────
# Approach 6 : Sorting + Binary Search
# ──────────────────────────────────────────────────────
# Intuition  : Sort nums1. For each element in nums2,
#              binary-search nums1 to find and "consume"
#              a match (overwrite with sentinel to mark used).
# Note       : Useful when one array is pre-sorted.
# Time       : O(n log n + m log n)
# Space      : O(n)  — sorted copy
# ──────────────────────────────────────────────────────
def intersect_binary_search(nums1: List[int], nums2: List[int]) -> List[int]:
    sorted1 = sorted(nums1)
    result = []
    for num in nums2:
        pos = bisect.bisect_left(sorted1, num)
        if pos < len(sorted1) and sorted1[pos] == num:
            result.append(num)
            sorted1.pop(pos)           # consume the match
    return result


# ──────────────────────────────────────────────────────
# Approach 7 : Bucket / Array Index (value-range known)
# ──────────────────────────────────────────────────────
# Intuition  : Since values are bounded 0–1000, use a
#              fixed-size count array instead of a hash map.
#              Index directly by value — no hashing overhead.
# Time       : O(n + m + V)  where V = value range (1001)
# Space      : O(V)  — constant 1001 integers
# ──────────────────────────────────────────────────────
def intersect_bucket(nums1: List[int], nums2: List[int]) -> List[int]:
    MAX_VAL = 1001
    freq = [0] * MAX_VAL
    for num in nums1:
        freq[num] += 1

    result = []
    for num in nums2:
        if freq[num] > 0:
            result.append(num)
            freq[num] -= 1
    return result


# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach              | Time          | Space        | Notes                          |
# |----|-----------------------|---------------|--------------|--------------------------------|
# | 1  | Brute Force           | O(n * m)      | O(m)         | Simple, slow                   |
# | 2  | Sort + Two Pointers   | O(n log n)    | O(1)         | Best when input already sorted |
# | 3  | Hash Map (smaller)    | O(n + m)      | O(min(n,m))  | Best general case ★            |
# | 4  | Counter &             | O(n + m)      | O(min(n,m))  | Cleanest Pythonic one-liner    |
# | 5  | defaultdict           | O(n + m)      | O(min(n,m))  | Cleaner hash map variant       |
# | 6  | Sort + Binary Search  | O(n log n)    | O(n)         | Good when one array is sorted  |
# | 7  | Bucket Array          | O(n + m + V)  | O(V)         | Fastest when value range small |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 2, 1],  [2, 2],          [2, 2]),
        ([4, 9, 5],     [9, 4, 9, 8, 4], [4, 9]),
        ([1],           [1],             [1]),
        ([1, 2],        [3, 4],          []),
        ([1, 1, 1],     [1, 1],          [1, 1]),
        ([3, 1, 2],     [1, 1],          [1]),
    ]

    solutions = [
        ("1. Brute Force",         intersect_brute_force),
        ("2. Sort + Two Ptrs",     intersect_two_pointers),
        ("3. Hash Map (smaller)",  intersect_hashmap),
        ("4. Counter &",           intersect_counter),
        ("5. defaultdict",         intersect_defaultdict),
        ("6. Sort + Bisect",       intersect_binary_search),
        ("7. Bucket Array",        intersect_bucket),
    ]

    for nums1, nums2, expected in test_cases:
        print(f"\nnums1={nums1}, nums2={nums2}  →  expected={sorted(expected)}")
        for name, fn in solutions:
            result = sorted(fn(nums1[:], nums2[:]))
            status = "PASS" if result == sorted(expected) else "FAIL"
            print(f"  {status}  {name:<26} → {result}")
