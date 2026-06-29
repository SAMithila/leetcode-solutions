"""
========================================================
LeetCode 347 - Top K Frequent Elements
========================================================
Difficulty : Medium
Link       : https://leetcode.com/problems/top-k-frequent-elements/

Problem Statement
-----------------
Given an integer array nums and an integer k, return the k
most frequent elements. You may return the answer in any order.

Follow-up: Your algorithm must be better than O(n log n),
where n is the array's size.

Examples
--------
Input : nums = [1, 1, 1, 2, 2, 3], k = 2
Output: [1, 2]

Input : nums = [1], k = 1
Output: [1]

Constraints
-----------
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in [1, number of unique elements]
- The answer is guaranteed to be unique
========================================================
"""

from typing import List
from collections import Counter
import heapq
import random


# ──────────────────────────────────────────────────────
# Approach 1 : Sort by Frequency
# ──────────────────────────────────────────────────────
# Intuition  : Count frequencies with Counter, sort all
#              unique elements by frequency descending,
#              return the first k.
# Time       : O(n log n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def topKFrequent_sort(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    return sorted(freq, key=lambda x: -freq[x])[:k]


# ──────────────────────────────────────────────────────
# Approach 2 : Counter.most_common()  (Pythonic)
# ──────────────────────────────────────────────────────
# Intuition  : Python's built-in uses a heap internally;
#              most_common(k) returns the k highest-count
#              (element, count) pairs.
# Time       : O(n log k)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def topKFrequent_most_common(nums: List[int], k: int) -> List[int]:
    return [num for num, _ in Counter(nums).most_common(k)]


# ──────────────────────────────────────────────────────
# Approach 3 : Min Heap of size k
# ──────────────────────────────────────────────────────
# Intuition  : Maintain a min-heap of size k keyed by frequency.
#              For each unique element, push (freq, num).
#              If heap grows beyond k, pop the minimum.
#              The heap retains the k largest frequencies.
# Time       : O(n log k)
# Space      : O(n + k)
# ──────────────────────────────────────────────────────
def topKFrequent_min_heap(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    heap: List[tuple] = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)          # remove least frequent
    return [num for _, num in heap]

'''
# ──────────────────────────────────────────────────────
# Approach 4 : Max Heap
# ──────────────────────────────────────────────────────
# Intuition  : Push all (-freq, num) pairs into a max-heap
#              (negate so Python's min-heap acts as max-heap).
#              Pop k times to get the k most frequent.
# Time       : O(n log n)   — heapify all unique elements
# Space      : O(n)
# ──────────────────────────────────────────────────────
def topKFrequent_max_heap(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    max_heap = [(-count, num) for num, count in freq.items()]
    heapq.heapify(max_heap)
    return [heapq.heappop(max_heap)[1] for _ in range(k)]
'''

# ──────────────────────────────────────────────────────
# Approach 5 : Bucket Sort  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : A number can appear at most n times.
#              Create n+1 buckets indexed by frequency.
#              Place each number in its frequency bucket.
#              Scan buckets from high to low, collecting
#              elements until we have k.
# Time       : O(n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def topKFrequent_bucket_sort(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]

    for num, count in freq.items():
        buckets[count].append(num)

    result = []
    for i in range(len(buckets) - 1, 0, -1):   # high freq → low freq
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result

'''
# ──────────────────────────────────────────────────────
# Approach 6 : Quick Select (partial sort)
# ──────────────────────────────────────────────────────
# Intuition  : Build a list of unique elements sorted by
#              their frequency. Use quickselect to find the
#              k-th largest without fully sorting.
#              On average, this partitions the correct k
#              elements to the right side.
# Time       : O(n) average, O(n²) worst case
# Space      : O(n)
# ──────────────────────────────────────────────────────
def topKFrequent_quick_select(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    unique = list(freq.keys())
    n = len(unique)

    def partition(left: int, right: int, pivot_idx: int) -> int:
        pivot_freq = freq[unique[pivot_idx]]
        unique[pivot_idx], unique[right] = unique[right], unique[pivot_idx]
        store = left
        for i in range(left, right):
            if freq[unique[i]] < pivot_freq:
                unique[store], unique[i] = unique[i], unique[store]
                store += 1
        unique[store], unique[right] = unique[right], unique[store]
        return store

    left, right = 0, n - 1
    target = n - k                     # k largest → target index from left

    while left <= right:
        pivot_idx = random.randint(left, right)
        pivot_final = partition(left, right, pivot_idx)
        if pivot_final == target:
            return unique[target:]
        elif pivot_final < target:
            left = pivot_final + 1
        else:
            right = pivot_final - 1

    return unique[target:]
'''

# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach            | Time       | Space | Notes                          |
# |----|---------------------|------------|-------|--------------------------------|
# | 1  | Sort by Frequency   | O(n log n) | O(n)  | Simple, readable               |
# | 2  | most_common()       | O(n log k) | O(n)  | Most Pythonic one-liner        |
# | 3  | Min Heap (size k)   | O(n log k) | O(n)  | Best heap approach             |
# | 4  | Max Heap            | O(n log n) | O(n)  | Simpler heap logic             |
# | 5  | Bucket Sort         | O(n)       | O(n)  | Optimal — meets follow-up ★    |
# | 6  | Quick Select        | O(n) avg   | O(n)  | O(n) avg but complex to write  |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([1, 1, 1, 2, 2, 3],       2, {1, 2}),
        ([1],                       1, {1}),
        ([1, 2],                    2, {1, 2}),
        ([4, 1, -1, 2, -1, 2, 3],  2, {-1, 2}),
        ([5, 5, 5, 3, 3, 1],       2, {5, 3}),
        ([1, 1, 2, 2, 3],          2, {1, 2}),
    ]

    solutions = [
        ("1. Sort by Frequency",  topKFrequent_sort),
        ("2. most_common()",      topKFrequent_most_common),
        ("3. Min Heap (size k)",  topKFrequent_min_heap),
     #  ("4. Max Heap",           topKFrequent_max_heap),
        ("5. Bucket Sort",        topKFrequent_bucket_sort),
     #  ("6. Quick Select",       topKFrequent_quick_select),
    ]

    for nums, k, expected in test_cases:
        print(f"\nnums={nums}, k={k}  →  expected={expected}")
        for name, fn in solutions:
            result = set(fn(nums[:], k))
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}  {name:<24} → {sorted(result)}")
