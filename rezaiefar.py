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

n = int(input("Enter n : ").strip())

matrix = []
for _ in range(n):
    row = list(map(float, input(f"Enter row number {_+1} : ").strip().split()))
    matrix.append(row)


determinant = rezaiefar_det(matrix)
print(f"determinant : {determinant}")