#!python3
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class GenerateMaps:
    def __init__(self):
        print("Generate Maps: init")

    # TODO figure out how to generate rectangles on map ...
    @staticmethod
    def tests():
        print("test")

        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()

        ny_lon, ny_lat = -75, 43
        delhi_lon, delhi_lat = 77.23, 28.61

        plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
                 color='gray', linestyle='--',
                 transform=ccrs.PlateCarree(),
                 )

        # plt.plot([-16.5, -16.0, -16.0, -16.5, -16.5], [-44.0, -44.0, -43.5, -43.5, -44.0],
        #         transform=ccrs.PlateCarree(),
        # )

        plt.savefig('coastlines.png')

        plt.show()