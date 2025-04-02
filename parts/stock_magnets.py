import math
from solid import *
from solid.utils import *

from pyMDA.new.core import *

class MagnetCoin(Component):

    def __init__(self, dia, thickness):
        super().__init__()
        self.dia = dia
        self.thickness = thickness
    
    def create(self):
        p = cylinder(d = self.dia, h = self.thickness, center = True, segments = self.segments_count)
        p = translate([0, 0, self.thickness / 2.0]) (p)
        return p
