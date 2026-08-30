def minimum_difference(arr, m):
    if m == 0 or m > len(arr):
        return -1

    arr.sort()
    minimum_diff = float("inf")

    for i in range(len(arr) - m + 1):
        difference = arr[i + m - 1] - arr[i]
        minimum_diff = min(minimum_diff, difference)

    return minimum_diff


arr = list(map(int, input().split(",")))
m = int(input())

print("Minimum Difference is", minimum_difference(arr, m))