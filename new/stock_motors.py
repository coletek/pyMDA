import math
from solid import *
from solid.utils import *
from core import *

class ShaftKey(Component):

    def __init__(self, dia, length, key_cut, key_length):
        super().__init__()
        self.dia = dia
        self.length = length
        self.key_cut = key_cut
        self.key_length = key_length
        
    def create(self):
        k = translate([-self.dia / 2.0 - 1.0,
                       self.dia / 2.0 - self.key_cut,
                       self.length - self.key_length]) (cube([self.dia + 2.0, self.dia, self.key_length + 1.0]))
        s = cylinder(d = self.dia, h = self.length, segments = self.segments_count)
        p = s - k
        p = color(Steel) (p)
        return p

class MotorDC(Component):
    ''' https://www.omc-stepperonline.com/brushed-12v-dc-gear-motor-3kg-cm-3rpm-w-828-1-worm-gearbox-wga-2430123100-g828 '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def create(self):
        m = cylinder(d = self.config['dia'], h = self.config['length'], segments = self.segments_count)
        m = color(Aluminum) (m)
        s = ShaftKey(self.config['shaft_dia'], self.config['shaft_length'], self.config['shaft_key_cut'], self.config['shaft_key_length']).create()
        p = m + translate([0, 0, self.config['length']]) (s)
        p = translate([0, 0, -self.config['length']]) (p)
        return p

class GearboxWorm(Component):
    ''' https://www.omc-stepperonline.com/brushed-12v-dc-gear-motor-3kg-cm-3rpm-w-828-1-worm-gearbox-wga-2430123100-g828 '''

    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        b = cube([self.config['width'], self.config['length'], self.config['height']])

        b = color(Aluminum) (b)
        
        s = ShaftKey(self.config['shaft_dia'], self.config['shaft_length'], self.config['shaft_key_cut'], self.config['shaft_key_length']).create()

        m3_tap_hole_size = 2.5
        h = cylinder(d = m3_tap_hole_size, h = self.config['height'] / 2.0, segments = self.segments_count)
    
        hp = translate([-self.config['width_pitch'] / 2.0, -self.config['length_pitch'] / 2.0, 0]) (h) + \
            translate([self.config['width_pitch'] / 2.0, -self.config['length_pitch'] / 2.0, 0]) (h) + \
            translate([-self.config['width_pitch'] / 2.0, self.config['length_pitch'] / 2.0, 0]) (h) + \
            translate([self.config['width_pitch'] / 2.0, self.config['length_pitch'] / 2.0, 0]) (h)
        
        y = self.config['length_pitch'] / 2.0 - self.config['shaft_pos'] + self.config['length_pitch_pos']
        p = translate([-self.config['width'] / 2.0, -self.config['shaft_pos'], 0]) (b) + \
            translate([0, 0, self.config['height']]) (s) - \
            translate([0, y, self.config['height'] / 2.0 + 1.0]) (hp)
        
        p = translate([0, 0, -self.config['height']]) (p)
        
        return p

class MotorDCwGearboxWorm(Assembly):
    ''' https://www.omc-stepperonline.com/brushed-12v-dc-gear-motor-3kg-cm-3rpm-w-828-1-worm-gearbox-wga-2430123100-g828 '''
    
    def __init__(self, motor_config, gearbox_config):
        self.motor_config = motor_config
        self.gearbox_config = gearbox_config
        
    def create(self):
        m = MotorDC(self.motor_config).create()
    
        g = GearboxWorm(self.gearbox_config).create()
        
        p = g + translate([-self.motor_config['shaft_dia'] / 2.0,
                           self.gearbox_config['length'] - self.gearbox_config['shaft_pos'],
                           -self.gearbox_config['height'] / 2.0]) (rotate(90, [1, 0, 0]) (m))
        
        return p

#==============================================================================
#
# Servo Motors
#
#==============================================================================

class ServoRDS3225(Component):
    ''' https://www.aliexpress.com/item/32907625266.html '''
    
    def __init__(self, a = 0.0, include_support_bracket = False):
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

class StepperDriver(Component):

    def create(self):
        return translate([-86.0 / 2.0, -55.0 / 2.0, -20.0 / 2.0]) (
            cube([86, 55, 20])
        )

