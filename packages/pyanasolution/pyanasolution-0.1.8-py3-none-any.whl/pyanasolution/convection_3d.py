import math
import numpy as np
from ._solution_base import SolutionBase


class Convection3D(SolutionBase):
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
        if len(coord) != 3:
            raise ValueError("The input coordinate must have a length of 3.")

        return math.exp(-3 * t) * math.exp(coord[0] + coord[1] + coord[2])
