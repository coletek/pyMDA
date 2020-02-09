from solid import *
from solid.utils import *
import math

def enclosure_face(height, length, wall_thickness, curve_radius, draft_angle):

    wall = translate([-length, -wall_thickness / 2.0, 0]) (cube([length, wall_thickness, height]))

    p = rotate(-math.degrees(draft_angle), [1, 0, 0]) (wall)

    d = math.tan(draft_angle) * height

    p = translate([(-curve_radius + d + wall_thickness / 2.0), 0, 0]) (p)
    
    return p

# for bottom undrafted corner
def enclosure_corner_top(wall_thickness, curve_radius, draft_angle, height, segments_count):

    o = sphere(r = curve_radius, segments = segments_count)

    i = sphere(r = curve_radius - wall_thickness, segments = segments_count)

    p = o - i

    aoi = translate([0, 0, -curve_radius - 1]) (cube([curve_radius + 1, curve_radius + 1, curve_radius + 1]))

    p = intersection() (aoi, p)

    p = translate([(-curve_radius + wall_thickness / 2.0), (-curve_radius + wall_thickness / 2.0), 0]) (p)

    d = math.tan(draft_angle) * height
    
    p = translate([d, d, height]) (mirror([0, 0, 1]) (p))

    return p

def enclosure_corner_bottom(wall_thickness, curve_radius, draft_angle, height, segments_count):

    d = math.tan(draft_angle) * height
    
    o = sphere(r = curve_radius - d, segments = segments_count)

    i = sphere(r = curve_radius - d - wall_thickness, segments = segments_count)

    p = o - i

    aoi = translate([0, 0, -curve_radius - 1]) (cube([curve_radius + 1, curve_radius + 1, curve_radius + 1]))

    p = intersection() (aoi, p)

    p = translate([(-curve_radius + d + wall_thickness / 2.0), (-curve_radius + d + wall_thickness / 2.0), 0]) (p)

    return p

def enclosure_edge(height, wall_thickness, curve_radius, draft_angle, segments_count):

    # e.g.
    #wall_thickness = 2.0
    #draft_angle = math.radians(1.5)
    #height = 20
    #curve_radius = 4.0
    
    d = math.tan(draft_angle) * height
    
    edge_o = cylinder(h = height, r1 = curve_radius - d, r2 = curve_radius, center = True, segments = segments_count)

    edge_i = cylinder(h = height + 2, r1 = curve_radius - d - wall_thickness, r2 = curve_radius - wall_thickness, center = True, segments = segments_count)
    
    aoi = translate([0, 0, -height / 2.0 - 1]) (cube([curve_radius, curve_radius, height + 2]))
    
    full = edge_o - edge_i

    offset = -curve_radius + wall_thickness / 2.0 + d
    
    p = translate([offset, offset, height / 2.0]) (intersection() (aoi, full))

    return p
