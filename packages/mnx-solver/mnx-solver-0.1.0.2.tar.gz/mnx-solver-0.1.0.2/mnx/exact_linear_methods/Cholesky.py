"""
Cholesky method for solving linear systems.

This method is based on the Cholesky decomposition of a matrix. It is a method that is used to solve
linear systems of equations. The Cholesky decomposition is a decomposition of a matrix into a lower
triangular matrix and its transpose. The Cholesky decomposition is used to solve linear systems of
equations by first decomposing the matrix into its lower triangular form and then solving the system
of equations using forward and backward substitution.
"""

import numpy as np
from mnx.exact_linear_methods.IMethod import IExactMethod

class CholeskyMethod(IExactMethod):
    def solve(self, A: np.array, b: np.array):
        """
        Cholesky method for solving linear systems.

        :param A: np.array
        :param b: np.array
        :return: np.array
        """
        print("CholeskyMethod")
        try:
            L = np.linalg.cholesky(A)
            LT = L.T

            y = [np.linalg.solve(L, bi) for bi in b]
            x = [np.linalg.solve(LT, yi) for yi in y]

            return x
        except np.linalg.LinAlgError:
            return None
