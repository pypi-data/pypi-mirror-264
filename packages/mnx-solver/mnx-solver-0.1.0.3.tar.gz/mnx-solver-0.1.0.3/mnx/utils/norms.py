"""
Compute the norm a Matrix.

This module provides a function to compute the norm of a matrix. Decide which is the best norm to use and
return the value of the norm.
"""

import numpy as np

def optimize_norm(A: np.array) -> tuple:
    """
    Compute the norm of a matrix.

    :param A: np.array
    :return: float
    """
    norms_value = {
        'frobenius': np.linalg.norm(A, ord='fro'),
        '1': np.linalg.norm(A, ord=1),
        'inf': np.linalg.norm(A, ord=np.inf),
    }
    return min(norms_value.values()), min(norms_value, key=norms_value.get)
