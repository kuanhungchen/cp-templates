from fenwick import Fenwick
from typing import Iterator, List


class OrderedSet:
    def __init__(self, maxn: int, nums: List[int] | None = None):
        self._maxn = maxn  # nums can be only [0, maxn - 1]
        self._freq = [0 for _ in range(maxn)]
        if nums:
            for num in nums:
                self._check(num)
                self._freq[num] = 1
        self._fenw = Fenwick(maxn, self._freq)
        self._sz = self._fenw.pref(maxn)

    def __contains__(self, val: int) -> bool:
        self._check(val)
        return bool(self._freq[val])

    def __len__(self) -> int:
        return self._sz

    @property
    def max(self) -> int:
        return self.kth(-1)

    @property
    def min(self) -> int:
        return self.kth(0)

    def median(self, ceil: bool = False) -> int:
        # return median of elements, or -1 if not exists
        if self._sz & 1 or ceil: return self.kth(self._sz // 2)
        return self.kth((self._sz - 1) // 2)

    def add(self, val: int) -> bool:
        self._check(val)
        if val in self: return False
        self._fenw.add(val, 1)
        self._freq[val] = 1
        self._sz += 1
        return True

    def remove(self, val: int) -> bool:
        self._check(val)
        if val not in self: return False
        self._fenw.add(val, -1)
        self._freq[val] = 0
        self._sz -= 1
        return True

    def kth(self, k: int) -> int:
        # return element of rank k (0-indexed), or -1 if not exists
        if not -self._sz <= k < self._sz: return -1
        if k < 0: return self.kth(self._sz + k)
        return self._fenw.bisect_left(k + 1)

    def rank(self, val: int) -> int:
        # return the rank of val (0-indexed), or -1 if not exists
        self._check(val)
        if val not in self: return -1
        return self._fenw.pref(val)

    def pre(self, val: int) -> int:
        # reutrn first element <= val, or -1 if not exists
        self._check(val)
        ans = self._fenw.bisect_left(self._fenw.pref(val + 1))
        return ans

    def nxt(self, val: int) -> int:
        # return first element >= val, or -1 if not exists
        self._check(val)
        ans = self._fenw.bisect_right(self._fenw.pref(val))
        return ans if ans != self._maxn else -1

    def _check(self, val: int) -> None:
        if not 0 <= val < self._maxn:
            raise ValueError("{} not in [0, {}]".format(val, self._maxn - 1))

    def __repr__(self) -> str:
        return "OrderedSet({})".format(list(self))

    def __iter__(self) -> Iterator[int]:
        for val in range(self._maxn):
            for _ in range(self._freq[val]):
                yield val


class OrderedMultiSet(OrderedSet):
    def __init__(self, maxn: int, nums: List[int] | None = None):
        self._maxn = maxn  # nums can be only [0, maxn - 1]
        self._freq = [0 for _ in range(maxn)]
        if nums:
            for num in nums:
                self._check(num)
                self._freq[num] += 1
        self._fenw = Fenwick(maxn, self._freq)
        self._sz = self._fenw.pref(maxn)

    def count(self, val: int) -> int:
        # return occurence of val
        self._check(val)
        return self._fenw.query(val, val + 1)

    def update(self, val: int, delta: int) -> bool:
        # add or remove occurence of val
        self._check(val)
        if self.count(val) + delta < 0: return False
        self._fenw.add(val, delta)
        self._freq[val] += delta
        self._sz += delta
        return True

    def add(self, val: int) -> bool:
        return self.update(val, 1)

    def remove(self, val: int) -> bool:
        return self.update(val, -1)
