import math
from solid import *
from solid.utils import *

from pyMDA.new.core import *

class Collar(Component):

    def __init__(self, config, gap_closed):
        super().__init__()
        self.config = config
        self.gap_closed = gap_closed
    
    def create(self):

        od = self.config['id'] + self.config['thickness'] * 2.0

        # process gap_closed - i.e. reduce the connection gap, which will also reduce the collar radius
        self.config['connection_gap'] -= self.gap_closed
        C = 2.0 * math.pi * (od / 2.0) - self.gap_closed
        od = C / (2.0 * math.pi) * 2.0
        self.config['id'] = od - self.config['thickness'] * 2.0

        connection_width = self.config['connection_thickness'] * 2.0 + self.config['connection_gap']
    
        co = cylinder(d = od, h = self.config['width'], segments = self.segments_count, center = True)

        cc = rotate(90, [0, 1, 0]) (cylinder(d = self.config['width'], h = connection_width, segments = self.segments_count, center = True))
        s = hull() (
            cc,
            translate([0, od / 2.0 + self.config['width'] / 2.0 + self.config['connection_height'], 0]) (cc)
        )
    
        # cuts
        ci_cut = cylinder(d = self.config['id'], h = self.config['width'] + 2, segments = self.segments_count, center = True)
        cc_cut = cube([self.config['connection_gap'], od / 2.0 + self.config['width'] + self.config['connection_height'] + 1.0, self.config['width'] + 2])
        hole = cylinder(d = self.config['connection_hole_dia'], h = connection_width + 2, segments = self.segments_count)
    
        p = co + \
            s - \
            ci_cut - \
            translate([-self.config['connection_gap'] / 2.0, 0, -self.config['width'] / 2.0 - 1]) (cc_cut) - \
            translate([-connection_width / 2.0 - 1, od / 2.0 + self.config['connection_height'] - connection_width / 2.0, 0]) (rotate(90, [0, 1, 0]) (hole))
        
        p = co + s - ci_cut - \
            translate([-self.config['connection_gap'] / 2.0, 0, -self.config['width'] / 2.0 - 1]) (cc_cut) - \
            translate([-connection_width / 2.0 - 1, od / 2.0 + self.config['width'] / 2.0 + self.config['connection_height'], 0]) (rotate(90, [0, 1, 0]) (hole))
    
        return p
