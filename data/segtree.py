class SegTree:
    def __init__(self, n, nums=None):
        self.FUNC = lambda a, b: a + b
        self.DFLT = 0

        self.n = n
        k = (n - 1).bit_length()
        self.n2 = 1 << k
        self.arr = arr = [self.DFLT for _ in range(1 << (k + 1))]
        if nums:
            arr[self.n2:self.n2 + n] = nums
            self.__build()

    def __build(self):
        for i in range(self.n2 - 1, -1, -1):
            self.arr[i] = self.FUNC(self.arr[i << 1], self.arr[i << 1 | 1])

    def getval(self, idx):
        return self.arr[self.n2 + idx]

    def ptassign(self, idx, val):
        i = idx + self.n2
        self.arr[i] = val
        while i:
            i >>= 1
            self.arr[i] = self.FUNC(self.arr[i << 1], self.arr[i << 1 | 1])

    def ptadd(self, idx, dlt):
        self.ptassign(idx, self.getval(idx) + dlt)

    def query(self, ql, qr):
        # [ql, qr)
        ql += self.n2
        qr += self.n2
        ans = self.DFLT
        while ql < qr:
            if ql & 1:
                ans = self.FUNC(ans, self.arr[ql])
                ql += 1
            if qr & 1:
                qr -= 1
                ans = self.FUNC(ans, self.arr[qr])
            ql >>= 1
            qr >>= 1
        return ans

    def bisect_left(self, val):
        # first index where prefix sum >= val
        if self.arr[1] < val:
            return self.n
        idx = 1
        while idx < self.n2:
            if self.arr[idx << 1] >= val:
                idx = idx << 1
            else:
                val -= self.arr[idx << 1]
                idx = idx << 1 | 1
        return idx - self.n2

    def bisect_right(self, val):
        # first index where prefix sum > val
        if self.arr[1] <= val:
            return self.n
        idx = 1
        while idx < self.n2:
            if self.arr[idx << 1] > val:
                idx = idx << 1
            else:
                val -= self.arr[idx << 1]
                idx = idx << 1 | 1
        return idx - self.n2
