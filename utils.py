
from enum import Enum


def is_max_points_exceeded(precision, x_min, x_max):
    max_points = 100000
    if x_min >= 0 and x_max >= 0:
        return (x_max - x_min) / precision > max_points
    if x_min < 0 and x_max < 0:
        return (x_min - x_max) * -1 / precision > max_points
    return (x_max + x_min * -1) / precision > max_points


class RangeType(Enum):
    X = 0,
    Y = 1,


def calculate_range(min_str, max_str, range_type):
    if range_type is RangeType.X and (not min_str or not max_str):
        raise Exception("Range error: minimum and maximum for X can not be empty")
    elif range_type is RangeType.Y:
        if not min_str and not max_str:
            return 0, 0
        if not min_str or not max_str:
            raise Exception("Range error: only one value for Y range provided")
    try:
        min_value = float(min_str)
        max_value = float(max_str)
    except Exception as e:
        raise Exception(f"Range error: {str(e)}")
    if min_value > max_value:
        raise Exception("Range error: minimum higher than maximum")
    return min_value, max_value


