from solid import *
from solid.utils import *
from solid.solidpython import scad_render_to_file

class Component:
    def __init__(self):
        self.width = 0
        self.length = 0
        self.height = 0
        self.origin = [0, 0, 0]
    
    def create(self):
        raise NotImplementedError("Each component must implement the create method.")

    def test(self):
        if self.width < 0 or self.length < 0 or self.height < 0:
            return False
        return True

    def get_origin(self):
        return self.origin
    
    def get_width(self):
        return self.width

    def get_length(self):
        return self.length

    def get_height(self):
        return self.height

    def add_text(self, p):
        s = "%.0fx%.0fx%.0fmm" % (self.width, self.length, self.height)
        txt = text(s, size=self.height / 10.0, halign="center", valign="center", font="Arial:style=Bold")
        #txt = rotate(-45, [0, 0, 1]) (txt)
        txt = translate([self.origin[0], self.origin[1], self.origin[2] + self.height / 2.0])(txt)
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

    def get_depth(self):
        """Calculate the total depth of the assembly."""
        min_y = float('inf')
        max_y = float('-inf')
        for item_info in self.items.values():
            item_depth = item_info['item'].get_depth()
            depth_position = item_info['position'][1]  # Y position
            if depth_position + item_depth > max_y:
                max_y = depth_position + item_depth
            if depth_position < min_y:
                min_y = depth_position
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
        height = self.get_height()
        depth = self.get_depth()
    
        x_offset = width / 2
        y_offset = depth / 2
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

    def add(self, name, item, position=(0, 0, 0), rotation=(0, 0, 0)):
        """Add a component or sub-assembly with an optional position and rotation."""
        self.items[name] = {'item': item, 'position': position, 'rotation': rotation}

    def join_to_surface(self, base_name, added_name, align='top', face_align='top'):
        base = self.items[base_name]
        added = self.items[added_name]

        # Get origin points for both base and added items
        base_origin = base['item'].get_origin()
        added_origin = added['item'].get_origin()

        # Calculate the necessary translations for proper alignment
        offset = [0, 0, 0]  # Initialize offset for x, y, z

        # Horizontal alignment (adjustments based on width or depth can be similarly computed)
        if align == 'left':
            if face_align == 'left':
                offset[0] = base_origin[0] - base['item'].get_width() / 2.0
            elif face_align == 'right':
                offset[0] = base_origin[0] - base['item'].get_width() / 2.0 - added['item'].get_width()
        elif align == 'right':
            if face_align == 'left':
                offset[0] = base_origin[0] + base['item'].get_width() / 2.0
            elif face_align == 'right':
                offset[0] = base_origin[0] + base['item'].get_width() / 2.0 - added['item'].get_width()

        # Horizontal alignment (adjustments based on width or depth can be similarly computed)
        if align == 'front':
            if face_align == 'front':
                offset[1] = base_origin[0] - base['item'].get_depth() / 2.0
            elif face_align == 'back':
                offset[1] = base_origin[0] - base['item'].get_depth() / 2.0 - added['item'].get_depth()
        elif align == 'back':
            if face_align == 'front':
                offset[1] = base_origin[0] + base['item'].get_depth() / 2.0
            elif face_align == 'back':
                offset[1] = base_origin[0] + base['item'].get_depth() / 2.0 - added['item'].get_depth()

        # Assume get_height(), get_width(), get_depth() are implemented
        if align == 'top':
            if face_align == 'top':
                offset[2] = base['item'].get_height() - base_origin[2] - added['item'].get_height()
            elif face_align == 'bottom':
                offset[2] = base['item'].get_height() - base_origin[2]
        elif align == 'bottom':
            if face_align == 'top':
                offset[2] = base_origin[2] - base['item'].get_height() / 2 - added['item'].get_height() / 2
            elif face_align == 'bottom':
                offset[2] = base_origin[2] - base['item'].get_height()

        # Apply the calculated offset to the added item's position
        new_position = (
            base['position'][0] + offset[0],
            base['position'][1] + offset[1],
            base['position'][2] + offset[2]
        )
        added['position'] = new_position

    def assemble(self):
        """Recursively creates the union of all items considering their positions and rotations."""
        model = None
        for item_info in self.items.values():
            item_model = item_info['item'].create()
            item_model = rotate(item_info['rotation'])(item_model)
            item_model = translate(item_info['position'])(item_model)
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
