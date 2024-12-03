from typing import List, Tuple
from .package import Package
from .uld import ULD
from .utils import log, save_file_and_get_name


def select_uld(
    list_of_ulds: List[ULD], priority_package_list: List[Package]
):  # returns best available uld, taking in the list of remaining priority packages

    uld_list = list_of_ulds.copy()

    if uld_list == []:
        return None

    if priority_package_list == []:
        return uld_list[0]

    total_priority_package_weight = 0
    total_priority_package_volume = 0

    for package in priority_package_list:
        total_priority_package_weight += package.weight
        total_priority_package_volume += package.volume

    density = total_priority_package_weight / total_priority_package_volume
    capacity = (
        lambda uld: (uld.volume) * (uld.weight_limit) / (density - uld.pseudo_density)
    )  # heuristic value of a uld. Takes density into account as well as how spacious it is.

    best_cap = 0
    best_uld = uld_list[0]
    for uld in uld_list:
        cap = capacity(uld)
        if cap > best_cap:
            best_cap = cap
            best_uld = uld

    return best_uld


### Density Grouping


def binary_search_closest(
    lst: List[float], n: float
):  # takes in a sorted list (ascending order) and tries to find the value closest to n in it. returns its index

    if len(lst) == 0:
        return None

    first_pointer = 0
    last_pointer = len(lst) - 1
    best_idx = 0
    best_score = abs(lst[best_idx] - n)

    while last_pointer - first_pointer > 1:

        middle_pointer = (last_pointer + first_pointer) // 2
        element = lst[middle_pointer]
        score = abs(element - n)

        if score < best_score:
            best_score = score
            best_idx = middle_pointer

        if element < n:
            first_pointer = middle_pointer + 1
        else:
            last_pointer = middle_pointer - 1

    elem1, elem2 = (
        lst[first_pointer],
        lst[last_pointer],
    )  # checking the last two (or one) elements
    if abs(elem1 - n) < best_score:
        best_score = abs(elem1 - n)
        best_idx = first_pointer
    if abs(elem2 - n) < best_score:
        best_score = abs(elem2 - n)
        best_idx = last_pointer

    return best_idx


def allocate_packages(
    uld: ULD, list_of_packages: List[Package]
):  # takes in a single uld and a big list of packages and selects some of them for the uld so as to minimize wastage of space and weight. Also returns loss (maximum of the two losses)

    package_list = list_of_packages.copy()
    density = lambda package: package.density
    package_list.sort(key=density)
    density_list = [package.density for package in package_list]

    desired_density = uld.pseudo_density  # this value will change over time
    remaining_volume = uld.volume
    remaining_weight_limit = uld.weight_limit

    selected_packages = []
    while True:
        idx = binary_search_closest(density_list, desired_density)
        if idx == None:
            break

        best_package = package_list[idx]
        if (
            best_package.weight > remaining_weight_limit
            or best_package.volume > remaining_volume
        ):
            break

        selected_packages.append(best_package)
        package_list.pop(idx)
        density_list.pop(idx)
        remaining_volume -= best_package.volume
        remaining_weight_limit -= best_package.weight
        if remaining_volume == 0 or remaining_weight_limit == 0:
            break
        desired_density = remaining_weight_limit / remaining_volume

    return selected_packages


### Three-Dimensional Recursive Stacking


def compare_surfaces(
    inner_surface: Tuple[float], outer_surface: Tuple[float]
):  # returns what fraction of outer surface the inner will occupy. if it does not fit, it returns None. format : (x,y)
    if inner_surface[0] > outer_surface[0] or inner_surface[1] > outer_surface[1]:
        return None

    inner_area = inner_surface[0] * inner_surface[1]
    outer_area = outer_surface[0] * outer_surface[1]

    return inner_area / outer_area


