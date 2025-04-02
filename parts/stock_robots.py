import math
from solid import *
from solid.utils import *

from pyMDA.parts.core import *

class RobotCartesianGantry(Component):
    ''' https://www.alibaba.com/product-detail/3-axis-linear-stage-like-the_62184209284.html '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):

        p = rotate(-90, [0, 0, 1]) (translate([-90, 165, 0]) (rotate(90, [1, 0, 0]) (import_stl("cots/robots/SW40XYZ-L(X400Y550Z100)_with_brake.stl"))))

        p = color(Aluminum) (p)
        
        return p
