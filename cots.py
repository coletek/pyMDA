import math
from solid import *
from solid.utils import *
from settings_common import *
from helpers import *

#==============================================================================
#
# Electronics Parts
#
#==============================================================================

# https://app.adam-tech.com/products/download/data_sheet/201605/ph1-xx-ua-data-sheet.pdf
def pcb_header(pitch = 2.54, number_of_pins = 2):

    pcb_header_width = 2.5
    pcb_header_length = pitch * number_of_pins
    pcb_header_height = 2.5
    pcb_header_thickness = (8.85 - 6.35) / 2.0
    pcb_header_pin_size = 0.64
    pcb_header_pin_length = 3.05
    pcb_header_pin_length_overall = pcb_header_pin_length + pcb_header_height + 6.0
    
    # enclosure
    p = color(BlackPaint) (cube([pcb_header_width, pcb_header_length, pcb_header_height], center = True))
    p = translate([0, 0, pcb_header_height / 2.0]) (p)
    
    # pins
    l = color(Aluminum) (cube([pcb_header_pin_size, pcb_header_pin_size, pcb_header_pin_length_overall], center = True))
    l = matrix_copy_simple(l, 0, pitch, 1, number_of_pins)
    p += translate([0, -(number_of_pins - 1) / 2.0 * pitch, pcb_header_pin_length_overall / 2.0 - pcb_header_pin_length]) (l)
    
    return p

# https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6025/302-S.pdf
def pcb_header_dual(pitch = 2.54, number_of_pins = 2):

    pcb_header_dual_width = 8.85
    pcb_header_dual_length = pitch * (number_of_pins / 2 - 1) + 7.66
    pcb_header_dual_height = 8.85
    pcb_header_thickness = (8.85 - 6.35) / 2.0
    pcb_header_pin_size = 0.64
    pcb_header_pin_length = 3.0
    pcb_header_pin_length_overall = pcb_header_pin_length + pcb_header_dual_height
    
    # enclosure
    o = cube([pcb_header_dual_width, pcb_header_dual_length, pcb_header_dual_height], center = True)
    i = cube([pcb_header_dual_width - pcb_header_thickness * 2.0,
              pcb_header_dual_length - pcb_header_thickness * 2.0, pcb_header_dual_height], center = True)
    p = o - translate([0, 0, pcb_header_thickness]) (i)
    p = color(BlackPaint) (p)
    
    # pins
    l = color(Aluminum) (cube([pcb_header_pin_size, pcb_header_pin_size, pcb_header_pin_length_overall], center = True))
    l = matrix_copy_simple(l, pitch, pitch, 2, int(number_of_pins / 2))
    p += translate([-pitch / 2.0,
                    -(number_of_pins / 2.0 - 1) / 2.0 * pitch,
                    pcb_header_pin_length_overall / 2.0 - pcb_header_dual_height / 2.0 - pcb_header_pin_length]) (l)
    
    return p

# https://www.bourns.com/docs/Product-Datasheets/3306.pdf - 3306K
def pot_side(segments_count):

    pot_wall_thickness = 1.0
    pot_dia = 6.81
    pot_length = 4.5
    pot_height = 8.4
    pot_pin_width = 0.8
    pot_pin_length = pot_pin_width / 2.0
    pot_pin_height = 3.0
    pot_pin_pitch_x = 5.0
    pot_pin_pitch_y = 2.5

    # blue body
    p = rotate(90, [1, 0, 0]) (cylinder(d = pot_dia, h = pot_length, center = True, segments = segments_count))
    # cut cross for aesthetics
    cut_width = 1.0
    cut_length = pot_length / 2.0
    cut_height = 5.0
    c = translate([0, pot_length / 2.0, 0]) (cube([cut_width, cut_length, cut_height], center = True))
    p -= c + rotate(90, [0, 1, 0]) (c)
    p = color(Blue) (translate([0, 0.01, 0]) (p))

    # white backplate
    p += color(White) (translate([0,
                                  pot_wall_thickness / 2.0 - pot_length / 2.0,
                                  pot_dia / 2.0 - pot_height / 2.0]) (cube([pot_dia, pot_wall_thickness, pot_height], center = True)))

    p = (translate([0, pot_length / 2.0, pot_height - pot_dia / 2.0]) (p))
    
    # pins
    l = color(Aluminum) (cube([pot_pin_width, pot_pin_length, pot_pin_height], center = True))
    p += translate([-pot_pin_pitch_x / 2.0, 0, -pot_pin_height / 2.0]) (l) + \
        translate([pot_pin_pitch_x / 2.0, 0, -pot_pin_height / 2.0]) (l) + \
        translate([0, -pot_pin_pitch_y, -pot_pin_height / 2.0]) (l)

    # joint center pin for aesthetics
    p += translate([0, pot_pin_height / 2.0 - pot_pin_pitch_y - pot_pin_length / 2.0, pot_pin_length / 2.0]) (rotate(90, [1, 0, 0]) (l))

    return p
    

