def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    first_len = len(mat[0])
    for row in mat:
        if len(row)!=first_len:
            raise ValueError
    return [list(row) for row in zip(*mat)]
'''
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
print(transpose([[1, 2], [3]]))
'''

def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    first_len = len(mat[0])
    for row in mat:
        if len(row)!=first_len:
            raise ValueError
    return [int(sum(row)) for row in mat ]
'''
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
print(row_sums([[1, 2], [3]]))
'''
def col_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    first_len = len(mat[0])
    for row in mat:
        if len(row)!=first_len:
            raise ValueError
    transposed = [list(row) for row in zip(*mat)]
    return [int(sum(col)) for col in transposed]
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
print(col_sums([[1, 2], [3]]))
