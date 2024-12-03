import time
import random


def log(head, message):

    print()
    print()
    print(f"{head}:")
    print()
    print(message)
    print()
    print()


def save_file_and_get_name(output_data):
    path = f"{time.time()*random.randint(1,1000)}.txt"
    f = open(path, "w")
    s = ""
    
    s += f"{output_data["total_cost"]},{output_data["packages_placed"]},{output_data['priority_uld_count']}\n"

    for package in output_data["packages"]:
        if package["uld"] == None:
            s += f"{package["name"]},NONE,-1,-1,-1,-1,-1,-1\n"
        else:
            reference_corner = package["reference_corner"]
            reference_corner = reference_corner[1 : len(reference_corner) - 1]
            reference_corner = reference_corner.split(",")
            diagonally_opposite_corner = package["diagonally_opposite_corner"]
            diagonally_opposite_corner = diagonally_opposite_corner[
                1 : len(diagonally_opposite_corner) - 1
            ]
            diagonally_opposite_corner = diagonally_opposite_corner.split(",")
            s += f"{package["name"]},{package["uld"]},{reference_corner[0]},{reference_corner[1]},{reference_corner[2]},{diagonally_opposite_corner[0]},{diagonally_opposite_corner[1]},{diagonally_opposite_corner[2]}\n"

    f.write(s)
    f.close()

    return path.split("/")[-1]
