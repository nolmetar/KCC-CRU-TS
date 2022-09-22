#!python3
import numpy as np
from datetime import datetime, timedelta
import sys


class Compute:
    def __init__(self):
        print("Compute: init")

    @staticmethod
    def gen_shape(lat: float, lon: float):
        shape = list()
        shape.append([lat - 0.25, lon - 0.25])
        shape.append([lat + 0.25, lon - 0.25])
        shape.append([lat + 0.25, lon + 0.25])
        shape.append([lat - 0.25, lon + 0.25])
        shape.append([lat - 0.25, lon - 0.25])
        return shape

    @staticmethod
    def c_to_f(celsius: float) -> float:
        return (celsius * (9/5)) + 32

    @staticmethod
    def f_to_c(fahrenheit: float) -> float:
        return (fahrenheit - 32) * (5/9)

    @staticmethod
    def c_to_k(celsius: float) -> float:
        return celsius + 273.15

    @staticmethod
    def k_to_c(kelvin: float) -> float:
        return kelvin - 273.15

    def tests(self):
        print("Compute: tests")
        print(self.c_to_f(15))
        print(self.f_to_c(100))
        print(self.c_to_k(15))
        print(self.k_to_c(320))
