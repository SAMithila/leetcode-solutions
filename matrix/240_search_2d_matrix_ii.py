"""
LeetCode 240 - Search a 2D Matrix II
Write an efficient algorithm to search for a target value in an m x n matrix
where each row is sorted left-to-right and each column is sorted top-to-bottom.

Example:
  Input:  matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], target = 5
  Output: True
"""

from typing import List


# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(m * n)
# Space: O(1)
# ─────────────────────────────────────────────
def searchMatrix_brute(matrix: List[List[int]], target: int) -> bool:
    for row in matrix:
        for val in row:
            if val == target:
                return True
    return False


# ─────────────────────────────────────────────
# Approach 2: Binary Search per Row
# Time:  O(m log n)
# Space: O(1)
# ─────────────────────────────────────────────
def searchMatrix_binary(matrix: List[List[int]], target: int) -> bool:
    import bisect
    for row in matrix:
        idx = bisect.bisect_left(row, target)
        if idx < len(row) and row[idx] == target:
            return True
    return False


# ─────────────────────────────────────────────
# Approach 3: Staircase Search (Top-Right Corner)
# Time:  O(m + n)
# Space: O(1)
#
# Key insight: starting at top-right, every move eliminates
# an entire row (go down) or an entire column (go left).
# ─────────────────────────────────────────────
def searchMatrix_staircase(matrix: List[List[int]], target: int) -> bool:
    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1

    while row < rows and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1   # current col too large — eliminate it
        else:
            row += 1   # current row too small — eliminate it

    return False


# ─────────────────────────────────────────────
# Approach 4: Divide and Conquer
# Time:  O(n log n)  for square n×n matrix
# Space: O(log n)    — recursion stack
#
# Split at midpoint of current submatrix. The mid value
# lets us prune two of the four quadrants each call.
# ─────────────────────────────────────────────
def searchMatrix_divide(matrix: List[List[int]], target: int) -> bool:
    def search(r1, c1, r2, c2):
        if r1 > r2 or c1 > c2:
            return False
        mid_row, mid_col = (r1 + r2) // 2, (c1 + c2) // 2
        mid = matrix[mid_row][mid_col]

        if mid == target:
            return True
        elif mid > target:
            # target is in top-left OR top-right OR bottom-left quadrant
            # but NOT bottom-right (all values >= mid > target)
            return (search(r1, c1, mid_row - 1, c2) or
                    search(mid_row, c1, r2, mid_col - 1))
        else:
            # target is in bottom-right OR bottom-left OR top-right quadrant
            # but NOT top-left (all values <= mid < target)
            return (search(mid_row + 1, c1, r2, c2) or
                    search(r1, mid_col + 1, mid_row, c2))

    if not matrix or not matrix[0]:
        return False
    return search(0, 0, len(matrix) - 1, len(matrix[0]) - 1)


# ─────────────────────────────────────────────
# OPTIMAL — Approach 3 (Staircase Search)
# O(m + n) time  |  O(1) extra space
# ─────────────────────────────────────────────
searchMatrix = searchMatrix_staircase


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    matrix = [
        [1,  4,  7,  11, 15],
        [2,  5,  8,  12, 19],
        [3,  6,  9,  16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]

    tests = [
        (matrix, 5,  True),
        (matrix, 20, False),
        (matrix, 1,  True),
        (matrix, 30, True),
        (matrix, 0,  False),
        (matrix, 31, False),
        ([[1]], 1,  True),
        ([[1]], 2,  False),
        ([[1, 3, 5]], 3, True),
        ([[1, 3, 5]], 4, False),
    ]

    solvers = [
        ("Brute Force",       searchMatrix_brute),
        ("Binary Search",     searchMatrix_binary),
        ("Staircase",         searchMatrix_staircase),
        ("Divide & Conquer",  searchMatrix_divide),
    ]

    for mat, target, expected in tests:
        for name, fn in solvers:
            out = fn(mat, target)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | target={target} | got={out}")
