class PersistentSegTree:
    def __init__(self, n, nums=None):
        self.n = n
        self.tot = 0

        size = (n << 5) + 10
        self.lchd = [0] * size
        self.rchd = [0] * size
        self.sums = [0] * size

        self.vers = [0]

        if nums is not None:
            for num in nums:
                self.insert(num)

    def insert(self, val):
        def _insert(l, r, root, val):
            cur = self.tot = self.tot + 1
            self.lchd[cur] = self.lchd[root]
            self.rchd[cur] = self.rchd[root]
            self.sums[cur] = self.sums[root] + 1

            if l == r:
                return cur

            mid = l + (r - l) // 2
            if val <= mid:
                self.lchd[cur] = _insert(l, mid, self.lchd[cur], val)
            else:
                self.rchd[cur] = _insert(mid + 1, r, self.rchd[cur], val)
            return cur

        self.vers.append(_insert(0, self.n - 1, self.vers[-1], val))

    def query(self, ql, qr, k):
        # Returns k-th smallest element in [ql, qr] (1-indexed)
        def _query(u, v, l, r, k):
            if l == r:
                return l

            mid = l + (r - l) // 2
            now = self.sums[self.lchd[v]] - self.sums[self.lchd[u]]

            if k <= now:
                return _query(self.lchd[u], self.lchd[v], l, mid, k)
            return _query(self.rchd[u], self.rchd[v], mid + 1, r, k - now)

        return _query(self.vers[ql], self.vers[qr + 1], 0, self.n - 1, k)

