import numpy as np

from mnx.utils.norms import optimize_norm
from mnx.approx_linear_methods.Richardson import RichardsonMethod
from mnx.approx_linear_methods.Jacobi import JacobiMethod
from mnx.approx_linear_methods.GaussSeidel import GaussSeidelMethod

class AproxLinearSolver:
    def __init__(self, A: np.array, b: np.array, x0: np.array, tol: float, max_iter: int):
        self.A = np.array(A)
        self.b = np.array(b)
        self.x0 = np.array(x0)
        self.tol = tol
        self.max_iter = max_iter
        self.method = {
            'richardson': RichardsonMethod(),
            'jacobi': JacobiMethod(),
            'gauss_seidel': GaussSeidelMethod(),
        }

    def optimize_method(self):
        """
        This method should be implemented to optimize the method used to solve the linear system.
        A good approach is to use the residual norm to choose the best method.

        :return:
        """
        pass

    def solve(self):
        return self.method['richardson'].solve(self.A, self.b, self.x0, self.tol, self.max_iter)

    def solve_all(self):
        return {
            'richardson': self.method['richardson'].solve(self.A, self.b, self.x0, self.tol, self.max_iter),
            'jacobi': self.method['jacobi'].solve(self.A, self.b, self.x0, self.tol, self.max_iter),
            'gauss_seidel': self.method['gauss_seidel'].solve(self.A, self.b, self.x0, self.tol, self.max_iter),
        }

    def stats(self):
        """
        This method should be implemented to print the error relative of the solution.

        :return:
        """
        pass


    def __str__(self):
        return \
f"""
Approximation of the linear system Ax = b

A: {self.A} \n
b: {self.b} \n
x0: {self.x0} \n
tol: {self.tol} \n
max_iter: {self.max_iter} \n

__________________________________________


1) Iterative relation: 
Richardson: Tx + b, where T = I - A and \n
T = {np.identity(len(self.b)) - self.A} \n

Jacobi: (I - D_a^-1 A)x + D_a^-1 b, where D_a is the diagonal of A \n
D_a = {np.diag(np.diag(self.A))} \n
D_a^-1 = {np.linalg.inv(np.diag(np.diag(self.A)))} \n
I - D_a^-1 A = {np.identity(len(self.b)) - np.dot(np.linalg.inv(np.diag(np.diag(self.A))), self.A)} \n
D_a^-1 b = {np.dot(np.linalg.inv(np.diag(np.diag(self.A))), self.b)} \n

Gauss-Seidel: (D_a + L_a)^-1 (b - U_a x), where L_a is the lower triangular part of A and U_a is the upper triangular part of A \n
D_a = {np.diag(np.diag(self.A))} \n
L_a = {np.tril(self.A, k=-1)} \n
U_a = {np.triu(self.A, k=1)} \n
D_a + L_a = {np.diag(np.diag(self.A)) + np.tril(self.A, k=-1)} \n
(D_a + L_a)^-1 = {np.linalg.inv(np.diag(np.diag(self.A)) + np.tril(self.A, k=-1))} \n
b - U_a x = {self.b - np.dot(np.triu(self.A, k=1), self.x0)} \n
(D_a + L_a)^-1 (b - U_a x) = {np.dot(np.linalg.inv(np.diag(np.diag(self.A)) + np.tril(self.A, k=-1)), self.b - np.dot(np.triu(self.A, k=1), self.x0))} \n

2) Which norm is the best to use for each method? \n

Richardson: {optimize_norm(self.A)}
Jacobi: {optimize_norm(self.A)}
Gauss-Seidel: {optimize_norm(self.A)}

3) Which method is the best to use? \n

{self.optimize_method()}

4) Solution: \n

{self.solve()}

5) Print error relative: \n

{self.stats()}

"""
