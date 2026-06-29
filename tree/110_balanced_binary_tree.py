"""
LeetCode 110 - Balanced Binary Tree
Given a binary tree, determine if it is height-balanced.

A height-balanced binary tree is defined as:
  A binary tree in which the left and right subtrees of every node 
  differ in height by no more than 1.

Example:
  Input:  root = [3,9,20,null,null,15,7]
  Output: true

  Input:  root = [1,2,2,3,3,null,null,4,4]
  Output: false

KEY INSIGHT:
  A tree is balanced if both subtrees are balanced and their height difference
  is at most 1. Checking top-down repeats calculations. Checking bottom-up
  calculates height and balance status in a single post-order traversal.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────
# Approach 1: Top-Down Recursion (Brute Force)
# Time:  O(n log n) average, O(n^2) worst case (skewed tree)
# Space: O(h) — recursion stack depth
# ─────────────────────────────────────────────
def is_balanced_top_down(root: Optional[TreeNode]) -> bool:
    def get_height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return 1 + max(get_height(node.left), get_height(node.right))

    if not root:
        return True

    # Check height difference at current node
    left_h = get_height(root.left)
    right_h = get_height(root.right)
    
    if abs(left_h - right_h) > 1:
        return False
        
    # Recursively check subtrees
    return is_balanced_top_down(root.left) and is_balanced_top_down(root.right)


# ─────────────────────────────────────────────
# Approach 2: Bottom-Up Recursion (Optimal)
# Time:  O(n) — visits each node exactly once
# Space: O(h) — recursion stack depth
#
# Return -1 if a subtree is unbalanced, otherwise return its actual height.
# ─────────────────────────────────────────────
def is_balanced_bottom_up(root: Optional[TreeNode]) -> bool:
    def check_height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0  # height of empty tree is 0

        # Check left subtree
        left_h = check_height(node.left)
        if left_h == -1:
            return -1  # left subtree is unbalanced

        # Check right subtree
        right_h = check_height(node.right)
        if right_h == -1:
            return -1  # right subtree is unbalanced

        # Check current node
        if abs(left_h - right_h) > 1:
            return -1  # current node is unbalanced

        # Return actual height of current node
        return 1 + max(left_h, right_h)

    return check_height(root) != -1


# ─────────────────────────────────────────────
# OPTIMAL — Approach 2 (Bottom-Up Recursion)
# O(n) time | O(h) space
# ─────────────────────────────────────────────
isBalanced = is_balanced_bottom_up


# ─── Helper for Testing ───────────────────────
def build_tree(arr: list) -> Optional[TreeNode]:
    if not arr:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while i < len(arr):
        curr = queue.pop(0)
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
        # (tree representation, expected_result)
        ([3, 9, 20, None, None, 15, 7], True),
        ([1, 2, 2, 3, 3, None, None, 4, 4], False),
        ([], True),
        ([1], True),
        ([1, 2, None, 3], False),
        ([1, 2, 2, 3, None, None, 3, 4, None, None, 4], False),
        ([1, 2, 3], True),
    ]

    solvers = [
        ("Top-Down", is_balanced_top_down),
        ("Bottom-Up", is_balanced_bottom_up),
    ]

    for arr, expected in tests:
        for name, fn in solvers:
            tree = build_tree(arr)
            out = fn(tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | tree={arr} | got={out}")
