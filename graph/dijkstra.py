from heapq import heappush, heappop

def dijkstra(n, G, start):
    # O(V + ElogV)
    dist = [-1 for _ in range(n)]
    prev = [-1 for _ in range(n)]
    dist[start] = 0
    pq = [(0, start)]  # (distance, node)
    while pq:
        d, node = heappop(pq)
        if d != dist[node]:
            continue
        for (neigh, neigh_d) in G[node]:
            if dist[neigh] == -1 or d + neigh_d < dist[neigh]:
                dist[neigh] = d + neigh_d
                prev[neigh] = node
                heappush(pq, (dist[neigh], neigh))
    return dist, prev
