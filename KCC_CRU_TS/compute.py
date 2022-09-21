#!python3
import numpy as np
from datetime import datetime, timedelta
import sys


class Compute:
    def __init__(self):
        print("Compute: init")

    # TODO adapt for 5 points (A B C D A) to draw shape
    @staticmethod
    def gen_shape(lat: float, lon: float):
        shape = list()
        shape.append([lat - 0.25, lon - 0.25])
        shape.append([lat + 0.25, lon - 0.25])
        shape.append([lat + 0.25, lon + 0.25])
        shape.append([lat - 0.25, lon + 0.25])
        return shape

    @staticmethod
    def tests():
        print("Compute: tests")