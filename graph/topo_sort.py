def topo_sort(n, G):
    order = []
    in_deg = [0 for _ in range(n)]
    for vs in G:
        for v in vs:
            in_deg[v] += 1

    cnt = 0
    q = deque([i for i in range(n) if in_deg[i] == 0])
    while q:
        u = q.popleft()
        order.append(u)
        for v in G[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                q.append(v)
        cnt += 1

    return order if cnt == n else list()
