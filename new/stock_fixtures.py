import math
from solid import *
from solid.utils import *
from core import *

class FixtureCounterSunk(Component):
    ''' https://image.pushauction.com/0/0/f2c27552-fb37-436a-9369-5b4293c5087b/eda41698-7b80-41de-b5b8-98625f130e93.jpg '''
    def __init__(self, d, dk, L, a):
        super().__init__()
        self.d = d
        self.dk = dk
        self.L = L
        self.a = a

    def create(self):
        angle = (math.radians(180) - self.a) / 2.0
        countersunk_h = math.tan(angle) * self.dk / 2.0
        p = cylinder(d1 = self.dk, d2 = 0, h = countersunk_h, segments = self.segments_count, center = False) + \
            cylinder(d = self.d, h = self.L, segments = self.segments_count, center = False)
        return p

    def clearance(self, clearance):
        # NOTE: still need to pass through the clearance hole size for 'd', otherwise everything is automatic based on countersunk dimensions
        angle = (math.radians(180) - self.a) / 2.0
        dk = self.dk + clearance * 2.0
        countersunk_h = math.tan(angle) * dk / 2.0 + 1.0
        dk2 = countersunk_h / math.tan(angle) * 2.0
        return fixture_countersunk(self.d, self.dk2, self.L + 2.0, self.a, segments_count)
    
class FixtureSocket(Component):
    ''' https://ae01.alicdn.com/kf/HTB1hoF9LVXXXXczXXXXq6xXFXXXt/222055624/HTB1hoF9LVXXXXczXXXXq6xXFXXXt.jpg '''
    def __init__(self, d, dk, L, k):
        super().__init__()
        self.d = d
        self.dk = dk
        self.L = L
        self.k = k

    def create(self):
        p = cylinder(d = self.d, h = self.L + self.k, segments = self.segments_count, center = False) + \
            cylinder(d = self.dk, h = self.k, segments = self.segments_count, center = False)
        return p

class Washer(Component):
    
    def __init__(self, dia, hole_dia, thickness, is_center = True):
        super().__init__()
        self.dia = dia
        self.hole_dia = hole_dia
        self.thickness = thickness
        self.is_center = is_center
        
    def create(self):
        rod = cylinder(segments = self.segments_count, d = self.dia, h = self.thickness, center = self.is_center)
        hole = cylinder(segments = self.segments_count, d = self.hole_dia, h = self.thickness + 2, center = self.is_center)
        if self.is_center:
            return rod - translate([0, 0, 0]) (hole)
        else:
            return rod - translate([0, 0, -1]) (hole)
