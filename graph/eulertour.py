def eulertour(n, G, rts=None):
    """Get an Euler tour of a graph or a tree.

    Return:
        first: First timestamp of each node during the Euler tour. Length of n.
        last:  Last timestamp of each node during the Euler tour. Length of n.
        parent: Parent of each node during the Euler tour. Length of n.
        euler: The actual Euler tour starting from given root(s). Length of 2n.
        depth: Depth of each node during the Euler tour. Length of 2n.

    Remarks:
        1. To get real depth of each node, use (depth[v] >> 32).
        2. Assume ST is a sparse table built on depth array, LCA(u, v) would
           be ST.query(left, right + 1) & ((1 << 32) - 1), where
           left = min(first[u], first[v]) and right = max(first[u], first[v]).
        3. G can be either adj lists or edges.
    """
    def bfs(node):
        dep = 0
        stk = [[node, 0]]
        first[node] = len(euler)
        euler.append(node)
        depth.append((dep << 32) + node)

        while stk:
            node, idx = stk[-1]
            if idx < len(G[node]):
                child = G[node][idx]
                stk[-1][1] += 1
                if child == parent[node]:
                    continue
                dep += 1
                first[child] = len(euler)
                euler.append(child)
                depth.append((dep << 32) + child)
                parent[child] = node
                stk.append([child, 0])
            else:
                last[node] = len(euler)
                if parent[node] != -1:
                    dep -= 1
                    euler.append(parent[node])
                    depth.append((dep << 32) + parent[node])
                stk.pop()

    first = [-1 for _ in range(n)]
    last = [-1 for _ in range(n)]
    parent = [-1 for _ in range(n)]
    euler = []
    depth = []

    if rts is None:
        rts = range(n)
    elif isinstance(rts, int):
        rts = [rts]

    for rt in rts:
        if parent[rt] == -1:
            bfs(rt)
    return first, last, parent, euler, depth
