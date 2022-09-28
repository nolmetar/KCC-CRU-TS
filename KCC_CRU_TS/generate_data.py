#!python3
from datetime import datetime
import random

from .io_interface import IOInterface
from .compute import Compute
from .koppen import Koppen
from .generate_maps import GenerateMaps

DATA = {
    "tmp": "DATA/cru_ts4.06.1901.2021.tmp.dat.nc",
    "pre": "DATA/cru_ts4.06.1901.2021.pre.dat.nc",
    "cld": "DATA/cru_ts4.06.01.1901.2021.cld.dat.nc",
    "tmn": "DATA/cru_ts4.06.1901.2021.tmn.dat.nc",
    "tmx": "DATA/cru_ts4.06.1901.2021.tmx.dat.nc",
    "vap": "DATA/cru_ts4.06.1901.2021.vap.dat.nc",
    "wet": "DATA/cru_ts4.06.1901.2021.wet.dat.nc",
    "frs": "DATA/cru_ts4.06.1901.2021.frs.dat.nc"
}
# Cloud: Collection params
OUTPUT_DIR_JSON_PARAM = "OUTPUT/JSON-PARAMS/"
# Cloud: Collection data
# One collection per year or one coll per data ?
# Every variable
OUTPUT_DIR_JSON_DATA = "OUTPUT/JSON-DATA/"
OUTPUT_DIR_MAPS = "OUTPUT/MAPS/"


class GenerateData:
    def __init__(self):
        print("Generate Data: init")
        self.io = IOInterface()
        self.co = Compute()
        self.ko = Koppen()
        self.gm = GenerateMaps()
        self.gm.tests()

    # TODO main loop goes here
    def generate_data(self, preview: bool, cloud: bool):
        print("Generate Data: Starting data generation")
        self.io.check_const(DATA)
        self.io.import_data_const(DATA)

        self.__generate_parameters(preview, cloud)

        self.__generate_climates(preview, cloud)
        self.__generate_min_temperatures(preview, cloud)
        self.__generate_avg_temperatures(preview, cloud)
        self.__generate_max_temperatures(preview, cloud)
        self.__generate_precipitation(preview, cloud)
        self.__generate_min_wet_bulb(preview, cloud)
        self.__generate_avg_wet_bulb(preview, cloud)
        self.__generate_max_wet_bulb(preview, cloud)
        self.__generate_cloud_cover(preview, cloud)
        self.__generate_wet_days(preview, cloud)
        self.__generate_frost_days(preview, cloud)

        print("Generate Data: Finished data generation")

    # { "type":"time", "data":[2021, 2020, 2019, ...] }
    # { "type":"area", "data":{ area id, real lat lon, rectangle } }
    # { "type":"koppen", "data":{ code name, class/full name, colors } }
    def __generate_parameters(self, preview: bool, cloud: bool):
        print("Generate Data: Starting parameters generation")

        print("Generate Data: Finished parameters generation")

    # TODO one funct for each data: climate, temp, pre, wet bulb, etc
    def __generate_climates(self, preview: bool, cloud: bool):
        print("Generate Data: Starting climate generation")
        self.io.check_data(DATA, ["tmp", "pre"])
        self.io.import_data(DATA, ["tmp", "pre"])

        lat_len = self.io.get_lat_len()
        lon_len = self.io.get_lon_len()
        if preview:
            years = [2021]
        else:
            years = self.io.get_years()
        for year in years:
            print("Generate Data: Generating climates {0:.2f}%".format((years.index(year) / len(years)) * 100))
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
            print(len(data_output))
            for i in range(0, 20):
                rand_int = random.randint(0, 259199)
                print(data_output[rand_int])
        self.io.reset_data()
        print("Generate Data: Finished climate generation")

    def __generate_min_temperatures(self, preview: bool, cloud: bool):
        print("Generate Data: Starting min temp generation")
        self.io.check_data(DATA, ["tmn"])
        self.io.import_data(DATA, ["tmn"])

        self.io.reset_data()
        print("Generate Data: Finished min temp generation")

    def __generate_avg_temperatures(self, preview: bool, cloud: bool):
        print("Generate Data: Starting avg temp generation")
        self.io.check_data(DATA, ["tmp"])
        self.io.import_data(DATA, ["tmp"])

        self.io.reset_data()
        print("Generate Data: Finished avg temp generation")

    def __generate_max_temperatures(self, preview: bool, cloud: bool):
        print("Generate Data: Starting max temp generation")
        self.io.check_data(DATA, ["tmx"])
        self.io.import_data(DATA, ["tmx"])

        self.io.reset_data()
        print("Generate Data: Finished max temp generation")

    def __generate_precipitation(self, preview: bool, cloud: bool):
        print("Generate Data: Starting precipitation generation")
        self.io.check_data(DATA, ["pre"])
        self.io.import_data(DATA, ["pre"])

        self.io.reset_data()
        print("Generate Data: Finished precipitation generation")

    def __generate_min_wet_bulb(self, preview: bool, cloud: bool):
        print("Generate Data: Starting min wet bulb generation")
        self.io.check_data(DATA, ["tmn", "vap"])
        self.io.import_data(DATA, ["tmn", "vap"])

        self.io.reset_data()
        print("Generate Data: Finished min wet bulb generation")

    def __generate_avg_wet_bulb(self, preview: bool, cloud: bool):
        print("Generate Data: Starting avg wet bulb generation")
        self.io.check_data(DATA, ["tmp", "vap"])
        self.io.import_data(DATA, ["tmp", "vap"])

        self.io.reset_data()
        print("Generate Data: Finished avg wet bulb generation")

    def __generate_max_wet_bulb(self, preview: bool, cloud: bool):
        print("Generate Data: Starting max wet bulb generation")
        self.io.check_data(DATA, ["tmx", "vap"])
        self.io.import_data(DATA, ["tmx", "vap"])

        self.io.reset_data()
        print("Generate Data: Finished max wet bulb generation")

    def __generate_cloud_cover(self, preview: bool, cloud: bool):
        print("Generate Data: Starting cloud cover generation")
        self.io.check_data(DATA, ["cld"])
        self.io.import_data(DATA, ["cld"])

        self.io.reset_data()
        print("Generate Data: Finished cloud cover generation")

    def __generate_wet_days(self, preview: bool, cloud: bool):
        print("Generate Data: Starting wet days generation")
        self.io.check_data(DATA, ["wet"])
        self.io.import_data(DATA, ["wet"])

        self.io.reset_data()
        print("Generate Data: Finished wet days generation")

    def __generate_frost_days(self, preview: bool, cloud: bool):
        print("Generate Data: Starting frost days generation")
        self.io.check_data(DATA, ["frs"])
        self.io.import_data(DATA, ["frs"])

        self.io.reset_data()
        print("Generate Data: Finished frost days generation")
