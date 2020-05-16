import os
import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import Part
import importCSG

def convert_openscad_to_step(scad_filename, step_filename, objname = 'difference'):

    # NOTES:
    # * Works with ubuntu 18.04 (python 2.7.17 and freecad 0.16)
    # * Needs rework for ubuntu 20.04 (python 3.8.2 and freecad 0.18.4)
    
    # TODO: automatically determine the top level object (objname)
    
    part_name = os.path.basename(scad_filename)
    part_name = part_name.replace(".scad", "")
    
    importCSG.open(scad_filename)
    FreeCAD.setActiveDocument(part_name)
    part = FreeCAD.getDocument(part_name).getObject(objname)
    Part.export([part], step_filename)
