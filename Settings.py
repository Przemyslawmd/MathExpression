

class Settings:

    def __init__(self):
        self.x_grid = True
        self.y_grid = True
        self.precision = 0.1
        self.background_color = 'black'
        self.coordinates = False

        self.coordinates_changed = False
        self.grid_changed = False
        self.background_color_changed = False


    def apply_settings(self, x_grid, y_grid, precision, coordinates, background_colour):
        self.grid_changed = self.x_grid != x_grid or self.y_grid != y_grid
        self.x_grid = x_grid
        self.y_grid = y_grid

        self.precision = precision

        self.background_color_changed = self.background_color != background_colour
        self.background_color = background_colour

        self.coordinates_changed = self.coordinates != coordinates
        self.coordinates = coordinates



