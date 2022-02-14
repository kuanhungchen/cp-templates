def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def exgcd(a, b):
    if b:
        g, y, x = exgcd(b, a % b)
        y -= x * (a // b)
        return (g, x, y)
    return (a, 1, 0)

def lcm(a, b):
    return a // gcd(a, b) * b

def common_gcd(nums):
    # O(n*sqrt(v))
    MAXV = 10 ** 6
    divisors = [0 for _ in range(MAXV + 5)]
    for num in nums:
        div = 1
        while div * div <= num:
            if num % div == 0:
                divisors[div] += 1
                divisors[num // div] += int(div * div != num)
            div += 1
    return next(v for v in range(MAXV, 0, -1) if divisors[v] >= 2)

def common_gcd_fast(nums):
    # O(vlogv)
    MAXV = 10 ** 6
    freq = [0 for _ in range(MAXV + 5)]
    for num in nums: freq[num] += 1
    return next(v for v in range(MAXV, 0, -1) if sum(freq[v::v]) >= 2)
