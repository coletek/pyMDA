import argparse
from solid import *
from solid.utils import *

from core import *
from geometry import *
from curved import *
from bezier_curve import *
from plates import *

from stock_materials import *
from stock_magnets import *
from stock_motors import *
from stock_bearings import *
from stock_fixtures import *
from stock_electronics import *

from collar import *
from cam_profile import *
from scotch_yoke import *

from enclosures import *

from holes import *

#
# NOTES:
#
# * At this stage, just demo each of the shapes, features, helpers
# of this repositories. Shapes/features/helpers are likely to
# envolve/merge moving forward with this OO approach - allowing
# easier management of the wide range of features
#
# * cube_curved_sides, cube_curved_edges and perhaps bar_curved_edges could be merged
#
# * Scotch Yotch is perhaps the better example of how to manage static vs dynamic params
#
# * Each compnonent has a bounding box width, length, heights, and orign - for features like stacking in 3D space
#
# * stock_motors could perhaps be more advanced OO of motor models for example
#

def build_geometry(config):
    assembly = Assembly()
    assembly.add('cube', Cube(10, 10, 10), position=([1, 2, 3]))
    assembly.add('cylinder', Cylinder(20, 20))
    assembly.add('sphere', Sphere(30))
    assembly.add('pyramid', Pyramid(30, 30))
    assembly.add('cone', Cone(40, 40))
    assembly.add('tetrahedron', Tetrahedron(50), position=(0, 0, 0))
    assembly.add('torus', Torus(60, 30, 100, 100))
    assembly.add('triangular_prism', TriangularPrism(70, 70, 70), position=(0, 0, 0))
    assembly.add('hexagonal_prism', HexagonalPrism(80, 80))
    assembly.stack_y(10)
    return assembly


def build_curved(config):
    assembly = Assembly()
    assembly.add('cube_curved_sides', CubeCurvedSides(20, 20, 20, 5, 4))
    #assembly.add('cube_curved_edges', CubeCurvedEdges(20, 20, 20, 5))
    assembly.add('bar_curved_edges', BarCurvedEdges(40, 10, 2))
    assembly.add('cylinder_curved_edges', CylinderCurvedEdges(20, 50, 10))
    assembly.stack_y(10)
    return assembly

def build_pts(config):
    assembly = Assembly()

    # Point Based Shapes
    assembly.add('line_round_via_hull', LineRoundViaHull((0, 0, 0), (10, 10, 10), 5))
    #assembly.add('polyline_round', PolylineRound([(0, 0, 0), (10, 10, 10), (0, 0, 10)], 2))

    # Bezier Curve (also a point based shape)
    p0 = (0, 0, 0)
    p1 = (0, 0, 100)
    p2 = (0, 100, 0)
    p3 = (100, 100, 100)
    pts = BezierCurve(0.05, p0, p1, p2, p3).create()
    for i in pts:
        print (i)
    assembly.add('bezier_curve', PolylineRound(pts, 5))

    assembly.stack_y(50)

    return assembly

def build_plates(config):

    assembly = Assembly()
    
    config['plate_with_mounting_holes'] = {
        'width': 25.0,
        'length': 23.862,
        'thickness': 1.12,
        'mounting_hole_dia': 2.2,
        'mounting_hole_pitch_width': 25.0 - 2.0 - 2.0,
        'mounting_hole_pitch_length': 14.5 - 2.0,
        'mounting_hole_offset_width': 0.0,
        'mounting_hole_offset_length': 23.862 / 2.0 - (14.5 - 2.0) / 2.0 - 2.0
    }
    assembly.add('plate_with_mounting_holes', PlateWithMountingHoles(config['plate_with_mounting_holes']))

    config['plate_with_mounting_holes_edges'] = {
        'width': 100,
        'height': 100,
        'thickness': 5,
        'mounting_hole_size': 3.0,
        'top_mounting_hole_depth': 10.0,
        'bottom_mounting_hole_depth': 10.0
    }
    assembly.add('plate_with_mounting_holes_edges', PlateWithMountingHolesEdges(config['plate_with_mounting_holes_edges']))
    config['plate_with_fillets'] = {
        'width': 100,
        'length': 100,
        'thickness': 5,
        'fillet_radius': 5.0
    }
    assembly.add('plate_with_fillets', PlateWithFillets(config['plate_with_fillets']))

    assembly.stack_y(150)
    
    return assembly

