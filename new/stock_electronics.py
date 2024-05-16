import math
from solid import *
from solid.utils import *
from core import *
from utilties import *
from plates import *

class PCBHeader(Component):
    ''' https://app.adam-tech.com/products/download/data_sheet/201605/ph1-xx-ua-data-sheet.pdf '''

    def __init__(self, config, pitch = 2.54, number_of_pins = 2):
        super().__init__()
        self.config = config
        self.config['width'] = 2.5
        self.config['length'] = pitch * number_of_pins
        self.config['height'] = 2.5
        self.config['thickness'] = (8.85 - 6.35) / 2.0
        self.config['pin_size'] = 0.64
        self.config['pin_length'] = 3.05
        self.config['pin_length_overall'] = self.config['pin_length'] + self.config['height'] + 6.0
        self.pitch = pitch
        self.number_of_pins = number_of_pins

    def create(self):
            
        # enclosure
        p = color(BlackPaint) (cube([self.config['width'], self.config['length'], self.config['height']], center = True))
        p = translate([0, 0, self.config['height'] / 2.0]) (p)
    
        # pins
        l = color(Aluminum) (cube([self.config['pin_size'], self.config['pin_size'], self.config['pin_length_overall']], center = True))
        l = matrix_copy_simple(l, 0, self.pitch, 1, self.number_of_pins)
        p += translate([0, -(self.number_of_pins - 1) / 2.0 * self.pitch, self.config['pin_length_overall'] / 2.0 - self.config['pin_length']]) (l)
    
        return p

class PCBHeaderDual(Component):
    ''' https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6025/302-S.pdf '''

    def __init__(self, config, pitch = 2.54, number_of_pins = 2):
        super().__init__()
        self.config = config
        self.pitch = pitch
        self.number_of_pins = number_of_pins
        self.config['dual_width'] = 8.85
        self.config['dual_length'] = pitch * (number_of_pins / 2 - 1) + 7.66
        self.config['dual_height'] = 8.85
        self.config['thickness'] = (8.85 - 6.35) / 2.0
        self.config['pin_size'] = 0.64
        self.config['pin_length'] = 3.0
        self.config['pin_length_overall'] = self.config['pin_length'] + self.config['dual_height']

    def create(self):
        # enclosure
        o = cube([self.config['dual_width'], self.config['dual_length'], self.config['dual_height']], center = True)
        i = cube([self.config['dual_width'] - self.config['thickness'] * 2.0,
                  self.config['dual_length'] - self.config['thickness'] * 2.0, self.config['dual_height']], center = True)
        p = o - translate([0, 0, self.config['thickness']]) (i)
        p = color(BlackPaint) (p)
    
        # pins
        l = color(Aluminum) (cube([self.config['pin_size'], self.config['pin_size'], self.config['pin_length_overall']], center = True))
        l = matrix_copy_simple(l, self.pitch, self.pitch, 2, int(self.number_of_pins / 2))
        p += translate([-self.pitch / 2.0,
                        -(self.number_of_pins / 2.0 - 1) / 2.0 * self.pitch,
                        self.config['pin_length_overall'] / 2.0 - self.config['dual_height'] / 2.0 - self.config['pin_length']]) (l)
        
        return p

