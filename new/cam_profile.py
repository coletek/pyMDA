def cam_profile(height, start_radius, start_angle, end_radius, end_angle, increment = 0.01, is_center = True):

    points = []

    angle_range = end_angle - start_angle

    radius_step = (end_radius - start_radius) / (angle_range / increment)

    radius = start_radius
    for i in np.arange(start_angle, end_angle, increment):
        x = radius * cos(i)
        y = radius * sin(i)
        pt = [x, y]
        points.append(pt)
        radius += radius_step

    return linear_extrude(height, center = is_center) (polygon(points=points))

def cam_profile_find_radius(target_angle, start_radius, start_angle, end_radius, end_angle, increment = 0.01):

    # TODO: this could/should be replaced with a single equation - can't think of the solution right now.
    
    angle_range = end_angle - start_angle

    radius_step = (end_radius - start_radius) / (angle_range / increment)

    # end_angle + 1deg is required to complete the loop
    radius = start_radius
    for i in np.arange(start_angle, end_angle + math.radians(1.0), increment):
        #print ("i=%f(%fdeg) radius_step=%f start_angle=%f(%fdeg) end_angle=%f(%fdeg) target_angle=%f(%fdeg) radius=%f" % \
        #       (i, math.degrees(i), radius_step, start_angle, math.degrees(start_angle), end_angle, math.degrees(end_angle), target_angle, math.degrees(target_angle), radius))
        if round(math.degrees(i)) == round(math.degrees(target_angle)):
            return radius
        radius += radius_step

    return False
