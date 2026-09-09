"""
LeetCode 130 - Surrounded Regions

Given an m x n matrix board containing 'X' and 'O', capture all regions that are 4-directionally surrounded by 'X'.

A region is captured by flipping all 'O's into 'X's in that surrounded region.

Example 1:
  Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
  Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
  Explanation: Notice that an 'O' should not be flipped if:
  - It is on the border, or
  - It is adjacent to an 'O' that should not be flipped.
  The bottom 'O' is on the border, so it is not flipped.
  The other three 'O's are surrounded by 'X's and are flipped.

Example 2:
  Input: board = [["X"]]
  Output: [["X"]]
"""
"""
## LC 130 — Surrounded Regions (Interview Format)

---

### Step 1 — Understand & Restate

> "We are given a grid of 'X's and 'O's. Any 'O' (or group of connected 'O's) that is completely surrounded by 'X's should be flipped to 'X'. A group of 'O's is NOT surrounded if at least one 'O' in the group is on the border of the board. Therefore, our task is to find all 'O's connected to the border, protect them, and flip all other 'O's to 'X's."

```
Board:
X X X X          X X X X
X O O X    →     X X X X
X X O X          X X X X
X O X X          X O X X
(The 'O' at the bottom row is on the border, so it and any 'O's connected to it are not captured.)
```

---

### Step 2 — Clarifying Questions

```
Q: What are the dimensions of the grid?              → m and n can be up to 200.
Q: Can the board be empty or have 1x1 dimensions?    → Yes, m, n >= 1.
Q: What direction qualifies as 'connected'?           → Only 4-directionally (up, down, left, right), not diagonally.
Q: Can we modify the grid in-place?                  → Yes, standard LeetCode signature returns None and expects in-place modification.
```

---

### Step 3 — Brute Force → Optimal

**Brute Force — DFS/BFS from every 'O' to see if it reaches the border — O(m * n) time, O(m * n) space:**
> "For each 'O' in the board, run a search to see if we can reach the boundary. If we can't, we collect all coordinates in that component and flip them. This requires keeping track of visited cells and is slightly messy because we search from the inside out."

**Optimal — Border-first DFS/BFS (Outside-In) — O(m * n) time, O(m * n) space:**
> "Instead of checking every inner cell, start at the borders. Any 'O' on the border is safe. Run a DFS/BFS from every border 'O' to find all reachable 'O's. Mark these safe 'O's with a temporary character (e.g., 'T').
> After marking, iterate through the entire board:
> - Flip any remaining 'O' (which must be surrounded) to 'X'.
> - Flip any 'T' back to 'O' (restoring safe cells)."

---

### Step 4 — Edge Cases

```
1. 1x1 or 2x2 board: All cells are borders, so no inner cell can be captured.
2. Board with no 'O's: No-op.
3. Board with all 'O's: All connected to the border, so nothing is flipped.
4. Large board with snake-like connected O-regions reaching the border.
```

---

### Step 5 — Code (Optimal Border DFS)

```python
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return
        
        m, n = len(board), len(board[0])
        
        def dfs(r, c):
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != 'O':
                return
            board[r][c] = 'T'
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        
        # Step 1: Run DFS for border 'O's
        for r in range(m):
            dfs(r, 0)
            dfs(r, n - 1)
        for c in range(n):
            dfs(0, c)
            dfs(m - 1, c)
            
        # Step 2: Traverse board, flip 'O' to 'X' and 'T' back to 'O'
        for r in range(m):
            for c in range(n):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == 'T':
                    board[r][c] = 'O'
```

---

### Step 6 — Dry Run

```
Board:
X X X X
X O O X
X X O X
X O X X

Borders:
Row 0: X X X X -> no 'O'
Row 3: X O X X -> 'O' at (3, 1) -> DFS(3, 1) starts
- board[3][1] = 'T'
- dfs(2, 1) -> board[2][1] is 'X', returns
- dfs(3, 2) -> board[3][2] is 'X', returns
- dfs(3, 0) -> board[3][0] is 'X', returns

Col 0: all 'X' or visited
Col 3: all 'X' or visited

After border DFS, board is:
X X X X
X O O X
X X O X
X T X X

Re-traversal:
- Inner 'O's at (1, 1), (1, 2), (2, 2) -> not connected to T -> remain 'O' -> flipped to 'X'.
- 'T' at (3, 1) -> flipped back to 'O'.

Final:
X X X X
X X X X
X X X X
X O X X (Correct!)
```

---

### Step 7 — Why This Works

> "An 'O' is surrounded if and only if it has no path to any border cell containing 'O'. By identifying all border 'O's and performing a graph traversal, we find the entire connected component of non-surrounded 'O's. Marking them with 'T' acts as a safeguard. Any remaining 'O' must be completely trapped, so it's safe to flip them to 'X'."

---

### Step 8 — Complexity Analysis

**Time — O(m * n)**
```
We potentially visit every cell during the DFS and definitely visit every cell during the final O(m*n) double-loop.
```

**Space — O(m * n)**
```
In the worst case (e.g., all cells are 'O'), the recursion stack can grow to O(m * n).
For BFS, the space complexity is O(min(m, n)) for the queue.
```

---

### Step 9 — Follow-up Questions & Answers

**Q: Can we implement this iteratively to avoid recursion stack overflow?**
> "Yes, using an explicit stack (DFS) or queue (BFS) with coordinates. This is safer for production code to avoid StackOverflowError in deep grids."

**Q: Can we solve this using Union-Find?**
> "Yes. We can union all border 'O's to a dummy node (index m*n). Then, for every 'O' in the grid, union it with its 4-directional 'O' neighbors. Finally, iterate through all cells; if it's an 'O' and its representative is not connected to the dummy node, flip it to 'X'."

---

### Recap Card

```
Problem type:   Graph (DFS/BFS / Matrix Traversal)
Pattern:        Border-first search / Outside-in flood fill
Key trick:      Mark border-connected 'O's with a temp character, then flip the rest

Time:    O(m * n)
Space:   O(m * n) recursion stack or queue

Alternatives:
  Iterative BFS/DFS (reduces maximum call stack)
  Union-Find (connect to dummy border node)

Edge cases:
  → Grid with size < 3x3 (no inner cells can be surrounded, no-op after restoration)
  → All 'O's or all 'X's
```
"""

