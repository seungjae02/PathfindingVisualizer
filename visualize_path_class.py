import pygame
import settings


class VisualizePath(object):

    def __init__(self, surface, position, path_coords):
        self.surface = surface
        self.position = position
        self.path_coords = path_coords

    def draw_path(self):
        self.path_coords.pop()
        for (x_pos, y_pos) in self.path_coords:
            pygame.draw.rect(self.surface, settings.SPRINGGREEN, (x_pos*24 + 240, y_pos*24, 24, 24), 0)
