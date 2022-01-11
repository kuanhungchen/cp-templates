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

def bellman_ford_negative_cycle(n, edges, start):
    dist = [INF for _ in range(n)]
    prev = [-1 for _ in range(n)]
    dist[start] = 0
    node = 0
    for _ in range(n):
        node = -1
        for (u, v, w) in edges:
            if dist[u] != INF and dist[v] > dist[u] + w:
                dist[v] = max(- INF, dist[u] + w)
                prev[v] = u
                node = v

    if node == -1:
        return []  # no reachable negative cycle from start

    for _ in range(n):
        node = prev[node]
    path = []
    cur = node
    while True:
        path.append(cur)
        if cur == node and len(path) > 1:
            break
        cur = prev[cur]
    path.reverse()
    return path