def build_holes(config):

    assembly = Assembly()

    config['slot'] = {
        'width': 5,
        'length': 100,
        'height': 10
    }
    assembly.add('slot', Slot(config['slot']))

    config['slot_curve'] = {
        'width': 6.0 + 0.1,
        'height': 10.0,
        'radius': 200.0,
        'start_angle': math.radians(15),
        'end_angle': math.radians(125),
        'step': 0.1
    }
    assembly.add('slot_curve', SlotCurve(config['slot_curve']))

    config['slot_array'] = {
        'length': 100,
        'slot_width': 100,
        'slot_length': 3.0,
        'slot_count': 10,
        'height': 360
    }
    #assembly.add('slot_array', SlotArray(config['slot_array']))

    config['speaker_grill'] = {
        'dia': 50,
        'pitch': 5,
        'hole_dia': 3,
        'wall_thickness': 2
    }
    assembly.add('speaker_grill', SpeakerGrill(config['speaker_grill']))

    assembly.stack_y(100)
    
    return assembly

def build_features(config):
    
    assembly = Assembly()

    # Scotch Yotch
    config['scotch_yotch'] = {
        "stroke_length": 40.0,
        "pulley_thickness": 3.0,
        "pin_dia": 3.0,
        "pin_length": 10.0,
        "slider_x_length": 35.0,
        "slider_x_width": 3.0 + 2.0,
        "slider_x_thickness": 5.0,
        "slider_y_length": 40.0 / 2.0 + 2.0,
        "slider_y_width": 3.0 + 2.0,
        "slider_y_thickness": 5.0
    }
    config['scotch_yotch']["slider_x_width"] = config['scotch_yotch']["pin_dia"] + 2.0
    config['scotch_yotch']["slider_y_length"] = config['scotch_yotch']["stroke_length"] / 2.0 + 2.0
    config['scotch_yotch']["slider_y_width"] = config['scotch_yotch']["pin_dia"] + 2.0
    config['scotch_yotch']["slider_y_thickness"] = config['scotch_yotch']["slider_x_thickness"]
    angle = math.pi / 180.0 * 90.0
    assembly.add('scotch_yoke', ScotchYoke(config['scotch_yotch'], angle))

    # Collar - based on Trimble GPS mount collar
    config['collar'] = {
        "id": 76, # 76 uncompressed
        "thickness": 8,
        "width": 25,
        "connection_gap": 8,
        "connection_hole_dia": 8.5, # m10_tap_hole_size
        "connection_thickness": 11.5,
        "connection_height": 0.0 # fixed distance between connection and collar - zero here I think
    }
    assembly.add('collar', Collar(config['collar'], 0.0))

    config['cam_profile'] = {
        "height": 20,
        "start_radius": 10.0 / 2.0,
        "start_angle": math.radians(180.0),
        "end_radius": 10.0 / 2.0 + config['collar']['connection_gap'],
        "end_angle": math.radians(360.0),
        "increment": 0.01,
        "is_center": True
    }
    assembly.add('cam_profile', CamProfile(config["cam_profile"]))

    assembly.stack_y(100)
    
    return assembly

def build_enclosures(config):
    
    assembly = Assembly()

    config['boss'] = {
        'dia': 10,
        'hole_dia': 5,
        'thickness': 10
    }
    assembly.add('boss', Boss(config['boss']))

    config['boss_plate'] = {
        'width': 100,
        'length': 100,
        'thickness': 10,
        'mounting_hole_dia': 4,
        'dia': 10,
        'hole_dia': 5,
        'height': 50,
    }
    assembly.add('boss_plate', BossPlate(config['boss_plate']))

    config['boss_plate_dual'] = {
        'width': 100,
        'length': 100,
        'thickness': 10,
        'mounting_hole_dia': 4,
        'dia': 10,
        'hole_dia': 5,
        'height': 50,
        'pitch': 30
    }
    assembly.add('boss_plate_dual', BossPlateDual(config['boss_plate_dual']))

    config['rubber_button'] = {
        'radius': 4.0, 
        'length': 15,
        'support_radius': 8,
        'support_length': 5
    }
    assembly.add('rubber_button', RubberButton(config['rubber_button']))

    config['lightpipe_straight'] = {
        'radius': 5,
        'length': 30,
        'support_radius': 8,
        'support_length': 5,
        'support_offset': 2,
        'head_radius': 10
    }
    assembly.add('lightpipe_straight', LightpipeStraight(config['lightpipe_straight']))

    assembly.stack_y(100)
    
    return assembly
    
