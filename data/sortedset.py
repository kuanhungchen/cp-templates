from math import ceil, sqrt
from bisect import bisect_left, bisect_right


class SortedSet:
    BUCKET_RATIO = 16
    SPLIT_RATIO = 32

    def __init__(self, nums=None):
        sorted_unique = sorted(set(nums if nums is not None else []))
        self._size = len(sorted_unique)
        self._build(sorted_unique)

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
        if isinstance(other, SortedSet):
            return list(self) == list(other)
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

    def add(self, x) -> bool:
        if self._size == 0:
            self._buckets = [[x]]
            self._size = 1
            return True
        bucket, bi, i = self._find(x)
        if i < len(bucket) and bucket[i] == x:
            return False
        bucket.insert(i, x)
        self._size += 1
        if len(bucket) > len(self._buckets) * self.SPLIT_RATIO:
            mid = len(bucket) >> 1
            self._buckets[bi: bi + 1] = [bucket[:mid], bucket[mid:]]
        return True

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
