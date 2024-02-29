
from solid import *
from solid.utils import *
import math
import numpy as np
from settings_common import *

def prism(l, w, h):
    return polyhedron(
        points=[[0,0,0], [l,0,0], [l,w,0], [0,w,0], [0,w,h], [l,w,h]],
        faces=[[0,1,2,3],[5,4,3,2],[0,4,5,1],[0,3,4],[5,2,1]]
    )

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

def cube_curved_sides(x, y, z, corner_radius, side_count, segments_count):

    # alternative approach to minkowski, so it imports into OpenSCAD and export as STEP
    # TODO: support non-center option
    # using hull() still requires high segments - perhaps use rotate_extrude instead

    corner_round = translate([0, 0, -z / 2.0]) (cylinder(segments = segments_count, r = corner_radius, h = z))

    if side_count == 4:
        return hull() (
            translate([x / 2.0 - corner_radius, y / 2.0 - corner_radius, 0]) (corner_round),
            translate([x / 2.0 - corner_radius, -y / 2.0 + corner_radius, 0]) (corner_round),
            translate([-x / 2.0 + corner_radius, y / 2.0 - corner_radius, 0]) (corner_round),
            translate([-x / 2.0 + corner_radius, -y / 2.0 + corner_radius, 0]) (corner_round),
        )
    elif side_count == 2:
        corner_sq = cube([corner_radius, corner_radius, z], center = True)
        # FIXME
        #return translate([x / 2.0 - corner_radius, y / 2.0 - corner_radius, 0]) (corner_round) + \
        #    translate([x / 2.0 - corner_radius + corner_radius / 2.0, y / 2.0 - corner_radius + corner_radius / 2.0, 0]) (corner_sq) + \
        #    translate([-x / 2.0 + corner_radius, y / 2.0 - corner_radius, 0]) (corner_round) + \
        #    translate([-x / 2.0 + corner_radius - corner_radius / 2.0, y / 2.0 - corner_radius + corner_radius / 2.0, 0]) (corner_sq)
        return hull() (
            translate([x / 2.0 - corner_radius, y / 2.0 - corner_radius, 0]) (corner_round),
            translate([x / 2.0 - corner_radius + corner_radius / 2.0, y / 2.0 - corner_radius + corner_radius / 2.0, 0]) (corner_sq),
            translate([-x / 2.0 + corner_radius, y / 2.0 - corner_radius, 0]) (corner_round),
            translate([-x / 2.0 + corner_radius - corner_radius / 2.0, y / 2.0 - corner_radius + corner_radius / 2.0, 0]) (corner_sq)
            )


