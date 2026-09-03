def longest_common_substring(s, t):
    # Returns (a, b, c, d) where s[a:b] = t[c:d]. O(MN)
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    s_end = t_end = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    s_end = i; t_end = j
            else:
                dp[i][j] = 0

    s_start = s_end - max_len
    t_start = t_end - max_len
    return s_start, s_end, t_start, t_end
