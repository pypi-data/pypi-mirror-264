import numpy as np

from mnx.approx_linear_methods.IMethod import IMethod
from mnx.utils.norms import optimize_norm


class RichardsonMethod(IMethod):
    @staticmethod
    def get_transformation_matrix(A: np.array):
        Q = np.eye(A.shape[0])
        T = Q - A
        return T

    def get_transformation_norm(self, A: np.array):
        T = self.get_transformation_matrix(A)
        return optimize_norm(T)

    def solve(self, A: np.array, b: np.array, x0: np.array, tol: float, max_iter: int):
        n = len(b)
        A = np.array(A, float)
        b = np.array(b, float).reshape(n, 1)
        x0 = np.array(x0, float).reshape(n, 1)
        T = self.get_transformation_matrix(A)

        x = x0

        print(f"x0 = T_r*x + b = {T} * {x} + {b}")

        for i in range(max_iter):
            x = T.dot(x) + b
            norm, _ = optimize_norm(A.dot(x) - b)
            if norm < tol:
                return x, i
        return x, max_iter