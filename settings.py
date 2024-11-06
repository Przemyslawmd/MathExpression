
from color import Color, Colors


class Settings:

    def __init__(self):
        self.x_grid = True
        self.y_grid = True
        self.precision = 0.1
        self.background = Color.BLACK
        self.coordinates = False
        self.graph_label = False


    def set_settings(self, x_grid, y_grid, precision, coordinates, background, graph_label):
        grid_changed = self.x_grid != x_grid or self.y_grid != y_grid
        self.x_grid = x_grid
        self.y_grid = y_grid

        self.precision = precision

        color = next((key for key, value in Colors.items() if value.text == background), None)
        background_changed = self.background != color
        self.background = color

        coordinates_changed = self.coordinates != coordinates
        self.coordinates = coordinates

        self.graph_label = graph_label
        return grid_changed, background_changed, coordinates_changed


