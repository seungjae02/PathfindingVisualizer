from settings import *

class DepthFirst():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.visited = [(self.start_node_x, self.start_node_y)]
        self.route = None

    def draw_all_paths(self, i, j):
        ##### Draw each node the computer is visiting as it is searching SIMULTNEOUSLY
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)

        ##### Redraw start/end nodes on top of all routes
        pygame.draw.rect(self.app.screen, TOMATO,
                         (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE,
                         (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GS_X + x * 24, GS_Y),
                             (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GS_X, GS_Y + y * 24),
                             (GE_X, GS_Y + y * 24))

        pygame.display.update()

    def checkValid(self, move):
        if move not in self.wall_pos and move not in self.visited:
            self.visited.append(move)
            return True
        return False

    def findEnd(self, first_out):
        if first_out == (self.end_node_x, self.end_node_y):
            return True
        return False

    def dfs_execute(self):
        stack = [(self.start_node_x, self.start_node_y)]
        moves_stack = ['']
        last_out = ''
        last_moves = ''

        while not self.findEnd(last_out):
            # Parent variables of parent nodes at the given time
            last_out = stack.pop()
            last_moves = moves_stack.pop()
            for m in ['L', 'R', 'U', 'D']:
                i, j = last_out
                print('parent:', i, j)
                if m == 'L':
                    i -= 1
                elif m == 'R':
                    i += 1
                elif m == 'U':
                    j -= 1
                elif m == 'D':
                    j += 1

                # Make new variable "latest_moves" for adding onto the queue again, because you don't want the 'parent' variable to change

                latest_moves = last_moves + m
                if self.checkValid((i, j)):
                    self.draw_all_paths(i, j)
                    stack.append((i, j))
                    moves_stack.append(latest_moves)

        self.route = last_moves


        # print('found! The end node is at:', first_out)