def build_stock_materials(config):
    
    assembly = Assembly()

    assembly.add('square_hollow_section', SHS(30, 3, 30))
    assembly.add('channel_section', CS(30, 3, 30))
    assembly.add('l_section', LS(30, 30, 3, 30))
    assembly.add('solid_section', SB(30, 30))
    assembly.add('rod', Rod(10, 30))
    assembly.add('sheet', Sheet(30, 30, 3))
    #assembly.add('wedge', Wedge(10, 10, 2, 2))
    #assembly.add('hinge', Hinge(3, 10, 20, 100, 100, 1, True, 100))

    assembly.stack_y(10)
    
    return assembly

def build_stock_magnets(config):
    assembly = Assembly()
    assembly.add('coin_magnet', MagnetCoin(20, 1.0))
    assembly.stack_y(10)
    return assembly

def build_stock_motors(config):    

    assembly = Assembly()

    # https://www.omc-stepperonline.com/brushed-12v-dc-gear-motor-3kg-cm-3rpm-w-828-1-worm-gearbox-wga-2430123100-g828
    config['motor_dc'] = {
        'dia':  24.4,
        'length':  30.8,
        'shaft_dia':  6.0, # FYI
        'shaft_length':  7.0, # FYI
        'shaft_key_cut':  6.0 - 4.0, # FYI
        'shaft_key_length':  6.2 # FYI
    }
    config['gearbox_worm'] = {
        'width': 32.0,
        'length': 46.0,
        'height': 25.0,
        'width_pitch': 18.0,
        'length_pitch': 33.0,
        'length_pitch_pos': 6.0,
        'shaft_pos': 9 + 6,
        'shaft_dia': 6.0,
        'shaft_length': 7.0,
        'shaft_key_cut': 6.0 - 4.0,
        'shaft_key_length': 6.2
    }
    assembly.add('motor_dc', MotorDC(config['motor_dc']))
    assembly.add('gearbox_worm', GearboxWorm(config['gearbox_worm']))
    #assembly.add('dc_motor_and_gearbox_worm', MotorDCwGearboxWorm(config['motor_dc'], config['gearbox_worm']))

    config['servo_rds3225'] = {
        'width': 20.0,
        'length': 40.0,
        'height': 40.5,
        'axle_pos': 11.0,
        'axle_mount_height': 1.5,
        'axle_gearhead_height': 4.0,
        'axle_wheel_gap': 2.8,
        'bracket_width': 20.0,
        'bracket_length': 57.0,
        'bracket_thickness': 2.0,
        'bracket_screw_head_height': 1.6,
        'cable_mount_height': 6.0
    }
    assembly.add('servo_rds3225', ServoRDS3225(config['servo_rds3225'], 0.0, True))

    assembly.add('stepper_driver', StepperDriver())
    assembly.add('stepper', Stepper())
    assembly.add('pulley', Pulley(0.0))
    #assembly.add('stepper_and_pulley', StepperAndPulley(0.0))

    inch_to_mm = 25.4
    config['linear_actuator_pa14p'] = {
        'size': 2.0 * inch_to_mm,
        'dist_to_mount': 0.78 * inch_to_mm,
        'dist_to_mount2': 0.4 * inch_to_mm,
        'width': 1.57 * inch_to_mm
    }
    assembly.add('LinearActuatorPA14P', LinearActuatorPA14P(config['linear_actuator_pa14p'], 0.0 * inch_to_mm))
    
    config['linear_actuator_mounting_bracket_brk14'] = {
        'width': 1.04 * inch_to_mm,
        'length': 2.3 * inch_to_mm,
        'length_to_axle': 0.32 * inch_to_mm,
        'height_to_axle': 1.43 * inch_to_mm
    }
    #assembly.add('linear_actuator_mounting_bracket_brk14', LinearActuatorMountingBracketBRK14(config['linear_actuator_mounting_bracket_brk14']))

    config['linear_actuator_mounting_bracket_brk03'] = { 'length': 55.88 }
    #assembly.add('linear_actuator_mounting_bracket_brk03', LinearActuatorMountingBracketBRK03(config['linear_actuator_mounting_bracket_brk03']))

    config['actuator_small'] = { 'dist_to_mount': 4.85 }
    #assembly.add('linear_actuator_pa12t', LinearActuatorPA12T(config['actuator_small']))

    config['linear_actuator_and_bracket'] = {
        "stroke": 0.0 * inch_to_mm,
        "angle": 0.0,
        "explode_dist": 0.0
    }
    #assembly.add('linear_actuator_and_bracket', LinearActuatorAndBracket(config['linear_actuator_pa14p'], config['linear_actuator_mounting_bracket_brk14'], config['linear_actuator_and_bracket']))

    assembly.stack_y(100)
        
    return assembly

