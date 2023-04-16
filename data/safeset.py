from functools import reduce
from random import randint

class SafeSet(set):
    def __init__(self, st=None, *ks):
        super().__init__()
        self._hash2key = {}
        self._xor1 = randint(1 << 30, 1 << 60)
        self._xor2 = randint(1 << 30, 1 << 60)
        self._mod = 1011001110001111

        assert st is None or isinstance(st, set) or isinstance(st, list)
        if st is not None:
            for k in st:
                self.add(k)
        for k in ks:
            self.add(k)

    def _hash(self, *x):
        return reduce(
            lambda hashv, elem:
            (hashv + hash(elem) ^ self._xor1 ^ self._xor2) % self._mod, x, 0)

    def __missing__(self, key):
        raise KeyError(key)

    def __delitem__(self, key):
        _ = self.__contains__(key) or self.__missing__(key)
        hashv = self._hash(key)
        super().remove(hashv)
        del self._hash2key[hashv]

    def __contains__(self, key):
        return self._hash(key) in self._hash2key

    def __str__(self):
        param = lambda v: "'" + v + "'" if isinstance(v, str) else str(v)
        return "{" + ", ".join("{}".format(param(key))
            for key in self._hash2key.values()) + "}"

    def add(self, key):
        hashv = self._hash(key)
        self._hash2key[hashv] = key
        super().add(hashv)

    def clear(self):
        self._hash2key.clear()
        super().clear()

    def copy(self):
        return SafeSet(list(self._hash2key.values()))

    def discard(self, key):
        if self.__contains__(key):
            self.remove(key)

    def pop(self):
        hashv = super().pop()
        return self._hash2key.pop(hashv)

    def remove(self, key):
        _ = self.__contains__(key) or self.__missing__(key)
        hashv = self._hash(key)
        super().remove(hashv)
        del self._hash2key[hashv]
