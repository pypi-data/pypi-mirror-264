import numpy as np

from mnx.approx_linear_methods.IMethod import IMethod
from mnx.utils.norms import optimize_norm

class JacobiMethod(IMethod):
    @staticmethod
    def get_transformation_matrix(A: np.array):
        I = np.eye(A.shape[0])
        D = np.diag(np.diag(A))
        D_inv = np.linalg.inv(D)
        return I - D_inv.dot(A)

    @staticmethod
    def get_diagonal_matrix(A: np.array):
        return np.diag(np.diag(A)), np.linalg.inv(np.diag(np.diag(A)))

    def get_transformation_norm(self, A: np.array):
        T = self.get_transformation_matrix(A)
        return optimize_norm(T)

    def solve(self, A: np.array, b: np.array, x0: np.array, tol: float, max_iter: int):
        n = len(b)
        A = np.array(A, float)
        b = np.array(b, float).reshape(n, 1)
        x0 = np.array(x0, float).reshape(n, 1)
        T = self.get_transformation_matrix(A)
        D, D_inv = self.get_diagonal_matrix(A)

        x = x0

        print("x0 = T_j*x + D^(-1)*b = ", T, "*", x, "+", D_inv, "*", b)

        for i in range(max_iter):
            x = T.dot(x) + D_inv.dot(b)
            norm, _ = optimize_norm(A.dot(x) - b)
            if norm < tol:
                return x, i
