def cartesian(n, WK):
    # WK = [(w0, k0), ...], sorted by k's
    par = [-1 for _ in range(n)]
    chain = []
    for i, (w, _) in enumerate(WK):
        prev_i = -1
        while chain and w < chain[-1][0]:
            prev_i = chain.pop()[1]
        if prev_i != -1:
            par[prev_i] = i
        if chain:
            par[i] = chain[-1][1]
        chain.append((w, i))
    return par
