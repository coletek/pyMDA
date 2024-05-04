def magnet_coin(dia, thickness, segments_count):

    p = cylinder(d = dia, h = thickness, center = True, segments = segments_count)

    p = translate([0, 0, thickness / 2.0]) (p)

    return p
