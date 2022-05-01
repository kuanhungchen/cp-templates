def eulertour(n, G, rt=None):
    # Assume ST is sparse table built on depth array, then LCA(u, v) is
    # ST.query(left, right + 1) & ((1 << 32) - 1),
    # where left = min(first[u], first[v]), right = max(first[u], first[v]).
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

    rts = [rt] if rt is not None else range(n)
    all(bfs(rt) for rt in rts if parent[rt] == -1)
    return first, last, euler, depth
