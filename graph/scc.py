def tarjan(n, G):
    SCC, S, P = [], [], []
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
