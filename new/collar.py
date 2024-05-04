def collar(id, thickness, width, connection_gap, connection_hole_dia, connection_thickness, connection_height = 0.0, connection_gap_closed = 0.0, segments_count = None):

    od = id + thickness * 2.0

    # process connection_gap_closed - i.e. reduce the connection gap, which will also reduce the collar radius
    connection_gap -= connection_gap_closed
    C = 2.0 * math.pi * (od / 2.0) - connection_gap_closed
    od = C / (2.0 * math.pi) * 2.0
    id = od - thickness * 2.0

    connection_width = connection_thickness * 2.0 + connection_gap
    
    co = cylinder(d = od, h = width, segments = segments_count, center = True)

    cc = rotate(90, [0, 1, 0]) (cylinder(d = width, h = connection_width, segments = segments_count, center = True))
    s = hull() (
        cc,
        translate([0, od / 2.0 + width / 2.0 + connection_height, 0]) (cc)
    )
    
    # cuts
    ci_cut = cylinder(d = id, h = width + 2, segments = segments_count, center = True)
    cc_cut = cube([connection_gap, od / 2.0 + width + connection_height + 1.0, width + 2])
    hole = cylinder(d = connection_hole_dia, h = connection_width + 2, segments = segments_count)
    
    p = co + \
        s - \
        ci_cut - \
        translate([-connection_gap / 2.0, 0, -width / 2.0 - 1]) (cc_cut) - \
        translate([-connection_width / 2.0 - 1, od / 2.0 + connection_height - connection_width / 2.0, 0]) (rotate(90, [0, 1, 0]) (hole))

    p = co + s - ci_cut - \
        translate([-connection_gap / 2.0, 0, -width / 2.0 - 1]) (cc_cut) - \
        translate([-connection_width / 2.0 - 1, od / 2.0 + width / 2.0 + connection_height, 0]) (rotate(90, [0, 1, 0]) (hole))
    
    return p
