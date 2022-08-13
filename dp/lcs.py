def lcs(s, t):
    m, n = len(s), len(t)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i, c1 in enumerate(s):
        row1 = dp[i]
        row2 = dp[i + 1]
        for j, c2 in enumerate(t):
            row2[j + 1] = row1[j] + 1 if c1 == c2 else max(row2[j], row1[j + 1])

    ans = []
    i, j = m, n
    while i and j:
        if dp[i][j] == dp[i - 1][j]:
            i -= 1
        elif dp[i][j] == dp[i][j - 1]:
            j -= 1
        else:
            ans.append(s[i - 1])
            i -= 1
            j -= 1
    return "".join(ans[::-1])
