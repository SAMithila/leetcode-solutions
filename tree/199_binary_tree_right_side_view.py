"""
LeetCode 199 - Binary Tree Right Side View

Given the root of a binary tree, imagine yourself standing on the right side of it,
return the values of the nodes you can see ordered from top to bottom.

Example 1:
  Input: root = [1,2,3,null,5,null,4]
  Output: [1,3,4]

Example 2:
  Input: root = [1,null,3]
  Output: [1,3]

Example 3:
  Input: root = []
  Output: []
"""
"""
## LC 199 — Binary Tree Right Side View (Interview Format)

---

### Step 1 — Understand & Restate

> "Imagine standing on the right side of a binary tree. Return the values of the nodes you can see from top to bottom. Visually, this means returning the rightmost node at each depth level of the tree."

```
Tree:
        1          <-- depth 0: sees 1
       / \
      2   3        <-- depth 1: sees 3
       \   \
        5   4      <-- depth 2: sees 4

Output: [1, 3, 4]
```

---

### Step 2 — Clarifying Questions

```
Q: Can the root be null?                    → Yes → return []
Q: What if the left subtree is deeper?      → We will see the left nodes once they protrude past the right subtree.
   For example:
        1
       / \
      2   3
     /
    4                                       → [1, 3, 4]
Q: Can values be negative?                  → Yes
Q: Return node values or nodes?             → Node values in a list
```

---

### Step 3 — Brute Force → Optimal

**BFS Level-Order Traversal — O(n) time, O(w) space:**
> "A simple way is to perform a level-order traversal (BFS) using a queue. At each level, we capture the value of the last node in the level (the rightmost node) and add it to our result. This is extremely intuitive but requires O(w) extra space for the queue, where w is the maximum width of the tree."

**DFS (Root-Right-Left) — O(n) time, O(h) space:**
> "To optimize the space complexity in a deep but narrow tree, we can use a DFS traversal where we visit the right child before the left child (Root-Right-Left).
By doing this, the first node we visit at any given depth will always be the rightmost node of that level. We can detect this by checking if the current depth equals the length of our result list. If it does, this is the first time we've reached this depth, so we add the node's value."

---

### Step 4 — Edge Cases

```
1. Empty tree:         root=None            → []
2. Single node:        root=[1]             → [1]
3. Left-skewed tree:   all nodes on left    → we see all of them: [1, 2, 3]
        1
       /
      2
     /
    3
4. Right-skewed tree:  all nodes on right   → we see all of them: [1, 2, 3]
5. Left side is deeper than right:
        1
       / \
      2   3
     /
    4                                       → [1, 3, 4] (4 is visible because it's the rightmost at level 2)
```

---

### Step 5 — Code

```python
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        result = []
        
        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            
            # If this is the first time we've visited this depth level,
            # it must be the rightmost node since we visit right before left.
            if depth == len(result):
                result.append(node.val)
            
            # Visit right child first, then left child
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)
            
        dfs(root, 0)
        return result
```

---

### Step 6 — Dry Run

```
Tree:
        1
       / \
      2   3
       \   \
        5   4

dfs(1, 0):
  depth = 0 == len(result) (0) → result = [1]
  dfs(3, 1):
    depth = 1 == len(result) (1) → result = [1, 3]
    dfs(4, 2):
      depth = 2 == len(result) (2) → result = [1, 3, 4]
      dfs(None, 3) → return
      dfs(None, 3) → return
    dfs(None, 2) → return
  dfs(2, 1):
    depth = 1 != len(result) (3) → do not append
    dfs(5, 2):
      depth = 2 != len(result) (3) → do not append
      dfs(None, 3) → return
      dfs(None, 3) → return
    dfs(None, 2) → return

Result: [1, 3, 4]  ✓
```

---

### Step 7 — Why Right-Before-Left DFS Works

> "The core insight is the order of traversal. By recursing on node.right before node.left, our search path hugs the right side of the tree. The condition depth == len(result) acts as a sentinel. Since len(result) starts at 0 and grows by 1 every time we add a node, we will only add one node per level. Because we traverse right-side first, that node is guaranteed to be the rightmost node at that depth level."

---

### Step 8 — Complexity Analysis

**Time — O(n)**
```
We visit every node in the tree exactly once.
Each visit performs O(1) checks and operations.
Total Time: O(n).
```

**Space — O(h)**
```
The space is determined by the recursion call stack, which is proportional to the height of the tree.
- Balanced tree: O(log n)
- Skewed tree: O(n) (worst case)
We do not use any additional data structures other than the output array.
```

---

### Step 9 — Follow-up Questions & Answers

**Q: How would you solve this with BFS?**
> "We can traverse level-by-level using a queue. At the end of each level (when processing the last node in the for _ in range(level_size) loop), we append that node's value to the result list."

```python
class Solution:
    def rightSideView_bfs(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.popleft()
                if i == level_size - 1:  # Rightmost node at this level
                    result.append(node.val)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
        return result
```

**Q: What if we wanted the left side view instead?**
> "Two simple ways: Either use BFS and capture the first node (i == 0) of each level, or use DFS traversing left-before-right (node.left before node.right) and keep the depth == len(result) check."

---

### Recap Card

```
Problem type:   Binary Tree View / Traversal
Pattern:        DFS (Root-Right-Left) with depth tracking
Key trick:      Visit right child first, append to result when depth == len(result)

Time:    O(n)   — visits every node once
Space:   O(h)   — stack depth (O(log n) average, O(n) worst)

Alternative:
  BFS level-order traversal, append the last element of each level.
  BFS Space: O(w) where w is max width.

Edge cases:
  → empty tree             → []
  → left subtree deeper    → left nodes correctly show at lower depths
  → skewed tree            → behaves like a list, visits all nodes
```
"""

