"""
========================================================
LeetCode 215 - Kth Largest Element in an Array
========================================================
Difficulty : Medium
Link       : https://leetcode.com/problems/kth-largest-element-in-an-array/

Problem Statement
-----------------
Given an integer array nums and an integer k, return the kth
largest element in the array.

Note that it is the kth largest element in the sorted order,
not the kth distinct element.

Can you solve it without sorting in O(n) time?

Examples
--------
Input : nums = [3, 2, 1, 5, 6, 4], k = 2
Output: 5

Input : nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
Output: 4

Constraints
-----------
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
========================================================
"""

from typing import List
import heapq
import random

# ──────────────────────────────────────────────────────
# Approach 1 : Sorting
# ──────────────────────────────────────────────────────
# Intuition  : Sort the array in descending order and return
#              the element at index k-1.
# Time       : O(n log n)
# Space      : O(n) (Python's Timsort uses O(n) space)
# ──────────────────────────────────────────────────────
def findKthLargest_sort(nums: List[int], k: int) -> int:
    return sorted(nums, reverse=True)[k - 1]


# ──────────────────────────────────────────────────────
# Approach 2 : Min Heap (Size k)
# ──────────────────────────────────────────────────────
# Intuition  : Maintain a min-heap of size k. For each number,
#              push to the heap. If heap size exceeds k, pop.
#              The top of the heap is the kth largest.
#              Optimization: heapify first k elements, then
#              use heappushpop for the rest.
# Time       : O(n log k)
# Space      : O(k)
# ──────────────────────────────────────────────────────
def findKthLargest_min_heap(nums: List[int], k: int) -> int:
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heappushpop(heap, num)
    return heap[0]


# ──────────────────────────────────────────────────────
# Approach 3 : Max Heap (Heapify + Pop)
# ──────────────────────────────────────────────────────
# Intuition  : Negate numbers to simulate a max-heap in Python's
#              min-heap implementation. Heapify all elements,
#              then pop k times.
# Time       : O(n + k log n)
# Space      : O(n)
# ──────────────────────────────────────────────────────
def findKthLargest_max_heap(nums: List[int], k: int) -> int:
    max_heap = [-num for num in nums]
    heapq.heapify(max_heap)
    for _ in range(k - 1):
        heapq.heappop(max_heap)
    return -heapq.heappop(max_heap)

'''
# ──────────────────────────────────────────────────────
# Approach 4 : Pythonic nlargest
# ──────────────────────────────────────────────────────
# Intuition  : Use python's built-in heapq.nlargest to find
#              the top k largest and return the last element.
# Time       : O(n log k)
# Space      : O(k)
# ──────────────────────────────────────────────────────
def findKthLargest_pythonic(nums: List[int], k: int) -> int:
    return heapq.nlargest(k, nums)[-1]
'''

# ──────────────────────────────────────────────────────
# Approach 5 : Quickselect (Dutch National Flag, Iterative)
# ──────────────────────────────────────────────────────
# Intuition  : Randomized Quickselect using 3-way partition
#              to handle duplicates efficiently and avoid
#              O(n^2) worst case. Iterative approach avoids
#              recursion overhead and call-stack limits.
# Time       : O(n) average, O(n^2) worst case
# Space      : O(1) auxiliary
# ──────────────────────────────────────────────────────
def findKthLargest_quickselect(nums: List[int], k: int) -> int:
    # Target index in 0-indexed sorted ascending array is len(nums) - k
    target = len(nums) - k
    left, right = 0, len(nums) - 1
    
    while left <= right:
        if left == right:
            return nums[left]
            
        # Choose a random pivot index
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]
        
        # Dutch National Flag (3-way) Partition
        lt = left
        i = left
        gt = right
        while i <= gt:
            if nums[i] < pivot:
                nums[lt], nums[i] = nums[i], nums[lt]
                lt += 1
                i += 1
            elif nums[i] > pivot:
                nums[i], nums[gt] = nums[gt], nums[i]
                gt -= 1
            else:
                i += 1
                
        # Partition ranges:
        # nums[left...lt-1] < pivot
        # nums[lt...gt] == pivot
        # nums[gt+1...right] > pivot
        if target < lt:
            right = lt - 1
        elif target <= gt:
            return pivot
        else:
            left = gt + 1
            
    return -1


