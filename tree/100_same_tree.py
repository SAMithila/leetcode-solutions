"""
LeetCode 100 - Same Tree
Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

Example 1:
  Input: p = [1,2,3], q = [1,2,3]
  Output: true

Example 2:
  Input: p = [1,2], q = [1,null,2]
  Output: false

Example 3:
  Input: p = [1,2,1], q = [1,1,2]
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
# Time:  O(min(n, m)) — visits each node up to once
# Space: O(min(hp, hq)) — recursion stack depth up to tree height
# ─────────────────────────────────────────────
def isSameTree_recursive(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    # If both nodes are None, they are the same
    if not p and not q:
        return True
    # If only one of them is None, or values don't match, they are not the same
    if not p or not q or p.val != q.val:
        return False
    # Recursively check left and right subtrees
    return isSameTree_recursive(p.left, q.left) and isSameTree_recursive(p.right, q.right)


# ─────────────────────────────────────────────
# Approach 2: Iterative BFS (Level-Order with Queue)
# Time:  O(min(n, m))
# Space: O(min(wp, wq)) — queue size up to maximum width
# ─────────────────────────────────────────────
def isSameTree_bfs(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    queue = deque([(p, q)])

    while queue:
        n1, n2 = queue.popleft()

        if not n1 and not n2:
            continue
        if not n1 or not n2 or n1.val != n2.val:
            return False

        queue.append((n1.left, n2.left))
        queue.append((n1.right, n2.right))

    return True


# ─────────────────────────────────────────────
# Approach 3: Iterative DFS (Pre-Order with Stack)
# Time:  O(min(n, m))
# Space: O(min(hp, hq)) — stack size up to tree height
# ─────────────────────────────────────────────
def isSameTree_iterative_dfs(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    stack = [(p, q)]

    while stack:
        n1, n2 = stack.pop()

        if not n1 and not n2:
            continue
        if not n1 or not n2 or n1.val != n2.val:
            return False

        stack.append((n1.right, n2.right))
        stack.append((n1.left, n2.left))

    return True


# ─────────────────────────────────────────────
# OPTIMAL — Approach 1 (Recursive DFS)
# O(min(n, m)) time | O(min(hp, hq)) space
# ─────────────────────────────────────────────
isSameTree = isSameTree_recursive


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
        (([1, 2, 3], [1, 2, 3]), True),
        (([1, 2], [1, None, 2]), False),
        (([1, 2, 1], [1, 1, 2]), False),
        (([], []), True),
        (([1], [1]), True),
        (([1], [2]), False),
    ]

    solvers = [
        ("Recursive DFS", isSameTree_recursive),
        ("Iterative BFS", isSameTree_bfs),
        ("Iterative DFS", isSameTree_iterative_dfs),
    ]

    for (p_arr, q_arr), expected in tests:
        for name, fn in solvers:
            p_tree = build_tree(p_arr)
            q_tree = build_tree(q_arr)
            out = fn(p_tree, q_tree)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | p={p_arr}, q={q_arr} | got={out}")
