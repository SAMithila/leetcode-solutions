"""
========================================================
LeetCode 49 - Group Anagrams
========================================================
Difficulty : Medium
Link       : https://leetcode.com/problems/group-anagrams/

Problem Statement
-----------------
Given an array of strings strs, group the anagrams together.
You can return the answer in any order.

An anagram is a word formed by rearranging all letters of
another word, using each original letter exactly once.

Examples
--------
Input : strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Input : strs = [""]
Output: [[""]]

Input : strs = ["a"]
Output: [["a"]]

Constraints
-----------
- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters
========================================================
"""

from typing import List
from collections import defaultdict, Counter
from itertools import groupby


# ──────────────────────────────────────────────────────
# Approach 1 : Brute Force
# ──────────────────────────────────────────────────────
# Intuition  : For each word, check every previously seen
#              group. If its sorted form matches the group's
#              key, add it there; otherwise start a new group.
# Time       : O(n² * k log k)  — n words, k = max word length
# Space      : O(n * k)
# ──────────────────────────────────────────────────────
def groupAnagrams_brute_force(strs: List[str]) -> List[List[str]]:
    groups: List[List[str]] = []
    keys:   List[str]       = []

    for word in strs:
        key = "".join(sorted(word))
        matched = False
        for i, k in enumerate(keys):
            if k == key:
                groups[i].append(word)
                matched = True
                break
        if not matched:
            groups.append([word])
            keys.append(key)

    return groups


# ──────────────────────────────────────────────────────
# Approach 2 : Sorted String as Key  ★ OPTIMAL (interview) ★
# ──────────────────────────────────────────────────────
# Intuition  : Anagrams produce identical strings when sorted.
#              Use the sorted word as a dict key to group them.
# Time       : O(n * k log k)
# Space      : O(n * k)
# ──────────────────────────────────────────────────────
def groupAnagrams_sorted_key(strs: List[str]) -> List[List[str]]:
    groups: dict[str, List[str]] = {}
    for word in strs:
        key = "".join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())


# ──────────────────────────────────────────────────────
# Approach 3 : Sorted Key + defaultdict  (cleaner variant)
# ──────────────────────────────────────────────────────
# Intuition  : Same as Approach 2; defaultdict(list) removes
#              the explicit key-existence check.
# Time       : O(n * k log k)
# Space      : O(n * k)
# ──────────────────────────────────────────────────────
def groupAnagrams_defaultdict(strs: List[str]) -> List[List[str]]:
    groups: defaultdict[str, List[str]] = defaultdict(list)
    for word in strs:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())


# ──────────────────────────────────────────────────────
# Approach 4 : Character Count Tuple as Key
# ──────────────────────────────────────────────────────
# Intuition  : Instead of sorting, count frequency of each
#              of the 26 letters and use the 26-int tuple as
#              the key. Avoids the O(k log k) sort cost.
# Time       : O(n * k)   — linear scan per word
# Space      : O(n * k)
# ──────────────────────────────────────────────────────
def groupAnagrams_count_tuple(strs: List[str]) -> List[List[str]]:
    groups: defaultdict[tuple, List[str]] = defaultdict(list)
    for word in strs:
        count = [0] * 26
        for c in word:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(word)
    return list(groups.values())

