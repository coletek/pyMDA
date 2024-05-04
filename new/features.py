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

def cam_profile(height, start_radius, start_angle, end_radius, end_angle, increment = 0.01, is_center = True):

    points = []

    angle_range = end_angle - start_angle

    radius_step = (end_radius - start_radius) / (angle_range / increment)

    radius = start_radius
    for i in np.arange(start_angle, end_angle, increment):
        x = radius * cos(i)
        y = radius * sin(i)
        pt = [x, y]
        points.append(pt)
        radius += radius_step

    return linear_extrude(height, center = is_center) (polygon(points=points))

def cam_profile_find_radius(target_angle, start_radius, start_angle, end_radius, end_angle, increment = 0.01):

    # TODO: this could/should be replaced with a single equation - can't think of the solution right now.
    
    angle_range = end_angle - start_angle

    radius_step = (end_radius - start_radius) / (angle_range / increment)

    # end_angle + 1deg is required to complete the loop
    radius = start_radius
    for i in np.arange(start_angle, end_angle + math.radians(1.0), increment):
        #print ("i=%f(%fdeg) radius_step=%f start_angle=%f(%fdeg) end_angle=%f(%fdeg) target_angle=%f(%fdeg) radius=%f" % \
        #       (i, math.degrees(i), radius_step, start_angle, math.degrees(start_angle), end_angle, math.degrees(end_angle), target_angle, math.degrees(target_angle), radius))
        if round(math.degrees(i)) == round(math.degrees(target_angle)):
            return radius
        radius += radius_step

    return False

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
