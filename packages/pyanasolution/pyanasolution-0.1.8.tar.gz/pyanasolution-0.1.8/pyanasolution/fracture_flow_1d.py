import math
import numpy as np
from ._solution_base import SolutionBase


class FractureFlow1D(SolutionBase):
    def __init__(self):
        super().__init__()

        # Settable parameters.
        self._length = 0
        self._add_param_info("Fracture length", "m", "_length", "float")
        self._b = 1
        self._add_param_info("Fracture width", "m", "_b", "float")
        self._k = 0
        self._add_param_info("Fracture permeability", "m^2", "_k", "float")
        self._niu = 0
        self._add_param_info("Fluid viscosity", "Pa.s", "_niu", "float")
        self._p_init = 0
        self._add_param_info("Initial Pressure", "Pa", "_p_init", "float")
        self._p_inlet = 0
        self._add_param_info("Inlet Pressure", "Pa", "_p_inlet", "float")
        self._p_outlet = 0
        self._add_param_info("Outlet Pressure", "Pa", "_p_outlet", "float")

    def calc(self, coord, t):
        result_0 = 0;
        result_1 = 0;
        coe_0 = (self._k * self._b * self._b) / (12 * self._niu)
        coe_1 = self._p_outlet - self._p_inlet
        coe_2 = self._p_init - self._p_inlet

        for j in range(1, 10):
            if j % 2 == 0:
                coe_3 = j * math.pi / self._length
                result_0 += 1 * math.exp(-coe_0 * t * coe_3 * coe_3) * math.sin(coe_3 * coord) / j;
            elif j % 2 != 0:
                coe_3 = j * math.pi / self._length
                result_1 += 1 * math.exp(-coe_0 * t * coe_3 * coe_3) * math.sin(coe_3 * coord) / j;

        return (self._p_inlet + coe_2 * ((coe_1 / coe_2) * (coord / self._length - 2 * result_0 / math.pi)
                                         + 2 * (2 - (coe_1 / coe_2)) * result_1 / math.pi)) / 1e+6;

    def doc(self):
        print("[PyAnaSolution - FractureFlow 1D]")
        print(" * -")
        print("[Parameters]")
        self.print_param_info()

    def set_fracture_length(self, length):
        self._length = length

    def set_fracture_width(self, width):
        self._b = width

    def set_fracture_permeability(self, permeability):
        self._k = permeability

    def set_fluid_viscosity(self,viscosity):
        self._niu = viscosity

    def set_initial_pressure(self, p_init):
        self._p_init = p_init

    def set_inlet_pressure(self, p_inlet):
        self._p_inlet = p_inlet

    def set_outlet_pressure(self, p_outlet):
        self._p_outlet = p_outlet
