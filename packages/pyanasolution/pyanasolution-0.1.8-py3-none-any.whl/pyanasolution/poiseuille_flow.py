import math
import numpy as np
from scipy.special import hyp1f1
from ._solution_base import SolutionBase


class PoiseuilleFlow(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._d = 0
        self._add_param_info("Diffusion coefficient", "-", "_d", "float")
        self._h = 0
        self._add_param_info("Height", "m", "_h", "float", "The height of the channel.")
        self._phi = 0
        self._add_param_info("Initial value", "-", "_phi", "float")
        self._v_x = 0
        self._add_param_info("Horizontal velocity", "m/s", "_v_x", "float")

        # Fixed parameters used in calculations.
        self.__m = [1.2967, 2.3811, 3.1093, 3.6969, 4.2032, 4.6548, 5.0662, 5.4467, 5.8023, 6.1373]
        self.__C_m = [1.2008, -0.2991, 0.1608, -0.1074, 0.0796, -0.0627, 0.0515, -0.0435, 0.0375, -0.0329]

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

        # Calculate the péclet number.
        Pe = self._v_x * self._h / self._d
        # Calculate the dimensionless coordinates.
        x = coord[0] / self._h
        y = coord[1] / self._h

        # Calculate.
        coe_2 = 0
        for i in range(10):
            coe_0 = pow(self.__m[i], 4) * (1 / Pe) * x;
            coe_1 = pow(self.__m[i], 2) * pow(y, 2) * 0.5
            coe_2 += self.__C_m[i] * math.exp(-1*coe_0 - coe_1) * self.__calc_hypergeometric_function(y, i)

        return self._phi * (1 - coe_2)

    def doc(self):
        print("[PyAnaSolution - Poiseuille flow]")
        print(" * The concentration layer development in a Poiseuille flow between two parallel plates "
              "with distance 2H.")
        print("[Parameters]")
        self.print_param_info()

    def set_diffusion_coe(self, d):
        self._d = d

    def set_height(self, h):
        self._h = h

    def set_horizontal_velocity(self, v_x):
        self._v_x = v_x

    def set_initial_value(self, phi):
        self._phi = phi

    def __calc_hypergeometric_function(self, y, i):
        a = (1 - pow(self.__m[i], 2)) / 4
        b = 1 / 2
        c = pow(self.__m[i], 2) * pow(y, 2)

        return hyp1f1(a, b, c)