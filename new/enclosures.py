def boss(dia, hole_dia, thickness, segments_count, is_center = True):
    return washer(dia, hole_dia, thickness, segments_count, is_center)
    
def boss_plate(width, length, thickness, mounting_hole_dia, dia, hole_dia, height, segments_count):

    plate = cube([length, width, thickness], center = True)
    rod = cylinder(segments = segments_count, d = dia, h = height, center = True)
    hole = cylinder(segments = segments_count, d = hole_dia, h = height + thickness + 2, center = True)

    p = plate + \
        translate([0, 0, height / 2.0 + thickness / 2.0]) (rod) - \
        translate([0, 0, (height + thickness + 2) / 2.0 - thickness / 2.0 - 1]) (hole)
    
    if mounting_hole_dia > 0:
        mounting_hole = cylinder(segments = segments_count, d = mounting_hole_dia, h = thickness + 2, center = True)
        mounting_holes = translate([length / 3.0, 0, 0]) (mounting_hole) + \
                         translate([-length / 3.0, 0, 0]) (mounting_hole)
        p -= mounting_holes

    p = translate([0, 0, thickness / 2.0]) (p)
        
    return p

def boss_dual_plate(width, length, thickness, mounting_hole_dia, dia, hole_dia, height, pitch, segments_count):

    plate = cube([length, width, thickness], center = True)
    rod = cylinder(segments = segments_count, d = dia, h = height, center = True)
    hole = cylinder(segments = segments_count, d = hole_dia, h = height + thickness + 2, center = True)

    p = plate + \
        translate([-pitch / 2.0, 0, height / 2.0 + thickness / 2.0]) (rod) + \
        translate([pitch / 2.0, 0, height / 2.0 + thickness / 2.0]) (rod) - \
        translate([-pitch / 2.0, 0, (height + thickness + 2) / 2.0 - thickness / 2.0 - 1]) (hole) - \
        translate([pitch / 2.0, 0, (height + thickness + 2) / 2.0 - thickness / 2.0 - 1]) (hole)
    
    if mounting_hole_dia > 0:
        mounting_hole = cylinder(segments = segments_count, d = mounting_hole_dia, h = thickness + 2, center = True)
        mounting_holes = translate([length / 3.0, 0, 0]) (mounting_hole) + \
                         translate([-length / 3.0, 0, 0]) (mounting_hole)
        p -= mounting_holes

    p = translate([0, 0, thickness / 2.0]) (p)
        
    return p

def rubber_button(radius, length, support_radius, support_length, segments_count):

    main = cylinder(r = radius, h = length, segments = segments_count)

    support = cylinder(r = support_radius, h = support_length, segments = segments_count)

    p = main + support
    
    return p

def lightpipe_straight(radius, length, support_radius, support_length, support_offset, head_radius, segments_count):
    main = cylinder(r = radius, h = length - support_offset - support_length, segments = segments_count)

    support = cylinder(r = support_radius, h = support_length, segments = segments_count)

    head = cylinder(r = head_radius, h = support_offset, segments = segments_count)
    
    p = head + translate([0, 0, support_offset]) (support) + \
        translate([0, 0, support_offset + support_length]) (main)
    
    return p