def build_stock_bearings(config):
    
    assembly = Assembly()

    assembly.add('bearing', Bearing(10, 20, 5))
    assembly.add('bearing_pillow_block_ucp201', BearingPillowBlockUCP201())
    assembly.add('bearing_pillow_block_ucp204', BearingPillowBlockUCP204())
    #assembly.add('bearing_2_bolt_flange_ucfl204', Bearing2BoltFlangeUCFL204())

    assembly.stack_y(150)

    return assembly

def build_stock_fixtures(config):
    
    assembly = Assembly()

    assembly.add('fixture_counter_sunk', FixtureCounterSunk(2, 4, 5, 1))
    assembly.add('fixture_socket', FixtureSocket(2, 4, 5, 2))
    assembly.add('washer', Washer(20, 10, 3))

    assembly.stack_y(20)
    
    return assembly

def build_stock_electronics(config):
    
    assembly = Assembly()
    
    config['pcb_header'] = {}
    assembly.add('pcb_header', PCBHeader(config['pcb_header'], 2.54, 10))
    config['pcb_header_dual'] = {}
    assembly.add('pcb_header_dual', PCBHeaderDual(config['pcb_header_dual'], 2.54, 10))

    config['pot_side'] = {
        'wall_thickness': 1.0,
        'dia': 6.81,
        'length': 4.5,
        'height': 8.4,
        'pin_width': 0.8,
        'pin_length': 0.8 / 2.0, # pin_width / 2.0
        'pin_height': 3.0,
        'pin_pitch_x': 5.0,
        'pin_pitch_y': 2.5
    }
    assembly.add('pot_side', POTSide(config['pot_side']))

    config['fuse_mini'] = {
        'width': 3.8,
        'length': 10.9,
        'height': 8.8,
        'pin_width': 0.8,
        'pin_length': 2.8,
        'pin_height': 7.5
    }
    assembly.add('fuse_mini', FuseMini(config['fuse_mini']))

    config['fuse_holder_mini'] = {
        'width': 6.73,
        'length': 16.0,
        'height': 7.37,
        'pitch_x': 3.41,
        'pitch_y': 9.9
    }
    assembly.add('fuse_holder_mini', FuseHolderMini(config['fuse_holder_mini']))

    #assembly.add('fuse_mini_and_holder', FuseMiniAndHolder(config['fuse_mini'], config['fuse_holder_mini']))

    config['rpi'] = {
        'width': 56.0,
        'length': 85.0,
        'width_offset': -1.57,
        'length_offset': -2.76,
        'mounting_holes_width_pitch': 49.0, # FYI
        'mounting_holes_length_pitch': 58.0, # FYI
        'mounting_holes_offset': 3.5 # FYI
    }
    assembly.add('rpi', RPI(config['rpi']))

    config['rpi_display'] = {
        'width': 110.8,
        'length': 193.0,
        'width_offset': 51.3,
        'length_offset': 69.5,
        'mounting_holes_width_pitch': 66.0, # FYI
        'mounting_holes_length_pitch': 126.0, # FYI
        'mounting_holes_offset': 33.5 # FYI
    }
    assembly.add('rpi_display', RPIDisplay(config['rpi_display']))

    config['nvidia_jetson_nano'] = {
        'width': 79.0,
        'length': 100.0,
        'mounting_holes_width_pitch': 58.0, # FYI
        'mounting_holes_length_pitch': 86.0, # FYI
        'mounting_holes_offset': 4.0 # FYI
    }
    assembly.add('nvidia_jetson_nano', NVidiaJetsonNano(config['nvidia_jetson_nano']))

    # ttps://www.raspberrypi.com/documentation/accessories/camera.html
    config['pcb_camera'] = {
        'lens_dia': 10.8,
        'lens_height':8.3,
        'lens_offset_width': 0.0,
        'lens_offset_length': 0.0, # or is this height which is 14.4 - 14.5
        
        'sensor_width': 6.45,
        'sensor_height': 3.63,
        'sensor_thickness': 1.0,
        'focal_length': 2.75
    }
    assembly.add('pcb_camera', PCBCamera(config['plate_with_mounting_holes'], config['pcb_camera'], 10.0, False))

    assembly.stack_y(150)
    
    return assembly

