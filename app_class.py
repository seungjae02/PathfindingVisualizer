import pygame, sys
from settings import *
from buttons import *

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.grid_square_length = 24 # The dimensions of each grid square is 24 x 24
        self.load()

        # Define Main-Menu buttons
        self.bfs_button = Buttons(self, WHITE, 338, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Breadth-First Search')
        self.dfs_button = Buttons(self, WHITE, 558, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Deep-First Search')
        self.astar_button = Buttons(self, WHITE, 778, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'A-Star Search')
        self.dijkstra_button = Buttons(self, WHITE, 998, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Dijkstra Search')

        # Define Grid-Menu buttons
        self.start_end_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start/End Node')
        self.wall_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Wall Node')
        self.reset_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*2 + BUTTON_SPACER*2, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Reset')
        self.start_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*3 + BUTTON_SPACER*3, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Visualize Path')

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'show grid':
                self.grid_events()
        pygame.quit()
        sys.exit()

#################################### SETUP FUNCTIONS #########################################

##### Loading Images
    def load(self):
        self.main_menu_background = pygame.image.load('main_background.png')
        self.grid_background = pygame.image.load('grid_logo.png')

##### Setup for Main Menu
    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))

        # Draw Buttons
        self.bfs_button.draw_button(AQUAMARINE)
        self.dfs_button.draw_button(AQUAMARINE)
        self.astar_button.draw_button(AQUAMARINE)
        self.dijkstra_button.draw_button(AQUAMARINE)

##### Setup for Grid
    def sketch_hotbar(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)
        self.screen.blit(self.grid_background, (0, 0))

    def sketch_grid(self):
        # Add borders for a cleaner look
        pygame.draw.rect(self.screen, ALICE, (240, 0, WIDTH, HEIGHT), 0)
        pygame.draw.rect(self.screen, AQUAMARINE, (264, 24, GRID_WIDTH, GRID_HEIGHT), 0)

        # Draw grid
        # There are 52 square pixels across on grid [ WITHOUT BORDERS! ]
        # There are 30 square pixels vertically on grid [ WITHOUT BORDERS! ]
        for x in range(52):
            pygame.draw.line(self.screen, ALICE, (GS_X + x*self.grid_square_length, GS_Y),
                             (GS_X + x*self.grid_square_length, GE_Y))
        for y in range(30):
            pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y*self.grid_square_length),
                             (GE_X, GS_Y + y*self.grid_square_length))

    def sketch_grid_buttons(self):
        # Draw buttons
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)

#################################### EXECUTION FUNCTIONS #########################################

##### MAIN MENU FUNCTIONS

    def main_menu_events(self):
        # Draw Background
        pygame.display.update()
        self.sketch_main_menu()

        # Check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.state = 'show grid'
                if self.dfs_button.isOver(pos):
                    self.state = 'show grid'
                if self.astar_button.isOver(pos):
                    self.state = 'show grid'
                if self.dijkstra_button.isOver(pos):
                    self.state = 'show grid'

            # Get mouse position and check if it is hovering over button
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

##### PLAYING STATE FUNCTIONS

    def grid_events(self):
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_end_node_button.isOver(pos):
                    print('pressed a')
                elif self.wall_node_button.isOver(pos):
                    print('pressed b')
                elif self.reset_button.isOver(pos):
                    print('pressed c')
                elif self.start_button.isOver(pos):
                    print('pressed d')

            # Get mouse position and check if it is hovering over button
            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = MINT
                elif self.start_button.isOver(pos):
                    self.start_button.colour = MINT
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE









