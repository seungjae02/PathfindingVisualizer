from settings import *
class Node:
    def __init__(self, position = None, parent = None):
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
        self.visited_pos_f = [(self.start_node_x, self.start_node_y)]
        self.visited_pos_r = [(self.end_node_x, self.end_node_y)]
        self.visited_node_f = []
        self.visited_node_r = []
        self.route_f = []
        self.route_r = []
        self.route_found = False

    def draw_all_paths(self, pos, colour):
        i, j = pos
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

    def checkValid(self, node, visited_node, visited_pos):
        if node.position not in self.wall_pos and node.position not in visited_pos:
            #print('appended')
            visited_node.append(node)
            visited_pos.append(node.position)
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

        # Initialize start/end nodes
        self.visited_node_f.append(start_node)
        self.visited_node_r.append(end_node)

        while len(fwd_queue) and len(rev_queue) > 0:
            # Parent variables of parent nodes at the given time
            first_out_f = fwd_queue.pop(0)
            first_out_r = rev_queue.pop(0)

            for m in ['L', 'R', 'U', 'D']:
                #print('ioahsoiadjioajiodjasdasdasdhdioad')
                i, j = first_out_f.position
                a, b = first_out_r.position
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

                new_node_f = Node((i, j), first_out_f)
                new_node_r = Node((a, b), first_out_r)

                if self.checkValid(new_node_f, self.visited_node_f, self.visited_pos_f):
                    #print('valid1')
                    print(new_node_f.position)
                    self.draw_all_paths(new_node_f.position, VIOLETRED)
                    fwd_queue.append(new_node_f)

                if self.checkValid(new_node_r, self.visited_node_r, self.visited_pos_r):
                    #print('valid2')
                    self.draw_all_paths(new_node_r.position, TURQUOISE)
                    rev_queue.append(new_node_r)

                if self.findRoute((i, j), self.visited_pos_r):
                    print('route found, but idk what to do')
                    #print('found')
                    self.route_found = True
                    current_f = first_out_f
                    current_r = None

                    for node in self.visited_node_r:
                        #print('three')
                        if node.position == (i,j):
                            current_r = node

                    while current_f is not None:
                        print('adding 1')
                        self.route_f.append(current_f.position)
                        current_f = current_f.parent

                    while current_r is not None:
                        print('adding 2')
                        self.route_r.append(current_r.position)
                        current_r = current_r.parent
                    print('about to break')
                    break

                elif self.findRoute((a, b), self.visited_pos_f):
                    print('route found, but idk what to do')
                    self.route_found = True
                    current_r = first_out_r
                    current_f = None

                    for node in self.visited_node_f:
                        if node.position == (a, b):
                            current_f = node

                    while current_f is not None:
                        print('adding 1')
                        self.route_f.append(current_f.position)
                        current_f = current_f.parent

                    while current_r is not None:
                        print('adding 2')
                        self.route_r.append(current_r.position)
                        current_r = current_r.parent
                    print('about to break')
                    break


            if self.route_found:
                break

