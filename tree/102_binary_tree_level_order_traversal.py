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
