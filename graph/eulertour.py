class EulerTour:
    def __init__(self, n, G, root=None):
        self.G = G
        self.parent = [-1 for _ in range(n)]
        self.first = [-1 for _ in range(n)]
        self.last = [-1 for _ in range(n)]
        self.depth = []
        self.euler = []

        if root is None: all(self.dfs(u) for u in range(n) if self.parent[u] == -1)
        else: self.dfs(root)

        self.st = SparseTable(self.depth)

    def dfs(self, rt):
        dep = 0
        stk = [rt, 0]
        self.first[rt] = len(self.euler)
        self.euler.append(rt)
        self.depth.append((dep << 32) + rt)
        while stk:
            v, idx = stk[-2:]
            if idx < len(self.G[v]):
                nxtv = self.G[v][idx]
                stk[-1] += 1
                if nxtv == self.parent[v]:
                    continue
                dep += 1
                self.first[nxtv] = len(self.euler)
                self.euler.append(nxtv)
                self.depth.append((dep << 32) + nxtv)
                self.parent[nxtv] = v
                stk.append(nxtv)
                stk.append(0)
            else:
                self.last[v] = len(self.euler)
                if self.parent[v] != -1:
                    dep -= 1
                    self.euler.append(self.parent[v])
                    self.depth.append((dep << 32) + self.parent[v])
                stk.pop()
                stk.pop()

    def lca(self, u, v):
        left = min(self.first[u], self.first[v])
        right = max(self.first[u], self.first[v])
        return self.st.query(left, right + 1) & ((1 << 32) - 1)