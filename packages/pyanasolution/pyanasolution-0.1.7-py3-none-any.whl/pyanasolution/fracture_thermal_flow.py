import math
import numpy as np
from ._solution_base import SolutionBase


class FractureThermalFlow(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._lambda_m = 0
        self._add_param_info("Matrix conductivity", "W/(m∙k)", "_lambda_m", "float", "Matrix means pure rock matrix.")
        self._rho_m = 0
        self._add_param_info("Matrix density", "kg/m^3", "_rho_m", "float")
        self._cp_m = 0
        self._add_param_info("Matrix specific heat capacity", "J/(Kg∙K)", "_cp_m", "float")
        self._rho_f = 0
        self._add_param_info("Fluid density", "kg/m^3", "_rho_f", "float")
        self._cp_f = 0
        self._add_param_info("Fluid specific heat capacity", "J/(Kg∙K)", "_cp_f", "float")
        self._b = 1
        self._add_param_info("Fracture width", "m", "_b", "float")
        self._t_init = 0
        self._add_param_info("Initial temperature", "°C", "_t_init", "float")
        self._t_inject = 0
        self._add_param_info("Injection temperature", "°C", "_t_inject", "float")
        self._t = 0
        self._add_param_info("Operation time", "s", "_t", "float")
        self._u = 0
        self._add_param_info("Injection velocity", "m/s", "_u", "float")

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

        # Calculate the Complementary error function.
        coe_0 = (self._lambda_m * coord[0]) / (self._rho_f * self._cp_f * self._b)
        coe_1 = (self._lambda_m * self._u * (self._u * self._t - coord[0])) / (self._rho_m * self._cp_m)
        value = math.erfc(coe_0 / (2 * math.sqrt(coe_1)))

        # Calculate the Unit step function.
        U = 1 if (self._t - coord[0] / self._u) > 0 else 0

        # Calculation
        return self._t_init + (self._t_inject - self._t_init)*value*U

    def doc(self):
        print("[PyAnaSolution - FractureThermalFlow]")
        print(" * Cold fluid reinjected into a hot matrix through the fracture with constant width in a 2D computational domain.")
        print("[Parameters]")
        self.print_param_info()

    def set_matrix_conductivity(self, lambda_m):
        self._lambda_m = lambda_m

    def set_matrix_density(self, rho_m):
        self._rho_m = rho_m

    def set_matrix_specific_heat_capacity(self, cp_m):
        self._cp_m = cp_m

    def set_fluid_density(self, rho_f):
        self._rho_f = rho_f

    def set_fluid_specific_heat_capacity(self, cp_f):
        self._cp_f = cp_f

    def set_fracture_width(self, b):
        self._b = b

    def set_initial_temperature(self, t_init):
        self._t_init = t_init

    def set_injection_temperature(self, t_inject):
        self._t_inject = t_inject

    def set_operation_time(self, t):
        self._t = t

    def set_injection_velocity(self, u):
        self._u = u
