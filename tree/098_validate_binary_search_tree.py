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
