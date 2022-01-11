def is_cyclic(n, G):
    # return a cycle (edge ids) if graph is cyclic
    def dfs(node):
        if state[node] == 0:
            state[node] = -1
            for (neigh, edge_i) in G[node]:
                if dfs(neigh) == -1:
                    cycle.append(edge_i)
                    return -1
            state[node] = 1
        return state[node]

    cycle = []
    state = [0 for _ in range(n)]
    for i in range(n):
        dfs(i)

    return cycle
