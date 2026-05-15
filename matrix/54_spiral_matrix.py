"""
LeetCode 54 - Spiral Matrix
Given an m x n matrix, return all elements in spiral order.

Example:
  Input:  [[1,2,3],[4,5,6],[7,8,9]]
  Output: [1,2,3,6,9,8,7,4,5]
"""

from typing import List

'''
# ─────────────────────────────────────────────
# Approach 1: Visited Array + Direction Vectors
# Time:  O(m * n)
# Space: O(m * n)  — visited grid
# ─────────────────────────────────────────────
def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return []
        
        rows, cols = len(matrix), len(matrix[0])
        result = []
        visited = [[False] * cols for _ in range(rows)]
        
        # Directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dir_idx = 0
        row, col = 0, 0
        
        for _ in range(rows * cols):
            result.append(matrix[row][col])
            visited[row][col] = True
            
            # Calculate next position
            next_row = row + directions[dir_idx][0]
            next_col = col + directions[dir_idx][1]
            
            # Change direction if needed
            if (next_row < 0 or next_row >= rows or 
                next_col < 0 or next_col >= cols or 
                visited[next_row][next_col]):
                dir_idx = (dir_idx + 1) % 4
                next_row = row + directions[dir_idx][0]
                next_col = col + directions[dir_idx][1]
            
            row, col = next_row, next_col
        
        return result
'''

# ─────────────────────────────────────────────
# Approach 2: Shrinking Boundaries (Layer Peeling)
# Time:  O(m * n)
# Space: O(1)  — no extra grid
# ─────────────────────────────────────────────
def spiralOrder_boundaries(matrix: List[List[int]]) -> List[int]:
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # left → right along top row
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # top → bottom along right col
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # right → left along bottom row  (guard: still a valid row)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # bottom → top along left col  (guard: still a valid col)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result

'''
# ─────────────────────────────────────────────
# Approach 3: Recursive Peel (pop first row + rotate)
# Time:  O((m * n)^2)  — zip/rotate rebuilds matrix each call
# Space: O(m * n)      — recursion + intermediate matrices
# ─────────────────────────────────────────────
def spiralOrder_recursive(matrix: List[List[int]]) -> List[int]:
    if not matrix:
        return []
    # take the top row, then rotate remaining 90° clockwise to bring
    # the next spiral edge to the top
    return list(matrix[0]) + spiralOrder_recursive(
        list(zip(*matrix[1:]))[::-1]
    )


# ─────────────────────────────────────────────
# Approach 4: Recursive Shrinking Boundaries
# Time:  O(m * n)
# Space: O(min(m, n))  — recursion depth = number of layers
# ─────────────────────────────────────────────
def spiralOrder_recursive_bounds(matrix: List[List[int]]) -> List[int]:
    result = []

    def spiral(top, bottom, left, right):
        if top > bottom or left > right:
            return

        for col in range(left, right + 1):
            result.append(matrix[top][col])

        for row in range(top + 1, bottom + 1):
            result.append(matrix[row][right])

        if top < bottom:
            for col in range(right - 1, left - 1, -1):
                result.append(matrix[bottom][col])

        if left < right:
            for row in range(bottom - 1, top, -1):
                result.append(matrix[row][left])

        spiral(top + 1, bottom - 1, left + 1, right - 1)

    if matrix and matrix[0]:
        spiral(0, len(matrix) - 1, 0, len(matrix[0]) - 1)

    return result
'''

# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Shrinking Boundaries)
# O(m * n) time  |  O(1) extra space
# ─────────────────────────────────────────────
spiralOrder = spiralOrder_boundaries


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]],        [1,2,3,6,9,8,7,4,5]),
        ([[1, 2, 3, 4], [5, 6, 7, 8], [9,10,11,12]], [1,2,3,4,8,12,11,10,9,5,6,7]),
        ([[1]],                                       [1]),
        ([[1, 2], [3, 4]],                            [1, 2, 4, 3]),
        ([[1], [2], [3]],                             [1, 2, 3]),
        ([[1, 2, 3]],                                 [1, 2, 3]),
    ]

    solvers = [
     #   ("Visited Array",          spiralOrder_visited),
        ("Shrinking Bounds",       spiralOrder_boundaries),
     #   ("Recursive Peel",         spiralOrder_recursive),
     #  ("Recursive Bounds",       spiralOrder_recursive_bounds),
    ]

    for mat, expected in tests:
        for name, fn in solvers:
            out = fn([row[:] for row in mat])
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | input={mat} | got={out}")
