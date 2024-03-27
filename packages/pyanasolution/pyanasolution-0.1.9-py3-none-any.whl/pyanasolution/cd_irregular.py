import math
import numpy as np
from ._solution_base import SolutionBase


class CDIrregular:
    def __init__(self):
        super().__init__()

    def calc(self, coord, t):
        # Unify the input parameter type.
        if isinstance(coord, np.ndarray):
            pass
        elif isinstance(coord, list):
            coord = np.array(coord)
        else:
            raise TypeError("The input coordinate must be a list of np.ndarray")
        # Check the input coord length.
        if len(coord) != 2:
            raise ValueError("The input coordinate must have a length of 2.")

        return math.pi * (math.exp(-coord[0]) + math.exp(-coord[1])) * math.exp(-t)
