class SegTree:
    def __init__(self, n, nums=None):
        self.FUNC = min
        self.DFLT = 1 << 60

        self.n = n
        self.k = (n - 1).bit_length()
        self.n2 = 1 << self.k
        self.arr = arr = [self.DFLT for _ in range(1 << (self.k + 1))]
        if nums:
            for i in range(self.n):
                arr[self.n2 + i] = nums[i]
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
