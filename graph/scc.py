def tarjan(n, G):
    SCC, S, P = list(), list(), list()
    stk, state = [i for i in range(n)], [0 for _ in range(n)]
    while stk:
        node = stk.pop()
        if node < 0:
            d = state[~node] - 1
            if P[-1] > d:
                SCC.append(S[d:])
                del S[d:]; P.pop()
                for v in SCC[-1]:
                    state[v] = -1
        elif state[node] > 0:
            while P[-1] > state[node]:
                P.pop()
        elif state[node] == 0:
            S.append(node)
            P.append(len(S))
            state[node] = len(S)
            stk.append(~node)
            stk.extend(G[node])
    return SCC[::-1]

def kosaraju(n, G, revG):
    def dfs1(node):
        seen[node] = True
        for neigh in G[node]:
            if not seen[neigh]:
                dfs1(neigh)
        order.append(node)

    def dfs2(node):
        S.append(node)
        seen[node] = True
        for neigh in revG[node]:
            if not seen[neigh]:
                dfs2(neigh)

    SCC, S, order = list(), list(), list()
    seen = [False for _ in range(n)]
    for i in range(n):
        if not seen[i]:
            dfs1(i)

    seen = [False for _ in range(n)]
    for node in reversed(order):
        if not seen[node]:
            dfs2(node)
            SCC.append(S)
            S = list()
    return SCC
