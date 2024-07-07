def laplace_det(matrix):
    size = len(matrix)
    
    if size == 1:
        return matrix[0][0]

    det = 0
    for j in range(size):
        # delete row 0 and column j
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** j
        cofactor = sign * matrix[0][j] * laplace_det(submatrix)
        det += cofactor

    return det


n = int(input("Enter n : ").strip())

matrix = []
for _ in range(n):
    row = list(map(float, input(f"Enter row number {_+1} : ").strip().split()))
    matrix.append(row)


determinant = laplace_det(matrix)
print(f"determinant : {determinant}")
