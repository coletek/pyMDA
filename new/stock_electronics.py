import math
from solid import *
from solid.utils import *
from core import *
from utilties import *

class PCBHeader(Component):
    ''' https://app.adam-tech.com/products/download/data_sheet/201605/ph1-xx-ua-data-sheet.pdf '''

    def __init__(self, config, pitch = 2.54, number_of_pins = 2):
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
