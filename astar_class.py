from settings import *

class AStar():
    def __init__(self, start_node_x, start_node_y, end_node_x, end_node_y):
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.g = 0
        self.h = 0
        self.f = 0

