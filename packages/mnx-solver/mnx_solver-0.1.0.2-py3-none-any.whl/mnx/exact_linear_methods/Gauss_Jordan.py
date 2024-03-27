"""
Gauss-Jordan method for solving linear systems.

This module contains the Gauss-Jordan method for solving linear systems. The method is implemented in the
solve_gauss_jordan function, which receives a matrix A and a vector b and returns the solution to the system.
"""

import numpy as np
from mnx.exact_linear_methods.IMethod import IExactMethod

def solve_gauss_jordan(A: np.array, b: np.array):
    """
    Gauss-Jordan method for solving a single linear system.

    :param A: np.array
    :param b: np.array
    :return: np.array
    """
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)

    for k in range(n):
        if np.fabs(A[k, k]) < 1.0e-12:
            for i in range(k+1, n):
                if np.fabs(A[i, k]) > np.fabs(A[k, k]):
                    for j in range(k, n):
                        A[k, j], A[i, j] = A[i, j], A[k, j]
                    b[k], b[i] = b[i], b[k]
                    break
        pivot = A[k, k]
        for j in range(k, n):
            A[k, j] /= pivot
        b[k] /= pivot
        for i in range(n):
            if i == k or A[i, k] == 0: continue
            factor = A[i, k]
            for j in range(k, n):
                A[i, j] -= factor * A[k, j]
            b[i] -= factor * b[k]

    return b


class GaussJordanMethod(IExactMethod):
    def solve(self, A: np.array, b):
        """
        Gauss-Jordan method for solving linear systems.

        :param A: np.array
        :param b: np.Array or list of np.Array
        :return: np.Array or list of np.Array
        """
        if isinstance(b, list):  # if b is a list of arrays
            solutions = []
            for bi in b:  # iterate over each array in the list
                solution = solve_gauss_jordan(A, bi)
                if solution is not None:
                    solutions.append(solution)
                else:
                    solutions.append(None)
            return solutions
        else:  # if b is a single array
            return solve_gauss_jordan(A, b)

