def is_cyclic(n, G):
    # Returns a cycle (edge IDs) if graph is cyclic.
    def dfs(node):
        nonlocal cycle_start
        state[node] = -1

        for (neigh, edge_i) in G[node]:
            if state[neigh] == -1:
                cycle_start = neigh
                cycle.append(edge_i)
                return True

            if state[neigh] == 0:
                if dfs(neigh):
                    if cycle_start is not None:
                        cycle.append(edge_i)
                        if node == cycle_start:
                            cycle_start = None
                    return True

        state[node] = 1
        return False

    cycle = []
    cycle_start = None
    state = [0 for _ in range(n)]
    for i in range(n):
        if state[i] == 0:
            if dfs(i):
                return cycle
    return []

adj = [[(1, 0)], [(2, 1)], [(1, 2)]]
print(is_cyclic(3, adj))
