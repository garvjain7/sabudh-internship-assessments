def can_reach_last_index(nums):
    farthest = 0
    for index, jump in enumerate(nums):
        if index > farthest:
            return False
        farthest = max(farthest, index + jump)
    return True


nums = list(map(int, input().split()))
print("true" if can_reach_last_index(nums) else "false")
