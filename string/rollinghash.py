class RollingHash:
    def __init__(self, s, P=123457, MOD=1011001110001111):
        self.MOD = MOD

        orda = ord("a")

        self.ps = ps = [1]
        self.hs = hs = [0]
        for c in s:
            ps.append(ps[-1] * P % MOD)
            hs.append((hs[-1] * P + (ord(c) - orda + 1)) % MOD)

    def get(self, ql, qr):
        # [ql, qr)
        ans = self.hs[qr] - self.hs[ql] * self.ps[qr - ql]
        return (ans + self.MOD) % self.MOD
