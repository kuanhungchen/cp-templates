from heapq import heappop, heappush

INF = 1 << 60


def prim_dense(n, mat):
    # O(V^2)
    used = [False for _ in range(n)]
    dist = [INF for _ in range(n)]
    dist[0] = 0
    total_w = cnt = 0
    for _ in range(n):
        min_i = -1
        for i in range(n):
            if not used[i] and (min_i == -1 or dist[i] < dist[min_i]):
                min_i = i

        if dist[min_i] == INF: return -1

        used[min_i] = True
        total_w += dist[min_i]; cnt += 1
        for i in range(n):
            if not used[i]:
                dist[i] = min(dist[i], mat[min_i][i])
    return total_w if cnt == n else -1

def prim_dense_with_mst(n, mat, edge_ids):
    # O(V^2)
    used = [False for _ in range(n)]
    dist = [INF for _ in range(n)]
    par_edges = [-1 for _ in range(n)]
    dist[0] = 0
    total_w = cnt = 0
    mst = []
    for _ in range(n):
        min_i = -1
        for i in range(n):
            if not used[i] and (min_i == -1 or dist[i] < dist[min_i]):
                min_i = i

        if dist[min_i] == INF: return -1, []

        used[min_i] = True
        total_w += dist[min_i]; cnt += 1
        if par_edges[min_i] != -1: mst.append(par_edges[min_i])
        for i in range(n):
            if not used[i] and mat[min_i][i] < dist[i]:
                dist[i] = mat[min_i][i]
                par_edges[i] = edge_ids[min_i][i]
    return (total_w, mst) if cnt == n else (-1, [])


def prim(n, G):
    # O(ElogV)
    used = [False for _ in range(n)]
    pq = [(0, 0)]  # (weight, node)
    ans = cnt = 0
    while pq:
        w, node = heappop(pq)
        if used[node]:
            continue
        used[node] = True
        ans += w; cnt += 1
        for (neigh, neigh_w) in G[node]:
            if not used[neigh]:
                heappush(pq, (neigh_w, neigh))
    return ans if cnt == n else -1

def prim_with_mst(n, G):
    # O(ElogV)
    used = [False for _ in range(n)]
    pq = [(0, 0, -1)]  # (weight, node, edge_i)
    total_w = cnt = 0
    mst = []
    while pq:
        w, node, ei = heappop(pq)
        if used[node]:
            continue
        used[node] = True
        total_w += w; cnt += 1
        if ei != -1:
            mst.append(ei)
        for (neigh, neigh_w, edge_i) in G[node]:
            if not used[neigh]:
                heappush(pq, (neigh_w, neigh, edge_i))
    return (total_w, mst) if cnt == n else (-1, [])
