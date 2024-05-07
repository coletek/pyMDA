import argparse
from solid import *
from solid.utils import *

from core import *
from geometry import *
from curved import *
from stock_materials import *
from stock_magnets import *
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

    # Stock Materials
    subassembly.add('square_hollow_section', SHS(30, 3, 30))
    subassembly.add('channel_section', CS(30, 3, 30))
    subassembly.add('l_section', LS(30, 30, 3, 30))
    subassembly.add('solid_section', SB(30, 30))
    subassembly.add('rod', Rod(10, 30))
    subassembly.add('sheet', Sheet(30, 30, 3))
    #subassembly.add('wedge', Wedge(10, 10, 2, 2))
    #subassembly.add('hinge', Hinge(3, 10, 20, 100, 100, 1, True, 100))

    # Stock Bearings - TBC
    # Stock Electronics - TBC
    # Stock Fixutres - TBC
    # Stock Motors - TBC

    # Stock Magnets - TBC

    #subassembly = Assembly()
    subassembly.add('coin_magnet', MagnetCoin(20, 1.0))
    
    # Utilites - TBC    
    # Cam Profile - TBC
    # Collar - TBC
    # Enclosures - TBC
    # Holes - TBC
    # Plates - TBC

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
    subassembly.add('scotch_yoke', ScotchYoke(config, angle))

    
    # demo stacking/aligning with margin/pitch
    #subassembly.stack_x(5)
    subassembly.stack_y(5)
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

