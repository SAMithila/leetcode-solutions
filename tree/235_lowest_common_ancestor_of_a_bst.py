"""
LeetCode 235 - Lowest Common Ancestor of a Binary Search Tree

Given a binary search tree (BST), find the lowest common ancestor (LCA) node
of two given nodes p and q in the BST.

The LCA is defined as the lowest node in the tree that has both p and q as
descendants (where a node can be a descendant of itself).

Example 1:
  Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
  Output: 6
  Explanation: The LCA of nodes 2 and 8 is 6.

Example 2:
  Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
  Output: 2
  Explanation: The LCA of nodes 2 and 4 is 2, since a node can be a
  descendant of itself according to the LCA definition.

Example 3:
  Input: root = [2,1], p = 2, q = 1
  Output: 2
"""
"""
## LC 235 — Lowest Common Ancestor of a BST (Interview Format)

---

### Step 1 — Understand & Restate

> "In a BST, left subtree values are smaller and right subtree values are
> larger than the current node. So the LCA of p and q is the first node
> we hit (walking down from the root) whose value falls *between* p and q
> (inclusive) — the point where p and q's paths from the root diverge."

```
Tree:
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5

p=2, q=8 → LCA = 6   (2 is in left subtree of 6, 8 is in right subtree)
p=2, q=4 → LCA = 2   (4 is a descendant of 2, so 2 is its own ancestor)
```

---

### Step 2 — Clarifying Questions

```
Q: Is it guaranteed p and q both exist in the tree?   → Yes
Q: Can p == q?                                        → Then LCA is that node itself
Q: Can a node be its own ancestor?                    → Yes, per problem definition
Q: Are all values unique?                              → Yes (BST constraint)
Q: Tree size?                                          → 2 to 10^5 nodes
Q: Is this guaranteed to be a valid BST (not just a
   general binary tree)?                              → Yes — that's what makes
                                                          the O(H) trick possible
```

---

### Step 3 — Brute Force → Optimal

**Brute Force — Find root-to-node paths for p and q, compare — O(n) time, O(n) space:**
> "Do a normal tree search (ignoring BST ordering) to record the full path
> of nodes from root to p, and root to q. Then walk both path lists in
> parallel and find the last point where they still match — that's the
> LCA. This works on ANY binary tree, not just a BST, but pays O(n) to
> build each path and O(n) extra space to store them."

**Optimal — Use BST ordering to steer a single walk — O(H) time, O(1) space:**
> "Since it's a BST, we don't need to search — we can compare p.val and
> q.val against the current node's value. If both are smaller, the LCA
> must be in the left subtree; if both are larger, it must be in the
> right subtree; the moment they're not both on the same side (one <=
> node <= other), we've found the split point — that node is the LCA.
> No need to store paths, no need for a stack in the iterative version."

---

### Step 4 — Edge Cases

```
1. p is an ancestor of q (or vice versa):  p=2, q=4  → LCA = 2 (self as ancestor)
2. p and q are on opposite sides of root:  p=2, q=8  → LCA = 6 (the root itself)
3. Two-node tree:                          root=[2,1], p=2, q=1 → LCA = 2
4. p == q:                                 LCA = p (trivially itself)
5. Skewed BST (essentially a linked list): LCA search degrades to O(n)
```

---

### Step 5 — Code (Optimal, iterative)

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node
```

---

### Step 6 — Dry Run

```
Tree:
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5

p=2, q=8

node=6: p(2) < 6 and q(8) > 6 → not both same side → return 6 ✓

p=2, q=4

node=6: p(2) < 6 and q(4) < 6 → both smaller → node = node.left = 2
node=2: p(2) < 2? No (equal) → not both smaller/larger → return 2 ✓
```

---

### Step 7 — Why This Works

> "BST ordering guarantees that at any node, everything in the left
> subtree is smaller and everything in the right subtree is larger. If
> both p and q are smaller than the current node, their LCA must live
> entirely within the left subtree — the current node can't be it, and
> neither can anything in the right subtree. Symmetric logic applies if
> both are larger. The instant p and q stop being on the same side (one
> is <= current <= other, including equality when the current node IS p
> or q), we've found the exact node where their ancestor paths diverge —
> that's the LCA, by definition the lowest shared ancestor."

---

### Step 8 — Complexity Analysis

**Time — O(H)**
```
Each step moves one level down the tree, either left or right.
Balanced BST: O(log n). Skewed BST: O(n).
```

**Space — O(1) iterative / O(H) recursive**
```
Iterative version uses no extra space beyond a pointer.
Recursive version pays O(H) for the call stack.
```

---

### Step 9 — Follow-up Questions & Answers

**Q: What if this were a general binary tree, not a BST?**
> "The value-comparison trick no longer applies since there's no
> ordering guarantee. Instead, do a single post-order DFS: recurse into
> left and right; if both sides return a non-null hit, the current node
> is the LCA; if exactly one side is non-null, propagate it up. This is
> LeetCode 236 and still runs in O(n) time, O(H) space, but requires
> visiting the whole tree since we can't prune based on value order."

**Q: What if we needed LCA for many pairs of nodes, repeatedly, on a
static tree?**
> "Precompute parent pointers and depths for every node in one O(n)
> pass, then use binary lifting (sparse ancestor table) to answer each
> LCA query in O(log n) after O(n log n) preprocessing. Useful when
> there are many queries (e.g., Q queries) since it beats O(H) per query
> re-walks when Q is large and H is large."

**Q: What if each node had a pointer to its parent?**
> "Walk up from p, recording all its ancestors in a set. Then walk up
> from q until we hit a node already in that set — that's the LCA. O(H)
> time, O(H) space for the ancestor set, no need to start from the root
> at all."

---

### Recap Card

```
Problem type:   BST / Ancestor Search
Pattern:        Use BST ordering to steer a single top-down walk
Key trick:      LCA = the node where p and q stop being on the same side

Time:    O(H)  — one pass down the tree
Space:   O(1) iterative, O(H) recursive

Alternatives:
  Brute force (root-to-node paths):  O(n) time, O(n) space (works on any tree)
  General binary tree (LC 236):      O(n) time, O(H) space (post-order DFS)
  Repeated queries (binary lifting): O(n log n) preprocess, O(log n) per query
  Parent pointers given:             O(H) time, O(H) space (ancestor set walk-up)

Edge cases:
  → p or q equals the current node       → that node is the LCA (self-ancestor)
  → p, q on opposite sides of a node     → that node is the LCA
  → skewed BST                           → degrades to O(n)
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
# Approach 1: Brute Force — Root-to-node paths, compare — works on any binary tree
# Time:  O(n) — searching for p and q each visits up to n nodes
# Space: O(n) — stores full root-to-node path for both p and q
# ─────────────────────────────────────────────
def lowestCommonAncestor_bruteforce(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    def find_path(node: Optional[TreeNode], target: TreeNode, path: list) -> bool:
        if not node:
            return False

        path.append(node)
        if node is target:
            return True

        if find_path(node.left, target, path) or find_path(node.right, target, path):
            return True

        path.pop()
        return False

    path_p: list = []
    path_q: list = []
    find_path(root, p, path_p)
    find_path(root, q, path_q)

    lca = None
    for node_p, node_q in zip(path_p, path_q):
        if node_p is not node_q:
            break
        lca = node_p
    return lca


# ─────────────────────────────────────────────
# Approach 2: Iterative BST Walk — Optimal
# Time:  O(H) — one pass down the tree, steered by BST ordering
# Space: O(1) — just a pointer, no stack/recursion
# ─────────────────────────────────────────────
def lowestCommonAncestor_iterative(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node
    return None


# ─────────────────────────────────────────────
# Approach 3: Recursive BST Walk
# Time:  O(H) — one path down the tree
# Space: O(H) — recursion call stack
# ─────────────────────────────────────────────
def lowestCommonAncestor_recursive(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    if not root:
        return None

    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor_recursive(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestor_recursive(root.right, p, q)
    return root


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Iterative BST Walk)
# O(H) time | O(1) space
# ─────────────────────────────────────────────
lowestCommonAncestor = lowestCommonAncestor_iterative


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


def find_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    node = root
    while node and node.val != val:
        node = node.left if val < node.val else node.right
    return node


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8, 6),
        ([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4, 2),
        ([2, 1], 2, 1, 2),
        ([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 0, 5, 2),
        ([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 7, 9, 8),
    ]

    solvers = [
        ("Brute Force (paths)", lowestCommonAncestor_bruteforce),
        ("Iterative BST Walk (optimal)", lowestCommonAncestor_iterative),
        ("Recursive BST Walk", lowestCommonAncestor_recursive),
    ]

    for arr, p_val, q_val, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            p_node = find_node(tree, p_val)
            q_node = find_node(tree, q_val)
            out = fn(tree, p_node, q_node)
            got = out.val if out else None
            status = "PASS" if got == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr}, p={p_val}, q={q_val} | got={got}")
