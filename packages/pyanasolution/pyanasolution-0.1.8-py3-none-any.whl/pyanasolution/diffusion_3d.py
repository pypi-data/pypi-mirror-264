import math
import numpy as np
from ._solution_base import SolutionBase


class Diffusion3D(SolutionBase):
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

        # Calculate
        value = []
        value.append(math.exp(-6 * math.pi**2 * t))
        value.append(math.sin(2 * math.pi * coord[0]))
        value.append(math.sin(math.pi * coord[1]))
        value.append(math.sin(math.pi * coord[2]))

        return value[0]*value[1]*value[2]*value[3]
