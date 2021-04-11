import algorithm
import settings


class DepthFirst(algorithm.VisualisableAlgorithm):
    def __init__(self, app, pos_start, pos_end, wall_pos):
        algorithm.VisualisableAlgorithm.__init__(self, app, pos_start, pos_end, wall_pos)
        self.visited = [self.pos_start]
        self.route = None
        self.route_found = False

    def execute(self):
        stack = []
        first_in = self.pos_start
        stack.append(first_in)

        moves_stack = []
        moves_first_in = ''
        moves_stack.append(moves_first_in)

        while len(stack) > 0:
            last_out = stack.pop()
            moves_last_out = moves_stack.pop()

            for m in ['L', 'R', 'U', 'D']:
                i, j = last_out
                if m == 'L':
                    i -= 1
                elif m == 'R':
                    i += 1
                elif m == 'U':
                    j -= 1
                elif m == 'D':
                    j += 1

                move_update = moves_last_out + m

                if self.find_end((i, j)):
                    self.route = move_update
                    self.route_found = True
                    break

                if self.is_valid((i, j)):
                    stack.append((i, j))
                    moves_stack.append(move_update)
                    self.draw_all_paths((i, j), settings.TAN)

            if self.route_found:
                break

    def get_routes(self):
        """For BFS and DFS mainly."""
        route = []
        x, y = self.pos_start
        for move in self.route:
            if move == 'L':
                x -= 1
            elif move == 'R':
                x += 1
            elif move == 'U':
                y -= 1
            elif move == 'D':
                y += 1
            route.append((x, y))
        return [route]

    def is_valid(self, position):
        if position not in self.wall_pos and position not in self.visited:
            self.visited.append(position)
            return True
        return False

    def find_end(self, first_in):
        if first_in == self.pos_end:
            return True
        return False
