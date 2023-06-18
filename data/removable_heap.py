from heapq import heapify, heappop, heappush
from heapq import _siftup_max, _siftdown_max, _heapify_max  # pyright: ignore [reportGeneralTypeIssues]

def heappop_max(pq):
    ans = pq.pop()
    if pq:
        ans, pq[0] = pq[0], ans
        _siftup_max(pq, 0)
    return ans

def heapreplace_max(pq, x):
    ans, pq[0] = pq[0], x
    _siftup_max(pq, 0)
    return ans

def heappush_max(pq, x):
    pq.append(x)
    _siftdown_max(pq, 0, len(pq) - 1)

def heappushpop_max(pq, x):
    if pq and pq[0] > x:
        x, pq[0] = pq[0], x
        _siftup_max(pq, 0)
    return x

heapify_max = _heapify_max


class RemovableHeap:
    def __init__(self, nums=[], is_max=False):
        self._pq = nums[:]
        if is_max: heapify_max(self._pq)
        else: heapify(self._pq)

        self._pq_del = []

        self._pop = heappop_max if is_max else heappop
        self._push = heappush_max if is_max else heappush

    def __len__(self):
        return len(self._pq) - len(self._pq_del)

    def __bool__(self):
        return self.__len__() != 0

    def _prop(self):
        while self._pq_del and self._pq[0] == self._pq_del[0]:
            self._pop(self._pq)
            self._pop(self._pq_del)

    def top(self):
        self._prop()
        return self._pq[0]

    def remove(self, val):
        self._push(self._pq_del, val)

    def push(self, val):
        self._push(self._pq, val)

    def pop(self):
        self._prop()
        return self._pop(self._pq)