from typing import List
from collections import deque


# ─────────────────────────────────────────────
# Approach 1: Recursive DFS (Border-First)
# Time:  O(m * n)
# Space: O(m * n) — recursion call stack
# ─────────────────────────────────────────────
def solve_dfs(board: List[List[str]]) -> None:
    if not board or not board[0]:
        return

    m, n = len(board), len(board[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != "O":
            return
        board[r][c] = "T"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Run DFS on border elements
    for r in range(m):
        dfs(r, 0)
        dfs(r, n - 1)
    for c in range(1, n - 1):
        dfs(0, c)
        dfs(m - 1, c)

    # Re-traverse board to flip remaining 'O's and restore 'T's
    for r in range(m):
        for c in range(n):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "T":
                board[r][c] = "O"


# ─────────────────────────────────────────────
# Approach 2: Iterative BFS (Border-First)
# Time:  O(m * n)
# Space: O(min(m, n)) — queue size
# ─────────────────────────────────────────────
def solve_bfs(board: List[List[str]]) -> None:
    if not board or not board[0]:
        return

    m, n = len(board), len(board[0])
    queue = deque()

    # Collect all border 'O's
    for r in range(m):
        if board[r][0] == "O":
            board[r][0] = "T"
            queue.append((r, 0))
        if board[r][n - 1] == "O":
            board[r][n - 1] = "T"
            queue.append((r, n - 1))
    for c in range(1, n - 1):
        if board[0][c] == "O":
            board[0][c] = "T"
            queue.append((0, c))
        if board[m - 1][c] == "O":
            board[m - 1][c] = "T"
            queue.append((m - 1, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                board[nr][nc] = "T"
                queue.append((nr, nc))

    # Re-traverse board to flip remaining 'O's and restore 'T's
    for r in range(m):
        for c in range(n):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "T":
                board[r][c] = "O"


# ─────────────────────────────────────────────
# Approach 3: Union-Find (Disjoint Set Union)
# Time:  O(m * n * α(m * n)) where α is the inverse Ackermann function
# Space: O(m * n)
# ─────────────────────────────────────────────
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> None:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            elif self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1

    def connected(self, i: int, j: int) -> bool:
        return self.find(i) == self.find(j)


def solve_union_find(board: List[List[str]]) -> None:
    if not board or not board[0]:
        return

    m, n = len(board), len(board[0])
    dummy = m * n
    uf = UnionFind(dummy + 1)

    for r in range(m):
        for c in range(n):
            if board[r][c] == "O":
                # If it's a border cell, union with the dummy node
                if r == 0 or r == m - 1 or c == 0 or c == n - 1:
                    uf.union(r * n + c, dummy)
                else:
                    # Union with 4-directional neighbors if they are 'O'
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                            uf.union(r * n + c, nr * n + nc)

    # Final pass: flip 'O's not connected to the dummy node
    for r in range(m):
        for c in range(n):
            if board[r][c] == "O" and not uf.connected(r * n + c, dummy):
                board[r][c] = "X"


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Iterative BFS)
# O(m * n) time | O(min(m, n)) space
# ─────────────────────────────────────────────
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        solve_bfs(board)


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    import copy

    tests = [
        # Test 1: Standard case
        [
            ["X", "X", "X", "X"],
            ["X", "O", "O", "X"],
            ["X", "X", "O", "X"],
            ["X", "O", "X", "X"],
        ],
        # Test 2: Single cell board
        [["X"]],
        # Test 3: Grid with only 'O's
        [["O", "O"], ["O", "O"]],
        # Test 4: Nested surrounded region
        [
            ["X", "X", "X", "X", "X"],
            ["X", "O", "O", "O", "X"],
            ["X", "O", "X", "O", "X"],
            ["X", "O", "O", "O", "X"],
            ["X", "X", "X", "X", "X"],
        ],
    ]

    expected_outputs = [
        [
            ["X", "X", "X", "X"],
            ["X", "X", "X", "X"],
            ["X", "X", "X", "X"],
            ["X", "O", "X", "X"],
        ],
        [["X"]],
        [["O", "O"], ["O", "O"]],
        [
            ["X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X"],
        ],
    ]

    solvers = [
        ("Recursive DFS", solve_dfs),
        ("Iterative BFS", solve_bfs),
        ("Union-Find", solve_union_find),
    ]

    for idx, (board_in, expected) in enumerate(zip(tests, expected_outputs)):
        print(f"\n--- Test Case {idx + 1} ---")
        print("Input:")
        for row in board_in:
            print(" ".join(row))
        print("Expected Output:")
        for row in expected:
            print(" ".join(row))

        for name, solver in solvers:
            board_copy = copy.deepcopy(board_in)
            solver(board_copy)
            status = "PASS" if board_copy == expected else "FAIL"
            print(f"[{status}] {name}")
            if status == "FAIL":
                print("Got:")
                for row in board_copy:
                    print(" ".join(row))
