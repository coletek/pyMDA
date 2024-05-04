def bearing_basic(id, od, thickness, segments_count):
    outter = cylinder(d = od, h = thickness, segments = segments_count)
    inner = cylinder(d = id, h = thickness + 2, segments = segments_count)
    p = outter - translate([0, 0, -1]) (inner)
    return p

@bom_part("Bearing Pillow Block (UCP201)", 22.42, 'A$')
def bearing_pillow_block_ucp201():
    return color(BlackPaint) (rotate(90, [0, 1, 0]) (rotate(90, [0, 0, 1]) (translate([102.9, -77.5, -169.0]) (import_stl("cots/ucp201.stl")))))

@bom_part("Bearing Pillow Block (UCP204)", 27.19, 'A$')
def bearing_pillow_block_ucp204():
    return color(BlackPaint) (import_stl("cots/ucp204.stl"))

@bom_part("Bearing 2 Bolt Flange (UCFL204)", 19.76, 'A$')
def bearing_2_bolt_flange_ucfl204():
    return color(BlackPaint) (import_stl("cots/ucfl204.stl"))

def door(door_width, door_thickness, door_height):
    p = cube([door_width, door_thickness, door_height], center = True)
    p = translate([0, 0, door_height / 2.0]) (p) 
    p = color(Oak) (p)
    return p