class POTSide(Component):
    ''' https://www.bourns.com/docs/Product-Datasheets/3306.pdf - 3306K '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):

        # blue body
        p = rotate(90, [1, 0, 0]) (cylinder(d = self.config['dia'], h = self.config['length'], center = True, segments = self.segments_count))
        # cut cross for aesthetics
        cut_width = 1.0
        cut_length = self.config['length'] / 2.0
        cut_height = 5.0
        c = translate([0, self.config['length'] / 2.0, 0]) (cube([cut_width, cut_length, cut_height], center = True))
        p -= c + rotate(90, [0, 1, 0]) (c)
        p = color(Blue) (translate([0, 0.01, 0]) (p))
        
        # white backplate
        p += color(White) (translate([0,
                                      self.config['wall_thickness'] / 2.0 - self.config['length'] / 2.0,
                                      self.config['dia'] / 2.0 - self.config['height'] / 2.0]) (cube([self.config['dia'], self.config['wall_thickness'], self.config['height']], center = True)))
        
        p = (translate([0, self.config['length'] / 2.0, self.config['height'] - self.config['dia'] / 2.0]) (p))
        
        # pins
        l = color(Aluminum) (cube([self.config['pin_width'], self.config['pin_length'], self.config['pin_height']], center = True))
        p += translate([-self.config['pin_pitch_x'] / 2.0, 0, -self.config['pin_height'] / 2.0]) (l) + \
            translate([self.config['pin_pitch_x'] / 2.0, 0, -self.config['pin_height'] / 2.0]) (l) + \
            translate([0, -self.config['pin_pitch_y'], -self.config['pin_height'] / 2.0]) (l)
        
        # joint center pin for aesthetics
        p += translate([0, self.config['pin_height'] / 2.0 - self.config['pin_pitch_y'] - self.config['pin_length'] / 2.0, self.config['pin_length'] / 2.0]) (rotate(90, [1, 0, 0]) (l))
        
        return p
    
class FuseMini(Component):
    ''' 
    https://www.digikey.com/en/products/detail/littelfuse-inc/0297003-WXNV/146575
    https://www.littelfuse.com/media?resourcetype=datasheets&itemid=42c9dd21-a88e-4328-8e67-2f832444faf1&filename=littelfuse_datasheet_297_mini32v.pdf
    '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def create(self):
        
        # body
        b = color(Transparent) (cube([self.config['width'], self.config['length'], self.config['height']], center = True))
        p = translate([0, 0, self.config['height'] / 2.0]) (b)

        # leg
        l = color(Aluminum) (cube([self.config['pin_width'], self.config['pin_length'], self.config['pin_height']], center = True))
        p += translate([0, self.config['length'] / 2.0 - self.config['pin_length'] / 2.0, -self.config['pin_height'] / 2.0]) (l) + \
            translate([0, -self.config['length'] / 2.0 + self.config['pin_length'] / 2.0, -self.config['pin_height'] / 2.0]) (l)
        
        return p

class FuseHolderMini(Component):
    ''' 
    https://www.digikey.com/en/products/detail/keystone-electronics/3568/2137306
    https://www.keyelco.com/userAssets/file/M65p42.pdf
    '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        p = cube([self.config['width'], self.config['length'], self.config['height']], center = True)
        p = translate([0, 0, self.config['height'] / 2.0]) (p)
        return color(BlackPaint) (p)

class FuseMiniAndHolder(Assembly):
    ''' mini_fuse_holder_and_fuse_height = 17 is manually measured '''
    
    def __init__(self, fuse_mini_config, fuse_holder_mini_config, mini_fuse_holder_and_fuse_height = 17.0):
        super().__init__()
        self.fuse_mini_config = fuse_mini_config
        self.fuse_holder_mini_config = fuse_holder_mini_config
        self.mini_fuse_holder_and_fuse_height = mini_fuse_holder_and_fuse_height
            
    def create(self):
        p = FuseHolderMini(self.fuse_holder_mini_config).create()
        p += translate([0, 0, -self.fuse_mini_config['height'] + self.mini_fuse_holder_and_fuse_height]) (FuseMini(self.fuse_mini_config).create())
        return p

class RPI(Component):
    ''' https://www.raspberrypi-spy.co.uk/2012/03/mechanical-data-dimensions/ '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        p = import_stl("cots/rpi3.stl")
        p = translate([self.config['length_offset'] - self.config['length'] / 2.0,
                       self.config['width_offset'] - self.config['width'] / 2.0,
                       -1.6]) (p)
        return color(Aluminum) (p)

