
from Color import Color, Colors


class Settings:

    def __init__(self):
        self.x_grid = True
        self.y_grid = True
        self.precision = 0.1
        self.background = Color.BLACK
        self.coordinates = False

        self.coordinates_changed = False
        self.grid_changed = False
        self.background_changed = False


    def apply_settings(self, x_grid, y_grid, precision, coordinates, background):
        self.grid_changed = self.x_grid != x_grid or self.y_grid != y_grid
        self.x_grid = x_grid
        self.y_grid = y_grid

        self.precision = precision

        color = next((key for key, value in Colors.items() if value.text == background), None)
        self.background_changed = self.background != color
        self.background = color

        self.coordinates_changed = self.coordinates != coordinates
        self.coordinates = coordinates


