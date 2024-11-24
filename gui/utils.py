
from math import fabs

from errorStorage import ErrorStorage


axis_changes = (
    0.1, 0.11, 0.125, 0.15, 0.2, 0.25, 0.33, 0.5, 0.65, 0.75, 0.85, 1, 1.15, 1.33, 1.5, 2, 3, 4, 5, 7, 8, 9, 10
)


def is_max_points_exceeded(precision, x_min, x_max):
    max_points = 100000
    if x_min >= 0 and x_max >= 0:
        return (x_max - x_min) / precision > max_points
    if x_min < 0 and x_max < 0:
        return (x_min - x_max) * -1 / precision > max_points
    return (x_max + x_min * -1) / precision > max_points


def range_x(min_str, max_str):
    if not min_str or not max_str:
        ErrorStorage.put_error("Range error: minimum and maximum for X can not be empty")
        return None, None
    return calculate_range(min_str, max_str)


def calculate_range(min_str, max_str):
    try:
        min_value = float(min_str)
        max_value = float(max_str)
    except Exception as e:
        ErrorStorage.put_error(f"Range error: {str(e)}")
        return None, None
    if min_value > max_value:
        ErrorStorage.put_error("Range error: minimum higher than maximum")
        return None, None
    return min_value, max_value


def calculate_range_change(slider, min_axis, max_axis):
    index = slider.value()
    ratio = axis_changes[index]
    axis_range = fabs(min_axis) - fabs(max_axis) if max_axis <= 0 and min_axis < 0 else max_axis - min_axis
    new_axis_range = axis_range * ratio
    return (new_axis_range - axis_range) / 2

