class BreadthFirst():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.visited = []
        self.route = None

    def checkValid(self, move):
        if move not in self.wall_pos and move not in self.visited:
            return True
        return False

    def findEnd(self, first_in):
        if first_in == (self.end_node_x, self.end_node_y):
            return True
        return False

    def execute_bfs(self):
        queue = [(self.start_node_x, self.start_node_y)]

        while not self.findEnd(first_in):
            # first out
            i, j = queue.pop(0)
            for m in ['L', 'R', 'U', 'D']:
                if m == 'L':
                    i -= 1
                elif m == 'R':
                    i += 1
                elif m == 'U':
                    j -= 1
                elif m == 'D':
                    j += 1
                if self.checkValid((i, j)):
                    queue.append((i, j))
                    first_in = (i, j)

        print('found! The end node is at:', first_in)

