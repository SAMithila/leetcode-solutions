"""
LeetCode 226 - Invert Binary Tree
Given the root of a binary tree, invert the tree, and return its root.

Example:
  Input:  root = [4,2,7,1,3,6,9]
  Output: [4,7,2,9,6,3,1]

  Input:  root = [2,1,3]
  Output: [2,3,1]

  Input:  root = []
  Output: []
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Recursive DFS (Pre-Order / Post-Order) - Optimal / Most Idiomatic
# Time:  O(n) — visits each node exactly once
# Space: O(h) — recursion stack depth, where h is the tree height
#               O(n) worst case (skewed tree), O(log n) best case (balanced tree)
# ─────────────────────────────────────────────
def invertTree_recursive(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    # Swap left and right children
    root.left, root.right = root.right, root.left

    # Recursively invert subtrees
    self.invertTree(root.left)
    self.invertTree(root.right)

    return root


# ─────────────────────────────────────────────
# Approach 2: Iterative BFS (Level-Order Traversal)
# Time:  O(n) — visits each node exactly once
# Space: O(w) — queue size up to the maximum width of the tree
#               O(n) worst case
# ─────────────────────────────────────────────
def invertTree_bfs(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    queue = deque([root])
    while queue:
        curr = queue.popleft()

        # Swap left and right children
        curr.left, curr.right = curr.right, curr.left

        if curr.left:
            queue.append(curr.left)
        if curr.right:
            queue.append(curr.right)

    return root


# ─────────────────────────────────────────────
# Approach 3: Iterative DFS (Pre-Order with Stack)
# Time:  O(n) — visits each node exactly once
# Space: O(h) — stack size up to the tree height
#               O(n) worst case
# ─────────────────────────────────────────────
def invertTree_iterative_dfs(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    stack = [root]
    while stack:
        curr = stack.pop()

        # Swap left and right children
        curr.left, curr.right = curr.right, curr.left

        if curr.left:
            stack.append(curr.left)
        if curr.right:
            stack.append(curr.right)

    return root


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Recursive DFS)
# O(n) time | O(h) space
# ─────────────────────────────────────────────
invertTree = invertTree_recursive


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


def serialize_tree(root: Optional[TreeNode]) -> list:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        curr = queue.popleft()
        if curr:
            result.append(curr.val)
            queue.append(curr.left)
            queue.append(curr.right)
        else:
            result.append(None)
    # Trim trailing None elements
    while result and result[-1] is None:
        result.pop()
    return result


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]),
        ([2, 1, 3], [2, 3, 1]),
        ([], []),
    ]

    solvers = [
        ("Recursive DFS", invertTree_recursive),
        ("Iterative BFS", invertTree_bfs),
        ("Iterative DFS", invertTree_iterative_dfs),
    ]

    # Note: Since the functions invert the tree in-place, 
    # we need to rebuild the tree for each solver test.
    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            inverted_root = fn(tree)
            out = serialize_tree(inverted_root)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
