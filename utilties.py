import math
from solid import *
from solid.utils import *
from solid.solidpython import scad_render_to_file

def matrix_copy_simple(part, x_pitch, y_pitch, x_count, y_count):

    p = part

    x = 0
    y = 0
    for j in range(y_count):
        x = 0
        p += translate([x, y, 0]) (part)
        for i in range(x_count - 1):
            x += x_pitch
            p += translate([x, y, 0]) (part)
        y += y_pitch

    return p

# TODO: remove this and merge to matrix_copy_simple
def matrix_copy(feature, part, space, x_length, y_length, x_count, y_count):
    
    x_gap = (x_length - x_count * space) / (x_count + 1.0)
    y_gap = (y_length - y_count * space) / (y_count + 1.0)

    p = part

    y = - y_length / 2.0 + y_gap + space / 2.0
    for j in range(y_count):
        x = - x_length / 2.0 + x_gap + space / 2.0
        p += translate([x, y, 0]) (feature)
        for i in range(x_count - 1):
            x += x_gap + space
            p += translate([x, y, 0]) (feature)
        y += y_gap + space

    return p
