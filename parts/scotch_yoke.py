import math
from solid import *
from solid.utils import *

from pyMDA.parts.core import *
from pyMDA.parts.plates import *

class ScotchYoke(Component):
    
    def __init__(self, config, angle):
        super().__init__()  # This calls the constructor of the parent class (Component)
        self.config = config
        self.angle = angle

    def create(self):

        # add crank
        p = cylinder(d=self.config["stroke_length"] + self.config['pin_dia'], h=self.config["pulley_thickness"], center=True, segments=self.segments_count)

        # add pin
        pin = cylinder(d=self.config["pin_dia"], h=self.config["pin_length"], center=True, segments=self.segments_count)
        d = self.config["stroke_length"] / 2.0 #- self.config["pin_dia"] / 2.0
        x = d * math.sin(self.angle)
        y = d * math.cos(self.angle)
        p += translate([x, y, self.config["pin_length"] / 2.0])(pin)

        #p += translate([0, 0, -self.config["pin_length"] / 2.0])(pin)
        p -= translate([0, 0, 0])(pin)
        
        p = translate([0, 0, self.config["pulley_thickness"] / 2.0 + self.config["crank_height"]])(p)

        # add connecting rod
        r = translate([self.config['slider_length_fwd'] / 2.0, 0, 0]) (rotate(90, [0, 1, 0]) (cylinder(d=self.config['slider_thickness'], h=self.config['slider_length_fwd'], center = True, segments = self.segments_count)))
        r += translate([-self.config['slider_length_rev'] / 2.0, 0, 0]) (rotate(90, [0, 1, 0]) (cylinder(d=self.config['slider_thickness'], h=self.config['slider_length_rev'], center = True, segments = self.segments_count)))
        r -= translate([28, 0, 0]) (cube([10, 0.5, 10], center = True))
        

        # add sliding rod
        sliding_rod_thickness = 2.0
        o = cylinder(d=self.config["slider_pin_dia"] + sliding_rod_thickness * 2.0, h=self.config['slider_thickness'], center = True, segments = self.segments_count)
        i = cylinder(d=self.config["slider_pin_dia"], h=self.config['slider_thickness'] + self.config['slider_thickness']  , center = True, segments = self.segments_count)
        o = hull()(translate([0, self.config['stroke_length'] / 2.0, 0]) (o),
                   translate([0, -self.config['stroke_length'] / 2.0, 0]) (o))

        i = hull()(translate([0, self.config['stroke_length'] / 2.0, 0]) (i),
                   translate([0, -self.config['stroke_length'] / 2.0, 0]) (i))
        s = r + o - i
        
        s = translate([x, 0, self.config["slider_thickness"] / 2.0 + self.config["pulley_thickness"] + self.config['sleeve_clearance']]) (s)
        p += s
        
        # add sleeve
        self.config['sleeve'] = { "width": self.config["sleeve_thickness"],
                                  "dia": self.config["sleeve_id"],
                                  "wall_thickness": self.config["sleeve_thickness"] / 3.0,
                                  "pitch": self.config["pulley_thickness"] + self.config['sleeve_clearance'] + self.config["slider_thickness"] / 2.0
                                 }
        x = self.config['stroke_length'] / 2.0 + self.config['pin_dia'] / 2.0 + self.config["sleeve"]["width"] / 2.0 + 0.4 + sliding_rod_thickness + 0.4 + self.config['clearance']

        p += translate([x, 0, 0]) (PlummerBlock(self.config['sleeve']).create())
        p += translate([-x, 0, 0]) (PlummerBlock(self.config['sleeve']).create())
        
        
        p = color(self.color) (p)
        
        return p
