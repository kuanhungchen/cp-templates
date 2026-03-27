def horizontal_flip(mat):
    for row in mat:
        row.reverse()

def vertical_flip(mat):
    mat.reverse()

def diagonal_flip(mat):
    # for N x N
    N = len(mat)
    for i in range(N):
        for j in range(i + 1, N):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]

def anti_diagonal_flip(mat):
    # for N x N
    N = len(mat)
    for i in range(N):
        for j in range(N - 1 - i):
            mat[i][j], mat[N - 1 - j][N - 1 - i] = mat[N - 1 - j][N - 1 - i], mat[i][j]

def diagonal_transpose(mat):
    # for R x C
    # equivalent to [[mat[r][c] for r in range(R)] for c in range(C)]
    return [list(row) for row in zip(*mat)]

def anti_diagonal_transpose(mat):
    # for R x C
    # equivalent to [[mat[R - 1 - r][C - 1 - c] for r in range(R)] for c in range(C)]
    return [list(row) for row in zip(*mat[::-1])][::-1]

def rotate_clockwise(mat):
    vertical_flip(mat)
    diagonal_flip(mat)

def rotate_counterclockwise(mat):
    diagonal_flip(mat)
    vertical_flip(mat)
