import math
from solid import *
from solid.utils import *

from core import *
from stock_fixtures import *

class Boss(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def create(self):
        return Washer(self.config['dia'], self.config['hole_dia'], self.config['thickness']).create()

class BossPlate(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config
    
    def create(self):

        plate = cube([self.config['length'], self.config['width'], self.config['thickness']], center = True)
        rod = cylinder(segments = self.segments_count, d = self.config['dia'], h = self.config['height'], center = True)
        hole = cylinder(segments = self.segments_count, d = self.config['hole_dia'], h = self.config['height'] + self.config['thickness'] + 2, center = True)

        p = plate + \
            translate([0, 0, self.config['height'] / 2.0 + self.config['thickness'] / 2.0]) (rod) - \
            translate([0, 0, (self.config['height'] + self.config['thickness'] + 2) / 2.0 - self.config['thickness'] / 2.0 - 1]) (hole)
        
        if self.config['mounting_hole_dia'] > 0:
            mounting_hole = cylinder(segments = self.segments_count,
                                     d = self.config['mounting_hole_dia'],
                                     h = self.config['thickness'] + 2,
                                     center = True)
            mounting_holes = translate([self.config['length'] / 3.0, 0, 0]) (mounting_hole) + \
                         translate([-self.config['length'] / 3.0, 0, 0]) (mounting_hole)
            p -= mounting_holes

        p = translate([0, 0, self.config['thickness'] / 2.0]) (p)
        
        return p

class BossPlateDual(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):

        plate = cube([self.config['length'], self.config['width'], self.config['thickness']], center = True)
        rod = cylinder(segments = self.segments_count, d = self.config['dia'], h = self.config['height'], center = True)
        hole = cylinder(segments = self.segments_count, d = self.config['hole_dia'], h = self.config['height'] + self.config['thickness'] + 2, center = True)

        p = plate + \
            translate([-self.config['pitch'] / 2.0, 0, self.config['height'] / 2.0 + self.config['thickness'] / 2.0]) (rod) + \
            translate([self.config['pitch'] / 2.0, 0, self.config['height'] / 2.0 + self.config['thickness'] / 2.0]) (rod) - \
            translate([-self.config['pitch'] / 2.0, 0, (self.config['height'] + self.config['thickness'] + 2) / 2.0 - self.config['thickness'] / 2.0 - 1]) (hole) - \
            translate([self.config['pitch'] / 2.0, 0, (self.config['height'] + self.config['thickness'] + 2) / 2.0 - self.config['thickness'] / 2.0 - 1]) (hole)
        
        if self.config['mounting_hole_dia'] > 0:
            mounting_hole = cylinder(segments = self.segments_count, d = self.config['mounting_hole_dia'], h = self.config['thickness'] + 2, center = True)
            mounting_holes = translate([self.config['length'] / 3.0, 0, 0]) (mounting_hole) + \
                translate([-self.config['length'] / 3.0, 0, 0]) (mounting_hole)
            p -= mounting_holes
            
        p = translate([0, 0, self.config['thickness'] / 2.0]) (p)
        
        return p

class RubberButton(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):

        main = cylinder(r = self.config['radius'], h = self.config['length'], segments = self.segments_count)
        support = cylinder(r = self.config['support_radius'], h = self.config['support_length'], segments = self.segments_count)
        p = main + support
        return p

class LightpipeStraight(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        main = cylinder(r = self.config['radius'], h = self.config['length'] - self.config['support_offset'] - self.config['support_length'], segments = self.segments_count)
        
        support = cylinder(r = self.config['support_radius'], h = self.config['support_length'], segments = self.segments_count)
        
        head = cylinder(r = self.config['head_radius'], h = self.config['support_offset'], segments = self.segments_count)
        
        p = head + translate([0, 0, self.config['support_offset']]) (support) + \
            translate([0, 0, self.config['support_offset'] + self.config['support_length']]) (main)
        
        return p
