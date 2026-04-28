"""
========================================================
LeetCode 128 - Longest Consecutive Sequence
========================================================
Difficulty : Medium
Link       : https://leetcode.com/problems/longest-consecutive-sequence/

Problem Statement
-----------------
Given an unsorted array of integers nums, return the length
of the longest consecutive elements sequence.
You must write an algorithm that runs in O(n) time.

Examples
--------
Input : nums = [100, 4, 200, 1, 3, 2]
Output: 4  →  sequence: [1, 2, 3, 4]

Input : nums = [0, 3, 7, 2, 5, 8, 1, 6, 0, 4]
Output: 9  →  sequence: [0, 1, 2, 3, 4, 5, 6, 7, 8]

Input : nums = []
Output: 0

Constraints
-----------
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
========================================================
"""

from typing import List


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force
# ──────────────────────────────────────────────────────
# Intuition  : For each number, keep looking for num+1,
#              num+2, ... in the array (using a set for
#              O(1) lookup). No early-start optimisation.
# Time       : O(n²)  — every number starts a search
# Space      : O(n)   — set
# ──────────────────────────────────────────────────────
def longestConsecutive_brute_force(nums: List[int]) -> int:
    if not nums:
        return 0
    num_set = set(nums)
    best = 0
    for num in num_set:
        length = 1
        while num + length in num_set:
            length += 1
        best = max(best, length)
    return best


# ──────────────────────────────────────────────────────
# Approach 2 : Sorting
# ──────────────────────────────────────────────────────
# Intuition  : Sort the array. Scan linearly: if the next
#              element is exactly current + 1, extend the
#              streak; if it's equal, skip (duplicate);
#              otherwise reset.
# Time       : O(n log n)
# Space      : O(1)  — ignoring sort stack
# ──────────────────────────────────────────────────────
def longestConsecutive_sorting(nums: List[int]) -> int:
    if not nums:
        return 0
    nums.sort()
    best = 1
    streak = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            continue                        # skip duplicates
        if nums[i] == nums[i - 1] + 1:
            streak += 1
            best = max(best, streak)
        else:
            streak = 1
    return best


# ──────────────────────────────────────────────────────
# Approach 3 : Hash Set  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : Convert nums to a set. Only start counting
#              from a number if num-1 is NOT in the set
#              (i.e. it is the true start of a sequence).
#              This ensures each number is visited at most
#              twice → O(n) total.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def longestConsecutive_hashset(nums: List[int]) -> int:
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 not in num_set:          # sequence start
            length = 1
            while num + length in num_set:
                length += 1
            best = max(best, length)
    return best

'''
# ──────────────────────────────────────────────────────
# Approach 4 : Hash Map — Merge Boundaries
# ──────────────────────────────────────────────────────
# Intuition  : For each number, look up the length of any
#              existing sequence immediately to the left
#              (ending at num-1) and to the right (starting
#              at num+1). Merge them into one sequence and
#              update the boundary endpoints in the map.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def longestConsecutive_hashmap(nums: List[int]) -> int:
    length_map: dict[int, int] = {}   # num → streak length at that boundary
    best = 0

    for num in nums:
        if num in length_map:
            continue                        # skip duplicates

        left  = length_map.get(num - 1, 0)
        right = length_map.get(num + 1, 0)
        total = left + right + 1

        length_map[num]          = total
        length_map[num - left]   = total   # update left boundary
        length_map[num + right]  = total   # update right boundary

        best = max(best, total)

    return best


# ──────────────────────────────────────────────────────
# Approach 5 : Union Find (Disjoint Set Union)
# ──────────────────────────────────────────────────────
# Intuition  : Each number is a node. Union num with num+1
#              if both exist. The size of the largest
#              connected component is the answer.
# Time       : O(n · α(n))  ≈ O(n)  (α = inverse Ackermann)
# Space      : O(n)
# ──────────────────────────────────────────────────────
class UnionFind:
    def __init__(self):
        self.parent: dict[int, int] = {}
        self.size:   dict[int, int] = {}

    def add(self, x: int) -> None:
        self.parent[x] = x
        self.size[x]   = 1

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]

    def max_size(self) -> int:
        return max(self.size.values()) if self.size else 0


def longestConsecutive_union_find(nums: List[int]) -> int:
    if not nums:
        return 0
    uf = UnionFind()
    seen = set()
    for num in nums:
        if num in seen:
            continue
        seen.add(num)
        uf.add(num)
        if num - 1 in seen:
            uf.union(num, num - 1)
        if num + 1 in seen:
            uf.union(num, num + 1)
    return uf.max_size()

'''
# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach          | Time       | Space | Notes                          |
# |----|-------------------|------------|-------|--------------------------------|
# | 1  | Brute Force       | O(n²)      | O(n)  | No start optimisation          |
# | 2  | Sorting           | O(n log n) | O(1)  | Simple; violates O(n) req.     |
# | 3  | Hash Set          | O(n)       | O(n)  | Start-only trick — best ★      |
# | 4  | Hash Map (merge)  | O(n)       | O(n)  | Merge-boundaries variant       |
# | 5  | Union Find        | O(n·α(n))  | O(n)  | Graph approach ≈ O(n)          |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([100, 4, 200, 1, 3, 2],           4),
        ([0, 3, 7, 2, 5, 8, 1, 6, 0, 4],  9),
        ([],                               0),
        ([1],                              1),
        ([1, 2, 0, 1],                     3),
        ([-1, 0, 1, 2, -2],               5),
        ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6], 7),
    ]

    solutions = [
        ("1. Brute Force",      longestConsecutive_brute_force),
        ("2. Sorting",          longestConsecutive_sorting),
        ("3. Hash Set",         longestConsecutive_hashset),
     #  ("4. Hash Map (merge)", longestConsecutive_hashmap),
     #  ("5. Union Find",       longestConsecutive_union_find),
    ]

    for nums, expected in test_cases:
        print(f"\nnums={nums}  →  expected={expected}")
        for name, fn in solutions:
            result = fn(nums[:])
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}  {name:<22} → {result}")
