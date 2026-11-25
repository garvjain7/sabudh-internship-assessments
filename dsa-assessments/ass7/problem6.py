# Problem 6: Minimum operations (insert, delete, replace) to convert word1 to word2


def edit_distance(word1, word2):
    rows, cols = len(word1), len(word2)
    # dp[i][j] = min operations to convert word1[:i] to word2[:j]
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]

    for i in range(rows + 1):
        dp[i][0] = i          # delete all i characters
    for j in range(cols + 1):
        dp[0][j] = j          # insert all j characters

    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],       # delete
                                   dp[i][j - 1],       # insert
                                   dp[i - 1][j - 1])   # replace
    return dp[rows][cols]


def main():
    word1 = input("Enter word1: ").strip()
    word2 = input("Enter word2: ").strip()
    print("Minimum number of operations:", edit_distance(word1, word2))


if __name__ == "__main__":
    main()
