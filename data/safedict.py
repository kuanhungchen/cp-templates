from random import randint


class SafeDict(dict):
    def __init__(self):
        super().__init__()

        self._keys = set()
        self._xor1 = randint(1 << 30, 1 << 60)
        self._xor2 = randint(1 << 30, 1 << 60)
        self._hash = lambda x: x ^ self._xor1 ^ self._xor2
        self._ihash = self._hash

    def __missing__(self, key):
        raise KeyError(self._ihash(key))

    def __setitem__(self, key, value):
        super().__setitem__(self._hash(key), value)
        self._keys.add(self._hash(key))

    def __getitem__(self, item):
        return super().__getitem__(self._hash(item))

    def __delitem__(self, item):
        super().__delitem__(self._hash(item))
        self._keys.discard(self._hash(item))

    def __contains__(self, item):
        return self._hash(item) in self._keys

    def keys(self):
        for key in self._keys:
            yield self._ihash(key)

    def values(self):
        for value in super().values():
            yield value

    def items(self):
        for key, value in super().items():
            yield self._ihash(key), value

    def __str__(self):
        s = "{" + ",".join(["{}: {}".format(self._ihash(key), value)
            for key, value in super().items()]) + "}"
        return s


class SafeDefaultDict(SafeDict):
    def __init__(self, default):
        super().__init__()
        self._default = default

    def __missing__(self, key):
        return self._default
