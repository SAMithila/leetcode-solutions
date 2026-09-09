"""
LeetCode 121 - Best Time to Buy and Sell Stock
You are given an array prices where prices[i] is the price of a given
stock on the i-th day. You want to maximize your profit by choosing a
single day to buy one stock and choosing a different day in the future
to sell that stock. Return the maximum profit you can achieve from this
transaction. If you cannot achieve any profit, return 0.

Example:
  Input:  prices = [7,1,5,3,6,4]
  Output: 5  (buy on day 2 at price 1, sell on day 5 at price 6)

  Input:  prices = [7,6,4,3,1]
  Output: 0  (no transaction is profitable)
"""


# ─────────────────────────────────────────────
# Approach 1: Brute Force
# Time:  O(n^2)  — check every buy/sell pair
# Space: O(1)
# ─────────────────────────────────────────────
def maxProfit_brute(prices: list[int]) -> int:
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


# ─────────────────────────────────────────────
# Approach 2: Sliding Window (track min price seen so far)
# Time:  O(n)
# Space: O(1)
#
# left = cheapest price seen so far, right = today's price.
# If today's price is a new low, move left up to it.
# Otherwise, check if selling today beats the best profit so far.
# ─────────────────────────────────────────────
def maxProfit(prices: list[int]) -> int:
    min_price = float("inf")
    best = 0

    for price in prices:
        if price < min_price:
            min_price = price
        else:
            best = max(best, price - min_price)

    return best


# ─── Tests ───────────────────────────────────
if __name__ == "__main__":
    tests = [
        ([7, 1, 5, 3, 6, 4], 5),
        ([7, 6, 4, 3, 1],    0),
        ([2, 4, 1],          2),
        ([1],                0),
        ([],                 0),
        ([3, 3, 3, 3],       0),
        ([1, 2],             1),
    ]

    solvers = [
        ("Brute Force",    maxProfit_brute),
        ("Sliding Window", maxProfit),
    ]

    for prices, expected in tests:
        for name, fn in solvers:
            out = fn(prices)
            status = "PASS" if out == expected else "FAIL"
            print(f"[{status}] {name} | prices={prices!r} | got={out}")
