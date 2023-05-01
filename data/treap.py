import random


class TreapMultiSet:
    def __init__(self, nums=None):
        self._rt = 0
        self._sz = 0  # number of total elements
        self._lchd = [0]
        self._rchd = [0]
        self._keys = [0]
        self._pris = [0.0]

        if nums:
            self._rt = self._build(nums)
            self._sz = len(nums)

    def add(self, key):
        # add one occurence for key
        self._rt = self._insert(key)
        self._sz += 1

    def remove(self, key):
        # remove one element for key, raise KeyError if not exists
        self._rt = self._erase(key)
        self._sz -= 1

    def discard(self, key):
        # safe remove
        try:
            self.remove(key)
        except KeyError:
            pass

    def ceiling(self, key):
        # return the first element x >= key, or None if not exists
        x = self._ceiling(key)
        return self._keys[x] if x else None

    def higher(self, key):
        # return the first element x > key, or None if not exists
        x = self._higher(key)
        return self._keys[x] if x else None

    def floor(self, key):
        # return the first element x <= key, or None if not exists
        x = self._floor(key)
        return self._keys[x] if x else None

    def lower(self, key):
        # return the first element x < key, or None if not exists
        x = self._lower(key)
        return self._keys[x] if x else None

    @property
    def max(self):
        return self._keys[self._max()]

    @property
    def min(self):
        return self._keys[self._min()]

    def __len__(self):
        # return number of all elements
        return self._sz

    def __nonzero__(self):
        return bool(self._rt)

    __bool__ = __nonzero__

    def __contains__(self, key):
        return self.floor(key) == key

    def __repr__(self):
        return "TreapMultiSet({})".format(list(self))

    def __iter__(self):
        # iterate all elements in ascending order
        if not self._rt:
            return iter([])
        out = []
        stk = [self._rt]
        lchd = self._lchd
        rchd = self._rchd
        keys = self._keys
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
        lchd = self._lchd
        rchd = self._rchd
        pris = self._pris
        return helper(0, len(nums))

    def _create_node(self, key):
        self._keys.append(key)
        self._pris.append(random.random())
        self._lchd.append(0)
        self._rchd.append(0)
        return len(self._keys) - 1

    def _insert(self, key):
        if not self._rt:
            return self._create_node(key)
        l, r = self._split(key)
        return self._merge(self._merge(l, self._create_node(key)), r)

    def _erase(self, key):
        if not self._rt:
            raise KeyError(key)
        if self._keys[self._rt] == key:
            return self._merge(self._lchd[self._rt], self._rchd[self._rt])
        node = rt = self._rt
        parent = rt
        while rt and self._keys[rt] != key:
            parent = rt
            rt = self._lchd[rt] if key < self._keys[rt] else self._rchd[rt]
        if not rt:
            raise KeyError(key)
        if rt == self._lchd[parent]:
            self._lchd[parent] = self._merge(self._lchd[rt], self._rchd[rt])
        else:
            self._rchd[parent] = self._merge(self._lchd[rt], self._rchd[rt])
        return node

    def _split(self, key):
        lp = rp = 0
        rt = self._rt
        lchd = self._lchd
        rchd = self._rchd
        keys = self._keys
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
        lchd = self._lchd
        rchd = self._rchd
        pris = self._pris
        where = self._lchd
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
        rt = self._rt
        lchd = self._lchd
        rchd = self._rchd
        keys = self._keys
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
        rt = self._rt
        lchd = self._lchd
        rchd = self._rchd
        keys = self._keys
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
        rt = self._rt
        lchd = self._lchd
        rchd = self._rchd
        keys = self._keys
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
        rt = self._rt
        lchd = self._lchd
        rchd = self._rchd
        keys = self._keys
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
        if not self._rt:
            raise ValueError("max on empty treap")
        rt = self._rt
        rchd = self._rchd
        while rchd[rt]:
            rt = rchd[rt]
        return rt

    def _min(self):
        if not self._rt:
            raise ValueError("min on empty treap")
        rt = self._rt
        lchd = self._lchd
        while lchd[rt]:
            rt = lchd[rt]
        return rt


class TreapHashSet(TreapMultiSet):
    def __init__(self, nums=None):
        if nums:
            self._internal_keys = set(nums)
            super(TreapHashSet, self).__init__(list(self._internal_keys))
        else:
            self._internal_keys = set()

    def add(self, key):
        if key not in self._internal_keys:
            self._internal_keys.add(key)
            super(TreapHashSet, self).add(key)

    def remove(self, key):
        self._internal_keys.remove(key)
        super(TreapHashSet, self).remove(key)

    def discard(self, key):
        if key in self._internal_keys:
            self.remove(key)

    def __contains__(self, key):
        return key in self._internal_keys

    def __repr__(self):
        return "TreapHashSet({})".format(list(self))


class TreapHashMap(TreapMultiSet):
    def __init__(self, dict_=None):
        self._internal_dict = dict()
        if dict_:
            self._internal_dict = dict_
            super(TreapHashMap, self).__init__(list(dict_.keys()))

    def __setitem__(self, key, value):
        if key not in self._internal_dict:
            super(TreapHashMap, self).add(key)
        self._internal_dict[key] = value

    def __getitem__(self, key):
        return self._internal_dict[key]

    def add(self, key):
        raise TypeError("add on TreapHashMap")

    def get(self, key, default=None):
        return self._internal_dict.get(key, default)

    def remove(self, key):
        self._internal_dict.pop(key)
        super(TreapHashMap, self).remove(key)

    def discard(self, key):
        if key in self._internal_dict:
            self.remove(key)

    def __contains__(self, key):
        return key in self._internal_dict

    def __repr__(self):
        return "TreapHashMap({{{}}})".format(
                ", ".join("{}: {}".format(key, self.get(key)) for key in self))
