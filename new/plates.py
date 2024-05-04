def plate_width_mounting_holes(width, length, thickness,
                               mounting_hole_dia, mounting_hole_pitch_width, mounting_hole_pitch_length,
                               mounting_hole_offset_width, mounting_hole_offset_length, segments_count):
    
    b = cube([width, length, thickness], center = True)

    h = cylinder(d = mounting_hole_dia, h = thickness + 2.0, segments = segments_count, center = True)

    hh = translate([mounting_hole_pitch_width / 2.0, mounting_hole_pitch_length / 2.0, 0]) (h) + \
        translate([-mounting_hole_pitch_width / 2.0, mounting_hole_pitch_length / 2.0, 0]) (h) + \
        translate([mounting_hole_pitch_width / 2.0, -mounting_hole_pitch_length / 2.0, 0]) (h) + \
        translate([-mounting_hole_pitch_width / 2.0, -mounting_hole_pitch_length / 2.0, 0]) (h)

    hh = translate([mounting_hole_offset_width, mounting_hole_offset_length, 0]) (hh)
    
    p = b - hh
    
    return p

def plate(width, height, thickness, top_mounting_hole_depth = 0, bottom_mounting_hole_depth = 0, mounting_hole_size = 0, segments_count = None):

    p = translate([-thickness / 2.0, -width / 2.0, -height / 2.0]) (
        cube([thickness, width, height])
    )

    distance = thickness / 2.0
        
    if top_mounting_hole_depth > 0:

        depth = top_mounting_hole_depth
        
        bolt_hole1 = translate([0, width / 2.0 - distance, height / 2.0 - depth - 1]) (
            rotate(90, [0, 0, 1]) (
                cylinder(h = depth + 2, d = mounting_hole_size, segments = segments_count)
            )
        )
        bolt_hole2 = translate([0, - width / 2.0 + distance, height / 2.0 - depth - 1]) (
            rotate(90, [0, 0, 1]) (
                cylinder(h = depth + 2, d = mounting_hole_size, segments = segments_count)
            )
        )

        p = p - bolt_hole1 - bolt_hole2
        
    if bottom_mounting_hole_depth > 0:

        depth = bottom_mounting_hole_depth
        
        bolt_hole3 = translate([0, width / 2.0 - distance, - height / 2.0 - 1]) (
            rotate(90, [0, 0, 1]) (
                cylinder(h = depth + 2, d = mounting_hole_size, segments = segments_count)
            )
        )
        bolt_hole4 = translate([0, - width / 2.0 + distance, - height / 2.0 - 1]) (
            rotate(90, [0, 0, 1]) (
                cylinder(h = depth + 2, d = mounting_hole_size, segments = segments_count)
            )
        )

        p = p - bolt_hole3 - bolt_hole4
                
    return p

def plate_with_fillets(width, length, thickness, fillet_radius, segments):
    # could be done with hull(), but done this way to support FreeCAD STEP exporting

    x = width - fillet_radius * 2.0
    y = length - fillet_radius * 2.0

    p = []
    
    if x != 0:
        p += cube([x, length, thickness], center = True)

    if y != 0:
        p += cube([width, y, thickness], center = True)
    
    f = cylinder(r = fillet_radius, h = thickness, center = True, segments = segments)
    p += translate([x / 2.0, y / 2.0, 0]) (f) + \
         translate([x / 2.0, -y / 2.0, 0]) (f) + \
         translate([-x / 2.0, y / 2.0, 0]) (f) + \
         translate([-x / 2.0, -y / 2.0, 0]) (f)

    return p
