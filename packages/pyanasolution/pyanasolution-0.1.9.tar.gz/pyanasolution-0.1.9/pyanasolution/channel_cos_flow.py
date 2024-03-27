import cmath as cm
import numpy as np
from ._solution_base import SolutionBase


class ChannelCosFlow(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._d = [0, 0]
        self._add_param_info("Diffusion coe", "-", "_d", "list or np.ndarray")
        self._v_x = 0
        self._add_param_info("Horizontal velocity", "m/s", "_v_x", "float")

        # Fixed parameters used in calculations.
        self._h = 1
        self._w = 1
        self._k = 2 * np.pi / self._w

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

        # Calculate.
        self._lambda = cm.sqrt(complex((self._k**2) * self._d[0] / self._d[1], self._k * self._v_x / self._d[1]))
        self._c1 = (1 - cm.exp(self._lambda)) / (cm.exp(-self._lambda) - cm.exp(self._lambda))
        self._c2 = (cm.exp(-self._lambda) - 1) / (cm.exp(-self._lambda) - cm.exp(self._lambda))

        tmp = cm.exp(complex(0, self._k * coord[0]))
        tmp_1 = self._lambda * coord[1] / self._h
        return (tmp * (self._c1*cm.exp(-tmp_1) + self._c2*cm.exp(tmp_1))).real

    def doc(self):
        print("[PyAnaSolution] - Channel cos flow")
        print(" * A channel flow case with two cos dirichlet conditions on the top and bottom boundaries.")
        print("[Parameters]")
        self.print_param_info()

    def set_diffusion_coefficient(self, d):
        # Unify the input parameter type.
        if isinstance(d, np.ndarray):
            pass
        elif isinstance(d, list):
            d = np.array(d)
        else:
            raise TypeError("The input diffusion coefficient must be a list of np.ndarray")
        # Check the input coord length.
        if len(d) != 2:
            raise ValueError("The input diffusion coefficient must have a length of 2.")

        self._d = d

    def set_horizontal_velocity(self, v_x):
        self._v_x = v_x
