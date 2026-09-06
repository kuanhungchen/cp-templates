from math import ceil, sqrt
from bisect import bisect_left, bisect_right


class SortedList:
    BUCKET_RATIO = 16
    SPLIT_RATIO = 24

    def __init__(self, nums=None):
        sorted_nums = sorted(nums) if nums is not None else []
        self._size = len(sorted_nums)
        self._build(sorted_nums)

    def _build(self, sorted_elements: list) -> None:
        n = self._size
        if n == 0:
            self._buckets = []
            return
        num_buckets = ceil(sqrt(n / self.BUCKET_RATIO))
        self._buckets = [
            sorted_elements[n * i // num_buckets : n * (i + 1) // num_buckets]
            for i in range(num_buckets)
        ]

    def __iter__(self):
        for bucket in self._buckets:
            yield from bucket

    def __reversed__(self):
        for bucket in reversed(self._buckets):
            yield from reversed(bucket)

    def __len__(self) -> int:
        return self._size

    def __eq__(self, other) -> bool:
        if isinstance(other, SortedList):
            return len(self) == len(other) and list(self) == list(other)
        return False

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({list(self)})"

    __repr__ = __str__

    def _find(self, x) -> tuple[list, int, int]:
        for i, bucket in enumerate(self._buckets):
            if x <= bucket[-1]:
                return (bucket, i, bisect_left(bucket, x))
        return (self._buckets[-1], len(self._buckets) - 1, len(self._buckets[-1]))

    def __contains__(self, x) -> bool:
        if self._size == 0:
            return False
        bucket, _, i = self._find(x)
        return i < len(bucket) and bucket[i] == x

    def add(self, x) -> None:
        if self._size == 0:
            self._buckets = [[x]]
            self._size = 1
            return
        bucket, bi, i = self._find(x)
        bucket.insert(i, x)
        self._size += 1
        if len(bucket) > len(self._buckets) * self.SPLIT_RATIO:
            mid = len(bucket) >> 1
            self._buckets[bi: bi + 1] = [bucket[:mid], bucket[mid:]]

    def discard(self, x) -> bool:
        if self._size == 0:
            return False
        bucket, bi, i = self._find(x)
        if i == len(bucket) or bucket[i] != x:
            return False
        self._pop(bucket, bi, i)
        return True

    def _pop(self, bucket, bi, i):
        res = bucket.pop(i)
        self._size -= 1
        if not bucket:
            del self._buckets[bi]
        return res

    def lt(self, x):
        for bucket in reversed(self._buckets):
            if bucket[0]  < x:
                return bucket[bisect_left(bucket, x) - 1]
        return None

    def le(self, x):
       for bucket in reversed(self._buckets):
           if bucket[0] <= x:
               return bucket[bisect_right(bucket, x) - 1]
       return None

    def gt(self, x):
        for bucket in self._buckets:
            if bucket[-1] > x:
                return bucket[bisect_right(bucket, x)]
        return None

    def ge(self, x):
        for bucket in self._buckets:
            if bucket[-1] >= x:
                return bucket[bisect_left(bucket, x)]
        return None

    def __getitem__(self, i_: int):
        i = i_
        if i < 0:
            i += self._size
        if i < 0 or i >= self._size:
            raise IndexError(f"Index {i_} out of range")
        for bucket in self._buckets:
            if i < len(bucket):
                return bucket[i]
            i -= len(bucket)

    def pop(self, i_: int = -1):
        i = i_
        if i < 0:
            i += self._size
        if i < 0 or i >= self._size:
            raise IndexError(f"Index {i_} out of range")
        for bi, bucket in enumerate(self._buckets):
            if i < len(bucket):
                return self._pop(bucket, bi, i)
            i -= len(bucket)

    def bisect_left(self, x) -> int:
        cnt = 0
        for bucket in self._buckets:
            if bucket[-1] >= x:
                return cnt + bisect_left(bucket, x)
            cnt += len(bucket)
        return cnt

    index = bisect_left

    def bisect_right(self, x) -> int:
        cnt = 0
        for bucket in self._buckets:
            if bucket[-1] > x:
                return cnt + bisect_right(bucket, x)
            cnt += len(bucket)
        return cnt

    def irange(self, left, right) -> range:
        # Returns the index range of elemetns in [left, right].
        return range(self.bisect_left(left), self.bisect_right(right))


class SortedSet:
    def __init__(self, nums=None):
        unique = sorted(set(nums)) if nums is not None else []
        self._list = SortedList(unique)

    def add(self, x) -> bool:
        if x in self._list:
            return False
        self._list.add(x)
        return True

    def discard(self, x) -> bool:
        return self._list.discard(x)

    def count(self, x) -> int:
        return 1 if x in self._list else 0

    def bisect_left(self, x) -> int:
        return self._list.bisect_left(x)

    def bisect_right(self, x) -> int:
        return self._list.bisect_right(x)

    def lt(self, x):
        return self._list.lt(x)

    def le(self, x):
        return self._list.le(x)

    def gt(self, x):
        return self._list.gt(x)

    def ge(self, x):
        return self._list.ge(x)

    def irange(self, left, right):
        return self._list.irange(left, right)

    def pop(self, i=-1):
        return self._list.pop(i)

    def __getitem__(self, i):
        return self._list[i]

    def __len__(self) -> int:
        return len(self._list)

    def __eq__(self, other) -> bool:
        if isinstance(other, SortedSet):
            return len(self) == len(other) and list(self) == list(other)
        return False

    def __contains__(self, x):
        return x in self._list

    def __iter__(self):
        return iter(self._list)

    def __reversed__(self):
        return reversed(self._list)

    def __str__(self):
        return f"SortedSet({list(self)})"

    __repr__ = __str__


class SortedDict:
    def __init__(self, pairs=None):
        self._map = {}
        self._keys = SortedList()
        if pairs:
            for k, v in pairs:
                self[k] = v

    def __setitem__(self, key, value):
        if key not in self._map:
            self._keys.add(key)
        self._map[key] = value

    def __getitem__(self, key):
        return self._map[key]

    def __delitem__(self, key):
        if key in self._map:
            del self._map[key]
            self._keys.discard(key)

    def pop(self, key, default=...):
        if key in self._map:
            val = self._map.pop(key)
            self._keys.discard(key)
            return val
        if default is not ...:
            return default
        raise KeyError(key)

    def peekitem(self, index=-1):
        key = self._keys[index]
        return key, self._map[key]

    def keys(self):
        return self._keys

    def values(self):
        for k in self._keys:
            yield self._map[k]

    def items(self):
        for k in self._keys:
            yield k, self._map[k]

    def bisect_left(self, key) -> int:
        return self._keys.bisect_left(key)

    def bisect_right(self, key) -> int:
        return self._keys.bisect_right(key)

    def __contains__(self, key):
        return key in self._map

    def __len__(self):
        return len(self._map)

    def __eq__(self, other) -> bool:
        if isinstance(other, SortedDict):
            return self._map == other._map
        return False

    def __iter__(self):
        return iter(self._keys)

    def __reversed__(self):
        return reversed(self._keys)

    def __str__(self):
        items_str = ", ".join(f"{k!r}: {self._map[k]!r}" for k in self._keys)
        return f"SortedDict({{{items_str}}})"

    __repr__ = __str__
