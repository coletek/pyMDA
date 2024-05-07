import math
from solid import *
from solid.utils import *
from core import *

class SHS(Component):
    
    def __init__(self, width, thickness, length = 100, end1_cut_angle = 0.0, end2_cut_angle = 0.0):
        self.width = width
        self.length = length
        self.height = thickness
        self.thickness = thickness
        self.end1_cut_angle = end1_cut_angle
        self.end2_cut_angle = end2_cut_angle
        
    def create(self):
        # works for -45 and 45.0
        # TODO: make work for any angle
    
        p = cube([self.width, self.length, self.width], center = True) - cube([self.width - self.thickness, self.length + 2, self.width - self.thickness], center = True)

        if self.end1_cut_angle != 0:
            l = math.sqrt(2 * (self.width) * (self.width))
            if self.end1_cut_angle < 0:
                c = translate([0, 0, -(self.width) / 2.0]) (rotate(self.end1_cut_angle, [1, 0, 0]) (cube([self.width + 2, l, l], center = True)))
            else:
                c = translate([0, 0, (self.width) / 2.0]) (rotate(self.end1_cut_angle, [1, 0, 0]) (cube([self.width + 2, l, l], center = True)))
            p -= translate([0, self.length / 2.0, 0]) (c)

        if self.end2_cut_angle != 0:
            l = math.sqrt(2 * (self.width) * (self.width))
            if self.end2_cut_angle < 0:
                c = translate([0, 0, -(self.width) / 2.0]) (rotate(self.end2_cut_angle, [1, 0, 0]) (cube([self.width + 2, l, l], center = True)))
            else:
                c = translate([0, 0, (self.width) / 2.0]) (rotate(self.end2_cut_angle, [1, 0, 0]) (cube([self.width + 2, l, l], center = True)))
            p -= translate([0, -self.length / 2.0, 0]) (c)

        p = color(Aluminum) (p)

        return p

class CS(Component):
    
    def __init__(self, width, thickness, length):
        self.width = width
        self.length = length
        self.height = thickness
        self.thickness = thickness
        
    def create(self):
        p = cube([self.width, self.length, self.width], center = True) - \
            translate([-0.5 - self.thickness, 0, 0]) (cube([self.width + 1, self.length + 2, self.width - self.thickness * 2.0], center = True))
        p = color(Aluminum) (p)
        return p

class LS(Component):
    
    def __init__(self, width, height, thickness, length):
        self.width = width
        self.length = length
        self.height = height
        self.thickness = thickness
        
    def create(self):
        p = cube([self.width, self.length, self.height], center = True) - translate([-0.5 - self.thickness, 0, -0.5 - self.thickness]) (cube([self.width + 1, self.length + 2, self.height + 1], center = True))
        p = color(Aluminum) (p)
        return p

class SB(Component):
    
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.height = width

    def create(self):
        p = cube([self.width, self.length, self.width], center = True)
        p = color(Aluminum) (p)
        return p

class Rod(Component):
    
    def __init__(self, dia, length, segments_count = 100):
        self.width = dia
        self.length = dia
        self.height = length
        self.segments_count = segments_count
        self.dia = dia

    def create(self):
        return color(Aluminum) (cylinder(d = self.dia, h = self.height, center = True, segments = self.segments_count))

class Sheet(Component):

    def __init__(self, width = 600, length = 2400, thickness = 1.2):
        self.width = width
        self.length = length
        self.height = thickness
        self.thickness = thickness

    def create(self):
        p = cube([self.width, self.length, self.thickness], center = True)
        p = color(Aluminum) (p)
        return p

class Wedge(Component):

    def __init__(self, r, h, sa, ea, segments_count = 100):
        self.width = r
        self.length = r
        self.height = h
        self.r = r
        self.h = h
        self.sa = sa
        self.ea = ea
        self.segments_count = segments_count
        # TODO make work for larger then 180deg

    def create(self):
    
        c = cylinder(r = self.r, h = self.h, center = True, segments = self.segments_count)

        l = self.r * 2.0 + 2.0
        cut = cube([l, l, self.h + 2.0], center = True)

        p = c - \
            rotate(math.degrees(self.sa), [0, 0, 1]) (translate([0, -l / 2.0, 0]) (cut)) - \
            rotate(math.degrees(self.ea) + 180, [0, 0, 1]) (translate([0, -l / 2.0, 0]) (cut))
    
        return p

class Hinge(Component):

    def __init__(self, d, axle_d, h, hinge_segments, l, tolerance, is_left, segments_count = 100):
        self.width = h
        self.length = h
        self.height = h
        self.d = d
        self.axle_d = d
        self.h = h
        self.hinge_segments = hinge_segments
        self.l = l
        self.tolerance = tolerance
        self.is_left = is_left
        self.segments_count = segments_count
    
    def create(self):

        c = cylinder(d = self.d, h = self.h, center = True, segments = self.segments_count)
        axle = cylinder(d = self.axle_d + self.tolerance, h = self.h + 2.0, center = True, segments = self.segments_count)
        a = cube([self.l, self.d / 2.0, self.h], center = True)

        cc_h = self.h / self.hinge_segments
        cc = cylinder(d = self.d + self.tolerance * 2.0, h = cc_h + self.tolerance * 2.0, center = True, segments = self.segments_count)

        offset = self.d / 4.0
        if self.is_left:
            offset = -offset
        p = translate([self.l / 2.0, offset, 0]) (a)

        p += c    
        if self.is_left:
            start_idx = 0
        else:
            start_idx = 1

        # odd set
        for i in range(start_idx, self.hinge_segments, 2):
            p -= translate([0, 0, -self.h / 2.0 + cc_h / 2.0 + cc_h * i]) (cc)

        p -= axle
     
        return p

class Door(Component):

    def __init__(self, config):
        self.config = config
        
    def door(self):
        p = cube([self.config['width'], self.config['thickness'], self.config['height']], center = True)
        p = translate([0, 0, self.config['height'] / 2.0]) (p) 
        p = color(Oak) (p)
        return p
