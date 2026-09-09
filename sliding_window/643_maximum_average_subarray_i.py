"""
LeetCode 643 - Maximum Average Subarray I

You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10^-5 will be accepted.

Example 1:
  Input: nums = [1,12,-5,-6,50,3], k = 4
  Output: 12.75000
  Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75

Example 2:
  Input: nums = [5], k = 1
  Output: 5.00000
"""
"""
## LC 643 — Maximum Average Subarray I (Interview Format)

---

### Step 1 — Understand & Restate

> "We are given an array of integers `nums` and an integer `k`. We need to find a contiguous subarray of size `k` that has the maximum average. Since the length `k` is fixed, maximizing the average of `k` elements is mathematically equivalent to maximizing the sum of those `k` elements. So we should find the maximum sum of any contiguous subarray of size `k` and divide it by `k` at the end."

```
nums = [1, 12, -5, -6, 50, 3], k = 4

Subarrays of size 4:
[1, 12, -5, -6] → sum = 2,  avg = 0.5
[12, -5, -6, 50] → sum = 51, avg = 12.75  ← max
[-5, -6, 50, 3]  → sum = 42, avg = 10.5

Answer: 12.75
```

---

### Step 2 — Clarifying Questions

```
Q: Can nums contain negative numbers?    → Yes, as seen in Example 1.
Q: Is it guaranteed that k <= len(nums)? → Yes, standard constraint.
Q: How large can len(nums) and k be?     → Up to 10^5.
Q: Can k be equal to 1?                  → Yes, standard constraint.
```

---

### Step 3 — Brute Force → Optimal

**Brute Force — O(n * k) time, O(1) space:**
> "Compute the sum of every possible subarray of size `k` from scratch. There are `n - k + 1` such subarrays, and computing each sum takes `O(k)` time. This is too slow for large inputs."

**Optimal — Sliding Window — O(n) time, O(1) space:**
> "Instead of recalculating the sum of `k` elements from scratch each time, we can maintain a running sum of the window. When we slide the window one step to the right:
> 1. Add the new element entering the window from the right.
> 2. Subtract the old element leaving the window from the left.
> 3. Update the maximum sum observed.
> This way, each slide takes O(1) time, yielding O(n) overall time."

---

### Step 4 — Edge Cases

```
1. k == len(nums): Only one window exists (the whole array).
2. k == 1: The maximum average is simply the maximum single element in the array.
3. All negative numbers: The sum will be negative, so we must initialize our max_sum appropriately (e.g., negative infinity or the first window sum).
```

---

### Step 5 — Code (Optimal Sliding Window)

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        # Step 1: Calculate the sum of the first window
        curr_sum = sum(nums[:k])
        max_sum = curr_sum
        
        # Step 2: Slide the window from index k to n - 1
        for i in range(k, len(nums)):
            curr_sum += nums[i] - nums[i - k]
            if curr_sum > max_sum:
                max_sum = curr_sum
                
        # Step 3: Return the maximum average
        return max_sum / k
```

---

### Step 6 — Dry Run

```
nums = [1, 12, -5, -6, 50, 3], k = 4
curr_sum = 1 + 12 + (-5) + (-6) = 2
max_sum = 2

i = 4 (value 50):
  curr_sum = curr_sum + nums[4] - nums[0]
           = 2 + 50 - 1 = 51
  51 > 2 → max_sum = 51

i = 5 (value 3):
  curr_sum = curr_sum + nums[5] - nums[1]
           = 51 + 3 - 12 = 42
  42 is not > 51 → max_sum remains 51

End of loop.
Return max_sum / k = 51 / 4 = 12.75 (Correct!)
```

---

### Step 7 — Why This Works

> "Calculating the sum of any adjacent window of size `k` shares `k - 1` elements with the previous window. 
By utilizing subtraction and addition, we avoid redundant calculations, achieving O(1) updates per slide. 
Because the division by `k` is a linear scaling, we can defer it until the very end, preventing division rounding issues during comparisons."

---

### Step 8 — Complexity Analysis

**Time — O(n)**
```
Initial sum takes O(k).
The loop runs (n - k) times, each iteration doing O(1) operations.
Total time complexity is O(k + (n - k)) = O(n).
```

**Space — O(1)**
```
Only a few scalar variables (curr_sum, max_sum) are kept in memory.
```

---

### Step 9 — Follow-up Questions & Answers

**Q: What if the subarray length was not fixed, but could be at least k?**
> "This refers to LeetCode 862 (Shortest Subarray with Sum at Least K) or similar problems, which require prefix sums, sliding window with queues/deques, or binary search, and have different complexity properties."

---

### Recap Card

```
Problem type:   Sliding Window (Fixed Size)
Pattern:        Compute initial window sum, then slide with O(1) updates
Key trick:      Defer division by k until the final step

Time:    O(n)
Space:   O(1)

Edge cases:
  → k == len(nums)      → single calculation
  → k == 1              → simple max search
  → all negative numbers → initialize max_sum with the first window, not 0
```
"""

from typing import List


# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(n * k)
# Space: O(1)
# ─────────────────────────────────────────────
def findMaxAverage_bruteforce(nums: List[int], k: int) -> float:
    max_avg = float("-inf")
    for i in range(len(nums) - k + 1):
        curr_sum = 0
        for j in range(i, i + k):
            curr_sum += nums[j]
        max_avg = max(max_avg, curr_sum / k)
    return max_avg


# ─────────────────────────────────────────────
# Approach 2: Sliding Window (Optimal)
# Time:  O(n)
# Space: O(1)
# ─────────────────────────────────────────────
def findMaxAverage_sliding_window(nums: List[int], k: int) -> float:
    # Compute initial window sum
    curr_sum = sum(nums[:k])
    max_sum = curr_sum

    # Slide the window
    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        if curr_sum > max_sum:
            max_sum = curr_sum

    return max_sum / k


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2
# O(n) time | O(1) space
# ─────────────────────────────────────────────
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        return findMaxAverage_sliding_window(nums, k)


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([1, 12, -5, -6, 50, 3], 4, 12.75),
        ([5], 1, 5.0),
        ([-1], 1, -1.0),
        ([4, 0, 4, 3, 3], 5, 2.8),
        ([0, 1, 1, 3, 3], 4, 2.0),
        ([-1, -2, -3, -4], 2, -1.5),
    ]

    solvers = [
        ("Brute Force", findMaxAverage_bruteforce),
        ("Sliding Window", findMaxAverage_sliding_window),
    ]

    for idx, (nums, k, expected) in enumerate(tests):
        print(f"\n--- Test Case {idx + 1} ---")
        print(f"nums = {nums}, k = {k}, expected = {expected}")
        for name, solver in solvers:
            got = solver(nums, k)
            status = "PASS" if abs(got - expected) < 1e-5 else "FAIL"
            print(f"[{status}] {name} | got={got}")
