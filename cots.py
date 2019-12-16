from solid import *
from solid.utils import *
from settings_common import *

def stepper_driver():
    return translate([-86.0 / 2.0, -55.0 / 2.0, -20.0 / 2.0]) (
        cube([86, 55, 20])
    )

def stepper(nema_type = 17, length = 24, segments_count = None):

    if nema_type == 17:
        width = 42
        bore = 5
        bore_length = 24
        mounting_hole_pitch = 31
        mounting_hole_size = m3_tap_hole_size
        mounting_hole_depth = 4
    else:
        print ("TODO: NEMA TYPE NOT DEFINED")
        
    block = cube([width, length, width], center = True)
    axle = cylinder(d = bore, h = bore_length, segments = segments_count)
    mounting_hole = cylinder(d = mounting_hole_size, h = mounting_hole_depth + 1, segments = segments_count)

    mounting_holes = translate([mounting_hole_pitch / 2.0, 1, mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
                     translate([mounting_hole_pitch / 2.0, 1, -mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
                     translate([-mounting_hole_pitch / 2.0, 1, mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
                     translate([-mounting_hole_pitch / 2.0, 1, -mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole))
                     
    
    p = translate([0, -length / 2.0, 0]) (block) + \
        rotate(90 + 180, [1, 0, 0]) (axle) - \
        mounting_holes
    
    return color(BlackPaint) (p)

def pulley(angle = 0):
    return rotate(angle, [1, 0, 0]) (
        translate([-6.95, -7, -7]) (
            color(Aluminum) (
                import_stl("cots/GT2_16T.STL")
            )
        )
    )

def stepper_and_pulley(angle = 0, nema_type = 17, length = 24, segments_count = None):
    return union()(
        stepper(nema_type, length, segments_count),
        translate([0, 13, 0]) (
            rotate(-270, [0, 0, 1]) (
                pulley(angle)
            )
        )
    )

def bearing(id, od, thickness):
    outter = cylinder(d = od, h = thickness)
    inner = cylinder(d = id, h = thickness + 2)
    p = outter - translate([0, 0, -1]) (inner)
    return p
