def extgcd(a, b):
    if not b:
        return (a, 1, 0)
    g, y, x = extgcd(b, a % b)
    y -= (a // b) * x
    return (g, x, y)

def inverse(a, mod):
    g, x, _ = extgcd(a % mod, mod)
    return (x + mod) % mod if g == 1 else -1

def inverse_prime(a, mod):
    # mod needs to be prime
    return pow(a, mod - 2, mod)
