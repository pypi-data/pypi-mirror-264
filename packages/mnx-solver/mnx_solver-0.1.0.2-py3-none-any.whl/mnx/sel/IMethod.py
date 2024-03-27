import numpy as np
from abc import ABC, abstractmethod

class IMethod(ABC):
    @abstractmethod
    def solve(self, A: np.array, b: np.array):
        pass


