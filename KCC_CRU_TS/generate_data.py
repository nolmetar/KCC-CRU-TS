#!python3
from datetime import datetime

from .io_interface import IOInterface
from .compute import Compute
from .koppen import Koppen

DATA = {
    "tmp": "DATA/cru_ts4.06.1901.2021.tmp.dat.nc",
    "pre": "DATA/cru_ts4.06.1901.2021.pre.dat.nc"
}
OUTPUT_DIR = "OUTPUT"


class GenerateData:
    def __init__(self):
        print("Generate Data: init")
        self.io = IOInterface()
        self.co = Compute()
        self.ko = Koppen()
        # io.check_data(DATA)

    # TODO main loop goes here
    def generate_data(self, preview: bool):
        self.__generate_climates(preview)

    # TODO one funct for each data: climate, temp, pre, wet bulb, etc
    # TODO remove loop
    def __generate_climates(self, preview: bool):
        self.io.import_data(DATA)

        file_name = "Koppen-climates_" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.io.export_data_open(OUTPUT_DIR, file_name)

        print("Generate Data: Starting climate generation")
        lat_len = self.io.get_lat_len()
        lon_len = self.io.get_lon_len()
        if preview:
            years = [2021]
        else:
            years = self.io.get_years()
        for year in years:
            print("Generate Data: Generating {0:.2f}%".format((years.index(year) / len(years)) * 100))
            if not years.index(year) == 0:
                self.io.export_data_comma(OUTPUT_DIR, file_name)
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    real_lat = float(self.io.get_lat(lat))
                    real_lon = float(self.io.get_lon(lon))
                    year_data_tmp = self.io.get_year_data("tmp", year, lat, lon)
                    year_data_pre = self.io.get_year_data("pre", year, lat, lon)
                    data_lat_lon = dict()
                    data_lat_lon["coords"] = dict()
                    data_lat_lon["coords"]["center"] = [real_lat, real_lon]
                    data_lat_lon["coords"]["shape"] = self.co.gen_shape(real_lat, real_lon)
                    data_lat_lon["data"] = dict()
                    if len(year_data_tmp) == 0 or len(year_data_pre) == 0:
                        data_lat_lon["dataValid"] = False
                    else:
                        data_lat_lon["dataValid"] = True
                        symbols = self.ko.compute_symbols(year_data_tmp, year_data_pre, real_lat)
                        data_lat_lon["data"]["symbols"] = "".join(symbols)
                        data_lat_lon["data"]["classname"] = self.ko.get_classname(symbols)
                        data_lat_lon["data"]["fullname"] = self.ko.get_fullname(symbols)
                        data_lat_lon["data"]["color"] = self.ko.get_color(symbols)
                    data_output.append(data_lat_lon)
                # break
            self.io.export_data_save(OUTPUT_DIR, file_name, year, data_output)
            break
        self.io.export_data_close(OUTPUT_DIR, file_name)
        print("Generate Data: Finished generation")


