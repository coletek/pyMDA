import math
from solid import *
from solid.utils import *
from core import *

#
# Fundamental Shapes
#

class Cube(Component):
    ''' 4sides (square) with depth '''
    
    def __init__(self, w, l, h, is_center = True, is_add_text = True):
        self.width = w
        self.length = l
        self.height = h
        self.is_center = is_center
        self.is_add_text = is_add_text
        if self.is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [self.width / 2.0, self.length / 2.0, self.height / 2.0]

    def create(self):
        if self.is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [self.width / 2.0, self.length / 2.0, self.height / 2.0]

        p = cube([self.width, self.length, self.height], self.is_center)

        if self.is_add_text:
            p = self.add_text(p)

        return p

class Cylinder(Component):
    
    def __init__(self, d, h, is_center = True, segments_count = 100, is_add_text = True):
        self.width = self.length = d
        self.height = h
        self.dia = d
        self.is_center = is_center
        self.segments_count = 100
        self.is_add_text = is_add_text
        if self.is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [0, 0, self.height / 2.0]

    def create(self):
        if self.is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [0, 0, self.height / 2.0]

        p = cylinder(d = self.dia, h = self.height, center = self.is_center, segments = self.segments_count)

        if self.is_add_text:
            p = self.add_text(p)

        return p

class Sphere(Component):
    
    def __init__(self, d, is_center = True, segments_count = 100, is_add_text = True):
        self.width = self.length = self.height = d
        self.dia = d
        self.is_center = is_center
        self.segments_count = 100
        self.is_add_text = is_add_text
        if self.is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [0, 0, self.height / 2.0]

    def create(self):
        self.origin = [0, 0, 0]
        p = sphere(d = self.dia, segments = self.segments_count)

        if self.is_add_text:
            p = self.add_text(p)

        if not self.is_center:
            p = translate([0, 0, self.height / 2]) (p)
            self.origin = [0, 0, self.height / 2]
        
        return p

