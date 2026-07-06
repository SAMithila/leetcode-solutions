"""
LeetCode 94 - Binary Tree Inorder Traversal
Given the root of a binary tree, return the inorder traversal of its nodes' values.

Example 1:
  Input: root = [1,null,2,3]
  Output: [1,3,2]

Example 2:
  Input: root = []
  Output: []

Example 3:
  Input: root = [1]
  Output: [1]
"""

from typing import List, Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Recursive DFS - Optimal / Most Idiomatic
# Time:  O(n) — visits each node exactly once
# Space: O(h) — recursion stack depth, where h is the tree height
#               O(n) worst case (skewed tree), O(log n) best case (balanced tree)
# ─────────────────────────────────────────────
def inorderTraversal_recursive(root: Optional[TreeNode]) -> List[int]:
    result = []

    def dfs(node: Optional[TreeNode]):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


# ─────────────────────────────────────────────
# Approach 2: Iterative DFS with Stack
# Time:  O(n) — visits each node exactly once
# Space: O(h) — stack size up to the tree height
#               O(n) worst case, O(log n) best case
# ─────────────────────────────────────────────
def inorderTraversal_iterative(root: Optional[TreeNode]) -> List[int]:
    result = []
    stack = []
    curr = root

    while curr or stack:
        # Reach the left-most node of the current node
        while curr:
            stack.append(curr)
            curr = curr.left

        # Current must be None at this point
        curr = stack.pop()
        result.append(curr.val)

        # We have visited the node and its left subtree. Now, it's right subtree's turn
        curr = curr.right

    return result


# ─────────────────────────────────────────────
# Approach 3: Morris Inorder Traversal (O(1) Auxiliary Space)
# Time:  O(n) — each edge is traversed at most 3 times
# Space: O(1) — no recursion stack or stack data structure is used
# ─────────────────────────────────────────────
def inorderTraversal_morris(root: Optional[TreeNode]) -> List[int]:
    result = []
    curr = root

    while curr:
        if not curr.left:
            result.append(curr.val)
            curr = curr.right
        else:
            # Find the inorder predecessor of curr
            pre = curr.left
            while pre.right and pre.right != curr:
                pre = pre.right

            # Make curr the right child of its inorder predecessor
            if not pre.right:
                pre.right = curr
                curr = curr.left
            # Revert the changes made to restore the original tree
            else:
                pre.right = None
                result.append(curr.val)
                curr = curr.right

    return result


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Recursive DFS)
# O(n) time | O(h) space
# ─────────────────────────────────────────────
inorderTraversal = inorderTraversal_recursive


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
        ([1, None, 2, 3], [1, 3, 2]),
        ([], []),
        ([1], [1]),
        ([1, 2, 3, 4, 5, None, None], [4, 2, 5, 1, 3]),
    ]

    solvers = [
        ("Recursive DFS", inorderTraversal_recursive),
        ("Iterative Stack", inorderTraversal_iterative),
        ("Morris Traversal", inorderTraversal_morris),
    ]

    for arr, expected in tests:
        # Since Morris traversal temporarily modifies the tree structure but restores it,
        # we can use the same tree or rebuild it to be safe. We'll rebuild it for each solver.
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
