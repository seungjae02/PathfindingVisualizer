import algorithm
import settings


class AStar(algorithm.VisualisableAlgorithm):
    def __init__(self, app, pos_start, pos_end, wall_pos):
        algorithm.VisualisableAlgorithm.__init__(self, pos_start, pos_end, app)
        self.open_list = []
        self.closed_list = []
        self.wall_pos = wall_pos
        self.route = []
        self.route_found = False

    def execute(self):
        # Initialize Start/End Nodes
        start_node = Node(self.pos_start, None)
        start_node.G = start_node.H = start_node.F = 0
        end_node = Node(self.pos_end, None)
        end_node.G = end_node.H = end_node.F = 0

        self.open_list.append(start_node)

        print(start_node.position)
        print(end_node.position)

        while len(self.open_list) > 0:
            current_node = self.open_list[0]
            current_index = 0

            # Get the node with lowest F-Cost
            for index, node in enumerate(self.open_list):
                if node.F < current_node.F:
                    current_node = node
                    current_index = index

            # Check if route has been found
            if self.find_end(current_node.position):
                current = current_node
                # Append path until the current node becomes none (start node has a parent of None)
                while current is not None:
                    self.route.append(current.position)
                    current = current.parent
                self.route.pop(0)
                self.route_found = True
                break

            self.generate_children(current_node, end_node)
            self.draw_all_paths(current_node.position, settings.TAN)

            self.open_list.pop(current_index)
            self.closed_list.append(current_node.position)

    def is_valid(self, position):
        if position not in self.wall_pos and position not in self.closed_list:
            return True
        return False

    def find_end(self, current):
        if current == self.pos_end:
            return True
        return False

    def generate_children(self, parent, end_node):
        print('generating children')
        parent_pos = parent.position
        for m in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            child_pos = (parent_pos[0] + m[0], parent_pos[1] + m[1])
            if self.is_valid(child_pos):
                child = Node(child_pos, parent)
                self.calc_g(child, parent, m)
                self.calc_h(child, end_node)
                self.calc_f(child)

                # If node not already added to the open list AND node isn't cutting corners around wall, then append
                if self.append_to_open(child) and self.check_wall_corner(m, parent_pos):
                    self.open_list.append(child)

    def append_to_open(self, child):
        # If node is already in open list and the new node has a higher F-score
        # than node about to be replaced, return False
        # IMPORTANT NOTE: Even if another node with same position with different F value gets added,
        # the node with higher F-score will never be checked, so it's fine to have two nodes with same position.
        for open_node in self.open_list:
            if child.position == open_node.position and child.F >= open_node.F:
                return False

        return True

    def check_wall_corner(self, move, parent_pos):
        if move == (-1, 1) or move == (1, 1) or move == (1, -1) or move == (-1, -1):
            i, j = parent_pos
            (m, n) = move
            # (x, y) = Orthogonal
            if move == (1, 1):
                (x, y) = (0, 1)
                (a, b) = (1, 0)
            elif move == (1, -1):
                (x, y) = (1, 0)
                (a, b) = (0, -1)
            elif move == (-1, -1):
                (x, y) = (0, -1)
                (a, b) = (-1, 0)
            else:
                (x, y) = (-1, 0)
                (a, b) = (0, 1)

            # If cutting corner case, return False
            if (i+x, j+y) in self.wall_pos or (i+a, i+b) in self. wall_pos and (i+m, j+n) not in self.wall_pos:
                return False
            return True
        else:
            return True

    def calc_g(self, child, parent, m):
        # Determine if move is orthogonal or diagonal
        sum_difference = abs(sum(m))
        # Add G-Score according to the type of move
        if sum_difference == 1:
            child.G = parent.G + 10
        elif sum_difference == 0 or sum_difference == 2:
            child.G = parent.G + 14

    def calc_h(self, child, end_node):
        child.H = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)

    def calc_f(self, child):
        child.F = child.G + child.H


class Node:
    def __init__(self, position = None, parent = None):
        self.position = position
        self.parent = parent
        self.G = 0
        self.H = 0
        self.F = 0
