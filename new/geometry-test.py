import argparse
from solid import *
from solid.utils import *
from core import *
from geometry import *
from curved import *

def build(config):

    # Fundamental Shapes
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

