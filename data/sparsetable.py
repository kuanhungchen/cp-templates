class SparseTable:
    def __init__(self, nums):
        self.FUNC = FUNC = max

        n = len(nums)
        self.lgs = lgs = [0 for _ in range(n + 1)]
        for i in range(2, n + 1):
            lgs[i] = lgs[i >> 1] + 1

        self.st = st = [list(nums)]
        i = 1
        while 2 * i <= n:
            prev = st[-1]
            st.append([FUNC(prev[j], prev[j + i]) for j in range(n - 2 * i + 1)])
            i <<= 1

    def query(self, ql, qr):
        # [ql, qr)
        depth = self.lgs[qr - ql]
        return self.FUNC(self.st[depth][ql], self.st[depth][qr - (1 << depth)])
