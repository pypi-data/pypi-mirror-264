import numpy as np
from mnx.approx_linear_methods.IMethod import IMethod
from mnx.utils.norms import optimize_norm

class GaussSeidelMethod(IMethod):
    @staticmethod
    def get_transformation_matrix(A: np.array):
        D = np.diag(np.diag(A))
        L = np.tril(A, k=-1)
        DL_inv = np.linalg.inv(D + L)
        return -DL_inv.dot(np.triu(A, k=1))

    @staticmethod
    def get_lower_triangular_matrix(A: np.array):
        L = np.tril(A)
        return L, np.linalg.inv(L)

    def get_transformation_norm(self, A: np.array, b: np.array):
        T = self.get_transformation_matrix(A)
        return optimize_norm(T)

    def solve(self, A: np.array, b: np.array, x0: np.array, tol: float, max_iter: int):
        n = len(b)
        A = np.array(A, float)
        b = np.array(b, float).reshape(n, 1)
        x0 = np.array(x0, float).reshape(n, 1)
        T = self.get_transformation_matrix(A)
        L, L_inv = self.get_lower_triangular_matrix(A)

        x = x0

        print("x0 = T_gs*x + D^(-1)*b = ", T, "*", x, "+", L_inv, "*", b)

        for i in range(max_iter):
            x = T.dot(x) + L_inv.dot(b)
            norm, _ = optimize_norm(A.dot(x) - b)
            if norm < tol:
                return x, i