from solid import *
from solid.utils import *
from solid.solidpython import scad_render_to_file

class Component:
    
    def create(self):
        raise NotImplementedError("Each component must implement the create method.")
    
    def test(self):
        raise NotImplementedError("Each component must implement the create method.")

class Assembly:
    def __init__(self):
        self.components = {}  # Dictionary to hold components and their transformations

    def add_component(self, name, component, position=(0, 0, 0), rotation=(0, 0, 0)):
        """Add a component with an optional position and rotation."""
        self.components[name] = {'component': component, 'position': position, 'rotation': rotation}

    def join_to_surface(self, base_name, added_name, align='top', face_align='top'):
        """Aligns 'added_name' component to 'base_name' component at specified surfaces."""
        base = self.components[base_name]
        added = self.components[added_name]

        # Mock-up example for alignment, needs actual implementation based on geometry
        base_pos = base['position']
        added_pos = added['position']

        if align == 'top' and face_align == 'top':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, base['component'].height - added['component'].height)
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
        if align == 'top' and face_align == 'bottom':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, base['component'].height)
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
        if align == 'bottom' and face_align == 'top':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, -added['component'].height)
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
        if align == 'bottom' and face_align == 'bottom':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, 0)
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])

            
    def assemble(self):
        """Creates the union of all components considering their positions and rotations."""
        assembly = None
        for comp_info in self.components.values():
            comp = comp_info['component'].create()
            comp = translate(comp_info['position'])(comp)
            comp = rotate(comp_info['rotation'])(comp)
            assembly = union()(assembly, comp) if assembly else comp
        return assembly

    def test_assembly(self):
        """Test the complete assembly."""
        print("Running assembly tests...")
        for name in self.components:
            print(f"Testing {name}")
            self.components[name]['component'].test()

    def export_scad(self, filename):
        model = self.assemble()
        scad_render_to_file(model, filename)
        print(f"Exported {filename}")

    def cross_section_view(self, axis, position):
        model = self.assemble()
        # Assuming axis='x' and position=0 for simplicity
        cross_section = intersection()(
            model,
            translate([position - 1, -100, -100])(cube([2, 200, 200]))
        )
        return cross_section
