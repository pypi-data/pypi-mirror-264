import math
import numpy as np
from ._solution_base import SolutionBase


class GaussianHill2D(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._d = np.array([[0.0, 0.0], [0.0, 0.0]])
        self._add_param_info("Diffusion coefficient", "-", "_d", "np.array", "The diffusion coefficient matrix.")
        self._sigma = 0
        self._add_param_info("Sigma", "-", "_sigma", "float", "A mathematics parameter.")
        self._v = np.array([0.0, 0.0])
        self._add_param_info("Velocity", "m/s", "_v", "list or np.array", "The field velocity.")

    def calc(self, coord, time):
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

        # Calculate temporary parameters.
        fai_0 = 2 * math.pi * self._sigma**2

        # Calculate.
        sigma_t = self._sigma**2 * np.eye(2) + 2 * time * self._d
        param_0 = fai_0 / (2 * math.pi * math.sqrt(abs(np.linalg.det(sigma_t))))

        vec_0 = coord - self._v * time
        vec_1 = vec_0.reshape([2, 1])
        mat_0 = np.multiply(vec_0, vec_1)

        return param_0 * math.exp(-0.5 * np.vdot(np.linalg.inv(sigma_t), mat_0))

    def calc_initial_value(self, coord):
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

        return math.exp(-1 / (2 * self._sigma**2) * np.linalg.norm(coord)**2)

    def doc(self):
        print("[PyAnaSolution - Gaussian hill (2D)]")
        print(" * A concentration species with an initial Gaussian profile develops "
              "in the presence of a uniform velocity field.")
        print("[Parameters]")
        self.print_param_info()

    def set_diffusion_coefficient(self, d):
        # Unify the input parameter type.
        if not isinstance(d, np.ndarray):
            raise TypeError("The diffusion coefficient must be a np.array")
        # Check the input coord length.
        if d.shape != (2, 2):
            raise ValueError("The diffusion coefficient must be a matrix with a size of 2x2.")

        self._d = d

    def set_sigma(self, sigma):
        self._sigma = sigma

    def set_velocity(self, v):
        # Unify the input parameter type.
        if isinstance(v, np.ndarray):
            pass
        elif isinstance(v, list):
            v = np.array(v)
        else:
            raise TypeError("The input velocity must be a list of np.ndarray")
        # Check the input velocity length.
        if len(v) != 2:
            raise ValueError("The input velocity must have a length of 2.")

        self._v = v
