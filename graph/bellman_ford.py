def bellman_ford(n, edges, start):
    dist = [INF for _ in range(n)]
    dist[start] = 0
    while True:
        change = False
        for (u, v, w) in edges:
            if dist[u] != INF and dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                change = True
        if not change:
            break
    return dist