def three_dimensional_recursive_stacking(
    uld: ULD, package_list: List[Package], active_box: Tuple[Tuple[float]]
):  # 3DRS is a legendary algorithm that fills a given ULD with a given list of packages and returns the leftovers
    # note: active box is a pair of sets of coordinates. Format: ((x1,y1,z1),(x2,y2,z2)) representing what region is in consideration. At the start it is the ULD itself
    # the function prioritizes priority packages over economy

    packages_in_queue = package_list.copy()
    priority_list = [package for package in packages_in_queue if package.is_priority]

    x1, y1, z1 = active_box[0]
    x2, y2, z2 = active_box[1]
    outer_surface = (x2 - x1, y2 - y1)
    orientation_preference_order = ["xyz", "yzx", "xzy", "zxy", "yzx", "zyx"]

    best_fit = None
    best_fit_fraction = 0

    if len(priority_list) == 0:
        lst = packages_in_queue.copy()
    else:
        lst = priority_list.copy()

    for package in lst:
        for order in orientation_preference_order:
            a, b, c = (
                package.dimensions[order[0]],
                package.dimensions[order[1]],
                package.dimensions[order[2]],
            )
            inner_surface = (a, b)
            area_fraction = compare_surfaces(inner_surface, outer_surface)

            if (
                area_fraction == None
                or c > (z2 - z1)
                or package.weight > uld.remaining_weight_limit
            ):
                continue
            if area_fraction > best_fit_fraction:
                best_fit = package
                best_fit_orientation = order
                best_fit_fraction = area_fraction
                break

    if best_fit == None:
        return packages_in_queue

    p_x = best_fit.dimensions[best_fit_orientation[0]]
    p_y = best_fit.dimensions[best_fit_orientation[1]]
    p_z = best_fit.dimensions[best_fit_orientation[2]]

    drop_successful = uld.drop_package(best_fit, x1, y1, p_x, p_y, p_z)
    if not (drop_successful):
        return packages_in_queue

    packages_in_queue.remove(best_fit)

    packages_in_queue = three_dimensional_recursive_stacking(
        uld, packages_in_queue, ((x1, y1, z1 + p_z), (x1 + p_x, y1 + p_y, z2))
    )  # recursion along z
    packages_in_queue = three_dimensional_recursive_stacking(
        uld, packages_in_queue, ((x1, y1 + p_y, z1), (x1 + p_x, y2, z2))
    )  # recursion along y
    packages_in_queue = three_dimensional_recursive_stacking(
        uld, packages_in_queue, ((x1 + p_x, y1, z1), (x2, y2, z2))
    )  # recursion along x

    return packages_in_queue


### Brute Packing


