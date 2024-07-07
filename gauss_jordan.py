def gauss_jordan_det(matrix):
    size = len(matrix)
    A = [row[:] for row in matrix]  # Make a copy of the matrix

    # Initialize determinant and current sign of determinant
    det = 1

    for i in range(size):
        # Find the pivot (non-zero element) in column i
        pivot_row = i
        while pivot_row < size and A[pivot_row][i] == 0:
            pivot_row += 1
        
        if pivot_row == size:
            return 0  # If no pivot found, determinant is zero
        
        # Swap current row (i) with pivot row (pivot_row) if necessary
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            det *= -1  # Change sign of determinant
        
        # Update determinant with the pivot element
        det *= A[i][i]

        # Eliminate other elements in the current column
        for j in range(i + 1, size):
            if A[j][i] != 0:
                ratio = A[j][i] / A[i][i]
                for k in range(i, size):
                    A[j][k] -= ratio * A[i][k]
    
    return det



n = int(input("Enter n : ").strip())

matrix = []
for _ in range(n):
    row = list(map(float, input(f"Enter row number {_+1} : ").strip().split()))
    matrix.append(row)


determinant = gauss_jordan_det(matrix)
print(f"determinant : {determinant}")
