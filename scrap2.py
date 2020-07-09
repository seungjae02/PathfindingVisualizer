start_node = Node((self.start_node_x, self.end_node_y), None)
        start_node.G = start_node.H = start_node.F = 0
        end_node = Node((self.end_node_x, self.end_node_y), None)
        end_node.G = end_node.H = end_node.F = 0

        self.open_list.append(start_node)

        while len(self.open_list) > 0:
            current_node = self.open_list[0]
            current_index = 0
            print('start', current_node.position)
            for index, item in enumerate(self.open_list):
                if item.F < current_node.F:
                    current_node = item
                    current_index = index

            self.open_list.pop(current_index)
            self.closed_list.append(current_node)


            self.draw_all_paths(current_node.position)

            if self.findEnd(current_node):
                current = current_node
                while current is not None:
                    self.route.append(current_node)
                    current = current.parent
                self.route_found = True

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if not self.check_valid(node_position):
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            for child in children:
                better_node = True

                # Create the f, g, and h values
                child.G = current_node.G + 1
                print('asd', child.position)
                print('asd', end_node.position)
                child.H = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.F = child.G + child.H

                # Child is already in the open list
                for open_node in self.open_list:
                    if child == open_node and child.G > open_node.G:
                        better_node = False
                        continue

                if not better_node:
                    continue

                # Add the child to the open list
                self.open_list.append(child)