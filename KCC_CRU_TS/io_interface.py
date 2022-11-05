#!python3
import netCDF4
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import json
import csv
import pandas as pd


class IOInterface:
    def __init__(self):
        print("IO: init")
        self.__data = dict()
        self.__const = dict()
        self.__checked_const = False
        self.__checked_data = []
        self.__imported_const = False
        self.__imported_data = []

    def check_const(self, data: dict):
        print("IO: Check const compat")
        checked = list()
        for key1 in data:
            file1 = netCDF4.Dataset(data[key1])
            for key2 in data:
                if key1 != key2:
                    check = (key1, key2)
                    check_i = (key2, key1)
                    if check not in checked:
                        file2 = netCDF4.Dataset(data[key2])
                        self.__check_compat("Variables " + key1 + "/" + key2, len(file1.variables.keys()),
                                            len(file2.variables.keys()))
                        self.__check_compat("Longitude " + key1 + "/" + key2, file1.variables["lon"][:].size,
                                            file2.variables["lon"][:].size)
                        self.__check_compat("Latitude " + key1 + "/" + key2, file1.variables["lat"][:].size,
                                            file2.variables["lat"][:].size)
                        self.__check_compat("Time " + key1 + "/" + key2, file1.variables["time"][:].size,
                                            file2.variables["time"][:].size)
                        file2.close()
                        checked.append(check_i)
            file1.close()
        self.__checked_const = True
        print("IO: Checked const compat")

    def check_data(self, data: dict, keys: list):
        print("IO: Check data compat {}".format(keys))
        if not self.__checked_const:
            print("IO: Const not checked")
            sys.exit(0)
        for key in keys:
            if key not in data.keys():
                print("IO: {} not in data".format(key))
                sys.exit(0)

        checked = list()
        for key1 in keys:
            file1 = netCDF4.Dataset(data[key1])
            for key2 in keys:
                if key1 != key2:
                    check = (key1, key2)
                    check_i = (key2, key1)
                    if check not in checked:
                        file2 = netCDF4.Dataset(data[key2])
                        # TODO REMOVE COMMENTS
                        # self.__check_compat("Data " + key1 + "/" + key2, file1.variables[key1][:, :, :].size,
                        #                     file2.variables[key2][:, :, :].size)
                        # self.__check_compat("Stations " + key1 + "/" + key2, file1.variables["stn"][:, :, :].size,
                        #                     file2.variables["stn"][:, :, :].size)
                        # self.__check_compat_a("Longitude values " + key1 + "/" + key2, file1.variables["lon"][:],
                        #                       file2.variables["lon"][:])
                        # self.__check_compat_a("Latitude values " + key1 + "/" + key2, file1.variables["lat"][:],
                        #                       file2.variables["lat"][:])
                        # self.__check_compat_a("Time values " + key1 + "/" + key2, file1.variables["time"][:],
                        #                       file2.variables["time"][:])
                        file2.close()
                        checked.append(check_i)
            file1.close()
        for key in keys:
            self.__checked_data.append(key)
        print("IO: Checked data compat {}".format(keys))

    def import_data_const(self, data: dict):
        print("IO: import const")
        if not self.__checked_const:
            print("IO: Const not checked")
            sys.exit(0)

        f_tmp = netCDF4.Dataset(data["tmp"])
        self.__const["len"] = dict()
        self.__const["len"]["years"] = int(len(f_tmp.variables["time"][:])) / 12
        self.__const["len"]["months"] = int(len(f_tmp.variables["time"][:]))
        self.__const["len"]["lat"] = int(len(f_tmp.variables["lat"][:]))
        self.__const["len"]["lon"] = int(len(f_tmp.variables["lon"][:]))
        self.__const["data"] = dict()
        self.__const["data"]["time"] = np.copy(f_tmp.variables["time"][:])
        self.__const["data"]["lat"] = np.copy(f_tmp.variables["lat"][:])
        self.__const["data"]["lon"] = np.copy(f_tmp.variables["lon"][:])
        self.__imported_const = True
        print("IO: const imported")

    def import_data(self, data: dict, keys: list):
        print("IO: import data {}".format(keys))
        if not self.__checked_const:
            print("IO: Const not checked")
            sys.exit(0)
        if not self.__imported_const:
            print("IO: Const not imported")
            sys.exit(0)
        if len(self.__checked_data) == 0:
            print("IO: Data not checked")
            sys.exit(0)
        for key in keys:
            if key not in self.__checked_data:
                print("IO: {} not checked".format(key))
                sys.exit(0)

        files = dict()
        for key in keys:
            files[key] = netCDF4.Dataset(data[key])

        start_date = datetime(1900, 1, 1, 0, 0)
        time_len = self.__const["len"]["months"]
        for time_index in range(time_len):
            # print("IO: Import {0} {1:.2f}%".format(keys, (time_index / time_len) * 100))
            days_since = int(self.__const["data"]["time"][time_index])
            current_date = start_date + timedelta(days=days_since)
            year = current_date.year
            month = current_date.month
            if year not in self.__data.keys():
                self.__data[year] = dict()
            self.__data[year][month] = dict()
            for key, file in files.items():
                self.__data[year][month][key] = np.ma.copy(file.variables[key][time_index, :, :])
                # self.__data[year][month][key + "-stn"] = np.ma.copy(file.variables["stn"][time_index, :, :])
        for key, file in files.items():
            self.__imported_data.append(key)
            file.close()
        print("IO: data imported {}".format(keys))

    @staticmethod
    def import_csv(path: str):
        csv_list = list()
        header = []
        with open(path, mode='r', encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            is_header = True
            for row in reader:
                item = dict()
                if is_header:
                    header = row
                    is_header = False
                else:
                    i = 0
                    while i < len(header):
                        item[header[i]] = row[i]
                        i += 1
                    csv_list.append(item)
                del item
        return csv_list

    def reset_data(self):
        self.__data.clear()
        self.__checked_data.clear()
        self.__imported_data.clear()

    def reset_all(self):
        self.__data.clear()
        self.__const.clear()
        self.__checked_const = False
        self.__checked_data.clear()
        self.__imported_const = False
        self.__imported_data.clear()

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
            print("IO: Data array not compatible: {}".format(name))
            sys.exit(0)
        else:
            print("IO: Data array compatible: {}".format(name))

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

    def get_month_data(self, key: str, year: int, month: int, lat_index: int, lon_index: int):
        if not self.__imported_const:
            print("IO: Const not imported")
            sys.exit(0)
        if key not in self.__imported_data:
            print("IO: {} not imported".format(key))
            sys.exit(0)

        data = self.__data[year][month][key][lat_index][lon_index]
        if np.ma.is_masked(data):
            return None
        return float(data)

    # If error, maybe here
    # In the loop, maybe the funct doesn't erase data with none
    # added del to prevent this issue
    def get_year_data(self, key: str, year: int, lat_index: int, lon_index: int) -> list:
        if not self.__imported_const:
            print("IO: Const not imported")
            sys.exit(0)
        if key not in self.__imported_data:
            print("IO: {} not imported".format(key))
            sys.exit(0)

        data_year = list()
        for month in range(1, 13):
            data = self.get_month_data(key, year, month, lat_index, lon_index)
            if data is None:
                return []
            else:
                data_year.append(float(data))
            del data
        return data_year

    @staticmethod
    def export_data_json(out_dir, name, name_type, year, props: list):
        path = out_dir + str(year) + "-" + str(name_type) + "-" + name + ".json"
        print("IO: export json data : {}".format(path))
        data_output = dict()
        data_output["type"] = name_type
        data_output["year"] = year
        data_output["data"] = props
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        data_json = json.dumps(data_output, indent=4)
        with open(path, "w") as f:
            f.write(data_json)
        print("IO: exported json data : {}".format(path))

    @staticmethod
    def export_param_json(out_dir, name, params: list):
        path = out_dir + "params-" + name + ".json"
        print("IO: export json params : {}".format(path))
        data_output = dict()
        data_output["type"] = name
        data_output["pl"] = params
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        data_json = json.dumps(data_output, indent=4)
        with open(path, "w") as f:
            f.write(data_json)
        print("IO: exported json params : {}".format(path))

    # TODO export to mongoDB
    @staticmethod
    def export_data_cloud(datalist: list):
        print("export to cloud")
        for data in datalist:
            # put many to cloud
            pass

    @staticmethod
    def export_param_cloud(datalist: list):
        print("export to cloud")
        for data in datalist:
            # put many to cloud
            pass

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
