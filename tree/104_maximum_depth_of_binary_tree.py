"""
LeetCode 104 - Maximum Depth of Binary Tree
Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path 
from the root node down to the farthest leaf node.

Example:
  Input:  root = [3,9,20,null,null,15,7]
  Output: 3

  Input:  root = [1,null,2]
  Output: 2
"""

from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Recursive DFS (Post-order Traversal) - Optimal / Most Idiomatic
# Time:  O(n) — visits each node exactly once
# Space: O(h) — where h is the tree height (recursion stack depth)
#               O(n) worst case (skewed tree), O(log n) best case (balanced tree)
# ─────────────────────────────────────────────
def maxDepth_recursive_dfs(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    return 1 + max(maxDepth_recursive_dfs(root.left), maxDepth_recursive_dfs(root.right))


# ─────────────────────────────────────────────
# Approach 2: Iterative BFS (Level-Order Traversal)
# Time:  O(n) — visits each node exactly once
# Space: O(w) — where w is the maximum width of the tree
#               O(n) worst case (full binary tree has n/2 leaf nodes at the bottom level)
# ─────────────────────────────────────────────
def maxDepth_bfs(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    queue = deque([root])
    depth = 0

    while queue:
        depth += 1
        # Process all nodes at the current level
        for _ in range(len(queue)):
            curr = queue.popleft()
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)

    return depth


# ─────────────────────────────────────────────
# Approach 3: Iterative DFS (Pre-order Traversal with Stack)
# Time:  O(n) — visits each node exactly once
# Space: O(h) — stack size up to the height of the tree
#               O(n) worst case, O(log n) best case
# ─────────────────────────────────────────────
def maxDepth_iterative_dfs(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    stack = [(root, 1)]
    max_depth = 0

    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)
        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return max_depth


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Recursive DFS)
# O(n) time | O(h) space
# Cleanest and most idiomatic implementation for binary tree depth problems.
# ─────────────────────────────────────────────
maxDepth = maxDepth_recursive_dfs


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
        ([3, 9, 20, None, None, 15, 7], 3),
        ([1, None, 2], 2),
        ([], 0),
        ([0], 1),
    ]

    solvers = [
        ("Recursive DFS", maxDepth_recursive_dfs),
        ("Iterative BFS", maxDepth_bfs),
        ("Iterative DFS", maxDepth_iterative_dfs),
    ]

    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
