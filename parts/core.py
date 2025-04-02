import math
from solid import *
from solid.utils import *
from solid.solidpython import scad_render_to_file

class Component:
    def __init__(self):
        self.config = {}
        self.segments_count = 100
        self.color = {}
        self.width = 0
        self.length = 0
        self.height = 0
        self.origin = [0, 0, 0]
        self.bounding_box = { "width": 0, "length": 0, "height": 0}
    
    def create(self):
        raise NotImplementedError("Each component must implement the create method.")

    def test(self):
        if self.bounding_box["width"] <= 0 or self.bounding_box["length"] < 0 or self.bounding_box["height"] < 0:
            return False
        return True

    def set_segment_count(self, segments_count):
        self.segments_count = segments_count

    def set_color(self, color):
        self.color = color

    def get_origin(self):
        return self.origin

    def get_width(self):
        return self.bounding_box["width"]

    def get_length(self):
        return self.bounding_box["length"]

    def get_height(self):
        return self.bounding_box["height"]

    def add_text(self, p):
        s = "%.0fx%.0fx%.0fmm" % (self.bounding_box["width"], self.bounding_box["length"], self.bounding_box["height"])
        txt = text(s, size=self.bounding_box["height"] / 10.0, halign="center", valign="center", font="Arial:style=Bold")
        #txt = rotate(-45, [0, 0, 1]) (txt)
        txt = translate([self.origin[0], self.origin[1], self.origin[2] + self.bounding_box["height"] / 2.0])(txt)
        return union() (p, txt)
    
class Assembly:
    def __init__(self):
        self.items = {}  # Stores both components and sub-assemblies

    def get_origin(self):
        raise NotImplementedError("Each component must implement the test method.")
        
    def get_width(self):
        """Calculate the total width of the assembly."""
        min_x = float('inf')
        max_x = float('-inf')
        for item_info in self.items.values():
            item_width = item_info['item'].get_width()
            horizontal_position = item_info['position'][0]  # X position
            if horizontal_position + item_width > max_x:
                max_x = horizontal_position + item_width
            if horizontal_position < min_x:
                min_x = horizontal_position
        return max_x - min_x

    def get_length(self):
        """Calculate the total length of the assembly."""
        min_y = float('inf')
        max_y = float('-inf')
        for item_info in self.items.values():
            item_length = item_info['item'].get_length()
            length_position = item_info['position'][1]  # Y position
            if length_position + item_length > max_y:
                max_y = length_position + item_length
            if length_position < min_y:
                min_y = length_position
        return max_y - min_y
    
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

    def center_assembly(self):
        """Reposition all components so the assembly is centered at the origin."""
        width = self.get_width()
        length = self.get_length()
        height = self.get_height()
    
        x_offset = width / 2
        y_offset = length / 2
        z_offset = height / 2

        for item_info in self.items.values():
            pos = item_info['position']
            item_info['position'] = (pos[0] - x_offset, pos[1] - y_offset, pos[2] - z_offset)

    def stack_x(self, margin):
        current_x = 0
        old_item = 0
        for name, item in self.items.items():
            try:
                current_x += old_item.get_width() / 2.0 + margin + self.items[name]['item'].get_width() / 2
            except:
                current_x = 0
            new_position = (current_x, item['position'][1], item['position'][2])
            self.items[name]['position'] = new_position
            old_item = self.items[name]['item']

    def stack_y(self, margin):
        current_y = 0
        old_item = 0
        for name, item in self.items.items():
            try:
                current_y += old_item.get_length() / 2.0 + margin + self.items[name]['item'].get_length() / 2
            except:
                current_y = 0
            new_position = (item['position'][0], current_y, item['position'][2])
            self.items[name]['position'] = new_position
            old_item = self.items[name]['item']
            
    def stack_z(self, margin):
        current_z = 0
        old_item = 0
        for name, item in self.items.items():
            try:
                current_z += old_item.get_height() / 2.0 + margin + self.items[name]['item'].get_height() / 2
            except:
                current_z = 0
            new_position = (item['position'][0], item['position'][1], current_z)
            self.items[name]['position'] = new_position
            old_item = self.items[name]['item']

    def add(self, name, item, position=(0, 0, 0), rotation=(0, 0, 0), parent=None):
        """Add a component with optional parent for hierarchical transformations."""
        self.items[name] = {
            'item': item,
            'position': position,
            'rotation': rotation,
            'parent': parent
        }

    def assemble(self):
        built = {}

        def apply_transform(name, parent_pos=(0, 0, 0), parent_rot=(0, 0, 0)):
            item_info = self.items[name]
            item = item_info['item']
            local_pos = item_info['position']
            local_rot = item_info['rotation']
            parent = item_info.get('parent')

            # Compose transformations
            def rotate_vector(vec, rot):
                x, y, z = vec
                rx, ry, rz = [math.radians(r) for r in rot]

                # Apply Z
                cz, sz = math.cos(rz), math.sin(rz)
                x, y = x * cz - y * sz, x * sz + y * cz

                # Apply Y
                cy, sy = math.cos(ry), math.sin(ry)
                x, z = x * cy + z * sy, -x * sy + z * cy
                
                # Apply X
                cx, sx = math.cos(rx), math.sin(rx)
                y, z = y * cx - z * sx, y * sx + z * cx
                
                return [x, y, z]

            # Recursively build parent transform if needed
            if parent:
                parent_pos, parent_rot = built[parent]['abs_pos'], built[parent]['abs_rot']

            abs_pos = [a + b for a, b in zip(parent_pos, rotate_vector(local_pos, parent_rot))]
            abs_rot = [a + b for a, b in zip(parent_rot, local_rot)]

            model = item.create()
            model = rotate(local_rot)(model)
            model = translate(local_pos)(model)
            model = rotate(parent_rot)(model)
            model = translate(parent_pos)(model)
            
            built[name] = {
                'model': model,
                'abs_pos': abs_pos,
                'abs_rot': abs_rot
            }

            return model

        full_model = None
        for name in self.items:
            if name not in built:
                model = apply_transform(name)
                full_model = union()(full_model, model) if full_model else model

        return full_model if full_model else cube(0)
        

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
