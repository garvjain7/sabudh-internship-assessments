def next_permutation(nums, n):
    # Step 1: Find pivot - first index from right where nums[i] < nums[i+1]
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    # Step 2: If pivot exists, find rightmost element greater than nums[i]
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # Step 3: Swap pivot and successor
        nums[i], nums[j] = nums[j], nums[i]

    # Step 4: Reverse the suffix after pivot (make it ascending)
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

    return nums

n = int(input())
nums = list(map(int, input().replace(",", " ").split()))
result = next_permutation(nums, n)
print(*result)