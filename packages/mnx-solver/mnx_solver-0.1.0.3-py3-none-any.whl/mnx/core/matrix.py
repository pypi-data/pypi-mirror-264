"""
Created by 0xCamiX with 🩵
"""

import numpy as np

class Matrix:
    def __init__(self, multi_array: np.array):
        self.multi_array = np.asarray(multi_array, dtype=np.float64)
        self.shape = self.multi_array.shape

    def __add__(self, other: np.array):
        if self.shape != other.shape:
            raise ValueError("The shapes of the matrices are different")
        return Matrix(self.multi_array + other.multi_array)

    def __sub__(self, other: np.array):
        if self.shape != other.shape:
            raise ValueError("The shapes of the matrices are different")
        return Matrix(self.multi_array - other.multi_array)

    def __mul__(self, other: np.array):
        if self.shape[1] != other.shape[0]:
            raise ValueError("The number of columns of the first matrix "
                             "is different from the number of rows of the second matrix")
        return Matrix(np.dot(self.multi_array, other.multi_array))

    def __str__(self):
        return str(self.multi_array)