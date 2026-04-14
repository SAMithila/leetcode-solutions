# 001. Two Sum
# Difficulty: Easy
# Approach: Hash Map - O(n) time, O(n) space

def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
