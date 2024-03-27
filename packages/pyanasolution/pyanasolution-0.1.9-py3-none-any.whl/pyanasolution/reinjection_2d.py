import math
import numpy as np
from ._solution_base import SolutionBase


class Reinjection2D(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._lambda_a = 0
        self._add_param_info("Aquifer conductivity", "W/(m∙k)", "_lambda_a", "float",
                             "The aquifer signifies the fluid-solid mixture.")
        self._rho_a = 0
        self._add_param_info("Aquifer density", "kg/m^3", "_rho_a", "float")
        self._cp_a = 0
        self._add_param_info("Aquifer specific heat capacity", "J/(Kg∙K)", "_cp_a", "float")
        self._b = 1
        self._add_param_info("Aquifer thick", "m", "_b", "float")
        self._rho_f = 1000
        self._add_param_info("Fluid density", "kg/m^3", "_rho_f", "float")
        self._cp_f = 4185
        self._add_param_info("Fluid specific heat capacity", "J/(Kg∙K)", "_cp_f", "float")
        self._t_init = 0
        self._add_param_info("Initial temperature", "°C", "_t_init", "float")
        self._t_inject = 0
        self._add_param_info("Injection temperature", "°C", "_t_inject", "float")
        self._t = 0
        self._add_param_info("Operation time", "s", "_t", "float")
        self._q = 0
        self._add_param_info("Well flow rate", "kg/s", "_q", "float", "It must be positive for injection.")

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

        # Calculate the volumetric flow rate.
        q = self._q / self._rho_f
        # Calculate temporary variables.
        nu = q * self._rho_f * self._cp_f / (4 * math.pi * self._b * self._lambda_a)
        tau = 4 * self._lambda_a * self._t / (self._rho_a * self._cp_a * self._b * self._b)

        # Calculation.
        try:
            # Calculate the radius.
            r = np.linalg.norm(coord)

            # Calculate the given result.
            omega = 2 * r / self._b
            tmp = math.gamma(nu) - self.__gamma_inc(nu, omega**2 / (4 * tau))
            tmp /= math.gamma(nu)

            # Calculate the check result.
            omega_check = 2 * (r + 1) / self._b
            tmp_check = math.gamma(nu) - self.__gamma_inc(nu, omega_check**2 / (4 * tau))
            tmp_check /= math.gamma(nu)

            # Check the value.
            if tmp_check - tmp >= 0:
                return self._t_init
            else:
                return tmp*(self._t_inject - self._t_init) + self._t_init
        except OverflowError:
            return self._t_init

    def doc(self):
        print("[PyAnaSolution - Reinjection 2D]")
        print(" * Cold fluid reinjected into a hot aquifer through a single well in a 2D computational domain.")
        print("[Parameters]")
        self.print_param_info()

    def set_aquifer_conductivity(self, lambda_a):
        self._lambda_a = lambda_a

    def set_aquifer_density(self, rho_a):
        self._rho_a = rho_a

    def set_aquifer_specific_heat_capacity(self, cp_a):
        self._cp_a = cp_a

    def set_aquifer_thick(self, b):
        self._b = b

    def set_fluid_density(self, rho_f):
        self._rho_f = rho_f

    def set_fluid_specific_heat_capacity(self, cp_f):
        self._cp_f = cp_f

    def set_initial_temperature(self, t_init):
        self._t_init = t_init

    def set_injection_temperature(self, t_inject):
        self._t_inject = t_inject

    def set_operation_time(self, t):
        self._t = t

    def set_well_flow_rate(self, q):
        self._q = q

    def __gamma_inc(self, s, x):
        iterations = 120
        sum = 0
        for i in range(iterations):
            math.pow(x, i)
            sum += math.pow(x, i) / math.gamma(s + i + 1)

        return math.pow(x, s) * math.gamma(s) * math.exp(-x) * sum
