import numpy as np

from mnx.utils.linalg import is_non_singular, is_symmetric, is_definite_positive

from mnx.exact_linear_methods.LU import LUMethod
from mnx.exact_linear_methods.Cholesky import CholeskyMethod
from mnx.exact_linear_methods.Gauss_Jordan import GaussJordanMethod
from mnx.exact_linear_methods.Gauss import GaussMethod

from mnx.utils.rule_out import rule_out_cholesky
from mnx.utils.rule_out import rule_out_lu
from mnx.utils.rule_out import rule_out_gauss
from mnx.utils.rule_out import rule_out_gauss_jordan

class LinearSolver:
    def __init__(self, A: np.array, *b: np.array):
        self.A = np.array(A)
        self.b = list(np.array(b))
        print(self.b)
        self.multi_b = len(self.b) > 1
        self.methods = {
            'cholesky': CholeskyMethod(),
            'lu': LUMethod(),
            'gauss': GaussMethod(),
            'gauss_jordan': GaussJordanMethod()
        }
        self.rule_out_errors = {
            'cholesky': rule_out_cholesky,
            'lu': rule_out_lu,
            'gauss': rule_out_gauss,
            'gauss_jordan': rule_out_gauss_jordan
        }
        self.best_method, self.scores, self.possible_methods = self.optimize()
        self.discarded_methods = {k: v for k, v in self.methods.items() if k not in self.possible_methods}

    def optimize(self):
        """
        Optimize the method for the given problem.

        :return: IMethod
        """
        scores = {
            'cholesky': 0,
            'lu': 0,
            'gauss_jordan': 0,
            'gauss': 0
        }

        if is_non_singular(self.A):
            scores['lu'] += 1
            scores['gauss'] += 1
            scores['gauss_jordan'] += 1

        if is_symmetric(self.A):
            scores['cholesky'] += 1
        else:
            scores['cholesky'] -= 1


        if is_definite_positive(self.A):
            scores['cholesky'] += 1
        else:
            scores['cholesky'] -= 1

        if self.multi_b:
            scores['lu'] += 1
            scores['cholesky'] += 1

        print("Optimized method: ", max(scores, key=scores.get), scores)
        possible_methods = [k for k, v in scores.items() if v >= 0]

        return max(scores, key=scores.get), scores, possible_methods

    def solve(self):
        method = self.methods[self.best_method]
        solution = method.solve(self.A, self.b)

        if solution is not None:
            return solution
        return None

    def solve_all(self):
        """
        Filter the methods that can solve the problem and return the solutions.
        :return: dict
        """
        solutions = {}

        # Remove the best method from the list.
        solvers_methods = self.possible_methods.copy()
        solvers_methods.remove(self.best_method)

        for method in solvers_methods:
            solution = self.methods[method].solve(self.A, self.b)
            if solution is not None:
                solutions[method] = solution

        return solutions, solvers_methods

    def rule_out(self, methods):
        """
        Explain why the method was not chosen.
        :param methods: dict
        :return: str
        """
        print(methods)
        reasons = {}
        for method, obj in methods.items():
            reasons[method] = self.rule_out_errors[method](self.A)
        return reasons

    def __str__(self):
        return f"""
        >>> Linear Solver <<<
        
A: {self.A}
b: {self.b}

        >>> Result <<<
        
a. Best Method: {self.best_method}
b. Solution: {self.solve()}
c. Other Methods: {self.solve_all()}
d. Explained why no other method was chosen: {self.rule_out(self.discarded_methods)}
        """