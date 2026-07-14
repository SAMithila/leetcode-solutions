"""
LeetCode 209 - Minimum Size Subarray Sum
Given an array of positive integers nums and a positive integer target,
return the minimal length of a subarray whose sum >= target.
Return 0 if no such subarray exists.

Example:
  Input:  target = 7, nums = [2,3,1,2,4,3]
  Output: 2  ([4,3])

  Input:  target = 4, nums = [1,4,4]
  Output: 1  ([4])

  Input:  target = 11, nums = [1,1,1,1,1,1,1,1]
  Output: 0

KEY INSIGHT:
  All numbers are positive → adding more always increases sum,
  removing always decreases. This monotonic property makes
  two-pointer / sliding window provably correct and O(n).
"""
"""
## LC 209 — Minimum Size Subarray Sum (Interview Format)

---

### Step 1 — Understand & Restate

> "Given an array of positive integers and a target, find the minimum length of a contiguous subarray whose sum is greater than or equal to target. Return 0 if no such subarray exists."

```
nums = [2,3,1,2,4,3],  target = 7

All valid subarrays with sum >= 7:
[2,3,1,2] → sum=8, length=4
[3,1,2,4] → sum=10, length=4
[1,2,4,3] → sum=10, length=4
[2,4,3]   → sum=9,  length=3
[4,3]     → sum=7,  length=2  ← shortest

Answer: 2
```

---

### Step 2 — Clarifying Questions

```
Q: Can nums be empty?              → Yes → return 0
Q: Can values be negative or zero? → No, all positive integers (crucial!)
Q: What if no subarray reaches target? → return 0
Q: Can target be larger than total sum? → Yes → return 0
Q: Duplicate values allowed?       → Yes
```

> "The fact that all values are **positive** is the key constraint — it means growing the window always increases the sum and shrinking always decreases it. This makes sliding window possible."

---

### Step 3 — Brute Force → Optimal

**Brute Force — O(n²)**

```python
# check every possible subarray
for i in range(len(nums)):
    total = 0
    for j in range(i, len(nums)):
        total += nums[j]
        if total >= target:
            best = min(best, j - i + 1)
            break
```

> "This is O(n²) — too slow for n=10^5. Since all values are positive, I can use a sliding window instead."

**Why sliding window works here:**

```
All values positive →
  growing window  (right++)  → sum always increases
  shrinking window (left++)  → sum always decreases

So we never need to recheck a window we've already shrunk past.
Both pointers only move forward → O(n) total.
```

---

### Step 4 — Edge Cases (say before coding)

```
1. Empty array:          nums=[],    target=7    → return 0
2. No valid subarray:    nums=[1,1], target=100  → return 0
3. Entire array needed:  nums=[1,2,3], target=6  → return 3
4. Single element fits:  nums=[7],   target=7    → return 1
5. Single element fails: nums=[3],   target=7    → return 0
6. All elements same:    nums=[1,1,1,1], target=3 → return 3
7. First element fits:   nums=[7,1,1], target=7  → return 1
```

---

### Step 5 — Code

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left  = 0
        total = 0
        best  = float('inf')

        for right in range(len(nums)):
            total += nums[right]            # expand window

            while total >= target:          # window valid — try to shrink
                best  = min(best, right - left + 1)
                total -= nums[left]         # remove leftmost element
                left  += 1                  # shrink window

        return 0 if best == float('inf') else best
```

---

### Step 6 — Dry Run (trace out loud)

```
nums = [2,3,1,2,4,3],  target = 7
left=0, total=0, best=inf

right=0: total = 0+2 = 2
         2 < 7 → no shrink
         window = [2]

right=1: total = 2+3 = 5
         5 < 7 → no shrink
         window = [2,3]

right=2: total = 5+1 = 6
         6 < 7 → no shrink
         window = [2,3,1]

right=3: total = 6+2 = 8
         8 >= 7 → SHRINK
           best = min(inf, 3-0+1) = 4     window=[2,3,1,2] length 4
           total = 8-2 = 6, left=1
         6 < 7 → stop shrinking
         window = [3,1,2]

right=4: total = 6+4 = 10
         10 >= 7 → SHRINK
           best = min(4, 4-1+1) = 4       window=[3,1,2,4] length 4
           total = 10-3 = 7, left=2
         7 >= 7 → SHRINK again
           best = min(4, 4-2+1) = 3       window=[1,2,4] length 3
           total = 7-1 = 6, left=3
         6 < 7 → stop shrinking
         window = [2,4]

right=5: total = 6+3 = 9
         9 >= 7 → SHRINK
           best = min(3, 5-3+1) = 3       window=[2,4,3] length 3
           total = 9-2 = 7, left=4
         7 >= 7 → SHRINK again
           best = min(3, 5-4+1) = 2       window=[4,3] length 2 ✓
           total = 7-4 = 3, left=5
         3 < 7 → stop shrinking

return 2  ✓
```

---

### Step 7 — Complexity Analysis

**Time — O(n)**

```
right moves forward n times total        → O(n)
left  moves forward at most n times total → O(n)

Even though there's a while inside a for,
left never goes backward — total moves = 2n → O(n)
```

**Space — O(1)**

```
Only 3 variables used: left, total, best
No extra arrays, maps, or stacks
Input array not modified
→ constant space regardless of input size
```

---

### Step 8 — Follow-up Questions & Answers

**Q: What if the array had negative numbers?**

> "Sliding window breaks completely. A negative number means adding it could decrease the sum, so shrinking the window doesn't guarantee the sum goes down. We'd need prefix sums + binary search instead, giving O(n log n)."

---

**Q: What if we wanted maximum size subarray instead of minimum?**

> "Flip the logic — instead of shrinking when valid, we'd track the largest window before it becomes invalid. Still O(n)."

---

**Q: How would you handle this for a streaming data input?**

> "We can't use sliding window directly since we don't have all elements upfront. We'd need a different approach — likely maintaining a running sum and a queue of partial sums."

---

### Recap Card

```
Problem type:   Sliding Window
Pattern:        Expand right, shrink left when valid
Key constraint: All positive → shrinking always reduces sum
Why not O(n²): left never goes backward, total moves = 2n

Time:    O(n)
Space:   O(1)

Edge cases:
  → empty array          → return 0
  → no valid subarray    → best stays inf → return 0
  → single element ≥ target → return 1

Recurring bugs to check:
  → right - left + 1 (not right - left)
  → float('inf') comparison at the end
  → while not if (need to keep shrinking, not just once)
```
"""

