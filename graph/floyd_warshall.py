INF = 1 << 60

def floyd(n, G):
    dist = [[INF for _ in range(n)] for _ in range(n)]
    prev = [[-1 for _ in range(n)] for _ in range(n)]
    for (u, v, w) in G:
        dist[u][v] = w
        prev[u][v] = u
    for v in range(n):
        dist[v][v] = 0
        prev[v][v] = v
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF and \
                        dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]
    return dist, prev
