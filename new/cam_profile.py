import math
import numpy as np

from solid import *
from solid.utils import *

from core import *

class CamProfile(Component):
    
    def __init__(self, config):        
        super().__init__()
        self.config = config
        
    def create(self):
        points = []
        angle_range = self.config["end_angle"] - self.config["start_angle"]
        radius_step = (self.config["end_radius"] - self.config["start_radius"]) / (angle_range / self.config["increment"])
        radius = self.config["start_radius"]
        for i in np.arange(self.config["start_angle"], self.config["end_angle"], self.config["increment"]):
            x = radius * math.cos(i)
            y = radius * math.sin(i)
            pt = [x, y]
            points.append(pt)
            radius += radius_step
        return linear_extrude(self.config["height"], center = self.config["is_center"]) (polygon(points=points))

    def find_radius(target_angle):

        # TODO: this could/should be replaced with a single equation - can't think of the solution right now.
        
        angle_range = self.config["end_angle"] - self.config["start_angle"]
        
        radius_step = (self.config["end_radius"] - self.config["start_radius"]) / (angle_range / self.config["increment"])
        
        # self.config["end_angle"] + 1deg is required to complete the loop
        radius = self.config["start_radius"]
        for i in np.arange(self.config["start_angle"], self.config["end_angle"] + math.radians(1.0), self.config["increment"]):
            #print ("i=%f(%fdeg) radius_step=%f self.config["start_angle"]=%f(%fdeg) self.config["end_angle"]=%f(%fdeg) target_angle=%f(%fdeg) radius=%f" % \
                #       (i, math.degrees(i), radius_step, self.config["start_angle"], math.degrees(self.config["start_angle"]), self.config["end_angle"], math.degrees(self.config["end_angle"]), target_angle, math.degrees(target_angle), radius))
            if round(math.degrees(i)) == round(math.degrees(target_angle)):
                return radius
            radius += radius_step

        return False
