def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def successful_pairs(spells, potions, success):
    potions.sort()
    m = len(potions)
    result = []

    for s in spells:
        threshold = (success + s - 1) // s
        idx = lower_bound(potions, threshold)
        result.append(m - idx)

    return result


spells = list(map(int, input().split()))
potions = list(map(int, input().split()))
success = int(input())

result = successful_pairs(spells, potions, success)

print(*result)