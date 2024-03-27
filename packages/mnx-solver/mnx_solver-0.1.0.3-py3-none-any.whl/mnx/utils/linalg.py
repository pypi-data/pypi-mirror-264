"""
Utils for linalg operations.
"""

import numpy as np
from numpy import bool_

def is_symmetric(A: np.array) -> bool:
    """
    Check if a matrix is symmetric.

    :param A: np.array
    :return: bool
    """
    return np.array_equal(A, A.T)

def is_definite_positive(A: np.array) -> bool_:
    """
    Check if a matrix is definite positive.

    :param A: np.array
    :return: bool
    """
    return np.all(np.linalg.eigvals(A) > 0)

def is_non_singular(A: np.array) -> bool:
    """
    Check if a matrix is non-singular.

    :param A: np.array
    :return: bool
    """
    return np.linalg.matrix_rank(A) == A.shape[0]

def is_diagonally_dominant(A: np.array) -> bool_:
    """
    Check if a matrix is diagonally dominant.

    :param A: np.array
    :return: bool
    """
    D = np.diag(np.abs(A))
    S = np.sum(np.abs(A), axis=1) - D
    return np.all(D > S)