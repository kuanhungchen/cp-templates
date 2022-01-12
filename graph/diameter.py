def diameter(n, G):
    def bfs(start):
        dist = [-1 for _ in range(n)]
        dist[start] = 0
        stk = [start]
        while stk:
            node = stk.pop()
            for (neigh, neigh_d) in G[node]:
                if dist[neigh] != -1:
                    continue
                dist[neigh] = dist[node] + neigh_d
                stk.append(neigh)
        max_i = dist.index(max(dist))
        return max_i, dist

    u, _ = bfs(0)
    v, dist = bfs(u)
    diam = dist[v]
    path = [v]
    while u != v:
        for (neigh, neigh_d) in G[v]:
            if dist[neigh] + neigh_d == dist[v]:
                path.append(neigh)
                v = neigh
                break
    return diam, path
