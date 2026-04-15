# 875. Koko Eating Bananas
# Difficulty: Medium
# Approach: Binary Search - O(n log m) time, O(1) space

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        result = r

        while l <= r:
            k = (l + r) // 2
            hours_needed = self.calculateHours(piles, k)

            if hours_needed <= h:
                result = k
                r = k - 1
            else:
                l = k + 1

        return result

    def calculateHours(self, piles: List[int], k: int) -> int:
        hours = 0
        for pile in piles:
            hours += (pile + k - 1) // k # Ceiling division

        return hours