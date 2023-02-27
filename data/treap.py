import random

"""
Elements are key-value pairs? use TreapHashMap.
Elements' actual occurences don't matter? use TreapHashSet.
Elements can be duplicate and occurences matter? use TreapMultiSet.
"""


class TreapMultiSet:
    rt = 0
    sz = 0
    lchd = [0]
    rchd = [0]
    keys = [0]
    pris = [0.0]

    def __init__(self, nums=None):
        if nums:
            self.rt = self._build(nums)
            self.sz = len(nums)

    def add(self, key):
        self.rt = self._insert(key)
        self.sz += 1

    def remove(self, key):
        self.rt = self._erase(key)
        self.sz -= 1

    def discard(self, key):
        try:
            self.remove(key)
        except KeyError:
            pass

    def ceiling(self, key):
        # return the first value x >= key, or None if not exists
        x = self._ceiling(key)
        return self.keys[x] if x else None

    def higher(self, key):
        # return the first value x > key, or None if not exists
        x = self._higher(key)
        return self.keys[x] if x else None

    def floor(self, key):
        # return the first value x <= key, or None if not exists
        x = self._floor(key)
        return self.keys[x] if x else None

    def lower(self, key):
        # return the first value x < key, or None if not exists
        x = self._lower(key)
        return self.keys[x] if x else None

    def max(self):
        return self.keys[self._max()]

    def min(self):
        return self.keys[self._min()]

    def __len__(self):
        return self.sz

    def __nonzero__(self):
        return bool(self.rt)

    __bool__ = __nonzero__

    def __contains__(self, key):
        return self.floor(key) == key

    def __repr__(self):
        return "TreapMultiSet({})".format(list(self))

    def __iter__(self):
        if not self.rt:
            return iter([])
        out = []
        stk = [self.rt]
        lchd = self.lchd
        rchd = self.rchd
        keys = self.keys
        while stk:
            node = stk.pop()
            if node > 0:
                if rchd[node]:
                    stk.append(rchd[node])
                stk.append(~node)
                if lchd[node]:
                    stk.append(lchd[node])
            else:
                out.append(keys[~node])
        return iter(out)

    def _build(self, nums):
        def helper(beg, end):
            if beg == end:
                return 0
            mid = (beg + end) >> 1
            rt = self._create_node(nums[mid])
            lchd[rt] = helper(beg, mid)
            rchd[rt] = helper(mid + 1, end)

            idx = rt
            while True:
                l = lchd[idx]
                r = rchd[idx]
                if l and pris[l] > pris[idx]:
                    if r and pris[r] > pris[idx]:
                        pris[idx], pris[r] = pris[r], pris[idx]
                        idx = r
                    else:
                        pris[idx], pris[l] = pris[l], pris[idx]
                        idx = l
                elif r and pris[r] > pris[idx]:
                    pris[idx], pris[r] = pris[r], pris[idx]
                    idx = r
                else:
                    break
            return rt

        nums.sort()
        lchd = self.lchd
        rchd = self.rchd
        pris = self.pris
        return helper(0, len(nums))

    def _create_node(self, key):
        self.keys.append(key)
        self.pris.append(random.random())
        self.lchd.append(0)
        self.rchd.append(0)
        return len(self.keys) - 1

    def _insert(self, key):
        if not self.rt:
            return self._create_node(key)
        l, r = self._split(key)
        return self._merge(self._merge(l, self._create_node(key)), r)

    def _erase(self, key):
        if not self.rt:
            raise KeyError(key)
        if self.keys[self.rt] == key:
            return self._merge(self.lchd[self.rt], self.rchd[self.rt])
        node = rt = self.rt
        while rt and self.keys[rt] != key:
            parent = rt
            rt = self.lchd[rt] if key < self.keys[rt] else self.rchd[rt]
        if not rt:
            raise KeyError(key)
        if rt == self.lchd[parent]:
            self.lchd[parent] = self._merge(self.lchd[rt], self.rchd[rt])
        else:
            self.rchd[parent] = self._merge(self.lchd[rt], self.rchd[rt])
        return node

    def _split(self, key):
        lp = rp = 0
        rt = self.rt
        lchd = self.lchd
        rchd = self.rchd
        keys = self.keys
        while rt:
            if key < keys[rt]:
                lchd[rp] = rp = rt
                rt = lchd[rt]
            else:
                rchd[lp] = lp = rt
                rt = rchd[rt]
        l, r = rchd[0], lchd[0]
        rchd[lp] = lchd[rp] = rchd[0] = lchd[0] = 0
        return l, r

    def _merge(self, l, r):
        lchd = self.lchd
        rchd = self.rchd
        pris = self.pris
        where = self.lchd
        pos = 0
        while l and r:
            if pris[l] > pris[r]:
                where[pos] = pos = l
                where = rchd
                l = rchd[l]
            else:
                where[pos] = pos = r
                where = lchd
                r = lchd[r]
        where[pos] = l or r
        node = lchd[0]
        lchd[0] = 0
        return node

    def _ceiling(self, key):
        rt = self.rt
        lchd = self.lchd
        rchd = self.rchd
        keys = self.keys
        while rt and keys[rt] < key:
            rt = rchd[rt]
        if not rt:
            return 0
        min_node = rt
        min_key = keys[rt]
        while rt:
            if keys[rt] < key:
                rt = rchd[rt]
            else:
                if keys[rt] < min_key:
                    min_key = keys[rt]
                    min_node = rt
                rt = lchd[rt]
        return min_node

    def _higher(self, key):
        rt = self.rt
        lchd = self.lchd
        rchd = self.rchd
        keys = self.keys
        while rt and keys[rt] <= key:
            rt = rchd[rt]
        if not rt:
            return 0
        min_node = rt
        min_key = keys[rt]
        while rt:
            if keys[rt] <= key:
                rt = rchd[rt]
            else:
                if keys[rt] < min_key:
                    min_key = keys[rt]
                    min_node = rt
                rt = lchd[rt]
        return min_node

    def _floor(self, key):
        rt = self.rt
        lchd = self.lchd
        rchd = self.rchd
        keys = self.keys
        while rt and keys[rt] > key:
            rt = lchd[rt]
        if not rt:
            return 0
        max_node = rt
        max_key = keys[rt]
        while rt:
            if keys[rt] > key:
                rt = lchd[rt]
            else:
                if keys[rt] > max_key:
                    max_key = keys[rt]
                    max_node = rt
                rt = rchd[rt]
        return max_node

    def _lower(self, key):
        rt = self.rt
        lchd = self.lchd
        rchd = self.rchd
        keys = self.keys
        while rt and keys[rt] >= key:
            rt = lchd[rt]
        if not rt:
            return 0
        max_node = rt
        max_key = keys[rt]
        while rt:
            if keys[rt] >= key:
                rt = lchd[rt]
            else:
                if keys[rt] > max_key:
                    max_key = keys[rt]
                    max_node = rt
                rt = rchd[rt]
        return max_node

    def _max(self):
        if not self.rt:
            raise ValueError("max on empty treap")
        rt = self.rt
        rchd = self.rchd
        while rchd[rt]:
            rt = rchd[rt]
        return rt

    def _min(self):
        if not self.rt:
            raise ValueError("min on empty treap")
        rt = self.rt
        lchd = self.lchd
        while lchd[rt]:
            rt = lchd[rt]
        return rt


