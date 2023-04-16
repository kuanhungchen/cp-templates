from functools import reduce
from random import randint


class SafeDict(dict):
    def __init__(self, mp=None, **kvs):
        super().__init__()
        self._hash2key = {}
        self._xor1 = randint(1 << 30, 1 << 60)
        self._xor2 = randint(1 << 30, 1 << 60)
        self._mod = 1011001110001111

        assert mp is None or isinstance(mp, dict)
        if mp is not None:
            for (k, v) in mp.items():
                self.__setitem__(k, v)
        for (k, v) in kvs.items():
            self.__setitem__(k, v)

    def _hash(self, *x):
        return reduce(
            lambda hashv, elem:
            (hashv + hash(elem) ^ self._xor1 ^ self._xor2) % self._mod, x, 0)

    def __missing__(self, key):
        raise KeyError(key)

    def __setitem__(self, key, value):
        hashv = self._hash(key)
        super().__setitem__(hashv, value)
        self._hash2key[hashv] = key

    def __getitem__(self, key):
        _ = self.__contains__(key) or self.__missing__(key)
        return super().__getitem__(self._hash(key))

    def __delitem__(self, key):
        _ = self.__contains__(key) or self.__missing__(key)
        hashv = self._hash(key)
        super().__delitem__(hashv)
        del self._hash2key[hashv]

    def __contains__(self, key):
        return self._hash(key) in self._hash2key

    def __str__(self):
        param = lambda v: "'" + v + "'" if isinstance(v, str) else str(v)
        return "{" + ", ".join("{}: {}".format(
            param(self._hash2key[hashv]), param(value))
            for hashv, value in super().items()) + "}"

    def clear(self):
        self._hash2key.clear()
        super().clear()

    def copy(self):
        return SafeDict(self)

    def get(self, key):
        return self.__getitem__(key)

    def items(self):
        for hashv, value in super().items():
            yield self._hash2key[hashv], value

    def keys(self):
        for key in self._hash2key.values():
            yield key

    def pop(self, key):
        _ = self.__contains__(key) or self.__missing__(key)
        hashv = self._hash(key)
        del self._hash2key[hashv]
        return super().pop(hashv)

    def popitem(self):
        hashv, value = super().popitem()
        key = self._hash2key.pop(hashv)
        return (key, value)

    def setdefault(self, key, default):
        return self.__getitem__(key) \
                if self.__contains__(key) \
                else self.__setitem__(key, default) or default


class SafeDefaultDict(SafeDict):
    def __init__(self, default):
        super().__init__()
        self._default = default

    def __missing__(self, key):
        self.__setitem__(key, self._default)
