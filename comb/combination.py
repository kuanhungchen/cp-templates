class Combination:
    def __init__(self, n, MOD):
        self.f = f = [1 for _ in range(n + 1)]
        for i in range(2, n + 1):
            f[i] = f[i - 1] * i % MOD

        self.inv_f = inv_f = [0 for _ in range(n + 1)]
        inv_f[n] = pow(f[n], MOD - 2, MOD)
        for i in range(n - 1, -1, -1):
            inv_f[i] = inv_f[i + 1] * (i + 1) % MOD

        self.MOD = MOD

    def inv(self, k):
        # inverse(k)
        return (self.inv_f[k] * self.f[k - 1]) % self.MOD

    def fact(self, k):
        # k!
        return self.f[k]

    def inv_fact(self, k):
        # inerse(k!)
        return self.inv_f[k]

    def perm(self, k, r):
        # kPr
        if k < r: return 0
        return (self.f[k] * self.inv_f[k - r]) % self.MOD

    def comb(self, k, r):
        # kCr
        if k < r: return 0
        return (self.f[k] * self.inv_f[k - r] % self.MOD) * self.inv_f[r] % self.MOD


def comb(k, r):
    # kCr
    if k < r: return 0
    r = min(r, k - r)
    numer = denom = 1
    for l in range(1, r + 1):
        numer = (numer * (k - r + l))
        denom = (denom * l)
    return numer // denom

def comb_mod(k, r, MOD):
    # kCr
    if k < r: return 0
    r = min(r, k - r)
    numer = denom = 1
    for l in range(1, r + 1):
        numer = (numer * (k - r + l)) % MOD
        denom = (denom * l) % MOD
    return numer * pow(denom, MOD - 2, MOD) % MOD

def perm(k, r, MOD):
    # kPr
    if k < r: return 0
    res = 1
    for l in range(k - r + 1, k + 1):
        res = (res * l) % MOD
    return res
