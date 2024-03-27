import numpy as np


class SolutionBase:
    def __init__(self):
        # A list used to store parameter information.
        self.__param_info = []

    def print_param_info(self):
        # Calculate the width of each column.
        max_name = max(max(len(item["NAME"]) for item in self.__param_info), 4) + 2
        max_unit = max(max(len(item["UNIT"]) for item in self.__param_info), 4) + 2
        max_value = max(max(len(str(getattr(self, item["VARIABLE"]))) for item in self.__param_info), 7) + 2
        max_type = max(max(len(item["TYPE"]) for item in self.__param_info), 4) + 2
        max_introduction = max(max(len(item["INTRODUCTION"]) for item in self.__param_info), 12) + 2
        prefix = " * "

        # Print a separator line.
        print(prefix + "-"*max_name + "|" + "-"*max_unit + "|" + "-"*max_value + "|" + "-"*max_type + "|" +
              "-"*max_introduction + "|")

        # Print the header line.
        name_head = " PARAMETERS NAME".ljust(max_name)
        unit_head = " UNIT".ljust(max_unit)
        value_head = " VALUE".ljust(max_value)
        type_head = " TYPE".ljust(max_type)
        introduction_head = " INTRODUCTION".ljust(max_introduction)
        print(prefix+f"{name_head}|{unit_head}|{value_head}|{type_head}|{introduction_head}" + "|")

        # Print a separator line.
        print(prefix + "-" * max_name + "|" + "-" * max_unit + "|" + "-" * max_value + "|" + "-" * max_type + "|" +
              "-" * max_introduction + "|")

        # Print parameter lines.
        for item in self.__param_info:
            name = (" " + item["NAME"]).ljust(max_name)
            unit = (" " + item["UNIT"]).ljust(max_unit)
            value = (" " + str(getattr(self, item["VARIABLE"]))).ljust(max_value) # todo: 打印二维np数组的时候会有换行显示问题。
            type = (" " + item["TYPE"]).ljust(max_type)
            introduction = (" " + item["INTRODUCTION"]).ljust(max_introduction)

            print(prefix + f"{name}|{unit}|{value}|{type}|{introduction}" + "|")

        # Print a separator line.
        print(prefix + "-" * max_name + "|" + "-" * max_unit + "|" + "-" * max_value + "|" + "-" * max_type + "|" +
              "-" * max_introduction + "|")

    def _add_param_info(self, name, unit, variable, type, introduction=""):
        self.__param_info.append({"NAME": name,
                                  "UNIT": unit,
                                  "VARIABLE": variable,
                                  "TYPE": type,
                                  "INTRODUCTION": introduction})
