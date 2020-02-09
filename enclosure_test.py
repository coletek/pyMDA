from solid import *
from solid.utils import *
from cots import *
from helpers import *
from settings_common import *
from enclosure_helpers import *
import math

CubePoints = [
  [  0,  0,  0 ],  #0
  [ 10,  0,  0 ],  #1
  [ 10,  7,  0 ],  #2
  [  0,  7,  0 ],  #3
  [  0,  0,  5 ],  #4
  [ 10,  0,  5 ],  #5
  [ 10,  7,  5 ],  #6
  [  0,  7,  5 ]] #7
  
CubeFaces = [
  [0,1,2,3],  # bottom
  [4,5,1,0],  # front
  [7,6,5,4],  # top
  [5,6,2,1],  # right
  [6,7,3,2],  # back
  [7,4,0,3]] # left
  
p = polyhedron(CubePoints, CubeFaces);

#pts = []

#p =

c = cube([10, 10, 10])

p = minkowski()(p, sphere(r=2, segments=segments_count)) - c

p = minkowski()(p, sphere(r=2, segments=segments_count))

# better way

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
