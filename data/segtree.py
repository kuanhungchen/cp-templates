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
        for i in range(self.n2 - 1, 0, -1):
            self.arr[i] = self.FUNC(self.arr[i << 1], self.arr[i << 1 | 1])

    def getval(self, idx):
        return self.arr[self.n2 + idx]

    def getall(self):
        return self.arr[1]

    def getvals(self, ql, qr):
        # [ql, qr)
        return self.arr[self.n2 + ql:self.n2 + qr]

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

    def rightmost(self, ql, condition):
        # return first index idx such that [ql, idx] unsatisfies condition
        # bisect_left(val)  <-> lambda x: x <  val <-> sum of [l, idx] >= val
        # bisect_right(val) <-> lambda x: x <= val <-> sum of [l, idx] >  val
        if ql == self.n:
            return self.n
        idx = idx0 = ql + self.n2
        curv = self.DFLT
        while idx == idx0 or (idx & (idx - 1)):
            while not idx & 1:
                idx >>= 1
            if not condition(self.FUNC(curv, self.arr[idx])):
                while idx < self.n2:
                    idx <<= 1
                    if condition(self.FUNC(curv, self.arr[idx])):
                        curv = self.FUNC(curv, self.arr[idx])
                        idx += 1
                return idx - self.n2
            curv = self.FUNC(curv, self.arr[idx])
            idx += 1
        return self.n