# ──────────────────────────────────────────────────────
# Approach 6 : Median of Medians (Deterministic Quickselect)
# ──────────────────────────────────────────────────────
# Intuition  : The BFPRT algorithm selects a pivot deterministically
#              by taking the median of medians of groups of 5.
#              This guarantees O(n) worst-case time complexity.
# Time       : O(n) worst case
# Space      : O(n) recursion stack & intermediate lists
# ──────────────────────────────────────────────────────
def findKthLargest_median_of_medians(nums: List[int], k: int) -> int:
    target = len(nums) - k
    
    def select(arr: List[int], left: int, right: int, t: int) -> int:
        if left == right:
            return arr[left]
            
        pivot = get_pivot(arr, left, right)
        lt, gt = partition_3way(arr, left, right, pivot)
        
        if t < lt:
            return select(arr, left, lt - 1, t)
        elif t <= gt:
            return pivot
        else:
            return select(arr, gt + 1, right, t)

    def get_pivot(arr: List[int], left: int, right: int) -> int:
        n = right - left + 1
        if n < 5:
            return sorted(arr[left:right+1])[n // 2]
            
        medians = []
        for i in range(left, right + 1, 5):
            sub_right = min(i + 4, right)
            sub_n = sub_right - i + 1
            medians.append(sorted(arr[i:sub_right+1])[sub_n // 2])
            
        return select(medians, 0, len(medians) - 1, len(medians) // 2)

    def partition_3way(arr: List[int], left: int, right: int, pivot: int) -> tuple:
        lt = left
        i = left
        gt = right
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        return lt, gt

    # Work on a copy to preserve original input
    return select(list(nums), 0, len(nums) - 1, target)


# ──────────────────────────────────────────────────────
# Approach 7 : Counting Sort (Dynamic Range)
# ──────────────────────────────────────────────────────
# Intuition  : Since range constraints are reasonably small,
#              we count frequencies of all numbers. Then traverse
#              from max value down to min value to find the kth element.
# Time       : O(n + R) where R = max - min
# Space      : O(R)
# ──────────────────────────────────────────────────────
def findKthLargest_counting_sort(nums: List[int], k: int) -> int:
    min_val, max_val = min(nums), max(nums)
    range_len = max_val - min_val + 1
    
    # Optimize: If range is too large to make memory-safe, fallback to heap.
    # On Leetcode, constraints limit elements to [-10^4, 10^4], range_len <= 20001.
    if range_len > 10**6:
        return findKthLargest_min_heap(nums, k)
        
    count = [0] * range_len
    for num in nums:
        count[num - min_val] += 1
        
    for val in range(range_len - 1, -1, -1):
        k -= count[val]
        if k <= 0:
            return val + min_val
            
    return -1


# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach            | Time       | Space | Notes                          |
# |----|---------------------|------------|-------|--------------------------------|
# | 1  | Sorting             | O(n log n) | O(n)  | Simple baseline                |
# | 2  | Min Heap (size k)   | O(n log k) | O(k)  | Best general heap approach     |
# | 3  | Max Heap            | O(n+k logn)| O(n)  | Simpler heap logic, more space |
# | 4  | Pythonic nlargest   | O(n log k) | O(k)  | Built-in standard library      |
# | 5  | Quickselect         | O(n) avg   | O(1)  | In-place, DNF handles dups ★   |
# | 6  | Median of Medians   | O(n) det   | O(n)  | O(n) worst-case guaranteed     |
# | 7  | Counting Sort       | O(n + R)   | O(R)  | Optimal if value range R small |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        # nums, k, expected
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([-1, -2, -3, -4, -5], 2, -2),
        ([3, 3, 3, 3, 3], 3, 3),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1, 10),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10, 1),
    ]

    solutions = [
        ("1. Sorting", findKthLargest_sort),
        ("2. Min Heap (size k)", findKthLargest_min_heap),
        ("3. Max Heap", findKthLargest_max_heap),
    #    ("4. Pythonic nlargest", findKthLargest_pythonic),
        ("5. Quickselect", findKthLargest_quickselect),
        ("6. Median of Medians", findKthLargest_median_of_medians),
        ("7. Counting Sort", findKthLargest_counting_sort),
    ]

    for nums, k, expected in test_cases:
        print(f"\nnums={nums}, k={k}  →  expected={expected}")
        for name, fn in solutions:
            # We copy nums using [:] because Quickselect modifies in-place
            result = fn(nums[:], k)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}  {name:<24} → {result}")