from typing import Optional, List
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Recursive DFS (Root-Right-Left) - Optimal / Most Idiomatic
# Time:  O(n) — visits each node exactly once
# Space: O(h) — recursion stack depth up to tree height (h)
# ─────────────────────────────────────────────
def rightSideView_recursive(root: Optional[TreeNode]) -> List[int]:
    result = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        # If this is the first time we've visited this depth level,
        # it must be the rightmost node since we visit right before left.
        if depth == len(result):
            result.append(node.val)

        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result


# ─────────────────────────────────────────────
# Approach 2: Iterative BFS (Level-Order with Queue)
# Time:  O(n) — visits each node exactly once
# Space: O(w) — queue holds up to max level width (w)
# ─────────────────────────────────────────────
def rightSideView_bfs(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()

            # If it's the last node of the current level, it's visible from the right
            if i == level_size - 1:
                result.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result


# ─────────────────────────────────────────────
# Approach 3: Iterative DFS (Root-Right-Left with Stack)
# Time:  O(n) — visits each node exactly once
# Space: O(h) — stack depth up to tree height (h)
# ─────────────────────────────────────────────
def rightSideView_iterative_dfs(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []

    result = []
    stack = [(root, 0)]  # (node, depth)

    while stack:
        node, depth = stack.pop()

        if depth == len(result):
            result.append(node.val)

        # Push left first so that right is popped first (LIFO)
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return result


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Recursive DFS)
# O(n) time | O(h) space
# ─────────────────────────────────────────────
rightSideView = rightSideView_recursive


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
        ([1, 2, 3, None, 5, None, 4], [1, 3, 4]),
        ([1, None, 3], [1, 3]),
        ([], []),
        ([1, 2, 3, 4], [1, 3, 4]),
        ([1, 2, 3, 4, None, None, None, 5], [1, 3, 4, 5]),
    ]

    solvers = [
        ("Recursive DFS", rightSideView_recursive),
        ("Iterative BFS", rightSideView_bfs),
        ("Iterative DFS", rightSideView_iterative_dfs),
    ]

    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
