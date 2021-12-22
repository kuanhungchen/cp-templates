def manacher(s):
    t = "#" + "#".join(list(s)) + "#"
    n = len(t)
    ans = ""
    d1 = [0 for _ in range(n)]
    l, r = 0, -1
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i)
        while 0 <= i - k and i + k < n and t[i - k] == t[i + k]:
            k += 1
        d1[i] = k
        k -= 1
        ans = max(ans, t[i - k:i + k + 1], key=len)
        if i + k > r:
            l, r = i - k, i + k
    return ans.replace("#", "")
