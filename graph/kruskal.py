def kruskal(n, edges):
    # O(ElogE)
    edges.sort(key=lambda e: e[2])
    dsu = DSU(n)
    res = 0
    for (u, v, c) in edges:
        if dsu.union(u, v):
            res += c
        if dsu.sz == 1:
            break
    return res if dsu.sz == 1 else -1
