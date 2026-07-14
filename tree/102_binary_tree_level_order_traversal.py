"""
LeetCode 102 - Binary Tree Level Order Traversal

Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

Example 1:
  Input: root = [3,9,20,null,null,15,7]
  Output: [[3],[9,20],[15,7]]

Example 2:
  Input: root = [1]
  Output: [[1]]

Example 3:
  Input: root = []
  Output: []
"""
""" ## LC 102 — Binary Tree Level Order Traversal (Interview Format)

---

### Step 1 — Understand & Restate

> "Given the root of a binary tree, return the values of nodes level by level — left to right, one level at a time. The output is a list of lists, where each inner list contains all values at that depth."

```
Tree:
        3
       / \
      9  20
         / \
        15   7

Output: [[3], [9,20], [15,7]]
```

---

### Step 2 — Clarifying Questions

```
Q: Can root be null?                  → Yes → return []
Q: Single node tree?                  → Yes → return [[root.val]]
Q: Is output order left to right?     → Yes, always left before right
Q: Can values be negative?            → Yes
Q: Return node values or nodes?       → Just the values
```

---

### Step 3 — Brute Force → Optimal

> "Level order traversal is naturally a BFS problem — BFS processes nodes level by level which is exactly what we need. There's no brute force that's meaningfully different here. DFS could work too but requires tracking depth explicitly. BFS is the clean, natural fit."

```
BFS with a queue:
  - Process ALL nodes at current level before moving to next
  - Key trick: snapshot len(queue) at the START of each level
    → this tells you exactly how many nodes belong to this level
    → process exactly that many, then start the next level
```

---

### Step 4 — Edge Cases

```
1. Empty tree:          root=None             → []
2. Single node:         root=[1]              → [[1]]
3. Complete binary tree: all levels full      → works naturally
4. Skewed left tree:
        1
       /
      2
     /
    3                                         → [[1],[2],[3]]
5. Skewed right tree:   same as above mirrored
6. All same values:     [1,1,1,1]             → groups correctly by level
```

---

### Step 5 — Code

```python
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue  = deque([root])

        while queue:
            level_size = len(queue)    # how many nodes are at this level
            level      = []

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)

                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)

            result.append(level)

        return result
```

---

### Step 6 — Dry Run

```
Tree:       3
           / \
          9  20
             / \
            15   7

Initial: queue=[3], result=[]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level 1:
  level_size = 1
  pop 3  → level=[3]
           push 9, push 20
           queue=[9,20]
  result=[[3]]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level 2:
  level_size = 2
  pop 9  → level=[9]
           9 has no children, nothing pushed
  pop 20 → level=[9,20]
           push 15, push 7
           queue=[15,7]
  result=[[3],[9,20]]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level 3:
  level_size = 2
  pop 15 → level=[15]
           no children
  pop 7  → level=[15,7]
           no children
           queue=[]
  result=[[3],[9,20],[15,7]]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
queue is empty → while loop ends
return [[3],[9,20],[15,7]]  ✓
```

---

### Step 7 — Why `level_size = len(queue)` is the key line

```python
level_size = len(queue)
for _ in range(level_size):
    ...
```

> "This is the most important line. At the start of each iteration, the queue contains EXACTLY the nodes for the current level. We snapshot that count before adding any children. Then we process exactly that many nodes — no more, no less. Children added during the loop belong to the NEXT level and won't be processed until the next iteration."

```
queue before level 2:  [9, 20]      ← level_size = 2
  pop 9  → add nothing
  pop 20 → add 15, 7
queue after level 2:   [15, 7]      ← ready for level 3

Without level_size snapshot:
  len(queue) changes as we add children mid-loop
  → we'd accidentally process level 3 nodes in level 2's loop
```

---

### Step 8 — Complexity Analysis

**Time — O(n)**

```
Every node is:
  - pushed into queue exactly once  → O(1)
  - popped from queue exactly once  → O(1)
  - appended to level list once     → O(1)

n nodes × O(1) each = O(n) total
```

**Space — O(n)**

```
queue holds at most one full level at a time.
Widest level in a perfect binary tree = n/2 nodes (bottom level).
So queue size = O(n/2) = O(n).

result list stores all n values = O(n).

Total space = O(n).
```

---

### Step 9 — Follow-up Questions & Answers

**Q: Can you do level order traversal with DFS instead?**

```python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []

        def dfs(node, depth):
            if not node:
                return
            if depth == len(result):       # first time at this depth
                result.append([])
            result[depth].append(node.val)
            dfs(node.left,  depth + 1)
            dfs(node.right, depth + 1)

        dfs(root, 0)
        return result
```

> "Yes — DFS works by tracking the depth of each node. When we visit a node at a new depth for the first time, we create a new inner list. O(n) time, O(h) space for the call stack instead of O(n) for the queue."

---

**Q: What if you needed right to left level order?**

> "Two options — either reverse each inner list before appending, or use `appendleft` on a deque for the result. Both O(n)."

```python
result.append(level[::-1])   # reverse each level
```

---

**Q: What if you needed bottom-up level order (LC 107)?**

> "Same exact code — just reverse the final result at the end."

```python
return result[::-1]
```

---

### Recap Card

```
Problem type:   BFS — Level Order Traversal
Data structure: Queue (deque)
Key trick:      Snapshot len(queue) before processing
                each level to know exactly how many
                nodes belong to current level

Time:    O(n)  — every node visited once
Space:   O(n)  — queue holds widest level (up to n/2 nodes)

Variants:
  LC 107 → bottom-up    → reverse final result
  LC 103 → zigzag       → alternate left/right each level
  LC 199 → right side   → take last element of each level

Edge cases:
  → empty tree     → return []
  → single node    → return [[val]]
  → skewed tree    → each level has exactly 1 node

Most common mistake:
  → forgetting level_size snapshot
  → processing children in same level as parents
``` """

