# Problem 1: Length of the longest common subsequence of two strings


def longest_common_subsequence(text1, text2):
    rows, cols = len(text1), len(text2)
    # dp[i][j] = LCS length of text1[:i] and text2[:j]
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]

    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[rows][cols]


def main():
    text1 = input("Enter text1: ").strip()
    text2 = input("Enter text2: ").strip()
    print("Length of longest common subsequence:", longest_common_subsequence(text1, text2))


if __name__ == "__main__":
    main()
