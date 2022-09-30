#!python3
import time

from .generate_data import GenerateData


# !! WARNING Af IS EQUAL TO Az !!
def main() -> None:
    start_time = time.time()
    print("Main: Start program")

    gd = GenerateData()

    choice = -1
    while choice != 0:
        print("Main: Choose action:")
        print("Main: 1 - Generate Data/Maps Preview")
        print("Main: 2 - Generate ALL Data/Maps on disk (!Disk Usage)")
        print("Main: 3 - Generate/Upload All Data/Maps (!RAM,Cost)")
        print("Main: 0 - EXIT")
        choice = int(input("=> "))

        if choice == 1:
            print("Main: 1 - Generate Data/Maps Preview")
            gd.generate_data(preview=True, cloud=False)
            break
        elif choice == 2:
            print("Main: 2 - Generate ALL Data on disk")
            # gd.generate_data(preview=False, cloud=False)
            print("Disabled for safety reason")
            break
        elif choice == 3:
            print("Main: 3 - Generate/Upload ALL Data/Maps")
            # gd.generate_data(preview=False, cloud=True)
            print("Disabled for safety reason")
            break
        else:
            print("Main: Exiting")

    end_time = time.time()
    time_elapsed_s = end_time - start_time
    print("Main: Time elapsed : {0:.2f} seconds".format(time_elapsed_s))
    time_elapsed_m = time_elapsed_s / 60
    print("Main: Or {0:.2f} minutes".format(time_elapsed_m))
    time_elapsed_h = time_elapsed_m / 60
    print("Main: Or {0:.2f} hours".format(time_elapsed_h))
