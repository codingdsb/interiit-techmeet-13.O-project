import json
from .utils import log


class ULD(object):

    def __init__(self, name, dimensions, weight_limit):  # dimensions is a tuple
        self.name = name
        self.real_dimensions = {
            "x": dimensions[0],
            "y": dimensions[1],
            "z": dimensions[2],
        }
        self.dimensions = {
            "x": sorted(dimensions)[2],
            "y": sorted(dimensions)[1],
            "z": sorted(dimensions)[0],
        }
        self.weight_limit = weight_limit
        self.volume = self.dimensions["x"] * self.dimensions["y"] * self.dimensions["z"]
        self.pseudo_density = self.weight_limit / self.volume
        self.packages = (
            []
        )  # contains packages in the format [package, [COM], [dimensions]]. We will create packages with respect to sorted dimensions, and then rotate them all in the end.
        self.remaining_weight_limit = self.weight_limit
        self.remaining_volume = self.volume
        self.priority = False  # turns on if theres at least one priority package

    def __str__(self):
        formatted_packages = []
        for package_details in self.packages:
            lst = [str(package_details[0].name), package_details[1], package_details[2]]
            formatted_packages.append(lst)
        return (
            self.name
            + "\n"
            + "Real dimensions: "
            + str(self.real_dimensions)
            + "\n"
            + "Volume = "
            + str(self.volume)
            + "\n"
            + "Weight Limit = "
            + str(self.weight_limit)
            + "\n"
            + "Pseudo-density = "
            + str(self.pseudo_density)
            + "\n"
            + "Priority: "
            + str(self.priority)
            + "\n"
            + "Package List: "
            + str(formatted_packages)
        )

    def drop_package(
        self, package, x, y, p_x, p_y, p_z, real_drop=False
    ):  # xy are the desired coordinates and px,py,pz are dimensions. real_drop = True means dropping into correct dimensions
        if real_drop:
            dim = self.real_dimensions.copy()
        else:
            dim = self.dimensions.copy()

        if not (
            (0 <= x <= dim["x"])
            and (0 <= x + p_x <= dim["x"])
            and (0 <= y <= dim["y"])
            and (0 <= y + p_y <= dim["y"])
            and package.weight < self.remaining_weight_limit
            and package.volume < self.remaining_volume
        ):
            return False

        highest_point = 0  # we will find the package that has the highest z that occupies x,y. package is the object
        for package_details in self.packages:
            com, axes = package_details[1], package_details[2]
            x1, x2, y1, y2, high_point = (
                com[0] - axes[0] / 2,
                com[0] + axes[0] / 2,
                com[1] - axes[1] / 2,
                com[1] + axes[1] / 2,
                com[2] + axes[2] / 2,
            )
            if (x < x2 and x + p_x > x1) and (y < y2 and y + p_y > y1):
                highest_point = max(highest_point, high_point)

        z = highest_point

        if not ((0 <= z <= dim["z"]) and (0 <= z + p_z <= dim["z"])):
            return False
        else:
            self.packages.append(
                [package, [x + p_x / 2, y + p_y / 2, z + p_z / 2], [p_x, p_y, p_z]]
            )
            package.placed = True
            self.remaining_weight_limit -= package.weight
            self.remaining_volume -= package.volume
            if package.is_priority:
                self.priority = True
                log("PRIORITY", self.name)
                
            return True

    def raw_drop(
        self, x, y, package
    ):  # also drops the package, but in a non-fixed orientation. Only good for brute packing or debugging

        a, b, c = (
            package.dimensions["x"],
            package.dimensions["y"],
            package.dimensions["z"],
        )

        if self.drop_package(package, x, y, a, b, c):
            return True
        if self.drop_package(package, x, y, a, c, b):
            return True
        if self.drop_package(package, x, y, b, a, c):
            return True
        if self.drop_package(package, x, y, b, c, a):
            return True
        if self.drop_package(package, x, y, c, a, b):
            return True
        if self.drop_package(package, x, y, c, b, a):
            return True

        return False

    def rotate_ULD(self):

        old_packages = self.packages.copy()

        self.empty()

        dim = self.real_dimensions.copy()
        sdim = self.dimensions.copy()

        ### rotate all coordinates wrt rotation of ULD

        if dim == sdim:  # xyz transformation
            rotate = lambda coords: coords
            swap = lambda coords: coords

        if (
            dim["x"] == sdim["y"] and dim["y"] == sdim["x"] and dim["z"] == sdim["z"]
        ):  # yxz transformation
            rotate = lambda coords: [sdim["y"] - coords[1], coords[0], coords[2]]
            swap = lambda coords: [coords[1], coords[0], coords[2]]

        if (
            dim["x"] == sdim["x"] and dim["y"] == sdim["z"] and dim["z"] == sdim["y"]
        ):  # xzy transformation
            rotate = lambda coords: [coords[0], sdim["z"] - coords[2], coords[1]]
            swap = lambda coords: [coords[0], coords[2], coords[1]]

        if (
            dim["x"] == sdim["z"] and dim["y"] == sdim["y"] and dim["z"] == sdim["x"]
        ):  # zyx transformation
            rotate = lambda coords: [sdim["z"] - coords[2], coords[1], coords[0]]
            swap = lambda coords: [coords[2], coords[1], coords[0]]

        if (
            dim["x"] == sdim["z"] and dim["z"] == sdim["y"] and dim["y"] == sdim["x"]
        ):  # yzx transformation
            rotate = lambda coords: [coords[2], coords[0], coords[1]]
            swap = lambda coords: [coords[2], coords[0], coords[1]]

        if (
            dim["x"] == sdim["y"] and dim["y"] == sdim["z"] and dim["z"] == sdim["x"]
        ):  # zxy transformation
            rotate = lambda coords: [coords[1], coords[2], coords[0]]
            swap = lambda coords: [coords[1], coords[2], coords[0]]

        modify_package = lambda package_details: [
            package_details[0],
            rotate(package_details[1]),
            swap(package_details[2]),
        ]
        new_packages = list(map(modify_package, old_packages))

        ### now let gravity take effect

        filter_func = lambda package_details: package_details[1][
            2
        ]  # returns z coordinate of COM
        new_packages.sort(key=filter_func)

        for package_details in new_packages:
            package = package_details[0]
            p_x, p_y, p_z = (
                package_details[2][0],
                package_details[2][1],
                package_details[2][2],
            )
            com_x, com_y = package_details[1][0], package_details[1][1]
            x, y = com_x - p_x / 2, com_y - p_y / 2
            self.drop_package(package, x, y, p_x, p_y, p_z, True)

        self.sorted_dimensions = (
            None  # voiding this characteristic as it should not be used again
        )

    def empty(self):  # removes all packages from ULD
        for lst in self.packages:
            package = lst[0]
            package.placed = False
        self.packages.clear()
        self.remaining_weight_limit = self.weight_limit
        self.remaining_volume = self.volume

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
