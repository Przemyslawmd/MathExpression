
def is_max_points_exceeded(precision, x_min, x_max):
    max_points = 100000
    if x_min >= 0 and x_max >= 0:
        return (x_max - x_min) / precision > max_points
    if x_min < 0 and x_max < 0:
        return (x_min - x_max) * -1 / precision > max_points
    return (x_max + x_min * -1) / precision > max_points


def range_x(min_str, max_str):
    if not min_str or not max_str:
        raise Exception("Range error: minimum and maximum for X can not be empty")
    return calculate_range(min_str, max_str)


def range_y(min_str, max_str):
    if not min_str and not max_str:
        return 0, 0
    if not min_str or not max_str:
        raise Exception("Range error: only one value for Y range provided")
    return calculate_range(min_str, max_str)


def calculate_range(min_str, max_str):
    try:
        min_value = float(min_str)
        max_value = float(max_str)
    except Exception as e:
        raise Exception(f"Range error: {str(e)}")
    if min_value > max_value:
        raise Exception("Range error: minimum higher than maximum")
    return min_value, max_value


