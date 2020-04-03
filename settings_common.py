#
# rendering settings:
#

# low res
#bezier_step = 0.05
#segments_count = None

# high res
bezier_step = 0.01
segments_count = 100

#
# OpenSCAD settings
#

thickness_2d_shape = 1.0 # as defined by OpenSCAD 2D shapes
overlap = 0.01 # for cuts, joins
#overlap = 2.0 # for cuts, joins

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
pcb_outline_tolerance = 0.2 # when CNC is used
pcb_hole_tolerance = 0.08

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

#
# threads:
#
# * https://www.trfastenings.com/Products/knowledgebase/Tables-Standards-Terminology/Tapping-Sizes-and-Clearance-Holes
# * https://ae01.alicdn.com/kf/HTB1hoF9LVXXXXczXXXXq6xXFXXXt/222055624/HTB1hoF9LVXXXXczXXXXq6xXFXXXt.jpg

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

m4_tap_hole_size = 3.3
m4_clearance_hole = 4.5
m4_head_size = 8.0 # 7.0 for nylon bolt
m4_head_or_nut_depth = 5.0
m4_nut_size = 7.0
m4_nut_height = 3.0

m10_tap_hole_size = 8.5 # fine
m10_die_rod_size = 10.0
m10_clearance_hole = 11

m20_tap_hole_size = 17.5 # fine
m20_clearance_hole = 22.0
