class Nodes:
    def __int__(self):
        self.start_node = None
        self.end_node = None
        self.wall_pos = []
        self.check_nodes()

    # implement a way to set start and end nodes
    # check for wall nodes
    def check_nodes(self):
        with open('nodes.txt') as nodes_file:
            for yidx, line in enumerate(nodes_file):
                for xidx, pos in enumerate(line):
                    if pos == 'A':
                        self.start_node = ((xidx, yidx))
                        print('start pos coord:', self.start_node)
                    elif pos == 'B':
                        self.end_node = ((xidx, yidx))
                        print('end pos coord:', self.end_node)
                    elif pos == 1:
                        self.wall_pos.append((xidx, yidx))