from settings import *

class VisualizePath():
    def __init__(self, surface, start_node_x, start_node_y, path):
        self.surface = surface
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.path = path
        self.path_coords = list()

    def get_path_coords(self):
        i = self.start_node_x
        j = self.start_node_y
        for move in self.path:
            if move == 'L':
                i -= 1
            elif move == 'R':
                i += 1
            elif move == 'U':
                j -= 1
            elif move == 'D':
                j += 1
            self.path_coords.append((i,j))

    def draw_path(self):
        self.path_coords.pop()
        for (x_pos, y_pos) in self.path_coords:
            pygame.draw.rect(self.surface, SPRINGGREEN, (x_pos*24 + 240, y_pos*24, 24, 24), 0)
