import algorithm
import settings


class Bidirectional(algorithm.VisualisableAlgorithm):
    def __init__(self, app, pos_start, pos_end, wall_pos):
        algorithm.VisualisableAlgorithm.__init__(self, pos_start, pos_end, app)
        self.wall_pos = wall_pos
        self.visited_pos_f = {self.pos_start}
        self.visited_pos_r = {self.pos_end}
        self.visited_node_f = dict()
        self.visited_node_r = dict()
        self.route_f = []
        self.route_r = []
        self.route_found = False

    def execute(self):
        start_node = Node(self.pos_start, None)
        end_node = Node(self.pos_end, None)
        fwd_queue = [start_node]
        rev_queue = [end_node]

        # Initialize start/end nodes
        self.visited_node_f[start_node.position] = start_node
        self.visited_node_r[end_node.position] = end_node

        while len(fwd_queue) and len(rev_queue) > 0:
            # Parent variables of parent nodes at the given time
            first_out_f = fwd_queue.pop(0)
            first_out_r = rev_queue.pop(0)

            for m in ['L', 'R', 'U', 'D']:
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

                if self.is_valid(new_node_f, self.visited_node_f, self.visited_pos_f):
                    # print(new_node_f.position)
                    self.draw_all_paths(new_node_f.position, settings.VIOLETRED)
                    fwd_queue.append(new_node_f)

                if self.is_valid(new_node_r, self.visited_node_r, self.visited_pos_r):
                    self.draw_all_paths(new_node_r.position, settings.TURQUOISE)
                    rev_queue.append(new_node_r)

                # Check if some route has been found from either ends
                if find_route((i, j), self.visited_pos_r):
                    self.route_found = True

                    # Backtrack the route from each ends
                    self.back_track(self.visited_node_r, new_node_f.position, first_out_f)
                    break

                elif find_route((a, b), self.visited_pos_f):
                    self.route_found = True

                    # Backtrack the route from each ends
                    self.back_track(self.visited_node_f, new_node_r.position, first_out_r)
                    break

            if self.route_found:
                print(self.route_f)
                # print(self.route_r)
                break

    def is_valid(self, node, visited_node, visited_pos):
        if node.position not in self.wall_pos and node.position not in visited_pos:
            visited_node[node.position] = node
            visited_pos.add(node.position)
            return True
        return False

    def back_track(self, opp_visited_node_list, converge_node_pos, first_out):

        current = first_out
        current_opp = opp_visited_node_list[converge_node_pos]

        while current is not None:
            self.route_f.append(current.position)
            current = current.parent

        while current_opp is not None:
            self.route_r.append(current_opp.position)
            current_opp = current_opp.parent


def find_route(first_out, opp_visited):
    if first_out in opp_visited:
        return True
    return False


class Node:
    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent
