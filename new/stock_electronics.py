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
        self.fuse_mini_config = fuse_mini_config
        self.fuse_holder_mini_config = fuse_holder_mini_config
        self.mini_fuse_holder_and_fuse_height = mini_fuse_holder_and_fuse_height
            
    def create(self):
        p = FuseHolderMini(self.fuse_holder_mini_config).create()
        p += translate([0, 0, -self.fuse_mini_config['height'] + mini_fuse_holder_and_fuse_height]) (FuseMini(self.fuse_mini_config).create())
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

    def __init__(self, config, fov_dist, enable_fov):
        self.config = config
        self.fov_dist = fov_dist
        self.enable_fov = enable_fov

    def create(self):
            
        b = PlateWithMountingHoles(self.config['pcb_width'], self.config['pcb_length'], self.config['pcb_thickness'],
                                   self.config['pcb_mounting_hole_dia'], self.config['pcb_mounting_pitch_width'], self.config['pcb_mounting_pitch_length'],
                                   self.config['pcb_mounting_hole_offset_width'], self.config['pcb_mounting_hole_offset_length']).create()
        b = color(colour_pcb)
        
        b = translate([self.config['lens_offset_width'], self.config['lens_offset_length'], 0]) (b)
        
        lens = color(BlackPaint) (cylinder(d = self.config['lens_dia'], h = self.config['lens_height'], center = True, segments = self.segments_count))
        
        p = translate([0, 0, self.config['pcb_thickness'] / 2.0]) (b) + \
            translate([0, 0, self.config['lens_height'] / 2.0 + self.config['pcb_thickness']]) (lens)
        
        if enable_fov:
            
            fov_width = 2.0 * math.atan2(self.config['sensor_width'], 2 * self.config['focal_length'])
            fov_height = 2.0 * math.atan2(self.config['sensor_height'], 2 * self.config['focal_length'])
            print ("H-FOV %f" % math.degrees(fov_width))
            print ("V-FOV %f" % math.degrees(fov_height))
            
            fov_start = cube([self.config['sensor_width'], self.config['sensor_height'], 0.1], center = True)
            fov_end = cube([fov_dist * math.tan(fov_width / 2.0) * 2.0, fov_dist * math.tan(fov_height / 2.0) * 2.0, 0.1], center = True)
            fov = color([0.5, 0.5, 0.5, 0.5]) (hull() (fov_start, translate([0, 0, fov_dist]) (fov_end)))
            p += translate([0, 0, 0.1 / 2.0 + self.config['pcb_thickness'] + self.config['sensor_thickness'] + self.config['focal_length']]) (fov)
    
        return p
        
