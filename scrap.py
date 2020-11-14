from settings import *


class Node:
    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent


class Bidirectional():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.visited_f = [(self.start_node_x, self.start_node_y)]
        self.visited_r = [(self.end_node_x, self.end_node_y)]
        self.route_f = None
        self.route_r = None
        self.route_found = False

    def draw_all_paths(self, i, j, colour):
        ##### Draw each node the computer is visiting as it is searching SIMULTNEOUSLY
        pygame.draw.rect(self.app.screen, colour, (i * 24 + 240, j * 24, 24, 24), 0)

        ##### Redraw start/end nodes on top of all routes
        pygame.draw.rect(self.app.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GS_X + x * 24, GS_Y), (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GS_X, GS_Y + y * 24), (GE_X, GS_Y + y * 24))

        pygame.display.update()

    def checkValid(self, move, visited):
        if move not in self.wall_pos and move not in visited:
            visited.append(move)
            return True
        return False

    def findRoute(self, first_out, opp_visited):
        if first_out in opp_visited:
            return True
        return False

    def bidirectional_execute(self):
        start_node = Node((self.start_node_x, self.start_node_y), None)
        end_node = Node((self.end_node_x, self.end_node_y), None)
        fwd_queue = [start_node]
        rev_queue = [end_node]
        fwd_moves_queue = ['']
        rev_moves_queue = ['']

        while len(fwd_queue) and len(rev_queue) > 0:
            # Parent variables of parent nodes at the given time
            first_out_f = fwd_queue.pop(0)
            first_out_r = rev_queue.pop(0)
            first_moves_f = fwd_moves_queue.pop(0)
            first_moves_r = rev_moves_queue.pop(0)

            for m in ['L', 'R', 'U', 'D']:
                i, j = first_out_f
                a, b = first_out_r
                # print('parent:', i, j)
                if m == 'L':
                    i -= 1
                    a -= 1
                elif m == 'R':
                    i += 1
                    a += 1
                elif m == 'U':
                    j -= 1
                    b -= 1
                elif m == 'D':
                    j += 1
                    b += 1

                # Make new variable "latest_moves" for adding onto the queue again, because you don't want the 'parent' variable to change
                latest_moves_f = first_moves_f + m
                latest_moves_r = first_moves_r + m
                if self.checkValid((i, j), self.visited_f):
                    self.draw_all_paths(i, j, VIOLETRED)
                    fwd_queue.append((i, j))
                    fwd_moves_queue.append(latest_moves_f)

                if self.checkValid((a, b), self.visited_r):
                    self.draw_all_paths(a, b, TURQUOISE)
                    rev_queue.append((a, b))
                    rev_moves_queue.append(latest_moves_r)

                if self.findRoute((i, j), self.visited_r) or self.findRoute((a, b), self.visited_f):
                    self.route_f = latest_moves_f
                    self.route_r = latest_moves_r
                    self.route_found = True
                    break

            if self.route_found:
                break

