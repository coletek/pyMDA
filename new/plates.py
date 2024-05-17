import math
from solid import *
from solid.utils import *

from pyMDA.new.core import *

class PlateWithMountingHoles(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        b = cube([self.config['width'], self.config['length'], self.config['thickness']], center = True)
        
        h = cylinder(d = self.config['mounting_hole_dia'], h = self.config['thickness'] + 2.0, segments = self.segments_count, center = True)
        
        hh = translate([self.config['mounting_hole_pitch_width'] / 2.0, self.config['mounting_hole_pitch_length'] / 2.0, 0]) (h) + \
            translate([-self.config['mounting_hole_pitch_width'] / 2.0, self.config['mounting_hole_pitch_length'] / 2.0, 0]) (h) + \
            translate([self.config['mounting_hole_pitch_width'] / 2.0, -self.config['mounting_hole_pitch_length'] / 2.0, 0]) (h) + \
            translate([-self.config['mounting_hole_pitch_width'] / 2.0, -self.config['mounting_hole_pitch_length'] / 2.0, 0]) (h)
        
        hh = translate([self.config['mounting_hole_offset_width'], self.config['mounting_hole_offset_length'], 0]) (hh)
    
        p = b - hh
        
        return p

class PlateWithMountingHolesEdges(Component):
    ''' TODO: perhaps z should be thickness'''
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):

        p = translate([-self.config['thickness'] / 2.0, -self.config['width'] / 2.0, -self.config['height'] / 2.0]) (
            cube([self.config['thickness'], self.config['width'], self.config['height']])
        )
        
        distance = self.config['thickness'] / 2.0
        
        if self.config['top_mounting_hole_depth'] > 0:

            depth = self.config['top_mounting_hole_depth']
            
            bolt_hole1 = translate([0, self.config['width'] / 2.0 - distance, self.config['height'] / 2.0 - depth - 1]) (
                rotate(90, [0, 0, 1]) (
                    cylinder(h = depth + 2, d = self.config['mounting_hole_size'], segments = self.segments_count)
                )
            )
            bolt_hole2 = translate([0, - self.config['width'] / 2.0 + distance, self.config['height'] / 2.0 - depth - 1]) (
                rotate(90, [0, 0, 1]) (
                    cylinder(h = depth + 2, d = self.config['mounting_hole_size'], segments = self.segments_count)
                )
            )
            
            p = p - bolt_hole1 - bolt_hole2
        
        if self.config['bottom_mounting_hole_depth'] > 0:
            
            depth = self.config['bottom_mounting_hole_depth']
            
            bolt_hole3 = translate([0, self.config['width'] / 2.0 - distance, - self.config['height'] / 2.0 - 1]) (
                rotate(90, [0, 0, 1]) (
                    cylinder(h = depth + 2, d = self.config['mounting_hole_size'], segments = self.segments_count)
                )
            )
            bolt_hole4 = translate([0, - self.config['width'] / 2.0 + distance, - self.config['height'] / 2.0 - 1]) (
                rotate(90, [0, 0, 1]) (
                    cylinder(h = depth + 2, d = self.config['mounting_hole_size'], segments = self.segments_count)
                )
            )

            p = p - bolt_hole3 - bolt_hole4
                
        return p

class PlateWithFillets(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config
    
    def create(self):

        # could be done with hull(), but done this way to support FreeCAD STEP exporting

        x = self.config['width'] - self.config['fillet_radius'] * 2.0
        y = self.config['length'] - self.config['fillet_radius'] * 2.0

        p = []
    
        if x != 0:
            p += cube([x, self.config['length'], self.config['thickness']], center = True)

        if y != 0:
            p += cube([self.config['width'], y, self.config['thickness']], center = True)
    
        f = cylinder(r = self.config['fillet_radius'], h = self.config['thickness'], center = True, segments = self.segments_count)
        p += translate([x / 2.0, y / 2.0, 0]) (f) + \
            translate([x / 2.0, -y / 2.0, 0]) (f) + \
            translate([-x / 2.0, y / 2.0, 0]) (f) + \
            translate([-x / 2.0, -y / 2.0, 0]) (f)

        return p

class PlummerBlock(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):

        c = cube([self.config["width"], self.config['dia'] + self.config['wall_thickness'] * 2.0, self.config['pitch']], center = True)
        cc = cylinder(d=self.config["dia"] + self.config['wall_thickness'] * 2.0, h = self.config["width"], center = True, segments = self.segments_count)
        h = cylinder(d=self.config["dia"], h=self.config["width"] + 2.0, center = True, segments = self.segments_count)
        
        d = self.config["pitch"]
        p = hull() (translate([0, 0, self.config["pitch"] / 2.0]) (c),
                    translate([0, 0, d]) (rotate(90, [0, 1, 0]) (cc)))

        p -= translate([0, 0, d]) (rotate(90, [0, 1, 0]) (h))

        return p
