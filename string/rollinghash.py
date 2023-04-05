class RollingHash:
    def __init__(self, s, P=3001, MOD=1101001001):
        self.MOD = MOD

        orda = ord("a")

        self.ps = ps = [1]
        self.hs = hs = [0]
        for c in s:
            ps.append(ps[-1] * P % MOD)
            hs.append((hs[-1] * P + (ord(c) - orda + 1)) % MOD)

    @property
    def hashv(self):
        return self.hs[-1]

    def prefix(self, qr):
        # [0, qr)
        return self.get(0, qr)

    def get(self, ql, qr):
        # [ql, qr)
        ans = self.hs[qr] - self.hs[ql] * self.ps[qr - ql]
        return (ans + self.MOD) % self.MOD
