# You are given an integer array nums of length n and an integer target.

# Find three integers at distinct indices in nums such that the sum is closest to target.

# Return the sum of the three integers.

# You may assume that each input would have exactly one solution.

 

# Example 1:

# Input: nums = [-1,2,1,-4], target = 1
# Output: 2
# Explanation: The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
# Example 2:

# Input: nums = [0,0,0], target = 1
# Output: 0
# Explanation: The sum that is closest to the target is 0. (0 + 0 + 0 = 0).
 

# Constraints:

# 3 <= nums.length <= 500
# -1000 <= nums[i] <= 1000
# -104 <= target <= 104

def threeSumClosest(nums, target):
    nums.sort()
    n = len(nums)

    closest = nums[0] + nums[1] + nums[2]

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if abs(total - target) < abs(closest - target): # important condition
                closest = total
                
            if total < target:
                left += 1
            elif total > target:
                right -= 1
            else:
                return target

    return closest

nums = list(map(int, input().replace(",", " ").split()))
target = int(input())
print(threeSumClosest(nums, target))