"""
LeetCode 1448 - Count Good Nodes in Binary Tree

Given a binary tree root, a node X in the tree is named good if in the path
from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree.

Example 1:
  Input: root = [3,1,4,3,null,1,5]
  Output: 4
  Explanation: Nodes in blue are good.
    Root Node (3) is always a good node.
    Node 4 -> (3,4) is the maximum value in the path starting from the root.
    Node 5 -> (3,4,5) is the maximum value in the path starting from the root.
    Node 3 -> (3,1,3) is the maximum value in the path starting from the root.

Example 2:
  Input: root = [3,3,null,4,2]
  Output: 3
  Explanation: Node 2 -> (3,3,2) is not good, because "3" is higher.

Example 3:
  Input: root = [1]
  Output: 1
"""
"""
## LC 1448 — Count Good Nodes in Binary Tree (Interview Format)

---

### Step 1 — Understand & Restate

> "A node is 'good' if no ancestor on the path from the root down to it (including
> the node itself) has a strictly greater value. I need to count how many nodes in
> the whole tree satisfy this."

```
Tree:
        3
       / \
      1   4
       \  / \
       3 1   5

Path to node 4:   [3,4]     max so far = 3 → 4 >= 3      → good
Path to node 5:   [3,4,5]   max so far = 4 → 5 >= 4      → good
Path to left 3:   [3,1,3]   max so far = 3 → 3 >= 3      → good (ties count as good)
Path to 1 (child of 4): [3,4,1]  max so far = 4 → 1 < 4  → not good

Good nodes: 3(root), 4, 5, 3  → Output: 4
```

---

### Step 2 — Clarifying Questions

```
Q: Does the root always count as good?          → Yes, trivially (empty path, no ancestor exceeds it)
Q: Are ties good or bad?                        → Good — "no nodes greater than X" allows equal values
Q: Can values be negative?                      → Yes, -4*10^4 to 4*10^4
Q: Tree size?                                   → 1 to 5*10^4 nodes
Q: Is "path" root-to-node only, or any path?    → Root-to-node only (downward path)
```

---

### Step 3 — Brute Force → Optimal

**Brute Force — For each node, re-walk the path from root — O(n²) worst case**

```python
# for every node, search from root down to it, tracking the max along the way
def is_good(root, target):
    def find_max_to(node, path_max):
        if node is target:
            return path_max <= node.val
        ...  # search both subtrees, carrying path_max down
```

> "This recomputes the root-to-node path for every single node, which is wasteful —
> O(n) work per node, O(n²) total on a skewed tree."

**Optimal — Single DFS, carry the running max down as a parameter — O(n)**

```
Do one traversal. Pass down max_so_far (the largest value seen on the path from
the root to the current node's parent). At each node:
  - if node.val >= max_so_far: it's good, count it
  - recurse into children with max(max_so_far, node.val)

Each node is visited exactly once → O(n) total.
```

---

### Step 4 — Edge Cases

```
1. Single node:              root=[1]              → 1 (root always good)
2. Strictly increasing path: root=[1,null,2,null,3] → 3 (every node is a new max)
3. Strictly decreasing path: root=[3,null,2,null,1] → 1 (only root is good)
4. All equal values:         root=[2,2,2]          → 3 (ties count as good)
5. Negative values:          root=[-1,-2,null]     → 2 (-2 >= -1 is false... wait: -2 < -1 → not good)
                              → actually root=[-1,-2] → only root good → 1
```

---

### Step 5 — Code

```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, max_so_far):
            if not node:
                return 0

            count = 1 if node.val >= max_so_far else 0
            new_max = max(max_so_far, node.val)

            count += dfs(node.left, new_max)
            count += dfs(node.right, new_max)
            return count

        return dfs(root, float('-inf'))
```

---

### Step 6 — Dry Run

```
Tree:
        3
       / \
      1   4
       \  / \
       3 1   5

dfs(3, -inf): 3 >= -inf → count=1, new_max=3
  dfs(1, 3):  1 >= 3? No → count=0, new_max=3
    dfs(None, 3): 0
    dfs(3, 3):  3 >= 3? Yes → count=1, new_max=3
      dfs(None,3)=0, dfs(None,3)=0
      returns 1
    returns 0 + 0 + 1 = 1
  dfs(4, 3):  4 >= 3? Yes → count=1, new_max=4
    dfs(1, 4): 1 >= 4? No → count=0
      returns 0
    dfs(5, 4): 5 >= 4? Yes → count=1
      returns 1
    returns 1 + 0 + 1 = 2
  total = 1 (root) + 1 (left subtree) + 2 (right subtree) = 4 ✓
```

---

### Step 7 — Complexity Analysis

**Time — O(n)**
```
Each node is visited exactly once, doing O(1) work per node.
```

**Space — O(H)**
```
Recursion call stack depth equals tree height.
Balanced tree: O(log n). Skewed tree: O(n).
```

---

### Step 8 — Follow-up Questions & Answers

**Q: How would you solve this iteratively to avoid recursion limits?**
> "Use an explicit stack holding (node, max_so_far) pairs instead of relying on the
> call stack. Same O(n) time, O(H) space, but avoids Python's recursion depth limit
> on very deep/skewed trees."

**Q: What if the tree could be huge and we needed O(1) extra space?**
> "Morris-style traversal could work in principle by threading pointers, but
> propagating 'max_so_far' down through Morris links is significantly more complex
> since Morris traversal is designed for in-order sequencing, not top-down state
> passing — it's not a natural fit here. In practice O(H) recursion/stack space is
> already efficient and acceptable for this problem's constraints."

**Q: What if we wanted to return the list of good node values, not just the count?**
> "Same DFS, but append node.val to a results list instead of incrementing a
> counter when the good-node condition holds."

---

### Recap Card

```
Problem type:   Binary Tree DFS / Path Aggregation
Pattern:        Carry running state (max-so-far) down the recursion
Key trick:      A node is good iff node.val >= max of all ancestors (ties count)

Time:    O(n)  — every node visited once
Space:   O(H)  — recursion stack, H = tree height

Edge cases:
  → root always good (empty ancestor path)
  → ties count as good (>=, not >)
  → strictly decreasing path → only root is good
```
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Brute Force — Re-walk root-to-node path for every node
# Time:  O(n^2) worst case (skewed tree) — O(n) search per node, n nodes
# Space: O(H) recursion stack per search
# ─────────────────────────────────────────────
def goodNodes_bruteforce(root: Optional[TreeNode]) -> int:
    def max_on_path_to(node: Optional[TreeNode], target: TreeNode, path_max: int):
        """Returns the max value on the path from `node` down to `target`, or None if not found."""
        if not node:
            return None
        if node is target:
            return max(path_max, node.val)

        left = max_on_path_to(node.left, target, max(path_max, node.val))
        if left is not None:
            return left
        return max_on_path_to(node.right, target, max(path_max, node.val))

    def collect_nodes(node: Optional[TreeNode]):
        if not node:
            return []
        return [node] + collect_nodes(node.left) + collect_nodes(node.right)

    count = 0
    for node in collect_nodes(root):
        path_max = max_on_path_to(root, node, float("-inf"))
        if node.val >= path_max:
            count += 1
    return count


# ─────────────────────────────────────────────
# Approach 2: Recursive DFS carrying max-so-far — Optimal
# Time:  O(n) — each node visited once
# Space: O(H) — recursion call stack
# ─────────────────────────────────────────────
def goodNodes_dfs(root: Optional[TreeNode]) -> int:
    def dfs(node: Optional[TreeNode], max_so_far: float) -> int:
        if not node:
            return 0

        count = 1 if node.val >= max_so_far else 0
        new_max = max(max_so_far, node.val)

        count += dfs(node.left, new_max)
        count += dfs(node.right, new_max)
        return count

    return dfs(root, float("-inf"))


# ─────────────────────────────────────────────
# Approach 3: Iterative DFS with Explicit Stack
# Time:  O(n) — each node visited once
# Space: O(H) — stack holds one root-to-leaf path at a time
# ─────────────────────────────────────────────
def goodNodes_iterative(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    count = 0
    stack = [(root, float("-inf"))]

    while stack:
        node, max_so_far = stack.pop()

        if node.val >= max_so_far:
            count += 1
        new_max = max(max_so_far, node.val)

        if node.left:
            stack.append((node.left, new_max))
        if node.right:
            stack.append((node.right, new_max))

    return count


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Recursive DFS)
# O(n) time | O(H) space
# ─────────────────────────────────────────────
goodNodes = goodNodes_dfs


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
        ([3, 1, 4, 3, None, 1, 5], 4),
        ([3, 3, None, 4, 2], 3),
        ([1], 1),
        ([1, None, 2, None, 3], 3),
        ([3, None, 2, None, 1], 1),
        ([2, 2, 2], 3),
        ([-1, -2], 1),
    ]

    solvers = [
        ("Brute Force",           goodNodes_bruteforce),
        ("Recursive DFS (opt.)",  goodNodes_dfs),
        ("Iterative DFS",         goodNodes_iterative),
    ]

    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
