from settings import *

class DepthFirst():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.visited = []
        self.route = None
        # print('hello')

    def update_position(self, move, i, j):
        if move == 'L':
            i -= 1
        elif move == 'R':
            i += 1
        elif move == 'U':
            j -= 1
        elif move == 'D':
            j += 1
        return i, j

    # check if a certain path is valid
    def check_valid(self, moves):
        i = self.start_node_x
        j = self.start_node_y
        for move in moves:
            i, j = self.update_position(move, i, j)

            if (i, j) in self.wall_pos:
                return False
        if (i, j) in self.visited:
            return False
        else:
            ##### Draw each node the computer is visiting as it is searching SIMULTNEOUSLY
            pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)

            ##### Redraw start/end nodes on top of all routes
            pygame.draw.rect(self.app.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
            pygame.draw.rect(self.app.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)
            pygame.display.update()
            self.visited.append((i, j))
            return True

    def findEnd(self, moves):
        i = self.start_node_x
        j = self.start_node_y
        for move in moves:
            i, j = self.update_position(move, i, j)

            print(i, j)
        if (i, j) == (self.end_node_x, self.end_node_y):
            return True
        return False

    def dfs_execute(self):
        # print('execute')
        stack = []
        stack.append("")
        last_out = ""

        while not self.findEnd(last_out):
            last_out = stack.pop()
            # print(add)
            for j in ["L", "R", "U", "D"]:
                latest_moves = last_out + j
                if self.check_valid(latest_moves):
                    stack.append(latest_moves)
        self.route = last_out


    def dfs_reset(self):
        self.visited = []
        self.route = None

