import math
from solid import *
from solid.utils import *

from pyMDA.new.core import *

class ScotchYoke(Component):
    
    def __init__(self, config, angle):
        super().__init__()  # This calls the constructor of the parent class (Component)
        self.config = config
        self.angle = angle

    def create(self):

        # add crack
        p = cylinder(d=self.config["stroke_length"] / 2.0, h=self.config["pulley_thickness"], center=True, segments=self.segments_count)

        # add pin
        pin = cylinder(d=self.config["pin_dia"], h=self.config["pin_length"], center=True, segments=self.segments_count)
        d = self.config["stroke_length"] / 4.0 - self.config["pin_dia"] / 2.0
        x = d * math.sin(self.angle)
        y = d * math.cos(self.angle)
        p += translate([x, y, self.config["pin_length"] / 2.0])(pin)
        
        p = translate([0, 0, self.config["pulley_thickness"] / 2.0])(p)

        # add slider
        s = cube([self.config["slider_x_length"], self.config["slider_x_width"], self.config["slider_x_thickness"]], center = True)
        s += rotate(90, [0, 0, 1]) (cube([self.config["slider_y_length"], self.config["slider_y_width"], self.config["slider_y_thickness"]], center = True))
        s -= rotate(90, [0, 0, 1]) (cube([self.config["slider_y_length"] - 2.0, self.config["slider_y_width"] - 2.0, self.config["slider_y_thickness"] + 2.0], center = True))
        s = translate([x, 0, self.config["slider_y_thickness"] / 2.0 + self.config["pulley_thickness"] + 1.1]) (s)
        p += s
    
        return p
