import sys

sys.path.append('/usr/lib/freecad/lib')

import FreeCAD
import Part
import importCSG

def convert_openscad_to_step(scad_filename, step_filename)
    importCSG.open(scad_filename)
    App.setActiveDocument(p)
    objname = "difference"
    part = FreeCAD.getDocument(p).getObject(objname)
    Part.export([part], step_filename)
