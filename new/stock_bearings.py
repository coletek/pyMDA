import math
from solid import *
from solid.utils import *
from core import *

class Bearing(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        outter = cylinder(d = self.config["od"], h = self.config["thickness"], segments = self.segments_count)
        inner = cylinder(d = self.config["id"], h = self.config["thickness"] + 2, segments = self.segments_count)
        p = outter - translate([0, 0, -1]) (inner)
        return p

class BearingPillowBlockUCP201(Component):
    '''@bom_part("Bearing Pillow Block (UCP201)", 22.42, 'A$')'''
    def create(self):
        return color(BlackPaint) (rotate(90, [0, 1, 0]) (rotate(90, [0, 0, 1]) (translate([102.9, -77.5, -169.0]) (import_stl("cots/ucp201.stl")))))

class BearingPillowBlockUCP204(Component):
    '''@bom_part("Bearing Pillow Block (UCP204)", 27.19, 'A$')'''
    def create(self):
        return color(BlackPaint) (import_stl("cots/ucp204.stl"))

class Bearing2BoltFlangeUCFL204(Component):
    '''@bom_part("Bearing 2 Bolt Flange (UCFL204)", 19.76, 'A$')'''
    def create(self):
        return color(BlackPaint) (import_stl("cots/ucfl204.stl"))
