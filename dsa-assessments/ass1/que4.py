def trap_rain_water(arr, n):
    if n < 3:
        return 0

    left, right = 0, n - 1
    left_max, right_max = 0, 0
    water = 0

    while left < right:
        if arr[left] <= arr[right]:
            left_max = max(left_max, arr[left])
            water += left_max - arr[left]
            left += 1
        else:
            right_max = max(right_max, arr[right])
            water += right_max - arr[right]
            right -= 1

    return water

n = int(input())
arr = list(map(int, input().split()))
result = trap_rain_water(arr, n)
print(result)