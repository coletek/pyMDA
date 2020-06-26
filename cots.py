from solid import *
from solid.utils import *
from settings_common import *

def stepper_driver():
    return translate([-86.0 / 2.0, -55.0 / 2.0, -20.0 / 2.0]) (
        cube([86, 55, 20])
    )

def stepper(nema_type = 17, length = 24.0, segments_count = None):

    if nema_type == 17:
        width = 42
        bore = 5
        bore_length = 24
        mounting_hole_pitch = 31
        mounting_hole_size = m3_tap_hole_size
        mounting_hole_depth = 4
    else:
        print ("TODO: NEMA TYPE NOT DEFINED")
        
    block = cube([width, length, width], center = True)
    axle = cylinder(d = bore, h = bore_length, segments = segments_count)
    mounting_hole = cylinder(d = mounting_hole_size, h = mounting_hole_depth + 1, segments = segments_count)

    mounting_holes = translate([mounting_hole_pitch / 2.0, 1, mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
                     translate([mounting_hole_pitch / 2.0, 1, -mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
                     translate([-mounting_hole_pitch / 2.0, 1, mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
                     translate([-mounting_hole_pitch / 2.0, 1, -mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole))
                     
    
    p = translate([0, -length / 2.0, 0]) (block) + \
        rotate(90 + 180, [1, 0, 0]) (axle) - \
        mounting_holes
    
    return color(BlackPaint) (p)

def pulley(angle = 0):
    return rotate(angle, [1, 0, 0]) (
        translate([-6.95, -7, -7]) (
            color(Aluminum) (
                import_stl("cots/GT2_16T.STL")
            )
        )
    )

def stepper_and_pulley(angle = 0.0, nema_type = 17, length = 24.0, segments_count = None):
    return union()(
        stepper(nema_type, length, segments_count),
        translate([0, 13, 0]) (
            rotate(-270, [0, 0, 1]) (
                pulley(angle)
            )
        )
    )

def bearing(id, od, thickness):
    outter = cylinder(d = od, h = thickness)
    inner = cylinder(d = id, h = thickness + 2)
    p = outter - translate([0, 0, -1]) (inner)
    return p

def collar(id, thickness, width, connection_gap, connection_hole_dia, connection_thickness, connection_height = 0.0, connection_gap_closed = 0.0):

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

@bom_part("Bearing Pillow Block (UCP201)", 22.42, 'A$')
def bearing_pillow_block_ucp201():
    return color(BlackPaint) (rotate(90, [0, 1, 0]) (rotate(90, [0, 0, 1]) (translate([102.9, -77.5, -169.0]) (import_stl("cots/ucp201.stl")))))

@bom_part("Bearing Pillow Block (UCP204)", 27.19, 'A$')
def bearing_pillow_block_ucp204():
    return color(BlackPaint) (import_stl("cots/ucp204.stl"))

@bom_part("Linear Actuator (PA-14P)", 138.99)
def linear_actuator_pa14p(size = 2.0 * inch_to_mm, stroke = 0.0, actuator_dist_to_mount = 0.78 * inch_to_mm, actuator_dist_to_mount2 = 0.4 * inch_to_mm, actuator_width = 1.57 * inch_to_mm):
    # TODO: make stroke work - requires replacing STL files with custom OpenSCAD model
    # until then, we can hack it via using size
    size += stroke
    p = import_stl("cots/PA-14P-2.stl")
    if size == 4.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-4.stl")
    if size == 6.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-6.stl")
    if size == 8.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-8.stl")
    if size == 10.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-10.stl")
    if size == 12.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-12.stl")
    if size == 18.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-18.stl")
    if size == 24.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-24.stl")
    if size == 30.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-30.stl")
    if size == 40.0 * inch_to_mm:
        p = import_stl("cots/PA-14P-40.stl")
    return color(BlackPaint) (translate([-actuator_dist_to_mount, actuator_dist_to_mount2, actuator_width / 2.0]) (p))

@bom_part("Linear Actuator Mounting Bracket (BRK-14)", 8.5)
def linear_actuator_mounting_bracket_brk14(actuator_mounting_bracket_width = 1.04 * inch_to_mm, actuator_mounting_bracket_length = 2.3 * inch_to_mm, actuator_mounting_bracket_length_to_axle = 0.32 * inch_to_mm, actuator_mounting_bracket_height_to_axle = 1.43 * inch_to_mm):
    return color(BlackPaint) (rotate(-90, [0, 0, 1]) (rotate(90, [0, 1, 0]) (translate([15.62 - actuator_mounting_bracket_width / 2.0, 11.899 - actuator_mounting_bracket_height_to_axle, actuator_mounting_bracket_length - actuator_mounting_bracket_length_to_axle]) (import_stl("cots/BRK-14.stl")))))

# waiting on revised 3D model
@bom_part("Linear Actuator Mounting Bracket (BRK-03)", 9.5)
def linear_actuator_mounting_bracket_brk03(actuator_mounting_bracket_length = 55.88):
    return color(BlackPaint) (translate([10.0, (0.79 + 0.75 / 2.0 + 5.16 + 0.11) * inch_to_mm + 1, 0]) (rotate(90, [1, 0, 0]) (rotate(90, [0, 0, 1]) (scale(20.066/50.8386) (import_stl("cots/BRK-03.stl"))))))

# waiting on revised 3D model
#@bom_part("Linear Actuator (PA-12-10626912T)", 78.60)
def linear_actuator_pa12t(actuator_small_dist_to_mount = 4.85):
    return color(BlackPaint) (translate([0, -actuator_small_dist_to_mount, 0]) (rotate(-90, [0, 0, 1]) (rotate(-90, [1, 0, 0]) (import_stl("cots/PA-12-1.06.stl")))))

def linear_actuator_and_bracket(size, stroke, angle, explode_dist):
    return rotate(angle, [0, 0, 1]) (linear_actuator_pa14p(size, stroke)) + translate([0, -explode_dist, 0]) (linear_actuator_mounting_bracket_brk14())

def door(door_width, door_thickness, door_height):
    p = cube([door_width, door_thickness, door_height], center = True)
    p = translate([0, 0, door_height / 2.0]) (p) 
    p = color(Oak) (p)
    return p