class Pyramid(Component):
    def __init__(self, base_length, height, is_center=False, is_add_text=True):
        self.width = self.length = base_length
        self.height = height
        self.is_center = is_center
        self.is_add_text = is_add_text
        if self.is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [0, 0, self.height / 2.0]

    def create(self):
        # Define points for a square base
        points = [[-self.length / 2, -self.length / 2],
                  [self.length / 2, -self.length / 2],
                  [self.length / 2, self.length / 2],
                  [-self.length / 2, self.length / 2]]
        # Create pyramid
        p = polyhedron(
            points=points + [[0, 0, self.height]],
            faces=[[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]
        )

        self.origin = [0, 0, self.height / 2.0]
        
        if self.is_add_text:
            p = self.add_text(p)
            
        if self.is_center:
            p = translate([0, 0, -self.height / 2]) (p)
            self.origin = [0, 0, 0]
            
        return p

class Cone(Component):
    def __init__(self, dia, height, is_center=False, segments_count=100, is_add_text=True):
        self.width = self.length = dia
        self.height = height
        self.is_center = is_center
        self.segments_count = segments_count
        self.is_add_text = is_add_text
        self.dia = dia
        if self.is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [0, 0, self.height / 2.0]

    def create(self):
        p = cylinder(r1=self.dia/2, r2=0, h=self.height, center=self.is_center, segments=self.segments_count)
        if self.is_add_text:
            p = self.add_text(p)
        return p

class Tetrahedron(Component):
    def __init__(self, side_length, is_center = False, is_add_text = True):
        self.width = self.length = self.height = side_length
        self.is_center = is_center
        self.is_add_text = is_add_text
        if is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [0, 0, self.height / 2.0]
        self.side_length = side_length

    def create(self):
        # Height of a tetrahedron based on the equilateral triangle height
        height = (self.side_length * (2/3)**0.5)

        # The height from the triangular base to the apex
        apex_height = (2/3) * height

        # Points of the tetrahedron
        points = [
            (0, 0, 0),  # Base vertex A
            (self.side_length, 0, 0),  # Base vertex B
            (self.side_length / 2, height, 0),  # Base vertex C
            (self.side_length / 2, height / 3, apex_height)  # Apex vertex D
        ]

        # Faces using zero-based index references to the points
        faces = [
            [0, 1, 2],  # Base triangle ABC
            [0, 1, 3],  # Side triangle ABD
            [1, 2, 3],  # Side triangle BCD
            [2, 0, 3]   # Side triangle CAD
        ]

        # Create the tetrahedron
        p = polyhedron(points=points, faces=faces)

        self.width = self.side_length
        self.length = self.side_length / 2
        self.height = apex_height
        self.origin = [self.width / 2.0, self.length / 2.0, self.height / 2.0]
        
        if self.is_add_text:
            p = self.add_text(p)

        if self.is_center: 
            p = translate([-self.width / 2.0, -self.length / 2.0, -self.height / 2]) (p)
            self.origin = [0, 0, 0]
        else:
            p = translate([-self.width / 2.0, -self.length / 2.0, 0]) (p)
            self.origin = [0, 0, 0]
        
        return p
    
class Torus(Component): # donut
    def __init__(self, dia, thickness, segments_count, rotate_extrude_segments_count, is_center = True, is_add_text = True):
        self.width = self.length = dia + thickness
        self.height = thickness
        self.is_center = is_center
        self.is_add_text = is_add_text
        if is_center:
            self.origin = [0, 0, 0]
        else:
            self.origin = [0, 0, self.height / 2.0]
        self.dia = dia
        self.thickness = thickness
        self.segments_count = segments_count
        self.rotate_extrude_segments_count = rotate_extrude_segments_count
        
    def create(self):
        """Create a ring with specified dia, thickness, and segment counts."""
        p = rotate_extrude(convexity=10, segments=self.rotate_extrude_segments_count)(
            translate([self.dia / 2.0, 0, 0])(circle(d=self.thickness, segments=self.segments_count))
        )

        self.origin = [0, 0, 0]

        if self.is_add_text:
            p = self.add_text(p)

        if not self.is_center:
            p = translate([0, 0, self.height / 2]) (p)
            self.origin = [0, 0, self.height / 2]

        return p
    
#
# Prisms
#
    
class TriangularPrism(Component):
    '''3sides (triangle) with depth'''
    
    def __init__(self, w, l, h, is_center = True, is_add_text = True):
        self.width = w
        self.length = l
        self.height = h
        self.is_center = is_center
        self.is_add_text = is_add_text
        self.origin = [0, 0, 0]
        
    def create(self):
        """Create a prism with specified length, width, and height."""

        p = polyhedron(
            points=[
                [0, 0, 0],            # Point 0 - Bottom face
                [self.length, 0, 0],  # Point 1 - Bottom face
                [0, self.width, 0],  # Point 2 - Bottom face
                [0, self.width, 0],    # Point 3 - Bottom face
                [0, 0, self.height],   # Point 4 - Top face
                [self.length, 0, self.height],  # Point 5 - Top face
                [0, self.width, self.height],  # Point 6 - Top face
                [0, self.width, self.height]  # Point 7 - Top face
            ],
            faces=[
                [0, 1, 2, 3],  # Bottom face
                [4, 5, 6, 7],  # Top face
                [0, 1, 5, 4],  # Front face
                [1, 2, 6, 5],  # Right face
                [2, 3, 7, 6],  # Back face
                [3, 0, 4, 7]   # Left face
            ]
        )

        self.origin = [self.width / 2.0, self.length / 2.0, self.height / 2.0]
        
        if self.is_add_text:
            p = self.add_text(p)
        
        if self.is_center:
            p = translate([-self.origin[0], -self.origin[1], -self.origin[2]]) (p)
            self.origin = [0, 0, 0]
            
        return p

class HexagonalPrism(Component): # 6sides (hexagonal) base with depth
    def __init__(self, cle, h, is_center = True, is_add_text = True):
        self.cle = cle
        self.angle = 360.0 / 6.0;
        self.width = cle
        self.length_half = cle * 1.0 / math.tan(math.radians(self.angle))
        self.length = self.length_half * 2.0
        self.height = h
        self.origin = [0, 0, 0]
        self.is_center = is_center
        self.is_add_text = is_add_text
        
    def create(self):
        p = cube([self.width, self.length_half, self.height], center = True) + \
            rotate(self.angle, [0, 0, 1]) (cube([self.width, self.length_half, self.height], center = True)) + \
            rotate(2 * self.angle, [0, 0, 1]) (cube([self.width, self.length_half, self.height], center = True))

        self.origin = [0, 0, 0]

        if self.is_add_text:
            p = self.add_text(p)
        
        if self.is_center:
            p = translate([-self.origin[0], -self.origin[1], -self.origin[2]]) (p)
            self.origin = [0, 0, 0]
        else:
            p = translate([0, 0, self.height / 2]) (p)
            self.origin = [0, 0, self.height / 2]
            
        return p