class DSU:
    def __init__(self, n):
        self.rt = [-1 for _ in range(n)]
        self.n = n
        self.sz = n  # number of sets

    def size(self, x): return - self.rt[self.find(x)]

    def same(self, x, y): return self.find(x) == self.find(y)

    def group_count(self): return self.sz

    def find(self, x):
        if self.rt[x] < 0:
            return x
        self.rt[x] = self.find(self.rt[x])
        return self.rt[x]

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        if self.rt[x] > self.rt[y]:
            x, y = y, x
        self.rt[x] += self.rt[y]
        self.rt[y] = x
        self.sz -= 1
        return True

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.rt) if x < 0]

    def all_groups(self):
        dic = {r: [] for r in self.roots()}
        for i in range(self.n):
            dic[self.find(i)].append(i)
        return dic
