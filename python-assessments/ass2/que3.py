def count_pairs(arr, k):
    count = 0
    frequency = {}

    for num in arr:
        complement = k - num

        if complement in frequency:
            count += frequency[complement]

        frequency[num] = frequency.get(num, 0) + 1

    return count


arr = list(map(int, input().split(",")))
k = int(input())

print(count_pairs(arr, k))