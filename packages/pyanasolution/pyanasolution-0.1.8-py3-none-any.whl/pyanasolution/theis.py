import math
import numpy as np
from ._solution_base import SolutionBase


class Theis(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._q = 0
        self._add_param_info("Flow rate", "m^3/s", "_q", "float", "The injection well is positive and vice versa.")
        self._g = 9.8
        self._add_param_info("Gravity acceleration", "m/(s^2)", "_g", "float", "The gravity acceleration.")
        self._h = 0
        self._add_param_info("Initial head", "m", "_h", "float", "The initial head of the field.")
        self._k = 0
        self._add_param_info("Permeability", "m^2", "_k", "float")
        self._S_s = 0
        self._add_param_info("Storage", "m^(-1)", "_S_s", "float")
        self._b = 1
        self._add_param_info("Thick", "m", "_b", "float", "The aquifer thick.")
        self._t = 0
        self._add_param_info("Time", "s", "_t", "float", "The operation time.")
        self._rho_f = 1000
        self._add_param_info("Fluid density", "kg/m^3", "_rho_f", "float")
        self._niu = 1.01e-3
        self._add_param_info("Fluid viscosity", "Pa∙s", "_niu", "float")
        self._coord_w = np.array([0.0, 0.0], dtype=np.double)
        self._add_param_info("Well coordinate", "m", "_coord_w", "list or np.ndarray")

        # Fixed parameters used in calculations.
        self.__a = [-0.57721566, 0.99999193, -0.24991055, 0.05519968, -0.00976004, 0.00107857]
        self.__b = [0.2677737343, 8.6347608925, 18.059016973, 8.5733287401]
        self.__c = [3.9584969228, 21.0996530827, 25.6329561486, 9.5733223454]

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

        # Calculate permeability coefficient.
        K = self._b * self._k * self._rho_f * self._g / self._niu
        # Calculate the variable of the series calculation function.
        u = self._S_s * self._b * np.linalg.norm(coord - self._coord_w)**2 / (4 * K * self._t)
        # Calculate the hydraulic head change.
        h_c = self._q * self.__calc_series_num(u) / (4 *math.pi *K)

        return self._h + h_c

    def doc(self):
        print("[PyAnaSolution - Theis]")
        print(" * The Theis model is a seminal mathematical solution in the field of hydrogeology for "
              "quantifying transient groundwater flow in a confined aquifer. (Provided by ChatGPT)")
        print("[Parameters]")
        self.print_param_info()

    def set_fluid_density(self, rho_f):
        self._rho_f = rho_f

    def set_fluid_viscosity(self, niu):
        self._niu = niu

    def set_gravity_acceleration(self, g):
        self._g = g

    def set_initial_head(self, h):
        self._h = h

    def set_permeability(self, k):
        self._k = k

    def set_storage(self, S_s):
        self._S_s = S_s

    def set_thick(self, b):
        self._b = b

    def set_time(self, t):
        self._t = t

    def set_well_coordinate(self, coord_w):
        # Unify the input parameter type.
        if isinstance(coord_w, np.ndarray):
            pass
        elif isinstance(coord_w, list):
            coord = np.array(coord_w)
        else:
            raise TypeError("The input coordinate must be a list of np.ndarray")
        # Check the input coord length.
        if len(coord_w) != 2:
            raise ValueError("The input coordinate must have a length of 2.")

        # Set value.
        self._coord_w = coord_w

    def set_well_flow_rate(self, q):
        self._q = q

    def __calc_series_num(self, u):
        if u < 1:
            tmp = self.__a[0] + \
                  u * (self.__a[1] + u * (self.__a[2] + u * (self.__a[3] + u * (self.__a[4] + u * self.__a[5]))))
            return -1 * math.log(u) + tmp
        else:
            tmp_1 = 1 / (u * (math.e**u))
            tmp_2 = self.__b[0] + u * (self.__b[1] + u * (self.__b[2] + u * (self.__b[3] + u)))
            tmp_3 = self.__c[0] + u * (self.__c[1] + u * (self.__c[2] + u * (self.__c[3] + u)))
            return tmp1 * tmp2 / tmp3
