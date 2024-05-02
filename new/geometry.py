import math
from solid import *
from solid.utils import *
from core import *

class Prism(Component):
    def __init__(self, l, w, h):
        self.length = l
        self.width = w
        self.height = h
        
    def create(self):
        """Create a prism with specified length, width, and height."""
        return polyhedron(
            points=[[0, 0, 0],
                    [self.length, 0, 0],
                    [self.length, self.width, 0],
                    [0, self.width, 0],
                    [0, self.width, self.height],
                    [self.length, self.width, self.height]],
            faces=[[0, 1, 2, 3],
                   [5, 4, 3, 2],
                   [0, 4, 5, 1],
                   [0, 3, 4],
                   [5, 2, 1]]
        )

    def test(self):
        if self.length < 0 or self.width < 0 or self.height < 0:
            return False
        return True

    def get_height(self):
        return self.height
    
class Hexagon(Component):
    def __init__(self, cle, h):
        self.cle = cle
        self.height = h
        self.center = False
        
    def create(self):
        angle = 360.0 / 6.0;
        cote = self.cle * 1.0 / math.tan(math.radians(angle));
        p = cube([self.cle, cote, self.height], center = True) + \
            rotate(angle, [0, 0, 1]) (cube([self.cle, cote, self.height], center = True)) + \
            rotate(2 * angle, [0, 0, 1]) (cube([self.cle, cote, self.height], center = True))
        if not self.center:
            p = translate([0, 0, self.height / 2.0]) (p)
        return p

    def test(self):
        if self.cle < 0 or self.height < 0:
            return False
        return True

    def get_height(self):
        return self.height
    
class Ring(Component):
    def create(self, r, thickness, segments_count, rotate_extrude_segments_count):
        """Create a ring with specified radius, thickness, and segment counts."""
        return rotate_extrude(convexity=10, segments=rotate_extrude_segments_count)(
            translate([r, 0, 0])(circle(d=thickness, segments=segments_count))
        )

class CylinderCurvedEdges(Component):
    def create(self, r, h, corner_radius, both_sides, segments_count):

        b_height = h - corner_radius
        if both_sides:
            b_height = h - corner_radius * 2.0
        b = cylinder(segments = segments_count, r = r, h = b_height)

        eb = ring(r, corner_radius * 2, segments_count)
        bb = cylinder(segments = segments_count, r = r - corner_radius, h = corner_radius * 2.0)

        p = translate([0, 0, corner_radius]) (b) + translate([0, 0, corner_radius]) (eb) + translate([0, 0, 0]) (bb)
    
        if both_sides:
            et = ring(r, corner_radius * 2, segments_count)
            bt = cylinder(segments = segments_count, r = r - corner_radius, h = corner_radius * 2.0)
            p += translate([0, 0, h - corner_radius]) (et) + translate([0, 0, h - corner_radius * 2.0]) (bt)
    
        return p

class RodCurvedEdges(Component):
    def create(self, length, thickness, corner_radius, segments_count):
        return cube_curved_edges(thickness, length, thickness, corner_radius, segments_count, True)

class LineRoundViaHull(Component):
    def create(self, p1, p2, radius, segments_count):

        s = sphere(r = radius, segments = segments_count)
        
        #s = cube_curved_sides(radius * 2, radius * 2, radius, 2.0, 4, segments_count)
        
        s1 = translate(p1) (s)
        s2 = translate(p2) (s)

        # TODO: use cylinder instead to avoid mesh
        p = hull() (s1, s2)
        #p = s1 + s2
        
        return p

class PolylineRound(Component):
    def create(self, pts, radius, segments_count, close):

        if close:
            p = line_round_via_hull(pts[len(pts) - 1], pts[0], radius, segments_count)
        else:
            p = 0
        
        for i in range(len(pts) - 1):
            p += line_round_via_hull(pts[i], pts[i + 1], radius, segments_count)

        return p
    
#class Cube:
#    @staticmethod
#    def create(x, y, z, is_center=True):
#        """Create a standard cube with specified dimensions."""
#        return cube([x, y, z], center=is_center)
    
#class Cylinder:
#    # Handles cylinders with options for curved edges
    
#class CurvedCube(Cube):
#    def __init__(self, x, y, z, corner_radius, side_count, segments_count, is_center=True):
#        self.x = x
#        self.y = y
#        self.z = z
#        self.corner_radius = corner_radius
#        self.side_count = side_count
#        self.segments_count = segments_count
#        self.is_center = is_center

#    def create(self):
#        """Create a cube with curved sides depending on the side count."""
#        corner_round = translate([0, 0, -self.z / 2.0])(cylinder(segments=self.segments_count, r=self.corner_radius, h=self.z))
#        if self.side_count == 4:
#            return hull()(
#                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round),
#                translate([self.x / 2.0 - self.corner_radius, -self.y / 2.0 + self.corner_radius, 0])(corner_round),
#                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round),
#                translate([-self.x / 2.0 + self.corner_radius, -self.y / 2.0 + self.corner_radius, 0])(corner_round),
#            )
#        elif self.side_count == 2:
#            return hull()(
#                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round),
#                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, 0])(corner_round)
#            )

