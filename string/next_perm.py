def next_perm(s, k=1):
    # return the k-th lexicographically larger permutation of string s
    assert isinstance(s, str)
    cs = list(s)
    n = len(cs)
    for _ in range(k):
        for i in range(n - 2, -1, -1):
            if cs[i] < cs[i + 1]:
                j = i + 1
                while j < n and cs[i] < cs[j]: j += 1
                cs[i], cs[j - 1] = cs[j - 1], cs[i]
                for d in range(((n - 1) - (i + 1) + 1) // 2):
                    cs[i + 1 + d], cs[n - 1 - d] = cs[n - 1 - d], cs[i + 1 + d]
                break
    return "".join(cs)
