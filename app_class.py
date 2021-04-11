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
        self.start_end_checker = 0
        self.mouse_drag = 0

        # Start and End Nodes Coordinates
        self.pos_start = (None, None)
        self.pos_end = (None, None)

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = settings.wall_nodes_coords_list.copy()

        # Loading Images
        self.main_menu_background = pygame.image.load('main_background.png')
        self.grid_background = pygame.image.load('grid_logo.png')

        # Maze Class Instantiation
        self.maze = maze.Maze(self, self.wall_pos)

        # Define Main-Menu buttons
        self.but_bfs = button.MainMenuButton(self, 1, 'Breadth-First Search', self.on_click_but_bfs)
        self.but_dfs = button.MainMenuButton(self, 2, 'Depth-First Search', self.on_click_but_dfs)
        self.but_astar = button.MainMenuButton(self, 3, 'A-Star Search', self.on_click_but_astar)
        self.but_dijkstra = button.MainMenuButton(self, 4, 'Dijkstra Search', self.on_click_but_dijkstra)
        self.but_bidirect = button.MainMenuButton(self, 5, 'Bidirectional Search', self.on_click_but_bidirect)

        # Define Grid-Menu buttons
        self.but_se = button.GridMenuButton(self, 1, 'Start/End Node', self.on_click_but_se)
        self.but_wall = button.GridMenuButton(self, 2, 'Wall Node', self.on_click_but_wall)
        self.but_reset = button.GridMenuButton(self, 3, 'Reset', self.on_click_but_reset)
        self.but_start = button.GridMenuButton(self, 4, 'Visualize Path', self.on_click_but_start)
        self.but_main = button.GridMenuButton(self, 5, 'Main Menu', self.on_click_but_main)
        self.but_maze = button.GridMenuButton(self, 6, 'Generate Maze', self.on_click_but_maze)

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.render_main_menu()
                self.handle_main_menu_events()
            elif self.state == 'grid window':
                self.render_grid()
                self.handle_grid_events()
            elif self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            elif self.state == 'start visualizing':
                self.execute_search_algorithm()
            elif self.state == 'aftermath':
                self.reset_or_main_menu()

    def render_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))  # draw background
        self.render_main_menu_buttons()
        draw_text(
            'Made By: Seung Jae Yang', self.screen, [1200, 720], 28,
            settings.WHITE, settings.FONT, centered=False)
        pygame.display.update()

    def handle_main_menu_events(self):
        pos_mouse = pygame.mouse.get_pos()
        buttons = [self.but_bfs, self.but_dfs, self.but_astar, self.but_dijkstra, self.but_bidirect]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for but in buttons:
                    if but.contains(pos_mouse):
                        but.click()
            elif event.type == pygame.MOUSEMOTION:
                for but in buttons:
                    if but.contains(pos_mouse):
                        [b.highlight(b.contains(pos_mouse)) for b in buttons]

    def render_grid(self):
        self.screen.fill(settings.BLACK)
        pygame.draw.rect(self.screen, settings.WHITE, (0, 0, 240, 768), 0)
        self.screen.blit(self.grid_background, (0, 0))

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

        self.render_grid_buttons()
        pygame.display.update()

    def handle_grid_events(self):
        pos_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            self.grid_window_buttons(pos_mouse, event)

    def draw_nodes(self):
        # DRAWING STATE FUNCTIONS
        # Check where the mouse is clicking on grid
        # Add in feature to Draw nodes on grid
        # Add in feature so that the drawn nodes on grid translate onto text file
        # Function made in Helper Functions to check which button is pressed and to make it keep colour
        if self.state == 'draw S/E':
            self.but_se.colour = settings.MINT
        elif self.state == 'draw walls':
            self.but_wall.colour = settings.MINT

        self.render_grid_buttons()
        pygame.display.update()

        pos_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Grid button function from Helper Functions
            self.grid_window_buttons(pos_mouse, event)

            # Set boundaries for where mouse position is valid
            if 264 < pos_mouse[0] < 1512 and 24 < pos_mouse[1] < 744:
                pos_grid_x = (pos_mouse[0] - 264) // 24
                pos_grid_y = (pos_mouse[1] - 24) // 24
                # print('GRID-COORD:', x_grid_pos, y_grid_pos)

                # Get mouse position and check if it is clicking button. Then, draw if clicking. CHECK DRAG STATE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    # The chunk of code for start/end pos is placed here,
                    # because I do not want the drag feature to be available for start/end nodes
                    if self.state == 'draw S/E' and self.start_end_checker < 2:
                        # Choose point colour for grid and record the coordinate of start pos
                        if self.start_end_checker == 0 \
                                and (pos_grid_x+1, pos_grid_y + 1) not in self.wall_pos:
                            node_colour = settings.TOMATO
                            self.pos_start = (pos_grid_x+1, pos_grid_y + 1)
                            self.start_end_checker += 1

                        # Choose point colour for grid and record the coordinate of end pos
                        # Also, check that the end node is not the same point as start node
                        elif self.start_end_checker == 1 \
                                and (pos_grid_x+1, pos_grid_y + 1) != self.pos_start \
                                and (pos_grid_x+1, pos_grid_y + 1) not in self.wall_pos:
                            node_colour = settings.ROYALBLUE
                            self.pos_end = (pos_grid_x+1, pos_grid_y + 1)
                            self.start_end_checker += 1
                        else:
                            continue

                        # Draw point on Grid
                        pygame.draw.rect(self.screen, node_colour,
                                         (264 + pos_grid_x * 24, 24 + pos_grid_y * 24, 24, 24), 0)

                # Checks if mouse button is no longer held down
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                # Checks if mouse button is being held down; drag feature
                if self.mouse_drag == 1:
                    # Draw Wall Nodes and append Wall Node Coordinates to the Wall Nodes List
                    # Check if wall node being drawn/added is already in the list
                    # and check if it is overlapping start/end nodes
                    if self.state == 'draw walls':
                        if (pos_grid_x + 1, pos_grid_y + 1) not in self.wall_pos \
                                and (pos_grid_x + 1, pos_grid_y + 1) != self.pos_start \
                                and (pos_grid_x + 1, pos_grid_y + 1) != self.pos_end:
                            pygame.draw.rect(self.screen, settings.BLACK,
                                             (264 + pos_grid_x * 24, 24 + pos_grid_y * 24, 24, 24), 0)
                            self.wall_pos.append((pos_grid_x + 1, pos_grid_y + 1))

                for x in range(52):
                    pygame.draw.line(self.screen, settings.ALICE,
                                     (settings.GS_X + x * self.grid_square_length, settings.GS_Y),
                                     (settings.GS_X + x * self.grid_square_length, settings.GE_Y))
                for y in range(30):
                    pygame.draw.line(self.screen, settings.ALICE,
                                     (settings.GS_X, settings.GS_Y + y * self.grid_square_length),
                                     (settings.GE_X, settings.GS_Y + y * self.grid_square_length))

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.algorithm_state == 'bfs':
            algorithm = bfs_class.BreadthFirst(self, self.pos_start, self.pos_end, self.wall_pos)
        elif self.algorithm_state == 'dfs':
            algorithm = dfs_class.DepthFirst(self, self.pos_start, self.pos_end, self.wall_pos)
        elif self.algorithm_state == 'astar':
            algorithm = astar_class.AStar(self, self.pos_start, self.pos_end, self.wall_pos)
        elif self.algorithm_state == 'dijkstra':
            algorithm = dijkstra_class.Dijkstra(self, self.pos_start, self.pos_end, self.wall_pos)
        elif self.algorithm_state == 'bidirectional':
            algorithm = bidirectional_class.Bidirectional(self, self.pos_start, self.pos_end, self.wall_pos)
        else:
            algorithm = None

        if algorithm is not None:
            if self.pos_start[0] is not None or self.pos_end[0] is not None:
                algorithm.execute()
            if algorithm.route_found:
                for route in algorithm.get_routes():
                    draw_path = visualize_path_class.VisualizePath(self.screen, self.pos_start, route)
                    draw_path.draw_path()
            else:
                draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, settings.RED, settings.FONT, centered=True)

        pygame.display.update()
        self.state = 'aftermath'

    def reset_or_main_menu(self):
        self.render_grid_buttons()
        pygame.display.update()

        buttons = [self.but_se, self.but_wall, self.but_reset, self.but_start, self.but_main, self.but_maze]
        pos_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.but_reset.contains(pos_mouse):
                    self.execute_reset()
                elif self.but_main.contains(pos_mouse):
                    self.back_to_menu()
            elif event.type == pygame.MOUSEMOTION:
                for but in buttons:
                    if but.contains(pos_mouse):
                        [b.highlight(b.contains(pos_mouse)) for b in buttons]

    def grid_window_buttons(self, pos_mouse, event):
        """Function for the buttons on grid window. Became too repetitive so, I made it a function.
        Checks for state when button is clicked and changes button colour when hovered over."""
        buttons = [self.but_se, self.but_wall, self.but_reset, self.but_start, self.but_main, self.but_maze]
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for but in buttons:
                if but.contains(pos_mouse):
                    but.click()
        elif event.type == pygame.MOUSEMOTION:
            for but in buttons:
                if but.contains(pos_mouse):
                    [b.highlight(b.contains(pos_mouse)) for b in buttons]

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

    def render_main_menu_buttons(self):
        self.but_bfs.draw(settings.AQUAMARINE)
        self.but_dfs.draw(settings.AQUAMARINE)
        self.but_astar.draw(settings.AQUAMARINE)
        self.but_dijkstra.draw(settings.AQUAMARINE)
        self.but_bidirect.draw(settings.AQUAMARINE)

    def render_grid_buttons(self):
        self.but_se.draw(settings.STEELBLUE)
        self.but_wall.draw(settings.STEELBLUE)
        self.but_reset.draw(settings.STEELBLUE)
        self.but_start.draw(settings.STEELBLUE)
        self.but_main.draw(settings.STEELBLUE)
        self.but_maze.draw(settings.STEELBLUE)

    def on_click_but_bfs(self):
        self.algorithm_state = 'bfs'
        self.state = 'grid window'

    def on_click_but_dfs(self):
        self.algorithm_state = 'dfs'
        self.state = 'grid window'

    def on_click_but_astar(self):
        self.algorithm_state = 'astar'
        self.state = 'grid window'

    def on_click_but_dijkstra(self):
        self.algorithm_state = 'dijkstra'
        self.state = 'grid window'

    def on_click_but_bidirect(self):
        self.algorithm_state = 'bidirectional'
        self.state = 'grid window'

    def on_click_but_se(self):
        self.state = 'draw S/E'

    def on_click_but_wall(self):
        self.state = 'draw walls'

    def on_click_but_reset(self):
        self.execute_reset()

    def on_click_but_start(self):
        self.state = 'start visualizing'

    def on_click_but_main(self):
        self.back_to_menu()

    def on_click_but_maze(self):
        self.state = 'draw walls'
        self.maze.generate_solid()
        self.state = 'draw S/E'


def draw_text(words, screen, pos, size, colour, font_name, centered=False):
    font = pygame.font.SysFont(font_name, size)
    text = font.render(words, False, colour)
    text_size = text.get_size()
    if centered:
        pos[0] = pos[0] - text_size[0] // 2
        pos[1] = pos[1] - text_size[1] // 2
    screen.blit(text, pos)
