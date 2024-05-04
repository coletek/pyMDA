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

def fixture_countersunk(d, dk, L, a, segments_count):
    # https://image.pushauction.com/0/0/f2c27552-fb37-436a-9369-5b4293c5087b/eda41698-7b80-41de-b5b8-98625f130e93.jpg

    angle = (math.radians(180) - a) / 2.0
    
    countersunk_h = math.tan(angle) * dk / 2.0
    
    p = cylinder(d1 = dk, d2 = 0, h = countersunk_h, segments = segments_count, center = False) + \
                      cylinder(d = d, h = L, segments = segments_count, center = False)
    
    return p

def fixture_socket(d, dk, L, k, segments_count):
    # https://ae01.alicdn.com/kf/HTB1hoF9LVXXXXczXXXXq6xXFXXXt/222055624/HTB1hoF9LVXXXXczXXXXq6xXFXXXt.jpg

    p = cylinder(d = d, h = L + k, segments = segments_count, center = False) + \
                     cylinder(d = dk, h = k, segments = segments_count, center = False)
    
    return p

def fixture_countersunk_clearance_hole(d, dk, L, a, segments_count):
    # NOTE: still need to pass through the clearance hole size for 'd', otherwise everything is automatic based on countersunk dimensions
    
    angle = (math.radians(180) - a) / 2.0
    dk = dk + sls_cots_clearance * 2.0
    countersunk_h = math.tan(angle) * dk / 2.0 + 1.0
    dk2 = countersunk_h / math.tan(angle) * 2.0

    return fixture_countersunk(d, dk2, L + 2.0, a, segments_count)

def washer(dia, hole_dia, thickness, segments_count, is_center = True):
    rod = cylinder(segments = segments_count, d = dia, h = thickness, center = is_center)
    hole = cylinder(segments = segments_count, d = hole_dia, h = thickness + 2, center = is_center)
    if is_center:
        return rod - translate([0, 0, 0]) (hole)
    else:
        return rod - translate([0, 0, -1]) (hole)

def magnet_coin(dia, thickness, segments_count):

    p = cylinder(d = dia, h = thickness, center = True, segments = segments_count)

    p = translate([0, 0, thickness / 2.0]) (p)

    return p

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
