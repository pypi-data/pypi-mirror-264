import math
from ._solution_base import SolutionBase


class SemiInfiniteFlow1D(SolutionBase):
    def __init__(self):
        super().__init__()

        self._d = 0
        self._add_param_info("Diffusion coefficient", "-", "_d", "float")
        self._v_x = 0
        self._add_param_info("Horizontal velocity", "-", "_v_x", "float")

    def set_diffusion_coefficient(self, d):
        self._d = d

    def set_horizontal_velocity(self, v_x):
        self._v_x = v_x

    def calc(self, coord, t):
        tmp_1 = math.erfc((coord - self._v_x * t) / (2 * math.sqrt(self._d * t)))
        tmp_2 = math.exp(self._v_x * coord / self._d)
        tmp_3 = math.erfc((coord + self._v_x * t) / (2*math.sqrt(self._d * t)))

        return 0.5 * (tmp_1 + tmp_2 * tmp_3)
