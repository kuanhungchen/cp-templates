def swaps(s, t):
    # return adjacent swaps to convert s to t, which are perm of each other
    assert len(s) == len(t)
    assert set(s) == set(t)
    ans = 0
    cs = list(s)
    for i in range(len(s)):
        j = i
        while cs[i] != t[i]:
            ans += 1
            j += 1
            cs[i], cs[j] = cs[j], cs[i]
    return ans
