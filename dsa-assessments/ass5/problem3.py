def maximal_rectangle(matrix):
    cols = len(matrix[0])
    heights = [0] * (cols + 1)
    best = 0
    for row in matrix:
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] == "1" else 0
        stack = [-1]
        for i in range(cols + 1):
            while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:
                h = heights[stack.pop()]
                best = max(best, h * (i - stack[-1] - 1))
            stack.append(i)
    return best


n = int(input())
matrix = ["".join(input().split()) for _ in range(n)]
print(maximal_rectangle(matrix))