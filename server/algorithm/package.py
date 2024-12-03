import json


class Package(object):

    def __init__(
        self, name, dimensions, weight, delay_cost, is_priority
    ):  # dimensions is a tuple, delay cost can be anything (non integer implies priority)
        self.name = name
        dimensions = sorted(
            dimensions
        )  # since only coordinates matter, we can take x,y,z to be whatever we want within length,width,height. Nomenclature isn't important, unlike in ULDs.
        self.dimensions = {"x": dimensions[2], "y": dimensions[1], "z": dimensions[0]}
        self.weight = weight
        self.delay_cost = (
            delay_cost  # if this value is not a number, it is a priority package
        )
        self.volume = self.dimensions["x"] * self.dimensions["y"] * self.dimensions["z"]
        self.density = self.weight / self.volume
        self.placed = False  # becomes True if package is placed inside a ULD
        self.is_priority = is_priority

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
