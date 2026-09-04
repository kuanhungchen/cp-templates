from data.dsu import DSU


def kruskal(n, edges):
    # O(ElogE)
    edges.sort(key=lambda e: e[2])
    dsu = DSU(n)
    total_w = 0
    for (u, v, w) in edges:
        if dsu.union(u, v):
            total_w += w
        if dsu.size == 1:
            break
    return total_w if dsu.size == 1 else -1


def kruskal_with_mst(n, edges):
    # O(ElogE)
    indexed_edges = [(u, v, w, idx) for idx, (u, v, w) in enumerate(edges)]
    indexed_edges.sort(key=lambda e: e[2])  # sort by weight

    dsu = DSU(n)
    total_w = 0
    mst = []
    for (u, v, w, idx) in indexed_edges:
        if dsu.union(u, v):
            total_w += w
            mst.append(idx)
        if dsu.size == 1:
            break
    return (total_w, mst) if dsu.size == 1 else (-1, [])
