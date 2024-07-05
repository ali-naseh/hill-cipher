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


# delete row i and column j of given matrix
def find_minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]


def swap_columns(matrix, col1, col2):
    for row in matrix:
        row[col1], row[col2] = row[col2], row[col1]
    return matrix


def rezaiefar_det(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


    detM11 = rezaiefar_det(find_minor(matrix, 0, 0))
    detM1n = rezaiefar_det(find_minor(matrix, 0, n-1))
    detMn1 = rezaiefar_det(find_minor(matrix, n-1, 0))
    detMnn = rezaiefar_det(find_minor(matrix, n-1, n-1))

    M11nn = [row[1:n-1] for row in matrix[1:n-1]]
    detM11nn = rezaiefar_det(M11nn)



    if detM11nn == 0:
        for i in range(n):
            for j in range(i + 1, n):
                # copy of matrix
                new_matrix = [row[:] for row in matrix]  
                new_matrix = swap_columns(new_matrix, i, j)
                M11nn = [row[1:n-1] for row in new_matrix[1:n-1]]
                new_detM11nn = rezaiefar_det(M11nn)
                if new_detM11nn != 0:
                    detM11 = rezaiefar_det(find_minor(new_matrix, 0, 0))
                    detM1n = rezaiefar_det(find_minor(new_matrix, 0, n-1))
                    detMn1 = rezaiefar_det(find_minor(new_matrix, n-1, 0))
                    detMnn = rezaiefar_det(find_minor(new_matrix, n-1, n-1))
                    M11nn = [row[1:n-1] for row in new_matrix[1:n-1]]
                    detM11nn = rezaiefar_det(M11nn)
                    return -(detM11 * detMnn - detMn1 * detM1n) / detM11nn

        if detM11nn == 0:
            return 0 

    return (detM11 * detMnn - detMn1 * detM1n) / detM11nn



#Result
matrix = [[1, 0, 2],[4, 0, 1],[1, 1, 2]]
laplace = laplace_det(matrix=matrix)
gauss_jordan = gauss_jordan_det(matrix=matrix)
rezaiefar = rezaiefar_det(matrix=matrix)

print(f"Laplace Expansion : {laplace}")
print(f"Gauss-Jordan Elimination : {gauss_jordan}")
print(f"Rezaiefar Algorithm : {rezaiefar}")
