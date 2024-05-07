import argparse
from solid import *
from solid.utils import *

from core import *
from geometry import *
from curved import *
from stock_materials import *
from bezier_curve import *
from stock_magnets import *
from stock_motors import *
from scotch_yoke import *

def build(config):

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
    # * TBC: Stock Bearings, Stock Electronics, Stock Fixtures, Utilites, Cam Profile, Collar, Enclosures, Holes
    #   and plates (perhaps perhaps should move to stock_materials?)
    #
    
    # Geometry - Fundamental Shapes
    subassembly = Assembly()
    subassembly.add('cube', Cube(10, 10, 10), position=([1, 2, 3]))
    subassembly.add('cylinder', Cylinder(20, 20))
    subassembly.add('sphere', Sphere(30))
    subassembly.add('pyramid', Pyramid(30, 30))
    subassembly.add('cone', Cone(40, 40))
    subassembly.add('tetrahedron', Tetrahedron(50), position=(0, 0, 0))
    subassembly.add('torus', Torus(60, 30, 100, 100))
    subassembly.add('triangular_prism', TriangularPrism(70, 70, 70), position=(0, 0, 0))
    subassembly.add('hexagonal_prism', HexagonalPrism(80, 80))

    # Curved Edges Shapes
    subassembly.add('cube_curved_sides', CubeCurvedSides(20, 20, 20, 5, 4))
    #subassembly.add('cube_curved_edges', CubeCurvedEdges(20, 20, 20, 5))
    subassembly.add('bar_curved_edges', BarCurvedEdges(40, 10, 2))
    subassembly.add('cylinder_curved_edges', CylinderCurvedEdges(20, 50, 10))

    # Point Based Shapes
    subassembly.add('line_round_via_hull', LineRoundViaHull((0, 0, 0), (10, 10, 10), 5))
    #subassembly.add('polyline_round', PolylineRound([(0, 0, 0), (10, 10, 10), (0, 0, 10)], 2))

    # Bezier Curve (also a point based shape)
    p0 = (0, 0, 0)
    p1 = (0, 0, 100)
    p2 = (0, 100, 0)
    p3 = (100, 100, 100)
    pts = BezierCurve(0.05, p0, p1, p2, p3).create()
    for i in pts:
        print (i)
    subassembly.add('bezier_curve', PolylineRound(pts, 5))
    
    # Stock Materials
    subassembly.add('square_hollow_section', SHS(30, 3, 30))
    subassembly.add('channel_section', CS(30, 3, 30))
    subassembly.add('l_section', LS(30, 30, 3, 30))
    subassembly.add('solid_section', SB(30, 30))
    subassembly.add('rod', Rod(10, 30))
    subassembly.add('sheet', Sheet(30, 30, 3))
    #subassembly.add('wedge', Wedge(10, 10, 2, 2))
    #subassembly.add('hinge', Hinge(3, 10, 20, 100, 100, 1, True, 100))

    # Stock Motors
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
    subassembly.add('motor_dc', MotorDC(config['motor_dc']))
    subassembly.add('gearbox_worm', GearboxWorm(config['gearbox_worm']))
    subassembly.add('dc_motor_and_gearbox_worm', MotorDCwGearboxWorm(config['motor_dc'], config['gearbox_worm']))

    subassembly = Assembly()
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
    subassembly.add('servo_rds3225', ServoRDS3225(config['servo_rds3225'], 0.0, True))

    subassembly.add('stepper_driver', StepperDriver())

    subassembly.add('stepper', Stepper())
    subassembly.add('pulley', Pulley(0.0))
    subassembly.add('stepper_and_pulley', StepperAndPulley(0.0))

    subassembly = Assembly()
    inch_to_mm = 25.4
    config['linear_actuator_pa14p'] = {
        'size': 2.0 * inch_to_mm,
        'dist_to_mount': 0.78 * inch_to_mm,
        'dist_to_mount2': 0.4 * inch_to_mm,
        'width': 1.57 * inch_to_mm
    }
    subassembly.add('LinearActuatorPA14P', LinearActuatorPA14P(config['linear_actuator_pa14p'], 0.0 * inch_to_mm))
    
    config['linear_actuator_mounting_bracket_brk14'] = {
        'width': 1.04 * inch_to_mm,
        'length': 2.3 * inch_to_mm,
        'length_to_axle': 0.32 * inch_to_mm,
        'height_to_axle': 1.43 * inch_to_mm
    }
    subassembly.add('linear_actuator_mounting_bracket_brk14', LinearActuatorMountingBracketBRK14(config['linear_actuator_mounting_bracket_brk14']))

    config['linear_actuator_mounting_bracket_brk03'] = { 'length': 55.88 }
    subassembly.add('linear_actuator_mounting_bracket_brk03', LinearActuatorMountingBracketBRK03(config['linear_actuator_mounting_bracket_brk03']))

    config['actuator_small'] = { 'dist_to_mount': 4.85 }
    subassembly.add('linear_actuator_pa12t', LinearActuatorPA12T(config['actuator_small']))

    config['linear_actuator_and_bracket'] = {
        "stroke": 0.0 * inch_to_mm,
        "angle": 0.0,
        "explode_dist": 0.0
    }
    subassembly.add('linear_actuator_and_bracket', LinearActuatorAndBracket(config['linear_actuator_pa14p'], config['linear_actuator_mounting_bracket_brk14'], config['linear_actuator_and_bracket']))
    
    # Stock Magnets
    #subassembly.add('coin_magnet', MagnetCoin(20, 1.0))
    
    # Scotch Yotch
    config = {
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
    config["slider_x_width"] = config["pin_dia"] + 2.0
    config["slider_y_length"] = config["stroke_length"] / 2.0 + 2.0
    config["slider_y_width"] = config["pin_dia"] + 2.0
    config["slider_y_thickness"] = config["slider_x_thickness"]
    angle = math.pi / 180.0 * 90.0
    #subassembly.add('scotch_yoke', ScotchYoke(config, angle))
    
    # demo stacking/aligning with margin/pitch
    #subassembly.stack_x(5)
    #subassembly.stack_y(5)
    #subassembly.stack_z(5)

    # demo adding component to 
    #assembly = Assembly()
    #assembly.add('assembly', subassembly)
    #assembly.add('cube_big', Cube(50, 50, 50), position=(0, 50, 0), rotation=(0, 0, 45))

    # example of smarter methods to join components - WIP
    #subassembly.join_to_surface('cube', 'cylinder', align='bottom', face_align='top')
    #subassembly.join_to_surface('hexagon', 'trianglular_prism', align='front', face_align='back')
    #subassembly.join_to_surface('hexagon', 'trianglular_prism', align='left', face_align='left')
    #subassembly.join_to_surface('hexagon', 'trianglular_prism', align='bottom', face_align='bottom')

    #assembly.join_to_surface('assembly1', 'assembly2', align='top', face_align='bottom')

    assembly = subassembly
    
    return assembly

def main():
    parser = argparse.ArgumentParser(description="Controls for 3D printer component assemblies")
    parser.add_argument('--test', action='store_true', help='Run tests on the assembly')
    parser.add_argument('--export', type=str, help='Export assembly to SCAD file', metavar='FILENAME')
    parser.add_argument('--cross-section', nargs=2, metavar=('AXIS', 'POSITION'), help='Generate a cross-sectional view of the assembly')

    args = parser.parse_args()

    # example of config
    #config = {
    #    "prism": { "dim": {"l": 20, "w": 20, "h": 20}, "pos": {"x": 100, "y": 100, "z": 5}},
    #    "hexagon": { "dim": {"cle": 10, "h": 20}, "pos": {"x": 10, "y": 10, "z": 10}}#,
    #}
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

