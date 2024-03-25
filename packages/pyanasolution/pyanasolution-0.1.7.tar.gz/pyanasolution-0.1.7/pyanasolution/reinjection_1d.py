import math
from ._solution_base import SolutionBase


class Reinjection1D(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._lambda_a = 20
        self._add_param_info("Aquifer conductivity", "W/(m∙k)", "_lambda_a", "float",
                             "The aquifer signifies the fluid-solid mixture.")
        self._q = 0
        self._add_param_info("Well flow rate", "kg/s", "_q", "float", "It must be positive for injection.")
        self._rho_a = 0
        self._add_param_info("Aquifer density", "kg/m^3", "_rho_a", "float")
        self._cp_a = 0
        self._add_param_info("Aquifer specific heat capacity", "J/(Kg∙K)", "_cp_a", "float")
        self._cp_f = 0
        self._add_param_info("Fluid specific heat capacity", "J/(Kg∙K)", "_cp_f", "float")
        self._rho_f = 0
        self._add_param_info("Fluid density", "kg/m^3", "_rho_f", "float")
        self._t_inject = 0
        self._add_param_info("Injection temperature", "°C", "_t_inject", "float")
        self._t_init = 0
        self._add_param_info("Initial temperature", "°C", "_t_init", "float")
        self._v = 0
        self._add_param_info("Velocity", "m/s", "_v", "float")
        self._t = 0
        self._add_param_info("Time", "s", "_t", "float")

    def calc(self, coord):
        unify_v = self._v * self._rho_f * self._cp_f / (self._rho_a * self._cp_a)
        unify_d = self._lambda_a / (self._rho_a * self._cp_a)

        result = 0.0
        try:
            tmp_1 = math.exp(unify_v * coord / unify_d)
        except OverflowError:
            tmp_1 = 0
        tmp_2 = math.erfc((coord + unify_v*self._t)/math.sqrt(4*unify_d*self._t))
        if math.isinf(tmp_1) and tmp_2 == 0:
            result += 0
        else:
            result += tmp_1 * tmp_2
        result += math.erfc((coord - unify_v*self._t)/math.sqrt(4*unify_d*self._t))
        result *= 0.5*(self._t_inject - self._t_init)
        result += self._t_init

        return result

    def doc(self):
        print("[PyAnaSolution - Reinjection 1D]")
        print(" * -")
        print("[Parameters]")
        self.print_param_info()

    def set_aquifer_conductivity(self, lambda_a):
        self._lambda_a = lambda_a

    def set_aquifer_density(self, rho_a):
        self._rho_a = rho_a

    def set_aquifer_specific_heat_capacity(self, cp_a):
        self._cp_a = cp_a

    def set_fluid_density(self, rho_f):
        self._rho_f = rho_f

    def set_fluid_specific_heat_capacity(self, cp_f):
        self._cp_f = cp_f

    def set_initial_temperature(self, t_init):
        self._t_init = t_init

    def set_injection_temperature(self, t_inject):
        self._t_inject = t_inject

    def set_time(self, t):
        self._t = t

    def set_velocity(self, v):
        self._v = v
