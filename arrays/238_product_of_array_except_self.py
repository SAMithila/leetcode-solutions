"""
========================================================
LeetCode 238 - Product of Array Except Self
========================================================
Difficulty : Medium
Link       : https://leetcode.com/problems/product-of-array-except-self/

Problem Statement
-----------------
Given an integer array nums, return an array answer such that
answer[i] is equal to the product of all elements of nums
except nums[i].

You must write an algorithm that runs in O(n) time and
without using the division operation.

Follow-up: Can you solve it in O(1) extra space?
(The output array does NOT count as extra space.)

Examples
--------
Input : nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]

Input : nums = [-1, 1, 0, -3, 3]
Output: [0, 0, 9, 0, 0]

Constraints
-----------
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- The product of any prefix or suffix fits in a 32-bit integer
========================================================
"""

from typing import List


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force
# ──────────────────────────────────────────────────────
# Intuition  : For each index i, multiply every element
#              except nums[i] using a nested loop.
# Time       : O(n²)
# Space      : O(1)  — ignoring output
# ──────────────────────────────────────────────────────
def productExceptSelf_brute_force(nums: List[int]) -> List[int]:
    n = len(nums)
    result = []
    for i in range(n):
        product = 1
        for j in range(n):
            if i != j:
                product *= nums[j]
        result.append(product)
    return result


# ──────────────────────────────────────────────────────
# Approach 2 : Division  (violates problem constraint)
# ──────────────────────────────────────────────────────
# Intuition  : Compute total product; answer[i] = total / nums[i].
#              Zero handling:
#              - 2+ zeros → all answers are 0
#              - 1 zero   → only the zero-index position gets
#                           the product of non-zero elements
#              - 0 zeros  → answer[i] = total / nums[i]
# Note       : The problem explicitly forbids division.
#              Shown here for completeness only.
# Time       : O(n)
# Space      : O(1)  — ignoring output
# ──────────────────────────────────────────────────────
def productExceptSelf_division(nums: List[int]) -> List[int]:
    zero_count = nums.count(0)
    n = len(nums)

    if zero_count > 1:
        return [0] * n

    if zero_count == 1:
        non_zero_product = 1
        for x in nums:
            if x != 0:
                non_zero_product *= x
        return [non_zero_product if x == 0 else 0 for x in nums]

    total = 1
    for x in nums:
        total *= x
    return [total // x for x in nums]


# ──────────────────────────────────────────────────────
# Approach 3 : Left Array + Right Array
# ──────────────────────────────────────────────────────
# Intuition  : answer[i] = (product of all elements left of i)
#                         * (product of all elements right of i)
#              Build two separate prefix/suffix arrays,
#              then multiply element-wise.
# Time       : O(n)
# Space      : O(n)  — two extra arrays
# ──────────────────────────────────────────────────────
def productExceptSelf_prefix_suffix(nums: List[int]) -> List[int]:
    n = len(nums)
    left  = [1] * n   # left[i]  = product of nums[0..i-1]
    right = [1] * n   # right[i] = product of nums[i+1..n-1]

    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]

    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i + 1]

    return [left[i] * right[i] for i in range(n)]


# ──────────────────────────────────────────────────────
# Approach 4 : Output Array + Right Running Product  ★ OPTIMAL ★
# ──────────────────────────────────────────────────────
# Intuition  : Use the output array itself to store left
#              prefix products (first pass left→right).
#              Then do a second pass right→left, maintaining
#              a running right product and multiplying in-place.
#              Result: O(1) extra space (output doesn't count).
# Time       : O(n)
# Space      : O(1)  — excluding output array
# ──────────────────────────────────────────────────────
def productExceptSelf_optimized(nums: List[int]) -> List[int]:
    n = len(nums)
    result = [1] * n

    # Pass 1: result[i] = product of all elements to the LEFT of i
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Pass 2: multiply in the product of all elements to the RIGHT of i
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result


# ──────────────────────────────────────────────────────
# Approach 5 : Prefix Products + Suffix on the Fly
# ──────────────────────────────────────────────────────
# Intuition  : Build the full left prefix array first (explicit),
#              then traverse right-to-left with a running suffix
#              and update each slot. Equivalent to Approach 4
#              but writes the left array explicitly for clarity.
# Time       : O(n)
# Space      : O(n)  — explicit left array
# ──────────────────────────────────────────────────────
def productExceptSelf_prefix_then_suffix(nums: List[int]) -> List[int]:
    n = len(nums)
    left = [1] * n

    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]

    suffix = 1
    for i in range(n - 1, -1, -1):
        left[i] *= suffix
        suffix *= nums[i]

    return left


# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach                   | Time  | Space | Notes                         |
# |----|----------------------------|-------|-------|-------------------------------|
# | 1  | Brute Force                | O(n²) | O(1)  | Nested loops                  |
# | 2  | Division                   | O(n)  | O(1)  | Easy but forbidden by problem |
# | 3  | Left + Right Arrays        | O(n)  | O(n)  | Clear and intuitive           |
# | 4  | Output + Right Running     | O(n)  | O(1)  | Optimal — follow-up answer ★  |
# | 5  | Prefix Array + Suffix OTF  | O(n)  | O(n)  | Explicit version of #4        |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 4],       [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3],  [0, 0, 9, 0, 0]),
        ([1, 1],             [1, 1]),
        ([2, 3],             [3, 2]),
        ([1, 0],             [0, 1]),
        ([0, 0],             [0, 0]),
        ([-1, -2, -3, -4],   [-24, -12, -8, -6]),
    ]

    solutions = [
        ("1. Brute Force",           productExceptSelf_brute_force),
        ("2. Division",              productExceptSelf_division),
        ("3. Left + Right Arrays",   productExceptSelf_prefix_suffix),
        ("4. Output + Right Running",productExceptSelf_optimized),
        ("5. Prefix + Suffix OTF",   productExceptSelf_prefix_then_suffix),
    ]

    for nums, expected in test_cases:
        print(f"\nnums={nums}  →  expected={expected}")
        for name, fn in solutions:
            result = fn(nums[:])
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}  {name:<28} → {result}")
