class Mo:
    def __init__(self, n):
        self.n = n
        self.q = 0

        self.queries = []

    def add_query(self, ql, qr):
        # [ql, qr]
        self.queries.append((ql, qr))
        self.q += 1

    def solve(self):
        def add(idx):
            raise NotImplementedError

        def remove(idx):
            raise NotImplementedError

        def out(idx):
            raise NotImplementedError

        queries = self.queries
        SZ = 128
        NUM = (self.n + SZ - 1) // SZ
        B = [[] for _ in range(NUM)]

        for qi, (ql, qr) in enumerate(queries):
            B[ql // SZ].append(qi)

        for bi in range(NUM):
            B[bi].sort(key=lambda qi: queries[qi][1], reverse=bool(bi & 1))

        L, R = 0, -1
        ans = [0 for _ in range(self.q)]
        for qis in B:
            for qi in qis:
                ql, qr = queries[qi]
                for i in range(L, ql): remove(i)
                for i in range(R, qr, -1): remove(i)
                for i in range(R + 1, qr + 1): add(i)
                for i in range(L - 1, ql - 1, -1): add(i)
                L, R = ql, qr
                out(qi)
        return ans
