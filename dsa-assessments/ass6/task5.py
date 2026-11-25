def insert_interval(intervals, new_interval):
    result = []
    new_start, new_end = new_interval
    index, count = 0, len(intervals)

    while index < count and intervals[index][1] < new_start:
        result.append(intervals[index])
        index += 1

    while index < count and intervals[index][0] <= new_end:
        new_start = min(new_start, intervals[index][0])
        new_end = max(new_end, intervals[index][1])
        index += 1
    result.append([new_start, new_end])

    result.extend(intervals[index:])
    return result


count = int(input())
intervals = [list(map(int, input().split())) for _ in range(count)]
new_interval = list(map(int, input().split()))
print(insert_interval(intervals, new_interval))
