class LazySegTree:
    def __init__(self, n, nums=None):
        # Function that combines two nodes
        self.FUNC = lambda a, b: a + b
        # Function that applies tag to val
        self.APLY = lambda tag, val, length: tag[0] * val + tag[1] * length
        # Function that composites old and new tags
        self.COMP = lambda new_t, old_t: (old_t[0] * new_t[0], \
                                            old_t[1] * new_t[0] + new_t[1])

        # Default value
        self.DFLT = 0
        # Default tag
        self.DFLT_TAG = (1, 0)

        self.n = n
        self.nums = []
        self.arr = [self.DFLT for _ in range(n << 2)]
        self.lzy = [self.DFLT_TAG for _ in range(n << 2)]
        if nums:
            self.nums = nums.copy()
            self.__build(0, n - 1)

    def __build(self, l, r, idx=1):
        if l == r:
            self.arr[idx] = self.nums[l]
            return
        mid = l + (r - l) // 2
        self.__build(l, mid, idx << 1)
        self.__build(mid + 1, r, idx << 1 | 1)
        self.arr[idx] = self.FUNC(self.arr[idx << 1], self.arr[idx << 1 | 1])

    def __push(self, idx, l, r):
        if self.lzy[idx] != self.DFLT_TAG and l < r:
            mid = l + (r - l) // 2
            len_l = mid - l + 1; len_r = r - mid
            new_tag = self.lzy[idx]
            self.arr[idx << 1] = self.APLY(new_tag, self.arr[idx << 1], len_l)
            self.lzy[idx << 1] = self.COMP(new_tag, self.lzy[idx << 1])

            self.arr[idx << 1 | 1] = self.APLY(new_tag, self.arr[idx << 1 | 1], len_r)
            self.lzy[idx << 1 | 1] = self.COMP(new_tag, self.lzy[idx << 1 | 1])

            self.lzy[idx] = self.DFLT_TAG

    def range_update(self, ql, qr, tag):
        def __range_update(ql, qr, tag, l, r, idx=1):
            if ql <= l and r <= qr:
                self.arr[idx] = self.APLY(tag, self.arr[idx], r - l + 1)
                self.lzy[idx] = self.COMP(tag, self.lzy[idx])
                return
            self.__push(idx, l, r)
            mid = l + (r - l) // 2
            if ql <= mid:
                __range_update(ql, qr, tag, l, mid, idx << 1)
            if mid + 1 <= qr:
                __range_update(ql, qr, tag, mid + 1, r, idx << 1 | 1)
            self.arr[idx] = self.FUNC(self.arr[idx << 1], self.arr[idx << 1 | 1])
        __range_update(ql, qr, tag, 0, self.n - 1)

    def query(self, ql, qr):
        def __query(ql, qr, l, r, idx=1):
            if ql <= l and r <= qr:
                return self.arr[idx]
            self.__push(idx, l, r)
            mid = l + (r - l) // 2
            ans = self.DFLT
            if ql <= mid:
                ans = self.FUNC(ans, __query(ql, qr, l, mid, idx << 1))
            if mid + 1 <= qr:
                ans = self.FUNC(ans, __query(ql, qr, mid + 1, r, idx << 1 | 1))
            return ans
        return __query(ql, qr, 0, self.n - 1)

    def bisect_left(self, val):
        # first index where prefix >= val
        if self.arr[1] < val:
            return self.n

        def __bisect_left(val, l, r, idx=1):
            if l == r:
                return l
            self.__push(idx, l, r)
            mid = l + (r - l) // 2

            if self.arr[idx << 1] >= val:
                return __bisect_left(val, l, mid, idx << 1)
            return __bisect_left(val - self.arr[idx << 1], mid + 1, r, idx << 1 | 1)

        return __bisect_left(val, 0, self.n - 1)
