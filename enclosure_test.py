from solid import *
from solid.utils import *
from cots import *
from helpers import *
from settings_common import *
from enclosure_helpers import *
import math

wall_thickness = 2.0
draft_angle = math.radians(1.5)
#draft_angle = math.radians(5.0)
#draft_angle = math.radians(0.0)
height = 20
length = 20
curve_radius = 4.0 # must be > wall_thickness * 2.0

from new import *

e = enclosure_edge(height, wall_thickness, curve_radius, draft_angle, segments_count)

ct = enclosure_corner_top(wall_thickness, curve_radius, draft_angle, height, segments_count)

cb = enclosure_corner_bottom(wall_thickness, curve_radius, draft_angle, height, segments_count)

f = enclosure_face(height, length, wall_thickness, curve_radius, draft_angle)

p = e + cb + ct + f
#p = e + f

print(scad_render(p))
exit()

s = l + mirror([1, 0, 0]) (l)

a = s + mirror([0, 1, 0]) (s)

p = a

p += enclosure_face(height, 10, wall_thickness, draft_angle)

print(scad_render(p))
