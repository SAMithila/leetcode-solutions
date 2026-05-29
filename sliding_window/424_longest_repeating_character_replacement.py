"""
LeetCode 424 - Longest Repeating Character Replacement
Given a string s and integer k, you can replace at most k characters.
Return the length of the longest substring containing the same letter
after at most k replacements.

Key insight: window is valid when (window_size - max_freq) <= k
  → characters to replace = window_size - count of most frequent char

Example:
  Input:  s = "AABABBA", k = 1
  Output: 4  ("AABA" or "ABBA", replace one char)
"""


# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(n^2)
# Space: O(1)  — only 26 uppercase letters
# ─────────────────────────────────────────────
def characterReplacement_brute(s: str, k: int) -> int:
    best = 0
    n = len(s)

    for left in range(n):
        freq = {}
        max_freq = 0
        for right in range(left, n):
            ch = s[right]
            freq[ch] = freq.get(ch, 0) + 1
            max_freq = max(max_freq, freq[ch])
            window = right - left + 1
            if window - max_freq <= k:
                best = max(best, window)
            else:
                break   # further expanding only makes it worse for this left
    return best


# ─────────────────────────────────────────────
# Approach 2: Sliding Window (shrink on invalid)
# Time:  O(n)
# Space: O(1)
#
# Expand right freely. When window becomes invalid
# (replacements needed > k), shrink left by one.
# ─────────────────────────────────────────────
def characterReplacement_shrink(s: str, k: int) -> int:
    freq = {}
    left = 0
    max_freq = 0
    best = 0

    for right in range(len(s)):
        ch = s[right]
        freq[ch] = freq.get(ch, 0) + 1
        max_freq = max(max_freq, freq[ch])

        window = right - left + 1
        if window - max_freq > k:
            freq[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best


# ─────────────────────────────────────────────
# Approach 3: Sliding Window (fixed window / no shrink)
# Time:  O(n)
# Space: O(1)
#
# Never shrink the window — only shift it.
# Since we want the LONGEST window, we only grow when we find
# a higher max_freq. Otherwise we slide (left += 1, right += 1)
# keeping the same window size, which can only help or stay equal.
# ─────────────────────────────────────────────
def characterReplacement_noShrink(s: str, k: int) -> int:
    freq = {}
    left = 0
    max_freq = 0

    for right in range(len(s)):
        ch = s[right]
        freq[ch] = freq.get(ch, 0) + 1
        max_freq = max(max_freq, freq[ch])

        # If invalid: slide the window (don't shrink, just shift)
        if (right - left + 1) - max_freq > k:
            freq[s[left]] -= 1
            left += 1

    return len(s) - left   # window never shrinks so final size = answer


# ─────────────────────────────────────────────
# OPTIMAL — Approach 3 (Fixed Window / No Shrink)
# O(n) time  |  O(1) space
# Avoids recalculating max_freq on shrink — cleaner and faster
# ─────────────────────────────────────────────
characterReplacement = characterReplacement_noShrink


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("AABABBA", 1, 4),
        ("ABAB",    2, 4),
        ("AAAA",    0, 4),
        ("AAAA",    2, 4),
        ("ABCDE",   1, 2),
        ("ABCDE",   4, 5),
        ("A",       0, 1),
        ("AABA",    0, 2),
        ("KRSCDCSONAJNHLBMDQGIFCPEKPOHQIHLTDIQGEKLRLPPGOOEFKPKR", 4, 6),
    ]

    solvers = [
        ("Brute Force",  characterReplacement_brute),
        ("Shrink",       characterReplacement_shrink),
        ("No Shrink",    characterReplacement_noShrink),
    ]

    for s, k, expected in tests:
        for name, fn in solvers:
            out = fn(s, k)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | s={s!r} k={k} | got={out}")
