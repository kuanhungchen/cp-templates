def horizontal_flip(mat):
    n = len(mat)
    for i in range(n):
        for j in range(n // 2):
            mat[i][j], mat[i][~j] = mat[i][~j], mat[i][j]

def vertical_flip(mat):
    n = len(mat)
    for j in range(n):
        for i in range(n // 2):
            mat[i][j], mat[~i][j] = mat[~i][j], mat[i][j]

def diagonal_flip(mat):
    n = len(mat)
    for i in range(n):
        for j in range(i):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]

def rotate(mat, reverse=False):
    # if reverse=False, rotate mat clockwise; otherwise counterclockwise
    if not reverse: vertical_flip(mat)
    else:           horizontal_flip(mat)
    diagonal_flip(mat)
