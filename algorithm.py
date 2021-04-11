import pygame
import settings


class Algorithm(object):
    """Base class for all algorithms."""
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end


class VisualisableAlgorithm(Algorithm):
    """Base class for all visualisable algorithms."""

    def __init__(self, pos_start, pos_end, app):
        Algorithm.__init__(self, pos_start, pos_end)
        self.app = app

    def draw_all_paths(self, position, colour):
        i, j = position

        # Draw each node the computer is visiting as it is searching SIMULTANEOUSLY
        pygame.draw.rect(self.app.screen, colour, (i * 24 + 240, j * 24, 24, 24), 0)

        # Redraw start/end nodes on top of all routes
        x, y = self.pos_start
        pygame.draw.rect(self.app.screen, settings.TOMATO,
                         (240 + x * 24, y * 24, 24, 24),
                         0)

        x, y = self.pos_end
        pygame.draw.rect(self.app.screen, settings.ROYALBLUE,
                         (240 + x * 24, y * 24, 24, 24),
                         0)

        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, settings.ALICE,
                             (settings.GS_X + x * 24, settings.GS_Y),
                             (settings.GS_X + x * 24, settings.GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, settings.ALICE,
                             (settings.GS_X, settings.GS_Y + y * 24),
                             (settings.GE_X, settings.GS_Y + y * 24))

        pygame.display.update()
