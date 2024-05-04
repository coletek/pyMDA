]def slot(width, length, height, segments_count, use_hull = False):
    
    hole = translate([0, 0, -(height + 2.0) / 2.0]) (cylinder(segments = segments_count, r = width / 2.0, h = height + 2.0))

    if use_hull:
        p = hull() (
            translate([0, -length / 2.0, 0]) (hole),
            translate([0, length / 2.0, 0]) (hole),
        )
    else:
        p = translate([0, -length / 2.0, 0]) (hole) + \
            translate([0, length / 2.0, 0]) (hole) + \
            cube([width, length, height + 2], center = True)

    return p

def slot_curve(width, height, radius, start_angle, end_angle, step, segments_count, use_holes):
    
    hole = translate([0, 0, -(height + 2.0) / 2.0]) (cylinder(segments = segments_count, r = width / 2.0, h = height + 2.0))

    p = []
    
    if use_holes:

        y = radius * math.cos(start_angle)
        x = radius * math.sin(start_angle)
        p += translate([x, y, 0]) (hole)

        y = radius * math.cos(end_angle)
        x = radius * math.sin(end_angle)
        p += translate([x, y, 0]) (hole)
            
        for a in np.arange(start_angle, end_angle, step):
            y = radius * math.cos(a)
            x = radius * math.sin(a)
            #print (radius, x, y, a)
            p += translate([x, y, 0]) (hole)

    else:
        
        p = cylinder(r = radius + width / 2.0, h = height + 2.0, center = True, segments = segments_count) - cylinder(r = radius - width / 2.0, h = height + 3.0, center = True, segments = segments_count)
        
        p -= rotate(-math.degrees(start_angle), [0, 0, 1]) (translate([-(radius + width) / 2.0, 0, 0]) (cube([radius + width, radius * 2.0 + width * 2.0, height * 2.0], center = True)))
        p -= rotate(-math.degrees(end_angle), [0, 0, 1]) (translate([(radius + width) / 2.0, 0, 0]) (cube([radius + width, radius * 2.0 + width * 2.0, height * 2.0], center = True)))

        y = radius * math.cos(start_angle)
        x = radius * math.sin(start_angle)
        p += translate([x, y, 0]) (hole)

        y = radius * math.cos(end_angle)
        x = radius * math.sin(end_angle)
        p += translate([x, y, 0]) (hole)
        
    return p

def slot_array(length, slot_width, slot_length, slot_count, height, segments_count, use_hull = False):
    gap = (length - slot_count * (slot_length + slot_width)) / (slot_count + 1.0)

    y = - length / 2.0 + gap + (slot_length + slot_width) / 2.0
    p = translate([0, y, 0]) (slot(slot_width, slot_length, height, segments_count))
    for i in range(slot_count - 1):
        y += gap + (slot_length + slot_width)
        p += translate([0, y, 0]) (slot(slot_width, slot_length, height, segments_count, use_hull))
    return p


def speaker_holes(enclosure_speaker_holes_outer_dia, enclosure_speaker_pitch, enclosure_speaker_hole_dia, enclosure_wall_thickness, segments_count):

    speaker_hole = cylinder(d = enclosure_speaker_hole_dia, h = enclosure_wall_thickness, segments = segments_count, center = True)

    l = int(enclosure_speaker_holes_outer_dia / 2.0 / enclosure_speaker_pitch)

    p = speaker_hole

    for j in range(l):
        c = 2 * math.pi * (enclosure_speaker_pitch * j + enclosure_speaker_pitch)
        num = int(c / enclosure_speaker_pitch)
        angle_diff = 2.0 * math.pi / num
        #print c, num
        angle = 0.0
        for i in range(num):
            x = ((enclosure_speaker_pitch * j) + enclosure_speaker_pitch) * math.cos(angle)
            y = ((enclosure_speaker_pitch * j) + enclosure_speaker_pitch) * math.sin(angle)
            p += translate([x, y, 0]) (speaker_hole)
            #print angle, x, y
            angle += angle_diff

    return p
