def merge_intervals(intervals):
    intervals.sort()
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


count = int(input())
intervals = [list(map(int, input().split())) for _ in range(count)]
print(merge_intervals(intervals))
