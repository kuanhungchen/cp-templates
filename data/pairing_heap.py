from functools import reduce


class Node:
    def __init__(self, key, val=None):
        self.key = key
        self.val = val if val is not None else key
        self.par = self.chd = self.bro = None

    def __repr__(self):
        return f"Node(key={self.key!r}, val={self.val!r})"


class PairingHeap:
    def __init__(self, min_key=float("-inf")):
        self.rt = None
        self.sz = 0
        self.min_key = min_key

    def __bool__(self) -> bool:
        return self.sz != 0

    def __len__(self) -> int:
        return self.sz

    @property
    def top(self) -> Node:
        if self.rt is None:
            raise ValueError("top from empty heap")
        return self.rt

    def pop(self) -> Node:
        if not self or self.rt is None:
            raise ValueError("pop from empty heap")
        rt = self.rt
        self.rt = self._pair(self.rt.chd)
        self.sz -= 1
        rt.par = rt.chd = rt.bro = None
        return rt

    def push(self, node: Node):
        self.rt = node if self.rt is None else self._merge(self.rt, node)
        self.sz += 1

    def merge(self, other: "PairingHeap"):
        """merge with another pairing heap"""
        self.rt = self._merge(self.rt, other.rt)
        self.sz += other.sz
        other.rt = None
        other.sz = 0

    def decrease(self, node: Node, key):
        """decrease key of given node"""
        if node != self.rt and node.par is None:
            raise ValueError(f"given node {node} have already been removed from heap")
        if not key <= node.key:
            raise ValueError(f"new key {key} should be <= original key {node.key}")

        node.key = key
        if node != self.rt:
            if node.par and node.par.chd and node.par.chd == node:
                node.par.chd = node.bro
            elif node.par:
                node.par.bro = node.bro
            if node.bro:
                node.bro.par = node.par
            node.par = node.bro = None
            self.rt = self._merge(self.rt, node)

    def remove(self, node: Node):
        """remove the given node from heap"""
        if node != self.rt and node.par is None:
            raise ValueError(f"given node {node} have already been removed from heap")
        self.decrease(node, self.min_key)
        self.pop()

    def _pair(self, node):
        arr = []
        while node and node.bro:
            cur, nxt = node.bro, node.bro.bro
            node.par = node.bro = cur.par = cur.bro = None
            arr.append(self._merge(node, cur))
            node = nxt
        if node:
            node.bro = node.par = None
        arr.reverse()
        return reduce(self._merge, arr, node)

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
        return a if a is not None else b
