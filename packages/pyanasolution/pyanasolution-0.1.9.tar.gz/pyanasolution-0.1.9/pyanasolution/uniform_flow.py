import math
import numpy as np
from ._solution_base import SolutionBase


class UniformFlow(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._d = 0
        self._add_param_info("Diffusion coefficient", "-", "_d", "float")
        self._phi = 0
        self._add_param_info("Initial value", "-", "_phi", "float", "The initial value of the computational domain.")
        self._v_x = 0
        self._add_param_info("Horizontal velocity", "m/s", "_v_x", "float")

    def calc(self, coord):
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

        # Calculate the solution.
        return self._phi*math.erfc(coord[1]/math.sqrt(4*self._d*coord[0]/self._v_x))

    def doc(self):
        print("[PyAnaSolution - Uniform flow]")
        print(" * The concentration layer development near a semi-infinite plate"
              ", controlled by a uniform horizontal fluid velocity.")
        print("[Parameters]")
        self.print_param_info()

    def set_diffusion_coe(self, d):
        self._d = d

    def set_horizontal_velocity(self, v_x):
        self._v_x = v_x

    def set_initial_value(self, phi):
        self._phi = phi
