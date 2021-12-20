def kmp(s, p):
    def get_pref_func(p):
        n = len(p)
        pref_func = [0 for _ in range(n)]
        for i in range(1, n):
            j = pref_func[i - 1]
            while j and s[i] != s[j]:
                j = pref_func[j - 1]
            pref_func[i] = j = j + (s[i] == s[j])
        return pref_func

    pref_func = get_pref_func(p)
    j = 0
    ans = []
    for i, c in enumerate(s):
        while j and p[j] != c:
            j = pref_func[j - 1]
        j += (p[j] == c)
        if j == len(p):
            ans.append(i - j + 1)
            j = pref_func[j - 1]
    return ans
