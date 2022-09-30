#!python3
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

    def compute_wet_bulb(self, temp_c, pres):
        # calculate relative humidity
        temp_k = self.co.c_to_k(temp_c)
        coefficient_a = 0
        coefficient_b = 0
        coefficient_c = 0
        if 255.9 <= temp_k < 273:
            coefficient_a = self.COEFFICIENTS["255.9-272.0"][0]
            coefficient_b = self.COEFFICIENTS["255.9-272.0"][1]
            coefficient_c = self.COEFFICIENTS["255.9-272.0"][2]
        vap_pres_log = coefficient_a - (coefficient_b/(temp_k + coefficient_c))
        vap_pres = 10 ** vap_pres_log
        print(vap_pres)
        # calculate wet bulb

    @staticmethod
    def tests():
        print("Wet bulb: tests")
