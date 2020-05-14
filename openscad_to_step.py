import os
import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import importCSG

def convert_openscad_to_step(scad_filename, step_filename, objname = 'difference'):
    
    part_name = os.path.basename(scad_filename)
    part_name = part_name.replace(".scad", "")
    
    importCSG.open(scad_filename)
    FreeCAD.setActiveDocument(part_name)
    part = FreeCAD.getDocument(part_name).getObject(objname)
    Part.export([part], step_filename)
