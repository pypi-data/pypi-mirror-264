import numpy as np
from abc import ABC, abstractmethod

class IExactMethod(ABC):
    @abstractmethod
    def solve(self, A: np.array, b: np.array):
        pass


