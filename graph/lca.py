class LCA:
    def __init__(self, G, root):
        n = len(G)
        self.G = G
        self.first = [-1 for _ in range(n)]
        self.depth = [-1 for _ in range(n)]
        self.euler = [-1 for _ in range(2 * n - 1)]

        self.__euler_tour(root)
        self.st = SparseTable(self.euler)

    def __euler_tour(self, node, prev=-1, d=0):
        self.depth[node] = d
        self.first[node] = len(self.euler)
        self.euler.append(node)
        for neigh in self.G[node]:
            if neigh != prev:
                self.__euler_tour(neigh, node, d + 1)
                self.euler.append(node)

    def lca(self, u, v):
        left = min(self.first[u], self.first[v])
        right = max(self.first[u], self.first[v])
        return self.st.query(left, right + 1)
