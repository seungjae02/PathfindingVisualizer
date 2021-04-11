import app_class
import pygame
import sys

if __name__ == '__main__':
    pygame.init()
    app = app_class.App()
    app.run()
    pygame.quit()
    sys.exit()
