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