# https://www.digikey.com/en/products/detail/littelfuse-inc/0297003-WXNV/146575
# https://www.littelfuse.com/media?resourcetype=datasheets&itemid=42c9dd21-a88e-4328-8e67-2f832444faf1&filename=littelfuse_datasheet_297_mini32v.pdf
def fuse_mini():

    mini_fuse_width = 3.8
    mini_fuse_length = 10.9
    mini_fuse_height = 8.8
    mini_fuse_pin_width = 0.8
    mini_fuse_pin_length = 2.8
    mini_fuse_pin_height = 7.5
    
    # body
    b = color(Transparent) (cube([mini_fuse_width, mini_fuse_length, mini_fuse_height], center = True))
    p = translate([0, 0, mini_fuse_height / 2.0]) (b)

    # leg
    l = color(Aluminum) (cube([mini_fuse_pin_width, mini_fuse_pin_length, mini_fuse_pin_height], center = True))
    p += translate([0, mini_fuse_length / 2.0 - mini_fuse_pin_length / 2.0, -mini_fuse_pin_height / 2.0]) (l) + \
        translate([0, -mini_fuse_length / 2.0 + mini_fuse_pin_length / 2.0, -mini_fuse_pin_height / 2.0]) (l)
    
    return p

# https://www.digikey.com/en/products/detail/keystone-electronics/3568/2137306
# https://www.keyelco.com/userAssets/file/M65p42.pdf
def fuse_holder_mini():

    mini_fuse_holder_width = 6.73
    mini_fuse_holder_length = 16.0
    mini_fuse_holder_height = 7.37
    mini_fuse_holder_pitch_x = 3.41
    mini_fuse_holder_pitch_y = 9.9

    p = cube([mini_fuse_holder_width, mini_fuse_holder_length, mini_fuse_holder_height], center = True)
    p = translate([0, 0, mini_fuse_holder_height / 2.0]) (p)

    return color(BlackPaint) (p)

def fuse_holder_and_fuse_mini_assembly():

    mini_fuse_holder_and_fuse_height = 17.0 # manually measured

    mini_fuse_height = 8.8 # copied from fuse_mini() - this is just an example of the redesign work required for this lib
    
    p = fuse_holder_mini()

    p += translate([0, 0, -mini_fuse_height + mini_fuse_holder_and_fuse_height]) (fuse_mini())

    return p

# https://www.raspberrypi-spy.co.uk/2012/03/mechanical-data-dimensions/
def rpi3():
    p = import_stl("cots/rpi3.stl")

    rpi3_width = 56.0
    rpi3_length = 85.0
    rpi3_width_offset = -1.57
    rpi3_length_offset = -2.76
    rpi3_mounting_holes_width_pitch = 49.0 # FYI
    rpi3_mounting_holes_length_pitch = 58.0 # FYI
    rpi3_mounting_holes_offset = 3.5 # FYI
    
    p = translate([rpi3_length_offset - rpi3_length / 2.0, rpi3_width_offset - rpi3_width / 2.0, -1.6]) (p)

    return color(Aluminum) (p)

# https://grabcad.com/library/raspberry-pi-display-7-1
# https://raspiworld.com/images/other/drawings/Raspberry-Pi-7in-Touchscreen-Display.jpg
def rpi_display():
    p = import_stl("cots/rpi-display.stl")

    rpi_display_width = 110.8
    rpi_display_length = 193.0
    rpi_display_width_offset = 51.3
    rpi_display_length_offset = 69.5
    rpi_display_mounting_holes_width_pitch = 66.0 # FYI
    rpi_display_mounting_holes_length_pitch = 126.0 # FYI
    rpi_display_mounting_holes_offset = 33.5 # FYI

    p = translate([rpi_display_width_offset + rpi_display_width / 2.0, rpi_display_length_offset - rpi_display_length / 2.0, -1.8]) (p)
    
    return color(Aluminum) (p)

# https://www.cadcrowd.com/3d-models/nvidia-jetson-nano-development-pc-board-assembly
# https://static.cytron.io/image/catalog/products/JN-ORNN-8G-DK/JN-ORNN-8G-DK-dimensiona.jpg
def nvidia_jetson_nano():
    p = import_stl("cots/p3450-p3449-a02-p3448-a02.stl")

    nvidia_jetson_nano_width = 79.0
    nvidia_jetson_nano_length = 100.0
    nvidia_jetson_nano_mounting_holes_width_pitch = 58.0 # FYI
    nvidia_jetson_nano_mounting_holes_length_pitch = 86.0 # FYI
    nvidia_jetson_nano_mounting_holes_offset = 4.0 # FYI
    
    p = translate([nvidia_jetson_nano_mounting_holes_offset - nvidia_jetson_nano_length / 2.0,
                   17.0 - nvidia_jetson_nano_width / 2.0,
                   0]) (p)
    
    return color(Aluminum) (p)

