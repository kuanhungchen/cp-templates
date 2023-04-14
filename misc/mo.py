class Mo:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.queries = []
        self.L = 0
        self.R = -1

    def add_query(self, ql, qr):
        # [ql, qr]
        self.queries.append((ql, qr))

    def _init(self):
        # TODO: add required information
        self.ans = [0 for _ in range(len(self.queries))]

    def _add(self, idx):
        # TODO: include self.arr[idx]
        _ = self.arr[idx]
        raise NotImplementedError

    def _rem(self, idx):
        # TODO: exclude self.arr[idx]
        _ = self.arr[idx]
        raise NotImplementedError

    def _out(self, qidx):
        # TODO: construct answer for a query
        self.ans[qidx] = 0
        raise NotImplementedError

    def _solve_bucket(self, ql, qr):
        for i in range(self.L, ql):
            self._rem(i)
        for i in range(self.R, qr, -1):
            self._rem(i)
        for i in range(self.R + 1, qr + 1):
            self._add(i)
        for i in range(self.L - 1, ql - 1, -1):
            self._add(i)

        self.L = ql
        self.R = qr

    def solve(self):
        self._init()

        queries = self.queries
        SZ = round(pow(len(queries), 0.5))
        NUM = (self.n + SZ - 1) // SZ
        BS = [[] for _ in range(NUM)]

        for qi, (ql, qr) in enumerate(queries):
            BS[ql // SZ].append(qi)

        for bi in range(NUM):
            BS[bi].sort(key=lambda qi: queries[qi][1], reverse=bool(bi & 1))

        for B in BS:
            for qi in B:
                ql, qr = queries[qi]
                self._solve_bucket(ql, qr)
                self._out(qi)

        return self.ans
