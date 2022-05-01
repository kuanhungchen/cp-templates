def eulertour(n, G, rt=None):
    # build sparse table on euler, then LCA(u, v) = st.query(left, right + 1)
    # where left = min(first[u], first[v]), right = max(first[u], first[v])
    def bfs(node):
        stk = [[node, 0]]
        first[node] = len(euler)
        euler.append(node)

        while stk:
            node, idx = stk[-1]
            if idx < len(G[node]):
                child = G[node][idx]
                stk[-1][1] += 1
                if child == parent[node]:
                    continue
                first[child] = len(euler)
                euler.append(child)
                parent[child] = node
                stk.append([child, 0])
            else:
                last[node] = len(euler)
                if parent[node] != -1:
                    euler.append(parent[node])
                stk.pop()

    first = [-1 for _ in range(n)]
    last = [-1 for _ in range(n)]
    parent = [-1 for _ in range(n)]
    euler = []

    if rt is None:
        all(bfs(node) for node in range(n) if parent[node] == -1)
    else:
        bfs(rt)

    return first, last, euler
