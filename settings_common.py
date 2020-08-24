#
# rendering settings:
# do locally
#

# low res
#bezier_step = 0.05
#segments_count = None
#rotate_extrude_segments_count = None

# high res
#bezier_step = 0.01
#segments_count = 50
#rotate_extrude_segments_count = 150

# export res
#bezier_step = 0.01
#segments_count = 100
#rotate_extrude_segments_count = 300

# temp
#bezier_step = 0.01
#segments_count = 200
#rotate_extrude_segments_count = 300

#
# magic numbers
#

golden_ratio = (1 + 5 ** 0.5) / 2
inch_to_mm = 25.4
mm_to_inch = 1.0 / inch_to_mm

#
# Colours
#

colour_pcb = [0, 0.549, 0.29]

#
# pcb settings
#

pcb_thickness_typical = 1.6
pcb_outline_tolerance = 0.2 # when CNC is used
pcb_hole_tolerance = 0.08
pcb_slot_min = 0.8 + pcb_outline_tolerance

#
# OpenSCAD settings
#

thickness_2d_shape = 1.0 # as defined by OpenSCAD 2D shapes
overlap = 0.01 # for cuts, joins
#overlap = 2.0 # for cuts, joins

#
# metal work tolerance settings
#
# https://www.protocase.com/resources/tolerances/profile-cutting.php

laser_tolerance = 0.13
extruded_chopsaw_tolerance = 0.25
chopsaw_tolerance = 1.02
bandsaw_tolerance = 3.18

#
# tolerance settings:
#
# * SLS - https://www.hlhprototypes.com/wp-content/uploads/2018/11/HLH-SLS-3D-Printing-Design-Guide-v1.0.pdf
# * SLA - https://www.hlhprototypes.com/wp-content/uploads/2018/11/HLH-SLA-3D-Printing-Design-Guide-v1.0.pdf
# * CNC - https://www.hlhprototypes.com/wp-content/uploads/2018/11/HLH-CNC-Machining-Design-Guide-v1.0.pdf
# * PCB - https://www.pcbway.com/pcb_prototype/PCB_Manufacturing_tolerances.html

cnc_metal_tolerance = 0.05
cnc_plastic_tolerance = 0.2
sls_tolerance = 0.3
sla_tolerance = 0.1

#
# clearance/mating settings:
#
# * SLS - https://www.hlhprototypes.com/wp-content/uploads/2018/11/HLH-SLS-3D-Printing-Design-Guide-v1.0.pdf
# * SLA - https://www.hlhprototypes.com/wp-content/uploads/2018/11/HLH-SLA-3D-Printing-Design-Guide-v1.0.pdf
# * CNC - https://www.hlhprototypes.com/wp-content/uploads/2018/11/HLH-CNC-Machining-Design-Guide-v1.0.pdf

# mating clearance between same part types
cnc_metal_clearance = 0.1 # if moving
cnc_plastic_clearance = 0.2 # if moving
sls_clearance = 0.5 # if moving
sla_clearance = 0.2 # if moving

# mating clearance between 3D prints and cots parts
sls_cots_clearance = 0.2 # if moving
sla_cots_clearance = 0.2 # if moving

#
# SLA printing settings
#

emboss_min_height = 0.5
deboss_min_height = 0.3

#
# IM settings
#

draft_angle = 1.5
wall_thickness_min = 1.0
wall_thickness_max = 3.0

#
# bolt threads:
#
# * https://www.trfastenings.com/Products/knowledgebase/Tables-Standards-Terminology/Tapping-Sizes-and-Clearance-Holes
# * https://ae01.alicdn.com/kf/HTB1hoF9LVXXXXczXXXXq6xXFXXXt/222055624/HTB1hoF9LVXXXXczXXXXq6xXFXXXt.jpg
# * https://image.pushauction.com/0/0/f2c27552-fb37-436a-9369-5b4293c5087b/eda41698-7b80-41de-b5b8-98625f130e93.jpg

m2_tap_hole_size = 1.6
m2_clearance_hole = 2.4
m2_head_size = 3.98
m2_head_or_nut_depth = 2.0

m2_5_tap_hole_size = 2.0
m2_5_clearance_hole = 2.9
m2_5_head_size = 4.68
m2_5_head_or_nut_depth = 2.36

m3_tap_hole_size = 2.5
m3_clearance_hole = 3.4
m3_head_size = 6.0

m4_tap_hole_size = 3.3
m4_clearance_hole = 4.5
m4_head_size = 8.0 # 7.0 for nylon bolt
m4_head_or_nut_depth = 5.0
m4_nut_size = 7.0
m4_nut_height = 3.0

m5_tap_hole_size = 4.2
m5_clearance_hole = 5.5

m10_tap_hole_size = 8.5 # fine
m10_die_rod_size = 10.0
m10_clearance_hole = 11

m20_tap_hole_size = 17.5 # fine
m20_clearance_hole = 22.0

#
# screw threads:
#
# * https://www.diydata.com/information/screwholes/screwholes.php

g8_clearance_hole = 4.5
g8_head_size = 8.0 # measured
g8_head_or_nut_depth = 4.0 # measured
