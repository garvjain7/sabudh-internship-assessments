def arrange_numbers(nums):
    position = 0

    for i in range(len(nums)):
        if nums[i] < 0:
            value = nums[i]
            j = i

            # Shift elements to maintain original order
            while j > position:
                nums[j] = nums[j - 1]
                j -= 1

            nums[position] = value
            position += 1

    return nums


nums = list(map(int, input().split(",")))
result = arrange_numbers(nums)

print(*result)