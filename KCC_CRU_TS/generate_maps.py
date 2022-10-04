#!python3
import os
import random
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
        chart.set_title(str(year) + " " + name)
        plt.savefig(path, bbox_inches='tight')
        plt.close(fig)
        del fig
        print("Generate Maps: finished map {} generation".format(path))

    @staticmethod
    def generate_map_scale(out_dir, name, name_type, year, props: list, map_type, min_val, max_val):
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
                scale = (prop["p"] / max_val)
                scale = 1 if scale > 1 else scale
                scale = round(scale, 1)
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
        chart.set_title(str(year) + " " + name)
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
