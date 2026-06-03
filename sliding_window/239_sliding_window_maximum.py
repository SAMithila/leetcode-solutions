"""
LeetCode 239 - Sliding Window Maximum
You are given an array of integers nums, there is a sliding window of size k 
which is moving from the very left of the array to the very right. You can 
only see the k numbers in the window. Each time the sliding window moves 
right by one position.

Return the max sliding window.

Example 1:
  Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
  Output: [3,3,5,5,6,7]
  Explanation:
    Window position                Max
    ---------------               ----
    [1  3  -1] -3  5  3  6  7       3
     1 [3  -1  -3] 5  3  6  7       3
     1  3 [-1  -3  5] 3  6  7       5
     1  3  -1 [-3  5  3] 6  7       5
     1  3  -1  -3 [5  3  6] 7       6
     1  3  -1  -3  5 [3  6  7]      7

Example 2:
  Input: nums = [1], k = 1
  Output: [1]

KEY INSIGHTS:
  - Brute force requires O(N * k) time which is too slow for large inputs (e.g., N = 10^5).
  - To optimize, we can use:
    1. A Heap (Priority Queue) with lazy deletion of out-of-bounds elements (O(N log N)).
    2. A Monotonic Deque to maintain the indices of candidate maximums in decreasing order of values (O(N) time, O(k) space).
    3. A Dynamic Programming approach using Prefix & Suffix maximums on blocks of size k (O(N) time, O(N) space).
"""

from collections import deque
import heapq

# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(N * k)
# Space: O(1) (excluding output array)
# ─────────────────────────────────────────────
def maxSlidingWindow_brute(nums: list[int], k: int) -> list[int]:
    if not nums or k == 0:
        return []
    
    n = len(nums)
    res = []
    for i in range(n - k + 1):
        res.append(max(nums[i:i + k]))
    return res

'''
# ─────────────────────────────────────────────
# Approach 2: Max-Heap (Priority Queue) with Lazy Deletion
# Time:  O(N log N) — in the worst case, heap size grows up to N
# Space: O(N) — to store elements in the heap
# ─────────────────────────────────────────────
def maxSlidingWindow_heap(nums: list[int], k: int) -> list[int]:
    if not nums or k == 0:
        return []
    
    # Python heapq is a min-heap by default, so we store negative values to simulate a max-heap.
    # We store tuples of (-value, index) so we can easily check if the top element is in the current window.
    heap = [(-nums[i], i) for i in range(k)]
    heapq.heapify(heap)
    
    res = [-heap[0][0]]
    
    for i in range(k, len(nums)):
        heapq.heappush(heap, (-nums[i], i))
        # Lazily remove elements from the top of the heap that are no longer in the sliding window
        while heap[0][1] <= i - k:
            heapq.heappop(heap)
        res.append(-heap[0][0])
        
    return res
'''

# ─────────────────────────────────────────────
# Approach 3: Monotonic Deque (Optimal)
# Time:  O(N) — each index is pushed and popped from the deque at most once
# Space: O(k) — deque size is capped at window size k
# ─────────────────────────────────────────────
def maxSlidingWindow_deque(nums: list[int], k: int) -> list[int]:
    if not nums or k == 0:
        return []
    
    q = deque()  # stores indices of elements in the current window
    res = []
    
    for i in range(len(nums)):
        # 1. Remove indices that are out of the current window boundary
        if q and q[0] < i - k + 1:
            q.popleft()
            
        # 2. Maintain monotonic property: remove elements from the back of the deque
        #    that are less than or equal to the current element nums[i].
        #    These elements can never be the maximum in the current or future windows.
        while q and nums[q[-1]] <= nums[i]:
            q.pop()
            
        # 3. Add the current element's index
        q.append(i)
        
        # 4. Once we have a full window of size k, the front of the deque is the maximum
        if i >= k - 1:
            res.append(nums[q[0]])
            
    return res

'''
# ─────────────────────────────────────────────
# Approach 4: Dynamic Programming (Prefix / Suffix Max)
# Time:  O(N)
# Space: O(N)
# ─────────────────────────────────────────────
def maxSlidingWindow_dp(nums: list[int], k: int) -> list[int]:
    if not nums or k == 0:
        return []
    
    n = len(nums)
    left = [0] * n
    right = [0] * n
    
    # Fill left array: prefix max within blocks of size k
    for i in range(n):
        if i % k == 0:
            left[i] = nums[i]
        else:
            left[i] = max(left[i - 1], nums[i])
            
    # Fill right array: suffix max within blocks of size k
    for i in range(n - 1, -1, -1):
        if i == n - 1 or (i + 1) % k == 0:
            right[i] = nums[i]
        else:
            right[i] = max(right[i + 1], nums[i])
            
    # For any window [i, i + k - 1], the max is the max of the suffix of the block containing i,
    # and the prefix of the block containing i + k - 1.
    res = []
    for i in range(n - k + 1):
        res.append(max(right[i], left[i + k - 1]))
        
    return res
'''

# ─────────────────────────────────────────────
# Default optimal solution
# ─────────────────────────────────────────────
maxSlidingWindow = maxSlidingWindow_deque


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1], 1, [1]),
        ([1, -1], 1, [1, -1]),
        ([9, 11], 2, [11]),
        ([4, -2], 2, [4]),
        ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),
        ([7, 2, 4, 1, 6, 5, 1, 2, 3], 4, [7, 6, 6, 6, 6, 5]),
    ]

    solvers = [
        ("Brute Force ", maxSlidingWindow_brute),
     #   ("Heap (PQ)   ", maxSlidingWindow_heap),
        ("Monotonic Q ", maxSlidingWindow_deque),
     #  ("Dynamic Prog", maxSlidingWindow_dp),
    ]

    for nums, k, expected in tests:
        print(f"Testing input: nums={nums}, k={k}")
        for name, fn in solvers:
            out = fn(nums, k)
            status = "PASS" if out == expected else "FAIL"
            print(f"  [{status}] {name} | got={out} expected={expected}")
        print()
