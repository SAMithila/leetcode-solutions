"""
LeetCode 230 - Kth Smallest Element in a BST

Given the root of a binary search tree, and an integer k, return the kth
smallest value (1-indexed) of all the values of the nodes in the tree.

Example 1:
  Input: root = [3,1,4,null,2], k = 1
  Output: 1

Example 2:
  Input: root = [5,3,6,2,4,null,null,1], k = 3
  Output: 3

Follow up: If the BST is modified often (insert/delete) and you need to
find the kth smallest frequently, how would you optimize?
"""
"""
## LC 230 — Kth Smallest Element in a BST (Interview Format)

---

### Step 1 — Understand & Restate

> "A BST's in-order traversal visits nodes in strictly ascending order.
> So the kth smallest element is simply the kth value produced by an
> in-order traversal (left, root, right)."

```
Tree:
        3
       / \
      1   4
       \
        2

In-order: 1, 2, 3, 4
k = 1 → 1
k = 3 → 3
```

---

### Step 2 — Clarifying Questions

```
Q: Are all values in the BST unique?          → Yes (typical constraint)
Q: Is k always valid (1 <= k <= n)?           → Yes, guaranteed
Q: Can the tree be empty?                     → No, n >= 1 given k is valid
Q: Can values be negative?                    → Yes
Q: Can there be duplicate values?             → No — BST has unique values
Q: What size is the tree?                     → 1 to 10^4 nodes
Q: Will this be called once or many times
   on a tree that changes between calls?      → Matters for the follow-up
                                                 (augmented BST approach)
```

---

### Step 3 — Brute Force → Optimal

**Brute Force — Collect all values, then index — O(n) time, O(n) space:**
> "Do a full in-order traversal, dump every value into a list, and return
> list[k-1]. Correct but wasteful: we keep visiting nodes long after we've
> already found the answer, and we pay O(n) extra space for the list."

**Better — Early-stopping in-order traversal — O(H + k) time, O(H) space:**
> "We don't need the whole list — we just need to stop as soon as we've
> visited k nodes in order. Using an explicit stack (iterative in-order),
> we can push left children, then pop/visit/count, then move right,
> breaking out the moment our counter hits k. This avoids visiting the
> whole tree when k is small."

**Optimal for repeated queries — Augmented BST (order-statistics tree):**
> "If findKthSmallest is called many times and the tree is also being
> mutated (insert/delete), we should annotate each node with the size of
> its left subtree. Then a query walks a single root-to-node path
> (O(H) per query, no traversal of unrelated subtrees) by comparing k
> against left-subtree-size + 1 at each node."

---

### Step 4 — Edge Cases

```
1. Single node tree:      root=[1], k=1        → 1
2. k = n (largest node):  root=[1,2,3], k=3    → 3 (rightmost value)
3. Left-skewed tree:      root=[3,2,1], k=2    → 2
4. Right-skewed tree:     root=[1,2,3], k=1    → 1
5. k = 1 always maps to the leftmost node; k = n always maps to the
   rightmost node, by BST in-order property.
```

---

### Step 5 — Code (Optimal single-query approach)

```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        node = root

        while stack or node:
            while node:
                stack.append(node)
                node = node.left

            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val

            node = node.right
```

---

### Step 6 — Dry Run

```
Tree:
        3
       / \
      1   4
       \
        2
k = 3

node=3 → push 3, go left
node=1 → push 1, go left (None)
stack=[3,1], node=None
pop 1 → k=2 (not 0) → node = 1.right = 2
push 2 → go left (None)
stack=[3,2], node=None
pop 2 → k=1 (not 0) → node = 2.right = None
stack=[3], node=None
pop 3 → k=0 → return 3 ✓
```

---

### Step 7 — Why This Works

> "In-order traversal of a BST (left → root → right) yields values in
> strictly increasing order. By simulating that traversal iteratively
> with an explicit stack, we can decrement a counter each time we
> *visit* (pop) a node, and return immediately once the counter reaches
> zero — meaning we've just visited the kth smallest value. We never
> descend into the right subtree of nodes we don't need to, so on
> average we do far less work than a full traversal when k is small."

---

### Step 8 — Complexity Analysis

**Time — O(H + k)**
```
We push at most H nodes (height) before the first pop, then each
subsequent step pops/pushes amortized O(1) until we've visited k nodes.
Worst case (skewed tree, k = n): O(n).
```

**Space — O(H)**
```
The stack holds at most one root-to-leaf path at a time → O(H).
Balanced tree: O(log n). Skewed tree: O(n).
```

---

### Step 9 — Follow-up Questions & Answers

**Q: What if the BST is modified often (insert/delete) and kth-smallest
is queried frequently?**
> "Augment every node with a count of nodes in its left subtree
> (subtree size). To find the kth smallest, start at the root: if
> leftSize + 1 == k, return the current node; if k <= leftSize, recurse
> left; otherwise recurse right with k -= leftSize + 1. This turns each
> query into O(H) instead of O(H + k), and insert/delete just need to
> keep the subtree-size counters updated along the path they modify."

**Q: Could we solve it recursively instead of iteratively?**
> "Yes — recursive in-order with a nonlocal/instance counter that stops
> descending once found. Same asymptotic complexity, but risks stack
> overflow on very deep/skewed trees where Python's recursion limit can
> be hit; the iterative stack version avoids that risk."

**Q: What about Morris Traversal?**
> "Morris in-order traversal achieves O(1) extra space by temporarily
> threading right pointers from a node's in-order predecessor back to
> itself, then removing the thread after use. It still runs in O(n)
> time overall (each edge is traversed at most twice) and never uses a
> stack or recursion. It's the space-optimal choice when O(H) auxiliary
> space is not acceptable, at the cost of temporarily mutating tree
> structure (restored before returning)."

---

### Recap Card

```
Problem type:   BST / In-order Traversal / Order Statistics
Pattern:        In-order traversal stops early once k values are seen
Key trick:      In-order traversal of a BST = sorted order

Time:    O(H + k)  — iterative stack version (best for a single query)
Space:   O(H)       — stack holds one root-to-leaf path

Alternatives:
  Full in-order collect-all:      O(n) time, O(n) space  (simplest)
  Recursive in-order w/ counter:  O(H + k) time, O(H) space (recursion risk)
  Morris traversal:               O(n) time, O(1) space (mutates tree temporarily)
  Augmented BST (subtree sizes):  O(H) per query — best when queried repeatedly
                                   on a mutating tree

Edge cases:
  → k = 1            → leftmost (minimum) node
  → k = n            → rightmost (maximum) node
  → skewed tree      → behaves like a linked list, O(n) worst case
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
# Approach 1: Brute Force — Full In-order Traversal, Collect All
# Time:  O(n) — visits every node regardless of k
# Space: O(n) — stores every value in a list, plus O(h) recursion stack
# ─────────────────────────────────────────────
def kthSmallest_bruteforce(root: Optional[TreeNode], k: int) -> int:
    values: List[int] = []

    def inorder(node: Optional[TreeNode]) -> None:
        if not node:
            return
        inorder(node.left)
        values.append(node.val)
        inorder(node.right)

    inorder(root)
    return values[k - 1]


# ─────────────────────────────────────────────
# Approach 2: Iterative In-order Traversal with Early Stop — Optimal (single query)
# Time:  O(H + k) — descends to leftmost node once, then k pops
# Space: O(H) — explicit stack holds one root-to-leaf path
# ─────────────────────────────────────────────
def kthSmallest_iterative(root: Optional[TreeNode], k: int) -> int:
    stack = []
    node = root

    while stack or node:
        while node:
            stack.append(node)
            node = node.left

        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val

        node = node.right

    raise ValueError("k is out of bounds for this tree")


# ─────────────────────────────────────────────
# Approach 3: Recursive In-order Traversal with Early Stop
# Time:  O(H + k) — stops recursing once the kth node is found
# Space: O(H) — recursion call stack
# ─────────────────────────────────────────────
def kthSmallest_recursive_early_stop(root: Optional[TreeNode], k: int) -> int:
    count = 0
    result = None

    def inorder(node: Optional[TreeNode]) -> bool:
        nonlocal count, result
        if not node or result is not None:
            return result is not None

        if inorder(node.left):
            return True

        count += 1
        if count == k:
            result = node.val
            return True

        return inorder(node.right)

    inorder(root)
    return result


# ─────────────────────────────────────────────
# Approach 4: Morris In-order Traversal — O(1) Extra Space
# Time:  O(n) — each edge is traversed at most twice
# Space: O(1) — no stack/recursion; temporarily threads tree pointers
# ─────────────────────────────────────────────
def kthSmallest_morris(root: Optional[TreeNode], k: int) -> int:
    count = 0
    node = root

    while node:
        if not node.left:
            count += 1
            if count == k:
                return node.val
            node = node.right
        else:
            # Find the in-order predecessor of node
            predecessor = node.left
            while predecessor.right and predecessor.right is not node:
                predecessor = predecessor.right

            if not predecessor.right:
                # Create the temporary thread back to node
                predecessor.right = node
                node = node.left
            else:
                # Thread already exists → remove it (restore tree) and visit node
                predecessor.right = None
                count += 1
                if count == k:
                    return node.val
                node = node.right

    raise ValueError("k is out of bounds for this tree")


# ─────────────────────────────────────────────
# Approach 5: Augmented BST (Order-Statistics Tree) — Best for Repeated Queries
# Preprocessing: O(n) once to annotate subtree sizes.
# Each query:    O(H) — walks a single root-to-node path, no wasted traversal.
# Insert/Delete: O(H) — update subtree-size counters along the modified path.
# Ideal when the BST mutates often and kthSmallest is called repeatedly.
# ─────────────────────────────────────────────
class AugmentedNode:
    def __init__(self, val: int, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.left_size = 0  # number of nodes in left subtree


def annotate_subtree_sizes(node: Optional[TreeNode]) -> Optional[AugmentedNode]:
    """Rebuilds the tree into AugmentedNode form, filling in left_size for each node."""
    if not node:
        return None

    left = annotate_subtree_sizes(node.left)
    right = annotate_subtree_sizes(node.right)

    aug = AugmentedNode(node.val, left, right)
    aug.left_size = count_nodes(left)
    return aug


def count_nodes(node: Optional[AugmentedNode]) -> int:
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def kthSmallest_augmented(root: AugmentedNode, k: int) -> int:
    node = root
    while node:
        if k <= node.left_size:
            node = node.left
        elif k == node.left_size + 1:
            return node.val
        else:
            k -= node.left_size + 1
            node = node.right

    raise ValueError("k is out of bounds for this tree")


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Iterative In-order with Early Stop)
# O(H + k) time | O(H) space
# ─────────────────────────────────────────────
kthSmallest = kthSmallest_iterative


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
        ([3, 1, 4, None, 2], 1, 1),
        ([5, 3, 6, 2, 4, None, None, 1], 3, 3),
        ([1], 1, 1),
        ([2, 1, 3], 3, 3),
        ([3, 2, None, 1], 2, 2),
    ]

    solvers = [
        ("Brute Force (collect-all)", kthSmallest_bruteforce),
        ("Iterative In-order (optimal)", kthSmallest_iterative),
        ("Recursive Early Stop", kthSmallest_recursive_early_stop),
        ("Morris Traversal (O(1) space)", kthSmallest_morris),
    ]

    for arr, k, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree, k)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr}, k={k} | got={out}")

        # Augmented BST approach (separate structure, built fresh per test)
        aug_tree = annotate_subtree_sizes(build_tree(arr))
        out = kthSmallest_augmented(aug_tree, k)
        status = "PASS" if out == expected else "FAIL"
        print(f"[{status}] Augmented BST (order-statistics) | tree={arr}, k={k} | got={out}")
