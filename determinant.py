import numpy as np

# Laplace Expansion
def laplace_det(matrix):
    size = len(matrix)
    
    if size == 1:
        return matrix[0][0]

    det = 0
    for j in range(size):
        # delete row i and column j
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** j
        cofactor = sign * matrix[0][j] * laplace_det(submatrix)
        det += cofactor

    return det


# Gauss-Jordan Elimination
def gauss_jordan_det(matrix):
    size = len(matrix)
    A = np.array(matrix, dtype=float)
    det = 1
    for i in range(size):
        # find the largest pivot element in each column
        max_row = i + np.argmax(np.abs(A[i:, i]))
        # switch rows if the current pivot is not the largest
        if i != max_row:
            A[[i, max_row]] = A[[max_row, i]]
            det *= -1  # change sign of det 
        # choose pivot
        pivot = A[i, i]
        if pivot == 0:
            return 0 
        # splitting the pivot row into the pivot element for normalization
        det *= pivot
        A[i] = A[i] / pivot
        # make other elemnts of column zero
        for j in range(size):
            if i != j:
                ratio = A[j, i]
                A[j] -= ratio * A[i]

    return det



#Result
matrix = [[1, 0, 2],[4, 0, 1],[1, 1, 2]]
laplace = laplace_det(matrix=matrix)
gauss_jordan = gauss_jordan_det(matrix=matrix)

print(f"Laplace Expansion : {laplace}")
print(f"Gauss-Jordan Elimination : {gauss_jordan}")
