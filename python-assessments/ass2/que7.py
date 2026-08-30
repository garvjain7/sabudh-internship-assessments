def rotate_matrix(matrix):
    n = len(matrix)

    # Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for row in matrix:
        row.reverse()

    return matrix


n = int(input())
matrix = []

for _ in range(n):
    matrix.append(list(map(int, input().split())))

print(rotate_matrix(matrix))