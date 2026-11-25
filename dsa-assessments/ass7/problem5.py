# Problem 5: Smallest missing non-negative element in a sorted array (binary search)


def smallest_missing(nums):
    low, high = 0, len(nums) - 1

    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == mid:
            low = mid + 1      # everything up to mid is present
        else:
            high = mid - 1     # a gap exists at or before mid
    return low


def main():
    nums = list(map(int, input("Enter sorted array elements (space separated): ").split()))
    print("The smallest missing element is", smallest_missing(nums))


if __name__ == "__main__":
    main()
