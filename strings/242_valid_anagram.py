"""
========================================================
LeetCode 242 - Valid Anagram
========================================================
Difficulty : Easy
Link       : https://leetcode.com/problems/valid-anagram/

Problem Statement
-----------------
Given two strings s and t, return true if t is an anagram
of s, and false otherwise.

An anagram is a word formed by rearranging all letters of
another word, using each original letter exactly once.

Examples
--------
Input : s = "anagram", t = "nagaram"
Output: True

Input : s = "rat", t = "car"
Output: False

Constraints
-----------
- 1 <= s.length, t.length <= 5 * 10^4
- s and t consist of lowercase English letters
========================================================
"""

from collections import Counter, defaultdict


# ──────────────────────────────────────────────────────
# Approach 1 : Sorting
# ──────────────────────────────────────────────────────
# Intuition  : Anagrams contain the same characters, so
#              sorting both strings must yield equal results.
# Time       : O(n log n)
# Space      : O(n)  — sorted() creates a new list
# ──────────────────────────────────────────────────────
def isAnagram_sorting(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)


# ──────────────────────────────────────────────────────
# Approach 2 : Counter Equality
# ──────────────────────────────────────────────────────
# Intuition  : Two strings are anagrams iff their character
#              frequency maps are identical.
# Time       : O(n)
# Space      : O(1)  — at most 26 distinct keys
# ──────────────────────────────────────────────────────
def isAnagram_counter(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)


# ──────────────────────────────────────────────────────
# Approach 3 : Fixed Array of 26
# ──────────────────────────────────────────────────────
# Intuition  : Since input is lowercase a–z, map each char
#              to index 0–25 and track frequency in a
#              fixed-size array.
# Time       : O(n)
# Space      : O(1)  — always 26 integers
# ──────────────────────────────────────────────────────
def isAnagram_array(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('a')] += 1
    for c in t:
        freq[ord(c) - ord('a')] -= 1
    return all(f == 0 for f in freq)


# ──────────────────────────────────────────────────────
# Approach 4 : Single-Pass Array (increment + decrement)
# ──────────────────────────────────────────────────────
# Intuition  : Traverse both strings simultaneously:
#              +1 for each char in s, -1 for each char in t.
#              If every slot is zero at the end → anagram.
# Time       : O(n)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def isAnagram_single_pass(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    freq = [0] * 26
    for cs, ct in zip(s, t):
        freq[ord(cs) - ord('a')] += 1
        freq[ord(ct) - ord('a')] -= 1
    return all(f == 0 for f in freq)


# ──────────────────────────────────────────────────────
# Approach 5 : Dictionary (manual frequency count)
# ──────────────────────────────────────────────────────
# Intuition  : Build a frequency dict for s, then subtract
#              counts while iterating t. Any nonzero value
#              or missing key means not an anagram.
# Time       : O(n)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def isAnagram_dict(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    freq: dict[str, int] = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    for c in t:
        if freq.get(c, 0) == 0:
            return False
        freq[c] -= 1
    return True

'''
# ──────────────────────────────────────────────────────
# Approach 6 : defaultdict
# ──────────────────────────────────────────────────────
# Intuition  : Same as dict approach; defaultdict(int)
#              removes the need for .get() fallbacks.
# Time       : O(n)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def isAnagram_defaultdict(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    freq: defaultdict[str, int] = defaultdict(int)
    for c in s:
        freq[c] += 1
    for c in t:
        freq[c] -= 1
    return all(v == 0 for v in freq.values())


# ──────────────────────────────────────────────────────
# Approach 7 : Counter Subtraction
# ──────────────────────────────────────────────────────
# Intuition  : Subtracting one Counter from another keeps
#              only positive counts. An empty result means
#              t has no "extra" characters beyond s.
# Note       : Counter subtraction ignores negative values,
#              so also check len equality first.
# Time       : O(n)
# Space      : O(1)
# ──────────────────────────────────────────────────────
def isAnagram_counter_subtract(s: str, t: str) -> bool:
    return len(s) == len(t) and not (Counter(s) - Counter(t))


# ──────────────────────────────────────────────────────
# Approach 8 : Prime Product Hashing
# ──────────────────────────────────────────────────────
# Intuition  : Assign the i-th prime to the i-th letter.
#              Multiply all primes for s and t; equal products
#              guarantee the same multiset of characters
#              (by the Fundamental Theorem of Arithmetic).
# Note       : Works correctly but product can grow very large
#              for long strings (Python handles big ints natively).
# Time       : O(n)
# Space      : O(1)
# ──────────────────────────────────────────────────────
_PRIMES = [
    2,  3,  5,  7, 11, 13, 17, 19, 23, 29,
   31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
   73, 79, 83, 89, 97,101
]

def isAnagram_prime(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    product = lambda string: 1
    def _product(string: str) -> int:
        p = 1
        for c in string:
            p *= _PRIMES[ord(c) - ord('a')]
        return p
    return _product(s) == _product(t)
'''

# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach              | Time     | Space | Notes                          |
# |----|-----------------------|----------|-------|--------------------------------|
# | 1  | Sorting               | O(nlogn) | O(n)  | Simple, clean                  |
# | 2  | Counter Equality      | O(n)     | O(1)  | Most Pythonic                  |
# | 3  | Fixed Array (26)      | O(n)     | O(1)  | Fastest in practice ★          |
# | 4  | Single-Pass Array     | O(n)     | O(1)  | One loop, same array           |
# | 5  | Dict Manual           | O(n)     | O(1)  | Explicit, early exit           |
# | 6  | defaultdict           | O(n)     | O(1)  | Cleaner dict variant           |
# | 7  | Counter Subtraction   | O(n)     | O(1)  | Counter arithmetic trick       |
# | 8  | Prime Product         | O(n)     | O(1)  | Math curiosity, big-int risk   |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ("anagram", "nagaram",  True),
        ("rat",     "car",      False),
        ("a",       "a",        True),
        ("ab",      "a",        False),
        ("aacc",    "ccac",     False),
        ("listen",  "silent",   True),
        ("hello",   "world",    False),
        ("",        "",         True),
    ]

    solutions = [
        ("1. Sorting",            isAnagram_sorting),
        ("2. Counter Equality",   isAnagram_counter),
        ("3. Fixed Array (26)",   isAnagram_array),
        ("4. Single-Pass Array",  isAnagram_single_pass),
        ("5. Dict Manual",        isAnagram_dict),
    #    ("6. defaultdict",        isAnagram_defaultdict),
    #   ("7. Counter Subtract",   isAnagram_counter_subtract),
    #    ("8. Prime Product",      isAnagram_prime),
    ]

    for s, t, expected in test_cases:
        print(f"\ns={s!r}, t={t!r}  →  expected={expected}")
        for name, fn in solutions:
            result = fn(s, t)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}  {name:<24} → {result}")
