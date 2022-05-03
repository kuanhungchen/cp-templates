class Fenwick:
    def __init__(self, n, nums=None):
        self.n = n
        self.arr = [0 for _ in range(n + 1)]
        if nums:
            self.arr[1:] = nums
            self.__build()

    def __build(self):
        for i in range(1, self.n):
            if i + (i & -i) <= self.n:
                self.arr[i + (i & -i)] += self.arr[i]

    def add(self, idx, dlt):
        idx += 1
        while idx <= self.n:
            self.arr[idx] += dlt
            idx += idx & -idx

    def query(self, ql, qr):
        # [ql, qr)
        return self.pref(qr) - self.pref(ql)

    def pref(self, qr):
        # [0, qr)
        ans = 0
        while qr:
            ans += self.arr[qr]
            qr -= qr & -qr
        return ans

    def suff(self, ql):
        # [ql, n)
        return self.pref(self.n) - self.pref(ql)

    def bisect_left(self, val):
        # equivalent to bisect_left on prefix sums array
        idx = 0
        shift = 1 << self.n.bit_length()
        while shift:
            if idx + shift <= self.n and self.arr[idx + shift] < val:
                val -= self.arr[idx + shift]
                idx += shift
            shift >>= 1
        return idx if val else -1

    def bisect_right(self, val):
        # equivalent to bisect_right on prefix sums array
        idx = 0
        shift = 1 << self.n.bit_length()
        while shift:
            if idx + shift <= self.n and self.arr[idx + shift] <= val:
                val -= self.arr[idx + shift]
                idx += shift
            shift >>= 1
        return idx
