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
"""
## LC 424 — Longest Repeating Character Replacement (Interview Format)

---

### Step 1 — Understand & Restate

> "Given a string of uppercase letters and an integer k, I can change up to k characters
> to any other letter. I need the length of the longest substring that becomes all one
> repeated letter after doing that."

```
s = "AABABBA", k = 1

Try window "ABBA" (indices 3..6): majority letter B appears 2 times, window size 4,
so we need 4-2=2 replacements. Too many for k=1.

Try window "AABA" (indices 0..3): majority letter A appears 3 times, window size 4,
need 4-3=1 replacement. Fits k=1. ✓

Answer: 4
```

---

### Step 2 — Clarifying Questions

```
Q: What characters appear in s?        → Uppercase English letters only (26 max)
Q: Can k be 0?                         → Yes → substring must already be uniform
Q: Can k be >= len(s)?                 → Yes → answer is len(s)
Q: Empty string?                       → Not per constraints, but would return 0
Q: Does "longest substring" mean contiguous? → Yes, substring not subsequence
```

> "The key constraint is that a window of length L is achievable with k replacements
> exactly when L minus the count of its most frequent character is <= k. That's what
> makes this a sliding window problem instead of a brute force scan."

---

### Step 3 — Brute Force → Optimal

**Brute Force — O(n²)**

```python
# for every starting index, expand right until we exceed k replacements
for left in range(n):
    freq = {}
    max_freq = 0
    for right in range(left, n):
        freq[s[right]] += 1
        max_freq = max(max_freq, freq[s[right]])
        if (right - left + 1) - max_freq <= k:
            best = max(best, right - left + 1)
        else:
            break
```

> "This is O(n²) in the worst case — too slow for n up to 10^5. Since I only ever care
> about the longest valid window, I can slide a window across the string instead of
> restarting from every left."

**Why sliding window works here:**

```
Track max_freq = count of the most frequent letter seen in the current window.
A window of size W is valid iff W - max_freq <= k (replace all the "minority" letters).

We never need to shrink below the best window found so far — if a window becomes
invalid, sliding it forward by one (both pointers move) can only match or improve
on the best length, never make it worse. So both pointers only move forward → O(n).
```

---

### Step 4 — Edge Cases (say before coding)

```
1. k covers everything:     s="ABCDE", k=4      → return 5 (replace all but one)
2. k=0, no repeats:         s="ABCDE", k=0      → return 1
3. Already uniform:         s="AAAA", k=0       → return 4
4. Single character:        s="A", k=0          → return 1
5. k larger than needed:    s="AAAA", k=2       → return 4 (no replacement needed)
6. Long run with noise:     s="AABABBA", k=1    → return 4
```

---

### Step 5 — Code

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        freq = {}
        left = 0
        max_freq = 0

        for right in range(len(s)):
            ch = s[right]
            freq[ch] = freq.get(ch, 0) + 1
            max_freq = max(max_freq, freq[ch])   # best letter count seen in any window so far

            # window invalid → slide forward (don't shrink, just shift)
            if (right - left + 1) - max_freq > k:
                freq[s[left]] -= 1
                left += 1

        return len(s) - left   # window size never shrinks, so final size is the answer
```

---

### Step 6 — Dry Run (trace out loud)

```
s = "AABABBA", k = 1
left=0, max_freq=0, freq={}

right=0 'A': freq={A:1}          max_freq=1   size=1  1-1=0<=1  ok
right=1 'A': freq={A:2}          max_freq=2   size=2  2-2=0<=1  ok
right=2 'B': freq={A:2,B:1}      max_freq=2   size=3  3-2=1<=1  ok
right=3 'A': freq={A:3,B:1}      max_freq=3   size=4  4-3=1<=1  ok
right=4 'B': freq={A:3,B:2}      max_freq=3   size=5  5-3=2>1   SLIDE
             freq[s[0]]=freq[A]-=1 → {A:2,B:2}, left=1
right=5 'B': freq={A:2,B:3}      max_freq=3   size=5  5-3=2>1   SLIDE
             freq[s[1]]=freq[A]-=1 → {A:1,B:3}, left=2
right=6 'A': freq={A:2,B:3}      max_freq=3   size=5  5-3=2>1   SLIDE
             freq[s[2]]=freq[B]-=1 → {A:2,B:2}, left=3

len(s) - left = 7 - 3 = 4  ✓
```

---

### Step 7 — Complexity Analysis

**Time — O(n)**

```
right moves forward n times total  → O(n)
left  moves forward at most n times total (only on invalid windows) → O(n)
max_freq is never decreased on slide — that's fine, it only ever
under-reports a stale value, and an under-reported max_freq only
makes the invalid check stricter, never lets an invalid window pass.
```

**Space — O(1)**

```
freq map holds at most 26 uppercase letters → constant space
```

---

### Step 8 — Follow-up Questions & Answers

**Q: Why is it safe that max_freq never decreases, even after letters are slid out of the window?**

> "max_freq is a historical high-water mark, not necessarily the true max of the
> current window. But that's fine — we only use it to test whether the *current*
> window size can be valid. If max_freq is stale (too high), the check becomes
> stricter, so we might miss growing the window by one extra step in a rare edge
> case, but we can never report an answer larger than what's achievable, and it's
> provably true we never need to beat the previous best window's length anyway."

---

**Q: What if the alphabet included lowercase and uppercase (52 letters)?**

> "No change to the algorithm — freq dict handles any number of distinct characters,
> just update from O(26) to O(52) space, still O(1)."

---

**Q: What if we wanted the actual replaced substring, not just the length?**

> "Track the best (left, right) pair whenever we update the best length, then
> slice s[left:right+1] and figure out which characters differ from the majority
> letter in that window to know what to replace."

---

### Recap Card

```
Problem type:   Sliding Window (fixed/no-shrink variant)
Pattern:        Expand right, slide (not shrink) when invalid
Key constraint: window - max_freq <= k determines validity
Why not O(n²):  left never goes backward, max_freq never recomputed on slide

Time:    O(n)
Space:   O(1)  — at most 26 letters tracked

Edge cases:
  → k=0, no repeats     → answer is 1
  → k >= len(s)         → answer is len(s)
  → single character    → answer is 1

Recurring bugs to check:
  → right - left + 1 (not right - left) for window size
  → compare with `> k` to trigger slide (not `>= k`)
  → don't shrink the window on invalid — just slide (left += 1 once)
```
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
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        left = 0
        best = 0
        max_freq = 0
        
        for right in range(len(s)):
            # Add right character to window
            ch = s[right]
            count[ch] = count.get(ch, 0) + 1
            
            # Update max_freq
            max_freq = max(max_freq, count[ch])

            # Shirnk if invalid
            while (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1

            # Update best
            best = max(best, right - left + 1)

        return best


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
        ("Solution",     Solution().characterReplacement),
    ]

    for s, k, expected in tests:
        for name, fn in solvers:
            out = fn(s, k)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | s={s!r} k={k} | got={out}")
