#!python3

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

        self.__generate_parameters(cloud)
        # self.__generate_climates(cloud, lat_len, lon_len, years)
        # self.__generate_min_temperatures(cloud, lat_len, lon_len, years)
        # self.__generate_avg_temperatures(cloud, lat_len, lon_len, years)
        # self.__generate_max_temperatures(cloud, lat_len, lon_len, years)
        # self.__generate_precipitation(cloud, lat_len, lon_len, years)
        # self.__generate_min_wet_bulb_hum(cloud, lat_len, lon_len, years)
        # self.__generate_avg_wet_bulb_hum(cloud, lat_len, lon_len, years)
        # self.__generate_max_wet_bulb_hum(cloud, lat_len, lon_len, years)
        # self.__generate_cloud_cover(cloud, lat_len, lon_len, years)
        # self.__generate_wet_days(cloud, lat_len, lon_len, years)
        # self.__generate_frost_days(cloud, lat_len, lon_len, years)

        print("Generate Data: Finished data generation")

    @staticmethod
    def __generate_payload(lat, lon, payload: float):
        data = dict()
        data["l"] = lat
        data["o"] = lon
        data["p"] = payload
        return data

    # { "type":"time", "data":[2021, 2020, 2019, ...] }
    # { "type":"area", "data":{ area id, real lat lon, rectangle } }
    # { "type":"koppen", "data":{ code name, class/full name, colors } }
    def __generate_parameters(self, cloud: bool):
        print("Generate Data: Starting parameters generation")

        years = self.io.get_years()
        lat_len = self.io.get_lat_len()
        lon_len = self.io.get_lon_len()
        for lat in range(lat_len):
            for lon in range(lon_len):
                print("")

        if cloud:
            print("cloud")
        else:
            self.io.export_param_json(OUTPUT_DIR_JSON_PARAM, "year", years)

        print("Generate Data: Finished parameters generation")

    # climates per year
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
                        symbols = self.ko.compute_symbols(year_data_tmp, year_data_pre, real_lat)
                        data_lat_lon = self.__generate_payload(lat, lon, self.ko.get_index(symbols))
                        data_output.append(data_lat_lon)
                        del data_lat_lon
            self.gm.generate_map_climates(OUTPUT_DIR_MAPS, self.io, "climate", 1, year, data_output)
            if cloud:
                self.io.export_data_cloud(data_output)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "climate", 1, year, data_output)
            del data_output

        self.io.reset_data()
        print("Generate Data: Finished climate generation")

    # min temp per year
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
                    if len(year_data_tmn) > 0:
                        data_lat_lon = self.__generate_payload(lat, lon, round(min(year_data_tmn), 2))
                        data_output.append(data_lat_lon)
                        del data_lat_lon
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "temperature_min", 2, year, data_output, "rb", -60, 60)
            if cloud:
                self.io.export_data_cloud(data_output)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "temperature_min", 2, year, data_output)
            del data_output

        self.io.reset_data()
        print("Generate Data: Finished min temp generation")

    # avg temp per year
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
                    if len(year_data_tmp) > 0:
                        average = sum(year_data_tmp) / len(year_data_tmp)
                        data_lat_lon = self.__generate_payload(lat, lon, round(average, 2))
                        data_output.append(data_lat_lon)
                        del data_lat_lon
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "temperature_avg", 3, year, data_output, "rb", -60, 60)
            if cloud:
                self.io.export_data_cloud(data_output)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "temperature_avg", 3, year, data_output)
            del data_output

        self.io.reset_data()
        print("Generate Data: Finished avg temp generation")

    # max temp per year
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
                    if len(year_data_tmx) > 0:
                        data_lat_lon = self.__generate_payload(lat, lon, round(max(year_data_tmx), 2))
                        data_output.append(data_lat_lon)
                        del data_lat_lon
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "temperature_max", 4, year, data_output, "rb", -60, 60)
            if cloud:
                self.io.export_data_cloud(data_output)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "temperature_max", 4, year, data_output)
            del data_output

        self.io.reset_data()
        print("Generate Data: Finished max temp generation")

    # min, avg, max, sum precipitations per year
    def __generate_precipitation(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting precipitation generation")
        self.io.check_data(DATA, ["pre"])
        self.io.import_data(DATA, ["pre"])

        for year in years:
            print("Generate Data: Generating precipitation {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output_min = list()
            data_output_avg = list()
            data_output_max = list()
            data_output_sum = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_pre = self.io.get_year_data("pre", year, lat, lon)
                    if len(year_data_pre) > 0:
                        data_lat_lon_min = self.__generate_payload(lat, lon, round(min(year_data_pre), 2))
                        data_output_min.append(data_lat_lon_min)
                        del data_lat_lon_min
                        average = sum(year_data_pre) / len(year_data_pre)
                        data_lat_lon_avg = self.__generate_payload(lat, lon, round(average, 2))
                        data_output_avg.append(data_lat_lon_avg)
                        del data_lat_lon_avg
                        data_lat_lon_max = self.__generate_payload(lat, lon, round(max(year_data_pre), 2))
                        data_output_max.append(data_lat_lon_max)
                        del data_lat_lon_max
                        data_lat_lon_sum = self.__generate_payload(lat, lon, round(sum(year_data_pre), 2))
                        data_output_sum.append(data_lat_lon_sum)
                        del data_lat_lon_sum
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "precipitation_min", 5, year, data_output_min, "b", 0, 400)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "precipitation_avg", 6, year, data_output_avg, "b", 0, 700)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "precipitation_max", 7, year, data_output_max, "b", 0, 3200)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "precipitation_sum", 8, year, data_output_sum, "b", 0, 8500)
            if cloud:
                self.io.export_data_cloud(data_output_min)
                self.io.export_data_cloud(data_output_avg)
                self.io.export_data_cloud(data_output_max)
                self.io.export_data_cloud(data_output_sum)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "precipitation_min", 5, year, data_output_min)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "precipitation_avg", 6, year, data_output_avg)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "precipitation_max", 7, year, data_output_max)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "precipitation_sum", 8, year, data_output_sum)
            del data_output_min
            del data_output_avg
            del data_output_max
            del data_output_sum
        self.io.reset_data()
        print("Generate Data: Finished precipitation generation")

    # min wet bulb & relative humidity per year
    def __generate_min_wet_bulb_hum(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting min wet bulb humidity generation")
        self.io.check_data(DATA, ["tmn", "vap"])
        self.io.import_data(DATA, ["tmn", "vap"])

        for year in years:
            print("Generate Data: Generating min wet bulb humidity {0:.2f}%"
                  .format((years.index(year) / len(years)) * 100))
            data_output_hum = list()
            data_output_wet = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmn = self.io.get_year_data("tmn", year, lat, lon)
                    year_data_vap = self.io.get_year_data("vap", year, lat, lon)
                    if len(year_data_tmn) > 0 and len(year_data_vap) > 0:
                        rel_hum_a, wet_bulb_a = self.wb.compute_wet_bulb_a(year_data_tmn, year_data_vap)
                        if rel_hum_a is not None and wet_bulb_a is not None:
                            data_lat_lon_hum = self.__generate_payload(lat, lon, round(max(rel_hum_a), 2))
                            data_lat_lon_wet = self.__generate_payload(lat, lon, round(min(wet_bulb_a), 2))
                            data_output_hum.append(data_lat_lon_hum)
                            data_output_wet.append(data_lat_lon_wet)
                            del data_lat_lon_hum
                            del data_lat_lon_wet
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "rel_hum_max", 9, year, data_output_hum, "b", 0, 100)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "wet_bulb_min", 10, year, data_output_wet, "rb", -60, 40)
            if cloud:
                self.io.export_data_cloud(data_output_hum)
                self.io.export_data_cloud(data_output_wet)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "rel_hum_max", 9, year, data_output_hum)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "wet_bulb_min", 10, year, data_output_wet)
            del data_output_hum
            del data_output_wet
        self.io.reset_data()
        print("Generate Data: Finished min wet bulb humidity generation")

    # avg wet bulb & relative humidity per year
    def __generate_avg_wet_bulb_hum(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting avg wet bulb humidity generation")
        self.io.check_data(DATA, ["tmp", "vap"])
        self.io.import_data(DATA, ["tmp", "vap"])

        for year in years:
            print("Generate Data: Generating avg wet bulb humidity {0:.2f}%"
                  .format((years.index(year) / len(years)) * 100))
            data_output_hum = list()
            data_output_wet = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmp = self.io.get_year_data("tmp", year, lat, lon)
                    year_data_vap = self.io.get_year_data("vap", year, lat, lon)
                    if len(year_data_tmp) > 0 and len(year_data_vap) > 0:
                        rel_hum_a, wet_bulb_a = self.wb.compute_wet_bulb_a(year_data_tmp, year_data_vap)
                        if rel_hum_a is not None and wet_bulb_a is not None:
                            average_hum = sum(rel_hum_a) / len(rel_hum_a)
                            average_wet = sum(wet_bulb_a) / len(wet_bulb_a)
                            data_lat_lon_hum = self.__generate_payload(lat, lon, round(average_hum, 2))
                            data_lat_lon_wet = self.__generate_payload(lat, lon, round(average_wet, 2))
                            data_output_hum.append(data_lat_lon_hum)
                            data_output_wet.append(data_lat_lon_wet)
                            del data_lat_lon_hum
                            del data_lat_lon_wet
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "rel_hum_avg", 11, year, data_output_hum, "b", 0, 100)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "wet_bulb_avg", 12, year, data_output_wet, "rb", -60, 40)
            if cloud:
                self.io.export_data_cloud(data_output_hum)
                self.io.export_data_cloud(data_output_wet)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "rel_hum_avg", 11, year, data_output_hum)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "wet_bulb_avg", 12, year, data_output_wet)
            del data_output_hum
            del data_output_wet
        self.io.reset_data()
        print("Generate Data: Finished avg wet bulb humidity generation")

    # max wet bulb & relative humidity per year
    def __generate_max_wet_bulb_hum(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting max wet bulb humidity generation")
        self.io.check_data(DATA, ["tmx", "vap"])
        self.io.import_data(DATA, ["tmx", "vap"])

        for year in years:
            print("Generate Data: Generating max wet bulb humidity {0:.2f}%"
                  .format((years.index(year) / len(years)) * 100))
            data_output_hum = list()
            data_output_wet = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_tmx = self.io.get_year_data("tmx", year, lat, lon)
                    year_data_vap = self.io.get_year_data("vap", year, lat, lon)
                    if len(year_data_tmx) > 0 and len(year_data_vap) > 0:
                        rel_hum_a, wet_bulb_a = self.wb.compute_wet_bulb_a(year_data_tmx, year_data_vap)
                        if rel_hum_a is not None and wet_bulb_a is not None:
                            data_lat_lon_hum = self.__generate_payload(lat, lon, round(min(rel_hum_a), 2))
                            data_lat_lon_wet = self.__generate_payload(lat, lon, round(max(wet_bulb_a), 2))
                            data_output_hum.append(data_lat_lon_hum)
                            data_output_wet.append(data_lat_lon_wet)
                            del data_lat_lon_hum
                            del data_lat_lon_wet
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "rel_hum_min", 13, year, data_output_hum, "b", 0, 100)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "wet_bulb_max", 14, year, data_output_wet, "rb", -60, 40)
            if cloud:
                self.io.export_data_cloud(data_output_hum)
                self.io.export_data_cloud(data_output_wet)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "rel_hum_min", 13, year, data_output_hum)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "wet_bulb_max", 14, year, data_output_wet)
            del data_output_hum
            del data_output_wet
        self.io.reset_data()
        print("Generate Data: Finished max wet bulb humidity generation")

    # min, avg, max cloud cover per year
    def __generate_cloud_cover(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting cloud cover generation")
        self.io.check_data(DATA, ["cld"])
        self.io.import_data(DATA, ["cld"])

        for year in years:
            print("Generate Data: Generating cloud cover {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output_min = list()
            data_output_avg = list()
            data_output_max = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_cld = self.io.get_year_data("cld", year, lat, lon)
                    if len(year_data_cld) > 0:
                        data_lat_lon_min = self.__generate_payload(lat, lon, round(min(year_data_cld), 2))
                        data_output_min.append(data_lat_lon_min)
                        del data_lat_lon_min
                        average = sum(year_data_cld) / len(year_data_cld)
                        data_lat_lon_avg = self.__generate_payload(lat, lon, round(average, 2))
                        data_output_avg.append(data_lat_lon_avg)
                        del data_lat_lon_avg
                        data_lat_lon_max = self.__generate_payload(lat, lon, round(max(year_data_cld), 2))
                        data_output_max.append(data_lat_lon_max)
                        del data_lat_lon_max
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "cloud_cover_min", 15, year, data_output_min, "b", 0, 90)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "cloud_cover_avg", 16, year, data_output_avg, "b", 0, 100)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "cloud_cover_max", 17, year, data_output_max, "b", 0, 100)
            if cloud:
                self.io.export_data_cloud(data_output_min)
                self.io.export_data_cloud(data_output_avg)
                self.io.export_data_cloud(data_output_max)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "cloud_cover_min", 15, year, data_output_min)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "cloud_cover_avg", 16, year, data_output_avg)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "cloud_cover_max", 17, year, data_output_max)
            del data_output_min
            del data_output_avg
            del data_output_max
        self.io.reset_data()
        print("Generate Data: Finished cloud cover generation")

    # avg, min, max, sum wet day per year
    def __generate_wet_days(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting wet days generation")
        self.io.check_data(DATA, ["wet"])
        self.io.import_data(DATA, ["wet"])

        for year in years:
            print("Generate Data: Generating wet days {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output_min = list()
            data_output_avg = list()
            data_output_max = list()
            data_output_sum = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_wet = self.io.get_year_data("wet", year, lat, lon)
                    if len(year_data_wet) > 0:
                        data_lat_lon_min = self.__generate_payload(lat, lon, round(min(year_data_wet), 2))
                        data_output_min.append(data_lat_lon_min)
                        del data_lat_lon_min
                        average = sum(year_data_wet) / len(year_data_wet)
                        data_lat_lon_avg = self.__generate_payload(lat, lon, round(average, 2))
                        data_output_avg.append(data_lat_lon_avg)
                        del data_lat_lon_avg
                        data_lat_lon_max = self.__generate_payload(lat, lon, round(max(year_data_wet), 2))
                        data_output_max.append(data_lat_lon_max)
                        del data_lat_lon_max
                        data_lat_lon_sum = self.__generate_payload(lat, lon, round(sum(year_data_wet), 2))
                        data_output_sum.append(data_lat_lon_sum)
                        del data_lat_lon_sum
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "wet_days_min", 18, year, data_output_min, "b", 0, 31)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "wet_days_avg", 19, year, data_output_avg, "b", 0, 31)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "wet_days_max", 20, year, data_output_max, "b", 0, 31)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "wet_days_sum", 21, year, data_output_sum, "b", 0, 365)
            if cloud:
                self.io.export_data_cloud(data_output_min)
                self.io.export_data_cloud(data_output_avg)
                self.io.export_data_cloud(data_output_max)
                self.io.export_data_cloud(data_output_sum)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "wet_days_min", 18, year, data_output_min)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "wet_days_avg", 19, year, data_output_avg)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "wet_days_max", 20, year, data_output_max)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "wet_days_sum", 21, year, data_output_sum)
            del data_output_min
            del data_output_avg
            del data_output_max
            del data_output_sum
        self.io.reset_data()
        print("Generate Data: Finished wet days generation")

    # avg, min, max, sum frost days per year
    def __generate_frost_days(self, cloud: bool, lat_len, lon_len, years: list):
        print("Generate Data: Starting frost days generation")
        self.io.check_data(DATA, ["frs"])
        self.io.import_data(DATA, ["frs"])

        for year in years:
            print("Generate Data: Generating frost days {0:.2f}%".format((years.index(year) / len(years)) * 100))
            data_output_min = list()
            data_output_avg = list()
            data_output_max = list()
            data_output_sum = list()
            for lat in range(lat_len):
                for lon in range(lon_len):
                    year_data_frs = self.io.get_year_data("frs", year, lat, lon)
                    if len(year_data_frs) > 0:
                        data_lat_lon_min = self.__generate_payload(lat, lon, round(min(year_data_frs), 2))
                        data_output_min.append(data_lat_lon_min)
                        del data_lat_lon_min
                        average = sum(year_data_frs) / len(year_data_frs)
                        data_lat_lon_avg = self.__generate_payload(lat, lon, round(average, 2))
                        data_output_avg.append(data_lat_lon_avg)
                        del data_lat_lon_avg
                        data_lat_lon_max = self.__generate_payload(lat, lon, round(max(year_data_frs), 2))
                        data_output_max.append(data_lat_lon_max)
                        del data_lat_lon_max
                        data_lat_lon_sum = self.__generate_payload(lat, lon, round(sum(year_data_frs), 2))
                        data_output_sum.append(data_lat_lon_sum)
                        del data_lat_lon_sum
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "frost_days_min", 22, year, data_output_min, "b", 0, 31)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "frost_days_avg", 23, year, data_output_avg, "b", 0, 31)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "frost_days_max", 24, year, data_output_max, "b", 0, 31)
            self.gm.generate_map_scale(OUTPUT_DIR_MAPS, "frost_days_sum", 25, year, data_output_sum, "b", 0, 365)
            if cloud:
                self.io.export_data_cloud(data_output_min)
                self.io.export_data_cloud(data_output_avg)
                self.io.export_data_cloud(data_output_max)
                self.io.export_data_cloud(data_output_sum)
            else:
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "frost_days_min", 22, year, data_output_min)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "frost_days_avg", 23, year, data_output_avg)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "frost_days_max", 24, year, data_output_max)
                self.io.export_data_json(OUTPUT_DIR_JSON_DATA, "frost_days_sum", 25, year, data_output_sum)
            del data_output_min
            del data_output_avg
            del data_output_max
            del data_output_sum
        self.io.reset_data()
        print("Generate Data: Finished frost days generation")
