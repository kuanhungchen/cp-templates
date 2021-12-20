class Fenwick:
    def __init__(self, n, nums=None):
        self.n = n
        self.LOGN = self.n.bit_length()
        self.arr = []
        if nums is not None: self.__build(nums)

    def add(self, idx, dlt):
        while idx < self.n:
            self.arr[idx] += dlt
            idx |= idx + 1

    def query(self, ql, qr):
        # [ql, qr)
        return self.pref(qr) - self.pref(ql)

    def pref(self, qr):
        # [0, qr)
        ans = 0
        while qr:
            ans += self.arr[qr - 1]
            qr &= qr - 1
        return ans

    def suff(self, ql):
        # [ql, n)
        return self.pref(self.n) - self.pref(ql)

    def bisect_left(self, val):
        # first idx s.t. sum[0, idx) >= val
        idx = -1
        for k in range(self.LOGN - 1, -1, -1):
            right_idx = idx + (1 << k)
            if right_idx < self.n and self.arr[right_idx] <= val:
                idx = right_idx; val -= self.arr[idx]
        return idx + 1

    def __build(self, nums):
        self.arr = nums.copy()
        for i in range(self.n):
            j = i | (i + 1)
            if j < self.n: self.arr[j] += self.arr[i]
