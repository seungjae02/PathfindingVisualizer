import algorithm
import settings


class BreadthFirst(algorithm.VisualisableAlgorithm):
    def __init__(self, app, pos_start, pos_end, wall_pos):
        algorithm.VisualisableAlgorithm.__init__(self, pos_start, pos_end, app)
        self.wall_pos = wall_pos
        self.visited = [self.pos_start]
        self.route = None
        self.route_found = False

    def execute(self):
        queue = [self.pos_start]
        moves_queue = ['']

        while len(queue) > 0:
            # Parent variables of parent nodes at the given time
            first_out = queue.pop(0)
            first_moves = moves_queue.pop(0)
            for m in ['L', 'R', 'U', 'D']:
                i, j = first_out
                # print('parent:', i, j)
                if m == 'L':
                    i -= 1
                elif m == 'R':
                    i += 1
                elif m == 'U':
                    j -= 1
                elif m == 'D':
                    j += 1

                # Make new variable "latest_moves" for adding onto the queue again,
                # because you don't want the 'parent' variable to change
                latest_moves = first_moves + m
                if self.is_valid((i, j)):
                    self.draw_all_paths((i, j), settings.TAN)
                    queue.append((i, j))
                    moves_queue.append(latest_moves)

                if self.find_end((i, j)):
                    self.route = latest_moves
                    self.route_found = True
                    break

            if self.route_found:
                break

    def is_valid(self, position):
        if position not in self.wall_pos and position not in self.visited:
            self.visited.append(position)
            return True
        return False

    def find_end(self, first_out):
        if first_out == self.pos_end:
            return True
        return False
