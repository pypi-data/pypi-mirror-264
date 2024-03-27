def rule_out_cholesky(A):
    """
    Rule out the Cholesky method if the matrix is not symmetric or definite positive.
    :param A: list
    :return: bool
    """

    return """Matrix is not symmetric or definite positive. Cholesky method is not applicable."""

def rule_out_lu(A):
    """
    Rule out the LU method if the matrix is singular.
    :param A: list
    :return: str
    """

    return """Matrix is singular. LU method is not applicable."""

def rule_out_gauss(A):
    """
    Rule out the Gauss method if the matrix is singular.
    :param A: list
    :return: str
    """

    return """Matrix is singular. Gauss method is not applicable."""

def rule_out_gauss_jordan(A):
    """
    Rule out the Gauss-Jordan method if the matrix is singular.
    :param A: list
    :return: str
    """

    return """Matrix is singular. Gauss-Jordan method is not applicable."""