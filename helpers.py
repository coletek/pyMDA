from solid import *
from solid.utils import *
import math
import numpy as np

def prism(l, w, h):
    return polyhedron(
        points=[[0,0,0], [l,0,0], [l,w,0], [0,w,0], [0,w,h], [l,w,h]],
        faces=[[0,1,2,3],[5,4,3,2],[0,4,5,1],[0,3,4],[5,2,1]]
    )

def cam_profile(height, start_radius, start_angle, end_radius, end_angle, increment = 0.01, center = True):

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

    return linear_extrude(height, center = center) (polygon(points=points))

def cam_profile_find_radius(target_angle, start_radius, start_angle, end_radius, end_angle, increment = 0.01):

    # TODO: this could/should be replaced with a single equation - can't think of the solution right now.
    
    angle_range = end_angle - start_angle

    radius_step = (end_radius - start_radius) / (angle_range / increment)

    # end_angle + 1deg is required to complete the loop
    radius = start_radius
    for i in np.arange(start_angle, end_angle + math.radians(1.0), increment):
        radius += radius_step
        #print math.degrees(target_angle), math.degrees(i), radius
        if round(math.degrees(i)) == round(math.degrees(target_angle)):
            return radius

    return False

def cube_curved_sides(x, y, z, corner_radius, side_count, segments_count):

    # alternative approach to minkowski, so it imports into OpenSCAD and export as STEP
    # TODO: support non-center option
    # using hull() still requires high segments - perhaps use rotate_extrude instead

    corner_sq = cube([corner_radius, corner_radius, z], center = True)
    corner_round = translate([0, 0, -z / 2.0]) (cylinder(segments = segments_count, r = corner_radius, h = z))

    if side_count == 4:
        return hull() (
            translate([x / 2.0 - corner_radius, y / 2.0 - corner_radius, 0]) (corner_round),
            translate([x / 2.0 - corner_radius, -y / 2.0 + corner_radius, 0]) (corner_round),
            translate([-x / 2.0 + corner_radius, y / 2.0 - corner_radius, 0]) (corner_round),
            translate([-x / 2.0 + corner_radius, -y / 2.0 + corner_radius, 0]) (corner_round),
        )
    elif side_count == 2:
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


def cube_curved_edges(x, y, z, corner_radius, segments_count, center):

    # alternative approach to minkowski, so it imports into OpenSCAD and export as STEP
    # using hull() still requires high segments - perhaps use rotate_extrude instead
    
    if center:
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

def ring(r, thickness, segments_count):
    return rotate_extrude(convexity = 10, segments = segments_count) (translate([r, 0, 0]) (circle(d = thickness, segments = segments_count)))

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

def washer(dia, hole_dia, thickness, segments_count, center):
    rod = cylinder(segments = segments_count, d = dia, h = thickness, center = center)
    hole = cylinder(segments = segments_count, d = hole_dia, h = thickness + 2, center = center)
    if center:
        return rod - translate([0, 0, 0]) (hole)
    else:
        return rod - translate([0, 0, -1]) (hole)

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

    return p

def slot(width, length, height, segments_count):
    
    hole = translate([0, 0, -(height + 2.0) / 2.0]) (cylinder(segments = segments_count, r = width / 2.0, h = height + 2.0))
    
    return hull() (
        translate([0, -length / 2.0, 0]) (hole),
        translate([0, length / 2.0, 0]) (hole),
    )

def slot_array(length, slot_width, slot_length, slot_count, height, segments_count):
    gap = (length - slot_count * (slot_length + slot_width)) / (slot_count + 1.0)

    y = - length / 2.0 + gap + (slot_length + slot_width) / 2.0
    p = translate([0, y, 0]) (slot(slot_width, slot_length, height, segments_count))
    for i in range(slot_count - 1):
        y += gap + (slot_length + slot_width)
        p += translate([0, y, 0]) (slot(slot_width, slot_length, height, segments_count))
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
