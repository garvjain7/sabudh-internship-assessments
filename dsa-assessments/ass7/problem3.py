# Problem 3: Longest strictly increasing subsequence in O(n log n)
from bisect import bisect_left


def longest_increasing_subsequence(nums):
    # tails[i] = smallest possible tail of an increasing subsequence of length i + 1
    tails = []

    for num in nums:
        position = bisect_left(tails, num)
        if position == len(tails):
            tails.append(num)
        else:
            tails[position] = num
    return len(tails)


def main():
    nums = list(map(int, input("Enter array elements (space separated): ").split()))
    print("Length of longest increasing subsequence:", longest_increasing_subsequence(nums))


if __name__ == "__main__":
    main()