class RPIDisplay(Component):
    '''
    https://grabcad.com/library/raspberry-pi-display-7-1
    https://raspiworld.com/images/other/drawings/Raspberry-Pi-7in-Touchscreen-Display.jpg
    '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config

    def create(self):
        p = import_stl("cots/rpi-display.stl")
        p = translate([self.config['width_offset'] + self.config['width'] / 2.0, \
                       self.config['length_offset'] - self.config['length'] / 2.0,
                       -1.8]) (p)
        return color(Aluminum) (p)

class NVidiaJetsonNano(Component):
    '''
    https://www.cadcrowd.com/3d-models/nvidia-jetson-nano-development-pc-board-assembly
    https://static.cytron.io/image/catalog/products/JN-ORNN-8G-DK/JN-ORNN-8G-DK-dimensiona.jpg
    '''
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        

    def create(self):
        p = import_stl("cots/p3450-p3449-a02-p3448-a02.stl")
        p = translate([self.config['mounting_holes_offset'] - self.config['length'] / 2.0,
                       17.0 - self.config['width'] / 2.0,
                       0]) (p)
        return color(Aluminum) (p)

class PCBCamera(Component):
    '''
    @bom_part("2MP/1080p USB Camera", 26.0)
    https://www.raspberrypi.com/documentation/accessories/camera.html
    '''

    def __init__(self, pcb_config, camera_config, fov_dist, enable_fov):
        super().__init__()
        self.pcb_config = pcb_config
        self.camera_config = camera_config
        self.fov_dist = fov_dist
        self.enable_fov = enable_fov

    def create(self):

        b = PlateWithMountingHoles(self.pcb_config).create()
        colour_pcb = [0, 0.549, 0.29]
        b = color(colour_pcb)
        
        b = translate([self.camera_config['lens_offset_width'], self.camera_config['lens_offset_length'], 0]) (b)
        
        lens = color(BlackPaint) (cylinder(d = self.camera_config['lens_dia'], h = self.camera_config['lens_height'], center = True, segments = self.segments_count))
        
        p = translate([0, 0, self.pcb_config['thickness'] / 2.0]) (b) + \
            translate([0, 0, self.camera_config['lens_height'] / 2.0 + self.pcb_config['thickness']]) (lens)
        
        if self.enable_fov:
            
            fov_width = 2.0 * math.atan2(self.camera_config['sensor_width'], 2 * self.camera_config['focal_length'])
            fov_height = 2.0 * math.atan2(self.camera_config['sensor_height'], 2 * self.camera_config['focal_length'])
            print ("H-FOV %f" % math.degrees(fov_width))
            print ("V-FOV %f" % math.degrees(fov_height))
            
            fov_start = cube([self.camera_config['sensor_width'], self.camera_config['sensor_height'], 0.1], center = True)
            fov_end = cube([fov_dist * math.tan(fov_width / 2.0) * 2.0, fov_dist * math.tan(fov_height / 2.0) * 2.0, 0.1], center = True)
            fov = color([0.5, 0.5, 0.5, 0.5]) (hull() (fov_start, translate([0, 0, fov_dist]) (fov_end)))
            p += translate([0, 0, 0.1 / 2.0 + self.camera_config['pcb_thickness'] + self.camera_config['sensor_thickness'] + self.camera_config['focal_length']]) (fov)
    
        return p
        

class LED():
    '''@bom_part("RGB LED (ASMB-MTB1-0A3A2)", 0.98)'''
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def create():
        return color(White) (translate([0, 0, self.config['height'] / 2.0]) (cube([self.config['length'], self.config['width'], self.config['height']], center = True)))

class button_tact():

    def __init__():
        super().__init__()
        self.config = config
        
    def create():
        return color(Aluminum) (translate([0, self.config['length'] / 2.0 + (self.config['length_all'] - self.config['length']), 0]) (rotate(90, [1, 0, 0]) (import_stl("cots/EVQP7-JA-01P.stl"))))

    def pcb_outline():
        return translate([0, self.config['length'] / 2.0 + (self.config['length_all'] - self.config['length']), 0]) (cube([self.config['width'], self.config['length'], self.config['pcb_thickness'] + 2], center = True))

# TODO: PORT BELOW
    
def switch_pins_holes(is_holes = False):

    pin_ground_pitch = 14.2
    
    pin_pitch = 2.0

    if is_holes:
        pin_ground_height = pcb_thickness + 2
        pin_ground_z_offset = 0.0
        pin_ground = cylinder(d = 1.25, h = pin_ground_height, center = True, segments = segments_count)
        pin_height = pcb_thickness + 2
        pin_dia = 0.8
    else:
        pin_ground_height = 2.8
        pin_ground_z_offset = 0.5
        pin_ground = color(Brass) (cube([1.2, 0.4, pin_ground_height], center = True))
        pin_height = pin_ground_height - pin_ground_z_offset
        pin_dia = 0.5

    pin = color(Brass) (cylinder(d = pin_dia, h = pin_height, center = True, segments = segments_count))

    # data pins
    p = translate([0, -pin_pitch / 2.0 - pin_pitch * 2.0, 0]) (pin) + \
        translate([0, -pin_pitch / 2.0 - pin_pitch, 0]) (pin) + \
        translate([0, -pin_pitch / 2.0, 0]) (pin) + \
        translate([0, pin_pitch / 2.0, 0]) (pin) + \
        translate([0, pin_pitch / 2.0 + pin_pitch, 0]) (pin) + \
        translate([0, pin_pitch / 2.0 + pin_pitch * 2.0, 0]) (pin)

    # ground pins
    p += translate([0, -pin_ground_pitch / 2.0, pin_ground_z_offset]) (pin_ground) + \
        translate([0, pin_ground_pitch / 2.0, pin_ground_z_offset]) (pin_ground)

    return p

@bom_part("Switch Slide SP4T (SK-14D01-G 6)", 0.47)
def switch(pos = 0):
    # https://www.digikey.com.au/product-detail/en/c-k/SK-14D01-G-6/CKN10368-ND/2747169

    b = color(Aluminum) (cube([switch_width, switch_length, switch_height], center = True))
    a = color(BlackPaint) (cube([9 + 2, switch_knob_width, switch_knob_width], center = True))

    pin_ground_height = 2.8
    pin_ground_z_offset = 0.5
    pin_height = pin_ground_height - pin_ground_z_offset
    
    p = b + \
        translate([9 / 2.0 - 1, -switch_pos_pitch / 2.0 - switch_pos_pitch + switch_pos_pitch * pos, -switch_height / 2.0 + switch_knob_pos_z]) (a) + \
        translate([0, 0, - switch_height / 2.0 - pin_height / 2.0]) (switch_pins_holes())

    p = translate([0, 0, switch_height / 2.0]) (p)
    
    return p

@bom_part("Battery 14500 800mAh 3.7V (SB2301)", 7.01)
def battery():
    b = color(Blue) (cylinder(d = battery_dia, h = battery_length, center = True, segments = segments_count))

    leg_total_height = battery_leg_height + battery_dia / 2.0
    l = color(Aluminum) (cube([battery_leg_width, leg_total_height, battery_leg_thickness], center = True))

    p = b + \
        translate([0, leg_total_height / 2.0, battery_length / 2.0 + battery_leg_thickness / 2.0]) (l) + \
        translate([0, leg_total_height / 2.0, -battery_length / 2.0 - battery_leg_thickness / 2.0]) (l)
    
    return p
    
@bom_part("Speaker 82dB 23mm (SP-2306Y)", 2.49)
def speaker():
    return color(Steel) (import_stl("cots/SP-2306Y-1.stl"))

@bom_part("Coin Vibration 10000rpm 3V (316040004)", 1.27)
def vibrator():    
    return color(Steel) (translate([0, 0, vibrator_thickness / 2.0]) (cylinder(d = vibrator_dia, h = vibrator_thickness, center = True, segments = segments_count) + \
                        translate([vibrator_dia / 2.0 + vibrator_connector_length / 2.0 - 1, 0, 0]) (cube([vibrator_connector_length + 2, vibrator_connector_width, 2.7], center = True))))

@bom_part("Wireless Charging Coil (IWAS3827ECEB100J50)", 1.8)
def coil():
    # TODO: revise to include backplate
    return color([0.722, 0.451, 0.20]) (translate([-21.5, 69.8, -46.72]) (rotate(90, [1, 0, 0]) (import_stl("cots/IWAS-3827EC-50.stl"))))

def magnet_connector_pins_holes(is_holes = False):

    pin_pitch = 2.2
    pin_ground_pitch = 10.0
    
    if is_holes:
        pin_height = pcb_thickness + 2
        pin_dia = 0.9
        pin_ground_dia = 1.15
    else:
        pin_height = 1.15 + magnet_connector_pins_extra_height
        pin_dia = 0.65
        pin_ground_dia = 1.0
        
    pin = color(Brass) (cylinder(d = pin_dia, h = pin_height, center = True, segments = segments_count))
    pin_ground = color(Brass) (cylinder(d = pin_ground_dia, h = pin_height, center = True, segments = segments_count))

    pin_ground_offset_y = -0.2
    
    # data pins
    p = translate([-pin_pitch / 2.0 - pin_pitch, 0, 0]) (pin) + \
         translate([-pin_pitch / 2.0, 0, 0]) (pin) + \
         translate([pin_pitch / 2.0, 0, 0]) (pin) + \
         translate([pin_pitch / 2.0 + pin_pitch, 0, 0]) (pin)

    # ground pins
    p += translate([-pin_ground_pitch / 2.0, pin_ground_offset_y, 0]) (pin_ground) + \
         translate([pin_ground_pitch / 2.0, pin_ground_offset_y, 0]) (pin_ground)
    
    return p

@bom_part("Magnet Connector (HTP-CON-M411P-F)", 4.64)
def magnet_connector():

    back_x = 15.0
    back_y = 3.1
    back_z = magnet_connector_height_from_pcb
    back_r = 2.14 # estimate

    mid1_x = 15.0
    mid1_y = 4.31 - 3.1

    mid2_x = 14.2
    mid2_y = 5.81 - 4.31
    mid2_r = 2.57 # estimate
    
    mid_z = 4.7

    front_y = 6.66 - 5.81
    front_z = 2.57
    front_x = 10.714 # estimate

    pin_pogo_dia = 1.45
    pin_pogo_height = 0.01
    
    back = color(BlackPaint) (hull() (
        translate([0, 0, -back_z / 2.0 + (back_z - mid_z / 2.0) / 2.0]) (cube([back_x, back_y, back_z - mid_z / 2.0], center = True)),
        translate([back_x / 2.0 - mid_z / 4.0, 0, back_z / 2.0 - mid_z / 4.0]) (rotate(90, [1, 0, 0]) (cylinder(d = mid_z / 2.0, h = back_y, center = True, segments = segments_count))),
        translate([-back_x / 2.0 + mid_z / 4.0, 0, back_z / 2.0 - mid_z / 4.0]) (rotate(90, [1, 0, 0]) (cylinder(d = mid_z / 2.0, h = back_y, center = True, segments = segments_count)))
        ))
    
    mid1 = color(BlackPaint) (hull() (
        translate([0, 0, -mid_z / 4.0]) (cube([mid1_x, mid1_y, mid_z / 2.0], center = True)),
        translate([mid1_x / 2.0 - mid_z / 4.0, 0, mid_z / 4.0]) (rotate(90, [1, 0, 0]) (cylinder(d = mid_z / 2.0, h = mid1_y, center = True, segments = segments_count))),
        translate([-mid1_x / 2.0 + mid_z / 4.0, 0, mid_z / 4.0]) (rotate(90, [1, 0, 0]) (cylinder(d = mid_z / 2.0, h = mid1_y, center = True, segments = segments_count))),
        ))
    
    mid2 = color(Aluminum) (hull() (
        translate([mid2_x / 2.0 - mid_z / 2.0, 0, 0]) (rotate(90, [1, 0, 0]) (cylinder(d = mid_z, h = mid2_y, center = True, segments = segments_count))),
        translate([-mid2_x / 2.0 + mid_z / 2.0, 0, 0]) (rotate(90, [1, 0, 0]) (cylinder(d = mid_z, h = mid2_y, center = True, segments = segments_count)))
        ))
    
    front = color(BlackPaint) (hull() (
        translate([front_x / 2.0 - front_z / 2.0, 0, 0]) (rotate(90, [1, 0, 0]) (cylinder(d = front_z, h = front_y, center = True, segments = segments_count))),
        translate([-front_x / 2.0 + front_z / 2.0, 0, 0]) (rotate(90, [1, 0, 0]) (cylinder(d = front_z, h = front_y, center = True, segments = segments_count)))
        ))

    pin_pitch = 2.2
    pin_height = 1.15 + magnet_connector_pins_extra_height
    pin_offset_y = -back_y / 2.0 + 2.1
    pin_pogo = color(Brass) (cylinder(d = pin_pogo_dia, h = pin_pogo_height, center = True, segments = segments_count))
    
    back += translate([0, -pin_offset_y, -pin_height / 2.0 - back_z / 2.0]) (magnet_connector_pins_holes())

    front += translate([-pin_pitch / 2.0 - pin_pitch, front_y / 2.0, 0]) (rotate(90, [1, 0, 0]) (pin_pogo)) + \
             translate([-pin_pitch / 2.0, front_y / 2.0, 0]) (rotate(90, [1, 0, 0]) (pin_pogo)) + \
             translate([pin_pitch / 2.0, front_y / 2.0, 0]) (rotate(90, [1, 0, 0]) (pin_pogo)) + \
             translate([pin_pitch / 2.0 + pin_pitch, front_y / 2.0, 0]) (rotate(90, [1, 0, 0]) (pin_pogo))
    
    p = union() (
        translate([0, pin_offset_y, (mid_z - back_z) / 2.0]) (back),
        translate([0, mid1_y / 2.0 - (back_y / 2.0 - pin_offset_y) + back_y, 0]) (mid1),
        translate([0, mid2_y / 2.0 - (back_y / 2.0 - pin_offset_y) + back_y + mid1_y, 0]) (mid2),
        translate([0, front_y / 2.0 - (back_y / 2.0 - pin_offset_y) + back_y + mid1_y + mid2_y, 0]) (front)
        )

    p = translate([0, 0, back_z - mid_z / 2.0]) (p)
    
    return p

#@bom_part("USB-C (USB4110-GF-A)", 1.42)
#def usb():
#    return translate([0, 0, usb_height / 2.0]) (rotate(90, [1, 0, 0]) (color(Aluminum) (import_stl("cots/USB4110-GF-A--3DModel-STEP-56544.stl"))))

@bom_part("Rubber Buttons", 0.5)
def rubber_buttons():

    d = 0
    if button_enable:
        d += button_knob_travel
    
    b1_angle = 0
    b2_angle = -switch_spacing
    b3_angle = switch_spacing
    
    # cylinder buttons
    button = translate([-rubber_button_length / 2.0 - rubber_button_support_thickness / 4.0, 0, 0]) (rotate(90, [0, 1, 0]) (cylinder(d = rubber_button_dia, h = rubber_button_length, center = True, segments = segments_count)))
    p = translate([(bl + d) * cos(math.radians(b1_angle)), (bl + d) * sin(math.radians(b1_angle)), 0]) (rotate(b1_angle, [0, 0, 1]) (button)) + \
        translate([(bl + d) * cos(math.radians(b2_angle)), (bl + d) * sin(math.radians(b2_angle)), 0]) (rotate(b2_angle, [0, 0, 1]) (button)) + \
        translate([(bl + d) * cos(math.radians(b3_angle)), (bl + d) * sin(math.radians(b3_angle)), 0]) (rotate(b3_angle, [0, 0, 1]) (button))
    
    # backplane
    o = cylinder(d = enclosure_id - d, h = rubber_button_support_height, segments = segments_count, center = True)
    i = cylinder(d = enclosure_id - d - rubber_button_support_thickness, h = rubber_button_support_height + 2.0, segments = segments_count, center = True)
    aoi1 = o - i
    aoi = cube([rubber_button_support_length, rubber_button_support_length, rubber_button_support_height], center = True)
    aoi2 = translate([bl * cos(math.radians(b1_angle)), bl * sin(math.radians(b1_angle)), 0]) (rotate(180 + b1_angle, [0, 0, 1]) (aoi))
    p += intersection() (aoi1, aoi2)
    
    return color(BlackPaint) (p)

@bom_part("Custom Enclosure Top Lens", 0.5)
def enclosure_top_lens():
    p = intersection() (enclosure_top_curve(), enclosure_top_lens_aoi())

    # mounting support (rough)
    o = sphere(d = enclosure_top_d - enclosure_wall_thickness * 2.0, segments = segments_count)
    i = sphere(d = enclosure_top_d - enclosure_wall_thickness * 4.0, segments = segments_count)
    p += translate([0, 0, -enclosure_top_r + enclosure_top_h]) (o - i)
    cut = cube([enclosure_top_d + 2, enclosure_top_d + 2, enclosure_top_d - enclosure_top_h + 1], center = True) # cut bottom
    p -= translate([0, 0, -(enclosure_top_d - enclosure_top_h + 1) / 2.0]) (cut)    
    p -= cylinder(d = enclosure_lens_id, h = enclosure_top_h * 2.0, center = True, segments = segments_count) # cut speaker hole
    c = cube([enclosure_od / 2.0, enclosure_od, enclosure_top_h + 6.0], center = True) # cut in half
    p -= rotate(enclosure_lens_angle, [0, 0, 1]) (translate([0, 0, enclosure_top_h / 2.0 - 1]) (translate([enclosure_od / 4.0, 0, 0]) (c)))
    
    p = translate([0, 0, pcb_thickness + magnet_connector_height_from_pcb + sla_cots_clearance]) (p)

    # colors - https://www.oliversbabycare.co.uk/wp-content/uploads/2019/02/Meemoo-Meelight-Portable-Nightlight-7.png
    # eec181, fedca7, ffeccc
    return color([0.93, 0.757, 0.506, 0.9]) (p)

# KHL

def usb():
    return translate([0, 0, usb_height / 2.0]) (rotate(90, [1, 0, 0]) (color(Aluminum) (import_stl("cots/USB4110-GF-A--3DModel-STEP-56544.stl"))))

def led():
    return translate([-led_length / 2.0, led_width / 2.0, 0.0254]) (rotate(90, [1, 0, 0]) (color(Aluminum) (import_stl("cots/LSM0603XXXV.stl"))))

def button():
    return translate([0, button_length / 2.0 + (button_length_all - button_length), 0]) (rotate(90, [1, 0, 0]) (color(Aluminum) (import_stl("cots/EVQP7-JA-01P.stl"))))

def battery():
    return color(Aluminum) (cube_curved_edges(battery_width, battery_length, battery_thickness, battery_corner_radius, segments_count, True))

# WHA

@bom_part("Generic ID Card", 0.0)
def card():
    p = cube([card_width, card_length, card_thickness], center = True)
    return color(Blue) (p)

@bom_part("ePaper (ER-EPD0154-2R)", 4.67)
def lcd():
    pcb = color(colour_pcb) (cube([lcd_width, lcd_length, lcd_thickness], center = True))

    cut_window = cube([lcd_window_width, lcd_window_length, lcd_thickness + 2], center = True)
    window = color([0.5, 0.5, 0.5, 0.5]) (cube([lcd_window_width, lcd_window_length, lcd_thickness], center = True))

    p = pcb - \
        translate([0, lcd_window_length / 2.0 + lcd_length / 2.0 - lcd_window_length - lcd_window_offset_y, 0]) (cut_window) + \
        translate([0, lcd_window_length / 2.0 + lcd_length / 2.0 - lcd_window_length - lcd_window_offset_y, 0]) (window)
    
    return p

@bom_part("3.7V 240mAh 1S 20C LiPo (Z240S20C)", 4.79, currency="AU$")
def battery():
    p = cube([battery_width, battery_length, battery_thickness], center = True)
    return color(Aluminum) (p)

@bom_part("Coin Vibration 10000rpm 3V (316040004)", 1.22)
def vibrator():    
    return color(Steel) (translate([0, 0, vibrator_thickness / 2.0]) (cylinder(d = vibrator_dia, h = vibrator_thickness, center = True, segments = segments_count) + \
                        translate([vibrator_dia / 2.0 + vibrator_connector_length / 2.0 - 1, 0, 0]) (cube([vibrator_connector_length + 2, vibrator_connector_width, 2.7], center = True))))

@bom_part("Switch Tactile SPST-NO (EVQ-P7A01P)", 0.31)
def button():
    return color(Aluminum) (translate([0, button_length / 2.0 + (button_length_all - button_length), 0]) (rotate(90, [1, 0, 0]) (import_stl("cots/EVQP7-JA-01P.stl"))))

def usb():
    return translate([0, 0, usb_height / 2.0]) (rotate(90, [1, 0, 0]) (color(Aluminum) (import_stl("cots/USB4110-GF-A--3DModel-STEP-56544.stl"))))

def button_outline():
    return translate([0, button_length / 2.0 + (button_length_all - button_length), 0]) (cube([button_width, button_length, pcb_thickness + 2], center = True
))

def lcd_connector_outline():
    return cube([lcd_connector_width, lcd_connector_length, pcb_thickness + 2], center = True)

