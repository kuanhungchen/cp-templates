class SparseTable2D:
    def __init__(self, mat):
        self.FUNC = FUNC = max

        R, C = len(mat), len(mat[0])
        lgR, lgC = R.bit_length(), C.bit_length()

        self.lgs = lgs = [0 for _ in range(max(R, C) + 1)]
        for i in range(2, len(lgs)):
            lgs[i] = lgs[i >> 1] + 1

        self.st = st = [[] for _ in range(lgR)]
        st[0].append(mat)

        for r in range(lgR - 1):
            r2 = 1 << r
            data = [[0 for _ in range(C)] for _ in range(R - r2 * 2 + 1)]
            p = st[r][0]
            for i in range(R - r2 * 2 + 1):
                for j in range(C):
                    data[i][j] = FUNC(p[i][j], p[i + r2][j])
            st[r + 1].append(data)

        for c in range(lgC - 1):
            c2 = 1 << c
            data = [[0 for _ in range(C - c2 * 2 + 1)] for _ in range(R)]
            p = st[0][c]
            for i in range(R):
                for j in range(C - c2 * 2 + 1):
                    data[i][j] = FUNC(p[i][j], p[i][j + c2])
            st[0].append(data)

        for r in range(lgR - 1):
            r2 = 1 << r
            for c in range(lgC - 1):
                c2 = 1 << c
                data = [[0 for _ in range(C - c2 * 2 + 1)] for _ in range(R - r2 * 2 + 1)]
                p = st[r][c]
                for i in range(R - r2 * 2 + 1):
                    for j in range(C - c2 * 2 + 1):
                        data[i][j] = FUNC(p[i][j], p[i][j + c2], p[i + r2][j],p[i + r2][j + c2])
                st[r + 1].append(data)

    def query(self, r1, r2, c1, c2):
        # [r1, r2) x [c1, c2)
        r = self.lgs[r2 - r1]
        c = self.lgs[c2 - c1]
        p = self.st[r][c]
        ul = p[r1][c1]
        ur = p[r1][c2 - (1 << c)]
        bl = p[r2 - (1 << r)][c1]
        br = p[r2 - (1 << r)][c2 - (1 << c)]
        return self.FUNC(ul, ur, bl, br)
