def convexhull(pts):
    if len(pts) <= 2:
        return pts

    # positive means counterclockwise
    ccw = lambda p, q, r: (p[0] - r[0]) * (q[1] - r[1]) - (p[1] - r[1]) * (q[0] - r[0])

    pts.sort()
    lower = [pts[0], pts[1]]
    upper = [pts[0], pts[1]]
    for pt in pts[2:]:
        while len(lower) >= 2 and ccw(lower[-2], lower[-1], pt) < 0:
            lower.pop()
        lower.append(pt)
        while len(upper) >= 2 and ccw(upper[-2], upper[-1], pt) > 0:
            upper.pop()
        upper.append(pt)

    return list(set(map(tuple, lower + upper[1:-1])))
