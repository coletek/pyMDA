from solid import *
from solid.utils import *
from core import *
from geometry import *

#
# This added fillets to 2 or 4 sides, not all 12 sides as done by
# CubeCurvedEdges - perhaps merge these two functions
#

class CubeCurvedSides(Component):
    
    def __init__(self, x, y, z, corner_radius, side_count, is_center = True):
        super().__init__()
        self.width = x
        self.length = y
        self.height = z
        self.bounding_box["width"] = x
        self.bounding_box["length"] = y
        self.bounding_box["height"] = z
        self.is_center = is_center
        self.origin = [0, 0, 0]
        self.x = x
        self.y = y
        self.z = z
        self.corner_radius = corner_radius
        self.side_count = side_count
        
    def create(self):
        
        # alternative approach to minkowski, so it imports into OpenSCAD and export as STEP
        # TODO: support non-center option
        # using hull() still requires high segments - perhaps use rotate_extrude instead

        corner_round = translate([0, 0, -self.z / 2.0]) (cylinder(segments = self.segments_count, r = self.corner_radius, h = self.z))

        if self.side_count == 4:
            return hull() (
                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, 0]) (corner_round),
                translate([self.x / 2.0 - self.corner_radius, -self.y / 2.0 + self.corner_radius, 0]) (corner_round),
                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, 0]) (corner_round),
                translate([-self.x / 2.0 + self.corner_radius, -self.y / 2.0 + self.corner_radius, 0]) (corner_round),
            )
        elif self.side_count == 2:
            corner_sq = cube([self.corner_radius, self.corner_radius, self.z], center = True)
            # FIXME
            #return translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, 0]) (corner_round) + \
                #    translate([self.x / 2.0 - self.corner_radius + self.corner_radius / 2.0, self.y / 2.0 - self.corner_radius + self.corner_radius / 2.0, 0]) (corner_sq) + \
                #    translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, 0]) (corner_round) + \
                #    translate([-self.x / 2.0 + self.corner_radius - self.corner_radius / 2.0, self.y / 2.0 - self.corner_radius + self.corner_radius / 2.0, 0]) (corner_sq)
            return hull() (
                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, 0]) (corner_round),
                translate([self.x / 2.0 - self.corner_radius + self.corner_radius / 2.0, self.y / 2.0 - self.corner_radius + self.corner_radius / 2.0, 0]) (corner_sq),
                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, 0]) (corner_round),
                translate([-self.x / 2.0 + self.corner_radius - self.corner_radius / 2.0, self.y / 2.0 - self.corner_radius + self.corner_radius / 2.0, 0]) (corner_sq)
            )

#
# Curve all 12 sides of a cube - similar to BarCurvedEdges, but not rectangular
#
        
