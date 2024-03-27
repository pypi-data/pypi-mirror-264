import numpy as np
from mnx.exact_linear_methods.IMethod import IMethod

class CholeskyMethod(IMethod):
    def solve(self, A: np.array, b: np.array):
        """
        Cholesky method for solving linear systems.

        :param A: np.array
        :param b: np.array
        :return: np.array
        """
        try:
            L = np.linalg.cholesky(A)
            LT = L.T

            y = [np.linalg.solve(L, bi) for bi in b]
            x = [np.linalg.solve(LT, yi) for yi in y]

            return x
        except np.linalg.LinAlgError:
            return None
