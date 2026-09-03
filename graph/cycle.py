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
                return cycle[::-1]
    return []


def is_cyclic_undirected(n, G):
    # Returns a cycle (edge IDs) if undirected graph is cyclic.
    def dfs(node, prev_e):
        nonlocal cycle_start
        state[node] = -1

        for (neigh, edge_i) in G[node]:
            if edge_i == prev_e:
                continue
            if state[neigh] == -1:
                cycle_start = neigh
                cycle.append(edge_i)
                return True

            if state[neigh] == 0:
                if dfs(neigh, edge_i):
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
            if dfs(i, -1):
                return cycle[::-1]
    return []
