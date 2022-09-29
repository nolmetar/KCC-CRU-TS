#!python3
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import cartopy.feature as c_feature
import random
from .koppen import Koppen
import os

class GenerateMaps:
    def __init__(self):
        print("Generate Maps: init")
        self.ko = Koppen()

    def generate_map(self, out_dir, name, year, props: list):
        print("Generate Maps: starting map {} generation".format(name))
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        path = out_dir + name + "-" + str(year) + ".jpg"

        fig = plt.figure(figsize=(16, 12))
        chart = fig.add_subplot(projection=ccrs.PlateCarree())

        chart.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
        # chart.add_feature(c_feature.LAND)
        # chart.add_feature(c_feature.OCEAN)
        chart.add_feature(c_feature.COASTLINE)

        for prop in props:
            lat = -90 + (prop["l"]/2)
            lon = -180 + (prop["o"]/2)
            symbol = self.ko.get_index_rev(prop["p"])
            color = self.ko.get_color(symbol)
            patch = Rectangle((lon, lat), 0.5, 0.5)
            patch.set_facecolor(color)
            patch.set_alpha(0.9)
            chart.add_patch(patch)

        chart.add_feature(c_feature.BORDERS, linestyle='-', linewidth=0.5)

        plt.savefig(path, bbox_inches='tight')

        print("Generate Maps: finished map {} generation".format(name))

    # TODO figure out how to generate rectangles on map ...
    @staticmethod
    def tests():
        print("Generate Maps: tests")

        fig = plt.figure(figsize=(16, 12))
        chart = fig.add_subplot(projection=ccrs.PlateCarree())

        chart.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
        chart.add_feature(c_feature.LAND)
        chart.add_feature(c_feature.OCEAN)
        chart.add_feature(c_feature.COASTLINE)
        # chart.add_feature(c_feature.BORDERS, linestyle='-', linewidth=0.5)

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
