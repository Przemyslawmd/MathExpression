
from enum import Enum


class Color(Enum):
    BLACK = 0
    BLUE = 1
    GREEN = 2
    LIGHT_BLUE = 3
    LIGHT_GREEN = 4
    ORANGE = 5
    RED = 6
    YELLOW = 7
    WHITE = 8


class ColorData:
    def __init__(self, rgb, text):
        self.rgb = rgb
        self.text = text


Colors = {
    Color.BLACK:       ColorData((0, 0, 0), "Black"),
    Color.BLUE:        ColorData((0, 0, 255), "Blue"),
    Color.GREEN:       ColorData((0, 128, 0), "Green"),
    Color.LIGHT_BLUE:  ColorData((0, 191, 255), "Light Blue"),
    Color.LIGHT_GREEN: ColorData((0, 255, 128), "Light Green"),
    Color.ORANGE:      ColorData((255, 140, 0), "Orange"),
    Color.RED:         ColorData((255, 0, 0), "Red"),
    Color.YELLOW:      ColorData((255, 255, 0), "Yellow"),
    Color.WHITE:       ColorData((255, 255, 255), "White"),
}


