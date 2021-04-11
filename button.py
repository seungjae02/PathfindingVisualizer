import pygame
import settings


class Button(object):
    """Base button class."""
    def __init__(self, app, colour, x, y, width, height, text, callback):
        self.app = app
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback

    def click(self):
        self.callback()

    def draw(self, outline=None):
        if outline:
            pygame.draw.rect(self.app.screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(self.app.screen, self.colour, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont(settings.FONT, settings.FONT_SIZE)
            text = font.render(self.text, 1, (0, 0, 0))
            # center text
            text_x = self.x + (self.width / 2 - text.get_width() / 2)
            text_y = self.y + (self.height / 2 - text.get_height() / 2)
            self.app.screen.blit(text, (text_x, text_y))

    def contains(self, pos):
        """Pos is the mouse position or a tuple of (x, y) coordinates."""
        pos_x, pos_y = pos
        return self.x < pos_x < self.x + self.width and self.y < pos_y < self.y + self.height


class MainMenuButton(Button):
    """Button to be displayed on the start screen."""
    def __init__(self, app, pos, text, callback):
        Button.__init__(self, app, settings.WHITE, pos * 220 + 8, 550, 200, 70, text, callback)

    def highlight(self, highlight):
        self.colour = settings.AQUAMARINE if highlight else settings.WHITE


class GridMenuButton(Button):
    """Button to be displayed on the start screen."""
    def __init__(self, app, pos, text, callback):
        Button.__init__(self, app, settings.AQUAMARINE, 20, 265 + 50 * pos + 20 * pos, 200, 50, text, callback)

    def highlight(self, highlight):
        self.colour = settings.STEELBLUE if highlight else settings.AQUAMARINE
