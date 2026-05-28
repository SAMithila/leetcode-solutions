"""
LeetCode 3 - Longest Substring Without Repeating Characters
Given a string s, find the length of the longest substring without
repeating characters.

Example:
  Input:  s = "abcabcbb"
  Output: 3  ("abc")

  Input:  s = "bbbbb"
  Output: 1  ("b")

  Input:  s = "pwwkew"
  Output: 3  ("wke")
"""


# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(n^3)  — all pairs + uniqueness check per substring
# Space: O(min(n, m))  — m = charset size
# ─────────────────────────────────────────────
def lengthOfLongestSubstring_brute(s: str) -> int:
    n = len(s)
    best = 0
    for i in range(n):
        for j in range(i + 1, n + 1):
            if len(set(s[i:j])) == j - i:   # all unique
                best = max(best, j - i)
    return best


# ─────────────────────────────────────────────
# Approach 2: Sliding Window + Set (Optima)
# Time:  O(n)
# Space: O(min(n, m))
#
# Expand right freely; when a duplicate enters, shrink left
# one step at a time until the window is valid again.
# ─────────────────────────────────────────────
def lengthOfLongestSubstring_set(s: str) -> int:
    seen = set()
    left = 0
    best = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        best = max(best, right - left + 1)

    return best


# ─────────────────────────────────────────────
# Approach 3: Sliding Window + HashMap (jump left pointer)
# Time:  O(n)
# Space: O(min(n, m))
#
# Store last seen index of each character.
# On a duplicate, jump left directly past its previous position
# instead of crawling one step at a time.
# ─────────────────────────────────────────────
def lengthOfLongestSubstring_map(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1   # jump past previous occurrence
        last_seen[ch] = right
        best = max(best, right - left + 1)

    return best

'''
# ─────────────────────────────────────────────
# Approach 4: Sliding Window + Array (ASCII only)
# Time:  O(n)
# Space: O(1)  — fixed 128-entry array, independent of input size
#
# Same as HashMap but uses a 128-slot index array for ASCII chars.
# Faster in practice due to array locality vs. dict hashing.
# ─────────────────────────────────────────────
def lengthOfLongestSubstring_array(s: str) -> int:
    index = [-1] * 128   # last seen position for each ASCII char
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if index[ord(ch)] >= left:
            left = index[ord(ch)] + 1
        index[ord(ch)] = right
        best = max(best, right - left + 1)

    return best
'''

# ─────────────────────────────────────────────
# OPTIMAL — Approach 3 (Sliding Window + HashMap)
# O(n) time  |  O(min(n, m)) space
# Most general: works for any Unicode, not just ASCII
# ─────────────────────────────────────────────
lengthOfLongestSubstring = lengthOfLongestSubstring_map


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("abcabcbb", 3),
        ("bbbbb",    1),
        ("pwwkew",   3),
        ("",         0),
        ("a",        1),
        ("au",       2),
        ("dvdf",     3),
        ("abba",     2),
        ("tmmzuxt",  5),
    ]

    solvers = [
        ("Brute Force", lengthOfLongestSubstring_brute),
        ("Set",         lengthOfLongestSubstring_set),
        ("HashMap",     lengthOfLongestSubstring_map),
        ("Array",       lengthOfLongestSubstring_array),
    ]

    for s, expected in tests:
        for name, fn in solvers:
            out = fn(s)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | s={s!r} | got={out}")
