#!python3
import time
import sys

from .generate_data import GenerateData


# !! WARNING Af IS EQUAL TO Az !!
def main() -> None:
    start_time = time.time()
    print("Main: Start program")

    gd = GenerateData()

    print("Main: Choose action:")
    print("Main: 0 - Generate Data Preview on disk")
    print("Main: 1 - Generate Maps Preview on disk")
    print("Main: 2 - Generate Data/Maps Preview on disk")
    print("Main: 3 - Generate/Upload Data Preview on cloud")
    print("Main: 4 - Generate/Upload Data/Maps Preview on cloud")
    print("Main: 5 - Generate ALL Data on disk (!Disk Usage)")
    print("Main: 6 - Generate ALL Maps on disk (!Disk Usage)")
    print("Main: 7 - Generate ALL Data/Maps on disk (!Disk Usage)")
    print("Main: 8 - Generate/Upload ALL Data on cloud (!RAM,Cost)")
    print("Main: 9 - Generate/Upload ALL Data/Maps on cloud (!RAM,Cost)")
    print("Main: X - EXIT")
    choice = int(input("=> "))

    preview = True
    save_data = True
    cloud = False
    gen_maps = False
    disabled = False
    if choice == 0:
        print("Main: 0 - Generate Data Preview on disk")
    elif choice == 1:
        print("Main: 1 - Generate Maps Preview on disk")
        save_data = False
        gen_maps = True
    elif choice == 2:
        print("Main: 2 - Generate Data/Maps Preview on disk")
        gen_maps = True
    elif choice == 3:
        print("Main: 3 - Generate/Upload Data Preview on cloud")
        cloud = True
    elif choice == 4:
        print("Main: 4 - Generate/Upload Data/Maps Preview on cloud")
        cloud = True
        gen_maps = True
    elif choice == 5:
        print("Main: 5 - Generate ALL Data on disk")
        disabled = True
        preview = False
    elif choice == 6:
        print("Main: 6 - Generate ALL Maps on disk")
        disabled = True
        preview = False
        save_data = False
        gen_maps = True
    elif choice == 7:
        print("Main: 7 - Generate ALL Data/Maps on disk")
        disabled = True
        preview = False
        gen_maps = True
    elif choice == 8:
        print("Main: 8 - Generate/Upload ALL Data on cloud")
        disabled = True
        preview = False
        cloud = True
    elif choice == 9:
        print("Main: 9 - Generate/Upload ALL Data/Maps on cloud")
        disabled = True
        preview = False
        cloud = True
        gen_maps = True

    if choice > 9 or choice < 0 or disabled:
        if disabled:
            print("Main: Disabled")
        print("Main: Exiting")
        sys.exit(0)

    gd.generate_data(preview=preview, save_data=save_data, cloud=cloud, gen_maps=gen_maps)

    end_time = time.time()
    time_elapsed_s = end_time - start_time
    print("Main: Time elapsed : {0:.2f} seconds".format(time_elapsed_s))
    time_elapsed_m = time_elapsed_s / 60
    print("Main: Or {0:.2f} minutes".format(time_elapsed_m))
    time_elapsed_h = time_elapsed_m / 60
    print("Main: Or {0:.2f} hours".format(time_elapsed_h))
