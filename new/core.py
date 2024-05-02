from solid import *
from solid.utils import *
from solid.solidpython import scad_render_to_file

class Component:
    def create(self):
        raise NotImplementedError("Each component must implement the create method.")

    def test(self):
        raise NotImplementedError("Each component must implement the test method.")

    def get_height(self):
        raise NotImplementedError("Each component must implement the test method.")
    
class Assembly:
    def __init__(self):
        self.items = {}  # Stores both components and sub-assemblies

    def get_height(self):
        """Calculate the total height of the assembly."""
        max_height = 0
        for item_info in self.items.values():
            item_height = item_info['item'].get_height()
            vertical_position = item_info['position'][2]  # Z position
            # Total height is the position plus the item's height
            total_height = vertical_position + item_height
            if total_height > max_height:
                max_height = total_height
        return max_height
    
    def add(self, name, item, position=(0, 0, 0), rotation=(0, 0, 0)):
        """Add a component or sub-assembly with an optional position and rotation."""
        self.items[name] = {'item': item, 'position': position, 'rotation': rotation}

    def join_to_surface(self, base_name, added_name, align='top', face_align='top'):
        """Aligns 'added_name' component to 'base_name' component at specified surfaces."""
        base = self.items[base_name]
        added = self.items[added_name]

        # Mock-up example for alignment, needs actual implementation based on geometry
        base_pos = base['position']
        added_pos = added['position']

        if align == 'top' and face_align == 'top':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, base['item'].get_height() - added['item'].get_height())
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
        if align == 'top' and face_align == 'bottom':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, base['item'].get_height())
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
        if align == 'bottom' and face_align == 'top':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, -added['item'].get_height())
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
        if align == 'bottom' and face_align == 'bottom':
            # Align the top surface of added to the top surface of base
            offset = (0, 0, 0)
            added['position'] = (base_pos[0] + offset[0], base_pos[1] + offset[1], base_pos[2] + offset[2])
        
    def assemble(self):
        """Recursively creates the union of all items considering their positions and rotations."""
        model = None
        for item_info in self.items.values():
            item_model = item_info['item'].create()
            item_model = translate(item_info['position'])(item_model)
            item_model = rotate(item_info['rotation'])(item_model)
            model = union()(model, item_model) if model else item_model
        return model

    def test_assembly(self):
        """Test the complete assembly, including any sub-assemblies."""
        print("Running assembly tests...")
        for name, item_info in self.items.items():
            print(f"Testing {name}")
            item_info['item'].test()

    def export_scad(self, filename):
        """Export the assembly to an SCAD file."""
        model = self.assemble()
        scad_render_to_file(model, filename)
        print(f"Exported {filename}")

    def create(self):
        """Allow Assembly to be used interchangeably with Components."""
        return self.assemble()

    def cross_section_view(self, axis, position):
        """Generate a cross-sectional view of the assembly."""
        model = self.assemble()
        # Assuming axis='x' and position=0 for simplicity
        cross_section = intersection()(
            model,
            translate([position - 1, -100, -100])(cube([2, 200, 200]))
        )
        return cross_section
