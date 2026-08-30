class LazySegTree:
    def __init__(self, n):
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

        self.n = n

        self.lc = [0]
        self.rc = [0]
        self.t = [self.DFLT]
        self.d = [self.DFLT_TAG]

        self.root = self.__new_node()

    def __new_node(self):
        self.lc.append(0)
        self.rc.append(0)
        self.t.append(self.DFLT)
        self.d.append(self.DFLT_TAG)
        return len(self.t) - 1

    def __apply(self, p, tag, length):
        self.t[p] = self.APLY(tag, self.t[p], length)
        self.d[p] = self.COMP(tag, self.d[p])

    def __push(self, p, l, r):
        if self.d[p] != self.DFLT_TAG and l < r:
            mid = l + (r - l) // 2

            # Create child nodes if they do not exist
            if not self.lc[p]:
                self.lc[p] = self.__new_node()
            if not self.rc[p]:
                self.rc[p] = self.__new_node()

            tag = self.d[p]
            self.__apply(self.lc[p], tag, mid - l + 1)
            self.__apply(self.rc[p], tag, r - mid)
            self.d[p] = self.DFLT_TAG

    def range_update(self, ql, qr, tag):
        # [ql, qr]
        def __range_update(ql, qr, tag, l, r, p):
            if ql <= l and r <= qr:
                self.__apply(p, tag, r - l + 1)
                return
            self.__push(p, l, r)
            mid = l + (r - l) // 2
            if ql <= mid:
                if not self.lc[p]:
                    self.lc[p] = self.__new_node()
                __range_update(ql, qr, tag, l, mid, self.lc[p])
            if mid + 1 <= qr:
                if not self.rc[p]:
                    self.rc[p] = self.__new_node()
                __range_update(ql, qr, tag, mid + 1, r, self.rc[p])

            left_val = self.t[self.lc[p]] if self.lc[p] else self.DFLT
            right_val = self.t[self.rc[p]] if self.rc[p] else self.DFLT
            self.t[p] = self.FUNC(left_val, right_val)

        if ql <= qr:
            __range_update(ql, qr, tag, 0, self.n - 1, self.root)

    def query(self, ql, qr):
        # [ql, qr]
        def __query(ql, qr, l, r, p):
            if not p:
                return self.DFLT
            if ql <= l and r <= qr:
                return self.t[p]
            self.__push(p, l, r)
            mid = l + (r - l) // 2
            ans = self.DFLT
            if ql <= mid and self.lc[p]:
                ans = self.FUNC(ans, __query(ql, qr, l, mid, self.lc[p]))
            if mid + 1 <= qr and self.rc[p]:
                ans = self.FUNC(ans, __query(ql, qr, mid + 1, r, self.rc[p]))
            return ans

        if ql > qr:
            return self.DFLT
        return __query(ql, qr, 0, self.n - 1, self.root)