class TreapHashSet(TreapMultiSet):
    def __init__(self, nums=None):
        if nums:
            self._keys = set(nums)
            super(TreapHashSet, self).__init__(list(self._keys))
        else:
            self._keys = set()

    def add(self, key):
        if key not in self._keys:
            self._keys.add(key)
            super(TreapHashSet, self).add(key)

    def remove(self, key):
        self._keys.remove(key)
        super(TreapHashSet, self).remove(key)

    def discard(self, key):
        if key in self._keys:
            self.remove(key)

    def __contains__(self, key):
        return key in self._keys

    def __repr__(self):
        return "TreapHashSet({})".format(list(self))


class TreapHashMap(TreapMultiSet):
    def __init__(self, nums=None):
        if nums:
            self._map = dict(nums)
            super(TreapHashMap, self).__init__(list(self._map.keys()))
        else:
            self._map = dict()

    def __setitem__(self, key, value):
        if key not in self._map:
            super(TreapHashMap, self).add(key)
        self._map[key] = value

    def __getitem__(self, key):
        return self._map[key]

    def add(self, key):
        raise TypeError("add on TreapHashMap")

    def get(self, key, dflt=None):
        return self._map.get(key, dflt)

    def remove(self, key):
        self._map.pop(key)
        super(TreapHashMap, self).remove(key)

    def discard(self, key):
        if key in self._map:
            self.remove(key)

    def __contains__(self, key):
        return key in self._map

    def __repr__(self):
        return "TreapHashMap({})".format(list(self))

