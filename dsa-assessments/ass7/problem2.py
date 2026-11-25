# Problem 2: Longest consecutive elements sequence in O(n)


def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0

    for num in num_set:
        # Only start counting from the beginning of a sequence
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            longest = max(longest, length)
    return longest


def main():
    nums = list(map(int, input("Enter array elements (space separated): ").split()))
    print("Longest consecutive sequence length:", longest_consecutive(nums))


if __name__ == "__main__":
    main()
