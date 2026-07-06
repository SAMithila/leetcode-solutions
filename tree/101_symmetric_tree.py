"""
LeetCode 101 - Symmetric Tree

Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

Example 1:
  Input: root = [1,2,2,3,4,4,3]
  Output: true

Example 2:
  Input: root = [1,2,2,null,3,null,3]
  Output: false
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Recursive DFS - Optimal / Most Idiomatic
# Time:  O(n) — visits each node exactly once
# Space: O(h) — recursion stack depth up to tree height (h)
# ─────────────────────────────────────────────
def isSymmetric_recursive(root: Optional[TreeNode]) -> bool:
    if not root:
        return True

    def isMirror(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool:
        if not t1 and not t2:
            return True
        if not t1 or not t2 or t1.val != t2.val:
            return False
        return isMirror(t1.left, t2.right) and isMirror(t1.right, t2.left)

    return isMirror(root.left, root.right)


# ─────────────────────────────────────────────
# Approach 2: Iterative BFS (Level-Order with Queue)
# Time:  O(n) — visits each node exactly once
# Space: O(w) — queue size up to maximum width of the tree (w)
# ─────────────────────────────────────────────
def isSymmetric_bfs(root: Optional[TreeNode]) -> bool:
    if not root:
        return True

    # Queue holds pairs of nodes that should be symmetric
    queue = deque([(root.left, root.right)])

    while queue:
        t1, t2 = queue.popleft()

        if not t1 and not t2:
            continue
        if not t1 or not t2 or t1.val != t2.val:
            return False

        # Add child nodes in mirror order
        queue.append((t1.left, t2.right))
        queue.append((t1.right, t2.left))

    return True


# ─────────────────────────────────────────────
# Approach 3: Iterative DFS (Pre-Order with Stack)
# Time:  O(n) — visits each node exactly once
# Space: O(h) — stack size up to tree height (h)
# ─────────────────────────────────────────────
def isSymmetric_iterative_dfs(root: Optional[TreeNode]) -> bool:
    if not root:
        return True

    # Stack holds pairs of nodes that should be symmetric
    stack = [(root.left, root.right)]

    while stack:
        t1, t2 = stack.pop()

        if not t1 and not t2:
            continue
        if not t1 or not t2 or t1.val != t2.val:
            return False

        # Add child nodes in mirror order
        stack.append((t1.right, t2.left))
        stack.append((t1.left, t2.right))

    return True


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Recursive DFS)
# O(n) time | O(h) space
# ─────────────────────────────────────────────
isSymmetric = isSymmetric_recursive


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
        ([1, 2, 2, 3, 4, 4, 3], True),
        ([1, 2, 2, None, 3, None, 3], False),
        ([], True),
        ([1], True),
        ([1, 2, 2, None, 3, 3, None], True),
        ([1, 2, 3], False),
    ]

    solvers = [
        ("Recursive DFS", isSymmetric_recursive),
        ("Iterative BFS", isSymmetric_bfs),
        ("Iterative DFS", isSymmetric_iterative_dfs),
    ]

    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
