import algorithm
import settings


class Dijkstra(algorithm.VisualisableAlgorithm):
    def __init__(self, app, pos_start, pos_end, wall_pos):
        algorithm.VisualisableAlgorithm.__init__(self, pos_start, pos_end, app)
        self.wall_pos = wall_pos
        self.route = []
        self.route_found = False
        self.open_list = []
        self.closed_list = []

    def execute(self):
        start_node = Node(self.pos_start, None)
        start_node.distance = 0
        end_node = Node(self.pos_end, None)

        self.open_list.append(start_node)

        while len(self.open_list) > 0:
            # Search for the node with the lowest distance traveled from the start node
            current_node = self.open_list[0]
            current_index = 0
            for index, node in enumerate(self.open_list):
                if node.distance < current_node.distance:
                    current_node = node
                    current_index = index

            # Check if the algorithm has reached the end node
            if self.find_end(current_node.position):
                current = current_node
                while current is not None:
                    self.route.append(current.position)
                    current = current.parent
                self.route.pop(0)
                self.route_found = True
                break

            self.draw_all_paths(current_node.position, settings.TAN)
            self.generate_children(current_node)

            self.open_list.pop(current_index)
            self.closed_list.append(current_node.position)

    def is_valid(self, position):
        if position not in self.wall_pos and position not in self.closed_list:
            return True
        return False

    def find_end(self, position):
        if position == self.pos_end:
            return True
        return False

    def generate_children(self, parent):
        parent_pos = parent.position
        for m in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            child_pos = (parent_pos[0] + m[0], parent_pos[1] + m[1])
            if self.is_valid(child_pos):
                child = Node(child_pos, parent)
                self.distance_calc(child, parent, m)

                if self.check_append(child) and self.check_wall_corner(parent, m):
                    self.open_list.append(child)

    def check_wall_corner(self, parent, move):
        i, j = parent.position
        if move == (-1, 1):
            x, y = 0, 1
            a, b = -1, 0
        elif move == (1, 1):
            x, y = 0, 1
            a, b = 1, 0
        elif move == (1, -1):
            x, y = 1, 0
            a, b = 0, -1
        else:
            x, y = 0, -1
            a, b = -1, 0

        if (i+x, j+y) not in self.wall_pos or (i+a, j+b) not in self.wall_pos and move not in self.wall_pos:
            return True
        return False

    def distance_calc(self, child, parent, m):
        # Determine if move is orthogonal or diagonal
        sum_difference = abs(sum(m))
        # Add G-Score according to the type of move
        if sum_difference == 1:
            child.distance = parent.distance + 10
        elif sum_difference == 0 or sum_difference == 2:
            child.distance = parent.distance + 14

    def check_append(self, child):
        for open_node in self.open_list:
            if child.position == open_node.position and child.distance >= open_node.distance:
                return False
        return True


class Node:
    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent
        # distance is the distance traveled from the start node
        self.distance = 0
