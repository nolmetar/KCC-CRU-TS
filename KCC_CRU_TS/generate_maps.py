#!python3
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cartopy.feature as c_feature
import random
from .koppen import Koppen
import os


class GenerateMaps:
    def __init__(self):
        print("Generate Maps: init")
        self.ko = Koppen()

    def generate_map_climates(self, out_dir, year, props: list):
        print("Generate Maps: starting map climates generation")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        path = out_dir + "climate" + "-" + str(year) + ".jpg"

        fig = plt.figure(figsize=(16, 12))
        chart = fig.add_subplot(projection=ccrs.PlateCarree())
        chart.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
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
        print("Generate Maps: finished map {} generation".format(path))

    @staticmethod
    def generate_map_temp(out_dir, year, props: list):
        print("Generate Maps: starting map temp generation")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        path = out_dir + "temp" + "-" + str(year) + ".jpg"

        fig = plt.figure(figsize=(16, 12))
        chart = fig.add_subplot(projection=ccrs.PlateCarree())
        chart.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
        chart.add_feature(c_feature.COASTLINE)

        for prop in props:
            lat = -90 + (prop["l"]/2)
            lon = -180 + (prop["o"]/2)
            r = str(hex(255)).replace("0x", "")
            scale = prop["p"]+60
            if scale/10 < 10:
                mod = 3
            elif scale/10 < 20:
                mod = 4.5
            elif scale/10 < 30:
                mod = 6.75
            elif scale/10 < 40:
                mod = 10.125
            elif scale/10 < 50:
                mod = 15.1875
            elif scale/10 < 60:
                mod = 22.7812
            elif scale/10 < 70:
                mod = 34.1718
            elif scale/10 < 80:
                mod = 51.2578
            elif scale/10 < 90:
                mod = 76.8867
            elif scale/10 < 100:
                mod = 115.3300
            elif scale/10 < 110:
                mod = 172.9951
            elif scale/10 < 120:
                mod = 259.4926
            else:
                mod = 259.4926
            c = 255-(((scale*mod)/31139)*255)
            # g = str(hex(int((1-((prop["p"]+60)/120))*255))).replace("0x", "")
            g = str(hex(int(c))).replace("0x", "")
            b = str(hex(int(c))).replace("0x", "")
            color = "#" + r + g + b
            # print(color)
            patch = Rectangle((lon, lat), 0.5, 0.5)
            patch.set_facecolor(color)
            patch.set_alpha(0.9)
            chart.add_patch(patch)

        chart.add_feature(c_feature.BORDERS, linestyle='-', linewidth=0.5)
        plt.savefig(path, bbox_inches='tight')
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