from typing import Optional, List
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Iterative BFS (Level-Order with Queue) - Optimal / Most Idiomatic
# Time:  O(n) — visits each node exactly once
# Space: O(n) — queue holds up to n/2 nodes (last level of a complete tree)
# ─────────────────────────────────────────────
def levelOrder_bfs(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


# ─────────────────────────────────────────────
# Approach 2: Recursive DFS (Pre-Order with Level Tracking)
# Time:  O(n) — visits each node exactly once
# Space: O(h) — recursion stack depth up to tree height (h)
#               (result list uses O(n) additional space for output)
# ─────────────────────────────────────────────
def levelOrder_dfs(root: Optional[TreeNode]) -> List[List[int]]:
    result = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        # If visiting this depth for the first time, create a new level list
        if depth == len(result):
            result.append([])

        result[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result


# ─────────────────────────────────────────────
# Approach 3: Iterative DFS (Pre-Order with Stack + Level Tracking)
# Time:  O(n) — visits each node exactly once
# Space: O(h) — stack depth up to tree height (h)
# ─────────────────────────────────────────────
def levelOrder_iterative_dfs(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    result = []
    stack = [(root, 0)]  # (node, depth)

    while stack:
        node, depth = stack.pop()

        if depth == len(result):
            result.append([])

        result[depth].append(node.val)

        # Push right first so that left is processed first (LIFO)
        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return result


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Iterative BFS)
# O(n) time | O(n) space
# ─────────────────────────────────────────────
levelOrder = levelOrder_bfs


# ─── Helper for Testing ───────────────────────
def build_tree(arr: list) -> Optional[TreeNode]:
    if not arr:
        return None
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    while i < len(arr):
        curr = queue.popleft()
        if curr is not None:
            if i < len(arr) and arr[i] is not None:
                curr.left = TreeNode(arr[i])
                queue.append(curr.left)
            else:
                curr.left = None
            i += 1
            if i < len(arr) and arr[i] is not None:
                curr.right = TreeNode(arr[i])
                queue.append(curr.right)
            else:
                curr.right = None
            i += 1
    return root


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
        ([1], [[1]]),
        ([], []),
        ([1, 2, 3, 4, 5], [[1], [2, 3], [4, 5]]),
        ([1, None, 2, None, 3], [[1], [2], [3]]),
    ]

    solvers = [
        ("Iterative BFS", levelOrder_bfs),
        ("Recursive DFS", levelOrder_dfs),
        ("Iterative DFS", levelOrder_iterative_dfs),
    ]

    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
