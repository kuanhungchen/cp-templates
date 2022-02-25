def kmp(s, p):
    n, m = len(s), len(p)
    pref_func = [0 for _ in range(m)]
    j = 0
    for i in range(1, m):
        while p[i] != p[j] and j:
            j = pref_func[j - 1]
        if p[i] == p[j]:
            j += 1
            pref_func[i] = j

    j = 0
    ans = []
    for i in range(n):
        while s[i] != p[j] and j:
            j = pref_func[j - 1]
        if s[i] == p[j]:
            j += 1
            if j == m:
                ans.append(i - j + 1)
                j = pref_func[j - 1]
    return ans
