import math
from solid import *
from solid.utils import *

from pyMDA.parts.core import *

Gears = import_scad("pyMDA/cots/gears/gears.scad")

class GearSpur(Component):
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        return Gears.spur_gear(modul=self.config["modul"],
                               tooth_number=self.config["tooth_number"],
                               width=self.config["width"],
                               bore=self.config["bore"],
                               pressure_angle=self.config["pressure_angle"],
                               helix_angle=self.config["helix_angle"],
                               optimized=self.config["is_optimized"]);

class GearHerringbone(Component):
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        return Gears.herringbone_gear(modul=self.config["modul"],
                                      tooth_number=self.config["tooth_number"],
                                      width=self.config["width"],
                                      bore=self.config["bore"],
                                      pressure_angle=self.config["pressure_angle"],
                                      helix_angle=self.config["helix_angle"],
                                      optimized=self.config["is_optimized"]);
