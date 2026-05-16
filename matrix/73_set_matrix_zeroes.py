"""
LeetCode 73 - Set Matrix Zeroes
Given an m x n integer matrix, if an element is 0, set its entire row
and column to 0's in-place.

Example:
  Input:  [[1,1,1],[1,0,1],[1,1,1]]
  Output: [[1,0,1],[0,0,0],[1,0,1]]
"""

from typing import List


# ─────────────────────────────────────────────
# Approach 1: Brute Force (Matrix Copy)
# Time:  O(m * n * (m + n))  — inner loops per zero found
# Space: O(m * n)            — full copy of matrix
# ─────────────────────────────────────────────
def setZeroes_brute(matrix: List[List[int]]) -> None:
    rows, cols = len(matrix), len(matrix[0])
    copy = [row[:] for row in matrix]

    for i in range(rows):
        for j in range(cols):
            if copy[i][j] == 0:
                for k in range(cols):
                    matrix[i][k] = 0
                for k in range(rows):
                    matrix[k][j] = 0


# ─────────────────────────────────────────────
# Approach 2: Extra Space (Sets)
# Time:  O(m * n)
# Space: O(m + n)  — two sets tracking zero rows/cols
# ─────────────────────────────────────────────
def setZeroes_sets(matrix: List[List[int]]) -> None:
    rows, cols = len(matrix), len(matrix[0])
    zero_rows = set()
    zero_cols = set()

    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 0:
                zero_rows.add(row)
                zero_cols.add(col)

    for row in range(rows):
        for col in range(cols):
            if row in zero_rows or col in zero_cols:
                matrix[row][col] = 0


# ─────────────────────────────────────────────
# Approach 3: In-place — First Row/Col as Markers
# Time:  O(m * n)
# Space: O(1)
# ─────────────────────────────────────────────
def setZeroes_inplace(matrix: List[List[int]]) -> None:
    rows, cols = len(matrix), len(matrix[0])

    # Check if first row / first col themselves contain a zero
    first_row_has_zero = any(matrix[0][col] == 0 for col in range(cols))
    first_col_has_zero = any(matrix[row][0] == 0 for row in range(rows))

    # Use first row and first col as markers for the rest of the matrix
    for row in range(1, rows):
        for col in range(1, cols):
            if matrix[row][col] == 0:
                matrix[row][0] = 0  # mark row
                matrix[0][col] = 0  # mark col

    # Zero out cells based on markers (skip first row/col for now)
    for row in range(1, rows):
        for col in range(1, cols):
            if matrix[row][0] == 0 or matrix[0][col] == 0:
                matrix[row][col] = 0

    # Handle first row and first col separately
    if first_row_has_zero:
        for col in range(cols):
            matrix[0][col] = 0

    if first_col_has_zero:
        for row in range(rows):
            matrix[row][0] = 0


# ─────────────────────────────────────────────
# Approach 4: Boolean Grid (full extra space)
# Time:  O(m * n)
# Space: O(m * n)  — two boolean grids
# ─────────────────────────────────────────────
def setZeroes_bool_grid(matrix: List[List[int]]) -> None:
    rows, cols = len(matrix), len(matrix[0])
    zero_row = [False] * rows
    zero_col = [False] * cols

    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 0:
                zero_row[row] = True
                zero_col[col] = True

    for row in range(rows):
        for col in range(cols):
            if zero_row[row] or zero_col[col]:
                matrix[row][col] = 0


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (In-place First Row/Col)
# O(m * n) time  |  O(1) extra space
# ─────────────────────────────────────────────
setZeroes = setZeroes_inplace


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    import copy

    tests = [
        (
            [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
            [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
        ),
        (
            [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],
            [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]],
        ),
        (
            [[1]],
            [[1]],
        ),
        (
            [[0]],
            [[0]],
        ),
        (
            [[1, 0], [1, 1]],
            [[0, 0], [1, 0]],
        ),
        (
            [[0, 1], [1, 1]],
            [[0, 0], [0, 1]],
        ),
    ]

    solvers = [
        ("Brute Force", setZeroes_brute),
        ("Sets",        setZeroes_sets),
        ("In-place",    setZeroes_inplace),
        ("Bool Grid",   setZeroes_bool_grid),
    ]

    for mat, expected in tests:
        for name, fn in solvers:
            m = copy.deepcopy(mat)
            fn(m)
            status = "PASS" if m == expected else "FAIL"
            print(f"[{status}] {name} | input={mat} | got={m}")
