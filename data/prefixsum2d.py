class PrefixSum2D:
    def __init__(self, mat):
        self.h = h = len(mat)
        self.w = w = len(mat[0])
        self.data = data = [[0 for _ in range(w + 1)] for _ in range(h + 1)]

        for i in range(h):
            for j in range(w):
                data[i + 1][j + 1] = data[i + 1][j] + mat[i][j]
        for i in range(h):
            for j in range(w):
                data[i + 1][j + 1] += data[i][j + 1]

    def query(self, r1, r2, c1, c2):
        # [r1, r2) x [c1, c2)
        return self.data[r2][c2] - self.data[r2][c1] \
               - self.data[r1][c2] + self.data[r1][c1]
