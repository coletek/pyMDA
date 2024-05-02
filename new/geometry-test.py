import argparse
from solid import *
from solid.utils import *
from core import *
from geometry import *

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

    assembly = Assembly()
    assembly.add_component('prism', Prism(20, 20, 20), position=(0, 0, 0)) # optional pos,rot
    assembly.add_component('hexagon', Hexagon(10, 10), position=(0, 0, 0)) # optional pos,rot

    # example of smarter methods to join components
    assembly.join_to_surface('hexagon', 'prism', align='top', face_align='bottom')
    #assembly.join_to_surface('hexagon', 'prism', align='bottom', face_align='top')
    #assembly.join_to_surface('hexagon', 'prism', align='bottom', face_align='bottom')
    
    # Generate the model
    model = assembly.assemble()
    
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

