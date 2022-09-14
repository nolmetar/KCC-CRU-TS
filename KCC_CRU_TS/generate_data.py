#!python3
import time
from datetime import datetime

from .io_interface import IOInterface
from .compute import Compute
from .koppen import Koppen

DATA = {
    "tmp": "DATA/cru_ts4.06.1901.2021.tmp.dat.nc",
    "pre": "DATA/cru_ts4.06.1901.2021.pre.dat.nc"
}
OUTPUT_DIR = "OUTPUT"


def generate_climates():
    io = IOInterface()
    co = Compute()
    ko = Koppen()

    # io.check_data(DATA)
    io.import_data(DATA)
    # io.tests()
    # co.tests()

    file_name = "Koppen-climates_" + datetime.now().strftime("%Y%m%d-%H%M%S")
    io.export_data_open(OUTPUT_DIR, file_name)

    print("Main: Starting climate generation")
    lat_len = io.get_lat_len()
    lon_len = io.get_lon_len()
    # years = io.get_years()
    years = [2021]
    for year in years:
        print("Main: Generating {0:.2f}%".format((years.index(year) / len(years)) * 100))
        if not years.index(year) == 0:
            io.export_data_comma(OUTPUT_DIR, file_name)
        data_output = list()
        for lat in range(lat_len):
            for lon in range(lon_len):
                real_lat = float(io.get_lat(lat))
                real_lon = float(io.get_lon(lon))
                year_data_tmp = io.get_year_data("tmp", year, lat, lon)
                year_data_pre = io.get_year_data("pre", year, lat, lon)
                data_lat_lon = dict()
                data_lat_lon["coords"] = dict()
                data_lat_lon["coords"]["center"] = [real_lat, real_lon]
                data_lat_lon["coords"]["shape"] = co.gen_shape(real_lat, real_lon)
                data_lat_lon["data"] = dict()
                if len(year_data_tmp) == 0 or len(year_data_pre) == 0:
                    data_lat_lon["dataValid"] = False
                else:
                    data_lat_lon["dataValid"] = True
                    symbols = ko.compute_symbols(year_data_tmp, year_data_pre, real_lat)
                    data_lat_lon["data"]["symbols"] = "".join(symbols)
                    data_lat_lon["data"]["classname"] = ko.get_classname(symbols)
                    data_lat_lon["data"]["fullname"] = ko.get_fullname(symbols)
                    data_lat_lon["data"]["color"] = ko.get_color(symbols)
                data_output.append(data_lat_lon)
            # break
        io.export_data_save(OUTPUT_DIR, file_name, year, data_output)
        break
    io.export_data_close(OUTPUT_DIR, file_name)
    print("Main: Finished generation")


# !! WARNING Af IS EQUAL TO z !!
# Test
def main() -> None:
    start_time = time.time()
    print("Main: Start program")

    choice = -1
    while choice != 0:
        print("Main: Choose action:")
        print("Main: 1 - Generate Data Preview")
        print("Main: 2 - Generate All Data (! Disk Usage)")
        print("Main: 3 - Upload Data (! Costs)")
        print("Main: 4 - Generate and Upload All Data (! RAM)")
        print("Main: 0 - EXIT")
        choice = int(input("=> "))

        if choice == 1:
            print("Main: Generate Data Preview")
            #generate data with preview parameter
            generate_climates()
            break
        elif choice == 2:
            print("Main: Generate Data ALL")
            #generate all data
            break
        elif choice == 3:
            print("Main: Upload Data")
            #upload all in special folder
            break
        elif choice == 4:
            print("Main: Generate and Upload All Data")
            #generate all and upload without saving to disk
            break
        elif choice == 0:
            print("Main: Exiting")

    end_time = time.time()
    time_elapsed_s = end_time - start_time
    print("Main: Time elapsed : {0:.2f} seconds".format(time_elapsed_s))
    time_elapsed_m = time_elapsed_s / 60
    print("Main: Or {0:.2f} minutes".format(time_elapsed_m))
