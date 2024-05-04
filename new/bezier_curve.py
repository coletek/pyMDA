def bezier_coordinate(t, n0, n1, n2, n3):
    return n0 * math.pow((1 - t), 3) + 3 * n1 * t * math.pow((1 - t), 2) + 3 * n2 * math.pow(t, 2) * (1 - t) + n3 * math.pow(t, 3)

def bezier_point(t, p0, p1, p2, p3):
    return [
        bezier_coordinate(t, p0[0], p1[0], p2[0], p3[0]),
        bezier_coordinate(t, p0[1], p1[1], p2[1], p3[1]),
        bezier_coordinate(t, p0[2], p1[2], p2[2], p3[2])
    ]

def bezier_curve_pts(t_step, p0, p1, p2, p3):
    p = []
    for t in np.arange(0, t_step + 1, t_step):
        p.append(bezier_point(t, p0, p1, p2, p3))

    return p

def bezier_curve_pts_brace_xyz(pts, pts2):
    xx_min = 1000
    xx_max = -1000
    yy_min = 1000
    yy_max = -1000
    zz_min = 1000
    zz_max = -1000
    
    for xx, yy, zz in pts:
        #print xx, yy, zz
        for xxx, yyy, zzz in pts2:
            if xx > xxx:
                xx_max = xxx            
            if xx < xxx:
                xx_min = xxx
            if yy > yyy:
                yy_max = yyy           
            if yy < yyy:
                yy_min = yyy
            if zz > zzz:
                zz_max = zzz           
            if zz < zzz:
                zz_min = zzz

    return [ xx_min, yy_min, zz_min, xx_max, yy_max, zz_max ]

def bezier_curve_pts_brace(t_step, p0, p1, p2, p3, pts):
    pts_brace = bezier_curve_pts(t_step, p0, p1, p2, p3)

    # get new pts
    [x_min, y_min, z_min, x_max, y_max, z_max] = bezier_curve_pts_brace_xyz(pts_brace, pts)
    #print [x_min, y_min, z_min, x_max, y_max, z_max]

    p0 = [-x_max, y_max, z_min]
    p1 = [-x_max, y_min, z_max]
    p2 = [x_max, y_min, z_max]
    p3 = [x_max, y_max, z_min]

    p = bezier_curve_pts(t_step, p0, p1, p2, p3)

    return p

def bezier_point_debug(t, p0, p1, p2, p3):
    pos = [
        bezier_coordinate(t, p0[0], p1[0], p2[0], p3[0]),
        bezier_coordinate(t, p0[1], p1[1], p2[1], p3[1]),
        bezier_coordinate(t, p0[2], p1[2], p2[2], p3[2])
    ]
    return color(Blue) (translate(pos) (sphere(r = 2)))

def bezier_curve_pts_debug(t_step, p0, p1, p2, p3):
    p = color(Red) (translate(p0) (sphere(r = 10)))
    p += color(Red) (translate(p1) (sphere(r = 10)))
    p += color(Red) (translate(p2) (sphere(r = 10)))
    p += color(Red) (translate(p3) (sphere(r = 10)))

    for t in np.arange(0, t_step + 1, t_step):
        p += bezier_point_debug(t, p0, p1, p2, p3)

    return p
