class LazySegTree:
    def __init__(self, n, nums=None):
        # Function that combines two nodes
        self.FUNC = lambda a, b: a + b
        # Function that applies tag to val
        self.APLY = lambda tag, val, length: tag[0] * val + tag[1] * length
        # Function that composites new and old tags
        self.COMP = lambda new_t, old_t: (new_t[0] * old_t[0], 
                                            new_t[0] * old_t[1] + new_t[1])
        # Default value
        self.DFLT = 0
        # Default tag
        self.DFLT_TAG = (1, 0)

        N = 1
        h = 0
        while N < n:
            N <<= 1
            h += 1
        self.n = n
        self.N = N
        self.h = h

        self.t = [self.DFLT] * (2 * N)
        self.d = [self.DFLT_TAG] * N

        self.node_len = [0] * (2 * N)
        for i in range(N, 2 * N):
            self.node_len[i] = 1
        for i in range(N - 1, 0, -1):
            self.node_len[i] = self.node_len[i << 1] + self.node_len[i << 1 | 1]

        if nums:
            for i in range(min(n, len(nums))):
                self.t[N + i] = nums[i]
            self.__rebuild()

    def __rebuild(self):
        t = self.t
        N = self.N
        for p in reversed(range(1, N)):
            t[p] = self.FUNC(t[p << 1], t[p << 1 | 1])

    def __apply(self, p, tag):
        self.t[p] = self.APLY(tag, self.t[p], self.node_len[p])
        if p < self.N:
            self.d[p] = self.COMP(tag, self.d[p])

    def __push(self, p):
        d = self.d
        h = self.h
        for s in range(h, 0, -1):
            i = p >> s
            if d[i] != self.DFLT_TAG:
                self.__apply(i << 1, d[i])
                self.__apply(i << 1 | 1, d[i])
                d[i] = self.DFLT_TAG

    def __build(self, p):
        t = self.t
        d = self.d
        while p > 1:
            p >>= 1
            combined = self.FUNC(t[p << 1], t[p << 1 | 1])
            t[p] = self.APLY(d[p], combined, self.node_len[p])

    def range_update(self, ql, qr, tag):
        # [ql, qr]
        if ql > qr:
            return
        l0 = ql + self.N
        r0 = qr + 1 + self.N
        
        self.__push(l0)
        self.__push(r0 - 1)
        
        l, r = l0, r0
        while l < r:
            if l & 1:
                self.__apply(l, tag)
                l += 1
            if r & 1:
                r -= 1
                self.__apply(r, tag)
            l >>= 1
            r >>= 1
            
        self.__build(l0)
        self.__build(r0 - 1)

    def query(self, ql, qr):
        # [ql, qr]
        if ql > qr:
            return self.DFLT
        l0 = ql + self.N
        r0 = qr + 1 + self.N
        
        self.__push(l0)
        self.__push(r0 - 1)
        
        res = self.DFLT
        l, r = l0, r0
        while l < r:
            if l & 1:
                res = self.FUNC(res, self.t[l])
                l += 1
            if r & 1:
                r -= 1
                res = self.FUNC(self.t[r], res)
            l >>= 1
            r >>= 1
        return res
