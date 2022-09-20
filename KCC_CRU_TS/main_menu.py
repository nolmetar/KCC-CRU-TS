#!python3
import time

from .generate_data import GenerateData
from .generate_maps import GenerateMaps


# !! WARNING Af IS EQUAL TO z !!
# Test
def main() -> None:
    start_time = time.time()
    print("Main: Start program")

    gd = GenerateData()
    gm = GenerateMaps()

    gm.tests()

    choice = -1
    while choice != 0:
        print("Main: Choose action:")
        print("Main: 1 - Generate Data Preview")
        print("Main: 2 - Generate ALL Data (!Disk Usage)")
        print("Main: 3 - Generate Picture Maps Preview")
        print("Main: 4 - Generate ALL Picture Maps (!Disk Usage)")
        print("Main: 5 - Upload ALL Data (!Cost)")
        print("Main: 6 - Generate/Upload All Data/Maps (!RAM,Cost)")
        print("Main: 0 - EXIT")
        choice = int(input("=> "))

        if choice == 1:
            print("Main: 1 - Generate Data Preview")
            gd.generate_climates(preview=True)
            break
        elif choice == 2:
            print("Main: 2 - Generate ALL Data")
            gd.generate_climates(preview=False)
            break
        elif choice == 3:
            print("Main: 3 - Generate Picture Maps Preview")
            break
        elif choice == 4:
            print("Main: 4 - Generate ALL Picture Maps")
            break
        elif choice == 5:
            print("Main: 5 - Upload ALL Data")
            break
        elif choice == 6:
            print("Main: 6 - Generate/Upload All Data/Maps")
            break
        else:
            print("Main: Exiting")

    end_time = time.time()
    time_elapsed_s = end_time - start_time
    print("Main: Time elapsed : {0:.2f} seconds".format(time_elapsed_s))
    time_elapsed_m = time_elapsed_s / 60
    print("Main: Or {0:.2f} minutes".format(time_elapsed_m))