def build(config):
    
    # demo stacking/aligning with margin/pitch
    #ass_geo.stack_x(5)
    #ass_geo.stack_y(100)
    #ass_geo.stack_z(5)

    demo_geometry = build_geometry(config)
    demo_curved = build_curved(config)
    demo_pts = build_pts(config)
    demo_plates = build_plates(config)
    demo_holes = build_holes(config)
    demo_features = build_features(config)
    demo_enclosures = build_enclosures(config)
    demo_stock_materials = build_stock_materials(config)
    demo_stock_magnets = build_stock_magnets(config)
    demo_stock_motors = build_stock_motors(config)
    demo_stock_bearings = build_stock_bearings(config)
    demo_stock_fixtures = build_stock_fixtures(config)
    demo_stock_electronics = build_stock_electronics(config)

    demo_geometry.export_scad("demo_geometry.scad")
    demo_curved.export_scad("demo_curved.scad")
    demo_pts.export_scad("demo_pts.scad")
    demo_plates.export_scad("demo_plates.scad")
    demo_holes.export_scad("demo_holes.scad")
    demo_features.export_scad("demo_features.scad")
    demo_enclosures.export_scad("demo_enclosures.scad")
    demo_stock_materials.export_scad("demo_stock_materials.scad")
    demo_stock_magnets.export_scad("demo_stock_magnets.scad")
    demo_stock_motors.export_scad("demo_stock_motors.scad")
    demo_stock_bearings.export_scad("demo_stock_bearings.scad")
    demo_stock_fixtures.export_scad("demo_stock_fixtures.scad")
    demo_stock_electronics.export_scad("demo_stock_electronics.scad")
    
    # demo adding component to 
    assembly = Assembly()
    assembly.add('demo_geo', demo_geometry)
    assembly.add('demo_curved', demo_curved)
    assembly.add('demo_pts', demo_pts)
    assembly.add('demo_plates', demo_plates)
    assembly.add('demo_holes', demo_holes)
    assembly.add('demo_features', demo_features)
    assembly.add('demo_enclosures', demo_enclosures)
    assembly.add('demo_stock_materials', demo_stock_materials)
    assembly.add('demo_stock_magnets', demo_stock_magnets)
    assembly.add('demo_stock_motors', demo_stock_motors)
    assembly.add('demo_stock_bearings', demo_stock_bearings)
    assembly.add('demo_stock_fixtures', demo_stock_fixtures)
    assembly.add('demo_stock_electronics', demo_stock_electronics)

    assembly.stack_x(100)
        
    # example of smarter methods to join components - WIP
    #demo_geo.join_to_surface('cube', 'cylinder', align='bottom', face_align='top')
    #demo_geo.join_to_surface('hexagon', 'trianglular_prism', align='front', face_align='back')
    #demo_geo.join_to_surface('hexagon', 'trianglular_prism', align='left', face_align='left')
    #demo_geo.join_to_surface('hexagon', 'trianglular_prism', align='bottom', face_align='bottom')

    #assembly.join_to_surface('assembly1', 'assembly2', align='top', face_align='bottom')

    return assembly

def main():
    parser = argparse.ArgumentParser(description="Controls for 3D printer component assemblies")
    parser.add_argument('--test', action='store_true', help='Run tests on the assembly')
    parser.add_argument('--export', type=str, help='Export assembly to SCAD file', metavar='FILENAME')
    parser.add_argument('--cross-section', nargs=2, metavar=('AXIS', 'POSITION'), help='Generate a cross-sectional view of the assembly')

    args = parser.parse_args()

    config = {}

    assembly = build(config)

    if args.test:
        assembly.test_assembly()

    if args.export:
        assembly.export_scad(args.export)

    if args.cross_section:
        axis, position = args.cross_section
        cross_section = assembly.cross_section_view(axis, float(position))
        scad_render_to_file(cross_section, f'{args.export}_cross_section.scad')
        print(f"Cross-sectional view exported as {args.export}_cross_section.scad")

if __name__ == "__main__":
    main()