class Stepper(Component):
    def __init__(self, nema_type = 17, length = 24.0):
        self.nema_type = nema_type
        self.length = 24.0
        
    def create(self):
        
        if nema_type == 17:
            self.width = 42
            self.bore = 5
            self.bore_length = 14#24
            self.mounting_hole_pitch = 31
            self.mounting_hole_size = m3_tap_hole_size
            self.mounting_hole_depth = 4
        else:
            print ("TODO: NEMA TYPE NOT DEFINED")
        
        block = cube([self.width, length, self.width], center = True)
        axle = cylinder(d = self.bore, h = self.bore_length, segments = self.segments_count)
        mounting_hole = cylinder(d = self.mounting_hole_size, h = self.mounting_hole_depth + 1, segments = self.segments_count)
        
        mounting_holes = translate([self.mounting_hole_pitch / 2.0, 1, self.mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
            translate([self.mounting_hole_pitch / 2.0, 1, -self.mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
            translate([-self.mounting_hole_pitch / 2.0, 1, self.mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
            translate([-self.mounting_hole_pitch / 2.0, 1, -self.mounting_hole_pitch / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole))
    
        p = translate([0, -self.length / 2.0, 0]) (block) + \
            rotate(90 + 180, [1, 0, 0]) (axle) - \
            mounting_holes
    
        return color(BlackPaint) (p)

class Pulley(Component):

    def __init__(self, angle = 0):
        self.angle = angle
        
    def create(self):
        return rotate(self.angle, [1, 0, 0]) (
            translate([-6.95, -7, -7]) (
                color(Aluminum) (
                    import_stl("cots/GT2_16T.STL")
                )
            )
        )

class StepperAndPulley(Component):

    def __init__(self, angle = 0.0, nema_type = 17, length = 24.0):
        self.angle = angle
        self.nema_type = nema_type
        self.length = length
        
    def create(self):
        return union()(
            Stepper(self.nema_type, self.length).create(),
            translate([0, 13, 0]) (
                rotate(-270, [0, 0, 1]) (
                    pulley(self.angle)
                )
            )
        )

#==============================================================================
#
# Actuators
#
#==============================================================================

class LinearActuatorPA14P(Component):
    '''@bom_part("Linear Actuator (PA-14P)", 138.99)'''
    ''' TODO: make stroke work - requires replacing STL files with custom OpenSCAD model until then, we can hack it via using size'''
    
    
    #def __init__(self, size = 2.0 * inch_to_mm, stroke = 0.0, actuator_dist_to_mount = 0.78 * inch_to_mm, actuator_dist_to_mount2 = 0.4 * inch_to_mm, actuator_width = 1.57 * inch_to_mm):
    #    self.size = size
        # etc
        
    def create(self):
        self.inch_to_mm = 25.4
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

class LinearActuatorMountingBracketBRK14(Component):
    '''@bom_part("Linear Actuator Mounting Bracket (BRK-14)", 8.5)'''
    
    #def __init__(actuator_mounting_bracket_width = 1.04 * inch_to_mm, actuator_mounting_bracket_length = 2.3 * inch_to_mm, actuator_mounting_bracket_length_to_axle = 0.32 * inch_to_mm, actuator_mounting_bracket_height_to_axle = 1.43 * inch_to_mm):
        
    #return color(BlackPaint) (rotate(-90, [0, 0, 1]) (rotate(90, [0, 1, 0]) (translate([15.62 - actuator_mounting_bracket_width / 2.0, 11.899 - actuator_mounting_bracket_height_to_axle, actuator_mounting_bracket_length - actuator_mounting_bracket_length_to_axle]) (import_stl("cots/BRK-14.stl")))))

class LinearActuatorMountingBracketBRK03(Component):
    # waiting on revised 3D model
    '''@bom_part("Linear Actuator Mounting Bracket (BRK-03)", 9.5)'''
    
    def __init__(self, actuator_mounting_bracket_length = 55.88):
        self.actuator_mounting_bracket_length = actuator_mounting_bracket_length
        
    def create(self):
        return color(BlackPaint) (translate([10.0, (0.79 + 0.75 / 2.0 + 5.16 + 0.11) * inch_to_mm + 1, 0]) (rotate(90, [1, 0, 0]) (rotate(90, [0, 0, 1]) (scale(20.066/50.8386) (import_stl("cots/BRK-03.stl"))))))

class LinearActuactorPA12T(Component):
    # waiting on revised 3D model
    #@bom_part("Linear Actuator (PA-12-10626912T)", 78.60)
    
    def __init__(self, actuator_small_dist_to_mount = 4.85):
        self.actuator_small_dist_to_mount = actuator_small_dist_to_mount

    def create(self):
        return color(BlackPaint) (translate([0, -self.actuator_small_dist_to_mount, 0]) (rotate(-90, [0, 0, 1]) (rotate(-90, [1, 0, 0]) (import_stl("cots/PA-12-1.06.stl")))))

class LinearActuatorAndBracket(Component):

    def __init__(self, size, stroke, angle, explode_dist):
        self.size = size
        self.stroke = stroke
        self.angle = angle
        self.explode_dist
        
    def create(self):
        return rotate(self.angle, [0, 0, 1]) (LinearActuatorPA14P(size, stroke)) + translate([0, -self.explode_dist, 0]) (LinearActuatorMountingBracketBRK14())
