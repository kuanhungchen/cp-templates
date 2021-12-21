import heapq

def dijkstra(G, start):
    n = len(G)
    dist = [-1 for _ in range(n)]
    prev = [-1 for _ in range(n)]
    dist[start] = 0
    pq = [(0, start)]  # (distance, node)
    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        d = dist[node]
        for (neigh, neigh_d) in G[node]:
            if dist[neigh] == -1 or d + neigh_d < dist[neigh]:
                dist[neigh] = d + neigh_d
                prev[neigh] = node
                heapq.heappush(pq, (dist[neigh], neigh))
    return dist, prev
