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
