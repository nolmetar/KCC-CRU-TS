#!python3
from math import atan

from .compute import Compute


class WetBulb:
    def __init__(self):
        print("Wet Bulb: init")
        self.co = Compute()
        self.COEFFICIENTS = {
            "255.9-272.0": [4.6543, 1435.264, -64.848],
            "273.0-303.0": [5.40221, 1838.675, -31.737],
            "304.0-333.0": [5.20389, 1733.926, -39.485],
            "334.0-363.0": [5.0768, 1659.793, -45.854]
        }

    def compute_wet_bulb_a(self, temperatures: list, pressures: list):
        wet_bulb_a = list()
        for i in range(0, len(temperatures)):
            wet_bulb_a.append(self.compute_wet_bulb(temperatures[i], pressures[i]))
        return wet_bulb_a

    def compute_wet_bulb(self, temp_c, pres_hpa):
        # calculate relative humidity
        temp_k = self.co.c_to_k(temp_c)
        vap_pres_hpa = self.__antoine_equation(temp_k)
        # calculate relative humidity
        rel_hum_per = pres_hpa / vap_pres_hpa
        # calculate wet bulb
        wet_bulb_c = self.__wet_bulb_equation(temp_c, rel_hum_per)
        return wet_bulb_c

    def __antoine_equation(self, temp_k):
        coefficient_a = 0
        coefficient_b = 0
        coefficient_c = 0
        if 255.9 <= temp_k < 273.0:
            coefficient_a = self.COEFFICIENTS["255.9-272.0"][0]
            coefficient_b = self.COEFFICIENTS["255.9-272.0"][1]
            coefficient_c = self.COEFFICIENTS["255.9-272.0"][2]
        elif 273.0 <= temp_k < 304.0:
            coefficient_a = self.COEFFICIENTS["273.0-303.0"][0]
            coefficient_b = self.COEFFICIENTS["273.0-303.0"][1]
            coefficient_c = self.COEFFICIENTS["273.0-303.0"][2]
        elif 304.0 <= temp_k < 334.0:
            coefficient_a = self.COEFFICIENTS["304.0-333.0"][0]
            coefficient_b = self.COEFFICIENTS["304.0-333.0"][1]
            coefficient_c = self.COEFFICIENTS["304.0-333.0"][2]
        elif 334.0 <= temp_k < 364.0:
            coefficient_a = self.COEFFICIENTS["334.0-363.0"][0]
            coefficient_b = self.COEFFICIENTS["334.0-363.0"][1]
            coefficient_c = self.COEFFICIENTS["334.0-363.0"][2]
        vap_pres_log = coefficient_a - (coefficient_b / (temp_k + coefficient_c))
        vap_pres_hpa = (10 ** vap_pres_log) * 1000
        return vap_pres_hpa

    @staticmethod
    def __wet_bulb_equation(temp, rel_hum_per):
        rel_hum = rel_hum_per * 100
        wet_bulb = temp * atan(0.151977 * ((rel_hum + 8.313659) ** 0.5))
        wet_bulb = wet_bulb + atan(temp + rel_hum) - atan(rel_hum - 1.676331)
        wet_bulb = wet_bulb + (0.00391838 * (rel_hum ** (3 / 2)) * atan(0.023101 * rel_hum))
        wet_bulb = wet_bulb - 4.686035
        return wet_bulb

    def tests(self):
        print("Wet bulb: tests")
        print(self.compute_wet_bulb(temp_c=15, pres_hpa=50))
        print(self.__wet_bulb_equation(20, 0.5))
