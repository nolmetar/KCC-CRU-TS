#!python3
import random

from .io_interface import IOInterface
from .compute import Compute
from .koppen import Koppen
from .generate_maps import GenerateMaps
from .wet_bulb import WetBulb

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

DATA_TO_GEN = {
    "climate": ["tmp", "pre"],
    "min temp": ["tmn"]
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
        self.wb = WetBulb()

    # TODO main loop goes here
    def generate_data(self, preview: bool, cloud: bool):
        print("Generate Data: Starting data generation")
        self.io.check_const(DATA)
        self.io.import_data_const(DATA)

        lat_len = self.io.get_lat_len()
        lon_len = self.io.get_lon_len()
        if preview:
            years = [2021]
        else:
            years = self.io.get_years()

        self.__generate_parameters(cloud, lat_len, lon_len, years)
        self.__generate_climates(cloud, lat_len, lon_len, years)
        self.__generate_min_temperatures(cloud, lat_len, lon_len, years)
        self.__generate_avg_temperatures(cloud, lat_len, lon_len, years)
        self.__generate_max_temperatures(cloud, lat_len, lon_len, years)
        self.__generate_precipitation(cloud, lat_len, lon_len, years)
        self.__generate_min_wet_bulb(cloud, lat_len, lon_len, years)
        self.__generate_avg_wet_bulb(cloud, lat_len, lon_len, years)
        self.__generate_max_wet_bulb(cloud, lat_len, lon_len, years)
        self.__generate_cloud_cover(cloud, lat_len, lon_len, years)
        self.__generate_wet_days(cloud, lat_len, lon_len, years)
        self.__generate_frost_days(cloud, lat_len, lon_len, years)

        print("Generate Data: Finished data generation")

    # { "type":"time", "data":[2021, 2020, 2019, ...] }
    # { "type":"area", "data":{ area id, real lat lon, rectangle } }
    # { "type":"koppen", "data":{ code name, class/full name, colors } }
    def __generate_parameters(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting parameters generation")

        for year in years:
            print("Generate Data: Generating parameters {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    real_lat = float(self.io.get_lat(lat))
                    real_lon = float(self.io.get_lon(lon))

        print("Generate Data: Finished parameters generation")

    # TODO one funct for each data: climate, temp, pre, wet bulb, etc
    def __generate_climates(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting climate generation")
        self.io.check_data(DATA, ["tmp", "pre"])
        self.io.import_data(DATA, ["tmp", "pre"])

        for year in years:
            print("Generate Data: Generating climates {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    real_lat = float(self.io.get_lat(lat))
                    year_data_tmp = self.io.get_year_data("tmp", year, lat, lon)
                    year_data_pre = self.io.get_year_data("pre", year, lat, lon)
                    if len(year_data_tmp) != 0 and len(year_data_pre) != 0:
                        data_lat_lon = dict()
                        symbols = self.ko.compute_symbols(year_data_tmp, year_data_pre, real_lat)
                        data_lat_lon["l"] = lat
                        data_lat_lon["o"] = lon
                        data_lat_lon["p"] = self.ko.get_index(symbols)
                        data_output.append(data_lat_lon)
                        del data_lat_lon
            self.gm.generate_map(OUTPUT_DIR_MAPS, "climate", year, data_output)
            if cloud:
                self.io.export_data_cloud(data_output)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "climate", 1, year, data_output)
            del data_output

        self.io.reset_data()
        print("Generate Data: Finished climate generation")

    def __generate_min_temperatures(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting min temp generation")
        self.io.check_data(DATA, ["tmn"])
        self.io.import_data(DATA, ["tmn"])

        for year in years:
            print("Generate Data: Generating min temp {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmn = self.io.get_year_data("tmn", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished min temp generation")

    def __generate_avg_temperatures(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting avg temp generation")
        self.io.check_data(DATA, ["tmp"])
        self.io.import_data(DATA, ["tmp"])

        for year in years:
            print("Generate Data: Generating avg temp {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmp = self.io.get_year_data("tmp", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished avg temp generation")

    def __generate_max_temperatures(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting max temp generation")
        self.io.check_data(DATA, ["tmx"])
        self.io.import_data(DATA, ["tmx"])

        for year in years:
            print("Generate Data: Generating max temp {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmx = self.io.get_year_data("tmx", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished max temp generation")

    def __generate_precipitation(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting precipitation generation")
        self.io.check_data(DATA, ["pre"])
        self.io.import_data(DATA, ["pre"])

        for year in years:
            print("Generate Data: Generating precipitation {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_pre = self.io.get_year_data("pre", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished precipitation generation")

    def __generate_min_wet_bulb(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting min wet bulb generation")
        self.io.check_data(DATA, ["tmn", "vap"])
        self.io.import_data(DATA, ["tmn", "vap"])

        for year in years:
            print("Generate Data: Generating min wet bulb {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmn = self.io.get_year_data("tmn", year, lat, lon)
                    year_data_vap = self.io.get_year_data("vap", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished min wet bulb generation")

    def __generate_avg_wet_bulb(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting avg wet bulb generation")
        self.io.check_data(DATA, ["tmp", "vap"])
        self.io.import_data(DATA, ["tmp", "vap"])

        for year in years:
            print("Generate Data: Generating avg wet bulb {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmp = self.io.get_year_data("tmp", year, lat, lon)
                    year_data_vap = self.io.get_year_data("vap", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished avg wet bulb generation")

    def __generate_max_wet_bulb(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting max wet bulb generation")
        self.io.check_data(DATA, ["tmx", "vap"])
        self.io.import_data(DATA, ["tmx", "vap"])

        for year in years:
            print("Generate Data: Generating max wet bulb {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmx = self.io.get_year_data("tmx", year, lat, lon)
                    year_data_vap = self.io.get_year_data("vap", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished max wet bulb generation")

    def __generate_cloud_cover(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting cloud cover generation")
        self.io.check_data(DATA, ["cld"])
        self.io.import_data(DATA, ["cld"])

        for year in years:
            print("Generate Data: Generating cloud cover {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_cld = self.io.get_year_data("cld", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished cloud cover generation")

    def __generate_wet_days(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting wet days generation")
        self.io.check_data(DATA, ["wet"])
        self.io.import_data(DATA, ["wet"])

        for year in years:
            print("Generate Data: Generating wet days {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_wet = self.io.get_year_data("wet", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished wet days generation")

    def __generate_frost_days(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting frost days generation")
        self.io.check_data(DATA, ["frs"])
        self.io.import_data(DATA, ["frs"])

        for year in years:
            print("Generate Data: Generating frost days {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_frs = self.io.get_year_data("frs", year, lat, lon)

        self.io.reset_data()
        print("Generate Data: Finished frost days generation")
