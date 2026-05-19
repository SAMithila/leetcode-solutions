"""
LeetCode 289 - Game of Life
Given an m x n board of cells (0=dead, 1=alive), apply Conway's rules
simultaneously to every cell and update the board in-place.

Rules (based on 8 neighbors):
  1. Live cell with < 2 live neighbors → dies (underpopulation)
  2. Live cell with 2 or 3 live neighbors → lives
  3. Live cell with > 3 live neighbors → dies (overpopulation)
  4. Dead cell with exactly 3 live neighbors → becomes alive (reproduction)

Example:
  Input:  [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]
  Output: [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]
"""

from typing import List

DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]


# ─────────────────────────────────────────────
# Approach 1: Extra Space (Copy)
# Time:  O(m * n)
# Space: O(m * n)  — full copy of board
# ─────────────────────────────────────────────
def gameOfLife_copy(board: List[List[int]]) -> None:
    rows, cols = len(board), len(board[0])
    copy = [row[:] for row in board]

    for r in range(rows):
        for c in range(cols):
            live = sum(
                copy[r + dr][c + dc]
                for dr, dc in DIRS
                if 0 <= r + dr < rows and 0 <= c + dc < cols
            )
            if copy[r][c] == 1:
                board[r][c] = 1 if live in (2, 3) else 0
            else:
                board[r][c] = 1 if live == 3 else 0


# ─────────────────────────────────────────────
# Approach 2: In-place Marker Encoding
# Time:  O(m * n)
# Space: O(1)
#
# Mark transitions without losing original state:
#   1 = alive → alive (unchanged)
#   2 = alive → dead  (was alive: cell in [1, 2])
#   3 = dead  → alive (was dead:  cell in [0, 3])
#   0 = dead  → dead  (unchanged)
#
# Final pass: board[r][c] %= 2
# ─────────────────────────────────────────────
def gameOfLife_inplace(board: List[List[int]]) -> None:
    rows, cols = len(board), len(board[0])

    for r in range(rows):
        for c in range(cols):
            live = 0
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] in (1, 2):
                        live += 1

            if board[r][c] == 1:
                if live < 2 or live > 3:
                    board[r][c] = 2   # alive → dead
            else:
                if live == 3:
                    board[r][c] = 3   # dead → alive

    for r in range(rows):
        for c in range(cols):
            board[r][c] %= 2


# ─────────────────────────────────────────────
# Approach 3: In-place Bit Encoding
# Time:  O(m * n)
# Space: O(1)
#
# Pack old and new state into one cell using two bits:
#   bit 0 (cell & 1)  = original state
#   bit 1 (cell >> 1) = new state
#
#   0b01 = 1 → alive dies       (bit 1 never set)
#   0b11 = 3 → alive stays alive
#   0b10 = 2 → dead  becomes alive
#   0b00 = 0 → dead  stays dead
#
# Final pass: board[r][c] >>= 1
# ─────────────────────────────────────────────
def gameOfLife_bitwise(board: List[List[int]]) -> None:
    rows, cols = len(board), len(board[0])

    for r in range(rows):
        for c in range(cols):
            live = 0
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    live += board[nr][nc] & 1   # original state in bit 0

            if board[r][c] == 1:
                if live == 2 or live == 3:
                    board[r][c] = 3   # 0b11: was alive, stays alive
            else:
                if live == 3:
                    board[r][c] = 2   # 0b10: was dead, becomes alive

    for r in range(rows):
        for c in range(cols):
            board[r][c] >>= 1


# ─────────────────────────────────────────────
# Approach 4: Sparse Set (Infinite Grid)
# Time:  O(L)   — L = number of live cells
# Space: O(L)   — set of live cell coordinates
#
# Only candidates for change are live cells and their neighbors.
# Scales well for large sparse boards; handles infinite grids.
# ─────────────────────────────────────────────
def gameOfLife_sparse(board: List[List[int]]) -> None:
    rows, cols = len(board), len(board[0])
    live = {(r, c) for r in range(rows) for c in range(cols) if board[r][c]}

    neighbor_count: dict = {}
    for r, c in live:
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_count[(nr, nc)] = neighbor_count.get((nr, nc), 0) + 1

    for r in range(rows):
        for c in range(cols):
            n = neighbor_count.get((r, c), 0)
            if (r, c) in live:
                board[r][c] = 1 if n in (2, 3) else 0
            else:
                board[r][c] = 1 if n == 3 else 0


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (In-place Bit Encoding)
# O(m * n) time  |  O(1) extra space
# ─────────────────────────────────────────────
gameOfLife = gameOfLife_inplace


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    import copy

    tests = [
        (
            [[0,1,0],[0,0,1],[1,1,1],[0,0,0]],
            [[0,0,0],[1,0,1],[0,1,1],[0,1,0]],
        ),
        (
            [[1,1],[1,0]],
            [[1,1],[1,1]],
        ),
        (
            [[0,0,0],[0,1,0],[0,0,0]],
            [[0,0,0],[0,0,0],[0,0,0]],
        ),
        (
            [[0,0,0],[1,1,1],[0,0,0]],
            [[0,1,0],[0,1,0],[0,1,0]],
        ),
        (
            [[1]],
            [[0]],
        ),
        (
            [[0]],
            [[0]],
        ),
    ]

    solvers = [
        ("Copy",          gameOfLife_copy),
        ("Marker",        gameOfLife_inplace),
        ("Bit Encoding",  gameOfLife_bitwise),
        ("Sparse Set",    gameOfLife_sparse),
    ]

    for board, expected in tests:
        for name, fn in solvers:
            b = copy.deepcopy(board)
            fn(b)
            status = "PASS" if b == expected else "FAIL"
            print(f"[{status}] {name} | input={board} | got={b}")
