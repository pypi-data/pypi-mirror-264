import numpy as np

class LinearSolver:
    @staticmethod
    def create_solver(solver_type: str, A: np.array, b: np.array, *args):
        if solver_type == 'exact':
            from mnx.les.ExactSolver import ExactSolver
            return ExactSolver(A, b)
        elif solver_type == 'approximation':
            from mnx.les.ApproximationSolver import ApproximationSolver
            return ApproximationSolver(A, b, *args)
        else:
            raise ValueError(f"Unknown solver type: {solver_type}")