class CubeCurvedEdges(Component):
    
    def __init__(self, x, y, z, corner_radius, is_center = True):
        super().__init__()
        self.width = x
        self.length = y
        self.height = z
        self.bounding_box["width"] = x
        self.bounding_box["length"] = y
        self.bounding_box["height"] = z
        self.is_center = is_center
        self.origin = [0, 0, 0]
        self.x = x
        self.y = y
        self.z = z
        self.corner_radius = corner_radius

    def create(self):
        
    # alternative approach to minkowski, so it imports into OpenSCAD and export as STEP
    # using hull() still requires high segments - perhaps use rotate_extrude instead
    
        if self.is_center:
            return hull() (
                translate([-self.x / 2.0 + self.corner_radius, -self.y / 2.0 + self.corner_radius, -self.z / 2.0 + self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x / 2.0 - self.corner_radius, -self.y / 2.0 + self.corner_radius, -self.z / 2.0 + self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, -self.z / 2.0 + self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, -self.z / 2.0 + self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
            
                translate([-self.x / 2.0 + self.corner_radius, -self.y / 2.0 + self.corner_radius, self.z / 2.0 - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x / 2.0 - self.corner_radius, -self.y / 2.0 + self.corner_radius, self.z / 2.0 - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x / 2.0 - self.corner_radius, self.y / 2.0 - self.corner_radius, self.z / 2.0 - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([-self.x / 2.0 + self.corner_radius, self.y / 2.0 - self.corner_radius, self.z / 2.0 - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
            )
    
        else:
            return hull() (
                translate([self.corner_radius, self.corner_radius, self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x - self.corner_radius, self.corner_radius, self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x - self.corner_radius, self.y - self.corner_radius, self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.corner_radius, self.y - self.corner_radius, self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
            
                translate([self.corner_radius, self.corner_radius, self.z - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x - self.corner_radius, self.corner_radius, self.z - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.x - self.corner_radius, self.y - self.corner_radius, self.z - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
                translate([self.corner_radius, self.y - self.corner_radius, self.z - self.corner_radius]) (sphere(segments = self.segments_count, r = self.corner_radius)),
            )

#
# Curve all 12 sides of a bar - similar to CubeCurvedEdges, but not cubic
#
        
class BarCurvedEdges(Component):

    def __init__(self, length, thickness, corner_radius):
        super().__init__()
        self.width = thickness
        self.length = length
        self.height = thickness
        self.bounding_box["width"] = thickness
        self.bounding_box["length"] = length
        self.bounding_box["height"] = thickness
        self.origin = [0, 0, 0]
        self.thickness = thickness
        self.corner_radius = corner_radius
        
    def create(self):
        return CubeCurvedEdges(self.thickness, self.length, self.thickness, self.corner_radius, True).create()

#
# FIXME: only really works with ideal corner_radius and r selection
# e.g. CylinderCurvedEdges(20, 50, 10))
#

class CylinderCurvedEdges(Component):
    
    def __init__(self, r, h, corner_radius, both_sides = True, is_center = True, is_add_test = True):
        super().__init__()
        self.width = self.length = r * 2
        self.height = h
        self.bounding_box["width"] = self.bounding_box["length"] = r * 2
        self.bounding_box["height"] = h
        self.origin = [0, 0, 0]
        self.is_center = is_center
        self.is_add_test = is_add_test
        self.origin = [0, 0, self.height / 2.0]
        self.r = r
        self.corner_radius = corner_radius
        self.both_sides = both_sides
        
    def create(self):

        b_height = self.height - self.corner_radius
        if self.both_sides:
            b_height = self.height - self.corner_radius * 2.0
        b = cylinder(segments = self.segments_count, r = self.r, h = b_height)
        
        eb = Torus(self.r, self.corner_radius * 2, self.segments_count, 100).create()
        bb = cylinder(segments = self.segments_count, r = self.r - self.corner_radius, h = self.corner_radius * 2.0)

        p = translate([0, 0, self.corner_radius]) (b) + translate([0, 0, self.corner_radius]) (eb) + translate([0, 0, 0]) (bb)
    
        if self.both_sides:
            et = Torus(self.r, self.corner_radius * 2, self.segments_count, 100).create()
            bt = cylinder(segments = self.segments_count, r = self.r - self.corner_radius, h = self.corner_radius * 2.0)
            p += translate([0, 0, self.height - self.corner_radius]) (et) + translate([0, 0, self.height - self.corner_radius * 2.0]) (bt)

        if self.is_center:
            p = translate([0, 0, -self.origin[2]]) (p)
            self.origin = [0, 0, 0]
            
        return p

# Curved
    
class LineRoundViaHull(Component):
    
    def __init__(self, p1, p2, radius):
        super().__init__()
        self.width = p2[0] - p1[0] + radius * 2
        self.length = p2[1] - p1[1] + radius * 2
        self.height = p2[2] - p1[2] + radius * 2
        self.bounding_box["width"] = p2[0] - p1[0] + radius * 2
        self.bounding_box["length"] = p2[1] - p1[1] + radius * 2
        self.bounding_box["height"] = p2[2] - p1[2] + radius * 2
        self.origin = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
        self.p1 = p1
        self.p2 = p2
        self.radius = radius
    
    def create(self):

        s = sphere(r = self.radius, segments = self.segments_count)
        
        #s = cube_curved_sides(self.radius * 2, self.radius * 2, self.radius, 2.0, 4, self.segments_count)
        
        s1 = translate(self.p1) (s)
        s2 = translate(self.p2) (s)

        # TODO: use cylinder instead to avoid mesh
        p = hull() (s1, s2)
        #p = s1 + s2
        
        return p

class PolylineRound(Component):

    def __init__(self, pts, radius, is_close = False):
        super().__init__()
        self.pts = pts
        self.radius = radius
        self.is_close = is_close
    
    def create(self):

        if self.is_close:
            p = LineRoundViaHull(self.pts[len(self.pts) - 1], self.pts[0], self.radius).create()
        else:
            p = 0
        
        for i in range(len(self.pts) - 1):
            p += LineRoundViaHull(self.pts[i], self.pts[i + 1], self.radius).create()

        return p
