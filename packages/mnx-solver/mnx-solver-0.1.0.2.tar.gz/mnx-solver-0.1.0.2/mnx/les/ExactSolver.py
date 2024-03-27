import numpy as np

from mnx.utils.linalg import is_non_singular
from mnx.utils.linalg import is_symmetric
from mnx.utils.linalg import is_definite_positive

from mnx.exact_linear_methods.LU import LUMethod
from mnx.exact_linear_methods.Cholesky import CholeskyMethod
from mnx.exact_linear_methods.Gauss import GaussMethod


class ExactSolver:
    def __init__(self, A: np.array, b: [np.array]):
        self.A = np.array(A)
        self.b = b
        self.multiple_b = len(self.b) > 1
        self.methods = [
            (lambda A_: is_symmetric(A_) and is_definite_positive(A_), CholeskyMethod()),
            (lambda A_: is_non_singular(A_), LUMethod()),
            (lambda A_: True, GaussMethod()) # default method
        ]

    def optimize(self):
        """
        Optimize the method for the given problem.
        Using the coefficients of the matrix A,
        this method should return the best method
        to solve the linear system.

        :return: IMethod
        """
        for condition, method in self.methods:
            if condition(self.A):
                return method
        return None

    def solve(self, method=None):
        if method:
            solution = method.solve(self.A, self.b)
            return solution

        optimized_method = self.optimize()
        solution = optimized_method.solve(self.A, self.b)

        if solution is not None:
            return solution
        return None