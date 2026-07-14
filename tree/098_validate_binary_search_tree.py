"""
LeetCode 98 - Validate Binary Search Tree

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

Example 1:
  Input: root = [2,1,3]
  Output: true

Example 2:
  Input: root = [5,1,4,null,null,3,6]
  Output: false
  Explanation: The root node's value is 5, but its right child's value is 4.
"""
"""
## LC 98 — Validate Binary Search Tree (Interview Format)

---

### Step 1 — Understand & Restate

> "Given the root of a binary tree, determine if it is a valid Binary Search Tree. A valid BST means every node's value must be strictly greater than all values in its left subtree and strictly less than all values in its right subtree — and this must hold for every node, not just immediate children."

```
Valid BST ✓              Invalid BST ✗
      5                        5
     / \                      / \
    3   7                    3   7
   / \ / \                  / \ / \
  2  4 6  8                2  4 6  4
                                    ↑
                               4 < 5 but sits
                               in right subtree!
```

> "The tricky part — it's not enough to check each node against its direct parent. Every node has a valid range it must fall within, defined by ALL its ancestors."

---

### Step 2 — Clarifying Questions

```
Q: Can the tree be empty (root=None)?    → Yes → return True
Q: Can values be negative?               → Yes
Q: Can values be duplicates?             → No — BST requires STRICT inequality
Q: What range are values in?             → -2^31 to 2^31-1 (32-bit integer)
Q: Is it guaranteed to be a binary tree? → Yes
```

---

### Step 3 — Brute Force → Optimal

**Wrong naive approach — only check parent vs child:**

```python
# ❌ THIS IS WRONG
def isValidBST(root):
    if not root: return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return isValidBST(root.left) and isValidBST(root.right)
```

This fails on:

```
      5
     / \
    1   4
       / \
      3   6

Node 4's children (3,6) look fine locally.
But 4 < 5 — the whole right subtree is wrong!
Local check can't catch this.
```

**Why we need a valid range per node:**

```
Every node has a (min, max) range it must stay within.

        5         range: (-inf, +inf)
       / \
      3   7       3 range: (-inf, 5)    7 range: (5, +inf)
     / \ / \
    2  4 6  8     2: (-inf,3)  4: (3,5)  6: (5,7)  8: (7,+inf)

As you go LEFT  → upper bound tightens (current node becomes new max)
As you go RIGHT → lower bound tightens (current node becomes new min)
```

---

### Step 4 — Edge Cases

```
1. Empty tree:          root=None              → True
2. Single node:         root=[1]               → True
3. Classic trick:
        5
       / \
      1   4
         / \
        3   6                                  → False (4 < 5)

4. Duplicate values:    [1,1] or [2,2,2]       → False (strict inequality)
5. Integer boundaries:  node.val = -2^31       → need float('-inf') as min bound
6. Left skewed tree:    valid if strictly decreasing
7. Right skewed tree:   valid if strictly increasing
```

---

### Step 5 — Code

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        def validate(node, min_val, max_val) -> bool:
            # base case — null node is always valid
            if not node:
                return True

            # current node must be strictly within (min_val, max_val)
            if node.val <= min_val or node.val >= max_val:
                return False

            # go left  → node becomes new upper bound (max)
            # go right → node becomes new lower bound (min)
            left_valid  = validate(node.left,  min_val,   node.val)
            right_valid = validate(node.right, node.val,  max_val)

            return left_valid and right_valid

        return validate(root, float('-inf'), float('inf'))
```

---

### Step 6 — Dry Run

```
Tree:       5
           / \
          3   7
         / \ / \
        2  4 6  8

validate(5, -inf, +inf)
  5 > -inf and 5 < +inf ✓
  → validate(3, -inf, 5)
      3 > -inf and 3 < 5 ✓
      → validate(2, -inf, 3)
          2 > -inf and 2 < 3 ✓
          → validate(None) → True
          → validate(None) → True
          → True
      → validate(4, 3, 5)
          4 > 3 and 4 < 5 ✓
          → validate(None) → True
          → validate(None) → True
          → True
      → True and True → True
  → validate(7, 5, +inf)
      7 > 5 and 7 < +inf ✓
      → validate(6, 5, 7)
          6 > 5 and 6 < 7 ✓ → True
      → validate(8, 7, +inf)
          8 > 7 and 8 < +inf ✓ → True
      → True
  → True and True → True ✓
```

Now the failing case:

```
Tree:       5
           / \
          1   4
             / \
            3   6

validate(5, -inf, +inf) ✓
  → validate(1, -inf, 5) ✓
  → validate(4, 5, +inf)
      4 > 5? NO → return False ✗

return False ✓  (correctly caught!)
```

---

### Step 7 — Complexity Analysis

**Time — O(n)**

```
Every node visited exactly once.
At each node we do O(1) work (one comparison).
n nodes × O(1) = O(n)
Early exit the moment any node fails its range check.
```

**Space — O(h)**

```
Recursion call stack holds at most h frames.

Balanced tree → h = O(log n)
Skewed tree   → h = O(n)      ← worst case

No extra data structures used.
```

---

### Step 8 — Follow-up Questions & Answers

**Q: Can you solve it using inorder traversal?**

> "Yes — inorder traversal of a valid BST always produces a strictly increasing sequence. So we do inorder traversal and check that each value is strictly greater than the previous one."

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        self.prev = float('-inf')

        def inorder(node) -> bool:
            if not node:
                return True
            if not inorder(node.left):
                return False          # left subtree invalid
            if node.val <= self.prev:
                return False          # not strictly increasing
            self.prev = node.val
            return inorder(node.right)

        return inorder(root)
```

> "Same O(n) time, O(h) space. The range-based approach is cleaner and more explicit — I prefer it in interviews because it directly encodes the BST definition."

---

**Q: Why float('-inf') and float('inf') instead of None?**

> "We need actual comparable values to check `node.val > min_val`. If we used None we'd need extra null checks everywhere. float('-inf') and float('inf') work as universal lower and upper bounds that any integer value will satisfy."

---

**Q: Why strict inequality (`<` and `>`) and not `<=` or `>=`?**

> "BST requires strictly greater and strictly less than — duplicates are not allowed. So a node equal to its bound is invalid. If the problem allowed duplicates, we'd relax to `<=` or `>=`."

---

### Recap Card

```
Problem type:   Tree DFS with valid range tracking
Pattern:        Pass (min, max) bounds down through recursion
Key insight:    Each node's valid range is determined by ALL
                ancestors, not just immediate parent

Time:    O(n)   — every node visited once
Space:   O(h)   — recursion stack depth

Two valid approaches:
  1. Range validation  → pass (min,max) bounds top-down
  2. Inorder traversal → check strictly increasing sequence

Edge cases:
  → empty tree             → True
  → single node            → True
  → duplicate values       → False (strict inequality)
  → node equal to ancestor → False (most common mistake)
  → integer min/max values → use float('-inf/+inf')

Most common mistake:
  → only checking node vs direct parent
  → missing that subtree must respect ALL ancestor bounds
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
# Approach 1: Recursive DFS (Range Boundaries) - Optimal / Most Idiomatic
# Time:  O(n) — visits each node exactly once
# Space: O(h) — recursion stack depth up to tree height (h)
# ─────────────────────────────────────────────
def isValidBST_recursive_range(root: Optional[TreeNode]) -> bool:
    def validate(node: Optional[TreeNode], low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)

    return validate(root, float('-inf'), float('inf'))


# ─────────────────────────────────────────────
# Approach 2: Iterative DFS (In-Order Traversal)
# Time:  O(n) — visits each node up to once
# Space: O(h) — stack depth up to tree height (h)
# ─────────────────────────────────────────────
def isValidBST_inorder_iterative(root: Optional[TreeNode]) -> bool:
    stack = []
    curr = root
    prev = None

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        # In a valid BST, the in-order traversal values must be strictly increasing.
        if prev is not None and curr.val <= prev:
            return False
        prev = curr.val
        curr = curr.right

    return True


# ─────────────────────────────────────────────
# Approach 3: Recursive DFS (In-Order Traversal)
# Time:  O(n) — visits each node up to once
# Space: O(h) — recursion stack depth up to tree height (h)
# ─────────────────────────────────────────────
def isValidBST_inorder_recursive(root: Optional[TreeNode]) -> bool:
    prev = None

    def inorder(node: Optional[TreeNode]) -> bool:
        nonlocal prev
        if not node:
            return True

        if not inorder(node.left):
            return False

        if prev is not None and node.val <= prev:
            return False
        prev = node.val

        return inorder(node.right)

    return inorder(root)


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Recursive DFS with Range Boundaries)
# O(n) time | O(h) space
# ─────────────────────────────────────────────
isValidBST = isValidBST_recursive_range


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
        ([2, 1, 3], True),
        ([5, 1, 4, None, None, 3, 6], False),
        ([], True),
        ([1], True),
        ([2, 2, 2], False),
        ([1, 1], False),
        ([10, 5, 15, None, None, 6, 20], False),  # 6 is on the right of 10 but must be > 10
    ]

    solvers = [
        ("Recursive Range DFS", isValidBST_recursive_range),
        ("Iterative In-Order DFS", isValidBST_inorder_iterative),
        ("Recursive In-Order DFS", isValidBST_inorder_recursive),
    ]

    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
