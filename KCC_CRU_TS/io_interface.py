#!python3
import netCDF4
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import json


# 50.180582, 5.864852 Cherain
class IOInterface:
    def __init__(self):
        print("IO: init")
        self.__data = dict()
        self.__const = dict()
        self.__data_imported = False

    # TODO only need to check data if 2 data source are involved to compute data
    # TODO Climates, wet bulb, etc
    def check_data(self, data: dict):
        f_tmp = netCDF4.Dataset(data["tmp"])
        f_pre = netCDF4.Dataset(data["pre"])

        print(f_tmp.variables.keys())
        print(f_pre.variables.keys())

        print("IO: Check compat")
        self.__check_compat("Variables", len(f_tmp.variables.keys()), len(f_pre.variables.keys()))
        self.__check_compat("Longitude", f_tmp.variables["lon"][:].size, f_pre.variables["lon"][:].size)
        self.__check_compat("Latitude", f_tmp.variables["lat"][:].size, f_pre.variables["lat"][:].size)
        self.__check_compat("Time", f_tmp.variables["time"][:].size, f_pre.variables["time"][:].size)
        self.__check_compat("Data", f_tmp.variables["tmp"][:, :, :].size, f_pre.variables["pre"][:, :, :].size)
        self.__check_compat("Stations", f_tmp.variables["stn"][:, :, :].size, f_pre.variables["stn"][:, :, :].size)
        self.__check_compat_a("Longitude values", f_tmp.variables["lon"][:], f_pre.variables["lon"][:])
        self.__check_compat_a("Latitude values", f_tmp.variables["lat"][:], f_pre.variables["lat"][:])
        self.__check_compat_a("Time values", f_tmp.variables["time"][:], f_pre.variables["time"][:])

        f_tmp.close()
        f_pre.close()
        print("IO: Compat checked")

    # TODO Multiple import funct for each data
    def import_data(self, data: dict):
        print("IO: import data")
        f_tmp = netCDF4.Dataset(data["tmp"])
        f_pre = netCDF4.Dataset(data["pre"])

        self.__const["len"] = dict()
        self.__const["len"]["years"] = int(len(f_tmp.variables["time"][:]))/12
        self.__const["len"]["months"] = int(len(f_tmp.variables["time"][:]))
        self.__const["len"]["lat"] = int(len(f_tmp.variables["lat"][:]))
        self.__const["len"]["lon"] = int(len(f_tmp.variables["lon"][:]))
        self.__const["data"] = dict()
        self.__const["data"]["time"] = np.copy(f_tmp.variables["time"][:])
        self.__const["data"]["lat"] = np.copy(f_tmp.variables["lat"][:])
        self.__const["data"]["lon"] = np.copy(f_tmp.variables["lon"][:])

        start_date = datetime(1900, 1, 1, 0, 0)
        time_len = int(len(f_tmp.variables["time"][:]))
        for time_index in range(time_len):
            print("IO: Import {0:.2f}%".format((time_index / time_len) * 100))
            days_since = int(f_tmp.variables["time"][time_index])
            current_date = start_date + timedelta(days=days_since)
            year = current_date.year
            month = current_date.month
            if year not in self.__data.keys():
                self.__data[year] = dict()
            self.__data[year][month] = dict()
            self.__data[year][month]["tmp"] = np.ma.copy(f_tmp.variables["tmp"][time_index, :, :])
            self.__data[year][month]["pre"] = np.ma.copy(f_pre.variables["pre"][time_index, :, :])
            # self.__data[year][month]["tmp-stn"] = np.ma.copy(f_tmp.variables["stn"][time_index, :, :])
            # self.__data[year][month]["pre-stn"] = np.ma.copy(f_pre.variables["stn"][time_index, :, :])
        f_tmp.close()
        f_pre.close()
        self.__data_imported = True
        print("IO: data imported")

    # TODO adapt export to GEOJson
    @staticmethod
    def export_data_open(out_dir, file):
        path = out_dir + "/" + file + ".json"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        f = open(path, "a")
        f.write("{")
        f.close()
        print("IO: file {} opened".format(file))

    @staticmethod
    def export_data_save(out_dir, file, year, data):
        path = out_dir + "/" + file + ".json"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        data_json = json.dumps(data, indent=4)
        f = open(path, "a")
        f.write('"' + str(year) + '" : ')
        f.write(data_json)
        f.close()
        print("IO: file {} saved".format(file))

    @staticmethod
    def export_data_comma(out_dir, file):
        path = out_dir + "/" + file + ".json"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        f = open(path, "a")
        f.write(",")
        f.close()

    @staticmethod
    def export_data_close(out_dir, file):
        path = out_dir + "/" + file + ".json"
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        f = open(path, "a")
        f.write("}")
        f.close()
        print("IO: file {} closed".format(file))

    @staticmethod
    def __check_compat(name: str, var1, var2):
        if var1 != var2:
            print("IO: Data not compatible: {} ({}!={})".format(name, var1, var2))
            sys.exit(0)
        else:
            print("IO: Data compatible: {} ({})".format(name, var1))

    @staticmethod
    def __check_compat_a(name: str, var1, var2):
        if not np.array_equal(var1, var2):
            print("IO: Data not compatible: {}".format(name))
            sys.exit(0)
        else:
            print("IO: Data compatible: {}".format(name))

    def get_data_size(self):
        return len(self.__data)

    def get_years(self):
        years = list()
        start_date = datetime(1900, 1, 1, 0, 0)
        for days_since in self.__const["data"]["time"]:
            current_date = start_date + timedelta(days=int(days_since))
            year = current_date.year
            if year not in years:
                years.append(year)
        return years

    def get_lat(self, index):
        return self.__const["data"]["lat"][index]

    def get_lat_len(self):
        return self.__const["len"]["lat"]

    def get_lon(self, index):
        return self.__const["data"]["lon"][index]

    def get_lon_len(self):
        return self.__const["len"]["lon"]

    def get_year_data(self, name: str, year: int, lat_index: int, lon_index: int):
        data_year = list()
        for i in range(1, 13):
            data = self.__data[year][i][name][lat_index][lon_index]
            if np.ma.is_masked(data):
                return []
            else:
                data_year.append(float(self.__data[year][i][name][lat_index][lon_index]))
        return data_year

    def tests(self):
        print("IO: test")
        # print(self.__data)
        print("Years : {}".format(len(self.__data)))
        print("Months : {}".format(len(self.__data[1901])))
        print("Data types : {}".format(len(self.__data[1901][1])))
        print("Latitude : {}".format(len(self.__data[1901][1]["tmp"])))
        print("Longitude : {}".format(len(self.__data[1901][1]["tmp"][0])))
        print("Data : {}".format(self.__data[1901][1]["tmp"][0][0]))
        print("Const years : {}".format(self.__const["len"]["years"]))
        print("Const months : {}".format(self.__const["len"]["months"]))
        # print("{}".format(self.__const["data"]["time"]))
        print("Const lat : {}".format(self.__const["len"]["lat"]))
        # print("{}".format(self.__const["data"]["lat"]))
        print("Const lon : {}".format(self.__const["len"]["lon"]))
        # print("{}".format(self.__const["data"]["lon"]))
        print(self.__const["data"]["time"][60])
        print(self.__const["data"]["lat"][256])
        print(self.__const["data"]["lon"][700])
        # print(self.__data[1924][2]["tmp"][270][360])
        for lat in range(self.__const["len"]["lat"]):
            for lon in range(self.__const["len"]["lon"]):
                print(self.get_year_data("tmp", 1905, lat, lon))