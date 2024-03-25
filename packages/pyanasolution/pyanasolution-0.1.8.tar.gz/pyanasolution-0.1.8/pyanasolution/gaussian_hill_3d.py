import math
import numpy as np
from ._solution_base import SolutionBase


class GaussianHill3D(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters
        self._d = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        self._add_param_info("Diffusion coefficient", "-", "_d", "np.array", "The diffusion coefficient matrix.")
        self._phi_0 = 0
        self._add_param_info("Total concentration", "-", "_phi_0", "float")
        self._sigma_0_2 = 0
        self._add_param_info("Sigma_2", "-", "_sigma_0_2", "float")
        self._v = np.array([0.0, 0.0, 0.0])
        self._add_param_info("Velocity", "m/s", "_v", "np.array", "The field velocity.")

    def calc(self, coord, time):
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

        # Calculation.
        sigma_ij = self._sigma_0_2 * np.eye(3) + 2 * time * self._d

        tmp_d = (2 * math.pi)**(3/2) * math.sqrt(abs(np.linalg.det(sigma_ij)))

        vec_r = coord - self._v * time
        vec_c = vec_r.reshape([3, 1])
        mat = np.multiply(vec_r, vec_c)
        tmp_r = math.exp(-0.5 * np.vdot(np.linalg.inv(sigma_ij), mat))
        # tmp_r = math.exp(-0.5 * np.dot(np.dot(vec_r, np.linalg.inv(sigma_ij)), vec_r))

        return (self._phi_0 / tmp_d) * tmp_r

    def doc(self):
        print("[PyAnaSolution - Gaussian hill (3D)]")
        print(" * A concentration species with an initial Gaussian profile develops "
              "in the presence of a uniform velocity field.")
        print("[Parameters]")
        self.print_param_info()

    def set_diffusion_coefficient(self, d):
        # Unify the input parameter type.
        if not isinstance(d, np.ndarray):
            raise TypeError("The diffusion coefficient must be a np.array")
        # Check the input coord length.
        if d.shape != (3, 3):
            raise ValueError("The diffusion coefficient must be a matrix with a size of 3x3.")

        self._d = d

    def set_initial_variance(self, sigma_0_2):
        self._sigma_0_2 = sigma_0_2

    def set_total_concentration(self, phi_0):
        self._phi_0 = phi_0

    def set_velocity(self, v):
        # Unify the input parameter type.
        if isinstance(v, np.ndarray):
            pass
        elif isinstance(v, list):
            v = np.array(v)
        else:
            raise TypeError("The input velocity must be a list of np.ndarray")
        # Check the input coord length.
        if len(v) != 3:
            raise ValueError("The input velocity must have a length of 3.")

        self._v = v
