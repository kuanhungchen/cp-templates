class DSU:
    def __init__(self, n):
        self._n = n
        self._sz = n
        self._root = [-1 for _ in range(n)]

    @property
    def size(self):
        return self._sz

    @property
    def roots(self):
        return [i for i, x in enumerate(self._root) if x < 0]

    @property
    def groups(self):
        dic = {r: [] for r in self.roots}
        for i in range(self._n):
            dic[self.find(i)].append(i)
        return dic

    def group_size(self, x: int):
        return - self._root[self.find(x)]

    def find(self, x: int):
        if self._root[x] < 0:
            return x
        self._root[x] = self.find(self._root[x])
        return self._root[x]

    def same(self, x: int, y: int):
        return self.find(x) == self.find(y)

    def union(self, x: int, y: int):
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        if self._root[x] > self._root[y]:
            x, y = y, x
        self._root[x] += self._root[y]
        self._root[y] = x
        self._sz -= 1
        return True

    def members(self, x: int):
        root = self.find(x)
        return [i for i in range(self._n) if self.find(i) == root]


class DSUWithData(DSU):
    def __init__(self, n, nums):
        super(DSUWithData, self).__init__(n)
        self._data = nums.copy()

    @property
    def data(self):
        return self._data

    def group_data(self, x: int):
        return self._data[self.find(x)]

    def union(self, x: int, y: int):
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        if self._root[x] > self._root[y]:
            x, y = y, x
        self._root[x] += self._root[y]
        self._data[x] += self._data[y]
        self._data[y] = 0
        self._root[y] = x
        self._sz -= 1
        return True
