def floor_sum(n, m, a, b, k):
    # compute floor((ai + b) / m) for i in [k, n]
    def floor_sum_sub(n, m, a, b):
        # compute floor((ai + b) / m) for i in [0, n - 1]
        ans = 0
        while True:
            ans += ((n - 1) * n // 2) * (a // m)
            ans += n * (b // m)
            a %= m
            b %= m

            y = (a * n + b) // m
            if y == 0: break

            x = b - y * m
            ans += (n + x // a) * y
            a, b, m, n = m, x % a, a, y
        return ans

    ans = floor_sum_sub(n + 1, m, a, b)
    if k != 0: ans -= floor_sum_sub(k, m, a, b)
    return ans
        
