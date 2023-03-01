
from enum import Enum
from collections import namedtuple


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


ColorAttr = namedtuple('ColorAttr', ('rgb', 'text'))


Colors = {
    Color.BLACK:       ColorAttr((0, 0, 0), 'Black'),
    Color.BLUE:        ColorAttr((0, 0, 255), 'Blue'),
    Color.GREEN:       ColorAttr((0, 128, 0), 'Green'),
    Color.LIGHT_BLUE:  ColorAttr((0, 191, 255), 'Light Blue'),
    Color.LIGHT_GREEN: ColorAttr((0, 255, 128), 'Light Green'),
    Color.ORANGE:      ColorAttr((255, 140, 0), 'Orange'),
    Color.RED:         ColorAttr((255, 0, 0), 'Red'),
    Color.YELLOW:      ColorAttr((255, 255, 0), 'Yellow'),
    Color.WHITE:       ColorAttr((255, 255, 255), 'White'),
}


