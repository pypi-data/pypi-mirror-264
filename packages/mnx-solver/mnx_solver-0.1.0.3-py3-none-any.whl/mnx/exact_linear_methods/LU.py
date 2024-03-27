"""
LU method for solving linear systems.

This module contains the LU method for solving linear systems. The method is implemented in the
solve function, which receives a matrix A and a vector b and returns the solution to the system.

The LU method is based on the LU decomposition of a matrix. It is a method that is used to solve
linear systems of equations. The LU decomposition is a decomposition of a matrix into a lower
triangular matrix and an upper triangular matrix. The LU decomposition is used to solve linear
systems of equations by first decomposing the matrix into its lower and upper triangular forms
and then solving the system of equations using forward and backward substitution.
"""

import numpy as np
from scipy.linalg import lu_factor, lu_solve
from mnx.exact_linear_methods.IMethod import IExactMethod

class LUMethod(IExactMethod):
    def solve(self, A: np.array, b: np.array):
        """
        LU method for solving linear systems.

        :param A: np.array
        :param b: np.array
        :return: np.array
        """
        print("LUMethod")
        try:
            LU, Piv = lu_factor(A)
            x = [lu_solve((LU, Piv), bi) for bi in b]

            return x
        except np.linalg.LinAlgError:
            return None