import math
from solid import *
from solid.utils import *

from pyMDA.new.core import *

class Slot(Component):

    def __init__(self, config, use_hull = False):
        super().__init__()
        self.config = config
        self.use_hull = use_hull
        
    def create(self):
    
        hole = translate([0, 0, -(self.config['height'] + 2.0) / 2.0]) (cylinder(segments = self.segments_count,
                                                                                 r = self.config['width'] / 2.0,
                                                                                 h = self.config['height'] + 2.0))

        if self.use_hull:
            p = hull() (
                translate([0, -self.config['length'] / 2.0, 0]) (hole),
                translate([0, self.config['length'] / 2.0, 0]) (hole),
            )
        else:
            p = translate([0, -self.config['length'] / 2.0, 0]) (hole) + \
                translate([0, self.config['length'] / 2.0, 0]) (hole) + \
                cube([self.config['width'], self.config['length'], self.config['height'] + 2], center = True)
            
        return p

class SlotCurve(Component):
    
    def __init__(self, config, use_holes = False):
        super().__init__()
        self.config = config
        self.use_holes = use_holes
    
    def create(self):

        hole = translate([0, 0, -(self.config['height'] + 2.0) / 2.0]) (cylinder(segments = self.segments_count, r = self.config['width'] / 2.0, h = self.config['height'] + 2.0))

        p = []
    
        if self.use_holes:

            y = self.config['radius'] * math.cos(self.config['start_angle'])
            x = self.config['radius'] * math.sin(self.config['start_angle'])
            p += translate([x, y, 0]) (hole)

            y = self.config['radius'] * math.cos(self.config['end_angle'])
            x = self.config['radius'] * math.sin(self.config['end_angle'])
            p += translate([x, y, 0]) (hole)
            
            for a in np.arange(self.config['start_angle'], self.config['end_angle'], self.config['step']):
                y = self.config['radius'] * math.cos(a)
                x = self.config['radius'] * math.sin(a)
                #print (self.config['radius'], x, y, a)
                p += translate([x, y, 0]) (hole)

        else:
        
            p = cylinder(r = self.config['radius'] + self.config['width'] / 2.0, h = self.config['height'] + 2.0, center = True, segments = self.segments_count) - cylinder(r = self.config['radius'] - self.config['width'] / 2.0, h = self.config['height'] + 3.0, center = True, segments = self.segments_count)
        
            p -= rotate(-math.degrees(self.config['start_angle']), [0, 0, 1]) (translate([-(self.config['radius'] + self.config['width']) / 2.0, 0, 0]) (cube([self.config['radius'] + self.config['width'], self.config['radius'] * 2.0 + self.config['width'] * 2.0, self.config['height'] * 2.0], center = True)))
            p -= rotate(-math.degrees(self.config['end_angle']), [0, 0, 1]) (translate([(self.config['radius'] + self.config['width']) / 2.0, 0, 0]) (cube([self.config['radius'] + self.config['width'], self.config['radius'] * 2.0 + self.config['width'] * 2.0, self.config['height'] * 2.0], center = True)))
        
            y = self.config['radius'] * math.cos(self.config['start_angle'])
            x = self.config['radius'] * math.sin(self.config['start_angle'])
            p += translate([x, y, 0]) (hole)
            
            y = self.config['radius'] * math.cos(self.config['end_angle'])
            x = self.config['radius'] * math.sin(self.config['end_angle'])
            p += translate([x, y, 0]) (hole)
        
        return p

class SlotArray(Component):

    def __init__(self, config, use_hull = False):
        super().__init__()
        self.config = config
        self.use_hull = use_hull
        
    def create(self):
        
        gap = (self.config['length'] - self.config['slot_count'] * (self.config['slot_length'] + self.config['slot_width'])) / (self.config['slot_count'] + 1.0)

        y = - self.config['length'] / 2.0 + gap + (self.config['slot_length'] + self.config['slot_width']) / 2.0
        p = translate([0, y, 0]) (Slot(self.config['slot_width'], self.config['slot_length'], self.config['height']).create())
        for i in range(self.config['slot_count'] - 1):
            y += gap + (self.config['slot_length'] + self.config['slot_width'])
            p += translate([0, y, 0]) (Slot(self.config['slot_width'], self.config['slot_length'], self.config['height'], self.use_hull).create())
        return p


class SpeakerGrill(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config
    
    def create(self):

        speaker_hole = cylinder(d = self.config['hole_dia'], h = self.config['wall_thickness'], segments = self.segments_count, center = True)
        
        l = int(self.config['dia'] / 2.0 / self.config['pitch'])
        
        p = speaker_hole

        for j in range(l):
            c = 2 * math.pi * (self.config['pitch'] * j + self.config['pitch'])
            num = int(c / self.config['pitch'])
            angle_diff = 2.0 * math.pi / num
            #print c, num
            angle = 0.0
            for i in range(num):
                x = ((self.config['pitch'] * j) + self.config['pitch']) * math.cos(angle)
                y = ((self.config['pitch'] * j) + self.config['pitch']) * math.sin(angle)
                p += translate([x, y, 0]) (speaker_hole)
                #print angle, x, y
                angle += angle_diff

        return p
