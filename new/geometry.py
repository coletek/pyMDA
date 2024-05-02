from solid import *
from solid.utils import *

class Cube:
    @staticmethod
    def create(x, y, z, is_center=True):
        """Create a standard cube with specified dimensions."""
        return cube([x, y, z], center=is_center)

class Cylinder:
    # Handles cylinders with options for curved edges

class Prism:
    @staticmethod
    def create(l, w, h):
        """Create a prism with specified length, width, and height."""
        return polyhedron(
            points=[[0, 0, 0], [l, 0, 0], [l, w, 0], [0, w, 0], [0, w, h], [l, w, h]],
            faces=[[0, 1, 2, 3], [5, 4, 3, 2], [0, 4, 5, 1], [0, 3, 4], [5, 2, 1]]
        )
    
class CurvedCube(Cube):
    def __init__(self, x, y, z, corner_radius, side_count, segments_count, is_center=True):
        self.x = x
        self.y = y
        self.z = z
        self.corner_radius = corner_radius
        self.side_count = side_count
        self.segments_count = segments_count
        self.is_center = is_center

    def create(self):
        """Create a cube with curved sides depending on the side count."""
        corner_round = translate([0, 0, -self.z / 2.0])(cylinder(segments=self.segments_count, r=self.corner_radius, h=self.z))
        if self.side_count == 4:
            return hull()(
                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round),
                translate([self.x / 2.0 - self.corner_radius, -self.y / 2.0 + self.corner_radius, 0])(corner_round),
                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round),
                translate([-self.x / 2.0 + self.corner_radius, -self.y / 2.0 + self.corner_radius, 0])(corner_round),
            )
        elif self.side_count == 2:
            return hull()(
                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round),
                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round)
            )

class Ring:
    @staticmethod
    def create(r, thickness, segments_count, rotate_extrude_segments_count):
        """Create a ring with specified radius, thickness, and segment counts."""
        return rotate_extrude(convexity=10, segments=rotate_extrude_segments_count)(
            translate([r, 0, 0])(circle(d=thickness, segments=segments_count))
        )

