import pygame
import settings


class VisualizePath(object):

    def __init__(self, surface, position, path, path_coords):
        self.surface = surface
        self.position = position
        self.path = path
        self.path_coords = path_coords

    def get_path_coords(self):
        """For BFS and DFS mainly."""
        x, y = self.position
        for move in self.path:
            if move == 'L':
                x -= 1
            elif move == 'R':
                x += 1
            elif move == 'U':
                y -= 1
            elif move == 'D':
                y += 1
            self.path_coords.append((x, y))

    def draw_path(self):
        self.path_coords.pop()
        for (x_pos, y_pos) in self.path_coords:
            pygame.draw.rect(self.surface, settings.SPRINGGREEN, (x_pos*24 + 240, y_pos*24, 24, 24), 0)
