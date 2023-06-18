from removable_heap import RemovableHeap


class TopK:
    def __init__(self, k, nums=[], is_max=False):
        self._k = k
        self._is_max = is_max

        _nums = nums[:]
        _nums.sort(reverse=is_max)
        self._sumv = sum(_nums[:k])
        self._pq_topk = RemovableHeap(_nums[:k], not is_max)
        self._pq_misc = RemovableHeap(_nums[k:], is_max)

    @property
    def sumv(self):
        return self._sumv

    def add(self, val):
        self._pq_topk.push(val)
        self._sumv += val
        if len(self._pq_topk) == self._k + 1:
            _val = self._pq_topk.pop()
            self._sumv -= _val
            self._pq_misc.push(_val)

    def remove(self, val):
        _top = self._pq_topk.top()
        remove_from_top_k = val <= _top if not self._is_max else _top <= val
        if remove_from_top_k:
            self._pq_topk.remove(val)
            self._sumv -= val
            if self._pq_misc:
                _val = self._pq_misc.pop()
                self._sumv += _val
                self._pq_topk.push(_val)
        else:
            self._pq_misc.remove(val)