'''
# ──────────────────────────────────────────────────────
# Approach 5 : Frozen Counter as Key
# ──────────────────────────────────────────────────────
# Intuition  : Use frozenset of Counter items as the key.
#              frozenset is hashable; Counter(word).items()
#              gives (char, count) pairs that uniquely identify
#              the character multiset.
# Time       : O(n * k)
# Space      : O(n * k)
# ──────────────────────────────────────────────────────
def groupAnagrams_frozen_counter(strs: List[str]) -> List[List[str]]:
    groups: defaultdict[frozenset, List[str]] = defaultdict(list)
    for word in strs:
        key = frozenset(Counter(word).items())
        groups[key].append(word)
    return list(groups.values())


# ──────────────────────────────────────────────────────
# Approach 6 : Prime Product as Key
# ──────────────────────────────────────────────────────
# Intuition  : Map each letter to a unique prime. Multiply
#              all primes for a word; anagrams yield the same
#              product (Fundamental Theorem of Arithmetic).
# Note       : Products can grow large for long strings, but
#              Python handles arbitrary-precision ints natively.
# Time       : O(n * k)
# Space      : O(n)
# ──────────────────────────────────────────────────────
_PRIMES = [
     2,  3,  5,  7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,101
]

def groupAnagrams_prime(strs: List[str]) -> List[List[str]]:
    groups: defaultdict[int, List[str]] = defaultdict(list)
    for word in strs:
        key = 1
        for c in word:
            key *= _PRIMES[ord(c) - ord('a')]
        groups[key].append(word)
    return list(groups.values())


# ──────────────────────────────────────────────────────
# Approach 7 : Sort Array + itertools.groupby
# ──────────────────────────────────────────────────────
# Intuition  : Sort the entire list of strings by their
#              sorted-character form, then groupby that key.
#              groupby collapses consecutive equal keys into
#              one group — works because we sorted first.
# Time       : O(n * k log k)   — sort of the full list
# Space      : O(n * k)
# ──────────────────────────────────────────────────────
def groupAnagrams_groupby(strs: List[str]) -> List[List[str]]:
    key_fn = lambda w: "".join(sorted(w))
    sorted_strs = sorted(strs, key=key_fn)
    return [list(group) for _, group in groupby(sorted_strs, key=key_fn)]

'''
# ──────────────────────────────────────────────────────
# ★ Quick comparison summary
# ──────────────────────────────────────────────────────
# | #  | Approach              | Time          | Space   | Notes                          |
# |----|-----------------------|---------------|---------|--------------------------------|
# | 1  | Brute Force           | O(n² k log k) | O(nk)   | Simple, very slow              |
# | 2  | Sorted Key + dict     | O(nk log k)   | O(nk)   | Clean, interview standard ★    |
# | 3  | Sorted Key + defdict  | O(nk log k)   | O(nk)   | Tidier version of #2           |
# | 4  | Count Tuple Key       | O(nk)         | O(nk)   | Faster key — no sort needed    |
# | 5  | Frozen Counter Key    | O(nk)         | O(nk)   | Pythonic Counter variant       |
# | 6  | Prime Product Key     | O(nk)         | O(n)    | Math trick, big-int risk       |
# | 7  | Sort + groupby        | O(nk log k)   | O(nk)   | Functional / itertools style   |
# ──────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────
# Test Driver
# ──────────────────────────────────────────────────────
def normalize(result: List[List[str]]) -> List[List[str]]:
    return sorted(sorted(group) for group in result)

if __name__ == "__main__":
    test_cases = [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]],
        ),
        (
            [""],
            [[""]],
        ),
        (
            ["a"],
            [["a"]],
        ),
        (
            ["ab", "ba", "abc", "bca", "cab", "xyz"],
            [["ab", "ba"], ["abc", "bca", "cab"], ["xyz"]],
        ),
        (
            ["aab", "aba", "baa", "bba"],
            [["aab", "aba", "baa"], ["bba"]],
        ),
    ]

    solutions = [
        ("1. Brute Force",         groupAnagrams_brute_force),
        ("2. Sorted Key + dict",   groupAnagrams_sorted_key),
        ("3. Sorted + defaultdict",groupAnagrams_defaultdict),
        ("4. Count Tuple Key",     groupAnagrams_count_tuple),
    #   ("5. Frozen Counter Key",  groupAnagrams_frozen_counter),
    #   ("6. Prime Product Key",   groupAnagrams_prime),
    #   ("7. Sort + groupby",      groupAnagrams_groupby),
    ]

    for strs, expected in test_cases:
        print(f"\nstrs={strs}")
        print(f"expected={normalize(expected)}")
        for name, fn in solutions:
            result = normalize(fn(strs[:]))
            status = "PASS" if result == normalize(expected) else "FAIL"
            print(f"  {status}  {name:<28} → {result}")
