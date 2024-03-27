import time
import numpy as np

from mnx.utils.norms import optimize_norm
from mnx.utils.linalg import is_diagonally_dominant

from mnx.approx_linear_methods.Richardson import RichardsonMethod
from mnx.approx_linear_methods.Jacobi import JacobiMethod
from mnx.approx_linear_methods.GaussSeidel import GaussSeidelMethod

class ApproximationSolver:
    def __init__(self, A: np.array, b: np.array, x0: np.array, tol: float, max_iter: int):
        self.A = np.array(A)
        self.b = np.array(b)
        self.x0 = np.array(x0)
        self.tol = tol
        self.max_iter = max_iter

    @staticmethod
    def time_method(method, A, b, x0, tol, max_iter):
        start = time.time()
        method.solve(A, b, x0, tol, max_iter)
        end = time.time()
        return end - start


    def optimize(self):
        """
        This method should be implemented to optimize the method used to solve the linear system.
        A good approach is to use the residual norm to choose the best method.

        :return:
        """
        if is_diagonally_dominant(self.A):
            # Both Jacobi and Gauss-Seidel methods are applicable
            # Choose the one that converges faster
            jacobi_time = self.time_method(JacobiMethod(), self.A, self.b, self.x0, 1e-5, 10)
            gauss_time = self.time_method(GaussSeidelMethod(), self.A, self.b, self.x0, 1e-5, 10)

            return JacobiMethod() if jacobi_time < gauss_time else GaussSeidelMethod()
        else:
            # If the matrix is not diagonally dominant, we will use Richardson method
            print("Using Richardson method")
            return GaussSeidelMethod()


    def solve(self, method=None):
        if method:
            solution = method.solve(self.A, self.b, self.x0, self.tol, self.max_iter)
            return solution

        optimized_method = self.optimize()
        solution = optimized_method.solve(self.A, self.b, self.x0, self.tol, self.max_iter)

        if solution is not None:
            return solution
        return None