#@bom_part("2MP/1080p USB Camera", 26.0)
# https://www.raspberrypi.com/documentation/accessories/camera.html
def pcb_camera(pcb_width, pcb_length, pcb_thickness,
               pcb_mounting_hole_dia, pcb_mounting_pitch_width, pcb_mounting_pitch_length,
               pcb_mounting_hole_offset_width, pcb_mounting_hole_offset_length, 
               lens_dia, lens_height, lens_offset_width, lens_offset_length,
               sensor_width, sensor_height, sensor_thickness, 
               focal_length, fov_dist, enable_fov,
               segments_count):
    
    b = plate_width_mounting_holes(pcb_width, pcb_length, pcb_thickness,
                                   pcb_mounting_hole_dia, pcb_mounting_pitch_width, pcb_mounting_pitch_length,
                                   pcb_mounting_hole_offset_width, pcb_mounting_hole_offset_length, 
                                   segments_count)
    b = color(colour_pcb)
    
    b = translate([lens_offset_width, lens_offset_length, 0]) (b)
    
    lens = color(BlackPaint) (cylinder(d = lens_dia, h = lens_height, center = True, segments = segments_count))

    p = translate([0, 0, pcb_thickness / 2.0]) (b) + \
        translate([0, 0, lens_height / 2.0 + pcb_thickness]) (lens)

    if enable_fov:

        fov_width = 2.0 * math.atan2(sensor_width, 2 * focal_length)
        fov_height = 2.0 * math.atan2(sensor_height, 2 * focal_length)
        print ("H-FOV %f" % math.degrees(fov_width))
        print ("V-FOV %f" % math.degrees(fov_height))
        
        fov_start = cube([sensor_width, sensor_height, 0.1], center = True)
        fov_end = cube([fov_dist * math.tan(fov_width / 2.0) * 2.0, fov_dist * math.tan(fov_height / 2.0) * 2.0, 0.1], center = True)
        fov = color([0.5, 0.5, 0.5, 0.5]) (hull() (fov_start, translate([0, 0, fov_dist]) (fov_end)))
        p += translate([0, 0, 0.1 / 2.0 + pcb_thickness + sensor_thickness + focal_length]) (fov)
    
    return p

#==============================================================================
#
# Mechanical Parts
#
#==============================================================================

def magnet_coin(dia, thickness, segments_count):

    p = cylinder(d = dia, h = thickness, center = True, segments = segments_count)

    p = translate([0, 0, thickness / 2.0]) (p)

    return p

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

#==============================================================================
#
# Bearings
#
#==============================================================================

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

#==============================================================================
#
# DC Motors
#
#==============================================================================

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

#==============================================================================
#
# Servo Motors
#
#==============================================================================

def servo_rds3225(a = 0.0, include_support_bracket = False):

    # https://www.aliexpress.com/item/32907625266.html
    servo_rds3225_width = 20.0
    servo_rds3225_length = 40.0
    servo_rds3225_height = 40.5
    servo_rds3225_axle_pos = 11.0
    servo_rds3225_axle_mount_height = 1.5
    servo_rds3225_axle_gearhead_height = 4.0
    servo_rds3225_axle_wheel_gap = 2.8
    servo_rds3225_bracket_width = 20.0
    servo_rds3225_bracket_length = 57.0
    servo_rds3225_bracket_thickness = 2.0
    servo_rds3225_bracket_screw_head_height = 1.6
    servo_rds3225_cable_mount_height = 6.0

    b = color(Aluminum) (import_stl("cots/RDS3225-bracket.stl"))

    b = rotate(180, [1, 0, 0]) (b)
    b = rotate(90, [0, 0, 1]) (b)
    
    b = translate([-servo_rds3225_width / 2.0, -servo_rds3225_axle_pos, 0]) (b)
    
    s = color(BlackPaint) (import_stl("cots/RDS3225-servo.stl"))

    if include_support_bracket:
        s += color(Aluminum) (import_stl("cots/RDS3225-bracket-support.stl"))

    s = rotate(180, [1, 0, 0]) (s)
    s = rotate(90, [0, 0, 1]) (s)
    
    s = translate([-servo_rds3225_width / 2.0, -servo_rds3225_axle_pos, 0]) (s)

    p = s + rotate(a, [0, 0, 1]) (b)

    p = translate([0, 0, -servo_rds3225_axle_mount_height / 2.0]) (p)
    
    return p

#==============================================================================
#
# Stepper Motors
#
#==============================================================================

def stepper_driver():
    return translate([-86.0 / 2.0, -55.0 / 2.0, -20.0 / 2.0]) (
        cube([86, 55, 20])
    )

def stepper(nema_type = 17, length = 24.0, segments_count = None):

    if nema_type == 17:
        width = 42
        bore = 5
        bore_length = 14#24
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

#==============================================================================
#
# Actuators
#
#==============================================================================

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

