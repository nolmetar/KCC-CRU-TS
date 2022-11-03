#!python3
import os
import random
import math
import datetime
import cartopy.crs as ccrs
import cartopy.feature as c_feature
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

from .koppen import Koppen


class GenerateMaps:
    def __init__(self):
        print("Generate Maps: init")
        self.ko = Koppen()
        self.map_name = {
            1: "Yearly Köppen climate classification map",
            2: "Yearly minimum of monthly temperature (degrees Celsius)",
            3: "Yearly mean of monthly temperature (degrees Celsius)",
            4: "Yearly maximum of monthly temperature (degrees Celsius)",
            5: "Yearly minimum of monthly precipitation (millimetres per month)",
            6: "Yearly mean of monthly precipitation (millimetres per month)",
            7: "Yearly maximum of monthly precipitation (millimetres per month)",
            8: "Yearly sum precipitation (millimetres per month)",
            9: "Yearly maximum of monthly relative humidity (percentage)",
            10: "Yearly minimum of monthly wet-bulb temperature (degrees Celsius)",
            11: "Yearly mean of monthly relative humidity (percentage)",
            12: "Yearly mean of monthly wet-bulb temperature (degrees Celsius)",
            13: "Yearly minimum of monthly relative humidity (percentage)",
            14: "Yearly maximum of monthly wet-bulb temperature (degrees Celsius)",
            15: "Yearly minimum of monthly cloud cover (percentage)",
            16: "Yearly mean of monthly cloud cover (percentage)",
            17: "Yearly maximum of monthly cloud cover (percentage)",
            18: "Yearly minimum of monthly wet days (days)",
            19: "Yearly mean of monthly wet days (days)",
            20: "Yearly maximum of monthly wet days (days)",
            21: "Yearly sum of monthly wet days (days)",
            22: "Yearly minimum of monthly frost days (days)",
            23: "Yearly mean of monthly frost days (days)",
            24: "Yearly maximum of monthly frost days (days)",
            25: "Yearly sum of monthly frost days (days)"
        }

    def generate_map_climates(self, out_dir, io, name, name_type, year, props: list):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        path = out_dir + str(year) + "-" + str(name_type) + "-" + name + ".jpg"
        print("Generate Maps: starting map {} generation".format(path))

        fig = plt.figure(figsize=(16, 12))
        chart = fig.add_subplot(projection=ccrs.PlateCarree())
        chart.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
        chart.add_feature(c_feature.COASTLINE)

        patches = []
        colors = []
        for prop in props:
            lat = io.get_lat(prop["l"])
            lon = io.get_lon(prop["o"])
            symbols = self.ko.get_symbols(prop["p"])
            color = self.ko.get_color(symbols)
            rectangle = Rectangle((lon, lat), 0.5, 0.5)
            colors.append(color)
            patches.append(rectangle)
        p = PatchCollection(patches, alpha=1, facecolors=colors)
        chart.add_collection(p)
        chart.add_feature(c_feature.BORDERS, linestyle='-', linewidth=0.5)

        now = datetime.datetime.now()
        text = "Legend: See 'Köppen climate classification' on wikipedia, white (no data)"
        text = text + " \nMade by climatle.earth (" + now.strftime("%Y-%m-%d") + ") with " \
                      "data from the Climatic Research Unit (University of East Anglia) and NCAS."
        plt.text(-175, -85, text, fontsize=10, backgroundcolor='white')

        chart.set_title(str(year) + " " + self.map_name[name_type], fontsize=16)
        plt.savefig(path, bbox_inches='tight')
        plt.close(fig)
        del fig
        print("Generate Maps: finished map {} generation".format(path))

    def generate_map_scale(self, out_dir, name, name_type, year, props: list, map_type, min_val, max_val):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        path = out_dir + str(year) + "-" + str(name_type) + "-" + name + ".jpg"
        print("Generate Maps: starting map {} generation".format(path))

        fig = plt.figure(figsize=(16, 12))
        chart = fig.add_subplot(projection=ccrs.PlateCarree())
        chart.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())

        rectangle = Rectangle((-180, -90), 360, 180)
        rectangle.set_facecolor("black")
        rectangle.set_alpha(0.2)
        chart.add_patch(rectangle)

        chart.add_feature(c_feature.COASTLINE)

        patches = []
        colors = []
        log_max_val = math.log2(max_val)
        for prop in props:
            lat = -90 + (prop["l"]/2)
            lon = -180 + (prop["o"]/2)
            r = 1
            g = 1
            b = 1
            if map_type == "rb":
                if prop["p"] < 0:
                    scale = (prop["p"] / min_val)
                    scale = 1 if scale > 1 else scale
                    r = 1 - scale
                    g = 1 - scale
                    b = 1
                else:
                    scale = (prop["p"] / max_val)
                    scale = 1 if scale > 1 else scale
                    r = 1
                    g = 1 - scale
                    b = 1 - scale
            elif map_type == "r":
                scale = (prop["p"] / max_val)
                scale = 1 if scale > 1 else scale
                r = 1
                g = 1 - scale
                b = 1 - scale
            elif map_type == "b":
                scale = (prop["p"] / max_val)
                scale = 1 if scale > 1 else scale
                r = 1 - scale
                g = 1 - scale
                b = 1
            elif map_type == "b2":
                log_val = 0 if prop["p"] <= 1 else math.log2(prop["p"])
                scale = (log_val / log_max_val)
                scale = 1 if scale > 1 else scale
                r = 1 - scale
                g = 1 - scale
                b = 1
            color = (r, g, b)
            rectangle = Rectangle((lon, lat), 0.5, 0.5)
            colors.append(color)
            patches.append(rectangle)
        p = PatchCollection(patches, alpha=1, facecolors=colors)
        chart.add_collection(p)
        chart.add_feature(c_feature.BORDERS, linestyle='-', linewidth=0.5)

        text = ""
        if map_type == "rb":
            text = "Legend (gradient): blue (" + str(min_val) + \
                   ") to white (0), white (0) to red (" + str(max_val) + "), gray (no data)"
        elif map_type == "r":
            text = "Legend (gradient): white (" + str(min_val) + \
                   ") to red (" + str(max_val) + "), gray (no data)"
        elif map_type == "b":
            text = "Legend (gradient): white (" + str(min_val) + \
                   ") to blue (" + str(max_val) + "), gray (no data)"
        elif map_type == "b2":
            text = "Legend (gradient, log): white (" + str(min_val) + \
                   ") to blue (" + str(max_val) + "), gray (no data)"
        now = datetime.datetime.now()
        text = text + " \nMade by climatle.earth (" + now.strftime("%Y-%m-%d") + ") with " \
                      "data from the Climatic Research Unit (University of East Anglia) and NCAS."

        plt.text(-175, -85, text, fontsize=10, backgroundcolor='white')

        chart.set_title(str(year) + " " + self.map_name[name_type], fontsize=16)
        plt.savefig(path, bbox_inches='tight')
        plt.close(fig)
        del fig
        print("Generate Maps: finished map {} generation".format(path))

    @staticmethod
    def tests():
        print("Generate Maps: tests")

        fig = plt.figure(figsize=(16, 12))
        chart = fig.add_subplot(projection=ccrs.PlateCarree())

        chart.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
        chart.add_feature(c_feature.LAND)
        chart.add_feature(c_feature.OCEAN)
        chart.add_feature(c_feature.COASTLINE)
        chart.add_feature(c_feature.BORDERS, linestyle='-', linewidth=0.5)

        chart.scatter(5, 50, color="blue", transform=ccrs.PlateCarree())

        for i in range(-90, 90, 2):
            for j in range(-180, 180, 2):
                color = "#%06x" % random.randint(0, 0xFFFFFF)
                patch = Rectangle((j, i), 2, 2)
                patch.set_facecolor(color)
                patch.set_alpha(1)
                chart.add_patch(patch)

        chart.add_feature(c_feature.BORDERS, linestyle='-', linewidth=0.5)

        plt.savefig('test.jpg', bbox_inches='tight')
        plt.show()
