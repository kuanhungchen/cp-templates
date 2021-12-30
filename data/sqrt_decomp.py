class SQRTDecomp:
    def __init__(self, nums):
        self.FUNC = lambda a, b: a + b
        self.DFLT = 0
        self.SZ = int(pow(len(nums), 0.5))  # block size

        self.nums = nums[:]
        self.bids = [0 for _ in range(len(nums))]  # block id
        self.arr = [self.DFLT for _ in range((len(nums) // self.SZ) + 1)]
        self.lzy = [0 for _ in range((len(nums) // self.SZ) + 1 )]  # rgadd
        self.lzy2 = [None for _ in range((len(nums) // self.SZ) + 1)]  # rgassign
        self.__build()

    def ptadd(self, idx, dlt):
        bid = self.bids[idx]
        self.arr[bid] = self.FUNC(self.arr[bid], dlt)
        self.nums[idx] += dlt

    def ptassign(self, idx, val):
        self.ptadd(idx, val - self.nums[idx])

    def rgadd(self, ql, qr, dlt):
        # [ql, qr]
        lid, rid = self.bids[ql], self.bids[qr]
        self.__update(lid); self.__update(rid)

        if lid == rid:
            for idx in range(ql, qr + 1):
                self.ptadd(idx, dlt)
        else:
            for idx in range(ql, (lid + 1) * self.SZ):
                self.ptadd(idx, dlt)
            for bid in range(lid + 1, rid):
                self.lzy[bid] += dlt
            for idx in range(rid * self.SZ, qr + 1):
                self.ptadd(idx, dlt)

    def rgassign(self, ql, qr, val):
        # [ql, qr]
        lid, rid = self.bids[ql], self.bids[qr]
        self.__update(lid); self.__update(rid)

        if lid == rid:
            for idx in range(ql, qr + 1):
                self.ptassign(idx, val)
        else:
            for idx in range(ql, (lid + 1) * self.SZ):
                self.ptassign(idx, val)
            for bid in range(lid + 1, rid):
                self.lzy[bid] = 0
                self.lzy2[bid] = val
            for idx in range(rid * self.SZ, qr + 1):
                self.ptassign(idx, val)

    def query(self, ql, qr):
        # [ql, qr]
        lid, rid = self.bids[ql], self.bids[qr]
        self.__update(lid); self.__update(rid)
        ans = self.DFLT

        if lid == rid:
            for idx in range(ql, qr + 1):
                ans = self.FUNC(ans, self.nums[idx])
        else:
            for idx in range(ql, (lid + 1) * self.SZ):
                ans = self.FUNC(ans, self.nums[idx])
            for bid in range(lid + 1, rid):
                ans = self.FUNC(ans, self.FUNC(self.arr[bid] if not self.lzy2[bid] \
                                else self.lzy2[bid] * self.SZ, self.lzy[bid] * self.SZ))
            for idx in range(rid * self.SZ, qr + 1):
                ans = self.FUNC(ans, self.nums[idx])
        return ans

    def __update(self, bid):
        if self.lzy2[bid]:
            for idx in range(bid * self.SZ, (bid + 1) * self.SZ):
                self.ptassign(idx, self.lzy2[bid])
        if self.lzy[bid]:
            for idx in range(bid * self.SZ, (bid + 1) * self.SZ):
                self.ptadd(idx, self.lzy[bid])
        self.lzy[bid] = 0
        self.lzy2[bid] = None

    def __build(self):
        for i in range(len(self.nums)):
            self.bids[i] = i // self.SZ
            self.arr[self.bids[i]] = self.FUNC(self.arr[self.bids[i]], self.nums[i])
