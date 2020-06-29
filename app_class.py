import pygame, sys
from settings import *
from main_menu_buttons import *

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.load()
        self.bfs_button = MainMenuButtons(self, WHITE, 338, BUTTON_HEIGHT, 200, 70, 'Breadth-First Search')
        self.dfs_button = MainMenuButtons(self, WHITE, 558, BUTTON_HEIGHT, 200, 70, 'Deep-First Search')
        self.astar_button = MainMenuButtons(self, WHITE, 778, BUTTON_HEIGHT, 200, 70, 'A-Star Search')
        self.dijkstra_button = MainMenuButtons(self, WHITE, 998, BUTTON_HEIGHT, 200, 70, 'Dijkstra Search')

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu()
            if self.state == 'playing':
                self.drawingboard()
        pygame.quit()
        sys.exit()

#################################### HELPER FUNCTIONS #########################################

    def load(self):
        self.background = pygame.image.load('main_background.png')

#################################### MAIN MENU FUNCTIONS ######################################

    def main_menu(self):
        # Draw Background
        pygame.display.update()
        self.screen.blit(self.background, (0, 0))

        # Draw Buttons
        self.bfs_button.draw_main_button(AQUAMARINE)
        self.dfs_button.draw_main_button(AQUAMARINE)
        self.astar_button.draw_main_button(AQUAMARINE)
        self.dijkstra_button.draw_main_button(AQUAMARINE)

        # Check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is hovering over button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.state = 'playing'
                if self.dfs_button.isOver(pos):
                    self.state = 'playing'
                if self.astar_button.isOver(pos):
                    self.state = 'playing'
                if self.dijkstra_button.isOver(pos):
                    self.state = 'playing'

            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEMOTION:
                if self.bfs_button.isOver(pos):
                    self.bfs_button.colour = AQUAMARINE
                elif self.dfs_button.isOver(pos):
                    self.dfs_button.colour = AQUAMARINE
                elif self.astar_button.isOver(pos):
                    self.astar_button.colour = AQUAMARINE
                elif self.dijkstra_button.isOver(pos):
                    self.dijkstra_button.colour = AQUAMARINE
                else:
                    self.bfs_button.colour, self.dfs_button.colour, self.astar_button.colour, self.dijkstra_button.colour = WHITE, WHITE, WHITE, WHITE

#################################### PLAYING STATE FUNCTIONS ######################################

    def drawingboard(self):




