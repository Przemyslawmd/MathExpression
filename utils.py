

def is_max_points_exceeded(precision, x_min, x_max):
    max_points = 100000
    if x_min >= 0 and x_max >= 0:
        return (x_max - x_min) / precision > max_points
    if x_min < 0 and x_max < 0:
        return (x_min - x_max) * -1 / precision > max_points
    return (x_max + x_min * -1) / precision > max_points


