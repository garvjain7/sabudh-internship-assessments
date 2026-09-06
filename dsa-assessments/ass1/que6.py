def spiral_order(matrix, m, n):
    result = []
    top, bottom = 0, m - 1
    left, right = 0, n - 1

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result


m, n = map(int, input().split())
matrix = [list(map(int, input().replace(",", " ").split())) for _ in range(m)]

result = spiral_order(matrix, m, n)

print(*result)