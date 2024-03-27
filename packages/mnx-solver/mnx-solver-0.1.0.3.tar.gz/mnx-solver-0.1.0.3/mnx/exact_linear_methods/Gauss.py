"""
Gauss method for solving linear systems.

This method is based on the Gauss elimination method, which is a direct method for solving linear systems.
It is a simple method that is not very efficient for large systems, but it is very accurate and stable.

The method is based on the following steps:
1. Partial Pivoting: If the diagonal element is zero, the method will swap the current row with another row
that has a non-zero element in the same column. This is done to avoid division by zero.

2. Elimination: The method will iterate over each row and column, and will eliminate the elements below the
diagonal by subtracting a multiple of the current row from the rows below it.

3. Back Substitution: Once the matrix is in upper triangular form, the method will solve the system by
back substitution.
"""

import numpy as np
from mnx.exact_linear_methods.IMethod import IExactMethod

def solve_gauss(A: np.array, b: np.array):
    """
    Gauss method for solving a single linear system.

    :param A: np.array
    :param b: np.array
    :return: np.array
    """
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)
    x = np.zeros(n, float)

    Ab = np.column_stack((A, b))

    for i in range(n):
        # Partial Pivoting
        if Ab[i, i] == 0:
            for r in range(i+1, n):
                if Ab[r, i] != 0:
                    Ab[[i, r]] = Ab[[r, i]]
                    break
            else:
                return None

        for j in range(i+1, n):
            ratio = Ab[j][i] / Ab[i][i]
            for k in range(n+1):
                Ab[j][k] -= ratio * Ab[i][k]

    x[n-1] = Ab[n-1][n] / Ab[n-1][n-1]

    for i in range(n-2, -1, -1):
        x[i] = Ab[i][n]
        for j in range(i+1, n):
            x[i] -= Ab[i][j] * x[j]
        x[i] /= Ab[i][i]

    return x


class GaussMethod(IExactMethod):
    def solve(self, A: np.array, b):
        """
        Gauss method for solving linear systems.

        :param A: np.array
        :param b: np.Array or list of np.Array
        :return: np.Array or list of np.Array
        """
        print("GaussMethod")
        if isinstance(b, list):  # if b is a list of arrays
            solutions = []
            for bi in b:  # iterate over each array in the list
                solution = solve_gauss(A, bi)
                if solution is not None:
                    solutions.append(solution)
                else:
                    solutions.append(None)
            return solutions
        else:  # if b is a single array
            return solve_gauss(A, b)

