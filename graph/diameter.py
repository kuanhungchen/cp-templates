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

def diameter2(n, G):
    def dfs(node, pre):
        nonlocal diam
        for (neigh, neigh_d) in G[node]:
            if neigh == pre: continue
            dfs(neigh, node)
            diam = max(diam, d[node] + d[neigh] + neigh_d)
            d[node] = max(d[node], d[neigh] + neigh_d)

    diam = 0
    d = [0 for _ in range(n)]
    dfs(0, -1)
    return diam
