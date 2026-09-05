def build_sa_slow(s):
    # O(n*(logn)^2)
    n = len(s)
    if n <= 1: return list(range(n)), [0] * n, [0] * n

    sa = list(range(n))
    rk = [ord(c) for c in s]
    tmp = [0] * n

    k = 1
    while k < n:
        sa.sort(key=lambda x: (rk[x], rk[x + k] if x + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, curr = sa[i - 1], sa[i]
            prev_key = (rk[prev], rk[prev + k] if prev + k < n else -1)
            curr_key = (rk[curr], rk[curr + k] if curr + k < n else -1)
            tmp[curr] = tmp[prev] + (1 if prev_key != curr_key else 0)
        rk, tmp = tmp, rk
        if rk[sa[n - 1]] == n - 1: break
        k <<= 1

    lcp = [0] * n
    h = 0
    for i in range(n):
        if rk[i] > 0:
            j = sa[rk[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rk[i]] = h
            if h > 0:
                h -= 1
        else:
            h = 0

    return sa, rk, lcp


def sa_is(s):
    # O(n)
    n = len(s)
    if n == 1: return [0]

    is_s = [False] * n
    is_s[-1] = True
    for i in range(n - 2, -1, -1):
        if s[i] < s[i + 1]:
            is_s[i] = True
        elif s[i] == s[i + 1]:
            is_s[i] = is_s[i + 1]

    is_lms = [False] * n
    lms = []
    for i in range(1, n):
        if is_s[i] and not is_s[i - 1]:
            is_lms[i] = True
            lms.append(i)

    mx = max(s)
    counts = [0] * (mx + 1)
    for c in s:
        counts[c] += 1

    def induce(lms_sub):
        sa = [-1] * n

        ends = []
        acc = 0
        for c in counts:
            acc += c
            ends.append(acc)
        for p in reversed(lms_sub):
            c = s[p]
            ends[c] -= 1
            sa[ends[c]] = p

        starts = [0]
        acc = 0
        for c in counts[:-1]:
            acc += c
            starts.append(acc)
        for i in range(n):
            p = sa[i] - 1
            if p >= 0 and not is_s[p]:
                c = s[p]
                sa[starts[c]] = p
                starts[c] += 1

        ends = []
        acc = 0
        for c in counts:
            acc += c
            ends.append(acc)
        for i in range(n - 1, -1, -1):
            p = sa[i] - 1
            if p >= 0 and is_s[p]:
                c = s[p]
                ends[c] -= 1
                sa[ends[c]] = p

        return sa

    sa = induce(lms)

    lms_in_sa = [p for p in sa if is_lms[p]]
    name = 0
    names = [-1] * n
    if lms_in_sa:
        names[lms_in_sa[0]] = name
        for i in range(1, len(lms_in_sa)):
            p1, p2 = lms_in_sa[i - 1], lms_in_sa[i]
            diff = False
            d = 0
            while True:
                if s[p1 + d] != s[p2 + d] or is_s[p1 + d] != is_s[p2 + d]:
                    diff = True
                    break
                if d > 0 and (is_lms[p1 + d] or is_lms[p2 + d]):
                    break
                d += 1
            if diff:
                name += 1
            names[p2] = name

    reduced_s = [names[p] for p in lms]

    if name < len(lms) - 1:
        sa_lms_names = sa_is(reduced_s)
        ordered_lms = [lms[i] for i in sa_lms_names]
    else:
        ordered_lms = [0] * len(lms)
        for i, p in enumerate(reduced_s):
            ordered_lms[p] = lms[i]

    return induce(ordered_lms)


def build_sa(s):
    # O(n)
    n = len(s)
    if n == 0:
        return [], [], []
    if n == 1:
        return [0], [0], [0]

    if isinstance(s, str):
        chars = sorted(set(s))
        char_map = {c: i + 1 for i, c in enumerate(chars)}
        num_s = [char_map[c] for c in s] + [0]
    else:
        mins = min(s)
        num_s = [x - mins + 1 for x in s] + [0]

    sa_raw = sa_is(num_s)
    sa = sa_raw[1:]

    rk = [0] * n
    for idx, pos in enumerate(sa):
        rk[pos] = idx

    lcp = [0] * n
    h = 0
    for i in range(n):
        if rk[i] > 0:
            j = sa[rk[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rk[i]] = h
            if h > 0:
                h -= 1
        else:
            h = 0

    return sa, rk, lcp
