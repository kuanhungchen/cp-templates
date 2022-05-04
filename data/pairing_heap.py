from functools import reduce


class Node:
    def __init__(self, val, key=None):
        self.val = val
        self.key = key if key is not None else val
        self.par = self.chd = self.bro = None


class PairingHeap:
    def __init__(self, nums=None):
        self.rt = None

        if nums is not None:
            self.sz = len(nums)
            for num in nums:
                self.push(num)
        else:
            self.sz = 0

    def __bool__(self):
        return bool(self.sz != 0)

    def __len__(self):
        return self.sz

    @property
    def top(self):
        # assert self.sz > 0
        return self.rt.val

    def pop(self):
        # assert self.sz > 0
        return self._pop().val

    def push(self, val, *, key=None):
        """return a pointer to the node containing the new value"""
        node = Node(val, key)
        self.rt = node if not self.rt else self._merge(self.rt, node)
        self.sz += 1
        return node

    def merge(self, other):
        """merge with another pairing heap"""
        self.rt = self._merge(self.rt, other.rt)
        self.sz += other.sz

    def decrease(self, node, key):
        """given pointer to a node, assign its key with a smaller one"""

        assert key <= node.key, "new key {} should be less than or equal " \
                                "to original key{}.".format(key, node.key)
        node.key = key
        if node != self.rt:
            par = node.par
            if par.chd == node:
                par.chd = node.bro
            else:
                par.bro = node.bro
            if node.bro:
                node.bro.par = par
            node.bro = node.par = None
            self.rt = self._merge(self.rt, node)

    def _pop(self):
        ret = self.rt
        self.rt = self._pair(self.rt.chd)
        self.sz -= 1
        ret.par = ret.chd = ret.bro = None
        return ret

    def _pair(self, node):
        arr = []
        while node and node.bro:
            cur, nxt = node.bro, node.bro.bro
            node.bro = node.par = cur.bro = cur.par = None
            arr.append(self._merge(node, cur))
            node = nxt
        if node:
            node.bro = node.par = None
            arr.append(node)
        return reduce(self._merge, arr, None)

    @staticmethod
    def _merge(a, b):
        if a and b:
            if a.key > b.key:
                a, b = b, a
            b.bro, a.chd = a.chd, b
            if b.bro:
                b.bro.par = b
            b.par = a
            return a
        return a if a else b
