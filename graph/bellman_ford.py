def bellman_ford(n, edges, start):
    dist = [INF for _ in range(n)]
    prev = [-1 for _ in range(n)]
    dist[start] = 0
    change = True
    while change:
        change = False
        for (u, v, w) in edges:
            if dist[u] != INF and dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                change = True

    return dist, prev
