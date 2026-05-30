"""
LeetCode 567 - Permutation in String
Given two strings s1 and s2, return True if s2 contains a permutation
of s1 as a substring, False otherwise.

Example:
  Input:  s1 = "ab", s2 = "eidbaooo"
  Output: True   ("ba" is a permutation of "ab")

  Input:  s1 = "ab", s2 = "eidboaoo"
  Output: False

KEY INSIGHT:
  A permutation has the same character frequencies as the original.
  So instead of generating permutations, slide a fixed window of
  len(s1) over s2 and compare frequency counts.
"""


# ─────────────────────────────────────────────
# Approach 1: Brute Force (Sort each window)
# Time:  O(n * k log k)  — k = len(s1), n = len(s2)
# Space: O(k)
# ─────────────────────────────────────────────

def checkInclusion_brute(s1: str, s2: str) -> bool:
    k = len(s1)
    target = sorted(s1)              # sorted s1 is our comparison target

    for i in range(len(s2) - k + 1):
        window = s2[i:i + k]         # extract fixed-size window
        if sorted(window) == target: # sort & compare — same chars = permutation
            return True

    return False


# ─────────────────────────────────────────────
# Approach 2: Sliding Window + Frequency Dicts
# Time:  O(n)
# Space: O(1)  — at most 26 keys in each dict
#
# Same idea as arrays but cleaner — dicts only hold distinct chars.
# Delete a key when its count hits 0 so equality check is accurate.
# ─────────────────────────────────────────────
def checkInclusion_freq(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False

    # Count letters in s1
    s1_count = {}
    for ch in s1:
        s1_count[ch] = s1_count.get(ch, 0) + 1
    
    # Count letters in first window of s2
    window_count = {}
    for ch in s2[:len(s1)]:
        window_count[ch] = window_count.get(ch, 0) + 1
    
    # Check if first window matches
    if window_count == s1_count:
        return True
    
    # Slide the window
    for i in range(len(s1), len(s2)):
        # Add new character (entering window)
        new_char = s2[i]
        window_count[new_char] = window_count.get(new_char, 0) + 1
        
        # Remove old character (leaving window)
        old_char = s2[i - len(s1)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]
        
        # Check if window matches
        if window_count == s1_count:
            return True
    
    return False

'''
# ─────────────────────────────────────────────
# Approach 3: Sliding Window + Match Counter
# Time:  O(n)
# Space: O(1)
#
# Avoid the O(26) array comparison each step.
# Track `matches`: how many of the 26 chars have equal frequency
# in s1 and the current window. When matches == 26, found it.
#
# On each slide:
#   - Adding right char may increase or decrease matches
#   - Removing left char may increase or decrease matches
# ─────────────────────────────────────────────
def checkInclusion_matches(s1: str, s2: str) -> bool:
    k = len(s1)
    if k > len(s2):
        return False

    freq_s1  = [0] * 26
    freq_win = [0] * 26

    for i in range(k):
        freq_s1[ord(s1[i]) - ord('a')] += 1
        freq_win[ord(s2[i]) - ord('a')] += 1

    # Count how many chars already match between s1 and first window
    matches = sum(1 for i in range(26) if freq_s1[i] == freq_win[i])

    if matches == 26:
        return True

    for right in range(k, len(s2)):
        # --- Add right char ---
        r = ord(s2[right]) - ord('a')
        freq_win[r] += 1
        if freq_win[r] == freq_s1[r]:
            matches += 1             # adding this char made it match
        elif freq_win[r] - 1 == freq_s1[r]:
            matches -= 1             # it was matching before, now over-counted

        # --- Remove left char (outgoing) ---
        l = ord(s2[right - k]) - ord('a')
        freq_win[l] -= 1
        if freq_win[l] == freq_s1[l]:
            matches += 1             # removing this char made it match
        elif freq_win[l] + 1 == freq_s1[l]:
            matches -= 1             # it was matching before, now under-counted

        if matches == 26:
            return True

    return False
'''

# ─────────────────────────────────────────────
# OPTIMAL — Approach 3 (Match Counter)
# O(n) time  |  O(1) space
# Each step updates exactly 2 chars instead of comparing 26
# ─────────────────────────────────────────────
# checkInclusion = checkInclusion_matches


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("ab",  "eidbaooo",  True),
        ("ab",  "eidboaoo",  False),
        ("adc", "dcda",      True),
        ("a",   "ab",        True),
        ("ab",  "ab",        True),
        ("abc", "bbbca",     True),
        ("abc", "bbbcaa",    True),
        ("hello", "ooolleoooleh", False),
        ("abc", "xyz",       False),
        ("ab",  "a",         False),   # s1 longer than s2
    ]

    solvers = [
        ("Brute Force",   checkInclusion_brute),
        ("Freq Arrays",   checkInclusion_freq),
     #   ("Match Counter", checkInclusion_matches),
    ]

    for s1, s2, expected in tests:
        for name, fn in solvers:
            out = fn(s1, s2)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | s1={s1!r} s2={s2!r} | got={out}")
