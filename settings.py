# Screen Settings
WIDTH = 1536
HEIGHT = 768

GRID_WIDTH = WIDTH - 240 - 24*2
GRID_HEIGHT = HEIGHT - 24*2

# GS MEANS Grid-Start
GS_X = 264
GS_Y = 24
# GE MEANS Grid-End
GE_X = 1512
GE_Y = 744

# Font Settings
FONT = 'Arial Black'
FONT_SIZE = 16

# Colour Settings
WHITE = (255, 255, 255)
AQUAMARINE = (127, 255, 212)
BLACK = (0, 0, 0)
ALICE = (240, 248, 255)
STEELBLUE = (110, 123, 139)
MINT = (189, 252, 201)
SPRINGGREEN = (0, 255, 127)
TOMATO = (255, 99, 71)
ROYALBLUE = (72, 118, 255)
TAN = (255, 165, 79)
RED = (255, 0, 0)
VIOLETRED = (255, 130, 171)
TURQUOISE = (30, 144, 255)


def build_walls(max_x, max_y):
    walls = []
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if (x in [0, max_x]) or (y in [0, max_y]):
                walls.append((x, y))
    return walls


# Coordinates of border
wall_nodes_coords_list = build_walls(53, 31)
