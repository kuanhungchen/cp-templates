def prim_dense(n, mat):
    # O(V^2)
    used = [False for _ in range(n)]
    dist = [INF for _ in range(n)]
    dist[0] = 0
    ans = cnt = 0
    for _ in range(n):
        min_i = -1
        for i in range(n):
            if not used[i] and (min_i == -1 or dist[i] < dist[min_i]):
                min_i = i
        used[min_i] = True
        ans += dist[min_i]; cnt += 1
        for i in range(n):
            if not used[i]:
                dist[i] = min(dist[i], mat[min_i][i])
    return ans if cnt == n else -1

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
