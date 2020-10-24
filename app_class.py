import sys
from settings import *
from buttons import *
from bfs_class import *
from dfs_class import *
from astar_class import *
from dijkstra_class import *
from visualize_path_class import *

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
        self.grid_square_length = 24 # The dimensions of each grid square is 24 x 24
        self.load()
        self.start_end_checker = 0
        self.mouse_drag = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()

        # Define Main-Menu buttons
        self.bfs_button = Buttons(self, WHITE, 338, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Breadth-First Search')
        self.dfs_button = Buttons(self, WHITE, 558, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Depth-First Search')
        self.astar_button = Buttons(self, WHITE, 778, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'A-Star Search')
        self.dijkstra_button = Buttons(self, WHITE, 998, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Dijkstra Search')

        # Define Grid-Menu buttons
        self.start_end_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start/End Node')
        self.wall_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Wall Node')
        self.reset_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*2 + BUTTON_SPACER*2, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Reset')
        self.start_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*3 + BUTTON_SPACER*3, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Visualize Path')
        self.main_menu_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 4 + BUTTON_SPACER * 4, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Main Menu')

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'start visualizing':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main_menu()

        pygame.quit()
        sys.exit()

#################################### SETUP FUNCTIONS #########################################

##### Loading Images
    def load(self):
        self.main_menu_background = pygame.image.load('main_background.png')
        self.grid_background = pygame.image.load('grid_logo.png')

##### Draw Text
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

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
        self.main_menu_button.draw_button(STEELBLUE)

##### Function for the buttons on grid window. Became too repetitive so, I made it a function. Checks for state when button is clicked and changes button colour when hovered over.
    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.isOver(pos):
                self.state = 'draw walls'
            elif self.reset_button.isOver(pos):
                self.execute_reset()
            elif self.start_button.isOver(pos):
                self.state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                self.back_to_menu()

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
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.colour = MINT
            else:
                self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour, self.main_menu_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

    def grid_button_keep_colour(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.colour = MINT

        elif self.state == 'draw walls':
            self.wall_node_button.colour = MINT

    def execute_reset(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None


        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()

        # Switch States
        self.state = 'grid window'

    def back_to_menu(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()

        # Switch States
        self.state = 'main menu'


#################################### EXECUTION FUNCTIONS #########################################

##### MAIN MENU FUNCTIONS

    def main_menu_events(self):
        # Draw Background
        pygame.display.update()
        self.sketch_main_menu()
        self.draw_text('Made By: Seung Jae Yang', self.screen, [1200, 720], 28, WHITE, FONT, centered=False)

        # Check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'
                if self.dfs_button.isOver(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'
                if self.astar_button.isOver(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'
                if self.dijkstra_button.isOver(pos):
                    self.algorithm_state = 'dijkstra'
                    self.state = 'grid window'

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

##### PLAYING STATE FUNCTIONS #####

    def grid_events(self):
        #print(len(wall_nodes_coords_list))
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

##### DRAWING STATE FUNCTIONS #####
    # Check where the mouse is clicking on grid
    # Add in feature to Draw nodes on grid
    # Add in feature so that the drawn nodes on grid translate onto text file
    def draw_nodes(self):
        # Function made in Helper Functions to check which button is pressed and to make it keep colour
        self.grid_button_keep_colour()
        self.sketch_grid_buttons()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

            # Set boundaries for where mouse position is valid
            if pos[0] > 264 and pos[0] < 1512 and pos[1] > 24 and pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                #print('GRID-COORD:', x_grid_pos, y_grid_pos)

                # Get mouse position and check if it is clicking button. Then, draw if clicking. CHECK DRAG STATE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    # The chunk of code for start/end pos is placed here, because I do not want the drag feature to be available for start/end nodes
                    if self.state == 'draw S/E' and self.start_end_checker < 2:
                        # Choose point colour for grid and record the coordinate of start pos
                        if self.start_end_checker == 0:
                            node_colour = TOMATO
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            # print(self.start_node_x, self.start_node_y)
                            self.start_end_checker += 1

                        # Choose point colour for grid and record the coordinate of end pos
                        # Also, check that the end node is not the same point as start node
                        elif self.start_end_checker == 1 and (x_grid_pos+1, y_grid_pos+1) != (self.start_node_x, self.start_node_y):
                            node_colour = ROYALBLUE
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.start_end_checker += 1

                        else:
                            continue

                        # Draw point on Grid
                        pygame.draw.rect(self.screen, node_colour, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                # Checks if mouse button is no longer held down
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                # Checks if mouse button is being held down; drag feature
                if self.mouse_drag == 1:
                    # Draw Wall Nodes and append Wall Node Coordinates to the Wall Nodes List
                    # Check if wall node being drawn/added is already in the list and check if it is overlapping start/end nodes
                    if self.state == 'draw walls':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):
                            pygame.draw.rect(self.screen, BLACK, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)
                            self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))
                        # print(len(self.wall_pos))

                for x in range(52):
                    pygame.draw.line(self.screen, ALICE, (GS_X + x * self.grid_square_length, GS_Y),
                                     (GS_X + x * self.grid_square_length, GE_Y))
                for y in range(30):
                    pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y * self.grid_square_length),
                                     (GE_X, GS_Y + y * self.grid_square_length))

#################################### VISUALIZATION FUNCTIONS #########################################

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        #print(self.start_node_x, self.start_node_y)
        #print(self.end_node_x, self.end_node_y)

        ### BFS ###

        if self.algorithm_state == 'bfs':
            self.bfs = BreadthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()

            # Make Object for new path
            if self.bfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.bfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768,384], 50, RED, FONT, centered = True)

        ### DFS ###

        elif self.algorithm_state == 'dfs':
            self.dfs = DepthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()

            # Make Object for new path
            if self.dfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.dfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768,384], 50, RED, FONT, centered = True)

        ### A-STAR ###

        elif self.algorithm_state == 'astar':
            self.astar = AStar(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.astar.astar_execute()

            if self.astar.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.astar.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, centered=True)

        ### DIJKSTRA ###

        elif self.algorithm_state == 'dijkstra':
            self.dijkstra = Dijkstra(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dijkstra.dijkstra_execute()

            if self.dijkstra.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.dijkstra.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, centered=True)

        pygame.display.update()
        self.state = 'aftermath'

#################################### AFTERMATH FUNCTIONS #########################################

    def reset_or_main_menu(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = MINT
                elif self.start_button.isOver(pos):
                    self.start_button.colour = MINT
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.colour = MINT
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour, self.main_menu_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.isOver(pos):
                    self.execute_reset()
                elif self.main_menu_button.isOver(pos):
                    self.back_to_menu()





























