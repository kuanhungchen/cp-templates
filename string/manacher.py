def manacher(s):
    t = "#".join("^{}$".format(s))
    n = len(t)
    d1 = [0 for _ in range(n)]
    left, right = 0, -1
    for i in range(1, n - 1):
        if i < right: d1[i] = min(d1[left + right - i], right - i)
        while t[i + (d1[i] + 1)] == t[i - (d1[i] + 1)]:
            d1[i] += 1
        if i + d1[i] > right:
            left, right = i - d1[i], i + d1[i]
    maxl, cidx = max((l, i) for i, l in enumerate(d1))
    return s[(cidx - maxl) // 2:(cidx + maxl) // 2]
