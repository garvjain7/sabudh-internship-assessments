def longest_subarray(arr, k):
    prefix_sum = 0
    max_length = 0
    first_occurrence = {}

    for i in range(len(arr)):
        prefix_sum += arr[i]

        if prefix_sum == k:
            max_length = i + 1

        if prefix_sum - k in first_occurrence:
            length = i - first_occurrence[prefix_sum - k]
            max_length = max(max_length, length)

        if prefix_sum not in first_occurrence:
            first_occurrence[prefix_sum] = i

    return max_length


arr = list(map(int, input().split()))
k = int(input())

print(longest_subarray(arr, k))