from typing import List
import bisect


# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(n^2)
# Space: O(1)
#
# Try every possible starting index.
# Expand right until sum >= target, record length, then move on.
# The `break` is valid because all nums are positive — a longer
# window from the same left can only be worse (larger length).
# ─────────────────────────────────────────────
def minSubArrayLen_brute(target: int, nums: List[int]) -> int:
    n = len(nums)
    best = float("inf")

    for left in range(n):          # try every starting position
        total = 0
        
        for right in range(left, n):
            total += nums[right]   # expand window to the right
            
            if total >= target:
                best = min(best, right - left + 1)  # valid window — record length
                break   # longer window from same left = worse answer
                        # only valid because all nums > 0

    return 0 if best == float("inf") else best


# ─────────────────────────────────────────────
# Approach 2: Sliding Window
# Time:  O(n)  — each element is added & removed at most once
# Space: O(1)
#
# Two pointers: right expands the window, left shrinks it.
#
# WHY the while loop (not if):
#   After shrinking once, total might still be >= target,
#   so keep shrinking to find the minimum valid window.
#
# WHY this is O(n) and not O(n^2):
#   left only ever moves forward — at most n times total
#   across all iterations of the outer loop.
# ─────────────────────────────────────────────
def minSubArrayLen_sliding(target: int, nums: List[int]) -> int:
    left = 0
    total = 0
    best = float("inf")

    for right in range(len(nums)):
        total += nums[right]           # expand: add right element to window

        while total >= target:         # window is valid — try to shrink it
            best = min(best, right - left + 1)  # record current window length
            total -= nums[left]        # shrink: remove left element from window
            left += 1                  # move left pointer forward

    return 0 if best == float("inf") else best

'''
# ─────────────────────────────────────────────
# Approach 3: Prefix Sum + Binary Search
# Time:  O(n log n)
# Space: O(n)
#
# prefix[i] = sum of nums[0..i-1]
# sum of subarray [left, right) = prefix[right] - prefix[left]
#
# For a fixed left, we want the smallest right such that:
#   prefix[right] >= prefix[left] + target
#
# Since prefix is strictly increasing (all nums > 0),
# binary search finds this right in O(log n).
#
# TRACE for nums=[2,3,1,2,4,3], target=7:
#   prefix = [0, 2, 5, 6, 8, 12, 15]
#   left=0: needed=7, bisect finds right=4 → length=4
#   left=1: needed=9, bisect finds right=5 → length=4
#   left=4: needed=16, bisect finds right=6 → length=2  ← best
# ─────────────────────────────────────────────
def minSubArrayLen_binary(target: int, nums: List[int]) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)         # prefix[0] = 0 (empty subarray)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]   # prefix[i+1] = sum of nums[0..i]

    best = float("inf")
    for left in range(n):
        needed = prefix[left] + target         # minimum prefix[right] to satisfy sum >= target
        right = bisect.bisect_left(prefix, needed)  # find smallest valid right index
        if right <= n:                         # right <= n means a valid subarray exists
            best = min(best, right - left)     # subarray length = right - left

    return 0 if best == float("inf") else best
'''

# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Sliding Window)
# O(n) time  |  O(1) space
# ─────────────────────────────────────────────
minSubArrayLen = minSubArrayLen_sliding


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        (7,  [2, 3, 1, 2, 4, 3],       2),
        (4,  [1, 4, 4],                 1),
        (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),
        (15, [1, 2, 3, 4, 5],           5),
        (7,  [2, 3, 1, 2, 4, 3],        2),
        (1,  [1, 1, 1],                 1),
        (100,[1, 2, 3],                 0),
        (6,  [10, 2, 3],                1),
    ]

    solvers = [
        ("Brute Force",  minSubArrayLen_brute),
        ("Sliding",      minSubArrayLen_sliding),
     #   ("Binary Search",minSubArrayLen_binary),
    ]

    for target, nums, expected in tests:
        for name, fn in solvers:
            out = fn(target, nums[:])
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | target={target} nums={nums} | got={out}")
