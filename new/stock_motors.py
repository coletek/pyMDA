import math
from solid import *
from solid.utils import *

from pyMDA.new.core import *

class ShaftKey(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def create(self):
        k = translate([-self.config['dia'] / 2.0 - 1.0,
                       self.config['dia'] / 2.0 - self.config['key_cut'],
                       self.config['length'] - self.config['key_length']]) (cube([self.config['dia'] + 2.0,
                                                                                  self.config['dia'],
                                                                                  self.config['key_length'] + 1.0]))
        s = cylinder(d = self.config['dia'], h = self.config['length'], segments = self.segments_count)
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

        s = ShaftKey(self.config['shaft']).create()
        
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
        
        s = ShaftKey(self.config['shaft']).create()

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
        super().__init__()
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
    
    def __init__(self, config, a = 0.0, include_support_bracket = False):
        super().__init__()
        self.config = config
        self.a = a
        self.include_support_bracket = include_support_bracket

    def create(self):

        b = color(Aluminum) (import_stl("cots/RDS3225-bracket.stl"))

        b = rotate(180, [1, 0, 0]) (b)
        b = rotate(90, [0, 0, 1]) (b)
        
        b = translate([-self.config['width'] / 2.0, -self.config['axle_pos'], 0]) (b)
        
        s = color(BlackPaint) (import_stl("cots/RDS3225-servo.stl"))
        
        if self.include_support_bracket:
            s += color(Aluminum) (import_stl("cots/RDS3225-bracket-support.stl"))

        s = rotate(180, [1, 0, 0]) (s)
        s = rotate(90, [0, 0, 1]) (s)
    
        s = translate([-self.config['width'] / 2.0, -self.config['axle_pos'], 0]) (s)

        p = s + rotate(self.a, [0, 0, 1]) (b)

        p = translate([0, 0, -self.config['axle_mount_height'] / 2.0]) (p)
    
        return p

#==============================================================================
#
# Stepper Motors
#
#==============================================================================

class StepperDriver(Component):

    def __init__(self, config):
        super().__init__()
        self.config = config
    
    def create(self):
        return translate([-self.config['width'] / 2.0, -self.config['length'] / 2.0, -self.config['height'] / 2.0]) (
            cube([self.config['width'], self.config['length'], self.config['height']])
        )

class Stepper(Component):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def create(self):
        
        if self.config['nema_type'] == 17:
            self.config['width'] = 42
            self.config['bore'] = 5
            self.config['bore_length'] = 14#24
            self.config['mounting_hole_pitch'] = 31
            self.config['mounting_hole_size'] = 2.5 #m3_tap_hole_size
            self.config['mounting_hole_depth'] = 4
        else:
            print ("TODO: NEMA TYPE NOT DEFINED")
        
        block = cube([self.config['width'], self.config['length'], self.config['width']], center = True)
        axle = cylinder(d = self.config['bore'], h = self.config['bore_length'], segments = self.segments_count)
        mounting_hole = cylinder(d = self.config['mounting_hole_size'], h = self.config['mounting_hole_depth'] + 1, segments = self.segments_count)
        
        mounting_holes = translate([self.config['mounting_hole_pitch'] / 2.0,
                                    1,
                                    self.config['mounting_hole_pitch'] / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
            translate([self.config['mounting_hole_pitch'] / 2.0, 1, -self.config['mounting_hole_pitch'] / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
            translate([-self.config['mounting_hole_pitch'] / 2.0, 1, self.config['mounting_hole_pitch'] / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole)) + \
            translate([-self.config['mounting_hole_pitch'] / 2.0, 1, -self.config['mounting_hole_pitch'] / 2.0]) (rotate(90, [1, 0, 0]) (mounting_hole))
    
        p = translate([0, -self.config['length'] / 2.0, 0]) (block) + \
            rotate(90 + 180, [1, 0, 0]) (axle) - \
            mounting_holes
    
        return color(BlackPaint) (p)

class Pulley(Component):

    def __init__(self, config, angle = 0):
        super().__init__()
        self.config = config
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

    def __init__(self, stepper_config, pulley_config, angle = 0.0):
        super().__init__()
        self.stepper_config = stepper_config
        self.pulley_config = pulley_config
        self.angle = angle
        
    def create(self):
        return union()(
            Stepper(self.stepper_config).create(),
            translate([0, 13, 0]) (
                rotate(-270, [0, 0, 1]) (
                    Pulley(self.pulley_config, self.angle).create()
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
    
    def __init__(self, config, stroke):
        super().__init__()
        self.config = config
        self.stroke = stroke
        
    def create(self):
        inch_to_mm = 25.4
        self.config['size'] += self.stroke
        p = import_stl("cots/PA-14P-2.stl")
        if self.config['size'] == 4.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-4.stl")
        if self.config['size'] == 6.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-6.stl")
        if self.config['size'] == 8.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-8.stl")
        if self.config['size'] == 10.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-10.stl")
        if self.config['size'] == 12.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-12.stl")
        if self.config['size'] == 18.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-18.stl")
        if self.config['size'] == 24.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-24.stl")
        if self.config['size'] == 30.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-30.stl")
        if self.config['size'] == 40.0 * inch_to_mm:
            p = import_stl("cots/PA-14P-40.stl")
        return color(BlackPaint) (translate([-self.config['dist_to_mount'], self.config['dist_to_mount2'], self.config['width'] / 2.0]) (p))

class LinearActuatorMountingBracketBRK14(Component):
    '''@bom_part("Linear Actuator Mounting Bracket (BRK-14)", 8.5)'''
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        return color(BlackPaint) (rotate(-90, [0, 0, 1]) (rotate(90, [0, 1, 0]) (translate([15.62 - self.config['width'] / 2.0, 11.899 - self.config['height_to_axle'], self.config['length'] - self.config['length_to_axle']]) (import_stl("cots/BRK-14.stl")))))
    
class LinearActuatorMountingBracketBRK03(Component):
    # waiting on revised 3D model
    '''@bom_part("Linear Actuator Mounting Bracket (BRK-03)", 9.5)'''
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def create(self):
        inch_to_mm = 25.4
        return color(BlackPaint) (translate([10.0, (0.79 + 0.75 / 2.0 + 5.16 + 0.11) * inch_to_mm + 1, 0]) (rotate(90, [1, 0, 0]) (rotate(90, [0, 0, 1]) (scale(20.066/50.8386) (import_stl("cots/BRK-03.stl"))))))
    
class LinearActuatorPA12T(Component):
    # waiting on revised 3D model
    #@bom_part("Linear Actuator (PA-12-10626912T)", 78.60)
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        return color(BlackPaint) (translate([0, -self.config['dist_to_mount'], 0]) (rotate(-90, [0, 0, 1]) (rotate(-90, [1, 0, 0]) (import_stl("cots/PA-12-1.06.stl")))))

class LinearActuatorAndBracket(Component):

    def __init__(self, actuator_config, bracket_config, config):
        super().__init__()
        self.actuator_config = actuator_config
        self.bracket_config = bracket_config
        self.config = config
        
    def create(self):
        return rotate(self.config['angle'], [0, 0, 1]) (LinearActuatorPA14P(self.actuator_config, self.config['stroke']).create()) + translate([0, -self.config['explode_dist'], 0]) (LinearActuatorMountingBracketBRK14(self.bracket_config).create())
