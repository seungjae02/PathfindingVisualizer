import pygame
import button
import maze
import settings
import astar_class
import bidirectional_class
import bfs_class
import dfs_class
import dijkstra_class
import visualize_path_class


class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
        self.grid_square_length = 24  # The dimensions of each grid square is 24 x 24

        # Loading Images
        self.main_menu_background = pygame.image.load('main_background.png')
        self.grid_background = pygame.image.load('grid_logo.png')

        self.start_end_checker = 0
        self.mouse_drag = 0

        # Start and End Nodes Coordinates
        self.pos_start = (None, None)
        self.pos_end = (None, None)

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = settings.wall_nodes_coords_list.copy()

        # Maze Class Instantiation
        self.maze = maze.Maze(self, self.wall_pos)

        # Define Main-Menu buttons
        self.but_bfs = button.MainMenuButton(self, 1, 'Breadth-First Search')
        self.but_dfs = button.MainMenuButton(self, 2, 'Depth-First Search')
        self.but_astar = button.MainMenuButton(self, 3, 'A-Star Search')
        self.but_dijkstra = button.MainMenuButton(self, 4, 'Dijkstra Search')
        self.but_bidirect = button.MainMenuButton(self, 5, 'Bidirectional Search')

        # Define Grid-Menu buttons
        self.but_se = button.GridMenuButton(self, 1, 'Start/End Node')
        self.but_wall = button.GridMenuButton(self, 2, 'Wall Node')
        self.but_reset = button.GridMenuButton(self, 3, 'Reset')
        self.but_start = button.GridMenuButton(self, 4, 'Visualize Path')
        self.but_main = button.GridMenuButton(self, 5, 'Main Menu')
        self.but_maze = button.GridMenuButton(self, 6, 'Generate Maze')

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

    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))
        self.but_bfs.draw(settings.AQUAMARINE)
        self.but_dfs.draw(settings.AQUAMARINE)
        self.but_astar.draw(settings.AQUAMARINE)
        self.but_dijkstra.draw(settings.AQUAMARINE)
        self.but_bidirect.draw(settings.AQUAMARINE)

    def sketch_hotbar(self):
        # Setup for Grid
        self.screen.fill(settings.BLACK)
        pygame.draw.rect(self.screen, settings.WHITE, (0, 0, 240, 768), 0)
        self.screen.blit(self.grid_background, (0, 0))

    def sketch_grid(self):
        # Add borders for a cleaner look
        pygame.draw.rect(self.screen, settings.ALICE, (240, 0, settings.WIDTH, settings.HEIGHT), 0)
        pygame.draw.rect(self.screen, settings.AQUAMARINE, (264, 24, settings.GRID_WIDTH, settings.GRID_HEIGHT), 0)

        # Draw grid
        # There are 52 square pixels across on grid [ WITHOUT BORDERS! ]
        # There are 30 square pixels vertically on grid [ WITHOUT BORDERS! ]
        for x in range(52):
            pygame.draw.line(
                self.screen, settings.ALICE,
                (settings.GS_X + x * self.grid_square_length, settings.GS_Y),
                (settings.GS_X + x * self.grid_square_length, settings.GE_Y))
        for y in range(30):
            pygame.draw.line(
                self.screen, settings.ALICE,
                (settings.GS_X, settings.GS_Y + y * self.grid_square_length),
                (settings.GE_X, settings.GS_Y + y * self.grid_square_length))

    def sketch_grid_buttons(self):
        self.but_se.draw(settings.STEELBLUE)
        self.but_wall.draw(settings.STEELBLUE)
        self.but_reset.draw(settings.STEELBLUE)
        self.but_start.draw(settings.STEELBLUE)
        self.but_main.draw(settings.STEELBLUE)
        self.but_maze.draw(settings.STEELBLUE)

    def grid_button_keep_colour(self):
        if self.state == 'draw S/E':
            self.but_se.colour = settings.MINT
        elif self.state == 'draw walls':
            self.but_wall.colour = settings.MINT

    def execute_reset(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.pos_start = (None, None)
        self.pos_end = (None, None)

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = settings.wall_nodes_coords_list.copy()

        # Switch States
        self.state = 'grid window'

    def back_to_menu(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.pos_start = (None, None)
        self.pos_end = (None, None)

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = settings.wall_nodes_coords_list.copy()

        # Switch States
        self.state = 'main menu'

    def main_menu_events(self):
        # draw Background
        pygame.display.update()
        self.sketch_main_menu()
        draw_text(
            'Made By: Seung Jae Yang', self.screen, [1200, 720], 28,
            settings.WHITE, settings.FONT, centered=False)

        # Get mouse position
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            # check if game is running
            if event.type == pygame.QUIT:
                self.running = False

            # check if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.but_bfs.contains(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'
                if self.but_dfs.contains(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'
                if self.but_astar.contains(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'
                if self.but_dijkstra.contains(pos):
                    self.algorithm_state = 'dijkstra'
                    self.state = 'grid window'
                if self.but_bidirect.contains(pos):
                    self.algorithm_state = 'bidirectional'
                    self.state = 'grid window'

            # highlight hovered button
            if event.type == pygame.MOUSEMOTION:
                for but in [self.but_bfs, self.but_dfs, self.but_astar, self.but_dijkstra, self.but_bidirect]:
                    but.highlight(but.contains(pos))

    def grid_window_buttons(self, pos, event):
        """Function for the buttons on grid window. Became too repetitive so, I made it a function.
        Checks for state when button is clicked and changes button colour when hovered over."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.but_se.contains(pos):
                self.state = 'draw S/E'
            elif self.but_wall.contains(pos):
                self.state = 'draw walls'
            elif self.but_reset.contains(pos):
                self.execute_reset()
            elif self.but_start.contains(pos):
                self.state = 'start visualizing'
            elif self.but_main.contains(pos):
                self.back_to_menu()
            elif self.but_maze.contains(pos):
                self.state = 'draw walls'
                self.maze.generateSolid()
                self.state = 'draw S/E'

        # highlight hovered button
        if event.type == pygame.MOUSEMOTION:
            for but in [self.but_se, self.but_wall, self.but_reset, self.but_start, self.but_main, self.but_maze]:
                but.highlight(but.contains(pos))

    def grid_events(self):
        # PLAYING STATE FUNCTIONS
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

    def draw_nodes(self):
        # DRAWING STATE FUNCTIONS
        # Check where the mouse is clicking on grid
        # Add in feature to Draw nodes on grid
        # Add in feature so that the drawn nodes on grid translate onto text file
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
            if 264 < pos[0] < 1512 and 24 < pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                # print('GRID-COORD:', x_grid_pos, y_grid_pos)

                # Get mouse position and check if it is clicking button. Then, draw if clicking. CHECK DRAG STATE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    # The chunk of code for start/end pos is placed here,
                    # because I do not want the drag feature to be available for start/end nodes
                    if self.state == 'draw S/E' and self.start_end_checker < 2:
                        # Choose point colour for grid and record the coordinate of start pos
                        if self.start_end_checker == 0 and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = settings.TOMATO
                            x, y = self.pos_start
                            self.pos_start = x+1, y+1
                            self.start_end_checker += 1

                        # Choose point colour for grid and record the coordinate of end pos
                        # Also, check that the end node is not the same point as start node
                        elif self.start_end_checker == 1 \
                                and (x_grid_pos+1, y_grid_pos+1) != self.pos_start \
                                and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = settings.ROYALBLUE
                            x, y = self.pos_end
                            self.pos_end = x+1, y+1
                            self.start_end_checker += 1
                        else:
                            continue

                        # Draw point on Grid
                        pygame.draw.rect(self.screen, node_colour,
                                         (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                # Checks if mouse button is no longer held down
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                # Checks if mouse button is being held down; drag feature
                if self.mouse_drag == 1:
                    # Draw Wall Nodes and append Wall Node Coordinates to the Wall Nodes List
                    # Check if wall node being drawn/added is already in the list
                    # and check if it is overlapping start/end nodes
                    if self.state == 'draw walls':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos \
                                and (x_grid_pos + 1, y_grid_pos + 1) != self.pos_start \
                                and (x_grid_pos + 1, y_grid_pos + 1) != self.pos_end:
                            pygame.draw.rect(self.screen, settings.BLACK,
                                             (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)
                            self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))

                for x in range(52):
                    pygame.draw.line(self.screen, settings.ALICE,
                                     (settings.GS_X + x * self.grid_square_length, settings.GS_Y),
                                     (settings.GS_X + x * self.grid_square_length, settings.GE_Y))
                for y in range(30):
                    pygame.draw.line(self.screen, settings.ALICE,
                                     (settings.GS_X, settings.GS_Y + y * self.grid_square_length),
                                     (settings.GE_X, settings.GS_Y + y * self.grid_square_length))

    def execute_search_algorithm(self):
        # VISUALIZATION FUNCTIONS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # BFS
        if self.algorithm_state == 'bfs':
            bfs = bfs_class.BreadthFirst(
                self, self.pos_start, self.pos_end, self.wall_pos)

            if self.pos_start[0] is not None or self.pos_end[0] is not None:
                bfs.execute()

            # Make Object for new path
            if bfs.route_found:
                draw_path = visualize_path_class.VisualizePath(
                    self.screen, self.pos_start, bfs.route, [])
                draw_path.get_path_coords()
                draw_path.draw_path()

            else:
                draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, settings.RED, settings.FONT, centered=True)

        # DFS
        elif self.algorithm_state == 'dfs':
            dfs = dfs_class.DepthFirst(
                self, self.pos_start, self.pos_end, self.wall_pos)

            if self.pos_start[0] is not None or self.pos_end[0] is not None:
                dfs.execute()

            # Make Object for new path
            if dfs.route_found:
                draw_path = visualize_path_class.VisualizePath(
                    self.screen, self.pos_start, dfs.route, [])
                draw_path.get_path_coords()
                draw_path.draw_path()

            else:
                draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, settings.RED, settings.FONT, centered=True)

        # A-STAR
        elif self.algorithm_state == 'astar':
            astar = astar_class.AStar(
                self, self.pos_start, self.pos_end, self.wall_pos)

            if self.pos_start[0] is not None or self.pos_end[0] is not None:
                astar.execute()

            if astar.route_found:
                draw_path = visualize_path_class.VisualizePath(
                    self.screen, self.pos_start, None, astar.route)
                draw_path.draw_path()

            else:
                draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, settings.RED, settings.FONT, centered=True)

        # DIJKSTRA
        elif self.algorithm_state == 'dijkstra':
            dijkstra = dijkstra_class.Dijkstra(
                self, self.pos_start, self.pos_end, self.wall_pos)

            if self.pos_start[0] is not None or self.pos_end[0] is not None:
                dijkstra.execute()

            if dijkstra.route_found:
                draw_path = visualize_path_class.VisualizePath(
                    self.screen, self.pos_start, None, dijkstra.route)
                draw_path.draw_path()

            else:
                draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, settings.RED, settings.FONT, centered=True)

        # BIDIRECTIONAL
        elif self.algorithm_state == 'bidirectional':
            bidirectional = bidirectional_class.Bidirectional(
                self, self.pos_start, self.pos_end, self.wall_pos)

            if self.pos_start[0] is not None or self.pos_end[0] is not None:
                bidirectional.execute()

            if bidirectional.route_found:
                draw_path_f = visualize_path_class.VisualizePath(
                    self.screen, self.pos_start, None, bidirectional.route_f)
                draw_path_r = visualize_path_class.VisualizePath(
                    self.screen, self.pos_end, None, bidirectional.route_r)

                draw_path_f.draw_path()
                draw_path_r.draw_path()

            else:
                draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, settings.RED, settings.FONT, centered=True)

        pygame.display.update()
        self.state = 'aftermath'

    def reset_or_main_menu(self):
        # AFTERMATH FUNCTIONS
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.but_se.contains(pos):
                    self.but_se.colour = settings.MINT
                elif self.but_wall.contains(pos):
                    self.but_wall.colour = settings.MINT
                elif self.but_reset.contains(pos):
                    self.but_reset.colour = settings.MINT
                elif self.but_start.contains(pos):
                    self.but_start.colour = settings.MINT
                elif self.but_main.contains(pos):
                    self.but_main.colour = settings.MINT
                else:
                    self.but_se.colour = settings.STEELBLUE
                    self.but_wall.colour = settings.STEELBLUE
                    self.but_reset.colour = settings.STEELBLUE
                    self.but_start.colour = settings.STEELBLUE
                    self.but_main.colour = settings.STEELBLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.but_reset.contains(pos):
                    self.execute_reset()
                elif self.but_main.contains(pos):
                    self.back_to_menu()


def draw_text(words, screen, pos, size, colour, font_name, centered=False):
    font = pygame.font.SysFont(font_name, size)
    text = font.render(words, False, colour)
    text_size = text.get_size()
    if centered:
        pos[0] = pos[0] - text_size[0] // 2
        pos[1] = pos[1] - text_size[1] // 2
    screen.blit(text, pos)