def cube_curved_edges(x, y, z, corner_radius, segments_count, is_center = True):

    # alternative approach to minkowski, so it imports into OpenSCAD and export as STEP
    # using hull() still requires high segments - perhaps use rotate_extrude instead
    
    if is_center:
        return hull() (
            translate([-x / 2.0 + corner_radius, -y / 2.0 + corner_radius, -z / 2.0 + corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x / 2.0 - corner_radius, -y / 2.0 + corner_radius, -z / 2.0 + corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x / 2.0 - corner_radius, y / 2.0 - corner_radius, -z / 2.0 + corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([-x / 2.0 + corner_radius, y / 2.0 - corner_radius, -z / 2.0 + corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            
            translate([-x / 2.0 + corner_radius, -y / 2.0 + corner_radius, z / 2.0 - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x / 2.0 - corner_radius, -y / 2.0 + corner_radius, z / 2.0 - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x / 2.0 - corner_radius, y / 2.0 - corner_radius, z / 2.0 - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([-x / 2.0 + corner_radius, y / 2.0 - corner_radius, z / 2.0 - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
        )
    
    else:
        return hull() (
            translate([corner_radius, corner_radius, corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x - corner_radius, corner_radius, corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x - corner_radius, y - corner_radius, corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([corner_radius, y - corner_radius, corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            
            translate([corner_radius, corner_radius, z - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x - corner_radius, corner_radius, z - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([x - corner_radius, y - corner_radius, z - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
            translate([corner_radius, y - corner_radius, z - corner_radius]) (sphere(segments = segments_count, r = corner_radius)),
        )

def ring(r, thickness, segments_count, rotate_extrude_segments_count):
    return rotate_extrude(convexity = 10, segments = rotate_extrude_segments_count) (translate([r, 0, 0]) (circle(d = thickness, segments = segments_count)))

def cylinder_curved_edges(r, h, corner_radius, both_sides, segments_count):

    b_height = h - corner_radius
    if both_sides:
        b_height = h - corner_radius * 2.0
    b = cylinder(segments = segments_count, r = r, h = b_height)

    eb = ring(r, corner_radius * 2, segments_count)
    bb = cylinder(segments = segments_count, r = r - corner_radius, h = corner_radius * 2.0)

    p = translate([0, 0, corner_radius]) (b) + translate([0, 0, corner_radius]) (eb) + translate([0, 0, 0]) (bb)
    
    if both_sides:
        et = ring(r, corner_radius * 2, segments_count)
        bt = cylinder(segments = segments_count, r = r - corner_radius, h = corner_radius * 2.0)
        p += translate([0, 0, h - corner_radius]) (et) + translate([0, 0, h - corner_radius * 2.0]) (bt)
    
    return p

def rod_curved_edges(length, thickness, corner_radius, segments_count):
    return cube_curved_edges(thickness, length, thickness, corner_radius, segments_count, True)

def line_round_via_hull(p1, p2, radius, segments_count):

    s = sphere(r = radius, segments = segments_count)

    #s = cube_curved_sides(radius * 2, radius * 2, radius, 2.0, 4, segments_count)

    s1 = translate(p1) (s)
    s2 = translate(p2) (s)

    # TODO: use cylinder instead to avoid mesh
    p = hull() (s1, s2)
    #p = s1 + s2
    
    return p

def polyline_round(pts, radius, segments_count, close):

    if close:
        p = line_round_via_hull(pts[len(pts) - 1], pts[0], radius, segments_count)
    else:
        p = 0
        
    for i in range(len(pts) - 1):
        p += line_round_via_hull(pts[i], pts[i + 1], radius, segments_count)

    return p

def bezier_coordinate(t, n0, n1, n2, n3):
    return n0 * math.pow((1 - t), 3) + 3 * n1 * t * math.pow((1 - t), 2) + 3 * n2 * math.pow(t, 2) * (1 - t) + n3 * math.pow(t, 3)

def bezier_point(t, p0, p1, p2, p3):
    return [
        bezier_coordinate(t, p0[0], p1[0], p2[0], p3[0]),
        bezier_coordinate(t, p0[1], p1[1], p2[1], p3[1]),
        bezier_coordinate(t, p0[2], p1[2], p2[2], p3[2])
    ]

def bezier_curve_pts(t_step, p0, p1, p2, p3):
    p = []
    for t in np.arange(0, t_step + 1, t_step):
        p.append(bezier_point(t, p0, p1, p2, p3))

    return p

def bezier_curve_pts_brace_xyz(pts, pts2):
    xx_min = 1000
    xx_max = -1000
    yy_min = 1000
    yy_max = -1000
    zz_min = 1000
    zz_max = -1000
    
    for xx, yy, zz in pts:
        #print xx, yy, zz
        for xxx, yyy, zzz in pts2:
            if xx > xxx:
                xx_max = xxx            
            if xx < xxx:
                xx_min = xxx
            if yy > yyy:
                yy_max = yyy           
            if yy < yyy:
                yy_min = yyy
            if zz > zzz:
                zz_max = zzz           
            if zz < zzz:
                zz_min = zzz

    return [ xx_min, yy_min, zz_min, xx_max, yy_max, zz_max ]

def bezier_curve_pts_brace(t_step, p0, p1, p2, p3, pts):
    pts_brace = bezier_curve_pts(t_step, p0, p1, p2, p3)

    # get new pts
    [x_min, y_min, z_min, x_max, y_max, z_max] = bezier_curve_pts_brace_xyz(pts_brace, pts)
    #print [x_min, y_min, z_min, x_max, y_max, z_max]

    p0 = [-x_max, y_max, z_min]
    p1 = [-x_max, y_min, z_max]
    p2 = [x_max, y_min, z_max]
    p3 = [x_max, y_max, z_min]

    p = bezier_curve_pts(t_step, p0, p1, p2, p3)

    return p

def bezier_point_debug(t, p0, p1, p2, p3):
    pos = [
        bezier_coordinate(t, p0[0], p1[0], p2[0], p3[0]),
        bezier_coordinate(t, p0[1], p1[1], p2[1], p3[1]),
        bezier_coordinate(t, p0[2], p1[2], p2[2], p3[2])
    ]
    return color(Blue) (translate(pos) (sphere(r = 2)))

def bezier_curve_pts_debug(t_step, p0, p1, p2, p3):
    p = color(Red) (translate(p0) (sphere(r = 10)))
    p += color(Red) (translate(p1) (sphere(r = 10)))
    p += color(Red) (translate(p2) (sphere(r = 10)))
    p += color(Red) (translate(p3) (sphere(r = 10)))

    for t in np.arange(0, t_step + 1, t_step):
        p += bezier_point_debug(t, p0, p1, p2, p3)

    return p

def hexagon(cle, h):

    angle = 360.0 / 6.0;
    cote = cle * 1.0 / math.tan(math.radians(angle));
    
    p = cube([cle, cote ,h], center = True) + \
        rotate(angle, [0, 0, 1]) (cube([cle, cote, h], center = True)) + \
        rotate(2 * angle, [0, 0, 1]) (cube([cle, cote, h], center = True))
    
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

def slot(width, length, height, segments_count, use_hull = False):
    
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

def stepper_mounting_plate(width, height, thickness, slot_dia, slot_height = 0, mounting_hole_depth = 0, mounting_hole_size = 0, segments_count = None):

    mounting_hole_gap = 31 # NEMA17
    slot_width = 23

    p = difference()(
        
	# rotation stepper mounting plate
	translate([-thickness / 2.0, -width / 2.0, -height / 2.0]) (
	    cube([thickness, width, height])
        ),

        # stepper motor slot
        translate([-thickness / 2.0 - 1, -slot_width / 2.0, -slot_height / 2.0]) (
            cube([thickness + 2, slot_width, slot_height])
        ),

        translate([-thickness / 2.0 - 1, 0, slot_height / 2.0]) (
	    rotate(90, [0, 1, 0]) (
	        cylinder(h = thickness + 2, d = slot_width, segments = segments_count)
            )
        ),

        # stepper motor mounting slot +ve y
        translate([-thickness / 2.0 - 1,
		   mounting_hole_gap / 2.0,
		   -slot_height / 2.0 - mounting_hole_gap / 2.0]) (
                       rotate(90, [0, 1, 0]) (
	                   cylinder(h = thickness + 2, d = slot_dia, segments = segments_count)
                       )
        ),
        
        translate([-thickness / 2.0 - 1,
		   mounting_hole_gap / 2.0,
		   slot_height / 2.0 + mounting_hole_gap / 2.0]) (
                       rotate(90, [0, 1, 0]) (
	                   cylinder(h = thickness + 2, d = slot_dia, segments = segments_count)
                       )
        ),

        # stepper motor mounting slot -ve y
        translate([-thickness / 2.0 - 1,
		   -mounting_hole_gap / 2.0,
		   -slot_height / 2.0 - mounting_hole_gap / 2.0]) (
                       rotate(90, [0, 1, 0]) (
	                   cylinder(h = thickness + 2, d = slot_dia, segments = segments_count)
                           )
        ),
        
        translate([-thickness / 2.0 - 1,
		   -mounting_hole_gap / 2.0,
		   slot_height / 2.0 + mounting_hole_gap / 2.0]) (
	               rotate(90, [0, 1, 0]) (
	                   cylinder(h = thickness + 2, d = slot_dia, segments = segments_count)
                       )
        )
    
    )
    
    if slot_height > 0:

        slot0 = translate([-thickness / 2.0 - 1, 0, -slot_height / 2.0]) (
	    rotate(90, [0, 1, 0]) (
	        cylinder(h = thickness + 2, d = slot_width, segments = segments_count)
            )
        )
        
        slot1 = translate([-thickness / 2.0 - 1,
		           -slot_dia / 2.0 + mounting_hole_gap / 2.0,
		           -slot_height / 2.0 - mounting_hole_gap / 2.0]) (
	                       cube([thickness + 2,
	                             slot_dia,
	                             slot_height + mounting_hole_gap])
	                   )
        
        slot2 = translate([-thickness / 2.0 - 1,
	                   -slot_dia / 2.0 - mounting_hole_gap / 2.0,
	                   -slot_height / 2.0 - mounting_hole_gap / 2.0]) (
		               cube([thickness + 2,
			             slot_dia,
			         slot_height + mounting_hole_gap])
                           )
        
        p = p - slot0 - slot1 - slot2
        
    if mounting_hole_depth > 0:
        
        depth = mounting_hole_depth
        distance = thickness / 2.0
        
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

        p = p - bolt_hole1 - bolt_hole2 - bolt_hole3 - bolt_hole4

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

def shaft_with_key(dia, length, key_cut, key_length, segments_count):

    k = translate([-dia / 2.0 - 1.0, dia / 2.0 - key_cut, length - key_length]) (cube([dia + 2.0, dia, key_length + 1.0]))
    s = cylinder(d = dia, h = length, segments = segments_count)

    p = s - k

    p = color(Steel) (p)
    
    return p

# https://www.omc-stepperonline.com/brushed-12v-dc-gear-motor-3kg-cm-3rpm-w-828-1-worm-gearbox-wga-2430123100-g828
def dc_motor(dia, length, shaft_dia, shaft_length, shaft_key_cut, shaft_key_length, segments_count):

    m = cylinder(d = dia, h = length, segments = segments_count)

    m = color(Aluminum) (m)
    
    s = shaft_with_key(shaft_dia, shaft_length, shaft_key_cut, shaft_key_length, segments_count)
    
    p = m + translate([0, 0, length]) (s)

    p = translate([0, 0, -length]) (p)

    return p

# https://www.omc-stepperonline.com/brushed-12v-dc-gear-motor-3kg-cm-3rpm-w-828-1-worm-gearbox-wga-2430123100-g828
def gearbox_worm(width, length, height, width_pitch, length_pitch, length_pitch_pos, shaft_pos, shaft_dia, shaft_length, shaft_key_cut, shaft_key_length, segments_count):
    
    b = cube([width, length, height])

    b = color(Aluminum) (b)
    
    s = shaft_with_key(shaft_dia, shaft_length, shaft_key_cut, shaft_key_length, segments_count)

    h = cylinder(d = m3_tap_hole_size, h = height / 2.0, segments = segments_count)

    hp = translate([-width_pitch / 2.0, -length_pitch / 2.0, 0]) (h) + \
        translate([width_pitch / 2.0, -length_pitch / 2.0, 0]) (h) + \
        translate([-width_pitch / 2.0, length_pitch / 2.0, 0]) (h) + \
        translate([width_pitch / 2.0, length_pitch / 2.0, 0]) (h)

    y = length_pitch / 2.0 - shaft_pos + length_pitch_pos
    p = translate([-width / 2.0, -shaft_pos, 0]) (b) + \
        translate([0, 0, height]) (s) - \
        translate([0, y, height / 2.0 + 1.0]) (hp)

    p = translate([0, 0, -height]) (p)

    return p

# https://www.omc-stepperonline.com/brushed-12v-dc-gear-motor-3kg-cm-3rpm-w-828-1-worm-gearbox-wga-2430123100-g828
def dc_motor_with_gearbox(motor_dia,
                          motor_length,
                          motor_shaft_dia,
                          motor_shaft_length,
                          motor_shaft_key_cut,
                          motor_shaft_key_length,
                          motor_worm_gearbox_width,
                          motor_worm_gearbox_length,
                          motor_worm_gearbox_height,
                          motor_worm_gearbox_width_pitch,
                          motor_worm_gearbox_length_pitch,
                          motor_worm_gearbox_length_pitch_pos,
                          motor_worm_gearbox_shaft_pos,
                          motor_worm_gearbox_shaft_dia,
                          motor_worm_gearbox_shaft_length,
                          motor_worm_gearbox_shaft_key_cut,
                          motor_worm_gearbox_shaft_key_length,
                          segments_count):

    m = dc_motor(motor_dia, motor_length, motor_shaft_dia, motor_shaft_length, motor_shaft_key_cut, motor_shaft_key_length, segments_count)

    g = gearbox_worm(motor_worm_gearbox_width, motor_worm_gearbox_length, motor_worm_gearbox_height,
                     motor_worm_gearbox_width_pitch, motor_worm_gearbox_length_pitch, motor_worm_gearbox_length_pitch_pos,
                     motor_worm_gearbox_shaft_pos, motor_worm_gearbox_shaft_dia, motor_worm_gearbox_shaft_length,
                     motor_worm_gearbox_shaft_key_cut, motor_worm_gearbox_shaft_key_length, segments_count)

    p = g + translate([-motor_shaft_dia / 2.0,
                       motor_worm_gearbox_length - motor_worm_gearbox_shaft_pos,
                       -motor_worm_gearbox_height / 2.0]) (rotate(90, [1, 0, 0]) (m))

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

def matrix_copy(feature, part, space, x_length, y_length, x_count, y_count):
    
    x_gap = (x_length - x_count * space) / (x_count + 1.0)
    y_gap = (y_length - y_count * space) / (y_count + 1.0)

    p = part
    
    y = - y_length / 2.0 + y_gap + space / 2.0
    for j in range(y_count):
        x = - x_length / 2.0 + x_gap + space / 2.0
        p -= translate([x, y, 0]) (feature)
        for i in range(x_count - 1):
            x += x_gap + space
            p -= translate([x, y, 0]) (feature)
        y += y_gap + space

    return p

def shs(width, thickness, length = 100, end1_cut_angle = 0.0, end2_cut_angle = 0.0, display_size_text = False):
    # works for -45 and 45.0
    # TODO: make work for any angle
    
    p = cube([width, length, width], center = True) - cube([width - thickness, length + 2, width - thickness], center = True)

    if end1_cut_angle != 0:
        l = math.sqrt(2 * (width) * (width))
        if end1_cut_angle < 0:
            c = translate([0, 0, -(width) / 2.0]) (rotate(end1_cut_angle, [1, 0, 0]) (cube([width + 2, l, l], center = True)))
        else:
            c = translate([0, 0, (width) / 2.0]) (rotate(end1_cut_angle, [1, 0, 0]) (cube([width + 2, l, l], center = True)))
        p -= translate([0, length / 2.0, 0]) (c)

    if end2_cut_angle != 0:
        l = math.sqrt(2 * (width) * (width))
        if end2_cut_angle < 0:
            c = translate([0, 0, -(width) / 2.0]) (rotate(end2_cut_angle, [1, 0, 0]) (cube([width + 2, l, l], center = True)))
        else:
            c = translate([0, 0, (width) / 2.0]) (rotate(end2_cut_angle, [1, 0, 0]) (cube([width + 2, l, l], center = True)))
        p -= translate([0, -length / 2.0, 0]) (c)

    p = color(Aluminum) (p)

    if display_size_text:
        txt = "%.1fx%.0fx%.0fmm" % (thickness, width, length)
        p += translate([width / 4.0, 0, width / 2.0]) (rotate(90, [0, 0, 1]) (color(Black) (text(txt, size=20))))

    return p

def cs(width, thickness, length):
    
    p = cube([width, length, width], center = True) - translate([-0.5 - thickness, 0, 0]) (cube([width + 1, length + 2, width - thickness * 2.0], center = True))

    p = color(Aluminum) (p)
    return p

def ls(width, height, thickness, length):
    
    p = cube([width, length, height], center = True) - translate([-0.5 - thickness, 0, -0.5 - thickness]) (cube([width + 1, length + 2, height + 1], center = True))

    p = color(Aluminum) (p)
    return p

def sb(width, length):
    
    p = cube([width, length, width], center = True)

    p = color(Aluminum) (p)
    return p

def rod(dia, length, segments_count):
    return color(Aluminum) (cylinder(d = dia, h = length, center = True, segments = segments_count))

def sheet(width = 600, length = 2400, thickness = 1.2, display_size_text = False):
    p = cube([width, length, thickness], center = True)
    p = color(Aluminum) (p)

    if display_size_text:
        axis = 0
        l = 1000000.0
        if thickness < l:
            a = [0, 0, thickness / 2.0]
            r = [0, 0, 1]
            l = thickness
            if width > length:
                l2 = length
                l3 = width
            else:
                l2 = width
                l3 = length
        if length < l:
            a = [0, -length / 2.0, 0]
            r = [1, 0, 0]
            l = length
            if width > thickness:
                l2 = thickness
                l3 = width
            else:
                l2 = width
                l3 = thickness
        if width < l:
            a = [width / 2.0, 0, 0]
            r = [0, 1, 0]
            l = width
            if length > thickness:
                l2 = thickness
                l3 = length
            else:
                l2 = length
                l3 = thickness
        txt = "%.1fx%.0fx%.0fmm" % (l, l2, l3)
        p += translate(a) (rotate(90, r) (color(Black) (text(txt, size = 20))))
    
    return p


def wedge(r, h, sa, ea, segments):
    # TODO make work for larger then 180deg
    
    c = cylinder(r = r, h = h, center = True, segments = segments)

    l = r * 2.0 + 2.0
    cut = cube([l, l, h + 2.0], center = True)

    p = c - \
        rotate(math.degrees(sa), [0, 0, 1]) (translate([0, -l / 2.0, 0]) (cut)) - \
        rotate(math.degrees(ea) + 180, [0, 0, 1]) (translate([0, -l / 2.0, 0]) (cut))
    
    return p

def hinge(d, axle_d, h, hinge_segments, l, tolerance, is_left, segments):

    c = cylinder(d = d, h = h, center = True, segments = segments)
    axle = cylinder(d = axle_d + tolerance, h = h + 2.0, center = True, segments = segments)
    a = cube([l, d / 2.0, h], center = True)

    cc_h = h / hinge_segments
    cc = cylinder(d = d + tolerance * 2.0, h = cc_h + tolerance * 2.0, center = True, segments = segments)

    offset = d / 4.0
    if is_left:
        offset = -offset
    p = translate([l / 2.0, offset, 0]) (a)

    p += c    
    if is_left:
        start_idx = 0
    else:
        start_idx = 1

    # odd set
    for i in range(start_idx, hinge_segments, 2):
        p -= translate([0, 0, -h / 2.0 + cc_h / 2.0 + cc_h * i]) (cc)

    p -= axle
     
    return p



#function polyRound(radiipoints,fn=5,mode=0)=
#  /*Takes a list of radii points of the format [x,y,radius] and rounds each point
#    with fn resolution
#    mode=0 - automatic radius limiting - DEFAULT
#    mode=1 - Debug, output radius reduction for automatic radius limiting
#    mode=2 - No radius limiting*/
#  let(
#    p=getpoints(radiipoints), //make list of coordinates without radii
#    Lp=len(p),
#    //remove the middle point of any three colinear points, otherwise adding a radius to the middle of a straigh line causes problems
#    radiiPointsWithoutTrippleColinear=[
#      for(i=[0:len(p)-1]) if(
#        // keep point if it isn't colinear or if the radius is 0
#        !isColinear(
#          p[listWrap(i-1,Lp)],
#          p[listWrap(i+0,Lp)],
#          p[listWrap(i+1,Lp)]
#        )||
#        p[listWrap(i+0,Lp)].z!=0
#      ) radiipoints[listWrap(i+0,Lp)] 
#    ],
#    newrp2=processRadiiPoints(radiiPointsWithoutTrippleColinear),
#    plusMinusPointRange=mode==2?1:2,
#    temp=[
#      for(i=[0:len(newrp2)-1]) //for each point in the radii array
#      let(
#        thepoints=[for(j=[-plusMinusPointRange:plusMinusPointRange])newrp2[listWrap(i+j,len(newrp2))]],//collect 5 radii points
#        temp2=mode==2?round3points(thepoints,fn):round5points(thepoints,fn,mode)
#      )
#      mode==1?temp2:newrp2[i][2]==0?
#        [[newrp2[i][0],newrp2[i][1]]]: //return the original point if the radius is 0
#        CentreN2PointsArc(temp2[0],temp2[1],temp2[2],0,fn) //return the arc if everything is normal
#    ]
#  )
#  [for (a = temp) for (b = a) b];//flattern and return the array

#function getpoints(p)=[for(i=[0:len(p)-1])[p[i].x,p[i].y]];// gets [x,y]list of[x,y,r]list

#function isColinear(p1,p2,p3)=getGradient(p1,p2)==getGradient(p2,p3)?1:0;//return 1 if 3 points are colinear

#function getGradient(p1,p2)=(p2.y-p1.y)/(p2.x-p1.x);

#function processRadiiPoints(rp)=
#  [for(i=[0:len(rp)-1])
#    processRadiiPoints2(rp,i)
#  ];

#function processRadiiPoints2(list,end=0,idx=0,result=0)=
#  idx>=end+1?result:
#  processRadiiPoints2(list,end,idx+1,relationalRadiiPoints(result,list[idx]));

#function relationalRadiiPoints(po,pi)=
#  let(
#    p0=pi[0],
#    p1=pi[1],
#    p2=pi[2],
#    pv0=pi[3][0],
#    pv1=pi[3][1],
#    pt0=pi[3][2],
#    pt1=pi[3][3],
#    pn=
#      (pv0=="y"&&pv1=="x")||(pv0=="r"&&pv1=="a")||(pv0=="y"&&pv1=="a")||(pv0=="x"&&pv1=="a")||(pv0=="y"&&pv1=="r")||(pv0=="x"&&pv1=="r")?
#        [p1,p0,p2,concat(pv1,pv0,pt1,pt0)]:
#        [p0,p1,p2,concat(pv0,pv1,pt0,pt1)],
#    n0=pn[0],
#    n1=pn[1],
#    n2=pn[2],
#    nv0=pn[3][0],
#    nv1=pn[3][1],
#    nt0=pn[3][2],
#    nt1=pn[3][3],
#    temp=
#      pn[0]=="l"?
#        [po[0],pn[1],pn[2]]
#      :pn[1]=="l"?
#        [pn[0],po[1],pn[2]]
#      :nv0==undef?
#        [pn[0],pn[1],pn[2]]//abs x, abs y as default when undefined
#      :nv0=="a"?
#        nv1=="r"?
#          nt0=="a"?
#            nt1=="a"||nt1==undef?
#              [cos(n0)*n1,sin(n0)*n1,n2]//abs angle, abs radius
#            :absArelR(po,pn)//abs angle rel radius
#          :nt1=="r"||nt1==undef?
#            [po[0]+cos(pn[0])*pn[1],po[1]+sin(pn[0])*pn[1],pn[2]]//rel angle, rel radius 
#          :[pn[0],pn[1],pn[2]]//rel angle, abs radius
#        :nv1=="x"?
#          nt0=="a"?
#            nt1=="a"||nt1==undef?
#              [pn[1],pn[1]*tan(pn[0]),pn[2]]//abs angle, abs x
#            :[po[0]+pn[1],(po[0]+pn[1])*tan(pn[0]),pn[2]]//abs angle rel x
#            :nt1=="r"||nt1==undef?
#              [po[0]+pn[1],po[1]+pn[1]*tan(pn[0]),pn[2]]//rel angle, rel x 
#            :[pn[1],po[1]+(pn[1]-po[0])*tan(pn[0]),pn[2]]//rel angle, abs x
#          :nt0=="a"?
#            nt1=="a"||nt1==undef?
#              [pn[1]/tan(pn[0]),pn[1],pn[2]]//abs angle, abs y
#            :[(po[1]+pn[1])/tan(pn[0]),po[1]+pn[1],pn[2]]//abs angle rel y
#          :nt1=="r"||nt1==undef?
#            [po[0]+(pn[1]-po[0])/tan(90-pn[0]),po[1]+pn[1],pn[2]]//rel angle, rel y 
#          :[po[0]+(pn[1]-po[1])/tan(pn[0]),pn[1],pn[2]]//rel angle, abs y
#      :nv0=="r"?
#        nv1=="x"?
#          nt0=="a"?
#            nt1=="a"||nt1==undef?
#              [pn[1],sign(pn[0])*sqrt(sq(pn[0])-sq(pn[1])),pn[2]]//abs radius, abs x
#            :[po[0]+pn[1],sign(pn[0])*sqrt(sq(pn[0])-sq(po[0]+pn[1])),pn[2]]//abs radius rel x
#          :nt1=="r"||nt1==undef?
#            [po[0]+pn[1],po[1]+sign(pn[0])*sqrt(sq(pn[0])-sq(pn[1])),pn[2]]//rel radius, rel x 
#          :[pn[1],po[1]+sign(pn[0])*sqrt(sq(pn[0])-sq(pn[1]-po[0])),pn[2]]//rel radius, abs x
#        :nt0=="a"?
#          nt1=="a"||nt1==undef?
#            [sign(pn[0])*sqrt(sq(pn[0])-sq(pn[1])),pn[1],pn[2]]//abs radius, abs y
#          :[sign(pn[0])*sqrt(sq(pn[0])-sq(po[1]+pn[1])),po[1]+pn[1],pn[2]]//abs radius rel y
#        :nt1=="r"||nt1==undef?
#          [po[0]+sign(pn[0])*sqrt(sq(pn[0])-sq(pn[1])),po[1]+pn[1],pn[2]]//rel radius, rel y 
#        :[po[0]+sign(pn[0])*sqrt(sq(pn[0])-sq(pn[1]-po[1])),pn[1],pn[2]]//rel radius, abs y
#      :nt0=="a"?
#        nt1=="a"||nt1==undef?
#          [pn[0],pn[1],pn[2]]//abs x, abs y
#        :[pn[0],po[1]+pn[1],pn[2]]//abs x rel y
#      :nt1=="r"||nt1==undef?
#        [po[0]+pn[0],po[1]+pn[1],pn[2]]//rel x, rel y 
#      :[po[0]+pn[0],pn[1],pn[2]]//rel x, abs y
#  )
#  temp;

#function round5points(rp,fn,debug=0)=
#	rp[2][2]==0&&debug==0?[[rp[2][0],rp[2][1]]]://return the middle point if the radius is 0
#	rp[2][2]==0&&debug==1?0://if debug is enabled and the radius is 0 return 0
#	let(
#    p=getpoints(rp), //get list of points
#    r=[for(i=[1:3]) abs(rp[i][2])],//get the centre 3 radii
#    //start by determining what the radius should be at point 3
#    //find angles at points 2 , 3 and 4
#    a2=cosineRuleAngle(p[0],p[1],p[2]),
#    a3=cosineRuleAngle(p[1],p[2],p[3]),
#    a4=cosineRuleAngle(p[2],p[3],p[4]),
#    //find the distance between points 2&3 and between points 3&4
#    d23=pointDist(p[1],p[2]),
#    d34=pointDist(p[2],p[3]),
#    //find the radius factors
#    F23=(d23*tan(a2/2)*tan(a3/2))/(r[0]*tan(a3/2)+r[1]*tan(a2/2)),
#    F34=(d34*tan(a3/2)*tan(a4/2))/(r[1]*tan(a4/2)+r[2]*tan(a3/2)),
#    newR=min(r[1],F23*r[1],F34*r[1]),//use the smallest radius
#    //now that the radius has been determined, find tangent points and circle centre
#    tangD=newR/tan(a3/2),//distance to the tangent point from p3
#      circD=newR/sin(a3/2),//distance to the circle centre from p3
#    //find the angle from the p3
#    an23=getAngle(p[1],p[2]),//angle from point 3 to 2
#    an34=getAngle(p[3],p[2]),//angle from point 3 to 4
#    //find tangent points
#    t23=[p[2][0]-cos(an23)*tangD,p[2][1]-sin(an23)*tangD],//tangent point between points 2&3
#    t34=[p[2][0]-cos(an34)*tangD,p[2][1]-sin(an34)*tangD],//tangent point between points 3&4
#    //find circle centre
#    tmid=getMidpoint(t23,t34),//midpoint between the two tangent points
#    anCen=getAngle(tmid,p[2]),//angle from point 3 to circle centre
#    cen=[p[2][0]-cos(anCen)*circD,p[2][1]-sin(anCen)*circD]
#  )
#    //circle center by offseting from point 3
#    //determine the direction of rotation
#	debug==1?//if debug in disabled return arc (default)
#    (newR-r[1]):
#	[t23,t34,cen];

#function round3points(rp,fn)=
#  rp[1][2]==0?[[rp[1][0],rp[1][1]]]://return the middle point if the radius is 0
#	let(
#    p=getpoints(rp), //get list of points
#	  r=rp[1][2],//get the centre 3 radii
#    ang=cosineRuleAngle(p[0],p[1],p[2]),//angle between the lines
#    //now that the radius has been determined, find tangent points and circle centre
#	  tangD=r/tan(ang/2),//distance to the tangent point from p2
#    circD=r/sin(ang/2),//distance to the circle centre from p2
#    //find the angles from the p2 with respect to the postitive x axis
#    angleFromPoint1ToPoint2=getAngle(p[0],p[1]),
#    angleFromPoint2ToPoint3=getAngle(p[2],p[1]),
#    //find tangent points
#    t12=[p[1][0]-cos(angleFromPoint1ToPoint2)*tangD,p[1][1]-sin(angleFromPoint1ToPoint2)*tangD],//tangent point between points 1&2
#    t23=[p[1][0]-cos(angleFromPoint2ToPoint3)*tangD,p[1][1]-sin(angleFromPoint2ToPoint3)*tangD],//tangent point between points 2&3
#    //find circle centre
#    tmid=getMidpoint(t12,t23),//midpoint between the two tangent points
#    angCen=getAngle(tmid,p[1]),//angle from point 2 to circle centre
#    cen=[p[1][0]-cos(angCen)*circD,p[1][1]-sin(angCen)*circD] //circle center by offseting from point 2 
#  )
#	[t12,t23,cen];

#function CentreN2PointsArc(p1,p2,cen,mode=0,fn)=
#  /* This function plots an arc from p1 to p2 with fn increments using the cen as the centre of the arc.
#  the mode determines how the arc is plotted
#  mode==0, shortest arc possible 
#  mode==1, longest arc possible
#  mode==2, plotted clockwise
#  mode==3, plotted counter clockwise
#  */
#	let(
#    isCWorCCW=CWorCCW([cen,p1,p2]),//determine the direction of rotation
#    //determine the arc angle depending on the mode
#    p1p2Angle=cosineRuleAngle(p2,cen,p1),
#    arcAngle=
#      mode==0?p1p2Angle:
#      mode==1?p1p2Angle-360:
#      mode==2&&isCWorCCW==-1?p1p2Angle:
#      mode==2&&isCWorCCW== 1?p1p2Angle-360:
#      mode==3&&isCWorCCW== 1?p1p2Angle:
#      mode==3&&isCWorCCW==-1?p1p2Angle-360:
#      cosineRuleAngle(p2,cen,p1),
#    r=pointDist(p1,cen),//determine the radius
#	  p1Angle=getAngle(cen,p1) //angle of line 1
#  )
#  [for(i=[0:fn])
#  let(angleIncrement=(arcAngle/fn)*i*isCWorCCW)
#  [cos(p1Angle+angleIncrement)*r+cen.x,sin(p1Angle+angleIncrement)*r+cen.y]];
