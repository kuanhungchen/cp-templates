from fenwick import Fenwick

class OrderedSet:
    def __init__(self, n, nums=None):
        # nums should be frequency array
        self.n = n
        self.fenw = Fenwick(n, nums)

    def __contains__(self, val):
        return bool(self.fenw.query(val, val + 1))

    def __len__(self):
        return self.fenw.pref(self.n)

    def add(self, val):
        if val in self: return False
        self.fenw.add(val, 1)
        return True

    def remove(self, val):
        if val not in self: return False
        self.fenw.add(val, -1)
        return True

    def count(self, val):
        return self.fenw.query(val, val + 1)

    def get(self, idx):
        # return value with given rank, 0-indexed and can be negative
        sz = len(self)
        if not (-sz <= idx < sz): return -1
        if idx < 0: return self.get(sz + idx)
        return self.fenw.bisect_left(idx + 1)

    def rank(self, val):
        # return rank of given value which should have already existed
        if val not in self: return -1
        return self.fenw.pref(val)

    def median(self, ceil=False):
        sz = len(self)
        if sz == 0: return -1
        if sz % 2 == 1 or ceil:
            return self.get(sz // 2)
        return self.get((sz - 1) // 2)

    @property
    def max(self):
        return self.get(-1)

    @property
    def min(self):
        return self.get(0)

    def pre(self, val):
        # return largest value less than or equal to val
        ans = self.fenw.bisect_left(self.fenw.pref(val + 1))
        return ans

    def nxt(self, val):
        # return smallest value greater than or equal to val
        ans = self.fenw.bisect_right(self.fenw.pref(val))
        return ans if ans != self.n else -1
