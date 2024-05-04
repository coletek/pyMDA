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
