"""
========================================================
LeetCode 48 - Rotate Image
========================================================
Difficulty : Medium
Link       : https://leetcode.com/problems/rotate-image/

Problem Statement
-----------------
You are given an n x n 2D matrix representing an image.
Rotate the image 90 degrees clockwise, in-place.

You must modify the input matrix directly.
Do NOT allocate another 2D matrix to do the rotation.

Examples
--------
Input : matrix = [[1,2,3],
                  [4,5,6],
                  [7,8,9]]
Output:           [[7,4,1],
                   [8,5,2],
                   [9,6,3]]

Input : matrix = [[5,1,9,11],
                  [2,4,8,10],
                  [13,3,6, 7],
                  [15,14,12,16]]
Output:           [[15,13,2,5],
                   [14,3,4,1],
                   [12,6,8,9],
                   [16,7,10,11]]

Constraints
-----------
- n == matrix.length == matrix[i].length
- 1 <= n <= 20
- -1000 <= matrix[i][j] <= 1000

Key insight
-----------
90° clockwise rotation:  new[j][n-1-i] = old[i][j]
Equivalently achieved by:
  (a) Transpose  then  reverse each row
  (b) Flip upside-down  then  transpose
  (c) Four-way cyclic swap layer by layer
========================================================
"""

from typing import List
import copy


# ──────────────────────────────────────────────────────
# Approach 1 : Extra Space
# ──────────────────────────────────────────────────────
# Intuition  : Copy the matrix, then apply the formula
#              new[j][n-1-i] = old[i][j] directly.
#              Simple but violates the in-place requirement.
# Time       : O(n²)
# Space      : O(n²)
# ──────────────────────────────────────────────────────
def rotate_extra_space(matrix: List[List[int]]) -> None:
    n = len(matrix)
    old = copy.deepcopy(matrix)
    for i in range(n):
        for j in range(n):
            matrix[j][n - 1 - i] = old[i][j]


# ──────────────────────────────────────────────────────
# Approach 2 : Transpose + Reverse Each Row  ★ CLASSIC ★
# ──────────────────────────────────────────────────────
# Intuition  : A 90° clockwise rotation equals:
#              1. Transpose the matrix  (swap [i][j] ↔ [j][i])
#              2. Reverse every row
#
#              Transpose:          Reverse rows:
#              1 4 7               7 4 1
#              2 5 8       →       8 5 2
#              3 6 9               9 6 3  ✓
# Time       : O(n²)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def rotate_transpose_reverse(matrix: List[List[int]]) -> None:
    n = len(matrix)
    # Step 1: Transpose (upper triangle only to avoid double-swap)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()


# ──────────────────────────────────────────────────────
# Approach 3 : Flip Upside-Down + Transpose
# ──────────────────────────────────────────────────────
# Intuition  : A 90° clockwise rotation also equals:
#              1. Reverse the row order  (flip top ↔ bottom)
#              2. Transpose the matrix
#
#              Flip:               Transpose:
#              7 8 9               7 4 1
#              4 5 6       →       8 5 2
#              1 2 3               9 6 3  ✓
# Time       : O(n²)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def rotate_flip_transpose(matrix: List[List[int]]) -> None:
    n = len(matrix)
    # Step 1: Reverse row order
    matrix.reverse()
    # Step 2: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]


# ──────────────────────────────────────────────────────
# Approach 4 : Four-Way Cyclic Swap (Layer by Layer)
# ──────────────────────────────────────────────────────
# Intuition  : Process each concentric layer from outside in.
#              For each element in the current layer, perform
#              a 4-way cyclic swap:
#                top → right → bottom → left → top
#              Uses a single temp variable; truly in-place.
#
#              For a 3×3 matrix, layer 0 processes 4 groups:
#              (0,0)↔(0,2)↔(2,2)↔(2,0)
#              (0,1)↔(1,2)↔(2,1)↔(1,0)
# Time       : O(n²)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def rotate_cyclic_swap(matrix: List[List[int]]) -> None:
    n = len(matrix)
    for layer in range(n // 2):
        first = layer
        last  = n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = matrix[first][i]                            # save top
            matrix[first][i]           = matrix[last - offset][first]   # left → top
            matrix[last - offset][first] = matrix[last][last - offset]  # bottom → left
            matrix[last][last - offset] = matrix[i][last]               # right → bottom
            matrix[i][last]            = top                            # top → right


# ──────────────────────────────────────────────────────
# Approach 5 : Pythonic One-Liner (zip trick)
# ──────────────────────────────────────────────────────
# Intuition  : zip(*matrix) transposes the matrix (each column
#              becomes a row). Reversing the order of zip's
#              result rotates 90° clockwise.
#              Not truly in-place (reassigns matrix[:]), but
#              widely accepted in interviews as "in-place spirit".
# Time       : O(n²)
# Space      : O(n²)  — zip builds new tuples
# ──────────────────────────────────────────────────────
def rotate_zip(matrix: List[List[int]]) -> None:
    matrix[:] = [list(row) for row in zip(*matrix[::-1])]


# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach                   | Time  | Space | In-place? |
# |----|----------------------------|-------|-------|-----------|
# | 1  | Extra Space                | O(n²) | O(n²) | No        |
# | 2  | Transpose + Reverse Rows   | O(n²) | O(1)  | Yes ★     |
# | 3  | Flip Upside-Down + Trans.  | O(n²) | O(1)  | Yes ★     |
# | 4  | Four-Way Cyclic Swap       | O(n²) | O(1)  | Yes ★     |
# | 5  | Pythonic zip trick         | O(n²) | O(n²) | Spirit    |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        (
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]],
            [[7, 4, 1],
             [8, 5, 2],
             [9, 6, 3]],
        ),
        (
            [[5,  1,  9, 11],
             [2,  4,  8, 10],
             [13, 3,  6,  7],
             [15, 14, 12, 16]],
            [[15, 13, 2,  5],
             [14, 3,  4,  1],
             [12, 6,  8,  9],
             [16, 7,  10, 11]],
        ),
        ([[1]], [[1]]),
        (
            [[1, 2],
             [3, 4]],
            [[3, 1],
             [4, 2]],
        ),
    ]

    solutions = [
        ("1. Extra Space",              rotate_extra_space),
        ("2. Transpose + Reverse Rows", rotate_transpose_reverse),
        ("3. Flip + Transpose",         rotate_flip_transpose),
        ("4. Four-Way Cyclic Swap",     rotate_cyclic_swap),
        ("5. Pythonic zip trick",       rotate_zip),
    ]

    for matrix_in, expected in test_cases:
        print(f"\nInput:\n  {matrix_in}")
        for name, fn in solutions:
            mat = copy.deepcopy(matrix_in)
            fn(mat)
            status = "PASS" if mat == expected else "FAIL"
            print(f"  {status}  {name:<30} → {mat}")
