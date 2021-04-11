import pygame
import random
import settings


class Maze:
    def __init__(self, app, wall_pos):
        self.app = app
        self.visited = []
        self.walls = wall_pos
        # x-range index on drawable surface is 1 to 52
        # y range index is 1 to 30
        self.xMax = 53
        self.yMax = 31

    def generate_solid(self):
        for y in range(1, self.yMax):
            for x in range(1, self.xMax):
                self.walls.append((x, y))
                self.draw((x, y), settings.BLACK)
        self.render_grid()
        self.generate_maze()

    def generate_maze(self):
        x_pos = random.randint(1, self.xMax)
        y_pos = random.randint(1, self.yMax)
        start_pos = (x_pos, y_pos)
        self.recursive_dfs(start_pos)

    def is_valid(self, pos):
        if pos not in settings.wall_nodes_coords_list and pos in self.walls:
            return True
        return False

    def recursive_dfs(self, pos):
        moves_left = ['L', 'R', 'U', 'D']
        i, j = pos

        while moves_left:
            choose_rand_move = random.randint(0, len(moves_left) - 1)
            curr_move = moves_left.pop(choose_rand_move)
            # Temporary variabes to not update the original pos of the current node
            x_temp = i
            y_temp = j

            if curr_move == 'L':
                x_temp -= 2
            elif curr_move == 'R':
                x_temp += 2
            elif curr_move == 'U':
                y_temp += 2
            else:
                y_temp -= 2

            new_pos = (x_temp, y_temp)

            if self.is_valid(new_pos):
                self.walls.remove(new_pos)
                # calculate difference between curr pos and neighbouring pos
                diff_x = new_pos[0] - i
                diff_y = new_pos[1] - j

                # Determine the middle wall position to remove
                middle_wall_pos = (i + diff_x / 2, j + diff_y / 2)

                # Remove the middle wall as well
                self.walls.remove(middle_wall_pos)

                self.draw_maze(middle_wall_pos, settings.AQUAMARINE)
                self.draw_maze(new_pos, settings.AQUAMARINE)

                self.recursive_dfs(new_pos)

        return

    def draw(self, pos, colour):
        i, j = pos
        pygame.draw.rect(self.app.screen, colour, (i * 24 + 240, j * 24, 24, 24), 0)

    def draw_maze(self, pos, colour):
        self.draw(pos, colour)
        self.render_grid()  # Redraw grid (for aesthetic purposes lol)
        pygame.display.update()

    def render_grid(self):
        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, settings.ALICE,
                             (settings.GS_X + x * 24, settings.GS_Y), (settings.GS_X + x * 24, settings.GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, settings.ALICE,
                             (settings.GS_X, settings.GS_Y + y * 24), (settings.GE_X, settings.GS_Y + y * 24))