def brute_pack(
    uld: ULD, package_list: List[Package], precision: int
):  # attempts to fit all given packages by brute force. precision is a natural number representing how finely we want to divide the box into areas for brute packing
    # also returns leftovers

    x_steps = [((uld.dimensions["x"]) * i) // precision for i in range(precision + 1)]
    y_steps = [((uld.dimensions["y"]) * i) // precision for i in range(precision + 1)]

    leftovers = package_list.copy()
    volume = lambda package: package.volume

    flag = False
    for x in x_steps[::-1]:
        for y in y_steps[::-1]:
            for package in sorted(package_list, key=volume):
                drop_successful = uld.raw_drop(x, y, package)
                if drop_successful:
                    flag = True
                    leftovers.remove(package)
                    break
            if flag:
                break

    return leftovers


### Packing


def stack_priority_packages(
    ulds: List[ULD], priority_packages: List[Package]
):  # packs all priority packages into uld. returns last uld and all empty ulds.

    remaining_packages = priority_packages.copy()
    remaining_ulds = ulds.copy()

    while remaining_packages != []:

        if remaining_ulds == []:
            raise Exception(
                "RAN OUT OF ULDS BEFORE ALL PRIORITY PACKAGES COULD BE PACKED"
            )

        uld = select_uld(remaining_ulds, remaining_packages)

        selected_packages = allocate_packages(uld, remaining_packages)
        leftovers = three_dimensional_recursive_stacking(
            uld,
            selected_packages,
            (
                (0, 0, 0),
                (uld.dimensions["x"], uld.dimensions["y"], uld.dimensions["z"]),
            ),
        )
        brute_leftovers = brute_pack(uld, leftovers, 10)

        remaining_ulds.remove(uld)
        remaining_packages = [
            package for package in remaining_packages if not (package.placed)
        ]

    return (
        uld,
        remaining_ulds,
    )  # returns last used uld, so that its empty space may be used for economy packages. and the empty ulds are returned as well


def transition_stacking(
    uld: ULD, economy_packages: List[Package]
):  # takes in a uld that has been filled with priority packages (but not completely) and fills the remaining space with economy packages. returns remaining economy packages

    selected_priority_packages = []
    for package_details in uld.packages:
        package = package_details[0]
        selected_priority_packages.append(package)

    wt = uld.remaining_weight_limit
    vol = uld.remaining_volume
    uld.empty()

    dimensions = (
        uld.real_dimensions["x"],
        uld.real_dimensions["y"],
        uld.real_dimensions["z"],
    )
    imaginary_uld = ULD(uld.name + "i", dimensions, uld.weight_limit)
    imaginary_uld.volume = imaginary_uld.remaining_volume = vol
    imaginary_uld.weight_limit = imaginary_uld.remaining_weight_limit = wt
    imaginary_uld.pseudo_density = wt / vol

    selected_economy = allocate_packages(imaginary_uld, economy_packages)
    new_package_list = selected_priority_packages + selected_economy
    leftovers = three_dimensional_recursive_stacking(
        uld,
        new_package_list,
        ((0, 0, 0), (uld.dimensions["x"], uld.dimensions["y"], uld.dimensions["z"])),
    )
    brute_leftovers = brute_pack(
        uld, leftovers, 10
    )  # this list will solely be comprised of economy packages. however, this list is irrelevant and we will simply treat them as the rest of the economy packages.

    remaining_packages = [
        package for package in economy_packages if not (package.placed)
    ]

    return remaining_packages


def stack_economy_packages(
    all_ulds: List[ULD], remaining_ulds: List[ULD], remaining_packages: List[Package]
):  # packs all the economy packages that it can across all ulds. returns economy packages that could not be stacked.

    while remaining_packages != [] and remaining_ulds != []:

        uld = select_uld(remaining_ulds, remaining_packages)
        selected_packages = allocate_packages(uld, remaining_packages)

        leftovers = three_dimensional_recursive_stacking(
            uld,
            selected_packages,
            (
                (0, 0, 0),
                (uld.dimensions["x"], uld.dimensions["y"], uld.dimensions["z"]),
            ),
        )
        packages_left_behind = brute_pack(uld, leftovers, 10)

        remaining_ulds.remove(uld)
        remaining_packages = [
            package
            for package in remaining_packages
            if (package not in selected_packages) or (package in packages_left_behind)
        ]

    final_leftovers = remaining_packages
    lost_packages = []
    for uld in all_ulds:
        packages_to_be_discarded = brute_pack(uld, final_leftovers, 10)
        lost_packages += packages_to_be_discarded

    return lost_packages


### Compiling Results


def finish_packing(
    ulds: List[ULD], priority_uld_cost: float, economy_packages: List[Package]
):  # reverts all ULDs to original position and calculates cost

    unplaced_economy_packages = [
        package for package in economy_packages if not (package.placed)
    ]

    priority_uld_total_cost = 0

    for uld in ulds:
        uld.rotate_ULD()
        if uld.priority:
            priority_uld_total_cost += priority_uld_cost

    delay_cost_sum = 0
    for package in unplaced_economy_packages:
        delay_cost_sum += package.delay_cost

    total_cost = priority_uld_total_cost + delay_cost_sum
    log(priority_uld_total_cost, delay_cost_sum)
    return total_cost


def confirm_validity(
    ulds: List[ULD], priority_packages: List[Package]
):  # checks if all constraints are satisfied

    for package in priority_packages:
        if not (package.placed):
            print("ERROR_LOG: NOT ALL PRIORITY PACKAGES WERE PACKED")
            print()

            raise Exception("NOT ALL PRIORITY PACKAGES WERE PACKED")

    for uld in ulds:
        package_list = [package_details[0] for package_details in uld.packages]
        total_package_volume = total_package_weight = 0
        for package in package_list:
            total_package_volume += package.volume
            total_package_weight += package.weight
        if total_package_weight > uld.weight_limit or total_package_volume > uld.volume:
            print("ERROR_LOG: LIMITS EXCEEDED IN ONE OR MORE ULDS")
            print()
            raise Exception("LIMITS EXCEEDED IN ONE OR MORE ULDS")


def get_data(packages: List[Package], ulds: List[ULD], k: float):

    priority_packages = [package for package in packages if package.is_priority]
    economy_packages = [package for package in packages if not package.is_priority]
    return ulds, priority_packages, economy_packages, k


def compile_data(ulds, packages):

    package_list = []

    for package in packages:
        name = package.name

        if not (package.placed):

            package_dict = {
                "name": name,
                "is_priority": package.is_priority,
                "is_placed": False,
                "uld": None,
                "reference_corner": None,
                "diagonally_opposite_corner": None,
            }

        else:

            required_package_details = None
            for uld in ulds:
                for package_details in uld.packages:
                    uld_package_name = package_details[0].name
                    if uld_package_name == name:
                        required_package_details = package_details
                        used_uld = uld.name

            _, centre_of_mass, dimensions = required_package_details

            closest_corner = f"({centre_of_mass[0] - dimensions[0] / 2}, {centre_of_mass[1] - dimensions[1] / 2}, {centre_of_mass[2] - dimensions[2] / 2})"

            furthest_corner = f"({centre_of_mass[0] + dimensions[0] / 2}, {centre_of_mass[1] + dimensions[1] / 2}, {centre_of_mass[2] + dimensions[2] / 2})"
            package_dict = {
                "name": name,
                "is_priority": package.is_priority,
                "is_placed": True,
                "uld": used_uld,
                "reference_corner": closest_corner,
                "diagonally_opposite_corner": furthest_corner,
            }

        package_list.append(package_dict)

    return package_list


def return_data(ulds, packages, k):

    economy_packages = [package for package in packages if not (package.is_priority)]
    cost = finish_packing(ulds, k, economy_packages)

    package_list = compile_data(ulds, packages)
    packages_placed = len([package for package in packages if package.placed])
    priority_ulds = len([uld for uld in ulds if uld.priority])  


    dict = {"total_cost": cost, "priority_uld_count": priority_ulds, "packages_placed": packages_placed,     "packages": package_list}
    return dict
